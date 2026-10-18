from __future__ import annotations

from pathlib import Path
from typing import Any

from owner import check_gate, execute, parser, plan_from_input, read_json, repo_root, validate_public_input


def run(package_root: Path, command: dict[str, Any], argv: list[str]) -> dict[str, Any]:
    del package_root, command
    args = parser("execute").parse_args(argv)
    root = repo_root(Path(args.root or "."))
    context = plan_from_input(root, validate_public_input(read_json(args.input)))
    if context.get("typed_exit") != "preview":
        return context["output"]
    check_gate(root, context, (root / args.gate).resolve())
    return execute(root, context)
