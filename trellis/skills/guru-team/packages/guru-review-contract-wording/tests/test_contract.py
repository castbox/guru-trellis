from __future__ import annotations

import copy
import hashlib
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

    def change_request_owner(self) -> tuple[dict, dict]:
        change = {
            "source_kind": "draft",
            "identity": "draft-274",
            "title": "Exact title",
            "body": "Exact body",
            "updated_at": None,
        }
        scope = wording_common.scope(self.root, "change_request", change=change)
        contents = {item["id"]: change[item["field"]] for item in scope["items"]}
        scan = wording_common.scan(scope, contents)
        authored = {
            "generated_at": "2026-08-18T00:00:00Z",
            "semantic_review": {
                "revisions": [],
                "classifications": [],
                "ai_review_gate": {
                    "status": "passed",
                    "reviewer": "package-local-test",
                    "summary": "The complete title and body scope was reviewed.",
                    "reviewed_scan_sha256": scan["scan_sha256"],
                    "checked_dimensions": {name: True for name in DIMENSIONS},
                },
            },
            "typed_exit": "pass",
        }
        owner = wording_common.contract_wording_derive_result(
            "change_request", "workflow", scope, scan, authored
        )
        wording_common.validate_result(PACKAGE_ROOT, owner)
        return owner, change

    def invoke_change_request(self, owner: dict) -> dict:
        transition = json.loads(
            (PACKAGE_ROOT / "examples/public-pass-output-2.0.json").read_text()
        )["transition"]
        transition.update({
            "stage": "clarity_current",
            "transition_id": "clarity_current:" + "3" * 24,
        })
        for field in ("wording_facts_sha256", "target_content_sha256", "wording"):
            transition.pop(field, None)
        envelope = self.write_json("change-request-invoke.json", {
            "public_input": {
                "profile": "change_request",
                "source_exit": "clear",
                "mode": "workflow",
                "target_locator": transition["target_locator"],
                "continuation_id": transition["continuation_id"],
            },
            "transition": transition,
            "owner_result": owner,
            "validation_receipt": wording_common.validation_receipt(owner),
        })
        return wording_invoke.run(
            PACKAGE_ROOT,
            {},
            ["--root", str(self.root), "--invocation", str(envelope)],
        )

    @staticmethod
    def reseal_owner(owner: dict) -> None:
        scope = owner["scope"]
        scope["scope_sha256"] = wording_common.digest({
            "identity": scope["identity"],
            "items": scope["items"],
        })
        unsigned = {key: value for key, value in owner.items() if key != "facts_sha256"}
        owner["facts_sha256"] = wording_common.digest(unsigned)

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
        envelope = self.write_json("invoke.json", {"public_input": public_input, "owner_result": result, "validation_receipt": checked["validation_receipt"]})
        output = wording_invoke.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--invocation", str(envelope)])
        self.assertEqual({"exit_id": "pass", "profile": "explicit_paths", "continuation_id": "stage0-current"}, output)
        schema = json.loads((PACKAGE_ROOT / "schemas/public-pass-output-2.0.schema.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(output)))

    def test_change_request_pass_projects_canonical_title_body_identity(self) -> None:
        owner, change = self.change_request_owner()
        output = self.invoke_change_request(owner)
        title_sha256 = hashlib.sha256(change["title"].encode()).hexdigest()
        body_sha256 = hashlib.sha256(change["body"].encode()).hexdigest()
        expected = wording_common.digest({
            "title_sha256": title_sha256,
            "body_sha256": body_sha256,
        })
        transition = output["transition"]
        self.assertEqual(expected, transition["target_content_sha256"])
        self.assertEqual(expected, transition["wording"]["target_content_sha256"])
        self.assertNotEqual(body_sha256, expected)
        self.assertEqual(
            "wording_current:" + wording_common.digest(transition["wording"])[:24],
            transition["transition_id"],
        )

    def test_change_request_pass_rejects_missing_or_duplicate_title_body(self) -> None:
        owner, _ = self.change_request_owner()
        cases = {
            "missing-title": ["body"],
            "missing-body": ["title"],
            "duplicate-title": ["title", "title", "body"],
            "duplicate-body": ["title", "body", "body"],
        }
        original = {item["field"]: item for item in owner["scope"]["items"]}
        for name, fields in cases.items():
            candidate = copy.deepcopy(owner)
            candidate["scope"]["items"] = [copy.deepcopy(original[field]) for field in fields]
            self.reseal_owner(candidate)
            with self.subTest(case=name), self.assertRaises(CommandError) as raised:
                self.invoke_change_request(candidate)
            self.assertEqual("stale_identity", raised.exception.code)
            self.assertEqual("owner_result.scope", raised.exception.field_path)

    def test_content_drift_invalidates_recorded_result(self) -> None:
        result_path = self.write_json("result.json", self.record())
        self.path.write_text("# Contract\n\n固定值。\n", encoding="utf-8")
        with self.assertRaises(CommandError) as raised:
            wording_check.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--input", str(result_path), "--path", "docs/contract.md"])
        self.assertEqual("stale_identity", raised.exception.code)

    def test_public_invocation_rejects_missing_or_stale_receipt(self) -> None:
        result = self.record()
        public_input = {"profile": "explicit_paths", "source_exit": "start", "mode": "standalone", "paths": ["docs/contract.md"], "continuation_id": "stage0-current"}
        for receipt in (None, {"schema_version": "1.0"}):
            envelope = self.write_json("receipt.json", {"public_input": public_input, "owner_result": result, "validation_receipt": receipt})
            with self.assertRaises(CommandError) as raised:
                wording_invoke.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--invocation", str(envelope)])
            self.assertEqual("stale_identity", raised.exception.code)

    def test_contract_violation_routes_blocked(self) -> None:
        result = self.record(typed_exit="blocked", classification="contract_violation")
        result_path = self.write_json("blocked-result.json", result)
        checked = wording_check.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--input", str(result_path), "--path", "docs/contract.md"])
        envelope = self.write_json("blocked.json", {"public_input": {"profile": "explicit_paths", "source_exit": "start", "mode": "standalone", "paths": ["docs/contract.md"], "continuation_id": "stage0-current"}, "owner_result": result, "validation_receipt": checked["validation_receipt"]})
        self.assertEqual({"exit_id": "blocked"}, wording_invoke.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--invocation", str(envelope)]))

    def test_incomplete_classification_fails_closed(self) -> None:
        scan = self.scan()
        authoring = self.authoring(scan)
        authoring["classifications"] = []
        path = self.write_json("incomplete.json", authoring)
        with self.assertRaises(CommandError) as raised:
            wording_record.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--mode", "standalone", "--profile", "explicit_paths", "--input", str(path), "--path", "docs/contract.md"])
        self.assertEqual("schema_mismatch", raised.exception.code)

    def test_recorder_requires_explicit_semantic_exit(self) -> None:
        scan = self.scan()
        for value in (None, "unknown"):
            authoring = self.authoring(scan)
            if value is None:
                authoring.pop("typed_exit")
            else:
                authoring["typed_exit"] = value
            path = self.write_json(f"exit-{value}.json", authoring)
            with self.subTest(typed_exit=value), self.assertRaises(CommandError) as raised:
                wording_record.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--mode", "standalone", "--profile", "explicit_paths", "--input", str(path), "--path", "docs/contract.md"])
            self.assertEqual("schema_mismatch", raised.exception.code)

    def test_exit_gate_and_revision_relations_fail_closed(self) -> None:
        scan = self.scan()
        cases = []
        blocked_with_passed_gate = self.authoring(scan, typed_exit="blocked")
        blocked_with_passed_gate["ai_review_gate"]["status"] = "passed"
        cases.append(blocked_with_passed_gate)
        pass_with_blocked_gate = self.authoring(scan, typed_exit="pass")
        pass_with_blocked_gate["ai_review_gate"]["status"] = "blocked"
        cases.append(pass_with_blocked_gate)
        changed_without_revision = self.authoring(scan, typed_exit="content_changed")
        cases.append(changed_without_revision)
        changed_with_unchecked = self.authoring(scan, typed_exit="content_changed", classification="contract_violation")
        changed_with_unchecked["revisions"] = [{"path": "docs/contract.md", "before_sha256": "0" * 64, "after_sha256": "1" * 64, "summary": "Reviewed revision."}]
        cases.append(changed_with_unchecked)
        for index, authoring in enumerate(cases):
            path = self.write_json(f"relation-{index}.json", authoring)
            with self.subTest(index=index), self.assertRaises(CommandError) as raised:
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
