from __future__ import annotations

import argparse
from pathlib import Path

from context import capture
from runtime.io import CommandError, read_json


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Provide --input with the selected public input or dash for stdin.") from exc
    return capture(package_root, read_json(args.input, "public_input"))
