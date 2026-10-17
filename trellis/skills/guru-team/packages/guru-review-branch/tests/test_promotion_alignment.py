"""Real Git/public-owner bindings; fixture judgments do not prove AI review."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
sys.path.insert(0, str(SKILLS))
from runtime.delivery_projection.adapter import authority_ref
from runtime.delivery_projection.gates import rework


class PromotionAlignmentTest(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location(
            "alignment_delivery_fixture", PACKAGE.parent / "guru-check-task/tests/test_delivery_flow.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.flow = module.DeliveryFlow()
        self.flow.setUp()
        self.addCleanup(self.flow.doCleanups)
        self.repo = self.flow.repo
        self.projection = self.flow.projection
        self.paths = ["app.txt", "promotion.md", "source.md"]
        (self.repo / "promotion.md").write_text("Source: source.md; promoted in this branch.\n")
        (self.repo / "source.md").write_text("Status: promoted; see promotion.md.\n")
        self.flow.git("add", ".")
        self.flow.git("commit", "-qm", "add promotion reference fixture")
        self.restart_check("check")
        original = self.flow.full_review(self.flow.check())
        # Lost original stdout is recovered before rework from the actual
        # public result, after its original private checkpoint was retired.
        self.assertFalse(self.checkpoint().exists())
        self.prior = self.flow.wrapper("guru-review-branch", "invoke.sh", "--input",
            str(self.flow.inputs / "review.json"))
        self.assertEqual(original, self.prior)
        self.base = self.projection.content_base(self.flow.key)
        self.assertFalse(self.checkpoint().exists())
        (self.repo / "promotion.md").write_text("Promoted source: source.md (current branch).\n")
        (self.repo / "source.md").write_text("Status in current branch: promoted; source for promotion.md.\n")
        self.flow.git("add", ".")
        self.flow.git("commit", "-qm", "align promotion references")
        self.restart_check("full_review")
        self.current_check = self.flow.check()
        self.assertIsNone(self.projection.resolve(self.flow.key)["results"]["full_review"])

    def checkpoint(self):
        return (self.repo / ".trellis/.runtime/guru-team/owner-checkpoints/flow-task"
                / self.flow.key["delivery_id"] / "review-gate.json")

    def restart_check(self, role):
        reason = authority_ref(self.projection.planning_directory(self.flow.key) / "implement.md", self.repo)
        rework(self.projection, self.flow.key, role, "implementation", reason,
               ["check", "full_review", "readiness"])
        self.flow.head = self.flow.git("rev-parse", "HEAD").strip()
        self.projection.begin_check(self.flow.key, self.projection.candidate(
            self.paths, head_ref=self.flow.head, base_ref=self.projection.content_base(self.flow.key)))

    def public(self):
        return {
            "profile": "delivery_promotion_reference_alignment", "mode": "workflow",
            "task_ref": self.flow.task_ref, "delivery_key": self.flow.key,
            "base_ref": self.base, "branch_review_commit": self.flow.head,
            "check_result_id": self.current_check["check_result_id"],
            "prior_review": copy.deepcopy(self.prior), "prior_reviewed_base_head": self.base,
        }

    def record(self, public=None, status="passed", success=True):
        fixture = json.loads((PACKAGE / "examples/review-gate.json").read_text())
        auth = {key: fixture[key] for key in (
            "candidate_classifications", "semantic_review", "verification_evidence", "delivery_review")}
        auth["semantic_review"]["qualified_findings"] = []
        auth["semantic_review"]["ai_review_gate"] = {
            "status": status,
            "summary": (
                "Fixture judgment: original full range plus both reference changes and dependencies reviewed; no new fact or obligation."
                if status == "passed" else
                "Fixture owner stops narrow review: app behavior changed; original affected full review is required."
            ),
        }
        return self.flow.wrapper("guru-review-branch", "review-branch.sh",
            "--task", self.flow.task_ref, "--skill-input", self.flow.write("alignment.json", public or self.public()),
            "--semantic-review-file", self.flow.write("alignment-owner.json", auth),
            "--typed-exit", status, success=success)

    def invoke(self, public=None, success=True):
        return self.flow.wrapper("guru-review-branch", "invoke.sh", "--input",
            self.flow.write("alignment.json", public or self.public()), success=success)

    def test_actual_prior_output_cleared_slot_and_new_check_reach_delivery_consumer(self):
        self.record()
        gate = json.loads(self.checkpoint().read_text())
        delta = subprocess.run(["git", "diff", "--no-ext-diff", "--no-textconv", "--binary",
            "--full-index", "--no-renames", self.prior["branch_review_commit"], self.flow.head, "--"],
            cwd=self.repo, capture_output=True, check=True).stdout
        self.assertIn(b"promotion.md", delta)
        self.assertIn(b"source.md", delta)
        self.assertEqual(hashlib.sha256(delta).hexdigest(), gate["promotion_alignment"]["delta_sha256"])
        checked = self.flow.wrapper("guru-review-branch", "check-review-gate.sh", "--task",
            self.flow.task_ref, "--delivery-key", json.dumps(self.flow.key), "--expected-exit", "passed")
        self.assertFalse(checked["formal_exit"])
        reviewed = self.invoke()
        self.assertEqual("passed", reviewed["exit_id"])
        self.assertNotEqual(self.prior["full_review_result_id"], reviewed["full_review_result_id"])
        stored = self.projection.resolve(self.flow.key)["results"]["full_review"]
        self.assertEqual(self.current_check["check_result_id"], stored["predecessor_result_id"])
        self.assertEqual(self.flow.head, stored["candidate"]["head_ref"])
        self.assertFalse(self.checkpoint().exists())
        self.assertEqual(reviewed, self.invoke())  # Output-loss recovery uses current public result.
        self.assertEqual("ready", self.flow.readiness(reviewed)["exit_id"])

    def test_normal_wrong_base_missing_result_and_stale_check_do_not_record(self):
        for key in ("prior_reviewed_base_head", "prior_review", "check_result_id"):
            with self.subTest(field=key):
                public = self.public()
                if key == "prior_review":
                    public.pop(key)  # Normal lost original result cannot be reconstructed.
                elif key == "check_result_id":
                    public[key] = "check:previous-candidate"
                else:
                    public[key] = self.prior["branch_review_commit"]
                self.record(public, success=False)
                self.assertFalse(self.checkpoint().exists())

    def test_candidate_advance_after_owner_review_stops_checker_and_invoke(self):
        self.record()
        (self.repo / "source.md").write_text("A later factual change requires its original owner.\n")
        self.flow.git("commit", "-qam", "later candidate change")
        self.flow.wrapper("guru-review-branch", "check-review-gate.sh", "--task", self.flow.task_ref,
            "--delivery-key", json.dumps(self.flow.key), success=False)
        self.invoke(success=False)
        self.assertTrue(self.checkpoint().exists())

    def test_owner_stop_for_real_behavior_delta_does_not_publish_a_new_full_review(self):
        (self.repo / "app.txt").write_text("A new behavior requires complete review.\n")
        self.flow.git("commit", "-qam", "change implementation behavior")
        self.restart_check("full_review")
        self.current_check = self.flow.check()
        self.record(status="blocked")
        self.assertEqual({"exit_id": "blocked"}, self.invoke())
        self.assertIsNone(self.projection.resolve(self.flow.key)["results"]["full_review"])
        self.assertFalse(self.checkpoint().exists())


if __name__ == "__main__":
    unittest.main()
