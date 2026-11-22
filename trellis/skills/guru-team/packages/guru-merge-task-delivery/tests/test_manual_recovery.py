"""Public wrappers and real local Git; GitHub/semantic judgments are fixtures.

This is component integration, not installed AI-owner or live provider proof.
"""
import importlib.util
import hashlib
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]


class _MergedPullRequestFixture(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("manual_recovery_flow", SKILLS / "packages/guru-check-task/tests/test_delivery_flow.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.flow = module.DeliveryFlow()
        self.flow.delivery_profile = "pull_request"
        self.flow.setUp()
        self.addCleanup(self.flow.doCleanups)
        self.repo = self.flow.repo
        self.projection = self.flow.projection
        self.base = self.flow.git("rev-parse", "main").strip()
        self.actual = self.flow.head

    def start_provider(self):
        self.checks = [{"name": "required", "status": "COMPLETED", "conclusion": "SUCCESS"}]
        self.bin = self.repo / ".trellis/.runtime/manual-provider"
        self.bin.mkdir()
        self.calls = self.bin / "calls.jsonl"
        gh = self.bin / "gh"
        gh.write_text("#!" + sys.executable + "\nimport json,sys\nfrom pathlib import Path\n"
            "args=sys.argv[1:]\nwith Path(" + repr(str(self.calls)) + ").open('a') as f: f.write(json.dumps(args)+'\\n')\n"
            "if args[:2]==['auth','status']: sys.exit(0)\n"
            "values=json.loads(Path(" + repr(str(self.bin / "responses.json")) + ").read_text())\n"
            "if args[:1]==['api']: key=next(x for x in args if x.startswith('repos/'))\nelif args[:2]==['pr','view']: key='checks'\nelse: sys.exit(31)\n"
            "print(json.dumps(values[key]))\n")
        gh.chmod(0o755)
        self.env = patch.dict(os.environ, {"PATH": str(self.bin) + os.pathsep + os.environ["PATH"]})
        self.env.start()
        self.addCleanup(self.env.stop)

    def responses(self, *, state="CLOSED", base="main", number=9):
        pr = {"number": number, "state": state, "merged_at": "2026-10-15T01:00:00Z" if state == "CLOSED" else None,
            "merge_commit_sha": self.merge, "base": {"ref": base, "repo": {"full_name": "example/repo"}},
            "head": {"sha": self.actual, "repo": {"full_name": "example/repo"}}}
        values = {"repos/example/repo": {"full_name": "example/repo"}, f"repos/example/repo/pulls/{number}": pr,
            "repos/example/repo/commits/" + self.merge + "/pulls": [pr],
            "checks": {"number": number, "state": "MERGED" if state == "CLOSED" else state,
                "url": f"https://github.com/example/repo/pull/{number}", "body": "Refs #9", "headRefOid": self.actual, "baseRefName": base,
                "mergeCommit": {"oid": self.merge}, "statusCheckRollup": self.checks, "reviewDecision": ""},
            "repos/example/repo/git/ref/heads/main": {"object": {"sha": self.flow.git("rev-parse", "main").strip()}},
            "repos/example/repo/git/commits/" + self.merge: {"sha": self.merge, "message": f"Merge pull request #{number}",
                "parents": [{"sha": self.base}, {"sha": self.actual}]}}
        (self.bin / "responses.json").write_text(json.dumps(values))

    def invoke(self, *, success=True, review=None):
        return self.flow.wrapper(PACKAGE.name, "invoke.sh", "--input", self.flow.write("manual.json", self.public),
            "--review-input", self.flow.write("manual-review.json", review or self.review()), success=success)


class ManualRecoveryTests(_MergedPullRequestFixture):
    def setUp(self):
        super().setUp()
        self.flow.readiness(self.flow.single_review())
        delivery = self.projection.resolve(self.flow.key)
        self.publication = {"result_id": "publication:manual", "owner_id": self.projection.declaration()["owners"]["publication"],
            "evidence": [delivery["scope_ref"]["authority"]], "profile": "pull_request",
            "candidate": delivery["candidate"], "repo_ref": "example/repo", "pr_number": 9,
            "reviewed_head": self.flow.head, "target_ref": "main",
            "publication_ref": {"locator": "https://github.com/example/repo/pull/9", "revision": "sha256:" + hashlib.sha256(b"Refs #9").hexdigest()}}
        self.make_merge()
        self.start_provider()
        self.public = {"profile": "delivery_merged_recovery", "mode": "workflow", "task_ref": self.flow.task_ref,
            "delivery_key": self.flow.key, "repo_ref": "example/repo", "pr_number": 9}
        self.responses()
        self.projection.apply({"api_version": "1.0", "operation": "record_publication", "key": self.flow.key,
            "owner_role": "publication", "owner_id": self.publication["owner_id"], "expected_phase": "publishing",
            "historical_success": True, "result": self.publication})

    def make_merge(self):
        tree = self.flow.git("merge-tree", "--write-tree", "main", "feat/flow").splitlines()[0]
        self.merge = self.flow.git("commit-tree", tree, "-p", self.base, "-p", self.actual,
            "-m", "Merge pull request #9").strip()
        self.flow.git("update-ref", "refs/heads/main", self.merge)

    def review(self):
        return {"reviewed_delivery_key": self.flow.key, "publication_result_id": "publication:manual",
            "reviewed_pr": {"repo_ref": "example/repo", "pr_number": 9, "head_sha": self.actual,
                "merge_sha": self.merge, "target_ref": "main"}, "observed_checks": self.checks,
            "content_impact": {"kind": "same_candidate" if self.actual == self.flow.head else "changed_candidate",
                "summary": "Reviewed the full published-to-actual and PR delta, including extra paths.",
                "affected_owner_refs": [] if self.actual == self.flow.head else ["guru-review-task-completion", "guru-check-task"]},
            "ai_review_gate": {"status": "passed", "summary": "Fixture attribution/actual content/CI truth reviewed; not whole-task completion."}}

    def trace_invoke(self):
        trace = self.flow.inputs / "manual-git-trace.jsonl"
        trace_bin = self.flow.inputs / "manual-trace-bin"
        trace_bin.mkdir(exist_ok=True)
        git = trace_bin / "git"
        git.write_text("#!" + sys.executable + "\nimport os,sys\n"
            "os.environ['GIT_TRACE2_EVENT'] = " + repr(str(trace)) + "\n"
            "os.execv(" + repr(shutil.which("git")) + ", ['git', *sys.argv[1:]])\n")
        git.chmod(0o755)
        with patch.dict(os.environ, {"PATH": str(trace_bin) + os.pathsep + os.environ["PATH"]}):
            result = self.invoke()
        commands = [row["argv"][1:] for row in map(json.loads, trace.read_text().splitlines())
                    if row.get("event") == "start"]
        return result, commands

    def test_repeated_terminal_endpoints_each_prepare_once_in_real_wrapper(self):
        result, commands = self.trace_invoke()
        self.assertEqual("delivered", result["exit_id"])
        checks = [command[2] for command in commands if command[:2] == ["cat-file", "-e"]]
        self.assertCountEqual([self.merge + "^{commit}", self.actual + "^{commit}"], checks)

    def test_original_file_and_stdin_carriers_recover_the_same_terminal_fact(self):
        import subprocess
        public_file = self.flow.write("carrier-manual.json", self.public)
        review = self.review()
        review_file = self.flow.write("carrier-manual-review.json", review)
        first = self.flow.wrapper(PACKAGE.name, "invoke.sh", "--input", public_file,
                                  "--review-input", review_file)
        self.assertEqual(first["exit_id"], "delivered")
        for arguments, content in [(["--input", "-", "--review-input", review_file], self.public),
                                   (["--input", public_file, "--review-input", "-"], review)]:
            result = subprocess.run(["bash", str(PACKAGE / "scripts/invoke.sh"), "--root", str(self.repo),
                                     *arguments], input=json.dumps(content), text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout), first)
        self.assertFalse(any(json.loads(line)[:2] == ["pr", "merge"]
                             for line in self.calls.read_text().splitlines()))

    def test_incomplete_provider_commit_keeps_original_error_classification(self):
        path = self.bin / "responses.json"
        values = json.loads(path.read_text())
        values["repos/example/repo/git/ref/heads/main"]["object"]["sha"] = []
        path.write_text(json.dumps(values))
        result = self.invoke(success=False)
        self.assertEqual("github_response_incomplete", result["code"])
        self.assertEqual("github.commit", result["field_path"])
        self.assertIsNone(self.projection.resolve(self.flow.key)["delivery_result"])

    def test_all_ci_states_record_real_merge_without_synthesizing_gates(self):
        original = self.projection.resolve(self.flow.key)["results"]
        for checks in ([{"conclusion": "SUCCESS"}], [{"status": "IN_PROGRESS"}], [{"conclusion": "CANCELLED"}], [], [{"conclusion": "FAILURE"}]):
            with self.subTest(checks=checks):
                self.checks = checks
                self.responses()
                out = self.invoke()
                self.assertEqual("delivered", out["exit_id"])
                recorded = self.projection.resolve(self.flow.key)
                self.assertEqual(self.merge, recorded["delivery_result"]["merge_commit"])
                self.assertEqual(original, recorded["results"])
                self.assertEqual(self.publication, recorded["publication_result"])
        self.assertFalse(any(json.loads(line)[:2] == ["pr", "merge"] for line in self.calls.read_text().splitlines()))

    def test_base_advance_branch_deletion_and_output_loss_recover_read_only(self):
        self.responses()
        out = self.invoke()
        tree = self.flow.git("rev-parse", "main^{tree}").strip()
        advanced = self.flow.git("commit-tree", tree, "-p", self.merge, "-m", "base bookkeeping").strip()
        self.flow.git("update-ref", "refs/heads/main", advanced)
        self.flow.git("switch", "--detach")
        self.flow.git("branch", "-D", "feat/flow")
        self.responses()
        before = (self.repo / self.flow.task_ref / "task.json").read_bytes()
        self.assertEqual(out, self.invoke())
        self.assertEqual(before, (self.repo / self.flow.task_ref / "task.json").read_bytes())

    def test_unmerged_and_base_mismatch_do_not_record(self):
        for state, base in (("OPEN", "main"), ("CLOSED", "dev")):
            with self.subTest(state=state, base=base):
                self.responses(state=state, base=base)
                out = self.invoke()
                self.assertEqual("merge_blocked", out["exit_id"])
                self.assertIsNone(self.projection.resolve(self.flow.key)["delivery_result"])

    def test_stale_ci_observation_stops_before_recording(self):
        self.responses()
        reviewed = self.review()
        reviewed["observed_checks"] = []
        result = self.invoke(success=False, review=reviewed)
        self.assertEqual("stale_identity", result["code"])
        self.assertIsNone(self.projection.resolve(self.flow.key)["delivery_result"])

    def test_actual_head_extra_path_is_recorded_without_rewriting_old_pass(self):
        original = self.projection.resolve(self.flow.key)["results"]
        (self.repo / "extra.txt").write_text("actual extra behavior\n")
        self.flow.git("add", "extra.txt")
        self.flow.git("commit", "-qm", "actual candidate addition")
        self.actual = self.flow.git("rev-parse", "HEAD").strip()
        tree = self.flow.git("merge-tree", "--write-tree", self.base, self.actual).splitlines()[0]
        self.merge = self.flow.git("commit-tree", tree, "-p", self.base, "-p", self.actual, "-m", "Merge pull request #9").strip()
        self.flow.git("update-ref", "refs/heads/main", self.merge)
        tree = self.flow.git("rev-parse", "main^{tree}").strip()
        advanced = self.flow.git("commit-tree", tree, "-p", self.merge, "-m", "base advance").strip()
        self.flow.git("update-ref", "refs/heads/main", advanced)
        self.responses()
        result, commands = self.trace_invoke()
        self.assertEqual("delivered", result["exit_id"])
        checks = [command[2] for command in commands if command[:2] == ["cat-file", "-e"]]
        self.assertCountEqual([sha + "^{commit}" for sha in
                               (self.merge, self.actual, advanced, self.flow.head)], checks)
        delivery = self.projection.resolve(self.flow.key)
        self.assertEqual(self.actual, delivery["delivery_result"]["candidate"]["head_ref"])
        self.assertEqual(self.flow.head, delivery["publication_result"]["candidate"]["head_ref"])
        self.assertEqual(original, delivery["results"])
        self.assertEqual(self.publication["candidate"]["content_ref"], delivery["delivery_result"]["candidate"]["content_ref"])

    def test_recorded_manual_fact_is_read_by_query2_but_not_query1(self):
        self.responses()
        self.invoke()
        before = (self.repo / self.flow.task_ref / "task.json").read_bytes()
        query = {"schema_version": "2.0", "task_identity": "flow-task", "repo_ref": "example/repo",
                 "base_ref": "main", "task_ref": self.flow.task_ref}
        trace = self.flow.inputs / "history-git-trace.jsonl"
        trace_bin = self.flow.inputs / "history-trace-bin"
        trace_bin.mkdir()
        git = trace_bin / "git"
        # The public API clears GIT_* variables. Set tracing at the real Git
        # process boundary, so the assertion covers the actual whole wrapper.
        git.write_text("#!" + sys.executable + "\nimport os,sys\n"
            "os.environ['GIT_TRACE2_EVENT'] = " + repr(str(trace)) + "\n"
            "os.execv(" + repr(shutil.which("git")) + ", ['git', *sys.argv[1:]])\n")
        git.chmod(0o755)
        with patch.dict(os.environ, {"PATH": str(trace_bin) + os.pathsep + os.environ["PATH"]}):
            out = self.flow.wrapper(PACKAGE.name, "discover-task-deliveries.sh", "--input", self.flow.write("history.json", query))
        rows = [json.loads(line) for line in trace.read_text().splitlines()]
        self.assertFalse(any(row.get("event") == "start" and row.get("argv", [])[1:] ==
                             ["cat-file", "-e", self.actual + "^{commit}"] for row in rows))
        with trace.open() as events:
            message_reads = sum(
                row.get("event") == "start"
                and row.get("argv", [])[1:] == ["show", "-s", "--format=%B", self.merge]
                for row in map(json.loads, events)
            )
        self.assertEqual(1, message_reads, "Read each matching merge message once in the actual query wrapper.")
        self.assertEqual([self.merge], [row["merge_commit_sha"] for row in out["deliveries"]])
        self.assertEqual(self.flow.key, out["deliveries"][0]["delivery_key"])
        query.pop("task_ref")
        query["schema_version"] = "1.0"
        old = self.flow.wrapper(PACKAGE.name, "discover-task-deliveries.sh", "--input", self.flow.write("old-history.json", query))
        self.assertEqual([], old["deliveries"])
        self.assertEqual(before, (self.repo / self.flow.task_ref / "task.json").read_bytes())

    def test_wrong_pr_selection_and_ambiguous_publication_stay_at_merge(self):
        self.public["pr_number"] = 10
        out = self.invoke()
        self.assertEqual("manual_merge_missing_publication", out["reason_code"])
        self.public["pr_number"] = 9
        key = {**self.flow.key, "delivery_id": "fc0c632d-c769-47e7-a754-6273d773e9bf"}
        self.projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": key,
            "owner_role": "creation", "owner_id": "guru-test-creation", "profile": "pull_request",
            "scope_ref": {"authority": self.projection.read_record()["accepted_scope"], "anchors": ["R1"]}})
        self.projection.apply({"api_version": "1.0", "operation": "record_publication", "key": key,
            "owner_role": "publication", "owner_id": "guru-test-publication", "expected_phase": "planning",
            "historical_success": True, "result": {**self.publication, "result_id": "publication:duplicate-relation"}})
        out = self.invoke()
        self.assertEqual("manual_merge_ambiguous_publication", out["reason_code"])
        self.assertIsNone(self.projection.resolve(self.flow.key)["delivery_result"])

    def test_public_projection_failure_after_record_recovers_same_fact(self):
        self.responses()
        self.flow.load_owner(PACKAGE.name)
        spec = importlib.util.spec_from_file_location("manual_projection_recovery", PACKAGE / "runtime/manual_recovery.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        from runtime.delivery_projection.adapter import DeliveryProjection
        from runtime.task_lifecycle import LifecycleContractError
        from runtime.io import CommandError
        apply = DeliveryProjection.apply
        def output_lost(projection, operation):
            apply(projection, operation)
            raise LifecycleContractError("delivery_projection_failed", "delivery", "Public result projection was lost after success.")
        with patch.object(DeliveryProjection, "apply", output_lost):
            with self.assertRaises(CommandError):
                module.invoke(self.repo, PACKAGE, self.public, self.review())
        before = (self.repo / self.flow.task_ref / "task.json").read_bytes()
        self.assertEqual("delivered", self.invoke()["exit_id"])
        self.assertEqual(before, (self.repo / self.flow.task_ref / "task.json").read_bytes())

    def test_completion_fixtures_preserve_incomplete_routes_after_real_fact(self):
        cases = [([{"status": "IN_PROGRESS"}], "evidence_pending"),
                 ([{"conclusion": "CANCELLED"}], "evidence_pending"),
                 ([], "evidence_pending"), ([{"conclusion": "FAILURE"}], "remaining_work"),
                 ([{"conclusion": "SUCCESS"}], "completed")]
        for checks, expected in cases:
            with self.subTest(checks=checks):
                self.checks = checks
                self.responses()
                self.invoke()
                record = self.projection.read_record()
                task_key = {k: self.flow.key[k] for k in ("task_id", "lifecycle_generation")}
                public = {"profile": "delivery_completion", "mode": "workflow", "task_ref": self.flow.task_ref, "task_key": task_key}
                reason = {"reason_code": "required_ci_unverified", "reason_refs": ["https://github.com/example/repo/pull/9"]}
                route = {"typed_exit": expected}
                if expected != "completed":
                    route["reason"] = reason
                semantic = {"profile": public["profile"], "mode": public["mode"], "reviewed_task_key": task_key,
                    "reviewed_scope": record["accepted_scope"], "reviewed_delivery_result_ids": ["delivery:" + self.merge],
                    "evidence": [record["accepted_scope"]], "remaining_work_refs": [] if expected == "completed" else ["requirements.md#R1"],
                    "result_id": "completion:ci-fixture", "route": route}
                out = self.flow.wrapper("guru-review-task-completion", "invoke.sh", "--input", self.flow.write("completion.json", public),
                    "--semantic-result", self.flow.write("completion-review.json", semantic))
                self.assertEqual(expected, out["exit_id"])
                if expected != "completed":
                    self.assertEqual([], self.projection.read_record()["completion_results"])


class AdoptMergedPullRequestTests(_MergedPullRequestFixture):
    def setUp(self):
        super().setUp()
        self.common_base = self.base
        self.task_json = self.repo / self.flow.task_ref / "task.json"
        self.flow.git("add", f"{self.flow.task_ref}/task.json")
        self.flow.git("commit", "-qm", "Record the current Delivery before merge")
        self.actual = self.flow.git("rev-parse", "HEAD").strip()
        self.flow.git("remote", "add", "origin", "https://github.com/example/repo.git")
        self.flow.git("switch", "main")
        (self.repo / "app.txt").write_text("main update\n")
        self.flow.git("add", "app.txt")
        self.flow.git("commit", "-qm", "Update the same file on main")
        self.base = self.flow.git("rev-parse", "HEAD").strip()
        conflict = subprocess.run(
            ["git", "merge", "--no-ff", "--no-commit", "feat/flow"],
            cwd=self.repo, capture_output=True, text=True,
        )
        self.assertEqual(1, conflict.returncode, conflict.stderr)
        self.assertEqual(self.actual, self.flow.git("rev-parse", "MERGE_HEAD").strip())
        (self.repo / "app.txt").write_text("main update and feature\n")
        self.flow.git("add", "app.txt")
        self.flow.git("commit", "-qm", "Merge pull request #9")
        self.merge = self.flow.git("rev-parse", "HEAD").strip()
        self.flow.git("switch", "feat/flow")
        self.start_provider()
        self.public = {"profile": "delivery_adopt_merged_pr", "mode": "workflow", "task_ref": self.flow.task_ref,
            "delivery_key": self.flow.key, "repo_ref": "example/repo", "pr_number": 9}
        self.checks = [{"name": "required", "status": "COMPLETED", "conclusion": "FAILURE"}]
        self.responses()

    def review(self):
        return {"reviewed_delivery_key": self.flow.key,
            "reviewed_scope_ref": self.projection.resolve(self.flow.key)["scope_ref"],
            "reviewed_pr": {"repo_ref": "example/repo", "pr_number": self.public["pr_number"],
                "head_sha": self.actual, "merge_sha": self.merge, "target_ref": "main"},
            "observed_checks": self.checks,
            "ai_review_gate": {"status": "passed", "summary": "Fixture review for attribution, PR content, and landed content."}}

    def test_adopts_actual_merge_without_publication_and_recovers_same_fact(self):
        before = self.projection.resolve(self.flow.key)
        self.assertIsNone(before["publication_result"])
        self.assertIsNone(before["delivery_result"])
        self.assertEqual("feature\n", self.flow.git("show", f"{self.actual}:app.txt"))
        self.assertEqual("main update and feature\n", self.flow.git("show", f"{self.merge}:app.txt"))
        self.assertEqual(f"{self.base} {self.actual}", self.flow.git("show", "-s", "--format=%P", self.merge).strip())

        result = self.invoke()
        self.assertEqual({"exit_id": "delivered", "task_ref": self.flow.task_ref,
            "task_key": {"task_id": self.flow.key["task_id"], "lifecycle_generation": self.flow.key["lifecycle_generation"]}},
            result)
        after = self.projection.resolve(self.flow.key)
        self.assertEqual("delivered", after["phase"])
        self.assertIsNone(after["publication_result"])
        self.assertEqual(before["results"], after["results"])
        self.assertEqual([], self.projection.read_record()["completion_results"])
        fact = after["delivery_result"]
        self.assertEqual("delivery:" + self.merge, fact["result_id"])
        self.assertEqual(self.merge, fact["merge_commit"])
        self.assertEqual(self.actual, fact["reviewed_head"])
        self.assertEqual(self.actual, fact["candidate"]["head_ref"])
        self.assertEqual(self.common_base, fact["candidate"]["base_ref"])
        self.assertEqual(["app.txt"], fact["candidate"]["paths"])
        with self.projection.api.delivery_store.GitCandidateContent(self.repo) as content:
            self.assertEqual(content.content_ref(self.actual, ["app.txt"]), fact["candidate"]["content_ref"])
            self.assertNotEqual(content.content_ref(self.merge, ["app.txt"]), fact["candidate"]["content_ref"])

        recorded = self.task_json.read_bytes()
        self.checks = []
        self.responses()
        self.assertEqual(result, self.invoke())
        self.assertEqual(recorded, self.task_json.read_bytes())
        calls = [json.loads(line) for line in self.calls.read_text().splitlines()]
        self.assertTrue(any(call[:3] == ["pr", "view", "9"] and "statusCheckRollup" in call[-1] for call in calls))
        self.assertFalse(any(call[:2] == ["pr", "merge"] for call in calls))

    def test_rejects_unrelated_pr_that_inherited_the_original_delivery(self):
        self.base = self.merge
        self.flow.git("switch", "-qc", "feat/unrelated", "main")
        (self.repo / "unrelated.txt").write_text("Other change\n")
        self.flow.git("add", "unrelated.txt")
        self.flow.git("commit", "-qm", "Add an unrelated file")
        self.actual = self.flow.git("rev-parse", "HEAD").strip()
        self.flow.git("switch", "main")
        self.flow.git("merge", "--no-ff", "-m", "Merge pull request #10", "feat/unrelated")
        self.merge = self.flow.git("rev-parse", "HEAD").strip()
        self.flow.git("switch", "feat/flow")
        self.public["pr_number"] = 10
        self.responses(number=10)
        self.assertEqual(self.flow.git("show", f"{self.base}:{self.flow.task_ref}/task.json"),
            self.flow.git("show", f"{self.actual}:{self.flow.task_ref}/task.json"))
        self.assertEqual("unrelated.txt", self.flow.git("diff", "--name-only", self.base, self.actual).strip())
        before = self.task_json.read_bytes()

        result = self.invoke()

        self.assertEqual("merge_blocked", result["exit_id"])
        self.assertEqual("merged_pr_attribution_missing", result["reason_code"])
        self.assertEqual(10, result["pr_number"])
        self.assertEqual(before, self.task_json.read_bytes())

    def test_rejects_newly_accepted_task_scope_without_writing_delivery(self):
        from runtime.delivery_projection.adapter import authority_ref

        authority = self.repo / "requirements.md"
        authority.write_text("R1: deliver the original feature. R2: cover an additional requirement.\n")
        self.projection.scope(authority_ref(authority, self.repo))
        before = self.task_json.read_bytes()

        result = self.invoke()

        self.assertEqual("merge_blocked", result["exit_id"])
        self.assertEqual("merged_pr_scope_mismatch", result["reason_code"])
        self.assertEqual(before, self.task_json.read_bytes())


if __name__ == "__main__":
    unittest.main()
