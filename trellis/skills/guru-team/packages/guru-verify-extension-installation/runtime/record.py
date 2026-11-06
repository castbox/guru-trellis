from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from runtime.io import CommandError


def _owner(package_root: Path):
    spec = importlib.util.spec_from_file_location("verify_owner", package_root / "runtime/owner.py")
    if spec is None or spec.loader is None:
        raise CommandError("internal_error", "runtime.owner", "Restore the package owner runtime.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--execution-input", required=True)
    parser.add_argument("--review-input", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the exact command help contract.") from exc
    owner = _owner(package_root)
    return owner.extension_verification_public_call(owner.cmd_record_extension_verification, args)
