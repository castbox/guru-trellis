from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json


def load(root: Path, package_root: Path, value: str, field: str) -> dict:
    path = Path(value)
    choices = [path] if path.is_absolute() else [root / path, package_root / path]
    source = next((candidate for candidate in choices if candidate.is_file() and not candidate.is_symlink()), None)
    if source is None:
        raise CommandError("invalid_json", field, "Provide one regular JSON file.")
    try:
        payload = json.loads(source.read_text())
    except json.JSONDecodeError as exc:
        raise CommandError("invalid_json", field, "Provide valid JSON.") from exc
    if not isinstance(payload, dict):
        raise CommandError("invalid_json", field, "Provide one object.")
    return payload


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode:
        raise CommandError("stale_identity", "workspace", proc.stderr.strip() or "Refresh the reviewed workspace facts.", 3)
    return proc


def worktrees(root: Path) -> dict[Path, dict[str, str]]:
    rows: dict[Path, dict[str, str]] = {}
    current: dict[str, str] = {}
    for line in git(root, "worktree", "list", "--porcelain").stdout.splitlines() + [""]:
        if not line:
            if "worktree" in current:
                rows[Path(current["worktree"]).resolve()] = current
            current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    return rows


def write_mapping(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def invalidate_finish_receipts(root: Path, task_ref: str) -> None:
    receipts = root / ".trellis/.runtime/guru-team/finish"
    if not receipts.is_dir():
        return
    for receipt in receipts.glob("*.json"):
        try:
            data = json.loads(receipt.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("task_ref") == task_ref:
            receipt.unlink()


def invalidate_cleanup_receipts(root: Path, task_ref: str) -> None:
    receipts = root / ".trellis/.runtime/guru-team/cleanup"
    if not receipts.is_dir():
        return
    for receipt in receipts.glob("*.json"):
        try:
            data = json.loads(receipt.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("task_ref") == task_ref:
            receipt.unlink()


def has_finish_receipt(root: Path, task_ref: str) -> bool:
    receipts = root / ".trellis/.runtime/guru-team/finish"
    if not receipts.is_dir():
        return False
    for receipt in receipts.glob("*.json"):
        try:
            data = json.loads(receipt.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("task_ref") == task_ref:
            return True
    return False


def has_cleanup_receipt(root: Path, task_ref: str) -> bool:
    receipts = root / ".trellis/.runtime/guru-team/cleanup"
    if not receipts.is_dir():
        return False
    for receipt in receipts.glob("*.json"):
        try:
            data = json.loads(receipt.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("task_ref") == task_ref:
            return True
    return False


def read_runtime_json(path: Path, field: str) -> dict:
    if not path.is_file() or path.is_symlink():
        raise CommandError("stale_identity", field, "The completed reactivation state is incomplete.", 3)
    try:
        payload = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("stale_identity", field, "The completed reactivation state is invalid.", 3) from exc
    if not isinstance(payload, dict):
        raise CommandError("stale_identity", field, "The completed reactivation state is invalid.", 3)
    return payload


def validate_recovery_mapping(path: Path, expected: dict, field: str) -> dict:
    payload = read_runtime_json(path, field)
    if set(payload) != {*expected, "updated_at"} or any(payload.get(key) != value for key, value in expected.items()):
        raise CommandError("stale_identity", field, "The completed reactivation mapping no longer matches this input.", 3)
    if not isinstance(payload.get("updated_at"), str) or not payload["updated_at"]:
        raise CommandError("stale_identity", field, "The completed reactivation mapping is missing its update time.", 3)
    return payload


def validate_task_identity(public: dict, plan: dict) -> None:
    task_id = public["task_id"]
    task_basename = Path(public["task_ref"]).name
    archive_basename = Path(public["archive_ref"]).name
    if task_basename != archive_basename:
        raise CommandError("stale_identity", "archive_ref", "Reactivate task and archive locators must use the same basename.", 3)
    mappings = {
        "workspace.workspace_mapping": Path(plan["workspace_mapping"]).stem,
        "workspace.task_mapping": Path(plan["task_mapping"]).stem,
    }
    for field, mapping_id in mappings.items():
        if mapping_id != task_id:
            raise CommandError("stale_identity", field, "Reactivate mappings must bind the exact task id.", 3)


def recover_completed_reactivation(root: Path, public: dict, plan: dict) -> int | None:
    workspace = Path(plan["workspace_path"]).resolve()
    branch_ref = f"refs/heads/{plan['branch_name']}"
    listed = worktrees(root)
    row = listed.get(workspace)
    branch_probe = git(root, "show-ref", "--verify", "--quiet", branch_ref, check=False)
    if plan["disposition"] == "create_new" and branch_probe.returncode and not workspace.exists() and row is None:
        return None
    if not workspace.is_dir() or row is None or row.get("branch") != branch_ref or branch_probe.returncode:
        if plan["disposition"] == "reuse_exact":
            return False
        raise CommandError("stale_identity", "workspace", "The completed reactivation workspace no longer matches this input.", 3)

    archive = workspace / public["archive_ref"]
    active = workspace / public["task_ref"]
    if archive.is_dir() and not archive.is_symlink() and not active.exists():
        return None
    if archive.exists() or not active.is_dir() or active.is_symlink():
        raise CommandError("stale_identity", "archive_ref", "The completed reactivation task state is incomplete or conflicting.", 3)
    if git(workspace, "branch", "--show-current").stdout.strip() != plan["branch_name"]:
        raise CommandError("stale_identity", "workspace.branch_name", "The completed reactivation branch changed.", 3)
    if git(workspace, "rev-parse", "HEAD").stdout.strip() != plan["base_head"]:
        raise CommandError("stale_identity", "workspace.base_head", "The completed reactivation workspace moved from the reviewed base.", 3)

    task = read_runtime_json(active / "task.json", "task_ref")
    generation = task.get("lifecycle_generation")
    if not isinstance(generation, int) or generation < 1:
        raise CommandError("stale_identity", "task_ref.lifecycle_generation", "The completed reactivation cycle identity is missing.", 3)
    expected_task = {
        "id": public["task_id"],
        "status": "in_progress",
        "completedAt": None,
        "branch": plan["branch_name"],
        "base_branch": plan["base_branch"],
        "worktree_path": str(workspace),
        "lifecycle_generation": generation,
    }
    if any(task.get(key) != value for key, value in expected_task.items()) or "archive_dir" in task:
        raise CommandError("stale_identity", "task_ref", "The completed reactivation task metadata no longer matches this input.", 3)

    workspace_expected = {
        "schema_version": "1.0",
        "workspace_slug": public["task_id"],
        "workspace_path": str(workspace),
        "source_checkout": str(root),
        "branch_name": plan["branch_name"],
        "lifecycle_generation": generation,
    }
    task_expected = {
        "schema_version": "1.0",
        "task_slug": public["task_id"],
        "workspace_slug": public["task_id"],
        "workspace_path": str(workspace),
        "task_artifact_dir": public["task_ref"],
        "lifecycle_generation": generation,
    }
    mapping_roots = {root.resolve(), workspace.resolve()}
    workspace_mappings = [
        validate_recovery_mapping(mapping_root / plan["workspace_mapping"], workspace_expected, "workspace.workspace_mapping")
        for mapping_root in mapping_roots
    ]
    task_mappings = [
        validate_recovery_mapping(mapping_root / plan["task_mapping"], task_expected, "workspace.task_mapping")
        for mapping_root in mapping_roots
    ]
    if any(payload != workspace_mappings[0] for payload in workspace_mappings[1:]) or any(
        payload != task_mappings[0] for payload in task_mappings[1:]
    ):
        raise CommandError("stale_identity", "workspace", "The completed reactivation mappings disagree.", 3)
    if workspace_mappings[0]["updated_at"] != task_mappings[0]["updated_at"]:
        raise CommandError("stale_identity", "workspace", "The completed reactivation mappings come from different writes.", 3)
    if any(has_finish_receipt(mapping_root, public["task_ref"]) for mapping_root in mapping_roots):
        raise CommandError("stale_identity", "task_ref", "The prior Finish receipt was not fully invalidated.", 3)
    if any(has_cleanup_receipt(mapping_root, public["task_ref"]) for mapping_root in mapping_roots):
        raise CommandError("stale_identity", "task_ref", "The prior Cleanup receipt was not fully invalidated.", 3)
    return generation


def prepare_workspace(root: Path, plan: dict) -> tuple[Path, bool, bool]:
    workspace = Path(plan["workspace_path"]).resolve()
    branch = plan["branch_name"]
    base_head = plan["base_head"]
    if branch == plan["base_branch"]:
        raise CommandError("stale_identity", "workspace.branch_name", "Reactivate must not bind the task to the target base branch.", 3)
    git(root, "fetch", "--no-tags", "origin", f"refs/heads/{plan['base_branch']}:refs/remotes/origin/{plan['base_branch']}")
    live_base = git(root, "rev-parse", f"refs/remotes/origin/{plan['base_branch']}", check=False)
    if live_base.returncode or live_base.stdout.strip() != base_head:
        raise CommandError("stale_identity", "workspace.base_head", "Fetch and review the current target baseline before reactivation.", 3)
    branch_ref = f"refs/heads/{branch}"
    branch_probe = git(root, "show-ref", "--verify", "--quiet", branch_ref, check=False)
    listed = worktrees(root)
    row = listed.get(workspace)
    created_branch = False
    created_worktree = False
    if plan["disposition"] == "create_new":
        if branch_probe.returncode == 0 or workspace.exists() or row is not None:
            raise CommandError("stale_identity", "workspace.disposition", "The reviewed branch or worktree already exists.", 3)
        git(root, "worktree", "add", "-b", branch, str(workspace), base_head)
        created_branch = True
        created_worktree = True
    else:
        if branch_probe.returncode:
            raise CommandError("stale_identity", "workspace.branch_name", "The reviewed reusable branch does not exist.", 3)
        if not workspace.is_dir() or row is None or row.get("branch") != branch_ref:
            raise CommandError("stale_identity", "workspace.workspace_path", "The reviewed reusable worktree is not registered for the exact branch.", 3)
        if git(workspace, "branch", "--show-current").stdout.strip() != branch:
            raise CommandError("stale_identity", "workspace.branch_name", "The selected worktree is not on the reviewed branch.", 3)
        if git(workspace, "status", "--porcelain=v1", "--untracked-files=all").stdout:
            raise CommandError("stale_identity", "workspace.workspace_path", "The selected worktree is not clean before reactivation.", 3)
        branch_head = git(workspace, "rev-parse", "HEAD").stdout.strip()
        if branch_head != base_head:
            if git(workspace, "merge-base", "--is-ancestor", branch_head, base_head, check=False).returncode:
                raise CommandError("stale_identity", "workspace.branch_name", "The reusable branch cannot fast-forward to the reviewed target baseline.", 3)
            git(workspace, "merge", "--ff-only", base_head)
            if git(workspace, "rev-parse", "HEAD").stdout.strip() != base_head:
                raise CommandError("stale_identity", "workspace.branch_name", "The reusable branch did not reach the reviewed target baseline.", 3)
    if git(workspace, "branch", "--show-current").stdout.strip() != branch:
        raise CommandError("stale_identity", "workspace.branch_name", "The selected worktree is not on the reviewed branch.", 3)
    if git(workspace, "status", "--porcelain=v1", "--untracked-files=all").stdout:
        raise CommandError("stale_identity", "workspace.workspace_path", "The selected worktree is not clean before reactivation.", 3)
    return workspace, created_branch, created_worktree


def rollback_workspace(root: Path, workspace: Path, branch: str, created_branch: bool, created_worktree: bool) -> None:
    if created_worktree:
        git(root, "worktree", "remove", "--force", str(workspace), check=False)
    if created_branch:
        git(root, "branch", "-D", branch, check=False)


def reactivate(root: Path, public: dict, semantic: dict) -> int:
    plan = semantic["workspace"]
    validate_task_identity(public, plan)
    if plan["branch_name"] == plan["base_branch"]:
        raise CommandError("stale_identity", "workspace.branch_name", "Reactivate must not bind the task to the target base branch.", 3)
    recovered_generation = recover_completed_reactivation(root, public, plan)
    if recovered_generation is not None:
        return recovered_generation
    workspace, created_branch, created_worktree = prepare_workspace(root, plan)
    archive = workspace / public["archive_ref"]
    active = workspace / public["task_ref"]
    try:
        if not archive.is_dir() or archive.is_symlink() or active.exists():
            raise CommandError("stale_identity", "archive_ref", "Archive identity or active target is not unique on the selected baseline.", 3)
        task_path = archive / "task.json"
        if not task_path.is_file() or task_path.is_symlink():
            raise CommandError("stale_identity", "archive_ref", "Archived task metadata is missing or unsafe.", 3)
        task = json.loads(task_path.read_text())
        if task.get("id") != public["task_id"] or task.get("status") != "completed":
            raise CommandError("stale_identity", "archive_ref", "Archived task is not the exact normally completed identity.", 3)
        active.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(archive), str(active))
        task_path = active / "task.json"
        generation = task.get("lifecycle_generation", 0)
        if not isinstance(generation, int) or generation < 0:
            raise CommandError("stale_identity", "archive_ref.task.json.lifecycle_generation", "Archived task lifecycle generation is invalid.", 3)
        task.update({"status": "in_progress", "completedAt": None, "branch": plan["branch_name"], "base_branch": plan["base_branch"], "worktree_path": str(workspace), "lifecycle_generation": generation + 1})
        task.pop("archive_dir", None)
        task_path.write_text(json.dumps(task, ensure_ascii=False, indent=2) + "\n")
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        workspace_payload = {"schema_version": "1.0", "workspace_slug": public["task_id"], "workspace_path": str(workspace), "source_checkout": str(root), "branch_name": plan["branch_name"], "lifecycle_generation": task["lifecycle_generation"], "updated_at": now}
        task_payload = {"schema_version": "1.0", "task_slug": public["task_id"], "workspace_slug": public["task_id"], "workspace_path": str(workspace), "task_artifact_dir": public["task_ref"], "lifecycle_generation": task["lifecycle_generation"], "updated_at": now}
        for mapping_root in {root.resolve(), workspace.resolve()}:
            write_mapping(mapping_root / plan["workspace_mapping"], workspace_payload)
            write_mapping(mapping_root / plan["task_mapping"], task_payload)
        invalidate_finish_receipts(root, public["task_ref"])
        invalidate_cleanup_receipts(root, public["task_ref"])
        if workspace != root:
            invalidate_finish_receipts(workspace, public["task_ref"])
            invalidate_cleanup_receipts(workspace, public["task_ref"])
        return task["lifecycle_generation"]
    except Exception:
        rollback_workspace(root, workspace, plan["branch_name"], created_branch, created_worktree)
        raise


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    parser.add_argument("--confirmed-reactivation", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the reactivation command contract.") from exc
    root = Path(args.root or ".").resolve()
    public = load(root, package_root, args.input, "input")
    semantic = load(root, package_root, args.semantic_result, "semantic_result")
    validate_json(public, package_root / "schemas/public-input.schema.json", "input")
    validate_json(semantic, package_root / "schemas/semantic-result.schema.json", "semantic_result")
    if public["profile"] != semantic["profile"] or public["mode"] != semantic["mode"]:
        raise CommandError("stale_identity", "semantic_result", "Reactivate identity differs.", 3)
    route = semantic["route"]
    out = {"exit_id": route["typed_exit"]}
    if route["typed_exit"] != "reactivate_blocked":
        if not args.confirmed_reactivation:
            raise CommandError("confirmation_required", "confirmed_reactivation", "Confirm the reviewed archive, target baseline, branch, worktree, binding and file plan.", 4)
        generation = reactivate(root, public, semantic)
        out.update({"task_ref":public["task_ref"], "resume_target":{"reactivated_to_requirements": "requirements", "reactivated_to_planning": "planning", "reactivated_to_implementation": "phase-2", "reactivated_to_evidence_refresh": "evidence-refresh"}[route["typed_exit"]], "lifecycle_generation": generation})
    validate_json(out, package_root / "schemas/public-output.schema.json", "stdout")
    return out


if __name__ == "__main__":
    try:
        print(json.dumps(run(Path(__file__).parents[1], {}, sys.argv[1:]), ensure_ascii=False))
    except CommandError as exc:
        print(json.dumps({"code": exc.code, "field_path": exc.field_path, "remediation": exc.remediation}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(exc.exit_status)
