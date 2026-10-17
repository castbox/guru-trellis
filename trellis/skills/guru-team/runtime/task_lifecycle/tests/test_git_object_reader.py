"""Independent old-show oracle and real call-local object transport."""
from __future__ import annotations

import io
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.git_object_batch import GitObjectBatch, GitObjectBatchError
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import TaskObjectReader, commit_path_bytes, inspect_repository


class TaskObjectReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Guru Test")
        self.git("config", "user.email", "guru@example.test")
        self.repository = inspect_repository(self.repo)

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, check=True,
                              capture_output=True).stdout.strip().decode()

    def write(self, path, data):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD")

    @staticmethod
    def read_all(reader, commit, paths):
        committed = reader.prepare(commit, paths)
        return {path: reader.read_path(committed, path) for path in paths}

    def observe(self, commands, requests):
        original = subprocess.run
        def run(argv, **kwargs):
            commands.append(argv)
            if "cat-file" in argv and "--batch" in argv:
                for name in ("stdin", "stdout"):
                    self.assertTrue(stat.S_ISREG(os.fstat(kwargs[name].fileno()).st_mode))
                position = kwargs["stdin"].tell()
                requests.extend(kwargs["stdin"].read().splitlines())
                kwargs["stdin"].seek(position)
            return original(argv, **kwargs)
        return patch("subprocess.run", side_effect=run)

    def test_matches_original_show_for_blob_modes_symlink_tree_and_gitlinks(self):
        self.write("plain.json", b'{"id":"plain"}')
        self.write("executable", b'{"id":"executable"}')
        self.write("directory/file", b"nested")
        self.write("特殊\tpath\n.json", b"binary\0\xff")
        (self.repo / "link").symlink_to('{"id":"link"}')
        first = self.commit()
        self.git("update-index", "--chmod=+x", "executable")
        self.git("update-index", "--add", "--cacheinfo", f"160000,{first},available-module")
        self.git("update-index", "--add", "--cacheinfo", "160000," + "1" * 40 + ",missing-module")
        self.git("commit", "-qm", "entry types")
        head = self.git("rev-parse", "HEAD")
        paths = ["plain.json", "executable", "link", "directory", "特殊\tpath\n.json",
                 "available-module", "missing-module", "absent"]
        expected = {path: commit_path_bytes(self.repository, head, path) for path in paths}
        with TaskObjectReader(self.repository) as reader:
            self.assertEqual(expected, self.read_all(reader, head, paths))

    def test_missing_path_blob_and_commit_preserve_original_result(self):
        self.write("present", b"present")
        oid = self.git("hash-object", "-w", "present")
        row = b"100644 blob " + b"1" * 40 + b"\tmissing\0" + b"100644 blob " + oid.encode() + b"\tpresent\0"
        tree = subprocess.run(["git", "mktree", "--missing", "-z"], cwd=self.repo,
                              input=row, check=True, capture_output=True).stdout.strip().decode()
        head = self.git("commit-tree", tree, "-m", "incomplete restored objects")
        paths = ["missing", "present", "absent"]
        expected = {path: commit_path_bytes(self.repository, head, path) for path in paths}
        commands, requests = [], []
        with self.observe(commands, requests), TaskObjectReader(self.repository) as reader:
            self.assertEqual(expected, self.read_all(reader, head, paths))
        self.assertFalse(any("-e" in command for command in commands))
        with TaskObjectReader(self.repository) as reader, self.assertRaises(LifecycleContractError) as caught:
            reader.read_path("0" * 40, "missing")
        self.assertEqual(("git_fact_unavailable", "commit"), (caught.exception.code, caught.exception.field_path))

    def test_metadata_and_content_reuse_but_moving_refs_refresh(self):
        self.write("tasks/a.json", b"same")
        self.write("tasks/b.json", b"same")
        first = self.commit()
        commands, requests = [], []
        with self.observe(commands, requests), TaskObjectReader(self.repository) as reader:
            paths = reader.paths_under(first, "tasks")
            self.assertEqual(paths, reader.paths_under(first, "tasks"))
            self.assertEqual({path: b"same" for path in paths}, self.read_all(reader, first, paths))
            self.assertEqual({path: b"same" for path in paths}, self.read_all(reader, first, paths))
            self.write("other", b"unrelated")
            self.commit()
            self.assertEqual(b"same", reader.read_path("main", "tasks/a.json"))
            self.write("tasks/a.json", b"changed")
            self.git("add", "tasks/a.json")
            self.assertEqual(b"same", reader.read_path("main", "tasks/a.json"))
            self.git("commit", "-qm", "new actual tree")
            self.assertEqual(b"changed", reader.read_path("main", "tasks/a.json"))
        self.assertEqual(2, len(requests))
        self.assertEqual(2, len(set(requests)))
        commands, requests = [], []
        with self.observe(commands, requests), TaskObjectReader(self.repository) as reader:
            self.assertEqual(b"same", reader.read_path(first, "tasks/a.json"))
        self.assertEqual(1, len(requests))

    def test_prepare_keeps_offsets_then_only_current_path_content_is_read(self):
        for number in range(3):
            self.write(f"tasks/{number}.json", b'"' + bytes([65 + number]) * (2 * 1024 * 1024) + b'"')
        head = self.commit()
        with TaskObjectReader(self.repository) as reader:
            with patch.object(reader.objects, "read_bytes", wraps=reader.objects.read_bytes) as reads:
                prepared = reader.prepare(head, [f"tasks/{n}.json" for n in range(3)])
                self.assertEqual(0, reads.call_count)
                self.assertTrue(all(isinstance(row, tuple) for row in reader.objects.entries.values()))
                self.assertEqual(2 * 1024 * 1024 + 2, len(reader.read_path(prepared, "tasks/0.json")))
                self.assertEqual(1, reads.call_count)

    def test_spool_unique_copy_and_missing_object_can_be_prepared_later(self):
        data = b"x" * (2 * 1024 * 1024 + 3)
        self.write("large", data)
        oid = self.git("hash-object", "large")
        commands, requests = [], []
        class Output(io.BytesIO):
            def write(self, value):
                self.maximum = max(getattr(self, "maximum", 0), len(value))
                return super().write(value)
        with self.observe(commands, requests), GitObjectBatch(self.repo) as objects:
            self.assertEqual({oid: None}, objects.ensure([oid]))
            self.git("hash-object", "-w", "large")
            self.assertIsNotNone(objects.ensure([oid, oid])[oid])
            objects.ensure([oid])
            output = Output()
            objects.copy_to(oid, output)
            self.assertEqual(data, output.getvalue())
            self.assertLessEqual(output.maximum, 1024 * 1024)
        self.assertTrue(objects.response.closed)
        self.assertEqual([oid.encode(), oid.encode()], requests)

    def test_show_failure_with_existing_commit_stays_none_but_truncation_is_error(self):
        self.write("file", b"data")
        head = self.commit()
        original = subprocess.run
        def failed(argv, **kwargs):
            if "--batch" in argv or "show" in argv:
                return subprocess.CompletedProcess(argv, 128, stdout=b"", stderr=b"ordinary read failed")
            return original(argv, **kwargs)
        with patch("subprocess.run", side_effect=failed), TaskObjectReader(self.repository) as reader:
            self.assertEqual({"file": None}, self.read_all(reader, head, ["file"]))
        def truncated(argv, **kwargs):
            if "--batch" in argv:
                oid = kwargs["stdin"].read().splitlines()[0]
                kwargs["stdout"].write(oid + b" blob 100\nshort")
                return subprocess.CompletedProcess(argv, 0, stderr=b"")
            return original(argv, **kwargs)
        with patch("subprocess.run", side_effect=truncated), TaskObjectReader(self.repository) as reader, self.assertRaises(LifecycleContractError) as caught:
            self.read_all(reader, head, ["file"])
        self.assertEqual("git_fact_unavailable", caught.exception.code)
        self.assertTrue(reader.objects.response.closed)


if __name__ == "__main__":
    unittest.main()
