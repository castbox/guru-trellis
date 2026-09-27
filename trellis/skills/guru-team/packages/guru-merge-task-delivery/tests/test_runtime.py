from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest import mock


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
spec = importlib.util.spec_from_file_location("merge_delivery_owner", PACKAGE / "runtime/owner.py")
assert spec and spec.loader
OWNER = importlib.util.module_from_spec(spec)
spec.loader.exec_module(OWNER)
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository


class RuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".git").mkdir()
        self.public = {
            "profile": "ready_for_merge", "mode": "workflow",
            "task_ref": ".trellis/tasks/current", "delivery_cycle_ref": "delivery-cycle:v1:" + "a" * 64,
            "repo_ref": "example/repo", "pr_number": 27,
            "expected_head_sha": "1" * 40,
            "publication_body_sha256": hashlib.sha256(b"Refs #27").hexdigest(),
        }
        self.review = {
            "dimensions": [
                {"id": name, "status": "passed", "summary": "Current dimension reviewed."}
                for name in OWNER.DIMENSIONS
            ],
            "route": {
                "typed_exit": "delivered", "merge_method": "merge",
                "merge_message": {
                    "subject": "chore(merge): 合并 #27 当前 Delivery",
                    "body": (
                        "交付当前已审核切片，剩余工作继续留在活动任务。\n\n"
                        "Guru-Task-Identity: current\n"
                        "Guru-Delivery-Schema: 1\n"
                        f"Guru-Delivery-Head: {'1' * 40}"
                    ),
                },
            },
        }
        self.input = self.write("input.json", self.public)
        self.review_path = self.write("review.json", self.review)

    def write(self, name: str, value: dict) -> Path:
        path = self.root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def facts(self, *, merged: bool) -> dict:
        merge_sha = "4" * 40 if merged else None
        facts = {
            "task": {"task_ref": self.public["task_ref"], "stable_task_id": "current", "lifecycle_generation": 0, "status": "in_progress", "branch": "feat/current", "base_branch": "main", "head_sha": "1" * 40},
            "pr": {"number": 27, "url": "https://github.com/example/repo/pull/27", "state": "MERGED" if merged else "OPEN", "is_draft": False, "head_sha": "1" * 40, "head_branch": "feat/current", "base_branch": "main", "body": "Refs #27", "merged_at": "2026-09-18T01:00:00Z" if merged else None, "merge_commit_sha": merge_sha, "mergeable": "MERGEABLE", "merge_state_status": "CLEAN", "review_decision": "APPROVED", "checks": []},
            "repository_policy": {"allow_merge_commit": True, "allow_squash_merge": True, "allow_rebase_merge": True},
            "base_ref": {"name": "main", "head_sha": merge_sha or "3" * 40},
            "merge_commit": None,
            "objective_blockers": [],
        }
        if merged:
            message = self.review["route"]["merge_message"]
            facts["merge_commit"] = {"sha": merge_sha, "message": message["subject"] + "\n\n" + message["body"], "parents": ["3" * 40, "1" * 40]}
        facts["facts_sha256"] = OWNER.digest(facts)
        return facts

    def args(self) -> Namespace:
        return Namespace(root=str(self.root), input=str(self.input), review_input=str(self.review_path))

    def test_task_facts_uses_live_binding_without_retired_task_fields(self) -> None:
        repo = self.root / "live"
        repo.mkdir()
        def git(*args: str) -> str:
            result = subprocess.run(["git", *args], cwd=repo, text=True, check=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.strip()
        git("init", "-q", "-b", "feat/current")
        git("config", "user.name", "Task Test")
        git("config", "user.email", "task@example.invalid")
        (repo / "README.md").write_text("test\n")
        git("add", "README.md")
        git("commit", "-qm", "base")
        task_dir = repo / self.public["task_ref"]
        task_dir.mkdir(parents=True)
        (task_dir / "task.json").write_text(json.dumps({
            "id": "current", "status": "in_progress", "base_branch": "main",
            "lifecycle_generation": 0,
        }))
        store = BranchBindingStore(inspect_repository(repo))
        key = TaskLifecycleKey("current", 0)
        with self.assertRaises(OWNER.CommandError) as missing:
            OWNER.task_facts(repo, self.public)
        self.assertEqual("stale_identity", missing.exception.code)
        store.establish(key, "feat/current")
        self.assertEqual("feat/current", OWNER.task_facts(repo, self.public)["branch"])
        binding = store.read(key)
        assert binding is not None
        stale = binding.as_dict()
        stale["branch_name"] = "feat/other"
        store.path_for(key).write_text(json.dumps(stale))
        with self.assertRaises(OWNER.CommandError) as wrong:
            OWNER.task_facts(repo, self.public)
        self.assertEqual("stale_identity", wrong.exception.code)

    def test_first_delivery_performs_one_mutation_and_projects_minimal_result(self) -> None:
        pre, post = self.facts(merged=False), self.facts(merged=True)
        with mock.patch.object(OWNER, "live_facts", side_effect=[pre, post]) as reads, mock.patch.object(OWNER, "run_merge") as mutation:
            result = OWNER.cmd_invoke(PACKAGE, self.args())
        artifact = {"task_id": "current", "task_ref": self.public["task_ref"], "lifecycle_generation": 0}
        self.assertEqual(result, {"exit_id": "delivered", "task_artifact": artifact, "merge_result": {
            **artifact, "delivery_cycle_ref": self.public["delivery_cycle_ref"], "repo_ref": "example/repo",
            "pr_number": 27, "reviewed_head": "1" * 40, "merge_commit_sha": "4" * 40,
            "result_id": "merge:" + "4" * 40,
        }})
        mutation.assert_called_once()
        self.assertEqual(reads.call_count, 2)
        self.assertFalse(OWNER.gate_path(self.root, self.public).exists())

    def test_terminal_output_loss_recovers_without_second_mutation(self) -> None:
        terminal = self.facts(merged=True)
        with mock.patch.object(OWNER, "live_facts", return_value=terminal), mock.patch.object(OWNER, "run_merge") as mutation:
            first = OWNER.cmd_invoke(PACKAGE, self.args())
            second = OWNER.cmd_invoke(PACKAGE, self.args())
        self.assertEqual(first, second)
        mutation.assert_not_called()

    def test_terminal_output_loss_recovers_after_target_base_advances(self) -> None:
        terminal = self.facts(merged=True)
        advanced = self.facts(merged=True)
        advanced["base_ref"]["head_sha"] = "5" * 40
        advanced["facts_sha256"] = OWNER.digest({k: v for k, v in advanced.items() if k != "facts_sha256"})
        comparison = {
            "status": "ahead",
            "merge_base_commit": {"sha": "4" * 40},
            "head_commit": {"sha": "5" * 40},
        }
        with mock.patch.object(OWNER, "live_facts", side_effect=[terminal, advanced]), \
                mock.patch.object(OWNER, "gh_json", return_value=comparison) as compare, \
                mock.patch.object(OWNER, "run_merge") as mutation:
            first = OWNER.cmd_invoke(PACKAGE, self.args())
            second = OWNER.cmd_invoke(PACKAGE, self.args())
        self.assertEqual(first, second)
        mutation.assert_not_called()
        compare.assert_called_once_with(
            self.root.resolve(), ["api", f"repos/example/repo/compare/{'4' * 40}...{'5' * 40}"],
            "target base ancestry",
        )

        comparison["merge_base_commit"]["sha"] = "3" * 40
        with mock.patch.object(OWNER, "live_facts", return_value=advanced), \
                mock.patch.object(OWNER, "gh_json", return_value=comparison), \
                mock.patch.object(OWNER, "run_merge") as mutation:
            with self.assertRaises(OWNER.CommandError) as rejected:
                OWNER.cmd_invoke(PACKAGE, self.args())
        self.assertEqual(rejected.exception.code, "stale_identity")
        mutation.assert_not_called()

    def test_retained_gate_recovers_completed_mutation_without_repeating_it(self) -> None:
        pre, terminal = self.facts(merged=False), self.facts(merged=True)
        gate = OWNER.build_gate(self.public, pre, self.review)
        OWNER.write_gate(PACKAGE, self.root, gate)
        with mock.patch.object(OWNER, "live_facts", return_value=terminal), mock.patch.object(OWNER, "run_merge") as mutation:
            result = OWNER.cmd_invoke(PACKAGE, self.args())
        self.assertEqual(result["exit_id"], "delivered")
        mutation.assert_not_called()
        self.assertFalse(OWNER.gate_path(self.root, self.public).exists())

    def test_nonmerge_routes_never_mutate_and_keep_closed_dtos(self) -> None:
        facts = self.facts(merged=False)
        cases = [
            ({"typed_exit": "merge_blocked", "reason_code": "provider_blocked", "remediation": "Retry after provider recovery."}, "merge_blocked"),
            ({"typed_exit": "implementation_required", "finding_refs": ["finding:1"]}, "implementation_required"),
            ({"typed_exit": "review_refresh_required", "reason_code": "delivery_review_stale"}, "review_refresh_required"),
        ]
        for route, expected in cases:
            review = json.loads(json.dumps(self.review))
            review["dimensions"][0]["status"] = "blocked"
            review["route"] = route
            self.review_path.write_text(json.dumps(review))
            with self.subTest(exit=expected), mock.patch.object(OWNER, "live_facts", return_value=facts), mock.patch.object(OWNER, "run_merge") as mutation:
                output = OWNER.cmd_invoke(PACKAGE, self.args())
            self.assertEqual(output["exit_id"], expected)
            mutation.assert_not_called()
        self.assertEqual(output, {"exit_id": "review_refresh_required", "task_ref": self.public["task_ref"], "reason_code": "delivery_review_stale"})

    def test_exact_trailers_and_refs_only_body_are_required(self) -> None:
        facts = self.facts(merged=False)
        changed = json.loads(json.dumps(self.review))
        changed["route"]["merge_message"]["body"] = changed["route"]["merge_message"]["body"].replace("Guru-Delivery-Schema: 1", "Guru-Delivery-Schema: 2")
        with self.assertRaises(OWNER.CommandError):
            OWNER.validate_route(self.public, facts, changed)
        closing = json.loads(json.dumps(facts))
        closing["pr"]["body"] = "Closes #27"
        self.assertIsNotNone(OWNER.CLOSING_KEYWORD.search(closing["pr"]["body"]))
        self.assertIsNone(OWNER.CLOSING_KEYWORD.search("Fix the validation described in #27"))

    def test_unsupported_policy_blocks_before_mutation(self) -> None:
        facts = self.facts(merged=False)
        facts["repository_policy"]["allow_merge_commit"] = False
        facts["objective_blockers"] = ["unsupported_delivery_merge_policy"]
        facts["facts_sha256"] = OWNER.digest({k: v for k, v in facts.items() if k != "facts_sha256"})
        with self.assertRaises(OWNER.CommandError):
            OWNER.validate_route(self.public, facts, self.review)

    def test_terminal_recovery_ignores_current_merge_method_policy(self) -> None:
        terminal = self.facts(merged=True)
        terminal["repository_policy"]["allow_merge_commit"] = False
        terminal["objective_blockers"] = OWNER.objective_blockers(
            terminal["pr"], terminal["repository_policy"]
        )
        terminal["facts_sha256"] = OWNER.digest(
            {key: value for key, value in terminal.items() if key != "facts_sha256"}
        )
        self.assertEqual(terminal["objective_blockers"], [])
        with mock.patch.object(OWNER, "live_facts", return_value=terminal), mock.patch.object(OWNER, "run_merge") as mutation:
            output = OWNER.cmd_invoke(PACKAGE, self.args())
        self.assertEqual(output["exit_id"], "delivered")
        mutation.assert_not_called()


if __name__ == "__main__":
    unittest.main()
