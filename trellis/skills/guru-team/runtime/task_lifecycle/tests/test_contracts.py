from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.schema import CONTRACT_ROOT, dto_names, load_contract, validate_dto


TASK_ID = "454-task-lifecycle-state-model"
TASK_REF = ".trellis/tasks/09-20-454-task-lifecycle-state-model"
GENERATION = 0
COMMIT = "a" * 40
OTHER_COMMIT = "b" * 40
DIGEST = "c" * 64


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


class ContractTests(unittest.TestCase):
    def test_catalog_is_closed_and_every_named_dto_has_a_valid_example(self):
        payloads = valid_payloads()
        self.assertEqual(set(dto_names()), set(payloads))
        for name, payload in payloads.items():
            with self.subTest(name=name):
                self.assertEqual(validate_dto(name, payload), payload)
                with self.assertRaises(LifecycleContractError):
                    validate_dto(name, {**payload, "authorization": "confirmed"})

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
