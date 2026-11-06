from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import verify_trellis_compatibility_matrix as matrix


class MatrixCaptureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.log = Path(self.temporary.name) / "command.log"

    def run_python(self, source: str, **kwargs: object) -> str:
        return matrix._run((sys.executable, "-c", source), log=self.log, **kwargs)

    def test_unicode_streams_remain_separate_when_writes_interleave(self) -> None:
        # A normal pipe write can end inside a multibyte character. Each stream
        # is valid UTF-8, even though merging their bytes would corrupt it.
        output = self.run_python(
            "import os\n"
            "glyph = '█'.encode('utf-8')\n"
            "os.write(1, glyph[:1])\n"
            "os.write(2, '警告\\n'.encode('utf-8'))\n"
            "os.write(1, glyph[1:])\n",
            capture=True,
        )
        self.assertEqual(output, "█")
        self.assertEqual(self.log.read_text(encoding="utf-8"), "stdout:\n█\nstderr:\n警告\n")

    def test_json_capture_excludes_warning_and_preserves_text_input(self) -> None:
        output = self.run_python(
            "import json, sys\n"
            "print('普通警告', file=sys.stderr)\n"
            "print(json.dumps({'input': sys.stdin.read()}, ensure_ascii=False))\n",
            capture=True,
            input_text="输入文本",
        )
        self.assertEqual(json.loads(output), {"input": "输入文本"})
        self.assertIn("普通警告", self.log.read_text(encoding="utf-8"))

    def test_nonzero_keeps_exit_code_and_both_complete_diagnostics(self) -> None:
        with self.assertRaises(matrix.MatrixError) as raised:
            self.run_python(
                "import sys\n"
                "print('标准输出')\n"
                "print('失败诊断', file=sys.stderr)\n"
                "sys.exit(7)\n"
            )
        error = raised.exception
        self.assertEqual(error.exit_code, 7)
        self.assertIn("标准输出", error.error_tail)
        self.assertIn("失败诊断", error.error_tail)
        self.assertEqual(self.log.read_text(encoding="utf-8"), error.error_tail)

    def test_success_without_capture_still_logs_both_streams(self) -> None:
        self.assertEqual(self.run_python(
            "import sys; print('out'); print('err', file=sys.stderr)"
        ), "")
        self.assertEqual(self.log.read_text(encoding="utf-8"), "stdout:\nout\n\nstderr:\nerr\n")

    def test_timeout_keeps_classification_and_both_partial_streams(self) -> None:
        with mock.patch.dict(os.environ, {"GURU_MATRIX_COMMAND_TIMEOUT_SECONDS": "1"}):
            with self.assertRaises(matrix.MatrixError) as raised:
                self.run_python(
                    "import os, time\n"
                    "os.write(1, '█'.encode('utf-8')[:1])\n"
                    "os.write(2, b'warning before deadline')\n"
                    "time.sleep(30)\n"
                )
        error = raised.exception
        self.assertEqual(error.exit_code, 124)
        self.assertIn("command timed out after 1.000s", str(error))
        self.assertIn("b'\\xe2'", error.error_tail)
        self.assertIn("warning before deadline", error.error_tail)
        self.assertIn(self.log.read_text(encoding="utf-8"), error.error_tail)


class PlatformProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.target = Path(self.temporary.name)

    def install_skill(self, *, agent: bool) -> tuple[Path, Path]:
        skill_id = "guru-agent" if agent else "guru-runtime"
        package = self.target / ".trellis/guru-team/skills/packages" / skill_id
        projection = self.target / ".agents/skills" / skill_id
        package.mkdir(parents=True)
        projection.mkdir(parents=True)
        # Runtime Interfaces retain their original wrapper contract without kind.
        invocation = (
            {"kind": "agent", "entrypoint": "SKILL.md"}
            if agent else {"wrapper": "scripts/invoke.sh"}
        )
        (package / "interface.json").write_text(json.dumps({
            "public_contracts": {"invocation": invocation},
        }))
        relative = invocation["entrypoint" if agent else "wrapper"]
        content = "# Agent entry\n" if agent else "#!/bin/sh\nexit 0\n"
        paths = (package / relative, projection / relative)
        for path in paths:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            path.chmod(0o644 if agent else 0o755)
        return paths

    def test_mixed_agent_and_runtime_entries_pass(self) -> None:
        self.install_skill(agent=True)
        self.install_skill(agent=False)
        matrix._assert_platform_projection(self.target, "codex")

    def test_missing_declared_entry_fails_for_both_types(self) -> None:
        for agent in (True, False):
            with self.subTest(agent=agent):
                package, public = self.install_skill(agent=agent)
                public.unlink()
                with self.assertRaisesRegex(matrix.MatrixError, "no .*declared"):
                    matrix._assert_platform_projection(self.target, "codex")
                # Keep the other iteration's installed package valid.
                public.write_bytes(package.read_bytes())
                public.chmod(0o644 if agent else 0o755)

    def test_declared_entry_byte_drift_fails_for_both_types(self) -> None:
        for agent in (True, False):
            with self.subTest(agent=agent):
                package, public = self.install_skill(agent=agent)
                public.write_text("ordinary local edit\n")
                with self.assertRaisesRegex(matrix.MatrixError, "drift"):
                    matrix._assert_platform_projection(self.target, "codex")
                public.write_bytes(package.read_bytes())

    def test_declared_entry_mode_drift_fails_for_both_types(self) -> None:
        for agent in (True, False):
            with self.subTest(agent=agent):
                _, public = self.install_skill(agent=agent)
                public.chmod(0o600 if agent else 0o700)
                with self.assertRaisesRegex(matrix.MatrixError, "drift"):
                    matrix._assert_platform_projection(self.target, "codex")
                public.chmod(0o644 if agent else 0o755)

    def test_runtime_wrapper_must_be_executable_even_when_modes_match(self) -> None:
        package, public = self.install_skill(agent=False)
        package.chmod(0o644)
        public.chmod(0o644)
        with self.assertRaisesRegex(matrix.MatrixError, "executable declared wrapper"):
            matrix._assert_platform_projection(self.target, "codex")

    def test_private_scripts_fail_for_both_types(self) -> None:
        for agent in (True, False):
            with self.subTest(agent=agent):
                _, public = self.install_skill(agent=agent)
                scripts = public.parent / "scripts" if agent else public.parent
                scripts.mkdir(exist_ok=True)
                private = scripts / "private.py"
                private.write_text("# private implementation\n")
                with self.assertRaisesRegex(matrix.MatrixError, "leaked private wrappers"):
                    matrix._assert_platform_projection(self.target, "codex")
                private.unlink()


if __name__ == "__main__":
    unittest.main()
