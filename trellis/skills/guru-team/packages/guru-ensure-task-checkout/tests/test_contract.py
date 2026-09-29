from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore

from runtime import schema
from runtime.task_lifecycle.checkout_resolution import canonical_head_ref
from runtime.task_lifecycle.identity import resolve_task_id

PACKAGE = Path(__file__).resolve().parents[1]


class EnsureCheckoutTests(unittest.TestCase):
    def test_binding_then_unique_checkout_resolution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
            task = root / ".trellis/tasks/demo"
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps({"id": "demo", "status": "in_progress", "lifecycle_generation": 0}), encoding="utf-8")
            subprocess.run(["git", "add", ".trellis/tasks/demo/task.json"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"],
                cwd=root, check=True,
            )
            repository = inspect_repository(root)
            key = TaskLifecycleKey("demo", 0)
            self.assertEqual(resolve_task_id(root, "demo").task_ref, ".trellis/tasks/demo")
            import importlib.util
            spec = importlib.util.spec_from_file_location("ensure_checkout", PACKAGE / "runtime/invoke.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            payload = {"profile": "active_task", "mode": "standalone", "task_id": "demo", "lifecycle_generation": 0}
            self.assertEqual(module.invoke(root, payload)["exit_id"], "binding_required")
            binding = BranchBindingStore(repository).establish(key, "main")
            self.assertEqual(module.invoke(root, payload)["exit_id"], "binding_required")
            ResourceLedgerStore(repository).establish_current(
                key, binding_revision=0,
                branch_name="main", branch_ownership="caller_owned", worktree_ownership="not_applicable",
            )
            resolved = module.invoke(root, payload)
            self.assertEqual(resolved["exit_id"], "checkout_resolved", resolved)
            self.assertEqual(resolved["checkout_path"], str(root.resolve()))
            self.assertEqual(canonical_head_ref("main"), binding.branch_ref)
            schema.validate_json(resolved, PACKAGE / "schemas/public-output.schema.json", "output")

    def test_stale_generation_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
            task = root / ".trellis/tasks/demo"
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps({"id": "demo", "status": "planning", "lifecycle_generation": 1}), encoding="utf-8")
            subprocess.run(["git", "add", ".trellis/tasks/demo/task.json"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"],
                cwd=root, check=True,
            )
            repository = inspect_repository(root)
            key = TaskLifecycleKey("demo", 0)
            binding = BranchBindingStore(repository).establish(key, "main")
            ResourceLedgerStore(repository).establish_current(
                key, binding_revision=0,
                branch_name="main", branch_ownership="caller_owned", worktree_ownership="not_applicable",
            )
            import importlib.util
            spec = importlib.util.spec_from_file_location("ensure_checkout_stale", PACKAGE / "runtime/invoke.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            payload = {"profile": "active_task", "mode": "workflow", "task_id": "demo", "lifecycle_generation": 0}
            self.assertEqual(module.invoke(root, payload), {"exit_id": "invalid_task_state", "reason_code": "task_identity_stale"})

    def test_new_task_in_linked_checkout_resolves_from_source_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
            (root / "README.md").write_text("source\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "base"],
                cwd=root, check=True,
            )
            linked = root / "linked"
            subprocess.run(["git", "worktree", "add", "-q", "-b", "task-branch", str(linked)], cwd=root, check=True)
            task = linked / ".trellis/tasks/demo"
            task.mkdir(parents=True)
            (task / "task.json").write_text(
                json.dumps({"id": "demo", "status": "planning", "lifecycle_generation": 0}), encoding="utf-8"
            )
            self.assertFalse((root / ".trellis/tasks/demo/task.json").exists())
            repository = inspect_repository(root)
            key = TaskLifecycleKey("demo", 0)
            binding = BranchBindingStore(repository).establish(key, "task-branch")
            ResourceLedgerStore(repository).establish_current(
                key, binding_revision=0,
                branch_name="task-branch", branch_ownership="guru_owned", worktree_ownership="guru_owned",
            )
            import importlib.util
            spec = importlib.util.spec_from_file_location("ensure_checkout_linked", PACKAGE / "runtime/invoke.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            payload = {"profile": "active_task", "mode": "workflow", "task_id": "demo", "lifecycle_generation": 0}

            output = module.invoke(root, payload)
            self.assertEqual(output["exit_id"], "checkout_resolved", output)
            self.assertEqual(output["task_ref"], ".trellis/tasks/demo")
            self.assertEqual(output["checkout_path"], str(linked.resolve()))
            schema.validate_json(output, PACKAGE / "schemas/public-output.schema.json", "output")

            (task / "task.json").unlink()
            self.assertEqual(
                module.invoke(root, payload),
                {"exit_id": "invalid_task_state", "reason_code": "task_artifact_mismatch"},
            )

    def test_bound_branch_without_registered_checkout_requests_acquisition(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
            task = root / ".trellis/tasks/demo"
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps({"id": "demo", "status": "planning", "lifecycle_generation": 0}), encoding="utf-8")
            subprocess.run(["git", "add", ".trellis/tasks/demo/task.json"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"],
                cwd=root, check=True,
            )
            subprocess.run(["git", "branch", "task-branch"], cwd=root, check=True)
            repository = inspect_repository(root)
            key = TaskLifecycleKey("demo", 0)
            binding = BranchBindingStore(repository).establish(key, "task-branch")
            ResourceLedgerStore(repository).establish_current(
                key, binding_revision=0,
                branch_name="task-branch", branch_ownership="caller_owned", worktree_ownership="not_applicable",
            )
            import importlib.util
            spec = importlib.util.spec_from_file_location("ensure_checkout_missing", PACKAGE / "runtime/invoke.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            output = module.invoke(root, {"profile": "active_task", "mode": "workflow", "task_id": "demo", "lifecycle_generation": 0})
            self.assertEqual(output["exit_id"], "checkout_required", output)
            schema.validate_json(output, PACKAGE / "schemas/public-output.schema.json", "output")


if __name__ == "__main__":
    unittest.main()
