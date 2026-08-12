from __future__ import annotations

import copy
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
import check as review_check  # noqa: E402
import common as review_common  # noqa: E402
import invoke as review_invoke  # noqa: E402
import record as review_record  # noqa: E402


class ChangeRequestReviewPackageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / "draft.json"
        self.source_value = {"kind": "draft", "draft_id": "draft-27", "title": "Add package-local review", "body": "Deliver one independently testable change.", "selected_comments": []}
        self.write(self.source, self.source_value)
        body_hash = review_common.sha(self.source_value["body"])
        authority = {"kind": "draft", "repo": "example/guru-extension", "issue_number": None, "url": None, "state": "draft", "updated_at": None, "body_sha256": body_hash}
        self.raw_target = {"kind": "proposed_draft", "repo": "example/guru-extension", "draft_id": "draft-27", "source_request_sha256": review_common.digest(authority), "title_sha256": review_common.sha(self.source_value["title"]), "body_sha256": body_hash, "side_effect_free": True}
        self.target = review_common.normalize_target(self.source_value, self.raw_target)
        self.prerequisites = {
            "clarity": {"status": "current", "schema_id": "guru-requirements-clarification-2.0", "typed_exit": "clear", "payload_sha256": "a" * 64, "facts_sha256": "b" * 64, "target_sha256": self.target["identity_sha256"], "disposition_sha256": "c" * 64, "content_sha256": self.target["content_sha256"], "scope_sha256": "d" * 64, "error_codes": []},
            "wording": {"status": "current", "schema_id": "guru-contract-wording-review-1.0", "profile": "change_request", "typed_exit": "pass", "payload_sha256": "e" * 64, "facts_sha256": "f" * 64, "scope_sha256": "1" * 64, "scan_sha256": "2" * 64, "target_content_sha256": self.target["content_sha256"], "error_codes": []},
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, path: Path, value: dict) -> Path:
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return path

    def authoring(self, exit_id: str = "ready") -> dict:
        linked = review_common.linkage(self.target, self.prerequisites)
        scope = {"requirement_scope_basis": "The reviewed draft defines the scope.", "delivery_unit_id": "draft-27", "close_issues": [], "related_issues": [], "followup_issues": [], "duplicate_reuse_decision": "No duplicate replaces this request.", "implementation_target": "The package-local review runtime.", "current_gap": "The package runtime is not implemented.", "archived_constraints": [], "risk_boundary": ["Normal workflow operation."], "excluded_scope": ["Workspace mutation is downstream."]}
        finding = {"finding_id": "finding-1", "category": "requirement_gap", "summary": "Requirements need clarification.", "blocking": True, "evidence_refs": ["evidence_linkage"], "affected_hashes": [linked["linkage_sha256"]], "route_basis": "Return to requirements clarification."}
        dimensions = []
        for index, dimension_id in enumerate(review_common.DIMENSIONS):
            failed = exit_id != "ready" and index == 0
            dimensions.append({"id": dimension_id, "status": "failed" if failed else "passed", "summary": "The dimension was reviewed against current evidence.", "evidence_refs": ["evidence_linkage"], "affected_hashes": [linked["linkage_sha256"]], "finding_ids": ["finding-1"] if failed else []})
        findings = [] if exit_id == "ready" else [finding]
        status = review_common.GATES[exit_id]
        return {"generated_at": "2026-08-12T00:00:00Z", "mode": "standalone", "target": copy.deepcopy(self.raw_target), "prerequisite_payloads": copy.deepcopy(self.prerequisites), "semantic_review": {"dimensions": dimensions, "findings": findings, "scope_conclusion": scope, "ai_review_gate": {"status": status, "reviewer": "package-local-test", "reviewed_linkage_sha256": linked["linkage_sha256"], "summary": "All dimensions and current evidence were reviewed.", "findings_count": len(findings), "scope_conclusion_sha256": review_common.digest(scope)}}, "typed_exit": exit_id, "reason": "The selected route follows the reviewed findings.", "affected_evidence": [{"ref": "evidence_linkage", "sha256": linked["linkage_sha256"], "summary": "Current target and prerequisite linkage."}], "consumer": review_common.CONSUMERS[exit_id]}

    def record(self, exit_id: str = "ready") -> dict:
        input_path = self.write(self.root / "authoring.json", self.authoring(exit_id))
        return review_record.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--mode", "standalone", "--input", str(input_path), "--change-request-input", str(self.source)])

    def test_interface_has_semantic_profile_and_five_exits(self) -> None:
        interface = json.loads((PACKAGE_ROOT / "interface.json").read_text())
        self.assertEqual("semantic", interface["judgment_mode"])
        self.assertEqual(list(review_common.CONSUMERS), [row["id"] for row in interface["external_exits"]])

    def test_record_check_and_ready_invoke_are_dynamic(self) -> None:
        result = self.record()
        result_path = self.write(self.root / "result.json", result)
        prereq_path = self.write(self.root / "prerequisites.json", self.prerequisites)
        checked = review_check.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--input", str(result_path), "--prerequisites-input", str(prereq_path), "--change-request-input", str(self.source), "--expected-facts-sha256", result["facts_sha256"]])
        self.assertEqual("ready", checked["typed_exit"])
        transition = json.loads((PACKAGE_ROOT.parent / "guru-review-contract-wording/examples/public-pass-output-2.0.json").read_text())["transition"]
        public_input = {"profile": "proposed_draft", "source_exit": "start", "mode": "standalone", "target_locator": "draft-27", "continuation_id": "stage0-current"}
        envelope = self.write(self.root / "invoke.json", {"public_input": public_input, "owner_result": result, "transition": transition})
        output = review_invoke.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--invocation", str(envelope)])
        self.assertEqual("ready", output["exit_id"])
        self.assertEqual(result["facts_sha256"], output["transition"]["readiness_facts_sha256"])
        schema = json.loads((PACKAGE_ROOT / "schemas/public-ready-output-3.0.schema.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(output)))

    def test_source_content_drift_fails_check(self) -> None:
        result_path = self.write(self.root / "result.json", self.record())
        prereq_path = self.write(self.root / "prerequisites.json", self.prerequisites)
        changed = dict(self.source_value)
        changed["body"] = "Changed current request."
        self.write(self.source, changed)
        with self.assertRaises(CommandError) as raised:
            review_check.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--input", str(result_path), "--prerequisites-input", str(prereq_path), "--change-request-input", str(self.source)])
        self.assertEqual("stale_identity", raised.exception.code)

    def test_non_ready_exit_requires_closed_finding_and_projects_route(self) -> None:
        result = self.record("blocked")
        envelope = self.write(self.root / "blocked.json", {"public_input": {"profile": "proposed_draft", "source_exit": "start", "mode": "standalone", "target_locator": "draft-27", "continuation_id": "stage0-current"}, "owner_result": result})
        self.assertEqual({"exit_id": "blocked"}, review_invoke.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--invocation", str(envelope)]))

    def test_missing_dimension_fails_closed(self) -> None:
        authored = self.authoring()
        authored["semantic_review"]["dimensions"].pop()
        path = self.write(self.root / "invalid.json", authored)
        with self.assertRaises(CommandError) as raised:
            review_record.run(PACKAGE_ROOT, {}, ["--root", str(self.root), "--mode", "standalone", "--input", str(path), "--change-request-input", str(self.source)])
        self.assertEqual("schema_mismatch", raised.exception.code)

    def test_runtime_has_no_monolith_or_example_projection(self) -> None:
        for path in (PACKAGE_ROOT / "runtime").glob("*.py"):
            text = path.read_text()
            self.assertNotIn("guru_team_trellis.py", text)
            self.assertNotIn("typed_output(package_root", text)

    def test_existing_issue_source_requires_exact_live_reread(self) -> None:
        source = {"kind": "issue", "repo": "example/repo", "number": 27, "title": "Current", "body": "Body", "updated_at": "2026-08-12T00:00:00Z"}
        live = {"number": 27, "url": "https://github.com/example/repo/issues/27", "state": "OPEN", "title": source["title"], "body": source["body"], "updatedAt": source["updated_at"]}
        with mock.patch.object(review_common.subprocess, "run", return_value=__import__("subprocess").CompletedProcess([], 0, json.dumps(live), "")):
            self.assertIs(source, review_common.live_issue_source(source))
        live["updatedAt"] = "2026-08-12T00:01:00Z"
        with mock.patch.object(review_common.subprocess, "run", return_value=__import__("subprocess").CompletedProcess([], 0, json.dumps(live), "")), self.assertRaises(CommandError):
            review_common.live_issue_source(source)


if __name__ == "__main__":
    unittest.main()
