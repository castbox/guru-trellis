from __future__ import annotations
import argparse, importlib.util
from pathlib import Path
from common import call_owner, parse_arguments
from reviewed_content import run as reviewed_content_run
def _owner(root):
    spec=importlib.util.spec_from_file_location("publication_owner",root/"runtime/owner.py"); module=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(module); return module
def run(package_root: Path, command: dict, argv: list[str])->dict:
    if command["id"] == "review-task-publication-content-identity":
        return reviewed_content_run(package_root, command, argv)
    p=argparse.ArgumentParser(add_help=False); p.add_argument("--root"); p.add_argument("--task"); p.add_argument("--expected-exit")
    owner = _owner(package_root)
    return call_owner(
        owner,
        owner.cmd_check_task_publication_review,
        parse_arguments(p, argv),
    )
