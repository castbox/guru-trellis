from __future__ import annotations

from pathlib import Path
from typing import Any

from owner import invoke, parser, repo_root
from runtime.io import read_json


def run(package_root: Path, command: dict[str, Any], argv: list[str]) -> dict[str, Any]:
    # Inspect only the profile before loading the separate legacy owner. Normal
    # current calls keep their original runtime dependencies and preconditions.
    import argparse as _argparse
    _selector=_argparse.ArgumentParser(add_help=False);_selector.add_argument('--input')
    _selected,_rest=_selector.parse_known_args(argv)
    if _selected.input is not None:
        _public=read_json(_selected.input,'input')
        if _public.get('profile') in {'legacy_control_retirement','legacy_history_verification'}:
            import importlib.util as _util
            _spec=_util.spec_from_file_location('legacy_'+package_root.name.replace('-','_'),package_root/'runtime/legacy_maintenance.py')
            _owner=_util.module_from_spec(_spec);_spec.loader.exec_module(_owner)
            return _owner.maybe_run(package_root,argv,public=_public)
    del command
    args = parser("invoke").parse_args(argv)
    public = _public
    if public.get("profile") not in {"delivery_remote_draft_recovery", "delivery_remote_ready_recovery", "delivery_return_to_draft", "delivery_review_ready", "delivery_same_plan_resume", "delivery_reprepare_publication", "delivery_scope_withdrawal", "delivery_scope_revision"}:
        from owner import WorkflowError
        raise WorkflowError("Use the current public Delivery publication profiles; legacy Task publication is pinned-old-only.", code="schema_mismatch")
    if public.get("profile") == "delivery_scope_revision":
        from runtime.delivery_projection.scope_revision import revise
        return revise(repo_root(Path(args.root or ".")), package_root, public, read_json(args.review_input, "review_input"), owner_role="publication", expected_phase="publishing")
    if public.get("profile") == "delivery_scope_withdrawal":
        from runtime.delivery_projection.withdrawal import stop
        return stop(repo_root(Path(args.root or ".")),package_root,public,read_json(args.review_input, "review_input"),owner_role="publication",expected_phase="publishing")
    return invoke(repo_root(Path(args.root or ".")), public, read_json(args.review_input, "review_input"), args.confirmed_preview_sha256)
