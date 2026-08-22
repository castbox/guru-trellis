import os
import tempfile
import unittest
from pathlib import Path

from runtime.temporary_lifecycle import cleanup, controlled_root, entry, reap_stale, temporary_directory


class TemporaryLifecycleTests(unittest.TestCase):
    def test_inventory_has_exact_contract_prefixes(self):
        self.assertEqual(
            [item.prefix for item in __import__("runtime.temporary_lifecycle", fromlist=["INVENTORY"]).INVENTORY],
            [
                "guru-team-preset-stage-",
                "guru-trellis-install.",
                "guru-extension-verification-",
                "guru-task-commit-input.",
                "guru-phase2-input.",
            ],
        )

    def test_context_manager_cleans_success_and_failure(self):
        with tempfile.TemporaryDirectory() as root:
            with temporary_directory("preset_staging", root=Path(root)) as path:
                self.assertTrue(path.is_dir())
            self.assertFalse(path.exists())
            with self.assertRaisesRegex(RuntimeError, "primary"):
                with temporary_directory("preset_staging", root=Path(root)) as path:
                    raise RuntimeError("primary")
            self.assertFalse(path.exists())

    def test_reaper_matches_exact_prefix_and_keeps_unknown_objects(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            stale = root_path / "guru-trellis-install.stale"
            stale.mkdir()
            unknown = root_path / "guru-other.stale"
            unknown.mkdir()
            result = reap_stale("throwaway_install", root=root_path)
            self.assertEqual(result[0]["disposition"], "deleted")
            self.assertTrue(unknown.exists())

    def test_live_and_non_stale_are_retained(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            live = root_path / "guru-extension-verification-live"
            live.mkdir()
            current = root_path / "guru-extension-verification-current"
            current.mkdir()
            self.assertEqual(cleanup("extension_verification", live, root=root_path, live=True)["disposition"], "retained_live")
            self.assertEqual(cleanup("extension_verification", current, root=root_path, stale=False)["disposition"], "retained_non_stale")

    def test_local_policy_is_unverified_not_pass(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "guru-task-commit-input.fixture"
            path.write_text("fixture")
            result = cleanup("task_commit_input", path, root=Path(root), deletion_allowed=False)
            self.assertEqual(result["disposition"], "deletion_unverified")
            self.assertTrue(path.exists())

    def test_unsafe_root_and_target_fail_closed(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            outside = root_path.parent / f"guru-trellis-install-outside-{root_path.name}"
            outside.mkdir()
            result = cleanup("throwaway_install", outside, root=root_path)
            self.assertEqual(result["disposition"], "retained_non_stale")
            self.assertTrue(outside.exists())
            with self.assertRaises(ValueError):
                controlled_root("throwaway_install", environ={"TMPDIR": str(root_path / "missing")})


if __name__ == "__main__":
    unittest.main()
