"""Public successor-candidate bindings; fixture judgments do not prove AI review."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]


class CandidateReuseTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location(
            "candidate_reuse_delivery_fixture",
            PACKAGE.parent / "guru-check-task/tests/test_delivery_flow.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.flow = module.DeliveryFlow()
        self.flow.setUp()
        self.addCleanup(self.flow.doCleanups)
        self.repo = self.flow.repo
        self.projection = self.flow.projection

    def restart(self, role, paths):
        from runtime.delivery_projection.adapter import authority_ref
        from runtime.delivery_projection.gates import rework

        rework(self.projection, self.flow.key, role, "implementation",
               authority_ref(self.repo / "requirements.md", self.repo), ["readiness"])
        self.flow.head = self.flow.git("rev-parse", "HEAD").strip()
        self.projection.begin_check(self.flow.key, self.projection.candidate(
            paths, head_ref=self.flow.head,
            base_ref=self.projection.content_base(self.flow.key)))

    def checkpoint(self):
        return (self.repo / ".trellis/.runtime/guru-team/owner-checkpoints/flow-task"
                / self.flow.key["delivery_id"] / "review-gate.json")

    def test_successor_review_uses_current_check_after_original_checkpoint_retired(self):
        (self.repo / "policy.md").write_text("Keep both task and target obligations.\n")
        (self.repo / "consumer.md").write_text("Consumer requires the policy obligations.\n")
        self.flow.git("add", "policy.md", "consumer.md")
        self.flow.git("commit", "-qm", "document current policy and consumer")
        self.restart("check", ["app.txt", "policy.md", "consumer.md"])
        checked = self.flow.check()
        prior = self.flow.full_review(checked)
        original = self.projection.resolve(self.flow.key)["results"]["full_review"]
        self.assertFalse(self.checkpoint().exists())
        self.assertEqual(original["candidate"]["head_ref"], prior["branch_review_commit"])

        # A legitimate documentation revision changes semantics. The fixture
        # authoring below only exercises recording after the AI-owned judgment.
        (self.repo / "policy.md").write_text(
            "Keep task and target obligations; preserve the existing consumer.\n")
        self.flow.git("add", "policy.md")
        self.flow.git("commit", "-qm", "combine policy obligations")
        self.restart("full_review", ["policy.md"])
        retained = self.projection.resolve(self.flow.key)["results"]["full_review"]
        self.assertEqual(original, retained)
        self.assertEqual("not_applicable", self.projection.gate_applicability(
            self.flow.key)["full_review"]["kind"])
        current_check = self.flow.check()
        stale = self.flow.wrapper(
            "guru-review-branch", "invoke.sh", "--input",
            str(self.flow.inputs / "review.json"), success=False)
        self.assertEqual("stale_identity", stale["code"])

        current = self.flow.full_review(current_check)
        result = self.projection.resolve(self.flow.key)["results"]["full_review"]
        self.assertNotEqual(prior["full_review_result_id"], current["full_review_result_id"])
        self.assertEqual(current_check["check_result_id"], result["predecessor_result_id"])
        self.assertEqual(self.flow.head, result["candidate"]["head_ref"])
        self.assertEqual(original["candidate"]["base_ref"], result["candidate"]["base_ref"])
        self.assertIn("consumer.md", result["candidate"]["paths"])
        self.assertFalse(self.checkpoint().exists())
        self.assertEqual("ready", self.flow.readiness(current)["exit_id"])
        self.assertEqual(self.flow.key, current["delivery_key"])

    def test_same_tree_commit_requires_current_binding_without_empty_followup_commit(self):
        checked = self.flow.check()
        prior = self.flow.full_review(checked)
        prior_tree = self.flow.git("rev-parse", "HEAD^{tree}").strip()
        # This is an actual same-content commit identity change, not a forged
        # candidate or an empty commit manufactured by the workflow.
        self.flow.git("-c", "commit.gpgsign=false", "commit", "--amend",
                      "-qm", "same content with corrected message")
        self.assertEqual(prior_tree, self.flow.git("rev-parse", "HEAD^{tree}").strip())
        self.assertNotEqual(prior["branch_review_commit"], self.flow.git("rev-parse", "HEAD").strip())
        self.restart("full_review", ["app.txt"])
        current_check = self.flow.check()
        public = {"profile": "delivery_committed_reentry", "mode": "workflow",
                  "task_ref": self.flow.task_ref, "delivery_key": self.flow.key,
                  "check_result_id": current_check["check_result_id"]}
        committed = self.flow.wrapper(
            "guru-create-task-commit", "invoke.sh", "--input",
            self.flow.write("same-tree-commit.json", public), "--owner-result",
            self.flow.write("same-tree-owner.json", {
                "status": "passed", "summary": "Fixture: current binding reviewed.",
                "evidence": ["Actual same tree and current public Check."]}))
        self.assertEqual(self.flow.head, committed["branch_review_commit"])
        self.assertEqual(self.flow.head, self.flow.git("rev-parse", "HEAD").strip())
        reviewed = self.flow.full_review(current_check)
        self.assertEqual(self.flow.head, reviewed["branch_review_commit"])
        self.assertFalse(self.checkpoint().exists())


if __name__ == "__main__":
    unittest.main()
