from __future__ import annotations

import argparse
from pathlib import Path

from common import load_checkpoint, parse, repo_root, task_dir, validate_gate


def check(package_root: Path, repo: Path, task_ref: str, expected_exit: str | None = None) -> dict:
    target = task_dir(repo, task_ref)
    path, value = load_checkpoint(repo, target)
    validate_gate(package_root, repo, value, expected_exit)
    return {
        "status": "passed",
        "task_ref": value["task_ref"],
        "typed_exit": value["semantic_result"]["route"]["typed_exit"],
        "checkpoint_id": "delivery-review-gate",
        "checkpoint_path": str(path),
        "gate": value,
    }


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--task", required=True)
    parser.add_argument("--expected-exit")
    args = parse(parser, argv)
    return check(package_root, repo_root(args.root), args.task, args.expected_exit)

