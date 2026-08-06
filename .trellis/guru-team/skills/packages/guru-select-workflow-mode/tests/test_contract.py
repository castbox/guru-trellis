from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
PACKAGE = ROOT / "trellis/skills/guru-team/packages/guru-select-workflow-mode"


class WorkflowModeContractTest(unittest.TestCase):
    def _selection(self, exit_id: str) -> dict:
        return {
            "schema_version": "1.0",
            "typed_exit": exit_id,
            "mode": "workflow",
            "selection": exit_id,
            "continuation_id": "turn-1",
        }

    def test_explicit_task_free_selection_is_minimal_and_unambiguous(self) -> None:
        result = json.loads((PACKAGE / "examples/workflow-mode-selection.json").read_text())
        self.assertEqual(result["typed_exit"], "task_free")
        self.assertEqual(result["selection"], "task_free")
        self.assertNotIn("confirmation", result)

    def test_selector_behavior_matrix_is_single_choice_and_fail_closed(self) -> None:
        self.assertEqual(self._selection("task_free")["typed_exit"], "task_free")
        self.assertEqual(self._selection("standard_intake")["typed_exit"], "standard_intake")
        self.assertEqual(self._selection("standard_intake")["selection"], "standard_intake")
        self.assertEqual(self._selection("task_free")["continuation_id"], "turn-1")

    def test_semantic_eval_matrix_covers_current_behavior_contract(self) -> None:
        corpus = json.loads((PACKAGE / "evals/evals.json").read_text())
        self.assertEqual(
            {case["id"] for case in corpus["evals"]},
            {
                "explicit-task-free",
                "implicit-confirmed",
                "implicit-refused",
                "ordinary-issue-request",
                "unrelated-dirty-preserved",
                "same-scope-retry",
                "selection-unavailable",
            },
        )
        self.assertEqual(
            {case["expected_exit"] for case in corpus["evals"]},
            {"standard_intake", "task_free", "blocked"},
        )
        self.assertTrue(all(case["prompt"].strip() for case in corpus["evals"]))
        self.assertTrue(all(case["files"] for case in corpus["evals"]))
        for case in corpus["evals"]:
            scenario_path = PACKAGE / case["files"][-1]
            scenario = json.loads(scenario_path.read_text())
            self.assertTrue(scenario["scenario"].strip(), case["id"])

    def test_blocked_owner_result_does_not_claim_a_selection(self) -> None:
        schema = json.loads((PACKAGE / "schemas/workflow-mode-selection.schema.json").read_text())
        blocked = next(
            branch for branch in schema["oneOf"]
            if branch["properties"]["typed_exit"].get("const") == "blocked"
        )
        self.assertNotIn("selection", blocked["required"])
        self.assertNotIn("selection", blocked["properties"])

    def test_task_free_contract_excludes_side_effect_authority(self) -> None:
        text = (PACKAGE / "SKILL.md").read_text()
        for forbidden in ("commit", "push", "PR", "merge", "tag", "release", "installation", "cleanup"):
            self.assertIn(forbidden, text)

    def test_public_outputs_have_only_typed_exit(self) -> None:
        for name, exit_id in (("public-standard-intake-output.json", "standard_intake"), ("public-task-free-output.json", "task_free"), ("public-blocked-output.json", "blocked")):
            payload = json.loads((PACKAGE / "examples" / name).read_text())
            self.assertEqual(payload, {"exit_id": exit_id})

    def test_no_legacy_task_free_contract_remains(self) -> None:
        text = (PACKAGE / "SKILL.md").read_text()
        self.assertNotIn("skip-flow", text)
        self.assertNotIn("legacy", text.lower())


if __name__ == "__main__":
    unittest.main()
