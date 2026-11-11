"""Current public Review producer; semantic inputs are fixtures, not AI evidence."""
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


class PostcommitReviewTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("postcommit_flow", PACKAGE.parent / "guru-check-task/tests/test_delivery_flow.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.flow = module.DeliveryFlow()
        self.flow.setUp()
        self.addCleanup(self.flow.doCleanups)
        self.repo = self.flow.repo
        self.projection = self.flow.projection
        self.public = {"profile": "delivery_branch_review", "mode": "workflow",
                       "task_ref": self.flow.task_ref, "delivery_key": self.flow.key,
                       "base_ref": self.projection.content_base(self.flow.key),
                       "branch_review_commit": self.flow.head, "review_intent": "initial_review"}
        self.authoring = json.loads((PACKAGE / "examples/authoring-delivery-passed-2.0.json").read_text())

    def record(self, exit_id="passed", *, success=True):
        self.authoring["semantic_review"]["ai_review_gate"]["status"] = exit_id
        return self.flow.wrapper("guru-review-branch", "review-branch.sh", "--task", self.flow.task_ref,
                                 "--skill-input", self.flow.write("review.json", self.public),
                                 "--semantic-review-file", self.flow.write("owner.json", self.authoring),
                                 "--typed-exit", exit_id, success=success)

    def invoke(self, public=None, success=True):
        return self.flow.wrapper("guru-review-branch", "invoke.sh", "--input",
                                 self.flow.write("review.json", public or self.public), success=success)

    def checkpoint(self):
        return (self.repo / ".trellis/.runtime/guru-team/owner-checkpoints/flow-task" /
                self.flow.key["delivery_id"] / "review-gate.json")

    def test_first_review_without_check_records_two_real_predecessors_and_recovers_output(self):
        self.assertIsNone(self.projection.resolve(self.flow.key)["results"]["check"])
        self.record()
        result = self.invoke()
        self.assertEqual("passed", result["exit_id"])
        results = self.projection.resolve(self.flow.key)["results"]
        self.assertEqual("planning:flow", results["check"]["predecessor_result_id"])
        self.assertEqual(results["check"]["result_id"], results["full_review"]["predecessor_result_id"])
        self.assertEqual(result["full_review_result_id"], results["full_review"]["result_id"])
        self.assertEqual(results["check"]["candidate"], results["full_review"]["candidate"])
        self.assertEqual("guru-review-branch", results["check"]["owner_id"])
        self.assertFalse(self.checkpoint().exists())
        self.assertEqual(result, self.invoke())

    def test_missing_full_review_projection_retries_original_semantic_result(self):
        # Stop at the actual public API boundary after the first successful
        # projection. This is ordinary missing-output recovery, not forged state.
        import sys
        sys.path.insert(0, str(PACKAGE / "runtime"))
        from delivery_review import result_id
        from runtime.delivery_projection.gates import record_gate
        from runtime.delivery_projection.adapter import authority_ref
        self.record()
        owner = json.loads(self.checkpoint().read_text())
        check_id = result_id(owner, "check")
        record_gate(self.projection, self.flow.key, "check", check_id,
                    owner["gate_judgments"]["check"]["outcome"],
                    [authority_ref(self.projection.planning_directory(self.flow.key) / "implement.md", self.repo)], [])
        self.assertIsNone(self.projection.resolve(self.flow.key)["results"]["full_review"])
        result = self.invoke()
        self.assertEqual("passed", result["exit_id"])
        self.assertEqual(check_id, self.projection.resolve(self.flow.key)["results"]["check"]["result_id"])
        self.assertEqual(result, self.invoke())

    def test_missing_semantic_result_never_supplies_missing_full_review(self):
        from runtime.delivery_projection.gates import record_gate
        from runtime.delivery_projection.adapter import authority_ref
        record_gate(self.projection, self.flow.key, "check", "check:completed-fixture",
                    "passed", [authority_ref(self.projection.planning_directory(self.flow.key) / "implement.md", self.repo)], [])
        result = self.invoke(success=False)
        self.assertEqual("stale_identity", result["code"])
        self.assertIsNone(self.projection.resolve(self.flow.key)["results"]["full_review"])

    def test_incomplete_nine_dimensions_cannot_record_pass(self):
        del self.authoring["adequacy_review"]["tests"]
        result = self.flow.wrapper("guru-review-branch", "review-branch.sh", "--task", self.flow.task_ref,
                                  "--skill-input", self.flow.write("review.json", self.public),
                                  "--semantic-review-file", self.flow.write("owner.json", self.authoring),
                                  "--typed-exit", "passed", success=False)
        self.assertEqual("schema_mismatch", result["code"])
        self.assertIsNone(self.projection.resolve(self.flow.key)["results"]["check"])

    def test_successor_keeps_fixed_base_and_full_consumer_coverage(self):
        prior = self.flow.single_review()
        from runtime.delivery_projection.gates import rework
        from runtime.delivery_projection.adapter import authority_ref
        rework(self.projection, self.flow.key, "full_review", "implementation",
               authority_ref(self.repo / "requirements.md", self.repo), ["readiness"])
        (self.repo / "consumer.txt").write_text("A new consumer depends on the task behavior.\n")
        self.flow.git("add", "consumer.txt")
        self.flow.git("commit", "-qm", "include consumer")
        head = self.flow.git("rev-parse", "HEAD").strip()
        self.projection.begin_check(self.flow.key, self.projection.candidate(["consumer.txt"], head_ref=head, base_ref=self.public["base_ref"]))
        self.assertEqual("stale_identity", self.invoke(success=False)["code"])
        self.public["branch_review_commit"] = head
        self.public["review_intent"] = "fresh_final_review"
        self.record()
        result = self.invoke()
        current = self.projection.resolve(self.flow.key)
        self.assertNotEqual(prior["full_review_result_id"], result["full_review_result_id"])
        self.assertEqual(self.public["base_ref"], current["candidate"]["base_ref"])
        self.assertIn("app.txt", current["candidate"]["paths"])
        self.assertIn("consumer.txt", current["candidate"]["paths"])

    def test_planning_rollback_handoff_recovers_without_second_rework(self):
        self.authoring["planning_revision"] = {"planning_route": "reapprove_plan", "proposal_refs": [],
                                               "revision_actions": ["Repair the missing design condition within accepted R1."]}
        self.record("planning_stale")
        output = self.invoke()
        self.assertEqual("planning_stale", output["exit_id"])
        self.assertEqual(self.authoring["planning_revision"]["revision_actions"], output["revision_actions"])
        before = (self.repo / self.flow.task_ref / "task.json").read_bytes()
        recovered = self.invoke({"profile": "delivery_planning_stale_recovery", "mode": "workflow",
                                 "task_ref": self.flow.task_ref, "delivery_key": self.flow.key,
                                 "original_review_input": self.public})
        self.assertEqual(output, recovered)
        self.assertEqual(before, (self.repo / self.flow.task_ref / "task.json").read_bytes())
        self.assertTrue(all(self.projection.resolve(self.flow.key)["results"][name] is None for name in ["planning", "check", "full_review", "readiness"]))

    def prepare_continuity(self):
        prior = self.flow.single_review()
        from runtime.delivery_projection.gates import rework
        from runtime.delivery_projection.adapter import authority_ref
        import sys
        sys.path.insert(0, str(PACKAGE / "runtime"))
        from common import tree_identity
        old_base = self.public["base_ref"]
        self.flow.git("add", self.flow.task_ref)
        self.flow.git("commit", "-qm", "retain real review facts")
        self.flow.git("switch", "main")
        (self.repo / "base-only.txt").write_text("Independent base behavior.\n")
        self.flow.git("add", "base-only.txt")
        self.flow.git("commit", "-qm", "advance base")
        new_base = self.flow.git("rev-parse", "HEAD").strip()
        self.flow.git("switch", "feat/flow")
        self.flow.git("merge", "--no-ff", "-m", "integrate base", "main")
        head = self.flow.git("rev-parse", "HEAD").strip()
        rework(self.projection, self.flow.key, "full_review", "implementation",
               authority_ref(self.repo / "requirements.md", self.repo), ["check", "full_review", "readiness"])
        self.projection.begin_check(self.flow.key, self.projection.candidate(["app.txt"], head_ref=head, base_ref=old_base))
        self.public = {"profile": "delivery_base_continuity", "mode": "workflow",
                       "task_ref": self.flow.task_ref, "delivery_key": self.flow.key,
                       "task_head": head, "branch_review_commit": prior["branch_review_commit"],
                       "old_base_head": old_base, "new_base_head": new_base,
                       "candidate_tree_sha256": tree_identity(self.repo, head),
                       "relevant_paths": ["base-only.txt"], "resume_target": "publication_review",
                       "review_intent": "base_continuity"}
        return old_base

    def test_bounded_continuity_without_check_does_not_manufacture_full_review(self):
        old_base = self.prepare_continuity()
        self.record("continuity_passed")
        bounded = self.invoke()
        self.assertEqual("continuity_passed", bounded["exit_id"])
        self.assertIsNone(self.projection.resolve(self.flow.key)["results"]["check"])
        self.assertIsNone(self.projection.resolve(self.flow.key)["results"]["full_review"])
        self.assertEqual(old_base, self.projection.resolve(self.flow.key)["candidate"]["base_ref"])

    def test_bounded_continuity_blocked_runs_record_check_invoke_without_pass_slots(self):
        self.prepare_continuity()
        task_file = self.repo / self.flow.task_ref / "task.json"
        before = task_file.read_bytes()
        candidate = self.projection.resolve(self.flow.key)["candidate"]
        self.authoring["semantic_review"]["ai_review_gate"]["summary"] = (
            "Fixture: required original integration evidence is unavailable; bounded review stops.")
        recorded = self.record("blocked")
        self.assertFalse(recorded["formal_exit"])
        checked = self.flow.wrapper("guru-review-branch", "check-review-gate.sh",
            "--task", self.flow.task_ref, "--delivery-key", json.dumps(self.flow.key),
            "--expected-exit", "blocked")
        self.assertFalse(checked["formal_exit"])
        self.assertEqual("blocked", checked["typed_exit"])
        self.assertEqual({"exit_id": "blocked"}, self.invoke())
        delivery = self.projection.resolve(self.flow.key)
        self.assertEqual("checking", delivery["phase"])
        self.assertIsNone(delivery["results"]["check"])
        self.assertIsNone(delivery["results"]["full_review"])
        self.assertEqual(candidate, delivery["candidate"])
        self.assertEqual(before, task_file.read_bytes())
        self.assertFalse(self.checkpoint().exists())

    def test_passing_exits_remain_specific_to_their_review_profiles(self):
        result = self.record("continuity_passed", success=False)
        self.assertEqual("schema_mismatch", result["code"])
        self.assertEqual("typed_exit", result["field_path"])
        self.assertFalse(self.checkpoint().exists())
        self.prepare_continuity()
        result = self.record("passed", success=False)
        self.assertEqual("schema_mismatch", result["code"])
        self.assertEqual("typed_exit", result["field_path"])
        self.assertFalse(self.checkpoint().exists())
        delivery = self.projection.resolve(self.flow.key)
        self.assertIsNone(delivery["results"]["check"])
        self.assertIsNone(delivery["results"]["full_review"])

    def test_scope_withdrawal_from_checking_uses_same_review_owner_and_recovers(self):
        from runtime.delivery_projection.adapter import authority_ref
        reason = authority_ref(self.repo / "requirements.md", self.repo)
        public = {"profile": "delivery_scope_withdrawal", "mode": "workflow",
                  "task_ref": self.flow.task_ref, "delivery_key": self.flow.key}
        semantic = {"reviewed_delivery_key": self.flow.key, "result_id": "stop:fixture",
                    "reason": reason, "scope_decision": reason, "evidence": [reason]}
        entry = ("--input", self.flow.write("withdrawal.json", public), "--owner-result",
                 self.flow.write("withdrawal-owner.json", semantic))
        output = self.flow.wrapper("guru-review-branch", "invoke.sh", *entry)
        self.assertEqual("delivery_stopped", output["exit_id"])
        self.assertEqual("stopped", self.projection.resolve(self.flow.key)["phase"])
        self.assertEqual(self.flow.head, self.flow.git("rev-parse", "HEAD").strip())
        self.assertEqual(output, self.flow.wrapper("guru-review-branch", "invoke.sh", *entry))

    def test_retired_old_normal_calls_and_checkpoint_cannot_emit_a_pass(self):
        legacy_ref = ".trellis/tasks/old-normal-fixture"
        directory = self.repo / legacy_ref
        directory.mkdir(parents=True)
        (directory / "task.json").write_text(json.dumps({
            "id": "old-normal-fixture", "status": "in_progress", "branch": "feat/flow", "base_branch": "main"}))
        task_file = self.repo / self.flow.task_ref / "task.json"
        before = task_file.read_bytes()
        for profile in ("branch_review", "base_continuity"):
            with self.subTest(profile=profile):
                old = {**self.public, "profile": profile, "task_ref": legacy_ref}
                old.pop("delivery_key")
                source = self.flow.write("old-normal-input.json", old)
                recorded = self.flow.wrapper("guru-review-branch", "review-branch.sh",
                    "--task", legacy_ref, "--skill-input", source,
                    "--semantic-review-file", self.flow.write("old-normal-owner.json", self.authoring),
                    "--typed-exit", "passed", success=False)
                self.assertEqual("schema_mismatch", recorded["code"])
                self.assertIn("MIGRATION-794", recorded["remediation"])
                invoked = self.flow.wrapper("guru-review-branch", "invoke.sh", "--input", source, success=False)
                self.assertEqual("schema_mismatch", invoked["code"])
                self.assertIn("MIGRATION-794", invoked["remediation"])
        # Historical reader precondition only: an existing schema7 checkpoint
        # does not become current authority or prove its retired producer.
        old_checkpoint = (self.repo / ".trellis/.runtime/guru-team/owner-checkpoints" /
                          "old-normal-fixture/review-gate.json")
        old_checkpoint.parent.mkdir(parents=True)
        historical = json.loads((PACKAGE / "examples/review-gate.json").read_text())
        historical["task_dir"] = legacy_ref
        old_checkpoint.write_text(json.dumps(historical))
        checked = self.flow.wrapper("guru-review-branch", "check-review-gate.sh", "--task", legacy_ref, success=False)
        self.assertEqual("stale_identity", checked["code"])
        self.assertIn("MIGRATION-794", checked["remediation"])
        self.assertEqual(before, task_file.read_bytes())
        self.assertIsNone(self.projection.resolve(self.flow.key)["results"]["check"])
        self.assertIsNone(self.projection.resolve(self.flow.key)["results"]["full_review"])


if __name__ == "__main__":
    unittest.main()
