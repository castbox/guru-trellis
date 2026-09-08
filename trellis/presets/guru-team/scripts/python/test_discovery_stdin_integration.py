from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import verify_installed_phase0_transcript as transcript


SOURCE = Path(__file__).resolve().parents[5]
INSTALLER = Path(__file__).with_name("apply_guru_team_trellis_preset.py")


def file_snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }


class DiscoveryStdinInstallationTests(unittest.TestCase):
    def test_fresh_install_and_reapply_close_the_stdin_chain(self) -> None:
        with tempfile.TemporaryDirectory(prefix="guru-384-installed-") as name:
            work = Path(name)
            installed = work / "installed"
            (installed / ".trellis").mkdir(parents=True)
            shutil.copy2(
                SOURCE / "trellis/workflows/guru-team/workflow.md",
                installed / ".trellis/workflow.md",
            )
            shutil.copytree(
                SOURCE / ".trellis/scripts", installed / ".trellis/scripts",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
            )
            environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
            for stage in ("initial", "reapply"):
                with self.subTest(stage=stage):
                    applied = subprocess.run(
                        [sys.executable, str(INSTALLER), "--repo", str(installed), "--json"],
                        env=environment, text=True, capture_output=True, check=False,
                    )
                    self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
                    self.assertEqual(list(installed.rglob("*.new")), [])
                    self.assertEqual(list(installed.rglob("*.bak")), [])
                    self.assertEqual(list(installed.rglob("__pycache__")), [])
                    self.run_chain(installed, work / stage)

    def run_chain(self, installed: Path, chain: Path) -> None:
        root, env = transcript.stage_transcript_owner_repo(installed, chain)
        # The fixture supplies remote responses; actual installed wrappers own the chain.
        sync, _ = transcript.invoke_public(
            root, env, "guru-sync-base",
            {"schema_version": "1.0", "public_input": {
                "source_exit": "start", "mode": "workflow", "repo_root": ".",
                "base_branch": "main", "route": "repo_change",
            }},
            "synced",
        )
        public, _ = transcript.project_installed_output(root, "guru-sync-base", "synced", sync)
        before_files = file_snapshot(root)
        before_siblings = {p.relative_to(chain).as_posix() for p in chain.rglob("*")}
        before_status = transcript.run(["git", "status", "--porcelain=v1", "--ignored"], cwd=root).stdout
        before_worktrees = transcript.run(["git", "worktree", "list", "--porcelain"], cwd=root).stdout
        owner, checked, public = transcript.checked_context_owner_for_issue(root, env, public, sync["transition"])
        self.assertEqual(checked["typed_exit"], "context_ready")
        discovered, _ = transcript.invoke_public(
            root, env, "guru-discover-change-context",
            {"schema_version": "1.0", "public_input": public, "transition": sync["transition"],
             "owner_context": {}, "owner_result": owner},
            "context_ready",
        )
        self.assertEqual(set(discovered), {
            "exit_id", "handoff_profile", "handoff_mode", "handoff_target_locator",
            "handoff_continuation_id", "duplicate_snapshot", "transition",
        })
        clarity_owner, _ = transcript.clarification_owner_for_issue(
            root, env, discovered["transition"], discovered["duplicate_snapshot"],
        )
        clarity, _ = transcript.invoke_public(
            root, env, "guru-clarify-requirements",
            {"schema_version": "1.0", "public_input": {
                "profile": "initial_change_request", "source_exit": "context_ready", "mode": "workflow",
                "target_locator": discovered["transition"]["target_locator"],
                "continuation_id": discovered["transition"]["continuation_id"],
                "duplicate_snapshot": discovered["duplicate_snapshot"],
            }, "transition": discovered["transition"], "owner_context": {}, "owner_result": clarity_owner},
            "clear",
        )
        self.assertEqual(clarity["exit_id"], "clear")
        self.assertEqual(file_snapshot(root), before_files)
        self.assertEqual({p.relative_to(chain).as_posix() for p in chain.rglob("*")}, before_siblings)
        self.assertEqual(transcript.run(["git", "status", "--porcelain=v1", "--ignored"], cwd=root).stdout, before_status)
        self.assertEqual(transcript.run(["git", "worktree", "list", "--porcelain"], cwd=root).stdout, before_worktrees)
        self.assertFalse((root / ".trellis/tasks").exists())
        self.assertFalse((root / ".trellis/workspace").exists())
        self.assertEqual(list(root.rglob("__pycache__")), [])
        self.assertEqual(list(root.rglob("*.pyc")), [])
        transcript.assert_forbidden_runtime_absent(root)


if __name__ == "__main__":
    unittest.main()
