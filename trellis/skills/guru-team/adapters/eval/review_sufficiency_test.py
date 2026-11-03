"""Mechanical collection checks, without grading an Agent's review semantics."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import review_sufficiency as collector
from review_sufficiency_cases import DOMAIN


class CollectionTests(unittest.TestCase):
    def test_real_thread_identity_and_candidate_update_are_carried(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "fixture"
            target.mkdir()
            (target / "domain.py").write_text(DOMAIN)
            calls = []

            def native(argv, **kwargs):
                calls.append(argv)
                if len(calls) > 1:
                    self.assertEqual(argv[argv.index("resume") + 1], "native-thread")
                    self.assertIn('"total": len(rows)', (target / "domain.py").read_text())
                    self.assertTrue((target / "csv_adapter.py").is_file())
                raw = (json.dumps({"type": "thread.started", "thread_id": "native-thread"})
                       + '\n{"type":"turn.completed"}\n').encode()
                return subprocess.CompletedProcess(argv, 0, raw, b"native diagnostic")

            with patch.object(collector, "prepare", return_value=target), patch.object(
                    collector.subprocess, "run", side_effect=native):
                result = collector.collect(root, root / "run", "B", 20, "python3")
            self.assertTrue(result["execution_complete"])
            self.assertEqual(len(calls), 3)
            self.assertNotIn("resume", calls[0])
            self.assertEqual((root / "run/turn-1/stderr.txt").read_bytes(), b"native diagnostic")

    def test_timeout_preserves_first_partial_output_and_stops(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            error = subprocess.TimeoutExpired("native", 1, output=b'{"type":"thread.started","thread_id":"x"}\n',
                                              stderr=b"timeout diagnostic")
            with patch.object(collector, "prepare", return_value=root), patch.object(
                    collector.subprocess, "run", side_effect=error):
                result = collector.collect(root, root / "run", "E", 1, "python3")
            self.assertFalse(result["execution_complete"])
            self.assertEqual(result["turns"][0]["error"], "timeout")
            self.assertEqual((root / "run/turn-1/events.jsonl").read_bytes(), error.stdout)

    def test_completed_event_without_thread_is_not_execution_complete(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            native = subprocess.CompletedProcess([], 0, b'{"type":"turn.completed"}\n', b"")
            with patch.object(collector, "prepare", return_value=root), patch.object(
                    collector.subprocess, "run", return_value=native):
                result = collector.collect(root, root / "run", "E", 1, "python3")
            self.assertFalse(result["execution_complete"])


if __name__ == "__main__":
    unittest.main()
