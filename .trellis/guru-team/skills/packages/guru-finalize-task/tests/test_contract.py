from __future__ import annotations

from support import *  # noqa: F403


class FinalizeTaskContractTests(unittest.TestCase):
    def test_all_json_documents_and_schemas_are_valid(self) -> None:
        for path in PACKAGE.rglob("*.json"):
            with self.subTest(path=path.relative_to(PACKAGE)):
                payload = json.loads(path.read_text(encoding="utf-8"))
                if path.name.endswith(".schema.json"):
                    jsonschema.Draft202012Validator.check_schema(payload)

    def test_current_lifecycle_module_is_packaged(self) -> None:
        self.assertTrue((PACKAGE / "runtime/lifecycle.py").is_file())

    def test_interface_projects_minimal_merge_identity(self) -> None:
        interface = load("interface.json")
        projection = next(
            item for item in interface["public_contracts"]["projections"]
            if item["id"] == "project_ready_for_merge"
        )
        self.assertEqual(
            [item["source"] for item in projection["mappings"]],
            [
                "repo_ref",
                "pr_number",
                "pr_url",
                "expected_head_sha",
                "expected_base_branch",
                "expected_head_branch",
                "publication_body_sha256",
            ],
        )
        consumer_input = next(
            item for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "ready_for_merge_input"
        )
        self.assertEqual(
            consumer_input["contract"]["seed_fields"][-1],
            "publication_body_sha256",
        )

    def test_ready_output_has_no_close_projection(self) -> None:
        output = load("examples/public-ready-for-merge-output.json")
        jsonschema.Draft202012Validator(
            load("schemas/public-ready-for-merge-output.schema.json")
        ).validate(output)
        publication = load("examples/public-publication-ready-input.json")
        self.assertEqual(
            output["publication_body_sha256"],
            hashlib.sha256(publication["pr_body"].encode("utf-8")).hexdigest(),
        )

    def test_ready_output_materializes_exact_publication_body_identity(self) -> None:
        root = Path("/repo")
        task_dir = root / ".trellis/tasks/archive/2026-09/example"
        body = "## Issue 关闭范围\n\nCloses #247\n"
        plan = {
            "task": {"archive_locator": ".trellis/tasks/archive/2026-09/example"},
            "git": {
                "repo": "castbox/guru-trellis",
                "base_branch": "main",
                "head_branch": "codex/finalizer-contract-fixture",
            },
            "publish": {"body": body},
        }
        gate = {
            "route": {
                "typed_exit": "ready_for_merge",
                "output": copy.deepcopy(GTT.FINALIZATION_EXECUTOR_OUTPUT_MARKER),
            }
        }
        pr = {
            "number": 247,
            "url": "https://github.com/castbox/guru-trellis/pull/247",
            "headRefOid": "1" * 40,
        }
        with mock.patch.object(
            GTT,
            "finalization_output_contract",
            return_value=load("schemas/public-ready-for-merge-output.schema.json"),
        ):
            materialized = GTT.finalization_gate_with_ready_for_merge_output(
                root, task_dir, gate, plan, pr
            )

        self.assertEqual(
            materialized["route"]["output"]["publication_body_sha256"],
            hashlib.sha256(body.encode("utf-8")).hexdigest(),
        )

    def test_pr_quality_accepts_publication_owned_closing_keyword(self) -> None:
        body = """## 变更摘要
- 删除旧关闭数组

## 影响范围
Finalizer 只绑定 PR payload。

## 验证结果
已运行 targeted tests。

## 安全说明
无新增安全影响。

## Review Gate
Publication 已审查精确 PR payload。

## Issue 关闭范围
由本 PR body 表达关闭效果。

## Docs SSOT
- requirements: current
- design: current
- tests: current

Closes #247
"""
        errors = GTT.validate_pr_body_quality(body, False)
        self.assertFalse(any("close keyword" in error for error in errors))

    def test_metadata_commit_subject_is_issue_independent(self) -> None:
        self.assertEqual(
            GTT.format_metadata_commit_subject(),
            "chore(trellis): 固化任务收尾元数据",
        )

    def test_owner_fragments_satisfy_line_limit(self) -> None:
        for path in sorted((PACKAGE / "runtime").glob("_owner_part_*.py")):
            with self.subTest(path=path.name):
                self.assertLessEqual(
                    len(path.read_text(encoding="utf-8").splitlines()),
                    3000,
                )

    def test_eval_staging_preview_rejects_nonempty_after_archive_hook_before_context(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            public_input, sentinel = eval_after_archive_hook_fixture(root)
            args = SimpleNamespace(root=str(root), input="input.json")
            with mock.patch.dict(
                os.environ,
                {"GURU_TEAM_EVAL_STAGING": "1"},
                clear=False,
            ):
                self.assertIsNotNone(
                    GTT.finalization_eval_preview_context(root, public_input)
                )
                with (
                    mock.patch.object(GTT, "repo_root", return_value=root),
                    mock.patch.object(
                        GTT,
                        "finalization_public_input",
                        return_value=(public_input, root / "input.json"),
                    ),
                    mock.patch.object(
                        GTT,
                        "finalization_eval_preview_context",
                        side_effect=AssertionError(
                            "eval context must not be selected before hook preflight"
                        ),
                    ) as eval_context,
                    mock.patch.object(GTT, "execute_archive_metadata_transaction") as archive,
                    mock.patch.object(GTT, "push_closeout_branch_if_needed") as push,
                    mock.patch.object(GTT, "resolve_closeout_pull_request") as resolve_pr,
                    mock.patch.object(GTT, "create_pull_request") as create_pr,
                    mock.patch.object(GTT, "update_pull_request_metadata") as update_pr,
                    mock.patch.object(GTT, "ensure_closeout_pr_ready") as ready_pr,
                    mock.patch.object(GTT, "run_gh_command") as gh,
                ):
                    with self.assertRaises(GTT.WorkflowError) as caught:
                        GTT.cmd_preview_finalization(args)

            self.assertEqual(
                caught.exception.payload,
                {"stage": "after-archive-hook-preflight"},
            )
            self.assertFalse(sentinel.exists())
            eval_context.assert_not_called()
            for mutation in (
                archive,
                push,
                resolve_pr,
                create_pr,
                update_pr,
                ready_pr,
                gh,
            ):
                mutation.assert_not_called()

    def test_eval_staging_execute_gate_check_rejects_nonempty_after_archive_hook_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            public_input, sentinel = eval_after_archive_hook_fixture(root)
            gate = load("examples/task-finalization-gate.json")
            args = SimpleNamespace(
                root=str(root),
                input="input.json",
                gate="gate.json",
            )
            with mock.patch.dict(
                os.environ,
                {"GURU_TEAM_EVAL_STAGING": "1"},
                clear=False,
            ):
                self.assertIsNotNone(
                    GTT.finalization_eval_preview_context(root, public_input)
                )
                with (
                    mock.patch.object(GTT, "repo_root", return_value=root),
                    mock.patch.object(
                        GTT,
                        "finalization_public_input",
                        return_value=(public_input, root / "input.json"),
                    ),
                    mock.patch.object(
                        GTT,
                        "finalization_gate_input",
                        return_value=(gate, root / "gate.json"),
                    ),
                    mock.patch.object(GTT, "finalization_package_root", return_value=PACKAGE),
                    mock.patch.object(
                        GTT,
                        "finalization_eval_preview_context",
                        side_effect=AssertionError(
                            "eval context must not be selected before hook preflight"
                        ),
                    ) as eval_context,
                    mock.patch.object(GTT, "cmd_finish_work") as finish_work,
                    mock.patch.object(GTT, "execute_archive_metadata_transaction") as archive,
                    mock.patch.object(GTT, "push_closeout_branch_if_needed") as push,
                    mock.patch.object(GTT, "resolve_closeout_pull_request") as resolve_pr,
                    mock.patch.object(GTT, "create_pull_request") as create_pr,
                    mock.patch.object(GTT, "update_pull_request_metadata") as update_pr,
                    mock.patch.object(GTT, "ensure_closeout_pr_ready") as ready_pr,
                    mock.patch.object(GTT, "run_gh_command") as gh,
                    mock.patch.object(GTT, "finalization_write_transaction") as transaction,
                    mock.patch.object(GTT, "write_json") as write_json,
                ):
                    with self.assertRaises(GTT.WorkflowError) as caught:
                        GTT.cmd_execute_finalization_transition(args)

            self.assertEqual(
                caught.exception.payload,
                {"stage": "after-archive-hook-preflight"},
            )
            self.assertFalse(sentinel.exists())
            eval_context.assert_not_called()
            for mutation in (
                finish_work,
                archive,
                push,
                resolve_pr,
                create_pr,
                update_pr,
                ready_pr,
                gh,
                transaction,
                write_json,
            ):
                mutation.assert_not_called()

    def test_workspace_boundary_accepts_clean_tracked_planning_and_blocks_real_overlays(self) -> None:
        temp_root, source, context = workspace_boundary_fixture()
        try:
            snapshot = GTT.collect_workspace_boundary_snapshot(context, {}, {})
            suspicious = snapshot["suspicious_source_artifacts"]
            suspicious_paths = {item["path"] for item in suspicious}
            for name in (
                "task.json",
                "prd.md",
                "design.md",
                "implement.md",
                "implement.jsonl",
                "check.jsonl",
                    ):
                self.assertNotIn(f"{context['task_dir_relative']}/{name}", suspicious_paths)
            for name in GTT.WORKSPACE_BOUNDARY_REVIEW_METADATA:
                self.assertIn(f"{context['task_dir_relative']}/{name}", suspicious_paths)
            self.assertTrue(
                any(item["kind"] == "same_task_reviews_dir" for item in suspicious)
            )

            untracked = source / context["task_dir_relative"] / "implement.jsonl"
            subprocess.run(["git", "rm", "--cached", "-q", str(untracked.relative_to(source))], cwd=source, check=True)
            snapshot = GTT.collect_workspace_boundary_snapshot(context, {}, {})
            self.assertIn(
                str(untracked.resolve()),
                [item["absolute_path"] for item in snapshot["suspicious_source_artifacts"]],
            )

            blocked_context = dict(context)
            blocked_context["actual_repo_root"] = source
            blocked_context["task_dir"] = source / context["task_dir_relative"]
            errors = GTT.workspace_boundary_errors(
                blocked_context,
                snapshot,
                allow_source_clean=True,
            )
            self.assertTrue(any("current-task artifacts" in error for error in errors))
        finally:
            shutil.rmtree(temp_root)

    def test_workspace_boundary_keeps_dirty_task_paths_fail_closed(self) -> None:
        cases = {
            "staged": lambda source, task: (
                (task / "prd.md").write_text("staged\n", encoding="utf-8"),
                subprocess.run(["git", "add", "--", str((task / "prd.md").relative_to(source))], cwd=source, check=True),
            ),
            "unstaged": lambda _source, task: (task / "design.md").write_text("unstaged\n", encoding="utf-8"),
            "deleted": lambda _source, task: (task / "implement.md").unlink(),
            "renamed": lambda source, task: subprocess.run(
                ["git", "mv", str((task / "check.jsonl").relative_to(source)), str((task / "renamed-check.jsonl").relative_to(source))],
                cwd=source,
                check=True,
            ),
            "unrelated": lambda source, _task: (
                (source / "unrelated.txt").write_text("unrelated\n", encoding="utf-8"),
            ),
        }
        for label, mutate in cases.items():
            with self.subTest(case=label):
                temp_root, source, context = workspace_boundary_fixture()
                try:
                    mutate(source, source / context["task_dir_relative"])
                    snapshot = GTT.collect_workspace_boundary_snapshot(context, {}, {})
                    dirty = [item for item in snapshot["suspicious_source_artifacts"] if item["kind"] == "same_task_dirty_path"]
                    if label == "unrelated":
                        self.assertEqual(dirty, [])
                    else:
                        self.assertTrue(dirty)
                finally:
                    shutil.rmtree(temp_root)

    def test_workspace_boundary_does_not_rebuild_missing_runtime_mapping(self) -> None:
        with tempfile.TemporaryDirectory(prefix="guru-boundary-no-rebuild-") as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Guru Test"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "guru@example.com"], cwd=root, check=True)
            task_dir = root / ".trellis/tasks/09-01-327-boundary"
            task_dir.mkdir(parents=True)
            (task_dir / "task.json").write_text(
                json.dumps(
                    {
                        "id": "327-boundary",
                        "name": "327-boundary",
                        "title": "boundary",
                        "status": "in_progress",
                        "branch": "main",
                        "base_branch": "main",
                    }
                ),
                encoding="utf-8",
            )
            git_fixture_commit(root, ".trellis/tasks/09-01-327-boundary/task.json")
            config = {"runtime_root": str(root / ".runtime")}
            with mock.patch.object(GTT, "rebuild_runtime_mappings") as rebuild:
                with self.assertRaises(GTT.WorkflowError) as caught:
                    GTT.load_task_runtime_identity(task_dir, config, allow_rebuild=False)
            rebuild.assert_not_called()
            self.assertIn("could not derive or rebuild", str(caught.exception))
            self.assertFalse((root / ".runtime").exists())

    def test_large_finish_summary_preserves_complete_path_contract(self) -> None:
        payload = large_finish_summary()
        self.assertEqual(GTT.finish_summary_errors(payload), [])

        cases = {}
        mismatch = copy.deepcopy(payload)
        mismatch["index"]["search_terms"]["paths"] = payload["git"]["changed_paths"][:-1]
        cases["mismatch"] = (
            mismatch,
            "index.search_terms.paths must equal sorted git.changed_paths.",
        )
        unsorted = copy.deepcopy(payload)
        unsorted_paths = list(reversed(payload["git"]["changed_paths"]))
        unsorted["git"]["changed_paths"] = unsorted_paths
        unsorted["index"]["search_terms"]["paths"] = unsorted_paths
        cases["unsorted"] = (
            unsorted,
            "git.changed_paths must be sorted and unique.",
        )
        duplicate = copy.deepcopy(payload)
        duplicate_paths = payload["git"]["changed_paths"] + [payload["git"]["changed_paths"][-1]]
        duplicate["git"]["changed_paths"] = duplicate_paths
        duplicate["index"]["search_terms"]["paths"] = duplicate_paths
        cases["duplicate"] = (
            duplicate,
            "git.changed_paths must be sorted and unique.",
        )
        unsafe = copy.deepcopy(payload)
        unsafe_paths = payload["git"]["changed_paths"][:-1] + ["../unsafe.txt"]
        unsafe["git"]["changed_paths"] = unsafe_paths
        unsafe["index"]["search_terms"]["paths"] = unsafe_paths
        cases["unsafe"] = (
            unsafe,
            "git.changed_paths[] must not contain empty, dot, or parent segments.",
        )

        for name, (invalid, expected_error) in cases.items():
            with self.subTest(case=name):
                self.assertIn(expected_error, GTT.finish_summary_errors(invalid))

    def test_step_local_contract_matches_current_gate_and_exit_graph(self) -> None:
        skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        contract = (PACKAGE / "references/contract.md").read_text(encoding="utf-8")
        interface = load("interface.json")
        gate = load("schemas/task-finalization-gate-5.0.schema.json")
        exits = [item["id"] for item in interface["external_exits"]]
        output_exits = [item["exit_id"] for item in interface["public_contracts"]["outputs"]]

        self.assertIn("and six typed exits.", skill)
        self.assertIn("and six typed exits.", interface["description"])
        self.assertIn("current aggregate input is 7.0, gate is 5.0, and ignored transaction is 3.0", contract)
        self.assertIn("The five inputs are", contract)
        self.assertIn("The six exits are", contract)
        self.assertEqual(6, len(exits))
        self.assertEqual(exits, output_exits)
        self.assertEqual(
            exits,
            gate["properties"]["route"]["properties"]["typed_exit"]["enum"],
        )
        self.assertEqual(exits[0], "base_reconciliation_required")

    def test_private_owner_failure_preserves_fail_closed_diagnostics(self) -> None:
        sys.path.insert(0, str(shared_runtime_parent()))
        sys.path.insert(0, str(PACKAGE / "runtime"))
        spec = importlib.util.spec_from_file_location(
            "finalize_common_test", PACKAGE / "runtime/common.py"
        )
        assert spec and spec.loader
        common = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(common)

        class FakeOwner:
            class WorkflowError(RuntimeError):
                def __init__(self) -> None:
                    super().__init__("archive path is unsafe")
                    self.exit_code = 2
                    self.payload = {
                        "stage": "archive-path-preflight",
                        "component": "archive-root",
                    }

        def fail() -> dict:
            raise FakeOwner.WorkflowError()

        from runtime.io import CommandError

        with self.assertRaises(CommandError) as raised:
            common.call_owner(FakeOwner, fail)
        self.assertEqual(raised.exception.code, "finalization_stale")
        self.assertEqual(raised.exception.response_stream, "stderr")
        self.assertEqual(
            raised.exception.response,
            {
                "status": "error",
                "error": "archive path is unsafe",
                "stage": "archive-path-preflight",
                "component": "archive-root",
            },
        )

    def test_package_runtime_has_no_verifier_consumer_artifact_or_monolith(self) -> None:
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((PACKAGE / "runtime").glob("*.py"))
        )
        for retired in ("guru_team_trellis.py", "verification_required", "not_required", "finalization_verification", "extension_verification", "marketplace-verification"):
            self.assertNotIn(retired, runtime_text)
        commands = load("commands.json")
        interface = load("interface.json")
        self.assertEqual(
            {(item["validator_id"], item["id"]) for item in commands["commands"]},
            {(item["id"], item["runtime_command"]) for item in interface["validators"]},
        )
        for validator in interface["validators"]:
            self.assertIn("runtime/launch.sh", (PACKAGE / validator["command"]).read_text(encoding="utf-8"))

    def test_public_invoke_is_the_only_public_command_and_wrapper(self) -> None:
        commands = load("commands.json")["commands"]
        by_id = {item["id"]: item for item in commands}
        self.assertNotIn("finalize-task-happy-path", by_id)
        self.assertEqual(
            by_id["invoke-guru-finalize-task"]["entrypoint"],
            "runtime/invoke.py",
        )
        invocation = load("interface.json")["public_contracts"]["invocation"]
        self.assertEqual(invocation["wrapper"], "scripts/invoke.sh")
        self.assertEqual(
            [
                item["runtime_command"]
                for item in load("interface.json")["validators"]
                if item["id"] == "public_invocation"
            ],
            ["invoke-guru-finalize-task"],
        )
        self.assertFalse((PACKAGE / "scripts/finalize-task-happy-path.sh").exists())
        jsonschema.Draft202012Validator(
            load("../../schemas/skill-commands.schema.json")
        ).validate(load("commands.json"))

    def test_public_invoke_confirmation_identity_tracks_only_material_plan(self) -> None:
        public_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": ".trellis/tasks/09-02-330-finalizer",
        }
        plan = {
            "task": {"active_locator": public_input["task_ref"]},
            "git": {
                "repo": "castbox/guru-trellis",
                "base_branch": "main",
                "head_branch": "fix/330-finalizer",
                "branch_review_commit": "a" * 40,
            },
            "publish": {"title": "feat: finalizer", "body": "Closes #330"},
        }
        context = {
            "plan": plan,
            "publication_mode": "ordinary_publication",
            "transaction_state": "prepared",
            "reprepare_reason_code": None,
            "published_transition_complete": False,
        }
        identity = GTT.finalization_confirmation_identity(public_input, context)
        same_plan_progress = copy.deepcopy(context)
        same_plan_progress.update(
            transaction_state="archived",
            reprepare_reason_code=GTT.FINALIZATION_REPREPARE_ARCHIVE_MONTH,
            published_transition_complete=True,
        )
        self.assertEqual(
            GTT.finalization_confirmation_identity(public_input, same_plan_progress),
            identity,
        )

        mutations = (
            ("repo", lambda value: value["plan"]["git"].update(repo="castbox/other")),
            ("base", lambda value: value["plan"]["git"].update(base_branch="release")),
            ("head", lambda value: value["plan"]["git"].update(head_branch="fix/other")),
            ("commit", lambda value: value["plan"]["git"].update(branch_review_commit="b" * 40)),
            ("title", lambda value: value["plan"]["publish"].update(title="feat: changed")),
            ("body", lambda value: value["plan"]["publish"].update(body="Closes #330\n\nChanged")),
            ("side_effect_set", lambda value: value.update(publication_mode="existing_pr_recovery")),
        )
        for label, mutate in mutations:
            changed = copy.deepcopy(context)
            mutate(changed)
            with self.subTest(label=label):
                self.assertNotEqual(
                    GTT.finalization_confirmation_identity(public_input, changed),
                    identity,
                )

    def test_public_invoke_stale_confirmation_blocks_before_record_or_execute(self) -> None:
        transaction = load_transaction()
        record = mock.Mock(side_effect=AssertionError("must block before record"))
        execute = mock.Mock(side_effect=AssertionError("must block before execute"))

        class WorkflowError(RuntimeError):
            pass

        owner = SimpleNamespace(
            WorkflowError=WorkflowError,
            repo_root=lambda path: Path("/repo"),
            finalization_public_input=lambda *_: (
                {"profile": "publication_ready", "mode": "workflow", "task_ref": "task"},
                "input.json",
            ),
            finalization_semantic_review_input=lambda *_: {
                "route": {"typed_exit": "ready_for_merge"}
            },
            finalization_preview_context=lambda *_: {
                "plan": {},
                "transaction_state": "prepared",
                "published_transition_complete": False,
            },
            finalization_confirmation_identity=lambda *_: "b" * 64,
            finalization_record_gate_result=record,
            execute_finalization_transition_result=execute,
            finalization_output_contract=lambda *_: {},
            skill_json_schema_validation_errors=lambda *_: [],
        )
        counters: dict[str, int] = {}
        output = transaction.execute_confirmed_transaction(
            owner,
            SimpleNamespace(
                root="/repo",
                input="input.json",
                review_input="review.json",
                confirmed_preview_sha256="a" * 64,
            ),
            counters=counters,
        )
        self.assertEqual(output["exit_id"], "blocked")
        self.assertEqual(output["reason_code"], "invalid_private_state")
        record.assert_not_called()
        execute.assert_not_called()
        self.assertEqual(counters["terminal.post_exit_operation"], 0)

    def test_public_invoke_budget_and_recommended_invocation_are_exact(self) -> None:
        transaction = load_transaction()
        self.assertEqual(
            transaction.invoke_budget(),
            {
                "component_path_command_invocations": 5,
                "public_invoke_command_invocations": 1,
                "command_reduction_percent": 80,
                "component_path_full_preview_reads": 5,
                "public_invoke_full_preview_reads": 1,
                "full_preview_read_reduction_percent": 80,
            },
        )
        interface = load("interface.json")
        public = [
            item for item in interface["validators"]
            if item["id"] == "public_invocation"
        ]
        self.assertEqual([item["runtime_command"] for item in public], ["invoke-guru-finalize-task"])
        self.assertNotIn(
            "legacy_public_invocation",
            {item["id"] for item in interface["validators"]},
        )
        for facts_path in sorted((PACKAGE / "evals/files").glob("*facts.json")):
            arguments = load(facts_path.relative_to(PACKAGE).as_posix())[
                "public_invocation"
            ]["arguments"]
            self.assertIn("--review-input", arguments)
            self.assertNotIn("--owner-result", arguments)

    def test_current_contract_has_no_verifier_edge_or_reentry(self) -> None:
        interface = load("interface.json")
        contracts = interface["public_contracts"]
        self.assertEqual(
            contracts["input"]["aggregate_schema"],
            {
                "schema_id": "guru-finalize-task-input-aggregate-7.0",
                "path": "schemas/public-input-7.0.schema.json",
            },
        )
        self.assertEqual(
            [item["id"] for item in contracts["input"]["profiles"]],
            ["publication_ready", "same_plan_resume", "reprepare_preview", "standalone_finalization", "archived_review_refresh"],
        )
        self.assertEqual(
            [item["exit_id"] for item in contracts["outputs"]],
            ["base_reconciliation_required", "publication_review_stale", "resume_finalization", "reprepare_required", "ready_for_merge", "blocked"],
        )
        serialized = json.dumps(contracts, sort_keys=True)
        for retired in (
            "verification_required",
            "verification_verified",
            "standalone_verification_not_required",
            "guru-verify-extension-installation",
        ):
            self.assertNotIn(retired, serialized)

    def test_publication_stale_route_rejects_mismatched_owner_facts_and_current_status(self) -> None:
        task_ref = ".trellis/tasks/08-17-253-planless-stale"
        owner_commit = "a" * 40
        context = {
            "plan": None,
            "plan_ref": None,
            "transaction_state": "publication_review_stale",
            "publication_status": "stale",
            "publication_stale_reason": "publication_review_stale",
            "publication_branch_review_commit": owner_commit,
        }
        route = {
            "typed_exit": "publication_review_stale",
            "consumer": copy.deepcopy(
                GTT.FINALIZATION_CONSUMERS["publication_review_stale"]
            ),
            "output": {
                "exit_id": "publication_review_stale",
                "task_ref": task_ref,
                "branch_review_commit": owner_commit,
                "stale_reason": "publication_review_stale",
            },
        }
        with mock.patch.object(GTT, "finalization_package_root", return_value=PACKAGE):
            GTT.finalization_validate_route(
                Path("/repo"), {"task_ref": task_ref}, context, route
            )
            cases = {
                "wrong_task": {"task_ref": ".trellis/tasks/other"},
                "wrong_owner_commit": {"branch_review_commit": "b" * 40},
                "wrong_reason": {"stale_reason": "publication_review_missing"},
            }
            for name, changes in cases.items():
                with self.subTest(case=name):
                    invalid = copy.deepcopy(route)
                    invalid["output"].update(changes)
                    with self.assertRaises(GTT.WorkflowError):
                        GTT.finalization_validate_route(
                            Path("/repo"),
                            {"task_ref": task_ref},
                            context,
                            invalid,
                        )
            current = copy.deepcopy(context)
            current["publication_status"] = "current"
            with self.assertRaises(GTT.WorkflowError):
                GTT.finalization_validate_route(
                    Path("/repo"), {"task_ref": task_ref}, current, route
                )

    def test_preexisting_summary_uses_adopted_ready_state(self) -> None:
        transaction = {
            "mode": "existing_pr_recovery",
            "adopted_pr": {"initial_is_draft": False},
        }
        self.assertFalse(
            GTT.finalization_expected_pr_draft_state(
                transaction,
                current_finalizer=True,
            )
        )

    def test_current_schema_aliases_match_explicit_acceptance_domains(self) -> None:
        pairs = (
            (
                "schemas/semantic-review-input.schema.json",
                "schemas/semantic-review-input-3.0.schema.json",
                load("examples/semantic-review-input.json"),
            ),
            (
                "schemas/task-finalization-gate.schema.json",
                "schemas/task-finalization-gate-5.0.schema.json",
                load("examples/task-finalization-gate.json"),
            ),
        )
        for alias_path, explicit_path, positive in pairs:
            with self.subTest(alias=alias_path):
                alias_bytes = (PACKAGE / alias_path).read_bytes()
                explicit_bytes = (PACKAGE / explicit_path).read_bytes()
                self.assertEqual(alias_bytes, explicit_bytes)
                alias = jsonschema.Draft202012Validator(load(alias_path))
                explicit = jsonschema.Draft202012Validator(load(explicit_path))
                negative = json.loads(json.dumps(positive))
                negative["route"]["typed_exit"] = "verification_required"
                extra_property = json.loads(json.dumps(positive))
                extra_property["unexpected"] = True
                for instance, expected in (
                    (positive, True),
                    (negative, False),
                    (extra_property, False),
                ):
                    self.assertEqual(alias.is_valid(instance), expected)
                    self.assertEqual(explicit.is_valid(instance), expected)

    def test_current_input_examples_validate(self) -> None:
        interface = load("interface.json")
        for profile in interface["public_contracts"]["input"]["profiles"]:
            schema = load(profile["schema"]["path"])
            example = load(profile["example"]["path"])
            jsonschema.Draft202012Validator(schema).validate(example)

    def test_base_reconciliation_output_is_distinct_from_publication_stale(self) -> None:
        output = load("examples/public-base-reconciliation-required-output.json")
        jsonschema.Draft202012Validator(load("schemas/public-base-reconciliation-required-output.schema.json")).validate(output)
        self.assertEqual(output["task_head"], output["publication_head"])
        self.assertEqual(output["resume_target"], "finalization_resume")
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(load("schemas/public-publication-review-stale-output.schema.json")).validate(output)


if __name__ == "__main__":
    unittest.main()
