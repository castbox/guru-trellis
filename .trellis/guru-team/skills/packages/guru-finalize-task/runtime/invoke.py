from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any

from common import call_owner, parse_arguments


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _o(package_root: Path):
    return _load_module("finalize_owner", package_root / "runtime/owner.py")


def _transaction(package_root: Path):
    return _load_module(
        "finalize_transaction",
        package_root / "runtime/transaction.py",
    )


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--review-input")
    parser.add_argument("--confirmed-preview-sha256")
    for name in ("repo", "base_branch", "remote", "title", "task_name"):
        parser.add_argument("--" + name.replace("_", "-"))
    parser.add_argument("--validation", action="append")
    return parse_arguments(parser, argv)


def run(
    package_root: Path,
    command: dict[str, Any],
    argv: list[str],
) -> dict[str, Any]:
    del command
    args = _parse_args(argv)
    owner = _o(package_root)

    def invoke_owner() -> dict[str, Any]:
        if not args.review_input:
            raise owner.WorkflowError(
                "Finalization public invocation requires --review-input.",
                exit_code=2,
            )
        root = owner.repo_root(Path(args.root or "."))
        public_input, _ = owner.finalization_public_input(root, args.input)
        if public_input["profile"] == "archived_review_refresh":
            return owner.invoke_archived_review_refresh(root, args, public_input)
        return _transaction(package_root).execute_confirmed_transaction(owner, args)

    return call_owner(owner, invoke_owner, public=True)
