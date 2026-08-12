from __future__ import annotations

import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from jsonschema import Draft202012Validator


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = PACKAGE_ROOT.parents[1]
PACKAGE_RUNTIME = PACKAGE_ROOT / "runtime"
for path in (SKILLS_ROOT, PACKAGE_RUNTIME):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from runtime.io import CommandError  # noqa: E402
import check as wording_check  # noqa: E402
import common as wording_common  # noqa: E402
import invoke as wording_invoke  # noqa: E402
import record as wording_record  # noqa: E402


DIMENSIONS = (
    "complete_profile_scope",
    "all_hits_classified",
    "zero_unchecked_hits",
    "product_semantics_preserved",
    "retained_reasons_sufficient",
    "zero_hits_not_requirement_review",
)


class ContractWordingPackageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.path = self.root / "docs/contract.md"
        self.path.parent.mkdir(parents=True)
        self.path.write_text("# Contract\n\n建议使用固定值。\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_json(self, name: str, value: dict) -> Path:
        path = self.root / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return path

    def scan(self) -> dict:
        return wording_record.run(
            PACKAGE_ROOT,
            {},
            ["--root", str(self.root), "--mode", "standalone", "--profile", "explicit_paths", "--input", "unused", "--path", "docs/contract.md", "--scan-only"],
        )

    def authoring(self, scan: dict, *, typed_exit: str = "pass", classification: str = "term_definition") -> dict:
        return {
            "generated_at": "2026-08-12T00:00:00Z",
            "revisions": [],
            "classifications": [
                {"hit_id": hit["hit_id"], "classification": classification, "reason": "The term has one reviewed deterministic meaning."}
                for hit in scan["scan"]["hits"]
            ],
            "ai_review_gate": {
                "status": "blocked" if typed_exit == "blocked" else "passed",
                "reviewer": "package-local-test",
                "summary": "The complete fixed scope and current scan were reviewed.",
                "reviewed_scan_sha256": scan["scan"]["scan_sha256"],
                "checked_dimensions": {name: typed_exit != "blocked" for name in DIMENSIONS},
            },
            "typed_exit": typed_exit,
        }

    def record(self, *, typed_exit: str = "pass", classification: str = "term_definition") -> dict:
        scan = self.scan()
        input_path = self.write_json("authoring.json", self.authoring(scan, typed_exit=typed_exit, classification=classification))
        return wording_record.run(
            PACKAGE_ROOT,
            {},
            ["--root", str(self.root), "--mode", "standalone", "--profile", "explicit_paths", "--input", str(input_path), "--path", "docs/contract.md"],
        )

    def test_interface_declares_semantic_closed_loop_and_fixed_exits(self) -> None:
        interface = json.loads((PACKAGE_ROOT / "interface.json").read_text(encoding="utf-8"))
        self.assertEqual("semantic", interface["judgment_mode"])
        self.assertEqual(["pass", "content_changed", "blocked"], [item["id"] for item in interface["external_exits"]])

    def test_scanner_covers_complete_vocabulary(self) -> None:
        self.path.write_text("# Vocabulary\n\n" + " | ".join(wording_common.VOCAB) + "\n", encoding="utf-8")
        self.assertEqual(set(wording_common.VOCAB), {hit["term"] for hit in self.scan()["scan"]["hits"]})

    def test_record_check_and_pass_invocation_are_package_local(self) -> None:
        result = self.record()
        result_path = self.write_json("result.json", result)
        checked = wording_check.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--input", str(result_path), "--path", "docs/contract.md"])
        self.assertEqual("pass", checked["typed_exit"])
        public_input = {"profile": "explicit_paths", "source_exit": "start", "mode": "standalone", "paths": ["docs/contract.md"], "continuation_id": "stage0-current"}
        envelope = self.write_json("invoke.json", {"public_input": public_input, "owner_result": result})
        output = wording_invoke.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--invocation", str(envelope)])
        self.assertEqual({"exit_id": "pass", "profile": "explicit_paths", "continuation_id": "stage0-current"}, output)
        schema = json.loads((PACKAGE_ROOT / "schemas/public-pass-output-2.0.schema.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(output)))

    def test_content_drift_invalidates_recorded_result(self) -> None:
        result_path = self.write_json("result.json", self.record())
        self.path.write_text("# Contract\n\n固定值。\n", encoding="utf-8")
        with self.assertRaises(CommandError) as raised:
            wording_check.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--input", str(result_path), "--path", "docs/contract.md"])
        self.assertEqual("stale_identity", raised.exception.code)

    def test_contract_violation_routes_blocked(self) -> None:
        result = self.record(typed_exit="blocked", classification="contract_violation")
        envelope = self.write_json("blocked.json", {"public_input": {"profile": "explicit_paths", "source_exit": "start", "mode": "standalone", "paths": ["docs/contract.md"], "continuation_id": "stage0-current"}, "owner_result": result})
        self.assertEqual({"exit_id": "blocked"}, wording_invoke.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--invocation", str(envelope)]))

    def test_incomplete_classification_fails_closed(self) -> None:
        scan = self.scan()
        authoring = self.authoring(scan)
        authoring["classifications"] = []
        path = self.write_json("incomplete.json", authoring)
        with self.assertRaises(CommandError) as raised:
            wording_record.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--mode", "standalone", "--profile", "explicit_paths", "--input", str(path), "--path", "docs/contract.md"])
        self.assertEqual("schema_mismatch", raised.exception.code)

    def test_eval_owner_staging_api_builds_schema_valid_result(self) -> None:
        scope, contents = wording_common.contract_wording_build_scope(
            self.root, "explicit_paths", "standalone", explicit_paths=["docs/contract.md"]
        )
        scan = wording_common.scan_contract_wording(scope, contents)
        authored = {
            "generated_at": "2026-08-12T00:00:00Z",
            "semantic_review": {
                "revisions": [],
                "classifications": [
                    {"hit_id": hit["hit_id"], "classification": "term_definition", "reason": "The term is reviewed."}
                    for hit in scan["hits"]
                ],
                "ai_review_gate": {
                    "status": "passed",
                    "reviewer": "package-local-test",
                    "summary": "The fixed scope and every hit were reviewed.",
                    "reviewed_scan_sha256": scan["scan_sha256"],
                    "checked_dimensions": {name: True for name in DIMENSIONS},
                },
            },
            "typed_exit": "pass",
        }
        result = wording_common.contract_wording_derive_result(
            "explicit_paths", "standalone", scope, scan, authored
        )
        schema = json.loads((PACKAGE_ROOT / "schemas/contract-wording-review.schema.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(result)))

    def test_runtime_does_not_import_monolith(self) -> None:
        for path in (PACKAGE_ROOT / "runtime").glob("*.py"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("guru_team_trellis.py", text)
            self.assertNotIn("spec_from_file_location", text)

    def test_existing_issue_source_requires_exact_live_reread(self) -> None:
        source = {"source_kind": "issue", "identity": "https://github.com/example/repo/issues/27", "title": "Current", "body": "Body", "updated_at": "2026-08-12T00:00:00Z"}
        live = {"number": 27, "url": source["identity"], "state": "OPEN", "title": source["title"], "body": source["body"], "updatedAt": source["updated_at"]}
        with mock.patch.object(wording_common.subprocess, "run", return_value=__import__("subprocess").CompletedProcess([], 0, json.dumps(live), "")):
            self.assertIs(source, wording_common.live_issue_source(source))
        live["body"] = "Changed"
        with mock.patch.object(wording_common.subprocess, "run", return_value=__import__("subprocess").CompletedProcess([], 0, json.dumps(live), "")), self.assertRaises(CommandError):
            wording_common.live_issue_source(source)


if __name__ == "__main__":
    unittest.main()
