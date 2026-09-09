"""Unit coverage of public authoring input, not predecessor payload reconstruction."""
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

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
for path in (SKILLS, PACKAGE / "runtime"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import check
import common
import execute
import plan_input
import record
from runtime.command import main
from runtime.io import CommandError


class RecordAuthoringTest(unittest.TestCase):
    def setUp(self):
        self.transition = json.loads((SKILLS / "packages/guru-review-change-request/examples/public-ready-output-3.0.json").read_text())["transition"]
        self.authoring = json.loads((PACKAGE / "examples/workspace-authoring.json").read_text())
        self.envelope = {"schema_version": "1.0", "transition": self.transition, "authoring": self.authoring}

    def call_record(self, envelope=None, package=PACKAGE):
        envelope = self.envelope if envelope is None else envelope
        with mock.patch("sys.stdin", io.StringIO(json.dumps(envelope))), mock.patch.object(common, "git", return_value=subprocess.CompletedProcess([], 0, self.transition["base"]["decision_head"], "")) as git:
            result = record.run(package, {}, ["--root", str(PACKAGE), "--invocation", "-"])
        git.assert_called_once_with(PACKAGE, "rev-parse", "HEAD")
        return result

    def test_public_authoring_returns_valid_plan_and_preserves_decisions(self):
        original = copy.deepcopy(self.envelope)
        plan = self.call_record()
        self.assertEqual(original, self.envelope)
        common.validate(PACKAGE, plan, "task-workspace-plan.schema.json")
        for key in ("naming", "assignee", "side_effects"):
            self.assertEqual(self.authoring[key], plan[key])
        self.assertEqual(self.authoring["ai_review_gate"], {key: value for key, value in plan["ai_review_gate"].items() if key != "reviewed_plan_sha256"})
        self.assertEqual(self.authoring["scope"], {key: value for key, value in plan["scope"].items() if key != "scope_sha256"})
        self.assertNotIn("content_sha256", plan["target"])
        self.assertEqual(self.transition["continuation_id"], plan["invocation"]["resume_identity"])
        self.assertEqual(common.digest(self.transition["clarity"]), plan["prerequisites"]["clarity"]["payload_sha256"])
        self.assertEqual(common.digest(common.reviewable(plan)), plan["ai_review_gate"]["reviewed_plan_sha256"])
        self.assertEqual(common.plan_digest(plan), plan["freshness"]["plan_sha256"])

    def test_fixed_clock_is_deterministic_and_gate_status_is_not_inferred(self):
        for status in ("passed", "blocked", "reroute"):
            self.authoring["ai_review_gate"]["status"] = status
            with mock.patch.object(plan_input, "now", return_value="2026-09-09T00:00:00Z"):
                first, second = self.call_record(), self.call_record()
            self.assertEqual(first, second)
            self.assertEqual(status, first["ai_review_gate"]["status"])

    def test_full_plan_envelope_compatibility(self):
        plan = self.call_record()
        self.assertEqual(plan, self.call_record({"schema_version": "1.0", "transition": self.transition, "plan": plan}))

    def test_distinct_public_disposition_identities_are_preserved(self):
        # Clarification publishes content_identity and target_disposition digests
        # from different owner fields; they are not aliases of each other.
        disposition = common.digest({"disposition": "keep_current_open_issue"})
        self.transition["target_disposition"]["disposition_sha256"] = disposition
        self.assertNotEqual(disposition, self.transition["clarity"]["disposition_sha256"])
        plan = self.call_record()
        self.assertEqual(disposition, plan["target"]["disposition_sha256"])
        self.assertEqual(common.digest(self.transition["clarity"]), plan["prerequisites"]["clarity"]["payload_sha256"])

    def test_required_authoring_field_diagnostic(self):
        del self.authoring["naming"]["branch_name"]
        with self.assertRaises(CommandError) as caught:
            self.call_record()
        self.assertEqual("invocation.authoring.naming.branch_name", caught.exception.field_path)

    def test_extra_and_wrong_type_fields_have_exact_paths(self):
        self.authoring["assignee"]["login"] = 12
        with self.assertRaises(CommandError) as caught:
            self.call_record()
        self.assertEqual("invocation.authoring.assignee.login", caught.exception.field_path)
        self.authoring["assignee"]["login"] = "example-user"
        self.authoring["unexpected"] = True
        with self.assertRaises(CommandError) as caught:
            self.call_record()
        self.assertEqual("invocation.authoring.unexpected", caught.exception.field_path)

    def test_actual_consumer_schema_is_loaded_in_installed_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            skills = Path(directory) / ".trellis/guru-team/skills"
            package = skills / "packages/guru-create-task-workspace"
            shutil.copytree(PACKAGE / "schemas", package / "schemas")
            consumer = Path("consumers/workflow/stage0/transitions/readiness-current.schema.json")
            (skills / consumer).parent.mkdir(parents=True)
            shutil.copyfile(SKILLS / consumer, skills / consumer)
            self.call_record(package=package)
            del self.transition["readiness"]["payload_sha256"]
            with self.assertRaises(CommandError) as caught:
                self.call_record(package=package)
            self.assertEqual("invocation.transition.readiness.payload_sha256", caught.exception.field_path)

    def test_scope_mismatch_does_not_rewrite_ai_decision(self):
        self.authoring["scope"]["close"] = []
        with self.assertRaises(CommandError) as caught:
            self.call_record()
        self.assertEqual("invocation.authoring.scope.close", caught.exception.field_path)
        self.assertEqual([], self.authoring["scope"]["close"])

    def test_draft_is_explicitly_compatibility_only(self):
        self.transition["target"] = {
            "kind": "proposed_draft", "repo": "example/repo", "draft_id": "draft-example",
            "source_request_sha256": self.transition["target"]["body_sha256"],
            **{key: self.transition["target"][key] for key in ("title_sha256", "body_sha256", "identity_sha256", "content_sha256")},
        }
        with self.assertRaises(CommandError) as caught:
            self.call_record()
        self.assertEqual("invocation.transition.target.kind", caught.exception.field_path)

    def test_bare_plan_and_unrecorded_authoring_fail_before_execute(self):
        plan = self.call_record()
        for envelope in (plan, self.envelope):
            with mock.patch("sys.stdin", io.StringIO(json.dumps(envelope))), mock.patch.object(execute, "mutation_boundary_current") as boundary:
                with self.assertRaises(CommandError) as caught:
                    execute.run(PACKAGE, {}, ["--root", str(PACKAGE), "--invocation", "-"])
            self.assertEqual("invocation.plan", caught.exception.field_path)
            boundary.assert_not_called()

    def test_missing_checker_result_and_plan_fields(self):
        plan = self.call_record()
        with mock.patch("sys.stdin", io.StringIO(json.dumps({"plan": plan}))):
            with self.assertRaises(CommandError) as caught:
                check.run(PACKAGE, {}, ["--root", str(PACKAGE), "--invocation", "-"])
        self.assertEqual("invocation.result", caught.exception.field_path)
        del plan["naming"]["branch_name"]
        with self.assertRaises(CommandError) as caught:
            self.call_record({"plan": plan})
        self.assertEqual("invocation.plan.naming.branch_name", caught.exception.field_path)

    def test_record_command_dispatch_accepts_authoring(self):
        output = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO(json.dumps(self.envelope))), mock.patch("sys.stdout", output), mock.patch.object(common, "git", return_value=subprocess.CompletedProcess([], 0, self.transition["base"]["decision_head"], "")):
            code = main(PACKAGE, ["record-task-workspace-plan", "--root", str(PACKAGE), "--invocation", "-"])
        self.assertEqual(0, code, output.getvalue())
        self.assertEqual("guru-create-task-workspace", json.loads(output.getvalue())["skill_id"])


if __name__ == "__main__":
    unittest.main()
