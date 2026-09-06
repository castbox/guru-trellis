from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
from pathlib import Path
from typing import Any

from runtime.io import CommandError
from runtime.schema import validate_json


INPUT_SCHEMA = "public-restore-input.schema.json"
SEMANTIC_SCHEMA = "semantic-review-input.schema.json"
FACTS_SCHEMA = "live-facts.schema.json"
RESTORED_SCHEMA = "public-restored-output.schema.json"
BLOCKED_SCHEMA = "public-blocked-output.schema.json"

AUTHORITY_FILES = (
    "phase2-check.json",
    "review-gate.json",
    "pr-readiness.json",
    "task-finalization-gate.json",
    "task-finalization-transition-gate.json",
    "finalization-transaction.json",
)

FINISH_SUMMARY = "finish-summary.json"


def _read_json(package_root: Path, root: Path, value: str, field: str) -> dict[str, Any]:
    if value == "-":
        raw = os.sys.stdin.read()
    else:
        candidate = Path(value)
        candidates = [candidate] if candidate.is_absolute() else [root / candidate, package_root / candidate]
        candidate = next((path for path in candidates if path.is_file() and not path.is_symlink()), None)
        if candidate is None:
            raise CommandError("restore_precondition_failed", field, "Provide one existing regular JSON contract file.")
        raw = candidate.read_text(encoding="utf-8")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CommandError("schema_mismatch", field, "Provide one valid JSON object.") from exc
    if not isinstance(payload, dict):
        raise CommandError("schema_mismatch", field, "Provide one valid JSON object.")
    return payload


def _repo_root(value: str | None) -> Path:
    root = Path(value or ".").resolve()
    if not (root / ".git").exists():
        raise CommandError("restore_precondition_failed", "root", "Use a Git repository root.")
    return root


def _reject_symlink_components(root: Path, path: Path, field: str) -> None:
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise CommandError("unsafe_path", field, "Use a path inside the repository root.") from exc
    current = root
    for part in relative.parts:
        current /= part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            break
        except OSError as exc:
            raise CommandError("unsafe_path", field, "The path components could not be inspected.") from exc
        if stat.S_ISLNK(mode):
            raise CommandError("unsafe_path", field, "Do not use symlink-backed task or runtime paths.")


def _safe_task_path(root: Path, locator: str, field: str) -> Path:
    path = Path(locator)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise CommandError("unsafe_path", field, "Use a canonical repository-relative task locator.")
    candidate = root / path
    tasks_root = root / ".trellis" / "tasks"
    if not candidate.is_relative_to(tasks_root):
        raise CommandError("unsafe_path", field, "Use a regular task path below .trellis/tasks.")
    _reject_symlink_components(root, candidate, field)
    return candidate


def _read_regular_json(path: Path, field: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise CommandError("restore_precondition_failed", field, "The required task artifact is missing or unsafe.")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CommandError("restore_precondition_failed", field, "The required task artifact is not valid JSON.") from exc
    if not isinstance(value, dict):
        raise CommandError("restore_precondition_failed", field, "The required task artifact must be an object.")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _blocked(reason_code: str, remediation: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "exit_id": "restore_blocked",
        "reason_code": reason_code,
        "remediation": remediation,
        "zero_writes": True,
    }


def _restored_output(public: dict[str, Any]) -> dict[str, Any]:
    return {
        "exit_id": "restored_to_phase2",
        "task_ref": public["active_locator"],
        "resume_target": "phase-2",
    }


def _matches_identity(public: dict[str, Any], semantic: dict[str, Any], facts: dict[str, Any]) -> str | None:
    if semantic["profile"] != public["profile"] or semantic["mode"] != public["mode"]:
        return "semantic_input_drift"
    if semantic["finding_refs"] != public["finding_refs"]:
        return "scope_drift"
    if semantic["classification"] != "task_work" or not semantic["requires_task_content_change"]:
        return "scope_drift"

    blockers = facts["blockers"]
    if blockers["merged"] or facts["pr"]["state"] == "MERGED":
        return "merged_pr"
    if any(blockers[name] for name in ("provider", "permission", "ruleset", "external_service")):
        return "external_blocker"
    if blockers["scope_drift"]:
        return "scope_drift"
    if blockers["identity_drift"] or blockers["ambiguous"]:
        return "identity_drift"

    expected = {
        "pr.number": (facts["pr"]["number"], public["pr_number"]),
        "pr.url": (facts["pr"]["url"], public["pr_url"]),
        "pr.head_sha": (facts["pr"]["head_sha"], public["expected_head_sha"]),
        "pr.base_branch": (facts["pr"]["base_branch"], public["expected_base_branch"]),
        "pr.head_branch": (facts["pr"]["head_branch"], public["expected_head_branch"]),
        "issue.number": (facts["issue"]["number"], public["issue_number"]),
        "issue.state": (facts["issue"]["state"], "OPEN"),
        "remote_branch.name": (facts["remote_branch"]["name"], public["expected_head_branch"]),
        "remote_branch.head_sha": (facts["remote_branch"]["head_sha"], public["expected_head_sha"]),
        "local_branch.name": (facts["local_branch"]["name"], public["expected_head_branch"]),
        "local_branch.head_sha": (facts["local_branch"]["head_sha"], public["expected_head_sha"]),
        "archive.locator": (facts["archive"]["locator"], public["archive_locator"]),
        "archive.commit": (facts["archive"]["commit"], public["archive_commit"]),
        "task.id": (facts["task"]["id"], public["task_id"]),
        "task.branch": (facts["task"]["branch"], public["expected_head_branch"]),
        "task.base_branch": (facts["task"]["base_branch"], public["expected_base_branch"]),
        "task.repo_ref": (facts["task"]["repo_ref"], public["repo_ref"]),
        "task.issue_number": (facts["task"]["issue_number"], public["issue_number"]),
        "task.pr_number": (facts["task"]["pr_number"], public["pr_number"]),
        "task.expected_head_sha": (facts["task"]["expected_head_sha"], public["expected_head_sha"]),
        "runtime_mapping.task_id": (facts["runtime_mapping"]["task_id"], public["task_id"]),
        "runtime_mapping.archive_locator": (facts["runtime_mapping"]["archive_locator"], public["archive_locator"]),
        "runtime_mapping.active_locator": (facts["runtime_mapping"]["active_locator"], public["active_locator"]),
        "runtime_mapping.repo_ref": (facts["runtime_mapping"]["repo_ref"], public["repo_ref"]),
        "runtime_mapping.branch_name": (facts["runtime_mapping"]["branch_name"], public["expected_head_branch"]),
        "worktree.branch": (facts["worktree"]["branch"], public["expected_head_branch"]),
    }
    for field, (actual, wanted) in expected.items():
        if actual != wanted:
            return "head_drift" if "head" in field or "branch" in field else "identity_drift"
    if facts["issue"]["close_intent"] != "unchanged":
        return "scope_drift"
    if facts["task"]["status"] not in {"completed", "in_progress"}:
        return "archive_conflict"
    if not facts["worktree"]["exists"] or facts["worktree"]["occupied_by"] is not None:
        return "dirty_worktree"
    active = facts["active_task"]
    if active["present"] and active["task_id"] != public["task_id"]:
        return "active_task_conflict"
    return None


def _archive_blob(root: Path, public: dict[str, Any], relative: str) -> bytes | None:
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{public['archive_commit']}:{public['archive_locator']}/{relative}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return result.stdout if result.returncode == 0 else None


def _pending_restore_matches(root: Path, public: dict[str, Any]) -> bool:
    archive = root / public["archive_locator"]
    active = root / public["active_locator"]
    if archive.exists() or not active.is_dir() or active.is_symlink():
        return False
    tracked = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "--name-only", "-z", public["archive_commit"], "--", public["archive_locator"]],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if tracked.returncode:
        return False
    prefix = public["archive_locator"] + "/"
    original_paths = {value.decode()[len(prefix):] for value in tracked.stdout.split(b"\0") if value}
    actual_paths = {path.relative_to(active).as_posix() for path in active.rglob("*") if path.is_file() or path.is_symlink()}
    removable = set(AUTHORITY_FILES) | {FINISH_SUMMARY}
    if not original_paths or actual_paths - original_paths or original_paths - actual_paths - removable:
        return False
    for relative in actual_paths:
        path = active / relative
        original = _archive_blob(root, public, relative)
        if path.is_symlink() or original is None:
            return False
        if relative == "task.json":
            try:
                archived_task = json.loads(original)
                restored_task = dict(archived_task, status="in_progress")
                restored_task.pop("completedAt", None)
                if json.loads(path.read_bytes()) not in (archived_task, restored_task):
                    return False
            except (ValueError, TypeError):
                return False
        elif path.read_bytes() != original:
            return False
    # A lost result may leave exactly the owned move dirty, never unrelated edits.
    for args in (["diff", "--name-only", "-z"], ["diff", "--cached", "--name-only", "-z"], ["ls-files", "--others", "--exclude-standard", "-z"]):
        result = subprocess.run(["git", "-C", str(root), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode or any(
            value and not value.decode().startswith((prefix, public["active_locator"] + "/"))
            for value in result.stdout.split(b"\0")
        ):
            return False
    return True


def _check_actual_worktree(root: Path, facts: dict[str, Any], public: dict[str, Any]) -> str | None:
    worktree = facts["worktree"]
    path = Path(worktree["path"])
    if not path.exists() or not path.is_dir():
        return "dirty_worktree"
    commands = {
        "root": ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        "branch": ["git", "-C", str(path), "branch", "--show-current"],
        "head": ["git", "-C", str(path), "rev-parse", "HEAD"],
        "status": ["git", "-C", str(path), "status", "--porcelain=v1", "--untracked-files=all"],
    }
    results = {
        name: subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for name, command in commands.items()
    }
    if any(result.returncode for result in results.values()):
        return "dirty_worktree"
    try:
        actual_root = Path(results["root"].stdout.strip()).resolve()
    except (OSError, RuntimeError):
        return "dirty_worktree"
    if actual_root != path.resolve() or actual_root != root:
        return "dirty_worktree"
    if results["branch"].stdout.strip() != public["expected_head_branch"]:
        return "head_drift"
    if results["head"].stdout.strip() != public["expected_head_sha"]:
        return "head_drift"
    archive_commit = subprocess.run(
        ["git", "-C", str(path), "cat-file", "-e", f"{public['archive_commit']}^{{commit}}"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    archive_ancestor = subprocess.run(
        ["git", "-C", str(path), "merge-base", "--is-ancestor", public["archive_commit"], public["expected_head_sha"]],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if archive_commit.returncode or archive_ancestor.returncode:
        return "head_drift"
    archive_identity = subprocess.run(
        ["git", "-C", str(path), "log", "-1", "--format=%H", public["expected_head_sha"], "--", f"{public['archive_locator']}/{FINISH_SUMMARY}"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if archive_identity.returncode or archive_identity.stdout.strip() != public["archive_commit"]:
        return "identity_drift"
    if (results["status"].stdout or not worktree["clean"]) and not _pending_restore_matches(root, public):
        return "dirty_worktree"
    return None


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _owner_checkpoint_dirs(root: Path, task_id: str) -> tuple[Path, ...]:
    checkpoints = root / ".trellis" / ".runtime" / "guru-team" / "owner-checkpoints"
    hashed_key = hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:20]
    return checkpoints / task_id, checkpoints / hashed_key


def _authority_paths(root: Path, task_dir: Path, task_id: str) -> tuple[Path, ...]:
    task_paths = tuple(task_dir / name for name in AUTHORITY_FILES)
    checkpoint_paths = tuple(
        checkpoint_dir / name
        for checkpoint_dir in _owner_checkpoint_dirs(root, task_id)
        for name in AUTHORITY_FILES
    )
    return task_paths + checkpoint_paths


def _unsafe_authority_path(root: Path, task_dir: Path, task_id: str) -> bool:
    for path in _authority_paths(root, task_dir, task_id):
        try:
            _reject_symlink_components(root, path, "stale_authority")
        except CommandError:
            return True
        if path.is_symlink() or (path.exists() and not path.is_file()):
            return True
    return False


def _retire_authority(root: Path, task_dir: Path, task_id: str) -> None:
    for path in _authority_paths(root, task_dir, task_id):
        if path.is_file() and not path.is_symlink():
            path.unlink()
    for checkpoint_dir in _owner_checkpoint_dirs(root, task_id):
        try:
            checkpoint_dir.rmdir()
        except OSError:
            pass


def _restore(root: Path, public: dict[str, Any], facts: dict[str, Any]) -> dict[str, Any]:
    archive = _safe_task_path(root, public["archive_locator"], "input.archive_locator")
    active = _safe_task_path(root, public["active_locator"], "input.active_locator")
    if archive == active:
        return _blocked("archive_conflict", "Archive and active task locators must be distinct.")

    mapping_path = root / ".trellis" / ".runtime" / "guru-team" / "tasks" / f"{public['task_id']}.json"
    _reject_symlink_components(root, mapping_path, "runtime_mapping")
    mapping = _read_regular_json(mapping_path, "runtime_mapping")
    archive_exists = archive.exists()
    active_exists = active.exists()
    if archive_exists and not archive.is_dir():
        return _blocked("archive_conflict", "The archived task locator is not a directory.")
    if active_exists and not active.is_dir():
        return _blocked("active_task_conflict", "The active task locator is occupied by a non-directory.")
    if archive_exists and active_exists:
        return _blocked("archive_conflict", "Both archive and active task locators exist; no move is safe.")
    if not archive_exists and not active_exists:
        return _blocked("archive_missing", "Restore requires either the exact archive or an exact already-restored task.")

    task_dir = archive if archive_exists else active
    workspace_slug = mapping.get("workspace_slug")
    if not isinstance(workspace_slug, str) or not workspace_slug or Path(workspace_slug).name != workspace_slug:
        return _blocked("identity_drift", "The existing task mapping lacks its workspace identity.")
    workspace_mapping_path = mapping_path.parent.parent / "workspaces" / f"{workspace_slug}.json"
    _reject_symlink_components(root, workspace_mapping_path, "runtime_mapping")
    workspace_mapping = _read_regular_json(workspace_mapping_path, "runtime_mapping")
    mapping_identity = {"schema_version": "1.0", "task_slug": public["task_id"], "workspace_path": str(root)}
    workspace_identity = {"schema_version": "1.0", "workspace_slug": workspace_slug, "workspace_path": str(root), "branch_name": public["expected_head_branch"]}
    # Finalizer keeps the original active locator in its disposable task mapping.
    allowed_locators = {public["active_locator"], public["archive_locator"]}
    if (
        any(mapping.get(key) != value for key, value in mapping_identity.items())
        or any(workspace_mapping.get(key) != value for key, value in workspace_identity.items())
        or mapping.get("task_artifact_dir") not in allowed_locators
        or facts["runtime_mapping"]["worktree_path"] != str(root)
    ):
        return _blocked("identity_drift", "The task and workspace mappings do not match the current checkout identity.")
    task_path = task_dir / "task.json"
    finish_summary_path = task_dir / "finish-summary.json"
    task = _read_regular_json(task_path, "task.json")
    if task.get("id") != public["task_id"] or task.get("branch") != public["expected_head_branch"] or task.get("base_branch") != public["expected_base_branch"]:
        return _blocked("identity_drift", "The task.json identity does not match the recovery input.")
    if task.get("status") not in {"completed", "in_progress"} or (task.get("status") == "completed" and not task.get("completedAt")):
        return _blocked("archive_conflict", "The task is neither a valid archived task nor a recoverable interrupted restore.")
    if archive_exists or task.get("status") == "completed" or finish_summary_path.exists():
        finish_summary = _read_regular_json(finish_summary_path, "finish-summary.json")
        summary_task = finish_summary.get("task", {})
        summary_git = finish_summary.get("git", {})
        summary_github = finish_summary.get("github", {})
        if not all(isinstance(value, dict) for value in (summary_task, summary_git, summary_github)):
            return _blocked("identity_drift", "The finish summary lacks the Finalizer identity projection.")
        if (
            summary_task.get("slug") != archive.name
            or summary_task.get("artifact_dir") != public["active_locator"]
            or summary_task.get("archive_dir") != public["archive_locator"]
            or summary_task.get("status") != "completed"
            or summary_git.get("branch") != public["expected_head_branch"]
            or summary_git.get("base_branch") != public["expected_base_branch"]
            or summary_github.get("pr_url") != public["pr_url"]
            or public["issue_number"] not in [number for key in ("source_issues", "close_issues", "related_issues", "followup_issues") for number in summary_github.get(key, [])]
        ):
            return _blocked("identity_drift", "The finish summary does not match the immutable recovery identity.")
        committed_summary = _archive_blob(root, public, FINISH_SUMMARY)
        if committed_summary is None:
            return _blocked("head_drift", "The archive commit is unavailable from the current task worktree.")
        if committed_summary != finish_summary_path.read_bytes():
            return _blocked("identity_drift", "The finish summary differs from the committed archive.")
        if archive_exists and (facts["archive"]["task_json_sha256"] != _sha256(task_path) or facts["archive"]["finish_summary_sha256"] != _sha256(finish_summary_path)):
            return _blocked("identity_drift", "Archive artifact content changed from the fresh fact snapshot.")
        if archive_exists:
            committed_task = _archive_blob(root, public, "task.json")
            if committed_task is None:
                return _blocked("head_drift", "The archive commit is unavailable from the current task worktree.")
            if committed_task != task_path.read_bytes():
                return _blocked("identity_drift", "The task differs from the committed archive.")

    if archive_exists and task.get("status") != "completed":
        return _blocked("archive_conflict", "An archived task must still have completed status before the move.")
    if not archive_exists and task.get("status") == "completed" and facts["runtime_mapping"]["state"] == "active":
        return _blocked("identity_drift", "The active task status and mapping disagree during recovery.")

    if facts["runtime_mapping"]["state"] == "active" and archive_exists:
        return _blocked("archive_conflict", "The runtime mapping is active while the archive still exists.")
    if facts["runtime_mapping"]["state"] not in {"archived", "active"}:
        return _blocked("identity_drift", "The runtime mapping state is not recoverable.")

    if _unsafe_authority_path(root, task_dir, public["task_id"]):
        return _blocked("identity_drift", "A stale authority path is not a regular file and cannot be safely retired.")

    current_task = root / ".trellis" / ".runtime" / "current-task"
    _reject_symlink_components(root, current_task, "current_task")
    if current_task.is_symlink() or (current_task.exists() and not current_task.is_file()):
        return _blocked("active_task_conflict", "The current task pointer is not a regular file.")
    current_task_value = current_task.read_text(encoding="utf-8").strip() if current_task.is_file() else ""
    if current_task_value not in {"", public["active_locator"]}:
        return _blocked("active_task_conflict", "The current task pointer belongs to a different task.")

    if reason := _check_actual_worktree(root, facts, public):
        return _blocked(reason, "Restore the original clean task worktree or refresh the recovery facts.")

    if not archive_exists and task.get("status") == "in_progress" and facts["runtime_mapping"]["state"] == "active":
        old_authority_absent = not any(path.exists() or path.is_symlink() for path in _authority_paths(root, active, public["task_id"]))
        if current_task_value == public["active_locator"] and old_authority_absent and not finish_summary_path.exists():
            return _restored_output(public)

    if archive_exists:
        shutil.move(str(archive), str(active))
        task_dir = active
        task_path = active / "task.json"

    task["status"] = "in_progress"
    task.pop("completedAt", None)
    _write_json(task_path, task)

    repaired_mapping = dict(mapping)
    repaired_mapping["task_artifact_dir"] = public["active_locator"]
    _write_json(mapping_path, repaired_mapping)

    current_task.parent.mkdir(parents=True, exist_ok=True)
    current_task.write_text(public["active_locator"] + "\n", encoding="utf-8")

    _retire_authority(root, task_dir, public["task_id"])
    finish_summary = task_dir / FINISH_SUMMARY
    if finish_summary.is_file() and not finish_summary.is_symlink():
        finish_summary.unlink()

    return _restored_output(public)


def run(package_root: Path, command: dict[str, Any], argv: list[str]) -> dict[str, Any]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    parser.add_argument("--facts", required=True)
    args = parser.parse_args(argv)
    root = _repo_root(args.root)
    public = _read_json(package_root, root, args.input, "input")
    semantic = _read_json(package_root, root, args.semantic_result, "semantic_result")
    facts = _read_json(package_root, root, args.facts, "facts")
    validate_json(public, package_root / "schemas" / INPUT_SCHEMA, "input")
    validate_json(semantic, package_root / "schemas" / SEMANTIC_SCHEMA, "semantic_result")
    validate_json(facts, package_root / "schemas" / FACTS_SCHEMA, "facts")

    reason = _matches_identity(public, semantic, facts)
    if reason:
        output = _blocked(reason, "Resolve the current blocker and rerun the recovery from fresh identity facts.")
    else:
        output = _restore(root, public, facts)
    schema = RESTORED_SCHEMA if output["exit_id"] == "restored_to_phase2" else BLOCKED_SCHEMA
    validate_json(output, package_root / "schemas" / schema, "stdout")
    return output
