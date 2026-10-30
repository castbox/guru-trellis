from __future__ import annotations

import errno
import json
import os
import tempfile
import unittest
from contextlib import chdir
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from runtime.io import CommandError, decode_json, fail, read_json, read_json_file


class JsonInputTests(unittest.TestCase):
    def error(self, operation, message):
        with self.assertRaises(CommandError) as caught:
            operation()
        error = caught.exception
        self.assertEqual((error.code, error.field_path, error.exit_status), ("invalid_json", "input", 2))
        self.assertIn(message, error.remediation)
        output = StringIO()
        with patch("sys.stdout", output):
            self.assertEqual(fail(error), 2)
        public = json.loads(output.getvalue())
        self.assertEqual(set(public), {"code", "field_path", "remediation"})
        self.assertNotIn("sensitive", output.getvalue())
        return error

    def test_inline_and_stdin_preserve_object_values(self):
        value = {"text": "中文", "items": [1, None, True]}
        encoded = json.dumps(value, ensure_ascii=False)
        self.assertEqual(read_json(encoded, "input"), value)
        stream = StringIO(encoded)
        with patch("sys.stdin", stream):
            self.assertEqual(read_json("-", "input"), value)
        self.assertEqual(stream.tell(), len(encoded))

    def test_regular_file_precedes_inline_and_symlink_still_reads_target(self):
        with tempfile.TemporaryDirectory() as directory, chdir(directory):
            source = Path("{}")
            source.write_text('{"text":"中文"}', encoding="utf-8")
            self.assertEqual(read_json("{}", "input"), {"text": "中文"})
            Path("linked.json").symlink_to(source)
            self.assertEqual(read_json("linked.json", "input"), {"text": "中文"})

    def test_long_inline_and_successful_decode_survive_path_probe_error(self):
        value = {"text": "x" * 20000}
        self.assertEqual(read_json(json.dumps(value), "input"), value)
        with patch.object(Path, "stat", side_effect=PermissionError("sensitive probe")):
            self.assertEqual(read_json('{"ok":true}', "input"), {"ok": True})
            self.error(lambda: read_json("[]", "input"), "top level must be an object")

    def test_explicit_missing_paths_and_ambiguous_mixed_input_differ(self):
        with tempfile.TemporaryDirectory() as directory, chdir(directory):
            for value in ("./sensitive.json", "../sensitive-missing/input.json", str(Path(directory) / "sensitive.json")):
                with self.subTest(value=value):
                    self.error(lambda: read_json(value, "input"), "file does not exist")
            for value in ("sensitive.json", "sensitive/missing.json", '{"sensitive":'):
                with self.subTest(value=value):
                    error = self.error(lambda: read_json(value, "input"), "neither an existing regular JSON file nor valid inline JSON")
                    self.assertNotIn("invalid syntax", error.remediation)

    def test_native_alternative_separator_recognizes_explicit_missing_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "working"
            workspace.mkdir()
            with chdir(workspace), patch("runtime.io.os.sep", "\\"), patch("runtime.io.os.altsep", "/"):
                for value in ("./sensitive.json", "../sensitive.json"):
                    with self.subTest(value=value):
                        self.error(lambda: read_json(value, "input"), "file does not exist")
                self.error(lambda: read_json("sensitive/missing.json", "input"), "neither an existing regular JSON file nor valid inline JSON")

    def test_nonregular_carriers_are_rejected_without_opening(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sensitive-directory"
            source.mkdir()
            carriers = [source]
            if hasattr(os, "mkfifo"):
                fifo = Path(directory) / "sensitive-fifo"
                os.mkfifo(fifo)
                carriers.append(fifo)
            with patch.object(Path, "read_text", side_effect=AssertionError("must not open a nonregular carrier")):
                for value in carriers:
                    with self.subTest(value=value):
                        self.error(lambda: read_json(str(value), "input"), "carrier is not a regular file")

    def test_valid_inline_remains_valid_when_same_name_is_directory(self):
        with tempfile.TemporaryDirectory() as directory, chdir(directory):
            Path("{}").mkdir()
            self.assertEqual(read_json("{}", "input"), {})

    def test_probe_failure_is_not_reported_as_body_syntax(self):
        with patch.object(Path, "stat", side_effect=OSError(errno.EACCES, "sensitive path")):
            self.error(lambda: read_json("./sensitive.json", "input"), "Cannot inspect")

    def test_file_read_failure_and_utf8_failure_are_not_body_syntax(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sensitive.json"
            source.write_bytes(b"\xff")
            self.error(lambda: read_json(str(source), "input"), "Cannot read the JSON file as UTF-8")
            source.write_text("{}", encoding="utf-8")
            with patch.object(Path, "read_text", side_effect=PermissionError("sensitive read failure")):
                self.error(lambda: read_json(str(source), "input"), "Cannot read the JSON file as UTF-8")

    def test_stdin_read_failure_has_safe_read_diagnostic(self):
        with patch("sys.stdin") as stream:
            stream.read.side_effect = OSError("sensitive read failure")
            self.error(lambda: read_json("-", "input"), "Cannot read JSON from stdin")

    def test_empty_syntax_and_type_errors_in_read_bodies_are_distinct(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sensitive.json"
            for body, message in ((" \n\t", "input is empty"), ('{"sensitive":', "invalid syntax"), ("[]", "top level must be an object")):
                with self.subTest(body=body):
                    source.write_text(body, encoding="utf-8")
                    self.error(lambda: read_json(str(source), "input"), message)
                    with patch("sys.stdin", StringIO(body)):
                        self.error(lambda: read_json("-", "input"), message)

    def test_nonobject_inline_remains_a_type_error(self):
        for body in ("[]", "1", "true", "null", '"sensitive"'):
            with self.subTest(body=body):
                self.error(lambda: read_json(body, "input"), "top level must be an object")

    def test_already_read_contract_body_does_not_resolve_another_file(self):
        with tempfile.TemporaryDirectory() as directory, chdir(directory):
            Path("1").write_text('{"incorrect":"second file"}', encoding="utf-8")
            source = Path("contract.json")
            source.write_text("1", encoding="utf-8")
            self.error(lambda: read_json_file(source, "input"), "top level must be an object")
            self.error(lambda: decode_json("1", "input"), "top level must be an object")
            source.write_text("{}", encoding="utf-8")
            self.assertEqual(read_json_file(source, "input"), {})
            Path("linked.json").symlink_to(source)
            with self.assertRaises(CommandError) as caught:
                read_json_file(Path("linked.json"), "input")
            self.assertEqual(caught.exception.code, "missing_contract")


if __name__ == "__main__":
    unittest.main()
