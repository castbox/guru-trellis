"""Real Git continuity digests, bounded transport and invocation-local reuse."""
from __future__ import annotations

import hashlib
import importlib.util
import json
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


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


common = module("continuity_tree_common", PACKAGE / "runtime/common.py")


class TreeIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.batch_processes = []
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Guru Test")
        self.git("config", "user.email", "guru@example.test")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, check=True,
                              capture_output=True).stdout.strip().decode()

    def write(self, path, data):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "candidate")
        return self.git("rev-parse", "HEAD")

    def oracle(self, head):
        # Independent original scalar algorithm: no production batch/memo helper.
        raw = subprocess.run(["git", "ls-tree", "-r", "-z", "--full-tree", head],
                             cwd=self.repo, capture_output=True, check=True).stdout
        rows = []
        for entry in raw.split(b"\0"):
            if not entry:
                continue
            metadata, path = entry.split(b"\t", 1)
            mode, kind, oid = metadata.split()
            if mode == b"160000" and kind == b"commit":
                rows.append(path + b"\0" + mode + b"\0" + oid + b"\0")
            elif kind == b"blob":
                content = subprocess.run(["git", "cat-file", "blob", oid.decode()],
                                         cwd=self.repo, capture_output=True, check=True).stdout
                rows.append(path + b"\0" + hashlib.sha256(content).hexdigest().encode() + b"\0")
        return hashlib.sha256(b"".join(rows)).hexdigest()

    def observe(self, commands, requests):
        original = subprocess.Popen
        def start(argv, **kwargs):
            commands.append(argv)
            batch = argv[:3] == ["git", "cat-file", "--batch"]
            if batch:
                for name in ("stdin", "stderr"):
                    self.assertTrue(stat.S_ISREG(os.fstat(kwargs[name].fileno()).st_mode))
                self.assertEqual(subprocess.PIPE, kwargs["stdout"])
                self.assertEqual(1024 * 1024, kwargs["bufsize"])
                position = kwargs["stdin"].tell()
                requests.extend(kwargs["stdin"].read().splitlines())
                kwargs["stdin"].seek(position)
            process = original(argv, **kwargs)
            if batch:
                self.assertTrue(stat.S_ISFIFO(os.fstat(process.stdout.fileno()).st_mode))
                self.batch_processes.append(process)
            return process
        return patch.object(common.subprocess, "Popen", side_effect=start)

    def assert_batches_finished(self):
        self.assertTrue(self.batch_processes)
        for process in self.batch_processes:
            self.assertIsNotNone(process.poll())
            self.assertTrue(process.stdout.closed)

    def test_original_bytes_for_all_types_modes_special_paths_and_deletion(self):
        for path, data in {"empty": b"", "binary": bytes(range(256)),
                           "复制\tfile\n.bin": b"shared\0bytes", "duplicate": b"shared\0bytes",
                           "directory/run.sh": b"#!/bin/sh\n"}.items():
            self.write(path, data)
        (self.repo / "link").symlink_to("missing-target")
        self.git("add", ".")
        self.git("update-index", "--chmod=+x", "directory/run.sh")
        self.git("update-index", "--add", "--cacheinfo", "160000," + "1" * 40 + ",submodule")
        self.git("commit", "-qm", "all supported tree entries")
        first = self.git("rev-parse", "HEAD")
        expected = self.oracle(first)
        self.assertEqual(expected, common.tree_identity(self.repo, first))
        self.git("update-index", "--chmod=-x", "directory/run.sh")
        self.git("commit", "-qm", "mode only")
        self.assertEqual(expected, common.tree_identity(self.repo, "HEAD"))
        self.git("rm", "duplicate")
        self.git("commit", "-qm", "normal deletion")
        deleted = self.git("rev-parse", "HEAD")
        self.assertEqual(self.oracle(deleted), common.tree_identity(self.repo, deleted))
        self.assertNotEqual(expected, common.tree_identity(self.repo, deleted))

    def test_unique_blob_requests_hash_once_using_file_request_and_single_pipe(self):
        for number in range(300):
            self.write(f"assets/unique-{number}", str(number).encode())
        for number in range(80):
            self.write(f"assets/copy-{number}", b"shared")
        self.write("assets/large", bytes(range(256)) * 8193)
        head = self.commit()
        expected = self.oracle(head)
        commands, requests = [], []
        real_sha256 = hashlib.sha256
        with self.observe(commands, requests), patch.object(common.hashlib, "sha256", wraps=real_sha256) as hashes:
            actual = common.tree_identity(self.repo, head)
        self.assertEqual(expected, actual)
        self.assertEqual(302, len(requests))
        self.assertEqual(len(requests), len(set(requests)))
        self.assertEqual(len(requests) + 1, hashes.call_count)
        self.assert_batches_finished()
        self.assertEqual(1, sum(command[:3] == ["git", "cat-file", "--batch"] for command in commands))

    def test_memo_reuses_immutable_commit_and_distinct_commits_with_same_tree(self):
        self.write("file", b"same tree")
        first = self.commit()
        self.git("commit", "--allow-empty", "-qm", "another commit same tree")
        second = self.git("rev-parse", "HEAD")
        commands, requests, memo = [], [], {}
        with self.observe(commands, requests):
            original = common.tree_identity(self.repo, first, tree_memo=memo)
            self.assertEqual(original, common.tree_identity(self.repo, first, tree_memo=memo))
            self.assertEqual(original, common.tree_identity(self.repo, second, tree_memo=memo))
        self.assertEqual(1, sum(command[1] == "ls-tree" for command in commands))
        self.assertEqual(2, sum(command[1] == "rev-parse" for command in commands))
        self.assertEqual(1, len(requests))

    def test_moving_ref_refreshes_and_index_worktree_never_replace_commit(self):
        self.write("file", b"old")
        first = self.commit()
        memo = {}
        original = common.tree_identity(self.repo, "main", tree_memo=memo)
        self.write("file", b"new")
        self.git("add", "file")
        self.assertEqual(original, common.tree_identity(self.repo, "main", tree_memo=memo))
        self.git("commit", "-qm", "new committed tree")
        changed = common.tree_identity(self.repo, "main", tree_memo=memo)
        self.assertNotEqual(original, changed)
        self.assertEqual(original, common.tree_identity(self.repo, first, tree_memo=memo))
        self.assertEqual(self.oracle("main"), changed)
        commands, requests = [], []
        with self.observe(commands, requests):
            self.assertEqual(changed, common.tree_identity(self.repo, "main"))
        self.assertEqual(1, len(requests))

    def test_shared_memo_is_bound_to_actual_repository(self):
        self.write("file", b"shared")
        head = self.commit()
        other = Path(self.temp.name) / "other"
        subprocess.run(["git", "clone", "-q", str(self.repo), str(other)], check=True, capture_output=True)
        commands, requests, memo = [], [], {}
        with self.observe(commands, requests):
            expected = common.tree_identity(self.repo, head, tree_memo=memo)
            self.assertEqual(expected, common.tree_identity(other, head, tree_memo=memo))
        self.assertEqual(2, len(requests))
        self.assertEqual(2, sum(command[1] == "ls-tree" for command in commands))

    def test_empty_tree_keeps_original_empty_digest(self):
        self.git("commit", "--allow-empty", "-qm", "empty tree")
        self.assertEqual(hashlib.sha256(b"").hexdigest(), common.tree_identity(self.repo, "HEAD"))

    def test_unavailable_blob_drains_remaining_output_and_git_failure_keeps_stderr(self):
        self.write("large", b"x" * (2 * 1024 * 1024))
        available = self.git("hash-object", "-w", "large")
        row = (b"100644 blob " + b"1" * 40 + b"\t00-missing\0"
               + b"100644 blob " + available.encode() + b"\tzz-large\0")
        tree = subprocess.run(["git", "mktree", "--missing", "-z"], cwd=self.repo,
                              input=row, check=True, capture_output=True).stdout.strip().decode()
        head = self.git("commit-tree", tree, "-m", "incomplete restored objects")
        commands, requests, memo = [], [], {}
        with self.observe(commands, requests), self.assertRaises(common.CommandError) as caught:
            common.tree_identity(self.repo, head, tree_memo=memo)
        self.assertEqual("stale_identity", caught.exception.code)
        self.assertEqual("candidate_tree_sha256", caught.exception.field_path)
        self.assert_batches_finished()
        self.assertEqual(0, self.batch_processes[-1].returncode)
        self.assertEqual({}, memo)
        head = self.commit()
        original = subprocess.Popen
        def failed(argv, **kwargs):
            if argv[:3] == ["git", "cat-file", "--batch"]:
                # Ordinary Git failure: the selected working directory is no
                # longer a repository. Retain real stderr and process cleanup.
                kwargs["cwd"] = self.temp.name
            process = original(argv, **kwargs)
            if argv[:3] == ["git", "cat-file", "--batch"]:
                self.batch_processes.append(process)
            return process
        with patch.object(common.subprocess, "Popen", side_effect=failed), self.assertRaises(common.CommandError) as caught:
            common.tree_identity(self.repo, head)
        self.assertEqual("candidate_tree_sha256", caught.exception.field_path)
        self.assertIn("not a git repository", caught.exception.remediation)
        self.assert_batches_finished()
        self.assertNotEqual(0, self.batch_processes[-1].returncode)

    def test_stdout_read_failure_closes_pipe_and_waits_for_real_git(self):
        self.write("large", b"x" * (2 * 1024 * 1024))
        head = self.commit()
        original = subprocess.Popen
        class Unreadable:
            def __init__(self, stream):
                self.stream = stream
            def read(self, size):
                raise OSError("ordinary response read failure")
            def __getattr__(self, name):
                return getattr(self.stream, name)
        def start(argv, **kwargs):
            process = original(argv, **kwargs)
            if argv[:3] == ["git", "cat-file", "--batch"]:
                process.stdout = Unreadable(process.stdout)
                self.batch_processes.append(process)
            return process
        memo = {}
        with patch.object(common.subprocess, "Popen", side_effect=start), self.assertRaises(common.CommandError) as caught:
            common.tree_identity(self.repo, head, tree_memo=memo)
        self.assertEqual("candidate_tree_sha256", caught.exception.field_path)
        self.assert_batches_finished()
        self.assertEqual({}, memo)

    def test_record_reuses_tree_but_separate_validator_reads_it_again(self):
        fixture = module("continuity_record_fixture", PACKAGE / "tests/test_contract.py")
        case = fixture.BranchReviewWrapperLifecycleTest()
        case.setUp()
        self.addCleanup(case.tearDown)
        public = case.continuity_public()
        args = ["--root", str(case.repo), "--task", fixture.TASK_REF,
                "--skill-input", str(case.write("public.json", public)),
                "--semantic-review-file", str(case.write("auth.json", case.auth("continuity_passed"))),
                "--typed-exit", "continuity_passed"]
        with patch.dict(sys.modules, {"common": common}):
            record = module("continuity_record_owner", PACKAGE / "runtime/record.py")
        commands, requests = [], []
        with self.observe(commands, requests):
            receipt = record.run(PACKAGE, {}, args)
        self.assertEqual("recorded", receipt["status"])
        self.assertEqual(1, sum(command[:3] == ["git", "cat-file", "--batch"] for command in commands))
        gate = json.loads(case.checkpoint().read_text())
        commands, requests = [], []
        with self.observe(commands, requests):
            common.validate_gate(PACKAGE, case.repo, gate)
        self.assertEqual(1, sum(command[:3] == ["git", "cat-file", "--batch"] for command in commands))


if __name__ == "__main__":
    unittest.main()
