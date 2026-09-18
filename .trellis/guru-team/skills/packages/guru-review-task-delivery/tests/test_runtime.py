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
                    "status": "in_progress",
                    "scope": "GitHub issue: https://github.com/castbox/guru-trellis/issues/435",
                    "branch": "codex/435-active-task-delivery-loop",
                    "base_branch": "main",
                    "worktree_path": str(self.repo),
                }
            )
        )
        (self.repo / "delivery.txt").write_text("review package\n")
        self.git("add", ".")
        self.git("commit", "-qm", "delivery review candidate")
        self.head = self.git("rev-parse", "HEAD")

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

    def test_closing_keyword_fails_before_checkpoint_write(self):
        semantic = self.semantic()
        semantic["pr_payload"]["body"] += "\nCloses #435\n"
        with self.assertRaises(CommandError) as raised:
            self.invoke(semantic)
        self.assertEqual("schema_mismatch", raised.exception.code)
        self.assertFalse(self.checkpoint().exists())

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
