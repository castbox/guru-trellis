from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
if str(SKILLS) not in sys.path:
    sys.path.insert(0, str(SKILLS))
from runtime.command import main


class PackageLocalRuntimeTest(unittest.TestCase):
    def test_command_and_error_contract_close(self) -> None:
        commands = json.loads((PACKAGE / "commands.json").read_text())
        catalog = json.loads((PACKAGE / "errors/catalog.json").read_text())
        command_schema = json.loads((SKILLS / "schemas/skill-commands.schema.json").read_text())
        error_schema = json.loads((SKILLS / "schemas/skill-error-catalog.schema.json").read_text())
        self.assertEqual([], list(Draft202012Validator(command_schema).iter_errors(commands)))
        self.assertEqual([], list(Draft202012Validator(error_schema).iter_errors(catalog)))
        codes = {item["code"] for item in catalog["errors"]}
        for command in commands["commands"]:
            self.assertEqual(PACKAGE.name, command["owner"])
            self.assertTrue((PACKAGE / command["entrypoint"]).is_file())
            self.assertLessEqual(set(command["errors"]), codes)

    def test_commands_help_without_repository_writes(self) -> None:
        commands = json.loads((PACKAGE / "commands.json").read_text())
        for command in commands["commands"]:
            with self.subTest(command=command["id"]):
                self.assertEqual(0, main(PACKAGE, [command["id"], "--help"]))

    def test_launchers_are_executable_and_bind_validators(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text())
        for validator in interface["validators"]:
            wrapper = PACKAGE / validator["command"]
            self.assertTrue(os.access(wrapper, os.X_OK), wrapper)
            self.assertIn('source "$LAUNCHER" ' + validator["runtime_command"], wrapper.read_text())

    def test_public_wrapper_serializes_real_completed_owner(self) -> None:
        result = subprocess.run(
            [str(PACKAGE / "scripts/invoke.sh"), "--input", str(PACKAGE / "examples/public-selected-route-input.json"), "--owner-result", str(PACKAGE / "examples/task-free-change-review.json"), "--json"],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(result.returncode, 0, result)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["exit_id"], "completed")
        self.assertEqual(payload["edited_paths"], ["docs/guide.md"])
        self.assertEqual(payload["validation_summary"]["overall_status"], "passed")
        self.assertTrue(payload["unverified_boundaries"])
        self.assertNotIn("command", json.dumps(payload))
        self.assertNotIn("post_write_review", payload)


if __name__ == "__main__":
    unittest.main()
