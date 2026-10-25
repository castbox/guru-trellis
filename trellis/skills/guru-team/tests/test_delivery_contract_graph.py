"""Versioned Delivery handoffs compose with real declared consumer inputs."""
from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
import sys
SKILLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILLS))
from runtime.schema import validate_json
from runtime.io import CommandError
from runtime.eval_runner import validate_instance
REGISTRY = json.loads((SKILLS / "registry.json").read_text())
PACKAGES = tuple(row["id"] for row in REGISTRY["skills"] if row["state"] == "active")


def project_output(value, projection):
    """Apply only the public Interface's declared transport operation."""
    if projection["operation"] == "direct":
        return value.copy()
    projected = {}
    for mapping in projection.get("mappings", []):
        if mapping["source"] not in value:
            continue
        item = value[mapping["source"]]
        normalizer = mapping.get("normalizer")
        if normalizer == "lowercase_ascii_enum":
            item = item.lower()
        elif normalizer == "trim_ascii_outer_whitespace":
            item = item.strip(" \t\r\n\v\f")
        elif normalizer is not None:
            raise AssertionError(f"Undeclared test support for normalizer {normalizer}")
        projected[mapping["target"]] = item
    return projected


class DeliveryGraphTests(unittest.TestCase):
    def test_every_current_profile_example_matches_independent_and_aggregate_schema(self):
        for name in PACKAGES:
            package = SKILLS / "packages" / name
            contract = json.loads((package / "interface.json").read_text())["public_contracts"]["input"]
            if contract["kind"] != "structured_json":
                continue
            for profile in contract["profiles"]:
                with self.subTest(package=name, profile=profile["id"]):
                    value = json.loads((package / profile["example"]["path"]).read_text())
                    validate_json(value, package / profile["schema"]["path"], "profile")
                    validate_json(value, package / contract["aggregate_schema"]["path"], "aggregate")

    def assert_projection(self, package, projection, value, consumers):
        projected = project_output(value, projection)
        consumer = consumers[projection["consumer_input_id"]]
        if consumer["payload_kind"] == "zero_payload":
            self.assertEqual(projected, {})
            return
        target = consumer["contract"]
        if target["kind"] == "json_schema":
            schema_path = package / target["path"]
            if not schema_path.is_file():
                schema_path = SKILLS / target["path"]
            validate_json(projected, schema_path, "workflow")
        elif target["kind"] == "skill_input":
            interface_path = SKILLS / target["interface_path"]
            if not interface_path.is_file():
                interface_path = SKILLS.parents[2] / target["interface_path"]
            interface = json.loads(interface_path.read_text())
            inputs = interface["public_contracts"]["input"]
            if inputs["kind"] == "scalar_cli":
                arguments = {row["id"]: row for row in inputs["arguments"]}
                self.assertLessEqual(set(projected), set(arguments))
                self.assertLessEqual({name for name, row in arguments.items() if row["required"]}, set(projected))
                for name, item in projected.items():
                    self.assertIsInstance(item, str)
                    if arguments[name]["type"] == "ascii_enum":
                        self.assertRegex(item, r"^[a-z][a-z0-9_-]*$")
            else:
                profile = next(x for x in inputs["profiles"] if x["id"] == target.get("profile_id", value.get(target.get("profile_selector", {}).get("field"))))
                validate_json(projected, interface_path.parent / profile["schema"]["path"], "consumer")
                validate_json(projected, interface_path.parent / inputs["aggregate_schema"]["path"], "aggregate_consumer")
        else:
            self.assertEqual(target["kind"], "skill_input_authoring_seed")
            self.assertEqual(set(projected), set(target["seed_fields"]))
            self.assertFalse(set(target["seed_fields"]) & set(target["authoring_fields"]))
            interface_path = SKILLS / target["interface_path"]
            if not interface_path.is_file():
                interface_path = SKILLS.parents[2] / target["interface_path"]
            interface = json.loads(interface_path.read_text())
            profile = next(x for x in interface["public_contracts"]["input"]["profiles"] if x["id"] == target.get("profile_id", value.get(target.get("profile_selector", {}).get("field"))))
            for authoring in [target, *target.get("alternate_authoring", [])]:
                relative = authoring["authoring_example"]["path"]
                path = package / relative
                if not path.is_file():
                    path = interface_path.parent / relative
                example = json.loads(path.read_text())
                authored = {field: example[field] for field in authoring["authoring_fields"]}
                self.assertFalse(set(projected) & set(authored))
                merged = {**projected, **authored}
                validate_json(merged, interface_path.parent / profile["schema"]["path"], "consumer")
                validate_json(merged, interface_path.parent / interface["public_contracts"]["input"]["aggregate_schema"]["path"], "aggregate_consumer")

    def test_all_versioned_outputs_compose_with_their_unique_consumer(self):
        for name in PACKAGES:
            package = SKILLS / "packages" / name
            contract = json.loads((package / "interface.json").read_text())["public_contracts"]
            outputs = {row["exit_id"]: row for row in contract["outputs"]}
            consumers = {row["id"]: row for row in contract["consumer_inputs"]}
            for projection in contract["projections"]:
                output = outputs[projection["exit_id"]]
                primary = package / output["example"]["path"]
                variants = {primary: json.loads(primary.read_text())}
                # Include every published example that is legal under this
                # selected output schema. Historical incompatible examples do
                # not become current runtime inputs.
                for path in (package / "examples").rglob("*.json"):
                    value = json.loads(path.read_text())
                    if not isinstance(value, dict) or value.get("exit_id") != projection["exit_id"]:
                        continue
                    try:
                        validate_json(value, package / output["schema"]["path"], "variant")
                    except CommandError as error:
                        if error.code != "schema_mismatch":
                            raise
                    else:
                        variants[path] = value
                for path, value in variants.items():
                    with self.subTest(package=name, exit=projection["exit_id"], example=path.name):
                        validate_json(value, package / output["schema"]["path"], "producer")
                        self.assert_projection(package, projection, value, consumers)

    def test_readiness_refresh_preserves_the_source_reason(self):
        for name, exit_id, reason in [("guru-publish-task-delivery", "review_stale", "stale_reason"),
                                      ("guru-merge-task-delivery", "review_refresh_required", "reason_code")]:
            contract = json.loads((SKILLS / "packages" / name / "interface.json").read_text())["public_contracts"]
            projection = next(x for x in contract["projections"] if x["exit_id"] == exit_id)
            target = next(x["contract"] for x in contract["consumer_inputs"] if x["id"] == projection["consumer_input_id"])
            self.assertEqual(target["profile_id"], "delivery_readiness_refresh")
            self.assertIn({"source": reason, "target": "reentry_reason"}, projection["mappings"])
    def test_relative_schema_refs_resolve_and_validate_both_versions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("legacy", "delivery"):
                (root / (name + ".json")).write_text(json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "public-" + name,
                    "type": "object", "required": ["profile"], "additionalProperties": False, "properties": {"profile": {"const": name}}}))
            index = root / "index.json"
            index.write_text(json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "public-versioned-index",
                "oneOf": [{"$ref": "legacy.json"}, {"$ref": "delivery.json"}]}))
            for name in ("legacy", "delivery"):
                validate_json({"profile": name}, index, "input")
                validate_instance({"profile": name}, index, "eval_input")
            with self.assertRaises(CommandError):
                validate_json({"profile": "unknown"}, index, "input")
            self.assertEqual(json.loads(index.read_text())["$id"], "public-versioned-index")
if __name__ == "__main__":
    unittest.main()
