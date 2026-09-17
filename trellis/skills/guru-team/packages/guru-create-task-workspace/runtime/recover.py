from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from common import git, parse, root
from runtime.io import CommandError
from runtime.schema import validate_json


def _json_command(argv: list[str], cwd: Path, field: str) -> dict:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode:
        raise CommandError(
            "stale_identity",
            field,
            completed.stderr.strip() or f"Revalidate {field} before recovery.",
            3,
        )
    try:
        value = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise CommandError("invalid_json", field, f"{field} did not return JSON.") from exc
    if not isinstance(value, dict):
        raise CommandError("invalid_json", field, f"{field} did not return one JSON object.")
    return value


def _read_json(path: Path, field: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("stale_identity", field, f"Reread the exact {field}.", 3) from exc
    if not isinstance(value, dict):
        raise CommandError("stale_identity", field, f"Reread the exact {field}.", 3)
    return value


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--task", required=True)
    args = parse(parser, argv)
    repo = root(package_root, args.root)

    task_ref = Path(args.task)
    if task_ref.is_absolute() or ".." in task_ref.parts or task_ref.parts[:2] != (".trellis", "tasks"):
        raise CommandError("unsafe_path", "task", "Use one repository-relative .trellis/tasks task path.")
    task_dir = (repo / task_ref).resolve()
    if repo not in task_dir.parents:
        raise CommandError("unsafe_path", "task", "Use a task inside the current repository checkout.")

    boundary = repo / ".trellis/guru-team/scripts/bash/check-workspace-boundary.sh"
    task_cli = repo / ".trellis/scripts/task.py"
    if not boundary.is_file() or not task_cli.is_file():
        raise CommandError(
            "stale_identity",
            "runtime",
            "Install the complete Guru Team preset and official Trellis task runtime.",
            3,
        )

    boundary_result = _json_command(
        [str(boundary), "--root", str(repo), "--task", task_ref.as_posix(), "--json"],
        repo,
        "workspace_boundary",
    )
    if boundary_result.get("status") != "ok":
        raise CommandError("stale_identity", "workspace_boundary", "Workspace boundary is not current.", 3)

    current = _json_command(
        ["python3", str(task_cli), "current", "--json"],
        repo,
        "current_task",
    )
    current_task = current.get("current_task")
    if current.get("stale") is not False or not isinstance(current_task, dict):
        raise CommandError("stale_identity", "current_task", "Resolve one exact current-session task.", 3)
    if current_task.get("dir") != task_ref.as_posix():
        raise CommandError("stale_identity", "current_task", "The current-session task does not match the recovery input.", 3)

    task = _read_json(task_dir / "task.json", "task identity")
    if task.get("status") != "planning":
        raise CommandError("stale_identity", "task.status", "Created-result recovery requires the exact planning task.", 3)
    task_id = task.get("id")
    branch = task.get("branch")
    if not isinstance(task_id, str) or not task_id or not isinstance(branch, str) or not branch:
        raise CommandError("stale_identity", "task identity", "Task id and branch are required for recovery.", 3)
    if Path(str(task.get("worktree_path", ""))).expanduser().resolve() != repo:
        raise CommandError("stale_identity", "task.worktree_path", "Task worktree does not match the current checkout.", 3)
    if git(repo, "branch", "--show-current").stdout.strip() != branch:
        raise CommandError("stale_identity", "task.branch", "Task branch does not match the current checkout.", 3)

    task_mapping = _read_json(
        repo / ".trellis/.runtime/guru-team/tasks" / f"{task_id}.json",
        "task runtime mapping",
    )
    workspace_slug = task_mapping.get("workspace_slug")
    if (
        task_mapping.get("task_slug") != task_id
        or task_mapping.get("workspace_path") != str(repo)
        or task_mapping.get("task_artifact_dir") != task_ref.as_posix()
        or not isinstance(workspace_slug, str)
        or not workspace_slug
    ):
        raise CommandError("stale_identity", "task runtime mapping", "Task runtime mapping identity drifted.", 3)

    workspace_mapping = _read_json(
        repo / ".trellis/.runtime/guru-team/workspaces" / f"{workspace_slug}.json",
        "workspace runtime mapping",
    )
    if (
        workspace_mapping.get("workspace_slug") != workspace_slug
        or workspace_mapping.get("workspace_path") != str(repo)
        or workspace_mapping.get("branch_name") != branch
    ):
        raise CommandError("stale_identity", "workspace runtime mapping", "Workspace runtime mapping identity drifted.", 3)

    result = {
        "schema_version": "1.0",
        "skill_id": "guru-create-task-workspace",
        "task_ref": task_ref.as_posix(),
        "status": "passed",
        "typed_exit": "created",
    }
    validate_json(result, package_root / "schemas/task-workspace-recovery-result.schema.json", "stdout")
    return result
