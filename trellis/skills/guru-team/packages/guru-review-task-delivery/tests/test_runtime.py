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

from runtime.io import CommandError  # noqa: E402
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository  # noqa: E402


def invoke(package, command, argv):
    result = subprocess.run(["bash", str(package / "scripts/invoke.sh"), *argv], capture_output=True, text=True)
    if result.returncode:
        error = json.loads(result.stdout or result.stderr)
        raise CommandError(error.get("code", "stale_identity"), error.get("field_path", "input"), error.get("remediation", "Reread current facts."), result.returncode)
    return json.loads(result.stdout)


TASK_REF = ".trellis/tasks/flow-task"


class DeliveryReviewRuntimeTest(unittest.TestCase):
    def setUp(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("readiness_flow", PACKAGE.parent / "guru-check-task/tests/test_delivery_flow.py")
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        self.flow = module.DeliveryFlow(); self.flow.setUp()
        self.repo = self.flow.repo
        self.inputs = self.flow.inputs
        self.git("remote", "add", "origin", "git@github.com:castbox/guru-trellis.git")
        task_file = self.repo / TASK_REF / "task.json"
        record = json.loads(task_file.read_text())
        record["source"] = {"kind":"issue","repo_ref":"castbox/guru-trellis","number":435,"disposition":"exact_source"}
        task_file.write_text(json.dumps(record))
        self.head = self.flow.head
        self.bindings = BranchBindingStore(inspect_repository(self.repo))
        self.key = TaskLifecycleKey("flow-task", 0)
        self.reviewed = self.flow.full_review(self.flow.check())

    def tearDown(self):
        self.flow.doCleanups()

    def refresh_review(self):
        # Metadata commits legitimately change the candidate anchor. Re-enter
        # through the actual owner transition and fresh Check/full Review.
        projection = self.flow.projection
        from runtime.delivery_projection.gates import rework
        from runtime.delivery_projection.adapter import authority_ref
        current = projection.resolve(self.flow.key)
        role = "readiness" if current["phase"] == "publishing" else "full_review"
        rework(projection, self.flow.key, role, "implementation",
               authority_ref(projection.planning_directory(self.flow.key) / "implement.md", self.repo),
               ["check", "full_review", "readiness"])
        self.flow.head = self.head
        projection.begin_check(self.flow.key, projection.candidate(["app.txt"], head_ref=self.head, base_ref=self.git("rev-parse", "main")))
        self.reviewed = self.flow.full_review(self.flow.check())

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
            "profile": "delivery_delivery_review",
            "delivery_key": self.flow.key,
            "full_review_result_id": self.reviewed["full_review_result_id"],
            "mode": "workflow",
            "task_ref": TASK_REF,
            "branch_review_commit": self.head,
        }

    def semantic(self, exit_id: str = "ready") -> dict:
        value = json.loads((PACKAGE / "examples/semantic-ready.json").read_text())
        if exit_id == "ready":
            return value
        value["route"] = {"typed_exit": exit_id}
        value["candidate_classifications"] = [self.classification(
            "candidate:delivery:" + exit_id, "qualified_current",
            "The current Delivery dimension requires the evidenced non-ready route.",
        )]
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
            value["scope_proposals"] = [{"proposal_ref":"proposal:scope","candidate_ref":"candidate:delivery:scope_confirmation_required","summary":"Expand the approved slice.","evidence_refs":["issue:#435"],"status":"open"}]
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
        return {"finding_ref":ref,"candidate_ref":"candidate:delivery:" + {"planning_revision":"planning_revision_required", "implementation":"implementation_required", "external_blocker":"blocked"}[route_class],"dimension":dimension,"summary":"Current evidence requires this route.","evidence_refs":["evidence:current"],"route_class":route_class,"status":"open","closure_evidence":[]}

    @staticmethod
    def classification(ref: str, decision: str, observation: str) -> dict:
        return {
            "candidate_ref": ref, "decision": decision,
            "witness": {
                "requirement_refs": ["PRD current Delivery policy and slice"],
                "supported_entry_refs": ["entry:delivery-review"],
                "existing_caller_refs": ["caller:guru-review-task-delivery"],
                "honest_action_sequence": ["Review the current slice, payload and required evidence."],
                "defect_observation": observation, "excluded_assumptions": [],
            },
            "consumer_use": "delivery_review_route_checker",
        }

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
        return self.repo / ".trellis/.runtime/guru-team/owner-checkpoints/flow-task/delivery-review-gate.json"

    def test_ready_projects_minimal_publish_seed_and_retires_checkpoint(self):
        output = self.invoke(self.semantic())
        self.assertEqual("ready", output["exit_id"])
        self.assertEqual(self.head, output["reviewed_head"])
        self.assertEqual("remaining", output["remaining_work_state"])
        self.assertEqual(output["delivery_key"], self.flow.key)
        self.assertTrue(output["readiness_result_id"].startswith("readiness:"))
        self.assertFalse(self.checkpoint().exists())

    def test_actual_nonempty_rejected_candidate_can_be_ready(self):
        semantic = self.semantic()
        semantic["candidate_classifications"] = [self.classification(
            "candidate:payload-closing-effect", "rejected_not_reproduced",
            "The inspected body uses Refs #435 and contains no closing keyword; the proposed closing effect does not reproduce.",
        )]
        self.assertEqual("ready", self.invoke(semantic)["exit_id"])
        self.assertFalse(self.checkpoint().exists())

    def test_zero_candidates_do_not_admit_an_unclassified_finding_or_proposal(self):
        for exit_id in ("implementation_required", "scope_confirmation_required"):
            with self.subTest(exit_id=exit_id):
                semantic = self.semantic(exit_id)
                semantic["candidate_classifications"] = []
                with self.assertRaises(CommandError) as caught:
                    self.invoke(semantic)
                self.assertEqual("candidate_classifications", caught.exception.field_path)
                self.assertFalse(self.checkpoint().exists())

    def test_zero_candidates_still_require_all_dimensions_and_conclusions(self):
        for missing in ("dimension", "conclusion"):
            with self.subTest(missing=missing):
                semantic = self.semantic()
                if missing == "dimension":
                    semantic["dimensions"].pop()
                else:
                    semantic["conclusions"].pop("docs_rdt_architecture")
                with self.assertRaises(CommandError):
                    self.invoke(semantic)
                self.assertFalse(self.checkpoint().exists())

    def test_same_head_fresh_reentry_after_output_loss_and_retirement(self):
        # Each invocation supplies a fresh completed owner result. This tests
        # deterministic transport/retirement, not reuse of a semantic pass.
        lost_output = self.invoke(self.semantic())
        self.assertFalse(self.checkpoint().exists())
        recovered = self.invoke(self.semantic())
        self.assertEqual(lost_output, recovered)
        self.assertFalse(self.checkpoint().exists())

        (self.repo / "app.txt").write_text("finding fixed in current slice\n")
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
                self.tearDown(); self.setUp()
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
        self.refresh_review()
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
        self.refresh_review()
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
        self.refresh_review()
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
        self.refresh_review()
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
        (self.repo / "app.txt").write_text("drift\n")
        with self.assertRaises(CommandError) as raised:
            self.invoke(self.semantic())
        self.assertEqual("stale_identity", raised.exception.code)
        self.assertFalse(self.checkpoint().exists())


if __name__ == "__main__":
    unittest.main()
