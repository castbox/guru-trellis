"""Real Git/public owner integration; not actual Agent or installation evidence."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from runtime.delivery_projection import DeliveryProjection, authority_ref
from runtime.delivery_projection.tests.test_installed_projection import DECLARATION
from runtime.delivery_projection.tests.upstream_fixture import install_common, public_task
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


PACKAGES = Path(__file__).resolve().parents[2]


def owner(name):
    spec = importlib.util.spec_from_file_location("portable_" + name.replace("-", "_"), PACKAGES / name / "runtime/invoke.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()


def files(root):
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}


class PortableRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "source"
        self.root.mkdir()
        git(self.root, "init", "-q", "-b", "main")
        git(self.root, "config", "user.name", "Fixture")
        git(self.root, "config", "user.email", "fixture@example.invalid")
        git(self.root, "config", "maintenance.auto", "false")
        git(self.root, "config", "gc.auto", "0")
        install_common(self.root)
        (self.root / ".trellis/workflow.md").write_text("[trellis-runtime-contract]\n" + json.dumps(DECLARATION) + "\n[/trellis-runtime-contract]\n")
        (self.root / "scope.md").write_text("Reviewed portable Task scope\n")
        git(self.root, "add", ".trellis/scripts/common", ".trellis/workflow.md", "scope.md")
        git(self.root, "commit", "-qm", "base tools")
        self.main = git(self.root, "rev-parse", "HEAD")
        git(self.root, "switch", "-qc", "task/shared")
        self.ref = ".trellis/tasks/a"
        task = self.root / self.ref
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps(public_task({"id": "a", "name": "a"})))
        (self.root / "active-code.py").write_text("value = 'only on active ref'\n")
        projection = DeliveryProjection(self.root, self.ref)
        scope = authority_ref(self.root / "scope.md", self.root)
        projection.scope(scope)
        self.key = {"task_id": "a", "lifecycle_generation": 0, "delivery_id": "11111111-1111-4111-8111-111111111111"}
        projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": self.key,
                          "owner_role": "creation", "owner_id": DECLARATION["owners"]["creation"],
                          "profile": "pull_request", "scope_ref": {"authority": scope, "anchors": ["portable work"]}})
        git(self.root, "add", self.ref, "active-code.py")
        git(self.root, "commit", "-qm", "active Task and Delivery outside main")
        self.identity = owner("guru-establish-task-identity")
        self.establish = owner("guru-establish-task-branch-binding")
        self.ensure = owner("guru-ensure-task-checkout")
        self.bind = owner("guru-bind-task-session")

    def controls(self, root, task_id="a"):
        selected = {"profile": "delivery_active_task", "mode": "standalone", "task_id": task_id,
                    "task_ref": f".trellis/tasks/{task_id}", "lifecycle_generation": 0}
        self.assertEqual(self.identity.invoke(root, selected)["exit_id"], "identity_established")
        self.assertEqual(self.establish.invoke(root, {**selected, "action": "establish"})["exit_id"], "binding_established")
        resolved = self.ensure.invoke(root, {name: value for name, value in selected.items() if name != "task_ref"})
        self.assertEqual(resolved["exit_id"], "checkout_resolved", resolved)
        self.assertEqual(resolved["checkout_path"], str(root.resolve()))

    def bind_task(self, root, task_id="a", profile="delivery_rebind_missing_session"):
        public = {"profile": profile, "mode": "standalone", "task_id": task_id,
                  "lifecycle_generation": 0, "continuation_id": "portable-fixture"}
        semantic = {**public, "route": "resume" if profile == "delivery_resume_current_task" else "rebind",
                    "resume_target": "phase-2", "ai_review_gate": {"status": "passed", "summary": "Controlled owner integration fixture; not actual Agent acceptance."}}
        return self.bind.execute(root, json.dumps(public), json.dumps(semantic))

    def test_non_main_ref_recovers_same_delivery_in_an_independent_common_dir(self):
        self.controls(self.root)
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "source-session"}):
            self.assertEqual(self.bind_task(self.root)["exit_id"], "session_rebound")
            DeliveryProjection(self.root, self.ref).select(self.key)
        source_controls = files(self.root / ".git/trellis")
        clone = self.base / "replacement"
        git(self.base, "clone", "-q", "--branch", "task/shared", str(self.root), str(clone))
        git(clone, "config", "maintenance.auto", "false")
        git(clone, "config", "gc.auto", "0")
        self.assertEqual(git(clone, "branch", "--show-current"), "task/shared")
        self.assertNotEqual(inspect_repository(clone).common_dir, inspect_repository(self.root).common_dir)
        self.assertEqual(git(clone, "ls-tree", self.main, "--", self.ref, "active-code.py"), "")
        self.assertEqual(git(clone, "rev-parse", "HEAD"), git(self.root, "rev-parse", "HEAD"))
        self.assertFalse((clone / ".git/trellis").exists())
        task_before = (clone / self.ref / "task.json").read_bytes()
        self.controls(clone)
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "replacement-session"}):
            projection = DeliveryProjection(clone, self.ref)
            self.assertEqual(self.bind_task(clone)["exit_id"], "session_rebound")
            self.assertEqual(projection.current()["kind"], "no_current_delivery")
            projection.select(self.key)
            self.assertEqual(projection.current()["key"], self.key)
            selected = (clone / ".git/trellis/sessions/replacement-session.json").read_bytes()
            self.assertEqual(self.bind_task(clone, profile="delivery_resume_current_task")["exit_id"], "session_resumed")
            self.assertEqual((clone / ".git/trellis/sessions/replacement-session.json").read_bytes(), selected)
        key = TaskLifecycleKey("a", 0)
        replacement = ResourceLedgerStore(inspect_repository(clone)).read(key)
        self.assertTrue(all(row.ownership == "caller_owned" for row in replacement.resources))
        self.assertEqual(BranchBindingStore(inspect_repository(clone)).read(key).branch_name,
                         BranchBindingStore(inspect_repository(self.root)).read(key).branch_name)
        self.assertEqual((clone / self.ref / "task.json").read_bytes(), task_before)
        self.assertEqual(files(self.root / ".git/trellis"), source_controls)

    def test_one_tasks_missing_controls_do_not_block_another_registered_task(self):
        self.controls(self.root)
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "a-session"}):
            self.assertEqual(self.bind_task(self.root)["exit_id"], "session_rebound")
        a_session = (self.root / ".git/trellis/sessions/a-session.json").read_bytes()
        other = self.base / "task-b"
        git(self.root, "worktree", "add", "-qb", "task/b", str(other), "main")
        task = other / ".trellis/tasks/b"
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps(public_task({"id": "b", "name": "b"})))
        git(other, "add", ".trellis/tasks/b/task.json")
        git(other, "commit", "-qm", "independent Task B")
        resources = ResourceLedgerStore(inspect_repository(self.root))
        resources.path_for(TaskLifecycleKey("a", 0)).unlink()
        self.controls(other, "b")
        b_controls = (BranchBindingStore(inspect_repository(other)).snapshot(TaskLifecycleKey("b", 0)), resources.snapshot(TaskLifecycleKey("b", 0)))
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "b-session"}):
            self.assertEqual(self.bind_task(other, "b")["exit_id"], "session_rebound")
            self.assertEqual(self.bind_task(other, "b", "delivery_resume_current_task")["exit_id"], "session_resumed")
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "a-session"}):
            self.assertEqual(self.bind_task(self.root, profile="delivery_resume_current_task")["reason_code"], "session_branch_unresolved")
        self.assertEqual((self.root / ".git/trellis/sessions/a-session.json").read_bytes(), a_session)
        self.assertFalse(resources.path_for(TaskLifecycleKey("a", 0)).exists())
        self.assertEqual((BranchBindingStore(inspect_repository(other)).snapshot(TaskLifecycleKey("b", 0)), resources.snapshot(TaskLifecycleKey("b", 0))), b_controls)


if __name__ == "__main__":
    unittest.main()
