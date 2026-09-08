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

POST_REVIEW_PROFILES = {
    "post_branch_review", "post_publication", "finalizer_base_mismatch",
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


def task_identity(repo: Path, task_ref: str, *, allow_planning: bool = False) -> dict[str, str]:
    tasks_root = (repo / ".trellis/tasks").resolve()
    task_dir = (repo / task_ref).resolve()
    if not task_ref.startswith(".trellis/tasks/") or task_dir == tasks_root or not task_dir.is_relative_to(tasks_root) or not task_dir.is_dir() or task_dir.is_symlink():
        raise CommandError("stale_identity", "task_ref", "Use the exact current task directory.", 3)
    task = _identity_json(task_dir / "task.json", "task.json")
    task_id = task.get("id")
    branch = task.get("branch")
    allowed_statuses = {"in_progress", "planning"} if allow_planning else {"in_progress"}
    if not isinstance(task_id, str) or not task_id or not isinstance(branch, str) or not branch or task.get("status") not in allowed_statuses:
        expected = "planning or in-progress" if allow_planning else "in-progress"
        raise CommandError("stale_identity", "task.json", f"Use the current {expected} task identity.", 3)
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


def index_tree_digest(repo: Path) -> str:
    process = subprocess.run(
        ["git", "ls-files", "--stage", "-z"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise CommandError("stale_identity", "repository.index", "Refresh the exact candidate index.", 3)
    rows: list[bytes] = []
    for entry in process.stdout.split(b"\0"):
        if not entry:
            continue
        metadata, separator, path = entry.partition(b"\t")
        parts = metadata.split()
        if not separator or len(parts) != 3 or parts[2] != b"0":
            raise CommandError(
                "candidate_failed",
                "repository.index",
                "Resolve the candidate before computing its identity.",
                3,
            )
        blob = subprocess.run(
            ["git", "cat-file", "blob", parts[1].decode("ascii")],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if blob.returncode:
            raise CommandError(
                "candidate_failed",
                "repository.index",
                blob.stderr.decode("utf-8", "replace").strip()
                or "Read the exact candidate blob identity.",
                3,
            )
        rows.append(
            path + b"\0" + hashlib.sha256(blob.stdout).hexdigest().encode() + b"\0"
        )
    return hashlib.sha256(b"".join(rows)).hexdigest()


def require_clean_worktree(repo: Path) -> None:
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=normal"],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if status.returncode or status.stdout:
        raise CommandError("stale_identity", "worktree", "Use a clean branch-bound task worktree.", 3)


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def validate_public(package: Path, value: dict[str, Any]) -> None:
    validate_json(value, package / "schemas/public-input.schema.json", "public_input")


def objective_identity(repo: Path, public: dict[str, Any], *, expected_head: str | None = None) -> None:
    task_identity(repo, public["task_ref"], allow_planning=public["profile"] == "post_plan")
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
    if resolve_commit(repo, "HEAD", "HEAD") != (expected_head or task_head):
        raise CommandError("stale_identity", "task_head", "Rebuild the pair for current task content.", 3)
    branch_commit = public.get("branch_review_commit")
    if branch_commit and resolve_commit(repo, branch_commit, "branch_review_commit") != branch_commit:
        raise CommandError("stale_identity", "branch_review_commit", "Use the exact existing review commit.", 3)


def checkpoint_path(repo: Path, task_ref: str, *, allow_planning: bool = False) -> Path:
    identity = task_identity(repo, task_ref, allow_planning=allow_planning)
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
        key: result[key] for key in ("profile", "mode", "task_ref", "selected_base_ref", "old_base_head", "new_base_head", "resume_target")
    }
    expected["task_head"] = result["prior_task_head"]
    if "branch_review_commit" in result:
        expected["branch_review_commit"] = result["branch_review_commit"]
    validate_public(package, expected)
    objective_identity(repo, expected, expected_head=result["task_head"])
    for key in ("profile", "mode", "task_ref", "selected_base_ref", "old_base_head", "new_base_head", "resume_target"):
        if result[key] != expected[key]:
            raise CommandError("stale_identity", key, "Use the result for this exact invocation pair.", 3)
    if result["prior_task_head"] != expected["task_head"]:
        raise CommandError("stale_identity", "prior_task_head", "Use the result for the exact pre-reconciliation task HEAD.", 3)
    if result.get("branch_review_commit") != expected.get("branch_review_commit"):
        raise CommandError("stale_identity", "branch_review_commit", "Use the result for the exact caller review identity.", 3)
    exit_id = result["typed_output"]["exit_id"]
    receipt = result.get("reconciliation_result")
    if exit_id == "review_continuity_required":
        if result["profile"] not in POST_REVIEW_PROFILES or not receipt:
            raise CommandError("schema_mismatch", "reconciliation_result", "Continuity requires one current post-review reconciliation result.")
        for key, expected_value in {
            "prior_task_head": result["prior_task_head"],
            "new_base_head": result["new_base_head"],
            "branch_review_commit": result["branch_review_commit"],
            "reconciled_task_head": result["task_head"],
            "candidate_tree_sha256": result["semantic_gate"]["route_payload"]["candidate_tree_sha256"],
        }.items():
            if receipt[key] != expected_value:
                raise CommandError("stale_identity", f"reconciliation_result.{key}", "Use the exact checked reconciliation result.", 3)
        if not is_ancestor(repo, result["prior_task_head"], result["task_head"]):
            raise CommandError("stale_identity", "prior_task_head", "The prior task HEAD must remain an ancestor.", 3)
        if not is_ancestor(repo, result["new_base_head"], result["task_head"]):
            raise CommandError("stale_identity", "new_base_head", "The reviewed new base must remain an ancestor.", 3)
        if not is_ancestor(repo, result["branch_review_commit"], result["task_head"]):
            raise CommandError("stale_identity", "branch_review_commit", "The prior full-review commit must remain an ancestor.", 3)
        require_clean_worktree(repo)
        if index_tree_digest(repo) != receipt["candidate_tree_sha256"]:
            raise CommandError("stale_identity", "candidate_tree_sha256", "The committed tree must match the reviewed candidate.", 3)
    elif receipt is not None or result["task_head"] != result["prior_task_head"]:
        raise CommandError("schema_mismatch", "reconciliation_result", "Only bounded post-review continuity may consume a reconciliation result.")


def output_for(public: dict[str, Any], gate: dict[str, Any], exit_id: str, *, task_head: str | None = None) -> dict[str, Any]:
    current_task_head = task_head or public["task_head"]
    if exit_id == "reconciled":
        return {"exit_id": exit_id, "task_ref": public["task_ref"], "task_head": current_task_head, "new_base_head": public["new_base_head"], "resume_target": public["resume_target"]}
    if exit_id == "review_continuity_required":
        details = gate["route_payload"]
        if "branch_review_commit" not in public:
            raise CommandError("schema_mismatch", "branch_review_commit", "Continuity requires an existing branch review identity.")
        return {"exit_id": exit_id, "task_ref": public["task_ref"], "task_head": current_task_head, "old_base_head": public["old_base_head"], "new_base_head": public["new_base_head"], "branch_review_commit": public["branch_review_commit"], "candidate_tree_sha256": details.get("candidate_tree_sha256"), "relevant_paths": details.get("relevant_paths"), "resume_target": public["resume_target"]}
    if exit_id == "implementation_required":
        return {"exit_id": exit_id, "task_ref": public["task_ref"], "task_head": public["task_head"], "finding_refs": gate["route_payload"].get("finding_refs"), "resume_target": public["resume_target"]}
    if exit_id == "planning_stale":
        return {"exit_id": exit_id, "task_ref": public["task_ref"], "reason_refs": gate["route_payload"].get("reason_refs")}
    if exit_id == "scope_confirmation_required":
        return {"exit_id": exit_id, "task_ref": public["task_ref"], "proposal_refs": gate["route_payload"].get("proposal_refs")}
    if exit_id == "blocked":
        return {"exit_id": "blocked"}
    raise CommandError("schema_mismatch", "typed_exit", "Select exactly one declared typed exit.")
