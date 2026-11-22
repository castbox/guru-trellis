"""Real wrapper/store checks; semantic judgments and remote PR facts are fixtures."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


class PreservedProjectionTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location(
            "preserved_commit_fixture", PACKAGE.parent / "guru-create-task-commit/tests/test_committed_reentry.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.commit = module.CommittedReentryTest()
        self.commit.delivery_profile = "pull_request"
        self.commit.setUp()
        self.addCleanup(self.commit.doCleanups)
        self.flow = self.commit.fixture
        self.repo, self.projection, self.key = self.flow.repo, self.flow.projection, self.flow.key
        self.commit.restart_implementation()
        self.config = self.repo / ".trellis/guru-team/config.yml"
        self.config.parent.mkdir(parents=True, exist_ok=True)
        self.config.write_text("preserved_worktree_paths: []\n")
        self.lock = self.repo / "pubspec.lock"
        self.lock.write_text("committed dependency graph\n")
        self.flow.git("add", "pubspec.lock", ".trellis/guru-team/config.yml")
        self.flow.git("commit", "-qm", "capture dependency change in complete range")
        self.flow.head = self.flow.git("rev-parse", "HEAD").strip()
        self.base = self.projection.content_base(self.key)
        self.lock.write_text("index dependency projection\n")
        self.flow.git("add", "pubspec.lock")
        self.lock.write_text("worktree dependency projection\n")
        self.lock.chmod(0o755)
        self.public = {"profile": "delivery_branch_review", "mode": "workflow",
                       "task_ref": self.flow.task_ref, "delivery_key": self.key,
                       "base_ref": self.base, "branch_review_commit": self.flow.head,
                       "review_intent": "initial_review"}
        self.owner = json.loads((PACKAGE / "examples/authoring-delivery-passed-2.0.json").read_text())

    def preserve(self, *, indent=True):
        self.config.write_text("preserved_worktree_paths:\n" + ("  " if indent else "") + "- pubspec.lock\n")
        # Config belongs to this fixture's tracked setup, not its dirty projection.
        self.flow.git("add", ".trellis/guru-team/config.yml")
        self.flow.git("commit", "--only", "-qm", "configure exact preserved path", ".trellis/guru-team/config.yml")
        self.flow.head = self.flow.git("rev-parse", "HEAD").strip()
        self.public["branch_review_commit"] = self.flow.head

    def capture(self):
        value = self.projection.candidate(["app.txt", "pubspec.lock"], head_ref=self.flow.head, base_ref=self.base)
        self.projection.begin_check(self.key, value)
        return value

    def record(self, success=True):
        return self.flow.wrapper("guru-review-branch", "review-branch.sh", "--task", self.flow.task_ref,
            "--skill-input", self.flow.write("preserved-review.json", self.public),
            "--semantic-review-file", self.flow.write("preserved-owner.json", self.owner),
            "--typed-exit", "passed", success=success)

    def preserved_state(self):
        return (self.lock.read_bytes(), self.lock.stat().st_mode & 0o777,
                self.flow.git("ls-files", "--stage", "--", "pubspec.lock"), self.flow.git("rev-parse", "HEAD"))

    def test_preserved_projection_reentry_review_readiness_and_publication_store(self):
        self.preserve()
        before = self.preserved_state()
        self.assertEqual("pre_review_committed", self.commit.reentry({})["exit_id"])
        candidate = self.capture()
        self.assertIn("pubspec.lock", candidate["paths"])
        self.assertIn("pubspec.lock", self.flow.git("diff", "--name-only", self.base, self.flow.head).splitlines())
        self.record()
        checked = self.flow.wrapper("guru-review-branch", "check-review-gate.sh", "--task", self.flow.task_ref,
                                   "--delivery-key", json.dumps(self.key), "--expected-exit", "passed")
        self.assertEqual("passed", checked["typed_exit"])
        reviewed = self.flow.wrapper("guru-review-branch", "invoke.sh", "--input", self.flow.write("preserved-review.json", self.public))
        self.assertEqual("passed", reviewed["exit_id"])
        ready = self.flow.readiness(reviewed)
        self.assertEqual("ready", ready["exit_id"])
        # The real store verifies Candidate again; only GitHub transport is isolated.
        body = "Current fixture slice."
        with self.flow.provider_response(body=body):
            self.projection.apply({"api_version": "1.0", "operation": "record_publication", "key": self.key,
                "owner_role": "publication", "owner_id": "guru-test-publication", "expected_phase": "publishing",
                "result": {"result_id": "publication:preserved", "owner_id": "guru-test-publication",
                    "evidence": [self.projection.read_record()["accepted_scope"]], "profile": "pull_request",
                    "candidate": candidate, "repo_ref": "example/repo", "pr_number": 9,
                    "reviewed_head": self.flow.head, "target_ref": "main",
                    "publication_ref": {"locator": "https://github.com/example/repo/pull/9",
                                        "revision": "sha256:" + hashlib.sha256(body.encode()).hexdigest()}}})
        self.assertEqual(candidate, self.projection.resolve(self.key)["candidate"])
        self.assertEqual(before, self.preserved_state())
        self.assertEqual("publication:preserved", self.projection.resolve(self.key)["publication_result"]["result_id"])
        # A later ordinary projection change still invalidates the captured Candidate.
        self.lock.write_text("later dependency graph\n")
        with self.assertRaisesRegex(Exception, "candidate_mismatch|content bytes/modes changed"):
            self.projection._call(self.projection.api.delivery_store.verify_candidate, self.repo, candidate)

    def test_unindented_yaml_list_reaches_committed_reentry_and_review(self):
        self.preserve(indent=False)
        before = self.preserved_state()
        self.assertEqual("pre_review_committed", self.commit.reentry({})["exit_id"])
        self.capture()
        self.record()
        checked = self.flow.wrapper("guru-review-branch", "check-review-gate.sh", "--task", self.flow.task_ref,
                                   "--delivery-key", json.dumps(self.key), "--expected-exit", "passed")
        self.assertEqual("passed", checked["typed_exit"])
        reviewed = self.flow.wrapper("guru-review-branch", "invoke.sh", "--input", self.flow.write("preserved-review.json", self.public))
        self.assertEqual("passed", reviewed["exit_id"])
        self.assertEqual(before, self.preserved_state())

    def test_unconfigured_and_unlisted_source_dirty_still_block(self):
        self.assertEqual("stale_identity", self.commit.reentry({}, ok=False)["code"])
        self.config.unlink()
        self.assertEqual("stale_identity", self.commit.reentry({}, ok=False)["code"])
        self.config.write_text("preserved_worktree_paths: []\n")
        self.preserve()
        self.capture()
        (self.repo / "app.txt").write_text("uncommitted source change\n")
        self.assertEqual("stale_identity", self.record(success=False)["code"])
        # Reentry uses the same exclusion but retains its original stage checks.
        self.commit.restart_implementation()
        self.assertEqual("stale_identity", self.commit.reentry({}, ok=False)["code"])


if __name__ == "__main__":
    unittest.main()
