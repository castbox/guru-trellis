#!/usr/bin/env python3
from __future__ import annotations

import json
import importlib.util
import subprocess
import unittest
from pathlib import Path


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
