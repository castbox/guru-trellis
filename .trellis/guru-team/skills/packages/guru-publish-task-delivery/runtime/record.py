from __future__ import annotations

from pathlib import Path
from typing import Any

from owner import parser, plan_from_input, read_json, record_gate, repo_root, validate_public_input, validate_review


def run(package_root: Path, command: dict[str, Any], argv: list[str]) -> dict[str, Any]:
    del package_root, command
    args = parser("record").parse_args(argv)
    root = repo_root(Path(args.root or "."))
    public_input = validate_public_input(read_json(args.input))
    review = validate_review(read_json(args.review_input))
    context = plan_from_input(root, public_input)
    if context.get("typed_exit") != "preview":
        return context
    path = record_gate(root, context, review)
    return {"status": "recorded", "gate": str(path.relative_to(root)), "transaction_ref": context["transaction_ref"]}
