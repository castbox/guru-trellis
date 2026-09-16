"""Archived profile contract units; full producer/wrapper chain is integration-owned."""
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

from test_contract import GTT, PACKAGE, PUBLIC_WRAPPER, load_runtime


def archived_payload():
    payload = json.loads((PACKAGE / "examples/pr-readiness.json").read_text())
    payload.pop("reviewed_content_sha256")
    payload.update(json.loads((PACKAGE / "examples/public-archived-publication-review-input.json").read_text()))
    payload["schema_version"] = "1.0"
    payload["route"] = {"typed_exit": "archived_ready"}
    return payload


def finding_payload(route_class):
    payload = archived_payload()
    status = "blocked" if route_class == "external_blocker" else "finding"
    payload["route"] = {"typed_exit": "blocked", "reason_code": "current_review_finding", "remediation": "Resolve the current finding outside this read-only round."}
    payload["dimensions"][0]["status"] = status
    payload["conclusions"]["issue_scope"]["status"] = status
    payload["findings"] = [{
        "finding_ref": "publication:F1", "candidate_ref": payload["candidate_classifications"][0]["candidate_ref"],
        "dimension": payload["dimensions"][0]["id"], "summary": "Current payload needs correction.",
        "scope_basis": "Approved archive review contract.", "evidence_refs": ["current-pr"],
        "affected_artifacts": ["PR body"], "route_class": route_class, "status": "open", "closure_evidence": [],
    }]
    return payload


class ArchivedSemanticTest(unittest.TestCase):
    def test_independent_variant_accepts_ready_and_truthful_blockers(self):
        schema = json.loads((PACKAGE / "schemas/archived-pr-readiness.schema.json").read_text())
        for payload in [archived_payload()] + [finding_payload(c) for c in ("metadata_revision", "task_work", "external_blocker")]:
            with self.subTest(route=payload["route"], findings=payload["findings"]):
                self.assertEqual([], GTT.skill_json_schema_validation_errors(payload, schema, "archived"))
                self.assertEqual([], GTT.task_publication_semantic_errors(payload, branch_review_commit=payload["branch_review_commit"], archived=True))

    def test_active_blocked_rules_are_not_widened(self):
        for route_class in ("metadata_revision", "task_work"):
            payload = finding_payload(route_class)
            self.assertTrue(GTT.task_publication_semantic_errors(payload, branch_review_commit=payload["branch_review_commit"]))

    def test_archived_rejects_active_route_and_mismatched_dimension(self):
        payload = finding_payload("task_work")
        payload["route"] = {"typed_exit": "return_to_task_work"}
        self.assertTrue(GTT.task_publication_semantic_errors(payload, branch_review_commit=payload["branch_review_commit"], archived=True))
        payload = finding_payload("metadata_revision")
        payload["dimensions"][0]["status"] = "blocked"
        self.assertTrue(GTT.task_publication_semantic_errors(payload, branch_review_commit=payload["branch_review_commit"], archived=True))

    def test_ready_cannot_carry_open_findings_or_nonpassed_conclusions(self):
        payload = finding_payload("task_work")
        payload["route"] = {"typed_exit": "archived_ready"}
        self.assertTrue(GTT.task_publication_semantic_errors(payload, branch_review_commit=payload["branch_review_commit"], archived=True))

    def test_projection_consumes_snapshot_and_preserves_b(self):
        payload = archived_payload()
        output = PUBLIC_WRAPPER._project_output(payload)
        self.assertEqual(set(output), {"exit_id", "task_ref", "branch_review_commit", "reviewed_base_head", "pr_title", "pr_body"})
        self.assertEqual(output["reviewed_base_head"], payload["reviewed_base_head"])
        PUBLIC_WRAPPER._validate_public_input(PACKAGE, {key: payload[key] for key in GTT.ARCHIVED_PUBLICATION_FIELDS})

    def test_semantic_input_binds_all_archived_fields(self):
        payload = archived_payload()
        public = {key: payload[key] for key in GTT.ARCHIVED_PUBLICATION_FIELDS}
        for key in ("reviewed_base_head", "branch_review_commit", "pr_payload_snapshot_sha256", "task_ref"):
            with self.subTest(field=key):
                changed = copy.deepcopy(payload)
                changed[key] += "x"
                with self.assertRaises(Exception):
                    PUBLIC_WRAPPER._validate_semantic_binding(public, changed)


class ArchivedPreflightTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.com")
        (self.root / "work.txt").write_text("base\n")
        (self.root / ".gitignore").write_text(".trellis/.runtime/\n")
        self.commit()
        base = self.git("rev-parse", "HEAD")
        self.git("checkout", "-qb", "task/example")
        self.payload = archived_payload()
        self.task = self.root / self.payload["task_ref"]
        self.task.mkdir(parents=True)
        self.task_data = {"id": "example", "status": "completed", "branch": "task/example", "base_branch": "main"}
        (self.task / "task.json").write_text(json.dumps(self.task_data))
        self.pr = {"title": self.payload["pr_payload"]["title"], "body": self.payload["pr_payload"]["body"], "url": "https://github.com/example/repo/pull/1", "isDraft": False}
        summary = {"task": {"archive_dir": self.payload["task_ref"], "status": "completed"}, "git": {"branch": "task/example", "base_branch": "main"}, "github": {"pr_url": self.pr["url"]}}
        (self.task / "finish-summary.json").write_text(json.dumps(summary))
        self.commit()
        self.head = self.git("rev-parse", "HEAD")
        self.pr["headRefOid"] = self.head
        self.payload.update(branch_review_commit=self.head, reviewed_base_head=base, pr_payload_snapshot_sha256=GTT.canonical_json_sha256(self.payload["pr_payload"]))
        self.live_base = {"ref": "refs/heads/main", "object": {"sha": base}}
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        patches = {
            "load_config": {"github_repo": "example/repo"},
            "load_task_runtime_identity": {"workspace_slug": "example"},
            "assert_workspace_boundary": None,
            "validate_github_remote_repository": "example/repo",
            "gh_json": self.live_base,
            "closeout_remote_branch_head": self.head,
            "resolve_closeout_pull_request": self.pr,
        }
        for name, value in patches.items():
            self.stack.enter_context(mock.patch.object(GTT, name, return_value=value))
        self.prepare = self.stack.enter_context(mock.patch.object(GTT, "prepare_closeout", side_effect=AssertionError("active preparation called")))
        self.rebuild = self.stack.enter_context(mock.patch.object(GTT, "rebuild_runtime_mappings", side_effect=AssertionError("mapping repair called")))

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, text=True, capture_output=True, check=True).stdout.strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def test_clean_archive_preflight_is_readonly(self):
        before = {path: path.read_bytes() for path in self.task.iterdir()}
        self.assertEqual(self.payload["pr_payload"], GTT.archived_publication_preflight(self.root, self.task, self.payload))
        self.assertEqual(before, {path: path.read_bytes() for path in self.task.iterdir()})
        self.assertEqual("", self.git("status", "--porcelain"))
        self.assertEqual(self.head, self.git("rev-parse", "HEAD"))
        GTT.load_task_runtime_identity.assert_called_with(self.task, {"github_repo": "example/repo"}, allow_rebuild=False)
        self.prepare.assert_not_called()
        self.rebuild.assert_not_called()

    def test_preflight_accepts_producer_owned_task_mapping_shape(self):
        owner = load_runtime()
        config = {"github_repo": "example/repo"}
        workspace_mapping = {
            "schema_version": "1.0", "workspace_slug": "example",
            "workspace_path": str(self.root.resolve()),
            "source_checkout": str(self.root.resolve()),
            "branch_name": self.task_data["branch"],
            "updated_at": "2026-09-16T00:00:00Z",
        }
        task_mapping = {
            "schema_version": "1.0", "task_slug": self.task_data["id"],
            "workspace_slug": "example", "workspace_path": str(self.root.resolve()),
            "task_artifact_dir": self.payload["task_ref"],
            "updated_at": "2026-09-16T00:00:00Z",
        }
        workspace_path = owner.runtime_workspace_path(self.root, config, "example")
        task_path = owner.runtime_task_path(self.root, config, self.task_data["id"])
        owner.write_json(workspace_path, workspace_mapping)
        owner.write_json(task_path, task_mapping)
        before = {path: path.read_bytes() for path in (workspace_path, task_path)}
        self.assertNotIn("task_artifact_dir", workspace_mapping)
        with ExitStack() as stack:
            for name, value in {
                "load_config": config,
                "assert_workspace_boundary": None,
                "validate_github_remote_repository": "example/repo",
                "gh_json": self.live_base,
                "closeout_remote_branch_head": self.head,
                "resolve_closeout_pull_request": self.pr,
            }.items():
                stack.enter_context(mock.patch.object(owner, name, return_value=value))
            rebuild = stack.enter_context(mock.patch.object(owner, "rebuild_runtime_mappings", side_effect=AssertionError("mapping repair called")))
            prepare = stack.enter_context(mock.patch.object(owner, "prepare_closeout", side_effect=AssertionError("active preparation called")))
            self.assertEqual(self.payload["pr_payload"], owner.archived_publication_preflight(self.root, self.task, self.payload))
            rebuild.assert_not_called()
            prepare.assert_not_called()
        self.assertEqual(before, {path: path.read_bytes() for path in (workspace_path, task_path)})
        self.assertEqual("", self.git("status", "--porcelain"))
        self.assertEqual(self.head, self.git("rev-parse", "HEAD"))

    def test_title_body_and_ready_state_drift_stop(self):
        for key, value in (("title", "Changed title"), ("body", "Changed body"), ("isDraft", True), ("headRefOid", "e" * 40)):
            with self.subTest(field=key):
                previous = self.pr[key]
                self.pr[key] = value
                with self.assertRaises(GTT.WorkflowError):
                    GTT.archived_publication_preflight(self.root, self.task, self.payload)
                self.pr[key] = previous

    def test_live_base_advance_stops(self):
        self.live_base["object"]["sha"] = "e" * 40
        with self.assertRaises(GTT.WorkflowError) as caught:
            GTT.archived_publication_preflight(self.root, self.task, self.payload)
        self.assertEqual(caught.exception.payload["field_path"], "input.reviewed_base_head")

    def test_local_base_advance_stops_even_when_ancestor(self):
        self.git("branch", "-f", "main", self.head)
        with self.assertRaises(GTT.WorkflowError):
            GTT.archived_publication_preflight(self.root, self.task, self.payload)

    def test_uncommitted_archive_stops(self):
        (self.task / "task.json").write_text(json.dumps({**self.task_data, "title": "changed"}))
        with self.assertRaises(GTT.WorkflowError):
            GTT.archived_publication_preflight(self.root, self.task, self.payload)

    def test_checker_rereads_instead_of_reusing_invocation_cache(self):
        context = mock.Mock(checked_owner_result=self.payload)
        args = argparse.Namespace(expected_exit=None)
        GTT.check_archived_publication(self.root, self.task, args, self.payload, context)
        self.pr["title"] = "Changed after record"
        with self.assertRaises(GTT.WorkflowError):
            GTT.check_archived_publication(self.root, self.task, args, self.payload, context)

    def test_public_invocation_records_checks_projects_and_retires(self):
        public = {key: self.payload[key] for key in GTT.ARCHIVED_PUBLICATION_FIELDS}
        authored = {key: value for key, value in self.payload.items() if key not in {"schema_version", "skill_id"}}
        before = {path: path.read_bytes() for path in self.task.iterdir()}
        with tempfile.TemporaryDirectory() as scratch:
            input_path = Path(scratch) / "input.json"
            semantic_path = Path(scratch) / "semantic.json"
            input_path.write_text(json.dumps(public))
            semantic_path.write_text(json.dumps(authored))
            with mock.patch.object(PUBLIC_WRAPPER, "_owner", return_value=GTT):
                output = PUBLIC_WRAPPER.run(PACKAGE, {}, [
                    "--root", str(self.root), "--input", str(input_path),
                    "--semantic-result", str(semantic_path),
                ])
        self.assertEqual("archived_ready", output["exit_id"])
        self.assertEqual(self.payload["reviewed_base_head"], output["reviewed_base_head"])
        self.assertFalse(GTT.task_publication_path(self.root, self.task).exists())
        self.assertEqual(before, {path: path.read_bytes() for path in self.task.iterdir()})
        self.assertEqual("", self.git("status", "--porcelain"))
        self.prepare.assert_not_called()
        self.rebuild.assert_not_called()

    def test_recorder_preserves_each_truthful_blocker_classification(self):
        for route_class in ("metadata_revision", "task_work", "external_blocker"):
            with self.subTest(route_class=route_class):
                payload = finding_payload(route_class)
                for key in GTT.ARCHIVED_PUBLICATION_FIELDS:
                    payload[key] = self.payload[key]
                authored = {key: value for key, value in payload.items() if key not in {"schema_version", "skill_id"}}
                args = argparse.Namespace(branch_review_commit=self.head, dry_run=False, expected_exit="blocked")
                recorded = GTT.record_archived_publication(self.root, self.task, args, authored)
                checked = GTT.check_archived_publication(self.root, self.task, args, GTT.read_json(Path(recorded["artifact_path"])))
                self.assertEqual(route_class, checked["owner_result"]["findings"][0]["route_class"])
                self.assertEqual("blocked", PUBLIC_WRAPPER._project_output(checked["owner_result"])["exit_id"])
                PUBLIC_WRAPPER._retire_checkpoint(GTT, self.root, self.task)
        self.prepare.assert_not_called()
        self.rebuild.assert_not_called()


if __name__ == "__main__":
    unittest.main()
