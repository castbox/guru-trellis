import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


PACKAGE = Path(__file__).resolve().parents[1]
SHARED = PACKAGE.parents[1] / "contracts/task-lifecycle/task-lifecycle-dtos.schema.json"


def load(path):
    return json.loads((PACKAGE / path).read_text())


class ContractTest(unittest.TestCase):
    def test_profiles_examples_and_generation_zero(self):
        interface = load("interface.json")
        self.assertEqual(interface["judgment_mode"], "semantic")
        profiles = interface["public_contracts"]["input"]["profiles"]
        self.assertEqual(len(profiles), 5)
        for row in profiles:
            schema = load(row["schema"]["path"])
            example = load(row["example"]["path"])
            Draft202012Validator(schema).validate(example)
            self.assertEqual(example["lifecycle_generation"], 1 if row["id"] == "reactivate_rebind" else 0)
            self.assertEqual(example["profile"], row["id"])
            self.assertNotIn("task_ref", schema["properties"])
            self.assertNotIn("workspace", json.dumps(schema))

    def test_exit_consumer_closure_and_shared_dto(self):
        interface = load("interface.json")
        outputs = interface["public_contracts"]["outputs"]
        exits = {row["id"] for row in interface["external_exits"]}
        self.assertEqual({row["exit_id"] for row in outputs}, exits)
        self.assertEqual(len(exits), 7)
        consumers = {row["id"] for row in interface["public_contracts"]["consumer_inputs"]}
        self.assertEqual({key for row in outputs for key in row["consumer_use_ids"]}, consumers)
        shared = load("schemas/public-output.schema.json")
        explicit = load("schemas/public-explicit-output.schema.json")
        blocked = load("schemas/public-blocked-output.schema.json")
        for row in outputs:
            schema = load(row["schema"]["path"])
            example = load(row["example"]["path"])
            if example["exit_id"] != row["exit_id"] and row["exit_id"] not in {
                "session_resumed", "task_switched", "reactivate_rebound", "session_manually_recovered"
            }:
                self.fail("unexpected output example")
            Draft202012Validator(schema).validate({**example, "exit_id": row["exit_id"]})
        self.assertEqual(set(shared["properties"]) - {"exit_id", "resume_target"},
                         {"task_id", "lifecycle_generation"})
        self.assertEqual(set(shared["required"]), {"exit_id", "task_id", "lifecycle_generation", "resume_target"})
        self.assertEqual(set(explicit["required"]), {"exit_id", "task_id", "lifecycle_generation"})
        self.assertFalse(Draft202012Validator(shared).is_valid(load("examples/public-explicit-output.json")))
        self.assertFalse(Draft202012Validator(explicit).is_valid(load("examples/public-output.json")))
        self.assertEqual(set(blocked["required"]), {"exit_id", "reason_code", "reason_refs"})
        catalog = json.loads(SHARED.read_text())
        for name, example in (
            ("TaskLifecycleDTO", load("examples/public-output.json")),
            ("ReasonDTO", load("examples/public-blocked-output.json")),
        ):
            dto = {key: value for key, value in example.items() if key in catalog["$defs"][name]["properties"]}
            Draft202012Validator({"$ref": f"#/$defs/{name}", "$defs": catalog["$defs"]}).validate(dto)
        for row in interface["public_contracts"]["consumer_inputs"]:
            if row["id"] == "blocked":
                self.assertEqual(load(row["contract"]["path"])["properties"], blocked["properties"])
            elif row["id"] == "explicit_task_mode":
                self.assertEqual(load(row["contract"]["path"])["properties"], explicit["properties"])
            else:
                self.assertEqual(load(row["contract"]["path"])["properties"], shared["properties"])

    def test_no_legacy_mapping_or_locator_authority(self):
        content = (PACKAGE / "runtime/invoke.py").read_text()
        for name in ("_mapping_path", "_read_mapping", "write_recovery_mappings", "task_facts", "base_head", "workspace_path"):
            self.assertNotIn(name, content)
        self.assertIn("validate_candidate", content)
        self.assertIn("BranchBindingStore", content)
        self.assertIn("ResourceLedgerStore", content)
        interface = load("interface.json")
        self.assertNotIn("mapping", json.dumps(interface).lower())
        self.assertEqual(next(row for row in interface["external_exits"] if row["id"] == "explicit_task_mode")
                         ["consumer"]["id"], "guru-current-phase-router")
        self.assertEqual(load("examples/public-explicit-output.json")["lifecycle_generation"], 0)


if __name__ == "__main__":
    unittest.main()
