from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest import mock


PACKAGE = Path(__file__).resolve().parents[1]
PUBLICATION_PACKAGE = PACKAGE.parent / "guru-review-task-publication"


def load_runtime():
    runtime_path = PACKAGE / "runtime/owner.py"
    spec = importlib.util.spec_from_file_location("merge_task_pr_runtime", runtime_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GTT = load_runtime()


class MergeTaskPrContractTest(unittest.TestCase):
    def terminal_fixture(self, *, closed: bool = True) -> tuple[dict, dict, dict]:
        public_input = {
            "repo_ref": "castbox/guru-trellis",
            "pr_number": 218,
            "pr_url": "https://github.com/castbox/guru-trellis/pull/218",
            "expected_head_sha": "1" * 40,
            "expected_base_branch": "main",
            "expected_head_branch": "fix/218-terminal-output",
            "expected_close_issues": [218],
        }
        facts = {
            "pr": {
                "number": 218,
                "url": public_input["pr_url"],
                "state": "MERGED",
                "head_sha": public_input["expected_head_sha"],
                "base_branch": "main",
                "head_branch": "fix/218-terminal-output",
                "merged_at": "2026-08-14T10:00:00Z",
                "merge_commit": {"oid": "2" * 40},
            },
            "close_issues": [218],
            "issues": [{
                "number": 218,
                "state": "CLOSED" if closed else "OPEN",
                "closed_at": "2026-08-14T10:00:01Z" if closed else None,
            }],
        }
        output = GTT.task_pr_merge_terminal_output(public_input, facts)
        return public_input, facts, output

    def test_terminal_recovery_revalidates_and_skips_merge_mutation(self) -> None:
        public_input, facts, output = self.terminal_fixture()
        gate = {"terminal_output": output}
        args = Namespace(root="/repo", input="input.json", gate="gate.json")
        with (
            mock.patch.object(GTT, "repo_root", return_value=Path("/repo")),
            mock.patch.object(GTT, "task_pr_merge_json_input", return_value=public_input),
            mock.patch.object(GTT, "task_pr_merge_gate", return_value=(Path("/repo/gate.json"), gate)),
            mock.patch.object(GTT, "task_pr_merge_live_facts", return_value=facts),
            mock.patch.object(GTT, "run") as mutation,
            mock.patch.object(GTT, "require_gh_auth") as auth,
        ):
            result = GTT.cmd_execute_task_pr_merge(args)

        self.assertEqual(result, {"status": "recovered", "typed_exit": "merged", "output": output})
        mutation.assert_not_called()
        auth.assert_not_called()

    def test_terminal_recovery_preserves_closure_mismatch(self) -> None:
        public_input, facts, output = self.terminal_fixture(closed=False)
        self.assertEqual(output["exit_id"], "closure_mismatch")
        checked = GTT.check_task_pr_merge_result
        with mock.patch.object(GTT, "task_pr_merge_live_facts", return_value=facts):
            result = checked(Path("/repo"), public_input, {"terminal_output": output})
        self.assertEqual(result["typed_exit"], "closure_mismatch")
        self.assertEqual(result["output"], output)

    def test_terminal_recovery_rejects_head_or_commit_drift(self) -> None:
        public_input, facts, output = self.terminal_fixture()
        for field, changed in (
            ("head_sha", "3" * 40),
            ("merge_commit", {"oid": "4" * 40}),
        ):
            with self.subTest(field=field):
                stale = json.loads(json.dumps(facts))
                stale["pr"][field] = changed
                with mock.patch.object(GTT, "task_pr_merge_live_facts", return_value=stale):
                    with self.assertRaises(GTT.WorkflowError):
                        GTT.check_task_pr_merge_result(
                            Path("/repo"), public_input, {"terminal_output": output}
                        )

    def test_package_local_runtime_is_monolith_independent(self) -> None:
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((PACKAGE / "runtime").glob("*.py"))
        )
        for retired in ("guru_team_trellis.py", "verification_required", "not_required", "finalization_verification"):
            self.assertNotIn(retired, runtime_text)
        commands = json.loads((PACKAGE / "commands.json").read_text(encoding="utf-8"))
        interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {(item["validator_id"], item["id"]) for item in commands["commands"]},
            {(item["id"], item["runtime_command"]) for item in interface["validators"]},
        )
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
        import jsonschema
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

    def test_live_facts_capture_required_readiness_composite(self) -> None:
        public_input = {
            "repo_ref": "castbox/guru-trellis",
            "pr_number": 180,
            "expected_close_issues": [180],
        }
        pr = {
            "number": 180,
            "url": "https://github.com/castbox/guru-trellis/pull/180",
            "state": "OPEN",
            "isDraft": False,
            "baseRefName": "main",
            "headRefName": "codex/180-eval",
            "headRefOid": "1" * 40,
            "mergeable": "MERGEABLE",
            "mergeStateStatus": "UNSTABLE",
            "reviewDecision": "APPROVED",
            "statusCheckRollup": [
                {"name": "required-ci", "conclusion": "SUCCESS"},
                {"name": "optional-preview", "conclusion": "FAILURE"},
            ],
            "body": "Closes #180\n",
            "mergedAt": None,
            "mergeCommit": None,
        }
        policy = {
            "full_name": "castbox/guru-trellis",
            "allow_merge_commit": True,
            "allow_squash_merge": False,
            "allow_rebase_merge": False,
        }
        issue = {
            "number": 180,
            "state": "OPEN",
            "closedAt": None,
            "url": "https://github.com/castbox/guru-trellis/issues/180",
        }
        with mock.patch.object(GTT, "gh_json", side_effect=[pr, policy, issue]) as gh_json:
            facts = GTT.task_pr_merge_live_facts(Path("."), public_input)

        requested_fields = gh_json.call_args_list[0].args[0][-1].split(",")
        self.assertIn("mergeStateStatus", requested_fields)
        self.assertIn(
            "mergeStateStatus",
            gh_json.call_args_list[0].kwargs["required_fields"],
        )
        self.assertEqual(facts["pr"]["merge_state_status"], "UNSTABLE")
        self.assertEqual(
            facts["pr"]["checks"],
            [
                {"name": "required-ci", "state": "SUCCESS"},
                {"name": "optional-preview", "state": "FAILURE"},
            ],
        )

    def test_live_facts_reject_unknown_required_readiness_composite(self) -> None:
        public_input = {
            "repo_ref": "castbox/guru-trellis",
            "pr_number": 180,
            "expected_close_issues": [180],
        }
        pr = {
            "number": 180,
            "url": "https://github.com/castbox/guru-trellis/pull/180",
            "state": "OPEN",
            "isDraft": False,
            "baseRefName": "main",
            "headRefName": "codex/180-eval",
            "headRefOid": "1" * 40,
            "mergeable": "MERGEABLE",
            "mergeStateStatus": "FUTURE_STATE",
            "reviewDecision": "APPROVED",
            "statusCheckRollup": [],
            "body": "Closes #180\n",
            "mergedAt": None,
            "mergeCommit": None,
        }
        with mock.patch.object(GTT, "gh_json", return_value=pr):
            with self.assertRaisesRegex(GTT.WorkflowError, "response is incomplete"):
                GTT.task_pr_merge_live_facts(Path("."), public_input)

    def test_preflight_blocks_draft_head_drift_and_early_close(self) -> None:
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
                "mergeable": "UNKNOWN", "merge_state_status": "BLOCKED",
                "checks": [{"name": "ci", "state": "PENDING"}],
            },
            "close_issues": [180, 181],
            "issues": [{"number": 180, "state": "CLOSED"}],
        }
        errors = GTT.task_pr_merge_preflight_errors(public_input, facts)
        self.assertEqual(len(errors), 7)
        self.assertTrue(any("expected head" in item for item in errors))
        self.assertTrue(any("base branch" in item for item in errors))
        self.assertTrue(any("head branch" in item for item in errors))
        self.assertTrue(any("reviewed close scope" in item for item in errors))
        self.assertTrue(any("before merge" in item for item in errors))
        self.assertFalse(any("checks" in item for item in errors))

    def test_optional_failed_check_is_not_an_objective_blocker(self) -> None:
        public_input = {
            "expected_head_sha": "1" * 40,
            "expected_base_branch": "main",
            "expected_head_branch": "codex/180-eval",
            "expected_close_issues": [180],
        }
        facts = {
            "pr": {
                "state": "OPEN", "is_draft": False, "head_sha": "1" * 40,
                "base_branch": "main", "head_branch": "codex/180-eval",
                "mergeable": "MERGEABLE", "merge_state_status": "UNSTABLE",
                "checks": [
                    {"name": "required-ci", "state": "SUCCESS"},
                    {"name": "optional-preview", "state": "FAILURE"},
                ],
            },
            "close_issues": [180],
            "issues": [{"number": 180, "state": "OPEN"}],
        }

        self.assertEqual(GTT.task_pr_merge_preflight_errors(public_input, facts), [])

    def test_record_merge_route_requires_every_semantic_dimension_passed(self) -> None:
        public_input = {
            "repo_ref": "castbox/guru-trellis",
            "pr_number": 180,
            "expected_head_sha": "1" * 40,
            "expected_base_branch": "main",
            "expected_head_branch": "codex/180-eval",
            "expected_close_issues": [180],
        }
        facts = {
            "facts_sha256": "2" * 64,
            "pr": {
                "state": "OPEN", "is_draft": False, "head_sha": "1" * 40,
                "base_branch": "main", "head_branch": "codex/180-eval",
                "mergeable": "MERGEABLE", "merge_state_status": "BLOCKED",
                "checks": [],
            },
            "repository_policy": {"allowed_methods": ["merge"]},
            "close_issues": [180],
            "issues": [{"number": 180, "state": "OPEN"}],
        }
        dimensions = [
            {"id": identifier, "status": "passed", "summary": "Current evidence passes."}
            for identifier in GTT.TASK_PR_MERGE_DIMENSIONS
        ]
        dimensions[2]["status"] = "blocked"
        review_payload = {
            "semantic_review": {"dimensions": dimensions},
            "route": {"typed_exit": "merged", "merge_method": "merge"},
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            review_path = Path(temp_dir) / "review.json"
            review_path.write_text(json.dumps(review_payload), encoding="utf-8")
            args = Namespace(root=temp_dir, input="unused.json", review_input=str(review_path))
            with (
                mock.patch.object(GTT, "repo_root", return_value=Path(temp_dir)),
                mock.patch.object(GTT, "task_pr_merge_json_input", return_value=public_input),
                mock.patch.object(GTT, "task_pr_merge_live_facts", return_value=facts),
            ):
                with self.assertRaisesRegex(GTT.WorkflowError, "cannot record a merge route"):
                    GTT.cmd_record_task_pr_merge(args)

    def test_check_rejects_stale_live_facts_digest(self) -> None:
        public_input = {
            "repo_ref": "castbox/guru-trellis",
            "pr_number": 180,
            "expected_head_sha": "1" * 40,
            "expected_base_branch": "main",
            "expected_head_branch": "codex/180-eval",
            "expected_close_issues": [180],
        }
        clean_facts = {
            "pr": {"merge_state_status": "CLEAN"},
            "repository_policy": {"allowed_methods": ["merge"]},
        }
        clean_digest = GTT.canonical_json_sha256(clean_facts)
        changed_facts = {
            "pr": {"merge_state_status": "BLOCKED"},
            "repository_policy": {"allowed_methods": ["merge"]},
        }
        changed_facts["facts_sha256"] = GTT.canonical_json_sha256(changed_facts)
        self.assertNotEqual(clean_digest, changed_facts["facts_sha256"])
        gate = {
            "facts_sha256": clean_digest,
            "route": {"typed_exit": "merged", "merge_method": "merge"},
        }
        with mock.patch.object(
            GTT,
            "task_pr_merge_live_facts",
            return_value=changed_facts,
        ):
            with self.assertRaisesRegex(GTT.WorkflowError, "stale against live GitHub facts"):
                GTT.check_task_pr_merge_result(Path("."), public_input, gate)

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
