"""Package-local deterministic runtime extracted from the frozen owner implementation."""

from __future__ import annotations

import argparse

import copy

import hashlib

import ipaddress

import json

import math

import os

import re

import shlex

import shutil

import stat

import subprocess

import sys

import tempfile

import time

import unicodedata

from collections.abc import Iterable

from datetime import datetime, timezone

from pathlib import Path

from typing import Any

from urllib.parse import quote, urlsplit

DEFAULTS: dict[str, Any] = {
    "github_repo": "",
    "source_issue_required": False,
    "duplicate_search_required": True,
    "duplicate_candidate_limit": 5,
    "duplicate_high_similarity_action": "confirm",
    "branch_type_default": "chore",
    "base_branch": "",
    "base_branch_candidates": ["dev", "develop", "main", "master"],
    "workspace_mode": "worktree",
    "worktree_root": "",
    "runtime_root": ".trellis/.runtime/guru-team",
    "artifact_language": "zh-CN",
    "publish": {
        "remote": "origin",
    },
    "created_issue_labels": [],
    "closeout_markers": ["最终收口口径", "Final Closeout"],
}

TASK_PR_MERGE_GATE_ARTIFACT = "task-pr-merge-gate.json"
TASK_PR_MERGE_BODY_ARTIFACT = "merge-body.md"

PR_CLOSE_KEYWORDS = ["Closes", "Fixes", "Resolves", "Close", "Fix", "Resolve"]

class WorkflowError(RuntimeError):
    def __init__(self, message: str, exit_code: int = 1, payload: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.exit_code = exit_code
        self.payload = payload or {}

GITHUB_ERROR_CODES = {
    "cli_missing": "github_cli_missing",
    "auth_failed": "github_auth_failed",
    "repo_access_denied": "github_repo_access_denied",
    "permission_denied": "github_permission_denied",
    "api_unavailable": "github_api_unavailable",
    "response_incomplete": "github_response_incomplete",
}

def run(
    cmd: list[str],
    cwd: Path | None = None,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    process_env = None if env is None else {**os.environ, **env}
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=check,
        env=process_env,
    )

def run_stdout(
    cmd: list[str], cwd: Path | None = None, env: dict[str, str] | None = None
) -> str:
    try:
        if env is None:
            return run(cmd, cwd=cwd).stdout.strip()
        return run(cmd, cwd=cwd, env=env).stdout.strip()
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        raise WorkflowError(f"Command failed: {shlex.join(cmd)}\n{stderr}") from exc

def require_gh_auth(root: Path) -> None:
    if shutil.which("gh") is None:
        raise WorkflowError(
            "GitHub CLI is not installed or is unavailable on PATH.",
            exit_code=2,
            payload={
                "error_code": GITHUB_ERROR_CODES["cli_missing"],
                "recovery": "Install GitHub CLI, then retry the same repo-bound operation.",
            },
        )
    proc = run(["gh", "auth", "status"], cwd=root, check=False)
    if proc.returncode != 0:
        raise WorkflowError(
            "GitHub CLI authentication is unavailable or invalid.",
            exit_code=2,
            payload={
                "error_code": GITHUB_ERROR_CODES["auth_failed"],
                "recovery": "Repair authentication with `gh auth login`, verify `gh auth status`, and retry.",
            },
        )

def github_error_from_process(
    proc: subprocess.CompletedProcess[str],
    *,
    operation: str,
    repo: str,
) -> WorkflowError:
    stderr = proc.stderr.strip()
    lowered = stderr.casefold()
    if (
        "could not resolve to a repository" in lowered
        or operation == "repo_access"
        and any(token in lowered for token in ("http 404", "not found"))
    ):
        category = "repo_access_denied"
        recovery = "Verify the owner/repository identity and grant the authenticated actor repository access."
    elif any(
        token in lowered
        for token in ("http 401", "authentication", "not logged", "bad credentials", "requires authentication")
    ):
        category = "auth_failed"
        recovery = "Repair authentication with `gh auth login`, verify `gh auth status`, and retry."
    elif any(
        token in lowered
        for token in ("http 403", "forbidden", "resource not accessible", "permission", "insufficient scope")
    ):
        category = "permission_denied"
        recovery = "Grant the authenticated actor the required repository permission or scope, then retry."
    elif any(
        token in lowered
        for token in (
            "http 500", "http 502", "http 503", "http 504", "timeout", "timed out",
            "connection refused", "could not resolve host", "network is unreachable", "tls handshake",
        )
    ):
        category = "api_unavailable"
        recovery = "Retry the same repo-bound GitHub CLI operation after API or network recovery."
    elif operation == "repo_access":
        category = "repo_access_denied"
        recovery = "Verify the owner/repository identity and the authenticated actor's repository access."
    else:
        category = "api_unavailable"
        recovery = "Inspect the GitHub CLI/API failure and retry the same repo-bound operation."
    return WorkflowError(
        f"GitHub CLI operation failed for {repo}: {operation}.",
        exit_code=2,
        payload={
            "error_code": GITHUB_ERROR_CODES[category],
            "operation": operation,
            "repo": repo,
            "exit_code": proc.returncode,
            "stderr_classification": category,
            "recovery": recovery,
        },
    )

def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", '""', "''"}:
        return ""
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value

def load_config(root: Path) -> dict[str, Any]:
    config = copy.deepcopy(DEFAULTS)
    path = root / ".trellis/guru-team/config.yml"
    if not path.exists():
        return config

    current_key: str | None = None
    current_nested_key: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        text = line.strip()
        if text.startswith("- "):
            value = parse_scalar(text[2:])
            if indent >= 4 and current_key and current_nested_key and isinstance(config.get(current_key), dict):
                nested = config[current_key].setdefault(current_nested_key, [])
                if isinstance(nested, list):
                    nested.append(value)
            elif current_key:
                existing = config.setdefault(current_key, [])
                if isinstance(existing, list):
                    existing.append(value)
            continue
        if ":" not in text:
            continue
        key, value = text.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if indent == 0:
            current_key = key
            current_nested_key = None
            if value == "":
                default_value = config.get(key)
                config[key] = copy.deepcopy(default_value) if isinstance(default_value, dict) else []
            else:
                config[key] = parse_scalar(value)
        elif current_key and isinstance(config.get(current_key), dict):
            current_nested_key = key
            if value == "":
                config[current_key][key] = []
            else:
                config[current_key][key] = parse_scalar(value)
        else:
            config[key] = parse_scalar(value)
    return config

def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".trellis").is_dir():
            return candidate
    top = run_stdout(["git", "rev-parse", "--show-toplevel"], cwd=current)
    return Path(top).resolve()

def normalize_github_repository(value: Any) -> str:
    if not isinstance(value, str) or not value:
        return ""
    raw = value
    parts = raw.split("/")
    if len(parts) != 2:
        return ""
    owner, repository = parts
    component = re.compile(r"^[A-Za-z0-9_.-]+$")
    if (
        not component.fullmatch(owner)
        or not component.fullmatch(repository)
        or owner in {".", ".."}
        or repository in {".", ".."}
    ):
        return ""
    return f"{owner}/{repository}".casefold()

def git_remote_config_value_is_safe(value: Any) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and not value[0].isspace()
        and not value[-1].isspace()
        and not any(unicodedata.category(character).startswith("C") for character in value)
    )

def github_repo_binding(args: list[str], explicit_repo: str | None = None) -> str:
    repo = normalize_github_repository(explicit_repo)
    if not args:
        return ""
    if args[0] in {"issue", "pr", "run"}:
        if "--repo" not in args:
            return ""
        index = args.index("--repo")
        bound = normalize_github_repository(args[index + 1] if index + 1 < len(args) else "")
        if not bound or (repo and bound != repo):
            return ""
        return bound
    if args[0] == "api" and len(args) > 1:
        match = re.match(r"^repos/([^/]+/[^/]+)(?:/|$)", args[1])
        if not match:
            return ""
        bound = normalize_github_repository(match.group(1))
        if not bound or (repo and bound != repo):
            return ""
        return bound
    return ""

def github_response_incomplete(
    *, operation: str, repo: str, detail: str
) -> WorkflowError:
    return WorkflowError(
        f"GitHub CLI response is incomplete for {repo}: {operation}.",
        exit_code=2,
        payload={
            "error_code": GITHUB_ERROR_CODES["response_incomplete"],
            "operation": operation,
            "repo": repo,
            "detail": detail,
            "recovery": "Fail closed and repair the adapter/query contract before retrying.",
        },
    )

def gh_json(
    args: list[str],
    cwd: Path,
    *,
    repo: str | None = None,
    required_fields: tuple[str, ...] = (),
    operation: str = "read",
) -> Any:
    bound_repo = github_repo_binding(args, repo)
    if not bound_repo:
        raise github_response_incomplete(
            operation=operation,
            repo=normalize_github_repository(repo) or "<unbound>",
            detail="GitHub CLI command lacks an explicit or matching repository binding.",
        )
    require_gh_auth(cwd)
    proc = run(["gh", *args], cwd=cwd, check=False)
    if proc.returncode != 0:
        raise github_error_from_process(proc, operation=operation, repo=bound_repo)
    text = proc.stdout.strip()
    if not text:
        raise github_response_incomplete(
            operation=operation, repo=bound_repo, detail="Response body is empty."
        )
    try:
        payload = json.loads(text)
    except (json.JSONDecodeError, TypeError) as exc:
        raise github_response_incomplete(
            operation=operation, repo=bound_repo, detail="Response body is not valid JSON."
        ) from exc
    if required_fields:
        rows = payload if isinstance(payload, list) else [payload]
        if any(
            not isinstance(row, dict) or any(field not in row or row[field] is None for field in required_fields)
            for row in rows
        ):
            raise github_response_incomplete(
                operation=operation,
                repo=bound_repo,
                detail="Required fields are missing: " + ", ".join(required_fields),
            )
    return payload

def runtime_root(root: Path, config: dict[str, Any]) -> Path:
    rel = Path(str(config.get("runtime_root") or DEFAULTS["runtime_root"]))
    return rel if rel.is_absolute() else root / rel

def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkflowError(f"Required JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"Invalid JSON file: {path}\n{exc}") from exc
    if not isinstance(payload, dict):
        raise WorkflowError(f"Invalid JSON file: {path}\nJSON root must be an object.", exit_code=2)
    return payload

def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json_document_bytes(payload).decode("utf-8")
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        tmp_path.replace(path)
    finally:
        tmp_path.unlink(missing_ok=True)

def json_document_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def parse_iso_datetime(value: Any, label: str = "timestamp") -> datetime:
    text = str(value or "").strip()
    if not text:
        raise WorkflowError(f"{label} is required.", exit_code=2)
    normalized = text.removesuffix("Z") + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise WorkflowError(f"{label} must be ISO-8601: {text}", exit_code=2) from exc
    if parsed.tzinfo is None:
        raise WorkflowError(f"{label} must include a UTC offset: {text}", exit_code=2)
    return parsed.astimezone(timezone.utc)

def is_strict_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)

def repo_relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)

def canonical_json_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def parse_canonical_pull_request_url(repo: str, url: Any) -> tuple[str, int]:
    expected_repo = normalize_github_repository(repo)
    if not expected_repo or not isinstance(url, str) or not git_remote_config_value_is_safe(url):
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        )
    try:
        parsed = urlsplit(url)
    except ValueError as exc:
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        ) from exc
    parts = parsed.path.split("/")
    if (
        parsed.scheme != "https"
        or parsed.netloc != "github.com"
        or parsed.query
        or parsed.fragment
        or len(parts) != 5
        or parts[0] != ""
        or parts[3] != "pull"
        or not re.fullmatch(r"[1-9][0-9]*", parts[4])
        or normalize_github_repository(f"{parts[1]}/{parts[2]}") != expected_repo
    ):
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        )
    try:
        number = int(parts[4])
    except ValueError as exc:
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        ) from exc
    return url, number

def canonical_pull_request_url(repo: str, number: int, url: Any) -> str:
    value, parsed_number = parse_canonical_pull_request_url(repo, url)
    if isinstance(number, bool) or not isinstance(number, int) or parsed_number != number:
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        )
    return value

TASK_PR_MERGE_SCHEMA_VERSION = "2.0"

TASK_PR_MERGE_DIMENSIONS = (
    "pr_ready",
    "repository_and_head",
    "checks_and_reviews",
    "mergeability",
    "repository_policy",
    "close_scope",
)

TASK_PR_MERGE_METHOD_FLAGS = {
    "merge": "--merge",
}

TASK_PR_MERGE_STATE_STATUSES = frozenset({
    "BEHIND",
    "BLOCKED",
    "CLEAN",
    "DIRTY",
    "HAS_HOOKS",
    "UNKNOWN",
    "UNSTABLE",
})

def task_pr_merge_package_root(root: Path) -> Path:
    invoked = os.environ.get("GURU_TEAM_INVOKED_PACKAGE_ROOT", "")
    candidates = [
        Path(invoked) if invoked else None,
        root / "trellis/skills/guru-team/packages/guru-merge-task-pr",
        root / ".trellis/guru-team/skills/packages/guru-merge-task-pr",
    ]
    for candidate in candidates:
        if candidate and candidate.is_dir() and not candidate.is_symlink():
            return candidate
    raise WorkflowError("Task PR merge package root is unavailable.", exit_code=2)

def build_reviewed_merge_message(
    *,
    pull_request: int | str,
    primary_issue: int,
    summary: str,
    head_branch: str,
    base_branch: str,
) -> dict[str, Any]:
    subject = f"chore(merge): #{pull_request} 合并 #{primary_issue} {summary}"
    body = (
        "合并：\n"
        f"合入 `{head_branch}` 到 `{base_branch}`，保留 PR 内部提交历史。\n\n"
        "范围：\n"
        f"本次 PR 完成 #{primary_issue}：{summary}。\n\n"
        "审计：\n"
        "Trellis task archive、review gate、finish-summary 和 readiness 提交保留在 PR 分支历史中，用于审计任务过程。\n\n"
        f"PR: #{pull_request}\n"
        f"Refs #{primary_issue}"
    )
    return {
        "primary_issue": primary_issue,
        "summary": summary,
        "subject": subject,
        "body": body,
    }

def validate_reviewed_merge_message(
    value: Any,
    *,
    pull_request: int | str,
    head_branch: str,
    base_branch: str,
) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {
        "primary_issue", "summary", "subject", "body"
    }:
        raise WorkflowError("Reviewed merge message failed its closed contract.", exit_code=2)
    primary_issue = value.get("primary_issue")
    summary = value.get("summary")
    subject = value.get("subject")
    body = value.get("body")
    if (
        not is_strict_int(primary_issue)
        or primary_issue < 1
        or not isinstance(summary, str)
        or summary != summary.strip()
        or not summary
        or "\n" in summary
        or re.search(r"[\u3400-\u9fff]", summary) is None
        or summary.casefold() in {"todo", "tbd", "placeholder", "待补充", "占位"}
        or not isinstance(subject, str)
        or not isinstance(body, str)
    ):
        raise WorkflowError("Reviewed merge message content is invalid.", exit_code=2)
    expected = build_reviewed_merge_message(
        pull_request=pull_request,
        primary_issue=primary_issue,
        summary=summary,
        head_branch=head_branch,
        base_branch=base_branch,
    )
    if value != expected:
        raise WorkflowError(
            "Reviewed merge subject/body do not exactly match the Chinese chore(merge) contract.",
            exit_code=2,
        )
    if task_pr_merge_contains_close_keyword(subject + "\n" + body):
        raise WorkflowError("Reviewed merge message must not contain close keywords.", exit_code=2)
    return expected

def task_pr_merge_json_input(root: Path, value: str | None) -> dict[str, Any]:
    if not value:
        raise WorkflowError("Task PR merge requires --input.", exit_code=2)
    raw = Path(value)
    candidates = [raw] if raw.is_absolute() else [root / raw, task_pr_merge_package_root(root) / raw]
    path = next((candidate for candidate in candidates if candidate.is_file() and not candidate.is_symlink()), None)
    if path is None:
        raise WorkflowError("Task PR merge input is missing or unsafe.", exit_code=2)
    payload = read_json(path)
    if not isinstance(payload, dict):
        raise WorkflowError("Task PR merge input must be a JSON object.", exit_code=2)
    repo = normalize_github_repository(payload.get("repo_ref"))
    number = payload.get("pr_number")
    expected = str(payload.get("expected_head_sha") or "")
    expected_base = payload.get("expected_base_branch")
    expected_branch = payload.get("expected_head_branch")
    expected_close_issues = payload.get("expected_close_issues")
    reviewed_merge_message = payload.get("reviewed_merge_message")
    if (
        payload.get("schema_version") != TASK_PR_MERGE_SCHEMA_VERSION
        or payload.get("profile") not in {"ready_for_merge", "standalone_merge"}
        or payload.get("mode") not in {"workflow", "standalone"}
        or (payload.get("profile") == "ready_for_merge" and payload.get("mode") != "workflow")
        or (payload.get("profile") == "standalone_merge" and payload.get("mode") != "standalone")
        or not repo
        or not is_strict_int(number)
        or number < 1
        or re.fullmatch(r"[0-9a-f]{40}", expected) is None
        or not isinstance(expected_base, str)
        or not expected_base.strip()
        or not isinstance(expected_branch, str)
        or not expected_branch.strip()
        or not isinstance(expected_close_issues, list)
        or any(
            not is_strict_int(issue_number) or issue_number < 1
            for issue_number in expected_close_issues
        )
        or expected_close_issues != sorted(set(expected_close_issues))
    ):
        raise WorkflowError("Task PR merge input failed its current closed contract.", exit_code=2)
    expected_url = canonical_pull_request_url(repo, number, payload.get("pr_url"))
    reviewed_merge_message = validate_reviewed_merge_message(
        reviewed_merge_message,
        pull_request=number,
        head_branch=expected_branch,
        base_branch=expected_base,
    )
    if (
        expected_close_issues
        and reviewed_merge_message["primary_issue"] not in expected_close_issues
    ):
        raise WorkflowError(
            "Reviewed merge primary Issue is outside the reviewed close scope.",
            exit_code=2,
        )
    return {
        "schema_version": TASK_PR_MERGE_SCHEMA_VERSION,
        "profile": payload["profile"],
        "mode": payload["mode"],
        "repo_ref": repo,
        "pr_number": number,
        "pr_url": expected_url,
        "expected_head_sha": expected,
        "expected_base_branch": expected_base,
        "expected_head_branch": expected_branch,
        "expected_close_issues": expected_close_issues,
        "reviewed_merge_message": reviewed_merge_message,
    }

def task_pr_merge_close_issues(body: Any) -> list[int]:
    if not isinstance(body, str):
        raise WorkflowError("Task PR merge requires a complete PR body.", exit_code=2)
    keywords = "|".join(re.escape(item) for item in PR_CLOSE_KEYWORDS)
    values = {
        int(match.group(1))
        for match in re.finditer(
            rf"(?im)^[ \t]*(?:[-+*][ \t]+)?(?:{keywords})[ \t]+"
            rf"#([1-9][0-9]*)[ \t]*[.。]?[ \t]*$",
            body,
        )
    }
    return sorted(values)

def task_pr_merge_contains_close_keyword(value: str) -> bool:
    keywords = "|".join(re.escape(item) for item in PR_CLOSE_KEYWORDS)
    return re.search(
        rf"(?i)(?:^|[^A-Za-z])(?:{keywords})[ \t]*:?[ \t]+#[1-9][0-9]*\b",
        value,
    ) is not None

def task_pr_merge_check_rows(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        raise github_response_incomplete(
            operation="merge_preview", repo="<bound>", detail="statusCheckRollup must be an array."
        )
    rows: list[dict[str, Any]] = []
    for item in payload:
        if not isinstance(item, dict):
            raise WorkflowError("Task PR merge check row is incomplete.", exit_code=2)
        name = item.get("name") or item.get("context") or item.get("workflowName")
        state = item.get("conclusion") or item.get("state") or item.get("status")
        if not isinstance(name, str) or not name or not isinstance(state, str) or not state:
            raise WorkflowError("Task PR merge check row lacks name/state.", exit_code=2)
        rows.append({"name": name, "state": state.upper()})
    return rows

def task_pr_merge_live_facts(root: Path, public_input: dict[str, Any]) -> dict[str, Any]:
    repo = public_input["repo_ref"]
    number = public_input["pr_number"]
    pr = gh_json(
        [
            "pr", "view", str(number), "--repo", repo, "--json",
            "number,url,state,isDraft,baseRefName,headRefName,headRefOid,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup,body,mergedAt,mergeCommit",
        ],
        cwd=root,
        repo=repo,
        required_fields=(
            "number", "url", "state", "isDraft", "baseRefName", "headRefName",
            "headRefOid", "mergeable", "mergeStateStatus", "statusCheckRollup", "body",
        ),
        operation="merge_preview",
    )
    if not isinstance(pr, dict) or pr.get("number") != number:
        raise github_response_incomplete(
            operation="merge_preview", repo=repo, detail="PR identity does not match the requested number."
        )
    merge_state_status = pr.get("mergeStateStatus")
    if (
        not isinstance(merge_state_status, str)
        or merge_state_status not in TASK_PR_MERGE_STATE_STATUSES
    ):
        raise github_response_incomplete(
            operation="merge_preview",
            repo=repo,
            detail="mergeStateStatus is outside the supported GitHub enum.",
        )
    pr_url = canonical_pull_request_url(repo, number, pr.get("url"))
    policy = gh_json(
        ["api", f"repos/{repo}"],
        cwd=root,
        repo=repo,
        required_fields=("full_name", "allow_merge_commit", "allow_squash_merge", "allow_rebase_merge"),
        operation="merge_policy",
    )
    if not isinstance(policy, dict) or normalize_github_repository(policy.get("full_name")) != repo:
        raise github_response_incomplete(
            operation="merge_policy", repo=repo, detail="Repository policy identity does not match."
        )
    methods = [
        method
        for method, field in (
            ("merge", "allow_merge_commit"),
            ("squash", "allow_squash_merge"),
            ("rebase", "allow_rebase_merge"),
        )
        if policy.get(field) is True
    ]
    if not methods:
        raise WorkflowError("Repository policy exposes no supported merge method.", exit_code=2)
    base_ref = gh_json(
        [
            "api",
            f"repos/{repo}/git/ref/heads/{quote(public_input['expected_base_branch'], safe='')}",
        ],
        cwd=root,
        repo=repo,
        required_fields=("ref", "object"),
        operation="merge_base_ref",
    )
    base_object = base_ref.get("object") if isinstance(base_ref, dict) else None
    base_head_sha = base_object.get("sha") if isinstance(base_object, dict) else None
    if (
        not isinstance(base_ref, dict)
        or base_ref.get("ref") != f"refs/heads/{public_input['expected_base_branch']}"
        or not isinstance(base_head_sha, str)
        or re.fullmatch(r"[0-9a-f]{40}", base_head_sha) is None
    ):
        raise github_response_incomplete(
            operation="merge_base_ref", repo=repo, detail="Expected base ref identity is incomplete."
        )
    close_issues = task_pr_merge_close_issues(pr.get("body"))
    issues: list[dict[str, Any]] = []
    for issue_number in public_input["expected_close_issues"]:
        issue = gh_json(
            ["issue", "view", str(issue_number), "--repo", repo, "--json", "number,state,closedAt,url"],
            cwd=root,
            repo=repo,
            required_fields=("number", "state", "url"),
            operation="merge_issue_preflight",
        )
        if not isinstance(issue, dict) or issue.get("number") != issue_number:
            raise github_response_incomplete(
                operation="merge_issue_preflight", repo=repo, detail="Issue identity does not match."
            )
        issues.append({
            "number": issue_number,
            "state": str(issue.get("state") or "").upper(),
            "closed_at": issue.get("closedAt"),
            "url": issue.get("url"),
        })
    commit: dict[str, Any] | None = None
    merge_commit = pr.get("mergeCommit")
    merge_oid = merge_commit.get("oid") if isinstance(merge_commit, dict) else None
    if str(pr.get("state") or "").upper() == "MERGED":
        if not isinstance(merge_oid, str) or re.fullmatch(r"[0-9a-f]{40}", merge_oid) is None:
            raise github_response_incomplete(
                operation="merge_commit", repo=repo, detail="Merged PR lacks a complete merge commit identity."
            )
        commit_payload = gh_json(
            ["api", f"repos/{repo}/git/commits/{merge_oid}"],
            cwd=root,
            repo=repo,
            required_fields=("sha", "message", "parents"),
            operation="merge_commit",
        )
        parents_payload = commit_payload.get("parents") if isinstance(commit_payload, dict) else None
        parents = [row.get("sha") for row in parents_payload] if isinstance(parents_payload, list) else []
        message = commit_payload.get("message") if isinstance(commit_payload, dict) else None
        if (
            commit_payload.get("sha") != merge_oid
            or not isinstance(message, str)
            or len(parents) != 2
            or any(not isinstance(parent, str) or re.fullmatch(r"[0-9a-f]{40}", parent) is None for parent in parents)
        ):
            raise github_response_incomplete(
                operation="merge_commit", repo=repo, detail="Merge commit message or parent identity is incomplete."
            )
        subject, separator, body = message.partition("\n\n")
        commit = {
            "sha": merge_oid,
            "subject": subject,
            "body": body if separator else "",
            "parents": parents,
        }
    facts = {
        "schema_version": TASK_PR_MERGE_SCHEMA_VERSION,
        "skill_id": "guru-merge-task-pr",
        "repo_ref": repo,
        "pr": {
            "number": number,
            "url": pr_url,
            "state": str(pr.get("state") or "").upper(),
            "is_draft": pr.get("isDraft"),
            "base_branch": pr.get("baseRefName"),
            "head_branch": pr.get("headRefName"),
            "head_sha": pr.get("headRefOid"),
            "mergeable": str(pr.get("mergeable") or "").upper(),
            "merge_state_status": merge_state_status,
            "review_decision": str(pr.get("reviewDecision") or "").upper(),
            "checks": task_pr_merge_check_rows(pr.get("statusCheckRollup")),
            "merged_at": pr.get("mergedAt"),
            "merge_commit": pr.get("mergeCommit"),
        },
        "repository_policy": {"allowed_methods": methods},
        "base_ref": {
            "name": public_input["expected_base_branch"],
            "head_sha": base_head_sha,
        },
        "merge_commit": commit,
        "close_issues": close_issues,
        "issues": issues,
    }
    facts["facts_sha256"] = canonical_json_sha256(facts)
    return facts

def task_pr_merge_gate_path(root: Path, public_input: dict[str, Any]) -> Path:
    key = hashlib.sha256(
        f"{public_input['repo_ref']}#{public_input['pr_number']}".encode("utf-8")
    ).hexdigest()[:20]
    return runtime_root(root, load_config(root)) / "task-pr-merge" / key / TASK_PR_MERGE_GATE_ARTIFACT

def task_pr_merge_body_path(root: Path, public_input: dict[str, Any]) -> Path:
    return task_pr_merge_gate_path(root, public_input).with_name(TASK_PR_MERGE_BODY_ARTIFACT)

def task_pr_merge_cleanup_body_file(root: Path, public_input: dict[str, Any]) -> None:
    path = task_pr_merge_body_path(root, public_input)
    if path.is_symlink():
        raise WorkflowError("Task PR merge body residue is a symlink.", exit_code=2)
    if not path.exists():
        return
    if not path.is_file():
        raise WorkflowError("Task PR merge body residue is not a regular file.", exit_code=2)
    expected = public_input["reviewed_merge_message"]["body"].encode("utf-8")
    if path.read_bytes() != expected:
        raise WorkflowError("Task PR merge body residue does not match the reviewed bytes.", exit_code=2)
    path.unlink()

def task_pr_merge_materialize_body_file(root: Path, public_input: dict[str, Any]) -> Path:
    path = task_pr_merge_body_path(root, public_input)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.parent.is_symlink() or path.exists() or path.is_symlink():
        raise WorkflowError("Task PR merge body path is not clean and private.", exit_code=2)
    try:
        with path.open("x", encoding="utf-8", newline="") as handle:
            handle.write(public_input["reviewed_merge_message"]["body"])
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except BaseException:
        if path.is_file() and not path.is_symlink():
            path.unlink(missing_ok=True)
        raise
    return path

def task_pr_merge_preflight_errors(
    public_input: dict[str, Any], facts: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    pr = facts["pr"]
    if pr["state"] != "OPEN":
        errors.append("pull request is not Open")
    if pr["is_draft"] is not False:
        errors.append("pull request is still Draft")
    if pr["head_sha"] != public_input["expected_head_sha"]:
        errors.append("expected head SHA changed")
    if pr["base_branch"] != public_input["expected_base_branch"]:
        errors.append("expected base branch changed")
    if pr["head_branch"] != public_input["expected_head_branch"]:
        errors.append("expected head branch changed")
    if pr["mergeable"] != "MERGEABLE":
        errors.append("pull request is not currently mergeable")
    if facts["close_issues"] != public_input["expected_close_issues"]:
        errors.append("PR body close keywords differ from reviewed close scope")
    if facts["base_ref"]["head_sha"] == public_input["expected_head_sha"]:
        errors.append("expected base head already equals the PR head before merge")
    nonopen = [str(row["number"]) for row in facts["issues"] if row["state"] != "OPEN"]
    if nonopen:
        errors.append("close issues are not Open before merge: " + ", ".join(nonopen))
    return errors

def cmd_preview_task_pr_merge(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or "."))
    public_input = task_pr_merge_json_input(root, args.input)
    facts = task_pr_merge_live_facts(root, public_input)
    return {
        "status": "ok",
        "input": public_input,
        "facts": facts,
        "objective_blockers": task_pr_merge_preflight_errors(public_input, facts),
        "gate_path": repo_relative(root, task_pr_merge_gate_path(root, public_input)),
    }

def task_pr_merge_semantic_review(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise WorkflowError("Task PR merge semantic review must be an object.", exit_code=2)
    dimensions = value.get("dimensions")
    if not isinstance(dimensions, list):
        raise WorkflowError("Task PR merge semantic dimensions are required.", exit_code=2)
    normalized: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in dimensions:
        if not isinstance(row, dict) or set(row) != {"id", "status", "summary"}:
            raise WorkflowError("Task PR merge semantic dimension is invalid.", exit_code=2)
        identifier = row.get("id")
        status_value = row.get("status")
        summary = row.get("summary")
        if (
            identifier not in TASK_PR_MERGE_DIMENSIONS
            or identifier in seen
            or status_value not in {"passed", "blocked"}
            or not isinstance(summary, str)
            or not summary.strip()
        ):
            raise WorkflowError("Task PR merge semantic dimension is invalid.", exit_code=2)
        seen.add(identifier)
        normalized.append({"id": identifier, "status": status_value, "summary": summary})
    if seen != set(TASK_PR_MERGE_DIMENSIONS):
        raise WorkflowError("Task PR merge semantic review must cover every dimension exactly once.", exit_code=2)
    return {"dimensions": normalized}

def cmd_record_task_pr_merge(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or "."))
    public_input = task_pr_merge_json_input(root, args.input)
    facts = task_pr_merge_live_facts(root, public_input)
    review_payload = read_json(Path(args.review_input))
    review = task_pr_merge_semantic_review(review_payload.get("semantic_review"))
    route = review_payload.get("route")
    if not isinstance(route, dict) or route.get("typed_exit") not in {"merged", "merge_blocked"}:
        raise WorkflowError("Task PR merge semantic route is invalid.", exit_code=2)
    blockers = task_pr_merge_preflight_errors(public_input, facts)
    passed = all(row["status"] == "passed" for row in review["dimensions"])
    if route["typed_exit"] == "merged":
        method = route.get("merge_method")
        if (
            blockers
            or not passed
            or method not in TASK_PR_MERGE_METHOD_FLAGS
            or method not in facts["repository_policy"]["allowed_methods"]
        ):
            raise WorkflowError("Task PR merge cannot record a merge route against blocked facts.", exit_code=2)
        normalized_route = {"typed_exit": "merged", "merge_method": method}
    else:
        if passed and not blockers:
            raise WorkflowError("Task PR merge blocked route requires a real failed dimension or objective blocker.", exit_code=2)
        reason = route.get("reason_code")
        remediation = route.get("remediation")
        if not isinstance(reason, str) or not reason or not isinstance(remediation, str) or not remediation:
            raise WorkflowError("Task PR merge blocked route requires reason/remediation.", exit_code=2)
        normalized_route = {
            "typed_exit": "merge_blocked",
            "reason_code": reason,
            "remediation": remediation,
        }
    gate = {
        "schema_version": TASK_PR_MERGE_SCHEMA_VERSION,
        "skill_id": "guru-merge-task-pr",
        "input": public_input,
        "facts_sha256": facts["facts_sha256"],
        "pre_merge_base_head": facts["base_ref"]["head_sha"],
        "reviewed_message_sha256": canonical_json_sha256(public_input["reviewed_merge_message"]),
        "semantic_review": review,
        "route": normalized_route,
    }
    path = task_pr_merge_gate_path(root, public_input)
    write_json(path, gate)
    return {"status": "recorded", "gate": repo_relative(root, path), "typed_exit": normalized_route["typed_exit"]}

def task_pr_merge_gate(root: Path, public_input: dict[str, Any], value: str | None) -> tuple[Path, dict[str, Any]]:
    expected = task_pr_merge_gate_path(root, public_input)
    path = expected if not value else Path(value)
    if not path.is_absolute():
        path = root / path
    if path != expected or not path.is_file() or path.is_symlink():
        raise WorkflowError("Task PR merge gate locator is stale or unsafe.", exit_code=2)
    gate = read_json(path)
    if (
        not isinstance(gate, dict)
        or gate.get("schema_version") != TASK_PR_MERGE_SCHEMA_VERSION
        or gate.get("skill_id") != "guru-merge-task-pr"
        or gate.get("input") != public_input
        or re.fullmatch(r"[0-9a-f]{40}", str(gate.get("pre_merge_base_head") or "")) is None
        or gate.get("reviewed_message_sha256")
        != canonical_json_sha256(public_input["reviewed_merge_message"])
    ):
        raise WorkflowError("Task PR merge gate failed its current contract.", exit_code=2)
    task_pr_merge_semantic_review(gate.get("semantic_review"))
    return path, gate

def check_task_pr_merge_result(
    root: Path, public_input: dict[str, Any], gate: dict[str, Any]
) -> dict[str, Any]:
    facts = task_pr_merge_live_facts(root, public_input)
    route = gate.get("route") if isinstance(gate.get("route"), dict) else {}
    terminal = gate.get("terminal_output")
    if terminal is not None:
        output = task_pr_merge_revalidate_terminal_output(public_input, facts, gate, terminal)
        return {"status": "passed", "typed_exit": output["exit_id"], "output": output}
    if facts["pr"]["state"] == "MERGED" and route.get("typed_exit") == "merged":
        output = task_pr_merge_terminal_output(public_input, facts, gate)
        return {"status": "passed", "typed_exit": output["exit_id"], "output": output}
    if gate.get("facts_sha256") != facts["facts_sha256"]:
        raise WorkflowError("Task PR merge gate is stale against live GitHub facts.", exit_code=2)
    if gate.get("pre_merge_base_head") != facts.get("base_ref", {}).get("head_sha"):
        raise WorkflowError(
            "Task PR merge gate pre-merge base head is stale against live GitHub facts.",
            exit_code=2,
        )
    blockers = task_pr_merge_preflight_errors(public_input, facts)
    if route.get("typed_exit") == "merge_blocked":
        return {
            "status": "passed",
            "typed_exit": "merge_blocked",
            "output": {
                "exit_id": "merge_blocked",
                "reason_code": route.get("reason_code"),
                "remediation": route.get("remediation"),
            },
        }
    method = route.get("merge_method")
    if (
        blockers
        or method not in TASK_PR_MERGE_METHOD_FLAGS
        or method not in facts["repository_policy"]["allowed_methods"]
    ):
        raise WorkflowError("Task PR merge gate no longer permits execution.", exit_code=2, payload={"blockers": blockers})
    return {"status": "passed", "typed_exit": "ready_to_merge", "merge_method": method, "facts": facts}

def task_pr_merge_terminal_output(
    public_input: dict[str, Any], facts: dict[str, Any], gate: dict[str, Any]
) -> dict[str, Any]:
    pr = facts["pr"]
    if (
        pr["number"] != public_input["pr_number"]
        or pr["url"] != public_input["pr_url"]
        or pr["state"] != "MERGED"
        or not pr.get("merged_at")
        or pr["head_sha"] != public_input["expected_head_sha"]
        or pr["base_branch"] != public_input["expected_base_branch"]
        or pr["head_branch"] != public_input["expected_head_branch"]
        or facts["close_issues"] != public_input["expected_close_issues"]
    ):
        raise WorkflowError(
            "Task PR merge terminal facts no longer match the exact reviewed merge.",
            exit_code=2,
        )
    merge_commit = pr.get("merge_commit")
    merge_oid = merge_commit.get("oid") if isinstance(merge_commit, dict) else None
    if not isinstance(merge_oid, str) or re.fullmatch(r"[0-9a-f]{40}", merge_oid) is None:
        raise WorkflowError("Merged PR lacks a complete merge commit identity.", exit_code=2)
    commit = facts.get("merge_commit")
    reviewed = validate_reviewed_merge_message(
        public_input.get("reviewed_merge_message"),
        pull_request=public_input["pr_number"],
        head_branch=public_input["expected_head_branch"],
        base_branch=public_input["expected_base_branch"],
    )
    if (
        not isinstance(commit, dict)
        or commit.get("sha") != merge_oid
        or commit.get("parents")
        != [gate.get("pre_merge_base_head"), public_input["expected_head_sha"]]
        or commit.get("subject") != reviewed["subject"]
        or commit.get("body") != reviewed["body"]
        or facts.get("base_ref", {}).get("head_sha") != merge_oid
    ):
        raise WorkflowError(
            "Task PR merge commit message, parents, or remote base identity is inconsistent.",
            exit_code=2,
        )
    merged_at = parse_iso_datetime(pr["merged_at"], "pull request merged_at")
    mismatches: list[dict[str, Any]] = []
    for issue in facts["issues"]:
        closed_at = issue.get("closed_at")
        reason = None
        if issue["state"] not in {"CLOSED", "COMPLETED"}:
            reason = "not_closed_by_merge"
        elif not closed_at:
            reason = "missing_closed_at"
        elif parse_iso_datetime(closed_at, f"issue #{issue['number']} closed_at") < merged_at:
            reason = "closed_before_merge"
        if reason:
            mismatches.append({"issue_number": issue["number"], "reason_code": reason})
    output = {
        "exit_id": "closure_mismatch" if mismatches else "merged",
        "repo_ref": public_input["repo_ref"],
        "pr_number": public_input["pr_number"],
        "pr_url": public_input["pr_url"],
        "merge_commit_sha": merge_oid,
    }
    if mismatches:
        output["mismatches"] = mismatches
    return output

def task_pr_merge_revalidate_terminal_output(
    public_input: dict[str, Any], facts: dict[str, Any], gate: dict[str, Any], terminal: Any
) -> dict[str, Any]:
    if not isinstance(terminal, dict) or terminal.get("exit_id") not in {"merged", "closure_mismatch"}:
        raise WorkflowError("Task PR merge terminal output is invalid.", exit_code=2)
    current = task_pr_merge_terminal_output(public_input, facts, gate)
    if terminal != current:
        raise WorkflowError(
            "Task PR merge terminal output is stale against live merged facts.",
            exit_code=2,
        )
    return current

def cmd_check_task_pr_merge(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or "."))
    public_input = task_pr_merge_json_input(root, args.input)
    _, gate = task_pr_merge_gate(root, public_input, args.gate)
    return check_task_pr_merge_result(root, public_input, gate)

def cmd_execute_task_pr_merge(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or "."))
    public_input = task_pr_merge_json_input(root, args.input)
    gate_path, gate = task_pr_merge_gate(root, public_input, args.gate)
    task_pr_merge_cleanup_body_file(root, public_input)
    checked = check_task_pr_merge_result(root, public_input, gate)
    if checked.get("typed_exit") in {"merged", "closure_mismatch"}:
        if gate.get("terminal_output") is None:
            gate["terminal_output"] = checked["output"]
            write_json(gate_path, gate)
        return {
            "status": "recovered",
            "typed_exit": checked["typed_exit"],
            "output": checked["output"],
        }
    if checked.get("typed_exit") != "ready_to_merge":
        raise WorkflowError("Task PR merge executor requires one checked merge route.", exit_code=2)
    repo = public_input["repo_ref"]
    method = checked["merge_method"]
    if method != "merge":
        raise WorkflowError("Task PR merge executor requires the merge commit method.", exit_code=2)
    require_gh_auth(root)
    body_path = task_pr_merge_materialize_body_file(root, public_input)
    command = [
        "gh", "pr", "merge", str(public_input["pr_number"]), "--repo", repo,
        "--match-head-commit", public_input["expected_head_sha"],
        "--merge",
        "--subject", public_input["reviewed_merge_message"]["subject"],
        "--body-file", str(body_path),
    ]
    if github_repo_binding(command[1:], repo) != repo:
        raise WorkflowError("Task PR merge mutation lacks an exact repository binding.", exit_code=2)
    try:
        proc = run(command, cwd=root, check=False)
        if proc.returncode != 0:
            raise github_error_from_process(proc, operation="expected_head_merge", repo=repo)
        post = task_pr_merge_live_facts(root, public_input)
        output = task_pr_merge_terminal_output(public_input, post, gate)
    finally:
        task_pr_merge_cleanup_body_file(root, public_input)
    gate["terminal_output"] = output
    write_json(gate_path, gate)
    return {"status": "executed", "typed_exit": output["exit_id"], "output": output}

def cmd_invoke_task_pr_merge(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or "."))
    public_input = task_pr_merge_json_input(root, args.input)
    gate_path, gate = task_pr_merge_gate(root, public_input, args.gate)
    task_pr_merge_cleanup_body_file(root, public_input)
    checked = check_task_pr_merge_result(root, public_input, gate)
    if checked.get("typed_exit") == "ready_to_merge":
        raise WorkflowError("Task PR merge has not executed its checked expected-head mutation.", exit_code=2)
    output = checked.get("output")
    if not isinstance(output, dict):
        raise WorkflowError("Task PR merge typed output is unavailable.", exit_code=2)
    gate_path.unlink()
    try:
        gate_path.parent.rmdir()
    except OSError:
        pass
    return output
