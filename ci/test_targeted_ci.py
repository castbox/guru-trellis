"""Integration checks use real Git checkouts and native unittest subprocesses."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import targeted_ci as ci


class DriverIntegrationTest(unittest.TestCase):
    def git(self, root, *args):
        return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.STDOUT).decode().strip()

    def test_independent_commits_continue_and_preserve_raw_results(self):
        with tempfile.TemporaryDirectory(prefix="Guru CI space ") as temporary:
            root = Path(temporary)
            repo = root / "source"
            repo.mkdir()
            self.git(repo, "init")
            self.git(repo, "config", "user.email", "ci@example.invalid")
            self.git(repo, "config", "user.name", "CI fixture")
            tests = repo / ci.TEST_ROOT
            tests.mkdir(parents=True)
            lock = repo / "trellis/skills/guru-team/runtime/requirements.lock"
            lock.parent.mkdir(parents=True)
            lock.write_text("", encoding="utf-8")
            test = tests / "test_behavior.py"
            test.write_text("import unittest\nclass Behavior(unittest.TestCase):\n def test_value(self):\n  self.assertEqual(1, 2, 'baseline value')\n", encoding="utf-8")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-m", "baseline")
            baseline = self.git(repo, "rev-parse", "HEAD")
            test.write_text(test.read_text().replace("assertEqual(1, 2", "assertEqual(2, 2"), encoding="utf-8")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-m", "candidate")
            candidate = self.git(repo, "rev-parse", "HEAD")
            output = root / "diagnostics"
            output.mkdir()
            report = {"driver_sha": "integration-driver", "targets": []}
            # This fixture proves tests/continuation only. Missing Bash explicitly
            # leaves installation incomplete; it must never become a passing job.
            ci.execute_targets(report, str(repo), [("baseline", baseline), ("candidate", candidate)],
                               root / "work", output, ["test_behavior.py"], None)
            first, second = report["targets"]
            self.assertEqual([row["sha"] for row in report["targets"]], [baseline, candidate])
            self.assertNotEqual(first["workspace"], second["workspace"])
            self.assertEqual(first["tests"]["failures"], 1)
            self.assertEqual(second["tests"]["failures"], 0)
            self.assertEqual(first["tests"]["outcomes"][0]["id"], "test_behavior.Behavior.test_value")
            codes = [next(step["returncode"] for step in row["steps"] if step["stage"] == "tests")
                     for row in report["targets"]]
            self.assertEqual(codes, [1, 0])
            summary = ci.summarize(report, "test_behavior.Behavior.test_value", "1 != 2 : baseline value")
            self.assertEqual(report["returncode"], 1)
            self.assertFalse(report["comparison"]["baseline_matched"])
            self.assertIn(candidate, summary)
            saved = json.loads((output / "candidate/result.json").read_text())
            self.assertEqual(saved["tests"]["tests_run"], 1)
            self.assertIn("Bash unavailable", saved["execution_error"])
            self.assertEqual(self.git(repo, "rev-parse", "HEAD"), candidate)

    def test_only_exact_assertion_can_exempt_baseline(self):
        baseline = {"role": "baseline", "status": "failed", "steps": [
            {"stage": "tests", "category": "tests", "returncode": 1, "log": "tests.log"}],
            "tests": {"tests_run": 1, "outcomes": [
                {"id": "case.test", "kind": "failure", "message": "specific assertion"}]}}
        candidate = {"role": "candidate", "status": "passed", "steps": []}
        report = {"driver_sha": "driver", "targets": [baseline, candidate]}
        ci.summarize(report, "case.test", "specific assertion")
        self.assertTrue(report["comparison"]["established"])
        self.assertEqual(report["returncode"], 0)
        baseline["tests"]["outcomes"][0]["kind"] = "error"
        ci.summarize(report, "case.test", "specific assertion")
        self.assertFalse(report["comparison"]["established"])
        self.assertEqual(report["returncode"], 1)
        baseline["tests"]["outcomes"][0]["kind"] = "failure"
        candidate["status"] = "failed"
        ci.summarize(report, "case.test", "specific assertion")
        self.assertFalse(report["comparison"]["established"])
        self.assertEqual(report["returncode"], 1)


if __name__ == "__main__":
    unittest.main()
