"""A public archive resume remains resolvable after ordinary formal Finish."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.delivery_projection.tests.test_installed_projection import DECLARATION
from runtime.delivery_projection.tests.upstream_fixture import install_common
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.identity import resolve_task_id, resolve_task_ref, task_identity_reservation
from runtime.task_lifecycle.tests.archive_resume_fixture import finish_resumed_archive, resume_manual_archive


class ArchiveResumeIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        for args in (("init", "-q", "-b", "main"), ("config", "user.email", "fixture@example.invalid"),
                     ("config", "user.name", "Fixture")):
            subprocess.run(["git", *args], cwd=self.repo, check=True)
        install_common(self.repo)
        (self.repo / ".trellis/workflow.md").write_text(
            "[trellis-runtime-contract]\n" + json.dumps(DECLARATION) + "\n[/trellis-runtime-contract]\n")
        (self.repo / ".gitignore").write_text(".trellis/.runtime/\n")
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.repo, check=True)

    def tearDown(self):
        self.temporary.cleanup()

    def assert_resolved(self, resumed, archive_ref):
        for entry, select in (
            ("id", lambda: resolve_task_id(self.repo, resumed["key"]["task_id"])),
            ("ref", lambda: resolve_task_ref(self.repo, archive_ref, expected_task_id=resumed["key"]["task_id"])),
        ):
            with self.subTest(entry=entry):
                identity = select()
                self.assertEqual(identity.task_ref, archive_ref)
                self.assertEqual(identity.lifecycle_generation, resumed["key"]["lifecycle_generation"])
                self.assertEqual(identity.lifecycle_state, "archived")
        self.assertEqual((self.repo / resumed["archive_ref"] / "task.json").read_bytes(), resumed["source_bytes"])
        self.assertEqual((self.repo / archive_ref / "migration/source-task.json").read_bytes(), resumed["source_bytes"])
        self.assertIsNotNone(task_identity_reservation(self.repo, resumed["key"]["task_id"], ".trellis/tasks/new"))
        with self.assertRaisesRegex(LifecycleContractError, "unsupported_legacy_task"):
            resolve_task_ref(self.repo, resumed["archive_ref"])

    def test_formal_finish_after_legacy_archive_resume(self):
        resumed = resume_manual_archive(self.repo, "legacy")
        self.assert_resolved(resumed, finish_resumed_archive(self.repo, resumed))

    def test_formal_finish_after_schema1_archive_resume(self):
        resumed = resume_manual_archive(self.repo, "schema1")
        self.assert_resolved(resumed, finish_resumed_archive(self.repo, resumed))

    def test_unrelated_same_id_archive_still_conflicts(self):
        resumed = resume_manual_archive(self.repo, "legacy")
        archive_ref = finish_resumed_archive(self.repo, resumed)
        # A separately retained manual archive has no public source relationship.
        other = self.repo / ".trellis/tasks/archive/2025-02/another-manual-archive"
        other.mkdir(parents=True)
        (other / "task.json").write_bytes(resumed["source_bytes"])
        for select in (lambda: resolve_task_id(self.repo, "resumed"), lambda: resolve_task_ref(self.repo, archive_ref)):
            with self.assertRaisesRegex(LifecycleContractError, "task_id_casefold_collision"):
                select()

    def test_two_formal_archives_still_conflict(self):
        resumed = resume_manual_archive(self.repo, "legacy")
        archive_ref = finish_resumed_archive(self.repo, resumed)
        # A second retained archive remains ambiguous even when both retain the source.
        other = self.repo / ".trellis/tasks/archive/2026-11/duplicate-finish-archive"
        shutil.copytree(self.repo / archive_ref, other)
        for select in (lambda: resolve_task_id(self.repo, "resumed"), lambda: resolve_task_ref(self.repo, archive_ref)):
            with self.assertRaisesRegex(LifecycleContractError, "task_id_casefold_collision"):
                select()


if __name__ == "__main__":
    unittest.main()
