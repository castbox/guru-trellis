from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]


def validate(schema_path: Path, value: dict) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(value)


class CheckoutPackageContractTests(unittest.TestCase):
    def test_interface_is_valid_but_package_is_not_registered_or_projected(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        validate(SKILLS / "schemas/skill-interface-1.4.schema.json", interface)
        registry = json.loads((SKILLS / "registry.json").read_text(encoding="utf-8"))
        self.assertNotIn("guru-ensure-task-checkout", {row["id"] for row in registry["skills"]})
        root = SKILLS.parents[2]
        self.assertFalse((root / ".trellis/guru-team/skills/packages/guru-ensure-task-checkout").exists())

    def test_examples_and_consumers_validate(self) -> None:
        pairs = [
            ("schemas/public-ensure-input.schema.json", "examples/public-ensure-input.json"),
            ("schemas/public-resume-input.schema.json", "examples/public-resume-input.json"),
            ("schemas/semantic-result.schema.json", "examples/semantic-ready.json"),
            ("schemas/semantic-result.schema.json", "examples/semantic-resume.json"),
            ("schemas/semantic-result.schema.json", "examples/semantic-blocked.json"),
            ("consumers/workflow/production/task-checkout-ready.schema.json", "consumers/workflow/production/task-checkout-ready.example.json"),
            ("consumers/stop/production/task-checkout-acquisition-blocked.schema.json", "consumers/stop/production/task-checkout-acquisition-blocked.example.json"),
        ]
        for schema, example in pairs:
            with self.subTest(example=example):
                validate(PACKAGE / schema, json.loads((PACKAGE / example).read_text(encoding="utf-8")))

    def test_public_outputs_are_minimal_and_path_free(self) -> None:
        for name in ["public-checkout-ready-output.schema.json", "public-resume-output.schema.json", "public-blocked-output.schema.json"]:
            text = (PACKAGE / "schemas" / name).read_text(encoding="utf-8")
            for forbidden in ["checkout_path", "worktree_path", "head", "authorization", "session_id"]:
                self.assertNotIn(forbidden, text)

    def test_package_identity_schemas_match_shared_task_grammar(self) -> None:
        public_input = json.loads((PACKAGE / "examples/public-ensure-input.json").read_text(encoding="utf-8"))
        schema = PACKAGE / "schemas/public-ensure-input.schema.json"
        invalid = [
            {**public_input, "task_artifact": {**public_input["task_artifact"], "task_id": "bad task"}},
            {**public_input, "task_artifact": {**public_input["task_artifact"], "task_ref": ".trellis/tasks/../escape"}},
            {**public_input, "branch_binding_ref": {**public_input["branch_binding_ref"], "task_id": "bad task"}},
        ]
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValidationError):
                validate(schema, value)


if __name__ == "__main__":
    unittest.main()
