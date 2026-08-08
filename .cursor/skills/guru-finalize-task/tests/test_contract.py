#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

import jsonschema


PACKAGE = Path(__file__).resolve().parents[1]


def resolve_runtime_layout() -> tuple[Path, Path, str]:
    for ancestor in [PACKAGE, *PACKAGE.parents]:
        candidates = (
            (
                ancestor
                / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py",
                "source",
            ),
            (
                ancestor
                / ".trellis/guru-team/scripts/python/guru_team_trellis.py",
                "installed",
            ),
        )
        for runtime_path, mode in candidates:
            if runtime_path.is_file():
                return ancestor, runtime_path, mode
    raise RuntimeError("Compatible Guru Team runtime not found for package tests.")


REPO, RUNTIME_PATH, PACKAGE_MODE = resolve_runtime_layout()


class FinalizeTaskContractTests(unittest.TestCase):
    def test_publication_head_public_io_uses_versioned_current_contracts(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        contracts = interface["public_contracts"]
        verified_input = next(
            item
            for item in contracts["input"]["profiles"]
            if item["id"] == "verification_verified"
        )
        verification_output = next(
            item
            for item in contracts["outputs"]
            if item["exit_id"] == "verification_required"
        )
        self.assertEqual(
            contracts["input"]["aggregate_schema"],
            {
                "schema_id": "guru-finalize-task-input-aggregate-4.0",
                "path": "schemas/public-input-4.0.schema.json",
            },
        )
        self.assertEqual(
            verified_input["schema"],
            {
                "schema_id": "guru-finalize-task-input-verification-verified-4.0",
                "path": "schemas/public-verification-verified-input-4.0.schema.json",
            },
        )
        self.assertEqual(
            verification_output["schema"],
            {
                "schema_id": "guru-finalize-task-output-verification-required-3.0",
                "path": "schemas/public-verification-required-output-3.0.schema.json",
            },
        )

    def test_verification_required_projection_executes_against_current_consumer(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        contracts = interface["public_contracts"]
        projection = next(
            item
            for item in contracts["projections"]
            if item["id"] == "project_verification_required"
        )
        consumer = next(
            item
            for item in contracts["consumer_inputs"]
            if item["id"] == projection["consumer_input_id"]
        )
        output = json.loads(
            (PACKAGE / "examples/public-verification-required-output.json").read_text(
                encoding="utf-8"
            )
        )
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
                "schemas/public-verification-required-output.schema.json",
                "2e3bc09dfab29fa538c762b767d11d1311a9d310817a8e37698933ad44fd731c",
                "schemas/public-verification-required-output-3.0.schema.json",
                "examples/public-verification-required-output.json",
            ),
            (
                "schemas/public-verification-verified-input.schema.json",
                "8d487babe2435d35c3fda5a1acbcb29a43191de5f3ac62d7e92db42030aa3fcb",
                "schemas/public-verification-verified-input-4.0.schema.json",
                "examples/public-verification-verified-input.json",
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
                current_schema = json.loads(
                    (PACKAGE / current_path).read_text(encoding="utf-8")
                )
                current_payload = json.loads(
                    (PACKAGE / example_path).read_text(encoding="utf-8")
                )
                legacy_payload = dict(current_payload)
                legacy_payload.pop("publication_head")
                self.assertEqual(
                    list(
                        jsonschema.Draft202012Validator(legacy_schema).iter_errors(
                            legacy_payload
                        )
                    ),
                    [],
                )
                self.assertTrue(
                    list(
                        jsonschema.Draft202012Validator(current_schema).iter_errors(
                            legacy_payload
                        )
                    )
                )
                self.assertTrue(
                    list(
                        jsonschema.Draft202012Validator(legacy_schema).iter_errors(
                            current_payload
                        )
                    )
                )
                self.assertEqual(
                    list(
                        jsonschema.Draft202012Validator(current_schema).iter_errors(
                            current_payload
                        )
                    ),
                    [],
                )

        legacy_aggregate = PACKAGE / "schemas/public-input.schema.json"
        self.assertEqual(
            hashlib.sha256(legacy_aggregate.read_bytes()).hexdigest(),
            "f7eaf2e0abb6e2f91699212d6bca270a7f59fb3fe0f6c11182349902bd86789a",
        )

    def test_private_route_schemas_accept_only_the_closed_executor_marker(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "guru_team_trellis_finalizer_contract_test",
            RUNTIME_PATH,
        )
        self.assertIsNotNone(spec)
        assert spec is not None and spec.loader is not None
        runtime = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runtime)

        fixtures = [
            (
                "schemas/semantic-review-input.schema.json",
                "examples/semantic-review-input.json",
            ),
            (
                "schemas/task-finalization-gate.schema.json",
                "examples/task-finalization-gate.json",
            ),
        ]
        for schema_relative, example_relative in fixtures:
            with self.subTest(schema=schema_relative):
                schema = json.loads(
                    (PACKAGE / schema_relative).read_text(encoding="utf-8")
                )
                payload = json.loads(
                    (PACKAGE / example_relative).read_text(encoding="utf-8")
                )
                payload["route"] = {
                    "typed_exit": "published",
                    "consumer": {
                        "kind": "workflow",
                        "id": "guru-finalization-finish-response",
                    },
                    "output": {"materialization": "executor"},
                }
                self.assertEqual(
                    runtime.skill_json_schema_validation_errors(
                        payload,
                        schema,
                        "private finalization route",
                    ),
                    [],
                )
                payload["route"]["output"] = {}
                self.assertTrue(
                    runtime.skill_json_schema_validation_errors(
                        payload,
                        schema,
                        "private finalization route",
                    )
                )

    def test_six_current_profiles_and_six_exits_are_closed(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        profiles = interface["public_contracts"]["input"]["profiles"]
        outputs = interface["public_contracts"]["outputs"]
        self.assertEqual(
            [item["id"] for item in profiles],
            [
                "publication_ready",
                "verification_verified",
                "standalone_verification_not_required",
                "same_plan_resume",
                "reprepare_preview",
                "standalone_finalization",
            ],
        )
        self.assertEqual(
            [item["exit_id"] for item in outputs],
            [
                "verification_required",
                "publication_review_stale",
                "resume_finalization",
                "reprepare_required",
                "published",
                "blocked",
            ],
        )

    def test_archive_contract_matches_current_runtime_limit(self) -> None:
        contract = (PACKAGE / "references/contract.md").read_text(encoding="utf-8")
        self.assertIn("schema 2.0", contract)
        self.assertIn("seven-file", contract)
        self.assertIn("at most eight files", contract)

        spec = importlib.util.spec_from_file_location(
            "guru_team_trellis_archive_contract_test",
            RUNTIME_PATH,
        )
        self.assertIsNotNone(spec)
        assert spec is not None and spec.loader is not None
        runtime = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runtime)
        self.assertEqual(len(runtime.CLOSEOUT_ARCHIVE_CORE_ARTIFACTS), 7)
        self.assertEqual(runtime.CLOSEOUT_ARCHIVE_MAX_ARTIFACTS, 8)
        self.assertEqual(
            runtime.CLOSEOUT_ARCHIVE_CORE_ARTIFACTS,
            {
                "task.json",
                "prd.md",
                "design.md",
                "implement.md",
                "issue-scope-ledger.json",
                "closeout-plan.json",
                "finish-summary.json",
            },
        )

    def test_reprepare_seed_is_exact_and_target_owned(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        consumer = next(
            item
            for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "reprepare_preview_input"
        )
        self.assertEqual(consumer["contract"]["seed_fields"], ["task_ref", "reason_code"])
        self.assertEqual(
            consumer["contract"]["authoring_fields"],
            ["profile", "mode"],
        )
        authoring = json.loads(
            (PACKAGE / consumer["contract"]["authoring_example"]["path"]).read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(set(authoring), set(consumer["contract"]["authoring_fields"]))

    def test_publication_stale_seed_has_no_reentry_narrative(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        consumer = next(
            item
            for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "publication_review_stale_input"
        )
        self.assertEqual(
            consumer["contract"]["seed_fields"],
            ["task_ref", "branch_review_commit", "stale_reason"],
        )
        self.assertEqual(
            consumer["contract"]["authoring_fields"],
            ["profile", "mode", "review_intent"],
        )
        authoring = json.loads(
            (PACKAGE / consumer["contract"]["authoring_example"]["path"]).read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(set(authoring), set(consumer["contract"]["authoring_fields"]))
        self.assertNotIn("reentry_context", authoring)

        output = json.loads(
            (PACKAGE / "examples/public-publication-review-stale-output.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            set(output),
            {"exit_id", "task_ref", "branch_review_commit", "stale_reason"},
        )
        stale_contract = next(
            item
            for item in interface["public_contracts"]["outputs"]
            if item["exit_id"] == "publication_review_stale"
        )
        self.assertEqual(
            stale_contract["schema"]["schema_id"],
            "guru-finalize-task-output-publication-review-stale-3.0",
        )

    def test_stale_route_is_current_only_and_side_effect_free(self) -> None:
        skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        contract = (PACKAGE / "references/contract.md").read_text(encoding="utf-8")
        interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        invocation = next(
            item
            for item in interface["validators"]
            if item["id"] == "public_invocation"
        )
        self.assertIn("without mutating", skill)
        self.assertIn("branch_review_commit", contract)
        self.assertIn("reviewed-content identity", contract)
        self.assertIn("current public input", invocation["objective_scope"])
        self.assertEqual(
            [
                item["exit_id"]
                for item in interface["public_contracts"]["outputs"]
            ],
            [
                "verification_required",
                "publication_review_stale",
                "resume_finalization",
                "reprepare_required",
                "published",
                "blocked",
            ],
        )

    def test_standalone_not_required_profile_is_closed_and_target_authored(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        profile = next(
            item
            for item in interface["public_contracts"]["input"]["profiles"]
            if item["id"] == "standalone_verification_not_required"
        )
        schema = json.loads(
            (PACKAGE / profile["schema"]["path"]).read_text(encoding="utf-8")
        )
        example = json.loads(
            (PACKAGE / profile["example"]["path"]).read_text(encoding="utf-8")
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            set(schema["required"]),
            {
                "profile",
                "mode",
                "task_ref",
                "repo_ref",
                "resolved_head",
                "verification_ref",
            },
        )
        self.assertEqual(set(example), set(schema["required"]))

    def test_package_registry_contract(self) -> None:
        result = subprocess.run(
            [
                "python3",
                str(RUNTIME_PATH),
                "check-skill-packages",
                "--root",
                str(REPO),
                "--mode",
                PACKAGE_MODE,
                "--json",
            ],
            cwd=REPO,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
