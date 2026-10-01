from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("establish_task_branch", PACKAGE / "runtime/invoke.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BranchBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-q", "-b", "main")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "initial", "--allow-empty")
        self.git("checkout", "-qb", "task/demo")
        task = self.root / ".trellis/tasks/demo"
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps({
            "id": "demo", "name": "demo", "lifecycle_generation": 0,
            "source": {"kind": "no_issue"}, "title": "Demo",
            "description": "Reviewed task", "status": "planning",
            "dev_type": None, "scope": None, "package": None, "priority": "P2",
            "createdAt": "2026-09-20", "completedAt": None,
            "base_branch": "main", "worktree_path": None, "commit": None,
            "pr_url": None, "children": [], "parent": None,
            "relatedFiles": [], "notes": "", "meta": {},
        }), encoding="utf-8")
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "task")
        self.head = self.git("rev-parse", "HEAD")
        self.repo = inspect_repository(self.root)
        self.key = TaskLifecycleKey("demo", 0)
        self.input = {"profile": "active_task", "mode": "workflow", "action": "establish", "task_id": "demo", "task_ref": ".trellis/tasks/demo", "lifecycle_generation": 0, "expected_status": "planning"}

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def invoke(self, payload: dict) -> dict:
        result = MODULE.invoke(self.root, payload)
        validate_json(result, PACKAGE / "schemas/public-output.schema.json", "output")
        return result

    def test_unique_candidate_establishes_once_and_recovers_without_write(self) -> None:
        result = self.invoke(self.input)
        self.assertEqual(result["exit_id"], "binding_established", result)
        store = BranchBindingStore(self.repo)
        binding = store.read(self.key)
        self.assertEqual(binding.branch_name, "task/demo")
        ledger = ResourceLedgerStore(self.repo)
        self.assertEqual(ledger.read_current(self.key).branch_name, "task/demo")
        recovery = {**self.input, "action": "recover", "recovery": {
            "expected_revision": binding.binding_revision,
            "expected_branch_name": binding.branch_name, "expected_head": self.head,
        }}
        before = (store.snapshot(self.key), ledger.snapshot(self.key))
        self.assertEqual(self.invoke(recovery), result)
        self.assertEqual((store.snapshot(self.key), ledger.snapshot(self.key)), before)
        self.assertEqual(self.invoke(self.input), result)
        self.assertEqual((store.snapshot(self.key), ledger.snapshot(self.key)), before)

    def test_stale_selected_head_and_recovery_before_write(self) -> None:
        self.assertEqual(self.invoke({**self.input, "action": "recover", "recovery": {
            "expected_revision": 0, "expected_branch_name": "task/demo", "expected_head": self.head,
        }})["exit_id"], "blocked")
        stale = {**self.input, "expected_candidate_head": "a" * 40}
        self.assertEqual(self.invoke(stale)["exit_id"], "selection_required")
        self.assertIsNone(BranchBindingStore(self.repo).read(self.key))

    def test_discovery_and_record_commands_are_read_only(self) -> None:
        for command_id in ("discover-task-branch-binding-candidates", "record-task-branch-binding-plan"):
            with self.subTest(command=command_id):
                result = MODULE.run(PACKAGE, {"id": command_id}, ["--root", str(self.root), "--input", json.dumps(self.input)])
                self.assertEqual(result["status"], "candidate_resolved")
                self.assertEqual(len([row for row in result["candidates"] if row["valid"]]), 1)
                self.assertIsNone(BranchBindingStore(self.repo).read(self.key))
                self.assertIsNone(ResourceLedgerStore(self.repo).read_current(self.key))
        with self.assertRaisesRegex(Exception, "read-only recovery action"):
            MODULE.run(PACKAGE, {"id": "recover-established-task-branch-binding-result"}, ["--root", str(self.root), "--input", json.dumps(self.input)])


if __name__ == "__main__":
    unittest.main()
