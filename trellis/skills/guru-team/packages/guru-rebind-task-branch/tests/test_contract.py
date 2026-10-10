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
from runtime.io import project_intermediate_receipt
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("rebind_task_branch", PACKAGE / "runtime/invoke.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RebindTaskBranchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-q", "-b", "main")
        task = self.root / ".trellis/tasks/demo"
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps({"id": "demo", "status": "in_progress", "lifecycle_generation": 0}), encoding="utf-8")
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture")
        self.head = self.git("rev-parse", "HEAD")
        self.git("checkout", "-qb", "task/demo")
        self.repository = inspect_repository(self.root)
        self.key = TaskLifecycleKey("demo", 0)
        store = BranchBindingStore(self.repository)
        binding = store.establish(self.key, "task/demo")
        ResourceLedgerStore(self.repository).establish_current(
            self.key, binding_revision=0,
            branch_name="task/demo", branch_ownership="caller_owned", worktree_ownership="not_applicable",
        )
        self.request = {
            "route": "same_checkout_new_ref", "task_id": "demo", "task_ref": ".trellis/tasks/demo",
            "lifecycle_generation": 0, "expected_status": "in_progress", "current_checkout": str(self.root),
            "target_branch_name": "task/new", "selected_base_ref": "main", "reviewed_base_head": self.head,
        }

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def test_rebind_and_recover_exact_plan_without_repeat(self) -> None:
        plan = MODULE.prepare(self.root, self.request)
        payload = {"profile": "task_branch_rebind", "mode": "workflow", "action": "execute", "plan": plan}
        result = MODULE.invoke(self.root, payload)
        validate_json(result, PACKAGE / "schemas/public-output.schema.json", "output")
        self.assertEqual(result["exit_id"], "rebound", result)
        self.assertEqual(self.git("branch", "--show-current"), "task/new")
        binding = BranchBindingStore(self.repository).read(self.key)
        self.assertEqual((binding.branch_name, binding.binding_revision), ("task/new", 1))
        recovery = MODULE.invoke(self.root, {**payload, "action": "recover"})
        self.assertEqual(recovery, result)
        self.assertEqual(BranchBindingStore(self.repository).read(self.key), binding)
        self.assertEqual(MODULE.invoke(self.root, payload)["exit_id"], "blocked")

    def test_dirty_and_base_head_drift_block_before_mutation(self) -> None:
        (self.root / "dirty.txt").write_text("dirty", encoding="utf-8")
        with self.assertRaisesRegex(Exception, "dirty_or_unregistered_checkout"):
            MODULE.prepare(self.root, self.request)
        (self.root / "dirty.txt").unlink()
        stale = {**self.request, "reviewed_base_head": "a" * 40}
        with self.assertRaisesRegex(Exception, "rebind_base_stale"):
            MODULE.prepare(self.root, stale)
        self.assertEqual(self.git("branch", "--show-current"), "task/demo")

    def test_real_atomic_receipt_and_recovery_keep_one_binding_revision(self) -> None:
        def call(script, payload):
            process = subprocess.run(
                [str(PACKAGE / "scripts" / script), "--root", str(self.root), "--input", "-"],
                input=json.dumps(payload), text=True, capture_output=True,
            )
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            return json.loads(process.stdout)

        prepared = project_intermediate_receipt(call("record-plan.sh", self.request), PACKAGE.parents[1] / "schemas")
        payload = {"profile": "task_branch_rebind", "mode": "workflow", "action": "execute", "plan": prepared["plan"]}
        executed = project_intermediate_receipt(call("rebind.sh", payload), PACKAGE.parents[1] / "schemas")
        self.assertEqual(executed["exit_id"], "rebound")
        self.assertEqual(self.git("branch", "--show-current"), "task/new")
        binding = BranchBindingStore(self.repository).read(self.key)
        self.assertEqual(binding.binding_revision, 1)
        recovery_input = {**payload, "action": "recover"}
        for script in ("check-result.sh", "recover-result.sh"):
            recovered = project_intermediate_receipt(call(script, recovery_input), PACKAGE.parents[1] / "schemas")
            self.assertEqual(recovered, executed)
        formal = call("invoke.sh", recovery_input)
        self.assertEqual(formal, executed)
        self.assertNotIn("formal_exit", formal)
        self.assertEqual(BranchBindingStore(self.repository).read(self.key), binding)


if __name__ == "__main__":
    unittest.main()
