from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / "trellis/skills/guru-team"
PACKAGES = SKILLS / "packages"
FIXTURE = Path(__file__).parent / "fixtures/closeout-118-sanitized.json"
WORKFLOW = REPO / "trellis/workflows/guru-team/workflow.md"

HAPPY_PATHS = {
    "guru-create-task-commit": {
        "commands": [
            "prepare-task-commit",
            "invoke-guru-create-task-commit-happy-path-v1",
        ],
        "legacy": [
            "prepare-task-commit",
            "check-commit-messages",
            "create-task-commit",
            "invoke-guru-create-task-commit",
        ],
        "wrapper": "scripts/invoke-happy-path-v1.sh",
        "public_invocation_switch": False,
    },
    "guru-review-task-publication": {
        "commands": ["review-task-publication"],
        "legacy": [
            "record-task-publication-review",
            "check-task-publication-review",
            "invoke-guru-review-task-publication",
        ],
        "wrapper": "scripts/review-task-publication.sh",
        "public_invocation_switch": True,
    },
    "guru-finalize-task": {
        "commands": ["finalize-task-happy-path"],
        "legacy": [
            "preview-finalization",
            "record-finalization-gate",
            "check-finalization-gate",
            "execute-finalization-transition",
            "invoke-guru-finalize-task",
        ],
        "wrapper": "scripts/finalize-task-happy-path.sh",
        "public_invocation_switch": True,
    },
    "guru-merge-task-pr": {
        "commands": ["complete-task-pr-merge"],
        "legacy": [
            "record-task-pr-merge",
            "check-task-pr-merge",
            "execute-task-pr-merge",
            "invoke-task-pr-merge",
        ],
        "wrapper": "scripts/complete-task-pr-merge.sh",
        "public_invocation_switch": True,
    },
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain one JSON object")
    return value


class CloseoutHappyPathIntegrationTests(unittest.TestCase):
    def test_each_stage_has_one_recommended_public_wrapper(self) -> None:
        for skill_id, expected in HAPPY_PATHS.items():
            with self.subTest(skill=skill_id):
                package = PACKAGES / skill_id
                commands = {
                    item["id"]: item
                    for item in read_json(package / "commands.json")["commands"]
                }
                interface = read_json(package / "interface.json")
                self.assertTrue(set(expected["commands"] + expected["legacy"]) <= commands.keys())
                recommended = [
                    item
                    for item in interface["validators"]
                    if item["command"] == expected["wrapper"]
                ]
                self.assertEqual(1, len(recommended))
                self.assertEqual(expected["commands"][-1], recommended[0]["runtime_command"])
                if expected["public_invocation_switch"]:
                    self.assertEqual(
                        expected["wrapper"],
                        interface["public_contracts"]["invocation"]["wrapper"],
                    )

    def test_sanitized_baseline_meets_hard_operation_budgets(self) -> None:
        stages = read_json(FIXTURE)["stages"]
        for stage, counts in stages.items():
            with self.subTest(stage=stage):
                legacy_commands = counts["legacy_normal_path_invocations"]
                happy_commands = counts["happy_path_invocations"]
                command_reduction = 1 - happy_commands / legacy_commands
                self.assertGreaterEqual(command_reduction, 0.50)

                required = counts["required_full_reads"]
                legacy_duplicates = counts["legacy_full_reads"] - required
                happy_duplicates = counts["happy_path_full_reads"] - required
                self.assertGreater(legacy_duplicates, 0)
                duplicate_reduction = 1 - happy_duplicates / legacy_duplicates
                self.assertGreaterEqual(duplicate_reduction, 0.70)

    def test_merge_watcher_is_single_expected_head_bound_entry(self) -> None:
        commands = read_json(
            PACKAGES / "guru-merge-task-pr/commands.json"
        )["commands"]
        watcher = next(item for item in commands if item["id"] == "watch-task-pr-checks")
        flags = {item["flag"] for item in watcher["arguments"]}
        self.assertTrue({"--repo", "--pull-request", "--expected-head"} <= flags)
        source = (
            PACKAGES / "guru-merge-task-pr/runtime/owner.py"
        ).read_text(encoding="utf-8")
        watcher_source = source[source.index("def cmd_watch_task_pr_checks") :]
        self.assertNotIn("gh run watch", watcher_source)
        self.assertNotIn("--watch", watcher_source)

    def test_merge_terminal_exits_stop_the_current_skill(self) -> None:
        markers = re.findall(
            r"<!-- guru-skill-exit: (\{.*?\}) -->",
            WORKFLOW.read_text(encoding="utf-8"),
        )
        routes = {
            (item["skill"], item["exit"]): item["consumer"]
            for item in map(json.loads, markers)
        }
        self.assertEqual(
            routes[("guru-merge-task-pr", "closure_mismatch")],
            {"kind": "stop", "id": "task-pr-closure-mismatch"},
        )
        self.assertNotEqual(
            routes[("guru-merge-task-pr", "merged")],
            {"kind": "skill", "id": "guru-merge-task-pr"},
        )
        terminal = read_json(FIXTURE)["terminal_observation"]
        self.assertEqual(terminal["expected_current_contract_operations_after_exit"], 0)


if __name__ == "__main__":
    unittest.main()
