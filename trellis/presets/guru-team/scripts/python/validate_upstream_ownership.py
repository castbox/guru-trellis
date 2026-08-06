#!/usr/bin/env python3
"""Validate the current Guru Team ownership boundary before preset mutation."""

from __future__ import annotations

import argparse
import ast
import fnmatch
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_RELATIVE = Path("trellis/presets/guru-team/ownership/upstream-ownership.schema.json")
INVENTORY_RELATIVE = Path("trellis/presets/guru-team/ownership/upstream-ownership.json")
EXTENSION_RELATIVE = Path("trellis/guru-team-extension.json")
INSTALLER_RELATIVE = Path("trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py")
SKILL_REGISTRY_RELATIVE = Path("trellis/skills/guru-team/registry.json")
OVERLAY_ROOT_RELATIVE = Path("trellis/presets/guru-team/overlays")
SKILL_PACKAGE_ROOT_RELATIVE = Path("trellis/skills/guru-team/packages")
WORKFLOW_ROOT_RELATIVE = Path("trellis/workflows/guru-team")

SCHEMA_VERSION = "3.0"
INVENTORY_ID = "guru-team-upstream-ownership"
TARGET_TRELLIS_CLI = "0.6.5"
TOP_LEVEL_KEYS = {
    "schema_version",
    "inventory_id",
    "target_trellis_cli",
    "overlay_root",
    "guru_owned_rules",
    "managed_path_claims",
}
RULE_KEYS = {"id", "match_type", "pattern", "category"}
CLAIM_KEYS = {"path", "category", "classification_rule"}
EXPECTED_GURU_RULES = [
    {
        "id": "installed-runtime",
        "match_type": "path_prefix",
        "pattern": ".trellis/guru-team/",
        "category": "guru_owned",
    },
    {
        "id": "canonical-workflow-root",
        "match_type": "path_prefix",
        "pattern": "trellis/workflows/guru-team/",
        "category": "guru_owned",
    },
    {
        "id": "canonical-skill-root",
        "match_type": "path_prefix",
        "pattern": "trellis/skills/guru-team/",
        "category": "guru_owned",
    },
    {
        "id": "canonical-skill-id",
        "match_type": "skill_id_prefix",
        "pattern": "guru-",
        "category": "guru_owned",
    },
    {
        "id": "shared-skill-discovery",
        "match_type": "path_glob",
        "pattern": ".agents/skills/guru-*/**",
        "category": "guru_owned",
    },
    {
        "id": "codex-skill-discovery",
        "match_type": "path_glob",
        "pattern": ".codex/skills/guru-*/**",
        "category": "guru_owned",
    },
    {
        "id": "cursor-skill-discovery",
        "match_type": "path_glob",
        "pattern": ".cursor/skills/guru-*/**",
        "category": "guru_owned",
    },
    {
        "id": "claude-skill-discovery",
        "match_type": "path_glob",
        "pattern": ".claude/skills/guru-*/**",
        "category": "guru_owned",
    },
    {
        "id": "codex-finish-entry",
        "match_type": "path_prefix",
        "pattern": ".codex/prompts/guru-finish-work.md",
        "category": "guru_owned",
    },
    {
        "id": "claude-finish-entry",
        "match_type": "path_prefix",
        "pattern": ".claude/commands/guru/finish-work.md",
        "category": "guru_owned",
    },
    {
        "id": "cursor-finish-entry",
        "match_type": "path_prefix",
        "pattern": ".cursor/commands/guru-finish-work.md",
        "category": "guru_owned",
    },
]
EXPECTED_MANAGED_PATH_CLAIMS = [
    {
        "path": ".trellis/guru-team/",
        "category": "guru_owned",
        "classification_rule": "installed-runtime",
    },
    {
        "path": ".trellis/guru-team/skills/",
        "category": "guru_owned",
        "classification_rule": "installed-runtime",
    },
    {
        "path": ".agents/skills/guru-*/",
        "category": "guru_owned",
        "classification_rule": "shared-skill-discovery",
    },
    {
        "path": ".codex/skills/guru-*/",
        "category": "guru_owned",
        "classification_rule": "codex-skill-discovery",
    },
    {
        "path": ".cursor/skills/guru-*/",
        "category": "guru_owned",
        "classification_rule": "cursor-skill-discovery",
    },
    {
        "path": ".claude/skills/guru-*/",
        "category": "guru_owned",
        "classification_rule": "claude-skill-discovery",
    },
    {
        "path": ".codex/prompts/guru-finish-work.md",
        "category": "guru_owned",
        "classification_rule": "codex-finish-entry",
    },
    {
        "path": ".claude/commands/guru/finish-work.md",
        "category": "guru_owned",
        "classification_rule": "claude-finish-entry",
    },
    {
        "path": ".cursor/commands/guru-finish-work.md",
        "category": "guru_owned",
        "classification_rule": "cursor-finish-entry",
    },
]
EXPECTED_MANAGED_PATHS = [claim["path"] for claim in EXPECTED_MANAGED_PATH_CLAIMS]
EXPECTED_FINISH_OVERLAY_CLAIMS = {
    ".codex/prompts/guru-finish-work.md": "codex-finish-entry",
    ".claude/commands/guru/finish-work.md": "claude-finish-entry",
    ".cursor/commands/guru-finish-work.md": "cursor-finish-entry",
}
EXPECTED_SKILL_PLATFORMS = ["shared", "codex", "cursor", "claude"]
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


def payload_aggregate_sha256(root: Path, paths: list[str]) -> str:
    digest = hashlib.sha256()
    for relative in sorted(paths):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update((root / relative).read_bytes())
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
    definitions = node.get("$defs")
    if definitions is not None:
        if not isinstance(definitions, dict):
            errors.append(ownership_error("schema_contract_invalid", f"{path}.$defs", "must be an object"))
        else:
            for name, child in definitions.items():
                validate_schema_node(child, root, f"{path}.$defs.{name}", errors)
    if "items" in node:
        validate_schema_node(node["items"], root, f"{path}.items", errors)
    if "pattern" in node:
        try:
            re.compile(node["pattern"])
        except (TypeError, re.error):
            errors.append(ownership_error("schema_contract_invalid", f"{path}.pattern", "invalid regular expression"))
    if "enum" in node and (not isinstance(node["enum"], list) or not node["enum"]):
        errors.append(ownership_error("schema_contract_invalid", f"{path}.enum", "enum must be a non-empty array"))
    if "uniqueItems" in node and not isinstance(node["uniqueItems"], bool):
        errors.append(ownership_error("schema_contract_invalid", f"{path}.uniqueItems", "must be boolean"))
    for keyword in ("minItems", "maxItems", "minLength"):
        if keyword in node and (not isinstance(node[keyword], int) or isinstance(node[keyword], bool) or node[keyword] < 0):
            errors.append(ownership_error("schema_contract_invalid", f"{path}.{keyword}", "must be a non-negative integer"))


def validate_schema_contract(schema: Any, errors: list[dict[str, str]]) -> None:
    if not isinstance(schema, dict):
        errors.append(ownership_error("schema_contract_invalid", SCHEMA_RELATIVE.as_posix(), "root must be an object"))
        return
    validate_schema_node(schema, schema, "$", errors)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append(ownership_error("schema_contract_invalid", "$.$schema", "expected Draft 2020-12"))
    if schema.get("$id") != "https://github.com/castbox/guru-trellis/schemas/upstream-ownership-3.0.json":
        errors.append(ownership_error("schema_contract_invalid", "$.$id", "expected current ownership schema id"))
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        errors.append(ownership_error("schema_contract_invalid", "$", "root must be a closed object"))
    required = schema.get("required")
    properties = schema.get("properties")
    if not (
        isinstance(required, list)
        and all(isinstance(item, str) for item in required)
        and isinstance(properties, dict)
        and set(required) == TOP_LEVEL_KEYS
        and set(properties) == TOP_LEVEL_KEYS
    ):
        errors.append(ownership_error("schema_contract_invalid", "$", "root required/properties must match current inventory fields"))
    definitions = schema.get("$defs")
    if not isinstance(definitions, dict) or set(definitions) != {"safePath", "guruOwnedRule", "managedPathClaim"}:
        errors.append(ownership_error("schema_contract_invalid", "$.$defs", "expected current ownership definitions"))


def classify_guru_path(path: str, rules: list[dict[str, Any]]) -> list[str]:
    matches: list[str] = []
    for rule in rules:
        match_type = rule.get("match_type")
        pattern = rule.get("pattern")
        if not isinstance(pattern, str):
            continue
        matched = False
        if match_type == "path_prefix":
            matched = path.startswith(pattern) if pattern.endswith("/") else path == pattern
        elif match_type == "path_glob":
            matched = fnmatch.fnmatchcase(path, pattern)
        elif match_type == "skill_id_prefix":
            matched = "/" not in path and path.startswith(pattern)
        if matched:
            matches.append(str(rule.get("id") or ""))
    return matches


def claim_matches_rule(claim_path: str, rule: dict[str, Any]) -> bool:
    if rule.get("match_type") == "path_prefix":
        pattern = str(rule.get("pattern") or "")
        return claim_path.startswith(pattern) if pattern.endswith("/") else claim_path == pattern
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


def collect_overlay_paths(root: Path, errors: list[dict[str, str]]) -> list[str]:
    try:
        root_stat = root.lstat()
    except FileNotFoundError:
        errors.append(ownership_error("missing_overlay_root", OVERLAY_ROOT_RELATIVE.as_posix(), "overlay root is missing"))
        return []
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        errors.append(ownership_error("overlay_root_not_directory", OVERLAY_ROOT_RELATIVE.as_posix(), "overlay root must be a real directory"))
        return []
    paths: list[str] = []
    for candidate in sorted(root.rglob("*")):
        relative = candidate.relative_to(root).as_posix()
        candidate_stat = candidate.lstat()
        if stat.S_ISDIR(candidate_stat.st_mode):
            continue
        paths.append(relative)
        if stat.S_ISLNK(candidate_stat.st_mode) or not stat.S_ISREG(candidate_stat.st_mode):
            errors.append(ownership_error("overlay_not_regular", relative, "overlay entries must be regular files"))
    return paths


def _validate_repository(repo: Path | str) -> dict[str, Any]:
    repo_root = Path(os.path.abspath(repo))
    errors: list[dict[str, str]] = []
    schema = read_json(repo_root / SCHEMA_RELATIVE, "ownership_schema", errors)
    inventory = read_json(repo_root / INVENTORY_RELATIVE, "ownership_inventory", errors)
    extension = read_json(repo_root / EXTENSION_RELATIVE, "extension_manifest", errors)
    registry = read_json(repo_root / SKILL_REGISTRY_RELATIVE, "skill_registry", errors)

    if schema is not None:
        validate_schema_contract(schema, errors)

    rules: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    if require_exact_keys(inventory, TOP_LEVEL_KEYS, "$", errors):
        assert isinstance(inventory, dict)
        expected_scalars = {
            "schema_version": SCHEMA_VERSION,
            "inventory_id": INVENTORY_ID,
            "target_trellis_cli": TARGET_TRELLIS_CLI,
            "overlay_root": OVERLAY_ROOT_RELATIVE.as_posix(),
        }
        for key, expected in expected_scalars.items():
            if inventory.get(key) != expected:
                errors.append(ownership_error("current_contract_mismatch", f"$.{key}", f"expected {expected!r}"))
        rule_values = inventory.get("guru_owned_rules")
        if not isinstance(rule_values, list):
            errors.append(ownership_error("schema_type_mismatch", "$.guru_owned_rules", "expected array"))
        else:
            for index, rule in enumerate(rule_values):
                if require_exact_keys(rule, RULE_KEYS, f"$.guru_owned_rules[{index}]", errors):
                    rules.append(rule)
        claim_values = inventory.get("managed_path_claims")
        if not isinstance(claim_values, list):
            errors.append(ownership_error("schema_type_mismatch", "$.managed_path_claims", "expected array"))
        else:
            for index, claim in enumerate(claim_values):
                if require_exact_keys(claim, CLAIM_KEYS, f"$.managed_path_claims[{index}]", errors):
                    claims.append(claim)

    if rules != EXPECTED_GURU_RULES:
        errors.append(ownership_error("guru_owned_rule_set_mismatch", "$.guru_owned_rules", "expected the exact current Guru ownership rules"))
    rule_by_id = {str(rule.get("id")): rule for rule in rules}
    if len(rule_by_id) != len(rules):
        errors.append(ownership_error("duplicate_guru_owned_rule", "$.guru_owned_rules", "rule ids must be unique"))
    for index, rule in enumerate(rules):
        if rule.get("category") != "guru_owned":
            errors.append(ownership_error("rule_category_mismatch", f"$.guru_owned_rules[{index}]", "only guru_owned rules are current"))

    claim_by_path: dict[str, dict[str, Any]] = {}
    for index, claim in enumerate(claims):
        claim_path = claim.get("path")
        display_path = claim_path if isinstance(claim_path, str) else f"$.managed_path_claims[{index}].path"
        if not is_safe_relative_path(claim_path):
            errors.append(ownership_error("invalid_managed_claim_path", str(display_path), "claim must be a safe repo-relative path"))
            continue
        if claim_path in claim_by_path:
            errors.append(ownership_error("duplicate_managed_claim", claim_path, "managed claim appears more than once"))
        claim_by_path[claim_path] = claim
        rule = rule_by_id.get(str(claim.get("classification_rule")))
        if claim.get("category") != "guru_owned":
            errors.append(ownership_error("managed_claim_category_mismatch", claim_path, "only guru_owned claims are current"))
        if rule is None or not claim_matches_rule(claim_path, rule):
            errors.append(ownership_error("guru_owned_claim_rule_mismatch", claim_path, "claim is outside its anchored Guru rule"))
    if claims != EXPECTED_MANAGED_PATH_CLAIMS:
        errors.append(ownership_error("managed_claim_set_mismatch", "$.managed_path_claims", "expected the exact current Guru managed claims"))

    overlay_root = repo_root / OVERLAY_ROOT_RELATIVE
    actual_overlay_paths = collect_overlay_paths(overlay_root, errors)
    expected_overlay_paths = sorted(EXPECTED_FINISH_OVERLAY_CLAIMS)
    for path in sorted(set(actual_overlay_paths) - set(expected_overlay_paths)):
        errors.append(ownership_error("undeclared_overlay", path, "overlay is outside the current finish-entry set"))
    for path in sorted(set(expected_overlay_paths) - set(actual_overlay_paths)):
        errors.append(ownership_error("missing_finish_overlay", path, "current finish entry is missing"))
    regular_overlay_paths: list[str] = []
    for path in expected_overlay_paths:
        target = overlay_root / path
        try:
            target_stat = target.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISREG(target_stat.st_mode) and not stat.S_ISLNK(target_stat.st_mode):
            regular_overlay_paths.append(path)
        expected_claim = {
            "path": path,
            "category": "guru_owned",
            "classification_rule": EXPECTED_FINISH_OVERLAY_CLAIMS[path],
        }
        if claim_by_path.get(path) != expected_claim:
            errors.append(ownership_error("finish_overlay_claim_mismatch", path, f"expected={expected_claim}"))

    manifest_paths: list[str] = []
    manifest_active_ids: list[str] = []
    manifest_planned_ids: list[str] = []
    if isinstance(extension, dict):
        public_api = extension.get("public_api")
        if not isinstance(public_api, dict):
            errors.append(ownership_error("extension_manifest_contract_invalid", "public_api", "expected object"))
        else:
            managed_paths = public_api.get("managed_paths")
            if not isinstance(managed_paths, list) or any(not isinstance(item, str) for item in managed_paths):
                errors.append(ownership_error("extension_manifest_contract_invalid", "public_api.managed_paths", "expected string array"))
            else:
                manifest_paths = managed_paths
                if managed_paths != EXPECTED_MANAGED_PATHS:
                    errors.append(ownership_error("extension_managed_path_set_mismatch", "public_api.managed_paths", "expected the exact current Guru managed paths"))
            contracts = public_api.get("skill_contracts")
            if not isinstance(contracts, dict):
                errors.append(ownership_error("extension_manifest_contract_invalid", "public_api.skill_contracts", "expected object"))
            else:
                active_values = contracts.get("active_skill_ids")
                planned_values = contracts.get("planned_skill_ids")
                if not isinstance(active_values, list) or any(not isinstance(item, str) for item in active_values):
                    errors.append(ownership_error("extension_manifest_contract_invalid", "public_api.skill_contracts.active_skill_ids", "expected string array"))
                else:
                    manifest_active_ids = active_values
                if not isinstance(planned_values, list) or any(not isinstance(item, str) for item in planned_values):
                    errors.append(ownership_error("extension_manifest_contract_invalid", "public_api.skill_contracts.planned_skill_ids", "expected string array"))
                else:
                    manifest_planned_ids = planned_values
                if contracts.get("registry_lifecycle") != ["planned", "active"]:
                    errors.append(ownership_error("extension_manifest_contract_invalid", "public_api.skill_contracts.registry_lifecycle", "expected current registry lifecycle"))

    managed_assets = extract_managed_assets(repo_root / INSTALLER_RELATIVE, errors)
    for relative in managed_assets:
        installed_path = f".trellis/guru-team/{relative}"
        if classify_guru_path(installed_path, rules) != ["installed-runtime"]:
            errors.append(ownership_error("unclassified_managed_asset", installed_path, "asset is outside the installed Guru runtime"))
        source = repo_root / WORKFLOW_ROOT_RELATIVE / relative
        try:
            source_stat = source.lstat()
        except FileNotFoundError:
            errors.append(ownership_error("missing_managed_asset", relative, "canonical managed asset is missing"))
            continue
        if stat.S_ISLNK(source_stat.st_mode) or not stat.S_ISREG(source_stat.st_mode):
            errors.append(ownership_error("managed_asset_not_regular", relative, "canonical managed asset must be a regular file"))

    active_skill_ids: list[str] = []
    planned_skill_ids: list[str] = []
    if isinstance(registry, dict) and isinstance(registry.get("skills"), list):
        seen_ids: set[str] = set()
        for index, skill in enumerate(registry["skills"]):
            if not isinstance(skill, dict):
                errors.append(ownership_error("skill_registry_contract_invalid", f"skills[{index}]", "expected object"))
                continue
            skill_id = skill.get("id")
            state = skill.get("state")
            if not isinstance(skill_id, str) or classify_guru_path(skill_id, rules) != ["canonical-skill-id"]:
                errors.append(ownership_error("skill_id_not_guru_owned", f"skills[{index}].id", "current Skill ids must use guru-*"))
                continue
            if skill_id in seen_ids:
                errors.append(ownership_error("duplicate_skill_id", skill_id, "registry Skill ids must be unique"))
            seen_ids.add(skill_id)
            if state == "active":
                active_skill_ids.append(skill_id)
            elif state == "planned":
                planned_skill_ids.append(skill_id)
            else:
                errors.append(ownership_error("skill_registry_contract_invalid", f"skills[{index}].state", "expected active or planned"))
                continue
            expected_package = f"packages/{skill_id}"
            expected_interface = f"{expected_package}/interface.json"
            if skill.get("package") != expected_package or skill.get("interface") != expected_interface:
                errors.append(ownership_error("skill_package_path_mismatch", skill_id, "registry package/interface must use the current canonical package"))
            platforms = skill.get("supported_platforms")
            if platforms != EXPECTED_SKILL_PLATFORMS:
                errors.append(ownership_error("skill_platform_set_mismatch", skill_id, "expected the current shared and platform discovery set"))
            if state == "active":
                package_root = repo_root / SKILL_PACKAGE_ROOT_RELATIVE / skill_id
                interface_path = package_root / "interface.json"
                if not package_root.is_dir() or package_root.is_symlink():
                    errors.append(ownership_error("active_skill_package_missing", skill_id, "canonical package directory is missing"))
                if not interface_path.is_file() or interface_path.is_symlink():
                    errors.append(ownership_error("active_skill_interface_missing", skill_id, "canonical interface is missing"))
                for platform, root in {
                    "shared": ".agents",
                    "codex": ".codex",
                    "cursor": ".cursor",
                    "claude": ".claude",
                }.items():
                    discovery = f"{root}/skills/{skill_id}/SKILL.md"
                    expected_rule = "shared-skill-discovery" if platform == "shared" else f"{platform}-skill-discovery"
                    if classify_guru_path(discovery, rules) != [expected_rule]:
                        errors.append(ownership_error("skill_discovery_path_unclassified", discovery, "discovery path is outside its Guru rule"))
    elif registry is not None:
        errors.append(ownership_error("skill_registry_contract_invalid", "skills", "expected array"))

    package_root = repo_root / SKILL_PACKAGE_ROOT_RELATIVE
    canonical_package_ids: list[str] = []
    if package_root.is_dir() and not package_root.is_symlink():
        for candidate in sorted(package_root.iterdir()):
            if candidate.is_symlink() or not candidate.is_dir():
                errors.append(ownership_error("canonical_package_entry_invalid", candidate.name, "package root may contain only real directories"))
                continue
            canonical_package_ids.append(candidate.name)
    else:
        errors.append(ownership_error("canonical_package_root_invalid", SKILL_PACKAGE_ROOT_RELATIVE.as_posix(), "package root must be a real directory"))
    if sorted(canonical_package_ids) != sorted(active_skill_ids):
        errors.append(ownership_error("canonical_package_set_mismatch", SKILL_PACKAGE_ROOT_RELATIVE.as_posix(), f"packages={sorted(canonical_package_ids)} active={sorted(active_skill_ids)}"))
    if sorted(active_skill_ids) != sorted(manifest_active_ids):
        errors.append(ownership_error("active_skill_manifest_mismatch", "public_api.skill_contracts.active_skill_ids", f"registry={sorted(active_skill_ids)} manifest={sorted(manifest_active_ids)}"))
    if sorted(planned_skill_ids) != sorted(manifest_planned_ids):
        errors.append(ownership_error("planned_skill_manifest_mismatch", "public_api.skill_contracts.planned_skill_ids", f"registry={sorted(planned_skill_ids)} manifest={sorted(manifest_planned_ids)}"))

    overlay_payload_sha256 = (
        payload_aggregate_sha256(overlay_root, expected_overlay_paths)
        if regular_overlay_paths == expected_overlay_paths
        else None
    )
    facts = {
        "schema_version": inventory.get("schema_version") if isinstance(inventory, dict) else None,
        "inventory_id": inventory.get("inventory_id") if isinstance(inventory, dict) else None,
        "target_trellis_cli": inventory.get("target_trellis_cli") if isinstance(inventory, dict) else None,
        "overlay_root": inventory.get("overlay_root") if isinstance(inventory, dict) else None,
        "schema_sha256": sha256_file(repo_root / SCHEMA_RELATIVE) if (repo_root / SCHEMA_RELATIVE).is_file() else None,
        "inventory_sha256": sha256_file(repo_root / INVENTORY_RELATIVE) if (repo_root / INVENTORY_RELATIVE).is_file() else None,
        "guru_owned_rules_sha256": canonical_sha256(rules),
        "managed_path_claims_sha256": canonical_sha256(claims),
        "overlay_count": len(actual_overlay_paths),
        "overlay_paths_sha256": path_set_sha256(actual_overlay_paths),
        "overlay_payload_aggregate_sha256": overlay_payload_sha256,
        "managed_claim_count": len(manifest_paths),
        "classified_managed_claim_count": len(set(manifest_paths) & set(claim_by_path)),
        "managed_asset_count": len(managed_assets),
        "active_skill_count": len(active_skill_ids),
        "planned_skill_count": len(planned_skill_ids),
        "canonical_package_count": len(canonical_package_ids),
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


def validate_repository(repo: Path | str) -> dict[str, Any]:
    try:
        return _validate_repository(repo)
    except Exception as exc:
        error = ownership_error("validator_internal_error", "$", type(exc).__name__)
        return {
            "status": "error",
            "schema_path": SCHEMA_RELATIVE.as_posix(),
            "inventory_path": INVENTORY_RELATIVE.as_posix(),
            "facts_sha256": canonical_sha256({"error": error}),
            "errors": [error],
        }


def render_text(payload: dict[str, Any]) -> str:
    if payload["status"] == "ok":
        return (
            "Current Guru ownership valid: "
            f"{payload['managed_claim_count']} managed claims, "
            f"{payload['overlay_count']} finish overlays, "
            f"{payload['active_skill_count']} active Skills."
        )
    lines = ["Current Guru ownership validation failed:"]
    lines.extend(f"{item['code']} {item['path']}: {item['detail']}" for item in payload["errors"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the current Guru Team ownership inventory")
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
