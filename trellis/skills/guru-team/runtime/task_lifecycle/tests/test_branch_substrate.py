from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from runtime.task_lifecycle.branch_resolution import (
    OwnershipCurrent,
    establish_branch_binding,
    recover_established_branch_binding,
    resolve_establishment,
)
from runtime.task_lifecycle.branch_store import (
    BranchBinding,
    BranchBindingStore,
    TaskLifecycleKey,
)
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import capture_checkout_state, inspect_repository
from runtime.task_lifecycle.rebind import execute_rebind, prepare_rebind, recover_rebind


TASK_ID = "454-task-lifecycle-state-model"
TASK_REF = ".trellis/tasks/09-20-454-task-lifecycle-state-model"
GENERATION = 2


class GitFixture:
    def __init__(self, root: Path, name: str = "repo") -> None:
        self.repo = root / name
        self.repo.mkdir(parents=True)
        self.git("init", "-b", "main")
        self.git("config", "user.email", "tests@example.com")
        self.git("config", "user.name", "Branch Substrate Tests")
        task = self.repo / TASK_REF
        task.mkdir(parents=True)
        (task / "task.json").write_text(
            json.dumps(
                {
                    "id": TASK_ID,
                    "name": task.name,
                    "status": "in_progress",
                    "lifecycle_generation": GENERATION,
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        (self.repo / "tracked.txt").write_text("base\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "fixture")

    def git(
        self,
        *args: str,
        cwd: Path | None = None,
        check: bool = True,
        input_text: str | None = None,
    ) -> str:
        completed = subprocess.run(
            ["git", *args],
            cwd=cwd or self.repo,
            check=False,
            input=input_text,
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

    def branch(self, name: str, commit: str | None = None) -> None:
        self.git("branch", name, commit or self.head)

    def linked(self, root: Path, branch: str) -> Path:
        path = root / branch.replace("/", "-")
        self.git("worktree", "add", str(path), branch)
        return path


class InMemoryOwnershipPort:
    def __init__(self) -> None:
        self.current: dict[TaskLifecycleKey, OwnershipCurrent] = {}
        self.ledger_revision = 0
        self.unresolved_branches: set[str] = set()
        self.projections: list[dict[str, object]] = []
        self.rebind_calls = 0

    def read_current(self, key: TaskLifecycleKey) -> OwnershipCurrent | None:
        return self.current.get(key)

    def snapshot(self, key: TaskLifecycleKey):
        return copy.deepcopy(
            (
                self.current.get(key),
                self.ledger_revision,
                self.unresolved_branches,
                self.projections,
                self.rebind_calls,
            )
        )

    def restore(self, key: TaskLifecycleKey, snapshot) -> None:
        current, revision, unresolved, projections, rebind_calls = copy.deepcopy(snapshot)
        if current is None:
            self.current.pop(key, None)
        else:
            self.current[key] = current
        self.ledger_revision = revision
        self.unresolved_branches = unresolved
        self.projections = projections
        self.rebind_calls = rebind_calls

    def establish_current(
        self,
        key: TaskLifecycleKey,
        *,
        binding_revision: int,
        branch_name: str,
        branch_ownership: str,
        worktree_ownership: str,
    ) -> OwnershipCurrent:
        if key in self.current:
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "ownership",
                "Use the existing current ownership record.",
            )
        current = OwnershipCurrent(
            key.task_id,
            key.lifecycle_generation,
            binding_revision,
            branch_name,
        )
        self.current[key] = current
        self.ledger_revision += 1
        self.projections.append(
            {
                "action": "establish",
                "branch_ownership": branch_ownership,
                "worktree_ownership": worktree_ownership,
            }
        )
        return current

    def rebind_current(
        self,
        key: TaskLifecycleKey,
        *,
        expected_revision: int,
        source_branch_name: str,
        target_branch_name: str,
        expected_cleanup_head: str,
        target_branch_ownership: str,
        target_worktree_ownership: str | None,
        worktree_reassociated: bool,
    ) -> OwnershipCurrent:
        current = self.current.get(key)
        if (
            current is None
            or current.binding_revision != expected_revision
            or current.branch_name != source_branch_name
        ):
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "ownership",
                "Repeat rebind against the current ownership revision.",
            )
        successor = OwnershipCurrent(
            key.task_id,
            key.lifecycle_generation,
            expected_revision + 1,
            target_branch_name,
        )
        self.current[key] = successor
        self.ledger_revision += 1
        self.rebind_calls += 1
        self.projections.append(
            {
                "action": "rebind",
                "expected_cleanup_head": expected_cleanup_head,
                "target_branch_ownership": target_branch_ownership,
                "target_worktree_ownership": target_worktree_ownership,
                "worktree_reassociated": worktree_reassociated,
            }
        )
        return successor

    def branch_has_unresolved_incarnation(
        self,
        branch_name: str,
        *,
        key: TaskLifecycleKey,
        allowed_current_revision: int | None,
    ) -> bool:
        if branch_name not in self.unresolved_branches:
            return False
        current = self.current.get(key)
        return not (
            current is not None
            and current.branch_name == branch_name
            and current.binding_revision == allowed_current_revision
        )


class BranchSubstrateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.fixture = GitFixture(self.root)
        self.repository = inspect_repository(self.fixture.repo)
        self.store = BranchBindingStore(self.repository)
        self.ownership = InMemoryOwnershipPort()
        self.key = TaskLifecycleKey(TASK_ID, GENERATION)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def establish_control(self, branch: str = "main", revision: int = 0) -> None:
        self.store.establish(self.key, branch, binding_revision=revision)
        self.ownership.establish_current(
            self.key,
            binding_revision=revision,
            branch_name=branch,
            branch_ownership="caller_owned",
            worktree_ownership="not_applicable",
        )

    def test_binding_store_uses_five_fields_revision_zero_and_strict_increment(self) -> None:
        initial = self.store.establish(self.key, "main")
        self.assertEqual(initial.binding_revision, 0)
        self.assertEqual(
            set(json.loads(self.store.path_for(self.key).read_text(encoding="utf-8"))),
            {
                "schema_version",
                "task_id",
                "lifecycle_generation",
                "binding_revision",
                "branch_name",
            },
        )
        successor = self.store.advance(
            self.key,
            expected_revision=0,
            branch_name="topic",
        )
        self.assertEqual((successor.binding_revision, successor.branch_name), (1, "topic"))
        with self.assertRaisesRegex(LifecycleContractError, "branch_binding_revision_conflict"):
            self.store.advance(self.key, expected_revision=0, branch_name="other")
        with self.assertRaisesRegex(LifecycleContractError, "branch_binding_unchanged"):
            self.store.advance(self.key, expected_revision=1, branch_name="topic")

    def test_runtime_branch_name_matches_closed_schema_domain(self) -> None:
        for branch_name in [
            "refs/heads/topic",
            "guru-task-lifecycle/task-a",
            "HEAD",
            *[f"bad{chr(codepoint)}name" for codepoint in (*range(32), 127)],
        ]:
            with self.subTest(branch_name=branch_name):
                with self.assertRaises(LifecycleContractError):
                    BranchBinding(TASK_ID, GENERATION, 0, branch_name)

    def test_establishment_recovers_all_four_binding_ownership_quadrants(self) -> None:
        for quadrant in ("both", "binding_only", "ownership_only", "neither"):
            with self.subTest(quadrant=quadrant):
                fixture = GitFixture(self.root, f"repo-{quadrant}")
                repository = inspect_repository(fixture.repo)
                store = BranchBindingStore(repository)
                ownership = InMemoryOwnershipPort()
                key = TaskLifecycleKey(TASK_ID, GENERATION)
                revision = 3 if quadrant != "neither" else 0
                if quadrant in {"both", "binding_only"}:
                    store.establish(key, "main", binding_revision=revision)
                if quadrant in {"both", "ownership_only"}:
                    ownership.establish_current(
                        key,
                        binding_revision=revision,
                        branch_name="main",
                        branch_ownership="caller_owned",
                        worktree_ownership="not_applicable",
                    )

                result = establish_branch_binding(
                    repository,
                    store,
                    ownership,
                    key=key,
                    task_ref=TASK_REF,
                    expected_status="in_progress",
                )
                expected_kind = "already_established" if quadrant == "both" else "binding_established"
                self.assertEqual(result.kind, expected_kind)
                self.assertEqual(result.binding.binding_revision, revision)
                self.assertEqual(result.ownership.binding_revision, revision)
                if quadrant in {"binding_only", "neither"}:
                    self.assertEqual(
                        ownership.projections[-1],
                        {
                            "action": "establish",
                            "branch_ownership": "caller_owned",
                            "worktree_ownership": "not_applicable",
                        },
                    )

    def test_establishment_candidate_cardinality_is_closed(self) -> None:
        unique = resolve_establishment(
            self.repository,
            self.store,
            self.ownership,
            key=self.key,
            task_ref=TASK_REF,
            expected_status="in_progress",
        )
        self.assertEqual((unique.kind, len(unique.valid_candidates)), ("candidate_resolved", 1))

        zero = resolve_establishment(
            self.repository,
            self.store,
            self.ownership,
            key=self.key,
            task_ref=TASK_REF,
            expected_status="completed",
        )
        self.assertEqual((zero.kind, zero.reason_code), ("selection_required", "zero_validated_candidates"))

        self.fixture.branch("second-candidate")
        multiple = resolve_establishment(
            self.repository,
            self.store,
            self.ownership,
            key=self.key,
            task_ref=TASK_REF,
            expected_status="in_progress",
        )
        self.assertEqual(
            (multiple.kind, multiple.reason_code, len(multiple.valid_candidates)),
            ("selection_required", "multiple_validated_candidates", 2),
        )

    def test_establishment_output_loss_recovery_is_read_only(self) -> None:
        result = establish_branch_binding(
            self.repository,
            self.store,
            self.ownership,
            key=self.key,
            task_ref=TASK_REF,
            expected_status="in_progress",
        )
        ledger_revision = self.ownership.ledger_revision
        recovered = recover_established_branch_binding(
            self.repository,
            self.store,
            self.ownership,
            key=self.key,
            task_ref=TASK_REF,
            expected_status="in_progress",
            expected_revision=0,
            expected_branch_name="main",
        )
        self.assertEqual(recovered.binding, result.binding)
        self.assertEqual(self.ownership.ledger_revision, ledger_revision)

    def test_local_branch_candidate_requires_checkout_acquisition_before_establishment(self) -> None:
        self.fixture.branch("local-only")
        self.store.establish(self.key, "local-only")
        result = establish_branch_binding(
            self.repository,
            self.store,
            self.ownership,
            key=self.key,
            task_ref=TASK_REF,
            expected_status="in_progress",
        )
        self.assertEqual(
            (result.kind, result.reason_code, result.selected),
            ("selection_required", "checkout_acquisition_required", None),
        )
        self.assertIsNone(self.ownership.read_current(self.key))

    def test_dirty_same_checkout_rebind_preserves_head_index_and_worktree_bytes(self) -> None:
        self.establish_control()
        (self.fixture.repo / "staged.bin").write_bytes(b"\x00staged\xff")
        self.fixture.git("add", "staged.bin")
        (self.fixture.repo / "tracked.txt").write_bytes(b"base\ndirty\x00bytes\n")
        (self.fixture.repo / "untracked.bin").write_bytes(b"\x00untracked\xfe")
        before = capture_checkout_state(self.fixture.repo)
        before_files = {
            name: (self.fixture.repo / name).read_bytes()
            for name in ("staged.bin", "tracked.txt", "untracked.bin")
        }

        plan = prepare_rebind(
            self.repository,
            self.store,
            self.ownership,
            route="same_checkout_new_ref",
            key=self.key,
            task_ref=TASK_REF,
            expected_status="in_progress",
            current_checkout=self.fixture.repo,
            target_branch_name="topic-dirty",
        )
        result = execute_rebind(self.repository, self.store, self.ownership, plan)
        after = capture_checkout_state(self.fixture.repo)

        self.assertEqual((result.binding.binding_revision, result.binding.branch_name), (1, "topic-dirty"))
        self.assertEqual(before.head, after.head)
        self.assertEqual(before.index_sha256, after.index_sha256)
        self.assertEqual(before.worktree_sha256, after.worktree_sha256)
        self.assertEqual(before.status_sha256, after.status_sha256)
        self.assertEqual(
            before_files,
            {name: (self.fixture.repo / name).read_bytes() for name in before_files},
        )

    def test_existing_target_requires_clean_exact_artifact_and_compatible_history(self) -> None:
        self.establish_control()
        self.fixture.branch("target")
        target = self.fixture.linked(self.root, "target")
        plan = prepare_rebind(
            self.repository,
            self.store,
            self.ownership,
            route="existing_target",
            key=self.key,
            task_ref=TASK_REF,
            expected_status="in_progress",
            current_checkout=self.fixture.repo,
            target_branch_name="target",
        )
        result = execute_rebind(self.repository, self.store, self.ownership, plan)
        self.assertEqual(result.checkout_path, target.resolve())
        self.assertEqual(self.fixture.git("branch", "--show-current"), "main")
        self.assertEqual(self.fixture.git("branch", "--show-current", cwd=target), "target")
        self.assertEqual(
            self.ownership.projections[-1],
            {
                "action": "rebind",
                "expected_cleanup_head": self.fixture.head,
                "target_branch_ownership": "caller_owned",
                "target_worktree_ownership": "caller_owned",
                "worktree_reassociated": False,
            },
        )

        other = GitFixture(self.root, "repo-artifact-mismatch")
        repository = inspect_repository(other.repo)
        store = BranchBindingStore(repository)
        ownership = InMemoryOwnershipPort()
        key = TaskLifecycleKey(TASK_ID, GENERATION)
        store.establish(key, "main")
        ownership.establish_current(
            key,
            binding_revision=0,
            branch_name="main",
            branch_ownership="caller_owned",
            worktree_ownership="not_applicable",
        )
        other.branch("wrong-target")
        wrong_target = other.linked(self.root, "wrong-target")
        task_json = wrong_target / TASK_REF / "task.json"
        payload = json.loads(task_json.read_text(encoding="utf-8"))
        payload["id"] = "another-task"
        task_json.write_text(json.dumps(payload) + "\n", encoding="utf-8")
        other.git("add", TASK_REF, cwd=wrong_target)
        other.git("commit", "-m", "wrong task", cwd=wrong_target)
        with self.assertRaisesRegex(LifecycleContractError, "task_artifact_mismatch"):
            prepare_rebind(
                repository,
                store,
                ownership,
                route="existing_target",
                key=key,
                task_ref=TASK_REF,
                expected_status="in_progress",
                current_checkout=other.repo,
                target_branch_name="wrong-target",
            )

    def test_existing_target_rejects_unrelated_history_with_named_reconcile_stop(self) -> None:
        self.establish_control()
        tree = self.fixture.git("rev-parse", "HEAD^{tree}")
        divergent = self.fixture.git("commit-tree", tree, input_text="divergent\n")
        self.fixture.branch("divergent", divergent)
        self.fixture.linked(self.root, "divergent")
        with self.assertRaisesRegex(LifecycleContractError, "rebind_reconcile_required"):
            prepare_rebind(
                self.repository,
                self.store,
                self.ownership,
                route="existing_target",
                key=self.key,
                task_ref=TASK_REF,
                expected_status="in_progress",
                current_checkout=self.fixture.repo,
                target_branch_name="divergent",
            )

    def test_rebind_failure_restores_exact_control_and_checkout_pre_state(self) -> None:
        self.establish_control()
        (self.fixture.repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")
        plan = prepare_rebind(
            self.repository,
            self.store,
            self.ownership,
            route="same_checkout_new_ref",
            key=self.key,
            task_ref=TASK_REF,
            expected_status="in_progress",
            current_checkout=self.fixture.repo,
            target_branch_name="rollback-target",
        )
        before_checkout = capture_checkout_state(self.fixture.repo)
        before_ownership = self.ownership.snapshot(self.key)

        def fail_after_mutation(_result) -> None:
            raise RuntimeError("lost consumer")

        with self.assertRaisesRegex(RuntimeError, "lost consumer"):
            execute_rebind(
                self.repository,
                self.store,
                self.ownership,
                plan,
                post_mutation=fail_after_mutation,
            )
        self.assertEqual(capture_checkout_state(self.fixture.repo), before_checkout)
        self.assertEqual(self.store.read(self.key).branch_name, "main")
        self.assertIsNone(
            self.fixture.git(
                "rev-parse",
                "--verify",
                "--quiet",
                "refs/heads/rollback-target",
                check=False,
            )
            or None
        )
        self.assertEqual(self.ownership.snapshot(self.key), before_ownership)

    def test_rebind_output_loss_recovery_does_not_increment_twice(self) -> None:
        self.establish_control()
        plan = prepare_rebind(
            self.repository,
            self.store,
            self.ownership,
            route="same_checkout_new_ref",
            key=self.key,
            task_ref=TASK_REF,
            expected_status="in_progress",
            current_checkout=self.fixture.repo,
            target_branch_name="recovered-target",
        )
        executed = execute_rebind(self.repository, self.store, self.ownership, plan)
        first = recover_rebind(self.repository, self.store, self.ownership, plan)
        second = recover_rebind(self.repository, self.store, self.ownership, plan)
        self.assertEqual(first.binding, executed.binding)
        self.assertEqual(second.binding.binding_revision, 1)
        self.assertTrue(first.recovered)
        self.assertEqual(self.ownership.rebind_calls, 1)

    def test_rebind_rejects_same_ref_with_unresolved_resource_incarnation(self) -> None:
        self.establish_control()
        self.ownership.unresolved_branches.add("blocked-target")
        with self.assertRaisesRegex(LifecycleContractError, "unresolved_resource_incarnation"):
            prepare_rebind(
                self.repository,
                self.store,
                self.ownership,
                route="same_checkout_new_ref",
                key=self.key,
                task_ref=TASK_REF,
                expected_status="in_progress",
                current_checkout=self.fixture.repo,
                target_branch_name="blocked-target",
            )


if __name__ == "__main__":
    unittest.main()
