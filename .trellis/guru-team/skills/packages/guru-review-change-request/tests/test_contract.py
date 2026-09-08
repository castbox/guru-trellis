from __future__ import annotations

import copy
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = PACKAGE_ROOT.parents[1]
RUNTIME_ROOT = next(path for path in (SKILLS_ROOT / "runtime", SKILLS_ROOT.parent / "runtime") if path.is_dir())
for path in (RUNTIME_ROOT.parent, PACKAGE_ROOT / "runtime"):
    sys.path.insert(0, str(path))

from runtime.io import CommandError
import common as review_common
import record as review_record
import check as review_check
import invoke as review_invoke


class ChangeRequestReviewPackageTest(unittest.TestCase):
    # Package tests exercise public shapes, not the externally owned real-producer chain.
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = {"kind": "draft", "draft_id": "draft-27", "title": "Current title", "body": "Current body"}
        self.raw_target = {"kind": "proposed_draft", "repo": "example/guru-extension", "draft_id": "draft-27"}
        authority = {"kind": "draft", "repo": self.raw_target["repo"], "issue_number": None, "url": None,
                     "state": "draft", "updated_at": None, "body_sha256": review_common.sha(self.source["body"])}
        self.raw_target["source_request_sha256"] = review_common.digest(authority)
        self.target = review_common.normalize_target(self.source, self.raw_target)
        self.transition = json.loads((PACKAGE_ROOT.parent / "guru-review-contract-wording/examples/public-pass-output-2.0.json").read_text())["transition"]
        self.transition.update(mode="standalone", target_locator="draft-27", continuation_id="stage0-current")
        self.transition["clarity"].update(target_sha256="7" * 64, content_sha256="a" * 64)
        self.transition["clarity_result_sha256"] = self.transition["clarity"]["facts_sha256"]
        self.transition["target_disposition"]["disposition_sha256"] = "b" * 64
        self.transition["wording"]["target_content_sha256"] = self.target["content_sha256"]
        self.transition["target_content_sha256"] = self.target["content_sha256"]
        self.transition["wording_facts_sha256"] = self.transition["wording"]["facts_sha256"]
        self.public = {"profile": "proposed_draft", "source_exit": "pass", "mode": "standalone",
                       "target_locator": "draft-27", "continuation_id": "stage0-current"}

    def authoring(self, exit_id="ready", transition=None):
        transition = transition or self.transition
        prerequisites = review_common.normalize_prerequisites(transition, self.target, self.source, PACKAGE_ROOT)
        linked = review_common.linkage(self.target, prerequisites)
        example = json.loads((PACKAGE_ROOT / "examples/issue-review.json").read_text())
        owner = {key: example[key] for key in ("generated_at", "semantic_review", "reason", "affected_evidence")}
        owner.update(mode=self.public["mode"], target=copy.deepcopy(self.raw_target),
                     typed_exit=exit_id, consumer=review_common.CONSUMERS[exit_id])
        semantic = owner["semantic_review"]
        semantic["findings"] = []
        for row in semantic["dimensions"]:
            row.update(status="passed", finding_ids=[])
        if exit_id != "ready":
            semantic["dimensions"][0].update(status="failed", finding_ids=["finding-1"])
            semantic["findings"] = [{"finding_id": "finding-1", "category": "requirement_gap",
                                    "summary": "Current evidence requires the selected reroute.", "blocking": True,
                                    "evidence_refs": ["evidence_linkage"], "affected_hashes": [linked["linkage_sha256"]],
                                    "route_basis": "AI reviewed this exit."}]
        semantic["ai_review_gate"].update(status=review_common.GATES[exit_id],
                                         reviewed_linkage_sha256=linked["linkage_sha256"],
                                         findings_count=len(semantic["findings"]),
                                         scope_conclusion_sha256=review_common.digest(semantic["scope_conclusion"]))
        return owner

    def envelope(self, exit_id="ready", transition=None):
        transition = transition or self.transition
        return {"schema_version": "1.0", "public_input": copy.deepcopy(self.public),
                "transition": copy.deepcopy(transition), "owner_context": {"change_request": copy.deepcopy(self.source)},
                "owner_result": self.authoring(exit_id, transition)}

    def run_command(self, module, envelope, package=PACKAGE_ROOT):
        with mock.patch.object(sys, "stdin", io.StringIO(json.dumps(envelope))):
            return module.run(package, {}, ["--root", str(self.root), "--invocation", "-"])

    def checked(self, envelope):
        envelope["owner_result"] = self.run_command(review_record, envelope)
        checked = self.run_command(review_check, envelope)
        envelope["validation_receipt"] = checked["validation_receipt"]
        return envelope

    def assert_error(self, module, envelope, code):
        with self.assertRaises(CommandError) as error:
            self.run_command(module, envelope)
        self.assertEqual(code, error.exception.code)

    def earlier(self, stage):
        keys = json.loads((SKILLS_ROOT / "consumers/workflow/stage0/transitions" /
                           (stage.replace("_", "-") + ".schema.json")).read_text())["required"]
        value = {key: copy.deepcopy(self.transition[key]) for key in keys if key in self.transition}
        value.update(stage=stage, transition_id=stage + ":example")
        if stage == "context_current":
            value["authority_content_sha256"] = self.target["body_sha256"]
        else:
            value["target_content_sha256"] = value["clarity"]["content_sha256"]
        return value

    def test_ready_preserves_distinct_semantic_content_and_disposition(self):
        envelope = self.checked(self.envelope())
        output = self.run_command(review_invoke, envelope)
        self.assertEqual("ready", output["exit_id"])
        owner = envelope["owner_result"]
        self.assertEqual("2.0", owner["schema_version"])
        self.assertNotEqual(owner["prerequisites"]["clarity"]["content_sha256"], self.target["content_sha256"])
        self.assertEqual(self.transition["target_disposition"], output["transition"]["target_disposition"])
        for value in owner["prerequisites"].values():
            self.assertNotIn("payload_sha256", value)
        self.assertEqual([], list(self.root.iterdir()))

    def test_workflow_and_standalone_same_contract(self):
        for mode in ("workflow", "standalone"):
            self.public["mode"] = self.transition["mode"] = mode
            self.assertEqual(mode, self.run_command(review_invoke, self.checked(self.envelope()))["mode"])

    def test_all_five_exits_and_original_reroute_stages(self):
        for exit_id in review_common.CONSUMERS:
            transition = self.transition
            if exit_id == "clarify_requirements":
                transition = self.earlier("context_current")
            elif exit_id == "review_wording":
                transition = self.earlier("clarity_current")
            with self.subTest(exit_id=exit_id):
                envelope = self.checked(self.envelope(exit_id, transition))
                output = self.run_command(review_invoke, envelope)
                self.assertEqual(exit_id, output["exit_id"])
                if exit_id in {"clarify_requirements", "review_wording"}:
                    self.assertEqual(transition, output["transition"])

    def test_missing_prerequisite_cannot_be_ready(self):
        self.assert_error(review_record, self.envelope("ready", self.earlier("clarity_current")), "schema_mismatch")

    def test_title_and_body_drift_rejected(self):
        for field in ("title", "body"):
            envelope = self.checked(self.envelope())
            envelope.pop("validation_receipt")
            envelope["owner_context"]["change_request"][field] += " updated"
            self.assert_error(review_check, envelope, "stale_identity")

    def test_shape_errors_are_not_live_drift(self):
        for value in (None, {}, {"stage": "readiness_current"}, {"clarity": {}, "wording": {}}, {"exit_id": "blocked"}):
            envelope = self.envelope()
            envelope["transition"] = value
            self.assert_error(review_record, envelope, "schema_mismatch")
        envelope = self.envelope()
        envelope["owner_result"]["prerequisite_payloads"] = {"clarity": {}, "wording": {}}
        self.assert_error(review_record, envelope, "schema_mismatch")

    def test_profile_and_identity_mismatch(self):
        envelope = self.envelope()
        envelope["public_input"]["profile"] = "current_issue"
        self.assert_error(review_record, envelope, "schema_mismatch")
        for field in ("continuation_id", "target_locator", "mode"):
            envelope = self.envelope()
            envelope["transition"][field] = "workflow" if field == "mode" else "different"
            self.assert_error(review_record, envelope, "stale_identity")

    def test_clarity_identities_are_opaque_and_receipt_bound(self):
        envelope = self.envelope()
        for key in ("target_sha256", "content_sha256", "disposition_sha256"):
            envelope["transition"]["clarity"][key] = "8" * 64
        self.transition = envelope["transition"]
        envelope["owner_result"] = self.authoring()
        envelope = self.checked(envelope)
        output = self.run_command(review_invoke, envelope)
        self.assertEqual(envelope["transition"]["clarity"], output["transition"]["clarity"])
        envelope["transition"]["clarity"]["target_sha256"] = "9" * 64
        self.assert_error(review_invoke, envelope, "stale_identity")

    def test_context_body_identity_must_match_current_source(self):
        envelope = self.envelope("clarify_requirements", self.earlier("context_current"))
        envelope["owner_context"]["change_request"]["body"] += " updated"
        self.assert_error(review_record, envelope, "stale_identity")
        envelope = self.envelope("clarify_requirements", self.earlier("context_current"))
        envelope["transition"]["authority_content_sha256"] = "0" * 64
        self.assert_error(review_record, envelope, "stale_identity")

    def test_facts_cross_fields_must_agree(self):
        for field in ("clarity_result_sha256", "wording_facts_sha256", "target_content_sha256"):
            envelope = self.envelope()
            envelope["transition"][field] = "0" * 64
            self.assert_error(review_record, envelope, "schema_mismatch")

    def test_receipt_and_transition_are_exact(self):
        envelope = self.checked(self.envelope())
        for key in ("context_result_sha256",):
            changed = copy.deepcopy(envelope)
            changed["transition"][key] = "0" * 64
            self.assert_error(review_invoke, changed, "stale_identity")
        changed = copy.deepcopy(envelope)
        changed["transition"]["target_disposition"]["disposition_sha256"] = "0" * 64
        self.assert_error(review_invoke, changed, "stale_identity")
        envelope["validation_receipt"]["result_sha256"] = "0" * 64
        self.assert_error(review_invoke, envelope, "stale_identity")

    def test_receipt_allowed_only_final(self):
        envelope = self.checked(self.envelope())
        self.assert_error(review_record, envelope, "schema_mismatch")
        self.assert_error(review_check, envelope, "schema_mismatch")
        envelope.pop("validation_receipt")
        self.assert_error(review_invoke, envelope, "schema_mismatch")

    def test_standalone_request_source_profile(self):
        self.raw_target.update(kind="standalone_request", request_id=self.source["draft_id"], caller_locator="request:local")
        self.raw_target.pop("draft_id")
        self.public["profile"] = "standalone_request"
        self.target = review_common.normalize_target(self.source, self.raw_target)
        self.assertEqual("ready", self.run_command(review_invoke, self.checked(self.envelope()))["exit_id"])

    def test_single_live_read_and_no_serializer_live_calls(self):
        self.source = {"kind": "issue", "repo": "example/guru-extension", "number": 27, "state": "open",
                       "title": "Current title", "body": "Current body", "updated_at": "2026-01-01T00:00:00Z"}
        url = "https://github.com/example/guru-extension/issues/27"
        self.raw_target = {"kind": "existing_issue", "repo": self.source["repo"], "issue_number": 27,
                           "url": url, "updated_at": self.source["updated_at"]}
        self.target = review_common.normalize_target(self.source, self.raw_target)
        self.public.update(profile="current_issue", target_locator=url)
        self.transition["target_locator"] = url
        live = {**self.source, "url": url, "state": "OPEN", "updatedAt": self.source["updated_at"]}
        with mock.patch.object(review_common.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, json.dumps(live), "")) as read:
            self.assertEqual("ready", self.run_command(review_invoke, self.checked(self.envelope()))["exit_id"])
            self.assertEqual(1, read.call_count)

    def test_installed_relative_schema_layout(self):
        skills = self.root / ".trellis/guru-team/skills"
        installed = skills / "packages" / PACKAGE_ROOT.name
        shutil.copytree(PACKAGE_ROOT, installed)
        shutil.copytree(SKILLS_ROOT / "consumers", skills / "consumers")
        envelope = self.envelope()
        envelope["owner_result"] = self.run_command(review_record, envelope, installed)
        checked = self.run_command(review_check, envelope, installed)
        envelope["validation_receipt"] = checked["validation_receipt"]
        self.assertEqual("ready", self.run_command(review_invoke, envelope, installed)["exit_id"])

    def test_retired_arguments_rejected(self):
        for module in (review_record, review_check):
            with self.assertRaises(CommandError) as error:
                module.run(PACKAGE_ROOT, {}, ["--input", "-", "--mode", "workflow"])
            self.assertEqual("invalid_arguments", error.exception.code)


if __name__ == "__main__":
    unittest.main()
