"""Shared fixture data for preset installer tests."""

from __future__ import annotations

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
