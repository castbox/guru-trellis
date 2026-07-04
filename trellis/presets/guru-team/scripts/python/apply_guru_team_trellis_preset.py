#!/usr/bin/env python3
"""Apply Guru team Trellis companion assets to a project repository."""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


GURU_OVERLAY_MARKER = "guru-team-overlay:"
EXTENSION_MANIFEST = Path("trellis/guru-team-extension.json")
WORKFLOW_MARKETPLACE = "gh:castbox/guru-trellis/trellis"
WORKFLOW_TEMPLATE = "guru-team"
DEFAULT_PLATFORMS = ("codex", "cursor")
PLATFORM_OVERLAY_PREFIXES = {
    "codex": (Path(".codex"),),
    "cursor": (Path(".cursor"),),
    "claude": (Path(".claude"),),
}
ALL_PLATFORMS = tuple(PLATFORM_OVERLAY_PREFIXES)
ALWAYS_OVERLAY_PREFIXES = (Path(".agents"),)
CODEX_DISPATCH_HEADER = """#-------------------------------------------------------------------------------
# Codex (dispatch behavior)
#-------------------------------------------------------------------------------
# Codex-only knob; other platforms ignore it. Default ("sub-agent") lets the
# main Codex session dispatch trellis-implement / trellis-check /
# trellis-research. Codex sub-agents run with `fork_turns="none"` isolation, so
# the main session must include `Active task: <task path>` in dispatch prompts
# and sub-agents fall back to `task.py current --source` if needed. Set
# "inline" only as an explicit downgrade/debug mode where the main Codex agent
# edits and checks directly.
"""
MANAGED_CONFIG = Path("config-template.yml")
MANAGED_ASSET_PATHS = [
    Path("config-template.yml"),
    Path("schemas/intake-handoff.schema.json"),
    Path("scripts/bash/check-env.sh"),
    Path("scripts/bash/version.sh"),
    Path("scripts/bash/prepare-task.sh"),
    Path("scripts/bash/record-planning-approval.sh"),
    Path("scripts/bash/check-planning-approval.sh"),
    Path("scripts/bash/record-phase2-check.sh"),
    Path("scripts/bash/check-phase2-check.sh"),
    Path("scripts/bash/review-branch.sh"),
    Path("scripts/bash/check-review-gate.sh"),
    Path("scripts/bash/publish-pr.sh"),
    Path("scripts/bash/finish-work.sh"),
    Path("scripts/python/guru_team_trellis.py"),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        return subprocess.CompletedProcess(["git", *args], 127, "", str(exc))


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


def load_extension_manifest(guru_root: Path) -> dict[str, Any]:
    manifest_path = guru_root / EXTENSION_MANIFEST
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing Guru Team extension manifest: {manifest_path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid Guru Team extension manifest JSON: {manifest_path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"Guru Team extension manifest must be a JSON object: {manifest_path}")
    for key in ["schema_version", "extension_id", "version", "workflow_template_id"]:
        if not str(payload.get(key) or "").strip():
            raise SystemExit(f"Guru Team extension manifest missing required field: {key}")
    return payload


def is_mutable_ref(ref: str | None, exact_tag: str | None) -> bool | None:
    if not ref:
        return None
    if exact_tag and ref == exact_tag:
        return False
    if ref == "HEAD":
        return True
    return not re_full_hex(ref)


def re_full_hex(value: str) -> bool:
    return len(value) == 40 and all(ch in "0123456789abcdefABCDEF" for ch in value)


def source_provenance(guru_root: Path) -> dict[str, Any]:
    top_proc = run_git(["rev-parse", "--show-toplevel"], guru_root)
    if top_proc.returncode != 0:
        return {
            "repo": None,
            "ref": None,
            "commit": None,
            "tree_state": "archive",
            "is_mutable_ref": None,
        }

    git_root = Path(top_proc.stdout.strip()).resolve()
    remote_proc = run_git(["remote", "get-url", "origin"], git_root)
    ref_proc = run_git(["rev-parse", "--abbrev-ref", "HEAD"], git_root)
    commit_proc = run_git(["rev-parse", "HEAD"], git_root)
    tag_proc = run_git(["describe", "--tags", "--exact-match", "HEAD"], git_root)
    dirty_proc = run_git(["status", "--short"], git_root)

    ref = ref_proc.stdout.strip() if ref_proc.returncode == 0 else None
    if ref == "HEAD" and tag_proc.returncode == 0:
        ref = tag_proc.stdout.strip()
    exact_tag = tag_proc.stdout.strip() if tag_proc.returncode == 0 else None
    tree_state = "dirty" if dirty_proc.returncode == 0 and dirty_proc.stdout.strip() else "clean"
    if dirty_proc.returncode != 0:
        tree_state = "unknown"

    return {
        "repo": remote_proc.stdout.strip() if remote_proc.returncode == 0 and remote_proc.stdout.strip() else None,
        "ref": ref,
        "commit": commit_proc.stdout.strip() if commit_proc.returncode == 0 and commit_proc.stdout.strip() else None,
        "tree_state": tree_state,
        "is_mutable_ref": is_mutable_ref(ref, exact_tag),
    }


def extension_summary(manifest: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    requires = manifest.get("requires") if isinstance(manifest.get("requires"), dict) else {}
    return {
        "extension_id": manifest.get("extension_id"),
        "version": manifest.get("version"),
        "workflow_template_id": manifest.get("workflow_template_id"),
        "trellis_cli_compatibility": requires.get("trellis_cli"),
        "source_repo": source.get("repo"),
        "source_ref": source.get("ref"),
        "source_commit": source.get("commit"),
        "source_tree_state": source.get("tree_state"),
        "source_is_mutable_ref": source.get("is_mutable_ref"),
    }


def build_installed_extension_manifest(
    manifest: dict[str, Any],
    source: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    managed_assets = sorted(
        set(result["installed"])
        | set(result["unchanged"])
        | set(result["updated_managed"])
        | set(result["replaced_overlays"])
        | {".trellis/guru-team/extension.json"}
    )
    return {
        "schema_version": "1.0",
        "extension": manifest,
        "installed_at": now_iso(),
        "source": source,
        "install": {
            "selected_platforms": result["platforms"],
            "all_platforms": result["all_platforms"],
            "managed_assets": managed_assets,
            "new_copies": result["new_copies"],
            "managed_backups": result["managed_backups"],
            "workflow_marketplace": WORKFLOW_MARKETPLACE,
            "workflow_template": WORKFLOW_TEMPLATE,
        },
        "notes": "This file records deterministic install provenance for the Guru Team Trellis extension. Upgrade and rollback judgment belongs to AI/human review.",
    }


def write_installed_extension_manifest(dst: Path, payload: dict[str, Any]) -> str:
    path = dst / "extension.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path.name


def ensure_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | 0o755)


def path_has_prefix(path: Path, prefix: Path) -> bool:
    return path == prefix or prefix in path.parents


def overlay_selected(relative: Path, platforms: set[str]) -> bool:
    if any(path_has_prefix(relative, prefix) for prefix in ALWAYS_OVERLAY_PREFIXES):
        return True
    selected_prefixes = [
        prefix
        for platform in sorted(platforms)
        for prefix in PLATFORM_OVERLAY_PREFIXES[platform]
    ]
    return any(path_has_prefix(relative, prefix) for prefix in selected_prefixes)


def selected_platforms(platforms: list[str] | None, all_platforms: bool) -> tuple[set[str], bool]:
    if all_platforms:
        return set(ALL_PLATFORMS), True
    if platforms:
        return set(platforms), False
    return set(DEFAULT_PLATFORMS), False


def leading_spaces(value: str) -> int:
    return len(value) - len(value.lstrip(" "))


def strip_inline_comment(value: str) -> str:
    return value.split("#", 1)[0].strip().strip("\"'")


def ensure_codex_dispatch_mode(repo: Path) -> dict[str, str | None]:
    """Materialize the Guru Team Codex default in project .trellis/config.yaml.

    Explicit `dispatch_mode: inline` is a user downgrade and is preserved.
    Missing, commented-out, or invalid values are updated to `sub-agent` so
    Codex can satisfy the independent Branch Review Gate path by default.
    """

    config_path = repo / ".trellis/config.yaml"
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(f"{CODEX_DISPATCH_HEADER}codex:\n  dispatch_mode: sub-agent\n", encoding="utf-8")
        return {"action": "installed", "path": ".trellis/config.yaml", "previous": None, "mode": "sub-agent"}

    original = config_path.read_text(encoding="utf-8")
    lines = original.splitlines()
    codex_index: int | None = None
    codex_indent = 0
    dispatch_index: int | None = None
    dispatch_value: str | None = None

    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "codex:":
            codex_index = index
            codex_indent = leading_spaces(line)
            continue
        if codex_index is not None:
            indent = leading_spaces(line)
            if indent <= codex_indent:
                break
            if stripped.startswith("dispatch_mode:"):
                dispatch_index = index
                dispatch_value = strip_inline_comment(stripped.split(":", 1)[1])
                break

    if dispatch_value in {"sub-agent", "inline"}:
        return {
            "action": "unchanged",
            "path": ".trellis/config.yaml",
            "previous": dispatch_value,
            "mode": dispatch_value,
        }

    if dispatch_index is not None:
        indent = " " * leading_spaces(lines[dispatch_index])
        previous = dispatch_value or None
        lines[dispatch_index] = f"{indent}dispatch_mode: sub-agent"
        updated = "\n".join(lines).rstrip() + "\n"
        config_path.write_text(updated, encoding="utf-8")
        return {"action": "updated", "path": ".trellis/config.yaml", "previous": previous, "mode": "sub-agent"}

    if codex_index is not None:
        insert_at = codex_index + 1
        child_indent = " " * (codex_indent + 2)
        while insert_at < len(lines):
            line = lines[insert_at]
            if line.strip() and not line.lstrip().startswith("#") and leading_spaces(line) <= codex_indent:
                break
            insert_at += 1
        lines.insert(insert_at, f"{child_indent}dispatch_mode: sub-agent")
        updated = "\n".join(lines).rstrip() + "\n"
        config_path.write_text(updated, encoding="utf-8")
        return {"action": "updated", "path": ".trellis/config.yaml", "previous": None, "mode": "sub-agent"}

    separator = "" if original.endswith("\n") or not original else "\n"
    addition = f"{separator}\n{CODEX_DISPATCH_HEADER}codex:\n  dispatch_mode: sub-agent\n"
    config_path.write_text(original.rstrip() + addition, encoding="utf-8")
    return {"action": "updated", "path": ".trellis/config.yaml", "previous": None, "mode": "sub-agent"}


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


def install_assets(
    src: Path,
    dst: Path,
    repo: Path,
    platforms: set[str] | None = None,
    all_platforms: bool = False,
) -> dict[str, Any]:
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
        dst / "scripts/bash/version.sh",
        dst / "scripts/bash/prepare-task.sh",
        dst / "scripts/bash/record-planning-approval.sh",
        dst / "scripts/bash/check-planning-approval.sh",
        dst / "scripts/bash/record-phase2-check.sh",
        dst / "scripts/bash/check-phase2-check.sh",
        dst / "scripts/bash/review-branch.sh",
        dst / "scripts/bash/check-review-gate.sh",
        dst / "scripts/bash/publish-pr.sh",
        dst / "scripts/bash/finish-work.sh",
        dst / "scripts/python/guru_team_trellis.py",
    ]:
        if script.exists():
            ensure_executable(script)

    selected = platforms or set(DEFAULT_PLATFORMS)
    overlays = install_overlays(repo, guru_root_from_script(), selected)
    installed.extend(overlays["installed"])
    unchanged.extend(overlays["unchanged"])
    new_copies.extend(overlays["new_copies"])
    replaced_overlays.extend(overlays["replaced_overlays"])
    updated_managed.extend(overlays["updated_managed"])
    managed_backups.extend(overlays["managed_backups"])
    codex_dispatch = ensure_codex_dispatch_mode(repo)

    result = {
        "installed": installed,
        "unchanged": unchanged,
        "new_copies": new_copies,
        "replaced_overlays": replaced_overlays,
        "updated_managed": updated_managed,
        "managed_backups": managed_backups,
        "codex_dispatch": codex_dispatch,
        "platforms": sorted(selected),
        "all_platforms": all_platforms,
    }
    guru_root = guru_root_from_script()
    manifest = load_extension_manifest(guru_root)
    source = source_provenance(guru_root)
    installed_manifest = build_installed_extension_manifest(manifest, source, result)
    write_installed_extension_manifest(dst, installed_manifest)
    rel_extension = (dst / "extension.json").relative_to(repo).as_posix()
    result["extension_manifest"] = rel_extension
    result["guru_team_extension"] = extension_summary(manifest, source)
    return result


def install_overlays(repo: Path, guru_root: Path, platforms: set[str]) -> dict[str, list[str]]:
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
        if not overlay_selected(relative, platforms):
            continue
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
    parser.add_argument("--version", action="store_true", help="Print the Guru Team extension version from the canonical manifest and exit.")
    platform_group = parser.add_mutually_exclusive_group()
    platform_group.add_argument(
        "--platform",
        action="append",
        choices=ALL_PLATFORMS,
        help="Platform overlay to install. Repeat to select multiple platforms. Defaults to codex + cursor.",
    )
    platform_group.add_argument(
        "--all-platforms",
        action="store_true",
        help="Install every known platform overlay, preserving the historical full-overlay behavior.",
    )
    args = parser.parse_args()

    guru_root = guru_root_from_script()
    if args.version:
        manifest = load_extension_manifest(guru_root)
        print(str(manifest["version"]))
        return 0

    repo = repo_root_from_args(args.repo)
    platforms, all_platforms = selected_platforms(args.platform, args.all_platforms)
    src = guru_root / "trellis/workflows/guru-team"
    dst = repo / ".trellis/guru-team"
    result = install_assets(src, dst, repo, platforms, all_platforms=all_platforms)

    payload: dict[str, Any] = {
        "status": "ok",
        "repo": str(repo),
        "platforms": result["platforms"],
        "all_platforms": result["all_platforms"],
        "installed": result["installed"],
        "unchanged": result["unchanged"],
        "new_copies": result["new_copies"],
        "replaced_overlays": result["replaced_overlays"],
        "updated_managed": result["updated_managed"],
        "managed_backups": result["managed_backups"],
        "codex_dispatch": result["codex_dispatch"],
        "extension_manifest": result["extension_manifest"],
        "guru_team_extension": result["guru_team_extension"],
        "config": ".trellis/guru-team/config.yml",
        "workflow_marketplace": WORKFLOW_MARKETPLACE,
        "public_workflow_marketplace": WORKFLOW_MARKETPLACE,
        "workflow_template": WORKFLOW_TEMPLATE,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
