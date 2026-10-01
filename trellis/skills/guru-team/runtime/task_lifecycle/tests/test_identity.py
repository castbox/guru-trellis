from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.identity import (
    discover_archived_issue_candidate,
    normalize_generation,
    normalize_task_id,
    normalize_task_ref,
    resolve_task_id,
    resolve_task_ref,
    task_inventory,
)


class IdentityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        (self.repo / ".trellis/tasks/archive").mkdir(parents=True)

    def tearDown(self):
        self.temporary.cleanup()

    def write_task(self, task_ref: str, task_id: str, generation=object(), *, modern: bool = False) -> Path:
        directory = self.repo / task_ref
        directory.mkdir(parents=True)
        payload = {"id": task_id, "name": directory.name, "status": "in_progress"}
        if type(generation) is int or isinstance(generation, (str, bool, float)) or generation is None:
            payload["lifecycle_generation"] = generation
        if modern or "/archive/" not in task_ref:
            payload.update({
                "source": {"kind": "no_issue"}, "title": "Example", "description": "Example",
                "dev_type": None, "scope": None, "package": None, "priority": "P2",
                "createdAt": "2026-09-20", "completedAt": "2026-09-20",
                "base_branch": "main", "worktree_path": None, "commit": None,
                "pr_url": None, "children": [], "parent": None, "relatedFiles": [],
                "notes": "", "meta": {},
            })
            if modern:
                payload["status"] = "completed"
        (directory / "task.json").write_text(json.dumps(payload), encoding="utf-8")
        return directory

    def test_task_id_and_task_ref_are_separate(self):
        old_ref = ".trellis/tasks/09-20-readable-name"
        new_ref = ".trellis/tasks/09-20-renamed-display"
        directory = self.write_task(old_ref, "stable-task-id", 2)
        self.assertEqual(resolve_task_id(self.repo, "stable-task-id").task_ref, old_ref)
        directory.rename(self.repo / new_ref)
        resolved = resolve_task_id(self.repo, "stable-task-id")
        self.assertEqual((resolved.task_id, resolved.task_ref, resolved.lifecycle_generation), ("stable-task-id", new_ref, 2))

    def test_archive_changes_locator_without_changing_lifecycle_key(self):
        active_ref = ".trellis/tasks/09-20-demo"
        archived_ref = ".trellis/tasks/archive/2026-09/09-20-demo"
        directory = self.write_task(active_ref, "demo", 3, modern=True)
        destination = self.repo / archived_ref
        destination.parent.mkdir(parents=True)
        shutil.move(str(directory), str(destination))
        resolved = resolve_task_ref(self.repo, archived_ref, expected_task_id="demo")
        self.assertEqual(resolved.lifecycle_key, ("demo", 3))
        self.assertEqual(resolved.lifecycle_state, "archived")

    def test_missing_generation_reads_as_zero_and_invalid_values_fail(self):
        self.write_task(".trellis/tasks/09-20-legacy", "legacy")
        with self.assertRaisesRegex(LifecycleContractError, "unsupported_legacy_task"):
            resolve_task_id(self.repo, "legacy")
        for value in [True, -1, 1.0, "1", None]:
            with self.subTest(value=value), self.assertRaises(LifecycleContractError):
                normalize_generation(value)

    def test_retired_personnel_archive_is_diagnostic_only(self):
        archived = ".trellis/tasks/archive/2026-09/09-19-old"
        directory = self.write_task(archived, "old-id", 0, modern=True)
        metadata_path = directory / "task.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata.update(creator="team", assignee="team")
        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
        current = ".trellis/tasks/09-20-current"
        self.write_task(current, "current-id", 0)
        before = metadata_path.read_bytes()
        self.assertEqual(resolve_task_id(self.repo, "current-id").task_ref, current)
        self.assertEqual([row.task_id for row in task_inventory(self.repo)], ["current-id"])
        with self.assertRaisesRegex(LifecycleContractError, "unsupported_legacy_task"):
            resolve_task_id(self.repo, "old-id")
        with self.assertRaisesRegex(LifecycleContractError, "unsupported_legacy_task"):
            resolve_task_ref(self.repo, archived, expected_task_id="old-id")
        self.assertEqual(metadata_path.read_bytes(), before)

    def test_old_active_task_fields_are_not_current_candidates(self):
        ref = ".trellis/tasks/09-20-current"
        path = self.write_task(ref, "current-id", 0) / "task.json"
        current = json.loads(path.read_text(encoding="utf-8"))
        for field, value in (
            ("creator", "team"), ("assignee", "team"),
            ("delivery_target", {"repo_ref": "example/repo", "branch_ref": "main"}),
        ):
            with self.subTest(field=field):
                path.write_text(json.dumps({**current, field: value}), encoding="utf-8")
                with self.assertRaisesRegex(LifecycleContractError, "unsupported_legacy_task"):
                    resolve_task_ref(self.repo, ref)
        path.write_text(json.dumps(current), encoding="utf-8")
        self.assertEqual([row.task_id for row in task_inventory(self.repo)], ["current-id"])

    def test_exact_and_casefold_collisions_fail_repository_resolution(self):
        current = ".trellis/tasks/09-20-first"
        self.write_task(current, "Task-A", 0)
        self.write_task(".trellis/tasks/archive/2026-09/09-19-second", "task-a", 1)
        with self.assertRaisesRegex(LifecycleContractError, "task_id_casefold_collision"):
            resolve_task_id(self.repo, "Task-A")
        with self.assertRaisesRegex(LifecycleContractError, "task_id_casefold_collision"):
            resolve_task_ref(self.repo, current, expected_task_id="Task-A")

    def test_exact_duplicate_task_ids_fail_repository_resolution(self):
        self.write_task(".trellis/tasks/09-20-first", "task-a", 0)
        self.write_task(".trellis/tasks/archive/2026-09/09-19-second", "task-a", 1)
        with self.assertRaisesRegex(LifecycleContractError, "task_id_casefold_collision"):
            resolve_task_id(self.repo, "task-a")

    def test_expected_id_mismatch_and_invalid_locators_fail(self):
        ref = ".trellis/tasks/09-20-demo"
        self.write_task(ref, "demo", 0)
        with self.assertRaisesRegex(LifecycleContractError, "invalid_task_identity"):
            resolve_task_ref(self.repo, ref, expected_task_id="other")
        for value in ["/tmp/task", "../task", ".trellis/tasks/archive/demo", ".trellis/tasks/demo/task.json", ".trellis\\tasks\\demo"]:
            with self.subTest(value=value), self.assertRaises(LifecycleContractError):
                normalize_task_ref(value)

    def test_symlink_backed_task_store_fails_with_contract_error(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            (repo / ".trellis").mkdir()
            store = repo / ".task-store"
            task = store / "09-20-demo"
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps({"id": "demo"}), encoding="utf-8")
            try:
                (repo / ".trellis/tasks").symlink_to(store, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"symlink unavailable: {exc}")
            with self.assertRaisesRegex(LifecycleContractError, "invalid_task_ref"):
                resolve_task_ref(repo, ".trellis/tasks/09-20-demo")

    def test_task_id_uses_exact_ascii_domain(self):
        for value in ["demo", "Demo_1.2", "9-task", "HEAD", "task.LOCK", "task.lock", "task.", "task..child"]:
            self.assertEqual(normalize_task_id(value), value)
        for value in ["", "-demo", "demo/task", "Straße", None, True]:
            with self.subTest(value=value), self.assertRaises(LifecycleContractError):
                normalize_task_id(value)

    def test_legacy_archive_issue_discovery_requires_unique_committed_source(self):
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.repo, check=True)
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/example/repo.git"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.repo, check=True)
        archive_ref = ".trellis/tasks/archive/2026-09/legacy-task"
        task = self.write_task(archive_ref, "immutable-task-id", 2)
        metadata = json.loads((task / "task.json").read_text(encoding="utf-8"))
        metadata.update({"status": "completed", "scope": "GitHub issue: https://github.com/example/repo/issues/154"})
        (task / "task.json").write_text(json.dumps(metadata), encoding="utf-8")
        (task / "finish-summary.json").write_text(json.dumps({
            "schema_version": 2,
            "task": {"archive_dir": archive_ref, "status": "completed"},
            "github": {"source_issues": []},
            "index": {"search_terms": {"issue_refs": []}},
        }), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "archive legacy task"], cwd=self.repo, check=True)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo, check=True, text=True, capture_output=True).stdout.strip()

        with self.assertRaisesRegex(LifecycleContractError, "unsupported_legacy_task"):
            discover_archived_issue_candidate(self.repo, "example/repo", 154, head)
        for repo_ref, number in (("other/repo", 154), ("example/repo", 155)):
            with self.subTest(repo_ref=repo_ref, number=number), self.assertRaisesRegex(
                LifecycleContractError, "archived_issue_candidate_not_found"
            ):
                discover_archived_issue_candidate(self.repo, repo_ref, number, head)

        second_ref = ".trellis/tasks/archive/2026-09/second-task"
        second = self.write_task(second_ref, "second-immutable-id")
        second_metadata = dict(metadata, id="second-immutable-id")
        (second / "task.json").write_text(json.dumps(second_metadata), encoding="utf-8")
        (second / "finish-summary.json").write_text(json.dumps({
            "schema_version": 2, "task": {"archive_dir": second_ref, "status": "completed"},
            "github": {"source_issues": [154]},
        }), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "second source archive"], cwd=self.repo, check=True)
        new_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo, check=True, text=True, capture_output=True).stdout.strip()
        with self.assertRaisesRegex(LifecycleContractError, "archived_issue_candidate_not_unique"):
            discover_archived_issue_candidate(self.repo, "example/repo", 154, new_head)

    def test_archived_issue_discovery_ignores_non_exact_structured_sources(self):
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.repo, check=True)
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/example/repo.git"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.repo, check=True)
        for task_id, disposition in (
            ("original-task", "exact_source"),
            ("reference-task", "reference_only"),
            ("followup-task", "follow_up"),
            ("parent-task", "parent"),
        ):
            archive_ref = f".trellis/tasks/archive/2026-09/{task_id}"
            task = self.write_task(archive_ref, task_id, 0, modern=True)
            metadata = json.loads((task / "task.json").read_text(encoding="utf-8"))
            metadata.update(status="completed", source={
                "kind": "issue", "repo_ref": "example/repo", "number": 154,
                "disposition": disposition,
            })
            (task / "task.json").write_text(json.dumps(metadata), encoding="utf-8")
            (task / "finish-summary.json").write_text(json.dumps({
                "schema_version": 2, "task": {"archive_dir": archive_ref, "status": "completed"},
                "github": {"source_issues": [154]},
            }), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "archive exact and referenced tasks"], cwd=self.repo, check=True)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo, check=True,
                              text=True, capture_output=True).stdout.strip()
        candidate = discover_archived_issue_candidate(self.repo, "example/repo", 154, head)
        self.assertEqual(candidate.task_id, "original-task")

    def test_noncanonical_legacy_issue_scope_is_not_a_locator(self):
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.repo, check=True)
        archive_ref = ".trellis/tasks/archive/2026-09/legacy-task"
        task = self.write_task(archive_ref, "immutable-task-id")
        metadata = json.loads((task / "task.json").read_text(encoding="utf-8"))
        metadata.update(status="completed", scope="GitHub Issue #237")
        (task / "task.json").write_text(json.dumps(metadata), encoding="utf-8")
        (task / "finish-summary.json").write_text(json.dumps({
            "schema_version": 2, "task": {"archive_dir": archive_ref, "status": "completed"},
            "github": {"source_issues": []},
        }), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "archive local issue"], cwd=self.repo, check=True)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo, check=True, text=True, capture_output=True).stdout.strip()
        with self.assertRaisesRegex(LifecycleContractError, "archived_issue_candidate_not_found"):
            discover_archived_issue_candidate(self.repo, "example/repo", 237, head)
        subprocess.run(["git", "remote", "add", "origin", "git@github.com:example/repo.git"], cwd=self.repo, check=True)
        with self.assertRaisesRegex(LifecycleContractError, "archived_issue_candidate_not_found"):
            discover_archived_issue_candidate(self.repo, "example/repo", 237, head)
        subprocess.run(["git", "remote", "set-url", "origin", "ssh://git@github.com/example/repo.git"], cwd=self.repo, check=True)
        with self.assertRaisesRegex(LifecycleContractError, "archived_issue_candidate_not_found"):
            discover_archived_issue_candidate(self.repo, "example/repo", 237, head)
        for repo_ref, number in (("other/repo", 237), ("example/repo", 238)):
            with self.subTest(repo_ref=repo_ref, number=number), self.assertRaisesRegex(
                LifecycleContractError, "archived_issue_candidate_not_found"
            ):
                discover_archived_issue_candidate(self.repo, repo_ref, number, head)

    def test_legacy_unstructured_scope_uses_committed_summary_as_candidate_only(self):
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.repo, check=True)
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/example/repo.git"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.repo, check=True)
        archive_ref = ".trellis/tasks/archive/2026-07/legacy-task"
        task = self.write_task(archive_ref, "legacy-task-id")
        metadata = json.loads((task / "task.json").read_text(encoding="utf-8"))
        metadata.update(status="completed", scope="workflow,preset,docs,companion-scripts")
        (task / "task.json").write_text(json.dumps(metadata), encoding="utf-8")
        (task / "finish-summary.json").write_text(json.dumps({
            "schema_version": 1, "task": {"archive_dir": archive_ref, "status": "completed"},
            "github": {"source_issues": [17]},
        }), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "archive unstructured source"], cwd=self.repo, check=True)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo, check=True, text=True, capture_output=True).stdout.strip()
        with self.assertRaisesRegex(LifecycleContractError, "unsupported_legacy_task"):
            discover_archived_issue_candidate(self.repo, "example/repo", 17, head)
        for repo_ref, number in (("other/repo", 17), ("example/repo", 18)):
            with self.assertRaisesRegex(LifecycleContractError, "archived_issue_candidate_not_found"):
                discover_archived_issue_candidate(self.repo, repo_ref, number, head)


if __name__ == "__main__":
    unittest.main()
