from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import jsonschema


PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[4]
RUNTIME_PATH = PACKAGE / "runtime/owner.py"


def load(relative: str):
    return json.loads((PACKAGE / relative).read_text(encoding="utf-8"))


def load_runtime():
    spec = importlib.util.spec_from_file_location("guru_verify_extension_installation_runtime", RUNTIME_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExtensionVerificationContractTests(unittest.TestCase):
    def test_active_runtime_is_source_only_and_monolith_independent(self) -> None:
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((PACKAGE / "runtime").glob("*.py"))
        )
        for retired in (
            "guru_team_trellis.py",
            "verification_required",
            "not_required",
            "finalization_verification",
            "task_ref",
            "task-bearing",
            "guru-finalize-task",
        ):
            self.assertNotIn(retired, runtime_text)
        commands = load("commands.json")
        self.assertEqual(
            {item["id"] for item in commands["commands"]},
            {item["runtime_command"] for item in load("interface.json")["validators"]},
        )

    def test_interface_is_source_owned_standalone_only(self) -> None:
        interface = load("interface.json")
        self.assertEqual(interface["schema_version"], "1.5")
        self.assertEqual(interface["modes"]["workflow"], {"routing": "not_applicable", "entry_precondition_ids": []})
        self.assertEqual(interface["modes"]["standalone"]["routing"], "direct_discovery")
        self.assertEqual([item["id"] for item in interface["external_exits"]], ["verified", "blocked"])
        self.assertEqual(
            [item["id"] for item in interface["public_contracts"]["input"]["profiles"]],
            ["source_repository_verification"],
        )
        current = json.dumps(interface["public_contracts"], sort_keys=True)
        for retired in ("verification_required", "not_required", "return_to_task_work", "task_ref", "guru-finalize-task"):
            self.assertNotIn(retired, current)
        self.assertEqual(interface["public_contracts"]["private_artifacts"][0]["persistence"], "ignored_runtime")

    def test_current_input_and_outputs_are_closed(self) -> None:
        input_schema = load("schemas/public-source-repository-verification-input.schema.json")
        input_example = load("examples/public-source-repository-verification-input.json")
        jsonschema.Draft202012Validator(input_schema).validate(input_example)
        self.assertFalse(jsonschema.Draft202012Validator(input_schema).is_valid({**input_example, "task_ref": ".trellis/tasks/current"}))
        for exit_id, schema_name in (("verified", "public-verified-output-4.0"), ("blocked", "public-blocked-output-2.0")):
            schema = load(f"schemas/{schema_name}.schema.json")
            example = load(f"examples/public-{exit_id}-output.json")
            jsonschema.Draft202012Validator(schema).validate(example)
        current_result = load("schemas/verification-result-5.0.schema.json")
        legacy_result = load("schemas/verification-result-4.0.schema.json")
        self.assertEqual(current_result["$id"], "guru-extension-installation-verification-result-5.0")
        self.assertEqual(legacy_result["$id"], "guru-extension-installation-verification-result-4.0")
        jsonschema.Draft202012Validator(current_result).validate(
            load("examples/verification-result.json")
        )
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE / "schemas/verification-result-4.0.schema.json").read_bytes()
            ).hexdigest(),
            "8f47671d8b5abb60eb10e334ceb21a9c46d6fb1bd5854e0190fc99c1df7c874d",
        )

    def test_current_semantic_input_requires_explicit_applicability(self) -> None:
        schema = load("schemas/semantic-review-input-2.0.schema.json")
        self.assertEqual(
            schema["properties"]["applicability"]["allOf"][1]["properties"]["status"],
            {"const": "required"},
        )
        self.assertEqual(
            schema["properties"]["semantic_review"]["allOf"][1]["properties"]["conclusion"],
            {"enum": ["verified", "blocked"]},
        )

    def test_non_source_rejected_before_executor(self) -> None:
        runtime = load_runtime()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/example/business.git"], cwd=root, check=True)
            for relative in (
                "trellis/guru-team-extension.json",
                "trellis/index.json",
                "trellis/workflows/guru-team/workflow.md",
                "trellis/presets/guru-team/scripts/bash/apply.sh",
            ):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}\n", encoding="utf-8")
            previous = os.environ.get("GURU_TEAM_INVOKED_PACKAGE_ROOT")
            os.environ["GURU_TEAM_INVOKED_PACKAGE_ROOT"] = str(PACKAGE)
            try:
                with mock.patch.object(runtime, "extension_verification_execute_facts") as execute:
                    with self.assertRaisesRegex(runtime.WorkflowError, "source_origin_mismatch"):
                        runtime.cmd_execute_extension_verification(argparse.Namespace(
                            root=str(root),
                            input="examples/public-source-repository-verification-input.json",
                            capability=["marketplace_index"],
                        ))
                    execute.assert_not_called()
            finally:
                if previous is None:
                    os.environ.pop("GURU_TEAM_INVOKED_PACKAGE_ROOT", None)
                else:
                    os.environ["GURU_TEAM_INVOKED_PACKAGE_ROOT"] = previous


if __name__ == "__main__":
    unittest.main()
