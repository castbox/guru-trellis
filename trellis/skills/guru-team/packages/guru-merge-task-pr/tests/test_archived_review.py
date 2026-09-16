from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

import test_errors


PACKAGE = Path(__file__).resolve().parents[1]


def archive_fixture():
    tests = PACKAGE.parent / "guru-finalize-task/tests"
    previous = sys.modules.pop("support", None)
    search = sys.path[:]
    try:
        sys.path.insert(0, str(tests))
        spec = importlib.util.spec_from_file_location("merge_archive_producer_fixture", tests / "test_archive_mappings.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = search
        sys.modules.pop("support", None)
        if previous is not None:
            sys.modules["support"] = previous
    fixture = module.ArchiveMappingTests()
    fixture.archive_owner = module.GTT
    return fixture


class ArchivedReviewTest(unittest.TestCase):
    def setUp(self):
        self.h = test_errors.MergeErrorWrapperTest()
        self.h.setUp()
        self.addCleanup(self.h.doCleanups)
        self.provider_root = self.h.root
        self.producer = archive_fixture()
        self.producer.setUp()
        self.addCleanup(self.producer.doCleanups)
        self.producer.archive()
        self.h.root = self.producer.root
        self.root = self.h.root
        self.head = self.git("rev-parse", "HEAD")
        self.base = self.git("rev-parse", "origin/main")
        # Keep the real local bare remote while exposing the canonical origin identity.
        self.git("remote", "set-url", "origin", "https://github.com/example/repo.git")
        self.git("config", f"url.{self.producer.producer.remote}.insteadOf", "https://github.com/example/repo.git")
        self.h.public = {
            "schema_version": "2.0", "profile": "archived_review_request", "mode": "workflow",
            "task_ref": self.producer.archived.relative_to(self.root).as_posix(),
            "repo_ref": "example/repo", "pr_number": 27, "expected_head_sha": self.head,
        }
        self.h.input.write_text(json.dumps(self.h.public))
        self.h.review.write_text(json.dumps({
            "semantic_review": {"dimensions": [
                {"id": name, "status": "passed", "summary": "Current archived entry reviewed, not merge approval."}
                for name in test_errors.OWNER.TASK_PR_MERGE_DIMENSIONS
            ]}, "route": {"typed_exit": "review_refresh_required"},
        }))
        self.pr = {**self.h.pr, "number": 27, "url": "https://github.com/example/repo/pull/27",
                   "headRefOid": self.head, "headRefName": "feat/027-workspace",
                   "title": "  \u5f52\u6863\u590d\u5ba1\r\n", "body": "Exact PR payload\r\n\n"}
        self.provider("pr.json", self.pr)
        self.provider("base.json", {"ref": "refs/heads/main", "object": {"sha": self.base}})
        self.provider("checks.json", [])
        gh = self.h.bin / "gh"
        gh.write_text(gh.read_text().replace('  "pr view")', '  "pr checks") cat "$MERGE_FIXTURE/checks.json" ;;\n  "pr view")'))

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, text=True, capture_output=True, check=True).stdout.strip()

    def provider(self, name, value):
        (self.provider_root / name).write_text(json.dumps(value), encoding="utf-8")

    def snapshot(self):
        return {
            "head": self.git("rev-parse", "HEAD"), "status": self.git("status", "--porcelain"),
            "remote": self.git("ls-remote", "origin"),
            "archive": {p.name: p.read_bytes() for p in self.producer.archived.iterdir()},
            "mappings": {str(p): p.read_bytes() for p in self.producer.mapping_paths + self.producer.workspace_paths},
            "pr": (self.provider_root / "pr.json").read_bytes(),
        }

    def configured_archive(self, configured_remote, *, scalar_publish=False):
        producer = archive_fixture()
        producer.setUp()
        self.addCleanup(producer.doCleanups)
        self.producer = producer
        self.root = self.h.root = producer.root
        owner = producer.archive_owner
        config = self.root / ".trellis/guru-team/config.yml"
        config.parent.mkdir(parents=True, exist_ok=True)
        existing = config.read_text() if config.exists() else "workspace_mode: worktree\n"
        setting = ("\npublish: " if scalar_publish else "\npublish:\n  remote: ") + json.dumps(configured_remote) + "\n"
        config.write_text(existing + setting)
        summary = producer.task_dir / owner.FINISH_SUMMARY_ARTIFACT
        summary.unlink()
        self.git("add", ".trellis/guru-team/config.yml")
        self.git("commit", "-qm", "Configure publish remote before archive")
        remote = "origin" if scalar_publish else configured_remote or "origin"
        if remote != "origin":
            self.git("remote", "add", remote, "https://github.com/example/repo.git")
        else:
            self.git("remote", "set-url", "origin", "https://github.com/example/repo.git")
        self.git("config", f"url.{producer.producer.remote}.insteadOf", "https://github.com/example/repo.git")
        producer.head = self.git("rev-parse", "HEAD")
        previous = producer.plan
        producer.plan = owner.build_finalization_plan(
            self.root, producer.task_dir, producer.context, owner.task_json(producer.task_dir),
            repo="example/repo", remote=remote, base_branch="main", head_branch="feat/027-workspace",
            branch_review_commit=producer.head, title=previous["publish"]["title"], body=previous["publish"]["body"],
            review_facts={"changed_paths": [".trellis/guru-team/config.yml", producer.active + "/task.json"]},
        )
        owner.write_json(summary, owner.closeout_summary_for_pr(producer.plan, producer.pr))
        producer.archive()
        self.head = self.git("rev-parse", "HEAD")
        self.base = self.git("rev-parse", "origin/main")
        self.h.public.update(task_ref=producer.archived.relative_to(self.root).as_posix(), expected_head_sha=self.head)
        self.h.input.write_text(json.dumps(self.h.public))
        self.pr["headRefOid"] = self.head
        self.provider("pr.json", self.pr)
        self.provider("base.json", {"ref": "refs/heads/main", "object": {"sha": self.base}})
        self.assertEqual(config.read_text().strip(), self.git("show", "HEAD:.trellis/guru-team/config.yml"))
        return remote

    def test_configured_publish_remote_is_readonly_and_keeps_origin_base_ref(self):
        remote = self.configured_archive("publishing")
        # Origin remains the local bare locator, so it cannot pass the GitHub URL guard.
        self.assertEqual(self.git("config", "--get", "remote.origin.url"), str(self.producer.producer.remote))
        before = self.snapshot()
        remote_before = self.git("ls-remote", remote)
        proc, output = self.h.wrapper("invoke")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertEqual(output["exit_id"], "review_refresh_required")
        self.assertEqual(output["branch_review_commit"], self.head)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(remote_before, self.git("ls-remote", remote))
        self.assertNotIn("pr merge", self.h.log.read_text())

    def test_blank_publish_remote_falls_back_to_origin(self):
        self.assertEqual(self.configured_archive(""), "origin")
        before = self.snapshot()
        proc, output = self.h.wrapper("invoke")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertEqual(output["exit_id"], "review_refresh_required")
        self.assertEqual(before, self.snapshot())

    def test_non_dict_publish_remote_falls_back_to_origin(self):
        self.assertEqual(self.configured_archive("unused", scalar_publish=True), "origin")
        before = self.snapshot()
        proc, output = self.h.wrapper("invoke")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertEqual(output["exit_id"], "review_refresh_required")
        self.assertEqual(before, self.snapshot())

    def test_configured_publish_remote_does_not_adopt_another_repository(self):
        remote = self.configured_archive("publishing")
        self.git("remote", "set-url", remote, "https://github.com/example/other.git")
        before = self.snapshot()
        self.h.assert_error("preview", "stale_identity", "publish.remote")
        self.assertEqual(before, self.snapshot())
        self.assertFalse(self.h.log.exists())

    def test_public_invoke_captures_snapshot_without_publication_hash_or_mutation(self):
        before = self.snapshot()
        proc, result = self.h.wrapper("invoke")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        expected_hash = hashlib.sha256(json.dumps({"title": self.pr["title"], "body": self.pr["body"]},
                                                 ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        self.assertEqual(result, {"exit_id": "review_refresh_required", "task_ref": self.h.public["task_ref"],
                                  "branch_review_commit": self.head, "pr_payload_snapshot_sha256": expected_hash})
        self.assertEqual(before, self.snapshot())
        self.assertNotIn("pr merge", self.h.log.read_text())
        self.assertFalse(list(self.root.rglob("archived-review-gate.json")))
        self.assertFalse(list(self.root.rglob("review-gate.json")))

    def test_preview_record_check_execute_original_wrappers_are_readonly(self):
        before = self.snapshot()
        proc, preview = self.h.wrapper("preview")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertEqual(preview["objective_blockers"], [])
        gate = self.h.record_current_gate()
        proc, checked = self.h.wrapper("check")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertEqual(checked["typed_exit"], "review_refresh_required")
        proc, executed = self.h.wrapper("execute")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertEqual(executed["output"], checked["output"])
        self.assertFalse(gate.exists())
        self.assertEqual(before, self.snapshot())
        self.assertNotIn("pr merge", self.h.log.read_text())

    def test_archived_profile_never_accepts_merge_route_or_prior_publication_hash(self):
        review = json.loads(self.h.review.read_text())
        review["route"] = {"typed_exit": "merged", "merge_method": "merge"}
        self.h.review.write_text(json.dumps(review))
        for op in ("record", "invoke"):
            self.h.assert_error(op, "invalid_arguments", "review_input.route")
        self.h.input.write_text(json.dumps({**self.h.public, "publication_body_sha256": "1" * 64}))
        self.h.assert_error("preview", "invalid_arguments", "input")
        self.assertFalse(list(self.root.rglob("archived-review-gate.json")))
        self.assertNotIn("pr merge", self.h.log.read_text())

    def test_produced_gate_rejects_normal_pr_payload_change(self):
        self.h.record_current_gate()
        self.provider("pr.json", {**self.pr, "title": "Updated title"})
        for op in ("check", "execute", "invoke"):
            self.h.assert_error(op, "stale_identity", "gate.archived_review")
        self.assertNotIn("pr merge", self.h.log.read_text())

    def test_current_semantic_change_does_not_reuse_prior_gate(self):
        self.h.record_current_gate()
        review = json.loads(self.h.review.read_text())
        review["semantic_review"]["dimensions"][0]["status"] = "blocked"
        review["route"] = {"typed_exit": "merge_blocked", "reason_code": "review_evidence_missing",
                           "remediation": "Supply the missing current review evidence."}
        self.h.review.write_text(json.dumps(review))
        self.h.assert_error("invoke", "stale_identity", "review_input")
        self.h.record_current_gate()
        proc, output = self.h.wrapper("invoke")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertEqual(output["exit_id"], "merge_blocked")

    def test_normal_archive_without_mapping_consumer_stops_without_repair(self):
        producer = archive_fixture()
        producer.setUp()
        self.addCleanup(producer.doCleanups)
        producer.archive_without_mapping_consumer()
        self.producer = producer
        self.root = self.h.root = producer.root
        self.git("remote", "set-url", "origin", "https://github.com/example/repo.git")
        self.git("config", f"url.{producer.producer.remote}.insteadOf", "https://github.com/example/repo.git")
        self.h.public["task_ref"] = producer.archived.relative_to(self.root).as_posix()
        self.h.public["expected_head_sha"] = self.git("rev-parse", "HEAD")
        self.h.input.write_text(json.dumps(self.h.public))
        before = {str(path): path.read_bytes() for path in producer.mapping_paths}
        self.h.assert_error("preview", "stale_identity", "task_mapping")
        self.assertEqual(before, {str(path): path.read_bytes() for path in producer.mapping_paths})
        self.assertFalse(self.h.log.exists())

    def test_required_ci_failure_is_not_refresh_success(self):
        self.provider("checks.json", [{"name": "required", "state": "FAILURE", "bucket": "fail"}])
        self.h.assert_error("invoke", "stale_identity", "review_input.route")
        review = json.loads(self.h.review.read_text())
        review["semantic_review"]["dimensions"][2]["status"] = "blocked"
        review["route"] = {"typed_exit": "merge_blocked", "reason_code": "required_checks_failed",
                           "remediation": "Resolve the required CI failure before requesting review."}
        self.h.review.write_text(json.dumps(review))
        proc, output = self.h.wrapper("invoke")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertEqual(output["exit_id"], "merge_blocked")
        self.assertFalse(list(self.root.rglob("archived-review-gate.json")))

    def test_unavailable_mapping_does_not_rebuild_or_touch_archive(self):
        self.producer.mapping_paths[0].unlink()
        before = {p.name: p.read_bytes() for p in self.producer.archived.iterdir()}
        self.h.assert_error("preview", "invalid_arguments", "task_mapping")
        self.assertFalse(self.producer.mapping_paths[0].exists())
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.producer.archived.iterdir()})

    def test_wrong_branch_and_dirty_archive_stop_readonly(self):
        self.git("checkout", "-qb", "other-task")
        self.h.assert_error("preview", "stale_identity", "task.branch")
        self.git("checkout", "feat/027-workspace")
        (self.producer.archived / "prd.md").write_text("Ordinary incomplete edit.\n")
        self.h.assert_error("preview", "stale_identity", "worktree.clean")
        self.assertFalse(self.h.log.exists())

    def test_provider_head_base_or_ready_state_changes_stop(self):
        for changed, code, field in (
            ({"headRefOid": "4" * 40}, "stale_identity", "github.pr.head"),
            ({"baseRefName": "dev"}, "stale_identity", "github.pr.branches"),
            ({"isDraft": True}, "merge_precondition_failed", "github.pr.state"),
            ({"state": "CLOSED"}, "merge_precondition_failed", "github.pr.state"),
        ):
            self.provider("pr.json", {**self.pr, **changed})
            self.h.assert_error("preview", code, field)
        self.assertNotIn("pr merge", self.h.log.read_text())


if __name__ == "__main__":
    unittest.main()
