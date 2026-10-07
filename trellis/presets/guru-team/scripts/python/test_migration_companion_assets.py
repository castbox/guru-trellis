"""Focused exact companion preservation and ordinary reapply checks."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import apply_guru_team_trellis_preset as preset
from migration_companion_assets import install_companions, ensure_companion_modes


class CompanionPreservationTests(unittest.TestCase):
    def test_reviewed_preserve_exits_managed_ownership_and_reapply_keeps_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            src = root / "source"
            dst = root / ".trellis/guru-team"
            relative = Path("scripts/bash/check-env.sh")
            (src / relative).parent.mkdir(parents=True)
            (src / relative).write_text("canonical\n")
            target = dst / relative
            target.parent.mkdir(parents=True)
            target.write_text("custom\n")
            target.chmod(0o640)
            path = target.relative_to(root).as_posix()
            result = install_companions(src, dst, root, (relative,), None, {path}, preset.copy_managed, preset.copy_managed_spec)
            self.assertEqual(result, [])
            ensure_companion_modes(dst, root, (relative,), {path}, result, preset.ensure_executable)
            self.assertEqual(target.read_text(), "custom\n")
            self.assertEqual(target.stat().st_mode & 0o777, 0o640)
            result = install_companions(src, dst, root, (relative,), {"install": {"managed_assets": [], "managed_asset_hashes": {}}}, set(), preset.copy_managed, preset.copy_managed_spec)
            self.assertEqual(result[0]["action"], "conflict")
            ensure_companion_modes(dst, root, (relative,), set(), result, preset.ensure_executable)
            self.assertEqual(target.read_text(), "custom\n")
            self.assertEqual(target.stat().st_mode & 0o777, 0o640)
            self.assertEqual(Path(str(target) + ".new").read_text(), "canonical\n")

    def test_normal_managed_companion_still_updates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            src = root / "source"
            dst = root / ".trellis/guru-team"
            relative = Path("config-template.yml")
            src.mkdir()
            dst.mkdir(parents=True)
            (src / relative).write_text("new\n")
            (dst / relative).write_text("old\n")
            path = (dst / relative).relative_to(root).as_posix()
            result = install_companions(src, dst, root, (relative,), {"install": {"managed_assets": [path]}}, set(), preset.copy_managed, preset.copy_managed_spec)
            self.assertEqual(result[0]["action"], "updated_managed")
            self.assertEqual((dst / relative).read_text(), "new\n")


if __name__ == "__main__":
    unittest.main()
