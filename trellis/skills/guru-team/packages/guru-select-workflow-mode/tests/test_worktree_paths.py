from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
from runtime.worktree_paths import resolve_worktree_paths
from runtime import worktree_paths
from runtime.task_lifecycle.errors import LifecycleContractError


class WorktreePathTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name).resolve()
        self.primary = self.directory / "project"
        self.primary.mkdir()
        self.git(self.primary, "init", "-q", "-b", "main")
        self.git(self.primary, "config", "user.name", "Test")
        self.git(self.primary, "config", "user.email", "test@example.invalid")
        self.git(self.primary, "commit", "--allow-empty", "-qm", "fixture")
        self.linked = self.directory / "linked"
        self.git(self.primary, "worktree", "add", "-q", "--detach", str(self.linked))

    def git(self, root, *arguments):
        return subprocess.check_output(["git", *arguments], cwd=root, text=True).strip()

    def config(self, root, value):
        path = root / ".trellis/guru-team/config.yml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("worktree_root: " + value + "\n")

    def test_project_roots_and_nonempty_linked_conflict(self):
        for value, expected in [("", self.directory / "project-worktrees"),
                                ("'../shared space'", self.directory / "shared space"),
                                (json.dumps(str(self.directory / 'absolute')), self.directory / 'absolute')]:
            with self.subTest(value=value):
                self.config(self.primary, value)
                self.config(self.linked, "''")
                self.assertEqual(resolve_worktree_paths(self.primary).worktree_root, expected)
                self.assertEqual(resolve_worktree_paths(self.linked).worktree_root, expected)
        self.config(self.linked, "../another")
        with self.assertRaises(LifecycleContractError) as raised:
            resolve_worktree_paths(self.linked)
        self.assertEqual(raised.exception.code, "worktree_config_conflict")

    def test_separate_git_directory_requires_verified_primary(self):
        primary = self.directory / "separate"
        metadata = self.directory / "metadata"
        self.git(self.directory, "init", "-q", "-b", "main", "--separate-git-dir", str(metadata), str(primary))
        self.git(primary, "config", "user.name", "Test")
        self.git(primary, "config", "user.email", "test@example.invalid")
        self.git(primary, "commit", "--allow-empty", "-qm", "fixture")
        linked = self.directory / "separate-linked"
        self.git(primary, "worktree", "add", "-q", "--detach", str(linked))
        self.assertEqual(resolve_worktree_paths(primary).primary_root, primary)
        with self.assertRaises(LifecycleContractError) as raised:
            resolve_worktree_paths(linked)
        self.assertEqual(raised.exception.code, "primary_anchor_unavailable")
        self.git(primary, "config", "core.worktree", str(primary))
        self.assertEqual(resolve_worktree_paths(linked).primary_root, primary)
        self.git(primary, "config", "core.worktree", str(self.primary))
        with self.assertRaises(LifecycleContractError) as raised:
            resolve_worktree_paths(linked)
        self.assertEqual(raised.exception.code, "primary_anchor_unavailable")

    def test_verified_primary_does_not_inspect_unrelated_linked_peers(self):
        peers = [self.directory / f"peer-{index}" for index in range(3)]
        for peer in peers:
            self.git(self.primary, "worktree", "add", "-q", "--detach", str(peer))
        for start in (self.primary, self.linked):
            with self.subTest(start=start), patch.object(worktree_paths, "inspect_repository", wraps=worktree_paths.inspect_repository) as inspected:
                self.assertEqual(resolve_worktree_paths(start).primary_root, self.primary)
                self.assertTrue(all(Path(call.args[0]) in {start, self.primary} for call in inspected.call_args_list))
                self.assertEqual(sum(Path(call.args[0]) == start for call in inspected.call_args_list), 1)

    def test_task_free_public_preflight_then_ordinary_git(self):
        self.config(self.primary, "'../task free # locations'")
        self.config(self.linked, "")
        # Only external GitHub facts are isolated; path discovery and Git are real.
        binary = self.directory / "bin"
        binary.mkdir()
        gh = binary / "gh"
        gh.write_text("#!/bin/sh\nexit 0\n")
        gh.chmod(0o755)
        environment = {**os.environ, "PATH": str(binary) + os.pathsep + os.environ["PATH"]}
        expected = self.directory / "task free # locations" / "bounded-change"

        def preflight(target):
            process = subprocess.run(["bash", str(PACKAGE / "scripts/check-env.sh"), "--root", str(self.linked),
                "--worktree-name", "bounded-change", "--checkout-root", str(target), "--json"],
                text=True, capture_output=True, env=environment)
            return process, json.loads(process.stdout)

        before = (self.git(self.primary, "worktree", "list", "--porcelain"), self.git(self.primary, "show-ref"))
        process, error = preflight(self.directory / "wrong")
        self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
        self.assertEqual(error["code"], "configured_checkout_mismatch")
        self.assertEqual((self.git(self.primary, "worktree", "list", "--porcelain"), self.git(self.primary, "show-ref")), before)
        process, receipt = preflight(expected)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertFalse(receipt["formal_exit"])
        result = receipt["result"]
        self.assertEqual(result["primary_root"], str(self.primary))
        self.assertEqual(result["checkout_root"], str(expected))
        self.git(self.linked, "worktree", "add", "-q", "-b", "task-free-change", result["checkout_root"])
        self.assertEqual(self.git(expected, "rev-parse", "--show-toplevel"), str(expected))
        self.assertIn("worktree " + str(expected), self.git(self.primary, "worktree", "list", "--porcelain"))
        self.assertEqual(resolve_worktree_paths(expected).worktree_root, expected.parent)
        self.assertFalse((expected / ".trellis/tasks").exists())
        self.assertFalse((self.primary / ".git/trellis").exists())


if __name__ == "__main__":
    unittest.main()
