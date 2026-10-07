from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
sys.path.insert(0, str(PACKAGE / "runtime"))

from files import MigrationError, state, write_json
from owner import validate_task_dispositions
from runtime.task_lifecycle.errors import LifecycleContractError


class InventoryDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.current = self.root / ".trellis/tasks/current/task.json"
        write_json(self.current, {
            "id": "current", "name": "current", "title": "Current", "description": "",
            "status": "planning", "lifecycle_generation": 0, "source": {"kind": "no_issue"},
            "dev_type": None, "scope": None, "package": None, "priority": "P2",
            "createdAt": "", "completedAt": None, "base_branch": None,
            "worktree_path": None, "commit": None, "pr_url": None, "children": [],
            "parent": None, "relatedFiles": [], "notes": "", "meta": {},
        })
        self.legacy = self.root / ".trellis/tasks/deferred/task.json"
        write_json(self.legacy, {
            "id": "deferred", "name": "deferred", "title": "Deferred", "status": "planning",
            "creator": "old", "assignee": "old",
        })
        self.plan = {"core_plan": {"tasks": [], "deferred_tasks": [{
            "task_ref": ".trellis/tasks/deferred", "expected_sha256": state(self.legacy)["sha256"],
        }]}}
        for ref in (
            ".trellis/tasks/07-27-fix-profile-sheet-language-reopen",
            ".trellis/tasks/archive/2026-07/07-27-evidence",
        ):
            directory = self.root / ref
            (directory / "reviews").mkdir(parents=True)
            (directory / "evidence.jsonl").write_text('{"result":"historical"}\n')
            (directory / "reviews/check.md").write_text("Historical review\n")

    def tree_bytes(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def test_current_and_deferred_tasks_accept_unchanged_evidence_directories(self):
        before = self.tree_bytes()
        validate_task_dispositions(self.root, self.plan)
        self.assertEqual(self.tree_bytes(), before)

    def test_omitted_real_legacy_task_remains_blocking(self):
        before = self.tree_bytes()
        with self.assertRaisesRegex(MigrationError, "inventory differs"):
            validate_task_dispositions(self.root, {"core_plan": {"tasks": []}})
        self.assertEqual(self.tree_bytes(), before)

    def test_ordinary_legacy_metadata_edit_requires_fresh_disposition(self):
        data = json.loads(self.legacy.read_text())
        data["title"] = "Ordinary task update"
        write_json(self.legacy, data)
        before = self.tree_bytes()
        with self.assertRaisesRegex(MigrationError, "bytes changed"):
            validate_task_dispositions(self.root, self.plan)
        self.assertEqual(self.tree_bytes(), before)

    def test_existing_malformed_metadata_remains_blocking(self):
        for path in (self.current, self.legacy):
            original = path.read_bytes()
            try:
                for content in ("unfinished JSON", '{"id":"incomplete"}'):
                    with self.subTest(task=path.parent.name, content=content):
                        path.write_text(content)
                        # A fresh ordinary disposition must not hide invalid metadata.
                        self.plan["core_plan"]["deferred_tasks"][0]["expected_sha256"] = state(self.legacy)["sha256"]
                        before = self.tree_bytes()
                        with self.assertRaises(LifecycleContractError):
                            validate_task_dispositions(self.root, self.plan)
                        self.assertEqual(self.tree_bytes(), before)
            finally:
                path.write_bytes(original)


if __name__ == "__main__":
    unittest.main()
