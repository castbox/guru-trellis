"""Run the #636 original migration command against real public Delivery state.

Schema 1.0 data here is a prior producer's normal pending or completed action.
The provider executable supplies read-only local PR facts, not GitHub proof.
"""
import importlib.util
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]


class CurrentTransactionMigrationTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location(
            "current_publication_migration_flow",
            SKILLS / "packages/guru-check-task/tests/test_delivery_flow.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.flow = module.DeliveryFlow()
        self.flow.delivery_profile = "pull_request"
        self.flow.setUp()
        self.addCleanup(self.flow.doCleanups)
        self.repo = self.flow.repo
        ready = self.flow.readiness(self.flow.full_review(self.flow.check()))
        self.source = {
            "profile": "delivery_review_ready", "mode": "workflow",
            "task_ref": self.flow.task_ref, "delivery_key": self.flow.key,
            "readiness_result_id": ready["readiness_result_id"],
            "reviewed_head": self.flow.head, "pr_title": ready["pr_title"],
            "pr_body": ready["pr_body"], "remaining_work_state": ready["remaining_work_state"],
        }
        _package, self.owner = self.flow.load_owner(PACKAGE.name)
        self.ref = self.owner.transaction_ref(self.source)
        self.path = self.owner.transaction_path(self.repo, self.ref)
        self.pr = {
            "number": 9, "url": "https://github.com/example/repo/pull/9",
            "state": "OPEN", "isDraft": True, "headRefOid": self.flow.head,
            "headRefName": "feat/flow", "baseRefName": "main",
            "headRepositoryOwner": {"login": "example"},
            "title": self.source["pr_title"], "body": self.source["pr_body"],
            "mergeCommit": None,
        }
        self.flow.git("remote", "add", "origin", "https://github.com/example/repo.git")
        self.bin = self.repo / ".trellis/.runtime/current-migration-provider"
        self.bin.mkdir()
        self.calls = self.bin / "calls.jsonl"
        self.pr_path = self.bin / "pr.json"
        self.pr_path.write_text(json.dumps(self.pr))
        provider = self.bin / "gh"
        provider.write_text(
            "#!" + sys.executable + "\nimport json,sys\nfrom pathlib import Path\n"
            "args=sys.argv[1:]\n"
            "with Path(" + repr(str(self.calls)) + ").open('a') as f: f.write(json.dumps(args)+'\\n')\n"
            "if args[:2]==['repo','view']: print(json.dumps({'nameWithOwner':'example/repo'}))\n"
            "elif args[:2]==['pr','view']: print(Path(" + repr(str(self.pr_path)) + ").read_text())\n"
            "else: sys.exit(31)\n"
        )
        provider.chmod(0o755)
        environment = patch.dict(os.environ, {"PATH": str(self.bin) + os.pathsep + os.environ["PATH"]})
        environment.start()
        self.addCleanup(environment.stop)

    def prior_transaction(self, stage):
        # This is the supported original 1.0 format, with the actual current
        # public key/readiness/candidate and the original mutation decisions.
        state = {
            "schema_version": "1.0", "skill_id": PACKAGE.name,
            "transaction_ref": self.ref, "stage": stage, "input": self.source,
            "public_candidate": self.flow.projection.resolve(self.flow.key)["candidate"],
            "repo_ref": "example/repo", "base_branch": "main", "head_branch": "feat/flow",
            "reviewed_head": self.flow.head, "initial_remote_head": None, "candidate_pr": None,
            "bound_pr": {"number": 9, "url": self.pr["url"], "head_sha": self.flow.head},
            "decisions": {
                "push_required": True, "create_pr_required": True,
                "metadata": {"original_title": self.source["pr_title"],
                    "original_body_sha256": self.owner.hashlib.sha256(self.source["pr_body"].encode()).hexdigest(),
                    "title_matches": True, "body_matches": True, "mutation_required": False},
                "ready": {"original_is_draft": True, "mutation_required": True},
            },
        }
        self.owner.save_transaction(self.repo, state)
        return state

    def migration_arguments(self):
        public = {"profile": "publication_transaction_636", "transaction_ref": self.ref,
                  "task_ref": self.flow.task_ref, "delivery_key": self.flow.key}
        review = {"status": "passed", "summary": "Original owner reviewed the same current transaction and actual PR facts.",
                  "evidence": ["Original action, stage, public identity, candidate and mutation decisions."]}
        return ("--input", self.flow.write("current-migration.json", public),
                "--owner-result", self.flow.write("current-migration-review.json", review))

    def migrate(self, original):
        args = self.migration_arguments()
        private_before = self.path.read_bytes()
        task_path = self.repo / self.flow.task_ref / "task.json"
        task_before = task_path.read_bytes()
        preview = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", *args, "--preview")
        self.assertEqual("preview", preview["status"])
        self.assertEqual(private_before, self.path.read_bytes())
        result = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", *args)
        self.assertEqual("transaction_bound", result["status"])
        self.assertEqual(task_before, task_path.read_bytes())
        migrated = json.loads(self.path.read_text())
        self.assertEqual("2.0", migrated["schema_version"])
        self.assertEqual(("ready", "ready"), (migrated["action"], migrated["terminal"]))
        for field, value in original.items():
            if field not in {"schema_version", "transaction_sha256"}:
                self.assertEqual(value, migrated[field], field)
        self.assertEqual("already_bound", self.flow.wrapper(
            PACKAGE.name, "migrate-delivery-transaction.sh", *args)["status"])
        self.assertEqual(task_before, task_path.read_bytes())
        self.assert_reads_only()
        return migrated

    def assert_reads_only(self):
        calls = [json.loads(line) for line in self.calls.read_text().splitlines()]
        self.assertTrue(calls)
        self.assertTrue(all(row[:2] in (["repo", "view"], ["pr", "view"]) for row in calls))
        self.assertEqual(self.flow.head, self.flow.git("rev-parse", "HEAD").strip())

    def rework_to_implementation(self):
        from runtime.delivery_projection.adapter import authority_ref
        from runtime.delivery_projection.gates import rework
        rework(self.flow.projection, self.flow.key, "publication", "implementation",
               authority_ref(self.flow.projection.planning_directory(self.flow.key) / "implement.md", self.repo),
               ["check", "full_review", "readiness"])

    def test_pending_ready_conversion_preserves_stage_and_actual_current_readiness(self):
        original = self.prior_transaction("mark_ready")
        before = self.flow.projection.resolve(self.flow.key)
        migrated = self.migrate(original)
        self.assertEqual("mark_ready", migrated["stage"])
        self.assertEqual(before, self.flow.projection.resolve(self.flow.key))
        self.assertIsNone(before["publication_result"])

    def test_completed_ready_conversion_and_lost_output_readback_do_not_invent_gates(self):
        self.pr["isDraft"] = False
        self.pr_path.write_text(json.dumps(self.pr))
        original = self.prior_transaction("ready")
        self.rework_to_implementation()
        self.migrate(original)
        self.assertIsNone(self.flow.projection.resolve(self.flow.key)["publication_result"])
        public = {"profile": "delivery_same_plan_resume", "mode": "workflow", "task_ref": self.flow.task_ref,
                  "delivery_key": self.flow.key, "transaction_ref": self.ref}
        review = {"schema_version": "1.0", "skill_id": PACKAGE.name,
                  "review": {"status": "passed", "summary": "Recover the original Ready fact; current gates remain absent."},
                  "route": {"typed_exit": "ready_for_merge"}}
        args = ("--input", self.flow.write("current-resume.json", public),
                "--review-input", self.flow.write("current-resume-review.json", review))
        first = self.flow.wrapper(PACKAGE.name, "invoke.sh", *args)
        self.assertEqual("review_stale", first["exit_id"])
        self.assertEqual(first, self.flow.wrapper(PACKAGE.name, "invoke.sh", *args))
        selected = self.flow.projection.resolve(self.flow.key)
        self.assertEqual("implementing", selected["phase"])
        self.assertIsNotNone(selected["publication_result"])
        for role in ("check", "full_review", "readiness"):
            self.assertIsNone(selected["results"][role])
        self.assert_reads_only()

    def test_pending_conversion_without_current_readiness_returns_to_original_owner(self):
        self.prior_transaction("mark_ready")
        self.rework_to_implementation()
        private_before = self.path.read_bytes()
        task_before = (self.repo / self.flow.task_ref / "task.json").read_bytes()
        result = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh",
                                   *self.migration_arguments(), success=False)
        self.assertEqual("publication_stale", result["code"])
        self.assertEqual(private_before, self.path.read_bytes())
        self.assertEqual(task_before, (self.repo / self.flow.task_ref / "task.json").read_bytes())
        self.assert_reads_only()


if __name__ == "__main__":
    unittest.main()
