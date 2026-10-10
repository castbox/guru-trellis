"""Deterministic producer/consumer integration, not semantic adequacy evidence.

Planning and Check run their original recorder/checker/public wrappers. The
execution owner runs its real composition and recorder functions; its complete
session/public invocation behavior is covered by its own package tests.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
sys.path.insert(0, str(SKILLS))

from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.composition import activate_task_status, prepare_activation_inputs, prepare_resume_execution_inputs
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.session_adapter import SessionAdapterResult

EXECUTION_PACKAGE = PACKAGE.parent / "guru-activate-task"
SPEC = importlib.util.spec_from_file_location("execution_consumption_owner", EXECUTION_PACKAGE / "runtime/execution_result.py")
EXECUTION_OWNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXECUTION_OWNER)

TASK_REF = ".trellis/tasks/test-task"
CHECK_FIELDS = (
    "mode", "reviewed_paths", "validation", "docs_ssot", "delivery_policy",
    "candidate_classifications", "semantic_review", "typed_exit", "route", "reason", "consumer",
)


class ExecutionConsumptionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name).resolve()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.task_dir = self.repo / TASK_REF
        self.task_dir.mkdir(parents=True)
        self.task_file = self.task_dir / "task.json"
        self.task_file.write_text(json.dumps({
            "id": "test-task", "name": "test-task", "lifecycle_generation": 0,
            "source": {"kind": "no_issue"}, "title": "Task", "description": "Reviewed scope",
            "status": "in_progress", "dev_type": None, "scope": None, "package": None,
            "priority": "P2", "createdAt": "2026-10-10", "completedAt": None,
            "base_branch": "main", "worktree_path": None, "commit": None, "pr_url": None,
            "children": [], "parent": None, "relatedFiles": [], "notes": "", "meta": {},
        }))
        for name in ("prd.md", "design.md", "implement.md"):
            (self.task_dir / name).write_text(f"# {name}\n\nCurrent accepted scope.\n")
        (self.repo / ".gitignore").write_text(".trellis/.runtime/\n")
        (self.repo / "candidate.txt").write_text("initial\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        self.key = TaskLifecycleKey("test-task", 0)
        repository = inspect_repository(self.repo)
        BranchBindingStore(repository).establish(self.key, "main")
        ResourceLedgerStore(repository).establish_current(
            self.key, binding_revision=0, branch_name="main",
            branch_ownership="caller_owned", worktree_ownership="not_applicable",
        )
        self.runtime = self.repo / ".trellis/.runtime"
        self.runtime.mkdir(parents=True)
        self.checkpoint = self.runtime / "guru-team/owner-checkpoints/test-task/phase2-check.json"
        self.execution_path = EXECUTION_OWNER.execution_result_path(self.repo, TASK_REF)
        self.public = {
            "profile": "initial_check", "mode": "workflow", "task_ref": TASK_REF,
            "source_exit": "implementation_complete",
        }

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.repo, text=True).strip()

    def command(self, package: Path, script: str, *args: str, input: str | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [str(package / "scripts" / script), "--root", str(self.repo), *args],
            text=True, input=input, capture_output=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def successful(self, result: subprocess.CompletedProcess) -> dict:
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        if Path(result.args[0]).name != "invoke.sh":
            from runtime.io import project_intermediate_receipt
            return project_intermediate_receipt(payload, PACKAGE.parents[1] / "schemas")
        return payload

    def completed_execution(self, operation: str = "resume_execution") -> None:
        planning = PACKAGE.parent / "guru-approve-task-plan"
        example = json.loads((planning / "examples/planning-approval.json").read_text())
        fields = ("mode", "authority_refs", "delivery_policy", "docs_ssot_plan", "semantic_review", "typed_exit", "consumer", "reason")
        authoring = {key: copy.deepcopy(example[key]) for key in fields}
        authoring["mode"] = "workflow"
        authoring_path = self.runtime / "planning-authoring.json"
        authoring_path.write_text(json.dumps(authoring))
        recorded = self.successful(self.command(planning, "record-planning-approval.sh", "--task", TASK_REF, "--input", str(authoring_path)))
        self.successful(self.command(planning, "check-planning-approval.sh", "--task", TASK_REF))
        public_path = self.runtime / "planning-public.json"
        public_path.write_text(json.dumps({"profile": "initial_review", "mode": "workflow", "task_ref": TASK_REF, "source_exit": "planning_ready"}))
        approved = self.successful(self.command(planning, "invoke.sh", "--input", str(public_path), "--owner-result", recorded["artifact_path"]))
        self.assertEqual("approved", approved["exit_id"])
        head = self.git("rev-parse", "HEAD")
        payload = {
            "task_id": "test-task", "task_ref": approved["task_ref"], "lifecycle_generation": 0,
            "planning_result_id": approved["planning_result_id"], "selected_base_ref": "main",
            "continuity": {"kind": "base_current", "task_head": head, "base_head": head},
            "session_mode": "explicit_task_mode",
        }
        session = SessionAdapterResult("explicit_task_mode", self.key)
        if operation == "activate":
            metadata = json.loads(self.task_file.read_text())
            metadata["status"] = "planning"
            self.task_file.write_text(json.dumps(metadata))
            inputs = prepare_activation_inputs(self.repo, payload, session)
            activate_task_status(self.repo, inputs)
        else:
            inputs = prepare_resume_execution_inputs(self.repo, payload, session)
        EXECUTION_OWNER.record_execution_result(self.repo, inputs, operation=operation)

    def record_check(self, *, blocked: bool = False, reason: str | None = None) -> dict:
        example = json.loads((PACKAGE / "examples/phase2-check.json").read_text())
        authoring = {key: copy.deepcopy(example[key]) for key in CHECK_FIELDS}
        tracked = self.git("ls-files", "-z").split("\0")
        untracked = self.git("ls-files", "--others", "--exclude-standard", "-z").split("\0")
        authoring["reviewed_paths"] = sorted({path for path in [*tracked, *untracked] if path})
        if reason is not None:
            authoring["reason"] = reason
        if blocked:
            authoring["typed_exit"] = "blocked"
            authoring["consumer"] = {"kind": "stop", "id": "task-check-blocked"}
            authoring["semantic_review"]["status"] = "blocked"
            authoring["semantic_review"]["adequacy_dimensions"][-1]["status"] = "blocked"
            authoring["validation"]["unverified_items"] = [{"id": "evidence", "summary": "Required integration evidence is unavailable.", "blocking": True}]
        authoring_path = self.runtime / "check-authoring.json"
        authoring_path.write_text(json.dumps(authoring))
        self.successful(self.command(PACKAGE, "record-phase2-check.sh", "--task", TASK_REF, "--input", str(authoring_path)))
        self.successful(self.command(PACKAGE, "check-phase2-check.sh", "--task", TASK_REF))
        return json.loads(self.checkpoint.read_text())

    def invoke_check(self, owner: dict) -> subprocess.CompletedProcess:
        return self.command(PACKAGE, "invoke.sh", "--invocation", "-", input=json.dumps({"public_input": self.public, "owner_result": owner}))

    def test_current_passed_consumes_each_completed_operation_and_rematerializes_output(self) -> None:
        for operation in ("activate", "resume_execution"):
            with self.subTest(operation=operation):
                self.completed_execution(operation)
                metadata = self.task_file.read_bytes()
                before = self.git("status", "--porcelain=v1", "--untracked-files=all")
                owner = self.record_check()
                output = self.successful(self.invoke_check(owner))
                self.assertEqual("passed", output["exit_id"])
                self.assertFalse(self.execution_path.exists())
                self.assertEqual(json.loads(self.checkpoint.read_text()), owner)
                self.assertEqual(metadata, self.task_file.read_bytes())
                self.assertEqual(before, self.git("status", "--porcelain=v1", "--untracked-files=all"))
                self.assertEqual(output, self.successful(self.invoke_check(owner)))

    def test_nonpassed_retains_completed_execution_bytes(self) -> None:
        self.completed_execution()
        execution = self.execution_path.read_bytes()
        owner = self.record_check(blocked=True)
        self.assertEqual({"exit_id": "blocked"}, self.successful(self.invoke_check(owner)))
        self.assertEqual(execution, self.execution_path.read_bytes())
        self.assertFalse(self.checkpoint.exists())

    def test_content_changed_after_check_retains_both_producer_checkpoints(self) -> None:
        self.completed_execution()
        owner = self.record_check()
        execution = self.execution_path.read_bytes()
        checked = self.checkpoint.read_bytes()
        (self.repo / "candidate.txt").write_text("later candidate\n")
        result = self.invoke_check(owner)
        self.assertEqual(3, result.returncode, result.stdout + result.stderr)
        self.assertEqual("stale_identity", json.loads(result.stdout)["code"])
        self.assertEqual(execution, self.execution_path.read_bytes())
        self.assertEqual(checked, self.checkpoint.read_bytes())

    def test_prior_check_output_does_not_consume_new_producer_result(self) -> None:
        self.completed_execution()
        prior = self.record_check()
        current = self.record_check(reason="Fresh review supersedes the prior round.")
        self.assertNotEqual(prior, current)
        execution = self.execution_path.read_bytes()
        result = self.invoke_check(prior)
        self.assertEqual(3, result.returncode, result.stdout + result.stderr)
        self.assertEqual("stale_identity", json.loads(result.stdout)["code"])
        self.assertEqual(current, json.loads(self.checkpoint.read_text()))
        self.assertEqual(execution, self.execution_path.read_bytes())

    def test_new_current_check_retains_execution_result_from_prior_plan(self) -> None:
        self.completed_execution()
        execution = self.execution_path.read_bytes()
        (self.task_dir / "design.md").write_text("# Current revised design\n")
        owner = self.record_check()
        self.assertEqual("passed", self.successful(self.invoke_check(owner))["exit_id"])
        self.assertEqual(execution, self.execution_path.read_bytes())
        self.assertEqual(owner, json.loads(self.checkpoint.read_text()))


if __name__ == "__main__":
    unittest.main()
