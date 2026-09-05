#!/usr/bin/env python3
"""Run and validate the live-manifest-derived Trellis compatibility matrix.

The matrix runner deliberately keeps semantic release judgment outside this
module.  It executes the six deterministic platform/scenario cells and emits a
compact capability projection that the owning AI can review for migration
losses.  Full command logs and temporary checkout paths stay below the caller's
explicit work root and never become repository artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


SCHEMA_VERSION = "1.0"
SCENARIOS = ("clean", "existing")
SHARED_PLATFORM = "shared"
PLATFORM_ROOTS = {
    "claude": Path(".claude/skills"),
    "codex": Path(".codex/skills"),
    "cursor": Path(".cursor/skills"),
}
PLATFORM_INIT_FLAGS = {
    "claude": "--claude",
    "codex": "--codex",
    "cursor": "--cursor",
}
PLATFORM_PATH_RE = re.compile(r"^\.(claude|codex|cursor)/")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
VERSION_RE = re.compile(r"(?<![0-9])([0-9]+\.[0-9]+\.[0-9]+)(?![0-9])")
SIDECAR_SUFFIXES = (".new", ".bak")
DEFAULT_BEFORE_TAG = "v0.6.5-guru.10"
DEFAULT_BEFORE_CLI = "0.6.5"
DEFAULT_TARGET_CLI = "0.6.15"
DEFAULT_PACKAGE = "@mindfoldhq/trellis"
FAILURE_TAIL_LIMIT = 2000
FAILURE_STAGES = {"pre-matrix", "matrix-cell", "post-matrix"}
DEFAULT_COMMAND_TIMEOUT_SECONDS = 600.0


class MatrixError(RuntimeError):
    """A deterministic matrix precondition or cell check failed."""

    def __init__(
        self,
        message: str,
        *,
        stage: str = "pre-matrix",
        cell_id: str | None = None,
        command_label: str = "matrix-validation",
        exit_code: int = 2,
        error_tail: str | None = None,
    ) -> None:
        super().__init__(message)
        self.stage = stage
        self.cell_id = cell_id
        self.command_label = command_label
        self.exit_code = exit_code
        self.error_tail = error_tail if error_tail is not None else message

    def with_context(self, stage: str, cell_id: str | None) -> "MatrixError":
        return MatrixError(
            str(self),
            stage=stage,
            cell_id=cell_id,
            command_label=self.command_label,
            exit_code=self.exit_code,
            error_tail=self.error_tail,
        )


def command_timeout_seconds() -> float:
    raw = os.environ.get("GURU_MATRIX_COMMAND_TIMEOUT_SECONDS", "")
    if not raw:
        return DEFAULT_COMMAND_TIMEOUT_SECONDS
    try:
        value = float(raw)
    except ValueError:
        return DEFAULT_COMMAND_TIMEOUT_SECONDS
    return value if value > 0 else DEFAULT_COMMAND_TIMEOUT_SECONDS


def _sanitize_failure_tail(value: str) -> str:
    text = value.replace("\x00", "")
    text = re.sub(
        r"(?is)-----BEGIN [^-\r\n]*PRIVATE KEY-----.*?(?:-----END [^-\r\n]*PRIVATE KEY-----|$)",
        "<redacted-private-key>",
        text,
    )
    text = re.sub(r"(?i)(https?://)[^/\s@]+@", r"\1<redacted>@", text)
    text = re.sub(
        r"(?i)(github_pat_|ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9_]+",
        "<redacted-token>",
        text,
    )
    text = re.sub(
        r"(?i)(x-access-token:)[^@\s]+",
        r"\1<redacted>",
        text,
    )
    text = re.sub(
        r"(?i)(authorization:\s*(?:bearer|basic)\s+)[^\s]+",
        r"\1<redacted>",
        text,
    )
    text = re.sub(
        r"(?i)(\b[A-Z0-9_]*(?:TOKEN|PASSWORD|SECRET|API[_-]?KEY|ACCESS[_-]?KEY)[A-Z0-9_]*\b\s*[=:]\s*)[^\s&]+",
        r"\1<redacted>",
        text,
    )
    text = re.sub(
        r"(?i)([?&](?:token|access_token|api[_-]?key|awsaccesskeyid|x-amz-(?:credential|signature)|x-goog-(?:credential|signature))=)[^&\s]+",
        r"\1<redacted>",
        text,
    )
    return text[-FAILURE_TAIL_LIMIT:]


def _stable_command_label(argv: Sequence[str]) -> str:
    executable = Path(str(argv[0])).name if argv else "unknown-command"
    if (executable.startswith("python") or executable == "resolve-python.sh") and len(argv) > 1:
        for value in argv[1:]:
            candidate = Path(str(value)).name
            if candidate.endswith((".py", ".sh")):
                return candidate
    return executable


def matrix_failure_payload(exc: MatrixError) -> dict[str, Any]:
    stage = exc.stage if exc.stage in FAILURE_STAGES else "pre-matrix"
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "failed",
        "failure": {
            "kind": "matrix_failure",
            "stage": stage,
            "cell_id": exc.cell_id if stage == "matrix-cell" else None,
            "command_label": exc.command_label,
            "exit_code": exc.exit_code,
            "error_tail": _sanitize_failure_tail(exc.error_tail),
        },
    }


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MatrixError(f"cannot read JSON {path}: {exc}") from exc


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


def _platforms_from_paths(values: Iterable[str]) -> set[str]:
    platforms: set[str] = set()
    for value in values:
        matched = PLATFORM_PATH_RE.match(value)
        if matched:
            platforms.add(matched.group(1))
    return platforms


def _active_registry_rows_from(skill_root: Path) -> list[dict[str, Any]]:
    registry = _require_dict(
        _load_json(skill_root / "registry.json"),
        "skill registry",
    )
    skills = registry.get("skills")
    if not isinstance(skills, list):
        raise MatrixError("skill registry skills must be an array")
    rows: list[dict[str, Any]] = []
    for index, raw in enumerate(skills):
        row = _require_dict(raw, f"skill registry row {index}")
        if row.get("state") == "active":
            rows.append(row)
    if not rows:
        raise MatrixError("skill registry contains no active rows")
    return rows


def _active_registry_rows(repo_root: Path) -> list[dict[str, Any]]:
    return _active_registry_rows_from(repo_root / "trellis/skills/guru-team")


def derive_platform_inventory(repo_root: Path) -> dict[str, Any]:
    """Cross-check every live platform authority and return one closed set."""

    canonical = _require_dict(
        _load_json(repo_root / "trellis/guru-team-extension.json"),
        "canonical extension manifest",
    )
    public_api = _require_dict(canonical.get("public_api"), "public_api")
    manifest_paths = _require_string_list(
        public_api.get("managed_paths"), "public_api.managed_paths"
    )

    ownership = _require_dict(
        _load_json(
            repo_root
            / "trellis/presets/guru-team/ownership/upstream-ownership.json"
        ),
        "upstream ownership",
    )
    claims = ownership.get("managed_path_claims")
    if not isinstance(claims, list):
        raise MatrixError("managed_path_claims must be an array")
    ownership_paths = [
        str(_require_dict(row, "managed_path_claim").get("path", ""))
        for row in claims
    ]

    registry_rows = _active_registry_rows(repo_root)
    registry_sets: dict[str, list[str]] = {}
    interface_sets: dict[str, list[str]] = {}
    for row in registry_rows:
        skill_id = row.get("id")
        if not isinstance(skill_id, str) or not skill_id:
            raise MatrixError("active skill row has no id")
        supported = set(
            _require_string_list(
                row.get("supported_platforms"),
                f"registry {skill_id}.supported_platforms",
            )
        )
        supported.discard(SHARED_PLATFORM)
        registry_sets[skill_id] = _sorted_strings(supported)

        interface_path = row.get("interface")
        if not isinstance(interface_path, str) or not interface_path:
            raise MatrixError(f"registry {skill_id} has no interface path")
        interface = _require_dict(
            _load_json(repo_root / "trellis/skills/guru-team" / interface_path),
            f"interface {skill_id}",
        )
        destinations = set(
            _require_string_list(
                interface.get("platform_destinations"),
                f"interface {skill_id}.platform_destinations",
            )
        )
        destinations.discard(SHARED_PLATFORM)
        interface_sets[skill_id] = _sorted_strings(destinations)
        if registry_sets[skill_id] != interface_sets[skill_id]:
            raise MatrixError(
                f"platform declaration drift for {skill_id}: "
                f"registry={registry_sets[skill_id]} "
                f"interface={interface_sets[skill_id]}"
            )

    overlay_root = repo_root / "trellis/presets/guru-team/overlays"
    overlay_platforms = {
        item.name.removeprefix(".")
        for item in overlay_root.iterdir()
        if item.is_dir() and item.name.removeprefix(".") in PLATFORM_ROOTS
    }

    installed_path = repo_root / ".trellis/guru-team/extension.json"
    installed = _require_dict(_load_json(installed_path), "installed manifest")
    installed_sets = {
        "install": _sorted_strings(
            _require_string_list(
                _require_dict(installed.get("install"), "installed install").get(
                    "selected_platforms"
                ),
                "installed install.selected_platforms",
            )
        ),
        "skill_packages": _sorted_strings(
            _require_string_list(
                _require_dict(
                    installed.get("skill_packages"), "installed skill_packages"
                ).get("selected_platforms"),
                "installed skill_packages.selected_platforms",
            )
        ),
        "overlays": _sorted_strings(
            _require_string_list(
                _require_dict(installed.get("overlays"), "installed overlays").get(
                    "selected_platforms"
                ),
                "installed overlays.selected_platforms",
            )
        ),
    }

    authorities: dict[str, list[str]] = {
        "canonical_manifest": _sorted_strings(_platforms_from_paths(manifest_paths)),
        "upstream_ownership": _sorted_strings(_platforms_from_paths(ownership_paths)),
        "overlay_tree": _sorted_strings(overlay_platforms),
        "installed_install": installed_sets["install"],
        "installed_skill_packages": installed_sets["skill_packages"],
        "installed_overlays": installed_sets["overlays"],
    }
    authorities.update(
        {f"registry:{skill_id}": value for skill_id, value in registry_sets.items()}
    )
    authorities.update(
        {f"interface:{skill_id}": value for skill_id, value in interface_sets.items()}
    )

    distinct = {tuple(platforms) for platforms in authorities.values()}
    if len(distinct) != 1:
        raise MatrixError(
            "live platform authorities disagree: "
            + json.dumps(authorities, ensure_ascii=False, sort_keys=True)
        )
    platforms = next(iter(distinct))
    if not platforms or any(platform not in PLATFORM_ROOTS for platform in platforms):
        raise MatrixError(f"unsupported or empty live platform set: {platforms}")

    result = {
        "schema_version": SCHEMA_VERSION,
        "platforms": list(platforms),
        "authorities": authorities,
    }
    result["identity_sha256"] = _digest(result)
    return result


def build_matrix(repo_root: Path) -> dict[str, Any]:
    inventory = derive_platform_inventory(repo_root)
    cells = [
        {
            "cell_id": f"{platform}-{scenario}",
            "platform": platform,
            "scenario": scenario,
            "shared_projection": True,
        }
        for platform in inventory["platforms"]
        for scenario in SCENARIOS
    ]
    result = {
        "schema_version": SCHEMA_VERSION,
        "platform_inventory_sha256": inventory["identity_sha256"],
        "platforms": inventory["platforms"],
        "cell_count": len(cells),
        "cells": cells,
    }
    result["matrix_sha256"] = _digest(result)
    return result


def _workflow_markers(workflow_path: Path) -> dict[str, list[str]]:
    text = workflow_path.read_text(encoding="utf-8")
    marker_pattern = re.compile(
        r"<!--\s+(guru-(?:skill-invoke|skill-exit|workflow-target|stop-target)):\s*"
        r"(\{.*?\})\s*-->",
    )
    groups: dict[str, list[str]] = {
        "skill_invokes": [],
        "skill_exits": [],
        "workflow_targets": [],
        "stop_targets": [],
    }
    mapping = {
        "guru-skill-invoke": "skill_invokes",
        "guru-skill-exit": "skill_exits",
        "guru-workflow-target": "workflow_targets",
        "guru-stop-target": "stop_targets",
    }
    for kind, raw in marker_pattern.findall(text):
        try:
            marker = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise MatrixError(f"invalid workflow marker {raw}: {exc}") from exc
        groups[mapping[kind]].append(
            json.dumps(marker, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        )
    return {key: _sorted_strings(values) for key, values in groups.items()}


def _interface_projection_from(
    skill_root: Path, row: Mapping[str, Any]
) -> dict[str, Any]:
    skill_id = str(row["id"])
    interface_path = str(row["interface"])
    interface = _require_dict(
        _load_json(skill_root / interface_path),
        f"interface {skill_id}",
    )
    public = _require_dict(interface.get("public_contracts"), f"{skill_id}.public")

    def schema_ids(values: Any) -> list[str]:
        if not isinstance(values, list):
            return []
        ids: list[str] = []
        for value in values:
            if not isinstance(value, dict):
                continue
            schema = value.get("schema")
            if isinstance(schema, dict) and isinstance(schema.get("schema_id"), str):
                ids.append(schema["schema_id"])
        return _sorted_strings(ids)

    outputs = public.get("outputs") if isinstance(public.get("outputs"), list) else []
    consumers = (
        public.get("consumer_inputs")
        if isinstance(public.get("consumer_inputs"), list)
        else []
    )
    return {
        "id": skill_id,
        "interface_schema_id": row.get("interface_schema_id"),
        "judgment_mode": interface.get("judgment_mode"),
        "workflow_route_id": row.get("workflow_route_id"),
        "platform_destinations": _sorted_strings(
            _require_string_list(
                interface.get("platform_destinations"),
                f"{skill_id}.platform_destinations",
            )
        ),
        "input_kind": _require_dict(public.get("input"), f"{skill_id}.input").get(
            "kind"
        ),
        "invocation_command": _require_dict(
            public.get("invocation"), f"{skill_id}.invocation"
        ).get("command_id"),
        "external_exits": _sorted_strings(
            str(value.get("exit_id"))
            for value in outputs
            if isinstance(value, dict) and isinstance(value.get("exit_id"), str)
        ),
        "public_output_schema_ids": schema_ids(outputs),
        "private_schema_ids": schema_ids(public.get("private_artifacts")),
        "consumers": _sorted_strings(
            json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            for value in consumers
            if isinstance(value, dict)
        ),
    }


def _interface_projection(repo_root: Path, row: Mapping[str, Any]) -> dict[str, Any]:
    return _interface_projection_from(repo_root / "trellis/skills/guru-team", row)


def capability_projection(repo_root: Path) -> dict[str, Any]:
    """Build a compact complete projection from current canonical authorities."""

    canonical = _require_dict(
        _load_json(repo_root / "trellis/guru-team-extension.json"),
        "canonical extension manifest",
    )
    public_api = _require_dict(canonical.get("public_api"), "public_api")
    ownership = _require_dict(
        _load_json(
            repo_root
            / "trellis/presets/guru-team/ownership/upstream-ownership.json"
        ),
        "upstream ownership",
    )
    rows = _active_registry_rows(repo_root)
    interfaces = [_interface_projection(repo_root, row) for row in rows]
    platform_inventory = derive_platform_inventory(repo_root)
    installed_manifest = _require_dict(
        _load_json(repo_root / ".trellis/guru-team/extension.json"),
        "source dogfood installed manifest",
    )
    mode_declarations = _installed_mode_declarations(installed_manifest)

    commands: list[str] = []
    companion = public_api.get("companion_scripts")
    if isinstance(companion, list):
        for row in companion:
            if isinstance(row, dict) and isinstance(row.get("id"), str):
                commands.append(row["id"])
            elif isinstance(row, str):
                commands.append(row)
    elif isinstance(companion, dict):
        commands.extend(str(key) for key in companion)

    overlay_files = []
    overlay_root = repo_root / "trellis/presets/guru-team/overlays"
    for path in sorted(item for item in overlay_root.rglob("*") if item.is_file()):
        executable = _executable_projection(path)
        overlay_files.append(
            f"{path.relative_to(repo_root).as_posix()}:{executable}"
        )

    docs_locators: list[str] = []
    for relative in (
        "docs/requirements/README.md",
        "docs/design/README.md",
        "docs/test/README.md",
        "docs/architecture/README.md",
        ".trellis/spec/docs/requirements-design-test-ssot.md",
        ".trellis/spec/architecture/baseline-usage.md",
    ):
        path = repo_root / relative
        if not path.is_file():
            raise MatrixError(f"missing Docs authority locator {relative}")
        docs_locators.append(relative)

    projection: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "extension": {
            "extension_id": canonical.get("extension_id"),
            "version": canonical.get("version"),
            "target_trellis_cli": canonical.get("target_trellis_cli"),
            "requires_trellis_cli": _require_dict(
                canonical.get("requires"), "requires"
            ).get("trellis_cli"),
            "tested_trellis_cli": _sorted_strings(
                _require_string_list(
                    _require_dict(canonical.get("tested"), "tested").get(
                        "trellis_cli"
                    ),
                    "tested.trellis_cli",
                )
            ),
        },
        "distribution": {
            "platforms": platform_inventory["platforms"],
            "managed_paths": _sorted_strings(
                _require_string_list(
                    public_api.get("managed_paths"), "public_api.managed_paths"
                )
            ),
            "artifact_contracts": _sorted_strings(
                _require_string_list(
                    public_api.get("artifact_contracts"),
                    "public_api.artifact_contracts",
                )
            ),
            "ownership_rules": _sorted_strings(
                json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                for row in ownership.get("guru_owned_rules", [])
                if isinstance(row, dict)
            ),
            "managed_claims": _sorted_strings(
                json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                for row in ownership.get("managed_path_claims", [])
                if isinstance(row, dict)
            ),
            "overlay_files_and_modes": mode_declarations[
                "overlay_files_and_modes"
            ],
            "skill_package_files_and_modes": mode_declarations[
                "skill_package_files_and_modes"
            ],
            "managed_asset_files_and_modes": mode_declarations[
                "managed_asset_files_and_modes"
            ],
            "canonical_overlay_files_and_modes": overlay_files,
        },
        "skill_api": {
            "interfaces": interfaces,
            "public_input_schema_ids": _sorted_strings(
                _require_string_list(
                    _require_dict(
                        public_api.get("skill_contracts"), "skill_contracts"
                    ).get("public_input_schema_ids"),
                    "skill_contracts.public_input_schema_ids",
                )
            ),
            "typed_output_schema_ids": _sorted_strings(
                _require_string_list(
                    _require_dict(
                        public_api.get("skill_contracts"), "skill_contracts"
                    ).get("typed_output_schema_ids"),
                    "skill_contracts.typed_output_schema_ids",
                )
            ),
            "private_artifact_schema_ids": _sorted_strings(
                _require_string_list(
                    _require_dict(
                        public_api.get("skill_contracts"), "skill_contracts"
                    ).get("private_artifact_schema_ids"),
                    "skill_contracts.private_artifact_schema_ids",
                )
            ),
            "commands": _sorted_strings(commands),
        },
        "workflow": _workflow_markers(
            repo_root / "trellis/workflows/guru-team/workflow.md"
        ),
        "task_data": {
            "artifact_contracts": _sorted_strings(
                _require_string_list(
                    public_api.get("artifact_contracts"),
                    "public_api.artifact_contracts",
                )
            ),
            "route_ids": _sorted_strings(
                str(row.get("workflow_route_id"))
                for row in rows
                if isinstance(row.get("workflow_route_id"), str)
            ),
            "companion_commands": _sorted_strings(commands),
        },
        "docs_authority": {"locators": docs_locators},
    }
    projection["projection_sha256"] = _digest(projection)
    return projection


def installed_capability_projection(target: Path) -> dict[str, Any]:
    """Project the same semantic groups from one installed matrix cell."""

    installed = _require_dict(
        _load_json(target / ".trellis/guru-team/extension.json"),
        "installed manifest",
    )
    extension = _require_dict(installed.get("extension"), "installed extension")
    public_api = _require_dict(extension.get("public_api"), "installed public_api")
    skill_root = target / ".trellis/guru-team/skills"
    rows = _active_registry_rows_from(skill_root)
    interfaces = [_interface_projection_from(skill_root, row) for row in rows]
    selected_sets = []
    for section in ("install", "skill_packages", "overlays"):
        selected_sets.append(
            _sorted_strings(
                _require_string_list(
                    _require_dict(installed.get(section), f"installed {section}").get(
                        "selected_platforms"
                    ),
                    f"installed {section}.selected_platforms",
                )
            )
        )
    if not selected_sets[0] or any(value != selected_sets[0] for value in selected_sets[1:]):
        raise MatrixError(f"installed platform declaration drift: {selected_sets}")

    commands = public_api.get("companion_scripts")
    command_ids = (
        _sorted_strings(str(value) for value in commands)
        if isinstance(commands, list)
        else _sorted_strings(str(value) for value in commands)
        if isinstance(commands, dict)
        else []
    )
    overlays = _require_dict(installed.get("overlays"), "installed overlays")
    mode_declarations = _installed_mode_declarations(installed)
    overlay_files = _sorted_strings(
        f"{row.get('source')}:{1 if row.get('executable') else 0}"
        for row in overlays.get("files", [])
        if isinstance(row, dict)
        and isinstance(row.get("source"), str)
        and isinstance(row.get("executable"), bool)
    )
    docs_locators = []
    for relative in (
        "docs/requirements/README.md",
        "docs/design/README.md",
        "docs/test/README.md",
        "docs/architecture/README.md",
        ".trellis/spec/docs/requirements-design-test-ssot.md",
        ".trellis/spec/architecture/baseline-usage.md",
    ):
        if (target / relative).is_file():
            docs_locators.append(relative)

    skill_contracts = _require_dict(
        public_api.get("skill_contracts"), "installed skill_contracts"
    )
    projection: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "extension": {
            "extension_id": extension.get("extension_id"),
            "version": extension.get("version"),
            "target_trellis_cli": extension.get("target_trellis_cli"),
            "requires_trellis_cli": _require_dict(
                extension.get("requires"), "installed requires"
            ).get("trellis_cli"),
            "tested_trellis_cli": _sorted_strings(
                _require_string_list(
                    _require_dict(extension.get("tested"), "installed tested").get(
                        "trellis_cli"
                    ),
                    "installed tested.trellis_cli",
                )
            ),
        },
        "distribution": {
            "platforms": selected_sets[0],
            "managed_paths": _sorted_strings(
                _require_string_list(
                    public_api.get("managed_paths"), "installed managed_paths"
                )
            ),
            "artifact_contracts": _sorted_strings(
                _require_string_list(
                    public_api.get("artifact_contracts"),
                    "installed artifact_contracts",
                )
            ),
            "ownership_rules": [],
            "managed_claims": [],
            "overlay_files_and_modes": mode_declarations[
                "overlay_files_and_modes"
            ],
            "skill_package_files_and_modes": mode_declarations[
                "skill_package_files_and_modes"
            ],
            "managed_asset_files_and_modes": mode_declarations[
                "managed_asset_files_and_modes"
            ],
            "canonical_overlay_files_and_modes": overlay_files,
        },
        "skill_api": {
            "interfaces": interfaces,
            "public_input_schema_ids": _sorted_strings(
                _require_string_list(
                    skill_contracts.get("public_input_schema_ids"),
                    "installed public_input_schema_ids",
                )
            ),
            "typed_output_schema_ids": _sorted_strings(
                _require_string_list(
                    skill_contracts.get("typed_output_schema_ids"),
                    "installed typed_output_schema_ids",
                )
            ),
            "private_artifact_schema_ids": _sorted_strings(
                _require_string_list(
                    skill_contracts.get("private_artifact_schema_ids"),
                    "installed private_artifact_schema_ids",
                )
            ),
            "commands": command_ids,
        },
        "workflow": _workflow_markers(target / ".trellis/workflow.md"),
        "task_data": {
            "artifact_contracts": _sorted_strings(
                _require_string_list(
                    public_api.get("artifact_contracts"),
                    "installed artifact_contracts",
                )
            ),
            "route_ids": _sorted_strings(
                str(row.get("workflow_route_id"))
                for row in rows
                if isinstance(row.get("workflow_route_id"), str)
            ),
            "companion_commands": command_ids,
        },
        "docs_authority": {"locators": docs_locators},
    }
    projection["projection_sha256"] = _digest(projection)
    return projection


def compare_capabilities(before: Mapping[str, Any], after: Mapping[str, Any]) -> dict[str, Any]:
    """Compare observable capabilities while isolating versioned projections.

    Distribution inventories and Skill API/schema projections are implementation
    assets. Their consistency is checked independently by the install and
    package validators; they are not observable workflow capability markers.
    """

    version_fields = (
        "version",
        "target_trellis_cli",
        "requires_trellis_cli",
        "tested_trellis_cli",
    )
    before_extension = _require_dict(before.get("extension"), "before extension")
    after_extension = _require_dict(after.get("extension"), "after extension")
    version_binding = {
        "before": {field: before_extension.get(field) for field in version_fields},
        "after": {field: after_extension.get(field) for field in version_fields},
    }
    differences: list[dict[str, Any]] = []
    before_identity = {
        key: value for key, value in before_extension.items() if key not in version_fields
    }
    after_identity = {
        key: value for key, value in after_extension.items() if key not in version_fields
    }
    extension_identity = {
        "before": before_identity,
        "after": after_identity,
        "consistent": before_identity == after_identity,
    }
    for group in ("workflow", "task_data", "docs_authority"):
        if before.get(group) != after.get(group):
            differences.append(
                {"group": group, "before": before.get(group), "after": after.get(group)}
            )
    result = {
        "schema_version": SCHEMA_VERSION,
        "version_binding": version_binding,
        "extension_identity": extension_identity,
        "blocking_differences": differences,
        "capabilities_preserved": not differences,
    }
    result["comparison_sha256"] = _digest(result)
    return result


def _assert_projection_consistency(
    comparison: Mapping[str, Any], projection_name: str
) -> None:
    if not comparison.get("capabilities_preserved"):
        raise MatrixError(
            f"{projection_name} capability projection changed outside version binding: "
            + json.dumps(comparison.get("blocking_differences"), ensure_ascii=False)
        )
    extension_identity = _require_dict(
        comparison.get("extension_identity"),
        f"{projection_name} extension identity",
    )
    if extension_identity.get("consistent") is not True:
        raise MatrixError(
            f"{projection_name} extension identity changed: "
            + json.dumps(extension_identity, ensure_ascii=False)
        )


def _run(
    argv: Sequence[str],
    *,
    cwd: Path | None = None,
    env: Mapping[str, str] | None = None,
    log: Path | None = None,
    capture: bool = False,
    input_text: str | None = None,
) -> str:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    timeout = command_timeout_seconds()
    try:
        completed = subprocess.run(
            list(argv),
            cwd=str(cwd) if cwd else None,
            env=merged_env,
            text=True,
            input=input_text,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.output or ""
        raise MatrixError(
            f"command timed out after {timeout:.3f}s: {_stable_command_label(argv)}",
            command_label=_stable_command_label(argv),
            exit_code=124,
            error_tail=(
                f"command timed out after {timeout:.3f}s\n"
                f"stdout:\n{output}"
            ),
        ) from exc
    output = completed.stdout or ""
    if log:
        log.write_text(output, encoding="utf-8")
    if completed.returncode != 0:
        raise MatrixError(
            f"command failed ({completed.returncode}): {_stable_command_label(argv)}",
            command_label=_stable_command_label(argv),
            exit_code=completed.returncode,
            error_tail=output,
        )
    return output if capture else ""


def _git(repo: Path, *args: str, capture: bool = True) -> str:
    return _run(("git", "-C", str(repo), *args), capture=capture).strip()


def _before_tag_ref(repo_root: Path, before_tag: str) -> tuple[str, str]:
    """Return one exact tag name/ref without accepting revision expressions."""

    tag_name = before_tag.strip()
    if not tag_name or tag_name != before_tag or tag_name.startswith("refs/"):
        raise MatrixError(
            "before tag must be one exact tag name",
            command_label="git",
        )
    tag_ref = f"refs/tags/{tag_name}"
    checked = subprocess.run(
        ("git", "-C", str(repo_root), "check-ref-format", tag_ref),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if checked.returncode != 0:
        raise MatrixError(
            f"invalid before tag name: {tag_name}",
            command_label="git",
            exit_code=checked.returncode or 2,
            error_tail=checked.stdout or f"invalid before tag name: {tag_name}",
        )
    return tag_name, tag_ref


def _local_before_tag_identity(
    repo_root: Path,
    tag_ref: str,
) -> tuple[str | None, str | None, str]:
    """Resolve the exact tag ref and its peeled commit without raising."""

    outputs: list[str] = []
    values: list[str | None] = []
    for revision in (tag_ref, f"{tag_ref}^{{commit}}"):
        resolved = subprocess.run(
            ("git", "-C", str(repo_root), "rev-parse", "--verify", revision),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        output = resolved.stdout or ""
        outputs.append(output)
        oid = output.strip()
        values.append(
            oid
            if resolved.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}", oid)
            else None
        )
    return values[0], values[1], "".join(outputs)


def _local_before_tag_ref_exists(repo_root: Path, tag_ref: str) -> bool:
    """Return whether one exact local tag ref exists."""

    resolved = subprocess.run(
        (
            "git",
            "-C",
            str(repo_root),
            "show-ref",
            "--verify",
            "--quiet",
            tag_ref,
        ),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if resolved.returncode == 0:
        return True
    if resolved.returncode == 1:
        return False
    raise MatrixError(
        f"failed to inspect local before tag ref: {tag_ref}",
        command_label="git",
        exit_code=resolved.returncode or 2,
        error_tail=resolved.stdout
        or f"failed to inspect local before tag ref: {tag_ref}",
    )


def resolve_before_tag(repo_root: Path, before_tag: str) -> dict[str, Any]:
    """Resolve one local before tag, fetching only that exact tag when absent."""

    tag_name, tag_ref = _before_tag_ref(repo_root, before_tag)
    local_ref_exists = _local_before_tag_ref_exists(repo_root, tag_ref)
    tag_object, commit, resolution_tail = _local_before_tag_identity(
        repo_root,
        tag_ref,
    )
    if local_ref_exists:
        if tag_object is None or commit is None:
            raise MatrixError(
                f"local before tag is not a resolvable commit: {tag_ref}",
                command_label="git",
                error_tail=resolution_tail
                or f"local before tag is not a resolvable commit: {tag_ref}",
            )
        return {
            "before_tag": tag_name,
            "before_tag_object": tag_object,
            "before_commit": commit,
            "fetch_performed": False,
        }

    _run(
        (
            "git",
            "fetch",
            "--no-tags",
            "--depth=1",
            "origin",
            f"{tag_ref}:{tag_ref}",
        ),
        cwd=repo_root,
        capture=True,
    )
    tag_object, commit, resolution_tail = _local_before_tag_identity(
        repo_root,
        tag_ref,
    )
    if tag_object is None or commit is None:
        raise MatrixError(
            f"before tag remains unavailable after exact fetch: {tag_ref}",
            command_label="git",
            error_tail=resolution_tail
            or f"before tag remains unavailable after exact fetch: {tag_ref}",
        )
    return {
        "before_tag": tag_name,
        "before_tag_object": tag_object,
        "before_commit": commit,
        "fetch_performed": True,
    }


def source_state(repo_root: Path) -> dict[str, Any]:
    """Bind one HEAD plus the exact tracked and untracked candidate delta."""

    head = _git(repo_root, "rev-parse", "HEAD")
    tracked = subprocess.run(
        ("git", "-C", str(repo_root), "diff", "--binary", "HEAD", "--"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if tracked.returncode != 0:
        raise MatrixError(
            "cannot capture source tracked delta: "
            + tracked.stderr.decode("utf-8", errors="replace")
        )
    untracked = subprocess.run(
        (
            "git",
            "-C",
            str(repo_root),
            "ls-files",
            "--others",
            "--exclude-standard",
            "-z",
        ),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if untracked.returncode != 0:
        raise MatrixError(
            "cannot capture source untracked paths: "
            + untracked.stderr.decode("utf-8", errors="replace")
        )
    untracked_rows: list[dict[str, Any]] = []
    for raw in (item for item in untracked.stdout.split(b"\0") if item):
        relative = raw.decode("utf-8")
        path = repo_root / relative
        if path.is_symlink():
            content = os.readlink(path).encode("utf-8")
            mode = "120000"
        elif path.is_file():
            content = path.read_bytes()
            mode = "100755" if _executable_projection(path) else "100644"
        else:
            raise MatrixError(f"unsupported untracked source entry: {relative}")
        untracked_rows.append(
            {
                "path": relative,
                "mode": mode,
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    with tempfile.TemporaryDirectory(prefix="guru-matrix-source-index-") as directory:
        index_path = Path(directory) / "index"
        index_env = {**os.environ, "GIT_INDEX_FILE": str(index_path)}
        for argv in (
            ("git", "-C", str(repo_root), "read-tree", "HEAD"),
            ("git", "-C", str(repo_root), "add", "-A", "--", "."),
        ):
            completed = subprocess.run(
                argv,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=index_env,
                check=False,
            )
            if completed.returncode != 0:
                raise MatrixError(
                    "cannot build source candidate tree: "
                    + completed.stderr.decode("utf-8", errors="replace")
                )
        written = subprocess.run(
            ("git", "-C", str(repo_root), "write-tree"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=index_env,
            check=False,
        )
        if written.returncode != 0:
            raise MatrixError(
                "cannot write source candidate tree: "
                + written.stderr.decode("utf-8", errors="replace")
            )
        candidate_tree = written.stdout.decode("ascii").strip()
    state: dict[str, Any] = {
        "head": head,
        "candidate_tree": candidate_tree,
        "tracked_delta_sha256": hashlib.sha256(tracked.stdout).hexdigest(),
        "untracked_files": sorted(
            untracked_rows, key=lambda row: str(row["path"]).encode("utf-8")
        ),
        "dirty": bool(tracked.stdout or untracked_rows),
    }
    state["identity_sha256"] = _digest(state)
    return state


def _parse_cli_version(output: str) -> str:
    matched = VERSION_RE.search(output)
    if not matched:
        raise MatrixError(f"cannot parse Trellis CLI version from: {output!r}")
    return matched.group(1)


def _install_cli(prefix: Path, version: str, log: Path) -> tuple[Path, dict[str, str]]:
    prefix.mkdir(parents=True)
    env = {"npm_config_prefix": str(prefix)}
    _run(
        ("npm", "install", "-g", f"{DEFAULT_PACKAGE}@{version}"),
        env=env,
        log=log,
    )
    binary = prefix / "bin/trellis"
    if not binary.is_file() or not os.access(binary, os.X_OK):
        raise MatrixError(f"isolated Trellis CLI is unavailable: {binary}")
    child_env = {
        "npm_config_prefix": str(prefix),
        "PATH": f"{prefix / 'bin'}:{os.environ.get('PATH', '')}",
        "TRELLIS_PYTHON_CMD": "python3",
    }
    return binary, child_env


def _assert_version(binary: Path, expected: str, env: Mapping[str, str]) -> str:
    actual = _parse_cli_version(_run((str(binary), "--version"), env=env, capture=True))
    if actual != expected:
        raise MatrixError(f"Trellis CLI version mismatch: expected {expected}, got {actual}")
    return actual


def _init_git_repo(target: Path) -> None:
    target.mkdir(parents=True)
    _run(("git", "init", "-q"), cwd=target)
    _run(("git", "config", "user.name", "Guru Team Compatibility Matrix"), cwd=target)
    _run(
        ("git", "config", "user.email", "guru-team-matrix@example.invalid"), cwd=target
    )
    _run(("git", "branch", "-M", "main"), cwd=target)
    (target / ".throwaway-baseline").write_text("compatibility matrix baseline\n")
    for domain in ("requirements", "design", "test", "architecture"):
        readme = target / "docs" / domain / "README.md"
        readme.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text(
            f"# Matrix {domain.title()} Authority\n\n"
            f"This exact business-owned {domain} authority must survive install and update.\n",
            encoding="utf-8",
        )
        versioned = (
            target
            / "docs"
            / domain
            / "versions"
            / "current-business"
            / "authority.md"
        )
        versioned.parent.mkdir(parents=True, exist_ok=True)
        versioned.write_text(
            f"# Current {domain.title()} Body\n\n"
            f"This versioned business-owned {domain} body must survive install and update.\n",
            encoding="utf-8",
        )
    _run(("git", "add", ".throwaway-baseline", "docs"), cwd=target)
    _run(("git", "commit", "-q", "-m", "chore: initialize compatibility cell"), cwd=target)


def _export_git_tree(repo_root: Path, ref: str, destination: Path, archive: Path) -> None:
    with archive.open("wb") as stream:
        completed = subprocess.run(
            ("git", "-C", str(repo_root), "archive", "--format=tar", ref),
            stdout=stream,
            stderr=subprocess.PIPE,
            check=False,
        )
    if completed.returncode != 0:
        raise MatrixError(
            f"cannot export {ref}: {completed.stderr.decode('utf-8', errors='replace')}"
        )
    destination.mkdir(parents=True)
    with tarfile.open(archive) as bundle:
        bundle.extractall(destination)


def _apply_preset(
    source_root: Path,
    target: Path,
    platform: str,
    log: Path,
    *,
    previous_root: Path | None = None,
) -> dict[str, Any]:
    argv = (
        sys.executable,
        str(
            source_root
            / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"
        ),
        "--repo",
        str(target),
        "--platform",
        platform,
    )

    def invoke() -> tuple[int, str, dict[str, Any]]:
        completed = subprocess.run(
            argv,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        output = completed.stdout or ""
        try:
            payload = _require_dict(json.loads(output), "preset result")
        except (json.JSONDecodeError, MatrixError) as exc:
            raise MatrixError(
                f"preset returned invalid JSON: {output[-4000:]}",
                command_label=_stable_command_label(argv),
                exit_code=completed.returncode,
                error_tail=output,
            ) from exc
        return completed.returncode, output, payload

    returncode, output, payload = invoke()
    log.write_text(output, encoding="utf-8")
    if returncode == 0:
        if payload.get("status") != "ok" or _sidecars(target):
            raise MatrixError("preset success did not produce a sidecar-free ok result")
        return {"status": "passed", "reconciled_backups": []}
    if returncode != 2 or previous_root is None or payload.get("status") != "conflict":
        raise MatrixError(
            f"preset apply failed ({returncode}): {output[-4000:]}",
            command_label=_stable_command_label(argv),
            exit_code=returncode,
            error_tail=output,
        )

    skill_packages = _require_dict(
        payload.get("skill_packages"), "preset skill_packages"
    )
    overlays = _require_dict(payload.get("overlays"), "preset overlays")
    declared_sidecars = _sorted_strings(
        path
        for paths in (
            _require_string_list(payload.get("new_copies"), "preset new copies"),
            _require_string_list(
                payload.get("managed_backups"), "preset managed backups"
            ),
            _require_string_list(
                skill_packages.get("sidecars"), "preset skill package sidecars"
            ),
            _require_string_list(
                overlays.get("sidecars"), "preset overlay sidecars"
            ),
        )
        for path in paths
        if Path(path).suffix in SIDECAR_SUFFIXES
    )
    actual_sidecars = _sidecars(target)
    if declared_sidecars != actual_sidecars:
        raise MatrixError(
            "preset sidecar inventory does not match the installed repository"
        )

    reconciled: list[str] = []
    for relative in actual_sidecars:
        relative_path = Path(relative)
        if (
            relative_path.is_absolute()
            or ".." in relative_path.parts
            or relative_path.suffix != ".bak"
        ):
            raise MatrixError(f"unexpected preset migration sidecar: {relative}")
        current_relative = Path(relative.removesuffix(".bak"))
        backup = target / relative_path
        current = target / current_relative
        previous = previous_root / current_relative
        candidate = source_root / current_relative
        for label, path in (
            ("backup", backup),
            ("current", current),
            ("previous", previous),
            ("candidate", candidate),
        ):
            if path.is_symlink() or not path.is_file():
                raise MatrixError(
                    f"preset migration {label} is unavailable for {relative}"
                )
        if backup.read_bytes() != previous.read_bytes():
            raise MatrixError(
                f"preset backup is not the immutable before-state for {relative}"
            )
        if current.read_bytes() != candidate.read_bytes():
            raise MatrixError(
                f"preset current file is not the candidate projection for {relative}"
            )
        backup.unlink()
        reconciled.append(relative)

    returncode, second_output, second_payload = invoke()
    log.write_text(
        output + "\n--- reconciled known upgrade backups ---\n" + second_output,
        encoding="utf-8",
    )
    if (
        returncode != 0
        or second_payload.get("status") != "ok"
        or _sidecars(target)
    ):
        raise MatrixError(
            f"preset reapply did not converge after known backup migration: "
            f"{second_output[-4000:]}"
        )
    return {
        "status": "passed",
        "reconciled_backups": _sorted_strings(reconciled),
    }


def _workflow_source_requires_local_sample(repo_root: Path, workflow_source: str) -> bool:
    if workflow_source not in {
        "gh:castbox/guru-trellis/trellis",
        "gh:castbox/guru-trellis/trellis#main",
    }:
        return False
    current_branch = _git(repo_root, "branch", "--show-current")
    dirty = _git(
        repo_root,
        "status",
        "--short",
        "--",
        "trellis/index.json",
        "trellis/workflows/guru-team/workflow.md",
    )
    return current_branch != "main" or bool(dirty)


def _install_workflow(
    target: Path,
    binary: Path,
    env: Mapping[str, str],
    platform: str,
    workflow_source: str,
    repo_root: Path,
    allow_local_sample: bool,
    log: Path,
) -> bool:
    local_sample = _workflow_source_requires_local_sample(repo_root, workflow_source)
    if local_sample and not allow_local_sample:
        raise MatrixError(
            "candidate workflow is not addressable through the configured marketplace; "
            "push an exact ref or set TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 and "
            "report the unpublished local-sample boundary"
        )
    _run(
        (
            str(binary),
            "init",
            "-y",
            PLATFORM_INIT_FLAGS[platform],
            "--workflow",
            "guru-team",
            "--workflow-source",
            workflow_source,
        ),
        cwd=target,
        env=env,
        log=log,
    )
    if local_sample:
        shutil.copyfile(
            repo_root / "trellis/workflows/guru-team/workflow.md",
            target / ".trellis/workflow.md",
        )
    return local_sample


def _preview_and_switch_workflow(
    target: Path,
    binary: Path,
    env: Mapping[str, str],
    workflow_source: str,
    repo_root: Path,
    previous_source_root: Path,
    local_sample: bool,
    work_root: Path,
) -> None:
    workflow = target / ".trellis/workflow.md"
    sidecar = target / ".trellis/workflow.md.new"
    backup = target / ".trellis/workflow.md.bak"
    if (
        sidecar.exists()
        or sidecar.is_symlink()
        or backup.exists()
        or backup.is_symlink()
    ):
        raise MatrixError("workflow switch found an unresolved .new/.bak sidecar")
    if not workflow.is_file() or workflow.is_symlink():
        raise MatrixError("managed workflow is missing or not a regular file")
    previous_candidate = previous_source_root / "trellis/workflows/guru-team/workflow.md"
    if (
        not previous_candidate.is_file()
        or workflow.read_bytes() != previous_candidate.read_bytes()
    ):
        raise MatrixError("current workflow is not the expected managed before-candidate")
    managed_before = workflow.read_bytes()
    _run(
        (
            str(binary),
            "workflow",
            "--marketplace",
            workflow_source,
            "--template",
            "guru-team",
            "--create-new",
        ),
        cwd=target,
        env=env,
        log=work_root / "workflow-preview.log",
    )
    if not sidecar.is_file() or sidecar.is_symlink():
        raise MatrixError("workflow preview did not create .trellis/workflow.md.new")
    preview = sidecar.read_bytes()
    if not preview:
        raise MatrixError("workflow preview candidate is empty")
    if workflow.read_bytes() != managed_before:
        raise MatrixError("current workflow changed while validating the preview")
    if not local_sample:
        expected_candidate = repo_root / "trellis/workflows/guru-team/workflow.md"
        if (
            not expected_candidate.is_file()
            or preview != expected_candidate.read_bytes()
        ):
            raise MatrixError("workflow preview does not match the expected marketplace candidate")
    elif not any(_workflow_markers(sidecar).values()):
        raise MatrixError("workflow preview has no Guru Team workflow markers")
    sidecar.unlink()
    _run(
        (
            str(binary),
            "workflow",
            "--marketplace",
            workflow_source,
            "--template",
            "guru-team",
            "--force",
        ),
        cwd=target,
        env=env,
        log=work_root / "workflow-switch.log",
    )
    if workflow.read_bytes() != preview:
        raise MatrixError("active workflow does not match the validated preview candidate")
    if local_sample:
        shutil.copyfile(
            repo_root / "trellis/workflows/guru-team/workflow.md",
            workflow,
        )
        if workflow.read_bytes() != (
            repo_root / "trellis/workflows/guru-team/workflow.md"
        ).read_bytes():
            raise MatrixError("local candidate workflow reapply did not converge")
    if sidecar.exists() or backup.exists():
        raise MatrixError("workflow switch left an unresolved .new/.bak sidecar")


def _sidecars(target: Path) -> list[str]:
    return _sorted_strings(
        path.relative_to(target).as_posix()
        for path in target.rglob("*")
        if path.is_file() and path.suffix in SIDECAR_SUFFIXES
    )


def _assert_installed_file_modes(
    target: Path, installed: Mapping[str, Any], source_root: Path
) -> None:
    skill_packages = _require_dict(installed.get("skill_packages"), "skill_packages")
    files = skill_packages.get("files")
    if not isinstance(files, list) or not files:
        raise MatrixError("installed skill package file inventory is empty")
    for index, raw in enumerate(files):
        row = _require_dict(raw, f"skill_packages.files[{index}]")
        relative = row.get("path")
        executable = row.get("executable")
        if not isinstance(relative, str) or not isinstance(executable, bool):
            raise MatrixError(f"invalid installed file row {index}")
        path = target / relative
        if not path.is_file():
            raise MatrixError(f"missing installed managed file {relative}")
        actual = bool(path.stat().st_mode & stat.S_IXUSR)
        if actual is not executable:
            raise MatrixError(
                f"installed executable mode mismatch for {relative}: "
                f"expected {executable}, got {actual}"
            )
    overlays = _require_dict(installed.get("overlays"), "overlays")
    overlay_files = overlays.get("files")
    if not isinstance(overlay_files, list) or not overlay_files:
        raise MatrixError("installed overlay file inventory is empty")
    for index, raw in enumerate(overlay_files):
        row = _require_dict(raw, f"overlays.files[{index}]")
        relative = row.get("path")
        source = row.get("source")
        executable = row.get("executable")
        if (
            not isinstance(relative, str)
            or not isinstance(source, str)
            or not isinstance(executable, bool)
        ):
            raise MatrixError(f"invalid installed overlay row {index}")
        target_path = target / relative
        source_path = source_root / source
        if not target_path.is_file() or not source_path.is_file():
            raise MatrixError(f"missing overlay source/target for {relative}")
        if target_path.read_bytes() != source_path.read_bytes():
            raise MatrixError(f"overlay byte drift for {relative}")
        actual = bool(target_path.stat().st_mode & stat.S_IXUSR)
        if actual is not executable:
            raise MatrixError(f"overlay executable mode mismatch for {relative}")

    install = _require_dict(installed.get("install"), "install")
    managed_assets = _require_string_list(
        install.get("managed_assets"), "install.managed_assets"
    )
    managed_hashes = _require_dict(
        install.get("managed_asset_hashes"), "install.managed_asset_hashes"
    )
    if not set(managed_hashes).issubset(managed_assets):
        raise MatrixError("managed asset path/hash inventory mismatch")
    for relative in managed_assets:
        target_path = target / relative
        if not target_path.is_file():
            raise MatrixError(f"missing managed asset {relative}")
        if relative in managed_hashes:
            digest = hashlib.sha256(target_path.read_bytes()).hexdigest()
            if managed_hashes[relative] != digest:
                raise MatrixError(f"managed asset digest mismatch for {relative}")
        expected_executable = _managed_asset_executable(relative)
        target_executable = bool(target_path.stat().st_mode & stat.S_IXUSR)
        if target_executable is not expected_executable:
            raise MatrixError(f"managed asset mode drift for {relative}")


def _assert_platform_projection(target: Path, platform: str) -> None:
    shared_root = target / ".agents/skills"
    selected_root = target / PLATFORM_ROOTS[platform]
    if not shared_root.is_dir() or not selected_root.is_dir():
        raise MatrixError(f"missing shared or selected {platform} skill projection")
    shared_ids = {path.name for path in shared_root.glob("guru-*") if path.is_dir()}
    selected_ids = {path.name for path in selected_root.glob("guru-*") if path.is_dir()}
    if not shared_ids or shared_ids != selected_ids:
        raise MatrixError(
            f"shared/{platform} skill projection mismatch: "
            f"shared={sorted(shared_ids)} selected={sorted(selected_ids)}"
        )
    for root in (shared_root, selected_root):
        for skill_id in sorted(shared_ids):
            package = target / ".trellis/guru-team/skills/packages" / skill_id
            interface = _require_dict(
                _load_json(package / "interface.json"),
                f"{skill_id}.interface",
            )
            public_contracts = _require_dict(
                interface.get("public_contracts"),
                f"{skill_id}.public_contracts",
            )
            invocation = _require_dict(
                public_contracts.get("invocation"),
                f"{skill_id}.public_contracts.invocation",
            )
            wrapper_value = invocation.get("wrapper")
            if not isinstance(wrapper_value, str):
                raise MatrixError(f"{skill_id} public wrapper is missing")
            wrapper_relative = Path(wrapper_value)
            if (
                wrapper_relative.is_absolute()
                or not wrapper_relative.parts
                or ".." in wrapper_relative.parts
            ):
                raise MatrixError(f"{skill_id} public wrapper is unsafe")
            scripts = root / skill_id / "scripts"
            public_wrapper = root / skill_id / wrapper_relative
            package_wrapper = package / wrapper_relative
            if not public_wrapper.is_file() or not os.access(public_wrapper, os.X_OK):
                raise MatrixError(
                    f"public projection has no executable declared wrapper: "
                    f"{public_wrapper.relative_to(target).as_posix()}"
                )
            if (
                not package_wrapper.is_file()
                or public_wrapper.read_bytes() != package_wrapper.read_bytes()
                or bool(public_wrapper.stat().st_mode & stat.S_IXUSR)
                != bool(package_wrapper.stat().st_mode & stat.S_IXUSR)
            ):
                raise MatrixError(
                    f"public projection declared-wrapper drift: "
                    f"{public_wrapper.relative_to(target).as_posix()}"
                )
            leaked = [
                path.relative_to(target).as_posix()
                for path in scripts.iterdir()
                if path.is_file() and path != public_wrapper
            ]
            if leaked:
                raise MatrixError(
                    f"platform public projection leaked private wrappers: {sorted(leaked)}"
                )
    for other, root in PLATFORM_ROOTS.items():
        if other == platform:
            continue
        other_root = target / root
        if any(other_root.glob("guru-*")):
            raise MatrixError(f"unselected platform projection exists: {other}")


def _template_hash_state(root: Path) -> dict[str, Any]:
    template_hashes = _require_dict(
        _load_json(root / ".trellis/.template-hashes.json"), "template hashes"
    )
    if template_hashes.get("__version") != 2:
        raise MatrixError(".trellis/.template-hashes.json is not schema version 2")
    hashes = template_hashes.get("hashes")
    if not isinstance(hashes, dict) or not hashes:
        raise MatrixError("template hash inventory is empty")
    missing: list[str] = []
    mismatched: list[str] = []
    for relative, digest in hashes.items():
        if not isinstance(relative, str) or not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise MatrixError(f"invalid template hash row: {relative!r}")
        path = root / relative
        if not path.is_file():
            missing.append(relative)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            mismatched.append(relative)
    return {
        "schema_version": 2,
        "entry_count": len(hashes),
        "missing": _sorted_strings(missing),
        "mismatched": _sorted_strings(mismatched),
        "identity_sha256": _digest(hashes),
    }


def _assert_template_hashes(target: Path, source_root: Path) -> dict[str, Any]:
    target_state = _template_hash_state(target)
    if target_state["missing"]:
        raise MatrixError(
            f"template hash inventory has missing files: {target_state['missing']}"
        )
    source_state = _template_hash_state(source_root)
    allowed_mismatches = set(source_state["mismatched"])
    unknown = sorted(
        set(target_state["mismatched"]) - allowed_mismatches,
        key=lambda item: item.encode("utf-8"),
    )
    if unknown:
        raise MatrixError(f"unknown template-hash drift in isolated cell: {unknown}")
    return {
        "schema_version": 2,
        "entry_count": target_state["entry_count"],
        "matched_count": target_state["entry_count"] - len(target_state["mismatched"]),
        "preserved_local_edit_paths": target_state["mismatched"],
        "unknown_drift_count": 0,
        "identity_sha256": target_state["identity_sha256"],
    }


def _docs_authority_snapshot(target: Path) -> dict[str, str]:
    docs_root = target / "docs"
    if not docs_root.is_dir():
        raise MatrixError("business repository has no Docs authority root")
    expected = {
        path.relative_to(target).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(docs_root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }
    for domain in ("requirements", "design", "test", "architecture"):
        prefix = f"docs/{domain}/"
        if not any(relative.startswith(prefix) for relative in expected):
            raise MatrixError(f"complete {domain} authority was not frozen")
        if not any(
            relative.startswith(f"{prefix}versions/") for relative in expected
        ):
            raise MatrixError(f"versioned {domain} authority was not frozen")
    return expected


def _assert_docs_authority(target: Path, expected: Mapping[str, str]) -> None:
    if not expected:
        raise MatrixError("complete Requirements/Design/Test/Architecture authority was not frozen")
    authority_bytes: list[bytes] = []
    for relative, digest in expected.items():
        path = target / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise MatrixError(f"official update/preset changed Docs authority {relative}")
        authority_bytes.append(path.read_bytes())
    spec_root = target / ".trellis/spec"
    if not spec_root.is_dir():
        raise MatrixError("installed repository has no .trellis/spec projection")
    for path in (item for item in spec_root.rglob("*") if item.is_file()):
        if path.read_bytes() in authority_bytes:
            raise MatrixError(
                f".trellis/spec duplicated a business authority body: "
                f"{path.relative_to(target).as_posix()}"
            )


def _run_installed_smokes(
    target: Path,
    source_root: Path,
    work_root: Path,
    scenario: str,
    platform: str,
) -> dict[str, Any]:
    wrappers = target / ".trellis/guru-team/scripts/bash"
    _run(
        (str(wrappers / "check-skill-packages.sh"), "--root", str(target), "--json", "--mode", "installed"),
        log=work_root / "check-skill-packages.log",
    )
    installed_profile_evals = []
    for skill_id in (
        "guru-maintain-requirements-design-test-ssot",
        "guru-maintain-architecture-baseline",
        "guru-bootstrap-repository-ssot",
    ):
        discovery_log = work_root / f"discover-{skill_id}.log"
        _run(
            (
                str(wrappers / "discover-skill-contract.sh"),
                "--root",
                str(target),
                "--mode",
                "installed",
                "--skill",
                skill_id,
                "--json",
            ),
            log=discovery_log,
        )
        eval_output = _run(
            (
                str(wrappers / "run-skill-evals.sh"),
                "--root",
                str(target),
                "--mode",
                "installed",
                "--skill",
                skill_id,
                "--adapter",
                "shared",
                "--run-root",
                str(work_root / f"eval-{skill_id}"),
                "--json",
            ),
            capture=True,
            log=work_root / f"eval-{skill_id}.log",
        )
        eval_result = _require_dict(
            json.loads(eval_output), f"installed {skill_id} eval result"
        )
        if eval_result.get("status") != "passed":
            raise MatrixError(f"installed {skill_id} profile eval did not pass")
        cases = eval_result.get("cases")
        if not isinstance(cases, list) or not cases:
            raise MatrixError(f"installed {skill_id} profile eval has no cases")
        package = target / ".trellis/guru-team/skills/packages" / skill_id
        corpus = _require_dict(_load_json(package / "evals/evals.json"), "eval corpus")
        declared_cases = corpus.get("evals")
        if not isinstance(declared_cases, list) or not declared_cases:
            raise MatrixError(f"installed {skill_id} eval corpus has no cases")
        covered_profiles = _sorted_strings(
            str(row.get("input_profile_id"))
            for row in declared_cases
            if isinstance(row, dict) and isinstance(row.get("input_profile_id"), str)
        )
        interface = _require_dict(_load_json(package / "interface.json"), "interface")
        public_contracts = _require_dict(
            interface.get("public_contracts"), "public_contracts"
        )
        input_contract = _require_dict(public_contracts.get("input"), "public input")
        declared_profiles = _sorted_strings(
            str(row.get("id"))
            for row in input_contract.get("profiles", [])
            if isinstance(row, dict) and isinstance(row.get("id"), str)
        )
        if covered_profiles != declared_profiles:
            raise MatrixError(
                f"installed {skill_id} profile coverage mismatch: "
                f"declared={declared_profiles}, covered={covered_profiles}"
            )
        installed_profile_evals.append(
            {
                "skill_id": skill_id,
                "adapter": "shared",
                "platform_projection": platform,
                "profiles": covered_profiles,
                "case_count": len(cases),
                "status": "passed",
            }
        )
    smoke_results = []
    installed_python = target / ".trellis/guru-team/runtime/resolve-python.sh"
    installed_runtime = target / ".trellis/guru-team/runtime"
    for name, args in (
        (
            "closeout",
            (
                source_root
                / "trellis/presets/guru-team/scripts/python/verify_installed_closeout.py",
                "--repo",
                target,
                "--case",
                "after-update" if scenario == "existing" else "initial",
            ),
        ),
        (
            "phase0",
            (
                source_root
                / "trellis/presets/guru-team/scripts/python/verify_installed_phase0_transcript.py",
                "--installed-repo",
                target,
                "--work-root",
                work_root / "phase0",
                "--checkpoint",
                "matrix-cell",
                "--semantic-grading",
                source_root
                / "trellis/presets/guru-team/tests/semantic-retrieval-grading.json",
            ),
        ),
        (
            "task_workspace",
            (
                source_root
                / "trellis/presets/guru-team/scripts/python/verify_installed_task_workspace.py",
                "--installed-repo",
                target,
                "--work-root",
                work_root / "task-workspace",
                "--checkpoint",
                "matrix-cell",
            ),
        ),
    ):
        argv = (
            str(installed_python),
            str(target),
            str(installed_runtime),
            *(str(value) for value in args),
        )
        output = _run(argv, capture=True, log=work_root / f"{name}.log")
        payload = _require_dict(json.loads(output), f"{name} smoke")
        if payload.get("status") != "ok":
            raise MatrixError(f"{name} installed smoke did not pass")
        smoke_results.append(name)
    return {
        "installed_profiles": installed_profile_evals,
        "runtime_smokes": smoke_results,
    }


def validate_cell(
    target: Path,
    platform: str,
    scenario: str,
    expected_cli: str,
    cli_version: str,
    source_root: Path,
    work_root: Path,
) -> dict[str, Any]:
    if platform not in PLATFORM_ROOTS or scenario not in SCENARIOS:
        raise MatrixError(f"invalid cell identity: {platform}/{scenario}")
    if cli_version != expected_cli:
        raise MatrixError(f"cell CLI mismatch: expected {expected_cli}, got {cli_version}")
    project_version = (target / ".trellis/.version").read_text(encoding="utf-8").strip()
    if project_version != expected_cli:
        raise MatrixError(
            f"project .trellis/.version mismatch: expected {expected_cli}, got {project_version}"
        )
    installed = _require_dict(
        _load_json(target / ".trellis/guru-team/extension.json"), "installed manifest"
    )
    extension = _require_dict(installed.get("extension"), "installed extension")
    if extension.get("target_trellis_cli") != expected_cli:
        raise MatrixError("installed target_trellis_cli does not match exact target")
    for section in ("install", "skill_packages", "overlays"):
        selected = _require_string_list(
            _require_dict(installed.get(section), f"installed {section}").get(
                "selected_platforms"
            ),
            f"installed {section}.selected_platforms",
        )
        if selected != [platform]:
            raise MatrixError(
                f"installed {section} platform set mismatch: expected {[platform]}, got {selected}"
            )
    _assert_installed_file_modes(target, installed, source_root)
    _assert_platform_projection(target, platform)
    template_hashes = _assert_template_hashes(target, source_root)
    sidecars = _sidecars(target)
    if sidecars:
        raise MatrixError(f"unresolved cell sidecars: {sidecars}")
    smokes = _run_installed_smokes(
        target, source_root, work_root, scenario, platform
    )
    sidecars = _sidecars(target)
    if sidecars:
        raise MatrixError(f"installed smokes left cell sidecars: {sidecars}")
    return {
        "platform": platform,
        "scenario": scenario,
        "cli_before": DEFAULT_BEFORE_CLI if scenario == "existing" else expected_cli,
        "cli_after": cli_version,
        "project_version": project_version,
        "extension_version": extension.get("version"),
        "target_trellis_cli": extension.get("target_trellis_cli"),
        "selected_platforms": [platform],
        "shared_projection": True,
        "template_hashes": template_hashes,
        "sidecar_count": 0,
        "installed_smokes": smokes,
        "status": "passed",
    }


def _run_cell(
    *,
    repo_root: Path,
    cell_root: Path,
    platform: str,
    scenario: str,
    workflow_source: str,
    before_tag: str,
    before_cli: str,
    target_cli: str,
    allow_local_sample: bool,
) -> dict[str, Any]:
    target = cell_root / "project"
    prefix = cell_root / "trellis-cli-prefix"
    _init_git_repo(target)
    initial_cli = target_cli if scenario == "clean" else before_cli
    binary, env = _install_cli(prefix, initial_cli, cell_root / "npm-install.log")
    actual_before = _assert_version(binary, initial_cli, env)

    if scenario == "existing":
        source_root = cell_root / "before-source"
        _export_git_tree(repo_root, before_tag, source_root, cell_root / "before-source.tar")
        initial_workflow_source = f"gh:castbox/guru-trellis/trellis#{before_tag}"
    else:
        source_root = repo_root
        initial_workflow_source = workflow_source

    local_sample = _install_workflow(
        target,
        binary,
        env,
        platform,
        initial_workflow_source,
        repo_root if scenario == "clean" else source_root,
        allow_local_sample if scenario == "clean" else False,
        cell_root / "trellis-init.log",
    )
    before_docs = _docs_authority_snapshot(target)
    initial_preset = _apply_preset(
        source_root, target, platform, cell_root / "preset-initial.log"
    )

    before_projection = capability_projection(source_root)
    before_installed_projection = installed_capability_projection(target)
    update_mode = "not_applicable"
    if scenario == "existing":
        before_manifest = _require_dict(
            _load_json(target / ".trellis/guru-team/extension.json"),
            "before installed manifest",
        )
        before_extension = _require_dict(
            before_manifest.get("extension"), "before installed extension"
        )
        if before_extension.get("version") != "0.6.5-guru.36":
            raise MatrixError(
                "existing cell did not start from replacement release extension 0.6.5-guru.36"
            )
        _run(
            (str(binary), "upgrade", "--tag", target_cli),
            cwd=target,
            env=env,
            log=cell_root / "trellis-upgrade.log",
        )
        actual_after_upgrade = _assert_version(binary, target_cli, env)
        dry_run = _run(
            (str(binary), "update", "--dry-run"),
            cwd=target,
            env=env,
            capture=True,
            log=cell_root / "trellis-update-dry-run.log",
        )
        if "MIGRATION REQUIRED" in dry_run:
            _run(
                (str(binary), "update", "--migrate", "--skip-all"),
                cwd=target,
                env=env,
                log=cell_root / "trellis-update.log",
            )
            update_mode = "migrate"
        else:
            _run(
                (str(binary), "update", "--skip-all"),
                cwd=target,
                env=env,
                log=cell_root / "trellis-update.log",
            )
            update_mode = "update"
        local_sample = _workflow_source_requires_local_sample(repo_root, workflow_source)
        if local_sample and not allow_local_sample:
            raise MatrixError(
                "existing cell candidate workflow is unpublished; exact remote source is required"
            )
        _preview_and_switch_workflow(
            target,
            binary,
            env,
            workflow_source,
            repo_root,
            source_root,
            local_sample,
            cell_root,
        )
        reapplied_preset = _apply_preset(
            repo_root,
            target,
            platform,
            cell_root / "preset-reapply.log",
            previous_root=source_root,
        )
    else:
        actual_after_upgrade = actual_before
        reapplied_preset = {"status": "not_applicable", "reconciled_backups": []}

    _assert_docs_authority(target, before_docs)

    after_projection = capability_projection(repo_root)
    comparison = compare_capabilities(before_projection, after_projection)
    _assert_projection_consistency(comparison, "source")
    after_installed_projection = installed_capability_projection(target)
    installed_comparison = compare_capabilities(
        before_installed_projection, after_installed_projection
    )
    _assert_projection_consistency(installed_comparison, "installed")
    result = validate_cell(
        target,
        platform,
        scenario,
        target_cli,
        actual_after_upgrade,
        repo_root,
        cell_root,
    )
    result.update(
        {
            "update_mode": update_mode,
            "workflow_sample": "public_plus_local_candidate" if local_sample else "exact_marketplace",
            "before_projection_sha256": before_projection["projection_sha256"],
            "after_projection_sha256": after_projection["projection_sha256"],
            "comparison_sha256": comparison["comparison_sha256"],
            "before_installed_projection_sha256": before_installed_projection[
                "projection_sha256"
            ],
            "after_installed_projection_sha256": after_installed_projection[
                "projection_sha256"
            ],
            "installed_comparison_sha256": installed_comparison[
                "comparison_sha256"
            ],
            "preset_initial": initial_preset,
            "preset_reapply": reapplied_preset,
        }
    )
    return result


def run_matrix(args: argparse.Namespace) -> dict[str, Any]:
    stage = "pre-matrix"
    cell_id: str | None = None
    try:
        repo_root = args.repo_root.resolve()
        work_root = args.work_root.resolve()
        if work_root.exists() and any(work_root.iterdir()):
            raise MatrixError(f"matrix work root must be empty: {work_root}")
        work_root.mkdir(parents=True, exist_ok=True)
        matrix = build_matrix(repo_root)
        source_before = source_state(repo_root)
        before_identity = resolve_before_tag(repo_root, args.before_tag)
        before_tag = str(before_identity["before_tag"])
        before_commit = str(before_identity["before_commit"])
        before_tag_object = str(before_identity["before_tag_object"])
        results = []
        for cell in matrix["cells"]:
            stage = "matrix-cell"
            cell_id = str(cell["cell_id"])
            cell_root = work_root / cell_id
            cell_root.mkdir()
            result = _run_cell(
                repo_root=repo_root,
                cell_root=cell_root,
                platform=str(cell["platform"]),
                scenario=str(cell["scenario"]),
                workflow_source=args.workflow_source,
                before_tag=before_tag,
                before_cli=args.before_cli,
                target_cli=args.target_cli,
                allow_local_sample=args.allow_local_sample,
            )
            result["cell_id"] = cell["cell_id"]
            (cell_root / "cell-summary.json").write_bytes(_canonical_json(result))
            results.append(result)

        stage = "post-matrix"
        cell_id = None

        representative = next(
            work_root / str(row["cell_id"]) / "project"
            for row in matrix["cells"]
            if row["scenario"] == "clean"
        )
        parallel_root = work_root / "parallel-finish"
        installed_python = representative / ".trellis/guru-team/runtime/resolve-python.sh"
        installed_runtime = representative / ".trellis/guru-team/runtime"
        parallel_helper = (
            repo_root
            / "trellis/presets/guru-team/scripts/python/verify_installed_parallel_finish.py"
        )
        parallel_output = _run(
            (
                str(installed_python),
                str(representative),
                str(installed_runtime),
                str(parallel_helper),
                "--installed-repo",
                str(representative),
                "--work-root",
                str(parallel_root),
            ),
            capture=True,
            log=work_root / "parallel-finish.log",
        )
        parallel_finish = _require_dict(
            json.loads(parallel_output), "parallel Finish compatibility summary"
        )
        if parallel_finish.get("status") != "passed":
            raise MatrixError("parallel Finish compatibility fixture did not pass")

        source_after = source_state(repo_root)
        if source_after["identity_sha256"] != source_before["identity_sha256"]:
            raise MatrixError("source repository changed while compatibility matrix was running")

        legacy_representative = work_root.parent / "project"
        if legacy_representative.exists():
            raise MatrixError(
                f"representative install root already exists: {legacy_representative}"
            )
        shutil.copytree(
            representative,
            legacy_representative,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "*.pyo"),
        )
        summary = {
            "schema_version": SCHEMA_VERSION,
            "status": "passed",
            "source_commit": source_before["head"],
            "source_state": source_before,
            "source_identity_sha256": source_before["identity_sha256"],
            "before_tag": before_tag,
            "before_tag_object": before_tag_object,
            "before_commit": before_commit,
            "before_cli": args.before_cli,
            "target_cli": args.target_cli,
            "workflow_source": args.workflow_source,
            "platform_inventory_sha256": matrix["platform_inventory_sha256"],
            "matrix_sha256": matrix["matrix_sha256"],
            "cell_count": len(results),
            "cells": results,
            "parallel_finish": parallel_finish,
            "representative_root": "project",
            "unpublished_candidate_boundary": any(
                row["workflow_sample"] == "public_plus_local_candidate"
                for row in results
            ),
            "external_boundaries": [
                "A github_pr route requires a separately confirmed dedicated disposable GitHub repository"
            ]
            if parallel_finish.get("a", {}).get("real_github_verified") is not True
            else [],
        }
        summary["summary_sha256"] = _digest(summary)
        (work_root / "matrix-summary.json").write_bytes(_canonical_json(summary))
        return summary
    except MatrixError as exc:
        raise exc.with_context(stage, cell_id) from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise MatrixError(str(exc), stage=stage, cell_id=cell_id) from exc


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("derive-platforms", "plan", "project"):
        command = sub.add_parser(name)
        command.add_argument("--repo-root", type=Path, required=True)
    compare = sub.add_parser("compare")
    compare.add_argument("--before", type=Path, required=True)
    compare.add_argument("--after", type=Path, required=True)
    run = sub.add_parser("run")
    run.add_argument("--repo-root", type=Path, required=True)
    run.add_argument("--work-root", type=Path, required=True)
    run.add_argument("--workflow-source", required=True)
    run.add_argument("--before-tag", default=DEFAULT_BEFORE_TAG)
    run.add_argument("--before-cli", default=DEFAULT_BEFORE_CLI)
    run.add_argument("--target-cli", default=DEFAULT_TARGET_CLI)
    run.add_argument("--allow-local-sample", action="store_true")
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "derive-platforms":
            result = derive_platform_inventory(args.repo_root.resolve())
        elif args.command == "plan":
            result = build_matrix(args.repo_root.resolve())
        elif args.command == "project":
            result = capability_projection(args.repo_root.resolve())
        elif args.command == "compare":
            result = compare_capabilities(
                _require_dict(_load_json(args.before), "before projection"),
                _require_dict(_load_json(args.after), "after projection"),
            )
        else:
            result = run_matrix(args)
    except MatrixError as exc:
        print(json.dumps(matrix_failure_payload(exc), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 2
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps(matrix_failure_payload(MatrixError(str(exc))), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
