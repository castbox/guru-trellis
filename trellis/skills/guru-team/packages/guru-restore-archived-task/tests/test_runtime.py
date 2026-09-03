from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


PACKAGE = Path(__file__).resolve().parents[1]
SKILLS_ROOT = PACKAGE.parents[1]
import sys

if str(SKILLS_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLS_ROOT))

from runtime.io import CommandError

sys.path.insert(0, str(PACKAGE / "runtime"))
import invoke


class RestoreArchivedTaskRuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        self.worktree = Path(self.temp.name) / "task-worktree"
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Restore Test"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "restore@example.invalid"], check=True)
        (self.root / "README.md").write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-q", "-m", "test: base"], check=True)
        self.branch = "codex/348-restore"
        subprocess.run(["git", "-C", str(self.root), "worktree", "add", "-q", "-b", self.branch, str(self.worktree), "HEAD"], check=True)

        self.task_id = "09-03-348-merge-blocked-phase2-reentry"
        self.archive_locator = f".trellis/tasks/archive/2026-09/{self.task_id}"
        self.active_locator = f".trellis/tasks/{self.task_id}"
        self.expected_head = subprocess.run(
            ["git", "-C", str(self.worktree), "rev-parse", "HEAD"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        self.archive_commit = self.expected_head
        self.mapping_path = self.root / ".trellis/.runtime/guru-team/tasks" / f"{self.task_id}.json"
        archive = self.root / self.archive_locator
        archive.mkdir(parents=True)
        task = {
            "id": self.task_id,
            "name": self.task_id,
            "title": "#348 restore",
            "status": "completed",
            "completedAt": "2026-09-03T00:00:00Z",
            "branch": self.branch,
            "base_branch": "main",
            "scope": "GitHub issue: https://github.com/castbox/guru-trellis/issues/348",
        }
        self._write_json(archive / "task.json", task)
        self._write_json(archive / "finish-summary.json", {"task_id": self.task_id, "repository": "castbox/guru-trellis", "pr_number": 348, "expected_head_sha": self.expected_head, "archive_commit": self.archive_commit})
        for name in ("phase2-check.json", "review-gate.json", "pr-readiness.json", "task-finalization-gate.json"):
            (archive / name).write_text("stale\n", encoding="utf-8")
        self.named_checkpoint = self.root / ".trellis/.runtime/guru-team/owner-checkpoints" / self.task_id
        self.hashed_checkpoint = self.root / ".trellis/.runtime/guru-team/owner-checkpoints" / __import__("hashlib").sha256(self.task_id.encode()).hexdigest()[:20]
        for checkpoint, name in ((self.named_checkpoint, "phase2-check.json"), (self.hashed_checkpoint, "pr-readiness.json")):
            checkpoint.mkdir(parents=True, exist_ok=True)
            (checkpoint / name).write_text("stale\n", encoding="utf-8")
        self.mapping = {"state": "archived", "task_id": self.task_id, "archive_locator": self.archive_locator, "active_locator": self.active_locator, "repository": "castbox/guru-trellis", "branch_name": self.branch, "worktree_path": str(self.worktree)}
        self._write_json(self.mapping_path, self.mapping)
        self.public = {"schema_version": "1.0", "profile": "restore_archived_task", "mode": "workflow", "exit_id": "phase2_reentry_required", "repo_ref": "castbox/guru-trellis", "pr_number": 348, "pr_url": "https://github.com/castbox/guru-trellis/pull/348", "expected_head_sha": self.expected_head, "expected_base_branch": "main", "expected_head_branch": self.branch, "issue_number": 348, "task_id": self.task_id, "archive_locator": self.archive_locator, "active_locator": self.active_locator, "archive_commit": self.archive_commit, "finding_refs": ["merge-finding:348:phase2-reentry"], "resume_target": "phase-2"}
        self.semantic = {"schema_version": "1.0", "profile": "restore_archived_task", "mode": "workflow", "review_intent": "task_work_reentry", "classification": "task_work", "requires_task_content_change": True, "finding_refs": list(self.public["finding_refs"])}
        self.facts = self._facts("archived", "completed", None, False)
        self.input_path = self._write_json(Path(self.temp.name) / "input.json", self.public)
        self.semantic_path = self._write_json(Path(self.temp.name) / "semantic.json", self.semantic)
        self.facts_path = self._write_json(Path(self.temp.name) / "facts.json", self.facts)

    def tearDown(self) -> None:
        subprocess.run(["git", "-C", str(self.root), "worktree", "remove", "-f", str(self.worktree)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.temp.cleanup()

    def _write_json(self, path: Path, value: dict) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return path

    def _facts(self, mapping_state: str, task_status: str, active_task: str | None, blocker: bool) -> dict:
        task_path = self.root / (self.archive_locator if mapping_state == "archived" else self.active_locator) / "task.json"
        finish_path = task_path.parent / "finish-summary.json"
        blockers = {name: False for name in ("provider", "permission", "ruleset", "external_service", "scope_drift", "identity_drift", "merged", "ambiguous")}
        if blocker:
            blockers["provider"] = True
        return {
            "schema_version": "1.0",
            "pr": {"state": "OPEN", "number": 348, "url": self.public["pr_url"], "head_sha": self.expected_head, "base_branch": "main", "head_branch": self.branch},
            "issue": {"number": 348, "state": "OPEN", "close_intent": "unchanged"},
            "remote_branch": {"name": self.branch, "head_sha": self.expected_head},
            "local_branch": {"name": self.branch, "head_sha": self.expected_head},
            "archive": {"locator": self.archive_locator, "commit": self.archive_commit, "task_json_sha256": __import__("hashlib").sha256(task_path.read_bytes()).hexdigest(), "finish_summary_sha256": __import__("hashlib").sha256(finish_path.read_bytes()).hexdigest() if finish_path.is_file() else "0" * 64},
            "task": {"id": self.task_id, "status": task_status, "completed_at": "2026-09-03T00:00:00Z" if task_status == "completed" else None, "branch": self.branch, "base_branch": "main", "repo_ref": "castbox/guru-trellis", "issue_number": 348, "pr_number": 348, "expected_head_sha": self.expected_head},
            "runtime_mapping": {"state": mapping_state, "task_id": self.task_id, "archive_locator": self.archive_locator, "active_locator": self.active_locator, "repo_ref": "castbox/guru-trellis", "branch_name": self.branch, "worktree_path": str(self.worktree)},
            "worktree": {"path": str(self.worktree), "exists": True, "clean": True, "branch": self.branch, "occupied_by": None},
            "active_task": {"present": active_task is not None, "task_id": active_task, "locator": self.active_locator if active_task else None},
            "blockers": blockers,
        }

    def _call(self, facts: dict | None = None) -> dict:
        facts_path = self.facts_path if facts is None else self._write_json(Path(self.temp.name) / "facts-current.json", facts)
        return invoke.run(PACKAGE, {"id": "restore-archived-task"}, ["--root", str(self.root), "--input", str(self.input_path), "--semantic-result", str(self.semantic_path), "--facts", str(facts_path)])

    def test_success_restores_archive_and_invalidates_old_authority(self) -> None:
        result = self._call()
        self.assertEqual("restored_to_phase2", result["exit_id"])
        self.assertFalse((self.root / self.archive_locator).exists())
        active = self.root / self.active_locator
        self.assertTrue(active.is_dir())
        task = json.loads((active / "task.json").read_text(encoding="utf-8"))
        self.assertEqual("in_progress", task["status"])
        self.assertNotIn("completedAt", task)
        self.assertEqual("active", json.loads(self.mapping_path.read_text(encoding="utf-8"))["state"])
        self.assertEqual(self.active_locator, (self.root / ".trellis/.runtime/current-task").read_text(encoding="utf-8").strip())
        self.assertFalse(any((active / name).exists() for name in ("phase2-check.json", "review-gate.json", "pr-readiness.json", "task-finalization-gate.json")))
        self.assertFalse((active / "finish-summary.json").exists())
        self.assertFalse(self.named_checkpoint.exists())
        self.assertFalse(self.hashed_checkpoint.exists())

    def test_exact_already_restored_retry_is_idempotent_and_read_only(self) -> None:
        self.assertEqual("restored_to_phase2", self._call()["exit_id"])
        active = self.root / self.active_locator
        watched = [active / "task.json", self.mapping_path, self.root / ".trellis/.runtime/current-task"]
        before = {str(path): (path.read_bytes(), path.stat().st_mtime_ns) for path in watched}
        facts = self._facts("active", "in_progress", self.task_id, False)
        result = self._call(facts)
        self.assertEqual("restored_to_phase2", result["exit_id"])
        after = {str(path): (path.read_bytes(), path.stat().st_mtime_ns) for path in watched}
        self.assertEqual(before, after)

    def test_same_active_task_identity_is_allowed_without_completed_at(self) -> None:
        self.assertEqual("restored_to_phase2", self._call()["exit_id"])
        facts = self._facts("active", "in_progress", self.task_id, False)
        del facts["task"]["completed_at"]
        result = self._call(facts)
        self.assertEqual("restored_to_phase2", result["exit_id"])

    def test_stale_authority_symlink_blocks_before_any_write(self) -> None:
        authority = self.root / self.archive_locator / "review-gate.json"
        authority.unlink()
        authority.symlink_to("missing-review-gate.json")
        current_task = self.root / ".trellis/.runtime/current-task"
        watched = {
            str(self.root / self.archive_locator / "task.json"): (self.root / self.archive_locator / "task.json").read_bytes(),
            str(self.mapping_path): self.mapping_path.read_bytes(),
            str(current_task): None,
        }
        result = self._call()
        self.assertEqual("restore_blocked", result["exit_id"])
        self.assertEqual("identity_drift", result["reason_code"])
        self.assertTrue(result["zero_writes"])
        self.assertTrue((self.root / self.archive_locator).is_dir())
        self.assertEqual(watched[str(self.root / self.archive_locator / "task.json")], (self.root / self.archive_locator / "task.json").read_bytes())
        self.assertEqual(watched[str(self.mapping_path)], self.mapping_path.read_bytes())
        self.assertFalse(current_task.exists())
        self.assertTrue(authority.is_symlink())

    def test_owner_checkpoint_symlink_blocks_before_any_write(self) -> None:
        checkpoint = self.named_checkpoint / "phase2-check.json"
        checkpoint.unlink()
        checkpoint.symlink_to("missing-phase2-check.json")
        before = (self.root / self.archive_locator / "task.json").read_bytes()

        result = self._call()

        self.assertEqual("restore_blocked", result["exit_id"])
        self.assertEqual("identity_drift", result["reason_code"])
        self.assertTrue(result["zero_writes"])
        self.assertEqual(before, (self.root / self.archive_locator / "task.json").read_bytes())
        self.assertTrue(checkpoint.is_symlink())

    def test_intermediate_task_symlink_fails_before_any_write(self) -> None:
        archive = self.root / self.archive_locator
        real_parent = self.root / ".trellis/tasks/archive-storage/2026-09"
        real_parent.mkdir(parents=True)
        archive.rename(real_parent / archive.name)
        archive.parent.rmdir()
        archive.parent.symlink_to("../archive-storage/2026-09")
        before = {
            str(self.mapping_path): self.mapping_path.read_bytes(),
            str(real_parent / archive.name / "task.json"): (real_parent / archive.name / "task.json").read_bytes(),
        }

        with self.assertRaises(CommandError) as raised:
            self._call()

        self.assertEqual("unsafe_path", raised.exception.code)
        self.assertEqual(before, {
            str(self.mapping_path): self.mapping_path.read_bytes(),
            str(real_parent / archive.name / "task.json"): (real_parent / archive.name / "task.json").read_bytes(),
        })

    def test_archive_and_active_conflict_returns_zero_write(self) -> None:
        active = self.root / self.active_locator
        active.mkdir(parents=True)
        (active / "unrelated.txt").write_text("keep\n", encoding="utf-8")
        watched = {str(path): path.read_bytes() for path in (self.mapping_path, active / "unrelated.txt")}
        result = self._call()
        self.assertEqual({"restore_blocked", "archive_conflict", True}, {result["exit_id"], result["reason_code"], result["zero_writes"]})
        self.assertEqual(watched, {str(path): path.read_bytes() for path in (self.mapping_path, active / "unrelated.txt")})
        self.assertTrue((self.root / self.archive_locator).exists())

    def test_non_git_worktree_and_actual_head_drift_are_zero_write(self) -> None:
        non_git = Path(self.temp.name) / "not-a-worktree"
        non_git.mkdir()
        facts = self._facts("archived", "completed", None, False)
        facts["worktree"]["path"] = str(non_git)
        facts["runtime_mapping"]["worktree_path"] = str(non_git)
        mapping = json.loads(self.mapping_path.read_text(encoding="utf-8"))
        mapping["worktree_path"] = str(non_git)
        self._write_json(self.mapping_path, mapping)
        result = self._call(facts)
        self.assertEqual("dirty_worktree", result["reason_code"])
        self.assertTrue(result["zero_writes"])

        self._write_json(self.mapping_path, self.mapping)
        subprocess.run(["git", "-C", str(self.worktree), "commit", "--allow-empty", "-q", "-m", "test: drift"], check=True)
        result = self._call()
        self.assertEqual("head_drift", result["reason_code"])
        self.assertTrue(result["zero_writes"])

    def test_missing_or_unreachable_archive_commit_is_zero_write(self) -> None:
        public = dict(self.public)
        public["archive_commit"] = "a" * 40
        input_path = self._write_json(Path(self.temp.name) / "missing-archive-commit.json", public)
        finish_summary = self.root / self.archive_locator / "finish-summary.json"
        summary = json.loads(finish_summary.read_text(encoding="utf-8"))
        summary["archive_commit"] = public["archive_commit"]
        self._write_json(finish_summary, summary)
        facts = self._facts("archived", "completed", None, False)
        facts["archive"]["commit"] = public["archive_commit"]
        facts["archive"]["finish_summary_sha256"] = __import__("hashlib").sha256(finish_summary.read_bytes()).hexdigest()
        result = invoke.run(PACKAGE, {"id": "restore-archived-task"}, ["--root", str(self.root), "--input", str(input_path), "--semantic-result", str(self.semantic_path), "--facts", str(self._write_json(Path(self.temp.name) / "missing-archive-facts.json", facts))])
        self.assertEqual("head_drift", result["reason_code"])
        self.assertTrue(result["zero_writes"])

    def test_non_regular_current_task_pointer_is_zero_write(self) -> None:
        current_task = self.root / ".trellis/.runtime/current-task"
        current_task.mkdir(parents=True)
        result = self._call()
        self.assertEqual("active_task_conflict", result["reason_code"])
        self.assertTrue(result["zero_writes"])
        self.assertTrue((self.root / self.archive_locator).exists())

    def test_external_blocker_head_drift_and_dirty_worktree_are_zero_write(self) -> None:
        for name, facts, expected in (
            ("external", self._facts("archived", "completed", None, True), "external_blocker"),
            ("head", {**self._facts("archived", "completed", None, False), "pr": {**self._facts("archived", "completed", None, False)["pr"], "head_sha": "2" * 40}}, "head_drift"),
            ("dirty", {**self._facts("archived", "completed", None, False), "worktree": {**self._facts("archived", "completed", None, False)["worktree"], "clean": False}}, "dirty_worktree"),
        ):
            with self.subTest(name=name):
                before = {str(path): path.read_bytes() for path in (self.mapping_path, self.root / self.archive_locator / "task.json")}
                result = self._call(facts)
                self.assertEqual(expected, result["reason_code"])
                self.assertTrue(result["zero_writes"])
                self.assertEqual(before, {str(path): path.read_bytes() for path in (self.mapping_path, self.root / self.archive_locator / "task.json")})

    def test_active_task_conflict_and_merged_pr_fail_closed(self) -> None:
        for name, facts, expected in (
            ("active", {**self._facts("archived", "completed", "other-task", False), "active_task": {"present": True, "task_id": "other-task", "locator": ".trellis/tasks/other-task"}}, "active_task_conflict"),
            ("merged", {**self._facts("archived", "completed", None, False), "pr": {**self._facts("archived", "completed", None, False)["pr"], "state": "MERGED"}}, "merged_pr"),
        ):
            with self.subTest(name=name):
                result = self._call(facts)
                self.assertEqual(expected, result["reason_code"])
                self.assertTrue(result["zero_writes"])
                self.assertTrue((self.root / self.archive_locator).exists())

    def test_public_and_runtime_outputs_validate(self) -> None:
        result = self._call()
        schema = json.loads((PACKAGE / "schemas/public-restored-output.schema.json").read_text(encoding="utf-8"))
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(result)))
        self.assertEqual({"exit_id", "task_ref", "resume_target"}, set(result))

    def test_invalid_public_input_fails_before_runtime_writes(self) -> None:
        invalid = copy.deepcopy(self.public)
        invalid["resume_target"] = "planning"
        invalid_path = self._write_json(Path(self.temp.name) / "invalid.json", invalid)
        with self.assertRaises(CommandError):
            invoke.run(PACKAGE, {"id": "restore-archived-task"}, ["--root", str(self.root), "--input", str(invalid_path), "--semantic-result", str(self.semantic_path), "--facts", str(self.facts_path)])
        self.assertTrue((self.root / self.archive_locator).exists())


if __name__ == "__main__":
    unittest.main()
