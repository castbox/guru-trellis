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
from execution_facts import probe_directory, run


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
        self.flow.planning_only = self._testMethodName in {
            "test_final_plan_with_missing_receiving_session_never_probes_or_binds",
            "test_final_plan_rejects_a_different_selection_without_overwriting_it",
            "test_candidate_assessment_does_not_require_future_author_bodies",
            "test_final_plan_reads_design_without_requiring_other_planning_bodies",
            "test_final_plan_query_does_not_refresh_the_index",
        }
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
        rows = self.query("--purpose", "branch_review", "--base-ref", "main", "--head-ref", self.flow.head)["checks"]
        self.assertIn({"operation": "probe_directory_write", "location": "<temporary-directory>",
                       "status": "not_probed"}, rows)

    def test_unrequested_probe_does_not_select_a_writable_temp_directory(self):
        args = ["--root", str(self.flow.repo), "--task", self.flow.task_ref,
                "--delivery-key", json.dumps(self.flow.key), "--purpose", "branch_review",
                "--base-ref", "main", "--head-ref", self.flow.head]
        with patch("execution_facts.tempfile.gettempdir",
                   side_effect=AssertionError("directory selection can write")):
            rows = run(PACKAGE, {}, args)["checks"]
        self.assertIn({"operation": "probe_directory_write", "location": "<temporary-directory>",
                       "status": "not_probed"}, rows)

    def test_branch_query_rejects_readable_commits_outside_the_bound_candidate(self):
        base = self.flow.git("rev-parse", "main").strip()
        head = self.flow.head
        for b, h, location in ((head, head, "<git-object>/base"), (base, base, "<git-object>/head")):
            with self.subTest(location=location):
                rows = self.query("--purpose", "branch_review", "--base-ref", b, "--head-ref", h,
                                  "--probe-writes")["checks"]
                self.assertEqual([("match_review_candidate", location)],
                                 [(row["operation"], row["location"]) for row in rows if row["status"] == "failed"])
                self.assertFalse(any("temporary" in row["operation"] or "write" in row["operation"] for row in rows))
        self.flow.git("commit", "--allow-empty", "-qm", "advance checkout")
        rows = self.query("--purpose", "branch_review", "--base-ref", base, "--head-ref", head)["checks"]
        self.assertEqual([("match_review_candidate", "<checkout>/HEAD")],
                         [(row["operation"], row["location"]) for row in rows if row["status"] == "failed"])

    def assert_query_preserves_index(self, *args):
        tracked = self.flow.repo / "app.txt"
        os.utime(tracked, (1_000_000_000, 1_000_000_000))
        index = self.flow.repo / ".git/index"
        before = index.read_bytes()
        with patch.dict(os.environ, {"GIT_OPTIONAL_LOCKS": "1"}):
            rows = self.query(*args)["checks"]
        self.assertFalse([row for row in rows if row["status"] == "failed"], rows)
        self.assertEqual(before, index.read_bytes())

    def test_branch_query_does_not_refresh_the_index(self):
        self.assert_query_preserves_index("--purpose", "branch_review", "--base-ref", "main",
                                          "--head-ref", self.flow.head)

    def test_final_plan_query_does_not_refresh_the_index(self):
        self.assert_query_preserves_index("--purpose", "planning", "--planning-purpose", "final_plan")

    def test_checkout_mismatch_keeps_the_original_reason(self):
        self.flow.git("branch", "-m", "replacement")
        rows = self.query("--purpose", "branch_review", "--base-ref", "main",
                          "--head-ref", self.flow.head)["checks"]
        failure, = [row for row in rows if row["status"] == "failed"]
        self.assertEqual(("read_explicit_checkout", "current_task_checkout_unresolved", "task_id"),
                         (failure["operation"], failure["reason_code"], failure["field_path"]))

    def test_branch_query_rejects_an_uncommitted_source_edit_before_probing(self):
        (self.flow.repo / "app.txt").write_text("local edit")
        rows = self.query("--purpose", "branch_review", "--base-ref", "main",
                          "--head-ref", self.flow.head, "--probe-writes")["checks"]
        self.assertEqual(["match_clean_checkout"], [row["operation"] for row in rows if row["status"] == "failed"])
        self.assertFalse(any("write" in row["operation"] for row in rows))

    def test_branch_query_preserves_official_session_read_reason(self):
        from runtime.delivery_projection.adapter import official_session_port
        context = "execution-session-read-failure"
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": context}):
            self.flow.projection.select(self.flow.key)
            official = official_session_port(self.flow.repo)
            session = official.session_path(self.flow.repo, context, official.repository_facts(self.flow.repo))

            def assert_failure(reason):
                result = self.query("--purpose", "branch_review", "--base-ref", "main",
                                    "--head-ref", self.flow.head, success=False)
                self.assertEqual("stale_identity", result["code"])
                self.assertEqual("session", result["field_path"])
                self.assertIn(reason, result["remediation"])
                self.assertNotIn(context, result["remediation"])

            mode = session.stat().st_mode
            try:
                session.chmod(0)
                if not os.access(session, os.R_OK):
                    assert_failure("binding_unreadable")
            finally:
                session.chmod(mode)
            session.write_text("invalid JSON")
            assert_failure("binding_invalid")

    def test_final_plan_rejects_a_delivery_that_has_entered_checking(self):
        rows = self.query("--purpose", "planning", "--planning-purpose", "final_plan")["checks"]
        self.assertEqual(["match_delivery_phase"], [row["operation"] for row in rows if row["status"] == "failed"])
        self.assertFalse(any(row["operation"] == "read_planning_object" for row in rows))

    def test_sessions_probe_is_needed_only_before_the_exact_selection_exists(self):
        from runtime.delivery_projection.adapter import official_session_port
        context = "execution-reuse-selection"
        session_location = "<git-common-dir>/trellis/sessions"
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": context}):
            args = ("--purpose", "branch_review", "--base-ref", "main", "--head-ref", self.flow.head, "--probe-writes")
            before = self.query(*args)["checks"]
            self.assertIn({"operation": "probe_directory_write", "location": session_location,
                           "status": "available"}, before)
            self.flow.projection.select(self.flow.key)
            official = official_session_port(self.flow.repo)
            session = official.session_path(self.flow.repo, context, official.repository_facts(self.flow.repo))
            payload = session.read_bytes()
            directory = session.parent
            mode = directory.stat().st_mode
            try:
                directory.chmod(0o555)
                after = self.query(*args)["checks"]
                self.assertEqual([{"operation": "read_session_selection", "location": session_location,
                                  "status": "available"}],
                                 [row for row in after if row["location"] == session_location])
                self.assertTrue(all(row["status"] == "available" for row in after), after)
                self.assertEqual(payload, session.read_bytes())
            finally:
                directory.chmod(mode)

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
