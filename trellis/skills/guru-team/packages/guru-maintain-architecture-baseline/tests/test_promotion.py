"""Real wrapper evidence for candidate binding and owner-written promotion.

These tests exercise deterministic validation, not independent AI judgment.
"""
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

import test_contract as contract_tests


class PromotionTest(unittest.TestCase):
    digest = staticmethod(contract_tests.ArchitectureBaselineContractTest.digest)
    load = contract_tests.ArchitectureBaselineContractTest.load
    project_check = contract_tests.ArchitectureBaselineContractTest.project_check
    project_check_descriptor = contract_tests.ArchitectureBaselineContractTest.project_check_descriptor
    architecture_selection = contract_tests.ArchitectureBaselineContractTest.architecture_selection
    write_current_constitution = contract_tests.ArchitectureBaselineContractTest.write_current_constitution
    tearDown = contract_tests.ArchitectureBaselineContractTest.tearDown

    def setUp(self):
        contract_tests.ArchitectureBaselineContractTest.setUp(self)
        sys.path.insert(0, str(self.package.parents[1]))
        spec = importlib.util.spec_from_file_location("architecture_promotion", self.package / "runtime/promotion.py")
        self.production = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.production)
        self.public = self.load("public-input-delivery-promotion-2.0.json")
        self.public.update(task_locator=self.upstream.task_ref, delivery_key=self.delivery_key,
                           planning_root=self.upstream.projection.resolve(self.delivery_key)["planning_root"])
        self.baseline = self.public["baseline"]["locator"]
        self.contract = self.public["project_contract"]["change_contract_locator"]
        for locator, content in [(self.baseline, "# Current v1\n"), (self.contract, "# Project contract\n")]:
            path = self.repository / locator
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.git("add", self.baseline, self.contract, self.public["constitution"]["authority_locator"])
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Architecture before")
        revision = self.git("rev-parse", "HEAD")
        self.public["before_authority"]["git_revision"] = revision
        (self.repository / "implementation.txt").write_text("Actual untracked implementation candidate\n")
        self.public["candidate"] = self.production.capture_candidate(self.repository)
        self.public["expected_current_content_identity"] = "sha256:" + hashlib.sha256((self.repository / self.baseline).read_bytes()).hexdigest()
        self.targets = [{"locator": self.baseline, "before_content": "# Current v1\n", "content": "# Current v2\n"},
                        {"locator": "docs/architecture/new-decision.md", "before_content": None,
                         "content": "# Reviewed decision\n"}]

    def git(self, *argv):
        return subprocess.run(["git", *argv], cwd=self.repository, check=True,
                              text=True, capture_output=True).stdout.strip()

    def write_targets(self, targets=None):
        for row in targets or self.targets:
            path = self.repository / row["locator"]
            if row["content"] is None:
                path.unlink(missing_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(row["content"])

    def owner(self, public=None):
        public = public or self.public
        selected = self.architecture_selection(public, promotion_state="reviewed_promoted",
                                              baseline_identity=public["successor_baseline"]["identity"],
                                              contribution_locator=public["sync_target"]["locator"],
                                              contribution_identity=public["sync_target"]["current_identity"])
        return {"schema_version": public["schema_version"],
                **{key: copy.deepcopy(public[key]) for key in
                   ("profile", "mode", "continuation_id", "stage", "task_locator", "baseline", "constitution",
                    "project_contract", "freshness_identity", "before_authority", "candidate",
                    "expected_current_identity", "current_identity", "sync_kind", "sync_target")},
                **({"delivery_key": public["delivery_key"], "planning_root": public["planning_root"]}
                   if public["profile"].startswith("delivery_") else {}),
                "input_sha256": self.digest(public),
                "ai_review_gate": {"status": "passed", "reviewed_scope": "Real candidate and proposed writes",
                                   "evidence_summary": "Test semantic fixture, not an AI behavior proof",
                                   "findings": [], "conclusion": "Fixture result"},
                "consumer": {"kind": "workflow", "id": "guru-architecture-baseline-current-router"},
                **selected,
                "review": {"status": "reviewed", "independent": True,
                           "candidate": public["candidate"], "before_authority": public["before_authority"]},
                "promotion_targets": self.targets,
                "post_candidate": self.production.capture_candidate(self.repository),
                "postwrite_applicability": {"status": "applicable", "reason": "Actual writes match the reviewed intent"}}

    def invoke(self, owner=None, public=None):
        public = public or self.public
        return subprocess.run([str(self.fixture_package / "scripts/invoke.sh"), "--invocation", "-"],
                              cwd=self.repository, input=json.dumps({"public_input": public,
                                                                    "owner_result": owner or self.owner(public)}),
                              text=True, capture_output=True)

    def test_promotes_before_check_without_future_committed_review_and_projects_actual_candidate(self):
        self.write_targets()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["stage"], "phase2")
        self.assertEqual(output["source_profile"], "delivery_promotion")
        self.assertEqual(output["candidate"], self.production.capture_candidate(self.repository))
        self.assertEqual(output["before_authority"], self.public["before_authority"])
        self.assertNotIn("promotion_targets", output)
        self.assertNotIn("review", output)
        self.assertNotEqual(output["candidate"], self.public["candidate"])

    def test_partial_write_readback_then_same_intent_completion_and_output_loss(self):
        self.write_targets(self.targets[:1])
        self.assertEqual(self.production.target_states(self.repository, self.targets),
                         {self.baseline: "completed", "docs/architecture/new-decision.md": "pending"})
        partial = self.invoke()
        self.assertEqual(partial.returncode, 3, partial.stdout)
        self.write_targets(self.targets[1:])
        owner = self.owner()
        first, recovered = self.invoke(owner), self.invoke(owner)
        self.assertEqual(first.returncode, 0, first.stdout)
        self.assertEqual(recovered.stdout, first.stdout)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.public["candidate"]["head"])

    def test_conflicting_target_and_new_candidate_content_block_without_writes(self):
        self.write_targets()
        (self.repository / self.baseline).write_text("A different current baseline\n")
        self.assertEqual(self.production.target_states(self.repository, self.targets)[self.baseline], "conflict")
        result = self.invoke()
        self.assertEqual(result.returncode, 3)
        self.assertEqual((self.repository / self.baseline).read_text(), "A different current baseline\n")
        self.write_targets()
        (self.repository / "implementation.txt").write_text("New implementation after independent review\n")
        result = self.invoke()
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["field_path"], "candidate")

    def test_expected_current_mismatch_and_unreviewed_actual_delta_block(self):
        self.write_targets()
        public = copy.deepcopy(self.public)
        public["expected_current_content_identity"] = "sha256:" + "0" * 64
        result = self.invoke(public=public)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["field_path"], "expected_current_content_identity")
        (self.repository / "docs/architecture/new-decision.md").write_text("Changed proposed decision\n")
        result = self.invoke()
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["field_path"], "owner_result.promotion_targets")

    def test_task_promotion_same_current_contract_and_legacy_input_rejected(self):
        self.write_targets()
        public = copy.deepcopy(self.public)
        public.update(profile="promotion", schema_version="4.0")
        public.pop("delivery_key")
        public.pop("planning_root")
        result = self.invoke(public=public)
        self.assertEqual(result.returncode, 0, result.stdout)
        legacy = self.load("public-input-delivery-promotion-1.0.json")
        result = self.invoke(owner=self.owner(), public=legacy)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["code"], "schema_mismatch")

    def test_current_contribution_accepts_precheck_review_without_future_committed_range(self):
        from runtime.schema import validate_json
        from runtime.io import CommandError
        value = contract_tests.ArchitectureBaselineContractTest.contribution(self, self.public)
        value.update(schema_version="4.0", guru_contract_identity="guru-maintain-architecture-baseline:4.0",
                     review={"status": "reviewed", "independent": True,
                             "candidate": self.public["candidate"], "before_authority": self.public["before_authority"]},
                     promotion={"state": "reviewed_promoted", "promoted_identity": self.public["successor_baseline"]["identity"]})
        validate_json(value, self.package / "schemas/architecture-contribution-4.0.schema.json", "contribution")
        with self.assertRaises(CommandError):
            validate_json(value, self.package / "schemas/architecture-contribution.schema.json", "legacy_contribution")

    def test_no_change_phase2_binds_actual_candidate_without_promotion_burden(self):
        public = self.load("public-input-delivery-task-impact-sync-2.0.json")
        public.update(task_locator=self.upstream.task_ref, delivery_key=self.delivery_key,
                      planning_root=self.public["planning_root"], stage="phase2",
                      candidate=self.public["candidate"], before_authority=self.public["before_authority"])
        owner = self.owner()
        for key in ("promotion_targets", "post_candidate", "postwrite_applicability", "review", "change_path",
                    "contribution_locator", "contribution_identity", "project_checks", "project_check_descriptors",
                    "expected_current_identity", "current_identity", "sync_kind", "sync_target"):
            owner.pop(key, None)
        owner.update({key: copy.deepcopy(public[key]) for key in ("profile", "mode", "continuation_id", "stage", "baseline", "freshness_identity")})
        owner.update(input_sha256=self.digest(public), impact_kind="no_architecture_impact",
                     promotion_state="no_change", impact_reason="No architecture boundary changes",
                     baseline_identity=public["baseline"]["identity"])
        result = self.invoke(owner, public)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["promotion_state"], "no_change")
        self.assertFalse((self.repository / "docs/architecture/new-decision.md").exists())
        (self.repository / "implementation.txt").write_text("Changed candidate\n")
        self.assertEqual(self.invoke(owner, public).returncode, 3)
