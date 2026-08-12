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
    parser.add_argument("--input", required=True)
    parser.add_argument("--review-input", required=True)
    return _owner(package_root).cmd_record_task_pr_merge(parser.parse_args(argv))
