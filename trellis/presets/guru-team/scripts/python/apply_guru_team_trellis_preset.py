#!/usr/bin/env python3
"""Apply Guru team Trellis companion assets to a project repository."""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import shutil
from pathlib import Path
from typing import Any


GURU_OVERLAY_MARKER = "guru-team-overlay:"
MANAGED_CONFIG = Path("config-template.yml")
MANAGED_ASSET_PATHS = [
    Path("config-template.yml"),
    Path("schemas/intake-handoff.schema.json"),
    Path("scripts/bash/check-env.sh"),
    Path("scripts/bash/prepare-task.sh"),
    Path("scripts/bash/review-branch.sh"),
    Path("scripts/bash/check-review-gate.sh"),
    Path("scripts/bash/publish-pr.sh"),
    Path("scripts/bash/finish-work.sh"),
    Path("scripts/python/guru_team_trellis.py"),
]


def read_text_if_exists(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""
    except FileNotFoundError:
        return ""


def repo_root_from_args(value: str | None) -> Path:
    root = Path(value or os.getcwd()).resolve()
    if not (root / ".trellis").is_dir():
        raise SystemExit(f"Target repo does not contain .trellis/: {root}")
    return root


def guru_root_from_script() -> Path:
    return Path(__file__).resolve().parents[5]


def ensure_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | 0o755)


def copy_managed(source: Path, target: Path) -> dict[str, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copyfile(source, target)
        return {"path": str(target), "action": "installed"}
    if filecmp.cmp(source, target, shallow=False):
        return {"path": str(target), "action": "unchanged"}
    backup = target.with_name(f"{target.name}.bak")
    shutil.copyfile(target, backup)
    shutil.copyfile(source, target)
    return {"path": str(target), "action": "updated_managed", "backup": str(backup)}


def looks_like_trellis_generated_entry(relative: Path, target: Path) -> bool:
    """Return true for known Trellis-generated command/skill entry files.

    The preset may replace upstream-generated entry prompts so Guru Team routing is
    active after install. Unknown local edits still get a .new copy.
    """

    text = read_text_if_exists(target)
    if not text:
        return False
    if GURU_OVERLAY_MARKER in text or "Guru Team" in text:
        return True

    rel = relative.as_posix()
    lower = text.lower()
    if "trellis" not in lower:
        return False

    is_start = rel.endswith("trellis-start/SKILL.md") or rel.endswith("trellis-start.md")
    is_continue = rel.endswith("trellis-continue/SKILL.md") or rel.endswith("trellis-continue.md") or rel.endswith("continue.md")
    is_finish = rel.endswith("trellis-finish-work/SKILL.md") or rel.endswith("trellis-finish-work.md") or rel.endswith("finish-work.md")
    is_known_entry_path = is_start or is_continue or is_finish
    has_trellis_generated_signal = any(
        signal in text
        for signal in [
            ".trellis/workflow.md",
            "get_context.py",
            "task.py",
            "add_session.py",
            "workflow-state",
            "trellis-brainstorm",
            "trellis-check",
            "trellis-update-spec",
        ]
    )
    if is_known_entry_path and has_trellis_generated_signal:
        return True

    if is_start:
        return "start" in lower and ("get_context.py" in text or "workflow" in lower or "session" in lower)
    if is_continue:
        return "continue" in lower and ("get_context.py" in text or "workflow" in lower or "task.py" in text)
    if is_finish:
        return "finish" in lower and ("archive" in lower or "journal" in lower or "add_session.py" in text)
    return False


def copy_overlay(source: Path, target: Path, relative: Path) -> dict[str, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copyfile(source, target)
        return {"path": str(target), "action": "installed"}
    if filecmp.cmp(source, target, shallow=False):
        return {"path": str(target), "action": "unchanged"}
    if looks_like_trellis_generated_entry(relative, target):
        shutil.copyfile(source, target)
        return {"path": str(target), "action": "replaced_overlay"}
    new_target = target.with_name(f"{target.name}.new")
    shutil.copyfile(source, new_target)
    return {"path": str(new_target), "action": "new_copy", "existing": str(target)}


def install_assets(src: Path, dst: Path, repo: Path) -> dict[str, list[str]]:
    if not src.is_dir():
        raise SystemExit(f"Missing source directory: {src}")

    dst.mkdir(parents=True, exist_ok=True)

    installed: list[str] = []
    unchanged: list[str] = []
    new_copies: list[str] = []
    replaced_overlays: list[str] = []
    updated_managed: list[str] = []
    managed_backups: list[str] = []
    for relative in MANAGED_ASSET_PATHS:
        result = copy_managed(src / relative, dst / relative)
        rel_path = Path(result["path"]).relative_to(repo).as_posix()
        if result["action"] == "installed":
            installed.append(rel_path)
        elif result["action"] == "unchanged":
            unchanged.append(rel_path)
        elif result["action"] == "updated_managed":
            updated_managed.append(rel_path)
            backup = result.get("backup")
            if backup:
                managed_backups.append(Path(backup).relative_to(repo).as_posix())

    target_config = dst / "config.yml"
    if not target_config.exists():
        shutil.copyfile(src / MANAGED_CONFIG, target_config)
        installed.append(target_config.relative_to(repo).as_posix())

    for script in [
        dst / "scripts/bash/check-env.sh",
        dst / "scripts/bash/prepare-task.sh",
        dst / "scripts/bash/review-branch.sh",
        dst / "scripts/bash/check-review-gate.sh",
        dst / "scripts/bash/publish-pr.sh",
        dst / "scripts/bash/finish-work.sh",
        dst / "scripts/python/guru_team_trellis.py",
    ]:
        if script.exists():
            ensure_executable(script)

    overlays = install_overlays(repo, guru_root_from_script())
    installed.extend(overlays["installed"])
    unchanged.extend(overlays["unchanged"])
    new_copies.extend(overlays["new_copies"])
    replaced_overlays.extend(overlays["replaced_overlays"])
    updated_managed.extend(overlays["updated_managed"])
    managed_backups.extend(overlays["managed_backups"])

    return {
        "installed": installed,
        "unchanged": unchanged,
        "new_copies": new_copies,
        "replaced_overlays": replaced_overlays,
        "updated_managed": updated_managed,
        "managed_backups": managed_backups,
    }


def install_overlays(repo: Path, guru_root: Path) -> dict[str, list[str]]:
    overlay_root = guru_root / "trellis/presets/guru-team/overlays"
    installed: list[str] = []
    unchanged: list[str] = []
    new_copies: list[str] = []
    replaced_overlays: list[str] = []
    updated_managed: list[str] = []
    managed_backups: list[str] = []
    if not overlay_root.is_dir():
        return {
            "installed": installed,
            "unchanged": unchanged,
            "new_copies": new_copies,
            "replaced_overlays": replaced_overlays,
            "updated_managed": updated_managed,
            "managed_backups": managed_backups,
        }
    for source in sorted(path for path in overlay_root.rglob("*") if path.is_file()):
        relative = source.relative_to(overlay_root)
        target = repo / relative
        result = copy_overlay(source, target, relative)
        rel_path = Path(result["path"]).relative_to(repo).as_posix()
        if result["action"] == "installed":
            installed.append(rel_path)
        elif result["action"] == "unchanged":
            unchanged.append(rel_path)
        elif result["action"] == "replaced_overlay":
            replaced_overlays.append(rel_path)
        else:
            new_copies.append(rel_path)
    return {
        "installed": installed,
        "unchanged": unchanged,
        "new_copies": new_copies,
        "replaced_overlays": replaced_overlays,
        "updated_managed": updated_managed,
        "managed_backups": managed_backups,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply Guru team Trellis preset")
    parser.add_argument("--repo", help="Target repository root. Defaults to current directory.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    repo = repo_root_from_args(args.repo)
    guru_root = guru_root_from_script()
    src = guru_root / "trellis/workflows/guru-team"
    dst = repo / ".trellis/guru-team"
    result = install_assets(src, dst, repo)

    payload: dict[str, Any] = {
        "status": "ok",
        "repo": str(repo),
        "installed": result["installed"],
        "unchanged": result["unchanged"],
        "new_copies": result["new_copies"],
        "replaced_overlays": result["replaced_overlays"],
        "updated_managed": result["updated_managed"],
        "managed_backups": result["managed_backups"],
        "config": ".trellis/guru-team/config.yml",
        "workflow_marketplace": "gh:castbox/guru-trellis/trellis",
        "public_workflow_marketplace": "gh:castbox/guru-trellis/trellis",
        "workflow_template": "guru-team",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
