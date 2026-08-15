from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import load, parse, validate_input, validate_owner
from runtime.io import CommandError
from runtime.schema import validate_json


def _inline(raw: str, field: str) -> dict:
    if raw == "-":
        raw = sys.stdin.read()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CommandError("invalid_json", field, "Provide one valid JSON object.") from exc
    if not isinstance(value, dict):
        raise CommandError("invalid_json", field, "Provide one valid JSON object.")
    return value


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--invocation")
    parser.add_argument("--input")
    parser.add_argument("--owner-result")
    args = parse(parser, argv)
    if bool(args.invocation) == bool(args.input):
        raise CommandError("invalid_arguments", "arguments", "Provide exactly one invocation or public input transport.")
    if args.invocation:
        envelope = _inline(args.invocation, "invocation")
        public_input = envelope.get("public_input")
        owner = envelope.get("owner_result")
        if not isinstance(public_input, dict) or not isinstance(owner, dict):
            raise CommandError("invalid_arguments", "invocation", "Provide public_input and owner_result objects.")
    else:
        if not args.owner_result:
            raise CommandError("invalid_arguments", "owner_result", "Provide the checked semantic owner result.")
        public_input = load(package_root, args.input, "input")
        owner = load(package_root, args.owner_result, "owner_result")
    public_input = validate_input(package_root, public_input)
    owner = validate_owner(package_root, public_input, owner)
    exit_id = owner["typed_exit"]
    output = {"exit_id": exit_id}
    if exit_id == "completed":
        completion = owner["completion_evidence"]
        output.update({
            "edited_paths": completion["edited_paths"],
            "validation_summary": {
                "overall_status": "passed",
                "checks": [
                    {"summary": item["summary"], "status": item["status"]}
                    for item in completion["targeted_checks"]
                ],
            },
            "unverified_boundaries": completion["unverified_boundaries"],
        })
    elif exit_id in {"resume_active_task", "scope_change"}:
        output["task_ref"] = owner["task_ref"]
    elif exit_id in {"location_required", "explicit_choice_required"}:
        output.update({"continuation_id": owner["continuation_id"], "selection_origin": owner["selection_origin"]})
    elif exit_id == "reselect_mode":
        output["continuation_id"] = owner["continuation_id"]
    schema = {
        "completed": "public-completed-output.schema.json",
        "resume_active_task": "public-resume-active-task-output.schema.json",
        "scope_change": "public-scope-change-output.schema.json",
        "location_required": "public-location-required-output.schema.json",
        "reselect_mode": "public-reselect-mode-output.schema.json",
        "explicit_choice_required": "public-explicit-choice-required-output.schema.json",
        "blocked": "public-blocked-output.schema.json",
    }.get(exit_id)
    if schema is None:
        raise CommandError("unknown_typed_exit", "owner_result.typed_exit", "Return one declared typed exit.")
    validate_json(output, package_root / "schemas" / schema, "stdout")
    return output
