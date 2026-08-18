from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json


PROFILES = {"bootstrap_foundation", "task_impact_sync", "promotion", "repair"}
PROFILE_SCHEMAS = {
    "bootstrap_foundation": "public-input-bootstrap.schema.json",
    "task_impact_sync": "public-input-impact.schema.json",
    "promotion": "public-input-promotion.schema.json",
    "repair": "public-input-repair.schema.json",
}
EXITS = {
    "ssot_current": "public-ssot-current-output.schema.json",
    "sync_required": "public-sync-required-output.schema.json",
    "revision_required": "public-revision-required-output.schema.json",
    "baseline_incomplete": "public-baseline-incomplete-output.schema.json",
    "blocked": "public-blocked-output.schema.json",
}
OUTPUT_FIELDS = {
    "ssot_current": ("authority_locator", "active_version", "status", "applicability_scope", "freshness"),
    "sync_required": ("authority_locator", "target_version", "contribution_locator", "sync_kind", "freshness"),
    "revision_required": ("task_locator", "affected_scope", "authority_locator", "authority_version", "revision_code"),
    "baseline_incomplete": ("authority_locator", "known_status", "applicability_scope", "missing_layer_code"),
    "blocked": ("reason_code", "remediation"),
}
CONSUMERS = {
    "ssot_current": {"kind": "workflow", "id": "guru-requirements-design-test-ssot-current-router"},
    "sync_required": {"kind": "skill", "id": "guru-maintain-requirements-design-test-ssot"},
    "revision_required": {"kind": "workflow", "id": "guru-requirements-design-test-ssot-planning-router"},
    "baseline_incomplete": {"kind": "workflow", "id": "guru-requirements-design-test-ssot-bootstrap-router"},
    "blocked": {"kind": "stop", "id": "requirements-design-test-ssot-blocked"},
}


def _digest(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _locator(value: object, field: str) -> None:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise CommandError("unsafe_path", field, "Use a non-empty repository-relative locator.")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise CommandError("unsafe_path", field, "Use a repository-relative locator without parent traversal.")


def _record_and_check(package_root: Path, public: dict, owner: dict) -> dict:
    recorded = copy.deepcopy(owner)
    recorded["input_sha256"] = _digest(public)
    validate_json(recorded, _schema(package_root, "semantic-result.schema.json"), "owner_result")
    if recorded["profile"] != public["profile"] or recorded["mode"] != public["mode"]:
        raise CommandError("stale_identity", "owner_result", "Rerun the profile in the declared mode from current authority facts.", 3)
    if recorded["continuation_id"] != public["continuation_id"]:
        raise CommandError("stale_identity", "owner_result.continuation_id", "Rerun the profile from current authority facts.", 3)
    exit_id = recorded["typed_exit"]
    if recorded["consumer"] != CONSUMERS[exit_id]:
        raise CommandError("semantic_result_invalid", "owner_result.consumer", "Use the unique consumer declared for the selected exit.", 3)
    gate_status = recorded["ai_review_gate"]["status"]
    if (exit_id == "blocked") != (gate_status == "blocked"):
        raise CommandError("semantic_result_invalid", "owner_result.ai_review_gate.status", "Blocked requires a blocked gate; every other exit requires a passed gate.", 3)
    for field in ("repo_locator", "existing_authority_locator", "task_locator", "task_delta_locator", "authority_locator", "contribution_locator"):
        if field in public:
            _locator(public[field], f"public_input.{field}")
        if field in recorded:
            _locator(recorded[field], f"owner_result.{field}")
    architecture = public.get("architecture_baseline")
    if isinstance(architecture, dict):
        _locator(architecture["locator"], "public_input.architecture_baseline.locator")
    for field in ("authority_locator", "authority_version", "task_locator", "target_version", "contribution_locator", "sync_kind"):
        if field in recorded and field in public and recorded[field] != public[field]:
            raise CommandError("stale_identity", f"owner_result.{field}", "Reread current authority and repeat the semantic round.", 3)
    public_freshness = public.get("authority_freshness", public.get("freshness"))
    if "freshness" in recorded and public_freshness is not None and recorded["freshness"] != public_freshness:
        raise CommandError("stale_identity", "owner_result.freshness", "Reread current authority and repeat the semantic round.", 3)
    return recorded


def _json(value: str, field: str, locator: bool = False) -> dict:
    if value == "-":
        value = sys.stdin.read()
    elif locator:
        path = Path(value)
        if not path.is_absolute():
            path = Path.cwd() / path
        if not path.is_file() or path.is_symlink():
            raise CommandError("unsafe_path", field, "Use a safe regular JSON file.")
        value = path.read_text(encoding="utf-8")
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
    if args.input and not args.owner_result:
        raise CommandError("invalid_arguments", "owner_result", "Provide a completed semantic owner result.")
    envelope = _json(args.invocation, "invocation") if args.invocation else None
    public = envelope.get("public_input") if envelope else _json(args.input, "input", True)
    owner = envelope.get("owner_result") if envelope else _json(args.owner_result, "owner_result", True)
    if not isinstance(public, dict) or not isinstance(owner, dict):
        raise CommandError("invalid_arguments", "owner_result", "Provide a completed semantic owner result.")
    profile = public.get("profile")
    if profile not in PROFILES:
        raise CommandError("schema_mismatch", "profile", "Use one declared Requirements Design Test SSOT profile.")
    validate_json(public, _schema(package_root, PROFILE_SCHEMAS[profile]), "input")
    owner = _record_and_check(package_root, public, owner)
    exit_id = owner["typed_exit"]
    output = {"exit_id": exit_id}
    for key in OUTPUT_FIELDS[exit_id]:
        if key in owner:
            output[key] = owner[key]
    validate_json(output, _schema(package_root, EXITS[exit_id]), "stdout")
    return copy.deepcopy(output)
