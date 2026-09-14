from __future__ import annotations

import importlib.util
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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
    def test_workspace_cli_consumes_shared_chain_and_preserves_legacy(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, workspace = root / "owner", root / "linked"
            task_ref = ".trellis/tasks/09-14-fixture"
            task = workspace / task_ref
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps({"creator": "stage0-transcript"}))

            def chain(installed, work, **kwargs):
                self.assertEqual(kwargs["issue"], 112)
                kwargs["setup_owner"](source)
                return [], [], {
                    "owner_repo": str(source), "workspace_path": str(workspace),
                    "task_artifact_dir": task_ref, "actual_exit": "created",
                    "checker_status": "passed", "activation": {"activation_status": "in_progress"},
                }

            with mock.patch.object(module, "six_step_transcript", side_effect=chain) as shared, \
                 mock.patch.object(module, "runtime_checkpoint", return_value={}), \
                 mock.patch.object(sys, "argv", [str(SCRIPT), "--installed-repo", str(root),
                     "--work-root", str(root / "work"), "--checkpoint", "test",
                     "--legacy-profile", "present-b"]), contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(module.main(), 0)
            result = json.loads(out.getvalue())
            shared.assert_called_once()
            self.assertTrue(result["legacy_preserved"])
            self.assertFalse(result["target_developer_identity"])
            self.assertEqual(result["activation"]["activation_status"], "in_progress")

    @unittest.skipUnless(os.environ.get("TRELLIS_INSTALLED_REPO"), "requires integrated installed candidate")
    def test_real_installed_chain_and_retired_data_preservation(self) -> None:
        module = load_module()
        installed = Path(os.environ["TRELLIS_INSTALLED_REPO"]).resolve()
        outcomes = []
        for profile in ("absent", "present-a", "present-b"):
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as directory, \
                 mock.patch.object(sys, "argv", [str(SCRIPT), "--installed-repo", str(installed),
                     "--work-root", directory, "--checkpoint", "regression", "--legacy-profile", profile]), \
                 contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(module.main(), 0)
                result = json.loads(out.getvalue())
                self.assertTrue(result["legacy_preserved"])
                self.assertEqual(result["activation"]["mapping_copies_checked"], 4)
                self.assertEqual(result["activation"]["activation_status"], "in_progress")
                self.assertEqual(len(result["activation"]["same_session_callers"]), 2)
                outcomes.append(result["lifecycle_outcome_sha256"])
        self.assertEqual(len(set(outcomes)), 1)

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
