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


def review_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "root": None,
        "json": True,
        "task": None,
        "base_branch": None,
        "pass_gate": True,
        "summary": "Branch Review Gate 通过：已审查完整 diff，未发现阻塞问题。",
        "evidence": [
            "审查范围：origin/main...HEAD，覆盖文档、代码、测试、Trellis artifacts、脚本、schema、preset overlay 和 issue ledger。",
            "部署影响：本次仅修改 Trellis workflow companion，不新增 API、worker、CI/CD、容器、K8s、DB migration 或 Makefile。",
        ],
        "reviewer": "codex-main-session",
        "review_report": None,
        "finding": None,
        "findings_file": None,
        "dry_run": True,
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


class ReviewGateReportRequiredTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".trellis/guru-team").mkdir(parents=True)
        self.task_dir = self.root / ".trellis/tasks/07-04-review"
        self.task_dir.mkdir(parents=True)
        (self.task_dir / "task.json").write_text(
            '{"title":"review gate","base_branch":"main","branch":"codex/review"}',
            encoding="utf-8",
        )
        (self.task_dir / "issue-scope-ledger.json").write_text(
            '{"close_issues":[],"related_issues":[],"followup_issues":[]}',
            encoding="utf-8",
        )
        self.handoff = {
            "base_branch": "main",
            "issue_scope_ledger": {"close_issues": [], "related_issues": [], "followup_issues": []},
        }
        self.config = {
            **gtt.DEFAULTS,
            "review_gate": {
                **gtt.DEFAULTS["review_gate"],
                "require_deployment_impact_evidence": True,
            },
        }

        self.patches = [
            mock.patch.object(gtt, "repo_root", return_value=self.root),
            mock.patch.object(gtt, "load_config", return_value=self.config),
            mock.patch.object(gtt, "load_handoff", return_value=self.handoff),
            mock.patch.object(gtt, "resolve_task_dir", return_value=self.task_dir),
            mock.patch.object(gtt, "current_branch", return_value="codex/review"),
            mock.patch.object(gtt, "current_head", return_value="abc123"),
            mock.patch.object(gtt, "diff_base_ref", return_value="origin/main"),
            mock.patch.object(gtt, "changed_files", return_value=["trellis/workflows/guru-team/workflow.md"]),
        ]
        for patcher in self.patches:
            patcher.start()

    def tearDown(self) -> None:
        for patcher in reversed(self.patches):
            patcher.stop()
        self.tmp.cleanup()

    def test_pass_gate_requires_review_report_even_with_reviewer(self) -> None:
        with self.assertRaises(gtt.WorkflowError) as raised:
            gtt.cmd_review_branch(review_args())

        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("--review-report", str(raised.exception))
        self.assertIn("cannot replace", str(raised.exception))

    def test_pass_gate_accepts_review_report_and_records_digest(self) -> None:
        report = self.task_dir / "review.md"
        report.write_text("# Branch Review Gate 审查报告\n\n未发现阻塞问题。\n", encoding="utf-8")

        payload = gtt.cmd_review_branch(review_args(review_report=str(report)))
        review_report = payload["verification_evidence"]["review_report"]

        self.assertEqual(review_report["path"], ".trellis/tasks/07-04-review/review.md")
        self.assertEqual(review_report["size_bytes"], report.stat().st_size)
        self.assertRegex(review_report["sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(payload["verification_evidence"]["reviewer"], "codex-main-session")

    def test_validate_review_gate_rejects_reviewer_only_passed_gate(self) -> None:
        gate = {
            "conclusion": {"passed": True, "summary": "通过"},
            "head": "abc123",
            "verification_evidence": {
                "reviewer": "codex-main-session",
                "evidence": ["部署影响：无。"],
            },
        }
        gtt.write_json(self.task_dir / "review-gate.json", gate)

        _, _, errors = gtt.validate_review_gate(
            self.root,
            self.task_dir,
            self.config,
            allow_metadata_after_gate=False,
        )

        self.assertTrue(any("review_report" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
