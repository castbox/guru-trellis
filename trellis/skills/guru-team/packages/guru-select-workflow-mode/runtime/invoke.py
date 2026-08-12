from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json


def _value(package_root: Path, raw: str, field: str, *, locator: bool = False):
    if raw == "-":
        raw = sys.stdin.read()
    elif locator:
        path = Path(raw)
        candidates = [path] if path.is_absolute() else [Path.cwd() / path, package_root / path]
        path = next((item for item in candidates if item.is_file() and not item.is_symlink()), None)
        if path is None:
            raise CommandError("unsafe_path", field, "Use a safe regular JSON file.")
        raw = path.read_text()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CommandError("invalid_json", field, "Provide one valid JSON object.") from exc
    if not isinstance(value, dict):
        raise CommandError("invalid_json", field, "Provide one valid JSON object.")
    return value


def _schema(package_root: Path, name: str) -> Path:
    path = package_root / "schemas" / name
    if not path.is_file() or path.is_symlink():
        raise CommandError("missing_contract", str(path), "Restore the declared package schema.")
    return path


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--invocation")
    parser.add_argument("--input")
    parser.add_argument("--owner-result")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the exact command help contract.") from exc
    if bool(args.invocation) == bool(args.input):
        raise CommandError("invalid_arguments", "arguments", "Provide exactly one invocation or public input transport.")
    if args.invocation:
        envelope = _value(package_root, args.invocation, "invocation")
        public_input = envelope.get("public_input")
        owner_result = envelope.get("owner_result")
    else:
        public_input = _value(package_root, args.input, "input", locator=True)
        owner_result = _value(package_root, args.owner_result, "owner_result", locator=True) if args.owner_result else None
    if not isinstance(public_input, dict) or not isinstance(owner_result, dict):
        raise CommandError("invalid_arguments", "owner_result", "Provide the completed semantic owner result.")
    profile = public_input.get("profile")
    input_schema = {
        "initial_request": "public-input-initial.schema.json",
    }.get(profile)
    if input_schema is None:
        raise CommandError("schema_mismatch", "input.profile", "Use one declared workflow-mode selection profile.")
    validate_json(public_input, _schema(package_root, input_schema), "input")
    exit_id = owner_result.get("typed_exit")
    examples = {
        "standard_intake": "public-standard-intake-output.json",
        "task_free": "public-task-free-output.json",
        "blocked": "public-blocked-output.json",
    }
    if exit_id not in examples:
        raise CommandError("unknown_typed_exit", "owner_result.typed_exit", "Return one declared typed exit.")
    if owner_result.get("mode") != public_input.get("mode") or owner_result.get("continuation_id") != public_input.get("continuation_id"):
        raise CommandError("stale_identity", "owner_result", "Rerun workflow-mode selection for the exact continuation.", 3)
    output = json.loads((package_root / "examples" / examples[exit_id]).read_text())
    output["exit_id"] = exit_id
    if "mode" in output and public_input.get("mode"):
        output["mode"] = public_input["mode"]
    schema_name = examples[exit_id].replace(".json", ".schema.json")
    validate_json(output, _schema(package_root, schema_name), "stdout")
    return copy.deepcopy(output)
