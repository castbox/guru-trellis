from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class CheckTaskPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.interface = json.loads((self.package / "interface.json").read_text(encoding="utf-8"))
        self.schema = json.loads((self.package / "schemas/phase2-check.schema.json").read_text(encoding="utf-8"))
        self.example = json.loads((self.package / "examples/phase2-check.json").read_text(encoding="utf-8"))

    def test_identity_modes_stages_runtime_and_exits(self) -> None:
        self.assertEqual(self.interface["id"], "guru-check-task")
        self.assertEqual(self.interface["schema_version"], "1.3")
        self.assertEqual(self.interface["judgment_mode"], "semantic")
        expected = [
            "runtime_dependency", "task_workspace", "approved_planning",
            "requirement_provenance", "implementation_handoff",
            "repository_check_inputs", "docs_ssot_plan", "issue_scope_ledger",
            "agent_assignment_recovery", "repository_snapshot",
            "invocation_freshness",
        ]
        self.assertEqual(self.interface["modes"]["workflow"]["entry_precondition_ids"], expected)
        self.assertEqual(self.interface["modes"]["standalone"]["entry_precondition_ids"], expected)
        self.assertEqual(self.interface["ordered_stages"], [
            "forward_behavior", "ai_review_gate", "conditional_human_confirmation",
            "recorder_validator", "typed_exit",
        ])
        self.assertEqual(
            [(item["id"], item["consumer"]) for item in self.interface["external_exits"]],
            [
                ("passed", {"kind": "skill", "id": "guru-create-task-commit"}),
                ("implementation_required", {"kind": "workflow", "id": "guru-resume-implementation"}),
                ("planning_stale", {"kind": "workflow", "id": "guru-task-check-planning-router"}),
                ("blocked", {"kind": "stop", "id": "task-check-blocked"}),
            ],
        )

    def test_skill_and_contract_keep_semantic_boundary(self) -> None:
        text = (self.package / "SKILL.md").read_text(encoding="utf-8") + (self.package / "references/contract.md").read_text(encoding="utf-8")
        for phrase in (
            "all eleven entry preconditions", "Classify every candidate issue",
            "official unchanged", "full\nrerun", "scope disposition", "never infer",
            "Legacy `--pass --coverage`", "not self-contained or portable",
        ):
            self.assertIn(phrase, text)
        for excluded in ("script decides scope", "worker produces Guru pass", "trellis/presets/guru-team/overlays/"):
            self.assertNotIn(excluded, text)

    def test_wrappers_are_dispatcher_only(self) -> None:
        for name, validator in (("record-phase2-check.sh", "phase2_check_recorder"), ("check-phase2-check.sh", "phase2_check_checker")):
            path = self.package / "scripts" / name
            self.assertTrue(path.stat().st_mode & 0o111)
            wrapper = path.read_text(encoding="utf-8")
            self.assertIn("run-skill-command.sh", wrapper)
            self.assertIn(f"--validator {validator}", wrapper)
            self.assertNotIn("guru_team_trellis.py", wrapper)

    def test_package_only_copy_fails_with_full_preset_remediation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "guru-check-task"
            shutil.copytree(self.package, copied)
            result = subprocess.run([str(copied / "scripts/record-phase2-check.sh"), "--help"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("not self-contained or portable", result.stderr)
            self.assertIn("complete Guru Team preset", result.stderr)

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_closed_schema_example_scope_order_and_four_exits(self) -> None:
        from jsonschema import Draft202012Validator

        Draft202012Validator.check_schema(self.schema)
        validator = Draft202012Validator(self.schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
        self.assertEqual(list(validator.iter_errors(self.example)), [])

        illegal = copy.deepcopy(self.example)
        illegal["scope_qualification"]["candidates"] = [{
            "id": "C1", "summary": "Untriggered proposal", "trigger_refs": [],
            "normal_path_reproduction": "Requires a scenario outside approved normal operation.",
            "disposition": "out_of_scope", "route_basis": "No approved trigger.",
            "severity": "P1", "finding_id": None,
        }]
        self.assertNotEqual(list(validator.iter_errors(illegal)), [])

        cases = [
            ("implementation_required", None, {"kind": "workflow", "id": "guru-resume-implementation"}),
            ("planning_stale", "reapprove_plan", {"kind": "workflow", "id": "guru-task-check-planning-router"}),
            ("planning_stale", "clarify_requirements", {"kind": "workflow", "id": "guru-task-check-planning-router"}),
            ("blocked", None, {"kind": "stop", "id": "task-check-blocked"}),
        ]
        for typed_exit, route, consumer in cases:
            with self.subTest(typed_exit=typed_exit, route=route):
                payload = copy.deepcopy(self.example)
                payload["typed_exit"] = typed_exit
                payload["route"] = route
                payload["consumer"] = consumer
                payload["semantic_review"]["ai_review_gate"]["status"] = typed_exit
                if typed_exit == "implementation_required":
                    payload["scope_qualification"]["candidates"] = [{
                        "id": "C1", "summary": "Open current-scope defect",
                        "trigger_refs": ["PRD R6"],
                        "normal_path_reproduction": "Reproduces on a supported normal path.",
                        "disposition": "current_scope", "route_basis": "Implementation fix.",
                        "severity": "P2", "finding_id": "F1",
                    }]
                    payload["semantic_review"]["findings"] = [{
                        "id": "F1", "candidate_id": "C1", "severity": "P2",
                        "summary": "Open defect.", "path": "example.py",
                        "blocking": True, "status": "open",
                    }]
                elif typed_exit == "planning_stale":
                    payload["scope_qualification"]["candidates"] = [{
                        "id": "C1", "summary": "Approved scope must change",
                        "trigger_refs": ["PRD R4"],
                        "normal_path_reproduction": "A supported path requires a scope change.",
                        "disposition": "scope_change_required", "route_basis": "Return to planning.",
                        "severity": None, "finding_id": None,
                    }]
                elif typed_exit == "blocked":
                    payload["check_execution"]["unverified_items"] = [{
                        "id": "U1", "command_or_area": "integration test",
                        "reason": "Dependency unavailable.",
                        "impact": "A reliable complete check cannot be formed.",
                        "blocking": True,
                    }]
                self.assertEqual(list(validator.iter_errors(payload)), [])

        ambiguous = copy.deepcopy(self.example)
        ambiguous["typed_exit"] = "planning_stale"
        ambiguous["semantic_review"]["ai_review_gate"]["status"] = "planning_stale"
        ambiguous["route"] = None
        ambiguous["consumer"] = {"kind": "workflow", "id": "guru-task-check-planning-router"}
        self.assertNotEqual(list(validator.iter_errors(ambiguous)), [])

        missing_assignment = copy.deepcopy(self.example)
        missing_assignment["agent_assignment"]["artifact_path"] = None
        self.assertNotEqual(list(validator.iter_errors(missing_assignment)), [])

        empty_check_agents = copy.deepcopy(self.example)
        empty_check_agents["agent_assignment"]["check_agent_ids"] = []
        self.assertNotEqual(list(validator.iter_errors(empty_check_agents)), [])

        nonblocking_finding = copy.deepcopy(self.example)
        nonblocking_finding["scope_qualification"]["candidates"] = [{
            "id": "C1", "summary": "Open current-scope defect",
            "trigger_refs": ["PRD R6"],
            "normal_path_reproduction": "Reproduces on a supported normal path.",
            "disposition": "current_scope", "route_basis": "Implementation fix.",
            "severity": "P3", "finding_id": "F1",
        }]
        nonblocking_finding["semantic_review"]["findings"] = [{
            "id": "F1", "candidate_id": "C1", "severity": "P3",
            "summary": "Open defect.", "path": "example.py",
            "blocking": False, "status": "open",
        }]
        self.assertNotEqual(list(validator.iter_errors(nonblocking_finding)), [])

        missing_current_finding = copy.deepcopy(self.example)
        missing_current_finding["scope_qualification"]["candidates"] = [{
            "id": "C1", "summary": "Current-scope defect",
            "trigger_refs": ["PRD R6"],
            "normal_path_reproduction": "Reproduces on a supported normal path.",
            "disposition": "current_scope", "route_basis": "Implementation fix.",
            "severity": "P1", "finding_id": None,
        }]
        self.assertNotEqual(list(validator.iter_errors(missing_current_finding)), [])

        unsupported_blocked = copy.deepcopy(self.example)
        unsupported_blocked["typed_exit"] = "blocked"
        unsupported_blocked["consumer"] = {"kind": "stop", "id": "task-check-blocked"}
        unsupported_blocked["semantic_review"]["ai_review_gate"]["status"] = "blocked"
        self.assertNotEqual(list(validator.iter_errors(unsupported_blocked)), [])

        unsupported_planning = copy.deepcopy(self.example)
        unsupported_planning["typed_exit"] = "planning_stale"
        unsupported_planning["route"] = "reapprove_plan"
        unsupported_planning["consumer"] = {"kind": "workflow", "id": "guru-task-check-planning-router"}
        unsupported_planning["semantic_review"]["ai_review_gate"]["status"] = "planning_stale"
        self.assertNotEqual(list(validator.iter_errors(unsupported_planning)), [])

        blocker_with_planning_exit = copy.deepcopy(self.example)
        blocker_with_planning_exit["typed_exit"] = "planning_stale"
        blocker_with_planning_exit["route"] = "reapprove_plan"
        blocker_with_planning_exit["consumer"] = {
            "kind": "workflow", "id": "guru-task-check-planning-router",
        }
        blocker_with_planning_exit["semantic_review"]["ai_review_gate"]["status"] = "planning_stale"
        blocker_with_planning_exit["scope_qualification"]["candidates"] = [{
            "id": "C1", "summary": "Scope change", "trigger_refs": ["PRD R4"],
            "normal_path_reproduction": "Normal path requires scope change.",
            "disposition": "scope_change_required", "route_basis": "Return to planning.",
            "severity": None, "finding_id": None,
        }]
        blocker_with_planning_exit["check_execution"]["unverified_items"] = [{
            "id": "U1", "command_or_area": "integration test",
            "reason": "Dependency unavailable.", "impact": "Coverage incomplete.",
            "blocking": True,
        }]
        self.assertNotEqual(list(validator.iter_errors(blocker_with_planning_exit)), [])

    def test_example_is_deidentified_and_package_local(self) -> None:
        encoded = json.dumps(self.example)
        self.assertNotIn("/Users/", encoded)
        self.assertNotIn("07-19-130", encoded)
        self.assertEqual(self.example["schema_version"], "2.0")
        self.assertEqual(self.example["skill_id"], "guru-check-task")

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_schema_rejects_duplicate_semantic_collection_items(self) -> None:
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(self.schema)

        duplicate_candidate = copy.deepcopy(self.example)
        candidate = {
            "id": "C1", "summary": "Follow-up proposal", "trigger_refs": ["PRD R4"],
            "normal_path_reproduction": "A supported path suggests later work.",
            "disposition": "followup_proposal", "route_basis": "Track separately.",
            "severity": None, "finding_id": None,
        }
        duplicate_candidate["scope_qualification"]["candidates"] = [candidate, copy.deepcopy(candidate)]

        duplicate_unverified = copy.deepcopy(self.example)
        unverified = {
            "id": "U1", "command_or_area": "integration test",
            "reason": "Dependency unavailable.", "impact": "Coverage is partial.",
            "blocking": False,
        }
        duplicate_unverified["check_execution"]["unverified_items"] = [
            unverified, copy.deepcopy(unverified),
        ]

        duplicate_finding = copy.deepcopy(self.example)
        duplicate_finding["typed_exit"] = "implementation_required"
        duplicate_finding["consumer"] = {
            "kind": "workflow", "id": "guru-resume-implementation",
        }
        duplicate_finding["semantic_review"]["ai_review_gate"]["status"] = "implementation_required"
        duplicate_finding["scope_qualification"]["candidates"] = [{
            "id": "C1", "summary": "Open current-scope defect", "trigger_refs": ["PRD R6"],
            "normal_path_reproduction": "Reproduces on a supported normal path.",
            "disposition": "current_scope", "route_basis": "Implementation fix.",
            "severity": "P2", "finding_id": "F1",
        }]
        finding = {
            "id": "F1", "candidate_id": "C1", "severity": "P2",
            "summary": "Open defect.", "path": "example.py",
            "blocking": True, "status": "open",
        }
        duplicate_finding["semantic_review"]["findings"] = [finding, copy.deepcopy(finding)]

        duplicate_dimension = copy.deepcopy(self.example)
        duplicate_dimension["semantic_review"]["adequacy_dimensions"][-1] = copy.deepcopy(
            duplicate_dimension["semantic_review"]["adequacy_dimensions"][0]
        )

        for payload in (
            duplicate_candidate,
            duplicate_unverified,
            duplicate_finding,
            duplicate_dimension,
        ):
            with self.subTest(collection=payload):
                self.assertFalse(validator.is_valid(payload))


if __name__ == "__main__":
    unittest.main()
