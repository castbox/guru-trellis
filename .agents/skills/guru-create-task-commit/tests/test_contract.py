from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path


def task_commit_tree_evidence(
    exact_paths: list[str], *, source: str, matches: bool
) -> dict[str, object]:
    return {
        "expected_tree": "a" * 40,
        "actual_tree": "a" * 40 if matches else "b" * 40,
        "actual_source": source,
        "matches": matches,
        "paths": [
            {
                "path": path,
                "expected_blob": "c" * 40,
                "expected_mode": "100644",
                "actual_blob": "c" * 40 if matches else "d" * 40,
                "actual_mode": "100644",
                "matches": matches,
            }
            for path in exact_paths
        ],
    }


def task_commit_blocked_producer_matrix(
    plan: dict[str, object],
) -> dict[str, dict[str, object]]:
    exact_paths = sorted(str(path) for path in plan["exact_stage_paths"])
    git = plan["git"]
    message = plan["message"]
    assert isinstance(git, dict)
    assert isinstance(message, dict)
    pre_commit_head = str(git["pre_commit_head"])
    message_sha256 = str(message["sha256"])
    blocked_base: dict[str, object] = {
        "status": "blocked",
        "exit": "blocked",
        "recorded_at": "2026-01-01T00:00:00Z",
        "failure_stage": "pre-commit",
        "pre_commit_head": pre_commit_head,
        "commit_sha": pre_commit_head,
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
    commit_changed = {
        **blocked_base,
        "failure_stage": "commit",
        "commit_sha": "e" * 40,
        "head_changed": True,
        "parent": pre_commit_head,
        "message_sha256": message_sha256,
        "committed_paths": exact_paths,
        "tree_evidence": task_commit_tree_evidence(
            exact_paths, source="commit", matches=True
        ),
    }
    postcondition = {
        **commit_changed,
        "failure_stage": "postcondition",
        "errors": ["Committed message parser rejected a non-tree postcondition."],
    }
    return {
        "pre-commit before tree binding": blocked_base,
        "pre-commit after tree binding": {
            **blocked_base,
            "tree_evidence": task_commit_tree_evidence(
                exact_paths, source="index", matches=True
            ),
        },
        "commit unchanged HEAD without mutation": {
            **blocked_base,
            "failure_stage": "commit",
            "tree_evidence": task_commit_tree_evidence(
                exact_paths, source="index", matches=True
            ),
        },
        "commit unchanged HEAD with index mutation": {
            **blocked_base,
            "failure_stage": "commit",
            "hook_mutation": True,
            "tree_evidence": task_commit_tree_evidence(
                exact_paths, source="index", matches=False
            ),
        },
        "commit changed HEAD": commit_changed,
        "postcondition non-tree error": postcondition,
        "postcondition hook mutation": {
            **postcondition,
            "hook_mutation": True,
            "tree_evidence": task_commit_tree_evidence(
                exact_paths, source="commit", matches=False
            ),
        },
    }


def task_commit_schema_negative_matrix(
    plan: dict[str, object],
) -> dict[str, dict[str, object]]:
    rows = task_commit_blocked_producer_matrix(plan)
    exact_paths = sorted(str(path) for path in plan["exact_stage_paths"])
    message = plan["message"]
    assert isinstance(message, dict)

    def changed(label: str, **updates: object) -> dict[str, object]:
        return {**copy.deepcopy(rows[label]), **updates}

    return {
        "pre-commit changed HEAD": changed(
            "pre-commit before tree binding",
            commit_sha="f" * 40,
            head_changed=True,
        ),
        "pre-commit mismatched tree": changed(
            "pre-commit after tree binding",
            tree_evidence=task_commit_tree_evidence(
                exact_paths, source="index", matches=False
            ),
        ),
        "pre-commit commit-sourced tree": changed(
            "pre-commit after tree binding",
            tree_evidence=task_commit_tree_evidence(
                exact_paths, source="commit", matches=True
            ),
        ),
        "commit unchanged HEAD missing tree": changed(
            "commit unchanged HEAD without mutation", tree_evidence=None
        ),
        "commit unchanged HEAD commit-sourced tree": changed(
            "commit unchanged HEAD without mutation",
            tree_evidence=task_commit_tree_evidence(
                exact_paths, source="commit", matches=True
            ),
        ),
        "commit unchanged HEAD with created identity": changed(
            "commit unchanged HEAD without mutation",
            message_sha256=str(message["sha256"]),
            committed_paths=exact_paths,
        ),
        "commit changed HEAD missing tree": changed(
            "commit changed HEAD", tree_evidence=None
        ),
        "commit changed HEAD index-sourced tree": changed(
            "commit changed HEAD",
            tree_evidence=task_commit_tree_evidence(
                exact_paths, source="index", matches=True
            ),
        ),
        "commit changed HEAD missing message identity": changed(
            "commit changed HEAD", message_sha256=None
        ),
        "commit changed HEAD missing path identity": changed(
            "commit changed HEAD", committed_paths=[]
        ),
        "postcondition unchanged HEAD": changed(
            "postcondition non-tree error",
            commit_sha=str(plan["git"]["pre_commit_head"]),
            head_changed=False,
        ),
        "postcondition missing tree": changed(
            "postcondition non-tree error", tree_evidence=None
        ),
        "postcondition index-sourced tree": changed(
            "postcondition non-tree error",
            tree_evidence=task_commit_tree_evidence(
                exact_paths, source="index", matches=True
            ),
        ),
        "postcondition missing message identity": changed(
            "postcondition non-tree error", message_sha256=None
        ),
        "postcondition missing path identity": changed(
            "postcondition non-tree error", committed_paths=[]
        ),
    }


def task_commit_runtime_tamper_matrix(
    plan: dict[str, object],
) -> dict[str, dict[str, object]]:
    rows = task_commit_blocked_producer_matrix(plan)
    exact_paths = sorted(str(path) for path in plan["exact_stage_paths"])
    pre_commit_head = str(plan["git"]["pre_commit_head"])

    def changed(label: str, **updates: object) -> dict[str, object]:
        return {**copy.deepcopy(rows[label]), **updates}

    duplicate_path = changed("postcondition non-tree error")
    duplicate_paths = duplicate_path["tree_evidence"]["paths"]
    duplicate_paths.append(copy.deepcopy(duplicate_paths[0]))

    missing_path = changed("postcondition non-tree error")
    missing_path["tree_evidence"]["paths"].pop()

    blob_flag_conflict = changed("postcondition non-tree error")
    blob_flag_conflict["tree_evidence"]["paths"][0]["actual_blob"] = "d" * 40

    aggregate_flag_conflict = changed("postcondition non-tree error")
    aggregate_flag_conflict["tree_evidence"]["actual_tree"] = "b" * 40

    mode_mutation_flag_conflict = changed("postcondition non-tree error")
    mode_mutation_flag_conflict["tree_evidence"]["paths"][0]["actual_mode"] = "100755"
    mode_mutation_flag_conflict["tree_evidence"]["paths"][0]["matches"] = False
    mode_mutation_flag_conflict["tree_evidence"]["matches"] = False

    return {
        "pre-commit mismatched tree with hook false": changed(
            "pre-commit after tree binding",
            tree_evidence=task_commit_tree_evidence(
                exact_paths, source="index", matches=False
            ),
        ),
        "commit null tree": changed(
            "commit unchanged HEAD without mutation", tree_evidence=None
        ),
        "postcondition null tree with unchanged HEAD": changed(
            "postcondition non-tree error",
            commit_sha=pre_commit_head,
            head_changed=False,
            tree_evidence=None,
        ),
        "commit unchanged HEAD wrong source": changed(
            "commit unchanged HEAD without mutation",
            tree_evidence=task_commit_tree_evidence(
                exact_paths, source="commit", matches=True
            ),
        ),
        "postcondition clean evidence with hook true": changed(
            "postcondition non-tree error",
            hook_mutation=True,
        ),
        "pre-commit HEAD identity contradiction": changed(
            "pre-commit before tree binding", commit_sha="f" * 40
        ),
        "postcondition HEAD identity contradiction": changed(
            "postcondition non-tree error", commit_sha=pre_commit_head
        ),
        "duplicate tree path": duplicate_path,
        "missing tree path": missing_path,
        "path match flag contradicts blob equality": blob_flag_conflict,
        "aggregate tree match flag contradicts tree facts": aggregate_flag_conflict,
        "postcondition mode evidence requires hook mutation": mode_mutation_flag_conflict,
    }


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
        non_blocked_results = [
            {"status": "planned", "exit": None},
            {
                "status": "revision-required",
                "exit": "revision-required",
                "recorded_at": "2026-01-01T00:00:00Z",
                "errors": ["Candidate message requires revision."],
            },
            {
                "status": "committed",
                "exit": "committed",
                "recorded_at": "2026-01-01T00:00:00Z",
                "commit_sha": "2" * 40,
                "parent": planned["git"]["pre_commit_head"],
                "message_sha256": planned["message"]["sha256"],
                "committed_paths": planned["exact_stage_paths"],
                "unrelated_preserved": True,
                "hook_mutation": False,
                "tree_evidence": task_commit_tree_evidence(
                    planned["exact_stage_paths"], source="commit", matches=True
                ),
            },
        ]
        for result in non_blocked_results:
            with self.subTest(kind="non-blocked", status=result["status"]):
                payload = copy.deepcopy(planned)
                payload["result"] = result
                self.assertEqual(list(validator.iter_errors(payload)), [])

        for label, result in task_commit_blocked_producer_matrix(planned).items():
            with self.subTest(kind="producer-row", label=label):
                payload = copy.deepcopy(planned)
                payload["result"] = result
                self.assertEqual(list(validator.iter_errors(payload)), [])

        generic_invalid_results = [
            {"status": "blocked", "exit": "committed"},
            {"status": "committed", "exit": "committed"},
            {"status": "planned", "exit": None, "unexpected": True},
            {
                **task_commit_blocked_producer_matrix(planned)[
                    "pre-commit before tree binding"
                ],
                "errors": [],
            },
            {**non_blocked_results[-1], "hook_mutation": True},
            {
                key: value
                for key, value in non_blocked_results[-1].items()
                if key != "tree_evidence"
            },
        ]
        for result in generic_invalid_results:
            with self.subTest(kind="generic-invalid", result=result):
                payload = copy.deepcopy(planned)
                payload["result"] = result
                self.assertTrue(list(validator.iter_errors(payload)))

        for label, result in task_commit_schema_negative_matrix(planned).items():
            with self.subTest(kind="schema-negative", label=label):
                payload = copy.deepcopy(planned)
                payload["result"] = result
                self.assertTrue(list(validator.iter_errors(payload)))


if __name__ == "__main__":
    unittest.main()
