from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json


def parse(parser: argparse.ArgumentParser, argv: list[str]) -> argparse.Namespace:
    try:
        return parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the exact command help contract.") from exc


def load(package_root: Path, raw: str, field: str) -> dict:
    path = Path(raw)
    candidates = [path] if path.is_absolute() else [Path.cwd() / path, package_root / path]
    resolved = next((item for item in candidates if item.is_file() and not item.is_symlink()), None)
    if resolved is None:
        raise CommandError("unsafe_path", field, "Use a safe regular JSON file.")
    try:
        value = json.loads(resolved.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CommandError("invalid_json", field, "Provide one valid JSON object.") from exc
    if not isinstance(value, dict):
        raise CommandError("invalid_json", field, "Provide one valid JSON object.")
    return value


def schema_for_input(value: dict) -> str:
    return {
        "selected_route": "public-selected-route-input.schema.json",
        "interaction_resume": "public-interaction-resume-input.schema.json",
    }.get(str(value.get("profile")), "")


def validate_input(package_root: Path, value: dict) -> dict:
    schema = schema_for_input(value)
    if not schema:
        raise CommandError("schema_mismatch", "input.profile", "Use one declared task-free input profile.")
    validate_json(value, package_root / "schemas" / schema, "input")
    return value


def validate_owner(package_root: Path, public_input: dict, owner: dict) -> dict:
    validate_json(owner, package_root / "schemas/task-free-change-review.schema.json", "owner_result")
    for field in ("mode", "continuation_id", "selection_origin", "request_summary", "target_paths"):
        if owner.get(field) != public_input.get(field):
            raise CommandError("stale_identity", f"owner_result.{field}", "Rerun task-free execution for the exact current request.", 3)
    exit_id = owner["typed_exit"]
    gate = owner["ai_review_gate"]["status"]
    if (exit_id == "blocked") != (gate == "blocked"):
        raise CommandError("schema_mismatch", "owner_result.ai_review_gate", "Blocked exit and blocked Gate must be equivalent.")
    expected_prewrite = {
        "completed": "suitable",
        "resume_active_task": "resume_active_task",
        "scope_change": "scope_change",
        "location_required": "location_required",
        "reselect_mode": "suitable",
        "explicit_choice_required": "suitable",
        "blocked": "blocked",
    }[exit_id]
    if owner["pre_write_review"]["status"] != expected_prewrite:
        raise CommandError("schema_mismatch", "owner_result.pre_write_review.status", "Bind the typed exit to its reviewed checkout route.")
    if exit_id == "completed":
        completion = owner["completion_evidence"]
        if not set(completion["edited_paths"]).issubset(set(public_input["target_paths"])):
            raise CommandError("schema_mismatch", "owner_result.completion_evidence.edited_paths", "Edited paths must stay inside the bounded target paths.")
        statuses = [item["status"] for item in completion["targeted_checks"]]
        if "passed" not in statuses or "failed" in statuses:
            raise CommandError("schema_mismatch", "owner_result.completion_evidence.targeted_checks", "Completion requires at least one passed targeted check and no failed check.")
    elif exit_id in {"reselect_mode", "explicit_choice_required"}:
        evolution = owner["evolution_evidence"]
        targets = set(public_input["target_paths"])
        edited = set(evolution["edited_paths"])
        remaining = {
            item["target_path"] for item in evolution["remaining_writes_not_performed"]
        }
        if not edited.issubset(targets) or not remaining.issubset(targets):
            raise CommandError("schema_mismatch", "owner_result.evolution_evidence", "Evolution paths must stay inside the bounded target paths.")
    return owner


def digest(value: dict) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
