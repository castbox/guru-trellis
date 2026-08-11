from __future__ import annotations

import hashlib
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
        self.assertEqual(interface["schema_version"], "1.4")
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
        contracts = interface["public_contracts"]
        self.assertEqual(
            contracts["input"]["aggregate_schema"]["schema_id"],
            "guru-extension-verify-installation-input-aggregate-3.0",
        )
        self.assertEqual(
            contracts["private_artifacts"][0]["schema"]["schema_id"],
            "guru-extension-installation-verification-result-4.0",
        )
        result_schema = load("schemas/verification-result.schema.json")
        result_example = load("examples/verification-result.json")
        jsonschema.Draft202012Validator(result_schema).validate(result_example)

    def test_distinct_inputs_and_taskless_standalone_branch(self) -> None:
        workflow_schema = load("schemas/public-verification-required-input-3.0.schema.json")
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

    def test_current_outputs_use_only_reachable_mode_contracts(self) -> None:
        for exit_id in ("verified", "return-to-task-work", "blocked"):
            schema_path = (
                "schemas/public-verified-output-3.0.schema.json"
                if exit_id == "verified"
                else f"schemas/public-{exit_id}-output.schema.json"
            )
            schema = load(schema_path)
            branches = schema["oneOf"]
            self.assertEqual(len(branches), 2)
            self.assertEqual(
                {branch["properties"]["mode"]["const"] for branch in branches},
                {"workflow", "standalone"},
            )
            for branch in branches:
                self.assertFalse(branch["additionalProperties"])
                self.assertIn("exit_id", branch["required"])
        not_required = load("schemas/public-not-required-output.schema.json")
        self.assertEqual(
            not_required["$id"],
            "guru-extension-verify-installation-output-not-required-3.0",
        )
        self.assertEqual(not_required["properties"]["mode"]["const"], "standalone")
        self.assertFalse(not_required["additionalProperties"])

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
            branches = schema.get("oneOf", [schema])
            fields = {
                field
                for branch in branches
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
            schema_path = (
                "schemas/public-verified-output-3.0.schema.json"
                if schema_name == "verified"
                else f"schemas/public-{schema_name}-output.schema.json"
            )
            schema = load(schema_path)
            example = load(f"examples/public-{example_name}-output.json")
            jsonschema.Draft202012Validator(schema).validate(example)
        private_schema = load("schemas/marketplace-verification.schema.json")
        private_example = load("examples/marketplace-verification.json")
        jsonschema.Draft202012Validator(private_schema).validate(private_example)
        for wrapper in (PACKAGE / "scripts").glob("*.sh"):
            self.assertTrue(wrapper.stat().st_mode & stat.S_IXUSR, wrapper)

    def test_not_required_projects_the_reachable_standalone_seed(self) -> None:
        interface = load("interface.json")
        consumer = next(
            item
            for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "not_required_finalization_seed"
        )
        self.assertEqual(
            consumer["contract"]["profile_id"],
            "standalone_verification_not_required",
        )
        self.assertEqual(
            consumer["contract"]["seed_fields"],
            ["repo_ref", "resolved_head", "verification_ref"],
        )
        self.assertEqual(
            consumer["contract"]["authoring_fields"],
            ["profile", "mode", "task_ref"],
        )
        projection = next(
            item
            for item in interface["public_contracts"]["projections"]
            if item["id"] == "project_not_required"
        )
        self.assertEqual(
            [item["source"] for item in projection["mappings"]],
            ["repo_ref", "resolved_head", "verification_ref"],
        )
        output = load("examples/public-not-required-output.json")
        self.assertEqual(output["mode"], "standalone")

    def test_publication_head_public_io_uses_versioned_current_contracts(self) -> None:
        interface = load("interface.json")
        contracts = interface["public_contracts"]
        workflow_input = next(
            item
            for item in contracts["input"]["profiles"]
            if item["id"] == "verification_required"
        )
        verified_output = next(
            item
            for item in contracts["outputs"]
            if item["exit_id"] == "verified"
        )
        self.assertEqual(
            contracts["input"]["aggregate_schema"],
            {
                "schema_id": "guru-extension-verify-installation-input-aggregate-3.0",
                "path": "schemas/public-input-3.0.schema.json",
            },
        )
        self.assertEqual(
            workflow_input["schema"],
            {
                "schema_id": "guru-extension-verify-installation-input-verification-required-3.0",
                "path": "schemas/public-verification-required-input-3.0.schema.json",
            },
        )
        self.assertEqual(
            verified_output["schema"],
            {
                "schema_id": "guru-extension-verify-installation-output-verified-3.0",
                "path": "schemas/public-verified-output-3.0.schema.json",
            },
        )

    def test_verified_projection_executes_against_current_finalizer_input(self) -> None:
        interface = load("interface.json")
        contracts = interface["public_contracts"]
        projection = next(
            item
            for item in contracts["projections"]
            if item["id"] == "project_verified"
        )
        consumer = next(
            item
            for item in contracts["consumer_inputs"]
            if item["id"] == projection["consumer_input_id"]
        )
        output = load("examples/public-verified-output.json")
        target_package = PACKAGE.parent / consumer["consumer"]["id"]
        authoring_path = (
            target_package / consumer["contract"]["authoring_example"]["path"]
        )
        authoring = json.loads(authoring_path.read_text(encoding="utf-8"))
        projected = {
            mapping["target"]: output[mapping["source"]]
            for mapping in projection["mappings"]
        }
        target_input = {**projected, **authoring}
        target_interface = json.loads(
            (target_package / "interface.json").read_text(encoding="utf-8")
        )
        target_profile = next(
            item
            for item in target_interface["public_contracts"]["input"]["profiles"]
            if item["id"] == consumer["contract"]["profile_id"]
        )
        target_schema = json.loads(
            (target_package / target_profile["schema"]["path"]).read_text(
                encoding="utf-8"
            )
        )
        jsonschema.Draft202012Validator(target_schema).validate(target_input)
        self.assertEqual(target_input["publication_head"], output["publication_head"])

    def test_publication_head_legacy_schemas_are_byte_stable_and_not_current(self) -> None:
        fixtures = (
            (
                "schemas/public-verification-required-input.schema.json",
                "4e4ea74142c0a3cfcf9ae083c60ef01c314427b4c42c388a3eb537bb55abd675",
                "schemas/public-verification-required-input-3.0.schema.json",
                "examples/public-verification-required-input.json",
            ),
            (
                "schemas/public-verified-output.schema.json",
                "3304d6589a665e7728624e9099d2053968adfef15ba4c4467dcef59d47f918b5",
                "schemas/public-verified-output-3.0.schema.json",
                "examples/public-verified-output.json",
            ),
        )
        for legacy_path, legacy_sha256, current_path, example_path in fixtures:
            with self.subTest(legacy=legacy_path):
                legacy_bytes = (PACKAGE / legacy_path).read_bytes()
                self.assertEqual(
                    hashlib.sha256(legacy_bytes).hexdigest(),
                    legacy_sha256,
                )
                legacy_schema = json.loads(legacy_bytes)
                current_schema = load(current_path)
                current_payload = load(example_path)
                legacy_payload = dict(current_payload)
                legacy_payload.pop("publication_head")
                self.assertTrue(
                    jsonschema.Draft202012Validator(legacy_schema).is_valid(
                        legacy_payload
                    )
                )
                self.assertFalse(
                    jsonschema.Draft202012Validator(current_schema).is_valid(
                        legacy_payload
                    )
                )
                self.assertFalse(
                    jsonschema.Draft202012Validator(legacy_schema).is_valid(
                        current_payload
                    )
                )
                self.assertTrue(
                    jsonschema.Draft202012Validator(current_schema).is_valid(
                        current_payload
                    )
                )

        legacy_aggregate = PACKAGE / "schemas/public-input.schema.json"
        self.assertEqual(
            hashlib.sha256(legacy_aggregate.read_bytes()).hexdigest(),
            "b3606ee5b03eb59a919c1b00871fb942ad71352acb9e46496bcb2bec810fb869",
        )

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
        self.assertEqual(execution["schema_version"], "3.0")
        self.assertEqual(
            execution["target_repository"]["reviewed_content_sha256"],
            execution["target_repository"]["remote_reviewed_content_sha256"],
        )
        self.assertEqual(
            execution["extension_source"]["manifest_provenance"],
            "available",
        )
        self.assertNotEqual(
            execution["extension_source"]["direct_oid"],
            execution["extension_source"]["commit"],
        )
        self.assertTrue(execution["extension_source"]["ref_matches_commit"])
        self.assertTrue(all(
            item["checkout_owner"]
            in {"target_checkout", "extension_source_checkout"}
            for item in execution["commands"]
        ))
        self.assertTrue(all(
            item["checkout_owner"] == "extension_source_checkout"
            for item in execution["asset_expectations"]
        ))
        self.assertTrue(all(
            item["checkout_owner"] == "extension_source_checkout"
            for item in execution["asset_digests"]
        ))
        self.assertEqual(
            execution["ownership"]["checkout_owner"],
            "extension_source_checkout",
        )
        self.assertEqual(
            execution["sidecars"],
            {"checkout_owner": "extension_source_checkout", "paths": []},
        )

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
        invalid_capability = json.loads(json.dumps(execution))
        capability = invalid_capability["capabilities"][0]
        capability["evidence_step"] = 0
        del capability["command_refs"]
        del capability["asset_paths"]
        self.assertFalse(validator.is_valid(invalid_capability))

        for label, mutate in (
            (
                "asset expectation",
                lambda value: value["asset_expectations"][0].update(
                    checkout_owner="target_checkout"
                ),
            ),
            (
                "asset digest",
                lambda value: value["asset_digests"][0].update(
                    checkout_owner="target_checkout"
                ),
            ),
            (
                "ownership",
                lambda value: value["ownership"].update(
                    checkout_owner="target_checkout"
                ),
            ),
            (
                "sidecar",
                lambda value: value["sidecars"].update(
                    checkout_owner="target_checkout"
                ),
            ),
        ):
            with self.subTest(label=label):
                cross_owned = json.loads(json.dumps(execution))
                mutate(cross_owned)
                self.assertFalse(validator.is_valid(cross_owned))

    def test_no_secret_marker_in_contract_assets(self) -> None:
        marker = "synthetic-" + "secret-marker"
        for path in PACKAGE.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                self.assertNotIn(marker, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
