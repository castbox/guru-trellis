from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location("decision_dialogue", Path(__file__).with_name("decision_dialogue.py"))
dialogue = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dialogue)


def events(thread="actual-thread", *, completed=True):
    rows = [{"type": "thread.started", "thread_id": thread}]
    if completed:
        rows.append({"type": "turn.completed", "usage": {}})
    return ("\n".join(json.dumps(row) for row in rows) + "\n").encode()


class DecisionDialogueTests(unittest.TestCase):
    def test_future_reply_is_withheld_and_actual_thread_is_resumed(self):
        case = {"id": "split", "repository_facts": "Repository facts only.",
                "turns": ["Initial request.", "FUTURE_REPLY_ONLY"],
                "review_focus": "HIDDEN_EXPECTATION"}
        observed = []

        def run(args, **kwargs):
            fixture = kwargs["cwd"]
            fixture_text = "\n".join(path.read_text() for path in fixture.rglob("*") if path.is_file())
            self.assertNotIn("FUTURE_REPLY_ONLY", fixture_text)
            self.assertNotIn("HIDDEN_EXPECTATION", fixture_text)
            observed.append((args, kwargs["input"]))
            return subprocess.CompletedProcess(args, 0, events(), b"")

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result"
            report = dialogue.collect(case, dialogue.REPO, output, run=run)
            self.assertTrue(report["execution_complete"])
            self.assertEqual(observed[0][1], b"Initial request.")
            self.assertEqual(observed[1][1], b"FUTURE_REPLY_ONLY")
            resume = observed[1][0].index("resume")
            self.assertEqual(observed[1][0][resume:resume + 2], ["resume", "actual-thread"])
            self.assertNotIn("--last", observed[1][0])
            self.assertNotIn("semantic_pass", report)
            self.assertEqual((output / "turn-1/events.jsonl").read_bytes(), events())

    def test_nonzero_or_missing_completion_does_not_send_later_reply(self):
        case = {"id": "failed", "repository_facts": "facts", "turns": ["first", "later"]}
        for code, stdout in ((3, events()), (0, events(completed=False)), (0, b"not-json")):
            with self.subTest(code=code, stdout=stdout), tempfile.TemporaryDirectory() as directory:
                calls = []

                def run(args, **kwargs):
                    calls.append(kwargs["input"])
                    return subprocess.CompletedProcess(args, code, stdout, b"original diagnostic")

                output = Path(directory) / "result"
                report = dialogue.collect(case, dialogue.REPO, output, run=run)
                self.assertFalse(report["execution_complete"])
                self.assertEqual(calls, [b"first"])
                self.assertEqual((output / "turn-1/stderr.txt").read_bytes(), b"original diagnostic")

    def test_timeout_keeps_partial_output_and_stops(self):
        case = {"id": "timeout", "repository_facts": "facts", "turns": ["first", "later"]}

        def run(args, **kwargs):
            raise subprocess.TimeoutExpired(args, kwargs["timeout"], output=b"partial", stderr=b"timeout diagnostic")

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result"
            report = dialogue.collect(case, dialogue.REPO, output, run=run)
            self.assertFalse(report["execution_complete"])
            self.assertEqual(len(report["turns"]), 1)
            self.assertEqual(report["turns"][0]["error"], "timeout")
            self.assertEqual((output / "turn-1/events.jsonl").read_bytes(), b"partial")
            self.assertIsNone(report["turns"][0]["returncode"])

    def test_resumed_identity_change_is_not_complete(self):
        case = {"id": "mismatch", "repository_facts": "facts", "turns": ["first", "second"]}
        calls = []

        def run(args, **kwargs):
            calls.append(args)
            return subprocess.CompletedProcess(args, 0, events("one" if len(calls) == 1 else "two"), b"")

        with tempfile.TemporaryDirectory() as directory:
            report = dialogue.collect(case, dialogue.REPO, Path(directory) / "result", run=run)
            self.assertFalse(report["execution_complete"])
            self.assertEqual(report["turns"][1]["error"], "resumed_thread_mismatch")

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            marker = output / "keep"
            marker.write_text("existing result")
            with self.assertRaises(FileExistsError):
                dialogue.collect({"id": "existing", "turns": []}, dialogue.REPO, output)
            self.assertEqual(marker.read_text(), "existing result")

    def test_trial_disables_hooks_apps_and_explicit_mcp_without_model_override(self):
        case = {"id": "configuration", "repository_facts": "facts", "turns": ["first"]}
        captured = []

        def run(args, **kwargs):
            captured.append(args)
            return subprocess.CompletedProcess(args, 0, events(), b"")

        with tempfile.TemporaryDirectory() as directory:
            dialogue.collect(case, dialogue.REPO, Path(directory) / "result",
                             disable_mcp=("example",), run=run)
        args = captured[0]
        self.assertIn("--no-daemon", args)
        self.assertIn("mcp_servers.example.enabled=false", args)
        for feature in ("hooks", "apps", "memories"):
            position = args.index(feature)
            self.assertEqual(args[position - 1], "--disable")
        self.assertNotIn("--model", args)
        self.assertNotIn("--ignore-user-config", args)


if __name__ == "__main__":
    unittest.main()
