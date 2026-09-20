"""Shared deterministic projections for the Trellis compatibility matrix."""

from __future__ import annotations

import hashlib
import json
import stat
from pathlib import Path
from typing import Any, Iterable, Mapping

from compatibility_matrix_errors import MatrixError


def _canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _sorted_strings(values: Iterable[str]) -> list[str]:
    return sorted(set(values), key=lambda item: item.encode("utf-8"))


def _executable_projection(path: Path) -> int:
    """Project the installer-owned executable bit, not archive/umask permissions."""

    return 1 if path.stat().st_mode & stat.S_IXUSR else 0


def _managed_asset_executable(relative: str) -> bool:
    return relative.startswith(".trellis/guru-team/scripts/bash/")


def _require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MatrixError(f"{label} must be an object")
    return value


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise MatrixError(f"{label} must be a non-empty-string array")
    return value


def _installed_mode_declarations(installed: Mapping[str, Any]) -> dict[str, list[str]]:
    skill_packages = _require_dict(installed.get("skill_packages"), "skill_packages")
    package_rows = skill_packages.get("files")
    if not isinstance(package_rows, list) or not package_rows:
        raise MatrixError("installed skill package file inventory is empty")
    package_modes = _sorted_strings(
        f"{row.get('path')}:{1 if row.get('executable') else 0}"
        for row in package_rows
        if isinstance(row, dict)
        and isinstance(row.get("path"), str)
        and isinstance(row.get("executable"), bool)
    )
    if len(package_modes) != len(package_rows):
        raise MatrixError("installed skill package mode inventory is incomplete")

    overlays = _require_dict(installed.get("overlays"), "overlays")
    overlay_rows = overlays.get("files")
    if not isinstance(overlay_rows, list) or not overlay_rows:
        raise MatrixError("installed overlay file inventory is empty")
    overlay_modes = _sorted_strings(
        f"{row.get('path')}:{1 if row.get('executable') else 0}"
        for row in overlay_rows
        if isinstance(row, dict)
        and isinstance(row.get("path"), str)
        and isinstance(row.get("executable"), bool)
    )
    if len(overlay_modes) != len(overlay_rows):
        raise MatrixError("installed overlay mode inventory is incomplete")

    install = _require_dict(installed.get("install"), "install")
    managed_assets = _require_string_list(
        install.get("managed_assets"), "install.managed_assets"
    )
    managed_modes = _sorted_strings(
        f"{relative}:{1 if _managed_asset_executable(relative) else 0}"
        for relative in managed_assets
    )
    return {
        "skill_package_files_and_modes": package_modes,
        "overlay_files_and_modes": overlay_modes,
        "managed_asset_files_and_modes": managed_modes,
    }
