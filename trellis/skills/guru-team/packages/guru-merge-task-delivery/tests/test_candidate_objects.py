"""Actual Git object transport, call-local reuse and snapshot compatibility."""
from __future__ import annotations

import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
sys.path.insert(0, str(PACKAGE / "runtime"))
import candidate_objects as objects
from history import HistoryContext


class CandidateObjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Guru Test")
        self.git("config", "user.email", "guru@example.test")

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

    def observe(self, calls, requests):
        original = subprocess.run
        def run(args, **kwargs):
            calls.append(args)
            if args[1:3] == ["cat-file", "--batch"]:
                request, response = kwargs["stdin"], kwargs["stdout"]
                self.assertTrue(stat.S_ISREG(os.fstat(request.fileno()).st_mode))
                self.assertTrue(stat.S_ISREG(os.fstat(response.fileno()).st_mode))
                self.assertNotEqual(subprocess.PIPE, response)
                at = request.tell()
                requests.extend(request.read().splitlines())
                request.seek(at)
            return original(args, **kwargs)
        return patch.object(objects.subprocess, "run", side_effect=run)

    def test_unique_content_and_binary_modes_deletions_special_paths(self):
        values = {"empty": b"", "二进制\tname\n\".bin": b"\x00\xff\n\x00",
                  "space dir/executable": b"#!/bin/sh\n", "large": b"z" * (2 * objects.COPY_BYTES + 7)}
        for name, content in values.items():
            self.write(name, content, 0o755 if name.endswith("executable") else 0o644)
        self.write("duplicate", values["large"])
        head = self.commit()
        paths = [*values, "duplicate", "deleted"]
        calls, requests = [], []
        with self.observe(calls, requests), objects.CandidateObjects(self.root) as reader:
            for index in range(2):
                snapshot = Path(self.temp.name) / f"snapshot{index}"
                snapshot.mkdir()
                reader.snapshot(head, paths, snapshot)
                for name, content in {**values, "duplicate": values["large"]}.items():
                    self.assertEqual(content, (snapshot / name).read_bytes())
                    self.assertEqual(name.endswith("executable"), bool((snapshot / name).stat().st_mode & 0o100))
                self.assertFalse((snapshot / "deleted").exists())
        self.assertEqual(4, len(requests))
        self.assertEqual(len(requests), len(set(requests)))
        self.assertEqual(1, sum(command[1] == "ls-tree" for command in calls))
        self.assertTrue(reader.response.closed)

    def test_metadata_chunks_use_byte_budget_and_real_unique_blobs(self):
        # Each component fits the filesystem limit; UTF-8 argv exceeds 64KiB.
        paths = [f"资产/{index:04d}-" + "长" * 65 for index in range(360)]
        for path in paths:
            self.write(path, path.encode())
        head = self.commit()
        calls, requests = [], []
        with self.observe(calls, requests), objects.CandidateObjects(self.root) as reader:
            reader.read(head, paths)
        chunks = [command for command in calls if command[1] == "ls-tree"]
        # Add enough multibyte paths to require more than one 64KiB chunk.
        self.assertEqual(2, len(chunks))
        self.assertTrue(all(sum(len(arg.encode()) + 1 for arg in command) <= objects.ARGV_BYTES for command in chunks))
        self.assertEqual(len(paths), len(requests))

    def test_reuse_across_commits_and_refresh_moving_ref(self):
        self.write("same", b"shared")
        self.write("changed", b"before")
        first = self.commit()
        calls, requests = [], []
        with objects.CandidateObjects(self.root) as reader:
            with self.observe(calls, requests):
                reader.read("main", ["same", "changed"])
            self.write("changed", b"after")
            second = self.commit()
            with self.observe(calls, requests):
                snapshot = Path(self.temp.name) / "current"
                snapshot.mkdir()
                reader.snapshot("main", ["same", "changed"], snapshot)
                reader.read(first, ["same", "changed"])
            self.assertNotEqual(first, second)
            self.assertEqual(b"after", (snapshot / "changed").read_bytes())
        self.assertEqual(3, len(requests))
        self.assertEqual(3, len(set(requests)))

    def test_unsupported_types_keep_candidate_error_and_context_cleanup(self):
        self.write("directory/file", b"data")
        (self.root / "link").symlink_to("directory/file")
        head = self.commit()
        self.git("update-index", "--add", "--cacheinfo", f"160000,{head},submodule")
        self.git("commit", "-qm", "gitlink candidate")
        head = self.git("rev-parse", "HEAD")
        for path in ("directory", "link", "submodule"):
            with self.subTest(path=path), HistoryContext(self.root, "example/repo", head) as context:
                with patch.object(context, "fetch", side_effect=AssertionError("unnecessary fetch")):
                    context.candidate(head, [path])
                    with self.assertRaises(objects.CommandError) as caught:
                        context.objects.snapshot(head, [path], Path(self.temp.name) / "snapshot")
                self.assertEqual("candidate.paths", caught.exception.field_path)
        self.assertTrue(context.objects.response.closed)

    def test_snapshot_rejects_absent_submodule_commit_before_content_read(self):
        self.write("file", b"data")
        self.commit()
        # A normal superproject gitlink need not have the submodule commit.
        self.git("update-index", "--add", "--cacheinfo", "160000," + "1" * 40 + ",submodule")
        self.git("commit", "-qm", "submodule reference")
        head = self.git("rev-parse", "HEAD")
        calls, requests = [], []
        with self.observe(calls, requests), objects.CandidateObjects(self.root) as reader:
            with self.assertRaises(objects.CommandError) as caught:
                reader.snapshot(head, ["submodule"], Path(self.temp.name) / "snapshot")
        self.assertEqual("candidate.paths", caught.exception.field_path)
        self.assertEqual([], requests)

    def test_missing_commit_is_an_object_error(self):
        self.write("file", b"data")
        self.commit()
        with objects.CandidateObjects(self.root) as reader, self.assertRaises(objects.CommandError) as caught:
            reader.read("0" * 40, ["file"])
        self.assertEqual("repository", caught.exception.field_path)

    def test_unavailable_blob_is_an_object_error_and_closes_spool(self):
        # Git can represent an available commit/tree with an unavailable blob,
        # as in an incomplete restored object store. Do not turn it into deletion.
        row = b"100644 blob " + b"1" * 40 + b"\tmissing\0"
        tree = subprocess.run(["git", "mktree", "--missing", "-z"], cwd=self.root,
                              input=row, check=True, capture_output=True).stdout.strip().decode()
        head = self.git("commit-tree", tree, "-m", "incomplete restored objects")
        with objects.CandidateObjects(self.root) as reader, self.assertRaises(objects.CommandError) as caught:
            reader.snapshot(head, ["missing"], Path(self.temp.name) / "snapshot")
        self.assertEqual("repository", caught.exception.field_path)
        self.assertTrue(reader.response.closed)

    def test_same_history_query_reuses_content_for_distinct_candidates(self):
        self.write("shared", b"shared")
        self.write("changed", b"one")
        first = self.commit()
        self.write("changed", b"two")
        second = self.commit()
        calls, requests = [], []
        with self.observe(calls, requests), HistoryContext(self.root, "example/repo", second) as context:
            context.candidate(first, ["shared", "changed"])
            context.candidate(second, ["shared", "changed"])
            snapshot = Path(self.temp.name) / "history"
            snapshot.mkdir()
            context.objects.snapshot(second, ["shared", "changed"], snapshot)
            self.assertEqual(b"two", (snapshot / "changed").read_bytes())
        self.assertEqual(3, len(requests))
        self.assertEqual(3, len(set(requests)))
        self.assertTrue(context.objects.response.closed)


if __name__ == "__main__":
    unittest.main()
