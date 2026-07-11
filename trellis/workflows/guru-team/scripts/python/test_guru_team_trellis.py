#!/usr/bin/env python3
"""Focused tests for Guru Team Trellis companion behavior."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
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
        "create_issue_confirmed": False,
        "issue_title": None,
        "issue_body_file": None,
        "base_branch": None,
        "branch": None,
        "task_slug": None,
        "workspace_slug": None,
        "title": None,
        "assignee": None,
        "priority": None,
        "description": None,
        "worktree": False,
        "create_worktree": False,
        "create_task": False,
        "requirement": ["Add default side-effect-free intake planning for freeform requests"],
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def publish_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "repo": None,
        "base_branch": None,
        "remote": None,
        "title": None,
        "validation": [],
        "body_file": None,
        "body_artifact": None,
        "draft": None,
        "allow_metadata_after_gate": False,
        "from_finish_work": False,
        "recovery_after_finish_work": False,
        "dry_run": True,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


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
        "body_file": None,
        "body_artifact": None,
        "draft": None,
        "finish_summary_index_file": "finish-summary-index.json",
        "from_trellis_finish_work": True,
        "skip_archive": False,
        "dry_run": True,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def valid_pr_body(summary: str = "增加 publish-pr 的 reviewed body source 门禁。") -> str:
    return f"""## 变更摘要

- {summary}

## 影响范围

- Guru Team publish helper
- finish-work PR 发布入口

## 验证结果

- python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py 通过

## Review Gate

- 结论：发布边界检查通过。
- Reviewed HEAD：`abc123`

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
        "pass_gate": True,
        "summary": "Branch Review Gate 通过。",
        "evidence": ["已覆盖 CI/CD、Docker、K8s、migration、Makefile 部署影响判断。"],
        "reviewer": "trellis-check-agent",
        "review_source": gtt.INDEPENDENT_REVIEW_SOURCE,
        "review_report": None,
        "agent_assignment": None,
        "finding": [],
        "findings_file": None,
        "observation": [],
        "observations_file": None,
        "followup_candidate": [],
        "followup_candidates_file": None,
        "dry_run": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def planning_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "reviewer": "codex-main-session",
        "summary": "规划 artifact 已审阅，可以进入实现。",
        "ambiguity_reviewer": "codex-main-session",
        "ambiguity_summary": "已完成 planning artifact ambiguity review，规范性条款无未处理弱约束表达。",
        "ambiguity_status": gtt.PLANNING_AMBIGUITY_STATUS_PASSED,
        "user_confirmation": "用户确认进入实现。",
        "review_prompt_presented_at": None,
        "confirmation_source": gtt.PLANNING_APPROVAL_CONFIRMATION_SOURCE,
        "normative_hit": None,
        "artifact": None,
        "dry_run": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def phase2_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "pass_check": True,
        "checker": "codex-main-session",
        "summary": "已按完整 task scope 执行 trellis-check。",
        "checked_artifact": None,
        "checked_spec": None,
        "coverage": list(gtt.REQUIRED_PHASE2_COVERAGE),
        "validation": ["python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py|passed"],
        "finding": [],
        "findings_file": None,
        "dry_run": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def assignment_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "logical_role": "实现代理",
        "agent_id": "019f315a-f262-7521-acdf-78e4adc99a11",
        "platform_nickname": "Gibbs",
        "reason": "Codex sub-agent 模式下分配实现代理。",
        "review_round": None,
        "review_round_report": None,
        "reviewed_head": None,
        "findings_count": 0,
        "reuse_policy": None,
        "reuse_decision": None,
        "reuse_reason": None,
        "from_round": None,
        "to_round": None,
        "decision_head": None,
        "status_event": None,
        "decision": None,
        "observed_at": None,
        "last_observed_progress_at": None,
        "workspace_evidence": None,
        "running_command_evidence": None,
        "handoff_summary": None,
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


def liveness_event_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "source_repo": None,
        "agent_id": "agent-a",
        "event": "assigned",
        "observed_at": "2026-07-07T00:00:00Z",
        "evidence": "分配实现代理。",
        "logical_role": "实现代理",
        "platform_nickname": "Implement A",
        "source": "main-session",
        "predecessor_agent_id": None,
        "predecessor_event_id": None,
        "termination_reason": None,
        "termination_source_event_id": None,
        "replacement_reason": None,
        "handoff_summary": None,
        "dry_run": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def liveness_check_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "source_repo": None,
        "agent_id": "agent-a",
        "progress_scan_interval": 120,
        "max_progress_silence": 180,
        "checked_at": "2026-07-07T00:00:00Z",
        "dry_run": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class ConventionalCommitContractTest(unittest.TestCase):
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


class PrepareSideEffectBoundaryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".trellis").mkdir()
        self.worktree_root = self.root / "worktrees"
        (self.root / ".trellis/.developer").write_text(
            "name=tester\ninitialized_at=2026-07-04T00:00:00\n",
            encoding="utf-8",
        )

        self.patches = [
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={
                **gtt.DEFAULTS,
                "github_repo": "owner/repo",
                "task_start_context_artifact": "task-start-context.json",
                "runtime_root": ".trellis/.runtime/guru-team",
            }),
            mock.patch.object(gtt, "require_tool"),
            mock.patch.object(gtt, "require_gh_auth"),
            mock.patch.object(gtt, "duplicate_search", return_value=[]),
            mock.patch.object(gtt, "resolve_base_branch", return_value=("main", ["main", "origin/main"])),
            mock.patch.object(gtt, "current_branch", return_value="main"),
            mock.patch.object(gtt, "git_dirty", return_value=False),
            mock.patch.object(gtt, "worktree_lines", return_value=[]),
            mock.patch.object(gtt, "configured_worktree_root", return_value=self.worktree_root),
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
            mock.patch.object(gtt, "create_task") as create_task,
            mock.patch.object(gtt, "run_stdout") as run_stdout,
        ):
            payload = gtt.cmd_prepare(prepare_args())

        create_issue.assert_not_called()
        create_task.assert_not_called()
        run_stdout.assert_not_called()
        self.assertIsNone(payload["source_issue"])
        self.assertTrue(payload["requires_confirmation"]["create_issue"])
        self.assertEqual(payload["workspace_ready"], False)
        self.assertEqual(payload["preflight"]["workspace_was_created_or_reused"], False)
        self.assertNotIn("task_start_context", payload)
        self.assertFalse((self.root / ".trellis/.runtime/guru-team").exists())
        self.assertFalse((self.root / ".trellis/tasks").exists())
        self.assertEqual(payload["proposed_issue"]["title"], "Add default side-effect-free intake planning for freeform requests")

    def test_create_worktree_requires_confirmed_source_issue(self) -> None:
        with (
            mock.patch.object(gtt, "create_issue") as create_issue,
            mock.patch.object(gtt, "run_stdout") as run_stdout,
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.cmd_prepare(prepare_args(create_worktree=True))

        create_issue.assert_not_called()
        run_stdout.assert_not_called()

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

    def test_prepare_legacy_branch_prefix_does_not_affect_automatic_branch(self) -> None:
        payload = gtt.prepare_naming_payload(
            prepare_args(short_name="052-semantic-business-name"),
            {**gtt.DEFAULTS, "branch_prefix": "codex/"},
            "52",
            "Fix broken prepare task naming",
        )

        self.assertEqual(payload["branch_name"], "fix/052-semantic-business-name")

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

    def test_prepare_planner_refreshes_base_without_executor_fast_forward(self) -> None:
        existing_issue = {
            "number": 52,
            "url": "https://github.com/owner/repo/issues/52",
            "title": "Add resume detail inline attachment preview",
        }
        freshness = {
            "remote": "origin",
            "base_branch": "main",
            "base_ref": "main",
            "remote_ref": "origin/main",
            "local_head_before": "old",
            "local_head_after": "old",
            "remote_head": "new",
            "remote_head_source": "fetched",
            "fetch_attempted": True,
            "fetch_performed": True,
            "fast_forwarded": False,
            "fresh": False,
            "status": "stale",
            "base_ref_for_worktree": "origin/main",
        }
        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "refresh_base_freshness_for_planner", return_value=freshness) as refresh,
            mock.patch.object(gtt, "ensure_base_freshness") as ensure_base_freshness,
        ):
            payload = gtt.cmd_prepare(prepare_args(requirement=["#52"]))

        refresh.assert_called_once_with(self.root, "main")
        ensure_base_freshness.assert_not_called()
        self.assertEqual(payload["preflight"]["base_freshness"]["fetch_performed"], True)
        self.assertEqual(payload["preflight"]["base_freshness"]["fast_forwarded"], False)
        self.assertEqual(payload["preflight"]["base_freshness"]["status"], "stale")
        self.assertEqual(payload["preflight"]["base_freshness"]["local_head_before"], "old")
        self.assertEqual(payload["preflight"]["base_freshness"]["local_head_after"], "old")

    def test_prepare_chinese_issue_title_marks_naming_quality_without_side_effects(self) -> None:
        existing_issue = {
            "number": 52,
            "url": "https://github.com/owner/repo/issues/52",
            "title": "简历详情页的原始简历查看功能应该强化",
        }
        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "create_task") as create_task,
            mock.patch.object(gtt, "run_stdout") as run_stdout,
        ):
            payload = gtt.cmd_prepare(prepare_args(requirement=["#52"]))

        create_task.assert_not_called()
        run_stdout.assert_not_called()
        self.assertFalse(payload["naming_quality"]["ok"])
        self.assertTrue(payload["naming_quality"]["requires_semantic_name"])
        self.assertEqual(payload["naming_quality"]["current_slug"], "issue-52")
        suggested_flags = " ".join(payload["naming_quality"]["suggested_override_flags"])
        self.assertIn("--short-name", suggested_flags)
        self.assertIn("--branch chore/052-semantic-business-name", suggested_flags)
        self.assertNotIn("--branch codex/", suggested_flags)
        self.assertEqual(payload["task_slug"], "52-issue-52")
        self.assertFalse(payload["workspace_ready"])

    def test_prepare_chinese_issue_title_blocks_create_before_side_effects(self) -> None:
        existing_issue = {
            "number": 52,
            "url": "https://github.com/owner/repo/issues/52",
            "title": "简历详情页的原始简历查看功能应该强化",
        }
        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "ensure_base_freshness") as ensure_base_freshness,
            mock.patch.object(gtt, "prepare_workspace") as prepare_workspace,
            mock.patch.object(gtt, "create_task") as create_task,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_prepare(prepare_args(requirement=["#52"], create_worktree=True))

        ensure_base_freshness.assert_not_called()
        prepare_workspace.assert_not_called()
        create_task.assert_not_called()
        self.assertEqual(raised.exception.exit_code, 2)
        self.assertFalse(raised.exception.payload["naming_quality"]["ok"])
        self.assertTrue(raised.exception.payload["naming_quality"]["requires_semantic_name"])
        self.assertIn("--short-name/--workspace-slug/--branch/--task-slug", str(raised.exception))

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

    def test_prepare_confirmed_chinese_issue_blocks_before_issue_creation(self) -> None:
        body_path = self.root / "reviewed-issue.md"
        body_path.write_text("Reviewed issue body\n", encoding="utf-8")
        with (
            mock.patch.object(gtt, "create_issue") as create_issue,
            mock.patch.object(gtt, "ensure_base_freshness") as ensure_base_freshness,
            mock.patch.object(gtt, "prepare_workspace") as prepare_workspace,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_prepare(
                prepare_args(
                    requirement=["简历详情页的原始简历查看功能应该强化，并补充任务命名门禁。"],
                    create_issue_confirmed=True,
                    issue_title="简历详情页的原始简历查看功能应该强化",
                    issue_body_file=str(body_path),
                    create_worktree=True,
                )
            )

        create_issue.assert_not_called()
        ensure_base_freshness.assert_not_called()
        prepare_workspace.assert_not_called()
        self.assertEqual(raised.exception.exit_code, 2)
        self.assertFalse(raised.exception.payload["naming_quality"]["ok"])

    def test_prepare_semantic_short_name_override_passes_create_naming_quality(self) -> None:
        existing_issue = {
            "number": 52,
            "url": "https://github.com/owner/repo/issues/52",
            "title": "简历详情页的原始简历查看功能应该强化",
        }
        workspace = self.worktree_root / "052-resume-detail-inline-attachment-preview"
        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "ensure_base_freshness", return_value={
                "remote": "origin",
                "base_branch": "main",
                "base_ref": "main",
                "remote_ref": "origin/main",
                "local_head_before": "abc",
                "local_head_after": "abc",
                "remote_head": "abc",
                "fetch_performed": True,
                "fast_forwarded": False,
                "fresh": True,
                "status": "fresh",
                "base_ref_for_worktree": "main",
            }),
            mock.patch.object(gtt, "prepare_workspace", return_value=("worktree", workspace, True)) as prepare_workspace,
            mock.patch.object(gtt, "ensure_workspace_developer_identity", return_value={
                "status": "copied",
                "developer": "tester",
            }),
        ):
            payload = gtt.cmd_prepare(
                prepare_args(
                    requirement=["#52"],
                    short_name="052-resume-detail-inline-attachment-preview",
                    create_worktree=True,
                )
            )

        self.assertTrue(payload["naming_quality"]["ok"])
        self.assertEqual(payload["task_slug"], "052-resume-detail-inline-attachment-preview")
        self.assertEqual(payload["workspace_slug"], "052-resume-detail-inline-attachment-preview")
        self.assertEqual(payload["branch_name"], "chore/052-resume-detail-inline-attachment-preview")
        prepare_workspace.assert_called_once_with(
            self.root,
            mock.ANY,
            "chore/052-resume-detail-inline-attachment-preview",
            "052-resume-detail-inline-attachment-preview",
            "main",
            False,
            True,
        )

    def test_prepare_all_semantic_override_surfaces_pass_create_naming_quality(self) -> None:
        existing_issue = {
            "number": 52,
            "url": "https://github.com/owner/repo/issues/52",
            "title": "简历详情页的原始简历查看功能应该强化",
        }
        workspace = self.worktree_root / "052-resume-detail-inline-attachment-preview"
        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "ensure_base_freshness", return_value={
                "remote": "origin",
                "base_branch": "main",
                "base_ref": "main",
                "remote_ref": "origin/main",
                "local_head_before": "abc",
                "local_head_after": "abc",
                "remote_head": "abc",
                "fetch_performed": True,
                "fast_forwarded": False,
                "fresh": True,
                "status": "fresh",
                "base_ref_for_worktree": "main",
            }),
            mock.patch.object(gtt, "prepare_workspace", return_value=("worktree", workspace, True)),
            mock.patch.object(gtt, "ensure_workspace_developer_identity", return_value={
                "status": "copied",
                "developer": "tester",
            }),
        ):
            payload = gtt.cmd_prepare(
                prepare_args(
                    requirement=["#52"],
                    short_name="052-resume-detail-inline-attachment-preview",
                    workspace_slug="052-resume-detail-inline-attachment-preview",
                    task_slug="052-resume-detail-inline-attachment-preview",
                    branch="custom/052-resume-detail-inline-attachment-preview",
                    create_worktree=True,
                )
            )

        self.assertTrue(payload["naming_quality"]["ok"])
        self.assertEqual(payload["slug"], "052-resume-detail-inline-attachment-preview")
        self.assertEqual(payload["task_slug"], "052-resume-detail-inline-attachment-preview")
        self.assertEqual(payload["workspace_slug"], "052-resume-detail-inline-attachment-preview")
        self.assertEqual(payload["branch_name"], "custom/052-resume-detail-inline-attachment-preview")

    def test_prepare_blocks_when_short_name_missing_even_if_other_surfaces_are_semantic(self) -> None:
        existing_issue = {
            "number": 52,
            "url": "https://github.com/owner/repo/issues/52",
            "title": "简历详情页的原始简历查看功能应该强化",
        }
        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "ensure_base_freshness") as ensure_base_freshness,
            mock.patch.object(gtt, "prepare_workspace") as prepare_workspace,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_prepare(
                prepare_args(
                    requirement=["#52"],
                    workspace_slug="052-resume-detail-inline-attachment-preview",
                    task_slug="052-resume-detail-inline-attachment-preview",
                    branch="custom/052-resume-detail-inline-attachment-preview",
                    create_worktree=True,
                )
            )

        ensure_base_freshness.assert_not_called()
        prepare_workspace.assert_not_called()
        self.assertFalse(raised.exception.payload["naming_quality"]["ok"])
        self.assertEqual(raised.exception.payload["naming_quality"]["current_surface"], "slug")
        self.assertEqual(raised.exception.payload["naming_quality"]["current_slug"], "issue-52")

    def test_prepare_low_information_short_name_override_blocks_create(self) -> None:
        existing_issue = {
            "number": 52,
            "url": "https://github.com/owner/repo/issues/52",
            "title": "Add resume detail inline attachment preview",
        }
        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "ensure_base_freshness") as ensure_base_freshness,
            mock.patch.object(gtt, "prepare_workspace") as prepare_workspace,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_prepare(
                prepare_args(
                    requirement=["#52"],
                    short_name="issue-52",
                    create_worktree=True,
                )
            )

        ensure_base_freshness.assert_not_called()
        prepare_workspace.assert_not_called()
        self.assertEqual(raised.exception.exit_code, 2)
        self.assertFalse(raised.exception.payload["naming_quality"]["ok"])
        self.assertEqual(raised.exception.payload["naming_quality"]["current_slug"], "issue-52")

    def test_high_duplicate_payload_includes_reviewed_force_new_command(self) -> None:
        duplicate = {
            "number": 6,
            "title": "Existing duplicate",
            "url": "https://github.com/owner/repo/issues/6",
            "similarity": "high",
        }
        with (
            mock.patch.object(gtt, "duplicate_search", return_value=[duplicate]),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_prepare(prepare_args())

        payload = raised.exception.payload
        self.assertEqual(payload["duplicates"], [duplicate])
        self.assertEqual(payload["proposed_issue"]["title"], "Add default side-effect-free intake planning for freeform requests")
        self.assertIn("--force-new", payload["proposed_issue"]["create_issue_command"])
        self.assertTrue(payload["requires_confirmation"]["reuse_issue_or_force_new"])

    def test_confirmed_issue_creation_uses_reviewed_body(self) -> None:
        body_path = self.root / "reviewed-issue.md"
        body_path.write_text("Reviewed issue body\n", encoding="utf-8")
        created_issue = {
            "number": 42,
            "url": "https://github.com/owner/repo/issues/42",
            "title": "Reviewed title",
        }
        with mock.patch.object(gtt, "create_issue", return_value=created_issue) as create_issue:
            payload = gtt.cmd_prepare(
                prepare_args(
                    create_issue_confirmed=True,
                    issue_title="Reviewed title",
                    issue_body_file=str(body_path),
                )
            )

        create_issue.assert_called_once_with(
            "owner/repo",
            "Reviewed title",
            "Reviewed issue body",
            self.root,
            [],
        )
        self.assertEqual(payload["source_issue"]["number"], 42)
        self.assertTrue(payload["source_issue"]["created_by_workflow"])
        self.assertIsNone(payload["requires_confirmation"])
        self.assertNotIn("task_start_context", payload)
        self.assertFalse((self.root / "handoff.json").exists())

    def test_create_worktree_writes_only_local_runtime_mapping(self) -> None:
        existing_issue = {
            "number": 42,
            "url": "https://github.com/owner/repo/issues/42",
            "title": "Resume attachment preview",
        }
        workspace = self.worktree_root / "42-resume-attachment-preview"
        workspace.mkdir(parents=True)
        (workspace / ".git").mkdir()

        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "ensure_base_freshness", return_value={
                "remote": "origin",
                "base_branch": "main",
                "base_ref": "main",
                "remote_ref": "origin/main",
                "local_head_before": "abc",
                "local_head_after": "abc",
                "remote_head": "abc",
                "fetch_performed": True,
                "fast_forwarded": False,
                "fresh": True,
                "status": "fresh",
                "base_ref_for_worktree": "main",
            }),
            mock.patch.object(gtt, "run_stdout") as run_stdout,
        ):
            payload = gtt.cmd_prepare(prepare_args(requirement=["#42"], create_worktree=True))

        run_stdout.assert_not_called()
        self.assertEqual(payload["source_issue"]["number"], 42)
        self.assertEqual(payload["workspace_path"], str(workspace))
        runtime = workspace / ".trellis/.runtime/guru-team/workspaces/42-resume-attachment-preview.json"
        self.assertTrue(runtime.exists())
        self.assertEqual(json.loads(runtime.read_text())["workspace_path"], str(workspace.resolve()))
        self.assertNotIn("task_start_context", payload)
        self.assertTrue((workspace / ".trellis/.developer").exists())
        self.assertEqual((workspace / ".trellis/.developer").read_text(encoding="utf-8"), "name=tester\ninitialized_at=2026-07-04T00:00:00\n")
        self.assertEqual(payload["preflight"]["developer_identity"]["status"], "copied")

    def test_create_task_runs_task_py_in_workspace(self) -> None:
        workspace = self.worktree_root / "42-resume-attachment-preview"
        workspace.mkdir(parents=True)
        (self.root / ".trellis/scripts").mkdir(parents=True)
        (self.root / ".trellis/scripts/task.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        payload = {
            "workspace_path": str(workspace),
            "task_title": "#42 Resume attachment preview",
            "task_slug": "42-resume-attachment-preview",
        }
        proc = mock.Mock(returncode=0, stdout=".trellis/tasks/07-04-42-resume-attachment-preview\n", stderr="")

        with mock.patch.object(gtt, "run", return_value=proc) as run:
            task_dir = gtt.create_task(self.root, payload, prepare_args(requirement=["#42"], create_task=True))

        self.assertEqual(task_dir, ".trellis/tasks/07-04-42-resume-attachment-preview")
        run.assert_called_once()
        self.assertEqual(run.call_args.kwargs["cwd"], workspace)
        self.assertIn("./.trellis/scripts/task.py", run.call_args.args[0])

    def test_create_worktree_refreshes_base_before_workspace_creation(self) -> None:
        existing_issue = {
            "number": 42,
            "url": "https://github.com/owner/repo/issues/42",
            "title": "Resume attachment preview",
        }
        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "ensure_base_freshness", return_value={
                "remote": "origin",
                "base_branch": "main",
                "base_ref": "main",
                "remote_ref": "origin/main",
                "local_head_before": "old",
                "local_head_after": "new",
                "remote_head": "new",
                "fetch_performed": True,
                "fast_forwarded": True,
                "fresh": True,
                "status": "fresh",
                "base_ref_for_worktree": "main",
            }) as refresh,
            mock.patch.object(gtt, "refresh_base_freshness_for_planner") as planner_refresh,
            mock.patch.object(gtt, "prepare_workspace", return_value=("worktree", self.worktree_root / "42-resume-attachment-preview", True)) as prepare_workspace,
            mock.patch.object(gtt, "ensure_workspace_developer_identity", return_value={
                "status": "copied",
                "developer": "tester",
            }) as ensure_identity,
        ):
            payload = gtt.cmd_prepare(prepare_args(requirement=["#42"], create_worktree=True))

        refresh.assert_called_once_with(self.root, "main")
        planner_refresh.assert_not_called()
        prepare_workspace.assert_called_once()
        ensure_identity.assert_called_once_with(self.root, self.worktree_root / "42-resume-attachment-preview", "tester")
        self.assertEqual(payload["preflight"]["base_freshness"]["fetch_performed"], True)
        self.assertEqual(payload["preflight"]["base_freshness"]["remote_head"], "new")

    def test_infer_assignee_reads_developer_name_field(self) -> None:
        self.assertEqual(gtt.infer_assignee(self.root, None), "tester")
        self.assertEqual(gtt.infer_assignee(self.root, "explicit-dev"), "explicit-dev")

    def test_infer_assignee_allows_legacy_single_line_identity(self) -> None:
        (self.root / ".trellis/.developer").write_text("legacy-dev\n", encoding="utf-8")
        self.assertEqual(gtt.infer_assignee(self.root, None), "legacy-dev")

    def test_create_worktree_initializes_developer_identity_from_explicit_assignee(self) -> None:
        existing_issue = {
            "number": 42,
            "url": "https://github.com/owner/repo/issues/42",
            "title": "Resume attachment preview",
        }
        (self.root / ".trellis/.developer").unlink()
        workspace = self.worktree_root / "42-resume-attachment-preview"
        workspace.mkdir(parents=True)
        (workspace / ".git").mkdir()

        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "ensure_base_freshness", return_value={
                "remote": "origin",
                "base_branch": "main",
                "base_ref": "main",
                "remote_ref": "origin/main",
                "local_head_before": "abc",
                "local_head_after": "abc",
                "remote_head": "abc",
                "fetch_performed": True,
                "fast_forwarded": False,
                "fresh": True,
                "status": "fresh",
                "base_ref_for_worktree": "main",
            }),
        ):
            payload = gtt.cmd_prepare(
                prepare_args(
                    requirement=["#42"],
                    create_worktree=True,
                    assignee="explicit-dev",
                )
            )

        identity = (workspace / ".trellis/.developer").read_text(encoding="utf-8")
        self.assertIn("name=explicit-dev\n", identity)
        self.assertEqual(payload["preflight"]["developer_identity"]["status"], "initialized")
        self.assertEqual(payload["preflight"]["developer_identity"]["developer"], "explicit-dev")

    def test_create_worktree_blocks_when_developer_identity_missing(self) -> None:
        existing_issue = {
            "number": 42,
            "url": "https://github.com/owner/repo/issues/42",
            "title": "Resume attachment preview",
        }
        (self.root / ".trellis/.developer").unlink()
        workspace = self.worktree_root / "42-resume-attachment-preview"
        workspace.mkdir(parents=True)
        (workspace / ".git").mkdir()

        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "ensure_base_freshness", return_value={
                "remote": "origin",
                "base_branch": "main",
                "base_ref": "main",
                "remote_ref": "origin/main",
                "local_head_before": "abc",
                "local_head_after": "abc",
                "remote_head": "abc",
                "fetch_performed": True,
                "fast_forwarded": False,
                "fresh": True,
                "status": "fresh",
                "base_ref_for_worktree": "main",
            }),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_prepare(prepare_args(requirement=["#42"], create_worktree=True))

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(raised.exception.payload["missing_identity"])
        self.assertIn("init_developer.py <name>", raised.exception.payload["recovery_command"])
        self.assertFalse((workspace / ".trellis/.developer").exists())

    def test_ensure_base_freshness_fast_forwards_current_base(self) -> None:
        fetch_result = mock.Mock(returncode=0, stdout="", stderr="")
        with (
            mock.patch.object(gtt, "ref_head", side_effect=["old", "new", "new"]),
            mock.patch.object(gtt, "run", return_value=fetch_result) as run,
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(gtt, "current_branch", return_value="main"),
            mock.patch.object(gtt, "git_dirty", return_value=False),
            mock.patch.object(gtt, "run_stdout") as run_stdout,
        ):
            payload = gtt.ensure_base_freshness(self.root, "main")

        run.assert_called_once_with(["git", "fetch", "origin", "main"], cwd=self.root, check=False)
        run_stdout.assert_called_once_with(["git", "merge", "--ff-only", "origin/main"], cwd=self.root)
        self.assertTrue(payload["fresh"])
        self.assertTrue(payload["fast_forwarded"])
        self.assertEqual(payload["base_ref_for_worktree"], "main")

    def test_ensure_base_freshness_rejects_diverged_base(self) -> None:
        fetch_result = mock.Mock(returncode=0, stdout="", stderr="")
        with (
            mock.patch.object(gtt, "ref_head", side_effect=["local", "remote"]),
            mock.patch.object(gtt, "run", return_value=fetch_result),
            mock.patch.object(gtt, "is_ancestor", return_value=False),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.ensure_base_freshness(self.root, "main")

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("diverged", str(raised.exception))
        self.assertEqual(raised.exception.payload["remote_ref"], "origin/main")

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

            payload = gtt.ensure_base_freshness(local, "main")

            self.assertTrue(payload["fetch_performed"])
            self.assertTrue(payload["fast_forwarded"])
            self.assertTrue(payload["fresh"])
            self.assertEqual(payload["remote_head"], remote_head)
            self.assertEqual(gtt.ref_head(local, "main"), remote_head)
            self.assertEqual(gtt.ref_head(local, "origin/main"), remote_head)

    def test_planner_refresh_base_freshness_fetches_without_fast_forwarding_local_base(self) -> None:
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
            subprocess.run(["git", "symbolic-ref", "HEAD", "refs/heads/main"], cwd=remote, check=True)
            subprocess.run(["git", "clone", str(remote), str(local)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            local_head_before = gtt.ref_head(local, "main")
            self.assertEqual(local_head_before, gtt.ref_head(local, "origin/main"))

            (seed / "README.md").write_text("two\n", encoding="utf-8")
            subprocess.run(["git", "commit", "-am", "two"], cwd=seed, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "push", "origin", "main"], cwd=seed, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            remote_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=seed, text=True).strip()

            payload = gtt.refresh_base_freshness_for_planner(local, "main")

            self.assertTrue(payload["fetch_attempted"])
            self.assertTrue(payload["fetch_performed"])
            self.assertFalse(payload["fast_forwarded"])
            self.assertFalse(payload["fresh"])
            self.assertEqual(payload["status"], "stale")
            self.assertEqual(payload["local_head_before"], local_head_before)
            self.assertEqual(payload["local_head_after"], local_head_before)
            self.assertEqual(payload["remote_head"], remote_head)
            self.assertEqual(payload["base_ref_for_worktree"], "origin/main")
            self.assertEqual(gtt.ref_head(local, "main"), local_head_before)
            self.assertEqual(gtt.ref_head(local, "origin/main"), remote_head)

    def test_planner_refresh_base_freshness_reports_diverged(self) -> None:
        fetch_result = mock.Mock(returncode=0, stdout="", stderr="")
        with (
            mock.patch.object(gtt, "ref_head", side_effect=["local", "remote", "local"]),
            mock.patch.object(gtt, "run", return_value=fetch_result) as run,
            mock.patch.object(gtt, "is_ancestor", return_value=False) as is_ancestor,
        ):
            payload = gtt.refresh_base_freshness_for_planner(self.root, "main")

        run.assert_called_once_with(["git", "fetch", "origin", "main"], cwd=self.root, check=False)
        is_ancestor.assert_called_once_with(self.root, "local", "origin/main")
        self.assertTrue(payload["fetch_performed"])
        self.assertFalse(payload["fresh"])
        self.assertEqual(payload["fast_forwarded"], False)
        self.assertEqual(payload["status"], "diverged")
        self.assertEqual(payload["local_head_before"], "local")
        self.assertEqual(payload["local_head_after"], "local")
        self.assertEqual(payload["remote_head"], "remote")

    def test_planner_refresh_base_freshness_reports_fetch_failed(self) -> None:
        fetch_result = mock.Mock(returncode=128, stdout="", stderr="network unavailable\n")
        with (
            mock.patch.object(gtt, "ref_head", side_effect=["local-before", "local-after"]),
            mock.patch.object(gtt, "run", return_value=fetch_result) as run,
            mock.patch.object(gtt, "is_ancestor") as is_ancestor,
        ):
            payload = gtt.refresh_base_freshness_for_planner(self.root, "main")

        run.assert_called_once_with(["git", "fetch", "origin", "main"], cwd=self.root, check=False)
        is_ancestor.assert_not_called()
        self.assertTrue(payload["fetch_attempted"])
        self.assertFalse(payload["fetch_performed"])
        self.assertFalse(payload["fast_forwarded"])
        self.assertFalse(payload["fresh"])
        self.assertEqual(payload["status"], "fetch_failed")
        self.assertEqual(payload["remote_head_source"], "unconfirmed")
        self.assertEqual(payload["fetch_error"], "network unavailable")
        self.assertEqual(payload["local_head_before"], "local-before")
        self.assertEqual(payload["local_head_after"], "local-after")
        self.assertIsNone(payload["remote_head"])

    def test_confirmed_issue_creation_requires_reviewed_title(self) -> None:
        body_path = self.root / "reviewed-issue.md"
        body_path.write_text("Reviewed issue body\n", encoding="utf-8")
        with (
            mock.patch.object(gtt, "create_issue") as create_issue,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_prepare(
                prepare_args(
                    create_issue_confirmed=True,
                    issue_body_file=str(body_path),
                )
            )

        create_issue.assert_not_called()
        self.assertIn("--issue-title", str(raised.exception))


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

    def test_resolve_active_task_returns_five_markdown_artifacts_only(self) -> None:
        self.write_artifacts(self.task_dir, ["prd.md", "design.md", "implement.md", "review.md", "pr-body.md"])
        for json_artifact in ["phase2-check.json", "review-gate.json", "pr-readiness.json", "agent-assignment.json"]:
            (self.task_dir / json_artifact).write_text("{}\n", encoding="utf-8")

        payload = gtt.cmd_resolve_human_artifacts(
            resolve_human_artifacts_args(root=str(self.root), task=self.task_rel)
        )

        self.assertEqual(payload["status"], "ok")
        self.assertFalse(payload["archived"])
        self.assertEqual(payload["task_dir_relative"], self.task_rel)
        artifacts = self.artifact_by_filename(payload)
        self.assertEqual(
            list(artifacts),
            ["prd.md", "design.md", "implement.md", "review.md", "pr-body.md"],
        )
        for filename, artifact in artifacts.items():
            self.assertTrue(artifact["exists"], filename)
            self.assertEqual(artifact["status"], "已生成")
            self.assertEqual(artifact["path"], f"{self.task_rel}/{filename}")
            self.assertEqual(artifact["link"], str((self.task_dir / filename).resolve()))
        artifact_text = json.dumps(payload, ensure_ascii=False)
        self.assertNotIn("phase2-check.json", artifact_text)
        self.assertNotIn("review-gate.json", artifact_text)
        self.assertNotIn("pr-readiness.json", artifact_text)
        self.assertNotIn("agent-assignment.json", artifact_text)

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
        self.assertFalse(artifacts["review.md"]["exists"])
        self.assertEqual(artifacts["review.md"]["status"], "未执行")
        self.assertEqual(artifacts["review.md"]["link"], "")

    def test_resolve_archive_task_when_active_task_is_missing(self) -> None:
        shutil.rmtree(self.task_dir)
        archived = self.root / f".trellis/tasks/archive/2026-07/{self.task_name}"
        archived.mkdir(parents=True)
        (archived / "task.json").write_text('{"title":"Archived human artifacts"}\n', encoding="utf-8")
        self.write_artifacts(archived, ["prd.md", "design.md", "implement.md", "review.md"])

        payload = gtt.cmd_resolve_human_artifacts(
            resolve_human_artifacts_args(root=str(self.root), task=self.task_name)
        )

        archived_rel = f".trellis/tasks/archive/2026-07/{self.task_name}"
        self.assertTrue(payload["archived"])
        self.assertEqual(payload["task_dir_relative"], archived_rel)
        artifacts = self.artifact_by_filename(payload)
        self.assertEqual(artifacts["review.md"]["path"], f"{archived_rel}/review.md")
        self.assertEqual(artifacts["review.md"]["link"], str((archived / "review.md").resolve()))
        self.assertFalse(artifacts["pr-body.md"]["exists"])
        self.assertEqual(artifacts["pr-body.md"]["link"], "")


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
        self.task_dir.mkdir(parents=True)
        (self.task_dir / "task.json").write_text('{"title":"Boundary task","base_branch":"main"}\n', encoding="utf-8")
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
        gtt.write_json(self.task_dir / "task-start-context.json", self.task_context)
        runtime = {
            "schema_version": "1.0", "workspace_slug": "060-workspace-boundary-guard",
            "workspace_path": str(self.workspace.resolve()), "source_checkout": str(self.source.resolve()),
            "branch_name": "chore/060-workspace-boundary-guard", "updated_at": gtt.now_iso(),
        }
        gtt.write_json(gtt.runtime_workspace_path(self.workspace, gtt.DEFAULTS, "060-workspace-boundary-guard"), runtime)
        gtt.write_json(gtt.runtime_workspace_path(self.source, gtt.DEFAULTS, "060-workspace-boundary-guard"), runtime)

    def tearDown(self) -> None:
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
        records = [
            {"worktree": str(self.source), "branch": "refs/heads/main"},
            {"worktree": str(self.workspace), "branch": "refs/heads/chore/060-workspace-boundary-guard"},
        ]

        with mock.patch.object(gtt, "worktree_records", return_value=records):
            payload = gtt.cmd_check_workspace_boundary(boundary_args(root=str(self.workspace), task=self.task_rel))

        self.assertEqual(payload["status"], "ok")
        self.assertTrue(gtt.runtime_workspace_path(self.workspace, gtt.DEFAULTS, "060-workspace-boundary-guard").is_file())
        self.assertTrue(gtt.runtime_task_path(self.workspace, gtt.DEFAULTS, "060-workspace-boundary-guard").is_file())

    def test_check_workspace_boundary_blocks_worktree_mode_without_task_context(self) -> None:
        self.source_task_dir.mkdir(parents=True)
        (self.source_task_dir / "task.json").write_text('{"title":"Wrong task copy"}\n', encoding="utf-8")
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.cmd_check_workspace_boundary(boundary_args(root=str(self.source), task=self.task_rel))
        payload = raised.exception.payload
        self.assertEqual(payload["status"], "blocked")
        self.assertTrue(any("task-start-context.json" in error for error in payload["errors"]))

    def test_check_workspace_boundary_blocks_wrong_cwd(self) -> None:
        self.source_task_dir.mkdir(parents=True)
        (self.source_task_dir / "task.json").write_text('{"title":"Wrong task copy"}\n', encoding="utf-8")
        gtt.write_json(self.source_task_dir / "task-start-context.json", self.task_context)
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.cmd_check_workspace_boundary(boundary_args(root=str(self.source), task=self.task_rel))
        payload = raised.exception.payload
        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["expected_workspace"], str(self.workspace.resolve()))
        self.assertTrue(any("workspace boundary mismatch" in error for error in payload["errors"]))

    def test_artifact_recorder_blocks_source_checkout_with_same_task_artifact(self) -> None:
        self.source_task_dir.mkdir(parents=True)
        (self.source_task_dir / "task.json").write_text('{"title":"Wrong task copy"}\n', encoding="utf-8")
        gtt.write_json(self.source_task_dir / "task-start-context.json", self.task_context)
        (self.source_task_dir / "review.md").write_text("# Review\n\n误写。\n", encoding="utf-8")
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.cmd_check_planning_approval(planning_args(root=str(self.source), task=self.task_rel))
        payload = raised.exception.payload
        self.assertEqual(payload["status"], "blocked")
        self.assertTrue(any("source checkout contains current-task artifacts" in error for error in payload["errors"]))

    def test_wrong_task_artifact_arguments_are_rejected(self) -> None:
        self.source_task_dir.mkdir(parents=True)
        for name, content in [("prd.md", "# PRD\n"), ("review.md", "# Review\n"), ("agent-assignment.json", "{}\n")]:
            (self.source_task_dir / name).write_text(content, encoding="utf-8")
        (self.source_task_dir / "reviews").mkdir()
        (self.source_task_dir / "reviews/round-001.md").write_text("# Round\n", encoding="utf-8")
        with self.assertRaises(gtt.WorkflowError):
            gtt.load_review_report(self.workspace, self.task_dir, str(self.source_task_dir / "review.md"))
        with self.assertRaises(gtt.WorkflowError):
            gtt.validate_agent_assignment(self.workspace, self.task_dir, str(self.source_task_dir / "agent-assignment.json"))
        with self.assertRaises(gtt.WorkflowError):
            gtt.load_review_round_report(self.workspace, self.task_dir, str(self.source_task_dir / "reviews/round-001.md"))
        with self.assertRaises(gtt.WorkflowError):
            gtt.build_phase2_check_payload(root=self.workspace, task_dir=self.task_dir, task_context=self.task_context, task={"base_branch": "main"}, checker="trellis-check", check_summary="检查完成。", checked_artifacts=[str(self.source_task_dir / "prd.md")], checked_specs=[], coverage_items=list(gtt.REQUIRED_PHASE2_COVERAGE), validation_items=["unit|passed"], findings=[])


class PlanningAndPhase2GateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.task_dir = self.root / ".trellis/tasks/07-04-gates"
        self.task_dir.mkdir(parents=True)
        (self.root / ".trellis/guru-team").mkdir(parents=True)
        (self.root / ".git").mkdir()
        (self.task_dir / "task.json").write_text(
            '{"title":"Gate task","base_branch":"main"}\n',
            encoding="utf-8",
        )
        gtt.write_json(self.task_dir / "finish-summary-index.json", {
            "schema_version": 1,
            "index": {
                "problem": "固定 journal 路径会让并行任务产生冲突。",
                "outcome": "完成摘要改为 task-local artifact；非目标：不实现搜索。",
                "changed_behavior": ["finish-work 完成后写入 finish-summary.json。"],
                "affected_surfaces": [{
                    "kind": "workflow",
                    "name": "finish-work",
                    "paths": ["trellis/workflows/guru-team/workflow.md"],
                    "change": "finish-work 不再调用 add_session.py。",
                }],
                "contract_changes": [],
                "search_terms": {
                    "commands": ["add_session.py"],
                    "config_keys": ["session_auto_commit"],
                    "schema_fields": ["finish-summary.json:index"],
                    "symbols": ["cmd_finish_work"],
                    "phrases": ["固定 journal 冲突", "add_session.py", "完成摘要改为 task-local artifact"],
                },
            },
        })
        (self.task_dir / "prd.md").write_text("# PRD\n\n需求。\n", encoding="utf-8")
        (self.task_dir / "design.md").write_text("# Design\n\n设计。\n", encoding="utf-8")
        (self.task_dir / "implement.md").write_text("# Implement\n\n计划。\n", encoding="utf-8")
        (self.root / ".trellis/spec").mkdir(parents=True)
        (self.root / ".trellis/spec/index.md").write_text("# Spec\n\n规则。\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def patch_common(self) -> list[mock._patch]:
        return [
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_start_context", return_value={
                "base_branch": "main",
                "workspace_mode": "worktree",
                "workspace_path": str(self.root),
                "task_dir": ".trellis/tasks/07-04-gates",
                "preflight": {"current_checkout": str(self.root)},
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_status_paths", return_value=[]),
        ]

    def write_normative_prd_hit(self, term: str) -> None:
        (self.task_dir / "prd.md").write_text(
            f"# PRD\n\n这里{term}固定合同。\n",
            encoding="utf-8",
        )

    def normative_hit_arg(self, term: str, classification: str, reason: str = "AI 已分类该命中。") -> str:
        return f"prd.md|3|{term}|{classification}|{reason}"

    def test_check_planning_approval_rejects_missing_artifact(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("Planning approval artifact not found", str(raised.exception))

    def test_planning_ambiguity_v2_terms_are_scanned(self) -> None:
        expected_terms = [
            "可以",
            "允许",
            "建议",
            "推荐",
            "可选",
            "尽量",
            "尽可能",
            "最好",
            "应该",
            "应当",
            "原则上",
            "一般",
            "通常",
            "视情况",
            "根据情况",
            "根据需要",
            "按需",
            "必要时",
            "如有需要",
            "需要时",
            "适当",
            "适当时",
            "合理",
            "合理时",
            "类似",
            "相关",
            "相应",
            "等",
            "等等",
            "之类",
            "一些",
            "若干",
            "部分",
            "至少",
            "默认",
        ]
        self.assertEqual(gtt.PLANNING_AMBIGUITY_CONTROLLED_TERMS, expected_terms)
        self.assertEqual(gtt.PLANNING_AMBIGUITY_SCAN_SCOPE, ["prd.md", "design.md", "implement.md"])

        for term in expected_terms:
            with self.subTest(term=term):
                self.write_normative_prd_hit(term)
                hits = gtt.scan_planning_normative_language(self.root, self.task_dir)
                self.assertIn(term, {str(hit["term"]) for hit in hits})

    def test_record_and_check_planning_approval(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_record_planning_approval(planning_args())
            check = gtt.cmd_check_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue((self.task_dir / "planning-approval.json").exists())
        self.assertEqual(payload["schema_version"], gtt.PLANNING_APPROVAL_SCHEMA_VERSION)
        self.assertTrue(payload["review_prompt_presented_at"])
        self.assertTrue(payload["approved_at"])
        self.assertEqual(payload["user_confirmation"]["source"], gtt.PLANNING_APPROVAL_CONFIRMATION_SOURCE)
        self.assertEqual(payload["head"], "abc123")
        self.assertEqual(check["status"], "ok")
        self.assertEqual(payload["ambiguity_review"]["status"], gtt.PLANNING_AMBIGUITY_STATUS_PASSED)
        self.assertEqual(payload["ambiguity_review"]["reviewer"], "codex-main-session")
        self.assertEqual(
            payload["ambiguity_review"]["normative_language"]["controlled_terms"],
            gtt.PLANNING_AMBIGUITY_CONTROLLED_TERMS,
        )
        self.assertEqual(
            payload["ambiguity_review"]["normative_language"]["scan_scope"],
            gtt.PLANNING_AMBIGUITY_SCAN_SCOPE,
        )
        self.assertEqual(payload["ambiguity_review"]["normative_language"]["hits"], [])
        self.assertEqual(payload["ambiguity_review"]["normative_language"]["unchecked_normative_hits"], [])
        self.assertEqual(
            set(payload["ambiguity_review"]["checked_dimensions"]),
            set(gtt.PLANNING_AMBIGUITY_REQUIRED_DIMENSIONS),
        )
        self.assertTrue(all(payload["ambiguity_review"]["checked_dimensions"].values()))
        self.assertEqual(len(payload["reviewed_artifacts"]), 3)
        self.assertEqual(len(payload["approved_artifacts"]), 3)

    def test_record_planning_approval_blocks_unclassified_normative_hits(self) -> None:
        for term in ["推荐", "可选", "至少", "默认"]:
            with self.subTest(term=term):
                self.write_normative_prd_hit(term)
                planning_artifact = self.task_dir / "planning-approval.json"
                if planning_artifact.exists():
                    planning_artifact.unlink()
                patches = self.patch_common()
                for patcher in patches:
                    patcher.start()
                try:
                    with self.assertRaises(gtt.WorkflowError) as raised:
                        gtt.cmd_record_planning_approval(planning_args())
                finally:
                    for patcher in reversed(patches):
                        patcher.stop()

                self.assertEqual(raised.exception.exit_code, 2)
                normative = raised.exception.payload["normative_language"]
                self.assertTrue(any(hit["term"] == term for hit in normative["hits"]))
                self.assertTrue(any(hit["term"] == term for hit in normative["unchecked_normative_hits"]))
                self.assertFalse(planning_artifact.exists())

    def test_record_planning_approval_accepts_allowed_normative_classifications(self) -> None:
        cases = [
            ("推荐", "quoted_source_non_contract"),
            ("默认", "term_definition"),
            ("可选", "literal_identifier"),
            ("相关", "historical_record_non_contract"),
            ("至少", "deterministic_threshold"),
            ("默认", "deterministic_default"),
            ("可选", "deterministic_option"),
            ("相关", "deterministic_reference"),
        ]
        for term, classification in cases:
            with self.subTest(classification=classification):
                self.write_normative_prd_hit(term)
                patches = self.patch_common()
                for patcher in patches:
                    patcher.start()
                try:
                    payload = gtt.cmd_record_planning_approval(
                        planning_args(normative_hit=[self.normative_hit_arg(term, classification)])
                    )
                    check = gtt.cmd_check_planning_approval(planning_args())
                finally:
                    for patcher in reversed(patches):
                        patcher.stop()

                normative = payload["ambiguity_review"]["normative_language"]
                self.assertEqual(check["status"], "ok")
                self.assertEqual(normative["unchecked_normative_hits"], [])
                self.assertEqual(normative["hits"][0]["classification"], classification)
                self.assertEqual(normative["hits"][0]["reason"], "AI 已分类该命中。")

    def test_record_planning_approval_blocks_contract_violation_classifications(self) -> None:
        for term in ["至少", "默认", "可选", "相关"]:
            with self.subTest(term=term):
                self.write_normative_prd_hit(term)
                planning_artifact = self.task_dir / "planning-approval.json"
                if planning_artifact.exists():
                    planning_artifact.unlink()
                patches = self.patch_common()
                for patcher in patches:
                    patcher.start()
                try:
                    with self.assertRaises(gtt.WorkflowError) as raised:
                        gtt.cmd_record_planning_approval(
                            planning_args(
                                normative_hit=[
                                    self.normative_hit_arg(
                                        term,
                                        "contract_violation",
                                        "缺少 issue #93 要求的确定性信息。",
                                    )
                                ]
                            )
                        )
                finally:
                    for patcher in reversed(patches):
                        patcher.stop()

                normative = raised.exception.payload["normative_language"]
                self.assertTrue(
                    any(
                        hit["term"] == term and hit["classification"] == "contract_violation"
                        for hit in normative["unchecked_normative_hits"]
                    )
                )
                self.assertFalse(planning_artifact.exists())

    def test_check_planning_approval_rejects_normative_scan_mismatch(self) -> None:
        self.write_normative_prd_hit("推荐")
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_record_planning_approval(
                planning_args(normative_hit=[self.normative_hit_arg("推荐", "term_definition")])
            )
            payload["ambiguity_review"]["normative_language"]["hits"][0]["text"] = "artifact 手工篡改。"
            payload.pop("artifact_path", None)
            payload.pop("dry_run", None)
            (self.task_dir / "planning-approval.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(any("扫描结果不一致" in error for error in raised.exception.payload["errors"]))

    def test_record_planning_approval_requires_ambiguity_summary(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_record_planning_approval(planning_args(ambiguity_summary=""))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("--ambiguity-summary", str(raised.exception))

    def test_record_planning_approval_rejects_non_passed_ambiguity_status(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_record_planning_approval(planning_args(ambiguity_status="failed"))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("--ambiguity-status", str(raised.exception))

    def test_check_planning_approval_rejects_missing_ambiguity_review(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_record_planning_approval(planning_args())
            payload.pop("ambiguity_review")
            payload.pop("artifact_path", None)
            payload.pop("dry_run", None)
            (self.task_dir / "planning-approval.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(any("ambiguity_review" in error for error in raised.exception.payload["errors"]))

    def test_check_planning_approval_rejects_schema_1_1_without_ambiguity_review(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_record_planning_approval(planning_args())
            payload["schema_version"] = "1.1"
            payload.pop("ambiguity_review")
            payload.pop("artifact_path", None)
            payload.pop("dry_run", None)
            (self.task_dir / "planning-approval.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        errors = raised.exception.payload["errors"]
        self.assertTrue(any("schema_version" in error for error in errors))
        self.assertTrue(any("ambiguity_review" in error for error in errors))

    def test_check_planning_approval_rejects_incomplete_ambiguity_review(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_record_planning_approval(planning_args())
            review = payload["ambiguity_review"]
            review["status"] = "failed"
            review["reviewer"] = ""
            review["summary"] = ""
            review["normative_language"]["controlled_terms"] = ["可以"]
            review["normative_language"]["unchecked_normative_hits"] = ["design.md:12 建议"]
            review["checked_dimensions"].pop("acceptance_criteria_are_deterministic")
            payload.pop("artifact_path", None)
            payload.pop("dry_run", None)
            (self.task_dir / "planning-approval.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        errors = raised.exception.payload["errors"]
        self.assertTrue(any("ambiguity_review.status" in error for error in errors))
        self.assertTrue(any("缺少 reviewer" in error for error in errors))
        self.assertTrue(any("缺少 summary" in error for error in errors))
        self.assertTrue(any("controlled_terms" in error for error in errors))
        self.assertTrue(any("unchecked_normative_hits" in error for error in errors))
        self.assertTrue(any("acceptance_criteria_are_deterministic" in error for error in errors))

    def test_validate_planning_approval_accepts_archived_task_with_active_artifact_paths(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        archived_task_dir = self.root / ".trellis/tasks/archive/2026-07/07-04-gates"
        archived_task_dir.mkdir(parents=True)
        for name in ["task.json", "prd.md", "design.md", "implement.md", "planning-approval.json"]:
            (archived_task_dir / name).write_bytes((self.task_dir / name).read_bytes())
        for name in ["prd.md", "design.md", "implement.md"]:
            (self.task_dir / name).unlink()

        with (
            mock.patch.object(gtt, "current_head", return_value="def456"),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
        ):
            _path, _payload, errors = gtt.validate_planning_approval(
                self.root,
                archived_task_dir,
                allow_committed_head=True,
            )

        self.assertEqual(errors, [])

    def test_record_planning_approval_requires_reviewer(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_record_planning_approval(planning_args(reviewer=""))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("--reviewer", str(raised.exception))

    def test_record_planning_approval_rejects_workflow_confirmation_source(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_record_planning_approval(planning_args(confirmation_source="workflow"))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn(gtt.PLANNING_APPROVAL_CONFIRMATION_SOURCE, str(raised.exception))

    def test_record_planning_approval_requires_all_three_planning_docs(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_record_planning_approval(planning_args(artifact=["prd.md"]))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("design.md", str(raised.exception))
        self.assertIn("implement.md", str(raised.exception))

    def test_check_planning_approval_rejects_legacy_workflow_source(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_record_planning_approval(planning_args())
            payload["schema_version"] = "1.0"
            payload["user_confirmation"]["source"] = "workflow"
            payload.pop("review_prompt_presented_at")
            payload.pop("approved_at")
            payload.pop("reviewed_artifacts")
            payload.pop("artifact_path", None)
            payload.pop("dry_run", None)
            (self.task_dir / "planning-approval.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        errors = raised.exception.payload["errors"]
        self.assertTrue(any("schema_version" in error for error in errors))
        self.assertTrue(any("user_confirmation.source" in error for error in errors))
        self.assertTrue(any("reviewed_artifacts" in error for error in errors))

    def test_check_planning_approval_rejects_phase0_handoff_source(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_record_planning_approval(planning_args())
            payload["user_confirmation"]["source"] = "phase0-handoff"
            payload.pop("artifact_path", None)
            payload.pop("dry_run", None)
            (self.task_dir / "planning-approval.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(any("Phase 0 handoff" in error for error in raised.exception.payload["errors"]))

    def test_check_planning_approval_rejects_missing_required_doc_entry(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_record_planning_approval(planning_args())
            payload["reviewed_artifacts"] = [
                item for item in payload["reviewed_artifacts"] if not str(item["path"]).endswith("/design.md")
            ]
            payload["approved_artifacts"] = [
                item for item in payload["approved_artifacts"] if not str(item["path"]).endswith("/design.md")
            ]
            payload.pop("artifact_path", None)
            payload.pop("dry_run", None)
            (self.task_dir / "planning-approval.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(any("design.md" in error for error in raised.exception.payload["errors"]))

    def test_check_planning_approval_rejects_missing_digest_metadata(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_record_planning_approval(planning_args())
            payload["reviewed_artifacts"][0].pop("sha256")
            payload.pop("artifact_path", None)
            payload.pop("dry_run", None)
            (self.task_dir / "planning-approval.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(any("缺少 sha256" in error for error in raised.exception.payload["errors"]))

    def test_check_planning_approval_rejects_changed_artifact(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            (self.task_dir / "prd.md").write_text("# PRD\n\n需求变更。\n", encoding="utf-8")
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(any("已过期" in error for error in raised.exception.payload["errors"]))

    def test_check_planning_approval_allows_modified_at_drift_when_content_matches(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            prd = self.task_dir / "prd.md"
            new_mtime = prd.stat().st_mtime + 10
            os.utime(prd, (new_mtime, new_mtime))
            check = gtt.cmd_check_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(check["status"], "ok")

    def test_check_planning_approval_allows_head_drift_when_artifacts_match(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        with mock.patch.object(gtt, "current_head", return_value="def456"):
            _path, _payload, errors = gtt.validate_planning_approval(self.root, self.task_dir)

        self.assertEqual(errors, [])

    def test_check_planning_approval_allows_dirty_path_drift_when_artifacts_match(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        with (
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_status_paths", return_value=["new-dirty-file.txt"]),
        ):
            _path, _payload, errors = gtt.validate_planning_approval(self.root, self.task_dir)

        self.assertEqual(errors, [])

    def test_check_planning_approval_allows_non_metadata_dirty_after_head_drift_when_artifacts_match(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        with (
            mock.patch.object(gtt, "current_head", return_value="def456"),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(gtt, "git_status_paths", return_value=["new-dirty-file.txt"]),
        ):
            _path, _payload, errors = gtt.validate_planning_approval(
                self.root,
                self.task_dir,
                allow_committed_head=True,
            )

        self.assertEqual(errors, [])

    def test_check_planning_approval_allows_metadata_dirty_after_committed_head(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        with (
            mock.patch.object(gtt, "current_head", return_value="def456"),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(
                gtt,
                "git_status_paths",
                return_value=[
                    ".trellis/tasks/07-04-review-gate/task-start-context.json",
                    ".trellis/tasks/07-04-gates/review.md",
                ],
            ),
        ):
            _path, _payload, errors = gtt.validate_planning_approval(
                self.root,
                self.task_dir,
                allow_committed_head=True,
            )

        self.assertEqual(errors, [])

    def test_record_phase2_check_requires_full_coverage_on_pass(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_record_phase2_check(phase2_args(coverage=["requirements"]))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("missing_coverage", raised.exception.payload)

    def test_record_and_check_phase2_check(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            payload = gtt.cmd_record_phase2_check(
                phase2_args(checked_spec=[".trellis/spec/index.md"])
            )
            check = gtt.cmd_check_phase2_check(phase2_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue((self.task_dir / "phase2-check.json").exists())
        self.assertEqual(payload["head"], "abc123")
        self.assertEqual(check["status"], "ok")
        self.assertTrue(all(payload["coverage"].values()))

    def test_phase2_pass_rejects_unclosed_agent_assignment_recovery_chain(self) -> None:
        assignment = self.task_dir / "agent-assignment.json"
        unclosed_assignment = {
            "schema_version": "1.1",
            "task": ".trellis/tasks/07-04-gates",
            "head": "abc123",
            "agents": [
                {
                    "logical_role": "实现代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "Implement A",
                    "assigned_at": "2026-07-07T00:00:00Z",
                    "assigned_head": "abc123",
                    "reason": "分配实现代理。",
                }
            ],
            "liveness": {},
            "review_rounds": [],
            "reuse_decisions": [],
            "status_events": [
                {
                    "event_id": "evt-0001",
                    "event": "terminated-unfinished",
                    "agent_id": "agent-a",
                    "logical_role": "实现代理",
                    "platform_nickname": "Implement A",
                    "observed_at": "2026-07-07T00:01:00Z",
                    "recorded_at": "2026-07-07T00:01:00Z",
                    "head": "abc123",
                    "source": "main-session",
                    "evidence": "实现代理被平台中断且未完成。",
                    "predecessor_agent_id": "",
                    "predecessor_event_id": "",
                    "termination_reason": "manual_or_platform_terminated_unfinished",
                    "termination_source_event_id": "",
                    "replacement_reason": "",
                    "handoff_summary": "predecessor output、当前 diff、剩余工作和 gate blockers。",
                }
            ],
        }
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        git_object_patch = mock.patch.object(gtt, "git_object_exists", return_value=True)
        git_object_patch.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            assignment.write_text(json.dumps(unclosed_assignment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(gtt.WorkflowError) as record_raised:
                gtt.cmd_record_phase2_check(phase2_args())
            assignment.unlink()
            gtt.cmd_record_phase2_check(phase2_args())
            assignment.write_text(json.dumps(unclosed_assignment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(gtt.WorkflowError) as check_raised:
                gtt.cmd_check_phase2_check(phase2_args())
        finally:
            git_object_patch.stop()
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(any("terminated-unfinished" in error for error in record_raised.exception.payload["errors"]))
        self.assertTrue(any("terminated-unfinished" in error for error in check_raised.exception.payload["errors"]))

    def test_check_phase2_ignores_recorded_task_artifact_dirty_paths(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            gtt.cmd_record_phase2_check(phase2_args())
            with mock.patch.object(
                gtt,
                "git_status_paths",
                return_value=[
                    ".trellis/tasks/07-04-gates/prd.md",
                    ".trellis/tasks/07-04-gates/planning-approval.json",
                    ".trellis/tasks/07-04-gates/phase2-check.json",
                ],
            ):
                check = gtt.cmd_check_phase2_check(phase2_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(check["status"], "ok")

    def test_record_phase2_check_requires_checker(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_record_phase2_check(phase2_args(checker=""))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("--checker", str(raised.exception))

    def test_record_phase2_check_rejects_checked_spec_outside_spec_dir(self) -> None:
        outside = self.root / "README.md"
        outside.write_text("# README\n", encoding="utf-8")
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_record_phase2_check(phase2_args(checked_spec=["README.md"]))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn(".trellis/spec", str(raised.exception))

    def test_check_phase2_rejects_unresolved_blocking_finding(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            gtt.cmd_record_phase2_check(
                phase2_args(
                    pass_check=False,
                    finding=["P2|需要修复|trellis/workflows/guru-team/workflow.md"],
                )
            )
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_phase2_check(phase2_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(any("P0/P1/P2" in error for error in raised.exception.payload["errors"]))

    def test_check_phase2_rejects_dirty_state_drift(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            gtt.cmd_record_phase2_check(phase2_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_status_paths", return_value=["trellis/workflows/guru-team/workflow.md"]):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_check_phase2_check(phase2_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(any("dirty_paths" in error for error in raised.exception.payload["errors"]))

    def test_validate_phase2_allows_post_commit_task_metadata_only(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            gtt.cmd_record_phase2_check(phase2_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        with (
            mock.patch.object(gtt, "current_head", return_value="def456"),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(gtt, "committed_paths_match_phase2_dirty_paths", return_value=(True, [])),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "git_status_paths", return_value=[".trellis/tasks/07-04-gates/review.md"]),
        ):
            _path, _payload, errors = gtt.validate_phase2_check(self.root, self.task_dir, allow_committed_head=True)

        self.assertEqual(errors, [])

    def test_validate_phase2_allows_post_commit_agent_assignment_metadata_update(self) -> None:
        assignment = self.task_dir / "agent-assignment.json"
        assignment.write_text(
            gtt.json.dumps(
                {
                    "schema_version": "1.0",
                    "task": ".trellis/tasks/07-04-gates",
                    "head": "abc123",
                    "agents": [],
                    "review_rounds": [],
                    "reuse_decisions": [],
                    "status_events": [],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            gtt.cmd_record_phase2_check(phase2_args(checked_artifact=["agent-assignment.json"]))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        assignment.write_text(
            gtt.json.dumps(
                {
                    "schema_version": "1.0",
                    "task": ".trellis/tasks/07-04-gates",
                    "head": "def456",
                    "agents": [
                        {
                            "logical_role": "最终放行审查代理",
                            "agent_id": "agent-1",
                            "platform_nickname": "Pasteur",
                            "assigned_at": "2026-07-05T00:00:00Z",
                            "assigned_head": "def456",
                            "reason": "提交后记录最终放行审查代理。",
                        }
                    ],
                    "review_rounds": [],
                    "reuse_decisions": [],
                    "status_events": [],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        with (
            mock.patch.object(gtt, "current_head", return_value="def456"),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(gtt, "committed_paths_match_phase2_dirty_paths", return_value=(True, [])),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "git_status_paths", return_value=[".trellis/tasks/07-04-gates/agent-assignment.json"]),
        ):
            _path, _payload, errors = gtt.validate_phase2_check(self.root, self.task_dir, allow_committed_head=True)

        self.assertEqual(errors, [])

    def test_validate_phase2_allows_post_commit_review_gate_metadata_updates(self) -> None:
        review_report = self.task_dir / "review.md"
        raw_report = self.task_dir / "reviews" / "round-001-final-release.md"
        raw_report.parent.mkdir(parents=True, exist_ok=True)
        review_report.write_text("# Review\n\n旧 final review evidence。\n", encoding="utf-8")
        raw_report.write_text("# Raw Review\n\n旧 raw final review evidence。\n", encoding="utf-8")
        ledger = self.task_dir / "issue-scope-ledger.json"
        ledger.write_text(
            gtt.json.dumps(
                {
                    "primary_issue": None,
                    "close_issues": [],
                    "related_issues": [],
                    "followup_issues": [],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            gtt.cmd_record_phase2_check(
                phase2_args(checked_artifact=["review.md", "reviews/round-001-final-release.md", "issue-scope-ledger.json"])
            )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        review_report.write_text("# Review\n\n新的 fresh final review evidence。\n", encoding="utf-8")
        raw_report.write_text("# Raw Review\n\n新的 fresh raw final review evidence。\n", encoding="utf-8")
        ledger.write_text(
            gtt.json.dumps(
                {
                    "primary_issue": None,
                    "close_issues": [
                        {
                            "number": 44,
                            "url": "https://github.com/castbox/guru-trellis/issues/44",
                            "title": "收紧 Branch Review Gate",
                            "acceptance_evidence": ["Branch Review Gate 已覆盖 Issue #44。"],
                        }
                    ],
                    "related_issues": [],
                    "followup_issues": [],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        with (
            mock.patch.object(gtt, "current_head", return_value="def456"),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(gtt, "committed_paths_match_phase2_dirty_paths", return_value=(True, [])),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(
                gtt,
                "git_status_paths",
                return_value=[
                    ".trellis/tasks/07-04-gates/review.md",
                    ".trellis/tasks/07-04-gates/reviews/round-001-final-release.md",
                    ".trellis/tasks/07-04-gates/issue-scope-ledger.json",
                ],
            ),
        ):
            _path, _payload, errors = gtt.validate_phase2_check(self.root, self.task_dir, allow_committed_head=True)

        self.assertEqual(errors, [])

    def test_validate_phase2_allows_post_commit_paths_recorded_as_dirty(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            with mock.patch.object(
                gtt,
                "git_status_paths",
                return_value=["trellis/workflows/guru-team/workflow.md"],
            ):
                gtt.cmd_record_phase2_check(phase2_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        diff_result = subprocess.CompletedProcess(
            ["git", "diff", "--name-only", "abc123..HEAD"],
            0,
            stdout="trellis/workflows/guru-team/workflow.md\n",
            stderr="",
        )
        with (
            mock.patch.object(gtt, "current_head", return_value="def456"),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(gtt, "run", return_value=diff_result),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "git_status_paths", return_value=[]),
        ):
            _path, _payload, errors = gtt.validate_phase2_check(self.root, self.task_dir, allow_committed_head=True)

        self.assertEqual(errors, [])

    def test_validate_phase2_rejects_post_commit_paths_outside_recorded_dirty_paths(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            gtt.cmd_record_phase2_check(phase2_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        with (
            mock.patch.object(gtt, "current_head", return_value="def456"),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(
                gtt,
                "committed_paths_match_phase2_dirty_paths",
                return_value=(False, ["trellis/workflows/guru-team/workflow.md"]),
            ),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "git_status_paths", return_value=[]),
        ):
            _path, _payload, errors = gtt.validate_phase2_check(self.root, self.task_dir, allow_committed_head=True)

        self.assertTrue(any("dirty_paths" in error for error in errors))
        self.assertFalse(any("working tree 不一致" in error for error in errors))

    def test_validate_phase2_rejects_post_commit_non_metadata_dirty_state(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
            gtt.cmd_record_phase2_check(phase2_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        with (
            mock.patch.object(gtt, "current_head", return_value="def456"),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(gtt, "committed_paths_match_phase2_dirty_paths", return_value=(True, [])),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(True, ["trellis/workflows/guru-team/workflow.md"])),
            mock.patch.object(gtt, "git_status_paths", return_value=["trellis/workflows/guru-team/workflow.md"]),
        ):
            _path, _payload, errors = gtt.validate_phase2_check(self.root, self.task_dir, allow_committed_head=True)

        self.assertTrue(any("非 Trellis metadata" in error for error in errors))

    def test_committed_paths_match_phase2_dirty_paths_uses_direct_range(self) -> None:
        diff_result = subprocess.CompletedProcess(
            ["git", "diff", "--name-only", "abc123..HEAD"],
            0,
            stdout="trellis/workflows/guru-team/workflow.md\n.trellis/tasks/07-04-gates/review.md\n",
            stderr="",
        )
        with mock.patch.object(gtt, "run", return_value=diff_result) as run:
            matches, uncovered = gtt.committed_paths_match_phase2_dirty_paths(
                self.root,
                "abc123",
                ["trellis/workflows/guru-team/workflow.md"],
            )

        self.assertTrue(matches)
        self.assertEqual(uncovered, [])
        run.assert_called_once_with(["git", "diff", "--name-only", "abc123..HEAD"], cwd=self.root, check=False)

    def test_committed_paths_match_phase2_dirty_paths_reports_uncovered_paths(self) -> None:
        diff_result = subprocess.CompletedProcess(
            ["git", "diff", "--name-only", "abc123..HEAD"],
            0,
            stdout="trellis/workflows/guru-team/workflow.md\n",
            stderr="",
        )
        with mock.patch.object(gtt, "run", return_value=diff_result):
            matches, uncovered = gtt.committed_paths_match_phase2_dirty_paths(self.root, "abc123", [])

        self.assertFalse(matches)
        self.assertEqual(uncovered, ["trellis/workflows/guru-team/workflow.md"])

    def test_committed_paths_match_phase2_dirty_paths_allows_recorded_directory(self) -> None:
        diff_result = subprocess.CompletedProcess(
            ["git", "diff", "--name-only", "abc123..HEAD"],
            0,
            stdout="docs/newdir/file.md\n",
            stderr="",
        )
        with mock.patch.object(gtt, "run", return_value=diff_result):
            matches, uncovered = gtt.committed_paths_match_phase2_dirty_paths(self.root, "abc123", ["docs/"])

        self.assertTrue(matches)
        self.assertEqual(uncovered, [])


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

    def test_planning_ambiguity_constants_match_dogfood_helper(self) -> None:
        dogfood = self.load_dogfood_module()
        for name in [
            "PLANNING_AMBIGUITY_CONTROLLED_TERMS",
            "PLANNING_AMBIGUITY_SCAN_SCOPE",
            "PLANNING_AMBIGUITY_CLASSIFICATIONS",
            "PLANNING_AMBIGUITY_BLOCKING_CLASSIFICATIONS",
        ]:
            with self.subTest(name=name):
                self.assertEqual(getattr(dogfood, name), getattr(gtt, name))


class PublishBoundaryTest(unittest.TestCase):
    PENDING_REMOTE_MARKETPLACE_EVIDENCE = {
        "type": "remote_marketplace_verification",
        "status": "pending",
        "required": True,
        "artifact_path": "marketplace-verification.json",
        "reason": "push 后由 deterministic marketplace verifier 生成真实 evidence；pending 不满足最终 publish。",
    }

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
            '{"title":"Publish boundary","base_branch":"main"}\n',
            encoding="utf-8",
        )
        gtt.write_json(self.task_dir / "finish-summary-index.json", {
            "schema_version": 1,
            "index": {
                "problem": "固定 journal 路径会让并行任务产生冲突。",
                "outcome": "完成摘要改为 task-local artifact；非目标：不实现搜索。",
                "changed_behavior": ["finish-work 完成后写入 finish-summary.json。"],
                "affected_surfaces": [{
                    "kind": "workflow", "name": "finish-work",
                    "paths": ["trellis/workflows/guru-team/workflow.md"],
                    "change": "finish-work 不再调用 add_session.py。",
                }],
                "contract_changes": [],
                "search_terms": {
                    "commands": ["add_session.py"],
                    "config_keys": ["session_auto_commit"],
                    "schema_fields": ["finish-summary.json:index"],
                    "symbols": ["cmd_finish_work"],
                    "phrases": ["固定 journal 冲突", "add_session.py", "完成摘要改为 task-local artifact"],
                },
            },
        })
        gtt.write_json(self.task_dir / "issue-scope-ledger.json", {
            "close_issues": [{
                "number": 18,
                "title": "Publish boundary",
                "acceptance_evidence": ["ok", dict(self.PENDING_REMOTE_MARKETPLACE_EVIDENCE)],
            }],
            "related_issues": [],
            "followup_issues": [],
        })
        self.body_path = self.task_dir / "pr-body.md"
        self.body_path.write_text(valid_pr_body("不可变 publish readiness fixture。"), encoding="utf-8")
        self.readiness_path = self.task_dir / "pr-readiness.json"
        gtt.write_json(self.readiness_path, {"ready": True, "body_file": "pr-body.md"})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def patch_publish_success_path(self) -> list[mock._patch]:
        gate = {
            "head": "abc123",
            "diff_range": "origin/main...HEAD",
            "changed_files": ["trellis/workflows/guru-team/workflow.md"],
            "conclusion": {"passed": True, "summary": "发布边界检查通过。"},
            "issue_scope": {
                "close_issues_reviewed": [{"number": 18, "title": "Publish boundary"}],
            },
            "verification_evidence": {
                "reviewer": "test",
                "evidence": ["已覆盖 publish 边界。"],
            },
            "deployment_impact": {
                "needs_deployment_impact_review": False,
                "deployment_asset_categories": {},
                "probable_runtime_changes_without_deployment_asset_change": [],
            },
        }
        return [
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={
                **gtt.DEFAULTS,
                "github_repo": "owner/repo",
            }),
            mock.patch.object(gtt, "load_task_start_context", return_value={
                "base_branch": "main",
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "assert_workspace_boundary"),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", gate, [])),
            mock.patch.object(gtt, "current_branch", return_value="codex/18-publish-boundary"),
            mock.patch.object(
                gtt,
                "read_pr_readiness_publish_inputs",
                side_effect=self.fake_readiness_publish_inputs,
            ),
            mock.patch.object(gtt, "validate_publish_identity_and_remote_head", return_value={
                "repo": "owner/repo",
                "base_branch": "main",
                "head_branch": "codex/18-publish-boundary",
                "head": "a" * 40,
                "remote_head": "a" * 40,
            }),
        ]

    def fake_readiness_publish_inputs(
        self,
        root: Path,
        task_dir: Path,
        artifact_arg: str | None,
        gate: dict[str, object],
        *,
        require_committed: bool,
    ) -> tuple[Path, dict[str, object], str]:
        del require_committed
        artifact_path = Path(artifact_arg) if artifact_arg else self.readiness_path
        if not artifact_path.is_absolute():
            artifact_path = root / artifact_path
        body, _source = gtt.load_pr_body_artifact(root, str(artifact_path))
        assert body is not None
        return artifact_path, {
            "repo": "owner/repo",
            "base_branch": "main",
            "head_branch": "codex/18-publish-boundary",
            "reviewed_head_sha": str(gate.get("head") or "abc123"),
            "title": "完成：#18 Publish boundary",
            "body_source": "pr-body.md",
            "body_sha256": "a" * 64,
            "draft": False,
            "reviewed_source": "body-artifact:pr-readiness.json",
        }, body

    def create_committed_readiness_fixture(self, root: Path) -> tuple[Path, Path, dict[str, object]]:
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
        (root / "README.md").write_text("fixture\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
        reviewed_head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=True
        ).stdout.strip()

        task_dir = root / ".trellis/tasks/archive/2026-07/task"
        task_dir.mkdir(parents=True)
        (task_dir / "pr-body.md").write_text(valid_pr_body("不可变快照 mutation fixture。"), encoding="utf-8")
        readiness_path, artifact = gtt.write_pr_readiness_snapshot(
            root,
            task_dir,
            repo="owner/repo",
            base_branch="main",
            head_branch="topic",
            reviewed_head_sha=reviewed_head,
            title="完成：#18 不可变发布输入",
            draft=False,
        )
        subprocess.run(["git", "add", ".trellis/tasks"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "metadata"], cwd=root, check=True)
        return task_dir, readiness_path, {"head": reviewed_head}

    def test_pr_readiness_mutations_fail_closed_before_publish_resolution(self) -> None:
        mutations = {
            "title": lambda payload: payload["publish_inputs"].__setitem__("title", "changed"),
            "draft": lambda payload: payload["publish_inputs"].__setitem__("draft", True),
            "repo": lambda payload: payload["publish_inputs"].__setitem__("repo", "other/repo"),
            "base": lambda payload: payload["publish_inputs"].__setitem__("base_branch", "release"),
            "head": lambda payload: payload["publish_inputs"].__setitem__("head_branch", "other"),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                task_dir, readiness_path, gate = self.create_committed_readiness_fixture(root)
                payload = gtt.read_json(readiness_path)
                mutate(payload)
                payload["publish_inputs_sha256"] = gtt.canonical_json_sha256(payload["publish_inputs"])
                gtt.write_json(readiness_path, payload)

                with (
                    mock.patch.object(gtt, "resolve_open_pull_request_for_recovery") as resolve_pr,
                    self.assertRaises(gtt.WorkflowError) as raised,
                ):
                    gtt.read_pr_readiness_publish_inputs(
                        root, task_dir, str(readiness_path), gate, require_committed=True
                    )
                resolve_pr.assert_not_called()
                self.assertIn("dirty/staged", str(raised.exception))

    def test_pr_readiness_body_head_source_and_digest_mutations_fail_closed(self) -> None:
        cases = ["body", "reviewed_head", "reviewed_source", "snapshot_digest"]
        for name in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                task_dir, readiness_path, gate = self.create_committed_readiness_fixture(root)
                payload = gtt.read_json(readiness_path)
                if name == "body":
                    (task_dir / "pr-body.md").write_text("changed body\n", encoding="utf-8")
                elif name == "reviewed_head":
                    payload["publish_inputs"]["reviewed_head_sha"] = "f" * 40
                    payload["publish_inputs_sha256"] = gtt.canonical_json_sha256(payload["publish_inputs"])
                    gtt.write_json(readiness_path, payload)
                elif name == "reviewed_source":
                    payload["publish_inputs"]["reviewed_source"] = "body-file:pr-body.md"
                    payload["publish_inputs_sha256"] = gtt.canonical_json_sha256(payload["publish_inputs"])
                    gtt.write_json(readiness_path, payload)
                else:
                    payload["publish_inputs_sha256"] = "0" * 64
                    gtt.write_json(readiness_path, payload)

                with (
                    mock.patch.object(gtt, "resolve_open_pull_request_for_recovery") as resolve_pr,
                    self.assertRaises(gtt.WorkflowError),
                ):
                    gtt.read_pr_readiness_publish_inputs(
                        root, task_dir, str(readiness_path), gate, require_committed=True
                    )
                resolve_pr.assert_not_called()

    def test_pr_readiness_rejects_committed_rewrite_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir, readiness_path, gate = self.create_committed_readiness_fixture(root)
            payload = gtt.read_json(readiness_path)
            payload["publish_inputs"]["title"] = "changed after initial metadata commit"
            payload["publish_inputs_sha256"] = gtt.canonical_json_sha256(payload["publish_inputs"])
            gtt.write_json(readiness_path, payload)
            subprocess.run(["git", "add", str(readiness_path)], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "rewrite metadata"], cwd=root, check=True)

            with (
                mock.patch.object(gtt, "resolve_open_pull_request_for_recovery") as resolve_pr,
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.read_pr_readiness_publish_inputs(
                    root, task_dir, str(readiness_path), gate, require_committed=True
                )
            resolve_pr.assert_not_called()
            self.assertIn("immutable after its initial metadata commit", str(raised.exception))

    def record_passed_marketplace_evidence(
        self,
        _root: Path,
        _task_dir: Path,
        ledger: dict[str, Any],
        _verification_path: Path,
        verification: dict[str, Any],
    ) -> Path:
        passed = {
            "type": "remote_marketplace_verification",
            "status": "passed",
            "required": True,
            "artifact_path": ".trellis/tasks/07-04-publish-boundary/marketplace-verification.json",
            "artifact_sha256": "f" * 64,
            "verified_content_head": verification["verified_head"],
            "remote_head": verification["remote_head"],
            "publish_head": verification["verified_head"],
            "commands_passed": True,
        }
        for issue in ledger["close_issues"]:
            issue["acceptance_evidence"] = [
                item for item in issue["acceptance_evidence"]
                if not (isinstance(item, dict) and item.get("type") == "remote_marketplace_verification")
            ] + [dict(passed)]
        gtt.write_json(self.task_dir / "issue-scope-ledger.json", ledger)
        return self.task_dir / "issue-scope-ledger.json"

    def test_publish_pr_direct_call_is_blocked_before_repo_or_push(self) -> None:
        with (
            mock.patch.object(gtt, "repo_root") as repo_root,
            mock.patch.object(gtt, "run_stdout") as run_stdout,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_publish_pr(publish_args())

        repo_root.assert_not_called()
        run_stdout.assert_not_called()
        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("trellis-finish-work", str(raised.exception))
        self.assertEqual(raised.exception.payload["required_entrypoint"], "trellis-finish-work")

    def test_publish_pr_checks_workspace_boundary_before_review_gate(self) -> None:
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "load_task_start_context", return_value={
                "base_branch": "main",
                "task_artifact_dir": ".trellis/tasks/07-04-publish-boundary",
            }),
            mock.patch.object(gtt, "assert_workspace_boundary", side_effect=gtt.WorkflowError("wrong workspace", exit_code=2)) as boundary,
            mock.patch.object(gtt, "validate_review_gate") as gate,
        ):
            with self.assertRaises(gtt.WorkflowError):
                gtt.cmd_publish_pr(publish_args(recovery_after_finish_work=True))

        boundary.assert_called_once()
        gate.assert_not_called()

    def test_publish_pr_recovery_dry_run_reports_generated_body_is_not_reviewed_source(self) -> None:
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_publish_pr(
                publish_args(
                    recovery_after_finish_work=True,
                    validation=["python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py 通过"],
                )
            )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(payload["status"], "dry-run")
        self.assertEqual(payload["repo"], "owner/repo")
        self.assertEqual(payload["base_branch"], "main")
        self.assertEqual(payload["head_branch"], "codex/18-publish-boundary")
        self.assertEqual(payload["body_source"], "generated")
        self.assertTrue(payload["reviewed_source_required"])
        self.assertFalse(payload["reviewed_source_ok"])
        self.assertIn("generated PR body is preview-only", payload["reviewed_source_errors"][0])
        self.assertFalse(payload["merge_commit"]["ready"])
        self.assertEqual(
            payload["merge_commit"]["subject"],
            "chore(merge): #<pull_request> 合并 #18 完成 Publish boundary",
        )
        self.assertIn("PR: #<pull_request>", payload["merge_commit"]["body"])
        self.assertIn("Refs #18", payload["merge_commit"]["body"])
        self.assertEqual(payload["merge_commit"]["command"][0:4], ["gh", "pr", "merge", "<pull_request>"])

    def test_publish_pr_formal_payload_uses_created_pr_number_in_merge_commit(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("publish 正式路径输出 merge commit 指令。"), encoding="utf-8")
        verification = {
            "status": "passed",
            "verified_head": "a" * 40,
            "remote_head": "a" * 40,
            "steps": [{"passed": True}],
        }
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(gtt, "current_head", side_effect=["a" * 40, "b" * 40, "b" * 40]),
                mock.patch.object(
                    gtt, "execute_marketplace_verification", return_value=verification
                ) as execute_verifier,
                mock.patch.object(gtt, "write_remote_marketplace_evidence", side_effect=self.record_passed_marketplace_evidence),
                mock.patch.object(gtt, "commit_marketplace_verification_metadata", return_value={"committed": True}),
                mock.patch.object(
                    gtt,
                    "validate_marketplace_verification",
                    return_value=(self.task_dir / "marketplace-verification.json", verification, []),
                ),
                mock.patch.object(gtt, "update_finish_summary_for_pr", return_value=(self.task_dir / "finish-summary.json", {})) as update_summary,
                mock.patch.object(gtt, "commit_and_push_finish_summary_metadata", return_value={"committed": True, "commit": "c" * 40}) as commit_summary,
                mock.patch.object(gtt, "run") as run,
            ):
                run.return_value = mock.Mock(
                    returncode=0,
                    stdout="https://github.com/owner/repo/pull/91\n",
                    stderr="",
                )
                payload = gtt.cmd_publish_pr(
                    publish_args(
                        from_finish_work=True,
                        recovery_after_finish_work=False,
                        dry_run=False,
                        body_file=str(body_path),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(payload["pr_url"], "https://github.com/owner/repo/pull/91")
        self.assertTrue(payload["merge_commit"]["ready"])
        self.assertEqual(
            payload["merge_commit"]["subject"],
            "chore(merge): #91 合并 #18 完成 Publish boundary",
        )
        self.assertIn("PR: #91", payload["merge_commit"]["body"])
        self.assertIn("Refs #18", payload["merge_commit"]["body"])
        self.assertIn("--subject", payload["merge_commit"]["command"])
        self.assertEqual(payload["marketplace_verification"]["status"], "passed")
        self.assertNotIn("pr_recovery", payload)
        execute_verifier.assert_called_once()
        update_summary.assert_called_once()
        commit_summary.assert_called_once()

    def test_publish_pr_recovery_reuses_passed_verifier_after_summary_commit_failure(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("PR 已存在时复用 verifier evidence 完成 recovery。"), encoding="utf-8")
        verification = {
            "status": "passed",
            "verified_head": "a" * 40,
            "remote_head": "a" * 40,
            "steps": [{"passed": True}],
        }
        summary_path = self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT

        def run_command(command: list[str], **_kwargs: object) -> mock.Mock:
            if command[:3] == ["gh", "pr", "create"]:
                return mock.Mock(
                    returncode=0,
                    stdout="https://github.com/owner/repo/pull/91\n",
                    stderr="",
                )
            if command[:3] == ["gh", "pr", "list"]:
                return mock.Mock(
                    returncode=0,
                    stdout=json.dumps([{
                        "number": 91,
                        "url": "https://github.com/owner/repo/pull/91",
                        "headRefName": "codex/18-publish-boundary",
                        "baseRefName": "main",
                    }]),
                    stderr="",
                )
            return mock.Mock(returncode=0, stdout="", stderr="")

        def rewrite_summary(*_args: object, **_kwargs: object) -> tuple[Path, dict[str, object]]:
            summary_path.write_text('{"pr_url":"https://github.com/owner/repo/pull/91"}\n', encoding="utf-8")
            return summary_path, {"pr_url": "https://github.com/owner/repo/pull/91"}

        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(gtt, "current_head", side_effect=["a" * 40, "b" * 40, "b" * 40]),
                mock.patch.object(
                    gtt, "execute_marketplace_verification", return_value=verification
                ) as execute_verifier,
                mock.patch.object(
                    gtt,
                    "write_remote_marketplace_evidence",
                    side_effect=self.record_passed_marketplace_evidence,
                ),
                mock.patch.object(
                    gtt, "commit_marketplace_verification_metadata", return_value={"committed": True}
                ),
                mock.patch.object(
                    gtt,
                    "validate_marketplace_verification",
                    return_value=(self.task_dir / "marketplace-verification.json", verification, []),
                ) as validate_verifier,
                mock.patch.object(gtt, "update_finish_summary_for_pr", side_effect=rewrite_summary),
                mock.patch.object(
                    gtt,
                    "commit_and_push_finish_summary_metadata",
                    side_effect=[
                        gtt.WorkflowError("commit failed", exit_code=2),
                        {"committed": True, "commit": "c" * 40},
                    ],
                ) as commit_summary,
                mock.patch.object(gtt, "run", side_effect=run_command),
            ):
                with self.assertRaises(gtt.WorkflowError) as first_attempt:
                    gtt.cmd_publish_pr(
                        publish_args(
                            from_finish_work=True,
                            recovery_after_finish_work=False,
                            dry_run=False,
                            body_file=str(body_path),
                        )
                    )
                self.assertEqual(
                    first_attempt.exception.payload["failed_stage"],
                    "finish-summary-metadata-commit-push",
                )
                self.assertTrue(summary_path.is_file())

                recovered = gtt.cmd_publish_pr(
                    publish_args(
                        recovery_after_finish_work=True,
                        dry_run=False,
                        body_file=str(body_path),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(execute_verifier.call_count, 1)
        self.assertEqual(validate_verifier.call_count, 2)
        self.assertEqual(commit_summary.call_count, 2)
        self.assertTrue(recovered["marketplace_verification_reused"])
        self.assertTrue(recovered["pr_recovery"]["reused_existing_open_pr"])
        self.assertEqual(recovered["pr_url"], "https://github.com/owner/repo/pull/91")

    def test_publish_pr_recovery_rejects_tampered_or_stale_verifier_evidence(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("Recovery 必须拒绝 stale verifier evidence。"), encoding="utf-8")
        verification = {
            "status": "passed",
            "verified_head": "a" * 40,
            "remote_head": "a" * 40,
            "steps": [{"passed": True}],
        }
        self.record_passed_marketplace_evidence(
            self.root,
            self.task_dir,
            gtt.read_json(self.task_dir / "issue-scope-ledger.json"),
            self.task_dir / "marketplace-verification.json",
            verification,
        )
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(gtt, "current_head", return_value="b" * 40),
                mock.patch.object(gtt, "execute_marketplace_verification") as execute_verifier,
                mock.patch.object(
                    gtt,
                    "validate_marketplace_verification",
                    return_value=(
                        self.task_dir / "marketplace-verification.json",
                        verification,
                        ["marketplace verification is stale or tampered"],
                    ),
                ),
                mock.patch.object(gtt, "run") as run,
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_publish_pr(
                    publish_args(
                        recovery_after_finish_work=True,
                        dry_run=False,
                        body_file=str(body_path),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        execute_verifier.assert_not_called()
        run.assert_not_called()
        self.assertTrue(any("stale or tampered" in error for error in raised.exception.payload["errors"]))
        self.assertEqual(raised.exception.payload["failed_stage"], "recovery-marketplace-evidence")
        self.assertEqual(raised.exception.payload["publish_inputs"]["repo"], "owner/repo")
        self.assertIn("--recovery-after-finish-work", raised.exception.payload["recovery_command"])
        recovery_command = raised.exception.payload["recovery_command"]
        self.assertIn("--body-artifact", recovery_command)
        self.assertNotIn("--body-file", recovery_command)
        self.assertNotIn("--title", recovery_command)
        self.assertNotIn("--draft", recovery_command)
        self.assertNotIn("--no-draft", recovery_command)
        self.assertNotIn("--base-branch", recovery_command)
        self.assertNotIn("--validation", recovery_command)

    def test_publish_recovery_rejects_cli_overrides_before_pr_query(self) -> None:
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "resolve_open_pull_request_for_recovery") as resolve_pr,
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_publish_pr(publish_args(
                    recovery_after_finish_work=True,
                    dry_run=False,
                    body_artifact=str(self.readiness_path),
                    title="changed",
                ))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        resolve_pr.assert_not_called()
        self.assertIn("forbids title/body/draft/base/validation overrides", str(raised.exception))

    def test_publish_pr_recovery_push_failure_preserves_inputs_before_pr_query(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("Recovery push 失败保留发布输入。"), encoding="utf-8")
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "marketplace_verification_required", return_value=False),
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout", side_effect=gtt.WorkflowError("push failed")),
                mock.patch.object(gtt, "resolve_open_pull_request_for_recovery") as resolve_pr,
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_publish_pr(publish_args(
                    recovery_after_finish_work=True,
                    dry_run=False,
                    body_file=str(body_path),
                ))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        resolve_pr.assert_not_called()
        self.assertEqual(raised.exception.payload["failed_stage"], "recovery-content-push")
        self.assertEqual(raised.exception.payload["publish_inputs"]["body_source"], "pr-body.md")
        self.assertNotIn("body", raised.exception.payload["publish_inputs"])
        self.assertIn("--recovery-after-finish-work", raised.exception.payload["recovery_command"])

    def test_publish_pr_recovery_identity_failure_preserves_inputs_before_pr_query(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("Recovery identity 失败保留发布输入。"), encoding="utf-8")
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "marketplace_verification_required", return_value=False),
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(
                    gtt,
                    "validate_publish_identity_and_remote_head",
                    side_effect=gtt.WorkflowError("identity failed", payload={"errors": ["head mismatch"]}),
                ),
                mock.patch.object(gtt, "resolve_open_pull_request_for_recovery") as resolve_pr,
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_publish_pr(publish_args(
                    recovery_after_finish_work=True,
                    dry_run=False,
                    body_file=str(body_path),
                ))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        resolve_pr.assert_not_called()
        self.assertEqual(raised.exception.payload["failed_stage"], "recovery-publish-identity")
        self.assertEqual(raised.exception.payload["errors"], ["head mismatch"])
        self.assertEqual(raised.exception.payload["publish_inputs"]["head_branch"], "codex/18-publish-boundary")
        self.assertIn("--recovery-after-finish-work", raised.exception.payload["recovery_command"])

    def test_publish_pr_verifier_failure_blocks_before_gh_pr_create(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("marketplace verifier 失败必须阻断 PR。"), encoding="utf-8")
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(gtt, "current_head", return_value="abc123"),
                mock.patch.object(gtt, "execute_marketplace_verification", side_effect=gtt.WorkflowError("verify failed", exit_code=2)),
                mock.patch.object(gtt, "run") as run,
                self.assertRaises(gtt.WorkflowError),
            ):
                gtt.cmd_publish_pr(publish_args(
                    from_finish_work=True,
                    recovery_after_finish_work=False,
                    dry_run=False,
                    body_file=str(body_path),
                ))
        finally:
            for patcher in reversed(patches):
                patcher.stop()
        run.assert_not_called()

    def test_validate_marketplace_verification_rejects_stale_non_metadata_tail(self) -> None:
        artifact = self.task_dir / "marketplace-verification.json"
        gtt.write_json(artifact, {
            "schema_version": "1.0", "generated_at": "2026-07-10T00:00:00Z",
            "status": "passed", "repo": "owner/repo", "remote": "origin",
            "branch": "codex/18-publish-boundary", "marketplace_source": "gh:owner/repo/trellis#codex/18-publish-boundary",
            "verified_head": "abc123", "remote_head": "abc123",
            "task_dir": ".trellis/tasks/07-04-publish-boundary",
            "steps": [{"passed": True}] * 7,
            "assets": {"workflow_sha256": "a", "preview_sha256": "b", "task_start_context_schema_sha256": "c", "runtime_gitignore_present": True},
        })
        with mock.patch.object(gtt, "run") as run:
            run.side_effect = [
                mock.Mock(returncode=0, stdout="src/app.py\n", stderr=""),
                mock.Mock(returncode=0, stdout="def456\trefs/heads/codex/18-publish-boundary\n", stderr=""),
            ]
            _path, _payload, errors = gtt.validate_marketplace_verification(
                self.root, self.task_dir, "def456", "owner/repo", "origin", "codex/18-publish-boundary"
            )
        self.assertTrue(any("stale" in error for error in errors))

    def test_validate_marketplace_verification_rejects_tampered_identity(self) -> None:
        artifact = self.task_dir / "marketplace-verification.json"
        gtt.write_json(artifact, {
            "schema_version": "1.0", "generated_at": "2026-07-10T00:00:00Z",
            "status": "passed", "repo": "attacker/repo", "remote": "upstream",
            "branch": "wrong-branch", "marketplace_source": "gh:attacker/repo/trellis#wrong-branch",
            "verified_head": "a" * 40, "remote_head": "a" * 40,
            "task_dir": ".trellis/tasks/wrong-task",
            "steps": [{"passed": True}] * 7,
            "assets": {"workflow_sha256": "a", "preview_sha256": "b", "task_start_context_schema_sha256": "c", "runtime_gitignore_present": True},
        })
        with (
            mock.patch.object(gtt, "run", return_value=mock.Mock(returncode=0, stdout=f"{'a' * 40}\trefs/heads/codex/18-publish-boundary\n", stderr="")),
        ):
            _path, _payload, errors = gtt.validate_marketplace_verification(
                self.root, self.task_dir, "a" * 40, "owner/repo", "origin", "codex/18-publish-boundary"
            )
        self.assertTrue(any("repo does not match" in error for error in errors))
        self.assertTrue(any("remote/branch identity" in error for error in errors))
        self.assertTrue(any("task_dir" in error for error in errors))

    def test_publish_pr_non_draft_rejects_generated_body_before_push(self) -> None:
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(
                    gtt,
                    "read_pr_readiness_publish_inputs",
                    side_effect=gtt.WorkflowError("immutable pr-readiness.json is required", exit_code=2),
                ),
                mock.patch.object(gtt, "require_gh_auth") as require_auth,
                mock.patch.object(gtt, "run_stdout") as run_stdout,
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_publish_pr(
                    publish_args(
                        recovery_after_finish_work=True,
                        dry_run=False,
                        validation=["python3 -m unittest 通过"],
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        require_auth.assert_not_called()
        run_stdout.assert_not_called()
        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("pr-readiness.json", str(raised.exception))

    def test_publish_pr_draft_allows_generated_body_preview(self) -> None:
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_publish_pr(
                publish_args(
                    recovery_after_finish_work=True,
                    draft=True,
                    validation=["python3 -m unittest 通过"],
                )
            )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(payload["body_source"], "generated")
        self.assertFalse(payload["reviewed_source_required"])
        self.assertTrue(payload["reviewed_source_ok"])
        self.assertEqual(payload["reviewed_source_errors"], [])

    def test_publish_pr_rejects_generated_body_without_validation(self) -> None:
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_publish_pr(publish_args(recovery_after_finish_work=True))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertEqual(raised.exception.payload["body_source"], "generated")
        self.assertTrue(any("publish validation" in error for error in raised.exception.payload["errors"]))

    def test_publish_pr_rejects_low_information_body_file(self) -> None:
        body_path = self.root / "pr-body.md"
        body_path.write_text(
            """## 变更摘要

- 本 PR 承接当前 Trellis task 的已提交实现与文档更新。

## 影响范围

- workflow

## 验证结果

- python3 -m unittest 通过

## Review Gate

- Reviewed HEAD：`abc123`

## Issue 关闭范围

- Closes #18

## 安全说明

- 未涉及 secrets。
""",
            encoding="utf-8",
        )
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_publish_pr(
                    publish_args(
                        recovery_after_finish_work=True,
                        body_file=str(body_path),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("低信息量" in error for error in raised.exception.payload["errors"]))

    def test_publish_pr_rejects_missing_docs_ssot_section(self) -> None:
        body_path = self.root / "pr-body.md"
        body_path.write_text(
            valid_pr_body("验证缺失 Docs SSOT section 会被阻断。").replace(
                """## Docs SSOT

- 策略：ssot_first。
- durable docs：已更新 `trellis/workflows/guru-team/workflow.md`。
- task delta merge：任务 artifact delta 已 merge 到 durable docs。
- task history：调试过程仅保留为 task history。
- follow-up / limitation：无 follow-up 或当前 PR limitation。

""",
                "",
            ),
            encoding="utf-8",
        )
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_publish_pr(
                    publish_args(
                        recovery_after_finish_work=True,
                        body_file=str(body_path),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("Docs SSOT" in error for error in raised.exception.payload["errors"]))

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

    def test_publish_pr_prefers_reviewed_body_file(self) -> None:
        body_path = self.root / "pr-body.md"
        body_path.write_text(
            """## 📋 变更摘要

- 增加 publish-pr 的 body file 读取路径，并在发布前校验 reviewer 可读性。

## 🔍 影响范围

- Guru Team publish helper
- finish-work PR 发布入口

## ✅ 验证结果

- python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py 通过

## Review Gate

- 结论：发布边界检查通过。
- Reviewed HEAD：`abc123`

## 文档同步

- 策略：ssot_first。
- durable docs：已更新 workflow 文档。
- task delta merge：task delta 已 merge。
- task history：无仅保留任务历史内容。
- follow-up / limitation：无后续限制。

## 🔗 Issue 关闭范围

- Closes #18

## 🔒 安全说明

- 未涉及 secrets、runtime config 或部署资产。
""",
            encoding="utf-8",
        )
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_publish_pr(
                publish_args(
                    recovery_after_finish_work=True,
                    body_file=str(body_path),
                    validation=["fallback validation should not replace body file"],
                )
            )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(payload["status"], "dry-run")
        self.assertIn("body-file:", payload["body_source"])
        self.assertIn("增加 publish-pr 的 body file 读取路径", payload["body"])
        self.assertNotIn("fallback validation should not replace body file", payload["body"])

    def test_publish_pr_rejects_close_keyword_for_related_issue(self) -> None:
        ledger_path = self.task_dir / "issue-scope-ledger.json"
        gtt.write_json(ledger_path, {
            "close_issues": [{
                "number": 18,
                "title": "Publish boundary",
                "acceptance_evidence": ["ok", dict(self.PENDING_REMOTE_MARKETPLACE_EVIDENCE)],
            }],
            "related_issues": [{"number": 19, "title": "Related only"}],
            "followup_issues": [],
        })
        body_path = self.root / "pr-body.md"
        body_path.write_text(
            """## 变更摘要

- 增加 publish-pr 的 close/ref 语义校验，避免误关闭 related issue。

## 影响范围

- Guru Team publish helper

## 验证结果

- python3 -m unittest 通过

## Review Gate

- 结论：发布边界检查通过。

## Docs SSOT

- strategy：ssot_first。
- durable docs：已更新 workflow 文档。
- task delta merge：task delta 已 merge。
- task history：无仅保留任务历史内容。
- follow-up / limitation：无。

## Issue 关闭范围

- Closes #19

## 安全说明

- 未涉及 secrets。
""",
            encoding="utf-8",
        )
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_publish_pr(
                    publish_args(
                        recovery_after_finish_work=True,
                        body_file=str(body_path),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(any("#19" in error for error in raised.exception.payload["errors"]))

    def test_publish_pr_uses_body_artifact(self) -> None:
        body_path = self.root / "artifact-body.md"
        body_path.write_text(
            """## 变更摘要

- 从 readiness artifact 读取 AI 审阅后的 PR body。

## 影响范围

- Guru Team publish helper

## 验证结果

- python3 -m unittest 通过

## Review Gate

- 结论：发布边界检查通过。

## Docs SSOT

- strategy：ssot_first。
- durable docs：已更新 workflow 文档。
- task delta merge：task delta 已 merge。
- task history：无仅保留任务历史内容。
- follow-up / limitation：无。

## Issue 关闭范围

- Closes #18

## 安全说明

- 未涉及 secrets。
""",
            encoding="utf-8",
        )
        artifact_path = self.root / "body-artifact.json"
        artifact_path.write_text(
            gtt.json.dumps({"ready": True, "body_file": str(body_path)}, ensure_ascii=False),
            encoding="utf-8",
        )
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_publish_pr(
                publish_args(
                    recovery_after_finish_work=True,
                    body_artifact=str(artifact_path),
                )
            )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertIn("body-artifact:", payload["body_source"])
        self.assertIn("readiness artifact", payload["body"])

    def test_publish_pr_resolves_relative_body_file_from_artifact_directory(self) -> None:
        artifact_dir = self.root / "artifacts"
        artifact_dir.mkdir()
        body_path = artifact_dir / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("从 artifact 所在目录解析相对 body_file。"), encoding="utf-8")
        artifact_path = artifact_dir / "pr-readiness.json"
        artifact_path.write_text(
            gtt.json.dumps({"ready": True, "body_file": "reviewed-pr-body.md"}, ensure_ascii=False),
            encoding="utf-8",
        )
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_publish_pr(
                publish_args(
                    recovery_after_finish_work=True,
                    body_artifact=str(artifact_path),
                )
            )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertIn("body-artifact:", payload["body_source"])
        self.assertIn("artifact 所在目录解析", payload["body"])

    def test_publish_pr_rejects_body_artifact_without_ready_true(self) -> None:
        artifact_path = self.root / "body-artifact.json"
        artifact_path.write_text(
            gtt.json.dumps({"body": valid_pr_body("缺少 ready true 的 artifact 不可发布。")}, ensure_ascii=False),
            encoding="utf-8",
        )
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_publish_pr(
                    publish_args(
                        recovery_after_finish_work=True,
                        body_artifact=str(artifact_path),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("ready=true", str(raised.exception))

    def test_rewrite_active_task_artifact_path_to_archived_task(self) -> None:
        active_path = self.task_dir / "pr-readiness.json"
        archived_task_dir = self.root / ".trellis/tasks/archive/2026-07/07-04-publish-boundary"

        rewritten = gtt.rewrite_active_task_artifact_path(
            self.root,
            self.task_dir,
            archived_task_dir,
            str(active_path),
        )

        self.assertEqual(rewritten, str(archived_task_dir / "pr-readiness.json"))

    def test_rewrite_active_task_artifact_path_keeps_external_path(self) -> None:
        external_path = self.root / "pr-readiness.json"
        archived_task_dir = self.root / ".trellis/tasks/archive/2026-07/07-04-publish-boundary"

        rewritten = gtt.rewrite_active_task_artifact_path(
            self.root,
            self.task_dir,
            archived_task_dir,
            str(external_path),
        )

        self.assertEqual(rewritten, str(external_path))

    def test_publish_pr_prefers_body_file_over_artifact_when_both_are_set(self) -> None:
        body_path = self.root / "preferred-body.md"
        body_path.write_text(
            """## 变更摘要

- 优先使用命令行传入的 reviewed body file。

## 影响范围

- Guru Team publish helper

## 验证结果

- python3 -m unittest 通过

## Review Gate

- 结论：发布边界检查通过。

## Docs SSOT

- strategy：ssot_first。
- durable docs：已更新 workflow 文档。
- task delta merge：task delta 已 merge。
- task history：无仅保留任务历史内容。
- follow-up / limitation：无。

## Issue 关闭范围

- Closes #18

## 安全说明

- 未涉及 secrets。
""",
            encoding="utf-8",
        )
        artifact_path = self.root / "body-artifact.json"
        artifact_path.write_text(
            gtt.json.dumps(
                {
                    "ready": True,
                    "body": """## 变更摘要

- artifact body 不应覆盖显式 body file。

## 影响范围

- Guru Team publish helper

## 验证结果

- python3 -m unittest 通过

## Review Gate

- 结论：发布边界检查通过。

## Docs SSOT

- strategy：ssot_first。
- durable docs：已更新 workflow 文档。
- task delta merge：task delta 已 merge。
- task history：无仅保留任务历史内容。
- follow-up / limitation：无。

## Issue 关闭范围

- Closes #18

## 安全说明

- 未涉及 secrets。
""",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_publish_pr(
                publish_args(
                    recovery_after_finish_work=True,
                    body_file=str(body_path),
                    body_artifact=str(artifact_path),
                )
            )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertIn("body-file:", payload["body_source"])
        self.assertIn("优先使用命令行传入的 reviewed body file", payload["body"])
        self.assertNotIn("artifact body 不应覆盖显式 body file", payload["body"])

    def test_finish_work_direct_call_requires_explicit_finish_work_entrypoint(self) -> None:
        with (
            mock.patch.object(gtt, "repo_root") as repo_root,
            mock.patch.object(gtt, "run") as run,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_finish_work(finish_args(from_trellis_finish_work=False))

        repo_root.assert_not_called()
        run_commands = [call.args[0] for call in run.call_args_list]
        self.assertNotIn(["python3", "./.trellis/scripts/task.py", "archive", self.task_dir.name], run_commands)
        self.assertFalse(any(command[:3] == ["python3", "./.trellis/scripts/add_session.py", "--title"] for command in run_commands))
        self.assertEqual(raised.exception.exit_code, 2)
        self.assertEqual(raised.exception.payload["blocked_step"], "finish-work")
        self.assertEqual(raised.exception.payload["required_entrypoint"], "trellis-finish-work")
        self.assertEqual(raised.exception.payload["intent_flag"], "--from-trellis-finish-work")

    def test_finish_work_rejects_missing_reviewed_source_before_archive(self) -> None:
        gate = {
            "head": "a" * 40,
            "conclusion": {"passed": True, "summary": "finish-work 后发布。"},
            "changed_files": ["trellis/workflows/guru-team/workflow.md"],
            "issue_scope": {"close_issues_reviewed": [{"number": 18}]},
        }
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_start_context", return_value={
                "base_branch": "main",
                "workspace_mode": "worktree",
                "workspace_path": str(self.root),
                "task_dir": ".trellis/tasks/07-04-review-gate",
                "preflight": {"current_checkout": str(self.root)},
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "assert_workspace_boundary"),
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", gate, [])),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "run") as run,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.cmd_finish_work(finish_args(validation=["python3 -m unittest 通过"]))

        run_commands = [call.args[0] for call in run.call_args_list]
        self.assertNotIn(["python3", "./.trellis/scripts/task.py", "archive", self.task_dir.name], run_commands)
        self.assertFalse(any(command[:3] == ["python3", "./.trellis/scripts/add_session.py", "--title"] for command in run_commands))
        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("requires --body-file", str(raised.exception))
        self.assertNotIn("body_source", raised.exception.payload)

    def test_finish_work_calls_publish_with_internal_marker(self) -> None:
        body_path = self.task_dir / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("finish-work 传递 reviewed body file。"), encoding="utf-8")
        gate = {
            "head": "a" * 40,
            "generated_at": "2026-07-11T00:00:00Z",
            "conclusion": {"passed": True, "summary": "finish-work 后发布。"},
            "changed_files": ["trellis/workflows/guru-team/workflow.md"],
            "issue_scope": {"close_issues_reviewed": [{"number": 18}]},
        }
        archived_task_dir = self.root / ".trellis/tasks/archive/2026-07/07-04-publish-boundary"
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_start_context", return_value={
                "base_branch": "main",
                "task_artifact_dir": ".trellis/tasks/07-04-publish-boundary",
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "assert_workspace_boundary"),
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", gate, [])),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "recent_work_commits", return_value=["abc123"]),
            mock.patch.object(gtt, "run") as run,
            mock.patch.object(gtt, "commit_if_metadata_dirty", return_value=None),
            mock.patch.object(gtt, "resolve_existing_task_dir", return_value=archived_task_dir),
            mock.patch.object(gtt, "prepare_closeout", return_value={"plan": {"plan_digest": "a" * 64}}),
            mock.patch.object(gtt, "build_finish_summary", return_value={"schema_version": 1}) as build_summary,
            mock.patch.object(gtt, "validate_finish_summary") as validate_summary,
            mock.patch.object(gtt, "cmd_publish_pr", return_value={"status": "dry-run"}) as publish,
        ):
            run.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_finish_work(finish_args(body_file=str(self.body_path), dry_run=False))

        self.assertEqual(raised.exception.payload["failed_stage"], "plan-digest-handshake")
        publish.assert_not_called()
        build_summary.assert_not_called()
        validate_summary.assert_not_called()
        self.assertFalse(any(call.args[0][:3] == ["python3", "./.trellis/scripts/task.py", "archive"] for call in run.call_args_list))

    def test_finish_work_migrates_archived_review_gate_before_publish(self) -> None:
        body_path = self.task_dir / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("finish-work 归档后迁移 review gate。"), encoding="utf-8")
        gate = {
            "head": "a" * 40,
            "generated_at": "2026-07-11T00:00:00Z",
            "conclusion": {"passed": True, "summary": "finish-work 后发布。"},
            "changed_files": ["trellis/workflows/guru-team/workflow.md"],
            "issue_scope": {"close_issues_reviewed": [{"number": 18}]},
        }
        archived_task_dir = self.root / ".trellis/tasks/archive/2026-07/07-04-publish-boundary"
        archive_migration = {"migrated": True, "updates": ["verification_evidence.review_report"]}
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_start_context", return_value={"base_branch": "main"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", gate, [])),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "recent_work_commits", return_value=["abc123"]),
            mock.patch.object(gtt, "run") as run,
            mock.patch.object(gtt, "commit_if_metadata_dirty", side_effect=[
                {"committed": True, "commit": "archive"},
                {"committed": True, "commit": "migration"},
            ]) as commit_metadata,
            mock.patch.object(gtt, "resolve_existing_task_dir", return_value=archived_task_dir),
            mock.patch.object(gtt, "prepare_closeout", return_value={"plan": {"plan_digest": "a" * 64}}),
            mock.patch.object(gtt, "migrate_review_gate_for_archived_task", return_value=archive_migration) as migrate,
            mock.patch.object(gtt, "build_finish_summary", return_value={"schema_version": 1}),
            mock.patch.object(gtt, "validate_finish_summary"),
            mock.patch.object(gtt, "cmd_publish_pr", return_value={"status": "dry-run"}) as publish,
        ):
            run.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_finish_work(finish_args(body_file=str(self.body_path), dry_run=False))

        self.assertEqual(raised.exception.payload["failed_stage"], "plan-digest-handshake")
        migrate.assert_not_called()
        commit_metadata.assert_not_called()
        publish.assert_not_called()

    def test_finish_work_dry_run_returns_plan_without_archive_journal_commit_or_publish(self) -> None:
        body_path = self.task_dir / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("finish-work dry-run 只输出 readiness preview。"), encoding="utf-8")
        gate = {
            "head": "a" * 40,
            "generated_at": "2026-07-11T00:00:00Z",
            "conclusion": {"passed": True, "summary": "finish-work dry-run preview。"},
            "changed_files": ["trellis/workflows/guru-team/workflow.md"],
            "issue_scope": {"close_issues_reviewed": [{"number": 18}]},
        }
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_start_context", return_value={
                "base_branch": "main",
                "task_artifact_dir": ".trellis/tasks/07-04-publish-boundary",
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", gate, [])),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "recent_work_commits", return_value=["abc123"]),
            mock.patch.object(gtt, "current_branch", return_value="codex/27-finish-work-dry-run-readiness"),
            mock.patch.object(gtt, "validate_github_remote_repository", return_value="owner/repo"),
            mock.patch.object(gtt, "run") as run,
            mock.patch.object(gtt, "commit_if_metadata_dirty") as commit_metadata,
            mock.patch.object(gtt, "cmd_publish_pr") as publish,
        ):
            run.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            payload = gtt.cmd_finish_work(finish_args(body_file=str(self.body_path)))

        run_commands = [call.args[0] for call in run.call_args_list]
        self.assertNotIn(["python3", "./.trellis/scripts/task.py", "archive", self.task_dir.name], run_commands)
        self.assertFalse(any(command[:3] == ["python3", "./.trellis/scripts/add_session.py", "--title"] for command in run_commands))
        commit_metadata.assert_not_called()
        publish.assert_not_called()
        self.assertEqual(payload["status"], "dry-run")
        self.assertFalse(payload["dry_run_side_effects"])
        plan = payload["closeout_plan"]
        self.assertEqual(payload["closeout_plan_digest"], plan["plan_digest"])
        self.assertEqual(plan["task"]["id"], self.task_dir.name)
        self.assertEqual(plan["git"]["repo"], "owner/repo")
        self.assertEqual(plan["git"]["base_branch"], "main")
        self.assertEqual(plan["git"]["head_branch"], "codex/27-finish-work-dry-run-readiness")
        self.assertTrue(plan["publish"]["draft"])
        self.assertEqual(plan["transitions"], gtt.CLOSEOUT_TRANSITIONS)
        self.assertEqual(gtt.closeout_plan_errors(plan), [])

    def test_finish_work_validates_gate_with_metadata_tail_allowed(self) -> None:
        body_path = self.task_dir / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("finish-work 校验 gate metadata tail。"), encoding="utf-8")
        gate = {
            "head": "a" * 40,
            "generated_at": "2026-07-11T00:00:00Z",
            "conclusion": {"passed": True, "summary": "finish-work 后发布。"},
            "changed_files": ["trellis/workflows/guru-team/workflow.md"],
            "issue_scope": {"close_issues_reviewed": [{"number": 18}]},
        }
        archived_task_dir = self.root / ".trellis/tasks/archive/2026-07/07-04-publish-boundary"
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_start_context", return_value={
                "base_branch": "main",
                "task_artifact_dir": ".trellis/tasks/07-04-publish-boundary",
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", gate, [])) as validate_gate,
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "recent_work_commits", return_value=["abc123"]),
            mock.patch.object(gtt, "validate_github_remote_repository", return_value="owner/repo"),
            mock.patch.object(gtt, "run") as run,
            mock.patch.object(gtt, "commit_if_metadata_dirty", return_value=None),
            mock.patch.object(gtt, "resolve_existing_task_dir", return_value=archived_task_dir),
            mock.patch.object(gtt, "validate_finish_summary"),
            mock.patch.object(gtt, "cmd_publish_pr", return_value={"status": "dry-run"}),
        ):
            run.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            gtt.cmd_finish_work(finish_args(body_file=str(self.body_path), dry_run=True))

        self.assertTrue(validate_gate.call_args.args[3])

    def test_open_pull_request_recovery_resolver_returns_zero_or_one_and_rejects_multiple(self) -> None:
        branch = "codex/18-publish-boundary"
        one = [{
            "number": 91,
            "url": "https://github.com/owner/repo/pull/91",
            "headRefName": branch,
            "baseRefName": "main",
        }]
        for values, state in [([], "none"), (one, "one")]:
            with self.subTest(state=state), mock.patch.object(
                gtt,
                "run",
                return_value=mock.Mock(returncode=0, stdout=json.dumps(values), stderr=""),
            ) as run:
                resolved = gtt.resolve_open_pull_request_for_recovery(
                    self.root, "owner/repo", branch, "main"
                )
            self.assertEqual(resolved["state"], state)
            self.assertEqual(resolved["open_pr_count"], len(values))
            command = run.call_args.args[0]
            self.assertIn("--repo", command)
            self.assertIn("--head", command)
            self.assertIn("--base", command)

        multiple = one + [{
            "number": 92,
            "url": "https://github.com/owner/repo/pull/92",
            "headRefName": branch,
            "baseRefName": "main",
        }]
        with mock.patch.object(
            gtt,
            "run",
            return_value=mock.Mock(returncode=0, stdout=json.dumps(multiple), stderr=""),
        ), self.assertRaises(gtt.WorkflowError) as raised:
            gtt.resolve_open_pull_request_for_recovery(
                self.root, "owner/repo", branch, "main"
            )
        self.assertEqual(raised.exception.payload["open_pr_count"], 2)

    def test_open_pull_request_recovery_resolver_validates_head_base_and_canonical_repo_url(self) -> None:
        branch = "codex/18-publish-boundary"
        invalid_entries = [
            {
                "number": 91,
                "url": "https://github.com/owner/repo/pull/91",
                "headRefName": "other-branch",
                "baseRefName": "main",
            },
            {
                "number": 91,
                "url": "https://github.com/owner/repo/pull/91",
                "headRefName": branch,
                "baseRefName": "release",
            },
            {
                "number": 91,
                "url": "https://github.com/other/repo/pull/91",
                "headRefName": branch,
                "baseRefName": "main",
            },
        ]
        for entry in invalid_entries:
            with self.subTest(entry=entry), mock.patch.object(
                gtt,
                "run",
                return_value=mock.Mock(returncode=0, stdout=json.dumps([entry]), stderr=""),
            ), self.assertRaises(gtt.WorkflowError):
                gtt.resolve_open_pull_request_for_recovery(
                    self.root, "owner/repo", branch, "main"
                )

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

    def test_publish_pr_create_failure_returns_deterministic_recovery_command(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("PR 创建失败 recovery。"), encoding="utf-8")
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "marketplace_verification_required", return_value=False),
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(gtt, "current_head", return_value="a" * 40),
                mock.patch.object(gtt, "run", return_value=mock.Mock(returncode=1, stdout="", stderr="create failed")),
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_publish_pr(publish_args(
                    from_finish_work=True,
                    recovery_after_finish_work=False,
                    dry_run=False,
                    body_file=str(body_path),
                ))
        finally:
            for patcher in reversed(patches):
                patcher.stop()
        self.assertEqual(raised.exception.payload["failed_stage"], "gh-pr-create")
        self.assertEqual(raised.exception.payload["pr_url"], "")
        self.assertEqual(
            set(raised.exception.payload["publish_inputs"]),
            gtt.PR_READINESS_PUBLISH_INPUT_KEYS,
        )
        self.assertEqual(raised.exception.payload["publish_inputs"]["body_source"], "pr-body.md")
        self.assertEqual(
            raised.exception.payload["publish_inputs"]["reviewed_source"],
            "body-artifact:pr-readiness.json",
        )
        self.assertIn("--recovery-after-finish-work", raised.exception.payload["recovery_command"])

    def test_publish_pr_recovery_reuses_one_open_pr_without_create(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("Recovery 查询到一个 PR 时只复用。"), encoding="utf-8")
        existing = {
            "number": 91,
            "url": "https://github.com/owner/repo/pull/91",
            "headRefName": "codex/18-publish-boundary",
            "baseRefName": "main",
        }
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "marketplace_verification_required", return_value=False),
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(
                    gtt,
                    "resolve_open_pull_request_for_recovery",
                    return_value={"state": "one", "open_pr_count": 1, "pull_request": existing},
                ) as resolve_pr,
                mock.patch.object(gtt, "create_pull_request") as create_pr,
                mock.patch.object(
                    gtt,
                    "update_finish_summary_for_pr",
                    return_value=(self.task_dir / "finish-summary.json", {}),
                ),
                mock.patch.object(
                    gtt,
                    "commit_and_push_finish_summary_metadata",
                    return_value={"committed": True, "commit": "c" * 40},
                ),
            ):
                payload = gtt.cmd_publish_pr(publish_args(
                    recovery_after_finish_work=True,
                    dry_run=False,
                    body_file=str(body_path),
                ))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        resolve_pr.assert_called_once_with(
            self.root, "owner/repo", "codex/18-publish-boundary", "main"
        )
        create_pr.assert_not_called()
        self.assertTrue(payload["pr_recovery"]["reused_existing_open_pr"])
        self.assertFalse(payload["pr_recovery"]["created_after_zero_open_pr"])

    def test_publish_pr_recovery_zero_open_pr_creates_once_with_same_publish_inputs(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("Recovery 查询到零个 PR 时单次创建。"), encoding="utf-8")
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "marketplace_verification_required", return_value=False),
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(
                    gtt,
                    "resolve_open_pull_request_for_recovery",
                    return_value={"state": "none", "open_pr_count": 0, "pull_request": None},
                ) as resolve_pr,
                mock.patch.object(
                    gtt,
                    "create_pull_request",
                    return_value="https://github.com/owner/repo/pull/91",
                ) as create_pr,
                mock.patch.object(
                    gtt,
                    "update_finish_summary_for_pr",
                    return_value=(self.task_dir / "finish-summary.json", {}),
                ),
                mock.patch.object(
                    gtt,
                    "commit_and_push_finish_summary_metadata",
                    return_value={"committed": True, "commit": "c" * 40},
                ),
            ):
                payload = gtt.cmd_publish_pr(publish_args(
                    recovery_after_finish_work=True,
                    dry_run=False,
                    body_file=str(body_path),
                    title="完成：#18 Publish boundary",
                    draft=False,
                ))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        resolve_pr.assert_called_once()
        create_pr.assert_called_once()
        self.assertEqual(create_pr.call_args.args[1:5], (
            "owner/repo", "main", "codex/18-publish-boundary", "完成：#18 Publish boundary"
        ))
        self.assertEqual(create_pr.call_args.args[5], self.body_path.read_text(encoding="utf-8"))
        self.assertFalse(create_pr.call_args.args[6])
        self.assertFalse(payload["pr_recovery"]["reused_existing_open_pr"])
        self.assertTrue(payload["pr_recovery"]["created_after_zero_open_pr"])

    def test_publish_pr_recovery_multiple_open_prs_fails_closed_without_create(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("Recovery 查询到多个 PR 时阻塞。"), encoding="utf-8")
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "marketplace_verification_required", return_value=False),
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(
                    gtt,
                    "resolve_open_pull_request_for_recovery",
                    side_effect=gtt.WorkflowError(
                        "multiple open PRs",
                        exit_code=2,
                        payload={"open_pr_count": 2},
                    ),
                ),
                mock.patch.object(gtt, "create_pull_request") as create_pr,
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_publish_pr(publish_args(
                    recovery_after_finish_work=True,
                    dry_run=False,
                    body_file=str(body_path),
                ))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        create_pr.assert_not_called()
        self.assertEqual(raised.exception.payload["open_pr_count"], 2)
        self.assertEqual(raised.exception.payload["failed_stage"], "open-pr-query")
        self.assertIn("--recovery-after-finish-work", raised.exception.payload["recovery_command"])

    def test_publish_pr_client_failure_then_server_created_race_reuses_without_second_create(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("客户端失败但服务端已有 PR 时必须复用。"), encoding="utf-8")
        existing = {
            "number": 91,
            "url": "https://github.com/owner/repo/pull/91",
            "headRefName": "codex/18-publish-boundary",
            "baseRefName": "main",
        }
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "marketplace_verification_required", return_value=False),
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(
                    gtt,
                    "create_pull_request",
                    side_effect=gtt.WorkflowError("client lost response", exit_code=2),
                ) as create_pr,
                mock.patch.object(
                    gtt,
                    "resolve_open_pull_request_for_recovery",
                    return_value={"state": "one", "open_pr_count": 1, "pull_request": existing},
                ) as resolve_pr,
                mock.patch.object(
                    gtt,
                    "update_finish_summary_for_pr",
                    return_value=(self.task_dir / "finish-summary.json", {}),
                ),
                mock.patch.object(
                    gtt,
                    "commit_and_push_finish_summary_metadata",
                    return_value={"committed": True, "commit": "c" * 40},
                ),
            ):
                with self.assertRaises(gtt.WorkflowError) as first_attempt:
                    gtt.cmd_publish_pr(publish_args(
                        from_finish_work=True,
                        dry_run=False,
                        body_file=str(body_path),
                    ))
                recovered = gtt.cmd_publish_pr(publish_args(
                    recovery_after_finish_work=True,
                    dry_run=False,
                    body_file=str(body_path),
                ))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(first_attempt.exception.payload["failed_stage"], "gh-pr-create")
        self.assertEqual(create_pr.call_count, 1)
        resolve_pr.assert_called_once()
        self.assertTrue(recovered["pr_recovery"]["reused_existing_open_pr"])

    def test_publish_pr_zero_open_single_retry_failure_keeps_summary_and_same_recovery_command(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("零个 PR 的单次 retry 再失败。"), encoding="utf-8")
        summary_path = self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT
        initial_summary = b'{"github":{"pr_url":""},"index":{"search_terms":{"pr_refs":[]}}}\n'
        summary_path.write_bytes(initial_summary)
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "marketplace_verification_required", return_value=False),
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(
                    gtt,
                    "create_pull_request",
                    side_effect=[
                        gtt.WorkflowError("normal create failed", exit_code=2),
                        gtt.WorkflowError("recovery create failed", exit_code=2),
                    ],
                ) as create_pr,
                mock.patch.object(
                    gtt,
                    "resolve_open_pull_request_for_recovery",
                    return_value={"state": "none", "open_pr_count": 0, "pull_request": None},
                ) as resolve_pr,
                mock.patch.object(gtt, "update_finish_summary_for_pr") as update_summary,
            ):
                with self.assertRaises(gtt.WorkflowError) as first_attempt:
                    gtt.cmd_publish_pr(publish_args(
                        from_finish_work=True,
                        dry_run=False,
                        body_file=str(body_path),
                    ))
                with self.assertRaises(gtt.WorkflowError) as retry_attempt:
                    gtt.cmd_publish_pr(publish_args(
                        recovery_after_finish_work=True,
                        dry_run=False,
                        body_file=str(body_path),
                    ))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(create_pr.call_count, 2)
        resolve_pr.assert_called_once()
        update_summary.assert_not_called()
        self.assertEqual(summary_path.read_bytes(), initial_summary)
        self.assertEqual(retry_attempt.exception.payload["failed_stage"], "gh-pr-create-recovery")
        self.assertEqual(
            retry_attempt.exception.payload["recovery_command"],
            first_attempt.exception.payload["recovery_command"],
        )
        self.assertEqual(
            retry_attempt.exception.payload["publish_inputs"],
            first_attempt.exception.payload["publish_inputs"],
        )
        self.assertEqual(retry_attempt.exception.payload["pr_url"], "")

    def test_publish_pr_backwrite_failure_preserves_pr_url_and_recovery_command(self) -> None:
        body_path = self.root / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("PR URL 回写失败 recovery。"), encoding="utf-8")
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "marketplace_verification_required", return_value=False),
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(gtt, "current_head", return_value="a" * 40),
                mock.patch.object(gtt, "run", return_value=mock.Mock(returncode=0, stdout="https://github.com/owner/repo/pull/91\n", stderr="")),
                mock.patch.object(gtt, "update_finish_summary_for_pr", side_effect=gtt.WorkflowError("rewrite failed", exit_code=2)),
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_publish_pr(publish_args(
                    from_finish_work=True,
                    recovery_after_finish_work=False,
                    dry_run=False,
                    body_file=str(body_path),
                ))
        finally:
            for patcher in reversed(patches):
                patcher.stop()
        self.assertEqual(raised.exception.payload["failed_stage"], "finish-summary-rewrite")
        self.assertEqual(raised.exception.payload["pr_url"], "https://github.com/owner/repo/pull/91")
        self.assertEqual(raised.exception.payload["publish_inputs"]["head_branch"], "codex/18-publish-boundary")
        self.assertIn("--recovery-after-finish-work", raised.exception.payload["recovery_command"])

    def test_finish_summary_metadata_commit_rejects_unexpected_dirty_path(self) -> None:
        summary = self.task_dir / "finish-summary.json"
        summary.write_text("{}\n", encoding="utf-8")
        with (
            mock.patch.object(gtt, "git_status_paths", return_value=[
                ".trellis/tasks/07-04-publish-boundary/finish-summary.json", "trellis/workflows/guru-team/workflow.md"
            ]),
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.commit_and_push_finish_summary_metadata(
                self.root, summary, "chore(trellis): #18 固化任务收尾元数据", "origin", "codex/18-publish-boundary"
            )
        self.assertIn("trellis/workflows/guru-team/workflow.md", raised.exception.payload["unexpected_dirty_paths"])


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
            '{"close_issues":[{"number":20,"title":"Review gate","acceptance_evidence":["ok"]}],'
            '"related_issues":[],"followup_issues":[]}\n',
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def patch_review_command(self) -> list[mock._patch]:
        return [
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_start_context", return_value={
                "base_branch": "main",
                "workspace_mode": "worktree",
                "workspace_path": str(self.root),
                "task_dir": ".trellis/tasks/07-04-review-gate",
                "preflight": {"current_checkout": str(self.root)},
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "validate_planning_approval", return_value=(self.task_dir / "planning-approval.json", {}, [])),
            mock.patch.object(gtt, "validate_phase2_check", return_value=(self.task_dir / "phase2-check.json", {}, [])),
            mock.patch.object(gtt, "current_branch", return_value="codex/20-review-gate"),
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "diff_base_ref", return_value="origin/main"),
            mock.patch.object(gtt, "changed_files", return_value=["trellis/workflows/guru-team/workflow.md"]),
        ]

    def write_raw_review_report(self, name: str, content: str | None = None) -> Path:
        reports_dir = self.task_dir / "reviews"
        reports_dir.mkdir(parents=True, exist_ok=True)
        path = reports_dir / name
        path.write_text(content or f"# 原始审查报告\n\n{name} 原始审查证据。\n", encoding="utf-8")
        return path

    def raw_report_name_for_round(self, round_item: dict[str, object], index: int) -> str:
        round_number = round_item.get("round") if isinstance(round_item.get("round"), int) else index + 1
        role = round_item.get("logical_role")
        findings_count = round_item.get("findings_count")
        if role == "最终放行审查代理" and findings_count == 0:
            suffix = "final-release"
        elif role == "问题闭环审查代理":
            suffix = "closure"
        else:
            suffix = "problem-finding" if findings_count else "review"
        return f"round-{int(round_number):03d}-{suffix}.md"

    def raw_report_names_for_rounds(self, rounds: list[dict[str, object]]) -> list[str]:
        return [self.raw_report_name_for_round(item, index) for index, item in enumerate(rounds)]

    def add_raw_report_fields(self, round_item: dict[str, object], index: int) -> dict[str, object]:
        item = dict(round_item)
        if "review_report_path" in item:
            return item
        report = self.write_raw_review_report(self.raw_report_name_for_round(item, index))
        digest = gtt.file_digest(self.root, report)
        item.update(
            {
                "review_report_path": digest["path"],
                "review_report_sha256": digest["sha256"],
                "review_report_size_bytes": digest["size_bytes"],
                "review_report_modified_at": digest["modified_at"],
            }
        )
        return item

    def review_rollup_text(self, body: str, report_names: list[str] | None = None) -> str:
        names = report_names or ["round-001-final-release.md"]
        links = "\n".join(f"- reviews/{name}" for name in names)
        return f"# 审查报告\n\n{body}\n\n## 原始报告链接\n\n{links}\n"

    def write_agent_assignment(
        self,
        review_rounds: list[dict[str, object]] | None = None,
        reuse_decisions: list[dict[str, object]] | None = None,
        status_events: list[dict[str, object]] | None = None,
    ) -> Path:
        assignment = self.task_dir / "agent-assignment.json"
        rounds = review_rounds if review_rounds is not None else [
            {
                "round": 1,
                "logical_role": "最终放行审查代理",
                "agent_id": "019f315a-f262-7521-acdf-78e4adc99a11",
                "platform_nickname": "Gibbs",
                "reviewed_head": "abc123",
                "findings_count": 0,
                "reuse_policy": "最终放行审查代理必须是 fresh new agent，并完整审查当前 diff。",
                "reuse_decision": "new-agent",
            }
        ]
        rounds = [self.add_raw_report_fields(item, index) for index, item in enumerate(rounds)]
        normalized_status_events: list[dict[str, object]] = []
        last_terminal_by_agent: dict[str, dict[str, object]] = {}
        for index, raw in enumerate(status_events or []):
            item = dict(raw)
            item.setdefault("event_id", f"evt-{index + 1:04d}")
            item.setdefault("recorded_at", item.get("observed_at", "2026-07-07T00:00:00Z"))
            item.setdefault("source", "main-session")
            item.setdefault("evidence", item.get("reason") or item.get("workspace_evidence") or "测试 fixture evidence")
            event_name = str(item.get("event") or "")
            agent_id = str(item.get("agent_id") or "")
            if event_name == "terminated-unfinished":
                item.setdefault("termination_reason", "manual_or_platform_terminated_unfinished")
                item.setdefault("termination_source_event_id", "")
                last_terminal_by_agent[agent_id] = item
            elif event_name == "failed":
                last_terminal_by_agent[agent_id] = item
            elif event_name == "replacement-started":
                predecessor = str(item.get("predecessor_agent_id") or "")
                terminal = last_terminal_by_agent.get(predecessor, {})
                predecessor_event = str(terminal.get("event") or "")
                predecessor_reason = str(terminal.get("termination_reason") or "")
                item.setdefault("predecessor_agent_id", predecessor)
                item.setdefault("predecessor_event_id", terminal.get("event_id", ""))
                if predecessor_event == "failed":
                    item.setdefault("replacement_reason", "terminal_failed_incomplete")
                elif predecessor_reason == "manual_or_platform_terminated_unfinished":
                    item.setdefault("replacement_reason", "manual_or_platform_terminated_unfinished")
                else:
                    item.setdefault("replacement_reason", "max_progress_silence_exceeded")
            item.setdefault("predecessor_agent_id", "")
            item.setdefault("predecessor_event_id", "")
            item.setdefault("termination_reason", "")
            item.setdefault("termination_source_event_id", "")
            item.setdefault("replacement_reason", "")
            item.setdefault("handoff_summary", item.get("handoff_summary", ""))
            normalized_status_events.append(item)
        agents = [
            {
                "logical_role": "实现代理",
                "agent_id": "019f315a-f262-7521-acdf-78e4adc99a11",
                "platform_nickname": "Gibbs",
                "assigned_at": "2026-07-05T00:00:00Z",
                "assigned_head": "abc123",
                "reason": "Codex sub-agent 模式下分配实现代理。",
            }
        ]
        known_agents = {str(agents[0]["agent_id"])}
        for item in normalized_status_events:
            agent_id = str(item.get("agent_id") or "")
            if not agent_id or agent_id in known_agents:
                continue
            agents.append(
                {
                    "logical_role": item.get("logical_role") or "实现代理",
                    "agent_id": agent_id,
                    "platform_nickname": item.get("platform_nickname") or agent_id,
                    "assigned_at": item.get("observed_at") or "2026-07-05T00:00:00Z",
                    "assigned_head": item.get("head") or "abc123",
                    "reason": "测试 fixture 中的 status event agent 已按新 liveness 合同登记。",
                }
            )
            known_agents.add(agent_id)
        assignment.write_text(
            gtt.json.dumps(
                {
                    "schema_version": "1.1",
                    "task": ".trellis/tasks/07-04-review-gate",
                    "head": "abc123",
                    "agents": agents,
                    "liveness": {},
                    "review_rounds": rounds,
                    "reuse_decisions": reuse_decisions if reuse_decisions is not None else [],
                    "status_events": normalized_status_events,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return assignment

    def test_review_branch_pass_requires_review_report(self) -> None:
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_review_branch(review_args(review_report=None))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("--review-report", str(raised.exception))
        self.assertIn("--reviewer is identity metadata only", str(raised.exception))

    def test_review_branch_records_review_report_digest(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text(self.review_rollup_text("无 finding。"), encoding="utf-8")
        assignment = self.write_agent_assignment()
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                payload = gtt.cmd_review_branch(
                    review_args(
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        recorded = payload["verification_evidence"]["review_report"]
        self.assertEqual(recorded["path"], ".trellis/tasks/07-04-review-gate/review.md")
        self.assertEqual(recorded["size_bytes"], review_report.stat().st_size)
        self.assertEqual(recorded["sha256"], gtt.hashlib.sha256(review_report.read_bytes()).hexdigest())
        raw_reports = payload["verification_evidence"]["review_reports"]
        self.assertEqual(len(raw_reports), 1)
        self.assertEqual(raw_reports[0]["path"], ".trellis/tasks/07-04-review-gate/reviews/round-001-final-release.md")
        self.assertEqual(raw_reports[0]["sha256"], gtt.hashlib.sha256((self.task_dir / "reviews/round-001-final-release.md").read_bytes()).hexdigest())
        self.assertTrue(recorded["modified_at"])
        self.assertTrue((self.task_dir / "review-gate.json").exists())

    def test_review_branch_rejects_final_rollup_english_template_headings(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text(
            "# Review Rounds\n\n"
            "- reviews/round-001-final-release.md\n\n"
            "## Findings Lifecycle\n\n无 finding。\n\n"
            "## Deployment / safety impact\n\n未涉及部署资产。\n\n"
            "## Follow-up Candidates\n\n无后续候选。\n",
            encoding="utf-8",
        )
        assignment = self.write_agent_assignment()
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "git_object_exists", return_value=True),
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_review_branch(
                    review_args(
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        errors = raised.exception.payload["errors"]
        self.assertTrue(any("Review Rounds" in error for error in errors))
        self.assertTrue(any("Findings Lifecycle" in error for error in errors))
        self.assertTrue(any("Deployment / safety impact" in error for error in errors))
        self.assertTrue(any("Follow-up Candidates" in error for error in errors))

    def test_review_branch_rejects_raw_report_english_template_heading(self) -> None:
        raw_report = self.write_raw_review_report(
            "round-001-final-release.md",
            "# Evidence Handoff\n\nBranch Review raw evidence。\n",
        )
        digest = gtt.file_digest(self.root, raw_report)
        review_report = self.task_dir / "review.md"
        review_report.write_text(self.review_rollup_text("无 finding。"), encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "019f315a-f262-7521-acdf-78e4adc99a11",
                    "platform_nickname": "Gibbs",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "最终放行审查代理必须是 fresh new agent，并完整审查当前 diff。",
                    "reuse_decision": "new-agent",
                    "review_report_path": digest["path"],
                    "review_report_sha256": digest["sha256"],
                    "review_report_size_bytes": digest["size_bytes"],
                    "review_report_modified_at": digest["modified_at"],
                }
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "git_object_exists", return_value=True),
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_review_branch(
                    review_args(
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("Evidence Handoff" in error for error in raised.exception.payload["errors"]))

    def test_review_branch_pass_requires_rollup_to_link_raw_reports(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n缺少 raw report 链接。\n", encoding="utf-8")
        assignment = self.write_agent_assignment()
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "git_object_exists", return_value=True),
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_review_branch(
                    review_args(
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertIn("review.md does not link every raw review report", str(raised.exception))
        self.assertTrue(any("reviews/round-001-final-release.md" in error for error in raised.exception.payload["errors"]))

    def test_review_branch_pass_requires_agent_assignment(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n缺少 agent-assignment，无法证明 fresh final reviewer。\n", encoding="utf-8")
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_review_branch(review_args(review_report=str(review_report)))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("--agent-assignment", str(raised.exception))
        self.assertIn("fresh 最终放行审查代理", str(raised.exception))

    def test_review_branch_pass_rejects_p3_finding(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\nP3 finding 也必须阻断。\n", encoding="utf-8")
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_review_branch(
                    review_args(
                        review_report=str(review_report),
                        finding=["P3|需要收敛的轻微问题|trellis/workflows/guru-team/workflow.md"],
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("any findings", str(raised.exception))

    def test_review_branch_records_blocking_finding_as_failed_artifact(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n独立审查发现 P3 finding。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "reviewer-a",
                    "platform_nickname": "问题发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "发现 finding 的 agent 只能复用为闭环审查代理。",
                    "reuse_decision": "new-agent",
                }
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                payload = gtt.cmd_review_branch(
                    review_args(
                        pass_gate=False,
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                        finding=["P3|需要收敛的轻微问题|trellis/workflows/guru-team/workflow.md"],
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertFalse(payload["conclusion"]["passed"])
        self.assertEqual(payload["conclusion"]["findings_count"], 1)
        self.assertEqual(payload["conclusion"]["blocking_findings_count"], 1)
        self.assertEqual(payload["verification_evidence"]["review_source"], gtt.INDEPENDENT_REVIEW_SOURCE)
        self.assertEqual(payload["verification_evidence"]["review_report"]["path"], ".trellis/tasks/07-04-review-gate/review.md")
        self.assertEqual(payload["verification_evidence"]["review_reports"][0]["findings_count"], 1)
        self.assertTrue((self.task_dir / "review-gate.json").exists())

    def test_review_branch_findings_requires_current_matching_review_round(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n独立审查发现 P3 finding。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "reviewer-a",
                    "platform_nickname": "问题发现代理",
                    "reviewed_head": "old123",
                    "findings_count": 1,
                    "reuse_policy": "发现 finding 的 agent 只能复用为闭环审查代理。",
                    "reuse_decision": "new-agent",
                }
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "git_object_exists", return_value=True),
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.cmd_review_branch(
                    review_args(
                        pass_gate=False,
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                        finding=["P3|需要收敛的轻微问题|trellis/workflows/guru-team/workflow.md"],
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        errors = raised.exception.payload["errors"]
        self.assertTrue(any("reviewed_head=abc123" in error and "findings_count=1" in error for error in errors))

    def test_review_branch_records_observations_without_blocking_pass(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text(self.review_rollup_text("无 finding，仅有 observation。"), encoding="utf-8")
        assignment = self.write_agent_assignment()
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                payload = gtt.cmd_review_branch(
                    review_args(
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                        observation=["文案可后续更精炼|trellis/workflows/guru-team/workflow.md"],
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(payload["conclusion"]["passed"])
        self.assertEqual(payload["conclusion"]["findings_count"], 0)
        self.assertEqual(payload["conclusion"]["observations_count"], 1)
        self.assertEqual(payload["observations"][0]["kind"], "observation")

    def test_review_branch_records_followup_candidates_without_blocking_pass(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text(self.review_rollup_text("无 finding，仅有 follow-up candidate。"), encoding="utf-8")
        assignment = self.write_agent_assignment()
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                payload = gtt.cmd_review_branch(
                    review_args(
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                        followup_candidate=["后续可增强 PR body lint|trellis/workflows/guru-team/scripts/python/guru_team_trellis.py"],
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(payload["conclusion"]["passed"])
        self.assertEqual(payload["conclusion"]["findings_count"], 0)
        self.assertEqual(payload["conclusion"]["followup_candidates_count"], 1)
        self.assertEqual(payload["followup_candidates"][0]["kind"], "followup_candidate")

    def test_review_branch_records_agent_assignment_digest(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text(self.review_rollup_text("fresh 最终放行审查代理给出 0 findings。"), encoding="utf-8")
        assignment = self.write_agent_assignment()
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                payload = gtt.cmd_review_branch(
                    review_args(
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        recorded = payload["verification_evidence"]["agent_assignment"]
        self.assertEqual(recorded["path"], ".trellis/tasks/07-04-review-gate/agent-assignment.json")
        self.assertEqual(recorded["sha256"], gtt.hashlib.sha256(assignment.read_bytes()).hexdigest())
        self.assertEqual(recorded["roles"], ["实现代理", "最终放行审查代理"])
        self.assertEqual(recorded["agents_count"], 1)
        self.assertEqual(recorded["review_rounds_count"], 1)

    def test_review_branch_pass_rejects_unclosed_terminated_unfinished_status_event(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n未完成终止事件缺少继任闭环。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            status_events=[
                {
                    "event": "terminated-unfinished",
                    "logical_role": "实现代理",
                    "agent_id": "implement-agent-a",
                    "platform_nickname": "实现代理 A",
                    "head": "abc123",
                    "observed_at": "2026-07-07T00:10:00Z",
                    "last_observed_progress_at": "2026-07-07T00:04:00Z",
                    "workspace_evidence": "git diff 无变化，channel event 无新增。",
                    "running_command_evidence": "验证命令无输出。",
                    "decision": "terminate-unfinished",
                    "reason": "AI 已判断当前 agent 无进展并中断。",
                    "handoff_summary": "前任输出、当前 diff、剩余任务已整理，等待恢复或继任。",
                }
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(
                        review_args(
                            review_report=str(review_report),
                            agent_assignment=str(assignment),
                        )
                    )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        errors = raised.exception.payload["errors"]
        self.assertTrue(any("terminated-unfinished" in error for error in errors))
        self.assertTrue(any("completed" in error for error in errors))

    def test_review_branch_pass_accepts_replacement_status_event_chain(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text(self.review_rollup_text("继任 agent 完成剩余工作后最终放行。"), encoding="utf-8")
        assignment = self.write_agent_assignment(
            status_events=[
                {
                    "event": "terminated-unfinished",
                    "logical_role": "实现代理",
                    "agent_id": "implement-agent-a",
                    "platform_nickname": "实现代理 A",
                    "head": "abc123",
                    "observed_at": "2026-07-07T00:10:00Z",
                    "last_observed_progress_at": "2026-07-07T00:04:00Z",
                    "workspace_evidence": "git diff 无变化，channel event 无新增。",
                    "running_command_evidence": "验证命令无输出。",
                    "decision": "terminate-unfinished",
                    "reason": "AI 已判断当前 agent 无进展并中断。",
                    "handoff_summary": "前任输出、当前 diff、剩余任务已整理。",
                },
                {
                    "event": "replacement-started",
                    "logical_role": "实现代理",
                    "agent_id": "implement-agent-b",
                    "platform_nickname": "实现代理 B",
                    "head": "abc123",
                    "observed_at": "2026-07-07T00:11:00Z",
                    "last_observed_progress_at": "",
                    "workspace_evidence": "继任 agent 读取前任输出和当前 diff。",
                    "running_command_evidence": "",
                    "decision": "start-replacement",
                    "reason": "同一会话无法恢复，启动继任 agent 继续剩余实现。",
                    "predecessor_agent_id": "implement-agent-a",
                    "handoff_summary": "继任已接收 task artifacts、当前 diff、剩余 checklist 和 gate 阻塞点。",
                },
                {
                    "event": "completed",
                    "logical_role": "实现代理",
                    "agent_id": "implement-agent-b",
                    "platform_nickname": "实现代理 B",
                    "head": "abc123",
                    "observed_at": "2026-07-07T00:30:00Z",
                    "last_observed_progress_at": "2026-07-07T00:29:00Z",
                    "workspace_evidence": "继任 agent 完成实现并交付验证结果。",
                    "running_command_evidence": "验证命令已结束。",
                    "decision": "mark-completed",
                    "reason": "继任 agent 已完成剩余工作。",
                    "handoff_summary": "",
                },
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                payload = gtt.cmd_review_branch(
                    review_args(
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(payload["conclusion"]["passed"])
        self.assertEqual(payload["verification_evidence"]["agent_assignment"]["status_events_count"], 3)

    def test_review_branch_rejects_finding_owner_as_final_reviewer(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n同一 agent 不能从 finding owner 变成最终放行。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "发现问题后可继续闭环确认，但不能最终放行。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "同一 agent 只确认上一轮 finding 是否修复。",
                    "reuse_decision": "reuse-for-closure",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "错误示例：复用 finding owner 作为最终放行。",
                    "reuse_decision": "new-agent",
                },
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(
                        review_args(
                            review_report=str(review_report),
                            agent_assignment=str(assignment),
                        )
                    )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("不能作为最终放行审查代理" in error for error in raised.exception.payload["errors"]))

    def test_review_branch_accepts_fresh_final_reviewer_after_finding_closure(self) -> None:
        review_report = self.task_dir / "review.md"
        rounds = [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "发现问题后可继续闭环确认，但不能最终放行。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "同一 agent 只确认上一轮 finding 是否修复。",
                    "reuse_decision": "reuse-for-closure",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "fresh final reviewer 必须完整审查当前 diff。",
                    "reuse_decision": "new-agent",
                },
        ]
        review_report.write_text(
            self.review_rollup_text(
                "fresh final reviewer 完整审查当前 HEAD，0 findings。",
                self.raw_report_names_for_rounds(rounds),
            ),
            encoding="utf-8",
        )
        assignment = self.write_agent_assignment(rounds)
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                payload = gtt.cmd_review_branch(
                    review_args(
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(payload["conclusion"]["passed"])
        self.assertEqual(payload["verification_evidence"]["agent_assignment"]["review_rounds_count"], 3)

    def test_final_review_round_errors_accepts_explicit_new_agent_closure(self) -> None:
        payload = {
            "review_rounds": [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "reviewed_head": "old123",
                    "findings_count": 2,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "reviewed_head": "fixed123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
            ],
            "reuse_decisions": [
                {
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "decision": "new-agent",
                    "reason": "agent-c 针对 round 1 findings 审查修复后的新 HEAD。",
                    "head": "fixed123",
                    "from_round": 1,
                    "to_round": 2,
                }
            ],
        }

        errors = gtt.final_review_round_errors(self.root, payload, expected_head="abc123")

        self.assertEqual(errors, [])

    def test_final_review_round_errors_accepts_chained_new_agent_closures(self) -> None:
        payload = {
            "review_rounds": [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "reviewed_head": "head-1",
                    "findings_count": 4,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "reviewed_head": "head-2",
                    "findings_count": 2,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 3,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-d",
                    "reviewed_head": "head-3",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 4,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
            ],
            "reuse_decisions": [
                {
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "decision": "new-agent",
                    "reason": "round 2 明确闭环 round 1 findings，同时记录新 findings。",
                    "head": "head-2",
                    "from_round": 1,
                    "to_round": 2,
                },
                {
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-d",
                    "decision": "new-agent",
                    "reason": "round 3 明确闭环 round 2 新 findings。",
                    "head": "head-3",
                    "from_round": 2,
                    "to_round": 3,
                },
            ],
        }

        errors = gtt.final_review_round_errors(self.root, payload, expected_head="abc123")

        self.assertEqual(errors, [])

    def test_final_review_round_errors_rejects_new_agent_closure_seen_in_earlier_round(self) -> None:
        payload = {
            "review_rounds": [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-c",
                    "reviewed_head": "head-1",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "reviewed_head": "head-2",
                    "findings_count": 1,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 3,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "reviewed_head": "head-3",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 4,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
            ],
            "reuse_decisions": [
                {
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "decision": "new-agent",
                    "reason": "Round 8 反例：agent-c 已在 round 1 出现，不能冒充 fresh closure agent。",
                    "head": "head-3",
                    "from_round": 2,
                    "to_round": 3,
                }
            ],
        }

        errors = gtt.final_review_round_errors(self.root, payload, expected_head="abc123")

        self.assertTrue(any("缺少闭环轮次" in error for error in errors))

    def test_final_review_round_errors_rejects_final_agent_seen_in_earlier_clean_round(self) -> None:
        payload = {
            "review_rounds": [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-b",
                    "reviewed_head": "old123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
            ],
            "reuse_decisions": [],
        }

        errors = gtt.final_review_round_errors(self.root, payload, expected_head="abc123")

        self.assertTrue(any("任何更早 review_rounds" in error for error in errors))

    def test_final_review_round_errors_rejects_new_agent_relation_type_and_round_decision_mismatch(self) -> None:
        base_payload = {
            "review_rounds": [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "reviewed_head": "old123",
                    "findings_count": 1,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "reviewed_head": "fixed123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
            ],
            "reuse_decisions": [
                {
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "decision": "new-agent",
                    "reason": "Round 8 关系精确性反例。",
                    "head": "fixed123",
                    "from_round": 1,
                    "to_round": 2,
                }
            ],
        }
        invalid_payloads = []
        for field, value in [("from_round", True), ("to_round", False), ("from_round", "1"), ("to_round", "2")]:
            payload = gtt.json.loads(gtt.json.dumps(base_payload))
            payload["reuse_decisions"][0][field] = value
            invalid_payloads.append(payload)
        round_mismatch = gtt.json.loads(gtt.json.dumps(base_payload))
        round_mismatch["review_rounds"][1]["reuse_decision"] = "not-applicable"
        invalid_payloads.append(round_mismatch)

        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                errors = gtt.final_review_round_errors(self.root, payload, expected_head="abc123")
                self.assertTrue(any("缺少闭环轮次" in error for error in errors))

    def test_validate_agent_assignment_rejects_non_strict_reuse_decision_rounds(self) -> None:
        assignment = self.write_agent_assignment(
            reuse_decisions=[
                {
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "decision": "new-agent",
                    "reason": "Round 8 strict int 反例。",
                    "head": "abc123",
                    "from_round": True,
                    "to_round": "2",
                }
            ]
        )
        payload = gtt.read_json(assignment)

        with mock.patch.object(gtt, "git_object_exists", return_value=True):
            errors = gtt.validate_agent_assignment_payload(self.root, self.task_dir, payload)

        self.assertTrue(any("from_round 必须是正 strict int" in error for error in errors))
        self.assertTrue(any("to_round 必须是正 strict int" in error for error in errors))

    def test_final_review_round_errors_rejects_new_agent_closure_without_explicit_relation(self) -> None:
        base_payload = {
            "review_rounds": [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "reviewed_head": "old123",
                    "findings_count": 1,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "reviewed_head": "fixed123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
            ],
            "reuse_decisions": [],
        }
        invalid_decisions = [
            None,
            {
                "logical_role": "问题闭环审查代理",
                "agent_id": "agent-c",
                "decision": "new-agent",
                "reason": "缺少 from_round/to_round。",
                "head": "fixed123",
            },
            {
                "logical_role": "问题闭环审查代理",
                "agent_id": "wrong-agent",
                "decision": "new-agent",
                "reason": "agent_id 不匹配 closure round。",
                "head": "fixed123",
                "from_round": 1,
                "to_round": 2,
            },
            {
                "logical_role": "问题闭环审查代理",
                "agent_id": "agent-c",
                "decision": "new-agent",
                "reason": "from/to 轮次错误。",
                "head": "fixed123",
                "from_round": 2,
                "to_round": 3,
            },
        ]

        for decision in invalid_decisions:
            with self.subTest(decision=decision):
                payload = gtt.json.loads(gtt.json.dumps(base_payload))
                if decision is not None:
                    payload["reuse_decisions"] = [decision]
                errors = gtt.final_review_round_errors(self.root, payload, expected_head="abc123")
                self.assertTrue(any("from_round/to_round" in error for error in errors))

    def test_final_review_round_errors_rejects_unclosed_nonzero_new_agent_closure(self) -> None:
        payload = {
            "review_rounds": [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "reviewed_head": "old123",
                    "findings_count": 1,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "reviewed_head": "fixed123",
                    "findings_count": 1,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
            ],
            "reuse_decisions": [
                {
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "decision": "new-agent",
                    "reason": "round 2 仍有 finding，不能闭环 round 1。",
                    "head": "fixed123",
                    "from_round": 1,
                    "to_round": 2,
                }
            ],
        }

        errors = gtt.final_review_round_errors(self.root, payload, expected_head="abc123")

        self.assertTrue(any("from_round/to_round" in error for error in errors))

    def test_review_branch_accepts_replacement_closure_when_original_review_agent_failed(self) -> None:
        review_report = self.task_dir / "review.md"
        rounds = [
                {
                    "round": 1,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "中断最终代理",
                    "reviewed_head": "old123",
                    "findings_count": 1,
                    "reuse_policy": "fresh final reviewer 发现 P2 finding，但随后失败，不能自己闭环。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "platform_nickname": "替代闭环代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "替代中断 agent，仅闭环 round 1 finding，不作为最终放行。",
                    "reuse_decision": "replace",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "fresh final reviewer 必须完整审查当前 HEAD diff。",
                    "reuse_decision": "new-agent",
                },
        ]
        review_report.write_text(
            self.review_rollup_text(
                "round 1 的 finding 已由替代闭环代理完成，fresh final reviewer 当前 HEAD 0 findings。",
                self.raw_report_names_for_rounds(rounds),
            ),
            encoding="utf-8",
        )
        assignment = self.write_agent_assignment(
            rounds,
            reuse_decisions=[
                {
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "decision": "replace",
                    "reason": "agent-a 已失败，无法继续同一技术 agent 闭环；agent-c 只闭环 round 1 finding。",
                    "head": "abc123",
                    "from_round": 1,
                    "to_round": 2,
                }
            ],
            status_events=[
                {
                    "event": "failed",
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "中断最终代理",
                    "head": "old123",
                    "observed_at": "2026-07-07T00:10:00Z",
                    "last_observed_progress_at": "",
                    "workspace_evidence": "raw report 已保留，连接中断后无法同 agent 继续。",
                    "running_command_evidence": "review agent stream disconnected。",
                    "decision": "mark-failed",
                    "reason": "该 agent 已失败，不能作为 passing final，也不能继续闭环。",
                    "handoff_summary": "",
                },
                {
                    "event": "replacement-started",
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "platform_nickname": "替代闭环代理",
                    "head": "abc123",
                    "observed_at": "2026-07-07T00:11:00Z",
                    "last_observed_progress_at": "",
                    "workspace_evidence": "替代 agent 读取前任 raw report、当前 diff 和 finding。",
                    "running_command_evidence": "替代闭环审查已启动。",
                    "decision": "start-replacement",
                    "reason": "原 review agent 已失败，启动替代闭环代理只复核该 finding。",
                    "predecessor_agent_id": "agent-a",
                    "handoff_summary": "闭环目标：确认 round 1 finding 在当前 HEAD 已修复。",
                },
                {
                    "event": "completed",
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "platform_nickname": "替代闭环代理",
                    "head": "abc123",
                    "observed_at": "2026-07-07T00:20:00Z",
                    "last_observed_progress_at": "2026-07-07T00:19:00Z",
                    "workspace_evidence": "替代闭环 raw report 已写入 task worktree。",
                    "running_command_evidence": "闭环审查完成，findings_count=0。",
                    "decision": "mark-completed",
                    "reason": "替代闭环代理已确认 finding 闭环。",
                    "handoff_summary": "",
                },
            ],
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            def object_exists(_root: Path, ref: str) -> bool:
                return ref in {"abc123", "old123"}

            with mock.patch.object(gtt, "git_object_exists", side_effect=object_exists):
                payload = gtt.cmd_review_branch(
                    review_args(
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(payload["conclusion"]["passed"])
        self.assertEqual(payload["verification_evidence"]["agent_assignment"]["reuse_decisions_count"], 1)
        self.assertEqual(payload["verification_evidence"]["agent_assignment"]["status_events_count"], 3)

    def test_review_branch_rejects_replacement_closure_without_recovery_evidence(self) -> None:
        review_report = self.task_dir / "review.md"
        rounds = [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "old123",
                    "findings_count": 1,
                    "reuse_policy": "发现问题后必须闭环。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "platform_nickname": "替代闭环代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "错误示例：只写 replace round，没有恢复链证据。",
                    "reuse_decision": "replace",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "fresh final reviewer 必须完整审查当前 HEAD diff。",
                    "reuse_decision": "new-agent",
                },
        ]
        review_report.write_text(
            self.review_rollup_text(
                "缺少 replacement-started / completed 恢复链时不能最终放行。",
                self.raw_report_names_for_rounds(rounds),
            ),
            encoding="utf-8",
        )
        assignment = self.write_agent_assignment(
            rounds,
            reuse_decisions=[
                {
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "decision": "replace",
                    "reason": "缺少 status_events 恢复链的替代闭环不能通过。",
                    "head": "abc123",
                    "from_round": 1,
                    "to_round": 2,
                }
            ],
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            def object_exists(_root: Path, ref: str) -> bool:
                return ref in {"abc123", "old123"}

            with mock.patch.object(gtt, "git_object_exists", side_effect=object_exists):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(
                        review_args(
                            review_report=str(review_report),
                            agent_assignment=str(assignment),
                        )
                    )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("replacement-started" in error for error in raised.exception.payload["errors"]))

    def test_final_review_round_errors_rejects_replacement_closure_agent_as_final(self) -> None:
        payload = {
            "review_rounds": [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "reviewed_head": "old123",
                    "findings_count": 1,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "replace",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-c",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
            ],
            "reuse_decisions": [
                {
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "decision": "replace",
                    "reason": "agent-a failed; agent-c closes only the finding.",
                    "head": "abc123",
                    "from_round": 1,
                    "to_round": 2,
                }
            ],
            "status_events": [
                {
                    "event": "failed",
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "head": "old123",
                    "decision": "mark-failed",
                },
                {
                    "event": "replacement-started",
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "head": "abc123",
                    "decision": "start-replacement",
                    "predecessor_agent_id": "agent-a",
                    "handoff_summary": "agent-c closes round 1 finding only.",
                },
                {
                    "event": "completed",
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "head": "abc123",
                    "decision": "mark-completed",
                },
            ],
        }

        errors = gtt.final_review_round_errors(self.root, payload, expected_head="abc123")

        self.assertTrue(any("替代 finding closure" in error for error in errors))

    def test_final_review_round_errors_rejects_new_agent_closure_agent_as_final(self) -> None:
        payload = {
            "review_rounds": [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "reviewed_head": "old123",
                    "findings_count": 1,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-c",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
            ],
            "reuse_decisions": [
                {
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-c",
                    "decision": "new-agent",
                    "reason": "agent-c 只负责闭环 round 1 finding。",
                    "head": "abc123",
                    "from_round": 1,
                    "to_round": 2,
                }
            ],
        }

        errors = gtt.final_review_round_errors(self.root, payload, expected_head="abc123")

        self.assertTrue(any("finding closure" in error for error in errors))

    def test_review_branch_accepts_prior_head_closure_before_current_final(self) -> None:
        review_report = self.task_dir / "review.md"
        rounds = [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "old123",
                    "findings_count": 1,
                    "reuse_policy": "发现问题后可继续闭环确认，但不能最终放行。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "old123",
                    "findings_count": 0,
                    "reuse_policy": "同一 agent 确认自己发现的问题已修复。",
                    "reuse_decision": "reuse-for-closure",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "fresh final reviewer 必须完整审查当前 HEAD diff。",
                    "reuse_decision": "new-agent",
                },
        ]
        review_report.write_text(
            self.review_rollup_text(
                "fresh final reviewer 负责当前 HEAD 完整 diff，历史 closure 不需要随 HEAD 重跑。",
                self.raw_report_names_for_rounds(rounds),
            ),
            encoding="utf-8",
        )
        assignment = self.write_agent_assignment(rounds)
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                payload = gtt.cmd_review_branch(
                    review_args(
                        review_report=str(review_report),
                        agent_assignment=str(assignment),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertTrue(payload["conclusion"]["passed"])
        self.assertEqual(payload["verification_evidence"]["agent_assignment"]["review_rounds_count"], 3)

    def test_review_branch_rejects_bool_findings_count(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\nfindings_count 必须是明确整数 0。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理",
                    "reviewed_head": "abc123",
                    "findings_count": False,
                    "reuse_policy": "错误示例：JSON false 不能冒充明确的 0 findings。",
                    "reuse_decision": "new-agent",
                }
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(
                        review_args(
                            review_report=str(review_report),
                            agent_assignment=str(assignment),
                        )
                    )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("findings_count 必须是非负整数" in error for error in raised.exception.payload["errors"]))

    def test_final_review_round_errors_rejects_bool_final_findings_count(self) -> None:
        payload = {
            "review_rounds": [
                {
                    "round": 1,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "reviewed_head": "abc123",
                    "findings_count": False,
                    "reuse_decision": "new-agent",
                }
            ],
        }

        errors = gtt.final_review_round_errors(self.root, payload, expected_head="abc123")

        self.assertTrue(any("findings_count 必须为明确整数 0" in error for error in errors))

    def test_review_branch_rejects_final_reviewer_without_prior_closure_round(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n缺少问题闭环审查代理。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "发现问题后必须先由同 agent 闭环确认。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "错误示例：未经过 finding owner 闭环就最终放行。",
                    "reuse_decision": "new-agent",
                },
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(
                        review_args(
                            review_report=str(review_report),
                            agent_assignment=str(assignment),
                        )
                    )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("问题闭环审查代理" in error for error in raised.exception.payload["errors"]))

    def test_review_branch_rejects_stale_final_review_round_head(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n最终放行 round 的 HEAD 过期。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理",
                    "reviewed_head": "old123",
                    "findings_count": 0,
                    "reuse_policy": "fresh final reviewer 必须完整审查当前 diff。",
                    "reuse_decision": "new-agent",
                }
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            def object_exists(_root: Path, ref: str) -> bool:
                return ref in {"abc123", "old123"}

            with mock.patch.object(gtt, "git_object_exists", side_effect=object_exists):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(
                        review_args(
                            review_report=str(review_report),
                            agent_assignment=str(assignment),
                        )
                    )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("与当前 HEAD" in error for error in raised.exception.payload["errors"]))

    def test_review_branch_rejects_finding_round_without_agent_id(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n发现过 finding 的轮次缺少 agent_id。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "发现问题后必须记录 technical agent id。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "fresh final reviewer 必须完整审查当前 diff。",
                    "reuse_decision": "new-agent",
                },
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(
                        review_args(
                            review_report=str(review_report),
                            agent_assignment=str(assignment),
                        )
                    )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("必须记录 agent_id" in error for error in raised.exception.payload["errors"]))

    def test_review_branch_rejects_non_integer_round_without_crashing(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\nround 字段非法时应返回校验错误。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
                {
                    "round": "one",
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "非法 round 应由 validator fail closed。",
                    "reuse_decision": "new-agent",
                },
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(
                        review_args(
                            review_report=str(review_report),
                            agent_assignment=str(assignment),
                        )
                    )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("round 必须是正整数" in error for error in raised.exception.payload["errors"]))

    def test_review_branch_rejects_new_final_round_without_prior_closure(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n上一轮 fresh final reviewer 发现 finding 后也必须先闭环。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "发现问题后必须由同 agent 闭环确认。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "同一 agent 只确认上一轮 finding 是否修复。",
                    "reuse_decision": "reuse-for-closure",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理一",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "fresh final reviewer 完整审查但发现新 finding。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 4,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-c",
                    "platform_nickname": "最终代理二",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "错误示例：跳过 agent-b 闭环直接换新 final。",
                    "reuse_decision": "new-agent",
                },
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(
                        review_args(
                            review_report=str(review_report),
                            agent_assignment=str(assignment),
                        )
                    )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("agent-b" in error and "问题闭环审查代理" in error for error in raised.exception.payload["errors"]))

    def test_review_branch_rejects_duplicate_review_round_numbers(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n重复 round 不能证明最后一轮 final reviewer。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "发现问题后必须由同 agent 闭环确认。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "同一 agent 只确认上一轮 finding 是否修复。",
                    "reuse_decision": "reuse-for-closure",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理一",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "fresh final reviewer 完整审查当前 diff。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "错误示例：重复 round 让最后一轮 final 有歧义。",
                    "reuse_decision": "new-agent",
                },
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(
                        review_args(
                            review_report=str(review_report),
                            agent_assignment=str(assignment),
                        )
                    )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("round 3 重复" in error for error in raised.exception.payload["errors"]))

    def test_review_branch_rejects_non_increasing_review_round_numbers(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\nround 必须按记录顺序严格递增。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 2,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "发现问题后必须由同 agent 闭环确认。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 1,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "同一 agent 只确认上一轮 finding 是否修复。",
                    "reuse_decision": "reuse-for-closure",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "fresh final reviewer 完整审查当前 diff。",
                    "reuse_decision": "new-agent",
                },
            ]
        )
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(
                        review_args(
                            review_report=str(review_report),
                            agent_assignment=str(assignment),
                        )
                    )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("严格递增" in error for error in raised.exception.payload["errors"]))

    def test_final_review_round_errors_rejects_duplicate_highest_final_round(self) -> None:
        payload = {
            "review_rounds": [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-a",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "reuse-for-closure",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-a",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_decision": "new-agent",
                },
            ],
        }

        errors = gtt.final_review_round_errors(self.root, payload, expected_head="abc123")

        self.assertTrue(any("round 3 重复" in error for error in errors))
        self.assertTrue(any("唯一最后一轮" in error for error in errors))

    def test_review_branch_rejects_invalid_agent_assignment(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n无 finding。\n", encoding="utf-8")
        assignment = self.write_agent_assignment()
        payload = gtt.read_json(assignment)
        payload["agents"][0]["logical_role"] = "Reviewer"
        assignment.write_text(gtt.json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(gtt, "git_object_exists", return_value=True):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(
                        review_args(
                            review_report=str(review_report),
                            agent_assignment=str(assignment),
                        )
                    )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("agent assignment", str(raised.exception).lower())
        self.assertTrue(any("logical_role" in error for error in raised.exception.payload["errors"]))

    def test_review_branch_pass_rejects_main_session_reviewer(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n主会话自审不应通过。\n", encoding="utf-8")
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_review_branch(
                    review_args(
                        reviewer="codex-main-session",
                        review_source=gtt.INDEPENDENT_REVIEW_SOURCE,
                        review_report=str(review_report),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("independent Agent", str(raised.exception))
        self.assertIn("main-session", raised.exception.payload["errors"][0])

    def test_review_branch_pass_requires_independent_review_source(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n缺 review_source 不应通过。\n", encoding="utf-8")
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_review_branch(
                    review_args(
                        review_source="",
                        review_report=str(review_report),
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn(gtt.INDEPENDENT_REVIEW_SOURCE, raised.exception.payload["errors"][0])

    def test_review_branch_findings_require_independent_review_source(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\nfindings artifact 也需要 independent source。\n", encoding="utf-8")
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_review_branch(
                    review_args(
                        pass_gate=False,
                        review_source="",
                        review_report=str(review_report),
                        finding=["P3|需要修复|trellis/workflows/guru-team/workflow.md"],
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn(gtt.INDEPENDENT_REVIEW_SOURCE, raised.exception.payload["errors"][0])

    def test_review_branch_requires_report_even_with_blocking_findings(self) -> None:
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_review_branch(
                    review_args(
                        pass_gate=False,
                        review_report=None,
                        finding=["P2|需要修复|trellis/workflows/guru-team/workflow.md"],
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("--review-report", str(raised.exception))

    def test_review_branch_requires_phase2_check_report(self) -> None:
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with mock.patch.object(
                gtt,
                "validate_phase2_check",
                return_value=(self.task_dir / "phase2-check.json", {}, ["phase2 missing"]),
            ):
                with self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_review_branch(review_args(review_report=str(self.task_dir / "review.md")))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("Phase 2 check report", str(raised.exception))

    def test_review_branch_requires_task_local_review_report(self) -> None:
        outside_report = self.root / "review.md"
        outside_report.write_text("# Review\n\n错误位置。\n", encoding="utf-8")
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_review_branch(review_args(review_report=str(outside_report)))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertIn("task-local review.md", str(raised.exception))

    def test_review_branch_requires_review_report_named_review_md(self) -> None:
        wrong_report = self.task_dir / "prd.md"
        wrong_report.write_text("# PRD\n\n不是 review report。\n", encoding="utf-8")
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_review_branch(review_args(review_report=str(wrong_report)))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertIn("review.md", str(raised.exception))

    def write_gate(self, head: str = "abc123", review_report: dict[str, object] | None = None) -> None:
        gate = {
            "head": head,
            "conclusion": {"passed": True, "summary": "Branch Review Gate 通过。"},
            "verification_evidence": {
                "reviewer": "trellis-check-agent",
                "review_source": gtt.INDEPENDENT_REVIEW_SOURCE,
                "review_report": review_report,
                "evidence": ["已覆盖 CI/CD、Docker、K8s、migration、Makefile 部署影响判断。"],
            },
        }
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def valid_report(self) -> dict[str, object]:
        review_report = self.task_dir / "review.md"
        if not review_report.exists():
            self.write_raw_review_report("round-001-final-release.md")
            review_report.write_text(self.review_rollup_text("最终放行审查代理给出 0 findings。"), encoding="utf-8")
        return gtt.file_digest(self.root, review_report)

    def assignment_summary_for_path(self, assignment: Path) -> dict[str, object]:
        return {
            "path": ".trellis/tasks/07-04-review-gate/agent-assignment.json",
            "sha256": gtt.hashlib.sha256(assignment.read_bytes()).hexdigest(),
            "size_bytes": assignment.stat().st_size,
            "modified_at": "2026-07-04T00:00:00+00:00",
            "roles": ["实现代理", "最终放行审查代理"],
            "agents_count": 1,
            "review_rounds_count": 1,
            "reuse_decisions_count": 0,
        }

    def valid_assignment_summary(self) -> dict[str, object]:
        return self.assignment_summary_for_path(self.write_agent_assignment())

    def review_reports_summary_for_assignment(self, assignment: Path | None = None) -> list[dict[str, object]]:
        assignment_path = assignment or (self.task_dir / "agent-assignment.json")
        payload = gtt.read_json(assignment_path)
        return gtt.review_reports_from_assignment(self.root, self.task_dir, payload)

    def add_assignment_evidence_to_gate(self, gate: dict[str, object], assignment: Path | None = None) -> Path:
        assignment_path = assignment or self.write_agent_assignment()
        verification = gate.setdefault("verification_evidence", {})
        assert isinstance(verification, dict)
        verification["agent_assignment"] = self.assignment_summary_for_path(assignment_path)
        verification["review_reports"] = self.review_reports_summary_for_assignment(assignment_path)
        return assignment_path

    def write_archived_gate_with_active_paths(self) -> Path:
        review_report = self.task_dir / "review.md"
        review_report.write_text(self.review_rollup_text("最终放行审查代理给出 0 findings。"), encoding="utf-8")
        assignment = self.write_agent_assignment()
        self.write_gate(review_report=gtt.file_digest(self.root, review_report))
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["task_dir"] = ".trellis/tasks/07-04-review-gate"
        gate["findings"] = []
        gate["conclusion"]["findings_count"] = 0
        gate["conclusion"]["blocking_findings_count"] = 0
        gate["issue_scope"] = {
            "ledger_path": ".trellis/tasks/07-04-review-gate/issue-scope-ledger.json",
            "close_issues_reviewed": [{"number": 20, "title": "Review gate"}],
        }
        gate["verification_evidence"]["agent_assignment"] = {
            "path": ".trellis/tasks/07-04-review-gate/agent-assignment.json",
            "sha256": gtt.hashlib.sha256(assignment.read_bytes()).hexdigest(),
            "size_bytes": assignment.stat().st_size,
            "modified_at": "2026-07-04T00:00:00+00:00",
            "roles": ["实现代理", "最终放行审查代理"],
            "agents_count": 1,
            "review_rounds_count": 1,
            "reuse_decisions_count": 0,
            "task": ".trellis/tasks/07-04-review-gate",
        }
        gate["verification_evidence"]["review_reports"] = self.review_reports_summary_for_assignment(assignment)
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        archived_task_dir = self.root / ".trellis/tasks/archive/2026-07/07-04-review-gate"
        archived_task_dir.mkdir(parents=True)
        for name in [
            "task.json",
            "issue-scope-ledger.json",
            "review.md",
            "agent-assignment.json",
            "review-gate.json",
        ]:
            (archived_task_dir / name).write_bytes((self.task_dir / name).read_bytes())
        archived_reports_dir = archived_task_dir / "reviews"
        archived_reports_dir.mkdir()
        for report in sorted((self.task_dir / "reviews").glob("*.md")):
            (archived_reports_dir / report.name).write_bytes(report.read_bytes())
        review_report.unlink()
        assignment.unlink()
        return archived_task_dir

    def test_validate_review_gate_rejects_reviewer_only_passed_gate(self) -> None:
        self.write_gate(review_report=None)
        with mock.patch.object(gtt, "current_head", return_value="abc123"):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("review_report" in error for error in errors))

    def test_validate_review_gate_rejects_missing_review_source(self) -> None:
        self.write_gate(review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["verification_evidence"].pop("review_source")
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with mock.patch.object(gtt, "current_head", return_value="abc123"):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("review_source" in error for error in errors))

    def test_validate_review_gate_rejects_missing_agent_assignment_summary(self) -> None:
        self.write_gate(review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["findings"] = []
        gate["conclusion"]["findings_count"] = 0
        gate["conclusion"]["blocking_findings_count"] = 0
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with mock.patch.object(gtt, "current_head", return_value="abc123"):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("agent_assignment" in error for error in errors))

    def test_validate_review_gate_rejects_passed_gate_with_findings(self) -> None:
        self.write_gate(review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["findings"] = [
            {
                "priority": "P3",
                "message": "P3 也必须阻断。",
                "path": "trellis/workflows/guru-team/workflow.md",
            }
        ]
        gate["conclusion"]["findings_count"] = 1
        gate["conclusion"]["blocking_findings_count"] = 1
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with mock.patch.object(gtt, "current_head", return_value="abc123"):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("findings[] 非空" in error for error in errors))
        self.assertTrue(any("findings_count=1" in error for error in errors))
        self.assertTrue(any("blocking_findings_count=1" in error for error in errors))

    def test_validate_review_gate_rejects_passed_gate_with_nonzero_finding_count(self) -> None:
        self.write_gate(review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["findings"] = []
        gate["conclusion"]["findings_count"] = 1
        gate["conclusion"]["blocking_findings_count"] = 0
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with mock.patch.object(gtt, "current_head", return_value="abc123"):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("findings_count=1" in error for error in errors))
        self.assertTrue(any("与 findings[] 数量 0 不一致" in error for error in errors))

    def test_validate_review_gate_accepts_zero_finding_counts(self) -> None:
        self.write_gate(review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["findings"] = []
        gate["conclusion"]["findings_count"] = 0
        gate["conclusion"]["blocking_findings_count"] = 0
        self.add_assignment_evidence_to_gate(gate)
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with (
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_object_exists", return_value=True),
        ):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertEqual(errors, [])

    def test_validate_review_gate_accepts_archived_task_with_active_artifact_paths(self) -> None:
        archived_task_dir = self.write_archived_gate_with_active_paths()
        with (
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_object_exists", return_value=True),
        ):
            _, _, errors = gtt.validate_review_gate(self.root, archived_task_dir, gtt.DEFAULTS, False)

        self.assertEqual(errors, [])

    def test_migrate_review_gate_for_archived_task_rewrites_task_local_paths(self) -> None:
        archived_task_dir = self.write_archived_gate_with_active_paths()
        migration = gtt.migrate_review_gate_for_archived_task(self.root, archived_task_dir, gtt.DEFAULTS)
        gate = gtt.read_json(archived_task_dir / "review-gate.json")
        archived_task = ".trellis/tasks/archive/2026-07/07-04-review-gate"

        self.assertTrue(migration["migrated"])
        self.assertEqual(gate["task_dir"], archived_task)
        self.assertEqual(gate["issue_scope"]["ledger_path"], f"{archived_task}/issue-scope-ledger.json")
        self.assertEqual(gate["verification_evidence"]["review_report"]["path"], f"{archived_task}/review.md")
        self.assertEqual(gate["verification_evidence"]["agent_assignment"]["path"], f"{archived_task}/agent-assignment.json")
        self.assertEqual(gate["verification_evidence"]["agent_assignment"]["task"], archived_task)
        self.assertEqual(gate["verification_evidence"]["review_reports"][0]["path"], f"{archived_task}/reviews/round-001-final-release.md")

    def test_validate_review_gate_rejects_main_session_reviewer(self) -> None:
        self.write_gate(review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["verification_evidence"]["reviewer"] = "codex-main-session"
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with mock.patch.object(gtt, "current_head", return_value="abc123"):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("main-session" in error for error in errors))

    def test_validate_review_gate_requires_modified_at(self) -> None:
        report = self.valid_report()
        report.pop("modified_at")
        self.write_gate(review_report=report)
        with mock.patch.object(gtt, "current_head", return_value="abc123"):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertIn("Branch Review Gate review_report 缺少 modified_at。", errors)

    def test_validate_review_gate_rejects_stale_review_report_digest(self) -> None:
        report = self.valid_report()
        report["sha256"] = "0" * 64
        report["size_bytes"] = int(report["size_bytes"]) + 1
        self.write_gate(review_report=report)
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["findings"] = []
        gate["conclusion"]["findings_count"] = 0
        gate["conclusion"]["blocking_findings_count"] = 0
        self.add_assignment_evidence_to_gate(gate)
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with (
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_object_exists", return_value=True),
        ):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("review_report artifact 已过期" in error and "sha256" in error for error in errors))
        self.assertTrue(any("review_report artifact 已过期" in error and "size_bytes" in error for error in errors))

    def test_validate_review_gate_rejects_final_rollup_english_template_heading(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text(
            "# Follow-up Candidates\n\n- reviews/round-001-final-release.md\n",
            encoding="utf-8",
        )
        self.write_gate(review_report=gtt.file_digest(self.root, review_report))
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["findings"] = []
        gate["conclusion"]["findings_count"] = 0
        gate["conclusion"]["blocking_findings_count"] = 0
        self.add_assignment_evidence_to_gate(gate)
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with (
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_object_exists", return_value=True),
        ):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("Follow-up Candidates" in error for error in errors))

    def test_validate_review_gate_accepts_agent_assignment_summary(self) -> None:
        self.write_gate(review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        self.add_assignment_evidence_to_gate(gate)
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with (
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_object_exists", return_value=True),
        ):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertEqual(errors, [])

    def test_validate_review_gate_rejects_finding_owner_as_final_reviewer(self) -> None:
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "发现问题后可继续闭环确认，但不能最终放行。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "同一 agent 只确认上一轮 finding 是否修复。",
                    "reuse_decision": "reuse-for-closure",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "错误示例：复用 finding owner 作为最终放行。",
                    "reuse_decision": "new-agent",
                },
            ]
        )
        self.write_gate(review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["verification_evidence"]["agent_assignment"] = {
            "path": ".trellis/tasks/07-04-review-gate/agent-assignment.json",
            "sha256": gtt.hashlib.sha256(assignment.read_bytes()).hexdigest(),
            "size_bytes": assignment.stat().st_size,
            "modified_at": "2026-07-04T00:00:00+00:00",
            "roles": ["问题发现审查代理", "问题闭环审查代理", "最终放行审查代理"],
            "agents_count": 0,
            "review_rounds_count": 3,
            "reuse_decisions_count": 0,
        }
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with (
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_object_exists", return_value=True),
        ):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("不能作为最终放行审查代理" in error for error in errors))

    def test_validate_review_gate_rejects_missing_closure_round_before_final(self) -> None:
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "发现问题后必须先由同 agent 闭环确认。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "错误示例：未经过 finding owner 闭环就最终放行。",
                    "reuse_decision": "new-agent",
                },
            ]
        )
        self.write_gate(review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["verification_evidence"]["agent_assignment"] = {
            "path": ".trellis/tasks/07-04-review-gate/agent-assignment.json",
            "sha256": gtt.hashlib.sha256(assignment.read_bytes()).hexdigest(),
            "size_bytes": assignment.stat().st_size,
            "modified_at": "2026-07-04T00:00:00+00:00",
            "roles": ["问题发现审查代理", "最终放行审查代理"],
            "agents_count": 0,
            "review_rounds_count": 2,
            "reuse_decisions_count": 0,
        }
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with (
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_object_exists", return_value=True),
        ):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("问题闭环审查代理" in error for error in errors))

    def test_validate_review_gate_rejects_duplicate_final_round_number(self) -> None:
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "问题发现审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "发现问题后必须先由同 agent 闭环确认。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 2,
                    "logical_role": "问题闭环审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "同一 agent 只确认上一轮 finding 是否修复。",
                    "reuse_decision": "reuse-for-closure",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理一",
                    "reviewed_head": "abc123",
                    "findings_count": 0,
                    "reuse_policy": "fresh final reviewer 完整审查当前 diff。",
                    "reuse_decision": "new-agent",
                },
                {
                    "round": 3,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-a",
                    "platform_nickname": "发现代理",
                    "reviewed_head": "abc123",
                    "findings_count": 1,
                    "reuse_policy": "错误示例：重复 round 让最后一轮 final 有歧义。",
                    "reuse_decision": "new-agent",
                },
            ]
        )
        self.write_gate(review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["verification_evidence"]["agent_assignment"] = {
            "path": ".trellis/tasks/07-04-review-gate/agent-assignment.json",
            "sha256": gtt.hashlib.sha256(assignment.read_bytes()).hexdigest(),
            "size_bytes": assignment.stat().st_size,
            "modified_at": "2026-07-04T00:00:00+00:00",
            "roles": ["问题发现审查代理", "问题闭环审查代理", "最终放行审查代理"],
            "agents_count": 0,
            "review_rounds_count": 4,
            "reuse_decisions_count": 0,
        }
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with (
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_object_exists", return_value=True),
        ):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("round 3 重复" in error for error in errors))
        self.assertTrue(any("唯一最后一轮" in error for error in errors))

    def test_validate_review_gate_rejects_non_task_local_agent_assignment(self) -> None:
        outside = self.root / "agent-assignment.json"
        outside.write_text(gtt.json.dumps(gtt.read_json(self.write_agent_assignment()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.write_gate(review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["verification_evidence"]["agent_assignment"] = {
            "path": "agent-assignment.json",
            "sha256": gtt.hashlib.sha256(outside.read_bytes()).hexdigest(),
            "size_bytes": outside.stat().st_size,
            "modified_at": "2026-07-04T00:00:00+00:00",
            "roles": ["实现代理"],
        }
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with mock.patch.object(gtt, "current_head", return_value="abc123"):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("task-local" in error for error in errors))

    def test_validate_review_gate_accepts_metadata_only_tail_when_allowed(self) -> None:
        assignment = self.write_agent_assignment(
            [
                {
                    "round": 1,
                    "logical_role": "最终放行审查代理",
                    "agent_id": "agent-b",
                    "platform_nickname": "最终代理",
                    "reviewed_head": "old123",
                    "findings_count": 0,
                    "reuse_policy": "fresh final reviewer 审查 gate 记录的代码 HEAD。",
                    "reuse_decision": "new-agent",
                }
            ]
        )
        self.write_gate(head="old123", review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["verification_evidence"]["agent_assignment"] = {
            "path": ".trellis/tasks/07-04-review-gate/agent-assignment.json",
            "sha256": gtt.hashlib.sha256(assignment.read_bytes()).hexdigest(),
            "size_bytes": assignment.stat().st_size,
            "modified_at": "2026-07-04T00:00:00+00:00",
            "roles": ["最终放行审查代理"],
            "agents_count": 1,
            "review_rounds_count": 1,
            "reuse_decisions_count": 0,
        }
        gate["verification_evidence"]["review_reports"] = self.review_reports_summary_for_assignment(assignment)
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with (
            mock.patch.object(gtt, "current_head", return_value="new123"),
            mock.patch.object(gtt, "git_object_exists", return_value=True),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(gtt, "metadata_only_since", return_value=(True, [".trellis/tasks/archive/07-04-review-gate/task.json"])),
        ):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, True)

        self.assertEqual(errors, [])

    def test_validate_review_gate_rejects_non_metadata_tail(self) -> None:
        self.write_gate(head="old123", review_report=self.valid_report())
        with (
            mock.patch.object(gtt, "current_head", return_value="new123"),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
            mock.patch.object(gtt, "metadata_only_since", return_value=(False, ["trellis/workflows/guru-team/workflow.md"])),
        ):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, True)

        self.assertTrue(any("非 Trellis metadata" in error for error in errors))


class AgentAssignmentArtifactTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.task_dir = self.root / ".trellis/tasks/07-05-agent-assignment"
        self.task_dir.mkdir(parents=True)
        (self.root / ".trellis/guru-team").mkdir(parents=True)
        (self.root / ".git").mkdir()
        (self.task_dir / "task.json").write_text(
            '{"title":"Agent assignment","base_branch":"main"}\n',
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def patch_assignment_command(self) -> list[mock._patch]:
        return [
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_start_context", return_value={
                "workspace_mode": "worktree",
                "workspace_path": str(self.root),
                "task_dir": ".trellis/tasks/07-05-agent-assignment",
                "preflight": {"current_checkout": str(self.root)},
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_object_exists", return_value=True),
        ]

    def write_raw_review_report(self, name: str = "round-001-problem-finding.md") -> Path:
        reports_dir = self.task_dir / "reviews"
        reports_dir.mkdir(parents=True, exist_ok=True)
        path = reports_dir / name
        path.write_text("# Raw Review\n\n问题发现审查代理 raw evidence。\n", encoding="utf-8")
        return path

    def test_record_agent_assignment_writes_agents_entry(self) -> None:
        patches = self.patch_assignment_command()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_record_agent_assignment(assignment_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        artifact = self.task_dir / "agent-assignment.json"
        self.assertTrue(artifact.exists())
        recorded = gtt.read_json(artifact)
        self.assertEqual(payload["recorded"]["logical_role"], "实现代理")
        self.assertEqual(recorded["task"], ".trellis/tasks/07-05-agent-assignment")
        self.assertEqual(recorded["head"], "abc123")
        self.assertEqual(recorded["agents"][0]["platform_nickname"], "Gibbs")

    def test_record_agent_assignment_writes_review_round(self) -> None:
        raw_report = self.write_raw_review_report()
        patches = self.patch_assignment_command()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_agent_assignment(assignment_args())
            payload = gtt.cmd_record_agent_assignment(
                assignment_args(
                    logical_role="问题发现审查代理",
                    review_round=1,
                    findings_count=2,
                    reuse_policy="问题发现代理可继续闭环复查，但不能作为最终放行审查代理。",
                    reuse_decision="reuse-for-closure",
                    review_round_report=str(raw_report),
                    reason=None,
                )
            )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        recorded = gtt.read_json(self.task_dir / "agent-assignment.json")
        self.assertEqual(payload["recorded"]["round"], 1)
        self.assertEqual(recorded["review_rounds"][0]["logical_role"], "问题发现审查代理")
        self.assertEqual(recorded["review_rounds"][0]["findings_count"], 2)
        self.assertEqual(recorded["review_rounds"][0]["review_report_path"], ".trellis/tasks/07-05-agent-assignment/reviews/round-001-problem-finding.md")
        self.assertEqual(recorded["review_rounds"][0]["review_report_sha256"], gtt.hashlib.sha256(raw_report.read_bytes()).hexdigest())

    def test_record_agent_assignment_review_round_requires_raw_report(self) -> None:
        patches = self.patch_assignment_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_record_agent_assignment(
                    assignment_args(
                        logical_role="问题发现审查代理",
                        review_round=1,
                        findings_count=1,
                        reuse_policy="问题发现代理可继续闭环复查，但不能作为最终放行审查代理。",
                        reuse_decision="new-agent",
                        reason=None,
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertIn("--review-round-report", str(raised.exception))

    def test_record_agent_assignment_status_event_fails_closed(self) -> None:
        patches = self.patch_assignment_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_record_agent_assignment(
                    assignment_args(
                        status_event="wait-timeout",
                        decision="continue-waiting",
                        reason="等待窗口 timeout，但最近仍有输出和工作区变化，继续等待。",
                        last_observed_progress_at="2026-07-07T00:00:00Z",
                        workspace_evidence="git diff 仍在变化。",
                        running_command_evidence="验证命令仍在运行。",
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("record-subagent-liveness-event.sh", str(raised.exception))
        self.assertFalse((self.task_dir / "agent-assignment.json").exists())

    def test_record_agent_assignment_rejects_terminated_unfinished_without_evidence(self) -> None:
        patches = self.patch_assignment_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_record_agent_assignment(
                    assignment_args(
                        status_event="terminated-unfinished",
                        decision="terminate-unfinished",
                        reason="缺少证据的终止记录。",
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("record-subagent-liveness-event.sh", str(raised.exception))

    def test_check_agent_assignment_rejects_invalid_status_event_enum(self) -> None:
        artifact = self.task_dir / "agent-assignment.json"
        artifact.write_text(
            gtt.json.dumps(
                {
                    "schema_version": "1.0",
                    "task": ".trellis/tasks/07-05-agent-assignment",
                    "head": "abc123",
                    "agents": [],
                    "review_rounds": [],
                    "reuse_decisions": [],
                    "status_events": [
                        {
                            "event": "timeout",
                            "logical_role": "实现代理",
                            "agent_id": "agent-a",
                            "platform_nickname": "实现代理",
                            "head": "abc123",
                            "observed_at": "2026-07-07T00:00:00Z",
                            "last_observed_progress_at": "",
                            "workspace_evidence": "",
                            "running_command_evidence": "",
                            "decision": "continue-waiting",
                            "reason": "非法事件枚举。",
                            "handoff_summary": "",
                        }
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        patches = self.patch_assignment_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_agent_assignment(
                    argparse.Namespace(
                        root=None,
                        json=True,
                        task=None,
                        agent_assignment=None,
                        require_current_head=False,
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("status_events[0].event 非法" in error for error in raised.exception.payload["errors"]))

    def test_check_agent_assignment_rejects_stale_head_when_required(self) -> None:
        artifact = self.task_dir / "agent-assignment.json"
        artifact.write_text(
            gtt.json.dumps(
                {
                    "schema_version": "1.0",
                    "task": ".trellis/tasks/07-05-agent-assignment",
                    "head": "old123",
                    "agents": [],
                    "review_rounds": [],
                    "reuse_decisions": [],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        patches = self.patch_assignment_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_agent_assignment(
                    argparse.Namespace(
                        root=None,
                        json=True,
                        task=None,
                        agent_assignment=None,
                        require_current_head=True,
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertTrue(any("当前 HEAD" in error for error in raised.exception.payload["errors"]))

    def test_check_agent_assignment_rejects_non_object_json(self) -> None:
        artifact = self.task_dir / "agent-assignment.json"
        artifact.write_text("[]\n", encoding="utf-8")
        patches = self.patch_assignment_command()
        for patcher in patches:
            patcher.start()
        try:
            with self.assertRaises(gtt.WorkflowError) as raised:
                gtt.cmd_check_agent_assignment(
                    argparse.Namespace(
                        root=None,
                        json=True,
                        task=None,
                        agent_assignment=None,
                        require_current_head=False,
                    )
                )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("JSON root must be an object", str(raised.exception))


class SubagentLivenessStateMachineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / "source-checkout"
        self.source.mkdir()
        self.task_dir = self.root / ".trellis/tasks/07-05-agent-assignment"
        self.task_dir.mkdir(parents=True)
        (self.root / ".trellis/guru-team").mkdir(parents=True)
        (self.root / ".git").mkdir()
        (self.source / ".git").mkdir()
        (self.task_dir / "task.json").write_text('{"title":"Liveness","base_branch":"main"}\n', encoding="utf-8")
        self.machine_state = {
            "task_head": "abc123",
            "task_content_status_digest": "task-status-a",
            "task_content_diff_stat_digest": "task-diff-a",
            "task_content_max_mtime": "2026-07-07T00:00:00Z",
            "source_head": "source123",
            "source_status_digest": "source-status-a",
            "source_diff_stat_digest": "source-diff-a",
            "source_max_mtime": "2026-07-07T00:00:00Z",
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def patch_liveness_command(self) -> list[mock._patch]:
        return [
            mock.patch.object(gtt, "repo_root", side_effect=lambda path: self.source if str(path).endswith("source-checkout") else self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_start_context", return_value={
                "workspace_mode": "worktree",
                "workspace_path": str(self.root),
                "task_dir": ".trellis/tasks/07-05-agent-assignment",
                "preflight": {"current_checkout": str(self.source)},
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "current_head", side_effect=lambda root: "source123" if root == self.source else "abc123"),
            mock.patch.object(gtt, "git_object_exists", return_value=True),
            mock.patch.object(gtt, "collect_liveness_snapshot", side_effect=self.snapshot),
        ]

    def snapshot(self, root: Path, task_dir: Path, source_repo: Path, payload: dict[str, object], agent_id: str, captured_at: str | None = None) -> dict[str, object]:
        return {
            "captured_at": captured_at or "2026-07-07T00:00:00Z",
            **self.machine_state,
            **gtt.progress_events_digest(payload, agent_id),
        }

    def run_with_patches(self, callback):
        patches = self.patch_liveness_command()
        for patcher in patches:
            patcher.start()
        try:
            return callback()
        finally:
            for patcher in reversed(patches):
                patcher.stop()

    def record(self, **overrides: object) -> dict[str, object]:
        args = liveness_event_args(source_repo=str(self.source), **overrides)
        return gtt.cmd_record_subagent_liveness_event(args)

    def check(self, **overrides: object) -> dict[str, object]:
        args = liveness_check_args(source_repo=str(self.source), **overrides)
        return gtt.cmd_check_subagent_liveness(args)

    def assign(self) -> None:
        self.record(event="assigned", observed_at="2026-07-07T00:00:00Z", evidence="分配实现代理。")

    def reset_assignment_artifact(self) -> None:
        artifact = self.task_dir / "agent-assignment.json"
        if artifact.exists():
            artifact.unlink()
        self.machine_state = {
            "task_head": "abc123",
            "task_content_status_digest": "task-status-a",
            "task_content_diff_stat_digest": "task-diff-a",
            "task_content_max_mtime": "2026-07-07T00:00:00Z",
            "source_head": "source123",
            "source_status_digest": "source-status-a",
            "source_diff_stat_digest": "source-diff-a",
            "source_max_mtime": "2026-07-07T00:00:00Z",
        }

    def test_assigned_initializes_agents_liveness_and_status_event(self) -> None:
        def scenario() -> dict[str, object]:
            return self.record(event="assigned", observed_at="2026-07-07T00:00:00Z", evidence="分配实现代理。")

        payload = self.run_with_patches(scenario)
        recorded = gtt.read_json(self.task_dir / "agent-assignment.json")
        self.assertTrue(str(payload["event_id"]).startswith("evt-"))
        self.assertEqual(recorded["schema_version"], "1.1")
        self.assertEqual(recorded["agents"][0]["assigned_at"], "2026-07-07T00:00:00Z")
        self.assertEqual(recorded["agents"][0]["assigned_head"], "abc123")
        self.assertEqual(recorded["agents"][0]["reason"], "分配实现代理。")
        self.assertEqual(recorded["status_events"][0]["event"], "assigned")
        self.assertIn("agent-a", recorded["liveness"])
        self.assertEqual(recorded["liveness"]["agent-a"]["progress_anchor_at"], "2026-07-07T00:00:00Z")

    def test_deadline_passed_without_pending_still_requires_status_request_then_allows_stale(self) -> None:
        def scenario() -> tuple[dict[str, object], dict[str, object]]:
            self.assign()
            first = self.check(checked_at="2026-07-07T00:03:01Z")
            self.record(
                event="status-requested",
                observed_at="2026-07-07T00:03:02Z",
                evidence="主会话已发送显式 status request。",
                logical_role=None,
                platform_nickname=None,
            )
            second = self.check(checked_at="2026-07-07T00:03:02Z")
            return first, second

        first, second = self.run_with_patches(scenario)
        self.assertEqual(first["decision"], "status_request_required")
        self.assertEqual(first["next_wait_ms"], 0)
        self.assertEqual(first["max_progress_silence_deadline_at"], "2026-07-07T00:03:00Z")
        self.assertEqual(second["decision"], "stale_allowed")
        self.assertEqual(second["max_progress_silence_deadline_at"], "2026-07-07T00:03:00Z")

    def test_pending_status_request_before_deadline_waits_without_repeat_ping(self) -> None:
        def scenario() -> dict[str, object]:
            self.assign()
            first = self.check(checked_at="2026-07-07T00:01:59Z")
            self.assertEqual(first["decision"], "status_request_required")
            self.record(
                event="status-requested",
                observed_at="2026-07-07T00:02:00Z",
                evidence="主会话已发送显式 status request。",
                logical_role=None,
                platform_nickname=None,
            )
            return self.check(checked_at="2026-07-07T00:02:01Z")

        payload = self.run_with_patches(scenario)
        self.assertEqual(payload["decision"], "continue_waiting_no_repeat_ping")
        self.assertLessEqual(payload["next_wait_ms"], 59000)

    def test_recorded_progress_refreshes_anchor_and_clears_pending_request(self) -> None:
        def scenario() -> dict[str, object]:
            self.assign()
            first = self.check(checked_at="2026-07-07T00:00:19Z")
            self.assertEqual(first["decision"], "status_request_required")
            self.record(
                event="status-requested",
                observed_at="2026-07-07T00:00:20Z",
                evidence="主会话已发送显式 status request。",
                logical_role=None,
                platform_nickname=None,
            )
            self.record(
                event="explicit-message-observed",
                observed_at="2026-07-07T00:01:00Z",
                evidence="实现代理回复正在迁移改动到 task worktree。",
                logical_role=None,
                platform_nickname=None,
            )
            return self.check(checked_at="2026-07-07T00:01:01Z")

        payload = self.run_with_patches(scenario)
        recorded = gtt.read_json(self.task_dir / "agent-assignment.json")
        self.assertEqual(payload["decision"], "progress_observed")
        self.assertEqual(payload["progress_anchor_at"], "2026-07-07T00:01:00Z")
        self.assertIsNone(recorded["liveness"]["agent-a"]["pending_status_request_at"])
        self.assertEqual(payload["progress_sources"][0]["source"], "status_event")

    def test_source_snapshot_change_outputs_workspace_boundary_progress(self) -> None:
        def scenario() -> dict[str, object]:
            self.assign()
            self.machine_state["source_status_digest"] = "source-status-b"
            return self.check(checked_at="2026-07-07T00:01:00Z")

        payload = self.run_with_patches(scenario)
        self.assertEqual(payload["decision"], "workspace_boundary_violation_progress")
        self.assertEqual(payload["progress_sources"][0]["source"], "source_status")

    def test_task_machine_snapshot_changes_are_progress_observed(self) -> None:
        cases = [
            ("task_head", "task456", "task_head"),
            ("task_content_status_digest", "task-status-b", "task_status"),
            ("task_content_diff_stat_digest", "task-diff-b", "task_diff_stat"),
            ("task_content_max_mtime", "2026-07-07T00:00:30Z", "task_mtime"),
        ]
        for field, value, source_kind in cases:
            with self.subTest(field=field):
                def scenario() -> dict[str, object]:
                    self.reset_assignment_artifact()
                    self.assign()
                    self.machine_state[field] = value
                    return self.check(checked_at="2026-07-07T00:01:00Z")

                payload = self.run_with_patches(scenario)
                self.assertEqual(payload["decision"], "progress_observed")
                self.assertEqual(payload["progress_anchor_at"], "2026-07-07T00:01:00Z")
                self.assertEqual(payload["progress_sources"][0]["source"], source_kind)

    def test_source_machine_snapshot_changes_are_workspace_boundary_progress(self) -> None:
        cases = [
            ("source_head", "source456", "source_head"),
            ("source_status_digest", "source-status-b", "source_status"),
            ("source_diff_stat_digest", "source-diff-b", "source_diff_stat"),
            ("source_max_mtime", "2026-07-07T00:00:30Z", "source_mtime"),
        ]
        for field, value, source_kind in cases:
            with self.subTest(field=field):
                def scenario() -> dict[str, object]:
                    self.reset_assignment_artifact()
                    self.assign()
                    self.machine_state[field] = value
                    return self.check(checked_at="2026-07-07T00:01:00Z")

                payload = self.run_with_patches(scenario)
                self.assertEqual(payload["decision"], "workspace_boundary_violation_progress")
                self.assertEqual(payload["progress_anchor_at"], "2026-07-07T00:01:00Z")
                self.assertEqual(payload["progress_sources"][0]["source"], source_kind)

    def test_recorded_progress_event_types_are_progress_observed(self) -> None:
        for event_name in sorted(gtt.AGENT_PROGRESS_EVENTS):
            with self.subTest(event=event_name):
                def scenario() -> dict[str, object]:
                    self.reset_assignment_artifact()
                    self.assign()
                    self.record(
                        event=event_name,
                        observed_at="2026-07-07T00:01:00Z",
                        evidence=f"{event_name} 公开进展。",
                        logical_role=None,
                        platform_nickname=None,
                    )
                    return self.check(checked_at="2026-07-07T00:01:01Z")

                payload = self.run_with_patches(scenario)
                self.assertEqual(payload["decision"], "progress_observed")
                self.assertEqual(payload["progress_anchor_at"], "2026-07-07T00:01:00Z")
                self.assertEqual(payload["progress_sources"][0]["source"], "status_event")
                self.assertEqual(payload["progress_sources"][0]["event"], event_name)

    def test_stale_assessed_rejects_new_progress_after_stale_allowed(self) -> None:
        def scenario() -> None:
            self.assign()
            first = self.check(checked_at="2026-07-07T00:00:09Z")
            self.assertEqual(first["decision"], "status_request_required")
            self.record(event="status-requested", observed_at="2026-07-07T00:00:10Z", evidence="已发送 status request。", logical_role=None, platform_nickname=None)
            self.check(checked_at="2026-07-07T00:03:01Z")
            self.record(event="tool-activity-observed", observed_at="2026-07-07T00:03:02Z", evidence="stale 写入前观察到 tool activity。", logical_role=None, platform_nickname=None)
            with self.assertRaises(gtt.WorkflowError) as raised:
                self.record(event="stale-assessed", observed_at="2026-07-07T00:03:03Z", evidence="尝试基于旧 stale_allowed 写入 stale。", logical_role=None, platform_nickname=None)
            self.assertIn("rerun check-subagent-liveness", str(raised.exception))

        self.run_with_patches(scenario)

    def test_stale_assessed_rejects_task_or_source_snapshot_drift_after_stale_allowed(self) -> None:
        cases = [
            ("task_content_status_digest", "task-status-b"),
            ("source_status_digest", "source-status-b"),
        ]
        for field, value in cases:
            with self.subTest(field=field):
                def scenario() -> None:
                    self.reset_assignment_artifact()
                    self.assign()
                    first = self.check(checked_at="2026-07-07T00:00:09Z")
                    self.assertEqual(first["decision"], "status_request_required")
                    self.record(event="status-requested", observed_at="2026-07-07T00:00:10Z", evidence="已发送 status request。", logical_role=None, platform_nickname=None)
                    self.check(checked_at="2026-07-07T00:03:01Z")
                    self.machine_state[field] = value
                    with self.assertRaises(gtt.WorkflowError) as raised:
                        self.record(event="stale-assessed", observed_at="2026-07-07T00:03:03Z", evidence="尝试基于旧 stale_allowed 写入 stale。", logical_role=None, platform_nickname=None)
                    self.assertIn("rerun check-subagent-liveness", str(raised.exception))

                self.run_with_patches(scenario)

    def test_stale_cutover_requires_replacement_completion_and_rejects_resume(self) -> None:
        def scenario() -> list[str]:
            self.assign()
            first = self.check(checked_at="2026-07-07T00:00:09Z")
            self.assertEqual(first["decision"], "status_request_required")
            self.record(event="status-requested", observed_at="2026-07-07T00:00:10Z", evidence="已发送 status request。", logical_role=None, platform_nickname=None)
            self.check(checked_at="2026-07-07T00:03:01Z")
            stale = self.record(event="stale-assessed", observed_at="2026-07-07T00:03:02Z", evidence="checker 已输出 stale_allowed。", logical_role=None, platform_nickname=None)
            with self.assertRaises(gtt.WorkflowError):
                self.record(event="resume-same-agent", observed_at="2026-07-07T00:03:03Z", evidence="错误尝试恢复 stale agent。", predecessor_event_id=stale["event_id"], handoff_summary="继续范围、已知输出、剩余工作和 gate blockers。", logical_role=None, platform_nickname=None)
            self.record(
                event="terminated-unfinished",
                observed_at="2026-07-07T00:03:04Z",
                evidence="stale cutover 停止接受 predecessor 输出。",
                termination_reason="stale_cutover",
                termination_source_event_id=stale["event_id"],
                handoff_summary="predecessor output、当前 diff、剩余工作和 gate blockers。",
                logical_role=None,
                platform_nickname=None,
            )
            self.record(event="assigned", agent_id="agent-b", observed_at="2026-07-07T00:03:05Z", evidence="分配 replacement。", logical_role="实现代理", platform_nickname="Implement B")
            self.record(
                event="replacement-started",
                agent_id="agent-b",
                observed_at="2026-07-07T00:03:06Z",
                evidence="replacement 已接收 handoff。",
                predecessor_agent_id="agent-a",
                predecessor_event_id=stale["event_id"],
                replacement_reason="max_progress_silence_exceeded",
                handoff_summary="predecessor output、当前 diff、task artifacts、剩余工作和 gate blockers。",
                logical_role=None,
                platform_nickname=None,
            )
            incomplete = gtt.validate_agent_assignment(self.root, self.task_dir)[2]
            self.record(event="completed", agent_id="agent-b", observed_at="2026-07-07T00:10:00Z", evidence="replacement 完成实现。", logical_role=None, platform_nickname=None)
            complete = gtt.validate_agent_assignment(self.root, self.task_dir)[2]
            return incomplete, complete

        incomplete, complete = self.run_with_patches(scenario)
        self.assertTrue(any("replacement chain" in error or "completed" in error for error in incomplete))
        self.assertEqual(complete, [])

    def test_status_request_failed_does_not_set_pending_or_allow_stale(self) -> None:
        def scenario() -> tuple[dict[str, object], dict[str, object]]:
            self.assign()
            decision = self.check(checked_at="2026-07-07T00:03:00Z")
            self.assertEqual(decision["decision"], "status_request_required")
            self.record(event="status-request-failed", observed_at="2026-07-07T00:03:01Z", evidence="平台 status request 发送失败。", logical_role=None, platform_nickname=None)
            first = self.check(checked_at="2026-07-07T00:03:02Z")
            second = self.check(checked_at="2026-07-07T00:04:00Z")
            return first, second

        first, second = self.run_with_patches(scenario)
        self.assertEqual(first["decision"], "status_request_required")
        self.assertEqual(second["decision"], "status_request_required")

    def test_status_request_events_require_checker_authorization(self) -> None:
        def scenario() -> None:
            self.assign()
            with self.assertRaises(gtt.WorkflowError) as raised:
                self.record(event="status-requested", observed_at="2026-07-07T00:00:10Z", evidence="未先运行 checker 就记录 status request。", logical_role=None, platform_nickname=None)
            self.assertIn("status_request_required", str(raised.exception))

        self.run_with_patches(scenario)

    def test_liveness_timestamps_are_normalized_to_utc_z_and_non_utc_is_rejected(self) -> None:
        def scenario() -> None:
            self.record(event="assigned", observed_at="2026-07-07T00:00:00+00:00", evidence="分配实现代理。")
            recorded = gtt.read_json(self.task_dir / "agent-assignment.json")
            self.assertEqual(recorded["agents"][0]["assigned_at"], "2026-07-07T00:00:00Z")
            with self.assertRaises(gtt.WorkflowError) as raised:
                self.record(event="explicit-message-observed", observed_at="2026-07-07T08:00:01+08:00", evidence="非 UTC 时间不应被接受。", logical_role=None, platform_nickname=None)
            self.assertIn("must be UTC", str(raised.exception))

        self.run_with_patches(scenario)

    def test_non_handoff_events_reject_handoff_summary(self) -> None:
        def scenario() -> None:
            self.assign()
            with self.assertRaises(gtt.WorkflowError) as raised:
                self.record(
                    event="explicit-message-observed",
                    observed_at="2026-07-07T00:00:10Z",
                    evidence="实现代理公开回复。",
                    handoff_summary="progress event 不应携带 handoff summary。",
                    logical_role=None,
                    platform_nickname=None,
                )
            self.assertIn("handoff_summary", str(raised.exception))

        self.run_with_patches(scenario)

    def test_terminated_unfinished_requires_structured_reason(self) -> None:
        def scenario() -> None:
            self.assign()
            with self.assertRaises(gtt.WorkflowError) as raised:
                self.record(
                    event="terminated-unfinished",
                    observed_at="2026-07-07T00:01:00Z",
                    evidence="缺少结构化终止原因。",
                    handoff_summary="predecessor output、当前 diff、剩余工作和 gate blockers。",
                    logical_role=None,
                    platform_nickname=None,
                )
            self.assertIn("--termination-reason", str(raised.exception))

        self.run_with_patches(scenario)

    def test_replacement_started_requires_predecessor_event_and_matching_reason(self) -> None:
        def scenario() -> None:
            self.assign()
            failed = self.record(event="failed", observed_at="2026-07-07T00:01:00Z", evidence="实现代理失败且未完成。", logical_role=None, platform_nickname=None)
            with self.assertRaises(gtt.WorkflowError) as same_agent:
                self.record(
                    event="replacement-started",
                    observed_at="2026-07-07T00:01:01Z",
                    evidence="错误地把同一 agent 记录为 replacement。",
                    predecessor_agent_id="agent-a",
                    predecessor_event_id=failed["event_id"],
                    replacement_reason="terminal_failed_incomplete",
                    handoff_summary="predecessor output、当前 diff、task artifacts、剩余工作和 gate blockers。",
                    logical_role=None,
                    platform_nickname=None,
                )
            self.assertIn("different replacement agent", str(same_agent.exception))
            self.record(event="assigned", agent_id="agent-b", observed_at="2026-07-07T00:01:01Z", evidence="分配 replacement。", logical_role="实现代理", platform_nickname="Implement B")
            with self.assertRaises(gtt.WorkflowError) as missing:
                self.record(
                    event="replacement-started",
                    agent_id="agent-b",
                    observed_at="2026-07-07T00:01:02Z",
                    evidence="replacement 缺少 predecessor_event_id。",
                    predecessor_agent_id="agent-a",
                    replacement_reason="terminal_failed_incomplete",
                    handoff_summary="predecessor output、当前 diff、task artifacts、剩余工作和 gate blockers。",
                    logical_role=None,
                    platform_nickname=None,
                )
            self.assertIn("--predecessor-event-id", str(missing.exception))
            with self.assertRaises(gtt.WorkflowError) as mismatch:
                self.record(
                    event="replacement-started",
                    agent_id="agent-b",
                    observed_at="2026-07-07T00:01:03Z",
                    evidence="replacement reason 与 failed 证据不匹配。",
                    predecessor_agent_id="agent-a",
                    predecessor_event_id=failed["event_id"],
                    replacement_reason="max_progress_silence_exceeded",
                    handoff_summary="predecessor output、当前 diff、task artifacts、剩余工作和 gate blockers。",
                    logical_role=None,
                    platform_nickname=None,
                )
            self.assertIn("terminal_failed_incomplete", str(mismatch.exception))

        self.run_with_patches(scenario)

    def test_replacement_failure_requires_additional_recovery_before_pass(self) -> None:
        def scenario() -> tuple[list[str], list[str]]:
            self.assign()
            unfinished = self.record(
                event="terminated-unfinished",
                observed_at="2026-07-07T00:01:00Z",
                evidence="平台手动终止未完成实现代理。",
                termination_reason="manual_or_platform_terminated_unfinished",
                handoff_summary="predecessor output、当前 diff、剩余工作和 gate blockers。",
                logical_role=None,
                platform_nickname=None,
            )
            self.record(event="assigned", agent_id="agent-b", observed_at="2026-07-07T00:01:01Z", evidence="分配第一任 replacement。", logical_role="实现代理", platform_nickname="Implement B")
            self.record(
                event="replacement-started",
                agent_id="agent-b",
                observed_at="2026-07-07T00:01:02Z",
                evidence="第一任 replacement 已接收 handoff。",
                predecessor_agent_id="agent-a",
                predecessor_event_id=unfinished["event_id"],
                replacement_reason="manual_or_platform_terminated_unfinished",
                handoff_summary="predecessor output、当前 diff、task artifacts、剩余工作和 gate blockers。",
                logical_role=None,
                platform_nickname=None,
            )
            failed = self.record(event="failed", agent_id="agent-b", observed_at="2026-07-07T00:02:00Z", evidence="第一任 replacement 失败且未完成。", logical_role=None, platform_nickname=None)
            incomplete = gtt.validate_agent_assignment(self.root, self.task_dir)[2]
            self.record(event="assigned", agent_id="agent-c", observed_at="2026-07-07T00:02:01Z", evidence="分配第二任 replacement。", logical_role="实现代理", platform_nickname="Implement C")
            self.record(
                event="replacement-started",
                agent_id="agent-c",
                observed_at="2026-07-07T00:02:02Z",
                evidence="第二任 replacement 已接收 handoff。",
                predecessor_agent_id="agent-b",
                predecessor_event_id=failed["event_id"],
                replacement_reason="terminal_failed_incomplete",
                handoff_summary="predecessor output、当前 diff、task artifacts、剩余工作和 gate blockers。",
                logical_role=None,
                platform_nickname=None,
            )
            self.record(event="completed", agent_id="agent-c", observed_at="2026-07-07T00:03:00Z", evidence="第二任 replacement 完成实现。", logical_role=None, platform_nickname=None)
            complete = gtt.validate_agent_assignment(self.root, self.task_dir)[2]
            return incomplete, complete

        incomplete, complete = self.run_with_patches(scenario)
        self.assertTrue(any("failed 后缺少" in error for error in incomplete))
        self.assertEqual(complete, [])


class FinishWorkEntrypointContractTest(unittest.TestCase):
    REPO_ROOT = Path(__file__).resolve().parents[5]
    ENTRYPOINT_FILES = [
        "trellis/workflows/guru-team/workflow.md",
        ".trellis/workflow.md",
        "trellis/presets/guru-team/overlays/.agents/skills/trellis-finish-work/SKILL.md",
        "trellis/presets/guru-team/overlays/.codex/prompts/trellis-finish-work.md",
        "trellis/presets/guru-team/overlays/.codex/skills/trellis-finish-work/SKILL.md",
        "trellis/presets/guru-team/overlays/.claude/commands/trellis/finish-work.md",
        "trellis/presets/guru-team/overlays/.cursor/commands/trellis-finish-work.md",
    ]
    PUBLIC_DOC_FILES = [
        "README.md",
        "trellis/workflows/guru-team/README.md",
        "trellis/presets/guru-team/README.md",
        "docs/requirements/requirement-main.md",
    ]
    CODE_BLOCK_RE = re.compile(r"```(?:bash)?\n(.*?)```", re.DOTALL)
    BARE_FINISH_COMMAND = ".trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work"

    def finish_work_code_blocks(self, content: str) -> list[str]:
        return [
            block.strip()
            for block in self.CODE_BLOCK_RE.findall(content)
            if "finish-work.sh" in block
        ]

    def test_finish_work_entrypoints_show_reviewed_body_and_dry_run(self) -> None:
        for relpath in self.ENTRYPOINT_FILES:
            with self.subTest(path=relpath):
                content = (self.REPO_ROOT / relpath).read_text(encoding="utf-8")
                finish_blocks = self.finish_work_code_blocks(content)

                self.assertTrue(finish_blocks, f"{relpath} must show finish-work command examples")
                self.assertTrue(
                    any("--body-file" in block or "--body-artifact" in block for block in finish_blocks),
                    f"{relpath} must pass a reviewed PR body source",
                )
                self.assertTrue(
                    any("--dry-run" in block for block in finish_blocks),
                    f"{relpath} must show a dry-run readiness preview",
                )
                for block in finish_blocks:
                    normalized = "\n".join(line.rstrip() for line in block.splitlines()).strip()
                    self.assertFalse(
                        any(line.strip() == self.BARE_FINISH_COMMAND for line in block.splitlines()),
                        f"{relpath} must not keep a bare finish-work command line",
                    )
                    self.assertNotEqual(
                        normalized,
                        self.BARE_FINISH_COMMAND,
                        f"{relpath} must not keep a bare finish-work main example",
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


class HumanArtifactReviewTableContractTest(unittest.TestCase):
    REPO_ROOT = Path(__file__).resolve().parents[5]
    CONTINUE_ENTRYPOINT_FILES = [
        "trellis/workflows/guru-team/workflow.md",
        ".trellis/workflow.md",
        "trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md",
        "trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md",
        "trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md",
        "trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md",
        "trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md",
    ]
    FINISH_ENTRYPOINT_FILES = [
        "trellis/workflows/guru-team/workflow.md",
        ".trellis/workflow.md",
        "trellis/presets/guru-team/overlays/.agents/skills/trellis-finish-work/SKILL.md",
        "trellis/presets/guru-team/overlays/.codex/prompts/trellis-finish-work.md",
        "trellis/presets/guru-team/overlays/.codex/skills/trellis-finish-work/SKILL.md",
        "trellis/presets/guru-team/overlays/.claude/commands/trellis/finish-work.md",
        "trellis/presets/guru-team/overlays/.cursor/commands/trellis-finish-work.md",
    ]

    def assert_file_contains(self, relpath: str, snippets: list[str]) -> None:
        content = (self.REPO_ROOT / relpath).read_text(encoding="utf-8")
        for snippet in snippets:
            self.assertIn(snippet, content, f"{relpath} must mention {snippet!r}")

    def test_continue_entrypoints_require_markdown_artifact_review_table(self) -> None:
        snippets = [
            "resolve-human-artifacts.sh",
            "Markdown 产物 review 表",
            "`prd.md`",
            "`design.md`",
            "`implement.md`",
            "`review.md`",
            "`pr-body.md`",
        ]
        for relpath in self.CONTINUE_ENTRYPOINT_FILES:
            with self.subTest(path=relpath):
                self.assert_file_contains(relpath, snippets)

    def test_finish_entrypoints_resolve_active_then_archive_paths(self) -> None:
        snippets = [
            "resolve-human-artifacts.sh",
            "Markdown 产物 review 表",
            "active",
            "archive",
            "`prd.md`",
            "`design.md`",
            "`implement.md`",
            "`review.md`",
            "`pr-body.md`",
        ]
        for relpath in self.FINISH_ENTRYPOINT_FILES:
            with self.subTest(path=relpath):
                self.assert_file_contains(relpath, snippets)

    def test_user_facing_docs_use_pr_body_as_default_body_artifact(self) -> None:
        forbidden = "reviewed-" + "pr-body.md"
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
    START_ENTRYPOINT_FILES = [
        "trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md",
        "trellis/presets/guru-team/overlays/.codex/prompts/trellis-start.md",
        "trellis/presets/guru-team/overlays/.codex/skills/trellis-start/SKILL.md",
    ]
    CONTINUE_ENTRYPOINT_FILES = [
        "trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md",
        "trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md",
        "trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md",
        "trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md",
        "trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md",
    ]
    PUBLIC_DOC_FILES = [
        "docs/requirements/requirement-main.md",
        "docs/requirements/guru-team-trellis-flow.md",
    ]

    def assert_file_contains(self, relpath: str, snippets: list[str]) -> None:
        content = (self.REPO_ROOT / relpath).read_text(encoding="utf-8")
        for snippet in snippets:
            self.assertIn(snippet, content, f"{relpath} must mention {snippet!r}")

    def test_workflow_requires_intake_clarity_and_scope_change_gates(self) -> None:
        for relpath in self.WORKFLOW_FILES:
            with self.subTest(path=relpath):
                self.assert_file_contains(
                    relpath,
                    [
                        "intake clarity check",
                        "trellis-brainstorm",
                        "issue comment",
                        "Scope Change Gate",
                        "GitHub-visible evidence",
                        "issue-scope-ledger.json",
                    ],
                )

    def test_start_entrypoints_prompt_intake_clarity_check(self) -> None:
        for relpath in self.START_ENTRYPOINT_FILES:
            with self.subTest(path=relpath):
                self.assert_file_contains(
                    relpath,
                    [
                        "intake clarity check",
                        "trellis-brainstorm",
                        "issue body/comments",
                        "reviewed proposed issue body",
                    ],
                )

    def test_continue_entrypoints_prompt_scope_change_gate(self) -> None:
        for relpath in self.CONTINUE_ENTRYPOINT_FILES:
            with self.subTest(path=relpath):
                self.assert_file_contains(
                    relpath,
                    [
                        "Scope Change Gate",
                        "close_issues",
                        "related_issues",
                        "followup_issues",
                        "GitHub-visible issue evidence",
                    ],
                )

    def test_public_docs_describe_scope_evolution_contract(self) -> None:
        for relpath in self.PUBLIC_DOC_FILES:
            with self.subTest(path=relpath):
                self.assert_file_contains(
                    relpath,
                    [
                        "Intake clarity",
                        "trellis-brainstorm",
                        "issue-scope-ledger.json",
                    ],
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
        self.assertEqual(payload["trellis_cli_compatibility"], "0.6.5")
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


if __name__ == "__main__":
    unittest.main()

class TaskRuntimeBoundaryContractTest(unittest.TestCase):
    def build_context(self, freshness: dict[str, object]) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            task_dir = workspace / ".trellis/tasks/07-10-096-task-runtime-boundary"
            task_dir.mkdir(parents=True)
            return gtt.build_task_start_context(workspace, {
                "workspace_path": str(workspace), "source_repo": "owner/repo",
                "source_issue": {"number": 96, "url": "https://github.com/owner/repo/issues/96", "title": "Task", "created_by_workflow": False},
                "task_slug": "096-task-runtime-boundary", "task_title": "Task",
                "branch_name": "chore/096-task-runtime-boundary", "base_branch": "main",
                "workspace_slug": "096-task-runtime-boundary", "issue_scope_ledger": {},
                "duplicate_search": {"performed": False}, "naming_quality": {},
                "base_freshness": freshness,
            }, task_dir, "tester")

    def test_task_start_context_copies_fresh_base_shas(self) -> None:
        sha = "a" * 40
        context = self.build_context({"status": "fresh", "base_ref": "main", "local_head_after": sha, "remote_head": sha})
        self.assertEqual(context["base_head_sha"], sha)
        self.assertEqual(context["remote_head_sha"], sha)

    def test_task_start_context_rejects_fresh_mismatched_shas(self) -> None:
        with self.assertRaises(gtt.WorkflowError):
            self.build_context({"status": "fresh", "base_ref": "main", "local_head_after": "a" * 40, "remote_head": "b" * 40})

    def test_task_start_context_remote_only_allows_empty_local_sha(self) -> None:
        remote = "b" * 40
        context = self.build_context({"status": "remote_only", "base_ref": "main", "local_head_after": None, "remote_head": remote})
        self.assertEqual(context["base_head_sha"], "")
        self.assertEqual(context["remote_head_sha"], remote)

    def test_task_start_context_fetch_failed_allows_empty_shas(self) -> None:
        context = self.build_context({"status": "fetch_failed", "base_ref": "main", "local_head_after": None, "remote_head": None})
        self.assertEqual(context["base_head_sha"], "")
        self.assertEqual(context["remote_head_sha"], "")

    def test_task_start_context_rejects_forbidden_absolute_path(self) -> None:
        payload = {
            "schema_version": "1.0", "source_issue": {}, "source_repo": {},
            "task_slug": "096-task-runtime-boundary", "task_title": "task",
            "task_artifact_dir": ".trellis/tasks/07-10-096-task-runtime-boundary",
            "branch_name": "chore/096-task-runtime-boundary", "base_branch": "main",
            "base_ref": "main", "base_head_sha": "", "remote_head_sha": "",
            "workspace_slug": "096-task-runtime-boundary", "task_workspace_id": "096-task-runtime-boundary",
            "assignee": "tester", "actor": {"login": "tester"},
            "issue_scope_ledger_seed": {}, "intake_summary": {"duplicate_decision": {}, "naming_quality": {}, "confirmation": {"workspace_path": "/tmp/worktree"}},
        }
        with self.assertRaises(gtt.WorkflowError):
            gtt.validate_task_start_context(payload)

    def test_parallel_tasks_use_distinct_runtime_and_tracked_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first_task = root / ".trellis/tasks/07-10-096-first"
            second_task = root / ".trellis/tasks/07-10-097-second"
            first_task.mkdir(parents=True)
            second_task.mkdir(parents=True)
            self.assertNotEqual(gtt.task_start_context_path(first_task, gtt.DEFAULTS), gtt.task_start_context_path(second_task, gtt.DEFAULTS))
            self.assertNotEqual(gtt.runtime_task_path(root, gtt.DEFAULTS, "096-first"), gtt.runtime_task_path(root, gtt.DEFAULTS, "097-second"))
            self.assertNotEqual(gtt.runtime_workspace_path(root, gtt.DEFAULTS, "096-first"), gtt.runtime_workspace_path(root, gtt.DEFAULTS, "097-second"))


class ActivePublicReferenceContractTest(unittest.TestCase):
    REPO_ROOT = Path(__file__).resolve().parents[5]
    FORBIDDEN_REFERENCES = (
        "handoff.workspace_path",
        "handoff `workspace_path`",
        "task-start-context.workspace_path",
        "task_start_context.workspace_path",
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
            "reuse_decision: reuse-for-closure",
            "decision: new-agent",
            "`from_round`, `to_round`, closure `agent_id`, reviewed `head`",
            "non-empty",
            "replacement closure chain",
            "becomes a new finding owner",
            "finding owner or closure agent",
        ]:
            self.assertIn(expected, workflow_text)

        overlay_pairs = [
            (
                "trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md",
                ".agents/skills/trellis-continue/SKILL.md",
            ),
            (
                "trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md",
                ".codex/skills/trellis-continue/SKILL.md",
            ),
            (
                "trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md",
                ".codex/prompts/trellis-continue.md",
            ),
            (
                "trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md",
                ".claude/commands/trellis/continue.md",
            ),
            (
                "trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md",
                ".cursor/commands/trellis-continue.md",
            ),
        ]
        for canonical_relative, dogfood_relative in overlay_pairs:
            with self.subTest(canonical=canonical_relative, dogfood=dogfood_relative):
                canonical = root / canonical_relative
                dogfood = root / dogfood_relative
                self.assertEqual(canonical.read_bytes(), dogfood.read_bytes())
                text = canonical.read_text(encoding="utf-8")
                self.assertIn("reuse_decision: reuse-for-closure", text)
                self.assertIn("reuse_decisions[] decision=new-agent", text)
                self.assertIn("from_round", text)
                self.assertIn("to_round", text)
                self.assertIn("replacement", text)
                self.assertIn("becomes a new finding owner", text)
                self.assertIn("Neither a finding owner nor any closure agent may become final", text)
                self.assertIn("reuse_decision: new-agent", text)

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


class MarketplaceVerificationContractTest(unittest.TestCase):
    MARKETPLACE_SCHEMA = gtt.read_json(Path(__file__).resolve().parents[2] / "schemas/marketplace-verification.schema.json")

    def assert_public_schema_valid(self, payload: dict[str, Any]) -> None:
        self.assertEqual(set(payload), set(self.MARKETPLACE_SCHEMA["required"]))
        self.assertIn(payload["status"], self.MARKETPLACE_SCHEMA["properties"]["status"]["enum"])
        step_schema = self.MARKETPLACE_SCHEMA["properties"]["steps"]["items"]
        for step in payload["steps"]:
            self.assertTrue(set(step_schema["required"]).issubset(step))
        self.assertEqual(set(payload["assets"]), set(self.MARKETPLACE_SCHEMA["properties"]["assets"]["required"]))
        self.assertEqual(gtt.marketplace_verification_contract_errors(payload), [])

    def passed_payload(self, root: Path, task_dir: Path) -> dict[str, Any]:
        workflow = root / "trellis/workflows/guru-team/workflow.md"
        schema = root / "trellis/workflows/guru-team/schemas/task-start-context.schema.json"
        finish_schema = root / "trellis/workflows/guru-team/schemas/finish-summary.schema.json"
        closeout_schema = root / "trellis/workflows/guru-team/schemas/closeout-plan.schema.json"
        workflow.parent.mkdir(parents=True, exist_ok=True)
        schema.parent.mkdir(parents=True, exist_ok=True)
        workflow.write_text("workflow\n", encoding="utf-8")
        schema.write_text("{}\n", encoding="utf-8")
        finish_schema.write_text('{"title":"finish"}\n', encoding="utf-8")
        closeout_schema.write_text('{"title":"closeout"}\n', encoding="utf-8")
        workflow_sha = gtt.digest_text("workflow\n")
        step = {
            "command": ["test"], "exit_code": 0,
            "stdout_sha256": gtt.digest_text(""), "stderr_sha256": gtt.digest_text(""),
            "stdout_size_bytes": 0, "stderr_size_bytes": 0, "passed": True,
        }
        return {
            "schema_version": "1.0", "generated_at": "2026-07-10T00:00:00Z", "status": "passed",
            "repo": "owner/repo", "remote": "origin", "branch": "codex/task",
            "marketplace_source": "gh:owner/repo/trellis#codex/task", "verified_head": "a" * 40,
            "remote_head": "a" * 40, "task_dir": gtt.repo_relative(root, task_dir),
            "steps": [dict(step) for _ in range(7)],
            "assets": {
                "workflow_sha256": workflow_sha,
                "preview_sha256": workflow_sha,
                "task_start_context_schema_sha256": gtt.hashlib.sha256(schema.read_bytes()).hexdigest(),
                "finish_summary_schema_sha256": gtt.hashlib.sha256(finish_schema.read_bytes()).hexdigest(),
                "closeout_plan_schema_sha256": gtt.hashlib.sha256(closeout_schema.read_bytes()).hexdigest(),
                "runtime_gitignore_present": True,
                "workspace_gitignore_present": True,
                "session_auto_commit_false": True,
                "legacy_handoff_absent": True,
                "legacy_intake_schema_absent": True,
            },
        }

    def test_marketplace_metadata_commit_rejects_unexpected_metadata_tail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifact = root / ".trellis/tasks/task/marketplace-verification.json"
            with (
                mock.patch.object(gtt, "git_status_paths", return_value=[
                    ".trellis/tasks/task/marketplace-verification.json",
                    ".trellis/tasks/task/issue-scope-ledger.json",
                    ".trellis/tasks/task/agent-assignment.json",
                ]),
                self.assertRaises(gtt.WorkflowError) as raised,
            ):
                gtt.commit_marketplace_verification_metadata(root, artifact, root / ".trellis/tasks/task/issue-scope-ledger.json", "chore(meta): test")
            self.assertIn(".trellis/tasks/task/agent-assignment.json", raised.exception.payload["unexpected_dirty_paths"])

    def test_marketplace_metadata_commit_allows_exact_artifact_and_ledger_tail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifact = root / ".trellis/tasks/task/marketplace-verification.json"
            ledger = root / ".trellis/tasks/task/issue-scope-ledger.json"
            with (
                mock.patch.object(gtt, "git_status_paths", return_value=[
                    ".trellis/tasks/task/marketplace-verification.json",
                    ".trellis/tasks/task/issue-scope-ledger.json",
                ]),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(gtt, "run", return_value=mock.Mock(returncode=1)),
                mock.patch.object(gtt, "current_head", return_value="a" * 40),
            ):
                payload = gtt.commit_marketplace_verification_metadata(root, artifact, ledger, "chore(meta): test")
            self.assertEqual(payload["paths"], [
                ".trellis/tasks/task/issue-scope-ledger.json",
                ".trellis/tasks/task/marketplace-verification.json",
            ])

    def test_pending_remote_marketplace_evidence_blocks_final_publish(self) -> None:
        pending = {
            "type": gtt.REMOTE_MARKETPLACE_EVIDENCE_TYPE,
            "status": "pending",
            "required": True,
            "artifact_path": "marketplace-verification.json",
            "reason": "push 后由 deterministic marketplace verifier 生成真实 evidence；pending 不满足最终 publish。",
        }
        ledger = {"close_issues": [{"number": 96, "acceptance_evidence": ["local ok", pending]}], "related_issues": [], "followup_issues": []}
        gate = {"changed_files": ["trellis/workflows/guru-team/workflow.md"], "issue_scope": {"close_issues_reviewed": [{"number": 96}]}}
        self.assertEqual(gtt.validate_ledger_for_publish(ledger, gate, allow_pending_remote_marketplace=True), [])
        self.assertTrue(any("必须是 passed" in error for error in gtt.validate_ledger_for_publish(ledger, gate)))

    def test_passed_remote_marketplace_evidence_rejects_tampered_digest(self) -> None:
        issue = {"acceptance_evidence": [{
            "type": gtt.REMOTE_MARKETPLACE_EVIDENCE_TYPE, "status": "passed", "required": True,
            "artifact_path": ".trellis/tasks/task/marketplace-verification.json", "artifact_sha256": "tampered",
            "verified_content_head": "a" * 40, "remote_head": "a" * 40, "publish_head": "a" * 40,
            "commands_passed": True,
        }]}
        self.assertTrue(any("artifact_sha256" in error for error in gtt.remote_marketplace_evidence_errors(issue, allow_pending=False)))

    def test_write_remote_marketplace_evidence_rejects_failed_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / ".trellis/tasks/task"
            task_dir.mkdir(parents=True)
            artifact = task_dir / "marketplace-verification.json"
            payload = self.passed_payload(root, task_dir)
            payload["status"] = "failed"
            payload["remote_head"] = ""
            payload["assets"] = {
                "workflow_sha256": "", "preview_sha256": "", "task_start_context_schema_sha256": "", "finish_summary_schema_sha256": "", "closeout_plan_schema_sha256": "",
                "runtime_gitignore_present": False, "workspace_gitignore_present": False, "session_auto_commit_false": False,
                "legacy_handoff_absent": False, "legacy_intake_schema_absent": False,
            }
            gtt.write_json(artifact, payload)
            with self.assertRaises(gtt.WorkflowError):
                gtt.write_remote_marketplace_evidence(root, task_dir, {"close_issues": []}, artifact, payload)

    def test_validate_marketplace_verification_accepts_exact_two_file_metadata_tail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / ".trellis/tasks/task"
            task_dir.mkdir(parents=True)
            artifact = task_dir / "marketplace-verification.json"
            payload = self.passed_payload(root, task_dir)
            gtt.write_json(artifact, payload)
            artifact_sha = gtt.hashlib.sha256(artifact.read_bytes()).hexdigest()
            evidence = {
                "type": gtt.REMOTE_MARKETPLACE_EVIDENCE_TYPE, "status": "passed", "required": True,
                "artifact_path": gtt.MARKETPLACE_VERIFICATION_ARTIFACT, "artifact_sha256": artifact_sha,
                "verified_content_head": "a" * 40, "remote_head": "a" * 40, "publish_head": "a" * 40,
                "commands_passed": True,
            }
            ledger = {
                "primary_issue": {"number": 96, "acceptance_evidence": [dict(evidence)]},
                "close_issues": [{"number": 96, "acceptance_evidence": [dict(evidence)]}],
                "related_issues": [], "followup_issues": [],
            }
            with mock.patch.object(gtt, "run") as run:
                run.side_effect = [
                    mock.Mock(returncode=0, stdout=(
                        ".trellis/tasks/task/issue-scope-ledger.json\n"
                        ".trellis/tasks/task/marketplace-verification.json\n"
                    ), stderr=""),
                    mock.Mock(returncode=0, stdout=f"{'b' * 40}\trefs/heads/codex/task\n", stderr=""),
                ]
                _path, _payload, errors = gtt.validate_marketplace_verification(
                    root, task_dir, "b" * 40, "owner/repo", "origin", "codex/task", ledger=ledger
                )
            self.assertEqual(errors, [])

    def test_validate_marketplace_verification_rejects_tampered_ledger_digest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / ".trellis/tasks/task"
            task_dir.mkdir(parents=True)
            artifact = task_dir / "marketplace-verification.json"
            payload = self.passed_payload(root, task_dir)
            gtt.write_json(artifact, payload)
            evidence = {
                "type": gtt.REMOTE_MARKETPLACE_EVIDENCE_TYPE, "status": "passed", "required": True,
                "artifact_path": gtt.repo_relative(root, artifact), "artifact_sha256": "f" * 64,
                "verified_content_head": "a" * 40, "remote_head": "a" * 40, "publish_head": "a" * 40,
                "commands_passed": True,
            }
            ledger = {"close_issues": [{"number": 96, "acceptance_evidence": [evidence]}]}
            with mock.patch.object(gtt, "run", return_value=mock.Mock(
                returncode=0, stdout=f"{'a' * 40}\trefs/heads/codex/task\n", stderr=""
            )):
                _path, _payload, errors = gtt.validate_marketplace_verification(
                    root, task_dir, "a" * 40, "owner/repo", "origin", "codex/task", ledger=ledger
                )
            self.assertTrue(any("does not match" in error for error in errors))

    def test_execute_marketplace_verification_records_order_and_digests(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / ".trellis/tasks/07-10-096-task-runtime-boundary"
            task_dir.mkdir(parents=True)
            apply_script = root / "trellis/presets/guru-team/scripts/bash/apply.sh"
            apply_script.parent.mkdir(parents=True)
            apply_script.write_text("#!/usr/bin/env bash\n", encoding="utf-8")
            expected = "a" * 40
            commands: list[list[str]] = []

            def fake_run(command: list[str], cwd: Path, check: bool = True) -> mock.Mock:
                commands.append(command)
                if command[:4] == ["git", "ls-remote", "--heads", "origin"]:
                    return mock.Mock(returncode=0, stdout=f"{expected}\trefs/heads/codex/096-task-runtime-boundary\n", stderr="")
                if command[:4] == ["git", "remote", "get-url", "origin"]:
                    return mock.Mock(returncode=0, stdout="https://github.com/owner/repo.git\n", stderr="")
                if command[:2] == ["git", "clone"]:
                    source_checkout = Path(command[-1])
                    script = source_checkout / "trellis/presets/guru-team/scripts/bash/apply.sh"
                    script.parent.mkdir(parents=True)
                    script.write_text("#!/usr/bin/env bash\n", encoding="utf-8")
                    workflow = source_checkout / "trellis/workflows/guru-team/workflow.md"
                    schema = source_checkout / "trellis/workflows/guru-team/schemas/task-start-context.schema.json"
                    finish_schema = source_checkout / "trellis/workflows/guru-team/schemas/finish-summary.schema.json"
                    closeout_schema = source_checkout / "trellis/workflows/guru-team/schemas/closeout-plan.schema.json"
                    workflow.parent.mkdir(parents=True, exist_ok=True)
                    schema.parent.mkdir(parents=True, exist_ok=True)
                    workflow.write_text("workflow", encoding="utf-8")
                    schema.write_text("{}", encoding="utf-8")
                    finish_schema.write_text('{"title":"finish"}', encoding="utf-8")
                    closeout_schema.write_text('{"title":"closeout"}', encoding="utf-8")
                    return mock.Mock(returncode=0, stdout="", stderr="")
                if command[:2] == ["git", "init"]:
                    return mock.Mock(returncode=0, stdout="", stderr="")
                project = cwd
                (project / ".trellis/guru-team/schemas").mkdir(parents=True, exist_ok=True)
                if command[:2] == ["trellis", "init"]:
                    (project / ".trellis/workflow.md").write_text("workflow", encoding="utf-8")
                elif "--create-new" in command:
                    (project / ".trellis/workflow.md.new").write_text("workflow", encoding="utf-8")
                elif command[:2] == ["trellis", "workflow"]:
                    (project / ".trellis/workflow.md").write_text("workflow", encoding="utf-8")
                elif command[0].endswith("trellis/presets/guru-team/scripts/bash/apply.sh"):
                    (project / ".trellis/guru-team/schemas/task-start-context.schema.json").write_text("{}", encoding="utf-8")
                    (project / ".trellis/guru-team/schemas/finish-summary.schema.json").write_text('{"title":"finish"}', encoding="utf-8")
                    (project / ".trellis/guru-team/schemas/closeout-plan.schema.json").write_text('{"title":"closeout"}', encoding="utf-8")
                    (project / ".gitignore").write_text(".trellis/.runtime/\n.trellis/workspace/\n", encoding="utf-8")
                    (project / ".trellis/config.yaml").write_text("session_auto_commit: false\n", encoding="utf-8")
                return mock.Mock(returncode=0, stdout="ok", stderr="")

            with mock.patch.object(gtt, "run", side_effect=fake_run):
                payload = gtt.execute_marketplace_verification(root, task_dir, "owner/repo", "origin", "codex/096-task-runtime-boundary", expected)

            self.assertEqual(payload["status"], "passed")
            self.assert_public_schema_valid(payload)
            self.assertEqual(payload["remote_head"], expected)
            self.assertEqual([step["passed"] for step in payload["steps"]], [True] * 7)
            self.assertEqual(commands[2][0:2], ["git", "clone"])
            self.assertEqual(commands[4][0:2], ["trellis", "init"])
            self.assertIn("--create-new", commands[5])
            self.assertIn("--force", commands[6])
            self.assertTrue(commands[7][0].endswith("trellis/presets/guru-team/scripts/bash/apply.sh"))
            self.assertEqual(payload["steps"][-1]["command"][0], "<temp-source>/trellis/presets/guru-team/scripts/bash/apply.sh")
            self.assertTrue(payload["assets"]["workflow_sha256"])
            self.assertTrue(payload["assets"]["finish_summary_schema_sha256"])
            self.assertTrue(payload["assets"]["workspace_gitignore_present"])
            self.assertTrue(payload["assets"]["session_auto_commit_false"])
            self.assertTrue(payload["assets"]["legacy_handoff_absent"])
            self.assertTrue(payload["assets"]["legacy_intake_schema_absent"])
            self.assertTrue((task_dir / "marketplace-verification.json").exists())

    def test_marketplace_failed_payload_contract_allows_partial_evidence(self) -> None:
        payload = {
            "schema_version": "1.0", "generated_at": "2026-07-10T00:00:00Z", "status": "failed",
            "repo": "owner/repo", "remote": "origin", "branch": "codex/task",
            "marketplace_source": "gh:owner/repo/trellis#codex/task", "verified_head": "a" * 40,
            "remote_head": "", "task_dir": ".trellis/tasks/task",
            "steps": [{"command": ["git", "ls-remote"], "exit_code": 2, "stdout_sha256": gtt.digest_text(""), "stderr_sha256": gtt.digest_text("failed"), "stdout_size_bytes": 0, "stderr_size_bytes": 6, "passed": False}],
            "assets": {"workflow_sha256": "", "preview_sha256": "", "task_start_context_schema_sha256": "", "finish_summary_schema_sha256": "", "closeout_plan_schema_sha256": "", "runtime_gitignore_present": False, "workspace_gitignore_present": False, "session_auto_commit_false": False, "legacy_handoff_absent": False, "legacy_intake_schema_absent": False},
        }
        self.assertEqual(gtt.marketplace_verification_contract_errors(payload), [])

    def test_execute_marketplace_verification_writes_schema_valid_early_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / ".trellis/tasks/task"
            task_dir.mkdir(parents=True)
            with (
                mock.patch.object(gtt, "run", return_value=mock.Mock(returncode=2, stdout="", stderr="network failed")),
                self.assertRaises(gtt.WorkflowError),
            ):
                gtt.execute_marketplace_verification(root, task_dir, "owner/repo", "origin", "codex/task", "a" * 40)
            payload = gtt.read_json(task_dir / "marketplace-verification.json")
            self.assertEqual(payload["status"], "failed")
            self.assertEqual(gtt.marketplace_verification_contract_errors(payload), [])
            self.assert_public_schema_valid(payload)
            self.assertGreaterEqual(len(payload["steps"]), 1)

    def test_execute_marketplace_verification_writes_schema_valid_partial_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / ".trellis/tasks/task"
            task_dir.mkdir(parents=True)
            expected = "a" * 40
            def fake_run(command: list[str], cwd: Path, check: bool = True) -> mock.Mock:
                if command[:4] == ["git", "ls-remote", "--heads", "origin"]:
                    return mock.Mock(returncode=0, stdout=f"{expected}\trefs/heads/codex/task\n", stderr="")
                if command[:4] == ["git", "remote", "get-url", "origin"]:
                    return mock.Mock(returncode=0, stdout="https://github.com/owner/repo.git\n", stderr="")
                if command[:2] == ["git", "clone"]:
                    source = Path(command[-1])
                    (source / "trellis/presets/guru-team/scripts/bash").mkdir(parents=True)
                    return mock.Mock(returncode=0, stdout="", stderr="")
                if command[:2] == ["git", "init"]:
                    return mock.Mock(returncode=0, stdout="", stderr="")
                return mock.Mock(returncode=3, stdout="", stderr="init failed")
            with mock.patch.object(gtt, "run", side_effect=fake_run), self.assertRaises(gtt.WorkflowError):
                gtt.execute_marketplace_verification(root, task_dir, "owner/repo", "origin", "codex/task", expected)
            payload = gtt.read_json(task_dir / "marketplace-verification.json")
            self.assertEqual(payload["status"], "failed")
            self.assertEqual(gtt.marketplace_verification_contract_errors(payload), [])
            self.assert_public_schema_valid(payload)
            self.assertGreater(len(payload["steps"]), 3)

    def test_marketplace_verification_required_for_public_extension_paths(self) -> None:
        self.assertTrue(gtt.marketplace_verification_required({"changed_files": ["trellis/workflows/guru-team/workflow.md"]}))
        self.assertFalse(gtt.marketplace_verification_required({"changed_files": ["docs/internal-note.md"]}))


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
            "head": self.head,
            "generated_at": "2026-07-11T00:00:00Z",
            "changed_files": ["trellis/workflows/guru-team/workflow.md"],
            "issue_scope": {"close_issues_reviewed": [{"number": 105}]},
        }
        self.ledger = {
            "primary_issue": {"number": 105, "acceptance_evidence": ["review passed"]},
            "close_issues": [{
                "number": 105,
                "acceptance_evidence": [
                    "acceptance passed",
                    {
                        "type": "remote_marketplace_verification",
                        "status": "pending",
                        "required": True,
                        "artifact_path": "marketplace-verification.json",
                        "reason": "push 后由 deterministic marketplace verifier 生成真实 evidence；pending 不满足最终 publish。",
                    },
                ],
            }],
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
        gtt.write_json(self.task_dir / "task.json", self.task)
        gtt.write_json(self.task_dir / "task-start-context.json", self.context)
        gtt.write_json(self.task_dir / "review-gate.json", self.gate)
        gtt.write_json(self.task_dir / "issue-scope-ledger.json", self.ledger)
        gtt.write_json(self.task_dir / "finish-summary-index.json", self.index)
        (self.task_dir / "pr-body.md").write_text(valid_pr_body("#105 closeout transaction。"), encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def build_plan(self) -> dict[str, object]:
        def fake_run(command: list[str], **_kwargs: object) -> mock.Mock:
            stdout = f"{self.head}\n" if command[:2] == ["git", "rev-list"] else ""
            return mock.Mock(returncode=0, stdout=stdout, stderr="")

        with mock.patch.object(gtt, "run", side_effect=fake_run):
            return gtt.build_closeout_plan(
                self.root,
                self.task_dir,
                self.context,
                self.task,
                self.task_dir / "review-gate.json",
                self.gate,
                self.ledger,
                self.task_dir / "finish-summary-index.json",
                repo="owner/repo",
                remote="origin",
                base_branch="main",
                head_branch="fix/105-closeout",
                reviewed_head=self.head,
                title="#105 重构 finish-work 收尾事务",
            )

    def test_read_pr_body_file_preserves_exact_utf8_text(self) -> None:
        body_path = self.root / "reviewed-body.md"
        exact = "\n## 变更摘要\n\n- Markdown hard break.  \n\n"
        body_path.write_bytes(exact.encode("utf-8"))

        self.assertEqual(gtt.read_pr_body_file(self.root, str(body_path)), exact)

    def test_closeout_reviewed_body_accepts_exact_task_local_relative_and_absolute_sources(self) -> None:
        body_path = self.task_dir / gtt.PR_BODY_ARTIFACT
        expected = body_path.read_text(encoding="utf-8")
        relative = body_path.relative_to(self.root).as_posix()

        for source in [relative, str(body_path)]:
            with self.subTest(source=source):
                body, body_source = gtt.resolve_closeout_reviewed_body(
                    self.root,
                    self.task_dir,
                    finish_args(body_file=source),
                )
                self.assertEqual(body, expected)
                self.assertEqual(body_source, f"body-file:{relative}")

    def test_closeout_reviewed_body_rejects_external_sources_even_when_strip_equivalent(self) -> None:
        body_path = self.task_dir / gtt.PR_BODY_ARTIFACT
        canonical = body_path.read_text(encoding="utf-8")
        variants = {
            "same-bytes": canonical,
            "leading-trailing-whitespace": f" \n{canonical}\n ",
            "final-newline": canonical.rstrip("\n"),
            "markdown-hard-break-spaces": canonical.replace(
                "- Guru Team publish helper\n",
                "- Guru Team publish helper  \n",
            ),
        }

        for label, content in variants.items():
            external = self.root / f"external-{label}.md"
            external.write_text(content, encoding="utf-8")
            with self.subTest(label=label), self.assertRaises(gtt.WorkflowError) as raised:
                gtt.resolve_closeout_reviewed_body(
                    self.root,
                    self.task_dir,
                    finish_args(body_file=str(external)),
                )
            self.assertIn("current task-local pr-body.md", str(raised.exception))

    def test_closeout_reviewed_body_rejects_body_artifact(self) -> None:
        artifact = self.task_dir / gtt.PR_READINESS_ARTIFACT
        gtt.write_json(artifact, {"ready": True, "body_file": gtt.PR_BODY_ARTIFACT})

        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.resolve_closeout_reviewed_body(
                self.root,
                self.task_dir,
                finish_args(
                    body_file=str(self.task_dir / gtt.PR_BODY_ARTIFACT),
                    body_artifact=str(artifact),
                ),
            )
        self.assertIn("does not accept --body-artifact", str(raised.exception))

    def test_closeout_reviewed_body_rejects_symlink_to_task_body(self) -> None:
        symlink = self.root / "reviewed-body-link.md"
        symlink.symlink_to(self.task_dir / gtt.PR_BODY_ARTIFACT)

        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.resolve_closeout_reviewed_body(
                self.root,
                self.task_dir,
                finish_args(body_file=str(symlink)),
            )
        self.assertIn("symbolic-link components", str(raised.exception))
        self.assertEqual(raised.exception.payload["symlink_component"], symlink.name)

    def test_closeout_reviewed_body_rejects_relative_and_absolute_ancestor_symlink_aliases(self) -> None:
        alias = self.root / "task-body-alias"
        alias.symlink_to(self.task_dir, target_is_directory=True)
        sources = [
            f"{alias.name}/{gtt.PR_BODY_ARTIFACT}",
            str(alias / gtt.PR_BODY_ARTIFACT),
        ]

        for source in sources:
            with self.subTest(source=source), self.assertRaises(gtt.WorkflowError) as raised:
                gtt.resolve_closeout_reviewed_body(
                    self.root,
                    self.task_dir,
                    finish_args(body_file=source),
                )
            self.assertIn("symbolic-link components", str(raised.exception))
            self.assertEqual(raised.exception.payload["symlink_component"], alias.name)

    def test_closeout_reviewed_body_rejects_multilevel_dangling_and_loop_symlink_components(self) -> None:
        aliases = self.root / "aliases"
        aliases.mkdir()
        multilevel = aliases / "level-one"
        multilevel.symlink_to(self.task_dir, target_is_directory=True)
        dangling = aliases / "dangling"
        dangling.symlink_to(self.root / "missing-task", target_is_directory=True)
        loop = aliases / "loop"
        loop.symlink_to(loop, target_is_directory=True)

        for alias in [multilevel, dangling, loop]:
            source = alias / gtt.PR_BODY_ARTIFACT
            with self.subTest(alias=alias.name), self.assertRaises(gtt.WorkflowError) as raised:
                gtt.resolve_closeout_reviewed_body(
                    self.root,
                    self.task_dir,
                    finish_args(body_file=str(source)),
                )
            self.assertIn("symbolic-link components", str(raised.exception))
            self.assertEqual(
                raised.exception.payload["symlink_component"],
                f"aliases/{alias.name}",
            )

    def test_closeout_reviewed_body_rejects_symlinked_task_directory_parent(self) -> None:
        root = self.root / "symlinked-task-parent"
        external_tasks = self.root / "external-tasks"
        task_dir = external_tasks / "07-11-closeout"
        task_dir.mkdir(parents=True)
        (task_dir / gtt.PR_BODY_ARTIFACT).write_text(valid_pr_body("symlinked task parent"), encoding="utf-8")
        (root / ".trellis").mkdir(parents=True)
        (root / ".trellis/tasks").symlink_to(external_tasks, target_is_directory=True)
        direct_task_dir = root / ".trellis/tasks/07-11-closeout"

        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.resolve_closeout_reviewed_body(
                root,
                direct_task_dir,
                finish_args(body_file=".trellis/tasks/07-11-closeout/pr-body.md"),
            )
        self.assertIn("symbolic-link components", str(raised.exception))
        self.assertEqual(raised.exception.payload["symlink_component"], ".trellis/tasks")

    def test_closeout_reviewed_body_rejects_repo_external_alias_for_relative_and_absolute_sources(self) -> None:
        alias = self.root.parent / f"{self.root.name}-repo-alias"
        alias.symlink_to(self.root, target_is_directory=True)
        self.addCleanup(alias.unlink, missing_ok=True)
        aliased_body = alias / self.task_dir.relative_to(self.root) / gtt.PR_BODY_ARTIFACT
        sources = [str(aliased_body), os.path.relpath(aliased_body, self.root)]

        for source in sources:
            with self.subTest(source=source), self.assertRaises(gtt.WorkflowError) as raised:
                gtt.resolve_closeout_reviewed_body(
                    self.root,
                    self.task_dir,
                    finish_args(body_file=source),
                )
            self.assertIn("must stay inside the repository root", str(raised.exception))

    def test_closeout_reviewed_body_rejects_multilevel_outer_alias_to_repo_root(self) -> None:
        second = self.root.parent / f"{self.root.name}-outer-second"
        first = self.root.parent / f"{self.root.name}-outer-first"
        second.symlink_to(self.root, target_is_directory=True)
        first.symlink_to(second, target_is_directory=True)
        self.addCleanup(first.unlink, missing_ok=True)
        self.addCleanup(second.unlink, missing_ok=True)
        source = first / self.task_dir.relative_to(self.root) / gtt.PR_BODY_ARTIFACT

        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.resolve_closeout_reviewed_body(
                self.root,
                self.task_dir,
                finish_args(body_file=str(source)),
            )
        self.assertIn("must stay inside the repository root", str(raised.exception))

    @unittest.skipUnless(sys.platform == "darwin", "Darwin /var system alias compatibility")
    def test_closeout_reviewed_body_accepts_fixed_darwin_var_system_alias(self) -> None:
        if not str(self.root).startswith("/var/"):
            self.skipTest("temporary directory is not exposed through the /var alias")
        canonical_root = Path("/private") / self.root.relative_to("/")
        canonical_task_dir = canonical_root / self.task_dir.relative_to(self.root)
        aliased_body = self.task_dir / gtt.PR_BODY_ARTIFACT

        body, body_source = gtt.resolve_closeout_reviewed_body(
            canonical_root,
            canonical_task_dir,
            finish_args(body_file=str(aliased_body)),
        )
        self.assertEqual(body, aliased_body.read_text(encoding="utf-8"))
        self.assertEqual(
            body_source,
            f"body-file:{self.task_dir.relative_to(self.root).as_posix()}/{gtt.PR_BODY_ARTIFACT}",
        )

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
            [gtt.FINISH_SUMMARY_ARTIFACT],
        )
        self.assertNotIn(
            f"{first['task']['active_locator']}/{gtt.FINISH_SUMMARY_ARTIFACT}",
            first["projection"]["metadata_allowlist"],
        )
        self.assertIn(
            f"{first['task']['archive_locator']}/{gtt.FINISH_SUMMARY_ARTIFACT}",
            first["projection"]["metadata_allowlist"],
        )
        if importlib.util.find_spec("jsonschema") is not None:
            from jsonschema import Draft202012Validator

            schema = gtt.read_json(
                Path(__file__).resolve().parents[2] / "schemas/closeout-plan.schema.json"
            )
            self.assertEqual(list(Draft202012Validator(schema).iter_errors(first)), [])

    def test_closeout_runtime_contracts_reject_legacy_archive_first_semantics(self) -> None:
        repo = Path(__file__).resolve().parents[5]
        surfaces = [
            repo / ".trellis/spec/workflow/companion-scripts.md",
            repo / ".trellis/spec/workflow/data-contracts.md",
            repo / ".trellis/spec/workflow/workflow-contract.md",
            repo / "trellis/workflows/guru-team/workflow.md",
            repo / ".trellis/workflow.md",
        ]
        forbidden = [
            "Initial summary uses empty",
            "after archive and initial finish-summary",
            "After PR creation, one additional exact archived-task",
            "archives the active task before publish",
            '"initial_pr_url"',
            '"initial_pr_refs"',
        ]
        violations = []
        for path in surfaces:
            text = path.read_text(encoding="utf-8")
            violations.extend(
                f"{path.relative_to(repo)}: {phrase}"
                for phrase in forbidden
                if phrase in text
            )
        self.assertEqual(violations, [])

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
                mock.patch.object(gtt, "load_task_start_context", return_value=self.context),
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

    def test_marketplace_relative_locator_survives_exact_archive_move_with_digest(self) -> None:
        plan = self.build_plan()
        verification = {
            "status": "passed",
            "verified_head": self.head,
            "remote_head": self.head,
            "steps": [{"passed": True}],
        }
        artifact = self.task_dir / gtt.MARKETPLACE_VERIFICATION_ARTIFACT
        gtt.write_json(artifact, verification)
        with mock.patch.object(gtt, "marketplace_verification_contract_errors", return_value=[]):
            evidence = gtt.closeout_passed_marketplace_evidence(self.root, artifact, verification)
            ledger = gtt.record_marketplace_machine_evidence(self.ledger, evidence)
            gtt.write_json(self.task_dir / "issue-scope-ledger.json", ledger)
            gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, plan)
            gtt.write_json(self.task_dir / gtt.PR_READINESS_ARTIFACT, {"ready": True})
            summary = gtt.closeout_summary_for_pr(
                plan,
                {"number": 105, "url": "https://github.com/owner/repo/pull/105"},
            )
            gtt.write_json(self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT, summary)
            for name in plan["projection"]["move_paths"]:
                path = self.task_dir / name
                if not path.exists():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("planned metadata\n", encoding="utf-8")
            archived = self.root / plan["task"]["archive_locator"]
            archived.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(self.task_dir), str(archived))
            gtt.validate_closeout_archive_layout(self.root, archived, plan)
        archived_ledger = gtt.read_json(archived / "issue-scope-ledger.json")
        archived_evidence = gtt.remote_marketplace_evidence(archived_ledger["primary_issue"])
        self.assertEqual(archived_evidence["artifact_path"], gtt.MARKETPLACE_VERIFICATION_ARTIFACT)
        self.assertEqual(
            archived_evidence["artifact_sha256"],
            gtt.hashlib.sha256((archived / gtt.MARKETPLACE_VERIFICATION_ARTIFACT).read_bytes()).hexdigest(),
        )

    def test_archive_recovery_rejects_partial_move_subset_and_evidence_lineage(self) -> None:
        plan = self.build_plan()
        allowed = set(plan["projection"]["metadata_allowlist"])
        subset = sorted(allowed - {next(iter(allowed))})
        archived = self.root / plan["task"]["archive_locator"]
        with (
            mock.patch.object(gtt, "validate_closeout_archive_layout"),
            mock.patch.object(gtt, "git_status_paths", return_value=subset),
            mock.patch.object(gtt, "run_stdout") as mutation,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.resume_archive_metadata_transaction(self.root, archived, plan)
        self.assertTrue(raised.exception.payload["missing_paths"])
        mutation.assert_not_called()

        evidence_paths = set(plan["projection"]["evidence_paths"])
        with (
            mock.patch.object(gtt, "closeout_commit_parent", return_value=self.head),
            mock.patch.object(gtt, "closeout_commit_paths", return_value=evidence_paths - {next(iter(evidence_paths))}),
            mock.patch.object(
                gtt,
                "closeout_commit_tracked_task_paths",
                return_value={
                    f"{plan['task']['active_locator']}/{path}"
                    for path in plan["projection"]["tracked_move_paths"]
                },
            ),
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.validate_closeout_evidence_commit(self.root, plan, "b" * 40)

    def test_real_git_mixed_tracked_untracked_archive_transaction_and_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "project"
            root.mkdir()
            active = root / ".trellis/tasks/task"
            archived = root / ".trellis/tasks/archive/2026-07/task"
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            (root / "README.md").write_text("reviewed work\n", encoding="utf-8")
            archive_script = root / ".trellis/scripts/task.py"
            archive_script.parent.mkdir(parents=True)
            archive_script.write_text(
                """import json
import shutil
from pathlib import Path

root = Path.cwd()
active = root / ".trellis/tasks/task"
task_path = active / "task.json"
task = json.loads(task_path.read_text(encoding="utf-8"))
task["status"] = "completed"
task["completedAt"] = "2026-07-11"
task_path.write_text(json.dumps(task, indent=2) + "\\n", encoding="utf-8")
archived = root / ".trellis/tasks/archive/2026-07/task"
archived.parent.mkdir(parents=True, exist_ok=True)
shutil.move(str(active), str(archived))
""",
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "README.md", ".trellis/scripts/task.py"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "reviewed"], cwd=root, check=True)
            reviewed_head = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True, capture_output=True
            ).stdout.strip()
            active.mkdir(parents=True)
            (active / "task.json").write_text('{"status":"in_progress"}\n', encoding="utf-8")
            (active / "review.md").write_text("reviewed metadata\n", encoding="utf-8")
            subprocess.run(["git", "add", ".trellis/tasks/task"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "evidence"], cwd=root, check=True)
            evidence_head = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True, capture_output=True
            ).stdout.strip()
            (active / gtt.FINISH_SUMMARY_ARTIFACT).write_text('{"projected":true}\n', encoding="utf-8")
            expected = {
                ".trellis/tasks/task/task.json",
                ".trellis/tasks/task/review.md",
                ".trellis/tasks/archive/2026-07/task/task.json",
                ".trellis/tasks/archive/2026-07/task/review.md",
                ".trellis/tasks/archive/2026-07/task/finish-summary.json",
            }
            plan = {
                "task": {
                    "active_locator": ".trellis/tasks/task",
                    "archive_locator": ".trellis/tasks/archive/2026-07/task",
                    "source_issue": 105,
                },
                "git": {
                    "reviewed_work_head": reviewed_head,
                    "remote": "origin",
                    "head_branch": "main",
                },
                "projection": {
                    "move_paths": ["finish-summary.json", "review.md", "task.json"],
                    "tracked_move_paths": ["review.md", "task.json"],
                    "untracked_archive_outputs": ["finish-summary.json"],
                    "metadata_allowlist": sorted(expected),
                    "evidence_paths": [
                        ".trellis/tasks/task/review.md",
                        ".trellis/tasks/task/task.json",
                    ],
                },
            }
            self.assertNotIn(".trellis/tasks/task/finish-summary.json", expected)
            gtt.validate_closeout_archive_git_paths(expected, plan, stage="real-status")
            gtt.validate_closeout_evidence_commit(root, plan, evidence_head)
            bare = base / "remote.git"
            subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
            subprocess.run(["git", "remote", "add", "origin", str(bare)], cwd=root, check=True)
            subprocess.run(["git", "push", "-qu", "origin", "main"], cwd=root, check=True)
            observed_status_sets: list[set[str]] = []
            real_git_status_paths = gtt.git_status_paths

            def capture_git_status_paths(repo: Path) -> list[str]:
                paths = real_git_status_paths(repo)
                observed_status_sets.append(set(paths))
                return paths

            subprocess.run(["python3", "./.trellis/scripts/task.py", "archive", "task", "--no-commit"], cwd=root, check=True)
            (archived / "review.md").write_text("tampered after archive move\n", encoding="utf-8")
            with (
                mock.patch.object(gtt, "validate_closeout_archive_layout"),
                self.assertRaises(gtt.WorkflowError) as tampered,
            ):
                gtt.resume_archive_metadata_transaction(root, archived, plan)
            self.assertIn("immutable evidence blob", str(tampered.exception))
            shutil.move(str(archived), str(active))
            (active / "task.json").write_text('{"status":"in_progress"}\n', encoding="utf-8")
            (active / "review.md").write_text("reviewed metadata\n", encoding="utf-8")

            with (
                mock.patch.object(gtt, "validate_closeout_active_projection"),
                mock.patch.object(gtt, "validate_closeout_archive_layout"),
                mock.patch.object(gtt, "git_status_paths", side_effect=capture_git_status_paths),
            ):
                executed_archive, archive_commit = gtt.execute_archive_metadata_transaction(
                    root, active, plan
                )
            archive_head = archive_commit["commit"]
            self.assertEqual(executed_archive, archived)
            self.assertIn(expected, observed_status_sets)
            self.assertEqual(gtt.closeout_commit_parent(root, archive_head), evidence_head)
            self.assertEqual(gtt.closeout_commit_paths(root, archive_head), expected)
            with mock.patch.object(gtt, "validate_closeout_archive_layout"):
                recovered = gtt.resume_archive_metadata_transaction(root, archived, plan)
            self.assertEqual(recovered["commit"], archive_head)
            self.assertEqual(set(recovered["paths"]), expected)

            invalid_sets = {
                "misreported-untracked-active-delete": expected | {".trellis/tasks/task/finish-summary.json"},
                "missing-archive-output": expected - {".trellis/tasks/archive/2026-07/task/finish-summary.json"},
                "extra-nonmetadata": expected | {"src/runtime.py"},
                "partial-tracked-move": expected - {".trellis/tasks/task/review.md"},
            }
            for case, paths in invalid_sets.items():
                with self.subTest(case=case), self.assertRaises(gtt.WorkflowError):
                    gtt.validate_closeout_archive_git_paths(paths, plan, stage=case)

    def test_2026_07_04_archive_move_failure_keeps_active_without_commit_or_push(self) -> None:
        plan = self.build_plan()
        archive_script = self.root / ".trellis/scripts/task.py"
        archive_script.parent.mkdir(parents=True)
        archive_script.write_text("# fixture\n", encoding="utf-8")
        archived = self.root / plan["task"]["archive_locator"]
        with (
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "validate_closeout_evidence_commit"),
            mock.patch.object(gtt, "validate_closeout_active_projection"),
            mock.patch.object(
                gtt,
                "run",
                return_value=mock.Mock(returncode=1, stdout="", stderr="injected archive move failure"),
            ),
            mock.patch.object(gtt, "run_stdout") as mutation,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.execute_archive_metadata_transaction(self.root, self.task_dir, plan)
        self.assertIn("archive move failed", str(raised.exception).lower())
        self.assertTrue(self.task_dir.is_dir())
        self.assertFalse(archived.exists())
        mutation.assert_not_called()

    def test_closeout_plan_tampering_and_protected_input_drift_fail_closed(self) -> None:
        plan = self.build_plan()
        plan["publish"]["title"] = "tampered"
        self.assertTrue(any("digest" in error for error in gtt.closeout_plan_errors(plan)))
        persisted = self.build_plan()
        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, persisted)
        (self.task_dir / "pr-body.md").write_text(valid_pr_body("changed body。"), encoding="utf-8")
        rebuilt = self.build_plan()
        self.assertNotEqual(persisted["plan_digest"], rebuilt["plan_digest"])

    def test_closeout_evidence_commit_owns_exact_phase3_metadata_tail(self) -> None:
        phase3 = [
            "review.md",
            "reviews/round-001-final.md",
            "review-gate.json",
            "agent-assignment.json",
            "pr-body.md",
            "finish-summary-index.json",
        ]
        for name in phase3:
            path = self.task_dir / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text("reviewed metadata\n", encoding="utf-8")
        planned_dirty = [
            f".trellis/tasks/07-11-closeout/{name}"
            for name in phase3
        ]
        with mock.patch.object(gtt, "git_status_paths", return_value=planned_dirty):
            plan = self.build_plan()
        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, plan)
        gtt.write_json(self.task_dir / gtt.PR_READINESS_ARTIFACT, {"ready": True})
        gtt.write_json(self.task_dir / gtt.MARKETPLACE_VERIFICATION_ARTIFACT, {"status": "passed"})
        dirty = set(plan["projection"]["evidence_paths"])

        def fake_stdout(command: list[str], **_kwargs: object) -> str:
            if command[:4] == ["git", "diff", "--cached", "--name-only"]:
                return "\n".join(sorted(dirty))
            if command[:3] == ["git", "rev-parse", "HEAD"]:
                return self.head
            return ""

        with (
            mock.patch.object(gtt, "git_status_paths", return_value=sorted(dirty)),
            mock.patch.object(gtt, "run_stdout", side_effect=fake_stdout) as run_stdout,
            mock.patch.object(gtt, "validate_closeout_evidence_commit"),
        ):
            result = gtt.commit_closeout_evidence_metadata(self.root, self.task_dir, plan)
        self.assertEqual(result["paths"], sorted(dirty))
        self.assertIn(
            mock.call(["git", "add", "-A", "--", plan["task"]["active_locator"]], cwd=self.root),
            run_stdout.mock_calls,
        )

    def test_closeout_evidence_commit_rejects_other_task_metadata(self) -> None:
        plan = self.build_plan()
        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, plan)
        gtt.write_json(self.task_dir / gtt.PR_READINESS_ARTIFACT, {"ready": True})
        gtt.write_json(self.task_dir / gtt.MARKETPLACE_VERIFICATION_ARTIFACT, {"status": "passed"})
        dirty = [
            f"{plan['task']['active_locator']}/{gtt.CLOSEOUT_PLAN_ARTIFACT}",
            ".trellis/tasks/07-11-other-task/review.md",
        ]
        with (
            mock.patch.object(gtt, "git_status_paths", return_value=dirty),
            mock.patch.object(gtt, "run_stdout") as mutation,
            self.assertRaises(gtt.WorkflowError) as raised,
        ):
            gtt.commit_closeout_evidence_metadata(self.root, self.task_dir, plan)
        self.assertIn(dirty[1], raised.exception.payload["unexpected_dirty_paths"])
        mutation.assert_not_called()

    def test_git_status_expands_untracked_and_disables_rename_detection(self) -> None:
        proc = mock.Mock(returncode=0, stdout=" D src/runtime.py\n?? .trellis/tasks/07-11-closeout/runtime.py\n")
        with mock.patch.object(gtt, "run", return_value=proc) as run:
            paths = gtt.git_status_paths(self.root)
        self.assertEqual(paths, ["src/runtime.py", ".trellis/tasks/07-11-closeout/runtime.py"])
        run.assert_called_once_with(
            ["git", "status", "--porcelain", "--untracked-files=all", "--no-renames"],
            cwd=self.root,
            check=False,
        )

    def test_marketplace_recorder_replaces_only_machine_evidence(self) -> None:
        pending = gtt.closeout_pending_marketplace_evidence(self.root, self.task_dir, self.head)
        first = gtt.record_marketplace_machine_evidence(self.ledger, pending)
        changed_reason = json.loads(json.dumps(self.ledger, ensure_ascii=False))
        changed_reason["close_issues"][0]["reason"] = "AI reviewed reason changed"
        second = gtt.record_marketplace_machine_evidence(changed_reason, pending)
        self.assertEqual(
            gtt.remote_marketplace_evidence(first["close_issues"][0]),
            gtt.remote_marketplace_evidence(second["close_issues"][0]),
        )
        tampered = dict(pending)
        tampered.pop("publish_head")
        issue = {"acceptance_evidence": [tampered]}
        self.assertTrue(gtt.remote_marketplace_evidence_errors(issue, allow_pending=True))

    def test_readiness_binds_closeout_digest_without_breaking_legacy_snapshot(self) -> None:
        digest = self.build_plan()["plan_digest"]
        _path, closeout = gtt.build_pr_readiness_snapshot(
            self.root,
            self.task_dir,
            repo="owner/repo",
            base_branch="main",
            head_branch="fix/105-closeout",
            reviewed_head_sha=self.head,
            title="#105 closeout",
            draft=True,
            closeout_plan_digest=digest,
        )
        self.assertEqual(closeout["publish_inputs"]["closeout_plan_digest"], digest)
        _path, legacy = gtt.build_pr_readiness_snapshot(
            self.root,
            self.task_dir,
            repo="owner/repo",
            base_branch="main",
            head_branch="fix/105-closeout",
            reviewed_head_sha=self.head,
            title="#105 closeout",
            draft=False,
        )
        self.assertNotIn("closeout_plan_digest", legacy["publish_inputs"])

    def test_draft_resolver_rejects_multiple_or_ready_before_archive(self) -> None:
        plan = self.build_plan()
        body = (self.task_dir / "pr-body.md").read_text(encoding="utf-8")
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
        with mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=ready), self.assertRaises(gtt.WorkflowError):
            gtt.ensure_closeout_draft_pr(self.root, plan, "body")

        for key, value in [("title", "tampered title"), ("body", "tampered body")]:
            with self.subTest(key=key):
                tampered = dict(entry, **{key: value})
                with (
                    mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=tampered),
                    self.assertRaises(gtt.WorkflowError),
                ):
                    gtt.ensure_closeout_draft_pr(self.root, plan, body)

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
        body = (self.task_dir / "pr-body.md").read_text(encoding="utf-8")
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
        body = (self.task_dir / "pr-body.md").read_text(encoding="utf-8")
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
            self.assertRaises(gtt.WorkflowError),
        ):
            gtt.ensure_closeout_draft_pr(self.root, plan, body)
        create.assert_not_called()

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
            source_root / "trellis/workflows/guru-team/workflow.md",
            source_root / "docs/requirements/guru-team-trellis-flow.md",
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
                (self.task_dir / "pr-body.md").write_text(exact_body, encoding="utf-8")
                plan = self.build_plan()
                readiness_path, readiness = gtt.build_pr_readiness_snapshot(
                    self.root,
                    self.task_dir,
                    repo="owner/repo",
                    base_branch="main",
                    head_branch="fix/105-closeout",
                    reviewed_head_sha=self.head,
                    title=plan["publish"]["title"],
                    draft=True,
                    closeout_plan_digest=plan["plan_digest"],
                )
                gtt.write_json(readiness_path, readiness)
                _path, _inputs, recovered_body = gtt.read_pr_readiness_publish_inputs(
                    self.root,
                    self.task_dir,
                    str(readiness_path),
                    self.gate,
                    require_committed=False,
                )
                self.assertEqual(recovered_body, exact_body)

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

    def test_archived_pr_replacement_cannot_diverge_from_final_summary_identity(self) -> None:
        plan = self.build_plan()
        body = (self.task_dir / "pr-body.md").read_text(encoding="utf-8")
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

        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, plan)
        args = finish_args(dry_run=False, expected_plan_digest=plan["plan_digest"])
        for case, tampered in [
            ("replacement", replacement),
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
        body = (self.task_dir / "pr-body.md").read_text(encoding="utf-8")
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
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", self.gate, [])),
            mock.patch.object(gtt, "load_issue_scope_ledger", return_value=self.ledger),
            mock.patch.object(gtt, "closeout_evidence_is_committed", return_value=True),
            mock.patch.object(gtt, "validate_closeout_active_projection"),
            mock.patch.object(gtt, "validate_closeout_evidence_commit"),
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

    def test_state_resolver_uses_persisted_facts_without_runtime_marker(self) -> None:
        plan = self.build_plan()
        with (
            mock.patch.object(gtt, "task_dir_is_archived", return_value=False),
            mock.patch.object(gtt, "closeout_evidence_is_committed", return_value=False),
        ):
            self.assertEqual(gtt.resolve_closeout_state(self.root, self.task_dir, plan, self.ledger, self.gate), "prepared")
        draft = {"isDraft": True}
        with (
            mock.patch.object(gtt, "task_dir_is_archived", return_value=False),
            mock.patch.object(gtt, "closeout_evidence_is_committed", return_value=True),
        ):
            self.assertEqual(gtt.resolve_closeout_state(self.root, self.task_dir, plan, self.ledger, self.gate), "evidence_pushed")
            self.assertEqual(gtt.resolve_closeout_state(self.root, self.task_dir, plan, self.ledger, self.gate, draft), "draft_bound")

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
            mock.patch.object(gtt, "load_task_start_context", return_value=self.context),
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

    def test_issue_100_pending_marketplace_evidence_regression(self) -> None:
        pending = gtt.closeout_pending_marketplace_evidence(self.root, self.task_dir, self.head)
        ledger = gtt.record_marketplace_machine_evidence(self.ledger, pending)
        errors = gtt.validate_ledger_for_publish(ledger, self.gate, allow_pending_remote_marketplace=False)
        self.assertTrue(any("pending" in error for error in errors))

    def test_cli_exposes_expected_digest_but_not_legacy_recovery_flag(self) -> None:
        parser = gtt.build_parser()
        finish = parser.parse_args([
            "finish-work", "--from-trellis-finish-work", "--dry-run",
            "--expected-plan-digest", "a" * 64,
        ])
        self.assertEqual(finish.expected_plan_digest, "a" * 64)
        with self.assertRaises(SystemExit):
            parser.parse_args(["publish-pr", "--recovery-after-finish-work"])

    @mock.patch.object(gtt, "closeout_remote_branch_head", return_value="0" * 40)
    def test_formal_state_machine_orders_verifier_draft_projection_archive_ready(
        self, _remote_head: mock.Mock
    ) -> None:
        plan = self.build_plan()
        prepared = {
            "plan": plan,
            "task": self.task,
            "task_context": self.context,
            "gate": self.gate,
            "ledger": self.ledger,
            "body": "reviewed body",
            "finish_summary_index": self.index,
        }
        order: list[str] = []
        archived = self.root / plan["task"]["archive_locator"]
        readiness = {
            "ready": True,
            "body_file": "pr-body.md",
            "publish_inputs": {"closeout_plan_digest": plan["plan_digest"]},
            "publish_inputs_sha256": "b" * 64,
        }
        verification = {"status": "passed"}
        pr = {"number": 105, "url": "https://github.com/owner/repo/pull/105"}
        args = finish_args(dry_run=False, expected_plan_digest=plan["plan_digest"])
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "load_task_start_context", return_value=self.context),
            mock.patch.object(gtt, "assert_workspace_boundary"),
            mock.patch.object(gtt, "task_dir_is_archived", return_value=False),
            mock.patch.object(gtt, "prepare_closeout", return_value=prepared),
            mock.patch.object(gtt, "require_gh_auth", side_effect=lambda _root: order.append("auth")),
            mock.patch.object(gtt, "load_issue_scope_ledger", return_value=self.ledger),
            mock.patch.object(gtt, "closeout_evidence_is_committed", return_value=False),
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "run_stdout", return_value=self.head),
            mock.patch.object(gtt, "validate_publish_identity_and_remote_head"),
            mock.patch.object(gtt, "build_pr_readiness_snapshot", return_value=(self.task_dir / "pr-readiness.json", readiness)),
            mock.patch.object(gtt, "execute_marketplace_verification", side_effect=lambda *a, **k: (order.append("verifier"), verification)[1]),
            mock.patch.object(gtt, "closeout_passed_marketplace_evidence", return_value={"type": "remote_marketplace_verification", "status": "passed"}),
            mock.patch.object(gtt, "commit_closeout_evidence_metadata", side_effect=lambda *a: (order.append("evidence-commit"), {"commit": self.head})[1]),
            mock.patch.object(gtt, "ensure_closeout_draft_pr", side_effect=lambda *a: (order.append("draft"), pr)[1]),
            mock.patch.object(gtt, "build_final_archive_projection", side_effect=lambda *a: (order.append("projection"), (self.task_dir / "finish-summary.json", {}))[1]),
            mock.patch.object(gtt, "execute_archive_metadata_transaction", side_effect=lambda *a: (order.append("archive"), (archived, {"commit": self.head}))[1]),
            mock.patch.object(gtt, "ensure_closeout_pr_ready", side_effect=lambda *a: (order.append("ready"), {"status": "ready"})[1]),
        ):
            result = gtt.cmd_finish_work(args)
        self.assertEqual(result["stage"], "ready")
        self.assertEqual(order, ["auth", "verifier", "evidence-commit", "draft", "projection", "archive", "ready"])

    def test_draft_to_ready_failure_has_no_repo_mutation(self) -> None:
        plan = self.build_plan()
        body = (self.task_dir / "pr-body.md").read_text(encoding="utf-8")
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

    def test_active_completed_archive_move_recovery_skips_verifier_and_pr_create(self) -> None:
        plan = self.build_plan()
        gtt.write_json(self.task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT, plan)
        completed = dict(self.task, status="completed")
        gtt.write_json(self.task_dir / "task.json", completed)
        gtt.write_json(self.task_dir / gtt.FINISH_SUMMARY_ARTIFACT, {"schema_version": 1})
        archived = self.root / plan["task"]["archive_locator"]
        args = finish_args(dry_run=False, expected_plan_digest=plan["plan_digest"])
        body = (self.task_dir / "pr-body.md").read_text(encoding="utf-8")
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
            "isDraft": True,
            "headRefOid": self.head,
        }
        with (
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", self.gate, [])),
            mock.patch.object(gtt, "load_issue_scope_ledger", return_value=self.ledger),
            mock.patch.object(gtt, "closeout_evidence_is_committed", return_value=True),
            mock.patch.object(gtt, "validate_finish_summary"),
            mock.patch.object(gtt, "validate_closeout_active_projection"),
            mock.patch.object(gtt, "validate_closeout_evidence_commit"),
            mock.patch.object(gtt, "current_head", return_value=self.head),
            mock.patch.object(gtt, "require_gh_auth"),
            mock.patch.object(gtt, "resolve_closeout_pull_request", return_value=draft),
            mock.patch.object(gtt, "execute_archive_metadata_transaction", return_value=(archived, {"commit": self.head})) as archive,
            mock.patch.object(gtt, "ensure_closeout_pr_ready", return_value={"status": "ready"}),
            mock.patch.object(gtt, "execute_marketplace_verification") as verifier,
            mock.patch.object(gtt, "create_pull_request") as create,
        ):
            result = gtt.resume_active_archive_move(self.root, args, {}, self.task_dir, self.context)
        self.assertEqual(result["entry_state"], "archive_moved")
        archive.assert_called_once()
        verifier.assert_not_called()
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


    def run_production_finish_case(self, failed_stage: str | None = None) -> dict[str, object]:
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
            workflow = root / "trellis/workflows/guru-team/workflow.md"
            workflow.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_root / "trellis/workflows/guru-team/workflow.md", workflow)
            config = root / ".trellis/guru-team/config.yml"
            config.parent.mkdir(parents=True, exist_ok=True)
            config.write_text("github_repo: owner/repo\npublish:\n  remote: origin\n", encoding="utf-8")
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
                "base_branch": "main",
            }
            gate = {
                "head": "pending",
                "generated_at": "2026-07-11T00:00:00Z",
                "changed_files": [
                    "trellis/workflows/guru-team/workflow.md"
                    if failed_stage == "verifier"
                    else "README.md"
                ],
                "issue_scope": {"close_issues_reviewed": [{"number": 105}]},
            }
            ledger = {
                "primary_issue": {"number": 105, "acceptance_evidence": ["passed"]},
                "close_issues": [{"number": 105, "acceptance_evidence": ["passed"]}],
                "related_issues": [],
                "followup_issues": [],
            }
            index = json.loads(json.dumps(self.index, ensure_ascii=False))
            gtt.write_json(task_dir / "task-start-context.json", context)
            gtt.write_json(task_dir / "task.json", task)
            gtt.write_json(task_dir / "review-gate.json", {"fixture": True})
            gtt.write_json(task_dir / "issue-scope-ledger.json", ledger)
            gtt.write_json(task_dir / "finish-summary-index.json", index)
            (task_dir / "review.md").write_text("# 审查报告\n\n最终审查通过。\n", encoding="utf-8")
            (task_dir / "pr-body.md").write_text(
                valid_pr_body("生产 closeout 集成。").replace("Closes #18", "Closes #105"),
                encoding="utf-8",
            )
            subprocess.run(["git", "add", ".trellis/tasks"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "reviewed"], cwd=root, check=True)
            reviewed_head = gtt.run_stdout(["git", "rev-parse", "HEAD"], cwd=root)
            gate["head"] = reviewed_head

            pr_store: dict[str, object] = {}
            original_run = gtt.run
            injected_stage = failed_stage
            archive_pushed = False
            transition_attempts: list[str] = []
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

            def git_transition_stage(command: list[str]) -> str:
                archived = root / f".trellis/tasks/archive/{datetime.now().strftime('%Y-%m')}/{task_dir.name}"
                if archived.is_dir() or (
                    (task_dir / "task.json").is_file()
                    and gtt.read_json(task_dir / "task.json").get("status") == "completed"
                ):
                    return "archive-push" if command[:2] == ["git", "push"] else "archive-commit"
                if (task_dir / gtt.CLOSEOUT_PLAN_ARTIFACT).is_file():
                    return "evidence-push" if command[:2] == ["git", "push"] else "evidence-commit"
                return "content-push"

            def command_failure(command: list[str], check: bool, message: str) -> subprocess.CompletedProcess[str]:
                if check:
                    raise subprocess.CalledProcessError(1, command, stderr=message)
                return subprocess.CompletedProcess(command, 1, "", message)

            def fake_external_run(
                command: list[str], cwd: Path | None = None, check: bool = True
            ) -> subprocess.CompletedProcess[str]:
                nonlocal archive_pushed
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
                    if injected_stage == "projection":
                        record_transition("projection")
                        (task_dir / "review.md").unlink()
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
                            "body": (task_dir / "pr-body.md").read_text(encoding="utf-8"),
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
                if command and command[0] == "trellis":
                    record_transition("verifier")
                    if injected_stage == "verifier":
                        return subprocess.CompletedProcess(command, 1, "", "injected verifier")
                    verifier_root = Path(cwd or root)
                    installed_workflow = verifier_root / ".trellis/workflow.md"
                    installed_workflow.parent.mkdir(parents=True, exist_ok=True)
                    installed_workflow.write_bytes(workflow.read_bytes())
                    if "--create-new" in command:
                        (verifier_root / ".trellis/workflow.md.new").write_bytes(workflow.read_bytes())
                    installed_schemas = verifier_root / ".trellis/guru-team/schemas"
                    installed_schemas.parent.mkdir(parents=True, exist_ok=True)
                    if not installed_schemas.exists():
                        shutil.copytree(root / "trellis/workflows/guru-team/schemas", installed_schemas)
                    (verifier_root / ".trellis/config.yaml").write_text(
                        "session_auto_commit: false\n", encoding="utf-8"
                    )
                    (verifier_root / ".gitignore").write_text(
                        ".trellis/.runtime/\n.trellis/workspace/\n", encoding="utf-8"
                    )
                    return subprocess.CompletedProcess(command, 0, "", "")
                if command and command[0].endswith("/trellis/presets/guru-team/scripts/bash/apply.sh"):
                    return subprocess.CompletedProcess(command, 0, "", "")
                return original_run(command, cwd=cwd, check=check)

            archive_locator = f".trellis/tasks/archive/{datetime.now().strftime('%Y-%m')}/{task_dir.name}"
            archived_path = root / archive_locator

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
                return {
                    "active_locator": ".trellis/tasks/07-11-closeout" if task_dir.is_dir() else None,
                    "active_path": str(task_dir) if task_dir.is_dir() else None,
                    "archive_locator": archive_locator if archived_path.is_dir() else None,
                    "archive_path": str(archived_path) if archived_path.is_dir() else None,
                    "task_status": (
                        gtt.read_json(current_task_dir / "task.json").get("status")
                        if current_task_dir is not None
                        else None
                    ),
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
                }

            dry_args = finish_args(
                root=str(root),
                task=str(task_dir),
                repo="owner/repo",
                base_branch="main",
                remote="origin",
                title="#105 重构 finish-work 收尾事务",
                body_file=str(task_dir / "pr-body.md"),
                finish_summary_index_file=str(task_dir / "finish-summary-index.json"),
                dry_run=True,
            )
            with (
                mock.patch.object(gtt, "assert_workspace_boundary"),
                mock.patch.object(
                    gtt,
                    "validate_review_gate",
                    return_value=(task_dir / "review-gate.json", gate, []),
                ),
                mock.patch.object(gtt, "run", side_effect=fake_external_run),
            ):
                if failed_stage in {
                    "prepare",
                    "raw-remote-control",
                    "remote-identity",
                    "remote-transport",
                }:
                    if failed_stage == "prepare":
                        (task_dir / "finish-summary-index.json").write_text(
                            "{}\n", encoding="utf-8"
                        )
                    with self.assertRaises(gtt.WorkflowError):
                        gtt.cmd_finish_work(dry_args)
                    failed_state = exact_state()
                    if failed_stage == "prepare":
                        gtt.write_json(task_dir / "finish-summary-index.json", index)
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
                    if failed_stage is None:
                        result = gtt.cmd_finish_work(formal_args)
                        failed_state = {}
                        reentry_events = []
                    else:
                        with self.assertRaises((gtt.WorkflowError, subprocess.CalledProcessError)):
                            gtt.cmd_finish_work(formal_args)
                        failed_state = exact_state()
                        injected_stage = None
                        if failed_stage == "projection":
                            (task_dir / "review.md").write_text(
                                "# 审查报告\n\n最终审查通过。\n", encoding="utf-8"
                            )
                        formal_args.expected_plan_digest = preview["closeout_plan_digest"]
                        reentry_offset = len(transition_attempts)
                        if failed_stage == "plan-digest":
                            transition_attempts.append("plan-digest")
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
            self.assertEqual(gtt.read_json(archived / "task.json")["status"], "completed")
            self.assertEqual(local_head, remote_head)
            self.assertEqual(pr_store["isDraft"], False)
            self.assertEqual(
                gtt.read_json(archived / gtt.FINISH_SUMMARY_ARTIFACT)["github"]["pr_url"],
                pr_store["url"],
            )
            self.assertEqual(gtt.git_status_paths(root), [])
            final_state = exact_state()
            evidence_head = gtt.run_stdout(["git", "rev-parse", f"{local_head}^"], cwd=root)
            return {
                "project_root": str(root),
                "failed_state": failed_state,
                "final_state": final_state,
                "reentry_events": reentry_events,
                "all_transition_attempts": transition_attempts,
                "reviewed_sha": reviewed_head,
                "evidence_sha": evidence_head,
                "archive_sha": local_head,
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
        self.assertEqual(failed["dirty_paths"], set())
        self.assertEqual(failed["staged_paths"], set())
        self.assertEqual(failed["local_sha"], result["reviewed_sha"])
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
        self.assertEqual(failed["dirty_paths"], set())
        self.assertEqual(failed["staged_paths"], set())
        self.assertEqual(failed["local_sha"], result["reviewed_sha"])
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
        self.assertEqual(failed["dirty_paths"], set())
        self.assertEqual(failed["staged_paths"], set())
        self.assertEqual(failed["local_sha"], result["reviewed_sha"])
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
            "verifier",
            "evidence-commit",
            "evidence-push",
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
        evidence_paths = {
            f"{active}/closeout-plan.json",
            f"{active}/pr-readiness.json",
        }
        archive_move_paths = {
            f"{active}/{name}"
            for name in [
                "closeout-plan.json", "finish-summary-index.json", "issue-scope-ledger.json",
                "pr-body.md", "pr-readiness.json", "review-gate.json", "review.md",
                "task-start-context.json", "task.json",
            ]
        } | {
            f"{archive}/{name}"
            for name in [
                "closeout-plan.json", "finish-summary-index.json", "finish-summary.json",
                "issue-scope-ledger.json", "pr-body.md", "pr-readiness.json",
                "review-gate.json", "review.md", "task-start-context.json", "task.json",
            ]
        }
        expected = {
            "prepare": (active, None, "in_progress", {f"{active}/finish-summary-index.json"}, set(), "reviewed", None, None, None, None, None),
            "plan-digest": (active, None, "in_progress", set(), set(), "reviewed", None, None, None, None, None),
            "content-push": (active, None, "in_progress", set(), set(), "reviewed", None, None, None, None, None),
            "verifier": (
                active, None, "in_progress",
                evidence_paths | {f"{active}/issue-scope-ledger.json", f"{active}/marketplace-verification.json"},
                set(), "reviewed", "reviewed", None, None, None, None,
            ),
            "evidence-commit": (active, None, "in_progress", evidence_paths, evidence_paths, "reviewed", "reviewed", None, None, None, None),
            "evidence-push": (active, None, "in_progress", set(), set(), "evidence", "reviewed", None, None, None, None),
            "draft": (active, None, "in_progress", set(), set(), "evidence", "evidence", None, None, None, None),
            "projection": (active, None, "in_progress", {f"{active}/review.md"}, set(), "evidence", "evidence", "evidence", True, "OPEN", 105),
            "archive-move": (active, None, "in_progress", {f"{active}/finish-summary.json"}, set(), "evidence", "evidence", "evidence", True, "OPEN", 105),
            "archive-commit": (None, archive, "completed", archive_move_paths, archive_move_paths, "evidence", "evidence", "evidence", True, "OPEN", 105),
            "archive-push": (None, archive, "completed", set(), set(), "archive", "evidence", "evidence", True, "OPEN", 105),
            "remote-head": (None, archive, "completed", set(), set(), "archive", "archive", "archive", True, "OPEN", 105),
            "ready": (None, archive, "completed", set(), set(), "archive", "archive", "archive", True, "OPEN", 105),
        }
        transition_order = stages
        for stage in stages:
            with self.subTest(stage=stage):
                result = self.run_production_finish_case(stage)
                state = result["failed_state"]
                sha = {
                    "reviewed": result["reviewed_sha"],
                    "evidence": result["evidence_sha"],
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

    def valid_backfill_summary(self) -> dict[str, object]:
        payload = self.valid_summary()
        payload["generator"] = "guru-team.finish-summary-backfill"
        payload["task"]["artifact_dir"] = ""  # type: ignore[index]
        payload["git"]["base_branch"] = ""  # type: ignore[index]
        payload["git"]["branch"] = ""  # type: ignore[index]
        payload["index"]["search_terms"]["branches"] = []  # type: ignore[index]
        payload["index"]["retrieval_text"] = gtt.finish_summary_retrieval_text(  # type: ignore[index]
            payload["task"]["title"], payload["index"]  # type: ignore[index]
        )
        payload["backfill"] = {
            "generated": True,
            "generated_at": "2026-07-10T00:00:00Z",
            "source_artifacts": ["task.json"],
            "missing_fields": ["task.artifact_dir"],
            "confidence": "partial",
        }
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
            gtt.finish_summary_retrieval_text(
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

    def test_valid_backfill_summary_requires_missing_field_evidence(self) -> None:
        payload = self.valid_backfill_summary()
        self.assertEqual(gtt.finish_summary_errors(payload), [])

    def test_backfill_exact_problem_fallback_allows_only_the_title_boundary(self) -> None:
        titles = [
            "07-07-051-prepare-task-naming-quality-gate",
            "07-07-059-refresh-base-freshness",
            "07-07-062-subagent-timeout-stale-policy",
            "07-08-078-review-report-chinese-language",
        ]
        for title in titles:
            with self.subTest(title=title):
                payload = self.valid_backfill_summary()
                payload["task"]["title"] = title  # type: ignore[index]
                payload["index"]["problem"] = (  # type: ignore[index]
                    f"{title}；旧行为：历史 artifact 未记录。"
                )
                payload["index"]["retrieval_text"] = gtt.finish_summary_retrieval_text(  # type: ignore[index]
                    title, payload["index"]  # type: ignore[index]
                )
                self.assertEqual(gtt.finish_summary_errors(payload), [])

    def test_normal_finish_work_rejects_the_backfill_title_boundary_pattern(self) -> None:
        payload = self.valid_summary()
        title = payload["task"]["title"]  # type: ignore[index]
        payload["index"]["problem"] = f"{title}；旧行为：历史 artifact 未记录。"  # type: ignore[index]
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

    def test_backfill_non_exact_problem_fallback_keeps_duplicate_rejection(self) -> None:
        payload = self.valid_backfill_summary()
        title = payload["task"]["title"]  # type: ignore[index]
        payload["index"]["problem"] = f"{title}；旧行为：旧 artifact 未记录。"  # type: ignore[index]
        payload["index"]["retrieval_text"] = gtt.finish_summary_retrieval_text(  # type: ignore[index]
            title, payload["index"]  # type: ignore[index]
        )

        self.assertIn(
            "index.retrieval_text contains adjacent duplicate clauses.",
            gtt.finish_summary_errors(payload),
        )

    def test_backfill_exact_fallback_keeps_other_adjacent_duplicate_rejection(self) -> None:
        payload = self.valid_backfill_summary()
        title = payload["task"]["title"]  # type: ignore[index]
        payload["index"]["problem"] = f"{title}；旧行为：历史 artifact 未记录。"  # type: ignore[index]
        payload["index"]["outcome"] = "历史结果已记录；历史结果已记录。"  # type: ignore[index]
        payload["index"]["retrieval_text"] = gtt.finish_summary_retrieval_text(  # type: ignore[index]
            title, payload["index"]  # type: ignore[index]
        )
        errors = gtt.finish_summary_errors(payload)

        self.assertIn("index.outcome contains adjacent duplicate clauses.", errors)
        self.assertIn("index.retrieval_text contains adjacent duplicate clauses.", errors)

    def test_finish_summary_schema_key_limits_and_path_refs_with_stdlib(self) -> None:
        schema = self.finish_summary_schema()
        properties = schema["properties"]  # type: ignore[index]
        definitions = schema["$defs"]  # type: ignore[index]

        self.assertEqual(properties["github"]["properties"]["pr_url"]["maxLength"], 1000)  # type: ignore[index]
        self.assertEqual(properties["index"]["properties"]["contract_changes"]["maxItems"], 20)  # type: ignore[index]
        backfill = properties["backfill"]["properties"]  # type: ignore[index]
        self.assertEqual(backfill["source_artifacts"]["maxItems"], 20)  # type: ignore[index]
        self.assertEqual(backfill["source_artifacts"]["items"]["$ref"], "#/$defs/taskPath")  # type: ignore[index]
        self.assertEqual(backfill["missing_fields"]["maxItems"], 30)  # type: ignore[index]
        self.assertEqual(backfill["missing_fields"]["items"]["maxLength"], 200)  # type: ignore[index]
        self.assertEqual(definitions["taskPath"]["$ref"], "#/$defs/safePath")  # type: ignore[index]
        self.assertEqual(definitions["optionalSafePath"]["anyOf"][1]["$ref"], "#/$defs/safePath")  # type: ignore[index]
        self.assertEqual(definitions["affectedSurface"]["properties"]["paths"]["items"]["$ref"], "#/$defs/safePath")  # type: ignore[index]
        self.assertEqual(definitions["contractChange"]["properties"]["source_artifact"]["$ref"], "#/$defs/optionalSafePath")  # type: ignore[index]
        self.assertEqual(definitions["searchTerms"]["properties"]["paths"]["items"]["$ref"], "#/$defs/safePath")  # type: ignore[index]

    def test_optional_draft_2020_12_cross_validation(self) -> None:
        normal = self.valid_summary()
        backfill = self.valid_backfill_summary()
        invalid_path = self.valid_summary()
        invalid_path["git"]["changed_paths"] = ["docs\\file.md"]  # type: ignore[index]
        invalid_url = self.valid_summary()
        invalid_url["github"]["pr_url"] = "https://github.com/" + ("o" * 980) + "/repo/pull/123"  # type: ignore[index]

        self.assertEqual(self.draft_schema_errors(normal), [])
        self.assertEqual(self.draft_schema_errors(backfill), [])
        self.assertTrue(self.draft_schema_errors(invalid_path))
        self.assertTrue(self.draft_schema_errors(invalid_url))

    def test_backfill_source_artifacts_must_exist_when_task_dir_is_available(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / ".trellis/tasks/archive/2026-07/07-10-task"
            task_dir.mkdir(parents=True)
            (task_dir / "task.json").write_text("{}\n", encoding="utf-8")
            (task_dir / "design.md").write_text("# Design\n", encoding="utf-8")
            payload = self.valid_backfill_summary()
            payload["task"]["slug"] = task_dir.name  # type: ignore[index]
            payload["task"]["archive_dir"] = task_dir.relative_to(root).as_posix()  # type: ignore[index]

            self.assertEqual(gtt.finish_summary_errors(payload, task_dir=task_dir), [])
            (task_dir / "task.json").unlink()
            contextual_errors = gtt.finish_summary_errors(payload, task_dir=task_dir)
            self.assertTrue(any("source_artifacts[0] does not exist" in error for error in contextual_errors))
            self.assertEqual(gtt.finish_summary_errors(payload), [])

    def test_backfill_schema_and_python_reject_path_and_limit_drift(self) -> None:
        exact_limit = self.valid_backfill_summary()
        exact_limit["backfill"]["source_artifacts"] = [  # type: ignore[index]
            f"source-{index}.json" for index in range(20)
        ]
        self.assertEqual(gtt.finish_summary_errors(exact_limit), [])
        schema = self.finish_summary_schema()
        backfill_schema = schema["properties"]["backfill"]["properties"]  # type: ignore[index]
        self.assertEqual(
            len(exact_limit["backfill"]["source_artifacts"]),  # type: ignore[index]
            backfill_schema["source_artifacts"]["maxItems"],  # type: ignore[index]
        )

        cases: list[tuple[str, dict[str, object]]] = []
        for name, source_artifacts in [
            ("parent", ["../task.json"]),
            ("protected", [".trellis/workspace/task.json"]),
            ("max_items", [f"source-{index}.json" for index in range(21)]),
        ]:
            payload = self.valid_backfill_summary()
            payload["backfill"]["source_artifacts"] = source_artifacts  # type: ignore[index]
            cases.append((name, payload))
        missing_length = self.valid_backfill_summary()
        missing_length["backfill"]["missing_fields"] = [  # type: ignore[index]
            "task.artifact_dir",
            "x" * 201,
        ]
        cases.append(("missing_length", missing_length))

        for name, payload in cases:
            with self.subTest(name=name):
                self.assertTrue(gtt.finish_summary_errors(payload))
                if name in {"parent", "protected"}:
                    source_path = payload["backfill"]["source_artifacts"][0]  # type: ignore[index]
                    self.assertFalse(self.safe_path_schema_valid(source_path))
                elif name == "max_items":
                    self.assertGreater(
                        len(payload["backfill"]["source_artifacts"]),  # type: ignore[index]
                        backfill_schema["source_artifacts"]["maxItems"],  # type: ignore[index]
                    )
                else:
                    self.assertGreater(
                        len(payload["backfill"]["missing_fields"][1]),  # type: ignore[index]
                        backfill_schema["missing_fields"]["items"]["maxLength"],  # type: ignore[index]
                    )

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

        backfill_path = self.valid_backfill_summary()
        backfill_path["backfill"]["source_artifacts"] = [  # type: ignore[index]
            ".trellis/.runtime/task.json"
        ]
        cases.append(("backfill.source_artifacts", ".trellis/.runtime/task.json", backfill_path))

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

        backfill_path = self.valid_backfill_summary()
        backfill_path["backfill"]["source_artifacts"] = ["docs\\file.md"]  # type: ignore[index]
        cases.append(("backfill.source_artifacts", backfill_path))

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

    def test_summary_rejects_unknown_keys_and_wrong_generator_branch(self) -> None:
        payload = self.valid_summary()
        payload["summary"] = "legacy"
        payload["backfill"] = {}
        errors = gtt.finish_summary_errors(payload)
        self.assertTrue(any("top-level keys" in error for error in errors))

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
                stdout=".trellis/workspace/legacy.txt\0safe.txt\0",
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
                index_payload = self.valid_ai_index()
                index_payload["index"]["contract_changes"] = self.contract_changes(19)  # type: ignore[index]
                summary = gtt.build_finish_summary(
                    root,
                    task_dir,
                    task_context,
                    ledger,
                    index_payload,
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
            self.assertEqual(len(summary["index"]["contract_changes"]), 20)
            self.assertNotIn("marketplace_verification", summary["artifacts"])
            retrieval_lines = summary["index"]["retrieval_text"].splitlines()
            fixed_before = gtt.FINISH_SUMMARY_PROTECTED_PATH_FILTER_CONTRACT["before"]
            fixed_after = gtt.FINISH_SUMMARY_PROTECTED_PATH_FILTER_CONTRACT["after"]
            previous_after = self.contract_changes(19)[-1]["after"]
            self.assertEqual(retrieval_lines.count(fixed_before), 1)
            self.assertEqual(retrieval_lines.count(fixed_after), 1)
            self.assertLess(retrieval_lines.index(previous_after), retrieval_lines.index(fixed_before))
            self.assertLess(retrieval_lines.index(fixed_before), retrieval_lines.index(fixed_after))
            retrieval_text = "\n".join(retrieval_lines)
            self.assertNotIn(".trellis/workspace/private-journal.md", retrieval_text)
            self.assertNotIn("private-journal.md", retrieval_text)
            self.assertFalse(any(re.search(r"过滤(?:了)?\s*1|1\s*个", line) for line in retrieval_lines))
            self.assertEqual(gtt.finish_summary_errors(summary, task_dir=task_dir), [])

    def test_pr_rewrite_applies_sanitized_paths_and_is_recovery_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / ".trellis/tasks/archive/2026-07/07-10-097-finish-summary-replaces-add-session"
            task_dir.mkdir(parents=True)
            (task_dir / "design.md").write_text("# Design\n", encoding="utf-8")
            summary = self.valid_summary()
            summary["task"]["archive_dir"] = task_dir.relative_to(root).as_posix()  # type: ignore[index]
            summary["artifacts"] = gtt.finish_summary_artifacts(task_dir)
            self.assertNotIn("marketplace_verification", summary["artifacts"])
            gtt.write_json(task_dir / gtt.FINISH_SUMMARY_ARTIFACT, summary)
            (task_dir / gtt.MARKETPLACE_VERIFICATION_ARTIFACT).write_text("{}\n", encoding="utf-8")
            snapshot = (["README.md"], True, False)

            first_updated = None
            with mock.patch.object(gtt, "finish_summary_git_path_snapshot", return_value=snapshot):
                for _attempt in range(2):
                    _path, updated = gtt.update_finish_summary_for_pr(
                        root,
                        task_dir,
                        {"base_branch": "main", "base_ref": "main"},
                        "https://github.com/castbox/guru-trellis/pull/123",
                    )
                    if first_updated is None:
                        first_updated = json.loads(json.dumps(updated, ensure_ascii=False))

            self.assertEqual(updated["git"]["changed_paths"], ["README.md"])
            self.assertEqual(updated["index"]["search_terms"]["paths"], ["README.md"])
            self.assertEqual(
                updated["artifacts"]["marketplace_verification"],
                gtt.MARKETPLACE_VERIFICATION_ARTIFACT,
            )
            self.assertEqual(updated, first_updated)
            self.assertEqual(sum(
                item.get("contract") == "finish-summary protected path filtering"
                for item in updated["index"]["contract_changes"]
            ), 1)
            retrieval_lines = updated["index"]["retrieval_text"].splitlines()
            fixed_before = gtt.FINISH_SUMMARY_PROTECTED_PATH_FILTER_CONTRACT["before"]
            fixed_after = gtt.FINISH_SUMMARY_PROTECTED_PATH_FILTER_CONTRACT["after"]
            self.assertEqual(retrieval_lines.count(fixed_before), 1)
            self.assertEqual(retrieval_lines.count(fixed_after), 1)
            self.assertLess(retrieval_lines.index(fixed_before), retrieval_lines.index(fixed_after))
            retrieval_text = "\n".join(retrieval_lines)
            self.assertNotIn(".trellis/workspace/private-journal.md", retrieval_text)
            self.assertNotIn("private-journal.md", retrieval_text)
            self.assertFalse(any(re.search(r"过滤(?:了)?\s*1|1\s*个", line) for line in retrieval_lines))
            self.assertEqual(
                updated["index"]["retrieval_text"],
                gtt.finish_summary_retrieval_text(updated["task"]["title"], updated["index"]),
            )

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
                index_payload = self.valid_ai_index()
                index_payload["index"]["contract_changes"] = self.contract_changes(19)  # type: ignore[index]
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
                        index_payload,
                        "a" * 40,
                    )

                self.assertEqual(len(summary["index"]["contract_changes"]), 20)  # type: ignore[index]
                self.assert_snapshot_unavailable_summary(
                    summary,
                    undisclosed_values=undisclosed_values,
                )

    def test_pr_rewrite_unavailable_snapshot_replaces_filter_fact_and_rederives_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / ".trellis/tasks/archive/2026-07/07-10-097-finish-summary-replaces-add-session"
            task_dir.mkdir(parents=True)
            (task_dir / "design.md").write_text("# Design\n", encoding="utf-8")
            summary = self.valid_summary()
            summary["task"]["archive_dir"] = task_dir.relative_to(root).as_posix()  # type: ignore[index]
            summary["index"]["contract_changes"].append(  # type: ignore[index]
                dict(gtt.FINISH_SUMMARY_PROTECTED_PATH_FILTER_CONTRACT)
            )
            summary["index"]["retrieval_text"] = gtt.finish_summary_retrieval_text(  # type: ignore[index]
                summary["task"]["title"], summary["index"]  # type: ignore[index]
            )
            gtt.write_json(task_dir / gtt.FINISH_SUMMARY_ARTIFACT, summary)
            failed = mock.Mock(
                returncode=1,
                stdout="README.md\0.trellis/workspace/private-journal.md\0",
                stderr="final diff denied for secret/ref",
            )
            with mock.patch.object(gtt, "run", return_value=failed):
                _path, updated = gtt.update_finish_summary_for_pr(
                    root,
                    task_dir,
                    {"base_branch": "main", "base_ref": "secret/ref"},
                    "https://github.com/castbox/guru-trellis/pull/123",
                )

        self.assert_snapshot_unavailable_summary(
            updated,
            undisclosed_values=[
                "README.md",
                "private-journal.md",
                "final diff denied",
                "secret/ref",
            ],
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

    def test_backfill_source_artifact_paths_use_exact_identity(self) -> None:
        payload = self.valid_backfill_summary()
        payload["backfill"]["source_artifacts"] = [  # type: ignore[index]
            ".trellis/guru-team/extension.json",
            "trellis/guru-team-extension.json",
        ]

        self.assertEqual(gtt.finish_summary_errors(payload), [])

        payload["backfill"]["source_artifacts"] = ["task.json", "task.json"]  # type: ignore[index]
        self.assertIn(
            "backfill.source_artifacts[1] duplicates backfill.source_artifacts[0].",
            gtt.finish_summary_errors(payload),
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

    def test_ai_index_contract_change_limit_reserves_filter_fact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = Path(tmp) / ".trellis/tasks/07-10-task"
            task_dir.mkdir(parents=True)
            index_path = task_dir / gtt.FINISH_SUMMARY_INDEX_ARTIFACT
            payload = self.valid_ai_index()
            payload["index"]["contract_changes"] = self.contract_changes(19)  # type: ignore[index]
            self.assertEqual(gtt.finish_summary_index_errors(payload["index"], final=False), [])
            gtt.write_json(index_path, payload)
            with mock.patch.object(gtt, "repo_root", return_value=Path(tmp)):
                gtt.load_finish_summary_index(task_dir, str(index_path))

            payload["index"]["contract_changes"] = self.contract_changes(20)  # type: ignore[index]
            errors = gtt.finish_summary_index_errors(payload["index"], final=False)
            self.assertTrue(any("exceeds 19 items" in error for error in errors))
            gtt.write_json(index_path, payload)
            with (
                mock.patch.object(gtt, "repo_root", return_value=Path(tmp)),
                self.assertRaises(gtt.WorkflowError),
            ):
                gtt.load_finish_summary_index(task_dir, str(index_path))

    def test_ai_index_loader_accepts_bare_repo_relative_and_absolute_task_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / ".trellis/tasks/07-10-task"
            task_dir.mkdir(parents=True)
            index_path = task_dir / "finish-summary-index.json"
            gtt.write_json(index_path, self.valid_ai_index())
            with mock.patch.object(gtt, "repo_root", return_value=root):
                for value in [
                    "finish-summary-index.json",
                    ".trellis/tasks/07-10-task/finish-summary-index.json",
                    str(index_path),
                ]:
                    with self.subTest(value=value):
                        loaded_path, _payload = gtt.load_finish_summary_index(task_dir, value)
                        self.assertEqual(loaded_path, index_path.resolve())

    def test_ai_index_loader_rejects_task_external_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / ".trellis/tasks/task"
            task_dir.mkdir(parents=True)
            external = root / "finish-summary-index.json"
            gtt.write_json(external, self.valid_ai_index())
            with mock.patch.object(gtt, "repo_root", return_value=root), self.assertRaises(gtt.WorkflowError):
                gtt.load_finish_summary_index(task_dir, str(external))

    def test_retrieval_fixture_hits_pre_and_post_pr_signals(self) -> None:
        payload = self.valid_summary()
        haystack = json.dumps(payload["index"], ensure_ascii=False)
        for token in ["#97", "codex/097", "workflow.md", "add_session.py", "session_auto_commit", "index.search_terms", "cmd_finish_work", "workspace journal 冲突", "完成摘要改为"]:
            self.assertIn(token, haystack)
        payload["github"]["pr_url"] = "https://github.com/castbox/guru-trellis/pull/123"  # type: ignore[index]
        payload["index"]["search_terms"]["pr_refs"] = ["PR #123"]  # type: ignore[index]
        self.assertEqual(gtt.finish_summary_errors(payload), [])
        self.assertIn("PR #123", json.dumps(payload["index"], ensure_ascii=False))


class FinishSummaryBackfillTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        archive = root / ".trellis/tasks/archive/2026-07"
        archive.mkdir(parents=True)
        return tmp, root, archive

    def args(self, root: Path, **overrides: object) -> argparse.Namespace:
        values: dict[str, object] = {
            "root": str(root),
            "json": True,
            "dry_run": True,
            "write": False,
            "force": False,
            "task": None,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def write_complete_sources(self, task_dir: Path, paths: list[str] | None = None) -> list[str]:
        paths = paths or ["trellis/workflows/guru-team/workflow.md"]
        gtt.write_json(task_dir / "task.json", {
            "title": "#100 历史完成摘要回填",
            "base_branch": "main",
            "branch": "feat/100-backfill",
            "commit": "a" * 40,
            "pr_url": "https://github.com/castbox/guru-trellis/pull/100",
        })
        gtt.write_json(task_dir / "issue-scope-ledger.json", {
            "primary_issue": {"number": 100},
            "close_issues": [{"number": 100}],
            "related_issues": [{"number": 53}],
            "followup_issues": [{"number": 98}],
        })
        gtt.write_json(task_dir / "review-gate.json", {
            "task_dir": f".trellis/tasks/{task_dir.name}",
            "base_branch": "main",
            "branch": "feat/100-backfill",
            "head": "a" * 40,
            "changed_files": paths,
            "summary": "历史任务完成摘要已通过最终审查。",
        })
        (task_dir / "prd.md").write_text(
            "# Backfill\n\n## 问题\n\n旧归档任务缺少完成摘要。\n",
            encoding="utf-8",
        )
        (task_dir / "design.md").write_text(
            "# Design\n\n## 合同变化\n\n"
            "| contract | before | after | source_artifact |\n"
            "| --- | --- | --- | --- |\n"
            "| history index | 缺少索引 | 写入完成摘要 | design.md |\n",
            encoding="utf-8",
        )
        (task_dir / "pr-body.md").write_text(
            "# PR\n\n## 变更摘要\n\n- 新增 backfill-finish-summary.sh 历史迁移命令。\n",
            encoding="utf-8",
        )
        return [
            "task.json", "issue-scope-ledger.json", "review-gate.json",
            "prd.md", "design.md", "pr-body.md",
        ]

    def test_parser_requires_exactly_one_mode(self) -> None:
        parser = gtt.build_parser()
        with self.assertRaises(SystemExit) as missing:
            parser.parse_args(["backfill-finish-summary"])
        self.assertEqual(missing.exception.code, 2)
        with self.assertRaises(SystemExit) as conflict:
            parser.parse_args(["backfill-finish-summary", "--dry-run", "--write"])
        self.assertEqual(conflict.exception.code, 2)

    def test_empty_archive_and_table_renderer(self) -> None:
        tmp, root, _archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        payload = gtt.cmd_backfill_finish_summary(self.args(root))
        self.assertEqual(payload["scanned_tasks"], 0)
        self.assertEqual(payload["errors"], [])
        table = gtt.render_finish_summary_backfill_table(payload)
        self.assertIn("scanned_tasks: 0", table)
        self.assertIn("STATUS\tARCHIVE_DIR", table)

    def test_task_path_rejects_absolute_parent_active_and_symlink_escape(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        task_dir = archive / "task"
        task_dir.mkdir()
        gtt.write_json(task_dir / "task.json", {})
        active = root / ".trellis/tasks/active"
        active.mkdir(parents=True)
        outside = root / "outside"
        outside.mkdir()
        (archive / "escape").symlink_to(outside, target_is_directory=True)
        for value in [
            str(task_dir),
            "../task",
            ".trellis/tasks/active",
            ".trellis/tasks/archive//2026-07/task",
            ".trellis/tasks/archive/2026-07/task/",
            ".trellis/tasks/archive/2026-07/escape",
        ]:
            with self.subTest(value=value), self.assertRaises(gtt.WorkflowError) as raised:
                gtt.resolve_finish_summary_backfill_task(root, value)
            self.assertEqual(raised.exception.exit_code, 2)
        self.assertEqual(
            gtt.resolve_finish_summary_backfill_task(root, task_dir.relative_to(root).as_posix()),
            task_dir.resolve(),
        )

    def test_task_root_rejects_group_and_nested_markers_for_all_write_modes(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        task_dir = archive / "task"
        task_dir.mkdir()
        gtt.write_json(task_dir / "task.json", {"title": "真实任务"})
        nested = task_dir / "arbitrary/nested"
        nested.mkdir(parents=True)
        gtt.write_json(nested / "task.json", {"title": "嵌套伪任务"})
        plain_child = task_dir / "plain-child"
        plain_child.mkdir()
        group = archive / "date-group"
        group.mkdir()
        targets = [archive, group, plain_child, nested]
        modes = [
            {"dry_run": True, "write": False, "force": False},
            {"dry_run": False, "write": True, "force": False},
            {"dry_run": False, "write": True, "force": True},
        ]
        for target in targets:
            for mode in modes:
                with self.subTest(target=target, mode=mode), self.assertRaises(gtt.WorkflowError) as raised:
                    gtt.cmd_backfill_finish_summary(self.args(
                        root,
                        task=target.relative_to(root).as_posix(),
                        **mode,
                    ))
                self.assertEqual(raised.exception.exit_code, 2)
                self.assertFalse((target / "finish-summary.json").exists())
        self.assertEqual(gtt.discover_finish_summary_backfill_tasks(root), [task_dir.resolve()])

    def test_complete_builder_uses_schema_validator_and_kind_chunks(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        task_dir = archive / "complete"
        task_dir.mkdir()
        paths = [f"trellis/workflows/guru-team/file-{index:03d}.md" for index in range(101)]
        source_artifacts = self.write_complete_sources(task_dir, paths)
        sources, loaded, errors = gtt.load_finish_summary_backfill_sources(task_dir)
        self.assertEqual(errors, [])
        self.assertEqual(set(loaded), set(source_artifacts))
        payload = gtt.build_finish_summary_backfill(root, task_dir, sources, loaded)
        self.assertEqual(payload["backfill"]["confidence"], "complete")
        self.assertEqual(payload["task"]["artifact_dir"], ".trellis/tasks/complete")
        self.assertEqual(payload["index"]["problem"], "旧归档任务缺少完成摘要。")
        self.assertEqual(payload["index"]["outcome"], "历史任务完成摘要已通过最终审查。")
        self.assertEqual(
            payload["index"]["changed_behavior"],
            ["新增 backfill-finish-summary.sh 历史迁移命令。"],
        )
        self.assertEqual(payload["index"]["contract_changes"], [{
            "contract": "history index",
            "before": "缺少索引",
            "after": "写入完成摘要",
            "source_artifact": "design.md",
        }])
        self.assertEqual([len(item["paths"]) for item in payload["index"]["affected_surfaces"]], [100, 1])
        self.assertEqual(payload["git"]["changed_paths"], paths)
        self.assertEqual(
            sorted(path for surface in payload["index"]["affected_surfaces"] for path in surface["paths"]),
            paths,
        )
        self.assertNotIn("summary", payload)
        self.assertNotIn("keywords", payload)
        self.assertEqual(gtt.finish_summary_errors(payload, task_dir=task_dir), [])
        self.assertEqual(
            payload["index"]["retrieval_text"],
            gtt.finish_summary_retrieval_text(payload["task"]["title"], payload["index"]),
        )
        self.assertNotIn("完成摘要 backfill 已生成", payload["index"]["search_terms"]["phrases"])

    def test_partial_builder_falls_back_source_issue_independently(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        task_dir = archive / "partial"
        task_dir.mkdir()
        gtt.write_json(task_dir / "task.json", {
            "title": "#100 历史完成摘要回填",
            "source_issue": "issue #100",
        })
        gtt.write_json(task_dir / "issue-scope-ledger.json", {
            "primary_issue": None,
            "close_issues": [],
            "related_issues": [{"number": 53}],
            "followup_issues": [{"number": 98}],
        })
        sources, loaded, errors = gtt.load_finish_summary_backfill_sources(task_dir)
        self.assertEqual(errors, [])
        payload = gtt.build_finish_summary_backfill(root, task_dir, sources, loaded)
        self.assertEqual(payload["backfill"]["confidence"], "partial")
        self.assertEqual(payload["github"]["source_issues"], [100])
        self.assertNotIn("github.source_issues", payload["backfill"]["missing_fields"])

    def test_pr_body_list_outcome_preserves_complete_behavior_with_two_narrow_boundaries(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        task_dir = archive / "pr-body-list-only"
        task_dir.mkdir()
        gtt.write_json(task_dir / "task.json", {"title": "PR body 列表任务"})
        (task_dir / "pr-body.md").write_text(
            "# PR\n\n## 变更摘要\n\n"
            "- 回填历史完成摘要。\n"
            "- 保留完整行为列表。\n",
            encoding="utf-8",
        )
        sources, loaded, errors = gtt.load_finish_summary_backfill_sources(task_dir)
        self.assertEqual(errors, [])
        payload = gtt.build_finish_summary_backfill(root, task_dir, sources, loaded)

        self.assertEqual(payload["index"]["outcome"], "回填历史完成摘要。")
        self.assertEqual(payload["index"]["changed_behavior"], [
            "回填历史完成摘要。",
            "保留完整行为列表。",
        ])
        self.assertEqual(gtt.finish_summary_errors(payload, task_dir=task_dir), [])
        self.assertIn(
            "index.retrieval_text contains adjacent duplicate clauses.",
            gtt.finish_summary_errors(payload),
        )

        tampered_retrieval = json.loads(json.dumps(payload, ensure_ascii=False))
        tampered_retrieval["index"]["retrieval_text"] += "\n篡改派生文本。"
        self.assertIn(
            "index.retrieval_text must equal the deterministic derived text.",
            gtt.finish_summary_errors(tampered_retrieval, task_dir=task_dir),
        )

        incomplete_behavior = json.loads(json.dumps(payload, ensure_ascii=False))
        incomplete_behavior["index"]["changed_behavior"] = incomplete_behavior["index"]["changed_behavior"][:1]
        incomplete_behavior["index"]["retrieval_text"] = gtt.finish_summary_retrieval_text(
            incomplete_behavior["task"]["title"], incomplete_behavior["index"]
        )
        self.assertIn(
            "index.retrieval_text contains adjacent duplicate clauses.",
            gtt.finish_summary_errors(incomplete_behavior, task_dir=task_dir),
        )

        other_duplicate = json.loads(json.dumps(payload, ensure_ascii=False))
        other_duplicate["index"]["changed_behavior"][1] = other_duplicate["index"]["changed_behavior"][0]
        other_duplicate["index"]["retrieval_text"] = gtt.finish_summary_retrieval_text(
            other_duplicate["task"]["title"], other_duplicate["index"]
        )
        other_errors = gtt.finish_summary_errors(other_duplicate, task_dir=task_dir)
        self.assertIn(
            "index.changed_behavior[1] duplicates index.changed_behavior[0] after normalization.",
            other_errors,
        )
        self.assertIn("index.retrieval_text contains adjacent duplicate clauses.", other_errors)

        (task_dir / "pr-body.md").write_text(
            "# PR\n\n## 变更摘要\n\n- 来源已被篡改。\n",
            encoding="utf-8",
        )
        self.assertIn(
            "index.retrieval_text contains adjacent duplicate clauses.",
            gtt.finish_summary_errors(payload, task_dir=task_dir),
        )

    def test_pr_body_paragraph_and_higher_outcome_sources_do_not_use_list_exception(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        task_dir = archive / "pr-body-priority"
        task_dir.mkdir()
        gtt.write_json(task_dir / "task.json", {"title": "PR body 优先级任务"})
        (task_dir / "pr-body.md").write_text(
            "# PR\n\n## 变更摘要\n\n段落结论优先。\n\n- 列表行为仍然保留。\n",
            encoding="utf-8",
        )
        sources, loaded, errors = gtt.load_finish_summary_backfill_sources(task_dir)
        self.assertEqual(errors, [])
        paragraph_payload = gtt.build_finish_summary_backfill(root, task_dir, sources, loaded)
        self.assertEqual(paragraph_payload["index"]["outcome"], "段落结论优先。")
        self.assertEqual(paragraph_payload["index"]["changed_behavior"], ["列表行为仍然保留。"])
        self.assertEqual(gtt.finish_summary_errors(paragraph_payload, task_dir=task_dir), [])

        gtt.write_json(task_dir / "review-gate.json", {"summary": "审查结论优先。"})
        sources, loaded, errors = gtt.load_finish_summary_backfill_sources(task_dir)
        self.assertEqual(errors, [])
        gate_payload = gtt.build_finish_summary_backfill(root, task_dir, sources, loaded)
        self.assertEqual(gate_payload["index"]["outcome"], "审查结论优先。")
        self.assertEqual(gtt.finish_summary_errors(gate_payload, task_dir=task_dir), [])

    def test_commit_sources_use_first_non_empty_priority_and_reject_invalid_values(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        task_dir = archive / "commit-priority"
        task_dir.mkdir()
        gtt.write_json(task_dir / "task.json", {"title": "提交优先级", "commit": "a" * 40})
        gtt.write_json(task_dir / "review-gate.json", {"head": "b" * 40})
        gtt.write_json(task_dir / "pr-readiness.json", {"commits": ["c" * 40]})
        sources, loaded, errors = gtt.load_finish_summary_backfill_sources(task_dir)
        self.assertEqual(errors, [])
        self.assertEqual(
            gtt.build_finish_summary_backfill(root, task_dir, sources, loaded)["git"]["commits"],
            ["a" * 40],
        )

        sources["task.json"].pop("commit")
        self.assertEqual(
            gtt.build_finish_summary_backfill(root, task_dir, sources, loaded)["git"]["commits"],
            ["b" * 40],
        )
        sources["review-gate.json"].pop("head")
        self.assertEqual(
            gtt.build_finish_summary_backfill(root, task_dir, sources, loaded)["git"]["commits"],
            ["c" * 40],
        )
        sources["task.json"]["commit"] = []
        with self.assertRaises(gtt.WorkflowError):
            gtt.build_finish_summary_backfill(root, task_dir, sources, loaded)

    def test_complete_confidence_requires_branch(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        task_dir = archive / "missing-branch"
        task_dir.mkdir()
        self.write_complete_sources(task_dir)
        task = gtt.read_json(task_dir / "task.json")
        task.pop("branch")
        gtt.write_json(task_dir / "task.json", task)
        gate = gtt.read_json(task_dir / "review-gate.json")
        gate.pop("branch")
        gtt.write_json(task_dir / "review-gate.json", gate)
        sources, loaded, errors = gtt.load_finish_summary_backfill_sources(task_dir)
        self.assertEqual(errors, [])
        payload = gtt.build_finish_summary_backfill(root, task_dir, sources, loaded)
        self.assertEqual(payload["git"]["branch"], "")
        self.assertEqual(payload["backfill"]["confidence"], "partial")

    def test_minimal_confidence_requires_absence_of_all_non_title_evidence(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        cases = {
            "artifact-dir": ({"artifact_dir": ".trellis/tasks/artifact-dir"}, {}),
            "base-branch": ({"base_branch": "main"}, {}),
            "branch": ({"branch": "feat/history"}, {}),
            "commit": ({"commit": "a" * 40}, {}),
            "description": ({"description": "历史任务需要回填。"}, {}),
            "source-issue": ({"source_issue": "issue #100"}, {}),
            "pr-url": ({"pr_url": "https://github.com/castbox/guru-trellis/pull/100"}, {}),
            "review-summary": ({}, {"review-gate.json": {"summary": "历史任务已完成审查。"}}),
            "prd-problem": ({}, {"prd.md": "# PRD\n\n## 问题\n\n旧归档缺少索引。\n"}),
            "implement-check": ({}, {"implement.md": "# Plan\n\n- [x] 回填历史完成摘要。\n"}),
            "contract-table": ({}, {"design.md": (
                "# Design\n\n## 合同变化\n\n"
                "| contract | before | after | source_artifact |\n"
                "| --- | --- | --- | --- |\n"
                "| history | 无索引 | 有索引 | design.md |\n"
            )}),
        }
        for name, (task_delta, files) in cases.items():
            with self.subTest(name=name):
                task_dir = archive / name
                task_dir.mkdir()
                gtt.write_json(task_dir / "task.json", {"title": f"{name} 任务", **task_delta})
                for filename, content in files.items():
                    path = task_dir / filename
                    if isinstance(content, dict):
                        gtt.write_json(path, content)
                    else:
                        path.write_text(content, encoding="utf-8")
                sources, loaded, errors = gtt.load_finish_summary_backfill_sources(task_dir)
                self.assertEqual(errors, [])
                payload = gtt.build_finish_summary_backfill(root, task_dir, sources, loaded)
                self.assertEqual(payload["backfill"]["confidence"], "partial")

    def test_search_terms_adds_completion_fallback_only_when_required(self) -> None:
        common = {
            "task_title": "历史任务",
            "task_slug": "history-task",
            "problem": "旧行为缺少索引",
            "outcome": "结果已有记录",
            "surfaces": [{"change": "workflow 类路径有差异"}],
            "source_artifacts": ["task.json"],
            "changed_paths": ["workflow.md"],
        }
        without_marker = gtt.backfill_search_terms(
            changed_behavior=["调整历史索引"],
            **common,
        )
        self.assertIn("历史归档 task 已完成", without_marker["phrases"])
        with_marker = gtt.backfill_search_terms(
            changed_behavior=["新增历史索引"],
            **common,
        )
        self.assertNotIn("历史归档 task 已完成", with_marker["phrases"])
        self.assertNotIn("完成摘要 backfill 已生成", with_marker["phrases"])

    def test_search_terms_skips_only_exact_fallback_at_a_duplicate_phrase_edge(self) -> None:
        title = "minimal-task"
        problem = f"{title}；旧行为：历史 artifact 未记录。"
        outcome = f"{title}；非目标：历史 artifact 未记录。"
        common = {
            "task_title": title,
            "problem": problem,
            "outcome": outcome,
            "changed_behavior": ["历史归档 task 已完成"],
            "surfaces": [{"change": "历史 artifact 未记录 changed_paths"}],
            "source_artifacts": [],
            "changed_paths": [],
        }

        same_slug = gtt.backfill_search_terms(task_slug=title, **common)
        self.assertNotIn(gtt.backfill_clean_text(problem, 60), same_slug["phrases"])
        self.assertNotIn(gtt.backfill_clean_text(outcome, 60), same_slug["phrases"])

        distinct_slug = gtt.backfill_search_terms(task_slug="07-11-minimal-task", **common)
        self.assertIn(gtt.backfill_clean_text(problem, 60), distinct_slug["phrases"])
        self.assertIn(gtt.backfill_clean_text(outcome, 60), distinct_slug["phrases"])

        non_exact = gtt.backfill_search_terms(
            task_slug=title,
            **{**common, "problem": f"{title}；旧行为：其它 artifact 未记录。"},
        )
        self.assertIn(
            gtt.backfill_clean_text(f"{title}；旧行为：其它 artifact 未记录。", 60),
            non_exact["phrases"],
        )

    def test_completion_fallback_matches_the_eight_historical_fixtures(self) -> None:
        root = Path(gtt.__file__).resolve().parents[5]
        expected = [
            "07-04-7-require-pr-readiness-review-before",
            "07-06-39-review-branch-findings-reviewer-only",
            "07-06-40-workflow-state-completed-closeout-pr",
            "07-06-41-task-system-task-py-create",
            "07-09-064-docs-ssot-plan-contract",
            "07-09-065-docs-ssot-phase2-sync-gate",
            "07-09-066-docs-ssot-phase3-enforcement",
            "07-10-073-trellis-doc-markdown-links",
        ]
        actual: list[str] = []
        for task_dir in gtt.discover_finish_summary_backfill_tasks(root):
            existing_path = task_dir / gtt.FINISH_SUMMARY_ARTIFACT
            if not existing_path.is_file():
                continue
            existing = gtt.read_json(existing_path)
            if existing.get("generator") != gtt.FINISH_SUMMARY_BACKFILL_GENERATOR:
                continue
            sources, source_artifacts, errors = gtt.load_finish_summary_backfill_sources(task_dir)
            self.assertEqual(errors, [], task_dir.name)
            payload = gtt.build_finish_summary_backfill(root, task_dir, sources, source_artifacts)
            if "历史归档 task 已完成" in payload["index"]["search_terms"]["phrases"]:
                actual.append(task_dir.name)

        self.assertEqual(actual, expected)

    def test_minimal_builder_has_fallback_surface_and_missing_fields(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        task_dir = archive / "minimal-task"
        task_dir.mkdir()
        payload = gtt.build_finish_summary_backfill(root, task_dir, {}, [])
        self.assertEqual(payload["backfill"]["confidence"], "minimal")
        self.assertEqual(payload["index"]["affected_surfaces"][0]["paths"], [])
        self.assertEqual(
            payload["index"]["problem"],
            "minimal-task；旧行为：历史 artifact 未记录。",
        )
        self.assertEqual(
            payload["index"]["outcome"],
            "minimal-task；非目标：历史 artifact 未记录。",
        )
        self.assertIn("task.artifact_dir", payload["backfill"]["missing_fields"])
        self.assertIn("github.pr_url", payload["backfill"]["missing_fields"])
        self.assertEqual(gtt.finish_summary_errors(payload, task_dir=task_dir), [])

    def test_table_preview_matches_json_for_complete_partial_and_minimal(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        complete = archive / "complete"
        complete.mkdir()
        self.write_complete_sources(complete)
        partial = archive / "partial"
        partial.mkdir()
        gtt.write_json(partial / "task.json", {
            "title": "部分证据任务",
            "description": "历史归档任务需要完成摘要。",
        })
        minimal = archive / "minimal"
        minimal.mkdir()
        gtt.write_json(minimal / "task.json", {})

        payload = gtt.cmd_backfill_finish_summary(self.args(root))
        self.assertEqual(payload["scanned_tasks"], 3)
        self.assertEqual({item["confidence"] for item in payload["to_write"]}, {"complete", "partial", "minimal"})
        table = gtt.render_finish_summary_backfill_table(payload)
        for item in payload["to_write"]:
            source_artifacts = ",".join(item["source_artifacts"]) or "-"
            missing_fields = ",".join(item["missing_fields"]) or "-"
            row = (
                f"to_write\t{item['archive_dir']}\t{item['target']}\t"
                f"{source_artifacts}\t{missing_fields}\t{item['confidence']}"
            )
            self.assertIn(row, table)

    def test_issue_number_parser_does_not_take_unrelated_url_digits(self) -> None:
        self.assertEqual(gtt.backfill_issue_number("https://github.com/team2/repo/issues/100"), 100)
        self.assertEqual(gtt.backfill_issue_number("issue #98"), 98)
        self.assertIsNone(gtt.backfill_issue_number("team2/repo"))

    def test_surface_limit_fails_closed_without_truncation(self) -> None:
        prefixes = [
            "trellis/workflows/", "trellis/presets/", ".agents/skills/",
            ".codex/", ".trellis/spec/", ".trellis/guru-team/",
            ".trellis/tasks/", "misc/",
        ]
        paths: list[str] = []
        for prefix in prefixes:
            paths.extend(f"{prefix}file-{index:03d}.txt" for index in range(101))
        paths.extend(f"trellis/workflows/guru-team/extra-{index:03d}.txt" for index in range(800))
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.backfill_affected_surfaces(sorted(paths), "too many")
        self.assertGreater(raised.exception.payload["surface_count"], 20)

    def test_corrupt_json_is_reported_and_batch_continues(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        broken = archive / "broken"
        broken.mkdir()
        (broken / "task.json").write_text("{broken", encoding="utf-8")
        good = archive / "good"
        good.mkdir()
        (good / "task.json").write_text('{"title":"正常历史任务"}\n', encoding="utf-8")
        payload = gtt.cmd_backfill_finish_summary(self.args(root))
        self.assertEqual(payload["scanned_tasks"], 2)
        self.assertEqual(len(payload["to_write"]), 2)
        self.assertEqual(len(payload["errors"]), 1)
        self.assertEqual(payload["errors"][0]["artifact"], "task.json")

    def test_discovery_and_loader_exclude_nested_and_symlink_sources(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        task_dir = archive / "task"
        task_dir.mkdir()
        (task_dir / "task.json").write_text('{"title":"真实任务"}\n', encoding="utf-8")
        nested = task_dir / "research/nested"
        nested.mkdir(parents=True)
        (nested / "task.json").write_text('{"title":"不能扫描"}\n', encoding="utf-8")
        outside = root / "outside.json"
        outside.write_text('{"title":"外部文件"}\n', encoding="utf-8")
        (task_dir / "review-gate.json").symlink_to(outside)
        self.assertEqual(gtt.discover_finish_summary_backfill_tasks(root), [task_dir.resolve()])
        sources, artifacts, errors = gtt.load_finish_summary_backfill_sources(task_dir)
        self.assertIn("task.json", sources)
        self.assertNotIn("review-gate.json", sources)
        self.assertEqual(artifacts, ["task.json"])
        self.assertEqual(errors[0]["artifact"], "review-gate.json")

    def test_source_os_error_does_not_expose_absolute_path(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        task_dir = archive / "unreadable"
        task_dir.mkdir()
        source = task_dir / "task.json"
        source.write_text('{}\n', encoding="utf-8")
        error = PermissionError(13, "Permission denied", str(source.resolve()))
        with mock.patch.object(Path, "read_text", side_effect=error):
            sources, artifacts, errors = gtt.load_finish_summary_backfill_sources(task_dir)
        self.assertEqual(sources, {})
        self.assertEqual(artifacts, [])
        self.assertEqual(errors, [{"artifact": "task.json", "error": "PermissionError: Permission denied"}])
        self.assertNotIn(str(root.resolve()), errors[0]["error"])

    def test_write_skip_force_and_post_write_validation(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        task_dir = archive / "write-task"
        task_dir.mkdir()
        (task_dir / "task.json").write_text('{"title":"写入历史任务"}\n', encoding="utf-8")
        task_arg = task_dir.relative_to(root).as_posix()
        write = gtt.cmd_backfill_finish_summary(self.args(root, dry_run=False, write=True, task=task_arg))
        self.assertEqual(len(write["to_write"]), 1)
        summary_path = task_dir / "finish-summary.json"
        first = summary_path.read_text(encoding="utf-8")
        self.assertEqual(gtt.finish_summary_errors(gtt.read_json(summary_path), task_dir=task_dir), [])
        skipped = gtt.cmd_backfill_finish_summary(self.args(root, task=task_arg))
        self.assertEqual(skipped["skipped"][0]["reason"], "finish-summary exists")
        self.assertEqual(summary_path.read_text(encoding="utf-8"), first)
        summary_path.write_text("{}\n", encoding="utf-8")
        forced = gtt.cmd_backfill_finish_summary(self.args(root, dry_run=False, write=True, force=True, task=task_arg))
        self.assertEqual(len(forced["to_write"]), 1)
        self.assertNotEqual(summary_path.read_text(encoding="utf-8"), "{}\n")
        self.assertEqual(gtt.finish_summary_errors(gtt.read_json(summary_path), task_dir=task_dir), [])

    def test_force_without_write_exits_two(self) -> None:
        tmp, root, _archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.cmd_backfill_finish_summary(self.args(root, force=True))
        self.assertEqual(raised.exception.exit_code, 2)

    def test_cli_exit_codes_zero_one_and_two(self) -> None:
        tmp, root, archive = self.make_repo()
        self.addCleanup(tmp.cleanup)
        script = Path(gtt.__file__).resolve()
        ok = subprocess.run(
            [sys.executable, str(script), "backfill-finish-summary", "--root", str(root), "--json", "--dry-run"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(ok.returncode, 0)
        self.assertEqual(json.loads(ok.stdout)["errors"], [])
        broken = archive / "broken"
        broken.mkdir()
        (broken / "task.json").write_text("{broken", encoding="utf-8")
        partial = subprocess.run(
            [sys.executable, str(script), "backfill-finish-summary", "--root", str(root), "--json", "--dry-run"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(partial.returncode, 1)
        self.assertEqual(len(json.loads(partial.stdout)["errors"]), 1)
        invalid = subprocess.run(
            [sys.executable, str(script), "backfill-finish-summary", "--root", str(root), "--json", "--dry-run", "--force"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(invalid.returncode, 2)
        self.assertEqual(json.loads(invalid.stderr)["status"], "error")
