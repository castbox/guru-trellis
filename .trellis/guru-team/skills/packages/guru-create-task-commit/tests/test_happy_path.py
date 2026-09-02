from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
LOCAL = PACKAGE / "runtime"
for path in (SKILLS, LOCAL):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from runtime.io import CommandError
from common import capture_snapshot, commit_result_path
import execute
import invoke
import record


class HappyPathFacadeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "feature/happy-path")
        self.git("config", "user.name", "Happy Path Test")
        self.git("config", "user.email", "happy-path@example.test")
        (self.repo / "reviewed.txt").write_text("before\n")
        (self.repo / "unrelated.txt").write_text("before\n")
        task = self.repo / ".trellis/tasks/09-02-happy-path"
        task.mkdir(parents=True)
        (task / "task.json").write_text(
            json.dumps(
                {
                    "id": "09-02-happy-path",
                    "status": "in_progress",
                    "branch": "feature/happy-path",
                    "base_branch": "main",
                }
            )
        )
        (task / "issue-scope-ledger.json").write_text(
            json.dumps({"primary_issue": {"number": 330}})
        )
        self.git("add", ".")
        self.git("commit", "-q", "-m", "base")
        self.parent = self.git("rev-parse", "HEAD")
        phase2 = (
            self.repo
            / ".trellis/.runtime/guru-team/owner-checkpoints/09-02-happy-path/phase2-check.json"
        )
        phase2.parent.mkdir(parents=True)
        phase2.write_text(
            json.dumps(
                {
                    "typed_exit": "passed",
                    "task_ref": ".trellis/tasks/09-02-happy-path",
                    "phase2_capture_commit": self.parent,
                }
            )
        )
        (self.repo / "reviewed.txt").write_text("reviewed\n")
        (self.repo / "unrelated.txt").write_text("preserved\n")
        self.candidate_path = (
            self.repo
            / ".trellis/.runtime/guru-team/task-commit-plans/09-02-happy-path/001.json"
        )
        self.candidate_path.parent.mkdir(parents=True)
        self.candidate_path.write_text(
            json.dumps(self.candidate(), ensure_ascii=False, indent=2) + "\n"
        )

    def git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode:
            self.fail(f"git {' '.join(args)} failed: {result.stderr}")
        return result.stdout.strip()

    def candidate(self) -> dict:
        snapshot = capture_snapshot(self.repo)
        rows = {row["path"]: row for row in snapshot["entries"]}
        subject = "fix(commit): #330 收敛提交正常路径"
        body = (
            "背景：\n减少正常提交的编排调用。\n\n"
            "变更：\n增加确认后事务 facade。\n\n"
            "边界：\n保留无关工作区状态。\n\n"
            "验证：\n运行 package-local 回归。\n\nRefs #330"
        )
        return {
            "$schema": "https://github.com/castbox/guru-trellis/schemas/guru-task-commit-candidate-5.0.json",
            "schema_version": "5.0",
            "skill_id": "guru-create-task-commit",
            "sequence": "001",
            "task": {
                "id": "09-02-happy-path",
                "path": ".trellis/tasks/09-02-happy-path",
                "status": "in_progress",
                "branch": "feature/happy-path",
            },
            "git": {
                "base_branch": "main",
                "base_ref": "HEAD^",
                "pre_commit_head": self.parent,
                "phase2_commit_anchor": self.parent,
            },
            "dirty_snapshot": snapshot,
            "path_classifications": [
                {
                    "path": "reviewed.txt",
                    "category": "task-reviewed",
                    "reason": "Covered by the current Phase 2 result.",
                    "coverage_source": "guru-check-task",
                },
                {
                    "path": "unrelated.txt",
                    "category": "unrelated-preserved",
                    "reason": "Parallel work remains outside this commit.",
                    "coverage_source": "live worktree",
                },
            ],
            "exact_stage_paths": ["reviewed.txt"],
            "message": {
                "type": "fix",
                "scope": "commit",
                "summary": "收敛提交正常路径",
                "background": "减少正常提交的编排调用。",
                "changes": "增加确认后事务 facade。",
                "boundaries": "保留无关工作区状态。",
                "validations": "运行 package-local 回归。",
                "subject": subject,
                "body": body,
                "bytes": subject + "\n\n" + body + "\n",
            },
            "ai_review": {
                "status": "passed",
                "summary": "The current paths and message satisfy the semantic gate.",
                "evidence": ["Phase 2 covers reviewed.txt and excludes unrelated.txt."],
            },
        }

    def invoke_facade(self) -> dict:
        return invoke.run(
            PACKAGE,
            {"id": "invoke-guru-create-task-commit-happy-path-v1"},
            [
                "--root",
                str(self.repo),
                "--candidate-artifact",
                ".trellis/.runtime/guru-team/task-commit-plans/09-02-happy-path/001.json",
            ],
        )

    def test_success_and_stdout_loss_recovery_execute_once(self) -> None:
        calls = 0
        original = invoke.execute_commit

        def counted(*args, **kwargs):
            nonlocal calls
            calls += 1
            return original(*args, **kwargs)

        invoke.execute_commit = counted
        self.addCleanup(setattr, invoke, "execute_commit", original)
        first = self.invoke_facade()
        commit = self.git("rev-parse", "HEAD")
        second = self.invoke_facade()

        self.assertEqual(first, second)
        self.assertEqual("committed", first["exit_id"])
        self.assertEqual(commit, first["branch_review_commit"])
        self.assertEqual(1, calls)
        self.assertFalse(self.candidate_path.exists())
        receipt = commit_result_path(self.repo, "09-02-happy-path", "001")
        self.assertTrue(receipt.is_file())
        self.assertEqual("preserved\n", (self.repo / "unrelated.txt").read_text())
        self.assertEqual("before", self.git("show", "HEAD:unrelated.txt"))

    def test_post_ref_interruption_recovers_same_dto_without_duplicate_mutation(self) -> None:
        execute_calls = 0
        original_execute = invoke.execute_commit
        original_git = execute.git

        def counted_execute(*args, **kwargs):
            nonlocal execute_calls
            execute_calls += 1
            return original_execute(*args, **kwargs)

        def interrupt_after_update_ref(repo, *args, **kwargs):
            result = original_git(repo, *args, **kwargs)
            if args and args[0] == "update-ref":
                raise RuntimeError("simulated interruption after update-ref")
            return result

        invoke.execute_commit = counted_execute
        execute.git = interrupt_after_update_ref
        self.addCleanup(setattr, invoke, "execute_commit", original_execute)
        self.addCleanup(setattr, execute, "git", original_git)
        ref = "refs/heads/feature/happy-path"
        reflog_before = self.git("reflog", "show", "--format=%H", ref).splitlines()
        commits_before = int(self.git("rev-list", "--count", "HEAD"))

        with self.assertRaisesRegex(RuntimeError, "after update-ref"):
            self.invoke_facade()

        commit = self.git("rev-parse", "HEAD")
        receipt = commit_result_path(self.repo, "09-02-happy-path", "001")
        reflog_after_interruption = self.git(
            "reflog", "show", "--format=%H", ref
        ).splitlines()
        self.assertTrue(self.candidate_path.exists())
        self.assertTrue(receipt.is_file())
        self.assertEqual(commits_before + 1, int(self.git("rev-list", "--count", "HEAD")))
        self.assertEqual(len(reflog_before) + 1, len(reflog_after_interruption))

        execute.git = original_git
        recovered = self.invoke_facade()
        recovered_again = self.invoke_facade()

        self.assertEqual(recovered, recovered_again)
        self.assertEqual("committed", recovered["exit_id"])
        self.assertEqual(commit, recovered["branch_review_commit"])
        self.assertEqual(1, execute_calls)
        self.assertFalse(self.candidate_path.exists())
        self.assertEqual("", self.git("diff", "--cached", "--name-only"))
        self.assertEqual("M unrelated.txt", self.git("status", "--short", "--untracked-files=no"))
        self.assertEqual(
            reflog_after_interruption,
            self.git("reflog", "show", "--format=%H", ref).splitlines(),
        )
        self.assertEqual(commits_before + 1, int(self.git("rev-list", "--count", "HEAD")))

    def test_recovery_rejects_changed_head_without_reexecuting(self) -> None:
        self.invoke_facade()
        (self.repo / "after.txt").write_text("after\n")
        self.git("add", "after.txt")
        self.git("commit", "-q", "-m", "later")

        def unexpected(*_args, **_kwargs):
            self.fail("recovery must not execute the commit transaction again")

        original = invoke.execute_commit
        invoke.execute_commit = unexpected
        self.addCleanup(setattr, invoke, "execute_commit", original)
        with self.assertRaises(CommandError) as raised:
            self.invoke_facade()
        self.assertEqual("happy_path_result", raised.exception.field_path)

    def test_new_prepare_retires_previous_recovery_receipt(self) -> None:
        receipt = commit_result_path(self.repo, "09-02-happy-path", "001")
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text("{}\n")
        self.candidate_path.unlink()
        public = (
            self.repo / ".trellis/.runtime/guru-team/test-inputs/public.json"
        )
        public.parent.mkdir(parents=True, exist_ok=True)
        public.write_text(
            json.dumps(
                {
                    "profile": "initial_commit",
                    "source_exit": "passed",
                    "mode": "workflow",
                    "task_ref": ".trellis/tasks/09-02-happy-path",
                    "phase2_commit_anchor": self.parent,
                }
            )
        )
        candidate = self.candidate()
        authoring = {
            key: candidate[key]
            for key in ("path_classifications", "message", "ai_review")
        }
        prepared = record.run(
            PACKAGE,
            {},
            [
                "--root",
                str(self.repo),
                "--input",
                str(public),
                "--candidate-json",
                json.dumps(authoring),
            ],
        )
        self.assertEqual("001", Path(prepared["candidate_artifact"]).stem)
        self.assertTrue(self.candidate_path.exists())
        self.assertFalse(receipt.exists())

    def test_recommended_route_meets_package_operation_budget(self) -> None:
        commands = json.loads((PACKAGE / "commands.json").read_text())["commands"]
        command_by_id = {row["id"]: row for row in commands}
        legacy = [
            "prepare-task-commit",
            "check-commit-messages",
            "create-task-commit",
            "invoke-guru-create-task-commit",
        ]
        recommended = [
            "prepare-task-commit",
            "invoke-guru-create-task-commit-happy-path-v1",
        ]
        self.assertTrue(set(legacy + recommended).issubset(command_by_id))
        self.assertLessEqual(len(recommended), len(legacy) * 0.5)
        legacy_validations = [
            command_by_id["check-commit-messages"]["validator_id"],
            command_by_id["create-task-commit"]["validator_id"],
        ]
        recommended_validations = [
            command_by_id["create-task-commit"]["validator_id"]
        ]
        self.assertEqual(["candidate_validator", "exact_executor"], legacy_validations)
        self.assertEqual(["exact_executor"], recommended_validations)
        legacy_redundant_full_reads = len(legacy_validations) - 1
        recommended_redundant_full_reads = len(recommended_validations) - 1
        reduction = 1 - (
            recommended_redundant_full_reads / legacy_redundant_full_reads
        )
        self.assertGreaterEqual(reduction, 0.70)

        interface = json.loads((PACKAGE / "interface.json").read_text())
        recommended_validators = [
            row
            for row in interface["validators"]
            if row["id"].startswith("recommended_happy_path")
        ]
        self.assertEqual(1, len(recommended_validators))
        self.assertEqual(recommended[1], recommended_validators[0]["runtime_command"])


if __name__ == "__main__":
    unittest.main()
