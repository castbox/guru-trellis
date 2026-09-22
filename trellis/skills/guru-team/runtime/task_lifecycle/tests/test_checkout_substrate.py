from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from runtime.task_lifecycle.checkout_acquisition import (
    CheckoutAcquisitionPlan,
    adopt_invocation_checkout,
    provision_linked_worktree,
    recover_checkout_acquisition,
)
from runtime.task_lifecycle.checkout_resolution import (
    CheckoutRequest,
    canonical_head_ref,
    discover_validate_classify,
    select_or_specify,
)
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import inspect_repository, list_worktree_registrations


TASK_ID = "454-task-lifecycle-state-model"
TASK_REF = ".trellis/tasks/09-20-454-task-lifecycle-state-model"


class GitFixture:
    def __init__(self, root: Path, name: str = "repo") -> None:
        self.repo = root / name
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.email", "tests@example.com")
        self.git("config", "user.name", "Checkout Tests")
        task = self.repo / TASK_REF
        task.mkdir(parents=True)
        (task / "task.json").write_text(
            json.dumps(
                {
                    "id": TASK_ID,
                    "name": task.name,
                    "status": "in_progress",
                    "lifecycle_generation": 0,
                }
            ),
            encoding="utf-8",
        )
        (self.repo / "README.md").write_text("fixture\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "fixture")

    def git(self, *args: str, cwd: Path | None = None, check: bool = True) -> str:
        completed = subprocess.run(
            ["git", *args],
            cwd=cwd or self.repo,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if check and completed.returncode != 0:
            raise AssertionError(f"git {' '.join(args)} failed: {completed.stderr}")
        return completed.stdout.strip()

    @property
    def head(self) -> str:
        return self.git("rev-parse", "HEAD")

    def branch(self, name: str) -> None:
        self.git("branch", name, self.head)

    def linked(self, root: Path, branch: str, *, force: bool = False) -> Path:
        path = root / branch.replace("/", "-")
        args = ["worktree", "add"]
        if force:
            args.append("--force")
        args.extend([str(path), branch])
        self.git(*args)
        return path


class CheckoutSubstrateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.fixture = GitFixture(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def request(
        self,
        branch: str,
        *,
        head: str | None = None,
        clean: bool = True,
        forbidden: tuple[str, ...] = (),
        artifact_expectation: str = "required",
    ) -> CheckoutRequest:
        return CheckoutRequest(
            repository=inspect_repository(self.fixture.repo),
            task_id=TASK_ID,
            task_ref=TASK_REF,
            lifecycle_generation=0,
            branch_ref=branch,
            expected_status="in_progress",
            expected_head=head,
            clean_required=clean,
            forbidden_branch_refs=forbidden,
            task_artifact_expectation=artifact_expectation,
        )

    def plan(
        self,
        route: str,
        branch: str,
        *,
        disposition: str | None = None,
        invocation: Path | None = None,
        target: Path | None = None,
        head: str | None = None,
        artifact_expectation: str = "required",
        transaction_id: str = "checkout-transaction:1",
        result_id: str = "checkout-result:1",
    ) -> CheckoutAcquisitionPlan:
        return CheckoutAcquisitionPlan(
            route=route,
            repository_context=self.fixture.repo,
            task_id=TASK_ID,
            task_ref=TASK_REF,
            lifecycle_generation=0,
            branch_ref=branch,
            expected_status="in_progress",
            decision_head=head or self.fixture.head,
            transaction_id=transaction_id,
            result_id=result_id,
            provision_disposition=disposition,
            invocation_checkout=invocation,
            target_path=target,
            task_artifact_expectation=artifact_expectation,
        )

    def remove_task_artifact(self, checkout: Path) -> None:
        task = checkout / TASK_REF
        for path in sorted(task.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        task.rmdir()

    def test_primary_and_linked_invocation_checkouts_are_adopted_as_caller_owned(self) -> None:
        self.fixture.git("checkout", "-b", "task-primary")
        primary = adopt_invocation_checkout(
            self.plan("adopt_invocation_checkout", "task-primary", invocation=self.fixture.repo)
        )
        self.assertEqual((primary.checkout.topology, primary.branch_ownership), ("primary", "caller_owned"))
        self.assertEqual(primary.worktree_ownership, "not_applicable")

        self.fixture.git("checkout", "main")
        self.fixture.branch("task-linked")
        linked_path = self.fixture.linked(self.root, "task-linked")
        linked = adopt_invocation_checkout(
            self.plan("adopt_invocation_checkout", "task-linked", invocation=linked_path)
        )
        self.assertEqual((linked.checkout.topology, linked.branch_ownership), ("linked", "caller_owned"))
        self.assertEqual(linked.worktree_ownership, "caller_owned")

    def test_new_existing_branch_and_exact_checkout_provision_routes(self) -> None:
        new_target = self.root / "new-target"
        created = provision_linked_worktree(
            self.plan(
                "provision_linked_worktree",
                "task-new",
                disposition="new_branch",
                target=new_target,
            )
        )
        self.assertEqual((created.branch_ownership, created.worktree_ownership), ("guru_owned", "guru_owned"))
        self.assertEqual(created.action, "created_branch_and_worktree")

        self.fixture.branch("task-existing")
        existing_target = self.root / "existing-target"
        existing = provision_linked_worktree(
            self.plan(
                "provision_linked_worktree",
                "task-existing",
                disposition="existing_branch",
                target=existing_target,
            )
        )
        self.assertEqual((existing.branch_ownership, existing.worktree_ownership), ("caller_owned", "guru_owned"))

        self.fixture.branch("task-reuse")
        reuse_path = self.fixture.linked(self.root, "task-reuse")
        reused = provision_linked_worktree(
            self.plan(
                "provision_linked_worktree",
                "task-reuse",
                disposition="existing_checkout",
                target=reuse_path,
            )
        )
        self.assertEqual((reused.branch_ownership, reused.worktree_ownership), ("caller_owned", "caller_owned"))
        self.assertEqual(reused.action, "reused_exact_checkout")
        with self.assertRaisesRegex(LifecycleContractError, "provision_pre_state_changed"):
            provision_linked_worktree(
                self.plan(
                    "provision_linked_worktree",
                    "task-reuse",
                    disposition="existing_checkout",
                    target=self.root / "different-reviewed-target",
                )
            )

    def test_existing_primary_checkout_must_use_adopt_route(self) -> None:
        self.fixture.git("checkout", "-b", "task-primary-provision")
        with self.assertRaisesRegex(LifecycleContractError, "primary_checkout_requires_adoption"):
            provision_linked_worktree(
                self.plan(
                    "provision_linked_worktree",
                    "task-primary-provision",
                    disposition="existing_checkout",
                    target=self.fixture.repo,
                )
            )

    def test_pre_task_adopt_and_provision_require_the_task_artifact_to_be_absent(self) -> None:
        self.fixture.git("checkout", "-b", "task-prebuilt")
        self.remove_task_artifact(self.fixture.repo)
        self.fixture.git("add", "-A")
        self.fixture.git("commit", "-m", "pre-task checkout")
        adopted = adopt_invocation_checkout(
            self.plan(
                "adopt_invocation_checkout",
                "task-prebuilt",
                invocation=self.fixture.repo,
                artifact_expectation="absent",
            )
        )
        self.assertEqual(adopted.checkout.path, self.fixture.repo.resolve())

        target = self.root / "pre-task-provision"
        provisioned = provision_linked_worktree(
            self.plan(
                "provision_linked_worktree",
                "task-pre-task-provision",
                disposition="new_branch",
                target=target,
                head=self.fixture.head,
                artifact_expectation="absent",
            )
        )
        self.assertEqual(provisioned.checkout.path, target.resolve())

        with self.assertRaisesRegex(LifecycleContractError, "task_artifact_missing"):
            adopt_invocation_checkout(
                self.plan(
                    "adopt_invocation_checkout",
                    "task-prebuilt",
                    invocation=self.fixture.repo,
                    artifact_expectation="required",
                )
            )

    def test_pre_task_candidate_rejects_another_active_task_authority(self) -> None:
        self.fixture.git("checkout", "-b", "task-prebuilt-conflict")
        self.remove_task_artifact(self.fixture.repo)
        other = self.fixture.repo / ".trellis/tasks/09-21-other-active"
        other.mkdir(parents=True)
        (other / "task.json").write_text(
            json.dumps(
                {
                    "id": "other-active-task",
                    "name": other.name,
                    "status": "in_progress",
                    "lifecycle_generation": 0,
                }
            ),
            encoding="utf-8",
        )
        self.fixture.git("add", "-A")
        self.fixture.git("commit", "-m", "other active task authority")

        resolution = discover_validate_classify(
            self.request(
                "task-prebuilt-conflict",
                head=self.fixture.head,
                artifact_expectation="absent",
            )
        )
        self.assertEqual(
            (resolution.kind, resolution.reason_code),
            ("authority_conflict", "active_task_authority_conflict"),
        )
        with self.assertRaisesRegex(LifecycleContractError, "active_task_authority_conflict"):
            adopt_invocation_checkout(
                self.plan(
                    "adopt_invocation_checkout",
                    "task-prebuilt-conflict",
                    invocation=self.fixture.repo,
                    artifact_expectation="absent",
                )
            )

    def test_transaction_and_result_ids_match_shared_identifier_grammar(self) -> None:
        self.fixture.git("checkout", "-b", "task-identifiers")
        accepted = adopt_invocation_checkout(
            self.plan(
                "adopt_invocation_checkout",
                "task-identifiers",
                invocation=self.fixture.repo,
                transaction_id="A.b_c:d-1",
                result_id="result:1.2_test-value",
            )
        )
        self.assertEqual(accepted.transaction_id, "A.b_c:d-1")
        self.assertEqual(accepted.result_id, "result:1.2_test-value")

        for field, value in [("transaction_id", "bad/id"), ("result_id", "@bad")]:
            overrides = {field: value}
            with self.subTest(field=field, value=value), self.assertRaisesRegex(
                LifecycleContractError,
                "invalid_transaction_identity",
            ):
                adopt_invocation_checkout(
                    self.plan(
                        "adopt_invocation_checkout",
                        "task-identifiers",
                        invocation=self.fixture.repo,
                        **overrides,
                    )
                )

    def test_wrong_repository_detached_dirty_and_head_drift_are_distinct(self) -> None:
        foreign = GitFixture(self.root, "foreign")
        foreign.git("checkout", "-b", "task-foreign")
        wrong = select_or_specify(self.request("task-foreign"), explicit_target=foreign.repo)
        self.assertEqual((wrong.kind, wrong.reason_code), ("authority_conflict", "wrong_repository"))

        detached = self.root / "detached"
        self.fixture.git("worktree", "add", "--detach", str(detached), self.fixture.head)
        detached_result = discover_validate_classify(self.request("task-detached", head=self.fixture.head))
        self.assertEqual(detached_result.kind, "selection_required")
        self.assertIn("detached_checkout", {row.reason_code for row in detached_result.candidates})

        self.fixture.branch("task-dirty")
        dirty = self.fixture.linked(self.root, "task-dirty")
        (dirty / "README.md").write_text("dirty\n", encoding="utf-8")
        dirty_result = discover_validate_classify(self.request("task-dirty", head=self.fixture.head))
        self.assertEqual(dirty_result.kind, "selection_required")
        self.assertIn("dirty_checkout", {row.reason_code for row in dirty_result.candidates})

        self.fixture.branch("task-drift")
        drift = self.fixture.linked(self.root, "task-drift")
        (drift / "drift.txt").write_text("drift\n", encoding="utf-8")
        self.fixture.git("add", "drift.txt", cwd=drift)
        self.fixture.git("commit", "-m", "drift", cwd=drift)
        drift_result = discover_validate_classify(self.request("task-drift", head="a" * 40))
        self.assertEqual((drift_result.kind, drift_result.reason_code), ("authority_conflict", "head_drift"))

    def test_delivery_base_and_reserved_refs_are_rejected_before_discovery(self) -> None:
        with self.assertRaisesRegex(LifecycleContractError, "delivery_or_base_branch_forbidden"):
            self.request("main", forbidden=("main", "develop"))
        for value in ["guru-task-lifecycle/task", "refs/heads/guru-task-lifecycle/task"]:
            with self.subTest(value=value), self.assertRaisesRegex(LifecycleContractError, "invalid_branch_ref"):
                canonical_head_ref(value)

    def test_zero_one_and_multiple_candidates_use_closed_classification(self) -> None:
        zero = discover_validate_classify(self.request("task-zero", head=self.fixture.head))
        self.assertEqual((zero.kind, zero.reason_code), ("selection_required", "zero_validated_candidates"))

        self.fixture.branch("task-one")
        self.fixture.linked(self.root, "task-one")
        one = discover_validate_classify(self.request("task-one", head=self.fixture.head))
        self.assertEqual((one.kind, one.selected.facts.branch_ref), ("checkout_resolved", "refs/heads/task-one"))

        second = self.root / "task-one-second"
        self.fixture.git("worktree", "add", "--force", str(second), "task-one")
        multiple = discover_validate_classify(self.request("task-one", head=self.fixture.head))
        self.assertEqual((multiple.kind, multiple.reason_code), ("selection_required", "multiple_validated_candidates"))

    def test_authority_conflict_cannot_be_downgraded_to_invalid_candidate(self) -> None:
        self.fixture.branch("task-conflict")
        path = self.fixture.linked(self.root, "task-conflict")
        metadata = path / TASK_REF / "task.json"
        payload = json.loads(metadata.read_text(encoding="utf-8"))
        payload["id"] = "another-task"
        metadata.write_text(json.dumps(payload), encoding="utf-8")
        self.fixture.git("add", str(metadata.relative_to(path)), cwd=path)
        self.fixture.git("commit", "-m", "conflicting task artifact", cwd=path)
        conflict = discover_validate_classify(self.request("task-conflict", head=self.fixture.head))
        self.assertEqual(conflict.kind, "authority_conflict")
        self.assertEqual(conflict.reason_code, "task_artifact_mismatch")

    def test_worktree_move_and_selected_candidate_revalidation_use_fresh_path(self) -> None:
        self.fixture.branch("task-move")
        old_path = self.fixture.linked(self.root, "task-move")
        initial = discover_validate_classify(self.request("task-move", head=self.fixture.head))
        self.assertEqual(initial.kind, "checkout_resolved")
        new_path = self.root / "moved-task"
        self.fixture.git("worktree", "move", str(old_path), str(new_path))
        refreshed = select_or_specify(
            self.request("task-move", head=self.fixture.head),
            selected_candidate_id=initial.selected.candidate_id,
        )
        self.assertEqual((refreshed.kind, refreshed.selected.facts.path), ("checkout_resolved", new_path.resolve()))

    def test_stale_selected_candidate_does_not_silently_switch_to_another_checkout(self) -> None:
        self.fixture.branch("task-stale")
        selected_path = self.fixture.linked(self.root, "task-stale")
        initial = discover_validate_classify(self.request("task-stale", head=self.fixture.head))
        self.assertEqual(initial.kind, "checkout_resolved")
        self.fixture.git("worktree", "remove", str(selected_path))
        replacement = self.root / "task-stale-replacement"
        self.fixture.git("worktree", "add", str(replacement), "task-stale")
        refreshed = select_or_specify(
            self.request("task-stale", head=self.fixture.head),
            selected_candidate_id=initial.selected.candidate_id,
        )
        self.assertEqual((refreshed.kind, refreshed.reason_code), ("selection_required", "selected_candidate_stale"))

    def test_adopt_does_not_bypass_multiple_candidate_selection(self) -> None:
        self.fixture.branch("task-ambiguous")
        first = self.fixture.linked(self.root, "task-ambiguous")
        second = self.root / "task-ambiguous-second"
        self.fixture.git("worktree", "add", "--force", str(second), "task-ambiguous")
        with self.assertRaisesRegex(LifecycleContractError, "multiple_validated_candidates"):
            adopt_invocation_checkout(
                self.plan("adopt_invocation_checkout", "task-ambiguous", invocation=first)
            )

    def test_explicit_target_is_revalidated_after_head_change(self) -> None:
        self.fixture.branch("task-explicit")
        path = self.fixture.linked(self.root, "task-explicit")
        reviewed_head = self.fixture.head
        initial = discover_validate_classify(self.request("task-explicit", head=reviewed_head))
        self.assertEqual(initial.kind, "checkout_resolved")
        (path / "change.txt").write_text("change\n", encoding="utf-8")
        self.fixture.git("add", "change.txt", cwd=path)
        self.fixture.git("commit", "-m", "advance", cwd=path)
        current = select_or_specify(self.request("task-explicit", head=reviewed_head), explicit_target=path)
        self.assertEqual((current.kind, current.reason_code), ("authority_conflict", "head_drift"))

    def test_output_loss_recovery_rematerializes_without_mutation(self) -> None:
        target = self.root / "recover-target"
        plan = self.plan(
            "provision_linked_worktree",
            "task-recover",
            disposition="new_branch",
            target=target,
        )
        created = provision_linked_worktree(plan)
        before = list_worktree_registrations(inspect_repository(self.fixture.repo))
        recovered = recover_checkout_acquisition(plan)
        after = list_worktree_registrations(inspect_repository(self.fixture.repo))
        self.assertEqual(before, after)
        self.assertEqual(recovered.checkout.path, created.checkout.path)
        self.assertEqual((recovered.branch_ownership, recovered.worktree_ownership), ("caller_owned", "caller_owned"))
        self.assertEqual(recovered.action, "rematerialized_unproven_resource_result")

    def test_recovery_never_infers_guru_ownership_for_replacement_resources(self) -> None:
        target = self.root / "replacement-target"
        plan = self.plan(
            "provision_linked_worktree",
            "task-replacement",
            disposition="new_branch",
            target=target,
        )
        provision_linked_worktree(plan)
        self.fixture.git("worktree", "remove", str(target))
        self.fixture.git("branch", "-D", "task-replacement")
        self.fixture.git("worktree", "add", "-b", "task-replacement", str(target), self.fixture.head)
        recovered = recover_checkout_acquisition(plan)
        self.assertEqual((recovered.branch_ownership, recovered.worktree_ownership), ("caller_owned", "caller_owned"))

    def test_failure_rolls_back_only_transaction_created_resources(self) -> None:
        target = self.root / "rollback-target"
        plan = self.plan(
            "provision_linked_worktree",
            "task-rollback",
            disposition="new_branch",
            target=target,
        )
        with self.assertRaisesRegex(RuntimeError, "downstream failed"):
            provision_linked_worktree(plan, post_acquire=lambda _: (_ for _ in ()).throw(RuntimeError("downstream failed")))
        self.assertFalse(target.exists())
        self.assertEqual(
            self.fixture.git("show-ref", "--verify", "--quiet", "refs/heads/task-rollback", check=False),
            "",
        )

    def test_new_checkout_runtime_has_zero_legacy_mapping_access(self) -> None:
        runtime = Path(__file__).resolve().parent.parent
        fragments = [
            "task_" + "workspace",
            "worktree_" + "path",
            "source_" + "checkout",
            ".trellis/" + "workspace",
        ]
        for name in ["git_facts.py", "checkout_resolution.py", "checkout_acquisition.py"]:
            content = (runtime / name).read_text(encoding="utf-8")
            for fragment in fragments:
                with self.subTest(name=name, fragment=fragment):
                    self.assertNotIn(fragment, content)


if __name__ == "__main__":
    unittest.main()
