from __future__ import annotations

import argparse
import contextlib
import copy
import io
import json
import os
import subprocess
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from test_contract import PACKAGE, REPO, load, load_runtime


class PublicVerificationDiagnosticsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="verification-public-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "fixture@example.test")
        self.git("config", "user.name", "Verification Fixture")
        self.git("remote", "add", "origin", "https://github.com/castbox/guru-trellis.git")
        self.assets = (
            "trellis/guru-team-extension.json",
            "trellis/index.json",
            "trellis/workflows/guru-team/workflow.md",
            "trellis/presets/guru-team/scripts/bash/apply.sh",
        )
        for relative in self.assets:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n", encoding="utf-8")
        self.public = load("examples/public-source-repository-verification-input.json")
        self.write("source.json", self.public)
        self.write("owner.json", {})
        self.write("execution.json", load("examples/execution-facts.json"))
        (self.root / "invalid.json").write_text("ordinary incomplete JSON", encoding="utf-8")
        self.write("array.json", [])
        self.commit()

    def git(self, *argv: str) -> str:
        return subprocess.run(
            ["git", *argv], cwd=self.root, text=True, capture_output=True, check=True,
        ).stdout.strip()

    def write(self, relative: str, payload) -> None:
        (self.root / relative).write_text(json.dumps(payload), encoding="utf-8")

    def commit(self) -> None:
        self.git("add", ".")
        self.git("commit", "-q", "-m", "verification fixture")

    def invoke(self, command: str, *argv: str, stdin: str | None = None):
        return subprocess.run(
            ["bash", str(PACKAGE / "scripts" / ("invoke.sh" if command == "invoke-extension-verification" else f"{command}.sh")),
             "--root", str(self.root), *argv],
            cwd=REPO, text=True, capture_output=True, input=stdin, check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
                 "GURU_TEAM_INVOKED_PACKAGE_ROOT": str(PACKAGE)},
        )

    def diagnostic(self, result, code: str, field: str, reason: str = "") -> dict:
        self.assertEqual(result.returncode, 2, result)
        self.assertEqual(result.stderr, "", result)
        payload = json.loads(result.stdout)
        self.assertEqual(set(payload), {"code", "field_path", "remediation"})
        self.assertEqual(payload["code"], code, result)
        self.assertEqual(payload["field_path"], field, result)
        self.assertIn("references/contract.md#", payload["remediation"])
        self.assertIn(reason, payload["remediation"])
        self.assertNotIn(str(self.root), result.stdout)
        self.assertFalse((self.root / ".trellis/.runtime").exists())
        return payload

    def execute(self, carrier: str):
        return self.invoke("execute-extension-verification", "--input", carrier,
                           "--capability", "marketplace_index")

    def test_file_carriers_and_owner_stdin_preserve_existing_success_domain(self) -> None:
        owner = load_runtime()
        with mock.patch.dict(os.environ, {"GURU_TEAM_INVOKED_PACKAGE_ROOT": str(PACKAGE)}):
            self.assertEqual(owner.extension_verification_public_input(self.root, "source.json"), self.public)
            self.assertEqual(owner.extension_verification_public_input(
                self.root, "examples/public-source-repository-verification-input.json"), self.public)
            with mock.patch("sys.stdin", io.StringIO('{"status":"recorded"}')):
                self.assertEqual(owner.extension_verification_owner_input(self.root, "-"),
                                 ({"status": "recorded"}, "<stdin>"))

    def test_execute_wrapper_classifies_ordinary_file_carrier_errors(self) -> None:
        for carrier in (str(self.root / "source.json"), "-", json.dumps(self.public),
                        "missing.json", "trellis", "invalid.json", "array.json"):
            with self.subTest(carrier=carrier):
                self.diagnostic(self.execute(carrier), "invalid_arguments", "input")

    def test_relative_files_reach_real_dirty_source_preflight_without_execution(self) -> None:
        (self.root / self.assets[0]).write_text("changed\n", encoding="utf-8")
        for carrier in ("source.json", "examples/public-source-repository-verification-input.json"):
            with self.subTest(carrier=carrier):
                self.diagnostic(self.execute(carrier), "source_verification_failed", "root",
                                "source_checkout_not_clean")

    def test_public_wrapper_source_preconditions_have_distinct_static_diagnostics(self) -> None:
        asset = self.root / self.assets[0]
        original = asset.read_bytes()
        asset.unlink()
        self.diagnostic(self.execute("source.json"), "source_verification_failed", "root",
                        "source_repository_required")
        asset.write_bytes(original)
        self.git("remote", "set-url", "origin", "https://github.com/example/business.git")
        self.diagnostic(self.execute("source.json"), "source_verification_failed", "root.origin",
                        "source_origin_mismatch")
        self.git("remote", "set-url", "origin", "https://github.com/castbox/guru-trellis.git")
        self.write("source.json", {**self.public, "ref": "refs/heads/missing"})
        self.diagnostic(self.execute("source.json"), "source_verification_failed", "input.ref",
                        "source_ref_head_mismatch")

    def test_all_adapters_project_the_actual_carrier_field(self) -> None:
        cases = (
            ("record-extension-verification", ["--input", "-", "--execution-input", "execution.json",
                                               "--review-input", "review.json"], "input"),
            ("record-extension-verification", ["--input", "source.json", "--execution-input", "-",
                                               "--review-input", "review.json"], "execution_input"),
            ("record-extension-verification", ["--input", "source.json", "--execution-input", "execution.json",
                                               "--review-input", "-"], "review_input"),
            ("check-extension-verification", ["--input", "missing.json"], "input"),
            ("check-extension-verification", ["--input", "owner.json", "--public-input", "-"], "public_input"),
            ("invoke-extension-verification", ["--input", "-", "--owner-result", "owner.json"], "input"),
            ("invoke-extension-verification", ["--input", "source.json", "--owner-result", "missing.json"], "owner_result"),
        )
        for command, argv, field in cases:
            with self.subTest(command=command, field=field):
                self.diagnostic(self.invoke(command, *argv), "invalid_arguments", field)

    def test_owner_result_stdin_errors_are_classified_at_check_and_invoke(self) -> None:
        for command, argv, field in (
            ("check-extension-verification", ["--input", "-"], "input"),
            ("invoke-extension-verification", ["--input", "source.json", "--owner-result", "-"], "owner_result"),
        ):
            for content in ("incomplete JSON", "[]"):
                with self.subTest(command=command, content=content):
                    self.diagnostic(self.invoke(command, *argv, stdin=content), "invalid_arguments", field)

    def test_unclassified_owner_errors_are_not_reinterpreted(self) -> None:
        owner = load_runtime()
        error = owner.WorkflowError("unclassified local failure", payload={"errors": ["local detail"]})
        def operation(args):
            raise error
        with self.assertRaises(owner.WorkflowError) as raised:
            owner.extension_verification_public_call(operation, argparse.Namespace())
        self.assertIs(raised.exception, error)

    def schema_diagnostic(self, result, field: str, schema_name: str, constraint: str) -> None:
        self.assertEqual(result.returncode, 2, result)
        self.assertEqual(result.stderr, "", result)
        payload = json.loads(result.stdout)
        self.assertEqual(set(payload), {"code", "field_path", "remediation"})
        self.assertEqual(payload["code"], "invalid_arguments", result)
        self.assertEqual(payload["field_path"], field, result)
        self.assertIn("Contract packages/guru-verify-extension-installation/schemas/" + schema_name,
                      payload["remediation"])
        self.assertIn(constraint, payload["remediation"])
        self.assertNotIn(str(self.root), result.stdout)
        self.assertFalse((self.root / ".trellis/.runtime").exists())

    def test_public_input_schema_rejections_use_the_shared_safe_diagnostic(self) -> None:
        for missing in (True, False):
            payload = copy.deepcopy(self.public)
            if missing:
                del payload["mode"]
            else:
                payload["mode"] = "workflow"
            self.write("source.json", payload)
            result = self.execute("source.json")
            self.schema_diagnostic(result, "input.mode", "public-source-repository-verification-input.schema.json",
                                   "required field is missing" if missing else "const must match")
            self.assertNotIn('"workflow"', result.stdout)

    def test_execution_schema_rejections_use_the_shared_safe_diagnostic(self) -> None:
        for missing in (True, False):
            payload = load("examples/execution-facts.json")
            if missing:
                del payload["status"]
            else:
                payload["status"] = "ordinary-invalid-status"
            self.write("execution.json", payload)
            self.commit()
            result = self.invoke("record-extension-verification", "--input", "source.json",
                                 "--execution-input", "execution.json", "--review-input", "unused.json")
            self.schema_diagnostic(result, "execution_input.status", "execution-facts.schema.json",
                                   "required field is missing" if missing else "enum must match")
            self.assertNotIn("ordinary-invalid-status", result.stdout)

    def test_review_schema_rejections_use_the_shared_safe_diagnostic(self) -> None:
        for missing in (True, False):
            payload = load("examples/semantic-review-input.json")
            if missing:
                del payload["typed_exit"]
            else:
                payload["typed_exit"] = "ordinary-invalid-exit"
            self.write("review.json", payload)
            self.commit()
            result = self.invoke("record-extension-verification", "--input", "source.json",
                                 "--execution-input", "execution.json", "--review-input", "review.json")
            self.schema_diagnostic(result, "review_input.typed_exit", "semantic-review-input-2.0.schema.json",
                                   "required field is missing" if missing else "enum must match")
            self.assertNotIn("ordinary-invalid-exit", result.stdout)

    def test_legal_original_fixtures_do_not_enter_the_diagnostic_validator(self) -> None:
        owner = load_runtime()
        self.write("review.json", load("examples/semantic-review-input.json"))
        with mock.patch.dict(os.environ, {"GURU_TEAM_INVOKED_PACKAGE_ROOT": str(PACKAGE)}), \
                mock.patch.object(owner, "validate_json") as formatter:
            self.assertEqual(owner.extension_verification_public_input(self.root, "source.json"), self.public)
            self.assertEqual(owner.extension_verification_execution_input(self.root, "execution.json"),
                             load("examples/execution-facts.json"))
            self.assertEqual(owner.extension_verification_review_input(self.root, "review.json"),
                             load("examples/semantic-review-input.json"))
            formatter.assert_not_called()

    def test_unexpected_formatter_fault_keeps_the_original_public_internal_error(self) -> None:
        from runtime import command as dispatcher
        owner = load_runtime()
        self.write("source.json", {**self.public, "mode": "workflow"})
        def operation(args):
            return owner.extension_verification_public_input(self.root, "source.json")
        entry = types.SimpleNamespace(run=lambda *args: owner.extension_verification_public_call(
            operation, argparse.Namespace()))
        output = io.StringIO()
        with mock.patch.dict(os.environ, {"GURU_TEAM_INVOKED_PACKAGE_ROOT": str(PACKAGE)}), \
                mock.patch.object(owner, "validate_json", side_effect=RuntimeError("local failure detail")), \
                mock.patch.object(dispatcher, "_load_entrypoint", return_value=entry), \
                contextlib.redirect_stdout(output):
            status = dispatcher.main(PACKAGE, ["execute-extension-verification", "--input", "source.json",
                                                "--capability", "marketplace_index"])
        self.assertEqual(status, 2)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["code"], "internal_error")
        self.assertNotIn("local failure detail", output.getvalue())

    def test_command_help_describes_each_supported_carrier(self) -> None:
        commands = {item["id"]: item for item in load("commands.json")["commands"]}
        for command in ("execute-extension-verification", "record-extension-verification"):
            self.assertEqual(commands[command]["stdin"], "none")
        for command in ("execute-extension-verification", "record-extension-verification",
                        "check-extension-verification", "invoke-extension-verification"):
            result = subprocess.run(
                ["bash", str(PACKAGE / "scripts" / ("invoke.sh" if command == "invoke-extension-verification" else f"{command}.sh")), "--help"],
                cwd=REPO, text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            self.assertIn("Repo- or package-relative regular", result.stdout)
            if command in ("check-extension-verification", "invoke-extension-verification"):
                self.assertIn("owner result from stdin", result.stdout)


if __name__ == "__main__":
    unittest.main()
