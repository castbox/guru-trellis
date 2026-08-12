from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from runtime.io import CommandError


def _owner(package_root: Path):
    path = package_root / "runtime/owner.py"
    spec = importlib.util.spec_from_file_location("verify_owner", path)
    if spec is None or spec.loader is None:
        raise CommandError("internal_error", "runtime.owner", "Restore the package owner runtime.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    if command["id"] == "show-extension-version":
        from version import run as show_version

        return show_version(argv)
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--public-input")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError(
            "invalid_arguments",
            "arguments",
            "Use the exact command help contract.",
        ) from exc
    return _owner(package_root).cmd_check_extension_verification(args)
