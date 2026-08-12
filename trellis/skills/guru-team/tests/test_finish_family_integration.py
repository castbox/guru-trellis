from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any


SOURCE_REPO = Path(__file__).resolve().parents[4]
EXECUTION_MODE = os.environ.get("GURU_FINISH_INTEGRATION_MODE", "source")
if EXECUTION_MODE not in {"source", "installed"}:
    raise RuntimeError("GURU_FINISH_INTEGRATION_MODE must be source or installed")
REPO = Path(
    os.environ.get("GURU_FINISH_INTEGRATION_ROOT", str(SOURCE_REPO))
).resolve()
if EXECUTION_MODE == "installed":
    SKILLS_ROOT = REPO / ".trellis/guru-team/skills"
    WORKFLOW = REPO / ".trellis/workflow.md"
    EVAL_DISCOVERY = REPO / ".trellis/guru-team/scripts/bash/discover-skill-evals.sh"
    EVAL_RUNNER = REPO / ".trellis/guru-team/scripts/bash/run-skill-evals.sh"
else:
    SKILLS_ROOT = REPO / "trellis/skills/guru-team"
    WORKFLOW = REPO / "trellis/workflows/guru-team/workflow.md"
    EVAL_DISCOVERY = (
        REPO / "trellis/workflows/guru-team/scripts/bash/discover-skill-evals.sh"
    )
    EVAL_RUNNER = (
        REPO / "trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh"
    )

FINISH_EXITS = {
    "guru-review-task-publication": {"ready", "return_to_task_work", "blocked"},
    "guru-verify-extension-installation": {"verified", "blocked"},
    "guru-finalize-task": {
        "publication_review_stale",
        "resume_finalization",
        "reprepare_required",
        "ready_for_merge",
        "blocked",
    },
    "guru-merge-task-pr": {"merged", "merge_blocked", "closure_mismatch"},
}
EXPECTED_CONSUMERS = {
    ("guru-review-task-publication", "ready"): ("skill", "guru-finalize-task"),
    ("guru-review-task-publication", "return_to_task_work"): (
        "workflow",
        "guru-task-publication-work-router",
    ),
    ("guru-review-task-publication", "blocked"): (
        "stop",
        "task-publication-review-blocked",
    ),
    ("guru-verify-extension-installation", "verified"): (
        "stop",
        "extension-installation-verification-verified",
    ),
    ("guru-verify-extension-installation", "blocked"): (
        "stop",
        "extension-installation-verification-blocked",
    ),
    ("guru-finalize-task", "publication_review_stale"): (
        "skill",
        "guru-review-task-publication",
    ),
    ("guru-finalize-task", "resume_finalization"): (
        "skill",
        "guru-finalize-task",
    ),
    ("guru-finalize-task", "reprepare_required"): (
        "skill",
        "guru-finalize-task",
    ),
    ("guru-finalize-task", "ready_for_merge"): (
        "skill",
        "guru-merge-task-pr",
    ),
    ("guru-finalize-task", "blocked"): (
        "stop",
        "task-finalization-blocked",
    ),
    ("guru-merge-task-pr", "merged"): (
        "workflow",
        "guru-finalization-finish-response",
    ),
    ("guru-merge-task-pr", "merge_blocked"): (
        "stop",
        "task-pr-merge-blocked",
    ),
    ("guru-merge-task-pr", "closure_mismatch"): (
        "stop",
        "task-pr-closure-mismatch",
    ),
}
ROUTE_GROUPS = {
    "normal": [
        ("guru-review-task-publication", "ready"),
        ("guru-finalize-task", "ready_for_merge"),
        ("guru-merge-task-pr", "merged"),
    ],
    "return_to_work": [
        ("guru-review-task-publication", "return_to_task_work"),
    ],
    "publication_refresh": [
        ("guru-finalize-task", "publication_review_stale"),
        ("guru-review-task-publication", "ready"),
    ],
    "same_plan_or_reprepare": [
        ("guru-finalize-task", "resume_finalization"),
        ("guru-finalize-task", "reprepare_required"),
    ],
    "terminal": [
        ("guru-review-task-publication", "blocked"),
        ("guru-finalize-task", "blocked"),
        ("guru-merge-task-pr", "merge_blocked"),
        ("guru-merge-task-pr", "closure_mismatch"),
    ],
    "standalone_verification": [
        ("guru-verify-extension-installation", "verified"),
        ("guru-verify-extension-installation", "blocked"),
    ],
}
GURU_ENTRIES = (
    ".codex/prompts/guru-finish-work.md",
    ".claude/commands/guru/finish-work.md",
    ".cursor/commands/guru-finish-work.md",
)
TERMINAL_CASES = {
    "publication-ready-ready-for-merge": "ready_for_merge",
    "same-plan-ready-for-merge": "ready_for_merge",
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain one JSON object")
    return value


def package(skill_id: str) -> Path:
    return SKILLS_ROOT / "packages" / skill_id


def markers(kind: str) -> list[dict[str, Any]]:
    pattern = re.compile(rf"<!-- guru-{kind}: (\{{.*?\}}) -->")
    return [json.loads(value) for value in pattern.findall(WORKFLOW.read_text(encoding="utf-8"))]


class FinishFamilyIntegrationTests(unittest.TestCase):
    def test_finish_exits_have_exact_unique_public_consumers(self) -> None:
        seen: set[tuple[str, str]] = set()
        for skill_id, expected_exits in FINISH_EXITS.items():
            interface = read_json(package(skill_id) / "interface.json")
            exits = interface["external_exits"]
            self.assertEqual({item["id"] for item in exits}, expected_exits)
            for item in exits:
                identity = (skill_id, item["id"])
                self.assertNotIn(identity, seen)
                seen.add(identity)
                consumer = item["consumer"]
                self.assertEqual(
                    (consumer["kind"], consumer["id"]),
                    EXPECTED_CONSUMERS[identity],
                )
            contracts = interface["public_contracts"]
            self.assertEqual(
                {item["exit_id"] for item in contracts["outputs"]}, expected_exits
            )
            self.assertEqual(
                {item["exit_id"] for item in contracts["projections"]},
                expected_exits,
            )

    def test_workflow_keeps_current_projection_and_six_route_groups(self) -> None:
        invokes = markers("skill-invoke")
        exits = markers("skill-exit")
        targets = markers("(?:workflow|stop)-target")
        self.assertEqual(len(invokes), 14)
        self.assertEqual(len(exits), 52)
        self.assertEqual(len(targets), 31)
        routed = {
            (item["skill"], item["exit"]): (
                item["consumer"]["kind"],
                item["consumer"]["id"],
            )
            for item in exits
        }
        for group in ROUTE_GROUPS.values():
            for identity in group:
                if identity[0] == "guru-verify-extension-installation":
                    self.assertNotIn(identity, routed)
                    continue
                self.assertIn(identity, routed)
                if identity in EXPECTED_CONSUMERS:
                    self.assertEqual(routed[identity], EXPECTED_CONSUMERS[identity])

    def test_business_closeout_has_no_verifier_route(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        business_skills = {
            "guru-review-task-publication",
            "guru-finalize-task",
            "guru-merge-task-pr",
        }
        for item in markers("skill-exit"):
            if item["skill"] in business_skills:
                self.assertNotEqual(
                    item["consumer"].get("id"),
                    "guru-verify-extension-installation",
                )
        for skill_id in business_skills:
            contract = json.dumps(read_json(package(skill_id) / "interface.json"))
            self.assertNotIn("marketplace-verification", contract)
        self.assertNotIn("guru-verify-extension-installation", text)

    def test_guru_finish_entries_are_equal_thin_routes(self) -> None:
        contents = [(REPO / relative).read_text(encoding="utf-8") for relative in GURU_ENTRIES]
        self.assertEqual(len(set(contents)), 1)
        content = contents[0]
        self.assertIn("guru-finalize-task", content)
        self.assertIn("guru-merge-task-pr", content)
        self.assertNotIn("implementation-handoff", content)

    def test_terminal_corpus_matches_public_discovery(self) -> None:
        corpus = read_json(package("guru-finalize-task") / "evals/evals.json")
        expected = [item["id"] for item in corpus["evals"]]
        process = subprocess.run(
            [
                str(EVAL_DISCOVERY),
                "--mode",
                EXECUTION_MODE,
                "--skill",
                "guru-finalize-task",
                "--json",
            ],
            cwd=REPO,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        discovery = json.loads(process.stdout)
        self.assertEqual(discovery["case_ids"], expected)
        self.assertEqual(
            [item["id"] for item in discovery["adapters"]],
            ["shared", "codex", "claude", "cursor"],
        )

    def test_terminal_cases_execute_through_public_eval_boundary(self) -> None:
        for case_id, expected_exit in TERMINAL_CASES.items():
            with self.subTest(case=case_id), tempfile.TemporaryDirectory(
                prefix="guru-finish-terminal-"
            ) as directory:
                process = subprocess.run(
                    [
                        str(EVAL_RUNNER),
                        "--mode",
                        EXECUTION_MODE,
                        "--skill",
                        "guru-finalize-task",
                        "--adapter",
                        "shared",
                        "--case",
                        case_id,
                        "--run-root",
                        directory,
                        "--json",
                    ],
                    cwd=REPO,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                result = json.loads(process.stdout)
                self.assertEqual(result["status"], "passed", result)
                case = result["cases"][0]
                self.assertEqual(case["actual_exit"], expected_exit)
                checks = {
                    item["id"]: item["passed"]
                    for item in case["deterministic_results"]
                }
                self.assertTrue(
                    all(
                        checks[item]
                        for item in (
                            "expected-exit",
                            "actual-exit-output-schema",
                            "expected-route",
                        )
                    )
                )
                transcript = read_json(Path(case["transcript_locator"]))
                trace = read_json(Path(transcript["native_trace_path"]))
                self.assertEqual(trace["events"][0]["kind"], "read")
                self.assertEqual(trace["events"][0]["target_kind"], "skill_contract")
                self.assertEqual(trace["events"][-1]["kind"], "invoke")
                self.assertEqual(trace["events"][-1]["returncode"], 0)


if __name__ == "__main__":
    unittest.main()
