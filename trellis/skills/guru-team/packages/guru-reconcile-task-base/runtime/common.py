from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from runtime.io import CommandError

EXITS = {
    "reconciled", "review_continuity_required", "implementation_required",
    "planning_stale", "scope_confirmation_required", "blocked",
}

def validate_json(instance: Any, schema_path: Path, field_path: str) -> None:
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
        schema = json.loads(schema_path.read_text())
        schema["$id"] = schema_path.as_uri()

        def retrieve(uri: str) -> Resource[Any]:
            target = Path(uri.removeprefix("file://")).resolve()
            schema_root = schema_path.parent.resolve()
            if target.parent != schema_root or not target.is_file() or target.is_symlink():
                raise CommandError("unsafe_path", field_path, "Resolve schema references only inside the package schema directory.")
            return Resource.from_contents(json.loads(target.read_text()))

        registry = Registry(retrieve=retrieve).with_resource(schema_path.as_uri(), Resource.from_contents(schema))
        errors = sorted(Draft202012Validator(schema, registry=registry).iter_errors(instance), key=lambda item: list(item.path))
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("runtime_dependency_missing", field_path, "Restore the package schema inventory.") from exc
    if errors:
        suffix = ".".join(str(part) for part in errors[0].path)
        raise CommandError("schema_mismatch", field_path + (f".{suffix}" if suffix else ""), "Repair the value to match the declared schema.")


def parse(parser: Any, argv: list[str]) -> Any:
    try:
        return parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the exact command help contract.") from exc


def repo_root(value: str | None) -> Path:
    root = Path(value or ".").resolve()
    probe = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if probe.returncode or Path(probe.stdout.strip()).resolve() != root:
        raise CommandError("unsafe_path", "root", "Use the exact Git worktree root.")
    return root


def read_json(repo: Path, package: Path, locator: str, field: str) -> dict[str, Any]:
    raw: str
    if locator == "-":
        raw = sys.stdin.read()
    else:
        path = Path(locator)
        choices = [path] if path.is_absolute() else [repo / path, package / path]
        selected = next((item for item in choices if item.is_file() and not item.is_symlink()), None)
        if selected is None:
            raise CommandError("unsafe_path", field, "Use a regular JSON file below the repository or package.")
        raw = selected.read_text()
    try:
        value = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("invalid_json", field, "Provide one JSON object.") from exc
    if not isinstance(value, dict):
        raise CommandError("invalid_json", field, "Provide one JSON object.")
    return value


def git(repo: Path, *args: str, check: bool = True) -> str:
    process = subprocess.run(["git", *args], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and process.returncode:
        raise CommandError("stale_identity", "repository", process.stderr.strip() or "Refresh current Git identity.", 3)
    return process.stdout.strip()


def resolve_commit(repo: Path, value: str, field: str) -> str:
    process = subprocess.run(["git", "rev-parse", "--verify", f"{value}^{{commit}}"], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode:
        raise CommandError("stale_identity", field, "Use one current unambiguous commit identity.", 3)
    return process.stdout.strip()


def _identity_json(path: Path, field: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise CommandError("stale_identity", field, "Restore the exact current task runtime identity.", 3)
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("stale_identity", field, "Restore the exact current task runtime identity.", 3) from exc
    if not isinstance(value, dict):
        raise CommandError("stale_identity", field, "Restore the exact current task runtime identity.", 3)
    return value


def _current_worktree_branch(repo: Path) -> str:
    rows: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in git(repo, "worktree", "list", "--porcelain").splitlines() + [""]:
        if not line:
            if current:
                rows.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    matches = [row for row in rows if Path(row.get("worktree", "")).resolve() == repo.resolve()]
    if len(matches) != 1 or not matches[0].get("branch", "").startswith("refs/heads/"):
        raise CommandError("stale_identity", "worktree", "Use the unique current branch worktree.", 3)
    return matches[0]["branch"].removeprefix("refs/heads/")


def task_identity(repo: Path, task_ref: str) -> dict[str, str]:
    tasks_root = (repo / ".trellis/tasks").resolve()
    task_dir = (repo / task_ref).resolve()
    if not task_ref.startswith(".trellis/tasks/") or task_dir == tasks_root or not task_dir.is_relative_to(tasks_root) or not task_dir.is_dir() or task_dir.is_symlink():
        raise CommandError("stale_identity", "task_ref", "Use the exact current task directory.", 3)
    task = _identity_json(task_dir / "task.json", "task.json")
    task_id = task.get("id")
    branch = task.get("branch")
    if not isinstance(task_id, str) or not task_id or not isinstance(branch, str) or not branch or task.get("status") != "in_progress":
        raise CommandError("stale_identity", "task.json", "Use the current in-progress task identity.", 3)
    live_branch = git(repo, "branch", "--show-current")
    if branch != live_branch or branch != _current_worktree_branch(repo):
        raise CommandError("stale_identity", "task.json.branch", "Use the task branch checked out in this exact worktree.", 3)
    task_mapping = _identity_json(repo / ".trellis/.runtime/guru-team/tasks" / f"{task_id}.json", "task_mapping")
    workspace_slug = task_mapping.get("workspace_slug")
    relative = task_dir.relative_to(repo.resolve()).as_posix()
    expected_task = {"schema_version": "1.0", "task_slug": task_id, "workspace_path": str(repo.resolve()), "task_artifact_dir": relative}
    if not isinstance(workspace_slug, str) or not workspace_slug or any(task_mapping.get(key) != value for key, value in expected_task.items()):
        raise CommandError("stale_identity", "task_mapping", "Use the mapping for this exact task and worktree.", 3)
    current_mappings: list[Path] = []
    mappings_root = repo / ".trellis/.runtime/guru-team/tasks"
    for candidate in mappings_root.glob("*.json"):
        try:
            candidate_mapping = json.loads(candidate.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(candidate_mapping, dict) and candidate_mapping.get("workspace_path") == str(repo.resolve()):
            current_mappings.append(candidate.resolve())
    if current_mappings != [(mappings_root / f"{task_id}.json").resolve()]:
        raise CommandError("stale_identity", "task_mapping", "Use the unique current task mapping for this worktree.", 3)
    workspace_mapping = _identity_json(repo / ".trellis/.runtime/guru-team/workspaces" / f"{workspace_slug}.json", "workspace_mapping")
    expected_workspace = {"schema_version": "1.0", "workspace_slug": workspace_slug, "workspace_path": str(repo.resolve()), "branch_name": branch}
    if any(workspace_mapping.get(key) != value for key, value in expected_workspace.items()):
        raise CommandError("stale_identity", "workspace_mapping", "Use the mapping for this exact task branch and worktree.", 3)
    return {"task_id": task_id, "task_ref": relative, "branch": branch, "workspace_slug": workspace_slug}


def is_ancestor(repo: Path, older: str, newer: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", older, newer], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def validate_public(package: Path, value: dict[str, Any]) -> None:
    validate_json(value, package / "schemas/public-input.schema.json", "public_input")


def objective_identity(repo: Path, public: dict[str, Any]) -> None:
    task_identity(repo, public["task_ref"])
    task_head = resolve_commit(repo, public["task_head"], "task_head")
    old_base = resolve_commit(repo, public["old_base_head"], "old_base_head")
    new_base = resolve_commit(repo, public["new_base_head"], "new_base_head")
    current_base = resolve_commit(repo, public["selected_base_ref"], "selected_base_ref")
    if task_head != public["task_head"] or old_base != public["old_base_head"] or new_base != public["new_base_head"]:
        raise CommandError("stale_identity", "pair", "Use full current commit identities.", 3)
    if current_base != new_base:
        raise CommandError("stale_identity", "new_base_head", "Refresh the selected base exactly once.", 3)
    if not is_ancestor(repo, old_base, new_base):
        raise CommandError("stale_identity", "base_pair", "History rewrites require explicit recovery.", 3)
    if resolve_commit(repo, "HEAD", "HEAD") != task_head:
        raise CommandError("stale_identity", "task_head", "Rebuild the pair for current task content.", 3)
    branch_commit = public.get("branch_review_commit")
    if branch_commit and resolve_commit(repo, branch_commit, "branch_review_commit") != branch_commit:
        raise CommandError("stale_identity", "branch_review_commit", "Use the exact existing review commit.", 3)


def checkpoint_path(repo: Path, task_ref: str) -> Path:
    identity = task_identity(repo, task_ref)
    namespace = f"{identity['task_id']}-{hashlib.sha256(identity['task_ref'].encode()).hexdigest()[:12]}"
    return repo / ".trellis/.runtime/guru-team/owner-checkpoints" / namespace / "guru-reconcile-task-base" / "base-reconciliation.json"


def validate_result(package: Path, repo: Path, result: dict[str, Any], public: dict[str, Any] | None = None) -> None:
    validate_json(result, package / "schemas/base-reconciliation.schema.json", "owner_result")
    unsigned = {key: copy.deepcopy(value) for key, value in result.items() if key != "facts_sha256"}
    if result["facts_sha256"] != digest(unsigned):
        raise CommandError("stale_identity", "facts_sha256", "Rerecord the current semantic result.", 3)
    if result["semantic_gate"]["typed_exit"] != result["typed_output"]["exit_id"]:
        raise CommandError("schema_mismatch", "typed_output.exit_id", "Match the AI-selected typed exit.")
    expected = public or {
        key: result[key] for key in ("profile", "mode", "task_ref", "task_head", "selected_base_ref", "old_base_head", "new_base_head", "resume_target")
    }
    if "branch_review_commit" in result:
        expected["branch_review_commit"] = result["branch_review_commit"]
    validate_public(package, expected)
    objective_identity(repo, expected)
    for key in ("profile", "mode", "task_ref", "task_head", "selected_base_ref", "old_base_head", "new_base_head", "resume_target"):
        if result[key] != expected[key]:
            raise CommandError("stale_identity", key, "Use the result for this exact invocation pair.", 3)
    if result.get("branch_review_commit") != expected.get("branch_review_commit"):
        raise CommandError("stale_identity", "branch_review_commit", "Use the result for the exact caller review identity.", 3)


def output_for(public: dict[str, Any], gate: dict[str, Any], exit_id: str) -> dict[str, Any]:
    if exit_id == "reconciled":
        return {"exit_id": exit_id, "task_ref": public["task_ref"], "task_head": public["task_head"], "new_base_head": public["new_base_head"], "resume_target": public["resume_target"]}
    if exit_id == "review_continuity_required":
        details = gate["route_payload"]
        if "branch_review_commit" not in public:
            raise CommandError("schema_mismatch", "branch_review_commit", "Continuity requires an existing branch review identity.")
        return {"exit_id": exit_id, "task_ref": public["task_ref"], "task_head": public["task_head"], "old_base_head": public["old_base_head"], "new_base_head": public["new_base_head"], "branch_review_commit": public["branch_review_commit"], "candidate_tree_sha256": details.get("candidate_tree_sha256"), "relevant_paths": details.get("relevant_paths"), "resume_target": public["resume_target"]}
    if exit_id == "implementation_required":
        return {"exit_id": exit_id, "task_ref": public["task_ref"], "task_head": public["task_head"], "finding_refs": gate["route_payload"].get("finding_refs"), "resume_target": public["resume_target"]}
    if exit_id == "planning_stale":
        return {"exit_id": exit_id, "task_ref": public["task_ref"], "reason_refs": gate["route_payload"].get("reason_refs")}
    if exit_id == "scope_confirmation_required":
        return {"exit_id": exit_id, "task_ref": public["task_ref"], "proposal_refs": gate["route_payload"].get("proposal_refs")}
    if exit_id == "blocked":
        return {"exit_id": "blocked"}
    raise CommandError("schema_mismatch", "typed_exit", "Select exactly one declared typed exit.")
