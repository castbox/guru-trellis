"""Current recovery boundary and pinned old schema assets."""
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


class CheckRecoveryContractTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("retirement_flow", PACKAGE / "tests/test_delivery_flow.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.flow = module.DeliveryFlow()
        self.flow.setUp()
        self.addCleanup(self.flow.doCleanups)

    def test_retired_development_input_creates_no_check_or_checkpoint(self):
        public = {"profile": "delivery_initial_check", "mode": "workflow",
                  "task_ref": self.flow.task_ref, "delivery_key": self.flow.key,
                  "source_exit": "implementation_complete", "planning_accepted_result_id": "planning:flow"}
        task_file = self.flow.repo / self.flow.task_ref / "task.json"
        before = task_file.read_bytes()
        result = self.flow.wrapper("guru-check-task", "invoke.sh", "--input",
            self.flow.write("retired-check.json", public), "--owner-result",
            PACKAGE / "examples/phase2-check.json", success=False)
        self.assertEqual("schema_mismatch", result["code"])
        self.assertEqual(before, task_file.read_bytes())
        self.assertIsNone(self.flow.projection.resolve(self.flow.key)["results"]["check"])
        self.assertFalse(list((self.flow.repo / ".trellis/.runtime").glob("**/phase2-check.json")))

    def test_retired_normal_recorder_does_not_write_checkpoint(self):
        result = self.flow.wrapper("guru-check-task", "record-phase2-check.sh", "--task", self.flow.task_ref,
                                  "--input", PACKAGE / "examples/phase2-authoring.json", success=False)
        self.assertEqual("schema_mismatch", result["code"])
        self.assertFalse(list((self.flow.repo / ".trellis/.runtime").glob("**/phase2-check.json")))


if __name__ == "__main__":
    unittest.main()
