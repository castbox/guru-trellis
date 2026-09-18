from __future__ import annotations

import argparse
from pathlib import Path

from check import check
from common import (
    OUTPUT_SCHEMAS,
    load_json,
    parse,
    project_output,
    repo_root,
    retire_checkpoint,
    task_dir,
)
from record import record
from runtime.schema import validate_json


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    args = parse(parser, argv)
    repo = repo_root(args.root)
    public = load_json(repo, package_root, args.input, "input")
    semantic = load_json(repo, package_root, args.semantic_result, "semantic_result")
    record(package_root, repo, public, semantic)
    checked = check(package_root, repo, public["task_ref"])
    gate = checked["gate"]
    output = project_output(gate)
    validate_json(output, package_root / "schemas" / OUTPUT_SCHEMAS[output["exit_id"]], "stdout")
    retire_checkpoint(repo, task_dir(repo, public["task_ref"]))
    return output

