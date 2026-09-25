from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.schema import CONTRACT_ROOT, dto_names, load_contract, validate_dto


TASK_ID = "454-task-lifecycle-state-model"
TASK_REF = ".trellis/tasks/09-20-454-task-lifecycle-state-model"
GENERATION = 0
COMMIT = "a" * 40
OTHER_COMMIT = "b" * 40
DIGEST = "c" * 64
BRANCH_NAME = "codex/454-task-lifecycle-state-model-c3-c7"


def valid_branch_binding() -> dict:
    return {
        "schema_version": "1.0",
        "task_id": TASK_ID,
        "lifecycle_generation": GENERATION,
        "binding_epoch": 7,
        "binding_revision": 0,
        "branch_name": BRANCH_NAME,
    }


def valid_rebind_transactions() -> dict[str, dict]:
    common = {
        "schema_version": "1.0",
        "transaction_id": "rebind:1",
        "task_id": TASK_ID,
        "lifecycle_generation": GENERATION,
        "stage": "prepared",
        "source_binding": valid_branch_binding(),
        "target_binding_revision": 1,
        "target_branch_name": "codex/454-task-lifecycle-state-model-c4",
        "source_head": COMMIT,
        "target_head": OTHER_COMMIT,
        "resource_ledger_revision": 0,
    }
    return {
        "same_checkout_new_ref": {
            **common,
            "route": "same_checkout_new_ref",
            "checkout_root": "/tmp/task",
            "source_index_sha256": DIGEST,
            "source_worktree_sha256": DIGEST,
            "source_status_sha256": DIGEST,
        },
        "existing_target": {
            **common,
            "route": "existing_target",
            "source_checkout_root": "/tmp/source",
            "target_checkout_root": "/tmp/target",
            "target_task_artifact_sha256": DIGEST,
        },
    }


def valid_payloads() -> dict[str, dict]:
    base = {"task_id": TASK_ID, "lifecycle_generation": GENERATION}
    artifact = {**base, "task_ref": TASK_REF}
    result = {**base, "result_id": "result:1"}
    return {
        "TaskIdentityDTO": {"task_id": TASK_ID, "task_ref": TASK_REF},
        "TaskLifecycleDTO": base,
        "TaskArtifactDTO": artifact,
        "ResultRefDTO": result,
        "IssueRefDTO": {"repo_ref": "castbox/guru-trellis", "issue_number": 454},
        "IssueIntakeRefDTO": {"repo_ref": "castbox/guru-trellis", "issue_number": 454, "result_id": "issue:454"},
        "SourceRelationRefDTO": {**base, "source_relation_id": "source:1"},
        "SourceCorrectionReadyDTO": {
            **artifact,
            "current_source": {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454},
            "reviewed_source": {"kind": "no_issue"},
            "accepted_scope_identity": "scope:1",
            "target_relation_id": "target:1",
            "result_id": "source-correction:1",
        },
        "DeliveryTargetRefDTO": {**base, "target_relation_id": "target:1"},
        "BranchBindingRefDTO": {**base, "binding_epoch": 0, "binding_revision": 1},
        "CheckoutAcquisitionPlanDTO": {**artifact, "route": "adopt_invocation_checkout", "branch_ref": "codex/task", "decision_head": COMMIT, "task_artifact_expectation": "required", "invocation_checkout": "/tmp/task", "transaction_id": "checkout:1", "result_id": "checkout-result:1"},
        "CheckoutCandidateDTO": {"candidate_id": "candidate:1", "path": "/tmp/task", "head": COMMIT, "branch_ref": "codex/task", "topology": "linked", "dirty_paths": [], "discovered_at": "2026-09-22T00:00:00Z", "validation_state": "valid", "reason_code": None},
        "CheckoutResolutionDTO": {"resolution_kind": "checkout_resolved", "reason_code": "unique_candidate", "selected_candidate_id": "candidate:1"},
        "CheckoutSelectionDTO": {"selection_kind": "explicit_target", "target_path": "/tmp/task", "branch_ref": "codex/task", "expected_head": COMMIT, "selected_at": "2026-09-22T00:00:00Z"},
        "CheckpointRefDTO": {**base, "checkpoint_commit": COMMIT, "checkpoint_ref": "refs/heads/checkpoint", "result_id": "checkpoint:1"},
        "HandoffRefDTO": {**base, "handoff_id": "handoff:1", "receipt_ref": f"refs/heads/guru-task-lifecycle/{TASK_ID}", "result_id": "handoff-result:1"},
        "HandoffInventoryRefDTO": {**base, "handoff_id": "handoff:1", "inventory_id": "inventory:1"},
        "ResourceSealRefDTO": {**base, "finish_result_id": "finish:1", "inventory_id": "inventory:1"},
        "TerminalFinishRefDTO": {**base, "finish_result_id": "finish:1", "cleanup_state": "manual_cleanup_required"},
        "CleanupResultRefDTO": {**base, "cleanup_result_id": "cleanup:1"},
        "PlanningApprovalRefDTO": {**artifact, "result_id": "planning:1"},
        "BaseReconcileResultDTO": {**artifact, "task_head": COMMIT, "new_base_head": OTHER_COMMIT, "resume_target": "task_activation", "result_id": "reconcile:1"},
        "BaseContinuitySeedDTO": {**artifact, "task_head": COMMIT, "old_base_head": OTHER_COMMIT, "new_base_head": COMMIT, "branch_review_commit": OTHER_COMMIT, "candidate_tree_sha256": DIGEST, "relevant_paths": ["trellis/skills/guru-team/runtime/task_lifecycle/identity.py"], "resume_target": "guru-review-branch", "result_id": "continuity-seed:1"},
        "BaseContinuityResultDTO": {**artifact, "branch_review_commit": COMMIT, "resume_target": "guru-current-phase-router", "result_id": "continuity:1"},
        "Phase2ResultDTO": {**artifact, "phase2_commit_anchor": COMMIT, "result_id": "phase2:1"},
        "TaskCommitResultDTO": {**artifact, "base_ref": "main", "branch_review_commit": COMMIT, "result_id": "commit:1"},
        "BranchReviewResultDTO": {**artifact, "branch_review_commit": COMMIT, "result_id": "review:1"},
        "PublicationReadyDTO": {**artifact, "branch_review_commit": COMMIT, "pr_title": "建立 lifecycle kernel", "pr_body": "Current reviewed payload.", "result_id": "publication:1"},
        "DeliveryReviewReadyDTO": {**artifact, "delivery_cycle_ref": "delivery:1", "reviewed_head": COMMIT, "pr_title": "交付 lifecycle kernel", "pr_body": "Reviewed delivery payload.", "remaining_work_state": "remaining", "result_id": "delivery-review:1"},
        "MergeReadyDTO": {**base, "repo_ref": "castbox/guru-trellis", "pr_number": 1, "expected_head_sha": COMMIT, "expected_base_branch": "main", "expected_head_branch": "codex/task", "publication_body_sha256": DIGEST, "result_id": "merge-ready:1"},
        "DeliveryMergeReadyDTO": {**artifact, "delivery_cycle_ref": "delivery:1", "repo_ref": "castbox/guru-trellis", "pr_number": 1, "expected_head_sha": COMMIT, "publication_body_sha256": DIGEST, "result_id": "delivery-merge-ready:1"},
        "TaskMergeResultDTO": {**base, "repo_ref": "castbox/guru-trellis", "pr_number": 1, "merge_commit_sha": COMMIT, "merge_lineage": "closeout", "result_id": "merge:1"},
        "DeliveryMergeResultDTO": {**artifact, "delivery_cycle_ref": "delivery:1", "repo_ref": "castbox/guru-trellis", "pr_number": 1, "reviewed_head": COMMIT, "merge_commit_sha": OTHER_COMMIT, "result_id": "delivery-merge:1"},
        "FinalizerBaseReconcileSeedDTO": {**artifact, "task_head": COMMIT, "publication_head": COMMIT, "selected_base_ref": "main", "old_base_head": OTHER_COMMIT, "new_base_head": COMMIT, "branch_review_commit": OTHER_COMMIT, "resume_target": "guru-finalize-task", "result_id": "finalizer-reconcile:1"},
        "PublicationRefreshSeedDTO": {**artifact, "branch_review_commit": COMMIT, "reason_code": "publication_stale", "result_id": "refresh:1"},
        "FinalizationReprepareRefDTO": {**artifact, "branch_review_commit": COMMIT, "publication_head": COMMIT, "reason_code": "pr_changed", "transaction_id": "finalize:1", "result_id": "reprepare:1"},
        "MergedPRRecoveryRefDTO": {**artifact, "repo_ref": "castbox/guru-trellis", "pr_number": 1, "expected_head_sha": COMMIT, "result_id": "merged-recovery:1"},
        "TransactionRefDTO": {**base, "transaction_id": "transaction:1", "result_id": "transaction-result:1"},
        "ReasonDTO": {"reason_code": "stale_authority", "reason_refs": ["task:454"]},
    }


def valid_resource() -> dict:
    return {
        "resource_id": "resource:1",
        "kind": "local_branch",
        "acquisition_origin": "guru_created",
        "ownership": "guru_owned",
        "portable_ref": {"kind": "local_branch", "ref": f"refs/heads/{BRANCH_NAME}"},
        "binding_epoch": 7,
        "binding_revision": 0,
        "state": "cleanup_pending",
        "responsibility_role": "retired_cleanup",
        "expected_cleanup_head": COMMIT,
    }


class ContractTests(unittest.TestCase):
    def test_branch_binding_schema_is_draft_2020_12_and_exactly_six_fields(self):
        schema = load_contract("task-branch-binding.schema.json")
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        payload = valid_branch_binding()

        self.assertEqual(list(validator.iter_errors(payload)), [])
        self.assertEqual(
            set(payload),
            {
                "schema_version",
                "task_id",
                "lifecycle_generation",
                "binding_epoch",
                "binding_revision",
                "branch_name",
            },
        )
        for field, value in {
            "path": "/tmp/task",
            "head": COMMIT,
            "session_id": "session:1",
            "ownership": "guru",
        }.items():
            with self.subTest(field=field):
                self.assertTrue(list(validator.iter_errors({**payload, field: value})))

    def test_branch_binding_schema_rejects_invalid_revisions_and_branch_names(self):
        validator = Draft202012Validator(load_contract("task-branch-binding.schema.json"))
        payload = valid_branch_binding()

        for field, value in [
            ("lifecycle_generation", True),
            ("lifecycle_generation", -1),
            ("lifecycle_generation", 1.5),
            ("binding_epoch", True),
            ("binding_epoch", -1),
            ("binding_epoch", 1.5),
            ("binding_revision", True),
            ("binding_revision", -1),
            ("binding_revision", 1.5),
        ]:
            with self.subTest(field=field, value=value):
                self.assertTrue(list(validator.iter_errors({**payload, field: value})))

        for branch_name in [
            "HEAD",
            "refs/heads/topic",
            "refs/tags/v1",
            "guru-task-lifecycle/task-a",
            "guru-task-lifecycle",
            *[f"bad{chr(codepoint)}name" for codepoint in (*range(32), 127)],
        ]:
            with self.subTest(branch_name=branch_name):
                self.assertTrue(
                    list(validator.iter_errors({**payload, "branch_name": branch_name}))
                )

        rebind_validator = Draft202012Validator(
            load_contract("task-branch-rebind-transaction.schema.json")
        )
        for route, transaction in valid_rebind_transactions().items():
            for codepoint in (*range(32), 127):
                with self.subTest(route=route, codepoint=codepoint):
                    self.assertTrue(
                        list(
                            rebind_validator.iter_errors(
                                {
                                    **transaction,
                                    "target_branch_name": f"bad{chr(codepoint)}name",
                                }
                            )
                        )
                    )

    def test_rebind_transaction_schema_accepts_only_the_two_closed_routes(self):
        schema = load_contract("task-branch-rebind-transaction.schema.json")
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        transactions = valid_rebind_transactions()

        for route, payload in transactions.items():
            with self.subTest(route=route):
                self.assertEqual(list(validator.iter_errors(payload)), [])

        invalid = [
            {**transactions["same_checkout_new_ref"], "route": "unknown"},
            {**transactions["same_checkout_new_ref"], "target_checkout_root": "/tmp/target"},
            {**transactions["existing_target"], "checkout_root": "/tmp/task"},
            {**transactions["existing_target"], "authorization": "confirmed"},
        ]
        for index, payload in enumerate(invalid):
            with self.subTest(index=index):
                self.assertTrue(list(validator.iter_errors(payload)))

    def test_rebind_transaction_schema_enforces_route_specific_required_fields(self):
        validator = Draft202012Validator(
            load_contract("task-branch-rebind-transaction.schema.json")
        )
        transactions = valid_rebind_transactions()
        required_by_route = {
            "same_checkout_new_ref": (
                "checkout_root",
                "source_index_sha256",
                "source_worktree_sha256",
                "source_status_sha256",
            ),
            "existing_target": (
                "source_checkout_root",
                "target_checkout_root",
                "target_task_artifact_sha256",
            ),
        }

        for route, fields in required_by_route.items():
            for field in fields:
                payload = dict(transactions[route])
                del payload[field]
                with self.subTest(route=route, field=field):
                    self.assertTrue(list(validator.iter_errors(payload)))

        for route, payload in transactions.items():
            for field, value in [
                ("lifecycle_generation", True),
                ("target_binding_revision", True),
                ("target_binding_revision", 0),
                ("target_binding_revision", 1.5),
                ("resource_ledger_revision", -1),
            ]:
                with self.subTest(route=route, field=field, value=value):
                    self.assertTrue(list(validator.iter_errors({**payload, field: value})))

            for epoch in (True, -1, 1.5):
                with self.subTest(route=route, source_binding_epoch=epoch):
                    self.assertTrue(
                        list(
                            validator.iter_errors(
                                {
                                    **payload,
                                    "source_binding": {
                                        **payload["source_binding"],
                                        "binding_epoch": epoch,
                                    },
                                }
                            )
                        )
                    )

    def test_resource_ledger_schema_is_closed_and_path_free(self):
        schema = load_contract("task-resource-ledger.schema.json")
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        payload = {
            "schema_version": "1.0",
            "task_id": TASK_ID,
            "lifecycle_generation": GENERATION,
            "ledger_revision": 4,
            "resources": [valid_resource()],
        }
        self.assertEqual(list(validator.iter_errors(payload)), [])
        retained = {
            "resource_id": "resource:retained",
            "kind": "remote_branch",
            "acquisition_origin": "retained_control",
            "ownership": "caller_owned",
            "portable_ref": {
                "kind": "remote_branch",
                "remote_name": "origin",
                "repository_ref": "castbox/guru-trellis",
                "ref": f"refs/heads/guru-task-lifecycle/{TASK_ID}",
            },
            "binding_epoch": 0,
            "binding_revision": 4,
            "state": "retained",
            "responsibility_role": "retained_control",
            "expected_cleanup_head": None,
        }
        self.assertEqual(
            list(validator.iter_errors({**payload, "resources": [retained]})),
            [],
        )
        current_worktree = {
            **valid_resource(),
            "resource_id": "resource:current-worktree",
            "kind": "linked_worktree",
            "portable_ref": {
                "kind": "linked_worktree",
                "branch_ref": f"refs/heads/{BRANCH_NAME}",
            },
            "state": "current",
            "responsibility_role": "current_worktree",
            "expected_cleanup_head": None,
        }
        current_delivery = {
            **valid_resource(),
            "resource_id": "resource:current-delivery",
            "kind": "remote_branch",
            "acquisition_origin": "publication",
            "portable_ref": {
                "kind": "remote_branch",
                "remote_name": "origin",
                "repository_ref": "castbox/guru-trellis",
                "ref": f"refs/heads/{BRANCH_NAME}",
            },
            "state": "current",
            "responsibility_role": "current_delivery",
        }
        current_branch = {
            **valid_resource(),
            "resource_id": "resource:current-branch",
            "state": "current",
            "responsibility_role": "current_branch",
        }
        self.assertTrue(list(validator.iter_errors({
            **payload,
            "resources": [current_branch, {**current_delivery, "expected_cleanup_head": None}],
        })))
        self.assertTrue(list(validator.iter_errors({
            **payload,
            "resources": [current_branch, {
                **current_delivery,
                "state": "cleanup_pending",
                "responsibility_role": "retired_cleanup",
                "expected_cleanup_head": None,
            }],
        })))
        self.assertEqual(list(validator.iter_errors({
            **payload,
            "resources": [current_branch, {
                **current_delivery,
                "acquisition_origin": "conservative_recovery",
                "ownership": "caller_owned",
                "expected_cleanup_head": None,
            }],
        })), [])
        for remote_name in ("origin", "upstream", "backup/main"):
            named_delivery = {
                **current_delivery,
                "portable_ref": {
                    **current_delivery["portable_ref"],
                    "remote_name": remote_name,
                },
            }
            with self.subTest(remote_name=remote_name):
                self.assertEqual(
                    list(validator.iter_errors({
                        **payload,
                        "resources": [current_branch, named_delivery],
                    })),
                    [],
                )
        for resource in (current_worktree, current_delivery):
            with self.subTest(orphan_role=resource["responsibility_role"]):
                self.assertTrue(
                    list(validator.iter_errors({**payload, "resources": [resource]}))
                )
        for mutation in [
            {**payload, "checkout_path": "/tmp/task"},
            {**payload, "ledger_revision": True},
            {**payload, "resources": [{**valid_resource(), "ownership": "unknown"}]},
            {**payload, "resources": [{**valid_resource(), "portable_ref": {"kind": "local_branch", "ref": "topic"}}]},
            {
                **payload,
                "resources": [{
                    **valid_resource(),
                    "portable_ref": {
                        "kind": "local_branch",
                        "ref": f"refs/heads/guru-task-lifecycle/{TASK_ID}",
                    },
                }],
            },
            {**payload, "resources": [{**valid_resource(), "state": "current"}]},
            {**payload, "resources": [{**valid_resource(), "ownership": "caller_owned"}]},
            {**payload, "resources": [{**valid_resource(), "authorization": "confirmed"}]},
            {
                **payload,
                "resources": [current_branch, {
                    **current_delivery,
                    "portable_ref": {
                        key: value
                        for key, value in current_delivery["portable_ref"].items()
                        if key != "remote_name"
                    },
                }],
            },
            {
                **payload,
                "resources": [current_branch, {
                    **current_delivery,
                    "portable_ref": {**current_delivery["portable_ref"], "remote_name": "bad name"},
                }],
            },
            {
                **payload,
                "resources": [{
                    **retained,
                    "portable_ref": {
                        **retained["portable_ref"],
                        "ref": "refs/heads/guru-task-lifecycle/bad ref",
                    },
                }],
            },
        ]:
            self.assertTrue(list(validator.iter_errors(mutation)))
        for suffix in ("bad\tref", "bad\nref", "bad\x00ref", "bad\x7fref"):
            invalid_retained = {
                **retained,
                "portable_ref": {
                    **retained["portable_ref"],
                    "ref": f"refs/heads/guru-task-lifecycle/{suffix}",
                },
            }
            with self.subTest(retained_suffix=repr(suffix)):
                self.assertTrue(
                    list(
                        validator.iter_errors(
                            {**payload, "resources": [invalid_retained]}
                        )
                    )
                )

    def test_finish_seal_and_cleanup_resolution_schemas_are_minimal_closed_contracts(self):
        seal_schema = load_contract("task-resource-seal-input.schema.json")
        cleanup_schema = load_contract("task-resource-cleanup-resolution.schema.json")
        Draft202012Validator.check_schema(seal_schema)
        Draft202012Validator.check_schema(cleanup_schema)
        seal = {
            "schema_version": "1.0",
            "task_id": TASK_ID,
            "lifecycle_generation": GENERATION,
            "finish_result_id": "finish:1",
            "finish_head": COMMIT,
            "ledger_revision": 5,
            "inventory_id": "resource-inventory:1",
        }
        resource = {
            "resource_id": "resource:1",
            "kind": "local_branch",
            "portable_ref": {"kind": "local_branch", "ref": f"refs/heads/{BRANCH_NAME}"},
            "expected_cleanup_head": COMMIT,
        }
        resolutions = [
            {
                "schema_version": "1.0",
                "task_id": TASK_ID,
                "lifecycle_generation": GENERATION,
                "finish_result_id": "finish:1",
                "resolution_kind": "ordinary_cleanup",
                "inventory_id": "resource-inventory:1",
                "resources": [resource],
            },
            {
                "schema_version": "1.0",
                "task_id": TASK_ID,
                "lifecycle_generation": GENERATION,
                "finish_result_id": "finish:1",
                "resolution_kind": "manual_selection_required",
                "reason_code": "terminal_resource_ledger_missing",
                "candidates": [],
            },
            {
                "schema_version": "1.0",
                "task_id": TASK_ID,
                "lifecycle_generation": GENERATION,
                "finish_result_id": "finish:1",
                "resolution_kind": "already_clean",
                "inventory_id": "resource-inventory:1",
            },
        ]
        self.assertEqual(list(Draft202012Validator(seal_schema).iter_errors(seal)), [])
        cleanup = Draft202012Validator(cleanup_schema)
        for payload in resolutions:
            with self.subTest(kind=payload["resolution_kind"]):
                self.assertEqual(list(cleanup.iter_errors(payload)), [])
        self.assertTrue(list(cleanup.iter_errors({**resolutions[0], "resources": []})))
        self.assertTrue(list(cleanup.iter_errors({
            **resolutions[0],
            "resources": [{**resource, "expected_cleanup_head": None}],
        })))
        remote_resource = {
            **resource,
            "kind": "remote_branch",
            "portable_ref": {
                "kind": "remote_branch",
                "remote_name": "upstream",
                "repository_ref": "castbox/guru-trellis",
                "ref": f"refs/heads/{BRANCH_NAME}",
            },
        }
        self.assertEqual(
            list(cleanup.iter_errors({**resolutions[0], "resources": [remote_resource]})),
            [],
        )
        self.assertTrue(list(cleanup.iter_errors({**resolutions[0], "resources": [{
            **remote_resource,
            "portable_ref": {**remote_resource["portable_ref"], "remote_name": "bad name"},
        }]})))
        self.assertEqual(
            list(cleanup.iter_errors({
                **resolutions[1],
                "candidates": [{**resource, "expected_cleanup_head": None}],
            })),
            [],
        )
        self.assertTrue(list(cleanup.iter_errors({**resolutions[1], "authorization": "confirmed"})))
        self.assertTrue(list(Draft202012Validator(seal_schema).iter_errors({**seal, "resources": []})))
        self.assertTrue(list(Draft202012Validator(seal_schema).iter_errors({
            key: value for key, value in seal.items() if key != "finish_head"
        })))
        self.assertTrue(list(Draft202012Validator(seal_schema).iter_errors({**seal, "finish_head": None})))

    def test_runtime_error_shape_has_exact_dispatcher_fields(self):
        error = LifecycleContractError("target_path_conflict", "target_path", "Choose another target.")
        self.assertEqual(set(error.as_dict()), {"code", "field_path", "remediation"})
        self.assertNotIn("details", error.__dataclass_fields__)
        for alias in ("details", "message", "unknown"):
            with self.subTest(alias=alias), self.assertRaises(TypeError):
                LifecycleContractError(
                    "target_path_conflict",
                    "target_path",
                    "Choose another target.",
                    **{alias: "not allowed"},
                )

    def test_catalog_is_closed_and_every_named_dto_has_a_valid_example(self):
        payloads = valid_payloads()
        self.assertEqual(set(dto_names()), set(payloads))
        for name, payload in payloads.items():
            with self.subTest(name=name):
                self.assertEqual(validate_dto(name, payload), payload)
                with self.assertRaises(LifecycleContractError):
                    validate_dto(name, {**payload, "authorization": "confirmed"})

    def test_checkout_timestamps_enforce_the_declared_rfc3339_domain(self):
        payloads = valid_payloads()
        valid_cases = [
            ("CheckoutCandidateDTO", "discovered_at", "2026-09-22t00:00:00z"),
            ("CheckoutSelectionDTO", "selected_at", "0000-01-01T00:00:00Z"),
            ("CheckoutSelectionDTO", "selected_at", "2016-12-31T23:59:60Z"),
        ]
        for name, field, value in valid_cases:
            with self.subTest(name=name, value=value):
                self.assertEqual(validate_dto(name, {**payloads[name], field: value})[field], value)

        invalid_cases = [
            ("CheckoutCandidateDTO", "discovered_at", "not-a-date"),
            ("CheckoutCandidateDTO", "discovered_at", "2026-13-22T00:00:00Z"),
            ("CheckoutSelectionDTO", "selected_at", "2016-12-30T23:59:60Z"),
        ]
        for name, field, value in invalid_cases:
            with self.subTest(name=name, value=value), self.assertRaises(LifecycleContractError):
                validate_dto(name, {**payloads[name], field: value})

    def test_task_artifact_projection_rejects_machine_and_git_authority(self):
        payload = valid_payloads()["TaskArtifactDTO"]
        for field, value in {
            "worktree_path": "/tmp/worktree",
            "checkout_path": "/tmp/checkout",
            "head": COMMIT,
            "base_head": OTHER_COMMIT,
            "session_id": "session-1",
            "evidence": {"digest": DIGEST},
        }.items():
            with self.subTest(field=field), self.assertRaises(LifecycleContractError):
                validate_dto("TaskArtifactDTO", {**payload, field: value})

    def test_checkout_machine_facts_are_limited_to_call_local_dtos(self):
        payloads = valid_payloads()
        self.assertEqual(validate_dto("CheckoutCandidateDTO", payloads["CheckoutCandidateDTO"])["path"], "/tmp/task")
        for name in ("TaskArtifactDTO", "TaskLifecycleDTO", "BranchBindingRefDTO", "ResultRefDTO"):
            with self.subTest(name=name), self.assertRaises(LifecycleContractError):
                validate_dto(name, {**payloads[name], "checkout_path": "/tmp/task"})

    def test_checkout_plan_has_a_closed_task_artifact_expectation(self):
        payload = valid_payloads()["CheckoutAcquisitionPlanDTO"]
        self.assertEqual(
            validate_dto("CheckoutAcquisitionPlanDTO", {**payload, "task_artifact_expectation": "absent"})[
                "task_artifact_expectation"
            ],
            "absent",
        )
        with self.assertRaises(LifecycleContractError):
            validate_dto("CheckoutAcquisitionPlanDTO", {**payload, "task_artifact_expectation": "optional"})

    def test_checkout_candidate_can_represent_detached_or_unreadable_live_facts(self):
        candidate = valid_payloads()["CheckoutCandidateDTO"]
        detached = {
            **candidate,
            "head": None,
            "branch_ref": None,
            "topology": "registered",
            "validation_state": "invalid_candidate",
            "reason_code": "detached_checkout",
        }
        self.assertEqual(validate_dto("CheckoutCandidateDTO", detached), detached)

    def test_checkout_candidate_reason_matches_validation_state(self):
        candidate = valid_payloads()["CheckoutCandidateDTO"]
        valid = [
            candidate,
            {**candidate, "topology": "primary"},
            {**candidate, "validation_state": "invalid_candidate", "reason_code": "detached_checkout"},
            {**candidate, "validation_state": "authority_conflict", "reason_code": "task_artifact_mismatch"},
        ]
        for payload in valid:
            with self.subTest(valid=payload["validation_state"]):
                self.assertEqual(validate_dto("CheckoutCandidateDTO", payload), payload)

        invalid = [
            {**candidate, "reason_code": "unexpected_reason"},
            {**candidate, "head": None},
            {**candidate, "branch_ref": None},
            {**candidate, "topology": "registered"},
            {**candidate, "dirty_paths": ["modified.txt"]},
            {**candidate, "validation_state": "invalid_candidate", "reason_code": None},
            {**candidate, "validation_state": "authority_conflict", "reason_code": None},
        ]
        for payload in invalid:
            with self.subTest(invalid=payload["validation_state"]), self.assertRaises(LifecycleContractError):
                validate_dto("CheckoutCandidateDTO", payload)

    def test_checkout_resolution_selection_matches_resolution_kind(self):
        resolution = valid_payloads()["CheckoutResolutionDTO"]
        valid = [
            resolution,
            {"resolution_kind": "selection_required", "reason_code": "no_candidates", "candidate_ids": []},
            {"resolution_kind": "selection_required", "reason_code": "multiple_candidates", "candidate_ids": ["candidate:1", "candidate:2"]},
            {"resolution_kind": "authority_conflict", "reason_code": "task_artifact_mismatch", "candidate_ids": []},
        ]
        for payload in valid:
            with self.subTest(valid=payload["resolution_kind"]):
                self.assertEqual(validate_dto("CheckoutResolutionDTO", payload), payload)

        invalid = [
            {**resolution, "selected_candidate_id": None},
            {**resolution, "candidate_ids": ["candidate:1"]},
            {"resolution_kind": "selection_required", "reason_code": "multiple_candidates"},
            {"resolution_kind": "selection_required", "reason_code": "multiple_candidates", "candidate_ids": [], "selected_candidate_id": None},
            {"resolution_kind": "authority_conflict", "reason_code": "task_artifact_mismatch"},
        ]
        for payload in invalid:
            with self.subTest(invalid=payload["resolution_kind"]), self.assertRaises(LifecycleContractError):
                validate_dto("CheckoutResolutionDTO", payload)

    def test_path_and_branch_primitives_reject_non_portable_values(self):
        payloads = valid_payloads()
        invalid = [
            ("TaskIdentityDTO", {**payloads["TaskIdentityDTO"], "task_ref": ".trellis/tasks/.."}),
            ("TaskCommitResultDTO", {**payloads["TaskCommitResultDTO"], "base_ref": "main."}),
            ("HandoffRefDTO", {**payloads["HandoffRefDTO"], "receipt_ref": ".trellis/receipts/result.json"}),
            ("HandoffRefDTO", {**payloads["HandoffRefDTO"], "receipt_ref": "refs/heads/topic"}),
        ]
        for name, payload in invalid:
            with self.subTest(name=name), self.assertRaises(LifecycleContractError):
                validate_dto(name, payload)

    def test_handoff_receipt_ref_is_bound_to_the_same_task_id(self):
        payload = valid_payloads()["HandoffRefDTO"]
        with self.assertRaisesRegex(LifecycleContractError, "dto_identity_mismatch"):
            validate_dto(
                "HandoffRefDTO",
                {**payload, "receipt_ref": "refs/heads/guru-task-lifecycle/another-task"},
            )

    def test_git_and_repository_primitives_use_closed_value_domains(self):
        payloads = valid_payloads()
        for task_id in ["task.lock", "task.", "task..child"]:
            with self.subTest(task_id=task_id), self.assertRaises(LifecycleContractError):
                validate_dto("TaskLifecycleDTO", {**payloads["TaskLifecycleDTO"], "task_id": task_id})
        self.assertEqual(
            validate_dto("TaskLifecycleDTO", {**payloads["TaskLifecycleDTO"], "task_id": "HEAD"})["task_id"],
            "HEAD",
        )
        for repo_ref in ["owner/repo.git", "../repo", "./repo", "owner/-repo"]:
            with self.subTest(repo_ref=repo_ref), self.assertRaises(LifecycleContractError):
                validate_dto("IssueRefDTO", {**payloads["IssueRefDTO"], "repo_ref": repo_ref})
        for branch_ref in [
            "task.lock",
            "foo/.bar",
            "foo.lock",
            "HEAD",
            "-foo",
            "guru-task-lifecycle/task-a",
            "refs/heads/guru-task-lifecycle/task-a",
        ]:
            with self.subTest(branch_ref=branch_ref), self.assertRaises(LifecycleContractError):
                validate_dto("TaskCommitResultDTO", {**payloads["TaskCommitResultDTO"], "base_ref": branch_ref})

    def test_state_fields_reject_unknown_values(self):
        payloads = valid_payloads()
        with self.assertRaises(LifecycleContractError):
            validate_dto(
                "TerminalFinishRefDTO",
                {**payloads["TerminalFinishRefDTO"], "cleanup_state": "cleanup_complete"},
            )
        with self.assertRaises(LifecycleContractError):
            validate_dto(
                "DeliveryReviewReadyDTO",
                {**payloads["DeliveryReviewReadyDTO"], "remaining_work_state": "unknown"},
            )

    def test_source_union_is_closed(self):
        payload = valid_payloads()["SourceCorrectionReadyDTO"]
        for source in [
            {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": True},
            {"kind": "no_issue", "number": 454},
            {"kind": "issue", "repo_ref": "https://github.com/castbox/guru-trellis", "number": 454},
        ]:
            with self.subTest(source=source), self.assertRaises(LifecycleContractError):
                validate_dto("SourceCorrectionReadyDTO", {**payload, "reviewed_source": source})

    def test_source_and_installed_copy_have_the_same_schema_identity(self):
        source = load_contract()
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / "contracts"
            shutil.copytree(CONTRACT_ROOT, installed)
            copied = load_contract(contract_root=installed)
        self.assertEqual(source["$id"], copied["$id"])
        self.assertEqual(source, copied)

    def test_loader_rejects_remote_parent_and_nested_schema_resources(self):
        invalid = [
            {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "invalid-1", "$ref": "https://example.com/schema"},
            {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "invalid-2", "$ref": "../outside.schema.json"},
            {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "invalid-3", "$defs": {"nested": {"$id": "nested", "type": "string"}}},
        ]
        for index, schema in enumerate(invalid):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "invalid.schema.json").write_text(json.dumps(schema), encoding="utf-8")
                with self.assertRaises(LifecycleContractError):
                    load_contract("invalid.schema.json", contract_root=root)


if __name__ == "__main__":
    unittest.main()
