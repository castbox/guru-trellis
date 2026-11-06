from __future__ import annotations

from pathlib import Path
from typing import Any

from owner import check_gate, parser, plan_from_input, preview, repo_root, validate_public_input
from runtime.io import read_json


def run(package_root: Path, command: dict[str, Any], argv: list[str]) -> dict[str, Any]:
    del package_root
    if command["id"] == "preview-task-delivery-publication":
        args = parser("preview").parse_args(argv)
        return preview(repo_root(Path(args.root or ".")), read_json(args.input, "input"))
    args = parser("check").parse_args(argv)
    root = repo_root(Path(args.root or "."))
    context = plan_from_input(root, validate_public_input(read_json(args.input, "input")))
    if context.get("typed_exit") != "preview":
        return context
    gate = check_gate(root, context, (root / args.gate).resolve())
    return {"status": "passed", "transaction_ref": context["transaction_ref"], "gate_sha256": gate.get("gate_sha256")}
