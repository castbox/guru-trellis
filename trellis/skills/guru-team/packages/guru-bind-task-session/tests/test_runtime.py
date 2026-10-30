import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
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
from runtime.delivery_projection.tests.upstream_fixture import install_common, public_task, scripts_source


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def current_task(name):
    return public_task({
        "id": name, "name": name, "lifecycle_generation": 0,
        "source": {"kind": "no_issue"}, "title": name,
        "description": "Reviewed task", "status": "in_progress",
        "dev_type": None, "scope": None, "package": None, "priority": "P2",
        "createdAt": "2026-09-20", "completedAt": None,
        "base_branch": "main", "worktree_path": None, "commit": None,
        "pr_url": None, "children": [], "parent": None,
        "relatedFiles": [], "notes": "", "meta": {},
    })


def request(profile, task_id="a", generation=0, **extra):
    value = {"profile": "delivery_" + profile, "mode": "standalone", "task_id": task_id,
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
        install_common(self.root)
        (self.root / "README").write_text("fixture\n")
        git(self.root, "add", ".")
        git(self.root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "seed")
        git(self.root, "worktree", "add", "-qb", "task-b", str(self.other), "main")
        for name, workspace in (("a", self.root), ("b", self.other)):
            task = workspace / ".trellis/tasks" / name
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps(current_task(name)))
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
            key, binding_revision=binding.binding_revision,
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
                         {"schema_version": 3, "task_id": "a", "lifecycle_generation": 0, "delivery_id": None})
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

    def test_double_stdin_conflicts_before_either_reader_or_identity_access(self):
        with patch.object(bind, "read_json", side_effect=AssertionError("must not read either input")), \
                patch.object(bind, "official_port", side_effect=AssertionError("must not resolve identity")):
            with self.assertRaises(bind.CommandError) as caught:
                bind.execute(self.root, "-", "-")
        error = caught.exception
        self.assertEqual((error.code, error.field_path, error.exit_status),
                         ("conflicting_arguments", "arguments.--owner-result", 2))
        self.assertIn("--input", error.remediation)
        self.assertIn("--owner-result", error.remediation)
        self.assertIn("only one", error.remediation)
        self.assertEqual(self.port.writes, 0)

    def test_complete_file_pair_and_single_stdin_pairs_preserve_resume(self):
        self.invoke("rebind_missing_session")
        before = dict(self.port.records)
        public, owner = request("resume_current_task")
        input_path = Path(self.temp.name) / "input.json"
        owner_path = Path(self.temp.name) / "owner.json"
        input_path.write_text(json.dumps(public), encoding="utf-8")
        owner_path.write_text(json.dumps(owner), encoding="utf-8")
        pairs = [(str(input_path), str(owner_path), None),
                 ("-", json.dumps(owner), json.dumps(public)),
                 (json.dumps(public), "-", json.dumps(owner))]
        for input_value, owner_value, stdin in pairs:
            with self.subTest(input=input_value, owner=owner_value), patch("sys.stdin", io.StringIO(stdin or "")):
                output = bind.execute(self.root, input_value, owner_value, official=self.port)
            self.assertEqual(output, {"exit_id": "session_resumed", "task_id": "a",
                                      "lifecycle_generation": 0, "resume_target": "phase-2"})
            self.assertEqual(self.port.records, before)
            self.assertEqual(self.port.writes, 1)


class FixedForkIntegrationTest(unittest.TestCase):
    def test_initial_identity_binding_checkout_and_session_keep_manual_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'repo'
            subprocess.check_call(['git','init','-q','-b','task-initial',str(root)])
            install_common(root)
            task_ref='.trellis/tasks/a'
            task=root/task_ref;task.mkdir(parents=True)
            (task/'task.json').write_text(json.dumps(current_task('a')))
            archive=root/'.trellis/tasks/archive/2026-10/a/task.json'
            archive.parent.mkdir(parents=True)
            archive.write_text(json.dumps({'id':'a','status':'completed','creator':'fixture','assignee':'fixture'}))
            # This module fixture enables the public resolver's installed-Guru
            # binding requirement; it is not an installation qualification.
            marker=root/'.trellis/guru-team/extension.json';marker.parent.mkdir(parents=True)
            marker.write_text('{}')
            git(root,'add','.')
            git(root,'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','initial task')
            def original_owner(name):
                path=PACKAGE.parent/name/'runtime/invoke.py'
                spec=importlib.util.spec_from_file_location('initial_'+name.replace('-','_'),path)
                owner=importlib.util.module_from_spec(spec);spec.loader.exec_module(owner)
                return owner
            identity=original_owner('guru-establish-task-identity')
            branch=original_owner('guru-establish-task-branch-binding')
            checkout=original_owner('guru-ensure-task-checkout')
            selected={'profile':'delivery_active_task','mode':'standalone','task_id':'a','task_ref':task_ref,'lifecycle_generation':0}
            before={p.relative_to(root).as_posix():p.read_bytes() for p in (root/'.trellis').rglob('*') if p.is_file()}
            with patch.object(sys, 'dont_write_bytecode', False):
                self.assertEqual(identity.invoke(root,selected)['exit_id'],'identity_established')
            self.assertEqual(before,{p.relative_to(root).as_posix():p.read_bytes() for p in (root/'.trellis').rglob('*') if p.is_file()})
            self.assertEqual(branch.invoke(root,{**selected,'action':'establish'})['exit_id'],'binding_established')
            key_only={k:v for k,v in selected.items() if k!='task_ref'}
            self.assertEqual(checkout.invoke(root,key_only)['exit_id'],'checkout_resolved')
            with patch.dict(os.environ,{'TRELLIS_CONTEXT_ID':'initial-bind-fixture'}):
                public,semantic=request('rebind_missing_session')
                self.assertEqual(bind.execute(root,json.dumps(public),json.dumps(semantic))['exit_id'],'session_rebound')
                official=bind.official_port(root)
                resolved=official.resolve_task_identity(official.repository_facts(root),'a',0)
                self.assertEqual(resolved.task_ref,task_ref)
            self.assertEqual(json.loads(archive.read_text())['id'],'a')

    def test_official_schema_three_port_with_real_git_checkout(self):
        scripts = scripts_source()
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
                (task / "task.json").write_text(json.dumps(current_task(name)))
                git(workspace, "add", ".trellis/tasks")
                git(workspace, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "task")
            repository = bind.inspect_repository(root)
            for name in ("a", "b"):
                key = bind.TaskLifecycleKey(name, 0)
                branch = "main" if name == "a" else "task-b"
                binding = bind.BranchBindingStore(repository).establish(key, branch)
                bind.ResourceLedgerStore(repository).establish_current(
                    key, binding_revision=binding.binding_revision,
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
                                 {"schema_version": 3, "task_id": "a", "lifecycle_generation": 0, "delivery_id": None})
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
                    key, binding_revision=binding.binding_revision,
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
                resolved = port.resolve_task_identity(port.repository_facts(root), "a", 1)
                self.assertEqual(resolved.workspace, root.resolve())
                self.assertEqual(resolved.task_ref, ".trellis/tasks/a")
                old = bind.BranchBindingStore(repository).read(key)
                bind.ResourceLedgerStore(repository).rebind_current(
                    key, expected_revision=old.binding_revision,
                    source_branch_name=old.branch_name, target_branch_name="rebound-a",
                    expected_cleanup_head=git(root, "rev-parse", "HEAD"),
                    target_branch_ownership="caller_owned", target_worktree_ownership="caller_owned",
                    worktree_reassociated=False,
                )
                bind.BranchBindingStore(repository).advance(
                    key, expected_revision=old.binding_revision,
                    branch_name="rebound-a",
                )
                resolved = port.resolve_task_identity(port.repository_facts(root), "a", 1)
                self.assertEqual(resolved.workspace, rebound.resolve())
                session.unlink()
                self.assertEqual(invoke("rebind_missing_session", generation=1)["exit_id"], "session_rebound")
                self.assertEqual(invoke("resume_current_task", generation=1)["exit_id"], "session_resumed")
                git(rebound, "mv", ".trellis/tasks/a", ".trellis/tasks/renamed-a")
                git(rebound, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "commit", "-qm", "rename task ref")
                self.assertEqual(bind.resolve_task_id(rebound, "a").task_ref, ".trellis/tasks/renamed-a")
                before = session.read_bytes()
                self.assertEqual(invoke("resume_current_task", generation=1)["exit_id"], "session_resumed")
                self.assertEqual(session.read_bytes(), before)
                session.unlink()
                self.assertEqual(invoke("rebind_missing_session", generation=1)["exit_id"], "session_rebound")
                self.assertEqual(json.loads(session.read_text()),
                                 {"schema_version": 3, "task_id": "a", "lifecycle_generation": 1, "delivery_id": None})


if __name__ == "__main__":
    unittest.main()
