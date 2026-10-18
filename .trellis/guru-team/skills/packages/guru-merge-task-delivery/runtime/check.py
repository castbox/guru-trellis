from __future__ import annotations
import argparse
from pathlib import Path
from history import cmd_discover
from owner import cmd_check, cmd_preview

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--gate")
    values = parser.parse_args(argv)
    if command["id"] == "discover-task-deliveries":
        return cmd_discover(package_root, values)
    if command["id"] == "preview-task-delivery-merge":
        return cmd_preview(package_root, values)
    if command["id"] == "check-task-delivery-merge":
        return cmd_check(package_root, values)
    raise KeyError(command["id"])
