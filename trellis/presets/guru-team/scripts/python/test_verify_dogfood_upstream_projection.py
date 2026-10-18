from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from verify_dogfood_upstream_projection import check_projection


REPO = Path(__file__).resolve().parents[5]


class DogfoodTaskBehaviorTests(unittest.TestCase):
    """Exercise the actual dogfood scripts, with no supplied Fork substitute."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="guru-dogfood-task-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.scripts = self.root / ".trellis/scripts"
        shutil.copytree(
            REPO / ".trellis/scripts", self.scripts,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        # A fixture has no session authority from the invoking model process.
        self.env = {
            k: v for k, v in os.environ.items()
            if not k.startswith(("TRELLIS_", "CODEX_", "CLAUDE_", "CURSOR_", "GIT_"))
        }
        self.env["PYTHONDONTWRITEBYTECODE"] = "1"

    def run_script(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.scripts / name), *args],
            cwd=self.root, env=self.env, text=True, capture_output=True, check=False,
        )

    def create(self, source: dict | None = None) -> dict:
        args = ["create", "Projection behavior", "--slug", "projection-behavior",
                "--task-id", "projection-behavior", "--description",
                "Prove actual dogfood task contract", "--base-branch", "main", "--no-start"]
        if source is not None:
            args += ["--source-json", json.dumps(source)]
        result = self.run_script("task.py", *args)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        files = list((self.root / ".trellis/tasks").glob("*/task.json"))
        self.assertEqual(len(files), 1)
        data = json.loads(files[0].read_text())
        self.assertNotIn("creator", data)
        self.assertNotIn("assignee", data)
        return data

    def test_no_issue_create_without_personnel(self) -> None:
        data = self.create()
        self.assertEqual(data["id"], "projection-behavior")
        self.assertEqual(data["source"], {"kind": "no_issue"})
        self.assertEqual(data["lifecycle_generation"], 0)

    def test_issue_create_without_personnel(self) -> None:
        source = {"kind": "issue", "repo_ref": "castbox/guru-trellis",
                  "number": 481, "disposition": "exact_source"}
        self.assertEqual(self.create(source)["source"], source)

    def test_reference_only_create_preserves_disposition(self) -> None:
        source = {"kind": "issue", "repo_ref": "castbox/guru-trellis",
                  "number": 490, "disposition": "reference_only"}
        self.assertEqual(self.create(source)["source"], source)

    def test_list_and_context_contain_task_without_personnel(self) -> None:
        self.create()
        listed = self.run_script("task.py", "list", "--json")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        items = json.loads(listed.stdout)["tasks"]
        self.assertEqual([item["id"] for item in items], ["projection-behavior"])
        for item in items:
            self.assertNotIn("creator", item)
            self.assertNotIn("assignee", item)
        context_json = self.run_script("get_context.py", "--json")
        self.assertEqual(context_json.returncode, 0, context_json.stderr)
        active = json.loads(context_json.stdout)["tasks"]["active"]
        self.assertEqual(len(active), 1)
        self.assertNotIn("assignee", active[0])
        self.assertNotIn("creator", active[0])
        context_text = self.run_script("get_context.py")
        self.assertEqual(context_text.returncode, 0, context_text.stderr)
        section = context_text.stdout.split("## PROJECT TASKS", 1)[1]
        self.assertIn("projection-behavior/ (planning)", section)
        self.assertNotIn("@", section.split("##", 1)[0])

    def test_retired_create_and_list_arguments_are_rejected(self) -> None:
        commands = [
            ("create", "Old request", "--description", "Old args", "--no-start",
             "--creator", "alice"),
            ("create", "Old request", "--description", "Old args", "--no-start",
             "--assignee", "bob"),
            ("list", "--assignee", "bob"),
        ]
        for args in commands:
            with self.subTest(args=args):
                result = self.run_script("task.py", *args)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("unrecognized arguments", result.stderr)
                self.assertFalse((self.root / ".trellis/tasks").exists())


class OfficialProjectionChecks(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="guru-official-projection-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / ".trellis").mkdir()
        (self.root / ".trellis/.version").write_text("0.7.0-castbox.1\n")
        self.current_hash = hashlib.sha256(b"current official task template\n").hexdigest()
        self.old_hash = hashlib.sha256(b"previous official task template\n").hexdigest()
        self.path = ".trellis/scripts/task.py"
        self.projection = {
            "rows": [{"path": self.path, "template_hash": self.current_hash,
                      "installed_hash": self.current_hash}],
            "excluded_paths": [".codex/config.toml"],
        }
        self.write_hashes({self.path: self.current_hash})

    def write_hashes(self, hashes: dict) -> None:
        (self.root / ".trellis/.template-hashes.json").write_text(
            json.dumps({"__version": 2, "hashes": hashes})
        )

    def check(self) -> dict:
        return check_projection(self.root, self.projection, "0.7.0-castbox.1")

    def test_current_projection_and_custom_surfaces(self) -> None:
        # Guru workflow and local config must not become official hash objects.
        (self.root / ".trellis/workflow.md").write_text("custom Guru workflow\n")
        (self.root / ".codex").mkdir()
        (self.root / ".codex/config.toml").write_text("custom local config\n")
        result = self.check()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["checked_file_count"], 1)
        self.assertEqual(result["excluded_editable_paths"], [".codex/config.toml"])

    def test_old_projection_rejected_even_when_hash_matches_installed_bytes(self) -> None:
        # A version-lock change plus old locally consistent template hashes was
        # the missed validation boundary; expected Fork bytes must also match.
        self.projection["rows"][0]["installed_hash"] = self.old_hash
        self.write_hashes({self.path: self.old_hash})
        result = self.check()
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["errors"], [
            {"code": "official_projection_drift", "path": self.path},
            {"code": "official_template_hash_drift", "path": self.path},
        ])

    def test_missing_file_and_old_version_are_reported(self) -> None:
        self.projection["rows"][0]["installed_hash"] = None
        (self.root / ".trellis/.version").write_text("0.6.17\n")
        self.assertEqual(self.check()["errors"], [
            {"code": "missing_official_file", "path": self.path},
            {"code": "official_version_drift", "path": ".trellis/.version"},
        ])

    def test_retired_module_is_rejected_without_reading_historical_roots(self) -> None:
        retired = ".trellis/scripts/common/history_paths.py"
        (self.root / retired).parent.mkdir(parents=True)
        (self.root / retired).write_text("previous official module\n")
        history = self.root / ".trellis/workspace/retired-user/journal.md"
        history.parent.mkdir(parents=True)
        history.write_text("historical bytes remain outside the validator\n")
        self.write_hashes({self.path: self.current_hash, retired: self.old_hash})
        self.assertEqual(self.check()["errors"], [
            {"code": "retired_official_file", "path": retired},
            {"code": "retired_official_hash", "path": retired},
        ])
        self.assertEqual(history.read_text(), "historical bytes remain outside the validator\n")


if __name__ == "__main__":
    unittest.main()
