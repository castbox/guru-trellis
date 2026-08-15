from __future__ import annotations

import argparse
from pathlib import Path

from common import digest, load, parse, validate_input, validate_owner


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    args = parse(parser, argv)
    public_input = validate_input(package_root, load(package_root, args.input, "input"))
    owner = validate_owner(package_root, public_input, load(package_root, args.owner_result, "owner_result"))
    return {"status": "recorded", "typed_exit": owner["typed_exit"], "result_sha256": digest(owner)}
