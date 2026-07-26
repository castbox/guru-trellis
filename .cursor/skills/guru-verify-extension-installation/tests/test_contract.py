from __future__ import annotations

import json
import stat
import unittest
from pathlib import Path

import jsonschema
from referencing import Registry, Resource


PACKAGE = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((PACKAGE / relative).read_text(encoding="utf-8"))


class ExtensionVerificationContractTests(unittest.TestCase):
    def test_interface_identity_and_semantic_profile(self) -> None:
        interface = load("interface.json")
        self.assertEqual(interface["schema_version"], "1.3")
        self.assertEqual(interface["id"], "guru-verify-extension-installation")
        self.assertEqual(interface["judgment_mode"], "semantic")
        self.assertEqual(
            interface["ordered_stages"],
            [
                "forward_behavior",
                "ai_review_gate",
                "conditional_human_confirmation",
                "recorder_validator",
                "typed_exit",
            ],
        )
        self.assertEqual(
            {item["id"] for item in interface["external_exits"]},
            {"verified", "not_required", "return_to_task_work", "blocked"},
        )

    def test_distinct_inputs_and_taskless_standalone_branch(self) -> None:
        workflow_schema = load("schemas/public-verification-required-input.schema.json")
        standalone_schema = load("schemas/public-standalone-verification-input.schema.json")
        workflow = load("examples/public-verification-required-input.json")
        standalone = load("examples/public-standalone-verification-input.json")
        jsonschema.Draft202012Validator(workflow_schema).validate(workflow)
        jsonschema.Draft202012Validator(standalone_schema).validate(standalone)
        self.assertFalse(jsonschema.Draft202012Validator(workflow_schema).is_valid(standalone))
        self.assertFalse(jsonschema.Draft202012Validator(standalone_schema).is_valid(workflow))
        self.assertNotIn("task_ref", standalone)
        with_task = {**standalone, "task_ref": ".trellis/tasks/current"}
        jsonschema.Draft202012Validator(standalone_schema).validate(with_task)

    def test_every_exit_uses_closed_mode_branches(self) -> None:
        for exit_id in ("verified", "not-required", "return-to-task-work", "blocked"):
            schema = load(f"schemas/public-{exit_id}-output.schema.json")
            branches = schema["oneOf"]
            self.assertEqual(len(branches), 2)
            self.assertEqual(
                {branch["properties"]["mode"]["const"] for branch in branches},
                {"workflow", "standalone"},
            )
            for branch in branches:
                self.assertFalse(branch["additionalProperties"])
                self.assertIn("exit_id", branch["required"])

    def test_public_outputs_exclude_private_state(self) -> None:
        forbidden = {
            "applicability",
            "verification_profile",
            "execution",
            "semantic_review",
            "machine_facts_sha256",
            "semantic_review_sha256",
            "facts_sha256",
        }
        for path in (PACKAGE / "schemas").glob("public-*-output.schema.json"):
            schema = json.loads(path.read_text(encoding="utf-8"))
            fields = {
                field
                for branch in schema["oneOf"]
                for field in branch["properties"]
            }
            self.assertFalse(fields & forbidden, path)

    def test_examples_validate_and_wrappers_are_executable(self) -> None:
        mapping = {
            "verified": "verified",
            "not-required": "not-required",
            "return-to-task-work": "return-to-task-work",
            "blocked": "blocked",
        }
        for schema_name, example_name in mapping.items():
            schema = load(f"schemas/public-{schema_name}-output.schema.json")
            example = load(f"examples/public-{example_name}-output.json")
            jsonschema.Draft202012Validator(schema).validate(example)
        private_schema = load("schemas/marketplace-verification.schema.json")
        private_example = load("examples/marketplace-verification.json")
        jsonschema.Draft202012Validator(private_schema).validate(private_example)
        for wrapper in (PACKAGE / "scripts").glob("*.sh"):
            self.assertTrue(wrapper.stat().st_mode & stat.S_IXUSR, wrapper)

    def test_recorder_input_schemas_resolve_private_contract_and_validate_examples(
        self,
    ) -> None:
        private_schema = load("schemas/marketplace-verification.schema.json")
        registry = Registry().with_resource(
            "marketplace-verification.schema.json",
            Resource.from_contents(private_schema),
        )
        cases = {
            "semantic-review-input": "semantic-review-input",
            "execution-facts": "execution-facts",
        }
        for schema_name, example_name in cases.items():
            with self.subTest(schema=schema_name):
                schema = load(f"schemas/{schema_name}.schema.json")
                example = load(f"examples/{example_name}.json")
                validator = jsonschema.Draft202012Validator(
                    schema,
                    registry=registry,
                )
                validator.validate(example)

        malformed_review = load("examples/semantic-review-input.json")
        malformed_review["redaction"] = "passed"
        review_validator = jsonschema.Draft202012Validator(
            load("schemas/semantic-review-input.schema.json"),
            registry=registry,
        )
        self.assertFalse(review_validator.is_valid(malformed_review))

        malformed_execution = load("examples/execution-facts.json")
        malformed_execution["status"] = "success"
        execution_validator = jsonschema.Draft202012Validator(
            load("schemas/execution-facts.schema.json"),
            registry=registry,
        )
        self.assertFalse(execution_validator.is_valid(malformed_execution))

    def test_session_only_input_has_no_task_work_route_fixture(self) -> None:
        standalone = load("examples/public-standalone-verification-input.json")
        self.assertNotIn("task_ref", standalone)
        returned = load("examples/public-return-to-task-work-output.json")
        self.assertEqual(returned["mode"], "workflow")
        self.assertIn("task_ref", returned)

    def test_private_execution_requires_installed_inventory_and_capability_bindings(
        self,
    ) -> None:
        private_schema = load("schemas/marketplace-verification.schema.json")
        registry = Registry().with_resource(
            "marketplace-verification.schema.json",
            Resource.from_contents(private_schema),
        )
        execution_schema = load("schemas/execution-facts.schema.json")
        validator = jsonschema.Draft202012Validator(
            execution_schema,
            registry=registry,
        )
        execution = load("examples/execution-facts.json")
        validator.validate(execution)

        inventory = execution["asset_inventory"]
        self.assertTrue(inventory["complete"])
        self.assertEqual(
            {item["id"] for item in inventory["categories"]},
            {"workflow", "preset", "schema", "skill", "platform"},
        )
        self.assertEqual(
            {item["category"] for item in execution["asset_expectations"]},
            {"workflow", "preset", "schema", "skill", "platform"},
        )
        self.assertTrue(
            all(item["command_refs"] and item["asset_paths"]
                for item in execution["capabilities"])
        )
        self.assertTrue(
            all(
                item["path"].startswith(".")
                for item in execution["asset_digests"]
            )
        )

        missing_inventory = json.loads(json.dumps(execution))
        del missing_inventory["asset_inventory"]
        self.assertFalse(validator.is_valid(missing_inventory))
        legacy_capability = json.loads(json.dumps(execution))
        capability = legacy_capability["capabilities"][0]
        capability["evidence_step"] = 0
        del capability["command_refs"]
        del capability["asset_paths"]
        self.assertFalse(validator.is_valid(legacy_capability))

    def test_no_secret_marker_in_contract_assets(self) -> None:
        marker = "synthetic-" + "secret-marker"
        for path in PACKAGE.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                self.assertNotIn(marker, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
