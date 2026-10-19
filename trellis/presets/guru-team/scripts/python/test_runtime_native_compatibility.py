"""Native fixtures load product code from the explicitly selected target checkout."""
from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

SOURCE = Path(__file__).resolve().parents[5]
TARGET = Path(os.environ.get("GURU_NATIVE_TARGET_ROOT", SOURCE)).resolve()
SKILLS = TARGET / "trellis/skills/guru-team"
ASSETS = SKILLS / "runtime"
COMMIT_PACKAGE = SKILLS / "packages/guru-create-task-commit"
sys.path.insert(0, str(SKILLS))
sys.path.insert(0, str(COMMIT_PACKAGE / "runtime"))
from runtime import base_selection, bootstrap, bootstrap_check
from runtime.io import CommandError
from runtime.schema import validate_json
from common import canonical_message, capture_snapshot
from execute import index_entries, run as execute_commit


class NativeRuntimeCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="guru-native-")
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name) / "中文 空格"
        self.workspace.mkdir()

    def git(self, repo, *arguments):
        result = subprocess.run(["git", *arguments], cwd=repo, text=True,
                                encoding="utf-8", capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        return result.stdout.strip()

    def repository(self):
        repo = self.workspace / "主仓库 root"
        repo.mkdir()
        self.git(repo, "init", "-q", "-b", "main")
        self.git(repo, "config", "user.name", "Native Test")
        self.git(repo, "config", "user.email", "native@example.test")
        self.git(repo, "config", "core.autocrlf", "false")
        (repo / "exact.txt").write_bytes(b"before\n")
        (repo / "unrelated.txt").write_bytes(b"before\n")
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-qm", "base")
        return repo

    def test_root_and_registered_worktree_use_native_path_identity(self):
        repo = self.repository()
        self.assertEqual(repo.resolve(), base_selection.repo(repo))
        linked = self.workspace / "linked 工作树"
        self.git(repo, "worktree", "add", "-qb", "feature/native", str(linked))
        self.assertEqual(linked.resolve(), base_selection.repo(linked))
        self.assertEqual(repo.resolve(), base_selection.authority_checkout(linked, "main"))
        subdir = repo / "subdir"
        subdir.mkdir()
        with self.assertRaises(CommandError):
            base_selection.repo(subdir)
        other = self.workspace / "other"
        other.mkdir()
        self.git(other, "init", "-q", "-b", "main")
        self.assertNotEqual(base_selection.repo(other), base_selection.repo(repo))

    def test_file_uri_resolves_relative_schema_with_unicode_and_spaces(self):
        schemas = self.workspace / "schema 引用"
        schemas.mkdir()
        (schemas / "child schema.json").write_text(json.dumps({
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object", "required": ["名称"],
            "properties": {"名称": {"type": "string"}},
        }, ensure_ascii=False), encoding="utf-8")
        root = schemas / "root.json"
        root.write_text(json.dumps({
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": "child%20schema.json",
        }), encoding="utf-8")
        validate_json({"名称": "原生路径"}, root, "fixture")
        with self.assertRaises(CommandError) as raised:
            validate_json({}, root, "fixture")
        self.assertEqual("schema_mismatch", raised.exception.code)

    def test_real_wrapper_fixture_keeps_stdin_and_inline_contracts(self):
        repo = self.workspace / "runtime repo"
        repo.mkdir()
        result = bootstrap.bootstrap(repo, ASSETS, Path(sys.executable))
        active = bootstrap.active_pointer_path(repo)
        before = active.read_bytes()
        target = Path(result["interpreter"]).parent.parent.parent
        calls = []
        real_run = subprocess.run

        @contextmanager
        def unicode_view(_purpose):
            with tempfile.TemporaryDirectory(dir=self.workspace, prefix="wrapper 检查 ") as directory:
                yield Path(directory).resolve()

        def observe(command, *args, **kwargs):
            outcome = real_run(command, *args, **kwargs)
            if len(command) > 1 and str(command[1]).endswith("/scripts/invoke.sh"):
                calls.append((list(command), kwargs.get("input"), outcome.returncode, outcome.stdout))
                # The existing public inline form uses exactly the same fixture JSON.
                if kwargs.get("input") is not None:
                    inline = list(command)
                    inline[inline.index("--invocation") + 1] = kwargs["input"]
                    options = dict(kwargs)
                    options.pop("input")
                    script = Path(kwargs["cwd"]) / "inline-fixture.sh"
                    script.write_text('exec "$BASH" ' + shlex.join(inline[1:]) + "\n",
                                      encoding="utf-8", newline="\n")
                    previous = real_run([inline[0], script.as_posix()], *args, **options)
                    self.assertTrue(outcome.stdout, outcome.stderr)
                    self.assertEqual(outcome.returncode, previous.returncode, previous.stderr)
                    self.assertEqual(json.loads(outcome.stdout), json.loads(previous.stdout))
            return outcome

        with mock.patch.object(bootstrap_check, "temporary_directory", unicode_view), \
             mock.patch.object(bootstrap_check.subprocess, "run", side_effect=observe):
            bootstrap_check.check_public_wrapper(ASSETS, result["runtime_identity"], target)
        self.assertEqual([0, 2], [row[2] for row in calls])
        self.assertEqual(before, active.read_bytes())
        if (ASSETS / "bootstrap_transport.py").is_file():
            self.assertTrue(all(row[0][row[0].index("--invocation") + 1] == "-" for row in calls))
            self.assertTrue(all(row[1] is not None for row in calls))

    def test_interpreter_visibility_and_failed_selection_preserve_active_runtime(self):
        repo = self.workspace / "selection repo"
        repo.mkdir()
        selected = bootstrap.bootstrap(repo, ASSETS, Path(sys.executable))
        pointer = bootstrap.active_pointer_path(repo)
        before = pointer.read_bytes()
        command = [sys.executable, str(ASSETS / "bootstrap.py"), "--repo", str(repo),
                   "--runtime-assets", str(ASSETS), "--json"]
        missing = self.workspace / "missing-python"
        failed = subprocess.run([*command, "--python", str(missing)],
                                text=True, encoding="utf-8", capture_output=True)
        self.assertEqual(2, failed.returncode, failed)
        self.assertEqual("interpreter_unavailable", json.loads(failed.stdout)["code"])
        self.assertEqual(before, pointer.read_bytes())
        if os.name != "nt":
            # This PATH contains an actual Python executable and no python alias or Bash.
            commands = self.workspace / "only-python3"
            commands.mkdir()
            (commands / "python3").symlink_to(sys.executable)
            environment = {**os.environ, "PATH": str(commands)}
            identity = subprocess.run([*command, "--print-identity"], env=environment,
                                      text=True, encoding="utf-8", capture_output=True)
            self.assertEqual(0, identity.returncode, identity.stderr)
            self.assertEqual(selected["runtime_identity"], identity.stdout.strip())
            failed = subprocess.run(command, env=environment, text=True,
                                    encoding="utf-8", capture_output=True)
            self.assertEqual(2, failed.returncode, failed)
            self.assertEqual("managed_runtime_check_failed", json.loads(failed.stdout)["code"])
            self.assertEqual(before, pointer.read_bytes())
        self.assertEqual(selected["runtime_identity"], bootstrap.validate_active(repo, ASSETS)["runtime_identity"])

    def commit_candidate(self, hook):
        repo = self.repository()
        self.git(repo, "checkout", "-qb", "feature/native")
        parent = self.git(repo, "rev-parse", "HEAD")
        (repo / "exact.txt").write_bytes(b"reviewed\n")
        (repo / "unrelated.txt").write_bytes(b"unrelated staged\n")
        self.git(repo, "add", "unrelated.txt")
        message = canonical_message({
            "type": "fix", "scope": "native", "summary": "中文提交消息",
            "background": "Windows 默认编码可能为 cp1252。",
            "changes": "按 UTF-8 写入并读回候选消息。",
            "boundaries": "保留真实 hook 与无关索引。",
            "validations": "真实 Git 隔离事务。",
        }, 630)
        expected = self.workspace / "expected-message"
        expected.write_bytes(message["bytes"].encode("utf-8"))
        evidence = self.workspace / "hook-observed"
        script = ("#!/bin/sh\nset -eu\n"
                  + f"cmp \"$1\" {shlex.quote(expected.as_posix())}\n"
                  + f"cp \"$1\" {shlex.quote(evidence.as_posix())}\n"
                  + hook + "\n")
        hook_file = repo / ".git/hooks/prepare-commit-msg"
        hook_file.write_text(script, encoding="utf-8", newline="\n")
        hook_file.chmod(0o755)
        snapshot = capture_snapshot(repo)
        candidate = {
            "$schema": "https://github.com/castbox/guru-trellis/schemas/guru-task-commit-candidate-5.0.json",
            "schema_version": "5.0", "skill_id": "guru-create-task-commit", "sequence": "001",
            "task": {"id": "native-test", "path": ".trellis/tasks/native-test",
                     "status": "in_progress", "branch": "feature/native"},
            "git": {"base_branch": "main", "base_ref": "main",
                    "pre_commit_head": parent, "phase2_commit_anchor": parent},
            "dirty_snapshot": snapshot,
            "path_classifications": [{
                "path": row["path"],
                "category": "task-reviewed" if row["path"] == "exact.txt" else "unrelated-preserved",
                "reason": "fixture", "coverage_source": "real native test",
            } for row in snapshot["entries"]],
            "exact_stage_paths": ["exact.txt"], "message": message,
            "ai_review": {"status": "passed", "summary": "fixture", "evidence": ["fixture"]},
        }
        locator = repo / ".trellis/.runtime/guru-team/native-candidate.json"
        locator.parent.mkdir(parents=True)
        locator.write_text(json.dumps(candidate, ensure_ascii=False), encoding="utf-8", newline="\n")
        return repo, parent, locator, message["bytes"].encode("utf-8"), evidence

    def test_taskcommit_utf8_roundtrip_real_hook_and_unrelated_index(self):
        repo, parent, locator, message, evidence = self.commit_candidate(":")
        unrelated = index_entries(repo, {"exact.txt"})
        result = execute_commit(COMMIT_PACKAGE, {}, ["--root", str(repo), "--candidate-artifact", str(locator)])
        self.assertEqual("committed", result["exit"])
        self.assertEqual(message, evidence.read_bytes())
        final = subprocess.run(["git", "cat-file", "commit", "HEAD"], cwd=repo, capture_output=True, check=True)
        self.assertEqual(message, final.stdout.partition(b"\n\n")[2])
        self.assertEqual(parent, self.git(repo, "show", "-s", "--format=%P", "HEAD"))
        self.assertEqual(unrelated, index_entries(repo, {"exact.txt"}))

    def test_taskcommit_detects_real_hook_message_change(self):
        repo, parent, locator, message, evidence = self.commit_candidate('printf "\\nchanged\\n" >> "$1"')
        index_before = index_entries(repo)
        with self.assertRaises(CommandError) as raised:
            execute_commit(COMMIT_PACKAGE, {}, ["--root", str(repo), "--candidate-artifact", str(locator)])
        self.assertEqual("pre_publication_validation", raised.exception.response["transaction_stage"])
        self.assertEqual(parent, self.git(repo, "rev-parse", "HEAD"))
        self.assertEqual(index_before, index_entries(repo))
        self.assertEqual(message, evidence.read_bytes())


if __name__ == "__main__":
    unittest.main()
