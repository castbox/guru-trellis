#!/usr/bin/env python3
"""Focused tests for Guru Team Trellis companion behavior."""

from __future__ import annotations

import argparse
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


def review_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "base_branch": None,
        "pass_gate": True,
        "summary": "Branch Review Gate 通过。",
        "evidence": ["已覆盖 CI/CD、Docker、K8s、migration、Makefile 部署影响判断。"],
        "reviewer": "codex-main-session",
        "review_report": None,
        "finding": [],
        "findings_file": None,
        "dry_run": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class PrepareSideEffectBoundaryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".trellis").mkdir()
        self.worktree_root = self.root / "worktrees"

        self.patches = [
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={
                **gtt.DEFAULTS,
                "github_repo": "owner/repo",
                "handoff_path": "handoff.json",
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
        self.assertFalse(payload["handoff_written"])
        self.assertFalse((self.root / "handoff.json").exists())
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
        self.assertFalse(payload["handoff_written"])
        self.assertFalse((self.root / "handoff.json").exists())

    def test_create_worktree_writes_handoff_only_in_workspace(self) -> None:
        existing_issue = {
            "number": 42,
            "url": "https://github.com/owner/repo/issues/42",
            "title": "Existing issue",
        }
        workspace = self.worktree_root / "42-existing"
        workspace.mkdir(parents=True)
        (workspace / ".git").mkdir()

        with (
            mock.patch.object(gtt, "issue_view", return_value=existing_issue),
            mock.patch.object(gtt, "run_stdout") as run_stdout,
        ):
            payload = gtt.cmd_prepare(prepare_args(requirement=["#42"], create_worktree=True))

        run_stdout.assert_not_called()
        self.assertEqual(payload["source_issue"]["number"], 42)
        self.assertTrue(payload["handoff_written"])
        self.assertEqual(payload["workspace_path"], str(workspace))
        self.assertTrue((workspace / "handoff.json").exists())
        self.assertFalse((self.root / "handoff.json").exists())
        self.assertEqual(payload["handoff_path"], str(workspace / "handoff.json"))

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
            '{"title":"Publish boundary","base_branch":"main"}\n',
            encoding="utf-8",
        )
        (self.task_dir / "issue-scope-ledger.json").write_text(
            '{"close_issues":[{"number":18,"title":"Publish boundary","acceptance_evidence":["ok"]}],'
            '"related_issues":[],"followup_issues":[]}\n',
            encoding="utf-8",
        )

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
            mock.patch.object(gtt, "load_handoff", return_value={
                "base_branch": "main",
            }),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", gate, [])),
            mock.patch.object(gtt, "current_branch", return_value="codex/18-publish-boundary"),
        ]

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

    def test_publish_pr_recovery_dry_run_uses_existing_publish_checks(self) -> None:
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
        ledger_path.write_text(
            '{"close_issues":[{"number":18,"title":"Publish boundary","acceptance_evidence":["ok"]}],'
            '"related_issues":[{"number":19,"title":"Related only"}],"followup_issues":[]}\n',
            encoding="utf-8",
        )
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
        run.assert_not_called()
        self.assertEqual(raised.exception.exit_code, 2)
        self.assertEqual(raised.exception.payload["blocked_step"], "finish-work")
        self.assertEqual(raised.exception.payload["required_entrypoint"], "trellis-finish-work")
        self.assertEqual(raised.exception.payload["intent_flag"], "--from-trellis-finish-work")

    def test_finish_work_calls_publish_with_internal_marker(self) -> None:
        gate = {
            "head": "abc123",
            "conclusion": {"passed": True, "summary": "finish-work 后发布。"},
        }
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_handoff", return_value={"base_branch": "main"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "validate_review_gate", return_value=(self.task_dir / "review-gate.json", gate, [])),
            mock.patch.object(gtt, "has_non_metadata_dirty_paths", return_value=(False, [])),
            mock.patch.object(gtt, "recent_work_commits", return_value=["abc123"]),
            mock.patch.object(gtt, "run") as run,
            mock.patch.object(gtt, "commit_if_metadata_dirty", return_value=None),
            mock.patch.object(gtt, "resolve_existing_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "cmd_publish_pr", return_value={"status": "dry-run"}) as publish,
        ):
            run.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            payload = gtt.cmd_finish_work(finish_args())

        publish.assert_called_once()
        publish_args_obj = publish.call_args.args[0]
        self.assertTrue(publish_args_obj.from_finish_work)
        self.assertFalse(publish_args_obj.recovery_after_finish_work)
        self.assertTrue(publish_args_obj.allow_metadata_after_gate)
        self.assertIsNone(publish_args_obj.body_file)
        self.assertIsNone(publish_args_obj.body_artifact)
        self.assertEqual(payload["publish"]["status"], "dry-run")

    def test_finish_work_validates_gate_with_metadata_tail_allowed(self) -> None:
        gate = {
            "head": "abc123",
            "conclusion": {"passed": True, "summary": "finish-work 后发布。"},
        }
        with (
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value={**gtt.DEFAULTS, "github_repo": "owner/repo"}),
            mock.patch.object(gtt, "load_handoff", return_value={"base_branch": "main"}),
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
            gtt.cmd_finish_work(finish_args())

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
            mock.patch.object(gtt, "load_handoff", return_value={"base_branch": "main"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "current_branch", return_value="codex/20-review-gate"),
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "diff_base_ref", return_value="origin/main"),
            mock.patch.object(gtt, "changed_files", return_value=["trellis/workflows/guru-team/workflow.md"]),
        ]

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
        review_report.write_text("# Review\n\n无 P0/P1/P2 finding。\n", encoding="utf-8")
        patches = self.patch_review_command()
        for patcher in patches:
            patcher.start()
        try:
            payload = gtt.cmd_review_branch(review_args(review_report=str(review_report)))
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        recorded = payload["verification_evidence"]["review_report"]
        self.assertEqual(recorded["path"], ".trellis/tasks/07-04-review-gate/review.md")
        self.assertEqual(recorded["size_bytes"], review_report.stat().st_size)
        self.assertEqual(recorded["sha256"], gtt.hashlib.sha256(review_report.read_bytes()).hexdigest())
        self.assertTrue(recorded["modified_at"])
        self.assertTrue((self.task_dir / "review-gate.json").exists())

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

    def write_gate(self, head: str = "abc123", review_report: dict[str, object] | None = None) -> None:
        gate = {
            "head": head,
            "conclusion": {"passed": True, "summary": "Branch Review Gate 通过。"},
            "verification_evidence": {
                "reviewer": "codex-main-session",
                "review_report": review_report,
                "evidence": ["已覆盖 CI/CD、Docker、K8s、migration、Makefile 部署影响判断。"],
            },
        }
        (self.task_dir / "review-gate.json").write_text(
            gtt.json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def valid_report(self) -> dict[str, object]:
        return {
            "path": ".trellis/tasks/07-04-review-gate/review.md",
            "sha256": "a" * 64,
            "size_bytes": 32,
            "modified_at": "2026-07-04T00:00:00+00:00",
        }

    def test_validate_review_gate_rejects_reviewer_only_passed_gate(self) -> None:
        self.write_gate(review_report=None)
        with mock.patch.object(gtt, "current_head", return_value="abc123"):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertTrue(any("review_report" in error for error in errors))

    def test_validate_review_gate_requires_modified_at(self) -> None:
        report = self.valid_report()
        report.pop("modified_at")
        self.write_gate(review_report=report)
        with mock.patch.object(gtt, "current_head", return_value="abc123"):
            _, _, errors = gtt.validate_review_gate(self.root, self.task_dir, gtt.DEFAULTS, False)

        self.assertIn("Branch Review Gate review_report 缺少 modified_at。", errors)

    def test_validate_review_gate_accepts_metadata_only_tail_when_allowed(self) -> None:
        self.write_gate(head="old123", review_report=self.valid_report())
        with (
            mock.patch.object(gtt, "current_head", return_value="new123"),
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


if __name__ == "__main__":
    unittest.main()
