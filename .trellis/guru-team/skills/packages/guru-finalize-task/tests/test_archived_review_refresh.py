from __future__ import annotations

from support import *  # noqa: F403
import test_archive_mappings as mappings


class ArchivedReviewRefreshTests(unittest.TestCase):
    def setUp(self):
        self.fixture = mappings.ArchiveMappingTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.archive()
        self.root = self.fixture.root
        self.archived = self.fixture.archived
        self.a = GTT.current_head(self.root)
        self.b = GTT.run_stdout(["git", "rev-parse", "main"], cwd=self.root)
        self.h = self.fixture.head
        self.input = {
            "profile": "archived_review_refresh", "mode": "workflow",
            "task_ref": self.fixture.plan["task"]["archive_locator"],
            "branch_review_commit": self.a, "reviewed_base_head": self.b,
            "pr_title": self.fixture.plan["publish"]["title"],
            "pr_body": self.fixture.plan["publish"]["body"],
        }
        self.runtime = self.root / ".trellis/.runtime/refresh-test"
        self.runtime.mkdir(parents=True)
        self.input_path = self.runtime / "input.json"
        GTT.write_json(self.input_path, self.input)
        self.review = load("examples/semantic-review-input.json")
        self.review["review"]["summary"] = "Deterministic wrapper fixture, not native semantic review evidence."
        self.review_path = self.runtime / "review.json"
        GTT.write_json(self.review_path, self.review)
        self.state_path = self.runtime / "provider.json"
        self.state = {
            "base": self.b, "head": self.a,
            "pr": {
                **self.fixture.pr, "title": self.input["pr_title"], "body": self.input["pr_body"],
                "headRefName": "feat/027-workspace", "baseRefName": "main",
                "headRefOid": self.a, "isDraft": False, "state": "OPEN",
                "headRepository": {"nameWithOwner": "example/repo"},
                "headRepositoryOwner": {"login": "example"}, "isCrossRepository": False,
            },
        }
        GTT.write_json(self.state_path, self.state)
        self.trace = self.runtime / "calls.jsonl"
        self.bin = self.runtime / "bin"
        self.bin.mkdir()
        real_git = shutil.which("git")
        for command in ("git", "gh"):
            path = self.bin / command
            path.write_text(
                f"#!{sys.executable}\n"
                "import json, os, sys\nfrom pathlib import Path\n"
                f"state = json.loads(Path({str(self.state_path)!r}).read_text())\n"
                f"with Path({str(self.trace)!r}).open('a') as trace: trace.write(json.dumps([{command!r}, *sys.argv[1:]]) + '\\n')\n"
                "args = sys.argv[1:]\n"
                + (
                    "if args[:1] == ['ls-remote']:\n"
                    "    print(state['head'] + '\\trefs/heads/feat/027-workspace'); sys.exit(0)\n"
                    "if args[:1] in (['push'], ['fetch'], ['commit'], ['add'], ['reset'], ['restore'], ['checkout']): sys.exit(81)\n"
                    f"os.execv({real_git!r}, [{real_git!r}, *args])\n"
                    if command == "git" else
                    "if args == ['--version']: print('gh version fixture'); sys.exit(0)\n"
                    "if args[:2] == ['auth', 'status']: sys.exit(0)\n"
                    "if args[:2] == ['pr', 'list']:\n"
                    "    print(json.dumps([state['pr']] if state['pr']['state'] == 'OPEN' else [])); sys.exit(0)\n"
                    "if args[:2] == ['api', 'repos/example/repo/git/ref/heads/main']:\n"
                    "    print(json.dumps({'object': {'sha': state['base'], 'type': 'commit'}})); sys.exit(0)\n"
                    "sys.exit(82)\n"
                ),
                encoding="utf-8",
            )
            path.chmod(0o755)
        subprocess.run([real_git, "remote", "set-url", "origin", "https://github.com/example/repo.git"], cwd=self.root, check=True)
        self.env = {**os.environ, "PATH": str(self.bin) + os.pathsep + os.environ["PATH"], "PYTHONDONTWRITEBYTECODE": "1", "GURU_TEAM_INVOKED_PACKAGE_ROOT": str(PACKAGE)}
        self.env.pop("GURU_TEAM_EVAL_STAGING", None)

    def wrapper(self, script, *args, success=True):
        proc = subprocess.run(
            [str(PACKAGE / "scripts" / script), "--root", str(self.root),
             "--input", self.input_path.relative_to(self.root).as_posix(), *args, "--json"],
            text=True, capture_output=True, env=self.env,
        )
        if success:
            self.assertEqual(0, proc.returncode, proc.stdout + proc.stderr)
            return json.loads(proc.stdout)
        self.assertNotEqual(0, proc.returncode, proc.stdout)
        self.assertNotIn('"internal_error"', proc.stdout + proc.stderr)
        return proc

    def snapshot(self):
        return {
            "refs": GTT.run_stdout(["git", "show-ref"], cwd=self.root),
            "archive": {p.name: p.read_bytes() for p in self.archived.iterdir()},
            "mappings": {str(p): p.read_bytes() for p in self.fixture.mapping_paths + self.fixture.workspace_paths},
            "provider": self.state_path.read_bytes(),
            "status": GTT.git_status_paths(self.root),
        }

    def assert_no_mutation(self):
        calls = [json.loads(line) for line in self.trace.read_text().splitlines()]
        self.assertFalse(any(call[:2] in (["git", "push"], ["git", "fetch"], ["git", "commit"], ["gh", "issue"]) for call in calls))
        self.assertFalse(any(call[:2] == ["gh", "pr"] and call[2] != "list" for call in calls))

    def test_original_preview_record_check_invoke_are_read_only(self):
        before = self.snapshot()
        preview = self.wrapper("preview-finalization.sh")
        self.assertEqual(self.h, preview["original_review_commit"])
        self.assertNotEqual(self.h, preview["branch_review_commit"])
        self.assertFalse(preview["side_effects"])
        self.assertNotIn("confirmation_identity", preview)
        review_arg = self.review_path.relative_to(self.root).as_posix()
        self.wrapper("record-finalization-gate.sh", "--review-input", review_arg)
        self.wrapper("check-finalization-gate.sh")
        output = self.wrapper("invoke.sh", "--review-input", review_arg)
        self.assertEqual("ready_for_merge", output["exit_id"])
        self.assertEqual(self.a, output["expected_head_sha"])
        self.assertEqual(hashlib.sha256(self.input["pr_body"].encode()).hexdigest(), output["publication_body_sha256"])
        self.assertFalse(GTT.task_finalization_path(self.root, self.archived).exists())
        self.assertEqual(before, self.snapshot())
        self.assert_no_mutation()

    def test_original_tip_uses_ancestry_not_position(self):
        self.assertEqual(self.h, GTT.archived_review_original_tip(self.root, [self.h, self.b]))
        self.assertEqual(self.h, GTT.archived_review_original_tip(self.root, [self.b, self.h]))
        with self.assertRaises(GTT.WorkflowError):
            GTT.archived_review_original_tip(self.root, [])

    def test_new_profile_rejects_payload_head_base_and_ready_drift(self):
        original = copy.deepcopy(self.state)
        variants = [
            {"base": self.h},
            {"head": self.h},
            {"pr": {**original["pr"], "title": "Changed title"}},
            {"pr": {**original["pr"], "body": original["pr"]["body"] + "\n"}},
            {"pr": {**original["pr"], "isDraft": True}},
            {"pr": {**original["pr"], "headRefOid": self.h}},
            {"pr": {**original["pr"], "state": "CLOSED"}},
        ]
        for update in variants:
            with self.subTest(update=list(update)):
                GTT.write_json(self.state_path, {**original, **update})
                before = self.snapshot()
                self.wrapper("preview-finalization.sh", success=False)
                self.assertEqual(before, self.snapshot())
        self.assert_no_mutation()

    def test_new_profile_rejects_dirty_archive_and_missing_mapping(self):
        path = self.archived / "design.md"
        path.write_text(path.read_text() + "\nNew unreviewed content\n")
        before = self.snapshot()
        self.wrapper("preview-finalization.sh", success=False)
        self.assertEqual(before, self.snapshot())

    def test_no_mapping_rebuild_or_transaction_reentry(self):
        self.fixture.mapping_paths[0].unlink()
        remaining = self.fixture.mapping_paths[1].read_bytes()
        self.wrapper("preview-finalization.sh", success=False)
        self.assertFalse(self.fixture.mapping_paths[0].exists())
        self.assertEqual(remaining, self.fixture.mapping_paths[1].read_bytes())

    def test_current_old_transaction_blocks_read_only_refresh(self):
        transaction = GTT.finalization_transaction_from_plan(
            self.fixture.plan, next_transition="archive", pr=self.fixture.pr,
        )
        with mock.patch.dict(os.environ, {"GURU_TEAM_INVOKED_PACKAGE_ROOT": str(PACKAGE)}):
            GTT.finalization_write_transaction(self.root, self.archived, transaction)
        path = GTT.finalization_transaction_path(self.root, self.archived)
        before = path.read_bytes()
        self.wrapper("preview-finalization.sh", success=False)
        self.assertEqual(before, path.read_bytes())

    def test_blocked_semantic_result_stays_blocked_and_retires_gate(self):
        review = copy.deepcopy(self.review)
        review["review"]["status"] = "blocked"
        review["route"] = {
            "typed_exit": "blocked", "consumer": {"kind": "stop", "id": "task-finalization-blocked"},
            "output": {"exit_id": "blocked", "reason_code": "prerequisite_incomplete", "remediation": "Resolve the missing current authority evidence."},
        }
        GTT.write_json(self.review_path, review)
        output = self.wrapper("invoke.sh", "--review-input", self.review_path.relative_to(self.root).as_posix())
        self.assertEqual("blocked", output["exit_id"])
        self.assertFalse(GTT.task_finalization_path(self.root, self.archived).exists())
        self.assert_no_mutation()

    def test_transaction_executor_and_confirmation_are_not_available(self):
        review_arg = self.review_path.relative_to(self.root).as_posix()
        self.wrapper("invoke.sh", "--review-input", review_arg, "--confirmed-preview-sha256", "d" * 64, success=False)
        self.wrapper("record-finalization-gate.sh", "--review-input", review_arg)
        self.wrapper("execute-finalization-transition.sh", success=False)
        self.assert_no_mutation()


if __name__ == "__main__":
    unittest.main()
