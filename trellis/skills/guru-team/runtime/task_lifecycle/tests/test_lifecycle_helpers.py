from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository


HELPER = Path(__file__).resolve().parents[2] / "lifecycle_helpers.py"
TASK = ".trellis/tasks/09-20-example"


class LifecycleHelperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        task = self.repo / TASK
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps({
            "id": "example-id", "name": "example", "status": "in_progress",
            "lifecycle_generation": 2, "branch": "retired-branch-is-not-authority",
            "source": {"kind": "no_issue"}, "title": "Example",
            "description": "Reviewed task", "dev_type": None, "scope": None,
            "package": None, "priority": "P2", "createdAt": "2026-09-20",
            "completedAt": None, "base_branch": "main", "worktree_path": None,
            "commit": None, "pr_url": None, "children": [], "parent": None,
            "relatedFiles": [], "notes": "", "meta": {},
        }), encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def git(self, *args: str) -> None:
        subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True)

    def helper(self, command: str, *args: str) -> tuple[int, dict]:
        result = subprocess.run(
            [sys.executable, str(HELPER), command, "--root", str(self.repo), "--task", TASK, *args],
            cwd=self.repo, text=True, capture_output=True,
        )
        return result.returncode, json.loads(result.stdout if result.returncode == 0 else result.stderr)

    def bind(self) -> None:
        BranchBindingStore(inspect_repository(self.repo)).establish(TaskLifecycleKey("example-id", 2), "main")

    def test_boundary_uses_binding_not_legacy_branch_and_blocks_missing_or_wrong_branch(self) -> None:
        code, result = self.helper("check-task-checkout-boundary")
        self.assertEqual((code, result["status"]), (2, "blocked"))
        self.assertIn("binding required", result["errors"][0])
        self.bind()
        code, result = self.helper("check-task-checkout-boundary")
        self.assertEqual((code, result["status"], result["task_dir_relative"]), (0, "ok", TASK))
        self.assertEqual(Path(result["checkout_root"]), self.repo.resolve())
        self.assertEqual(set(result), {"status", "task_dir_relative", "checkout_root", "task_worktree_status", "errors"})
        self.git("checkout", "-qb", "wrong-branch")
        code, result = self.helper("check-task-checkout-boundary")
        self.assertEqual((code, result["status"]), (2, "blocked"))
        self.assertIn("does not match branch binding", result["errors"][0])

    def test_recovery_requires_ordered_predecessor_and_current_boundary(self) -> None:
        self.bind()
        base = ("--logical-role", "review", "--agent-id", "agent-a",
                "--reason", "interrupted", "--handoff-summary", "current result")
        code, result = self.helper("record-agent-recovery", "--event", "replacement", *base)
        self.assertEqual((code, result["status"]), (2, "blocked"))
        self.assertIn("predecessor", result["errors"][0])
        code, result = self.helper("record-agent-recovery", "--event", "unfinished", *base)
        self.assertEqual((code, result["event"]["event_id"]), (0, "recovery-001"))
        code, result = self.helper("record-agent-recovery", "--event", "replacement", *base,
                                   "--predecessor-event-id", "recovery-001")
        self.assertEqual((code, result["event"]["event_id"]), (0, "recovery-002"))
        code, result = self.helper("check-agent-recovery")
        self.assertEqual((code, result["replacement_count"], result["open_unfinished"]), (0, 1, {}))
        self.git("checkout", "-qb", "wrong-branch")
        code, result = self.helper("check-agent-recovery")
        self.assertEqual((code, result["status"]), (2, "blocked"))


if __name__ == "__main__":
    unittest.main()
