#!/usr/bin/env python3
"""Focused tests for Guru Team Trellis companion behavior."""

from __future__ import annotations

import argparse
import copy
import contextlib
import hashlib
import importlib.util
import inspect
import io
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
import sys
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import guru_team_trellis as gtt


def prepare_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "short_name": None,
        "reuse_issue": None,
        "force_new": False,
        "issue_title": None,
        "expected_resolution_sha256": "b" * 64,
        "base_branch": None,
        "branch": None,
        "task_slug": None,
        "workspace_slug": None,
        "title": None,
        "assignee": None,
        "priority": None,
        "description": None,
        "worktree": False,
        "requirement": ["Add default side-effect-free intake planning for freeform requests"],
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def fresh_base_sync_projection(
    sha: str = "a" * 40,
    *,
    resolution_sha256: str = "b" * 64,
    post_sync_resolution_sha256: str | None = None,
) -> dict[str, object]:
    post_digest = post_sync_resolution_sha256 or resolution_sha256
    post_resolution = {
        "schema_version": "1.0",
        "skill_id": "guru-sync-base",
        "status": "resolved",
        "source": "explicit",
        "selected_base": "main",
        "remote": "origin",
        "candidates": ["main"],
        "decision_checkout": {
            "branch": "main",
            "head": sha,
            "clean": True,
        },
    }
    return {
        "remote": "origin",
        "base_branch": "main",
        "base_ref": "main",
        "remote_ref": "origin/main",
        "local_head_before": sha,
        "local_head_after": sha,
        "remote_head": sha,
        "remote_head_source": "fetched",
        "fetch_attempted": True,
        "fetch_performed": True,
        "fast_forwarded": False,
        "fresh": True,
        "status": "fresh",
        "base_ref_for_worktree": "main",
        "resolution": {
            "source": "explicit",
            "selected_base": "main",
            "remote": "origin",
            "candidates": ["main"],
            "resolution_sha256": resolution_sha256,
        },
        "post_sync_resolution": post_resolution,
        "post_sync_resolution_sha256": post_digest,
        "reviewed_resolution_sha256": resolution_sha256,
        "decision_checkout": {
            "branch": "main",
            "head_before": sha,
            "head_after": sha,
            "clean_before": True,
            "clean_after": True,
        },
        "three_way_equal": True,
        "facts_sha256": "c" * 64,
    }


def fresh_base_sync_result(sha: str = "a" * 40) -> dict[str, object]:
    resolution = gtt.resolution_identity(
        source="explicit",
        selected_base="main",
        remote="origin",
        candidates=["main"],
        decision_branch="main",
        decision_head=sha,
        decision_clean=True,
    )
    resolution_sha256 = gtt.canonical_json_sha256(resolution)
    payload: dict[str, object] = {
        "schema_version": "1.0",
        "skill_id": "guru-sync-base",
        "status": "synced",
        "resolution": {
            "source": "explicit",
            "selected_base": "main",
            "remote": "origin",
            "candidates": ["main"],
            "resolution_sha256": resolution_sha256,
        },
        "post_sync_resolution": resolution,
        "post_sync_resolution_sha256": resolution_sha256,
        "decision_checkout": {
            "branch": "main",
            "head_before": sha,
            "head_after": sha,
            "clean_before": True,
            "clean_after": True,
        },
        "git": {
            "local_ref": "refs/heads/main",
            "remote_ref": "refs/remotes/origin/main",
            "local_head_before": sha,
            "local_head_after": sha,
            "remote_head_after": sha,
            "fetch_performed": True,
            "fast_forwarded": False,
        },
        "fresh": True,
    }
    payload["facts_sha256"] = gtt.canonical_json_sha256(payload)
    return payload


def finish_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "task_name": None,
        "repo": None,
        "base_branch": None,
        "remote": None,
        "title": None,
        "validation": [],
        "from_guru_finalizer": True,
        "dry_run": True,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def valid_pr_body(summary: str = "增加 PR 发布的 reviewed body source 门禁。") -> str:
    return f"""## 变更摘要

- {summary}

## 影响范围

- Guru Team publish helper
- finish-work PR 发布入口

## 验证结果

- python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py 通过

## Review Gate

- 结论：发布边界检查通过。
- branch_review_commit：`abc123`

## Docs SSOT

- 策略：ssot_first。
- durable docs：已更新 `trellis/workflows/guru-team/workflow.md`。
- task delta merge：任务 artifact delta 已 merge 到 durable docs。
- task history：调试过程仅保留为 task history。
- follow-up / limitation：无 follow-up 或当前 PR limitation。

## Issue 关闭范围

- Closes #18

## 安全说明

- 未涉及 secrets、runtime config 或部署资产。
"""


def closeout_head_repository_fields(
    repo: str = "owner/repo", *, cross_repository: bool = False
) -> dict[str, object]:
    owner, name = repo.split("/", 1)
    return {
        "headRepository": {"name": name, "nameWithOwner": repo},
        "headRepositoryOwner": {"login": owner},
        "isCrossRepository": cross_repository,
    }


def review_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "base_branch": None,
        "evidence": ["已覆盖 CI/CD、Docker、K8s、migration、Makefile 部署影响判断。"],
        "reviewer": "trellis-check-agent",
        "review_source": gtt.INDEPENDENT_REVIEW_SOURCE,
        "skill_input": None,
        "semantic_review_file": None,
        "typed_exit": "passed",
        "dry_run": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def planning_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "input": None,
        "require_exit": None,
        "dry_run": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def recovery_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "event": "unfinished",
        "logical_role": "实现代理",
        "agent_id": "agent-original",
        "reason": "The implementation agent ended before completing its scope.",
        "handoff_summary": "Preserve completed work and the exact remaining implementation scope.",
        "predecessor_event_id": None,
        "dry_run": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def boundary_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "allow_source_clean": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def resolve_human_artifacts_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class GitHubCliAdapterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path("/tmp/repo")

    def completed(self, code: int, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(["gh"], code, stdout, stderr)

    def test_high_level_and_api_operations_require_explicit_matching_repo(self) -> None:
        self.assertEqual(
            gtt.github_repo_binding(["issue", "view", "1", "--repo", "Owner/Repo"]),
            "owner/repo",
        )
        self.assertEqual(
            gtt.github_repo_binding(["api", "repos/Owner/Repo/issues/1"]),
            "owner/repo",
        )
        self.assertEqual(gtt.github_repo_binding(["issue", "view", "1"]), "")
        self.assertEqual(
            gtt.github_repo_binding(["issue", "view", "1"], "owner/repo"),
            "",
        )
        self.assertEqual(
            gtt.github_repo_binding(["api", "user"], "owner/repo"),
            "",
        )
        self.assertEqual(
            gtt.github_repo_binding(["pr", "view", "1", "--repo", "owner/other"], "owner/repo"),
            "",
        )

    def test_missing_cli_and_auth_are_distinct(self) -> None:
        with mock.patch.object(gtt.shutil, "which", return_value=None):
            with self.assertRaises(gtt.WorkflowError) as missing:
                gtt.require_gh_auth(self.root)
        self.assertEqual(missing.exception.payload["error_code"], "github_cli_missing")
        with (
            mock.patch.object(gtt.shutil, "which", return_value="/usr/bin/gh"),
            mock.patch.object(gtt, "run", return_value=self.completed(1, stderr="not logged in")),
            self.assertRaises(gtt.WorkflowError) as auth,
        ):
            gtt.require_gh_auth(self.root)
        self.assertEqual(auth.exception.payload["error_code"], "github_auth_failed")

    def test_process_failure_taxonomy_is_precise(self) -> None:
        cases = [
            ("repo_access", "HTTP 404: Not Found", "github_repo_access_denied"),
            (
                "issue_read",
                "GraphQL: Could not resolve to a Repository with the name 'owner/repo'.",
                "github_repo_access_denied",
            ),
            (
                "issue_edit",
                "GraphQL: Could not resolve to a Repository with the name 'owner/repo'.",
                "github_repo_access_denied",
            ),
            ("issue_edit", "HTTP 403: Resource not accessible by integration", "github_permission_denied"),
            ("pr_read", "HTTP 503: service unavailable", "github_api_unavailable"),
            ("pr_read", "HTTP 401: Bad credentials", "github_auth_failed"),
        ]
        for operation, stderr, expected in cases:
            with self.subTest(expected=expected):
                error = gtt.github_error_from_process(
                    self.completed(1, stderr=stderr), operation=operation, repo="owner/repo"
                )
                self.assertEqual(error.payload["error_code"], expected)
                self.assertEqual(error.payload["stderr_classification"], expected.removeprefix("github_"))
                self.assertNotIn("stderr", error.payload)

    def test_empty_invalid_and_missing_field_responses_fail_incomplete(self) -> None:
        for stdout in ("", "{", '{"number": 1}'):
            with (
                self.subTest(stdout=stdout),
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run", return_value=self.completed(0, stdout=stdout)),
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.gh_json(
                    ["issue", "view", "1", "--repo", "owner/repo"],
                    self.root,
                    required_fields=("number", "url"),
                    operation="issue_read",
                )
            self.assertEqual(raised.exception.payload["error_code"], "github_response_incomplete")

    def test_repo_access_preflight_binds_full_endpoint_and_identity(self) -> None:
        payload = '{"full_name":"owner/repo","url":"https://api.github.com/repos/owner/repo"}'
        with (
            mock.patch.object(gtt, "require_gh_auth"),
            mock.patch.object(gtt, "run", return_value=self.completed(0, stdout=payload)) as runner,
        ):
            result = gtt.require_github_repo_access(self.root, "Owner/Repo")
        self.assertEqual(result["full_name"], "owner/repo")
        self.assertEqual(runner.call_args.args[0], ["gh", "api", "repos/owner/repo"])

    def test_authenticated_login_reads_the_supported_hosts_shape(self) -> None:
        payload = json.dumps({
            "hosts": {
                "github.com": [{
                    "state": "success",
                    "active": True,
                    "host": "github.com",
                    "login": "current-user",
                }]
            }
        })
        with (
            mock.patch.object(gtt, "require_github_repo_access"),
            mock.patch.object(gtt, "run", return_value=self.completed(0, stdout=payload)) as runner,
        ):
            self.assertEqual(
                gtt.github_authenticated_login(self.root, "owner/repo"),
                "current-user",
            )
        self.assertEqual(
            runner.call_args.args[0],
            [
                "gh", "auth", "status", "--active", "--hostname", "github.com",
                "--json", "hosts",
            ],
        )

        incomplete = json.dumps({"hosts": {"github.com": []}})
        with (
            mock.patch.object(gtt, "require_github_repo_access"),
            mock.patch.object(gtt, "run", return_value=self.completed(0, stdout=incomplete)),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.github_authenticated_login(self.root, "owner/repo")
        self.assertEqual(
            raised.exception.payload["error_code"],
            "github_response_incomplete",
        )

    def test_duplicate_search_rejects_incomplete_issue_rows(self) -> None:
        incomplete = {
            "title": "Incomplete issue",
            "body": "body",
            "url": "https://github.com/owner/repo/issues/1",
            "labels": [],
            "updatedAt": "2026-08-09T00:00:00Z",
        }
        with mock.patch.object(gtt, "gh_json", return_value=[incomplete]) as gh_json:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.duplicate_search("owner/repo", "requirement", self.root, 5)
        self.assertEqual(
            raised.exception.payload["error_code"],
            "github_response_incomplete",
        )
        self.assertEqual(
            gh_json.call_args.kwargs["required_fields"],
            ("number", "title", "body", "url", "labels", "updatedAt"),
        )

    def test_check_env_exposes_stable_cli_and_auth_error_codes(self) -> None:
        common = {
            "repo_root": mock.patch.object(gtt, "repo_root", return_value=self.root),
            "config": mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            "branch": mock.patch.object(gtt, "current_branch", return_value="main"),
            "base": mock.patch.object(gtt, "resolve_base_branch", return_value=("main", ["main"])),
            "dirty": mock.patch.object(gtt, "git_dirty", return_value=False),
            "worktree_root": mock.patch.object(gtt, "configured_worktree_root", return_value=self.root / "worktrees"),
            "worktrees": mock.patch.object(gtt, "worktree_lines", return_value=[]),
        }
        with contextlib.ExitStack() as stack:
            for patcher in common.values():
                stack.enter_context(patcher)
            stack.enter_context(mock.patch.object(gtt.shutil, "which", return_value=None))
            missing = gtt.check_env_payload(self.root)
        self.assertEqual(missing["github_error"]["error_code"], "github_cli_missing")

        with contextlib.ExitStack() as stack:
            for patcher in common.values():
                stack.enter_context(patcher)
            stack.enter_context(mock.patch.object(gtt.shutil, "which", return_value="/usr/bin/gh"))
            stack.enter_context(mock.patch.object(gtt, "run", return_value=self.completed(1)))
            auth = gtt.check_env_payload(self.root)
        self.assertEqual(auth["github_error"]["error_code"], "github_auth_failed")

    def test_current_surfaces_declare_cli_only_matrix_and_git_transport(self) -> None:
        repo = Path(__file__).resolve().parents[5]
        documents = [
            repo / ".trellis/spec/workflow/workflow-contract.md",
            repo / ".trellis/spec/workflow/companion-scripts.md",
            repo / ".trellis/spec/workflow/skill-package-contract.md",
            repo / "trellis/workflows/guru-team/README.md",
            repo / "trellis/presets/guru-team/README.md",
        ]
        content = "\n".join(path.read_text(encoding="utf-8") for path in documents)
        for operation in (
            "Issue/PR create/read/edit/comment/labels/state",
            "checks",
            "reviews",
            "mergeability",
            "Draft/Ready",
            "merge",
            "workflow run/check",
            "post-merge",
        ):
            self.assertIn(operation, content)
        self.assertIn("`git` remains the sole owner", content)
        self.assertNotIn("existing connector", content.casefold())

    def test_issue_comment_index_incomplete_shapes_use_stable_error(self) -> None:
        invalid_payloads = [
            {},
            [["not-an-object"]],
            [[{"id": 1, "node_id": "", "html_url": "https://github.com/owner/repo/issues/1#issuecomment-1"}]],
            [[
                {"id": 1, "node_id": "IC_one", "html_url": "https://github.com/owner/repo/issues/1#issuecomment-1"},
                {"id": 1, "node_id": "IC_two", "html_url": "https://github.com/owner/repo/issues/1#issuecomment-2"},
            ]],
        ]
        for payload in invalid_payloads:
            with (
                self.subTest(payload=payload),
                mock.patch.object(gtt, "gh_json", return_value=payload),
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.contract_wording_live_issue_comment_index(
                    self.root, "owner/repo", 1
                )
            self.assertEqual(
                raised.exception.payload["error_code"],
                "github_response_incomplete",
            )
            self.assertEqual(
                raised.exception.payload["operation"],
                "issue_comments_read",
            )
            self.assertEqual(raised.exception.payload["repo"], "owner/repo")

    def test_selected_issue_comment_incomplete_fields_use_stable_error(self) -> None:
        source = {
            "kind": "issue",
            "repo": "owner/repo",
            "number": 1,
            "selected_comments": [
                {"id": "IC_one", "selection_reason": "Defines required behavior."}
            ],
        }
        live_issue = {
            "title": "Issue title",
            "body": "Issue body",
            "updatedAt": "2026-08-09T00:00:00Z",
            "url": "https://github.com/owner/repo/issues/1",
        }
        complete_comment = {
            "id": 1,
            "node_id": "IC_one",
            "html_url": "https://github.com/owner/repo/issues/1#issuecomment-1",
            "user": {"login": "reviewer"},
            "updated_at": "2026-08-09T00:01:00Z",
            "body": "Selected comment body",
        }
        cases = []
        for field in ("user", "updated_at", "body"):
            comment = copy.deepcopy(complete_comment)
            comment[field] = None
            cases.append((field, live_issue, comment, "issue_comments_read"))
        invalid_timestamp = copy.deepcopy(complete_comment)
        invalid_timestamp["updated_at"] = "not-a-timestamp"
        cases.append(("invalid_comment_timestamp", live_issue, invalid_timestamp, "issue_comments_read"))
        for value in (None, "not-a-timestamp"):
            issue = {**live_issue, "updatedAt": value}
            cases.append((f"issue_updated_at_{value}", issue, complete_comment, "issue_read"))

        for label, issue, comment, operation in cases:
            with (
                self.subTest(label=label),
                mock.patch.object(gtt, "contract_wording_read_input", return_value=source),
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "issue_view", return_value=issue),
                mock.patch.object(
                    gtt,
                    "contract_wording_live_issue_comment_index",
                    return_value={"IC_one": comment},
                ),
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.contract_wording_change_request_scope(self.root, None)
            self.assertEqual(
                raised.exception.payload["error_code"],
                "github_response_incomplete",
            )
            self.assertEqual(raised.exception.payload["operation"], operation)
            self.assertEqual(raised.exception.payload["repo"], "owner/repo")

    def test_create_mutation_incomplete_urls_use_stable_error(self) -> None:
        invalid_urls = (
            "",
            "not-a-url",
            "https://github.com/owner/other/issues/12",
        )
        for url in invalid_urls:
            with (
                self.subTest(operation="issue_create", url=url),
                mock.patch.object(
                    gtt,
                    "run_gh_command",
                    return_value=self.completed(0, stdout=url),
                ),
                mock.patch.object(gtt, "issue_view") as issue_view,
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.create_issue("owner/repo", "Title", "Body", self.root, [])
            self.assertEqual(
                raised.exception.payload["error_code"],
                "github_response_incomplete",
            )
            self.assertEqual(raised.exception.payload["operation"], "issue_create")
            self.assertEqual(raised.exception.payload["repo"], "owner/repo")
            issue_view.assert_not_called()

        for url in ("", "not-a-url", "https://github.com/owner/other/pull/12"):
            with (
                self.subTest(operation="pull_request_create", url=url),
                mock.patch.object(
                    gtt,
                    "run_gh_command",
                    return_value=self.completed(0, stdout=url),
                ),
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.create_pull_request(
                    self.root,
                    "owner/repo",
                    "main",
                    "codex/181-fix",
                    "Title",
                    "Body",
                    True,
                )
            self.assertEqual(
                raised.exception.payload["error_code"],
                "github_response_incomplete",
            )
            self.assertEqual(
                raised.exception.payload["operation"],
                "pull_request_create",
            )
            self.assertEqual(raised.exception.payload["repo"], "owner/repo")


class ConventionalCommitContractTest(unittest.TestCase):
    def test_merge_command_requires_explicit_repo_binding(self) -> None:
        expected_head = "a" * 40
        payload = gtt.build_merge_commit_payload(
            repo="Owner/Repo",
            primary_issue=181,
            summary="统一 GitHub 操作通道",
            head_branch="codex/181-gh-cli-only-github-operations",
            base_branch="main",
            expected_head=expected_head,
            pull_request=200,
        )
        self.assertEqual(payload["errors"], [])
        self.assertEqual(payload["expected_head"], expected_head)
        self.assertEqual(
            payload["command"][payload["command"].index("--repo") + 1],
            "owner/repo",
        )
        self.assertEqual(
            payload["command"][payload["command"].index("--match-head-commit") + 1],
            expected_head,
        )
        unbound = gtt.build_merge_commit_payload(
            repo="",
            primary_issue=181,
            summary="统一 GitHub 操作通道",
            head_branch="codex/181-gh-cli-only-github-operations",
            base_branch="main",
            expected_head="",
            pull_request=200,
        )
        self.assertTrue(unbound["errors"])

    def test_issue_92_rejects_invalid_commit_subjects(self) -> None:
        invalid_subjects = [
            "Merge pull request #91 from castbox/codex/073-trellis-doc-markdown-links",
            "完成：#73 将项目里的 trellis 官方文档链接的 html 地址替换为 markdown 格式的地址 (#91)",
            "#73 docs(agents): 将 Trellis 官方文档链接改为 Markdown 端点",
            "docs(#73): 将 Trellis 官方文档链接改为 Markdown 端点",
            "docs(agents): 合并 Trellis 官方文档链接 Markdown 化",
            "Update Guru Team extension public API metadata",
        ]

        for subject in invalid_subjects:
            with self.subTest(subject=subject):
                self.assertTrue(gtt.validate_commit_subject(subject, primary_issue=73))

    def test_issue_92_accepts_valid_commit_subjects(self) -> None:
        valid_subjects = [
            "docs(agents): #73 将 Trellis 官方文档链接改为 Markdown 端点",
            "chore(trellis): #73 归档任务元数据",
            "chore(merge): #91 合并 #73 Trellis 官方文档链接 Markdown 化",
        ]

        for subject in valid_subjects:
            with self.subTest(subject=subject):
                self.assertEqual([], gtt.validate_commit_subject(subject, primary_issue=73))

    def test_issue_92_rejects_close_keywords_in_commit_subjects(self) -> None:
        close_keywords = ["Closes", "Fixes", "Resolves", "Close", "Fix", "Resolve"]


        invalid_subjects = [
            f"docs(workflow): #92 {keyword} #92 提交规范"
            for keyword in close_keywords
        ] + [
            f"chore(merge): #91 合并 #92 {keyword} #92 提交规范"
            for keyword in close_keywords
        ]

        for subject in invalid_subjects:
            with self.subTest(subject=subject):
                self.assertTrue(gtt.validate_commit_subject(subject, primary_issue=92))

        self.assertEqual([], gtt.validate_commit_subject("docs(workflow): #92 提交规范保持 Refs 分工", primary_issue=92))

    def test_work_commit_body_requires_fixed_sections_refs_and_no_closes(self) -> None:
        body = """背景：
issue #92 要求统一提交规范。

变更：
- 增加 subject/body 校验。

边界：
不自动执行 GitHub PR merge。

验证：
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`

Refs #92
"""

        self.assertEqual([], gtt.validate_work_commit_body(body, primary_issue=92))
        self.assertTrue(gtt.validate_work_commit_body(body.replace("Refs #92", "Closes #92"), primary_issue=92))
        self.assertTrue(gtt.validate_work_commit_body(body.replace("边界：", "验证：", 1), primary_issue=92))

    def test_metadata_commit_body_must_be_empty(self) -> None:
        self.assertEqual([], gtt.validate_metadata_commit_body(""))
        self.assertTrue(gtt.validate_metadata_commit_body("记录归档动作。"))

    def test_merge_commit_body_requires_fixed_sections_pr_and_refs(self) -> None:
        body = gtt.format_merge_commit_body(
            91,
            73,
            "Trellis 官方文档链接 Markdown 化",
            "codex/073-trellis-doc-markdown-links",
            "main",
        )

        self.assertEqual([], gtt.validate_merge_commit_body(body, primary_issue=73, pull_request=91))
        self.assertTrue(gtt.validate_merge_commit_body(body.replace("PR: #91", "PR: #90"), primary_issue=73, pull_request=91))
        self.assertTrue(gtt.validate_merge_commit_body(body.replace("Refs #73", "Closes #73"), primary_issue=73, pull_request=91))


class ReviewedContentIdentityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "identity@example.invalid"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Identity Test"],
            cwd=self.root,
            check=True,
        )
        (self.root / ".gitignore").write_text(
            ".trellis/.runtime/\n.DS_Store\n",
            encoding="utf-8",
        )
        source = self.root / "src/value.txt"
        source.parent.mkdir(parents=True)
        source.write_text("one\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "initial"], cwd=self.root, check=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def commit_all(self, message: str) -> str:
        subprocess.run(["git", "add", "-A"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=self.root, check=True)
        return gtt.current_head(self.root)

    def identity(self, *, include_worktree: bool = True) -> str:
        result = gtt.reviewed_content_identity(
            self.root,
            include_worktree=include_worktree,
        )
        self.assertEqual(result["algorithm"], "guru-reviewed-content-1.0")
        return result["sha256"]

    def add_submodule_history(self) -> tuple[Path, str, str]:
        source_tmp = tempfile.TemporaryDirectory()
        self.addCleanup(source_tmp.cleanup)
        source = Path(source_tmp.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=source, check=True)
        subprocess.run(["git", "config", "user.name", "Gitlink Test"], cwd=source, check=True)
        subprocess.run(
            ["git", "config", "user.email", "gitlink@example.invalid"],
            cwd=source,
            check=True,
        )
        revisions: list[str] = []
        for label in ("A", "B"):
            (source / "dependency.txt").write_text(
                f"revision {label}\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "dependency.txt"], cwd=source, check=True)
            subprocess.run(
                ["git", "commit", "-q", "-m", f"revision {label}"],
                cwd=source,
                check=True,
            )
            revisions.append(gtt.current_head(source))
        subprocess.run(
            [
                "git",
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                "-q",
                str(source),
                "deps/dependency",
            ],
            cwd=self.root,
            check=True,
        )
        submodule = self.root / "deps/dependency"
        subprocess.run(
            ["git", "checkout", "-q", revisions[0]],
            cwd=submodule,
            check=True,
        )
        self.commit_all("add gitlink baseline")
        return submodule, revisions[0], revisions[1]

    def test_dirty_commit_and_metadata_descendant_share_one_identity(self) -> None:
        baseline = self.identity()
        (self.root / "src/value.txt").write_text("two\n", encoding="utf-8")
        dirty = self.identity()
        self.assertNotEqual(dirty, baseline)

        self.commit_all("change reviewed content")
        self.assertEqual(self.identity(), dirty)
        task_file = self.root / ".trellis/tasks/08-05-example/context-discovery.json"
        task_file.parent.mkdir(parents=True)
        task_file.write_text("publication metadata\n", encoding="utf-8")
        self.assertEqual(self.identity(), dirty)
        self.commit_all("record task metadata")
        self.assertEqual(self.identity(), dirty)

    def test_included_content_mode_path_and_delete_change_identity(self) -> None:
        baseline = self.identity()
        source = self.root / "src/value.txt"
        source.chmod(0o755)
        executable = self.identity()
        self.assertNotEqual(executable, baseline)

        source.rename(self.root / "src/renamed.txt")
        renamed = self.identity()
        self.assertNotEqual(renamed, executable)
        (self.root / "src/renamed.txt").unlink()
        deleted = self.identity()
        self.assertNotEqual(deleted, renamed)

        untracked = self.root / ".trellis/spec/reviewed.md"
        untracked.parent.mkdir(parents=True)
        untracked.write_text("durable contract\n", encoding="utf-8")
        self.assertNotEqual(self.identity(), deleted)

    def test_included_symlink_uses_link_bytes_and_matches_committed_identity(self) -> None:
        baseline = self.identity()
        link = self.root / "src/reviewed-link"
        link.symlink_to("target-a")
        dirty = self.identity()
        self.assertNotEqual(dirty, baseline)
        overlay = next(
            item
            for item in gtt.reviewed_content_worktree_overlays(self.root)
            if item["path"] == "src/reviewed-link"
        )
        self.assertEqual(overlay["mode"], "120000")
        self.assertEqual(
            overlay["oid"],
            gtt.reviewed_content_blob_oid(self.root, b"target-a"),
        )

        self.commit_all("add reviewed symlink")
        self.assertEqual(self.identity(), dirty)
        link.unlink()
        link.symlink_to("target-b")
        self.assertNotEqual(self.identity(), dirty)

    def test_gitlink_initialized_and_deinitialized_clean_share_stable_identity(self) -> None:
        submodule, revision_a, revision_b = self.add_submodule_history()
        baseline = self.identity()
        self.assertEqual(
            gtt.reviewed_content_tree_entries(self.root, "HEAD")["deps/dependency"],
            {
                "path": "deps/dependency",
                "mode": "160000",
                "oid": revision_a,
            },
        )

        subprocess.run(["git", "checkout", "-q", revision_b], cwd=submodule, check=True)
        dirty_candidate = self.identity()
        self.assertNotEqual(dirty_candidate, baseline)
        self.commit_all("advance reviewed gitlink")
        self.assertEqual(self.identity(), dirty_candidate)

        subprocess.run(
            ["git", "submodule", "deinit", "-f", "--", "deps/dependency"],
            cwd=self.root,
            check=True,
            stdout=subprocess.PIPE,
        )
        self.assertEqual(
            subprocess.run(
                ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
                cwd=self.root,
                check=True,
                stdout=subprocess.PIPE,
            ).stdout,
            b"",
        )
        self.assertEqual(self.identity(), dirty_candidate)
        self.assertEqual(self.identity(), dirty_candidate)

    def test_gitlink_initialized_dirty_fails_closed(self) -> None:
        submodule, _, _ = self.add_submodule_history()

        (submodule / "dependency.txt").write_text("dirty\n", encoding="utf-8")
        with self.assertRaisesRegex(
            gtt.WorkflowError,
            "gitlink worktree must be clean",
        ):
            self.identity()

    def test_gitlink_head_drift_after_overlay_capture_fails_closed(self) -> None:
        submodule, _, revision_b = self.add_submodule_history()
        subprocess.run(["git", "checkout", "-q", revision_b], cwd=submodule, check=True)
        original = gtt.task_commit_gitlink_worktree_identity
        calls = 0

        def drift_after_capture(root: Path, path: str) -> dict[str, object]:
            nonlocal calls
            calls += 1
            identity = original(root, path)
            if calls == 2:
                return {**identity, "gitlink_head": "f" * 40}
            return identity

        with mock.patch.object(
            gtt,
            "task_commit_gitlink_worktree_identity",
            side_effect=drift_after_capture,
        ):
            with self.assertRaisesRegex(gtt.WorkflowError, "HEAD drifted after capture"):
                self.identity()
        self.assertEqual(calls, 2)

    def test_gitlink_pointer_drift_after_overlay_capture_fails_closed(self) -> None:
        submodule, revision_a, revision_b = self.add_submodule_history()
        subprocess.run(["git", "checkout", "-q", revision_b], cwd=submodule, check=True)
        original = gtt.reviewed_content_worktree_overlays

        def drift_index_after_capture(root: Path) -> list[dict[str, object]]:
            overlays = original(root)
            subprocess.run(
                [
                    "git",
                    "update-index",
                    "--cacheinfo",
                    "160000",
                    revision_b,
                    "deps/dependency",
                ],
                cwd=root,
                check=True,
            )
            return overlays

        self.assertEqual(
            gtt.task_commit_index_identity(self.root, "deps/dependency"),
            (revision_a, "160000"),
        )
        with mock.patch.object(
            gtt,
            "reviewed_content_worktree_overlays",
            side_effect=drift_index_after_capture,
        ):
            with self.assertRaisesRegex(gtt.WorkflowError, "index binding drifted"):
                self.identity()

    def test_gitlink_deletion_replacement_and_nonempty_root_mismatch_fail_closed(self) -> None:
        submodule, _, _ = self.add_submodule_history()
        subprocess.run(
            ["git", "submodule", "deinit", "-f", "--", "deps/dependency"],
            cwd=self.root,
            check=True,
            stdout=subprocess.PIPE,
        )
        (submodule / "unexpected.txt").write_text("not a submodule\n", encoding="utf-8")
        with self.assertRaisesRegex(
            gtt.WorkflowError,
            "gitlink worktree is uninitialized or root-mismatched",
        ):
            self.identity()

        original_resolve = Path.resolve

        def ambiguous_resolve(path: Path, strict: bool = False) -> Path:
            if path == submodule:
                raise RuntimeError("ambiguous gitlink root")
            return original_resolve(path, strict=strict)

        with mock.patch.object(Path, "resolve", new=ambiguous_resolve):
            with self.assertRaisesRegex(gtt.WorkflowError, "root is ambiguous"):
                self.identity()

        (submodule / "unexpected.txt").unlink()
        submodule.rmdir()
        submodule.write_text("replacement\n", encoding="utf-8")
        with self.assertRaisesRegex(gtt.WorkflowError, "not an exact directory"):
            self.identity()

        submodule.unlink()
        with self.assertRaisesRegex(gtt.WorkflowError, "deletion or replacement"):
            self.identity()

    def test_metadata_classifier_uses_complete_repo_relative_prefixes(self) -> None:
        excluded = [
            ".trellis/tasks/x/task.json",
            ".trellis/workspace/dev/journal.md",
            ".trellis/.runtime/guru-team/state.json",
            "nested/.DS_Store",
        ]
        included = [
            ".trellis/taskset/readme.md",
            ".trellis/workspaces/readme.md",
            ".trellis/runtime/readme.md",
            ".trellis/workflow.md",
            ".trellis/spec/workflow/data-contracts.md",
        ]
        self.assertTrue(all(gtt.reviewed_content_metadata_path(path) for path in excluded))
        self.assertTrue(all(not gtt.reviewed_content_metadata_path(path) for path in included))

    def test_task_archive_symlink_state_does_not_enter_reviewed_identity(self) -> None:
        archived = self.root / ".trellis/tasks/archive/2026-08/example/finish-summary.json"
        archived.parent.mkdir(parents=True)
        archived.write_text("archived metadata\n", encoding="utf-8")
        self.commit_all("record archived task metadata")
        baseline = self.identity()

        archive_root = self.root / ".trellis/tasks/archive"
        backup = self.root / ".trellis/tasks/archive-backup"
        target = self.root / ".trellis/tasks/archive-target"
        target.mkdir(parents=True)
        (target / "sentinel.txt").write_text("metadata target\n", encoding="utf-8")
        archive_root.rename(backup)
        archive_root.symlink_to(target, target_is_directory=True)

        self.assertEqual(self.identity(), baseline)


class ProductionPublicInvocationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.task_rel = ".trellis/tasks/example-task"
        self.task_dir = self.root / self.task_rel
        self.task_dir.mkdir(parents=True)
        gtt.write_json(self.task_dir / "task.json", {
            "id": "example-task",
            "status": "in_progress",
        })
        self.packages = (
            Path(gtt.__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages"
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def invoke(
        self,
        skill_id: str,
        public_input: dict[str, object],
        owner_result: dict[str, object],
        checked: dict[str, object],
    ) -> dict[str, object]:
        artifact_name = (
            gtt.PLANNING_APPROVAL_ARTIFACT
            if skill_id == "guru-approve-task-plan"
            else gtt.PR_READINESS_ARTIFACT
            if skill_id == gtt.TASK_PUBLICATION_SKILL_ID
            else gtt.PHASE2_CHECK_ARTIFACT
        )
        owner_path = gtt.ai_first_owner_checkpoint_path(
            self.root,
            self.task_dir,
            artifact_name,
        )
        gtt.write_json(owner_path, owner_result)
        input_path = self.root / f"{skill_id}-input.json"
        gtt.write_json(input_path, public_input)
        checker_name = (
            "cmd_check_planning_approval"
            if skill_id == "guru-approve-task-plan"
            else "cmd_check_task_publication_review"
            if skill_id == gtt.TASK_PUBLICATION_SKILL_ID
            else "cmd_check_phase2_check"
        )
        with (
            mock.patch.object(
                gtt,
                "stage0_invocation_identity",
                return_value=(skill_id, self.packages / skill_id),
            ),
            mock.patch.object(gtt, "stage0_repo_root", return_value=self.root),
            mock.patch.object(gtt, checker_name, return_value=checked),
        ):
            output = gtt.cmd_invoke_stage0_skill(argparse.Namespace(
                input=input_path.relative_to(self.root).as_posix(),
                owner_result=owner_path.relative_to(self.root).as_posix(),
            ))
        if skill_id == "guru-check-task" and output.get("exit_id") == "passed":
            self.assertTrue(owner_path.is_file())
        else:
            self.assertFalse(owner_path.exists())
        return output

    def example_input(self, skill_id: str, name: str) -> dict[str, object]:
        return json.loads(
            (self.packages / skill_id / "examples" / name).read_text(encoding="utf-8")
        )

    def test_planning_public_routes_are_checker_derived_minimal_dtos(self) -> None:
        sha = "a" * 64
        cases = [
            (
                "approved",
                "public-initial-review-input.json",
                [],
                {
                    "exit_id": "approved", "task_ref": self.task_rel,
                },
            ),
            (
                "revision_required",
                "public-revision-reentry-input.json",
                [],
                {"exit_id": "revision_required", "task_ref": self.task_rel},
            ),
            (
                "clarify_scope",
                "public-clarification-reentry-input.json",
                ["scope-proposal:R13"],
                {
                    "exit_id": "clarify_scope", "task_ref": self.task_rel,
                    "proposal_refs": ["scope-proposal:R13"],
                },
            ),
            (
                "blocked",
                "public-initial-review-input.json",
                [],
                {"exit_id": "blocked"},
            ),
        ]
        for exit_id, example_name, proposals, expected in cases:
            with self.subTest(exit_id=exit_id):
                public_input = self.example_input("guru-approve-task-plan", example_name)
                public_input["task_ref"] = self.task_rel
                gate_status = "passed" if exit_id == "approved" else exit_id
                owner = {
                    "mode": public_input["mode"],
                    "typed_exit": exit_id,
                    "task_ref": self.task_rel,
                    "semantic_review": {
                        "status": gate_status,
                        "scope_proposals": proposals,
                    },
                }
                output = self.invoke(
                    "guru-approve-task-plan",
                    public_input,
                    owner,
                    {"status": "ok", "typed_exit": exit_id, "artifact_sha256": sha},
                )
                self.assertEqual(output, expected)

    def test_check_public_routes_are_checker_derived_minimal_dtos(self) -> None:
        sha = "b" * 64
        head = "c" * 40
        cases = [
            (
                "passed",
                "public-initial-check-input.json",
                None,
                [],
                {
                    "exit_id": "passed", "task_ref": self.task_rel,
                    "phase2_commit_anchor": head,
                },
            ),
            (
                "implementation_required",
                "public-finding-fix-rerun-input.json",
                None,
                [{"id": "F1", "status": "open"}],
                {
                    "exit_id": "implementation_required", "task_ref": self.task_rel,
                    "finding_refs": ["F1"],
                },
            ),
            (
                "planning_stale",
                "public-planning-reentry-input.json",
                "reapprove_plan",
                [],
                {
                    "exit_id": "planning_stale", "task_ref": self.task_rel,
                    "planning_route": "reapprove_plan",
                    "proposal_refs": ["scope-proposal:R13"],
                },
            ),
            (
                "blocked",
                "public-initial-check-input.json",
                None,
                [],
                {"exit_id": "blocked"},
            ),
        ]
        for exit_id, example_name, route, findings, expected in cases:
            with self.subTest(exit_id=exit_id):
                public_input = self.example_input("guru-check-task", example_name)
                public_input["task_ref"] = self.task_rel
                owner = {
                    "mode": public_input["mode"],
                    "typed_exit": exit_id,
                    "route": route,
                    "task_ref": self.task_rel,
                    "semantic_review": {
                        "findings": findings,
                        "status": exit_id,
                        "scope_decisions": ([{
                            "id": "scope-proposal:R13",
                            "disposition": "scope_change_required",
                            "finding_id": None,
                        }] if exit_id == "planning_stale" else []),
                    },
                }
                output = self.invoke(
                    "guru-check-task",
                    public_input,
                    owner,
                    {
                        "status": "ok", "typed_exit": exit_id,
                        "phase2_capture_commit": head, "artifact_sha256": sha,
                    },
                )
                self.assertEqual(output, expected)

    def test_production_owner_rejects_task_mismatch_and_stale_checker_exit(self) -> None:
        public_input = self.example_input(
            "guru-check-task", "public-initial-check-input.json",
        )
        public_input["task_ref"] = self.task_rel
        owner = {
            "mode": public_input["mode"],
            "typed_exit": "passed",
            "task_ref": ".trellis/tasks/other-task",
            "semantic_review": {"status": "passed"},
        }
        checked = {
            "status": "ok", "typed_exit": "passed",
            "phase2_capture_commit": "c" * 40, "artifact_sha256": "b" * 64,
        }
        with self.assertRaises(gtt.WorkflowError) as task_mismatch:
            self.invoke("guru-check-task", public_input, owner, checked)
        self.assertEqual(
            task_mismatch.exception.payload.get("code"),
            "owner_result_input_mismatch",
        )

        owner["task_ref"] = self.task_rel
        stale_checked = {**checked, "typed_exit": "implementation_required"}
        with self.assertRaises(gtt.WorkflowError) as stale_owner:
            self.invoke("guru-check-task", public_input, owner, stale_checked)
        self.assertEqual(
            stale_owner.exception.payload.get("code"),
            "owner_result_input_mismatch",
        )

    def test_publication_stale_wrapper_emits_current_minimal_ready_seed(self) -> None:
        public_input = self.example_input(
            gtt.TASK_PUBLICATION_SKILL_ID,
            "public-publication-review-stale-input.json",
        )
        public_input["task_ref"] = self.task_rel
        public_input["branch_review_commit"] = "c" * 40
        owner = json.loads(
            (
                self.packages
                / gtt.TASK_PUBLICATION_SKILL_ID
                / "examples/pr-readiness.json"
            ).read_text(encoding="utf-8")
        )
        owner["task_ref"] = self.task_rel
        owner["branch_review_commit"] = "c" * 40
        checked = {
            "status": "ok",
            "typed_exit": "ready",
            "branch_review_commit": "c" * 40,
            "owner_result": owner,
        }
        output = self.invoke(
            gtt.TASK_PUBLICATION_SKILL_ID,
            public_input,
            owner,
            checked,
        )
        self.assertEqual(output, {
            "exit_id": "ready",
            "task_ref": self.task_rel,
            "branch_review_commit": "c" * 40,
            "pr_title": owner["pr_payload"]["title"],
            "pr_body": owner["pr_payload"]["body"],
        })
        self.assertFalse(
            {"stale_reason", "reentry_context", "publication_ref"} & set(output)
        )

    def test_publication_stale_wrapper_rejects_owner_head_mismatch(self) -> None:
        public_input = self.example_input(
            gtt.TASK_PUBLICATION_SKILL_ID,
            "public-publication-review-stale-input.json",
        )
        public_input["task_ref"] = self.task_rel
        public_input["branch_review_commit"] = "d" * 40
        owner = json.loads(
            (
                self.packages
                / gtt.TASK_PUBLICATION_SKILL_ID
                / "examples/pr-readiness.json"
            ).read_text(encoding="utf-8")
        )
        owner["task_ref"] = self.task_rel
        owner["branch_review_commit"] = "c" * 40
        checked = {
            "status": "ok",
            "typed_exit": "ready",
            "branch_review_commit": "c" * 40,
            "owner_result": owner,
        }

        with self.assertRaises(gtt.WorkflowError) as mismatch:
            self.invoke(
                gtt.TASK_PUBLICATION_SKILL_ID,
                public_input,
                owner,
                checked,
            )
        self.assertEqual(
            mismatch.exception.payload.get("code"),
            "owner_result_input_mismatch",
        )

    def test_commit_semantic_route_is_owned_by_private_candidate(self) -> None:
        for status, expected_exit in (
            ("passed", "committed"),
            ("revision-required", "revision-required"),
            ("blocked", "blocked"),
        ):
            with self.subTest(status=status):
                self.assertEqual(
                    gtt.production_commit_semantic_exit({
                        "ai_review": {
                            "status": status,
                            "summary": "The candidate owner completed semantic review.",
                            "evidence": ["The exact task paths and commit message were reviewed."],
                        }
                    }),
                    expected_exit,
                )

        with self.assertRaisesRegex(
            gtt.WorkflowError,
            "no declared semantic exit",
        ):
            gtt.production_commit_semantic_exit({"ai_review": {"status": "unknown"}})


class TaskCommitCandidateExecutorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Task Commit Test"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "task-commit@example.invalid"], cwd=self.root, check=True)
        self.task_rel = ".trellis/tasks/example-task"
        self.task_dir = self.root / self.task_rel
        self.task_dir.mkdir(parents=True)
        (self.root / ".trellis/guru-team").mkdir(parents=True)
        (self.root / "src").mkdir()
        (self.root / "src/task.txt").write_text("base\n", encoding="utf-8")
        (self.root / ".gitignore").write_text(
            ".trellis/.runtime/\n",
            encoding="utf-8",
        )
        self.task = {
            "id": "example-task", "name": "example-task", "title": "Example task",
            "status": "in_progress", "branch": "feat/example-task", "base_branch": "main",
        }
        self.context = {
            "schema_version": "1.0", "task_artifact_dir": self.task_rel,
            "task_slug": "example-task", "workspace_slug": "example-task",
            "task_title": "Example task", "task_workspace_id": "example-task",
            "branch_name": "feat/example-task", "base_branch": "main",
            "base_ref": "main", "base_head_sha": "", "remote_head_sha": "",
            "source_issue": {"number": 122},
            "source_repo": {"repo": "owner/repo", "url": ""},
            "assignee": "tester", "actor": {"login": "tester"},
            "issue_scope_ledger_seed": {},
            "intake_summary": {"duplicate_decision": {}, "naming_quality": {}, "confirmation": {}},
        }
        self.ledger = {
            "schema_version": "2.0",
            "primary_issue": {
                "number": 122,
                "url": "https://github.com/owner/repo/issues/122",
                "title": "Example task",
                "reason": "Primary task scope.",
            },
            "close_issues": [{
                "number": 122,
                "url": "https://github.com/owner/repo/issues/122",
                "title": "Example task",
                "reason": "Primary task scope.",
            }],
            "related_issues": [], "followup_issues": [],
        }
        gtt.write_json(self.task_dir / "task.json", self.task)
        gtt.write_json(self.task_dir / "issue-scope-ledger.json", self.ledger)
        (self.root / ".trellis/guru-team/config.yml").write_text(
            "github_repo: owner/repo\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "chore(test): #122 初始化测试仓库"], cwd=self.root, check=True)
        subprocess.run(["git", "checkout", "-q", "-b", "feat/example-task"], cwd=self.root, check=True)
        gtt.write_runtime_mappings(
            self.root,
            gtt.load_config(self.root),
            {
                "workspace_slug": "example-task",
                "task_slug": "example-task",
                "task_dir": self.task_rel,
                "branch_name": "feat/example-task",
            },
            self.root,
        )
        schema = (
            Path(gtt.__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages/guru-create-task-commit/schemas/task-commit-candidate.schema.json"
        )
        self.phase2_commit_anchor_override: str | None = None

        def current_phase2_result(
            root: Path,
            _task_dir: Path,
            additional_dirty_excluded: set[str] | None = None,
        ) -> tuple[Path, dict[str, object], list[str]]:
            del additional_dirty_excluded
            phase2_commit_anchor = (
                self.phase2_commit_anchor_override or gtt.current_head(root)
            )
            return (
                self.task_dir / gtt.PHASE2_CHECK_ARTIFACT,
                {
                    "phase2_capture_commit": phase2_commit_anchor,
                    "typed_exit": "passed",
                },
                [],
            )

        self.patches = [
            mock.patch.object(gtt, "assert_workspace_boundary", return_value={"status": "ok"}),
            mock.patch.object(gtt, "task_commit_candidate_schema_path", return_value=schema),
            mock.patch.object(
                gtt,
                "validate_phase2_check",
                side_effect=current_phase2_result,
            ),
        ]
        for patcher in self.patches:
            patcher.start()

    def tearDown(self) -> None:
        for patcher in reversed(self.patches):
            patcher.stop()
        self.tmp.cleanup()

    def make_plan(
        self,
        sequence: int,
        reviewed_paths: list[str],
        unrelated_paths: list[str] | None = None,
    ) -> Path:
        task_key = hashlib.sha256(self.task_rel.encode("utf-8")).hexdigest()[:16]
        candidate = (
            self.root / gtt.TASK_COMMIT_RUNTIME_DIR / task_key / f"{sequence:03d}.json"
        )
        candidate_rel = candidate.relative_to(self.root).as_posix()
        snapshot = gtt.task_commit_snapshot_without_digest(
            gtt.capture_task_commit_snapshot(self.root, {candidate_rel})
        )
        classifications = [
            {
                "path": path,
                "category": "task-reviewed" if path in reviewed_paths else "unrelated-preserved",
                "reason": "Covered by the current Phase 2 result." if path in reviewed_paths else "Preserve unrelated test state.",
                "coverage_source": "guru-check-task passed result" if path in reviewed_paths else "AI scope review",
            }
            for path in [str(item["path"]) for item in snapshot["entries"]]
        ]
        exact_paths = set(reviewed_paths)
        snapshot_by_path = {str(item["path"]): item for item in snapshot["entries"]}
        for path in reviewed_paths:
            renamed_from = snapshot_by_path.get(path, {}).get("renamed_from")
            if renamed_from:
                exact_paths.add(str(renamed_from))
        message = gtt.task_commit_canonical_message(
            {
                "type": "feat",
                "scope": "workflow",
                "summary": "增加任务提交闭环",
                "background": "需要验证 task commit 闭环。",
                "changes": "提交精确测试路径。",
                "boundaries": "保留无关工作区状态。",
                "validations": "运行 task commit 单元测试。",
            },
            primary_issue=122,
        )
        plan = {
            "$schema": gtt.TASK_COMMIT_CANDIDATE_SCHEMA_ID,
            "schema_version": "3.0", "skill_id": gtt.TASK_COMMIT_SKILL_ID,
            "sequence": f"{sequence:03d}",
            "task": {"id": "example-task", "path": self.task_rel, "status": "in_progress", "branch": "feat/example-task"},
            "git": {
                "base_branch": "main",
                "base_ref": gtt.diff_base_ref(self.root, "main"),
                "pre_commit_head": gtt.current_head(self.root),
                "phase2_commit_anchor": gtt.current_head(self.root),
            },
            "dirty_snapshot": snapshot,
            "path_classifications": classifications,
            "exact_stage_paths": sorted(exact_paths),
            "message": message,
            "ai_review": {"status": "passed", "summary": "Reviewed exact test scope.", "evidence": ["Phase 2 covers each task-reviewed path."]},
        }
        gtt.write_json(candidate, plan)
        return candidate

    def task_commit_entry_state(self, candidate: Path) -> dict[str, object]:
        return {
            "head": gtt.current_head(self.root),
            "index": gtt.task_commit_index_preimage(self.root)["bytes"],
            "candidate": candidate.read_bytes(),
            "operation": gtt.task_commit_git_operation_state(self.root),
        }

    def assert_task_commit_entry_state(
        self,
        before: dict[str, object],
        candidate: Path,
        *,
        candidate_bytes: bytes | None = None,
    ) -> None:
        self.assertEqual(gtt.current_head(self.root), before["head"])
        self.assertEqual(gtt.task_commit_index_preimage(self.root)["bytes"], before["index"])
        self.assertEqual(
            candidate.read_bytes(),
            before["candidate"] if candidate_bytes is None else candidate_bytes,
        )
        self.assertEqual(gtt.task_commit_git_operation_state(self.root), before["operation"])

    def committed_paths(self, commit_sha: str) -> set[str]:
        return gtt.git_nul_path_set(
            self.root,
            [
                "diff-tree", "--root", "--no-commit-id", "--name-only",
                "--no-renames", "-r", "-z", commit_sha,
            ],
        )

    def run_task_commit_after_validation_mutation(
        self,
        candidate: Path,
        mutate: object,
    ) -> gtt.WorkflowError:
        before = self.task_commit_entry_state(candidate)
        original = gtt.task_commit_planned_index_bindings
        candidate_after_mutation: bytes | None = None

        def mutate_before_binding(*args: object, **kwargs: object) -> object:
            nonlocal candidate_after_mutation
            assert callable(mutate)
            mutate()
            candidate_after_mutation = candidate.read_bytes()
            return original(*args, **kwargs)

        with mock.patch.object(
            gtt,
            "task_commit_planned_index_bindings",
            side_effect=mutate_before_binding,
        ):
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertEqual(raised.exception.exit_code, 2)
        self.assert_task_commit_entry_state(
            before,
            candidate,
            candidate_bytes=candidate_after_mutation,
        )
        return raised.exception

    def add_submodule_history(self) -> tuple[Path, str, str, str]:
        source_tmp = tempfile.TemporaryDirectory()
        self.addCleanup(source_tmp.cleanup)
        source = Path(source_tmp.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=source, check=True)
        subprocess.run(["git", "config", "user.name", "Gitlink Test"], cwd=source, check=True)
        subprocess.run(["git", "config", "user.email", "gitlink@example.invalid"], cwd=source, check=True)
        revisions: list[str] = []
        for label in ("A", "B", "C"):
            (source / "dependency.txt").write_text(f"revision {label}\n", encoding="utf-8")
            subprocess.run(["git", "add", "dependency.txt"], cwd=source, check=True)
            subprocess.run(
                ["git", "commit", "-q", "-m", f"test(dependency): #122 添加版本 {label}"],
                cwd=source,
                check=True,
            )
            revisions.append(gtt.current_head(source))

        submodule = self.root / "deps/dependency"
        subprocess.run(
            ["git", "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(source), "deps/dependency"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(["git", "-C", str(submodule), "checkout", "-q", revisions[0]], cwd=self.root, check=True)
        subprocess.run(["git", "add", ".gitmodules", "deps/dependency"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(trellis): #122 添加 gitlink 基线"],
            cwd=self.root,
            check=True,
        )
        return submodule, revisions[0], revisions[1], revisions[2]

    def test_candidate_mode_validates_when_branch_range_is_empty(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])
        payload = gtt.cmd_check_commit_messages(argparse.Namespace(
            root=str(self.root), task=self.task_rel, candidate_artifact=str(candidate),
            primary_issue=None, base_ref=None, range=None,
        ))
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["mode"], "candidate")
        self.assertEqual(payload["checked_commits"], [])
        self.assertEqual(payload["candidate_validation"]["sequence"], "001")

    def public_commit_input(
        self,
        *,
        profile: str = "initial_commit",
        source_exit: str = "passed",
    ) -> dict[str, object]:
        return {
            "profile": profile,
            "mode": "workflow",
            "task_ref": self.task_rel,
            "source_exit": source_exit,
            "phase2_commit_anchor": (
                self.phase2_commit_anchor_override
                or gtt.current_head(self.root)
            ),
        }

    def task_commit_authoring(
        self,
        reviewed_paths: list[str],
        *,
        status: str = "passed",
    ) -> dict[str, object]:
        candidate, _ = gtt.task_commit_prepare_candidate_path(self.root, self.task_dir)
        snapshot = gtt.task_commit_snapshot_without_digest(
            gtt.capture_task_commit_snapshot(
                self.root, {candidate.relative_to(self.root).as_posix()}
            )
        )
        reviewed = set(reviewed_paths)
        return {
            "path_classifications": [
                {
                    "path": str(entry["path"]),
                    "category": (
                        "task-reviewed"
                        if entry["path"] in reviewed
                        else "unrelated-preserved"
                    ),
                    "reason": (
                        "Current Phase 2 covers this task path."
                        if entry["path"] in reviewed
                        else "Preserve unrelated test state."
                    ),
                    "coverage_source": (
                        "guru-check-task passed DTO"
                        if entry["path"] in reviewed
                        else "AI scope review"
                    ),
                }
                for entry in snapshot["entries"]
            ],
            "message": {
                "type": "feat",
                "scope": "trellis",
                "summary": "增加 production 提交闭环",
                "background": "需要验证 production public commit。",
                "changes": "通过 deterministic builder 提交精确路径。",
                "boundaries": "保留未纳入任务范围的工作区路径。",
                "validations": "运行 task commit focused tests。",
            },
            "ai_review": {
                "status": status,
                "summary": "AI reviewed the exact commit message and path set.",
                "evidence": ["Current Phase 2 covers every task-reviewed path."],
            },
        }

    def test_public_candidate_builder_materializes_exact_authority_and_preserves_unrelated(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        (self.root / "src/unrelated.txt").write_text("preserve\n", encoding="utf-8")

        candidate, plan, facts = gtt.build_task_commit_candidate(
            self.root,
            self.task_dir,
            self.public_commit_input(),
            self.task_commit_authoring(["src/task.txt"]),
        )

        self.assertEqual(candidate.name, "001.json")
        self.assertEqual(facts["exact_stage_paths"], ["src/task.txt"])
        self.assertTrue(
            candidate.relative_to(self.root).as_posix().startswith(
                gtt.TASK_COMMIT_RUNTIME_DIR
            )
        )
        classifications = {
            item["path"]: item["category"]
            for item in plan["path_classifications"]
        }
        self.assertEqual(classifications["src/task.txt"], "task-reviewed")
        self.assertEqual(classifications["src/unrelated.txt"], "unrelated-preserved")
        self.assertEqual(
            gtt.validate_task_commit_candidate(self.root, candidate, self.task_dir)[2],
            [],
        )

    def test_metadata_only_descendant_uses_live_head_as_commit_parent(self) -> None:
        phase2_commit_anchor = gtt.current_head(self.root)
        self.phase2_commit_anchor_override = phase2_commit_anchor
        (self.root / "src/task.txt").write_text("reviewed change\n", encoding="utf-8")
        metadata = self.task_dir / "context-discovery.json"
        metadata.write_text("publication metadata\n", encoding="utf-8")
        subprocess.run(
            ["git", "add", self.task_rel + "/context-discovery.json"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-qm", "chore(task): record publication metadata"],
            cwd=self.root,
            check=True,
        )
        descendant_head = gtt.current_head(self.root)
        self.assertNotEqual(descendant_head, phase2_commit_anchor)
        self.assertTrue(
            gtt.is_ancestor(self.root, phase2_commit_anchor, descendant_head)
        )

        candidate, plan, _ = gtt.build_task_commit_candidate(
            self.root,
            self.task_dir,
            self.public_commit_input(),
            self.task_commit_authoring(["src/task.txt"]),
        )
        phase2_checkpoint = gtt.phase2_check_path(self.root, self.task_dir)
        gtt.write_json(phase2_checkpoint, {"typed_exit": "passed"})

        self.assertEqual(
            plan["git"]["phase2_commit_anchor"], phase2_commit_anchor
        )
        self.assertEqual(plan["git"]["pre_commit_head"], descendant_head)
        result = gtt.execute_task_commit_candidate(
            self.root,
            candidate,
            self.task_dir,
        )
        self.assertEqual(result["pre_commit_head"], descendant_head)
        self.assertEqual(
            gtt.run_stdout(["git", "rev-parse", result["commit_sha"] + "^"], cwd=self.root),
            descendant_head,
        )
        self.assertFalse(phase2_checkpoint.exists())

    def test_candidate_builder_rejects_invalid_paths_and_stale_passed_dto_identity(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        stale_input = self.public_commit_input()
        stale_input["phase2_commit_anchor"] = "f" * 40
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.build_task_commit_candidate(
                self.root,
                self.task_dir,
                stale_input,
                self.task_commit_authoring(["src/task.txt"]),
            )
        self.assertEqual(
            str(raised.exception),
            "Public commit input does not bind the current passed Phase 2 identity.",
        )

        invalid_authoring = self.task_commit_authoring(["src/task.txt"])
        invalid_authoring["path_classifications"].append(
            {
                "path": "src/missing.txt",
                "category": "task-reviewed",
                "reason": "This path does not exist.",
                "coverage_source": "invalid test fixture",
            }
        )
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.build_task_commit_candidate(
                self.root,
                self.task_dir,
                self.public_commit_input(),
                invalid_authoring,
            )
        self.assertEqual(
            str(raised.exception),
            "Deterministic task commit candidate validation failed.",
        )
        self.assertEqual(
            list(
                (self.root / gtt.TASK_COMMIT_RUNTIME_DIR).glob(
                    "**/[0-9][0-9][0-9].json"
                )
            ),
            [],
        )

    def test_candidate_builder_accepts_profile_owned_reentry_sources(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")

        for profile, source_exit in (
            ("revision_reentry", "revision-required"),
            ("recovery_resume", "transaction_recovery"),
        ):
            with self.subTest(profile=profile):
                candidate, plan, _ = gtt.build_task_commit_candidate(
                    self.root,
                    self.task_dir,
                    self.public_commit_input(
                        profile=profile,
                        source_exit=source_exit,
                    ),
                    self.task_commit_authoring(["src/task.txt"], status="blocked"),
                )
                self.assertEqual(
                    plan["git"]["phase2_commit_anchor"],
                    gtt.current_head(self.root),
                )
                candidate.unlink()

    def test_candidate_builder_restores_existing_private_candidate_on_validation_failure(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])
        preimage = candidate.read_bytes()
        invalid_authoring = self.task_commit_authoring(["src/missing.txt"])

        with self.assertRaises(gtt.WorkflowError):
            gtt.build_task_commit_candidate(
                self.root,
                self.task_dir,
                self.public_commit_input(),
                invalid_authoring,
            )

        self.assertEqual(candidate.read_bytes(), preimage)

    def test_committed_candidate_recovery_verifies_current_result_and_passed_dto_identity(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        public_input = self.public_commit_input()
        candidate, _, _ = gtt.build_task_commit_candidate(
            self.root,
            self.task_dir,
            public_input,
            self.task_commit_authoring(["src/task.txt"]),
        )
        self.phase2_commit_anchor_override = str(
            public_input["phase2_commit_anchor"]
        )
        phase2_checkpoint = gtt.phase2_check_path(self.root, self.task_dir)
        gtt.write_json(phase2_checkpoint, {"typed_exit": "passed"})
        original_publish = gtt.task_commit_publish_validated_commit

        def publish_then_interrupt(*args: object, **kwargs: object) -> None:
            original_publish(*args, **kwargs)
            raise gtt.WorkflowError("simulated interruption after ref publication", exit_code=2)

        with (
            mock.patch.object(
                gtt,
                "task_commit_publish_validated_commit",
                side_effect=publish_then_interrupt,
            ),
            self.assertRaisesRegex(gtt.WorkflowError, "simulated interruption"),
        ):
            gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)
        committed_sha = gtt.current_head(self.root)
        self.assertTrue(candidate.is_file())
        self.assertTrue(phase2_checkpoint.is_file())

        recovery = self.public_commit_input(
            profile="recovery_resume", source_exit="transaction_recovery"
        )
        recovery["phase2_commit_anchor"] = public_input[
            "phase2_commit_anchor"
        ]
        args = argparse.Namespace(
            owner_result=candidate.relative_to(self.root).as_posix()
        )
        owner_result, verified = gtt.production_commit_result(
            self.root, args, recovery
        )
        self.assertEqual(owner_result, {"typed_exit": "committed"})
        self.assertIsNotNone(verified)
        self.assertEqual(verified["commit_sha"], committed_sha)  # type: ignore[index]
        self.assertFalse(candidate.exists())
        self.assertFalse(phase2_checkpoint.exists())

        recovery["phase2_commit_anchor"] = "f" * 40
        args.owner_result = None
        blocked, evidence = gtt.production_commit_result(self.root, args, recovery)
        self.assertEqual(blocked, {"typed_exit": "blocked"})
        self.assertEqual(
            evidence["errors"],  # type: ignore[index]
            ["Task commit recovery requires the surviving owner-private candidate."],
        )

    def test_committed_candidate_recovery_rejects_parseable_sibling_commit(self) -> None:
        task_path = self.root / "src/task.txt"
        task_path.write_text("candidate content\n", encoding="utf-8")
        public_input = self.public_commit_input()
        candidate, plan, _ = gtt.build_task_commit_candidate(
            self.root,
            self.task_dir,
            public_input,
            self.task_commit_authoring(["src/task.txt"]),
        )
        self.phase2_commit_anchor_override = str(
            public_input["phase2_commit_anchor"]
        )

        task_path.write_text("sibling content\n", encoding="utf-8")
        message_path = self.root / "sibling-commit-message.txt"
        message_path.write_bytes(plan["message"]["bytes"].encode("utf-8"))
        subprocess.run(["git", "add", "src/task.txt"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "--cleanup=verbatim", "-F", str(message_path)],
            cwd=self.root,
            check=True,
        )
        recovery = self.public_commit_input(
            profile="recovery_resume", source_exit="transaction_recovery"
        )
        recovery["phase2_commit_anchor"] = public_input[
            "phase2_commit_anchor"
        ]
        args = argparse.Namespace(
            owner_result=candidate.relative_to(self.root).as_posix()
        )

        owner_result, evidence = gtt.production_commit_result(
            self.root, args, recovery
        )

        self.assertEqual(owner_result, {"typed_exit": "blocked"})
        self.assertEqual(
            evidence["errors"],  # type: ignore[index]
            ["Current recovery commit does not match the surviving private candidate."],
        )
        self.assertTrue(candidate.is_file())

    def test_review_entry_accepts_current_commit_identity_and_rejects_stale_identity(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        candidate, _, _ = gtt.build_task_commit_candidate(
            self.root,
            self.task_dir,
            self.public_commit_input(),
            self.task_commit_authoring(["src/task.txt"]),
        )
        committed = gtt.execute_task_commit_candidate(
            self.root,
            candidate,
            self.task_dir,
        )
        review_input = {
            "task_ref": self.task_rel,
            "base_ref": gtt.diff_base_ref(self.root, "main"),
            "branch_review_commit": committed["commit_sha"],
        }

        self.assertEqual(
            gtt.review_branch_commit_identity_errors(
                self.root,
                self.task_dir,
                self.task,
                self.context,
                review_input,
            ),
            [],
        )

        entry_input = {
            **review_input,
            "profile": "branch_review",
            "mode": "workflow",
            "review_intent": "initial_review",
        }
        with (
            mock.patch.object(
                gtt,
                "review_branch_public_input_schema",
                return_value={},
            ),
            mock.patch.object(
                gtt,
                "review_branch_gate_schema",
                return_value={},
            ),
        ):
            self.assertEqual(
                gtt.review_branch_entry_precondition_errors(
                    self.root,
                    self.task_dir,
                    gtt.load_config(self.root),
                    public_input=entry_input,
                ),
                [],
            )

        review_input["branch_review_commit"] = "f" * 40
        errors = gtt.review_branch_commit_identity_errors(
            self.root,
            self.task_dir,
            self.task,
            self.context,
            review_input,
        )
        self.assertIn(
            "review entry branch_review_commit is not the current HEAD.",
            errors,
        )
        self.assertTrue(
            any("review entry live commit validation failed" in error for error in errors)
        )

    def test_review_entry_commit_identity_ignores_message_format(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        subprocess.run(["git", "add", "src/task.txt"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-qm", "plain noncanonical task message"],
            cwd=self.root,
            check=True,
        )
        commit = gtt.current_head(self.root)

        self.assertEqual(
            gtt.review_branch_commit_identity_errors(
                self.root,
                self.task_dir,
                self.task,
                self.context,
                {
                    "task_ref": self.task_rel,
                    "base_ref": gtt.diff_base_ref(self.root, "main"),
                    "branch_review_commit": commit,
                },
            ),
            [],
        )

    def test_review_gate_checker_and_public_wrapper_accept_metadata_descendant_and_block_content_descendant(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        candidate, _, _ = gtt.build_task_commit_candidate(
            self.root,
            self.task_dir,
            self.public_commit_input(),
            self.task_commit_authoring(["src/task.txt"]),
        )
        committed = gtt.execute_task_commit_candidate(
            self.root,
            candidate,
            self.task_dir,
        )
        review_commit = str(committed["commit_sha"])
        reviewed_content_sha256 = gtt.reviewed_content_identity(
            self.root,
            review_commit,
            include_worktree=False,
        )["sha256"]
        package = (
            Path(gtt.__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages/guru-review-branch"
        )
        gate = gtt.read_json(package / "examples/review-gate.json")
        gate.update({
            "task_dir": self.task_rel,
            "base_ref": gtt.diff_base_ref(self.root, "main"),
            "review_commit": review_commit,
            "reviewed_content_sha256": reviewed_content_sha256,
        })
        gate["facts_sha256"] = gtt.context_digest({
            key: value
            for key, value in gate.items()
            if key not in {"generated_at", "facts_sha256"}
        })
        gate_path = gtt.configured_review_gate_path(self.root, self.task_dir)
        gtt.write_json(gate_path, gate)

        metadata_path = self.task_dir / "context-discovery.json"
        metadata_path.write_text("publication metadata\n", encoding="utf-8")
        subprocess.run(
            ["git", "add", "--", metadata_path.relative_to(self.root).as_posix()],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-qm", "chore(task): #122 记录发布元数据"],
            cwd=self.root,
            check=True,
        )

        initial_errors = gtt.review_branch_commit_identity_errors(
            self.root,
            self.task_dir,
            self.task,
            self.context,
            {
                "task_ref": self.task_rel,
                "base_ref": gtt.diff_base_ref(self.root, "main"),
                "branch_review_commit": review_commit,
            },
        )
        self.assertIn(
            "review entry branch_review_commit is not the current HEAD.",
            initial_errors,
        )

        schema_patchers = (
            mock.patch.object(
                gtt,
                "review_branch_public_input_schema",
                return_value=gtt.read_json(
                    package / "schemas/public-branch-review-input.schema.json"
                ),
            ),
            mock.patch.object(
                gtt,
                "review_branch_gate_schema",
                return_value=gtt.read_json(package / "schemas/review-gate.schema.json"),
            ),
        )
        for patcher in schema_patchers:
            patcher.start()
        try:
            checked = gtt.cmd_check_review_gate(argparse.Namespace(
                root=str(self.root),
                task=self.task_rel,
                allow_nonpass=False,
                expected_exit="passed",
            ))
            self.assertEqual(checked["review_commit"], review_commit)
            self.assertEqual(checked["head"], gtt.current_head(self.root))

            public_input_path = (
                self.root
                / ".trellis/.runtime/guru-team/review-wrapper-input.json"
            )
            gtt.write_json(
                public_input_path,
                {
                    "profile": "branch_review",
                    "mode": "workflow",
                    "task_ref": self.task_rel,
                    "base_ref": gtt.diff_base_ref(self.root, "main"),
                    "branch_review_commit": review_commit,
                    "review_intent": "fresh_final_review",
                },
            )
            wrapper_args = argparse.Namespace(
                input=public_input_path.relative_to(self.root).as_posix(),
                owner_result=gate_path.relative_to(self.root).as_posix(),
            )
            with (
                mock.patch.object(
                    gtt,
                    "stage0_invocation_identity",
                    return_value=(gtt.BRANCH_REVIEW_SKILL_ID, package),
                ),
                mock.patch.object(gtt, "stage0_repo_root", return_value=self.root),
            ):
                self.assertEqual(
                    gtt.cmd_invoke_stage0_skill(wrapper_args),
                    {
                        "exit_id": "passed",
                        "task_ref": self.task_rel,
                        "branch_review_commit": review_commit,
                    },
                )
            self.assertFalse(gate_path.exists())

            gtt.write_json(gate_path, gate)

            (self.root / "src/task.txt").write_text(
                "changed after review\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "--", "src/task.txt"], cwd=self.root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "fix(workflow): #122 修改已审查内容"],
                cwd=self.root,
                check=True,
            )
            with self.assertRaises(gtt.WorkflowError) as stale:
                gtt.cmd_check_review_gate(argparse.Namespace(
                    root=str(self.root),
                    task=self.task_rel,
                    allow_nonpass=False,
                    expected_exit="passed",
                ))
            self.assertTrue(
                any(
                    gtt.BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX in error
                    for error in stale.exception.payload["errors"]
                )
            )
            with (
                mock.patch.object(
                    gtt,
                    "stage0_invocation_identity",
                    return_value=(gtt.BRANCH_REVIEW_SKILL_ID, package),
                ),
                mock.patch.object(gtt, "stage0_repo_root", return_value=self.root),
            ):
                self.assertEqual(
                    gtt.cmd_invoke_stage0_skill(wrapper_args),
                    {"exit_id": "blocked"},
                )
        finally:
            for patcher in reversed(schema_patchers):
                patcher.stop()

    def test_public_wrapper_builds_executes_and_serializes_minimal_committed_dto(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        (self.root / "src/unrelated.txt").write_text("preserve\n", encoding="utf-8")
        public_input_path = self.root / "public-commit-input.json"
        public_input_path.write_text(
            json.dumps(self.public_commit_input(), ensure_ascii=False),
            encoding="utf-8",
        )
        candidate, _, _ = gtt.build_task_commit_candidate(
            self.root,
            self.task_dir,
            self.public_commit_input(),
            self.task_commit_authoring(["src/task.txt"]),
        )
        package = (
            Path(gtt.__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages/guru-create-task-commit"
        )
        args = argparse.Namespace(
            input=public_input_path.relative_to(self.root).as_posix(),
            owner_result=candidate.relative_to(self.root).as_posix(),
        )

        with (
            mock.patch.object(
                gtt,
                "stage0_invocation_identity",
                return_value=("guru-create-task-commit", package),
            ),
            mock.patch.object(gtt, "stage0_repo_root", return_value=self.root),
        ):
            output = gtt.cmd_invoke_stage0_skill(args)

        self.assertEqual(set(output), {
            "exit_id", "task_ref", "base_ref", "branch_review_commit",
        })
        self.assertEqual(output["exit_id"], "committed")
        self.assertEqual(output["task_ref"], self.task_rel)
        self.assertEqual(output["branch_review_commit"], gtt.current_head(self.root))
        self.assertEqual((self.root / "src/unrelated.txt").read_text(), "preserve\n")
        self.assertIn("src/unrelated.txt", gtt.git_status_paths(self.root))

    def test_git_operation_marker_matrix_is_objective_and_non_mutating(self) -> None:
        for operation_id, git_path_name in gtt.TASK_COMMIT_GIT_OPERATION_MARKERS:
            with self.subTest(operation=operation_id):
                marker = gtt.task_commit_git_path(self.root, git_path_name)
                if git_path_name in {"sequencer", "rebase-merge", "rebase-apply"}:
                    marker.mkdir(parents=True)
                    (marker / "state").write_text(operation_id, encoding="utf-8")
                else:
                    marker.parent.mkdir(parents=True, exist_ok=True)
                    marker.write_text(operation_id, encoding="utf-8")
                before = marker.lstat()

                state = gtt.task_commit_git_operation_state(self.root)

                self.assertEqual(state["status"], "blocked")
                self.assertIn(operation_id, [item["id"] for item in state["active"]])
                self.assertEqual(marker.lstat().st_ino, before.st_ino)
                if marker.is_dir():
                    shutil.rmtree(marker)
                else:
                    marker.unlink()
        self.assertEqual(gtt.task_commit_git_operation_state(self.root), {"status": "ordinary", "active": []})

    def test_real_cherry_pick_state_blocks_candidate_and_executor_without_mutation(self) -> None:
        conflict = self.root / "src/conflict.txt"
        conflict.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "src/conflict.txt"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "test(trellis): #122 添加冲突基线"], cwd=self.root, check=True)
        task_branch = gtt.current_branch(self.root)
        subprocess.run(["git", "checkout", "-q", "-b", "cherry-source"], cwd=self.root, check=True)
        conflict.write_text("source\n", encoding="utf-8")
        subprocess.run(["git", "add", "src/conflict.txt"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "test(trellis): #122 添加待拣选修改"], cwd=self.root, check=True)
        source_commit = gtt.current_head(self.root)
        subprocess.run(["git", "checkout", "-q", task_branch], cwd=self.root, check=True)
        conflict.write_text("target\n", encoding="utf-8")
        subprocess.run(["git", "add", "src/conflict.txt"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "test(trellis): #122 添加目标修改"], cwd=self.root, check=True)
        (self.root / "src/task.txt").write_text("reviewed\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])

        cherry_pick = subprocess.run(
            ["git", "cherry-pick", source_commit],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertNotEqual(cherry_pick.returncode, 0)
        marker = gtt.task_commit_git_path(self.root, "CHERRY_PICK_HEAD")
        self.assertTrue(marker.is_file())
        before = {
            "head": gtt.current_head(self.root),
            "marker": marker.read_bytes(),
            "index": subprocess.run(["git", "ls-files", "--stage", "-z"], cwd=self.root, check=True, stdout=subprocess.PIPE).stdout,
            "status": subprocess.run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=self.root, check=True, stdout=subprocess.PIPE).stdout,
            "candidate": candidate.read_bytes(),
        }

        _, facts, errors = gtt.validate_task_commit_candidate(self.root, candidate, self.task_dir)
        self.assertTrue(any("ordinary Git operation state" in error for error in errors))
        self.assertEqual(facts["git_operation_state"]["status"], "blocked")
        with self.assertRaises(gtt.WorkflowError) as validator_error:
            gtt.cmd_check_commit_messages(
                argparse.Namespace(
                    root=str(self.root),
                    task=self.task_rel,
                    candidate_artifact=str(candidate),
                    primary_issue=None,
                    base_ref=None,
                    range=None,
                )
            )
        self.assertEqual(validator_error.exception.exit_code, 2)
        self.assertEqual(validator_error.exception.payload["status"], "blocked")
        with self.assertRaises(gtt.WorkflowError):
            gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertEqual(gtt.current_head(self.root), before["head"])
        self.assertEqual(marker.read_bytes(), before["marker"])
        self.assertEqual(subprocess.run(["git", "ls-files", "--stage", "-z"], cwd=self.root, check=True, stdout=subprocess.PIPE).stdout, before["index"])
        self.assertEqual(subprocess.run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=self.root, check=True, stdout=subprocess.PIPE).stdout, before["status"])
        self.assertEqual(candidate.read_bytes(), before["candidate"])

    def test_gitlink_revision_change_makes_candidate_stale_without_staging(self) -> None:
        submodule, revision_a, revision_b, revision_c = self.add_submodule_history()
        subprocess.run(["git", "-C", str(submodule), "checkout", "-q", revision_b], cwd=self.root, check=True)
        candidate = self.make_plan(1, ["deps/dependency"])

        plan, _, errors = gtt.validate_task_commit_candidate(self.root, candidate, self.task_dir)
        self.assertEqual(errors, [])
        entry = next(item for item in plan["dirty_snapshot"]["entries"] if item["path"] == "deps/dependency")
        self.assertEqual(entry["mode"], "160000")
        self.assertEqual(entry["index_blob"], revision_a)
        self.assertEqual(entry["gitlink_head"], revision_b)
        self.assertTrue(entry["gitlink_initialized"])
        self.assertFalse(entry["gitlink_dirty"])

        subprocess.run(["git", "-C", str(submodule), "checkout", "-q", revision_c], cwd=self.root, check=True)
        before_head = gtt.current_head(self.root)
        before_tree = gtt.task_commit_write_tree(self.root)
        before_status = subprocess.run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=self.root, check=True, stdout=subprocess.PIPE).stdout
        before_candidate = candidate.read_bytes()

        _, _, stale_errors = gtt.validate_task_commit_candidate(self.root, candidate, self.task_dir)
        self.assertTrue(any("dirty_snapshot is stale" in error for error in stale_errors))
        with self.assertRaises(gtt.WorkflowError):
            gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertEqual(gtt.current_head(self.root), before_head)
        self.assertEqual(gtt.task_commit_write_tree(self.root), before_tree)
        self.assertEqual(gtt.task_commit_index_identity(self.root, "deps/dependency"), (revision_a, "160000"))
        self.assertEqual(gtt.task_commit_gitlink_worktree_identity(self.root, "deps/dependency")["gitlink_head"], revision_c)
        self.assertEqual(subprocess.run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=self.root, check=True, stdout=subprocess.PIPE).stdout, before_status)
        self.assertEqual(candidate.read_bytes(), before_candidate)

    def test_gitlink_switch_after_executor_entry_blocks_before_stage_and_never_indexes_c(self) -> None:
        submodule, revision_a, revision_b, revision_c = self.add_submodule_history()
        subprocess.run(["git", "-C", str(submodule), "checkout", "-q", revision_b], cwd=self.root, check=True)
        candidate = self.make_plan(1, ["deps/dependency"])
        _, _, entry_errors = gtt.validate_task_commit_candidate(
            self.root, candidate, self.task_dir
        )
        self.assertEqual(entry_errors, [])
        before = {
            "head": gtt.current_head(self.root),
            "index": subprocess.run(
                ["git", "ls-files", "--stage", "-z"],
                cwd=self.root,
                check=True,
                stdout=subprocess.PIPE,
            ).stdout,
            "candidate": candidate.read_bytes(),
            "operation": gtt.task_commit_git_operation_state(self.root),
        }
        original_identity = gtt.task_commit_gitlink_worktree_identity
        identity_calls = 0

        def switch_before_exact_stage(root: Path, path: str) -> dict[str, object]:
            nonlocal identity_calls
            identity_calls += 1
            if identity_calls == 2:
                subprocess.run(
                    ["git", "-C", str(submodule), "checkout", "-q", revision_c],
                    cwd=self.root,
                    check=True,
                )
            return original_identity(root, path)

        with mock.patch.object(
            gtt,
            "task_commit_gitlink_worktree_identity",
            side_effect=switch_before_exact_stage,
        ):
            with self.assertRaises(gtt.WorkflowError) as blocked:
                gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertEqual(blocked.exception.exit_code, 2)
        self.assertEqual(blocked.exception.payload["status"], "blocked")
        self.assertIn("worktree HEAD no longer matches", blocked.exception.payload["gitlink_binding_errors"][0])
        self.assertEqual(identity_calls, 2)
        self.assertEqual(gtt.current_head(self.root), before["head"])
        self.assertEqual(
            subprocess.run(
                ["git", "ls-files", "--stage", "-z"],
                cwd=self.root,
                check=True,
                stdout=subprocess.PIPE,
            ).stdout,
            before["index"],
        )
        self.assertEqual(gtt.task_commit_index_identity(self.root, "deps/dependency"), (revision_a, "160000"))
        self.assertNotEqual(gtt.task_commit_index_identity(self.root, "deps/dependency")[0], revision_c)
        self.assertEqual(candidate.read_bytes(), before["candidate"])
        self.assertEqual(gtt.task_commit_git_operation_state(self.root), before["operation"])

        subprocess.run(["git", "-C", str(submodule), "checkout", "-q", revision_b], cwd=self.root, check=True)
        payload = gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)
        self.assertEqual(payload["status"], "committed")
        self.assertEqual(
            gtt.task_commit_tree_path_identity(self.root, payload["commit_sha"], "deps/dependency"),
            (revision_b, "160000"),
        )
        self.assertNotEqual(
            gtt.task_commit_tree_path_identity(self.root, payload["commit_sha"], "deps/dependency")[0],
            revision_c,
        )

    def test_gitlink_uninitialized_dirty_and_unborn_states_fail_closed(self) -> None:
        submodule, _, revision_b, _ = self.add_submodule_history()
        subprocess.run(["git", "-C", str(submodule), "checkout", "-q", revision_b], cwd=self.root, check=True)
        (submodule / "dependency.txt").write_text("dirty\n", encoding="utf-8")
        with self.assertRaises(gtt.WorkflowError):
            gtt.task_commit_gitlink_worktree_identity(self.root, "deps/dependency")
        with self.assertRaises(gtt.WorkflowError):
            gtt.capture_task_commit_snapshot(self.root)

        subprocess.run(["git", "-C", str(submodule), "checkout", "--", "dependency.txt"], cwd=self.root, check=True)
        subprocess.run(["git", "submodule", "deinit", "-f", "--", "deps/dependency"], cwd=self.root, check=True, stdout=subprocess.PIPE)
        with self.assertRaises(gtt.WorkflowError):
            gtt.task_commit_gitlink_worktree_identity(self.root, "deps/dependency")

        subprocess.run(["git", "init", "-q", str(submodule)], cwd=self.root, check=True)
        with self.assertRaises(gtt.WorkflowError):
            gtt.task_commit_gitlink_worktree_identity(self.root, "deps/dependency")

    def test_tracked_b_to_c_after_validation_preserves_transaction_preimages(self) -> None:
        path = self.root / "src/task.txt"
        path.write_text("reviewed-B\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])

        self.run_task_commit_after_validation_mutation(
            candidate,
            lambda: path.write_text("unreviewed-C\n", encoding="utf-8"),
        )
        self.assertEqual(path.read_text(encoding="utf-8"), "unreviewed-C\n")

    def test_symlink_b_to_c_after_validation_preserves_transaction_preimages(self) -> None:
        link = self.root / "src/reviewed-link"
        os.symlink("target-B", link)
        candidate = self.make_plan(1, ["src/reviewed-link"])

        def mutate() -> None:
            link.unlink()
            os.symlink("target-C", link)

        self.run_task_commit_after_validation_mutation(candidate, mutate)
        self.assertEqual(os.readlink(link), "target-C")

    def test_reviewed_delete_recreate_after_validation_never_commits_c(self) -> None:
        path = self.root / "src/task.txt"
        path.unlink()
        candidate = self.make_plan(1, ["src/task.txt"])

        self.run_task_commit_after_validation_mutation(
            candidate,
            lambda: path.write_text("unreviewed-C\n", encoding="utf-8"),
        )
        self.assertEqual(path.read_text(encoding="utf-8"), "unreviewed-C\n")

    def test_rename_destination_b_to_c_after_validation_never_commits_c(self) -> None:
        source = "src/task.txt"
        destination = "src/renamed-task.txt"
        subprocess.run(["git", "mv", source, destination], cwd=self.root, check=True)
        target = self.root / destination
        target.write_text("reviewed-B\n", encoding="utf-8")
        candidate = self.make_plan(1, [destination])

        self.run_task_commit_after_validation_mutation(
            candidate,
            lambda: target.write_text("unreviewed-C\n", encoding="utf-8"),
        )
        self.assertEqual(target.read_text(encoding="utf-8"), "unreviewed-C\n")

    def test_multiple_paths_second_b_to_c_after_validation_never_commits_c(self) -> None:
        first = self.root / "src/first.txt"
        second = self.root / "src/second.txt"
        first.write_text("reviewed-B1\n", encoding="utf-8")
        second.write_text("reviewed-B2\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/first.txt", "src/second.txt"])

        self.run_task_commit_after_validation_mutation(
            candidate,
            lambda: second.write_text("unreviewed-C2\n", encoding="utf-8"),
        )
        self.assertEqual(first.read_text(encoding="utf-8"), "reviewed-B1\n")
        self.assertEqual(second.read_text(encoding="utf-8"), "unreviewed-C2\n")

    def test_candidate_self_raw_mutation_after_validation_is_never_published(self) -> None:
        task_path = self.root / "src/task.txt"
        task_path.write_text("reviewed-B\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])

        self.run_task_commit_after_validation_mutation(
            candidate,
            lambda: candidate.write_bytes(candidate.read_bytes() + b" \n"),
        )
        self.assertTrue(candidate.read_bytes().endswith(b" \n"))

    def test_entry_index_a_worktree_b_then_c_preserves_complete_index_a(self) -> None:
        path = self.root / "src/task.txt"
        path.write_text("staged-A\n", encoding="utf-8")
        subprocess.run(["git", "add", "src/task.txt"], cwd=self.root, check=True)
        path.write_text("reviewed-B\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])
        index_a = gtt.task_commit_index_identity(self.root, "src/task.txt")

        self.run_task_commit_after_validation_mutation(
            candidate,
            lambda: path.write_text("unreviewed-C\n", encoding="utf-8"),
        )
        self.assertEqual(gtt.task_commit_index_identity(self.root, "src/task.txt"), index_a)
        self.assertEqual(path.read_text(encoding="utf-8"), "unreviewed-C\n")

    def test_exact_executor_commits_only_reviewed_paths_and_preserves_unrelated(self) -> None:
        reviewed = "src/任务 [one]*.txt"
        (self.root / reviewed).write_text("reviewed\n", encoding="utf-8")
        (self.root / "unrelated.log").write_text("keep\n", encoding="utf-8")
        self.assertIn(reviewed, gtt.git_status_paths(self.root))
        candidate = self.make_plan(1, [reviewed], ["unrelated.log"])

        payload = gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertEqual(payload["status"], "committed")
        self.assertEqual(self.committed_paths(payload["commit_sha"]), {reviewed})
        self.assertEqual((self.root / "unrelated.log").read_text(encoding="utf-8"), "keep\n")
        self.assertIn("unrelated.log", gtt.git_status_paths(self.root))
        self.assertFalse(candidate.exists())
        self.assertEqual(gtt.current_head(self.root), payload["commit_sha"])
        self.assertEqual(
            gtt.task_commit_write_tree(self.root),
            gtt.task_commit_commit_tree(self.root, payload["commit_sha"]),
        )
        self.assertNotIn(gtt.TASK_COMMIT_RUNTIME_DIR, gtt.git_status_paths(self.root))

    def test_index_identity_uses_literal_exact_record_for_metacharacter_paths(self) -> None:
        literal = "src/[0]*.txt"
        decoy = "src/0foo.txt"
        (self.root / literal).write_text("literal tracked\n", encoding="utf-8")
        (self.root / decoy).write_text("decoy tracked\n", encoding="utf-8")
        subprocess.run(
            ["git", "--literal-pathspecs", "add", "--", literal, decoy],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(trellis): #122 添加字面路径测试"],
            cwd=self.root,
            check=True,
        )

        tracked_blob = subprocess.run(
            ["git", "hash-object", literal],
            cwd=self.root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        self.assertEqual(gtt.task_commit_index_identity(self.root, literal), (tracked_blob, "100644"))
        self.assertEqual(gtt.task_commit_tree_path_identity(self.root, "HEAD", literal), (tracked_blob, "100644"))

        (self.root / literal).write_text("literal staged\n", encoding="utf-8")
        subprocess.run(["git", "--literal-pathspecs", "add", "--", literal], cwd=self.root, check=True)
        staged_blob = subprocess.run(
            ["git", "hash-object", literal],
            cwd=self.root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        self.assertEqual(gtt.task_commit_index_identity(self.root, literal), (staged_blob, "100644"))

        (self.root / literal).unlink()
        self.assertEqual(gtt.task_commit_index_identity(self.root, literal), (staged_blob, "100644"))
        subprocess.run(["git", "--literal-pathspecs", "add", "--", literal], cwd=self.root, check=True)
        self.assertEqual(gtt.task_commit_index_identity(self.root, literal), (None, None))

    def test_index_identity_rejects_unmerged_literal_path(self) -> None:
        path = "src/conflicted [0]*.txt"
        (self.root / path).write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "--literal-pathspecs", "add", "--", path], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(trellis): #122 添加冲突路径基线"],
            cwd=self.root,
            check=True,
        )
        base_branch = gtt.current_branch(self.root)
        subprocess.run(["git", "checkout", "-q", "-b", "conflict-side"], cwd=self.root, check=True)
        (self.root / path).write_text("side\n", encoding="utf-8")
        subprocess.run(["git", "--literal-pathspecs", "add", "--", path], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(trellis): #122 修改冲突路径侧支"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(["git", "checkout", "-q", base_branch], cwd=self.root, check=True)
        (self.root / path).write_text("main\n", encoding="utf-8")
        subprocess.run(["git", "--literal-pathspecs", "add", "--", path], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(trellis): #122 修改冲突路径主支"],
            cwd=self.root,
            check=True,
        )
        merge = subprocess.run(
            ["git", "merge", "--no-edit", "conflict-side"],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertNotEqual(merge.returncode, 0)

        with self.assertRaises(gtt.WorkflowError):
            gtt.task_commit_index_identity(self.root, path)

    def test_exact_executor_never_stages_private_candidate(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])
        candidate_rel = candidate.relative_to(self.root).as_posix()

        payload = gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertEqual(self.committed_paths(payload["commit_sha"]), {"src/task.txt"})
        self.assertEqual(
            gtt.task_commit_tree_path_identity(self.root, payload["commit_sha"], candidate_rel),
            (None, None),
        )
        self.assertFalse(candidate.exists())

    def test_exact_executor_stages_reviewed_delete_without_broad_add(self) -> None:
        reviewed = "src/task.txt"
        (self.root / reviewed).unlink()
        candidate = self.make_plan(1, [reviewed])

        payload = gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertEqual(self.committed_paths(payload["commit_sha"]), {reviewed})
        self.assertFalse((self.root / reviewed).exists())

    def test_exact_executor_preserves_rename_source_and_destination(self) -> None:
        source = "src/task.txt"
        destination = "src/重命名 [two]*.txt"
        subprocess.run(["git", "mv", source, destination], cwd=self.root, check=True)
        candidate = self.make_plan(1, [destination])

        payload = gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertEqual(self.committed_paths(payload["commit_sha"]), {source, destination})
        self.assertFalse((self.root / source).exists())
        self.assertTrue((self.root / destination).is_file())

    def test_copy_relation_never_stages_unrelated_modified_source(self) -> None:
        source = "src/task.txt"
        destination = "src/z-copy.txt"
        subprocess.run(
            ["git", "config", "status.renames", "copies"],
            cwd=self.root,
            check=True,
        )
        (self.root / destination).write_bytes((self.root / source).read_bytes())
        subprocess.run(["git", "add", "--", destination], cwd=self.root, check=True)
        (self.root / source).write_text("unrelated staged source\n", encoding="utf-8")
        subprocess.run(["git", "add", "--", source], cwd=self.root, check=True)

        candidate = self.make_plan(1, [destination], [source])
        plan = json.loads(candidate.read_text(encoding="utf-8"))
        by_path = {
            str(item["path"]): item for item in plan["dirty_snapshot"]["entries"]
        }
        self.assertEqual(by_path[destination]["renamed_from"], None)
        self.assertEqual(by_path[destination]["copied_from"], source)
        self.assertEqual(by_path[source]["renamed_from"], None)
        self.assertEqual(by_path[source]["copied_from"], None)
        self.assertNotIn(source, plan["exact_stage_paths"])
        _, _, validation_errors = gtt.validate_task_commit_candidate(
            self.root, candidate, self.task_dir
        )
        self.assertEqual(validation_errors, [])

        before = self.task_commit_entry_state(candidate)
        source_tree_identity = gtt.task_commit_tree_path_identity(
            self.root, before["head"], source
        )
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertIn(source, raised.exception.payload["unexpected_staged_paths"])
        self.assert_task_commit_entry_state(before, candidate)
        self.assertEqual(
            gtt.task_commit_tree_path_identity(self.root, before["head"], source),
            source_tree_identity,
        )
        self.assertEqual(
            gtt.task_commit_tree_path_identity(self.root, before["head"], destination),
            (None, None),
        )
        self.assertEqual(
            (self.root / source).read_text(encoding="utf-8"),
            "unrelated staged source\n",
        )

    def test_copy_config_with_clean_source_commits_only_destination(self) -> None:
        source = "src/task.txt"
        destination = "src/clean-copy.txt"
        subprocess.run(
            ["git", "config", "status.renames", "copies"],
            cwd=self.root,
            check=True,
        )
        source_head_identity = gtt.task_commit_tree_path_identity(self.root, "HEAD", source)
        (self.root / destination).write_bytes((self.root / source).read_bytes())
        subprocess.run(["git", "add", "--", destination], cwd=self.root, check=True)
        candidate = self.make_plan(1, [destination])

        payload = gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertEqual(self.committed_paths(payload["commit_sha"]), {destination})
        self.assertEqual(
            gtt.task_commit_tree_path_identity(
                self.root, payload["commit_sha"], source
            ),
            source_head_identity,
        )
        self.assertNotEqual(
            gtt.task_commit_tree_path_identity(
                self.root, payload["commit_sha"], destination
            ),
            (None, None),
        )
        self.assertEqual((self.root / source).read_text(encoding="utf-8"), "base\n")

    def test_independently_reviewed_copy_source_is_updated_not_deleted(self) -> None:
        source = "src/task.txt"
        destination = "src/z-reviewed-copy.txt"
        subprocess.run(
            ["git", "config", "status.renames", "copies"],
            cwd=self.root,
            check=True,
        )
        (self.root / destination).write_bytes((self.root / source).read_bytes())
        subprocess.run(["git", "add", "--", destination], cwd=self.root, check=True)
        (self.root / source).write_text("reviewed source update\n", encoding="utf-8")
        subprocess.run(["git", "add", "--", source], cwd=self.root, check=True)
        candidate = self.make_plan(1, [source, destination])
        plan = json.loads(candidate.read_text(encoding="utf-8"))
        by_path = {
            str(item["path"]): item for item in plan["dirty_snapshot"]["entries"]
        }
        self.assertEqual(by_path[destination]["copied_from"], source)
        self.assertEqual(by_path[destination]["renamed_from"], None)

        payload = gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertEqual(self.committed_paths(payload["commit_sha"]), {source, destination})
        source_blob, source_mode = gtt.task_commit_tree_path_identity(
            self.root, payload["commit_sha"], source
        )
        self.assertIsNotNone(source_blob)
        self.assertEqual(source_mode, "100644")
        self.assertEqual(
            subprocess.run(
                ["git", "show", f"{payload['commit_sha']}:{source}"],
                cwd=self.root,
                check=True,
                stdout=subprocess.PIPE,
            ).stdout,
            b"reviewed source update\n",
        )
        self.assertNotEqual(
            gtt.task_commit_tree_path_identity(
                self.root, payload["commit_sha"], destination
            ),
            (None, None),
        )

    def test_task_commit_rejects_non_passed_source_exit_before_candidate_generation(self) -> None:
        reviewed = "src/task.txt"
        (self.root / reviewed).write_text("changed\n", encoding="utf-8")
        authoring = self.task_commit_authoring([reviewed])

        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.build_task_commit_candidate(
                self.root,
                self.task_dir,
                self.public_commit_input(source_exit="implementation_required"),
                authoring,
            )

        self.assertIn(
            "does not bind the current passed Phase 2 identity",
            str(raised.exception),
        )
        candidate, _ = gtt.task_commit_prepare_candidate_path(
            self.root,
            self.task_dir,
        )
        self.assertFalse(candidate.exists())

    def test_unrelated_staged_path_blocks_without_unstage(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        (self.root / "unrelated.log").write_text("staged unrelated\n", encoding="utf-8")
        subprocess.run(["git", "add", "unrelated.log"], cwd=self.root, check=True)
        candidate = self.make_plan(1, ["src/task.txt"], ["unrelated.log"])
        before = self.task_commit_entry_state(candidate)
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)
        self.assertIn("unrelated.log", raised.exception.payload["unexpected_staged_paths"])
        self.assertIn("unrelated.log", gtt.git_nul_path_set(self.root, ["diff", "--cached", "--name-only", "--no-renames", "-z"]))
        self.assert_task_commit_entry_state(before, candidate)

    def test_partial_isolated_index_write_preserves_complete_live_index_preimage(self) -> None:
        first = self.root / "src/first.txt"
        second = self.root / "src/second.txt"
        first.write_text("reviewed-one\n", encoding="utf-8")
        second.write_text("reviewed-two\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/first.txt", "src/second.txt"])
        before = self.task_commit_entry_state(candidate)
        original = gtt.stage_task_commit_index_bindings

        def fail_after_one_binding(
            root: Path,
            bindings: dict[str, tuple[str | None, str | None]],
            git_env: dict[str, str],
        ) -> None:
            first_path = sorted(bindings)[0]
            original(root, {first_path: bindings[first_path]}, git_env)
            raise gtt.WorkflowError("controlled partial isolated index failure", exit_code=2)

        with mock.patch.object(
            gtt,
            "stage_task_commit_index_bindings",
            side_effect=fail_after_one_binding,
        ):
            with self.assertRaises(gtt.WorkflowError):
                gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assert_task_commit_entry_state(before, candidate)

    def test_candidate_stale_and_noncanonical_negative_matrix(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])
        original = json.loads(candidate.read_text(encoding="utf-8"))

        def stale_head(plan: dict[str, object]) -> None:
            plan["git"]["pre_commit_head"] = "0" * 40

        def stale_phase2_anchor(plan: dict[str, object]) -> None:
            plan["git"]["phase2_commit_anchor"] = "0" * 40

        def stale_snapshot(plan: dict[str, object]) -> None:
            plan["dirty_snapshot"]["entries"][0]["worktree_sha256"] = "0" * 64

        def wrong_issue(plan: dict[str, object]) -> None:
            message = plan["message"]
            message["subject"] = str(message["subject"]).replace("#122", "#999")

        def wrong_order(plan: dict[str, object]) -> None:
            message = plan["message"]
            body = str(message["body"])
            message["body"] = body.replace("变更：", "TEMP：").replace(
                "边界：", "变更："
            ).replace("TEMP：", "边界：")

        def missing_section(plan: dict[str, object]) -> None:
            message = plan["message"]
            message["body"] = str(message["body"]).replace(
                "\n验证：\n运行 task commit 单元测试。", ""
            )

        def placeholder(plan: dict[str, object]) -> None:
            plan["message"]["background"] = "TODO"

        def close_keyword(plan: dict[str, object]) -> None:
            message = plan["message"]
            message["body"] = str(message["body"]).replace(
                "Refs #122", "Closes #122"
            )

        def add_authorization(plan: dict[str, object]) -> None:
            plan["authorization"] = {"status": "confirmed"}

        def empty_ai_evidence(plan: dict[str, object]) -> None:
            plan["ai_review"]["evidence"] = []

        def unknown_classification(plan: dict[str, object]) -> None:
            plan["path_classifications"][0]["category"] = "unknown"

        mutations = {
            "stale HEAD": stale_head,
            "stale Phase 2 anchor": stale_phase2_anchor,
            "stale snapshot": stale_snapshot,
            "wrong issue": wrong_issue,
            "wrong body order": wrong_order,
            "missing body section": missing_section,
            "placeholder body": placeholder,
            "close keyword": close_keyword,
            "authorization field": add_authorization,
            "empty AI evidence": empty_ai_evidence,
            "unknown classification": unknown_classification,
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                plan = json.loads(json.dumps(original, ensure_ascii=False))
                mutate(plan)
                gtt.write_json(candidate, plan)
                _, _, errors = gtt.validate_task_commit_candidate(self.root, candidate, self.task_dir)
                self.assertTrue(errors, label)

    def test_hook_extra_path_blocks_before_real_publication(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])
        hook = self.root / ".git/hooks/pre-commit"
        hook.write_text("#!/usr/bin/env bash\nset -euo pipefail\necho hook > hook-extra.txt\ngit add hook-extra.txt\n", encoding="utf-8")
        hook.chmod(0o755)
        before = self.task_commit_entry_state(candidate)
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)
        self.assertIn("isolated commit path set", " ".join(raised.exception.payload["errors"]))
        self.assert_task_commit_entry_state(before, candidate)
        self.assertTrue((self.root / "hook-extra.txt").is_file())

    def test_benign_pre_commit_hook_preserves_expected_tree(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])
        hook = self.root / ".git/hooks/pre-commit"
        hook.write_text("#!/usr/bin/env bash\nset -euo pipefail\nexit 0\n", encoding="utf-8")
        hook.chmod(0o755)

        payload = gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertEqual(payload["status"], "committed")
        self.assertEqual(self.committed_paths(payload["commit_sha"]), {"src/task.txt"})
        self.assertEqual(
            gtt.task_commit_write_tree(self.root),
            gtt.task_commit_commit_tree(self.root, payload["commit_sha"]),
        )
        self.assertFalse(candidate.exists())

    def test_failing_pre_commit_hook_preserves_ref_index_and_candidate_preimages(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])
        hook = self.root / ".git/hooks/pre-commit"
        hook.write_text("#!/usr/bin/env bash\nset -euo pipefail\nexit 1\n", encoding="utf-8")
        hook.chmod(0o755)
        before = self.task_commit_entry_state(candidate)

        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertIn("isolated git commit failed", str(raised.exception))
        self.assert_task_commit_entry_state(before, candidate)

    def test_current_candidate_has_semantic_exit_without_result_or_digest_chain(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])
        plan = json.loads(candidate.read_text(encoding="utf-8"))
        self.assertEqual(gtt.task_commit_ai_exit(plan["ai_review"]), "committed")
        encoded = json.dumps(plan, ensure_ascii=False, sort_keys=True)
        for forbidden in (
            '"authorization"',
            '"human_authorization"',
            '"freshness"',
            '"result"',
            '"check_ref"',
            '"sha256"',
        ):
            self.assertNotIn(forbidden, encoded)

    def test_same_path_hook_content_restage_never_publishes_unreviewed_tree(self) -> None:
        (self.root / "src/task.txt").write_text("reviewed-change\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])
        pre_commit_head = gtt.current_head(self.root)
        hook = self.root / ".git/hooks/pre-commit"
        hook.write_text(
            "#!/usr/bin/env bash\nset -euo pipefail\n"
            "printf 'hook-mutated\\n' > src/task.txt\n"
            "git --literal-pathspecs add -- src/task.txt\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)
        before = self.task_commit_entry_state(candidate)

        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertEqual(pre_commit_head, before["head"])
        self.assertIn("isolated commit tree", " ".join(raised.exception.payload["errors"]))
        self.assert_task_commit_entry_state(before, candidate)
        self.assertEqual((self.root / "src/task.txt").read_text(encoding="utf-8"), "hook-mutated\n")

    def test_same_path_hook_mode_restage_never_publishes_unreviewed_mode(self) -> None:
        (self.root / "src/task.txt").write_text("reviewed-change\n", encoding="utf-8")
        candidate = self.make_plan(1, ["src/task.txt"])
        hook = self.root / ".git/hooks/pre-commit"
        hook.write_text(
            "#!/usr/bin/env bash\nset -euo pipefail\n"
            "chmod +x src/task.txt\n"
            "git --literal-pathspecs add -- src/task.txt\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)
        before = self.task_commit_entry_state(candidate)

        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.execute_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertIn("isolated commit tree", " ".join(raised.exception.payload["errors"]))
        self.assert_task_commit_entry_state(before, candidate)
        self.assertTrue((self.root / "src/task.txt").stat().st_mode & stat.S_IXUSR)

    def test_private_candidate_is_single_use_and_next_candidate_restarts_runtime_sequence(self) -> None:
        (self.root / "src/task.txt").write_text("first\n", encoding="utf-8")
        first = self.make_plan(1, ["src/task.txt"])
        gtt.execute_task_commit_candidate(self.root, first, self.task_dir)
        with self.assertRaises(gtt.WorkflowError):
            gtt.execute_task_commit_candidate(self.root, first, self.task_dir)

        (self.root / "src/task.txt").write_text("second\n", encoding="utf-8")
        second = self.make_plan(1, ["src/task.txt"])
        plan, facts, errors = gtt.validate_task_commit_candidate(self.root, second, self.task_dir)
        self.assertEqual(errors, [])
        self.assertEqual(plan["sequence"], "001")
        self.assertEqual(facts["pre_commit_head"], gtt.current_head(self.root))

    def test_sequence_must_be_next_unused(self) -> None:
        (self.root / "src/task.txt").write_text("changed\n", encoding="utf-8")
        candidate = self.make_plan(2, ["src/task.txt"])

        _, _, errors = gtt.validate_task_commit_candidate(self.root, candidate, self.task_dir)

        self.assertTrue(any("only contiguous private sequence" in error for error in errors))


class BaseSyncRuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.remote = self.base / "remote.git"
        self.seed = self.base / "seed"
        self.local = self.base / "local"
        subprocess.run(
            ["git", "init", "--bare", str(self.remote)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["git", "init", "-b", "main", str(self.seed)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.git(self.seed, "config", "user.email", "test@example.com")
        self.git(self.seed, "config", "user.name", "Test User")
        (self.seed / "README.md").write_text("one\n", encoding="utf-8")
        config = self.seed / ".trellis/guru-team/config.yml"
        config.parent.mkdir(parents=True)
        config.write_text(
            "base_branch: main\nbase_branch_candidates: [dev, develop, main, master]\n",
            encoding="utf-8",
        )
        schema_source = (
            Path(__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages/guru-sync-base/schemas/base-sync-result.schema.json"
        )
        schema_target = (
            self.seed
            / ".trellis/guru-team/skills/packages/guru-sync-base/schemas/base-sync-result.schema.json"
        )
        schema_target.parent.mkdir(parents=True)
        shutil.copy2(schema_source, schema_target)
        self.git(self.seed, "add", ".")
        self.git(self.seed, "commit", "-qm", "initial")
        self.git(self.seed, "remote", "add", "origin", str(self.remote))
        self.git(self.seed, "push", "-u", "origin", "main")
        self.git(self.remote, "symbolic-ref", "HEAD", "refs/heads/main")
        subprocess.run(
            ["git", "clone", str(self.remote), str(self.local)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.git(self.local, "config", "user.email", "test@example.com")
        self.git(self.local, "config", "user.name", "Test User")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def git(self, cwd: Path, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout.strip()

    def sync_args(self, **overrides: object) -> argparse.Namespace:
        values: dict[str, object] = {
            "root": str(self.local),
            "json": True,
            "mode": "standalone",
            "resolve_only": True,
            "execute": False,
            "base": None,
            "remote": "origin",
            "expected_resolution_sha256": None,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def check_args(self, **overrides: object) -> argparse.Namespace:
        values: dict[str, object] = {
            "root": str(self.local),
            "json": True,
            "mode": "standalone",
            "result_json": None,
            "expected_resolution_sha256": None,
            "record_skipped": None,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def resolve(self, *, base: str | None = None) -> dict[str, object]:
        return gtt.cmd_sync_base(self.sync_args(base=base))

    def execute(
        self,
        resolution: dict[str, object],
        *,
        base: str | None = None,
        remote: str = "origin",
    ) -> dict[str, object]:
        return gtt.cmd_sync_base(
            self.sync_args(
                resolve_only=False,
                execute=True,
                base=base,
                remote=remote,
                expected_resolution_sha256=resolution["resolution_sha256"],
            )
        )

    def validate(self, result: dict[str, object]) -> dict[str, object]:
        resolution = result["resolution"]
        assert isinstance(resolution, dict)
        return gtt.cmd_check_base_sync(
            self.check_args(
                result_json=result,
                expected_resolution_sha256=resolution["resolution_sha256"],
            )
        )

    def advance_remote(self, text: str = "two\n") -> str:
        (self.seed / "README.md").write_text(text, encoding="utf-8")
        self.git(self.seed, "commit", "-am", f"update-{text.strip()}")
        self.git(self.seed, "push", "origin", "main")
        return self.git(self.seed, "rev-parse", "HEAD")

    def test_resolver_precedence_is_explicit_scalar_ordered_candidate_then_remote_default(self) -> None:
        explicit = gtt.resolve_base_selection(
            self.local,
            {"base_branch": 7, "base_branch_candidates": "not-a-list"},
            "release",
        )
        self.assertEqual((explicit["source"], explicit["selected_base"]), ("explicit", "release"))

        scalar = gtt.resolve_base_selection(
            self.local,
            {"base_branch": "develop", "base_branch_candidates": "not-a-list"},
        )
        self.assertEqual((scalar["source"], scalar["selected_base"]), ("config", "develop"))

        self.git(self.local, "branch", "dev")
        ordered = gtt.resolve_base_selection(
            self.local,
            {"base_branch": "", "base_branch_candidates": ["dev", "main"]},
        )
        self.assertEqual(
            (ordered["source"], ordered["selected_base"]),
            ("config-candidate", "dev"),
        )

        self.git(self.local, "branch", "-D", "dev")
        remote_default = gtt.resolve_base_selection(
            self.local,
            {"base_branch": "", "base_branch_candidates": ["develop", "master"]},
        )
        self.assertEqual(
            (remote_default["source"], remote_default["selected_base"]),
            ("remote-default", "main"),
        )

    def test_ordered_candidates_choose_first_existing_without_ambiguity(self) -> None:
        cases = [
            (["dev", "main"], ["dev"], "dev"),
            (["develop", "main"], ["develop"], "develop"),
            (["main", "master"], ["master"], "main"),
            (["main", "dev"], ["dev"], "main"),
        ]
        for index, (candidates, create, expected) in enumerate(cases):
            with self.subTest(index=index, candidates=candidates):
                for branch in ("dev", "develop", "master"):
                    subprocess.run(
                        ["git", "branch", "-D", branch],
                        cwd=self.local,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        check=False,
                    )
                for branch in create:
                    self.git(self.local, "branch", branch)
                resolution = gtt.resolve_base_selection(
                    self.local,
                    {"base_branch": "", "base_branch_candidates": candidates},
                )
                self.assertEqual(resolution["source"], "config-candidate")
                self.assertEqual(resolution["selected_base"], expected)

    def test_candidate_dedup_custom_order_and_blocked_fallback(self) -> None:
        self.git(self.local, "branch", "dev")
        resolution = gtt.resolve_base_selection(
            self.local,
            {"base_branch": "", "base_branch_candidates": ["main", "dev", "main"]},
        )
        self.assertEqual(resolution["candidates"], ["main", "dev"])
        self.assertEqual(resolution["selected_base"], "main")

        with mock.patch.object(gtt, "remote_default_branch", return_value=None):
            with self.assertRaises(gtt.WorkflowError) as blocked:
                gtt.resolve_base_selection(
                    self.local,
                    {"base_branch": "", "base_branch_candidates": ["ghost", "missing"]},
                )
        self.assertEqual(blocked.exception.payload["source"], "blocked")

    def test_resolve_execute_validate_use_stdout_facts_and_digests(self) -> None:
        resolution = self.resolve()
        self.assertEqual(resolution["source"], "config")
        self.assertEqual(
            resolution["resolution_sha256"],
            gtt.canonical_json_sha256({
                key: value
                for key, value in resolution.items()
                if key != "resolution_sha256"
            }),
        )
        result = self.execute(resolution)
        self.assertTrue(result["fresh"])
        self.assertEqual(
            result["resolution"]["resolution_sha256"],
            result["post_sync_resolution_sha256"],
        )
        self.assertEqual(
            result["post_sync_resolution_sha256"],
            gtt.canonical_json_sha256(result["post_sync_resolution"]),
        )
        self.assertEqual(
            result["decision_checkout"]["head_after"],
            result["git"]["remote_head_after"],
        )
        validated = self.validate(result)
        self.assertEqual(validated["status"], "validated")
        self.assertEqual(validated["facts_sha256"], result["facts_sha256"])
        self.assertEqual(
            validated["post_sync_resolution_sha256"],
            result["post_sync_resolution_sha256"],
        )
        self.assertFalse(any(path.name in {"resolution.json", "result.json"} for path in self.base.iterdir()))

    def test_prepare_base_assertion_preserves_reviewed_resolution_source_and_digest(self) -> None:
        issue = {
            "number": 110,
            "url": "https://github.com/owner/repo/issues/110",
            "title": "Add reusable base synchronization skill",
            "body": "Keep prepare base assertions source preserving.",
        }
        cases = [
            (
                "config-scalar",
                {"base_branch": "main", "base_branch_candidates": ["dev", "main"]},
                None,
                "config",
            ),
            (
                "config-candidate-single",
                {"base_branch": "", "base_branch_candidates": ["main"]},
                None,
                "config-candidate",
            ),
            (
                "remote-default",
                {"base_branch": "", "base_branch_candidates": ["missing"]},
                None,
                "remote-default",
            ),
            (
                "explicit",
                {"base_branch": 7, "base_branch_candidates": "not-a-list"},
                "main",
                "explicit",
            ),
        ]

        for name, base_config, explicit, expected_source in cases:
            with self.subTest(name=name):
                config = {
                    **gtt.DEFAULTS,
                    **base_config,
                    "github_repo": "owner/repo",
                }
                reviewed = gtt.resolve_base_selection(
                    self.local,
                    config,
                    explicit,
                )
                with (
                    mock.patch.object(gtt, "load_config", return_value=config),
                    mock.patch.object(gtt, "require_tool"),
                    mock.patch.object(gtt, "require_gh_auth"),
                    mock.patch.object(gtt, "issue_view", return_value=issue),
                ):
                    payload = gtt.cmd_prepare(
                        prepare_args(
                            root=str(self.local),
                            requirement=["#110"],
                            base_branch="main",
                            expected_resolution_sha256=reviewed["resolution_sha256"],
                        )
                    )

                preserved = payload["base_freshness"]["resolution"]
                self.assertEqual(preserved["source"], expected_source)
                self.assertEqual(preserved["selected_base"], "main")
                self.assertEqual(
                    preserved["resolution_sha256"],
                    reviewed["resolution_sha256"],
                )
                self.assertEqual(
                    payload["base_freshness"]["reviewed_resolution_sha256"],
                    reviewed["resolution_sha256"],
                )

    def test_prepare_base_assertion_mismatch_and_digest_drift_block_before_fetch(self) -> None:
        config = {"base_branch": "main", "base_branch_candidates": ["main"]}
        reviewed = gtt.resolve_base_selection(self.local, config)
        calls: list[list[str]] = []
        original_run = gtt.run

        def recording_run(cmd: list[str], *args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
            calls.append(cmd)
            return original_run(cmd, *args, **kwargs)

        with (
            mock.patch.object(gtt, "load_config", return_value=config),
            mock.patch.object(gtt, "run", side_effect=recording_run),
            self.assertRaises(gtt.WorkflowError) as mismatch,
        ):
            gtt.ensure_base_freshness(
                self.local,
                "develop",
                expected_resolution_sha256=reviewed["resolution_sha256"],
            )
        self.assertIn("assertion does not match", str(mismatch.exception))
        self.assertFalse(any(command[:2] == ["git", "fetch"] for command in calls))

        calls.clear()
        with (
            mock.patch.object(
                gtt,
                "load_config",
                return_value={"base_branch": "develop", "base_branch_candidates": ["main"]},
            ),
            mock.patch.object(gtt, "run", side_effect=recording_run),
            self.assertRaises(gtt.WorkflowError) as drift,
        ):
            gtt.ensure_base_freshness(
                self.local,
                "main",
                expected_resolution_sha256=reviewed["resolution_sha256"],
            )
        self.assertIn("digest changed", str(drift.exception))
        self.assertFalse(any(command[:2] == ["git", "fetch"] for command in calls))

    def test_prepare_base_assertion_checkout_drift_blocks_before_fetch(self) -> None:
        config = {"base_branch": "main", "base_branch_candidates": ["main"]}
        reviewed = gtt.resolve_base_selection(self.local, config)
        remote_ref = "refs/remotes/origin/main"
        remote_tracking_before = self.git(self.local, "rev-parse", remote_ref)
        self.git(self.local, "checkout", "-qb", "feature")
        calls: list[list[str]] = []
        original_run = gtt.run

        def recording_run(cmd: list[str], *args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
            calls.append(cmd)
            return original_run(cmd, *args, **kwargs)

        with (
            mock.patch.object(gtt, "load_config", return_value=config),
            mock.patch.object(gtt, "run", side_effect=recording_run),
            self.assertRaises(gtt.WorkflowError) as drift,
        ):
            gtt.ensure_base_freshness(
                self.local,
                "main",
                expected_resolution_sha256=reviewed["resolution_sha256"],
            )

        self.assertIn("digest changed", str(drift.exception))
        self.assertFalse(any(command[:2] == ["git", "fetch"] for command in calls))
        self.assertEqual(
            self.git(self.local, "rev-parse", remote_ref),
            remote_tracking_before,
        )

    def test_execute_fast_forwards_only_selected_base_checkout(self) -> None:
        resolution = self.resolve()
        remote_head = self.advance_remote()
        result = self.execute(resolution)
        self.assertTrue(result["git"]["fast_forwarded"])
        self.assertNotEqual(
            result["resolution"]["resolution_sha256"],
            result["post_sync_resolution_sha256"],
        )
        self.assertEqual(result["post_sync_resolution"]["decision_checkout"]["head"], remote_head)
        self.assertEqual(self.git(self.local, "rev-parse", "HEAD"), remote_head)

        self.git(self.local, "checkout", "-qb", "feature")
        explicit = self.resolve(base="main")
        self.advance_remote("three\n")
        with self.assertRaises(gtt.WorkflowError) as raised:
            self.execute(explicit, base="main")
        self.assertIn("not on that base", str(raised.exception))

    def test_behind_sync_validator_digest_feeds_prepare_and_pre_sync_digest_is_stale(self) -> None:
        resolution = self.resolve()
        remote_head = self.advance_remote()
        result = self.execute(resolution)
        validated = self.validate(result)
        post_digest = str(validated["post_sync_resolution_sha256"])

        calls: list[list[str]] = []
        original_run = gtt.run

        def recording_run(cmd: list[str], *args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
            calls.append(cmd)
            return original_run(cmd, *args, **kwargs)

        with (
            mock.patch.object(gtt, "run", side_effect=recording_run),
            self.assertRaises(gtt.WorkflowError) as stale,
        ):
            gtt.ensure_base_freshness(
                self.local,
                "main",
                expected_resolution_sha256=str(resolution["resolution_sha256"]),
            )
        self.assertIn("digest changed", str(stale.exception))
        self.assertFalse(any(command[:2] == ["git", "fetch"] for command in calls))

        issue = {
            "number": 110,
            "url": "https://github.com/owner/repo/issues/110",
            "title": "Add reusable base synchronization skill",
            "body": "Reuse the synchronized base identity.",
        }
        config = {
            **gtt.DEFAULTS,
            "base_branch": "main",
            "base_branch_candidates": ["dev", "develop", "main", "master"],
            "github_repo": "owner/repo",
        }
        with (
            mock.patch.object(gtt, "load_config", return_value=config),
            mock.patch.object(gtt, "require_tool"),
            mock.patch.object(gtt, "require_gh_auth"),
            mock.patch.object(gtt, "issue_view", return_value=issue),
        ):
            payload = gtt.cmd_prepare(
                prepare_args(
                    root=str(self.local),
                    requirement=["#110"],
                    base_branch="main",
                    expected_resolution_sha256=post_digest,
                )
            )

        self.assertEqual(payload["base_freshness"]["reviewed_resolution_sha256"], post_digest)
        self.assertEqual(
            payload["base_freshness"]["post_sync_resolution_sha256"],
            post_digest,
        )
        self.assertEqual(payload["base_freshness"]["remote_head"], remote_head)

    def test_resolve_blocks_dirty_and_missing_local_base(self) -> None:
        (self.local / "dirty.txt").write_text("dirty\n", encoding="utf-8")
        with self.assertRaises(gtt.WorkflowError) as dirty:
            self.resolve()
        self.assertIn("not clean", " ".join(dirty.exception.payload["errors"]))
        (self.local / "dirty.txt").unlink()

        self.git(self.local, "checkout", "-qb", "feature")
        self.git(self.local, "branch", "-D", "main")
        with self.assertRaises(gtt.WorkflowError) as missing:
            self.resolve(base="main")
        self.assertIn("does not exist", " ".join(missing.exception.payload["errors"]))

    def test_execute_recomputes_resolution_and_blocks_digest_drift_before_fetch(self) -> None:
        resolution = self.resolve()
        self.git(self.local, "branch", "develop")
        calls: list[list[str]] = []
        original_run = gtt.run

        def recording_run(cmd: list[str], *args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
            calls.append(cmd)
            return original_run(cmd, *args, **kwargs)

        with (
            mock.patch.object(
                gtt,
                "load_config",
                return_value={"base_branch": "develop", "base_branch_candidates": ["develop"]},
            ),
            mock.patch.object(gtt, "run", side_effect=recording_run),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            self.execute(resolution)
        self.assertIn("digest changed", str(raised.exception))
        self.assertFalse(any(command[:2] == ["git", "fetch"] for command in calls))

    def test_execute_rejects_decision_checkout_drift_before_remote_tracking_mutation(self) -> None:
        resolution = self.resolve()
        remote_ref = "refs/remotes/origin/main"
        remote_tracking_before = self.git(self.local, "rev-parse", remote_ref)
        self.advance_remote()
        self.git(self.local, "checkout", "-qb", "feature")
        calls: list[list[str]] = []
        original_run = gtt.run

        def recording_run(cmd: list[str], *args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
            calls.append(cmd)
            return original_run(cmd, *args, **kwargs)

        with (
            mock.patch.object(gtt, "run", side_effect=recording_run),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            self.execute(resolution)

        self.assertIn("digest changed", str(raised.exception))
        self.assertFalse(any(command[:2] == ["git", "fetch"] for command in calls))
        self.assertEqual(
            self.git(self.local, "rev-parse", remote_ref),
            remote_tracking_before,
        )

    def test_execute_blocks_divergence_fetch_failure_and_post_sync_mismatch(self) -> None:
        resolution = self.resolve()
        (self.local / "local.txt").write_text("local\n", encoding="utf-8")
        self.git(self.local, "add", "local.txt")
        self.git(self.local, "commit", "-qm", "local divergence")
        self.advance_remote()
        diverged_resolution = self.resolve()
        with self.assertRaises(gtt.WorkflowError) as diverged:
            self.execute(diverged_resolution)
        self.assertIn("diverged", str(diverged.exception))

        self.git(self.local, "reset", "--hard", resolution["decision_checkout"]["head"])
        clean_resolution = self.resolve()
        self.git(self.local, "remote", "set-url", "origin", str(self.base / "missing.git"))
        with self.assertRaises(gtt.WorkflowError) as fetch_failed:
            self.execute(clean_resolution)
        self.assertIn("fetch failed", str(fetch_failed.exception))

        self.git(self.local, "remote", "set-url", "origin", str(self.remote))
        mismatch_resolution = self.resolve()
        real_ref_head = gtt.ref_head
        remote_reads = 0

        def drifting_ref_head(root: Path, ref: str) -> str | None:
            nonlocal remote_reads
            value = real_ref_head(root, ref)
            if ref == "refs/remotes/origin/main":
                remote_reads += 1
                if remote_reads == 2:
                    return "f" * 40
            return value

        with (
            mock.patch.object(gtt, "ref_head", side_effect=drifting_ref_head),
            self.assertRaises(gtt.WorkflowError) as mismatch,
        ):
            self.execute(mismatch_resolution)
        self.assertIn("did not prove", str(mismatch.exception))

    def test_validator_rejects_tamper_digest_mismatch_and_live_git_drift(self) -> None:
        resolution = self.resolve()
        result = self.execute(resolution)

        tampered = copy.deepcopy(result)
        tampered["fresh"] = False
        with self.assertRaises(gtt.WorkflowError):
            self.validate(tampered)

        tampered_checkout = copy.deepcopy(result)
        tampered_checkout["decision_checkout"]["head_before"] = "f" * 40
        unsigned = dict(tampered_checkout)
        unsigned.pop("facts_sha256")
        tampered_checkout["facts_sha256"] = gtt.canonical_json_sha256(unsigned)
        with self.assertRaises(gtt.WorkflowError) as checkout_digest:
            self.validate(tampered_checkout)
        self.assertIn(
            "resolution digest is invalid",
            " ".join(checkout_digest.exception.payload["errors"]),
        )

        tampered_post = copy.deepcopy(result)
        tampered_post["post_sync_resolution"]["decision_checkout"]["head"] = "f" * 40
        unsigned = dict(tampered_post)
        unsigned.pop("facts_sha256")
        tampered_post["facts_sha256"] = gtt.canonical_json_sha256(unsigned)
        with self.assertRaises(gtt.WorkflowError) as post_digest:
            self.validate(tampered_post)
        self.assertIn(
            "post-sync resolution",
            " ".join(post_digest.exception.payload["errors"]),
        )

        with self.assertRaises(gtt.WorkflowError) as digest_mismatch:
            gtt.cmd_check_base_sync(
                self.check_args(
                    result_json=result,
                    expected_resolution_sha256="f" * 64,
                )
            )
        self.assertIn("does not match", str(digest_mismatch.exception))

        (self.local / "untracked.txt").write_text("drift\n", encoding="utf-8")
        with self.assertRaises(gtt.WorkflowError) as stale:
            self.validate(result)
        self.assertIn("not clean", " ".join(stale.exception.payload["errors"]))

    def test_invalid_branch_missing_remote_and_skipped_route_fail_closed(self) -> None:
        with self.assertRaises(gtt.WorkflowError) as invalid:
            self.resolve(base="-invalid")
        self.assertIn("valid Git branch", str(invalid.exception))

        missing_remote = gtt.cmd_sync_base(self.sync_args(base="main", remote="missing"))
        with self.assertRaises(gtt.WorkflowError) as failed:
            self.execute(missing_remote, base="main", remote="missing")
        self.assertIn("fetch failed", str(failed.exception))

        skipped = gtt.cmd_check_base_sync(
            self.check_args(
                mode="workflow",
                record_skipped="original-request-route",
            )
        )
        self.assertEqual(skipped["status"], "skipped")
        unsigned = dict(skipped)
        digest = unsigned.pop("facts_sha256")
        self.assertEqual(digest, gtt.canonical_json_sha256(unsigned))
        with self.assertRaises(gtt.WorkflowError):
            gtt.cmd_check_base_sync(
                self.check_args(record_skipped="original-request-route")
            )


class PrepareSideEffectBoundaryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".trellis").mkdir()
        (self.root / ".trellis/.developer").write_text(
            "name=tester\ninitialized_at=2026-07-04T00:00:00\n",
            encoding="utf-8",
        )

        self.real_ensure_base_freshness = gtt.ensure_base_freshness
        self.patches = [
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={
                **gtt.DEFAULTS,
                "github_repo": "owner/repo",
                "runtime_root": ".trellis/.runtime/guru-team",
            }),
            mock.patch.object(gtt, "require_tool"),
            mock.patch.object(gtt, "require_gh_auth"),
            mock.patch.object(gtt, "duplicate_search", return_value=[]),
            mock.patch.object(gtt, "resolve_base_branch", return_value=("main", ["main", "origin/main"])),
            mock.patch.object(
                gtt,
                "ensure_base_freshness",
                side_effect=lambda *_args, **_kwargs: fresh_base_sync_projection(),
            ),
        ]
        for patcher in self.patches:
            patcher.start()

    def tearDown(self) -> None:
        for patcher in reversed(self.patches):
            patcher.stop()
        self.tmp.cleanup()

    def test_freeform_prepare_outputs_proposal_without_side_effects(self) -> None:
        with (
            mock.patch.object(gtt, "create_issue") as create_issue,
            mock.patch.object(gtt, "run_stdout") as run_stdout,
        ):
            payload = gtt.cmd_prepare(prepare_args())

        create_issue.assert_not_called()
        run_stdout.assert_not_called()
        self.assertIsNone(payload["source_issue"])
        for retired_field in (
            "requires_confirmation",
            "create_issue_command",
            "create_task_command",
            "workspace_mode",
            "workspace_path",
            "workspace_ready",
            "preflight",
            "issue_scope_ledger",
            "task_dir",
        ):
            self.assertNotIn(retired_field, payload)
        self.assertFalse((self.root / ".trellis/.runtime/guru-team").exists())
        self.assertFalse((self.root / ".trellis/tasks").exists())
        self.assertEqual(payload["proposed_issue"]["title"], "Add default side-effect-free intake planning for freeform requests")
        issue_draft = payload["proposed_issue"]["body"]
        for retired_phrase in (
            "## Handoff",
            "## 交接",
            "requires confirmation",
            "需要用户确认",
            "请复述",
            "repeat the digest",
        ):
            self.assertNotIn(retired_phrase, issue_draft)

    def test_prepare_english_issue_title_passes_automatic_naming_quality(self) -> None:
        existing_issue = {
            "number": 52,
            "url": "https://github.com/owner/repo/issues/52",
            "title": "Add resume detail inline attachment preview",
        }
        with mock.patch.object(gtt, "issue_view", return_value=existing_issue):
            payload = gtt.cmd_prepare(prepare_args(requirement=["#52"]))

        self.assertTrue(payload["naming_quality"]["ok"])
        self.assertFalse(payload["naming_quality"]["requires_semantic_name"])
        self.assertEqual(payload["task_slug"], "52-resume-detail-inline-attachment-preview")
        self.assertEqual(payload["workspace_slug"], "52-resume-detail-inline-attachment-preview")
        self.assertEqual(payload["branch_name"], "feat/52-resume-detail-inline-attachment-preview")

    def test_prepare_infers_all_supported_branch_types(self) -> None:
        cases = {
            "feat": "feat: support semantic branch type inference",
            "fix": "Fix broken prepare task naming failure",
            "refactor": "Refactor prepare naming helper structure",
            "perf": "Optimize prepare task performance",
            "test": "Add tests for prepare task branch inference",
            "docs": "[docs] update README documentation",
            "style": "Format lint output for scripts",
            "build": "Update package dependency build metadata",
            "ci": "type=ci update GitHub Actions workflow",
            "chore": "Maintenance housekeeping for intake scripts",
            "revert": "Rollback previous branch naming change",
        }
        args = prepare_args(short_name="052-semantic-business-name")

        for expected_type, source_text in cases.items():
            with self.subTest(expected_type=expected_type):
                payload = gtt.prepare_naming_payload(args, gtt.DEFAULTS, "52", source_text)
                self.assertEqual(payload["branch_name"], f"{expected_type}/052-semantic-business-name")

    def test_prepare_unknown_branch_type_falls_back_to_chore(self) -> None:
        payload = gtt.prepare_naming_payload(
            prepare_args(short_name="052-semantic-business-name"),
            gtt.DEFAULTS,
            "52",
            "Synchronize semantic business capability",
        )

        self.assertEqual(payload["branch_name"], "chore/052-semantic-business-name")

    def test_prepare_issue_body_participates_in_branch_type_inference(self) -> None:
        existing_issue = {
            "number": 52,
            "url": "https://github.com/owner/repo/issues/52",
            "title": "Update Guru Team workflow behavior",
            "body": "Docs: update README and workflow documentation.",
        }
        with mock.patch.object(gtt, "issue_view", return_value=existing_issue):
            payload = gtt.cmd_prepare(prepare_args(requirement=["#52"]))

        self.assertEqual(payload["branch_name"], "docs/52-update-guru-team-workflow-behavior")

    def test_prepare_branch_type_catalog_in_issue_body_does_not_pollute_inference(self) -> None:
        branch_type_catalog = (
            "合法分支类型为 feat, fix, refactor, perf, test, docs, style, build, ci, chore, revert."
        )
        payload = gtt.prepare_naming_payload(
            prepare_args(short_name="052-semantic-business-name"),
            gtt.DEFAULTS,
            "52",
            "Synchronize semantic business capability",
            f"Synchronize semantic business capability\n{branch_type_catalog}",
        )

        self.assertEqual(payload["branch_name"], "chore/052-semantic-business-name")

    def test_prepare_generated_issue_body_duplicate_list_does_not_pollute_inference(self) -> None:
        generated_body = gtt.issue_body(
            "Synchronize semantic business capability",
            [
                {
                    "number": 7,
                    "title": "Fix broken workflow bug",
                    "similarity": "low",
                    "url": "https://github.com/owner/repo/issues/7",
                }
            ],
        )
        payload = gtt.prepare_naming_payload(
            prepare_args(short_name="052-semantic-business-name"),
            gtt.DEFAULTS,
            "52",
            "Synchronize semantic business capability",
            f"Synchronize semantic business capability\n{generated_body}",
        )

        self.assertEqual(payload["branch_name"], "chore/052-semantic-business-name")

    def test_prepare_workflow_keyword_alone_does_not_infer_ci(self) -> None:
        payload = gtt.prepare_naming_payload(
            prepare_args(short_name="052-semantic-business-name"),
            gtt.DEFAULTS,
            "52",
            "Update Guru Team workflow contract",
        )

        self.assertEqual(payload["branch_name"], "chore/052-semantic-business-name")

    def test_prepare_github_workflows_path_infers_ci(self) -> None:
        payload = gtt.prepare_naming_payload(
            prepare_args(short_name="052-semantic-business-name"),
            gtt.DEFAULTS,
            "52",
            "Update .github/workflows release automation",
        )

        self.assertEqual(payload["branch_name"], "ci/052-semantic-business-name")

    def test_prepare_explicit_branch_preserves_custom_value(self) -> None:
        payload = gtt.prepare_naming_payload(
            prepare_args(branch="custom/slug"),
            gtt.DEFAULTS,
            "52",
            "Fix broken prepare task naming",
        )

        self.assertEqual(payload["branch_name"], "custom/slug")

    def test_prepare_planner_uses_shared_sync_before_issue_read(self) -> None:
        existing_issue = {
            "number": 52,
            "url": "https://github.com/owner/repo/issues/52",
            "title": "Add resume detail inline attachment preview",
        }
        freshness = fresh_base_sync_projection("d" * 40)
        order: list[str] = []
        with (
            mock.patch.object(
                gtt, "issue_view", side_effect=lambda *_args: order.append("issue") or existing_issue
            ),
            mock.patch.object(
                gtt, "require_gh_auth", side_effect=lambda *_args: order.append("gh-auth")
            ),
            mock.patch.object(
                gtt,
                "ensure_base_freshness",
                side_effect=lambda *_args, **_kwargs: order.append("sync") or freshness,
            ) as ensure_base_freshness,
        ):
            payload = gtt.cmd_prepare(prepare_args(requirement=["#52"]))

        ensure_base_freshness.assert_called_once_with(
            self.root,
            None,
            expected_resolution_sha256="b" * 64,
        )
        self.assertEqual(order, ["sync", "gh-auth", "issue"])
        self.assertEqual(payload["base_freshness"]["fetch_performed"], True)
        self.assertEqual(payload["base_freshness"]["fast_forwarded"], False)
        self.assertEqual(payload["base_freshness"]["status"], "fresh")
        self.assertTrue(payload["base_freshness"]["three_way_equal"])

    def test_prepare_chinese_issue_title_marks_naming_quality_without_side_effects(self) -> None:
        existing_issue = {
            "number": 52,
            "url": "https://github.com/owner/repo/issues/52",
            "title": "简历详情页的原始简历查看功能应该强化",
        }
        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "run_stdout") as run_stdout,
        ):
            payload = gtt.cmd_prepare(prepare_args(requirement=["#52"]))

        run_stdout.assert_not_called()
        self.assertFalse(payload["naming_quality"]["ok"])
        self.assertTrue(payload["naming_quality"]["requires_semantic_name"])
        self.assertEqual(payload["naming_quality"]["current_slug"], "issue-52")
        suggested_flags = " ".join(payload["naming_quality"]["suggested_override_flags"])
        self.assertIn("--short-name", suggested_flags)
        self.assertIn("--branch chore/052-semantic-business-name", suggested_flags)
        self.assertNotIn("--branch codex/", suggested_flags)
        self.assertEqual(payload["task_slug"], "52-issue-52")
        self.assertNotIn("workspace_ready", payload)

    def test_prepare_mixed_non_ascii_title_requires_explicit_semantic_name(self) -> None:
        existing_issue = {
            "number": 52,
            "url": "https://github.com/owner/repo/issues/52",
            "title": "强化 resume detail inline attachment preview",
        }
        with mock.patch.object(gtt, "issue_view", return_value=existing_issue):
            payload = gtt.cmd_prepare(prepare_args(requirement=["#52"]))

        self.assertFalse(payload["naming_quality"]["ok"])
        self.assertTrue(payload["naming_quality"]["requires_semantic_name"])
        self.assertIn("non-ASCII", payload["naming_quality"]["reason"])
        self.assertEqual(payload["task_slug"], "52-resume-detail-inline-attachment-preview")

    def test_high_duplicate_payload_requires_one_real_target_choice(self) -> None:
        duplicate = {
            "number": 6,
            "title": "Existing duplicate",
            "url": "https://github.com/owner/repo/issues/6",
            "similarity": "high",
        }
        with (
            mock.patch.object(gtt, "duplicate_search", return_value=[duplicate]),
            mock.patch.object(
                gtt,
                "ensure_base_freshness",
                return_value=fresh_base_sync_projection(
                    post_sync_resolution_sha256="d" * 64,
                ),
            ),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_prepare(prepare_args())

        payload = raised.exception.payload
        self.assertEqual(payload["duplicates"], [duplicate])
        self.assertEqual(payload["proposed_issue"]["title"], "Add default side-effect-free intake planning for freeform requests")
        self.assertNotIn("create_issue_command", payload["proposed_issue"])
        self.assertNotIn("requires_confirmation", payload)
        self.assertEqual(
            payload["choice_required"],
            {
                "id": "reuse_issue_or_force_new",
                "options": ["reuse_issue", "force_new"],
                "reason": "High-similarity duplicate candidates require one real target choice.",
            },
        )

    def test_ensure_base_freshness_adapter_uses_shared_core(self) -> None:
        result = fresh_base_sync_result()
        with (
            mock.patch.object(gtt, "resolve_base_selection", return_value={"selected_base": "main"}) as resolve,
            mock.patch.object(gtt, "execute_base_sync", return_value=result) as execute,
        ):
            payload = self.real_ensure_base_freshness(self.root, "main")

        resolve.assert_called_once_with(self.root, mock.ANY, "main", "origin")
        execute.assert_called_once_with(self.root, {"selected_base": "main"})
        self.assertTrue(payload["fresh"])
        self.assertTrue(payload["three_way_equal"])
        self.assertEqual(payload["base_ref_for_worktree"], "main")

    def test_ensure_base_freshness_rejects_diverged_base(self) -> None:
        with (
            mock.patch.object(gtt, "resolve_base_selection", return_value={"selected_base": "main"}),
            mock.patch.object(
                gtt,
                "execute_base_sync",
                side_effect=gtt.WorkflowError("Local selected base diverged from the fetched remote base.", exit_code=2),
            ),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            self.real_ensure_base_freshness(self.root, "main")

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("diverged", str(raised.exception))

    def test_ensure_base_freshness_fetches_remote_tracking_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            remote = tmp_path / "remote.git"
            seed = tmp_path / "seed"
            local = tmp_path / "local"
            subprocess.run(["git", "init", "--bare", str(remote)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "init", "-b", "main", str(seed)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=seed, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=seed, check=True)
            (seed / "README.md").write_text("one\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=seed, check=True)
            subprocess.run(["git", "commit", "-m", "one"], cwd=seed, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=seed, check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], cwd=seed, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "clone", str(remote), str(local)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=local, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=local, check=True)

            (seed / "README.md").write_text("two\n", encoding="utf-8")
            subprocess.run(["git", "commit", "-am", "two"], cwd=seed, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "push", "origin", "main"], cwd=seed, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            remote_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=seed, text=True).strip()

            payload = self.real_ensure_base_freshness(local, "main")

            self.assertTrue(payload["fetch_performed"])
            self.assertTrue(payload["fast_forwarded"])
            self.assertTrue(payload["fresh"])
            self.assertEqual(payload["remote_head"], remote_head)
            self.assertEqual(gtt.ref_head(local, "main"), remote_head)
            self.assertEqual(gtt.ref_head(local, "origin/main"), remote_head)

class TaskWorkspaceRuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    @staticmethod
    def assignee_plan(source: str, login: str, candidates: list[str]) -> dict[str, object]:
        return {
            "target": {"repo": "owner/repo"},
            "assignee": {
                "source": source,
                "login": login,
                "candidates": candidates,
                "resolution_evidence": "The user selected the exact assignee after the candidate facts were shown.",
            }
        }

    def test_portable_prerequisite_path_rejects_absolute_and_escape(self) -> None:
        evidence = self.root / "evidence.json"
        evidence.write_text("{}\n", encoding="utf-8")
        self.assertEqual(
            gtt.task_workspace_portable_input_path(self.root, "evidence.json", "evidence"),
            evidence.resolve(),
        )
        for value in (str(evidence), "../evidence.json", "nested\\evidence.json"):
            with self.subTest(value=value), self.assertRaises(gtt.WorkflowError):
                gtt.task_workspace_portable_input_path(self.root, value, "evidence")

    def test_ai_authored_non_mutation_routes_are_checked_zero_write_results(self) -> None:
        repository_source = Path(__file__).resolve().parents[5]
        plan = json.loads((
            repository_source
            / "trellis/skills/guru-team/packages/guru-create-task-workspace/examples/task-workspace-plan.json"
        ).read_text(encoding="utf-8"))
        snapshot = {
            "head": "a" * 40,
            "status_sha256": "b" * 64,
            "worktrees_sha256": "c" * 64,
            "issues_sha256": "d" * 64,
        }

        def finalize(authored: dict[str, object]) -> None:
            reviewable = gtt.context_digest(gtt.task_workspace_reviewable_projection(authored))
            authored["ai_review_gate"]["reviewed_plan_sha256"] = reviewable
            authored["freshness"]["reviewable_plan_sha256"] = reviewable
            authored["freshness"]["plan_sha256"] = gtt.task_workspace_plan_digest(authored)

        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "task_workspace_validate_plan", return_value=({}, [])),
            mock.patch.object(gtt, "task_workspace_snapshot", return_value=snapshot),
            mock.patch.object(gtt, "task_workspace_schema", return_value={}),
            mock.patch.object(gtt, "skill_json_schema_validation_errors", return_value=[]),
        ):
            for gate_status, typed_exit, reason_code in (
                ("reroute", "refresh_review", "disposition_changed"),
                ("blocked", "blocked", "object_conflict"),
            ):
                authored = copy.deepcopy(plan)
                authored["ai_review_gate"]["status"] = gate_status
                if gate_status == "blocked":
                    authored["naming"]["task_disposition"] = "conflict_blocked"
                finalize(authored)
                path = self.root / f"{gate_status}-plan.json"
                gtt.write_json(path, authored)
                result = gtt.cmd_create_task_workspace(argparse.Namespace(
                    root=str(self.root), input=str(path),
                    refresh_review=gate_status == "reroute", reason=None,
                    reason_code=reason_code,
                ))
                self.assertEqual(result["typed_exit"], typed_exit)
                self.assertTrue(result["no_side_effect"]["zero_writes"])

    def test_planned_task_locator_is_exact_and_reusable_across_dates(self) -> None:
        plan = {
            "naming": {"task_slug": "112-create-task-workspace"},
            "side_effects": {
                "task_artifacts": [
                    f".trellis/tasks/07-18-112-create-task-workspace/{name}"
                    for name in gtt.TASK_WORKSPACE_ARTIFACT_NAMES
                ]
            },
        }
        self.assertEqual(
            gtt.task_workspace_planned_task_dir(self.root, plan),
            self.root / ".trellis/tasks/07-18-112-create-task-workspace",
        )
        plan["side_effects"]["task_artifacts"][0] = ".trellis/tasks/07-19-wrong-task/issue-scope-ledger.json"
        with self.assertRaises(gtt.WorkflowError):
            gtt.task_workspace_planned_task_dir(self.root, plan)

    def test_assignee_fixed_order_cannot_be_bypassed(self) -> None:
        single = {"assignees": ["issue-owner"]}
        gtt.task_workspace_validate_assignee(
            self.root,
            self.assignee_plan("single_issue_assignee", "issue-owner", ["issue-owner"]),
            single,
        )
        with self.assertRaises(gtt.WorkflowError):
            gtt.task_workspace_validate_assignee(
                self.root,
                self.assignee_plan("user_supplied_after_unresolved", "other-user", ["issue-owner"]),
                single,
            )

        with mock.patch.object(gtt, "github_authenticated_login", return_value="current-user"):
            gtt.task_workspace_validate_assignee(
                self.root,
                self.assignee_plan("current_github_login", "current-user", []),
                {"assignees": []},
            )
            with self.assertRaises(gtt.WorkflowError):
                gtt.task_workspace_validate_assignee(
                    self.root,
                    self.assignee_plan("user_supplied_after_unresolved", "other-user", []),
                    {"assignees": []},
                )

        multiple = {"assignees": ["alice", "bob"]}
        gtt.task_workspace_validate_assignee(
            self.root,
            self.assignee_plan("user_selected_from_candidates", "alice", ["alice", "bob"]),
            multiple,
        )
        with mock.patch.object(gtt, "github_authenticated_login", side_effect=gtt.WorkflowError("actor unresolved")):
            gtt.task_workspace_validate_assignee(
                self.root,
                self.assignee_plan("user_supplied_after_unresolved", "chosen-user", []),
                {"assignees": []},
            )

    def test_official_task_create_adapter_ignores_existing_developer_identity(self) -> None:
        repository_source = Path(__file__).resolve().parents[5]
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Adapter Fixture"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "adapter-fixture@example.invalid"],
            cwd=self.root,
            check=True,
        )
        shutil.copytree(
            repository_source / ".trellis/scripts",
            self.root / ".trellis/scripts",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )
        identity_path = self.root / ".trellis/.developer"
        identity_bytes = b"name=existing-identity\n"
        identity_path.write_bytes(identity_bytes)

        proc = gtt.task_workspace_run_official_task_create(
            self.root,
            "#112 Verify no-developer adapter",
            "112-no-developer-adapter",
            "explicit-assignee",
        )

        self.assertEqual(proc.returncode, 0, proc.stderr)
        task_dir = gtt.resolve_task_dir(self.root, proc.stdout.strip())
        task_data = gtt.read_json(task_dir / "task.json")
        self.assertEqual(task_data["assignee"], "explicit-assignee")
        self.assertEqual(task_data["creator"], "explicit-assignee")
        self.assertEqual(identity_path.read_bytes(), identity_bytes)

    def test_issue_creation_adapter_writes_exact_reviewed_body_bytes(self) -> None:
        title = "Create exact reviewed issue"
        body = "First reviewed line\nSecond reviewed line"
        observed: dict[str, object] = {}
        live_issue = {
            "number": 112,
            "url": "https://github.com/owner/repo/issues/112",
            "state": "OPEN",
            "title": title,
            "body": body,
            "updatedAt": "2026-07-19T00:00:00Z",
            "labels": [{"name": "workflow"}],
        }

        def create_command(
            command: list[str],
            *,
            cwd: Path,
            check: bool,
            **_kwargs: object,
        ) -> subprocess.CompletedProcess[str]:
            self.assertEqual(command[:3], ["gh", "issue", "create"])
            body_path = Path(command[command.index("--body-file") + 1])
            observed["title"] = command[command.index("--title") + 1]
            observed["body"] = body_path.read_bytes()
            return subprocess.CompletedProcess(
                command,
                0,
                "https://github.com/owner/repo/issues/112\n",
                "",
            )

        with (
            mock.patch.object(gtt, "require_gh_auth"),
            mock.patch.object(gtt, "run", side_effect=create_command),
            mock.patch.object(gtt, "issue_view", return_value=live_issue),
        ):
            created = gtt.create_issue("owner/repo", title, body, self.root, ["workflow"])

        self.assertEqual(created, live_issue)
        self.assertEqual(observed["title"], title)
        self.assertEqual(observed["body"], body.encode("utf-8"))

    def test_reviewed_draft_checks_exact_live_labels_and_stops_at_refresh(self) -> None:
        draft = {
            "draft_id": "draft-112",
            "title": "Create exact task workspace",
            "body": "Reviewed body",
            "labels": ["workflow", "enhancement"],
            "reviewed_draft_sha256": "a" * 64,
        }
        plan = {
            "mode": "workflow",
            "target": {
                "repo": "owner/repo",
                "title_sha256": hashlib.sha256(draft["title"].encode()).hexdigest(),
                "body_sha256": hashlib.sha256(draft["body"].encode()).hexdigest(),
                "draft": draft,
            },
            "freshness": {"captured_at": "2026-07-18T00:00:00Z", "plan_sha256": "c" * 64},
        }
        live_issue = {
            "number": 112,
            "url": "https://github.com/owner/repo/issues/112",
            "state": "OPEN",
            "title": draft["title"],
            "body": draft["body"],
            "updatedAt": "2026-07-18T00:00:00Z",
            "labels": [{"name": "enhancement"}, {"name": "workflow"}],
        }
        with (
            mock.patch.object(gtt, "task_workspace_created_issue_recovery_candidates", return_value=[]),
            mock.patch.object(gtt, "create_issue", return_value=live_issue) as create_issue,
        ):
            result = gtt.task_workspace_created_issue_result(self.root, plan)
        create_issue.assert_called_once_with("owner/repo", draft["title"], draft["body"], self.root, draft["labels"])
        self.assertEqual(result["variant"], "created_issue")
        self.assertEqual(result["typed_exit"], "refresh_review")
        self.assertIsNone(result["created_workspace"])

        wrong_labels = copy.deepcopy(live_issue)
        wrong_labels["labels"] = [{"name": "workflow"}]
        with (
            mock.patch.object(gtt, "task_workspace_created_issue_recovery_candidates", return_value=[]),
            mock.patch.object(gtt, "create_issue", return_value=wrong_labels),
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.task_workspace_created_issue_result(self.root, plan)

    def test_created_issue_recovery_search_and_retry_create_only_once(self) -> None:
        title = "Recover exact reviewed issue"
        body = "Reviewed recovery body"
        plan = {
            "mode": "workflow",
            "target": {
                "repo": "owner/repo",
                "title_sha256": hashlib.sha256(title.encode()).hexdigest(),
                "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
                "draft": {
                    "draft_id": "draft-recovery-112",
                    "title": title,
                    "body": body,
                    "labels": ["enhancement", "workflow"],
                    "reviewed_draft_sha256": "a" * 64,
                },
            },
            "freshness": {"captured_at": "2026-07-18T00:00:00Z", "plan_sha256": "c" * 64},
        }
        exact = {
            "number": 500,
            "url": "https://github.com/owner/repo/issues/500",
            "state": "OPEN",
            "title": title,
            "body": body,
            "updatedAt": "2026-07-18T00:01:00Z",
            "createdAt": "2026-07-18T00:00:30Z",
            "labels": [{"name": "workflow"}, {"name": "enhancement"}],
        }
        old = {**exact, "number": 499, "url": "https://github.com/owner/repo/issues/499", "createdAt": "2026-07-17T23:59:59Z"}
        wrong_labels = {**exact, "number": 501, "url": "https://github.com/owner/repo/issues/501", "labels": [{"name": "workflow"}]}

        with mock.patch.object(gtt, "gh_json", return_value=[]):
            self.assertEqual(gtt.task_workspace_created_issue_recovery_candidates(self.root, plan), [])
        with mock.patch.object(gtt, "gh_json", return_value=[old, wrong_labels, exact]):
            self.assertEqual(
                [item["number"] for item in gtt.task_workspace_created_issue_recovery_candidates(self.root, plan)],
                [500],
            )
        incomplete = dict(exact)
        incomplete.pop("createdAt")
        with (
            mock.patch.object(gtt, "gh_json", return_value=[incomplete]) as gh_json,
            mock.patch.object(gtt, "create_issue") as create_issue,
            self.assertRaises(gtt.WorkflowError) as incomplete_error,
        ):
            gtt.task_workspace_created_issue_result(self.root, plan)
        self.assertEqual(
            incomplete_error.exception.payload["error_code"],
            "github_response_incomplete",
        )
        self.assertIn("createdAt", gh_json.call_args.kwargs["required_fields"])
        create_issue.assert_not_called()
        second_exact = {**exact, "number": 502, "url": "https://github.com/owner/repo/issues/502"}
        with (
            mock.patch.object(gtt, "task_workspace_created_issue_recovery_candidates", return_value=[exact, second_exact]),
            mock.patch.object(gtt, "create_issue") as create_issue,
            self.assertRaises(gtt.WorkflowError) as ambiguous,
        ):
            gtt.task_workspace_created_issue_result(self.root, plan)
        self.assertEqual(ambiguous.exception.payload["typed_exit"], "blocked")
        create_issue.assert_not_called()

        remote_issues: list[dict[str, object]] = []

        def create_then_lose_reread(*_args: object, **_kwargs: object) -> dict[str, object]:
            remote_issues.append(copy.deepcopy(exact))
            raise gtt.WorkflowError("immediate reread failed")

        with (
            mock.patch.object(gtt, "gh_json", side_effect=lambda *_args, **_kwargs: copy.deepcopy(remote_issues)),
            mock.patch.object(gtt, "create_issue", side_effect=create_then_lose_reread) as create_issue,
            mock.patch.object(gtt, "issue_view", return_value=exact),
        ):
            with self.assertRaises(gtt.WorkflowError):
                gtt.task_workspace_created_issue_result(self.root, plan)
            recovered = gtt.task_workspace_created_issue_result(self.root, plan)

        self.assertEqual(create_issue.call_count, 1)
        self.assertEqual(len(remote_issues), 1)
        self.assertEqual(recovered["typed_exit"], "refresh_review")
        self.assertIn("recovered", recovered["reason"].lower())

    def test_created_issue_provenance_requires_checked_result_and_context_binding(self) -> None:
        binding = {
            "repo": "owner/repo",
            "number": 500,
            "canonical_url": "https://github.com/owner/repo/issues/500",
            "state": "open",
            "title_sha256": "a" * 64,
            "body_sha256": "b" * 64,
            "updated_at": "2026-07-18T00:01:00Z",
            "reviewed_draft_id": "draft-112",
            "reviewed_draft_sha256": "c" * 64,
        }
        binding["facts_sha256"] = gtt.context_digest(binding)
        checked_result = {
            "schema_version": "2.0",
            "skill_id": "guru-create-task-workspace",
            "generated_at": "2026-07-18T00:02:00Z",
            "mode": "workflow",
            "variant": "created_issue",
            "plan_sha256": "e" * 64,
            "executor": {"status": "passed", "checked_at": "2026-07-18T00:01:00Z", "evidence": ["created"]},
            "checker": {"status": "passed", "checked_at": "2026-07-18T00:02:00Z", "evidence": ["checked"]},
            "created_issue": binding,
            "created_workspace": None,
            "no_side_effect": None,
            "typed_exit": "refresh_review",
            "reason": "Complete Intake refresh is required.",
            "consumer": {"kind": "skill", "id": "guru-sync-base"},
            "facts_sha256": "",
        }
        checked_result["facts_sha256"] = gtt.task_workspace_result_digest(checked_result)
        plan = {
            "mode": "workflow",
            "target": {
                "repo": binding["repo"],
                "issue_number": binding["number"],
                "url": binding["canonical_url"],
                "state": binding["state"],
                "title_sha256": binding["title_sha256"],
                "body_sha256": binding["body_sha256"],
                "updated_at": binding["updated_at"],
                "created_issue_binding_sha256": binding["facts_sha256"],
                "created_issue_result": checked_result,
            },
        }
        payloads = {
            "readiness": {
                "target": {
                    "kind": "existing_issue",
                    "repo": binding["repo"],
                    "issue_number": binding["number"],
                    "url": binding["canonical_url"],
                    "updated_at": binding["updated_at"],
                    "title_sha256": binding["title_sha256"],
                    "body_sha256": binding["body_sha256"],
                }
            }
        }
        self.assertEqual(gtt.task_workspace_created_issue_provenance_errors(plan, payloads), [])

        ordinary = copy.deepcopy(plan)
        ordinary["target"]["created_issue_binding_sha256"] = None
        ordinary["target"]["created_issue_result"] = None
        self.assertEqual(
            gtt.task_workspace_created_issue_provenance_errors(ordinary, payloads),
            [],
        )

        missing = copy.deepcopy(plan)
        missing["target"]["created_issue_result"] = None
        self.assertIn(
            "task_workspace_created_issue_provenance_incomplete",
            gtt.task_workspace_created_issue_provenance_errors(missing, payloads),
        )
        for field in ("reviewed_draft_id", "reviewed_draft_sha256"):
            stale = copy.deepcopy(plan)
            stale["target"]["created_issue_result"]["created_issue"][field] = "stale" if field.endswith("id") else "f" * 64
            errors = gtt.task_workspace_created_issue_provenance_errors(stale, payloads)
            self.assertIn("task_workspace_created_issue_binding_digest_mismatch", errors, field)
            self.assertIn("task_workspace_created_issue_result_facts_digest_mismatch", errors, field)
        invalid_readiness = {
            "repo": "other/repo",
            "kind": "proposed_draft",
            "issue_number": 501,
            "url": "https://github.com/owner/repo/issues/501",
            "updated_at": "2026-07-18T00:03:00Z",
            "title_sha256": "f" * 64,
            "body_sha256": "f" * 64,
        }
        for field, value in invalid_readiness.items():
            with self.subTest(readiness_field=field):
                wrong_readiness = copy.deepcopy(payloads)
                wrong_readiness["readiness"]["target"][field] = value
                self.assertIn(
                    f"task_workspace_created_issue_readiness_{field}_mismatch",
                    gtt.task_workspace_created_issue_provenance_errors(
                        plan, wrong_readiness
                    ),
                )

    def test_created_issue_provenance_survives_existing_issue_review_projection_chain(self) -> None:
        digest = lambda value: hashlib.sha256(value.encode()).hexdigest()
        repo = "owner/repo"
        number = 500
        url = f"https://github.com/{repo}/issues/{number}"
        updated_at = "2026-07-18T00:01:00Z"
        title_sha256 = digest("Reviewed title")
        body_sha256 = digest("Reviewed body")
        issue_facts = {
            "repo": repo,
            "number": number,
            "url": url,
            "state": "open",
            "updated_at": updated_at,
            "body_sha256": body_sha256,
        }
        clarity = {
            "invocation_context": {"kind": "initial_issue"},
            "review_target": {
                "kind": "issue",
                "repo": repo,
                "issue_number": number,
                "url": url,
                "state": "open",
                "updated_at": updated_at,
                "body_sha256": body_sha256,
            },
            "target_disposition": {
                "disposition_digest": digest("disposition"),
                "duplicate_facts_sha256": digest("duplicates"),
            },
        }
        wording = {
            "scope": {
                "identity": f"change_request:{url}",
                "items": [
                    {"field": "title", "content_sha256": title_sha256},
                    {"field": "body", "content_sha256": body_sha256},
                ],
            }
        }
        payloads = {"clarity": clarity, "wording": wording}
        target = gtt.change_request_review_prerequisite_target_identity_projection(payloads)
        self.assertEqual(
            target,
            {
                "kind": "existing_issue",
                "repo": repo,
                "title_sha256": title_sha256,
                "body_sha256": body_sha256,
                "issue_number": number,
                "url": url,
                "updated_at": updated_at,
            },
        )
        target.update({
            "identity_sha256": gtt.context_digest(
                gtt.change_request_review_target_identity_projection(target)
            ),
            "content_sha256": gtt.context_digest({
                "title_sha256": title_sha256,
                "body_sha256": body_sha256,
            }),
            "draft_id": None,
            "source_request_sha256": None,
            "caller_locator": None,
            "request_id": None,
            "side_effect_free": False,
        })
        projections = {
            "clarity": {
                "status": "current", "payload_sha256": gtt.context_digest(clarity),
                "facts_sha256": digest("clarity"),
                "disposition_sha256": clarity["target_disposition"]["disposition_digest"],
                "error_codes": [],
            },
            "wording": {
                "status": "current", "payload_sha256": gtt.context_digest(wording),
                "facts_sha256": digest("wording"), "error_codes": [],
            },
        }
        gtt.change_request_review_target_linkage_errors(target, payloads, projections)
        self.assertTrue(all(row["status"] == "current" for row in projections.values()))
        self.assertTrue(all(row["error_codes"] == [] for row in projections.values()))
        linkage = gtt.change_request_review_linkage(target, projections)
        conclusion = {"close_issues": [number], "related_issues": [], "followup_issues": []}
        readiness = {
            "target": target,
            "prerequisites": projections,
            "evidence_linkage": linkage,
            "semantic_review": {
                "scope_conclusion": conclusion,
                "ai_review_gate": {
                    "reviewed_linkage_sha256": linkage["linkage_sha256"],
                    "scope_conclusion_sha256": gtt.context_digest(conclusion),
                },
            },
        }
        payloads["readiness"] = readiness
        self.assertEqual(gtt.task_workspace_readiness_linkage_errors(readiness, payloads), [])

        binding = {
            "repo": repo,
            "number": number,
            "canonical_url": url,
            "state": "open",
            "title_sha256": title_sha256,
            "body_sha256": body_sha256,
            "updated_at": updated_at,
            "reviewed_draft_id": "draft-112",
            "reviewed_draft_sha256": digest("reviewed-draft"),
        }
        binding["facts_sha256"] = gtt.context_digest(binding)
        result = {
            "schema_version": "2.0",
            "skill_id": "guru-create-task-workspace",
            "generated_at": "2026-07-18T00:02:00Z",
            "mode": "workflow",
            "variant": "created_issue",
            "plan_sha256": digest("draft-plan"),
            "executor": {"status": "passed", "checked_at": "2026-07-18T00:01:00Z", "evidence": ["created"]},
            "checker": {"status": "passed", "checked_at": "2026-07-18T00:02:00Z", "evidence": ["checked"]},
            "created_issue": binding,
            "created_workspace": None,
            "no_side_effect": None,
            "typed_exit": "refresh_review",
            "reason": "Complete Intake refresh is required.",
            "consumer": copy.deepcopy(gtt.TASK_WORKSPACE_CONSUMERS["refresh_review"]),
            "facts_sha256": "",
        }
        result["facts_sha256"] = gtt.task_workspace_result_digest(result)
        plan = {
            "mode": "workflow",
            "target": {
                "repo": repo,
                "issue_number": number,
                "url": url,
                "state": "open",
                "updated_at": updated_at,
                "title_sha256": title_sha256,
                "body_sha256": body_sha256,
                "created_issue_binding_sha256": binding["facts_sha256"],
                "created_issue_result": result,
            },
        }
        self.assertEqual(gtt.task_workspace_created_issue_provenance_errors(plan, payloads), [])

        stale_readiness = copy.deepcopy(payloads)
        stale_readiness["readiness"]["target"]["body_sha256"] = digest(
            "stale-live-issue"
        )
        self.assertIn(
            "task_workspace_created_issue_readiness_body_sha256_mismatch",
            gtt.task_workspace_created_issue_provenance_errors(
                plan, stale_readiness
            ),
        )

    def test_mutation_time_base_sync_detects_remote_advance_before_business_writes(self) -> None:
        repository = self.root / "repository"
        remote = self.root / "remote.git"
        updater = self.root / "updater"
        repository.mkdir()
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repository, check=True)
        subprocess.run(["git", "config", "user.name", "Base Fixture"], cwd=repository, check=True)
        subprocess.run(["git", "config", "user.email", "base@example.invalid"], cwd=repository, check=True)
        (repository / "base.txt").write_text("initial\n", encoding="utf-8")
        subprocess.run(["git", "add", "base.txt"], cwd=repository, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "initial"], cwd=repository, check=True)
        subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=repository, check=True)
        subprocess.run(["git", "push", "-q", "-u", "origin", "main"], cwd=repository, check=True)

        resolution = gtt.resolve_base_selection(repository, {}, "main", "origin")
        initial = gtt.execute_base_sync(repository, resolution)
        initial_head = initial["git"]["remote_head_after"]
        plan = {
            "base": {
                "selected_base": "main",
                "remote": "origin",
                "base_ref": "refs/remotes/origin/main",
                "decision_head": initial_head,
                "local_head": initial_head,
                "remote_head": initial_head,
                "post_sync_resolution_sha256": initial["post_sync_resolution_sha256"],
                "sync_facts_sha256": initial["facts_sha256"],
            }
        }
        unchanged = gtt.task_workspace_refresh_base_before_mutation(repository, plan, initial)
        self.assertEqual(unchanged["post_sync_resolution_sha256"], initial["post_sync_resolution_sha256"])

        subprocess.run(["git", "clone", "-q", "-b", "main", str(remote), str(updater)], check=True)
        subprocess.run(["git", "config", "user.name", "Remote Fixture"], cwd=updater, check=True)
        subprocess.run(["git", "config", "user.email", "remote@example.invalid"], cwd=updater, check=True)
        (updater / "base.txt").write_text("advanced\n", encoding="utf-8")
        subprocess.run(["git", "add", "base.txt"], cwd=updater, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "advance"], cwd=updater, check=True)
        subprocess.run(["git", "push", "-q", "origin", "main"], cwd=updater, check=True)
        remote_head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=updater, check=True, text=True, capture_output=True
        ).stdout.strip()
        self.assertEqual(gtt.ref_head(repository, "refs/remotes/origin/main"), initial_head)

        with self.assertRaises(gtt.WorkflowError) as advanced:
            gtt.task_workspace_refresh_base_before_mutation(repository, plan, initial)
        self.assertEqual(advanced.exception.payload["typed_exit"], "refresh_review")
        self.assertEqual(
            advanced.exception.payload["error_code"],
            "task_workspace_base_post_sync_identity_changed",
        )
        self.assertEqual(gtt.current_head(repository), remote_head)
        self.assertEqual(gtt.ref_head(repository, "refs/remotes/origin/main"), remote_head)
        self.assertEqual(
            subprocess.run(
                ["git", "branch", "--format=%(refname:short)"],
                cwd=repository,
                check=True,
                text=True,
                capture_output=True,
            ).stdout.splitlines(),
            ["main"],
        )
        self.assertEqual(len(gtt.worktree_records(repository)), 1)
        self.assertFalse((repository / ".trellis/tasks").exists())

    def test_create_command_stops_before_business_mutation_when_base_refreshes(self) -> None:
        repository_source = Path(__file__).resolve().parents[5]
        plan = json.loads((
            repository_source
            / "trellis/skills/guru-team/packages/guru-create-task-workspace/examples/task-workspace-plan.json"
        ).read_text(encoding="utf-8"))
        plan_path = self.root / "plan.json"
        gtt.write_json(plan_path, plan)
        snapshot = {
            "head": "a" * 40,
            "status_sha256": "b" * 64,
            "worktrees_sha256": "c" * 64,
            "issues_sha256": "d" * 64,
        }
        refresh = gtt.WorkflowError(
            "base advanced",
            exit_code=2,
            payload={"typed_exit": "refresh_review", "error_code": "task_workspace_base_post_sync_identity_changed"},
        )
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "task_workspace_validate_plan", return_value=({"base": {}}, [])),
            mock.patch.object(gtt, "task_workspace_snapshot", return_value=snapshot),
            mock.patch.object(gtt, "task_workspace_refresh_base_before_mutation", side_effect=refresh) as base_guard,
            mock.patch.object(gtt, "task_workspace_created_issue_result") as issue_mutation,
            mock.patch.object(gtt, "task_workspace_created_workspace_result") as workspace_mutation,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_create_task_workspace(argparse.Namespace(
                root=str(self.root), input=str(plan_path), cancelled=False,
                refresh_review=False, reason=None, reason_code=None,
            ))
        self.assertEqual(raised.exception.payload["typed_exit"], "refresh_review")
        base_guard.assert_called_once_with(self.root, plan, {})
        issue_mutation.assert_not_called()
        workspace_mutation.assert_not_called()

    def test_reviewed_draft_plan_binds_current_readiness_identity(self) -> None:
        digest = lambda value: hashlib.sha256(value.encode()).hexdigest()
        clarity = {
            "review_target": {"state": "draft"},
            "target_disposition": {
                "disposition_digest": digest("disposition"),
                "duplicate_facts_sha256": digest("duplicate"),
            },
        }
        wording = {"scope": {"scope_sha256": digest("wording-scope")}}
        target = {
            "kind": "proposed_draft",
            "repo": "owner/repo",
            "issue_number": None,
            "url": None,
            "updated_at": None,
            "draft_id": "draft-112",
            "source_request_sha256": digest("source-request"),
            "caller_locator": None,
            "request_id": None,
            "title_sha256": digest("Reviewed title"),
            "body_sha256": digest("Reviewed body"),
            "side_effect_free": True,
        }
        target["identity_sha256"] = gtt.context_digest(
            gtt.change_request_review_target_identity_projection(target)
        )
        target["content_sha256"] = gtt.context_digest({
            "title_sha256": target["title_sha256"],
            "body_sha256": target["body_sha256"],
        })
        readiness_prerequisites = {
            "clarity": {
                "status": "current", "payload_sha256": gtt.context_digest(clarity),
                "facts_sha256": digest("clarity"),
                "disposition_sha256": clarity["target_disposition"]["disposition_digest"],
                "error_codes": [],
            },
            "wording": {
                "status": "current", "payload_sha256": gtt.context_digest(wording),
                "facts_sha256": digest("wording"), "error_codes": [],
            },
        }
        linkage = gtt.change_request_review_linkage(target, readiness_prerequisites)
        conclusion = {"close_issues": [], "related_issues": [], "followup_issues": []}
        readiness = {
            "target": target,
            "prerequisites": readiness_prerequisites,
            "evidence_linkage": linkage,
            "semantic_review": {
                "scope_conclusion": conclusion,
                "ai_review_gate": {
                    "reviewed_linkage_sha256": linkage["linkage_sha256"],
                    "scope_conclusion_sha256": gtt.context_digest(conclusion),
                },
            },
        }
        payloads = {
            "clarity": clarity, "wording": wording, "readiness": readiness,
            "base": {
                "resolution": {"selected_base": "main", "remote": "origin"},
                "decision_checkout": {"head_after": "a" * 40},
                "git": {
                    "local_head_after": "a" * 40,
                    "remote_head_after": "a" * 40,
                    "remote_ref": "refs/remotes/origin/main",
                },
                "post_sync_resolution_sha256": digest("post-sync"),
                "facts_sha256": digest("base"),
            },
        }
        self.assertEqual(gtt.task_workspace_readiness_linkage_errors(readiness, payloads), [])

        plan = {
            "invocation": {"target_kind": "reviewed_draft"},
            "target": {
                "kind": "reviewed_draft", "repo": "wrong/repo",
                "issue_number": None, "url": None, "state": None, "updated_at": None,
                "title_sha256": target["title_sha256"], "body_sha256": target["body_sha256"],
                "disposition_sha256": clarity["target_disposition"]["disposition_digest"],
                "duplicate_decision_sha256": clarity["target_disposition"]["duplicate_facts_sha256"],
                "created_issue_binding_sha256": None,
                "created_issue_result": None,
                "draft": {
                    "draft_id": target["draft_id"],
                    "source_request_sha256": digest("wrong-source"),
                    "title": "Reviewed title", "body": "Reviewed body", "labels": [],
                    "reviewed_draft_sha256": digest("wrong-draft"),
                },
            },
            "prerequisites": {"wording": {"content_sha256": wording["scope"]["scope_sha256"]}},
            "scope": {
                "primary": None, "close": [], "related": [], "followup": [],
                "scope_sha256": digest("wrong-scope"),
            },
            "base": {}, "naming": {},
            "side_effects": {
                "operations": ["create_issue"], "task_artifacts": [],
                "runtime_mappings": [], "stop_after": "created_issue_refresh",
            },
            "confirmations": {}, "ai_review_gate": {}, "freshness": {},
        }
        errors = gtt.task_workspace_plan_semantic_errors(self.root, plan, payloads)
        self.assertIn("task_workspace_reviewed_draft_identity_mismatch", errors)
        self.assertIn("task_workspace_reviewed_draft_source_request_mismatch", errors)
        self.assertIn("task_workspace_reviewed_draft_digest_mismatch", errors)
        self.assertIn("task_workspace_scope_digest_mismatch", errors)
        self.assertIn("task_workspace_base_base_ref_mismatch", errors)

        valid_plan = copy.deepcopy(plan)
        valid_plan["target"]["repo"] = target["repo"]
        valid_plan["target"]["draft"]["source_request_sha256"] = target["source_request_sha256"]
        valid_plan["target"]["draft"]["reviewed_draft_sha256"] = target["identity_sha256"]
        valid_plan["scope"]["scope_sha256"] = gtt.task_workspace_scope_digest(valid_plan["scope"])
        valid_plan["base"] = {
            "selected_base": "main", "remote": "origin",
            "base_ref": "refs/remotes/origin/main",
            "decision_head": "a" * 40, "local_head": "a" * 40,
            "remote_head": "a" * 40,
            "post_sync_resolution_sha256": digest("post-sync"),
            "sync_facts_sha256": digest("base"),
        }
        valid_errors = gtt.task_workspace_plan_semantic_errors(self.root, valid_plan, payloads)
        self.assertFalse(any("reviewed_draft_" in error for error in valid_errors))

        standalone_payloads = copy.deepcopy(payloads)
        standalone_target = standalone_payloads["readiness"]["target"]
        standalone_target.update({
            "kind": "standalone_request", "draft_id": None,
            "caller_locator": "direct-platform-caller", "request_id": "draft-112",
        })
        standalone_target["identity_sha256"] = gtt.context_digest(
            gtt.change_request_review_target_identity_projection(standalone_target)
        )
        standalone_linkage = gtt.change_request_review_linkage(
            standalone_target,
            standalone_payloads["readiness"]["prerequisites"],
        )
        standalone_payloads["readiness"]["evidence_linkage"] = standalone_linkage
        standalone_payloads["readiness"]["semantic_review"]["ai_review_gate"][
            "reviewed_linkage_sha256"
        ] = standalone_linkage["linkage_sha256"]
        standalone_plan = copy.deepcopy(valid_plan)
        standalone_plan["invocation"]["caller"] = "direct-platform-caller"
        standalone_plan["target"]["draft"]["reviewed_draft_sha256"] = standalone_target[
            "identity_sha256"
        ]
        standalone_errors = gtt.task_workspace_plan_semantic_errors(
            self.root,
            standalone_plan,
            standalone_payloads,
        )
        self.assertFalse(any("reviewed_draft_" in error for error in standalone_errors))
        self.assertNotIn("task_workspace_standalone_caller_mismatch", standalone_errors)

        invalid_ref_plan = copy.deepcopy(valid_plan)
        invalid_ref_plan["scope"]["followup"] = [{
            "number": 132,
            "url": "https://github.com/owner/repo/issues/131",
            "title": "Follow-up",
            "reason": "Deferred scope.",
        }]
        invalid_ref_plan["scope"]["scope_sha256"] = gtt.task_workspace_scope_digest(
            invalid_ref_plan["scope"]
        )
        invalid_ref_errors = gtt.task_workspace_plan_semantic_errors(
            self.root,
            invalid_ref_plan,
            payloads,
        )
        self.assertIn("task_workspace_scope_issue_url_mismatch", invalid_ref_errors)

    def test_checker_reconstructs_canonical_artifact_bytes(self) -> None:
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        (self.root / ".gitignore").write_text(".trellis/.runtime/\n", encoding="utf-8")
        task_relative = ".trellis/tasks/07-18-112-create-task-workspace"
        task_dir = self.root / task_relative
        task_dir.mkdir(parents=True)
        task_data = {
            "id": "112-create-task-workspace",
            "name": "112-create-task-workspace",
            "branch": "feat/112-create-task-workspace",
            "base_branch": "main",
            "creator": "maintainer",
            "assignee": "maintainer",
            "status": "planning",
        }
        (task_dir / "task.json").write_text(json.dumps(task_data), encoding="utf-8")
        intended = {name: f"canonical {name}\n".encode() for name in gtt.TASK_WORKSPACE_ARTIFACT_NAMES}
        for name, content in intended.items():
            (task_dir / name).write_bytes(content)

        plan = {
            "target": {"repo": "owner/repo", "issue_number": 112},
            "naming": {
                "branch_name": "feat/112-create-task-workspace",
                "workspace_slug": "112-create-task-workspace",
                "task_slug": "112-create-task-workspace",
            },
            "base": {"base_ref": "refs/remotes/origin/main", "decision_head": "a" * 40, "selected_base": "main"},
            "assignee": {"login": "maintainer"},
            "side_effects": {
                "task_artifacts": [f"{task_relative}/{name}" for name in gtt.TASK_WORKSPACE_ARTIFACT_NAMES],
                "runtime_mappings": [
                    ".trellis/.runtime/guru-team/workspaces/112-create-task-workspace.json",
                    ".trellis/.runtime/guru-team/tasks/112-create-task-workspace.json",
                ],
            },
            "freshness": {"plan_sha256": "b" * 64},
            "ai_review_gate": {"status": "passed"},
        }
        runtime_rows = []
        for relative in plan["side_effects"]["runtime_mappings"]:
            mapping_path = self.root / relative
            mapping_path.parent.mkdir(parents=True, exist_ok=True)
            if "/workspaces/" in relative:
                payload = {
                    "workspace_slug": "112-create-task-workspace",
                    "workspace_path": str(self.root.resolve()),
                    "source_checkout": str(self.root.resolve()),
                    "branch_name": "feat/112-create-task-workspace",
                }
            else:
                payload = {
                    "task_slug": "112-create-task-workspace",
                    "workspace_slug": "112-create-task-workspace",
                    "workspace_path": str(self.root.resolve()),
                    "task_artifact_dir": task_relative,
                }
            mapping_path.write_text(json.dumps(payload), encoding="utf-8")
            runtime_rows.append({"path": relative, "ignored": True})
        result = {
            "plan_sha256": "b" * 64,
            "variant": "created_workspace",
            "created_workspace": {
                "repo": "owner/repo",
                "issue_number": 112,
                "branch_name": "feat/112-create-task-workspace",
                "base_ref": "refs/remotes/origin/main",
                "base_head": "a" * 40,
                "workspace_slug": "112-create-task-workspace",
                "task_slug": "112-create-task-workspace",
                "task_artifact_dir": task_relative,
                "assignee": "maintainer",
                "task_status": "planning",
                "artifacts": [gtt.task_workspace_artifact_row(self.root, task_dir / name) for name in gtt.TASK_WORKSPACE_ARTIFACT_NAMES],
                "runtime_mappings": runtime_rows,
            },
            "typed_exit": "created",
            "executor": {"status": "passed"},
            "consumer": copy.deepcopy(gtt.TASK_WORKSPACE_CONSUMERS["created"]),
            "facts_sha256": "",
        }
        result["facts_sha256"] = gtt.task_workspace_result_digest(result)
        with (
            mock.patch.object(gtt, "task_workspace_schema", return_value={}),
            mock.patch.object(gtt, "skill_json_schema_validation_errors", return_value=[]),
            mock.patch.object(gtt, "load_config", return_value={"workspace_mode": "current"}),
            mock.patch.object(gtt, "task_workspace_live_issue", return_value={"title": "Issue title"}),
            mock.patch.object(gtt, "task_workspace_intended_artifacts", return_value=intended),
        ):
            self.assertEqual(gtt.task_workspace_result_check_errors(self.root, plan, result, {}), [])
            changed_path = task_dir / "issue-scope-ledger.json"
            changed_path.write_bytes(b"different but self-consistent\n")
            for index, row in enumerate(result["created_workspace"]["artifacts"]):
                if row["path"].endswith("/issue-scope-ledger.json"):
                    result["created_workspace"]["artifacts"][index] = gtt.task_workspace_artifact_row(self.root, changed_path)
            result["facts_sha256"] = gtt.task_workspace_result_digest(result)
            errors = gtt.task_workspace_result_check_errors(self.root, plan, result, {})
        self.assertIn("task_workspace_result_issue-scope-ledger.json_canonical_bytes_mismatch", errors)
        changed_path.chmod(0o600)
        with self.assertRaises(gtt.WorkflowError):
            gtt.task_workspace_artifact_row(self.root, changed_path)

    def test_production_task_workspaces_archive_and_merge_in_both_orders(self) -> None:
        fixture_root = self.root / "ab-merge"
        source = fixture_root / "project"
        worktree_root = fixture_root / "task-worktrees"
        source.mkdir(parents=True)
        repository_source = Path(__file__).resolve().parents[5]

        subprocess.run(["git", "init", "-q"], cwd=source, check=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=source, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture Maintainer"], cwd=source, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.com"], cwd=source, check=True)
        shutil.copytree(
            repository_source / ".trellis/scripts",
            source / ".trellis/scripts",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )
        installed_schemas = (
            source
            / ".trellis/guru-team/skills/packages/guru-create-task-workspace/schemas"
        )
        installed_schemas.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            repository_source
            / "trellis/skills/guru-team/packages/guru-create-task-workspace/schemas",
            installed_schemas,
        )
        (source / ".trellis/guru-team/config.yml").write_text(
            f"workspace_mode: worktree\nworktree_root: {worktree_root}\n",
            encoding="utf-8",
        )
        (source / ".trellis/config.yaml").write_text(
            "session_auto_commit: false\n",
            encoding="utf-8",
        )
        (source / ".gitignore").write_text(
            ".trellis/.runtime/\n__pycache__/\n*.py[cod]\n",
            encoding="utf-8",
        )
        (source / "README.md").write_text("# A/B fixture\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=source, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture base"], cwd=source, check=True)
        base_head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=source, check=True, text=True, capture_output=True
        ).stdout.strip()

        def fixture_payloads(issue_number: int, token: str) -> dict[str, dict[str, object]]:
            digest = lambda value: hashlib.sha256(f"{token}:{value}".encode()).hexdigest()
            disposition = digest("disposition")
            duplicate = digest("duplicate")
            title = f"Create task workspace {token.upper()}"
            body = f"Reviewed fixture body {token.upper()}"
            payloads = {
                "base": {
                    "skill_id": "guru-sync-base",
                    "status": "synced",
                    "facts_sha256": digest("base-facts"),
                    "resolution": {"selected_base": "main", "remote": "origin"},
                    "decision_checkout": {"head_after": base_head},
                    "post_sync_resolution_sha256": digest("post-sync-resolution"),
                    "git": {
                        "local_head_after": base_head,
                        "remote_head_after": base_head,
                        "remote_ref": "main",
                    },
                },
                "clarity": {
                    "skill_id": "guru-clarify-requirements",
                    "typed_exit": "clear",
                    "content_identity": {
                        "result_sha256": digest("clarity-result"),
                        "content_sha256": digest("clarity-content"),
                        "context_sha256": digest("clarity-context"),
                    },
                    "review_target": {"state": "open"},
                    "target_disposition": {
                        "disposition_digest": disposition,
                        "duplicate_facts_sha256": duplicate,
                    },
                },
                "wording": {
                    "skill_id": "guru-review-contract-wording",
                    "typed_exit": "pass",
                    "facts_sha256": digest("wording-facts"),
                    "scope": {"scope_sha256": digest("wording-scope")},
                    "scan": {"scan_sha256": digest("wording-scan")},
                },
                "readiness": {
                    "skill_id": "guru-review-change-request",
                    "typed_exit": "ready",
                    "facts_sha256": digest("readiness-facts"),
                    "target": {
                        "kind": "existing_issue",
                        "repo": "example/fixture",
                        "issue_number": issue_number,
                        "url": f"https://github.com/example/fixture/issues/{issue_number}",
                        "updated_at": "2026-07-18T00:00:00Z",
                        "title_sha256": hashlib.sha256(title.encode()).hexdigest(),
                        "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
                        "draft_id": None,
                        "source_request_sha256": None,
                        "caller_locator": None,
                        "request_id": None,
                        "side_effect_free": False,
                    },
                },
            }
            target = payloads["readiness"]["target"]
            target["identity_sha256"] = gtt.context_digest(
                gtt.change_request_review_target_identity_projection(target)
            )
            target["content_sha256"] = gtt.context_digest({
                "title_sha256": target["title_sha256"],
                "body_sha256": target["body_sha256"],
            })
            projections = {
                "clarity": {
                    "status": "current", "payload_sha256": gtt.context_digest(payloads["clarity"]),
                    "facts_sha256": digest("clarity-facts"),
                    "disposition_sha256": disposition, "error_codes": [],
                },
                "wording": {
                    "status": "current", "payload_sha256": gtt.context_digest(payloads["wording"]),
                    "facts_sha256": payloads["wording"]["facts_sha256"], "error_codes": [],
                },
            }
            linkage = gtt.change_request_review_linkage(target, projections)
            conclusion = {
                "close_issues": [issue_number],
                "related_issues": [],
                "followup_issues": [],
            }
            payloads["readiness"].update({
                "prerequisites": projections,
                "evidence_linkage": linkage,
                "semantic_review": {
                    "scope_conclusion": conclusion,
                    "ai_review_gate": {
                        "reviewed_linkage_sha256": linkage["linkage_sha256"],
                        "scope_conclusion_sha256": gtt.context_digest(conclusion),
                    },
                },
            })
            return payloads

        def write_plan(issue_number: int, token: str) -> tuple[Path, dict[str, object], dict[str, object]]:
            payloads = fixture_payloads(issue_number, token)
            input_root = source / ".fixture-inputs" / token
            input_root.mkdir(parents=True)
            prerequisites: dict[str, dict[str, object]] = {}
            for key, payload in payloads.items():
                relative = f".fixture-inputs/{token}/{key}.json"
                path = source / relative
                gtt.write_json(path, payload)
                prerequisites[key] = gtt.task_workspace_prerequisite_projection(
                    key,
                    relative,
                    payload,
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                )

            task_slug = f"{issue_number}-create-task-workspace-{token}"
            task_dir = f".trellis/tasks/{datetime.now().strftime('%m-%d')}-{task_slug}"
            title = str(payloads["readiness"]["target"]["title_sha256"])
            body = str(payloads["readiness"]["target"]["body_sha256"])
            target_url = f"https://github.com/example/fixture/issues/{issue_number}"
            scope_item = {
                "number": issue_number,
                "url": target_url,
                "title": f"Create task workspace {token.upper()}",
                "reason": "Independently archived A/B merge fixture task.",
            }
            plan: dict[str, object] = {
                "schema_version": "2.0",
                "skill_id": "guru-create-task-workspace",
                "generated_at": "2026-07-18T00:00:00Z",
                "mode": "workflow",
                "invocation": {
                    "caller": "guru-review-change-request:ready",
                    "target_kind": "existing_issue",
                    "action_scope": "workspace_and_task_mutation",
                    "resume_identity": f"fixture-{token}",
                },
                "prerequisites": prerequisites,
                "target": {
                    "kind": "existing_issue",
                    "repo": "example/fixture",
                    "issue_number": issue_number,
                    "url": target_url,
                    "state": "open",
                    "updated_at": "2026-07-18T00:00:00Z",
                    "title_sha256": title,
                    "body_sha256": body,
                    "draft": None,
                    "disposition_sha256": payloads["clarity"]["target_disposition"]["disposition_digest"],
                    "duplicate_decision_sha256": payloads["clarity"]["target_disposition"]["duplicate_facts_sha256"],
                    "created_issue_binding_sha256": None,
                    "created_issue_result": None,
                },
                "scope": {
                    "primary": scope_item,
                    "close": [scope_item],
                    "related": [],
                    "followup": [],
                    "scope_sha256": "0" * 64,
                },
                "base": {
                    "selected_base": "main",
                    "remote": "origin",
                    "base_ref": "main",
                    "decision_head": base_head,
                    "local_head": base_head,
                    "remote_head": base_head,
                    "post_sync_resolution_sha256": payloads["base"]["post_sync_resolution_sha256"],
                    "sync_facts_sha256": payloads["base"]["facts_sha256"],
                },
                "naming": {
                    "branch_name": f"feat/{task_slug}",
                    "workspace_slug": task_slug,
                    "task_slug": task_slug,
                    "task_title": f"#{issue_number} Create task workspace {token.upper()}",
                    "reason": "Names bind the issue number and task workspace action.",
                    "branch_disposition": "create_new",
                    "workspace_disposition": "create_new",
                    "task_disposition": "create_new",
                },
                "assignee": {
                    "login": "fixture-maintainer",
                    "source": "explicit_input",
                    "candidates": [],
                    "resolution_evidence": "The fixture provides the exact reviewed assignee.",
                },
                "side_effects": {
                    "operations": [
                        "create_branch", "create_worktree", "create_task",
                        "write_task_artifacts", "write_runtime_mappings",
                    ],
                    "task_artifacts": [
                        f"{task_dir}/{name}" for name in gtt.TASK_WORKSPACE_ARTIFACT_NAMES
                    ],
                    "runtime_mappings": [
                        f".trellis/.runtime/guru-team/workspaces/{task_slug}.json",
                        f".trellis/.runtime/guru-team/tasks/{task_slug}.json",
                    ],
                    "command_argv": ["create-task-workspace", "--input", f".fixture-inputs/{token}/plan.json"],
                    "stop_after": "created_workspace",
                },
                "ai_review_gate": {
                    "status": "passed",
                    "reviewer": "A/B production fixture reviewer",
                    "reviewed_plan_sha256": "0" * 64,
                    "summary": "The target, names, assignee, scope and isolated task metadata are complete.",
                    "evidence": [
                        "The invocation contains only one workspace and task mutation.",
                        "All tracked metadata is task-local.",
                    ],
                },
                "freshness": {
                    "captured_at": "2026-07-18T00:00:00Z",
                    "reviewable_plan_sha256": "0" * 64,
                    "plan_sha256": "0" * 64,
                },
            }
            plan["scope"]["scope_sha256"] = gtt.task_workspace_scope_digest(plan["scope"])
            reviewable = gtt.context_digest(gtt.task_workspace_reviewable_projection(plan))
            plan["ai_review_gate"]["reviewed_plan_sha256"] = reviewable
            plan["freshness"]["reviewable_plan_sha256"] = reviewable
            plan["freshness"]["plan_sha256"] = gtt.task_workspace_plan_digest(plan)
            plan_path = input_root / "plan.json"
            gtt.write_json(plan_path, plan)
            live_issue = {
                "repo": "example/fixture",
                "issue_number": issue_number,
                "url": target_url,
                "state": "open",
                "updated_at": "2026-07-18T00:00:00Z",
                "title_sha256": title,
                "body_sha256": body,
                "title": scope_item["title"],
                "body": f"Reviewed fixture body {token.upper()}",
                "assignees": [],
            }
            return plan_path, plan, live_issue

        def build_and_archive(issue_number: int, token: str) -> tuple[str, set[str]]:
            plan_path, plan, live_issue = write_plan(issue_number, token)
            args = argparse.Namespace(root=str(source), input=str(plan_path))
            result_path = plan_path.parent / "result.json"
            real_prepare_workspace = gtt.prepare_workspace

            def prepare_and_copy_inputs(*arguments: object, **kwargs: object) -> tuple[str, Path, bool]:
                mode, workspace, ready = real_prepare_workspace(*arguments, **kwargs)
                if ready and workspace.resolve() != source.resolve():
                    shutil.copytree(
                        plan_path.parent,
                        workspace / ".fixture-inputs" / token,
                        dirs_exist_ok=True,
                    )
                return mode, workspace, ready

            with (
                mock.patch.object(gtt, "task_workspace_prerequisite_errors", return_value=[]),
                mock.patch.object(gtt, "task_workspace_live_issue", return_value=live_issue),
                mock.patch.object(gtt, "task_workspace_refresh_base_before_mutation", return_value={}),
            ):
                self.assertEqual(gtt.cmd_record_task_workspace_plan(args), plan)
                with mock.patch.object(gtt, "prepare_workspace", side_effect=prepare_and_copy_inputs):
                    result = gtt.cmd_create_task_workspace(
                        argparse.Namespace(
                            root=str(source), input=str(plan_path),
                            refresh_review=False, reason=None,
                        )
                    )
                gtt.write_json(result_path, result)
                checked = gtt.cmd_check_task_workspace_result(
                    argparse.Namespace(
                        root=str(source), input=str(result_path), plan_input=str(plan_path)
                    )
                )
            self.assertEqual(checked["checker"]["status"], "passed")
            workspace = worktree_root / str(result["created_workspace"]["workspace_slug"])
            task_dir = workspace / result["created_workspace"]["task_artifact_dir"]
            shutil.rmtree(workspace / ".fixture-inputs")
            task_context = {
                "base_branch": "main",
                "base_ref": "main",
                "branch_name": str(plan["naming"]["branch_name"]),
                "task_artifact_dir": gtt.repo_relative(workspace, task_dir),
            }
            ledger = gtt.read_json(task_dir / "issue-scope-ledger.json")
            archive_relative = (
                f".trellis/tasks/archive/{datetime.now().strftime('%Y-%m')}/{task_dir.name}"
            )
            archived_paths = [
                f"{archive_relative}/{path.name}"
                for path in task_dir.iterdir()
                if path.is_file()
            ]
            archived_paths.append(f"{archive_relative}/finish-summary.json")
            summary = gtt.build_finish_summary(
                workspace,
                task_dir,
                task_context,
                ledger,
                valid_pr_body(
                    f"新增 task-local {token.upper()} 归档元数据并验证双向合并。"
                ),
                base_head,
                changed_paths=archived_paths,
                archive_dir_override=archive_relative,
            )
            gtt.write_json(task_dir / "finish-summary.json", summary)
            subprocess.run(
                ["python3", "./.trellis/scripts/task.py", "archive", task_dir.name, "--no-commit"],
                cwd=workspace,
                check=True,
                text=True,
                capture_output=True,
            )
            archived = workspace / archive_relative
            gtt.validate_finish_summary(gtt.read_json(archived / "finish-summary.json"), task_dir=archived)
            subprocess.run(["git", "add", "-A"], cwd=workspace, check=True)
            subprocess.run(["git", "commit", "-qm", f"archive fixture {token}"], cwd=workspace, check=True)
            branch = str(plan["naming"]["branch_name"])
            changed = set(
                subprocess.run(
                    ["git", "diff", "--name-only", "main...HEAD"],
                    cwd=workspace,
                    check=True,
                    text=True,
                    capture_output=True,
                ).stdout.splitlines()
            )
            self.assertTrue(changed)
            self.assertTrue(all(path.startswith(".trellis/tasks/archive/") for path in changed))
            self.assertFalse((workspace / ".trellis/.developer").exists())
            self.assertFalse((workspace / ".trellis/workspace").exists())
            return branch, changed

        branch_a, changed_a = build_and_archive(201, "a")
        branch_b, changed_b = build_and_archive(202, "b")
        self.assertEqual(changed_a & changed_b, set())
        forbidden = {
            ".trellis/guru-team/handoff.json",
            ".trellis/.developer",
        }
        for changed in (changed_a, changed_b):
            self.assertTrue(forbidden.isdisjoint(changed))
            self.assertFalse(any(path.startswith(".trellis/workspace/") for path in changed))
            self.assertFalse(any(path.startswith(".trellis/.runtime/") for path in changed))

        def merge_projection(name: str, branches: tuple[str, str]) -> set[str]:
            integration = fixture_root / name
            subprocess.run(
                ["git", "worktree", "add", "-q", "-b", name, str(integration), "main"],
                cwd=source,
                check=True,
            )
            subprocess.run(["git", "merge", "--no-edit", branches[0]], cwd=integration, check=True)
            second = subprocess.run(
                ["git", "merge", "--no-edit", branches[1]],
                cwd=integration,
                text=True,
                capture_output=True,
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            conflicts = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=U"],
                cwd=integration,
                check=True,
                text=True,
                capture_output=True,
            ).stdout.splitlines()
            self.assertEqual(conflicts, [])
            return set(
                subprocess.run(
                    ["git", "ls-tree", "-r", "--name-only", "HEAD", ".trellis/tasks/archive"],
                    cwd=integration,
                    check=True,
                    text=True,
                    capture_output=True,
                ).stdout.splitlines()
            )

        projection_ab = merge_projection("integration-ab", (branch_a, branch_b))
        projection_ba = merge_projection("integration-ba", (branch_b, branch_a))
        self.assertEqual(projection_ab, projection_ba)
        self.assertEqual(projection_ab, changed_a | changed_b)


class HumanMarkdownArtifactResolverTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".trellis/tasks").mkdir(parents=True)
        self.task_name = "07-09-061-task-markdown-review-table"
        self.task_rel = f".trellis/tasks/{self.task_name}"
        self.task_dir = self.root / self.task_rel
        self.task_dir.mkdir(parents=True)
        (self.task_dir / "task.json").write_text('{"title":"Human artifacts"}\n', encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_artifacts(self, task_dir: Path, names: list[str]) -> None:
        for name in names:
            task_dir.mkdir(parents=True, exist_ok=True)
            (task_dir / name).write_text(f"# {name}\n\n内容。\n", encoding="utf-8")

    def artifact_by_filename(self, payload: dict[str, object]) -> dict[str, dict[str, object]]:
        artifacts = payload["markdown_artifacts"]
        self.assertIsInstance(artifacts, list)
        return {str(item["filename"]): item for item in artifacts}  # type: ignore[index]

    def test_resolve_active_task_returns_three_planning_artifacts_only(self) -> None:
        self.write_artifacts(self.task_dir, ["prd.md", "design.md", "implement.md"])
        for intermediate in [
            "check.jsonl",
            "finish-summary-index.json",
            "issue-scope-ledger.json",
            "closeout-plan.json",
        ]:
            (self.task_dir / intermediate).write_text("{}\n", encoding="utf-8")

        payload = gtt.cmd_resolve_human_artifacts(
            resolve_human_artifacts_args(root=str(self.root), task=self.task_rel)
        )

        self.assertEqual(payload["status"], "ok")
        self.assertFalse(payload["archived"])
        self.assertEqual(payload["task_dir_relative"], self.task_rel)
        artifacts = self.artifact_by_filename(payload)
        self.assertEqual(
            list(artifacts),
            ["prd.md", "design.md", "implement.md"],
        )
        for filename, artifact in artifacts.items():
            self.assertTrue(artifact["exists"], filename)
            self.assertEqual(artifact["status"], "已生成")
            self.assertEqual(artifact["path"], f"{self.task_rel}/{filename}")
            self.assertEqual(artifact["link"], str((self.task_dir / filename).resolve()))
        artifact_text = json.dumps(payload, ensure_ascii=False)
        self.assertNotIn("check.jsonl", artifact_text)
        self.assertNotIn("finish-summary-index.json", artifact_text)
        self.assertNotIn("issue-scope-ledger.json", artifact_text)
        self.assertNotIn("closeout-plan.json", artifact_text)

    def test_missing_artifacts_have_no_dead_links(self) -> None:
        self.write_artifacts(self.task_dir, ["prd.md"])

        payload = gtt.cmd_resolve_human_artifacts(
            resolve_human_artifacts_args(root=str(self.root), task=self.task_name)
        )

        artifacts = self.artifact_by_filename(payload)
        self.assertTrue(artifacts["prd.md"]["exists"])
        self.assertEqual(artifacts["prd.md"]["link"], str((self.task_dir / "prd.md").resolve()))
        self.assertFalse(artifacts["design.md"]["exists"])
        self.assertEqual(artifacts["design.md"]["status"], "未生成")
        self.assertEqual(artifacts["design.md"]["link"], "")

    def test_resolve_archive_task_when_active_task_is_missing(self) -> None:
        shutil.rmtree(self.task_dir)
        archived = self.root / f".trellis/tasks/archive/2026-07/{self.task_name}"
        archived.mkdir(parents=True)
        (archived / "task.json").write_text('{"title":"Archived human artifacts"}\n', encoding="utf-8")
        self.write_artifacts(archived, ["prd.md", "design.md", "implement.md"])

        payload = gtt.cmd_resolve_human_artifacts(
            resolve_human_artifacts_args(root=str(self.root), task=self.task_name)
        )

        archived_rel = f".trellis/tasks/archive/2026-07/{self.task_name}"
        self.assertTrue(payload["archived"])
        self.assertEqual(payload["task_dir_relative"], archived_rel)
        artifacts = self.artifact_by_filename(payload)
        self.assertEqual(list(artifacts), ["prd.md", "design.md", "implement.md"])
        self.assertTrue(all(artifact["exists"] for artifact in artifacts.values()))


class TaskRuntimeIdentityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.task_slug = "runtime-identity"
        self.workspace_slug = "runtime-identity-workspace"
        self.branch = "feat/runtime-identity"
        self.task_ref = f".trellis/tasks/{self.task_slug}"
        self.task_dir = self.root / self.task_ref
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Runtime Test"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "runtime@example.invalid"],
            cwd=self.root,
            check=True,
        )
        (self.root / ".gitignore").write_text(
            ".trellis/.runtime/\n",
            encoding="utf-8",
        )
        (self.root / "README.md").write_text("runtime identity fixture\n", encoding="utf-8")
        subprocess.run(["git", "add", ".gitignore", "README.md"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "test: initialize runtime identity fixture"], cwd=self.root, check=True)
        subprocess.run(["git", "checkout", "-qb", self.branch], cwd=self.root, check=True)
        self.task_dir.mkdir(parents=True)
        gtt.write_json(
            self.task_dir / "task.json",
            {
                "id": self.task_slug,
                "name": self.task_slug,
                "title": "Runtime identity",
                "status": "in_progress",
                "branch": self.branch,
                "base_branch": "main",
            },
        )
        gtt.write_json(
            self.task_dir / "issue-scope-ledger.json",
            {
                "primary_issue": {"number": 161, "title": "AI-first workflow"},
                "close_issues": [{"number": 161}],
                "related_issues": [],
                "followup_issues": [],
            },
        )
        gtt.write_runtime_mappings(
            self.root,
            gtt.DEFAULTS,
            {
                "workspace_slug": self.workspace_slug,
                "task_slug": self.task_slug,
                "task_dir": self.task_ref,
                "branch_name": self.branch,
            },
            self.root,
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_synthesizes_runtime_identity_from_current_contract(self) -> None:
        identity = gtt.load_task_runtime_identity(self.task_dir, gtt.DEFAULTS)

        self.assertEqual(identity["_identity_source"], "task_json_runtime_mapping")
        self.assertEqual(identity["task_slug"], self.task_slug)
        self.assertEqual(identity["task_artifact_dir"], self.task_ref)
        self.assertEqual(identity["workspace_slug"], self.workspace_slug)
        self.assertEqual(identity["branch_name"], self.branch)
        self.assertEqual(identity["base_branch"], "main")
        self.assertEqual(identity["source_issue"]["number"], 161)
        self.assertRegex(identity["base_head_sha"], r"^[0-9a-f]{40}$")

    def test_mismatched_task_mapping_fails_closed(self) -> None:
        mapping_path = gtt.runtime_task_path(self.root, gtt.DEFAULTS, self.task_slug)
        mapping = gtt.read_json(mapping_path)
        mapping["task_artifact_dir"] = ".trellis/tasks/other-task"
        gtt.write_json(mapping_path, mapping)

        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.load_task_runtime_identity(self.task_dir, gtt.DEFAULTS)

        self.assertIn("does not match task.json", str(raised.exception))

    def test_worktree_branch_mismatch_fails_closed(self) -> None:
        with (
            mock.patch.object(
                gtt,
                "worktree_records",
                return_value=[
                    {
                        "worktree": str(self.root),
                        "branch": "refs/heads/feat/other-task",
                    }
                ],
            ),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.load_task_runtime_identity(self.task_dir, gtt.DEFAULTS)

        self.assertIn("worktree identity does not match", str(raised.exception))


class WorkspaceBoundaryGuardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.source = base / "source"
        self.workspace = base / "worktrees/060-workspace-boundary-guard"
        self.task_rel = ".trellis/tasks/07-08-060-workspace-boundary-guard"
        self.task_dir = self.workspace / self.task_rel
        self.source_task_dir = self.source / self.task_rel
        for root in [self.source, self.workspace]:
            (root / ".trellis/guru-team").mkdir(parents=True)
            (root / ".trellis/tasks").mkdir(parents=True)
            (root / ".trellis/guru-team/config.yml").write_text(
                "github_repo: owner/repo\n",
                encoding="utf-8",
            )
        self.task_dir.mkdir(parents=True)
        gtt.write_json(
            self.task_dir / "task.json",
            {
                "id": "060-workspace-boundary-guard",
                "name": "060-workspace-boundary-guard",
                "title": "Boundary task",
                "status": "in_progress",
                "branch": "chore/060-workspace-boundary-guard",
                "base_branch": "main",
            },
        )
        for name in ["prd.md", "design.md", "implement.md"]:
            (self.task_dir / name).write_text(f"# {name}\n\n内容。\n", encoding="utf-8")
        self.task_context = {
            "schema_version": "1.0", "task_artifact_dir": self.task_rel,
            "task_slug": "060-workspace-boundary-guard", "workspace_slug": "060-workspace-boundary-guard",
            "task_title": "Boundary task", "task_workspace_id": "060-workspace-boundary-guard",
            "branch_name": "chore/060-workspace-boundary-guard", "base_branch": "main",
            "base_ref": "main", "base_head_sha": "", "remote_head_sha": "",
            "source_issue": {"number": 60}, "source_repo": {"repo": "owner/repo", "url": ""},
            "assignee": "tester", "actor": {"login": "tester"}, "issue_scope_ledger_seed": {},
            "intake_summary": {"duplicate_decision": {}, "naming_quality": {}, "confirmation": {}},
        }
        gtt.write_runtime_mappings(
            self.source,
            gtt.DEFAULTS,
            {
                "workspace_slug": "060-workspace-boundary-guard",
                "task_slug": "060-workspace-boundary-guard",
                "task_dir": self.task_rel,
                "branch_name": "chore/060-workspace-boundary-guard",
            },
            self.workspace,
        )
        records = [
            {"worktree": str(self.source), "branch": "refs/heads/main"},
            {
                "worktree": str(self.workspace),
                "branch": "refs/heads/chore/060-workspace-boundary-guard",
            },
        ]
        self.patches = [
            mock.patch.object(gtt, "worktree_records", return_value=records),
            mock.patch.object(gtt, "diff_base_ref", return_value="main"),
            mock.patch.object(
                gtt,
                "run",
                return_value=mock.Mock(returncode=0, stdout=f"{'a' * 40}\n"),
            ),
        ]
        for patcher in self.patches:
            patcher.start()

    def tearDown(self) -> None:
        for patcher in reversed(self.patches):
            patcher.stop()
        self.tmp.cleanup()

    def test_check_workspace_boundary_reports_ok_snapshot(self) -> None:
        payload = gtt.cmd_check_workspace_boundary(boundary_args(root=str(self.workspace), task=self.task_rel))
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["expected_workspace"], str(self.workspace.resolve()))
        self.assertEqual(payload["actual_repo_root"], str(self.workspace.resolve()))
        self.assertEqual(payload["source_checkout"], str(self.source.resolve()))
        self.assertEqual(payload["task_dir_relative"], self.task_rel)
        self.assertEqual(payload["errors"], [])

    def test_check_workspace_boundary_rebuilds_deleted_runtime_cache(self) -> None:
        for root in [self.source, self.workspace]:
            gtt.runtime_workspace_path(root, gtt.DEFAULTS, "060-workspace-boundary-guard").unlink()
            gtt.runtime_task_path(root, gtt.DEFAULTS, "060-workspace-boundary-guard").unlink(missing_ok=True)
        payload = gtt.cmd_check_workspace_boundary(
            boundary_args(root=str(self.workspace), task=self.task_rel)
        )

        self.assertEqual(payload["status"], "ok")
        self.assertTrue(gtt.runtime_workspace_path(self.workspace, gtt.DEFAULTS, "060-workspace-boundary-guard").is_file())
        self.assertTrue(gtt.runtime_task_path(self.workspace, gtt.DEFAULTS, "060-workspace-boundary-guard").is_file())

    def test_check_workspace_boundary_blocks_without_task_runtime_identity(self) -> None:
        self.source_task_dir.mkdir(parents=True)
        (self.source_task_dir / "task.json").write_text('{"title":"Wrong task copy"}\n', encoding="utf-8")
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.cmd_check_workspace_boundary(boundary_args(root=str(self.source), task=self.task_rel))
        payload = raised.exception.payload
        self.assertEqual(payload["status"], "blocked")
        self.assertTrue(any("Task runtime identity" in error for error in payload["errors"]))

    def test_ordinary_task_resolution_rejects_plan_only_archived_directory(self) -> None:
        archived = self.workspace / ".trellis/tasks/archive/2026-07/07-08-plan-only"
        archived.mkdir(parents=True)
        (archived / gtt.CLOSEOUT_PLAN_ARTIFACT).write_text("{}\n", encoding="utf-8")

        self.assertIsNone(gtt.resolve_existing_task_dir(self.workspace, str(archived)))
        for task_arg in [
            archived.name,
            str(self.workspace / ".trellis/tasks" / archived.name),
            str(archived.relative_to(self.workspace)),
            str(archived),
        ]:
            with self.subTest(task_arg=task_arg):
                self.assertEqual(
                    gtt.resolve_finish_work_task_dir(self.workspace, task_arg),
                    gtt.closeout_lexical_path(archived),
                )
        with self.assertRaises(gtt.WorkflowError):
            gtt.cmd_check_workspace_boundary(
                boundary_args(root=str(self.workspace), task=str(archived))
            )

    def test_finish_work_prefers_active_task_over_same_name_plan_only_archive(self) -> None:
        archived = self.workspace / ".trellis/tasks/archive/2026-06" / self.task_dir.name
        archived.mkdir(parents=True)
        (archived / gtt.CLOSEOUT_PLAN_ARTIFACT).write_text("{}\n", encoding="utf-8")

        for task_arg in [
            self.task_dir.name,
            str(self.task_dir.relative_to(self.workspace)),
            str(self.task_dir),
        ]:
            with self.subTest(task_arg=task_arg):
                self.assertEqual(
                    gtt.resolve_finish_work_task_dir(self.workspace, task_arg),
                    self.task_dir.resolve(),
                )

    def test_finish_work_prefers_ordinary_archive_over_same_name_plan_only_archive(self) -> None:
        shutil.rmtree(self.task_dir)
        ordinary = self.workspace / ".trellis/tasks/archive/2026-06" / self.task_dir.name
        ordinary.mkdir(parents=True)
        (ordinary / "task.json").write_text(
            '{"title":"Ordinary archived task"}\n',
            encoding="utf-8",
        )
        plan_only = self.workspace / ".trellis/tasks/archive/2026-07" / self.task_dir.name
        plan_only.mkdir(parents=True)
        (plan_only / gtt.CLOSEOUT_PLAN_ARTIFACT).write_text("{}\n", encoding="utf-8")

        self.assertEqual(
            gtt.resolve_finish_work_task_dir(self.workspace, self.task_dir.name),
            ordinary.resolve(),
        )

    def test_finish_work_uses_unique_plan_only_fallback_after_ordinary_not_found(self) -> None:
        shutil.rmtree(self.task_dir)
        archived = self.workspace / ".trellis/tasks/archive/2026-07" / self.task_dir.name
        archived.mkdir(parents=True)
        (archived / gtt.CLOSEOUT_PLAN_ARTIFACT).write_text("{}\n", encoding="utf-8")

        self.assertIsNone(gtt.resolve_existing_task_dir(self.workspace, self.task_dir.name))
        self.assertEqual(
            gtt.resolve_finish_work_task_dir(self.workspace, self.task_dir.name),
            gtt.closeout_lexical_path(archived),
        )

    def test_finish_work_exact_plan_only_locator_falls_back_after_ordinary_not_found(self) -> None:
        archived = self.workspace / ".trellis/tasks/archive/2026-07/07-08-exact-plan-only"
        archived.mkdir(parents=True)
        (archived / gtt.CLOSEOUT_PLAN_ARTIFACT).write_text("{}\n", encoding="utf-8")
        same_name = self.workspace / ".trellis/tasks/archive/2026-06" / archived.name
        same_name.mkdir(parents=True)
        (same_name / gtt.CLOSEOUT_PLAN_ARTIFACT).write_text("{}\n", encoding="utf-8")

        self.assertIsNone(gtt.resolve_existing_task_dir(self.workspace, str(archived)))
        self.assertEqual(
            gtt.resolve_finish_work_task_dir(self.workspace, str(archived)),
            gtt.closeout_lexical_path(archived),
        )

    def test_finish_work_rejects_ambiguous_plan_only_basename(self) -> None:
        shutil.rmtree(self.task_dir)
        archived_paths = []
        for month in ["2026-06", "2026-07"]:
            archived = self.workspace / ".trellis/tasks/archive" / month / self.task_dir.name
            archived.mkdir(parents=True)
            (archived / gtt.CLOSEOUT_PLAN_ARTIFACT).write_text("{}\n", encoding="utf-8")
            archived_paths.append(archived)

        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.resolve_finish_work_task_dir(self.workspace, self.task_dir.name)

        self.assertIn("multiple archived plan-only tasks", str(raised.exception))
        self.assertEqual(
            raised.exception.payload["candidates"],
            [
                str(path.relative_to(self.workspace))
                for path in reversed(archived_paths)
            ],
        )

    def test_finish_work_symlink_input_fails_before_any_resolver_fallback(self) -> None:
        archived = self.workspace / ".trellis/tasks/archive/2026-07/07-08-plan-only-no-fallback"
        archived.mkdir(parents=True)
        (archived / gtt.CLOSEOUT_PLAN_ARTIFACT).write_text("{}\n", encoding="utf-8")
        alias = archived.parent / "plan-only-alias-no-fallback"
        alias.symlink_to(archived, target_is_directory=True)

        with (
            mock.patch.object(gtt, "resolve_existing_task_dir") as ordinary_resolver,
            mock.patch.object(gtt, "plan_only_archived_task_candidate") as plan_only_fallback,
        ):
            with self.assertRaises(gtt.WorkflowError):
                gtt.resolve_finish_work_task_dir(self.workspace, str(alias))

        ordinary_resolver.assert_not_called()
        plan_only_fallback.assert_not_called()

    def test_finish_work_basename_rejects_direct_active_and_repo_root_aliases(self) -> None:
        target = self.workspace / ".trellis/tasks/07-08-basename-alias-target"
        target.mkdir(parents=True)
        (target / "task.json").write_text('{"title":"Alias target"}\n', encoding="utf-8")

        aliases = [
            self.workspace / ".trellis/tasks/07-08-active-basename-alias",
            self.workspace / "07-08-root-basename-alias",
        ]
        for alias in aliases:
            alias.symlink_to(target, target_is_directory=True)
            with self.subTest(alias=alias):
                with mock.patch.object(gtt, "resolve_existing_task_dir") as ordinary_resolver:
                    with self.assertRaises(gtt.WorkflowError) as raised:
                        gtt.resolve_finish_work_task_dir(self.workspace, alias.name)
                self.assertIn("symbolic-link", str(raised.exception))
                ordinary_resolver.assert_not_called()

    def test_finish_work_basename_rejects_matching_ordinary_archive_alias(self) -> None:
        shutil.rmtree(self.task_dir)
        target = self.workspace / ".trellis/tasks/archive/2026-06/ordinary-alias-target"
        target.mkdir(parents=True)
        (target / "task.json").write_text(
            '{"title":"Ordinary archive alias target"}\n',
            encoding="utf-8",
        )
        alias = self.workspace / ".trellis/tasks/archive/2026-07/07-08-ordinary-archive-alias"
        alias.parent.mkdir(parents=True)
        alias.symlink_to(target, target_is_directory=True)

        with mock.patch.object(gtt, "resolve_existing_task_dir") as ordinary_resolver:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.resolve_finish_work_task_dir(self.workspace, alias.name)

        self.assertIn("symbolic-link", str(raised.exception))
        ordinary_resolver.assert_not_called()

    def test_finish_work_basename_rejects_matching_restored_plan_only_alias(self) -> None:
        shutil.rmtree(self.task_dir)
        target = self.workspace / ".trellis/tasks/archive/2026-06/restored-plan-only-target"
        target.mkdir(parents=True)
        (target / gtt.CLOSEOUT_PLAN_ARTIFACT).write_text("{}\n", encoding="utf-8")
        (target / "task.json").write_text(
            '{"title":"Restored plan-only alias target"}\n',
            encoding="utf-8",
        )
        alias = self.workspace / ".trellis/tasks/archive/2026-07/07-08-restored-plan-only-alias"
        alias.parent.mkdir(parents=True)
        alias.symlink_to(target, target_is_directory=True)

        with mock.patch.object(gtt, "resolve_existing_task_dir") as ordinary_resolver:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.resolve_finish_work_task_dir(self.workspace, alias.name)

        self.assertIn("symbolic-link", str(raised.exception))
        ordinary_resolver.assert_not_called()

    def test_finish_work_basename_ignores_unmatched_archive_alias(self) -> None:
        shutil.rmtree(self.task_dir)
        empty_target = self.workspace / ".trellis/tasks/archive/2026-05/empty-alias-target"
        empty_target.mkdir(parents=True)
        alias = self.workspace / ".trellis/tasks/archive/2026-07" / self.task_dir.name
        alias.parent.mkdir(parents=True)
        alias.symlink_to(empty_target, target_is_directory=True)
        ordinary = self.workspace / ".trellis/tasks/archive/2026-06" / self.task_dir.name
        ordinary.mkdir(parents=True)
        (ordinary / "task.json").write_text(
            '{"title":"Later ordinary archive match"}\n',
            encoding="utf-8",
        )

        self.assertEqual(
            gtt.resolve_finish_work_task_dir(self.workspace, self.task_dir.name),
            ordinary.resolve(),
        )

    def test_finish_work_basename_ignores_unmatched_repo_root_alias(self) -> None:
        empty_target = self.workspace / "empty-root-alias-target"
        empty_target.mkdir()
        alias = self.workspace / self.task_dir.name
        alias.symlink_to(empty_target, target_is_directory=True)

        self.assertEqual(
            gtt.resolve_finish_work_task_dir(self.workspace, self.task_dir.name),
            self.task_dir.resolve(),
        )

    def test_finish_work_basename_ignores_unmatched_active_alias(self) -> None:
        shutil.rmtree(self.task_dir)
        empty_target = self.workspace / ".trellis/tasks/empty-active-alias-target"
        empty_target.mkdir(parents=True)
        self.task_dir.symlink_to(empty_target, target_is_directory=True)
        ordinary = self.workspace / ".trellis/tasks/archive/2026-07" / self.task_dir.name
        ordinary.mkdir(parents=True)
        (ordinary / "task.json").write_text(
            '{"title":"Ordinary archive after unmatched active alias"}\n',
            encoding="utf-8",
        )

        self.assertEqual(
            gtt.resolve_finish_work_task_dir(self.workspace, self.task_dir.name),
            ordinary.resolve(),
        )

    def test_finish_work_plan_only_resolution_rejects_internal_and_external_aliases(self) -> None:
        archived = self.workspace / ".trellis/tasks/archive/2026-07/07-08-plan-only-alias"
        archived.mkdir(parents=True)
        (archived / gtt.CLOSEOUT_PLAN_ARTIFACT).write_text("{}\n", encoding="utf-8")

        internal_final = archived.parent / "final-alias"
        internal_final.symlink_to(archived, target_is_directory=True)
        internal_ancestor = self.workspace / ".trellis/tasks/archive-alias"
        internal_ancestor.symlink_to(
            self.workspace / ".trellis/tasks/archive",
            target_is_directory=True,
        )
        aliases = self.workspace / "aliases"
        aliases.mkdir()
        multilevel_second = aliases / "second"
        multilevel_second.symlink_to(archived, target_is_directory=True)
        multilevel_first = aliases / "first"
        multilevel_first.symlink_to(multilevel_second, target_is_directory=True)
        dangling = aliases / "dangling"
        dangling.symlink_to(self.workspace / "missing-plan-only", target_is_directory=True)
        loop = aliases / "loop"
        loop.symlink_to(loop, target_is_directory=True)

        external_alias = Path(self.tmp.name) / "external-plan-only-alias"
        external_alias.symlink_to(archived, target_is_directory=True)
        sources = [
            internal_final,
            internal_ancestor / "2026-07" / archived.name,
            multilevel_first,
            dangling,
            loop,
            external_alias,
        ]
        for source in sources:
            for task_arg in [str(source), os.path.relpath(source, self.workspace)]:
                with self.subTest(source=source.name, task_arg=task_arg):
                    with self.assertRaises(gtt.WorkflowError) as raised:
                        gtt.resolve_finish_work_task_dir(self.workspace, task_arg)
                    self.assertTrue(
                        "symbolic-link" in str(raised.exception)
                        or "repository root" in str(raised.exception)
                        or "current repository" in str(raised.exception)
                    )

        (archived / "task.json").write_text(
            '{"title":"restored dirty task metadata"}\n',
            encoding="utf-8",
        )
        for task_arg in [str(internal_final), str(external_alias)]:
            with self.subTest(restored_task_json=task_arg):
                with self.assertRaises(gtt.WorkflowError):
                    gtt.resolve_finish_work_task_dir(self.workspace, task_arg)

    @unittest.skipUnless(sys.platform == "darwin", "Darwin /var system alias compatibility")
    def test_finish_work_plan_only_resolution_accepts_fixed_darwin_var_alias(self) -> None:
        canonical_root = self.workspace.resolve()
        canonical_prefix = Path("/private/var")
        try:
            suffix = canonical_root.relative_to(canonical_prefix)
        except ValueError:
            self.skipTest("temporary workspace is not under /private/var")
        archived = canonical_root / ".trellis/tasks/archive/2026-07/07-08-plan-only-var"
        archived.mkdir(parents=True)
        (archived / gtt.CLOSEOUT_PLAN_ARTIFACT).write_text("{}\n", encoding="utf-8")
        aliased = Path("/var") / suffix / archived.relative_to(canonical_root)

        self.assertEqual(
            gtt.resolve_finish_work_task_dir(canonical_root, str(aliased)),
            gtt.closeout_lexical_path(archived),
        )

    def test_check_workspace_boundary_blocks_wrong_cwd(self) -> None:
        self.source_task_dir.mkdir(parents=True)
        (self.source_task_dir / "task.json").write_text('{"title":"Wrong task copy"}\n', encoding="utf-8")
        payload = gtt.workspace_boundary_snapshot(
            self.source,
            gtt.DEFAULTS,
            self.task_context,
            self.source_task_dir,
        )
        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["expected_workspace"], str(self.workspace.resolve()))
        self.assertTrue(any("workspace boundary mismatch" in error for error in payload["errors"]))

    def test_workspace_guard_blocks_source_checkout_with_same_task_artifact(self) -> None:
        self.source_task_dir.mkdir(parents=True)
        (self.source_task_dir / "task.json").write_text('{"title":"Wrong task copy"}\n', encoding="utf-8")
        (self.source_task_dir / "check.jsonl").write_text(
            '{"kind":"phase2-evidence"}\n', encoding="utf-8"
        )
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.assert_workspace_boundary(
                self.source,
                gtt.DEFAULTS,
                self.task_context,
                self.source_task_dir,
            )
        payload = raised.exception.payload
        self.assertEqual(payload["status"], "blocked")
        self.assertTrue(any("source checkout contains current-task artifacts" in error for error in payload["errors"]))

    def test_wrong_phase2_artifact_argument_is_rejected(self) -> None:
        self.source_task_dir.mkdir(parents=True)
        (self.source_task_dir / "prd.md").write_text("# PRD\n", encoding="utf-8")
        with self.assertRaises(gtt.WorkflowError):
            gtt.phase2_reviewed_paths(
                self.workspace,
                [str(self.source_task_dir / "prd.md")],
            )


class PlanningAndPhase2GateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.task_ref = ".trellis/tasks/07-04-gates"
        self.task_dir = self.root / self.task_ref
        self.task_dir.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        (self.root / ".gitignore").write_text(".trellis/.runtime/\n", encoding="utf-8")
        gtt.write_json(self.task_dir / "task.json", {
            "id": "gate-task",
            "name": "gate-task",
            "title": "Gate task",
            "status": "planning",
            "scope": "issue #27",
            "branch": "feat/gate-task",
            "base_branch": "main",
        })
        for name, body in (
            ("prd.md", "# PRD\n\n## R1\n\nRequirement.\n"),
            ("design.md", "# Design\n\n## Docs SSOT Plan\n\n- Strategy: ssot_first\n"),
            ("implement.md", "# Implement\n\nImplementation plan.\n"),
        ):
            (self.task_dir / name).write_text(body, encoding="utf-8")

        packages = (
            Path(__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages"
        )
        self.planning_example = json.loads(
            (
                packages
                / "guru-approve-task-plan/examples/planning-approval.json"
            ).read_text(encoding="utf-8")
        )
        self.planning_schema = json.loads(
            (
                packages
                / "guru-approve-task-plan/schemas/planning-approval.schema.json"
            ).read_text(encoding="utf-8")
        )
        self.phase2_example = json.loads(
            (
                packages / "guru-check-task/examples/phase2-check.json"
            ).read_text(encoding="utf-8")
        )
        self.phase2_schema = json.loads(
            (
                packages / "guru-check-task/schemas/phase2-check.schema.json"
            ).read_text(encoding="utf-8")
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def planning_authored(self) -> dict[str, object]:
        fields = {
            "mode", "authority_refs", "docs_ssot_plan", "semantic_review",
            "typed_exit", "consumer", "reason",
        }
        return {
            key: copy.deepcopy(value)
            for key, value in self.planning_example.items()
            if key in fields
        }

    def phase2_authored(self) -> dict[str, object]:
        fields = {
            "mode", "reviewed_paths", "validation", "docs_ssot",
            "semantic_review", "typed_exit", "route", "reason", "consumer",
        }
        authored = {
            key: copy.deepcopy(value)
            for key, value in self.phase2_example.items()
            if key in fields
        }
        authored["reviewed_paths"] = [f"{self.task_ref}/prd.md"]
        return authored

    @staticmethod
    def nested_keys(value: object) -> set[str]:
        if isinstance(value, dict):
            return set(value) | set().union(
                *(PlanningAndPhase2GateTest.nested_keys(item) for item in value.values()),
                set(),
            )
        if isinstance(value, list):
            return set().union(
                *(PlanningAndPhase2GateTest.nested_keys(item) for item in value),
                set(),
            )
        return set()

    def test_planning_v3_is_compact_owner_private_and_valid(self) -> None:
        before = set(gtt.git_status_paths(self.root))
        with mock.patch.object(
            gtt, "planning_approval_schema", return_value=self.planning_schema
        ):
            payload = gtt.build_planning_approval_payload(
                self.root, self.task_dir, self.planning_authored()
            )
            artifact = gtt.planning_approval_path(self.root, self.task_dir)
            gtt.write_json(artifact, payload)
            checked_path, checked, errors = gtt.validate_planning_approval(
                self.root, self.task_dir
            )

        self.assertEqual(errors, [])
        self.assertEqual(checked_path, artifact)
        self.assertEqual(checked["schema_version"], "3.0")
        self.assertEqual(checked["typed_exit"], "approved")
        self.assertTrue(
            artifact.is_relative_to(
                self.root / ".trellis/.runtime/guru-team/owner-checkpoints"
            )
        )
        self.assertFalse((self.task_dir / "planning-approval.json").exists())
        self.assertEqual(set(gtt.git_status_paths(self.root)), before)
        self.assertTrue({
            "confirmation", "confirmed_action_id", "human_confirmation",
            "user_confirmation", "agent_assignment", "liveness",
        }.isdisjoint(self.nested_keys(checked)))

    def test_planning_v3_closed_routes_and_invalid_pass_fail_closed(self) -> None:
        cases = {
            "approved": (
                "passed",
                {"kind": "workflow", "id": "phase-1-task-activation"},
            ),
            "revision_required": (
                "revision_required",
                {"kind": "skill", "id": "guru-approve-task-plan"},
            ),
            "clarify_scope": (
                "clarify_scope",
                {"kind": "workflow", "id": "guru-task-plan-clarify-scope-router"},
            ),
            "blocked": (
                "blocked",
                {"kind": "stop", "id": "task-plan-approval-blocked"},
            ),
        }
        with mock.patch.object(
            gtt, "planning_approval_schema", return_value=self.planning_schema
        ):
            for typed_exit, (status, consumer) in cases.items():
                with self.subTest(typed_exit=typed_exit):
                    authored = self.planning_authored()
                    semantic = authored["semantic_review"]
                    semantic["status"] = status
                    semantic["findings"] = []
                    semantic["revision_actions"] = (
                        ["Revise the task-local plan."]
                        if typed_exit == "revision_required"
                        else []
                    )
                    semantic["scope_proposals"] = (
                        ["scope-proposal:R13"]
                        if typed_exit == "clarify_scope"
                        else []
                    )
                    semantic["blocking_reasons"] = (
                        ["Current authority is unavailable."]
                        if typed_exit == "blocked"
                        else []
                    )
                    authored["typed_exit"] = typed_exit
                    authored["consumer"] = consumer
                    payload = gtt.build_planning_approval_payload(
                        self.root, self.task_dir, authored
                    )
                    self.assertEqual(payload["typed_exit"], typed_exit)

            invalid = self.planning_authored()
            invalid["semantic_review"]["findings"] = ["An open finding remains."]
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.build_planning_approval_payload(
                    self.root, self.task_dir, invalid
                )
            self.assertIn(
                "planning_approval_approved_findings_not_empty",
                raised.exception.payload["error_codes"],
            )

    def test_owner_checkpoints_reject_same_path_content_drift(self) -> None:
        with mock.patch.object(
            gtt, "planning_approval_schema", return_value=self.planning_schema
        ):
            planning = gtt.build_planning_approval_payload(
                self.root,
                self.task_dir,
                self.planning_authored(),
            )
            planning_path = gtt.planning_approval_path(self.root, self.task_dir)
            gtt.write_json(planning_path, planning)
            (self.task_dir / "prd.md").write_text(
                "# PRD\n\nA materially different requirement.\n",
                encoding="utf-8",
            )
            _path, _payload, planning_errors = gtt.validate_planning_approval(
                self.root,
                self.task_dir,
            )
        self.assertIn(
            "planning_approval_reviewed_content_stale",
            planning_errors,
        )

        dirty = ["src/example.py"]
        authored = self.phase2_authored()
        authored["reviewed_paths"] = dirty
        with (
            mock.patch.object(
                gtt, "load_phase2_check_schema", return_value=self.phase2_schema
            ),
            mock.patch.object(gtt, "current_head", return_value="2" * 40),
            mock.patch.object(gtt, "git_status_paths", return_value=dirty),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                side_effect=[
                    {
                        "algorithm": gtt.REVIEWED_CONTENT_ALGORITHM,
                        "sha256": "a" * 64,
                    },
                    {
                        "algorithm": gtt.REVIEWED_CONTENT_ALGORITHM,
                        "sha256": "b" * 64,
                    },
                ],
            ),
        ):
            phase2 = gtt.materialize_phase2_check_payload(
                self.root,
                self.task_dir,
                {},
                authored,
            )
            phase2_path = gtt.phase2_check_path(self.root, self.task_dir)
            gtt.write_json(phase2_path, phase2)
            _path, _payload, phase2_errors = gtt.validate_phase2_check(
                self.root,
                self.task_dir,
            )
        self.assertIn("phase2_check_reviewed_content_stale", phase2_errors)

    def test_owner_checkpoint_lifecycle_is_lazy_consumed_and_terminally_empty(self) -> None:
        checkpoint_root = (
            self.root
            / ".trellis/.runtime/guru-team"
            / gtt.AI_FIRST_OWNER_CHECKPOINT_DIR
        )
        paths = {
            artifact_name: gtt.ai_first_owner_checkpoint_path(
                self.root,
                self.task_dir,
                artifact_name,
            )
            for artifact_name in gtt.AI_FIRST_OWNER_ARTIFACTS
        }
        self.assertFalse(checkpoint_root.exists())

        planning_path = paths[gtt.PLANNING_APPROVAL_ARTIFACT]
        gtt.write_json(planning_path, {"owner": "planning", "state": "recoverable"})
        self.assertEqual(
            gtt.ai_first_retire_owner_checkpoints(
                self.root,
                self.task_dir,
                (gtt.PLANNING_APPROVAL_ARTIFACT,),
            ),
            [gtt.PLANNING_APPROVAL_ARTIFACT],
        )
        self.assertFalse(planning_path.exists())
        self.assertFalse(planning_path.parent.exists())

        for artifact_name, path in paths.items():
            gtt.write_json(path, {"owner": artifact_name, "state": "stale"})
        self.assertEqual(
            set(gtt.ai_first_retire_owner_checkpoints(
                self.root,
                self.task_dir,
                sorted(gtt.AI_FIRST_OWNER_ARTIFACTS),
            )),
            set(gtt.AI_FIRST_OWNER_ARTIFACTS),
        )
        self.assertFalse(checkpoint_root.exists())

    def test_owner_checkpoint_cleanup_rejects_unsafe_targets(self) -> None:
        artifact_name = gtt.PLANNING_APPROVAL_ARTIFACT
        checkpoint = gtt.ai_first_owner_checkpoint_path(
            self.root,
            self.task_dir,
            artifact_name,
        )
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        external = self.root / "external-owner-state.json"
        external.write_text("preserve\n", encoding="utf-8")
        checkpoint.symlink_to(external)
        with self.assertRaises(gtt.WorkflowError):
            gtt.ai_first_retire_owner_checkpoints(
                self.root,
                self.task_dir,
                (artifact_name,),
            )
        self.assertEqual(external.read_text(encoding="utf-8"), "preserve\n")
        checkpoint.unlink()

        checkpoint.mkdir()
        with self.assertRaises(gtt.WorkflowError):
            gtt.ai_first_retire_owner_checkpoints(
                self.root,
                self.task_dir,
                (artifact_name,),
            )
        self.assertTrue(checkpoint.is_dir())

    def test_terminal_owner_checkpoint_sweep_rejects_unknown_and_unsafe_residue(self) -> None:
        checkpoint = gtt.ai_first_owner_checkpoint_path(
            self.root,
            self.task_dir,
            gtt.TASK_FINALIZATION_GATE_ARTIFACT,
        )
        gtt.write_json(checkpoint, {"owner": "finalizer"})
        unknown = checkpoint.parent / "unknown-owner-state.json"
        unknown.write_text("{}\n", encoding="utf-8")
        with self.assertRaises(gtt.WorkflowError) as unknown_error:
            gtt.ai_first_sweep_terminal_owner_checkpoints(
                self.root,
                self.task_dir,
            )
        self.assertEqual(
            unknown_error.exception.payload["error_codes"],
            ["owner_checkpoint_residue_unknown"],
        )
        self.assertTrue(checkpoint.is_file())
        unknown.unlink()

        nested = checkpoint.parent / "nested-owner-state"
        nested.mkdir()
        with self.assertRaises(gtt.WorkflowError) as nested_error:
            gtt.ai_first_sweep_terminal_owner_checkpoints(
                self.root,
                self.task_dir,
            )
        self.assertEqual(
            nested_error.exception.payload["error_codes"],
            ["owner_checkpoint_residue_unsafe"],
        )
        self.assertTrue(checkpoint.is_file())
        nested.rmdir()

        external = self.root / "external-terminal-owner-state.json"
        external.write_text("preserve\n", encoding="utf-8")
        unsafe = checkpoint.parent / gtt.CONTEXT_DISCOVERY_RECOVERY_ARTIFACT
        unsafe.symlink_to(external)
        with self.assertRaises(gtt.WorkflowError) as unsafe_error:
            gtt.ai_first_sweep_terminal_owner_checkpoints(
                self.root,
                self.task_dir,
            )
        self.assertEqual(
            unsafe_error.exception.payload["error_codes"],
            ["owner_checkpoint_residue_unsafe"],
        )
        self.assertEqual(external.read_text(encoding="utf-8"), "preserve\n")
        self.assertTrue(checkpoint.is_file())

    def test_phase2_v4_is_compact_owner_private_and_independent_of_planning_checkpoint(self) -> None:
        with (
            mock.patch.object(
                gtt, "load_phase2_check_schema", return_value=self.phase2_schema
            ),
            mock.patch.object(gtt, "git_status_paths", return_value=[]),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={
                    "algorithm": gtt.REVIEWED_CONTENT_ALGORITHM,
                    "sha256": "f" * 64,
                },
            ),
            mock.patch.object(gtt, "current_head", return_value="2" * 40),
        ):
            payload = gtt.materialize_phase2_check_payload(
                self.root, self.task_dir, {}, self.phase2_authored()
            )
            artifact = gtt.phase2_check_path(self.root, self.task_dir)
            gtt.write_json(artifact, payload)
            checked_path, checked, errors = gtt.validate_phase2_check(
                self.root, self.task_dir
            )

        self.assertEqual(errors, [])
        self.assertEqual(checked_path, artifact)
        self.assertEqual(checked["schema_version"], "4.0")
        self.assertEqual(checked["typed_exit"], "passed")
        self.assertTrue(artifact.is_file())
        self.assertFalse((self.task_dir / "phase2-check.json").exists())
        self.assertTrue({
            "confirmation", "confirmed_action_id", "human_confirmation",
            "agent_assignment", "implementation_handoff", "liveness",
            "review_report", "review_reports",
        }.isdisjoint(self.nested_keys(checked)))

    def test_phase2_v4_rejects_unreviewed_content_dirty(self) -> None:
        unknown_path = "unknown.txt"
        with (
            mock.patch.object(
                gtt, "load_phase2_check_schema", return_value=self.phase2_schema
            ),
            mock.patch.object(gtt, "current_head", return_value="2" * 40),
            mock.patch.object(
                gtt,
                "git_status_paths",
                return_value=[unknown_path],
            ),
        ):
            with self.assertRaises(gtt.WorkflowError) as dirty:
                gtt.materialize_phase2_check_payload(
                    self.root, self.task_dir, {}, self.phase2_authored()
                )
        self.assertEqual(dirty.exception.payload["paths"], [unknown_path])

    def test_phase2_v4_checker_excludes_private_runtime_dirty(self) -> None:
        reviewed_path = f"{self.task_ref}/prd.md"
        runtime_path = ".trellis/.runtime/guru-team/debug.json"
        with (
            mock.patch.object(
                gtt, "load_phase2_check_schema", return_value=self.phase2_schema
            ),
            mock.patch.object(gtt, "current_head", return_value="2" * 40),
            mock.patch.object(gtt, "git_status_paths", return_value=[reviewed_path]),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={
                    "algorithm": gtt.REVIEWED_CONTENT_ALGORITHM,
                    "sha256": "f" * 64,
                },
            ),
        ):
            payload = gtt.materialize_phase2_check_payload(
                self.root,
                self.task_dir,
                {},
                self.phase2_authored(),
            )
        artifact = gtt.phase2_check_path(self.root, self.task_dir)
        gtt.write_json(artifact, payload)

        with (
            mock.patch.object(
                gtt, "load_phase2_check_schema", return_value=self.phase2_schema
            ),
            mock.patch.object(gtt, "current_head", return_value="2" * 40),
            mock.patch.object(
                gtt,
                "git_status_paths",
                return_value=[reviewed_path, runtime_path],
            ),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={
                    "algorithm": gtt.REVIEWED_CONTENT_ALGORITHM,
                    "sha256": "f" * 64,
                },
            ),
        ):
            _path, _payload, errors = gtt.validate_phase2_check(
                self.root,
                self.task_dir,
            )

        self.assertEqual(errors, [])

    def test_phase2_v4_rejects_invalid_pass(self) -> None:
        invalid = self.phase2_authored()
        invalid["semantic_review"]["findings"] = [{
            "id": "F1",
            "severity": "P2",
            "summary": "A supported current-scope defect remains.",
            "path": "src/example.py",
            "status": "open",
        }]
        invalid["semantic_review"]["scope_decisions"] = [{
            "id": "C1",
            "disposition": "current_scope",
            "summary": "The current implementation remains incorrect.",
            "normal_path_reproduction": "The supported path reproduces the defect.",
            "finding_id": "F1",
        }]
        with (
            mock.patch.object(
                gtt, "load_phase2_check_schema", return_value=self.phase2_schema
            ),
            mock.patch.object(gtt, "current_head", return_value="2" * 40),
            mock.patch.object(gtt, "git_status_paths", return_value=[]),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={
                    "algorithm": gtt.REVIEWED_CONTENT_ALGORITHM,
                    "sha256": "f" * 64,
                },
            ),
            self.assertRaises(gtt.WorkflowError) as invalid_pass,
        ):
            gtt.materialize_phase2_check_payload(
                self.root, self.task_dir, {}, invalid
            )
        self.assertIn(
            "phase2_check_passed_has_open_findings",
            invalid_pass.exception.payload["error_codes"],
        )

    def test_phase2_recorder_rejects_committed_trailing_whitespace_against_base(self) -> None:
        subprocess.run(["git", "config", "user.name", "Phase 2 Test"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "phase2@example.invalid"],
            cwd=self.root,
            check=True,
        )
        task = gtt.read_json(self.task_dir / "task.json")
        task["status"] = "in_progress"
        gtt.write_json(self.task_dir / "task.json", task)
        source = self.root / "src/committed.py"
        source.parent.mkdir(parents=True)
        source.write_text("value = 1\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(phase2): #27 添加基线"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "checkout", "-q", "-b", "feat/gate-task"],
            cwd=self.root,
            check=True,
        )
        source.write_text("value = 2  \n", encoding="utf-8")
        subprocess.run(["git", "add", "src/committed.py"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(phase2): #27 引入已提交空白"],
            cwd=self.root,
            check=True,
        )
        with (
            mock.patch.object(
                gtt,
                "load_task_runtime_identity",
                return_value={"base_branch": "main"},
            ),
            mock.patch.object(gtt, "assert_workspace_boundary", return_value={"status": "ok"}),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_record_phase2_check(argparse.Namespace(
                root=str(self.root),
                task=self.task_ref,
                input="unused.json",
                dry_run=True,
            ))

        self.assertIn(
            "git-diff-check:src/committed.py:1: trailing whitespace.",
            raised.exception.payload["errors"],
        )
        self.assertEqual(
            raised.exception.payload["base_ref"],
            gtt.diff_base_ref(self.root, "main"),
        )

    def test_phase2_recorder_rejects_committed_invalid_json_against_base(self) -> None:
        subprocess.run(["git", "config", "user.name", "Phase 2 Test"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "phase2@example.invalid"],
            cwd=self.root,
            check=True,
        )
        task = gtt.read_json(self.task_dir / "task.json")
        task["status"] = "in_progress"
        gtt.write_json(self.task_dir / "task.json", task)
        source = self.root / "config/committed.json"
        source.parent.mkdir(parents=True)
        source.write_text('{"value": 1}\n', encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(phase2): #27 添加 JSON 基线"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "checkout", "-q", "-b", "feat/gate-task"],
            cwd=self.root,
            check=True,
        )
        source.write_text("{\n", encoding="utf-8")
        subprocess.run(["git", "add", "config/committed.json"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(phase2): #27 引入无效 JSON"],
            cwd=self.root,
            check=True,
        )
        with (
            mock.patch.object(
                gtt,
                "load_task_runtime_identity",
                return_value={"base_branch": "main"},
            ),
            mock.patch.object(gtt, "assert_workspace_boundary", return_value={"status": "ok"}),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_record_phase2_check(argparse.Namespace(
                root=str(self.root),
                task=self.task_ref,
                input="unused.json",
                dry_run=True,
            ))

        self.assertIn(
            "candidate-invalid-json:config/committed.json:2:1",
            raised.exception.payload["errors"],
        )
        self.assertIn(
            "config/committed.json",
            raised.exception.payload["candidate_paths"],
        )
        self.assertEqual(
            raised.exception.payload["base_ref"],
            gtt.diff_base_ref(self.root, "main"),
        )

    def test_phase2_recorder_accepts_committed_exact_template_whitespace_against_base(
        self,
    ) -> None:
        subprocess.run(
            ["git", "config", "user.name", "Phase 2 Test"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "phase2@example.invalid"],
            cwd=self.root,
            check=True,
        )
        task = gtt.read_json(self.task_dir / "task.json")
        task["status"] = "in_progress"
        gtt.write_json(self.task_dir / "task.json", task)
        template_relative = (
            ".claude/skills/trellis-meta/references/"
            "local-architecture/workspace-memory.md"
        )
        template_path = self.root / template_relative
        template_path.parent.mkdir(parents=True)
        template_path.write_bytes(b"# Workspace memory\n\nOld bytes.\n")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(phase2): #27 添加模板基线"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "checkout", "-q", "-b", "feat/gate-task"],
            cwd=self.root,
            check=True,
        )
        official_bytes = b"# Workspace memory\n\nOfficial hard break  \n\n"
        template_path.write_bytes(official_bytes)
        gtt.write_json(
            self.root / gtt.AI_FIRST_TEMPLATE_HASHES_PATH,
            {
                "__version": gtt.AI_FIRST_TEMPLATE_HASHES_SCHEMA_VERSION,
                "hashes": {
                    template_relative: hashlib.sha256(official_bytes).hexdigest(),
                },
            },
        )
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)

        _paths, staged_template_errors = gtt.ai_first_candidate_hygiene_scan(
            self.root,
            base_ref="main",
        )
        self.assertFalse(
            [error for error in staged_template_errors if template_relative in error]
        )

        subprocess.run(
            ["git", "commit", "-q", "-m", "test(phase2): #27 恢复官方模板字节"],
            cwd=self.root,
            check=True,
        )
        owner_input = self.root / ".trellis/.runtime/phase2-input.json"
        owner_input.parent.mkdir(parents=True)
        gtt.write_json(owner_input, self.phase2_authored())

        with (
            mock.patch.object(
                gtt,
                "load_task_runtime_identity",
                return_value={"base_branch": "main"},
            ),
            mock.patch.object(gtt, "assert_workspace_boundary", return_value={"status": "ok"}),
            mock.patch.object(
                gtt,
                "load_phase2_check_schema",
                return_value=self.phase2_schema,
            ),
        ):
            result = gtt.cmd_record_phase2_check(argparse.Namespace(
                root=str(self.root),
                task=self.task_ref,
                input=str(owner_input),
                dry_run=True,
            ))

        self.assertEqual(result["typed_exit"], "passed")
        self.assertEqual(
            result["phase2_capture_commit"], gtt.current_head(self.root)
        )

        template_path.write_bytes(official_bytes + b"local edit  \n")
        with (
            mock.patch.object(
                gtt,
                "load_task_runtime_identity",
                return_value={"base_branch": "main"},
            ),
            mock.patch.object(gtt, "assert_workspace_boundary", return_value={"status": "ok"}),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_record_phase2_check(argparse.Namespace(
                root=str(self.root),
                task=self.task_ref,
                input=str(owner_input),
                dry_run=True,
            ))

        self.assertIn(
            f"git-diff-check:{template_relative}:5: trailing whitespace.",
            raised.exception.payload["errors"],
        )

    def test_candidate_hygiene_binds_template_exemption_to_each_git_projection(
        self,
    ) -> None:
        subprocess.run(
            ["git", "config", "user.name", "Phase 2 Test"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "phase2@example.invalid"],
            cwd=self.root,
            check=True,
        )
        template_relative = (
            ".claude/skills/trellis-meta/references/"
            "local-architecture/workspace-memory.md"
        )
        template_path = self.root / template_relative
        template_path.parent.mkdir(parents=True)
        template_path.write_bytes(b"# Workspace memory\n\nOld bytes.\n")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(phase2): #27 添加模板基线"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "checkout", "-q", "-b", "feat/gate-task"],
            cwd=self.root,
            check=True,
        )
        official_bytes = b"# Workspace memory\n\nOfficial hard break  \n\n"
        template_path.write_bytes(official_bytes)
        gtt.write_json(
            self.root / gtt.AI_FIRST_TEMPLATE_HASHES_PATH,
            {
                "__version": gtt.AI_FIRST_TEMPLATE_HASHES_SCHEMA_VERSION,
                "hashes": {
                    template_relative: hashlib.sha256(official_bytes).hexdigest(),
                },
            },
        )
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(phase2): #27 恢复官方模板字节"],
            cwd=self.root,
            check=True,
        )

        local_bytes = official_bytes + b"staged local edit  \n"
        template_path.write_bytes(local_bytes)
        subprocess.run(["git", "add", template_relative], cwd=self.root, check=True)
        template_path.write_bytes(official_bytes)

        _paths, staged_errors = gtt.ai_first_candidate_hygiene_scan(
            self.root,
            base_ref="main",
        )
        self.assertIn(
            f"git-diff-check:{template_relative}:5: trailing whitespace.",
            staged_errors,
        )

        subprocess.run(
            ["git", "commit", "-q", "-m", "test(phase2): #27 提交本地模板改动"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(["git", "add", template_relative], cwd=self.root, check=True)

        _paths, committed_errors = gtt.ai_first_candidate_hygiene_scan(
            self.root,
            base_ref="main",
        )
        self.assertIn(
            f"git-diff-check:{template_relative}:5: trailing whitespace.",
            committed_errors,
        )

    def test_candidate_hygiene_exempts_only_exact_trellis_template_bytes(self) -> None:
        template_relative = (
            ".claude/skills/trellis-meta/references/"
            "local-architecture/workspace-memory.md"
        )
        template_path = self.root / template_relative
        template_path.parent.mkdir(parents=True)
        official_bytes = b"# Workspace memory\n\nOfficial hard break  \n\n"
        template_path.write_bytes(official_bytes)
        gtt.write_json(
            self.root / gtt.AI_FIRST_TEMPLATE_HASHES_PATH,
            {
                "__version": 2,
                "hashes": {
                    template_relative: hashlib.sha256(official_bytes).hexdigest(),
                },
            },
        )

        paths, errors = gtt.ai_first_candidate_hygiene_scan(
            self.root,
            candidate_paths=[template_relative],
        )
        self.assertIn(template_relative, paths)
        self.assertFalse([error for error in errors if template_relative in error])

        template_path.write_bytes(official_bytes + b"local edit\n")
        _paths, mismatch_errors = gtt.ai_first_candidate_hygiene_scan(
            self.root,
            candidate_paths=[template_relative],
        )
        self.assertIn(
            f"candidate-trailing-whitespace:{template_relative}:3",
            mismatch_errors,
        )

        unknown_relative = "notes/unknown.md"
        unknown_path = self.root / unknown_relative
        unknown_path.parent.mkdir(parents=True)
        unknown_path.write_bytes(b"# Unknown\n\nUnknown hard break  \n\n")
        _paths, unknown_errors = gtt.ai_first_candidate_hygiene_scan(
            self.root,
            candidate_paths=[unknown_relative],
        )
        self.assertIn(
            f"candidate-trailing-whitespace:{unknown_relative}:3",
            unknown_errors,
        )
        self.assertIn(
            f"candidate-blank-line-at-eof:{unknown_relative}",
            unknown_errors,
        )

    def test_candidate_hygiene_invalid_provenance_does_not_exempt_whitespace(self) -> None:
        relative = ".claude/skills/trellis-channel/references/command-reference.md"
        path = self.root / relative
        path.parent.mkdir(parents=True)
        content = b"# Command reference\n\n"
        path.write_bytes(content)
        valid_digest = hashlib.sha256(content).hexdigest()
        invalid_manifests = (
            {
                "__version": gtt.AI_FIRST_TEMPLATE_HASHES_SCHEMA_VERSION,
                "hashes": {relative: "not-a-sha256"},
            },
            {"__version": 1, "hashes": {relative: valid_digest}},
            {"__version": 3, "hashes": {relative: valid_digest}},
        )

        for manifest in invalid_manifests:
            with self.subTest(
                version=manifest["__version"],
                digest=manifest["hashes"][relative],
            ):
                gtt.write_json(
                    self.root / gtt.AI_FIRST_TEMPLATE_HASHES_PATH,
                    manifest,
                )
                _paths, errors = gtt.ai_first_candidate_hygiene_scan(
                    self.root,
                    candidate_paths=[relative],
                )
                self.assertIn(f"candidate-blank-line-at-eof:{relative}", errors)

    def test_candidate_hygiene_template_hash_does_not_bypass_content_safety(self) -> None:
        invalid_utf8_relative = ".claude/skills/trellis-meta/invalid.md"
        invalid_json_relative = ".claude/skills/trellis-meta/invalid.json"
        nonstandard_json_relative = ".claude/skills/trellis-meta/nonstandard.json"
        overflow_json_relative = ".claude/skills/trellis-meta/overflow.json"
        invalid_utf8 = b"\xff"
        invalid_json = b"{\n"
        nonstandard_json = b'{"value": NaN}\n'
        overflow_json = b'{"value": 1e9999}\n'
        for relative, content in (
            (invalid_utf8_relative, invalid_utf8),
            (invalid_json_relative, invalid_json),
            (nonstandard_json_relative, nonstandard_json),
            (overflow_json_relative, overflow_json),
        ):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        gtt.write_json(
            self.root / gtt.AI_FIRST_TEMPLATE_HASHES_PATH,
            {
                "__version": 2,
                "hashes": {
                    invalid_utf8_relative: hashlib.sha256(invalid_utf8).hexdigest(),
                    invalid_json_relative: hashlib.sha256(invalid_json).hexdigest(),
                    nonstandard_json_relative: hashlib.sha256(nonstandard_json).hexdigest(),
                    overflow_json_relative: hashlib.sha256(overflow_json).hexdigest(),
                },
            },
        )

        _paths, errors = gtt.ai_first_candidate_hygiene_scan(
            self.root,
            candidate_paths=[
                invalid_utf8_relative,
                invalid_json_relative,
                nonstandard_json_relative,
                overflow_json_relative,
            ],
        )
        self.assertIn(f"candidate-invalid-utf8:{invalid_utf8_relative}", errors)
        self.assertIn(f"candidate-invalid-json:{invalid_json_relative}:2:1", errors)
        self.assertIn(f"candidate-invalid-json:{nonstandard_json_relative}:1:1", errors)
        self.assertIn(f"candidate-invalid-json:{overflow_json_relative}:1:1", errors)

    def test_candidate_hygiene_validates_content_safety_per_git_projection(self) -> None:
        subprocess.run(
            ["git", "config", "user.name", "Phase 2 Test"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "phase2@example.invalid"],
            cwd=self.root,
            check=True,
        )
        invalid_utf8_relative = ".claude/skills/trellis-meta/invalid.md"
        invalid_json_relative = ".claude/skills/trellis-meta/invalid.json"
        invalid_nul_json_relative = ".claude/skills/trellis-meta/invalid-nul.json"
        nonstandard_json_relative = ".claude/skills/trellis-meta/nonstandard.json"
        overflow_json_relative = ".claude/skills/trellis-meta/overflow.json"
        candidate_contents = {
            invalid_utf8_relative: (b"# Baseline\n", b"\xff", b"# Fixed\n"),
            invalid_json_relative: (b"{}\n", b"{\n", b'{"fixed": true}\n'),
            invalid_nul_json_relative: (b"{}\n", b"{\x00}", b'{"fixed": true}\n'),
            nonstandard_json_relative: (
                b"{}\n",
                b'{"value": NaN}\n',
                b'{"fixed": true}\n',
            ),
            overflow_json_relative: (
                b"{}\n",
                b'{"value": 1e9999}\n',
                b'{"fixed": true}\n',
            ),
        }
        for relative, (baseline, _invalid, _fixed) in candidate_contents.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(baseline)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(phase2): #27 添加内容安全基线"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "checkout", "-q", "-b", "feat/gate-task"],
            cwd=self.root,
            check=True,
        )

        for relative, (_baseline, invalid, _fixed) in candidate_contents.items():
            (self.root / relative).write_bytes(invalid)
        gtt.write_json(
            self.root / gtt.AI_FIRST_TEMPLATE_HASHES_PATH,
            {
                "__version": gtt.AI_FIRST_TEMPLATE_HASHES_SCHEMA_VERSION,
                "hashes": {
                    relative: hashlib.sha256(invalid).hexdigest()
                    for relative, (_baseline, invalid, _fixed) in candidate_contents.items()
                },
            },
        )
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        for relative, (_baseline, _invalid, fixed) in candidate_contents.items():
            (self.root / relative).write_bytes(fixed)

        _paths, index_errors = gtt.ai_first_candidate_hygiene_scan(
            self.root,
            base_ref="main",
        )
        self.assertIn(f"candidate-invalid-utf8:{invalid_utf8_relative}", index_errors)
        self.assertIn(
            f"candidate-invalid-json:{invalid_json_relative}:2:1",
            index_errors,
        )
        self.assertIn(
            f"candidate-invalid-json:{invalid_nul_json_relative}:1:2",
            index_errors,
        )
        self.assertIn(
            f"candidate-invalid-json:{nonstandard_json_relative}:1:1",
            index_errors,
        )
        self.assertIn(
            f"candidate-invalid-json:{overflow_json_relative}:1:1",
            index_errors,
        )

        subprocess.run(
            ["git", "commit", "-q", "-m", "test(phase2): #27 提交无效模板投影"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "add", *candidate_contents],
            cwd=self.root,
            check=True,
        )
        _paths, head_errors = gtt.ai_first_candidate_hygiene_scan(
            self.root,
            base_ref="main",
        )
        self.assertIn(f"candidate-invalid-utf8:{invalid_utf8_relative}", head_errors)
        self.assertIn(
            f"candidate-invalid-json:{invalid_json_relative}:2:1",
            head_errors,
        )
        self.assertIn(
            f"candidate-invalid-json:{invalid_nul_json_relative}:1:2",
            head_errors,
        )
        self.assertIn(
            f"candidate-invalid-json:{nonstandard_json_relative}:1:1",
            head_errors,
        )
        self.assertIn(
            f"candidate-invalid-json:{overflow_json_relative}:1:1",
            head_errors,
        )

    def test_candidate_hygiene_validates_only_changed_git_projections(self) -> None:
        subprocess.run(
            ["git", "config", "user.name", "Phase 2 Test"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "phase2@example.invalid"],
            cwd=self.root,
            check=True,
        )
        relative = "data/preexisting-invalid.json"
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"{\n")
        subprocess.run(["git", "add", relative], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "test(phase2): #27 添加既有无效 JSON"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "checkout", "-q", "-b", "feat/gate-task"],
            cwd=self.root,
            check=True,
        )
        path.write_bytes(b'{"fixed": true}\n')

        paths, errors = gtt.ai_first_candidate_hygiene_scan(
            self.root,
            base_ref="main",
        )

        self.assertIn(relative, paths)
        self.assertFalse([error for error in errors if relative in error])

    def test_candidate_hygiene_template_hash_does_not_bypass_path_safety(self) -> None:
        outside_relative = f"../{self.root.name}-outside.md"
        outside_path = self.root.parent / f"{self.root.name}-outside.md"
        outside_content = b"# Outside\n\n"
        outside_path.write_bytes(outside_content)
        self.addCleanup(outside_path.unlink, missing_ok=True)
        gtt.write_json(
            self.root / gtt.AI_FIRST_TEMPLATE_HASHES_PATH,
            {
                "__version": 2,
                "hashes": {
                    outside_relative: hashlib.sha256(outside_content).hexdigest(),
                },
            },
        )

        _paths, errors = gtt.ai_first_candidate_hygiene_scan(
            self.root,
            candidate_paths=[outside_relative],
        )
        self.assertIn(
            f"candidate-path-outside-repository:{outside_relative}",
            errors,
        )

class PlanningApprovalDogfoodSyncTest(unittest.TestCase):
    REPO_ROOT = Path(__file__).resolve().parents[5]

    def load_dogfood_module(self) -> Any:
        path = self.REPO_ROOT / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
        self.assertTrue(path.exists(), f"Dogfood helper missing: {path}")
        spec = importlib.util.spec_from_file_location("dogfood_guru_team_trellis_for_test", path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_contract_wording_constants_match_dogfood_helper(self) -> None:
        dogfood = self.load_dogfood_module()
        for name in [
            "CONTRACT_WORDING_VOCABULARY_V2",
            "CONTRACT_WORDING_PLANNING_SCOPE",
            "CONTRACT_WORDING_CLASSIFICATIONS_V1",
            "CONTRACT_WORDING_BLOCKING_CLASSIFICATIONS",
        ]:
            with self.subTest(name=name):
                self.assertEqual(getattr(dogfood, name), getattr(gtt, name))


class PublishBoundaryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.task_dir = self.root / ".trellis/tasks/07-04-publish-boundary"
        self.task_dir.mkdir(parents=True)
        (self.root / ".trellis/guru-team").mkdir(parents=True)
        (self.root / ".trellis/scripts").mkdir(parents=True)
        (self.root / ".trellis/scripts/task.py").write_text("# test task script\n", encoding="utf-8")
        (self.root / ".trellis/scripts/add_session.py").write_text("# test journal script\n", encoding="utf-8")
        (self.root / ".git").mkdir()
        (self.task_dir / "task.json").write_text(
            '{"id":"publish-boundary","name":"publish-boundary","title":"Publish boundary","status":"in_progress","branch":"topic","base_branch":"main"}\n',
            encoding="utf-8",
        )
        issue = {
            "number": 18,
            "url": "https://github.com/owner/repo/issues/18",
            "title": "Publish boundary",
            "reason": "Primary delivered scope.",
        }
        gtt.write_json(self.task_dir / "issue-scope-ledger.json", {
            "schema_version": "2.0",
            "primary_issue": issue,
            "close_issues": [issue],
            "related_issues": [],
            "followup_issues": [],
        })

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def publication_ready_input(self, commit: str = "a" * 40) -> dict[str, str]:
        return {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": self.task_dir.relative_to(self.root).as_posix(),
            "branch_review_commit": commit,
            "pr_title": "#105 重构 finish-work 收尾事务",
            "pr_body": valid_pr_body("Publication ready DTO。"),
        }

    def test_publication_entry_consumes_passed_dto_without_review_gate(self) -> None:
        branch_review_commit = "a" * 40
        task_ref = self.task_dir.relative_to(self.root).as_posix()
        package = (
            self.root
            / "trellis/skills/guru-team/packages/guru-review-task-publication"
        )
        (package / "schemas").mkdir(parents=True)
        (package / "interface.json").write_text("{}\n", encoding="utf-8")
        (package / "schemas/public-input.schema.json").write_text(
            "{}\n",
            encoding="utf-8",
        )
        repository = {
            "head": branch_review_commit,
            "branch": "topic",
            "base_ref": "origin/main",
            "diff_paths": ["src/example.py"],
            "status_paths": [],
        }
        continuity = mock.Mock(return_value=[])
        private_gate = gtt.configured_review_gate_path(self.root, self.task_dir)
        self.assertFalse(private_gate.exists())

        with (
            mock.patch.object(gtt, "task_publication_schema", return_value={}),
            mock.patch.object(
                gtt,
                "load_task_runtime_identity",
                return_value={
                    "task_artifact_dir": task_ref,
                    "task_workspace_id": "publish-boundary",
                    "branch_name": "topic",
                    "base_branch": "main",
                },
            ),
            mock.patch.object(gtt, "assert_workspace_boundary"),
            mock.patch.object(gtt, "current_branch", return_value="topic"),
            mock.patch.object(gtt, "current_head", return_value=branch_review_commit),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={"sha256": "b" * 64},
            ) as identity,
            mock.patch.object(
                gtt,
                "review_branch_content_continuity_errors",
                continuity,
            ),
            mock.patch.object(
                gtt,
                "validate_review_gate",
                side_effect=AssertionError(
                    "Publication reopened Branch Review private evidence"
                ),
            ) as review_gate,
            mock.patch.object(
                gtt,
                "task_publication_repository_binding",
                return_value=repository,
            ),
            mock.patch.object(
                gtt,
                "task_publication_unexpected_status_paths",
                return_value=[],
            ),
            mock.patch.object(
                gtt,
                "load_issue_scope_ledger",
                return_value=gtt.read_json(self.task_dir / "issue-scope-ledger.json"),
            ),
            mock.patch.object(gtt, "validate_ledger_for_publish", return_value=[]),
            mock.patch.object(gtt, "validate_pr_body_quality", return_value=[]),
        ):
            bindings, errors, handoff, bound_repository = (
                gtt.task_publication_entry_precondition_bindings(
                    self.root,
                    self.task_dir,
                    {**gtt.DEFAULTS, "workspace_mode": "worktree"},
                    {
                        "profile": "publication_review",
                        "mode": "workflow",
                        "task_ref": task_ref,
                        "branch_review_commit": branch_review_commit,
                        "pr_payload": {
                            "title": "完成：验证 Publication entry",
                            "body": valid_pr_body("Publication entry 直接审查 exact payload。"),
                        },
                    },
                )
            )

        self.assertEqual(errors, [])
        self.assertEqual(bindings["branch_review_handoff"]["status"], "passed")
        self.assertEqual(
            handoff,
            {
                "typed_exit": "passed",
                "branch_review_commit": branch_review_commit,
            },
        )
        self.assertEqual(bound_repository, repository)
        identity.assert_called_once_with(
            self.root,
            branch_review_commit,
            include_worktree=False,
        )
        continuity.assert_called_once_with(
            self.root,
            self.task_dir,
            branch_review_commit,
            "b" * 64,
            branch_review_commit,
        )
        review_gate.assert_not_called()
        self.assertFalse(private_gate.exists())

    def test_closeout_anchor_uses_publication_dto_or_immutable_plan(self) -> None:
        task_ref = self.task_dir.relative_to(self.root).as_posix()
        initial_commit = "a" * 40
        publication_ready = {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": task_ref,
            "branch_review_commit": initial_commit,
            "pr_title": "#105 重构 finish-work 收尾事务",
            "pr_body": valid_pr_body("Publication ready DTO。"),
        }
        self.assertEqual(
            gtt.resolve_closeout_branch_review_commit(
                task_ref,
                publication_ready=publication_ready,
                existing_plan=None,
            ),
            initial_commit,
        )
        plan = {
            "task": {"active_locator": task_ref},
            "git": {"branch_review_commit": initial_commit},
        }
        self.assertEqual(
            gtt.resolve_closeout_branch_review_commit(
                task_ref,
                publication_ready=None,
                existing_plan=plan,
            ),
            initial_commit,
        )
        with self.assertRaises(gtt.WorkflowError):
            gtt.resolve_closeout_branch_review_commit(
                task_ref,
                publication_ready={
                    **publication_ready,
                    "branch_review_commit": "b" * 40,
                },
                existing_plan=plan,
            )
        evolved_commit = "b" * 40
        self.assertEqual(
            gtt.resolve_closeout_branch_review_commit(
                task_ref,
                publication_ready={
                    **publication_ready,
                    "branch_review_commit": evolved_commit,
                },
                existing_plan=plan,
                allow_base_evolution_supersession=True,
            ),
            evolved_commit,
        )
        with self.assertRaises(gtt.WorkflowError) as missing:
            gtt.resolve_closeout_branch_review_commit(
                task_ref,
                publication_ready=None,
                existing_plan=None,
            )
        self.assertIn("Publication ready DTO or immutable plan", str(missing.exception))

    def test_prepare_closeout_initial_entry_uses_publication_dto_without_review_gate(self) -> None:
        task_ref = self.task_dir.relative_to(self.root).as_posix()
        branch_review_commit = "a" * 40
        publication_ready = {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": task_ref,
            "branch_review_commit": branch_review_commit,
            "pr_title": "#105 重构 finish-work 收尾事务",
            "pr_body": valid_pr_body("Publication ready DTO。"),
        }
        task_context = {
            "task_artifact_dir": task_ref,
            "base_branch": "main",
        }
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": task_ref},
            "git": {"branch_review_commit": branch_review_commit},
            "marketplace": {"required": False},
        }
        args = argparse.Namespace(
            repo="owner/repo",
            remote="origin",
            base_branch="main",
            title="Publish boundary",
        )
        ledger = gtt.read_json(self.task_dir / "issue-scope-ledger.json")
        continuity = mock.Mock(return_value="b" * 64)
        with (
            mock.patch.object(gtt, "official_after_archive_hook_state"),
            mock.patch.object(
                gtt,
                "validate_review_gate",
                side_effect=AssertionError(
                    "Finalizer reopened Branch Review private evidence"
                ),
            ) as review_gate,
            mock.patch.object(gtt, "current_head", return_value=branch_review_commit),
            mock.patch.object(
                gtt,
                "validate_closeout_reviewed_content",
                continuity,
            ),
            mock.patch.object(
                gtt,
                "closeout_reviewed_change_facts",
                return_value={
                    "changed_paths": [],
                    "candidate_surfaces": [],
                    "marketplace_required": False,
                },
            ),
            mock.patch.object(gtt, "load_issue_scope_ledger", return_value=ledger),
            mock.patch.object(gtt, "finalizer_unreviewed_dirty_paths", return_value=[]),
            mock.patch.object(gtt, "validate_ledger_for_publish", return_value=[]),
            mock.patch.object(gtt, "validate_pr_body_quality", return_value=[]),
            mock.patch.object(gtt, "validate_closeout_task_children"),
            mock.patch.object(
                gtt,
                "normalize_github_repository",
                return_value="owner/repo",
            ),
            mock.patch.object(gtt, "base_branch_from_sources", return_value="main"),
            mock.patch.object(gtt, "current_branch", return_value="topic"),
            mock.patch.object(gtt, "validate_github_remote_repository"),
            mock.patch.object(gtt, "pr_title_from_task", return_value="Publish boundary"),
            mock.patch.object(gtt, "build_closeout_plan", return_value=plan),
        ):
            prepared = gtt.prepare_closeout(
                self.root,
                args,
                {**gtt.DEFAULTS, "github_repo": "owner/repo"},
                self.task_dir,
                task_context,
                publication_ready=publication_ready,
            )

        self.assertEqual(prepared["plan"], plan)
        self.assertNotIn("gate", prepared)
        self.assertNotIn("gate_path", prepared)
        self.assertEqual(prepared["body"], publication_ready["pr_body"])
        continuity.assert_called_once_with(
            self.root,
            {"git": {"branch_review_commit": branch_review_commit}},
            branch_review_commit,
            include_worktree=True,
        )
        review_gate.assert_not_called()

    def test_pr_body_quality_rejects_incomplete_docs_ssot_keys(self) -> None:
        body = valid_pr_body("验证 Docs SSOT section 固定键 presence。").replace(
            "- follow-up / limitation：无 follow-up 或当前 PR limitation。\n",
            "",
        )
        errors = gtt.validate_pr_body_quality(body, {"close_issues": [{"number": 18}]}, draft=False)

        self.assertTrue(any("followup_or_limitation" in error for error in errors))

    def test_pr_body_quality_accepts_reviewer_readable_chinese_docs_sync(self) -> None:
        body = valid_pr_body("验证合理中文文档同步正文不会被 key presence 误伤。").replace(
            """## Docs SSOT

- 策略：ssot_first。
- durable docs：已更新 `trellis/workflows/guru-team/workflow.md`。
- task delta merge：任务 artifact delta 已 merge 到 durable docs。
- task history：调试过程仅保留为 task history。
- follow-up / limitation：无 follow-up 或当前 PR limitation。
""",
            """## 文档同步

- 本次采用 ssot_first。
- 长期文档已更新 workflow、spec 与 README。
- 任务文档差异已同步回长期文档。
- 调试记录仅保留在任务历史中。
- 无后续事项或当前 PR 限制。
""",
        )
        errors = gtt.validate_pr_body_quality(body, {"close_issues": [{"number": 18}]}, draft=False)

        self.assertEqual([], errors)

    def test_finish_work_direct_call_requires_guru_finalizer(self) -> None:
        with (
            mock.patch.object(gtt, "repo_root") as repo_root,
            mock.patch.object(gtt, "run") as run,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_finish_work(finish_args(from_guru_finalizer=False))

        repo_root.assert_not_called()
        run_commands = [call.args[0] for call in run.call_args_list]
        self.assertNotIn(["python3", "./.trellis/scripts/task.py", "archive", self.task_dir.name], run_commands)
        self.assertFalse(any(command[:3] == ["python3", "./.trellis/scripts/add_session.py", "--title"] for command in run_commands))
        self.assertEqual(raised.exception.exit_code, 2)
        self.assertEqual(raised.exception.payload["blocked_step"], "finish-work")
        self.assertEqual(raised.exception.payload["required_entrypoint"], "guru-finish-work")
        self.assertNotIn("intent_flag", raised.exception.payload)
        self.assertIn("guru-finalize-task", str(raised.exception))

    def test_finish_work_rejects_missing_publication_payload_before_archive(self) -> None:
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_runtime_identity", return_value={
                "base_branch": "main",
                "workspace_mode": "worktree",
                "workspace_path": str(self.root),
                "task_dir": ".trellis/tasks/07-04-publish-boundary",
                "preflight": {"current_checkout": str(self.root)},
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "assert_workspace_boundary"),
            mock.patch.object(gtt, "current_head", return_value="a" * 40),
            mock.patch.object(
                gtt,
                "validate_closeout_reviewed_content",
                return_value="b" * 64,
            ),
            mock.patch.object(
                gtt,
                "closeout_reviewed_change_facts",
                return_value={
                    "changed_paths": ["trellis/workflows/guru-team/workflow.md"],
                    "marketplace_required": False,
                },
            ),
            mock.patch.object(gtt, "finalizer_unreviewed_dirty_paths", return_value=[]),
            mock.patch.object(gtt, "run") as run,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_finish_work(finish_args(
                validation=["python3 -m unittest 通过"],
            ))

        run_commands = [call.args[0] for call in run.call_args_list]
        self.assertNotIn(["python3", "./.trellis/scripts/task.py", "archive", self.task_dir.name], run_commands)
        self.assertFalse(any(command[:3] == ["python3", "./.trellis/scripts/add_session.py", "--title"] for command in run_commands))
        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("Publication ready DTO or immutable plan", str(raised.exception))

    def test_finish_work_dry_run_returns_plan_without_archive_journal_commit_or_publish(self) -> None:
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_runtime_identity", return_value={
                "base_branch": "main",
                "task_artifact_dir": ".trellis/tasks/07-04-publish-boundary",
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "current_head", return_value="a" * 40),
            mock.patch.object(
                gtt,
                "validate_closeout_reviewed_content",
                return_value="b" * 64,
            ),
            mock.patch.object(
                gtt,
                "closeout_reviewed_change_facts",
                return_value={
                    "changed_paths": ["trellis/workflows/guru-team/workflow.md"],
                    "marketplace_required": False,
                },
            ),
            mock.patch.object(gtt, "finalizer_unreviewed_dirty_paths", return_value=[]),
            mock.patch.object(gtt, "current_branch", return_value="codex/27-finish-work-dry-run-readiness"),
            mock.patch.object(gtt, "validate_github_remote_repository", return_value="owner/repo"),
            mock.patch.object(
                gtt,
                "closeout_live_move_classes",
                side_effect=lambda _root, _active, move_paths: ([], move_paths),
            ),
            mock.patch.object(
                gtt,
                "build_closeout_reviewed_tracked_bindings",
                return_value=[],
            ),
            mock.patch.object(
                gtt,
                "run_stdout",
                side_effect=lambda command, **_kwargs: (
                    "2026-07-11T00:00:00+00:00"
                    if command[:3] == ["git", "show", "-s"]
                    else ""
                ),
            ),
            mock.patch.object(gtt, "run") as run,
        ):
            run.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            payload = gtt.cmd_finish_work(finish_args(
                publication_ready=self.publication_ready_input(),
            ))

        run_commands = [call.args[0] for call in run.call_args_list]
        self.assertNotIn(["python3", "./.trellis/scripts/task.py", "archive", self.task_dir.name], run_commands)
        self.assertFalse(any(command[:3] == ["python3", "./.trellis/scripts/add_session.py", "--title"] for command in run_commands))
        self.assertEqual(payload["status"], "dry-run")
        self.assertFalse(payload["dry_run_side_effects"])
        plan = payload["closeout_plan"]
        self.assertEqual(payload["closeout_plan_digest"], plan["plan_digest"])
        self.assertEqual(plan["task"]["id"], "publish-boundary")
        self.assertEqual(plan["git"]["repo"], "owner/repo")
        self.assertEqual(plan["git"]["base_branch"], "main")
        self.assertEqual(plan["git"]["head_branch"], "codex/27-finish-work-dry-run-readiness")
        self.assertTrue(plan["publish"]["draft"])
        self.assertEqual(plan["transitions"], gtt.CLOSEOUT_TRANSITIONS)
        self.assertEqual(gtt.closeout_plan_errors(plan), [])

    def test_finish_work_uses_publication_dto_without_review_gate(self) -> None:
        archived_task_dir = self.root / ".trellis/tasks/archive/2026-07/07-04-publish-boundary"
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_runtime_identity", return_value={
                "base_branch": "main",
                "task_artifact_dir": ".trellis/tasks/07-04-publish-boundary",
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "current_head", return_value="a" * 40),
            mock.patch.object(
                gtt,
                "validate_review_gate",
                side_effect=AssertionError(
                    "Finalizer reopened Branch Review private evidence"
                ),
            ) as validate_gate,
            mock.patch.object(
                gtt,
                "validate_closeout_reviewed_content",
                return_value="b" * 64,
            ),
            mock.patch.object(
                gtt,
                "closeout_reviewed_change_facts",
                return_value={
                    "changed_paths": ["trellis/workflows/guru-team/workflow.md"],
                    "marketplace_required": False,
                },
            ),
            mock.patch.object(gtt, "finalizer_unreviewed_dirty_paths", return_value=[]),
            mock.patch.object(gtt, "current_branch", return_value="codex/27-finish-work-dry-run-readiness"),
            mock.patch.object(gtt, "validate_github_remote_repository", return_value="owner/repo"),
            mock.patch.object(
                gtt,
                "closeout_live_move_classes",
                side_effect=lambda _root, _active, move_paths: ([], move_paths),
            ),
            mock.patch.object(
                gtt,
                "build_closeout_reviewed_tracked_bindings",
                return_value=[],
            ),
            mock.patch.object(
                gtt,
                "run_stdout",
                side_effect=lambda command, **_kwargs: (
                    "2026-07-11T00:00:00+00:00"
                    if command[:3] == ["git", "show", "-s"]
                    else ""
                ),
            ),
            mock.patch.object(gtt, "run") as run,
            mock.patch.object(gtt, "resolve_existing_task_dir", return_value=archived_task_dir),
            mock.patch.object(gtt, "validate_finish_summary"),
        ):
            run.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            gtt.cmd_finish_work(finish_args(
                dry_run=True,
                publication_ready=self.publication_ready_input(),
            ))

        validate_gate.assert_not_called()

    def test_publish_identity_validation_rejects_repo_branch_or_base_mismatch_before_remote_query(self) -> None:
        task = {"base_branch": "main"}
        base_context = {
            "source_repo": {"repo": "owner/repo"},
            "branch_name": "codex/18-publish-boundary",
            "base_branch": "main",
        }
        cases = [
            ("other/repo", "main", "codex/18-publish-boundary", base_context),
            ("owner/repo", "main", "other-branch", base_context),
            ("owner/repo", "release", "codex/18-publish-boundary", base_context),
        ]
        for repo, base, branch, context in cases:
            with self.subTest(repo=repo, base=base, branch=branch), mock.patch.object(
                gtt, "run"
            ) as run, self.assertRaises(gtt.WorkflowError):
                gtt.validate_publish_identity_and_remote_head(
                    self.root, task, context, repo, base, branch, "origin"
                )
            run.assert_not_called()

    def test_publish_identity_validation_requires_remote_head_to_equal_current_head(self) -> None:
        context = {
            "source_repo": {"repo": "owner/repo"},
            "branch_name": "codex/18-publish-boundary",
            "base_branch": "main",
        }
        with (
            mock.patch.object(gtt, "current_head", return_value="a" * 40),
            mock.patch.object(
                gtt,
                "run",
                return_value=mock.Mock(
                    returncode=0,
                    stdout=f"{'b' * 40}\trefs/heads/codex/18-publish-boundary\n",
                    stderr="",
                ),
            ),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.validate_publish_identity_and_remote_head(
                self.root,
                {"base_branch": "main"},
                context,
                "owner/repo",
                "main",
                "codex/18-publish-boundary",
                "origin",
            )
        self.assertEqual(raised.exception.payload["head"], "a" * 40)
        self.assertEqual(raised.exception.payload["remote_head"], "b" * 40)



class ReviewGateReportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.task_dir = self.root / ".trellis/tasks/07-04-review-gate"
        self.task_dir.mkdir(parents=True)
        (self.root / ".trellis/guru-team").mkdir(parents=True)
        (self.root / ".git").mkdir()
        (self.task_dir / "task.json").write_text(
            '{"title":"Review gate","base_branch":"main"}\n',
            encoding="utf-8",
        )
        (self.task_dir / "issue-scope-ledger.json").write_text(
            '{"schema_version":"2.0",'
            '"primary_issue":{"number":20,"url":"https://github.com/owner/repo/issues/20",'
            '"title":"Review gate","reason":"This task closes issue 20."},'
            '"close_issues":[{"number":20,"url":"https://github.com/owner/repo/issues/20",'
            '"title":"Review gate","reason":"This task closes issue 20."}],'
            '"related_issues":[],"followup_issues":[]}\n',
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def package_schema(self, name: str) -> dict[str, object]:
        package = (
            Path(gtt.__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages/guru-review-branch/schemas"
        )
        return gtt.read_json(package / name)

    def patch_review_command(self, head: str) -> list[mock._patch]:
        return [
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(
                gtt,
                "load_config",
                return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"},
            ),
            mock.patch.object(
                gtt,
                "load_task_runtime_identity",
                return_value={
                    "base_branch": "main",
                    "workspace_mode": "worktree",
                    "workspace_path": str(self.root),
                    "task_dir": ".trellis/tasks/07-04-review-gate",
                    "preflight": {"current_checkout": str(self.root)},
                },
            ),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "review_branch_entry_precondition_errors", return_value=[]),
            mock.patch.object(gtt, "current_branch", return_value="codex/20-review-gate"),
            mock.patch.object(gtt, "current_head", return_value=head),
            mock.patch.object(gtt, "diff_base_ref", return_value="origin/main"),
            mock.patch.object(
                gtt,
                "changed_files",
                return_value=["trellis/workflows/guru-team/workflow.md"],
            ),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(gtt, "git_status_paths", return_value=[]),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={
                    "algorithm": gtt.REVIEWED_CONTENT_ALGORITHM,
                    "sha256": "f" * 64,
                },
            ),
            mock.patch.object(
                gtt,
                "review_branch_public_input_schema",
                return_value=self.package_schema("public-branch-review-input.schema.json"),
            ),
            mock.patch.object(
                gtt,
                "review_branch_gate_schema",
                return_value=self.package_schema("review-gate.schema.json"),
            ),
        ]

    def write_inputs(
        self,
        *,
        head: str,
        review_intent: str,
        typed_exit: str,
        candidates: list[dict[str, object]],
    ) -> tuple[Path, Path]:
        public_input = self.root / "review-public-input.json"
        semantic_input = self.root / "review-semantic-input.json"
        gtt.write_json(
            public_input,
            {
                "profile": "branch_review",
                "mode": "workflow",
                "task_ref": ".trellis/tasks/07-04-review-gate",
                "base_ref": "origin/main",
                "branch_review_commit": head,
                "review_intent": review_intent,
            },
        )
        gtt.write_json(
            semantic_input,
            {
                "candidates": candidates,
                "ai_review_gate": {
                    "status": typed_exit,
                    "summary": "已完成当前完整 diff 的独立语义审查。",
                },
            },
        )
        return public_input, semantic_input

    def record(
        self,
        *,
        head: str,
        review_intent: str,
        typed_exit: str,
        candidates: list[dict[str, object]],
        reviewer: str = "independent-review-agent",
    ) -> dict[str, object]:
        public_input, semantic_input = self.write_inputs(
            head=head,
            review_intent=review_intent,
            typed_exit=typed_exit,
            candidates=candidates,
        )
        patchers = self.patch_review_command(head)
        for patcher in patchers:
            patcher.start()
        try:
            return gtt.cmd_review_branch(
                review_args(
                    reviewer=reviewer,
                    skill_input=str(public_input),
                    semantic_review_file=str(semantic_input),
                    typed_exit=typed_exit,
                )
            )
        finally:
            for patcher in reversed(patchers):
                patcher.stop()

    def resolved_finding(
        self,
        introduced_head: str,
        fix_head: str,
        closure_head: str,
    ) -> dict[str, object]:
        return {
            "candidate_ref": "candidate-001",
            "disposition": "qualified_finding",
            "scenario_class": "normal_required_behavior",
            "affected_behavior": "已批准行为需要修复。",
            "path": "trellis/workflows/guru-team/workflow.md",
            "evidence_refs": ["review-gate.json:F-001"],
            "requirement_refs": ["Issue #119 regression"],
            "scope_basis": "当前批准范围。",
            "qualification_reason": "正常路径违反当前 requirement。",
            "finding_ref": "F-001",
            "severity": "P2",
            "introduced_head": introduced_head,
            "fix_head": fix_head,
            "closure_head": closure_head,
            "status": "resolved",
            "closure_evidence": [
                f"commit:{closure_head}",
                "test:branch-review-regression",
            ],
        }

    def open_finding(self, introduced_head: str) -> dict[str, object]:
        finding = self.resolved_finding(
            introduced_head,
            "b" * 40,
            "c" * 40,
        )
        finding.update({
            "status": "open",
            "fix_head": None,
            "closure_head": None,
            "closure_evidence": [],
        })
        return finding

    def test_review_branch_records_only_current_private_gate(self) -> None:
        head = "a" * 40
        payload = self.record(
            head=head,
            review_intent="initial_review",
            typed_exit="passed",
            candidates=[],
        )

        self.assertEqual(payload["schema_version"], "3.0")
        self.assertEqual(payload["typed_exit"], "passed")
        gate_path = Path(str(payload["artifact_path"]))
        self.assertEqual(
            set(gtt.read_json(gate_path)),
            {
                "schema_version", "skill_id", "generated_at", "task_dir",
                "mode", "review_intent", "typed_exit", "review_commit",
                "reviewed_content_sha256", "base_ref",
                "semantic_review", "verification_evidence", "facts_sha256",
            },
        )
        self.assertTrue(
            gate_path.as_posix().startswith(
                (self.root / ".trellis/.runtime/guru-team/owner-checkpoints").as_posix()
            )
        )
        self.assertTrue(payload["tracked_status_unchanged"])
        self.assertFalse((self.task_dir / "review-gate.json").exists())
        self.assertFalse((self.task_dir / "review.md").exists())
        self.assertFalse((self.task_dir / "agent-assignment.json").exists())
        self.assertFalse((self.task_dir / "reviews").exists())

    def test_review_branch_accepts_closure_then_distinct_fresh_final_sequence(self) -> None:
        introduced_head = "a" * 40
        fix_head = "b" * 40
        closure_head = "c" * 40
        review_commit = "d" * 40

        initial = self.record(
            head=introduced_head,
            review_intent="initial_review",
            typed_exit="implementation_required",
            candidates=[self.open_finding(introduced_head)],
            reviewer="finding-owner",
        )
        self.assertEqual(initial["typed_exit"], "implementation_required")

        ephemeral_closure = {
            "reviewer": "finding-owner",
            "introduced_head": introduced_head,
            "fix_head": fix_head,
            "closure_head": closure_head,
            "evidence": [f"commit:{closure_head}", "test:branch-review-regression"],
        }
        fresh_final_reviewer = "fresh-final-agent"
        self.assertNotEqual(ephemeral_closure["reviewer"], fresh_final_reviewer)

        payload = self.record(
            head=review_commit,
            review_intent="fresh_final_review",
            typed_exit="passed",
            candidates=[
                self.resolved_finding(
                    introduced_head,
                    fix_head,
                    closure_head,
                )
            ],
            reviewer=fresh_final_reviewer,
        )

        recorded = gtt.read_json(Path(str(payload["artifact_path"])))
        self.assertEqual(payload["typed_exit"], "passed")
        finding = recorded["semantic_review"]["qualified_findings"][0]
        self.assertEqual(finding["introduced_head"], introduced_head)
        self.assertEqual(finding["fix_head"], fix_head)
        self.assertEqual(finding["closure_head"], closure_head)
        self.assertEqual(recorded["review_commit"], review_commit)
        self.assertEqual(recorded["reviewed_content_sha256"], "f" * 64)
        self.assertEqual(
            len({introduced_head, fix_head, closure_head, review_commit}),
            4,
        )
        self.assertEqual(
            set(recorded["verification_evidence"]),
            {"reviewer", "review_source", "evidence"},
        )
        self.assertEqual(recorded["verification_evidence"]["reviewer"], fresh_final_reviewer)
        self.assertFalse((self.task_dir / "reviews").exists())
        self.assertFalse((self.task_dir / "review.md").exists())
        self.assertFalse((self.task_dir / "agent-assignment.json").exists())

    def test_review_branch_records_open_finding_without_raw_round(self) -> None:
        head = "c" * 40
        payload = self.record(
            head=head,
            review_intent="initial_review",
            typed_exit="implementation_required",
            candidates=[self.open_finding(head)],
        )

        self.assertEqual(payload["typed_exit"], "implementation_required")
        self.assertEqual(
            payload["semantic_review"]["qualified_findings"][0]["finding_ref"],
            "F-001",
        )
        self.assertFalse((self.task_dir / "reviews").exists())

    def test_review_branch_rejects_main_session_reviewer(self) -> None:
        with self.assertRaises(gtt.WorkflowError) as raised:
            self.record(
                head="d" * 40,
                review_intent="initial_review",
                typed_exit="passed",
                candidates=[],
                reviewer="codex-main-session",
            )

        self.assertIn("independent Agent", str(raised.exception))

    def test_review_branch_consumes_committed_dto_without_rereading_phase2_checkpoint(self) -> None:
        head = "e" * 40
        public_input, semantic_input = self.write_inputs(
            head=head,
            review_intent="initial_review",
            typed_exit="passed",
            candidates=[],
        )
        patchers = self.patch_review_command(head)
        for patcher in patchers:
            patcher.start()
        try:
            with mock.patch.object(
                gtt,
                "validate_phase2_check",
                side_effect=AssertionError("Branch Review must not reread Phase 2 private state."),
            ) as phase2_check:
                payload = gtt.cmd_review_branch(
                    review_args(
                        skill_input=str(public_input),
                        semantic_review_file=str(semantic_input),
                    )
                )
                phase2_check.assert_not_called()
        finally:
            for patcher in reversed(patchers):
                patcher.stop()

        self.assertEqual(payload["typed_exit"], "passed")
        self.assertEqual(payload["review_commit"], head)
        self.assertEqual(payload["reviewed_content_sha256"], "f" * 64)

    def test_review_branch_cli_exposes_only_structured_recorder(self) -> None:
        review = next(
            action
            for action in gtt.build_parser()._actions
            if isinstance(action, argparse._SubParsersAction)
        ).choices["review-branch"]
        options = {
            option
            for action in review._actions
            for option in action.option_strings
        }

        for required in {
            "--skill-input", "--semantic-review-file", "--typed-exit",
            "--reviewer", "--review-source", "--evidence",
        }:
            self.assertIn(required, options)
        for removed in {
            "--pass", "--summary", "--review-report", "--agent-assignment",
            "--finding", "--findings-file", "--observation",
            "--observations-file", "--followup-candidate",
            "--followup-candidates-file",
        }:
            self.assertNotIn(removed, options)

class ReviewBranchAncestryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.task_dir = self.root / ".trellis/tasks/08-01-review-ancestry"
        self.task_dir.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "review@example.com"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Review Test"],
            cwd=self.root,
            check=True,
        )
        self.introduced_head = self.commit(
            "src/feature.txt",
            "behavior needing review\n",
            "introduce reviewed behavior",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def commit(self, relative: str, content: str, message: str) -> str:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "add", "--", relative], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=self.root, check=True)
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()

    @staticmethod
    def resolved_finding(
        introduced_head: str,
        fix_head: str,
        closure_head: str,
    ) -> dict[str, object]:
        return {
            "finding_ref": "F-ANCESTRY",
            "introduced_head": introduced_head,
            "fix_head": fix_head,
            "closure_head": closure_head,
            "status": "resolved",
            "closure_evidence": ["test:real-git-ancestry"],
        }

    def test_resolved_historical_heads_pass_real_ancestry_chain(self) -> None:
        fix_head = self.commit(
            "src/feature.txt",
            "fixed behavior\n",
            "fix reviewed behavior",
        )
        closure_head = self.commit(
            "tests/feature.txt",
            "closure evidence\n",
            "close reviewed finding",
        )
        review_commit = self.commit(
            "tests/fresh-final.txt",
            "fresh final coverage\n",
            "complete fresh final coverage",
        )
        semantic = {
            "qualified_findings": [
                self.resolved_finding(
                    self.introduced_head,
                    fix_head,
                    closure_head,
                )
            ]
        }

        self.assertEqual(
            gtt.review_branch_finding_lifecycle_errors(
                self.root,
                self.task_dir,
                semantic,
                review_commit=review_commit,
            ),
            [],
        )
        self.assertEqual(
            len(
                {
                    self.introduced_head,
                    fix_head,
                    closure_head,
                    review_commit,
                }
            ),
            4,
        )

    def test_fix_that_is_not_reviewed_history_fails_closed(self) -> None:
        subprocess.run(
            ["git", "switch", "-q", "-c", "alternate-fix", self.introduced_head],
            cwd=self.root,
            check=True,
        )
        unrelated_fix = self.commit(
            "src/feature.txt",
            "alternate fix\n",
            "create alternate fix",
        )
        subprocess.run(["git", "switch", "-q", "main"], cwd=self.root, check=True)
        review_commit = self.commit(
            "tests/closure.txt",
            "main history closure\n",
            "record main history closure",
        )
        semantic = {
            "qualified_findings": [
                self.resolved_finding(
                    self.introduced_head,
                    unrelated_fix,
                    review_commit,
                )
            ]
        }

        errors = gtt.review_branch_finding_lifecycle_errors(
            self.root,
            self.task_dir,
            semantic,
            review_commit=review_commit,
        )

        self.assertTrue(any("introduced -> fix -> closure" in item for item in errors))

    def test_explicit_task_metadata_descendant_preserves_content_identity(self) -> None:
        reviewed_content_sha256 = gtt.reviewed_content_identity(
            self.root,
            self.introduced_head,
            include_worktree=False,
        )["sha256"]
        current = self.commit(
            ".trellis/tasks/08-01-review-ancestry/context-discovery.json",
            "publication metadata\n",
            "record publication metadata",
        )

        self.assertEqual(
            gtt.review_branch_content_continuity_errors(
                self.root,
                self.task_dir,
                self.introduced_head,
                reviewed_content_sha256,
                current,
            ),
            [],
        )

    def test_finalizer_dirty_gate_excludes_all_private_metadata(self) -> None:
        status_paths = [
            ".trellis/tasks/08-01-review-ancestry/context-discovery.json",
            ".trellis/tasks/08-01-review-ancestry/design.md",
            ".trellis/tasks/other/review.md",
            ".trellis/.runtime/guru-team/debug.json",
            ".trellis/workspace/dev/journal.md",
            ".trellis/workflow.md",
            "src/feature.txt",
        ]

        with mock.patch.object(
            gtt,
            "git_status_paths",
            return_value=status_paths,
        ) as git_status:
            dirty_paths = gtt.finalizer_unreviewed_dirty_paths(
                self.root,
                self.task_dir,
            )

        git_status.assert_called_once_with(self.root, fail_closed=True)

        self.assertEqual(
            dirty_paths,
            [
                ".trellis/workflow.md",
                "src/feature.txt",
            ],
        )

    def test_finalizer_dirty_gate_propagates_git_status_failure(self) -> None:
        with (
            mock.patch.object(
                gtt,
                "git_status_paths",
                side_effect=gtt.WorkflowError(
                    "Could not inspect Git status paths.",
                    exit_code=2,
                ),
            ) as git_status,
            self.assertRaises(gtt.WorkflowError) as failed,
        ):
            gtt.finalizer_unreviewed_dirty_paths(self.root, self.task_dir)

        self.assertEqual(failed.exception.exit_code, 2)
        git_status.assert_called_once_with(self.root, fail_closed=True)

    def test_task_metadata_descendant_stays_fresh_but_code_descendant_is_stale(self) -> None:
        reviewed_content_sha256 = gtt.reviewed_content_identity(
            self.root,
            self.introduced_head,
            include_worktree=False,
        )["sha256"]
        metadata_head = self.commit(
            ".trellis/tasks/08-01-review-ancestry/design.md",
            "changed durable design\n",
            "change durable design",
        )
        self.assertEqual(
            gtt.review_branch_content_continuity_errors(
                self.root,
                self.task_dir,
                self.introduced_head,
                reviewed_content_sha256,
                metadata_head,
            ),
            [],
        )

        code_head = self.commit(
            "src/feature.txt",
            "changed after review\n",
            "change reviewed code",
        )
        code_errors = gtt.review_branch_content_continuity_errors(
            self.root,
            self.task_dir,
            self.introduced_head,
            reviewed_content_sha256,
            code_head,
        )
        self.assertEqual(
            code_errors,
            [gtt.BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX + "identity mismatch"],
        )

    def test_runtime_descendant_is_excluded_from_reviewed_content(self) -> None:
        reviewed_content_sha256 = gtt.reviewed_content_identity(
            self.root,
            self.introduced_head,
            include_worktree=False,
        )["sha256"]
        current = self.commit(
            ".trellis/.runtime/guru-team/debug.json",
            "{}\n",
            "record unknown runtime state",
        )

        errors = gtt.review_branch_content_continuity_errors(
            self.root,
            self.task_dir,
            self.introduced_head,
            reviewed_content_sha256,
            current,
        )

        self.assertEqual(errors, [])



class AgentRecoveryCheckpointTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.task_dir = self.root / ".trellis/tasks/07-05-agent-recovery"
        self.task_dir.mkdir(parents=True)
        (self.root / ".trellis/guru-team").mkdir(parents=True)
        (self.root / ".git").mkdir()
        (self.task_dir / "task.json").write_text(
            '{"title":"Agent recovery","base_branch":"main"}\n',
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def patch_recovery_command(self) -> list[mock._patch]:
        return [
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value=gtt.DEFAULTS),
            mock.patch.object(
                gtt,
                "load_task_runtime_identity",
                return_value={
                    "workspace_mode": "worktree",
                    "workspace_path": str(self.root),
                    "task_dir": ".trellis/tasks/07-05-agent-recovery",
                    "preflight": {"current_checkout": str(self.root)},
                },
            ),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "current_head", return_value="a" * 40),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
        ]

    def test_checkpoint_records_only_real_unfinished_replacement(self) -> None:
        patchers = self.patch_recovery_command()
        for patcher in patchers:
            patcher.start()
        try:
            unfinished = gtt.cmd_record_agent_recovery(recovery_args())
            replacement = gtt.cmd_record_agent_recovery(
                recovery_args(
                    event="replacement",
                    agent_id="agent-replacement",
                    reason="The replacement accepted the unfinished scope.",
                    predecessor_event_id="recovery-001",
                )
            )
            checked = gtt.cmd_check_agent_recovery(recovery_args())
        finally:
            for patcher in reversed(patchers):
                patcher.stop()

        self.assertTrue(unfinished["checkpoint"].startswith(gtt.AGENT_RECOVERY_RUNTIME_DIR))
        self.assertEqual(replacement["event"]["predecessor_event_id"], "recovery-001")
        self.assertEqual(checked["replacement_count"], 1)
        self.assertEqual(checked["open_unfinished"], {})
        self.assertFalse((self.task_dir / "agent-assignment.json").exists())

    def test_checkpoint_rejects_replacement_without_unfinished(self) -> None:
        patchers = self.patch_recovery_command()
        for patcher in patchers:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_record_agent_recovery(
                    recovery_args(
                        event="replacement",
                        agent_id="agent-replacement",
                        predecessor_event_id="recovery-001",
                    )
                )
        finally:
            for patcher in reversed(patchers):
                patcher.stop()

        self.assertIn("must close the open unfinished role", str(raised.exception.payload["errors"]))

    def test_routine_path_creates_no_recovery_checkpoint(self) -> None:
        path = gtt.agent_recovery_path(self.root, self.task_dir)
        self.assertFalse(path.exists())
        self.assertTrue(path.as_posix().startswith((self.root / gtt.AGENT_RECOVERY_RUNTIME_DIR).as_posix()))


class FinishWorkEntrypointContractTest(unittest.TestCase):
    REPO_ROOT = Path(__file__).resolve().parents[5]
    ENTRYPOINT_FILES = [
        "trellis/presets/guru-team/overlays/.codex/prompts/guru-finish-work.md",
        "trellis/presets/guru-team/overlays/.claude/commands/guru/finish-work.md",
        "trellis/presets/guru-team/overlays/.cursor/commands/guru-finish-work.md",
        ".codex/prompts/guru-finish-work.md",
        ".claude/commands/guru/finish-work.md",
        ".cursor/commands/guru-finish-work.md",
    ]
    PUBLIC_DOC_FILES = [
        "README.md",
        "trellis/workflows/guru-team/README.md",
        "trellis/presets/guru-team/README.md",
        "docs/requirements/requirement-main.md",
    ]
    CLOSEOUT_DOC_CONTRACTS = {
        ".trellis/spec/workflow/workflow-contract.md": {
            "required": [
                "`guru-finalize-task` owns the single resumable transaction loop",
                "canonical thin `guru-finish-work` router.",
                "accepts exactly one reviewed payload source: Publication `ready` schema 4.0",
                "`task_ref/branch_review_commit/pr_title/pr_body`",
                "no body file, summary-index file, alternate locator, or generated source participates in closeout.",
            ],
            "forbidden": [
                "It calls `finish-work.sh` with the required",
                "script-generated `generated` bodies are preview/draft-only",
                "resolve it relative to the artifact's own directory.",
            ],
        },
        ".trellis/spec/workflow/companion-scripts.md": {
            "required": [
                "canonical user route is `guru-finish-work`.",
                "Every interruption returns through the same finalizer semantic loop",
                "Formal closeout accepts only the exact `pr_title` and `pr_body` projected by the current Publication `ready` output",
                "No file locator, generated source, or payload override participates.",
            ],
            "forbidden": [
                "Every interruption is resumed through that same state-aware entry.",
                "`generated` bodies are limited to draft/preview paths.",
            ],
        },
    }
    BARE_FINISH_COMMAND = ".trellis/guru-team/scripts/bash/finish-work.sh --json"

    def test_finish_work_entrypoints_are_thin_semantic_routers(self) -> None:
        for relpath in self.ENTRYPOINT_FILES:
            with self.subTest(path=relpath):
                content = (self.REPO_ROOT / relpath).read_text(encoding="utf-8")
                for required in (
                    "read `.trellis/workflow.md`",
                    "Phase 3.6/3.7",
                    "guru-review-task-publication",
                    "guru-verify-extension-installation",
                    "guru-finalize-task",
                    "Consume only their current public typed exits",
                    "Mapped",
                ):
                    self.assertIn(required, content, f"{relpath} must route through {required!r}")
                for forbidden in (
                    "finish-work.sh",
                    "--body-file",
                    "--finish-summary-index-file",
                    "--dry-run",
                    "--expected-plan-digest",
                    "resolve-human-artifacts.sh",
                    "Markdown 产物 review 表",
                ):
                    self.assertNotIn(
                        forbidden,
                        content,
                        f"{relpath} must leave {forbidden!r} to its semantic owner",
                    )

    def test_public_docs_do_not_show_bare_finish_work_command(self) -> None:
        for relpath in self.PUBLIC_DOC_FILES:
            with self.subTest(path=relpath):
                content = (self.REPO_ROOT / relpath).read_text(encoding="utf-8")
                bare_lines = [
                    line_number
                    for line_number, line in enumerate(content.splitlines(), start=1)
                    if line.strip() == self.BARE_FINISH_COMMAND
                ]

                self.assertEqual(
                    bare_lines,
                    [],
                    f"{relpath} must not show bare finish-work command lines",
                )

    def test_closeout_docs_match_canonical_contract(self) -> None:
        for relpath, contract in self.CLOSEOUT_DOC_CONTRACTS.items():
            with self.subTest(path=relpath):
                content = "".join((self.REPO_ROOT / relpath).read_text(encoding="utf-8").split())
                for required in contract["required"]:
                    self.assertIn("".join(required.split()), content)
                for forbidden in contract["forbidden"]:
                    self.assertNotIn("".join(forbidden.split()), content)


class ThinWorkflowPublicGraphContractTest(unittest.TestCase):
    REPO_ROOT = Path(__file__).resolve().parents[5]
    CANONICAL_WORKFLOW = Path("trellis/workflows/guru-team/workflow.md")
    DOGFOOD_WORKFLOW = Path(".trellis/workflow.md")
    SKILL_ROOT = Path("trellis/skills/guru-team")
    MARKERS = {
        "invoke": re.compile(r"^<!-- guru-skill-invoke: (\{.*\}) -->$"),
        "exit": re.compile(r"^<!-- guru-skill-exit: (\{.*\}) -->$"),
        "workflow": re.compile(r"^<!-- guru-workflow-target: (\{.*\}) -->$"),
        "stop": re.compile(r"^<!-- guru-stop-target: (\{.*\}) -->$"),
    }

    def marker_payloads(self, text: str, kind: str) -> list[dict[str, object]]:
        pattern = self.MARKERS[kind]
        return [
            json.loads(match.group(1))
            for line in text.splitlines()
            if (match := pattern.fullmatch(line)) is not None
        ]

    def expected_public_graph(
        self,
    ) -> tuple[set[str], dict[tuple[str, str], dict[str, str]], set[str], set[str]]:
        skill_root = self.REPO_ROOT / self.SKILL_ROOT
        registry = json.loads((skill_root / "registry.json").read_text(encoding="utf-8"))
        active_rows = [row for row in registry["skills"] if row["state"] == "active"]
        active_ids = {row["id"] for row in active_rows}
        exits: dict[tuple[str, str], dict[str, str]] = {}
        workflow_targets: set[str] = set()
        stop_targets: set[str] = set()
        for row in active_rows:
            interface = json.loads(
                (skill_root / row["interface"]).read_text(encoding="utf-8")
            )
            for external_exit in interface["external_exits"]:
                key = (row["id"], external_exit["id"])
                self.assertNotIn(key, exits)
                consumer = external_exit["consumer"]
                exits[key] = consumer
                if consumer["kind"] == "workflow":
                    workflow_targets.add(consumer["id"])
                elif consumer["kind"] == "stop":
                    stop_targets.add(consumer["id"])
        return active_ids, exits, workflow_targets, stop_targets

    def test_canonical_and_dogfood_workflows_are_byte_identical(self) -> None:
        canonical = (self.REPO_ROOT / self.CANONICAL_WORKFLOW).read_bytes()
        dogfood = (self.REPO_ROOT / self.DOGFOOD_WORKFLOW).read_bytes()
        self.assertEqual(canonical, dogfood)

    def test_phase_context_entrypoints_remain_parseable(self) -> None:
        script = self.REPO_ROOT / ".trellis/scripts/get_context.py"
        cases = [
            (["--mode", "phase"], "## Phase Index"),
            (["--mode", "phase", "--step", "0.4"], "guru-review-change-request"),
            (["--mode", "phase", "--step", "1.1"], "Planning artifacts"),
            (["--mode", "phase", "--step", "2.2"], "guru-check-task"),
            (["--mode", "phase", "--step", "3.5"], "guru-review-branch"),
        ]
        for arguments, expected in cases:
            with self.subTest(arguments=arguments):
                completed = subprocess.run(
                    [sys.executable, str(script), *arguments],
                    cwd=self.REPO_ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertIn(expected, completed.stdout)

    def test_thin_workflow_matches_the_complete_interface_graph(self) -> None:
        text = (self.REPO_ROOT / self.CANONICAL_WORKFLOW).read_text(encoding="utf-8")
        active_ids, expected_exits, expected_workflow_targets, expected_stop_targets = (
            self.expected_public_graph()
        )

        invokes = self.marker_payloads(text, "invoke")
        exits = self.marker_payloads(text, "exit")
        workflow_targets = self.marker_payloads(text, "workflow")
        stop_targets = self.marker_payloads(text, "stop")

        self.assertEqual(len(active_ids), 14)
        self.assertEqual(len(expected_exits), 54)
        self.assertEqual(len(expected_workflow_targets) + len(expected_stop_targets), 31)
        self.assertEqual(len(invokes), 14)
        self.assertEqual(len(exits), 54)
        self.assertEqual(len(workflow_targets) + len(stop_targets), 31)

        invoke_ids = [payload["skill"] for payload in invokes]
        self.assertEqual(set(invoke_ids), active_ids)
        self.assertEqual(len(invoke_ids), len(set(invoke_ids)))
        self.assertTrue(
            all(
                payload == {"skill": payload["skill"], "required": True}
                for payload in invokes
            )
        )

        actual_exits: dict[tuple[str, str], dict[str, str]] = {}
        for payload in exits:
            key = (payload["skill"], payload["exit"])
            self.assertNotIn(key, actual_exits)
            actual_exits[key] = payload["consumer"]
        self.assertEqual(actual_exits, expected_exits)

        actual_workflow_targets = [payload["id"] for payload in workflow_targets]
        actual_stop_targets = [payload["id"] for payload in stop_targets]
        self.assertEqual(set(actual_workflow_targets), expected_workflow_targets)
        self.assertEqual(set(actual_stop_targets), expected_stop_targets)
        self.assertEqual(len(actual_workflow_targets), len(set(actual_workflow_targets)))
        self.assertEqual(len(actual_stop_targets), len(set(actual_stop_targets)))

    def test_workflow_contains_only_global_graph_and_boundaries(self) -> None:
        text = (self.REPO_ROOT / self.CANONICAL_WORKFLOW).read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 420)
        for forbidden in (
            "entry_preconditions",
            "planning_checked_dimensions",
            "scope-before-severity",
            "ten-dimension",
            "eight-dimension",
            "record-planning-approval",
            "check-planning-approval",
            "record-phase2-check",
            "check-phase2-check",
            "planning-approval.json",
            "phase2-check.json",
            "review-gate.json",
            "pr-readiness.json",
            "agent-assignment.json",
            ".trellis/.runtime",
            "guru_team_trellis.py",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)


class HumanArtifactResolutionContractTest(unittest.TestCase):
    REPO_ROOT = Path(__file__).resolve().parents[5]
    CONTINUE_ENTRYPOINT_FILES = [
        "trellis/workflows/guru-team/workflow.md",
        ".trellis/workflow.md",
    ]
    FINISH_WORKFLOW_FILES = [
        "trellis/workflows/guru-team/workflow.md",
        ".trellis/workflow.md",
    ]
    FINISH_ENTRYPOINT_FILES = [
        "trellis/presets/guru-team/overlays/.codex/prompts/guru-finish-work.md",
        "trellis/presets/guru-team/overlays/.claude/commands/guru/finish-work.md",
        "trellis/presets/guru-team/overlays/.cursor/commands/guru-finish-work.md",
        ".codex/prompts/guru-finish-work.md",
        ".claude/commands/guru/finish-work.md",
        ".cursor/commands/guru-finish-work.md",
    ]

    def assert_file_contains(self, relpath: str, snippets: list[str]) -> None:
        content = (self.REPO_ROOT / relpath).read_text(encoding="utf-8")
        for snippet in snippets:
            self.assertIn(snippet, content, f"{relpath} must mention {snippet!r}")

    def test_continue_entrypoints_delegate_minimal_human_artifact_resolution(self) -> None:
        for relpath in self.CONTINUE_ENTRYPOINT_FILES:
            with self.subTest(path=relpath):
                self.assert_file_contains(relpath, ["resolve-human-artifacts.sh"])
                content = (self.REPO_ROOT / relpath).read_text(encoding="utf-8")
                if "trellis-continue" in relpath or relpath.endswith("/continue.md"):
                    self.assertIn("human-authored artifacts", content)
                    self.assertNotIn("Markdown 产物 review 表", content)

    def test_finish_workflow_resolves_active_then_archive_paths(self) -> None:
        snippets = [
            "resolve-human-artifacts.sh",
            "active",
            "archive",
            "`prd.md`",
            "`design.md`",
            "`implement.md`",
            "Show links only for existing",
        ]
        for relpath in self.FINISH_WORKFLOW_FILES:
            with self.subTest(path=relpath):
                self.assert_file_contains(relpath, snippets)

    def test_finish_entrypoints_delegate_human_artifacts_to_semantic_owner(self) -> None:
        for relpath in self.FINISH_ENTRYPOINT_FILES:
            with self.subTest(path=relpath):
                content = (self.REPO_ROOT / relpath).read_text(encoding="utf-8")
                self.assertIn("guru-finalize-task", content)
                self.assertNotIn("resolve-human-artifacts.sh", content)
                self.assertNotIn("Markdown 产物 review 表", content)

    def test_user_facing_docs_do_not_expose_retired_pr_body_handoff(self) -> None:
        forbidden = "pr-body.md"
        for relpath in [
            "trellis/workflows/guru-team/workflow.md",
            ".trellis/workflow.md",
            "README.md",
            "trellis/workflows/guru-team/README.md",
            "trellis/presets/guru-team/README.md",
        ]:
            with self.subTest(path=relpath):
                content = (self.REPO_ROOT / relpath).read_text(encoding="utf-8")
                self.assertNotIn(forbidden, content)


class IntakeScopeEvolutionContractTest(unittest.TestCase):
    REPO_ROOT = Path(__file__).resolve().parents[5]
    WORKFLOW_FILES = [
        "trellis/workflows/guru-team/workflow.md",
        ".trellis/workflow.md",
    ]
    PUBLIC_DOC_FILES = [
        "docs/requirements/requirement-main.md",
        "docs/requirements/guru-team-trellis-flow.md",
    ]

    def assert_file_contains(self, relpath: str, snippets: list[str]) -> None:
        content = (self.REPO_ROOT / relpath).read_text(encoding="utf-8")
        for snippet in snippets:
            self.assertIn(snippet, content, f"{relpath} must mention {snippet!r}")

    def test_workflow_requires_thin_skill_owned_intake_and_scope_change_gates(self) -> None:
        for relpath in self.WORKFLOW_FILES:
            with self.subTest(path=relpath):
                self.assert_file_contains(
                    relpath,
                    [
                        "guru-sync-base",
                        "guru-discover-change-context",
                        "guru-clarify-requirements",
                        "guru-review-contract-wording",
                        "guru-review-change-request",
                        "guru-create-task-workspace",
                        "Scope Change Gate",
                        "issue-scope-ledger.json",
                    ],
                )
                content = (self.REPO_ROOT / relpath).read_text(encoding="utf-8")
                guru_team_gate = content.split("## Guru Team Gate", 1)[1].split("\n## ", 1)[0]
                self.assertNotIn("intake clarity check", guru_team_gate)
                self.assertNotIn("trellis-brainstorm", guru_team_gate)

    def test_preset_does_not_ship_upstream_start_or_continue_entries(self) -> None:
        overlay_root = self.REPO_ROOT / "trellis/presets/guru-team/overlays"
        forbidden = [
            ".agents/skills/trellis-start/SKILL.md",
            ".agents/skills/trellis-continue/SKILL.md",
            ".codex/prompts/trellis-start.md",
            ".codex/prompts/trellis-continue.md",
            ".codex/skills/trellis-start/SKILL.md",
            ".codex/skills/trellis-continue/SKILL.md",
            ".claude/commands/trellis/continue.md",
            ".cursor/commands/trellis-continue.md",
        ]
        for relpath in forbidden:
            with self.subTest(path=relpath):
                self.assertFalse((overlay_root / relpath).exists())

    def test_public_docs_point_to_canonical_scope_and_interaction_contracts(self) -> None:
        for relpath in self.PUBLIC_DOC_FILES:
            with self.subTest(path=relpath):
                self.assert_file_contains(
                    relpath,
                    [
                        "Intake clarity",
                        "workflow",
                        "确认继续",
                    ],
                )


class ProvenanceMetadataTailRuntimeTest(unittest.TestCase):
    REPO_ROOT = Path(__file__).resolve().parents[5]

    def git(self, root: Path, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=root, text=True).strip()

    def test_checked_in_manifest_has_no_pending_installer_sidecars(self) -> None:
        manifest = json.loads(
            (self.REPO_ROOT / gtt.PROVENANCE_TAIL_MANIFEST_PATH).read_text(
                encoding="utf-8"
            )
        )
        install = manifest["install"]
        self.assertEqual(install["managed_backups"], [])
        self.assertEqual(install["new_copies"], [])

        pending = [
            relpath
            for key in ("managed_backups", "new_copies")
            for relpath in install[key]
            if (self.REPO_ROOT / relpath).exists()
        ]
        self.assertEqual(pending, [])

    def fixture(self) -> tuple[Path, str, str]:
        root = Path(tempfile.mkdtemp(prefix="guru-provenance-tail-test-"))
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        manifest = root / gtt.PROVENANCE_TAIL_MANIFEST_PATH
        manifest.parent.mkdir(parents=True)
        manifest.write_text(
            json.dumps(
                {
                    "installed_at": "old",
                    "source": {
                        "ref": "old",
                        "commit": "0" * 40,
                        "tree_state": "dirty",
                        "is_mutable_ref": True,
                    },
                }
            ),
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "reviewed"], cwd=root, check=True)
        reviewed = self.git(root, "rev-parse", "HEAD")
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        payload["installed_at"] = "new"
        payload["source"] = {
            "ref": reviewed,
            "commit": reviewed,
            "tree_state": "clean",
            "is_mutable_ref": False,
        }
        manifest.write_text(json.dumps(payload), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "provenance tail"], cwd=root, check=True)
        publication = self.git(root, "rev-parse", "HEAD")
        return root, reviewed, publication

    def test_clean_tail_preserves_reviewed_identity_and_validates_publication_head(self) -> None:
        root, reviewed, publication = self.fixture()
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        subprocess.run(["git", "checkout", "--detach", "-q", publication], cwd=root, check=True)
        self.assertTrue(gtt.reviewed_content_metadata_path(gtt.PROVENANCE_TAIL_MANIFEST_PATH))
        result = gtt.validate_provenance_metadata_tail(root, reviewed, publication)
        self.assertEqual(result["reviewed_content_head"], reviewed)
        self.assertEqual(result["publication_head"], publication)

    def test_tail_rejects_non_allowlisted_manifest_field(self) -> None:
        root, reviewed, publication = self.fixture()
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        manifest = root / gtt.PROVENANCE_TAIL_MANIFEST_PATH
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        payload["extension"] = {"version": "drift"}
        manifest.write_text(json.dumps(payload), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "invalid tail"], cwd=root, check=True)
        invalid = self.git(root, "rev-parse", "HEAD")
        with self.assertRaisesRegex(gtt.WorkflowError, "failed its clean-source contract"):
            gtt.validate_provenance_metadata_tail(root, reviewed, invalid)

    def test_manifest_diff_rejects_added_and_removed_non_allowlisted_null_fields(self) -> None:
        valid = {
            "installed_at": "new",
            "source": {
                "ref": "a" * 40,
                "commit": "a" * 40,
                "tree_state": "clean",
                "is_mutable_ref": False,
            },
        }
        with_null = {**copy.deepcopy(valid), "unexpected": None}
        for before, after in ((valid, with_null), (with_null, valid)):
            with self.subTest(before_has_null="unexpected" in before):
                self.assertEqual(
                    gtt.provenance_tail_manifest_field_diff(before, after),
                    ["unexpected"],
                )
                self.assertIn(
                    "provenance_tail_manifest_fields_outside_allowlist",
                    gtt.provenance_tail_manifest_errors(before, after, "a" * 40),
                )

    def test_manifest_diff_ignores_unchanged_present_null_field(self) -> None:
        payload = {"unexpected": None}
        self.assertEqual(
            gtt.provenance_tail_manifest_field_diff(payload, copy.deepcopy(payload)),
            [],
        )

    def test_manifest_diff_tracks_added_and_removed_nested_empty_objects(self) -> None:
        valid = {
            "installed_at": "new",
            "source": {
                "ref": "a" * 40,
                "commit": "a" * 40,
                "tree_state": "clean",
                "is_mutable_ref": False,
            },
            "unexpected": {},
        }
        with_nested_empty = copy.deepcopy(valid)
        with_nested_empty["unexpected"]["nested"] = {}
        for before, after in (
            (valid, with_nested_empty),
            (with_nested_empty, valid),
        ):
            with self.subTest(before_has_nested="nested" in before["unexpected"]):
                self.assertEqual(
                    gtt.provenance_tail_manifest_field_diff(before, after),
                    ["unexpected.nested"],
                )
                self.assertIn(
                    "provenance_tail_manifest_fields_outside_allowlist",
                    gtt.provenance_tail_manifest_errors(before, after, "a" * 40),
                )

    def test_manifest_diff_ignores_unchanged_empty_object_during_allowlisted_change(self) -> None:
        before = {
            "installed_at": "old",
            "source": {
                "ref": "a" * 40,
                "commit": "a" * 40,
                "tree_state": "clean",
                "is_mutable_ref": False,
            },
            "stable_empty": {},
        }
        after = copy.deepcopy(before)
        after["installed_at"] = "new"
        self.assertEqual(
            gtt.provenance_tail_manifest_field_diff(before, after),
            ["installed_at"],
        )
        self.assertEqual(
            gtt.provenance_tail_manifest_errors(before, after, "a" * 40),
            [],
        )

    def test_publication_identity_accepts_one_tail_without_reclassifying_reviewed_head(self) -> None:
        root, reviewed, publication = self.fixture()
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        identity = gtt.finalizer_publication_identity(root, reviewed)
        self.assertEqual(identity["reviewed_content_head"], reviewed)
        self.assertEqual(identity["publication_head"], publication)
        self.assertEqual(identity["metadata_tail"]["parent"], reviewed)

    def test_publication_identity_rejects_manifest_drift_mixed_with_task_metadata(self) -> None:
        root, reviewed, _ = self.fixture()
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        subprocess.run(
            ["git", "checkout", "--detach", "-q", reviewed], cwd=root, check=True
        )
        manifest = root / gtt.PROVENANCE_TAIL_MANIFEST_PATH
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        payload["unexpected"] = "drift"
        manifest.write_text(json.dumps(payload), encoding="utf-8")
        task_metadata = root / ".trellis/tasks/current/runtime-note.json"
        task_metadata.parent.mkdir(parents=True)
        task_metadata.write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "mixed metadata"], cwd=root, check=True)

        with self.assertRaisesRegex(
            gtt.WorkflowError, "invalid provenance tail"
        ) as blocked:
            gtt.finalizer_publication_identity(root, reviewed)
        self.assertIn(
            "provenance_tail_changed_paths_invalid",
            blocked.exception.payload["errors"],
        )

    def test_provenance_reprepare_error_classification_is_narrow(self) -> None:
        self.assertTrue(gtt.finalizer_provenance_reprepare_error(gtt.WorkflowError(
            "dirty source",
            payload={"reason_code": "extension_source_not_clean"},
        )))
        self.assertTrue(gtt.finalizer_provenance_reprepare_error(gtt.WorkflowError(
            "stale manifest",
            payload={"errors": [
                "installed extension manifest provenance is stale.",
            ]},
        )))
        self.assertFalse(gtt.finalizer_provenance_reprepare_error(gtt.WorkflowError(
            "mixed drift",
            payload={"errors": [
                "installed extension manifest provenance is stale.",
                "target remote ref HEAD no longer matches private evidence.",
            ]},
        )))

    def test_reprepare_route_uses_a_marker_only_when_the_tail_changes_head(self) -> None:
        task_ref = ".trellis/tasks/current"
        public_input = {"task_ref": task_ref}
        context = {
            "transaction_state": "reprepare_required",
            "reprepare_reason_code": gtt.FINALIZATION_REPREPARE_PROVENANCE_TAIL,
            "publication_status": "current",
            "publication_stale_reason": None,
            "plan_ref": f"closeout-plan:{'a' * 64}",
            "plan": {
                "git": {
                    "branch_review_commit": "b" * 40,
                    "publication_head": "c" * 40,
                },
                "task": {"active_locator": task_ref},
            },
        }
        route = {
            "typed_exit": "reprepare_required",
            "consumer": gtt.FINALIZATION_CONSUMERS["reprepare_required"],
            "output": copy.deepcopy(gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER),
        }
        gtt.finalization_validate_route(
            Path.cwd(),
            public_input,
            context,
            route,
            allow_pending_transition=True,
        )
        with self.assertRaisesRegex(gtt.WorkflowError, "checked transition"):
            gtt.finalization_validate_route(
                Path.cwd(),
                public_input,
                context,
                route,
            )
        non_materialized = copy.deepcopy(route)
        non_materialized["output"] = {
            "exit_id": "reprepare_required",
            "task_ref": task_ref,
            "reason_code": gtt.FINALIZATION_REPREPARE_PROVENANCE_TAIL,
            "branch_review_commit": "b" * 40,
            "publication_head": "c" * 40,
        }
        with self.assertRaisesRegex(gtt.WorkflowError, "executor marker"):
            gtt.finalization_validate_route(
                Path.cwd(),
                public_input,
                context,
                non_materialized,
                allow_pending_transition=True,
            )
        context["reprepare_reason_code"] = gtt.FINALIZATION_REPREPARE_ARCHIVE_MONTH
        with self.assertRaisesRegex(gtt.WorkflowError, "complete current public output"):
            gtt.finalization_validate_route(
                Path.cwd(),
                public_input,
                context,
                route,
                allow_pending_transition=True,
            )
        archive_output = copy.deepcopy(non_materialized)
        archive_output["output"]["reason_code"] = gtt.FINALIZATION_REPREPARE_ARCHIVE_MONTH
        with mock.patch.object(
            gtt,
            "finalization_output_contract",
            return_value={"type": "object"},
        ):
            gtt.finalization_validate_route(
                Path.cwd(),
                public_input,
                context,
                archive_output,
                allow_pending_transition=True,
            )
        context["reprepare_reason_code"] = None
        with self.assertRaisesRegex(gtt.WorkflowError, "reason does not match"):
            gtt.finalization_validate_route(
                Path.cwd(),
                public_input,
                context,
                route,
                allow_pending_transition=True,
            )

    def test_reprepare_executor_keeps_archive_month_and_provenance_actions_separate(self) -> None:
        root, reviewed, _ = self.fixture()
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        task_dir = root / ".trellis/tasks/current"
        task_dir.mkdir(parents=True)
        public_input = {"task_ref": ".trellis/tasks/current"}
        gate = {
            "route": {
                "typed_exit": "reprepare_required",
                "output": {
                    "exit_id": "reprepare_required",
                    "task_ref": public_input["task_ref"],
                    "reason_code": gtt.FINALIZATION_REPREPARE_ARCHIVE_MONTH,
                    "branch_review_commit": reviewed,
                    "publication_head": "d" * 40,
                },
            },
        }
        context = {
            "task_dir": task_dir,
            "plan": {"git": {"reviewed_content_head": reviewed}},
            "reprepare_reason_code": gtt.FINALIZATION_REPREPARE_ARCHIVE_MONTH,
        }
        args = argparse.Namespace(root=str(root), input="unused", gate=None)
        publication = {
            "reviewed_content_head": reviewed,
            "publication_head": "d" * 40,
            "metadata_tail": None,
        }
        with (
            mock.patch.object(gtt, "finalization_public_input", return_value=(public_input, "unused")),
            mock.patch.object(gtt, "finalization_gate_input", return_value=(gate, root / "gate.json")),
            mock.patch.object(gtt, "check_finalization_gate_result", return_value=(gate, context)),
            mock.patch.object(gtt, "finalizer_publication_identity", return_value=publication),
            mock.patch.object(gtt, "prepare_provenance_metadata_tail") as prepare_tail,
            mock.patch.object(gtt, "finalizer_pre_pr_provenance_reprepare_preflight"),
            mock.patch.object(gtt, "finalizer_supersede_pre_pr_state", return_value=["old-plan"]) as retire,
            mock.patch.object(gtt, "finalization_output_contract", return_value={"type": "object"}),
        ):
            result = gtt.cmd_execute_finalization_transition(args)
        prepare_tail.assert_not_called()
        retire.assert_called_once_with(root.resolve(), task_dir)
        self.assertEqual(result["publication_head"], publication["publication_head"])
        self.assertEqual(result["output"]["branch_review_commit"], reviewed)
        self.assertEqual(result["output"]["publication_head"], publication["publication_head"])

        context["reprepare_reason_code"] = gtt.FINALIZATION_REPREPARE_PROVENANCE_TAIL
        gate["route"]["output"] = copy.deepcopy(gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER)
        prepared = {**publication, "publication_head": "e" * 40}
        with (
            mock.patch.object(gtt, "finalization_public_input", return_value=(public_input, "unused")),
            mock.patch.object(gtt, "finalization_gate_input", return_value=(gate, root / "gate.json")),
            mock.patch.object(gtt, "check_finalization_gate_result", return_value=(gate, context)),
            mock.patch.object(gtt, "finalizer_publication_identity", return_value=publication),
            mock.patch.object(gtt, "prepare_provenance_metadata_tail", return_value=prepared) as prepare_tail,
            mock.patch.object(gtt, "finalizer_pre_pr_provenance_reprepare_preflight"),
            mock.patch.object(gtt, "finalizer_supersede_pre_pr_state", return_value=["old-plan"]),
            mock.patch.object(gtt, "finalization_output_contract", return_value={"type": "object"}),
        ):
            result = gtt.cmd_execute_finalization_transition(args)
        prepare_tail.assert_called_once_with(root.resolve(), reviewed)
        self.assertEqual(result["publication_head"], prepared["publication_head"])
        self.assertEqual(result["output"]["reason_code"], gtt.FINALIZATION_REPREPARE_PROVENANCE_TAIL)

    def test_base_evolution_executor_persists_replacement_plan_after_retirement(self) -> None:
        root, reviewed, publication = self.fixture()
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        task_dir = root / ".trellis/tasks/current"
        task_dir.mkdir(parents=True)
        task_ref = ".trellis/tasks/current"
        previous_plan = {"plan_digest": "a" * 64}
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "base_branch": "main",
                "head_branch": "topic",
                "branch_review_commit": reviewed,
                "reviewed_content_head": reviewed,
                "publication_head": reviewed,
            },
            "publish": {
                "title": "完成：恢复 Finalizer",
                "body": valid_pr_body("恢复 Finalizer。"),
            },
        }
        replacement_plan = {
            "schema_version": gtt.CLOSEOUT_PLAN_SCHEMA_VERSION,
            "plan_digest": "b" * 64,
        }
        public_input = {"task_ref": task_ref, "mode": "workflow"}
        gate = {
            "route": {
                "typed_exit": "reprepare_required",
                "output": copy.deepcopy(gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER),
            },
        }
        context = {
            "task_dir": task_dir,
            "task_context": {"task_artifact_dir": task_ref},
            "plan": plan,
            "prepared": {
                "pre_pr_reprepare": {
                    "previous_plan": previous_plan,
                    "base_evolution": {"reviewed_content_head": reviewed},
                },
            },
            "reprepare_reason_code": gtt.FINALIZATION_REPREPARE_PROVENANCE_TAIL,
        }
        args = argparse.Namespace(root=str(root), input="unused", gate=None)
        with (
            mock.patch.object(gtt, "finalization_public_input", return_value=(public_input, "unused")),
            mock.patch.object(gtt, "finalization_gate_input", return_value=(gate, root / "gate.json")),
            mock.patch.object(gtt, "check_finalization_gate_result", return_value=(gate, context)),
            mock.patch.object(gtt, "finalizer_pre_pr_provenance_reprepare_preflight") as preflight,
            mock.patch.object(gtt, "finalizer_publication_identity", return_value={
                "reviewed_content_head": reviewed,
                "publication_head": publication,
                "metadata_tail": {"parent": reviewed, "commit": publication},
            }),
            mock.patch.object(gtt, "finalizer_supersede_pre_pr_state", return_value=["old-state"]) as retire,
            mock.patch.object(gtt, "prepare_closeout", return_value={"plan": replacement_plan}) as prepare,
            mock.patch.object(gtt, "validate_closeout_plan", side_effect=lambda value: value),
            mock.patch.object(gtt, "finalization_output_contract", return_value={"type": "object"}),
        ):
            result = gtt.cmd_execute_finalization_transition(args)

        preflight.assert_called_once_with(
            root.resolve(),
            task_dir,
            plan,
            previous_plan=previous_plan,
            allowed_current_gate=gate,
        )
        retire.assert_called_once_with(root.resolve(), task_dir)
        prepare.assert_called_once()
        self.assertEqual(
            gtt.read_json(task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT),
            replacement_plan,
        )
        self.assertEqual(result["replacement_plan_digest"], replacement_plan["plan_digest"])

    def test_reprepare_supersession_preserves_tracked_task_artifacts(self) -> None:
        root, _, _ = self.fixture()
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        task_dir = root / ".trellis/tasks/current"
        task_dir.mkdir(parents=True)
        plan = task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT
        verification = task_dir / gtt.MARKETPLACE_VERIFICATION_ARTIFACT
        plan.write_text("{}\n", encoding="utf-8")
        verification.write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "add", ".trellis/tasks/current"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "tracked task artifacts"], cwd=root, check=True)

        with self.assertRaisesRegex(gtt.WorkflowError, "will not delete tracked") as blocked:
            gtt.finalizer_supersede_pre_pr_state(root, task_dir)
        self.assertEqual(
            blocked.exception.payload["tracked_paths"],
            [
                ".trellis/tasks/current/closeout-plan.json",
                ".trellis/tasks/current/marketplace-verification.json",
            ],
        )
        self.assertTrue(plan.is_file())
        self.assertTrue(verification.is_file())

    def test_reprepare_preconditions_block_before_producer_head_or_artifact_mutation(self) -> None:
        cases = {
            "tracked": None,
            "pull_request": "provenance_reprepare_pull_request_exists",
            "remote_changed": "provenance_reprepare_remote_not_reviewed_head",
            "parallel_consumer": "provenance_reprepare_parallel_publication_consumer",
        }
        for case, expected_reason in cases.items():
            with self.subTest(case=case):
                root, reviewed, _ = self.fixture()
                self.addCleanup(lambda path=root: shutil.rmtree(path, ignore_errors=True))
                subprocess.run(["git", "checkout", "-B", "topic", reviewed], cwd=root, check=True)
                task_dir = root / ".trellis/tasks/current"
                task_dir.mkdir(parents=True)
                plan_path = task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT
                verification_path = task_dir / gtt.MARKETPLACE_VERIFICATION_ARTIFACT
                plan_path.write_text("{}\n", encoding="utf-8")
                verification_path.write_text("{}\n", encoding="utf-8")
                if case == "tracked":
                    subprocess.run(["git", "add", ".trellis/tasks/current"], cwd=root, check=True)
                    subprocess.run(["git", "commit", "-qm", "tracked owner state"], cwd=root, check=True)
                    reviewed = self.git(root, "rev-parse", "HEAD")

                plan = {
                    "git": {
                        "repo": "castbox/guru-trellis",
                        "remote": "origin",
                        "base_branch": "main",
                        "head_branch": "topic",
                        "branch_review_commit": reviewed,
                        "reviewed_content_head": reviewed,
                        "publication_head": reviewed,
                    },
                    "task": {
                        "active_locator": ".trellis/tasks/current",
                        "archive_locator": ".trellis/tasks/archive/2026-08/current",
                    },
                }
                public_input = {"task_ref": ".trellis/tasks/current"}
                gate = {
                    "route": {
                        "typed_exit": "reprepare_required",
                        "output": copy.deepcopy(gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER),
                    },
                }
                context = {
                    "task_dir": task_dir,
                    "plan": plan,
                    "reprepare_reason_code": gtt.FINALIZATION_REPREPARE_PROVENANCE_TAIL,
                }
                args = argparse.Namespace(root=str(root), input="unused", gate=None)
                records = [{
                    "worktree": str(root),
                    "branch": "refs/heads/topic",
                    "HEAD": reviewed,
                }]
                if case == "parallel_consumer":
                    records.append({
                        "worktree": str(root.parent / "parallel-publication"),
                        "branch": "refs/heads/topic",
                        "HEAD": reviewed,
                    })
                existing_pr = {"number": 191} if case == "pull_request" else None
                remote_head = "f" * 40 if case == "remote_changed" else reviewed
                head_before = self.git(root, "rev-parse", "HEAD")

                with (
                    mock.patch.object(gtt, "finalization_public_input", return_value=(public_input, "unused")),
                    mock.patch.object(gtt, "finalization_gate_input", return_value=(gate, root / "gate.json")),
                    mock.patch.object(gtt, "check_finalization_gate_result", return_value=(gate, context)),
                    mock.patch.object(gtt, "worktree_records", return_value=records),
                    mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=existing_pr),
                    mock.patch.object(gtt, "closeout_remote_branch_head", return_value=remote_head),
                    mock.patch.object(gtt, "prepare_provenance_metadata_tail") as producer,
                    mock.patch.object(gtt, "finalizer_supersede_pre_pr_state") as retire,
                ):
                    with self.assertRaises(gtt.WorkflowError) as blocked:
                        gtt.cmd_execute_finalization_transition(args)

                producer.assert_not_called()
                retire.assert_not_called()
                if expected_reason is None:
                    self.assertEqual(
                        blocked.exception.payload["tracked_paths"],
                        [
                            ".trellis/tasks/current/closeout-plan.json",
                            ".trellis/tasks/current/marketplace-verification.json",
                        ],
                    )
                else:
                    self.assertEqual(
                        blocked.exception.payload["reason_code"],
                        expected_reason,
                    )
                self.assertEqual(self.git(root, "rev-parse", "HEAD"), head_before)
                self.assertTrue(plan_path.is_file())
                self.assertTrue(verification_path.is_file())

    def test_reprepare_preflight_accepts_an_existing_valid_unpushed_tail(self) -> None:
        root, reviewed, publication = self.fixture()
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        task_dir = root / ".trellis/tasks/current"
        task_dir.mkdir(parents=True)
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "base_branch": "main",
                "head_branch": gtt.current_branch(root),
                "branch_review_commit": reviewed,
                "reviewed_content_head": reviewed,
                "publication_head": reviewed,
            },
            "task": {
                "active_locator": ".trellis/tasks/current",
                "archive_locator": ".trellis/tasks/archive/2026-08/current",
            },
        }
        with (
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=None),
            mock.patch.object(gtt, "closeout_remote_branch_head", return_value=reviewed),
        ):
            facts = gtt.finalizer_pre_pr_provenance_reprepare_preflight(
                root,
                task_dir,
                plan,
            )
        self.assertEqual(facts["reviewed_content_head"], reviewed)
        self.assertEqual(facts["local_head"], publication)
        self.assertEqual(facts["remote_head"], reviewed)


class PrePrProvenanceReprepareFixtureTest(unittest.TestCase):
    """Reproduce the #179 ordering with a disposable, local-only fixture."""

    def git(self, root: Path, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=root, text=True).strip()

    def base_evolution_fixture(self) -> tuple[Path, Path, dict[str, Any], dict[str, Any], str, str]:
        fixture = Path(tempfile.mkdtemp(prefix="guru-179-base-evolution-"))
        self.addCleanup(lambda: shutil.rmtree(fixture, ignore_errors=True))
        root = fixture / "repo"
        remote = fixture / "remote.git"
        root.mkdir()
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
        subprocess.run(["git", "init", "-q", "-b", "topic"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.com"], cwd=root, check=True)
        subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=root, check=True)
        (root / "tracked.txt").write_text("old\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "old reviewed"], cwd=root, check=True)
        previous_reviewed = self.git(root, "rev-parse", "HEAD")
        subprocess.run(["git", "push", "-qu", "origin", "topic"], cwd=root, check=True)
        (root / "tracked.txt").write_text("current\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "current reviewed"], cwd=root, check=True)
        current_reviewed = self.git(root, "rev-parse", "HEAD")

        task_dir = root / ".trellis/tasks/fixture"
        task_dir.mkdir(parents=True)
        task_ref = ".trellis/tasks/fixture"
        archive_ref = ".trellis/tasks/archive/2026-08/fixture"
        gtt.write_json(task_dir / "task.json", {"id": "fixture", "status": "in_progress"})
        previous_plan = {
            "schema_version": gtt.CLOSEOUT_PLAN_SCHEMA_VERSION,
            "task": {"active_locator": task_ref, "archive_locator": archive_ref},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "base_branch": "main",
                "head_branch": "topic",
                "branch_review_commit": previous_reviewed,
            },
            "plan_digest": "",
        }
        previous_plan["plan_digest"] = gtt.closeout_plan_digest(previous_plan)
        gtt.write_json(task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, previous_plan)
        current_plan = {
            "schema_version": gtt.CLOSEOUT_PLAN_SCHEMA_VERSION,
            "task": {"active_locator": task_ref, "archive_locator": archive_ref},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "base_branch": "main",
                "head_branch": "topic",
                "branch_review_commit": current_reviewed,
                "reviewed_content_head": current_reviewed,
                "publication_head": current_reviewed,
            },
        }
        plan_ref = f"closeout-plan:{previous_plan['plan_digest']}"
        gate = {
            "schema_version": gtt.FINALIZATION_GATE_SCHEMA_VERSION,
            "skill_id": gtt.FINALIZE_TASK_SKILL_ID,
            "identity": {
                "task_ref": task_ref,
                "plan_ref": plan_ref,
                "plan_digest": previous_plan["plan_digest"],
                "branch_review_commit": previous_reviewed,
            },
            "route": {
                "typed_exit": "verification_required",
                "consumer": copy.deepcopy(gtt.FINALIZATION_CONSUMERS["verification_required"]),
                "output": {
                    "exit_id": "verification_required",
                    "task_ref": task_ref,
                    "plan_ref": plan_ref,
                    "repo_ref": "castbox/guru-trellis",
                    "branch_review_commit": previous_reviewed,
                    "verification_target": "extension-installation",
                },
            },
        }
        gtt.write_json(gtt.task_finalization_path(root, task_dir), gate)
        request_path = root / ".trellis/.runtime/guru-team/finalizer-inputs/fixture/verification-required.json"
        gtt.write_json(request_path, {
            "profile": "verification_required",
            "mode": "workflow",
            "task_ref": task_ref,
            "plan_ref": plan_ref,
            "branch_review_commit": previous_reviewed,
        })
        gtt.write_json(request_path.with_name("publication-ready.json"), {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": task_ref,
            "branch_review_commit": current_reviewed,
        })
        gtt.write_json(request_path.with_name("semantic-review.json"), {
            "profile": "semantic_review",
            "mode": "workflow",
            "task_ref": task_ref,
            "plan_ref": "closeout-plan:stale-semantic-review",
        })
        return root, task_dir, previous_plan, current_plan, previous_reviewed, current_reviewed

    def current_plan_evolution_fixture(
        self,
    ) -> tuple[Path, Path, dict[str, Any], dict[str, Any], dict[str, Any], str, str, str]:
        fixture = Path(tempfile.mkdtemp(prefix="guru-179-current-plan-evolution-"))
        self.addCleanup(lambda: shutil.rmtree(fixture, ignore_errors=True))
        root = fixture / "repo"
        remote = fixture / "remote.git"
        root.mkdir()
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
        subprocess.run(["git", "init", "-q", "-b", "topic"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.com"], cwd=root, check=True)
        subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=root, check=True)

        manifest = root / gtt.PROVENANCE_TAIL_MANIFEST_PATH
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({
            "installed_at": "old",
            "source": {
                "repo": "https://github.com/castbox/guru-trellis.git",
                "ref": "0" * 40,
                "commit": "0" * 40,
                "tree_state": "dirty",
                "is_mutable_ref": False,
            },
        }), encoding="utf-8")
        apply_script = root / "trellis/presets/guru-team/scripts/bash/apply.sh"
        apply_script.parent.mkdir(parents=True)
        apply_script.write_text(
            """#!/usr/bin/env bash
set -euo pipefail
repo=''
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) repo="$2"; shift 2 ;;
    *) shift ;;
  esac
done
reviewed="$(git -C "$repo" rev-parse HEAD)"
python3 - "$repo/.trellis/guru-team/extension.json" "$reviewed" <<'PY'
import json
import pathlib
import sys
path = pathlib.Path(sys.argv[1])
reviewed = sys.argv[2]
payload = json.loads(path.read_text(encoding="utf-8"))
payload["installed_at"] = "2026-08-09T00:00:00Z"
payload["source"].update({
    "ref": reviewed,
    "commit": reviewed,
    "tree_state": "clean",
    "is_mutable_ref": False,
})
path.write_text(json.dumps(payload, sort_keys=True) + "\\n", encoding="utf-8")
PY
printf '{"status":"ok"}\\n'
""",
            encoding="utf-8",
        )
        apply_script.chmod(0o755)
        (root / "base.txt").write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture base"], cwd=root, check=True)
        base_head = self.git(root, "rev-parse", "HEAD")

        task_dir = root / ".trellis/tasks/fixture"
        task_dir.mkdir(parents=True)
        task_ref = ".trellis/tasks/fixture"
        issue = {
            "number": 179,
            "url": "https://github.com/castbox/guru-trellis/issues/179",
            "title": "Finalizer current plan evolution",
            "reason": "Primary delivered scope.",
        }
        gtt.write_json(task_dir / "task.json", {
            "id": "fixture",
            "title": "#179 Finalizer current plan evolution",
            "status": "in_progress",
            "base_branch": "main",
        })
        gtt.write_json(task_dir / "issue-scope-ledger.json", {
            "schema_version": "2.0",
            "primary_issue": issue,
            "close_issues": [issue],
            "related_issues": [],
            "followup_issues": [],
        })
        workflow_change = root / "trellis/workflows/guru-team/change.txt"
        workflow_change.parent.mkdir(parents=True, exist_ok=True)
        workflow_change.write_text("reviewed-v1\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "reviewed v1"], cwd=root, check=True)
        previous_reviewed = self.git(root, "rev-parse", "HEAD")
        subprocess.run(["git", "push", "-qu", "origin", "topic"], cwd=root, check=True)

        previous_publication = gtt.prepare_provenance_metadata_tail(
            root,
            previous_reviewed,
        )["publication_head"]
        task_context = {
            "task_artifact_dir": task_ref,
            "base_branch": "main",
            "base_ref": base_head,
            "branch_name": "topic",
            "base_head_sha": base_head,
        }
        previous_title = "修复：记录 previous Finalizer plan payload"
        previous_body = valid_pr_body("#179 previous plan payload。").replace(
            "Closes #18",
            "Closes #179",
        )
        title = "修复：支持 current Finalizer plan 内容演进"
        body = valid_pr_body("#179 current Publication payload。").replace(
            "Closes #18",
            "Closes #179",
        )
        args = argparse.Namespace(
            repo="castbox/guru-trellis",
            remote="origin",
            base_branch="main",
            title=previous_title,
            include_finalization_gate=True,
        )
        with mock.patch.object(
            gtt,
            "validate_github_remote_repository",
            return_value="castbox/guru-trellis",
        ):
            prepared = gtt.prepare_closeout(
                root,
                args,
                {},
                task_dir,
                task_context,
                publication_ready={
                    "profile": "publication_ready",
                    "mode": "workflow",
                    "task_ref": task_ref,
                    "branch_review_commit": previous_reviewed,
                    "pr_title": previous_title,
                    "pr_body": previous_body,
                },
            )
        previous_plan = prepared["plan"]
        self.assertEqual(
            previous_plan["git"]["publication_head"],
            previous_publication,
        )
        gtt.write_json(task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, previous_plan)

        workflow_change.write_text("reviewed-v2\n", encoding="utf-8")
        subprocess.run(["git", "add", workflow_change.relative_to(root).as_posix()], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "reviewed v2"], cwd=root, check=True)
        current_reviewed = self.git(root, "rev-parse", "HEAD")
        prospective_plan = {
            "schema_version": gtt.CLOSEOUT_PLAN_SCHEMA_VERSION,
            "task": {
                "active_locator": task_ref,
                "archive_locator": previous_plan["task"]["archive_locator"],
            },
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "base_branch": "main",
                "head_branch": "topic",
                "branch_review_commit": current_reviewed,
                "reviewed_content_head": current_reviewed,
                "publication_head": current_reviewed,
            },
        }
        return (
            root,
            task_dir,
            previous_plan,
            prospective_plan,
            task_context,
            title,
            body,
            current_reviewed,
        )

    def test_current_plan_evolution_reuses_payload_through_real_gate_and_executor(
        self,
    ) -> None:
        (
            root,
            task_dir,
            previous_plan,
            _,
            task_context,
            title,
            body,
            current_reviewed,
        ) = self.current_plan_evolution_fixture()
        task_ref = previous_plan["task"]["active_locator"]
        package_root = (
            Path(__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages/guru-finalize-task"
        )
        publication_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": task_ref,
            "branch_review_commit": current_reviewed,
            "pr_title": title,
            "pr_body": body,
        }
        current_payload = {"title": title, "body": body}
        previous_payload = {
            key: previous_plan["publish"][key]
            for key in ("title", "body")
        }
        self.assertNotEqual(previous_payload, current_payload)
        active_input = {"value": publication_input}
        reviewed = {
            "review": {
                "status": "passed",
                "summary": "The current plan evolution route is semantically reviewed.",
            },
            "route": {
                "typed_exit": "reprepare_required",
                "consumer": copy.deepcopy(
                    gtt.FINALIZATION_CONSUMERS["reprepare_required"]
                ),
                "output": copy.deepcopy(gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER),
            },
        }
        args = argparse.Namespace(
            root=str(root),
            input="unused-input.json",
            review_input="unused-review.json",
            gate=None,
            dry_run=False,
            repo="castbox/guru-trellis",
            remote="origin",
            base_branch="main",
            title=title,
            include_finalization_gate=True,
        )
        repository_binding = {
            "head": current_reviewed,
            "branch": "topic",
            "base_ref": task_context["base_ref"],
            "diff_paths": [
                ".trellis/tasks/fixture/issue-scope-ledger.json",
                ".trellis/tasks/fixture/task.json",
                "trellis/workflows/guru-team/change.txt",
            ],
            "status_paths": [],
        }
        plan_path = task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT
        standard_gate = gtt.task_finalization_path(root, task_dir)
        transition_gate = gtt.task_finalization_transition_path(root, task_dir)

        with (
            mock.patch.object(
                gtt,
                "finalization_public_input",
                side_effect=lambda _root, _value: (
                    copy.deepcopy(active_input["value"]),
                    "<test>",
                ),
            ),
            mock.patch.object(
                gtt,
                "finalization_semantic_review_input",
                return_value=reviewed,
            ),
            mock.patch.object(gtt, "finalization_package_root", return_value=package_root),
            mock.patch.object(
                gtt,
                "validate_github_remote_repository",
                return_value="castbox/guru-trellis",
            ),
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=None),
            mock.patch.object(gtt, "finalization_verification_owner_result", return_value=None),
            mock.patch.object(gtt, "load_task_runtime_identity", return_value=task_context),
            mock.patch.object(gtt, "assert_workspace_boundary"),
            mock.patch.object(
                gtt,
                "task_publication_repository_binding",
                return_value=repository_binding,
            ),
        ):
            initial = gtt.finalization_preview_context(root, args, publication_input)
            self.assertEqual(initial["transaction_state"], "reprepare_required")
            self.assertEqual(
                initial["prepared"]["pre_pr_reprepare"]["base_evolution"][
                    "supersession_kind"
                ],
                "current_plan",
            )
            self.assertEqual(
                {
                    key: initial["plan"]["publish"][key]
                    for key in ("title", "body")
                },
                current_payload,
            )
            self.assertFalse(standard_gate.exists())
            self.assertFalse(transition_gate.exists())

            recorded = gtt.cmd_record_finalization_gate(args)
            self.assertEqual(Path(recorded["artifact_path"]).resolve(), standard_gate.resolve())
            self.assertTrue(standard_gate.is_file())
            self.assertFalse(transition_gate.exists())

            checked = gtt.cmd_check_finalization_gate(args)
            self.assertEqual(checked["typed_exit"], "reprepare_required")
            transitioned = gtt.cmd_execute_finalization_transition(args)

            self.assertEqual(transitioned["typed_exit"], "reprepare_required")
            self.assertEqual(
                transitioned["output"]["branch_review_commit"],
                current_reviewed,
            )
            self.assertNotEqual(
                transitioned["output"]["publication_head"],
                current_reviewed,
            )
            self.assertFalse(standard_gate.exists())
            self.assertFalse(transition_gate.exists())
            replacement = gtt.validate_closeout_plan(gtt.read_json(plan_path))
            self.assertEqual(
                {
                    key: replacement["publish"][key]
                    for key in ("title", "body")
                },
                current_payload,
            )
            self.assertEqual(
                replacement["git"]["reviewed_content_head"],
                current_reviewed,
            )
            self.assertEqual(
                replacement["git"]["publication_head"],
                transitioned["output"]["publication_head"],
            )
            self.assertEqual(
                transitioned["replacement_plan_digest"],
                replacement["plan_digest"],
            )
            self.assertNotEqual(previous_plan["plan_digest"], replacement["plan_digest"])

            reprepare_input = {
                "profile": "reprepare_preview",
                "mode": "workflow",
                "task_ref": task_ref,
                "reason_code": transitioned["output"]["reason_code"],
                "branch_review_commit": transitioned["output"][
                    "branch_review_commit"
                ],
                "publication_head": transitioned["output"]["publication_head"],
            }
            active_input["value"] = reprepare_input
            plan_bytes = plan_path.read_bytes()
            head_before = self.git(root, "rev-parse", "HEAD")
            preview = gtt.cmd_preview_finalization(args)

        self.assertEqual(preview["closeout_plan_digest"], replacement["plan_digest"])
        self.assertEqual(
            {
                key: preview["closeout_plan"]["publish"][key]
                for key in ("title", "body")
            },
            current_payload,
        )
        self.assertEqual(plan_path.read_bytes(), plan_bytes)
        self.assertEqual(self.git(root, "rev-parse", "HEAD"), head_before)

    def test_current_plan_evolution_rejection_matrix(self) -> None:
        cases = {
            "non_ancestor": "provenance_reprepare_base_evolution_mismatch",
            "remote_non_fast_forward": "provenance_reprepare_remote_not_reviewed_head",
            "remote_at_previous_publication": "provenance_reprepare_remote_not_reviewed_head",
            "remote_at_current_reviewed": "provenance_reprepare_remote_not_reviewed_head",
            "pull_request": "provenance_reprepare_pull_request_exists",
            "archive": "provenance_reprepare_archive_started",
            "verification_artifact": "provenance_reprepare_verification_started",
            "verification_request": "provenance_reprepare_verification_started",
            "standard_gate": "provenance_reprepare_gate_started",
            "transition_gate": "provenance_reprepare_gate_started",
            "tracked_plan": None,
        }
        for case, reason_code in cases.items():
            with self.subTest(case=case):
                (
                    root,
                    task_dir,
                    previous_plan,
                    prospective_plan,
                    _,
                    _,
                    _,
                    current_reviewed,
                ) = self.current_plan_evolution_fixture()
                candidate = copy.deepcopy(prospective_plan)
                pull_request = None
                remote_head: str | None = None
                if case == "non_ancestor":
                    candidate["git"]["branch_review_commit"] = "f" * 40
                    candidate["git"]["reviewed_content_head"] = "f" * 40
                elif case == "remote_non_fast_forward":
                    remote_head = "f" * 40
                elif case == "remote_at_previous_publication":
                    remote_head = previous_plan["git"]["publication_head"]
                elif case == "remote_at_current_reviewed":
                    remote_head = current_reviewed
                elif case == "pull_request":
                    pull_request = {"number": 179}
                elif case == "archive":
                    (root / previous_plan["task"]["archive_locator"]).mkdir(
                        parents=True,
                    )
                elif case == "verification_artifact":
                    gtt.write_json(task_dir / gtt.MARKETPLACE_VERIFICATION_ARTIFACT, {})
                elif case == "verification_request":
                    request = root / (
                        ".trellis/.runtime/guru-team/finalizer-inputs/fixture/"
                        "verification-required.json"
                    )
                    gtt.write_json(request, {
                        "profile": "verification_required",
                        "mode": "workflow",
                        "task_ref": previous_plan["task"]["active_locator"],
                        "plan_ref": f"closeout-plan:{previous_plan['plan_digest']}",
                        "branch_review_commit": previous_plan["git"][
                            "branch_review_commit"
                        ],
                        "publication_head": previous_plan["git"]["publication_head"],
                    })
                elif case == "standard_gate":
                    gtt.write_json(gtt.task_finalization_path(root, task_dir), {})
                elif case == "transition_gate":
                    gtt.write_json(gtt.task_finalization_transition_path(root, task_dir), {})
                elif case == "tracked_plan":
                    subprocess.run(
                        [
                            "git",
                            "add",
                            (task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT)
                            .relative_to(root)
                            .as_posix(),
                        ],
                        cwd=root,
                        check=True,
                    )

                patches = [
                    mock.patch.object(
                        gtt,
                        "resolve_closeout_pull_request",
                        return_value=pull_request,
                    )
                ]
                if remote_head is not None:
                    patches.append(
                        mock.patch.object(
                            gtt,
                            "closeout_remote_branch_head",
                            return_value=remote_head,
                        )
                    )
                with (
                    patches[0],
                    patches[1] if len(patches) == 2 else contextlib.nullcontext(),
                    self.assertRaises(gtt.WorkflowError) as blocked,
                ):
                    gtt.finalizer_current_plan_base_evolution_supersession_preflight(
                        root,
                        task_dir,
                        previous_plan,
                        candidate,
                    )
                if case == "tracked_plan":
                    self.assertEqual(
                        blocked.exception.payload["tracked_paths"],
                        [".trellis/tasks/fixture/closeout-plan.json"],
                    )
                else:
                    self.assertEqual(
                        blocked.exception.payload.get("reason_code"),
                        reason_code,
                    )
                    if case == "remote_at_previous_publication":
                        self.assertIs(
                            blocked.exception.payload.get(
                                "predecessor_has_outbound_publication_side_effect"
                            ),
                            True,
                        )

    def test_base_evolution_supersession_is_exact_and_fail_closed(self) -> None:
        root, task_dir, previous_plan, current_plan, previous_reviewed, current_reviewed = self.base_evolution_fixture()
        with mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=None):
            facts = gtt.finalizer_pre_pr_base_evolution_supersession_preflight(
                root, task_dir, previous_plan, current_plan
            )
        self.assertEqual(facts["previous_reviewed_content_head"], previous_reviewed)
        self.assertEqual(facts["reviewed_content_head"], current_reviewed)
        self.assertEqual(facts["remote_head"], previous_reviewed)

        failures = {
            "non_ancestor": "provenance_reprepare_base_evolution_mismatch",
            "pull_request": "provenance_reprepare_pull_request_exists",
            "archive": "provenance_reprepare_archive_started",
            "remote": "provenance_reprepare_remote_not_reviewed_head",
            "parallel": "provenance_reprepare_parallel_publication_consumer",
        }
        for case, reason in failures.items():
            with self.subTest(case=case):
                candidate = copy.deepcopy(current_plan)
                pr = None
                remote_head = previous_reviewed
                records = gtt.worktree_records(root)
                archive = root / previous_plan["task"]["archive_locator"]
                if case == "non_ancestor":
                    candidate["git"]["branch_review_commit"] = "f" * 40
                    candidate["git"]["reviewed_content_head"] = "f" * 40
                elif case == "pull_request":
                    pr = {"number": 179}
                elif case == "archive":
                    archive.mkdir(parents=True, exist_ok=True)
                elif case == "remote":
                    remote_head = "f" * 40
                elif case == "parallel":
                    records = records + [{
                        "worktree": str(root.parent / "parallel"),
                        "branch": "refs/heads/topic",
                        "HEAD": current_reviewed,
                    }]
                with (
                    mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=pr),
                    mock.patch.object(gtt, "closeout_remote_branch_head", return_value=remote_head),
                    mock.patch.object(gtt, "worktree_records", return_value=records),
                    self.assertRaises(gtt.WorkflowError) as blocked,
                ):
                    gtt.finalizer_pre_pr_base_evolution_supersession_preflight(
                        root, task_dir, previous_plan, candidate
                    )
                self.assertEqual(blocked.exception.payload.get("reason_code"), reason)
                if archive.exists():
                    archive.rmdir()

        subprocess.run(
            ["git", "add", task_dir.relative_to(root).as_posix() + "/closeout-plan.json"],
            cwd=root,
            check=True,
        )
        with (
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=None),
            self.assertRaises(gtt.WorkflowError) as tracked,
        ):
            gtt.finalizer_pre_pr_base_evolution_supersession_preflight(
                root, task_dir, previous_plan, current_plan
            )
        self.assertEqual(
            tracked.exception.payload["tracked_paths"],
            [".trellis/tasks/fixture/closeout-plan.json"],
        )

    def test_base_evolution_gate_record_check_execute_preserves_legacy_until_supersession(
        self,
    ) -> None:
        (
            root,
            task_dir,
            previous_plan,
            current_plan,
            previous_reviewed,
            current_reviewed,
        ) = self.base_evolution_fixture()
        task_ref = previous_plan["task"]["active_locator"]
        current_plan.update({
            "publish": {
                "title": "修复 Finalizer gate supersession",
                "body": "## 变更摘要\n\n- 保留 legacy gate 直到 transition 完成。\n",
            },
            "marketplace": {"required": True},
        })
        current_plan["plan_digest"] = gtt.closeout_plan_digest(current_plan)
        current_plan_ref = f"closeout-plan:{current_plan['plan_digest']}"
        public_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": task_ref,
            "branch_review_commit": current_reviewed,
            "pr_title": current_plan["publish"]["title"],
            "pr_body": current_plan["publish"]["body"],
        }
        reviewed = {
            "review": {
                "status": "passed",
                "summary": "The current provenance reprepare route is semantically reviewed.",
            },
            "route": {
                "typed_exit": "reprepare_required",
                "consumer": copy.deepcopy(
                    gtt.FINALIZATION_CONSUMERS["reprepare_required"]
                ),
                "output": copy.deepcopy(gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER),
            },
        }
        legacy_path = gtt.task_finalization_path(root, task_dir)
        legacy_bytes = legacy_path.read_bytes()
        transition_path = gtt.task_finalization_transition_path(root, task_dir)
        package_root = (
            Path(__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages/guru-finalize-task"
        )
        args = argparse.Namespace(
            root=str(root),
            input="unused-input.json",
            review_input="unused-review.json",
            gate=None,
            dry_run=False,
        )
        preview_count = 0

        def preview(
            _root: Path,
            _args: argparse.Namespace,
            _public_input: dict[str, Any],
        ) -> dict[str, Any]:
            nonlocal preview_count
            preview_count += 1
            base_evolution = gtt.finalizer_pre_pr_base_evolution_supersession_preflight(
                root,
                task_dir,
                previous_plan,
                current_plan,
            )
            return {
                "task_dir": task_dir,
                "task_context": {},
                "prepared": {
                    "pre_pr_reprepare": {
                        "previous_plan": previous_plan,
                        "prior_state": "content_pushed",
                        "base_evolution": base_evolution,
                    },
                },
                "plan": current_plan,
                "plan_ref": current_plan_ref,
                "transaction_state": "reprepare_required",
                "published_transition_complete": False,
                "publication_status": "current",
                "publication_stale_reason": None,
                "reprepare_reason_code": gtt.FINALIZATION_REPREPARE_PROVENANCE_TAIL,
                "verification": None,
            }

        replacement_plan = copy.deepcopy(current_plan)
        replacement_plan["plan_digest"] = gtt.closeout_plan_digest(replacement_plan)
        provenance = {
            "reviewed_content_head": current_reviewed,
            "publication_head": current_reviewed,
            "metadata_tail": {
                "commit": current_reviewed,
                "parent": current_reviewed,
                "path": gtt.PROVENANCE_TAIL_MANIFEST_PATH,
            },
        }
        with (
            mock.patch.object(
                gtt,
                "finalization_public_input",
                return_value=(public_input, "<test>"),
            ),
            mock.patch.object(
                gtt,
                "finalization_semantic_review_input",
                return_value=reviewed,
            ),
            mock.patch.object(gtt, "finalization_task_dir", return_value=task_dir),
            mock.patch.object(gtt, "finalization_package_root", return_value=package_root),
            mock.patch.object(gtt, "finalization_preview_context", side_effect=preview),
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=None),
            mock.patch.object(
                gtt,
                "prepare_provenance_metadata_tail",
                return_value=provenance,
            ),
            mock.patch.object(
                gtt,
                "prepare_closeout",
                return_value={"plan": replacement_plan},
            ),
            mock.patch.object(
                gtt,
                "validate_closeout_plan_for_migration",
                side_effect=lambda value: value,
            ),
            mock.patch.object(
                gtt,
                "validate_closeout_plan",
                side_effect=lambda value: value,
            ),
        ):
            recorded = gtt.cmd_record_finalization_gate(args)
            self.assertEqual(
                Path(recorded["artifact_path"]).resolve(),
                transition_path.resolve(),
            )
            self.assertEqual(legacy_path.read_bytes(), legacy_bytes)
            self.assertEqual(
                gtt.read_json(transition_path)["route"]["typed_exit"],
                "reprepare_required",
            )

            _, default_gate_path = gtt.finalization_gate_input(
                root,
                public_input,
                None,
            )
            self.assertEqual(default_gate_path.resolve(), transition_path.resolve())

            args.gate = gtt.repo_relative(root, legacy_path)
            with self.assertRaises(gtt.WorkflowError) as stale_legacy:
                gtt.cmd_check_finalization_gate(args)
            self.assertTrue(
                any(
                    "objective identity mismatch" in error
                    for error in stale_legacy.exception.payload["errors"]
                ),
                stale_legacy.exception.payload["errors"],
            )
            args.gate = None

            checked = gtt.cmd_check_finalization_gate(args)
            self.assertEqual(checked["typed_exit"], "reprepare_required")
            self.assertEqual(legacy_path.read_bytes(), legacy_bytes)

            transitioned = gtt.cmd_execute_finalization_transition(args)

        self.assertEqual(preview_count, 4)
        self.assertEqual(transitioned["typed_exit"], "reprepare_required")
        self.assertEqual(
            transitioned["output"],
            {
                "exit_id": "reprepare_required",
                "task_ref": task_ref,
                "reason_code": gtt.FINALIZATION_REPREPARE_PROVENANCE_TAIL,
                "branch_review_commit": current_reviewed,
                "publication_head": current_reviewed,
            },
        )
        self.assertFalse(legacy_path.exists())
        self.assertFalse(transition_path.exists())
        self.assertFalse(
            root.joinpath(
                ".trellis/.runtime/guru-team/finalizer-inputs/fixture/verification-required.json"
            ).exists()
        )
        self.assertTrue((task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT).is_file())
        self.assertNotEqual(previous_reviewed, current_reviewed)

    def test_transition_gate_without_legacy_predecessor_fails_closed(self) -> None:
        root, task_dir, _, _, _, _ = self.base_evolution_fixture()
        legacy_path = gtt.task_finalization_path(root, task_dir)
        transition_path = gtt.task_finalization_transition_path(root, task_dir)
        gtt.write_json(transition_path, gtt.read_json(legacy_path))
        legacy_path.unlink()
        public_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": ".trellis/tasks/fixture",
        }

        with (
            mock.patch.object(gtt, "finalization_task_dir", return_value=task_dir),
            self.assertRaises(gtt.WorkflowError) as blocked,
        ):
            gtt.finalization_gate_input(root, public_input, None)

        self.assertIn("legacy predecessor checkpoint", str(blocked.exception))

    def test_base_evolution_retirement_ignores_unrelated_finalizer_input_profiles(self) -> None:
        root, task_dir, previous_plan, current_plan, _, _ = self.base_evolution_fixture()
        request_dir = root / ".trellis/.runtime/guru-team/finalizer-inputs/fixture"
        verification_request = request_dir / "verification-required.json"
        publication_request = request_dir / "publication-ready.json"
        semantic_request = request_dir / "semantic-review.json"
        with mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=None):
            gtt.finalizer_pre_pr_base_evolution_supersession_preflight(
                root, task_dir, previous_plan, current_plan
            )
        with mock.patch.object(
            gtt,
            "validate_closeout_plan_for_migration",
            side_effect=lambda value: value,
        ):
            retired = gtt.finalizer_supersede_pre_pr_state(root, task_dir)

        self.assertFalse(verification_request.exists())
        self.assertTrue(publication_request.is_file())
        self.assertTrue(semantic_request.is_file())
        self.assertIn(
            ".trellis/.runtime/guru-team/finalizer-inputs/fixture/verification-required.json",
            retired,
        )
        self.assertNotIn(repo_relative := gtt.repo_relative(root, publication_request), retired)
        self.assertNotIn(gtt.repo_relative(root, semantic_request), retired)
        self.assertEqual(
            repo_relative,
            ".trellis/.runtime/guru-team/finalizer-inputs/fixture/publication-ready.json",
        )

    def test_reviewed_push_dirty_rejection_tail_reprepare_and_exact_ref(self) -> None:
        fixture = Path(tempfile.mkdtemp(prefix="guru-191-pre-pr-fixture-"))
        self.addCleanup(lambda: shutil.rmtree(fixture, ignore_errors=True))
        root = fixture / "repo"
        remote = fixture / "remote.git"
        root.mkdir()
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
        subprocess.run(["git", "init", "-q", "-b", "topic"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.com"], cwd=root, check=True)
        subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=root, check=True)
        manifest = root / gtt.PROVENANCE_TAIL_MANIFEST_PATH
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({
            "installed_at": "old",
            "source": {
                "repo": "https://github.com/castbox/guru-trellis.git",
                "ref": "0" * 40,
                "commit": "0" * 40,
                "tree_state": "dirty",
                "is_mutable_ref": False,
            },
        }), encoding="utf-8")
        apply_script = root / "trellis/presets/guru-team/scripts/bash/apply.sh"
        apply_script.parent.mkdir(parents=True)
        apply_script.write_text(
            """#!/usr/bin/env bash
set -euo pipefail
repo=''
while [[ $# -gt 0 ]]; do
  case \"$1\" in
    --repo) repo=\"$2\"; shift 2 ;;
    *) shift ;;
  esac
done
reviewed=\"$(git -C \"$repo\" rev-parse HEAD)\"
python3 - \"$repo/.trellis/guru-team/extension.json\" \"$reviewed\" <<'PY'
import json
import pathlib
import sys
path = pathlib.Path(sys.argv[1])
reviewed = sys.argv[2]
payload = json.loads(path.read_text(encoding="utf-8"))
payload["installed_at"] = "2026-08-08T00:00:00Z"
payload["source"].update({
    "ref": reviewed,
    "commit": reviewed,
    "tree_state": "clean",
    "is_mutable_ref": False,
})
path.write_text(json.dumps(payload, sort_keys=True) + "\\n", encoding="utf-8")
PY
printf '{\"status\":\"ok\"}\\n'
""",
            encoding="utf-8",
        )
        apply_script.chmod(0o755)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "reviewed content"], cwd=root, check=True)
        reviewed = self.git(root, "rev-parse", "HEAD")
        subprocess.run(["git", "push", "-qu", "origin", "topic"], cwd=root, check=True)
        self.assertEqual(gtt.closeout_remote_branch_head(root, {
            "git": {"remote": "origin", "head_branch": "topic"},
        }), reviewed)
        self.assertTrue(gtt.finalizer_pre_pr_provenance_tail_required(root, {
            "git": {"branch_review_commit": reviewed},
        }))
        with self.assertRaises(gtt.WorkflowError) as rejected:
            gtt.extension_verification_manifest_source(root, {}, task_bearing=True)
        self.assertEqual(rejected.exception.payload["reason_code"], "extension_source_not_clean")

        task_dir = root / ".trellis/tasks/fixture"
        task_dir.mkdir(parents=True)
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "base_branch": "main",
                "head_branch": "topic",
                "branch_review_commit": reviewed,
                "reviewed_content_head": reviewed,
                "publication_head": reviewed,
            },
            "task": {
                "active_locator": ".trellis/tasks/fixture",
                "archive_locator": ".trellis/tasks/archive/2026-08/fixture",
            },
            "projection": {"reviewed_tracked_bindings": []},
        }
        plan["plan_digest"] = gtt.closeout_plan_digest(plan)
        old_plan_ref = f"closeout-plan:{plan['plan_digest']}"
        plan_path = task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT
        verification_path = task_dir / gtt.MARKETPLACE_VERIFICATION_ARTIFACT
        gtt.write_json(plan_path, plan)
        verification_path.write_text("{}\n", encoding="utf-8")
        public_input = {"task_ref": ".trellis/tasks/fixture"}
        gate = {
            "route": {
                "typed_exit": "reprepare_required",
                "output": copy.deepcopy(gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER),
            },
        }
        context = {
            "task_dir": task_dir,
            "plan": plan,
            "reprepare_reason_code": gtt.FINALIZATION_REPREPARE_PROVENANCE_TAIL,
        }
        args = argparse.Namespace(root=str(root), input="unused", gate=None)
        with (
            mock.patch.object(gtt, "finalization_public_input", return_value=(public_input, "unused")),
            mock.patch.object(gtt, "finalization_gate_input", return_value=(gate, root / "gate.json")),
            mock.patch.object(gtt, "check_finalization_gate_result", return_value=(gate, context)),
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=None),
            mock.patch.object(gtt, "finalization_output_contract", return_value={"type": "object"}),
        ):
            result = gtt.cmd_execute_finalization_transition(args)

        publication = result["publication_head"]
        self.assertNotEqual(publication, reviewed)
        self.assertEqual(self.git(root, "rev-parse", "HEAD"), publication)
        self.assertFalse(plan_path.exists())
        self.assertFalse(verification_path.exists())
        self.assertEqual(
            gtt.validate_provenance_metadata_tail(root, reviewed, publication)["status"],
            "passed",
        )
        self.assertFalse(gtt.finalizer_pre_pr_provenance_tail_required(root, {
            "git": {"branch_review_commit": reviewed},
        }))
        self.assertEqual(result["output"], {
            "exit_id": "reprepare_required",
            "task_ref": public_input["task_ref"],
            "reason_code": gtt.FINALIZATION_REPREPARE_PROVENANCE_TAIL,
            "branch_review_commit": reviewed,
            "publication_head": publication,
        })

        new_plan = copy.deepcopy(plan)
        new_plan["git"]["publication_head"] = publication
        new_plan["plan_digest"] = gtt.closeout_plan_digest(new_plan)
        new_plan_ref = f"closeout-plan:{new_plan['plan_digest']}"
        self.assertNotEqual(new_plan_ref, old_plan_ref)
        self.assertTrue(gtt.closeout_verification_plan_ref_matches(new_plan, new_plan_ref))
        self.assertFalse(gtt.closeout_verification_plan_ref_matches(new_plan, old_plan_ref))

        reprepare_input = {
            **result["output"],
            "profile": "reprepare_preview",
            "mode": "workflow",
        }
        reprepare_input.pop("exit_id")
        prepared = {
            "plan": new_plan,
            "ledger": {},
            "metadata_tail": {"commit": publication, "parent": reviewed},
        }
        verification = ({}, {"typed_exit": "not_required"})
        with (
            mock.patch.object(gtt, "finalization_task_dir", return_value=task_dir),
            mock.patch.object(gtt, "task_dir_is_archived", return_value=False),
            mock.patch.object(gtt, "load_config", return_value={}),
            mock.patch.object(gtt, "finalization_verification_owner_result", return_value=verification),
            mock.patch.object(gtt, "load_task_runtime_identity", return_value={}),
            mock.patch.object(gtt, "assert_workspace_boundary"),
            mock.patch.object(gtt, "task_json", return_value={"status": "in_progress"}),
            mock.patch.object(gtt, "prepare_closeout", return_value=prepared) as prepare,
            mock.patch.object(gtt, "resolve_closeout_pre_draft_state", return_value="prepared"),
        ):
            preview = gtt.finalization_preview_context(
                root,
                argparse.Namespace(),
                reprepare_input,
            )
        prepare.assert_called_once()
        self.assertEqual(
            prepare.call_args.kwargs["publication_ready"],
            {
                "profile": "publication_ready",
                "mode": "workflow",
                "task_ref": public_input["task_ref"],
                "branch_review_commit": reviewed,
            },
        )
        self.assertEqual(preview["plan_ref"], new_plan_ref)
        self.assertEqual(preview["plan"]["git"]["branch_review_commit"], reviewed)
        self.assertEqual(preview["plan"]["git"]["publication_head"], publication)
        self.assertEqual(preview["publication_status"], "current")

        subprocess.run(["git", "push", "-q", "origin", "topic"], cwd=root, check=True)
        exact_ref = "refs/heads/topic"
        remote_proc = gtt.run(
            gtt.extension_verification_remote_ref_command(str(remote), exact_ref),
            cwd=root,
            check=False,
        )
        self.assertEqual(
            gtt.extension_verification_resolved_remote_head(remote_proc, exact_ref),
            publication,
        )


class ExtensionVersionPayloadTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".trellis/guru-team").mkdir(parents=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_extension_manifest(self) -> None:
        payload = {
            "schema_version": "1.0",
            "extension": {
                "extension_id": "guru-team",
                "version": "0.6.5-guru.3",
                "workflow_template_id": "guru-team",
                "target_trellis_cli": "0.6.5",
                "requires": {"trellis_cli": "0.6.5"},
                "tested": {"trellis_cli": ["0.6.5"]},
            },
            "installed_at": "2026-07-04T00:00:00Z",
            "source": {
                "repo": "https://github.com/castbox/guru-trellis.git",
                "ref": "main",
                "commit": "abc123",
                "tree_state": "clean",
                "is_mutable_ref": True,
            },
            "install": {
                "selected_platforms": ["codex", "cursor"],
                "all_platforms": False,
            },
        }
        (self.root / ".trellis/guru-team/extension.json").write_text(
            json.dumps(payload),
            encoding="utf-8",
        )

    def test_guru_team_extension_payload_reads_installed_manifest(self) -> None:
        self.write_extension_manifest()

        payload = gtt.guru_team_extension_payload(self.root)

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["version"], "0.6.5-guru.3")
        self.assertEqual(payload["workflow_template_id"], "guru-team")
        self.assertEqual(payload["target_trellis_cli"], "0.6.5")
        self.assertEqual(payload["tested_trellis_cli"], ["0.6.5"])
        self.assertEqual(payload["source_tree_state"], "clean")
        self.assertEqual(payload["selected_platforms"], ["codex", "cursor"])

    def test_guru_team_extension_payload_reports_missing_manifest(self) -> None:
        payload = gtt.guru_team_extension_payload(self.root)

        self.assertEqual(payload["status"], "missing")
        self.assertEqual(payload["path"], ".trellis/guru-team/extension.json")

    def test_guru_team_extension_payload_reports_invalid_manifest(self) -> None:
        (self.root / ".trellis/guru-team/extension.json").write_text("{", encoding="utf-8")

        payload = gtt.guru_team_extension_payload(self.root)

        self.assertEqual(payload["status"], "invalid")
        self.assertIn("invalid", payload["error"])

    def test_check_env_payload_includes_extension_and_missing_warning(self) -> None:
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "infer_github_repo", return_value="owner/repo"),
            mock.patch.object(gtt, "current_branch", return_value="main"),
            mock.patch.object(gtt, "resolve_base_branch", return_value=("main", ["main"])),
            mock.patch.object(gtt, "git_dirty", return_value=False),
            mock.patch.object(gtt, "configured_worktree_root", return_value=self.root / "worktrees"),
            mock.patch.object(gtt, "worktree_lines", return_value=[]),
            mock.patch.object(gtt.shutil, "which", return_value="/usr/bin/gh"),
            mock.patch.object(gtt, "run", return_value=mock.Mock(returncode=0)),
        ):
            payload = gtt.check_env_payload(self.root)

        self.assertEqual(payload["guru_team_extension"]["status"], "missing")
        self.assertTrue(any("extension manifest" in item for item in payload["warnings"]))

    def test_cmd_version_returns_extension_payload(self) -> None:
        self.write_extension_manifest()
        with mock.patch.object(gtt, "repo_root", return_value=self.root):
            payload = gtt.cmd_version(argparse.Namespace(root=str(self.root), json=True))

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["guru_team_extension"]["version"], "0.6.5-guru.3")
        self.assertEqual(payload["guru_team_extension"]["target_trellis_cli"], "0.6.5")


class TaskRuntimeBoundaryContractTest(unittest.TestCase):
    def test_active_runtime_rebuilds_missing_ignored_mappings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "096-task-runtime-boundary"
            task_dir = root / ".trellis/tasks/07-10-096-task-runtime-boundary"
            task_dir.mkdir(parents=True)
            gtt.write_json(
                task_dir / "task.json",
                {
                    "id": "096-task-runtime-boundary",
                    "name": "096-task-runtime-boundary",
                    "title": "task",
                    "branch": "chore/096-task-runtime-boundary",
                    "base_branch": "main",
                    "status": "in_progress",
                    "assignee": "tester",
                    "creator": "tester",
                },
            )
            config = {**gtt.DEFAULTS, "github_repo": "owner/repo"}
            records = [
                {
                    "worktree": str(root),
                    "branch": "refs/heads/chore/096-task-runtime-boundary",
                }
            ]
            with (
                mock.patch.object(gtt, "repo_root", return_value=root),
                mock.patch.object(gtt, "worktree_records", return_value=records),
                mock.patch.object(gtt, "diff_base_ref", return_value="main"),
                mock.patch.object(
                    gtt,
                    "run",
                    return_value=mock.Mock(returncode=0, stdout=f"{'a' * 40}\n"),
                ),
            ):
                context = gtt.load_task_runtime_identity(task_dir, config)

            self.assertEqual(context["_identity_source"], "task_json_runtime_mapping")
            self.assertEqual(context["workspace_slug"], root.name)
            self.assertTrue(
                gtt.runtime_task_path(root, config, "096-task-runtime-boundary").is_file()
            )
            self.assertTrue(
                gtt.runtime_workspace_path(root, config, root.name).is_file()
            )

    def test_parallel_tasks_use_distinct_runtime_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first_task = root / ".trellis/tasks/07-10-096-first"
            second_task = root / ".trellis/tasks/07-10-097-second"
            first_task.mkdir(parents=True)
            second_task.mkdir(parents=True)
            self.assertNotEqual(gtt.runtime_task_path(root, gtt.DEFAULTS, "096-first"), gtt.runtime_task_path(root, gtt.DEFAULTS, "097-second"))
            self.assertNotEqual(gtt.runtime_workspace_path(root, gtt.DEFAULTS, "096-first"), gtt.runtime_workspace_path(root, gtt.DEFAULTS, "097-second"))


class ActivePublicReferenceContractTest(unittest.TestCase):
    REPO_ROOT = Path(__file__).resolve().parents[5]
    FORBIDDEN_REFERENCES = (
        "handoff.workspace_path",
        "handoff `workspace_path`",
        ".trellis/guru-team/handoff.json",
    )

    def managed_overlay_files(self, repo_root: Path) -> list[Path]:
        overlay_root = repo_root / "trellis/presets/guru-team/overlays"
        files: list[Path] = []
        for source in overlay_root.rglob("*"):
            if (
                not source.is_file()
                or "__pycache__" in source.parts
                or source.suffix in {".pyc", ".pyo"}
            ):
                continue
            files.append(source)
            files.append(repo_root / source.relative_to(overlay_root))
        return files

    def active_public_files(self, repo_root: Path | None = None) -> list[Path]:
        root = repo_root or self.REPO_ROOT
        files = [
            root / "README.md",
            root / "trellis/workflows/guru-team/workflow.md",
            root / "trellis/workflows/guru-team/README.md",
            root / "trellis/presets/guru-team/README.md",
            root / ".trellis/workflow.md",
        ]
        files.extend(self.managed_overlay_files(root))
        for public_root in [
            root / "docs/requirements",
            root / ".trellis/spec",
        ]:
            files.extend(path for path in public_root.rglob("*") if path.is_file())
        return sorted(path for path in set(files) if path.is_file())

    def active_public_reference_violations(self, repo_root: Path | None = None) -> list[str]:
        root = repo_root or self.REPO_ROOT
        violations: list[str] = []
        for path in self.active_public_files(root):
            text = path.read_text(encoding="utf-8")
            for reference in self.FORBIDDEN_REFERENCES:
                if reference in text:
                    violations.append(f"{path.relative_to(root)}: {reference}")
        return violations

    def test_active_public_surfaces_do_not_restore_legacy_workspace_api(self) -> None:
        self.assertEqual(self.active_public_reference_violations(), [])

    def test_review_closure_contract_is_explicit_and_dogfood_copies_match(self) -> None:
        root = self.REPO_ROOT
        canonical_workflow = root / "trellis/workflows/guru-team/workflow.md"
        dogfood_workflow = root / ".trellis/workflow.md"
        self.assertEqual(canonical_workflow.read_bytes(), dogfood_workflow.read_bytes())

        workflow_text = canonical_workflow.read_text(encoding="utf-8")
        for expected in [
            'guru-skill-invoke: {"skill":"guru-review-branch"',
            'guru-skill-exit: {"skill":"guru-review-branch","exit":"passed"',
            'guru-skill-exit: {"skill":"guru-review-branch","exit":"implementation_required"',
            'guru-skill-exit: {"skill":"guru-review-branch","exit":"scope_confirmation_required"',
            'guru-skill-exit: {"skill":"guru-review-branch","exit":"blocked"',
        ]:
            self.assertIn(expected, workflow_text)
        for step_local_detail in [
            "reuse_decision: reuse-for-closure",
            "replacement closure chain",
            "becomes a new finding owner",
        ]:
            self.assertNotIn(step_local_detail, workflow_text)

        package_contract = " ".join(
            (
                root
                / "trellis/skills/guru-team/packages/guru-review-branch/references/contract.md"
            ).read_text(encoding="utf-8").split()
        )
        for expected in [
            "Qualify every candidate before assigning severity",
            "Retain the original `introduced_head`",
            "bind a later `closure_head`",
            "ancestry, not equality, proves finding continuity",
            "Closure has no public exit, recorder call, or artifact",
            "distinct fresh reviewer",
            "fails closed before owner evaluation",
        ]:
            self.assertIn(expected, package_contract)

    def test_scanner_detects_forbidden_reference_in_dogfood_codex_agent_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            relative = Path(".codex/agents/trellis-check.toml")
            canonical = root / "trellis/presets/guru-team/overlays" / relative
            dogfood = root / relative
            canonical.parent.mkdir(parents=True)
            dogfood.parent.mkdir(parents=True)
            canonical.write_text("description = 'portable boundary'\n", encoding="utf-8")
            dogfood.write_text("description = 'handoff.workspace_path'\n", encoding="utf-8")

            violations = self.active_public_reference_violations(root)

            self.assertEqual(violations, [".codex/agents/trellis-check.toml: handoff.workspace_path"])


def materialize_extension_verification_installed_asset_target(
    source: Path,
    installed: Path,
) -> list[dict[str, Any]]:
    expectations, _, _ = gtt.extension_verification_installed_asset_facts(
        source,
        installed,
    )
    for expectation in expectations:
        source_path = source / expectation["source_path"]
        installed_path = installed / expectation["path"]
        installed_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, installed_path)
    managed_assets = [
        item["path"]
        for item in expectations
        if item["relation"] == "managed_manifest"
    ]
    manifest_files = [
        {
            "path": item["path"],
            "source": item["source_path"],
            "sha256": item["expected_sha256"],
            "executable": False,
            "action": "installed",
        }
        for item in expectations
        if item["relation"] in {"skill_manifest", "platform_manifest"}
    ]
    gtt.write_json(
        installed / ".trellis/guru-team/extension.json",
        {
            "install": {
                "selected_platforms": ["claude", "codex", "cursor"],
                "managed_assets": managed_assets,
            },
            "skill_packages": {"files": manifest_files},
        },
    )
    return expectations


def copy_extension_verification_source_fixture(destination: Path) -> None:
    source = Path(__file__).resolve().parents[5]
    paths = (
        "trellis/workflows/guru-team/workflow.md",
        "trellis/workflows/guru-team/config-template.yml",
        "trellis/workflows/guru-team/scripts/bash/"
        "execute-extension-verification.sh",
        "trellis/workflows/guru-team/scripts/bash/"
        "record-extension-verification.sh",
        "trellis/workflows/guru-team/scripts/bash/"
        "check-extension-verification.sh",
        "trellis/workflows/guru-team/scripts/bash/"
        "invoke-extension-verification.sh",
        "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py",
        "trellis/presets/guru-team/scripts/bash/"
        "verify-throwaway-install.sh",
        "trellis/presets/guru-team/ownership/upstream-ownership.json",
    )
    for relative in paths:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, target)
    shutil.copytree(
        source / "trellis/workflows/guru-team/schemas",
        destination / "trellis/workflows/guru-team/schemas",
    )
    shutil.copytree(
        source
        / "trellis/skills/guru-team/packages/"
        "guru-verify-extension-installation",
        destination
        / "trellis/skills/guru-team/packages/"
        "guru-verify-extension-installation",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )
    shutil.copytree(
        source / "trellis/presets/guru-team/overlays",
        destination / "trellis/presets/guru-team/overlays",
    )


class ExtensionVerificationRuntimeTest(unittest.TestCase):
    PACKAGE = (
        Path(__file__).resolve().parents[5]
        / "trellis/skills/guru-team/packages/guru-verify-extension-installation"
    )

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(
            ["git", "init", "-q", "-b", "main"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "extension-eval@example.invalid"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Extension Eval"],
            cwd=self.root,
            check=True,
        )
        self.task_dir = self.root / ".trellis/tasks/current"
        self.task_dir.mkdir(parents=True)
        scripts_dir = self.root / ".trellis/scripts"
        scripts_dir.mkdir(parents=True)
        (scripts_dir / "task.py").write_text(
            "#!/usr/bin/env python3\n"
            "import sys\n"
            "if sys.argv[1:] == ['current']:\n"
            "    print('.trellis/tasks/current')\n"
            "    raise SystemExit(0)\n"
            "raise SystemExit(2)\n",
            encoding="utf-8",
        )
        gtt.write_json(
            self.task_dir / "task.json",
            {
                "id": "current",
                "name": "current",
                "title": "Extension verification",
                "status": "in_progress",
                "branch": "main",
                "base_branch": "main",
            },
        )
        gtt.write_json(
            self.task_dir / "issue-scope-ledger.json",
            {
                "schema_version": "2.0",
                "primary_issue": {
                    "number": 117,
                    "url": "https://github.com/example/guru-extension/issues/117",
                    "title": "Extension verification",
                    "reason": "Primary task scope.",
                },
                "close_issues": [],
                "related_issues": [],
                "followup_issues": [],
            },
        )
        (self.root / ".trellis/guru-team").mkdir(parents=True)
        (self.root / ".trellis/guru-team/config.yml").write_text(
            "github_repo: example/guru-extension\n",
            encoding="utf-8",
        )
        gtt.write_json(
            self.root / ".trellis/guru-team/extension.json",
            {
                "schema_version": "2.0",
                "source": {
                    "repo": "https://github.com/example/guru-extension.git",
                    "ref": "refs/heads/main",
                    "commit": "b" * 40,
                    "tree_state": "clean",
                    "is_mutable_ref": True,
                },
            },
        )
        (self.root / ".gitignore").write_text(
            ".trellis/.runtime/\n",
            encoding="utf-8",
        )
        (self.root / "README.md").write_text("fixture\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-qm", "fixture"],
            cwd=self.root,
            check=True,
        )
        self.head = gtt.current_head(self.root)
        gtt.write_runtime_mappings(
            self.root,
            gtt.load_config(self.root),
            {
                "workspace_slug": "current",
                "task_slug": "current",
                "task_dir": ".trellis/tasks/current",
                "branch_name": "main",
            },
            self.root,
        )
        self.env = mock.patch.dict(
            os.environ,
            {"GURU_TEAM_INVOKED_PACKAGE_ROOT": str(self.PACKAGE)},
        )
        self.env.start()

    def tearDown(self) -> None:
        self.env.stop()
        self.tmp.cleanup()

    def public_input(
        self,
        mode: str,
        *,
        task: bool,
        plan_ref: str = "closeout-plan:current",
    ) -> dict[str, Any]:
        if mode == "workflow":
            return {
                "profile": "verification_required",
                "mode": "workflow",
                "task_ref": ".trellis/tasks/current",
                "plan_ref": plan_ref,
                "repo_ref": "example/guru-extension",
                "branch_review_commit": self.head,
                "publication_head": self.head,
                "verification_target": "extension-installation",
            }
        payload: dict[str, Any] = {
            "profile": "standalone_verification",
            "mode": "standalone",
            "repo_ref": "example/guru-extension",
            "remote": "origin",
            "ref": "refs/heads/main",
            "caller_intent": "verify-extension-installation",
        }
        if task:
            payload["task_ref"] = ".trellis/tasks/current"
        return payload

    def execution(
        self,
        public_input: dict[str, Any],
        status: str,
        selected: list[str],
        *,
        sensitive_argv: str | None = None,
    ) -> dict[str, Any]:
        branch_review_commit = (
            public_input["branch_review_commit"]
            if public_input["mode"] == "workflow"
            else None
        )
        reviewed_content_sha256 = (
            gtt.reviewed_content_identity(self.root)["sha256"]
            if "task_ref" in public_input
            else None
        )
        remote_reviewed_content_sha256 = (
            reviewed_content_sha256
            if reviewed_content_sha256 is not None
            else None
            if status in {"not_run", "blocked"}
            else "1" * 64
        )
        commands = (
            []
            if status == "not_run"
            else [{
                "id": "verify_throwaway_installation",
                "checkout_owner": "extension_source_checkout",
                "argv": [
                    sensitive_argv
                    or "git",
                    "ls-remote",
                    "origin",
                    public_input.get("ref", "refs/heads/main"),
                ],
                "exit_code": 0,
                "stdout_sha256": gtt.digest_text(""),
                "stderr_sha256": gtt.digest_text(""),
                "stdout_size_bytes": 0,
                "stderr_size_bytes": 0,
            }]
        )
        capability_status = (
            "passed"
            if status == "passed"
            else "failed"
            if status == "failed"
            else "blocked"
            if status == "blocked"
            else "not_run"
        )
        if status == "passed":
            example = json.loads(
                (self.PACKAGE / "examples/execution-facts.json").read_text(
                    encoding="utf-8"
                )
            )
            asset_expectations = copy.deepcopy(example["asset_expectations"])
            asset_digests = copy.deepcopy(example["asset_digests"])
            asset_inventory = copy.deepcopy(example["asset_inventory"])
        else:
            asset_expectations = []
            asset_digests = []
            asset_inventory = gtt.extension_verification_asset_inventory_summary(
                [],
                [],
            )
        target_head = (
                None
                if status == "blocked" and public_input["mode"] == "standalone"
                else branch_review_commit or "a" * 40
            )
        target_repository = {
            "repo_ref": public_input["repo_ref"],
            "remote": public_input.get("remote", "origin"),
            "ref": public_input.get("ref", "refs/heads/main"),
            "branch_review_commit": branch_review_commit,
            "publication_head": (
                public_input["publication_head"]
                if public_input["mode"] == "workflow"
                else None
            ),
            "resolved_head": target_head,
            "checkout_head": target_head,
            "reviewed_content_sha256": reviewed_content_sha256,
            "remote_reviewed_content_sha256": remote_reviewed_content_sha256,
            "content_identity_matches": status == "passed",
        }
        source_commit = "b" * 40 if "task_ref" in public_input else target_head
        extension_source = {
            "selection": "manifest" if "task_ref" in public_input else "standalone_fallback",
            "manifest_provenance": "available" if "task_ref" in public_input else "not_available",
            "repo": "example/guru-extension",
            "locator": "https://github.com/example/guru-extension.git",
            "requested_ref": "refs/heads/main",
            "resolved_ref": "refs/heads/main",
            "direct_oid": source_commit,
            "commit": source_commit,
            "checkout_head": source_commit if status == "passed" else None,
            "tree_state": "clean",
            "is_mutable_ref": True,
            "ref_matches_commit": status == "passed",
            "checkout_head_matches": status == "passed",
        }
        return {
            "schema_version": "3.0",
            "target_repository": target_repository,
            "extension_source": extension_source,
            "status": status,
            "commands": commands,
            "capabilities": gtt.extension_verification_capability_facts(
                selected,
                capability_status,
                commands,
                asset_digests,
            ),
            "asset_expectations": asset_expectations,
            "asset_digests": asset_digests,
            "asset_inventory": asset_inventory,
            "ownership": {
                "checkout_owner": "extension_source_checkout",
                "current_contract": True,
                "schema_version": "3.0",
                "inventory_id": "guru-team-upstream-ownership",
                "guru_owned_rule_count": 11,
                "managed_claim_count": 9,
            },
            "sidecars": {
                "checkout_owner": "extension_source_checkout",
                "paths": [],
            },
        }

    def materialize_installed_asset_target(
        self,
        source: Path,
        installed: Path,
    ) -> list[dict[str, Any]]:
        return materialize_extension_verification_installed_asset_target(
            source,
            installed,
        )

    def copy_extension_source_fixture(self, destination: Path) -> None:
        copy_extension_verification_source_fixture(destination)

    def review(
        self,
        typed_exit: str,
        selected: list[str],
        *,
        supersedes: str | None = None,
        applicability_status: str | None = None,
    ) -> dict[str, Any]:
        finding = {
            "finding_ref": "extension-finding-001",
            "evidence": "The selected extension capability requires follow-up.",
            "route_class": (
                "task_work"
                if typed_exit == "return_to_task_work"
                else "external_blocker"
            ),
            "status": "open",
            "closure_evidence": "",
        }
        payload: dict[str, Any] = {
            "applicability": {
                "status": (
                    applicability_status
                    if applicability_status is not None
                    else "not_required"
                    if typed_exit == "not_required"
                    else "required"
                ),
                "reason": "The semantic owner reviewed the current extension surface.",
                "evidence_paths": ["trellis/skills/guru-team/registry.json"],
            },
            "verification_profile": {
                "selected_capabilities": selected,
                "selection_reason": "The closed profile covers the reviewed surface.",
                "coverage": [
                    f"surface -> {capability}" for capability in selected
                ],
            },
            "semantic_review": {
                "adequacy": [{
                    "id": "profile_coverage",
                    "status": (
                        "passed"
                        if typed_exit == "verified"
                        else "not_applicable"
                        if typed_exit == "not_required"
                        else "failed"
                        if typed_exit == "return_to_task_work"
                        else "blocked"
                    ),
                    "evidence_refs": ["execution:0"],
                }],
                "findings": (
                    [finding]
                    if typed_exit in {"return_to_task_work", "blocked"}
                    else []
                ),
                "conclusion": typed_exit,
            },
            "typed_exit": typed_exit,
            "redaction": {
                "status": "passed",
                "scanned_surfaces": ["artifact", "wrapper_stdout"],
            },
        }
        if typed_exit == "blocked":
            payload.update({
                "reason_code": "remote_unavailable",
                "remediation": "Restore remote access and retry.",
            })
        if supersedes is not None:
            payload["supersedes_verification_ref"] = supersedes
        return payload

    def record(
        self,
        public_input: dict[str, Any],
        execution: dict[str, Any],
        review: dict[str, Any],
    ) -> dict[str, Any]:
        runtime_dir = self.root / ".trellis/.runtime/guru-team/tests"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        input_path = runtime_dir / "public-input.json"
        execution_path = runtime_dir / "execution.json"
        review_path = runtime_dir / "review.json"
        gtt.write_json(input_path, public_input)
        gtt.write_json(execution_path, execution)
        gtt.write_json(review_path, review)
        return gtt.cmd_record_extension_verification(argparse.Namespace(
            root=str(self.root),
            input=input_path.relative_to(self.root).as_posix(),
            execution_input=execution_path.relative_to(self.root).as_posix(),
            review_input=review_path.relative_to(self.root).as_posix(),
        ))

    def test_record_validates_published_nested_input_schemas_before_use(self) -> None:
        public_input = self.public_input("workflow", task=True)
        selected = ["marketplace_index"]
        malformed_marker = "synthetic-sensitive-nested-value"

        malformed_review = self.review("verified", selected)
        malformed_review["redaction"] = malformed_marker
        with self.assertRaises(gtt.WorkflowError) as review_error:
            self.record(
                public_input,
                self.execution(public_input, "passed", selected),
                malformed_review,
            )
        review_public_error = json.dumps(
            {
                "status": "error",
                "error": str(review_error.exception),
                **review_error.exception.payload,
            }
        )
        self.assertIn("semantic review input failed schema validation", review_public_error)
        self.assertNotIn(malformed_marker, review_public_error)
        self.assertFalse(
            (self.task_dir / "marketplace-verification.json").exists()
        )

        malformed_execution = self.execution(
            public_input,
            "passed",
            selected,
        )
        malformed_execution["capabilities"] = None
        with self.assertRaises(gtt.WorkflowError) as execution_error:
            self.record(
                public_input,
                malformed_execution,
                self.review("verified", selected),
            )
        self.assertIn(
            "execution facts failed schema validation",
            str(execution_error.exception),
        )
        self.assertFalse(
            (self.task_dir / "marketplace-verification.json").exists()
        )

        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(
                sys,
                "argv",
                [
                    "guru_team_trellis.py",
                    "record-extension-verification",
                    "--root",
                    str(self.root),
                    "--input",
                    ".trellis/.runtime/guru-team/tests/public-input.json",
                    "--execution-input",
                    ".trellis/.runtime/guru-team/tests/execution.json",
                    "--review-input",
                    ".trellis/.runtime/guru-team/tests/review.json",
                    "--json",
                ],
            ),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            return_code = gtt.main()
        public_streams = stdout.getvalue() + stderr.getvalue()
        self.assertEqual(return_code, 2)
        self.assertNotIn("Traceback", public_streams)

    def test_workflow_public_input_rejects_legacy_missing_publication_head(self) -> None:
        public_input = self.public_input("workflow", task=True)
        del public_input["publication_head"]
        runtime_dir = self.root / ".trellis/.runtime/guru-team/tests"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        input_path = runtime_dir / "legacy-public-input.json"
        gtt.write_json(input_path, public_input)

        with self.assertRaises(gtt.WorkflowError) as rejected:
            gtt.extension_verification_public_input(
                self.root,
                input_path.relative_to(self.root).as_posix(),
            )
        self.assertIn(
            "public input failed validation",
            str(rejected.exception),
        )

    def test_workflow_docs_reject_legacy_publication_head_fallback(self) -> None:
        source_root = Path(__file__).resolve().parents[5]
        contract = (
            source_root / ".trellis/spec/workflow/companion-scripts.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "a legacy payload without `publication_head` fails current-schema",
            contract,
        )
        self.assertIn("never defaults or derives the missing identity", contract)
        self.assertNotIn(
            "inputs without `publication_head` normalize to `branch_review_commit`",
            contract,
        )

    def test_record_schema_validation_rejects_missing_and_invalid_enums(self) -> None:
        public_input = self.public_input("workflow", task=True)
        selected = ["marketplace_index"]

        missing_exit = self.review("verified", selected)
        del missing_exit["typed_exit"]
        with self.assertRaises(gtt.WorkflowError) as missing_error:
            self.record(
                public_input,
                self.execution(public_input, "passed", selected),
                missing_exit,
            )
        self.assertIn(
            "semantic review input failed schema validation",
            str(missing_error.exception),
        )

        invalid_exit = self.review("verified", selected)
        invalid_exit["typed_exit"] = "success"
        with self.assertRaises(gtt.WorkflowError) as invalid_review_error:
            self.record(
                public_input,
                self.execution(public_input, "passed", selected),
                invalid_exit,
            )
        self.assertIn(
            "semantic review input failed schema validation",
            str(invalid_review_error.exception),
        )

        invalid_execution = self.execution(
            public_input,
            "passed",
            selected,
        )
        invalid_execution["status"] = "success"
        with self.assertRaises(gtt.WorkflowError) as invalid_execution_error:
            self.record(
                public_input,
                invalid_execution,
                self.review("verified", selected),
            )
        self.assertIn(
            "execution facts failed schema validation",
            str(invalid_execution_error.exception),
        )
        self.assertFalse(
            (self.task_dir / "marketplace-verification.json").exists()
        )

    def test_supersession_requires_existing_exact_prior_owner(self) -> None:
        public_input = self.public_input("workflow", task=True)
        selected = ["marketplace_index"]

        with self.assertRaises(gtt.WorkflowError) as no_prior:
            self.record(
                public_input,
                self.execution(public_input, "blocked", selected),
                self.review(
                    "blocked",
                    selected,
                    supersedes="extension-verification:does-not-exist",
                ),
            )
        self.assertIn("requires an existing prior owner result", str(no_prior.exception))
        self.assertFalse(
            (self.task_dir / "marketplace-verification.json").exists()
        )

        prior = self.record(
            public_input,
            self.execution(public_input, "blocked", selected),
            self.review("blocked", selected),
        )
        prior_ref = prior["identity"]["verification_ref"]
        with self.assertRaises(gtt.WorkflowError) as wrong_prior:
            self.record(
                public_input,
                self.execution(public_input, "passed", selected),
                self.review(
                    "verified",
                    selected,
                    supersedes="extension-verification:not-the-prior",
                ),
            )
        self.assertIn("exact prior verification_ref", str(wrong_prior.exception))

        current = self.record(
            public_input,
            self.execution(public_input, "passed", selected),
            self.review("verified", selected, supersedes=prior_ref),
        )
        self.assertEqual(
            current["freshness"]["supersedes_verification_ref"],
            prior_ref,
        )

    def test_supersession_allows_changed_plan_with_exact_prior_owner(self) -> None:
        prior_input = self.public_input(
            "workflow",
            task=True,
            plan_ref="closeout-plan:prior",
        )
        selected = ["marketplace_index"]
        prior = self.record(
            prior_input,
            self.execution(prior_input, "blocked", selected),
            self.review("blocked", selected),
        )
        prior_ref = prior["identity"]["verification_ref"]

        current_input = self.public_input(
            "workflow",
            task=True,
            plan_ref="closeout-plan:current",
        )
        current = self.record(
            current_input,
            self.execution(current_input, "passed", selected),
            self.review("verified", selected, supersedes=prior_ref),
        )

        self.assertEqual(
            current["freshness"]["supersedes_verification_ref"],
            prior_ref,
        )
        self.assertEqual(
            current["public_input"]["plan_ref"],
            "closeout-plan:current",
        )

    def test_taskless_standalone_is_session_only(self) -> None:
        public_input = self.public_input("standalone", task=False)
        owner = self.record(
            public_input,
            self.execution(public_input, "not_run", []),
            self.review("not_required", []),
        )

        self.assertEqual(owner["consumer"], {"kind": "session", "id": "direct-caller"})
        self.assertEqual(list(self.root.rglob("marketplace-verification.json")), [])
        with mock.patch.object(
            gtt,
            "run",
            return_value=mock.Mock(
                returncode=0,
                stdout=f"{'a' * 40}\trefs/heads/main\n",
                stderr="",
            ),
        ):
            checked = gtt.check_extension_verification_result(
                self.root,
                owner,
                "<stdin>",
                public_input,
            )
        self.assertEqual(checked["typed_exit"], "not_required")

    def test_checker_and_public_projection_use_annotated_tag_commit(
        self,
    ) -> None:
        public_input = self.public_input("standalone", task=False)
        public_input["ref"] = "refs/tags/v0.6.5-annotated"
        direct_tag_object = "b" * 40
        resolved_commit = "a" * 40
        execution = self.execution(public_input, "not_run", [])
        execution["target_repository"]["resolved_head"] = resolved_commit
        execution["target_repository"]["checkout_head"] = resolved_commit
        execution["extension_source"].update({
            "requested_ref": public_input["ref"],
            "resolved_ref": public_input["ref"],
            "direct_oid": direct_tag_object,
            "commit": resolved_commit,
        })
        owner = self.record(
            public_input,
            execution,
            self.review("not_required", []),
        )
        self.assertEqual(
            owner["target_repository"]["resolved_head"],
            resolved_commit,
        )

        remote_result = mock.Mock(
            returncode=0,
            stdout=(
                f"{direct_tag_object}\t{public_input['ref']}\n"
                f"{resolved_commit}\t{public_input['ref']}^{{}}\n"
            ),
            stderr="",
        )
        with mock.patch.object(gtt, "run", return_value=remote_result):
            checked = gtt.check_extension_verification_result(
                self.root,
                owner,
                "<stdin>",
                public_input,
            )
            with mock.patch.object(
                sys,
                "stdin",
                io.StringIO(json.dumps(owner)),
            ):
                output = gtt.cmd_invoke_extension_verification(
                    argparse.Namespace(
                        root=str(self.root),
                        input=(
                            ".trellis/.runtime/guru-team/tests/"
                            "public-input.json"
                        ),
                        owner_result="-",
                    )
                )

        self.assertEqual(checked["typed_exit"], "not_required")
        self.assertEqual(output["resolved_head"], resolved_commit)
        self.assertNotIn(direct_tag_object, json.dumps(output))

    def test_checker_rejects_installed_manifest_commit_drift(self) -> None:
        public_input = self.public_input("workflow", task=True)
        selected = ["marketplace_index"]
        owner = self.record(
            public_input,
            self.execution(public_input, "passed", selected),
            self.review("verified", selected),
        )
        live_source = {
            "selection": "manifest",
            "manifest_provenance": "available",
            "repo": "example/guru-extension",
            "locator": "https://github.com/example/guru-extension.git",
            "requested_ref": "refs/heads/main",
            "manifest_commit": "c" * 40,
            "tree_state": "clean",
            "is_mutable_ref": True,
        }
        real_run = gtt.run

        def current_ref_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> Any:
            if command[:2] == ["git", "ls-remote"]:
                oid = self.head if command[2] == "origin" else "b" * 40
                return mock.Mock(
                    returncode=0,
                    stdout=f"{oid}\trefs/heads/main\n",
                    stderr="",
                )
            return real_run(command, cwd=cwd, check=check, env=env)

        with (
            mock.patch.object(gtt, "run", side_effect=current_ref_run),
            mock.patch.object(
                gtt,
                "extension_verification_reviewed_content_sha256",
                return_value=owner["target_repository"][
                    "reviewed_content_sha256"
                ],
            ),
            mock.patch.object(
                gtt,
                "extension_verification_manifest_source",
                return_value=live_source,
            ),
            self.assertRaises(gtt.WorkflowError) as stale,
        ):
            gtt.check_extension_verification_result(
                self.root,
                owner,
                ".trellis/tasks/current/marketplace-verification.json",
                public_input,
            )
        self.assertIn(
            "installed extension manifest provenance is stale",
            json.dumps(stale.exception.payload),
        )

    def test_taskless_remote_unavailable_emits_blocked_without_fake_head(self) -> None:
        public_input = self.public_input("standalone", task=False)
        public_input["remote"] = "missing-remote"
        selected = ["marketplace_index"]
        execution = gtt.extension_verification_execute_facts(
            self.root,
            public_input,
            selected,
        )
        self.assertEqual(execution["status"], "blocked")
        self.assertIsNone(execution["target_repository"]["resolved_head"])
        owner = self.record(
            public_input,
            execution,
            self.review("blocked", selected),
        )

        checked = gtt.check_extension_verification_result(
            self.root,
            owner,
            "<stdin>",
            public_input,
        )
        self.assertEqual(checked["typed_exit"], "blocked")
        input_path = (
            ".trellis/.runtime/guru-team/tests/public-input.json"
        )
        with mock.patch.object(sys, "stdin", io.StringIO(json.dumps(owner))):
            output = gtt.cmd_invoke_extension_verification(
                argparse.Namespace(
                    root=str(self.root),
                    input=input_path,
                    owner_result="-",
                )
            )
        self.assertEqual(
            output,
            {
                "exit_id": "blocked",
                "mode": "standalone",
                "repo_ref": "example/guru-extension",
                "reason_code": "remote_unavailable",
                "remediation": "Restore remote access and retry.",
            },
        )

    def test_exit_zero_does_not_override_failed_adequacy(self) -> None:
        public_input = self.public_input("standalone", task=True)
        selected = ["marketplace_index"]
        owner = self.record(
            public_input,
            self.execution(public_input, "passed", selected),
            self.review("return_to_task_work", selected),
        )

        self.assertEqual(owner["typed_exit"], "return_to_task_work")
        self.assertEqual(owner["execution"]["commands"][0]["exit_code"], 0)
        self.assertEqual(
            owner["semantic_review"]["adequacy"][0]["status"],
            "failed",
        )

    def test_workflow_applicability_conflict_blocks_without_execution(self) -> None:
        public_input = self.public_input("workflow", task=True)
        review = self.review(
            "blocked",
            [],
            applicability_status="not_required",
        )
        review["reason_code"] = "applicability_conflict"
        review["remediation"] = (
            "Reconcile the reviewed applicability with the required workflow plan."
        )
        owner = self.record(
            public_input,
            self.execution(public_input, "not_run", []),
            review,
        )

        self.assertEqual(owner["typed_exit"], "blocked")
        self.assertEqual(owner["applicability"]["status"], "not_required")
        self.assertEqual(owner["execution"]["status"], "not_run")
        self.assertEqual(owner["verification_profile"]["selected_capabilities"], [])
        self.assertEqual(
            owner["blocker"]["reason_code"],
            "applicability_conflict",
        )

    def test_credential_userinfo_redaction_covers_normal_url_shapes(self) -> None:
        credential_urls = [
            "https://@example.invalid/repo.git",
            "https://s@example.invalid/repo.git",
            "https://user@example.invalid/repo.git",
            "https://user:secret@example.invalid/repo.git",
            "https://user@team@example.invalid/repo.git",
            "https://user%40team:pa%3Ass@example.invalid/repo.git",
            "prefix https://user:secret@example.invalid/repo.git suffix",
            "before\nhttps://user:secret@example.invalid/repo.git\nafter",
        ]
        for value in credential_urls:
            with self.subTest(value=value):
                self.assertTrue(gtt.extension_verification_sensitive_text(value))
        for value in [
            "https://example.invalid/repo.git",
            "https://user name@example.invalid/repo.git",
            "https://example.invalid/path@segment",
        ]:
            with self.subTest(value=value):
                self.assertFalse(gtt.extension_verification_sensitive_text(value))

    def test_sensitive_command_fails_closed_without_artifact_or_public_error_leak(
        self,
    ) -> None:
        public_input = self.public_input("standalone", task=True)
        selected = ["redaction"]
        for credential_url in [
            "https://s@example.invalid/repo.git",
            "https://user:secret@example.invalid/repo.git",
            "https://user@team@example.invalid/repo.git",
        ]:
            with self.subTest(credential_url=credential_url):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    self.record(
                        public_input,
                        self.execution(
                            public_input,
                            "passed",
                            selected,
                            sensitive_argv=credential_url,
                        ),
                        self.review("verified", selected),
                    )
                public_error = json.dumps(
                    {
                        "status": "error",
                        "error": str(raised.exception),
                        **raised.exception.payload,
                    }
                )
                self.assertIn("unredacted sensitive material", public_error)
                self.assertNotIn(credential_url, public_error)
                self.assertFalse(
                    (self.task_dir / "marketplace-verification.json").exists()
                )
                stdout = io.StringIO()
                stderr = io.StringIO()
                with (
                    mock.patch.object(
                        sys,
                        "argv",
                        [
                            "guru_team_trellis.py",
                            "record-extension-verification",
                            "--root",
                            str(self.root),
                            "--input",
                            ".trellis/.runtime/guru-team/tests/public-input.json",
                            "--execution-input",
                            ".trellis/.runtime/guru-team/tests/execution.json",
                            "--review-input",
                            ".trellis/.runtime/guru-team/tests/review.json",
                            "--json",
                        ],
                    ),
                    contextlib.redirect_stdout(stdout),
                    contextlib.redirect_stderr(stderr),
                ):
                    return_code = gtt.main()
                public_streams = stdout.getvalue() + stderr.getvalue()
                self.assertEqual(return_code, 2)
                self.assertNotIn(credential_url, public_streams)
                self.assertIn("unredacted sensitive material", public_streams)

    def test_record_rejects_wrong_active_task(self) -> None:
        public_input = self.public_input("workflow", task=True)
        public_input["task_ref"] = ".trellis/tasks/other"
        other = self.root / ".trellis/tasks/other"
        other.mkdir()
        gtt.write_json(
            other / "task.json",
            {
                "id": "other",
                "name": "other",
                "title": "Other",
                "status": "in_progress",
                "branch": "main",
                "base_branch": "main",
            },
        )
        gtt.write_runtime_mappings(
            self.root,
            gtt.load_config(self.root),
            {
                "workspace_slug": "other",
                "task_slug": "other",
                "task_dir": ".trellis/tasks/other",
                "branch_name": "main",
            },
            self.root,
        )
        with self.assertRaises(gtt.WorkflowError) as raised:
            self.record(
                public_input,
                self.execution(public_input, "passed", ["marketplace_index"]),
                self.review("verified", ["marketplace_index"]),
            )
        self.assertIn(
            "current active Trellis task",
            json.dumps(raised.exception.payload),
        )
        self.assertFalse((other / "marketplace-verification.json").exists())

    def test_check_rejects_archived_task(self) -> None:
        public_input = self.public_input("standalone", task=True)
        public_input["task_ref"] = ".trellis/tasks/archive/2026-07/archived"
        archived = self.root / public_input["task_ref"]
        archived.mkdir(parents=True)
        gtt.write_json(
            archived / "task.json",
            {
                "id": "archived",
                "name": "archived",
                "title": "Archived",
                "status": "completed",
                "branch": "main",
                "base_branch": "main",
            },
        )
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.check_extension_verification_result(
                self.root,
                {},
                f"{public_input['task_ref']}/marketplace-verification.json",
                public_input,
            )
        self.assertIn(
            "direct active task",
            json.dumps(raised.exception.payload),
        )

    def test_execute_rejects_wrong_worktree_mapping(self) -> None:
        public_input = self.public_input("workflow", task=True)
        wrong_workspace = self.root.parent / f"{self.root.name}-other-worktree"
        wrong_workspace.mkdir()
        self.addCleanup(shutil.rmtree, wrong_workspace, True)
        gtt.write_json(
            gtt.runtime_workspace_path(
                self.root,
                gtt.load_config(self.root),
                "current",
            ),
            {
                "schema_version": "1.0",
                "workspace_slug": "current",
                "workspace_path": str(wrong_workspace),
                "source_checkout": str(self.root),
                "branch_name": "main",
                "updated_at": gtt.now_iso(),
            },
        )
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.extension_verification_execute_facts(
                self.root,
                public_input,
                ["marketplace_index"],
            )
        self.assertIn(
            "workspaces/current.json",
            json.dumps(raised.exception.payload),
        )

    def test_same_identity_retry_requires_exact_supersession(self) -> None:
        public_input = self.public_input("workflow", task=True)
        selected = ["marketplace_index"]
        prior = self.record(
            public_input,
            self.execution(public_input, "blocked", selected),
            self.review("blocked", selected),
        )
        prior_ref = prior["identity"]["verification_ref"]

        with self.assertRaises(gtt.WorkflowError):
            self.record(
                public_input,
                self.execution(public_input, "passed", selected),
                self.review("verified", selected),
            )
        current = self.record(
            public_input,
            self.execution(public_input, "passed", selected),
            self.review("verified", selected, supersedes=prior_ref),
        )
        self.assertEqual(
            current["freshness"]["supersedes_verification_ref"],
            prior_ref,
        )
        self.assertNotEqual(current["identity"]["verification_ref"], prior_ref)

    def test_checker_rejects_local_and_remote_head_drift(self) -> None:
        workflow_input = self.public_input("workflow", task=True)
        selected = ["marketplace_index"]
        workflow_owner = self.record(
            workflow_input,
            self.execution(workflow_input, "passed", selected),
            self.review("verified", selected),
        )
        (self.root / "drift.txt").write_text("drift\n", encoding="utf-8")
        subprocess.run(["git", "add", "drift.txt"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-qm", "drift"],
            cwd=self.root,
            check=True,
        )
        real_run = gtt.run

        def local_drift_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> Any:
            if command[:2] == ["git", "ls-remote"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{self.head}\trefs/heads/main\n",
                    stderr="",
                )
            return real_run(command, cwd=cwd, check=check, env=env)

        with (
            mock.patch.object(gtt, "run", side_effect=local_drift_run),
            self.assertRaises(gtt.WorkflowError) as local_drift,
        ):
            gtt.check_extension_verification_result(
                self.root,
                workflow_owner,
                ".trellis/tasks/current/marketplace-verification.json",
                workflow_input,
            )
        self.assertIn(
            "reviewed-content drift",
            json.dumps(local_drift.exception.payload),
        )

        standalone_input = self.public_input("standalone", task=False)
        standalone_owner = self.record(
            standalone_input,
            self.execution(standalone_input, "not_run", []),
            self.review("not_required", []),
        )
        def remote_drift_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> Any:
            if command[:2] == ["git", "ls-remote"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{'b' * 40}\trefs/heads/main\n",
                    stderr="",
                )
            return real_run(command, cwd=cwd, check=check, env=env)

        with (
            mock.patch.object(gtt, "run", side_effect=remote_drift_run),
            self.assertRaises(gtt.WorkflowError) as remote_drift,
        ):
            gtt.check_extension_verification_result(
                self.root,
                standalone_owner,
                "<stdin>",
                standalone_input,
            )
        self.assertIn(
            "remote ref HEAD",
            json.dumps(remote_drift.exception.payload),
        )

    def test_task_modes_reject_same_head_tracked_content_drift(self) -> None:
        for mode in ("workflow", "standalone"):
            with self.subTest(mode=mode):
                (self.task_dir / "marketplace-verification.json").unlink(
                    missing_ok=True
                )
                public_input = self.public_input(mode, task=True)
                selected = ["marketplace_index"]
                readme = self.root / "README.md"
                readme.write_text("reviewed dirty content\n", encoding="utf-8")
                owner = self.record(
                    public_input,
                    self.execution(public_input, "passed", selected),
                    self.review("verified", selected),
                )
                recorded_binding = owner["target_repository"]["reviewed_content_sha256"]
                self.assertRegex(recorded_binding, r"^[0-9a-f]{64}$")

                readme.write_text("later dirty content\n", encoding="utf-8")
                remote_head = (
                    self.head if mode == "workflow" else "a" * 40
                )
                real_run = gtt.run

                def drift_run(
                    command: list[str],
                    cwd: Path | None = None,
                    check: bool = True,
                    env: dict[str, str] | None = None,
                ) -> Any:
                    if command[:2] == ["git", "ls-remote"]:
                        return mock.Mock(
                            returncode=0,
                            stdout=f"{remote_head}\trefs/heads/main\n",
                            stderr="",
                        )
                    return real_run(command, cwd=cwd, check=check, env=env)

                with (
                    mock.patch.object(gtt, "run", side_effect=drift_run),
                    self.assertRaises(gtt.WorkflowError) as drift,
                ):
                    gtt.check_extension_verification_result(
                        self.root,
                        owner,
                        ".trellis/tasks/current/marketplace-verification.json",
                        public_input,
                    )
                self.assertIn(
                    "reviewed-content drift",
                    json.dumps(drift.exception.payload),
                )
                readme.write_text("fixture\n", encoding="utf-8")
                (
                    self.task_dir / "marketplace-verification.json"
                ).unlink(missing_ok=True)

    def test_taskless_return_to_task_work_is_rejected(self) -> None:
        public_input = self.public_input("standalone", task=False)
        selected = ["marketplace_index"]
        with self.assertRaises(gtt.WorkflowError) as raised:
            self.record(
                public_input,
                self.execution(public_input, "failed", selected),
                self.review("return_to_task_work", selected),
            )
        self.assertIn(
            "taskless standalone",
            json.dumps(raised.exception.payload),
        )

    def test_current_ownership_inventory_reports_current_claim_counts(self) -> None:
        canonical = (
            Path(__file__).resolve().parents[5]
            / "trellis/presets/guru-team/ownership/upstream-ownership.json"
        )
        facts = gtt.extension_verification_ownership_facts(canonical)
        self.assertEqual(
            facts,
            {
                "checkout_owner": "extension_source_checkout",
                "current_contract": True,
                "schema_version": "3.0",
                "inventory_id": "guru-team-upstream-ownership",
                "guru_owned_rule_count": 11,
                "managed_claim_count": 9,
            },
        )

    def test_verified_rejects_ownership_facts_outside_current_contract(self) -> None:
        public_input = self.public_input("workflow", task=True)
        selected = ["ownership_inventory"]
        execution = self.execution(public_input, "passed", selected)
        execution["ownership"]["current_contract"] = False
        with self.assertRaises(gtt.WorkflowError) as raised:
            self.record(
                public_input,
                execution,
                self.review("verified", selected),
            )
        self.assertIn(
            "current ownership contract",
            json.dumps(raised.exception.payload),
        )

    def test_verified_rejects_cross_owned_source_command(self) -> None:
        public_input = self.public_input("workflow", task=True)
        selected = ["marketplace_index"]
        execution = self.execution(public_input, "passed", selected)
        execution["commands"][0]["checkout_owner"] = "target_checkout"
        with self.assertRaises(gtt.WorkflowError) as raised:
            self.record(
                public_input,
                execution,
                self.review("verified", selected),
            )
        self.assertIn(
            "extension_source_checkout",
            json.dumps(raised.exception.payload),
        )

    def test_installed_asset_inventory_covers_expected_categories_and_relations(
        self,
    ) -> None:
        source = Path(__file__).resolve().parents[5]
        installed = self.root / "installed-assets"
        expectations = self.materialize_installed_asset_target(
            source,
            installed,
        )
        observed_expectations, digests, inventory = (
            gtt.extension_verification_installed_asset_facts(
                source,
                installed,
            )
        )

        self.assertEqual(observed_expectations, expectations)
        self.assertTrue(inventory["complete"])
        self.assertEqual(inventory["expected_count"], len(expectations))
        self.assertEqual(inventory["observed_count"], len(digests))
        self.assertEqual(inventory["matched_count"], len(expectations))
        self.assertEqual(
            {item["id"] for item in inventory["categories"]},
            {"workflow", "preset", "schema", "skill", "platform"},
        )
        self.assertTrue(all(item["complete"] for item in inventory["categories"]))
        self.assertEqual(
            {item["platform"] for item in expectations if item["category"] == "platform"},
            {"shared", "codex", "claude", "cursor"},
        )
        self.assertTrue(
            all(
                item["path"].startswith((".",))
                and not Path(item["path"]).is_absolute()
                for item in digests
            )
        )

    def test_installed_asset_inventory_fails_closed_for_mismatch_missing_and_duplicate(
        self,
    ) -> None:
        source = Path(__file__).resolve().parents[5]
        installed = self.root / "installed-assets"
        expectations = self.materialize_installed_asset_target(
            source,
            installed,
        )
        platform_path = next(
            item["path"]
            for item in expectations
            if item["category"] == "platform"
            and item["platform"] == "codex"
        )
        (installed / platform_path).write_text("ordinary drift\n", encoding="utf-8")
        _, _, mismatch = gtt.extension_verification_installed_asset_facts(
            source,
            installed,
        )
        self.assertFalse(mismatch["complete"])
        self.assertIn(platform_path, mismatch["mismatched_paths"])

        schema_path = next(
            item["path"]
            for item in expectations
            if item["category"] == "schema"
        )
        (installed / schema_path).unlink()
        _, _, missing = gtt.extension_verification_installed_asset_facts(
            source,
            installed,
        )
        self.assertFalse(missing["complete"])
        self.assertIn(schema_path, missing["missing_paths"])

        manifest_path = installed / ".trellis/guru-team/extension.json"
        manifest = gtt.read_json(manifest_path)
        duplicate_record = copy.deepcopy(manifest["skill_packages"]["files"][0])
        manifest["skill_packages"]["files"].append(duplicate_record)
        gtt.write_json(manifest_path, manifest)
        _, _, duplicate = gtt.extension_verification_installed_asset_facts(
            source,
            installed,
        )
        self.assertFalse(duplicate["complete"])
        self.assertIn(duplicate_record["path"], duplicate["duplicate_paths"])

    def test_verified_rejects_incomplete_inventory_and_capability_evidence(
        self,
    ) -> None:
        public_input = self.public_input("workflow", task=True)
        selected = ["marketplace_index"]

        incomplete = self.execution(public_input, "passed", selected)
        missing_path = incomplete["asset_digests"].pop(0)["path"]
        incomplete["asset_inventory"] = (
            gtt.extension_verification_asset_inventory_summary(
                incomplete["asset_expectations"],
                incomplete["asset_digests"],
            )
        )
        with self.assertRaises(gtt.WorkflowError) as missing_error:
            self.record(
                public_input,
                incomplete,
                self.review("verified", selected),
            )
        self.assertIn(
            "complete matching installed asset inventory",
            json.dumps(missing_error.exception.payload),
        )
        self.assertIn(
            missing_path,
            incomplete["asset_inventory"]["missing_paths"],
        )

        for fault in ("mismatch", "duplicate"):
            with self.subTest(fault=fault):
                invalid = self.execution(public_input, "passed", selected)
                if fault == "mismatch":
                    invalid["asset_digests"][0]["sha256"] = "f" * 64
                else:
                    duplicate = copy.deepcopy(invalid["asset_expectations"][0])
                    duplicate["relation"] = "managed_manifest"
                    invalid["asset_expectations"].append(duplicate)
                invalid["asset_inventory"] = (
                    gtt.extension_verification_asset_inventory_summary(
                        invalid["asset_expectations"],
                        invalid["asset_digests"],
                    )
                )
                with self.assertRaises(gtt.WorkflowError) as invalid_error:
                    self.record(
                        public_input,
                        invalid,
                        self.review("verified", selected),
                    )
                self.assertIn(
                    "complete matching installed asset inventory",
                    json.dumps(invalid_error.exception.payload),
                )

        unbound = self.execution(public_input, "passed", selected)
        unbound["capabilities"][0]["command_refs"] = []
        unbound["capabilities"][0]["asset_paths"] = []
        with self.assertRaises(gtt.WorkflowError) as capability_error:
            self.record(
                public_input,
                unbound,
                self.review("verified", selected),
            )
        self.assertIn(
            "requires command and installed asset evidence",
            json.dumps(capability_error.exception.payload),
        )

    def test_executor_collects_installed_target_and_binds_each_capability(
        self,
    ) -> None:
        public_input = self.public_input("standalone", task=False)
        remote_head = "b" * 40
        selected = list(gtt.EXTENSION_VERIFICATION_CAPABILITIES)

        def fake_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> mock.Mock:
            if command[:2] == ["git", "ls-remote"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{remote_head}\trefs/heads/main\n",
                    stderr="",
                )
            if command[:3] == ["git", "remote", "get-url"]:
                return mock.Mock(
                    returncode=0,
                    stdout="https://github.com/example/guru-extension.git\n",
                    stderr="",
                )
            if command[:2] == ["git", "clone"]:
                self.copy_extension_source_fixture(Path(command[-1]))
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "checkout", "--detach"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "rev-parse", "--verify"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{remote_head}\n",
                    stderr="",
                )
            self.assertEqual(len(command), 2)
            install_work = Path(command[1])
            self.materialize_installed_asset_target(
                Path(cwd),
                install_work / "project",
            )
            return mock.Mock(returncode=0, stdout="", stderr="")

        with (
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={
                    "algorithm": "guru-reviewed-content-1.0",
                    "sha256": "c" * 64,
                },
            ),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
        ):
            facts = gtt.extension_verification_execute_facts(
                self.root,
                public_input,
                selected,
                expected_branch_review_commit=remote_head,
            )

        self.assertEqual(facts["status"], "passed", facts)
        self.assertTrue(facts["asset_inventory"]["complete"])
        self.assertEqual(
            {item["category"] for item in facts["asset_digests"]},
            {"workflow", "preset", "schema", "skill", "platform"},
        )
        self.assertEqual(
            [item["id"] for item in facts["capabilities"]],
            selected,
        )
        for capability in facts["capabilities"]:
            self.assertEqual(capability["status"], "passed")
            self.assertTrue(capability["command_refs"])
            self.assertTrue(capability["asset_paths"])
        self.assertEqual(
            facts["commands"][-1]["argv"][-1],
            "<temp-install-work>",
        )

    def test_task_bearing_executor_with_deinitialized_gitlink_reaches_throwaway(
        self,
    ) -> None:
        source_tmp = tempfile.TemporaryDirectory()
        self.addCleanup(source_tmp.cleanup)
        source = Path(source_tmp.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=source, check=True)
        subprocess.run(
            ["git", "config", "user.email", "gitlink@example.invalid"],
            cwd=source,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Gitlink Test"],
            cwd=source,
            check=True,
        )
        (source / "dependency.txt").write_text("dependency\n", encoding="utf-8")
        subprocess.run(["git", "add", "dependency.txt"], cwd=source, check=True)
        subprocess.run(["git", "commit", "-qm", "dependency"], cwd=source, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                "-q",
                str(source),
                "deps/dependency",
            ],
            cwd=self.root,
            check=True,
        )
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-qm", "add dependency gitlink"],
            cwd=self.root,
            check=True,
        )
        self.head = gtt.current_head(self.root)
        subprocess.run(
            ["git", "submodule", "deinit", "-f", "--", "deps/dependency"],
            cwd=self.root,
            check=True,
            stdout=subprocess.PIPE,
        )
        self.assertEqual(
            subprocess.run(
                ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
                cwd=self.root,
                check=True,
                stdout=subprocess.PIPE,
            ).stdout,
            b"",
        )
        expected_identity = gtt.reviewed_content_identity(self.root)["sha256"]
        public_input = self.public_input("workflow", task=True)
        clone_commands: list[list[str]] = []
        throwaway_commands: list[list[str]] = []
        source_commit = "b" * 40

        def fake_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> mock.Mock:
            del check, env
            if command[:3] == ["git", "rev-parse", "--abbrev-ref"]:
                return mock.Mock(returncode=0, stdout="main\n", stderr="")
            if command[:2] == ["git", "ls-remote"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{self.head}\trefs/heads/main\n",
                    stderr="",
                )
            if command[:3] == ["git", "remote", "get-url"]:
                return mock.Mock(
                    returncode=0,
                    stdout="https://github.com/example/guru-extension.git\n",
                    stderr="",
                )
            if command[:2] == ["git", "clone"]:
                clone_commands.append(command)
                destination = Path(command[-1])
                proc = subprocess.run(
                    ["git", "clone", "-q", "--no-checkout", str(self.root), str(destination)],
                    cwd=cwd,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                return mock.Mock(
                    returncode=proc.returncode,
                    stdout=proc.stdout,
                    stderr=proc.stderr,
                )
            if command[:3] == ["git", "checkout", "--detach"]:
                if Path(cwd).name == "target-checkout":
                    proc = subprocess.run(
                        command,
                        cwd=cwd,
                        check=False,
                        capture_output=True,
                        text=True,
                    )
                    return mock.Mock(
                        returncode=proc.returncode,
                        stdout=proc.stdout,
                        stderr=proc.stderr,
                    )
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "rev-parse", "--verify"]:
                head = self.head if Path(cwd).name == "target-checkout" else source_commit
                return mock.Mock(returncode=0, stdout=f"{head}\n", stderr="")
            if command and command[0].endswith("verify-throwaway-install.sh"):
                throwaway_commands.append(command)
                self.materialize_installed_asset_target(
                    Path(cwd),
                    Path(command[1]) / "project",
                )
                return mock.Mock(returncode=0, stdout="", stderr="")
            return mock.Mock(returncode=1, stdout="", stderr="unexpected command")

        def resolve_source(
            locator: str,
            requested_ref: str,
            checkout: Path,
        ) -> dict[str, Any]:
            self.assertEqual(locator, "https://github.com/example/guru-extension.git")
            self.assertEqual(requested_ref, "refs/heads/main")
            self.copy_extension_source_fixture(checkout)
            return {
                "status": "passed",
                "resolved_ref": source_commit,
                "direct_oid": source_commit,
                "commit": source_commit,
                "checkout_prepared": True,
                "commands": [],
            }

        with (
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(
                gtt,
                "extension_verification_task_identity",
                return_value=self.task_dir,
            ),
            mock.patch.object(
                gtt,
                "extension_verification_resolve_source_reference",
                side_effect=resolve_source,
            ),
        ):
            facts = gtt.extension_verification_execute_facts(
                self.root,
                public_input,
                ["marketplace_index"],
            )

        self.assertEqual(facts["status"], "passed", facts)
        self.assertEqual(
            facts["target_repository"]["reviewed_content_sha256"],
            expected_identity,
        )
        self.assertEqual(len(clone_commands), 1)
        self.assertEqual(clone_commands[0][:3], ["git", "clone", "--filter=blob:none"])
        command_ids = [item["id"] for item in facts["commands"]]
        self.assertIn("clone_target", command_ids)
        self.assertIn("verify_extension_source_checkout", command_ids)
        self.assertIn("verify_throwaway_installation", command_ids)
        self.assertEqual(len(throwaway_commands), 1)

    def test_executor_resolves_branch_lightweight_and_annotated_refs_to_commits(
        self,
    ) -> None:
        cases = (
            (
                "branch",
                "refs/heads/feature/117",
                "b" * 40,
                None,
            ),
            (
                "lightweight_tag",
                "refs/tags/v0.6.5-lightweight",
                "c" * 40,
                None,
            ),
            (
                "annotated_tag",
                "refs/tags/v0.6.5-annotated",
                "d" * 40,
                "e" * 40,
            ),
        )
        for label, ref, direct_head, peeled_head in cases:
            with self.subTest(label=label):
                public_input = self.public_input("standalone", task=False)
                public_input["ref"] = ref
                resolved_head = peeled_head or direct_head
                observed_commands: list[list[str]] = []
                observed_env: list[dict[str, str] | None] = []

                def fake_run(
                    command: list[str],
                    cwd: Path | None = None,
                    check: bool = True,
                    env: dict[str, str] | None = None,
                ) -> mock.Mock:
                    observed_commands.append(command)
                    if command[:2] == ["git", "ls-remote"]:
                        rows = [f"{direct_head}\t{ref}"]
                        if peeled_head is not None:
                            rows.append(f"{peeled_head}\t{ref}^{{}}")
                        return mock.Mock(
                            returncode=0,
                            stdout="\n".join(rows) + "\n",
                            stderr="",
                        )
                    if command[:3] == ["git", "remote", "get-url"]:
                        return mock.Mock(
                            returncode=0,
                            stdout=(
                                "https://github.com/example/"
                                "guru-extension.git\n"
                            ),
                            stderr="",
                        )
                    if command[:2] == ["git", "clone"]:
                        source = Path(command[-1])
                        throwaway = (
                            source
                            / "trellis/presets/guru-team/scripts/bash/"
                            "verify-throwaway-install.sh"
                        )
                        throwaway.parent.mkdir(parents=True)
                        throwaway.write_text(
                            "#!/usr/bin/env bash\n",
                            encoding="utf-8",
                        )
                        return mock.Mock(returncode=0, stdout="", stderr="")
                    if command[:3] == ["git", "checkout", "--detach"]:
                        return mock.Mock(returncode=0, stdout="", stderr="")
                    if command[:3] == ["git", "rev-parse", "--verify"]:
                        return mock.Mock(
                            returncode=0,
                            stdout=f"{resolved_head}\n",
                            stderr="",
                        )
                    observed_env.append(env)
                    return mock.Mock(returncode=0, stdout="", stderr="")

                with (
                    mock.patch.object(gtt, "run", side_effect=fake_run),
                    mock.patch.object(
                        gtt,
                        "reviewed_content_identity",
                        return_value={"sha256": "f" * 64},
                    ),
                ):
                    facts = gtt.extension_verification_execute_facts(
                        self.root,
                        public_input,
                        ["marketplace_index"],
                        expected_branch_review_commit=resolved_head,
                    )

                self.assertEqual(
                    facts["target_repository"]["resolved_head"],
                    resolved_head,
                )
                self.assertIn(
                    ["git", "ls-remote", "origin", ref, f"{ref}^{{}}"],
                    observed_commands,
                )
                self.assertIn(
                    ["git", "checkout", "--detach", resolved_head],
                    observed_commands,
                )
                self.assertIn(
                    ["git", "rev-parse", "--verify", "HEAD^{commit}"],
                    observed_commands,
                )
                self.assertEqual(
                    observed_env,
                    [{
                        "TRELLIS_WORKFLOW_SOURCE": (
                            f"gh:example/guru-extension/trellis#{ref}"
                        )
                    }],
                )

    def test_executor_fails_before_throwaway_when_checkout_commit_mismatches(
        self,
    ) -> None:
        public_input = self.public_input("standalone", task=False)
        requested_head = "b" * 40
        checkout_head = "c" * 40
        throwaway_called = False

        def fake_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> mock.Mock:
            nonlocal throwaway_called
            if command[:2] == ["git", "ls-remote"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{requested_head}\trefs/heads/main\n",
                    stderr="",
                )
            if command[:3] == ["git", "remote", "get-url"]:
                return mock.Mock(
                    returncode=0,
                    stdout="https://github.com/example/guru-extension.git\n",
                    stderr="",
                )
            if command[:2] == ["git", "clone"]:
                source = Path(command[-1])
                throwaway = (
                    source
                    / "trellis/presets/guru-team/scripts/bash/"
                    "verify-throwaway-install.sh"
                )
                throwaway.parent.mkdir(parents=True)
                throwaway.write_text(
                    "#!/usr/bin/env bash\n",
                    encoding="utf-8",
                )
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "checkout", "--detach"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "rev-parse", "--verify"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{checkout_head}\n",
                    stderr="",
                )
            throwaway_called = True
            return mock.Mock(returncode=0, stdout="", stderr="")

        with mock.patch.object(gtt, "run", side_effect=fake_run):
            facts = gtt.extension_verification_execute_facts(
                self.root,
                public_input,
                ["marketplace_index"],
                expected_branch_review_commit=requested_head,
            )

        self.assertEqual(facts["status"], "failed")
        self.assertEqual(
            facts["target_repository"]["resolved_head"],
            requested_head,
        )
        self.assertFalse(throwaway_called)
        self.assertEqual(
            facts["commands"][-1]["argv"],
            ["git", "rev-parse", "--verify", "HEAD^{commit}"],
        )

    def test_workflow_executor_binds_remote_commit_to_branch_review_commit(self) -> None:
        public_input = self.public_input("workflow", task=True)
        different_head = "b" * 40
        commands: list[list[str]] = []
        real_run = gtt.run

        def fake_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> mock.Mock:
            commands.append(command)
            if command[:2] == ["git", "ls-remote"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{different_head}\trefs/heads/main\n",
                    stderr="",
                )
            return real_run(command, cwd=cwd, check=check, env=env)

        with mock.patch.object(gtt, "run", side_effect=fake_run):
            facts = gtt.extension_verification_execute_facts(
                self.root,
                public_input,
                ["marketplace_index"],
            )

        self.assertEqual(facts["status"], "blocked")
        self.assertEqual(
            facts["target_repository"]["branch_review_commit"],
            self.head,
        )
        self.assertEqual(
            facts["target_repository"]["resolved_head"],
            different_head,
        )
        self.assertTrue(
            any(command[:3] == ["git", "remote", "get-url"] for command in commands)
        )

    def test_executor_pins_throwaway_marketplace_to_requested_remote_ref(self) -> None:
        self.assertEqual(
            gtt.extension_verification_workflow_source(
                "example/guru-extension",
                "refs/tags/v0.6.5-guru.23",
            ),
            "gh:example/guru-extension/trellis#refs/tags/v0.6.5-guru.23",
        )
        immutable_commit = "a" * 40
        self.assertEqual(
            gtt.extension_verification_workflow_source(
                "example/guru-extension",
                immutable_commit,
            ),
            f"gh:example/guru-extension/trellis#{immutable_commit}",
        )
        public_input = self.public_input("standalone", task=False)
        public_input["ref"] = "refs/heads/feature/117"
        remote_head = "b" * 40
        observed_env: list[dict[str, str] | None] = []

        def fake_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> mock.Mock:
            if command[:2] == ["git", "ls-remote"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{remote_head}\trefs/heads/feature/117\n",
                    stderr="",
                )
            if command[:3] == ["git", "remote", "get-url"]:
                return mock.Mock(
                    returncode=0,
                    stdout="https://github.com/example/guru-extension.git\n",
                    stderr="",
                )
            if command[:2] == ["git", "clone"]:
                source = Path(command[-1])
                throwaway = (
                    source
                    / "trellis/presets/guru-team/scripts/bash/"
                    "verify-throwaway-install.sh"
                )
                throwaway.parent.mkdir(parents=True)
                throwaway.write_text("#!/usr/bin/env bash\n", encoding="utf-8")
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "checkout", "--detach"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "rev-parse", "--verify"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{remote_head}\n",
                    stderr="",
                )
            observed_env.append(env)
            return mock.Mock(returncode=0, stdout="", stderr="")

        with (
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={"sha256": "f" * 64},
            ),
        ):
            gtt.extension_verification_execute_facts(
                self.root,
                public_input,
                ["marketplace_index"],
                expected_branch_review_commit=remote_head,
            )

        self.assertEqual(
            observed_env,
            [
                {
                    "TRELLIS_WORKFLOW_SOURCE": (
                        "gh:example/guru-extension/trellis#refs/heads/feature/117"
                    )
                }
            ],
        )

    def test_task_bearing_executor_uses_manifest_source_in_distinct_checkout(self) -> None:
        public_input = self.public_input("standalone", task=True)
        target_head = "a" * 40
        direct_tag = "b" * 40
        source_commit = "c" * 40
        source_ref = "refs/tags/v0.6.5-guru.3"
        clone_destinations: list[Path] = []
        real_run = gtt.run

        def fake_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> mock.Mock:
            if command[:2] == ["git", "ls-remote"]:
                if command[2] == "origin":
                    return mock.Mock(
                        returncode=0,
                        stdout=f"{target_head}\trefs/heads/main\n",
                        stderr="",
                    )
                self.assertEqual(
                    command[2],
                    "https://github.com/example/extension-source.git",
                )
                return mock.Mock(
                    returncode=0,
                    stdout=(
                        f"{direct_tag}\t{source_ref}\n"
                        f"{source_commit}\t{source_ref}^{{}}\n"
                    ),
                    stderr="",
                )
            if command[:3] == ["git", "remote", "get-url"]:
                return mock.Mock(
                    returncode=0,
                    stdout="https://github.com/example/guru-extension.git\n",
                    stderr="",
                )
            if command[:2] == ["git", "clone"]:
                destination = Path(command[-1])
                clone_destinations.append(destination)
                if destination.name == "target-checkout":
                    (destination / ".trellis/guru-team").mkdir(parents=True)
                    gtt.write_json(
                        destination / ".trellis/guru-team/extension.json",
                        {
                            "schema_version": "2.0",
                            "source": {
                                "repo": "https://github.com/example/extension-source.git",
                                "ref": source_ref,
                                "commit": source_commit,
                                "tree_state": "clean",
                                "is_mutable_ref": False,
                            },
                        },
                    )
                    self.assertFalse(
                        (
                            destination
                            / "trellis/presets/guru-team/scripts/bash/"
                            "verify-throwaway-install.sh"
                        ).exists()
                    )
                else:
                    self.copy_extension_source_fixture(destination)
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "checkout", "--detach"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "rev-parse", "--verify"]:
                head = (
                    target_head
                    if Path(cwd).name == "target-checkout"
                    else source_commit
                )
                return mock.Mock(returncode=0, stdout=f"{head}\n", stderr="")
            if command and command[0].endswith("verify-throwaway-install.sh"):
                install_work = Path(command[1])
                self.materialize_installed_asset_target(
                    Path(cwd),
                    install_work / "project",
                )
                return mock.Mock(returncode=0, stdout="", stderr="")
            return real_run(command, cwd=cwd, check=check, env=env)

        with (
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(
                gtt,
                "extension_verification_task_identity",
                return_value=self.task_dir,
            ),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={"sha256": "d" * 64},
            ),
        ):
            facts = gtt.extension_verification_execute_facts(
                self.root,
                public_input,
                list(gtt.EXTENSION_VERIFICATION_CAPABILITIES),
            )

        self.assertEqual(facts["status"], "passed", facts)
        self.assertEqual(facts["target_repository"]["resolved_head"], target_head)
        self.assertEqual(facts["extension_source"]["repo"], "example/extension-source")
        self.assertEqual(facts["extension_source"]["direct_oid"], direct_tag)
        self.assertEqual(facts["extension_source"]["commit"], source_commit)
        self.assertEqual(facts["extension_source"]["checkout_head"], source_commit)
        self.assertEqual(
            {path.name for path in clone_destinations},
            {"target-checkout", "extension-source-checkout"},
        )
        self.assertTrue(all(
            command["checkout_owner"] == "extension_source_checkout"
            for command in facts["commands"]
            if command["id"] in {
                "resolve_extension_source_ref",
                "clone_extension_source",
                "checkout_extension_source",
                "verify_extension_source_checkout",
                "verify_throwaway_installation",
            }
        ))

    def test_manifest_source_absence_fallback_and_task_bearing_failure(self) -> None:
        taskless = self.public_input("standalone", task=False)
        (self.root / ".trellis/guru-team/extension.json").unlink()
        source = gtt.extension_verification_manifest_source(
            self.root,
            taskless,
            task_bearing=False,
        )
        self.assertEqual(source["selection"], "standalone_fallback")
        self.assertEqual(source["manifest_provenance"], "not_available")
        self.assertEqual(
            source["locator"],
            "https://github.com/example/guru-extension.git",
        )
        with self.assertRaises(gtt.WorkflowError):
            gtt.extension_verification_manifest_source(
                self.root,
                taskless,
                task_bearing=True,
            )

    def test_malformed_or_credential_manifest_never_falls_back_or_leaks(self) -> None:
        manifest = self.root / ".trellis/guru-team/extension.json"
        taskless = self.public_input("standalone", task=False)
        manifest.write_text("{", encoding="utf-8")
        with self.assertRaises(gtt.WorkflowError) as malformed:
            gtt.extension_verification_manifest_source(
                self.root,
                taskless,
                task_bearing=False,
            )
        self.assertIn("malformed", str(malformed.exception))

        secret_locator = "https://user:secret@github.com/example/source.git"
        gtt.write_json(
            manifest,
            {
                "source": {
                    "repo": secret_locator,
                    "ref": "main",
                    "commit": "a" * 40,
                    "tree_state": "clean",
                    "is_mutable_ref": True,
                }
            },
        )
        with self.assertRaises(gtt.WorkflowError) as unsafe:
            gtt.extension_verification_manifest_source(
                self.root,
                taskless,
                task_bearing=False,
            )
        self.assertNotIn(secret_locator, str(unsafe.exception))
        self.assertNotIn("secret", json.dumps(unsafe.exception.payload))

    def test_task_bearing_dirty_source_blocks_before_source_resolution(self) -> None:
        public_input = self.public_input("standalone", task=True)
        target_head = "a" * 40
        source_calls: list[list[str]] = []

        def fake_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> mock.Mock:
            del check, env
            if command[:2] == ["git", "ls-remote"]:
                if command[2] != "origin":
                    source_calls.append(command)
                return mock.Mock(
                    returncode=0,
                    stdout=f"{target_head}\trefs/heads/main\n",
                    stderr="",
                )
            if command[:3] == ["git", "remote", "get-url"]:
                return mock.Mock(
                    returncode=0,
                    stdout="https://github.com/example/guru-extension.git\n",
                    stderr="",
                )
            if command[:2] == ["git", "clone"]:
                destination = Path(command[-1])
                if destination.name == "extension-source-checkout":
                    source_calls.append(command)
                destination.mkdir(parents=True)
                if destination.name == "target-checkout":
                    (destination / ".trellis/guru-team").mkdir(parents=True)
                    gtt.write_json(
                        destination / ".trellis/guru-team/extension.json",
                        {
                            "schema_version": "2.0",
                            "source": {
                                "repo": "https://github.com/example/extension-source.git",
                                "ref": "refs/heads/main",
                                "commit": "b" * 40,
                                "tree_state": "dirty",
                                "is_mutable_ref": True,
                            },
                        },
                    )
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "checkout", "--detach"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "rev-parse", "--verify"]:
                return mock.Mock(returncode=0, stdout=f"{target_head}\n", stderr="")
            if command and command[0].endswith("verify-throwaway-install.sh"):
                source_calls.append(command)
                return mock.Mock(returncode=0, stdout="", stderr="")
            return mock.Mock(returncode=1, stdout="", stderr="unexpected command")

        with (
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(
                gtt,
                "extension_verification_task_identity",
                return_value=self.task_dir,
            ),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={"sha256": "d" * 64},
            ),
            self.assertRaises(gtt.WorkflowError) as blocked,
        ):
            gtt.extension_verification_execute_facts(
                self.root,
                public_input,
                ["marketplace_index"],
            )

        self.assertEqual(
            blocked.exception.payload.get("reason_code"),
            "extension_source_not_clean",
        )
        self.assertEqual(source_calls, [])

    def test_manifest_commit_drift_blocks_before_source_clone(self) -> None:
        resolved = "a" * 40
        source = {
            "locator": "https://github.com/example/source.git",
            "requested_ref": "refs/tags/v1",
        }
        command = gtt.extension_verification_source_ref_command(
            source["locator"],
            source["requested_ref"],
        )
        proc = mock.Mock(
            returncode=0,
            stdout=f"{resolved}\trefs/tags/v1\n",
            stderr="",
        )
        resolved_ref, direct_oid, commit = (
            gtt.extension_verification_resolved_source_ref(
                proc,
                source["requested_ref"],
            )
        )
        self.assertEqual(command[0:3], ["git", "ls-remote", source["locator"]])
        self.assertEqual((resolved_ref, direct_oid, commit), (
            "refs/tags/v1",
            resolved,
            resolved,
        ))
        self.assertNotEqual(commit, "b" * 40)

    def test_immutable_commit_source_survives_branch_advance(self) -> None:
        source = self.root / "source-fixture"
        remote = self.root / "source-remote.git"
        source.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=source, check=True)
        subprocess.run(
            ["git", "config", "user.email", "source@example.invalid"],
            cwd=source,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Source Fixture"],
            cwd=source,
            check=True,
        )
        (source / "source.txt").write_text("source A\n", encoding="utf-8")
        subprocess.run(["git", "add", "source.txt"], cwd=source, check=True)
        subprocess.run(["git", "commit", "-qm", "source A"], cwd=source, check=True)
        source_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=source,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        subprocess.run(["git", "clone", "-q", "--bare", str(source), str(remote)], check=True)

        (source / "source.txt").write_text("target branch B\n", encoding="utf-8")
        subprocess.run(["git", "add", "source.txt"], cwd=source, check=True)
        subprocess.run(["git", "commit", "-qm", "target branch B"], cwd=source, check=True)
        subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=source, check=True)
        subprocess.run(["git", "push", "-q", "origin", "main"], cwd=source, check=True)
        advanced_head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=source,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertNotEqual(advanced_head, source_commit)

        checkout = self.root / "immutable-source-checkout"
        resolution = gtt.extension_verification_resolve_source_reference(
            str(remote),
            source_commit,
            checkout,
        )

        self.assertEqual(resolution["status"], "passed")
        self.assertEqual(resolution["resolved_ref"], source_commit)
        self.assertEqual(resolution["direct_oid"], source_commit)
        self.assertEqual(resolution["commit"], source_commit)
        self.assertTrue(resolution["checkout_prepared"])
        configured_origin = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=checkout,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(configured_origin, str(remote))
        self.assertEqual(
            [command["id"] for command in resolution["commands"]],
            [
                "clone_extension_source",
                "configure_extension_source_origin",
                "fetch_extension_source_commit",
                "resolve_extension_source_ref",
            ],
        )
        fetch_command = next(
            command["argv"]
            for command in resolution["commands"]
            if command["id"] == "fetch_extension_source_commit"
        )
        self.assertEqual(fetch_command[3], "origin")

    def test_executor_reuses_checkout_prepared_by_immutable_source_fetch(self) -> None:
        public_input = self.public_input("standalone", task=True)
        target_head = "a" * 40
        source_commit = "b" * 40
        clone_destinations: list[Path] = []

        def fake_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> mock.Mock:
            del check, env
            if command[:2] == ["git", "ls-remote"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{target_head}\trefs/heads/main\n",
                    stderr="",
                )
            if command[:3] == ["git", "remote", "get-url"]:
                return mock.Mock(
                    returncode=0,
                    stdout="https://github.com/example/guru-extension.git\n",
                    stderr="",
                )
            if command[:2] == ["git", "clone"]:
                destination = Path(command[-1])
                clone_destinations.append(destination)
                destination.mkdir(parents=True)
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "checkout", "--detach"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "rev-parse", "--verify"]:
                head = target_head if Path(cwd).name == "target-checkout" else source_commit
                return mock.Mock(returncode=0, stdout=f"{head}\n", stderr="")
            if command and command[0].endswith("verify-throwaway-install.sh"):
                self.materialize_installed_asset_target(
                    Path(cwd),
                    Path(command[1]) / "project",
                )
                return mock.Mock(returncode=0, stdout="", stderr="")
            return mock.Mock(returncode=1, stdout="", stderr="unexpected command")

        def resolve_source(
            locator: str,
            requested_ref: str,
            checkout: Path,
        ) -> dict[str, Any]:
            self.assertEqual(locator, "https://github.com/example/extension-source.git")
            self.assertEqual(requested_ref, source_commit)
            self.copy_extension_source_fixture(checkout)
            proc = mock.Mock(returncode=0, stdout=f"{source_commit}\n", stderr="")
            return {
                "status": "passed",
                "resolved_ref": source_commit,
                "direct_oid": source_commit,
                "commit": source_commit,
                "checkout_prepared": True,
                "commands": [
                    gtt.extension_verification_command_evidence(
                        "fetch_extension_source_commit",
                        "extension_source_checkout",
                        ["git", "fetch", "--depth=1", locator, requested_ref],
                        proc,
                    )
                ],
            }

        selected_source = {
            "selection": "manifest",
            "manifest_provenance": "available",
            "repo": "example/extension-source",
            "locator": "https://github.com/example/extension-source.git",
            "requested_ref": source_commit,
            "manifest_commit": source_commit,
            "tree_state": "clean",
            "is_mutable_ref": False,
        }
        with (
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(
                gtt,
                "extension_verification_task_identity",
                return_value=self.task_dir,
            ),
            mock.patch.object(
                gtt,
                "extension_verification_manifest_source",
                return_value=selected_source,
            ),
            mock.patch.object(
                gtt,
                "extension_verification_resolve_source_reference",
                side_effect=resolve_source,
            ),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={"sha256": "d" * 64},
            ),
        ):
            facts = gtt.extension_verification_execute_facts(
                self.root,
                public_input,
                ["marketplace_index"],
            )

        self.assertEqual(facts["status"], "passed", facts)
        self.assertEqual(facts["extension_source"]["resolved_ref"], source_commit)
        self.assertEqual([path.name for path in clone_destinations], ["target-checkout"])
        self.assertIn(
            "fetch_extension_source_commit",
            [command["id"] for command in facts["commands"]],
        )

    def test_source_checkout_head_mismatch_fails_before_installer(self) -> None:
        public_input = self.public_input("standalone", task=True)
        target_head = "a" * 40
        source_commit = "b" * 40
        reported_source_head = "c" * 40
        installer_commands: list[list[str]] = []

        def fake_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> mock.Mock:
            del check, env
            if command[:2] == ["git", "ls-remote"]:
                oid = target_head if command[2] == "origin" else source_commit
                ref = "refs/heads/main"
                return mock.Mock(
                    returncode=0,
                    stdout=f"{oid}\t{ref}\n",
                    stderr="",
                )
            if command[:3] == ["git", "remote", "get-url"]:
                return mock.Mock(
                    returncode=0,
                    stdout="https://github.com/example/guru-extension.git\n",
                    stderr="",
                )
            if command[:2] == ["git", "clone"]:
                Path(command[-1]).mkdir(parents=True)
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "checkout", "--detach"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "rev-parse", "--verify"]:
                head = (
                    target_head
                    if Path(cwd).name == "target-checkout"
                    else reported_source_head
                )
                return mock.Mock(returncode=0, stdout=f"{head}\n", stderr="")
            if command and command[0].endswith("verify-throwaway-install.sh"):
                installer_commands.append(command)
                return mock.Mock(returncode=0, stdout="", stderr="")
            return mock.Mock(returncode=1, stdout="", stderr="unexpected command")

        source = {
            "selection": "manifest",
            "manifest_provenance": "available",
            "repo": "example/extension-source",
            "locator": "https://github.com/example/extension-source.git",
            "requested_ref": "refs/heads/main",
            "manifest_commit": source_commit,
            "tree_state": "clean",
            "is_mutable_ref": True,
        }
        with (
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(
                gtt,
                "extension_verification_task_identity",
                return_value=self.task_dir,
            ),
            mock.patch.object(
                gtt,
                "extension_verification_manifest_source",
                return_value=source,
            ),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={"sha256": "d" * 64},
            ),
        ):
            facts = gtt.extension_verification_execute_facts(
                self.root,
                public_input,
                ["marketplace_index"],
            )

        self.assertEqual(facts["status"], "failed")
        self.assertEqual(
            facts["extension_source"]["checkout_head"],
            reported_source_head,
        )
        self.assertFalse(facts["extension_source"]["checkout_head_matches"])
        self.assertEqual(installer_commands, [])

    def test_missing_source_installer_fails_with_current_source_head(self) -> None:
        public_input = self.public_input("standalone", task=True)
        target_head = "a" * 40
        source_commit = "b" * 40
        source_checkout_cloned = False
        installer_commands: list[list[str]] = []

        def fake_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> mock.Mock:
            nonlocal source_checkout_cloned
            del check, env
            if command[:2] == ["git", "ls-remote"]:
                oid = target_head if command[2] == "origin" else source_commit
                return mock.Mock(
                    returncode=0,
                    stdout=f"{oid}\trefs/heads/main\n",
                    stderr="",
                )
            if command[:3] == ["git", "remote", "get-url"]:
                return mock.Mock(
                    returncode=0,
                    stdout="https://github.com/example/guru-extension.git\n",
                    stderr="",
                )
            if command[:2] == ["git", "clone"]:
                destination = Path(command[-1])
                destination.mkdir(parents=True)
                if destination.name == "extension-source-checkout":
                    source_checkout_cloned = True
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "checkout", "--detach"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "rev-parse", "--verify"]:
                head = (
                    target_head
                    if Path(cwd).name == "target-checkout"
                    else source_commit
                )
                return mock.Mock(returncode=0, stdout=f"{head}\n", stderr="")
            if command and command[0].endswith("verify-throwaway-install.sh"):
                installer_commands.append(command)
                return mock.Mock(returncode=0, stdout="", stderr="")
            return mock.Mock(returncode=1, stdout="", stderr="unexpected command")

        source = {
            "selection": "manifest",
            "manifest_provenance": "available",
            "repo": "example/extension-source",
            "locator": "https://github.com/example/extension-source.git",
            "requested_ref": "refs/heads/main",
            "manifest_commit": source_commit,
            "tree_state": "clean",
            "is_mutable_ref": True,
        }
        with (
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(
                gtt,
                "extension_verification_task_identity",
                return_value=self.task_dir,
            ),
            mock.patch.object(
                gtt,
                "extension_verification_manifest_source",
                return_value=source,
            ),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={"sha256": "d" * 64},
            ),
        ):
            facts = gtt.extension_verification_execute_facts(
                self.root,
                public_input,
                ["marketplace_index"],
            )

        self.assertTrue(source_checkout_cloned)
        self.assertTrue(facts["extension_source"]["ref_matches_commit"])
        self.assertEqual(facts["extension_source"]["checkout_head"], source_commit)
        self.assertTrue(facts["extension_source"]["checkout_head_matches"])
        self.assertEqual(installer_commands, [])
        self.assertEqual(facts["status"], "failed")
        with self.assertRaises(gtt.WorkflowError):
            self.record(
                public_input,
                facts,
                self.review("verified", ["marketplace_index"]),
            )

    def test_task_bearing_dirty_source_cannot_be_recorded_or_checked(self) -> None:
        public_input = self.public_input("workflow", task=True)
        selected = ["marketplace_index"]
        dirty_execution = self.execution(public_input, "passed", selected)
        dirty_execution["extension_source"]["tree_state"] = "dirty"
        with (
            mock.patch.object(
                gtt,
                "extension_verification_task_identity",
                return_value=self.task_dir,
            ),
            mock.patch.object(
                gtt,
                "worktree_records",
                return_value=[{
                    "worktree": str(self.root),
                    "branch": "refs/heads/main",
                }],
            ),
            self.assertRaises(gtt.WorkflowError) as record_error,
        ):
            self.record(
                public_input,
                dirty_execution,
                self.review("verified", selected),
            )
        self.assertIn(
            "requires clean source provenance",
            f"{record_error.exception} {json.dumps(record_error.exception.payload)}",
        )

        owner = self.record(
            public_input,
            self.execution(public_input, "passed", selected),
            self.review("verified", selected),
        )
        owner["extension_source"]["tree_state"] = "dirty"
        owner["execution"]["extension_source"]["tree_state"] = "dirty"
        machine_digest, semantic_digest, facts_digest = (
            gtt.extension_verification_payload_digests(owner)
        )
        owner["machine_facts_sha256"] = machine_digest
        owner["semantic_review_sha256"] = semantic_digest
        owner["facts_sha256"] = facts_digest
        owner["identity"]["verification_ref"] = (
            f"extension-verification:{facts_digest[:24]}"
        )
        source_ref_calls: list[list[str]] = []

        def checker_run(
            command: list[str],
            cwd: Path | None = None,
            check: bool = True,
            env: dict[str, str] | None = None,
        ) -> mock.Mock:
            del cwd, check, env
            if command[:2] == ["git", "ls-remote"]:
                if command[2] != "origin":
                    source_ref_calls.append(command)
                oid = self.head if command[2] == "origin" else "b" * 40
                return mock.Mock(
                    returncode=0,
                    stdout=f"{oid}\trefs/heads/main\n",
                    stderr="",
                )
            return mock.Mock(returncode=1, stdout="", stderr="unexpected command")

        with (
            mock.patch.object(gtt, "run", side_effect=checker_run),
            mock.patch.object(
                gtt,
                "extension_verification_task_identity",
                return_value=self.task_dir,
            ),
            mock.patch.object(
                gtt,
                "extension_verification_reviewed_content_sha256",
                return_value=owner["target_repository"]["reviewed_content_sha256"],
            ),
            self.assertRaises(gtt.WorkflowError) as check_error,
        ):
            gtt.check_extension_verification_result(
                self.root,
                owner,
                ".trellis/tasks/current/marketplace-verification.json",
                public_input,
            )
        self.assertIn(
            "requires clean source provenance",
            f"{check_error.exception} {json.dumps(check_error.exception.payload)}",
        )
        self.assertEqual(source_ref_calls, [])

    def test_recorded_source_checkout_head_mismatch_is_rejected(self) -> None:
        public_input = self.public_input("workflow", task=True)
        execution = self.execution(
            public_input,
            "passed",
            ["marketplace_index"],
        )
        execution["extension_source"]["checkout_head"] = "c" * 40
        execution["extension_source"]["checkout_head_matches"] = False
        with self.assertRaises(gtt.WorkflowError) as mismatch:
            self.record(
                public_input,
                execution,
                self.review("verified", ["marketplace_index"]),
            )
        self.assertIn(
            "current target and source identities",
            json.dumps(mismatch.exception.payload),
        )


class CloseoutTransactionContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.task_dir = self.root / ".trellis/tasks/07-11-closeout"
        self.task_dir.mkdir(parents=True)
        self.head = "a" * 40
        self.context = {
            "task_artifact_dir": ".trellis/tasks/07-11-closeout",
            "base_branch": "main",
            "branch_name": "fix/105-closeout",
        }
        self.task = {"id": "105-closeout", "title": "#105 closeout", "base_branch": "main"}
        self.gate = {
            "schema_version": gtt.BRANCH_REVIEW_SCHEMA_VERSION,
            "skill_id": gtt.BRANCH_REVIEW_SKILL_ID,
            "task_dir": ".trellis/tasks/07-11-closeout",
            "typed_exit": "passed",
            "review_commit": self.head,
            "reviewed_content_sha256": "b" * 64,
            "generated_at": "2026-07-11T00:00:00Z",
        }
        issue = {
            "number": 105,
            "url": "https://github.com/owner/repo/issues/105",
            "title": "closeout",
            "reason": "Primary delivered scope.",
        }
        self.ledger = {
            "schema_version": "2.0",
            "primary_issue": issue,
            "close_issues": [issue],
            "related_issues": [],
            "followup_issues": [],
        }
        self.index = {
            "schema_version": 1,
            "index": {
                "problem": "旧 finish-work 在 archive 后仍有可预见失败。",
                "outcome": "closeout 改为单入口可恢复事务。",
                "changed_behavior": ["archive 前完成 draft identity 与 final projection。"],
                "affected_surfaces": [{
                    "kind": "workflow",
                    "name": "finish-work",
                    "paths": ["trellis/workflows/guru-team/workflow.md"],
                    "change": "收尾改为 immutable plan 状态机。",
                }],
                "contract_changes": [],
                "search_terms": {
                    "commands": ["finish-work.sh"],
                    "config_keys": [],
                    "schema_fields": ["closeout_plan_digest"],
                    "symbols": ["prepare_closeout"],
                    "phrases": [
                        "旧 finish-work archive 后失败问题",
                        "closeout_plan_digest schema 合同",
                        "draft-to-ready 收尾事务已完成",
                    ],
                },
            },
        }
        self.body = valid_pr_body("#105 closeout transaction。")
        gtt.write_json(self.task_dir / "task.json", self.task)
        self.review_gate_path = gtt.configured_review_gate_path(
            self.root,
            self.task_dir,
        )
        gtt.write_json(self.review_gate_path, self.gate)
        gtt.write_json(self.task_dir / "issue-scope-ledger.json", self.ledger)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def validate_task_json_archive_continuity_fixture(
        self,
        *,
        parent: bytes,
        after: bytes,
        binding: dict[str, str] | None,
        after_mode: str = "100644",
        archive_commit: str | None = None,
    ) -> None:
        archived = self.root / "archive-fixture"
        archived.mkdir(exist_ok=True)
        task_json = archived / "task.json"
        task_json.write_bytes(after)
        task_json.chmod(0o755 if after_mode == "100755" else 0o644)
        (archived / gtt.FINISH_SUMMARY_ARTIFACT).write_text("{}", encoding="utf-8")
        plan = {
            "schema_version": gtt.CLOSEOUT_PLAN_SCHEMA_VERSION,
            "task": {
                "active_locator": ".trellis/tasks/07-11-closeout",
                "archive_locator": ".trellis/tasks/archive/2026-07/07-11-closeout",
            },
            "marketplace": {"required": False},
            "projection": {
                "move_paths": ["task.json"],
                "tracked_move_paths": ["task.json"],
                "reviewed_tracked_bindings": [] if binding is None else [binding],
            },
        }
        committed = "c" * 40

        def blob_bytes(_root: Path, commit: str, path: str) -> bytes:
            if commit == self.head:
                return parent
            if commit == committed and path.endswith("/task.json"):
                return after
            if commit == committed and path.endswith(f"/{gtt.FINISH_SUMMARY_ARTIFACT}"):
                return b"{}"
            raise AssertionError((commit, path))

        def tree_entry(_root: Path, commit: str, path: str) -> tuple[str, str, str]:
            mode = "100644" if commit == self.head else after_mode
            return mode, "blob", "d" * 40

        with (
            mock.patch.object(gtt, "closeout_commit_blob_bytes", side_effect=blob_bytes),
            mock.patch.object(gtt, "closeout_commit_tree_entry", side_effect=tree_entry),
            mock.patch.object(
                gtt,
                "closeout_summary_runtime_pr_facts_from_bytes",
                return_value={"number": 105},
            ),
        ):
            gtt.validate_closeout_archive_blob_continuity(
                self.root,
                archived,
                plan,
                self.head,
                archive_commit=committed if archive_commit is not None else None,
            )

    def test_closeout_children_contract_requires_list_of_strings(self) -> None:
        gtt.validate_closeout_task_children(self.task_dir, self.task)
        for malformed in ({"child": "bad"}, "child", ["child", 7]):
            with self.subTest(malformed=malformed), self.assertRaises(gtt.WorkflowError) as error:
                gtt.validate_closeout_task_children(
                    self.task_dir,
                    {**self.task, "children": malformed},
                )
            self.assertEqual(error.exception.payload.get("stage"), "task-children-preflight")

    def test_closeout_children_contract_uses_official_active_suffix_lookup(self) -> None:
        child_dir = self.task_dir.parent / "07-10-child"
        child_dir.mkdir()
        gtt.write_json(child_dir / "task.json", {"id": "child", "parent": self.task_dir.name})
        with self.assertRaises(gtt.WorkflowError) as error:
            gtt.validate_closeout_task_children(
                self.task_dir,
                {**self.task, "children": ["child"]},
            )
        self.assertEqual(error.exception.payload.get("active_children"), ["07-10-child"])

    def test_archive_path_preflight_rejects_dangling_root_and_month_symlinks(self) -> None:
        archive_root = self.root / ".trellis/tasks/archive"
        archive_locator = ".trellis/tasks/archive/2026-07/07-11-closeout"
        archive_root.symlink_to(self.root / "missing-archive-root", target_is_directory=True)
        with self.assertRaises(gtt.WorkflowError) as root_error:
            gtt.assert_closeout_archive_path_preflight(self.root, archive_locator)
        self.assertEqual(root_error.exception.payload.get("component"), "archive-root")
        archive_root.unlink()

        archive_root.mkdir()
        month = archive_root / "2026-07"
        month.symlink_to(self.root / "missing-archive-month", target_is_directory=True)
        with self.assertRaises(gtt.WorkflowError) as month_error:
            gtt.assert_closeout_archive_path_preflight(self.root, archive_locator)
        self.assertEqual(month_error.exception.payload.get("component"), "archive-month")

    def test_committed_summary_runtime_facts_use_deterministic_bytes_without_general_validator(self) -> None:
        plan = self.build_plan()
        pr = {"number": 105, "url": "https://github.com/owner/repo/pull/105"}
        summary = gtt.render_closeout_summary_for_pr(plan, pr)
        content = gtt.closeout_json_artifact_bytes(summary)
        with mock.patch.object(
            gtt,
            "validate_finish_summary",
            side_effect=AssertionError("general validator must not run"),
        ):
            facts = gtt.closeout_summary_runtime_pr_facts_from_bytes(
                plan,
                content,
                expected_pr=pr,
            )
        self.assertEqual(facts["number"], 105)
        self.assertEqual(facts["url"], pr["url"])
        self.assertEqual(facts["summary_sha256"], gtt.hashlib.sha256(content).hexdigest())

        tampered = gtt.copy.deepcopy(summary)
        tampered["index"]["outcome"] = "tampered deterministic JSON"
        with self.assertRaises(gtt.WorkflowError):
            gtt.closeout_summary_runtime_pr_facts_from_bytes(
                plan,
                gtt.closeout_json_artifact_bytes(tampered),
                expected_pr=pr,
            )
        with self.assertRaises(gtt.WorkflowError):
            gtt.closeout_summary_runtime_pr_facts_from_bytes(
                plan,
                content,
                expected_pr={"number": 106, "url": "https://github.com/owner/repo/pull/106"},
            )

    def test_strict_pr_url_parser_preserves_mixed_case_remote_canonical_url(self) -> None:
        url = "https://github.com/microsoft/PowerToys/pull/105"
        self.assertEqual(
            gtt.parse_canonical_pull_request_url("microsoft/powertoys", url),
            (url, 105),
        )
        for invalid in [
            "http://github.com/microsoft/PowerToys/pull/105",
            "https://github.com/microsoft/PowerShell/pull/105",
            "https://github.com/micro%73oft/PowerToys/pull/105",
            "https://github.com/microsoft/Power%54oys/pull/105",
            "https://github.com/microsoft/PowerToys/pull/0105",
            "https://github.com/microsoft/PowerToys/pull/105/",
            "https://github.com/microsoft/PowerToys/pull/105/files",
            "https://github.com/microsoft/PowerToys/pull/105?diff=split",
            "https://github.com/microsoft/PowerToys/pull/105#discussion",
            "https://github.com/microsoft/PowerToys/pull/" + "9" * 5000,
        ]:
            with self.subTest(invalid=invalid), self.assertRaises(gtt.WorkflowError):
                gtt.parse_canonical_pull_request_url("microsoft/powertoys", invalid)
        with self.assertRaises(gtt.WorkflowError):
            gtt.canonical_pull_request_url(
                "microsoft/powertoys", 105, "https://github.com/microsoft/PowerToys/pull/106"
            )

    def test_mixed_case_pr_url_final_projection_uses_remote_canonical_output(self) -> None:
        plan = self.build_plan(repo="microsoft/powertoys")
        pr = {"number": 105, "url": "https://github.com/microsoft/PowerToys/pull/105"}
        summary = gtt.closeout_summary_for_pr(plan, pr)
        self.assertEqual(summary["github"]["pr_url"], pr["url"])
        gtt.validate_closeout_final_summary(plan, summary)
        with self.assertRaises(gtt.WorkflowError):
            gtt.render_closeout_summary_for_pr(
                plan,
                {"number": 105, "url": "https://github.com/microsoft/PowerShell/pull/105"},
            )

    def test_mixed_case_pr_url_incomplete_and_exact_recovery_share_strict_parser(self) -> None:
        plan = self.build_plan(repo="microsoft/powertoys")
        pr = {"number": 105, "url": "https://github.com/microsoft/PowerToys/pull/105"}
        content = gtt.closeout_json_artifact_bytes(gtt.render_closeout_summary_for_pr(plan, pr))
        incomplete = gtt.closeout_summary_runtime_pr_facts_from_bytes(
            plan, content, expected_pr=pr
        )
        exact = gtt.closeout_summary_runtime_pr_facts_from_bytes(plan, content)
        self.assertEqual(incomplete["url"], pr["url"])
        self.assertEqual(exact["url"], pr["url"])

        wrong_repo = json.loads(content.decode("utf-8"))
        wrong_repo["github"]["pr_url"] = "https://github.com/microsoft/PowerShell/pull/105"
        wrong_content = gtt.closeout_json_artifact_bytes(wrong_repo)
        with self.assertRaises(gtt.WorkflowError):
            gtt.closeout_summary_runtime_pr_facts_from_bytes(
                plan, wrong_content, expected_pr=pr
            )
        with self.assertRaises(gtt.WorkflowError):
            gtt.closeout_summary_runtime_pr_facts_from_bytes(plan, wrong_content)

    def build_plan(
        self,
        *,
        repo: str = "owner/repo",
        head_branch: str = "fix/105-closeout",
    ) -> dict[str, object]:
        def fake_run(command: list[str], **_kwargs: object) -> mock.Mock:
            if command[:2] == ["git", "rev-list"]:
                stdout = f"{self.head}\n"
            elif command[:2] == ["git", "show"]:
                stdout = "2026-07-11T00:00:00+00:00\n"
            elif command[:2] == ["git", "ls-files"]:
                stdout = "\n".join(
                    path.relative_to(self.root).as_posix()
                    for path in sorted(self.task_dir.rglob("*"))
                    if path.is_file()
                )
            else:
                stdout = ""
            return mock.Mock(returncode=0, stdout=stdout, stderr="")

        tracked = sorted(
            path.relative_to(self.task_dir).as_posix()
            for path in self.task_dir.rglob("*")
            if path.is_file()
        )
        generated_outputs = [
            gtt.CLOSEOUT_PLAN_ARTIFACT,
            gtt.FINISH_SUMMARY_ARTIFACT,
            gtt.MARKETPLACE_VERIFICATION_ARTIFACT,
        ]
        with (
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(
                gtt,
                "closeout_live_move_classes",
                return_value=(
                    tracked,
                    [name for name in generated_outputs if name not in tracked],
                ),
            ),
            mock.patch.object(
                gtt,
                "build_closeout_reviewed_tracked_bindings",
                return_value=[],
            ),
        ):
            return gtt.build_closeout_plan(
                self.root,
                self.task_dir,
                self.context,
                self.task,
                self.ledger,
                repo=repo,
                remote="origin",
                base_branch="main",
                head_branch=head_branch,
                branch_review_commit=self.head,
                title="#105 重构 finish-work 收尾事务",
                body=self.body,
                review_facts={
                    "changed_paths": ["trellis/workflows/guru-team/workflow.md"],
                    "marketplace_required": True,
                },
            )

    def legacy_plan_from_current(
        self,
        current: dict[str, object],
        *,
        body: str | None = None,
    ) -> dict[str, object]:
        legacy = copy.deepcopy(current)
        exact_body = body if body is not None else self.body
        legacy["schema_version"] = gtt.LEGACY_CLOSEOUT_PLAN_SCHEMA_VERSION
        legacy["publish"]["body_sha256"] = hashlib.sha256(  # type: ignore[index]
            exact_body.encode("utf-8")
        ).hexdigest()
        legacy["publish"].pop("body")  # type: ignore[index]
        active = legacy["task"]["active_locator"]  # type: ignore[index]
        legacy["inputs"]["pr_body"] = {  # type: ignore[index]
            "path": f"{active}/pr-body.md",
            "sha256": hashlib.sha256(exact_body.encode("utf-8")).hexdigest(),
        }
        legacy["inputs"]["finish_summary_index"] = {  # type: ignore[index]
            "path": f"{active}/finish-summary-index.json",
            "sha256": gtt.canonical_json_sha256(self.index),
        }
        legacy["projection"]["migration_predecessor_plan_digest"] = None  # type: ignore[index]
        legacy["plan_digest"] = gtt.closeout_plan_digest(legacy)
        gtt.validate_closeout_plan_for_migration(legacy)
        return legacy

    def test_current_plan_omits_producer_private_runtime_identity(self) -> None:
        current = self.build_plan()

        self.assertEqual(current["schema_version"], gtt.CLOSEOUT_PLAN_SCHEMA_VERSION)
        self.assertNotIn("task_context", current["inputs"])
        self.assertNotIn("review_gate", current["inputs"])
        self.assertEqual(gtt.closeout_plan_errors(current), [])

    def current_publication_owner(
        self,
        *,
        task_ref: str,
        branch_review_commit: str,
    ) -> dict[str, object]:
        source = (
            Path(__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages/guru-review-task-publication"
            / "examples/pr-readiness.json"
        )
        owner = json.loads(source.read_text(encoding="utf-8"))
        owner["task_ref"] = task_ref
        owner["branch_review_commit"] = branch_review_commit
        owner["pr_payload"] = {
            "title": "#105 重构 finish-work 收尾事务",
            "body": self.body,
        }
        return owner

    def write_current_publication_owner(
        self,
        root: Path,
        task_dir: Path,
        *,
        task_ref: str,
        branch_review_commit: str,
    ) -> Path:
        path = gtt.task_publication_path(root, task_dir)
        gtt.write_json(
            path,
            self.current_publication_owner(
                task_ref=task_ref,
                branch_review_commit=branch_review_commit,
            ),
        )
        return path

    def exercise_prepared_finalization_gate_reentry(
        self,
        *,
        arbitrary_metadata: bool = False,
    ) -> dict[str, object] | None:
        self.task["status"] = "in_progress"
        gtt.write_json(self.task_dir / "task.json", self.task)
        task_ref = gtt.repo_relative(self.root, self.task_dir)
        gate_relative = f"{task_ref}/{gtt.TASK_FINALIZATION_GATE_ARTIFACT}"
        unexpected_relative = f"{task_ref}/arbitrary-finalization-note.md"
        plan = self.build_plan()
        plan_ref = f"closeout-plan:{plan['plan_digest']}"
        public_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": task_ref,
            "branch_review_commit": self.head,
            "pr_title": plan["publish"]["title"],
            "pr_body": plan["publish"]["body"],
        }
        stored_repository = {
            "head": self.head,
            "branch": "fix/105-closeout",
            "base_ref": "origin/main",
            "diff_paths": ["src/runtime.py"],
            "status_paths": [],
        }
        self.write_current_publication_owner(
            self.root,
            self.task_dir,
            task_ref=task_ref,
            branch_review_commit=self.head,
        )
        prepared = {
            "plan": plan,
            "ledger": self.ledger,
            "gate": self.gate,
            "month_supersession": None,
        }
        review = {
            "review": {
                "status": "passed",
                "summary": "The exact prepared plan is current.",
            },
            "route": {
                "typed_exit": "verification_required",
                "consumer": gtt.FINALIZATION_CONSUMERS["verification_required"],
                "output": {
                    "exit_id": "verification_required",
                    "task_ref": task_ref,
                    "plan_ref": plan_ref,
                    "repo_ref": plan["git"]["repo"],
                    "branch_review_commit": plan["git"]["branch_review_commit"],
                    "verification_target": "extension-installation",
                },
            },
        }
        package_root = (
            Path(__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages/guru-finalize-task"
        )
        runtime_args = argparse.Namespace(
            root=str(self.root),
            input="unused-public-input.json",
            review_input="unused-review-input.json",
            gate=None,
            dry_run=False,
            repo="owner/repo",
            remote="origin",
        )

        def current_repository() -> dict[str, object]:
            paths = list(stored_repository["status_paths"])
            if (self.task_dir / gtt.TASK_FINALIZATION_GATE_ARTIFACT).is_file():
                paths.append(gate_relative)
            if (self.task_dir / "arbitrary-finalization-note.md").is_file():
                paths.append(unexpected_relative)
            return {**stored_repository, "status_paths": sorted(paths)}

        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "finalization_task_dir", return_value=self.task_dir),
            mock.patch.object(
                gtt,
                "finalization_public_input",
                return_value=(public_input, "<test>"),
            ),
            mock.patch.object(
                gtt,
                "finalization_semantic_review_input",
                return_value=review,
            ),
            mock.patch.object(gtt, "finalization_package_root", return_value=package_root),
            mock.patch.object(gtt, "finalization_output_contract", return_value={"type": "object"}),
            mock.patch.object(gtt, "finalization_verification_owner_result", return_value=None),
            mock.patch.object(
                gtt,
                "finalization_current_verification_owner_result",
                return_value=None,
            ),
            mock.patch.object(gtt, "load_config", return_value={}),
            mock.patch.object(gtt, "load_task_runtime_identity", return_value=self.context),
            mock.patch.object(gtt, "assert_workspace_boundary"),
            mock.patch.object(gtt, "prepare_closeout", return_value=prepared),
            mock.patch.object(
                gtt,
                "current_head",
                return_value=self.head,
            ),
            mock.patch.object(
                gtt,
                "is_ancestor",
                return_value=True,
            ),
            mock.patch.object(
                gtt,
                "reviewed_content_identity",
                return_value={"sha256": "b" * 64},
            ),
            mock.patch.object(
                gtt,
                "review_branch_content_continuity_errors",
                return_value=[],
            ),
            mock.patch.object(
                gtt,
                "task_publication_repository_binding",
                side_effect=lambda *_args, **_kwargs: current_repository(),
            ),
        ):
            recorded = gtt.cmd_record_finalization_gate(runtime_args)
            self.assertEqual(recorded["typed_exit"], "verification_required")
            if arbitrary_metadata:
                (self.task_dir / "arbitrary-finalization-note.md").write_text(
                    "ordinary unowned metadata\n",
                    encoding="utf-8",
                )
                return gtt.cmd_check_finalization_gate(runtime_args)
            return gtt.cmd_check_finalization_gate(runtime_args)

    def test_prepared_finalization_gate_recorder_reenters_checker(self) -> None:
        checked = self.exercise_prepared_finalization_gate_reentry()
        assert checked is not None
        self.assertEqual(checked["transaction_state"], "prepared")
        self.assertEqual(checked["typed_exit"], "verification_required")

    def test_prepared_finalization_gate_reentry_accepts_task_metadata_tail(self) -> None:
        checked = self.exercise_prepared_finalization_gate_reentry(
            arbitrary_metadata=True
        )
        assert checked is not None
        self.assertEqual(checked["typed_exit"], "verification_required")

    def test_public_wrapper_does_not_default_initial_preview_sources(self) -> None:
        wrapper_args = argparse.Namespace(base_branch=None)
        checker_args = gtt.finalization_public_wrapper_checker_args(
            self.root,
            wrapper_args,
            self.task_dir,
        )
        self.assertFalse(hasattr(checker_args, "finish_summary_index_file"))
        self.assertFalse(hasattr(checker_args, "body_file"))
        self.assertFalse(hasattr(gtt, "load_finish_summary_index"))
        self.assertFalse(hasattr(gtt, "resolve_closeout_reviewed_body"))

    def test_existing_plan_public_wrapper_preserves_checked_blocked_evidence_ready_route(
        self,
    ) -> None:
        plan = self.build_plan()
        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, plan)
        task_ref = self.task_dir.relative_to(self.root).as_posix()
        plan_ref = f"closeout-plan:{plan['plan_digest']}"
        public_input = {
            "profile": "same_plan_resume",
            "mode": "workflow",
            "task_ref": task_ref,
            "plan_ref": plan_ref,
        }
        output = {
            "exit_id": "blocked",
            "reason_code": "external_dependency_blocked",
            "remediation": "Retry the same reviewed Finalizer transaction when the dependency recovers.",
        }
        gate = {
            "schema_version": gtt.FINALIZATION_GATE_SCHEMA_VERSION,
            "skill_id": gtt.FINALIZE_TASK_SKILL_ID,
            "identity": {
                "task_ref": task_ref,
                "plan_ref": plan_ref,
                "plan_digest": plan["plan_digest"],
                "branch_review_commit": plan["git"]["branch_review_commit"],
            },
            "review": {
                "status": "passed",
                "summary": "The exact same-plan recovery is externally blocked.",
            },
            "route": {
                "typed_exit": "blocked",
                "consumer": gtt.FINALIZATION_CONSUMERS["blocked"],
                "output": output,
            },
        }
        context = {
            "task_dir": self.task_dir,
            "task_context": self.context,
            "prepared": {"plan": plan},
            "plan": plan,
            "plan_ref": plan_ref,
            "transaction_state": "evidence_ready",
            "published_transition_complete": False,
            "published_pr": None,
            "publication_status": "current",
            "publication_stale_reason": None,
            "verification": ({}, {"typed_exit": "verified"}),
        }
        package_root = (
            Path(__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages/guru-finalize-task"
        )
        args = argparse.Namespace(
            root=str(self.root),
            input="unused-public-input.json",
            owner_result=None,
            gate=None,
            base_branch=None,
        )
        seen_checker_args: list[argparse.Namespace] = []

        def preview(
            _root: Path,
            checker_args: argparse.Namespace,
            _public_input: dict[str, object],
        ) -> dict[str, object]:
            seen_checker_args.append(checker_args)
            return context

        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(
                gtt,
                "finalization_public_input",
                return_value=(public_input, "<test>"),
            ),
            mock.patch.object(
                gtt,
                "finalization_gate_input",
                return_value=(gate, self.task_dir / gtt.TASK_FINALIZATION_GATE_ARTIFACT),
            ),
            mock.patch.object(gtt, "finalization_preview_context", side_effect=preview),
            mock.patch.object(
                gtt,
                "stage0_invocation_identity",
                return_value=(gtt.FINALIZE_TASK_SKILL_ID, self.root),
            ),
            mock.patch.object(gtt, "stage0_public_interface", return_value={}),
            mock.patch.object(gtt, "stage0_repo_root", return_value=self.root),
            mock.patch.object(
                gtt,
                "stage0_structured_input",
                return_value=public_input,
            ),
            mock.patch.object(gtt, "finalization_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "finalization_package_root", return_value=package_root),
            mock.patch.object(
                gtt,
                "stage0_output_contract",
                return_value=(
                    gtt.read_json(package_root / "schemas/public-blocked-output.schema.json"),
                    {},
                ),
            ),
        ):
            direct = gtt.cmd_check_finalization_gate(args)
            wrapped = gtt.cmd_invoke_stage0_skill(args)

        self.assertEqual(direct["typed_exit"], "blocked")
        self.assertEqual(direct["transaction_state"], "evidence_ready")
        self.assertEqual(wrapped, output)
        self.assertEqual(len(seen_checker_args), 2)
        wrapper_args = seen_checker_args[1]
        self.assertFalse(hasattr(wrapper_args, "finish_summary_index_file"))
        self.assertFalse(hasattr(wrapper_args, "body_file"))

    def test_finalization_eval_context_carries_publication_stale_owner_facts(self) -> None:
        public_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": self.task_dir.relative_to(self.root).as_posix(),
            "branch_review_commit": self.head,
            "pr_title": "#105 重构 finish-work 收尾事务",
            "pr_body": self.body,
        }
        runtime_dir = self.root / ".trellis/.runtime/guru-team/evals"
        runtime_dir.mkdir(parents=True)
        gtt.write_json(
            runtime_dir / "finalization-context.json",
            {
                "schema_version": "2.0",
                "task_ref": public_input["task_ref"],
                "plan_ref": f"closeout-plan:{'b' * 64}",
                "plan_digest": "b" * 64,
                "branch_review_commit": self.head,
                "publication_head": self.head,
                "archive_locator": ".trellis/tasks/archive/2026-07/07-11-closeout",
                "repo_ref": "owner/repo",
                "remote": "origin",
                "head_branch": "main",
                "verification_ref": None,
                "publication_status": "stale",
                "publication_stale_reason": "publication_review_missing",
                "marketplace_required": True,
                "transaction_state": "prepared",
            },
        )
        with mock.patch.dict(os.environ, {"GURU_TEAM_EVAL_STAGING": "1"}):
            context = gtt.finalization_eval_preview_context(self.root, public_input)
        self.assertIsNotNone(context)
        assert context is not None
        self.assertEqual(context["publication_status"], "stale")
        self.assertEqual(context["plan"]["git"]["reviewed_content_head"], self.head)
        self.assertEqual(context["plan"]["git"]["publication_head"], self.head)
        self.assertEqual(
            context["publication_stale_reason"],
            "publication_review_missing",
        )
        with mock.patch.object(
            gtt,
            "finalization_output_contract",
            return_value={"type": "object"},
        ):
            gtt.finalization_validate_route(
                self.root,
                public_input,
                context,
                {
                    "typed_exit": "publication_review_stale",
                    "consumer": gtt.FINALIZATION_CONSUMERS[
                        "publication_review_stale"
                    ],
                    "output": {
                        "exit_id": "publication_review_stale",
                        "task_ref": public_input["task_ref"],
                        "branch_review_commit": self.head,
                        "stale_reason": "publication_review_missing",
                    },
                },
            )

    def test_published_route_requires_current_verification_before_committed_recovery(
        self,
    ) -> None:
        task_ref = self.task_dir.relative_to(self.root).as_posix()
        archive_ref = ".trellis/tasks/archive/2026-07/07-11-closeout"
        plan_ref = f"closeout-plan:{'b' * 64}"
        public_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": task_ref,
            "branch_review_commit": self.head,
            "pr_title": "#105 重构 finish-work 收尾事务",
            "pr_body": self.body,
        }
        marker_route = {
            "typed_exit": "published",
            "consumer": gtt.FINALIZATION_CONSUMERS["published"],
            "output": gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
        }

        def context(
            state: str,
            verification: object = None,
            *,
            transition_complete: bool = False,
        ) -> dict[str, object]:
            return {
                "transaction_state": state,
                "published_transition_complete": transition_complete,
                "publication_status": "current",
                "publication_stale_reason": None,
                "plan_ref": plan_ref,
                "plan": {
                    "marketplace": {"required": True},
                    "git": {
                        "repo": "owner/repo",
                        "branch_review_commit": self.head,
                    },
                    "task": {
                        "active_locator": task_ref,
                        "archive_locator": archive_ref,
                    },
                },
                "verification": verification,
            }

        checked_evidence = ({}, {"typed_exit": "verified"})
        not_required_evidence = ({}, {"typed_exit": "not_required"})
        pre_archive_states = [
            "prepared",
            "content_pushed",
            "evidence_ready",
            "draft_bound",
            "projection_validated",
            "archive_moved",
            "reprepare_required",
        ]
        for state in pre_archive_states:
            with self.subTest(state=state), self.assertRaises(gtt.WorkflowError):
                gtt.finalization_validate_route(
                    self.root,
                    public_input,
                    context(state),
                    marker_route,
                )
        for evidence in [checked_evidence, not_required_evidence]:
            with self.subTest(evidence=evidence[1]["typed_exit"]):
                gtt.finalization_validate_route(
                    self.root,
                    public_input,
                    context("evidence_ready", evidence),
                    marker_route,
                    allow_pending_transition=True,
                )
        with self.assertRaises(gtt.WorkflowError):
            gtt.finalization_validate_route(
                self.root,
                public_input,
                context("archived"),
                marker_route,
            )
        gtt.finalization_validate_route(
            self.root,
            public_input,
            context("ready", transition_complete=True),
            marker_route,
        )

        early_public_route = {
            **marker_route,
            "output": {
                "exit_id": "published",
                "task_ref": task_ref,
                "pr_number": 118,
                "pr_url": "https://github.com/owner/repo/pull/118",
            },
        }
        with self.assertRaisesRegex(
            gtt.WorkflowError,
            "persisted published route",
        ):
            gtt.finalization_validate_route(
                self.root,
                public_input,
                context("evidence_ready", checked_evidence),
                early_public_route,
                allow_pending_transition=True,
            )

    def test_published_route_skips_verification_for_non_extension_plan(self) -> None:
        task_ref = self.task_dir.relative_to(self.root).as_posix()
        public_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": task_ref,
            "branch_review_commit": self.head,
            "pr_title": "#105 重构 finish-work 收尾事务",
            "pr_body": self.body,
        }
        context = {
            "transaction_state": "prepared",
            "published_transition_complete": False,
            "publication_status": "current",
            "publication_stale_reason": None,
            "plan_ref": f"closeout-plan:{'b' * 64}",
            "plan": {
                "marketplace": {"required": False},
                "git": {
                    "repo": "owner/repo",
                    "branch_review_commit": self.head,
                },
                "task": {
                    "active_locator": task_ref,
                    "archive_locator": ".trellis/tasks/archive/2026-07/07-11-closeout",
                },
            },
            "verification": None,
        }
        gtt.finalization_validate_route(
            self.root,
            public_input,
            context,
            {
                "typed_exit": "published",
                "consumer": gtt.FINALIZATION_CONSUMERS["published"],
                "output": gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
            },
            allow_pending_transition=True,
        )

    def test_finalization_route_validates_empty_and_malformed_selected_exit_output(
        self,
    ) -> None:
        task_ref = self.task_dir.relative_to(self.root).as_posix()
        plan_ref = f"closeout-plan:{'b' * 64}"
        public_input = {
            "profile": "same_plan_resume",
            "mode": "workflow",
            "task_ref": task_ref,
        }
        context = {
            "transaction_state": "draft_bound",
            "published_transition_complete": False,
            "publication_status": "current",
            "publication_stale_reason": None,
            "plan_ref": plan_ref,
            "plan": {
                "marketplace": {"required": True},
                "git": {"branch_review_commit": self.head},
            },
            "verification": None,
        }
        resume_schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["exit_id", "task_ref", "plan_ref"],
            "properties": {
                "exit_id": {"const": "resume_finalization"},
                "task_ref": {"type": "string", "minLength": 1},
                "plan_ref": {"type": "string", "minLength": 1},
            },
        }
        invalid_outputs = [
            {},
            {"exit_id": "resume_finalization", "task_ref": task_ref},
            {
                "exit_id": "resume_finalization",
                "task_ref": task_ref,
                "plan_ref": plan_ref,
                "extra": "not-closed",
            },
            {
                "exit_id": "blocked",
                "task_ref": task_ref,
                "plan_ref": plan_ref,
            },
        ]
        with mock.patch.object(
            gtt,
            "finalization_output_contract",
            return_value=resume_schema,
        ):
            for output in invalid_outputs:
                with self.subTest(output=output), self.assertRaises(gtt.WorkflowError):
                    gtt.finalization_validate_route(
                        self.root,
                        public_input,
                        context,
                        {
                            "typed_exit": "resume_finalization",
                            "consumer": gtt.FINALIZATION_CONSUMERS[
                                "resume_finalization"
                            ],
                            "output": output,
                        },
                    )

        with self.assertRaises(gtt.WorkflowError):
            gtt.finalization_validate_route(
                self.root,
                public_input,
                {**context, "transaction_state": "prepared"},
                {
                    "typed_exit": "verification_required",
                    "consumer": gtt.FINALIZATION_CONSUMERS[
                        "verification_required"
                    ],
                    "output": gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
                },
            )

    def test_published_executor_marker_is_private_and_materialized_to_public_dto(
        self,
    ) -> None:
        task_ref = self.task_dir.relative_to(self.root).as_posix()
        plan_ref = f"closeout-plan:{'b' * 64}"
        public_input = {
            "profile": "verification_verified",
            "mode": "workflow",
            "task_ref": task_ref,
            "plan_ref": plan_ref,
            "branch_review_commit": self.head,
            "publication_head": self.head,
            "verification_ref": "extension-verification:current",
        }
        context = {
            "transaction_state": "evidence_ready",
            "published_transition_complete": False,
            "publication_status": "current",
            "publication_stale_reason": None,
            "plan_ref": plan_ref,
            "plan": {
                "marketplace": {"required": True},
                "git": {
                    "repo": "owner/repo",
                    "branch_review_commit": self.head,
                },
                "task": {
                    "active_locator": task_ref,
                    "archive_locator": (
                        ".trellis/tasks/archive/2026-07/07-11-closeout"
                    ),
                },
            },
            "verification": ({}, {"typed_exit": "verified"}),
        }
        route = {
            "typed_exit": "published",
            "consumer": gtt.FINALIZATION_CONSUMERS["published"],
            "output": gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
        }
        with mock.patch.object(
            gtt,
            "finalization_output_contract",
            side_effect=AssertionError("pre-materialization must not validate a public DTO"),
        ):
            gtt.finalization_validate_route(
                self.root,
                public_input,
                context,
                route,
                allow_pending_transition=True,
            )

        published_schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["exit_id", "task_ref", "pr_number", "pr_url"],
            "properties": {
                "exit_id": {"const": "published"},
                "task_ref": {"type": "string", "minLength": 1},
                "pr_number": {"type": "integer", "minimum": 1},
                "pr_url": {"type": "string", "minLength": 1},
            },
        }
        gate = {"route": route}
        archive_ref = ".trellis/tasks/archive/2026-07/07-11-closeout"
        archive_dir = self.root / archive_ref
        archive_dir.mkdir(parents=True)
        plan = {
            "git": {"repo": "owner/repo"},
            "task": {"archive_locator": archive_ref},
        }
        with mock.patch.object(
            gtt,
            "finalization_output_contract",
            return_value=published_schema,
        ):
            materialized = gtt.finalization_gate_with_published_output(
                self.root,
                archive_dir,
                gate,
                plan,
                {
                    "number": 118,
                    "url": "https://github.com/owner/repo/pull/118",
                },
            )
        self.assertEqual(
            materialized["route"]["output"],
            {
                "exit_id": "published",
                "task_ref": archive_ref,
                "pr_number": 118,
                "pr_url": "https://github.com/owner/repo/pull/118",
            },
        )

    def test_public_wrapper_materializes_only_terminal_published_marker(self) -> None:
        task_ref = self.task_dir.relative_to(self.root).as_posix()
        archive_ref = ".trellis/tasks/archive/2026-07/07-11-closeout"
        archive_dir = self.root / archive_ref
        archive_dir.mkdir(parents=True)
        gtt.write_json(archive_dir / "task.json", self.task)
        plan_ref = f"closeout-plan:{'b' * 64}"
        public_input = {
            "profile": "verification_verified",
            "mode": "workflow",
            "task_ref": task_ref,
            "plan_ref": plan_ref,
            "branch_review_commit": self.head,
            "publication_head": self.head,
            "verification_ref": "extension-verification:current",
        }
        plan = {
            "marketplace": {"required": True},
            "git": {
                "repo": "owner/repo",
                "remote": "origin",
                "head_branch": "main",
                "branch_review_commit": self.head,
            },
            "task": {
                "active_locator": task_ref,
                "archive_locator": archive_ref,
            },
        }
        gate = {
            "route": {
                "typed_exit": "published",
                "consumer": gtt.FINALIZATION_CONSUMERS["published"],
                "output": gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
            }
        }
        published_schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["exit_id", "task_ref", "pr_number", "pr_url"],
            "properties": {
                "exit_id": {"const": "published"},
                "task_ref": {"type": "string", "minLength": 1},
                "pr_number": {"type": "integer", "minimum": 1},
                "pr_url": {"type": "string", "minLength": 1},
            },
        }
        pr = {
            "number": 118,
            "url": "https://github.com/owner/repo/pull/118",
        }
        executor = mock.Mock(
            side_effect=AssertionError("public wrapper must not execute transitions")
        )

        def invoke(context: dict[str, object]) -> dict[str, object]:
            with (
                mock.patch.object(
                    gtt,
                    "stage0_invocation_identity",
                    return_value=(gtt.FINALIZE_TASK_SKILL_ID, self.root),
                ),
                mock.patch.object(gtt, "stage0_public_interface", return_value={}),
                mock.patch.object(gtt, "stage0_repo_root", return_value=self.root),
                mock.patch.object(
                    gtt,
                    "stage0_structured_input",
                    return_value=public_input,
                ),
                mock.patch.object(
                    gtt,
                    "finalization_gate_input",
                    return_value=(gate, archive_dir / gtt.TASK_FINALIZATION_GATE_ARTIFACT),
                ),
                mock.patch.object(
                    gtt,
                    "check_finalization_gate_result",
                    return_value=(gate, context),
                ),
                mock.patch.object(
                    gtt,
                    "stage0_output_contract",
                    return_value=(published_schema, {}),
                ),
                mock.patch.object(
                    gtt,
                    "finalization_output_contract",
                    return_value=published_schema,
                ),
                mock.patch.object(
                    gtt,
                    "cmd_execute_finalization_transition",
                    executor,
                ),
            ):
                return gtt.cmd_invoke_stage0_skill(
                    argparse.Namespace(input="unused.json", owner_result=None)
                )

        early_context = {
            "task_dir": self.task_dir,
            "transaction_state": "evidence_ready",
            "published_transition_complete": False,
            "published_pr": None,
            "publication_status": "current",
            "publication_stale_reason": None,
            "plan_ref": plan_ref,
            "plan": plan,
            "verification": ({}, {"typed_exit": "verified"}),
        }
        discovery_checkpoint = gtt.ai_first_owner_checkpoint_path(
            self.root,
            self.task_dir,
            gtt.CONTEXT_DISCOVERY_RECOVERY_ARTIFACT,
        )
        discovery_package = (
            Path(gtt.__file__).resolve().parents[4]
            / "skills/guru-team/packages/guru-discover-change-context"
        )
        discovery_result = json.loads(
            (
                discovery_package
                / "examples/change-context-owner-result.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            gtt.context_record_recovery_checkpoint(
                self.root,
                self.task_dir,
                discovery_result,
                "interrupted-discovery-owner",
            ),
            discovery_checkpoint,
        )
        with self.assertRaises(gtt.WorkflowError):
            invoke(early_context)
        self.assertTrue(discovery_checkpoint.is_file())

        finalization_checkpoint = gtt.ai_first_owner_checkpoint_path(
            self.root,
            archive_dir,
            gtt.TASK_FINALIZATION_GATE_ARTIFACT,
        )
        publication_checkpoint = gtt.ai_first_owner_checkpoint_path(
            self.root,
            archive_dir,
            gtt.PR_READINESS_ARTIFACT,
        )
        gtt.write_json(finalization_checkpoint, {"owner": "finalizer"})
        gtt.write_json(publication_checkpoint, {"owner": "publication"})
        other_task = self.root / ".trellis/tasks/08-07-other-task"
        other_task.mkdir(parents=True)
        gtt.write_json(other_task / "task.json", {"id": "other-task"})
        other_checkpoint = gtt.ai_first_owner_checkpoint_path(
            self.root,
            other_task,
            gtt.CONTEXT_DISCOVERY_RECOVERY_ARTIFACT,
        )
        gtt.write_json(other_checkpoint, {"owner": "other-task"})
        terminal_context = {
            **early_context,
            "task_dir": archive_dir,
            "transaction_state": "ready",
            "published_transition_complete": True,
            "published_pr": pr,
        }
        self.assertEqual(
            invoke(terminal_context),
            {
                "exit_id": "published",
                "task_ref": archive_ref,
                "pr_number": 118,
                "pr_url": pr["url"],
            },
        )
        executor.assert_not_called()
        self.assertFalse(finalization_checkpoint.exists())
        self.assertFalse(publication_checkpoint.exists())
        self.assertFalse(discovery_checkpoint.exists())
        self.assertFalse(finalization_checkpoint.parent.exists())
        self.assertTrue(other_checkpoint.is_file())

    def test_verification_required_binds_repo_to_immutable_plan(self) -> None:
        task_ref = self.task_dir.relative_to(self.root).as_posix()
        plan_ref = f"closeout-plan:{'b' * 64}"
        public_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": task_ref,
            "branch_review_commit": self.head,
            "pr_title": "#105 重构 finish-work 收尾事务",
            "pr_body": self.body,
        }
        context = {
            "transaction_state": "prepared",
            "published_transition_complete": False,
            "publication_status": "current",
            "publication_stale_reason": None,
            "plan_ref": plan_ref,
            "plan": {
                "marketplace": {"required": True},
                "git": {
                    "repo": "owner/repo",
                    "branch_review_commit": self.head,
                },
            },
            "verification": None,
        }
        route = {
            "typed_exit": "verification_required",
            "consumer": gtt.FINALIZATION_CONSUMERS["verification_required"],
            "output": {
                "exit_id": "verification_required",
                "task_ref": task_ref,
                "plan_ref": plan_ref,
                "repo_ref": "other/repo",
                "branch_review_commit": self.head,
                "verification_target": "extension-installation",
            },
        }
        with mock.patch.object(
            gtt,
            "finalization_output_contract",
            return_value={"type": "object"},
        ):
            with self.assertRaises(gtt.WorkflowError):
                gtt.finalization_validate_route(
                    self.root,
                    public_input,
                    context,
                    route,
                    allow_pending_transition=True,
                )
            route["output"]["repo_ref"] = "owner/repo"
            gtt.finalization_validate_route(
                self.root,
                public_input,
                context,
                route,
                allow_pending_transition=True,
            )
            with self.assertRaises(gtt.WorkflowError):
                gtt.finalization_validate_route(
                    self.root,
                    public_input,
                    context,
                    route,
                )

    def test_resume_finalization_accepts_only_legal_same_plan_recovery_states(
        self,
    ) -> None:
        task_ref = self.task_dir.relative_to(self.root).as_posix()
        plan_ref = f"closeout-plan:{'b' * 64}"
        public_input = {
            "profile": "same_plan_resume",
            "mode": "workflow",
            "task_ref": task_ref,
        }
        route = {
            "typed_exit": "resume_finalization",
            "consumer": gtt.FINALIZATION_CONSUMERS["resume_finalization"],
            "output": {
                "exit_id": "resume_finalization",
                "task_ref": task_ref,
                "plan_ref": plan_ref,
            },
        }

        def context(state: str, verification: object = None) -> dict[str, object]:
            return {
                "transaction_state": state,
                "published_transition_complete": False,
                "publication_status": "current",
                "publication_stale_reason": None,
                "plan_ref": plan_ref,
                "plan": {
                    "marketplace": {"required": True},
                    "git": {
                        "repo": "owner/repo",
                        "branch_review_commit": self.head,
                    },
                },
                "verification": verification,
            }

        with mock.patch.object(
            gtt,
            "finalization_output_contract",
            return_value={"type": "object"},
        ):
            for state in sorted(gtt.FINALIZATION_RESUME_RECOVERY_STATES):
                verification = (
                    ({}, {"typed_exit": "verified"})
                    if state == "content_pushed"
                    else None
                )
                with self.subTest(legal_state=state):
                    gtt.finalization_validate_route(
                        self.root,
                        public_input,
                        context(state, verification),
                        route,
                    )
            for state in ["prepared", "reprepare_required", "ready"]:
                with self.subTest(illegal_state=state), self.assertRaises(
                    gtt.WorkflowError
                ):
                    gtt.finalization_validate_route(
                        self.root,
                        public_input,
                        context(state),
                        route,
                    )
            with self.assertRaises(gtt.WorkflowError):
                gtt.finalization_validate_route(
                    self.root,
                    public_input,
                    context("content_pushed"),
                    route,
                )

    def install_official_config_parser(self) -> Path:
        source = Path(__file__).resolve().parents[5] / ".trellis/scripts/common"
        target = self.root / ".trellis/scripts/common"
        shutil.copytree(source, target)
        return self.root / ".trellis/config.yaml"

    def test_after_archive_hook_preflight_allows_missing_and_empty_configuration(self) -> None:
        self.assertEqual(gtt.official_after_archive_hook_state(self.root), {"commands": []})
        config = self.install_official_config_parser()
        for content in [
            "session_auto_commit: false\n",
            "hooks:\n  after_archive:\n",
        ]:
            with self.subTest(content=content):
                config.write_text(content, encoding="utf-8")
                self.assertEqual(
                    gtt.official_after_archive_hook_state(self.root),
                    {"commands": []},
                )

    def test_after_archive_hook_preflight_rejects_nonempty_or_unparseable_without_execution(self) -> None:
        config = self.install_official_config_parser()
        sentinel = self.root / "after-archive-hook-sentinel"
        cases = {
            "nonempty": f"hooks:\n  after_archive:\n    - \"touch {sentinel}\"\n",
            "top-level": f"hooks:\nafter_archive:\n  - \"touch {sentinel}\"\n",
            "duplicate": (
                f"hooks:\n  after_archive:\n    - \"touch {sentinel}\"\n"
                "  after_archive:\n"
            ),
            "scalar": f"hooks:\n  after_archive: \"touch {sentinel}\"\n",
            "nul": "hooks:\n  after_archive:\n\x00",
        }
        for case, content in cases.items():
            with self.subTest(case=case):
                config.write_bytes(content.encode("utf-8"))
                with self.assertRaises(gtt.WorkflowError):
                    gtt.official_after_archive_hook_state(self.root)
                self.assertFalse(sentinel.exists())

    def test_after_archive_hook_preflight_rejects_config_symlink_without_execution(self) -> None:
        config = self.install_official_config_parser()
        target = self.root / "outside-config.yaml"
        sentinel = self.root / "after-archive-hook-sentinel"
        target.write_text(
            f"hooks:\n  after_archive:\n    - \"touch {sentinel}\"\n",
            encoding="utf-8",
        )
        config.symlink_to(target)
        with self.assertRaises(gtt.WorkflowError):
            gtt.official_after_archive_hook_state(self.root)
        self.assertFalse(sentinel.exists())
        config.unlink()
        config.symlink_to(self.root / "missing-outside-config.yaml")
        with self.assertRaises(gtt.WorkflowError):
            gtt.official_after_archive_hook_state(self.root)
        self.assertFalse(sentinel.exists())

    def test_closeout_plan_is_canonical_schema_valid_and_digest_stable(self) -> None:
        first = self.build_plan()
        second = self.build_plan()
        self.assertEqual(first, second)
        self.assertEqual(gtt.closeout_plan_errors(first), [])
        self.assertEqual(first["plan_digest"], gtt.closeout_plan_digest(first))
        self.assertTrue(first["publish"]["draft"])
        self.assertEqual(first["transitions"], gtt.CLOSEOUT_TRANSITIONS)
        serialized = json.dumps(first, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.assertNotIn(str(self.root), serialized)
        self.assertEqual(
            first["marketplace"]["verifier_artifact_locator"],
            gtt.MARKETPLACE_VERIFICATION_ARTIFACT,
        )
        self.assertEqual(
            first["projection"]["summary_template_sha256"],
            gtt.closeout_json_artifact_sha256(first["projection"]["summary_template"]),
        )
        self.assertEqual(
            first["projection"]["untracked_archive_outputs"],
            [
                gtt.CLOSEOUT_PLAN_ARTIFACT,
                gtt.FINISH_SUMMARY_ARTIFACT,
                gtt.MARKETPLACE_VERIFICATION_ARTIFACT,
            ],
        )
        self.assertEqual(
            set(first["projection"]),
            {
                "active_locator",
                "archive_locator",
                "finish_summary_locator",
                "move_paths",
                "tracked_move_paths",
                "untracked_archive_outputs",
                "reviewed_tracked_bindings",
                "migration_predecessor_plan_digest",
                "summary_placeholder",
                "summary_template_sha256",
                "summary_template",
                "runtime_fact_fields",
            },
        )
        if importlib.util.find_spec("jsonschema") is not None:
            from jsonschema import Draft202012Validator

            schema = gtt.read_json(
                Path(__file__).resolve().parents[2] / "schemas/closeout-plan.schema.json"
            )
            self.assertEqual(list(Draft202012Validator(schema).iter_errors(first)), [])

    def test_migrated_schema2_plan_reclassifies_live_index_and_binds_metadata_tail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=root, check=True)
            task_dir = root / ".trellis/tasks/08-03-migrated"
            task_dir.mkdir(parents=True)
            task = {
                "id": "migrated",
                "name": "migrated",
                "title": "#105 migrated closeout",
                "status": "in_progress",
                "base_branch": "main",
            }
            context = {
                "task_artifact_dir": ".trellis/tasks/08-03-migrated",
                "base_branch": "main",
                "base_ref": "HEAD",
                "branch_name": "main",
            }
            gtt.write_json(task_dir / "task.json", task)
            gtt.write_json(task_dir / "issue-scope-ledger.json", self.ledger)
            gtt.write_json(task_dir / "finish-summary-index.json", self.index)
            migrated_body = valid_pr_body("migrated closeout。")
            (task_dir / "pr-body.md").write_text(migrated_body, encoding="utf-8")
            for name in ("prd.md", "design.md", "implement.md", "context-discovery.json"):
                (task_dir / name).write_text(f"base {name}\n", encoding="utf-8")
            (task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT).write_text("{}\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "reviewed metadata"], cwd=root, check=True)
            review_commit = gtt.current_head(root)

            (task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT).unlink()
            (task_dir / "prd.md").write_text("reviewed metadata tail\n", encoding="utf-8")
            (task_dir / "context-discovery.json").write_text(
                "reviewed discovery metadata tail\n", encoding="utf-8"
            )
            current = gtt.build_closeout_plan(
                root,
                task_dir,
                context,
                task,
                self.ledger,
                repo="owner/repo",
                remote="origin",
                base_branch="main",
                head_branch="main",
                branch_review_commit=review_commit,
                title="#105 migrated closeout",
                body=migrated_body,
                review_facts={"changed_paths": [], "marketplace_required": False},
            )
            legacy = self.legacy_plan_from_current(current, body=migrated_body)
            gtt.write_json(task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, legacy)

            normalized = gtt.build_closeout_plan(
                root,
                task_dir,
                context,
                task,
                self.ledger,
                repo="owner/repo",
                remote="origin",
                base_branch="main",
                head_branch="main",
                branch_review_commit=review_commit,
                title="#105 migrated closeout",
                body=migrated_body,
                review_facts={"changed_paths": [], "marketplace_required": False},
            )
            self.assertEqual(gtt.closeout_schema2_migration_errors(legacy, normalized), [])
            self.assertEqual(
                normalized["projection"]["migration_predecessor_plan_digest"],
                legacy["plan_digest"],
            )
            self.assertIn(
                gtt.CLOSEOUT_PLAN_ARTIFACT,
                normalized["projection"]["tracked_move_paths"],
            )
            self.assertEqual(
                normalized["projection"]["untracked_archive_outputs"],
                [gtt.FINISH_SUMMARY_ARTIFACT],
            )
            bindings = {
                item["path"]: item
                for item in normalized["projection"]["reviewed_tracked_bindings"]
            }
            self.assertIn("prd.md", bindings)
            self.assertIn("context-discovery.json", bindings)
            self.assertNotIn(gtt.CLOSEOUT_PLAN_ARTIFACT, bindings)
            self.assertIn(
                "context-discovery.json",
                gtt.closeout_archive_pruned_paths(normalized),
            )

            gtt.write_json(task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, normalized)
            summary = gtt.closeout_summary_for_pr(
                normalized,
                {"number": 105, "url": "https://github.com/owner/repo/pull/105"},
            )
            gtt.write_json(task_dir / gtt.FINISH_SUMMARY_ARTIFACT, summary)
            gtt.validate_closeout_pre_move_continuity(
                root,
                task_dir,
                normalized,
                review_commit,
                expected_summary_pr={
                    "number": 105,
                    "url": "https://github.com/owner/repo/pull/105",
                },
            )
            self.assertEqual(
                gtt.finalization_uncommitted_output_paths(root, normalized),
                set(gtt.git_status_paths(root)),
            )

            original = (task_dir / "prd.md").read_bytes()
            (task_dir / "prd.md").write_bytes(original + b"drift\n")
            with self.assertRaisesRegex(gtt.WorkflowError, "reviewed binding"):
                gtt.validate_closeout_pre_move_continuity(
                    root, task_dir, normalized, review_commit
                )
            (task_dir / "prd.md").write_bytes(original)
            (task_dir / "prd.md").chmod(0o755)
            with self.assertRaisesRegex(gtt.WorkflowError, "reviewed binding"):
                gtt.validate_closeout_pre_move_continuity(
                    root, task_dir, normalized, review_commit
                )
            (task_dir / "prd.md").chmod(0o644)

            (task_dir / "prd.md").write_text(
                "a later unreviewed metadata tail\n", encoding="utf-8"
            )
            rebuilt_after_drift = gtt.build_closeout_plan(
                root,
                task_dir,
                context,
                task,
                self.ledger,
                repo="owner/repo",
                remote="origin",
                base_branch="main",
                head_branch="main",
                branch_review_commit=review_commit,
                title="#105 migrated closeout",
                body=migrated_body,
                review_facts={"changed_paths": [], "marketplace_required": False},
            )
            self.assertEqual(
                gtt.closeout_schema2_migration_errors(
                    normalized, rebuilt_after_drift
                ),
                ["schema 2.0 migration requires one legacy plan"],
            )
            (task_dir / "prd.md").write_bytes(original)
            gtt.validate_closeout_pre_move_continuity(
                root,
                task_dir,
                normalized,
                review_commit,
                expected_summary_pr={
                    "number": 105,
                    "url": "https://github.com/owner/repo/pull/105",
                },
            )
            gtt.compact_closeout_archive(task_dir, normalized)
            self.assertFalse((task_dir / "context-discovery.json").exists())
            self.assertTrue((task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT).is_file())
            self.assertTrue((task_dir / gtt.FINISH_SUMMARY_ARTIFACT).is_file())

    def test_migration_verification_plan_ref_is_exact_and_reprepare_retires_it(
        self,
    ) -> None:
        plan = self.build_plan()
        predecessor_digest = "c" * 64
        projection = plan["projection"]
        projection["tracked_move_paths"] = sorted(
            projection["tracked_move_paths"]
            + [gtt.MARKETPLACE_VERIFICATION_ARTIFACT]
        )
        projection["untracked_archive_outputs"] = [
            path
            for path in projection["untracked_archive_outputs"]
            if path != gtt.MARKETPLACE_VERIFICATION_ARTIFACT
        ]
        projection["reviewed_tracked_bindings"] = [
            {
                "path": gtt.MARKETPLACE_VERIFICATION_ARTIFACT,
                "mode": "100644",
                "sha256": "d" * 64,
            }
        ]
        projection["migration_predecessor_plan_digest"] = predecessor_digest
        plan["plan_digest"] = gtt.closeout_plan_digest(plan)
        gtt.validate_closeout_plan(plan)

        current_ref = f"closeout-plan:{plan['plan_digest']}"
        predecessor_ref = f"closeout-plan:{predecessor_digest}"
        unrelated_ref = f"closeout-plan:{'e' * 64}"
        self.assertTrue(gtt.closeout_verification_plan_ref_matches(plan, current_ref))
        self.assertTrue(
            gtt.closeout_verification_plan_ref_matches(plan, predecessor_ref)
        )
        self.assertFalse(
            gtt.closeout_verification_plan_ref_matches(plan, unrelated_ref)
        )
        self.assertFalse(
            gtt.closeout_verification_plan_ref_matches(plan, "closeout-plan:invalid")
        )

        task_ref = plan["task"]["active_locator"]
        verification_ref = "extension-verification:exact-predecessor"
        owner_input = {
            "profile": "workflow_verification",
            "mode": "workflow",
            "task_ref": task_ref,
            "plan_ref": predecessor_ref,
            "branch_review_commit": plan["git"]["branch_review_commit"],
            "repo_ref": plan["git"]["repo"],
        }
        payload = {
            "public_input": owner_input,
            "typed_exit": "verified",
            "mode": "workflow",
            "identity": {"verification_ref": verification_ref},
            "target_repository": {},
        }
        locator = f"{task_ref}/{gtt.MARKETPLACE_VERIFICATION_ARTIFACT}"
        with (
            mock.patch.dict(os.environ, {"GURU_TEAM_EVAL_STAGING": "1"}),
            mock.patch.object(
                gtt,
                "extension_verification_payload_errors",
                return_value=[],
            ),
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "validate_closeout_reviewed_content"),
            mock.patch.object(
                gtt,
                "finalization_uncommitted_output_paths",
                return_value=set(),
            ),
            mock.patch.object(gtt, "git_status_paths", return_value=[]),
        ):
            checked = gtt.check_extension_verification_for_closeout(
                self.root,
                self.task_dir,
                payload,
                locator,
                plan=plan,
                task_ref=task_ref,
                plan_ref=current_ref,
                branch_review_commit=plan["git"]["branch_review_commit"],
            )
            self.assertEqual(checked["typed_exit"], "verified")
            payload["public_input"]["plan_ref"] = unrelated_ref
            with self.assertRaises(gtt.WorkflowError):
                gtt.check_extension_verification_for_closeout(
                    self.root,
                    self.task_dir,
                    payload,
                    locator,
                    plan=plan,
                    task_ref=task_ref,
                    plan_ref=current_ref,
                    branch_review_commit=plan["git"]["branch_review_commit"],
                )

        payload["public_input"]["plan_ref"] = predecessor_ref
        public_input = {
            "profile": "verification_verified",
            "mode": "workflow",
            "task_ref": task_ref,
            "plan_ref": current_ref,
            "branch_review_commit": plan["git"]["branch_review_commit"],
            "publication_head": plan["git"].get(
                "publication_head",
                plan["git"]["branch_review_commit"],
            ),
            "verification_ref": verification_ref,
        }
        direct_failure = gtt.WorkflowError("stale direct checker", exit_code=2)
        with (
            mock.patch.object(
                gtt,
                "finalization_verification_owner_payload",
                return_value=(payload, locator),
            ),
            mock.patch.object(
                gtt,
                "check_extension_verification_result",
                side_effect=direct_failure,
            ),
            mock.patch.object(gtt, "finalization_closeout_plan", return_value=plan),
            mock.patch.object(
                gtt,
                "check_extension_verification_for_closeout",
                return_value=checked,
            ),
        ):
            recovered = gtt.finalization_verification_owner_result(
                self.root,
                self.task_dir,
                public_input,
            )
            self.assertEqual(recovered, (payload, checked))
            payload["public_input"]["plan_ref"] = unrelated_ref
            with self.assertRaises(gtt.WorkflowError):
                gtt.finalization_verification_owner_result(
                    self.root,
                    self.task_dir,
                    public_input,
                )

        payload["public_input"]["plan_ref"] = predecessor_ref
        with (
            mock.patch.object(
                gtt,
                "finalization_verification_owner_payload",
                return_value=(payload, locator),
            ),
            mock.patch.object(
                gtt,
                "check_extension_verification_result",
                return_value=checked,
            ),
        ):
            self.assertEqual(
                gtt.finalization_current_verification_owner_result(
                    self.root,
                    self.task_dir,
                    task_ref=task_ref,
                    plan_ref=current_ref,
                    branch_review_commit=plan["git"]["branch_review_commit"],
                    plan=plan,
                ),
                (payload, checked),
            )
            payload["public_input"]["plan_ref"] = unrelated_ref
            self.assertIsNone(
                gtt.finalization_current_verification_owner_result(
                    self.root,
                    self.task_dir,
                    task_ref=task_ref,
                    plan_ref=current_ref,
                    branch_review_commit=plan["git"]["branch_review_commit"],
                    plan=plan,
                )
            )

        without_binding = copy.deepcopy(plan)
        without_binding["projection"]["reviewed_tracked_bindings"] = []
        without_binding["plan_digest"] = gtt.closeout_plan_digest(without_binding)
        self.assertFalse(
            gtt.closeout_verification_plan_ref_matches(
                without_binding,
                predecessor_ref,
            )
        )

        old_locator = plan["task"]["archive_locator"]
        old_month = old_locator.split("/")[3]
        new_month = "2099-12" if old_month != "2099-12" else "2099-11"
        new_locator = old_locator.replace(f"/{old_month}/", f"/{new_month}/")

        def replace_archive_locator(value: object) -> object:
            if isinstance(value, dict):
                return {
                    key: replace_archive_locator(item)
                    for key, item in value.items()
                }
            if isinstance(value, list):
                return [replace_archive_locator(item) for item in value]
            if isinstance(value, str):
                return value.replace(old_locator, new_locator)
            return value

        reprepared = replace_archive_locator(copy.deepcopy(plan))
        assert isinstance(reprepared, dict)
        reprepared["projection"]["migration_predecessor_plan_digest"] = None
        reprepared["projection"]["summary_template_sha256"] = (
            gtt.closeout_json_artifact_sha256(
                reprepared["projection"]["summary_template"]
            )
        )
        reprepared["plan_digest"] = gtt.closeout_plan_digest(reprepared)
        gtt.validate_closeout_plan(reprepared)
        self.assertEqual(gtt.closeout_month_supersession_errors(plan, reprepared), [])
        self.assertFalse(
            gtt.closeout_verification_plan_ref_matches(
                reprepared,
                predecessor_ref,
            )
        )

    def test_migrated_schema2_active_resume_reuses_existing_draft_without_branch_review(
        self,
    ) -> None:
        current = self.build_plan()
        normalized = copy.deepcopy(current)
        normalized["projection"]["tracked_move_paths"] = sorted(
            normalized["projection"]["tracked_move_paths"]
            + [gtt.CLOSEOUT_PLAN_ARTIFACT]
        )
        normalized["projection"]["untracked_archive_outputs"] = [
            path
            for path in normalized["projection"]["untracked_archive_outputs"]
            if path != gtt.CLOSEOUT_PLAN_ARTIFACT
        ]
        legacy = self.legacy_plan_from_current(normalized)
        normalized["projection"]["migration_predecessor_plan_digest"] = legacy[
            "plan_digest"
        ]
        normalized["plan_digest"] = gtt.closeout_plan_digest(normalized)
        gtt.validate_closeout_plan(normalized)
        self.assertEqual(gtt.closeout_schema2_migration_errors(legacy, normalized), [])

        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, normalized)
        gtt.write_json(
            self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT,
            gtt.closeout_summary_for_pr(
                normalized,
                {"number": 105, "url": "https://github.com/owner/repo/pull/105"},
            ),
        )
        gtt.write_json(self.task_dir / "task.json", {**self.task, "status": "completed"})
        draft = {
            **closeout_head_repository_fields(),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
            "title": normalized["publish"]["title"],
            "body": normalized["publish"]["body"],
            "headRefName": normalized["git"]["head_branch"],
            "baseRefName": normalized["git"]["base_branch"],
            "headRefOid": self.head,
            "isDraft": True,
        }
        archived = self.root / normalized["task"]["archive_locator"]
        args = finish_args(
            dry_run=False,
            expected_plan_digest=normalized["plan_digest"],
        )
        with (
            mock.patch.object(gtt, "validate_closeout_reviewed_content"),
            mock.patch.object(gtt, "validate_closeout_active_projection"),
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "require_gh_auth"),
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=draft),
            mock.patch.object(gtt, "validate_closeout_pull_request_identity"),
            mock.patch.object(
                gtt,
                "execute_archive_metadata_transaction",
                return_value=(archived, {"commit": self.head}),
            ) as archive,
            mock.patch.object(
                gtt,
                "ensure_closeout_pr_ready",
                return_value={"status": "ready", "pr": {**draft, "isDraft": False}},
            ) as ready,
            mock.patch.object(gtt, "create_pull_request") as create_pr,
            mock.patch.object(gtt, "cmd_review_branch") as review_branch,
            mock.patch.object(gtt, "cmd_check_review_gate") as check_review,
        ):
            result = gtt.resume_active_archive_move(
                self.root,
                args,
                {},
                self.task_dir,
                self.context,
            )

        self.assertEqual(result["stage"], "ready")
        archive.assert_called_once_with(
            self.root,
            self.task_dir,
            normalized,
            bound_pr=draft,
            verification_owner_result=None,
        )
        ready.assert_called_once_with(self.root, normalized, bound_pr=draft)
        create_pr.assert_not_called()
        review_branch.assert_not_called()
        check_review.assert_not_called()

    def test_final_summary_injects_only_plan_constrained_pr_runtime_facts(self) -> None:
        plan = self.build_plan()
        template = plan["projection"]["summary_template"]
        summary = gtt.closeout_summary_for_pr(
            plan,
            {"number": 105, "url": "https://github.com/owner/repo/pull/105"},
        )

        def changed_paths(left: object, right: object, prefix: str = "") -> set[str]:
            if isinstance(left, dict) and isinstance(right, dict):
                result: set[str] = set()
                for key in set(left) | set(right):
                    child = f"{prefix}.{key}" if prefix else str(key)
                    result.update(changed_paths(left.get(key), right.get(key), child))
                return result
            return set() if left == right else {prefix}

        self.assertEqual(
            changed_paths(template, summary),
            set(gtt.CLOSEOUT_SUMMARY_RUNTIME_FACT_FIELDS),
        )
        gtt.validate_closeout_final_summary(plan, summary)
        tampered = json.loads(json.dumps(summary, ensure_ascii=False))
        tampered["git"]["branch"] = "fix/tampered"
        with self.assertRaises(gtt.WorkflowError):
            gtt.validate_closeout_final_summary(plan, tampered)
        summary_path = self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT
        summary_path.write_text(json.dumps(summary, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(gtt.WorkflowError):
            gtt.read_and_validate_closeout_final_summary(summary_path, plan)
        gtt.write_json(summary_path, summary)
        self.assertEqual(gtt.read_and_validate_closeout_final_summary(summary_path, plan), summary)
        with self.assertRaises(gtt.WorkflowError):
            gtt.closeout_summary_for_pr(
                plan,
                {
                    "number": gtt.CLOSEOUT_PR_PLACEHOLDER_NUMBER + 1,
                    "url": f"https://github.com/owner/repo/pull/{gtt.CLOSEOUT_PR_PLACEHOLDER_NUMBER + 1}",
                },
            )

    def test_prepare_projection_failure_is_identical_for_dry_run_and_formal_before_side_effects(self) -> None:
        observed: list[dict[str, object]] = []
        for dry_run in [True, False]:
            args = finish_args(
                dry_run=dry_run,
                expected_plan_digest="a" * 64,
            )
            error = gtt.WorkflowError(
                "future summary projection invalid",
                exit_code=2,
                payload={"failed_stage": "prepare-final-summary-projection", "errors": ["schema"]},
            )
            with (
                mock.patch.object(gtt, "repo_root", return_value=self.root),
                mock.patch.object(gtt, "load_config", return_value={}),
                mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
                mock.patch.object(gtt, "load_task_runtime_identity", return_value=self.context),
                mock.patch.object(gtt, "assert_workspace_boundary"),
                mock.patch.object(gtt, "task_dir_is_archived", return_value=False),
                mock.patch.object(gtt, "prepare_closeout", side_effect=error),
                mock.patch.object(gtt, "require_gh_auth") as auth,
                mock.patch.object(gtt, "write_json") as write,
                mock.patch.object(gtt, "run_stdout") as mutation,
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_finish_work(args)
            observed.append(raised.exception.payload)
            auth.assert_not_called()
            write.assert_not_called()
            mutation.assert_not_called()
        self.assertEqual(observed[0], observed[1])

    def test_same_plan_preview_keeps_historical_verification_fail_closed(self) -> None:
        plan = self.build_plan()
        task_ref = plan["task"]["active_locator"]
        public_input = {
            "profile": "same_plan_resume",
            "mode": "workflow",
            "task_ref": task_ref,
            "plan_ref": f"closeout-plan:{plan['plan_digest']}",
        }
        prepared = {
            "plan": plan,
            "ledger": self.ledger,
            "gate": self.gate,
            "finalizer_takeover": None,
            "month_supersession": None,
        }
        args = argparse.Namespace(include_finalization_gate=True)
        stale_error = gtt.WorkflowError(
            "Extension verification evidence is not current for the immutable finalization plan.",
            exit_code=2,
        )
        with (
            mock.patch.object(
                gtt,
                "finalization_publication_owner_result",
                return_value={
                    "owner_status": "current",
                    "publication_ref": "publication:current",
                },
            ),
            mock.patch.object(gtt, "load_config", return_value={}),
            mock.patch.object(gtt, "task_dir_is_archived", return_value=False),
            mock.patch.object(
                gtt,
                "load_task_runtime_identity",
                return_value=self.context,
            ),
            mock.patch.object(gtt, "assert_workspace_boundary"),
            mock.patch.object(
                gtt,
                "task_json",
                return_value={**self.task, "status": "in_progress"},
            ),
            mock.patch.object(gtt, "prepare_closeout", return_value=prepared),
            mock.patch.object(
                gtt,
                "finalization_current_verification_owner_result",
                side_effect=stale_error,
            ) as rediscover,
        ):
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.finalization_preview_context(
                    self.root,
                    args,
                    public_input,
                )

        self.assertIs(raised.exception, stale_error)
        rediscover.assert_called_once()

    def test_archived_owner_results_use_committed_gate_without_readiness(self) -> None:
        plan = self.build_plan()
        public_input = {
            "profile": "same_plan_resume",
            "mode": "workflow",
            "task_ref": plan["task"]["active_locator"],
            "plan_ref": f"closeout-plan:{plan['plan_digest']}",
        }
        transaction = {"commit": self.head, "parent": "d" * 40}
        package_root = (
            Path(__file__).resolve().parents[5]
            / "trellis/skills/guru-team/packages/guru-finalize-task"
        )
        with (
            mock.patch.object(
                gtt,
                "task_publication_path",
                side_effect=AssertionError("archived readiness was reopened"),
            ),
            mock.patch.object(
                gtt,
                "finalization_package_root",
                return_value=package_root,
            ),
        ):
            publication, verification = gtt.finalization_archived_owner_results(
                self.root,
                plan,
                transaction,
                public_input,
            )

        self.assertEqual(publication, {"owner_status": "current"})
        self.assertIsNone(verification)

        with mock.patch.object(
            gtt,
            "closeout_commit_blob_bytes",
            side_effect=AssertionError("compact recovery reopened active-only evidence"),
        ):
            recovered = gtt.finalization_archived_owner_results(
                self.root,
                plan,
                transaction,
                {**public_input, "verification_ref": "extension-verification:other"},
            )
        self.assertEqual(recovered, ({"owner_status": "current"}, None))

    def test_archived_same_plan_transition_uses_committed_gate_and_only_marks_ready(
        self,
    ) -> None:
        plan = self.build_plan()
        body = self.body
        archived = self.root / plan["task"]["archive_locator"]
        shutil.rmtree(self.task_dir)
        archived.mkdir(parents=True)
        gtt.write_json(archived / gtt.CLOSEOUT_PLAN_ARTIFACT, plan)

        publication_ref = "publication:current reviewed result"
        verification_ref = "extension-verification:checked result / 当前"
        committed_gate = {
            "schema_version": "3.0",
            "skill_id": gtt.FINALIZE_TASK_SKILL_ID,
            "identity": {
                "task_ref": plan["task"]["active_locator"],
                "plan_ref": f"closeout-plan:{plan['plan_digest']}",
                "plan_digest": plan["plan_digest"],
                "branch_review_commit": plan["git"]["branch_review_commit"],
            },
            "review": {
                "status": "passed",
                "summary": "The committed archive authorizes the same plan.",
            },
            "route": {
                "typed_exit": "published",
                "consumer": gtt.FINALIZATION_CONSUMERS["published"],
                "output": gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
            },
        }
        committed_gate_path = archived / gtt.TASK_FINALIZATION_GATE_ARTIFACT
        gtt.write_json(committed_gate_path, committed_gate)

        subprocess.run(
            ["git", "init", "-q", "-b", "fix/105-closeout"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Finalization Recovery"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            [
                "git",
                "config",
                "user.email",
                "finalization-recovery@example.invalid",
            ],
            cwd=self.root,
            check=True,
        )
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-qm", "committed compact archive"],
            cwd=self.root,
            check=True,
        )
        archive_commit = gtt.current_head(self.root)
        committed_gate_bytes = committed_gate_path.read_bytes()

        public_input = {
            "profile": "same_plan_resume",
            "mode": "workflow",
            "task_ref": plan["task"]["active_locator"],
            "plan_ref": f"closeout-plan:{plan['plan_digest']}",
        }
        facts = {
            "task_ref": public_input["task_ref"],
            "profile": public_input["profile"],
            "mode": public_input["mode"],
            "plan_ref": public_input["plan_ref"],
            "plan_digest": plan["plan_digest"],
            "branch_review_commit": plan["git"]["branch_review_commit"],
            "archive_locator": plan["task"]["archive_locator"],
            "publication_ref": publication_ref,
            "verification_ref": verification_ref,
        }
        verification = (
            {"source": "committed-finalization-gate"},
            {
                "status": "ok",
                "typed_exit": "verified",
                "verification_ref": verification_ref,
            },
        )
        context = {
            "task_dir": archived,
            "task_context": None,
            "prepared": None,
            "plan": plan,
            "plan_ref": public_input["plan_ref"],
            "transaction_state": "archived",
            "published_transition_complete": False,
            "published_pr": None,
            "publication": {
                "owner_status": "current",
                "publication_ref": publication_ref,
            },
            "publication_status": "current",
            "publication_stale_reason": None,
            "verification": verification,
            "facts": facts,
            "current_facts_sha256": gtt.context_digest(facts),
        }
        reviewed = {
            "review": {
                "status": "passed",
                "summary": "The same committed transaction is ready to resume.",
            },
            "route": {
                "typed_exit": "published",
                "consumer": gtt.FINALIZATION_CONSUMERS["published"],
                "output": gtt.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
            },
        }
        transaction = {
            "commit": archive_commit,
            "parent": "d" * 40,
            "summary_pr": {
                "number": 166,
                "url": "https://github.com/owner/repo/pull/166",
            },
        }
        draft = {
            **closeout_head_repository_fields(),
            "number": 166,
            "url": "https://github.com/owner/repo/pull/166",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": plan["git"]["head_branch"],
            "baseRefName": plan["git"]["base_branch"],
            "headRefOid": archive_commit,
            "isDraft": True,
        }
        ready = dict(draft, isDraft=False)
        args = argparse.Namespace(
            root=str(self.root),
            input="unused-input.json",
            review_input="unused-review.json",
            gate=None,
            dry_run=False,
            include_finalization_gate=True,
        )
        source_root = Path(__file__).resolve().parents[5]
        package_root = (
            source_root
            / "trellis/skills/guru-team/packages/guru-finalize-task"
        )
        original_run = gtt.run
        ready_commands: list[list[str]] = []

        def run_with_ready(command: list[str], **kwargs: object) -> object:
            if command[:3] == ["gh", "pr", "ready"]:
                ready_commands.append(command)
                return mock.Mock(returncode=0, stdout="", stderr="")
            return original_run(command, **kwargs)

        def execute_archived(finish_args: argparse.Namespace) -> dict[str, object]:
            return gtt.resume_archived_closeout(
                self.root,
                finish_args,
                archived,
                committed_plan=plan,
                committed_archive=transaction,
            )

        with (
            mock.patch.object(
                gtt,
                "finalization_public_input",
                return_value=(public_input, "unused-input.json"),
            ),
            mock.patch.object(
                gtt,
                "finalization_semantic_review_input",
                return_value=reviewed,
            ),
            mock.patch.object(
                gtt,
                "finalization_preview_context",
                return_value=context,
            ),
            mock.patch.object(gtt, "finalization_task_dir", return_value=archived),
            mock.patch.object(
                gtt,
                "resolve_committed_closeout_archive_transaction",
                return_value=transaction,
            ),
            mock.patch.object(
                gtt,
                "finalization_package_root",
                return_value=package_root,
            ),
            mock.patch.object(gtt, "require_gh_auth"),
            mock.patch.object(
                gtt,
                "resolve_closeout_pull_request",
                side_effect=[draft, draft, ready],
            ),
            mock.patch.object(
                gtt,
                "closeout_remote_branch_head",
                return_value=archive_commit,
            ),
            mock.patch.object(gtt, "run", side_effect=run_with_ready),
            mock.patch.object(gtt, "cmd_finish_work", side_effect=execute_archived),
            mock.patch.object(gtt, "create_pull_request") as create_pr,
            mock.patch.object(
                gtt,
                "resume_archive_metadata_transaction",
            ) as archive_transaction,
            mock.patch.object(
                gtt,
                "execute_archive_metadata_transaction",
            ) as archive_commit_side_effect,
            mock.patch.object(
                gtt,
                "push_closeout_branch_if_needed",
            ) as push_branch,
        ):
            recorded = gtt.cmd_record_finalization_gate(args)
            self.assertEqual(recorded["typed_exit"], "published")
            self.assertEqual(gtt.git_status_paths(self.root), [])
            checked = gtt.cmd_check_finalization_gate(args)
            self.assertEqual(checked["typed_exit"], "published")
            transitioned = gtt.cmd_execute_finalization_transition(args)

        self.assertEqual(transitioned["typed_exit"], "published")
        self.assertEqual(transitioned["output"]["pr_number"], 166)
        self.assertEqual(ready_commands, [["gh", "pr", "ready", "--repo", "owner/repo", "166"]])
        self.assertEqual(committed_gate_path.read_bytes(), committed_gate_bytes)
        self.assertEqual(gtt.git_status_paths(self.root), [])
        self.assertEqual(
            subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=self.root,
                text=True,
                capture_output=True,
                check=True,
            ).stdout,
            "",
        )
        create_pr.assert_not_called()
        archive_transaction.assert_not_called()
        archive_commit_side_effect.assert_not_called()
        push_branch.assert_not_called()

    def test_active_preview_without_readiness_remains_publication_stale(self) -> None:
        public_input = {
            "profile": "standalone_finalization",
            "mode": "standalone",
            "task_ref": self.task_dir.relative_to(self.root).as_posix(),
        }
        stale = {
            "owner_status": "stale",
            "stale_reason": "publication_review_missing",
        }
        with (
            mock.patch.object(gtt, "finalization_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "task_dir_is_archived", return_value=False),
            mock.patch.object(gtt, "load_config", return_value={}),
            mock.patch.object(
                gtt,
                "finalization_verification_owner_result",
                return_value=None,
            ),
            mock.patch.object(
                gtt,
                "finalization_publication_owner_result",
                return_value=stale,
            ) as publication_owner,
        ):
            context = gtt.finalization_preview_context(
                self.root,
                argparse.Namespace(include_finalization_gate=True),
                public_input,
            )

        self.assertIsNone(context["plan"])
        self.assertEqual(context["transaction_state"], "publication_review_stale")
        self.assertEqual(context["publication_stale_reason"], "publication_review_missing")
        publication_owner.assert_called_once()

    def test_closeout_plan_tampering_and_protected_input_drift_fail_closed(self) -> None:
        plan = self.build_plan()
        plan["publish"]["title"] = "tampered"
        self.assertTrue(any("digest" in error for error in gtt.closeout_plan_errors(plan)))
        persisted = self.build_plan()
        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, persisted)
        self.body = valid_pr_body("changed body。")
        rebuilt = self.build_plan()
        self.assertNotEqual(persisted["plan_digest"], rebuilt["plan_digest"])

    def test_git_status_expands_untracked_and_disables_rename_detection(self) -> None:
        proc = mock.Mock(
            returncode=0,
            stdout=b" D src/runtime.py\0?? .trellis/tasks/07-11-closeout/runtime.py\0",
            stderr=b"",
        )
        with mock.patch.object(gtt.subprocess, "run", return_value=proc) as run:
            paths = gtt.git_status_paths(self.root)
        self.assertEqual(paths, ["src/runtime.py", ".trellis/tasks/07-11-closeout/runtime.py"])
        run.assert_called_once_with(
            ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all", "--no-renames"],
            cwd=str(self.root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_draft_resolver_rejects_multiple_or_ready_before_archive(self) -> None:
        plan = self.build_plan()
        body = self.body
        entry = {
            **closeout_head_repository_fields(),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "headRefOid": self.head,
            "isDraft": True,
        }
        with (
            mock.patch.object(gtt, "validate_github_remote_repository", return_value="owner/repo"),
            mock.patch.object(gtt, "run", return_value=mock.Mock(returncode=0, stdout=json.dumps([entry, entry]), stderr="")),
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.resolve_closeout_pull_request(self.root, "owner/repo", "fix/105-closeout", "main")
        ready = dict(entry, isDraft=False)
        with (
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=ready),
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "update_pull_request_metadata") as update,
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.ensure_closeout_draft_pr(self.root, plan, body)
        update.assert_not_called()

        stable_identity_mismatches = {
            "head": dict(entry, headRefName="fix/wrong"),
            "base": dict(entry, baseRefName="wrong"),
            "head-sha": dict(entry, headRefOid="b" * 40),
            "number-url": dict(entry, number=106),
            "url": dict(entry, url="http://github.com/owner/repo/pull/105"),
        }
        for name, candidate in stable_identity_mismatches.items():
            candidate["title"] = "predecessor title"
            candidate["body"] = "predecessor body\n"
            with (
                self.subTest(case=name),
                mock.patch.object(
                    gtt, "resolve_closeout_pull_request", return_value=candidate
                ),
                mock.patch.object(gtt, "current_head", return_value=self.head),
                mock.patch.object(gtt, "update_pull_request_metadata") as update,
                self.assertRaises(gtt.WorkflowError),
            ):
                gtt.ensure_closeout_draft_pr(self.root, plan, body)
            update.assert_not_called()

    def test_existing_draft_metadata_rebinds_same_identity_and_is_idempotent(self) -> None:
        plan = self.build_plan()
        body = self.body
        stale = {
            **closeout_head_repository_fields(),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
            "title": "predecessor title",
            "body": "predecessor body\n",
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "headRefOid": self.head,
            "isDraft": True,
        }
        rebound = {
            **stale,
            "title": plan["publish"]["title"],
            "body": body,
        }
        edit_commands: list[list[str]] = []
        edited_body_bytes: list[bytes] = []

        def fake_run(command: list[str], **_kwargs: object) -> mock.Mock:
            if command == ["gh", "auth", "status"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            self.assertEqual(command[:4], ["gh", "pr", "edit", "105"])
            edit_commands.append(command)
            body_path = Path(command[command.index("--body-file") + 1])
            edited_body_bytes.append(body_path.read_bytes())
            return mock.Mock(returncode=0, stdout="", stderr="")

        with (
            mock.patch.object(
                gtt,
                "resolve_closeout_pull_request",
                side_effect=[stale, rebound, rebound],
            ) as resolve,
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(gtt, "create_pull_request") as create,
        ):
            first = gtt.ensure_closeout_draft_pr(self.root, plan, body)
            second = gtt.ensure_closeout_draft_pr(self.root, plan, body)

        self.assertEqual(first, rebound)
        self.assertEqual(second, rebound)
        self.assertEqual(resolve.call_count, 3)
        self.assertEqual(len(edit_commands), 1)
        self.assertEqual(edit_commands[0][edit_commands[0].index("--repo") + 1], "owner/repo")
        self.assertEqual(
            edit_commands[0][edit_commands[0].index("--title") + 1],
            plan["publish"]["title"],
        )
        self.assertEqual(edited_body_bytes, [body.encode("utf-8")])
        self.assertEqual(
            hashlib.sha256(edited_body_bytes[0]).hexdigest(),
            hashlib.sha256(plan["publish"]["body"].encode("utf-8")).hexdigest(),
        )
        create.assert_not_called()

    def test_metadata_rebind_rejects_replaced_identity_after_edit(self) -> None:
        plan = self.build_plan()
        body = self.body
        stale = {
            **closeout_head_repository_fields(),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
            "title": "predecessor title",
            "body": "predecessor body\n",
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "headRefOid": self.head,
            "isDraft": True,
        }
        replacement = {
            **stale,
            "number": 106,
            "url": "https://github.com/owner/repo/pull/106",
            "title": plan["publish"]["title"],
            "body": body,
        }
        with (
            mock.patch.object(
                gtt,
                "resolve_closeout_pull_request",
                side_effect=[stale, replacement],
            ),
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "update_pull_request_metadata") as update,
            mock.patch.object(gtt, "create_pull_request") as create,
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.ensure_closeout_draft_pr(self.root, plan, body)
        update.assert_called_once_with(
            self.root,
            "owner/repo",
            105,
            plan["publish"]["title"],
            body,
        )
        create.assert_not_called()

    def test_closeout_repository_identity_normalizes_remote_urls_and_rejects_mismatch(self) -> None:
        for value in ["owner/repo", "Owner/Repo", "OWNER/REPO"]:
            with self.subTest(identifier=value):
                self.assertEqual(gtt.normalize_github_repository(value), "owner/repo")
        for value in [
            "",
            "owner",
            "owner/repo/extra",
            "https://github.com/Owner/Repo.git",
            "git@github.com:OWNER/REPO.git",
            "ssh://git@github.com/owner/repo.git",
            "owner/repo?token=x",
        ]:
            with self.subTest(invalid_identifier=value):
                self.assertEqual(gtt.normalize_github_repository(value), "")

        for value in [
            "https://github.com/Owner/Repo.git",
            "https://GITHUB.COM/owner/repo",
            "git@github.com:OWNER/REPO.git",
            "ssh://git@github.com/owner/repo.git",
        ]:
            with self.subTest(remote=value):
                self.assertEqual(gtt.parse_github_remote_repository_url(value), "owner/repo")
        for value in [
            "",
            "owner/repo",
            "Owner/Repo.git",
            "../owner/repo",
            "/tmp/owner/repo",
            "file:///tmp/owner/repo.git",
            "github.com/owner/repo",
            "github.com:owner/repo",
            "https://example.com/owner/repo.git",
            "http://github.com/owner/repo.git",
            "git://github.com/owner/repo.git",
            "https://token@github.com/owner/repo.git",
            "https://token:secret@github.com/owner/repo.git",
            "ssh://owner@github.com/owner/repo.git",
            "ssh://git:secret@github.com/owner/repo.git",
            "ssh://git@github.com:22/owner/repo.git",
            "https://github.com/owner/repo.git?token=secret",
            "https://github.com/owner/repo.git#fragment",
            "https://github.com/owner/repo/extra",
            "https://github.com/owner/repo/",
        ]:
            with self.subTest(invalid_remote=value):
                self.assertEqual(gtt.parse_github_remote_repository_url(value), "")

        canonical_remote = "https://github.com/owner/repo.git"
        unsafe_remote_values = [
            " " + canonical_remote,
            canonical_remote + " ",
            "\t" + canonical_remote,
            canonical_remote + "\t",
            canonical_remote + "\r",
            canonical_remote + "\n",
            canonical_remote + "\x00",
            canonical_remote + "\x01",
            canonical_remote + "\x7f",
            canonical_remote + "\u0085",
        ]
        self.assertTrue(gtt.git_remote_config_value_is_safe(canonical_remote))
        for value in unsafe_remote_values:
            with self.subTest(unsafe_remote=repr(value)):
                self.assertFalse(gtt.git_remote_config_value_is_safe(value))
                self.assertEqual(gtt.parse_github_remote_repository_url(value), "")
        self.assertEqual(
            gtt.parse_nul_terminated_git_config_values("one\0two\0"), ["one", "two"]
        )
        for output in ["", "one", "one\0two", "\0", "one\0\0"]:
            with self.subTest(invalid_nul_output=repr(output)):
                self.assertIsNone(gtt.parse_nul_terminated_git_config_values(output))
        self.assertEqual(
            gtt.parse_effective_git_remote_urls(canonical_remote + "\n", 1),
            [canonical_remote],
        )
        for output, count in [
            (canonical_remote, 1),
            (canonical_remote + "\r\n", 1),
            (canonical_remote + "\n" + canonical_remote + "\n", 1),
            ("\n", 1),
        ]:
            with self.subTest(invalid_effective_output=repr(output)):
                self.assertIsNone(gtt.parse_effective_git_remote_urls(output, count))

        with tempfile.TemporaryDirectory() as tmp:
            fixture_root = Path(tmp)

            def git(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    ["git", *args], cwd=cwd, check=True, text=True, capture_output=True
                )

            def remote_fixture(
                name: str,
                fetch_urls: list[str],
                push_urls: list[str] | None = None,
            ) -> Path:
                repository = fixture_root / name
                repository.mkdir()
                git("init", "-q", cwd=repository)
                git("remote", "add", "origin", fetch_urls[0], cwd=repository)
                for value in fetch_urls[1:]:
                    git("config", "--add", "remote.origin.url", value, cwd=repository)
                for value in push_urls or []:
                    git("config", "--add", "remote.origin.pushurl", value, cwd=repository)
                return repository

            fetch_mismatch = remote_fixture(
                "multiple-fetch",
                [
                    "https://github.com/fork-owner/repo.git",
                    "https://github.com/owner/repo.git",
                ],
            )
            effective_fetch = git("remote", "get-url", "--all", "origin", cwd=fetch_mismatch)
            self.assertEqual(
                [
                    gtt.parse_github_remote_repository_url(value)
                    for value in effective_fetch.stdout.splitlines()
                ],
                ["fork-owner/repo", "owner/repo"],
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.validate_github_remote_repository(fetch_mismatch, "origin", "owner/repo")
            self.assertEqual(raised.exception.payload["direction"], "fetch")
            self.assertNotIn("fork-owner", json.dumps(raised.exception.payload))

            push_mismatch = remote_fixture(
                "multiple-push",
                ["https://github.com/owner/repo.git"],
                [
                    "https://github.com/owner/repo.git",
                    "https://github.com/fork-owner/repo.git",
                    "https://github.com/OWNER/REPO.git",
                ],
            )
            effective_push = git(
                "remote", "get-url", "--push", "--all", "origin", cwd=push_mismatch
            )
            self.assertEqual(
                [
                    gtt.parse_github_remote_repository_url(value)
                    for value in effective_push.stdout.splitlines()
                ],
                ["owner/repo", "fork-owner/repo", "owner/repo"],
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.validate_github_remote_repository(push_mismatch, "origin", "owner/repo")
            self.assertEqual(raised.exception.payload["direction"], "push")
            self.assertNotIn("fork-owner", json.dumps(raised.exception.payload))

            rewritten_push = remote_fixture(
                "push-instead-of", ["https://github.com/owner/repo.git"]
            )
            git(
                "config",
                "url.https://github.com/fork-owner/repo.git.pushInsteadOf",
                "https://github.com/owner/repo.git",
                cwd=rewritten_push,
            )
            effective_rewrite = git(
                "remote", "get-url", "--push", "--all", "origin", cwd=rewritten_push
            )
            self.assertEqual(
                [
                    gtt.parse_github_remote_repository_url(value)
                    for value in effective_rewrite.stdout.splitlines()
                ],
                ["fork-owner/repo"],
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.validate_github_remote_repository(rewritten_push, "origin", "owner/repo")
            self.assertEqual(raised.exception.payload["direction"], "push")
            self.assertNotIn("fork-owner", json.dumps(raised.exception.payload))

            matching = remote_fixture(
                "matching",
                [
                    "https://github.com/Owner/Repo.git",
                    "ssh://git@github.com/owner/repo.git",
                ],
                [
                    "git@github.com:OWNER/REPO.git",
                    "https://github.com/owner/repo.git",
                ],
            )
            for push in [False, True]:
                command = ["remote", "get-url"]
                if push:
                    command.append("--push")
                command.extend(["--all", "origin"])
                result = git(*command, cwd=matching)
                self.assertTrue(result.stdout.splitlines())
                self.assertEqual(
                    {
                        gtt.parse_github_remote_repository_url(value)
                        for value in result.stdout.splitlines()
                    },
                    {"owner/repo"},
                )
            self.assertEqual(
                gtt.validate_github_remote_repository(matching, "origin", "OWNER/REPO"),
                "owner/repo",
            )

            malformed = remote_fixture(
                "malformed", ["https://example.com/owner/repo.git"]
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.validate_github_remote_repository(malformed, "origin", "owner/repo")
            self.assertEqual(raised.exception.payload["direction"], "fetch")
            self.assertNotIn("example.com", json.dumps(raised.exception.payload))

            missing_remote = fixture_root / "missing-remote"
            missing_remote.mkdir()
            git("init", "-q", cwd=missing_remote)
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.validate_github_remote_repository(missing_remote, "origin", "owner/repo")
            self.assertEqual(
                raised.exception.payload, {"remote": "origin", "source": "raw-config"}
            )

            raw_control_values = [
                ("leading-space", " " + canonical_remote),
                ("trailing-space", canonical_remote + " "),
                ("leading-tab", "\t" + canonical_remote),
                ("trailing-tab", canonical_remote + "\t"),
                ("carriage-return", canonical_remote + "\r"),
                ("single-value-newline", canonical_remote + "\n" + canonical_remote),
                ("c0-control", canonical_remote + "\x01"),
                ("delete-control", canonical_remote + "\x7f"),
            ]
            for name, value in raw_control_values:
                with self.subTest(raw_control=name):
                    repository = remote_fixture(f"raw-{name}", [value])
                    raw = git(
                        "config", "--null", "--get-all", "remote.origin.url", cwd=repository
                    )
                    self.assertTrue(raw.stdout.endswith("\0"))
                    with self.assertRaises(gtt.WorkflowError) as raised:
                        gtt.validate_github_remote_repository(repository, "origin", "owner/repo")
                    self.assertEqual(
                        raised.exception.payload,
                        {"remote": "origin", "direction": "fetch", "source": "raw-config"},
                    )
                    self.assertNotIn(value, json.dumps(raised.exception.payload))

            for name, pattern in [
                ("newline", "gh:\n"),
                ("tab", "gh:\t"),
                ("c0", "gh:\x01"),
            ]:
                with self.subTest(rewrite_control=name):
                    repository = remote_fixture(f"rewrite-{name}", ["gh:repo"])
                    git(
                        "config",
                        "url.https://github.com/owner/.insteadOf",
                        pattern,
                        cwd=repository,
                    )
                    with self.assertRaises(gtt.WorkflowError) as raised:
                        gtt.validate_github_remote_repository(repository, "origin", "owner/repo")
                    self.assertEqual(
                        raised.exception.payload, {"source": "url-rewrite-config"}
                    )
                    self.assertNotIn(pattern, json.dumps(raised.exception.payload))

            rewrite_base = remote_fixture("rewrite-base-tab", ["gh:repo"])
            rewrite_config = rewrite_base / ".git/config"
            rewrite_config.write_text(
                rewrite_config.read_text(encoding="utf-8")
                + '\n[url "https://github.com/\t"]\n\tinsteadOf = gh:\n',
                encoding="utf-8",
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.validate_github_remote_repository(rewrite_base, "origin", "owner/repo")
            self.assertEqual(raised.exception.payload, {"source": "url-rewrite-config"})

            nul_config = fixture_root / "raw-nul"
            nul_config.mkdir()
            git("init", "-q", cwd=nul_config)
            config_path = nul_config / ".git/config"
            config_path.write_bytes(
                config_path.read_bytes()
                + b'\n[remote "origin"]\n\turl = https://github.com/owner/repo.git\x00tail\n'
            )
            raw_nul = subprocess.run(
                ["git", "config", "--null", "--get-all", "remote.origin.url"],
                cwd=nul_config,
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertEqual(raw_nul.returncode, 0)
            self.assertEqual(raw_nul.stdout, canonical_remote + "\0")
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.validate_github_remote_repository(nul_config, "origin", "owner/repo")
            self.assertEqual(
                raised.exception.payload, {"remote": "origin", "source": "raw-config"}
            )
            self.assertNotIn("tail", json.dumps(raised.exception.payload))

            local_target = fixture_root / "local-target.git"
            invalid_transports = [
                ("relative", "owner/repo"),
                ("relative-dotgit", "Owner/Repo.git"),
                ("parent-relative", "../owner/repo"),
                ("absolute", str(local_target)),
                ("file", local_target.as_uri()),
            ]
            for name, value in invalid_transports:
                with self.subTest(local_transport=name):
                    repository = remote_fixture(f"invalid-{name}", [value])
                    effective = git("remote", "get-url", "--all", "origin", cwd=repository)
                    self.assertTrue(effective.stdout.strip())
                    with self.assertRaises(gtt.WorkflowError) as raised:
                        gtt.validate_github_remote_repository(repository, "origin", "owner/repo")
                    self.assertEqual(
                        raised.exception.payload,
                        {
                            "remote": "origin",
                            "direction": "fetch",
                            "expected_repo": "owner/repo",
                        },
                    )

        empty = subprocess.CompletedProcess(
            ["git", "remote", "get-url", "--all", "origin"], 0, "\n", ""
        )
        with (
            mock.patch.object(gtt, "git_url_rewrite_config_is_safe", return_value=True),
            mock.patch.object(
                gtt,
                "read_raw_git_config_values",
                side_effect=[[canonical_remote], []],
            ),
            mock.patch.object(gtt, "run", return_value=empty) as remote,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.validate_github_remote_repository(self.root, "origin", "owner/repo")
        remote.assert_called_once_with(
            ["git", "remote", "get-url", "--all", "origin"], cwd=self.root, check=False
        )
        self.assertEqual(raised.exception.payload, {"remote": "origin", "direction": "fetch"})

        fetch = subprocess.CompletedProcess(
            ["git", "remote", "get-url", "--all", "origin"],
            0,
            "https://github.com/owner/repo.git\n",
            "",
        )
        failed_push = subprocess.CompletedProcess(
            ["git", "remote", "get-url", "--push", "--all", "origin"],
            2,
            "",
            "credential-bearing failure",
        )
        with (
            mock.patch.object(gtt, "git_url_rewrite_config_is_safe", return_value=True),
            mock.patch.object(
                gtt,
                "read_raw_git_config_values",
                side_effect=[[canonical_remote], []],
            ),
            mock.patch.object(gtt, "run", side_effect=[fetch, failed_push]),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.validate_github_remote_repository(self.root, "origin", "owner/repo")
        self.assertEqual(raised.exception.payload, {"remote": "origin", "direction": "push"})
        self.assertNotIn("credential-bearing", str(raised.exception))

        noncanonical_plan = self.build_plan()
        noncanonical_plan["git"]["repo"] = "Owner/Repo"
        self.assertIn(
            "closeout git.repo must be a normalized GitHub owner/repository identity.",
            gtt.closeout_plan_errors(noncanonical_plan),
        )

    def test_closeout_pr_query_rejects_same_branch_fork_before_cardinality(self) -> None:
        plan = self.build_plan()
        body = self.body
        target = {
            **closeout_head_repository_fields(),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "headRefOid": self.head,
            "isDraft": True,
        }
        fork = {
            **target,
            **closeout_head_repository_fields("fork-owner/repo", cross_repository=True),
            "number": 106,
            "url": "https://github.com/owner/repo/pull/106",
        }
        for name, candidates in [("fork-only", [fork]), ("target-and-fork", [target, fork])]:
            with (
                self.subTest(case=name),
                mock.patch.object(gtt, "validate_github_remote_repository", return_value="owner/repo"),
                mock.patch.object(
                    gtt,
                    "run",
                    return_value=mock.Mock(returncode=0, stdout=json.dumps(candidates), stderr=""),
                ) as query,
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.resolve_closeout_pull_request(
                    self.root, "owner/repo", "fix/105-closeout", "main", "origin"
                )
            self.assertIn("cross-repository", str(raised.exception))
            json_fields = query.call_args.args[0][query.call_args.args[0].index("--json") + 1]
            self.assertIn("headRepository", json_fields)
            self.assertIn("headRepositoryOwner", json_fields)
            self.assertIn("isCrossRepository", json_fields)

        missing = dict(target)
        missing.pop("headRepositoryOwner")
        with (
            mock.patch.object(gtt, "validate_github_remote_repository", return_value="owner/repo"),
            mock.patch.object(
                gtt, "run", return_value=mock.Mock(returncode=0, stdout=json.dumps([missing]), stderr="")
            ),
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.resolve_closeout_pull_request(
                self.root, "owner/repo", "fix/105-closeout", "main", "origin"
            )

    def test_fork_identity_blocks_draft_reuse_final_projection_and_ready(self) -> None:
        plan = self.build_plan()
        body = self.body
        fork = {
            **closeout_head_repository_fields("fork-owner/repo", cross_repository=True),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "headRefOid": self.head,
            "isDraft": True,
        }
        with (
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=fork),
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "create_pull_request") as create,
            mock.patch.object(gtt, "update_pull_request_metadata") as update,
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.ensure_closeout_draft_pr(self.root, plan, body)
        create.assert_not_called()
        update.assert_not_called()

        gtt.write_json(
            self.task_dir / gtt.PR_READINESS_ARTIFACT,
            {"publish_inputs": {"closeout_plan_digest": plan["plan_digest"]}},
        )
        prepared = {
            "plan": plan,
            "task_context": self.context,
            "gate": self.gate,
        }
        with (
            mock.patch.object(gtt, "load_issue_scope_ledger", return_value=self.ledger),
            mock.patch.object(gtt, "validate_ledger_for_publish", return_value=[]),
            mock.patch.object(gtt, "current_head", return_value=self.head),
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.build_final_archive_projection(self.root, self.task_dir, prepared, fork)
        self.assertFalse((self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT).exists())

        with (
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=fork),
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "run") as mutation,
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.ensure_closeout_pr_ready(self.root, plan)
        mutation.assert_not_called()

    def test_closeout_docs_and_query_require_exact_head_repository_identity(self) -> None:
        source_root = Path(__file__).resolve().parents[5]
        paths = [
            source_root / ".trellis/spec/workflow/companion-scripts.md",
            source_root / ".trellis/spec/workflow/data-contracts.md",
            source_root / ".trellis/spec/workflow/workflow-contract.md",
        ]
        for path in paths:
            with self.subTest(path=str(path)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("headRepository", text)
                self.assertIn("isCrossRepository", text)
        source = (
            source_root / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py"
        ).read_text(encoding="utf-8")
        self.assertIn("headRepository,headRepositoryOwner,isCrossRepository", source)
        self.assertNotIn(
            '"--json", "number,url,title,body,headRefName,baseRefName,headRefOid,isDraft"',
            source,
        )

    def test_closeout_pr_body_identity_preserves_exact_utf8_whitespace(self) -> None:
        base_body = valid_pr_body("PR body exact bytes identity。")
        cases = {
            "leading-whitespace": ("\n" + base_body, base_body),
            "trailing-whitespace": (base_body + " \n", base_body + "\n"),
            "markdown-hard-break": (
                base_body + "Markdown hard break  \n下一行\n",
                base_body + "Markdown hard break\n下一行\n",
            ),
        }
        for name, (exact_body, tampered_body) in cases.items():
            with self.subTest(case=name):
                self.body = exact_body
                plan = self.build_plan()

                pr = {
                    **closeout_head_repository_fields(),
                    "number": 105,
                    "url": "https://github.com/owner/repo/pull/105",
                    "title": plan["publish"]["title"],
                    "body": exact_body,
                    "headRefName": "fix/105-closeout",
                    "baseRefName": "main",
                    "headRefOid": self.head,
                    "isDraft": True,
                }
                gtt.validate_closeout_pull_request_identity(
                    self.root,
                    self.task_dir,
                    plan,
                    pr,
                    expected_draft=True,
                    require_summary=False,
                )
                with self.assertRaises(gtt.WorkflowError):
                    gtt.validate_closeout_pull_request_identity(
                        self.root,
                        self.task_dir,
                        plan,
                        dict(pr, body=tampered_body),
                        expected_draft=True,
                        require_summary=False,
                    )
                with (
                    mock.patch.object(gtt, "resolve_closeout_pull_request") as resolve,
                    mock.patch.object(gtt, "create_pull_request") as create,
                    mock.patch.object(gtt, "update_pull_request_metadata") as update,
                    self.assertRaises(gtt.WorkflowError),
                ):
                    gtt.ensure_closeout_draft_pr(self.root, plan, tampered_body)
                resolve.assert_not_called()
                create.assert_not_called()
                update.assert_not_called()

    def test_active_summary_and_bound_remote_identity_reject_pr_replacement(self) -> None:
        plan = self.build_plan()
        body = self.body
        summary = gtt.closeout_summary_for_pr(
            plan, {"number": 105, "url": "https://github.com/owner/repo/pull/105"}
        )
        gtt.write_json(self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT, summary)
        replacement = {
            **closeout_head_repository_fields(),
            "number": 106,
            "url": "https://github.com/owner/repo/pull/106",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "headRefOid": self.head,
            "isDraft": True,
        }
        with self.assertRaises(gtt.WorkflowError):
            gtt.validate_closeout_pull_request_identity(
                self.root,
                self.task_dir,
                plan,
                replacement,
                expected_draft=True,
                require_summary=True,
            )
        with self.assertRaises(gtt.WorkflowError):
            gtt.validate_closeout_remote_pull_request_identity(
                plan,
                replacement,
                expected_draft=True,
                bound_pr={
                    "number": 105,
                    "url": "https://github.com/owner/repo/pull/105",
                },
            )

        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, plan)
        args = finish_args(dry_run=False, expected_plan_digest=plan["plan_digest"])
        for case, tampered in [
            ("title", dict(replacement, number=105, url="https://github.com/owner/repo/pull/105", title="tampered")),
            ("body", dict(replacement, number=105, url="https://github.com/owner/repo/pull/105", body="tampered")),
        ]:
            with (
                self.subTest(case=case),
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=tampered),
                mock.patch.object(gtt, "resume_archive_metadata_transaction") as archive,
                mock.patch.object(gtt, "ensure_closeout_pr_ready") as ready,
                self.assertRaises(gtt.WorkflowError),
            ):
                gtt.resume_archived_closeout(self.root, args, self.task_dir)
            archive.assert_not_called()
            ready.assert_not_called()

    def test_active_and_archived_recovery_never_rebind_same_identity_fork(self) -> None:
        plan = self.build_plan()
        body = self.body
        target = {
            **closeout_head_repository_fields(),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
        }
        summary = gtt.closeout_summary_for_pr(plan, target)
        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, plan)
        gtt.write_json(self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT, summary)
        fork = {
            **closeout_head_repository_fields("fork-owner/repo", cross_repository=True),
            "number": 106,
            "url": "https://github.com/owner/repo/pull/106",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "headRefOid": self.head,
            "isDraft": True,
        }
        completed = dict(self.task, status="completed")
        gtt.write_json(self.task_dir / "task.json", completed)
        args = finish_args(dry_run=False, expected_plan_digest=plan["plan_digest"])
        with (
            mock.patch.object(gtt, "load_issue_scope_ledger", return_value=self.ledger),
            mock.patch.object(gtt, "validate_closeout_active_projection"),
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "require_gh_auth"),
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=fork),
            mock.patch.object(gtt, "execute_archive_metadata_transaction") as archive,
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.resume_active_archive_move(self.root, args, {}, self.task_dir, self.context)
        archive.assert_not_called()
        self.assertEqual(
            gtt.read_json(self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT)["github"]["pr_url"],
            target["url"],
        )

        archived = self.root / plan["task"]["archive_locator"]
        archived.parent.mkdir(parents=True, exist_ok=True)
        self.task_dir.rename(archived)
        summary_before = (archived / gtt.FINISH_SUMMARY_ARTIFACT).read_bytes()
        with (
            mock.patch.object(gtt, "require_gh_auth"),
            mock.patch.object(gtt, "validate_github_remote_repository", return_value="owner/repo"),
            mock.patch.object(
                gtt,
                "run",
                return_value=mock.Mock(returncode=0, stdout=json.dumps([fork]), stderr=""),
            ),
            mock.patch.object(gtt, "resume_archive_metadata_transaction") as archive,
            mock.patch.object(gtt, "ensure_closeout_pr_ready") as ready,
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.resume_archived_closeout(self.root, args, archived)
        archive.assert_not_called()
        ready.assert_not_called()
        self.assertEqual((archived / gtt.FINISH_SUMMARY_ARTIFACT).read_bytes(), summary_before)

    def test_task_json_archive_content_allows_only_official_fields(self) -> None:
        before = b'{"status":"in_progress","title":"task"}\n'
        after = b'{"status":"completed","title":"task","completedAt":"2026-07-11"}\n'
        gtt.validate_closeout_task_json_archive_change(before, after)
        tampered = b'{"status":"completed","title":"changed","completedAt":"2026-07-11"}\n'
        with self.assertRaises(gtt.WorkflowError):
            gtt.validate_closeout_task_json_archive_change(before, tampered)

    def test_task_json_reviewed_binding_survives_worktree_and_commit_archive_validation(self) -> None:
        parent_payload = {
            "status": "in_progress",
            "title": "task",
            "completedAt": None,
            "meta": {},
        }
        reviewed_payload = copy.deepcopy(parent_payload)
        reviewed_payload["meta"] = {"publication_round": "reviewed-tail"}
        reviewed = json.dumps(reviewed_payload, ensure_ascii=False, indent=2).encode("utf-8")
        archived_payload = copy.deepcopy(reviewed_payload)
        archived_payload["status"] = "completed"
        archived_payload["completedAt"] = "2026-07-11"
        archived = json.dumps(archived_payload, ensure_ascii=False, indent=2).encode("utf-8")
        binding = {
            "path": "task.json",
            "mode": "100644",
            "sha256": hashlib.sha256(reviewed).hexdigest(),
        }

        for archive_commit in (None, "c" * 40):
            with self.subTest(archive_commit=archive_commit):
                self.validate_task_json_archive_continuity_fixture(
                    parent=json.dumps(parent_payload, ensure_ascii=False, indent=2).encode("utf-8"),
                    after=archived,
                    binding=binding,
                    archive_commit=archive_commit,
                )

    def test_task_json_reviewed_binding_rejects_digest_mode_and_extra_field_drift(self) -> None:
        parent_payload = {"status": "in_progress", "title": "task", "completedAt": None}
        reviewed_payload = {
            **parent_payload,
            "meta": {"publication_round": "reviewed-tail"},
        }
        reviewed = json.dumps(reviewed_payload, ensure_ascii=False, indent=2).encode("utf-8")
        archived_payload = {
            **reviewed_payload,
            "status": "completed",
            "completedAt": "2026-07-11",
        }
        archived = json.dumps(archived_payload, ensure_ascii=False, indent=2).encode("utf-8")
        binding = {
            "path": "task.json",
            "mode": "100644",
            "sha256": hashlib.sha256(reviewed).hexdigest(),
        }
        cases = {
            "digest": ({**binding, "sha256": "0" * 64}, archived, "100644"),
            "mode": ({**binding, "mode": "100755"}, archived, "100644"),
            "extra-field": (
                binding,
                json.dumps(
                    {**archived_payload, "title": "changed during archive"},
                    ensure_ascii=False,
                    indent=2,
                ).encode("utf-8"),
                "100644",
            ),
        }
        for name, (candidate_binding, candidate_after, candidate_mode) in cases.items():
            with self.subTest(name=name), self.assertRaises(gtt.WorkflowError):
                self.validate_task_json_archive_continuity_fixture(
                    parent=json.dumps(parent_payload, ensure_ascii=False, indent=2).encode("utf-8"),
                    after=candidate_after,
                    binding=candidate_binding,
                    after_mode=candidate_mode,
                    archive_commit="c" * 40,
                )

    def test_task_json_without_binding_still_uses_transaction_parent_baseline(self) -> None:
        parent = b'{"status":"in_progress","title":"task"}\n'
        archived = b'{"status":"completed","title":"task","completedAt":"2026-07-11"}\n'
        self.validate_task_json_archive_continuity_fixture(
            parent=parent,
            after=archived,
            binding=None,
            archive_commit="c" * 40,
        )

    def test_formal_digest_mismatch_blocks_before_any_side_effect(self) -> None:
        plan = self.build_plan()
        prepared = {
            "plan": plan,
            "task": self.task,
            "task_context": self.context,
            "gate": self.gate,
            "ledger": self.ledger,
            "body": "body",
        }
        args = finish_args(dry_run=False, expected_plan_digest="b" * 64)
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "load_task_runtime_identity", return_value=self.context),
            mock.patch.object(gtt, "assert_workspace_boundary"),
            mock.patch.object(gtt, "task_dir_is_archived", return_value=False),
            mock.patch.object(gtt, "prepare_closeout", return_value=prepared),
            mock.patch.object(gtt, "require_gh_auth") as auth,
            mock.patch.object(gtt, "run_stdout") as mutation,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_finish_work(args)
        self.assertEqual(raised.exception.payload["failed_stage"], "plan-digest-handshake")
        auth.assert_not_called()
        mutation.assert_not_called()

    def test_2026_07_04_dry_run_formal_drift_regression(self) -> None:
        self.test_formal_digest_mismatch_blocks_before_any_side_effect()

    def test_2026_07_03_post_archive_identity_regression_moves_check_before_archive(self) -> None:
        plan = self.build_plan()
        with mock.patch.object(gtt, "run") as remote, self.assertRaises(gtt.WorkflowError):
            gtt.validate_publish_identity_and_remote_head(
                self.root,
                {"base_branch": "main"},
                {"source_repo": {"repo": "owner/repo"}, "branch_name": "fix/105-closeout", "base_branch": "main"},
                "other/repo",
                "main",
                "fix/105-closeout",
                "origin",
            )
        remote.assert_not_called()
        self.assertEqual(plan["transitions"].index("content_pushed"), 1)
        self.assertGreater(plan["transitions"].index("archive_moved"), 1)

    def test_cli_exposes_expected_plan_digest(self) -> None:
        parser = gtt.build_parser()
        finish = parser.parse_args([
            "finish-work", "--dry-run",
            "--expected-plan-digest", "a" * 64,
        ])
        self.assertEqual(finish.expected_plan_digest, "a" * 64)

    def test_draft_to_ready_failure_has_no_repo_mutation(self) -> None:
        plan = self.build_plan()
        body = self.body
        summary = gtt.closeout_summary_for_pr(
            plan, {"number": 105, "url": "https://github.com/owner/repo/pull/105"}
        )
        gtt.write_json(self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT, summary)
        draft = {
            **closeout_head_repository_fields(),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "headRefOid": self.head,
            "isDraft": True,
        }
        def fake_run(command: list[str], **_kwargs: object) -> mock.Mock:
            if command == ["gh", "auth", "status"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "ls-remote", "--heads"]:
                return mock.Mock(returncode=0, stdout=f"{self.head}\trefs/heads/fix/105-closeout\n", stderr="")
            if command[:3] == ["gh", "pr", "ready"]:
                return mock.Mock(returncode=1, stdout="", stderr="ready failed")
            raise AssertionError(command)
        with (
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=draft),
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(gtt, "run_stdout") as mutation,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.ensure_closeout_pr_ready(self.root, plan)
        self.assertEqual(raised.exception.payload["stage"], "draft-to-ready")
        mutation.assert_not_called()

    def test_draft_to_ready_waits_for_transient_pr_head_convergence(self) -> None:
        plan = self.build_plan()
        body = self.body
        stale_head = "b" * 40
        draft = {
            **closeout_head_repository_fields(),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "headRefOid": stale_head,
            "isDraft": True,
        }
        converged = dict(draft, headRefOid=self.head)
        ready = dict(converged, isDraft=False)
        commands: list[list[str]] = []

        def fake_run(command: list[str], **_kwargs: object) -> mock.Mock:
            commands.append(command)
            if command == ["gh", "auth", "status"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "ls-remote", "--heads"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{self.head}\trefs/heads/fix/105-closeout\n",
                    stderr="",
                )
            if command[:3] == ["gh", "pr", "ready"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            raise AssertionError(command)

        with (
            mock.patch.object(
                gtt,
                "resolve_closeout_pull_request",
                side_effect=[draft, converged, ready],
            ) as resolve,
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(gtt.time, "sleep") as sleeper,
        ):
            result = gtt.ensure_closeout_pr_ready(
                self.root,
                plan,
                bound_pr=draft,
            )

        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["pr"]["number"], 105)
        self.assertFalse(result["pr"]["isDraft"])
        self.assertEqual(resolve.call_count, 3)
        sleeper.assert_called_once_with(
            gtt.CLOSEOUT_PR_HEAD_READ_DELAY_SECONDS,
        )
        self.assertEqual(
            sum(command[:3] == ["gh", "pr", "ready"] for command in commands),
            1,
        )

    def test_draft_to_ready_fails_after_bounded_pr_head_mismatch(self) -> None:
        plan = self.build_plan()
        body = self.body
        stale_head = "b" * 40
        draft = {
            **closeout_head_repository_fields(),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "headRefOid": stale_head,
            "isDraft": True,
        }
        commands: list[list[str]] = []

        def fake_run(command: list[str], **_kwargs: object) -> mock.Mock:
            commands.append(command)
            if command[:3] == ["git", "ls-remote", "--heads"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{self.head}\trefs/heads/fix/105-closeout\n",
                    stderr="",
                )
            raise AssertionError(command)

        with (
            mock.patch.object(
                gtt,
                "resolve_closeout_pull_request",
                return_value=draft,
            ) as resolve,
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "run", side_effect=fake_run),
            mock.patch.object(gtt.time, "sleep") as sleeper,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.ensure_closeout_pr_ready(self.root, plan, bound_pr=draft)

        self.assertEqual(resolve.call_count, gtt.CLOSEOUT_PR_HEAD_READ_ATTEMPTS)
        self.assertEqual(
            sleeper.call_count,
            gtt.CLOSEOUT_PR_HEAD_READ_ATTEMPTS - 1,
        )
        self.assertEqual(raised.exception.payload["local_head"], self.head)
        self.assertEqual(raised.exception.payload["remote_head"], self.head)
        self.assertEqual(raised.exception.payload["pr_head"], stale_head)
        self.assertFalse(
            any(command[:3] == ["gh", "pr", "ready"] for command in commands)
        )

    def test_post_archive_layout_and_ready_do_not_run_local_artifact_validators(self) -> None:
        plan = self.build_plan()
        body = self.body
        for relative in plan["projection"]["move_paths"]:
            path = self.task_dir / relative
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("not a valid closeout artifact\n", encoding="utf-8")
        archived = self.root / plan["task"]["archive_locator"]
        archived.parent.mkdir(parents=True, exist_ok=True)
        self.task_dir.rename(archived)
        gtt.compact_closeout_archive(archived, plan)
        (archived / "task.json").write_bytes(b"\xff")
        (archived / gtt.FINISH_SUMMARY_ARTIFACT).write_text("invalid summary\n", encoding="utf-8")

        draft = {
            **closeout_head_repository_fields(),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "headRefOid": self.head,
            "isDraft": True,
        }
        ready = dict(draft, isDraft=False)

        def fake_run(command: list[str], **_kwargs: object) -> mock.Mock:
            if command == ["gh", "auth", "status"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            if command[:3] == ["git", "ls-remote", "--heads"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{self.head}\trefs/heads/fix/105-closeout\n",
                    stderr="",
                )
            if command[:3] == ["gh", "pr", "ready"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            raise AssertionError(command)

        forbidden = [
            "read_and_validate_closeout_final_summary",
            "validate_finish_summary",
            "load_issue_scope_ledger",
            "validate_ledger_for_publish",
            "validate_closeout_marketplace_artifact",
            "validate_closeout_pull_request_identity",
        ]
        patches = [
            mock.patch.object(gtt, name, side_effect=AssertionError(f"post-archive local validator called: {name}"))
            for name in forbidden
        ]
        with contextlib.ExitStack() as stack:
            for patcher in patches:
                stack.enter_context(patcher)
            gtt.validate_closeout_archive_move_layout(self.root, archived, plan)
            stack.enter_context(mock.patch.object(gtt, "resolve_closeout_pull_request", side_effect=[draft, ready]))
            stack.enter_context(mock.patch.object(gtt, "current_head", return_value=self.head))
            stack.enter_context(mock.patch.object(gtt, "run", side_effect=fake_run))
            result = gtt.ensure_closeout_pr_ready(self.root, plan, bound_pr=draft)
        self.assertEqual(result["status"], "ready")
        self.assertFalse(result["pr"]["isDraft"])

    def test_archived_draft_reentry_uses_plan_remote_identity_and_ready_only(self) -> None:
        plan = self.build_plan()
        body = self.body
        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, plan)
        archived = self.root / plan["task"]["archive_locator"]
        archived.parent.mkdir(parents=True, exist_ok=True)
        self.task_dir.rename(archived)
        for path in list(archived.iterdir()):
            if path.name != gtt.CLOSEOUT_PLAN_ARTIFACT:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()

        draft = {
            **closeout_head_repository_fields(),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "headRefOid": self.head,
            "isDraft": True,
        }
        ready = dict(draft, isDraft=False)
        args = finish_args(dry_run=False, expected_plan_digest=plan["plan_digest"])
        commands: list[list[str]] = []

        def fake_run(command: list[str], **_kwargs: object) -> mock.Mock:
            commands.append(command)
            if command[:3] == ["git", "ls-remote", "--heads"]:
                return mock.Mock(
                    returncode=0,
                    stdout=f"{self.head}\trefs/heads/fix/105-closeout\n",
                    stderr="",
                )
            if command[:3] == ["gh", "pr", "ready"]:
                return mock.Mock(returncode=0, stdout="", stderr="")
            raise AssertionError(command)

        forbidden = [
            "read_and_validate_closeout_final_summary",
            "validate_finish_summary",
            "load_issue_scope_ledger",
            "validate_ledger_for_publish",
            "validate_closeout_marketplace_artifact",
            "validate_closeout_pull_request_identity",
        ]
        with contextlib.ExitStack() as stack:
            for name in forbidden:
                stack.enter_context(
                    mock.patch.object(
                        gtt,
                        name,
                        side_effect=AssertionError(f"archived recovery local validator called: {name}"),
                    )
                )
            stack.enter_context(mock.patch.object(gtt, "require_gh_auth"))
            stack.enter_context(
                mock.patch.object(
                    gtt,
                    "resolve_closeout_pull_request",
                    side_effect=[draft, draft, ready],
                )
            )
            archive = stack.enter_context(
                mock.patch.object(
                    gtt,
                    "resume_archive_metadata_transaction",
                    return_value={"commit": self.head},
                )
            )
            stack.enter_context(mock.patch.object(gtt, "current_head", return_value=self.head))
            stack.enter_context(mock.patch.object(gtt, "run", side_effect=fake_run))
            stack.enter_context(
                mock.patch.object(
                    gtt,
                    "resolve_committed_closeout_archive_transaction",
                    return_value=None,
                )
            )
            result = gtt.resume_archived_closeout(self.root, args, archived)
        archive.assert_called_once_with(self.root, archived, plan, bound_pr=draft)
        self.assertEqual(result["stage"], "ready")
        self.assertEqual(
            [command[:3] for command in commands],
            [["git", "ls-remote", "--heads"], ["gh", "pr", "ready"]],
        )

    def test_active_completed_archive_move_recovery_uses_owner_and_skips_pr_create(self) -> None:
        plan = self.build_plan()
        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, plan)
        completed = dict(self.task, status="completed")
        gtt.write_json(self.task_dir / "task.json", completed)
        gtt.write_json(self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT, {"schema_version": 1})
        archived = self.root / plan["task"]["archive_locator"]
        args = finish_args(dry_run=False, expected_plan_digest=plan["plan_digest"])
        verification_owner_result = {
            "typed_exit": "verified",
            "branch_review_commit": self.head,
        }
        args.verification_owner_result = verification_owner_result
        body = self.body
        summary = gtt.closeout_summary_for_pr(
            plan, {"number": 105, "url": "https://github.com/owner/repo/pull/105"}
        )
        gtt.write_json(self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT, summary)
        draft = {
            **closeout_head_repository_fields(),
            "number": 105,
            "url": "https://github.com/owner/repo/pull/105",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": "fix/105-closeout",
            "baseRefName": "main",
            "isDraft": True,
            "headRefOid": self.head,
        }
        with (
            mock.patch.object(gtt, "validate_closeout_reviewed_content"),
            mock.patch.object(gtt, "load_issue_scope_ledger", return_value=self.ledger),
            mock.patch.object(gtt, "validate_finish_summary"),
            mock.patch.object(
                gtt,
                "validate_closeout_active_projection",
            ) as active_projection,
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "require_gh_auth"),
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=draft),
            mock.patch.object(gtt, "execute_archive_metadata_transaction", return_value=(archived, {"commit": self.head})) as archive,
            mock.patch.object(gtt, "ensure_closeout_pr_ready", return_value={"status": "ready"}),
            mock.patch.object(gtt, "create_pull_request") as create,
        ):
            result = gtt.resume_active_archive_move(self.root, args, {}, self.task_dir, self.context)
        self.assertEqual(result["entry_state"], "archive_moved")
        active_projection.assert_called_once_with(
            self.root,
            self.task_dir,
            plan,
            verification_owner_result=verification_owner_result,
        )
        archive.assert_called_once_with(
            self.root,
            self.task_dir,
            plan,
            bound_pr=draft,
            verification_owner_result=verification_owner_result,
        )
        create.assert_not_called()

    def test_archived_recovery_requires_gh_auth_before_git_or_pr_mutation(self) -> None:
        plan = self.build_plan()
        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, plan)
        args = finish_args(dry_run=False, expected_plan_digest=plan["plan_digest"])
        with (
            mock.patch.object(
                gtt,
                "require_gh_auth",
                side_effect=gtt.WorkflowError("auth required", exit_code=2),
            ) as auth,
            mock.patch.object(gtt, "resume_archive_metadata_transaction") as archive,
            mock.patch.object(gtt, "ensure_closeout_pr_ready") as ready,
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.resume_archived_closeout(self.root, args, self.task_dir)
        auth.assert_called_once_with(self.root)
        archive.assert_not_called()
        ready.assert_not_called()

    def run_production_finish_case(
        self,
        failed_stage: str | None = None,
        *,
        archived_damage: str | None = None,
        expect_reentry_failure: bool = False,
        create_mismatched_commit: bool = False,
        plan_only_boundary_fault: str | None = None,
        pre_move_fault: str | None = None,
        formal_month_fault: bool = False,
        recover_pre_move_fault: bool = False,
        after_archive_hook: bool = False,
        archive_locator_conflict: bool = False,
        children_case: str | None = None,
        archived_pr_replacement: bool = False,
        predecessor_draft_metadata: bool = False,
        migrated_tracked_plan: bool = False,
        archived_legacy_without_predecessor: bool = False,
        reviewed_task_metadata_tail: bool = False,
    ) -> dict[str, object]:
        source_root = Path(__file__).resolve().parents[5]
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "project"
            remote = base / "remote.git"
            root.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
            subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=root, check=True)

            shutil.copytree(source_root / ".trellis/scripts", root / ".trellis/scripts")
            shutil.copytree(
                source_root / "trellis/workflows/guru-team/schemas",
                root / "trellis/workflows/guru-team/schemas",
            )
            publication_schema = (
                source_root
                / "trellis/skills/guru-team/packages/guru-review-task-publication/schemas/pr-readiness.schema.json"
            )
            installed_publication_schema = (
                root
                / "trellis/skills/guru-team/packages/guru-review-task-publication/schemas/pr-readiness.schema.json"
            )
            installed_publication_schema.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(publication_schema, installed_publication_schema)
            workflow = root / "trellis/workflows/guru-team/workflow.md"
            workflow.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_root / "trellis/workflows/guru-team/workflow.md", workflow)
            config = root / ".trellis/guru-team/config.yml"
            config.parent.mkdir(parents=True, exist_ok=True)
            config.write_text("github_repo: owner/repo\npublish:\n  remote: origin\n", encoding="utf-8")
            hook_sentinel = root / "after-archive-hook-sentinel"
            if after_archive_hook:
                (root / ".trellis/config.yaml").write_text(
                    f"hooks:\n  after_archive:\n    - \"touch {hook_sentinel}\"\n",
                    encoding="utf-8",
                )
            (root / ".gitignore").write_text(".trellis/.runtime/\n.trellis/workspace/\n", encoding="utf-8")
            (root / "README.md").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)
            subprocess.run(["git", "push", "-qu", "origin", "main"], cwd=root, check=True)
            base_head = gtt.run_stdout(["git", "rev-parse", "HEAD"], cwd=root)
            subprocess.run(["git", "switch", "-qc", "fix/105-closeout"], cwd=root, check=True)

            task_dir = root / ".trellis/tasks/07-11-closeout"
            task_dir.mkdir(parents=True)
            context = {
                "schema_version": "1.0",
                "source_issue": {
                    "number": 105,
                    "url": "https://github.com/owner/repo/issues/105",
                    "title": "closeout",
                    "created_by_workflow": False,
                },
                "source_repo": {"repo": "owner/repo", "url": "https://github.com/owner/repo"},
                "task_slug": "105-closeout",
                "task_title": "#105 closeout",
                "task_artifact_dir": ".trellis/tasks/07-11-closeout",
                "branch_name": "fix/105-closeout",
                "base_branch": "main",
                "base_ref": "main",
                "base_head_sha": base_head,
                "remote_head_sha": base_head,
                "workspace_slug": "105-closeout",
                "task_workspace_id": "105-closeout",
                "assignee": "test",
                "actor": {"login": "test"},
                "issue_scope_ledger_seed": {},
                "intake_summary": {},
            }
            task = {
                "id": "105-closeout",
                "name": "105-closeout",
                "title": "#105 closeout",
                "status": "in_progress",
                "branch": "fix/105-closeout",
                "base_branch": "main",
            }
            if children_case == "malformed":
                task["children"] = {"invalid": "not-list-str"}
            elif children_case in {"active", "archived"}:
                task["children"] = ["07-10-child"]
            issue = {
                "number": 105,
                "url": "https://github.com/owner/repo/issues/105",
                "title": "closeout",
                "reason": "Primary delivered scope.",
            }
            ledger = {
                "schema_version": "2.0",
                "primary_issue": issue,
                "close_issues": [issue],
                "related_issues": [],
                "followup_issues": [],
            }
            publication_title = "#105 重构 finish-work 收尾事务"
            publication_body = valid_pr_body("生产 closeout 集成。").replace(
                "Closes #18", "Closes #105"
            )
            gtt.write_json(task_dir / "task.json", task)
            gtt.write_runtime_mappings(
                root,
                gtt.load_config(root),
                {
                    "workspace_slug": "105-closeout",
                    "task_slug": "105-closeout",
                    "task_dir": ".trellis/tasks/07-11-closeout",
                    "branch_name": "fix/105-closeout",
                },
                root,
            )
            if children_case in {"active", "archived"}:
                child_parent = (
                    task_dir.parent
                    if children_case == "active"
                    else task_dir.parent / "archive" / datetime.now().strftime("%Y-%m")
                )
                child_dir = child_parent / "07-10-child"
                child_dir.mkdir(parents=True)
                gtt.write_json(
                    child_dir / "task.json",
                    {
                        "id": "child",
                        "name": "child",
                        "status": "completed" if children_case == "archived" else "in_progress",
                        "parent": task_dir.name,
                        "children": [],
                    },
                )
            gtt.write_json(task_dir / "issue-scope-ledger.json", ledger)
            (task_dir / "check.jsonl").write_text(
                '{"kind":"phase2-evidence","status":"passed"}\n',
                encoding="utf-8",
            )
            for name, content in {
                "prd.md": "# 需求\n\n验证 production closeout fixture。\n",
                "design.md": "# 设计\n\n## Docs SSOT Plan\n\nStrategy: no_docs_update_needed。\n",
                "implement.md": "# 实施\n\n验证 production closeout fixture。\n",
            }.items():
                (task_dir / name).write_text(content, encoding="utf-8")
            reviewed_paths = [".trellis/tasks"]
            subprocess.run(
                ["git", "add", "--", *reviewed_paths],
                cwd=root,
                check=True,
            )
            subprocess.run(["git", "commit", "-qm", "reviewed"], cwd=root, check=True)
            branch_review_commit = gtt.run_stdout(["git", "rev-parse", "HEAD"], cwd=root)
            publication_gate = self.current_publication_owner(
                task_ref=".trellis/tasks/07-11-closeout",
                branch_review_commit=branch_review_commit,
            )
            publication_gate["pr_payload"] = {
                "title": publication_title,
                "body": publication_body,
            }
            gtt.write_json(gtt.task_publication_path(root, task_dir), publication_gate)
            if reviewed_task_metadata_tail:
                task["meta"] = {"publication_round": "reviewed-tail"}
                (task_dir / "task.json").write_text(
                    json.dumps(task, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )

            if migrated_tracked_plan:
                current_plan = gtt.build_closeout_plan(
                    root,
                    task_dir,
                    context,
                    task,
                    ledger,
                    repo="owner/repo",
                    remote="origin",
                    base_branch="main",
                    head_branch="fix/105-closeout",
                    branch_review_commit=branch_review_commit,
                    title=publication_title,
                    body=publication_body,
                    review_facts=gtt.closeout_reviewed_change_facts(
                        root,
                        context,
                        branch_review_commit,
                    ),
                )
                legacy_plan = self.legacy_plan_from_current(
                    current_plan,
                    body=publication_body,
                )
                gtt.write_json(
                    task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT,
                    legacy_plan,
                )
                subprocess.run(
                    ["git", "add", "--", str(task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT)],
                    cwd=root,
                    check=True,
                )
                subprocess.run(
                    ["git", "commit", "-qm", "legacy tracked closeout plan"],
                    cwd=root,
                    check=True,
                )
                subprocess.run(
                    ["git", "push", "-qu", "origin", "fix/105-closeout"],
                    cwd=root,
                    check=True,
                )

            immutable_body_bytes = publication_body.encode("utf-8")
            pr_store: dict[str, object] = {}
            draft_rebind_body_bytes: list[bytes] = []
            if predecessor_draft_metadata:
                pr_store.update({
                    **closeout_head_repository_fields(),
                    "number": 105,
                    "url": "https://github.com/owner/repo/pull/105",
                    "title": "predecessor Round title",
                    "body": "predecessor Round body\n",
                    "isDraft": True,
                    "state": "OPEN",
                    "headRefOid": (
                        gtt.current_head(root)
                        if migrated_tracked_plan
                        else branch_review_commit
                    ),
                })
            original_run = gtt.run
            injected_stage = failed_stage
            active_plan_only_boundary_fault: str | None = None
            archive_pushed = False
            archived_legacy_plan_digest: str | None = None
            transition_attempts: list[str] = []
            actual_archive_month = datetime.now().strftime("%Y-%m")
            archive_month_clock = actual_archive_month

            def following_month(value: str) -> str:
                year, month = (int(part) for part in value.split("-"))
                return f"{year + (1 if month == 12 else 0):04d}-{1 if month == 12 else month + 1:02d}"

            def preceding_month(value: str) -> str:
                year, month = (int(part) for part in value.split("-"))
                return f"{year - (1 if month == 1 else 0):04d}-{12 if month == 1 else month - 1:02d}"

            if pre_move_fault == "archive-month" and recover_pre_move_fault:
                archive_month_clock = preceding_month(actual_archive_month)
            if failed_stage == "raw-remote-control":
                original_run(
                    [
                        "git",
                        "config",
                        "--replace-all",
                        "remote.origin.url",
                        " " + str(remote),
                    ],
                    cwd=root,
                    check=True,
                )

            def record_transition(stage: str) -> None:
                transition_attempts.append(stage)

            original_compact_closeout_archive = gtt.compact_closeout_archive

            def compact_closeout_archive_with_failure(
                archive_dir: Path, plan: dict[str, object]
            ) -> None:
                if failed_stage == "archive-prune":
                    record_transition("archive-prune")
                if injected_stage == "archive-prune":
                    raise gtt.WorkflowError(
                        "injected archive compaction failure", exit_code=2
                    )
                original_compact_closeout_archive(archive_dir, plan)

            def git_transition_stage(command: list[str]) -> str:
                archived = root / f".trellis/tasks/archive/{datetime.now().strftime('%Y-%m')}/{task_dir.name}"
                if archived.is_dir() or (
                    (task_dir / "task.json").is_file()
                    and gtt.read_json(task_dir / "task.json").get("status") == "completed"
                ):
                    return "archive-push" if command[:2] == ["git", "push"] else "archive-commit"
                if (task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT).is_file():
                    return "pre-archive-push" if command[:2] == ["git", "push"] else "pre-archive-commit"
                return "content-push"

            def command_failure(command: list[str], check: bool, message: str) -> subprocess.CompletedProcess[str]:
                if check:
                    raise subprocess.CalledProcessError(1, command, stderr=message)
                return subprocess.CompletedProcess(command, 1, "", message)

            def fake_external_run(
                command: list[str], cwd: Path | None = None, check: bool = True
            ) -> subprocess.CompletedProcess[str]:
                nonlocal archive_pushed, archive_month_clock
                if (
                    command == ["git", "rev-parse", "--show-toplevel"]
                    and active_plan_only_boundary_fault == "root"
                ):
                    return subprocess.CompletedProcess(
                        command, 0, str(root.parent / "wrong-root") + "\n", ""
                    )
                if (
                    command
                    == [
                        "git",
                        "config",
                        "--null",
                        "--show-origin",
                        "--get-all",
                        "remote.origin.url",
                    ]
                    and injected_stage == "raw-remote-control"
                ):
                    record_transition("raw-remote-control")
                if command in [
                    ["git", "remote", "get-url", "--all", "origin"],
                    ["git", "remote", "get-url", "--push", "--all", "origin"],
                ]:
                    if active_plan_only_boundary_fault == "repo":
                        return subprocess.CompletedProcess(
                            command,
                            0,
                            "https://github.com/wrong-owner/repo.git\n",
                            "",
                        )
                    if (
                        injected_stage in {"remote-identity", "remote-transport"}
                        and "--push" in command
                    ):
                        record_transition(str(injected_stage))
                        value = (
                            "owner/repo"
                            if injected_stage == "remote-transport"
                            else "https://github.com/fork-owner/repo.git"
                        )
                        return subprocess.CompletedProcess(
                            command, 0, value + "\n", ""
                        )
                    return subprocess.CompletedProcess(
                        command, 0, "https://github.com/owner/repo.git\n", ""
                    )
                if command[:2] == ["git", "push"]:
                    stage = git_transition_stage(command)
                    record_transition(stage)
                    if injected_stage == stage:
                        return command_failure(command, check, f"injected {stage}")
                    result = original_run(command, cwd=cwd, check=check)
                    if stage == "archive-push":
                        archive_pushed = True
                    if pr_store:
                        remote_head = original_run(
                            ["git", "ls-remote", "--heads", "origin", "fix/105-closeout"],
                            cwd=root,
                            check=True,
                        ).stdout.split()[0]
                        pr_store["headRefOid"] = remote_head
                    return result
                if (
                    command[:2] == ["git", "add"]
                    and injected_stage == "archive-summary-tamper"
                    and archived_path.is_dir()
                ):
                    result = original_run(command, cwd=cwd, check=check)
                    original_run(["git", "reset"], cwd=root, check=True)
                    summary_path = archived_path / gtt.FINISH_SUMMARY_ARTIFACT
                    summary = gtt.read_json(summary_path)
                    summary["index"]["outcome"] = "tampered after archive move and index loss"
                    gtt.write_json(summary_path, summary)
                    record_transition("archive-summary-tamper")
                    return result
                if command[:2] == ["git", "commit"]:
                    stage = git_transition_stage(command)
                    record_transition(stage)
                    if injected_stage == stage:
                        return command_failure(command, check, f"injected {stage}")
                if (
                    command[:3] == ["git", "ls-remote", "--heads"]
                    and archive_pushed
                ):
                    record_transition("remote-head")
                    if injected_stage == "remote-head":
                        return subprocess.CompletedProcess(
                            command, 0, f"{'0' * 40}\trefs/heads/fix/105-closeout\n", ""
                        )
                if command[:3] == ["gh", "auth", "status"]:
                    return subprocess.CompletedProcess(command, 0, "", "")
                if command[:3] == ["gh", "pr", "create"]:
                    record_transition("draft")
                    if injected_stage == "draft":
                        return subprocess.CompletedProcess(command, 1, "", "injected draft")
                    body_path = Path(command[command.index("--body-file") + 1])
                    remote_head = original_run(
                        ["git", "ls-remote", "--heads", "origin", "fix/105-closeout"],
                        cwd=root,
                        check=True,
                    ).stdout.split()[0]
                    pr_store.update({
                        **closeout_head_repository_fields(),
                        "number": 105,
                        "url": "https://github.com/owner/repo/pull/105",
                        "title": command[command.index("--title") + 1],
                        "body": body_path.read_text(encoding="utf-8"),
                        "isDraft": True,
                        "state": "OPEN",
                        "headRefOid": remote_head,
                    })
                    if pre_move_fault == "tracked-content":
                        (task_dir / "check.jsonl").write_text(
                            "tampered after draft binding\n", encoding="utf-8"
                        )
                    elif pre_move_fault == "tracked-symlink":
                        check_path = task_dir / "check.jsonl"
                        check_path.unlink()
                        check_path.symlink_to(root / "README.md")
                    elif pre_move_fault == "tracked-mode":
                        check_path = task_dir / "check.jsonl"
                        check_path.chmod(check_path.stat().st_mode | stat.S_IXUSR)
                    elif pre_move_fault == "unexpected-untracked":
                        (root / "unexpected-closeout.txt").write_text(
                            "unexpected\n", encoding="utf-8"
                        )
                    elif pre_move_fault == "unexpected-staged":
                        unexpected = root / "unexpected-staged-closeout.txt"
                        unexpected.write_text("unexpected staged\n", encoding="utf-8")
                        original_run(["git", "add", unexpected.name], cwd=root, check=True)
                    elif pre_move_fault == "archive-month":
                        archive_month_clock = following_month(archive_month_clock)
                    if injected_stage == "projection":
                        record_transition("projection")
                        (task_dir / "check.jsonl").unlink()
                    return subprocess.CompletedProcess(command, 0, str(pr_store["url"]) + "\n", "")
                if command[:3] == ["gh", "pr", "list"]:
                    if injected_stage == "fork-candidate" and not pr_store:
                        remote_head = original_run(
                            ["git", "ls-remote", "--heads", "origin", "fix/105-closeout"],
                            cwd=root,
                            check=True,
                        ).stdout.split()[0]
                        payload = [{
                            **closeout_head_repository_fields(
                                "fork-owner/repo", cross_repository=True
                            ),
                            "number": 106,
                            "url": "https://github.com/owner/repo/pull/106",
                            "title": "#105 重构 finish-work 收尾事务",
                            "body": publication_body,
                            "isDraft": True,
                            "state": "OPEN",
                            "headRefOid": remote_head,
                            "headRefName": "fix/105-closeout",
                            "baseRefName": "main",
                        }]
                    elif not pr_store:
                        payload: list[dict[str, object]] = []
                    else:
                        payload = [{
                            **pr_store,
                            "headRefName": "fix/105-closeout",
                            "baseRefName": "main",
                        }]
                    return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")
                if command[:3] == ["gh", "pr", "edit"]:
                    record_transition("draft-rebind")
                    self.assertEqual(command[3], str(pr_store["number"]))
                    self.assertEqual(
                        command[command.index("--repo") + 1], "owner/repo"
                    )
                    if injected_stage == "draft-rebind":
                        return subprocess.CompletedProcess(
                            command, 1, "", "injected draft rebind"
                        )
                    body_path = Path(command[command.index("--body-file") + 1])
                    body_bytes = body_path.read_bytes()
                    draft_rebind_body_bytes.append(body_bytes)
                    pr_store["title"] = command[command.index("--title") + 1]
                    pr_store["body"] = body_bytes.decode("utf-8")
                    return subprocess.CompletedProcess(command, 0, "", "")
                if command[:3] == ["gh", "pr", "ready"]:
                    record_transition("ready")
                    if injected_stage == "ready":
                        return subprocess.CompletedProcess(command, 1, "", "injected ready")
                    pr_store["isDraft"] = False
                    return subprocess.CompletedProcess(command, 0, "", "")
                if (
                    len(command) >= 4
                    and command[:3] == ["python3", "./.trellis/scripts/task.py", "archive"]
                ):
                    if "projection" not in transition_attempts:
                        record_transition("projection")
                    record_transition("archive-move")
                    if injected_stage == "archive-move":
                        return subprocess.CompletedProcess(command, 1, "", "injected archive move")
                    return original_run(
                        command,
                        cwd=cwd,
                        check=check,
                        env={"PYTHONDONTWRITEBYTECODE": "1"},
                    )
                if command and command[0].endswith("/trellis/presets/guru-team/scripts/bash/apply.sh"):
                    return subprocess.CompletedProcess(command, 0, "", "")
                return original_run(command, cwd=cwd, check=check)

            archive_locator = f".trellis/tasks/archive/{datetime.now().strftime('%Y-%m')}/{task_dir.name}"
            archived_path = root / archive_locator
            if archive_locator_conflict:
                archived_path.mkdir(parents=True)

            def damage_archived_worktree(mode: str) -> None:
                if not archived_path.is_dir():
                    raise AssertionError("archive damage requires the official move to have completed")
                if mode in {"delete", "delete-retain-plan"}:
                    for path in list(archived_path.iterdir()):
                        keep = {gtt.CLOSEOUT_PLAN_ARTIFACT}
                        if path.name in keep:
                            continue
                        if path.is_dir():
                            shutil.rmtree(path)
                        else:
                            path.unlink()
                    return
                if mode == "tamper":
                    (archived_path / gtt.FINISH_SUMMARY_ARTIFACT).write_text(
                        "invalid committed summary\n", encoding="utf-8"
                    )
                    return
                plan_path = archived_path / gtt.CLOSEOUT_PLAN_ARTIFACT
                if mode == "plan-delete":
                    plan_path.unlink()
                    return
                if mode == "plan-tamper":
                    plan_path.write_text("not committed plan bytes\n", encoding="utf-8")
                    return
                if mode == "plan-invalid":
                    plan_path.write_text('{"schema_version":"invalid"}\n', encoding="utf-8")
                    return
                if mode == "plan-symlink":
                    plan_path.unlink()
                    plan_path.symlink_to(root / "README.md")
                    return
                raise AssertionError(f"unsupported archived damage mode: {mode}")

            def exact_state() -> dict[str, object]:
                local_head = gtt.run_stdout(["git", "rev-parse", "HEAD"], cwd=root)
                remote_proc = original_run(
                    ["git", "ls-remote", "--heads", "origin", "fix/105-closeout"],
                    cwd=root,
                    check=False,
                )
                rows = [line.split() for line in remote_proc.stdout.splitlines() if line.strip()]
                remote_head = rows[0][0] if len(rows) == 1 else None
                current_task_dir = task_dir if task_dir.is_dir() else archived_path if archived_path.is_dir() else None
                task_status: object = None
                if current_task_dir is not None and (current_task_dir / "task.json").is_file():
                    try:
                        task_status = gtt.read_json(current_task_dir / "task.json").get("status")
                    except (gtt.WorkflowError, json.JSONDecodeError):
                        task_status = "invalid"
                return {
                    "active_locator": ".trellis/tasks/07-11-closeout" if task_dir.is_dir() else None,
                    "active_path": str(task_dir) if task_dir.is_dir() else None,
                    "archive_locator": archive_locator if archived_path.is_dir() else None,
                    "archive_path": str(archived_path) if archived_path.is_dir() else None,
                    "task_status": task_status,
                    "dirty_paths": set(gtt.git_status_paths(root)),
                    "staged_paths": set(
                        gtt.run_stdout(
                            ["git", "diff", "--cached", "--name-only", "--no-renames"], cwd=root
                        ).splitlines()
                    ),
                    "local_sha": local_head,
                    "remote_sha": remote_head,
                    "pr_head_sha": pr_store.get("headRefOid"),
                    "pr_is_draft": pr_store.get("isDraft"),
                    "pr_state": pr_store.get("state"),
                    "pr_number": pr_store.get("number"),
                    "finish_summary_exists": (
                        current_task_dir is not None
                        and (current_task_dir / gtt.FINISH_SUMMARY_ARTIFACT).is_file()
                    ),
                    "ledger_bytes": (
                        (task_dir / "issue-scope-ledger.json").read_bytes()
                        if (task_dir / "issue-scope-ledger.json").is_file()
                        else None
                    ),
                    "plan_bytes": (
                        (task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT).read_bytes()
                        if (task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT).is_file()
                        else None
                    ),
                    "readiness_bytes": (
                        (task_dir / gtt.PR_READINESS_ARTIFACT).read_bytes()
                        if (task_dir / gtt.PR_READINESS_ARTIFACT).is_file()
                        else None
                    ),
                }

            dry_args = finish_args(
                root=str(root),
                task=str(task_dir),
                repo="owner/repo",
                base_branch="main",
                remote="origin",
                title=publication_title,
                publication_ready={
                    "profile": "publication_ready",
                    "mode": "workflow",
                    "task_ref": ".trellis/tasks/07-11-closeout",
                    "branch_review_commit": branch_review_commit,
                    "pr_title": publication_title,
                    "pr_body": publication_body,
                },
                dry_run=True,
            )
            with (
                mock.patch.object(
                    gtt,
                    "cmd_check_task_publication_review",
                    return_value={
                        "status": "ok",
                        "typed_exit": "ready",
                        "branch_review_commit": branch_review_commit,
                        "owner_result": publication_gate,
                    },
                ),
                mock.patch.object(gtt, "run", side_effect=fake_external_run),
                mock.patch.object(
                    gtt,
                    "compact_closeout_archive",
                    side_effect=compact_closeout_archive_with_failure,
                ),
                mock.patch.object(gtt, "current_archive_month", side_effect=lambda: archive_month_clock),
            ):
                if (
                    archive_locator_conflict
                    or children_case in {"active", "malformed"}
                ):
                    before = exact_state()
                    errors: list[gtt.WorkflowError] = []
                    for failure_args in (
                        dry_args,
                        finish_args(
                            **{
                                **vars(dry_args),
                                "dry_run": False,
                                "expected_plan_digest": "0" * 64,
                            }
                        ),
                    ):
                        with self.assertRaises(gtt.WorkflowError) as failure:
                            gtt.cmd_finish_work(failure_args)
                        errors.append(failure.exception)
                        self.assertEqual(exact_state(), before)
                    return {
                        "failed_state": before,
                        "errors": errors,
                        "events": transition_attempts,
                        "branch_review_commit": branch_review_commit,
                        "archive_locator": archive_locator,
                    }
                if after_archive_hook:
                    with self.assertRaises(gtt.WorkflowError) as hook_error:
                        gtt.cmd_finish_work(dry_args)
                    return {
                        "failed_state": exact_state(),
                        "error": str(hook_error.exception),
                        "error_payload": hook_error.exception.payload,
                        "sentinel_exists": hook_sentinel.exists(),
                        "events": transition_attempts,
                        "branch_review_commit": branch_review_commit,
                    }
                if failed_stage in {
                    "prepare",
                    "raw-remote-control",
                    "remote-identity",
                    "remote-transport",
                }:
                    if failed_stage == "prepare":
                        dry_args.publication_ready["pr_body"] = "invalid body"
                    with self.assertRaises(gtt.WorkflowError):
                        gtt.cmd_finish_work(dry_args)
                    failed_state = exact_state()
                    if failed_stage == "prepare":
                        dry_args.publication_ready["pr_body"] = publication_body
                    if failed_stage == "raw-remote-control":
                        original_run(
                            [
                                "git",
                                "config",
                                "--replace-all",
                                "remote.origin.url",
                                str(remote),
                            ],
                            cwd=root,
                            check=True,
                        )
                    injected_stage = None
                    reentry_offset = len(transition_attempts)
                    preview = gtt.cmd_finish_work(dry_args)
                    if failed_stage == "prepare":
                        transition_attempts.insert(reentry_offset, "prepare")
                    formal_args = finish_args(
                        **{
                            **vars(dry_args),
                            "dry_run": False,
                            "expected_plan_digest": preview["closeout_plan_digest"],
                        }
                    )
                    result = gtt.cmd_finish_work(formal_args)
                    reentry_events = transition_attempts[reentry_offset:]
                else:
                    try:
                        preview = gtt.cmd_finish_work(dry_args)
                    except gtt.WorkflowError as exc:
                        self.fail(f"production preview failed: {exc}; payload={exc.payload}")
                    formal_args = finish_args(
                        **{
                            **vars(dry_args),
                            "dry_run": False,
                            "expected_plan_digest": preview["closeout_plan_digest"],
                        }
                    )
                    if failed_stage == "plan-digest":
                        formal_args.expected_plan_digest = "0" * 64
                    if formal_month_fault:
                        archive_month_clock = following_month(archive_month_clock)
                        with self.assertRaises(gtt.WorkflowError) as month_error:
                            gtt.cmd_finish_work(formal_args)
                        return {
                            "failed_state": exact_state(),
                            "error": str(month_error.exception),
                            "error_payload": month_error.exception.payload,
                            "events": transition_attempts,
                            "branch_review_commit": branch_review_commit,
                        }
                    if pre_move_fault is not None:
                        with self.assertRaises(gtt.WorkflowError) as pre_move_error:
                            gtt.cmd_finish_work(formal_args)
                        failed_state = exact_state()
                        failed_error = str(pre_move_error.exception)
                        failed_payload = pre_move_error.exception.payload
                        failed_events = list(transition_attempts)
                        if not recover_pre_move_fault:
                            return {
                                "project_root": str(root),
                                "failed_state": failed_state,
                                "error": failed_error,
                                "error_payload": failed_payload,
                                "events": failed_events,
                                "branch_review_commit": branch_review_commit,
                                "archive_parent_sha": gtt.run_stdout(["git", "rev-parse", "HEAD"], cwd=root),
                            }
                        reentry_offset = len(transition_attempts)
                        replacement_preview = gtt.cmd_finish_work(dry_args)
                        self.assertNotEqual(
                            replacement_preview["closeout_plan_digest"],
                            preview["closeout_plan_digest"],
                        )
                        formal_args.expected_plan_digest = replacement_preview["closeout_plan_digest"]
                        result = gtt.cmd_finish_work(formal_args)
                        reentry_events = transition_attempts[reentry_offset:]
                    if recover_pre_move_fault and pre_move_fault is not None:
                        pass
                    elif failed_stage is None:
                        result = gtt.cmd_finish_work(formal_args)
                        failed_state = {}
                        reentry_events = []
                    else:
                        with self.assertRaises((gtt.WorkflowError, subprocess.CalledProcessError)):
                            gtt.cmd_finish_work(formal_args)
                        failed_state = exact_state()
                        if archived_legacy_without_predecessor:
                            self.assertEqual(failed_stage, "ready")
                            archived_plan_path = (
                                archived_path / gtt.CLOSEOUT_PLAN_ARTIFACT
                            )
                            archived_plan = gtt.read_json(archived_plan_path)
                            archived_plan["projection"].pop(
                                "migration_predecessor_plan_digest"
                            )
                            archived_plan["plan_digest"] = gtt.closeout_plan_digest(
                                archived_plan
                            )
                            gtt.validate_closeout_plan_for_migration(archived_plan)
                            gtt.write_json(archived_plan_path, archived_plan)
                            original_run(
                                ["git", "add", "--", str(archived_plan_path)],
                                cwd=root,
                                check=True,
                            )
                            original_run(
                                ["git", "commit", "--amend", "--no-edit", "-q"],
                                cwd=root,
                                check=True,
                            )
                            original_run(
                                [
                                    "git",
                                    "push",
                                    "--force",
                                    "-q",
                                    "origin",
                                    "fix/105-closeout",
                                ],
                                cwd=root,
                                check=True,
                            )
                            amended_head = gtt.current_head(root)
                            pr_store["headRefOid"] = amended_head
                            formal_args.expected_plan_digest = archived_plan[
                                "plan_digest"
                            ]
                            archived_legacy_plan_digest = archived_plan[
                                "plan_digest"
                            ]
                        if create_mismatched_commit:
                            original_run(["git", "reset"], cwd=root, check=True)
                            mismatch = root / ".trellis/archive-mismatch-marker.txt"
                            mismatch.write_text("mismatched archive head\n", encoding="utf-8")
                            original_run(["git", "add", str(mismatch)], cwd=root, check=True)
                            original_run(
                                ["git", "commit", "-qm", "mismatched archive head"],
                                cwd=root,
                                check=True,
                            )
                        if archived_damage is not None:
                            damage_archived_worktree(archived_damage)
                        if archived_pr_replacement:
                            pr_store.update(
                                {
                                    "number": 106,
                                    "url": "https://github.com/owner/repo/pull/106",
                                    "isDraft": True,
                                    "state": "OPEN",
                                }
                            )
                        if plan_only_boundary_fault == "branch":
                            original_run(
                                ["git", "branch", "-m", "fix/105-wrong-branch"],
                                cwd=root,
                                check=True,
                            )
                        elif plan_only_boundary_fault == "config-repo":
                            config.write_text(
                                "github_repo: wrong-owner/repo\n"
                                "publish:\n"
                                "  remote: origin\n",
                                encoding="utf-8",
                            )
                        elif plan_only_boundary_fault == "head":
                            mismatch = root / ".trellis/plan-only-head-mismatch.txt"
                            mismatch.write_text("wrong head\n", encoding="utf-8")
                            original_run(["git", "add", str(mismatch)], cwd=root, check=True)
                            original_run(
                                ["git", "commit", "-qm", "plan-only wrong head"],
                                cwd=root,
                                check=True,
                            )
                        elif plan_only_boundary_fault in {
                            "committed-plan-delete",
                            "committed-plan-invalid",
                            "committed-plan-symlink",
                        }:
                            committed_plan_path = archived_path / gtt.CLOSEOUT_PLAN_ARTIFACT
                            if plan_only_boundary_fault == "committed-plan-delete":
                                committed_plan_path.unlink()
                            elif plan_only_boundary_fault == "committed-plan-invalid":
                                committed_plan_path.write_text(
                                    '{"schema_version":"invalid"}\n', encoding="utf-8"
                                )
                            else:
                                committed_plan_path.unlink()
                                committed_plan_path.symlink_to(root / "README.md")
                            original_run(["git", "add", "-A", "--", str(committed_plan_path)], cwd=root, check=True)
                            original_run(
                                ["git", "commit", "-qm", f"{plan_only_boundary_fault}"],
                                cwd=root,
                                check=True,
                            )
                        elif plan_only_boundary_fault == "locator":
                            wrong_archived = archived_path.parent / f"wrong-{archived_path.name}"
                            wrong_archived.mkdir(parents=True)
                            shutil.copy2(
                                archived_path / gtt.CLOSEOUT_PLAN_ARTIFACT,
                                wrong_archived / gtt.CLOSEOUT_PLAN_ARTIFACT,
                            )
                            original_run(
                                ["git", "add", str(wrong_archived / gtt.CLOSEOUT_PLAN_ARTIFACT)],
                                cwd=root,
                                check=True,
                            )
                            original_run(
                                ["git", "commit", "-qm", "plan-only wrong locator"],
                                cwd=root,
                                check=True,
                            )
                            formal_args.task = str(wrong_archived)
                        injected_stage = None
                        active_plan_only_boundary_fault = plan_only_boundary_fault
                        if failed_stage == "projection":
                            (task_dir / "check.jsonl").write_text(
                                '{"kind":"phase2-evidence","status":"passed"}\n',
                                encoding="utf-8",
                            )
                        formal_args.expected_plan_digest = (
                            archived_legacy_plan_digest
                            or preview["closeout_plan_digest"]
                        )
                        if plan_only_boundary_fault == "plan":
                            formal_args.expected_plan_digest = "0" * 64
                        reentry_offset = len(transition_attempts)
                        if failed_stage == "plan-digest":
                            transition_attempts.append("plan-digest")
                        if expect_reentry_failure:
                            with self.assertRaises(
                                (gtt.WorkflowError, subprocess.CalledProcessError)
                            ) as reentry_error:
                                gtt.cmd_finish_work(formal_args)
                            return {
                                "failed_state": failed_state,
                                "reentry_failed_state": exact_state(),
                                "reentry_error": str(reentry_error.exception),
                                "reentry_events": transition_attempts[reentry_offset:],
                                "all_transition_attempts": transition_attempts,
                                "branch_review_commit": branch_review_commit,
                            }
                        result = gtt.cmd_finish_work(formal_args)
                        if failed_stage == "projection":
                            transition_attempts.insert(reentry_offset, "projection")
                        reentry_events = transition_attempts[reentry_offset:]

            archived = archived_path
            local_head = gtt.run_stdout(["git", "rev-parse", "HEAD"], cwd=root)
            remote_head = gtt.run_stdout(
                ["git", "ls-remote", "--heads", "origin", "fix/105-closeout"], cwd=root
            ).split()[0]
            self.assertFalse(task_dir.exists())
            self.assertTrue(archived.is_dir())
            self.assertEqual(local_head, remote_head)
            self.assertEqual(pr_store["isDraft"], False)
            if archived_damage is None:
                self.assertEqual(gtt.read_json(archived / "task.json")["status"], "completed")
                if reviewed_task_metadata_tail:
                    self.assertEqual(
                        gtt.read_json(archived / "task.json")["meta"],
                        {"publication_round": "reviewed-tail"},
                    )
                self.assertEqual(
                    gtt.read_json(archived / gtt.FINISH_SUMMARY_ARTIFACT)["github"]["pr_url"],
                    pr_store["url"],
                )
                self.assertEqual(gtt.git_status_paths(root), [])
            else:
                self.assertTrue(gtt.git_status_paths(root))
            final_state = exact_state()
            archive_parent_sha = gtt.run_stdout(["git", "rev-parse", f"{local_head}^"], cwd=root)
            return {
                "project_root": str(root),
                "failed_state": failed_state,
                "final_state": final_state,
                "reentry_events": reentry_events,
                "all_transition_attempts": transition_attempts,
                "branch_review_commit": branch_review_commit,
                "archive_parent_sha": archive_parent_sha,
                "archive_sha": local_head,
                "archive_paths": gtt.closeout_commit_paths(root, local_head),
                "immutable_body_bytes": immutable_body_bytes,
                "draft_rebind_body_bytes": draft_rebind_body_bytes,
                "archived_legacy_plan_digest": archived_legacy_plan_digest,
                "archived_files": sorted(
                    path.relative_to(archived).as_posix()
                    for path in archived.rglob("*")
                    if path.is_file()
                ),
            }

    def test_production_finish_entry_uses_real_git_remote_and_fake_github_store(self) -> None:
        result = self.run_production_finish_case()
        final = result["final_state"]
        self.assertIsNone(final["active_locator"])
        self.assertEqual(
            final["archive_locator"],
            f".trellis/tasks/archive/{datetime.now().strftime('%Y-%m')}/07-11-closeout",
        )
        self.assertEqual(final["task_status"], "completed")
        self.assertEqual(final["dirty_paths"], set())
        self.assertEqual(final["staged_paths"], set())
        self.assertEqual(final["local_sha"], result["archive_sha"])
        self.assertEqual(final["remote_sha"], result["archive_sha"])
        self.assertEqual(final["pr_head_sha"], result["archive_sha"])
        self.assertEqual(final["pr_is_draft"], False)
        self.assertEqual(final["pr_state"], "OPEN")
        self.assertEqual(
            result["archived_files"],
            [
                "closeout-plan.json",
                "design.md",
                "finish-summary.json",
                "implement.md",
                "issue-scope-ledger.json",
                "prd.md",
                "task.json",
            ],
        )
        self.assertEqual(len(result["archived_files"]), 7)

    def test_production_predecessor_draft_rebinds_same_number_after_content_push(self) -> None:
        result = self.run_production_finish_case(predecessor_draft_metadata=True)
        final = result["final_state"]
        events = result["all_transition_attempts"]

        self.assertEqual(final["pr_number"], 105)
        self.assertEqual(final["pr_is_draft"], False)
        self.assertNotIn("draft", events)
        self.assertEqual(events.count("draft-rebind"), 1)
        self.assertLess(events.index("content-push"), events.index("draft-rebind"))
        self.assertNotIn("pre-archive-push", events)
        self.assertLess(events.index("draft-rebind"), events.index("projection"))
        self.assertEqual(
            result["draft_rebind_body_bytes"],
            [result["immutable_body_bytes"]],
        )
        self.assertEqual(
            hashlib.sha256(result["draft_rebind_body_bytes"][0]).hexdigest(),
            hashlib.sha256(result["immutable_body_bytes"]).hexdigest(),
        )

    def test_production_draft_rebind_failure_retries_same_plan_before_archive(self) -> None:
        result = self.run_production_finish_case(
            failed_stage="draft-rebind",
            predecessor_draft_metadata=True,
        )
        failed = result["failed_state"]
        final = result["final_state"]

        self.assertEqual(failed["active_locator"], ".trellis/tasks/07-11-closeout")
        self.assertIsNone(failed["archive_locator"])
        self.assertEqual(failed["task_status"], "in_progress")
        self.assertEqual(failed["pr_number"], 105)
        self.assertEqual(failed["pr_is_draft"], True)
        self.assertEqual(final["pr_number"], 105)
        self.assertEqual(final["pr_is_draft"], False)
        self.assertIn("draft-rebind", result["reentry_events"])
        self.assertNotIn("draft", result["all_transition_attempts"])
        self.assertEqual(
            result["draft_rebind_body_bytes"],
            [result["immutable_body_bytes"]],
        )

    def test_production_migrated_tracked_plan_recovers_ready_after_archive(self) -> None:
        result = self.run_production_finish_case(
            failed_stage="ready",
            predecessor_draft_metadata=True,
            migrated_tracked_plan=True,
        )
        failed = result["failed_state"]
        final = result["final_state"]
        self.assertIsNone(failed["active_locator"])
        self.assertIsNotNone(failed["archive_locator"])
        self.assertTrue(failed["pr_is_draft"])
        self.assertEqual(final["pr_number"], 105)
        self.assertFalse(final["pr_is_draft"])
        self.assertEqual(final["local_sha"], result["archive_sha"])
        self.assertEqual(final["remote_sha"], result["archive_sha"])
        self.assertIsNone(result["archived_legacy_plan_digest"])
        self.assertIn("ready", result["reentry_events"])
        self.assertNotIn("draft", result["all_transition_attempts"])

    def test_production_reviewed_task_metadata_tail_recovers_from_archive_commit(self) -> None:
        result = self.run_production_finish_case(
            failed_stage="ready",
            reviewed_task_metadata_tail=True,
        )
        failed = result["failed_state"]
        final = result["final_state"]
        self.assertIsNone(failed["active_locator"])
        self.assertIsNotNone(failed["archive_locator"])
        self.assertEqual(failed["task_status"], "completed")
        self.assertTrue(failed["pr_is_draft"])
        self.assertEqual(final["local_sha"], result["archive_sha"])
        self.assertEqual(final["remote_sha"], result["archive_sha"])
        self.assertFalse(final["pr_is_draft"])
        self.assertIn("ready", result["reentry_events"])

    def test_production_finish_recovers_after_move_before_archive_compaction(self) -> None:
        result = self.run_production_finish_case("archive-prune")
        failed = result["failed_state"]
        self.assertIsNone(failed["active_locator"])
        self.assertIsNotNone(failed["archive_locator"])
        self.assertIn(
            f"{failed['archive_locator']}/check.jsonl",
            failed["dirty_paths"],
        )
        self.assertEqual(len(result["archived_files"]), 7)
        self.assertNotIn("check.jsonl", result["archived_files"])
        self.assertGreaterEqual(result["all_transition_attempts"].count("archive-prune"), 2)

    def test_production_existing_archive_locator_fails_dry_run_and_formal_without_side_effects(self) -> None:
        result = self.run_production_finish_case(archive_locator_conflict=True)
        state = result["failed_state"]
        self.assertEqual(state["active_locator"], ".trellis/tasks/07-11-closeout")
        self.assertEqual(state["archive_locator"], result["archive_locator"])
        self.assertEqual(state["task_status"], "in_progress")
        self.assertEqual(state["local_sha"], result["branch_review_commit"])
        self.assertIsNone(state["remote_sha"])
        self.assertIsNone(state["pr_number"])
        self.assertIsNone(state["plan_bytes"])
        self.assertIsNone(state["readiness_bytes"])
        self.assertEqual(result["events"], [])
        self.assertEqual(
            [error.payload.get("stage") for error in result["errors"]],
            ["archive-locator-preflight", "archive-locator-preflight"],
        )

    def test_production_archived_child_allows_parent_closeout(self) -> None:
        result = self.run_production_finish_case(children_case="archived")
        final = result["final_state"]
        self.assertIsNone(final["active_locator"])
        self.assertEqual(final["task_status"], "completed")
        self.assertEqual(final["local_sha"], result["archive_sha"])
        self.assertEqual(final["remote_sha"], result["archive_sha"])
        self.assertEqual(final["pr_head_sha"], result["archive_sha"])
        self.assertEqual(final["pr_is_draft"], False)

    def test_production_active_child_fails_before_side_effects(self) -> None:
        result = self.run_production_finish_case(children_case="active")
        state = result["failed_state"]
        self.assertEqual(state["active_locator"], ".trellis/tasks/07-11-closeout")
        self.assertIsNone(state["archive_locator"])
        self.assertEqual(state["task_status"], "in_progress")
        self.assertEqual(state["local_sha"], result["branch_review_commit"])
        self.assertIsNone(state["remote_sha"])
        self.assertIsNone(state["pr_number"])
        self.assertIsNone(state["plan_bytes"])
        self.assertIsNone(state["readiness_bytes"])
        self.assertEqual(result["events"], [])
        self.assertEqual(
            [error.payload.get("active_children") for error in result["errors"]],
            [["07-10-child"], ["07-10-child"]],
        )

    def test_production_malformed_children_type_fails_before_side_effects(self) -> None:
        result = self.run_production_finish_case(children_case="malformed")
        state = result["failed_state"]
        self.assertEqual(state["active_locator"], ".trellis/tasks/07-11-closeout")
        self.assertIsNone(state["archive_locator"])
        self.assertEqual(state["task_status"], "in_progress")
        self.assertEqual(state["local_sha"], result["branch_review_commit"])
        self.assertIsNone(state["remote_sha"])
        self.assertIsNone(state["pr_number"])
        self.assertIsNone(state["plan_bytes"])
        self.assertIsNone(state["readiness_bytes"])
        self.assertEqual(result["events"], [])
        self.assertEqual(
            [error.payload.get("stage") for error in result["errors"]],
            ["task-children-preflight", "task-children-preflight"],
        )

    def test_production_pre_move_continuity_failures_keep_task_active_and_pr_draft(self) -> None:
        cases = [
            "tracked-content",
            "tracked-symlink",
            "tracked-mode",
            "unexpected-untracked",
            "unexpected-staged",
            "archive-month",
        ]
        for fault in cases:
            with self.subTest(fault=fault):
                result = self.run_production_finish_case(pre_move_fault=fault)
                state = result["failed_state"]
                self.assertEqual(state["active_locator"], ".trellis/tasks/07-11-closeout")
                self.assertIsNone(state["archive_locator"])
                self.assertEqual(state["task_status"], "in_progress")
                self.assertEqual(state["local_sha"], result["archive_parent_sha"])
                self.assertEqual(state["remote_sha"], result["archive_parent_sha"])
                self.assertEqual(state["pr_head_sha"], result["archive_parent_sha"])
                self.assertEqual(state["pr_is_draft"], True)
                self.assertEqual(state["pr_state"], "OPEN")
                self.assertNotIn("archive-move", result["events"])
                self.assertIn(
                    result["error_payload"].get("stage"),
                    {"pre-archive-continuity", "archive-month-preflight", None},
                )

    def test_production_prepare_to_formal_month_change_fails_before_side_effects(self) -> None:
        result = self.run_production_finish_case(formal_month_fault=True)
        state = result["failed_state"]
        self.assertEqual(state["active_locator"], ".trellis/tasks/07-11-closeout")
        self.assertIsNone(state["archive_locator"])
        self.assertEqual(state["task_status"], "in_progress")
        self.assertEqual(state["local_sha"], result["branch_review_commit"])
        self.assertIsNone(state["remote_sha"])
        self.assertIsNone(state["pr_number"])
        self.assertEqual(result["events"], [])
        self.assertEqual(result["error_payload"].get("failed_stage"), "plan-digest-handshake")

    def test_production_after_archive_hook_is_rejected_before_execution_or_side_effects(self) -> None:
        result = self.run_production_finish_case(after_archive_hook=True)
        state = result["failed_state"]
        self.assertEqual(state["active_locator"], ".trellis/tasks/07-11-closeout")
        self.assertIsNone(state["archive_locator"])
        self.assertEqual(state["task_status"], "in_progress")
        self.assertEqual(state["local_sha"], result["branch_review_commit"])
        self.assertIsNone(state["remote_sha"])
        self.assertIsNone(state["pr_number"])
        self.assertFalse(result["sentinel_exists"])
        self.assertEqual(result["events"], [])
        self.assertEqual(result["error_payload"].get("stage"), "after-archive-hook-preflight")
        self.assertEqual(result["error_payload"].get("hook_executed"), False)

    def test_production_cross_month_reprepare_rebuilds_untracked_plan_without_commit(self) -> None:
        result = self.run_production_finish_case(
            pre_move_fault="archive-month",
            recover_pre_move_fault=True,
        )
        failed = result["failed_state"]
        final = result["final_state"]
        self.assertEqual(failed["active_locator"], ".trellis/tasks/07-11-closeout")
        self.assertIsNone(failed["archive_locator"])
        self.assertEqual(failed["task_status"], "in_progress")
        self.assertEqual(failed["pr_is_draft"], True)
        self.assertEqual(result["archive_parent_sha"], failed["local_sha"])
        self.assertNotIn("pre-archive-commit", result["all_transition_attempts"])
        self.assertNotIn("pre-archive-push", result["all_transition_attempts"])
        self.assertIsNone(final["active_locator"])
        self.assertEqual(
            final["archive_locator"],
            f".trellis/tasks/archive/{datetime.now().strftime('%Y-%m')}/07-11-closeout",
        )
        self.assertEqual(final["task_status"], "completed")
        self.assertEqual(final["pr_is_draft"], False)
        self.assertEqual(final["local_sha"], result["archive_sha"])
        self.assertEqual(final["remote_sha"], result["archive_sha"])
        self.assertEqual(final["pr_head_sha"], result["archive_sha"])

    def test_production_archived_reentry_uses_committed_git_facts_with_damaged_worktree(self) -> None:
        cases = [
            ("archive-push", "delete", None),
            ("ready", "tamper", "completed"),
            ("ready", "plan-delete", "completed"),
            ("ready", "plan-tamper", "completed"),
            ("ready", "plan-invalid", "completed"),
            ("ready", "plan-symlink", "completed"),
        ]
        for failed_stage, damage, expected_task_status in cases:
            with self.subTest(failed_stage=failed_stage, damage=damage):
                result = self.run_production_finish_case(
                    failed_stage,
                    archived_damage=damage,
                )
                final = result["final_state"]
                self.assertIsNone(final["active_locator"])
                self.assertEqual(final["task_status"], expected_task_status)
                self.assertTrue(final["dirty_paths"])
                self.assertEqual(final["local_sha"], result["archive_sha"])
                self.assertEqual(final["remote_sha"], result["archive_sha"])
                self.assertEqual(final["pr_head_sha"], result["archive_sha"])
                self.assertEqual(final["pr_is_draft"], False)
                self.assertEqual(final["pr_state"], "OPEN")
                self.assertIn(failed_stage, result["reentry_events"])

    def test_production_fresh_archived_recovery_rejects_replacement_pr_identity(self) -> None:
        result = self.run_production_finish_case(
            "ready",
            expect_reentry_failure=True,
            archived_pr_replacement=True,
        )
        state = result["reentry_failed_state"]
        self.assertIsNone(state["active_locator"])
        self.assertIsNotNone(state["archive_locator"])
        self.assertEqual(state["pr_number"], 106)
        self.assertEqual(state["pr_is_draft"], True)
        self.assertEqual(state["local_sha"], state["remote_sha"])
        self.assertEqual(result["reentry_events"], [])
        self.assertIn("bound remote identity", result["reentry_error"])

    def test_production_index_loss_summary_only_tamper_fails_incomplete_recovery(self) -> None:
        result = self.run_production_finish_case(
            "archive-summary-tamper",
            expect_reentry_failure=True,
        )
        failed = result["failed_state"]
        reentry = result["reentry_failed_state"]
        self.assertIsNone(failed["active_locator"])
        self.assertIsNotNone(failed["archive_locator"])
        self.assertEqual(failed["pr_is_draft"], True)
        self.assertEqual(reentry["local_sha"], failed["local_sha"])
        self.assertEqual(reentry["remote_sha"], failed["remote_sha"])
        self.assertEqual(reentry["pr_head_sha"], failed["pr_head_sha"])
        self.assertEqual(reentry["pr_is_draft"], True)
        self.assertIn("deterministic runtime PR projection", result["reentry_error"])
        self.assertEqual(result["reentry_events"], [])

    def test_production_incomplete_or_mismatched_archive_still_requires_worktree_contracts(self) -> None:
        cases = [
            (False, "Archived closeout files do not match"),
            (
                True,
                "Closeout reviewed content changed after Branch Review",
            ),
        ]
        for create_mismatch, expected_error in cases:
            with self.subTest(create_mismatch=create_mismatch):
                result = self.run_production_finish_case(
                    "archive-commit",
                    archived_damage=(
                        "tamper" if create_mismatch else "delete-retain-plan"
                    ),
                    expect_reentry_failure=True,
                    create_mismatched_commit=create_mismatch,
                )
                state = result["reentry_failed_state"]
                self.assertIsNone(state["active_locator"])
                self.assertIsNotNone(state["archive_locator"])
                self.assertTrue(state["dirty_paths"])
                self.assertEqual(state["pr_is_draft"], True)
                self.assertIn(expected_error, result["reentry_error"])

    def test_production_plan_only_boundary_fails_closed_before_recovery(self) -> None:
        cases = [
            ("repo", "repository differs"),
            ("config-repo", "configured repository mismatch"),
            ("root", "repository root mismatch"),
            ("branch", "branch mismatch"),
            ("head", "exact committed archive transaction"),
            ("locator", "task identity or locator mismatch"),
            ("plan", "expected digest mismatch"),
            ("committed-plan-delete", "Could not resolve task directory"),
            (
                "committed-plan-invalid",
                "closeout-plan migration input validation failed",
            ),
            ("committed-plan-symlink", "must be a real directory with a regular closeout plan file"),
        ]
        for fault, expected_error in cases:
            with self.subTest(fault=fault):
                result = self.run_production_finish_case(
                    "ready",
                    archived_damage="delete",
                    expect_reentry_failure=True,
                    plan_only_boundary_fault=fault,
                )
                state = result["reentry_failed_state"]
                self.assertIsNone(state["active_locator"])
                self.assertTrue(state["dirty_paths"])
                self.assertEqual(state["pr_is_draft"], True)
                self.assertEqual(result["reentry_events"], [])
                self.assertIn(expected_error, result["reentry_error"])

    def test_production_finish_fork_candidate_fails_before_archive_and_summary_binding(self) -> None:
        result = self.run_production_finish_case("fork-candidate")
        failed = result["failed_state"]
        self.assertEqual(failed["active_locator"], ".trellis/tasks/07-11-closeout")
        self.assertIsNone(failed["archive_locator"])
        self.assertEqual(failed["task_status"], "in_progress")
        self.assertEqual(failed["pr_number"], None)
        self.assertEqual(failed["finish_summary_exists"], False)
        final = result["final_state"]
        self.assertIsNone(final["active_locator"])
        self.assertEqual(final["task_status"], "completed")
        self.assertEqual(final["pr_number"], 105)
        self.assertEqual(final["pr_head_sha"], result["archive_sha"])

    def test_production_finish_remote_identity_failure_is_side_effect_free_and_retryable(self) -> None:
        result = self.run_production_finish_case("remote-identity")
        failed = result["failed_state"]
        self.assertEqual(failed["active_locator"], ".trellis/tasks/07-11-closeout")
        self.assertIsNone(failed["archive_locator"])
        self.assertEqual(failed["task_status"], "in_progress")
        self.assertEqual(
            failed["dirty_paths"],
            set(),
        )
        self.assertEqual(failed["staged_paths"], set())
        self.assertEqual(failed["local_sha"], result["branch_review_commit"])
        self.assertIsNone(failed["remote_sha"])
        self.assertIsNone(failed["pr_number"])
        self.assertFalse(failed["finish_summary_exists"])
        self.assertEqual(result["all_transition_attempts"].count("remote-identity"), 1)

        final = result["final_state"]
        self.assertIsNone(final["active_locator"])
        self.assertEqual(final["task_status"], "completed")
        self.assertEqual(final["pr_number"], 105)
        self.assertEqual(final["pr_head_sha"], result["archive_sha"])

    def test_production_finish_local_remote_transport_is_side_effect_free_and_retryable(self) -> None:
        result = self.run_production_finish_case("remote-transport")
        failed = result["failed_state"]
        self.assertEqual(failed["active_locator"], ".trellis/tasks/07-11-closeout")
        self.assertIsNone(failed["archive_locator"])
        self.assertEqual(failed["task_status"], "in_progress")
        self.assertEqual(
            failed["dirty_paths"],
            set(),
        )
        self.assertEqual(failed["staged_paths"], set())
        self.assertEqual(failed["local_sha"], result["branch_review_commit"])
        self.assertIsNone(failed["remote_sha"])
        self.assertIsNone(failed["pr_number"])
        self.assertFalse(failed["finish_summary_exists"])
        self.assertEqual(result["all_transition_attempts"].count("remote-transport"), 1)

        final = result["final_state"]
        self.assertIsNone(final["active_locator"])
        self.assertEqual(final["task_status"], "completed")
        self.assertEqual(final["pr_number"], 105)
        self.assertEqual(final["pr_head_sha"], result["archive_sha"])

    def test_production_finish_raw_remote_control_is_side_effect_free_and_retryable(self) -> None:
        result = self.run_production_finish_case("raw-remote-control")
        failed = result["failed_state"]
        self.assertEqual(failed["active_locator"], ".trellis/tasks/07-11-closeout")
        self.assertIsNone(failed["archive_locator"])
        self.assertEqual(failed["task_status"], "in_progress")
        self.assertEqual(
            failed["dirty_paths"],
            set(),
        )
        self.assertEqual(failed["staged_paths"], set())
        self.assertEqual(failed["local_sha"], result["branch_review_commit"])
        self.assertIsNone(failed["remote_sha"])
        self.assertIsNone(failed["pr_number"])
        self.assertFalse(failed["finish_summary_exists"])
        self.assertEqual(result["all_transition_attempts"].count("raw-remote-control"), 1)

        final = result["final_state"]
        self.assertIsNone(final["active_locator"])
        self.assertEqual(final["task_status"], "completed")
        self.assertEqual(final["pr_number"], 105)
        self.assertEqual(final["pr_head_sha"], result["archive_sha"])

    def test_production_finish_entry_failure_matrix_reads_real_state(self) -> None:
        stages = [
            "prepare",
            "plan-digest",
            "content-push",
            "draft",
            "projection",
            "archive-move",
            "archive-commit",
            "archive-push",
            "remote-head",
            "ready",
        ]
        active = ".trellis/tasks/07-11-closeout"
        archive = f".trellis/tasks/archive/{datetime.now().strftime('%Y-%m')}/07-11-closeout"
        archive_move_paths = {
            f"{active}/{name}"
            for name in [
                "check.jsonl", "design.md",
                "implement.md", "issue-scope-ledger.json", "prd.md",
                "task.json",
            ]
        } | {
            f"{archive}/{name}"
            for name in [
                "closeout-plan.json", "design.md", "finish-summary.json",
                "implement.md", "issue-scope-ledger.json", "prd.md", "task.json",
            ]
        }
        expected = {
            "prepare": (
                active, None, "in_progress",
                set(),
                set(), "reviewed", None, None, None, None, None,
            ),
            "plan-digest": (
                active, None, "in_progress",
                set(),
                set(), "reviewed", None, None, None, None, None,
            ),
            "content-push": (
                active, None, "in_progress",
                set(),
                set(), "reviewed", None, None, None, None, None,
            ),
            "draft": (
                active, None, "in_progress",
                {f"{active}/closeout-plan.json"},
                set(), "reviewed", "reviewed", None, None, None, None,
            ),
            "projection": (
                active, None, "in_progress",
                {
                    f"{active}/closeout-plan.json",
                    f"{active}/finish-summary.json",
                    f"{active}/check.jsonl",
                },
                set(), "reviewed", "reviewed", "reviewed", True, "OPEN", 105,
            ),
            "archive-move": (
                active, None, "in_progress",
                {
                    f"{active}/closeout-plan.json",
                    f"{active}/finish-summary.json",
                },
                set(), "reviewed", "reviewed", "reviewed", True, "OPEN", 105,
            ),
            "archive-commit": (None, archive, "completed", archive_move_paths, archive_move_paths, "reviewed", "reviewed", "reviewed", True, "OPEN", 105),
            "archive-push": (None, archive, "completed", set(), set(), "archive", "reviewed", "reviewed", True, "OPEN", 105),
            "remote-head": (None, archive, "completed", set(), set(), "archive", "archive", "archive", True, "OPEN", 105),
            "ready": (None, archive, "completed", set(), set(), "archive", "archive", "archive", True, "OPEN", 105),
        }
        transition_order = stages
        for stage in stages:
            with self.subTest(stage=stage):
                result = self.run_production_finish_case(stage)
                state = result["failed_state"]
                sha = {
                    "reviewed": result["branch_review_commit"],
                    "archive": result["archive_sha"],
                    None: None,
                }
                expected_row = expected[stage]
                observed = (
                    state["active_locator"],
                    state["archive_locator"],
                    state["task_status"],
                    state["dirty_paths"],
                    state["staged_paths"],
                    state["local_sha"],
                    state["remote_sha"],
                    state["pr_head_sha"],
                    state["pr_is_draft"],
                    state["pr_state"],
                    state["pr_number"],
                )
                resolved_expected = (
                    *expected_row[:5],
                    sha[expected_row[5]],
                    sha[expected_row[6]],
                    sha[expected_row[7]],
                    *expected_row[8:],
                )
                self.assertEqual(observed, resolved_expected)
                root = Path(result["project_root"])
                self.assertEqual(state["active_path"], str(root / active) if expected_row[0] else None)
                self.assertEqual(state["archive_path"], str(root / archive) if expected_row[1] else None)

                compressed_events = [
                    event for index, event in enumerate(result["reentry_events"])
                    if index == 0 or event != result["reentry_events"][index - 1]
                ]
                mutating_events = [event for event in compressed_events if event != "remote-head"]
                next_transition = compressed_events[0] if stage == "remote-head" else mutating_events[0]
                self.assertEqual(next_transition, stage)
                earlier_mutations = set(transition_order[:transition_order.index(stage)]) - {"remote-head"}
                self.assertTrue(earlier_mutations.isdisjoint(mutating_events))


class FinishSummaryContractTests(unittest.TestCase):
    def valid_ai_index(self) -> dict[str, object]:
        summary = self.valid_summary()
        index = json.loads(json.dumps(summary["index"], ensure_ascii=False))
        index.pop("retrieval_text")
        for key in ["issue_refs", "pr_refs", "branches", "paths"]:
            index["search_terms"].pop(key)
        return {"schema_version": 1, "index": index}

    def valid_summary(self) -> dict[str, object]:
        index: dict[str, object] = {
            "problem": "并行 task 完成时会共同改写固定 journal，造成分支冲突。",
            "outcome": "完成摘要改存于当前归档 task；非目标：不实现历史搜索。",
            "changed_behavior": ["finish-work 完成后写入 task-local finish-summary。"],
            "affected_surfaces": [{
                "kind": "workflow",
                "name": "Guru Team finish-work",
                "paths": ["trellis/workflows/guru-team/workflow.md"],
                "change": "finish-work 不再执行 add_session.py，改为记录完成摘要。",
            }],
            "contract_changes": [{
                "contract": "finish session recording",
                "before": "完成信息写入固定 workspace journal。",
                "after": "完成信息写入 archived task 的 finish-summary.json。",
                "source_artifact": "design.md",
            }],
            "search_terms": {
                "issue_refs": ["#53", "#97", "#98", "#100"],
                "pr_refs": [],
                "branches": ["codex/097-finish-summary-replaces-add-session"],
                "paths": ["trellis/workflows/guru-team/workflow.md"],
                "commands": ["add_session.py"],
                "config_keys": ["session_auto_commit"],
                "schema_fields": ["finish-summary.json:index.search_terms"],
                "symbols": ["cmd_finish_work"],
                "phrases": ["workspace journal 冲突", "add_session.py", "完成摘要改为 task-local artifact"],
            },
        }
        index["retrieval_text"] = gtt.finish_summary_retrieval_text("#97 finish summary", index)
        return {
            "schema_version": 1,
            "generated_at": "2026-07-10T00:00:00Z",
            "generator": "guru-team.finish-work",
            "task": {
                "slug": "07-10-097-finish-summary-replaces-add-session",
                "title": "#97 finish summary",
                "status": "completed",
                "artifact_dir": ".trellis/tasks/07-10-097-finish-summary-replaces-add-session",
                "archive_dir": ".trellis/tasks/archive/2026-07/07-10-097-finish-summary-replaces-add-session",
            },
            "git": {
                "base_branch": "main",
                "branch": "codex/097-finish-summary-replaces-add-session",
                "commits": ["a" * 40],
                "changed_paths": ["trellis/workflows/guru-team/workflow.md"],
            },
            "github": {
                "source_issues": [97],
                "close_issues": [97],
                "related_issues": [53, 100],
                "followup_issues": [98],
                "pr_url": "",
            },
            "artifacts": {"design": "design.md"},
            "index": index,
        }

    def valid_current_summary(self) -> dict[str, object]:
        payload = self.valid_summary()
        payload["schema_version"] = gtt.FINISH_SUMMARY_SCHEMA_VERSION
        payload["generator"] = gtt.FINISH_SUMMARY_GENERATOR
        payload["index"]["retrieval_text"] = gtt.current_finish_summary_retrieval_text(  # type: ignore[index]
            payload["task"]["title"], payload["index"]  # type: ignore[index]
        )
        return payload

    def finish_summary_schema(self) -> dict[str, object]:
        schema_path = Path(gtt.__file__).resolve().parents[2] / "schemas/finish-summary.schema.json"
        return json.loads(schema_path.read_text(encoding="utf-8"))

    def safe_path_schema_valid(self, value: object) -> bool:
        schema = self.finish_summary_schema()["$defs"]["safePath"]  # type: ignore[index]
        return (
            isinstance(value, str)
            and schema["minLength"] <= len(value) <= schema["maxLength"]  # type: ignore[index,operator]
            and re.search(schema["pattern"], value) is not None  # type: ignore[index,arg-type]
        )

    def draft_schema_errors(self, payload: dict[str, object]) -> list[object]:
        if importlib.util.find_spec("jsonschema") is None:
            self.skipTest("optional jsonschema dependency is not installed")
        from jsonschema import Draft202012Validator

        schema = self.finish_summary_schema()
        Draft202012Validator.check_schema(schema)
        return list(Draft202012Validator(schema).iter_errors(payload))

    def contract_changes(self, count: int) -> list[dict[str, str]]:
        return [
            {
                "contract": f"finish contract {index}",
                "before": f"旧行为 {index}",
                "after": f"新行为 {index}",
                "source_artifact": "",
            }
            for index in range(count)
        ]

    def expected_snapshot_unavailable_contract(self) -> dict[str, str]:
        return {
            "contract": "finish-summary git path snapshot unavailable",
            "before": "Git 变更路径快照未成功完成。",
            "after": "完成摘要已使用空路径集合，未写入未验证路径。",
            "source_artifact": "",
        }

    def assert_snapshot_unavailable_summary(
        self,
        summary: dict[str, object],
        *,
        undisclosed_values: list[str],
    ) -> None:
        expected_contract = self.expected_snapshot_unavailable_contract()
        self.assertEqual(
            gtt.FINISH_SUMMARY_PATH_SNAPSHOT_UNAVAILABLE_CONTRACT,
            expected_contract,
        )
        self.assertEqual(summary["git"]["changed_paths"], [])  # type: ignore[index]
        self.assertEqual(summary["index"]["search_terms"]["paths"], [])  # type: ignore[index]
        contracts = summary["index"]["contract_changes"]  # type: ignore[index]
        unavailable_contracts = [
            item
            for item in contracts
            if item.get("contract") == expected_contract["contract"]
        ]
        self.assertEqual(unavailable_contracts, [expected_contract])
        self.assertFalse(any(
            item.get("contract") == "finish-summary protected path filtering"
            for item in contracts
        ))
        self.assertEqual(
            summary["index"]["retrieval_text"],  # type: ignore[index]
            gtt.current_finish_summary_retrieval_text(
                summary["task"]["title"],  # type: ignore[index]
                summary["index"],  # type: ignore[index]
            ),
        )
        serialized = json.dumps(summary, ensure_ascii=False)
        for value in undisclosed_values:
            self.assertNotIn(value, serialized)

        protected_path_payload = json.loads(serialized)
        protected_path_payload["git"]["changed_paths"] = [
            ".trellis/workspace/private-journal.md"
        ]
        protected_path_payload["index"]["search_terms"]["paths"] = [
            ".trellis/workspace/private-journal.md"
        ]
        path_errors = gtt.finish_summary_errors(protected_path_payload)
        self.assertTrue(any(
            "git.changed_paths[] must not point to workspace or runtime state" in error
            for error in path_errors
        ))
        self.assertTrue(any(
            "index.search_terms.paths[0] must not point to workspace or runtime state" in error
            for error in path_errors
        ))

    def test_valid_normal_summary_passes_strict_validator(self) -> None:
        self.assertEqual(gtt.finish_summary_errors(self.valid_summary()), [])

    def test_current_retrieval_text_deduplicates_generated_source_fields(self) -> None:
        payload = self.valid_current_summary()
        title = payload["task"]["title"]  # type: ignore[index]
        first_behavior = payload["index"]["changed_behavior"][0]  # type: ignore[index]
        payload["index"]["problem"] = title  # type: ignore[index]
        payload["index"]["outcome"] = first_behavior  # type: ignore[index]
        payload["index"]["affected_surfaces"][0]["change"] = first_behavior  # type: ignore[index]
        payload["index"]["retrieval_text"] = gtt.current_finish_summary_retrieval_text(  # type: ignore[index]
            title, payload["index"]  # type: ignore[index]
        )

        retrieval_lines = payload["index"]["retrieval_text"].splitlines()  # type: ignore[index]
        self.assertEqual(retrieval_lines.count(title), 1)
        self.assertEqual(retrieval_lines.count(first_behavior), 1)
        self.assertEqual(gtt.finish_summary_errors(payload), [])

    def test_historical_retrieval_text_keeps_legacy_derivation(self) -> None:
        payload = self.valid_summary()
        title = payload["task"]["title"]  # type: ignore[index]
        payload["index"]["problem"] = title  # type: ignore[index]
        legacy_retrieval = gtt.finish_summary_retrieval_text(  # type: ignore[index]
            title, payload["index"]  # type: ignore[index]
        )
        payload["index"]["retrieval_text"] = legacy_retrieval  # type: ignore[index]
        self.assertEqual(
            legacy_retrieval,
            gtt.finish_summary_retrieval_text(title, payload["index"]),  # type: ignore[index]
        )
        self.assertEqual(legacy_retrieval.splitlines().count(title), 2)

        payload["index"]["retrieval_text"] = gtt.current_finish_summary_retrieval_text(  # type: ignore[index]
            title, payload["index"]  # type: ignore[index]
        )
        self.assertIn(
            "index.retrieval_text must equal the deterministic derived text.",
            gtt.finish_summary_errors(payload),
        )

    def test_retrieval_text_rejects_adjacent_title_problem_clauses(self) -> None:
        payload = self.valid_summary()
        title = payload["task"]["title"]  # type: ignore[index]
        payload["index"]["problem"] = f"{title}；当前问题描述重复标题。"  # type: ignore[index]
        payload["index"]["retrieval_text"] = gtt.finish_summary_retrieval_text(  # type: ignore[index]
            title, payload["index"]  # type: ignore[index]
        )

        self.assertIn(
            "index.retrieval_text contains adjacent duplicate clauses.",
            gtt.finish_summary_errors(payload),
        )

    def test_normal_finish_work_rejects_outcome_behavior_boundary_pattern(self) -> None:
        payload = self.valid_summary()
        first_behavior = payload["index"]["changed_behavior"][0]  # type: ignore[index]
        payload["index"]["outcome"] = first_behavior  # type: ignore[index]
        payload["index"]["retrieval_text"] = gtt.finish_summary_retrieval_text(  # type: ignore[index]
            payload["task"]["title"], payload["index"]  # type: ignore[index]
        )

        self.assertIn(
            "index.retrieval_text contains adjacent duplicate clauses.",
            gtt.finish_summary_errors(payload),
        )

    def test_finish_summary_schema_key_limits_and_path_refs_with_stdlib(self) -> None:
        schema = self.finish_summary_schema()
        properties = schema["properties"]  # type: ignore[index]
        definitions = schema["$defs"]  # type: ignore[index]

        self.assertEqual(properties["github"]["properties"]["pr_url"]["maxLength"], 1000)  # type: ignore[index]
        self.assertEqual(properties["index"]["properties"]["contract_changes"]["maxItems"], 20)  # type: ignore[index]
        self.assertEqual(properties["generator"]["const"], "guru-team.finalize-task")  # type: ignore[index]
        self.assertEqual(properties["task"]["properties"]["artifact_dir"]["$ref"], "#/$defs/safePath")  # type: ignore[index]
        self.assertEqual(properties["git"]["properties"]["base_branch"]["minLength"], 1)  # type: ignore[index]
        self.assertEqual(properties["git"]["properties"]["branch"]["minLength"], 1)  # type: ignore[index]
        self.assertEqual(definitions["taskPath"]["$ref"], "#/$defs/safePath")  # type: ignore[index]
        self.assertEqual(definitions["optionalSafePath"]["anyOf"][1]["$ref"], "#/$defs/safePath")  # type: ignore[index]
        self.assertEqual(definitions["affectedSurface"]["properties"]["paths"]["items"]["$ref"], "#/$defs/safePath")  # type: ignore[index]
        self.assertEqual(definitions["contractChange"]["properties"]["source_artifact"]["$ref"], "#/$defs/optionalSafePath")  # type: ignore[index]
        self.assertEqual(definitions["searchTerms"]["properties"]["paths"]["items"]["$ref"], "#/$defs/safePath")  # type: ignore[index]

    def test_optional_draft_2020_12_cross_validation(self) -> None:
        normal = self.valid_current_summary()
        invalid_generator = self.valid_current_summary()
        invalid_generator["generator"] = "unknown.generator"
        invalid_path = self.valid_current_summary()
        invalid_path["git"]["changed_paths"] = ["docs\\file.md"]  # type: ignore[index]
        invalid_url = self.valid_current_summary()
        invalid_url["github"]["pr_url"] = "https://github.com/" + ("o" * 980) + "/repo/pull/123"  # type: ignore[index]

        self.assertEqual(self.draft_schema_errors(normal), [])
        self.assertTrue(self.draft_schema_errors(invalid_generator))
        self.assertTrue(self.draft_schema_errors(invalid_path))
        self.assertTrue(self.draft_schema_errors(invalid_url))

    def test_schema_and_python_reject_protected_prefix_on_every_path_surface(self) -> None:
        cases: list[tuple[str, str, dict[str, object]]] = []

        task_artifact = self.valid_summary()
        task_artifact["task"]["artifact_dir"] = ".trellis/workspace/task"  # type: ignore[index]
        cases.append(("task.artifact_dir", ".trellis/workspace/task", task_artifact))

        task_archive = self.valid_summary()
        task_archive["task"]["archive_dir"] = ".trellis/.runtime/task"  # type: ignore[index]
        cases.append(("task.archive_dir", ".trellis/.runtime/task", task_archive))

        git_paths = self.valid_summary()
        git_paths["git"]["changed_paths"] = [".trellis/workspace/file"]  # type: ignore[index]
        git_paths["index"]["search_terms"]["paths"] = [".trellis/workspace/file"]  # type: ignore[index]
        cases.append(("git.changed_paths", ".trellis/workspace/file", git_paths))

        artifact_path = self.valid_summary()
        artifact_path["artifacts"]["design"] = ".trellis/.runtime/design.md"  # type: ignore[index]
        cases.append(("artifacts.design", ".trellis/.runtime/design.md", artifact_path))

        surface_path = self.valid_summary()
        surface_path["index"]["affected_surfaces"][0]["paths"] = [  # type: ignore[index]
            ".trellis/workspace/file"
        ]
        cases.append(("affected_surfaces.paths", ".trellis/workspace/file", surface_path))

        contract_path = self.valid_summary()
        contract_path["index"]["contract_changes"][0]["source_artifact"] = (  # type: ignore[index]
            ".trellis/.runtime/design.md"
        )
        cases.append(("contract_changes.source_artifact", ".trellis/.runtime/design.md", contract_path))

        search_path = self.valid_summary()
        search_path["index"]["search_terms"]["paths"] = [  # type: ignore[index]
            ".trellis/workspace/file"
        ]
        cases.append(("search_terms.paths", ".trellis/workspace/file", search_path))

        for name, path, payload in cases:
            with self.subTest(name=name):
                python_errors = gtt.finish_summary_errors(payload)
                self.assertTrue(python_errors)
                self.assertFalse(self.safe_path_schema_valid(path))
                if name == "search_terms.paths":
                    self.assertTrue(any(
                        "index.search_terms.paths[0] must not point" in error
                        for error in python_errors
                    ))

    def test_schema_and_python_reject_backslash_on_every_path_surface(self) -> None:
        cases: list[tuple[str, dict[str, object]]] = []

        task_artifact = self.valid_summary()
        task_artifact["task"]["artifact_dir"] = "docs\\file.md"  # type: ignore[index]
        cases.append(("task.artifact_dir", task_artifact))

        task_archive = self.valid_summary()
        task_archive["task"]["archive_dir"] = "docs\\file.md"  # type: ignore[index]
        cases.append(("task.archive_dir", task_archive))

        git_path = self.valid_summary()
        git_path["git"]["changed_paths"] = ["docs\\file.md"]  # type: ignore[index]
        cases.append(("git.changed_paths", git_path))

        artifact_path = self.valid_summary()
        artifact_path["artifacts"]["design"] = "docs\\file.md"  # type: ignore[index]
        cases.append(("artifacts.design", artifact_path))

        surface_path = self.valid_summary()
        surface_path["index"]["affected_surfaces"][0]["paths"] = ["docs\\file.md"]  # type: ignore[index]
        cases.append(("affected_surfaces.paths", surface_path))

        contract_path = self.valid_summary()
        contract_path["index"]["contract_changes"][0]["source_artifact"] = "docs\\file.md"  # type: ignore[index]
        cases.append(("contract_changes.source_artifact", contract_path))

        search_path = self.valid_summary()
        search_path["index"]["search_terms"]["paths"] = ["docs\\file.md"]  # type: ignore[index]
        cases.append(("search_terms.paths", search_path))

        for name, payload in cases:
            with self.subTest(name=name):
                python_errors = gtt.finish_summary_errors(payload)
                self.assertTrue(any("must not contain backslashes" in error for error in python_errors))
                self.assertFalse(self.safe_path_schema_valid("docs\\file.md"))

    def test_safe_path_schema_and_python_parity(self) -> None:
        cases = [
            ("safe", "docs/file.md", True),
            ("absolute", "/docs/file.md", False),
            ("windows_absolute", "C:/docs/file.md", False),
            ("parent", "docs/../file.md", False),
            ("dot", "docs/./file.md", False),
            ("double_slash", "docs//file.md", False),
            ("workspace", ".trellis/workspace/file.md", False),
            ("runtime", ".trellis/.runtime/file.md", False),
            ("backslash", "docs\\file.md", False),
            ("crlf", "docs/\r\nfile.md", False),
            ("leading_whitespace", " docs/file.md", False),
            ("trailing_whitespace", "docs/file.md ", False),
        ]

        for name, value, valid in cases:
            with self.subTest(name=name):
                self.assertEqual(gtt.finish_summary_path_errors(value, "path") == [], valid)
                self.assertEqual(self.safe_path_schema_valid(value), valid)

    def test_summary_rejects_unknown_keys_and_generator(self) -> None:
        payload = self.valid_summary()
        payload["summary"] = "unknown"
        payload["generator"] = "unknown.generator"
        errors = gtt.finish_summary_errors(payload)
        self.assertTrue(any("top-level keys" in error for error in errors))
        self.assertTrue(any("generator must equal" in error for error in errors))

    def test_schema_and_python_reject_overlong_canonical_pr_url(self) -> None:
        payload = self.valid_summary()
        payload["github"]["pr_url"] = (  # type: ignore[index]
            "https://github.com/" + ("o" * 980) + "/repo/pull/123"
        )
        payload["index"]["search_terms"]["pr_refs"] = ["PR #123"]  # type: ignore[index]

        python_errors = gtt.finish_summary_errors(payload)
        self.assertTrue(any("github.pr_url" in error for error in python_errors))
        schema = self.finish_summary_schema()["properties"]["github"]["properties"]["pr_url"]  # type: ignore[index]
        self.assertGreater(len(payload["github"]["pr_url"]), schema["maxLength"])  # type: ignore[index,operator]
        self.assertIsNotNone(re.fullmatch(schema["pattern"], payload["github"]["pr_url"]))  # type: ignore[index,arg-type]

    def test_summary_rejects_absolute_parent_workspace_and_runtime_paths(self) -> None:
        bad_paths = [
            "/Users/test/file",
            "../file",
            ".trellis/workspace",
            ".trellis/workspace/index.md",
            ".trellis/.runtime",
            ".trellis/.runtime/cache.json",
        ]
        for path in bad_paths:
            with self.subTest(path=path):
                payload = self.valid_summary()
                payload["git"]["changed_paths"] = [path]  # type: ignore[index]
                payload["index"]["search_terms"]["paths"] = [path]  # type: ignore[index]
                self.assertTrue(gtt.finish_summary_errors(payload))

    def test_git_path_sanitizer_returns_empty_when_all_paths_are_protected(self) -> None:
        paths, filtered = gtt.sanitize_finish_summary_git_paths([
            ".trellis/workspace/index.md",
            ".trellis/.runtime/guru-team/task.json",
        ])

        self.assertEqual(paths, [])
        self.assertTrue(filtered)

    def test_git_path_sanitizer_keeps_only_safe_paths_from_mixed_input(self) -> None:
        paths, filtered = gtt.sanitize_finish_summary_git_paths([
            "trellis/workflows/guru-team/workflow.md",
            ".trellis/workspace/index.md",
            "docs/requirements/requirement-main.md",
            ".trellis/.runtime/guru-team/task.json",
        ])

        self.assertEqual(paths, [
            "docs/requirements/requirement-main.md",
            "trellis/workflows/guru-team/workflow.md",
        ])
        self.assertTrue(filtered)

    def test_git_path_sanitizer_preserves_sorted_unique_safe_input(self) -> None:
        paths, filtered = gtt.sanitize_finish_summary_git_paths([
            "trellis/workflows/guru-team/workflow.md",
            "README.md",
            "README.md",
        ])

        self.assertEqual(paths, ["README.md", "trellis/workflows/guru-team/workflow.md"])
        self.assertFalse(filtered)

        for invalid in [["README.md", 1], [""], [" README.md"], None]:
            with self.subTest(invalid=invalid), self.assertRaises(gtt.WorkflowError):
                gtt.sanitize_finish_summary_git_paths(invalid)

    def test_initial_snapshot_expands_untracked_archive_metadata_files(self) -> None:
        responses = [
            mock.Mock(
                returncode=0,
                stdout=".trellis/workspace/existing.txt\0safe.txt\0",
                stderr="",
            ),
            mock.Mock(
                returncode=0,
                stdout=(
                    ".trellis/tasks/archive/2026-07/task/task.json\0"
                    ".trellis/tasks/archive/2026-07/task/review.md\0"
                ),
                stderr="",
            ),
        ]

        with mock.patch.object(gtt, "run", side_effect=responses) as run:
            paths, filtered, unavailable = gtt.finish_summary_git_path_snapshot(
                Path("/repo"), "main", include_worktree=True
            )

        self.assertEqual(paths, [
            ".trellis/tasks/archive/2026-07/task/review.md",
            ".trellis/tasks/archive/2026-07/task/task.json",
            "safe.txt",
        ])
        self.assertTrue(filtered)
        self.assertFalse(unavailable)
        self.assertEqual(
            run.call_args_list[1].args[0],
            ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        )

    def test_initial_diff_failure_returns_empty_unavailable_snapshot_without_disclosure(self) -> None:
        failed = mock.Mock(
            returncode=128,
            stdout=".trellis/workspace/private-journal.md\0README.md\0",
            stderr="fatal: bad revision secret/ref",
        )
        with mock.patch.object(gtt, "run", return_value=failed) as run:
            snapshot = gtt.finish_summary_git_path_snapshot(
                Path("/repo"), "secret/ref", include_worktree=True
            )

        self.assertEqual(snapshot, ([], False, True))
        self.assertEqual(run.call_count, 1)
        self.assertNotIn("secret/ref", json.dumps(snapshot))

    def test_initial_untracked_failure_discards_partial_diff_snapshot(self) -> None:
        responses = [
            mock.Mock(returncode=0, stdout="README.md\0", stderr=""),
            mock.Mock(returncode=1, stdout="private-untracked.md\0", stderr="denied"),
        ]
        with mock.patch.object(gtt, "run", side_effect=responses):
            snapshot = gtt.finish_summary_git_path_snapshot(
                Path("/repo"), "main", include_worktree=True
            )

        self.assertEqual(snapshot, ([], False, True))

    def test_final_diff_failure_returns_empty_unavailable_snapshot(self) -> None:
        failed = mock.Mock(returncode=1, stdout="README.md\0", stderr="denied")
        with mock.patch.object(gtt, "run", return_value=failed) as run:
            snapshot = gtt.finish_summary_git_path_snapshot(
                Path("/repo"), "main", include_worktree=False
            )

        self.assertEqual(snapshot, ([], False, True))
        self.assertEqual(run.call_count, 1)

    def test_protected_path_filter_contract_is_exact_idempotent_and_removable(self) -> None:
        index = self.valid_summary()["index"]

        gtt.apply_finish_summary_path_filter_contract(index, True)  # type: ignore[arg-type]
        gtt.apply_finish_summary_path_filter_contract(index, True)  # type: ignore[arg-type]
        matches = [
            item
            for item in index["contract_changes"]  # type: ignore[index]
            if item.get("contract") == "finish-summary protected path filtering"
        ]
        self.assertEqual(matches, [gtt.FINISH_SUMMARY_PROTECTED_PATH_FILTER_CONTRACT])
        self.assertNotIn(".trellis/", json.dumps(matches, ensure_ascii=False))
        self.assertNotRegex(json.dumps(matches, ensure_ascii=False), r"[0-9]")

        gtt.apply_finish_summary_path_filter_contract(index, False)  # type: ignore[arg-type]
        self.assertFalse(any(
            item.get("contract") == "finish-summary protected path filtering"
            for item in index["contract_changes"]  # type: ignore[index]
        ))

    def test_initial_summary_uses_sanitized_paths_and_appends_filter_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / ".trellis/tasks/archive/2026-07/07-10-097-finish-summary-replaces-add-session"
            task_dir.mkdir(parents=True)
            (task_dir / "task.json").write_text(
                json.dumps({
                    "name": task_dir.name,
                    "title": "#97 finish summary",
                    "base_branch": "main",
                }) + "\n",
                encoding="utf-8",
            )
            (task_dir / "design.md").write_text("# Design\n", encoding="utf-8")
            ledger = {
                "primary_issue": {"number": 97},
                "close_issues": [{"number": 97}],
                "related_issues": [{"number": 53}, {"number": 100}],
                "followup_issues": [{"number": 98}],
            }
            task_context = {
                "base_branch": "main",
                "base_ref": "main",
                "branch_name": "codex/097-finish-summary-replaces-add-session",
                "task_artifact_dir": ".trellis/tasks/07-10-097-finish-summary-replaces-add-session",
            }

            with (
                mock.patch.object(
                    gtt,
                    "run",
                    return_value=mock.Mock(returncode=0, stdout=f"{'a' * 40}\n", stderr=""),
                ),
                mock.patch.object(
                    gtt,
                    "finish_summary_git_path_snapshot",
                    return_value=([
                        ".trellis/guru-team/extension.json",
                        "trellis/guru-team-extension.json",
                    ], True, False),
                ),
            ):
                summary = gtt.build_finish_summary(
                    root,
                    task_dir,
                    task_context,
                    ledger,
                    valid_pr_body("finish-summary 使用经过清理的路径并记录过滤事实。"),
                    "a" * 40,
                )

            expected_paths = [
                ".trellis/guru-team/extension.json",
                "trellis/guru-team-extension.json",
            ]
            self.assertEqual(summary["git"]["changed_paths"], expected_paths)
            self.assertEqual(summary["index"]["search_terms"]["paths"], expected_paths)
            self.assertEqual(sum(
                item.get("contract") == "finish-summary protected path filtering"
                for item in summary["index"]["contract_changes"]
            ), 1)
            self.assertEqual(len(summary["index"]["contract_changes"]), 1)
            self.assertNotIn("marketplace_verification", summary["artifacts"])
            retrieval_lines = summary["index"]["retrieval_text"].splitlines()
            fixed_before = gtt.FINISH_SUMMARY_PROTECTED_PATH_FILTER_CONTRACT["before"]
            fixed_after = gtt.FINISH_SUMMARY_PROTECTED_PATH_FILTER_CONTRACT["after"]
            self.assertEqual(retrieval_lines.count(fixed_before), 1)
            self.assertEqual(retrieval_lines.count(fixed_after), 1)
            self.assertLess(retrieval_lines.index(fixed_before), retrieval_lines.index(fixed_after))
            retrieval_text = "\n".join(retrieval_lines)
            self.assertNotIn(".trellis/workspace/private-journal.md", retrieval_text)
            self.assertNotIn("private-journal.md", retrieval_text)
            self.assertFalse(any(re.search(r"过滤(?:了)?\s*1|1\s*个", line) for line in retrieval_lines))
            self.assertEqual(gtt.finish_summary_errors(summary, task_dir=task_dir), [])

    def test_initial_snapshot_failures_use_empty_paths_and_exact_fixed_fact(self) -> None:
        cases = {
            "git_diff": (
                [
                    mock.Mock(returncode=0, stdout=f"{'a' * 40}\n", stderr=""),
                    mock.Mock(
                        returncode=128,
                        stdout="README.md\0.trellis/workspace/private-journal.md\0",
                        stderr="fatal: bad revision secret/ref",
                    ),
                ],
                ["README.md", "private-journal.md", "fatal: bad revision", "secret/ref"],
            ),
            "git_ls_files_others": (
                [
                    mock.Mock(returncode=0, stdout=f"{'a' * 40}\n", stderr=""),
                    mock.Mock(returncode=0, stdout="README.md\0", stderr=""),
                    mock.Mock(
                        returncode=1,
                        stdout="private-untracked.md\0",
                        stderr="untracked enumeration denied",
                    ),
                ],
                ["README.md", "private-untracked.md", "untracked enumeration denied"],
            ),
        }

        for failure_case, (responses, undisclosed_values) in cases.items():
            with self.subTest(failure_case=failure_case), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                task_dir = root / ".trellis/tasks/archive/2026-07/task"
                task_dir.mkdir(parents=True)
                (task_dir / "task.json").write_text(
                    '{"name":"task","title":"完成摘要","base_branch":"main"}\n',
                    encoding="utf-8",
                )
                (task_dir / "design.md").write_text("# Design\n", encoding="utf-8")
                with mock.patch.object(gtt, "run", side_effect=responses):
                    summary = gtt.build_finish_summary(
                        root,
                        task_dir,
                        {
                            "base_branch": "main",
                            "base_ref": "secret/ref" if failure_case == "git_diff" else "main",
                            "branch_name": "topic",
                            "task_artifact_dir": ".trellis/tasks/task",
                        },
                        {"primary_issue": {"number": 97}, "close_issues": [], "related_issues": [], "followup_issues": []},
                        valid_pr_body("finish-summary 在 Git 快照失败时使用空路径集合。"),
                        "a" * 40,
                    )

                self.assertEqual(len(summary["index"]["contract_changes"]), 1)  # type: ignore[index]
                self.assert_snapshot_unavailable_summary(
                    summary,
                    undisclosed_values=undisclosed_values,
                )

    def test_summary_rejects_lengths_counts_enum_and_normalized_duplicates(self) -> None:
        payload = self.valid_summary()
        payload["index"]["problem"] = "问" * 401  # type: ignore[index]
        payload["index"]["changed_behavior"] = ["重复行为。", "重复 行为!"]  # type: ignore[index]
        payload["index"]["affected_surfaces"][0]["kind"] = "invalid"  # type: ignore[index]
        payload["index"]["search_terms"]["phrases"] = ["相同短语", "相同 短语！"]  # type: ignore[index]
        errors = gtt.finish_summary_errors(payload)
        self.assertTrue(any("index.problem length" in error for error in errors))
        self.assertTrue(any(
            "index.changed_behavior[1] duplicates index.changed_behavior[0] after normalization."
            == error
            for error in errors
        ))
        self.assertTrue(any(
            "index.search_terms.phrases[1] duplicates index.search_terms.phrases[0] after normalization."
            == error
            for error in errors
        ))
        self.assertTrue(any("kind is invalid" in error for error in errors))
        self.assertTrue(any("item count" in error for error in errors))

    def test_summary_path_arrays_use_exact_identity(self) -> None:
        payload = self.valid_summary()
        paths = [
            ".trellis/guru-team/extension.json",
            "trellis/guru-team-extension.json",
        ]
        payload["git"]["changed_paths"] = paths  # type: ignore[index]
        payload["index"]["search_terms"]["paths"] = paths  # type: ignore[index]
        payload["index"]["affected_surfaces"][0]["paths"] = paths  # type: ignore[index]
        second_surface = json.loads(json.dumps(
            payload["index"]["affected_surfaces"][0], ensure_ascii=False  # type: ignore[index]
        ))
        payload["index"]["affected_surfaces"][0]["paths"] = [paths[0]]  # type: ignore[index]
        second_surface["paths"] = [paths[1]]
        payload["index"]["affected_surfaces"].append(second_surface)  # type: ignore[index]
        payload["index"]["retrieval_text"] = gtt.finish_summary_retrieval_text(  # type: ignore[index]
            payload["task"]["title"], payload["index"]  # type: ignore[index]
        )

        self.assertEqual(gtt.finish_summary_errors(payload), [])

    def test_summary_path_arrays_reject_exact_duplicates(self) -> None:
        payload = self.valid_summary()
        duplicate_paths = ["README.md", "README.md"]
        payload["git"]["changed_paths"] = duplicate_paths  # type: ignore[index]
        payload["index"]["search_terms"]["paths"] = duplicate_paths  # type: ignore[index]
        payload["index"]["affected_surfaces"][0]["paths"] = duplicate_paths  # type: ignore[index]
        errors = gtt.finish_summary_errors(payload)

        self.assertIn("git.changed_paths must be sorted and unique.", errors)
        self.assertIn(
            "index.search_terms.paths[1] duplicates index.search_terms.paths[0].",
            errors,
        )
        self.assertIn(
            "index.affected_surfaces[0].paths[1] duplicates "
            "index.affected_surfaces[0].paths[0].",
            errors,
        )

    def test_summary_rejects_adjacent_duplicate_clause_and_derived_field_drift(self) -> None:
        payload = self.valid_summary()
        payload["index"]["outcome"] = "完成摘要改为归档文件；完成 摘要改为归档文件。"  # type: ignore[index]
        payload["index"]["search_terms"]["issue_refs"] = ["#97"]  # type: ignore[index]
        payload["index"]["search_terms"]["branches"] = []  # type: ignore[index]
        payload["index"]["search_terms"]["paths"] = []  # type: ignore[index]
        payload["index"]["retrieval_text"] = "manual text"  # type: ignore[index]
        errors = gtt.finish_summary_errors(payload)
        self.assertTrue(any("adjacent duplicate clauses" in error for error in errors))
        self.assertTrue(any("issue_refs" in error for error in errors))
        self.assertTrue(any("branches" in error for error in errors))
        self.assertTrue(any("paths" in error for error in errors))
        self.assertTrue(any("retrieval_text" in error for error in errors))

    def test_ai_index_rejects_factual_search_terms(self) -> None:
        payload = self.valid_summary()
        ai_index = {"schema_version": 1, "index": payload["index"]}
        ai_index["index"].pop("retrieval_text")  # type: ignore[union-attr]
        errors = gtt.finish_summary_index_errors(ai_index["index"], final=False)
        self.assertTrue(any("search_terms keys" in error for error in errors))

    def test_historical_ai_index_contract_change_limit_reserves_filter_fact(self) -> None:
        payload = self.valid_ai_index()
        payload["index"]["contract_changes"] = self.contract_changes(19)  # type: ignore[index]
        self.assertEqual(gtt.finish_summary_index_errors(payload["index"], final=False), [])

        payload["index"]["contract_changes"] = self.contract_changes(20)  # type: ignore[index]
        errors = gtt.finish_summary_index_errors(payload["index"], final=False)
        self.assertTrue(any("exceeds 19 items" in error for error in errors))

    def test_retrieval_fixture_hits_pre_and_post_pr_signals(self) -> None:
        payload = self.valid_summary()
        haystack = json.dumps(payload["index"], ensure_ascii=False)
        for token in ["#97", "codex/097", "workflow.md", "add_session.py", "session_auto_commit", "index.search_terms", "cmd_finish_work", "workspace journal 冲突", "完成摘要改为"]:
            self.assertIn(token, haystack)
        payload["github"]["pr_url"] = "https://github.com/castbox/guru-trellis/pull/123"  # type: ignore[index]
        payload["index"]["search_terms"]["pr_refs"] = ["PR #123"]  # type: ignore[index]
        self.assertEqual(gtt.finish_summary_errors(payload), [])
        self.assertIn("PR #123", json.dumps(payload["index"], ensure_ascii=False))


class ChangeContextDiscoveryTests(unittest.TestCase):
    def make_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / ".trellis/tasks/archive/2026-01").mkdir(parents=True)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Context Discovery Test"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "context@example.invalid"], cwd=root, check=True)
        subprocess.run(
            ["git", "commit", "--allow-empty", "-q", "-m", "test: seed context repository"],
            cwd=root,
            check=True,
        )
        subprocess.run(
            [
                "git", "remote", "add", "origin",
                "https://github.com/example/guru-extension.git",
            ],
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["git", "update-ref", "refs/remotes/origin/main", "HEAD"],
            cwd=root,
            check=True,
        )
        return temp, root

    def valid_index(self, issue: int, token: str, path: str) -> dict[str, object]:
        return {
            "problem": f"需要检索 {token} 的历史合同。",
            "outcome": f"已完成 {token} 历史索引。",
            "changed_behavior": [f"新增 {token} 索引预览能力。"],
            "affected_surfaces": [
                {"kind": "workflow", "name": token, "paths": [path], "change": f"新增 {token} preview。"}
            ],
            "contract_changes": [],
            "search_terms": {
                "issue_refs": [f"#{issue}"],
                "pr_refs": [],
                "branches": [f"feat/{issue}-{token}"],
                "paths": [path],
                "commands": ["preview-change-context-history"],
                "config_keys": [],
                "schema_fields": [],
                "symbols": [token],
                "phrases": [
                    f"{token} 历史索引预览已完成",
                    "preview-change-context-history 命令已新增",
                    f"{token} 支持检索",
                ],
            },
            "retrieval_text": (
                f"{token} 历史索引预览已完成\n"
                "preview-change-context-history 命令已新增\n"
                f"{token} 支持检索"
            ),
        }

    def write_summary(self, root: Path, name: str, index: dict[str, object]) -> Path:
        task = root / ".trellis/tasks/archive/2026-01" / name
        task.mkdir()
        path = task / "finish-summary.json"
        path.write_text(json.dumps({"ignored": {"private": "not consumed"}, "index": index}), encoding="utf-8")
        return path

    def test_query_canonicalization_is_stable_and_rejects_unsafe_paths(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        first = gtt.canonicalize_context_query(
            root,
            {
                "issue_refs": ["111", "#111"],
                "paths": ["trellis/GuruSkill.md"],
                "terms": ["  Change   Context ", "change context"],
                "symbols": ["GuruContextSkill"],
            },
        )
        second = gtt.canonicalize_context_query(
            root,
            {
                "symbols": ["GuruContextSkill"],
                "terms": ["change context"],
                "paths": ["trellis/GuruSkill.md"],
                "issue_refs": ["#111"],
            },
        )
        self.assertEqual(first, second)
        self.assertEqual(first["issue_refs"], ["#111"])
        self.assertIn("guru", first["tokens"])
        self.assertIn("context", first["tokens"])
        with self.assertRaises(gtt.WorkflowError):
            gtt.canonicalize_context_query(root, {"paths": ["../secret"]})
        with self.assertRaises(gtt.WorkflowError):
            gtt.canonicalize_context_query(root, {"paths": [".trellis/workspace/private.md"]})

    def test_preview_scores_sorts_limits_and_isolates_invalid(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        for number in range(25):
            self.write_summary(root, f"valid-{number:02d}", self.valid_index(111, "guru-context", f"trellis/{number:02d}.md"))
        broken = root / ".trellis/tasks/archive/2026-01/broken"
        broken.mkdir()
        (broken / "finish-summary.json").write_text("{broken", encoding="utf-8")
        missing = root / ".trellis/tasks/archive/2026-01/missing"
        missing.mkdir()
        (missing / "finish-summary.json").write_text('{"not_index":true}', encoding="utf-8")
        bad_shape = root / ".trellis/tasks/archive/2026-01/bad-shape"
        bad_shape.mkdir()
        (bad_shape / "finish-summary.json").write_text('{"index":{}}', encoding="utf-8")
        query = {
            "issue_refs": ["#111"],
            "commands": ["preview-change-context-history"],
            "symbols": ["guru-context"],
            "queries": ["guru-context 支持检索"],
        }
        first = gtt.build_context_history_preview(root, query)
        second = gtt.build_context_history_preview(root, dict(reversed(list(query.items()))))
        self.assertEqual(first, second)
        self.assertEqual(len(first["candidates"]), 20)
        self.assertEqual(
            [row["finish_summary_path"] for row in first["candidates"]],
            sorted(row["finish_summary_path"] for row in first["candidates"]),
        )
        self.assertEqual(
            {row["error_code"] for row in first["invalid"]},
            {"invalid_json", "missing_index", "invalid_index_shape"},
        )
        self.assertTrue(all("/Users/" not in json.dumps(row) for row in first["invalid"]))
        zero = gtt.build_context_history_preview(root, {"terms": ["no-match-anywhere"]})
        self.assertEqual(zero["candidates"], [])
        self.assertEqual(zero["manifest"], first["manifest"])

    def test_score_uses_every_exact_weight_once_and_caps_tokens(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        index = self.valid_index(111, "guru-context", "trellis/context.md")
        index["search_terms"].update({
            "pr_refs": ["PR #222"],
            "config_keys": ["context.mode"],
            "schema_fields": ["snapshot_sha256"],
        })
        index["retrieval_text"] += "\ncontext mode snapshot sha256 full request phrase " + " ".join(f"token{number}" for number in range(120))
        query = gtt.canonicalize_context_query(root, {
            "issue_refs": ["#111", "#111"],
            "pr_refs": ["PR #222"],
            "branches": ["feat/111-guru-context"],
            "paths": ["trellis/context.md"],
            "commands": ["preview-change-context-history"],
            "config_keys": ["context.mode"],
            "schema_fields": ["snapshot_sha256"],
            "symbols": ["guru-context"],
            "terms": ["guru-context"],
            "queries": ["full request phrase"],
        })
        query["tokens"] = [f"token{number}" for number in range(120)]
        score, matched = gtt.context_candidate_score(query, index)
        self.assertEqual(score["exact"], 6500)
        self.assertEqual(score["exact_match_count"], 10)
        self.assertEqual(score["token"], 99)
        self.assertEqual(set(matched) - {"tokens"}, set(gtt.CONTEXT_QUERY_KINDS))

    def valid_sync_result(
        self,
        *,
        head: str = "1" * 40,
        branch: str = "main",
        remote: str = "origin",
    ) -> dict[str, object]:
        identity = gtt.resolution_identity(
            source="explicit",
            selected_base=branch,
            remote=remote,
            candidates=[branch],
            decision_branch=branch,
            decision_head=head,
            decision_clean=True,
        )
        resolution_sha256 = gtt.canonical_json_sha256(identity)
        result: dict[str, object] = {
            "schema_version": "1.0",
            "skill_id": "guru-sync-base",
            "status": "synced",
            "resolution": {
                "source": "explicit",
                "selected_base": branch,
                "remote": remote,
                "candidates": [branch],
                "resolution_sha256": resolution_sha256,
            },
            "post_sync_resolution": identity,
            "post_sync_resolution_sha256": resolution_sha256,
            "decision_checkout": {
                "branch": branch,
                "head_before": head,
                "head_after": head,
                "clean_before": True,
                "clean_after": True,
            },
            "git": {
                "local_ref": f"refs/heads/{branch}",
                "remote_ref": f"refs/remotes/{remote}/{branch}",
                "local_head_before": head,
                "local_head_after": head,
                "remote_head_after": head,
                "fetch_performed": True,
                "fast_forwarded": False,
            },
            "fresh": True,
        }
        result["facts_sha256"] = gtt.canonical_json_sha256(result)
        return result

    def bind_valid_base(
        self,
        payload: dict[str, object],
        *,
        head: str = "1" * 40,
        branch: str = "main",
        remote: str = "origin",
    ) -> None:
        result = self.valid_sync_result(head=head, branch=branch, remote=remote)
        payload["repository"] = {
            "repo": "example/guru-extension",
            "selected_base": branch,
            "decision_branch": branch,
        }
        payload["base_evidence"] = {
            "schema_id": "guru-base-sync-result-1.0",
            "sync_result": result,
            "remote": remote,
            "base_head": head,
            "decision_head": head,
            "local_head": head,
            "remote_head": head,
            "post_sync_resolution_sha256": result["post_sync_resolution_sha256"],
            "clean": True,
        }


    def valid_owner_result(self, root: Path) -> dict[str, object]:
        package = (
            Path(gtt.__file__).resolve().parents[4]
            / "skills/guru-team/packages/guru-discover-change-context"
        )
        payload = json.loads(
            (package / "examples/change-context-owner-result.json").read_text(
                encoding="utf-8"
            )
        )
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        self.bind_valid_base(payload, head=head)
        query = gtt.canonicalize_context_query(
            root, payload["change_input"], validate_repo_paths=False
        )
        payload["canonical_query"] = query
        payload["history_preview"] = gtt.build_context_history_preview(root, query)
        payload["history_review"] = {
            "selected_candidates": [],
            "excluded_candidates": [],
            "deep_reads": [],
        }
        live = payload["live_change"]
        live["facts_sha256"] = gtt.context_digest({
            key: live[key]
            for key in ("kind", "identity", "state", "updated_at", "body_sha256")
        })
        binding = live["issue_binding"]
        binding["facts_sha256"] = gtt.context_digest({
            key: binding[key]
            for key in ("repo", "number", "url", "state", "updated_at", "body_sha256")
        })
        payload["result_identity"] = gtt.context_result_identity(payload)
        return payload

    def public_input(self, root: Path) -> Path:
        path = root / "public-input.json"
        path.write_text(
            json.dumps({
                "profile": "pre_task",
                "source_exit": "start",
                "mode": "workflow",
                "repo_locator": "example/guru-extension",
                "base_branch": "main",
                "continuation_id": "stage0-current",
            }),
            encoding="utf-8",
        )
        return path

    def test_owner_result_record_check_and_public_invocation_are_ephemeral(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        payload = self.valid_owner_result(root)
        public_input = self.public_input(root)
        package = (
            Path(gtt.__file__).resolve().parents[4]
            / "skills/guru-team/packages/guru-discover-change-context"
        )
        before = {
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file()
        }
        with mock.patch.object(gtt, "context_live_errors", return_value=[]):
            recorded = gtt.cmd_record_context_discovery(argparse.Namespace(
                root=str(root), mode="workflow", input=None, payload=payload,
                expected_result_sha256=payload["result_identity"]["result_sha256"],
            ))
            checked = gtt.cmd_check_context_discovery(argparse.Namespace(
                root=str(root), input=None, payload=recorded,
                expected_result_sha256=recorded["result_identity"]["result_sha256"],
            ))
            with (
                mock.patch.object(
                    gtt,
                    "stage0_invocation_identity",
                    return_value=("guru-discover-change-context", package),
                ),
                mock.patch.object(gtt, "stage0_repo_root", return_value=root),
                mock.patch.object(
                    sys,
                    "stdin",
                    io.StringIO(json.dumps(recorded)),
                ),
            ):
                output = gtt.cmd_invoke_stage0_skill(argparse.Namespace(
                    input=public_input.relative_to(root).as_posix(),
                    owner_result="-",
                ))

        self.assertEqual(checked["status"], "passed")
        self.assertEqual(
            output,
            {
                "exit_id": "context_ready",
                "handoff_profile": "initial_change_request",
                "handoff_mode": "workflow",
                "handoff_target_locator": payload["live_change"]["identity"],
                "handoff_continuation_id": "stage0-current",
            },
        )
        self.assertEqual(
            before,
            {
                path.relative_to(root).as_posix()
                for path in root.rglob("*")
                if path.is_file()
            },
        )
        self.assertFalse((root / ".trellis/.runtime").exists())

    def test_record_and_check_accept_stdin_without_repository_writes(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        payload = self.valid_owner_result(root)
        before = set(gtt.git_status_paths(root))
        with (
            mock.patch.object(gtt, "context_live_errors", return_value=[]),
            mock.patch.object(sys, "stdin", io.StringIO(json.dumps(payload))),
        ):
            recorded = gtt.cmd_record_context_discovery(argparse.Namespace(
                root=str(root), mode="workflow", input="-", payload=None,
                expected_result_sha256=payload["result_identity"]["result_sha256"],
            ))
        with (
            mock.patch.object(gtt, "context_live_errors", return_value=[]),
            mock.patch.object(sys, "stdin", io.StringIO(json.dumps(recorded))),
        ):
            checked = gtt.cmd_check_context_discovery(argparse.Namespace(
                root=str(root), input="-", payload=None,
                expected_result_sha256=recorded["result_identity"]["result_sha256"],
            ))
        self.assertEqual(checked["typed_exit"], "context_ready")
        self.assertEqual(before, set(gtt.git_status_paths(root)))
        self.assertFalse((root / ".trellis/.runtime").exists())

    def test_active_task_normal_invocation_uses_task_identity_without_checkpoint(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        task_dir = root / ".trellis/tasks/08-07-context-active"
        task_dir.mkdir(parents=True)
        gtt.write_json(task_dir / "task.json", {
            "id": "08-07-context-active",
            "status": "in_progress",
            "branch": "codex/context-active",
        })
        subprocess.run(
            ["git", "add", task_dir.relative_to(root).as_posix()],
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", "test: add active context task"],
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["git", "update-ref", "refs/remotes/origin/main", "HEAD"],
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["git", "switch", "-q", "-c", "codex/context-active"],
            cwd=root,
            check=True,
        )
        payload = self.valid_owner_result(root)
        task_ref = task_dir.relative_to(root).as_posix()
        checkpoint = gtt.context_recovery_checkpoint_path(root, task_dir)
        package = (
            Path(gtt.__file__).resolve().parents[4]
            / "skills/guru-team/packages/guru-discover-change-context"
        )

        self.assertIn(
            "base_decision_branch_stale",
            gtt.context_live_base_errors(root, payload, None),
        )
        self.assertEqual(
            gtt.context_active_task_dir(root, task_ref),
            Path(os.path.abspath(task_dir)),
        )
        self.assertEqual(gtt.context_live_base_errors(root, payload, task_dir), [])

        base_only = lambda live_root, live_payload, live_task: (
            gtt.context_live_base_errors(live_root, live_payload, live_task)
        )
        with mock.patch.object(gtt, "context_live_errors", side_effect=base_only):
            recorded = gtt.cmd_record_context_discovery(argparse.Namespace(
                root=str(root), mode="workflow", input=None, payload=payload,
                expected_result_sha256=payload["result_identity"]["result_sha256"],
                active_task=task_ref,
            ))
            self.assertFalse(checkpoint.exists())
            checked = gtt.cmd_check_context_discovery(argparse.Namespace(
                root=str(root), input=None, payload=recorded,
                expected_result_sha256=recorded["result_identity"]["result_sha256"],
                active_task=task_ref,
            ))
            self.assertFalse(checkpoint.exists())
            public_input = self.public_input(root)
            with (
                mock.patch.object(
                    gtt,
                    "stage0_invocation_identity",
                    return_value=("guru-discover-change-context", package),
                ),
                mock.patch.object(gtt, "stage0_repo_root", return_value=root),
                mock.patch.object(sys, "stdin", io.StringIO(json.dumps(recorded))),
            ):
                output = gtt.cmd_invoke_stage0_skill(argparse.Namespace(
                    input=public_input.relative_to(root).as_posix(),
                    owner_result="-",
                    active_task=task_ref,
                ))

        self.assertEqual(checked["typed_exit"], "context_ready")
        self.assertEqual(output["exit_id"], "context_ready")
        self.assertFalse(checkpoint.exists())
        self.assertFalse((root / ".trellis/.runtime").exists())

    def test_active_task_recovery_is_lazy_checked_and_consumed_by_public_wrapper(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        payload = self.valid_owner_result(root)
        public_input = self.public_input(root)
        task_dir = root / ".trellis/tasks/08-07-context-recovery"
        task_dir.mkdir(parents=True)
        gtt.write_json(task_dir / "task.json", {
            "id": "08-07-context-recovery",
            "status": "in_progress",
            "branch": "main",
        })
        task_ref = task_dir.relative_to(root).as_posix()
        continuation_id = "stage0-current"
        package = (
            Path(gtt.__file__).resolve().parents[4]
            / "skills/guru-team/packages/guru-discover-change-context"
        )
        checkpoint = gtt.context_recovery_checkpoint_path(root, task_dir)
        self.assertFalse(checkpoint.exists())

        base_only = lambda live_root, live_payload, live_task: (
            gtt.context_live_base_errors(live_root, live_payload, live_task)
        )
        self.assertTrue(gtt.git_status_paths(root))
        with mock.patch.object(gtt, "context_live_errors", side_effect=base_only):
            recorded = gtt.cmd_record_context_discovery(argparse.Namespace(
                root=str(root), mode="workflow", input=None, payload=payload,
                expected_result_sha256=payload["result_identity"]["result_sha256"],
                active_task=task_ref,
                recovery_continuation_id=continuation_id,
            ))
            self.assertTrue(checkpoint.is_file())
            private = gtt.read_json(checkpoint)
            self.assertEqual(private["task_ref"], task_ref)
            self.assertEqual(private["task_id"], "08-07-context-recovery")
            self.assertEqual(private["continuation_id"], continuation_id)
            forbidden = {
                "authorization", "reviewer", "generated_at", "result_identity",
                "live_change", "repository", "history_preview", "canonical_query",
            }
            self.assertTrue(forbidden.isdisjoint(private))

            checked = gtt.cmd_check_context_discovery(argparse.Namespace(
                root=str(root), input=None, payload=recorded,
                expected_result_sha256=recorded["result_identity"]["result_sha256"],
                active_task=task_ref,
                recovery_continuation_id=continuation_id,
            ))
            self.assertEqual(checked["typed_exit"], "context_ready")

            with (
                mock.patch.object(
                    gtt,
                    "stage0_invocation_identity",
                    return_value=("guru-discover-change-context", package),
                ),
                mock.patch.object(gtt, "stage0_repo_root", return_value=root),
                mock.patch.object(sys, "stdin", io.StringIO(json.dumps(recorded))),
            ):
                output = gtt.cmd_invoke_stage0_skill(argparse.Namespace(
                    input=public_input.relative_to(root).as_posix(),
                    owner_result="-",
                    active_task=task_ref,
                    recovery_continuation_id=continuation_id,
                ))

        self.assertEqual(output["exit_id"], "context_ready")
        self.assertFalse(checkpoint.exists())
        self.assertFalse(checkpoint.parent.exists())

    def test_active_task_recovery_stale_or_unsafe_checkpoint_fails_closed(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        payload = self.valid_owner_result(root)
        task_dir = root / ".trellis/tasks/08-07-context-recovery"
        task_dir.mkdir(parents=True)
        gtt.write_json(task_dir / "task.json", {
            "id": "08-07-context-recovery",
            "status": "in_progress",
            "branch": "main",
        })
        task_ref = task_dir.relative_to(root).as_posix()
        checkpoint = gtt.context_recovery_checkpoint_path(root, task_dir)

        checkpoint.parent.mkdir(parents=True)
        external = root / "preserve-context-recovery.json"
        external.write_text("preserve\n", encoding="utf-8")
        checkpoint.symlink_to(external)
        with (
            mock.patch.object(gtt, "context_live_errors", return_value=[]),
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.cmd_record_context_discovery(argparse.Namespace(
                root=str(root), mode="workflow", input=None, payload=payload,
                expected_result_sha256=payload["result_identity"]["result_sha256"],
                active_task=task_ref,
                recovery_continuation_id="stage0-current",
            ))
        self.assertEqual(external.read_text(encoding="utf-8"), "preserve\n")
        checkpoint.unlink()

        checkpoint.write_text("{\n", encoding="utf-8")
        with (
            mock.patch.object(gtt, "context_live_errors", return_value=[]),
            self.assertRaises(gtt.WorkflowError) as invalid,
        ):
            gtt.cmd_check_context_discovery(argparse.Namespace(
                root=str(root), input=None, payload=payload,
                expected_result_sha256=payload["result_identity"]["result_sha256"],
                active_task=task_ref,
                recovery_continuation_id="stage0-current",
            ))
        self.assertEqual(
            invalid.exception.payload["error_codes"],
            ["context_recovery_checkpoint_invalid"],
        )
        self.assertFalse(checkpoint.exists())
        self.assertFalse(checkpoint.parent.exists())

        with mock.patch.object(gtt, "context_live_errors", return_value=[]):
            recorded = gtt.cmd_record_context_discovery(argparse.Namespace(
                root=str(root), mode="workflow", input=None, payload=payload,
                expected_result_sha256=payload["result_identity"]["result_sha256"],
                active_task=task_ref,
                recovery_continuation_id="stage0-current",
            ))
            changed = copy.deepcopy(recorded)
            changed["ai_review_gate"]["reason"] = "Fresh authority required a new semantic conclusion."
            changed["result_identity"] = gtt.context_result_identity(changed)
            with self.assertRaises(gtt.WorkflowError):
                gtt.cmd_check_context_discovery(argparse.Namespace(
                    root=str(root), input=None, payload=changed,
                    expected_result_sha256=changed["result_identity"]["result_sha256"],
                    active_task=task_ref,
                    recovery_continuation_id="stage0-current",
                ))
        self.assertFalse(checkpoint.exists())
        self.assertFalse(checkpoint.parent.exists())

    def test_active_task_recovery_base_drift_retires_valid_checkpoint(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        task_dir = root / ".trellis/tasks/08-07-context-recovery"
        task_dir.mkdir(parents=True)
        gtt.write_json(task_dir / "task.json", {
            "id": "08-07-context-recovery",
            "status": "in_progress",
            "branch": "main",
        })
        subprocess.run(
            ["git", "add", task_dir.relative_to(root).as_posix()],
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", "test: add context recovery task"],
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["git", "update-ref", "refs/remotes/origin/main", "HEAD"],
            cwd=root,
            check=True,
        )
        payload = self.valid_owner_result(root)
        task_ref = task_dir.relative_to(root).as_posix()
        continuation_id = "stage0-current"
        checkpoint = gtt.context_recovery_checkpoint_path(root, task_dir)

        with mock.patch.object(gtt, "context_live_errors", return_value=[]):
            recorded = gtt.cmd_record_context_discovery(argparse.Namespace(
                root=str(root), mode="workflow", input=None, payload=payload,
                expected_result_sha256=payload["result_identity"]["result_sha256"],
                active_task=task_ref,
                recovery_continuation_id=continuation_id,
            ))
        self.assertTrue(checkpoint.is_file())

        subprocess.run(
            ["git", "commit", "--allow-empty", "-q", "-m", "test: advance base"],
            cwd=root,
            check=True,
        )
        with self.assertRaises(gtt.WorkflowError) as stale:
            gtt.cmd_check_context_discovery(argparse.Namespace(
                root=str(root), input=None, payload=recorded,
                expected_result_sha256=recorded["result_identity"]["result_sha256"],
                active_task=task_ref,
                recovery_continuation_id=continuation_id,
            ))

        self.assertIn("local_base_stale", stale.exception.payload["error_codes"])
        self.assertFalse(checkpoint.exists())
        self.assertFalse(checkpoint.parent.exists())
        self.assertFalse(checkpoint.parent.parent.exists())

    def test_active_task_recovery_recorder_stale_retires_checkpoint_and_accepts_refresh_base(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        task_dir = root / ".trellis/tasks/08-07-context-recovery"
        task_dir.mkdir(parents=True)
        gtt.write_json(task_dir / "task.json", {
            "id": "08-07-context-recovery",
            "status": "in_progress",
            "branch": "main",
        })
        payload = self.valid_owner_result(root)
        task_ref = task_dir.relative_to(root).as_posix()
        continuation_id = "stage0-current"
        checkpoint = gtt.context_recovery_checkpoint_path(root, task_dir)
        args = argparse.Namespace(
            root=str(root), mode="workflow", input=None, payload=payload,
            expected_result_sha256=payload["result_identity"]["result_sha256"],
            active_task=task_ref,
            recovery_continuation_id=continuation_id,
        )

        with mock.patch.object(gtt, "context_live_errors", return_value=[]):
            gtt.cmd_record_context_discovery(args)
        self.assertTrue(checkpoint.is_file())

        with (
            mock.patch.object(
                gtt,
                "context_live_errors",
                return_value=["base_head_stale"],
            ),
            self.assertRaises(gtt.WorkflowError) as stale,
        ):
            gtt.cmd_record_context_discovery(args)

        self.assertEqual(stale.exception.payload["error_codes"], ["base_head_stale"])
        self.assertFalse(checkpoint.exists())
        self.assertFalse(checkpoint.parent.exists())

        refresh_payload = copy.deepcopy(payload)
        refresh_payload["typed_exit"] = "refresh_base"
        refresh_payload["result_identity"] = gtt.context_result_identity(refresh_payload)
        refresh_args = argparse.Namespace(
            root=str(root), mode="workflow", input=None, payload=refresh_payload,
            expected_result_sha256=refresh_payload["result_identity"]["result_sha256"],
            active_task=task_ref,
            recovery_continuation_id=continuation_id,
        )
        with mock.patch.object(
            gtt,
            "context_live_errors",
            return_value=["base_head_stale"],
        ):
            recorded = gtt.cmd_record_context_discovery(refresh_args)

        self.assertEqual(recorded["typed_exit"], "refresh_base")
        self.assertTrue(checkpoint.is_file())

    def test_public_invocation_rejects_repository_owner_locator(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        public_input = self.public_input(root)
        owner_path = root / "owner-result.json"
        owner_path.write_text("{}\n", encoding="utf-8")
        package = (
            Path(gtt.__file__).resolve().parents[4]
            / "skills/guru-team/packages/guru-discover-change-context"
        )
        with (
            mock.patch.object(
                gtt,
                "stage0_invocation_identity",
                return_value=("guru-discover-change-context", package),
            ),
            mock.patch.object(gtt, "stage0_repo_root", return_value=root),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_invoke_stage0_skill(argparse.Namespace(
                input=public_input.relative_to(root).as_posix(),
                owner_result=owner_path.relative_to(root).as_posix(),
            ))
        self.assertEqual(raised.exception.payload["code"], "invalid_owner_result")

    def test_live_base_validation_rejects_current_ref_drift(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        payload = self.valid_owner_result(root)
        self.assertEqual(gtt.context_live_base_errors(root, payload, None), [])
        subprocess.run(
            ["git", "commit", "--allow-empty", "-q", "-m", "test: advance base"],
            cwd=root,
            check=True,
        )
        errors = gtt.context_live_base_errors(root, payload, None)
        self.assertIn("base_head_stale", errors)
        self.assertIn("local_base_stale", errors)

    def test_stale_context_requires_refresh_route_and_short_circuits_later_reads(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        payload = self.valid_owner_result(root)
        with (
            mock.patch.object(
                gtt, "context_live_base_errors", return_value=["base_head_stale"]
            ),
            mock.patch.object(gtt, "context_repo_bound_locator_errors") as locators,
            mock.patch.object(gtt, "context_live_change_errors") as live_change,
            mock.patch.object(gtt, "context_reviewed_blob_errors") as blobs,
        ):
            self.assertEqual(
                gtt.context_live_errors(root, payload, None),
                ["base_head_stale"],
            )
        locators.assert_not_called()
        live_change.assert_not_called()
        blobs.assert_not_called()

        with (
            mock.patch.object(
                gtt, "context_live_errors", return_value=["base_head_stale"]
            ),
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.cmd_check_context_discovery(argparse.Namespace(
                root=str(root), input=None, payload=payload,
                expected_result_sha256=None,
            ))

        payload["typed_exit"] = "refresh_base"
        payload["result_identity"] = gtt.context_result_identity(payload)
        with mock.patch.object(
            gtt, "context_live_errors", return_value=["base_head_stale"]
        ):
            checked = gtt.cmd_check_context_discovery(argparse.Namespace(
                root=str(root), input=None, payload=payload,
                expected_result_sha256=payload["result_identity"]["result_sha256"],
            ))
        self.assertEqual(checked["typed_exit"], "refresh_base")

    def test_current_owner_shape_rejects_undeclared_state(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        payload = self.valid_owner_result(root)
        self.assertEqual(gtt.context_structural_errors(root, payload), [])
        payload["legacy_owner_state"] = {"artifact": "retired.json"}
        payload["result_identity"] = gtt.context_result_identity(payload)
        errors = gtt.context_structural_errors(root, payload)
        self.assertIn("invalid_top_level_fields", errors)
        self.assertIn("context_schema_validation_failed", errors)


class RequirementsClarificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repo = Path(__file__).resolve().parents[5]
        cls.package = (
            cls.repo
            / "trellis/skills/guru-team/packages/guru-clarify-requirements"
        )
        cls.example_path = cls.package / "examples/requirements-clarification.json"
        cls.schema = json.loads(
            (
                cls.package / "schemas/requirements-clarification.schema.json"
            ).read_text(encoding="utf-8")
        )

    def raw_example(self) -> dict[str, object]:
        return json.loads(self.example_path.read_text(encoding="utf-8"))

    def example(self) -> dict[str, object]:
        return gtt.derive_requirements_clarification_result(self.raw_example())

    def derive(self, payload: dict[str, object]) -> dict[str, object]:
        return gtt.derive_requirements_clarification_result(payload)

    def structural(
        self,
        payload: dict[str, object],
        task_dir: Path | None = None,
        root: Path | None = None,
    ) -> list[str]:
        with mock.patch.object(
            gtt, "requirements_clarification_schema", return_value=self.schema
        ):
            return gtt.requirements_clarification_structural_errors(
                root or self.repo, payload, task_dir
            )

    @staticmethod
    def nested_keys(value: object) -> set[str]:
        if isinstance(value, dict):
            return set(value) | set().union(
                *(RequirementsClarificationTests.nested_keys(item) for item in value.values()),
                set(),
            )
        if isinstance(value, list):
            return set().union(
                *(RequirementsClarificationTests.nested_keys(item) for item in value),
                set(),
            )
        return set()

    def set_issue_target(
        self,
        payload: dict[str, object],
        *,
        number: int = 7,
        state: str = "open",
        updated_at: str = "2026-01-01T00:00:00Z",
        body_sha256: str = "1" * 64,
    ) -> dict[str, object]:
        payload["invocation_context"] = {
            "kind": "initial_issue",
            "caller": "initial intake",
            "task_locator": None,
            "resume_target": "guru-review-contract-wording",
        }
        projection = {
            "kind": "issue",
            "repo": "example/guru-extension",
            "issue_number": number,
            "url": f"https://github.com/example/guru-extension/issues/{number}",
            "state": state,
            "updated_at": updated_at,
            "body_sha256": body_sha256,
        }
        payload["review_target"] = {
            **projection,
            "facts_sha256": gtt.context_digest(projection),
        }
        return payload

    def set_target_disposition(
        self,
        payload: dict[str, object],
        disposition: str,
        *,
        candidates: list[dict[str, object]] | None = None,
        selected_issue: dict[str, object] | None = None,
        original_target_role: str = "primary",
    ) -> dict[str, object]:
        payload["target_disposition"] = {
            "disposition": disposition,
            "duplicate_query": (
                "repo:example/guru-extension is:issue is:open reviewed target"
            ),
            "duplicate_checked_at": "2026-01-01T00:00:00Z",
            "duplicate_candidates": candidates or [],
            "duplicate_facts_sha256": "0" * 64,
            "selected_issue": selected_issue,
            "original_target_role": original_target_role,
            "decision_summary": (
                f"The AI selected {disposition} from current evidence."
            ),
            "disposition_digest": "0" * 64,
        }
        return self.derive(payload)

    def duplicate_candidate(
        self,
        number: int,
        *,
        decision: str,
    ) -> dict[str, object]:
        projection = {
            "repo": "example/guru-extension",
            "number": number,
            "identity": f"#{number}",
            "url": f"https://github.com/example/guru-extension/issues/{number}",
            "state": "open",
            "updated_at": "2026-01-01T00:00:00Z",
        }
        return {
            **projection,
            "facts_sha256": gtt.context_digest(projection),
            "decision": decision,
            "reason": "The candidate was compared with the reviewed delivery unit.",
        }

    def closed_followup_payload(
        self,
        body: str = "Reviewed follow-up scope",
    ) -> dict[str, object]:
        payload = self.set_issue_target(self.example(), state="closed")
        payload["typed_exit"] = "new_task"
        payload["consumer"] = {
            "kind": "workflow",
            "id": "guru-full-task-intake-chain",
        }
        payload["source_actions"] = [{
            "action_id": "new_issue",
            "kind": "new_issue_draft",
            "target": {"repo": "example/guru-extension"},
            "payload": {
                "title": "Independent follow-up delivery",
                "body": body,
            },
            "preimage_sha256": None,
            "payload_sha256": None,
            "action_digest": "0" * 64,
            "status": "draft_ready",
            "mutation_evidence": None,
        }]
        return self.set_target_disposition(
            payload,
            "create_followup_draft",
            original_target_role="related",
        )

    def retarget_payload(self) -> dict[str, object]:
        payload = self.example()
        candidate = self.duplicate_candidate(8, decision="selected")
        selected_issue = {
            "repo": candidate["repo"],
            "issue_number": candidate["number"],
            "url": candidate["url"],
            "state": candidate["state"],
            "updated_at": candidate["updated_at"],
            "facts_sha256": candidate["facts_sha256"],
        }
        payload["typed_exit"] = "retarget_context"
        payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
        payload["source_actions"] = [{
            "action_id": "select_existing",
            "kind": "select_existing_issue",
            "target": {
                "repo": candidate["repo"],
                "issue_number": candidate["number"],
            },
            "payload": selected_issue,
            "preimage_sha256": payload["review_target"]["facts_sha256"],
            "payload_sha256": None,
            "action_digest": "0" * 64,
            "status": "validated",
            "mutation_evidence": None,
        }]
        return self.set_target_disposition(
            payload,
            "retarget_existing_issue",
            candidates=[candidate],
            selected_issue=selected_issue,
            original_target_role="related",
        )

    def reopen_closed_payload(self) -> dict[str, object]:
        payload = self.set_issue_target(self.example(), state="closed")
        payload["typed_exit"] = "refresh_context"
        payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
        payload["source_actions"] = [{
            "action_id": "reopen_source",
            "kind": "reopen_issue",
            "target": {
                "repo": "example/guru-extension",
                "issue_number": 7,
            },
            "payload": {"state": "open"},
            "preimage_sha256": payload["review_target"]["facts_sha256"],
            "payload_sha256": None,
            "action_digest": "0" * 64,
            "status": "executed",
            "mutation_evidence": {"source": "ai-reviewed-gh"},
        }]
        payload = self.set_target_disposition(
            payload,
            "reopen_closed_issue",
        )
        action_digest = payload["source_actions"][0]["action_digest"]
        payload["mutation_results"] = [{
            "action_id": "reopen_source",
            "kind": "reopen_issue",
            "status": "succeeded",
            "url": payload["review_target"]["url"],
            "state": "open",
            "updated_at": "2026-01-01T00:00:02Z",
            "content_sha256": payload["review_target"]["body_sha256"],
            "action_digest": action_digest,
            "facts_sha256": "0" * 64,
        }]
        return self.derive(payload)

    def closed_complete_payload(self) -> dict[str, object]:
        payload = self.set_issue_target(self.example(), state="closed")
        payload["typed_exit"] = "blocked"
        payload["consumer"] = {
            "kind": "stop",
            "id": "requirements-clarification-blocked",
        }
        payload["ai_review_gate"]["status"] = "blocked"
        payload["error"] = {
            "codes": ["requirements_target_complete"],
            "summary": "The closed target is complete and no gap remains.",
        }
        return self.set_target_disposition(
            payload,
            "block_target_complete",
            original_target_role="reference",
        )

    def issue_payload_with_action(
        self,
        *,
        kind: str,
        action_id: str,
        body: str,
        mutation_url: str,
        mutation_updated_at: str,
    ) -> dict[str, object]:
        payload = self.set_issue_target(self.example())
        payload["typed_exit"] = "refresh_context"
        payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
        payload["source_actions"] = [{
            "action_id": action_id,
            "kind": kind,
            "target": {
                "repo": "example/guru-extension",
                "issue_number": 7,
            },
            "payload": {"body": body},
            "preimage_sha256": "1" * 64,
            "payload_sha256": None,
            "action_digest": "0" * 64,
            "status": "executed",
            "mutation_evidence": {"source": "ai-reviewed-gh"},
        }]
        payload = self.set_target_disposition(
            payload, "keep_current_open_issue"
        )
        action_digest = payload["source_actions"][0]["action_digest"]
        payload["mutation_results"] = [{
            "action_id": action_id,
            "kind": kind,
            "status": "succeeded",
            "url": mutation_url,
            "state": "open",
            "updated_at": mutation_updated_at,
            "content_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "action_digest": action_digest,
            "facts_sha256": "0" * 64,
        }]
        return self.derive(payload)

    def active_task_classification_payload(
        self,
        root: Path,
    ) -> tuple[
        Path,
        dict[str, object],
        dict[str, object],
        subprocess.CompletedProcess[str],
    ]:
        task = root / ".trellis/tasks/active-scope"
        task.mkdir(parents=True)
        locator = task.relative_to(root).as_posix()
        planning = []
        for name, content in (
            ("prd.md", "# Requirements\n\nKeep the current delivery scope unchanged.\n"),
            ("design.md", "# Design\n\nClassify the request from current authority.\n"),
            ("implement.md", "# Implementation\n\nResume the interrupted owner after classification.\n"),
        ):
            path = task / name
            path.write_text(content, encoding="utf-8")
            planning.append({
                "path": f"{locator}/{name}",
                "content_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })

        payload = self.set_issue_target(self.example())
        payload["invocation_context"] = {
            "kind": "active_task_scope_change",
            "caller": "active task",
            "task_locator": locator,
            "resume_target": "guru-resume-implementation",
        }
        payload["target_disposition"] = None
        payload["context_evidence"] = {
            "status": "current",
            "evidence_refs": ["current-session:change-context"],
            "missing_reason": None,
        }
        payload["scope_proposals"] = [{
            "proposal_id": "classify_out_of_scope",
            "scenario": "Classify an independent active-task request.",
            "trigger_evidence": ["new active-task input"],
            "proposed_contracts": ["one final scope classification"],
            "cost": "A separate delivery and validation path.",
            "alternatives": ["Keep the current confirmed scope unchanged."],
            "consequence_if_omitted": "The independent request remains outside this delivery.",
            "origin_requirement_status": "unconfirmed_expansion",
            "optional_mechanism_origin": False,
            "decision": "out_of_scope",
            "proposal_digest": "0" * 64,
        }]
        payload = self.derive(payload)
        proposal_digest = payload["scope_proposals"][0]["proposal_digest"]
        comment_body = "The independent request is outside the active delivery."
        comment_url = (
            "https://github.com/example/guru-extension/issues/7#issuecomment-99"
        )
        trail = {
            "trail_id": "scope_decision_out_of_scope",
            "proposal_decisions": [{
                "proposal_id": "classify_out_of_scope",
                "proposal_digest": proposal_digest,
                "decision": "out_of_scope",
            }],
            "github_authority": {
                "kind": "issue_comment",
                "url": comment_url,
                "content_sha256": hashlib.sha256(
                    comment_body.encode("utf-8")
                ).hexdigest(),
            },
        }
        ledger_path = task / "issue-scope-ledger.json"
        primary_issue = {
            "number": 7,
            "url": payload["review_target"]["url"],
            "title": "Active scope authority",
            "reason": "Current task close scope.",
        }
        ledger_path.write_text(
            json.dumps({
                "schema_version": "2.0",
                "primary_issue": primary_issue,
                "close_issues": [primary_issue],
                "related_issues": [],
                "followup_issues": [],
            }, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        evidence = {
            "task_locator": locator,
            "github_authority_facts_sha256": payload["review_target"]["facts_sha256"],
            "ledger": {
                "path": f"{locator}/issue-scope-ledger.json",
                "content_sha256": hashlib.sha256(
                    ledger_path.read_bytes()
                ).hexdigest(),
            },
            "planning_documents": planning,
            "decision_trail": trail,
            "reentry_owners": [
                "guru-approve-task-plan",
                "guru-check-task",
                "guru-review-branch",
            ],
        }
        payload["active_task_evidence"] = evidence
        payload["source_actions"] = [{
            "action_id": "task_scope",
            "kind": "active_task_scope_update",
            "target": {"task_locator": locator},
            "payload": gtt.requirements_clarification_active_task_payload_projection(
                evidence
            ),
            "preimage_sha256": gtt.context_digest(payload["context_evidence"]),
            "payload_sha256": None,
            "action_digest": "0" * 64,
            "status": "validated",
            "mutation_evidence": {"source": "task-local-update"},
        }]
        payload["mutation_results"] = []
        payload["typed_exit"] = "clear"
        payload["consumer"] = gtt.REQUIREMENTS_CLARIFICATION_CONSUMERS["clear"]
        payload = self.derive(payload)

        current_issue = {
            "repo": "example/guru-extension",
            "number": 7,
            "url": payload["review_target"]["url"],
            "state": "open",
            "updated_at": payload["review_target"]["updated_at"],
            "body_sha256": payload["review_target"]["body_sha256"],
            "facts_sha256": "unused",
        }
        comment_response = subprocess.CompletedProcess(
            [],
            0,
            json.dumps({
                "id": 99,
                "html_url": comment_url,
                "updated_at": "2026-01-01T00:00:02Z",
                "body": comment_body,
            }),
            "",
        )
        return task, payload, current_issue, comment_response

    def test_example_record_and_check_are_canonical_and_stdout_only(self) -> None:
        before = set(gtt.git_status_paths(self.repo))
        with mock.patch.object(
            gtt, "requirements_clarification_schema", return_value=self.schema
        ):
            recorded = gtt.cmd_record_requirements_clarification(
                argparse.Namespace(
                    root=str(self.repo),
                    mode="standalone",
                    input=str(self.example_path),
                    task=None,
                )
            )
            self.assertEqual(recorded, self.raw_example())
            checked = gtt.cmd_check_requirements_clarification(
                argparse.Namespace(
                    root=str(self.repo),
                    input=str(self.example_path),
                    task=None,
                    expected_result_sha256=recorded["content_identity"]["result_sha256"],
                )
            )
        self.assertEqual(checked["status"], "passed")
        self.assertEqual(checked["typed_exit"], "clear")
        self.assertEqual(set(gtt.git_status_paths(self.repo)), before)

    def test_authorization_fields_are_rejected_not_projected(self) -> None:
        top_level = self.example()
        top_level["human_confirmation"] = {"status": "confirmed"}
        top_level = self.derive(top_level)
        top_errors = self.structural(top_level)
        self.assertIn("requirements_clarification_schema_validation_failed", top_errors)
        self.assertIn("invalid_requirements_clarification_top_level", top_errors)

        nested = self.example()
        nested["target_disposition"]["confirmation_ref"] = "forbidden-confirmation"
        nested = self.derive(nested)
        nested_errors = self.structural(nested)
        self.assertIn("requirements_clarification_schema_validation_failed", nested_errors)
        self.assertIn("invalid_requirements_target_disposition", nested_errors)

        proposal = self.example()
        proposal["scope_proposals"] = [{
            "proposal_id": "forbidden_confirmation",
            "scenario": "A current-shape proposal carries a removed field.",
            "trigger_evidence": ["payload with a removed field"],
            "proposed_contracts": ["scope"],
            "cost": "None.",
            "alternatives": ["Use the current dialogue only."],
            "consequence_if_omitted": "No persistent authorization remains.",
            "origin_requirement_status": "confirmed_expansion",
            "optional_mechanism_origin": False,
            "decision": "related",
            "proposal_digest": "0" * 64,
            "confirmation_ref": "forbidden-confirmation",
        }]
        proposal = self.derive(proposal)
        self.assertIn(
            "requirements_clarification_schema_validation_failed",
            self.structural(proposal),
        )

        forbidden = {
            "confirmed_action_id", "confirmation_ref", "human_confirmation",
            "user_confirmation", "authorization_digest", "confirmed_at",
        }
        self.assertTrue(forbidden.isdisjoint(self.nested_keys(self.example())))

    def test_active_task_compact_trail_keeps_only_direct_consumer_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            task, payload, current_issue, comment_response = (
                self.active_task_classification_payload(root)
            )
            self.assertEqual(self.structural(payload, task, root), [])
            trail = payload["active_task_evidence"]["decision_trail"]
            self.assertEqual(
                set(trail),
                {"trail_id", "proposal_decisions", "github_authority"},
            )
            self.assertEqual(
                set(trail["proposal_decisions"][0]),
                {"proposal_id", "proposal_digest", "decision"},
            )
            self.assertEqual(
                set(trail["github_authority"]),
                {"kind", "url", "content_sha256"},
            )
            forbidden = {
                "user_decision",
                "confirmation_ref",
                "context_before_task_update_sha256",
                "stale_downstream_evidence",
                "review_evidence",
                "interrupted_resume_target",
                "updated_at",
            }
            self.assertTrue(forbidden.isdisjoint(self.nested_keys(trail)))
            ledger = json.loads((task / "issue-scope-ledger.json").read_text(encoding="utf-8"))
            self.assertEqual(
                set(ledger),
                {
                    "schema_version",
                    "primary_issue",
                    "close_issues",
                    "related_issues",
                    "followup_issues",
                },
            )
            self.assertNotIn("decision_trail", self.nested_keys(ledger))
            with (
                mock.patch.object(
                    gtt,
                    "context_read_live_issue",
                    return_value=(current_issue, None),
                ),
                mock.patch.object(gtt, "run", return_value=comment_response),
            ):
                self.assertEqual(
                    gtt.requirements_clarification_live_errors(
                        root, payload, task
                    ),
                    [],
                )

    def test_unknown_fields_on_current_trail_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            task, payload, _current_issue, _comment_response = (
                self.active_task_classification_payload(root)
            )
            payload["active_task_evidence"]["decision_trail"][
                "user_decision"
            ] = {"status": "confirmed"}
            payload = self.derive(payload)
            errors = self.structural(payload, task, root)
            self.assertIn(
                "requirements_clarification_schema_validation_failed",
                errors,
            )
            self.assertIn("active_task_decision_trail_shape_invalid", errors)

    def test_current_target_dispositions_are_closed_without_authorization_state(self) -> None:
        open_issue = self.set_target_disposition(
            self.set_issue_target(self.example()),
            "keep_current_open_issue",
        )
        cases = {
            "keep_current_open_issue": open_issue,
            "retarget_existing_issue": self.retarget_payload(),
            "reopen_closed_issue": self.reopen_closed_payload(),
            "create_followup_draft": self.closed_followup_payload(),
            "block_target_complete": self.closed_complete_payload(),
        }
        for name, payload in cases.items():
            with self.subTest(disposition=name):
                self.assertEqual(self.structural(payload), [])
                self.assertTrue({
                    "confirmation_ref", "human_confirmation", "user_confirmation",
                }.isdisjoint(self.nested_keys(payload)))

    def test_live_mutation_binds_action_payload_and_result_without_authorization(self) -> None:
        payload = self.issue_payload_with_action(
            kind="issue_body_edit",
            action_id="edit_body",
            body="new body",
            mutation_url="https://github.com/example/guru-extension/issues/7",
            mutation_updated_at="2026-01-01T00:00:02Z",
        )
        self.assertEqual(self.structural(payload), [])
        self.assertTrue({
            "confirmation_ref", "human_confirmation", "confirmed_actions",
        }.isdisjoint(self.nested_keys(payload)))

        live_issue = {
            "repo": "example/guru-extension",
            "number": 7,
            "url": "https://github.com/example/guru-extension/issues/7",
            "state": "open",
            "updated_at": "2026-01-01T00:00:02Z",
            "body_sha256": hashlib.sha256(b"new body").hexdigest(),
            "facts_sha256": "unused",
        }
        with mock.patch.object(
            gtt, "context_read_live_issue", return_value=(live_issue, None)
        ):
            live_errors = gtt.requirements_clarification_live_errors(
                self.repo, payload, None
            )
        self.assertEqual(live_errors, ["requirements_target_issue_stale"])
        self.assertEqual(
            gtt.requirements_clarification_typed_exit_live_errors(
                payload, live_errors
            ),
            [],
        )

        mismatch = copy.deepcopy(payload)
        mismatch["mutation_results"][0]["content_sha256"] = "f" * 64
        mismatch = self.derive(mismatch)
        self.assertIn(
            "mutation_payload_result_mismatch",
            self.structural(mismatch),
        )

        missing_result = copy.deepcopy(payload)
        missing_result["mutation_results"] = []
        missing_result = self.derive(missing_result)
        self.assertIn(
            "executed_source_action_requires_mutation_result",
            self.structural(missing_result),
        )

    def test_action_bodies_allow_multiline_markdown_and_reject_controls(self) -> None:
        markdown = "# Clarification\n\n- first\tvalue\r\n- second"
        self.assertTrue(gtt.requirements_clarification_nonempty(markdown))

        def payload_for(kind: str, body: str) -> dict[str, object]:
            if kind == "new_issue_draft":
                return self.closed_followup_payload(body)
            url = "https://github.com/example/guru-extension/issues/7"
            if kind == "issue_comment":
                url += "#issuecomment-99"
            return self.issue_payload_with_action(
                kind=kind,
                action_id=f"multiline_{kind}",
                body=body,
                mutation_url=url,
                mutation_updated_at="2026-01-01T00:00:02Z",
            )

        for kind in ("issue_comment", "issue_body_edit", "new_issue_draft"):
            with self.subTest(kind=kind, value="multiline"):
                self.assertEqual(self.structural(payload_for(kind, markdown)), [])
            expected = (
                "draft_source_action_shape_invalid"
                if kind == "new_issue_draft"
                else "github_source_action_shape_invalid"
            )
            for label, control in (
                ("nul", "\x00"),
                ("other_c0", "\x01"),
                ("del", "\x7f"),
            ):
                with self.subTest(kind=kind, value=label):
                    invalid = markdown + control
                    self.assertFalse(
                        gtt.requirements_clarification_nonempty(invalid)
                    )
                    self.assertIn(
                        expected,
                        self.structural(payload_for(kind, invalid)),
                    )

    def test_non_current_schema_is_rejected_before_derivation(self) -> None:
        invalid = self.raw_example()
        invalid["schema_version"] = "unexpected"
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "invalid-clarification.json"
            path.write_text(json.dumps(invalid) + "\n", encoding="utf-8")
            for command, args in (
                (
                    gtt.cmd_record_requirements_clarification,
                    argparse.Namespace(
                        root=str(self.repo),
                        mode="standalone",
                        input=str(path),
                        task=None,
                    ),
                ),
                (
                    gtt.cmd_check_requirements_clarification,
                    argparse.Namespace(
                        root=str(self.repo),
                        input=str(path),
                        task=None,
                        expected_result_sha256=None,
                    ),
                ),
            ):
                with self.subTest(command=command.__name__), self.assertRaises(
                    gtt.WorkflowError
                ) as raised:
                    command(args)
                self.assertEqual(
                    raised.exception.payload["error_codes"],
                    ["requirements_clarification_schema_version_invalid"],
                )

    def test_public_outputs_are_minimal_consumer_dtos(self) -> None:
        output_paths = sorted(
            (self.package / "examples").glob("public-*-output.json")
        )
        self.assertEqual(len(output_paths), 6)
        forbidden = {
            "confirmed_action_id", "confirmation_ref", "human_confirmation",
            "user_confirmation", "content_identity", "source_actions",
        }
        for path in output_paths:
            with self.subTest(path=path.name):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(forbidden.isdisjoint(self.nested_keys(payload)))


class ChangeRequestReviewRuntimeCommandTests(unittest.TestCase):
    def test_record_and_check_commands_are_registered(self) -> None:
        expected_flags = {
            "record-change-request-review": (
                "--mode", "--input", "--change-request-input",
            ),
            "check-change-request-review": (
                "--input", "--prerequisites-input", "--change-request-input",
                "--expected-facts-sha256",
            ),
        }
        for command, flags in expected_flags.items():
            with self.subTest(command=command):
                process = subprocess.run(
                    [sys.executable, str(Path(gtt.__file__).resolve()), command, "--help"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                for flag in flags:
                    self.assertIn(flag, process.stdout)


if __name__ == "__main__":
    unittest.main()
