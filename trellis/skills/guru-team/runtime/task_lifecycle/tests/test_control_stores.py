from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from runtime.task_lifecycle.branch_store import TaskLifecycleKey
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import RepositoryFacts
from runtime.task_lifecycle.resource_ledger import ResourceLedger, ResourceLedgerStore
from runtime.task_lifecycle.session_adapter import bind_session, resolve_session


TASK_A = "454-task-lifecycle-state-model"
TASK_B = "another-task"
BRANCH = "codex/454-task-lifecycle-state-model-c3-c7"
TARGET = "codex/454-task-lifecycle-state-model-c5"
HEAD = "a" * 40
FINISH_HEAD = "b" * 40


class FakeOfficialSessionPort:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.records: dict[Path, dict] = {}
        self.tasks: dict[tuple[str, int], str] = {
            (TASK_A, 0): ".trellis/tasks/09-20-454-task-lifecycle-state-model",
            (TASK_B, 0): ".trellis/tasks/09-21-another-task",
        }
        self.fail_write = False
        self.calls: list[str] = []

    def resolve_context_key(self, platform_input=None, platform=None):
        self.calls.append("resolve_context_key")
        return (platform_input or {}).get("context_key")

    def repository_facts(self, root):
        self.calls.append("repository_facts")
        return SimpleNamespace(common_dir=self.root / ".git")

    def session_path(self, root, key, facts):
        self.calls.append("session_path")
        return facts.common_dir / "trellis" / "sessions" / f"{key}.json"

    def record_exists(self, path):
        self.calls.append("record_exists")
        return path in self.records

    def read_record(self, path, root, facts):
        self.calls.append("read_record")
        payload = self.records[path]
        return SimpleNamespace(
            path=path,
            root=root,
            task_id=payload["task_id"],
            lifecycle_generation=payload["lifecycle_generation"],
            data=dict(payload),
        )

    def write_record(self, path, data, root):
        self.calls.append("write_record")
        if self.fail_write:
            raise ValueError("binding_write_failed")
        self.records[path] = dict(data)

    def resolve_task_identity(self, facts, task_id, lifecycle_generation):
        self.calls.append("resolve_task_identity")
        key = (task_id, lifecycle_generation)
        if key not in self.tasks:
            raise ValueError("stale_lifecycle_generation")
        return SimpleNamespace(task_ref=self.tasks[key])


class SessionAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.official = FakeOfficialSessionPort(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def bind(self, task_id=TASK_A, generation=0, context="session-a"):
        return bind_session(
            self.official,
            self.root,
            {"task_id": task_id, "lifecycle_generation": generation},
            platform_input={"context_key": context} if context else {},
        )

    def test_bind_delegates_exact_schema_two_record_and_fresh_task_ref(self) -> None:
        result = self.bind()
        self.assertEqual((result.status, result.task_ref), (
            "session_bound",
            ".trellis/tasks/09-20-454-task-lifecycle-state-model",
        ))
        self.assertEqual(
            next(iter(self.official.records.values())),
            {
                "schema_version": 2,
                "task_id": TASK_A,
                "lifecycle_generation": 0,
            },
        )
        self.assertEqual(
            self.official.calls,
            [
                "resolve_context_key",
                "repository_facts",
                "session_path",
                "resolve_task_identity",
                "write_record",
                "read_record",
            ],
        )

    def test_invalid_target_is_rejected_before_the_existing_record_is_replaced(self) -> None:
        self.assertEqual(self.bind().status, "session_bound")
        path = next(iter(self.official.records))
        before = dict(self.official.records[path])
        self.official.calls.clear()

        invalid = self.bind(TASK_A, generation=1)

        self.assertEqual(
            (invalid.status, invalid.reason_code),
            ("session_invalid", "official_session_target_invalid"),
        )
        self.assertEqual(self.official.records[path], before)
        self.assertEqual(
            self.official.calls,
            [
                "resolve_context_key",
                "repository_facts",
                "session_path",
                "resolve_task_identity",
            ],
        )

    def test_missing_context_key_uses_explicit_task_mode_without_store_access(self) -> None:
        result = self.bind(context=None)
        self.assertEqual((result.status, result.reason_code), (
            "explicit_task_mode",
            "context_key_unavailable",
        ))
        self.assertEqual(self.official.records, {})
        self.assertEqual(self.official.calls, ["resolve_context_key"])

    def test_write_failure_is_session_local_and_does_not_request_lifecycle_rollback(self) -> None:
        lifecycle_result = ["branch_binding_established"]
        self.official.fail_write = True
        result = self.bind()
        self.assertEqual(result.status, "session_write_failed")
        self.assertEqual(lifecycle_result, ["branch_binding_established"])
        self.assertEqual(self.official.records, {})

    def test_multi_session_switch_and_a_to_b_to_a_remain_isolated(self) -> None:
        self.assertEqual(self.bind(TASK_A, context="one").status, "session_bound")
        self.assertEqual(self.bind(TASK_A, context="two").status, "session_bound")
        self.assertEqual(self.bind(TASK_B, context="one").status, "session_bound")
        self.assertEqual(self.bind(TASK_A, context="one").status, "session_bound")

        one = resolve_session(
            self.official,
            self.root,
            platform_input={"context_key": "one"},
        )
        two = resolve_session(
            self.official,
            self.root,
            platform_input={"context_key": "two"},
        )
        self.assertEqual((one.lifecycle.task_id, two.lifecycle.task_id), (TASK_A, TASK_A))
        self.assertNotEqual(one.context_key, two.context_key)

    def test_generation_change_invalidates_old_record_and_task_ref_is_fresh(self) -> None:
        self.assertEqual(self.bind().status, "session_bound")
        self.official.tasks[(TASK_A, 0)] = ".trellis/tasks/09-24-renamed-task"
        moved = resolve_session(
            self.official,
            self.root,
            platform_input={"context_key": "session-a"},
        )
        self.assertEqual(moved.task_ref, ".trellis/tasks/09-24-renamed-task")

        del self.official.tasks[(TASK_A, 0)]
        self.official.tasks[(TASK_A, 1)] = ".trellis/tasks/09-24-renamed-task"
        stale = resolve_session(
            self.official,
            self.root,
            platform_input={"context_key": "session-a"},
        )
        self.assertEqual((stale.status, stale.reason_code), (
            "session_invalid",
            "official_session_record_invalid",
        ))

    def test_adapter_rejects_non_lifecycle_dto_fields_before_official_calls(self) -> None:
        with self.assertRaises(LifecycleContractError):
            bind_session(
                self.official,
                self.root,
                {
                    "task_id": TASK_A,
                    "lifecycle_generation": 0,
                    "task_ref": ".trellis/tasks/09-20-454-task-lifecycle-state-model",
                },
                platform_input={"context_key": "one"},
            )
        self.assertEqual(self.official.calls, [])


class ResourceLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.common = self.root / ".git"
        self.common.mkdir()
        self.repository = RepositoryFacts(self.root, self.common, self.common)
        self.store = ResourceLedgerStore(self.repository)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @staticmethod
    def key(generation=0):
        return TaskLifecycleKey(TASK_A, generation)

    def test_five_acquisition_projections_are_conservative_and_path_free(self) -> None:
        cases = [
            (0, "caller_owned", "not_applicable", 1),
            (1, "caller_owned", "caller_owned", 2),
            (2, "guru_owned", "guru_owned", 2),
            (3, "caller_owned", "guru_owned", 2),
        ]
        for generation, branch_owner, worktree_owner, resource_count in cases:
            with self.subTest(generation=generation):
                key = self.key(generation)
                current = self.store.establish_current(
                    key,
                    binding_epoch=10 + generation,
                    binding_revision=0,
                    branch_name=f"topic-{generation}",
                    branch_ownership=branch_owner,
                    worktree_ownership=worktree_owner,
                )
                ledger = self.store.read(key)
                self.assertEqual(current.binding_revision, 0)
                self.assertEqual(len(ledger.resources), resource_count)
                self.assertNotIn("path", json.dumps(ledger.as_dict()))

        recovered = self.store.recover_active_missing(
            self.key(4),
            binding_epoch=14,
            binding_revision=2,
            branch_name="topic-4",
            live_branch_present=True,
            linked_worktree_present=True,
            remote_delivery=("origin", "castbox/guru-trellis", "refs/heads/topic-4"),
        )
        ledger = self.store.read(self.key(4))
        self.assertEqual(recovered.binding_revision, 2)
        self.assertEqual({row.ownership for row in ledger.resources}, {"caller_owned"})
        self.assertEqual(
            {row.acquisition_origin for row in ledger.resources},
            {"conservative_recovery"},
        )
        before = self.store.snapshot(self.key(4)).content
        rematerialized = self.store.recover_active_missing(
            self.key(4),
            binding_epoch=14,
            binding_revision=2,
            branch_name="topic-4",
            live_branch_present=True,
            linked_worktree_present=True,
            remote_delivery=("origin", "castbox/guru-trellis", "refs/heads/topic-4"),
        )
        self.assertEqual(rematerialized, recovered)
        self.assertEqual(self.store.snapshot(self.key(4)).content, before)
        with self.assertRaisesRegex(LifecycleContractError, "resource_ownership_conflict"):
            self.store.recover_active_missing(
                self.key(4),
                binding_epoch=14,
                binding_revision=2,
                branch_name="topic-4",
                live_branch_present=True,
                linked_worktree_present=True,
                remote_delivery=("upstream", "castbox/guru-trellis", "refs/heads/topic-4"),
            )
        self.assertEqual(self.store.snapshot(self.key(4)).content, before)

    def test_snapshot_restore_and_c4_port_projection_preserve_exact_bytes(self) -> None:
        key = self.key()
        self.store.establish_current(
            key,
            binding_epoch=7,
            binding_revision=0,
            branch_name=BRANCH,
            branch_ownership="caller_owned",
            worktree_ownership="caller_owned",
        )
        snapshot = self.store.snapshot(key)
        before = snapshot.content
        self.store.rebind_current(
            key,
            expected_epoch=7,
            expected_revision=0,
            source_branch_name=BRANCH,
            target_branch_name=TARGET,
            expected_cleanup_head=HEAD,
            target_branch_ownership="guru_owned",
            target_worktree_ownership=None,
            worktree_reassociated=True,
        )
        self.assertEqual(
            (self.store.read_current(key).binding_revision, self.store.read_current(key).branch_name),
            (1, TARGET),
        )
        self.store.restore(key, snapshot)
        self.assertEqual(self.store.snapshot(key).content, before)
        self.assertEqual(self.store.read_current(key).branch_name, BRANCH)

    def test_rebind_retires_old_resources_without_dropping_responsibility(self) -> None:
        key = self.key()
        self.store.establish_current(
            key,
            binding_epoch=7,
            binding_revision=0,
            branch_name=BRANCH,
            branch_ownership="guru_owned",
            worktree_ownership="guru_owned",
        )
        self.store.rebind_current(
            key,
            expected_epoch=7,
            expected_revision=0,
            source_branch_name=BRANCH,
            target_branch_name=TARGET,
            expected_cleanup_head=HEAD,
            target_branch_ownership="guru_owned",
            target_worktree_ownership=None,
            worktree_reassociated=True,
        )
        ledger = self.store.read(key)
        source_branch = next(
            row for row in ledger.resources
            if row.kind == "local_branch" and row.branch_ref == f"refs/heads/{BRANCH}"
        )
        source_worktree = next(
            row for row in ledger.resources
            if row.kind == "linked_worktree" and row.branch_ref == f"refs/heads/{BRANCH}"
        )
        self.assertEqual(
            (source_branch.state, source_branch.responsibility_role, source_branch.expected_cleanup_head),
            ("cleanup_pending", "retired_cleanup", HEAD),
        )
        self.assertEqual(
            (source_worktree.state, source_worktree.responsibility_role),
            ("resolved", "superseded"),
        )
        self.assertTrue(
            self.store.branch_has_unresolved_incarnation(
                BRANCH,
                key=key,
                allowed_current_epoch=None,
                allowed_current_revision=None,
            )
        )
        self.assertFalse(
            self.store.branch_has_unresolved_incarnation(
                TARGET,
                key=key,
                allowed_current_epoch=7,
                allowed_current_revision=1,
            )
        )
        seal = self.store.seal_for_finish(
            key, finish_result_id="finish:rebound", finish_head=FINISH_HEAD
        )
        resolution = self.store.cleanup_resolution(
            key,
            finish_result_id="finish:rebound",
            inventory_id=seal["inventory_id"],
        )
        self.assertEqual(
            {
                row.portable_ref["ref"]: row.expected_cleanup_head
                for row in resolution.resources
                if row.kind == "local_branch"
            },
            {f"refs/heads/{BRANCH}": HEAD, f"refs/heads/{TARGET}": FINISH_HEAD},
        )

    def test_caller_owned_rebind_history_stays_retained_and_manual_only(self) -> None:
        key = self.key()
        self.store.establish_current(
            key,
            binding_epoch=7,
            binding_revision=0,
            branch_name=BRANCH,
            branch_ownership="caller_owned",
            worktree_ownership="caller_owned",
        )
        self.store.rebind_current(
            key,
            expected_epoch=7,
            expected_revision=0,
            source_branch_name=BRANCH,
            target_branch_name=TARGET,
            expected_cleanup_head=HEAD,
            target_branch_ownership="caller_owned",
            target_worktree_ownership="caller_owned",
            worktree_reassociated=False,
        )
        retired = [
            row for row in self.store.read(key).resources
            if row.branch_ref == f"refs/heads/{BRANCH}"
        ]
        self.assertEqual({row.state for row in retired}, {"retained"})
        self.assertEqual({row.responsibility_role for row in retired}, {"manual_only"})

    def test_active_missing_is_not_conflict_and_terminal_missing_does_not_write(self) -> None:
        key = self.key()
        recovered = self.store.recover_active_missing(
            key,
            binding_epoch=7,
            binding_revision=3,
            branch_name=BRANCH,
            live_branch_present=True,
            linked_worktree_present=False,
        )
        self.assertEqual((recovered.binding_epoch, recovered.binding_revision), (7, 3))
        before = self.store.snapshot(key).content
        self.assertEqual(
            self.store.recover_active_missing(
                key,
                binding_epoch=7,
                binding_revision=3,
                branch_name=BRANCH,
                live_branch_present=True,
                linked_worktree_present=False,
            ),
            recovered,
        )
        self.assertEqual(self.store.snapshot(key).content, before)
        with self.assertRaisesRegex(LifecycleContractError, "resource_ownership_conflict"):
            self.store.recover_active_missing(
                key,
                binding_epoch=7,
                binding_revision=4,
                branch_name=BRANCH,
                live_branch_present=True,
                linked_worktree_present=False,
            )

        missing_key = self.key(1)
        resolution = self.store.terminal_missing_resolution(
            missing_key,
            finish_result_id="finish:1",
        )
        self.assertEqual(resolution.resolution_kind, "manual_selection_required")
        self.assertFalse(self.store.path_for(missing_key).exists())

    def test_malformed_ledger_is_conflict_not_missing(self) -> None:
        key = self.key()
        path = self.store.path_for(key)
        path.parent.mkdir(parents=True)
        path.write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(LifecycleContractError, "resource_ledger_conflict"):
            self.store.read_current(key)

    def test_remote_role_finish_inventory_and_cleanup_filtering(self) -> None:
        key = self.key()
        self.store.establish_current(
            key,
            binding_epoch=7,
            binding_revision=0,
            branch_name=BRANCH,
            branch_ownership="guru_owned",
            worktree_ownership="guru_owned",
        )
        with self.assertRaisesRegex(LifecycleContractError, "resource_ledger_conflict"):
            self.store.record_remote_delivery(
                key,
                expected_epoch=7,
                expected_revision=0,
                remote_name="origin",
                repository_ref="castbox/guru-trellis",
                branch_ref=f"refs/heads/{TARGET}",
                ownership="guru_owned",
                expected_cleanup_head=HEAD,
            )
        remote = self.store.record_remote_delivery(
            key,
            expected_epoch=7,
            expected_revision=0,
            remote_name="origin",
            repository_ref="castbox/guru-trellis",
            branch_ref=f"refs/heads/{BRANCH}",
            ownership="guru_owned",
            expected_cleanup_head=HEAD,
        )
        self.assertEqual(remote.responsibility_role, "current_delivery")
        self.assertEqual(remote.portable_ref["remote_name"], "origin")
        ledger = self.store.read(key)
        current_worktree = next(
            row for row in ledger.resources
            if row.responsibility_role == "current_worktree"
        )
        for row in (current_worktree, remote):
            with self.subTest(orphan_role=row.responsibility_role):
                with self.assertRaisesRegex(LifecycleContractError, "resource_ledger_conflict"):
                    ResourceLedger(
                        key.task_id,
                        key.lifecycle_generation,
                        ledger.ledger_revision,
                        (row,),
                    )
        before_remote_retry = self.store.snapshot(key).content
        self.assertEqual(
            self.store.record_remote_delivery(
                key,
                expected_epoch=7,
                expected_revision=0,
                remote_name="origin",
                repository_ref="castbox/guru-trellis",
                branch_ref=f"refs/heads/{BRANCH}",
                ownership="guru_owned",
                expected_cleanup_head=HEAD,
            ),
            remote,
        )
        self.assertEqual(self.store.snapshot(key).content, before_remote_retry)
        with self.assertRaisesRegex(LifecycleContractError, "resource_ownership_conflict"):
            self.store.record_remote_delivery(
                key,
                expected_epoch=7,
                expected_revision=0,
                remote_name="upstream",
                repository_ref="castbox/guru-trellis",
                branch_ref=f"refs/heads/{BRANCH}",
                ownership="guru_owned",
                expected_cleanup_head=HEAD,
            )
        self.assertEqual(self.store.snapshot(key).content, before_remote_retry)
        with self.assertRaisesRegex(LifecycleContractError, "resource_ownership_conflict"):
            self.store.record_remote_delivery(
                key,
                expected_epoch=7,
                expected_revision=0,
                remote_name="origin",
                repository_ref="castbox/guru-trellis",
                branch_ref=f"refs/heads/{BRANCH}",
                ownership="caller_owned",
                expected_cleanup_head=HEAD,
            )
        retained = self.store.record_retained_control_ref(
            key,
            remote_name="origin",
            repository_ref="castbox/guru-trellis",
            branch_ref=f"refs/heads/guru-task-lifecycle/{TASK_A}",
        )
        other_remote = self.store.record_retained_control_ref(
            key,
            remote_name="upstream",
            repository_ref="castbox/guru-trellis",
            branch_ref=f"refs/heads/guru-task-lifecycle/{TASK_A}",
        )
        self.assertNotEqual(retained.resource_id, other_remote.resource_id)
        self.assertNotEqual(retained.portable_ref, other_remote.portable_ref)
        after_unrelated_mutation = self.store.snapshot(key).content
        self.assertEqual(
            self.store.record_remote_delivery(
                key,
                expected_epoch=7,
                expected_revision=0,
                remote_name="origin",
                repository_ref="castbox/guru-trellis",
                branch_ref=f"refs/heads/{BRANCH}",
                ownership="guru_owned",
                expected_cleanup_head=HEAD,
            ),
            remote,
        )
        self.assertEqual(self.store.snapshot(key).content, after_unrelated_mutation)
        for suffix in ("bad ref", "bad\tref", "bad\nref", "bad\x00ref", "bad\x7fref"):
            with self.subTest(retained_suffix=repr(suffix)):
                with self.assertRaisesRegex(LifecycleContractError, "invalid_branch_ref"):
                    self.store.record_retained_control_ref(
                        key,
                        remote_name="origin",
                        repository_ref="castbox/guru-trellis",
                        branch_ref=f"refs/heads/guru-task-lifecycle/{suffix}",
                    )
        with self.assertRaisesRegex(LifecycleContractError, "invalid_resource_ref"):
            self.store.record_remote_delivery(
                key,
                expected_epoch=7,
                expected_revision=0,
                remote_name="bad name",
                repository_ref="castbox/guru-trellis",
                branch_ref=f"refs/heads/{BRANCH}",
                ownership="guru_owned",
            )
        before_invalid_seal = self.store.snapshot(key).content
        with self.assertRaisesRegex(LifecycleContractError, "resource_ledger_conflict"):
            self.store.seal_for_finish(key, finish_result_id="finish:1", finish_head=None)
        self.assertEqual(self.store.snapshot(key).content, before_invalid_seal)
        seal = self.store.seal_for_finish(
            key, finish_result_id="finish:1", finish_head=FINISH_HEAD
        )
        self.assertEqual(seal["finish_head"], FINISH_HEAD)
        sealed_snapshot = self.store.snapshot(key).content
        self.assertEqual(
            self.store.seal_for_finish(
                key, finish_result_id="finish:1", finish_head=FINISH_HEAD
            ),
            seal,
        )
        for finish_id, finish_head in (("finish:2", FINISH_HEAD), ("finish:1", HEAD)):
            with self.subTest(finish_id=finish_id, finish_head=finish_head):
                with self.assertRaisesRegex(LifecycleContractError, "resource_ledger_conflict"):
                    self.store.seal_for_finish(
                        key, finish_result_id=finish_id, finish_head=finish_head
                    )
        self.assertEqual(self.store.snapshot(key).content, sealed_snapshot)
        with self.assertRaisesRegex(LifecycleContractError, "resource_ledger_conflict"):
            self.store.cleanup_resolution(
                key, finish_result_id="finish:2", inventory_id=seal["inventory_id"]
            )
        resolution = self.store.cleanup_resolution(
            key,
            finish_result_id="finish:1",
            inventory_id=seal["inventory_id"],
        )
        self.assertEqual(resolution.resolution_kind, "ordinary_cleanup")
        cleanup_ids = {row.resource_id for row in resolution.resources}
        self.assertIn(remote.resource_id, cleanup_ids)
        self.assertNotIn(retained.resource_id, cleanup_ids)
        self.assertNotIn(other_remote.resource_id, cleanup_ids)
        self.assertEqual(len(cleanup_ids), 3)
        self.assertEqual(
            {row.expected_cleanup_head for row in resolution.resources}, {FINISH_HEAD}
        )
        self.assertEqual(
            next(
                row for row in resolution.resources if row.kind == "remote_branch"
            ).portable_ref,
            remote.portable_ref,
        )
        self.store.record_retained_control_ref(
            key,
            remote_name="origin",
            repository_ref="castbox/guru-trellis",
            branch_ref=f"refs/heads/guru-task-lifecycle/{TASK_A}-post-finish",
        )
        after_retained = self.store.snapshot(key).content
        refreshed_seal = self.store.seal_for_finish(
            key, finish_result_id="finish:1", finish_head=FINISH_HEAD
        )
        self.assertNotEqual(refreshed_seal["inventory_id"], seal["inventory_id"])
        self.assertEqual(self.store.snapshot(key).content, after_retained)
        self.assertEqual(
            self.store.cleanup_resolution(
                key, finish_result_id="finish:1", inventory_id=refreshed_seal["inventory_id"]
            ).resources,
            resolution.resources,
        )
        with self.assertRaisesRegex(LifecycleContractError, "resource_inventory_stale"):
            self.store.resolve_for_cleanup(
                key, finish_result_id="finish:1", inventory_id=refreshed_seal["inventory_id"],
                resource_ids=[remote.resource_id],
            )
        resolved_inventory = self.store.resolve_for_cleanup(
            key, finish_result_id="finish:1", inventory_id=refreshed_seal["inventory_id"],
            resource_ids=sorted(cleanup_ids),
        )
        self.assertEqual(
            self.store.cleanup_resolution(
                key, finish_result_id="finish:1", inventory_id=resolved_inventory,
            ).resolution_kind,
            "already_clean",
        )
        self.assertEqual(
            self.store.resolve_for_cleanup(
                key, finish_result_id="finish:1", inventory_id=resolved_inventory,
                resource_ids=[],
            ),
            resolved_inventory,
        )

    def test_remote_delivery_advances_one_incarnation_and_rebind_seals_latest_head(self) -> None:
        checkout = self.root / "published-commits"
        subprocess.run(["git", "init", "-q", str(checkout)], check=True)
        git_command = ["git", "-C", str(checkout)]

        def commit(message: str) -> str:
            subprocess.run(
                [
                    *git_command,
                    "-c", "user.name=Guru Test",
                    "-c", "user.email=guru-test@example.invalid",
                    "commit", "--allow-empty", "-qm", message,
                ],
                check=True,
            )
            return subprocess.check_output([*git_command, "rev-parse", "HEAD"], text=True).strip()

        first_head = commit("first publication")
        second_head = commit("second publication")
        finish_head = commit("finish")
        repository = RepositoryFacts(checkout, checkout / ".git", checkout / ".git")
        store = ResourceLedgerStore(repository)
        key = self.key()
        store.establish_current(
            key,
            binding_epoch=7,
            binding_revision=0,
            branch_name=BRANCH,
            branch_ownership="guru_owned",
            worktree_ownership="not_applicable",
        )
        with self.assertRaisesRegex(LifecycleContractError, "resource_ledger_conflict"):
            store.record_remote_delivery(
                key,
                expected_epoch=7,
                expected_revision=0,
                remote_name="origin",
                repository_ref="castbox/guru-trellis",
                branch_ref=f"refs/heads/{BRANCH}",
                ownership="guru_owned",
            )
        first = store.record_remote_delivery(
            key,
            expected_epoch=7,
            expected_revision=0,
            remote_name="origin",
            repository_ref="castbox/guru-trellis",
            branch_ref=f"refs/heads/{BRANCH}",
            ownership="guru_owned",
            expected_cleanup_head=first_head,
        )
        second = store.record_remote_delivery(
            key,
            expected_epoch=7,
            expected_revision=0,
            remote_name="origin",
            repository_ref="castbox/guru-trellis",
            branch_ref=f"refs/heads/{BRANCH}",
            ownership="guru_owned",
            expected_cleanup_head=second_head,
        )
        self.assertEqual((second.resource_id, second.acquisition_origin), (
            first.resource_id, first.acquisition_origin,
        ))
        self.assertEqual(second.expected_cleanup_head, second_head)
        after_advance = store.snapshot(key).content
        self.assertEqual(
            store.record_remote_delivery(
                key,
                expected_epoch=7,
                expected_revision=0,
                remote_name="origin",
                repository_ref="castbox/guru-trellis",
                branch_ref=f"refs/heads/{BRANCH}",
                ownership="guru_owned",
                expected_cleanup_head=second_head,
            ),
            second,
        )
        self.assertEqual(store.snapshot(key).content, after_advance)
        with self.assertRaisesRegex(LifecycleContractError, "resource_ownership_conflict"):
            store.record_remote_delivery(
                key,
                expected_epoch=7,
                expected_revision=0,
                remote_name="origin",
                repository_ref="castbox/guru-trellis",
                branch_ref=f"refs/heads/{BRANCH}",
                ownership="guru_owned",
                expected_cleanup_head=first_head,
            )
        self.assertEqual(store.snapshot(key).content, after_advance)
        store.rebind_current(
            key,
            expected_epoch=7,
            expected_revision=0,
            source_branch_name=BRANCH,
            target_branch_name=TARGET,
            expected_cleanup_head=second_head,
            target_branch_ownership="guru_owned",
            target_worktree_ownership="not_applicable",
            worktree_reassociated=False,
        )
        seal = store.seal_for_finish(
            key, finish_result_id="finish:advanced", finish_head=finish_head
        )
        resolution = store.cleanup_resolution(
            key,
            finish_result_id="finish:advanced",
            inventory_id=seal["inventory_id"],
        )
        remote = next(row for row in resolution.resources if row.kind == "remote_branch")
        self.assertEqual((remote.resource_id, remote.expected_cleanup_head), (
            first.resource_id, second_head,
        ))

    def test_recovered_caller_remote_can_gain_a_known_head_without_changing_origin(self) -> None:
        key = self.key()
        self.store.recover_active_missing(
            key,
            binding_epoch=7,
            binding_revision=0,
            branch_name=BRANCH,
            live_branch_present=True,
            linked_worktree_present=False,
            remote_delivery=("origin", "castbox/guru-trellis", f"refs/heads/{BRANCH}"),
        )
        updated = self.store.record_remote_delivery(
            key,
            expected_epoch=7,
            expected_revision=0,
            remote_name="origin",
            repository_ref="castbox/guru-trellis",
            branch_ref=f"refs/heads/{BRANCH}",
            ownership="caller_owned",
            expected_cleanup_head=HEAD,
        )
        self.assertEqual((updated.acquisition_origin, updated.expected_cleanup_head), (
            "conservative_recovery", HEAD,
        ))
        self.assertEqual(
            self.store.record_remote_delivery(
                key,
                expected_epoch=7,
                expected_revision=0,
                remote_name="origin",
                repository_ref="castbox/guru-trellis",
                branch_ref=f"refs/heads/{BRANCH}",
                ownership="caller_owned",
                expected_cleanup_head=HEAD,
            ),
            updated,
        )

    def test_cleanup_runtime_rejects_shapes_forbidden_by_the_public_schema(self) -> None:
        from runtime.task_lifecycle.resource_ledger import CleanupResolution, CleanupResource

        with self.assertRaisesRegex(LifecycleContractError, "retained_control_ref_forbidden"):
            CleanupResource(
                "resource:manual",
                "remote_branch",
                {
                    "kind": "remote_branch",
                    "remote_name": "origin",
                    "repository_ref": "castbox/guru-trellis",
                    "ref": f"refs/heads/guru-task-lifecycle/{TASK_A}",
                },
                HEAD,
            )
        with self.assertRaisesRegex(LifecycleContractError, "resource_ledger_conflict"):
            CleanupResolution(
                "ordinary_cleanup",
                self.key(),
                "finish:1",
                inventory_id="resource-inventory:1",
                resources=(),
            )
        with self.assertRaisesRegex(LifecycleContractError, "resource_ledger_conflict"):
            CleanupResolution(
                "ordinary_cleanup",
                self.key(),
                "finish:1",
                inventory_id="resource-inventory:1",
                resources=(
                    CleanupResource(
                        "resource:1",
                        "local_branch",
                        {"kind": "local_branch", "ref": f"refs/heads/{BRANCH}"},
                        None,
                    ),
                ),
            )

    def test_caller_owned_and_unknown_recovery_never_enter_ordinary_cleanup(self) -> None:
        key = self.key()
        self.store.recover_active_missing(
            key,
            binding_epoch=7,
            binding_revision=0,
            branch_name=BRANCH,
            live_branch_present=True,
            linked_worktree_present=True,
        )
        seal = self.store.seal_for_finish(
            key, finish_result_id="finish:2", finish_head=FINISH_HEAD
        )
        resolution = self.store.cleanup_resolution(
            key,
            finish_result_id="finish:2",
            inventory_id=seal["inventory_id"],
        )
        self.assertEqual(resolution.resolution_kind, "already_clean")
        rows = self.store.read(key).resources
        with self.assertRaisesRegex(LifecycleContractError, "resource_ownership_conflict"):
            self.store.resolve_selected_cleanup(
                key, finish_result_id="finish:2", resource_ids=["resource:other"]
            )
        selected = rows[0].resource_id
        inventory = self.store.resolve_selected_cleanup(
            key, finish_result_id="finish:2", resource_ids=[selected]
        )
        updated = self.store.read(key)
        self.assertEqual(updated.resources[0].state, "resolved")
        self.assertEqual(updated.resources[1].state, "retained")
        self.assertEqual(self.store._inventory_id(updated), inventory)


if __name__ == "__main__":
    unittest.main()
