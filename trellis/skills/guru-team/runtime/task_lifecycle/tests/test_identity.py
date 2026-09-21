from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.identity import (
    normalize_generation,
    normalize_task_id,
    normalize_task_ref,
    resolve_task_id,
    resolve_task_ref,
)


class IdentityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        (self.repo / ".trellis/tasks/archive").mkdir(parents=True)

    def tearDown(self):
        self.temporary.cleanup()

    def write_task(self, task_ref: str, task_id: str, generation=object()) -> Path:
        directory = self.repo / task_ref
        directory.mkdir(parents=True)
        payload = {"id": task_id, "name": directory.name, "status": "in_progress"}
        if type(generation) is int or isinstance(generation, (str, bool, float)) or generation is None:
            payload["lifecycle_generation"] = generation
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
        directory = self.write_task(active_ref, "demo", 3)
        destination = self.repo / archived_ref
        destination.parent.mkdir(parents=True)
        shutil.move(str(directory), str(destination))
        resolved = resolve_task_ref(self.repo, archived_ref, expected_task_id="demo")
        self.assertEqual(resolved.lifecycle_key, ("demo", 3))
        self.assertEqual(resolved.lifecycle_state, "archived")

    def test_missing_generation_reads_as_zero_and_invalid_values_fail(self):
        self.write_task(".trellis/tasks/09-20-legacy", "legacy")
        self.assertEqual(resolve_task_id(self.repo, "legacy").lifecycle_generation, 0)
        for value in [True, -1, 1.0, "1", None]:
            with self.subTest(value=value), self.assertRaises(LifecycleContractError):
                normalize_generation(value)

    def test_exact_and_casefold_collisions_fail_repository_resolution(self):
        self.write_task(".trellis/tasks/09-20-first", "Task-A", 0)
        self.write_task(".trellis/tasks/archive/2026-09/09-19-second", "task-a", 1)
        with self.assertRaisesRegex(LifecycleContractError, "task_id_casefold_collision"):
            resolve_task_id(self.repo, "Task-A")

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
        for value in ["demo", "Demo_1.2", "9-task", "HEAD", "task.LOCK"]:
            self.assertEqual(normalize_task_id(value), value)
        for value in ["", "-demo", "demo/task", "task.lock", "task.", "task..child", "Straße", None, True]:
            with self.subTest(value=value), self.assertRaises(LifecycleContractError):
                normalize_task_id(value)


if __name__ == "__main__":
    unittest.main()
