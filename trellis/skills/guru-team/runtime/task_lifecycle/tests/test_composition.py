from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.checkout_acquisition import CheckoutAcquisitionPlan, acquire_checkout
from runtime.task_lifecycle.composition import (
    bind_created_session, establish_created_control_state, prepare_activation_inputs, prepare_creation_inputs,
    recover_created_control_state,
)
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.session_adapter import SessionAdapterResult


TASK_ID = "new-task"
TASK_REF = ".trellis/tasks/09-25-new-task"


class CompositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Lifecycle Tests")
        self.git("config", "user.email", "tests@example.com")
        (self.repo / "README.md").write_text("fixture\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "fixture")
        self.head = self.git("rev-parse", "HEAD")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.repo, text=True).strip()

    def creation(self, profile: str = "standalone_request") -> dict:
        return {
            "task_id": TASK_ID,
            "task_ref": TASK_REF,
            "source_profile": profile,
            "reviewed_source": {"kind": "no_issue"} if profile == "standalone_request" else {
                "kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454,
            },
            "accepted_scope_identity": "scope:reviewed",
            "delivery_target": {"repo_ref": "castbox/guru-trellis", "branch_ref": "main"},
            "selected_base_ref": "main",
            "reviewed_base_head": self.head,
        }

    def acquisition(self, route: str = "adopt_invocation_checkout", disposition: str = "new_branch", invocation: Path | None = None) -> CheckoutAcquisitionPlan:
        return CheckoutAcquisitionPlan(
            route=route,
            repository_context=self.repo,
            task_id=TASK_ID,
            task_ref=TASK_REF,
            lifecycle_generation=0,
            branch_ref="codex/new-task",
            expected_status="planning",
            decision_head=self.head,
            transaction_id="acquire:1",
            result_id="checkout:1",
            invocation_checkout=(invocation or self.repo) if route == "adopt_invocation_checkout" else None,
            target_path=Path(self.temporary.name) / "linked" if route == "provision_linked_worktree" else None,
            provision_disposition=disposition if route == "provision_linked_worktree" else None,
            task_artifact_expectation="absent",
        )

    def test_both_reviewed_source_profiles_and_checkout_routes_are_inputs_only(self) -> None:
        for profile in ("standalone_request", "existing_issue"):
            for route in ("adopt_invocation_checkout", "provision_linked_worktree"):
                with self.subTest(profile=profile, route=route):
                    result = prepare_creation_inputs(self.repo, self.creation(profile), self.acquisition(route))
                    self.assertEqual(result.reviewed_source["kind"], "no_issue" if profile == "standalone_request" else "issue")
                    self.assertEqual(result.accepted_scope_identity, "scope:reviewed")
                    self.assertNotIn("accepted_scope_identity", result.reviewed_source)
                    self.assertEqual(result.acquisition.route, route)
        self.assertFalse((self.repo / TASK_REF).exists())
        self.assertEqual(self.git("branch", "--list", "codex/new-task"), "")

    def test_creation_rejects_profile_mismatch_and_preexisting_identity(self) -> None:
        payload = self.creation()
        payload["reviewed_source"] = {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454}
        with self.assertRaises(LifecycleContractError):
            prepare_creation_inputs(self.repo, payload, self.acquisition())
        path = self.repo / TASK_REF
        path.mkdir(parents=True)
        (path / "task.json").write_text(json.dumps({"id": TASK_ID, "status": "planning"}), encoding="utf-8")
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_creation_inputs(self.repo, self.creation(), self.acquisition())
        self.assertEqual(raised.exception.code, "task_identity_already_exists")

    def test_creation_rejects_unretired_prior_generation_resource_identity(self) -> None:
        self.git("branch", "legacy-task")
        resources = ResourceLedgerStore(inspect_repository(self.repo))
        resources.establish_current(
            TaskLifecycleKey(TASK_ID, 1), binding_epoch=7, binding_revision=0,
            branch_name="legacy-task", branch_ownership="caller_owned",
            worktree_ownership="not_applicable",
        )
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_creation_inputs(self.repo, self.creation(), self.acquisition())
        self.assertEqual(raised.exception.code, "task_identity_already_exists")
        self.assertFalse((self.repo / TASK_REF).exists())

    def test_creation_rejects_archived_identity_in_registered_sibling_checkout(self) -> None:
        sibling = Path(self.temporary.name) / "prior-task"
        self.git("worktree", "add", "-b", "prior-task", str(sibling))
        archived = sibling / ".trellis/tasks/archive/2026-09/prior-task"
        archived.mkdir(parents=True)
        (archived / "task.json").write_text(
            json.dumps({"id": TASK_ID, "status": "completed", "lifecycle_generation": 0}), encoding="utf-8",
        )
        self.assertFalse((self.repo / archived.relative_to(sibling)).exists())
        self.assertIsNone(ResourceLedgerStore(inspect_repository(self.repo)).read(TaskLifecycleKey(TASK_ID, 0)))
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_creation_inputs(self.repo, self.creation(), self.acquisition())
        self.assertEqual(raised.exception.code, "task_identity_already_exists")
        self.assertFalse((self.repo / TASK_REF).exists())

    def test_recovery_rejects_branch_ledger_disagreement(self) -> None:
        plan = self.acquisition("provision_linked_worktree")
        inputs = prepare_creation_inputs(self.repo, self.creation(), plan)
        acquired = acquire_checkout(plan)
        task = acquired.checkout.path / TASK_REF
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps({
            "id": TASK_ID, "status": "planning", "lifecycle_generation": 0,
            "source": inputs.reviewed_source, "delivery_target": inputs.delivery_target,
        }), encoding="utf-8")
        self.git("branch", "unrelated-branch")
        repository = inspect_repository(self.repo)
        key = TaskLifecycleKey(TASK_ID, 0)
        binding = BranchBindingStore(repository).establish(key, "codex/new-task")
        ResourceLedgerStore(repository).establish_current(
            key, binding_epoch=binding.binding_epoch, binding_revision=0,
            branch_name="unrelated-branch", branch_ownership=acquired.branch_ownership,
            worktree_ownership=acquired.worktree_ownership,
        )
        with self.assertRaises(LifecycleContractError) as raised:
            recover_created_control_state(
                inputs, acquired, expected_epoch=binding.binding_epoch,
                expected_result_id=inputs.result_id,
            )
        self.assertEqual(raised.exception.code, "creation_result_mismatch")

    def test_creation_requires_pre_task_plan_and_non_delivery_branch(self) -> None:
        plan = self.acquisition()
        for changes in (
            {"task_artifact_expectation": "required"}, {"lifecycle_generation": 1},
            {"branch_ref": "main"}, {"decision_head": "a" * 40},
        ):
            with self.subTest(changes=changes):
                invalid = CheckoutAcquisitionPlan(**{**vars(plan), **changes})
                with self.assertRaises(LifecycleContractError):
                    prepare_creation_inputs(self.repo, self.creation(), invalid)
        stale = self.creation()
        stale["reviewed_base_head"] = "a" * 40
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_creation_inputs(self.repo, stale, plan)
        self.assertEqual(raised.exception.code, "creation_base_stale")

    def assert_created(self, route: str, disposition: str = "new_branch", invocation: Path | None = None) -> None:
        plan = self.acquisition(route, disposition, invocation)
        inputs = prepare_creation_inputs(self.repo, self.creation(), plan)
        acquired = acquire_checkout(plan)
        task = acquired.checkout.path / TASK_REF
        task.mkdir(parents=True)
        (task / "task.json").write_text(
            json.dumps({
                "id": TASK_ID, "status": "planning", "lifecycle_generation": 0,
                "source": inputs.reviewed_source, "delivery_target": inputs.delivery_target,
            }), encoding="utf-8",
        )
        binding = establish_created_control_state(inputs, acquired)
        self.assertEqual(binding.binding_revision, 0)
        ledger = ResourceLedgerStore(inspect_repository(self.repo)).read(TaskLifecycleKey(TASK_ID, 0))
        expected_branch_owner = "guru_owned" if disposition == "new_branch" and route == "provision_linked_worktree" else "caller_owned"
        expected_worktree_owner = "guru_owned" if route == "provision_linked_worktree" and disposition != "existing_checkout" else "caller_owned"
        self.assertEqual(ledger.resources[0].ownership, expected_branch_owner)
        if acquired.checkout.topology == "linked":
            self.assertEqual(ledger.resources[1].ownership, expected_worktree_owner)
        else:
            self.assertEqual(len(ledger.resources), 1)
        recovered = recover_created_control_state(
            inputs, acquired, expected_epoch=binding.binding_epoch, expected_result_id=inputs.result_id,
        )
        self.assertEqual(recovered, binding)
        self.assertEqual(ResourceLedgerStore(inspect_repository(self.repo)).read(TaskLifecycleKey(TASK_ID, 0)), ledger)
        wrong_owner = "guru_owned" if acquired.branch_ownership == "caller_owned" else "caller_owned"
        with self.assertRaises(LifecycleContractError) as raised:
            recover_created_control_state(
                inputs, replace(acquired, branch_ownership=wrong_owner),
                expected_epoch=binding.binding_epoch, expected_result_id=inputs.result_id,
            )
        self.assertEqual(raised.exception.code, "creation_acquisition_mismatch")
        with self.assertRaises(LifecycleContractError) as raised:
            establish_created_control_state(inputs, acquired)
        self.assertEqual(raised.exception.code, "creation_control_state_exists")
        for epoch, result_id in ((binding.binding_epoch + 1, inputs.result_id), (binding.binding_epoch, "task-created:other")):
            with self.assertRaises(LifecycleContractError):
                recover_created_control_state(inputs, acquired, expected_epoch=epoch, expected_result_id=result_id)
        data = json.loads((task / "task.json").read_text())
        data["source"] = {"kind": "no_issue"} if inputs.reviewed_source["kind"] == "issue" else {
            "kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454,
        }
        (task / "task.json").write_text(json.dumps(data))
        with self.assertRaises(LifecycleContractError) as raised:
            recover_created_control_state(inputs, acquired, expected_epoch=binding.binding_epoch, expected_result_id=inputs.result_id)
        self.assertEqual(raised.exception.code, "creation_identity_mismatch")
        self.assertEqual(ResourceLedgerStore(inspect_repository(self.repo)).read(TaskLifecycleKey(TASK_ID, 0)), ledger)

    def test_adopt_primary_ownership(self) -> None:
        self.git("switch", "-c", "codex/new-task")
        self.assert_created("adopt_invocation_checkout")

    def test_adopt_linked_ownership(self) -> None:
        self.git("branch", "codex/new-task")
        linked = Path(self.temporary.name) / "linked"
        self.git("worktree", "add", str(linked), "codex/new-task")
        self.assert_created("adopt_invocation_checkout", invocation=linked)

    def test_provision_new_branch_ownership(self) -> None:
        self.assert_created("provision_linked_worktree", "new_branch")

    def test_provision_existing_branch_ownership(self) -> None:
        self.git("branch", "codex/new-task")
        self.assert_created("provision_linked_worktree", "existing_branch")

    def test_provision_existing_checkout_ownership(self) -> None:
        self.git("branch", "codex/new-task")
        linked = Path(self.temporary.name) / "linked"
        self.git("worktree", "add", str(linked), "codex/new-task")
        self.assert_created("provision_linked_worktree", "existing_checkout")

    def test_created_session_missing_context_or_write_failure_preserves_control_state(self) -> None:
        self.git("switch", "-c", "codex/new-task")
        plan = self.acquisition()
        inputs = prepare_creation_inputs(self.repo, self.creation(), plan)
        acquired = acquire_checkout(plan)
        task = self.repo / TASK_REF
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps({
            "id": TASK_ID, "status": "planning", "lifecycle_generation": 0,
            "source": inputs.reviewed_source, "delivery_target": inputs.delivery_target,
        }), encoding="utf-8")
        binding = establish_created_control_state(inputs, acquired)

        class SessionPort:
            def __init__(self, key: str | None) -> None:
                self.key = key
                self.writes = 0

            def resolve_context_key(self, platform_input=None, platform=None):
                return self.key

            def repository_facts(self, root):
                return inspect_repository(root)

            def session_path(self, root, key, facts):
                return facts.common_dir / "trellis" / "sessions" / f"{key}.json"

            def resolve_task_identity(self, facts, task_id, lifecycle_generation):
                return type("Resolved", (), {"task_ref": TASK_REF})()

            def write_record(self, path, data, root):
                self.writes += 1
                raise OSError("session store unavailable")

        absent = SessionPort(None)
        explicit = bind_created_session(absent, inputs, acquired, expected_epoch=binding.binding_epoch)
        self.assertEqual(explicit.status, "explicit_task_mode")
        self.assertEqual(absent.writes, 0)
        failing = SessionPort("codex-test")
        failed = bind_created_session(failing, inputs, acquired, expected_epoch=binding.binding_epoch)
        self.assertEqual(failed.status, "session_write_failed")
        self.assertEqual(failing.writes, 1)
        self.assertEqual(BranchBindingStore(inspect_repository(self.repo)).read(TaskLifecycleKey(TASK_ID, 0)), binding)
        self.assertIsNotNone(ResourceLedgerStore(inspect_repository(self.repo)).read(TaskLifecycleKey(TASK_ID, 0)))

    def planning_task(self) -> None:
        self.base_head = self.head
        self.git("branch", "base", self.base_head)
        path = self.repo / TASK_REF
        path.mkdir(parents=True)
        (path / "task.json").write_text(json.dumps({"id": TASK_ID, "status": "planning", "lifecycle_generation": 0, "base_branch": "base"}), encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "task")
        self.head = self.git("rev-parse", "HEAD")
        repository = inspect_repository(self.repo)
        key = TaskLifecycleKey(TASK_ID, 0)
        BranchBindingStore(repository).establish(key, "main", binding_epoch=7)
        ResourceLedgerStore(repository).establish_current(
            key, binding_epoch=7, binding_revision=0, branch_name="main",
            branch_ownership="caller_owned", worktree_ownership="not_applicable",
        )

    def activation(self) -> dict:
        return {
            "task_id": TASK_ID, "task_ref": TASK_REF, "lifecycle_generation": 0,
            "planning_result_id": "planning:1", "selected_base_ref": "base",
            "continuity": {"kind": "base_current", "task_head": self.head, "base_head": self.base_head},
            "session_mode": "explicit_task_mode",
        }

    def test_activation_accepts_explicit_mode_and_reconciled_continuity_without_mutation(self) -> None:
        self.planning_task()
        session = SessionAdapterResult("explicit_task_mode", TaskLifecycleKey(TASK_ID, 0), reason_code="context_key_unavailable")
        result = prepare_activation_inputs(self.repo, self.activation(), session)
        self.assertEqual(result.session_mode, "explicit_task_mode")
        reconciled = self.activation()
        reconciled["continuity"] = {
            "kind": "reconciled", "task_head": self.head, "new_base_head": self.base_head,
            "result_id": "reconcile:1", "resume_target": "task_activation",
        }
        self.assertEqual(prepare_activation_inputs(self.repo, reconciled, session).continuity["kind"], "reconciled")
        bound = self.activation()
        bound["session_mode"] = "session_bound"
        self.assertEqual(
            prepare_activation_inputs(self.repo, bound, SessionAdapterResult("session_bound", TaskLifecycleKey(TASK_ID, 0))).session_mode,
            "session_bound",
        )
        self.assertEqual(json.loads((self.repo / TASK_REF / "task.json").read_text())["status"], "planning")

    def test_activation_rejects_stale_head_session_and_status(self) -> None:
        self.planning_task()
        session = SessionAdapterResult("explicit_task_mode", TaskLifecycleKey(TASK_ID, 0))
        payload = self.activation()
        payload["continuity"]["task_head"] = "a" * 40
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_activation_inputs(self.repo, payload, session)
        self.assertEqual(raised.exception.code, "activation_head_stale")
        payload = self.activation()
        payload["session_mode"] = "session_bound"
        with self.assertRaises(LifecycleContractError):
            prepare_activation_inputs(self.repo, payload, session)
        metadata = self.repo / TASK_REF / "task.json"
        data = json.loads(metadata.read_text())
        data["status"] = "in_progress"
        metadata.write_text(json.dumps(data))
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_activation_inputs(self.repo, self.activation(), session)
        self.assertEqual(raised.exception.code, "activation_status_mismatch")

    def test_activation_rejects_selected_base_drift_and_unrelated_reconcile(self) -> None:
        self.planning_task()
        session = SessionAdapterResult("explicit_task_mode", TaskLifecycleKey(TASK_ID, 0))
        self.git("update-ref", "refs/heads/base", self.head)
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_activation_inputs(self.repo, self.activation(), session)
        self.assertEqual(raised.exception.code, "activation_base_stale")
        reconciled = self.activation()
        reconciled["continuity"] = {
            "kind": "reconciled", "task_head": self.head, "new_base_head": self.base_head,
            "result_id": "reconcile:1", "resume_target": "task_activation",
        }
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_activation_inputs(self.repo, reconciled, session)
        self.assertEqual(raised.exception.code, "activation_base_stale")
        wrong_base = self.activation()
        wrong_base["selected_base_ref"] = "main"
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_activation_inputs(self.repo, wrong_base, session)
        self.assertEqual(raised.exception.code, "activation_base_mismatch")


if __name__ == "__main__":
    unittest.main()
