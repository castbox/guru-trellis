from __future__ import annotations

import argparse
from pathlib import Path

from common import checkpoint, file_set, load, parse, rel, root, task, planning_directory
from runtime.io import CommandError
from runtime.schema import validate_json


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    if command["id"] == "resolve-planning-artifacts":
        from artifacts import run as resolve_artifacts

        return resolve_artifacts(argv)
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--task")
    parser.add_argument("--delivery-key", required=True)
    parser.add_argument(
        "--require-exit",
        choices=("approved", "revision_required", "clarify_scope", "blocked"),
    )
    args = parse(parser, argv)
    repo = root(package_root, args.root)
    task_dir = task(repo, args.task)
    from runtime.io import read_json
    key = read_json(args.delivery_key, "delivery_key")
    directory = planning_directory(repo, task_dir, key)
    path = checkpoint(repo, task_dir, "planning-approval.json", key)
    value = load(repo, package_root, str(path), "artifact")
    validate_json(value, package_root / "schemas/planning-approval-delivery.schema.json", "artifact")
    paths = sorted(rel(repo, directory / name) for name in ("prd.md", "design.md", "implement.md"))
    if (
        value["task_ref"] != rel(repo, task_dir)
        or value["delivery_key"] != key
        or value["planning_paths"] != paths
        or value["reviewed_content_sha256"] != file_set(repo, paths)
    ):
        raise CommandError(
            "stale_identity",
            "artifact",
            "Rerun planning review from current files.",
            3,
        )
    if args.require_exit and value["typed_exit"] != args.require_exit:
        raise CommandError(
            "stale_identity",
            "typed_exit",
            "Rerun planning for the required exit.",
            3,
        )
    return {
        "status": "ok",
        "artifact_path": str(path),
        "task_dir": str(task_dir),
        "typed_exit": value["typed_exit"],
        "consumer": value["consumer"],
    }
