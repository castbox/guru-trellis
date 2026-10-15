"""Real Git transport/history and caller isolation; GitHub facts are fixtures."""
from __future__ import annotations

import hashlib
import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

PACKAGE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("history_fixture", PACKAGE / "tests/test_history.py")
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
HISTORY = fixture.HISTORY


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=True, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


def snapshot(root):
    return {p.relative_to(root).as_posix(): (p.stat().st_mode, hashlib.sha256(p.read_bytes()).hexdigest())
            for p in root.rglob("*") if p.is_file()}


class FixedCutoffTests(unittest.TestCase):
    def setUp(self):
        self.source = fixture.DeliveryHistoryTest()
        self.source.setUp()
        self.addCleanup(self.source.doCleanups)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.caller = self.workspace / "caller"
        self.initial = git(self.source.root, "rev-list", "--max-parents=0", "main")
        git(self.source.root, "branch", "seed", self.initial)
        self.cutoff = self.source.base_head
        self.url = self.source.root.as_uri()
        self.environment = mock.patch.dict(os.environ, {
            "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "url." + self.url + ".insteadOf",
            "GIT_CONFIG_VALUE_0": "https://github.com/example/repo.git",
        })
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def clone(self, *, shallow=False):
        args = ["clone", "--single-branch", "--branch", "main" if shallow else "seed", "--no-tags"]
        if shallow:
            args += ["--depth", "1"]
        git(self.workspace, *args, self.url, str(self.caller))
        git(self.caller, "config", "user.name", "Test")
        git(self.caller, "config", "user.email", "test@example.invalid")

    def discover(self, *, github=None, query=None):
        with mock.patch.object(HISTORY, "require_gh"), mock.patch.object(
            HISTORY, "gh_value", side_effect=github or self.source.github_value
        ):
            return HISTORY.discover(self.caller, PACKAGE, query or self.source.query)

    def test_missing_objects_prepared_without_any_caller_or_peer_git_writes(self):
        self.clone()
        peer = self.workspace / "peer"
        git(self.caller, "worktree", "add", "--detach", str(peer))
        (self.caller / "unrelated.txt").write_text("retained dirty file\n")
        (peer / "peer.txt").write_text("retained peer work\n")
        before, other = snapshot(self.caller), snapshot(peer)
        created = []
        temporary = HISTORY.tempfile.TemporaryDirectory
        def capture(*args, **kwargs):
            directory = temporary(*args, **kwargs)
            created.append(Path(directory.name))
            return directory
        with mock.patch.object(HISTORY.tempfile, "TemporaryDirectory", side_effect=capture):
            result = self.discover()
        self.assertEqual(self.cutoff, result["cutoff_commit"])
        self.assertEqual([101, 102], [d["pr_number"] for d in result["deliveries"]])
        self.assertEqual(before, snapshot(self.caller))
        self.assertEqual(other, snapshot(peer))
        self.assertTrue(created)
        self.assertTrue(all(not p.exists() for p in created))
        self.assertEqual(self.initial, git(self.caller, "rev-parse", "HEAD"))

    def test_shallow_successful_rev_list_is_not_complete_history(self):
        self.clone(shallow=True)
        before = snapshot(self.caller)
        self.assertEqual(1, len(git(self.caller, "rev-list", "--first-parent", "HEAD").splitlines()))
        result = self.discover()
        self.assertEqual([101, 102], [d["pr_number"] for d in result["deliveries"]])
        self.assertEqual(before, snapshot(self.caller))

    def test_local_complete_objects_are_reused_even_with_stale_or_missing_base_ref(self):
        git(self.workspace, "clone", self.url, str(self.caller))
        git(self.caller, "update-ref", "refs/remotes/origin/main", self.initial)
        git(self.caller, "update-ref", "refs/heads/main", self.initial)
        with mock.patch.object(HISTORY.HistoryContext, "fetch", side_effect=AssertionError("unnecessary fetch")):
            result = self.discover()
        self.assertEqual(self.cutoff, result["cutoff_commit"])
        self.assertEqual(2, len(result["deliveries"]))

    def test_remote_advance_does_not_replace_cutoff_or_repeat_base_read(self):
        self.clone()
        reads = []
        def advancing(root, args, operation):
            value = self.source.github_value(root, args, operation)
            if operation == "base ref":
                reads.append(value["object"]["sha"])
                tree = git(self.source.root, "rev-parse", "main^{tree}")
                next_commit = git(self.source.root, "commit-tree", tree, "-p", self.cutoff, "-m", "unrelated B2")
                git(self.source.root, "update-ref", "refs/heads/main", next_commit)
                self.source.base_head = next_commit
            return value
        result = self.discover(github=advancing)
        self.assertEqual([self.cutoff], reads)
        self.assertEqual(self.cutoff, result["cutoff_commit"])
        self.assertNotEqual(self.source.base_head, result["cutoff_commit"])
        self.assertEqual(2, len(result["deliveries"]))

    def test_transport_failure_is_concrete_and_cleans_scratch(self):
        self.clone()
        created = []
        temporary = HISTORY.tempfile.TemporaryDirectory
        def capture(*args, **kwargs):
            directory = temporary(*args, **kwargs)
            created.append(Path(directory.name))
            return directory
        before = snapshot(self.caller)
        with mock.patch.dict(os.environ, {"GIT_CONFIG_KEY_0": "url.file:///nonexistent-guru-history.insteadOf"}), \
             mock.patch.object(HISTORY.tempfile, "TemporaryDirectory", side_effect=capture), \
             self.assertRaises(HISTORY.CommandError) as caught:
            self.discover()
        self.assertEqual("history.preparation", caught.exception.field_path)
        self.assertEqual(before, snapshot(self.caller))
        self.assertTrue(created and all(not p.exists() for p in created))

    def test_still_incomplete_preparation_fails_instead_of_empty_success(self):
        self.clone()
        with mock.patch.object(HISTORY.HistoryContext, "fetch"), self.assertRaises(HISTORY.CommandError):
            self.discover()

    def test_provider_permission_and_network_failures_keep_specific_reasons(self):
        self.clone()
        original = HISTORY.subprocess.run
        for stderr, reason in (("fatal: HTTP 403 permission denied", "Git permission denied"),
                               ("fatal: Could not resolve host", "Git network unavailable")):
            def failed_fetch(args, *a, **kw):
                if args[:2] == ["git", "fetch"]:
                    return subprocess.CompletedProcess(args, 128, "", stderr)
                return original(args, *a, **kw)
            with self.subTest(reason=reason), mock.patch.object(HISTORY.subprocess, "run", side_effect=failed_fetch), \
                 self.assertRaises(HISTORY.CommandError) as caught:
                self.discover()
            self.assertEqual("history.preparation", caught.exception.field_path)
            self.assertIn(reason, caught.exception.remediation)

    def test_complete_unmatched_history_has_valid_empty_result(self):
        self.clone()
        result = self.discover(query={**self.source.query, "task_identity": "another-task"})
        self.assertEqual("3.0", result["schema_version"])
        self.assertEqual(self.cutoff, result["cutoff_commit"])
        self.assertEqual([], result["deliveries"])

    def test_schema1_and_schema2_deliveries_keep_order_and_public_key(self):
        source = self.source
        git(source.root, "switch", "-c", "schema-two", "main")
        (source.root / "new.txt").write_text("third delivery\n")
        git(source.root, "add", "new.txt")
        git(source.root, "commit", "-m", "schema two feature")
        head = git(source.root, "rev-parse", "HEAD")
        key = {"task_id": source.task_identity, "lifecycle_generation": 1,
               "delivery_id": "43134b50-2c8b-4d70-b114-218a735a82e2"}
        git(source.root, "switch", "main")
        message = ("third merge\n\nGuru-Task-Identity: " + source.task_identity
                   + "\nGuru-Delivery-Schema: 2\nGuru-Delivery-Head: " + head
                   + "\nGuru-Delivery-Identity: " + key["delivery_id"] + "\nGuru-Task-Generation: 1")
        git(source.root, "merge", "--no-ff", "schema-two", "-m", message)
        source.base_head = git(source.root, "rev-parse", "HEAD")
        source.deliveries.append({"reviewed_head": head, "merge_commit_sha": source.base_head, "pr_number": 103})
        self.clone()
        result = self.discover()
        self.assertEqual([101, 102, 103], [row["pr_number"] for row in result["deliveries"]])
        self.assertEqual(key, result["deliveries"][-1]["delivery_key"])


if __name__ == "__main__":
    unittest.main()
