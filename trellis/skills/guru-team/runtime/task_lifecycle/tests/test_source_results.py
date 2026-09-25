from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.closure_result import read_terminal_closure_result
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.results import reason, result_ref, task_artifact, task_identity, task_lifecycle, transaction_ref
from runtime.task_lifecycle.source import normalize_branch_ref, normalize_delivery_target, normalize_repo_ref, normalize_source, task_source


class SourceAndResultTests(unittest.TestCase):
    def test_terminal_closure_reader_retains_frozen_source(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
            repository = inspect_repository(root)
            result = {"task_id": "demo", "lifecycle_generation": 0, "result_id": "closure:demo"}
            frozen_source = {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454,
                             "disposition": "reference_only"}
            transaction = {"ref": result, "frozen": {"action_set": [], "source": frozen_source},
                           "terminal": "no_mutation"}
            path = repository.common_dir / "guru-team/closure/demo/0.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(transaction))
            self.assertEqual(read_terminal_closure_result(repository, result)["source"], frozen_source)

    def test_issue_and_no_issue_sources_are_the_only_shapes(self):
        self.assertEqual(normalize_source({"kind": "no_issue"}), {"kind": "no_issue"})
        self.assertEqual(
            normalize_source({"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454, "disposition": "reference_only"}),
            {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454, "disposition": "reference_only"},
        )
        for invalid in [
            {},
            {"kind": "no_issue", "repo_ref": "castbox/guru-trellis"},
            {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": True},
            {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 0},
            {"kind": "issue", "repo_ref": "/tmp/repo", "number": 454},
            {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454},
            {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454, "disposition": "unknown"},
            {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454, "disposition": []},
        ]:
            with self.subTest(invalid=invalid), self.assertRaises(LifecycleContractError):
                normalize_source(invalid)

    def test_only_exact_legacy_issue_scope_normalizes_without_writing(self):
        expected = {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454, "disposition": "exact_source"}
        self.assertEqual(task_source({"scope": "GitHub issue: https://github.com/castbox/guru-trellis/issues/454"}), expected)
        for scope in ["related to #454", "GitHub issue: https://github.com/castbox/guru-trellis/issues/454/", None]:
            with self.subTest(scope=scope), self.assertRaises(LifecycleContractError):
                task_source({"scope": scope})

    def test_delivery_target_is_portable_and_head_free(self):
        self.assertEqual(
            normalize_delivery_target({"repo_ref": "castbox/guru-trellis", "branch_ref": "main"}),
            {"repo_ref": "castbox/guru-trellis", "branch_ref": "main"},
        )
        for invalid in [
            {"repo_ref": "castbox/guru-trellis", "branch_ref": "main", "head": "a" * 40},
            {"repo_ref": "castbox/guru-trellis", "branch_ref": "refs/remotes/origin/main"},
            {"repo_ref": "castbox/guru-trellis", "branch_ref": "../main"},
            {"repo_ref": "castbox/guru-trellis", "branch_ref": "main."},
            {"repo_ref": "castbox/guru-trellis", "branch_ref": "topic@{1}"},
        ]:
            with self.subTest(invalid=invalid), self.assertRaises(LifecycleContractError):
                normalize_delivery_target(invalid)

    def test_repository_and_branch_refs_match_portable_git_domains(self):
        for value in ["castbox/guru-trellis", "Owner_1/repo.name", "a/b.git-tools"]:
            self.assertEqual(normalize_repo_ref(value), value)
        for value in ["owner/repo.git", "../repo", "./repo", "owner/-repo", "_owner/repo"]:
            with self.subTest(value=value), self.assertRaises(LifecycleContractError):
                normalize_repo_ref(value)

        for value in ["main", "refs/heads/topic", "topic@", "foo/-bar", "@"]:
            self.assertEqual(normalize_branch_ref(value), value)
        for value in [
            "task.lock",
            "foo/.bar",
            "foo.lock",
            "foo.lock/bar",
            "HEAD",
            "-foo",
            "guru-task-lifecycle/task-a",
            "refs/heads/guru-task-lifecycle/task-a",
        ]:
            with self.subTest(value=value), self.assertRaises(LifecycleContractError):
                normalize_branch_ref(value)

    def test_named_dto_constructors_return_minimal_closed_payloads(self):
        task_id = "demo"
        task_ref = ".trellis/tasks/09-20-demo"
        self.assertEqual(task_identity(task_id, task_ref), {"task_id": task_id, "task_ref": task_ref})
        self.assertEqual(task_lifecycle(task_id, 0), {"task_id": task_id, "lifecycle_generation": 0})
        self.assertEqual(task_artifact(task_id, task_ref, 0), {"task_id": task_id, "task_ref": task_ref, "lifecycle_generation": 0})
        self.assertEqual(result_ref(task_id, 0, "result:1")["result_id"], "result:1")
        self.assertEqual(transaction_ref(task_id, 0, "transaction:1", "result:1")["transaction_id"], "transaction:1")
        self.assertEqual(reason("stale_authority", ["task:demo"])["reason_code"], "stale_authority")

    def test_result_constructors_reject_bool_generation_and_absolute_task_ref(self):
        with self.assertRaises(LifecycleContractError):
            task_lifecycle("demo", True)
        with self.assertRaises(LifecycleContractError):
            task_artifact("demo", "/tmp/task", 0)


if __name__ == "__main__":
    unittest.main()
