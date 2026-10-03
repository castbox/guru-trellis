from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json


PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("establish_task_identity", PACKAGE / "runtime/invoke.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TaskIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        task = self.root / ".trellis/tasks/demo"
        task.mkdir(parents=True)
        self.task_file = task / "task.json"
        self.input = {"profile": "active_task", "mode": "workflow", "task_id": "demo", "task_ref": ".trellis/tasks/demo", "lifecycle_generation": 0}

    def task(self, **fields: object) -> None:
        current = {
            "id": "demo", "name": "demo", "lifecycle_generation": 0,
            "source": {"kind": "no_issue"}, "title": "Current identity",
            "description": "Reviewed task identity", "status": "planning",
            "dev_type": None, "scope": None, "package": None, "priority": "P2",
            "createdAt": "2026-10-04", "completedAt": None,
            "base_branch": "main", "worktree_path": None, "commit": None,
            "pr_url": None, "children": [], "parent": None,
            "relatedFiles": [], "notes": "", "meta": {},
        }
        self.task_file.write_text(json.dumps({**current, **fields}), encoding="utf-8")

    def invoke(self, **fields: object) -> dict:
        result = MODULE.invoke(self.root, {**self.input, **fields})
        validate_json(result, PACKAGE / "schemas/public-output.schema.json", "output")
        return result

    def test_current_issue_and_no_issue_sources_resolve_read_only(self) -> None:
        for source in (
            {"kind": "no_issue"},
            {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 481,
             "disposition": "exact_source"},
        ):
            with self.subTest(source=source):
                self.task(source=source)
                before = self.task_file.read_bytes()
                result = self.invoke()
                self.assertEqual(result["exit_id"], "identity_established")
                self.assertEqual(result["source"], source)
                self.assertEqual(result["task_id"], "demo")
                self.assertEqual(result["lifecycle_generation"], 0)
                self.assertEqual(self.task_file.read_bytes(), before)

    def test_missing_source_is_unsupported_even_with_legacy_scope_or_review(self) -> None:
        for scope in (
            "GitHub issue: https://github.com/castbox/guru-trellis/issues/454",
            "independent task",
        ):
            with self.subTest(scope=scope):
                self.task(scope=scope)
                data = json.loads(self.task_file.read_text())
                del data["source"]
                self.task_file.write_text(json.dumps(data))
                before = self.task_file.read_bytes()
                expected = {"exit_id": "blocked", "reason_code": "unsupported_legacy_task"}
                self.assertEqual(self.invoke(), expected)
                self.assertEqual(self.invoke(reviewed_source={"kind": "no_issue"}), expected)
                self.assertEqual(self.task_file.read_bytes(), before)

    def test_incomplete_legacy_identity_is_rejected_without_rewriting(self) -> None:
        self.task_file.write_text(json.dumps({"id": "demo", "status": "planning"}))
        before = self.task_file.read_bytes()
        self.assertEqual(self.invoke(),
                         {"exit_id": "blocked", "reason_code": "unsupported_legacy_task"})
        self.assertEqual(self.task_file.read_bytes(), before)

    def test_stale_generation_or_source_override_fails_closed(self) -> None:
        self.task(lifecycle_generation=1, source={"kind": "no_issue"})
        self.assertEqual(self.invoke()["exit_id"], "invalid_task_state")
        self.task(source={"kind": "no_issue"})
        self.assertEqual(self.invoke(reviewed_source={"kind": "no_issue"})["exit_id"], "blocked")


if __name__ == "__main__":
    unittest.main()
