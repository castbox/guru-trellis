from __future__ import annotations

from support import *  # noqa: F403


def workspace_producer_fixture():
    path = PACKAGE.parent / "guru-create-task-workspace/tests/test_contract.py"
    spec = importlib.util.spec_from_file_location("archive_workspace_producer_tests", path)
    module = importlib.util.module_from_spec(spec)
    # The producer tests use package-local short module names.
    names = ("check", "common", "execute", "invoke", "record")
    previous = {name: sys.modules.pop(name) for name in names if name in sys.modules}
    search_path = sys.path[:]
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = search_path
        for name in names:
            sys.modules.pop(name, None)
        sys.modules.update(previous)
    return module.WorkspaceTest()


class ArchiveMappingTests(unittest.TestCase):
    def setUp(self):
        self.producer = workspace_producer_fixture()
        self.producer.setUp()
        self.addCleanup(self.producer.tearDown)
        result, checked = self.producer.execute_and_check()
        self.assertEqual("passed", checked["checker"]["status"])
        self.source = self.producer.repo.resolve()
        self.root = (self.producer.parent / "repo-worktrees/027-workspace").resolve()
        self.active = result["created_workspace"]["task_artifact_dir"]
        self.task_dir = self.root / self.active
        (self.root / ".gitignore").write_text(".trellis/.runtime/\n__pycache__/\n*.pyc\n")
        subprocess.run(
            [sys.executable, ".trellis/scripts/task.py", "start", self.active],
            cwd=self.root, check=True, capture_output=True,
        )
        for name in ("prd.md", "design.md", "implement.md"):
            (self.task_dir / name).write_text(f"# {name}\n\nArchive identity fixture.\n")
        git_fixture_commit(self.root, self.active, ".gitignore")
        self.head = GTT.current_head(self.root)
        self.context = GTT.load_task_runtime_identity(
            self.task_dir, GTT.load_config(self.root), allow_rebuild=False
        )
        self.plan = GTT.build_finalization_plan(
            self.root, self.task_dir, self.context, GTT.task_json(self.task_dir),
            repo="example/repo", remote="origin", base_branch="main",
            head_branch="feat/027-workspace", branch_review_commit=self.head,
            title="Archive mapping convergence",
            body="## \u53d8\u66f4\u6458\u8981\n\n- Converge task mappings after archive.\n\nRefs #27\n",
            review_facts={"changed_paths": [self.active + "/task.json"]},
        )
        self.archived = self.root / self.plan["task"]["archive_locator"]
        self.pr = {"number": 27, "url": "https://github.com/example/repo/pull/27"}
        GTT.write_json(
            self.task_dir / GTT.FINISH_SUMMARY_ARTIFACT,
            GTT.closeout_summary_for_pr(self.plan, self.pr),
        )
        self.mapping_paths = [
            GTT.runtime_task_path(checkout, GTT.load_config(self.root), "027-workspace")
            for checkout in (self.source, self.root)
        ]
        self.original_mappings = {path: GTT.read_json(path) for path in self.mapping_paths}
        self.workspace_paths = [
            GTT.runtime_workspace_path(checkout, GTT.load_config(self.root), "027-workspace")
            for checkout in (self.source, self.root)
        ]
        self.workspace_bytes = {path: path.read_bytes() for path in self.workspace_paths}

    def assert_converged(self):
        for path in self.mapping_paths:
            self.assertEqual(
                {**self.original_mappings[path], "task_artifact_dir": self.plan["task"]["archive_locator"]},
                GTT.read_json(path),
            )
        self.assertEqual(self.workspace_bytes, {path: path.read_bytes() for path in self.workspace_paths})
        self.assertFalse((self.source / self.plan["task"]["archive_locator"]).exists())
        process = subprocess.run(
            [sys.executable, str(PACKAGE / "runtime/lifecycle.py"),
             "check-workspace-boundary", "--root", str(self.root),
             "--task", str(self.archived), "--json"],
            text=True, capture_output=True,
        )
        self.assertEqual(0, process.returncode, process.stdout + process.stderr)

    def archive(self):
        return GTT.execute_archive_metadata_transaction(
            self.root, self.task_dir, self.plan, bound_pr=self.pr
        )

    def archive_without_mapping_consumer(self):
        # The normal producer and official archive leave their original projections
        # untouched until Finalizer consumes the committed move.
        subprocess.run(
            [sys.executable, ".trellis/scripts/task.py", "archive", self.task_dir.name, "--no-commit"],
            cwd=self.root, check=True, capture_output=True,
        )
        GTT.compact_closeout_archive(self.archived, self.plan)
        git_fixture_commit(self.root, self.active, self.plan["task"]["archive_locator"])
        subprocess.run(
            ["git", "push", "-q", "origin", "feat/027-workspace"],
            cwd=self.root, check=True, capture_output=True,
        )

    def test_normal_producer_archive_converges_both_mappings(self):
        archived, transaction = self.archive()
        self.assertEqual(self.archived, archived)
        self.assertEqual(self.head, transaction["parent"])
        self.assert_converged()
        self.assertEqual([], GTT.git_status_paths(self.root))

    def test_committed_archive_recovery_is_idempotent(self):
        self.archive_without_mapping_consumer()
        self.assertEqual(self.original_mappings, {path: GTT.read_json(path) for path in self.mapping_paths})
        before_head = GTT.current_head(self.root)
        before_archive = {p.name: p.read_bytes() for p in self.archived.iterdir() if p.is_file()}
        original_run = GTT.run
        calls = []

        def observed(argv, **kwargs):
            calls.append(argv)
            return original_run(argv, **kwargs)

        with mock.patch.object(GTT, "run", side_effect=observed):
            first = GTT.resume_archive_metadata_transaction(self.root, self.archived, self.plan, bound_pr=self.pr)
            mapping_bytes = {path: path.read_bytes() for path in self.mapping_paths}
            second = GTT.resume_archive_metadata_transaction(self.root, self.archived, self.plan, bound_pr=self.pr)
        self.assertEqual(first, second)
        self.assertEqual(before_head, GTT.current_head(self.root))
        self.assertEqual(mapping_bytes, {path: path.read_bytes() for path in self.mapping_paths})
        self.assertEqual(before_archive, {p.name: p.read_bytes() for p in self.archived.iterdir() if p.is_file()})
        self.assertFalse(any(argv[:2] in (["git", "push"], ["git", "commit"], ["git", "add"]) for argv in calls))
        self.assert_converged()

    def test_ready_executor_converges_before_materialization(self):
        self.archive_without_mapping_consumer()
        gate = {"route": {"typed_exit": "ready_for_merge"}}
        context = {"task_dir": self.archived, "transaction_state": "ready", "plan": self.plan, "published_pr": self.pr}

        def materialize(*args):
            self.assert_converged()
            return {"route": {"output": {"exit_id": "ready_for_merge"}}}

        with (
            mock.patch.object(GTT, "finalization_gate_with_ready_for_merge_output", side_effect=materialize),
            mock.patch.object(GTT, "finalization_retire_current_state", return_value=False),
            mock.patch.object(GTT, "cmd_finish_work") as finish,
            mock.patch.object(GTT, "ensure_closeout_pr_ready") as ready,
        ):
            result = GTT.execute_finalization_transition_result(self.root, SimpleNamespace(), {}, gate, context)
        self.assertEqual("ready_recovered", result["stage"])
        finish.assert_not_called()
        ready.assert_not_called()

    def test_missing_source_mapping_blocks_before_archive(self):
        self.mapping_paths[0].unlink()
        target_before = self.mapping_paths[1].read_bytes()
        with self.assertRaises(GTT.WorkflowError):
            self.archive()
        self.assertTrue(self.task_dir.is_dir())
        self.assertFalse(self.archived.exists())
        self.assertEqual(self.head, GTT.current_head(self.root))
        self.assertEqual(target_before, self.mapping_paths[1].read_bytes())
        self.assertFalse(self.mapping_paths[0].exists())

    def test_wrong_current_branch_blocks_without_mapping_writes(self):
        self.archive_without_mapping_consumer()
        subprocess.run(["git", "checkout", "-qb", "other-task"], cwd=self.root, check=True)
        before = {path: path.read_bytes() for path in self.mapping_paths}
        with self.assertRaises(GTT.WorkflowError):
            GTT.reconcile_closeout_task_mappings(self.root, self.archived, self.plan)
        self.assertEqual(before, {path: path.read_bytes() for path in self.mapping_paths})

    def test_missing_target_mapping_recovery_does_not_rebuild(self):
        self.archive_without_mapping_consumer()
        self.mapping_paths[1].unlink()
        source_before = self.mapping_paths[0].read_bytes()
        with self.assertRaises(GTT.WorkflowError):
            GTT.reconcile_closeout_task_mappings(self.root, self.archived, self.plan)
        self.assertFalse(self.mapping_paths[1].exists())
        self.assertEqual(source_before, self.mapping_paths[0].read_bytes())

    def test_stale_boundary_is_read_only_before_owner_recovery(self):
        self.archive_without_mapping_consumer()
        before = {path: path.read_bytes() for path in self.mapping_paths}
        process = subprocess.run(
            [sys.executable, str(PACKAGE / "runtime/lifecycle.py"),
             "check-workspace-boundary", "--root", str(self.root),
             "--task", str(self.archived), "--json"],
            text=True, capture_output=True,
        )
        self.assertNotEqual(0, process.returncode)
        self.assertEqual(before, {path: path.read_bytes() for path in self.mapping_paths})
        GTT.reconcile_closeout_task_mappings(self.root, self.archived, self.plan)
        self.assert_converged()


if __name__ == "__main__":
    unittest.main()
