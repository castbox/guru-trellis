"""Exercise real Git prerequisites for the temporary Agent installation."""
import os
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from windows_codex_session import REQUEST_NAME, prepare_fixture, run_session


class FixtureTest(unittest.TestCase):
    def test_unborn_repo_gets_empty_head_without_consuming_staged_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "中文 clean install"
            root.mkdir()
            output = Path(temporary) / "output"
            output.mkdir()
            subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
            (root / "installed.txt").write_text("installed bytes", encoding="utf-8")
            subprocess.run(["git", "add", "installed.txt"], cwd=root, check=True)
            report = {"commands": []}
            prepare_fixture(root, dict(os.environ), output, report)
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root)
            self.assertEqual(subprocess.check_output(["git", "ls-tree", "HEAD"], cwd=root), b"")
            self.assertEqual(subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=root),
                             b"installed.txt\n")
            self.assertEqual((root / REQUEST_NAME).read_bytes(), (output / "request-draft.md").read_bytes())
            self.assertEqual(report["commands"][-1]["returncode"], 0)
            self.assertEqual(subprocess.run(["git", "config", "--local", "--get", "user.name"],
                                            cwd=root, capture_output=True).returncode, 1)
            prepare_fixture(root, dict(os.environ), output, report)
            self.assertEqual(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root), head)

    def test_git_preparation_failure_is_recorded_and_stops(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "not a repo"
            root.mkdir()
            output = Path(temporary) / "output"
            output.mkdir()
            report = {"commands": []}
            with self.assertRaisesRegex(RuntimeError, "initial commit failed"):
                prepare_fixture(root, dict(os.environ), output, report)
            self.assertNotEqual(report["commands"][-1]["returncode"], 0)
            self.assertTrue((output / report["commands"][-1]["stderr"]).is_file())


class SessionExecutionTest(unittest.TestCase):
    def test_resume_uses_emitted_identity_and_preserves_nonzero_result(self):
        script = """import json, sys
print(json.dumps({'type': 'thread.started', 'thread_id': 'actual-fixture-thread'}))
print(json.dumps({'type': 'fixture', 'argv': sys.argv[1:], 'input': sys.stdin.read()}))
if 'resume' in sys.argv:
    sys.exit(7)
"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            report = {}
            result = run_session([sys.executable, "-c", script], ("first", "second"),
                                 root, dict(os.environ), root, report)
            self.assertEqual(result, 7)
            self.assertEqual(report["session"]["status"], "session_failed")
            actual = [json.loads(line) for line in (root / "session-resume.jsonl").read_text().splitlines()]
            self.assertEqual(actual[1]["argv"], ["resume", "actual-fixture-thread", "-"])
            self.assertEqual(actual[1]["input"], "second")

    def test_second_process_uses_remaining_budget_and_retains_timeout_output(self):
        script = """import json, sys, time
print(json.dumps({'type': 'thread.started', 'thread_id': 'actual-fixture-thread'}), flush=True)
time.sleep(5 if 'resume' in sys.argv else 0.05)
"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            report = {}
            with patch("windows_codex_session.SESSION_TIMEOUT", 0.8):
                with self.assertRaises(subprocess.TimeoutExpired):
                    run_session([sys.executable, "-c", script], ("first", "second"),
                                root, dict(os.environ), root, report)
            rounds = report["session"]["rounds"]
            self.assertEqual(len(rounds), 2)
            self.assertLess(rounds[1]["remaining_seconds"], rounds[0]["remaining_seconds"])
            self.assertEqual(rounds[1]["status"], "timed_out")
            self.assertIn("returncode", rounds[1])
            self.assertIn("thread.started", (root / rounds[1]["events"]).read_text())


if __name__ == "__main__":
    unittest.main()
