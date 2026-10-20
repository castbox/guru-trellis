"""Real wrapper evidence for candidate binding and owner-written promotion.

These tests exercise deterministic validation, not independent AI judgment.
"""
import copy
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
        self.public = self.load("public-input-delivery-promotion-3.0.json")
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
        self.unit = "docs/architecture/capability-a.md"
        (self.repository / self.unit).write_text("# Query\nRead-only calls preserve the original error source.\n")
        self.public["candidate"] = self.production.capture_candidate(self.repository)
        self.targets = [{"locator": self.unit, "before_content": (self.repository / self.unit).read_text(),
                         "content": "# Query\nRead-only calls preserve the original error source, including timeouts.\n"},
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
                                              baseline_identity=public["baseline"]["identity"],
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

    def test_final_integration_promotes_stable_identity_without_root_write(self):
        self.write_targets()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["stage"], "final_integration")
        self.assertEqual(output["source_profile"], "delivery_promotion")
        self.assertEqual(output["candidate"], self.production.capture_candidate(self.repository))
        self.assertEqual(output["before_authority"], self.public["before_authority"])
        self.assertNotIn("promotion_targets", output)
        self.assertNotIn("review", output)
        self.assertNotEqual(output["candidate"], self.public["candidate"])
        self.assertEqual(output["baseline_identity"], self.public["baseline"]["identity"])
        self.assertEqual((self.repository / self.baseline).read_text(), "# Current v1\n")
        self.assertNotIn(self.baseline, [row["locator"] for row in self.targets])

    def test_numbered_to_stable_identity_requires_actual_reviewed_baseline_write(self):
        from runtime.schema import validate_json
        before = "# Architecture\nIdentity: guru-trellis-architecture-baseline.105\n"
        after = "# Architecture\nIdentity: guru-trellis-architecture\n\n[Query](capability-a.md)\n"
        (self.repository / self.baseline).write_text(before)
        self.git("add", self.baseline)
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "commit", "-qm", "Numbered before authority")
        public = copy.deepcopy(self.public)
        public["baseline"]["identity"] = "guru-trellis-architecture-baseline.105"
        public["expected_current_identity"] = public["current_identity"] = public["baseline"]["identity"]
        public["before_authority"]["git_revision"] = self.git("rev-parse", "HEAD")
        public["candidate"] = self.production.capture_candidate(self.repository)
        self.write_targets()

        def migration_result():
            owner = self.owner(public)
            owner["baseline_identity"] = "guru-trellis-architecture"
            return self.invoke(owner, public)

        leaf_only = migration_result()
        self.assertEqual(leaf_only.returncode, 3, leaf_only.stdout)
        self.assertEqual(json.loads(leaf_only.stdout)["field_path"], "owner_result.baseline_identity")
        self.targets.append({"locator": self.baseline, "before_content": before, "content": before})
        unchanged_entry = migration_result()
        self.assertEqual(unchanged_entry.returncode, 3, unchanged_entry.stdout)
        self.assertEqual(json.loads(unchanged_entry.stdout)["field_path"], "owner_result.baseline_identity")
        self.targets[-1]["content"] = after
        partial = migration_result()
        self.assertEqual(partial.returncode, 3, partial.stdout)
        self.assertEqual(json.loads(partial.stdout)["field_path"], "owner_result.promotion_targets")
        self.write_targets(self.targets[-1:])
        complete = migration_result()
        self.assertEqual(complete.returncode, 0, complete.stdout + complete.stderr)
        output = json.loads(complete.stdout)
        self.assertEqual(output["baseline_identity"], "guru-trellis-architecture")
        self.assertEqual(output["before_authority"], public["before_authority"])
        self.assertEqual(output["candidate"], self.production.capture_candidate(self.repository))
        self.assertEqual((self.repository / self.baseline).read_text(), after)
        validate_json(output, self.package / "consumers/workflow/current-5.0.schema.json", "consumer")
        self.assertEqual(migration_result().stdout, complete.stdout)

    def test_final_integration_repair_projection_returns_to_same_promotion(self):
        from runtime.schema import validate_json
        continuation = copy.deepcopy(self.public)
        owner = self.owner()
        owner.update(typed_exit="sync_required", sync_kind="repair",
                     consumer={"kind": "workflow", "id": "guru-architecture-baseline-sync-router"},
                     sync_target={"kind": "project_contract", "locator": self.contract,
                                  "expected_identity": self.public["project_contract"]["change_contract_identity"],
                                  "current_identity": self.public["project_contract"]["change_contract_identity"]})
        requested = self.invoke(owner)
        self.assertEqual(requested.returncode, 0, requested.stdout)
        output = json.loads(requested.stdout)
        validate_json(output, self.package / "consumers/workflow/sync-required-5.0.schema.json", "consumer")

        # This is the declared caller-side thin projection. The old maintenance
        # contract retains phase2; its current result never becomes promotion.
        repair = self.load("public-input-delivery-repair-1.0.json")
        repair.update(stage="phase2", source_exit=output["exit_id"],
                      continuation_id=continuation["continuation_id"],
                      **{key: output[key] for key in ("task_locator", "delivery_key", "planning_root")})
        for key in ("baseline", "constitution"):
            repair[key] = copy.deepcopy(continuation[key])
        repair["project_contract"] = copy.deepcopy(continuation["project_contract"])
        repair["project_contract"]["guru_contract_identity"] = "guru-maintain-architecture-baseline:2.0"
        (self.repository / self.contract).write_text("# Project contract\nRestored descriptor.\n")
        repair_owner = {key: copy.deepcopy(repair[key]) for key in
                        ("schema_version", "profile", "mode", "continuation_id", "stage", "task_locator",
                         "baseline", "constitution", "project_contract", "freshness_identity",
                         "delivery_key", "planning_root")}
        repair_owner.update(input_sha256=self.digest(repair), typed_exit="baseline_current",
                            baseline_identity=repair["baseline"]["identity"],
                            constitution_identity=repair["constitution"]["identity"],
                            impact_kind="no_architecture_impact", promotion_state="no_change",
                            impact_reason="Original maintenance restored the descriptor.",
                            ai_review_gate=copy.deepcopy(owner["ai_review_gate"]),
                            consumer={"kind": "workflow", "id": "guru-architecture-baseline-current-router"})
        repaired = self.invoke(repair_owner, repair)
        self.assertEqual(repaired.returncode, 0, repaired.stdout + repaired.stderr)
        maintenance = json.loads(repaired.stdout)
        self.assertEqual(maintenance["source_profile"], "delivery_repair")
        self.assertEqual(maintenance["stage"], "phase2")
        self.assertEqual(maintenance["promotion_state"], "no_change")
        self.assertEqual(maintenance["delivery_key"], continuation["delivery_key"])

        resumed = copy.deepcopy(continuation)
        resumed["source_exit"] = maintenance["exit_id"]
        resumed["candidate"] = self.production.capture_candidate(self.repository)
        resumed["project_contract"]["change_contract_identity"] = "project-change-contract-repaired"
        self.assertEqual(resumed["profile"], "delivery_promotion")
        self.assertEqual(resumed["stage"], "final_integration")
        self.assertEqual(resumed["delivery_key"], continuation["delivery_key"])
        self.write_targets()
        stale = self.invoke(public=continuation)
        self.assertEqual(stale.returncode, 3, stale.stdout)
        self.assertEqual(json.loads(stale.stdout)["field_path"], "candidate")
        promoted = self.invoke(public=resumed)
        self.assertEqual(promoted.returncode, 0, promoted.stdout + promoted.stderr)
        final = json.loads(promoted.stdout)
        self.assertEqual(final["source_profile"], "delivery_promotion")
        self.assertEqual(final["stage"], "final_integration")
        self.assertEqual(final["promotion_state"], "reviewed_promoted")
        self.assertEqual(final["planning_root"], continuation["planning_root"])

    def test_partial_write_readback_then_same_intent_completion_and_output_loss(self):
        self.write_targets(self.targets[:1])
        self.assertEqual(self.production.target_states(self.repository, self.targets),
                         {self.unit: "completed", "docs/architecture/new-decision.md": "pending"})
        partial = self.invoke()
        self.assertEqual(partial.returncode, 3, partial.stdout)
        self.write_targets(self.targets[1:])
        owner = self.owner()
        first, recovered = self.invoke(owner), self.invoke(owner)
        self.assertEqual(first.returncode, 0, first.stdout)
        self.assertEqual(recovered.stdout, first.stdout)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.public["candidate"]["head"])

    def test_different_capability_promotions_preserve_root_and_first_unit(self):
        before_head = self.git("rev-parse", "HEAD")
        root_bytes = (self.repository / self.baseline).read_bytes()
        self.write_targets()
        first = self.invoke()
        self.assertEqual(first.returncode, 0, first.stdout)
        first_bytes = (self.repository / self.unit).read_bytes()

        # Another complete capability is authored against the same immutable
        # authority. Its actual candidate includes the already promoted unit.
        public = copy.deepcopy(self.public)
        public["continuation_id"] = "export-final-integration"
        public["sync_target"].update(locator="docs/architecture/contributions/export",
                                     expected_identity="export-contribution",
                                     current_identity="export-contribution")
        public["candidate"] = self.production.capture_candidate(self.repository)
        self.targets = [{"locator": "docs/architecture/capability-b.md", "before_content": None,
                         "content": "# Export\nTask completion does not mean notification delivery.\n"}]
        self.write_targets()
        second = self.invoke(public=public)
        self.assertEqual(second.returncode, 0, second.stdout)
        self.assertEqual(json.loads(second.stdout)["baseline_identity"],
                         json.loads(first.stdout)["baseline_identity"])
        self.assertEqual((self.repository / self.unit).read_bytes(), first_bytes)
        self.assertEqual((self.repository / self.baseline).read_bytes(), root_bytes)
        self.assertEqual(self.git("rev-parse", "HEAD"), before_head)
        self.assertIn("Task completion does not mean notification delivery.",
                      (self.repository / self.targets[0]["locator"]).read_text())

    def test_final_integration_failures_project_to_declared_consumers(self):
        from runtime.schema import validate_json
        interface = json.loads((self.package / "interface.json").read_text())
        branches = {
            "sync_required": {"sync_kind": "promotion_required", "sync_target": self.public["sync_target"],
                              "expected_current_identity": self.public["expected_current_identity"],
                              "current_identity": self.public["current_identity"]},
            "architecture_conflict": {"conflict_refs": [self.unit], "return_route": "planning"},
            "contract_incomplete": {"missing_refs": [self.contract], "return_route": "planning"},
            "fitness_regression": {"regression_refs": [self.unit], "return_route": "implementation"},
        }
        for exit_id, fields in branches.items():
            with self.subTest(exit=exit_id):
                owner = self.owner()
                owner.update(typed_exit=exit_id, **fields)
                owner["consumer"] = next(row["consumer"] for row in interface["external_exits"]
                                         if row["id"] == exit_id)
                result = self.invoke(owner)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                output = json.loads(result.stdout)
                self.assertEqual(output["stage"], "final_integration")
                projection = next(row for row in interface["public_contracts"]["projections"]
                                  if row["exit_id"] == exit_id)
                consumer = next(row for row in interface["public_contracts"]["consumer_inputs"]
                                if row["id"] == projection["consumer_input_id"])
                validate_json(output, self.package / consumer["contract"]["path"], "consumer")

    def test_conflicting_target_and_new_candidate_content_block_without_writes(self):
        self.write_targets()
        (self.repository / self.unit).write_text("A different current capability\n")
        self.assertEqual(self.production.target_states(self.repository, self.targets)[self.unit], "conflict")
        result = self.invoke()
        self.assertEqual(result.returncode, 3)
        self.assertEqual((self.repository / self.unit).read_text(), "A different current capability\n")
        self.write_targets()
        (self.repository / "implementation.txt").write_text("New implementation after independent review\n")
        result = self.invoke()
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["field_path"], "candidate")

    def test_expected_current_mismatch_and_unreviewed_actual_delta_block(self):
        self.write_targets()
        public = copy.deepcopy(self.public)
        public["expected_current_identity"] = "a different authority"
        result = self.invoke(public=public)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["field_path"], "public_input.current_identity")
        (self.repository / "docs/architecture/new-decision.md").write_text("Changed proposed decision\n")
        result = self.invoke()
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["field_path"], "owner_result.promotion_targets")

    def test_task_promotion_same_current_contract_and_legacy_input_rejected(self):
        self.write_targets()
        public = copy.deepcopy(self.public)
        public.update(profile="promotion", schema_version="5.0")
        public.pop("delivery_key")
        public.pop("planning_root")
        result = self.invoke(public=public)
        self.assertEqual(result.returncode, 0, result.stdout)
        for name in ("public-input-delivery-promotion-1.0.json", "public-input-delivery-promotion-2.0.json", "public-input-promotion-4.0.json"):
            legacy = self.load(name)
            result = self.invoke(owner=self.owner(), public=legacy)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["code"], "schema_mismatch")

    def test_current_contribution_accepts_precheck_review_without_future_committed_range(self):
        from runtime.schema import validate_json
        from runtime.io import CommandError
        value = contract_tests.ArchitectureBaselineContractTest.contribution(self, self.public)
        value.update(schema_version="5.0", guru_contract_identity="guru-maintain-architecture-baseline:5.0",
                     review={"status": "reviewed", "independent": True,
                             "candidate": self.public["candidate"], "before_authority": self.public["before_authority"]},
                     promotion={"state": "reviewed_promoted", "promoted_identity": self.public["baseline"]["identity"]})
        validate_json(value, self.package / "schemas/architecture-contribution-5.0.schema.json", "contribution")
        with self.assertRaises(CommandError):
            validate_json(value, self.package / "schemas/architecture-contribution.schema.json", "legacy_contribution")

    def test_no_change_phase2_binds_actual_candidate_without_promotion_burden(self):
        public = self.load("public-input-delivery-task-impact-sync-3.0.json")
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
