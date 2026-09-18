from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote

from runtime.io import CommandError
from runtime.schema import validate_json


DIMENSIONS = (
    "active_task",
    "pr_identity",
    "checks_and_reviews",
    "mergeability",
    "repository_policy",
    "message_and_delivery_boundary",
)
TRAILER_KEYS = (
    "Guru-Task-Identity",
    "Guru-Delivery-Schema",
    "Guru-Delivery-Head",
)
CLOSING_KEYWORD = re.compile(
    r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b[^\r\n#]{0,160}#\d+",
    re.IGNORECASE,
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def repo_root(value: str | None) -> Path:
    root = Path(value or ".").resolve()
    if not (root / ".git").exists():
        raise CommandError("unsafe_path", "root", "Use the exact Git worktree root.")
    return root


def load_json(root: Path, package_root: Path, value: str, field: str) -> dict[str, Any]:
    if value == "-":
        raw = sys.stdin.read()
    else:
        path = Path(value)
        candidates = [path] if path.is_absolute() else [root / path, package_root / path]
        resolved = next((item for item in candidates if item.is_file() and not item.is_symlink()), None)
        if resolved is None:
            raise CommandError("unsafe_path", field, "Use one existing regular JSON file.")
        raw = resolved.read_text(encoding="utf-8")
    try:
        result = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("invalid_arguments", field, "Provide one valid JSON object.") from exc
    if not isinstance(result, dict):
        raise CommandError("invalid_arguments", field, "Provide one valid JSON object.")
    return result


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if proc.returncode:
        raise CommandError(
            "stale_identity", "repository", proc.stderr.strip() or "Repair current Git state.", 3
        )
    return proc.stdout.strip()


def _github_error(proc: subprocess.CompletedProcess[str], operation: str) -> CommandError:
    text = proc.stderr.casefold()
    if "not logged" in text or "authentication" in text or "http 401" in text:
        code, field, remediation = "github_auth_failed", "github.auth", "Repair GitHub authentication and retry."
    elif "http 403" in text or "forbidden" in text or "permission" in text:
        code, field, remediation = "github_permission_denied", "github.permission", "Resolve repository permission and repeat the current review."
    elif "could not resolve to a repository" in text or "http 404" in text:
        code, field, remediation = "github_repo_access_denied", "github.repository", "Verify repository identity and access."
    else:
        code, field, remediation = "github_api_unavailable", "github.provider", "Retry after provider or network recovery."
    return CommandError(code, field, remediation, response={"operation": operation})


def require_gh(root: Path) -> None:
    if shutil.which("gh") is None:
        raise CommandError("github_cli_missing", "github.cli", "Install GitHub CLI and retry.")
    proc = subprocess.run(
        ["gh", "auth", "status"], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if proc.returncode:
        raise _github_error(proc, "auth status")


def gh_json(root: Path, args: list[str], operation: str) -> dict[str, Any]:
    proc = subprocess.run(
        ["gh", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if proc.returncode:
        raise _github_error(proc, operation)
    try:
        value = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise CommandError(
            "github_response_incomplete",
            "github.response",
            "Repair the adapter/query contract and reread live facts.",
        ) from exc
    if not isinstance(value, dict):
        raise CommandError(
            "github_response_incomplete",
            "github.response",
            "Repair the adapter/query contract and reread live facts.",
        )
    return value


def validate_public(package_root: Path, value: dict[str, Any]) -> None:
    validate_json(value, package_root / "schemas/public-ready-for-merge-input.schema.json", "input")


def validate_review(package_root: Path, value: dict[str, Any]) -> None:
    validate_json(value, package_root / "schemas/semantic-review.schema.json", "review_input")
    ids = [item["id"] for item in value["dimensions"]]
    if len(set(ids)) != len(ids) or set(ids) != set(DIMENSIONS):
        raise CommandError(
            "schema_mismatch", "review_input.dimensions", "Review every declared dimension exactly once."
        )


def task_facts(root: Path, public: dict[str, Any]) -> dict[str, Any]:
    task_root = (root / ".trellis/tasks").resolve()
    path = (root / public["task_ref"]).resolve()
    try:
        path.relative_to(task_root)
    except ValueError as exc:
        raise CommandError("unsafe_path", "input.task_ref", "Use one task below .trellis/tasks.") from exc
    task_file = path / "task.json"
    if path.is_symlink() or not task_file.is_file() or task_file.is_symlink():
        raise CommandError("unsafe_path", "input.task_ref", "Use one current regular task directory.")
    try:
        task = json.loads(task_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("invalid_arguments", "task", "Repair the current task.json.") from exc
    if not isinstance(task, dict):
        raise CommandError("invalid_arguments", "task", "Repair the current task.json.")
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if task.get("status") != "in_progress":
        raise CommandError("stale_identity", "task.status", "Use the current active task.", 3)
    if task.get("branch") != branch:
        raise CommandError("stale_identity", "task.branch", "Use the task's current bound branch.", 3)
    configured_worktree = task.get("worktree_path")
    if configured_worktree and Path(configured_worktree).resolve() != root:
        raise CommandError("stale_identity", "task.worktree_path", "Use the task's current bound worktree.", 3)
    stable_id = task.get("id")
    if not isinstance(stable_id, str) or not stable_id:
        raise CommandError("invalid_arguments", "task.id", "Repair the stable task identity.")
    base_branch = task.get("base_branch")
    if not isinstance(base_branch, str) or not base_branch:
        raise CommandError("invalid_arguments", "task.base_branch", "Repair the current task base binding.")
    return {
        "task_ref": public["task_ref"],
        "stable_task_id": stable_id,
        "status": task["status"],
        "branch": branch,
        "base_branch": base_branch,
        "head_sha": head,
    }


def _check_state(item: dict[str, Any]) -> str:
    raw = str(
        item.get("conclusion")
        or item.get("state")
        or item.get("status")
        or ""
    ).upper()
    if raw in {"SUCCESS", "NEUTRAL", "SKIPPED", "COMPLETED", "PASS", "EXPECTED"}:
        return "passed"
    if raw in {"FAILURE", "ERROR", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED", "FAIL"}:
        return "failed"
    return "pending"


def live_facts(root: Path, package_root: Path, public: dict[str, Any]) -> dict[str, Any]:
    validate_public(package_root, public)
    task = task_facts(root, public)
    require_gh(root)
    fields = (
        "number,url,state,isDraft,headRefOid,headRefName,baseRefName,mergeable,"
        "mergeStateStatus,reviewDecision,statusCheckRollup,body,mergedAt,mergeCommit"
    )
    raw_pr = gh_json(
        root,
        ["pr", "view", str(public["pr_number"]), "--repo", public["repo_ref"], "--json", fields],
        "pr view",
    )
    try:
        merge_sha = (raw_pr.get("mergeCommit") or {}).get("oid")
        pr = {
            "number": int(raw_pr["number"]),
            "url": str(raw_pr["url"]),
            "state": str(raw_pr["state"]).upper(),
            "is_draft": bool(raw_pr["isDraft"]),
            "head_sha": str(raw_pr["headRefOid"]),
            "head_branch": str(raw_pr["headRefName"]),
            "base_branch": str(raw_pr["baseRefName"]),
            "body": str(raw_pr.get("body") or ""),
            "merged_at": raw_pr.get("mergedAt"),
            "merge_commit_sha": str(merge_sha) if merge_sha else None,
            "mergeable": str(raw_pr.get("mergeable") or "UNKNOWN").upper(),
            "merge_state_status": str(raw_pr.get("mergeStateStatus") or "UNKNOWN").upper(),
            "review_decision": str(raw_pr.get("reviewDecision") or "").upper(),
            "checks": raw_pr.get("statusCheckRollup") or [],
        }
    except (KeyError, TypeError, ValueError) as exc:
        raise CommandError(
            "github_response_incomplete", "github.pr", "Repair the PR query contract and reread live facts."
        ) from exc
    if pr["number"] != public["pr_number"]:
        raise CommandError("stale_identity", "github.pr.number", "Rebuild the publication handoff.", 3)
    if pr["head_sha"] != public["expected_head_sha"] or task["head_sha"] != public["expected_head_sha"]:
        raise CommandError("stale_identity", "github.pr.head", "Rebuild review and publication from the current task HEAD.", 3)
    if pr["head_branch"] != task["branch"] or pr["base_branch"] != task["base_branch"]:
        raise CommandError("stale_identity", "github.pr.branches", "Rebuild publication for the active task's current head and base branches.", 3)
    if hashlib.sha256(pr["body"].encode("utf-8")).hexdigest() != public["publication_body_sha256"]:
        raise CommandError("stale_identity", "publication_body_sha256", "Re-enter Delivery Review and Publish for the current PR body.", 3)
    if CLOSING_KEYWORD.search(pr["body"]):
        raise CommandError("merge_precondition_failed", "github.pr.body", "Use a Refs-only Delivery PR body without closing keywords.")

    raw_policy = gh_json(root, ["api", f"repos/{public['repo_ref']}"], "repository policy")
    if str(raw_policy.get("full_name") or public["repo_ref"]).casefold() != public["repo_ref"].casefold():
        raise CommandError("stale_identity", "github.repository", "Use the exact same-repository PR.", 3)
    policy = {
        "allow_merge_commit": bool(raw_policy.get("allow_merge_commit")),
        "allow_squash_merge": bool(raw_policy.get("allow_squash_merge")),
        "allow_rebase_merge": bool(raw_policy.get("allow_rebase_merge")),
    }
    raw_base = gh_json(
        root,
        ["api", f"repos/{public['repo_ref']}/git/ref/heads/{quote(pr['base_branch'], safe='')}"],
        "base ref",
    )
    try:
        base_ref = {"name": pr["base_branch"], "head_sha": str(raw_base["object"]["sha"])}
    except (KeyError, TypeError) as exc:
        raise CommandError(
            "github_response_incomplete", "github.base_ref", "Repair the base-ref query and reread live facts."
        ) from exc

    merge_commit = None
    if pr["state"] == "MERGED":
        if not pr["merge_commit_sha"]:
            raise CommandError("github_response_incomplete", "github.pr.merge_commit", "Reread the terminal PR facts.")
        raw_commit = gh_json(
            root,
            ["api", f"repos/{public['repo_ref']}/git/commits/{pr['merge_commit_sha']}"],
            "merge commit",
        )
        try:
            merge_commit = {
                "sha": str(raw_commit["sha"]),
                "message": str(raw_commit["message"]),
                "parents": [str(item["sha"]) for item in raw_commit["parents"]],
            }
        except (KeyError, TypeError) as exc:
            raise CommandError(
                "github_response_incomplete", "github.merge_commit", "Repair the merge-commit query and reread live facts."
            ) from exc

    blockers: list[str] = []
    if not policy["allow_merge_commit"]:
        blockers.append("unsupported_delivery_merge_policy")
    if pr["state"] == "OPEN":
        if pr["is_draft"]:
            blockers.append("pr_is_draft")
        if pr["mergeable"] != "MERGEABLE":
            blockers.append("pr_not_mergeable")
        if pr["merge_state_status"] in {"BEHIND", "BLOCKED", "DIRTY", "DRAFT", "UNKNOWN"}:
            blockers.append("merge_state_not_ready")
        states = {_check_state(item) for item in pr["checks"] if isinstance(item, dict)}
        if "failed" in states:
            blockers.append("required_checks_failed")
        elif "pending" in states:
            blockers.append("required_checks_pending")
        if pr["review_decision"] in {"CHANGES_REQUESTED", "REVIEW_REQUIRED"}:
            blockers.append("review_not_ready")
    elif pr["state"] != "MERGED":
        blockers.append("pr_not_open_or_merged")

    facts: dict[str, Any] = {
        "task": task,
        "pr": pr,
        "repository_policy": policy,
        "base_ref": base_ref,
        "merge_commit": merge_commit,
        "objective_blockers": sorted(set(blockers)),
    }
    facts["facts_sha256"] = digest(facts)
    validate_json(facts, package_root / "schemas/live-facts.schema.json", "live_facts")
    return facts


def expected_trailers(task_id: str, head: str) -> list[str]:
    return [
        f"Guru-Task-Identity: {task_id}",
        "Guru-Delivery-Schema: 1",
        f"Guru-Delivery-Head: {head}",
    ]


def validate_message(public: dict[str, Any], facts: dict[str, Any], review: dict[str, Any]) -> None:
    route = review["route"]
    if route["typed_exit"] != "delivered":
        return
    message = route["merge_message"]
    subject, body = message["subject"], message["body"]
    if "\r" in body or body.endswith("\n") or CLOSING_KEYWORD.search(subject) or CLOSING_KEYWORD.search(body):
        raise CommandError("schema_mismatch", "review_input.route.merge_message", "Use exact LF-only Refs-neutral subject/body bytes without a trailing newline.")
    lines = body.split("\n")
    trailers = expected_trailers(facts["task"]["stable_task_id"], public["expected_head_sha"])
    if len(lines) < 5 or lines[-4] != "" or lines[-3:] != trailers:
        raise CommandError("schema_mismatch", "review_input.route.merge_message.body", "End the body with one blank line and the exact three Delivery trailers.")
    for key in TRAILER_KEYS:
        if sum(line.startswith(key + ":") for line in lines) != 1:
            raise CommandError("schema_mismatch", "review_input.route.merge_message.body", "Include each Delivery trailer exactly once.")
    if not any(line.strip() for line in lines[:-4]):
        raise CommandError("schema_mismatch", "review_input.route.merge_message.body", "Provide a concrete reviewed merge body before the trailers.")


def validate_route(public: dict[str, Any], facts: dict[str, Any], review: dict[str, Any]) -> None:
    route = review["route"]
    exit_id = route["typed_exit"]
    blocked_dimensions = [item["id"] for item in review["dimensions"] if item["status"] == "blocked"]
    if exit_id == "delivered":
        if blocked_dimensions or facts["objective_blockers"]:
            raise CommandError("merge_precondition_failed", "review_input.route", "Resolve every blocker before selecting delivered.")
        if facts["pr"]["state"] not in {"OPEN", "MERGED"}:
            raise CommandError("merge_precondition_failed", "github.pr.state", "Use the current Ready/Open PR or exact merged recovery.")
        validate_message(public, facts, review)
    elif exit_id in {"implementation_required", "review_refresh_required"}:
        if not blocked_dimensions:
            raise CommandError("schema_mismatch", "review_input.dimensions", "Identify the semantic dimension that requires re-entry.")
    elif exit_id == "merge_blocked":
        if not blocked_dimensions and not facts["objective_blockers"]:
            raise CommandError("schema_mismatch", "review_input.route", "Provide one current blocker for merge_blocked.")


def action_sha(public: dict[str, Any], facts: dict[str, Any], review: dict[str, Any]) -> str:
    route = review["route"]
    return digest({
        "repo_ref": public["repo_ref"],
        "pr_number": public["pr_number"],
        "expected_head_sha": public["expected_head_sha"],
        "pre_merge_base_head": facts["base_ref"]["head_sha"],
        "merge_method": route.get("merge_method"),
        "merge_message": route.get("merge_message"),
    })


def gate_path(root: Path, public: dict[str, Any]) -> Path:
    key = hashlib.sha256(
        f"{public['task_ref']}\0{public['delivery_cycle_ref']}\0{public['repo_ref']}\0{public['pr_number']}".encode()
    ).hexdigest()[:24]
    return root / ".trellis/.runtime/guru-team/merge-task-delivery" / f"{key}.json"


def build_gate(public: dict[str, Any], facts: dict[str, Any], review: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "skill_id": "guru-merge-task-delivery",
        "public_input": public,
        "semantic_review": review,
        "pre_merge_facts": facts,
        "pre_merge_base_head": facts["base_ref"]["head_sha"],
        "action_sha256": action_sha(public, facts, review),
    }


def validate_gate(package_root: Path, gate: dict[str, Any]) -> None:
    if set(gate) != {
        "schema_version", "skill_id", "public_input", "semantic_review",
        "pre_merge_facts", "pre_merge_base_head", "action_sha256",
    }:
        raise CommandError("schema_mismatch", "gate", "Use the closed package-owned merge gate.")
    if gate.get("schema_version") != "1.0" or gate.get("skill_id") != "guru-merge-task-delivery":
        raise CommandError("schema_mismatch", "gate.identity", "Use the current package-owned merge gate.")
    public = gate.get("public_input")
    review = gate.get("semantic_review")
    facts = gate.get("pre_merge_facts")
    if not isinstance(public, dict) or not isinstance(review, dict) or not isinstance(facts, dict):
        raise CommandError("schema_mismatch", "gate", "Use the closed package-owned merge gate.")
    validate_public(package_root, public)
    validate_review(package_root, review)
    validate_json(facts, package_root / "schemas/live-facts.schema.json", "gate.pre_merge_facts")
    if gate.get("pre_merge_base_head") != facts["base_ref"]["head_sha"]:
        raise CommandError("schema_mismatch", "gate.pre_merge_base_head", "Bind the gate to the observed base head.")
    if gate.get("action_sha256") != action_sha(public, facts, review):
        raise CommandError("schema_mismatch", "gate.action_sha256", "Bind the gate to the exact reviewed action.")


def write_gate(package_root: Path, root: Path, gate: dict[str, Any]) -> Path:
    validate_gate(package_root, gate)
    path = gate_path(root, gate["public_input"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def load_gate(package_root: Path, root: Path, public: dict[str, Any], value: str | None = None) -> tuple[Path, dict[str, Any]]:
    expected = gate_path(root, public)
    path = Path(value).resolve() if value else expected
    if path != expected or not path.is_file() or path.is_symlink():
        raise CommandError("stale_identity", "gate", "Record the current merge semantic gate before execution.", 3)
    gate = load_json(root, package_root, str(path), "gate")
    validate_gate(package_root, gate)
    if gate["public_input"] != public:
        raise CommandError("stale_identity", "gate.public_input", "Record a gate for the exact current handoff.", 3)
    return path, gate


def retire_gate(path: Path) -> None:
    path.unlink(missing_ok=True)
    try:
        path.parent.rmdir()
    except OSError:
        pass


def project_nonmerge(package_root: Path, public: dict[str, Any], review: dict[str, Any]) -> dict[str, Any]:
    route = review["route"]
    exit_id = route["typed_exit"]
    if exit_id == "merge_blocked":
        output = {"exit_id": exit_id, "repo_ref": public["repo_ref"], "pr_number": public["pr_number"], "reason_code": route["reason_code"], "remediation": route["remediation"]}
        schema = "public-merge-blocked-output.schema.json"
    elif exit_id == "implementation_required":
        output = {"exit_id": exit_id, "task_ref": public["task_ref"], "finding_refs": route["finding_refs"], "resume_target": "phase-2"}
        schema = "public-implementation-required-output.schema.json"
    elif exit_id == "review_refresh_required":
        output = {"exit_id": exit_id, "task_ref": public["task_ref"], "reason_code": route["reason_code"]}
        schema = "public-review-refresh-required-output.schema.json"
    else:
        raise CommandError("schema_mismatch", "review_input.route", "Select one declared non-merge route.")
    validate_json(output, package_root / f"schemas/{schema}", "stdout")
    return output


def terminal_output(package_root: Path, public: dict[str, Any], facts: dict[str, Any], review: dict[str, Any], pre_base: str) -> dict[str, Any]:
    validate_route(public, facts, review)
    pr, commit = facts["pr"], facts["merge_commit"]
    if pr["state"] != "MERGED" or not isinstance(commit, dict) or pr["merge_commit_sha"] != commit["sha"]:
        raise CommandError("stale_identity", "github.terminal", "Reread the exact merged PR and merge commit.", 3)
    message = review["route"]["merge_message"]
    expected_message = message["subject"] + "\n\n" + message["body"]
    if commit["message"] != expected_message:
        raise CommandError("stale_identity", "github.merge_commit.message", "The merge commit message differs from the reviewed exact bytes.", 3)
    if commit["parents"] != [pre_base, public["expected_head_sha"]]:
        raise CommandError("stale_identity", "github.merge_commit.parents", "The merge commit parents do not carry the reviewed base and head.", 3)
    if facts["base_ref"]["head_sha"] != commit["sha"]:
        raise CommandError("stale_identity", "github.base_ref", "The target base does not point to the reviewed merge commit.", 3)
    validate_message(public, facts, review)
    output = {
        "exit_id": "delivered",
        "task_ref": public["task_ref"],
        "delivery_cycle_ref": public["delivery_cycle_ref"],
        "repo_ref": public["repo_ref"],
        "pr_number": public["pr_number"],
        "reviewed_head": public["expected_head_sha"],
        "merge_commit_sha": commit["sha"],
    }
    validate_json(output, package_root / "schemas/public-delivered-output.schema.json", "stdout")
    return output


def run_merge(root: Path, public: dict[str, Any], review: dict[str, Any], body_path: Path) -> None:
    message = review["route"]["merge_message"]
    body_path.parent.mkdir(parents=True, exist_ok=True)
    body_path.write_text(message["body"], encoding="utf-8")
    try:
        proc = subprocess.run(
            [
                "gh", "pr", "merge", str(public["pr_number"]), "--repo", public["repo_ref"],
                "--merge", "--match-head-commit", public["expected_head_sha"],
                "--subject", message["subject"], "--body-file", str(body_path),
            ],
            cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if proc.returncode:
            raise _github_error(proc, "pr merge")
    finally:
        body_path.unlink(missing_ok=True)


def cmd_preview(package_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(args.root)
    public = load_json(root, package_root, args.input, "input")
    facts = live_facts(root, package_root, public)
    return {"status": "previewed", "facts": facts}


def cmd_record(package_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(args.root)
    public = load_json(root, package_root, args.input, "input")
    review = load_json(root, package_root, args.review_input, "review_input")
    validate_public(package_root, public)
    validate_review(package_root, review)
    facts = live_facts(root, package_root, public)
    validate_route(public, facts, review)
    path = write_gate(package_root, root, build_gate(public, facts, review))
    return {"status": "recorded", "typed_exit": review["route"]["typed_exit"], "gate": path.relative_to(root).as_posix(), "action_sha256": action_sha(public, facts, review)}


def _check_gate_current(package_root: Path, public: dict[str, Any], facts: dict[str, Any], gate: dict[str, Any]) -> None:
    if gate["semantic_review"]["route"]["typed_exit"] == "delivered" and facts["pr"]["state"] == "MERGED":
        terminal_output(package_root, public, facts, gate["semantic_review"], gate["pre_merge_base_head"])
        return
    if facts["facts_sha256"] != gate["pre_merge_facts"]["facts_sha256"]:
        raise CommandError("stale_identity", "gate.pre_merge_facts", "Repeat the semantic review for current live facts.", 3)
    if action_sha(public, facts, gate["semantic_review"]) != gate["action_sha256"]:
        raise CommandError("stale_identity", "gate.action_sha256", "Repeat the exact merge confirmation plan.", 3)
    validate_route(public, facts, gate["semantic_review"])


def cmd_check(package_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(args.root)
    public = load_json(root, package_root, args.input, "input")
    validate_public(package_root, public)
    _path, gate = load_gate(package_root, root, public, args.gate)
    facts = live_facts(root, package_root, public)
    _check_gate_current(package_root, public, facts, gate)
    return {"status": "checked", "typed_exit": gate["semantic_review"]["route"]["typed_exit"], "action_sha256": gate["action_sha256"]}


def _execute_with_gate(package_root: Path, root: Path, public: dict[str, Any], path: Path, gate: dict[str, Any], facts: dict[str, Any]) -> dict[str, Any]:
    review = gate["semantic_review"]
    _check_gate_current(package_root, public, facts, gate)
    if review["route"]["typed_exit"] != "delivered":
        output = project_nonmerge(package_root, public, review)
        retire_gate(path)
        return output
    if facts["pr"]["state"] == "MERGED":
        output = terminal_output(package_root, public, facts, review, gate["pre_merge_base_head"])
        retire_gate(path)
        return output
    body_path = path.with_suffix(".body")
    run_merge(root, public, review, body_path)
    post = live_facts(root, package_root, public)
    output = terminal_output(package_root, public, post, review, gate["pre_merge_base_head"])
    retire_gate(path)
    return output


def cmd_execute(package_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(args.root)
    public = load_json(root, package_root, args.input, "input")
    validate_public(package_root, public)
    path, gate = load_gate(package_root, root, public, args.gate)
    facts = live_facts(root, package_root, public)
    return _execute_with_gate(package_root, root, public, path, gate, facts)


def cmd_invoke(package_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(args.root)
    public = load_json(root, package_root, args.input, "input")
    review = load_json(root, package_root, args.review_input, "review_input")
    validate_public(package_root, public)
    validate_review(package_root, review)
    facts = live_facts(root, package_root, public)
    validate_route(public, facts, review)
    path = gate_path(root, public)
    if path.exists():
        path, gate = load_gate(package_root, root, public)
        if gate["semantic_review"] != review:
            raise CommandError("stale_identity", "review_input", "Retry the exact semantic review bound to the retained gate.", 3)
        return _execute_with_gate(package_root, root, public, path, gate, facts)
    if review["route"]["typed_exit"] == "delivered" and facts["pr"]["state"] == "MERGED":
        commit = facts["merge_commit"]
        if not isinstance(commit, dict) or len(commit["parents"]) != 2:
            raise CommandError("stale_identity", "github.merge_commit.parents", "Reread the exact terminal merge commit.", 3)
        return terminal_output(package_root, public, facts, review, commit["parents"][0])
    gate = build_gate(public, facts, review)
    path = write_gate(package_root, root, gate)
    return _execute_with_gate(package_root, root, public, path, gate, facts)
