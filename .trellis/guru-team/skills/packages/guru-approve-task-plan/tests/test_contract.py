from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class ApproveTaskPlanPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.interface = json.loads((self.package / "interface.json").read_text(encoding="utf-8"))
        self.schema = json.loads(
            (self.package / "schemas/planning-approval.schema.json").read_text(encoding="utf-8")
        )
        self.example = json.loads(
            (self.package / "examples/planning-approval.json").read_text(encoding="utf-8")
        )

    def test_identity_modes_stages_runtime_and_exits(self) -> None:
        self.assertEqual(self.interface["id"], "guru-approve-task-plan")
        self.assertEqual(self.interface["schema_version"], "1.2")
        self.assertEqual(self.interface["judgment_mode"], "semantic")
        workflow = self.interface["modes"]["workflow"]
        standalone = self.interface["modes"]["standalone"]
        self.assertEqual(workflow["routing"], "global_workflow")
        self.assertEqual(standalone["routing"], "direct_discovery")
        self.assertEqual(workflow["entry_precondition_ids"], standalone["entry_precondition_ids"])
        self.assertEqual(
            workflow["entry_precondition_ids"],
            [
                "runtime_dependency",
                "task_workspace",
                "requirement_authority",
                "planning_artifacts",
                "docs_ssot_plan",
                "contract_wording_evidence",
                "scope_ledger",
                "repository_snapshot",
                "invocation_freshness",
            ],
        )
        self.assertEqual(
            self.interface["ordered_stages"],
            [
                "forward_behavior",
                "ai_review_gate",
                "conditional_human_confirmation",
                "recorder_validator",
                "typed_exit",
            ],
        )
        self.assertEqual(
            {item["id"]: item["runtime_command"] for item in self.interface["validators"]},
            {
                "planning_approval_recorder": "record-planning-approval",
                "planning_approval_checker": "check-planning-approval",
            },
        )
        self.assertEqual(
            [(item["id"], item["consumer"]) for item in self.interface["external_exits"]],
            [
                ("approved", {"kind": "workflow", "id": "phase-1-task-activation"}),
                ("revision_required", {"kind": "skill", "id": "guru-approve-task-plan"}),
                ("clarify_scope", {"kind": "skill", "id": "guru-clarify-requirements"}),
                ("blocked", {"kind": "stop", "id": "task-plan-approval-blocked"}),
            ],
        )

    def test_skill_and_contract_keep_semantic_boundary(self) -> None:
        skill = (self.package / "SKILL.md").read_text(encoding="utf-8")
        contract = (self.package / "references/contract.md").read_text(encoding="utf-8")
        for phrase in (
            "all nine entry preconditions",
            "dedicated proposal confirmation",
            "post-planning confirmation",
            "Return exactly one",
            "not self-contained or portable",
        ):
            self.assertIn(phrase, skill)
        for phrase in (
            "judgment_mode=semantic",
            "explicit_requirement",
            "necessary_implementation_choice",
            "approved_scope_expansion",
            "out_of_scope_proposal",
            "dedicated-unusual-scenario",
            "proposal_binding",
            "authority_binding",
            "caller-declared digest",
            "phase-1-task-activation",
            "schema_version=2.0",
            "never infer or generate provenance",
            "do not alone make planning stale",
        ):
            self.assertIn(phrase, contract)
        combined = skill + contract + json.dumps(self.interface)
        for forbidden in (
            "script decides adequacy",
            "script selects provenance",
            "generic confirmation satisfies",
            "trellis/presets/guru-team/overlays/",
        ):
            self.assertNotIn(forbidden, combined)

    def test_wrappers_are_dispatcher_only(self) -> None:
        for name, validator in (
            ("record-planning-approval.sh", "planning_approval_recorder"),
            ("check-planning-approval.sh", "planning_approval_checker"),
        ):
            path = self.package / "scripts" / name
            self.assertTrue(path.stat().st_mode & 0o111)
            wrapper = path.read_text(encoding="utf-8")
            self.assertIn("run-skill-command.sh", wrapper)
            self.assertIn(f"--validator {validator}", wrapper)
            self.assertNotIn("guru_team_trellis.py", wrapper)

    def test_package_only_copy_fails_with_full_preset_remediation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "guru-approve-task-plan"
            shutil.copytree(self.package, copied)
            for name in ("record-planning-approval.sh", "check-planning-approval.sh"):
                result = subprocess.run(
                    [str(copied / "scripts" / name), "--help"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(result.returncode, 2, result)
                self.assertIn("not self-contained or portable", result.stderr)
                self.assertIn("Install or upgrade the complete Guru Team preset", result.stderr)

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_closed_schema_example_and_four_exit_union(self) -> None:
        from jsonschema import Draft202012Validator

        Draft202012Validator.check_schema(self.schema)
        validator = Draft202012Validator(self.schema)
        self.assertEqual(list(validator.iter_errors(self.example)), [])

        cases = {
            "revision_required": (
                "revision_required",
                {"kind": "skill", "id": "guru-approve-task-plan"},
                {"revision_actions": ["Revise the task-local test plan."]},
            ),
            "clarify_scope": (
                "clarify_scope",
                {"kind": "skill", "id": "guru-clarify-requirements"},
                {"scope_proposals": ["Confirm the proposed authority change."]},
            ),
            "blocked": (
                "blocked",
                {"kind": "stop", "id": "task-plan-approval-blocked"},
                {"blocking_reasons": ["The source authority is unavailable."]},
            ),
        }
        for typed_exit, (status, consumer, updates) in cases.items():
            with self.subTest(typed_exit=typed_exit):
                payload = copy.deepcopy(self.example)
                payload["typed_exit"] = typed_exit
                payload["consumer"] = consumer
                payload["semantic_review"]["ai_review_gate"]["status"] = status
                payload["user_confirmation"] = {
                    "kind": "not-required",
                    "status": "not_required",
                    "prompt_presented_at": None,
                    "confirmed_at": None,
                    "evidence_summary": "This exit does not activate the task.",
                }
                payload["semantic_review"]["ai_review_gate"].update(updates)
                self.assertEqual(list(validator.iter_errors(payload)), [])

        invalid = copy.deepcopy(self.example)
        invalid["consumer"] = {"kind": "skill", "id": "guru-approve-task-plan"}
        self.assertNotEqual(list(validator.iter_errors(invalid)), [])

        for field in (
            "findings",
            "revision_actions",
            "scope_proposals",
            "blocking_reasons",
        ):
            with self.subTest(approved_gate_field=field):
                invalid = copy.deepcopy(self.example)
                invalid["semantic_review"]["ai_review_gate"][field] = [
                    "A passed gate cannot retain unresolved review state."
                ]
                self.assertNotEqual(list(validator.iter_errors(invalid)), [])

        for field in ("prompt_presented_at", "confirmed_at"):
            with self.subTest(approved_confirmation_field=field):
                invalid = copy.deepcopy(self.example)
                invalid["user_confirmation"][field] = None
                self.assertNotEqual(list(validator.iter_errors(invalid)), [])

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_provenance_and_dedicated_confirmation_are_closed(self) -> None:
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(self.schema)
        invalid_choice = copy.deepcopy(self.example)
        entry = invalid_choice["provenance_review"]["entries"][0]
        entry["classification"] = "necessary_implementation_choice"
        self.assertNotEqual(list(validator.iter_errors(invalid_choice)), [])

        invalid_confirmation = copy.deepcopy(self.example)
        invalid_confirmation["unusual_scenario_review"]["candidates"] = [
            {
                "id": "U1",
                "scenario_class": "other_nonstandard",
                "trigger_evidence": "A proposal adds non-required locking.",
                "scope": "Task-local runtime",
                "cost": "Additional complexity",
                "alternatives": ["Remove the mechanism"],
                "consequence": "The task scope expands.",
                "source_requirement_refs": [],
                "proposal_sha256": "1" * 64,
                "disposition": "confirmed_scope_expansion",
                "confirmation": {
                    "confirmation_kind": "post-planning-approval",
                    "proposal_sha256": "1" * 64,
                    "confirmation_summary": "Generic confirmation is invalid here.",
                    "confirmed_at": "2026-01-15T09:32:00Z",
                    "authority_ref": "issue:27",
                },
            }
        ]
        self.assertNotEqual(list(validator.iter_errors(invalid_confirmation)), [])

        empty_alternatives = copy.deepcopy(invalid_confirmation)
        candidate = empty_alternatives["unusual_scenario_review"]["candidates"][0]
        candidate["disposition"] = "mechanism_removed"
        candidate["confirmation"] = None
        candidate["alternatives"] = []
        self.assertNotEqual(list(validator.iter_errors(empty_alternatives)), [])

        explicit_without_authority = copy.deepcopy(empty_alternatives)
        candidate = explicit_without_authority["unusual_scenario_review"]["candidates"][0]
        candidate["disposition"] = "explicit_requirement"
        candidate["alternatives"] = ["Keep the explicit requirement bounded."]
        candidate["source_requirement_refs"] = []
        self.assertNotEqual(list(validator.iter_errors(explicit_without_authority)), [])

        valid_scope_expansion = copy.deepcopy(self.example)
        entry = valid_scope_expansion["provenance_review"]["entries"][0]
        entry["classification"] = "approved_scope_expansion"
        entry["scope_expansion"] = {
            "proposal_binding": {
                "source_kind": "planning_artifact",
                "artifact_path": ".trellis/tasks/example-task/prd.md",
                "locator": "R1. Task plan approval owner",
                "unusual_candidate_id": None,
                "proposal_sha256": "1" * 64,
            },
            "confirmation": {
                "confirmation_kind": "dedicated-scope-expansion",
                "proposal_sha256": "1" * 64,
                "confirmation_summary": "The user confirmed this exact proposal.",
                "confirmed_at": "2026-01-15T09:32:00Z",
            },
            "authority_binding": {
                "authority_ref": "issue:27",
                "authority_sha256": "4" * 64,
                "proposal_sha256": "1" * 64,
            },
        }
        self.assertEqual(list(validator.iter_errors(valid_scope_expansion)), [])

        legacy_caller_digest = copy.deepcopy(valid_scope_expansion)
        legacy_caller_digest["provenance_review"]["entries"][0]["scope_expansion"] = {
            "proposal_sha256": "1" * 64,
            "confirmation_kind": "dedicated-scope-expansion",
            "confirmation_summary": "A caller-only digest has no canonical proposal source.",
            "confirmed_at": "2026-01-15T09:32:00Z",
            "authority_ref": "issue:27",
        }
        self.assertNotEqual(list(validator.iter_errors(legacy_caller_digest)), [])

    def test_example_is_deidentified_and_package_local(self) -> None:
        encoded = json.dumps(self.example)
        self.assertNotIn("/Users/", encoded)
        self.assertNotIn("07-19-129", encoded)
        self.assertEqual(self.example["schema_version"], "2.0")
        self.assertEqual(self.example["skill_id"], "guru-approve-task-plan")


if __name__ == "__main__":
    unittest.main()
