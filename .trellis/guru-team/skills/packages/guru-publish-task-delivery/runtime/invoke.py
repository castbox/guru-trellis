from __future__ import annotations

from pathlib import Path
from typing import Any

from owner import invoke, parser, repo_root


def run(package_root: Path, command: dict[str, Any], argv: list[str]) -> dict[str, Any]:
    del package_root, command
    args = parser("invoke").parse_args(argv)
    return invoke(repo_root(Path(args.root or ".")), args.input, args.review_input, args.confirmed_preview_sha256)
