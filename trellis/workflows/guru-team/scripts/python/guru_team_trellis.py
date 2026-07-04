#!/usr/bin/env python3
"""Guru Team Trellis workflow companion scripts.

The script intentionally uses only the Python standard library plus external
`git` and `gh` commands. It is installed into target repositories under
`.trellis/guru-team/` and never modifies Trellis upstream files.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULTS: dict[str, Any] = {
    "github_repo": "",
    "source_issue_required": False,
    "auto_create_issue": False,
    "duplicate_search_required": True,
    "duplicate_candidate_limit": 5,
    "duplicate_high_similarity_action": "confirm",
    "branch_prefix": "codex/",
    "base_branch_candidates": ["dev", "develop", "main", "master"],
    "workspace_mode": "worktree",
    "worktree_root": "",
    "handoff_path": ".trellis/guru-team/handoff.json",
    "artifact_language": "zh-CN",
    "review_gate": {
        "artifact_path": "review-gate.json",
        "block_priorities": ["P0", "P1", "P2"],
        "require_head_match": True,
        "require_deployment_impact_evidence": True,
    },
    "publish": {
        "draft": False,
        "close_keyword": "Closes",
        "pr_language": "zh-CN",
        "remote": "origin",
    },
    "created_issue_labels": [],
    "closeout_markers": ["最终收口口径", "Final Closeout"],
}

VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}
BLOCKING_PRIORITIES = {"P0", "P1", "P2"}
PLANNING_APPROVAL_ARTIFACT = "planning-approval.json"
PHASE2_CHECK_ARTIFACT = "phase2-check.json"
GURU_TEAM_EXTENSION_MANIFEST = Path(".trellis/guru-team/extension.json")
DEFAULT_PLANNING_ARTIFACTS = ["prd.md", "design.md", "implement.md"]
DEFAULT_PHASE2_TASK_ARTIFACTS = [
    "prd.md",
    "design.md",
    "implement.md",
    PLANNING_APPROVAL_ARTIFACT,
]
REQUIRED_PHASE2_COVERAGE = [
    "requirements",
    "design",
    "code",
    "tests",
    "spec_sync",
    "cross_layer",
    "docs_ssot",
    "deployment",
]
RESOLVED_FINDING_STATUSES = {"resolved", "fixed", "closed"}
INDEPENDENT_REVIEW_SOURCE = "independent-agent"
SELF_REVIEWER_PATTERNS = [
    re.compile(r"(^|[-_./\s])main[-_./\s]*session($|[-_./\s])", re.IGNORECASE),
    re.compile(r"(^|[-_./\s])self[-_./\s]*review($|[-_./\s])", re.IGNORECASE),
]
METADATA_ONLY_PREFIXES = (".trellis/tasks/", ".trellis/workspace/", ".trellis/.runtime/")
METADATA_ONLY_FILES = {".trellis/guru-team/handoff.json"}
PR_BODY_REQUIRED_SECTIONS = [
    "变更摘要",
    "影响范围",
    "验证结果",
    "Review Gate",
    "Issue 关闭范围",
    "安全说明",
]
PR_BODY_SECTION_ALIASES = {
    "变更摘要": ["变更摘要", "更新摘要"],
    "影响范围": ["影响范围"],
    "验证结果": ["验证结果", "验证"],
    "Review Gate": ["Review Gate", "ReviewGate"],
    "Issue 关闭范围": ["Issue 关闭范围", "议题关闭范围", "关联议题"],
    "安全说明": ["安全说明", "安全与部署影响", "安全/部署影响", "安全和部署影响"],
}
PR_BODY_LOW_INFORMATION_PHRASES = [
    "当前 Trellis task",
    "已提交实现与文档更新",
    "详见 artifact",
    "详见 Trellis task artifact",
    "详见 Trellis task artifact 与 Review Gate 记录",
    "未提供具体 publish validation",
    "需要 AI 在 body file 中补充",
    "未记录 changed_files",
]
PR_BODY_PLACEHOLDER_VALUES = {
    "",
    "无",
    "n/a",
    "na",
    "none",
    "tbd",
    "todo",
    "待补充",
    "待定",
}
PR_CLOSE_KEYWORDS = ["Closes", "Fixes", "Resolves", "Close", "Fix", "Resolve"]
REVIEWED_PR_BODY_SOURCE_PREFIXES = ("body-file:", "body-artifact:")
DEPLOYMENT_ASSET_CATEGORIES: dict[str, list[str]] = {
    "ci_cd": [
        ".github/workflows/",
        ".github/actions/",
        ".gitlab-ci",
        "Jenkinsfile",
        "buildkite/",
        ".circleci/",
    ],
    "container": [
        "Dockerfile",
        "dockerfile",
        "docker-compose",
        "compose.",
        "container",
        "entrypoint",
        "startup",
    ],
    "kubernetes": [
        "k8s/",
        "kubernetes/",
        "deploy/",
        "deployment/",
        "kustomization.yaml",
        "kustomization.yml",
        "helm/",
        "values.yaml",
        "values.yml",
    ],
    "database": [
        "migration",
        "migrations/",
        "schema/",
        "seed",
        "seeds/",
        "backfill",
        "db/",
        "database/",
    ],
    "makefile": [
        "Makefile",
    ],
}
DEPLOYMENT_IMPACT_KEYWORDS = [
    "api",
    "service",
    "server",
    "worker",
    "background",
    "daemon",
    "cron",
    "job",
    "queue",
    "consumer",
    "cli",
    "cmd/",
    "command",
    "deploy",
    "deployment",
    "runtime",
    "entrypoint",
    "docker",
    "k8s",
    "kubernetes",
    "compose",
    "migration",
    "schema",
]


class WorkflowError(RuntimeError):
    def __init__(self, message: str, exit_code: int = 1, payload: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.exit_code = exit_code
        self.payload = payload or {}


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True, check=check)


def run_stdout(cmd: list[str], cwd: Path | None = None) -> str:
    try:
        return run(cmd, cwd=cwd).stdout.strip()
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        raise WorkflowError(f"Command failed: {shlex.join(cmd)}\n{stderr}") from exc


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise WorkflowError(f"Required tool not found on PATH: {name}")


def require_gh_auth(root: Path) -> None:
    require_tool("gh")
    proc = run(["gh", "auth", "status"], cwd=root, check=False)
    if proc.returncode != 0:
        raise WorkflowError(
            "GitHub CLI is not authenticated. Run `gh auth login` before GitHub issue intake."
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


def infer_github_repo(root: Path) -> str:
    try:
        url = run_stdout(["git", "remote", "get-url", "origin"], cwd=root)
    except WorkflowError:
        return ""
    match = re.search(r"github\.com[:/]([^/]+)/(.+?)(?:\.git)?$", url)
    if not match:
        return ""
    return f"{match.group(1)}/{match.group(2)}"


def gh_json(args: list[str], cwd: Path) -> Any:
    require_gh_auth(cwd)
    proc = run(["gh", *args], cwd=cwd, check=False)
    if proc.returncode != 0:
        raise WorkflowError(f"gh command failed: gh {shlex.join(args)}\n{proc.stderr.strip()}")
    text = proc.stdout.strip()
    return json.loads(text) if text else None


def parse_issue_ref(text: str, default_repo: str) -> tuple[str, int] | None:
    url_match = re.search(r"https://github\.com/([^/\s]+)/([^/\s]+)/issues/(\d+)", text)
    if url_match:
        return f"{url_match.group(1)}/{url_match.group(2)}", int(url_match.group(3))
    hash_match = re.search(r"(?<![\w/])#(\d+)\b", text)
    if hash_match and default_repo:
        return default_repo, int(hash_match.group(1))
    word_match = re.search(r"\bissue\s+#?(\d+)\b", text, re.IGNORECASE)
    if word_match and default_repo:
        return default_repo, int(word_match.group(1))
    return None


def clean_requirement(text: str) -> str:
    text = re.sub(r"https://github\.com/[^\s]+/issues/\d+", "", text)
    text = re.sub(r"(?<![\w/])#\d+\b", "", text)
    text = re.sub(r"\bissue\s+#?\d+\b", "", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> set[str]:
    lower = text.lower()
    tokens = set(re.findall(r"[a-z0-9][a-z0-9_-]{1,}", lower))
    cjk = "".join(re.findall(r"[\u4e00-\u9fff]", text))
    tokens.update(cjk[i : i + 2] for i in range(max(0, len(cjk) - 1)))
    return {token for token in tokens if len(token) >= 2}


def has_minimum_clarity(text: str) -> bool:
    compact = clean_requirement(text)
    if len(compact) >= 30:
        return True
    return len(tokenize(compact)) >= 4


def slugify(text: str, fallback: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    stop = {"the", "and", "for", "with", "from", "this", "that", "into", "add", "new", "issue"}
    selected = [word for word in words if word not in stop][:5]
    slug = "-".join(selected) if selected else fallback
    slug = re.sub(r"[^a-z0-9-]+", "-", slug).strip("-")
    return slug or fallback


def make_issue_title(requirement: str, short_name: str | None = None) -> str:
    text = clean_requirement(requirement)
    first = re.split(r"[。\n.!?]", text, maxsplit=1)[0].strip()
    if first:
        return first[:90]
    if short_name:
        return short_name.replace("-", " ").title()
    return "Trellis intake"


def issue_body(requirement: str, duplicates: list[dict[str, Any]]) -> str:
    duplicate_lines = "\n".join(
        f"- #{candidate['number']} {candidate['title']} ({candidate['similarity']}): {candidate['url']}"
        for candidate in duplicates
    )
    if not duplicate_lines:
        duplicate_lines = "- 创建前未发现阻塞级重复 issue。"
    return f"""## Background

This issue body was drafted by the Guru Team Trellis intake workflow because the user request did not provide an existing source issue.

## Current State

The request has not yet been converted into Trellis planning artifacts.

## Problem or Gap

{clean_requirement(requirement)}

## Requirement Change

The Trellis task `prd.md` should turn this intake into testable requirements and acceptance criteria.

## Design or Implementation Handoff

Use this issue as the discussion and intake record. Trellis task artifacts become the execution source of truth after planning.

## Out of Scope

Clarify during Trellis planning if the request is broader than the next task.

## Open Questions

Clarify during Trellis planning.

## Duplicate Issue Search

{duplicate_lines}

## Trellis Handoff

The workflow will record the Trellis task path, branch, base branch, and workspace path in the task artifacts or follow-up comments when the task is created.
"""


def confirmed_issue_prepare_command(
    args: argparse.Namespace,
    title: str,
    requirement: str,
    force_new: bool | None = None,
) -> list[str]:
    cmd = [
        "python3",
        "./.trellis/guru-team/scripts/python/guru_team_trellis.py",
        "prepare",
        "--json",
        "--create-issue-confirmed",
        "--issue-title",
        title,
        "--issue-body-file",
        "<reviewed-issue-body.md>",
    ]
    option_map = [
        ("short_name", "--short-name"),
        ("base_branch", "--base-branch"),
        ("branch", "--branch"),
        ("task_slug", "--task-slug"),
        ("workspace_slug", "--workspace-slug"),
        ("title", "--title"),
        ("assignee", "--assignee"),
        ("priority", "--priority"),
        ("description", "--description"),
    ]
    for attr, option in option_map:
        value = getattr(args, attr, None)
        if value:
            cmd.extend([option, str(value)])
    should_force_new = getattr(args, "force_new", False) if force_new is None else force_new
    if should_force_new:
        cmd.append("--force-new")
    if getattr(args, "worktree", False):
        cmd.append("--worktree")
    cmd.append(requirement)
    return cmd


def issue_view(repo: str, number: int, root: Path) -> dict[str, Any]:
    return gh_json(
        [
            "issue",
            "view",
            str(number),
            "--repo",
            repo,
            "--json",
            "number,title,url,body,comments,state",
        ],
        cwd=root,
    )


def score_duplicate(requirement: str, issue: dict[str, Any]) -> tuple[float, str]:
    req_tokens = tokenize(requirement)
    issue_text = f"{issue.get('title', '')}\n{issue.get('body', '')}"
    issue_tokens = tokenize(issue_text)
    if not req_tokens or not issue_tokens:
        return 0.0, "No comparable keywords"
    overlap = req_tokens & issue_tokens
    score = len(overlap) / max(1, len(req_tokens))
    title = issue.get("title", "").lower()
    reason = "keyword overlap: " + ", ".join(sorted(overlap)[:8]) if overlap else "weak keyword overlap"
    phrase = clean_requirement(requirement).lower()[:30]
    if phrase and phrase in title:
        score = max(score, 0.75)
        reason = "title contains the requirement phrase"
    return score, reason


def duplicate_search(repo: str, requirement: str, root: Path, limit: int) -> list[dict[str, Any]]:
    issues = gh_json(
        [
            "issue",
            "list",
            "--repo",
            repo,
            "--state",
            "open",
            "--limit",
            "50",
            "--json",
            "number,title,body,url,labels,updatedAt",
        ],
        cwd=root,
    ) or []
    candidates: list[dict[str, Any]] = []
    for issue in issues:
        score, reason = score_duplicate(requirement, issue)
        if score >= 0.18:
            similarity = "high" if score >= 0.45 else "medium" if score >= 0.25 else "low"
            candidates.append(
                {
                    "number": issue["number"],
                    "title": issue.get("title", ""),
                    "url": issue.get("url", ""),
                    "score": round(score, 3),
                    "similarity": similarity,
                    "reason": reason,
                }
            )
    candidates.sort(key=lambda item: item["score"], reverse=True)
    return candidates[:limit]


def create_issue(repo: str, title: str, body: str, root: Path, labels: list[str]) -> dict[str, Any]:
    title = title.strip()
    body = body.strip()
    if not title:
        raise WorkflowError("Confirmed issue creation requires a non-empty issue title.")
    if not body:
        raise WorkflowError("Confirmed issue creation requires a non-empty issue body.")
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        tmp.write(body + "\n")
        tmp_path = tmp.name
    try:
        cmd = ["issue", "create", "--repo", repo, "--title", title, "--body-file", tmp_path]
        for label in labels:
            if label:
                cmd.extend(["--label", str(label)])
        require_gh_auth(root)
        proc = run(["gh", *cmd], cwd=root, check=False)
        if proc.returncode != 0:
            raise WorkflowError(f"gh issue create failed:\n{proc.stderr.strip()}")
        url = proc.stdout.strip()
    finally:
        Path(tmp_path).unlink(missing_ok=True)
    match = re.search(r"/issues/(\d+)", url)
    if not match:
        raise WorkflowError(f"Could not parse created issue number from URL: {url}")
    return issue_view(repo, int(match.group(1)), root)


def read_confirmed_issue_body(path_value: str | None) -> str:
    if not path_value:
        raise WorkflowError(
            "--create-issue-confirmed requires --issue-body-file containing the AI/human reviewed issue body.",
            exit_code=2,
        )
    path = Path(path_value)
    if not path.exists():
        raise WorkflowError(f"Confirmed issue body file not found: {path}")
    body = path.read_text(encoding="utf-8").strip()
    if not body:
        raise WorkflowError(f"Confirmed issue body file is empty: {path}")
    return body


def git_branch_exists(root: Path, ref: str) -> bool:
    return run(["git", "rev-parse", "--verify", "--quiet", ref], cwd=root, check=False).returncode == 0


def local_branch_exists(root: Path, branch: str) -> bool:
    return git_branch_exists(root, f"refs/heads/{branch}")


def ref_head(root: Path, ref: str) -> str | None:
    proc = run(["git", "rev-parse", "--verify", "--quiet", ref], cwd=root, check=False)
    value = proc.stdout.strip()
    if proc.returncode == 0 and value:
        return value
    return None


def base_short_name(base_ref: str) -> str:
    normalized = normalize_ref(base_ref)
    return normalized.split("/", 1)[1] if normalized.startswith("origin/") else normalized


def inspect_base_freshness(root: Path, base_ref: str, remote: str = "origin") -> dict[str, Any]:
    base = base_short_name(base_ref)
    local_head = ref_head(root, base)
    remote_ref = f"{remote}/{base}"
    remote_head = ref_head(root, remote_ref)
    fresh = bool(remote_head and local_head == remote_head)
    if remote_head and not local_head:
        fresh = True
    status = "fresh" if fresh else "unknown"
    if remote_head and local_head and local_head != remote_head:
        status = "stale"
    if not remote_head:
        status = "remote_ref_missing"
    return {
        "remote": remote,
        "base_branch": base,
        "base_ref": base_ref,
        "remote_ref": remote_ref,
        "local_head_before": local_head,
        "local_head_after": local_head,
        "remote_head": remote_head,
        "fetch_performed": False,
        "fast_forwarded": False,
        "fresh": fresh,
        "status": status,
        "base_ref_for_worktree": remote_ref if remote_head else base_ref,
    }


def ensure_base_freshness(root: Path, base_ref: str, remote: str = "origin") -> dict[str, Any]:
    base = base_short_name(base_ref)
    remote_ref = f"{remote}/{base}"
    local_head_before = ref_head(root, base)
    fetch_proc = run(["git", "fetch", remote, base], cwd=root, check=False)
    if fetch_proc.returncode != 0:
        raise WorkflowError(
            f"Could not refresh base branch before worktree creation: git fetch {remote} {base}\n{fetch_proc.stderr.strip()}",
            exit_code=2,
        )
    remote_head = ref_head(root, remote_ref)
    if not remote_head:
        raise WorkflowError(
            f"Remote base ref not found after fetch: {remote_ref}",
            exit_code=2,
            payload={"remote": remote, "base_branch": base, "remote_ref": remote_ref},
        )

    fast_forwarded = False
    if local_head_before:
        if local_head_before == remote_head:
            pass
        elif is_ancestor(root, local_head_before, remote_ref):
            if current_branch(root) == base:
                if git_dirty(root):
                    raise WorkflowError(
                        f"Base branch {base} is behind {remote_ref}, but the checkout is dirty and cannot be fast-forwarded safely.",
                        exit_code=2,
                    )
                run_stdout(["git", "merge", "--ff-only", remote_ref], cwd=root)
            else:
                run_stdout(["git", "branch", "-f", base, remote_ref], cwd=root)
            fast_forwarded = True
        else:
            raise WorkflowError(
                f"Local base branch {base} diverged from {remote_ref}; cannot create task worktree from stale base.",
                exit_code=2,
                payload={
                    "base_branch": base,
                    "local_head": local_head_before,
                    "remote_head": remote_head,
                    "remote_ref": remote_ref,
                },
            )

    local_head_after = ref_head(root, base)
    fresh = local_head_after == remote_head if local_head_after else True
    return {
        "remote": remote,
        "base_branch": base,
        "base_ref": base_ref,
        "remote_ref": remote_ref,
        "local_head_before": local_head_before,
        "local_head_after": local_head_after,
        "remote_head": remote_head,
        "fetch_performed": True,
        "fast_forwarded": fast_forwarded,
        "fresh": fresh,
        "status": "fresh" if fresh else "remote_only",
        "base_ref_for_worktree": base if fresh and local_head_after else remote_ref,
    }


def resolve_base_branch(root: Path, config: dict[str, Any], explicit: str | None = None) -> tuple[str, list[str]]:
    candidates = [explicit] if explicit else list(config.get("base_branch_candidates") or DEFAULTS["base_branch_candidates"])
    discovered: list[str] = []
    for candidate in candidates:
        if not candidate:
            continue
        candidate = str(candidate)
        refs = [candidate, f"origin/{candidate}"] if not candidate.startswith("origin/") else [candidate]
        for ref in refs:
            if git_branch_exists(root, ref):
                discovered.append(ref)
    if discovered:
        return discovered[0], discovered
    current = current_branch(root)
    return current, [current]


def current_branch(root: Path) -> str:
    proc = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root, check=False)
    value = proc.stdout.strip()
    if proc.returncode == 0 and value and value != "HEAD":
        return value
    proc = run(["git", "symbolic-ref", "--short", "HEAD"], cwd=root, check=False)
    value = proc.stdout.strip()
    return value or "HEAD"


def current_head(root: Path) -> str:
    return run_stdout(["git", "rev-parse", "HEAD"], cwd=root)


def git_dirty(root: Path) -> bool:
    return bool(run(["git", "status", "--porcelain"], cwd=root, check=False).stdout.strip())


def git_status_paths(root: Path) -> list[str]:
    lines = run(["git", "status", "--porcelain"], cwd=root, check=False).stdout.splitlines()
    paths: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path:
            paths.append(path)
    return paths


def has_non_metadata_dirty_paths(root: Path) -> tuple[bool, list[str]]:
    paths = git_status_paths(root)
    non_metadata = [
        path
        for path in paths
        if not path.startswith(METADATA_ONLY_PREFIXES) and path not in METADATA_ONLY_FILES
    ]
    return bool(non_metadata), non_metadata


def stage_metadata_paths(root: Path) -> list[str]:
    metadata_paths = [
        path
        for path in git_status_paths(root)
        if path.startswith(METADATA_ONLY_PREFIXES) or path in METADATA_ONLY_FILES
    ]
    if metadata_paths:
        run_stdout(["git", "add", "--", *metadata_paths], cwd=root)
    return metadata_paths


def commit_if_metadata_dirty(root: Path, message: str) -> dict[str, Any]:
    dirty, dirty_paths = has_non_metadata_dirty_paths(root)
    if dirty:
        raise WorkflowError(
            "finish-work produced uncommitted non-metadata changes. Return to continue/review before publish.",
            exit_code=2,
            payload={"dirty_paths": dirty_paths},
        )
    metadata_paths = stage_metadata_paths(root)
    if not metadata_paths:
        return {"committed": False, "paths": []}
    if run(["git", "diff", "--cached", "--quiet"], cwd=root, check=False).returncode == 0:
        return {"committed": False, "paths": metadata_paths}
    run_stdout(["git", "commit", "-m", message], cwd=root)
    return {"committed": True, "paths": metadata_paths, "commit": current_head(root)}


def recent_work_commits(root: Path, reviewed_head: str, max_count: int = 5) -> list[str]:
    proc = run(["git", "log", "--format=%H", f"{reviewed_head}^..{reviewed_head}"], cwd=root, check=False)
    if proc.returncode == 0:
        commits = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
        if commits:
            return commits[:max_count]
    return [reviewed_head] if reviewed_head else []


def normalize_ref(ref: str) -> str:
    return ref.removeprefix("refs/heads/")


def diff_base_ref(root: Path, base_branch: str) -> str:
    candidates: list[str] = []
    base = normalize_ref(base_branch)
    if base.startswith("origin/"):
        candidates.append(base)
        candidates.append(base.split("/", 1)[1])
    else:
        candidates.append(f"origin/{base}")
        candidates.append(base)
    for candidate in candidates:
        if git_branch_exists(root, candidate):
            return candidate
    return candidates[0]


def diff_range(root: Path, base_branch: str) -> str:
    return f"{diff_base_ref(root, base_branch)}...HEAD"


def changed_files(root: Path, diff_spec: str) -> list[str]:
    proc = run(["git", "diff", "--name-only", diff_spec], cwd=root, check=False)
    if proc.returncode != 0:
        raise WorkflowError(f"Could not compute diff for {diff_spec}:\n{proc.stderr.strip()}")
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def file_matches_marker(path: str, marker: str) -> bool:
    lowered = path.lower()
    marker_lower = marker.lower()
    name = Path(path).name
    if marker.endswith("/"):
        return lowered.startswith(marker_lower) or f"/{marker_lower}" in lowered
    if marker_lower in {"makefile", "dockerfile", "jenkinsfile"}:
        return name.lower() == marker_lower or name.lower().startswith(f"{marker_lower}.")
    return marker_lower in lowered


def classify_changed_files(files: list[str]) -> dict[str, list[str]]:
    categories: dict[str, list[str]] = {key: [] for key in DEPLOYMENT_ASSET_CATEGORIES}
    categories.update(
        {
            "docs": [],
            "tests": [],
            "trellis_artifacts": [],
            "config": [],
            "scripts": [],
            "schemas": [],
            "code": [],
            "other": [],
        }
    )
    for path in files:
        matched = False
        lowered = path.lower()
        for category, markers in DEPLOYMENT_ASSET_CATEGORIES.items():
            if any(file_matches_marker(path, marker) for marker in markers):
                categories[category].append(path)
                matched = True
        if path.startswith(".trellis/") or "/.trellis/" in path or path.startswith("trellis/"):
            categories["trellis_artifacts"].append(path)
            matched = True
        if lowered.endswith((".md", ".mdx", ".rst", ".txt")) or lowered.startswith("docs/"):
            categories["docs"].append(path)
            matched = True
        if any(part in lowered for part in ["/test", "/tests/", "_test.", ".spec.", ".test."]):
            categories["tests"].append(path)
            matched = True
        if lowered.endswith((".json", ".yaml", ".yml", ".toml", ".ini", ".conf", ".cfg", ".properties")):
            categories["config"].append(path)
            matched = True
        if lowered.endswith((".sh", ".bash", ".zsh", ".py", ".rb", ".pl")) and (
            "/script" in lowered or lowered.startswith("scripts/") or "/bin/" in lowered
        ):
            categories["scripts"].append(path)
            matched = True
        if "schema" in lowered or lowered.endswith(".schema.json"):
            categories["schemas"].append(path)
            matched = True
        if lowered.endswith(
            (
                ".go",
                ".py",
                ".ts",
                ".tsx",
                ".js",
                ".jsx",
                ".java",
                ".kt",
                ".rs",
                ".rb",
                ".php",
                ".cs",
                ".cpp",
                ".c",
                ".h",
                ".sql",
            )
        ):
            categories["code"].append(path)
            matched = True
        if not matched:
            categories["other"].append(path)
    return {key: sorted(set(value)) for key, value in categories.items() if value}


def detect_deployment_impact(files: list[str]) -> dict[str, Any]:
    changed_categories = classify_changed_files(files)
    deployment_categories = {
        key: changed_categories[key]
        for key in DEPLOYMENT_ASSET_CATEGORIES
        if key in changed_categories
    }
    changed_deployment_assets = sorted(
        {path for paths in deployment_categories.values() for path in paths}
    )
    probable_runtime_changes = sorted(
        {
            path
            for path in files
            if any(keyword in path.lower() for keyword in DEPLOYMENT_IMPACT_KEYWORDS)
            and path not in changed_deployment_assets
        }
    )
    needs_deployment_review = bool(changed_deployment_assets or probable_runtime_changes)
    return {
        "changed_file_categories": changed_categories,
        "deployment_asset_categories": deployment_categories,
        "changed_deployment_assets": changed_deployment_assets,
        "probable_runtime_changes_without_deployment_asset_change": probable_runtime_changes,
        "needs_deployment_impact_review": needs_deployment_review,
        "review_instruction": (
            "当本次 diff 改变部署资产，或业务/API/CLI/worker/runtime 形态可能变化但部署资产未改时，"
            "review evidence 必须说明 CI/CD、容器、Compose、K8s/Kustomize、migration、Makefile 是否需要同步调整；"
            "如果不需要，必须给出不需要的理由。"
        ),
    }


def evidence_mentions_category(evidence: list[str], category: str) -> bool:
    text = "\n".join(evidence).lower()
    aliases = {
        "ci_cd": ["ci", "cd", "github actions", ".github/workflows", "workflow", "发布自动化"],
        "container": ["docker", "compose", "container", "容器", "entrypoint", "startup"],
        "kubernetes": ["k8s", "kubernetes", "kustomize", "helm", "yaml", "部署"],
        "database": ["migration", "schema", "seed", "backfill", "数据库", "迁移"],
        "makefile": ["makefile", "make "],
        "runtime_impact": [
            "部署",
            "runtime",
            "运行",
            "api",
            "cli",
            "worker",
            "服务",
            "后台",
            "ci",
            "cd",
            "docker",
            "compose",
            "k8s",
            "kubernetes",
            "kustomize",
            "migration",
            "makefile",
        ],
    }
    return any(alias in text for alias in aliases.get(category, [category]))


def deployment_evidence_errors(impact: dict[str, Any], evidence: list[str], findings: list[dict[str, Any]]) -> list[str]:
    if blocking_findings(findings, {"review_gate": {"block_priorities": ["P0", "P1", "P2"]}}):
        return []
    errors: list[str] = []
    if not evidence_mentions_category(evidence, "runtime_impact"):
        errors.append("Gate evidence 未说明本次变更的部署影响，或未说明 Docker/Compose/CI/CD/K8s/migration/Makefile 是否需要同步调整。")
    if not impact.get("needs_deployment_impact_review"):
        return errors
    deployment_categories = impact.get("deployment_asset_categories")
    if isinstance(deployment_categories, dict):
        for category, paths in deployment_categories.items():
            if paths and not evidence_mentions_category(evidence, category):
                errors.append(f"Gate evidence 未点名已变更的部署资产类别 {category}。")
    runtime_changes = impact.get("probable_runtime_changes_without_deployment_asset_change")
    if isinstance(runtime_changes, list) and runtime_changes and not evidence_mentions_category(evidence, "runtime_impact"):
        errors.append("本次 diff 可能改变 API/CLI/worker/runtime 形态，但 evidence 未说明部署资产是否需要同步调整。")
    return errors


def is_ancestor(root: Path, ancestor: str, descendant: str = "HEAD") -> bool:
    return run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=root, check=False).returncode == 0


def worktree_lines(root: Path) -> list[str]:
    proc = run(["git", "worktree", "list"], cwd=root, check=False)
    return [line for line in proc.stdout.splitlines() if line.strip()]


def default_worktree_root(root: Path) -> Path:
    return root.parent / f"{root.name}-worktrees"


def configured_worktree_root(root: Path, config: dict[str, Any]) -> Path:
    configured = str(config.get("worktree_root") or "").strip()
    if not configured:
        return default_worktree_root(root)
    path = Path(configured)
    return path if path.is_absolute() else (root / path).resolve()


def prepare_workspace(
    root: Path,
    config: dict[str, Any],
    branch_name: str,
    workspace_slug: str,
    base_ref: str,
    force_worktree: bool,
    create_worktree: bool,
) -> tuple[str, Path, bool]:
    require_tool("git")
    mode = str(config.get("workspace_mode") or "worktree")
    if force_worktree:
        mode = "worktree"
    if mode not in {"worktree", "current"}:
        raise WorkflowError(f"Unsupported workspace_mode: {mode}")

    if mode == "current":
        return mode, root, True

    worktree_root = configured_worktree_root(root, config)
    workspace_path = worktree_root / workspace_slug
    if workspace_path.exists():
        if not (workspace_path / ".git").exists():
            raise WorkflowError(f"Workspace path exists but is not a git worktree: {workspace_path}")
        return mode, workspace_path, True

    if not create_worktree:
        return mode, workspace_path, False

    workspace_path.parent.mkdir(parents=True, exist_ok=True)
    if local_branch_exists(root, branch_name):
        run_stdout(["git", "worktree", "add", str(workspace_path), branch_name], cwd=root)
    else:
        run_stdout(["git", "worktree", "add", "-b", branch_name, str(workspace_path), base_ref], cwd=root)
    return mode, workspace_path, True


def developer_identity_path(root: Path) -> Path:
    return root / ".trellis/.developer"


def parse_developer_identity(content: str) -> dict[str, str]:
    identity: dict[str, str] = {}
    for raw in content.splitlines():
        line = raw.strip()
        if not line:
            continue
        if "=" not in line:
            identity.setdefault("name", line)
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key:
            identity[key] = value
    return identity


def read_developer_identity(root: Path) -> dict[str, str] | None:
    path = developer_identity_path(root)
    if not path.exists():
        return None
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return None
    return parse_developer_identity(content)


def developer_name_from_identity(identity: dict[str, str] | None) -> str | None:
    if not identity:
        return None
    value = str(identity.get("name") or "").strip()
    return value or None


def write_developer_identity(path: Path, name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"name={name}\ninitialized_at={now_iso()}\n"
    path.write_text(content, encoding="utf-8")


def ensure_workspace_developer_identity(source_root: Path, workspace_path: Path, assignee: str | None = None) -> dict[str, Any]:
    source_identity_path = developer_identity_path(source_root)
    workspace_identity_path = developer_identity_path(workspace_path)
    if workspace_identity_path.exists():
        workspace_identity = read_developer_identity(workspace_path)
        return {
            "status": "exists",
            "source": "workspace",
            "path": str(workspace_identity_path),
            "developer": developer_name_from_identity(workspace_identity),
        }

    if source_identity_path.exists():
        workspace_identity_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_identity_path, workspace_identity_path)
        workspace_identity = read_developer_identity(workspace_path)
        return {
            "status": "copied",
            "source": str(source_identity_path),
            "path": str(workspace_identity_path),
            "developer": developer_name_from_identity(workspace_identity),
        }

    normalized_assignee = str(assignee or "").strip()
    if normalized_assignee:
        write_developer_identity(workspace_identity_path, normalized_assignee)
        return {
            "status": "initialized",
            "source": "--assignee",
            "path": str(workspace_identity_path),
            "developer": normalized_assignee,
        }

    recovery_command = "python3 ./.trellis/scripts/init_developer.py <name>"
    raise WorkflowError(
        "Trellis developer identity is missing. Initialize the source checkout before creating a task worktree.",
        exit_code=2,
        payload={
            "missing_identity": True,
            "source_identity_path": str(source_identity_path),
            "workspace_identity_path": str(workspace_identity_path),
            "recovery_command": recovery_command,
        },
    )


def configured_handoff_path(root: Path, config: dict[str, Any]) -> Path:
    rel = Path(str(config.get("handoff_path") or DEFAULTS["handoff_path"]))
    return rel if rel.is_absolute() else root / rel


def workspace_handoff_path(config: dict[str, Any], workspace_path: Path) -> Path:
    rel = Path(str(config.get("handoff_path") or DEFAULTS["handoff_path"]))
    return rel if rel.is_absolute() else workspace_path / rel


def write_handoff(
    root: Path,
    config: dict[str, Any],
    payload: dict[str, Any],
    workspace_path: Path,
    mirror_to_source: bool = False,
) -> Path:
    path = workspace_handoff_path(config, workspace_path)
    payload["handoff_path"] = str(path)
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    if mirror_to_source and workspace_path != root:
        source_handoff = configured_handoff_path(root, config)
        source_handoff.parent.mkdir(parents=True, exist_ok=True)
        source_handoff.write_text(content, encoding="utf-8")
    return path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkflowError(f"Required JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"Invalid JSON file: {path}\n{exc}") from exc


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_optional_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, "missing"
    except json.JSONDecodeError as exc:
        return None, f"invalid: {exc}"
    if not isinstance(payload, dict):
        return None, "invalid: JSON root is not an object"
    return payload, None


def guru_team_extension_payload(root: Path) -> dict[str, Any]:
    path = root / GURU_TEAM_EXTENSION_MANIFEST
    payload, error = read_optional_json(path)
    if payload is None:
        status = "missing" if error == "missing" else "invalid"
        result: dict[str, Any] = {
            "status": status,
            "path": GURU_TEAM_EXTENSION_MANIFEST.as_posix(),
        }
        if error and error != "missing":
            result["error"] = error
        return result

    extension = payload.get("extension") if isinstance(payload.get("extension"), dict) else {}
    source = payload.get("source") if isinstance(payload.get("source"), dict) else {}
    install = payload.get("install") if isinstance(payload.get("install"), dict) else {}
    requires = extension.get("requires") if isinstance(extension.get("requires"), dict) else {}
    return {
        "status": "ok",
        "path": GURU_TEAM_EXTENSION_MANIFEST.as_posix(),
        "schema_version": payload.get("schema_version"),
        "extension_id": extension.get("extension_id"),
        "version": extension.get("version"),
        "workflow_template_id": extension.get("workflow_template_id"),
        "trellis_cli_compatibility": requires.get("trellis_cli"),
        "installed_at": payload.get("installed_at"),
        "source_repo": source.get("repo"),
        "source_ref": source.get("ref"),
        "source_commit": source.get("commit"),
        "source_tree_state": source.get("tree_state"),
        "source_is_mutable_ref": source.get("is_mutable_ref"),
        "selected_platforms": install.get("selected_platforms") if isinstance(install.get("selected_platforms"), list) else [],
        "all_platforms": install.get("all_platforms"),
    }


def load_handoff(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    path = configured_handoff_path(root, config)
    if not path.exists():
        return {}
    payload = read_json(path)
    payload.setdefault("handoff_path", str(path))
    return payload


def tasks_root(root: Path) -> Path:
    return root / ".trellis/tasks"


def resolve_existing_task_dir(root: Path, value: str) -> Path | None:
    raw = Path(value)
    candidates: list[Path] = []
    if raw.is_absolute():
        candidates.append(raw)
    else:
        candidates.extend([root / raw, tasks_root(root) / value])
    for candidate in candidates:
        if candidate.is_dir() and (candidate / "task.json").is_file():
            return candidate.resolve()

    base_name = raw.name.rstrip("/")
    task_root = tasks_root(root)
    active = task_root / base_name
    if active.is_dir() and (active / "task.json").is_file():
        return active.resolve()
    archive_root = task_root / "archive"
    if archive_root.is_dir():
        for month in sorted(archive_root.iterdir(), reverse=True):
            archived = month / base_name
            if archived.is_dir() and (archived / "task.json").is_file():
                return archived.resolve()
    return None


def current_task_dir(root: Path) -> Path | None:
    task_script = root / ".trellis/scripts/task.py"
    if not task_script.exists():
        return None
    proc = run(["python3", "./.trellis/scripts/task.py", "current"], cwd=root, check=False)
    value = proc.stdout.strip()
    if proc.returncode == 0 and value:
        return resolve_existing_task_dir(root, value)
    return None


def resolve_task_dir(root: Path, task_arg: str | None, handoff: dict[str, Any] | None = None) -> Path:
    if task_arg:
        resolved = resolve_existing_task_dir(root, task_arg)
        if resolved:
            return resolved
        raise WorkflowError(f"Could not resolve task directory: {task_arg}")

    if handoff:
        handoff_task = str(handoff.get("task_dir") or "").strip()
        if handoff_task:
            resolved = resolve_existing_task_dir(root, handoff_task)
            if resolved:
                return resolved

    current = current_task_dir(root)
    if current:
        return current
    raise WorkflowError("Could not resolve current Trellis task. Pass --task <task-dir>.")


def task_json(task_dir: Path) -> dict[str, Any]:
    return read_json(task_dir / "task.json")


def issue_entry(number: Any, url: str = "", title: str = "", reason: str = "", evidence: list[str] | None = None) -> dict[str, Any]:
    try:
        parsed_number = int(number)
    except (TypeError, ValueError):
        parsed_number = number
    return {
        "number": parsed_number,
        "url": url,
        "title": title,
        "reason": reason,
        "acceptance_evidence": evidence or [],
    }


def default_issue_scope_ledger(handoff: dict[str, Any]) -> dict[str, Any]:
    source = handoff.get("source_issue") if isinstance(handoff.get("source_issue"), dict) else {}
    primary = issue_entry(
        source.get("number"),
        str(source.get("url") or ""),
        str(source.get("title") or ""),
        "intake/handoff 主 issue，默认进入 close 候选；publish 前必须补齐验收证据。",
    )
    return {
        "schema_version": "1.0",
        "primary_issue": primary,
        "close_issues": [primary] if primary.get("number") is not None else [],
        "related_issues": [],
        "followup_issues": [],
        "rules": [
            "close_issues 只放当前 task 明确承诺完整解决且 review gate 已验证的 issue。",
            "related_issues 只能生成 Refs/Related 语义，不能自动关闭。",
            "followup_issues 表示新范围或后续任务，不能自动关闭。",
            "新增 issue 进入 close_issues 前必须更新 prd/design/implement 并取得用户明确确认。",
        ],
    }


def issue_scope_ledger_path(task_dir: Path) -> Path:
    return task_dir / "issue-scope-ledger.json"


def ensure_issue_scope_ledger(task_dir: Path, handoff: dict[str, Any]) -> Path:
    path = issue_scope_ledger_path(task_dir)
    if not path.exists():
        ledger = handoff.get("issue_scope_ledger")
        if not isinstance(ledger, dict):
            ledger = default_issue_scope_ledger(handoff)
        write_json(path, ledger)
    return path


def load_issue_scope_ledger(task_dir: Path, handoff: dict[str, Any]) -> dict[str, Any]:
    path = issue_scope_ledger_path(task_dir)
    if path.exists():
        return read_json(path)
    ledger = handoff.get("issue_scope_ledger")
    if isinstance(ledger, dict):
        return ledger
    return default_issue_scope_ledger(handoff)


def issue_numbers(items: Any) -> list[int]:
    numbers: list[int] = []
    if not isinstance(items, list):
        return numbers
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            numbers.append(int(item.get("number")))
        except (TypeError, ValueError):
            continue
    return numbers


def issue_has_evidence(issue: dict[str, Any]) -> bool:
    for key in ("acceptance_evidence", "verification", "evidence"):
        value = issue.get(key)
        if isinstance(value, list) and any(str(item).strip() for item in value):
            return True
        if isinstance(value, str) and value.strip():
            return True
    return False


def validate_ledger_for_publish(ledger: dict[str, Any], gate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    close_issues = ledger.get("close_issues")
    if not isinstance(close_issues, list):
        errors.append("issue-scope-ledger.json 缺少 close_issues 数组。")
        close_issues = []
    related_numbers = set(issue_numbers(ledger.get("related_issues")))
    followup_numbers = set(issue_numbers(ledger.get("followup_issues")))
    gate_reviewed = set(issue_numbers(gate.get("issue_scope", {}).get("close_issues_reviewed")))
    for issue in close_issues:
        if not isinstance(issue, dict):
            errors.append("close_issues 中存在非对象条目。")
            continue
        try:
            number = int(issue.get("number"))
        except (TypeError, ValueError):
            errors.append("close_issues 中存在缺少 number 的条目。")
            continue
        if number in related_numbers or number in followup_numbers:
            errors.append(f"issue #{number} 同时出现在 close_issues 与 related/followup 中。")
        if not issue_has_evidence(issue):
            errors.append(f"close_issues 中 issue #{number} 缺少验收或验证证据。")
        if number not in gate_reviewed:
            errors.append(f"Branch Review Gate 未记录对 close issue #{number} 的覆盖结论。")
    return errors


def review_gate_config(config: dict[str, Any]) -> dict[str, Any]:
    value = config.get("review_gate")
    return value if isinstance(value, dict) else dict(DEFAULTS["review_gate"])


def publish_config(config: dict[str, Any]) -> dict[str, Any]:
    value = config.get("publish")
    return value if isinstance(value, dict) else dict(DEFAULTS["publish"])


def validate_publish_invocation(args: argparse.Namespace) -> None:
    if getattr(args, "from_finish_work", False) or getattr(args, "recovery_after_finish_work", False):
        return
    raise WorkflowError(
        "publish-pr is an internal helper. Run `.trellis/guru-team/scripts/bash/finish-work.sh --json` "
        "so archive and journal complete before PR publish. If finish-work already completed and only "
        "publish recovery is needed, rerun publish-pr with --recovery-after-finish-work.",
        exit_code=2,
        payload={
            "blocked_step": "publish-pr",
            "required_entrypoint": ".trellis/guru-team/scripts/bash/finish-work.sh --json",
            "recovery_flag": "--recovery-after-finish-work",
        },
    )


def validate_finish_work_invocation(args: argparse.Namespace) -> None:
    if getattr(args, "from_trellis_finish_work", False):
        return
    raise WorkflowError(
        "finish-work is the closeout helper and must be entered through the explicit "
        "`trellis-finish-work` skill/command, not chained from `trellis-continue`. "
        "Run `.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work` "
        "only after the user/session explicitly invoked trellis-finish-work.",
        exit_code=2,
        payload={
            "blocked_step": "finish-work",
            "required_entrypoint": "trellis-finish-work",
            "intent_flag": "--from-trellis-finish-work",
        },
    )


def configured_review_gate_path(task_dir: Path, config: dict[str, Any]) -> Path:
    gate_config = review_gate_config(config)
    configured = Path(str(gate_config.get("artifact_path") or "review-gate.json"))
    return configured if configured.is_absolute() else task_dir / configured


def parse_finding_arg(value: str) -> dict[str, Any]:
    parts = [part.strip() for part in value.split("|")]
    if len(parts) < 2:
        raise WorkflowError("Invalid --finding format. Use PRIORITY|message[|path].")
    priority = parts[0].upper()
    if priority not in VALID_PRIORITIES:
        raise WorkflowError(f"Invalid finding priority: {priority}")
    return {
        "priority": priority,
        "message": parts[1],
        "path": parts[2] if len(parts) >= 3 else "",
    }


def load_findings(args: argparse.Namespace) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if getattr(args, "findings_file", None):
        raw = json.loads(Path(args.findings_file).read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            raw = raw.get("findings", [])
        if not isinstance(raw, list):
            raise WorkflowError("--findings-file must contain a JSON list or an object with findings[].")
        for item in raw:
            if not isinstance(item, dict):
                raise WorkflowError("Each finding must be an object.")
            priority = str(item.get("priority") or "").upper()
            if priority not in VALID_PRIORITIES:
                raise WorkflowError(f"Invalid finding priority: {priority}")
            normalized = dict(item)
            normalized["priority"] = priority
            findings.append(normalized)
    for value in getattr(args, "finding", []) or []:
        findings.append(parse_finding_arg(value))
    return findings


def load_review_report(root: Path, task_dir: Path, report_arg: str | None) -> dict[str, Any] | None:
    if not report_arg:
        return None
    raw_path = Path(report_arg).expanduser()
    path = raw_path if raw_path.is_absolute() else root / raw_path
    if not path.exists():
        raise WorkflowError(f"--review-report not found: {path}")
    if not path.is_file():
        raise WorkflowError(f"--review-report must point to a file: {path}")
    if task_dir.resolve() not in [path.resolve(), *path.resolve().parents]:
        raise WorkflowError("--review-report must point to a task-local review.md inside the current task directory.")
    if path.name != "review.md":
        raise WorkflowError("--review-report must point to the task-local review.md file, not another task artifact.")
    content = path.read_bytes()
    if not content.strip():
        raise WorkflowError("--review-report must not be empty.")
    stat = path.stat()
    return {
        "path": repo_relative(root, path),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
    }


def resolve_task_local_path(root: Path, task_dir: Path, value: str) -> Path:
    raw_path = Path(value).expanduser()
    if raw_path.is_absolute():
        path = raw_path
    elif str(value).startswith(".trellis/") or str(value).startswith("trellis/"):
        path = root / raw_path
    else:
        path = task_dir / raw_path
    resolved = path.resolve()
    if task_dir.resolve() not in [resolved, *resolved.parents]:
        raise WorkflowError(f"Artifact path must stay inside the current task directory: {value}")
    return resolved


def resolve_repo_path(root: Path, value: str) -> Path:
    raw_path = Path(value).expanduser()
    return raw_path if raw_path.is_absolute() else root / raw_path


def resolve_checked_spec_path(root: Path, value: str) -> Path:
    path = resolve_repo_path(root, value).resolve()
    spec_root = (root / ".trellis/spec").resolve()
    if spec_root not in [path, *path.parents]:
        raise WorkflowError(f"Checked spec must stay inside .trellis/spec: {value}", exit_code=2)
    return path


def file_digest(root: Path, path: Path) -> dict[str, Any]:
    if not path.exists():
        raise WorkflowError(f"Required artifact not found: {path}")
    if not path.is_file():
        raise WorkflowError(f"Artifact must point to a file: {path}")
    content = path.read_bytes()
    if not content.strip():
        raise WorkflowError(f"Artifact must not be empty: {path}")
    stat = path.stat()
    return {
        "path": repo_relative(root, path),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
    }


def digest_errors(root: Path, entry: Any, label: str) -> list[str]:
    if not isinstance(entry, dict):
        return [f"{label} 中存在非对象 artifact entry。"]
    errors: list[str] = []
    path_value = str(entry.get("path") or "").strip()
    if not path_value:
        return [f"{label} artifact entry 缺少 path。"]
    path = resolve_repo_path(root, path_value)
    if not path.exists() or not path.is_file():
        return [f"{label} artifact 不存在或不是文件: {path_value}。"]
    current = file_digest(root, path)
    for key in ["sha256", "size_bytes"]:
        if entry.get(key) != current.get(key):
            errors.append(f"{label} artifact 已过期: {path_value} 的 {key} 不匹配。")
    if not entry.get("modified_at"):
        errors.append(f"{label} artifact 缺少 modified_at: {path_value}。")
    return errors


def default_existing_task_artifacts(task_dir: Path, names: list[str]) -> list[str]:
    artifacts: list[str] = []
    for name in names:
        if (task_dir / name).is_file():
            artifacts.append(name)
    return artifacts


def dirty_paths_excluding(root: Path, excluded: set[str]) -> list[str]:
    return [
        path
        for path in git_status_paths(root)
        if path not in excluded
    ]


def planning_approval_path(task_dir: Path) -> Path:
    return task_dir / PLANNING_APPROVAL_ARTIFACT


def phase2_check_path(task_dir: Path) -> Path:
    return task_dir / PHASE2_CHECK_ARTIFACT


def valid_review_report_fields(review_report: Any) -> list[str]:
    if not isinstance(review_report, dict):
        return ["Branch Review Gate 缺少 review_report；passed gate 必须引用 task-local review.md digest。"]
    errors: list[str] = []
    for key in ["path", "sha256", "size_bytes", "modified_at"]:
        if not review_report.get(key):
            errors.append(f"Branch Review Gate review_report 缺少 {key}。")
    return errors


def reviewer_identity_errors(reviewer: str) -> list[str]:
    value = reviewer.strip()
    if not value:
        return ["Branch Review Gate 缺少 reviewer identity。"]
    if any(pattern.search(value) for pattern in SELF_REVIEWER_PATTERNS):
        return [
            "Branch Review Gate reviewer 不能是 main-session / self-review；通过门禁必须基于独立 Agent 审查。",
        ]
    return []


def independent_review_source_errors(review_source: str, reviewer: str) -> list[str]:
    errors: list[str] = []
    if review_source != INDEPENDENT_REVIEW_SOURCE:
        errors.append(
            f"Branch Review Gate review_source 必须是 {INDEPENDENT_REVIEW_SOURCE}；脚本 gate 只能记录独立 Agent 审查后的结果。",
        )
    errors.extend(reviewer_identity_errors(reviewer))
    return errors


def blocking_findings(findings: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
    block = {str(item).upper() for item in review_gate_config(config).get("block_priorities", ["P0", "P1", "P2"])}
    return [finding for finding in findings if str(finding.get("priority") or "").upper() in block]


def unresolved_blocking_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    for finding in findings:
        priority = str(finding.get("priority") or "").upper()
        status = str(finding.get("status") or "").strip().lower()
        if priority in BLOCKING_PRIORITIES and status not in RESOLVED_FINDING_STATUSES:
            blockers.append(finding)
    return blockers


def build_planning_approval_payload(
    root: Path,
    task_dir: Path,
    reviewer: str,
    approval_summary: str,
    user_confirmation: str,
    artifacts: list[str],
) -> dict[str, Any]:
    artifact_paths = artifacts or default_existing_task_artifacts(task_dir, DEFAULT_PLANNING_ARTIFACTS)
    if not artifact_paths:
        raise WorkflowError("planning approval needs at least prd.md as an approved artifact.", exit_code=2)
    approved = [file_digest(root, resolve_task_local_path(root, task_dir, item)) for item in artifact_paths]
    artifact_repo_paths = {str(item["path"]) for item in approved}
    dirty_paths = dirty_paths_excluding(root, artifact_repo_paths)
    return {
        "schema_version": "1.0",
        "generated_at": now_iso(),
        "task_dir": repo_relative(root, task_dir),
        "head": current_head(root),
        "dirty_paths": dirty_paths,
        "reviewer": reviewer,
        "approval_summary": approval_summary,
        "user_confirmation": {
            "source": "workflow",
            "message": user_confirmation,
        },
        "approved_artifacts": approved,
        "notes": "record-planning-approval 是 recorder / validator：记录已经完成的 AI/human planning review 和用户确认；它不替代 planning 判断。",
    }


def validate_planning_approval(
    root: Path,
    task_dir: Path,
    allow_committed_head: bool = False,
) -> tuple[Path, dict[str, Any], list[str]]:
    path = planning_approval_path(task_dir)
    if not path.exists():
        raise WorkflowError(f"Planning approval artifact not found: {path}", exit_code=2)
    payload = read_json(path)
    errors: list[str] = []
    if not str(payload.get("approval_summary") or "").strip():
        errors.append("planning-approval.json 缺少 approval_summary。")
    if not str(payload.get("reviewer") or "").strip():
        errors.append("planning-approval.json 缺少 reviewer。")
    if not isinstance(payload.get("user_confirmation"), dict) or not str(payload["user_confirmation"].get("message") or "").strip():
        errors.append("planning-approval.json 缺少用户确认摘要。")
    recorded_head = str(payload.get("head") or "")
    head = current_head(root)
    if recorded_head != head:
        if allow_committed_head and recorded_head and is_ancestor(root, recorded_head, "HEAD"):
            pass
        else:
            errors.append(f"planning-approval.json 记录的 HEAD {recorded_head or '(missing)'} 与当前 HEAD {head} 不一致。")
    approved = payload.get("approved_artifacts")
    if not isinstance(approved, list) or not approved:
        errors.append("planning-approval.json 缺少 approved_artifacts。")
    else:
        approved_paths = {str(item.get("path") or "") for item in approved if isinstance(item, dict)}
        if repo_relative(root, task_dir / "prd.md") not in approved_paths:
            errors.append("planning-approval.json 未记录 prd.md。")
        for item in approved:
            errors.extend(digest_errors(root, item, "planning approval"))
    return path, payload, errors


def normalize_coverage(items: list[str] | None) -> dict[str, bool]:
    coverage = {key: False for key in REQUIRED_PHASE2_COVERAGE}
    for item in items or []:
        key = str(item).strip()
        if not key:
            continue
        if key not in coverage:
            raise WorkflowError(
                f"Unknown phase2 coverage key: {key}. Valid keys: {', '.join(REQUIRED_PHASE2_COVERAGE)}",
                exit_code=2,
            )
        coverage[key] = True
    return coverage


def recorded_digest_paths(entries: Any) -> set[str]:
    if not isinstance(entries, list):
        return set()
    paths: set[str] = set()
    for entry in entries:
        if isinstance(entry, dict) and str(entry.get("path") or "").strip():
            paths.add(str(entry["path"]))
    return paths


def parse_validation_arg(value: str) -> dict[str, Any]:
    parts = [part.strip() for part in value.split("|", 1)]
    command = parts[0]
    result = parts[1] if len(parts) > 1 else "recorded"
    if not command:
        raise WorkflowError("Validation evidence command must not be empty.", exit_code=2)
    return {"command": command, "result": result}


def build_phase2_check_payload(
    root: Path,
    task_dir: Path,
    handoff: dict[str, Any],
    task: dict[str, Any],
    checker: str,
    check_summary: str,
    checked_artifacts: list[str],
    checked_specs: list[str],
    coverage_items: list[str],
    validation_items: list[str],
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    base_branch = base_branch_from_sources(argparse.Namespace(base_branch=None), task, handoff)
    task_artifact_names = checked_artifacts or default_existing_task_artifacts(task_dir, DEFAULT_PHASE2_TASK_ARTIFACTS)
    task_artifacts = [file_digest(root, resolve_task_local_path(root, task_dir, item)) for item in task_artifact_names]
    specs = [file_digest(root, resolve_checked_spec_path(root, item)) for item in checked_specs]
    validation_commands = [parse_validation_arg(item) for item in validation_items]
    coverage = normalize_coverage(coverage_items)
    excluded = {str(item["path"]) for item in task_artifacts}
    excluded.add(repo_relative(root, phase2_check_path(task_dir)))
    dirty_paths = dirty_paths_excluding(root, excluded)
    return {
        "schema_version": "1.0",
        "generated_at": now_iso(),
        "task_dir": repo_relative(root, task_dir),
        "base_branch": base_branch,
        "head": current_head(root),
        "diff_range": diff_range(root, base_branch),
        "dirty_paths": dirty_paths,
        "checker": checker,
        "check_summary": check_summary,
        "checked_artifacts": task_artifacts,
        "checked_specs": specs,
        "coverage": coverage,
        "validation_commands": validation_commands,
        "findings": findings,
        "notes": "record-phase2-check 是 recorder / validator：记录已经完成的完整 trellis-check 结论、证据和 stale 判定；验证命令只是 check evidence 的一部分。",
    }


def validate_phase2_check(
    root: Path,
    task_dir: Path,
    allow_committed_head: bool = False,
) -> tuple[Path, dict[str, Any], list[str]]:
    path = phase2_check_path(task_dir)
    if not path.exists():
        raise WorkflowError(f"Phase 2 check artifact not found: {path}", exit_code=2)
    payload = read_json(path)
    errors: list[str] = []
    if not str(payload.get("check_summary") or "").strip():
        errors.append("phase2-check.json 缺少 check_summary。")
    if not str(payload.get("checker") or "").strip():
        errors.append("phase2-check.json 缺少 checker。")
    recorded_head = str(payload.get("head") or "")
    head = current_head(root)
    accepted_committed_state = False
    if recorded_head != head:
        if allow_committed_head and recorded_head and is_ancestor(root, recorded_head, "HEAD"):
            metadata_only, tail_files = metadata_only_since(root, recorded_head)
            if not metadata_only:
                errors.append(
                    "phase2-check.json 记录的 HEAD 是当前 HEAD 的祖先，但之后提交了非 Trellis metadata 变更: "
                    + ", ".join(tail_files[:20])
                )
            else:
                has_non_metadata, non_metadata_paths = has_non_metadata_dirty_paths(root)
                if has_non_metadata:
                    errors.append(
                        "phase2-check.json 记录的 HEAD 是当前 HEAD 的祖先，但工作区存在非 Trellis metadata 变更: "
                        + ", ".join(non_metadata_paths[:20])
                    )
                else:
                    accepted_committed_state = True
        else:
            errors.append(f"phase2-check.json 记录的 HEAD {recorded_head or '(missing)'} 与当前 HEAD {head} 不一致。")
    dirty_excluded = {repo_relative(root, phase2_check_path(task_dir))}
    dirty_excluded.update(recorded_digest_paths(payload.get("checked_artifacts")))
    dirty_now = dirty_paths_excluding(root, dirty_excluded)
    recorded_dirty = payload.get("dirty_paths")
    if not isinstance(recorded_dirty, list):
        errors.append("phase2-check.json 缺少 dirty_paths 数组。")
    elif accepted_committed_state:
        pass
    elif sorted(str(item) for item in recorded_dirty) != sorted(dirty_now):
        errors.append("phase2-check.json 记录的 dirty_paths 与当前 working tree 不一致。")
    coverage = payload.get("coverage")
    if not isinstance(coverage, dict):
        errors.append("phase2-check.json 缺少 coverage。")
    else:
        for key in REQUIRED_PHASE2_COVERAGE:
            if coverage.get(key) is not True:
                errors.append(f"phase2-check.json coverage.{key} 不是 true。")
    validation_commands = payload.get("validation_commands")
    if not isinstance(validation_commands, list) or not validation_commands:
        errors.append("phase2-check.json 缺少 validation_commands。")
    checked_artifacts = payload.get("checked_artifacts")
    if not isinstance(checked_artifacts, list) or not checked_artifacts:
        errors.append("phase2-check.json 缺少 checked_artifacts。")
    else:
        for item in checked_artifacts:
            errors.extend(digest_errors(root, item, "phase2 checked_artifacts"))
    checked_specs = payload.get("checked_specs")
    if isinstance(checked_specs, list):
        for item in checked_specs:
            errors.extend(digest_errors(root, item, "phase2 checked_specs"))
    findings = payload.get("findings")
    if not isinstance(findings, list):
        errors.append("phase2-check.json 缺少 findings 数组。")
    else:
        blockers = unresolved_blocking_findings([item for item in findings if isinstance(item, dict)])
        if blockers:
            errors.append("phase2-check.json 存在未 resolved 的 P0/P1/P2 finding。")
    return path, payload, errors


def build_review_gate_payload(
    root: Path,
    task_dir: Path,
    config: dict[str, Any],
    handoff: dict[str, Any],
    base_branch: str,
    findings: list[dict[str, Any]],
    command: list[str],
    summary: str,
    evidence: list[str],
    reviewer: str,
    review_source: str,
    review_report: dict[str, Any] | None,
) -> dict[str, Any]:
    diff_spec = diff_range(root, base_branch)
    files = changed_files(root, diff_spec)
    deployment_impact = detect_deployment_impact(files)
    blockers = blocking_findings(findings, config)
    ledger = load_issue_scope_ledger(task_dir, handoff)
    close_issues = ledger.get("close_issues") if isinstance(ledger.get("close_issues"), list) else []
    return {
        "schema_version": "1.0",
        "generated_at": now_iso(),
        "task_dir": repo_relative(root, task_dir),
        "base_branch": base_branch,
        "base_ref": diff_base_ref(root, base_branch),
        "head_branch": current_branch(root),
        "head": current_head(root),
        "diff_range": diff_spec,
        "changed_files": files,
        "review_scope": [
            "文档",
            "代码",
            "测试",
            "Trellis artifacts",
            "配置",
            "脚本",
            "schema",
            "CI/CD workflow 与发布自动化",
            "Dockerfile / Docker Compose / 容器启动脚本",
            "Kubernetes YAML / Helm values / Kustomize base 和 overlay",
            "数据库 schema / migration / seed / backfill 脚本",
            "各目录下本次变更涉及的 Makefile",
            "preset installer",
        ],
        "command": command,
        "conclusion": {
            "passed": not blockers,
            "summary": summary or ("Branch Review Gate 通过。" if not blockers else "Branch Review Gate 未通过。"),
            "block_priorities": review_gate_config(config).get("block_priorities", ["P0", "P1", "P2"]),
            "blocking_findings_count": len(blockers),
        },
        "findings": findings,
        "issue_scope": {
            "ledger_path": repo_relative(root, issue_scope_ledger_path(task_dir)),
            "close_issues_reviewed": close_issues,
            "related_issues": ledger.get("related_issues", []),
            "followup_issues": ledger.get("followup_issues", []),
        },
        "verification_evidence": {
            "base_head": f"{diff_base_ref(root, base_branch)}...{current_head(root)}",
            "changed_file_count": len(files),
            "reviewer": reviewer,
            "review_source": review_source,
            "review_report": review_report,
            "evidence": evidence,
            "notes": "review-branch 是 recorder / validator：记录已经完成的 AI/human review 结论、diff 范围和审查证据；它不执行 review 判断。",
        },
        "deployment_impact": deployment_impact,
    }


def repo_relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def load_review_gate(task_dir: Path, config: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    path = configured_review_gate_path(task_dir, config)
    if not path.exists():
        raise WorkflowError(f"Branch Review Gate artifact not found: {path}")
    return path, read_json(path)


def metadata_only_since(root: Path, reviewed_head: str) -> tuple[bool, list[str]]:
    proc = run(["git", "diff", "--name-only", f"{reviewed_head}...HEAD"], cwd=root, check=False)
    if proc.returncode != 0:
        return False, []
    files = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    return all(path.startswith(METADATA_ONLY_PREFIXES) or path in METADATA_ONLY_FILES for path in files), files


def validate_review_gate(
    root: Path,
    task_dir: Path,
    config: dict[str, Any],
    allow_metadata_after_gate: bool,
) -> tuple[Path, dict[str, Any], list[str]]:
    path, gate = load_review_gate(task_dir, config)
    errors: list[str] = []
    conclusion = gate.get("conclusion") if isinstance(gate.get("conclusion"), dict) else {}
    if conclusion.get("passed") is not True:
        errors.append("Branch Review Gate 结论不是 passed=true。")
    if not str(conclusion.get("summary") or "").strip():
        errors.append("Branch Review Gate 缺少中文 summary。")
    verification = gate.get("verification_evidence") if isinstance(gate.get("verification_evidence"), dict) else {}
    evidence = verification.get("evidence")
    if not (isinstance(evidence, list) and any(str(item).strip() for item in evidence)):
        errors.append("Branch Review Gate 缺少具体 review evidence。")
    reviewer = str(verification.get("reviewer") or "").strip()
    review_source = str(verification.get("review_source") or "").strip()
    errors.extend(independent_review_source_errors(review_source, reviewer))
    review_report = verification.get("review_report") if isinstance(verification.get("review_report"), dict) else None
    errors.extend(valid_review_report_fields(review_report))
    reviewed_head = str(gate.get("head") or "")
    head = current_head(root)
    gate_config = review_gate_config(config)
    require_head_match = bool(gate_config.get("require_head_match", True))
    if require_head_match and reviewed_head != head:
        accepted_metadata_tail = False
        if allow_metadata_after_gate and reviewed_head and is_ancestor(root, reviewed_head, "HEAD"):
            metadata_only, tail_files = metadata_only_since(root, reviewed_head)
            accepted_metadata_tail = metadata_only
            if not metadata_only:
                errors.append(
                    "Branch Review Gate 通过后出现非 Trellis metadata 变更: "
                    + ", ".join(tail_files[:20])
                )
        if not accepted_metadata_tail:
            errors.append(f"Branch Review Gate 记录的 HEAD {reviewed_head or '(missing)'} 与当前 HEAD {head} 不一致。")
    return path, gate, errors


def base_branch_from_sources(args: argparse.Namespace, task: dict[str, Any], handoff: dict[str, Any]) -> str:
    for value in [
        getattr(args, "base_branch", None),
        handoff.get("base_branch"),
        task.get("base_branch"),
    ]:
        if value:
            return str(value)
    raise WorkflowError("Could not resolve base_branch from args, handoff, or task.json.")


def pr_issue_line(keyword: str, issue: dict[str, Any], mode: str) -> str:
    number = issue.get("number")
    title = str(issue.get("title") or "").strip()
    suffix = f" - {title}" if title else ""
    if mode == "close":
        return f"- {keyword} #{number}{suffix}"
    if mode == "followup":
        return f"- Follow-up #{number}{suffix}"
    return f"- Refs #{number}{suffix}"


def markdown_section_ranges(body: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^(#{2,6})\s+(.+?)\s*$", body))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[title] = body[start:end].strip()
    return sections


def find_pr_body_sections(body: str) -> dict[str, str]:
    raw_sections = markdown_section_ranges(body)
    found: dict[str, str] = {}
    for required, aliases in PR_BODY_SECTION_ALIASES.items():
        for title, content in raw_sections.items():
            normalized_title = re.sub(r"\s+", " ", title).strip()
            if any(alias.lower() in normalized_title.lower() for alias in aliases):
                found[required] = content
                break
    return found


def normalized_body_line(line: str) -> str:
    return line.strip().lstrip("-*•").strip()


def section_has_specific_bullet(section: str) -> bool:
    for line in section.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("-") or stripped.startswith("*") or stripped.startswith("•")):
            continue
        normalized = normalized_body_line(stripped).lower()
        if normalized in PR_BODY_PLACEHOLDER_VALUES:
            continue
        if "详见" in normalized:
            continue
        if len(normalized) < 8:
            continue
        return True
    return False


def section_has_substantive_text(section: str) -> bool:
    lines = [normalized_body_line(line) for line in section.splitlines()]
    meaningful = [line for line in lines if line and line.lower() not in PR_BODY_PLACEHOLDER_VALUES]
    if not meaningful:
        return False
    return any("详见" not in line for line in meaningful)


def issue_number_set(items: Any) -> set[int]:
    return set(issue_numbers(items))


def close_keyword_pattern() -> re.Pattern[str]:
    return re.compile(r"(?i)\b(" + "|".join(re.escape(keyword) for keyword in PR_CLOSE_KEYWORDS) + r")\s+#(\d+)\b")


def is_reviewed_pr_body_source(body_source: str) -> bool:
    return body_source.startswith(REVIEWED_PR_BODY_SOURCE_PREFIXES)


def active_task_relative_path(root: Path, task_dir: Path, body_path_arg: str | None) -> str | None:
    if not body_path_arg:
        return None
    raw_path = Path(body_path_arg).expanduser()
    path = raw_path if raw_path.is_absolute() else root / raw_path
    try:
        return path.resolve().relative_to(task_dir.resolve()).as_posix()
    except ValueError:
        return None


def rewrite_active_task_artifact_path(root: Path, task_dir: Path, archived_task_dir: Path, body_path_arg: str | None) -> str | None:
    relative = active_task_relative_path(root, task_dir, body_path_arg)
    if relative is None:
        return body_path_arg
    return str(archived_task_dir / relative)


def load_pr_body_artifact(root: Path, artifact_arg: str | None) -> tuple[str | None, Path | None]:
    if not artifact_arg:
        return None, None
    raw_path = Path(artifact_arg).expanduser()
    path = raw_path if raw_path.is_absolute() else root / raw_path
    payload = read_json(path)
    ready = payload.get("ready")
    if ready is not True:
        raise WorkflowError("PR body readiness artifact is not ready=true.", exit_code=2, payload={"artifact_path": str(path)})
    body_file = str(payload.get("body_file") or "").strip()
    if body_file:
        body_path = Path(body_file).expanduser()
        resolved = body_path if body_path.is_absolute() else path.parent / body_path
        return read_pr_body_file(root, str(resolved)), resolved
    body = payload.get("body")
    if isinstance(body, str) and body.strip():
        return body.strip() + "\n", path
    raise WorkflowError(
        "PR body readiness artifact must contain a non-empty body or body_file.",
        exit_code=2,
        payload={"artifact_path": str(path)},
    )


def read_pr_body_file(root: Path, body_file: str | None) -> str | None:
    if not body_file:
        return None
    raw_path = Path(body_file).expanduser()
    path = raw_path if raw_path.is_absolute() else root / raw_path
    if not path.exists():
        raise WorkflowError(f"PR body file not found: {path}", exit_code=2)
    if not path.is_file():
        raise WorkflowError(f"PR body file must point to a file: {path}", exit_code=2)
    body = path.read_text(encoding="utf-8").strip()
    if not body:
        raise WorkflowError(f"PR body file is empty: {path}", exit_code=2)
    return body + "\n"


def resolve_pr_body(
    root: Path,
    args: argparse.Namespace,
    ledger: dict[str, Any],
    gate: dict[str, Any],
    validations: list[str],
    config: dict[str, Any],
) -> tuple[str, str]:
    file_body = read_pr_body_file(root, getattr(args, "body_file", None))
    if file_body is not None:
        return file_body, f"body-file:{getattr(args, 'body_file')}"
    artifact_body, artifact_path = load_pr_body_artifact(root, getattr(args, "body_artifact", None))
    if artifact_body is not None:
        return artifact_body, f"body-artifact:{artifact_path}"
    return build_pr_body(ledger, gate, validations, config), "generated"


def validate_reviewed_body_source_for_publish(body_source: str, draft: bool) -> list[str]:
    if draft or is_reviewed_pr_body_source(body_source):
        return []
    return [
        "non-draft publish requires an AI-reviewed --body-file or --body-artifact; generated PR body is preview-only.",
    ]


def validate_pr_body_quality(body: str, ledger: dict[str, Any], draft: bool) -> list[str]:
    errors: list[str] = []
    sections = find_pr_body_sections(body)
    for section in PR_BODY_REQUIRED_SECTIONS:
        if section not in sections:
            errors.append(f"PR body 缺少 `{section}` section。")

    if not draft:
        for phrase in PR_BODY_LOW_INFORMATION_PHRASES:
            if phrase in body:
                errors.append(f"PR body 包含低信息量摘要或占位短语：{phrase}")

    summary = sections.get("变更摘要", "")
    if summary and not section_has_specific_bullet(summary):
        errors.append("PR body `变更摘要` 缺少具体 bullet。")
    for section in ["影响范围", "验证结果", "安全说明"]:
        value = sections.get(section, "")
        if value and not section_has_substantive_text(value):
            errors.append(f"PR body `{section}` 缺少具体内容。")

    close_allowed = issue_number_set(ledger.get("close_issues"))
    related_numbers = issue_number_set(ledger.get("related_issues"))
    followup_numbers = issue_number_set(ledger.get("followup_issues"))
    for match in close_keyword_pattern().finditer(body):
        number = int(match.group(2))
        if number not in close_allowed:
            errors.append(f"PR body 对非 close_issues issue #{number} 使用了 close keyword。")
        if number in related_numbers or number in followup_numbers:
            errors.append(f"PR body 对 related/followup issue #{number} 使用了 close keyword。")
    return errors


def build_pr_body(ledger: dict[str, Any], gate: dict[str, Any], validations: list[str], config: dict[str, Any]) -> str:
    publish = publish_config(config)
    keyword = str(publish.get("close_keyword") or "Closes")
    close_issues = ledger.get("close_issues") if isinstance(ledger.get("close_issues"), list) else []
    related_issues = ledger.get("related_issues") if isinstance(ledger.get("related_issues"), list) else []
    followup_issues = ledger.get("followup_issues") if isinstance(ledger.get("followup_issues"), list) else []

    close_lines = "\n".join(pr_issue_line(keyword, issue, "close") for issue in close_issues) or "- 无"
    related_lines = "\n".join(pr_issue_line(keyword, issue, "related") for issue in related_issues) or "- 无"
    followup_lines = "\n".join(pr_issue_line(keyword, issue, "followup") for issue in followup_issues) or "- 无"
    validation_lines = "\n".join(f"- {item}" for item in validations) or "- 未提供具体 publish validation；non-draft publish 会被 PR body 质量校验阻塞。"
    gate_summary = gate.get("conclusion", {}).get("summary", "Branch Review Gate 通过。")
    gate_head = gate.get("head", "")
    gate_range = gate.get("diff_range", "")
    changed_files = gate.get("changed_files") if isinstance(gate.get("changed_files"), list) else []
    impact = gate.get("deployment_impact") if isinstance(gate.get("deployment_impact"), dict) else {}
    changed_file_lines = "\n".join(f"- `{path}`" for path in changed_files[:12]) or "- 未记录 changed_files；需要 AI 在 body file 中补充影响范围。"
    deployment_note = "未检测到部署资产变更。"
    if impact.get("needs_deployment_impact_review"):
        deployment_note = "Review Gate 已要求覆盖部署影响判断；请结合 gate evidence 确认是否需要 CI/CD、容器、K8s、migration 或 Makefile 更新。"
    summary_items: list[str] = []
    for issue in close_issues[:5]:
        number = issue.get("number")
        title = str(issue.get("title") or "").strip()
        if number and title:
            summary_items.append(f"- 完成 #{number}：{title}。")
        elif number:
            summary_items.append(f"- 完成 #{number} 对应的 PR 关闭范围。")
    if not summary_items:
        summary_items.append("- 完成 Issue Scope Ledger 中记录的 PR 关闭范围。")
    summary_items.append(f"- Review Gate 结论：{gate_summary}")
    summary_bullets = "\n".join(summary_items)

    return f"""## 变更摘要

{summary_bullets}

## 影响范围

{changed_file_lines}

## 验证结果

{validation_lines}

## Review Gate

- 结论：{gate_summary}
- Reviewed HEAD：`{gate_head}`
- Diff 范围：`{gate_range}`

## Issue 关闭范围

{close_lines}

### 仅引用或相关

{related_lines}

### 后续范围

{followup_lines}

## 安全说明

- 未在 PR 正文中包含 token、secret、签名 URL、`.env` 内容或数据库 URL。
- {deployment_note}
"""


def pr_title_from_task(task: dict[str, Any], args: argparse.Namespace) -> str:
    if getattr(args, "title", None):
        return str(args.title)
    title = str(task.get("title") or task.get("name") or "Trellis task").strip()
    return f"完成：{title}"


def check_env_payload(root: Path) -> dict[str, Any]:
    root = repo_root(root)
    config = load_config(root)
    repo = str(config.get("github_repo") or "").strip() or infer_github_repo(root)
    current = current_branch(root)
    base, candidates = resolve_base_branch(root, config)
    gh_installed = shutil.which("gh") is not None
    gh_authenticated = run(["gh", "auth", "status"], cwd=root, check=False).returncode == 0 if gh_installed else False
    extension = guru_team_extension_payload(root)
    warnings: list[str] = []
    next_steps: list[str] = []
    if not repo:
        warnings.append("github_repo is not configured and could not be inferred from the Git origin remote.")
        next_steps.append(
            "Set `github_repo: owner/repo` in `.trellis/guru-team/config.yml` "
            "or configure a GitHub `origin` remote before GitHub issue intake or publish."
        )
    if not gh_installed:
        warnings.append("GitHub CLI is not installed.")
        next_steps.append("Install `gh` before using Guru Team GitHub issue intake or publish.")
    elif not gh_authenticated:
        warnings.append("GitHub CLI is not authenticated.")
        next_steps.append("Run `gh auth login` before using Guru Team GitHub issue intake or publish.")
    if extension.get("status") == "missing":
        warnings.append("Guru Team extension manifest is not installed.")
        next_steps.append("Re-apply the Guru Team preset so `.trellis/guru-team/extension.json` records the installed extension version.")
    elif extension.get("status") == "invalid":
        warnings.append("Guru Team extension manifest is invalid.")
        next_steps.append("Inspect `.trellis/guru-team/extension.json` or re-apply the Guru Team preset.")
    payload = {
        "status": "ok",
        "repo_root": str(root),
        "github_repo": repo,
        "trellis_installed": (root / ".trellis").is_dir(),
        "guru_team_extension": extension,
        "gh_installed": gh_installed,
        "gh_authenticated": gh_authenticated,
        "current_branch": current,
        "base_branch": base,
        "base_branch_candidates": candidates,
        "dirty": git_dirty(root),
        "worktree_root": str(configured_worktree_root(root, config)),
        "existing_worktrees": worktree_lines(root),
    }
    if warnings:
        payload["warnings"] = warnings
    if next_steps:
        payload["next_steps"] = next_steps
    return payload


def cmd_version(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    return {
        "status": "ok",
        "repo_root": str(root),
        "guru_team_extension": guru_team_extension_payload(root),
    }


def infer_assignee(root: Path, explicit: str | None) -> str | None:
    if explicit:
        return explicit
    return developer_name_from_identity(read_developer_identity(root))


def create_task(root: Path, payload: dict[str, Any], args: argparse.Namespace) -> str:
    task_script = root / ".trellis/scripts/task.py"
    if not task_script.exists():
        raise WorkflowError(f"Trellis task script not found: {task_script}")
    workspace = Path(payload["workspace_path"])
    cmd = ["python3", "./.trellis/scripts/task.py", "create", payload["task_title"], "--slug", payload["task_slug"]]
    assignee = infer_assignee(root, args.assignee)
    if assignee:
        cmd.extend(["--assignee", assignee])
    if args.priority:
        cmd.extend(["--priority", args.priority])
    if args.description:
        cmd.extend(["--description", args.description])
    proc = run(cmd, cwd=workspace, check=False)
    if proc.returncode != 0:
        raise WorkflowError(f"task.py create failed:\n{proc.stderr.strip()}")
    return proc.stdout.strip()


def cmd_prepare(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    repo = str(config.get("github_repo") or "").strip() or infer_github_repo(root)
    if not repo:
        raise WorkflowError("Could not resolve GitHub repo. Configure github_repo in .trellis/guru-team/config.yml.")
    if args.create_issue_confirmed and not str(args.issue_title or "").strip():
        raise WorkflowError(
            "--create-issue-confirmed requires --issue-title containing the AI/human reviewed issue title.",
            exit_code=2,
        )

    require_tool("git")
    require_gh_auth(root)

    requirement = " ".join(args.requirement).strip()
    if not requirement:
        raise WorkflowError("No requirement description provided.")

    provided = parse_issue_ref(requirement, repo)
    duplicates: list[dict[str, Any]] = []
    duplicate_search_performed = False
    created_by_workflow = False
    issue: dict[str, Any] | None = None
    proposed_issue: dict[str, Any] | None = None
    issue_title_for_planning = ""
    issue_number_for_slug = "new"
    source_issue: dict[str, Any] | None = None
    confirmation_required: dict[str, Any] | None = None

    if args.reuse_issue:
        issue = issue_view(repo, int(args.reuse_issue), root)
    elif provided:
        issue_repo, number = provided
        repo = issue_repo
        issue = issue_view(repo, number, root)
    else:
        if config.get("source_issue_required"):
            raise WorkflowError("No source issue provided and source_issue_required is true.")
        if not has_minimum_clarity(requirement):
            raise WorkflowError("Requirement is not clear enough for issue intake. Add target, capability, expected outcome, and boundary/open question.")
        if config.get("duplicate_search_required", True):
            duplicate_search_performed = True
            duplicates = duplicate_search(repo, requirement, root, int(config.get("duplicate_candidate_limit") or 5))
            high = [item for item in duplicates if item.get("similarity") == "high"]
            if high and not args.force_new:
                proposed_title = args.issue_title or make_issue_title(requirement, args.short_name)
                proposed_body = issue_body(requirement, duplicates)
                raise WorkflowError(
                    "Likely duplicate open issue found. Re-run with --reuse-issue <number> or --force-new after user confirmation.",
                    exit_code=2,
                    payload={
                        "duplicates": high,
                        "repo": repo,
                        "proposed_issue": {
                            "repo": repo,
                            "title": proposed_title,
                            "body": proposed_body,
                            "labels": list(config.get("created_issue_labels") or []),
                            "body_reviewed": False,
                            "create_issue_command": confirmed_issue_prepare_command(args, proposed_title, requirement, force_new=True),
                        },
                        "requires_confirmation": {
                            "reuse_issue_or_force_new": True,
                            "reason": "High-similarity duplicate candidates require AI/human review before binding an existing issue or forcing a new one.",
                        },
                    },
                )
        proposed_title = args.issue_title or make_issue_title(requirement, args.short_name)
        proposed_body = read_confirmed_issue_body(args.issue_body_file) if args.create_issue_confirmed else issue_body(requirement, duplicates)
        proposed_issue = {
            "repo": repo,
            "title": proposed_title,
            "body": proposed_body,
            "labels": list(config.get("created_issue_labels") or []),
            "body_reviewed": bool(args.create_issue_confirmed),
            "create_issue_command": confirmed_issue_prepare_command(args, proposed_title, requirement),
        }
        if config.get("auto_create_issue", False):
            proposed_issue["legacy_auto_create_issue_config_ignored"] = True
            proposed_issue["legacy_auto_create_issue_note"] = (
                "auto_create_issue is kept only for backward-compatible config parsing; "
                "prepare requires --create-issue-confirmed before GitHub issue creation."
            )
        if args.create_issue_confirmed:
            issue = create_issue(repo, proposed_title, proposed_body, root, list(config.get("created_issue_labels") or []))
            created_by_workflow = True
        else:
            confirmation_required = {
                "create_issue": True,
                "reason": "No source issue was provided. prepare generated a proposed issue only; an AI/human must review title/body and rerun with --create-issue-confirmed before GitHub issue creation.",
                "next_commands": proposed_issue["create_issue_command"],
            }

    if issue is not None:
        issue_number = int(issue["number"])
        issue_title_for_planning = str(issue.get("title") or make_issue_title(requirement, args.short_name))
        issue_number_for_slug = str(issue_number)
        source_issue = {
            "number": issue_number,
            "url": issue["url"],
            "title": issue_title_for_planning,
            "created_by_workflow": created_by_workflow,
        }
    else:
        issue_title_for_planning = str(proposed_issue.get("title") if proposed_issue else make_issue_title(requirement, args.short_name))
    if (args.create_worktree or args.create_task) and source_issue is None:
        raise WorkflowError(
            "--create-worktree and --create-task require a confirmed source issue. Review proposed_issue, create/bind the GitHub issue, then rerun prepare.",
            exit_code=2,
            payload={"proposed_issue": proposed_issue, "requires_confirmation": confirmation_required},
        )
    issue_slug = slugify(args.short_name or issue_title_for_planning or requirement, f"issue-{issue_number_for_slug}")
    unique_prefix = f"{issue_number_for_slug}-{issue_slug}"
    task_slug = args.task_slug or unique_prefix
    workspace_slug = args.workspace_slug or unique_prefix
    branch_name = args.branch or f"{config.get('branch_prefix') or ''}{unique_prefix}"
    title_prefix = f"#{issue_number_for_slug}" if issue is not None else "[proposed-issue]"
    task_title = args.title or f"{title_prefix} {issue_title_for_planning}"
    base_ref, base_candidates = resolve_base_branch(root, config, args.base_branch)
    should_create_worktree = args.create_worktree or args.create_task
    base_freshness = (
        ensure_base_freshness(root, base_ref)
        if should_create_worktree
        else inspect_base_freshness(root, base_ref)
    )
    workspace_base_ref = str(base_freshness.get("base_ref_for_worktree") or base_ref)
    workspace_mode, workspace_path, workspace_ready = prepare_workspace(
        root,
        config,
        branch_name,
        workspace_slug,
        workspace_base_ref,
        args.worktree,
        should_create_worktree,
    )
    current = current_branch(root)
    assignee = infer_assignee(root, args.assignee)
    developer_identity: dict[str, Any] | None = None
    if should_create_worktree and workspace_ready:
        developer_identity = ensure_workspace_developer_identity(root, workspace_path, assignee)

    create_cmd = ["python3", "./.trellis/scripts/task.py", "create", task_title, "--slug", task_slug]
    if assignee:
        create_cmd.extend(["--assignee", assignee])
    if args.priority:
        create_cmd.extend(["--priority", args.priority])
    if args.description:
        create_cmd.extend(["--description", args.description])

    payload: dict[str, Any] = {
        "schema_version": "1.1",
        "source_issue": source_issue,
        "proposed_issue": proposed_issue,
        "requires_confirmation": confirmation_required,
        "handoff_path": str(workspace_handoff_path(config, workspace_path)),
        "handoff_written": False,
        "slug": issue_slug,
        "task_slug": task_slug,
        "task_title": task_title,
        "branch_name": branch_name,
        "workspace_mode": workspace_mode,
        "workspace_path": str(workspace_path),
        "workspace_ready": workspace_ready,
        "base_branch": base_ref,
        "base_branch_candidates": base_candidates,
        "create_task_command": create_cmd,
        "task_dir": None,
        "duplicate_search": {
            "performed": duplicate_search_performed,
            "candidates": duplicates,
        },
        "issue_scope_ledger": {},
        "preflight": {
            "repo_root": str(root),
            "current_checkout": str(root),
            "current_branch": current,
            "dirty": git_dirty(root),
            "worktree_root": str(configured_worktree_root(root, config)),
            "existing_worktrees": worktree_lines(root),
            "selected_base_branch": base_ref,
            "base_freshness": base_freshness,
            "workspace_was_created_or_reused": workspace_ready,
            "developer_identity": developer_identity,
        },
    }
    if source_issue is not None:
        payload["issue_scope_ledger"] = {
            "primary_issue": issue_entry(
                source_issue["number"],
                source_issue["url"],
                source_issue.get("title", ""),
                "intake/handoff 主 issue，默认进入 close 候选。",
            ),
            "close_issues": [
                issue_entry(
                    source_issue["number"],
                    source_issue["url"],
                    source_issue.get("title", ""),
                    "默认 close 候选；publish 前必须在 task artifact 中补齐验收证据。",
                )
            ],
            "related_issues": [],
            "followup_issues": [],
        }
    else:
        payload["issue_scope_ledger"] = {
            "primary_issue": None,
            "close_issues": [],
            "related_issues": [],
            "followup_issues": [],
            "notes": [
                "尚未创建或绑定 source issue；用户确认 proposed_issue 后重新运行 prepare。",
                "未绑定 source issue 前不得创建 Trellis task 或发布关闭语义。",
            ],
        }

    if args.create_task:
        if source_issue is None:
            raise WorkflowError(
                "--create-task requires a confirmed source issue. Review proposed_issue, create/bind the GitHub issue, then rerun prepare.",
                exit_code=2,
                payload={"proposed_issue": proposed_issue, "requires_confirmation": confirmation_required},
            )
        payload["task_dir"] = create_task(root, payload, args)
        run(["python3", "./.trellis/scripts/task.py", "set-branch", payload["task_dir"], branch_name], cwd=workspace_path, check=False)
        run(["python3", "./.trellis/scripts/task.py", "set-base-branch", payload["task_dir"], base_ref], cwd=workspace_path, check=False)
        run(["python3", "./.trellis/scripts/task.py", "set-scope", payload["task_dir"], f"GitHub issue: {source_issue['url']}"], cwd=workspace_path, check=False)
        task_dir = resolve_task_dir(workspace_path, payload["task_dir"], payload)
        ensure_issue_scope_ledger(task_dir, payload)

    if source_issue is not None and should_create_worktree:
        payload["handoff_written"] = True
        handoff = write_handoff(root, config, payload, workspace_path)
        payload["handoff_path"] = str(handoff)
    return payload


def cmd_review_branch(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    handoff = load_handoff(root, config)
    task_dir = resolve_task_dir(root, args.task, handoff)
    task = task_json(task_dir)
    base_branch = base_branch_from_sources(args, task, handoff)
    ensure_issue_scope_ledger(task_dir, handoff)
    planning_path, _planning_payload, planning_errors = validate_planning_approval(
        root,
        task_dir,
        allow_committed_head=True,
    )
    if planning_errors:
        raise WorkflowError(
            "Branch Review Gate blocked because planning approval evidence is missing, stale, or incomplete.",
            exit_code=2,
            payload={"artifact_path": str(planning_path), "errors": planning_errors},
        )
    phase2_path, _phase2_payload, phase2_errors = validate_phase2_check(root, task_dir, allow_committed_head=True)
    if phase2_errors:
        raise WorkflowError(
            "Branch Review Gate blocked because Phase 2 check report is missing, stale, or incomplete.",
            exit_code=2,
            payload={"artifact_path": str(phase2_path), "errors": phase2_errors},
        )

    findings = load_findings(args)
    evidence = [str(item).strip() for item in (args.evidence or []) if str(item).strip()]
    summary = str(args.summary or "").strip()
    blockers = blocking_findings(findings, config)
    if args.pass_gate and blockers:
        raise WorkflowError("--pass cannot be used when P0/P1/P2 findings are present.")
    if args.pass_gate and not summary:
        raise WorkflowError(
            "Branch Review Gate pass needs --summary with a human-readable Chinese review conclusion.",
            exit_code=2,
        )
    if args.pass_gate and not evidence:
        raise WorkflowError(
            "Branch Review Gate pass needs at least one --evidence line from the actual review.",
            exit_code=2,
        )
    reviewer = str(args.reviewer or "").strip()
    review_source = str(getattr(args, "review_source", "") or "").strip()
    if args.pass_gate:
        source_errors = independent_review_source_errors(review_source, reviewer)
        if source_errors:
            raise WorkflowError(
                "Branch Review Gate pass requires independent Agent review evidence.",
                exit_code=2,
                payload={"errors": source_errors},
            )
    review_report = load_review_report(root, task_dir, args.review_report)
    if not blockers and not evidence:
        raise WorkflowError(
            "Branch Review Gate passing result needs at least one --evidence line from the actual review.",
            exit_code=2,
        )
    if review_report is None:
        raise WorkflowError(
            "Branch Review Gate needs --review-report pointing to the task-local review.md from the prior AI/human review. "
            "--reviewer is identity metadata only and cannot satisfy passed gate evidence.",
            exit_code=2,
        )
    if not args.pass_gate and not findings:
        raise WorkflowError(
            "Branch Review Gate needs an explicit result. Use --pass after review found no P0/P1/P2, or provide --finding/--findings-file.",
            exit_code=2,
        )

    payload = build_review_gate_payload(
        root=root,
        task_dir=task_dir,
        config=config,
        handoff=handoff,
        base_branch=base_branch,
        findings=findings,
        command=sys.argv[:],
        summary=summary,
        evidence=evidence,
        reviewer=reviewer,
        review_source=review_source,
        review_report=review_report,
    )
    if args.pass_gate and bool(review_gate_config(config).get("require_deployment_impact_evidence", True)):
        deployment_errors = deployment_evidence_errors(payload.get("deployment_impact", {}), evidence, findings)
        if deployment_errors:
            raise WorkflowError(
                "Branch Review Gate pass needs deployment impact evidence.",
                exit_code=2,
                payload={"errors": deployment_errors, "deployment_impact": payload.get("deployment_impact", {})},
            )
    path = configured_review_gate_path(task_dir, config)
    if not args.dry_run:
        write_json(path, payload)
    payload["artifact_path"] = str(path)
    payload["dry_run"] = bool(args.dry_run)
    return payload


def cmd_record_planning_approval(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    handoff = load_handoff(root, config)
    task_dir = resolve_task_dir(root, args.task, handoff)
    reviewer = str(args.reviewer or "").strip()
    summary = str(args.summary or "").strip()
    confirmation = str(args.user_confirmation or "").strip()
    if not reviewer:
        raise WorkflowError("record-planning-approval requires --reviewer identity metadata.", exit_code=2)
    if not summary:
        raise WorkflowError("record-planning-approval requires --summary with the planning review conclusion.", exit_code=2)
    if not confirmation:
        raise WorkflowError("record-planning-approval requires --user-confirmation evidence.", exit_code=2)
    payload = build_planning_approval_payload(
        root=root,
        task_dir=task_dir,
        reviewer=reviewer,
        approval_summary=summary,
        user_confirmation=confirmation,
        artifacts=list(args.artifact or []),
    )
    path = planning_approval_path(task_dir)
    if not args.dry_run:
        write_json(path, payload)
    payload["artifact_path"] = str(path)
    payload["dry_run"] = bool(args.dry_run)
    return payload


def cmd_check_planning_approval(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    handoff = load_handoff(root, config)
    task_dir = resolve_task_dir(root, args.task, handoff)
    path, payload, errors = validate_planning_approval(
        root,
        task_dir,
        allow_committed_head=bool(getattr(args, "allow_committed_head", False)),
    )
    if errors:
        raise WorkflowError(
            "Planning approval is missing or stale.",
            exit_code=2,
            payload={"artifact_path": str(path), "errors": errors},
        )
    return {
        "status": "ok",
        "artifact_path": str(path),
        "task_dir": str(task_dir),
        "head": current_head(root),
        "approved_head": payload.get("head"),
    }


def cmd_record_phase2_check(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    handoff = load_handoff(root, config)
    task_dir = resolve_task_dir(root, args.task, handoff)
    task = task_json(task_dir)
    checker = str(args.checker or "").strip()
    summary = str(args.summary or "").strip()
    if not checker:
        raise WorkflowError("record-phase2-check requires --checker identity metadata.", exit_code=2)
    if not summary:
        raise WorkflowError("record-phase2-check requires --summary with the trellis-check conclusion.", exit_code=2)
    findings = load_findings(args)
    payload = build_phase2_check_payload(
        root=root,
        task_dir=task_dir,
        handoff=handoff,
        task=task,
        checker=checker,
        check_summary=summary,
        checked_artifacts=list(args.checked_artifact or []),
        checked_specs=list(args.checked_spec or []),
        coverage_items=list(args.coverage or []),
        validation_items=list(args.validation or []),
        findings=findings,
    )
    blockers = unresolved_blocking_findings(findings)
    if args.pass_check and blockers:
        raise WorkflowError("--pass cannot be used while unresolved P0/P1/P2 findings are present.", exit_code=2)
    if args.pass_check and any(value is not True for value in payload["coverage"].values()):
        missing = [key for key, value in payload["coverage"].items() if value is not True]
        raise WorkflowError(
            "record-phase2-check --pass requires every coverage key to be explicitly checked.",
            exit_code=2,
            payload={"missing_coverage": missing},
        )
    if args.pass_check and not payload["validation_commands"]:
        raise WorkflowError("record-phase2-check --pass requires at least one --validation evidence line.", exit_code=2)
    path = phase2_check_path(task_dir)
    if not args.dry_run:
        write_json(path, payload)
    payload["artifact_path"] = str(path)
    payload["dry_run"] = bool(args.dry_run)
    return payload


def cmd_check_phase2_check(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    handoff = load_handoff(root, config)
    task_dir = resolve_task_dir(root, args.task, handoff)
    path, payload, errors = validate_phase2_check(root, task_dir)
    if errors:
        raise WorkflowError(
            "Phase 2 check report is missing, stale, or incomplete.",
            exit_code=2,
            payload={"artifact_path": str(path), "errors": errors},
        )
    return {
        "status": "ok",
        "artifact_path": str(path),
        "task_dir": str(task_dir),
        "head": current_head(root),
        "checked_head": payload.get("head"),
    }


def cmd_check_review_gate(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    handoff = load_handoff(root, config)
    task_dir = resolve_task_dir(root, args.task, handoff)
    path, gate, errors = validate_review_gate(root, task_dir, config, args.allow_metadata_after_gate)
    if errors:
        raise WorkflowError(
            "Branch Review Gate has not passed for the current HEAD.",
            exit_code=2,
            payload={"artifact_path": str(path), "errors": errors},
        )
    return {
        "status": "ok",
        "artifact_path": str(path),
        "task_dir": str(task_dir),
        "head": current_head(root),
        "reviewed_head": gate.get("head"),
    }


def cmd_publish_pr(args: argparse.Namespace) -> dict[str, Any]:
    validate_publish_invocation(args)
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    publish = publish_config(config)
    handoff = load_handoff(root, config)
    task_dir = resolve_task_dir(root, args.task, handoff)
    task = task_json(task_dir)
    base_branch = base_branch_from_sources(args, task, handoff)
    repo = str(args.repo or config.get("github_repo") or "").strip() or infer_github_repo(root)
    if not repo:
        raise WorkflowError("Could not resolve GitHub repo. Configure github_repo or pass --repo owner/repo.")

    dirty, dirty_paths = has_non_metadata_dirty_paths(root)
    if dirty:
        raise WorkflowError(
            "Working tree has uncommitted non-metadata changes. Commit task work before publish.",
            exit_code=2,
            payload={"dirty_paths": dirty_paths},
        )

    gate_path, gate, gate_errors = validate_review_gate(root, task_dir, config, args.allow_metadata_after_gate)
    if gate_errors:
        raise WorkflowError(
            "Publish blocked because Branch Review Gate is not valid for the current HEAD.",
            exit_code=2,
            payload={"artifact_path": str(gate_path), "errors": gate_errors},
        )

    ledger = load_issue_scope_ledger(task_dir, handoff)
    ledger_errors = validate_ledger_for_publish(ledger, gate)
    if ledger_errors:
        raise WorkflowError(
            "Publish blocked because Issue Scope Ledger is incomplete.",
            exit_code=2,
            payload={"ledger_path": str(issue_scope_ledger_path(task_dir)), "errors": ledger_errors},
        )

    branch = current_branch(root)
    remote = str(args.remote or publish.get("remote") or "origin")
    draft = bool(args.draft) if args.draft is not None else bool(publish.get("draft", False))
    title = pr_title_from_task(task, args)
    validations = list(args.validation or [])
    body, body_source = resolve_pr_body(root, args, ledger, gate, validations, config)
    body_errors = validate_pr_body_quality(body, ledger, draft)
    reviewed_source_errors = validate_reviewed_body_source_for_publish(body_source, draft)
    if body_errors:
        raise WorkflowError(
            "Publish blocked because PR body is not reviewer-readable.",
            exit_code=2,
            payload={"errors": body_errors, "body_source": body_source},
        )
    if reviewed_source_errors and not args.dry_run:
        raise WorkflowError(
            "Publish blocked because non-draft PR body lacks reviewed source evidence.",
            exit_code=2,
            payload={
                "errors": reviewed_source_errors,
                "body_source": body_source,
                "reviewed_source_required": True,
                "reviewed_source_ok": False,
            },
        )

    payload: dict[str, Any] = {
        "status": "dry-run" if args.dry_run else "ok",
        "repo": repo,
        "base_branch": normalize_ref(base_branch).removeprefix("origin/"),
        "head_branch": branch,
        "remote": remote,
        "draft": draft,
        "title": title,
        "body": body,
        "body_source": body_source,
        "reviewed_source_required": not draft,
        "reviewed_source_ok": not reviewed_source_errors,
        "reviewed_source_errors": reviewed_source_errors,
        "review_gate": str(gate_path),
        "issue_scope_ledger": str(issue_scope_ledger_path(task_dir)),
    }
    if args.dry_run:
        return payload

    require_gh_auth(root)
    run_stdout(["git", "push", "-u", remote, branch], cwd=root)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        tmp.write(body)
        body_file = tmp.name
    try:
        cmd = [
            "pr",
            "create",
            "--repo",
            repo,
            "--base",
            payload["base_branch"],
            "--head",
            branch,
            "--title",
            title,
            "--body-file",
            body_file,
        ]
        if draft:
            cmd.append("--draft")
        proc = run(["gh", *cmd], cwd=root, check=False)
        if proc.returncode != 0:
            raise WorkflowError(f"gh pr create failed:\n{proc.stderr.strip()}")
        payload["pr_url"] = proc.stdout.strip()
    finally:
        Path(body_file).unlink(missing_ok=True)
    return payload


def build_finish_work_dry_run_plan(
    root: Path,
    args: argparse.Namespace,
    config: dict[str, Any],
    handoff: dict[str, Any],
    task_dir: Path,
    task_name: str,
    gate_path: Path,
    gate: dict[str, Any],
    reviewed_head: str,
    title: str,
    summary: str,
    commits: str,
    draft: bool,
    body_source: str,
    body_errors: list[str],
    reviewed_source_errors: list[str],
) -> dict[str, Any]:
    publish = publish_config(config)
    task = task_json(task_dir)
    base_branch = base_branch_from_sources(args, task, handoff)
    repo = str(args.repo or config.get("github_repo") or "").strip() or infer_github_repo(root)
    remote = str(args.remote or publish.get("remote") or "origin")
    head_branch = current_branch(root)
    pr_title = pr_title_from_task(task, args)
    archive_would_run = not args.skip_archive
    journal_would_run = not args.skip_journal
    return {
        "status": "dry-run",
        "task_dir": str(task_dir),
        "task_name": task_name,
        "review_gate": str(gate_path),
        "reviewed_head": reviewed_head,
        "dry_run_side_effects": False,
        "checks": {
            "non_metadata_dirty_paths": [],
            "pr_readiness": {
                "body_source": body_source,
                "body_quality_ok": not body_errors,
                "body_quality_errors": body_errors,
                "reviewed_source_required": not draft,
                "reviewed_source_ok": not reviewed_source_errors,
                "reviewed_source_errors": reviewed_source_errors,
            },
        },
        "plan": {
            "archive": {
                "would_run": archive_would_run,
                "skip": bool(args.skip_archive),
                "task_name": task_name,
                "command": ["python3", "./.trellis/scripts/task.py", "archive", task_name],
            },
            "journal": {
                "would_run": journal_would_run,
                "skip": bool(args.skip_journal),
                "title": title,
                "summary": summary,
                "commits": commits or reviewed_head,
                "command": [
                    "python3",
                    "./.trellis/scripts/add_session.py",
                    "--title",
                    title,
                    "--commit",
                    commits or reviewed_head,
                    "--summary",
                    summary,
                ],
            },
            "metadata_commit": {
                "would_run": True,
                "message": "chore(trellis): finalize task metadata",
            },
            "publish": {
                "would_run": True,
                "repo": repo,
                "base_branch": normalize_ref(base_branch).removeprefix("origin/"),
                "head_branch": head_branch,
                "remote": remote,
                "draft": draft,
                "title": pr_title,
                "body_source": body_source,
                "allow_metadata_after_gate": True,
                "from_finish_work": True,
            },
        },
    }


def cmd_finish_work(args: argparse.Namespace) -> dict[str, Any]:
    validate_finish_work_invocation(args)
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    handoff = load_handoff(root, config)
    task_dir = resolve_task_dir(root, args.task, handoff)
    gate_path, gate, gate_errors = validate_review_gate(root, task_dir, config, True)
    if gate_errors:
        raise WorkflowError(
            "finish-work blocked because Branch Review Gate is not valid for the current HEAD.",
            exit_code=2,
            payload={"artifact_path": str(gate_path), "errors": gate_errors},
        )

    dirty, dirty_paths = has_non_metadata_dirty_paths(root)
    if dirty:
        raise WorkflowError(
            "Working tree has uncommitted non-metadata changes. Commit task work before finish-work.",
            exit_code=2,
            payload={"dirty_paths": dirty_paths},
        )

    reviewed_head = str(gate.get("head") or current_head(root))
    task_name = args.task_name or task_dir.name
    title = args.journal_title or f"完成：{task_json(task_dir).get('title') or task_name}"
    summary = args.journal_summary or str(gate.get("conclusion", {}).get("summary") or "完成当前 Trellis task，并通过 Branch Review Gate。")
    commits = args.commit or ",".join(recent_work_commits(root, reviewed_head))
    draft = bool(args.draft) if args.draft is not None else bool(publish_config(config).get("draft", False))

    ledger = load_issue_scope_ledger(task_dir, handoff)
    validations = list(args.validation or [])
    body, body_source = resolve_pr_body(root, args, ledger, gate, validations, config)
    body_errors = validate_pr_body_quality(body, ledger, draft)
    reviewed_source_errors = validate_reviewed_body_source_for_publish(body_source, draft)
    readiness_errors = body_errors + reviewed_source_errors
    if readiness_errors:
        raise WorkflowError(
            "finish-work blocked because PR readiness evidence is incomplete.",
            exit_code=2,
            payload={
                "errors": readiness_errors,
                "body_source": body_source,
                "reviewed_source_required": not draft,
                "reviewed_source_ok": not reviewed_source_errors,
            },
        )

    if args.dry_run:
        return build_finish_work_dry_run_plan(
            root,
            args,
            config,
            handoff,
            task_dir,
            task_name,
            gate_path,
            gate,
            reviewed_head,
            title,
            summary,
            commits,
            draft,
            body_source,
            body_errors,
            reviewed_source_errors,
        )

    if not args.skip_archive:
        archive_script = root / ".trellis/scripts/task.py"
        if not archive_script.exists():
            raise WorkflowError(f"Trellis task.py not found: {archive_script}")
        proc = run(["python3", "./.trellis/scripts/task.py", "archive", task_name], cwd=root, check=False)
        if proc.returncode != 0:
            raise WorkflowError(f"task.py archive failed:\n{proc.stderr.strip()}", payload={"stdout": proc.stdout.strip()})

    if not args.skip_journal:
        journal_script = root / ".trellis/scripts/add_session.py"
        if not journal_script.exists():
            raise WorkflowError(f"Trellis add_session.py not found: {journal_script}")
        journal_cmd = [
            "python3",
            "./.trellis/scripts/add_session.py",
            "--title",
            title,
            "--commit",
            commits or reviewed_head,
            "--summary",
            summary,
        ]
        proc = run(journal_cmd, cwd=root, check=False)
        if proc.returncode != 0:
            raise WorkflowError(f"add_session.py failed:\n{proc.stderr.strip()}", payload={"stdout": proc.stdout.strip()})

    metadata_commit = commit_if_metadata_dirty(root, "chore(trellis): finalize task metadata")
    archived_task_dir = resolve_existing_task_dir(root, task_name)
    publish_task = str(archived_task_dir) if archived_task_dir else (args.task or str(task_dir))
    publish_body_file = args.body_file
    publish_body_artifact = args.body_artifact
    if archived_task_dir:
        publish_body_file = rewrite_active_task_artifact_path(root, task_dir, archived_task_dir, publish_body_file)
        publish_body_artifact = rewrite_active_task_artifact_path(root, task_dir, archived_task_dir, publish_body_artifact)
    publish_args = argparse.Namespace(
        root=str(root),
        task=publish_task,
        repo=args.repo,
        base_branch=args.base_branch,
        remote=args.remote,
        title=args.title,
        validation=args.validation,
        body_file=publish_body_file,
        body_artifact=publish_body_artifact,
        draft=args.draft,
        allow_metadata_after_gate=True,
        dry_run=args.dry_run,
        from_finish_work=True,
        recovery_after_finish_work=False,
    )
    publish_payload = cmd_publish_pr(publish_args)
    return {
        "status": "dry-run" if args.dry_run else "ok",
        "task_dir": str(task_dir),
        "task_name": task_name,
        "review_gate": str(gate_path),
        "reviewed_head": reviewed_head,
        "metadata_commit": metadata_commit,
        "publish": publish_payload,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guru Team Trellis workflow helpers")
    sub = parser.add_subparsers(dest="command", required=True)

    check_env = sub.add_parser("check-env")
    check_env.add_argument("--root")
    check_env.add_argument("--json", action="store_true")

    version = sub.add_parser("version")
    version.add_argument("--root")
    version.add_argument("--json", action="store_true")

    prepare = sub.add_parser("prepare")
    prepare.add_argument("--root")
    prepare.add_argument("--json", action="store_true")
    prepare.add_argument("--short-name")
    prepare.add_argument("--reuse-issue", type=int)
    prepare.add_argument("--force-new", action="store_true")
    prepare.add_argument("--create-issue-confirmed", action="store_true", help="Create a GitHub issue only after AI/human review confirmed the proposed title/body.")
    prepare.add_argument("--issue-title", help="Reviewed issue title used with --create-issue-confirmed.")
    prepare.add_argument("--issue-body-file", help="Path to reviewed issue body used with --create-issue-confirmed.")
    prepare.add_argument("--base-branch")
    prepare.add_argument("--branch")
    prepare.add_argument("--task-slug")
    prepare.add_argument("--workspace-slug")
    prepare.add_argument("--title")
    prepare.add_argument("--assignee")
    prepare.add_argument("--priority")
    prepare.add_argument("--description")
    prepare.add_argument("--worktree", action="store_true")
    prepare.add_argument("--create-worktree", action="store_true")
    prepare.add_argument("--create-task", action="store_true")
    prepare.add_argument("requirement", nargs="*")

    review = sub.add_parser("review-branch")
    review.add_argument("--root")
    review.add_argument("--json", action="store_true")
    review.add_argument("--task")
    review.add_argument("--base-branch")
    review.add_argument("--pass", dest="pass_gate", action="store_true")
    review.add_argument("--summary")
    review.add_argument("--evidence", action="append", help="Chinese review evidence line. Required with --pass.")
    review.add_argument("--reviewer", help="Reviewer name or AI/human review channel.")
    review.add_argument("--review-source", help="Review source metadata. Passing gate requires independent-agent.")
    review.add_argument("--review-report", help="Path to the prior AI/human review report recorded before gate artifact creation.")
    review.add_argument("--finding", action="append", help="Finding as PRIORITY|message[|path].")
    review.add_argument("--findings-file", help="JSON list or object with findings[].")
    review.add_argument("--dry-run", action="store_true")

    planning = sub.add_parser("record-planning-approval")
    planning.add_argument("--root")
    planning.add_argument("--json", action="store_true")
    planning.add_argument("--task")
    planning.add_argument("--reviewer", required=True, help="Reviewer name or AI/human review channel.")
    planning.add_argument("--summary", required=True, help="Chinese planning review conclusion.")
    planning.add_argument("--user-confirmation", required=True, help="Evidence summary for user approval to enter implementation.")
    planning.add_argument("--artifact", action="append", help="Task-local artifact path to approve. Defaults to existing prd/design/implement.")
    planning.add_argument("--dry-run", action="store_true")

    check_planning = sub.add_parser("check-planning-approval")
    check_planning.add_argument("--root")
    check_planning.add_argument("--json", action="store_true")
    check_planning.add_argument("--task")
    check_planning.add_argument("--allow-committed-head", action="store_true", help="Allow the approved planning HEAD to be an ancestor for post-commit gate audits.")

    phase2 = sub.add_parser("record-phase2-check")
    phase2.add_argument("--root")
    phase2.add_argument("--json", action="store_true")
    phase2.add_argument("--task")
    phase2.add_argument("--pass", dest="pass_check", action="store_true")
    phase2.add_argument("--checker", required=True, help="Checker name or AI/human check channel.")
    phase2.add_argument("--summary", required=True, help="Chinese trellis-check conclusion.")
    phase2.add_argument("--checked-artifact", action="append", help="Task-local artifact read by the check. Defaults to existing task planning/gate artifacts.")
    phase2.add_argument("--checked-spec", action="append", help="Repo-relative .trellis/spec file read by the check.")
    phase2.add_argument("--coverage", action="append", help="Coverage key. Required keys: requirements, design, code, tests, spec_sync, cross_layer, docs_ssot, deployment.")
    phase2.add_argument("--validation", action="append", help="Validation command evidence as COMMAND or COMMAND|RESULT.")
    phase2.add_argument("--finding", action="append", help="Finding as PRIORITY|message[|path]. Add status in findings-file for resolved blocking findings.")
    phase2.add_argument("--findings-file", help="JSON list or object with findings[].")
    phase2.add_argument("--dry-run", action="store_true")

    check_phase2 = sub.add_parser("check-phase2-check")
    check_phase2.add_argument("--root")
    check_phase2.add_argument("--json", action="store_true")
    check_phase2.add_argument("--task")

    check_gate = sub.add_parser("check-review-gate")
    check_gate.add_argument("--root")
    check_gate.add_argument("--json", action="store_true")
    check_gate.add_argument("--task")
    check_gate.add_argument("--allow-metadata-after-gate", action="store_true")

    publish = sub.add_parser("publish-pr")
    publish.add_argument("--root")
    publish.add_argument("--json", action="store_true")
    publish.add_argument("--task")
    publish.add_argument("--repo")
    publish.add_argument("--base-branch")
    publish.add_argument("--remote")
    publish.add_argument("--title")
    publish.add_argument("--validation", action="append", help="Chinese validation evidence line for PR body.")
    publish.add_argument("--body-file", help="AI-reviewed Markdown PR body. Preferred over generated fallback.")
    publish.add_argument("--body-artifact", help="AI-reviewed JSON readiness artifact containing body or body_file.")
    publish.add_argument("--draft", dest="draft", action="store_true", default=None)
    publish.add_argument("--no-draft", dest="draft", action="store_false")
    publish.add_argument("--allow-metadata-after-gate", action="store_true")
    publish.add_argument(
        "--recovery-after-finish-work",
        action="store_true",
        help="Explicit recovery/debug path for rerunning publish after finish-work already completed.",
    )
    publish.add_argument("--dry-run", action="store_true")

    finish = sub.add_parser("finish-work")
    finish.add_argument("--root")
    finish.add_argument("--json", action="store_true")
    finish.add_argument("--task")
    finish.add_argument("--task-name", help="Task directory/name for task.py archive. Defaults to resolved task dir name.")
    finish.add_argument("--repo")
    finish.add_argument("--base-branch")
    finish.add_argument("--remote")
    finish.add_argument("--title", help="Chinese PR title override.")
    finish.add_argument("--validation", action="append", help="Chinese validation evidence line for PR body.")
    finish.add_argument("--body-file", help="AI-reviewed Markdown PR body passed through to publish-pr.")
    finish.add_argument("--body-artifact", help="AI-reviewed JSON readiness artifact passed through to publish-pr.")
    finish.add_argument("--draft", dest="draft", action="store_true", default=None)
    finish.add_argument("--no-draft", dest="draft", action="store_false")
    finish.add_argument("--journal-title", help="Chinese session journal title.")
    finish.add_argument("--journal-summary", help="Chinese session journal summary.")
    finish.add_argument("--commit", help="Comma-separated work commit hashes for add_session.py.")
    finish.add_argument(
        "--from-trellis-finish-work",
        action="store_true",
        help="Required intent marker set by the explicit trellis-finish-work entrypoint.",
    )
    finish.add_argument("--skip-archive", action="store_true", help="Internal recovery switch. Do not use in normal finish-work.")
    finish.add_argument("--skip-journal", action="store_true", help="Internal recovery switch. Do not use in normal finish-work.")
    finish.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate finish-work readiness and print planned archive/journal/publish actions without writing files.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "check-env":
            payload = check_env_payload(Path(args.root or os.getcwd()))
        elif args.command == "version":
            payload = cmd_version(args)
        elif args.command == "prepare":
            payload = cmd_prepare(args)
        elif args.command == "review-branch":
            payload = cmd_review_branch(args)
        elif args.command == "record-planning-approval":
            payload = cmd_record_planning_approval(args)
        elif args.command == "check-planning-approval":
            payload = cmd_check_planning_approval(args)
        elif args.command == "record-phase2-check":
            payload = cmd_record_phase2_check(args)
        elif args.command == "check-phase2-check":
            payload = cmd_check_phase2_check(args)
        elif args.command == "check-review-gate":
            payload = cmd_check_review_gate(args)
        elif args.command == "publish-pr":
            payload = cmd_publish_pr(args)
        elif args.command == "finish-work":
            payload = cmd_finish_work(args)
        else:
            raise WorkflowError(f"Unsupported command: {args.command}")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    except WorkflowError as exc:
        payload = {"status": "error", "error": str(exc), **exc.payload}
        if getattr(args, "json", False):
            print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
            if exc.payload:
                print(json.dumps(exc.payload, ensure_ascii=False, indent=2), file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
