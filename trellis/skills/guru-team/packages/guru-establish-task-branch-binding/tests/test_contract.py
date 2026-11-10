from __future__ import annotations

import importlib.util
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json
from runtime.delivery_projection.adapter import upstream_modules
from runtime.delivery_projection.tests.upstream_fixture import install_common, public_task
from runtime.task_lifecycle import branch_resolution
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
        install_common(self.root)
        self.git("init", "-q", "-b", "main")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "initial", "--allow-empty")
        self.git("checkout", "-qb", "task/demo")
        task = self.root / ".trellis/tasks/demo"
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps(public_task({
            "id": "demo", "name": "demo", "lifecycle_generation": 0,
            "source": {"kind": "no_issue"}, "title": "Demo",
            "description": "Reviewed task", "status": "planning",
            "dev_type": None, "scope": None, "package": None, "priority": "P2",
            "createdAt": "2026-09-20", "completedAt": None,
            "base_branch": "main", "worktree_path": None, "commit": None,
            "pr_url": None, "children": [], "parent": None,
            "relatedFiles": [], "notes": "", "meta": {},
        })), encoding="utf-8")
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "task")
        self.head = self.git("rev-parse", "HEAD")
        self.repo = inspect_repository(self.root)
        self.key = TaskLifecycleKey("demo", 0)
        self.input = {"profile": "delivery_active_task", "mode": "workflow", "action": "establish", "task_id": "demo", "task_ref": ".trellis/tasks/demo", "lifecycle_generation": 0}

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

    def test_first_invoke_reuses_bytes_but_resolves_both_inputs(self):
        original = branch_resolution.resolve_establishment
        run = subprocess.run
        readers, requests = [], []
        def resolve(*args, **kwargs):
            readers.append(kwargs["reader"])
            return original(*args, **kwargs)
        def observe(argv, **kwargs):
            if "cat-file" in argv and "--batch" in argv:
                position = kwargs["stdin"].tell()
                requests.extend(kwargs["stdin"].read().splitlines())
                kwargs["stdin"].seek(position)
            return run(argv, **kwargs)
        with patch.object(MODULE, "resolve_establishment", side_effect=resolve), \
                patch.object(branch_resolution, "resolve_establishment", side_effect=resolve), \
                patch("subprocess.run", side_effect=observe):
            result = self.invoke(self.input)
        self.assertEqual("binding_established", result["exit_id"])
        self.assertEqual(2, len(readers))
        self.assertIs(readers[0], readers[1])
        self.assertEqual(1, len(requests))
        self.assertTrue(readers[0].objects.response.closed)

    def test_second_resolve_rereads_ref_after_normal_head_advance(self):
        original = branch_resolution.resolve_establishment
        calls = []
        def resolve(*args, **kwargs):
            calls.append(kwargs["reader"])
            if len(calls) == 2:
                (self.root / "new-work.txt").write_text("normal work committed between operations\n")
                self.git("add", "new-work.txt")
                self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "new work")
            return original(*args, **kwargs)
        with patch.object(MODULE, "resolve_establishment", side_effect=resolve), \
                patch.object(branch_resolution, "resolve_establishment", side_effect=resolve):
            result = self.invoke(self.input)
        self.assertEqual("selection_required", result["exit_id"])
        self.assertEqual("selected_candidate_stale", result["reason_code"])
        self.assertEqual(2, len(calls))
        self.assertIs(calls[0], calls[1])
        self.assertIsNone(BranchBindingStore(self.repo).read(self.key))
        self.assertIsNone(ResourceLedgerStore(self.repo).read_current(self.key))

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
                self.assertNotIn("binding_ref", result)
        with self.assertRaisesRegex(Exception, "read-only recovery action"):
            MODULE.run(PACKAGE, {"id": "recover-established-task-branch-binding-result"}, ["--root", str(self.root), "--input", json.dumps(self.input)])

    def test_missing_task_diagnostic_rejects_both_read_only_commands(self) -> None:
        missing_ref = ".trellis/tasks/missing-demo"
        request = {**self.input, "task_ref": missing_ref}
        for script in ("discover-candidates.sh", "record-plan.sh"):
            with self.subTest(script=script):
                command = subprocess.run(
                    [str(PACKAGE / "scripts" / script), "--root", str(self.root),
                     "--input", json.dumps(request)], text=True, capture_output=True,
                )
                self.assertEqual(3, command.returncode, command.stdout + command.stderr)
                diagnostic = json.loads(command.stdout)
                self.assertEqual("stale_identity", diagnostic["code"])
                self.assertEqual(missing_ref, diagnostic["field_path"])
                self.assertIn("task_not_found", diagnostic["remediation"])
                self.assertIn("guru-establish-task-identity", diagnostic["remediation"])
                self.assertIn("task-carrier-recovery.md", diagnostic["remediation"])
                self.assertNotIn("candidates", diagnostic)
                self.assertIsNone(BranchBindingStore(self.repo).read(self.key))
                self.assertIsNone(ResourceLedgerStore(self.repo).read_current(self.key))

    def test_discovery_exposes_existing_binding_for_closure_without_write(self) -> None:
        formal = self.invoke(self.input)
        self.assertEqual(set(formal), {"exit_id", "task_id", "lifecycle_generation"})
        store, ledger = BranchBindingStore(self.repo), ResourceLedgerStore(self.repo)
        before = (store.snapshot(self.key), ledger.snapshot(self.key))
        command = subprocess.run([str(PACKAGE / "scripts/discover-candidates.sh"),
                                  "--root", str(self.root), "--input", json.dumps(self.input)],
                                 text=True, capture_output=True)
        self.assertEqual(0, command.returncode, command.stdout + command.stderr)
        receipt = json.loads(command.stdout)
        self.assertFalse(receipt["formal_exit"])
        result = receipt["result"]
        self.assertEqual("already_established", result["status"])
        binding = store.read(self.key)
        self.assertEqual(result["binding_ref"], {"task_id": "demo", "lifecycle_generation": 0,
                                               "binding_revision": binding.binding_revision})
        closure = PACKAGE.parent / "guru-complete-task-closure"
        public = json.loads((closure / "examples/public-input.json").read_text())
        public["binding_ref"] = result["binding_ref"]
        validate_json(public, closure / "schemas/public-input.schema.json", "closure_input")
        self.assertEqual((store.snapshot(self.key), ledger.snapshot(self.key)), before)
        plan = MODULE.run(PACKAGE, {"id": "record-task-branch-binding-plan"},
                          ["--root", str(self.root), "--input", json.dumps(self.input)])
        self.assertNotIn("binding_ref", plan)

    def test_public_restored_carrier_association_and_bind_preserve_original_history(self) -> None:
        task_ref = self.input["task_ref"]
        task = self.root / task_ref
        delivery_id = "e62bce4e-0fc4-4ef0-a6cc-b34745efb92c"
        plan_root = f"deliveries/{delivery_id}"
        (task / "prd.md").write_text("# Original accepted recovery scope\n")
        authority = {"locator": f"{task_ref}/prd.md", "revision": "sha256:" +
                     hashlib.sha256((task / "prd.md").read_bytes()).hexdigest()}
        metadata = json.loads((task / "task.json").read_text())
        metadata["accepted_scope"] = authority
        metadata["deliveries"] = [{
            "id": delivery_id, "lifecycle_generation": 0,
            "scope_ref": {"authority": authority, "anchors": ["recovery"]},
            "planning_root": plan_root, "profile": "pull_request", "phase": "planning",
            "plan_ref": None, "candidate": None,
            "results": {"planning": None, "check": None, "full_review": None, "readiness": None},
            "publication_result": None, "delivery_result": None, "stop_result": None,
        }]
        plans = task / plan_root
        plans.mkdir(parents=True)
        for name in ("prd", "design", "implement"):
            (plans / f"{name}.md").write_text(f"# Original {name}\n\nRetain this complete carrier.\n")
        for name in ("implement", "check"):
            (plans / f"{name}.jsonl").write_text("")
        (task / "task.json").write_text(json.dumps(metadata))
        self.git("add", task_ref)
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "original carrier")
        carrier = self.git("rev-parse", "HEAD")
        original = {path.relative_to(task).as_posix(): path.read_bytes()
                    for path in task.rglob("*") if path.is_file()}
        self.git("switch", "main")
        target_head = self.git("rev-parse", "HEAD")
        # Unchanged installed native APIs are fixture dependencies outside the
        # Branch producer boundary; Task/Delivery bytes come only from Git.
        install_common(self.root)
        workflow = self.root / ".trellis/workflow.md"
        workflow.write_bytes((PACKAGE.parents[4] / "trellis/workflows/guru-team/workflow.md").read_bytes())
        self.git("restore", "--source", carrier, "--worktree", "--", task_ref)
        self.assertNotEqual(0, subprocess.run(
            ["git", "cat-file", "-e", f"HEAD:{task_ref}/task.json"], cwd=self.root,
            capture_output=True,
        ).returncode)
        self.assertIn("?? .trellis/", self.git("status", "--porcelain"))
        ordinary = MODULE.run(PACKAGE, {"id": "discover-task-branch-binding-candidates"},
                              ["--root", str(self.root), "--input", json.dumps(self.input)])
        target_candidates = [row for row in ordinary["candidates"] if row["branch_name"] == "main"]
        self.assertEqual(len(target_candidates), 1)
        self.assertFalse(target_candidates[0]["valid"])
        self.assertEqual(target_candidates[0]["reason_code"], "task_artifact_mismatch")
        restored = {"profile": "delivery_restored_checkout", "mode": "standalone",
                    "task_id": "demo", "task_ref": task_ref, "lifecycle_generation": 0,
                    "branch_name": "main", "expected_head": target_head}
        command = subprocess.run(
            [str(PACKAGE / "scripts/invoke.sh"), "--root", str(self.root), "--input", "-"],
            input=json.dumps(restored), capture_output=True, text=True,
        )
        self.assertEqual(0, command.returncode, command.stdout + command.stderr)
        established = json.loads(command.stdout)
        self.assertEqual(established, {"exit_id": "binding_established", "task_id": "demo",
                                       "lifecycle_generation": 0})
        repository = inspect_repository(self.root)
        store, ledger = BranchBindingStore(repository), ResourceLedgerStore(repository)
        binding = store.read(self.key)
        self.assertEqual((binding.branch_name, binding.binding_revision), ("main", 0))
        self.assertEqual(ledger.read_current(self.key).branch_name, "main")
        resources = ledger.read(self.key).resources
        self.assertEqual([(row.kind, row.ownership) for row in resources], [("local_branch", "caller_owned")])
        before = (store.snapshot(self.key), ledger.snapshot(self.key))
        self.assertEqual(self.invoke(restored), established)
        recovery = {**self.input, "action": "recover", "recovery": {
            "expected_revision": binding.binding_revision,
            "expected_branch_name": "main", "expected_head": target_head,
        }}
        self.assertEqual(self.invoke(recovery), established)
        self.assertEqual((store.snapshot(self.key), ledger.snapshot(self.key)), before)

        # This is a package/native-API integration fixture. Its semantic Bind
        # input does not claim that a native Agent performed an AI review.
        public = {"profile": "delivery_rebind_missing_session", "mode": "standalone",
                  "task_id": established["task_id"],
                  "lifecycle_generation": established["lifecycle_generation"],
                  "continuation_id": "restored-carrier-fixture"}
        semantic = {**public, "route": "rebind", "resume_target": "guru-current-phase-router",
                    "ai_review_gate": {"status": "passed", "summary": "Fixture selects the restored identity."}}
        context = "restored-carrier-fixture"
        bound = subprocess.run(
            [str(PACKAGE.parent / "guru-bind-task-session/scripts/invoke.sh"),
             "--root", str(self.root), "--input", json.dumps(public),
             "--owner-result", json.dumps(semantic)],
            env={**os.environ, "TRELLIS_CONTEXT_ID": context}, capture_output=True, text=True,
        )
        self.assertEqual(0, bound.returncode, bound.stdout + bound.stderr)
        rebound = json.loads(bound.stdout)
        self.assertEqual((rebound["exit_id"], rebound["task_id"], rebound["lifecycle_generation"]),
                         ("session_rebound", "demo", 0))
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": context}):
            current = upstream_modules(self.root).delivery_session.get_current_delivery(self.root)
        self.assertEqual(current, {"kind": "no_current_delivery",
                                   "key": {"task_id": "demo", "lifecycle_generation": 0}})
        self.assertEqual(self.git("rev-parse", "HEAD"), target_head)
        self.assertEqual(original, {path.relative_to(task).as_posix(): path.read_bytes()
                                    for path in task.rglob("*") if path.is_file()})
        retained = json.loads((task / "task.json").read_text())["deliveries"][0]
        self.assertEqual(retained["id"], delivery_id)
        for name in ("publication_result", "delivery_result"):
            self.assertIsNone(retained[name])
        for name in ("full_review", "readiness"):
            self.assertIsNone(retained["results"][name])

    def test_restored_profile_keeps_identity_rejection_and_read_only_command_boundary(self) -> None:
        restored = {"profile": "delivery_restored_checkout", "mode": "workflow",
                    "task_id": "demo", "task_ref": self.input["task_ref"], "lifecycle_generation": 1,
                    "branch_name": "task/demo", "expected_head": self.head}
        self.assertEqual(self.invoke(restored)["exit_id"], "invalid_task_state")
        for command_id in ("discover-task-branch-binding-candidates", "record-task-branch-binding-plan"):
            with self.subTest(command=command_id), self.assertRaises(MODULE.CommandError) as error:
                MODULE.run(PACKAGE, {"id": command_id}, ["--root", str(self.root), "--input", json.dumps(restored)])
            self.assertEqual("invalid_arguments", error.exception.code)
        self.assertIsNone(BranchBindingStore(self.repo).read(self.key))
        self.assertIsNone(ResourceLedgerStore(self.repo).read_current(self.key))


if __name__ == "__main__":
    unittest.main()
