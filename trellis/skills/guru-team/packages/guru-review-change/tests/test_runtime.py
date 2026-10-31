from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
PROVIDER = PACKAGE.parents[4]


class ReadOnlyReviewRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="guru-review-change-")
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name).resolve()
        self.git("init", "-q")
        self.git("config", "user.email", "review@example.invalid")
        self.git("config", "user.name", "Review fixture")
        self.write("src/with space.txt", "original\n")
        self.write("other.txt", "other\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Initial fixture")
        self.initial = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], text=True)

    def write(self, relative, content):
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def public_input(self, **extra):
        return {"profile": "working_tree", "mode": "standalone", "repository": str(self.repo), **extra}

    def call(self, wrapper, payload, expected=0):
        flag = "--input" if wrapper == "capture" else "--invocation"
        result = subprocess.run(
            [str(PACKAGE / f"scripts/{wrapper}.sh"), flag, "-"],
            input=json.dumps(payload), text=True, capture_output=True,
            # The launcher must resolve relative targets from its provider root.
            cwd=self.repo,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def capture(self, public_input=None):
        receipt = self.call("capture", public_input or self.public_input())
        self.assertFalse(receipt["formal_exit"])
        return receipt["result"]

    def invoke(self, public_input, snapshot, expected=0):
        return self.call("invoke", {
            "schema_version": "1.0", "public_input": public_input,
            "owner_result": {"exit_id": "reviewed", "snapshot": snapshot},
        }, expected)

    def state(self):
        return {
            str(path.relative_to(self.repo)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in self.repo.rglob("*") if path.is_file()
        }

    def test_plain_repository_and_read_only_reviewed_exit(self):
        self.write("src/with space.txt", "changed\n")
        self.write("new.txt", "untracked\n")
        before = self.state()
        public_input = self.public_input()
        snapshot = self.capture(public_input)
        self.assertEqual(snapshot["repository_root"], str(self.repo))
        self.assertEqual(self.invoke(public_input, snapshot), {"exit_id": "reviewed"})
        self.assertEqual(before, self.state())
        self.assertFalse((self.repo / ".trellis").exists())

    def test_unborn_repository_supports_staged_unstaged_and_untracked(self):
        self.repo = self.repo / "new repository"
        self.repo.mkdir()
        self.git("init", "-q")
        self.write("new tracked.txt", "staged\n")
        self.git("add", "new tracked.txt")
        self.write("new tracked.txt", "unstaged\n")
        self.write("new untracked.txt", "untracked\n")
        before = self.state()
        public_input = self.public_input()
        snapshot = self.capture(public_input)
        self.assertIsNone(snapshot["base_oid"])
        self.assertIsNone(snapshot["head_oid"])
        self.assertEqual(self.invoke(public_input, snapshot), {"exit_id": "reviewed"})
        self.assertEqual(before, self.state())
        self.write("new untracked.txt", "later\n")
        self.assertEqual(self.invoke(public_input, snapshot, 3)["code"], "stale_identity")

    def test_staged_and_unstaged_versions_are_separate(self):
        public_input = self.public_input()
        original = self.capture(public_input)
        self.write("src/with space.txt", "staged\n")
        self.git("add", "src/with space.txt")
        staged = self.capture(public_input)
        self.assertNotEqual(original, staged)
        self.write("src/with space.txt", "original\n")
        split = self.capture(public_input)
        self.assertNotEqual(split, original)
        self.assertNotEqual(split, staged)
        self.assertEqual(self.invoke(public_input, split), {"exit_id": "reviewed"})
        self.write("src/with space.txt", "new unstaged\n")
        self.assertEqual(self.invoke(public_input, split, 3)["code"], "stale_identity")

    def test_untracked_content_and_mode_are_bound(self):
        self.write("new.txt", "one\n")
        public_input = self.public_input()
        snapshot = self.capture(public_input)
        self.write("new.txt", "two\n")
        self.assertEqual(self.invoke(public_input, snapshot, 3)["code"], "stale_identity")
        snapshot = self.capture(public_input)
        (self.repo / "new.txt").chmod(0o755)
        self.assertNotEqual(snapshot, self.capture(public_input))

    def test_literal_directory_scope_and_unrelated_changes(self):
        public_input = self.public_input(paths=["src"])
        self.write("src/with space.txt", "selected\n")
        snapshot = self.capture(public_input)
        self.write("other.txt", "outside\n")
        self.write("outside new.txt", "outside untracked\n")
        self.assertEqual(snapshot, self.capture(public_input))
        self.assertEqual(self.invoke(public_input, snapshot), {"exit_id": "reviewed"})
        self.write("src/new file.txt", "inside\n")
        self.assertEqual(self.invoke(public_input, snapshot, 3)["code"], "stale_identity")

    def test_paths_with_spaces_and_git_metacharacters_are_literal(self):
        self.write("[name].txt", "selected\n")
        self.write("n.txt", "unrelated\n")
        public_input = self.public_input(paths=["[name].txt", "src/with space.txt"])
        snapshot = self.capture(public_input)
        self.write("n.txt", "still unrelated\n")
        self.assertEqual(snapshot, self.capture(public_input))
        self.write("[name].txt", "new selected\n")
        self.assertNotEqual(snapshot, self.capture(public_input))

    def test_root_directory_selection_includes_all_changes(self):
        public_input = self.public_input(paths=["."])
        snapshot = self.capture(public_input)
        self.write("src/with space.txt", "selected tracked\n")
        changed = self.capture(public_input)
        self.assertNotEqual(snapshot, changed)
        self.write("new.txt", "selected untracked\n")
        self.assertNotEqual(changed, self.capture(public_input))

    def test_untracked_symlink_binds_link_content(self):
        path = self.repo / "link.txt"
        path.symlink_to("other.txt")
        public_input = self.public_input(paths=["link.txt"])
        snapshot = self.capture(public_input)
        self.write("other.txt", "unselected target change\n")
        self.assertEqual(snapshot, self.capture(public_input))
        path.unlink()
        path.symlink_to("src/with space.txt")
        self.assertNotEqual(snapshot, self.capture(public_input))

    def test_deleted_and_renamed_content(self):
        public_input = self.public_input(paths=["src"])
        snapshot = self.capture(public_input)
        self.git("mv", "src/with space.txt", "src/renamed.txt")
        renamed = self.capture(public_input)
        self.assertNotEqual(snapshot, renamed)
        (self.repo / "src/renamed.txt").unlink()
        self.assertNotEqual(renamed, self.capture(public_input))

    def test_committed_range_ignores_dirty_content_but_tracks_refs(self):
        self.write("src/with space.txt", "committed\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Candidate fixture")
        public_input = self.public_input(profile="committed_range", base=self.initial, head="HEAD")
        snapshot = self.capture(public_input)
        self.write("src/with space.txt", "dirty\n")
        self.write("new.txt", "untracked\n")
        self.assertEqual(snapshot, self.capture(public_input))
        self.assertEqual(self.invoke(public_input, snapshot), {"exit_id": "reviewed"})
        self.git("add", ".")
        self.git("commit", "-qm", "Later fixture")
        self.assertEqual(self.invoke(public_input, snapshot, 3)["code"], "stale_identity")

    def test_direct_range_does_not_require_ancestry(self):
        self.git("checkout", "-qb", "left")
        self.write("left.txt", "left\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Left fixture")
        left = self.git("rev-parse", "HEAD").strip()
        self.git("checkout", "-qb", "right", self.initial)
        self.write("right.txt", "right\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Right fixture")
        public_input = self.public_input(profile="committed_range", base=left, head="HEAD")
        snapshot = self.capture(public_input)
        self.assertEqual(snapshot["base_oid"], left)
        self.assertEqual(self.invoke(public_input, snapshot), {"exit_id": "reviewed"})

    def test_relative_repository_uses_provider_root(self):
        absolute = self.public_input()
        relative = self.public_input(repository=os.path.relpath(self.repo, PROVIDER))
        snapshot = self.capture(relative)
        self.assertEqual(snapshot["repository_root"], str(self.repo))
        self.assertEqual(self.invoke(relative, snapshot), {"exit_id": "reviewed"})
        # The selector is part of this invocation even when the root is equivalent.
        self.assertNotEqual(snapshot, self.capture(absolute))

    def test_normal_missing_reference_and_scope_diagnostics(self):
        public_input = self.public_input(profile="committed_range", base="missing-fixture-ref", head="HEAD")
        error = self.call("capture", public_input, 2)
        self.assertEqual(error["code"], "git_unavailable")
        self.assertEqual(error["field_path"], "public_input.base")
        self.assertEqual(self.call("capture", self.public_input(paths=["../outside"]), 2)["code"], "invalid_scope")

    def test_blocked_exit_has_no_snapshot_or_semantic_inference(self):
        before = self.state()
        output = self.call("invoke", {
            "schema_version": "1.0", "public_input": self.public_input(),
            "owner_result": {"exit_id": "blocked", "reason": "Required design authority is unavailable."},
        })
        self.assertEqual(output, {"exit_id": "blocked"})
        self.assertEqual(before, self.state())


if __name__ == "__main__":
    unittest.main()
