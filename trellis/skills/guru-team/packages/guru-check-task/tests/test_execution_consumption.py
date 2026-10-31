"""Current Delivery Check consumption, zero candidates, and original gate duties.

The old Task execution checkpoint is retired. These actual installed-API tests
retain its current-input, result-recovery and evidence/freshness assertions on
the Delivery owner; fixture judgments do not constitute semantic review.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

import test_delivery_flow as flow_fixture
from runtime.delivery_projection.adapter import authority_ref
from runtime.delivery_projection.gates import rework

PACKAGE = Path(__file__).resolve().parents[1]
PROFILES = ("delivery_initial_check", "delivery_finding_fix_rerun",
            "delivery_planning_reentry", "delivery_resolved_reconciliation")


class ExecutionConsumptionTests(unittest.TestCase):
    setUp = flow_fixture.DeliveryFlow.setUp
    git = flow_fixture.DeliveryFlow.git
    write = flow_fixture.DeliveryFlow.write
    wrapper = flow_fixture.DeliveryFlow.wrapper

    def fixture(self, profile):
        fixture = flow_fixture.DeliveryFlow()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        if profile == "delivery_resolved_reconciliation":
            # Construct a normal evolved-base merge with a real resolved index.
            fixture.git("add", ".")
            fixture.git("commit", "-qm", "bind current delivery metadata")
            fixture.head = fixture.git("rev-parse", "HEAD").strip()
            old_base = fixture.git("rev-parse", "main").strip()
            fixture.git("switch", "main")
            (fixture.repo / "app.txt").write_text("evolved base\n")
            fixture.git("add", "app.txt")
            fixture.git("commit", "-qm", "base evolution")
            fixture.git("switch", "feat/flow")
            result = subprocess.run(["git", "merge", "--no-commit", "main"],
                                    cwd=fixture.repo, capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            (fixture.repo / "app.txt").write_text("feature with evolved base\n")
            fixture.git("add", "app.txt")
            rework(fixture.projection, fixture.key, "check", "implementation",
                   authority_ref(fixture.repo / "requirements.md", fixture.repo),
                   ["check", "full_review", "readiness"])
            fixture.projection.begin_check(fixture.key, fixture.projection.candidate(
                ["app.txt"], head_ref=fixture.head, base_ref=old_base))
            fixture.git("add", fixture.task_ref + "/task.json")
        return fixture

    def public(self, fixture, profile):
        example = PACKAGE / ("examples/public-" + profile.replace("_", "-") + "-input-1.0.json")
        value = json.loads(example.read_text())
        value.update(task_ref=fixture.task_ref, delivery_key=fixture.key,
                     planning_accepted_result_id="planning:flow")
        return value

    def candidate(self, decision="rejected_not_reproduced"):
        row = json.loads((PACKAGE / "examples/phase2-rejected-candidates.json").read_text())[0]
        row["decision"] = decision
        if decision == "qualified_current":
            row["witness"]["defect_observation"] = "The supported upper endpoint fails."
        elif decision == "qualified_approved_expansion":
            row["witness"]["defect_observation"] = "The current authority requests a revised endpoint contract."
        return row

    def owner(self, fixture, *, candidates=None, result="passed"):
        path = PACKAGE / "runtime/common.py"
        spec = importlib.util.spec_from_file_location("consumption_check_common", path)
        common = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(common)
        value = json.loads((PACKAGE / "examples/phase2-check.json").read_text())
        value.update(task_ref=fixture.task_ref, phase2_capture_commit=fixture.head,
                     reviewed_content_sha256=common.content_identity(fixture.repo),
                     reviewed_paths=["app.txt"], candidate_classifications=copy.deepcopy(candidates or []),
                     typed_exit=result)
        if result == "resolved_reconciliation_passed":
            value["consumer"] = {"kind": "skill", "id": "guru-reconcile-task-base"}
        elif result == "blocked":
            value["consumer"] = {"kind": "stop", "id": "task-check-blocked"}
            value["semantic_review"]["status"] = "blocked"
            value["semantic_review"]["adequacy_dimensions"][-1]["status"] = "blocked"
            value["validation"]["unverified_items"] = [{"id": "evidence", "summary": "Required integration evidence is unavailable.", "blocking": True}]
        elif result in {"implementation_required", "planning_stale"}:
            ref = value["candidate_classifications"][0]["candidate_ref"]
            value["semantic_review"]["status"] = result
            if result == "implementation_required":
                value["consumer"] = {"kind": "workflow", "id": "guru-resume-implementation"}
                value["semantic_review"]["adequacy_dimensions"][2]["status"] = "failed"
                value["semantic_review"]["findings"] = [{"id": "F-boundary", "candidate_ref": ref, "severity": "P2", "summary": "The upper endpoint is excluded.", "path": "app.txt", "status": "open"}]
                decision = "current_scope"
            else:
                value["consumer"] = {"kind": "workflow", "id": "guru-task-check-planning-router"}
                value["route"] = "reapprove_plan"
                decision = "scope_change_required"
            value["semantic_review"]["scope_decisions"] = [{"id": "scope-boundary", "candidate_ref": ref, "disposition": decision, "summary": "The endpoint contract requires current review.", "finding_id": "F-boundary" if result == "implementation_required" else None}]
        return value

    def invoke(self, fixture, public, owner, *, success=True):
        return fixture.wrapper("guru-check-task", "invoke.sh", "--input",
                               fixture.write("check-public.json", public), "--owner-result",
                               fixture.write("check-owner.json", owner), success=success)

    def test_zero_and_all_rejected_sets_preserve_all_profile_consumers(self):
        for profile in PROFILES:
            for candidates in ([], [self.candidate()]):
                with self.subTest(profile=profile, candidates=len(candidates)):
                    fixture = self.fixture(profile)
                    resolved = profile == "delivery_resolved_reconciliation"
                    owner = self.owner(fixture, candidates=candidates,
                                       result="resolved_reconciliation_passed" if resolved else "passed")
                    public = self.public(fixture, profile)
                    output = self.invoke(fixture, public, owner)
                    self.assertEqual(fixture.task_ref, output["task_ref"])
                    self.assertEqual(fixture.key, output["delivery_key"])
                    if resolved:
                        self.assertEqual("resolved_reconciliation_passed", output["exit_id"])
                        self.assertEqual(fixture.head, output["phase2_commit_anchor"])
                        self.assertIsNone(fixture.projection.resolve(fixture.key)["results"]["check"])
                    else:
                        self.assertEqual("passed", output["exit_id"])
                        self.assertEqual(output["check_result_id"], fixture.projection.resolve(fixture.key)["results"]["check"]["result_id"])
                        self.assertEqual(output, self.invoke(fixture, public, owner))
                    self.assertEqual(fixture.head, fixture.git("rev-parse", "HEAD").strip())
                    self.assertEqual(candidates, owner["candidate_classifications"])

    def test_nonempty_findings_and_planning_routes_keep_unique_consumers(self):
        for profile in PROFILES:
            for result, decision in (("implementation_required", "qualified_current"),
                                     ("planning_stale", "qualified_approved_expansion")):
                with self.subTest(profile=profile, result=result):
                    fixture = self.fixture(profile)
                    owner = self.owner(fixture, candidates=[self.candidate(decision)], result=result)
                    output = self.invoke(fixture, self.public(fixture, profile), owner)
                    self.assertEqual(result, output["exit_id"])
                    key, refs = ("finding_refs", ["F-boundary"]) if result == "implementation_required" else ("proposal_refs", ["scope-boundary"])
                    self.assertEqual(refs, output[key])
                    phase = "implementing" if result == "implementation_required" else "planning"
                    self.assertEqual(phase, fixture.projection.resolve(fixture.key)["phase"])
                    self.assertEqual(fixture.head, fixture.git("rev-parse", "HEAD").strip())

    def test_zero_candidates_do_not_bypass_missing_evidence_or_content_freshness(self):
        for profile in PROFILES:
            with self.subTest(profile=profile):
                fixture = self.fixture(profile)
                public = self.public(fixture, profile)
                blocked = self.owner(fixture, result="blocked")
                before = (fixture.repo / fixture.task_ref / "task.json").read_bytes()
                self.assertEqual({"exit_id": "blocked"}, self.invoke(fixture, public, blocked))
                self.assertEqual(before, (fixture.repo / fixture.task_ref / "task.json").read_bytes())
                resolved = profile == "delivery_resolved_reconciliation"
                owner = self.owner(fixture, result="resolved_reconciliation_passed" if resolved else "passed")
                (fixture.repo / "app.txt").write_text("New ordinary content after review.\n")
                result = self.invoke(fixture, public, owner, success=False)
                self.assertEqual("stale_identity", result["code"])
                self.assertEqual(before, (fixture.repo / fixture.task_ref / "task.json").read_bytes())

    def test_semantic_authoring_real_commands_keep_final_profile_routes(self):
        """Command evidence only; the fixture does not claim native judgment."""
        for profile in PROFILES:
            for result in ("success", "implementation_required", "planning_stale", "blocked"):
                with self.subTest(profile=profile, result=result):
                    fixture = self.fixture(profile)
                    public = self.public(fixture, profile)
                    authored = json.loads((PACKAGE / "examples/phase2-authoring.json").read_text())
                    authored["reviewed_paths"] = ["app.txt"]
                    exit_id = ("resolved_reconciliation_passed" if profile == "delivery_resolved_reconciliation" else "passed") if result == "success" else result
                    authored["typed_exit"] = exit_id
                    if exit_id == "resolved_reconciliation_passed":
                        authored["consumer"] = {"kind": "skill", "id": "guru-reconcile-task-base"}
                    elif exit_id == "blocked":
                        authored["consumer"] = {"kind": "stop", "id": "task-check-blocked"}
                        authored["semantic_review"]["status"] = "blocked"
                        authored["semantic_review"]["adequacy_dimensions"][-1]["status"] = "blocked"
                        authored["validation"]["unverified_items"] = [{"id": "U-command", "summary": "Required command evidence is unavailable.", "blocking": True}]
                    elif exit_id in {"implementation_required", "planning_stale"}:
                        finding = exit_id == "implementation_required"
                        authored["consumer"] = {"kind": "workflow", "id": "guru-resume-implementation" if finding else "guru-task-check-planning-router"}
                        authored["semantic_review"]["status"] = exit_id
                        authored["candidate_classifications"] = [self.candidate("qualified_current" if finding else "qualified_approved_expansion")]
                        ref = authored["candidate_classifications"][0]["candidate_ref"]
                        authored["semantic_review"]["scope_decisions"] = [{"id": "scope-command", "candidate_ref": ref,
                            "disposition": "current_scope" if finding else "scope_change_required", "summary": "The endpoint requires current review.", "finding_id": "F-command" if finding else None}]
                        if finding:
                            authored["semantic_review"]["adequacy_dimensions"][2]["status"] = "failed"
                            authored["semantic_review"]["findings"] = [{"id": "F-command", "candidate_ref": ref, "severity": "P2", "summary": "Supported endpoint fails.", "path": "app.txt", "status": "open"}]
                        else:
                            authored["route"] = "reapprove_plan"
                    # The host supplies only semantics. No private content helper
                    # or result identity is used before the real recorder.
                    recorded = fixture.wrapper("guru-check-task", "record-phase2-check.sh", "--task", fixture.task_ref,
                        "--input", fixture.write("semantic-command.json", authored))
                    artifact = Path(recorded["artifact_path"])
                    before = artifact.read_bytes()
                    checked = fixture.wrapper("guru-check-task", "check-phase2-check.sh", "--task", fixture.task_ref)
                    self.assertEqual(recorded["artifact_path"], checked["artifact_path"])
                    output = fixture.wrapper("guru-check-task", "invoke.sh", "--input", fixture.write("public-command.json", public),
                        "--owner-result", artifact)
                    self.assertEqual(exit_id, output["exit_id"])
                    self.assertEqual(before, artifact.read_bytes())
                    if exit_id == "passed":
                        # Recover the exact recorded result after its metadata write.
                        fixture.wrapper("guru-check-task", "check-phase2-check.sh", "--task", fixture.task_ref)
                        self.assertEqual(output, fixture.wrapper("guru-check-task", "invoke.sh", "--input", fixture.write("public-command.json", public),
                            "--owner-result", artifact))

    def test_current_planning_predecessor_is_required(self):
        public = self.public(self, "delivery_initial_check")
        public["planning_accepted_result_id"] = "planning:previous"
        result = self.invoke(self, public, self.owner(self), success=False)
        self.assertEqual("stale_identity", result["code"])


if __name__ == "__main__":
    unittest.main()
