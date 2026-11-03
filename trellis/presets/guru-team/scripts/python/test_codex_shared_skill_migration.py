"""Exercise normal old installer provenance and its shared-root successor."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import apply_guru_team_trellis_preset as preset

REPO = Path(__file__).resolve().parents[5]


class CodexSharedMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        self.dst = self.repo / ".trellis/guru-team"

    def apply(self, previous=None, platforms=None):
        return preset.install_skill_packages(
            self.repo, REPO, self.dst, platforms or {"codex", "claude"},
            {"skill_packages": previous} if previous else None,
        )

    def old_install(self):
        # The predecessor installer used these descriptors. Let its real copy
        # owner produce the prior receipt rather than constructing file hashes.
        old_codex = replace(preset.PLATFORM_BY_FLAG["codex"], skill_roots=(Path(".codex/skills"),))
        with mock.patch.dict(preset.PLATFORM_BY_FLAG, {"codex": old_codex}), mock.patch.object(
            preset, "selected_skill_roots", return_value=(Path(".agents/skills"), Path(".codex/skills"), Path(".claude/skills"))
        ):
            result = self.apply()
        self.assertEqual(result["status"], "ok", result["conflicts"])
        return result

    def test_old_managed_files_retire_after_complete_replacement_and_stay_retired(self):
        previous = self.old_install()
        upgraded = self.apply(previous)
        self.assertEqual(upgraded["status"], "ok", upgraded["conflicts"])
        self.assertFalse(any((self.repo / ".codex/skills").glob("guru-*")))
        self.assertTrue((self.repo / ".agents/skills/guru-orchestrate-issue-dag/agents/openai.yaml").is_file())
        legacy_removals = [row for row in upgraded["removals"] if row["path"].startswith(".codex/skills/")]
        self.assertTrue(legacy_removals)
        self.assertTrue(all(row["action"] == "removed_managed" for row in legacy_removals))
        reapplied = self.apply(upgraded)
        self.assertEqual(reapplied["status"], "ok", reapplied["conflicts"])
        self.assertFalse(any((self.repo / ".codex/skills").glob("guru-*")))

    def test_target_conflict_preserves_old_projection_until_normal_retry(self):
        previous = self.old_install()
        target = self.repo / ".agents/skills/guru-check-task/SKILL.md"
        original = target.read_bytes()
        target.write_bytes(original + b"\nLocal instructions.\n")
        old_paths = {row["path"] for row in previous["files"] if row["path"].startswith(".codex/skills/")}
        failed = self.apply(previous)
        self.assertEqual(failed["status"], "conflict")
        self.assertEqual(target.read_bytes(), original + b"\nLocal instructions.\n")
        self.assertTrue(all((self.repo / path).is_file() for path in old_paths))
        self.assertTrue(target.with_name("SKILL.md.new").is_file())
        target.write_bytes(original)
        target.with_name("SKILL.md.new").unlink()
        retried = self.apply(previous)
        self.assertEqual(retried["status"], "ok", retried["conflicts"])
        self.assertFalse(any((self.repo / ".codex/skills").glob("guru-*")))

    def test_old_edit_and_unknown_content_are_preserved_and_block_success(self):
        previous = self.old_install()
        edited = self.repo / ".codex/skills/guru-check-task/SKILL.md"
        content = edited.read_bytes() + b"\nLocal instructions.\n"
        edited.write_bytes(content)
        unknown = edited.parent / "local-notes.md"
        unknown.write_text("Local notes.\n")
        result = self.apply(previous)
        self.assertEqual(result["status"], "conflict")
        self.assertEqual(edited.read_bytes(), content)
        self.assertEqual(unknown.read_text(), "Local notes.\n")
        self.assertTrue(any(row["reason"] == "unmanaged_legacy_codex_skill" for row in result["conflicts"]))
        unknown.unlink()
        retried = self.apply(previous)
        self.assertEqual(retried["status"], "conflict")
        self.assertEqual(edited.read_bytes(), content)
        self.assertTrue(edited.with_name("SKILL.md.new").is_file())
        self.assertTrue(any(row["reason"] == "stale_unknown_local_edit" for row in retried["conflicts"]))

    def test_unknown_empty_legacy_directory_is_visible_and_blocks_staging(self):
        unknown = self.repo / ".codex/skills/guru-local/empty"
        unknown.mkdir(parents=True)
        staged = self.repo / "staged"
        staged.mkdir()
        preset.materialize_managed_preimage(self.repo, staged, set())
        result = preset.install_skill_packages(staged, REPO, staged / ".trellis/guru-team", {"codex"}, None)
        self.assertEqual(result["status"], "conflict")
        self.assertTrue(unknown.is_dir())
        self.assertTrue(any(row["reason"] == "legacy_codex_projection_remaining" for row in result["conflicts"]))

    def test_shared_selection_adds_and_removes_codex_only_packages(self):
        non_codex = self.apply(platforms={"claude"})
        only_codex = self.repo / ".agents/skills/guru-orchestrate-issue-sequence"
        common = self.repo / ".agents/skills/guru-check-task/SKILL.md"
        self.assertFalse(only_codex.exists())
        selected = self.apply(non_codex)
        self.assertEqual(selected["status"], "ok", selected["conflicts"])
        self.assertTrue((only_codex / "agents/openai.yaml").is_file())
        self.assertEqual(len(selected["files"]), len({row["path"] for row in selected["files"]}))
        removed = self.apply(selected, {"claude"})
        self.assertEqual(removed["status"], "ok", removed["conflicts"])
        self.assertFalse(only_codex.exists())
        self.assertTrue(common.is_file())
        self.assertTrue((self.repo / ".claude/skills/guru-check-task/SKILL.md").is_file())


class CodexSharedTransactionTests(unittest.TestCase):
    setUp = CodexSharedMigrationTests.setUp
    apply = CodexSharedMigrationTests.apply
    old_install = CodexSharedMigrationTests.old_install
    def transaction(self, hashes):
        from installer_test_support import install_reviewed_delivery_candidate, RUNTIME_RESULT
        install_reviewed_delivery_candidate(self.repo)
        workflow = REPO / "trellis/workflows/guru-team"
        (self.repo / ".trellis/workflow.md").write_bytes((workflow / "workflow.md").read_bytes())
        with mock.patch.object(preset, "ensure_managed_python_runtime", return_value=RUNTIME_RESULT):
            return preset.install_assets(workflow, self.dst, self.repo, {"codex", "claude"}, legacy_codex_hashes=hashes)

    def test_maintenance_receipt_activates_shared_projection_and_legacy_removals_together(self):
        previous = self.old_install()
        hashes = {row["path"]: row["sha256"] for row in previous["files"] if row["path"].startswith(".codex/skills/")}
        result = self.transaction(hashes)
        self.assertEqual(result["skill_packages"]["status"], "ok", result["skill_packages"]["conflicts"][:2])
        self.assertEqual(result["skill_installed_validation"]["returncode"], 0)
        self.assertFalse(any((self.repo / ".codex/skills").glob("guru-*")))
        self.assertTrue((self.repo / ".agents/skills/guru-orchestrate-issue-sequence/agents/openai.yaml").is_file())

    def test_previously_empty_managed_legacy_directories_retire_from_receipt(self):
        previous = self.old_install()
        hashes = {row["path"]: row["sha256"] for row in previous["files"] if row["path"].startswith(".codex/skills/")}
        for path in hashes:
            (self.repo / path).unlink()
        result = self.transaction(hashes)
        self.assertEqual(result["skill_packages"]["status"], "ok", result["skill_packages"]["conflicts"][:2])
        self.assertEqual(result["skill_installed_validation"]["returncode"], 0)
        self.assertFalse(any((self.repo / ".codex/skills").glob("guru-*")))

    def test_maintenance_target_conflict_keeps_legacy_preimages_and_retries(self):
        previous = self.old_install()
        hashes = {row["path"]: row["sha256"] for row in previous["files"] if row["path"].startswith(".codex/skills/")}
        target = self.repo / ".agents/skills/guru-check-task/SKILL.md"
        original = target.read_bytes()
        target.write_bytes(original + b"\nLocal instructions.\n")
        result = self.transaction(hashes)
        self.assertEqual(result["skill_packages"]["status"], "conflict")
        self.assertTrue(all((self.repo / path).is_file() for path in hashes))
        target.write_bytes(original)
        target.with_name("SKILL.md.new").unlink()
        repeated = self.transaction(hashes)
        self.assertEqual(repeated["skill_packages"]["status"], "ok", repeated["skill_packages"]["conflicts"][:2])
        self.assertEqual(repeated["skill_installed_validation"]["returncode"], 0)
        self.assertFalse(any((self.repo / ".codex/skills").glob("guru-*")))


if __name__ == "__main__":
    unittest.main()
