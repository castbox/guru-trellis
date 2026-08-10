from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path
from unittest import mock


PACKAGE = Path(__file__).resolve().parents[1]
PUBLICATION_PACKAGE = PACKAGE.parent / "guru-review-task-publication"


def load_runtime():
    candidates: list[Path] = []
    for parent in PACKAGE.parents:
        candidates.extend([
            parent / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py",
            parent / ".trellis/guru-team/scripts/python/guru_team_trellis.py",
        ])
    runtime_path = next(path for path in candidates if path.is_file())
    spec = importlib.util.spec_from_file_location("merge_task_pr_runtime", runtime_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GTT = load_runtime()


class MergeTaskPrContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))

    def test_semantic_package_has_exact_three_exits(self) -> None:
        self.assertEqual(self.interface["judgment_mode"], "semantic")
        self.assertEqual(
            self.interface["ordered_stages"],
            [
                "forward_behavior",
                "ai_review_gate",
                "conditional_human_confirmation",
                "recorder_validator",
                "typed_exit",
            ],
        )
        exits = self.interface["external_exits"]
        self.assertEqual(
            [item["id"] for item in exits],
            ["merged", "merge_blocked", "closure_mismatch"],
        )
        self.assertEqual(
            len({(item["consumer"]["kind"], item["consumer"]["id"]) for item in exits}),
            3,
        )

    def test_workflow_and_standalone_profiles_are_closed_and_minimal(self) -> None:
        profiles = self.interface["public_contracts"]["input"]["profiles"]
        self.assertEqual([item["id"] for item in profiles], ["ready_for_merge", "standalone_merge"])
        expected = {
            "schema_version", "profile", "mode", "repo_ref", "pr_number",
            "pr_url", "expected_head_sha", "expected_base_branch",
            "expected_head_branch", "expected_close_issues",
        }
        for profile in profiles:
            schema = json.loads((PACKAGE / profile["schema"]["path"]).read_text(encoding="utf-8"))
            self.assertEqual(set(schema["required"]), expected)
            self.assertEqual(set(schema["properties"]), expected)

    def test_outputs_exclude_finalizer_and_authorization_state(self) -> None:
        forbidden = {
            "task_ref", "plan_ref", "transaction", "review_history",
            "authorization", "confirmation", "local_main", "cleanup",
        }
        for output in self.interface["public_contracts"]["outputs"]:
            schema = json.loads((PACKAGE / output["schema"]["path"]).read_text(encoding="utf-8"))
            self.assertFalse(forbidden & set(schema["properties"]))

    def test_examples_validate_against_independent_schemas(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        for profile in self.interface["public_contracts"]["input"]["profiles"]:
            schema = json.loads((PACKAGE / profile["schema"]["path"]).read_text(encoding="utf-8"))
            example = json.loads((PACKAGE / profile["example"]["path"]).read_text(encoding="utf-8"))
            self.assertEqual(list(jsonschema.Draft202012Validator(schema).iter_errors(example)), [])
        for output in self.interface["public_contracts"]["outputs"]:
            schema = json.loads((PACKAGE / output["schema"]["path"]).read_text(encoding="utf-8"))
            example = json.loads((PACKAGE / output["example"]["path"]).read_text(encoding="utf-8"))
            self.assertEqual(list(jsonschema.Draft202012Validator(schema).iter_errors(example)), [])

    def test_close_keyword_parser_selects_only_line_owned_closures(self) -> None:
        body = (
            "## Issue\n"
            "Closes #180\n"
            "Related #174\n"
            "Fixes #181.\n"
            "* Resolves #182。\n"
            "+ Close #183.\n"
            "text Closes #999\n"
            "- This sentence mentions Closes #998。\n"
        )
        self.assertEqual(
            GTT.task_pr_merge_close_issues(body),
            [180, 181, 182, 183],
        )

    def test_close_keyword_parser_accepts_publication_producer_bodies(self) -> None:
        public_ready = json.loads(
            (PUBLICATION_PACKAGE / "examples/public-ready-output.json").read_text(
                encoding="utf-8"
            )
        )
        readiness = json.loads(
            (PUBLICATION_PACKAGE / "examples/pr-readiness.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(GTT.task_pr_merge_close_issues(public_ready["pr_body"]), [179])
        self.assertEqual(
            GTT.task_pr_merge_close_issues(readiness["pr_payload"]["body"]),
            [179],
        )

    def test_preflight_blocks_draft_head_drift_checks_and_early_close(self) -> None:
        public_input = {
            "expected_head_sha": "1" * 40,
            "expected_base_branch": "main",
            "expected_head_branch": "codex/180-eval",
            "expected_close_issues": [180],
        }
        facts = {
            "pr": {
                "state": "OPEN", "is_draft": True, "head_sha": "2" * 40,
                "base_branch": "release", "head_branch": "codex/other",
                "mergeable": "UNKNOWN", "checks": [{"name": "ci", "state": "PENDING"}],
            },
            "close_issues": [180, 181],
            "issues": [{"number": 180, "state": "CLOSED"}],
        }
        errors = GTT.task_pr_merge_preflight_errors(public_input, facts)
        self.assertEqual(len(errors), 8)
        self.assertTrue(any("expected head" in item for item in errors))
        self.assertTrue(any("base branch" in item for item in errors))
        self.assertTrue(any("head branch" in item for item in errors))
        self.assertTrue(any("reviewed close scope" in item for item in errors))
        self.assertTrue(any("before merge" in item for item in errors))

    def test_runtime_has_expected_head_merge_and_no_issue_close_or_local_sync(self) -> None:
        source = Path(GTT.__file__).read_text(encoding="utf-8")
        start = source.index("def cmd_execute_task_pr_merge")
        end = source.index("def cmd_invoke_task_pr_merge", start)
        executor = source[start:end]
        self.assertIn('"--match-head-commit"', executor)
        self.assertNotIn("gh issue close", executor)
        self.assertNotIn('"issue", "close"', executor)
        self.assertNotIn("cmd_sync_base", executor)
        self.assertNotIn("git pull", executor)

    def test_post_merge_closure_timestamp_rule(self) -> None:
        self.assertLess(
            GTT.parse_iso_datetime("2026-08-05T06:20:54Z"),
            GTT.parse_iso_datetime("2026-08-05T06:21:00Z"),
        )

    def test_evals_cover_all_exits_and_primary_blockers(self) -> None:
        corpus = json.loads((PACKAGE / "evals/evals.json").read_text(encoding="utf-8"))
        exits = {item["expected_exit"] for item in corpus["evals"]}
        self.assertEqual(exits, {"merged", "merge_blocked", "closure_mismatch"})
        ids = {item["id"] for item in corpus["evals"]}
        self.assertTrue({
            "standalone-draft-blocked",
            "workflow-head-drift-blocked",
            "workflow-branch-drift-blocked",
            "workflow-close-keyword-mismatch-blocked",
            "workflow-added-close-keyword-blocked",
        } <= ids)

    def test_semantic_evals_declare_owner_staging_and_public_invocation(self) -> None:
        corpus = json.loads((PACKAGE / "evals/evals.json").read_text(encoding="utf-8"))
        for case in corpus["evals"]:
            facts_path = next(path for path in case["files"] if path.endswith("-facts.json"))
            facts = json.loads((PACKAGE / facts_path).read_text(encoding="utf-8"))
            self.assertTrue(facts["owner_staging"]["recipe"].startswith("merge-"))
            arguments = facts["public_invocation"]["arguments"]
            self.assertEqual(arguments[:2], ["--input", ".trellis/.runtime/guru-team/evals/public-input.json"])
            self.assertIn("--gate", arguments)


if __name__ == "__main__":
    unittest.main()
