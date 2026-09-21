#!/usr/bin/env python3
"""Pinned Trellis platform descriptors and exact-selection validation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

from guru_platform_inventory import (
    DEFAULT_PLATFORM_FLAGS as CORE_DEFAULT_PLATFORM_FLAGS,
    PINNED_INVENTORY_SOURCE,
    UPSTREAM_PLATFORMS,
)

PLATFORM_INVENTORY_SOURCE = PINNED_INVENTORY_SOURCE
PLATFORM_INVENTORY_VERSION = "trellis-ai-tools-2026-09-19"
PLATFORM_INVENTORY_SHA256 = (
    "bceda2df084a5f649f7661615588c33dc43221e7cce6c196673a9bc0bfa34171"
)
DEFAULT_PLATFORM_FLAGS = CORE_DEFAULT_PLATFORM_FLAGS
DOGFOOD_PLATFORM_FLAGS = DEFAULT_PLATFORM_FLAGS
SHARED_SKILL_CLAIM = ".agents/skills/guru-*/"


def _descriptor(
    canonical_id: str,
    cli_flag: str,
    template_dir: str,
    config_dir: str,
    skill_root: str,
    entry_path: str,
    entry_kind: str,
    *,
    actual_load: str = "projection_contract",
) -> dict[str, str]:
    return {
        "id": canonical_id,
        "cli_flag": cli_flag,
        "template_dir": template_dir,
        "config_dir": config_dir,
        "skill_root": skill_root,
        "entry_path": entry_path,
        "entry_kind": entry_kind,
        "actual_load": actual_load,
    }


PLATFORM_DESCRIPTORS = (
    _descriptor("claude-code", "claude", "claude", ".claude", ".claude/skills", ".claude/commands/guru/finish-work.md", "markdown_command"),
    _descriptor("cursor", "cursor", "cursor", ".cursor", ".cursor/skills", ".cursor/commands/guru-finish-work.md", "markdown_command"),
    _descriptor("opencode", "opencode", "opencode", ".opencode", ".opencode/skills", ".opencode/commands/guru-finish-work.md", "markdown_command", actual_load="opencode_catalog"),
    _descriptor("codex", "codex", "codex", ".codex", ".codex/skills", ".codex/prompts/guru-finish-work.md", "markdown_prompt"),
    _descriptor("kilo", "kilo", "kilo", ".kilocode", ".kilocode/skills", ".kilocode/workflows/guru-finish-work.md", "markdown_workflow"),
    _descriptor("kiro", "kiro", "kiro", ".kiro/skills", ".kiro/skills", ".kiro/skills/guru-finish-work/SKILL.md", "skill_command"),
    _descriptor("gemini", "gemini", "gemini", ".gemini", ".agents/skills", ".gemini/commands/guru/finish-work.toml", "toml_command"),
    _descriptor("antigravity", "antigravity", "antigravity", ".agent/workflows", ".agent/skills", ".agent/workflows/guru-finish-work.md", "markdown_workflow"),
    _descriptor("devin", "devin", "devin", ".devin/workflows", ".devin/skills", ".devin/workflows/guru-finish-work.md", "markdown_workflow"),
    _descriptor("qoder", "qoder", "qoder", ".qoder", ".qoder/skills", ".qoder/commands/guru-finish-work.md", "markdown_command"),
    _descriptor("codebuddy", "codebuddy", "codebuddy", ".codebuddy", ".codebuddy/skills", ".codebuddy/commands/guru/finish-work.md", "markdown_command"),
    _descriptor("copilot", "copilot", "copilot", ".github/copilot", ".github/skills", ".github/prompts/guru-finish-work.prompt.md", "markdown_prompt"),
    _descriptor("droid", "droid", "droid", ".factory", ".factory/skills", ".factory/commands/guru/finish-work.md", "markdown_command"),
    _descriptor("dsh", "dsh", "dsh", ".dsh", ".agents/skills", ".dsh/skills/guru-finish-work/SKILL.md", "skill_command"),
    _descriptor("pi", "pi", "pi", ".pi", ".agents/skills", ".pi/prompts/guru-finish-work.md", "markdown_prompt"),
    _descriptor("reasonix", "reasonix", "reasonix", ".reasonix", ".reasonix/skills", ".reasonix/skills/guru-finish-work/SKILL.md", "skill_command"),
    _descriptor("zcode", "zcode", "zcode", ".zcode", ".zcode/skills", ".zcode/commands/guru/finish-work.md", "markdown_command"),
    _descriptor("trae", "trae", "trae", ".trae", ".trae/skills", ".trae/commands/guru-finish-work.md", "markdown_command"),
    _descriptor("omp", "omp", "omp", ".omp", ".omp/skills", ".omp/commands/guru-finish-work.md", "markdown_command"),
    _descriptor("grok", "grok", "grok", ".grok", ".grok/skills", ".grok/commands/guru-finish-work.md", "markdown_command"),
    _descriptor("kimi", "kimi", "kimi", ".kimi-code", ".agents/skills", ".kimi-code/skills/guru-finish-work/SKILL.md", "skill_command"),
    _descriptor("snow", "snow", "snow", ".snow/skills", ".snow/skills", ".snow/commands/guru-finish-work.json", "json_prompt"),
)

DESCRIPTOR_KEYS = frozenset(PLATFORM_DESCRIPTORS[0])
DESCRIPTORS_BY_FLAG = {row["cli_flag"]: row for row in PLATFORM_DESCRIPTORS}
DESCRIPTORS_BY_ID = {row["id"]: row for row in PLATFORM_DESCRIPTORS}
PLATFORM_FLAGS = tuple(row["cli_flag"] for row in PLATFORM_DESCRIPTORS)
PLATFORM_IDS = tuple(row["id"] for row in PLATFORM_DESCRIPTORS)

_CORE_ROWS = tuple(
    {
        "id": row.upstream_id,
        "cli_flag": row.cli_flag,
        "template_dir": row.template_dir,
        "config_dir": row.config_dir,
        "skill_root": row.skill_roots[0].as_posix(),
    }
    for row in UPSTREAM_PLATFORMS
)
_EXTENDED_CORE_ROWS = tuple(
    {key: row[key] for key in ("id", "cli_flag", "template_dir", "config_dir", "skill_root")}
    for row in PLATFORM_DESCRIPTORS
)
if _CORE_ROWS != _EXTENDED_CORE_ROWS:
    raise RuntimeError("Ownership platform descriptors drift from guru_platform_inventory")


class PlatformContractError(ValueError):
    """The pinned inventory or one exact target selection is invalid."""


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def is_safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    pure = PurePosixPath(value)
    return not pure.is_absolute() and "." not in pure.parts and ".." not in pure.parts


def validate_descriptors(rows: Any) -> tuple[dict[str, str], ...]:
    if not isinstance(rows, list) or len(rows) != len(PLATFORM_DESCRIPTORS):
        raise PlatformContractError("platform descriptors must contain all 22 pinned rows")
    normalized: list[dict[str, str]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != DESCRIPTOR_KEYS:
            raise PlatformContractError(f"platform descriptor {index} has an invalid field set")
        if not all(isinstance(value, str) and value for value in row.values()):
            raise PlatformContractError(f"platform descriptor {index} contains an empty value")
        for field in ("config_dir", "skill_root", "entry_path"):
            if not is_safe_relative_path(row[field]):
                raise PlatformContractError(f"platform descriptor {index} has invalid {field}")
        normalized.append(dict(row))
    if normalized != list(PLATFORM_DESCRIPTORS):
        raise PlatformContractError("platform descriptors disagree with the pinned inventory")
    if len({row["id"] for row in normalized}) != len(normalized):
        raise PlatformContractError("canonical platform ids must be unique")
    if len({row["cli_flag"] for row in normalized}) != len(normalized):
        raise PlatformContractError("platform cli_flag values must be unique")
    return tuple(normalized)


def validate_selection(values: Any, label: str = "selected_platforms") -> tuple[str, ...]:
    if not isinstance(values, list) or not values:
        raise PlatformContractError(f"{label} must be a non-empty array")
    if any(not isinstance(value, str) or not value for value in values):
        raise PlatformContractError(f"{label} must contain non-empty strings")
    if values != sorted(set(values)):
        raise PlatformContractError(f"{label} must be sorted and unique")
    unknown = sorted(set(values) - set(PLATFORM_FLAGS))
    if unknown:
        raise PlatformContractError(f"{label} contains unknown platform flags: {unknown}")
    return tuple(values)


def descriptor_for_flag(cli_flag: str) -> dict[str, str]:
    try:
        return DESCRIPTORS_BY_FLAG[cli_flag]
    except KeyError as exc:
        raise PlatformContractError(f"unknown platform cli_flag: {cli_flag}") from exc


def descriptor_projection(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, str]]:
    projection = []
    for row in rows:
        projection.append({key: str(row.get(key, "")) for key in DESCRIPTOR_KEYS})
    return projection


def managed_path_claims(
    selected_flags: Iterable[str] = PLATFORM_FLAGS,
    *,
    include_shared: bool = True,
) -> tuple[str, ...]:
    selected = tuple(selected_flags)
    unknown = sorted(set(selected) - set(PLATFORM_FLAGS))
    if unknown:
        raise PlatformContractError(f"cannot derive claims for unknown platforms: {unknown}")
    claims = {".trellis/guru-team/", ".trellis/guru-team/skills/"}
    if include_shared:
        claims.add(SHARED_SKILL_CLAIM)
    for flag in selected:
        descriptor = descriptor_for_flag(flag)
        claims.add(descriptor["skill_root"].rstrip("/") + "/guru-*/")
        claims.add(descriptor["entry_path"])
    return tuple(sorted(claims))


def installed_selection(manifest: Mapping[str, Any]) -> tuple[str, ...]:
    selections: dict[str, tuple[str, ...]] = {}
    for section_name in ("install", "skill_packages", "overlays"):
        section = manifest.get(section_name)
        if not isinstance(section, dict):
            raise PlatformContractError(f"installed manifest is missing {section_name}")
        selections[section_name] = validate_selection(
            section.get("selected_platforms"),
            f"{section_name}.selected_platforms",
        )
    distinct = set(selections.values())
    if len(distinct) != 1:
        raise PlatformContractError(
            "installed manifest selected_platforms sections disagree"
        )
    return next(iter(distinct))


def load_installed_selection(path: Path) -> tuple[str, ...]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PlatformContractError(f"cannot read installed manifest {path}: {exc}") from exc
    if not isinstance(manifest, dict):
        raise PlatformContractError("installed manifest root must be an object")
    return installed_selection(manifest)
