#!/usr/bin/env python3
"""Focused tests for Guru Team Trellis companion behavior."""

from __future__ import annotations

import argparse
import json
import re
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
        "user_confirmation": "用户确认进入实现。",
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
        "reviewed_head": None,
        "findings_count": 0,
        "reuse_policy": None,
        "reuse_decision": None,
        "reuse_reason": None,
        "from_round": None,
        "to_round": None,
        "decision_head": None,
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
        (self.root / ".trellis/.developer").write_text(
            "name=tester\ninitialized_at=2026-07-04T00:00:00\n",
            encoding="utf-8",
        )

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
        self.assertTrue(payload["handoff_written"])
        self.assertEqual(payload["workspace_path"], str(workspace))
        self.assertTrue((workspace / "handoff.json").exists())
        self.assertFalse((self.root / "handoff.json").exists())
        self.assertEqual(payload["handoff_path"], str(workspace / "handoff.json"))
        self.assertTrue((workspace / ".trellis/.developer").exists())
        self.assertEqual((workspace / ".trellis/.developer").read_text(encoding="utf-8"), "name=tester\ninitialized_at=2026-07-04T00:00:00\n")
        self.assertEqual(payload["preflight"]["developer_identity"]["status"], "copied")

    def test_create_worktree_refreshes_base_before_workspace_creation(self) -> None:
        existing_issue = {
            "number": 42,
            "url": "https://github.com/owner/repo/issues/42",
            "title": "Existing issue",
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
            mock.patch.object(gtt, "prepare_workspace", return_value=("worktree", self.worktree_root / "42-existing", True)) as prepare_workspace,
            mock.patch.object(gtt, "ensure_workspace_developer_identity", return_value={
                "status": "copied",
                "developer": "tester",
            }) as ensure_identity,
        ):
            payload = gtt.cmd_prepare(prepare_args(requirement=["#42"], create_worktree=True))

        refresh.assert_called_once_with(self.root, "main")
        prepare_workspace.assert_called_once()
        ensure_identity.assert_called_once_with(self.root, self.worktree_root / "42-existing", "tester")
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
            "title": "Existing issue",
        }
        (self.root / ".trellis/.developer").unlink()
        workspace = self.worktree_root / "42-existing"
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
            "title": "Existing issue",
        }
        (self.root / ".trellis/.developer").unlink()
        workspace = self.worktree_root / "42-existing"
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
            mock.patch.object(gtt, "load_handoff", return_value={"base_branch": "main"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_status_paths", return_value=[]),
        ]

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
        self.assertEqual(payload["head"], "abc123")
        self.assertEqual(check["status"], "ok")
        self.assertEqual(len(payload["approved_artifacts"]), 3)

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

    def test_check_planning_approval_allows_committed_head_only_when_explicit(self) -> None:
        patches = self.patch_common()
        for patcher in patches:
            patcher.start()
        try:
            gtt.cmd_record_planning_approval(planning_args())
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        with mock.patch.object(gtt, "current_head", return_value="def456"):
            _path, _payload, strict_errors = gtt.validate_planning_approval(self.root, self.task_dir)
        self.assertTrue(any("HEAD" in error for error in strict_errors))

        with (
            mock.patch.object(gtt, "current_head", return_value="def456"),
            mock.patch.object(gtt, "is_ancestor", return_value=True),
        ):
            _path, _payload, relaxed_errors = gtt.validate_planning_approval(
                self.root,
                self.task_dir,
                allow_committed_head=True,
            )
        self.assertEqual(relaxed_errors, [])

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
        review_report.write_text("# Review\n\n旧 final review evidence。\n", encoding="utf-8")
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
                phase2_args(checked_artifact=["review.md", "issue-scope-ledger.json"])
            )
        finally:
            for patcher in reversed(patches):
                patcher.stop()

        review_report.write_text("# Review\n\n新的 fresh final review evidence。\n", encoding="utf-8")
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
            mock.patch.object(gtt, "load_handoff", return_value={"base_branch": "main"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
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
            mock.patch.object(gtt, "load_handoff", return_value={"base_branch": "main"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
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
            mock.patch.object(gtt, "load_handoff", return_value={"base_branch": "main"}),
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
            mock.patch.object(gtt, "load_handoff", return_value={"base_branch": "main"}),
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
            mock.patch.object(gtt, "load_handoff", return_value={"base_branch": "main"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "validate_planning_approval", return_value=(self.task_dir / "planning-approval.json", {}, [])),
            mock.patch.object(gtt, "validate_phase2_check", return_value=(self.task_dir / "phase2-check.json", {}, [])),
            mock.patch.object(gtt, "current_branch", return_value="codex/20-review-gate"),
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "diff_base_ref", return_value="origin/main"),
            mock.patch.object(gtt, "changed_files", return_value=["trellis/workflows/guru-team/workflow.md"]),
        ]

    def write_agent_assignment(self, review_rounds: list[dict[str, object]] | None = None) -> Path:
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
        assignment.write_text(
            gtt.json.dumps(
                {
                    "schema_version": "1.0",
                    "task": ".trellis/tasks/07-04-review-gate",
                    "head": "abc123",
                    "agents": [
                        {
                            "logical_role": "实现代理",
                            "agent_id": "019f315a-f262-7521-acdf-78e4adc99a11",
                            "platform_nickname": "Gibbs",
                            "assigned_at": "2026-07-05T00:00:00Z",
                            "assigned_head": "abc123",
                            "reason": "Codex sub-agent 模式下分配实现代理。",
                        }
                    ],
                    "review_rounds": rounds,
                    "reuse_decisions": [],
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
        review_report.write_text("# Review\n\n无 finding。\n", encoding="utf-8")
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
        self.assertTrue(recorded["modified_at"])
        self.assertTrue((self.task_dir / "review-gate.json").exists())

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

    def test_review_branch_records_observations_without_blocking_pass(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n无 finding，仅有 observation。\n", encoding="utf-8")
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
        review_report.write_text("# Review\n\n无 finding，仅有 follow-up candidate。\n", encoding="utf-8")
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
        review_report.write_text("# Review\n\nfresh 最终放行审查代理给出 0 findings。\n", encoding="utf-8")
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
        review_report.write_text("# Review\n\nfresh final reviewer 完整审查当前 HEAD，0 findings。\n", encoding="utf-8")
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

    def test_review_branch_accepts_prior_head_closure_before_current_final(self) -> None:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\nfresh final reviewer 负责当前 HEAD 完整 diff，历史 closure 不需要随 HEAD 重跑。\n", encoding="utf-8")
        assignment = self.write_agent_assignment(
            [
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
            review_report.write_text("# Review\n\n最终放行审查代理给出 0 findings。\n", encoding="utf-8")
        return gtt.file_digest(self.root, review_report)

    def valid_assignment_summary(self) -> dict[str, object]:
        assignment = self.write_agent_assignment()
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

    def write_archived_gate_with_active_paths(self) -> Path:
        review_report = self.task_dir / "review.md"
        review_report.write_text("# Review\n\n最终放行审查代理给出 0 findings。\n", encoding="utf-8")
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
        gate["verification_evidence"]["agent_assignment"] = self.valid_assignment_summary()
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
        gate["verification_evidence"]["agent_assignment"] = self.valid_assignment_summary()
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

    def test_validate_review_gate_accepts_agent_assignment_summary(self) -> None:
        self.write_gate(review_report=self.valid_report())
        gate = gtt.read_json(self.task_dir / "review-gate.json")
        gate["verification_evidence"]["agent_assignment"] = self.valid_assignment_summary()
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
            mock.patch.object(gtt, "load_handoff", return_value={"task_dir": ".trellis/tasks/07-05-agent-assignment"}),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "git_object_exists", return_value=True),
        ]

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
                "version": "0.6.5",
                "workflow_template_id": "guru-team",
                "requires": {"trellis_cli": ">=0.6.0"},
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
        self.assertEqual(payload["version"], "0.6.5")
        self.assertEqual(payload["workflow_template_id"], "guru-team")
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
        self.assertEqual(payload["guru_team_extension"]["version"], "0.6.5")


if __name__ == "__main__":
    unittest.main()
