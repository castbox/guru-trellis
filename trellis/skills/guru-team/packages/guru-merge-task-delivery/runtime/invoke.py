from __future__ import annotations
import argparse
from pathlib import Path
from owner import cmd_invoke, repo_root, load_json

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
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
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--review-input", required=True)
    args = parser.parse_args(argv)
    root = repo_root(args.root)
    public = load_json(root,package_root,args.input,"input")
    if public.get("profile") not in {"delivery_ready_for_merge", "delivery_scope_withdrawal", "delivery_scope_revision", "delivery_merged_recovery"}:
        from runtime.io import CommandError
        raise CommandError("schema_mismatch", "profile", "Use the current public Delivery merge profiles; legacy Task merge is pinned-old-only.")
    if public.get("profile") == "delivery_merged_recovery":
        from manual_recovery import invoke
        return invoke(root, package_root, public, load_json(root, package_root, args.review_input, "review_input"))
    if public.get("profile") == "delivery_scope_revision":
        from runtime.delivery_projection.scope_revision import revise
        return revise(root, package_root, public, load_json(root, package_root, args.review_input, "review_input"), owner_role="delivery", expected_phase="publishing")
    if public.get("profile") == "delivery_scope_withdrawal":
        from runtime.delivery_projection.withdrawal import stop
        return stop(root,package_root,public,load_json(root,package_root,args.review_input,"review_input"),owner_role="delivery",expected_phase="publishing")
    return cmd_invoke(package_root,args)
