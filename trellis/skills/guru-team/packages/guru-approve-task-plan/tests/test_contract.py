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

    def test_planning_artifact_resolution_is_package_owned_and_compatible(self) -> None:
        command = next(
            item for item in self.read("commands.json")["commands"]
            if item["id"] == "resolve-planning-artifacts"
        )
        self.assertEqual(command["entrypoint"], "runtime/check.py")
        self.assertEqual(command["runtime_role"], "check")
        self.assertEqual(command["side_effect"], "repo_read")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            task = root / ".trellis/tasks/08-12-example"
            task.mkdir(parents=True)
            (task / "prd.md").write_text("# PRD\n", encoding="utf-8")
            wrapper = self.package / "scripts/resolve-human-artifacts.sh"
            result = subprocess.run(
                [str(wrapper), "--root", str(root), "--task", str(task), "--json"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["task_dir_relative"], ".trellis/tasks/08-12-example")
            self.assertEqual(
                [item["exists"] for item in payload["markdown_artifacts"]],
                [True, False, False],
            )
            self.assertEqual(payload["markdown_artifacts"][0]["status"], "已生成")

    def test_artifact_help_and_compatibility_wrapper_route_to_package(self) -> None:
        root = self.package.parents[4]
        wrapper = (
            root / "trellis/workflows/guru-team/scripts/bash/resolve-human-artifacts.sh"
            if (root / "trellis/skills/guru-team").is_dir()
            else root / ".trellis/guru-team/scripts/bash/resolve-human-artifacts.sh"
        )
        for target in (self.package / "scripts/resolve-human-artifacts.sh", wrapper):
            result = subprocess.run(
                [str(target), "--help"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            self.assertIn("usage: resolve-planning-artifacts", result.stdout)
            self.assertIn("owner: guru-approve-task-plan", result.stdout)


    def test_interface_declares_compact_private_owner_contract(self) -> None:
        self.assertEqual(self.interface["id"], "guru-approve-task-plan")
        self.assertEqual(self.interface["schema_version"], "1.4")
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
            (self.package.parents[1] / self.interface["$schema"].removeprefix("../../")).read_text(encoding="utf-8")
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

    def test_public_invoke_consumes_only_the_exact_successful_owner_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-b", "main", str(root)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            task_ref = ".trellis/tasks/08-12-planning-consumption"
            task_dir = root / task_ref
            task_dir.mkdir(parents=True)
            checkpoint = root / ".trellis/.runtime/guru-team/owner-checkpoints/08-12-planning-consumption/planning-approval.json"
            checkpoint.parent.mkdir(parents=True)
            owner = copy.deepcopy(self.example)
            owner["mode"] = "workflow"
            owner["task_ref"] = task_ref
            owner["planning_paths"] = [f"{task_ref}/{name}" for name in ("prd.md", "design.md", "implement.md")]
            checkpoint.write_text(json.dumps(owner), encoding="utf-8")
            public_input = root / "public-input.json"
            public_input.write_text(json.dumps({"mode": "workflow", "task_ref": task_ref}), encoding="utf-8")

            result = subprocess.run(
                [str(self.package / "scripts/invoke.sh"), "--root", str(root), "--input", "public-input.json", "--owner-result", checkpoint.relative_to(root).as_posix()],
                cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            self.assertEqual(json.loads(result.stdout), {"exit_id": "approved", "task_ref": task_ref})
            self.assertFalse(checkpoint.exists())
            self.assertFalse(checkpoint.parent.exists())

            checkpoint.parent.mkdir(parents=True)
            checkpoint.write_text(json.dumps(owner), encoding="utf-8")
            public_input.write_text(json.dumps({"mode": "workflow", "task_ref": ".trellis/tasks/other"}), encoding="utf-8")
            mismatch = subprocess.run(
                [str(self.package / "scripts/invoke.sh"), "--root", str(root), "--input", "public-input.json", "--owner-result", checkpoint.relative_to(root).as_posix()],
                cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertNotEqual(mismatch.returncode, 0, mismatch)
            self.assertTrue(checkpoint.is_file())

    def test_wrappers_are_dispatcher_only_and_package_is_not_portable(self) -> None:
        for name, validator in (
            ("record-planning-approval.sh", "planning_approval_recorder"),
            ("check-planning-approval.sh", "planning_approval_checker"),
        ):
            path = self.package / "scripts" / name
            self.assertTrue(path.stat().st_mode & 0o111)
            wrapper = path.read_text(encoding="utf-8")
            self.assertIn("runtime/launch.sh", wrapper)
            runtime_command = next(item["runtime_command"] for item in self.interface["validators"] if item["id"] == validator)
            self.assertIn(f'source "$LAUNCHER" {runtime_command}', wrapper)
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
