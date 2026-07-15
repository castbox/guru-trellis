#!/usr/bin/env python3
"""Validate frozen upstream ownership facts before Guru Team preset mutation."""

from __future__ import annotations

import argparse
import ast
import fnmatch
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_RELATIVE = Path("trellis/presets/guru-team/ownership/upstream-ownership.schema.json")
INVENTORY_RELATIVE = Path("trellis/presets/guru-team/ownership/upstream-ownership.json")
EXTENSION_RELATIVE = Path("trellis/guru-team-extension.json")
INSTALLER_RELATIVE = Path("trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py")
SKILL_REGISTRY_RELATIVE = Path("trellis/skills/guru-team/registry.json")
OVERLAY_ROOT_RELATIVE = Path("trellis/presets/guru-team/overlays")
BASE_COMMIT = "291b57b6c02872320a4dce0626a2f718399b8f56"
FROZEN_PATH_COUNT = 43
FROZEN_PATH_SET_SHA256 = "56874019bb93b6669aaeb36b7ca9506aed9127a28ef9f81637ea428a6b0a838b"
BASELINE_PAYLOAD_AGGREGATE_SHA256 = "52dfb4036828865e070002f89712fc2bcd802d1f50263da5d9ef58e6edf5c5f0"
OWNERSHIP_CATEGORIES = {
    "upstream_owned",
    "guru_owned",
    "transitional_legacy",
    "unclassified",
}
LEGACY_NOT_GENERATED_PATHS = {
    ".codex/prompts/trellis-continue.md",
    ".codex/prompts/trellis-finish-work.md",
    ".codex/prompts/trellis-start.md",
    ".codex/skills/trellis-continue/SKILL.md",
    ".codex/skills/trellis-finish-work/SKILL.md",
    ".codex/skills/trellis-start/SKILL.md",
}
TOP_LEVEL_KEYS = {
    "schema_version",
    "inventory_id",
    "target_trellis_cli",
    "baseline",
    "ownership_categories",
    "guru_owned_rules",
    "managed_path_claims",
    "legacy_entries",
}
BASELINE_KEYS = {
    "base_commit",
    "overlay_root",
    "frozen_path_count",
    "sorted_path_set_sha256",
    "active_payload_aggregate_sha256",
    "path_set_digest_contract",
    "payload_digest_contract",
    "clean_init",
}
CLEAN_INIT_KEYS = {
    "command",
    "trellis_cli",
    "generated_count",
    "legacy_not_generated_count",
}
RULE_KEYS = {"id", "match_type", "pattern", "category"}
CLAIM_KEYS = {"path", "category", "classification_rule", "covered_by_legacy_paths"}
LEGACY_ENTRY_KEYS = {
    "path",
    "category",
    "migration_state",
    "baseline_sha256",
    "generated_in_clean_init",
    "upstream_producer",
    "current_guru_behavior",
    "replacement_owners",
    "blocking_issues",
    "removal_issue",
    "update_upgrade_conflict",
    "dogfood_status",
    "target_business_repo_status",
}
EXPECTED_GURU_RULES = [
    {"id": "installed-runtime", "match_type": "path_prefix", "pattern": ".trellis/guru-team/", "category": "guru_owned"},
    {"id": "canonical-workflow-root", "match_type": "path_prefix", "pattern": "trellis/workflows/guru-team/", "category": "guru_owned"},
    {"id": "canonical-skill-root", "match_type": "path_prefix", "pattern": "trellis/skills/guru-team/", "category": "guru_owned"},
    {"id": "canonical-skill-id", "match_type": "skill_id_prefix", "pattern": "guru-", "category": "guru_owned"},
    {"id": "shared-skill-discovery", "match_type": "path_glob", "pattern": ".agents/skills/guru-*/**", "category": "guru_owned"},
    {"id": "codex-skill-discovery", "match_type": "path_glob", "pattern": ".codex/skills/guru-*/**", "category": "guru_owned"},
    {"id": "cursor-skill-discovery", "match_type": "path_glob", "pattern": ".cursor/skills/guru-*/**", "category": "guru_owned"},
    {"id": "claude-skill-discovery", "match_type": "path_glob", "pattern": ".claude/skills/guru-*/**", "category": "guru_owned"},
]
EXPECTED_REPLACEMENT_OWNERS = {
    "guru-create-task-workspace",
    "guru-approve-task-plan",
    "guru-check-task",
    "guru-review-branch",
    "guru-review-task-publication",
    "guru-verify-extension-installation",
    "guru-finalize-task",
}
EXPECTED_REPLACEMENT_OWNER_ISSUES = {
    "guru-create-task-workspace": 112,
    "guru-approve-task-plan": 129,
    "guru-check-task": 130,
    "guru-review-branch": 131,
    "guru-review-task-publication": 119,
    "guru-verify-extension-installation": 119,
    "guru-finalize-task": 119,
}
VALID_SCHEMA_KEYWORDS = {
    "$schema",
    "$id",
    "$ref",
    "$defs",
    "title",
    "description",
    "type",
    "additionalProperties",
    "required",
    "properties",
    "const",
    "enum",
    "items",
    "minItems",
    "maxItems",
    "uniqueItems",
    "minLength",
    "pattern",
    "minimum",
    "allOf",
    "oneOf",
    "if",
    "then",
}


def ownership_error(code: str, path: str, detail: str) -> dict[str, str]:
    return {"code": code, "path": path, "detail": detail}


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    if any(ord(character) < 32 for character in value):
        return False
    pure = PurePosixPath(value)
    return not pure.is_absolute() and "." not in pure.parts and ".." not in pure.parts


def path_set_sha256(paths: list[str]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def payload_aggregate_sha256(overlay_root: Path, paths: list[str]) -> str:
    digest = hashlib.sha256()
    for relative in sorted(paths):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update((overlay_root / relative).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def read_json(path: Path, label: str, errors: list[dict[str, str]]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(ownership_error(f"missing_{label}", path.as_posix(), "required JSON file is missing"))
    except UnicodeDecodeError:
        errors.append(ownership_error(f"invalid_{label}_encoding", path.as_posix(), "JSON file is not UTF-8"))
    except json.JSONDecodeError as exc:
        errors.append(ownership_error(f"invalid_{label}_json", path.as_posix(), f"line {exc.lineno}, column {exc.colno}"))
    return None


def require_exact_keys(
    value: Any,
    expected: set[str],
    path: str,
    errors: list[dict[str, str]],
) -> bool:
    if not isinstance(value, dict):
        errors.append(ownership_error("schema_type_mismatch", path, "expected object"))
        return False
    actual = set(value)
    if actual != expected:
        errors.append(
            ownership_error(
                "fixed_key_set_mismatch",
                path,
                f"missing={sorted(expected - actual)} unknown={sorted(actual - expected)}",
            )
        )
        return False
    return True


def validate_schema_node(
    node: Any,
    root: dict[str, Any],
    path: str,
    errors: list[dict[str, str]],
) -> None:
    if isinstance(node, bool):
        return
    if not isinstance(node, dict):
        errors.append(ownership_error("schema_contract_invalid", path, "schema node must be an object or boolean"))
        return
    unknown = set(node) - VALID_SCHEMA_KEYWORDS
    if unknown:
        errors.append(ownership_error("schema_contract_invalid", path, f"unknown schema keywords: {sorted(unknown)}"))
    if "$ref" in node:
        reference = node["$ref"]
        if not isinstance(reference, str) or not reference.startswith("#/$defs/"):
            errors.append(ownership_error("schema_contract_invalid", f"{path}.$ref", "only local $defs references are allowed"))
        elif reference.removeprefix("#/$defs/") not in root.get("$defs", {}):
            errors.append(ownership_error("schema_contract_invalid", f"{path}.$ref", f"unresolved reference {reference}"))
    schema_type = node.get("type")
    allowed_types = {"array", "boolean", "integer", "null", "number", "object", "string"}
    if schema_type is not None:
        values = schema_type if isinstance(schema_type, list) else [schema_type]
        if not values or any(item not in allowed_types for item in values):
            errors.append(ownership_error("schema_contract_invalid", f"{path}.type", "invalid JSON Schema type"))
    properties = node.get("properties")
    if properties is not None:
        if not isinstance(properties, dict):
            errors.append(ownership_error("schema_contract_invalid", f"{path}.properties", "properties must be an object"))
        else:
            for name, child in properties.items():
                validate_schema_node(child, root, f"{path}.properties.{name}", errors)
    required = node.get("required")
    if required is not None:
        if not isinstance(required, list) or any(not isinstance(item, str) for item in required) or len(required) != len(set(required)):
            errors.append(ownership_error("schema_contract_invalid", f"{path}.required", "required must contain unique strings"))
        elif isinstance(properties, dict) and not set(required).issubset(properties):
            errors.append(ownership_error("schema_contract_invalid", f"{path}.required", "required refers to an unknown property"))
    additional = node.get("additionalProperties")
    if additional is not None and not isinstance(additional, (bool, dict)):
        errors.append(ownership_error("schema_contract_invalid", f"{path}.additionalProperties", "must be boolean or schema"))
    elif isinstance(additional, dict):
        validate_schema_node(additional, root, f"{path}.additionalProperties", errors)
    definitions = node.get("$defs")
    if definitions is not None:
        if not isinstance(definitions, dict):
            errors.append(ownership_error("schema_contract_invalid", f"{path}.$defs", "must be an object"))
        else:
            for name, child in definitions.items():
                validate_schema_node(child, root, f"{path}.$defs.{name}", errors)
    if "items" in node:
        validate_schema_node(node["items"], root, f"{path}.items", errors)
    for keyword in ("allOf", "oneOf"):
        if keyword in node:
            children = node[keyword]
            if not isinstance(children, list) or not children:
                errors.append(ownership_error("schema_contract_invalid", f"{path}.{keyword}", "must be a non-empty array"))
            else:
                for index, child in enumerate(children):
                    validate_schema_node(child, root, f"{path}.{keyword}[{index}]", errors)
    for keyword in ("if", "then"):
        if keyword in node:
            validate_schema_node(node[keyword], root, f"{path}.{keyword}", errors)
    if "pattern" in node:
        try:
            re.compile(node["pattern"])
        except (TypeError, re.error):
            errors.append(ownership_error("schema_contract_invalid", f"{path}.pattern", "invalid regular expression"))
    if "enum" in node and (not isinstance(node["enum"], list) or not node["enum"]):
        errors.append(ownership_error("schema_contract_invalid", f"{path}.enum", "enum must be a non-empty array"))
    if "uniqueItems" in node and not isinstance(node["uniqueItems"], bool):
        errors.append(ownership_error("schema_contract_invalid", f"{path}.uniqueItems", "must be boolean"))
    for keyword in ("minItems", "maxItems", "minLength", "minimum"):
        if keyword in node and (not isinstance(node[keyword], int) or isinstance(node[keyword], bool) or node[keyword] < 0):
            errors.append(ownership_error("schema_contract_invalid", f"{path}.{keyword}", "must be a non-negative integer"))


def validate_schema_contract(schema: Any, errors: list[dict[str, str]]) -> None:
    if not isinstance(schema, dict):
        errors.append(ownership_error("schema_contract_invalid", SCHEMA_RELATIVE.as_posix(), "root must be an object"))
        return
    validate_schema_node(schema, schema, "$", errors)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append(ownership_error("schema_contract_invalid", "$.$schema", "expected Draft 2020-12"))
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        errors.append(ownership_error("schema_contract_invalid", "$", "root must be a closed object"))
    if set(schema.get("required", [])) != TOP_LEVEL_KEYS or set(schema.get("properties", {})) != TOP_LEVEL_KEYS:
        errors.append(ownership_error("schema_contract_invalid", "$", "root required/properties must match the fixed inventory keys"))


def classify_guru_path(path: str, rules: list[dict[str, Any]]) -> list[str]:
    matches: list[str] = []
    for rule in rules:
        match_type = rule.get("match_type")
        pattern = rule.get("pattern")
        if not isinstance(pattern, str):
            continue
        matched = False
        if match_type == "path_prefix":
            matched = path.startswith(pattern)
        elif match_type == "path_glob":
            matched = fnmatch.fnmatchcase(path, pattern)
        elif match_type == "skill_id_prefix":
            matched = "/" not in path and path.startswith(pattern)
        if matched:
            matches.append(str(rule.get("id") or ""))
    return matches


def claim_matches_rule(claim_path: str, rule: dict[str, Any]) -> bool:
    if rule.get("match_type") == "path_prefix":
        return claim_path.startswith(str(rule.get("pattern") or ""))
    if rule.get("match_type") == "path_glob":
        pattern = str(rule.get("pattern") or "")
        return pattern.endswith("/**") and claim_path.rstrip("/") + "/**" == pattern
    return False


def extract_managed_assets(installer_path: Path, errors: list[dict[str, str]]) -> list[str]:
    try:
        module = ast.parse(installer_path.read_text(encoding="utf-8"), filename=installer_path.as_posix())
    except (FileNotFoundError, UnicodeDecodeError, SyntaxError) as exc:
        errors.append(ownership_error("managed_asset_source_invalid", INSTALLER_RELATIVE.as_posix(), type(exc).__name__))
        return []
    assignments = [
        node
        for node in module.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "MANAGED_ASSET_PATHS" for target in node.targets)
    ]
    if len(assignments) != 1 or not isinstance(assignments[0].value, (ast.List, ast.Tuple)):
        errors.append(ownership_error("managed_asset_source_invalid", "MANAGED_ASSET_PATHS", "expected one literal list assignment"))
        return []
    values: list[str] = []
    for index, element in enumerate(assignments[0].value.elts):
        if not (
            isinstance(element, ast.Call)
            and isinstance(element.func, ast.Name)
            and element.func.id == "Path"
            and len(element.args) == 1
            and not element.keywords
            and isinstance(element.args[0], ast.Constant)
            and isinstance(element.args[0].value, str)
        ):
            errors.append(ownership_error("managed_asset_source_invalid", f"MANAGED_ASSET_PATHS[{index}]", "expected Path string literal"))
            continue
        value = element.args[0].value
        if not is_safe_relative_path(value):
            errors.append(ownership_error("managed_asset_path_invalid", value, "managed asset must be a safe relative path"))
            continue
        values.append(value)
    if len(values) != len(set(values)):
        errors.append(ownership_error("duplicate_managed_asset", "MANAGED_ASSET_PATHS", "managed asset literals must be unique"))
    return values


def validate_repository(repo: Path | str) -> dict[str, Any]:
    repo_root = Path(repo).resolve()
    errors: list[dict[str, str]] = []
    schema = read_json(repo_root / SCHEMA_RELATIVE, "ownership_schema", errors)
    inventory = read_json(repo_root / INVENTORY_RELATIVE, "ownership_inventory", errors)
    extension = read_json(repo_root / EXTENSION_RELATIVE, "extension_manifest", errors)
    registry = read_json(repo_root / SKILL_REGISTRY_RELATIVE, "skill_registry", errors)

    if schema is not None:
        validate_schema_contract(schema, errors)

    entries: list[dict[str, Any]] = []
    rules: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    baseline: dict[str, Any] = {}
    if require_exact_keys(inventory, TOP_LEVEL_KEYS, "$", errors):
        if inventory.get("schema_version") != "1.0":
            errors.append(ownership_error("inventory_identity_mismatch", "$.schema_version", "expected 1.0"))
        if inventory.get("inventory_id") != "guru-team-upstream-ownership":
            errors.append(ownership_error("inventory_identity_mismatch", "$.inventory_id", "unexpected inventory id"))
        if inventory.get("target_trellis_cli") != "0.6.5":
            errors.append(ownership_error("target_trellis_cli_mismatch", "$.target_trellis_cli", "expected 0.6.5"))
        categories = inventory.get("ownership_categories")
        if not isinstance(categories, list) or len(categories) != 4 or set(categories) != OWNERSHIP_CATEGORIES:
            errors.append(ownership_error("ownership_category_set_mismatch", "$.ownership_categories", "expected exactly four mutually exclusive categories"))
        baseline_value = inventory.get("baseline")
        if require_exact_keys(baseline_value, BASELINE_KEYS, "$.baseline", errors):
            baseline = baseline_value
            expected_baseline = {
                "base_commit": BASE_COMMIT,
                "overlay_root": OVERLAY_ROOT_RELATIVE.as_posix(),
                "frozen_path_count": FROZEN_PATH_COUNT,
                "sorted_path_set_sha256": FROZEN_PATH_SET_SHA256,
                "active_payload_aggregate_sha256": BASELINE_PAYLOAD_AGGREGATE_SHA256,
                "path_set_digest_contract": "sorted-relative-path-newline-v1",
                "payload_digest_contract": "sorted-relative-path-nul-payload-nul-v1",
            }
            for key, expected in expected_baseline.items():
                if baseline.get(key) != expected:
                    errors.append(ownership_error("frozen_baseline_mismatch", f"$.baseline.{key}", f"expected {expected}"))
            clean_init = baseline.get("clean_init")
            if require_exact_keys(clean_init, CLEAN_INIT_KEYS, "$.baseline.clean_init", errors):
                expected_clean_init = {
                    "command": "trellis init -y -u ownership-audit --claude --codex --cursor",
                    "trellis_cli": "0.6.5",
                    "generated_count": 37,
                    "legacy_not_generated_count": 6,
                }
                if clean_init != expected_clean_init:
                    errors.append(ownership_error("clean_init_baseline_mismatch", "$.baseline.clean_init", "expected pinned Trellis 0.6.5 facts"))
        rule_values = inventory.get("guru_owned_rules")
        if not isinstance(rule_values, list):
            errors.append(ownership_error("schema_type_mismatch", "$.guru_owned_rules", "expected array"))
        else:
            rules = [item for item in rule_values if isinstance(item, dict)]
            for index, rule in enumerate(rule_values):
                require_exact_keys(rule, RULE_KEYS, f"$.guru_owned_rules[{index}]", errors)
            if rule_values != EXPECTED_GURU_RULES:
                errors.append(ownership_error("guru_owned_rule_set_mismatch", "$.guru_owned_rules", "anchored Guru namespace rules changed"))
        claim_values = inventory.get("managed_path_claims")
        if not isinstance(claim_values, list):
            errors.append(ownership_error("schema_type_mismatch", "$.managed_path_claims", "expected array"))
        else:
            claims = [item for item in claim_values if isinstance(item, dict)]
            for index, claim in enumerate(claim_values):
                require_exact_keys(claim, CLAIM_KEYS, f"$.managed_path_claims[{index}]", errors)
        entry_values = inventory.get("legacy_entries")
        if not isinstance(entry_values, list):
            errors.append(ownership_error("schema_type_mismatch", "$.legacy_entries", "expected array"))
        else:
            entries = [item for item in entry_values if isinstance(item, dict)]
            for index, entry in enumerate(entry_values):
                require_exact_keys(entry, LEGACY_ENTRY_KEYS, f"$.legacy_entries[{index}]", errors)

    if len(entries) > FROZEN_PATH_COUNT:
        errors.append(ownership_error("frozen_baseline_expanded", "$.legacy_entries", f"expected {FROZEN_PATH_COUNT}, found {len(entries)}"))
    elif len(entries) < FROZEN_PATH_COUNT:
        errors.append(ownership_error("frozen_baseline_reduced", "$.legacy_entries", f"expected {FROZEN_PATH_COUNT}, found {len(entries)}"))

    entry_by_path: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(entries):
        entry_path = entry.get("path")
        display_path = entry_path if isinstance(entry_path, str) else f"$.legacy_entries[{index}].path"
        if not is_safe_relative_path(entry_path):
            errors.append(ownership_error("invalid_legacy_path", str(display_path), "path must be a safe overlay-relative path"))
            continue
        if entry_path in entry_by_path:
            errors.append(ownership_error("duplicate_legacy_path", entry_path, "legacy path appears more than once"))
        entry_by_path[entry_path] = entry
        category = entry.get("category")
        state = entry.get("migration_state")
        if category == "unclassified":
            errors.append(ownership_error("unclassified_path", entry_path, "legacy entry has no reviewed ownership category"))
        if state == "active" and category != "transitional_legacy":
            errors.append(ownership_error("migration_state_category_mismatch", entry_path, "active requires transitional_legacy"))
        if state == "removed" and category != "upstream_owned":
            errors.append(ownership_error("migration_state_category_mismatch", entry_path, "removed requires upstream_owned"))
        if state not in {"active", "removed"}:
            errors.append(ownership_error("invalid_migration_state", entry_path, "expected active or removed"))
        replacement_owners = entry.get("replacement_owners")
        if not isinstance(replacement_owners, list) or not replacement_owners:
            errors.append(ownership_error("missing_replacement_owner", entry_path, "at least one replacement owner is required"))
        elif any(not isinstance(owner, str) or not re.fullmatch(r"guru-[a-z0-9]+(?:-[a-z0-9]+)*", owner) for owner in replacement_owners):
            errors.append(ownership_error("invalid_replacement_owner", entry_path, "replacement owners must use guru-* ids"))
        elif len(replacement_owners) != len(set(replacement_owners)):
            errors.append(ownership_error("duplicate_replacement_owner", entry_path, "replacement owners must be unique"))
        elif not set(replacement_owners).issubset(EXPECTED_REPLACEMENT_OWNERS):
            unknown = sorted(set(replacement_owners) - EXPECTED_REPLACEMENT_OWNERS)
            errors.append(ownership_error("unknown_replacement_owner", entry_path, f"owners are absent from the reviewed migration issue set: {unknown}"))
        blocking = entry.get("blocking_issues")
        if not isinstance(blocking, list) or not blocking:
            errors.append(ownership_error("missing_blocking_issue", entry_path, "at least one positive issue number is required"))
        elif any(not isinstance(issue, int) or isinstance(issue, bool) or issue < 1 for issue in blocking):
            errors.append(ownership_error("invalid_blocking_issue", entry_path, "blocking issue numbers must be positive integers"))
        elif len(blocking) != len(set(blocking)):
            errors.append(ownership_error("duplicate_blocking_issue", entry_path, "blocking issue numbers must be unique"))
        elif isinstance(replacement_owners, list):
            missing_owner_issues = sorted(
                {
                    EXPECTED_REPLACEMENT_OWNER_ISSUES[owner]
                    for owner in replacement_owners
                    if owner in EXPECTED_REPLACEMENT_OWNER_ISSUES
                    and EXPECTED_REPLACEMENT_OWNER_ISSUES[owner] not in blocking
                }
            )
            if missing_owner_issues:
                errors.append(
                    ownership_error(
                        "replacement_owner_issue_mismatch",
                        entry_path,
                        f"blocking_issues is missing owner issues {missing_owner_issues}",
                    )
                )
        removal_issue = entry.get("removal_issue")
        if not isinstance(removal_issue, int) or isinstance(removal_issue, bool) or removal_issue < 1:
            errors.append(ownership_error("missing_removal_issue", entry_path, "a positive removal issue is required"))
        elif removal_issue != 132:
            errors.append(ownership_error("removal_issue_mismatch", entry_path, "frozen overlays are removed only by issue 132"))
        for field in ("upstream_producer", "current_guru_behavior", "update_upgrade_conflict"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(ownership_error("missing_legacy_fact", entry_path, f"{field} is required"))
        digest = entry.get("baseline_sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(ownership_error("invalid_baseline_sha256", entry_path, "expected lowercase SHA-256"))
        if not isinstance(entry.get("generated_in_clean_init"), bool):
            errors.append(ownership_error("invalid_clean_init_fact", entry_path, "generated_in_clean_init must be boolean"))
        if state == "active":
            if entry.get("dogfood_status") != "canonical_payload_matches_installed_copy":
                errors.append(ownership_error("active_dogfood_status_mismatch", entry_path, "active path must match the installed dogfood copy"))
            if entry.get("target_business_repo_status") != "installed_when_selected_platform_applies":
                errors.append(ownership_error("active_target_status_mismatch", entry_path, "active path must remain selected-platform installable"))
        elif state == "removed":
            if entry.get("dogfood_status") != "removed_with_audit_history":
                errors.append(ownership_error("removed_dogfood_status_mismatch", entry_path, "removed path must retain audit history"))
            if entry.get("target_business_repo_status") != "no_longer_installed":
                errors.append(ownership_error("removed_target_status_mismatch", entry_path, "removed path must no longer install"))

    frozen_paths = sorted(entry_by_path)
    if path_set_sha256(frozen_paths) != FROZEN_PATH_SET_SHA256:
        errors.append(ownership_error("frozen_path_set_mismatch", "$.legacy_entries", "sorted path-set digest differs from the issue 128 baseline"))
    generated_count = sum(entry.get("generated_in_clean_init") is True for entry in entries)
    if generated_count != 37 or len(entries) - generated_count != 6:
        errors.append(ownership_error("clean_init_count_mismatch", "$.legacy_entries", f"generated={generated_count} legacy_not_generated={len(entries) - generated_count}"))
    actual_not_generated = {
        str(entry.get("path"))
        for entry in entries
        if entry.get("generated_in_clean_init") is False
    }
    if actual_not_generated != LEGACY_NOT_GENERATED_PATHS:
        errors.append(
            ownership_error(
                "clean_init_path_set_mismatch",
                "$.legacy_entries",
                f"missing={sorted(LEGACY_NOT_GENERATED_PATHS - actual_not_generated)} unknown={sorted(actual_not_generated - LEGACY_NOT_GENERATED_PATHS)}",
            )
        )

    overlay_root = repo_root / OVERLAY_ROOT_RELATIVE
    actual_overlay_paths = sorted(
        path.relative_to(overlay_root).as_posix()
        for path in overlay_root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"}
    ) if overlay_root.is_dir() else []
    active_paths = sorted(path for path, entry in entry_by_path.items() if entry.get("migration_state") == "active")
    removed_paths = sorted(path for path, entry in entry_by_path.items() if entry.get("migration_state") == "removed")
    for path in sorted(set(actual_overlay_paths) - set(entry_by_path)):
        errors.append(ownership_error("overlay_not_in_frozen_baseline", path, "overlay path is not in the frozen issue 128 inventory"))
    for path in sorted(set(active_paths) - set(actual_overlay_paths)):
        errors.append(ownership_error("active_overlay_missing", path, "active transitional overlay is missing"))
    for path in sorted(set(removed_paths) & set(actual_overlay_paths)):
        errors.append(ownership_error("removed_overlay_still_present", path, "upstream_owned/removed path must not exist"))
    for path in sorted(set(active_paths) & set(actual_overlay_paths)):
        overlay_path = overlay_root / path
        if overlay_path.is_symlink() or not overlay_path.is_file():
            errors.append(ownership_error("active_overlay_not_regular", path, "active overlay must be a regular file, not a symlink"))
            continue
        expected = entry_by_path[path].get("baseline_sha256")
        actual = sha256_file(overlay_path)
        if actual != expected:
            errors.append(ownership_error("active_payload_hash_mismatch", path, f"expected={expected} actual={actual}"))
    actual_payload_aggregate = None
    if (
        active_paths
        and set(active_paths) == set(actual_overlay_paths)
        and all(not (overlay_root / path).is_symlink() and (overlay_root / path).is_file() for path in active_paths)
    ):
        actual_payload_aggregate = payload_aggregate_sha256(overlay_root, active_paths)
        if not removed_paths and actual_payload_aggregate != BASELINE_PAYLOAD_AGGREGATE_SHA256:
            errors.append(ownership_error("active_payload_aggregate_mismatch", OVERLAY_ROOT_RELATIVE.as_posix(), f"actual={actual_payload_aggregate}"))

    claim_by_path: dict[str, dict[str, Any]] = {}
    rule_by_id = {str(rule.get("id")): rule for rule in rules}
    for index, claim in enumerate(claims):
        claim_path = claim.get("path")
        display_path = claim_path if isinstance(claim_path, str) else f"$.managed_path_claims[{index}].path"
        if not is_safe_relative_path(claim_path):
            errors.append(ownership_error("invalid_managed_claim_path", str(display_path), "claim must be a safe repo-relative path"))
            continue
        if claim_path in claim_by_path:
            errors.append(ownership_error("duplicate_managed_claim", claim_path, "managed claim appears more than once"))
        claim_by_path[claim_path] = claim
        classification_rule = claim.get("classification_rule")
        if not isinstance(classification_rule, str) or not classification_rule:
            errors.append(ownership_error("managed_claim_rule_missing", claim_path, "classification_rule is required"))
        covered_paths = claim.get("covered_by_legacy_paths")
        if not isinstance(covered_paths, list) or any(not is_safe_relative_path(item) for item in covered_paths):
            errors.append(ownership_error("managed_claim_coverage_invalid", claim_path, "coverage must contain safe relative paths"))
        elif len(covered_paths) != len(set(covered_paths)):
            errors.append(ownership_error("managed_claim_coverage_invalid", claim_path, "coverage paths must be unique"))
        category = claim.get("category")
        if category == "unclassified":
            errors.append(ownership_error("unclassified_path", claim_path, "managed claim has no reviewed owner"))
        elif category == "upstream_owned":
            errors.append(ownership_error("upstream_owned_managed_claim", claim_path, "Guru Team must not claim an upstream-owned path"))
        elif category == "guru_owned":
            rule = rule_by_id.get(str(claim.get("classification_rule")))
            if rule is None or not claim_matches_rule(claim_path, rule):
                errors.append(ownership_error("guru_owned_claim_rule_mismatch", claim_path, "claim is outside its anchored Guru rule"))
            if claim.get("covered_by_legacy_paths") != []:
                errors.append(ownership_error("guru_owned_claim_has_legacy_coverage", claim_path, "Guru-owned claim must not cite legacy paths"))
        elif category == "transitional_legacy":
            covered = claim.get("covered_by_legacy_paths")
            if not isinstance(covered, list) or not covered:
                errors.append(ownership_error("missing_legacy_claim_coverage", claim_path, "transitional claim requires active frozen paths"))
            else:
                for covered_path in covered:
                    covered_entry = entry_by_path.get(covered_path)
                    if covered_entry is None or covered_entry.get("migration_state") != "active":
                        errors.append(ownership_error("invalid_legacy_claim_coverage", claim_path, f"{covered_path} is not active frozen legacy"))
                    elif not covered_path.startswith(claim_path.rstrip("/") + "/"):
                        errors.append(ownership_error("invalid_legacy_claim_coverage", claim_path, f"{covered_path} is outside the claimed prefix"))
        else:
            errors.append(ownership_error("unclassified_path", claim_path, f"unknown category {category!r}"))

    manifest_paths: list[str] = []
    manifest_active_ids: list[str] = []
    if isinstance(extension, dict):
        public_api = extension.get("public_api")
        if not isinstance(public_api, dict):
            errors.append(ownership_error("extension_manifest_contract_invalid", "public_api", "expected object"))
        else:
            values = public_api.get("managed_paths")
            if not isinstance(values, list) or any(not isinstance(item, str) for item in values):
                errors.append(ownership_error("extension_manifest_contract_invalid", "public_api.managed_paths", "expected string array"))
            else:
                manifest_paths = values
                if len(values) != len(set(values)):
                    errors.append(ownership_error("duplicate_extension_managed_path", "public_api.managed_paths", "paths must be unique"))
            contracts = public_api.get("skill_contracts")
            if isinstance(contracts, dict) and isinstance(contracts.get("active_skill_ids"), list):
                manifest_active_ids = contracts["active_skill_ids"]
    for path in sorted(set(manifest_paths) - set(claim_by_path)):
        errors.append(ownership_error("unclassified_managed_claim", path, "extension manifest path is absent from ownership inventory"))
    for path in sorted(set(claim_by_path) - set(manifest_paths)):
        errors.append(ownership_error("stale_managed_claim_inventory", path, "inventory claim is absent from extension manifest"))

    managed_assets = extract_managed_assets(repo_root / INSTALLER_RELATIVE, errors)
    for relative in managed_assets:
        installed_path = f".trellis/guru-team/{relative}"
        matches = classify_guru_path(installed_path, rules)
        if matches != ["installed-runtime"]:
            errors.append(ownership_error("unclassified_managed_asset", installed_path, f"classification_rules={matches}"))

    active_skill_ids: list[str] = []
    if isinstance(registry, dict) and isinstance(registry.get("skills"), list):
        for index, skill in enumerate(registry["skills"]):
            if not isinstance(skill, dict) or skill.get("state") != "active":
                continue
            skill_id = skill.get("id")
            if not isinstance(skill_id, str):
                errors.append(ownership_error("active_skill_id_invalid", f"skills[{index}].id", "expected string"))
                continue
            active_skill_ids.append(skill_id)
            if classify_guru_path(skill_id, rules) != ["canonical-skill-id"]:
                errors.append(ownership_error("active_skill_not_guru_owned", skill_id, "active Skill id must use guru-*"))
            for field in ("package", "interface"):
                relative = skill.get(field)
                if not isinstance(relative, str) or not is_safe_relative_path(relative):
                    errors.append(ownership_error("active_skill_path_invalid", skill_id, f"invalid {field}"))
                    continue
                canonical_path = f"trellis/skills/guru-team/{relative}"
                if classify_guru_path(canonical_path, rules) != ["canonical-skill-root"]:
                    errors.append(ownership_error("active_skill_path_not_guru_owned", canonical_path, f"invalid {field} classification"))
            platform_map = {"shared": ".agents", "codex": ".codex", "cursor": ".cursor", "claude": ".claude"}
            platforms = skill.get("supported_platforms")
            if isinstance(platforms, list):
                for platform in platforms:
                    root = platform_map.get(platform)
                    if root is None:
                        errors.append(ownership_error("active_skill_platform_invalid", skill_id, f"unsupported platform {platform!r}"))
                        continue
                    discovery = f"{root}/skills/{skill_id}/SKILL.md"
                    matches = classify_guru_path(discovery, rules)
                    expected_rule = f"{platform}-skill-discovery" if platform != "shared" else "shared-skill-discovery"
                    if matches != [expected_rule]:
                        errors.append(ownership_error("guru_discovery_path_unclassified", discovery, f"classification_rules={matches}"))
    elif registry is not None:
        errors.append(ownership_error("skill_registry_contract_invalid", "skills", "expected array"))
    if sorted(active_skill_ids) != sorted(manifest_active_ids):
        errors.append(ownership_error("active_skill_manifest_mismatch", "public_api.skill_contracts.active_skill_ids", f"registry={sorted(active_skill_ids)} manifest={sorted(manifest_active_ids)}"))

    facts = {
        "target_trellis_cli": inventory.get("target_trellis_cli") if isinstance(inventory, dict) else None,
        "base_commit": baseline.get("base_commit"),
        "schema_sha256": sha256_file(repo_root / SCHEMA_RELATIVE) if (repo_root / SCHEMA_RELATIVE).is_file() else None,
        "inventory_sha256": sha256_file(repo_root / INVENTORY_RELATIVE) if (repo_root / INVENTORY_RELATIVE).is_file() else None,
        "guru_owned_rules_sha256": canonical_sha256(rules),
        "managed_path_claims_sha256": canonical_sha256(claims),
        "legacy_entries_sha256": canonical_sha256(entries),
        "frozen_count": len(entries),
        "active_count": len(active_paths),
        "removed_count": len(removed_paths),
        "generated_in_clean_init_count": generated_count,
        "legacy_not_generated_count": len(entries) - generated_count,
        "overlay_count": len(actual_overlay_paths),
        "sorted_path_set_sha256": path_set_sha256(frozen_paths),
        "active_payload_aggregate_sha256": actual_payload_aggregate,
        "managed_claim_count": len(manifest_paths),
        "classified_managed_claim_count": len(set(manifest_paths) & set(claim_by_path)),
        "managed_asset_count": len(managed_assets),
        "active_skill_count": len(active_skill_ids),
    }
    errors.sort(key=lambda item: (item["code"], item["path"], item["detail"]))
    return {
        "status": "ok" if not errors else "error",
        "schema_path": SCHEMA_RELATIVE.as_posix(),
        "inventory_path": INVENTORY_RELATIVE.as_posix(),
        **facts,
        "facts_sha256": canonical_sha256(facts),
        "errors": errors,
    }


def render_text(payload: dict[str, Any]) -> str:
    if payload["status"] == "ok":
        return (
            "Upstream ownership valid: "
            f"{payload['active_count']} active, {payload['removed_count']} removed, "
            f"{payload['managed_claim_count']} managed claims."
        )
    lines = ["Upstream ownership validation failed:"]
    lines.extend(f"{item['code']} {item['path']}: {item['detail']}" for item in payload["errors"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Guru Team upstream ownership inventory")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[5]), help="Guru Trellis source repository root")
    parser.add_argument("--json", action="store_true", help="Print structured validation facts")
    args = parser.parse_args(argv)
    payload = validate_repository(args.repo)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        stream = sys.stdout if payload["status"] == "ok" else sys.stderr
        print(render_text(payload), file=stream)
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
