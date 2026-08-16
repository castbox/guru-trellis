from __future__ import annotations

import argparse
import copy
from pathlib import Path

from common import _authoring, check_value, parse, stdin_object


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input", required=True)
    args = parse(parser, argv)
    recorded = stdin_object(args.input, "input")
    receipt = check_value(package_root, recorded)
    return {"schema_version": "1.0", "semantic_result": _authoring(recorded), "validation_receipt": copy.deepcopy(receipt)}
