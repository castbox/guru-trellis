from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]


class CheckoutPackageRuntimeTests(unittest.TestCase):
    def test_wrapper_projects_each_exact_exit(self) -> None:
        cases = [
            ("public-ensure-input.json", "semantic-ready.json", "checkout_ready"),
            ("public-resume-input.json", "semantic-resume.json", "resume_checkout_acquisition"),
            ("public-ensure-input.json", "semantic-blocked.json", "blocked"),
        ]
        for public_input, semantic, expected in cases:
            with self.subTest(semantic=semantic):
                completed = subprocess.run(
                    [str(PACKAGE / "scripts/invoke.sh"), "--input", str(PACKAGE / "examples" / public_input), "--semantic-result", str(PACKAGE / "examples" / semantic)],
                    check=True,
                    stdout=subprocess.PIPE,
                    text=True,
                )
                self.assertEqual(json.loads(completed.stdout)["exit_id"], expected)

    def test_wrapper_rejects_cross_lifecycle_result_projection(self) -> None:
        semantic = json.loads((PACKAGE / "examples/semantic-ready.json").read_text(encoding="utf-8"))
        semantic["result_ref"]["task_id"] = "another-task"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "semantic.json"
            path.write_text(json.dumps(semantic), encoding="utf-8")
            completed = subprocess.run(
                [str(PACKAGE / "scripts/invoke.sh"), "--input", str(PACKAGE / "examples/public-ensure-input.json"), "--semantic-result", str(path)],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        self.assertNotEqual(completed.returncode, 0)

    def test_wrapper_uses_shared_dispatcher_and_rejects_invalid_task_identity(self) -> None:
        public_input = json.loads((PACKAGE / "examples/public-ensure-input.json").read_text(encoding="utf-8"))
        public_input["task_artifact"]["task_id"] = "bad task"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text(json.dumps(public_input), encoding="utf-8")
            completed = subprocess.run(
                [
                    str(PACKAGE / "scripts/invoke.sh"),
                    "--input",
                    str(path),
                    "--semantic-result",
                    str(PACKAGE / "examples/semantic-ready.json"),
                ],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(json.loads(completed.stdout)["code"], "schema_mismatch")


if __name__ == "__main__":
    unittest.main()
