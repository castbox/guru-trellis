"""Publish error contracts at the production wrapper and direct command boundaries."""
from __future__ import annotations

import json
from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[4]


def public_input():
    return json.loads((PACKAGE / "examples/public-delivery-review-ready-input-1.0.json").read_text())


class PublicWrapperErrors(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.bin = Path(temporary.name)
        self.calls = self.bin / "calls.jsonl"
        self.calls.touch()
        real_git = shutil.which("git")
        for name in ("git", "gh"):
            executable = self.bin / name
            executable.write_text(
                "#!" + sys.executable + "\nimport json,os,sys\nfrom pathlib import Path\n"
                "with Path(" + repr(str(self.calls)) + ").open('a') as f: f.write(json.dumps(sys.argv)+'\\n')\n"
                + ("os.execv(" + repr(real_git) + ",['git',*sys.argv[1:]])\n" if name == "git" else "sys.exit(99)\n")
            )
            executable.chmod(0o755)

    def invoke(self, value):
        review = (PACKAGE / "examples/semantic-review.json").read_text()
        environment = {**os.environ, "PATH": str(self.bin) + os.pathsep + os.environ["PATH"]}
        completed = subprocess.run(
            ["bash", str(PACKAGE / "scripts/invoke.sh"), "--root", str(REPO),
             "--input", value, "--review-input", review],
            cwd=REPO, env=environment, text=True, capture_output=True,
        )
        self.assertEqual(completed.stderr, "")
        output = json.loads(completed.stdout)
        self.assertEqual(set(output), {"code", "field_path", "remediation"})
        self.assertTrue(output["remediation"])
        calls = [json.loads(line) for line in self.calls.read_text().splitlines()]
        # Resolver and owner may locate Git, but must not reach publication or GitHub.
        self.assertTrue(all(Path(row[0]).name == "git" and row[1] == "rev-parse" for row in calls), calls)
        return completed.returncode, output

    def test_retired_review_ready_is_rejected_before_task_or_publication(self):
        status, output = self.invoke(json.dumps(public_input()))
        self.assertEqual(status, 2)
        self.assertEqual((output["code"], output["field_path"]), ("schema_mismatch", "input"))

    def test_invalid_json_retains_shared_reader_contract(self):
        status, output = self.invoke("{")
        self.assertEqual(status, 2)
        self.assertEqual((output["code"], output["field_path"]), ("invalid_json", "input"))


class DirectCommandErrors(unittest.TestCase):
    def setUp(self):
        self.path_before = list(sys.path)
        self.addCleanup(setattr, sys, "path", self.path_before)
        sys.path.insert(0, str(PACKAGE / "runtime"))
        modules = {}
        for name in ("owner", "legacy_maintenance"):
            spec = importlib.util.spec_from_file_location(name, PACKAGE / "runtime" / (name + ".py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules[name] = module
        context = patch.dict(sys.modules, modules)
        context.start()
        self.addCleanup(context.stop)
        self.owner = modules["owner"]
        self.legacy = modules["legacy_maintenance"]
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.temporary = Path(temporary.name)

    def command(self, command, *arguments):
        from runtime.command import main
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(PACKAGE, [command, "--root", str(REPO), *arguments])
        self.assertEqual(stderr.getvalue(), "")
        output = json.loads(stdout.getvalue())
        self.assertEqual(set(output), {"code", "field_path", "remediation"})
        return status, output

    def test_preview_record_check_execute_keep_classified_input_errors(self):
        public = public_input()
        public.pop("readiness_result_id")
        commands = (
            ("preview-task-delivery-publication", []),
            ("record-task-delivery-publication-gate", ["--review-input", "{}"]),
            ("check-task-delivery-publication-gate", ["--gate", "unused"]),
            ("execute-task-delivery-publication", ["--gate", "unused"]),
        )
        with patch.object(self.owner, "task_context") as task, patch.object(self.owner, "_run", wraps=self.owner._run) as effects:
            for command, extra in commands:
                with self.subTest(command=command):
                    status, output = self.command(command, "--input", json.dumps(public), *extra)
                    self.assertEqual((status, output["code"], output["field_path"]),
                                     (2, "schema_mismatch", "input.readiness_result_id"))
        task.assert_not_called()
        self.assertTrue(all(call.args[1] == ["git", "rev-parse", "--show-toplevel"] for call in effects.call_args_list))

    def test_publication_stale_remediation_matches_catalog_and_current_route(self):
        catalog = json.loads((PACKAGE / "errors/catalog.json").read_text(encoding="utf-8"))
        catalog_remediation = next(
            item["remediation"]
            for item in catalog["errors"]
            if item["code"] == "publication_stale"
        )
        owner_remediation = self.owner.PUBLIC_ERRORS["publication_stale"][1]
        self.assertEqual(catalog_remediation, owner_remediation)
        self.assertIn("Branch Review", owner_remediation)
        self.assertIn("Publication preparation/readiness", owner_remediation)

    def test_all_five_entry_boundaries_keep_unknown_failures_safe_at_exit_70(self):
        sentinel = "private-body-and-credential-sentinel"
        commands = (
            ("invoke-guru-publish-task-delivery", ["--review-input", "{}"]),
            ("preview-task-delivery-publication", []),
            ("record-task-delivery-publication-gate", ["--review-input", "{}"]),
            ("execute-task-delivery-publication", ["--gate", "unused"]),
            ("legacy-maintenance-guru-publish-task-delivery", []),
        )
        legacy = json.loads((PACKAGE / "examples/legacy_control_inspection-input-1.0.json").read_text())
        legacy["root"] = str(REPO)
        for command, extra in commands:
            with self.subTest(command=command):
                target, attribute = ((self.legacy, "execute") if command.startswith("legacy-") else (self.owner, "repo_root"))
                with patch.object(target, attribute, side_effect=KeyError(sentinel)):
                    status, output = self.command(command, "--input", json.dumps(legacy if command.startswith("legacy-") else public_input()), *extra)
                self.assertEqual((status, output["code"], output["field_path"]), (70, "internal_error", "runtime"))
                self.assertIn("maintenance", output["remediation"])
                self.assertNotIn(sentinel, json.dumps(output))

    def test_known_external_failure_retains_exit_4_without_private_payload(self):
        sentinel = "private-command-stderr-sentinel"
        with patch("subprocess.run", return_value=subprocess.CompletedProcess([sentinel], 1, "", sentinel)):
            status, output = self.command("execute-task-delivery-publication", "--input", json.dumps(public_input()), "--gate", "unused")
        self.assertEqual((status, output["code"]), (4, "external_command_failed"))
        self.assertNotIn(sentinel, json.dumps(output))

    def test_migration_preserves_json_schema_and_private_state_categories(self):
        source = self.temporary / "input.json"
        review = self.temporary / "review.json"
        review.write_text(json.dumps({"status": "passed", "summary": "Original transaction reviewed.", "evidence": ["Original owner transaction."]}))
        args = ("--input", str(source), "--owner-result", str(review), "--preview")
        source.write_text("{")
        status, output = self.command("migrate-task-delivery-publication", *args)
        self.assertEqual((status, output["code"]), (2, "invalid_json"))
        self.assertNotIn(str(source), json.dumps(output))
        source.write_text("{}")
        status, output = self.command("migrate-task-delivery-publication", *args)
        self.assertEqual((status, output["code"], output["field_path"]), (2, "schema_mismatch", "input"))
        source.write_text(json.dumps({"profile": "publication_transaction_636", "transaction_ref": "c" * 64,
                                      "task_ref": public_input()["task_ref"], "delivery_key": public_input()["delivery_key"]}))
        with patch.object(self.owner, "load_transaction", return_value=None):
            status, output = self.command("migrate-task-delivery-publication", *args)
        self.assertEqual((status, output["code"], output["field_path"]), (3, "private_state_missing", "transaction"))


if __name__ == "__main__":
    unittest.main()
