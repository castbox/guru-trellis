from __future__ import annotations
import argparse
from pathlib import Path
from owner import cmd_invoke, repo_root, load_json

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
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
