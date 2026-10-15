"""Existing public writers and actual query wrappers; provider/review are fixtures."""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("history_public_fixture", PACKAGE / "tests/test_manual_recovery.py")
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class PublicHistoryTests(unittest.TestCase):
    def setUp(self):
        self.source = fixture.ManualRecoveryTests()
        self.source.setUp()
        self.addCleanup(self.source.doCleanups)
        self.flow = self.source.flow
        self.assertEqual("delivered", self.source.invoke()["exit_id"])
        self.query = {"schema_version": "2.0", "task_identity": "flow-task", "repo_ref": "example/repo",
                      "base_ref": "main", "task_ref": self.flow.task_ref}

    def query_result(self, *, success=True):
        return self.flow.wrapper(PACKAGE.name, "discover-task-deliveries.sh", "--input",
                                 self.flow.write("fixed-history.json", self.query), success=success)

    def set_remote_cutoff(self, commit):
        path = self.source.bin / "responses.json"
        values = json.loads(path.read_text())
        values["repos/example/repo/git/ref/heads/main"]["object"]["sha"] = commit
        path.write_text(json.dumps(values))

    def test_recorded_successor_is_validated_then_excluded_from_old_cutoff(self):
        self.set_remote_cutoff(self.source.base)
        before = (self.flow.repo / self.flow.task_ref / "task.json").read_bytes()
        result = self.query_result()
        self.assertEqual(self.source.base, result["cutoff_commit"])
        self.assertEqual([], result["deliveries"])
        self.assertEqual(before, (self.flow.repo / self.flow.task_ref / "task.json").read_bytes())
        calls = [json.loads(line) for line in self.source.calls.read_text().splitlines()]
        self.assertTrue(any("repos/example/repo/commits/" + self.source.merge + "/pulls" in call for call in calls))

    def test_post_cutoff_identity_failure_is_not_silently_excluded(self):
        self.set_remote_cutoff(self.source.base)
        path = self.source.bin / "responses.json"
        values = json.loads(path.read_text())
        values["repos/example/repo/commits/" + self.source.merge + "/pulls"][0]["head"]["sha"] = self.source.base
        path.write_text(json.dumps(values))
        result = self.query_result(success=False)
        self.assertEqual("stale_identity", result["code"])
        self.assertEqual("github.pull_request", result["field_path"])

    def test_recorded_merge_on_unrelated_first_parent_line_fails(self):
        # This is an ordinary selection mismatch: query another existing base
        # commit on the feature line, not a manually altered public fact.
        self.set_remote_cutoff(self.flow.head)
        result = self.query_result(success=False)
        self.assertEqual("history.base_ref", result["field_path"])

    def test_restored_session_missing_merge_uses_scratch_candidate_context(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        clone = Path(temporary.name) / "restored"
        subprocess.run(["git", "clone", "--single-branch", "--branch", "feat/flow", "--no-tags",
                        self.flow.repo.as_uri(), str(clone)], check=True, capture_output=True)
        missing = subprocess.run(["git", "cat-file", "-e", self.source.merge], cwd=clone, capture_output=True)
        self.assertNotEqual(0, missing.returncode)
        # Restore the exact public record emitted by the original writer,
        # without constructing another Delivery or inventing a result.
        shutil.copyfile(self.flow.repo / self.flow.task_ref / "task.json", clone / self.flow.task_ref / "task.json")
        task_before = (clone / self.flow.task_ref / "task.json").read_bytes()
        sys.path.insert(0, str(PACKAGE / "runtime"))
        spec = importlib.util.spec_from_file_location("history_public_owner", PACKAGE / "runtime/history.py")
        history = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(history)
        with patch.dict(os.environ, {"GIT_CONFIG_COUNT": "1",
                 "GIT_CONFIG_KEY_0": "url." + self.flow.repo.as_uri() + ".insteadOf",
                 "GIT_CONFIG_VALUE_0": "https://github.com/example/repo.git"}):
            result = history.discover(clone, PACKAGE, self.query)
            self.set_remote_cutoff(self.source.base)
            successor = history.discover(clone, PACKAGE, self.query)
        self.assertEqual(self.source.merge, result["cutoff_commit"])
        self.assertEqual([self.source.merge], [row["merge_commit_sha"] for row in result["deliveries"]])
        self.assertEqual(self.flow.key, result["deliveries"][0]["delivery_key"])
        self.assertEqual(self.source.base, successor["cutoff_commit"])
        self.assertEqual([], successor["deliveries"])
        self.assertEqual(task_before, (clone / self.flow.task_ref / "task.json").read_bytes())
        self.assertNotEqual(0, subprocess.run(["git", "cat-file", "-e", self.source.merge], cwd=clone, capture_output=True).returncode)


if __name__ == "__main__":
    unittest.main()
