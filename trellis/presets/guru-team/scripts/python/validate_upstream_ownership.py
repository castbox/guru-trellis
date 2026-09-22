#!/usr/bin/env python3
"""Validate descriptor-derived Guru ownership before preset mutation."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any, Mapping


SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from platform_projection_contract import (
    DEFAULT_PLATFORM_FLAGS,
    DESCRIPTOR_KEYS,
    DOGFOOD_PLATFORM_FLAGS,
    PLATFORM_DESCRIPTORS,
    PLATFORM_FLAGS,
    PLATFORM_IDS,
    PLATFORM_INVENTORY_SHA256,
    PLATFORM_INVENTORY_SOURCE,
    PLATFORM_INVENTORY_VERSION,
    PlatformContractError,
    canonical_sha256,
    descriptor_projection,
    installed_selection,
    is_safe_relative_path,
    managed_path_claims,
    validate_descriptors,
)


SCHEMA_RELATIVE = Path("trellis/presets/guru-team/ownership/upstream-ownership.schema.json")
INVENTORY_RELATIVE = Path("trellis/presets/guru-team/ownership/upstream-ownership.json")
EXTENSION_RELATIVE = Path("trellis/guru-team-extension.json")
INSTALLED_EXTENSION_RELATIVE = Path(".trellis/guru-team/extension.json")
INSTALLER_RELATIVE = Path("trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py")
SKILL_REGISTRY_RELATIVE = Path("trellis/skills/guru-team/registry.json")
OVERLAY_ROOT_RELATIVE = Path("trellis/presets/guru-team/overlays")
SKILL_PACKAGE_ROOT_RELATIVE = Path("trellis/skills/guru-team/packages")
WORKFLOW_ROOT_RELATIVE = Path("trellis/workflows/guru-team")

SCHEMA_VERSION = "4.0"
INVENTORY_ID = "guru-team-upstream-ownership"
TARGET_TRELLIS_CLI = "0.6.17"
EXPECTED_SHARED_MANAGED_PATHS = [
    ".trellis/guru-team/",
    ".trellis/guru-team/skills/",
    ".agents/skills/guru-*/",
]
TOP_LEVEL_KEYS = {
    "schema_version",
    "inventory_id",
    "target_trellis_cli",
    "inventory_source",
    "inventory_version",
    "inventory_sha256",
    "overlay_root",
    "shared_managed_paths",
    "dogfood_platforms",
    "platform_descriptors",
}
EXPECTED_MANAGED_PATHS = list(managed_path_claims())
EXPECTED_SKILL_PLATFORMS = ["shared", *PLATFORM_FLAGS]
FORBIDDEN_CAPABILITY_KEYS = {"guru_supported_platforms", "deferred_platforms"}


def ownership_error(code: str, path: str, detail: str) -> dict[str, str]:
    return {"code": code, "path": path, "detail": detail}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_set_sha256(paths: list[str]) -> str:
    return canonical_sha256(sorted(paths))


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


def classify_guru_path(path: str, inventory: Mapping[str, Any]) -> list[str]:
    """Return descriptor-derived ownership labels for one exact path."""
    labels: list[str] = []
    if path.startswith(".trellis/guru-team/"):
        labels.append("installed-runtime")
    if path.startswith("trellis/workflows/guru-team/"):
        labels.append("canonical-workflow-root")
    if path.startswith("trellis/skills/guru-team/"):
        labels.append("canonical-skill-root")
    if "/" not in path and path.startswith("guru-"):
        labels.append("canonical-skill-id")
    rows = inventory.get("platform_descriptors")
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            flag = row.get("cli_flag")
            skill_root = row.get("skill_root")
            entry_path = row.get("entry_path")
            if isinstance(flag, str) and isinstance(skill_root, str):
                prefix = skill_root.rstrip("/") + "/guru-"
                if path.startswith(prefix):
                    labels.append(f"platform:{flag}:skill")
            if isinstance(flag, str) and path == entry_path:
                labels.append(f"platform:{flag}:entry")
    if path.startswith(".agents/skills/guru-"):
        labels.append("shared-skill-discovery")
    return sorted(set(labels))


def extract_managed_assets(installer_path: Path, errors: list[dict[str, str]]) -> list[str]:
    try:
        module = ast.parse(installer_path.read_text(encoding="utf-8"), filename=installer_path.as_posix())
    except (FileNotFoundError, UnicodeDecodeError, SyntaxError) as exc:
        errors.append(ownership_error("managed_asset_source_invalid", INSTALLER_RELATIVE.as_posix(), type(exc).__name__))
        return []
    assignments = [
        node for node in module.body
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
        candidate_stat = candidate.lstat()
        if stat.S_ISDIR(candidate_stat.st_mode):
            continue
        relative = candidate.relative_to(root).as_posix()
        paths.append(relative)
        if stat.S_ISLNK(candidate_stat.st_mode) or not stat.S_ISREG(candidate_stat.st_mode):
            errors.append(ownership_error("overlay_not_regular", relative, "overlay entries must be regular files"))
    return paths


def _manifest_descriptors(capabilities: Mapping[str, Any]) -> Any:
    return capabilities.get("platform_descriptors", capabilities.get("upstream_platforms"))


def _validate_platform_authorities(
    extension: Any,
    inventory: Mapping[str, Any],
    errors: list[dict[str, str]],
) -> tuple[list[str], dict[str, Any]]:
    manifest_paths: list[str] = []
    facts: dict[str, Any] = {}
    if not isinstance(extension, dict) or not isinstance(extension.get("public_api"), dict):
        errors.append(ownership_error("extension_manifest_contract_invalid", "public_api", "expected object"))
        return manifest_paths, facts
    public_api = extension["public_api"]
    paths = public_api.get("managed_paths")
    if not isinstance(paths, list) or any(not isinstance(item, str) for item in paths):
        errors.append(ownership_error("extension_manifest_contract_invalid", "public_api.managed_paths", "expected string array"))
    else:
        manifest_paths = paths
        if paths != EXPECTED_MANAGED_PATHS:
            errors.append(ownership_error("extension_managed_path_set_mismatch", "public_api.managed_paths", "managed paths must be descriptor-derived"))
    capabilities = public_api.get("platform_capabilities")
    if not isinstance(capabilities, dict):
        errors.append(ownership_error("platform_capability_inventory_invalid", "public_api.platform_capabilities", "expected object"))
        return manifest_paths, facts
    forbidden = sorted(set(capabilities) & FORBIDDEN_CAPABILITY_KEYS)
    if forbidden:
        errors.append(ownership_error("platform_capability_legacy_tier", "public_api.platform_capabilities", f"forbidden keys={forbidden}"))
    rows = _manifest_descriptors(capabilities)
    expected_rows = [
        {
            "id": row["id"],
            "template_dir": row["template_dir"],
            "config_dir": row["config_dir"],
            "cli_flag": row["cli_flag"],
        }
        for row in PLATFORM_DESCRIPTORS
    ]
    if rows != expected_rows:
        errors.append(ownership_error("platform_capability_inventory_invalid", "public_api.platform_capabilities.upstream_platforms", "expected exact pinned 22-row AI_TOOLS projection"))
    if capabilities.get("projection_descriptors") != list(PLATFORM_DESCRIPTORS):
        errors.append(ownership_error("platform_projection_descriptor_mismatch", "public_api.platform_capabilities.projection_descriptors", "expected exact descriptor-bound Guru projection inventory"))
    expected_scalars = {
        "inventory_source": PLATFORM_INVENTORY_SOURCE,
        "inventory_version": PLATFORM_INVENTORY_VERSION,
        "inventory_sha256": PLATFORM_INVENTORY_SHA256,
    }
    for key, expected in expected_scalars.items():
        if capabilities.get(key) != expected:
            errors.append(ownership_error("platform_capability_inventory_invalid", f"public_api.platform_capabilities.{key}", f"expected {expected!r}"))
    defaults = capabilities.get("default_platforms", capabilities.get("default_dogfood_platforms"))
    if defaults != list(DEFAULT_PLATFORM_FLAGS):
        errors.append(ownership_error("platform_capability_inventory_invalid", "public_api.platform_capabilities.default_platforms", "expected claude,codex,cursor"))
    facts = {
        "inventory_source": capabilities.get("inventory_source"),
        "inventory_version": capabilities.get("inventory_version"),
        "inventory_sha256": capabilities.get("inventory_sha256"),
        "platform_ids": list(PLATFORM_IDS),
        "platform_cli_flags": list(PLATFORM_FLAGS),
        "default_platform_ids": defaults,
        "descriptor_sha256": canonical_sha256(list(PLATFORM_DESCRIPTORS)),
    }
    return manifest_paths, facts


def _validate_registry(
    repo_root: Path,
    registry: Any,
    inventory: Mapping[str, Any],
    errors: list[dict[str, str]],
) -> tuple[list[str], list[str]]:
    active: list[str] = []
    planned: list[str] = []
    if not isinstance(registry, dict) or not isinstance(registry.get("skills"), list):
        errors.append(ownership_error("skill_registry_contract_invalid", "skills", "expected array"))
        return active, planned
    seen: set[str] = set()
    for index, skill in enumerate(registry["skills"]):
        if not isinstance(skill, dict):
            errors.append(ownership_error("skill_registry_contract_invalid", f"skills[{index}]", "expected object"))
            continue
        skill_id = skill.get("id")
        state = skill.get("state")
        if not isinstance(skill_id, str) or classify_guru_path(skill_id, inventory) != ["canonical-skill-id"]:
            errors.append(ownership_error("skill_id_not_guru_owned", f"skills[{index}].id", "current Skill ids must use guru-*"))
            continue
        if skill_id in seen:
            errors.append(ownership_error("duplicate_skill_id", skill_id, "registry Skill ids must be unique"))
        seen.add(skill_id)
        if state == "active":
            active.append(skill_id)
        elif state == "planned":
            planned.append(skill_id)
            continue
        else:
            errors.append(ownership_error("skill_registry_contract_invalid", f"skills[{index}].state", "expected active or planned"))
            continue
        if skill.get("supported_platforms") != EXPECTED_SKILL_PLATFORMS:
            errors.append(ownership_error("skill_platform_set_mismatch", skill_id, "expected shared plus all 22 cli flags"))
        interface_path = skill.get("interface")
        if not isinstance(interface_path, str):
            errors.append(ownership_error("skill_package_path_mismatch", skill_id, "missing interface path"))
            continue
        interface = read_json(repo_root / "trellis/skills/guru-team" / interface_path, "skill_interface", errors)
        if isinstance(interface, dict) and interface.get("platform_destinations") != EXPECTED_SKILL_PLATFORMS:
            errors.append(ownership_error("skill_interface_platform_set_mismatch", skill_id, "interface destinations disagree with complete inventory"))
    return active, planned


def _validate_public_projection_privacy(
    repo_root: Path,
    inventory: Mapping[str, Any],
    errors: list[dict[str, str]],
) -> None:
    roots = {".agents/skills"}
    for row in inventory.get("platform_descriptors", []):
        if isinstance(row, dict) and isinstance(row.get("skill_root"), str):
            roots.add(row["skill_root"])
    for relative in sorted(roots):
        root = repo_root / relative
        if not root.exists():
            continue
        for candidate in root.glob("guru-*/tests"):
            if candidate.exists():
                errors.append(ownership_error("package_private_test_projected", candidate.relative_to(repo_root).as_posix(), "public platform projection must exclude tests/"))


def _validate_repository(
    repo: Path | str,
    *,
    validate_installed: bool = True,
) -> dict[str, Any]:
    repo_root = Path(os.path.abspath(repo))
    errors: list[dict[str, str]] = []
    schema = read_json(repo_root / SCHEMA_RELATIVE, "ownership_schema", errors)
    inventory = read_json(repo_root / INVENTORY_RELATIVE, "ownership_inventory", errors)
    extension = read_json(repo_root / EXTENSION_RELATIVE, "extension_manifest", errors)
    installed = read_json(repo_root / INSTALLED_EXTENSION_RELATIVE, "installed_extension_manifest", errors)
    registry = read_json(repo_root / SKILL_REGISTRY_RELATIVE, "skill_registry", errors)

    if not isinstance(inventory, dict):
        inventory = {}
    if set(inventory) != TOP_LEVEL_KEYS:
        errors.append(ownership_error("fixed_key_set_mismatch", "$", f"expected={sorted(TOP_LEVEL_KEYS)} actual={sorted(inventory)}"))
    expected_scalars = {
        "schema_version": SCHEMA_VERSION,
        "inventory_id": INVENTORY_ID,
        "target_trellis_cli": TARGET_TRELLIS_CLI,
        "inventory_source": PLATFORM_INVENTORY_SOURCE,
        "inventory_version": PLATFORM_INVENTORY_VERSION,
        "inventory_sha256": PLATFORM_INVENTORY_SHA256,
        "overlay_root": OVERLAY_ROOT_RELATIVE.as_posix(),
    }
    for key, expected in expected_scalars.items():
        if inventory.get(key) != expected:
            errors.append(ownership_error("current_contract_mismatch", f"$.{key}", f"expected {expected!r}"))
    if inventory.get("shared_managed_paths") != EXPECTED_SHARED_MANAGED_PATHS:
        errors.append(ownership_error("shared_managed_path_set_mismatch", "$.shared_managed_paths", "expected exact shared ownership roots"))
    if inventory.get("dogfood_platforms") != list(DOGFOOD_PLATFORM_FLAGS):
        errors.append(ownership_error("dogfood_platform_set_mismatch", "$.dogfood_platforms", "expected claude,codex,cursor"))
    try:
        descriptors = validate_descriptors(inventory.get("platform_descriptors"))
    except PlatformContractError as exc:
        errors.append(ownership_error("platform_descriptor_inventory_invalid", "$.platform_descriptors", str(exc)))
        descriptors = ()

    if isinstance(schema, dict):
        try:
            from jsonschema import Draft202012Validator
            Draft202012Validator.check_schema(schema)
            schema_errors = sorted(Draft202012Validator(schema).iter_errors(inventory), key=lambda item: list(item.path))
            for error in schema_errors:
                errors.append(ownership_error("ownership_schema_validation_failed", "/".join(map(str, error.path)) or "$", error.message))
        except (ImportError, Exception) as exc:
            if type(exc).__name__ != "ModuleNotFoundError":
                errors.append(ownership_error("schema_contract_invalid", SCHEMA_RELATIVE.as_posix(), type(exc).__name__))

    manifest_paths, capability_facts = _validate_platform_authorities(extension, inventory, errors)
    active_skill_ids, planned_skill_ids = _validate_registry(repo_root, registry, inventory, errors)

    if validate_installed and isinstance(installed, dict):
        try:
            selected = installed_selection(installed)
            if selected != DOGFOOD_PLATFORM_FLAGS:
                errors.append(ownership_error("dogfood_installed_selection_mismatch", INSTALLED_EXTENSION_RELATIVE.as_posix(), f"expected={list(DOGFOOD_PLATFORM_FLAGS)} actual={list(selected)}"))
        except PlatformContractError as exc:
            errors.append(ownership_error("dogfood_installed_selection_invalid", INSTALLED_EXTENSION_RELATIVE.as_posix(), str(exc)))

    managed_assets = extract_managed_assets(repo_root / INSTALLER_RELATIVE, errors)
    for relative in managed_assets:
        source = repo_root / WORKFLOW_ROOT_RELATIVE / relative
        try:
            source_stat = source.lstat()
        except FileNotFoundError:
            errors.append(ownership_error("missing_managed_asset", relative, "canonical managed asset is missing"))
            continue
        if stat.S_ISLNK(source_stat.st_mode) or not stat.S_ISREG(source_stat.st_mode):
            errors.append(ownership_error("managed_asset_not_regular", relative, "canonical managed asset must be a regular file"))

    package_root = repo_root / SKILL_PACKAGE_ROOT_RELATIVE
    package_ids = sorted(
        candidate.name for candidate in package_root.iterdir()
        if candidate.is_dir() and not candidate.is_symlink()
    ) if package_root.is_dir() else []
    active_package_ids = sorted(active_skill_ids)
    planned_package_ids = sorted(set(package_ids) & set(planned_skill_ids))
    for skill_id in planned_package_ids:
        errors.append(ownership_error(
            "planned_skill_package_present",
            (SKILL_PACKAGE_ROOT_RELATIVE / skill_id).as_posix(),
            "planned Skill ids reserve identity only and must not have a canonical package",
        ))
    if package_ids != active_package_ids:
        errors.append(ownership_error("canonical_package_set_mismatch", SKILL_PACKAGE_ROOT_RELATIVE.as_posix(), f"packages={package_ids} active={active_package_ids}"))

    overlay_root = repo_root / OVERLAY_ROOT_RELATIVE
    overlay_paths = collect_overlay_paths(overlay_root, errors)
    descriptor_entries = {row["entry_path"] for row in descriptors}
    for path in overlay_paths:
        if path not in descriptor_entries:
            errors.append(ownership_error("undeclared_overlay", path, "overlay is not an explicit platform entry descriptor"))
    regular_overlay_paths = [path for path in overlay_paths if (overlay_root / path).is_file() and not (overlay_root / path).is_symlink()]
    _validate_public_projection_privacy(repo_root, inventory, errors)

    facts = {
        "schema_version": inventory.get("schema_version"),
        "inventory_id": inventory.get("inventory_id"),
        "target_trellis_cli": inventory.get("target_trellis_cli"),
        "schema_sha256": sha256_file(repo_root / SCHEMA_RELATIVE) if (repo_root / SCHEMA_RELATIVE).is_file() else None,
        "inventory_sha256": sha256_file(repo_root / INVENTORY_RELATIVE) if (repo_root / INVENTORY_RELATIVE).is_file() else None,
        "descriptor_count": len(descriptors),
        "descriptor_sha256": canonical_sha256(list(descriptors)),
        "platform_ids": list(PLATFORM_IDS),
        "platform_cli_flags": list(PLATFORM_FLAGS),
        "dogfood_platforms": list(DOGFOOD_PLATFORM_FLAGS),
        "derived_managed_paths": EXPECTED_MANAGED_PATHS,
        "managed_claim_count": len(manifest_paths),
        "classified_managed_claim_count": len(set(manifest_paths) & set(EXPECTED_MANAGED_PATHS)),
        "managed_asset_count": len(managed_assets),
        "overlay_count": len(overlay_paths),
        "overlay_paths_sha256": path_set_sha256(overlay_paths),
        "overlay_payload_aggregate_sha256": payload_aggregate_sha256(overlay_root, regular_overlay_paths),
        "active_skill_count": len(active_skill_ids),
        "planned_skill_count": len(planned_skill_ids),
        "planned_skill_ids": sorted(planned_skill_ids),
        "canonical_package_count": len(package_ids),
        "platform_capabilities": capability_facts,
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


def validate_repository(
    repo: Path | str,
    *,
    validate_installed: bool = True,
) -> dict[str, Any]:
    try:
        return _validate_repository(repo, validate_installed=validate_installed)
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
            f"{payload['descriptor_count']} platform descriptors, "
            f"{payload['managed_claim_count']} derived managed paths, "
            f"dogfood={','.join(payload['dogfood_platforms'])}."
        )
    lines = ["Current Guru ownership validation failed:"]
    lines.extend(f"{item['code']} {item['path']}: {item['detail']}" for item in payload["errors"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate descriptor-derived Guru ownership")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[5]))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = validate_repository(args.repo)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(payload), file=sys.stdout if payload["status"] == "ok" else sys.stderr)
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
