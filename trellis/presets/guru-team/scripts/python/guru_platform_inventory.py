#!/usr/bin/env python3
"""Pinned upstream Trellis platform inventory and projection descriptors."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


PINNED_INVENTORY_SOURCE = (
    "castbox/Trellis@43fffc170927c85d9f7fc106cc5a059e80d4530b:"
    "packages/cli/src/types/ai-tools.ts#AI_TOOLS"
)
DEFAULT_PLATFORM_FLAGS = ("claude", "codex", "cursor")


@dataclass(frozen=True)
class PlatformDescriptor:
    upstream_id: str
    template_dir: str
    config_dir: str
    cli_flag: str
    skill_roots: tuple[Path, ...]

    def manifest_row(self) -> dict[str, str]:
        return {
            "id": self.upstream_id,
            "template_dir": self.template_dir,
            "config_dir": self.config_dir,
            "cli_flag": self.cli_flag,
        }


UPSTREAM_PLATFORMS = (
    PlatformDescriptor("claude-code", "claude", ".claude", "claude", (Path(".claude/skills"),)),
    PlatformDescriptor("cursor", "cursor", ".cursor", "cursor", (Path(".cursor/skills"),)),
    PlatformDescriptor("opencode", "opencode", ".opencode", "opencode", (Path(".opencode/skills"),)),
    PlatformDescriptor("codex", "codex", ".codex", "codex", (Path(".codex/skills"),)),
    PlatformDescriptor("kilo", "kilo", ".kilocode", "kilo", (Path(".kilocode/skills"),)),
    PlatformDescriptor("kiro", "kiro", ".kiro/skills", "kiro", (Path(".kiro/skills"),)),
    PlatformDescriptor("gemini", "gemini", ".gemini", "gemini", (Path(".agents/skills"),)),
    PlatformDescriptor("antigravity", "antigravity", ".agent/workflows", "antigravity", (Path(".agent/skills"),)),
    PlatformDescriptor("devin", "devin", ".devin/workflows", "devin", (Path(".devin/skills"),)),
    PlatformDescriptor("qoder", "qoder", ".qoder", "qoder", (Path(".qoder/skills"),)),
    PlatformDescriptor("codebuddy", "codebuddy", ".codebuddy", "codebuddy", (Path(".codebuddy/skills"),)),
    PlatformDescriptor("copilot", "copilot", ".github/copilot", "copilot", (Path(".github/skills"),)),
    PlatformDescriptor("droid", "droid", ".factory", "droid", (Path(".factory/skills"),)),
    PlatformDescriptor("dsh", "dsh", ".dsh", "dsh", (Path(".agents/skills"),)),
    PlatformDescriptor("pi", "pi", ".pi", "pi", (Path(".agents/skills"),)),
    PlatformDescriptor("reasonix", "reasonix", ".reasonix", "reasonix", (Path(".reasonix/skills"),)),
    PlatformDescriptor("zcode", "zcode", ".zcode", "zcode", (Path(".zcode/skills"),)),
    PlatformDescriptor("trae", "trae", ".trae", "trae", (Path(".trae/skills"),)),
    PlatformDescriptor("omp", "omp", ".omp", "omp", (Path(".omp/skills"),)),
    PlatformDescriptor("grok", "grok", ".grok", "grok", (Path(".grok/skills"),)),
    PlatformDescriptor("kimi", "kimi", ".kimi-code", "kimi", (Path(".agents/skills"),)),
    PlatformDescriptor("snow", "snow", ".snow/skills", "snow", (Path(".snow/skills"),)),
)

PLATFORM_FLAGS = tuple(descriptor.cli_flag for descriptor in UPSTREAM_PLATFORMS)
PLATFORM_BY_FLAG = {descriptor.cli_flag: descriptor for descriptor in UPSTREAM_PLATFORMS}
PLATFORM_BY_UPSTREAM_ID = {
    descriptor.upstream_id: descriptor for descriptor in UPSTREAM_PLATFORMS
}

if len(PLATFORM_FLAGS) != 22 or len(PLATFORM_BY_FLAG) != len(UPSTREAM_PLATFORMS):
    raise RuntimeError("Pinned Trellis platform inventory must contain 22 unique cli_flag values")
if len(PLATFORM_BY_UPSTREAM_ID) != len(UPSTREAM_PLATFORMS):
    raise RuntimeError("Pinned Trellis platform inventory must contain unique AITool ids")
if not set(DEFAULT_PLATFORM_FLAGS).issubset(PLATFORM_BY_FLAG):
    raise RuntimeError("Default platform selection must be part of the pinned inventory")


def _platform_capabilities(manifest: dict[str, Any]) -> dict[str, Any]:
    public_api = manifest.get("public_api")
    capabilities = (
        public_api.get("platform_capabilities")
        if isinstance(public_api, dict)
        else None
    )
    if not isinstance(capabilities, dict):
        raise SystemExit("Guru Team extension manifest has no platform capability inventory")
    return capabilities


def validate_manifest_inventory(
    manifest: dict[str, Any],
) -> tuple[PlatformDescriptor, ...]:
    """Bind the canonical manifest to the pinned upstream 22-row inventory."""
    capabilities = _platform_capabilities(manifest)
    if capabilities.get("inventory_source") != PINNED_INVENTORY_SOURCE:
        raise SystemExit("Guru Team extension manifest has an unexpected upstream inventory source")
    rows = capabilities.get("upstream_platforms")
    if not isinstance(rows, list) or len(rows) != len(UPSTREAM_PLATFORMS):
        raise SystemExit("Guru Team extension manifest must contain all 22 upstream platforms")
    expected = [descriptor.manifest_row() for descriptor in UPSTREAM_PLATFORMS]
    if rows != expected:
        raise SystemExit("Guru Team extension manifest platform rows drift from the pinned inventory")
    return UPSTREAM_PLATFORMS


def select_platforms(
    requested: Iterable[str] | None,
    available: tuple[str, ...] = PLATFORM_FLAGS,
    default: tuple[str, ...] = DEFAULT_PLATFORM_FLAGS,
) -> set[str]:
    if requested:
        selected = set(requested)
        unknown = selected - set(available)
        if unknown:
            raise SystemExit(f"Unknown Guru Team platform selection: {', '.join(sorted(unknown))}")
        return selected
    return set(default)


def selected_skill_roots(platforms: Iterable[str]) -> tuple[Path, ...]:
    """Return stable, de-duplicated native skill roots for an exact selection."""
    selected = set(platforms)
    unknown = selected - set(PLATFORM_BY_FLAG)
    if unknown:
        raise SystemExit(f"Unknown Guru Team platform selection: {', '.join(sorted(unknown))}")
    roots: list[Path] = [Path(".agents/skills")]
    ordered_flags = ("codex", "claude", "cursor", "opencode") + tuple(
        flag
        for flag in PLATFORM_FLAGS
        if flag not in {"codex", "claude", "cursor", "opencode"}
    )
    for flag in ordered_flags:
        if flag not in selected:
            continue
        for root in PLATFORM_BY_FLAG[flag].skill_roots:
            if root not in roots:
                roots.append(root)
    return tuple(roots)


def all_skill_roots() -> tuple[Path, ...]:
    return selected_skill_roots(PLATFORM_FLAGS)
