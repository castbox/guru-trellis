from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
SCRIPT = (
    REPO
    / "trellis/presets/guru-team/scripts/python/verify_installed_task_workspace.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("verify_installed_task_workspace", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load task workspace verifier")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(SCRIPT.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(SCRIPT.parent))
    return module


class InstalledTaskWorkspaceTests(unittest.TestCase):
    def test_legacy_snapshot_records_valid_and_dangling_symlinks(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / ".trellis/workspace/alice"
            workspace.mkdir(parents=True)
            (workspace / "journal.md").write_text("legacy journal\n")
            (workspace / "latest.md").symlink_to("journal.md")
            (workspace / "missing.md").symlink_to("not-created.md")

            snapshot = module.legacy_snapshot(root)

        self.assertEqual(
            snapshot[".trellis/workspace/alice/latest.md"]["kind"], "symlink"
        )
        self.assertEqual(
            snapshot[".trellis/workspace/alice/latest.md"]["target"], "journal.md"
        )
        dangling = snapshot[".trellis/workspace/alice/missing.md"]
        self.assertEqual(dangling["kind"], "symlink")
        self.assertEqual(dangling["target"], "not-created.md")
        self.assertIsInstance(dangling["mode"], int)

    def test_legacy_snapshot_detects_symlink_replaced_by_regular_file(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / ".trellis/workspace/alice"
            workspace.mkdir(parents=True)
            link = workspace / "latest.md"
            link.symlink_to("journal.md")
            before = module.legacy_snapshot(root)

            link.unlink()
            link.write_text("journal.md")
            link.chmod(0o777)
            after = module.legacy_snapshot(root)

        self.assertNotEqual(before, after)
        self.assertEqual(
            before[".trellis/workspace/alice/latest.md"]["kind"], "symlink"
        )
        self.assertEqual(
            after[".trellis/workspace/alice/latest.md"]["kind"], "file"
        )

    def test_present_profiles_include_symlink_preservation_cases(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            present_a = module.seed_legacy_fixture(root / "a", "present-a")
            present_b = module.seed_legacy_fixture(root / "b", "present-b")

        self.assertEqual(
            present_a[".trellis/workspace/alice/latest.md"]["target"], "journal.md"
        )
        self.assertEqual(
            present_b[".trellis/workspace/bob/archive/missing.md"]["target"],
            "not-created.md",
        )


if __name__ == "__main__":
    unittest.main()
