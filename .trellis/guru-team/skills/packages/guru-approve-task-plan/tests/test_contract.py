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
        self.repo = self.package.parents[1]
        self.interface = self.read("interface.json")
        self.schema = self.read("schemas/planning-approval.schema.json")
        self.example = self.read("examples/planning-approval.json")

    def read(self, relative: str) -> dict:
        return json.loads((self.package / relative).read_text(encoding="utf-8"))

    def test_interface_declares_compact_private_owner_contract(self) -> None:
        self.assertEqual(self.interface["id"], "guru-approve-task-plan")
        self.assertEqual(self.interface["schema_version"], "1.3")
        self.assertEqual(self.interface["judgment_mode"], "semantic")
        expected = [
            "runtime_dependency", "task_workspace", "current_authority",
            "planning_documents", "docs_ssot", "wording_result",
            "issue_scope", "invocation_freshness",
        ]
        self.assertEqual(self.interface["modes"]["workflow"]["entry_precondition_ids"], expected)
        self.assertEqual(self.interface["modes"]["standalone"]["entry_precondition_ids"], expected)
        self.assertEqual(
            [(item["id"], item["consumer"]) for item in self.interface["external_exits"]],
            [
                ("approved", {"kind": "workflow", "id": "phase-1-task-activation"}),
                ("revision_required", {"kind": "skill", "id": "guru-approve-task-plan"}),
                ("clarify_scope", {"kind": "workflow", "id": "guru-task-plan-clarify-scope-router"}),
                ("blocked", {"kind": "stop", "id": "task-plan-approval-blocked"}),
            ],
        )
        private = self.interface["public_contracts"]["private_artifacts"]
        self.assertEqual(private[0]["persistence"], "ignored_runtime")
        self.assertTrue(private[0]["schema"]["schema_id"].endswith("guru-planning-approval-3.0.json"))
        self.assertRegex(self.example["reviewed_content_sha256"], r"^[0-9a-f]{64}$")
        self.assertIn(
            "Owner-private composite freshness token",
            self.schema["properties"]["reviewed_content_sha256"]["description"],
        )

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_interface_gate_inputs_outputs_and_consumer_examples_validate(self) -> None:
        from jsonschema import Draft202012Validator

        interface_schema = json.loads(
            (self.package.parents[1] / "schemas/skill-interface-1.3.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator(interface_schema).validate(self.interface)
        Draft202012Validator.check_schema(self.schema)
        Draft202012Validator(self.schema).validate(self.example)

        for name in ("initial-review", "revision-reentry", "clarification-reentry"):
            schema = self.read(f"schemas/public-{name}-input.schema.json")
            example = self.read(f"examples/public-{name}-input.json")
            Draft202012Validator(schema).validate(example)
        for name in ("approved", "revision-required", "clarify-scope", "blocked"):
            schema = self.read(f"schemas/public-{name}-output.schema.json")
            example = self.read(f"examples/public-{name}-output.json")
            Draft202012Validator(schema).validate(example)

        consumer_schema = json.loads(
            (self.repo / "consumers/workflow/production/approve-task-plan-approved.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator(consumer_schema).validate(
            self.read("examples/public-approved-output.json")
        )

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_compact_gate_has_four_closed_semantic_routes(self) -> None:
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(self.schema)
        cases = {
            "revision_required": {
                "status": "revision_required",
                "revision_actions": ["Revise the task-local plan."],
                "scope_proposals": [],
                "blocking_reasons": [],
                "consumer": {"kind": "skill", "id": "guru-approve-task-plan"},
            },
            "clarify_scope": {
                "status": "clarify_scope",
                "revision_actions": [],
                "scope_proposals": ["scope-proposal:R13"],
                "blocking_reasons": [],
                "consumer": {"kind": "workflow", "id": "guru-task-plan-clarify-scope-router"},
            },
            "blocked": {
                "status": "blocked",
                "revision_actions": [],
                "scope_proposals": [],
                "blocking_reasons": ["Current authority is unavailable."],
                "consumer": {"kind": "stop", "id": "task-plan-approval-blocked"},
            },
        }
        for typed_exit, case in cases.items():
            with self.subTest(typed_exit=typed_exit):
                payload = copy.deepcopy(self.example)
                payload["typed_exit"] = typed_exit
                payload["consumer"] = case.pop("consumer")
                payload["semantic_review"].update(case)
                validator.validate(payload)

        invalid = copy.deepcopy(self.example)
        invalid["semantic_review"]["scope_proposals"] = ["scope-proposal:R13"]
        self.assertFalse(validator.is_valid(invalid))

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
            ("record-planning-approval.sh", "planning_approval_recorder"),
            ("check-planning-approval.sh", "planning_approval_checker"),
        ):
            path = self.package / "scripts" / name
            self.assertTrue(path.stat().st_mode & 0o111)
            wrapper = path.read_text(encoding="utf-8")
            self.assertIn("run-skill-command.sh", wrapper)
            self.assertIn(f"--validator {validator}", wrapper)
            self.assertNotIn("guru_team_trellis.py", wrapper)

        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "guru-approve-task-plan"
            shutil.copytree(self.package, copied)
            result = subprocess.run(
                [str(copied / "scripts/record-planning-approval.sh"), "--help"],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("not self-contained or portable", result.stderr)

    def test_example_is_deidentified_and_current(self) -> None:
        encoded = json.dumps(self.example)
        self.assertNotIn("/Users/", encoded)
        self.assertEqual(self.example["schema_version"], "3.0")
        self.assertEqual(self.example["skill_id"], "guru-approve-task-plan")


if __name__ == "__main__":
    unittest.main()
