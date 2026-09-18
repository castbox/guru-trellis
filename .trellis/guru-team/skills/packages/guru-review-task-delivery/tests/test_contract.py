from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
GURU_ROOT = PACKAGE.parents[1]
sys.path.insert(0, str(GURU_ROOT))

from runtime.schema import validate_json  # noqa: E402


class DeliveryReviewContractTest(unittest.TestCase):
    def test_interface_and_declared_assets_are_closed(self):
        interface = json.loads((PACKAGE / "interface.json").read_text())
        validate_json(
            interface,
            GURU_ROOT / "schemas/skill-interface-1.4.schema.json",
            "interface",
        )
        self.assertEqual("semantic", interface["judgment_mode"])
        self.assertEqual(
            [
                "ready",
                "planning_revision_required",
                "implementation_required",
                "scope_confirmation_required",
                "blocked",
            ],
            [item["id"] for item in interface["external_exits"]],
        )
        for group in ("artifacts", "schemas"):
            for item in interface[group]:
                self.assertTrue((PACKAGE / item["path"]).is_file(), item)
        for item in interface["validators"]:
            self.assertTrue((PACKAGE / item["command"]).is_file(), item)
        for item in interface["tests"]:
            self.assertTrue((PACKAGE / item).is_file(), item)
        for consumer_input in interface["public_contracts"]["consumer_inputs"]:
            contract = consumer_input["contract"]
            if contract["kind"] == "json_schema":
                self.assertTrue((PACKAGE / contract["path"]).is_file(), consumer_input["id"])

    def test_frontmatter_identity_and_description_match_interface(self):
        interface = json.loads((PACKAGE / "interface.json").read_text())
        lines = (PACKAGE / "SKILL.md").read_text().splitlines()
        self.assertEqual("---", lines[0])
        self.assertEqual("---", lines[3])
        self.assertEqual(f"name: {interface['name']}", lines[1])
        self.assertEqual(f"description: {interface['description']}", lines[2])
        self.assertEqual(2, lines.count("---"))

    def test_examples_validate_against_per_profile_contracts(self):
        pairs = {
            "public-delivery-review-input.json": "public-delivery-review-input.schema.json",
            "semantic-ready.json": "semantic-result.schema.json",
            "delivery-review-gate.json": "delivery-review-gate.schema.json",
            "public-ready-output.json": "public-ready-output.schema.json",
            "public-planning-revision-required-output.json": "public-planning-revision-required-output.schema.json",
            "public-implementation-required-output.json": "public-implementation-required-output.schema.json",
            "public-scope-confirmation-required-output.json": "public-scope-confirmation-required-output.schema.json",
            "public-blocked-output.json": "public-blocked-output.schema.json",
            "public-invocation-error.json": "public-invocation-error.schema.json",
        }
        for example, schema in pairs.items():
            value = json.loads((PACKAGE / "examples" / example).read_text())
            validate_json(value, PACKAGE / "schemas" / schema, example)

    def test_public_outputs_contain_no_terminal_task_lifecycle_fields(self):
        forbidden = {"completed", "completion", "closure", "archive", "finish", "cleanup", "issue_state"}
        interface = json.loads((PACKAGE / "interface.json").read_text())
        for output in interface["public_contracts"]["outputs"]:
            value = json.loads((PACKAGE / output["example"]["path"]).read_text())
            self.assertFalse(forbidden.intersection(value), output["exit_id"])

    def test_ready_projection_matches_publish_review_ready_seed(self):
        ready = json.loads((PACKAGE / "examples/public-ready-output.json").read_text())
        publish_schema = PACKAGE.parent / "guru-publish-task-delivery/schemas/public-review-ready-input.schema.json"
        if not publish_schema.is_file():
            self.skipTest("Publish package is being assembled in a disjoint ownership slice.")
        projected = {"profile": "review_ready", "mode": "workflow"}
        projected.update({key: value for key, value in ready.items() if key != "exit_id"})
        validate_json(projected, publish_schema, "publish_input")

    def test_every_declared_consumer_contract_exists_and_validates_projection(self):
        interface = json.loads((PACKAGE / "interface.json").read_text())
        outputs = {
            item["exit_id"]: json.loads((PACKAGE / item["example"]["path"]).read_text())
            for item in interface["public_contracts"]["outputs"]
        }
        consumers = {
            item["id"]: item for item in interface["public_contracts"]["consumer_inputs"]
        }
        for projection in interface["public_contracts"]["projections"]:
            consumer_input = consumers[projection["consumer_input_id"]]
            contract = consumer_input["contract"]
            if contract["kind"] != "json_schema":
                continue
            source = outputs[projection["exit_id"]]
            projected = self.project(source, projection)
            schema_path = PACKAGE / contract["path"]
            example_path = schema_path.with_name(
                schema_path.name.removesuffix(".schema.json") + ".example.json"
            )
            self.assertTrue(schema_path.is_file(), contract["path"])
            self.assertTrue(example_path.is_file(), example_path)
            consumer_example = json.loads(example_path.read_text())
            self.assertEqual(source, projected)
            self.assertEqual(projected, consumer_example)
            validate_json(projected, schema_path, projection["id"])
            validate_json(consumer_example, schema_path, str(example_path))

    def test_publish_review_stale_projects_normal_fresh_review_input(self):
        publish_package = PACKAGE.parent / "guru-publish-task-delivery"
        publish_interface_path = publish_package / "interface.json"
        if not publish_interface_path.is_file():
            self.skipTest("Publish package is being assembled in a disjoint ownership slice.")
        interface = json.loads(publish_interface_path.read_text())
        consumer_input = next(
            item
            for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "review_stale_input"
        )
        projection = next(
            item
            for item in interface["public_contracts"]["projections"]
            if item["consumer_input_id"] == consumer_input["id"]
        )
        output_contract = next(
            item
            for item in interface["public_contracts"]["outputs"]
            if item["exit_id"] == projection["exit_id"]
        )
        output = json.loads((publish_package / output_contract["example"]["path"]).read_text())
        authored = json.loads(
            (publish_package / consumer_input["contract"]["authoring_example"]["path"]).read_text()
        )
        if consumer_input["contract"]["profile_id"] != "delivery_review":
            self.skipTest(
                "Publish package still exposes the pre-migration publication_review_stale contract."
            )
        projected = self.project(output, projection)
        review_input = {**projected, **authored}
        self.assertEqual("delivery_review", consumer_input["contract"]["profile_id"])
        self.assertEqual(
            {"profile", "mode", "task_ref", "branch_review_commit"}, set(review_input)
        )
        self.assertNotIn("stale_reason", review_input)
        validate_json(
            review_input,
            PACKAGE / "schemas/public-delivery-review-input.schema.json",
            "publish_review_stale_projection",
        )

    @staticmethod
    def project(source: dict, projection: dict) -> dict:
        if projection["operation"] == "direct":
            return dict(source)
        if projection["operation"] == "select":
            return {
                mapping["target"]: source[mapping["source"]]
                for mapping in projection["mappings"]
            }
        raise AssertionError(f"unsupported projection operation: {projection['operation']}")


if __name__ == "__main__":
    unittest.main()
