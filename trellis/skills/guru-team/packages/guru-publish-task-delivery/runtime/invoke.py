from __future__ import annotations

from pathlib import Path
from typing import Any

from owner import invoke, parser, repo_root, read_json


def run(package_root: Path, command: dict[str, Any], argv: list[str]) -> dict[str, Any]:
    del command
    args = parser("invoke").parse_args(argv)
    public = read_json(args.input)
    if public.get("profile") not in {"delivery_review_ready", "delivery_same_plan_resume", "delivery_reprepare_publication", "delivery_scope_withdrawal", "delivery_scope_revision"}:
        from owner import WorkflowError
        raise WorkflowError("Use the current public Delivery publication profiles; legacy Task publication is pinned-old-only.", code="schema_mismatch")
    if public.get("profile") == "delivery_scope_revision":
        from runtime.delivery_projection.scope_revision import revise
        return revise(repo_root(Path(args.root or ".")), package_root, public, read_json(args.review_input), owner_role="publication", expected_phase="publishing")
    if public.get("profile") == "delivery_scope_withdrawal":
        from runtime.delivery_projection.withdrawal import stop
        return stop(repo_root(Path(args.root or ".")),package_root,public,read_json(args.review_input),owner_role="publication",expected_phase="publishing")
    return invoke(repo_root(Path(args.root or ".")), args.input, args.review_input, args.confirmed_preview_sha256)
