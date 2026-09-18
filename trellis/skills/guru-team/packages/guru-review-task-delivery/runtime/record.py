from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
from pathlib import Path

from common import (
    cycle_ref,
    digest,
    dirty_paths,
    load_json,
    parse,
    rel,
    repo_root,
    store_checkpoint,
    task_dir,
    task_facts,
    validate_semantic,
)
from runtime.io import CommandError
from runtime.schema import validate_json


def record(package_root: Path, repo: Path, public: dict, semantic: dict, dry_run: bool = False) -> dict:
    if public.get("profile") != "delivery_review":
        raise CommandError("schema_mismatch", "input.profile", "Use one declared Delivery Review profile.")
    validate_json(public, package_root / "schemas/public-delivery-review-input.schema.json", "input")
    target = task_dir(repo, public["task_ref"])
    if rel(repo, target) != public["task_ref"]:
        raise CommandError("stale_identity", "task_ref", "Use the exact current task.", 3)
    facts = task_facts(repo, target)
    branch_review_commit = public["branch_review_commit"]
    if branch_review_commit != facts["head"]:
        raise CommandError("stale_identity", "branch_review_commit", "Review the exact current HEAD.", 3)
    if dirty_paths(repo):
        raise CommandError("stale_identity", "worktree", "Commit or remove all post-review changes.", 3)
    exit_id = validate_semantic(package_root, public, semantic, facts["scope"])
    value = {
        "schema_version": "1.0",
        "skill_id": "guru-review-task-delivery",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "task_ref": public["task_ref"],
        "profile": public["profile"],
        "mode": public["mode"],
        "branch_review_commit": branch_review_commit,
        "reviewed_head": facts["head"],
        "base_ref": facts["base_ref"],
        "base_head": facts["base_head"],
        "delivery_cycle_ref": cycle_ref(public["task_ref"], facts["head"], semantic["pr_payload"]),
        "semantic_result": copy.deepcopy(semantic),
    }
    value["facts_sha256"] = digest({key: copy.deepcopy(item) for key, item in value.items() if key != "generated_at"})
    validate_json(value, package_root / "schemas/delivery-review-gate.schema.json", "checkpoint")
    duplicate = False
    path = None
    if not dry_run:
        path, duplicate = store_checkpoint(repo, target, value)
    return {
        "status": "validated" if dry_run else ("duplicate" if duplicate else "recorded"),
        "task_ref": public["task_ref"],
        "typed_exit": exit_id,
        "checkpoint_id": "delivery-review-gate",
        "checkpoint_path": None if path is None else str(path),
        "dry_run": dry_run,
    }


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parse(parser, argv)
    repo = repo_root(args.root)
    public = load_json(repo, package_root, args.input, "input")
    semantic = load_json(repo, package_root, args.semantic_result, "semantic_result")
    return record(package_root, repo, public, semantic, args.dry_run)
