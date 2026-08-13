from __future__ import annotations

import copy
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class CheckTaskPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.interface = self.read("interface.json")
        self.schema = self.read("schemas/phase2-check.schema.json")
        self.example = self.read("examples/phase2-check.json")

    def read(self, relative: str) -> dict:
        return json.loads((self.package / relative).read_text(encoding="utf-8"))

    def test_interface_declares_compact_private_owner_contract(self) -> None:
        self.assertEqual(self.interface["id"], "guru-check-task")
        self.assertEqual(self.interface["schema_version"], "1.4")
        self.assertEqual(self.interface["judgment_mode"], "semantic")
        expected = [
            "runtime_dependency", "task_workspace", "approved_planning",
            "live_implementation", "validation_scope", "docs_ssot",
            "issue_scope", "invocation_freshness",
        ]
        self.assertEqual(self.interface["modes"]["workflow"]["entry_precondition_ids"], expected)
        self.assertEqual(self.interface["modes"]["standalone"]["entry_precondition_ids"], expected)
        self.assertEqual(
            [(item["id"], item["consumer"]) for item in self.interface["external_exits"]],
            [
                ("passed", {"kind": "skill", "id": "guru-create-task-commit"}),
                ("implementation_required", {"kind": "workflow", "id": "guru-resume-implementation"}),
                ("planning_stale", {"kind": "workflow", "id": "guru-task-check-planning-router"}),
                ("blocked", {"kind": "stop", "id": "task-check-blocked"}),
            ],
        )
        private = self.interface["public_contracts"]["private_artifacts"]
        self.assertEqual(private[0]["persistence"], "ignored_runtime")
        self.assertTrue(private[0]["schema"]["schema_id"].endswith("guru-phase2-check-4.0.json"))
        self.assertRegex(self.example["reviewed_content_sha256"], r"^[0-9a-f]{64}$")
        self.assertIn(
            "guru-reviewed-content-1.0",
            self.schema["properties"]["reviewed_content_sha256"]["description"],
        )

    def test_interface_gate_inputs_and_outputs_validate(self) -> None:
        from jsonschema import Draft202012Validator

        interface_schema = json.loads(
            (self.package.parents[1] / self.interface["$schema"].removeprefix("../../")).read_text(encoding="utf-8")
        )
        Draft202012Validator(interface_schema).validate(self.interface)
        Draft202012Validator.check_schema(self.schema)
        Draft202012Validator(self.schema).validate(self.example)

        for name in ("initial-check", "finding-fix-rerun", "planning-reentry"):
            Draft202012Validator(self.read(f"schemas/public-{name}-input.schema.json")).validate(
                self.read(f"examples/public-{name}-input.json")
            )
        for name in ("passed", "implementation-required", "planning-stale", "blocked"):
            Draft202012Validator(self.read(f"schemas/public-{name}-output.schema.json")).validate(
                self.read(f"examples/public-{name}-output.json")
            )

    def test_compact_gate_has_four_closed_semantic_routes(self) -> None:
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(self.schema)

        implementation = copy.deepcopy(self.example)
        implementation["typed_exit"] = "implementation_required"
        implementation["consumer"] = {"kind": "workflow", "id": "guru-resume-implementation"}
        implementation["semantic_review"]["status"] = "implementation_required"
        implementation["semantic_review"]["adequacy_dimensions"][2]["status"] = "failed"
        implementation["semantic_review"]["scope_decisions"] = [{
            "id": "C1", "disposition": "current_scope",
            "summary": "A supported current-scope defect remains.",
            "normal_path_reproduction": "The supported path reproduces the defect.",
            "finding_id": "F1",
        }]
        implementation["semantic_review"]["findings"] = [{
            "id": "F1", "severity": "P2", "summary": "Open defect.",
            "path": "src/example.py", "status": "open",
        }]
        validator.validate(implementation)

        planning = copy.deepcopy(self.example)
        planning["typed_exit"] = "planning_stale"
        planning["route"] = "reapprove_plan"
        planning["consumer"] = {"kind": "workflow", "id": "guru-task-check-planning-router"}
        planning["semantic_review"]["status"] = "planning_stale"
        planning["semantic_review"]["scope_decisions"] = [{
            "id": "scope-proposal:R13", "disposition": "scope_change_required",
            "summary": "The current authority changes scope.",
            "normal_path_reproduction": "A supported path requires the scope change.",
            "finding_id": None,
        }]
        validator.validate(planning)

        blocked = copy.deepcopy(self.example)
        blocked["typed_exit"] = "blocked"
        blocked["consumer"] = {"kind": "stop", "id": "task-check-blocked"}
        blocked["semantic_review"]["status"] = "blocked"
        blocked["semantic_review"]["adequacy_dimensions"][-1]["status"] = "blocked"
        blocked["validation"]["unverified_items"] = [{
            "id": "U1", "summary": "Required integration evidence is unavailable.",
            "blocking": True,
        }]
        validator.validate(blocked)

        invalid_pass = copy.deepcopy(self.example)
        invalid_pass["semantic_review"]["findings"] = implementation["semantic_review"]["findings"]
        self.assertFalse(validator.is_valid(invalid_pass))

    def test_public_inputs_only_route_owner_entry(self) -> None:
        forbidden = {
            "adequacy_review", "ai_review_gate", "evidence_locators",
            "exit_intent", "findings", "provenance_review",
            "scope_dispositions", "unusual_scenario_dispositions",
            "unverified_conclusions",
        }
        for path in sorted((self.package / "schemas").glob("public-*input.schema.json")):
            properties = self.read(path.relative_to(self.package).as_posix()).get("properties", {})
            self.assertTrue(forbidden.isdisjoint(properties), path)

    def test_package_json_has_no_authorization_or_routine_handoff_fields(self) -> None:
        forbidden = {
            "agent_assignment", "confirmation", "confirmation_ref",
            "confirmation_sha256", "confirmed_plan_digest", "human_authorization",
            "human_confirmation", "implementation_handoff", "liveness",
            "review_report", "review_reports", "user_confirmation",
        }

        def keys(value: object) -> set[str]:
            if isinstance(value, dict):
                return set(value) | set().union(*(keys(item) for item in value.values()), set())
            if isinstance(value, list):
                return set().union(*(keys(item) for item in value), set())
            return set()

        for path in sorted(self.package.rglob("*.json")):
            self.assertTrue(forbidden.isdisjoint(keys(json.loads(path.read_text(encoding="utf-8")))), path)

    def test_wrappers_are_dispatcher_only_and_package_is_not_portable(self) -> None:
        for name, validator in (
            ("record-phase2-check.sh", "phase2_check_recorder"),
            ("check-phase2-check.sh", "phase2_check_checker"),
        ):
            path = self.package / "scripts" / name
            self.assertTrue(path.stat().st_mode & 0o111)
            wrapper = path.read_text(encoding="utf-8")
            self.assertIn("runtime/launch.sh", wrapper)
            runtime_command = next(item["runtime_command"] for item in self.interface["validators"] if item["id"] == validator)
            self.assertIn(f'source "$LAUNCHER" {runtime_command}', wrapper)
            self.assertNotIn("guru_team_trellis.py", wrapper)

        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "guru-check-task"
            shutil.copytree(self.package, copied)
            result = subprocess.run(
                [str(copied / "scripts/record-phase2-check.sh"), "--help"],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("not self-contained or portable", result.stderr)

    def test_example_is_deidentified_and_current(self) -> None:
        encoded = json.dumps(self.example)
        self.assertNotIn("/Users/", encoded)
        self.assertEqual(self.example["schema_version"], "4.0")
        self.assertEqual(self.example["skill_id"], "guru-check-task")


if __name__ == "__main__":
    unittest.main()
