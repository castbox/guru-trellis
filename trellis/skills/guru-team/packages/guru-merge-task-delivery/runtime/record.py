from __future__ import annotations
import argparse
from pathlib import Path
from owner import cmd_record

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--review-input", required=True)
    return cmd_record(package_root, parser.parse_args(argv))
