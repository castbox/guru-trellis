from __future__ import annotations

import argparse
from pathlib import Path

from common import parse, record_value, stdin_object


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input", required=True)
    args = parse(parser, argv)
    return record_value(package_root, stdin_object(args.input, "input"))
