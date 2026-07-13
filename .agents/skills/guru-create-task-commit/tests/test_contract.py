from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path


class TaskCommitPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.interface = json.loads((self.package / "interface.json").read_text(encoding="utf-8"))

    def test_identity_modes_and_exits(self) -> None:
        self.assertEqual(self.interface["id"], "guru-create-task-commit")
        self.assertEqual(
            self.interface["modes"]["workflow"]["entry_precondition_ids"],
            self.interface["modes"]["standalone"]["entry_precondition_ids"],
        )
        self.assertEqual(
            [item["id"] for item in self.interface["external_exits"]],
            ["committed", "revision-required", "blocked"],
        )

    def test_skill_triggers_and_thin_wrappers(self) -> None:
        skill = (self.package / "SKILL.md").read_text(encoding="utf-8")
        for phrase in ("creating a task commit", "committing Phase 2 changes", "finding fix", "revision commit"):
            self.assertIn(phrase, skill)
        for name in ("check-task-commit-plan.sh", "create-task-commit.sh"):
            wrapper = (self.package / "scripts" / name).read_text(encoding="utf-8")
            self.assertIn("exec \"$RUNTIME\"", wrapper)
            self.assertNotIn("validate_commit_message", wrapper)
            self.assertNotIn("git add", wrapper)

    def test_example_message_and_plan_digests_match(self) -> None:
        plan = json.loads((self.package / "examples/task-commit-plan.json").read_text(encoding="utf-8"))
        message = plan["message"]["bytes"].encode("utf-8")
        self.assertEqual(hashlib.sha256(message).hexdigest(), plan["message"]["sha256"])
        normalized = json.loads(json.dumps(plan, ensure_ascii=False))
        normalized["freshness"]["plan_digest"] = ""
        encoded = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), plan["freshness"]["plan_digest"])

    def test_public_result_schema_state_machine(self) -> None:
        if importlib.util.find_spec("jsonschema") is None:
            self.skipTest("optional jsonschema dependency is not installed")
        from jsonschema import Draft202012Validator

        schema = json.loads(
            (self.package / "schemas/task-commit-plan.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        planned = json.loads(
            (self.package / "examples/task-commit-plan.json").read_text(encoding="utf-8")
        )
        exact_paths = planned["exact_stage_paths"]
        tree_paths = [
            {
                "path": path,
                "expected_blob": "a" * 40,
                "expected_mode": "100644",
                "actual_blob": "a" * 40,
                "actual_mode": "100644",
                "matches": True,
            }
            for path in exact_paths
        ]
        tree_evidence = {
            "expected_tree": "b" * 40,
            "actual_tree": "b" * 40,
            "actual_source": "commit",
            "matches": True,
            "paths": tree_paths,
        }
        index_tree_evidence = copy.deepcopy(tree_evidence)
        index_tree_evidence["actual_source"] = "index"
        mismatched_index_tree = copy.deepcopy(index_tree_evidence)
        mismatched_index_tree["actual_tree"] = "c" * 40
        mismatched_index_tree["matches"] = False
        mismatched_index_tree["paths"][0]["actual_blob"] = "d" * 40
        mismatched_index_tree["paths"][0]["matches"] = False
        mismatched_commit_tree = copy.deepcopy(mismatched_index_tree)
        mismatched_commit_tree["actual_source"] = "commit"
        blocked_base = {
            "status": "blocked",
            "exit": "blocked",
            "recorded_at": "2026-01-01T00:00:00Z",
            "failure_stage": "pre-commit",
            "pre_commit_head": planned["git"]["pre_commit_head"],
            "commit_sha": planned["git"]["pre_commit_head"],
            "head_changed": False,
            "parent": None,
            "message_sha256": None,
            "committed_paths": [],
            "unrelated_preserved": True,
            "hook_mutation": False,
            "unexpected_staged_paths": [],
            "unexpected_dirty_paths": [],
            "planned_unstaged_paths": [],
            "tree_evidence": None,
            "errors": ["Objective task commit failure."],
        }
        pre_commit_with_index = copy.deepcopy(blocked_base)
        pre_commit_with_index["tree_evidence"] = index_tree_evidence
        commit_without_mutation = copy.deepcopy(blocked_base)
        commit_without_mutation.update(
            {"failure_stage": "commit", "tree_evidence": index_tree_evidence}
        )
        commit_with_mutation = copy.deepcopy(commit_without_mutation)
        commit_with_mutation.update(
            {"hook_mutation": True, "tree_evidence": mismatched_index_tree}
        )
        postcondition_non_tree_error = copy.deepcopy(blocked_base)
        postcondition_non_tree_error.update(
            {
                "failure_stage": "postcondition",
                "commit_sha": "2" * 40,
                "head_changed": True,
                "parent": planned["git"]["pre_commit_head"],
                "message_sha256": planned["message"]["sha256"],
                "committed_paths": exact_paths,
                "tree_evidence": tree_evidence,
                "errors": ["Committed message parser rejected a non-tree postcondition."],
            }
        )
        postcondition_with_mutation = copy.deepcopy(postcondition_non_tree_error)
        postcondition_with_mutation.update(
            {"hook_mutation": True, "tree_evidence": mismatched_commit_tree}
        )
        positive_results = [
            {"status": "planned", "exit": None},
            {
                "status": "revision-required",
                "exit": "revision-required",
                "recorded_at": "2026-01-01T00:00:00Z",
                "errors": ["Candidate message requires revision."],
            },
            blocked_base,
            pre_commit_with_index,
            commit_without_mutation,
            commit_with_mutation,
            postcondition_non_tree_error,
            postcondition_with_mutation,
            {
                "status": "committed",
                "exit": "committed",
                "recorded_at": "2026-01-01T00:00:00Z",
                "commit_sha": "2" * 40,
                "parent": planned["git"]["pre_commit_head"],
                "message_sha256": planned["message"]["sha256"],
                "committed_paths": exact_paths,
                "unrelated_preserved": True,
                "hook_mutation": False,
                "tree_evidence": tree_evidence,
            },
        ]
        for result in positive_results:
            with self.subTest(status=result["status"]):
                payload = copy.deepcopy(planned)
                payload["result"] = result
                self.assertEqual(list(validator.iter_errors(payload)), [])

        invalid_results = [
            {"status": "blocked", "exit": "committed"},
            {"status": "committed", "exit": "committed"},
            {"status": "planned", "exit": None, "unexpected": True},
            {**blocked_base, "errors": []},
            {**blocked_base, "hook_mutation": True},
            {**positive_results[-1], "hook_mutation": True},
            {key: value for key, value in positive_results[-1].items() if key != "tree_evidence"},
            {**blocked_base, "tree_evidence": mismatched_index_tree},
            {**commit_without_mutation, "tree_evidence": None},
            {
                **blocked_base,
                "failure_stage": "postcondition",
                "tree_evidence": None,
            },
            {**commit_without_mutation, "tree_evidence": tree_evidence},
            {**postcondition_non_tree_error, "tree_evidence": index_tree_evidence},
        ]
        invalid_results.append(
            {
                **commit_without_mutation,
                "failure_stage": "commit",
                "hook_mutation": False,
                "tree_evidence": mismatched_index_tree,
            }
        )
        for result in invalid_results:
            with self.subTest(result=result):
                payload = copy.deepcopy(planned)
                payload["result"] = result
                self.assertTrue(list(validator.iter_errors(payload)))


if __name__ == "__main__":
    unittest.main()
