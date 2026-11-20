from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from runtime.schema import validate_json


SKILLS = Path(__file__).resolve().parents[3]
PACKAGES = SKILLS / "packages"
OWNERS = {
    "requirements": PACKAGES / "guru-clarify-requirements",
    "readiness": PACKAGES / "guru-review-change-request",
}
GH_COMMAND = [
    "issue", "view", "17", "--repo", "example/project", "--json",
    "number,url,state,title,body,updatedAt,comments",
]


class StandaloneIssueReviewTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.snapshot_path = self.root / "snapshot.json"
        self.calls_path = self.root / "calls.jsonl"
        self.snapshot = {
            "number": 17,
            "url": "https://github.com/example/project/issues/17",
            "state": "OPEN",
            "title": "Write CSV output to stdout",
            "body": "Emit the selected rows and verify the documented invocation.",
            "updatedAt": "2026-11-01T08:12:00Z",
            "comments": [{"id": "reporter-comment", "body": "Use the named columns."}],
        }
        self.write_live(self.snapshot)
        gh = self.root / "gh"
        gh.write_text(
            "#!" + sys.executable + "\n"
            "import json, os, sys\n"
            "from pathlib import Path\n"
            "with open(os.environ['FIXTURE_CALLS'], 'a') as log:\n"
            "    log.write(json.dumps(sys.argv[1:]) + '\\n')\n"
            "print(Path(os.environ['FIXTURE_SNAPSHOT']).read_text())\n",
        )
        gh.chmod(0o755)
        self.env = {**os.environ,
                    "PATH": str(self.root) + os.pathsep + os.environ["PATH"],
                    "FIXTURE_CALLS": str(self.calls_path),
                    "FIXTURE_SNAPSHOT": str(self.snapshot_path)}

    def write_live(self, snapshot):
        self.snapshot_path.write_text(json.dumps(snapshot))

    def invocation(self, purpose):
        return {
            "schema_version": "1.0",
            "public_input": {
                "profile": f"standalone_issue_{purpose}",
                "mode": "standalone",
                "issue": {"repo_ref": "example/project", "number": 17},
            },
            "owner_context": {"issue_snapshot": self.snapshot},
            "owner_result": {"typed_exit": "issue_reviewed", "report": {
                "coverage": ["Issue body and reporter's discussion."],
                "conclusion": "The issue states a goal. Column order remains unclear.",
                "findings": [],
                "open_items": ["Identify the required column order."],
            }},
        }

    def invoke(self, purpose, envelope, expected_returncode=0):
        owner = OWNERS[purpose]
        result = subprocess.run(
            [str(owner / "scripts/invoke.sh"), "--invocation", "-", "--json"],
            input=json.dumps(envelope), text=True, capture_output=True,
            cwd=self.root, env=self.env,
        )
        self.assertEqual(result.returncode, expected_returncode, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_current_report_reaches_the_read_only_response(self):
        for purpose, owner in OWNERS.items():
            with self.subTest(purpose=purpose):
                envelope = self.invocation(purpose)
                out = self.invoke(purpose, envelope)
                self.assertEqual(out, {"exit_id": "issue_reviewed",
                                       "report": envelope["owner_result"]["report"]})
                interface = json.loads((owner / "interface.json").read_text())
                consumer = next(
                    row for row in interface["public_contracts"]["consumer_inputs"]
                    if row["id"] == "issue_review_response"
                )
                self.assertEqual(consumer["consumer"], {"kind": "stop", "id": "issue-review-response"})
                validate_json(out, SKILLS / consumer["contract"]["path"], "response")

        calls = [json.loads(line) for line in self.calls_path.read_text().splitlines()]
        self.assertEqual(calls, [GH_COMMAND, GH_COMMAND])

    def test_discussion_edit_or_body_edit_requires_current_reassessment(self):
        for purpose, changed in [("requirements", "comments"), ("readiness", "body")]:
            with self.subTest(purpose=purpose):
                live = copy.deepcopy(self.snapshot)
                if changed == "comments":
                    live["comments"][0]["body"] = "The default column order is unspecified."
                else:
                    live["body"] += "\nThe scope changed."
                self.write_live(live)
                envelope = self.invocation(purpose)
                detail = self.invoke(purpose, envelope, 3)
                self.assertEqual(detail["code"], "stale_identity")
                self.assertEqual(detail["field_path"], "owner_context.issue_snapshot")
                envelope["owner_context"]["issue_snapshot"] = live
                envelope["owner_result"]["report"]["conclusion"] = "The revised issue needs a follow-up."
                self.assertEqual(self.invoke(purpose, envelope)["exit_id"], "issue_reviewed")

    def test_unavailable_target_can_return_blocked_without_a_provider_call(self):
        envelope = self.invocation("readiness")
        envelope["owner_context"] = {}
        envelope["owner_result"] = {"typed_exit": "blocked"}
        self.assertEqual(self.invoke("readiness", envelope), {"exit_id": "blocked"})
        self.assertFalse(self.calls_path.exists())
