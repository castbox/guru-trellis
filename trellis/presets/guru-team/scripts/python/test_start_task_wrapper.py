from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[5]


class StartTaskWrapperTests(unittest.TestCase):
    def test_wrapper_blocks_before_upstream_task_start_when_boundary_fails(self):
        with tempfile.TemporaryDirectory(prefix="guru-start-task-") as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            wrapper = root / ".trellis/guru-team/scripts/bash/start-task.sh"
            wrapper.parent.mkdir(parents=True)
            wrapper.write_bytes(
                (SOURCE / "trellis/workflows/guru-team/scripts/bash/start-task.sh").read_bytes()
            )
            wrapper.chmod(0o755)

            boundary = wrapper.parent / "check-workspace-boundary.sh"
            boundary.write_text("#!/usr/bin/env bash\nexit 7\n", encoding="utf-8")
            boundary.chmod(0o755)

            marker = root / "upstream-start-ran"
            upstream = root / ".trellis/scripts/task.py"
            upstream.parent.mkdir(parents=True)
            upstream.write_text(
                "from pathlib import Path\nPath('upstream-start-ran').touch()\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [str(wrapper), ".trellis/tasks/identity"],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 7)
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
