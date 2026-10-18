from __future__ import annotations

import argparse
from pathlib import Path

from check import check
from common import (
    OUTPUT_SCHEMAS,
    load_json,
    parse,
    project_output,
    repo_root,
    retire_checkpoint,
    task_dir,
)
from record import record
from runtime.schema import validate_json


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    args = parse(parser, argv)
    repo = repo_root(args.root)
    public = load_json(repo, package_root, args.input, "input")
    semantic = load_json(repo, package_root, args.semantic_result, "semantic_result")
    if public.get("profile") == "delivery_scope_revision":
        from runtime.delivery_projection.scope_revision import revise
        return revise(repo, package_root, public, semantic, owner_role="readiness", expected_phase="reviewing")
    if public.get("profile") == "delivery_scope_withdrawal":
        from runtime.delivery_projection.withdrawal import stop
        return stop(repo,package_root,public,semantic,owner_role="readiness",expected_phase="reviewing")
    if str(public.get("profile", "")).startswith("delivery_"):
        from delivery import invoke as invoke_delivery
        from runtime.task_lifecycle.errors import LifecycleContractError
        from runtime.io import CommandError
        try:
            return invoke_delivery(package_root, repo, public, semantic)
        except LifecycleContractError as exc:
            raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    from runtime.io import CommandError
    raise CommandError("schema_mismatch", "profile", "Migrate through the public Delivery contract; legacy Task readiness profiles are not active.")
