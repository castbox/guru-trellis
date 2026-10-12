import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
from runtime.io import CommandError

spec = importlib.util.spec_from_file_location("author_plan_invocation", PACKAGE / "runtime/invoke.py")
owner_runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner_runtime)


def load(name):
    return json.loads((PACKAGE / "examples" / name).read_text())


class RuntimeTest(unittest.TestCase):
    def test_first_requirements_handoff_needs_no_future_design_or_contribution(self):
        public = load("public-initial-review-input.json")
        owner = load("semantic-result.json")
        with tempfile.TemporaryDirectory() as temp:
            task = Path(temp)
            (task / "prd.md").write_text("Current source requirements")
            with patch.object(owner_runtime, "_task", return_value=task):
                self.assertEqual(owner["output"], owner_runtime.execute(PACKAGE, task, public, owner))
            self.assertEqual(["prd.md"], [p.name for p in task.iterdir()])

    def test_normal_revision_mismatch_requires_the_current_owner_round(self):
        public = load("public-wording-reentry-input.json")
        owner = load("semantic-result.json")
        with self.assertRaises(CommandError) as caught:
            owner_runtime.execute(PACKAGE, PACKAGE, public, owner)
        self.assertEqual(caught.exception.code, "stale_identity")

    def test_plan_handoff_validates_official_context_and_is_read_only(self):
        public = load("public-solution-planning-input.json")
        owner = {"public_input":public,"output":load("public-plan-ready-output.json"),
                 "ai_review_gate":{"status":"passed","summary":"Current owner reviewed solution writing."}}
        with tempfile.TemporaryDirectory() as temp:
            task = Path(temp)
            for name in ("prd.md", "design.md", "implement.md"):
                (task / name).write_text("Current planning")
            for name in ("implement.jsonl", "check.jsonl"):
                (task / name).write_text(json.dumps({"file":".trellis/spec/workflow/index.md","reason":"Current workflow contract"})+'\n')
            before = {p.name:p.read_bytes() for p in task.iterdir()}
            with patch.object(owner_runtime, "_task", return_value=task):
                self.assertEqual(owner["output"], owner_runtime.execute(PACKAGE, task, public, owner))
                (task / "check.jsonl").write_text('{}\n')
                with self.assertRaises(CommandError):
                    owner_runtime.execute(PACKAGE, task, public, owner)
            self.assertEqual(before["prd.md"], (task / "prd.md").read_bytes())
            self.assertEqual(set(before), {p.name for p in task.iterdir()})


if __name__ == "__main__":
    unittest.main()
