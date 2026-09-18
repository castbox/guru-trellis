from __future__ import annotations

import json
import stat
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


PACKAGE = Path(__file__).resolve().parents[1]
GURU = PACKAGE.parents[1]


class ContractTest(unittest.TestCase):
    def test_interface_and_frontmatter_are_current(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text())
        schema = json.loads((GURU / "schemas/skill-interface-1.4.schema.json").read_text())
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(interface)), [])
        skill = (PACKAGE / "SKILL.md").read_text()
        self.assertTrue(skill.startswith("---\nname: guru-merge-task-delivery\n"))
        self.assertIn(f"description: {interface['description']}\n---\n", skill)
        self.assertEqual(interface["judgment_mode"], "semantic")
        self.assertEqual(interface["ordered_stages"], [
            "forward_behavior", "ai_review_gate", "conditional_human_confirmation",
            "recorder_validator", "typed_exit",
        ])

    def test_declared_assets_exist_and_scripts_are_executable(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text())
        paths = [item["path"] for key in ("artifacts", "schemas") for item in interface[key]]
        paths += [item["command"] for item in interface["validators"]]
        paths += interface["tests"]
        for relative in paths:
            path = PACKAGE / relative
            self.assertTrue(path.is_file(), relative)
            self.assertFalse(path.is_symlink(), relative)
        for script in (PACKAGE / "scripts").glob("*.sh"):
            self.assertTrue(script.stat().st_mode & stat.S_IXUSR, script.name)

    def test_examples_match_closed_public_schemas(self) -> None:
        pairs = {
            "delivery-history-query.schema.json": "delivery-history-query.json",
            "delivery-history-result.schema.json": "delivery-history-result.json",
            "public-ready-for-merge-input.schema.json": "public-ready-for-merge-input.json",
            "semantic-review.schema.json": "semantic-review.json",
            "public-delivered-output.schema.json": "public-delivered-output.json",
            "public-merge-blocked-output.schema.json": "public-merge-blocked-output.json",
            "public-implementation-required-output.schema.json": "public-implementation-required-output.json",
            "public-review-refresh-required-output.schema.json": "public-review-refresh-required-output.json",
            "public-invocation-error.schema.json": "public-invocation-error.json",
        }
        for schema_name, example_name in pairs.items():
            schema = json.loads((PACKAGE / "schemas" / schema_name).read_text())
            example = json.loads((PACKAGE / "examples" / example_name).read_text())
            self.assertEqual(list(Draft202012Validator(schema).iter_errors(example)), [], example_name)

    def test_private_gate_example_matches_runtime_identity(self) -> None:
        import importlib.util
        import sys
        sys.path.insert(0, str(PACKAGE.parents[1]))
        spec = importlib.util.spec_from_file_location("merge_delivery_contract_owner", PACKAGE / "runtime/owner.py")
        assert spec and spec.loader
        owner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(owner)
        gate = json.loads((PACKAGE / "examples/private-merge-gate.json").read_text())
        owner.validate_gate(PACKAGE, gate)

    def test_outputs_keep_delivery_completion_boundary(self) -> None:
        delivered = json.loads((PACKAGE / "examples/public-delivered-output.json").read_text())
        self.assertEqual(set(delivered), {
            "exit_id", "task_ref", "delivery_cycle_ref", "repo_ref", "pr_number",
            "reviewed_head", "merge_commit_sha",
        })
        forbidden = {"completed", "closed", "closure", "archive", "finish", "cleanup"}
        for path in (PACKAGE / "schemas").glob("public-*-output.schema.json"):
            properties = json.loads(path.read_text()).get("properties", {})
            self.assertTrue(forbidden.isdisjoint(properties), path.name)

    def test_json_schema_consumers_exist_and_accept_declared_projections(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text())
        outputs = {
            item["exit_id"]: json.loads((PACKAGE / item["example"]["path"]).read_text())
            for item in interface["public_contracts"]["outputs"]
        }
        consumers = {
            item["id"]: item
            for item in interface["public_contracts"]["consumer_inputs"]
            if item["contract"]["kind"] == "json_schema"
        }
        projections = {
            item["consumer_input_id"]: item
            for item in interface["public_contracts"]["projections"]
        }
        self.assertEqual(set(consumers), {"merge_blocked_stop_input", "implementation_router_input"})
        for consumer_id, consumer in consumers.items():
            with self.subTest(consumer=consumer_id):
                schema_path = PACKAGE / consumer["contract"]["path"]
                self.assertTrue(schema_path.is_file(), consumer["contract"]["path"])
                self.assertFalse(schema_path.is_symlink(), consumer["contract"]["path"])
                projection = projections[consumer_id]
                source = outputs[projection["exit_id"]]
                if projection["operation"] == "direct":
                    projected = source
                else:
                    projected = {
                        mapping["target"]: source[mapping["source"]]
                        for mapping in projection["mappings"]
                    }
                schema = json.loads(schema_path.read_text())
                self.assertEqual(
                    list(Draft202012Validator(schema).iter_errors(projected)),
                    [],
                    consumer_id,
                )

    def test_review_refresh_authors_current_delivery_review_input(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text())
        consumer = next(
            item for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "delivery_review_seed"
        )
        contract = consumer["contract"]
        self.assertEqual(contract["profile_id"], "delivery_review")
        self.assertEqual(contract["seed_fields"], ["task_ref"])
        self.assertEqual(
            contract["authoring_fields"],
            ["profile", "mode", "branch_review_commit"],
        )
        projection = next(
            item for item in interface["public_contracts"]["projections"]
            if item["id"] == "project_review_refresh_required"
        )
        self.assertEqual(projection["operation"], "select")
        self.assertEqual(
            projection["mappings"],
            [{"source": "task_ref", "target": "task_ref"}],
        )

    def test_command_surface_has_one_public_mutation_entry(self) -> None:
        commands = json.loads((PACKAGE / "commands.json").read_text())["commands"]
        self.assertEqual({item["id"] for item in commands}, {
            "preview-task-delivery-merge", "record-task-delivery-merge",
            "check-task-delivery-merge", "execute-task-delivery-merge",
            "invoke-guru-merge-task-delivery", "discover-task-deliveries",
        })
        discovery = next(
            item for item in commands if item["id"] == "discover-task-deliveries"
        )
        self.assertEqual(discovery["side_effect"], "github_read")
        public = next(item for item in commands if item["id"] == "invoke-guru-merge-task-delivery")
        self.assertEqual(public["side_effect"], "github_write")
        source = (PACKAGE / "runtime/owner.py").read_text()
        self.assertEqual(source.count('"gh", "pr", "merge"'), 1)
        self.assertNotIn("issue close", source)
        self.assertNotIn("task.py finish", source)
        self.assertNotIn("--squash", source)
        self.assertNotIn("--rebase", source)


if __name__ == "__main__":
    unittest.main()
