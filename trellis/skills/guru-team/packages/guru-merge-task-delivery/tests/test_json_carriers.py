"""Current Merge file/stdin admission; no live merge prerequisites are supplied."""
from contextlib import chdir
import errno
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
spec = importlib.util.spec_from_file_location("merge_carrier_owner", PACKAGE / "runtime/owner.py")
OWNER = importlib.util.module_from_spec(spec)
spec.loader.exec_module(OWNER)


class CurrentJsonCarrierTests(unittest.TestCase):
    def test_root_file_priority_package_fallback_absolute_file_and_stdin(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            package = Path(temporary) / "package"
            root.mkdir()
            package.mkdir()
            (root / "call.json").write_text('{"selected":"root"}')
            (package / "call.json").write_text('{"selected":"package"}')
            self.assertEqual(OWNER.load_json(root, package, "call.json", "input"), {"selected": "root"})
            (root / "call.json").unlink()
            self.assertEqual(OWNER.load_json(root, package, "call.json", "input"), {"selected": "package"})
            self.assertEqual(OWNER.load_json(root, package, str(package / "call.json"), "input"), {"selected": "package"})
            with patch.object(sys, "stdin", io.StringIO('{"selected":"stdin"}')):
                self.assertEqual(OWNER.load_json(root, package, "-", "review_input"), {"selected": "stdin"})

    def test_symlink_rejection_and_read_oserror_keep_original_input_error(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            original = root / "call.json"
            original.write_text('{"selected":"file"}')
            link = root / "link.json"
            link.symlink_to(original.name)
            with self.assertRaises(OWNER.CommandError) as linked:
                OWNER.load_json(root, root, str(link), "input")
            self.assertEqual((linked.exception.code, linked.exception.field_path), ("unsafe_path", "input"))
            with patch.object(Path, "read_text", side_effect=PermissionError(errno.EACCES, "Cannot read this input")):
                with self.assertRaises(OWNER.CommandError) as unreadable:
                    OWNER.load_json(root, root, str(original), "review_input")
            error = unreadable.exception
            self.assertEqual((error.code, error.field_path, error.exit_status), ("unsafe_path", "review_input", 2))
            self.assertIn("regular non-symlink UTF-8 JSON file", error.remediation)

    def test_public_entries_reject_complete_inline_input_before_any_live_read(self):
        public = json.loads((PACKAGE / "examples/public-delivery-ready-for-merge-input-1.0.json").read_text())
        encoded = json.dumps(public)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
            call = root / "call.json"
            call.write_text(encoded)
            review = root / "review.json"
            review.write_bytes((PACKAGE / "examples/semantic-review.json").read_bytes())
            provider = root / "provider"
            provider.mkdir()
            marker = root / "provider-called"
            gh = provider / "gh"
            gh.write_text("#!" + sys.executable + "\nfrom pathlib import Path\nPath(" + repr(str(marker)) + ").write_text('called')\nraise SystemExit(91)\n")
            gh.chmod(0o755)
            environment = {**os.environ, "PATH": str(provider) + os.pathsep + os.environ["PATH"]}
            cases = [
                ("preview-task-delivery-merge.sh", ["--input", encoded], "input"),
                ("record-task-delivery-merge.sh", ["--input", encoded, "--review-input", str(review)], "input"),
                ("check-task-delivery-merge.sh", ["--input", encoded], "input"),
                ("execute-task-delivery-merge.sh", ["--input", encoded], "input"),
                ("invoke.sh", ["--input", encoded, "--review-input", str(review)], "input"),
                ("record-task-delivery-merge.sh", ["--input", str(call), "--review-input", json.dumps({"review": "ordinary complete object"})], "review_input"),
            ]
            # Source wrappers retain their own canonical working directory.
            with chdir(root):
                for script, arguments, field in cases:
                    with self.subTest(script=script, field=field):
                        result = subprocess.run(["bash", str(PACKAGE / "scripts" / script), "--root", str(root), *arguments], env=environment, text=True, capture_output=True)
                        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                        error = json.loads(result.stdout)
                        self.assertEqual((error["code"], error["field_path"]), ("unsafe_path", field))
                        self.assertIn("stdin", error["remediation"])
                        self.assertIn("inline JSON is not a current Merge carrier", error["remediation"])
                        self.assertFalse(marker.exists())
            self.assertEqual(sorted(path.name for path in root.iterdir()), [".git", "call.json", "provider", "review.json"])

    def test_current_root_relative_absolute_package_file_and_stdin_share_review_diagnostic(self):
        public = (PACKAGE / "examples/public-delivery-ready-for-merge-input-1.0.json").read_text()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
            call = root / "call.json"
            call.write_text(public)
            review = root / "review.json"
            review.write_text("{}")
            errors = []
            for carrier, content in [(str(call), None), ("call.json", None),
                                     ("examples/public-delivery-ready-for-merge-input-1.0.json", None),
                                     ("-", public)]:
                result = subprocess.run(["bash", str(PACKAGE / "scripts/invoke.sh"), "--root", str(root),
                                         "--input", carrier, "--review-input", "review.json"],
                                        input=content, text=True, capture_output=True)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                error = json.loads(result.stdout)
                self.assertEqual(error["code"], "schema_mismatch")
                self.assertTrue(error["field_path"].startswith("review_input"), error)
                errors.append(error)
            self.assertTrue(all(error == errors[0] for error in errors))
            self.assertFalse((root / ".trellis").exists())

    def test_formal_legacy_keeps_inline_file_symlink_and_stdin_carriers(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
            public = {"profile": "legacy_history_verification", "root": str(root),
                      "key": {"task_id": "selected", "lifecycle_generation": 0},
                      "task_ref": ".trellis/tasks/selected",
                      "fact_refs": [{"repo_ref": "example/repo", "pr_number": 1, "reviewed_head": "a" * 40,
                                     "target_branch": "main", "head_branch": "old", "merge_commit": "b" * 40,
                                     "target_ref": "origin/main"}]}
            provider = root / "provider"
            provider.mkdir()
            gh = provider / "gh"
            gh.write_text("#!" + sys.executable + "\nraise SystemExit(1)\n")
            gh.chmod(0o755)
            encoded = json.dumps(public)
            call = root / "legacy.json"
            call.write_text(encoded)
            link = root / "legacy-link.json"
            link.symlink_to(call.name)
            outputs = []
            for carrier, content in [(encoded, None), (str(call), None), (str(link), None), ("-", encoded)]:
                result = subprocess.run(["bash", str(PACKAGE / "scripts/invoke.sh"), "--root", str(root),
                                         "--input", carrier], input=content,
                                        env={**os.environ, "PATH": str(provider) + os.pathsep + os.environ["PATH"]},
                                        text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                output = json.loads(result.stdout)
                self.assertEqual(output["exit_id"], "unverified_legacy_history")
                outputs.append(output)
            self.assertTrue(all(output == outputs[0] for output in outputs))
            self.assertFalse((root / ".trellis").exists())


if __name__ == "__main__":
    unittest.main()
