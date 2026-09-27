"""Installed checkout-boundary launcher uses the managed Python runtime."""

from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[5]


class TaskCheckoutBoundaryWrapperTests(unittest.TestCase):
    def fixture(self, root: Path) -> Path:
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
        script_dir = root / ".trellis/guru-team/scripts/bash"
        script_dir.mkdir(parents=True)
        boundary = script_dir / "check-task-checkout-boundary.sh"
        boundary.write_bytes(
            (SOURCE / "trellis/workflows/guru-team/scripts/bash/check-task-checkout-boundary.sh").read_bytes()
        )
        boundary.chmod(0o755)

        resolver = root / ".trellis/guru-team/runtime/resolve-python.sh"
        resolver.parent.mkdir(parents=True)
        resolver.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "shift 2\n"
            f"exec {shlex.quote(sys.executable)} \"$@\"\n",
            encoding="utf-8",
        )
        resolver.chmod(0o755)

        helper = root / ".trellis/guru-team/runtime/lifecycle_helpers.py"
        helper.write_text(
            "import json,sys\n"
            "assert sys.argv[1:] == ['check-task-checkout-boundary', '--json']\n"
            "print(json.dumps({'status':'ok'}))\n",
            encoding="utf-8",
        )
        return boundary

    def path_without_python(self, root: Path) -> str:
        path_bin = root / "path-bin"
        path_bin.mkdir()
        for command in ("bash", "dirname"):
            target = shutil.which(command)
            self.assertIsNotNone(target, command)
            (path_bin / command).symlink_to(target)
        return str(path_bin)

    def test_boundary_uses_managed_python_without_path_python(self) -> None:
        with tempfile.TemporaryDirectory(prefix="guru-boundary-managed-") as tmp:
            root = Path(tmp)
            boundary = self.fixture(root)
            env = {**os.environ, "PATH": self.path_without_python(root)}

            result = subprocess.run(
                [str(boundary), "--json"],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {"status": "ok"})

    def test_boundary_fails_when_managed_runtime_is_missing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="guru-boundary-missing-") as tmp:
            root = Path(tmp)
            boundary = self.fixture(root)
            (root / ".trellis/guru-team/runtime/resolve-python.sh").unlink()

            result = subprocess.run(
                [str(boundary), "--json"], cwd=root, text=True, capture_output=True, check=False
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("managed Python runtime is unavailable", result.stderr)


if __name__ == "__main__":
    unittest.main()
