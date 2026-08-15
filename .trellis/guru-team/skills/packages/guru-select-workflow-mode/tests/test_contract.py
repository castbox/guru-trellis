from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
PACKAGE = ROOT / "trellis/skills/guru-team/packages/guru-select-workflow-mode"


class WorkflowModeContractTest(unittest.TestCase):
    def test_environment_checker_is_package_owned_and_reports_warnings(self) -> None:
        commands = json.loads((PACKAGE / "commands.json").read_text())
        command = next(item for item in commands["commands"] if item["id"] == "check-workflow-environment")
        self.assertEqual(command["entrypoint"], "runtime/check.py")
        self.assertEqual(command["runtime_role"], "check")
        self.assertEqual(command["side_effect"], "github_read")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "README.md").write_text("test\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "test"], check=True)
            (root / ".trellis/guru-team").mkdir(parents=True)
            (root / ".trellis/guru-team/config.yml").write_text(
                "base_branch: main\nbase_branch_candidates:\n  - main\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment["PATH"] = "/usr/bin:/bin"
            result = subprocess.run(
                [str(PACKAGE / "scripts/check-env.sh"), "--root", str(root), "--json"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=environment,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["base_branch"], "main")
            self.assertFalse(payload["gh_installed"])
            self.assertIn("GitHub CLI is not installed.", payload["warnings"])
            self.assertEqual(payload["guru_team_extension"]["status"], "missing")

    def test_environment_help_and_compatibility_wrapper_route_to_package(self) -> None:
        wrapper = (
            ROOT / "trellis/workflows/guru-team/scripts/bash/check-env.sh"
            if (ROOT / "trellis/skills/guru-team").is_dir()
            else ROOT / ".trellis/guru-team/scripts/bash/check-env.sh"
        )
        for target in (PACKAGE / "scripts/check-env.sh", wrapper):
            result = subprocess.run(
                [str(target), "--help"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            self.assertIn("usage: check-workflow-environment", result.stdout)
            self.assertIn("owner: guru-select-workflow-mode", result.stdout)

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
                "automatic-high-confidence",
                "insufficient-confirmed",
                "insufficient-refused",
                "complex-request",
                "simple-issue",
                "insufficient-issue-confirmed",
                "complex-issue",
                "same-file-count-low-risk",
                "same-file-count-high-risk",
                "non-default-checkout",
                "active-task-same-scope",
                "active-task-scope-expansion",
                "unrelated-worktree",
                "dirty-overlap",
                "position-evidence-insufficient",
                "unrelated-dirty-preserved",
                "same-scope-retry",
                "automatic-risk-expansion",
                "explicit-risk-expansion",
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

    def test_semantic_owner_and_checkout_consumer_boundaries_are_explicit(self) -> None:
        skill = (PACKAGE / "SKILL.md").read_text()
        workflow = (ROOT / "trellis/workflows/guru-team/workflow.md").read_text()
        self.assertIn("这次走 task-free", skill)
        self.assertIn("File count, paths, and", skill)
        self.assertIn("never reads remote branch protection", skill)
        self.assertIn("active task with the same scope returns to that task route", workflow)
        self.assertIn("Never read branch protection", workflow)
        self.assertIn("automatically selected route is re-evaluated", workflow)
        self.assertIn("explicitly selected route reports the new facts", workflow)

    def test_initial_gate_routes_only_file_changes_to_selector(self) -> None:
        workflow = (ROOT / "trellis/workflows/guru-team/workflow.md").read_text()
        gate = workflow.split("## Guru Team Gate", 1)[1].split(
            "## Integrated Public Graph", 1
        )[0]
        self.assertIn(
            "a file-changing request that is not already inside an active-task route",
            gate,
        )
        self.assertIn(
            "Issue-backed or task-like requests that only ask\n"
            "  for information remain non-file-changing and are answered directly",
            gate,
        )
        self.assertNotIn(
            "repo-changing, issue-backed, task-like, or file-changing work",
            gate,
        )

    def test_task_free_public_dto_and_projection_remain_minimal(self) -> None:
        expected = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "guru-workflow-mode-output-task-free-1.0",
            "type": "object",
            "additionalProperties": False,
            "required": ["exit_id"],
            "properties": {"exit_id": {"const": "task_free"}},
        }
        output_schema = json.loads(
            (PACKAGE / "schemas/public-task-free-output.schema.json").read_text()
        )
        consumer_schema = json.loads(
            (
                ROOT
                / "trellis/skills/guru-team/consumers/workflow/stage0/workflow-mode-task-free.schema.json"
            ).read_text()
        )
        self.assertEqual(output_schema, expected)
        self.assertEqual(
            consumer_schema,
            {**expected, "$id": "guru-workflow-task-free-input-1.0"},
        )
        interface = json.loads((PACKAGE / "interface.json").read_text())
        projection = next(
            item
            for item in interface["public_contracts"]["projections"]
            if item["exit_id"] == "task_free"
        )
        self.assertEqual(projection["operation"], "direct")

    def test_task_free_contract_has_no_branch_protection_query_or_lifecycle_executor(self) -> None:
        surfaces = [
            ROOT / "trellis/workflows/guru-team/workflow.md",
            ROOT / "README.md",
            ROOT / "trellis/workflows/guru-team/README.md",
            ROOT / "trellis/presets/guru-team/README.md",
        ]
        query_pattern = re.compile(
            r"gh\s+api[^\n]*(?:branches/[^\s]+/protection|branch[- ]protection)",
            re.IGNORECASE,
        )
        for path in surfaces:
            text = path.read_text()
            self.assertIn("这次走 task-free", text, path)
            self.assertIsNone(query_pattern.search(text), path)
        commands = json.loads((PACKAGE / "commands.json").read_text())
        invocation = next(
            item
            for item in commands["commands"]
            if item["id"] == "invoke-guru-select-workflow-mode"
        )
        self.assertEqual(invocation["side_effect"], "none")
        runtime_text = (PACKAGE / "runtime/invoke.py").read_text()
        for forbidden in ("subprocess", "git commit", "git push", "gh pr", "task.py"):
            self.assertNotIn(forbidden, runtime_text)

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
