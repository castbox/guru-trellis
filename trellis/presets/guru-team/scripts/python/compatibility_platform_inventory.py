#!/usr/bin/env python3
"""Descriptor-driven platform inventory used by compatibility verification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from compatibility_matrix_errors import MatrixError
from compatibility_matrix_support import _digest
from guru_platform_inventory import (
    DEFAULT_PLATFORM_FLAGS,
    PLATFORM_BY_FLAG,
    PLATFORM_FLAGS,
    UPSTREAM_PLATFORMS,
    validate_manifest_inventory,
)
from platform_projection_contract import (
    DOGFOOD_PLATFORM_FLAGS,
    PLATFORM_DESCRIPTORS,
    PlatformContractError,
    installed_selection,
    managed_path_claims,
    validate_descriptors,
)


SCENARIOS = ("clean", "existing")


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MatrixError(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise MatrixError(f"{label} must be an object")
    return value


def platform_skill_roots(cli_flag: str) -> tuple[Path, ...]:
    try:
        return PLATFORM_BY_FLAG[cli_flag].skill_roots
    except KeyError as exc:
        raise MatrixError(f"unknown platform cli_flag: {cli_flag}") from exc


def platform_init_flag(cli_flag: str) -> str:
    if cli_flag not in PLATFORM_BY_FLAG:
        raise MatrixError(f"unknown platform cli_flag: {cli_flag}")
    return f"--{cli_flag}"


def derive_platform_inventory(repo_root: Path) -> dict[str, Any]:
    canonical = _load_json(
        repo_root / "trellis/guru-team-extension.json",
        "canonical extension manifest",
    )
    try:
        validate_manifest_inventory(canonical)
    except SystemExit as exc:
        raise MatrixError(str(exc)) from exc
    public_api = canonical.get("public_api")
    capabilities = public_api.get("platform_capabilities") if isinstance(public_api, dict) else None
    if not isinstance(capabilities, dict):
        raise MatrixError("public_api.platform_capabilities must be an object")
    legacy = sorted(set(capabilities) & {"guru_supported_platforms", "deferred_platforms"})
    if legacy:
        raise MatrixError(f"legacy platform tiers remain in canonical manifest: {legacy}")
    defaults = capabilities.get("default_platforms", capabilities.get("default_dogfood_platforms"))
    if defaults != list(DEFAULT_PLATFORM_FLAGS):
        raise MatrixError("canonical default platforms must be claude,codex,cursor")

    ownership = _load_json(
        repo_root / "trellis/presets/guru-team/ownership/upstream-ownership.json",
        "upstream ownership",
    )
    try:
        descriptors = validate_descriptors(ownership.get("platform_descriptors"))
    except PlatformContractError as exc:
        raise MatrixError(str(exc)) from exc
    if ownership.get("dogfood_platforms") != list(DOGFOOD_PLATFORM_FLAGS):
        raise MatrixError("ownership dogfood selection must be claude,codex,cursor")

    managed_paths = public_api.get("managed_paths") if isinstance(public_api, dict) else None
    if managed_paths != list(managed_path_claims()):
        raise MatrixError("canonical managed paths are not descriptor-derived")

    installed = _load_json(
        repo_root / ".trellis/guru-team/extension.json",
        "source dogfood installed manifest",
    )
    try:
        dogfood = installed_selection(installed)
    except PlatformContractError as exc:
        raise MatrixError(str(exc)) from exc
    if dogfood != DOGFOOD_PLATFORM_FLAGS:
        raise MatrixError(
            f"source dogfood selection mismatch: expected={list(DOGFOOD_PLATFORM_FLAGS)} "
            f"actual={list(dogfood)}"
        )

    result = {
        "schema_version": "2.0",
        "platforms": list(PLATFORM_FLAGS),
        "canonical_platform_ids": [row.upstream_id for row in UPSTREAM_PLATFORMS],
        "default_platforms": list(DEFAULT_PLATFORM_FLAGS),
        "dogfood_platforms": list(dogfood),
        "descriptors": list(descriptors),
        "descriptor_count": len(descriptors),
    }
    result["identity_sha256"] = _digest(result)
    return result


def build_matrix(repo_root: Path) -> dict[str, Any]:
    inventory = derive_platform_inventory(repo_root)
    representative_platforms = ["claude", "codex", "cursor", "opencode"]
    cells = [
        {
            "cell_id": f"{platform}-{scenario}",
            "platform": platform,
            "scenario": scenario,
            "shared_projection": True,
        }
        for platform in representative_platforms
        for scenario in SCENARIOS
    ]
    result = {
        "schema_version": "2.0",
        "platform_inventory_sha256": inventory["identity_sha256"],
        "platforms": representative_platforms,
        "upstream_platform_count": len(inventory["platforms"]),
        "descriptor_count": inventory["descriptor_count"],
        "cells": cells,
        "cell_count": len(cells),
    }
    result["matrix_sha256"] = _digest(result)
    return result
