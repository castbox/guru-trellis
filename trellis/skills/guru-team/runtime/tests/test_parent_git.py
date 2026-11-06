from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runtime.parent_git import ParentGitError, index_entries, parent_status_records
from runtime.reviewed_content import reviewed_content_identity


class ParentGitFactsTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.git(self.root, "init", "-qb", "main")
        self.configure(self.root)
        self.child = self.root / "module"
        self.child.mkdir()
        self.git(self.child, "init", "-q")
        self.configure(self.child)
        (self.child / "child.txt").write_text("first\n")
        self.git(self.child, "add", "child.txt")
        self.git(self.child, "commit", "-qm", "child first")
        self.oid = self.git(self.child, "rev-parse", "HEAD")
        self.git(self.root, "update-index", "--add", "--cacheinfo", f"160000,{self.oid},module")
        self.git(self.root, "commit", "-qm", "parent first")

    def tearDown(self):
        self.temporary.cleanup()

    def git(self, root, *args, input=None):
        return subprocess.run(["git", *args], cwd=root, input=input, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              check=True).stdout.strip()

    def configure(self, root):
        self.git(root, "config", "user.name", "Parent Git Test")
        self.git(root, "config", "user.email", "parent@example.invalid")

    def projected_tree_identity(self):
        tree = self.git(self.root, "write-tree")
        commit = self.git(self.root, "commit-tree", tree, "-p", "HEAD", input="projection\n")
        return reviewed_content_identity(self.root, commit=commit, include_worktree=False)

    def test_child_state_is_irrelevant_but_parent_pointer_is_content(self):
        initial = reviewed_content_identity(self.root)
        (self.child / "child.txt").write_text("dirty child\n")
        self.assertEqual([], parent_status_records(self.root))
        self.assertEqual(initial, reviewed_content_identity(self.root))
        self.git(self.child, "add", "child.txt")
        self.git(self.child, "commit", "-qm", "child second")
        next_oid = self.git(self.child, "rev-parse", "HEAD")
        self.assertEqual(initial, reviewed_content_identity(self.root))
        self.git(self.root, "update-index", "--cacheinfo", f"160000,{next_oid},module")
        self.assertEqual([("M ", "module")],
                         [(row["status_text"], row["path"]) for row in parent_status_records(self.root)])
        current = reviewed_content_identity(self.root)
        self.assertNotEqual(initial, current)
        self.assertEqual(self.projected_tree_identity(), current)
        # A parent entry remains readable without either the checkout or object.
        shutil.rmtree(self.child)
        self.git(self.root, "update-index", "--cacheinfo", f"160000,{'1'*40},module")
        self.assertEqual("1" * 40, index_entries(self.root)["module"]["oid"])
        self.assertEqual(self.projected_tree_identity(), reviewed_content_identity(self.root))

    def test_staged_delete_keeps_child_directory_out_of_parent_content(self):
        self.git(self.root, "update-index", "--force-remove", "module")
        (self.child / "extra.txt").write_text("child only\n")
        self.assertTrue(self.child.is_dir())
        rows = parent_status_records(self.root)
        self.assertEqual([("D ", "module")], [(row["status_text"], row["path"]) for row in rows])
        self.assertEqual(self.projected_tree_identity(), reviewed_content_identity(self.root))

    def test_parent_type_replacement_and_rename_are_preserved(self):
        shutil.rmtree(self.child)
        self.child.write_text("ordinary parent file\n")
        self.git(self.root, "add", "module")
        self.assertEqual("100644", index_entries(self.root)["module"]["mode"])
        self.assertEqual(self.projected_tree_identity(), reviewed_content_identity(self.root))
        self.git(self.root, "commit", "-qm", "replace")
        self.git(self.root, "mv", "module", "renamed.txt")
        row, = parent_status_records(self.root)
        self.assertEqual(("R ", "renamed.txt", "module"),
                         (row["status_text"], row["path"], row["renamed_from"]))
        self.assertEqual(self.projected_tree_identity(), reviewed_content_identity(self.root))

    def test_capture_uses_only_parent_git_commands_and_rejects_unmerged(self):
        original_run = subprocess.run
        with patch("subprocess.run", wraps=original_run) as run:
            reviewed_content_identity(self.root)
            for call in run.call_args_list:
                self.assertEqual(self.root, Path(call.kwargs["cwd"]))
                self.assertNotIn("-C", call.args[0])
        records = f"0 {self.oid}\tmodule\n160000 {self.oid} 1\tmodule\n160000 {'2'*40} 2\tmodule\n"
        self.git(self.root, "update-index", "--index-info", input=records)
        with self.assertRaises(ParentGitError):
            parent_status_records(self.root)


if __name__ == "__main__":
    unittest.main()
