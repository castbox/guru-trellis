from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError
from runtime.schema import validate_json

PROFILE_ROUTES = {"resume_current_task": "resume", "rebind_missing_session": "rebind", "switch_task": "switch", "reactivate_rebind": "reactivate", "manual_recovery": "manual_recovery"}

EXITS = {
    "resume": "session_resumed",
    "rebind": "session_rebound",
    "switch": "task_switched",
    "reactivate": "reactivate_rebound",
    "manual_recovery": "session_manually_recovered",
}
TASK_REF_RE = re.compile(r"^\.trellis/tasks(?:/|$)")


def load_json(value: str, field: str) -> dict[str, Any]:
    if value == "-":
        value = sys.stdin.read()
    elif isinstance(value, str) and Path(value).is_file():
        value = Path(value).read_text()
    try:
        data = json.loads(value)
    except Exception as exc:
        raise CommandError("invalid_json", field, "Provide one JSON object.") from exc
    if not isinstance(data, dict):
        raise CommandError("invalid_json", field, "Provide one JSON object.")
    return data


def active_module(root: Path):
    init = root / ".trellis/scripts/common/__init__.py"
    if not init.is_file():
        raise CommandError("stale_identity", "session_identity", "Official Trellis session resolver is unavailable.", 3)
    spec = importlib.util.spec_from_file_location(
        "guru_bind_target_common", init, submodule_search_locations=[str(init.parent)]
    )
    if spec is None or spec.loader is None:
        raise CommandError("stale_identity", "session_identity", "Session resolver cannot be loaded.", 3)
    module = importlib.util.module_from_spec(spec)
    sys.modules["guru_bind_target_common"] = module
    spec.loader.exec_module(module)
    return module


def session_id(module) -> str:
    key = module.resolve_context_key()
    if not key:
        raise CommandError("stale_identity", "session_identity", "Current session identity is unavailable.", 3)
    return key


def _git(root: Path, *args: str) -> str:
    process = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)
    if process.returncode:
        raise CommandError("stale_identity", "git", "Live Git identity could not be read.", 3)
    return process.stdout.strip()


def _safe_path(path: Path, root: Path, field: str) -> Path:
    path = path.expanduser().resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise CommandError("stale_identity", field, "Path escapes the reviewed repository.", 3) from exc
    current = root.resolve()
    for part in path.relative_to(current).parts:
        current = current / part
        if current.is_symlink():
            raise CommandError("stale_identity", field, "Binding path contains a symlink.", 3)
    return path


def _repo_common_dir(path: Path) -> Path:
    raw = Path(_git(path, "rev-parse", "--git-common-dir"))
    return (path / raw if not raw.is_absolute() else raw).resolve()


def _repo_root(path: Path) -> Path:
    return Path(_git(path, "rev-parse", "--show-toplevel")).resolve()


def _worktree_paths(root: Path) -> list[Path]:
    output = _git(root, "worktree", "list", "--porcelain")
    paths: list[Path] = []
    for line in output.splitlines():
        if line.startswith("worktree "):
            paths.append(Path(line.removeprefix("worktree ")).resolve())
    return paths


def _mapping_path(base: Path, category: str, task_id: str) -> Path:
    return base / ".trellis/.runtime/guru-team" / category / f"{task_id}.json"


def _read_mapping(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text())
    except Exception as exc:
        raise CommandError("stale_identity", "runtime_mapping", f"Invalid runtime mapping: {path}", 3) from exc
    if not isinstance(value, dict):
        raise CommandError("stale_identity", "runtime_mapping", f"Invalid runtime mapping: {path}", 3)
    return value


def _task_ref(value: str) -> str:
    if not isinstance(value, str) or not TASK_REF_RE.match(value.rstrip("/")) or ".." in Path(value).parts:
        raise CommandError("stale_identity", "task_ref", "Task reference must be a repository-relative .trellis/tasks path.", 3)
    return value.rstrip("/")


def _candidate_task_paths(root: Path, task_ref: str, manual: bool) -> list[tuple[Path, Path]]:
    task_ref = _task_ref(task_ref)
    task_id = Path(task_ref).name
    roots: set[Path] = {root.resolve()}
    try:
        roots.update(_worktree_paths(root))
    except CommandError:
        pass
    mapped_workspaces: set[Path] = set()
    for candidate_root in list(roots):
        metadata_id = None
        meta_locator = candidate_root / task_ref / "task.json"
        if meta_locator.is_file():
            try:
                metadata = json.loads(meta_locator.read_text())
            except Exception as exc:
                raise CommandError("stale_identity", "task.json", "Task metadata is not valid JSON.", 3) from exc
            metadata_id = str(metadata.get("id") or "") or None
            workspace = metadata.get("worktree_path") or (metadata.get("meta") or {}).get("worktree_path")
            if workspace:
                roots.add(Path(str(workspace)).expanduser().resolve())
        mapping_ids = [task_id] if metadata_id is None else [task_id, metadata_id]
        for mapping_id in dict.fromkeys(mapping_ids):
            for category in ("tasks", "workspaces"):
                mapping = _read_mapping(_mapping_path(candidate_root, category, mapping_id))
                if mapping and mapping.get("workspace_path"):
                    mapped_workspaces.add(Path(str(mapping["workspace_path"])).expanduser().resolve())
    if len(mapped_workspaces) > 1:
        raise CommandError("stale_identity", "runtime_mapping", "Multiple runtime mappings point at different task workspaces.", 3)
    if mapped_workspaces:
        roots = set(mapped_workspaces)
    candidates: list[tuple[Path, Path]] = []
    for candidate_root in roots:
        task_path = (candidate_root / task_ref).resolve()
        if (task_path / "task.json").is_file():
            candidates.append((candidate_root, task_path))
    dedup: dict[str, tuple[Path, Path]] = {str(task_path): (candidate_root, task_path) for candidate_root, task_path in candidates}
    if not dedup:
        raise CommandError("stale_identity", "task_ref", "Task artifact cannot be discovered from current checkout, worktrees, or metadata locators.", 3)
    if len(dedup) != 1:
        raise CommandError("stale_identity", "task_ref", "Multiple task artifacts match the requested identity.", 3)
    return list(dedup.values())


def task_facts(root: Path, task_ref: str, allow_missing_mappings: bool = False) -> dict[str, Any]:
    root = _repo_root(root)
    common_dir = _repo_common_dir(root)
    _, task_path = _candidate_task_paths(root, task_ref, allow_missing_mappings)[0]
    task_ref = _task_ref(task_ref)
    try:
        task = json.loads((task_path / "task.json").read_text())
    except Exception as exc:
        raise CommandError("stale_identity", "task.json", "Official task identity is unavailable.", 3) from exc
    if not isinstance(task, dict) or not task.get("id") or task.get("status") not in {"planning", "in_progress"}:
        raise CommandError("stale_identity", "task.json", "Task identity or lifecycle status is invalid.", 3)
    if task_path.name != task["id"] and not task_path.name.endswith(str(task["id"])):
        raise CommandError("stale_identity", "task.json.id", "Task artifact directory does not match task identity.", 3)
    workspace_value = task.get("worktree_path") or (task.get("meta") or {}).get("worktree_path")
    if not workspace_value:
        raise CommandError("stale_identity", "task.json.worktree_path", "Task workspace locator is missing.", 3)
    workspace = Path(str(workspace_value)).expanduser().resolve()
    if not workspace.is_dir() or (workspace / task_ref).resolve() != task_path:
        raise CommandError("stale_identity", "workspace", "Task workspace does not match task identity.", 3)
    if _repo_common_dir(workspace) != common_dir:
        raise CommandError("stale_identity", "repository_common_dir", "Task workspace belongs to a different repository.", 3)
    branch = _git(workspace, "branch", "--show-current")
    if not branch or branch != task.get("branch"):
        raise CommandError("stale_identity", "branch", "Task branch does not match current checkout.", 3)
    head = _git(workspace, "rev-parse", "HEAD")
    base_branch = task.get("base_branch") or (task.get("meta") or {}).get("base_branch")
    if not base_branch:
        raise CommandError("stale_identity", "base_branch", "Task base branch is missing.", 3)
    task_id = str(task["id"])
    tm = wm = None
    for candidate_root in (root, workspace):
        tm = tm or _read_mapping(_mapping_path(candidate_root, "tasks", task_id))
        wm = wm or _read_mapping(_mapping_path(candidate_root, "workspaces", task_id))
    if (not tm or not wm) and not allow_missing_mappings:
        raise CommandError("stale_identity", "runtime_mapping", "Task/workspace mapping identity drifted.", 3)
    generation = int(task.get("lifecycle_generation") or (task.get("meta") or {}).get("lifecycle_generation") or 1)
    for mapping, category in ((tm, "tasks"), (wm, "workspaces")):
        if mapping is None:
            continue
        if mapping.get("task_artifact_dir") and mapping.get("task_artifact_dir") != task_ref:
            raise CommandError("stale_identity", f"{category}.task_artifact_dir", "Runtime mapping points at another task.", 3)
        if mapping.get("workspace_path") != str(workspace) or mapping.get("repository_common_dir", str(common_dir)) != str(common_dir):
            raise CommandError("stale_identity", f"{category}.workspace_path", "Runtime mapping workspace or repository identity drifted.", 3)
        if category == "workspaces" and mapping.get("branch_name") != branch:
            raise CommandError("stale_identity", "workspaces.branch_name", "Workspace mapping branch drifted.", 3)
        if mapping.get("lifecycle_generation", generation) != generation:
            raise CommandError("stale_identity", "lifecycle_generation", "Task and workspace lifecycle generations differ.", 3)
    return {"task": task, "task_ref": task_ref, "task_path": task_path, "workspace": workspace, "branch": branch, "head": head, "common_dir": common_dir, "base_branch": str(base_branch), "generation": generation, "task_mapping": tm, "workspace_mapping": wm}


def _mapping_payloads(root: Path, workspace: Path, task_ref: str, task: dict[str, Any], branch: str, base_branch: str, common_dir: Path, generation: int) -> dict[Path, dict[str, Any]]:
    slug = str(task["id"])
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    base = {"schema_version": "1.0", "task_slug": slug, "workspace_slug": slug, "workspace_path": str(workspace), "repository_common_dir": str(common_dir), "base_branch": base_branch, "lifecycle_generation": generation, "updated_at": now}
    return {
        _mapping_path(root, "tasks", slug): {**base, "task_artifact_dir": task_ref},
        _mapping_path(root, "workspaces", slug): {**base, "source_checkout": str(root), "branch_name": branch},
        _mapping_path(workspace, "tasks", slug): {**base, "task_artifact_dir": task_ref},
        _mapping_path(workspace, "workspaces", slug): {**base, "source_checkout": str(root), "branch_name": branch},
    }


def write_recovery_mappings(root: Path, facts: dict[str, Any], task_ref: str) -> list[Path]:
    payloads = _mapping_payloads(root, facts["workspace"], task_ref, facts["task"], facts["branch"], facts["base_branch"], facts["common_dir"], facts["generation"])
    # Check every destination before the first write: conflicts are zero-write.
    for path, payload in payloads.items():
        if path.exists():
            current = _read_mapping(path)
            if any(current.get(key) != value for key, value in payload.items() if key != "updated_at"):
                raise CommandError("stale_identity", "runtime_mapping", "Existing mapping conflicts with recovery identity.", 3)
    created: list[Path] = []
    for path, payload in payloads.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
            created.append(path)
    return created


def _assert_post_write(module, root: Path, facts: dict[str, Any], task_ref: str) -> dict[str, Any]:
    post = task_facts(root, task_ref, allow_missing_mappings=False)
    active = module.resolve_active_task(root)
    if getattr(active, "error", None) or getattr(active, "task_path", None) is None:
        raise CommandError("stale_identity", "session_identity", "Post-write session boundary validation failed.", 3)
    expected_path = str((post["workspace"] / task_ref).resolve())
    actual_path = str(Path(active.task_path).resolve())
    if actual_path != expected_path or getattr(active, "task_workspace_root", None) and Path(active.task_workspace_root).resolve() != post["workspace"]:
        raise CommandError("stale_identity", "session_identity", "Post-write session task or workspace does not match.", 3)
    if getattr(active, "repository_common_dir", None) and Path(active.repository_common_dir).resolve() != post["common_dir"]:
        raise CommandError("stale_identity", "repository_common_dir", "Post-write repository identity does not match.", 3)
    return post


def execute(root: Path, input_value: str, owner_value: str) -> dict[str, Any]:
    public = load_json(input_value, "input")
    owner = load_json(owner_value, "owner_result")
    package_root = Path(__file__).parents[1]
    validate_json(public, package_root / "schemas/public-input.schema.json", "input")
    validate_json(owner, package_root / "schemas/semantic-result.schema.json", "owner_result")
    for key in ("profile", "mode", "continuation_id"):
        if owner.get(key) != public.get(key):
            raise CommandError("stale_identity", f"owner_result.{key}", "Rerun semantic review for the current binding request.", 3)
    profile = str(public["profile"])
    expected_route = PROFILE_ROUTES[profile]
    if owner.get("route") != expected_route:
        raise CommandError("stale_identity", "owner_result.route", "Semantic route does not match the selected profile.", 3)
    if profile == "switch_task":
        current_ref = _task_ref(public.get("current_task_ref") or owner.get("current_task_ref") or "")
        target_ref = _task_ref(public.get("target_task_ref") or owner.get("target_task_ref") or "")
        if current_ref == target_ref:
            raise CommandError("stale_identity", "target_task_ref", "Switch source and target tasks must differ.", 3)
    else:
        current_ref = ""
        target_ref = _task_ref(public.get("task_ref") or owner.get("task_ref") or "")
    if owner.get("task_ref") and profile != "switch_task" and owner.get("task_ref") != target_ref:
        raise CommandError("stale_identity", "owner_result.task_ref", "Target task changed.", 3)
    if profile == "switch_task" and owner.get("target_task_ref") != target_ref:
        raise CommandError("stale_identity", "target_task_ref", "Switch target changed.", 3)
    module = active_module(root)
    sid = session_id(module)
    if profile == "switch_task":
        previous = module.resolve_active_task(root)
        if getattr(previous, "error", None) or str(getattr(previous, "task_path", "")) == "":
            raise CommandError("stale_identity", "current_task_ref", "Switch source task is not currently bound.", 3)
        source_facts = task_facts(root, current_ref, allow_missing_mappings=False)
        if Path(previous.task_path).resolve() != (source_facts["workspace"] / current_ref).resolve():
            raise CommandError("stale_identity", "current_task_ref", "Current session is bound to another source task.", 3)
    manual = profile == "manual_recovery"
    facts = task_facts(root, target_ref, allow_missing_mappings=manual)
    previous = module.resolve_active_task(root)
    previous_path = getattr(previous, "task_path", None)
    previous_error = getattr(previous, "error", None)
    target_path = (facts["workspace"] / target_ref).resolve()
    if profile == "resume_current_task":
        if previous_error or previous_path is None or Path(previous_path).resolve() != target_path:
            raise CommandError("stale_identity", "current_task_ref", "Resume requires the current session to already target the requested task.", 3)
    elif profile in {"rebind_missing_session", "reactivate_rebind"}:
        if previous_error:
            raise CommandError("stale_identity", "current_task_ref", "Current session route is invalid; rebind cannot replace an unknown active task.", 3)
        if previous_path is not None and Path(previous_path).resolve() != target_path:
            raise CommandError("stale_identity", "current_task_ref", "A different active task requires an explicit switch route.", 3)
    if facts["generation"] != int(owner["lifecycle_generation"]):
        raise CommandError("stale_identity", "lifecycle_generation", "Requested lifecycle generation is stale.", 3)
    created: list[Path] = []
    if manual:
        created = write_recovery_mappings(root, facts, target_ref)
    try:
        result = module.set_active_task(target_ref, facts["workspace"])
        if result is None:
            raise CommandError("stale_identity", "session_identity", "Official session binding could not be established.", 3)
        facts = _assert_post_write(module, root, facts, target_ref)
        output = {"exit_id": EXITS[owner["route"]], "task_ref": target_ref, "lifecycle_generation": facts["generation"], "resume_target": owner["resume_target"]}
        validate_json(output, package_root / "schemas/public-output.schema.json", "stdout")
        return output
    except CommandError:
        raise


def run(package_root: Path, command: dict, argv: list[str]):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    args = parser.parse_args(argv)
    return execute(Path(args.root).resolve(), args.input, args.owner_result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    args = parser.parse_args()
    print(json.dumps(execute(Path(args.root).resolve(), args.input, args.owner_result), ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    try:
        main()
    except CommandError as exc:
        print(json.dumps({"code": exc.code, "field_path": exc.field_path, "remediation": exc.remediation}, ensure_ascii=False))
        raise SystemExit(exc.exit_status)
