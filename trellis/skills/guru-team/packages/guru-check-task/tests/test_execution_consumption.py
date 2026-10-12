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

    def record_check(self, *, blocked: bool = False, reason: str | None = None,
                     candidates: list | None = None, result: str = "passed") -> dict:
        example = json.loads((PACKAGE / "examples/phase2-check.json").read_text())
        authoring = {key: copy.deepcopy(example[key]) for key in CHECK_FIELDS}
        if candidates is not None:
            authoring["candidate_classifications"] = copy.deepcopy(candidates)
        tracked = self.git("ls-files", "-z").split("\0")
        untracked = self.git("ls-files", "--others", "--exclude-standard", "-z").split("\0")
        authoring["reviewed_paths"] = sorted({path for path in [*tracked, *untracked] if path})
        if reason is not None:
            authoring["reason"] = reason
        if result == "resolved_reconciliation_passed":
            authoring["typed_exit"] = result
            authoring["consumer"] = {"kind": "skill", "id": "guru-reconcile-task-base"}
        elif result in {"implementation_required", "planning_stale"}:
            authoring["typed_exit"] = result
            authoring["semantic_review"]["status"] = result
            ref = authoring["candidate_classifications"][0]["candidate_ref"]
            if result == "implementation_required":
                authoring["consumer"] = {"kind": "workflow", "id": "guru-resume-implementation"}
                authoring["semantic_review"]["adequacy_dimensions"][2]["status"] = "failed"
                authoring["semantic_review"]["findings"] = [{
                    "id": "F-boundary", "candidate_ref": ref, "severity": "P2",
                    "summary": "The upper endpoint is excluded.",
                    "path": "candidate.txt", "status": "open",
                }]
                decision = "current_scope"
            else:
                authoring["consumer"] = {"kind": "workflow", "id": "guru-task-check-planning-router"}
                authoring["route"] = "reapprove_plan"
                decision = "scope_change_required"
            authoring["semantic_review"]["scope_decisions"] = [{
                "id": "scope-boundary", "candidate_ref": ref,
                "disposition": decision, "summary": "The endpoint contract requires current review.",
                "finding_id": "F-boundary" if result == "implementation_required" else None,
            }]
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

    def select_profile(self, profile: str) -> None:
        names = {
            "initial_check": "initial-check", "finding_fix_rerun": "finding-fix-rerun",
            "planning_reentry": "planning-reentry", "resolved_reconciliation": "resolved-reconciliation",
        }
        self.public = json.loads((PACKAGE / f"examples/public-{names[profile]}-input.json").read_text())
        self.public["task_ref"] = TASK_REF

    def project_resolved(self, owner: dict) -> subprocess.CompletedProcess:
        public_path = self.runtime / "resolved-public.json"
        public_path.write_text(json.dumps(self.public))
        authoring = json.loads((PACKAGE / "examples/public-resolved-reconciliation-authoring.json").read_text())
        authoring["parent_order"][0] = owner["phase2_capture_commit"]
        authoring_path = self.runtime / "resolved-authoring.json"
        authoring_path.write_text(json.dumps(authoring))
        return self.command(PACKAGE, "project-resolved-reconciliation.sh",
                            "--input", str(public_path), "--owner-result", str(self.checkpoint),
                            "--authoring", str(authoring_path))

    def boundary_candidate(self, decision: str = "rejected_not_reproduced") -> dict:
        row = json.loads((PACKAGE / "examples/phase2-rejected-candidates.json").read_text())[0]
        row["decision"] = decision
        if decision == "qualified_current":
            row["witness"]["defect_observation"] = "The staged current-scope implementation excludes the upper endpoint."
        elif decision == "qualified_approved_expansion":
            row["witness"]["defect_observation"] = "The current authority requests a new endpoint contract."
        return row

    def test_zero_and_all_rejected_sets_use_original_chains_for_all_profiles(self) -> None:
        for profile in ("initial_check", "finding_fix_rerun", "planning_reentry", "resolved_reconciliation"):
            for candidates in ([], [self.boundary_candidate()]):
                with self.subTest(profile=profile, candidates=len(candidates)):
                    self.completed_execution()
                    self.select_profile(profile)
                    execution = self.execution_path.read_bytes()
                    resolved = profile == "resolved_reconciliation"
                    owner = self.record_check(candidates=candidates,
                                              result="resolved_reconciliation_passed" if resolved else "passed")
                    self.assertEqual(candidates, owner["candidate_classifications"])
                    output = self.successful(self.project_resolved(owner) if resolved else self.invoke_check(owner))
                    self.assertEqual(TASK_REF, output["task_ref"])
                    self.assertEqual(owner["phase2_capture_commit"], output["phase2_commit_anchor"])
                    if resolved:
                        self.assertEqual("resolved_candidate", output["profile"])
                        self.assertEqual("resolved_reconciliation_passed", output["source_exit"])
                        self.assertNotIn("exit_id", output)
                        self.assertEqual(execution, self.execution_path.read_bytes())
                    else:
                        self.assertEqual("passed", output["exit_id"])
                        self.assertFalse(self.execution_path.exists())
                    self.assertEqual(owner, json.loads(self.checkpoint.read_text()))

    def test_nonempty_findings_and_planning_routes_keep_original_profile_consumers(self) -> None:
        for profile in ("initial_check", "finding_fix_rerun", "planning_reentry", "resolved_reconciliation"):
            for result, decision in (("implementation_required", "qualified_current"),
                                     ("planning_stale", "qualified_approved_expansion")):
                with self.subTest(profile=profile, result=result):
                    self.completed_execution()
                    self.select_profile(profile)
                    execution = self.execution_path.read_bytes()
                    owner = self.record_check(candidates=[self.boundary_candidate(decision)], result=result)
                    output = self.successful(self.invoke_check(owner))
                    self.assertEqual(result, output["exit_id"])
                    key, refs = ("finding_refs", ["F-boundary"]) if result == "implementation_required" else ("proposal_refs", ["scope-boundary"])
                    self.assertEqual(refs, output[key])
                    self.assertEqual(execution, self.execution_path.read_bytes())
                    self.assertFalse(self.checkpoint.exists())

    def test_zero_candidates_do_not_bypass_missing_evidence_or_content_freshness(self) -> None:
        for profile in ("initial_check", "finding_fix_rerun", "planning_reentry", "resolved_reconciliation"):
            with self.subTest(profile=profile):
                self.completed_execution()
                self.select_profile(profile)
                execution = self.execution_path.read_bytes()
                blocked = self.record_check(blocked=True)
                self.assertEqual([], blocked["candidate_classifications"])
                self.assertEqual({"exit_id": "blocked"}, self.successful(self.invoke_check(blocked)))
                self.assertEqual(execution, self.execution_path.read_bytes())
                self.assertFalse(self.checkpoint.exists())
                resolved = profile == "resolved_reconciliation"
                owner = self.record_check(result="resolved_reconciliation_passed" if resolved else "passed")
                checked = self.checkpoint.read_bytes()
                (self.repo / "candidate.txt").write_text(f"New ordinary content after {profile} review.\n")
                outcome = self.project_resolved(owner) if resolved else self.invoke_check(owner)
                self.assertEqual(3, outcome.returncode, outcome.stdout + outcome.stderr)
                self.assertEqual("stale_identity", json.loads(outcome.stdout)["code"])
                self.assertEqual(execution, self.execution_path.read_bytes())
                self.assertEqual(checked, self.checkpoint.read_bytes())

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
