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
        "journal_title": None,
        "journal_summary": None,
        "commit": None,
        "from_trellis_finish_work": True,
        "skip_archive": False,
        "skip_journal": False,
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
        gtt.write_json(self.task_dir / "issue-scope-ledger.json", {
            "close_issues": [{
                "number": 18,
                "title": "Publish boundary",
                "acceptance_evidence": ["ok", dict(self.PENDING_REMOTE_MARKETPLACE_EVIDENCE)],
            }],
            "related_issues": [],
            "followup_issues": [],
        })

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
        ]

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
        self.assertIn("finish-work.sh", str(raised.exception))
        self.assertEqual(raised.exception.payload["recovery_flag"], "--recovery-after-finish-work")

    def test_publish_pr_checks_workspace_boundary_before_review_gate(self) -> None:
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "load_task_start_context", return_value={"base_branch": "main"}),
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
        patches = self.patch_publish_success_path()
        for patcher in patches:
            patcher.start()
        try:
            with (
                mock.patch.object(gtt, "require_gh_auth"),
                mock.patch.object(gtt, "run_stdout"),
                mock.patch.object(gtt, "current_head", side_effect=["a" * 40, "b" * 40, "b" * 40]),
                mock.patch.object(gtt, "execute_marketplace_verification", return_value={
                    "status": "passed",
                    "verified_head": "a" * 40,
                    "remote_head": "a" * 40,
                    "steps": [{"passed": True}],
                }),
                mock.patch.object(gtt, "write_remote_marketplace_evidence", side_effect=self.record_passed_marketplace_evidence),
                mock.patch.object(gtt, "commit_marketplace_verification_metadata", return_value={"committed": True}),
                mock.patch.object(gtt, "validate_marketplace_verification", return_value=(self.task_dir / "marketplace-verification.json", {}, [])),
                mock.patch.object(gtt, "run") as run,
            ):
                run.return_value = mock.Mock(
                    returncode=0,
                    stdout="https://github.com/owner/repo/pull/91\n",
                    stderr="",
                )
                payload = gtt.cmd_publish_pr(
                    publish_args(
                        recovery_after_finish_work=True,
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
                gtt.cmd_publish_pr(publish_args(recovery_after_finish_work=True, dry_run=False, body_file=str(body_path)))
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
        self.assertEqual(raised.exception.payload["body_source"], "generated")
        self.assertFalse(raised.exception.payload["reviewed_source_ok"])

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
            "head": "abc123",
            "conclusion": {"passed": True, "summary": "finish-work 后发布。"},
            "changed_files": ["trellis/workflows/guru-team/workflow.md"],
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
        self.assertEqual(raised.exception.payload["body_source"], "generated")
        self.assertFalse(raised.exception.payload["reviewed_source_ok"])

    def test_finish_work_calls_publish_with_internal_marker(self) -> None:
        body_path = self.task_dir / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("finish-work 传递 reviewed body file。"), encoding="utf-8")
        gate = {
            "head": "abc123",
            "conclusion": {"passed": True, "summary": "finish-work 后发布。"},
            "changed_files": ["trellis/workflows/guru-team/workflow.md"],
        }
        archived_task_dir = self.root / ".trellis/tasks/archive/2026-07/07-04-publish-boundary"
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_start_context", return_value={"base_branch": "main"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "assert_workspace_boundary"),
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", gate, [])),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "recent_work_commits", return_value=["abc123"]),
            mock.patch.object(gtt, "run") as run,
            mock.patch.object(gtt, "commit_if_metadata_dirty", return_value=None),
            mock.patch.object(gtt, "resolve_existing_task_dir", return_value=archived_task_dir),
            mock.patch.object(gtt, "cmd_publish_pr", return_value={"status": "dry-run"}) as publish,
        ):
            run.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            payload = gtt.cmd_finish_work(finish_args(body_file=str(body_path), dry_run=False))

        publish.assert_called_once()
        publish_args_obj = publish.call_args.args[0]
        self.assertTrue(publish_args_obj.from_finish_work)
        self.assertFalse(publish_args_obj.recovery_after_finish_work)
        self.assertTrue(publish_args_obj.allow_metadata_after_gate)
        self.assertEqual(publish_args_obj.task, str(archived_task_dir))
        self.assertEqual(publish_args_obj.body_file, str(archived_task_dir / "reviewed-pr-body.md"))
        self.assertIsNone(publish_args_obj.body_artifact)
        self.assertEqual(payload["publish"]["status"], "dry-run")

    def test_finish_work_migrates_archived_review_gate_before_publish(self) -> None:
        body_path = self.task_dir / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("finish-work 归档后迁移 review gate。"), encoding="utf-8")
        gate = {
            "head": "abc123",
            "conclusion": {"passed": True, "summary": "finish-work 后发布。"},
            "changed_files": ["trellis/workflows/guru-team/workflow.md"],
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
            mock.patch.object(gtt, "migrate_review_gate_for_archived_task", return_value=archive_migration) as migrate,
            mock.patch.object(gtt, "cmd_publish_pr", return_value={"status": "dry-run"}) as publish,
        ):
            run.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            payload = gtt.cmd_finish_work(finish_args(body_file=str(body_path), dry_run=False))

        migrate.assert_called_once_with(self.root, archived_task_dir, {**gtt.DEFAULTS, "github_repo": "owner/repo"})
        self.assertEqual(commit_metadata.call_count, 2)
        publish.assert_called_once()
        self.assertEqual(payload["archive_migration"], archive_migration)
        self.assertEqual(payload["metadata_commit"]["commit"], "migration")

    def test_finish_work_dry_run_returns_plan_without_archive_journal_commit_or_publish(self) -> None:
        body_path = self.task_dir / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("finish-work dry-run 只输出 readiness preview。"), encoding="utf-8")
        gate = {
            "head": "abc123",
            "conclusion": {"passed": True, "summary": "finish-work dry-run preview。"},
            "changed_files": ["trellis/workflows/guru-team/workflow.md"],
        }
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_start_context", return_value={"base_branch": "main"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", gate, [])),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "recent_work_commits", return_value=["abc123"]),
            mock.patch.object(gtt, "current_branch", return_value="codex/27-finish-work-dry-run-readiness"),
            mock.patch.object(gtt, "run") as run,
            mock.patch.object(gtt, "commit_if_metadata_dirty") as commit_metadata,
            mock.patch.object(gtt, "cmd_publish_pr") as publish,
        ):
            payload = gtt.cmd_finish_work(finish_args(body_file=str(body_path)))

        run_commands = [call.args[0] for call in run.call_args_list]
        self.assertNotIn(["python3", "./.trellis/scripts/task.py", "archive", self.task_dir.name], run_commands)
        self.assertFalse(any(command[:3] == ["python3", "./.trellis/scripts/add_session.py", "--title"] for command in run_commands))
        commit_metadata.assert_not_called()
        publish.assert_not_called()
        self.assertEqual(payload["status"], "dry-run")
        self.assertFalse(payload["dry_run_side_effects"])
        self.assertEqual(payload["plan"]["archive"]["task_name"], self.task_dir.name)
        self.assertEqual(payload["plan"]["journal"]["commits"], "abc123")
        self.assertEqual(payload["plan"]["publish"]["repo"], "owner/repo")
        self.assertEqual(payload["plan"]["publish"]["base_branch"], "main")
        self.assertEqual(payload["plan"]["publish"]["head_branch"], "codex/27-finish-work-dry-run-readiness")
        self.assertEqual(payload["plan"]["metadata_commit"]["message"], "chore(trellis): #18 固化任务收尾元数据")
        self.assertEqual(
            payload["plan"]["publish"]["merge_commit"]["subject"],
            "chore(merge): #<pull_request> 合并 #18 完成 Publish boundary",
        )
        self.assertIn("body-file:", payload["checks"]["pr_readiness"]["body_source"])
        self.assertTrue(payload["checks"]["pr_readiness"]["body_quality_ok"])
        self.assertTrue(payload["checks"]["pr_readiness"]["reviewed_source_ok"])

    def test_finish_work_validates_gate_with_metadata_tail_allowed(self) -> None:
        body_path = self.task_dir / "reviewed-pr-body.md"
        body_path.write_text(valid_pr_body("finish-work 校验 gate metadata tail。"), encoding="utf-8")
        gate = {
            "head": "abc123",
            "conclusion": {"passed": True, "summary": "finish-work 后发布。"},
            "changed_files": ["trellis/workflows/guru-team/workflow.md"],
        }
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_task_start_context", return_value={"base_branch": "main"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", gate, [])) as validate_gate,
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "recent_work_commits", return_value=["abc123"]),
            mock.patch.object(gtt, "run") as run,
            mock.patch.object(gtt, "commit_if_metadata_dirty", return_value=None),
            mock.patch.object(gtt, "resolve_existing_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "cmd_publish_pr", return_value={"status": "dry-run"}),
        ):
            run.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            gtt.cmd_finish_work(finish_args(body_file=str(body_path), dry_run=False))

        self.assertTrue(validate_gate.call_args.args[3])


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
        workflow.parent.mkdir(parents=True, exist_ok=True)
        schema.parent.mkdir(parents=True, exist_ok=True)
        workflow.write_text("workflow\n", encoding="utf-8")
        schema.write_text("{}\n", encoding="utf-8")
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
                "runtime_gitignore_present": True,
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
                "workflow_sha256": "", "preview_sha256": "", "task_start_context_schema_sha256": "",
                "runtime_gitignore_present": False, "legacy_handoff_absent": False, "legacy_intake_schema_absent": False,
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
                "artifact_path": gtt.repo_relative(root, artifact), "artifact_sha256": artifact_sha,
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
                    workflow.parent.mkdir(parents=True, exist_ok=True)
                    schema.parent.mkdir(parents=True, exist_ok=True)
                    workflow.write_text("workflow", encoding="utf-8")
                    schema.write_text("{}", encoding="utf-8")
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
                    (project / ".gitignore").write_text(".trellis/.runtime/\n", encoding="utf-8")
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
            "assets": {"workflow_sha256": "", "preview_sha256": "", "task_start_context_schema_sha256": "", "runtime_gitignore_present": False, "legacy_handoff_absent": False, "legacy_intake_schema_absent": False},
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
