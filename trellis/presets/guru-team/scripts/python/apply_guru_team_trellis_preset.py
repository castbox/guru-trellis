#!/usr/bin/env python3
"""Apply Guru team Trellis companion assets to a project repository."""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import os
import stat
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_MODULE_DIR = Path(__file__).resolve().parent
if str(SCRIPT_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_MODULE_DIR))

from validate_upstream_ownership import validate_repository as validate_upstream_ownership_repository


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
SKILL_DESTINATION_PLATFORM_ORDER = ("shared", "codex", "claude", "cursor")
ALWAYS_OVERLAY_PREFIXES = (Path(".agents"), Path(".trellis/agents"))
CODEX_ONLY_SHARED_OVERLAY_PREFIXES = (Path(".agents/skills/trellis-meta"),)
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
    Path("schemas/task-start-context.schema.json"),
    Path("schemas/closeout-plan.schema.json"),
    Path("schemas/finish-summary.schema.json"),
    Path("schemas/marketplace-verification.schema.json"),
    Path("scripts/bash/check-env.sh"),
    Path("scripts/bash/version.sh"),
    Path("scripts/bash/prepare-task.sh"),
    Path("scripts/bash/check-workspace-boundary.sh"),
    Path("scripts/bash/check-skill-packages.sh"),
    Path("scripts/bash/run-skill-command.sh"),
    Path("scripts/bash/sync-base.sh"),
    Path("scripts/bash/check-base-sync.sh"),
    Path("scripts/bash/preview-change-context-history.sh"),
    Path("scripts/bash/record-context-discovery.sh"),
    Path("scripts/bash/check-context-discovery.sh"),
    Path("scripts/bash/record-requirements-clarification.sh"),
    Path("scripts/bash/check-requirements-clarification.sh"),
    Path("scripts/bash/record-contract-wording-review.sh"),
    Path("scripts/bash/check-contract-wording-review.sh"),
    Path("scripts/bash/resolve-human-artifacts.sh"),
    Path("scripts/bash/verify-marketplace.sh"),
    Path("scripts/bash/record-planning-approval.sh"),
    Path("scripts/bash/check-planning-approval.sh"),
    Path("scripts/bash/record-phase2-check.sh"),
    Path("scripts/bash/check-phase2-check.sh"),
    Path("scripts/bash/record-agent-assignment.sh"),
    Path("scripts/bash/check-agent-assignment.sh"),
    Path("scripts/bash/record-subagent-liveness-event.sh"),
    Path("scripts/bash/check-subagent-liveness.sh"),
    Path("scripts/bash/check-commit-messages.sh"),
    Path("scripts/bash/create-task-commit.sh"),
    Path("scripts/bash/format-merge-commit.sh"),
    Path("scripts/bash/review-branch.sh"),
    Path("scripts/bash/check-review-gate.sh"),
    Path("scripts/bash/publish-pr.sh"),
    Path("scripts/bash/finish-work.sh"),
    Path("scripts/bash/backfill-finish-summary.sh"),
    Path("scripts/python/guru_team_trellis.py"),
]
OBSOLETE_MANAGED_ASSETS = {
    Path("handoff.json"): set(),
    Path("schemas/intake-handoff.schema.json"): {
        "6d9484b82ea7e71b4661035f370d8b21240aa1af844dfa131c1131bba1c3dcfc"
    },
}
ENGLISH_LANGUAGE_RULES = (
    "**Language**: All documentation must be written in **English**.",
    "**Language**: All documentation should be written in **English**.",
)
CHINESE_LANGUAGE_RULE = (
    "**Language**: 业务项目人类可读文档默认使用**中文**；"
    "命令、路径、代码符号、配置键、GitHub keyword 等 literal token 可保留英文。"
)
RUNTIME_GITIGNORE_MARKER = "# Guru Team local runtime cache"
RUNTIME_GITIGNORE_RULE = ".trellis/.runtime/"
WORKSPACE_GITIGNORE_MARKER = "# Guru Team excludes upstream workspace journals"
WORKSPACE_GITIGNORE_RULE = ".trellis/workspace/"
SESSION_AUTO_COMMIT_HEADER = """# Guru Team owns archive and finish-summary metadata commits.
# Keep official task.py/add_session.py bookkeeping from committing implicitly.
"""


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


def run_upstream_ownership_validator(guru_root: Path) -> dict[str, Any]:
    payload = validate_upstream_ownership_repository(guru_root)
    if payload.get("status") != "ok":
        first_error = next(iter(payload.get("errors") or []), {})
        code = str(first_error.get("code") or "ownership_validation_failed")
        path = str(first_error.get("path") or "unknown")
        raise SystemExit(
            "Canonical upstream ownership validation failed before preset mutation: "
            f"{code} {path}"
        )
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
    tested = manifest.get("tested") if isinstance(manifest.get("tested"), dict) else {}
    return {
        "extension_id": manifest.get("extension_id"),
        "version": manifest.get("version"),
        "workflow_template_id": manifest.get("workflow_template_id"),
        "target_trellis_cli": manifest.get("target_trellis_cli"),
        "trellis_cli_compatibility": requires.get("trellis_cli"),
        "tested_trellis_cli": tested.get("trellis_cli") if isinstance(tested.get("trellis_cli"), list) else [],
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
        (set(result["installed"]) - {".trellis/guru-team/config.yml"})
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
        "skill_packages": result["skill_packages"],
        "notes": (
            "This file records deterministic install provenance for the Guru Team Trellis extension. "
            "source.commit and source.tree_state describe the extension source observed at apply time; "
            "they are not a claim that this installed manifest is contained in that commit. "
            "Upgrade and rollback judgment belongs to AI/human review."
        ),
    }


def write_installed_extension_manifest(dst: Path, payload: dict[str, Any]) -> str:
    path = dst / "extension.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path.name


def ensure_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | 0o755)


def load_previous_installed_manifest(dst: Path) -> dict[str, Any] | None:
    path = dst / "extension.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def previous_skill_hashes(
    manifest: dict[str, Any] | None,
) -> tuple[dict[str, str], set[str], bool, set[str]]:
    if manifest is None:
        return {}, set(), True, set()
    skill_packages = manifest.get("skill_packages")
    if skill_packages is None:
        return {}, set(), True, set()
    required_fields = {
        "schema_version", "status", "canonical_registry_sha256", "registry_schema_version",
        "reserved_ids", "active_ids", "selected_platforms", "packages", "files", "removals",
        "conflicts", "sidecars",
    }
    if (
        not isinstance(skill_packages, dict)
        or set(skill_packages) != required_fields
        or skill_packages.get("schema_version") != "1.0"
        or not isinstance(skill_packages.get("packages"), list)
        or not isinstance(skill_packages.get("removals"), list)
    ):
        return {}, set(), False, set()
    status = skill_packages.get("status")
    conflicts = skill_packages.get("conflicts")
    sidecars = skill_packages.get("sidecars")
    clean = status == "ok" and conflicts == [] and sidecars == []
    recovering_backups = (
        status == "conflict"
        and conflicts == []
        and isinstance(sidecars, list)
        and bool(sidecars)
    )
    if not clean and not recovering_backups:
        return {}, set(), False, set()
    files = skill_packages.get("files")
    if not isinstance(files, list):
        return {}, set(), False, set()
    hashes: dict[str, str] = {}
    paths: set[str] = set()
    valid = True
    for item in files:
        if not isinstance(item, dict):
            valid = False
            continue
        path = item.get("path")
        digest = item.get("sha256")
        if (
            not isinstance(path, str)
            or not path
            or path.startswith("/")
            or ".." in Path(path).parts
            or path in paths
        ):
            valid = False
            continue
        paths.add(path)
        if not isinstance(digest, str) or not re_full_hex_digest(digest):
            valid = False
            continue
        hashes[path] = digest
    recoverable_sidecars: set[str] = set()
    if recovering_backups:
        for sidecar in sidecars:
            relative = Path(sidecar) if isinstance(sidecar, str) else None
            if (
                relative is None
                or not sidecar.endswith(".bak")
                or sidecar.startswith("/")
                or ".." in relative.parts
                or relative.as_posix() != sidecar
                or sidecar in recoverable_sidecars
                or sidecar[:-4] not in paths
            ):
                valid = False
                continue
            recoverable_sidecars.add(sidecar)
    return hashes, paths, valid, recoverable_sidecars


def re_full_hex_digest(value: str) -> bool:
    return len(value) == 64 and all(ch in "0123456789abcdef" for ch in value)


def lexical_repo_relative(repo: Path, target: Path) -> Path:
    repo_abs = Path(os.path.abspath(repo))
    target_abs = Path(os.path.abspath(target))
    try:
        relative = target_abs.relative_to(repo_abs)
    except ValueError as exc:
        raise ValueError("target is outside the repository boundary") from exc
    if not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        raise ValueError("target has an unsafe repository-relative path")
    return relative


def lstat_repo_path(repo: Path, target: Path) -> tuple[Path, os.stat_result | None, str | None]:
    try:
        relative = lexical_repo_relative(repo, target)
    except ValueError as exc:
        return Path(), None, str(exc)
    current = Path(os.path.abspath(repo))
    for index, part in enumerate(relative.parts):
        current /= part
        try:
            current_stat = current.lstat()
        except FileNotFoundError:
            return relative, None, None
        except OSError:
            return relative, None, "path component cannot be inspected"
        if stat.S_ISLNK(current_stat.st_mode):
            return relative, current_stat, "path contains a symlink component"
        if index < len(relative.parts) - 1 and not stat.S_ISDIR(current_stat.st_mode):
            return relative, current_stat, "path ancestor is not a directory"
    return relative, current_stat, None


def ensure_safe_repo_parents(repo: Path, target: Path) -> Path:
    relative = lexical_repo_relative(repo, target)
    current = Path(os.path.abspath(repo))
    for part in relative.parts[:-1]:
        current /= part
        try:
            current_stat = current.lstat()
        except FileNotFoundError:
            current.mkdir(mode=0o755)
            current_stat = current.lstat()
        if stat.S_ISLNK(current_stat.st_mode) or not stat.S_ISDIR(current_stat.st_mode):
            raise ValueError("target ancestor is not a real directory")
    return relative


def write_safe_repo_file(repo: Path, path: Path, content: bytes, mode: int) -> None:
    ensure_safe_repo_parents(repo, path)
    _, current_stat, error = lstat_repo_path(repo, path)
    if error:
        raise ValueError(error)
    if current_stat is not None and not stat.S_ISREG(current_stat.st_mode):
        raise ValueError("target is not a regular file")
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, mode)
    with os.fdopen(fd, "wb") as handle:
        handle.write(content)
    path.chmod(mode)


def skill_conflict(
    path: str,
    reason: str,
    *,
    sidecar: str | None = None,
    previous_managed_sha256: str | None = None,
) -> dict[str, Any]:
    payload = {
        "path": path,
        "reason": reason,
        "remediation": "Review the preserved local path and sidecar, then remove the conflict before reapplying the preset.",
    }
    if sidecar:
        payload["sidecar"] = sidecar
    if previous_managed_sha256:
        payload["previous_managed_sha256"] = previous_managed_sha256
    return payload


def copy_skill_managed(
    source: Path,
    target: Path,
    repo: Path,
    previous_hashes: dict[str, str],
    provenance_valid: bool,
) -> dict[str, Any]:
    try:
        relative_path = lexical_repo_relative(repo, target)
    except ValueError:
        return {"action": "conflict", "path": "<outside-repo>", "reason": "outside_repo_boundary"}
    relative = relative_path.as_posix()
    canonical = source.read_bytes()
    canonical_hash = hashlib.sha256(canonical).hexdigest()
    executable = bool(source.stat().st_mode & 0o100)
    target_mode = 0o755 if executable else 0o644

    def write_target(path: Path, content: bytes) -> None:
        write_safe_repo_file(repo, path, content, target_mode)

    _, target_stat, target_error = lstat_repo_path(repo, target)
    if target_error:
        return {"action": "conflict", "path": relative, "reason": "unsafe_path_boundary"}
    if target_stat is None:
        try:
            write_target(target, canonical)
        except ValueError:
            return {"action": "conflict", "path": relative, "reason": "unsafe_path_boundary"}
        return {"action": "installed", "path": relative, "sha256": canonical_hash, "executable": executable}
    if not stat.S_ISREG(target_stat.st_mode):
        sidecar = target.with_name(f"{target.name}.new")
        try:
            write_target(sidecar, canonical)
            sidecar_path = lexical_repo_relative(repo, sidecar).as_posix()
        except ValueError:
            sidecar_path = None
        return {
            "action": "conflict", "path": relative, "sha256": canonical_hash,
            "executable": executable, "sidecar": sidecar_path,
            "reason": "target_not_regular_file",
        }
    current = target.read_bytes()
    current_hash = hashlib.sha256(current).hexdigest()
    if current_hash == canonical_hash:
        if stat.S_IMODE(target_stat.st_mode) != target_mode:
            target.chmod(target_mode)
        return {"action": "unchanged", "path": relative, "sha256": canonical_hash, "executable": executable}
    previous_hash = previous_hashes.get(relative)
    if provenance_valid and previous_hash and current_hash == previous_hash:
        backup = target.with_name(f"{target.name}.bak")
        try:
            write_safe_repo_file(repo, backup, current, target_stat.st_mode & 0o777)
            write_target(target, canonical)
        except ValueError:
            return {"action": "conflict", "path": relative, "reason": "unsafe_sidecar_boundary"}
        return {
            "action": "updated_managed", "path": relative, "sha256": canonical_hash,
            "executable": executable, "sidecar": backup.relative_to(repo).as_posix(),
            "previous_managed_sha256": previous_hash,
        }
    sidecar = target.with_name(f"{target.name}.new")
    try:
        write_target(sidecar, canonical)
    except ValueError:
        return {"action": "conflict", "path": relative, "reason": "unsafe_sidecar_boundary"}
    return {
        "action": "conflict", "path": relative, "sha256": canonical_hash,
        "executable": executable, "sidecar": sidecar.relative_to(repo).as_posix(),
        "reason": "unknown_local_edit" if provenance_valid else "invalid_provenance",
        "previous_managed_sha256": previous_hash,
    }


def skill_registry_entries(skills_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    try:
        registry = json.loads((skills_root / "registry.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit("Canonical Guru Team skill registry is missing or invalid.") from exc
    if not isinstance(registry, dict) or not isinstance(registry.get("skills"), list):
        raise SystemExit("Canonical Guru Team skill registry has an invalid structure.")
    entries = [entry for entry in registry["skills"] if isinstance(entry, dict)]
    if len(entries) != len(registry["skills"]):
        raise SystemExit("Canonical Guru Team skill registry contains a non-object entry.")
    return registry, entries


SKILL_MANAGED_ROOTS = (
    Path(".trellis/guru-team/skills"),
    Path(".agents/skills"),
    Path(".codex/skills"),
    Path(".cursor/skills"),
    Path(".claude/skills"),
)


def skill_path_is_managed(relative: Path) -> bool:
    return any(relative == root or root in relative.parents for root in SKILL_MANAGED_ROOTS)


def prune_empty_managed_skill_parents(repo: Path, path: Path) -> None:
    relative = lexical_repo_relative(repo, path)
    managed_root = next((root for root in SKILL_MANAGED_ROOTS if root in relative.parents), None)
    if managed_root is None:
        return
    current = path.parent
    stop = Path(os.path.abspath(repo)) / managed_root
    while current != stop and stop in current.parents:
        _, current_stat, error = lstat_repo_path(repo, current)
        if error or current_stat is None or not stat.S_ISDIR(current_stat.st_mode):
            return
        try:
            current.rmdir()
        except OSError:
            return
        current = current.parent


def remove_stale_skill_path(
    repo: Path,
    relative_text: str,
    previous_hashes: dict[str, str],
    provenance_valid: bool,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, str | None]:
    relative = Path(relative_text)
    if not skill_path_is_managed(relative):
        return None, skill_conflict(relative_text, "previous_path_outside_skill_roots"), None
    target = Path(os.path.abspath(repo)) / relative
    checked_relative, target_stat, error = lstat_repo_path(repo, target)
    if error or checked_relative != relative:
        return None, skill_conflict(relative_text, "unsafe_stale_path_boundary"), None
    if target_stat is None:
        return {"path": relative_text, "action": "already_missing"}, None, None
    if not stat.S_ISREG(target_stat.st_mode):
        return None, skill_conflict(relative_text, "stale_target_not_regular_file"), None
    current_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    previous_hash = previous_hashes.get(relative_text)
    if provenance_valid and previous_hash and current_hash == previous_hash:
        target.unlink()
        prune_empty_managed_skill_parents(repo, target)
        return {
            "path": relative_text,
            "action": "removed_managed",
            "previous_managed_sha256": previous_hash,
        }, None, None
    sidecar = target.with_name(f"{target.name}.new")
    tombstone = (
        "Guru Team managed removal requested. Review the adjacent preserved local file, "
        "remove it or migrate its content, then delete this sidecar and reapply the preset.\n"
    ).encode("utf-8")
    try:
        write_safe_repo_file(repo, sidecar, tombstone, 0o644)
        sidecar_relative = lexical_repo_relative(repo, sidecar).as_posix()
    except ValueError:
        sidecar_relative = None
    reason = "stale_unknown_local_edit" if provenance_valid else "stale_invalid_provenance"
    return None, skill_conflict(
        relative_text,
        reason,
        sidecar=sidecar_relative,
        previous_managed_sha256=previous_hash,
    ), sidecar_relative


def run_skill_package_validator(
    repo: Path,
    guru_root: Path,
    mode: str,
) -> dict[str, Any]:
    runtime = guru_root / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py"
    proc = subprocess.run(
        [sys.executable, str(runtime), "check-skill-packages", "--json", "--mode", mode, "--root", str(repo)],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    raw = proc.stdout if proc.returncode == 0 else proc.stderr
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        payload = {"status": "failed", "mode": mode, "facts": {}, "errors": ["skill package validator returned invalid JSON"]}
    if not isinstance(payload, dict):
        payload = {"status": "failed", "mode": mode, "facts": {}, "errors": ["skill package validator returned a non-object payload"]}
    payload["returncode"] = proc.returncode
    return payload


def skill_package_source_files(package_root: Path) -> list[Path]:
    return sorted(
        path
        for path in package_root.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and "__pycache__" not in path.relative_to(package_root).parts
        and path.suffix not in {".pyc", ".pyo"}
    )


def install_skill_packages(
    repo: Path,
    guru_root: Path,
    dst: Path,
    platforms: set[str],
    previous_manifest: dict[str, Any] | None,
) -> dict[str, Any]:
    canonical_root = guru_root / "trellis/skills/guru-team"
    registry, entries = skill_registry_entries(canonical_root)
    previous_hash_map, previous_paths, provenance_valid, recoverable_sidecars = previous_skill_hashes(
        previous_manifest
    )
    pending_recovery_sidecars: list[str] = []
    if provenance_valid:
        for sidecar_text in sorted(recoverable_sidecars):
            sidecar = Path(os.path.abspath(repo)) / Path(sidecar_text)
            checked_relative, sidecar_stat, sidecar_error = lstat_repo_path(repo, sidecar)
            if (
                sidecar_error
                or checked_relative.as_posix() != sidecar_text
                or (sidecar_stat is not None and not stat.S_ISREG(sidecar_stat.st_mode))
            ):
                provenance_valid = False
                pending_recovery_sidecars = []
                break
            if sidecar_stat is not None:
                pending_recovery_sidecars.append(sidecar_text)
    active_entries = [entry for entry in entries if entry.get("state") == "active"]
    reserved_ids = sorted(str(entry.get("id")) for entry in entries if entry.get("state") == "reserved")
    active_ids = sorted(str(entry.get("id")) for entry in active_entries)
    source_files: list[tuple[Path, Path]] = [
        (canonical_root / "registry.json", Path("registry.json")),
        (canonical_root / "schemas/skill-registry.schema.json", Path("schemas/skill-registry.schema.json")),
        (canonical_root / "schemas/skill-interface.schema.json", Path("schemas/skill-interface.schema.json")),
    ]
    packages: list[dict[str, Any]] = []
    for entry in active_entries:
        skill_id = str(entry["id"])
        package_root = canonical_root / str(entry["package"])
        package_files = skill_package_source_files(package_root)
        for source in package_files:
            source_files.append((source, source.relative_to(canonical_root)))
        interface_path = canonical_root / str(entry["interface"])
        tree_hash = hashlib.sha256()
        for source in package_files:
            rel = source.relative_to(package_root).as_posix()
            tree_hash.update(rel.encode("utf-8") + b"\0" + source.read_bytes() + b"\0")
        packages.append({
            "id": skill_id,
            "interface_sha256": hashlib.sha256(interface_path.read_bytes()).hexdigest(),
            "tree_sha256": tree_hash.hexdigest(),
        })

    records: list[dict[str, Any]] = []
    removals: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    sidecars: list[str] = list(pending_recovery_sidecars)

    if not provenance_valid:
        conflicts.append(skill_conflict(
            ".trellis/guru-team/extension.json",
            "invalid_previous_provenance",
        ))

    def install_one(source: Path, target: Path) -> None:
        result = copy_skill_managed(source, target, repo, previous_hash_map, provenance_valid)
        if result["action"] == "conflict":
            sidecar = result.get("sidecar")
            conflict = skill_conflict(
                result["path"],
                str(result.get("reason") or "skill_install_conflict"),
                sidecar=str(sidecar) if sidecar else None,
                previous_managed_sha256=result.get("previous_managed_sha256"),
            )
            conflicts.append(conflict)
            if sidecar:
                sidecars.append(str(sidecar))
            return
        record = {
            "path": result["path"],
            "source": source.relative_to(guru_root).as_posix(),
            "sha256": result["sha256"],
            "executable": result["executable"],
            "action": result["action"],
        }
        records.append(record)
        if result.get("sidecar"):
            sidecars.append(str(result["sidecar"]))

    desired_files: list[tuple[Path, Path]] = []
    installed_root = dst / "skills"
    for source, relative in source_files:
        desired_files.append((source, installed_root / relative))

    destination_roots = [
        (
            platform,
            Path(".agents/skills")
            if platform == "shared"
            else PLATFORM_OVERLAY_PREFIXES[platform][0] / "skills",
        )
        for platform in SKILL_DESTINATION_PLATFORM_ORDER
        if platform == "shared" or platform in platforms
    ]
    for entry in active_entries:
        skill_id = str(entry["id"])
        supported = set(entry.get("supported_platforms") or [])
        package_root = canonical_root / str(entry["package"])
        package_files = skill_package_source_files(package_root)
        for platform, target_root in destination_roots:
            if platform not in supported:
                continue
            for source in package_files:
                desired_files.append((source, repo / target_root / skill_id / source.relative_to(package_root)))

    desired_paths = {
        lexical_repo_relative(repo, target).as_posix()
        for _, target in desired_files
    }
    for source, target in desired_files:
        install_one(source, target)
    for stale_path in sorted(previous_paths - desired_paths):
        removal, conflict, sidecar = remove_stale_skill_path(
            repo,
            stale_path,
            previous_hash_map,
            provenance_valid,
        )
        if removal:
            removals.append(removal)
        if conflict:
            conflicts.append(conflict)
        if sidecar:
            sidecars.append(sidecar)

    status = "ok" if provenance_valid and not conflicts and not sidecars else "conflict"
    return {
        "schema_version": "1.0",
        "status": status,
        "canonical_registry_sha256": hashlib.sha256((canonical_root / "registry.json").read_bytes()).hexdigest(),
        "registry_schema_version": registry.get("schema_version"),
        "reserved_ids": reserved_ids,
        "active_ids": active_ids,
        "selected_platforms": sorted(platforms),
        "packages": packages,
        "files": records,
        "removals": removals,
        "conflicts": conflicts,
        "sidecars": sorted(sidecars),
    }


def ensure_runtime_gitignore(repo: Path) -> dict[str, str]:
    path = repo / ".gitignore"
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = original.splitlines()
    if RUNTIME_GITIGNORE_RULE in {line.strip() for line in lines}:
        return {"action": "unchanged", "path": ".gitignore", "rule": RUNTIME_GITIGNORE_RULE}
    separator = "" if not original or original.endswith("\n\n") else ("\n" if original.endswith("\n") else "\n\n")
    path.write_text(f"{original}{separator}{RUNTIME_GITIGNORE_MARKER}\n{RUNTIME_GITIGNORE_RULE}\n", encoding="utf-8")
    return {"action": "updated" if original else "installed", "path": ".gitignore", "rule": RUNTIME_GITIGNORE_RULE}


def ensure_workspace_gitignore(repo: Path) -> dict[str, str]:
    path = repo / ".gitignore"
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    if WORKSPACE_GITIGNORE_RULE in {line.strip() for line in original.splitlines()}:
        return {"action": "unchanged", "path": ".gitignore", "rule": WORKSPACE_GITIGNORE_RULE}
    separator = "" if not original or original.endswith("\n\n") else ("\n" if original.endswith("\n") else "\n\n")
    path.write_text(
        f"{original}{separator}{WORKSPACE_GITIGNORE_MARKER}\n{WORKSPACE_GITIGNORE_RULE}\n",
        encoding="utf-8",
    )
    return {"action": "updated" if original else "installed", "path": ".gitignore", "rule": WORKSPACE_GITIGNORE_RULE}


def ensure_session_auto_commit_false(repo: Path) -> dict[str, str | None]:
    path = repo / ".trellis/config.yaml"
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = original.splitlines()
    active_indexes: list[int] = []
    previous: str | None = None
    for index, line in enumerate(lines):
        if line.startswith("session_auto_commit:"):
            active_indexes.append(index)
            if previous is None:
                previous = strip_inline_comment(line.split(":", 1)[1]) or None
    if len(active_indexes) > 1:
        raise SystemExit(".trellis/config.yaml contains duplicate top-level session_auto_commit keys")
    if active_indexes and previous == "false":
        return {"action": "unchanged", "path": ".trellis/config.yaml", "previous": "false", "value": "false"}
    if active_indexes:
        lines[active_indexes[0]] = "session_auto_commit: false"
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        return {"action": "updated", "path": ".trellis/config.yaml", "previous": previous, "value": "false"}
    separator = "" if not original else ("\n" if original.endswith("\n") else "\n\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"{original}{separator}{SESSION_AUTO_COMMIT_HEADER}session_auto_commit: false\n",
        encoding="utf-8",
    )
    return {"action": "updated" if original else "installed", "path": ".trellis/config.yaml", "previous": None, "value": "false"}


def path_has_prefix(path: Path, prefix: Path) -> bool:
    return path == prefix or prefix in path.parents


def overlay_selected(relative: Path, platforms: set[str]) -> bool:
    if any(path_has_prefix(relative, prefix) for prefix in CODEX_ONLY_SHARED_OVERLAY_PREFIXES):
        return "codex" in platforms
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

    is_trellis_agent = (
        rel.startswith(".codex/agents/trellis-")
        or rel.startswith(".cursor/agents/trellis-")
        or rel.startswith(".claude/agents/trellis-")
        or rel in {".trellis/agents/implement.md", ".trellis/agents/check.md"}
    )
    if is_trellis_agent and any(
        signal in text
        for signal in [
            "Required: Load Trellis Context First",
            "Recursion Guard",
            "Trellis workflow",
            "Trellis channel",
            "implement.jsonl",
            "check.jsonl",
            "{TASK_DIR}/research",
            "Workspace-write Trellis",
        ]
    ):
        return True

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

    is_brainstorm_skill = rel in {
        ".agents/skills/trellis-brainstorm/SKILL.md",
        ".cursor/skills/trellis-brainstorm/SKILL.md",
    }
    if (
        is_brainstorm_skill
        and "# Trellis Brainstorm" in text
        and ("PRD Convergence Pass" in text or "trellis-brainstorm" in lower)
    ):
        return True

    is_check_or_before_dev_skill = rel in {
        ".agents/skills/trellis-check/SKILL.md",
        ".cursor/skills/trellis-check/SKILL.md",
        ".agents/skills/trellis-before-dev/SKILL.md",
        ".cursor/skills/trellis-before-dev/SKILL.md",
    }
    if (
        is_check_or_before_dev_skill
        and ("# Code Quality Check" in text or "Read the relevant development guidelines" in text)
        and "prd.md" in text
    ):
        return True

    is_session_start_hook = rel in {
        ".codex/hooks/session-start.py",
        ".cursor/hooks/session-start.py",
    }
    if (
        is_session_start_hook
        and "session" in lower
        and "trellis" in lower
        and "_get_task_status" in text
    ):
        return True

    is_cursor_subagent_context_hook = rel == ".cursor/hooks/inject-subagent-context.py"
    if (
        is_cursor_subagent_context_hook
        and "Multi-Platform Sub-Agent Context Injection Hook" in text
        and "implement.jsonl" in text
        and "check.jsonl" in text
    ):
        return True

    is_trellis_meta_reference = rel in {
        ".agents/skills/trellis-meta/references/local-architecture/task-system.md",
        ".cursor/skills/trellis-meta/references/local-architecture/task-system.md",
        ".agents/skills/trellis-meta/references/local-architecture/context-injection.md",
        ".cursor/skills/trellis-meta/references/local-architecture/context-injection.md",
        ".agents/skills/trellis-meta/references/customize-local/change-workflow.md",
        ".cursor/skills/trellis-meta/references/customize-local/change-workflow.md",
        ".agents/skills/trellis-meta/references/customize-local/change-context-loading.md",
        ".cursor/skills/trellis-meta/references/customize-local/change-context-loading.md",
        ".agents/skills/trellis-meta/references/platform-files/agents.md",
        ".cursor/skills/trellis-meta/references/platform-files/agents.md",
    }
    has_trellis_meta_reference_signal = any(
        signal in text
        for signal in [
            "# Local Task System",
            "# Local Context Injection System",
            "# Change Local Workflow",
            "# Change Local Context Loading",
            "# Change Context Loading",
            "# Agents",
        ]
    ) and any(
        signal in text
        for signal in [
            ".trellis/tasks/",
            ".trellis/workflow.md",
            "trellis-implement",
        ]
    )
    if (
        is_trellis_meta_reference
        and has_trellis_meta_reference_signal
    ):
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


def language_guidance_targets(repo: Path) -> list[Path]:
    targets: set[Path] = set()
    spec_root = repo / ".trellis/spec"
    if spec_root.is_dir():
        targets.update(path for path in spec_root.rglob("*.md") if path.is_file())

    bootstrap_root = repo / ".trellis/tasks/00-bootstrap-guidelines"
    if bootstrap_root.is_dir():
        targets.update(path for path in bootstrap_root.rglob("*.md") if path.is_file())

    return sorted(targets)


def normalize_business_doc_language_guidance(repo: Path) -> dict[str, Any]:
    checked_paths: list[str] = []
    updated_paths: list[dict[str, Any]] = []
    replacement_count = 0

    for path in language_guidance_targets(repo):
        rel_path = path.relative_to(repo).as_posix()
        checked_paths.append(rel_path)
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        updated = original
        path_replacements = 0
        for english_rule in ENGLISH_LANGUAGE_RULES:
            occurrences = updated.count(english_rule)
            if occurrences:
                updated = updated.replace(english_rule, CHINESE_LANGUAGE_RULE)
                path_replacements += occurrences

        if path_replacements:
            path.write_text(updated, encoding="utf-8")
            replacement_count += path_replacements
            updated_paths.append({"path": rel_path, "replacements": path_replacements})

    return {
        "action": "updated" if replacement_count else "checked",
        "rule": "business-project-human-readable-docs-default-chinese",
        "replacement": CHINESE_LANGUAGE_RULE,
        "checked_paths": checked_paths,
        "updated_paths": updated_paths,
        "replacement_count": replacement_count,
        "scope": [
            ".trellis/spec/**/*.md",
            ".trellis/tasks/00-bootstrap-guidelines/**/*.md",
        ],
    }


def install_assets(
    src: Path,
    dst: Path,
    repo: Path,
    platforms: set[str] | None = None,
    all_platforms: bool = False,
) -> dict[str, Any]:
    if not src.is_dir():
        raise SystemExit(f"Missing source directory: {src}")

    guru_root = guru_root_from_script()
    upstream_ownership_validation = run_upstream_ownership_validator(guru_root)
    source_validation = run_skill_package_validator(guru_root, guru_root, "source")
    if source_validation.get("returncode") != 0:
        raise SystemExit("Canonical Guru Team skill package validation failed before preset mutation.")
    previous_manifest = load_previous_installed_manifest(dst)
    dst.mkdir(parents=True, exist_ok=True)

    installed: list[str] = []
    unchanged: list[str] = []
    new_copies: list[str] = []
    replaced_overlays: list[str] = []
    updated_managed: list[str] = []
    managed_backups: list[str] = []
    removed_obsolete: list[str] = []
    obsolete_conflicts: list[str] = []
    for relative, managed_hashes in OBSOLETE_MANAGED_ASSETS.items():
        target = dst / relative
        repo_relative_path = target.relative_to(repo).as_posix()
        if not target.exists():
            continue
        digest = __import__("hashlib").sha256(target.read_bytes()).hexdigest()
        tracked_clean = False
        if not managed_hashes:
            tracked = run_git(["ls-files", "--error-unmatch", repo_relative_path], repo)
            changed = run_git(["diff", "--quiet", "HEAD", "--", repo_relative_path], repo)
            tracked_clean = tracked.returncode == 0 and changed.returncode == 0
        if digest in managed_hashes or tracked_clean:
            target.unlink()
            removed_obsolete.append(repo_relative_path)
        else:
            obsolete_conflicts.append(repo_relative_path)
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
        dst / "scripts/bash/check-workspace-boundary.sh",
        dst / "scripts/bash/check-skill-packages.sh",
        dst / "scripts/bash/run-skill-command.sh",
        dst / "scripts/bash/sync-base.sh",
        dst / "scripts/bash/check-base-sync.sh",
        dst / "scripts/bash/preview-change-context-history.sh",
        dst / "scripts/bash/record-context-discovery.sh",
        dst / "scripts/bash/check-context-discovery.sh",
        dst / "scripts/bash/record-requirements-clarification.sh",
        dst / "scripts/bash/check-requirements-clarification.sh",
        dst / "scripts/bash/record-contract-wording-review.sh",
        dst / "scripts/bash/check-contract-wording-review.sh",
        dst / "scripts/bash/resolve-human-artifacts.sh",
        dst / "scripts/bash/verify-marketplace.sh",
        dst / "scripts/bash/record-planning-approval.sh",
        dst / "scripts/bash/check-planning-approval.sh",
        dst / "scripts/bash/record-phase2-check.sh",
        dst / "scripts/bash/check-phase2-check.sh",
        dst / "scripts/bash/record-agent-assignment.sh",
        dst / "scripts/bash/check-agent-assignment.sh",
        dst / "scripts/bash/record-subagent-liveness-event.sh",
        dst / "scripts/bash/check-subagent-liveness.sh",
        dst / "scripts/bash/check-commit-messages.sh",
        dst / "scripts/bash/create-task-commit.sh",
        dst / "scripts/bash/format-merge-commit.sh",
        dst / "scripts/bash/review-branch.sh",
        dst / "scripts/bash/check-review-gate.sh",
        dst / "scripts/bash/publish-pr.sh",
        dst / "scripts/bash/finish-work.sh",
        dst / "scripts/bash/backfill-finish-summary.sh",
        dst / "scripts/python/guru_team_trellis.py",
    ]:
        if script.exists():
            ensure_executable(script)

    selected = platforms or set(DEFAULT_PLATFORMS)
    skill_packages = install_skill_packages(repo, guru_root, dst, selected, previous_manifest)
    overlays = install_overlays(repo, guru_root, selected)
    installed.extend(overlays["installed"])
    unchanged.extend(overlays["unchanged"])
    new_copies.extend(overlays["new_copies"])
    replaced_overlays.extend(overlays["replaced_overlays"])
    updated_managed.extend(overlays["updated_managed"])
    managed_backups.extend(overlays["managed_backups"])
    codex_dispatch = ensure_codex_dispatch_mode(repo)
    session_auto_commit = ensure_session_auto_commit_false(repo)
    runtime_gitignore = ensure_runtime_gitignore(repo)
    workspace_gitignore = ensure_workspace_gitignore(repo)
    language_guidance = normalize_business_doc_language_guidance(repo)

    result = {
        "installed": installed,
        "unchanged": unchanged,
        "new_copies": new_copies,
        "replaced_overlays": replaced_overlays,
        "updated_managed": updated_managed,
        "managed_backups": managed_backups,
        "removed_obsolete": removed_obsolete,
        "obsolete_conflicts": obsolete_conflicts,
        "codex_dispatch": codex_dispatch,
        "session_auto_commit": session_auto_commit,
        "runtime_gitignore": runtime_gitignore,
        "workspace_gitignore": workspace_gitignore,
        "language_guidance": language_guidance,
        "platforms": sorted(selected),
        "all_platforms": all_platforms,
        "skill_packages": skill_packages,
        "skill_source_validation": source_validation,
        "upstream_ownership_validation": upstream_ownership_validation,
    }
    manifest = load_extension_manifest(guru_root)
    source = source_provenance(guru_root)
    installed_manifest = build_installed_extension_manifest(manifest, source, result)
    write_installed_extension_manifest(dst, installed_manifest)
    rel_extension = (dst / "extension.json").relative_to(repo).as_posix()
    result["extension_manifest"] = rel_extension
    result["guru_team_extension"] = extension_summary(manifest, source)
    result["skill_installed_validation"] = run_skill_package_validator(repo, guru_root, "installed")
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
        if "__pycache__" in source.parts or source.suffix == ".pyc":
            continue
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
        "session_auto_commit": result["session_auto_commit"],
        "runtime_gitignore": result["runtime_gitignore"],
        "workspace_gitignore": result["workspace_gitignore"],
        "language_guidance": result["language_guidance"],
        "extension_manifest": result["extension_manifest"],
        "guru_team_extension": result["guru_team_extension"],
        "skill_packages": result["skill_packages"],
        "skill_source_validation": result["skill_source_validation"],
        "upstream_ownership_validation": result["upstream_ownership_validation"],
        "skill_installed_validation": result["skill_installed_validation"],
        "config": ".trellis/guru-team/config.yml",
        "workflow_marketplace": WORKFLOW_MARKETPLACE,
        "public_workflow_marketplace": WORKFLOW_MARKETPLACE,
        "workflow_template": WORKFLOW_TEMPLATE,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if (
        result["skill_packages"]["status"] != "ok"
        or result["skill_installed_validation"].get("returncode") != 0
    ):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
