from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
GURU_ROOT = PACKAGE.parents[1]
sys.path.insert(0, str(GURU_ROOT))
sys.path.insert(0, str(PACKAGE / "runtime"))

from invoke import run as invoke  # noqa: E402
from runtime.io import CommandError  # noqa: E402
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository  # noqa: E402


TASK_REF = ".trellis/tasks/09-18-435-active-task-delivery-loop"


class DeliveryReviewRuntimeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.inputs = Path(self.tmp.name) / "inputs"
        self.inputs.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.repo)], check=True)
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("remote", "add", "origin", "git@github.com:castbox/guru-trellis.git")
        (self.repo / ".gitignore").write_text(".trellis/.runtime/\n")
        (self.repo / "base.txt").write_text("base\n")
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        self.git("switch", "-qc", "codex/435-active-task-delivery-loop")
        task = self.repo / TASK_REF
        task.mkdir(parents=True)
        (task / "task.json").write_text(
            json.dumps(
                {
                    "id": "435-active-task-delivery-loop",
                    "name": "435-active-task-delivery-loop",
                    "lifecycle_generation": 0,
                    "source": {"kind": "issue", "repo_ref": "castbox/guru-trellis",
                               "number": 435, "disposition": "exact_source"},
                    "title": "Delivery review fixture",
                    "description": "One current independently deliverable slice.",
                    "status": "in_progress",
                    "dev_type": None,
                    "scope": "GitHub issue: https://github.com/castbox/guru-trellis/issues/435",
                    "package": None,
                    "priority": "P2",
                    "createdAt": "2026-10-09",
                    "completedAt": None,
                    "base_branch": "main",
                    "worktree_path": None,
                    "commit": None,
                    "pr_url": None,
                    "children": [],
                    "parent": None,
                    "relatedFiles": [],
                    "notes": "",
                    "meta": {},
                }
            )
        )
        (self.repo / "delivery.txt").write_text("review package\n")
        self.git("add", ".")
        self.git("commit", "-qm", "delivery review candidate")
        self.head = self.git("rev-parse", "HEAD")
        self.bindings = BranchBindingStore(inspect_repository(self.repo))
        self.key = TaskLifecycleKey("435-active-task-delivery-loop", 0)
        self.bindings.establish(self.key, "codex/435-active-task-delivery-loop")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=self.repo, text=True, stdout=subprocess.PIPE, check=True
        ).stdout.strip()

    def write(self, name: str, value: dict) -> Path:
        path = self.inputs / name
        path.write_text(json.dumps(value, ensure_ascii=False))
        return path

    def public(self) -> dict:
        return {
            "profile": "delivery_review",
            "mode": "workflow",
            "task_ref": TASK_REF,
            "branch_review_commit": self.head,
        }

    def semantic(self, exit_id: str = "ready") -> dict:
        value = json.loads((PACKAGE / "examples/semantic-ready.json").read_text())
        if exit_id == "ready":
            return value
        value["route"] = {"typed_exit": exit_id}
        if exit_id == "planning_revision_required":
            self.mark_dimension(value, "delivery_policy", "finding")
            value["conclusions"]["delivery_readiness"]["status"] = "finding"
            value["findings"] = [self.finding("finding:policy", "delivery_policy", "planning_revision")]
        elif exit_id == "implementation_required":
            self.mark_dimension(value, "implementation_quality", "finding")
            value["conclusions"]["delivery_readiness"]["status"] = "finding"
            value["findings"] = [self.finding("finding:defect", "implementation_quality", "implementation")]
        elif exit_id == "scope_confirmation_required":
            self.mark_dimension(value, "requirement_authority", "finding")
            value["conclusions"]["delivery_readiness"]["status"] = "finding"
            value["scope_proposals"] = [{"proposal_ref":"proposal:scope","candidate_ref":"candidate:delivery:no-defect","summary":"Expand the approved slice.","evidence_refs":["issue:#435"],"status":"open"}]
        elif exit_id == "blocked":
            self.mark_dimension(value, "base_and_live_facts", "blocked")
            value["conclusions"]["delivery_readiness"]["status"] = "blocked"
            value["findings"] = [self.finding("finding:github", "base_and_live_facts", "external_blocker")]
            value["route"] = {"typed_exit":"blocked","reason_code":"live_github_unavailable","remediation":"Restore live GitHub evidence."}
        return value

    @staticmethod
    def mark_dimension(value: dict, dimension: str, status: str) -> None:
        next(item for item in value["dimensions"] if item["id"] == dimension)["status"] = status

    @staticmethod
    def finding(ref: str, dimension: str, route_class: str) -> dict:
        return {"finding_ref":ref,"candidate_ref":"candidate:delivery:no-defect","dimension":dimension,"summary":"Current evidence requires this route.","evidence_refs":["evidence:current"],"route_class":route_class,"status":"open","closure_evidence":[]}

    def invoke(self, semantic: dict) -> dict:
        return invoke(
            PACKAGE,
            {},
            [
                "--root", str(self.repo),
                "--input", str(self.write("input.json", self.public())),
                "--semantic-result", str(self.write("semantic.json", semantic)),
            ],
        )

    def checkpoint(self) -> Path:
        return self.repo / ".trellis/.runtime/guru-team/owner-checkpoints/09-18-435-active-task-delivery-loop/delivery-review-gate.json"

    def test_ready_projects_minimal_publish_seed_and_retires_checkpoint(self):
        output = self.invoke(self.semantic())
        self.assertEqual("ready", output["exit_id"])
        self.assertEqual(self.head, output["reviewed_head"])
        self.assertEqual("remaining", output["remaining_work_state"])
        self.assertRegex(output["delivery_cycle_ref"], r"^delivery-cycle:v1:[0-9a-f]{64}$")
        self.assertFalse(self.checkpoint().exists())

    def test_same_head_fresh_reentry_after_output_loss_and_retirement(self):
        # Each invocation supplies a fresh completed owner result. This tests
        # deterministic transport/retirement, not reuse of a semantic pass.
        lost_output = self.invoke(self.semantic())
        self.assertFalse(self.checkpoint().exists())
        recovered = self.invoke(self.semantic())
        self.assertEqual(lost_output, recovered)
        self.assertFalse(self.checkpoint().exists())

        (self.repo / "delivery.txt").write_text("finding fixed in current slice\n")
        self.git("commit", "-qam", "fix delivery candidate")
        with self.assertRaises(CommandError) as caught:
            self.invoke(self.semantic())
        self.assertEqual("stale_identity", caught.exception.code)
        self.assertFalse(self.checkpoint().exists())

    def test_missing_or_wrong_branch_binding_fails_before_checkpoint(self):
        self.bindings.path_for(self.key).unlink()
        for branch in (None, "main"):
            with self.subTest(branch=branch):
                if branch is not None:
                    self.bindings.establish(self.key, branch)
                with self.assertRaises(CommandError) as raised:
                    self.invoke(self.semantic())
                self.assertEqual("stale_identity", raised.exception.code)
                self.assertFalse(self.checkpoint().exists())

    def test_all_non_ready_exits_project_minimal_dtos_and_retire_checkpoint(self):
        expected = {
            "planning_revision_required": {"reason_refs"},
            "implementation_required": {"finding_refs", "resume_target"},
            "scope_confirmation_required": {"proposal_refs"},
            "blocked": {"reason_code", "remediation"},
        }
        for exit_id, fields in expected.items():
            with self.subTest(exit_id=exit_id):
                output = self.invoke(self.semantic(exit_id))
                self.assertEqual(exit_id, output["exit_id"])
                self.assertTrue(fields.issubset(output))
                self.assertFalse(self.checkpoint().exists())

    def test_closing_keyword_forms_fail_before_checkpoint_write(self):
        for closing_text in (
            "- Closes #435",
            "Text: fixes #435",
            "Closes castbox/guru-trellis#435",
        ):
            with self.subTest(closing_text=closing_text):
                semantic = self.semantic()
                semantic["pr_payload"]["body"] += f"\n{closing_text}\n"
                with self.assertRaises(CommandError) as raised:
                    self.invoke(semantic)
                self.assertEqual("schema_mismatch", raised.exception.code)
                self.assertFalse(self.checkpoint().exists())

    def test_issue_reference_uses_structured_source_not_free_text_scope(self):
        task_file = self.repo / TASK_REF / "task.json"
        metadata = json.loads(task_file.read_text())
        metadata["source"] = {"kind": "no_issue"}
        task_file.write_text(json.dumps(metadata))
        self.git("add", TASK_REF)
        self.git("commit", "-qm", "no issue task")
        self.head = self.git("rev-parse", "HEAD")
        semantic = self.semantic()
        semantic["pr_payload"]["body"] = semantic["pr_payload"]["body"].replace("Refs #435", "")
        self.assertEqual(self.invoke(semantic)["exit_id"], "ready")

        metadata["source"] = {"kind": "issue", "repo_ref": "castbox/guru-trellis",
                              "number": 436, "disposition": "reference_only"}
        metadata["scope"] = "delivery review without an Issue URL"
        task_file.write_text(json.dumps(metadata))
        self.git("add", TASK_REF)
        self.git("commit", "-qm", "structured issue source")
        self.head = self.git("rev-parse", "HEAD")
        with self.assertRaises(CommandError) as caught:
            self.invoke(self.semantic())
        self.assertEqual(caught.exception.field_path, "pr_payload.body")
        semantic = self.semantic()
        semantic["pr_payload"]["body"] = semantic["pr_payload"]["body"].replace("Refs #435", "Refs #436")
        self.assertEqual(self.invoke(semantic)["exit_id"], "ready")

    def test_cross_repository_source_requires_qualified_issue_reference(self):
        task_file = self.repo / TASK_REF / "task.json"
        metadata = json.loads(task_file.read_text())
        metadata["source"] = {"kind": "issue", "repo_ref": "other/repo",
                              "number": 435, "disposition": "reference_only"}
        task_file.write_text(json.dumps(metadata))
        self.git("add", TASK_REF)
        self.git("commit", "-qm", "cross repository source")
        self.head = self.git("rev-parse", "HEAD")
        with self.assertRaises(CommandError) as caught:
            self.invoke(self.semantic())
        self.assertEqual(caught.exception.field_path, "pr_payload.body")
        semantic = self.semantic()
        semantic["pr_payload"]["body"] = semantic["pr_payload"]["body"].replace("Refs #435", "Refs castbox/guru-trellis#435")
        with self.assertRaises(CommandError):
            self.invoke(semantic)
        semantic["pr_payload"]["body"] = semantic["pr_payload"]["body"].replace("Refs castbox/guru-trellis#435", "Refs other/repo#435")
        self.assertEqual(self.invoke(semantic)["exit_id"], "ready")

    def test_same_repository_short_reference_ignores_github_name_case(self):
        task_file = self.repo / TASK_REF / "task.json"
        metadata = json.loads(task_file.read_text())
        metadata["source"] = {"kind": "issue", "repo_ref": "CastBox/Guru-Trellis",
                              "number": 435, "disposition": "exact_source"}
        task_file.write_text(json.dumps(metadata))
        self.git("add", TASK_REF)
        self.git("commit", "-qm", "case variant issue source")
        self.head = self.git("rev-parse", "HEAD")
        self.assertEqual(self.invoke(self.semantic())["exit_id"], "ready")

    def test_missing_structured_source_is_not_a_current_lifecycle_candidate(self):
        task_file = self.repo / TASK_REF / "task.json"
        metadata = json.loads(task_file.read_text())
        metadata.pop("source")
        metadata["scope"] = "GitHub Issue #435"
        task_file.write_text(json.dumps(metadata))
        self.git("add", TASK_REF)
        self.git("commit", "-qm", "legacy task source")
        self.head = self.git("rev-parse", "HEAD")
        before = task_file.read_bytes()
        with self.assertRaises(CommandError) as caught:
            self.invoke(self.semantic())
        self.assertEqual(caught.exception.code, "stale_identity")
        self.assertEqual(caught.exception.field_path, TASK_REF)
        self.assertFalse(self.checkpoint().exists())
        self.assertEqual(task_file.read_bytes(), before)

        # A new semantic result cannot migrate or reactivate an unsupported
        # header. Record migration belongs to its existing installation owner.
        semantic = self.semantic()
        semantic["reviewed_source"] = {"kind": "issue", "repo_ref": "castbox/guru-trellis",
                                       "number": 435, "disposition": "reference_only"}
        with self.assertRaises(CommandError) as caught:
            self.invoke(semantic)
        self.assertEqual(caught.exception.code, "stale_identity")
        self.assertEqual(caught.exception.field_path, TASK_REF)
        self.assertEqual(task_file.read_bytes(), before)

    def test_publish_review_stale_reentry_uses_ordinary_fresh_review_input(self):
        public = self.public()
        public["branch_review_commit"] = "0" * 40
        with self.assertRaises(CommandError) as raised:
            invoke(
                PACKAGE,
                {},
                [
                    "--root", str(self.repo),
                    "--input", str(self.write("stale-input.json", public)),
                    "--semantic-result", str(self.write("stale-semantic.json", self.semantic())),
                ],
            )
        self.assertEqual("stale_identity", raised.exception.code)
        self.assertFalse(self.checkpoint().exists())

    def test_post_review_dirty_content_fails_closed(self):
        (self.repo / "delivery.txt").write_text("drift\n")
        with self.assertRaises(CommandError) as raised:
            self.invoke(self.semantic())
        self.assertEqual("stale_identity", raised.exception.code)
        self.assertFalse(self.checkpoint().exists())


if __name__ == "__main__":
    unittest.main()
