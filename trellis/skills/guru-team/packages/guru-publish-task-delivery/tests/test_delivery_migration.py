"""Bounded original publication migration with installed public fact checks.

The provider fixture is local; these checks do not claim remote publication.
"""
import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]


class PublicationMigrationTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("publication_migration_flow", SKILLS / "packages/guru-check-task/tests/test_delivery_flow.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.flow = module.DeliveryFlow()
        self.flow.setUp()
        self.addCleanup(self.flow.doCleanups)
        self.repo = self.flow.repo
        self.key = {**self.flow.key, "delivery_id": "e14a82d9-6185-4941-9a46-24809c1e8621"}
        projection = self.flow.projection
        record = projection.read_record()
        projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": self.key, "owner_role": "creation", "owner_id": "guru-test-creation", "scope_ref": {"authority": record["accepted_scope"], "anchors": ["R1"]}, "profile": "pull_request"})
        self.flow.git("remote", "add", "origin", "https://github.com/example/repo.git")
        self.cycle = "delivery-cycle:v1:" + "a" * 64
        self.ref = "b" * 64
        self.body = "Refs #9"
        self.source = {"profile": "review_ready", "mode": "workflow", "task_ref": self.flow.task_ref, "delivery_cycle_ref": self.cycle, "reviewed_head": self.flow.head, "pr_title": "交付已存在成果", "pr_body": self.body, "remaining_work_state": "remaining"}
        self.path = self.repo / ".trellis/.runtime/guru-team/guru-publish-task-delivery" / (self.ref + ".json")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.state = {"schema_version": "1.0", "skill_id": PACKAGE.name, "transaction_ref": self.ref, "stage": "ready", "input": self.source, "repo_ref": "example/repo", "base_branch": "main", "head_branch": "feat/flow", "reviewed_head": self.flow.head, "initial_remote_head": None, "candidate_pr": None, "bound_pr": {"number": 9}, "decisions": {"push_required": True, "create_pr_required": True, "metadata": None, "ready": None}}
        _package, owner = self.flow.load_owner(PACKAGE.name)
        self.state["transaction_sha256"] = owner.digest(self.state)
        self.path.write_text(json.dumps(self.state))
        self.pr = {"number": 9, "url": "https://github.com/example/repo/pull/9", "state": "OPEN", "isDraft": False, "headRefOid": self.flow.head, "headRefName": "feat/flow", "baseRefName": "main", "headRepositoryOwner": {"login": "example"}, "title": self.source["pr_title"], "body": self.body, "mergeCommit": None}
        self.bin = self.repo / ".trellis/.runtime/provider-bin"
        self.bin.mkdir()
        self.calls = self.bin / "calls.jsonl"
        provider = self.bin / "gh"
        provider.write_text("#!" + sys.executable + "\nimport json,sys\nfrom pathlib import Path\nargs=sys.argv[1:]\nwith Path(" + repr(str(self.calls)) + ").open('a') as f: f.write(json.dumps(args)+'\\n')\nif args[:2]==['repo','view']: print(json.dumps({'nameWithOwner':'example/repo'}))\nelif args[:2]==['pr','view']: print(" + repr(json.dumps(self.pr)) + ")\nelse: sys.exit(31)\n")
        provider.chmod(0o755)
        self.environment = patch.dict(os.environ, {"PATH": str(self.bin) + os.pathsep + os.environ["PATH"]})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def migrate(self):
        value = {"profile": "historical_publication_migration", "transaction_ref": self.ref, "delivery_cycle_ref": self.cycle, "delivery_key": self.key, "candidate": self.flow.projection.resolve(self.flow.key)["candidate"]}
        review = {"status": "passed", "summary": "Original owner verified exact old cycle attribution.", "evidence": ["Actual original Task/candidate/PR payload and Ready stage."]}
        args = ("--input", self.flow.write("migration.json", value), "--owner-result", self.flow.write("migration-review.json", review))
        before = self.path.read_bytes()
        preview = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", *args, "--preview")
        self.assertEqual("preview", preview["status"])
        self.assertEqual(before, self.path.read_bytes())
        return self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", *args)

    def test_incomplete_transaction_requires_fresh_real_readiness_before_binding(self):
        _package, owner = self.flow.load_owner(PACKAGE.name)
        state = {**self.state, "stage": "converge_metadata"}
        owner.save_transaction(self.repo, state)
        before = self.path.read_bytes()
        current = {**self.source, "profile": "delivery_review_ready", "delivery_key": self.key, "readiness_result_id": "readiness:lost"}
        current.pop("delivery_cycle_ref")
        public = {"profile": "inflight_publication_migration", "transaction_ref": self.ref, "delivery_cycle_ref": self.cycle, "delivery_key": self.key, "current_input": current}
        review = {"status": "passed", "summary": "Restore exact original incomplete transaction; gate absent.", "evidence": ["Actual PR/Task association; original retry stage."]}
        result = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", "--input", self.flow.write("migration.json", public), "--owner-result", self.flow.write("migration-review.json", review), success=False)
        self.assertEqual("publication_stale", result["code"])
        self.assertEqual(before, self.path.read_bytes())

    def test_ready_history_migrates_without_readiness_pass_or_remote_mutation(self):
        before = self.flow.projection.resolve(self.key)
        self.assertEqual("transaction_bound", self.migrate()["status"])
        self.assertEqual("already_bound", self.migrate()["status"])
        state = json.loads(self.path.read_text())
        self.assertEqual(self.ref, state["transaction_ref"])
        self.assertEqual("ready", state["stage"])
        self.assertEqual(self.state["decisions"], state["decisions"])
        self.assertIsNone(state["input"]["readiness_result_id"])
        self.assertEqual(before, self.flow.projection.resolve(self.key))
        public = {"profile": "delivery_same_plan_resume", "mode": "workflow", "task_ref": self.flow.task_ref, "delivery_key": self.key, "transaction_ref": self.ref}
        review = {"schema_version": "1.0", "skill_id": PACKAGE.name, "review": {"status": "passed", "summary": "Recover actual successful publication; current readiness absent."}, "route": {"typed_exit": "ready_for_merge"}}
        output = self.flow.wrapper(PACKAGE.name, "invoke.sh", "--input", self.flow.write("resume.json", public), "--review-input", self.flow.write("resume-review.json", review))
        self.assertEqual("review_stale", output["exit_id"])
        current = self.flow.projection.resolve(self.key)
        self.assertIsNotNone(current["publication_result"])
        self.assertIsNone(current["results"]["readiness"])
        self.assertEqual("planning", current["phase"])
        self.assertEqual(self.flow.head, self.flow.git("rev-parse", "HEAD").strip())
        self.assertTrue(all(json.loads(line)[:2] in (["repo", "view"], ["pr", "view"]) for line in self.calls.read_text().splitlines()))
