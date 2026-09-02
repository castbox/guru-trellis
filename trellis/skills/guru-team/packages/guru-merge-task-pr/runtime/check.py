from __future__ import annotations
import argparse
import importlib.util
from pathlib import Path

def _owner(package_root: Path):
    path = package_root / "runtime/owner.py"
    spec = importlib.util.spec_from_file_location("guru_merge_task_pr_owner", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    if command["id"] == "watch-task-pr-checks":
        parser.add_argument("--repo", required=True)
        parser.add_argument("--pull-request", required=True, type=int)
        parser.add_argument("--expected-head", required=True)
        parser.add_argument("--timeout-seconds", type=int, default=1800)
        parser.add_argument("--interval-seconds", type=int, default=10)
        return _owner(package_root).cmd_watch_task_pr_checks(parser.parse_args(argv))
    parser.add_argument("--input", required=True)
    parser.add_argument("--gate")
    values = parser.parse_args(argv)
    handler = {"preview-task-pr-merge": _owner(package_root).cmd_preview_task_pr_merge,
               "check-task-pr-merge": _owner(package_root).cmd_check_task_pr_merge}[command["id"]]
    return handler(values)
