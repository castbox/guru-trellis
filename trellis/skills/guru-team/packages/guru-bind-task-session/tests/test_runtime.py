import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


PACKAGE = Path(__file__).resolve().parents[1]
SOURCE = PACKAGE / "runtime/invoke.py"
spec = importlib.util.spec_from_file_location("bind_package_runtime", SOURCE)
bind = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bind)


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def request(profile, task_id="a", generation=0, **extra):
    value = {"profile": profile, "mode": "standalone", "task_id": task_id,
             "lifecycle_generation": generation, "continuation_id": "run-1", **extra}
    route = bind.PROFILE_ROUTES[profile]
    owner = {**value, "route": route, "resume_target": "phase-2",
             "ai_review_gate": {"status": "passed", "summary": "Current identity reviewed."}}
    return value, owner


class OfficialPort:
    def __init__(self, root, other):
        self.root = root
        self.other = other
        self.context = "one"
        self.records = {}
        self.tasks = {("a", 0), ("a", 1), ("b", 0)}
        self.writes = 0

    def resolve_context_key(self, platform_input=None, platform=None):
        return self.context

    def repository_facts(self, root):
        return SimpleNamespace(common_dir=self.root / ".git")

    def session_path(self, root, key, facts):
        return facts.common_dir / "trellis/sessions" / (key + ".json")

    def record_exists(self, path):
        return path in self.records

    def read_record(self, path, root, facts):
        value = self.records[path]
        return SimpleNamespace(task_id=value["task_id"], lifecycle_generation=value["lifecycle_generation"], data=value)

    def write_record(self, path, data, root):
        self.writes += 1
        self.records[path] = dict(data)

    def resolve_task_identity(self, facts, task_id, lifecycle_generation):
        if (task_id, lifecycle_generation) not in self.tasks:
            raise ValueError("stale_lifecycle_generation")
        task_ref = f".trellis/tasks/{task_id}"
        workspace = self.root if task_id == "a" else self.other
        return SimpleNamespace(task_ref=task_ref, workspace=workspace, task_path=workspace / task_ref)


class RuntimeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        self.other = Path(self.temp.name) / "other"
        subprocess.check_call(["git", "init", "-q", "-b", "main", str(self.root)])
        (self.root / "README").write_text("fixture\n")
        git(self.root, "add", ".")
        git(self.root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "seed")
        git(self.root, "worktree", "add", "-qb", "task-b", str(self.other), "main")
        for name, workspace in (("a", self.root), ("b", self.other)):
            task = workspace / ".trellis/tasks" / name
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps({"id": name, "status": "in_progress", "lifecycle_generation": 0}))
            git(workspace, "add", ".trellis")
            git(workspace, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "task")
        self.port = OfficialPort(self.root, self.other)
        for name in ("a", "b"):
            self.establish(name, 0)

    def tearDown(self):
        self.temp.cleanup()

    def establish(self, name, generation):
        repository = bind.inspect_repository(self.root)
        key = bind.TaskLifecycleKey(name, generation)
        branch = "task-b" if name == "b" else "reactivated-a" if generation == 1 else "main"
        binding = bind.BranchBindingStore(repository).establish(key, branch)
        bind.ResourceLedgerStore(repository).establish_current(
            key, binding_epoch=binding.binding_epoch, binding_revision=binding.binding_revision,
            branch_name=branch, branch_ownership="caller_owned", worktree_ownership="not_applicable",
        )

    def invoke(self, profile, task_id="a", generation=0, **extra):
        public, owner = request(profile, task_id, generation, **extra)
        return bind.execute(self.root, json.dumps(public), json.dumps(owner), official=self.port)

    def test_rebind_resume_and_manual_recovery_are_pointer_only(self):
        rebound = self.invoke("rebind_missing_session")
        self.assertEqual(rebound, {"exit_id": "session_rebound", "task_id": "a",
                                   "lifecycle_generation": 0, "resume_target": "phase-2"})
        self.assertEqual(self.invoke("resume_current_task")["exit_id"], "session_resumed")
        self.assertEqual(self.port.writes, 1)
        self.port.records.clear()
        self.assertEqual(self.invoke("manual_recovery")["exit_id"], "session_manually_recovered")
        self.assertEqual(self.port.writes, 2)
        self.assertEqual(next(iter(self.port.records.values())),
                         {"schema_version": 2, "task_id": "a", "lifecycle_generation": 0})
        self.assertFalse((self.root / ".trellis/.runtime/guru-team").exists())

    def test_switch_a_b_a_preserves_other_session(self):
        self.invoke("rebind_missing_session")
        self.port.context = "two"
        self.invoke("rebind_missing_session")
        self.port.context = "one"
        self.assertEqual(self.invoke("switch_task", "b", current_task_id="a",
                                     current_lifecycle_generation=0)["exit_id"], "task_switched")
        self.assertEqual(self.invoke("switch_task", "a", current_task_id="b",
                                     current_lifecycle_generation=0)["exit_id"], "task_switched")
        self.assertEqual({v["task_id"] for v in self.port.records.values()}, {"a"})
        self.assertEqual(len(self.port.records), 2)

    def test_reactivation_replaces_old_generation_pointer(self):
        self.invoke("rebind_missing_session")
        task = self.root / ".trellis/tasks/a/task.json"
        data = json.loads(task.read_text()); data["lifecycle_generation"] = 1
        task.write_text(json.dumps(data))
        git(self.root, "switch", "-c", "reactivated-a")
        self.establish("a", 1)
        before = dict(self.port.records)
        self.assertEqual(self.invoke("manual_recovery", generation=1)["reason_code"], "session_target_mismatch")
        self.assertEqual(self.port.records, before)
        result = self.invoke("reactivate_rebind", generation=1)
        self.assertEqual((result["exit_id"], result["lifecycle_generation"]), ("reactivate_rebound", 1))
        self.assertEqual(self.invoke("resume_current_task", generation=0)["exit_id"], "binding_blocked")
        self.assertEqual(self.invoke("reactivate_rebind", generation=1)["exit_id"], "reactivate_rebound")
        self.assertEqual(self.port.writes, 2)

    def test_cross_session_reactivation_does_not_require_old_pointer(self):
        task = self.root / ".trellis/tasks/a/task.json"
        data = json.loads(task.read_text()); data["lifecycle_generation"] = 1
        task.write_text(json.dumps(data))
        git(self.root, "switch", "-c", "reactivated-a")
        self.establish("a", 1)
        self.assertEqual(self.invoke("reactivate_rebind", generation=1)["exit_id"], "reactivate_rebound")
        self.assertEqual(self.port.writes, 1)

    def test_binding_ownership_and_checkout_mismatch_are_zero_write(self):
        repository = bind.inspect_repository(self.root)
        key = bind.TaskLifecycleKey("a", 0)
        ledger = bind.ResourceLedgerStore(repository).path_for(key)
        saved = ledger.read_bytes()
        ledger.unlink()
        self.assertEqual(self.invoke("rebind_missing_session")["reason_code"], "session_branch_unresolved")
        ledger.parent.mkdir(parents=True, exist_ok=True); ledger.write_bytes(saved)
        rows = bind.discover_worktree_facts(repository)
        with patch.object(bind, "discover_worktree_facts", return_value=rows + rows):
            self.assertEqual(self.invoke("rebind_missing_session")["reason_code"], "session_checkout_unresolved")
        self.assertEqual(self.port.writes, 0)

    def test_dirty_checkout_can_resume_but_branch_drift_blocks_without_write(self):
        (self.root / "README").write_text("uncommitted work\n")
        self.assertEqual(self.invoke("rebind_missing_session")["exit_id"], "session_rebound")
        before = dict(self.port.records)
        git(self.root, "switch", "-c", "unrelated")
        self.assertEqual(self.invoke("resume_current_task")["reason_code"], "session_checkout_unresolved")
        self.assertEqual(self.port.records, before)

    def test_explicit_mode_and_stale_mismatch_are_zero_write(self):
        self.port.context = None
        self.assertEqual(self.invoke("rebind_missing_session"),
                         {"exit_id": "explicit_task_mode", "task_id": "a", "lifecycle_generation": 0})
        self.assertEqual(self.port.writes, 0)
        with patch.object(self.port, "resolve_context_key", side_effect=ValueError("unavailable")):
            self.assertEqual(self.invoke("manual_recovery"),
                             {"exit_id": "explicit_task_mode", "task_id": "a", "lifecycle_generation": 0})
        self.assertEqual(self.port.writes, 0)
        self.port.context = "one"
        self.assertEqual(self.invoke("rebind_missing_session", generation=8)["reason_code"], "session_branch_unresolved")
        self.assertEqual(self.invoke("resume_current_task")["exit_id"], "binding_blocked")
        self.invoke("rebind_missing_session")
        before = dict(self.port.records)
        self.assertEqual(self.invoke("switch_task", "b", current_task_id="b",
                                     current_lifecycle_generation=0)["exit_id"], "binding_blocked")
        self.assertEqual(self.invoke("manual_recovery", "b")["exit_id"], "binding_blocked")
        self.assertEqual(self.port.records, before)
        self.assertEqual(self.invoke("rebind_missing_session")["exit_id"], "session_rebound")
        self.assertEqual(self.port.records, before)

    def test_mismatched_semantic_result_blocks_before_official_access(self):
        public, owner = request("rebind_missing_session")
        owner["task_id"] = "b"
        with patch.object(self.port, "repository_facts", side_effect=AssertionError("must not resolve")):
            self.assertEqual(bind.execute(self.root, json.dumps(public), json.dumps(owner), official=self.port)["reason_code"],
                             "stale_semantic_result")


class FixedForkIntegrationTest(unittest.TestCase):
    def test_official_schema_two_port_with_real_git_checkout(self):
        source = os.environ.get("TRELLIS_FIXED_FORK_SOURCE")
        if not source:
            self.skipTest("Set TRELLIS_FIXED_FORK_SOURCE to the Fixed Fork source checkout")
        scripts = Path(source) / "packages/cli/src/templates/trellis/scripts"
        if not (scripts / "common/session_storage.py").is_file():
            self.skipTest("Fixed Fork source template unavailable")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            other = Path(directory) / "other"
            subprocess.check_call(["git", "init", "-q", "-b", "main", str(root)])
            (root / ".trellis/scripts").mkdir(parents=True)
            shutil.copytree(scripts / "common", root / ".trellis/scripts/common")
            (root / "README").write_text("test\n")
            git(root, "add", ".")
            git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "seed")
            git(root, "worktree", "add", "-qb", "task-b", str(other), "main")
            for name, workspace in (("a", root), ("b", other)):
                task = workspace / ".trellis/tasks" / name
                task.mkdir(parents=True)
                (task / "task.json").write_text(json.dumps({"id": name, "status": "in_progress", "lifecycle_generation": 0}))
                git(workspace, "add", ".trellis/tasks")
                git(workspace, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "task")
            repository = bind.inspect_repository(root)
            for name in ("a", "b"):
                key = bind.TaskLifecycleKey(name, 0)
                branch = "main" if name == "a" else "task-b"
                binding = bind.BranchBindingStore(repository).establish(key, branch)
                bind.ResourceLedgerStore(repository).establish_current(
                    key, binding_epoch=binding.binding_epoch, binding_revision=binding.binding_revision,
                    branch_name=branch, branch_ownership="caller_owned", worktree_ownership="not_applicable",
                )
            with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "package-fixture"}):
                port = bind.official_port(root)
                def invoke(profile, task_id="a", generation=0, **extra):
                    public, owner = request(profile, task_id, generation, **extra)
                    return bind.execute(root, json.dumps(public), json.dumps(owner), official=port)

                output = invoke("rebind_missing_session")
                self.assertEqual(output["exit_id"], "session_rebound")
                session = root / ".git/trellis/sessions/package-fixture.json"
                self.assertEqual(json.loads(session.read_text()),
                                 {"schema_version": 2, "task_id": "a", "lifecycle_generation": 0})
                legacy_mapping = root / ".trellis/.runtime/guru-team/tasks/a.json"
                legacy_mapping.parent.mkdir(parents=True)
                legacy_mapping.write_text("not-json")
                self.assertEqual(invoke("resume_current_task")["exit_id"], "session_resumed")
                self.assertEqual(invoke("switch_task", "b", current_task_id="a",
                                        current_lifecycle_generation=0)["exit_id"], "task_switched")
                self.assertEqual(invoke("switch_task", "a", current_task_id="b",
                                        current_lifecycle_generation=0)["exit_id"], "task_switched")
                before = session.read_bytes()
                self.assertEqual(invoke("switch_task", "b", current_task_id="b",
                                        current_lifecycle_generation=0)["exit_id"], "binding_blocked")
                self.assertEqual(session.read_bytes(), before)
                session.unlink()
                self.assertEqual(invoke("manual_recovery")["exit_id"], "session_manually_recovered")
                task = root / ".trellis/tasks/a/task.json"
                data = json.loads(task.read_text())
                data["lifecycle_generation"] = 1
                task.write_text(json.dumps(data))
                git(root, "switch", "-c", "reactivated-a")
                key = bind.TaskLifecycleKey("a", 1)
                binding = bind.BranchBindingStore(repository).establish(key, "reactivated-a")
                bind.ResourceLedgerStore(repository).establish_current(
                    key, binding_epoch=binding.binding_epoch, binding_revision=binding.binding_revision,
                    branch_name="reactivated-a", branch_ownership="caller_owned", worktree_ownership="not_applicable",
                )
                before = session.read_bytes()
                self.assertEqual(invoke("resume_current_task")["exit_id"], "binding_blocked")
                self.assertEqual(session.read_bytes(), before)
                self.assertEqual(invoke("reactivate_rebind", generation=1)["exit_id"], "reactivate_rebound")
                self.assertEqual(json.loads(session.read_text())["lifecycle_generation"], 1)
                with patch.object(port, "resolve_context_key", return_value=None):
                    before = session.read_bytes()
                    self.assertEqual(invoke("manual_recovery", generation=1),
                                     {"exit_id": "explicit_task_mode", "task_id": "a", "lifecycle_generation": 1})
                    self.assertEqual(session.read_bytes(), before)
                self.assertEqual(legacy_mapping.read_text(), "not-json")

                git(root, "add", ".trellis/tasks/a/task.json")
                git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "commit", "-qm", "reactivate")
                rebound = Path(directory) / "rebound-a"
                git(root, "worktree", "add", "-qb", "rebound-a", str(rebound), "reactivated-a")
                with self.assertRaisesRegex(ValueError, "ambiguous_task_identity"):
                    port.resolve_task_identity(port.repository_facts(root), "a", 1)
                old = bind.BranchBindingStore(repository).read(key)
                bind.ResourceLedgerStore(repository).rebind_current(
                    key, expected_epoch=old.binding_epoch, expected_revision=old.binding_revision,
                    source_branch_name=old.branch_name, target_branch_name="rebound-a",
                    expected_cleanup_head=git(root, "rev-parse", "HEAD"),
                    target_branch_ownership="caller_owned", target_worktree_ownership="caller_owned",
                    worktree_reassociated=False,
                )
                bind.BranchBindingStore(repository).advance(
                    key, expected_epoch=old.binding_epoch, expected_revision=old.binding_revision,
                    branch_name="rebound-a",
                )
                session.unlink()
                self.assertEqual(invoke("rebind_missing_session", generation=1)["exit_id"], "session_rebound")
                self.assertEqual(invoke("resume_current_task", generation=1)["exit_id"], "session_resumed")


if __name__ == "__main__":
    unittest.main()
