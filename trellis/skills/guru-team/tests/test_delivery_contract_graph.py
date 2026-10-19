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
PACKAGES = (
    "guru-create-delivery", "guru-activate-delivery", "guru-approve-task-plan",
    "guru-check-task", "guru-create-task-commit", "guru-review-branch",
    "guru-review-task-delivery", "guru-publish-task-delivery", "guru-merge-task-delivery",
    "guru-review-task-completion", "guru-complete-task-closure", "guru-finish-task",
    "guru-cleanup-task-resources", "guru-reactivate-task", "guru-reconcile-task-base",
)
class DeliveryGraphTests(unittest.TestCase):
    def test_all_versioned_outputs_compose_with_their_unique_consumer(self):
        checked = 0
        for name in PACKAGES:
            package = SKILLS / "packages" / name
            contract = json.loads((package / "interface.json").read_text())["public_contracts"]
            outputs = {x["exit_id"]: x for x in contract["outputs"]}
            consumers = {x["id"]: x for x in contract["consumer_inputs"]}
            for projection in contract["projections"]:
                with self.subTest(package=name, exit=projection["exit_id"]):
                    output = outputs[projection["exit_id"]]
                    value = json.loads((package / output["example"]["path"]).read_text())
                    validate_json(value, package / output["schema"]["path"], "producer")
                    projected = value if projection["operation"] == "direct" else {
                        x["target"]: value[x["source"]] for x in projection.get("mappings", [])}
                    consumer = consumers[projection["consumer_input_id"]]
                    if consumer["payload_kind"] == "zero_payload":
                        self.assertEqual(projected, {})
                        continue
                    target = consumer["contract"]
                    if target["kind"] == "json_schema":
                        schema_path = package / target["path"]
                        if not schema_path.is_file():
                            schema_path = SKILLS / target["path"]
                        validate_json(projected, schema_path, "workflow")
                    else:
                        self.assertEqual(target["kind"], "skill_input_authoring_seed")
                        self.assertEqual(set(projected), set(target["seed_fields"]))
                        self.assertFalse(set(target["seed_fields"]) & set(target["authoring_fields"]))
                        authored = json.loads((package / target["authoring_example"]["path"]).read_text())
                        self.assertEqual(set(authored), set(target["authoring_fields"]))
                        interface_path = SKILLS / target["interface_path"]
                        interface = json.loads(interface_path.read_text())
                        profile = next(x for x in interface["public_contracts"]["input"]["profiles"] if x["id"] == target["profile_id"])
                        validate_json({**projected, **authored}, interface_path.parent / profile["schema"]["path"], "consumer")
                    checked += 1
        self.assertGreater(checked, 70)
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
