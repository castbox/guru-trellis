from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[5]


class StartTaskWrapperTests(unittest.TestCase):
    def fixture(
        self,
        root: Path,
        *,
        status: str = "planning",
        worktree_path: str | None = "current",
        boundary_exit: int = 0,
        current_task_id: str = "identity",
    ) -> tuple[Path, Path, Path]:
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
        wrapper = root / ".trellis/guru-team/scripts/bash/start-task.sh"
        wrapper.parent.mkdir(parents=True)
        wrapper.write_bytes(
            (SOURCE / "trellis/workflows/guru-team/scripts/bash/start-task.sh").read_bytes()
        )
        wrapper.chmod(0o755)

        boundary = wrapper.parent / "check-workspace-boundary.sh"
        boundary.write_text(
            "#!/usr/bin/env bash\n"
            f"exit {boundary_exit}\n",
            encoding="utf-8",
        )
        boundary.chmod(0o755)

        task_dir = root / ".trellis/tasks/identity"
        task_dir.mkdir(parents=True)
        task = {
            "id": "identity",
            "name": "identity",
            "status": status,
            "branch": "main",
            "base_branch": "main",
        }
        if worktree_path is not None:
            task["worktree_path"] = str(root if worktree_path == "current" else worktree_path)
        (task_dir / "task.json").write_text(json.dumps(task), encoding="utf-8")

        counter = root / "upstream-start-count"
        upstream = root / ".trellis/scripts/task.py"
        upstream.parent.mkdir(parents=True)
        upstream.write_text(
            "from __future__ import annotations\n"
            "import json,sys\n"
            "from pathlib import Path\n"
            "root=Path(__file__).resolve().parents[2]\n"
            "task_ref='.trellis/tasks/identity'\n"
            "task_dir=(root/task_ref).resolve()\n"
            "task_file=task_dir/'task.json'\n"
            "task=json.loads(task_file.read_text())\n"
            "command=sys.argv[1]\n"
            "if command=='current':\n"
            " active=task.get('status')=='in_progress'\n"
            f" payload={{'current_task':({{'dir':task_ref,'id':{current_task_id!r},'status':task.get('status'),'branch':task.get('branch')}} if active else None),'source':('session:test' if active else 'none'),'stale':False,'invocation_root':str(root),'repository_common_dir':str(root/'.git'),'task_workspace_root':(str(root.resolve()) if active else None),'resolved_task_path':(str(task_dir) if active else None)}}\n"
            " print(json.dumps(payload))\n"
            "elif command=='start':\n"
            " counter=root/'upstream-start-count'\n"
            " count=int(counter.read_text()) if counter.exists() else 0\n"
            " counter.write_text(str(count+1))\n"
            " task['status']='in_progress'\n"
            " task_file.write_text(json.dumps(task))\n"
            " print('upstream start output that the wrapper must replace')\n"
            "else:\n"
            " raise SystemExit(2)\n",
            encoding="utf-8",
        )
        return wrapper, task_dir, counter

    def run_wrapper(self, wrapper: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(wrapper), *args],
            cwd=wrapper.parents[4],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_wrapper_blocks_before_upstream_task_start_when_boundary_fails(self):
        with tempfile.TemporaryDirectory(prefix="guru-start-task-") as tmp:
            root = Path(tmp)
            wrapper, _, counter = self.fixture(root, boundary_exit=7)

            result = self.run_wrapper(
                wrapper, "--mode", "initial", ".trellis/tasks/identity"
            )

            self.assertEqual(result.returncode, 7)
            self.assertFalse(counter.exists())

    def test_wrapper_blocks_incomplete_task_identity_after_boundary_passes(self):
        for worktree_path in (None, ""):
            with self.subTest(worktree_path=worktree_path):
                with tempfile.TemporaryDirectory(prefix="guru-start-task-identity-") as tmp:
                    root = Path(tmp)
                    wrapper, _, counter = self.fixture(
                        root, worktree_path=worktree_path
                    )

                    result = self.run_wrapper(
                        wrapper, "--mode", "initial", ".trellis/tasks/identity"
                    )

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("worktree_path", result.stderr)
                    self.assertFalse(counter.exists())

    def test_initial_returns_structured_success_and_executes_upstream_once(self):
        with tempfile.TemporaryDirectory(prefix="guru-start-task-initial-") as tmp:
            root = Path(tmp)
            wrapper, task_dir, counter = self.fixture(root)

            result = self.run_wrapper(
                wrapper, "--mode", "initial", ".trellis/tasks/identity"
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(output["exit_id"], "activated")
            self.assertEqual(output["mode"], "initial")
            self.assertTrue(output["upstream_start_executed"])
            self.assertEqual(output["task_status"], "in_progress")
            self.assertNotIn("upstream start output", result.stdout)
            self.assertEqual(counter.read_text(encoding="utf-8"), "1")
            self.assertEqual(
                json.loads((task_dir / "task.json").read_text())["status"],
                "in_progress",
            )

    def test_recovery_rematerializes_success_without_repeating_upstream_start(self):
        with tempfile.TemporaryDirectory(prefix="guru-start-task-recovery-") as tmp:
            root = Path(tmp)
            wrapper, _, counter = self.fixture(root)
            initial = self.run_wrapper(
                wrapper, "--mode", "initial", ".trellis/tasks/identity"
            )
            self.assertEqual(initial.returncode, 0, initial.stderr)

            recovered = self.run_wrapper(
                wrapper, "--mode", "recovery", ".trellis/tasks/identity"
            )

            self.assertEqual(recovered.returncode, 0, recovered.stderr)
            output = json.loads(recovered.stdout)
            self.assertEqual(output["exit_id"], "activated")
            self.assertEqual(output["mode"], "recovery")
            self.assertFalse(output["upstream_start_executed"])
            self.assertEqual(counter.read_text(encoding="utf-8"), "1")

    def test_modes_are_closed_over_task_status(self):
        cases = (("initial", "in_progress"), ("recovery", "planning"))
        for mode, status in cases:
            with self.subTest(mode=mode, status=status):
                with tempfile.TemporaryDirectory(prefix="guru-start-task-mode-") as tmp:
                    root = Path(tmp)
                    wrapper, _, counter = self.fixture(root, status=status)

                    result = self.run_wrapper(
                        wrapper, "--mode", mode, ".trellis/tasks/identity"
                    )

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(f"--mode {mode} requires task status", result.stderr)
                    self.assertFalse(counter.exists())

    def test_recovery_rejects_mismatched_current_identity(self):
        with tempfile.TemporaryDirectory(prefix="guru-start-task-current-") as tmp:
            root = Path(tmp)
            wrapper, _, counter = self.fixture(
                root, status="in_progress", current_task_id="other-task"
            )

            result = self.run_wrapper(
                wrapper, "--mode", "recovery", ".trellis/tasks/identity"
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("current active-task identity mismatch", result.stderr)
            self.assertFalse(counter.exists())

    def test_recovery_rejects_task_start_options(self):
        with tempfile.TemporaryDirectory(prefix="guru-start-task-options-") as tmp:
            root = Path(tmp)
            wrapper, _, counter = self.fixture(root, status="in_progress")

            result = self.run_wrapper(
                wrapper,
                "--mode",
                "recovery",
                ".trellis/tasks/identity",
                "--allow-empty-context",
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("accepts no task.py start options", result.stderr)
            self.assertFalse(counter.exists())


if __name__ == "__main__":
    unittest.main()
