from __future__ import annotations

import argparse
from pathlib import Path

from common import git, load_checkpoint, parse, rel, root, task, validate_gate
from runtime.io import CommandError


def checked_gate(package_root: Path, repo: Path, task_dir: Path, expected_exit=None):
    _, value = load_checkpoint(repo, task_dir)
    if value.get("task_dir") != rel(repo, task_dir):
        raise CommandError(
            "stale_identity", "task", "Use the exact task-owned Branch Review gate.", 3
        )
    return validate_gate(package_root, repo, value, expected_exit)


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--task")
    parser.add_argument("--expected-exit")
    args = parse(parser, argv)
    repo = root(package_root, args.root)
    task_dir = task(repo, args.task)
    value = checked_gate(package_root, repo, task_dir, args.expected_exit)
    return {
        "status": "ok",
        "task_ref": rel(repo, task_dir),
        "head": git(repo, "rev-parse", "HEAD"),
        "review_commit": value["review_commit"],
        "typed_exit": value["typed_exit"],
        "facts_sha256": value["facts_sha256"],
    }
