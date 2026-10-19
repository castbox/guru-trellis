from __future__ import annotations

from pathlib import Path
from typing import Any

from owner import invoke, parser, repo_root, read_json


def run(package_root: Path, command: dict[str, Any], argv: list[str]) -> dict[str, Any]:
    # Inspect only the profile before loading the separate legacy owner. Normal
    # current calls keep their original runtime dependencies and preconditions.
    import argparse as _argparse, io as _io, sys as _sys
    from runtime.io import read_json as _read_json
    _selector=_argparse.ArgumentParser(add_help=False);_selector.add_argument('--input')
    _selected,_rest=_selector.parse_known_args(argv)
    if _selected.input:
        if _selected.input=='-':
            _content=_sys.stdin.read();_sys.stdin=_io.StringIO(_content)
            _public=_read_json(_content,'input')
        else:_public=_read_json(_selected.input,'input')
        if _public.get('profile') in {'legacy_control_retirement','legacy_history_verification'}:
            import importlib.util as _util
            _spec=_util.spec_from_file_location('legacy_'+package_root.name.replace('-','_'),package_root/'runtime/legacy_maintenance.py')
            _owner=_util.module_from_spec(_spec);_spec.loader.exec_module(_owner)
            return _owner.maybe_run(package_root,argv)
    del command
    args = parser("invoke").parse_args(argv)
    public = read_json(args.input)
    if public.get("profile") not in {"delivery_draft_publish", "delivery_return_to_draft", "delivery_review_ready", "delivery_same_plan_resume", "delivery_reprepare_publication", "delivery_scope_withdrawal", "delivery_scope_revision"}:
        from owner import WorkflowError
        raise WorkflowError("Use the current public Delivery publication profiles; legacy Task publication is pinned-old-only.", code="schema_mismatch")
    if public.get("profile") == "delivery_scope_revision":
        from runtime.delivery_projection.scope_revision import revise
        return revise(repo_root(Path(args.root or ".")), package_root, public, read_json(args.review_input), owner_role="publication", expected_phase="publishing")
    if public.get("profile") == "delivery_scope_withdrawal":
        from runtime.delivery_projection.withdrawal import stop
        return stop(repo_root(Path(args.root or ".")),package_root,public,read_json(args.review_input),owner_role="publication",expected_phase="publishing")
    return invoke(repo_root(Path(args.root or ".")), args.input, args.review_input, args.confirmed_preview_sha256)
