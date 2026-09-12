from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[5]


class TaskStartIdentityTests(unittest.TestCase):
    def test_start_rejects_missing_or_empty_worktree_path_without_writes(self):
        for value in (None, ""):
            with self.subTest(worktree_path=value):
                with tempfile.TemporaryDirectory(prefix="guru-task-start-") as tmp:
                    root = Path(tmp)
                    subprocess.run(
                        ["git", "init", "-q"], cwd=root, check=True,
                    )
                    shutil.copytree(
                        SOURCE / ".trellis/scripts",
                        root / ".trellis/scripts",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
                    )
                    task_dir = root / ".trellis/tasks/09-12-identity"
                    task_dir.mkdir(parents=True)
                    task = {
                        "id": "identity",
                        "name": "identity",
                        "title": "Identity",
                        "status": "planning",
                        "branch": None,
                        "base_branch": "main",
                    }
                    if value is not None:
                        task["worktree_path"] = value
                    task_path = task_dir / "task.json"
                    task_path.write_text(json.dumps(task) + "\n", encoding="utf-8")
                    before = task_path.read_text(encoding="utf-8")

                    result = subprocess.run(
                        [
                            sys.executable,
                            ".trellis/scripts/task.py",
                            "start",
                            ".trellis/tasks/09-12-identity",
                            "--allow-empty-context",
                        ],
                        cwd=root,
                        text=True,
                        capture_output=True,
                        check=False,
                    )

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("worktree_path is required", result.stdout)
                    self.assertEqual(task_path.read_text(encoding="utf-8"), before)
                    self.assertFalse((root / ".trellis/.runtime").exists())


if __name__ == "__main__":
    unittest.main()
