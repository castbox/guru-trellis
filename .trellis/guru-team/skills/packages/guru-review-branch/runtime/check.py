from __future__ import annotations

import argparse
from pathlib import Path

from common import git, load_checkpoint, parse, rel, root, task, validate_gate
from runtime.io import CommandError
from reviewed_content import run as reviewed_content_run


def checked_gate(package_root: Path, repo: Path, task_dir: Path, expected_exit=None, *, delivery_key=None):
    _, value = load_checkpoint(repo, task_dir, delivery_key)
    if delivery_key is not None and value.get("delivery_key") != delivery_key:
        raise CommandError("stale_identity", "delivery_key", "Read the selected Delivery checkpoint.", 3)
    if value.get("task_dir") != rel(repo, task_dir):
        raise CommandError(
            "stale_identity", "task", "Use the exact task-owned Branch Review gate.", 3
        )
    return validate_gate(package_root, repo, value, expected_exit)


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    if command["id"] == "review-branch-content-identity":
        return reviewed_content_run(package_root, command, argv)
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--task")
    parser.add_argument("--expected-exit")
    parser.add_argument("--delivery-key")
    args = parse(parser, argv)
    repo = root(package_root, args.root)
    task_dir = task(repo, args.task)
    delivery_key = None
    if args.delivery_key:
        import json
        from common import load
        try:
            delivery_key = json.loads(args.delivery_key)
        except json.JSONDecodeError:
            delivery_key = load(repo,package_root,args.delivery_key,"delivery_key")
        from runtime.delivery_projection.adapter import DeliveryProjection
        DeliveryProjection(repo, rel(repo, task_dir)).resolve(delivery_key)
    value = checked_gate(package_root, repo, task_dir, args.expected_exit, delivery_key=delivery_key)
    return {
        # This command validates an owner-private checkpoint only. It is not
        # the public Skill exit and cannot establish Branch Review by itself.
        "status": "owner_checkpoint_validated",
        "formal_exit": False,
        "task_ref": rel(repo, task_dir),
        "head": git(repo, "rev-parse", "HEAD"),
        "review_commit": value["review_commit"],
        "typed_exit": value["typed_exit"],
        "facts_sha256": value["facts_sha256"],
    }
