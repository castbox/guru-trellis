from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json

PROFILES = {"bootstrap_foundation", "task_impact_sync", "promotion", "repair"}
EXITS = {
    "baseline_current": "public-baseline-current-output.schema.json",
    "sync_required": "public-sync-required-output.schema.json",
    "baseline_incomplete": "public-baseline-incomplete-output.schema.json",
    "architecture_conflict": "public-architecture-conflict-output.schema.json",
    "contract_incomplete": "public-contract-incomplete-output.schema.json",
    "fitness_regression": "public-fitness-regression-output.schema.json",
    "blocked": "public-blocked-output.schema.json",
}

def _json(value: str, field: str, locator: bool = False) -> dict:
    if value == "-":
        value = sys.stdin.read()
    elif locator:
        path = Path(value)
        if not path.is_absolute():
            path = Path.cwd() / path
        if not path.is_file() or path.is_symlink():
            raise CommandError("unsafe_path", field, "Use a safe regular JSON file.")
        value = path.read_text()
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise CommandError("invalid_json", field, "Provide one valid JSON object.") from exc
    if not isinstance(parsed, dict):
        raise CommandError("invalid_json", field, "Provide one valid JSON object.")
    return parsed

def _schema(package_root: Path, name: str) -> Path:
    path = package_root / "schemas" / name
    if not path.is_file() or path.is_symlink():
        raise CommandError("schema_mismatch", name, "Restore the declared package schema.")
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
    envelope = _json(args.invocation, "invocation") if args.invocation else None
    public = envelope.get("public_input") if envelope else _json(args.input, "input", True)
    owner = envelope.get("owner_result") if envelope else _json(args.owner_result, "owner_result", True)
    if not isinstance(public, dict) or not isinstance(owner, dict):
        raise CommandError("invalid_arguments", "owner_result", "Provide a completed semantic owner result.")
    profile = public.get("profile")
    if profile not in PROFILES:
        raise CommandError("schema_mismatch", "profile", "Use one declared architecture baseline profile.")
    validate_json(public, _schema(package_root, "public-input.schema.json"), "input")
    if owner.get("profile") != profile or owner.get("continuation_id") != public.get("continuation_id"):
        raise CommandError("stale_identity", "owner_result", "Rerun the profile from current baseline facts.", 3)
    exit_id = owner.get("typed_exit")
    if exit_id not in EXITS:
        raise CommandError("unknown_typed_exit", "owner_result.typed_exit", "Return one declared architecture exit.")
    output = {"exit_id": exit_id}
    for key in ("baseline", "scope", "freshness", "consumer", "reason"):
        if key in owner:
            output[key] = owner[key]
    validate_json(output, _schema(package_root, EXITS[exit_id]), "stdout")
    return copy.deepcopy(output)
