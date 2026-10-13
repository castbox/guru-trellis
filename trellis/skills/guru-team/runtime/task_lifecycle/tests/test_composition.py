from __future__ import annotations

import hashlib
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
    bind_created_session, establish_created_control_state, prepare_creation_inputs,
    recover_created_control_state,
)
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.session_adapter import SessionAdapterResult
from runtime.delivery_projection.tests.upstream_fixture import install_common, public_task


TASK_ID = "new-task"
TASK_REF = ".trellis/tasks/09-25-new-task"


class CompositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name) / "repo"
        self.repo.mkdir()
        install_common(self.repo)
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

    @staticmethod
    def task_metadata(status: str, source: dict | None = None, base_branch: str = "main") -> dict:
        return public_task({
            "id": TASK_ID, "name": "09-25-new-task", "lifecycle_generation": 0,
            "source": source or {"kind": "no_issue"}, "title": "New task",
            "description": "Reviewed scope", "status": status, "dev_type": None,
            "scope": None, "package": None, "priority": "P2",
            "createdAt": "2026-09-25", "completedAt": None,
            "base_branch": base_branch, "worktree_path": None, "commit": None,
            "pr_url": None, "children": [], "parent": None,
            "relatedFiles": [], "notes": "", "meta": {},
        })

    def creation(self, profile: str = "standalone_request") -> dict:
        return {
            "task_id": TASK_ID,
            "task_ref": TASK_REF,
            "source_profile": profile,
            "reviewed_source": {"kind": "no_issue"} if profile == "standalone_request" else {
                "kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454, "disposition": "exact_source",
            },
            "accepted_scope_identity": "scope:reviewed",
            "delivery_target": {"repo_ref": "castbox/guru-trellis", "branch_ref": "main"},
            "selected_base_ref": "main",
            "reviewed_base_head": self.head,
        }

    def acquisition(self, route: str = "provision_linked_worktree", disposition: str = "new_branch", invocation: Path | None = None) -> CheckoutAcquisitionPlan:
        return CheckoutAcquisitionPlan(
            route=route,
            repository_context=self.repo,
            task_id=TASK_ID,
            task_ref=TASK_REF,
            lifecycle_generation=0,
            branch_ref="codex/new-task",
            expected_status="active",
            decision_head=self.head,
            transaction_id="acquire:1",
            result_id="checkout:1",
            invocation_checkout=(invocation or self.repo) if route == "adopt_invocation_checkout" else None,
            target_path=Path(self.temporary.name) / "linked" if route == "provision_linked_worktree" else None,
            provision_disposition=disposition if route == "provision_linked_worktree" else None,
            task_artifact_expectation="absent",
        )

    def test_both_reviewed_source_profiles_and_checkout_routes_are_inputs_only(self) -> None:
        linked = Path(self.temporary.name) / "adopted"
        self.git("worktree", "add", "-b", "codex/new-task", str(linked))
        for profile in ("standalone_request", "existing_issue"):
            for route in ("adopt_invocation_checkout", "provision_linked_worktree"):
                with self.subTest(profile=profile, route=route):
                    plan = self.acquisition(route, invocation=linked)
                    if route == "provision_linked_worktree":
                        plan = replace(plan, branch_ref="codex/provision-task")
                    result = prepare_creation_inputs(self.repo, self.creation(profile), plan)
                    self.assertEqual(result.reviewed_source["kind"], "no_issue" if profile == "standalone_request" else "issue")
                    self.assertEqual(result.accepted_scope_identity, "scope:reviewed")
                    self.assertNotIn("accepted_scope_identity", result.reviewed_source)
                    self.assertEqual(result.acquisition.route, route)
        self.assertFalse((self.repo / TASK_REF).exists())
        self.assertEqual(self.git("symbolic-ref", "HEAD"), "refs/heads/main")

    def test_creation_rejects_profile_mismatch_and_preexisting_identity(self) -> None:
        payload = self.creation()
        payload["reviewed_source"] = {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454, "disposition": "exact_source"}
        with self.assertRaises(LifecycleContractError):
            prepare_creation_inputs(self.repo, payload, self.acquisition())
        payload = self.creation("existing_issue")
        for disposition in ("exact_source", "reference_only"):
            payload["reviewed_source"]["disposition"] = disposition
            self.assertEqual(prepare_creation_inputs(self.repo, payload, self.acquisition()).reviewed_source,
                             payload["reviewed_source"])
        for disposition in ("follow_up", "parent"):
            payload["reviewed_source"]["disposition"] = disposition
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
            TaskLifecycleKey(TASK_ID, 1), binding_revision=0,
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

    def test_creation_ignores_unrelated_legacy_checkout_artifacts(self) -> None:
        sibling = Path(self.temporary.name) / "legacy"
        self.git("worktree", "add", "-b", "legacy", str(sibling))
        active = sibling / ".trellis/tasks/09-20-old"
        archived = sibling / ".trellis/tasks/archive/2026-09/09-20-old"
        active.mkdir(parents=True)
        archived.mkdir(parents=True)
        (active / "task.json").write_text(json.dumps({
            "id": "old-task", "name": "old-task", "title": "Old task",
            "status": "in_progress", "creator": "team", "assignee": "team",
            "branch": "legacy", "base_branch": "main", "scope": None, "lifecycle_generation": 1,
        }), encoding="utf-8")
        (archived / "task.json").write_text(json.dumps({"id": "old-task"}), encoding="utf-8")
        (sibling / ".trellis/tasks/09-21-empty").mkdir()
        self.assertEqual(prepare_creation_inputs(self.repo, self.creation(), self.acquisition()).task_id, TASK_ID)
        (sibling / TASK_REF).mkdir()
        with self.assertRaisesRegex(LifecycleContractError, "task_identity_already_exists"):
            prepare_creation_inputs(self.repo, self.creation(), self.acquisition())

    def test_creation_checks_target_id_when_legacy_generation_is_invalid(self) -> None:
        sibling = Path(self.temporary.name) / "legacy"
        self.git("worktree", "add", "-b", "legacy", str(sibling))
        old = sibling / ".trellis/tasks/archive/2026-09/09-20-old/task.json"
        old.parent.mkdir(parents=True)
        old.write_text(json.dumps({"id": "old-task", "lifecycle_generation": "unknown"}), encoding="utf-8")
        self.assertEqual(prepare_creation_inputs(self.repo, self.creation(), self.acquisition()).task_id, TASK_ID)
        old.write_text(json.dumps({"id": TASK_ID, "lifecycle_generation": "unknown"}), encoding="utf-8")
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_creation_inputs(self.repo, self.creation(), self.acquisition())
        self.assertEqual(raised.exception.code, "task_identity_already_exists")

    def test_creation_ignores_unrelated_malformed_branch_artifact(self) -> None:
        sibling = Path(self.temporary.name) / "legacy"
        self.git("worktree", "add", "-b", "legacy", str(sibling))
        old = sibling / ".trellis/tasks/archive/2026-01/01-00-old/task.json"
        old.parent.mkdir(parents=True)
        old.write_text('{"id": ', encoding="utf-8")
        subprocess.run(["git", "add", ".trellis/tasks"], cwd=sibling, check=True)
        subprocess.run(["git", "commit", "-qm", "legacy artifact"], cwd=sibling, check=True)
        self.assertEqual(prepare_creation_inputs(self.repo, self.creation(), self.acquisition()).task_id, TASK_ID)

    def test_creation_rejects_target_ref_with_nonobject_branch_artifact(self) -> None:
        sibling = Path(self.temporary.name) / "legacy"
        self.git("worktree", "add", "-b", "legacy", str(sibling))
        old = sibling / ".trellis/tasks/archive/2026-01/01-00-old/task.json"
        old.parent.mkdir(parents=True)
        old.write_text("[]", encoding="utf-8")
        subprocess.run(["git", "add", ".trellis/tasks"], cwd=sibling, check=True)
        subprocess.run(["git", "commit", "-qm", "unrelated legacy artifact"], cwd=sibling, check=True)
        self.assertEqual(prepare_creation_inputs(self.repo, self.creation(), self.acquisition()).task_id, TASK_ID)
        target = sibling / TASK_REF / "task.json"
        target.parent.mkdir(parents=True)
        target.write_text("[]", encoding="utf-8")
        subprocess.run(["git", "add", ".trellis/tasks"], cwd=sibling, check=True)
        subprocess.run(["git", "commit", "-qm", "occupied target task ref"], cwd=sibling, check=True)
        self.git("worktree", "remove", str(sibling))
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_creation_inputs(self.repo, self.creation(), self.acquisition())
        self.assertEqual(raised.exception.code, "invalid_task_identity")

    def test_creation_ignores_unrelated_old_resource_ledger(self) -> None:
        resources = ResourceLedgerStore(inspect_repository(self.repo))
        path = resources.path_for(TaskLifecycleKey("old-task", 0))
        path.parent.mkdir(parents=True)
        path.write_text('{"schema_version":"old"}', encoding="utf-8")
        self.assertEqual(prepare_creation_inputs(self.repo, self.creation(), self.acquisition()).task_id, TASK_ID)
        target = resources.path_for(TaskLifecycleKey(TASK_ID, 0))
        target.parent.mkdir(parents=True)
        target.write_text('{"schema_version":"old"}', encoding="utf-8")
        with self.assertRaisesRegex(LifecycleContractError, "resource_ledger_conflict"):
            prepare_creation_inputs(self.repo, self.creation(), self.acquisition())

    def test_creation_rejects_identity_on_unregistered_local_branch(self) -> None:
        sibling = Path(self.temporary.name) / "prior-task"
        self.git("worktree", "add", "-b", "prior-task", str(sibling))
        archived = sibling / ".trellis/tasks/archive/2026-09/prior-task"
        archived.mkdir(parents=True)
        (archived / "task.json").write_text(
            json.dumps({"id": TASK_ID, "status": "completed", "lifecycle_generation": 0}), encoding="utf-8",
        )
        subprocess.run(["git", "add", ".trellis/tasks"], cwd=sibling, check=True)
        subprocess.run(["git", "commit", "-qm", "prior task"], cwd=sibling, check=True)
        self.git("worktree", "remove", str(sibling))
        self.assertIsNone(ResourceLedgerStore(inspect_repository(self.repo)).read(TaskLifecycleKey(TASK_ID, 0)))
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_creation_inputs(self.repo, self.creation(), self.acquisition())
        self.assertEqual(raised.exception.code, "task_identity_already_exists")

    def test_creation_rejects_identity_on_remote_tracking_branch(self) -> None:
        sibling = Path(self.temporary.name) / "prior-task"
        self.git("worktree", "add", "-b", "prior-task", str(sibling))
        task = sibling / ".trellis/tasks/09-25-prior-task"
        task.mkdir(parents=True)
        (task / "task.json").write_text(
            json.dumps({"id": TASK_ID, "status": "in_progress", "lifecycle_generation": 0}), encoding="utf-8",
        )
        subprocess.run(["git", "add", ".trellis/tasks"], cwd=sibling, check=True)
        subprocess.run(["git", "commit", "-qm", "prior task"], cwd=sibling, check=True)
        prior_head = self.git("rev-parse", "prior-task")
        self.git("worktree", "remove", str(sibling))
        self.git("update-ref", "refs/remotes/origin/prior-task", prior_head)
        with self.assertRaises(LifecycleContractError) as raised:
            prepare_creation_inputs(self.repo, self.creation(), self.acquisition())
        self.assertEqual(raised.exception.code, "task_identity_already_exists")

    def test_recovery_rejects_branch_ledger_disagreement(self) -> None:
        plan = self.acquisition("provision_linked_worktree")
        inputs = prepare_creation_inputs(self.repo, self.creation(), plan)
        acquired = acquire_checkout(plan)
        task = acquired.checkout.path / TASK_REF
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps(self.task_metadata("planning", inputs.reviewed_source)), encoding="utf-8")
        self.git("branch", "unrelated-branch")
        repository = inspect_repository(self.repo)
        key = TaskLifecycleKey(TASK_ID, 0)
        binding = BranchBindingStore(repository).establish(key, "codex/new-task")
        ResourceLedgerStore(repository).establish_current(
            key, binding_revision=0,
            branch_name="unrelated-branch", branch_ownership=acquired.branch_ownership,
            worktree_ownership=acquired.worktree_ownership,
        )
        with self.assertRaises(LifecycleContractError) as raised:
            recover_created_control_state(
                inputs, acquired, expected_result_id=inputs.result_id,
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
            json.dumps(self.task_metadata("planning", inputs.reviewed_source)), encoding="utf-8",
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
            inputs, acquired, expected_result_id=inputs.result_id,
        )
        self.assertEqual(recovered, binding)
        self.assertEqual(ResourceLedgerStore(inspect_repository(self.repo)).read(TaskLifecycleKey(TASK_ID, 0)), ledger)
        wrong_owner = "guru_owned" if acquired.branch_ownership == "caller_owned" else "caller_owned"
        with self.assertRaises(LifecycleContractError) as raised:
            recover_created_control_state(
                inputs, replace(acquired, branch_ownership=wrong_owner),
                expected_result_id=inputs.result_id,
            )
        self.assertEqual(raised.exception.code, "creation_acquisition_mismatch")
        with self.assertRaises(LifecycleContractError) as raised:
            establish_created_control_state(inputs, acquired)
        self.assertEqual(raised.exception.code, "creation_control_state_exists")
        with self.assertRaises(LifecycleContractError):
            recover_created_control_state(inputs, acquired, expected_result_id="task-created:other")
        data = json.loads((task / "task.json").read_text())
        data["source"] = {"kind": "no_issue"} if inputs.reviewed_source["kind"] == "issue" else {
            "kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454, "disposition": "exact_source",
        }
        (task / "task.json").write_text(json.dumps(data))
        with self.assertRaises(LifecycleContractError) as raised:
            recover_created_control_state(inputs, acquired, expected_result_id=inputs.result_id)
        self.assertEqual(raised.exception.code, "creation_identity_mismatch")
        self.assertEqual(ResourceLedgerStore(inspect_repository(self.repo)).read(TaskLifecycleKey(TASK_ID, 0)), ledger)

    def test_new_creation_rejects_primary_adoption_before_mutation(self) -> None:
        self.git("switch", "-c", "codex/new-task")
        before = (self.git("symbolic-ref", "HEAD"), self.git("rev-parse", "HEAD"),
                  self.git("status", "--porcelain"), self.git("worktree", "list", "--porcelain"))
        with self.assertRaises(LifecycleContractError) as caught:
            prepare_creation_inputs(self.repo, self.creation(), self.acquisition("adopt_invocation_checkout"))
        self.assertEqual(caught.exception.code, "primary_checkout_requires_isolation")
        self.assertEqual(before, (self.git("symbolic-ref", "HEAD"), self.git("rev-parse", "HEAD"),
                                 self.git("status", "--porcelain"), self.git("worktree", "list", "--porcelain")))
        self.assertFalse((self.repo / TASK_REF).exists())
        repository = inspect_repository(self.repo)
        key = TaskLifecycleKey(TASK_ID, 0)
        self.assertIsNone(BranchBindingStore(repository).read(key))
        self.assertIsNone(ResourceLedgerStore(repository).read(key))

    def test_existing_primary_created_result_remains_recoverable(self) -> None:
        from runtime.task_lifecycle.composition import CreationInputs

        self.git("switch", "-c", "codex/new-task")
        plan = self.acquisition("adopt_invocation_checkout")
        data = self.creation()
        inputs = CreationInputs(
            TASK_ID, TASK_REF, data["source_profile"], data["reviewed_source"],
            data["accepted_scope_identity"], data["delivery_target"], "refs/heads/main", self.head, plan,
        )
        acquired = acquire_checkout(plan)
        task = self.repo / TASK_REF
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps(self.task_metadata("planning")), encoding="utf-8")
        binding = establish_created_control_state(inputs, acquired)
        before = (self.git("status", "--porcelain"), (task / "task.json").read_bytes())
        self.assertEqual(recover_created_control_state(inputs, acquired, expected_result_id=inputs.result_id), binding)
        self.assertEqual(before, (self.git("status", "--porcelain"), (task / "task.json").read_bytes()))

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
        plan = self.acquisition()
        inputs = prepare_creation_inputs(self.repo, self.creation(), plan)
        acquired = acquire_checkout(plan)
        task = acquired.checkout.path / TASK_REF
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps(self.task_metadata("planning", inputs.reviewed_source)), encoding="utf-8")
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

            def record_exists(self, path):
                return False

            def write_record(self, path, data, root):
                self.writes += 1
                raise OSError("session store unavailable")

        absent = SessionPort(None)
        explicit = bind_created_session(absent, inputs, acquired)
        self.assertEqual(explicit.status, "explicit_task_mode")
        self.assertEqual(absent.writes, 0)
        failing = SessionPort("codex-test")
        failed = bind_created_session(failing, inputs, acquired)
        self.assertEqual(failed.status, "session_write_failed")
        self.assertEqual(failing.writes, 1)
        self.assertEqual(BranchBindingStore(inspect_repository(self.repo)).read(TaskLifecycleKey(TASK_ID, 0)), binding)
        self.assertIsNotNone(ResourceLedgerStore(inspect_repository(self.repo)).read(TaskLifecycleKey(TASK_ID, 0)))


if __name__ == "__main__":
    unittest.main()
