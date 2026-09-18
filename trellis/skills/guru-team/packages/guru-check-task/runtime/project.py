from __future__ import annotations

import argparse
import copy
from pathlib import Path

from check import run as check_phase2
from common import checkpoint, load, parse, rel, root, task
from runtime.io import CommandError
from runtime.schema import validate_json


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    parser.add_argument("--authoring", required=True)
    args = parse(parser, argv)
    repo = root(package_root, args.root)
    public = load(repo, package_root, args.input, "input")
    owner = load(repo, package_root, args.owner_result, "owner_result")
    authoring = load(repo, package_root, args.authoring, "authoring")
    validate_json(public, package_root / "schemas/public-resolved-reconciliation-input.schema.json", "input")
    validate_json(owner, package_root / "schemas/phase2-check.schema.json", "owner_result")
    validate_json(authoring, package_root / "schemas/resolved-reconciliation-authoring.schema.json", "authoring")
    task_dir = task(repo, public["task_ref"])
    checked = check_phase2(package_root, command, ["--root", str(repo), "--task", rel(repo, task_dir)])
    expected_owner = load(repo, package_root, str(checkpoint(repo, task_dir, "phase2-check.json")), "checkpoint")
    if (
        owner != expected_owner
        or owner["task_ref"] != public["task_ref"]
        or owner["mode"] != public["mode"]
        or authoring["mode"] != public["mode"]
        or owner["typed_exit"] != "resolved_reconciliation_passed"
        or owner["consumer"] != {"kind": "skill", "id": "guru-reconcile-task-base"}
        or checked["artifact_path"] != str(checkpoint(repo, task_dir, "phase2-check.json"))
    ):
        raise CommandError("stale_identity", "owner_result", "Use the exact checked resolved-tree Phase 2 result.", 3)
    output = {
        **copy.deepcopy(authoring),
        "source_exit": "resolved_reconciliation_passed",
        "task_ref": owner["task_ref"],
        "phase2_commit_anchor": owner["phase2_capture_commit"],
    }
    target = package_root.parent / "guru-reconcile-task-base/schemas/public-resolved-candidate-input.schema.json"
    validate_json(output, target, "stdout")
    return output
