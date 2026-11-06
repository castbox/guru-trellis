from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runtime import command
from runtime.io import CommandError
from runtime.schema import validate_json


ROOT = Path(__file__).resolve().parents[2]
PACKAGES = ROOT / "packages"


class PublicContractDiagnosticsTests(unittest.TestCase):
    def test_architecture_union_error_names_the_extra_field_in_the_current_branch(self):
        package = PACKAGES / "guru-maintain-architecture-baseline"
        value = json.loads((package / "examples/public-input-delivery-task-impact-sync-3.0.json").read_text())
        for name in ("source_exit", "requirement_authority", "behavior_authority"):
            value.pop(name)
        value.update(
            stage="branch_review", input_sha256="a" * 64,
            ai_review_gate={
                "status": "passed", "reviewed_scope": "schema-only fixture",
                "evidence_summary": "schema-only fixture", "findings": [],
                "conclusion": "schema-only fixture",
            },
            typed_exit="baseline_current",
            consumer={"kind": "workflow", "id": "guru-architecture-baseline-current-router"},
            baseline_identity=value["baseline"]["identity"],
            constitution_identity=value["constitution"]["identity"],
            impact_kind="no_architecture_impact", impact_reason="schema-only fixture",
            promotion_state="no_change",
        )
        schema = package / "schemas/semantic-result-delivery-3.0.schema.json"
        validate_json(value, schema, "owner_result")
        value["committed_range"] = {"base_ref": "ordinary-extra-value"}
        with self.assertRaises(CommandError) as raised:
            validate_json(value, schema, "owner_result")
        self.assertEqual(raised.exception.code, "schema_mismatch")
        self.assertEqual(raised.exception.field_path, "owner_result.committed_range")
        self.assertIn("field is not declared", raised.exception.remediation)
        self.assertNotIn("ordinary-extra-value", raised.exception.remediation)
        self.assertNotIn("planning:3.0", raised.exception.remediation)

    def test_nested_union_diagnostic_and_tied_alternatives(self):
        from jsonschema import Draft202012Validator
        from jsonschema.exceptions import best_match

        schema = {"anyOf": [
            {"type": "object", "properties": {"payload": {"oneOf": [
                {"type": "object", "properties": {"kind": {"const": "current"}},
                 "additionalProperties": False},
                {"type": "object", "required": ["legacy"],
                 "properties": {"kind": {"const": "legacy"}}},
            ]}}},
            {"type": "object", "required": ["other"], "properties": {"kind": {"const": "other"}}},
        ]}
        value = {"kind": "current", "payload": {"kind": "current", "extra": "ordinary-extra-value"}}
        tied_schema = {"oneOf": [
            {"properties": {"kind": {"const": "first"}}},
            {"properties": {"kind": {"const": "second"}}},
        ]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.json"
            path.write_text(json.dumps(schema))
            with self.assertRaises(CommandError) as raised:
                validate_json(value, path, "input")
            self.assertEqual(raised.exception.field_path, "input.payload.extra")
            path.write_text(json.dumps(tied_schema))
            with self.assertRaises(CommandError) as raised:
                validate_json(value, path, "input")
            original = best_match(Draft202012Validator(tied_schema).iter_errors(value))
            self.assertEqual(list(original.absolute_path), [])
            self.assertEqual(original.validator, "oneOf")
            self.assertEqual(raised.exception.field_path, "input")
            self.assertIn("oneOf constraint is not satisfied", raised.exception.remediation)

    def test_completion_help_locates_current_profile_and_semantic_contracts(self):
        stdout = StringIO()
        with redirect_stdout(stdout):
            status = command.main(PACKAGES / "guru-review-task-completion", [
                "invoke-guru-review-task-completion", "--help",
            ])
        self.assertEqual(status, 0)
        help_text = stdout.getvalue()
        for profile in ("delivery_completion", "delivery_evidence_refresh", "delivery_reactivation_validation"):
            self.assertIn(profile, help_text)
        self.assertIn("schemas/semantic-delivery-result-1.0.schema.json", help_text)
        self.assertIn("examples/semantic-delivery-result-1.0.json", help_text)
        self.assertIn("regular UTF-8 JSON file", help_text)

    def test_source_error_names_current_contract_and_undeclared_field_without_values(self):
        package = PACKAGES / "guru-create-task"
        value = json.loads((package / "examples/public-create-issue-input.json").read_text())
        source = value["creation"]["reviewed_source"]
        source["relation"] = source.pop("disposition")
        with self.assertRaises(CommandError) as raised:
            validate_json(value, package / "schemas/public-input.schema.json", "input")
        error = raised.exception
        self.assertEqual(error.code, "schema_mismatch")
        self.assertEqual(error.field_path, "input.creation.reviewed_source.relation")
        self.assertIn("field is not declared", error.remediation)
        self.assertIn("packages/guru-create-task/schemas/public-input.schema.json", error.remediation)
        self.assertIn("rerun this original command", error.remediation)
        self.assertNotIn(source["repo_ref"], error.remediation)

    def test_missing_source_disposition_names_the_required_field(self):
        package = PACKAGES / "guru-create-task"
        value = json.loads((package / "examples/public-create-issue-input.json").read_text())
        value["creation"]["reviewed_source"].pop("disposition")
        with self.assertRaises(CommandError) as raised:
            validate_json(value, package / "schemas/public-input.schema.json", "input")
        self.assertEqual(raised.exception.field_path, "input.creation.reviewed_source.disposition")
        self.assertIn("required field is missing", raised.exception.remediation)

    def test_source_enum_error_reports_allowed_literals_without_echoing_input(self):
        package = PACKAGES / "guru-create-task"
        value = json.loads((package / "examples/public-create-issue-input.json").read_text())
        value["creation"]["reviewed_source"]["disposition"] = "ordinary-invalid-choice"
        with self.assertRaises(CommandError) as raised:
            validate_json(value, package / "schemas/public-input.schema.json", "input")
        self.assertEqual(raised.exception.field_path, "input.creation.reviewed_source.disposition")
        self.assertIn("exact_source", raised.exception.remediation)
        self.assertIn("reference_only", raised.exception.remediation)
        self.assertNotIn("ordinary-invalid-choice", raised.exception.remediation)

    def test_terminal_owner_error_examples_and_real_errors_use_their_declared_schema(self):
        for name in ("guru-cleanup-task-resources", "guru-finish-task", "guru-review-task-completion"):
            with self.subTest(owner=name):
                package = PACKAGES / name
                invocation = json.loads((package / "interface.json").read_text())["public_contracts"]["invocation"]
                schema = package / invocation["error_schema"]["path"]
                validate_json(json.loads((package / invocation["error_example"]["path"]).read_text()), schema, "error")
                result = subprocess.run([
                    "bash", str(package / "scripts/invoke.sh"), "--root", str(ROOT.parents[2]),
                    "--input", "./missing-contract-diagnostics-input.json",
                    "--semantic-result", "./missing-contract-diagnostics-semantic.json",
                ], text=True, capture_output=True)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                error = json.loads(result.stdout)
                validate_json(error, schema, "error")
                self.assertEqual(error["code"], "invalid_json")
                self.assertEqual(error["field_path"], "input")

    def test_terminal_wrappers_parameter_errors_match_the_public_error_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.json"
            input_path.write_text("{}", encoding="utf-8")
            supplied = ["--input", str(input_path), "--semantic-result", str(input_path)]
            cases = (
                ("repeated_input", supplied + ["--input", str(input_path)], "conflicting_arguments", "arguments.--input"),
                ("repeated_json", ["--json", "--json"], "conflicting_arguments", "arguments.--json"),
                ("mixed_help", ["--help", "--root", "."], "conflicting_arguments", "arguments"),
                ("unknown_option", supplied + ["--unknown-option"], "invalid_arguments", "arguments"),
                ("missing_required", [], "invalid_arguments", "arguments"),
                ("missing_value", ["--input", str(input_path), "--semantic-result"], "invalid_arguments", "arguments"),
            )
            for name in ("guru-cleanup-task-resources", "guru-finish-task", "guru-review-task-completion"):
                package = PACKAGES / name
                invocation = json.loads((package / "interface.json").read_text())["public_contracts"]["invocation"]
                schema = package / invocation["error_schema"]["path"]
                for case, arguments, code, field_path in cases:
                    with self.subTest(owner=name, case=case):
                        result = subprocess.run([
                            "bash", str(package / "scripts/invoke.sh"), "--root", str(ROOT.parents[2]),
                            *arguments,
                        ], text=True, capture_output=True)
                        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                        error = json.loads(result.stdout)
                        self.assertEqual(set(error), {"code", "field_path", "remediation"})
                        self.assertEqual(error["code"], code)
                        self.assertEqual(error["field_path"], field_path)
                        validate_json(error, schema, "error")


if __name__ == "__main__":
    unittest.main()
