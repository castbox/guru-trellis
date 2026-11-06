"""Public successor-candidate bindings; fixture judgments do not prove AI review."""
from __future__ import annotations

import importlib.util
import json
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

    def test_current_authoring_example_reaches_public_review(self):
        """Consume fixture authoring through real wrappers, without a native claim."""
        checked = self.flow.check()
        commit_input = {
            "profile": "delivery_committed_reentry", "mode": "workflow",
            "task_ref": self.flow.task_ref, "delivery_key": checked["delivery_key"],
            "check_result_id": checked["check_result_id"],
        }
        committed = self.flow.wrapper(
            "guru-create-task-commit", "invoke.sh", "--input",
            self.flow.write("example-commit.json", commit_input), "--owner-result",
            self.flow.write("example-commit-owner.json", {
                "status": "passed", "summary": "Fixture: retain the committed candidate.",
                "evidence": ["The actual current Check binds the existing commit."],
            }))
        self.assertEqual("committed", committed["exit_id"])
        public = {
            "profile": "delivery_branch_review", "mode": "workflow",
            "task_ref": committed["task_ref"], "delivery_key": committed["delivery_key"],
            "check_result_id": committed["check_result_id"],
            "base_ref": self.projection.resolve(committed["delivery_key"])["candidate"]["base_ref"],
            "branch_review_commit": committed["branch_review_commit"],
            "review_intent": "initial_review",
        }
        authoring = json.loads(
            (PACKAGE / "examples/authoring-delivery-passed-1.0.json").read_text())
        public_file = self.flow.write("example-review.json", public)
        recorded = self.flow.wrapper(
            "guru-review-branch", "review-branch.sh", "--task", committed["task_ref"],
            "--skill-input", public_file, "--semantic-review-file",
            self.flow.write("example-review-owner.json", authoring), "--typed-exit", "passed")
        self.assertFalse(recorded["formal_exit"])
        self.assertEqual("recorded", recorded["status"])
        self.assertEqual(committed["task_ref"], recorded["task_ref"])
        validated = self.flow.wrapper(
            "guru-review-branch", "check-review-gate.sh", "--task", committed["task_ref"],
            "--delivery-key", json.dumps(committed["delivery_key"]), "--expected-exit", "passed")
        self.assertFalse(validated["formal_exit"])
        self.assertEqual("owner_checkpoint_validated", validated["status"])
        self.assertEqual(committed["branch_review_commit"], validated["review_commit"])
        reviewed = self.flow.wrapper("guru-review-branch", "invoke.sh", "--input", public_file)
        self.assertEqual("passed", reviewed["exit_id"])
        self.assertEqual(committed["task_ref"], reviewed["task_ref"])
        self.assertEqual(committed["delivery_key"], reviewed["delivery_key"])
        self.assertEqual(committed["branch_review_commit"], reviewed["branch_review_commit"])
        stored = self.projection.resolve(committed["delivery_key"])["results"]["full_review"]
        self.assertEqual(reviewed["full_review_result_id"], stored["result_id"])
        self.assertEqual(checked["check_result_id"], stored["predecessor_result_id"])
        self.assertEqual(committed["branch_review_commit"], stored["candidate"]["head_ref"])
        self.assertEqual(public["base_ref"], stored["candidate"]["base_ref"])
        self.assertFalse(self.checkpoint().exists())

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
