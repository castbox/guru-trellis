"""Execution capability facts; fixture judgments are not independent AI Review."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
sys.path.insert(0, str(PACKAGE / "runtime"))
from execution_facts import probe_directory


class ProbeTests(unittest.TestCase):
    def test_missing_directories_are_removed_and_existing_content_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            retained = root / "existing"
            retained.mkdir()
            (retained / "record.json").write_text("unchanged")
            rows = probe_directory(retained / "new" / "child", root, "<checkout>/existing/new/child")
            self.assertEqual(["available"], [row["status"] for row in rows])
            self.assertEqual(["record.json"], [path.name for path in retained.iterdir()])
            self.assertEqual("unchanged", (retained / "record.json").read_text())

    def test_real_wrong_directory_reports_errno_without_exception_message(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "file").write_text("private content")
            rows = probe_directory(root / "file", root, "<checkout>/file")
            self.assertEqual("failed", rows[0]["status"])
            self.assertEqual("NotADirectoryError", rows[0]["exception_class"])
            self.assertEqual(20, rows[0]["errno"])
            self.assertNotIn(temporary, json.dumps(rows))
            self.assertEqual("private content", (root / "file").read_text())

    def test_write_failure_and_cleanup_failure_remain_distinct_facts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            original_unlink = Path.unlink
            def failed_cleanup(path, *args, **kwargs):
                if path.name.startswith(".guru-review-execution-"):
                    raise PermissionError(1, "private OS detail")
                return original_unlink(path, *args, **kwargs)
            with patch("execution_facts.os.fdopen", side_effect=PermissionError(13, "private detail")), patch.object(Path, "unlink", failed_cleanup):
                # fdopen's replacement does not take ownership of the descriptor.
                original_mkstemp = tempfile.mkstemp
                descriptors = []
                def tracked(*args, **kwargs):
                    fd, name = original_mkstemp(*args, **kwargs)
                    descriptors.append(fd)
                    return fd, name
                with patch("execution_facts.tempfile.mkstemp", tracked):
                    rows = probe_directory(root, root, "<temporary-directory>")
            for fd in descriptors:
                os.close(fd)
            self.assertEqual(["write_temporary_file", "cleanup_temporary_file"], [row["operation"] for row in rows])
            self.assertEqual([13, 1], [row["errno"] for row in rows])
            self.assertNotIn("private", json.dumps(rows))
            for path in root.iterdir():
                path.unlink()


class QueryTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("execution_flow", PACKAGE.parent / "guru-check-task/tests/test_delivery_flow.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.flow = module.DeliveryFlow()
        self.flow.setUp()
        self.addCleanup(self.flow.doCleanups)

    def query(self, *args, success=True):
        return self.flow.wrapper("guru-review-branch", "inspect-review-execution.sh",
                                 "--task", self.flow.task_ref, "--delivery-key", json.dumps(self.flow.key),
                                 *args, success=success)

    def test_branch_query_does_not_change_formal_records_or_leave_probe_items(self):
        task_file = self.flow.repo / self.flow.task_ref / "task.json"
        before = task_file.read_bytes()
        rows = self.query("--purpose", "branch_review", "--base-ref", "main",
                          "--head-ref", self.flow.head, "--probe-writes")["checks"]
        self.assertTrue(all(row["status"] == "available" for row in rows), rows)
        self.assertEqual(before, task_file.read_bytes())
        self.assertFalse(list(self.flow.repo.rglob(".guru-review-execution-*")))
        self.assertFalse((self.flow.repo / ".trellis/.runtime/guru-team/owner-checkpoints").exists())
        self.assertIsNone(self.flow.projection.resolve(self.flow.key)["results"]["check"])
        self.assertIsNone(self.flow.projection.resolve(self.flow.key)["results"]["full_review"])

    def test_final_plan_with_missing_receiving_session_never_probes_or_binds(self):
        from runtime.delivery_projection.adapter import official_session_port
        context = "execution-final-plan-unbound"
        official = official_session_port(self.flow.repo)
        path = official.session_path(self.flow.repo, context, official.repository_facts(self.flow.repo))
        self.assertFalse(path.exists())
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": context}):
            rows = self.query("--purpose", "planning", "--planning-purpose", "final_plan", "--probe-writes")["checks"]
        self.assertTrue(all(row["status"] == "available" for row in rows), rows)
        self.assertFalse(any("write" in row["operation"] or "temporary" in row["operation"] for row in rows))
        self.assertFalse(path.exists())
        self.assertFalse((self.flow.repo / ".trellis/.runtime/guru-team/owner-checkpoints").exists())

    def test_unrequested_probe_is_unknown_and_missing_commit_is_an_operation_fact(self):
        rows = self.query("--purpose", "branch_review", "--base-ref", "unavailable-ref",
                          "--head-ref", self.flow.head)["checks"]
        failure = next(row for row in rows if row["status"] == "failed")
        self.assertEqual("read_commit", failure["operation"])
        self.assertIsNone(failure["errno"])
        self.assertTrue(any(row["status"] == "not_probed" for row in rows))

    def test_final_plan_rejects_a_different_selection_without_overwriting_it(self):
        from runtime.delivery_projection.adapter import official_session_port
        # A second Delivery created and selected through the original public API.
        key = {**self.flow.key, "delivery_id": "5073de38-9b65-4b52-9e16-c772f062338e"}
        record = self.flow.projection.read_record()
        declaration = self.flow.projection.declaration()
        self.flow.projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": key,
            "owner_role": "creation", "owner_id": declaration["owners"]["creation"],
            "scope_ref": {"authority": record["accepted_scope"], "anchors": ["R1"]}, "profile": "local_commit"})
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "execution-other-selection"}):
            self.flow.projection.select(key)
            official = official_session_port(self.flow.repo)
            path = official.session_path(self.flow.repo, "execution-other-selection", official.repository_facts(self.flow.repo))
            before = path.read_bytes()
            error = self.query("--purpose", "planning", "--planning-purpose", "final_plan", success=False)
            self.assertEqual("stale_identity", error["code"])
            self.assertEqual(before, path.read_bytes())

    def test_candidate_assessment_does_not_require_future_author_bodies(self):
        planning = self.flow.projection.planning_directory(self.flow.key)
        (planning / "design.md").unlink()
        (planning / "implement.md").unlink()
        rows = self.query("--purpose", "planning", "--planning-purpose", "candidate_assessment")["checks"]
        self.assertTrue(all(row["status"] in {"available", "not_probed"} for row in rows), rows)
        objects = [row["location"] for row in rows if row["operation"] == "read_planning_object"]
        self.assertEqual(["<checkout>/" + self.flow.task_ref + "/" + self.flow.projection.resolve(self.flow.key)["planning_root"] + "/prd.md"], objects)

    def test_final_plan_reads_design_without_requiring_other_planning_bodies(self):
        planning = self.flow.projection.planning_directory(self.flow.key)
        (planning / "prd.md").unlink()
        (planning / "implement.md").unlink()
        rows = self.query("--purpose", "planning", "--planning-purpose", "final_plan", "--probe-writes")["checks"]
        self.assertTrue(all(row["status"] == "available" for row in rows), rows)
        objects = [row["location"] for row in rows if row["operation"] == "read_planning_object"]
        self.assertEqual(["<checkout>/" + self.flow.task_ref + "/" + self.flow.projection.resolve(self.flow.key)["planning_root"] + "/design.md"], objects)
        (planning / "design.md").unlink()
        failure = next(row for row in self.query("--purpose", "planning", "--planning-purpose", "final_plan")["checks"] if row["status"] == "failed")
        self.assertEqual("read_planning_object", failure["operation"])
        self.assertEqual("FileNotFoundError", failure["exception_class"])

    def test_declared_purpose_arguments_are_enforced_at_public_entry(self):
        for args in (("--purpose", "planning"),
                     ("--purpose", "branch_review", "--planning-purpose", "final_plan", "--base-ref", "main", "--head-ref", self.flow.head)):
            with self.subTest(args=args):
                self.assertEqual("invalid_arguments", self.query(*args, success=False)["code"])


if __name__ == "__main__":
    unittest.main()
