"""Real manual/history callers of the installed public immutable-content API."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
sys.path.insert(0, str(PACKAGE / "runtime"))
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.io import CommandError
from runtime.task_lifecycle import LifecycleContractError
from history import HistoryContext
from manual_recovery import commit_candidate


class CandidateContentTests(unittest.TestCase):
    def setUp(self):
        source = os.environ.get("TRELLIS_DELIVERY_API_COMMON")
        if not source:
            self.skipTest("Set TRELLIS_DELIVERY_API_COMMON to the reviewed public candidate common directory.")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Guru Test")
        self.git("config", "user.email", "guru@example.test")
        shutil.copytree(source, self.root / ".trellis/scripts/common",
                        ignore=shutil.ignore_patterns("__pycache__"))
        self.projection = DeliveryProjection(self.root, ".trellis/tasks/test")
        self.content_type = self.projection.api.delivery_store.GitCandidateContent

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              capture_output=True).stdout.strip().decode()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "candidate")
        return self.git("rev-parse", "HEAD")

    def write(self, name, content, mode=0o644):
        file = self.root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(content)
        file.chmod(mode)

    def fact(self, head, paths):
        return {"reviewed_head": head, "candidate": {
            "kind": "git", "paths": paths, "head_ref": head, "content_ref": "expected-by-caller",
            "base_ref": "retained-by-caller"}}

    def candidate(self, head, paths):
        return commit_candidate(self.projection, self.fact(head, paths), head)

    def test_manual_digest_matches_filesystem_api_with_modes_deletions_and_literal_paths(self):
        values = {"empty": b"", "二进制\tname\n\".bin": b"\x00\xff\n\x00",
                  "space dir/executable": b"#!/bin/sh\n", "large": b"z" * (2 * 1024 * 1024 + 7),
                  "[literal]*.txt": b"literal"}
        for name, content in values.items():
            self.write(name, content, 0o755 if name.endswith("executable") else 0o644)
        self.write("duplicate", values["large"])
        head = self.commit()
        paths = [*values, "duplicate", "deleted"]
        expected = self.projection._call(
            self.projection.api.delivery_store.candidate_content_ref, self.root, paths, "git")
        original = self.content_type.close
        closed = []
        def close(content):
            closed.append(content)
            original(content)
        with patch.object(self.content_type, "close", close):
            actual = self.candidate(head, paths)
        self.assertEqual(expected, actual["content_ref"])
        self.assertEqual("retained-by-caller", actual["base_ref"])
        self.assertEqual(1, len(closed))
        with self.assertRaises(ValueError):
            closed[0].content_ref(head, paths)

    def test_history_reuses_context_but_checks_each_candidate_and_refreshes_next_operation(self):
        self.write("shared", b"shared")
        self.write("changed", b"one")
        first = self.commit()
        first_expected = self.candidate(first, ["shared", "changed"])
        self.write("changed", b"two")
        second = self.commit()
        calls = []
        original = self.content_type.content_ref
        def read(content, head, paths):
            calls.append((content, head, paths))
            return original(content, head, paths)
        with patch.object(self.content_type, "content_ref", read):
            with HistoryContext(self.root, "example/repo", second) as context:
                one = context.candidate(self.projection, self.fact(first, ["shared", "changed"]))
                two = context.candidate(self.projection, self.fact(second, ["shared", "changed"]))
                self.assertEqual(first_expected, one)
                self.assertNotEqual(one["content_ref"], two["content_ref"])
                self.assertIs(calls[0][0], calls[1][0])
        with self.assertRaises(ValueError):
            context.content.content_ref(second, ["shared"])
        self.write("changed", b"three")
        third = self.commit()
        with HistoryContext(self.root, "example/repo", third) as following:
            three = following.candidate(self.projection, self.fact(third, ["shared", "changed"]))
            self.assertIsNot(following.content, context.content)
            self.assertNotEqual(two["content_ref"], three["content_ref"])

    def test_unsupported_types_do_not_fetch_or_read_submodule_content(self):
        self.write("directory/file", b"data")
        (self.root / "link").symlink_to("directory/file")
        self.commit()
        # A normal superproject need not contain the submodule commit object.
        self.git("update-index", "--add", "--cacheinfo", "160000," + "1" * 40 + ",submodule")
        self.git("commit", "-qm", "submodule reference")
        head = self.git("rev-parse", "HEAD")
        original = subprocess.run
        calls = []
        def run(args, **kwargs):
            calls.append(args)
            return original(args, **kwargs)
        for path in ("directory", "link", "submodule"):
            with self.subTest(path=path), HistoryContext(self.root, "example/repo", head) as context:
                with patch.object(context, "fetch", side_effect=AssertionError("unnecessary fetch")), \
                        patch("subprocess.run", side_effect=run), self.assertRaises(CommandError) as caught:
                    context.candidate(self.projection, self.fact(head, [path]))
                self.assertEqual("candidate.paths", caught.exception.field_path)
                with self.assertRaises(CommandError) as manual:
                    self.candidate(head, [path])
                self.assertEqual("candidate.paths", manual.exception.field_path)
        self.assertFalse(any("cat-file" in command for command in calls))

    def test_failed_read_metadata_diagnosis_uses_literal_byte_bounded_batches(self):
        self.write("[directory]*/file", b"data")
        head = self.commit()
        # Normal broad candidates can include many deleted multibyte paths.
        paths = [f"资产/{index:04d}-" + "长" * 65 for index in range(360)] + ["[directory]*"]
        original = subprocess.run
        commands = []
        def run(args, **kwargs):
            if args[:3] == ["git", "--literal-pathspecs", "ls-tree"]:
                commands.append(args)
            return original(args, **kwargs)
        with HistoryContext(self.root, "example/repo", head) as context:
            with patch("subprocess.run", side_effect=run), \
                    patch.object(context, "fetch", side_effect=AssertionError("unnecessary fetch")), \
                    self.assertRaises(CommandError) as caught:
                context.candidate(self.projection, self.fact(head, paths))
        self.assertEqual("candidate.paths", caught.exception.field_path)
        self.assertEqual(2, len(commands))
        self.assertTrue(all(sum(len(os.fsencode(arg)) + 1 for arg in command) <= 64 * 1024
                            for command in commands))

    def test_successful_public_read_has_no_extra_diagnostic_metadata_pass(self):
        self.write("file", b"data")
        head = self.commit()
        original = subprocess.run
        commands = []
        def run(args, **kwargs):
            if "ls-tree" in args:
                commands.append(args)
            return original(args, **kwargs)
        with patch("subprocess.run", side_effect=run):
            self.candidate(head, ["file"])
        self.assertEqual(1, len(commands))

    def test_missing_commit_and_blob_keep_repository_error(self):
        self.write("file", b"data")
        self.commit()
        with self.assertRaises(CommandError) as missing:
            self.candidate("0" * 40, ["file"])
        self.assertEqual("repository", missing.exception.field_path)
        row = b"100644 blob " + b"1" * 40 + b"\tmissing\0"
        tree = subprocess.run(["git", "mktree", "--missing", "-z"], cwd=self.root,
                              input=row, check=True, capture_output=True).stdout.strip().decode()
        head = self.git("commit-tree", tree, "-m", "incomplete restored objects")
        with self.assertRaises(CommandError) as blob:
            self.candidate(head, ["missing"])
        self.assertEqual("repository", blob.exception.field_path)

    def test_history_prepares_missing_commit_in_new_root_and_closes_both_contexts(self):
        self.write("file", b"data")
        head = self.commit()
        expected = self.candidate(head, ["file"])
        empty = Path(self.temp.name) / "empty"
        empty.mkdir()
        subprocess.run(["git", "init", "-q", "--bare", str(empty)], check=True)
        original_run, original_close = subprocess.run, self.content_type.close
        closed, environments = [], []
        def close(content):
            closed.append(content)
            original_close(content)
        def run(args, **kwargs):
            if "fetch" in args:
                args = [str(self.root) if arg == "https://github.com/example/repo.git" else arg for arg in args]
            elif "ls-tree" in args or "cat-file" in args:
                environments.append(kwargs.get("env", {}))
            return original_run(args, **kwargs)
        with patch("subprocess.run", side_effect=run), patch.object(self.content_type, "close", close):
            with HistoryContext(empty, "example/repo", head) as context:
                actual = context.candidate(self.projection, self.fact(head, ["file"]))
                scratch = context.root
                self.assertNotEqual(empty, scratch)
                self.assertEqual(expected, actual)
                self.assertEqual(1, len(closed))
            self.assertEqual(2, len(closed))
        self.assertFalse(scratch.exists())
        self.assertTrue(environments)
        self.assertTrue(all(env.get("GIT_NO_LAZY_FETCH") == "1" for env in environments))
        self.assertFalse((empty / "objects" / head[:2] / head[2:]).exists())

    def test_history_prepares_available_commit_with_unavailable_blob(self):
        self.write("file", b"data")
        head = self.commit()
        blob = self.git("rev-parse", head + ":file")
        restored = Path(self.temp.name) / "restored"
        restored.mkdir()
        subprocess.run(["git", "init", "-q", "--bare", str(restored)], check=True)
        shutil.copytree(self.root / ".git/objects", restored / "objects", dirs_exist_ok=True)
        (restored / "objects" / blob[:2] / blob[2:]).unlink()
        original = subprocess.run
        def run(args, **kwargs):
            if "fetch" in args:
                args = [str(self.root) if arg == "https://github.com/example/repo.git" else arg for arg in args]
            return original(args, **kwargs)
        with patch("subprocess.run", side_effect=run):
            with HistoryContext(restored, "example/repo", head) as context:
                actual = context.candidate(self.projection, self.fact(head, ["file"]))
                self.assertNotEqual(restored, context.root)
        self.assertEqual(self.candidate(head, ["file"]), actual)
        self.assertFalse((restored / "objects" / blob[:2] / blob[2:]).exists())

    def test_read_failure_retries_and_still_reports_repository_error(self):
        self.write("file", b"data")
        head = self.commit()
        error = LifecycleContractError("invalid_git_fact", "delivery", "ordinary Git read failure")
        with HistoryContext(self.root, "example/repo", head) as context:
            with patch.object(self.content_type, "content_ref", side_effect=error), \
                    patch.object(context, "fetch") as fetch, self.assertRaises(CommandError) as caught:
                context.candidate(self.projection, self.fact(head, ["file"]))
            self.assertEqual("repository", caught.exception.field_path)
            fetch.assert_called_once_with(head)
        with self.assertRaises(ValueError):
            context.content.content_ref(head, ["file"])

    def test_other_public_errors_are_not_reclassified_or_prepared(self):
        self.write("file", b"data")
        head = self.commit()
        with HistoryContext(self.root, "example/repo", head) as context:
            with patch.object(context, "fetch", side_effect=AssertionError("unnecessary fetch")), \
                    self.assertRaises(LifecycleContractError) as caught:
                context.candidate(self.projection, self.fact(head, ["file", "file"]))
            self.assertEqual("invalid_candidate", caught.exception.code)


if __name__ == "__main__":
    unittest.main()
