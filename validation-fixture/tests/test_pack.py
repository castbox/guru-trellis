"""仅验证 fixture 已有的构建行为。"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CLI = Path(__file__).resolve().parents[1] / "sandbox" / "pack.py"


class PackBuildTest(unittest.TestCase):
    def invoke(self, root, *args):
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_help_describes_output_without_building(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            before = set(root.rglob("*"))
            result = self.invoke(root, "--help")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            for expected in ("--output", "DIR", "输出目录", "dist"):
                self.assertIn(expected, result.stdout)
            self.assertEqual(set(root.rglob("*")), before)

    def test_default_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.invoke(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((root / "dist" / "package.txt").read_text(), "package\n")

    def test_explicit_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.invoke(root, "--output", "artifacts")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "artifacts" / "package.txt").is_file())
            self.assertFalse((root / "dist").exists())

    def test_existing_target_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "dist"
            target.mkdir()
            original = target / "package.txt"
            original.write_text("保留原内容\n", encoding="utf-8")
            result = self.invoke(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("目标已存在", result.stderr)
            self.assertEqual(original.read_text(encoding="utf-8"), "保留原内容\n")
            self.assertEqual([f.name for f in target.iterdir()], ["package.txt"])


if __name__ == "__main__":
    unittest.main()
