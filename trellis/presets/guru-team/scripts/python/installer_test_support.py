"""Shared fixture data for preset installer tests."""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path
from unittest import mock

import apply_guru_team_trellis_preset as preset
import validate_upstream_ownership as ownership


GURU_FINISH_ENTRIES = (
    ".codex/prompts/guru-finish-work.md",
    ".claude/commands/guru/finish-work.md",
    ".cursor/commands/guru-finish-work.md",
    ".opencode/commands/guru-finish-work.md",
)

PLANNED_SKILL_IDS: list[str] = []
PLANNED_SKILL_ROWS: list[dict[str, str]] = []
RUNTIME_RESULT = {
    "status": "ok",
    "action": "reused",
    "runtime_identity": "0123456789abcdef01234567",
    "interpreter": sys.executable,
}
_runtime_patchers: list[mock._patch] = []


def install_reviewed_delivery_candidate(root: Path) -> None:
    """Prepare a test target from explicit, actually installed upstream assets.

    This is fixture preparation, not CLI installation proof. The production
    installation diagnosis still loads and validates these copied modules.
    """
    configured = os.environ.get("GURU_UPSTREAM_DELIVERY_SCRIPTS")
    if not configured:
        raise RuntimeError("Set GURU_UPSTREAM_DELIVERY_SCRIPTS to reviewed installed candidate scripts.")
    source = Path(configured).resolve()
    if not (source / "common/delivery_schema.py").is_file():
        raise RuntimeError("The installed candidate must contain the public Delivery modules.")
    package = None
    for parent in source.parents:
        manifest = parent / "package.json"
        if manifest.is_file():
            value = json.loads(manifest.read_text(encoding="utf-8"))
            if value.get("name") == "@mindfoldhq/trellis":
                package = value
                break
    if package is None or not isinstance(package.get("version"), str):
        raise RuntimeError("The candidate version must come from its installed Trellis package.")
    trellis = root / ".trellis"
    trellis.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, trellis / "scripts", dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (trellis / ".version").write_text(package["version"] + "\n", encoding="utf-8")


def setUpModule() -> None:
    patcher = mock.patch.object(preset, "ensure_managed_python_runtime", return_value=RUNTIME_RESULT)
    _runtime_patchers.append(patcher)
    patcher.start()


def tearDownModule() -> None:
    for patcher in reversed(_runtime_patchers):
        patcher.stop()


def copy_canonical_source(source_root: Path, target: Path) -> None:
    for relative in (
        Path("trellis/presets/guru-team/ownership"),
        Path("trellis/presets/guru-team/overlays"),
        Path("trellis/workflows/guru-team"),
        Path("trellis/skills/guru-team"),
        Path(".trellis/guru-team"),
        Path(".agents/skills"),
        Path(".claude/skills"),
        Path(".codex/skills"),
        Path(".cursor/skills"),
    ):
        source = source_root / relative
        if source.exists():
            shutil.copytree(source, target / relative)
    for relative in (ownership.EXTENSION_RELATIVE, ownership.INSTALLER_RELATIVE):
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_root / relative, destination)


def prepare_raw_apply_source(source_root: Path, target: Path) -> None:
    """Prepare an isolated current candidate for real apply/reapply tests."""
    shutil.copytree(
        source_root, target,
        ignore=shutil.ignore_patterns(
            ".git", ".runtime", "tasks", "__pycache__", "*.pyc", "*.pyo", ".DS_Store"
        ),
    )
    # Keep the original checkout's legacy Task inventory and runtime untouched.
    install_reviewed_delivery_candidate(target)
    (target / ".trellis/workflow.md").write_bytes(
        (target / "trellis/workflows/guru-team/workflow.md").read_bytes()
    )
    # Retain original selection metadata, then materialize packages afresh.
    manifest = (target / ".trellis/guru-team/extension.json").read_bytes()
    for relative in (".trellis/guru-team", ".agents/skills", ".claude/skills",
                     ".codex/skills", ".cursor/skills", ".opencode/skills"):
        shutil.rmtree(target / relative, ignore_errors=True)
    (target / ".trellis/guru-team").mkdir(parents=True)
    (target / ".trellis/guru-team/extension.json").write_bytes(manifest)
