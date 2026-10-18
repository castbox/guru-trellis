"""Original schema-1 message survives installed historical projection/retry.

Provider outputs are fixtures, not remote merge evidence.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]


class MergeMigrationTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("merge_migration_flow", SKILLS / "packages/guru-check-task/tests/test_delivery_flow.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.flow = module.DeliveryFlow()
        self.flow.setUp()
        self.addCleanup(self.flow.doCleanups)
        self.repo = self.flow.repo
        self.key = {**self.flow.key, "delivery_id": "e14a82d9-6185-4941-9a46-24809c1e8622"}
        projection = self.flow.projection
        record = projection.read_record()
        projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": self.key, "owner_role": "creation", "owner_id": "guru-test-creation", "scope_ref": {"authority": record["accepted_scope"], "anchors": ["R1"]}, "profile": "pull_request"})
        _package, self.owner = self.flow.load_owner(PACKAGE.name)
        self.body = "Refs #9"
        self.merge = "f" * 40
        self.base = "e" * 40
        self.public = {"profile": "delivery_ready_for_merge", "mode": "workflow", "task_ref": self.flow.task_ref, "delivery_key": self.key, "publication_result_id": "publication:original", "repo_ref": "example/repo", "pr_number": 9, "expected_head_sha": self.flow.head, "publication_body_sha256": hashlib.sha256(self.body.encode()).hexdigest()}
        self.legacy = {k: v for k, v in self.public.items() if k not in {"delivery_key", "publication_result_id"}}
        self.cycle = "delivery-cycle:v1:" + "a" * 64
        self.legacy.update(profile="ready_for_merge", delivery_cycle_ref=self.cycle)
        self.review = {"dimensions": [{"id": name, "status": "passed", "summary": "Original pre-merge judgment, not a current gate."} for name in self.owner.DIMENSIONS], "route": {"typed_exit": "delivered", "merge_method": "merge", "merge_message": {"subject": "chore(merge): 合并原切片", "body": "原交付事实。\n\n" + "\n".join(self.owner.expected_trailers("flow-task", self.flow.head))}}}
        message = self.review["route"]["merge_message"]
        self.pr = {"number": 9, "url": "https://github.com/example/repo/pull/9", "state": "MERGED", "isDraft": False, "headRefOid": self.flow.head, "headRefName": "feat/flow", "baseRefName": "main", "body": self.body, "mergeCommit": {"oid": self.merge}, "mergedAt": "2026-10-12T01:00:00Z", "mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN", "reviewDecision": "APPROVED", "statusCheckRollup": []}
        self.commit = {"sha": self.merge, "message": message["subject"] + "\n\n" + message["body"], "parents": [{"sha": self.base}, {"sha": self.flow.head}]}
        pre = {"task": {"task_ref": self.flow.task_ref, "stable_task_id": "flow-task", "lifecycle_generation": 0, "status": "in_progress", "branch": "feat/flow", "base_branch": "main", "head_sha": self.flow.head}, "pr": {"number": 9, "url": self.pr["url"], "state": "OPEN", "is_draft": False, "head_sha": self.flow.head, "head_branch": "feat/flow", "base_branch": "main", "body": self.body, "merged_at": None, "merge_commit_sha": None, "mergeable": "MERGEABLE", "merge_state_status": "CLEAN", "review_decision": "APPROVED", "checks": []}, "repository_policy": {"allow_merge_commit": True, "allow_squash_merge": True, "allow_rebase_merge": True}, "base_ref": {"name": "main", "head_sha": self.base}, "merge_commit": None, "objective_blockers": []}
        pre["facts_sha256"] = self.owner.digest(pre)
        gate = self.owner.build_gate(self.legacy, pre, self.review)
        self.gate = self.owner.write_gate(PACKAGE, self.repo, gate)
        self.original = self.gate.read_bytes()
        self.bin = self.repo / ".trellis/.runtime/provider-bin"
        self.bin.mkdir()
        self.calls = self.bin / "calls.jsonl"
        provider = self.bin / "gh"
        values = {"repos/example/repo": {"full_name": "example/repo", "allow_merge_commit": True, "allow_squash_merge": True, "allow_rebase_merge": True}, "repos/example/repo/git/ref/heads/main": {"object": {"sha": self.merge}}, "repos/example/repo/git/commits/" + self.merge: self.commit}
        provider.write_text("#!" + sys.executable + "\nimport json,sys\nfrom pathlib import Path\nargs=sys.argv[1:]\nwith Path(" + repr(str(self.calls)) + ").open('a') as f: f.write(json.dumps(args)+'\\n')\nif args[:2]==['auth','status']: sys.exit(0)\nelif args[:2]==['pr','view']: print(" + repr(json.dumps(self.pr)) + ")\nelif args[:1]==['api']: print(json.dumps(" + repr(values) + "[args[1]]))\nelse: sys.exit(31)\n")
        provider.chmod(0o755)
        environment = patch.dict(os.environ, {"PATH": str(self.bin) + os.pathsep + os.environ["PATH"]})
        environment.start()
        self.addCleanup(environment.stop)
        projection.apply({"api_version": "1.0", "operation": "record_publication", "key": self.key, "owner_role": "publication", "owner_id": "guru-test-publication", "expected_phase": "planning", "historical_success": True, "result": {"result_id": "publication:original", "owner_id": "guru-test-publication", "evidence": [record["accepted_scope"]], "profile": "pull_request", "candidate": projection.resolve(self.flow.key)["candidate"], "repo_ref": "example/repo", "pr_number": 9, "reviewed_head": self.flow.head, "target_ref": "main", "publication_ref": {"locator": self.pr["url"], "revision": "sha256:" + hashlib.sha256(self.body.encode()).hexdigest()}}})

    def test_old_message_records_history_and_formal_output_recovers_without_merge(self):
        public = {"profile": "historical_merge_migration", "legacy_gate": self.gate.resolve().relative_to(self.repo.resolve()).as_posix(), "delivery_cycle_ref": self.cycle, "current_input": self.public}
        review = {"status": "passed", "summary": "Original owner verified exact historical PR attribution.", "evidence": ["Actual original message, two parents and target ancestry."]}
        args = ("--input", self.flow.write("migration.json", public), "--owner-result", self.flow.write("migration-owner.json", review))
        before = (self.repo / self.flow.task_ref / "task.json").read_bytes()
        preview = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", *args, "--preview")
        self.assertEqual("preview", preview["status"])
        self.assertEqual(before, (self.repo / self.flow.task_ref / "task.json").read_bytes())
        self.assertEqual(2, len(preview["write_paths"]))
        first = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", *args)
        self.assertEqual("historical_delivery_recorded", first["status"])
        self.assertEqual(first, self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", *args))
        args = ("--input", self.flow.write("merge.json", self.public), "--review-input", self.flow.write("merge-review.json", self.review))
        output = self.flow.wrapper(PACKAGE.name, "invoke.sh", *args)
        self.assertEqual("delivered", output["exit_id"])
        self.assertEqual(output, self.flow.wrapper(PACKAGE.name, "invoke.sh", *args))
        self.assertEqual(self.original, self.gate.read_bytes())
        current = self.flow.projection.resolve(self.key)
        self.assertEqual("delivered", current["phase"])
        self.assertIsNone(current["results"]["readiness"])
        self.assertEqual(self.flow.head, self.flow.git("rev-parse", "HEAD").strip())
        self.assertTrue(all(json.loads(line)[:2] in (["auth", "status"], ["pr", "view"]) or json.loads(line)[:1] == ["api"] for line in self.calls.read_text().splitlines()))

    def archive_task(self):
        original = self.repo / self.flow.task_ref
        archive = self.repo / ".trellis/tasks/archive/2026-10/flow-task"
        archive.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(original), archive)
        self.flow.task_ref = archive.relative_to(self.repo).as_posix()
        self.public["task_ref"] = self.flow.task_ref
        from runtime.delivery_projection.adapter import DeliveryProjection
        self.flow.projection = DeliveryProjection(self.repo, self.flow.task_ref)
        self.flow.git("add", ".")
        self.flow.git("commit", "-qm", "archive bookkeeping")
        self.flow.git("switch", "--detach")

    def test_archived_original_gate_recovers_without_active_binding_or_current_head(self):
        initial = {"profile": "historical_merge_migration", "legacy_gate": self.gate.resolve().relative_to(self.repo.resolve()).as_posix(), "delivery_cycle_ref": self.cycle, "current_input": self.public}
        reviewed = {"status": "passed", "summary": "Original owner restored the actual fact before archive adoption.", "evidence": ["Actual PR/message/parents/base."]}
        self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", "--input", self.flow.write("before-archive.json", initial), "--owner-result", self.flow.write("before-archive-owner.json", reviewed))
        self.archive_task()
        public = {"profile": "historical_merge_migration", "legacy_gate": self.gate.resolve().relative_to(self.repo.resolve()).as_posix(), "delivery_cycle_ref": self.cycle, "current_input": self.public}
        review = {"status": "passed", "summary": "Original owner reviewed archived identity and historical merge.", "evidence": ["Exact original gate and actual PR/message/parents/base."]}
        args = ("--input", self.flow.write("migration.json", public), "--owner-result", self.flow.write("migration-owner.json", review))
        preview = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", *args, "--preview")
        self.assertEqual(1, len(preview["write_paths"]))
        result = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", *args)
        self.assertEqual("historical_delivery_recorded", result["status"])
        output = self.flow.wrapper(PACKAGE.name, "invoke.sh", "--input", self.flow.write("merge.json", self.public), "--review-input", self.flow.write("merge-review.json", self.review))
        self.assertEqual("delivered", output["exit_id"])
        self.assertEqual(output, self.flow.wrapper(PACKAGE.name, "invoke.sh", "--input", self.flow.write("merge.json", self.public), "--review-input", self.flow.write("merge-review.json", self.review)))
        self.assertEqual(self.original, self.gate.read_bytes())
        self.assertNotEqual(self.flow.head, self.flow.git("rev-parse", "HEAD").strip())
        self.assertIsNone(self.flow.projection.resolve(self.key)["results"]["readiness"])
        self.assertFalse(any(json.loads(line)[:2] == ["pr", "merge"] for line in self.calls.read_text().splitlines()))

    def test_noactive_task_restores_missing_actual_historical_fact(self):
        self.flow.git("switch", "--detach")
        public = {"profile": "historical_merge_migration", "legacy_gate": self.gate.resolve().relative_to(self.repo.resolve()).as_posix(), "delivery_cycle_ref": self.cycle, "current_input": self.public}
        review = {"status": "passed", "summary": "Original owner reviewed exact history with no active checkout.", "evidence": ["Actual PR/message/parents/base."]}
        result = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", "--input", self.flow.write("migration.json", public), "--owner-result", self.flow.write("migration-owner.json", review))
        self.assertEqual("historical_delivery_recorded", result["status"])
        self.assertIsNone(self.flow.projection.resolve(self.key)["results"]["readiness"])
        self.assertFalse(any(json.loads(line)[:2] == ["pr", "merge"] for line in self.calls.read_text().splitlines()))

    def test_archived_missing_public_fact_names_plan2_prerequisite_without_writes(self):
        self.archive_task()
        public = {"profile": "historical_merge_migration", "legacy_gate": self.gate.resolve().relative_to(self.repo.resolve()).as_posix(), "delivery_cycle_ref": self.cycle, "current_input": self.public}
        review = {"status": "passed", "summary": "Original owner verified actual history, but Plan2 omitted the public result.", "evidence": ["Actual old gate/PR/message/parents/base."]}
        before = (self.repo / self.flow.task_ref / "task.json").read_bytes()
        args = ("--input", self.flow.write("migration.json", public), "--owner-result", self.flow.write("migration-owner.json", review))
        preview = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", *args, "--preview", success=False)
        result = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", *args, success=False)
        self.assertEqual(preview, result)
        self.assertEqual("stale_identity", result["code"])
        self.assertEqual("delivery_result", result["field_path"])
        self.assertIn("prospective Plan2 target record", result["remediation"])
        self.assertEqual(before, (self.repo / self.flow.task_ref / "task.json").read_bytes())
        self.assertFalse(self.owner.gate_path(self.repo, self.public).with_suffix(".migration.json").exists())
        self.assertEqual(self.original, self.gate.read_bytes())
        self.assertFalse(any(json.loads(line)[:2] == ["pr", "merge"] for line in self.calls.read_text().splitlines()))

    def test_archived_open_source_requires_fresh_merge_owner_without_writes(self):
        self.archive_task()
        provider = self.bin / "gh"
        opened = {**self.pr, "state": "OPEN", "mergeCommit": None, "mergedAt": None}
        provider.write_text(provider.read_text().replace(repr(json.dumps(self.pr)), repr(json.dumps(opened))))
        public = {"profile": "historical_merge_migration", "legacy_gate": self.gate.resolve().relative_to(self.repo.resolve()).as_posix(), "delivery_cycle_ref": self.cycle, "current_input": self.public}
        review = {"status": "passed", "summary": "Original owner reviewed identity only; a new merge needs its own current gate.", "evidence": ["Current OPEN PR and preserved old gate."]}
        before = (self.repo / self.flow.task_ref / "task.json").read_bytes()
        result = self.flow.wrapper(PACKAGE.name, "migrate-delivery-transaction.sh", "--input", self.flow.write("migration.json", public), "--owner-result", self.flow.write("migration-owner.json", review))
        self.assertEqual("fresh_merge_review_required", result["status"])
        self.assertEqual(before, (self.repo / self.flow.task_ref / "task.json").read_bytes())
        self.assertEqual(self.original, self.gate.read_bytes())
        self.assertFalse(self.owner.gate_path(self.repo, self.public).with_suffix(".migration.json").exists())
        self.flow.wrapper(PACKAGE.name, "invoke.sh", "--input", self.flow.write("merge.json", self.public), "--review-input", self.flow.write("merge-review.json", self.review), success=False)
        self.assertFalse(any(json.loads(line)[:2] == ["pr", "merge"] for line in self.calls.read_text().splitlines()))
