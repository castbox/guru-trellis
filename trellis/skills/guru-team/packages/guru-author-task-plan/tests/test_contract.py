import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
sys.path.insert(0, str(SKILLS))
from runtime.schema import validate_json


def load(path):
    return json.loads((PACKAGE / path).read_text())


class ContractTest(unittest.TestCase):
    def test_profiles_and_target_owned_consumer_projections(self):
        interface = load("interface.json")
        profiles = interface["public_contracts"]["input"]["profiles"]
        self.assertEqual(len(profiles), 9)
        for row in profiles:
            example = load(row["example"]["path"])
            validate_json(example, PACKAGE / row["schema"]["path"], "example")
            self.assertEqual(example["profile"], row["id"])
        consumers = {row["id"]: row for row in interface["public_contracts"]["consumer_inputs"]}
        projections = {row["exit_id"]: row for row in interface["public_contracts"]["projections"]}
        for row in interface["public_contracts"]["outputs"]:
            output = load(row["example"]["path"])
            validate_json(output, PACKAGE / row["schema"]["path"], "output")
            consumer = consumers[projections[row["exit_id"]]["consumer_input_id"]]
            validate_json(output, PACKAGE / consumer["contract"]["path"], "consumer")
            self.assertIn("task_ref", output)
        self.assertEqual([], interface["public_contracts"]["private_artifacts"])

    def test_profile_inputs_do_not_accept_neighboring_route_fields(self):
        row = load("examples/public-delivery-plan-revision-input.json")
        schema = load("schemas/public-delivery-plan-revision-input.schema.json")
        row["revision_reason"] = "remaining_work"
        self.assertFalse(Draft202012Validator(schema).is_valid(row))
        candidate = load("examples/public-requirements-ready-output.json")
        candidate["candidate"]["design_locator"] = "design.md"
        self.assertFalse(Draft202012Validator(load("schemas/public-requirements-ready-output.schema.json")).is_valid(candidate))


if __name__ == "__main__":
    unittest.main()
