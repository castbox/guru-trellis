"""Publication entry behavior using the real store and a stateful remote port."""
from __future__ import annotations

from contextlib import redirect_stdout
import io
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("publication_fixture", PACKAGE / "tests/test_early_draft.py")
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class PublicationEntryTests(unittest.TestCase):
    setUp = fixture.EarlyDraftPublication.setUp
    github = fixture.EarlyDraftPublication.github
    mutate = fixture.EarlyDraftPublication.mutate
    provider_reads = fixture.EarlyDraftPublication.provider_reads

    def ready_to_prepare(self):
        from runtime.reviewed_content import reviewed_content_identity

        self.f.projection.begin_check(
            self.f.key,
            self.f.projection.candidate(["app.txt"], head_ref=self.f.head, base_ref=self.base),
        )
        review = self.f.single_review()
        self.mode = "workflow"
        self.public = {
            "profile": "delivery_prepare_publication",
            "mode": self.mode,
            "task_ref": self.f.task_ref,
            "delivery_key": self.f.key,
            "branch_review_commit": self.f.head,
            "full_review_result_id": review["full_review_result_id"],
            "architecture_assessment": {
                "head": self.f.head,
                "content_identity": "sha256:" + reviewed_content_identity(self.f.repo)["sha256"],
                "promotion_state": "no_change",
            },
        }
        self.semantic = json.loads((PACKAGE / "examples/semantic-publication-readiness-1.0.json").read_text())
        self.semantic["pr_payload"] = {"title": "完成本批交付", "body": "本次验证结果覆盖当前切片。"}
        self.release = json.loads((PACKAGE / "examples/semantic-review.json").read_text())

    def run_profile(self, input_data, review=None, identity=None):
        for module in ("current", "invoke", "readiness"):
            sys.modules.pop(module, None)
        from runtime.command import main

        args = ["invoke-guru-publish-task-delivery", "--root", str(self.f.repo), "--input", json.dumps(input_data)]
        if review is not None:
            args.extend(("--review-input", json.dumps(review)))
        if identity is not None:
            args.extend(("--confirmed-preview-sha256", identity))
        with redirect_stdout(io.StringIO()) as stdout:
            status = main(PACKAGE, args)
        value = json.loads(stdout.getvalue())
        self.assertEqual(0, status, value)
        return value

    def prepare(self):
        return self.run_profile(self.public, self.semantic)

    def execute(self, preview):
        return self.run_profile({"profile": "delivery_execute_publication", "prepared": preview},
                                self.release, preview["preview_identity"])

    def test_new_entry_prepares_without_remote_writes_and_executes_exact_preview(self):
        self.ready_to_prepare()
        preview = self.prepare()
        self.assertEqual("publication_prepared", preview["exit_id"])
        self.assertEqual(self.semantic["pr_payload"]["body"], preview["pr_body"])
        self.assertEqual(["push_content", "create_pr", "mark_ready"], preview["target"]["actions"])
        self.assertEqual([], self.effects)
        with self.provider_reads():
            result = self.execute(preview)
        self.assertEqual("ready_for_merge", result["exit_id"])
        self.assertEqual(["push", "create", "ready"], self.effects)
        self.assertEqual(42, result["pr_number"])

    def test_existing_pr_changes_the_waiting_preview(self):
        self.ready_to_prepare()
        preview = self.prepare()
        self.remote = self.f.head
        self.pr = {"number":42, "url":"https://github.com/example/repo/pull/42", "state":"OPEN",
                   "isDraft":True, "title":"此前标题", "body":"此前正文",
                   "headRefName":"feat/flow", "headRefOid":self.remote, "baseRefName":"main",
                   "headRepositoryOwner":{"login":"example"}}
        self.assertEqual("reprepare_required", self.execute(preview)["exit_id"])
        self.assertEqual([], self.effects)
        updated = self.prepare()
        self.assertEqual(["converge_metadata", "mark_ready"], updated["target"]["actions"])
        with self.provider_reads():
            result = self.execute(updated)
        self.assertEqual(42, result["pr_number"])
        self.assertEqual(["edit", "ready"], self.effects)

    def test_recovers_lost_preview_and_a_lost_create_response(self):
        self.ready_to_prepare()
        self.prepare()
        self.assertEqual("publishing", self.f.projection.resolve(self.f.key)["phase"])
        restarted = self.prepare()
        self.assertEqual("publication_prepared", restarted["exit_id"])
        self.assertEqual([], self.effects)
        self.drop = "create"
        paused = self.execute(restarted)
        self.assertEqual("resume_publication", paused["exit_id"])
        self.semantic["pr_payload"]["body"] = "本次验证结果覆盖当前切片。环境观察仍待补充。"
        resumed = self.prepare()
        self.assertEqual(["converge_metadata", "mark_ready"], resumed["target"]["actions"])
        self.assertEqual(42, resumed["target"]["pr_number"])
        with self.provider_reads():
            result = self.execute(resumed)
        self.assertEqual("ready_for_merge", result["exit_id"])
        self.assertEqual(["push", "create", "edit", "ready"], self.effects)

    def test_merges_route_before_refreshing_readiness(self):
        self.ready_to_prepare()
        preview = self.prepare()
        with self.provider_reads():
            self.execute(preview)
        self.pr["state"] = "MERGED"
        result = self.prepare()
        self.assertEqual("merged_recovery_required", result["exit_id"])
        self.assertEqual(42, result["pr_number"])
        self.assertEqual(["push", "create", "ready"], self.effects)

    def test_recovers_terminal_transaction_when_public_projection_was_interrupted(self):
        self.ready_to_prepare()
        preview = self.prepare()
        with patch.object(fixture.owner, "ready_output",
                          side_effect=fixture.owner.WorkflowError("Projection response lost.", code="external_command_failed")):
            self.assertEqual("resume_publication", self.execute(preview)["exit_id"])
        selected = self.f.projection.resolve(self.f.key)
        self.assertIsNone(selected["publication_result"])
        with self.provider_reads():
            output = self.prepare()
        self.assertEqual("ready_for_merge", output["exit_id"])
        self.assertEqual(["push", "create", "ready"], self.effects)
        self.assertEqual(42, self.f.projection.resolve(self.f.key)["publication_result"]["pr_number"])

    def resume(self, interrupted):
        return self.run_profile({
            "profile": "delivery_same_plan_resume", "mode": self.mode,
            "task_ref": self.f.task_ref, "delivery_key": self.f.key,
            "transaction_ref": interrupted["transaction_ref"],
        })

    def test_same_plan_recovers_ready_response_without_replaying_it(self):
        self.ready_to_prepare()
        preview = self.prepare()
        self.drop = "ready"
        interrupted = self.execute(preview)
        self.assertEqual("resume_publication", interrupted["exit_id"])
        self.assertIsNone(self.f.projection.resolve(self.f.key)["publication_result"])
        with self.provider_reads():
            output = self.resume(interrupted)
        self.assertEqual("ready_for_merge", output["exit_id"])
        self.assertEqual(42, output["pr_number"])
        self.assertEqual(["push", "create", "ready"], self.effects)

    def test_same_plan_recovers_draft_response_and_public_rework(self):
        self.ready_to_prepare()
        with self.provider_reads():
            self.execute(self.prepare())
        returning = {
            "profile": "delivery_return_to_draft", "mode": self.mode,
            "task_ref": self.f.task_ref, "delivery_key": self.f.key,
            "revision_reason": "Correct a normal implementation finding before publishing.",
        }
        draft_review = {**self.release, "route": {"typed_exit": "draft_revision_ready"}}
        context = fixture.owner.plan_from_input(self.f.repo, returning)
        self.drop = "draft"
        interrupted = self.run_profile(returning, draft_review, context["confirmation_identity"])
        self.assertEqual("resume_publication", interrupted["exit_id"])
        self.assertTrue(self.pr["isDraft"])
        self.assertEqual("publishing", self.f.projection.resolve(self.f.key)["phase"])
        output = self.resume(interrupted)
        self.assertEqual("draft_revision_ready", output["exit_id"])
        self.assertEqual(42, output["pr_number"])
        self.assertEqual("implementing", self.f.projection.resolve(self.f.key)["phase"])
        self.assertEqual(output, self.resume(interrupted))
        self.assertEqual(["push", "create", "ready", "draft"], self.effects)

    def test_routes_already_merged_transaction_without_publication_fact(self):
        self.ready_to_prepare()
        preview = self.prepare()
        with patch.object(fixture.owner, "ready_output",
                          side_effect=fixture.owner.WorkflowError("Projection response lost.", code="external_command_failed")):
            self.assertEqual("resume_publication", self.execute(preview)["exit_id"])
        self.pr["state"] = "MERGED"
        output = self.prepare()
        self.assertEqual("merged_adoption_required", output["exit_id"])
        self.assertEqual(42, output["pr_number"])
        self.assertIsNone(self.f.projection.resolve(self.f.key)["publication_result"])
        self.assertEqual(["push", "create", "ready"], self.effects)

    def test_completed_open_pr_metadata_refresh_retains_same_pr(self):
        self.ready_to_prepare()
        with self.provider_reads():
            original = self.execute(self.prepare())
        self.pr["body"] = "维护者更新了正文。"
        preview = self.prepare()
        self.assertEqual(["converge_metadata"], preview["target"]["actions"])
        with self.provider_reads():
            refreshed = self.execute(preview)
        self.assertEqual("ready_for_merge", refreshed["exit_id"])
        self.assertEqual(original["pr_number"], refreshed["pr_number"])
        self.assertNotEqual(original["publication_result_id"], refreshed["publication_result_id"])
        self.assertEqual(["push", "create", "ready", "edit"], self.effects)

    def test_merge_rework_refreshes_readiness_for_same_pr(self):
        from runtime.delivery_projection.adapter import authority_ref
        from runtime.delivery_projection.gates import rework
        self.ready_to_prepare()
        with self.provider_reads():
            initial = self.execute(self.prepare())
        rework(self.f.projection, self.f.key, "delivery", "readiness",
               authority_ref(self.f.repo / "requirements.md", self.f.repo), ["readiness"])
        self.semantic["pr_payload"]["body"] = "复核后更新正文。"
        updated = self.prepare()
        self.assertEqual("publication_prepared", updated["exit_id"])
        self.assertEqual(["converge_metadata"], updated["target"]["actions"])
        with self.provider_reads():
            refreshed = self.execute(updated)
        self.assertEqual("ready_for_merge", refreshed["exit_id"])
        self.assertEqual(initial["pr_number"], refreshed["pr_number"])
        self.assertEqual(["push", "create", "ready", "edit"], self.effects)
