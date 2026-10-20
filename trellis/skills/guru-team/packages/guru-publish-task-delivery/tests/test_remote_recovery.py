"""Real shared Git/independent common-dir recovery with controlled PR effects.

Provider ports prove Publication integration, not live GitHub or AI readiness.
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("remote_draft_fixture", PACKAGE / "tests/test_early_draft.py")
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
owner = fixture.owner


class RemoteRecovery(unittest.TestCase):
    setUp = fixture.EarlyDraftPublication.setUp
    github = fixture.EarlyDraftPublication.github
    def mutate(self, root, argv, **kwargs):
        if argv[:2] == ["git", "push"]:
            self.assertEqual(f"{self.f.head}:refs/heads/feat/flow", argv[-1])
        return fixture.EarlyDraftPublication.mutate(self, root, argv, **kwargs)

    public = fixture.EarlyDraftPublication.public
    invoke = fixture.EarlyDraftPublication.invoke
    final_input = fixture.EarlyDraftPublication.final_input
    provider_reads = fixture.EarlyDraftPublication.provider_reads

    def existing_pr(self, public, *, draft=True):
        self.remote = self.f.head
        self.pr = {"number": 42, "url": "https://github.com/example/repo/pull/42", "state": "OPEN",
                   "isDraft": draft, "title": public["pr_title"], "body": public["pr_body"],
                   "headRefName": "feat/flow", "headRefOid": self.remote, "baseRefName": "main",
                   "headRepositoryOwner": {"login": "example"}}

    def independent_clone(self):
        from runtime.delivery_projection.adapter import DeliveryProjection
        from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
        self.f.git("add", ".")
        self.f.git("commit", "-qm", "share public lifecycle source")
        self.source_commit = self.f.git("rev-parse", "HEAD").strip()
        self.assertNotEqual(0, subprocess.run(["git", "merge-base", "--is-ancestor", self.source_commit, "main"],
                                             cwd=self.f.repo, capture_output=True).returncode)
        prior = self.f.repo
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        clone = Path(directory.name) / "replacement"
        subprocess.run(["git", "clone", "-q", "--no-local", str(prior), str(clone)], check=True)
        clone = clone.resolve()
        self.f.repo = clone
        self.f.git("config", "user.name", "Replacement")
        self.f.git("config", "user.email", "replacement@example.invalid")
        self.f.git("switch", "-qc", "replacement/local")
        self.f.projection = DeliveryProjection(clone, self.f.task_ref)
        BranchBindingStore(inspect_repository(clone)).establish(TaskLifecycleKey("flow-task", 0), "replacement/local")
        self.f.inputs = clone / ".trellis/.runtime/test-inputs"
        self.f.inputs.mkdir(parents=True)
        self.assertNotEqual((clone / self.f.git("rev-parse", "--git-common-dir").strip()).resolve(), (prior / ".git").resolve())
        self.assertFalse((clone / ".trellis/.runtime/guru-team/guru-publish-task-delivery").exists())
        self.local_branch = self.f.git("branch", "--show-current")
        self.local_head = self.f.git("rev-parse", "HEAD")

    def remote_input(self, public, kind="draft"):
        return {**public, "profile": f"delivery_remote_{kind}_recovery", "source_commit": self.source_commit,
                "pr_ref": {"repo_ref": "example/repo", "pr_number": 42}}

    def assert_binding_preserved(self):
        self.assertEqual(self.local_branch, self.f.git("branch", "--show-current"))
        self.assertEqual(self.local_head, self.f.git("rev-parse", "HEAD"))
        from runtime.task_lifecycle import resolve_active_task_checkout
        self.assertEqual("replacement/local", resolve_active_task_checkout(self.f.repo, self.f.task_ref).branch_name)

    def test_shared_draft_complete_has_zero_remote_writes_and_no_final_fact(self):
        public = self.public()
        self.existing_pr(public)
        self.independent_clone()
        remote = self.remote_input(public)
        result = self.invoke(remote)
        self.assertEqual("draft_published", result["exit_id"])
        self.assertEqual(result, self.invoke(remote))
        self.assertEqual([], self.effects)
        self.assertIsNone(self.f.projection.resolve(self.f.key)["publication_result"])
        self.assert_binding_preserved()

    def test_existing_draft_only_finishes_metadata_with_no_push_create_or_ready(self):
        public = self.public()
        self.existing_pr(public)
        self.pr.update(title="此前标题", body="此前待审正文")
        self.independent_clone()
        remote = self.remote_input(public)
        self.drop = "edit"
        interrupted = self.invoke(remote)
        self.assertEqual("resume_publication", interrupted["exit_id"])
        result = self.invoke({"profile": "delivery_same_plan_resume", "mode": "workflow", "task_ref": self.f.task_ref,
                              "delivery_key": self.f.key, "transaction_ref": interrupted["transaction_ref"]})
        self.assertEqual("draft_published", result["exit_id"])
        self.assertEqual(["edit"], self.effects)
        self.assert_binding_preserved()

    def test_existing_ready_is_draft_before_remaining_candidate_push(self):
        public = self.public()
        self.existing_pr(public, draft=False)
        (self.f.repo / "app.txt").write_text("normal candidate correction\n")
        self.f.git("add", "app.txt")
        self.f.git("commit", "-qm", "candidate correction")
        self.f.head = self.f.git("rev-parse", "HEAD").strip()
        public = self.public()
        self.independent_clone()
        result = self.invoke(self.remote_input(public))
        self.assertEqual("draft_published", result["exit_id"])
        self.assertEqual(["draft", "push"], self.effects)
        self.assertTrue(self.pr["isDraft"])
        self.assert_binding_preserved()

    def test_ready_recovers_original_publication_without_private_transaction_or_mutations(self):
        self.invoke(self.public())
        final = self.final_input()
        with self.provider_reads():
            published = self.invoke(final)
        original_fact = self.f.projection.resolve(self.f.key)["publication_result"]
        self.independent_clone()
        self.effects.clear()
        with self.provider_reads():
            recovered = self.invoke(self.remote_input(final, "ready"))
        self.assertEqual(published, recovered)
        self.assertEqual(original_fact, self.f.projection.resolve(self.f.key)["publication_result"])
        self.assertEqual([], self.effects)
        self.assert_binding_preserved()

    def test_ready_projection_missing_only_records_fact_and_ready_pending_only_marks_ready(self):
        final = self.final_input()
        self.existing_pr(final)
        self.independent_clone()
        with self.provider_reads():
            result = self.invoke(self.remote_input(final, "ready"))
        self.assertEqual("ready_for_merge", result["exit_id"])
        self.assertEqual(["ready"], self.effects)
        self.assertFalse(self.pr["isDraft"])
        with self.provider_reads():
            self.assertEqual(result, self.invoke(self.remote_input(final, "ready")))
        self.assertEqual(["ready"], self.effects)
        self.assert_binding_preserved()

    def test_already_ready_missing_public_projection_does_not_repeat_remote_writes(self):
        final = self.final_input()
        self.existing_pr(final, draft=False)
        self.independent_clone()
        with self.provider_reads():
            result = self.invoke(self.remote_input(final, "ready"))
        self.assertEqual("ready_for_merge", result["exit_id"])
        self.assertEqual([], self.effects)
        self.assertEqual(self.f.head, self.f.projection.resolve(self.f.key)["publication_result"]["reviewed_head"])
        self.assert_binding_preserved()

    def test_missing_current_readiness_returns_original_review_without_remote_write(self):
        public = self.public()
        self.existing_pr(public, draft=False)
        self.independent_clone()
        remote = self.remote_input({k: v for k, v in public.items() if k not in {"base_ref", "candidate_head"}}, "ready")
        remote.update(readiness_result_id="unavailable", reviewed_head=self.f.head, remaining_work_state="none")
        self.assertEqual("review_stale", self.invoke(remote)["exit_id"])
        self.assertEqual([], self.effects)

    def test_wrong_target_and_unavailable_source_stop_without_duplicate_pr(self):
        public = self.public()
        self.existing_pr(public)
        self.independent_clone()
        remote = self.remote_input(public)
        self.pr["baseRefName"] = "other-target"
        self.assertEqual("blocked", self.invoke(remote)["exit_id"])
        self.pr["baseRefName"] = "main"
        remote["source_commit"] = "f" * 40
        from runtime.task_lifecycle import LifecycleContractError
        with self.assertRaises(LifecycleContractError) as missing:
            self.invoke(remote)
        self.assertEqual("candidate_commit_missing", missing.exception.code)
        self.assertEqual([], self.effects)

    def test_public_inputs_and_current_aggregate_accept_independent_closed_profiles(self):
        from runtime.schema import validate_json
        for kind in ("draft", "ready"):
            name = f"public-delivery-remote-{kind}-recovery-input-1.0"
            value = json.loads((PACKAGE / "examples" / (name + ".json")).read_text())
            validate_json(value, PACKAGE / "schemas" / (name + ".schema.json"), "input")
            validate_json(value, PACKAGE / "schemas/public-input-delivery-3.0.schema.json", "input")
            value["transaction_ref"] = "a" * 64
            from runtime.io import CommandError
            with self.assertRaises(CommandError) as invalid:
                owner.validate_public_input(value)
            self.assertEqual("schema_mismatch", invalid.exception.code)


if __name__ == "__main__":
    unittest.main()
