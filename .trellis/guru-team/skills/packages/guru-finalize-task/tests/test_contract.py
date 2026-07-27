#!/usr/bin/env python3
from __future__ import annotations

import json
import importlib.util
import subprocess
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[4]


class FinalizeTaskContractTests(unittest.TestCase):
    def test_private_route_schemas_accept_only_the_closed_executor_marker(self) -> None:
        runtime_path = (
            REPO
            / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py"
        )
        spec = importlib.util.spec_from_file_location(
            "guru_team_trellis_finalizer_contract_test",
            runtime_path,
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

    def test_seven_profiles_and_six_exits_are_closed(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        profiles = interface["public_contracts"]["input"]["profiles"]
        outputs = interface["public_contracts"]["outputs"]
        self.assertEqual(
            [item["id"] for item in profiles],
            [
                "publication_ready",
                "verification_verified",
                "verification_not_required",
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
            ["profile", "mode", "reprepare_intent", "reprepare_context"],
        )
        authoring = json.loads(
            (PACKAGE / consumer["contract"]["authoring_example"]["path"]).read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(set(authoring), set(consumer["contract"]["authoring_fields"]))

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

    def test_package_source_contract(self) -> None:
        result = subprocess.run(
            [
                "python3",
                str(REPO / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py"),
                "check-skill-packages",
                "--root",
                str(REPO),
                "--mode",
                "source",
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
