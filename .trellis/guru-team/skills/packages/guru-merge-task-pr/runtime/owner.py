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

from runtime.io import CommandError

DEFAULTS: dict[str, Any] = {
    "github_repo": "",
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

PR_CLOSE_KEYWORDS = [
    "Close", "Closes", "Closed",
    "Fix", "Fixes", "Fixed",
    "Resolve", "Resolves", "Resolved",
]

class WorkflowError(CommandError):
    def __init__(
        self, message: str, exit_code: int = 2,
        payload: dict[str, Any] | None = None, *,
        code: str,
        field_path: str,
        remediation: str | None = None,
    ) -> None:
        # Only source-authored diagnostics cross the dispatcher boundary, never payloads.
        super().__init__(
            code, field_path,
            remediation or f"{message} Refresh current facts and repeat the Merge semantic review.",
            exit_status=2,
        )
        self.message = message
        self.exit_code = exit_code
        self.payload = payload or {}

    def __str__(self) -> str:
        return self.message

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
        raise WorkflowError(
            "Repository command failed.", code="merge_precondition_failed", field_path="repository",
            remediation="Check the current checkout and Git command prerequisites, then retry.",
        ) from exc

def require_gh_auth(root: Path) -> None:
    if shutil.which("gh") is None:
        raise WorkflowError(
            "GitHub CLI is not installed or is unavailable on PATH.",
            exit_code=2,
            code=GITHUB_ERROR_CODES["cli_missing"],
            field_path="github.cli",
            remediation="Install GitHub CLI, then retry the same repo-bound operation.",
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
            code=GITHUB_ERROR_CODES["auth_failed"],
            field_path="github.auth",
            remediation="Repair authentication with `gh auth login`, verify `gh auth status`, and retry.",
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
        code=GITHUB_ERROR_CODES[category],
        field_path=f"github.{category}",
        remediation=recovery,
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
        code=GITHUB_ERROR_CODES["response_incomplete"],
        field_path="github.response",
        remediation="Fail closed and repair the adapter/query contract before retrying.",
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

def read_json(path: Path, field_path: str = "input") -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkflowError(
            "Required JSON file not found.", code="invalid_arguments", field_path=field_path,
            remediation="Provide the current owner-produced JSON file at the declared input path.",
        ) from exc
    except json.JSONDecodeError as exc:
        raise WorkflowError(
            "Invalid JSON file.", code="invalid_arguments", field_path=field_path,
            remediation="Provide a complete valid JSON object from the current owner.",
        ) from exc
    if not isinstance(payload, dict):
        raise WorkflowError("JSON root must be an object.", code="invalid_arguments", field_path=field_path)
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
        raise WorkflowError("Provider timestamp is required.", code="github_response_incomplete", field_path="github.timestamp")
    normalized = text.removesuffix("Z") + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise WorkflowError("Provider timestamp must be ISO-8601.", code="github_response_incomplete", field_path="github.timestamp") from exc
    if parsed.tzinfo is None:
        raise WorkflowError("Provider timestamp must include a UTC offset.", code="github_response_incomplete", field_path="github.timestamp")
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
            code="invalid_arguments", field_path="pr_url",
        )
    try:
        parsed = urlsplit(url)
    except ValueError as exc:
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
            code="invalid_arguments", field_path="pr_url",
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
            code="invalid_arguments", field_path="pr_url",
        )
    try:
        number = int(parts[4])
    except ValueError as exc:
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
            code="invalid_arguments", field_path="pr_url",
        ) from exc
    return url, number

def canonical_pull_request_url(repo: str, number: int, url: Any) -> str:
    value, parsed_number = parse_canonical_pull_request_url(repo, url)
    if isinstance(number, bool) or not isinstance(number, int) or parsed_number != number:
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
            code="invalid_arguments", field_path="pr_url",
        )
    return value

TASK_PR_MERGE_SCHEMA_VERSION = "2.0"

TASK_PR_MERGE_DIMENSIONS = (
    "pr_ready",
    "repository_and_head",
    "checks_and_reviews",
    "mergeability",
    "repository_policy",
    "publication_effect",
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

TASK_PR_CHECK_BUCKETS = frozenset({"pass", "fail", "pending", "skipping", "cancel"})

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
    raise WorkflowError("Task PR merge package root is unavailable.", code="merge_precondition_failed", field_path="package_root")

def build_reviewed_merge_message(
    *,
    pull_request: int | str,
    summary: str,
    head_branch: str,
    base_branch: str,
) -> dict[str, Any]:
    subject = f"chore(merge): #{pull_request} {summary}"
    body = (
        "合并：\n"
        f"合入 `{head_branch}` 到 `{base_branch}`，保留 PR 内部提交历史。\n\n"
        "范围：\n"
        f"本次 PR：{summary}。\n\n"
        "审计：\n"
        "Trellis task archive、review gate、finish-summary 和 readiness 提交保留在 PR 分支历史中，用于审计任务过程。\n\n"
        f"PR: #{pull_request}"
    )
    return {
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
    if not isinstance(value, dict) or set(value) != {"summary", "subject", "body"}:
        raise WorkflowError("Reviewed merge message failed its closed contract.", code="invalid_arguments", field_path="reviewed_merge_message")
    summary = value.get("summary")
    subject = value.get("subject")
    body = value.get("body")
    if (
        not isinstance(summary, str)
        or summary != summary.strip()
        or not summary
        or "\n" in summary
        or re.search(r"[\u3400-\u9fff]", summary) is None
        or summary.casefold() in {"todo", "tbd", "placeholder", "待补充", "占位"}
        or not isinstance(subject, str)
        or not isinstance(body, str)
    ):
        raise WorkflowError("Reviewed merge message content is invalid.", code="invalid_arguments", field_path="reviewed_merge_message")
    expected = build_reviewed_merge_message(
        pull_request=pull_request,
        summary=summary,
        head_branch=head_branch,
        base_branch=base_branch,
    )
    if value != expected:
        raise WorkflowError(
            "Reviewed merge subject/body do not exactly match the Chinese chore(merge) contract.",
            exit_code=2,
            code="invalid_arguments", field_path="reviewed_merge_message",
        )
    if task_pr_merge_contains_close_keyword(subject + "\n" + body):
        raise WorkflowError("Reviewed merge message must not contain close keywords.", code="invalid_arguments", field_path="reviewed_merge_message")
    return expected

def task_pr_merge_json_input(root: Path, value: str | None) -> dict[str, Any]:
    if not value:
        raise WorkflowError("Task PR merge requires --input.", code="invalid_arguments", field_path="input")
    raw = Path(value)
    candidates = [raw] if raw.is_absolute() else [root / raw, task_pr_merge_package_root(root) / raw]
    path = next((candidate for candidate in candidates if candidate.is_file() and not candidate.is_symlink()), None)
    if path is None:
        raise WorkflowError(
            "Task PR merge input is missing or unsafe.", code="invalid_arguments", field_path="input",
            remediation="Provide the current Merge input. If a completed archive genuinely needs fresh review and its handoff is unavailable, use archived_review_request; a normally retired checkpoint alone does not require it.",
        )
    payload = read_json(path)
    if payload.get("profile") == "archived_review_request":
        return archived_review_input(payload)
    if not isinstance(payload, dict):
        raise WorkflowError("Task PR merge input must be a JSON object.", code="invalid_arguments", field_path="input")
    repo = normalize_github_repository(payload.get("repo_ref"))
    number = payload.get("pr_number")
    expected = str(payload.get("expected_head_sha") or "")
    expected_base = payload.get("expected_base_branch")
    expected_branch = payload.get("expected_head_branch")
    publication_body_sha256 = payload.get("publication_body_sha256")
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
        or (
            payload.get("profile") == "ready_for_merge"
            and re.fullmatch(r"[0-9a-f]{64}", str(publication_body_sha256 or ""))
            is None
        )
        or (
            payload.get("profile") == "standalone_merge"
            and "publication_body_sha256" in payload
        )
    ):
        raise WorkflowError("Task PR merge input failed its current closed contract.", code="invalid_arguments", field_path="input")
    expected_url = canonical_pull_request_url(repo, number, payload.get("pr_url"))
    reviewed_merge_message = validate_reviewed_merge_message(
        reviewed_merge_message,
        pull_request=number,
        head_branch=expected_branch,
        base_branch=expected_base,
    )
    normalized = {
        "schema_version": TASK_PR_MERGE_SCHEMA_VERSION,
        "profile": payload["profile"],
        "mode": payload["mode"],
        "repo_ref": repo,
        "pr_number": number,
        "pr_url": expected_url,
        "expected_head_sha": expected,
        "expected_base_branch": expected_base,
        "expected_head_branch": expected_branch,
        "reviewed_merge_message": reviewed_merge_message,
    }
    if payload["profile"] == "ready_for_merge":
        normalized["publication_body_sha256"] = publication_body_sha256
    return normalized

def task_pr_merge_pr_body_closing_issue_numbers(body: Any) -> list[int]:
    if not isinstance(body, str):
        raise WorkflowError("Task PR merge requires a complete PR body.", code="github_response_incomplete", field_path="github.pr.body")
    keywords = "|".join(re.escape(item) for item in PR_CLOSE_KEYWORDS)
    matches = list(
        re.finditer(
            rf"(?im)^[ \t]*(?:[-+*][ \t]+)?(?:{keywords})[ \t]*:?[ \t]+"
            rf"(?:(?P<repo>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+))?"
            rf"#(?P<issue>[1-9][0-9]*)[ \t]*[.。]?[ \t]*$",
            body,
        )
    )
    if any(match.group("repo") for match in matches):
        raise WorkflowError(
            "Task PR body closing effect must not contain cross-repository Issue references.",
            exit_code=2,
            code="merge_precondition_failed",
            field_path="github.pr.body",
        )
    values = {int(match.group("issue")) for match in matches}
    return sorted(values)

def task_pr_merge_contains_close_keyword(value: str) -> bool:
    keywords = "|".join(re.escape(item) for item in PR_CLOSE_KEYWORDS)
    issue_reference = (
        r"(?:#[1-9][0-9]*|"
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#[1-9][0-9]*)"
    )
    return re.search(
        rf"(?i)(?:^|[^A-Za-z])(?:{keywords})[ \t]*:?[ \t]+"
        rf"{issue_reference}\b",
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
            raise WorkflowError("Task PR merge check row is incomplete.", code="github_response_incomplete", field_path="github.pr.statusCheckRollup")
        name = item.get("name") or item.get("context") or item.get("workflowName")
        state = item.get("conclusion") or item.get("state") or item.get("status")
        if not isinstance(name, str) or not name or not isinstance(state, str) or not state:
            raise WorkflowError("Task PR merge check row lacks name/state.", code="github_response_incomplete", field_path="github.pr.statusCheckRollup")
        rows.append({"name": name, "state": state.upper()})
    return rows

def task_pr_merge_live_facts(root: Path, public_input: dict[str, Any]) -> dict[str, Any]:
    repo = public_input["repo_ref"]
    number = public_input["pr_number"]
    archived = public_input.get("profile") == "archived_review_request"
    pr = gh_json(
        [
            "pr", "view", str(number), "--repo", repo, "--json",
            "number,url,state,isDraft,baseRefName,headRefName,headRefOid,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup,body,mergedAt,mergeCommit" + (",title" if archived else ""),
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
    body = pr.get("body")
    if not isinstance(body, str):
        raise WorkflowError("Task PR merge requires a complete PR body.", code="github_response_incomplete", field_path="github.pr.body")
    if archived and (pr.get("state") != "OPEN" or pr.get("isDraft") is not False):
        raise WorkflowError("Archived review requires a Ready Open PR.", code="merge_precondition_failed", field_path="github.pr.state")
    if archived and not isinstance(pr.get("title"), str):
        raise WorkflowError("Archived review requires the complete PR title.", code="github_response_incomplete", field_path="github.pr.title")
    if public_input.get("profile") == "ready_for_merge":
        live_body_sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()
        if live_body_sha256 != public_input.get("publication_body_sha256"):
            raise WorkflowError(
                "Task PR body differs from the Publication-reviewed bytes.",
                exit_code=2,
                code="stale_identity",
                field_path="publication_body_sha256",
                remediation="Return to the Publication owner for current payload review, then rebuild the Finalizer handoff and Merge input.",
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
        raise WorkflowError("Repository policy exposes no supported merge method.", code="merge_precondition_failed", field_path="repository_policy.allowed_methods")
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
    pr_body_closing_issue_numbers = task_pr_merge_pr_body_closing_issue_numbers(body)
    issues: list[dict[str, Any]] = []
    for issue_number in pr_body_closing_issue_numbers if str(pr.get("state") or "").upper() == "MERGED" else []:
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
        "pr_body_closing_issue_numbers": pr_body_closing_issue_numbers,
        "issues": issues,
    }
    if archived:
        facts["pr_payload_snapshot_sha256"] = canonical_json_sha256({"title": pr["title"], "body": body})
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
        raise WorkflowError("Task PR merge body residue is a symlink.", code="merge_precondition_failed", field_path="merge_body")
    if not path.exists():
        return
    if not path.is_file():
        raise WorkflowError("Task PR merge body residue is not a regular file.", code="merge_precondition_failed", field_path="merge_body")
    expected = public_input["reviewed_merge_message"]["body"].encode("utf-8")
    if path.read_bytes() != expected:
        raise WorkflowError("Task PR merge body residue does not match the reviewed bytes.", code="stale_identity", field_path="merge_body")
    path.unlink()

def task_pr_merge_materialize_body_file(root: Path, public_input: dict[str, Any]) -> Path:
    path = task_pr_merge_body_path(root, public_input)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.parent.is_symlink() or path.exists() or path.is_symlink():
        raise WorkflowError("Task PR merge body path is not clean and private.", code="merge_precondition_failed", field_path="merge_body")
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
    if facts["base_ref"]["head_sha"] == public_input["expected_head_sha"]:
        errors.append("expected base head already equals the PR head before merge")
    return errors


def task_pr_merge_gate_from_facts(
    public_input: dict[str, Any], facts: dict[str, Any], review_payload: Any
) -> dict[str, Any]:
    if not isinstance(review_payload, dict):
        raise WorkflowError("Task PR merge semantic review input must be an object.", code="invalid_arguments", field_path="review_input")
    review = task_pr_merge_semantic_review(review_payload.get("semantic_review"))
    route = review_payload.get("route")
    if not isinstance(route, dict) or route.get("typed_exit") not in {
        "merged", "merge_blocked", "phase2_reentry_required"
    }:
        raise WorkflowError("Task PR merge semantic route is invalid.", code="invalid_arguments", field_path="review_input.route")
    blockers = task_pr_merge_preflight_errors(public_input, facts)
    passed = all(row["status"] == "passed" for row in review["dimensions"])
    if route["typed_exit"] == "phase2_reentry_required":
        normalized_route = task_pr_merge_phase2_reentry_route(public_input, facts, review, route)
    elif route["typed_exit"] == "merged":
        method = route.get("merge_method")
        if (
            blockers
            or not passed
            or method not in TASK_PR_MERGE_METHOD_FLAGS
            or method not in facts["repository_policy"]["allowed_methods"]
        ):
            raise WorkflowError("Task PR merge cannot record a merge route against blocked facts.", code="merge_precondition_failed", field_path="review_input.route")
        normalized_route = {"typed_exit": "merged", "merge_method": method}
    else:
        if passed and not blockers:
            raise WorkflowError("Task PR merge blocked route requires a real failed dimension or objective blocker.", code="merge_precondition_failed", field_path="review_input.route")
        reason = route.get("reason_code")
        remediation = route.get("remediation")
        if not isinstance(reason, str) or not reason or not isinstance(remediation, str) or not remediation:
            raise WorkflowError("Task PR merge blocked route requires reason/remediation.", code="invalid_arguments", field_path="review_input.route")
        normalized_route = {
            "typed_exit": "merge_blocked",
            "reason_code": reason,
            "remediation": remediation,
        }
    return {
        "schema_version": TASK_PR_MERGE_SCHEMA_VERSION,
        "skill_id": "guru-merge-task-pr",
        "input": public_input,
        "facts_sha256": facts["facts_sha256"],
        "pre_merge_base_head": facts["base_ref"]["head_sha"],
        "reviewed_message_sha256": canonical_json_sha256(public_input["reviewed_merge_message"]),
        "semantic_review": review,
        "route": normalized_route,
    }


def task_pr_merge_phase2_reentry_route(
    public_input: dict[str, Any],
    facts: dict[str, Any],
    review: dict[str, Any],
    route: dict[str, Any],
) -> dict[str, Any]:
    """Validate the semantic handoff without deciding task scope in code."""
    required = {
        "typed_exit", "scope_classification", "requires_task_content_change",
        "blocked_dimension", "repo_ref", "pr_number", "pr_url",
        "expected_head_sha", "expected_base_branch", "expected_head_branch",
        "task_id", "archive_locator", "active_locator",
        "archive_commit", "finding_refs", "resume_target",
    }
    if set(route) != required:
        raise WorkflowError("Task PR phase-2 re-entry route is incomplete.", code="invalid_arguments", field_path="review_input.route")
    if route["scope_classification"] != "task_work" or route["requires_task_content_change"] is not True:
        raise WorkflowError("Task PR phase-2 re-entry requires a task-work content finding.", code="merge_precondition_failed", field_path="review_input.route.requires_task_content_change")
    if route["resume_target"] != "phase-2":
        raise WorkflowError("Task PR phase-2 re-entry has an invalid resume target.", code="invalid_arguments", field_path="review_input.route.resume_target")
    if route["blocked_dimension"] not in TASK_PR_MERGE_DIMENSIONS:
        raise WorkflowError("Task PR phase-2 re-entry has an invalid blocked dimension.", code="invalid_arguments", field_path="review_input.route.blocked_dimension")
    dimensions = {row["id"]: row for row in review["dimensions"]}
    if dimensions[route["blocked_dimension"]]["status"] != "blocked":
        raise WorkflowError("Task PR phase-2 re-entry requires a blocked semantic dimension.", code="merge_precondition_failed", field_path="review_input.route.blocked_dimension")

    identity = {
        "repo_ref": public_input["repo_ref"],
        "pr_number": public_input["pr_number"],
        "pr_url": public_input["pr_url"],
        "expected_head_sha": public_input["expected_head_sha"],
        "expected_base_branch": public_input["expected_base_branch"],
        "expected_head_branch": public_input["expected_head_branch"],
    }
    if any(route[key] != value for key, value in identity.items()):
        raise WorkflowError("Task PR phase-2 re-entry route does not match PR identity.", code="stale_identity", field_path="review_input.route")
    pr = facts["pr"]
    if (
        pr["state"] != "OPEN"
        or pr["number"] != public_input["pr_number"]
        or pr["url"] != public_input["pr_url"]
        or pr["head_sha"] != public_input["expected_head_sha"]
        or pr["base_branch"] != public_input["expected_base_branch"]
        or pr["head_branch"] != public_input["expected_head_branch"]
    ):
        raise WorkflowError("Task PR phase-2 re-entry route is stale against live PR identity.", code="stale_identity", field_path="review_input.route")

    task_id = route["task_id"]
    if not isinstance(task_id, str) or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", task_id) is None:
        raise WorkflowError("Task PR phase-2 re-entry task identity is invalid.", code="invalid_arguments", field_path="review_input.route.task_id")
    archive_locator = route["archive_locator"]
    active_locator = route["active_locator"]
    if (
        not isinstance(archive_locator, str)
        or re.fullmatch(r"\.trellis/tasks/archive/[0-9]{4}-[0-9]{2}/[A-Za-z0-9][A-Za-z0-9._-]*", archive_locator) is None
        or not isinstance(active_locator, str)
        or re.fullmatch(r"\.trellis/tasks/[A-Za-z0-9][A-Za-z0-9._-]*", active_locator) is None
    ):
        raise WorkflowError("Task PR phase-2 re-entry task locators are invalid.", code="invalid_arguments", field_path="review_input.route.archive_locator")
    archive_commit = route["archive_commit"]
    finding_refs = route["finding_refs"]
    if (
        not isinstance(archive_commit, str)
        or re.fullmatch(r"[0-9a-f]{40}", archive_commit) is None
        or not isinstance(finding_refs, list)
        or not finding_refs
        or any(not isinstance(ref, str) or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]*", ref) is None for ref in finding_refs)
        or finding_refs != sorted(set(finding_refs))
    ):
        raise WorkflowError("Task PR phase-2 re-entry archive or finding identity is invalid.", code="invalid_arguments", field_path="review_input.route")
    return {
        "typed_exit": "phase2_reentry_required",
        "scope_classification": "task_work",
        "requires_task_content_change": True,
        "blocked_dimension": route["blocked_dimension"],
        "repo_ref": public_input["repo_ref"],
        "pr_number": public_input["pr_number"],
        "pr_url": public_input["pr_url"],
        "expected_head_sha": public_input["expected_head_sha"],
        "expected_base_branch": public_input["expected_base_branch"],
        "expected_head_branch": public_input["expected_head_branch"],
        "task_id": task_id,
        "archive_locator": archive_locator,
        "active_locator": active_locator,
        "archive_commit": archive_commit,
        "finding_refs": finding_refs,
        "resume_target": "phase-2",
    }


def task_pr_merge_recovery_gate_from_merged_facts(
    public_input: dict[str, Any], facts: dict[str, Any], review_payload: Any
) -> dict[str, Any]:
    if not isinstance(review_payload, dict):
        raise WorkflowError("Task PR merge semantic review input must be an object.", code="invalid_arguments", field_path="review_input")
    review = task_pr_merge_semantic_review(review_payload.get("semantic_review"))
    route = review_payload.get("route")
    if (
        not isinstance(route, dict)
        or route.get("typed_exit") != "merged"
        or route.get("merge_method") != "merge"
        or any(row["status"] != "passed" for row in review["dimensions"])
        or "merge" not in facts.get("repository_policy", {}).get("allowed_methods", [])
    ):
        raise WorkflowError(
            "Task PR merge recovery requires the exact passed merge route.",
            exit_code=2,
            code="merge_precondition_failed",
            field_path="review_input.route",
        )
    commit = facts.get("merge_commit")
    parents = commit.get("parents") if isinstance(commit, dict) else None
    pre_merge_base_head = parents[0] if isinstance(parents, list) and len(parents) == 2 else None
    if (
        not isinstance(pre_merge_base_head, str)
        or re.fullmatch(r"[0-9a-f]{40}", pre_merge_base_head) is None
    ):
        raise WorkflowError(
            "Task PR merge recovery lacks the exact pre-merge base parent.",
            exit_code=2,
            code="github_response_incomplete", field_path="facts.merge_commit.parents",
        )
    facts_sha256 = facts.get("facts_sha256")
    if not isinstance(facts_sha256, str) or re.fullmatch(r"[0-9a-f]{64}", facts_sha256) is None:
        raise WorkflowError("Task PR merge recovery facts are incomplete.", code="github_response_incomplete", field_path="facts")
    return {
        "schema_version": TASK_PR_MERGE_SCHEMA_VERSION,
        "skill_id": "guru-merge-task-pr",
        "input": public_input,
        "facts_sha256": facts_sha256,
        "pre_merge_base_head": pre_merge_base_head,
        "reviewed_message_sha256": canonical_json_sha256(public_input["reviewed_merge_message"]),
        "semantic_review": review,
        "route": {"typed_exit": "merged", "merge_method": "merge"},
    }

def cmd_preview_task_pr_merge(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or "."))
    public_input = task_pr_merge_json_input(root, args.input)
    if public_input.get("profile") == "archived_review_request":
        facts = archived_review_facts(root, public_input)
        return {"status": "ok", "input": public_input, "facts": facts,
                "objective_blockers": facts["objective_blockers"],
                "gate_path": repo_relative(root, archived_review_gate_path(root, public_input))}
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
        raise WorkflowError("Task PR merge semantic review must be an object.", code="invalid_arguments", field_path="review_input.semantic_review")
    dimensions = value.get("dimensions")
    if not isinstance(dimensions, list):
        raise WorkflowError("Task PR merge semantic dimensions are required.", code="invalid_arguments", field_path="review_input.semantic_review.dimensions")
    normalized: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in dimensions:
        if not isinstance(row, dict) or set(row) != {"id", "status", "summary"}:
            raise WorkflowError("Task PR merge semantic dimension is invalid.", code="invalid_arguments", field_path="review_input.semantic_review.dimensions")
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
            raise WorkflowError("Task PR merge semantic dimension is invalid.", code="invalid_arguments", field_path="review_input.semantic_review.dimensions")
        seen.add(identifier)
        normalized.append({"id": identifier, "status": status_value, "summary": summary})
    if seen != set(TASK_PR_MERGE_DIMENSIONS):
        raise WorkflowError("Task PR merge semantic review must cover every dimension exactly once.", code="invalid_arguments", field_path="review_input.semantic_review.dimensions")
    return {"dimensions": normalized}

def cmd_record_task_pr_merge(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or "."))
    public_input = task_pr_merge_json_input(root, args.input)
    if public_input.get("profile") == "archived_review_request":
        gate = archived_review_record(root, public_input, read_json(Path(args.review_input), "review_input"))
        return {"status": "recorded", "gate": repo_relative(root, archived_review_gate_path(root, public_input)),
                "typed_exit": gate["route"]["typed_exit"]}
    facts = task_pr_merge_live_facts(root, public_input)
    gate = task_pr_merge_gate_from_facts(
        public_input, facts, read_json(Path(args.review_input), "review_input")
    )
    path = task_pr_merge_gate_path(root, public_input)
    write_json(path, gate)
    return {
        "status": "recorded",
        "gate": repo_relative(root, path),
        "typed_exit": gate["route"]["typed_exit"],
    }

def task_pr_merge_gate(root: Path, public_input: dict[str, Any], value: str | None) -> tuple[Path, dict[str, Any]]:
    expected = task_pr_merge_gate_path(root, public_input)
    path = expected if not value else Path(value)
    if not path.is_absolute():
        path = root / path
    if path != expected or not path.is_file() or path.is_symlink():
        raise WorkflowError(
            "Task PR merge gate locator is stale or unsafe.", code="stale_identity", field_path="gate",
            remediation="Repeat the current Merge semantic review and record its gate at the owner path.",
        )
    gate = read_json(path, "gate")
    if (
        not isinstance(gate, dict)
        or gate.get("schema_version") != TASK_PR_MERGE_SCHEMA_VERSION
        or gate.get("skill_id") != "guru-merge-task-pr"
        or gate.get("input") != public_input
        or re.fullmatch(r"[0-9a-f]{40}", str(gate.get("pre_merge_base_head") or "")) is None
        or gate.get("reviewed_message_sha256")
        != canonical_json_sha256(public_input["reviewed_merge_message"])
    ):
        raise WorkflowError(
            "Task PR merge gate failed its current contract.", code="stale_identity", field_path="gate.input",
            remediation="Rebuild current Merge input and repeat the Merge semantic review and recording.",
        )
    task_pr_merge_semantic_review(gate.get("semantic_review"))
    return path, gate

def check_task_pr_merge_result(
    root: Path, public_input: dict[str, Any], gate: dict[str, Any]
) -> dict[str, Any]:
    facts = task_pr_merge_live_facts(root, public_input)
    return check_task_pr_merge_result_with_facts(public_input, gate, facts)


def check_task_pr_merge_result_with_facts(
    public_input: dict[str, Any], gate: dict[str, Any], facts: dict[str, Any]
) -> dict[str, Any]:
    route = gate.get("route") if isinstance(gate.get("route"), dict) else {}
    terminal = gate.get("terminal_output")
    if terminal is not None:
        output = task_pr_merge_revalidate_terminal_output(public_input, facts, gate, terminal)
        return {"status": "passed", "typed_exit": output["exit_id"], "output": output}
    if facts["pr"]["state"] == "MERGED" and route.get("typed_exit") == "merged":
        output = task_pr_merge_terminal_output(public_input, facts, gate)
        return {"status": "passed", "typed_exit": output["exit_id"], "output": output}
    if gate.get("facts_sha256") != facts["facts_sha256"]:
        raise WorkflowError(
            "Task PR merge gate is stale against live GitHub facts.", code="stale_identity", field_path="gate.facts_sha256",
            remediation="Refresh live GitHub facts and repeat the Merge semantic review before recording a current gate.",
        )
    if gate.get("pre_merge_base_head") != facts.get("base_ref", {}).get("head_sha"):
        raise WorkflowError(
            "Task PR merge gate pre-merge base head is stale against live GitHub facts.",
            exit_code=2,
            code="stale_identity",
            field_path="gate.pre_merge_base_head",
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
    if route.get("typed_exit") == "phase2_reentry_required":
        normalized_route = task_pr_merge_phase2_reentry_route(public_input, facts, gate["semantic_review"], route)
        return {
            "status": "passed",
            "typed_exit": "phase2_reentry_required",
            "output": task_pr_merge_phase2_reentry_output(normalized_route),
        }
    method = route.get("merge_method")
    if (
        blockers
        or method not in TASK_PR_MERGE_METHOD_FLAGS
        or method not in facts["repository_policy"]["allowed_methods"]
    ):
        raise WorkflowError("Task PR merge gate no longer permits execution.", code="merge_precondition_failed", field_path="gate.route", payload={"blockers": blockers})
    return {"status": "passed", "typed_exit": "ready_to_merge", "merge_method": method, "facts": facts}


def task_pr_merge_retire_terminal_state(
    root: Path, public_input: dict[str, Any], gate_path: Path
) -> None:
    task_pr_merge_cleanup_body_file(root, public_input)
    gate_path.unlink(missing_ok=True)
    try:
        gate_path.parent.rmdir()
    except OSError:
        pass


def task_pr_merge_phase2_reentry_output(route: dict[str, Any]) -> dict[str, Any]:
    return {
        "exit_id": "phase2_reentry_required",
        "repo_ref": route["repo_ref"],
        "pr_number": route["pr_number"],
        "pr_url": route["pr_url"],
        "expected_head_sha": route["expected_head_sha"],
        "expected_base_branch": route["expected_base_branch"],
        "expected_head_branch": route["expected_head_branch"],
        "task_id": route["task_id"],
        "archive_locator": route["archive_locator"],
        "active_locator": route["active_locator"],
        "archive_commit": route["archive_commit"],
        "finding_refs": route["finding_refs"],
        "resume_target": route["resume_target"],
    }


def task_pr_merge_execute_checked(
    root: Path,
    public_input: dict[str, Any],
    gate_path: Path,
    gate: dict[str, Any],
    checked: dict[str, Any],
) -> dict[str, Any]:
    if checked.get("typed_exit") == "phase2_reentry_required":
        return {
            "status": "routed",
            "typed_exit": "phase2_reentry_required",
            "output": checked["output"],
        }
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
        raise WorkflowError("Task PR merge executor requires one checked merge route.", code="merge_precondition_failed", field_path="gate.route")
    repo = public_input["repo_ref"]
    method = checked["merge_method"]
    if method != "merge":
        raise WorkflowError("Task PR merge executor requires the merge commit method.", code="merge_precondition_failed", field_path="gate.route.merge_method")
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
        raise WorkflowError("Task PR merge mutation lacks an exact repository binding.", code="invalid_arguments", field_path="repo_ref")
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
    ):
        raise WorkflowError(
            "Task PR merge terminal facts no longer match the exact reviewed merge.",
            exit_code=2,
            code="stale_identity", field_path="facts.pr",
        )
    merge_commit = pr.get("merge_commit")
    merge_oid = merge_commit.get("oid") if isinstance(merge_commit, dict) else None
    if not isinstance(merge_oid, str) or re.fullmatch(r"[0-9a-f]{40}", merge_oid) is None:
        raise WorkflowError("Merged PR lacks a complete merge commit identity.", code="github_response_incomplete", field_path="github.pr.mergeCommit")
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
            code="stale_identity", field_path="facts.merge_commit",
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
        raise WorkflowError("Task PR merge terminal output is invalid.", code="merge_precondition_failed", field_path="terminal_output")
    current = task_pr_merge_terminal_output(public_input, facts, gate)
    if terminal != current:
        raise WorkflowError(
            "Task PR merge terminal output is stale against live merged facts.",
            exit_code=2,
            code="stale_identity", field_path="terminal_output",
        )
    return current

def cmd_check_task_pr_merge(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or "."))
    public_input = task_pr_merge_json_input(root, args.input)
    if public_input.get("profile") == "archived_review_request":
        return archived_review_check(root, public_input, args.gate)[1]
    _, gate = task_pr_merge_gate(root, public_input, args.gate)
    return check_task_pr_merge_result(root, public_input, gate)

def cmd_execute_task_pr_merge(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or "."))
    public_input = task_pr_merge_json_input(root, args.input)
    if public_input.get("profile") == "archived_review_request":
        path, checked = archived_review_check(root, public_input, args.gate)
        path.unlink()
        return {"status": "executed", "typed_exit": checked["typed_exit"], "output": checked["output"]}
    gate_path, gate = task_pr_merge_gate(root, public_input, args.gate)
    task_pr_merge_cleanup_body_file(root, public_input)
    checked = check_task_pr_merge_result(root, public_input, gate)
    return task_pr_merge_execute_checked(root, public_input, gate_path, gate, checked)


def _cmd_invoke_task_pr_merge_happy_path(args: argparse.Namespace) -> dict[str, Any]:
    """Run the original public entry's one-snapshot-pair merge transaction."""
    root = repo_root(Path(args.root or "."))
    public_input = task_pr_merge_json_input(root, args.input)
    if public_input.get("profile") == "archived_review_request":
        return archived_review_invoke(root, public_input, read_json(Path(args.review_input), "review_input"))
    gate_path = task_pr_merge_gate_path(root, public_input)
    task_pr_merge_cleanup_body_file(root, public_input)

    if gate_path.exists():
        gate_path, gate = task_pr_merge_gate(root, public_input, None)
        pre = task_pr_merge_live_facts(root, public_input)
    else:
        pre = task_pr_merge_live_facts(root, public_input)
        review_payload = read_json(Path(args.review_input), "review_input")
        if pre["pr"]["state"] == "MERGED":
            gate = task_pr_merge_recovery_gate_from_merged_facts(
                public_input, pre, review_payload
            )
            return task_pr_merge_terminal_output(public_input, pre, gate)
        gate = task_pr_merge_gate_from_facts(
            public_input, pre, review_payload
        )
        write_json(gate_path, gate)

    checked = check_task_pr_merge_result_with_facts(public_input, gate, pre)
    if checked.get("typed_exit") == "merge_blocked":
        output = checked["output"]
        task_pr_merge_retire_terminal_state(root, public_input, gate_path)
        return output
    if checked.get("typed_exit") == "phase2_reentry_required":
        output = checked["output"]
        task_pr_merge_retire_terminal_state(root, public_input, gate_path)
        return output

    completed = task_pr_merge_execute_checked(
        root, public_input, gate_path, gate, checked
    )
    output = completed.get("output")
    if not isinstance(output, dict) or output.get("exit_id") not in {
        "merged", "closure_mismatch"
    }:
        raise WorkflowError("Task PR merge public invocation terminal output is unavailable.", code="merge_precondition_failed", field_path="terminal_output")
    task_pr_merge_retire_terminal_state(root, public_input, gate_path)
    return output

def cmd_invoke_task_pr_merge(args: argparse.Namespace) -> dict[str, Any]:
    return _cmd_invoke_task_pr_merge_happy_path(args)


def task_pr_merge_required_checks(
    root: Path, repo: str, pr_number: int
) -> list[dict[str, str]]:
    require_gh_auth(root)
    command = [
        "gh", "pr", "checks", str(pr_number), "--repo", repo,
        "--required", "--json", "name,state,bucket",
    ]
    if github_repo_binding(command[1:], repo) != repo:
        raise WorkflowError("Task PR check watcher lacks an exact repository binding.", code="invalid_arguments", field_path="repo_ref")
    proc = run(command, cwd=root, check=False)
    if proc.returncode not in {0, 8}:
        if "no checks reported" in proc.stderr.casefold():
            return []
        raise github_error_from_process(proc, operation="required_checks_watch", repo=repo)
    try:
        payload = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise github_response_incomplete(
            operation="required_checks_watch", repo=repo, detail="Required check response is not JSON."
        ) from exc
    if not isinstance(payload, list):
        raise github_response_incomplete(
            operation="required_checks_watch", repo=repo, detail="Required check response is not an array."
        )
    rows: list[dict[str, str]] = []
    for item in payload:
        if not isinstance(item, dict):
            raise WorkflowError("Task PR required check row is incomplete.", code="github_response_incomplete", field_path="github.checks")
        name = item.get("name")
        state = item.get("state")
        bucket = item.get("bucket")
        if (
            not isinstance(name, str) or not name
            or not isinstance(state, str) or not state
            or bucket not in TASK_PR_CHECK_BUCKETS
        ):
            raise WorkflowError("Task PR required check row lacks name/state/bucket.", code="github_response_incomplete", field_path="github.checks")
        rows.append({"name": name, "state": state, "bucket": bucket})
    return sorted(rows, key=lambda row: (row["name"], row["state"], row["bucket"]))


def archived_review_input(payload: dict[str, Any]) -> dict[str, Any]:
    required = {"schema_version", "profile", "mode", "task_ref", "repo_ref", "pr_number", "expected_head_sha"}
    if (
        set(payload) != required or payload.get("schema_version") != "2.0"
        or payload.get("profile") != "archived_review_request"
        or payload.get("mode") not in {"workflow", "standalone"}
        or not normalize_github_repository(payload.get("repo_ref"))
        or not is_strict_int(payload.get("pr_number")) or payload["pr_number"] < 1
        or re.fullmatch(r"[0-9a-f]{40}", str(payload.get("expected_head_sha") or "")) is None
        or re.fullmatch(r"\.trellis/tasks/archive/[0-9]{4}-[0-9]{2}/[A-Za-z0-9][A-Za-z0-9._-]*", str(payload.get("task_ref") or "")) is None
    ):
        raise WorkflowError("Archived review input failed its closed contract.", code="invalid_arguments", field_path="input")
    return {**payload, "repo_ref": normalize_github_repository(payload["repo_ref"])}


def archived_review_require(condition: bool, field: str) -> None:
    if not condition:
        raise WorkflowError(
            "Archived review identity or prerequisite is not current.", code="stale_identity", field_path=field,
            remediation="Verify the exact completed archive, mappings, checkout and Ready PR. Resolve missing or stale prerequisites with their owner before requesting read-only archived review; do not edit archive state.",
        )


def archived_review_mappings(root: Path, public_input: dict[str, Any], task: dict[str, Any]) -> None:
    config = load_config(root)
    task_id = task.get("id")
    archived_review_require(isinstance(task_id, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", task_id) is not None, "task.id")
    runtime = runtime_root(root, config)
    mapping = read_json(runtime / "tasks" / f"{task_id}.json", "task_mapping")
    slug = mapping.get("workspace_slug")
    archived_review_require(isinstance(slug, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", slug) is not None, "task_mapping.workspace_slug")
    workspace = read_json(runtime / "workspaces" / f"{slug}.json", "workspace_mapping")
    source = workspace.get("source_checkout")
    archived_review_require(isinstance(source, str) and Path(source).is_absolute() and Path(source).is_dir(), "workspace_mapping.source_checkout")
    records = []
    for block in run_stdout(["git", "worktree", "list", "--porcelain"], cwd=root).split("\n\n"):
        records.append(dict(line.split(" ", 1) for line in block.splitlines() if " " in line))
    matches = [row for row in records if row.get("branch") == f"refs/heads/{task['branch']}"]
    archived_review_require(len(matches) == 1 and Path(matches[0]["worktree"]).resolve() == root, "worktree.branch")
    archived_review_require(any(Path(row.get("worktree", "")).resolve() == Path(source).resolve() for row in records), "worktree.source_checkout")
    expected_task = {"schema_version": "1.0", "task_slug": task_id, "workspace_slug": slug,
                     "workspace_path": str(root), "task_artifact_dir": public_input["task_ref"]}
    expected_workspace = {"schema_version": "1.0", "workspace_slug": slug, "workspace_path": str(root),
                          "branch_name": task["branch"], "source_checkout": source}
    for checkout in {root, Path(source).resolve()}:
        mapped_root = runtime_root(checkout, config)
        current_task = read_json(mapped_root / "tasks" / f"{task_id}.json", "task_mapping")
        current_workspace = read_json(mapped_root / "workspaces" / f"{slug}.json", "workspace_mapping")
        archived_review_require(all(current_task.get(key) == value for key, value in expected_task.items()), "task_mapping")
        archived_review_require(all(current_workspace.get(key) == value for key, value in expected_workspace.items()), "workspace_mapping")


def archived_review_local(root: Path, public_input: dict[str, Any]) -> dict[str, Any]:
    root = root.resolve()
    ref = public_input["task_ref"]
    archived_review_require(not run_stdout(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=root), "worktree.clean")
    head = run_stdout(["git", "rev-parse", "HEAD"], cwd=root)
    archived_review_require(head == public_input["expected_head_sha"], "expected_head_sha")
    core = {"task.json", "prd.md", "design.md", "implement.md", "finish-summary.json"}
    tracked = run_stdout(["git", "ls-tree", "-r", "--name-only", "HEAD", "--", ref], cwd=root).splitlines()
    archived_review_require(set(tracked) == {f"{ref}/{name}" for name in core}, "task_ref.archive_files")
    for name in core:
        path = root / ref / name
        archived_review_require(path.is_file() and not path.is_symlink(), "task_ref.archive_files")
    task = read_json(root / ref / "task.json", "task")
    summary = read_json(root / ref / "finish-summary.json", "finish_summary")
    archived_review_require(task.get("status") == "completed", "task.status")
    branch, base = task.get("branch"), task.get("base_branch")
    archived_review_require(isinstance(branch, str) and bool(branch) and isinstance(base, str) and bool(base), "task.branch")
    for name in (branch, base):
        archived_review_require(run(["git", "check-ref-format", "--branch", name], cwd=root, check=False).returncode == 0, "task.branch")
    archived_review_require(run_stdout(["git", "branch", "--show-current"], cwd=root) == branch, "task.branch")
    archived_review_require(summary.get("schema_version") == 2 and summary.get("generator") == "guru-team.finalize-task", "finish_summary.schema_version")
    archived_task, archived_git, archived_pr = summary.get("task"), summary.get("git"), summary.get("github")
    archived_review_require(all(isinstance(value, dict) for value in (archived_task, archived_git, archived_pr)), "finish_summary")
    active = archived_task.get("artifact_dir")
    archived_review_require(
        archived_task.get("status") == "completed" and archived_task.get("archive_dir") == ref
        and archived_task.get("slug") == Path(ref).name
        and active == f".trellis/tasks/{Path(ref).name}" and not (root / active).exists()
        and archived_git.get("branch") == branch and archived_git.get("base_branch") == base,
        "finish_summary.task",
    )
    canonical_pull_request_url(public_input["repo_ref"], public_input["pr_number"], archived_pr.get("pr_url"))
    publish = load_config(root).get("publish")
    if not isinstance(publish, dict):
        publish = {}
    remote_name = str(publish.get("remote") or "origin")
    remote_url = run_stdout(["git", "config", "--get", f"remote.{remote_name}.url"], cwd=root)
    match = re.fullmatch(r"(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?", remote_url)
    archived_review_require(match is not None and normalize_github_repository(match.group(1)) == public_input["repo_ref"], "publish.remote")
    archived_review_mappings(root, public_input, task)
    remote = run_stdout(["git", "ls-remote", "--exit-code", remote_name, f"refs/heads/{branch}"], cwd=root).splitlines()
    archived_review_require(remote == [f"{head}\trefs/heads/{branch}"], "remote.head")
    base_ref = f"refs/remotes/origin/{base}"
    base_head = run_stdout(["git", "rev-parse", "--verify", f"{base_ref}^{{commit}}"], cwd=root)
    archived_review_require(run(["git", "merge-base", "--is-ancestor", base_head, head], cwd=root, check=False).returncode == 0, "base.ancestry")
    return {"expected_base_branch": base, "expected_head_branch": branch, "base_head": base_head}


def archived_review_facts(root: Path, public_input: dict[str, Any]) -> dict[str, Any]:
    local = archived_review_local(root, public_input)
    facts = task_pr_merge_live_facts(root, {**public_input, **local})
    pr = facts["pr"]
    archived_review_require(pr["head_sha"] == public_input["expected_head_sha"], "github.pr.head")
    archived_review_require(pr["head_branch"] == local["expected_head_branch"] and pr["base_branch"] == local["expected_base_branch"], "github.pr.branches")
    archived_review_require(facts["base_ref"]["head_sha"] == local["base_head"], "base.head")
    blockers = task_pr_merge_preflight_errors({**public_input, **local}, facts)
    required = task_pr_merge_required_checks(root, public_input["repo_ref"], public_input["pr_number"])
    if any(row["bucket"] in {"pending", "fail", "cancel"} for row in required):
        blockers.append("required checks are not successful")
    if pr["review_decision"] in {"CHANGES_REQUESTED", "REVIEW_REQUIRED"}:
        blockers.append("required review is not satisfied")
    if "merge" not in facts["repository_policy"]["allowed_methods"]:
        blockers.append("repository policy does not allow the merge method")
    facts["required_checks"] = required
    facts["objective_blockers"] = blockers
    facts.pop("facts_sha256")
    facts["facts_sha256"] = canonical_json_sha256(facts)
    return facts


def archived_review_gate_path(root: Path, public_input: dict[str, Any]) -> Path:
    return task_pr_merge_gate_path(root, public_input).with_name("archived-review-gate.json")


def archived_review_route(review_payload: dict[str, Any], facts: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    review = task_pr_merge_semantic_review(review_payload.get("semantic_review"))
    route = review_payload.get("route")
    if not isinstance(route, dict) or route.get("typed_exit") not in {"review_refresh_required", "merge_blocked"}:
        raise WorkflowError("Archived review cannot select a merge or task-restoration route.", code="invalid_arguments", field_path="review_input.route")
    passed = all(row["status"] == "passed" for row in review["dimensions"])
    if route["typed_exit"] == "review_refresh_required":
        archived_review_require(set(route) == {"typed_exit"} and passed and not facts["objective_blockers"], "review_input.route")
    else:
        archived_review_require((not passed or bool(facts["objective_blockers"])) and set(route) == {"typed_exit", "reason_code", "remediation"}
                                and all(isinstance(route.get(key), str) and route[key].strip() for key in ("reason_code", "remediation")), "review_input.route")
    return review, route


def archived_review_record(root: Path, public_input: dict[str, Any], review_payload: dict[str, Any], facts: dict[str, Any] | None = None) -> dict[str, Any]:
    facts = facts if facts is not None else archived_review_facts(root, public_input)
    review, route = archived_review_route(review_payload, facts)
    gate = {"schema_version": "1.0", "skill_id": "guru-merge-task-pr", "input": public_input,
            "facts_sha256": facts["facts_sha256"], "semantic_review": review, "route": route}
    path = archived_review_gate_path(root, public_input)
    archived_review_require(run(["git", "check-ignore", "--quiet", str(path)], cwd=root, check=False).returncode == 0, "gate.ignored_runtime")
    write_json(path, gate)
    return gate


def archived_review_result(public_input: dict[str, Any], gate: dict[str, Any], facts: dict[str, Any]) -> dict[str, Any]:
    archived_review_require(set(gate) == {"schema_version", "skill_id", "input", "facts_sha256", "semantic_review", "route"}
                            and gate.get("schema_version") == "1.0" and gate.get("skill_id") == "guru-merge-task-pr"
                            and gate.get("input") == public_input and gate.get("facts_sha256") == facts["facts_sha256"], "gate.archived_review")
    _, route = archived_review_route(gate, facts)
    if route["typed_exit"] == "merge_blocked":
        output = {"exit_id": "merge_blocked", "reason_code": route["reason_code"], "remediation": route["remediation"]}
    else:
        output = {"exit_id": "review_refresh_required", "task_ref": public_input["task_ref"],
                  "branch_review_commit": public_input["expected_head_sha"],
                  "pr_payload_snapshot_sha256": facts["pr_payload_snapshot_sha256"]}
    return {"status": "passed", "typed_exit": output["exit_id"], "output": output}


def archived_review_check(root: Path, public_input: dict[str, Any], value: str | None) -> tuple[Path, dict[str, Any]]:
    expected = archived_review_gate_path(root, public_input)
    path = Path(value) if value else expected
    if not path.is_absolute():
        path = root / path
    archived_review_require(path == expected and path.is_file() and not path.is_symlink(), "gate.archived_review")
    gate = read_json(path, "gate.archived_review")
    return path, archived_review_result(public_input, gate, archived_review_facts(root, public_input))


def archived_review_invoke(root: Path, public_input: dict[str, Any], review_payload: dict[str, Any]) -> dict[str, Any]:
    facts = archived_review_facts(root, public_input)
    review, route = archived_review_route(review_payload, facts)
    path = archived_review_gate_path(root, public_input)
    if path.exists():
        gate = read_json(path, "gate.archived_review")
        archived_review_require(gate.get("semantic_review") == review and gate.get("route") == route, "review_input")
    else:
        gate = archived_review_record(root, public_input, review_payload, facts)
    output = archived_review_result(public_input, gate, facts)["output"]
    path.unlink()
    return output


def cmd_watch_task_pr_checks(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or "."))
    repo = normalize_github_repository(args.repo)
    if not repo:
        raise WorkflowError("Task PR check watcher requires owner/repository.", code="invalid_arguments", field_path="repo_ref")
    pr_number = args.pull_request
    expected_head = str(args.expected_head or "")
    timeout_seconds = args.timeout_seconds
    interval_seconds = args.interval_seconds
    if (
        not is_strict_int(pr_number) or pr_number < 1
        or re.fullmatch(r"[0-9a-f]{40}", expected_head) is None
        or not is_strict_int(timeout_seconds) or timeout_seconds < 0
        or not is_strict_int(interval_seconds) or interval_seconds < 1
    ):
        raise WorkflowError("Task PR check watcher arguments are invalid.", code="invalid_arguments", field_path="arguments")

    started = time.monotonic()
    polls = 0
    while True:
        polls += 1
        pr = gh_json(
            ["pr", "view", str(pr_number), "--repo", repo, "--json", "number,headRefOid"],
            cwd=root,
            repo=repo,
            required_fields=("number", "headRefOid"),
            operation="required_checks_head",
        )
        if not isinstance(pr, dict) or pr.get("number") != pr_number:
            raise github_response_incomplete(
                operation="required_checks_head", repo=repo, detail="PR identity does not match."
            )
        live_head = pr.get("headRefOid")
        if not isinstance(live_head, str) or re.fullmatch(r"[0-9a-f]{40}", live_head) is None:
            raise github_response_incomplete(
                operation="required_checks_head", repo=repo, detail="PR head identity is incomplete."
            )
        elapsed_ms = int((time.monotonic() - started) * 1000)
        if live_head != expected_head:
            return {
                "status": "head_changed",
                "repo_ref": repo,
                "pr_number": pr_number,
                "expected_head_sha": expected_head,
                "actual_head_sha": live_head,
                "poll_count": polls,
                "external_ci_wait_ms": elapsed_ms,
                "checks": [],
            }

        checks = task_pr_merge_required_checks(root, repo, pr_number)
        buckets = {row["bucket"] for row in checks}
        if buckets & {"fail", "cancel"}:
            status = "checks_failed"
        elif "pending" not in buckets:
            status = "checks_succeeded"
        elif elapsed_ms >= timeout_seconds * 1000:
            status = "checks_pending_timeout"
        else:
            remaining = timeout_seconds - elapsed_ms / 1000
            time.sleep(min(interval_seconds, max(0.0, remaining)))
            continue
        return {
            "status": status,
            "repo_ref": repo,
            "pr_number": pr_number,
            "expected_head_sha": expected_head,
            "actual_head_sha": live_head,
            "poll_count": polls,
            "external_ci_wait_ms": elapsed_ms,
            "checks": checks,
        }
