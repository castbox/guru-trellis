from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json


PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("establish_task_identity", PACKAGE / "runtime/invoke.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TaskIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        task = self.root / ".trellis/tasks/demo"
        task.mkdir(parents=True)
        self.task_file = task / "task.json"
        self.input = {"profile": "active_task", "mode": "workflow", "task_id": "demo", "task_ref": ".trellis/tasks/demo", "lifecycle_generation": 0}

    def task(self, **fields: object) -> None:
        self.task_file.write_text(json.dumps({"id": "demo", "status": "planning", **fields}), encoding="utf-8")

    def invoke(self, **fields: object) -> dict:
        result = MODULE.invoke(self.root, {**self.input, **fields})
        validate_json(result, PACKAGE / "schemas/public-output.schema.json", "output")
        return result

    def test_current_source_and_canonical_legacy_scope(self) -> None:
        self.task(source={"kind": "no_issue"})
        before = self.task_file.read_bytes()
        self.assertEqual(self.invoke()["source"], {"kind": "no_issue"})
        self.assertEqual(self.task_file.read_bytes(), before)
        self.task(scope="GitHub issue: https://github.com/castbox/guru-trellis/issues/454")
        before = self.task_file.read_bytes()
        self.assertEqual(self.invoke()["source"], {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454, "disposition": "exact_source"})
        self.assertEqual(self.task_file.read_bytes(), before)

    def test_ambiguous_legacy_requires_review_and_never_writes(self) -> None:
        self.task(scope="independent task")
        before = self.task_file.read_bytes()
        self.assertEqual(self.invoke()["exit_id"], "source_review_required")
        self.assertEqual(self.invoke(reviewed_source={"kind": "no_issue"})["source"], {"kind": "no_issue"})
        self.assertEqual(self.task_file.read_bytes(), before)
        with self.assertRaisesRegex(Exception, "schema_mismatch"):
            self.invoke(reviewed_source={"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454, "disposition": "exact_source"})

    def test_stale_generation_or_source_override_fails_closed(self) -> None:
        self.task(lifecycle_generation=1, source={"kind": "no_issue"})
        self.assertEqual(self.invoke()["exit_id"], "invalid_task_state")
        self.task(source={"kind": "no_issue"})
        self.assertEqual(self.invoke(reviewed_source={"kind": "no_issue"})["exit_id"], "blocked")


if __name__ == "__main__":
    unittest.main()
