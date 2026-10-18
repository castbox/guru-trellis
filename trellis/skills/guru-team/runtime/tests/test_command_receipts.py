from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runtime import command
from runtime.io import CommandError, project_intermediate_receipt
from runtime.schema import validate_json

SKILLS = Path(__file__).resolve().parents[2]
PACKAGES = SKILLS / "packages"


class CommandReceiptTests(unittest.TestCase):
    def dispatch(self, skill, command_id, original):
        output = StringIO()
        entrypoint = SimpleNamespace(run=lambda *args: original)
        with patch.object(command, "_load_entrypoint", return_value=entrypoint), redirect_stdout(output):
            result = command.main(PACKAGES / skill, [command_id])
        self.assertEqual(result, 0, output.getvalue())
        return json.loads(output.getvalue())

    def test_intermediate_owner_checker_and_typed_shaped_atomic_results_are_transport_only(self):
        # Dispatcher unit evidence: entrypoint logic/semantic judgment is outside
        # this layer. Both real typed-shaped atomic metadata and closed owner
        # shapes must remain payload, irrespective of their status/exit fields.
        cases = [
            ("guru-discover-change-context", "record-context-discovery", {"schema_version": "1.0", "typed_exit": "context_ready"}),
            ("guru-review-task-delivery", "check-task-delivery-review", {"status": "passed", "typed_exit": "ready"}),
            ("guru-create-task", "create-task", {"exit_id": "created", "task_id": "sample"}),
            ("guru-rebind-task-branch", "recover-task-branch-result", {"exit_id": "rebound"}),
            ("guru-sync-base", "check-base-sync", {"status": "validated"}),
        ]
        metadata = json.loads((PACKAGES / "guru-rebind-task-branch/commands.json").read_text())
        cases[3] = (cases[3][0], next(c["id"] for c in metadata["commands"] if c["id"].startswith("recover-")), cases[3][2])
        for skill, command_id, original in cases:
            with self.subTest(command=command_id):
                output = self.dispatch(skill, command_id, original)
                validate_json(output, SKILLS / "schemas/intermediate-command-receipt-1.0.schema.json", "stdout")
                self.assertEqual(output["formal_exit"], False)
                self.assertNotIn("exit_id", output)
                self.assertEqual(project_intermediate_receipt(output, SKILLS / "schemas"), original)

    def test_formal_positive_and_nonpass_outputs_remain_exact(self):
        for original in ({"exit_id": "pass", "profile": "planning_artifacts", "continuation_id": "test"},
                         {"exit_id": "blocked", "reason": "current wording needs revision"}):
            self.assertEqual(self.dispatch("guru-review-contract-wording", "invoke-guru-review-contract-wording", original), original)

    def test_same_owner_projection_requires_current_receipt_not_formal_or_old_stdout(self):
        for payload in ({"status": "passed"}, {"exit_id": "approved"},
                        {"schema_version": "1.0", "formal_exit": True, "result": {}}):
            with self.subTest(payload=payload), self.assertRaises(CommandError):
                project_intermediate_receipt(payload, SKILLS / "schemas")


if __name__ == "__main__":
    unittest.main()
