"""Read exact shared archive facts. Semantic qualification remains with the AI."""
from __future__ import annotations

import json
import subprocess
import shutil
from pathlib import Path

from runtime.delivery_projection.adapter import upstream_modules
from runtime.maintenance_transport import call
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import commit_path_bytes, discover_worktree_facts, inspect_repository, is_ancestor, run_common_git
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.identity import normalize_task_ref, origin_matches, resolve_task_id
from runtime.task_lifecycle.source import normalize_repo_ref, task_source


def require(condition, field, message):
    if not condition:
        raise LifecycleContractError("shared_archive_mismatch", field, message)


def github_json(repo_ref, endpoint):
    """Repository-bound, read-only provider port; never emit provider stderr."""
    if shutil.which("gh") is None:
        raise LifecycleContractError("github_cli_missing", "github.cli", "Install GitHub CLI and retry.")
    for argv in (["gh", "auth", "status"], ["gh", "api", f"repos/{repo_ref}"],
                 ["gh", "api", f"repos/{repo_ref}/{endpoint}"]):
        try:
            result = subprocess.run(argv, capture_output=True, text=True)
        except OSError as exc:
            raise LifecycleContractError("github_cli_missing", "github.cli", "Restore GitHub CLI and retry.") from exc
        if result.returncode:
            text = result.stderr.casefold()
            if any(value in text for value in ("not logged", "authentication", "http 401")):
                code = "github_auth_failed"
            elif any(value in text for value in ("http 403", "forbidden", "permission")):
                code = "github_permission_denied"
            elif any(value in text for value in ("http 404", "could not resolve to a repository")):
                code = "github_repo_access_denied"
            else:
                code = "github_api_unavailable"
            raise LifecycleContractError(code, "github.provider", "Restore the selected repository's GitHub fact access and retry.")
    try:
        rows = json.loads(result.stdout)
        if endpoint.startswith("pulls/"):
            if not isinstance(rows, dict) or not {"number", "state", "draft", "base", "head"} <= rows.keys():
                raise ValueError("incomplete implementation PR response")
        else:
            required = {"number", "base", "merge_commit_sha", "merged_at"}
            if not isinstance(rows, list) or any(not isinstance(row, dict) or not required <= row.keys()
                    or not isinstance(row["base"], dict) or "ref" not in row["base"]
                    or not isinstance(row["base"].get("repo"), dict) or "full_name" not in row["base"]["repo"] for row in rows):
                raise ValueError("incomplete provider response")
        return rows
    except (ValueError, TypeError) as exc:
        raise LifecycleContractError("github_response_incomplete", "github.response", "Reread complete repository-bound bookkeeping PR facts.") from exc


def read_shared_archive(root, key, anchor):
    repository = inspect_repository(root)
    repo_ref = normalize_repo_ref(anchor["repo_ref"])
    require(origin_matches(root, repo_ref), "repo_ref", "Use the selected repository identity.")
    archive_ref = normalize_task_ref(anchor["archive_ref"])
    original_ref = normalize_task_ref(anchor["original_task_ref"])
    require(archive_ref.startswith(".trellis/tasks/archive/") and not original_ref.startswith(".trellis/tasks/archive/"), "archive_ref", "Select exact archive and original active locators.")
    commit = run_common_git(repository, ["rev-parse", "--verify", anchor["archive_commit"] + "^{commit}"]).stdout.strip()
    target = run_common_git(repository, ["rev-parse", "--verify", anchor["target_ref"] + "^{commit}"]).stdout.strip()
    require(is_ancestor(repository, commit, target), "target_ref", "The selected target must contain the exact archive commit.")
    task_bytes = commit_path_bytes(repository, commit, archive_ref + "/task.json")
    summary_bytes = commit_path_bytes(repository, commit, archive_ref + "/finish-summary.json")
    require(task_bytes is not None and summary_bytes is not None, "archive_commit", "Read both archived Task and Finish summary at the exact commit.")
    require(commit_path_bytes(repository, commit, original_ref + "/task.json") is None, "original_task_ref", "The exact archive result must remove the original active record.")
    task, summary = json.loads(task_bytes), json.loads(summary_bytes)
    require(task.get("id") == key.task_id and task.get("lifecycle_generation") == key.lifecycle_generation, "archived_lifecycle", "Read the exact predecessor TaskId and generation.")
    require(summary.get("schema_version") == 2 and summary.get("generator") == "guru-team.finalize-task"
            and summary.get("task", {}).get("archive_dir") == archive_ref
            and summary["task"].get("artifact_dir") == original_ref
            and summary["task"].get("status") == "completed", "finish-summary", "Read the matching formal Finish summary and original locator.")
    source = task_source(task)
    family = "schema2" if task.get("schema_version") == "2.0" else "schema1"
    if family == "schema2":
        task = upstream_modules(root).delivery_schema.parse_task_v2(task)
        completed = [row for row in task["completion_results"] if row["lifecycle_generation"] == key.lifecycle_generation
                     and row["accepted_scope"] == task["accepted_scope"] and row["outcome"] == "completed"]
        require(bool(completed) and any(row["lifecycle_generation"] == key.lifecycle_generation
                and row["completion_result_id"] == completed[-1]["result_id"] for row in task["closure_results"]),
                "completion_results", "Use the public Completion and matching Closure of the archived generation.")
    else:
        require(task.get("status") == "completed" and task.get("schema_version") is None
                and "creator" not in task and "assignee" not in task, "task", "Only the selected formal schema1 family can enter public reactivation.")
    branch = run_common_git(repository, ["rev-parse", "--symbolic-full-name", anchor["target_ref"]]).stdout.strip()
    for prefix in ("refs/heads/", "refs/remotes/origin/"):
        if branch.startswith(prefix):
            branch = branch[len(prefix):]
            break
    rows = github_json(repo_ref, f"commits/{commit}/pulls")
    matches = []
    for row in rows:
        merge = row.get("merge_commit_sha")
        if (row.get("base", {}).get("repo", {}).get("full_name", "").casefold() != repo_ref.casefold()
                or row.get("base", {}).get("ref") != branch or not row.get("merged_at") or not merge):
            continue
        if not is_ancestor(repository, commit, merge) or not is_ancestor(repository, merge, target):
            continue
        first_parent = run_common_git(repository, ["rev-parse", "--verify", merge + "^1"]).stdout.strip()
        if is_ancestor(repository, commit, first_parent):
            # A later PR retaining the archive did not introduce this Finish.
            continue
        if (commit_path_bytes(repository, merge, archive_ref + "/task.json") != task_bytes
                or commit_path_bytes(repository, merge, archive_ref + "/finish-summary.json") != summary_bytes
                or commit_path_bytes(repository, merge, original_ref + "/task.json") is not None):
            continue
        matches.append(row)
    require(len(matches) == 1, "bookkeeping_pr", "Resolve one exact merged bookkeeping PR and target archive result.")
    return {"task": task, "summary": summary, "source": source, "family": family,
            "archive_ref": archive_ref, "original_task_ref": original_ref,
            "archive_commit": commit, "target_head": target, "bookkeeping_pr": matches[0]["number"]}


def formal_inspection(root, key, anchor, facts, source):
    from hashlib import sha256
    repository = inspect_repository(root)
    summary = commit_path_bytes(repository, facts["archive_commit"], facts["archive_ref"] + "/finish-summary.json")
    return {"root": str(root), "key": {"task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation},
            "task_ref": facts["archive_ref"], "original_task_ref": facts["original_task_ref"],
            "archive": {"commit": facts["archive_commit"], "target_ref": anchor["target_ref"],
                        "target_head": facts["target_head"], "evidence": [{"locator": facts["archive_ref"] + "/finish-summary.json", "revision": "sha256:" + sha256(summary).hexdigest()}]}}


def _successor_at_checkout(root, key, anchor, facts, source=None):
    if facts["family"] == "schema1":
        require(source is not None, "source_ref", "Select the matching public CLI/Core source before formal archive inspection.")
        result = call(source, "inspectFormalArchiveReactivation", formal_inspection(root, key, anchor, facts, source))
        require(result["successor"]["kind"] != "conflicting", "successor", "Resolve the actual accessible successor conflict.")
        return result["successor"].get("task")
    identity = resolve_task_id(root, key.task_id)
    if identity.lifecycle_generation == key.lifecycle_generation:
        require(identity.task_ref == facts["archive_ref"] and identity.lifecycle_state == "archived", "successor", "Resolve the exact archived predecessor.")
        return None
    record = json.loads((root / identity.task_ref / "task.json").read_text())
    record = upstream_modules(root).delivery_schema.parse_task_v2(record)
    require(record["lifecycle_generation"] > key.lifecycle_generation and task_source(record) == facts["source"], "successor", "Read the same Task's public successor.")
    for field in ("completion_results", "closure_results"):
        require(all(row in record[field] for row in facts["task"][field]), "successor", "The successor must retain the exact predecessor's public terminal history.")
    return {"key": {"task_id": identity.task_id, "lifecycle_generation": identity.lifecycle_generation}, "task_ref": identity.task_ref}


def find_successor(root, key, anchor, facts, source=None, *, with_checkout=False):
    """Read registered public Tasks and current C4, never peer recovery receipts."""
    repository = inspect_repository(root)
    branches = BranchBindingStore(repository)
    candidates = []
    for checkout in discover_worktree_facts(repository):
        if checkout.inspection_error is not None:
            ref = checkout.registration.registered_branch_ref
            bound = branches.branch_owner(ref) if ref else None
            require(bound is None or bound.task_id != key.task_id or bound.lifecycle_generation <= key.lifecycle_generation,
                    "checkout", "Restore the selected Task successor's registered checkout facts.")
            continue
        # A shared active snapshot can be present on a non-owner branch after
        # an ordinary merge. Parse its public key before invoking the C4-aware
        # resolver, which correctly rejects resolution from that non-owner.
        task_root = checkout.path / ".trellis/tasks"
        selected_refs = []
        for path in (*task_root.glob("*/task.json"), *task_root.glob("archive/*/*/task.json")):
            ref = path.parent.relative_to(checkout.path).as_posix()
            try:
                raw = json.loads(path.read_text())
            except (OSError, ValueError):
                if ref.startswith(".trellis/tasks/archive/"):
                    continue
                raise LifecycleContractError("invalid_task_metadata", ref + "/task.json", "Read the active Task metadata before successor discovery.")
            if not isinstance(raw, dict):
                if ref.startswith(".trellis/tasks/archive/"):
                    continue
                raise LifecycleContractError("invalid_task_metadata", ref + "/task.json", "Use one active Task metadata object.")
            if raw.get("id") != key.task_id or raw.get("schema_version") != "2.0":
                continue
            record = upstream_modules(checkout.path).delivery_schema.parse_task_v2(raw)
            if record["lifecycle_generation"] <= key.lifecycle_generation:
                continue
            binding = branches.read(TaskLifecycleKey(record["id"], record["lifecycle_generation"]))
            if not ref.startswith(".trellis/tasks/archive/") and binding is not None and checkout.branch_ref != binding.branch_ref:
                continue
            selected_refs.append(ref)
        if not selected_refs:
            continue
        try:
            identity = resolve_task_id(checkout.path, key.task_id)
        except LifecycleContractError as exc:
            if exc.code == "task_not_found":
                continue
            if exc.code == "unsupported_legacy_task" and facts["family"] == "schema1":
                # The exact schema1 predecessor is read through its SDK below.
                continue
            raise
        if identity.lifecycle_generation <= key.lifecycle_generation:
            continue
        binding = branches.read(TaskLifecycleKey(identity.task_id, identity.lifecycle_generation))
        if identity.lifecycle_state == "active" and binding is not None and checkout.branch_ref != binding.branch_ref:
            continue
        successor = _successor_at_checkout(checkout.path, key, anchor, facts, source)
        if successor is not None:
            candidates.append((checkout.path, successor))
    identities = {(row[1]["key"]["task_id"], row[1]["key"]["lifecycle_generation"], row[1]["task_ref"]) for row in candidates}
    require(len(identities) <= 1, "successor", "Resolve the actual accessible successor conflict through the original identity owner.")
    if candidates:
        selected = next((row for row in candidates if row[0].resolve() == root.resolve()), candidates[0])
    else:
        selected = (root, _successor_at_checkout(root, key, anchor, facts, source))
    return selected if with_checkout else selected[1]
