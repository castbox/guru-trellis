from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from runtime.io import CommandError
from runtime.reviewed_content import ReviewedContentError, reviewed_content_identity
from runtime.schema import validate_json


ERROR_CODE = "reviewed_content_continuity_failed"


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument("--include-worktree", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError(
            "invalid_arguments", "arguments", "Use the exact command help contract."
        ) from exc
    root = Path(args.root or ".").resolve()
    resolved = subprocess.run(
        ["git", "rev-parse", args.commit],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if resolved.returncode != 0:
        raise CommandError(
            ERROR_CODE,
            "commit",
            "Use one commit available in the target repository.",
            3,
        )
    try:
        identity = reviewed_content_identity(root, args.commit, args.include_worktree)
    except ReviewedContentError as exc:
        raise CommandError(
            ERROR_CODE,
            "reviewed_content_sha256",
            str(exc),
            3,
        ) from exc
    output = {
        **identity,
        "commit": resolved.stdout.strip(),
        "include_worktree": args.include_worktree,
    }
    validate_json(
        output,
        package_root / "schemas/reviewed-content-identity-output.schema.json",
        "stdout",
    )
    return output
