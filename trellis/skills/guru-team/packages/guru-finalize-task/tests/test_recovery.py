from __future__ import annotations

from support import *  # noqa: F403


class FinalizeTaskRecoveryTests(unittest.TestCase):
    def test_transaction_binds_only_publication_payload(self) -> None:
        plan = {
            "task": {"active_locator": ".trellis/tasks/current"},
            "git": {
                "repo": "castbox/guru-trellis",
                "base_branch": "main",
                "head_branch": "codex/247",
                "branch_review_commit": "a" * 40,
                "publication_head": "b" * 40,
            },
            "plan_digest": "c" * 64,
            "publish": {"title": "修订 Finalizer", "body": "Closes #247"},
        }
        transaction = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="push_content",
            pre_push_remote_head="",
        )
        self.assertEqual(transaction["publication"], plan["publish"])
        jsonschema.Draft202012Validator(
            load("schemas/finalization-transaction.schema.json")
        ).validate(transaction)

    def test_existing_pr_recovery_compares_exact_title_and_body(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "codex/247",
                "base_branch": "main",
                "publication_head": "b" * 40,
                "branch_review_commit": "a" * 40,
            },
            "publish": {"title": "当前标题", "body": "Closes #247"},
        }
        pr = {
            "number": 247,
            "url": "https://github.com/castbox/guru-trellis/pull/247",
            "title": "旧标题",
            "body": "Refs #247",
            "isDraft": True,
            "headRefOid": "a" * 40,
        }
        with mock.patch.object(GTT, "is_ancestor", return_value=True):
            result = GTT.classify_existing_pr_recovery(
                Path("."), plan, existing_pr=pr, remote_head="a" * 40
            )
        self.assertTrue(result["metadata_update_required"])
        self.assertFalse(result["metadata_comparison"]["title_matches"])
        self.assertFalse(result["metadata_comparison"]["body_matches"])

    def test_pre_move_continuity_rechecks_bindings_already_in_publication_parent(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Guru Test"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "guru@example.com"], cwd=root, check=True)

            active_locator = ".trellis/tasks/08-18-270-fixture"
            task_dir = root / active_locator
            task_dir.mkdir(parents=True)
            (task_dir / "task.json").write_bytes(b'{"status":"in_progress"}\n')
            (task_dir / "design.md").write_bytes(b"# Reviewed design\n")
            business = root / "src/feature.txt"
            business.parent.mkdir(parents=True)
            business.write_bytes(b"reviewed business content\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "reviewed content"], cwd=root, check=True)
            review_commit = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True,
                stdout=subprocess.PIPE,
            ).stdout.strip()

            planned_task = b'{"status":"completed"}\n'
            (task_dir / "task.json").write_bytes(planned_task)
            provenance = root / ".trellis/guru-team/extension.json"
            provenance.parent.mkdir(parents=True)
            provenance.write_bytes(b'{"source":"publication"}\n')
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "publication metadata"], cwd=root, check=True)
            publication_parent = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True,
                stdout=subprocess.PIPE,
            ).stdout.strip()

            self.assertEqual(
                GTT.reviewed_content_identity(root, review_commit, include_worktree=False),
                GTT.reviewed_content_identity(root, publication_parent, include_worktree=False),
            )

            summary_bytes = b'{"summary":"planned"}\n'
            (task_dir / GTT.FINISH_SUMMARY_ARTIFACT).write_bytes(summary_bytes)
            hook_state = {}
            plan = {
                "task": {"active_locator": active_locator},
                "inputs": {
                    "official_after_archive_hooks": {
                        "path": ".trellis/config.yaml",
                        "sha256": GTT.canonical_json_sha256(hook_state),
                    },
                },
                "projection": {
                    "move_paths": ["design.md", GTT.FINISH_SUMMARY_ARTIFACT, "task.json"],
                    "tracked_move_paths": ["design.md", "task.json"],
                    "untracked_archive_outputs": [GTT.FINISH_SUMMARY_ARTIFACT],
                    "retired_tracked_paths": [],
                    "reviewed_tracked_bindings": [
                        {
                            "path": "task.json",
                            "mode": "100644",
                            "sha256": hashlib.sha256(planned_task).hexdigest(),
                        },
                    ],
                },
            }

            def validate(candidate: dict = plan) -> None:
                with (
                    mock.patch.object(GTT, "assert_closeout_archive_month_current"),
                    mock.patch.object(
                        GTT, "official_after_archive_hook_state", return_value=hook_state
                    ),
                    mock.patch.object(GTT, "closeout_summary_runtime_pr_facts_from_bytes"),
                ):
                    GTT.validate_closeout_pre_move_continuity(
                        root, task_dir, candidate, publication_parent
                    )

            validate()

            (task_dir / "task.json").write_bytes(b'{"status":"drifted"}\n')
            with self.assertRaises(GTT.WorkflowError):
                validate()

            (task_dir / "task.json").write_bytes(planned_task)
            os.chmod(task_dir / "task.json", 0o755)
            with self.assertRaises(GTT.WorkflowError):
                validate()
            os.chmod(task_dir / "task.json", 0o644)

            (task_dir / "design.md").write_bytes(b"# Unplanned metadata drift\n")
            with self.assertRaises(GTT.WorkflowError):
                validate()
            (task_dir / "design.md").write_bytes(b"# Reviewed design\n")

            extra_binding = copy.deepcopy(plan)
            extra_binding["projection"]["reviewed_tracked_bindings"].append(
                {
                    "path": "missing.md",
                    "mode": "100644",
                    "sha256": hashlib.sha256(b"missing\n").hexdigest(),
                }
            )
            with self.assertRaisesRegex(GTT.WorkflowError, "exactly cover"):
                validate(extra_binding)

            validate()

    def test_execute_ready_recovery_materializes_without_finish_work(self) -> None:
        public_input = {"task_ref": ".trellis/tasks/archive/2026-08/example"}
        gate = {"route": {"typed_exit": "ready_for_merge", "output": {"materialization": "executor"}}}
        task_dir = Path("/repo/.trellis/tasks/archive/2026-08/example")
        context = {
            "transaction_state": "ready",
            "task_dir": task_dir,
            "plan": {"plan_digest": "a" * 64},
            "published_pr": {"number": 218},
        }
        output = {"exit_id": "ready_for_merge", "pr_number": 218}
        args = SimpleNamespace(root="/repo", input="input.json", gate=None)
        with (
            mock.patch.object(GTT, "repo_root", return_value=Path("/repo")),
            mock.patch.object(GTT, "finalization_public_input", return_value=(public_input, Path("/repo/input.json"))),
            mock.patch.object(GTT, "finalization_gate_input", return_value=(gate, Path("/repo/gate.json"))),
            mock.patch.object(GTT, "check_finalization_gate_result", return_value=(gate, context)),
            mock.patch.object(GTT, "reconcile_closeout_task_mappings") as reconcile,
            mock.patch.object(GTT, "finalization_gate_with_ready_for_merge_output", return_value={"route": {"output": output}}) as materialize,
            mock.patch.object(GTT, "finalization_retire_current_state", return_value=["transaction", "gate"]) as retire,
            mock.patch.object(GTT, "cmd_finish_work") as finish_work,
        ):
            result = GTT.cmd_execute_finalization_transition(args)

        self.assertEqual(result["stage"], "ready_recovered")
        self.assertEqual(result["output"], output)
        self.assertEqual(result["retired_owner_state"], ["transaction", "gate"])
        finish_work.assert_not_called()
        reconcile.assert_called_once_with(Path("/repo"), task_dir, context["plan"])
        retire.assert_called_once_with(Path("/repo"), task_dir)
        materialize.assert_called_once_with(
            Path("/repo"), task_dir, gate, context["plan"], context["published_pr"]
        )

    def test_archived_terminal_projection_accepts_retired_exact_gate_locator(self) -> None:
        root = Path("/repo")
        task_dir = root / ".trellis/tasks/archive/2026-08/example"
        expected = root / ".trellis/.runtime/guru-team/example/finalization-gate.json"
        public_input = {"task_ref": ".trellis/tasks/2026-08-example"}
        projected_gate = {
            "route": {
                "typed_exit": "ready_for_merge",
                "output": GTT.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
            },
        }
        with (
            mock.patch.object(GTT, "finalization_task_dir", return_value=task_dir),
            mock.patch.object(GTT, "task_dir_is_archived", return_value=True),
            mock.patch.object(GTT, "task_finalization_path", return_value=expected),
            mock.patch.object(GTT, "finalization_find_transaction_by_task_ref", return_value=None),
            mock.patch.object(GTT, "finalization_current_terminal_gate", return_value=None),
            mock.patch.object(
                GTT,
                "finalization_terminal_projection_gate",
                return_value=projected_gate,
            ),
        ):
            gate, gate_path = GTT.finalization_gate_input(
                root,
                public_input,
                ".trellis/.runtime/guru-team/example/finalization-gate.json",
            )

        self.assertEqual(gate_path, expected)
        self.assertEqual(gate, projected_gate)
        self.assertEqual(gate["route"]["typed_exit"], "ready_for_merge")
        self.assertEqual(gate["route"]["output"], GTT.FINALIZATION_EXECUTOR_OUTPUT_MARKER)

    def test_archived_terminal_projection_requires_retired_exact_gate_locator(self) -> None:
        root = Path("/repo")
        task_dir = root / ".trellis/tasks/archive/2026-08/example"
        expected = root / ".trellis/.runtime/guru-team/example/finalization-gate.json"
        with (
            mock.patch.object(GTT, "finalization_task_dir", return_value=task_dir),
            mock.patch.object(GTT, "task_dir_is_archived", return_value=True),
            mock.patch.object(GTT, "task_finalization_path", return_value=expected),
            mock.patch.object(GTT, "finalization_find_transaction_by_task_ref", return_value=None),
            mock.patch.object(GTT, "finalization_current_terminal_gate", return_value=None),
            mock.patch.object(
                GTT,
                "finalization_terminal_projection_gate",
                return_value={"route": {"typed_exit": "ready_for_merge"}},
            ),
        ):
            with self.assertRaisesRegex(
                GTT.WorkflowError,
                "requires its exact owner-private locator",
            ):
                GTT.finalization_gate_input(
                    root,
                    {"task_ref": ".trellis/tasks/2026-08-example"},
                    None,
                )

    def test_archived_terminal_projection_rejects_wrong_retired_gate_locator(self) -> None:
        root = Path("/repo")
        task_dir = root / ".trellis/tasks/archive/2026-08/example"
        with (
            mock.patch.object(GTT, "finalization_task_dir", return_value=task_dir),
            mock.patch.object(GTT, "task_dir_is_archived", return_value=True),
            mock.patch.object(
                GTT,
                "task_finalization_path",
                return_value=root / ".trellis/.runtime/guru-team/example/finalization-gate.json",
            ),
            mock.patch.object(GTT, "finalization_find_transaction_by_task_ref", return_value=None),
        ):
            with self.assertRaisesRegex(
                GTT.WorkflowError,
                "exact owner-private artifact",
            ):
                GTT.finalization_gate_input(
                    root,
                    {"task_ref": ".trellis/tasks/2026-08-example"},
                    ".trellis/.runtime/guru-team/other/finalization-gate.json",
                )

    def test_terminal_archive_commit_requires_exact_current_archive_head(self) -> None:
        root = Path("/repo")
        task_ref = ".trellis/tasks/example"
        archive_locator = ".trellis/tasks/archive/2026-08/example"
        reviewed = "a" * 40
        parent = "b" * 40
        archive = "c" * 40
        active_paths = {
            f"{task_ref}/task.json",
            f"{task_ref}/prd.md",
            f"{task_ref}/design.md",
            f"{task_ref}/implement.md",
        }
        archive_paths = {
            f"{archive_locator}/{relative}"
            for relative in GTT.CLOSEOUT_ARCHIVE_DURABLE_ARTIFACTS
        }

        def tracked_paths(_root, commit, locator):
            if commit == parent and locator == task_ref:
                return active_paths
            if commit == archive and locator == archive_locator:
                return archive_paths
            return set()

        with (
            mock.patch.object(GTT, "current_head", return_value=archive),
            mock.patch.object(GTT, "closeout_commit_parent", return_value=parent),
            mock.patch.object(
                GTT,
                "closeout_commit_tracked_task_paths",
                side_effect=tracked_paths,
            ),
            mock.patch.object(
                GTT,
                "closeout_commit_paths",
                return_value=active_paths | archive_paths,
            ),
            mock.patch.object(GTT, "is_ancestor", return_value=True),
            mock.patch.object(
                GTT,
                "reviewed_content_identity",
                return_value={"sha256": "d" * 64},
            ),
        ):
            self.assertEqual(
                GTT.finalization_terminal_archive_commit(
                    root,
                    task_ref,
                    archive_locator,
                    reviewed,
                ),
                archive,
            )

    def test_terminal_archive_commit_rejects_post_archive_head(self) -> None:
        root = Path("/repo")
        task_ref = ".trellis/tasks/example"
        archive_locator = ".trellis/tasks/archive/2026-08/example"
        reviewed = "a" * 40
        archive = "b" * 40
        later = "c" * 40
        with (
            mock.patch.object(GTT, "current_head", return_value=later),
            mock.patch.object(GTT, "closeout_commit_parent", return_value=archive),
            mock.patch.object(
                GTT,
                "closeout_commit_tracked_task_paths",
                return_value=set(),
            ),
            mock.patch.object(
                GTT,
                "closeout_commit_paths",
                return_value={"README.md"},
            ),
            mock.patch.object(GTT, "is_ancestor", return_value=True),
            mock.patch.object(
                GTT,
                "reviewed_content_identity",
                return_value={"sha256": "d" * 64},
            ),
        ):
            with self.assertRaisesRegex(
                GTT.WorkflowError,
                "exact reviewed archive metadata commit",
            ):
                GTT.finalization_terminal_archive_commit(
                    root,
                    task_ref,
                    archive_locator,
                    reviewed,
                )

    def test_terminal_archive_commit_real_git_rejects_metadata_tail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
            subprocess.run(
                ["git", "config", "user.name", "Test"], cwd=root, check=True
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.invalid"],
                cwd=root,
                check=True,
            )
            task_ref = ".trellis/tasks/example"
            archive_locator = ".trellis/tasks/archive/2026-08/example"
            active = root / task_ref
            active.mkdir(parents=True)
            artifacts = {
                "task.json": '{"status":"in_progress"}\n',
                "prd.md": "requirements\n",
                "design.md": "design\n",
                "implement.md": "implementation\n",
                "check.jsonl": "{}\n",
            }
            for relative, content in artifacts.items():
                (active / relative).write_text(content, encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "reviewed"], cwd=root, check=True
            )
            reviewed = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=root,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            ).stdout.strip()

            archived = root / archive_locator
            archived.mkdir(parents=True)
            for relative in GTT.CLOSEOUT_ARCHIVE_DURABLE_ARTIFACTS - {
                GTT.FINISH_SUMMARY_ARTIFACT
            }:
                source = active / relative
                target = archived / relative
                target.write_bytes(source.read_bytes())
            (archived / "task.json").write_text(
                '{"status":"completed"}\n', encoding="utf-8"
            )
            (archived / GTT.FINISH_SUMMARY_ARTIFACT).write_text(
                "{}\n", encoding="utf-8"
            )
            shutil.rmtree(active)
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "archive"], cwd=root, check=True
            )
            archive_commit = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=root,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            ).stdout.strip()
            self.assertEqual(
                GTT.finalization_terminal_archive_commit(
                    root,
                    task_ref,
                    archive_locator,
                    reviewed,
                ),
                archive_commit,
            )

            journal = root / ".trellis/workspace/test/journal.md"
            journal.parent.mkdir(parents=True)
            journal.write_text("later metadata\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "later metadata"], cwd=root, check=True
            )
            with self.assertRaisesRegex(
                GTT.WorkflowError,
                "exact reviewed archive metadata commit",
            ):
                GTT.finalization_terminal_archive_commit(
                    root,
                    task_ref,
                    archive_locator,
                    reviewed,
                )

    def test_public_invoke_mapped_reprepare_converges_and_cleans_once(self) -> None:
        transaction = load_transaction()
        task_dir = Path("/repo/.trellis/tasks/09-02-330-finalizer")
        plan = {
            "git": {
                "branch_review_commit": "a" * 40,
                "publication_head": "a" * 40,
            }
        }
        contexts = iter(
            [
                {
                    "plan": plan,
                    "task_dir": task_dir,
                    "transaction_state": "reprepare_required",
                    "published_transition_complete": False,
                    "reprepare_reason_code": "archive_month_changed",
                },
                {
                    "plan": plan,
                    "task_dir": task_dir,
                    "transaction_state": "prepared",
                    "published_transition_complete": False,
                    "reprepare_reason_code": None,
                },
            ]
        )
        reprepare_output = {
            "exit_id": "reprepare_required",
            "task_ref": "task",
            "reason_code": "archive_month_changed",
            "branch_review_commit": "a" * 40,
            "publication_head": "a" * 40,
        }
        ready_output = {"exit_id": "ready_for_merge"}
        execute = mock.Mock(
            side_effect=[
                {"typed_exit": "reprepare_required", "output": reprepare_output},
                {"typed_exit": "ready_for_merge", "output": ready_output},
            ]
        )
        cleanup = mock.Mock(return_value=[])
        owner = SimpleNamespace(
            WorkflowError=RuntimeError,
            FINALIZATION_REPREPARE_ARCHIVE_MONTH="archive_month_changed",
            FINALIZATION_REPREPARE_PROVENANCE_TAIL="provenance_tail_required",
            FINALIZATION_EXECUTOR_OUTPUT_MARKER={"executor": True},
            FINALIZATION_CONSUMERS={
                "reprepare_required": {"kind": "skill", "id": "guru-finalize-task"}
            },
            repo_root=lambda path: Path("/repo"),
            finalization_public_input=lambda *_: (
                {"profile": "publication_ready", "mode": "workflow", "task_ref": "task"},
                "input.json",
            ),
            finalization_semantic_review_input=lambda *_: {
                "schema_version": "3.0",
                "skill_id": "guru-finalize-task",
                "review": {},
                "route": {"typed_exit": "ready_for_merge", "output": ready_output},
            },
            finalization_preview_context=lambda *_: next(contexts),
            finalization_confirmation_identity=lambda *_: "c" * 64,
            finalization_reprepare_public_output=lambda *_args, **_kwargs: reprepare_output,
            finalization_record_gate_result=lambda _root, _input, reviewed, _context, **_kwargs: {
                "gate": {"route": reviewed["route"]},
                "gate_path": Path("/repo/gate.json"),
            },
            check_finalization_gate_context=lambda _root, _input, gate, _path, _context, **_kwargs: (gate, {}),
            execute_finalization_transition_result=execute,
            finalization_output_contract=lambda *_: {},
            skill_json_schema_validation_errors=lambda *_: [],
            finalization_retire_current_state=cleanup,
        )
        counters: dict[str, int] = {}
        output = transaction.execute_confirmed_transaction(
            owner,
            SimpleNamespace(
                root="/repo",
                input="input.json",
                review_input="review.json",
                confirmed_preview_sha256="c" * 64,
            ),
            counters=counters,
        )
        self.assertEqual(output, ready_output)
        self.assertEqual(execute.call_count, 2)
        cleanup.assert_called_once_with(Path("/repo"), Path(task_dir))
        self.assertEqual(counters["mapped.reprepare"], 1)
        self.assertEqual(counters["owner_state.cleanup"], 1)
        self.assertEqual(counters["terminal.post_exit_operation"], 0)

    def test_public_invoke_terminal_stdout_loss_recovery_needs_no_digest_or_cleanup(self) -> None:
        transaction = load_transaction()
        ready_output = {"exit_id": "ready_for_merge"}
        cleanup = mock.Mock(side_effect=AssertionError("terminal recovery is read-only"))
        owner = SimpleNamespace(
            WorkflowError=RuntimeError,
            repo_root=lambda path: Path("/repo"),
            finalization_public_input=lambda *_: (
                {"profile": "same_plan_resume", "mode": "workflow", "task_ref": "task"},
                "input.json",
            ),
            finalization_semantic_review_input=lambda *_: {
                "route": {"typed_exit": "ready_for_merge", "output": ready_output}
            },
            finalization_preview_context=lambda *_: {
                "plan": {},
                "task_dir": Path("/repo/archive/task"),
                "transaction_state": "ready",
                "published_transition_complete": True,
            },
            finalization_confirmation_identity=lambda *_: "d" * 64,
            finalization_record_gate_result=lambda _root, _input, reviewed, _context, **_kwargs: {
                "gate": {"route": reviewed["route"]},
                "gate_path": Path("/repo/gate.json"),
            },
            check_finalization_gate_context=lambda _root, _input, gate, _path, _context, **_kwargs: (gate, {}),
            execute_finalization_transition_result=lambda *_: {
                "typed_exit": "ready_for_merge",
                "output": ready_output,
                "retired_owner_state": True,
            },
            finalization_output_contract=lambda *_: {},
            skill_json_schema_validation_errors=lambda *_: [],
            finalization_retire_current_state=cleanup,
        )
        counters: dict[str, int] = {}
        output = transaction.execute_confirmed_transaction(
            owner,
            SimpleNamespace(
                root="/repo",
                input="input.json",
                review_input="review.json",
                confirmed_preview_sha256=None,
            ),
            counters=counters,
        )
        self.assertEqual(output, ready_output)
        cleanup.assert_not_called()
        self.assertNotIn("mapped.reprepare", counters)
        self.assertNotIn("owner_state.cleanup", counters)
        self.assertEqual(counters["terminal.post_exit_operation"], 0)

    def test_current_gate_and_transaction_remove_verify(self) -> None:
        gate = load("schemas/task-finalization-gate-5.0.schema.json")
        current_gate_alias = load("schemas/task-finalization-gate.schema.json")
        current_review_alias = load("schemas/semantic-review-input.schema.json")
        transaction = load("schemas/finalization-transaction.schema.json")
        self.assertEqual(gate["properties"]["schema_version"]["const"], "5.0")
        self.assertEqual(current_gate_alias["$id"], gate["$id"])
        self.assertEqual(current_gate_alias["properties"]["schema_version"], gate["properties"]["schema_version"])
        explicit_review = load("schemas/semantic-review-input-3.0.schema.json")
        self.assertEqual(current_review_alias["$id"], explicit_review["$id"])
        self.assertEqual(current_review_alias["properties"]["schema_version"], explicit_review["properties"]["schema_version"])
        exits = gate["properties"]["route"]["properties"]["typed_exit"]["enum"]
        self.assertNotIn("verification_required", exits)
        self.assertNotIn("verification_required", current_review_alias["properties"]["route"]["properties"]["typed_exit"]["enum"])
        self.assertIn("base_reconciliation_required", exits)
        self.assertEqual(transaction["properties"]["schema_version"]["const"], "3.0")
        self.assertEqual(
            transaction["properties"]["mode"]["enum"],
            ["ordinary_publication", "existing_pr_recovery"],
        )
        self.assertIn("bind_pr", transaction["properties"]["next_transition"]["enum"])
        self.assertNotIn("bind_draft", transaction["properties"]["next_transition"]["enum"])
        self.assertNotIn("verify", transaction["properties"]["next_transition"]["enum"])
        self.assertNotIn("verification_ref", transaction["properties"])

    def test_existing_pr_recovery_classifies_strict_ancestor_and_scope(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "publish": {"title": "当前标题", "body": "## 变更摘要\n\nCloses #208"},
        }
        pr = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
            "headRefOid": "a" * 40,
            "isDraft": False,
            "title": "旧标题",
            "body": "旧内容\n\nCloses #208",
        }
        with mock.patch.object(GTT, "is_ancestor", return_value=True) as ancestor:
            facts = GTT.classify_existing_pr_recovery(
                Path("/repo"), plan, pr, "a" * 40
            )
        self.assertEqual(facts["mode"], "existing_pr_recovery")
        self.assertEqual(facts["ancestry"], "strict_ancestor")
        self.assertTrue(facts["push_required"])
        self.assertEqual(facts["ready_action"], "preserve_ready")
        self.assertTrue(facts["metadata_update_required"])
        ancestor.assert_called_once_with(Path("/repo"), "a" * 40, "b" * 40)

    def test_existing_pr_recovery_uses_real_git_ancestry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            GTT.run_stdout(["git", "init", "-q"], cwd=root)
            GTT.run_stdout(["git", "config", "user.name", "Guru Test"], cwd=root)
            GTT.run_stdout(["git", "config", "user.email", "guru@example.invalid"], cwd=root)
            marker = root / "marker.txt"
            marker.write_text("old\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "marker.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "old pr head"], cwd=root)
            old_head = GTT.current_head(root)
            marker.write_text("new\n", encoding="utf-8")
            GTT.run_stdout(["git", "commit", "-q", "-am", "publication head"], cwd=root)
            publication_head = GTT.current_head(root)
            plan = {
                "git": {
                    "repo": "castbox/guru-trellis",
                    "remote": "origin",
                    "head_branch": "feat/208",
                    "base_branch": "main",
                    "branch_review_commit": publication_head,
                    "publication_head": publication_head,
                },
                    "publish": {"title": "current", "body": "Closes #208"},
            }
            pr = {
                "number": 59,
                "url": "https://github.com/castbox/guru-trellis/pull/59",
                "headRefOid": old_head,
                "isDraft": False,
                "title": "old",
                "body": "Closes #208",
            }
            facts = GTT.classify_existing_pr_recovery(root, plan, pr, old_head)
            self.assertEqual(facts["ancestry"], "strict_ancestor")
            self.assertTrue(facts["push_required"])

            GTT.run_stdout(["git", "checkout", "-q", old_head], cwd=root)
            marker.write_text("sibling\n", encoding="utf-8")
            GTT.run_stdout(["git", "commit", "-q", "-am", "force pushed sibling"], cwd=root)
            sibling_head = GTT.current_head(root)
            pr["headRefOid"] = sibling_head
            with self.assertRaises(GTT.WorkflowError) as raised:
                GTT.classify_existing_pr_recovery(root, plan, pr, sibling_head)
            self.assertEqual(
                raised.exception.payload["reason_code"],
                "existing_pr_head_not_ancestor",
            )

            unknown_head = "f" * 40
            pr["headRefOid"] = unknown_head
            with self.assertRaises(GTT.WorkflowError) as unknown:
                GTT.classify_existing_pr_recovery(root, plan, pr, unknown_head)
            self.assertEqual(
                unknown.exception.payload["reason_code"],
                "existing_pr_head_not_ancestor",
            )

    def test_existing_pr_resolver_rejects_ambiguous_fork_and_identity_matrix(self) -> None:
        def candidate(number: int = 59) -> dict:
            return {
                "number": number,
                "url": f"https://github.com/castbox/guru-trellis/pull/{number}",
                "title": "current",
                "body": "Closes #208",
                "headRefName": "feat/208",
                "baseRefName": "main",
                "headRefOid": "a" * 40,
                "isDraft": False,
                "headRepository": {"nameWithOwner": "castbox/guru-trellis"},
                "headRepositoryOwner": {"login": "castbox"},
                "isCrossRepository": False,
            }

        cases = {
            "multiple_open_prs": (
                [candidate(), candidate(60)],
                "zero or one exact open pull request",
            ),
            "fork": (
                [{
                    **candidate(),
                    "headRepository": {"nameWithOwner": "contributor/guru-trellis"},
                    "headRepositoryOwner": {"login": "contributor"},
                    "isCrossRepository": True,
                }],
                "cross-repository pull request candidates",
            ),
            "head_mismatch": (
                [{**candidate(), "headRefName": "feat/other"}],
                "repo/head/base identity is invalid",
            ),
            "base_mismatch": (
                [{**candidate(), "baseRefName": "release"}],
                "repo/head/base identity is invalid",
            ),
            "repository_fields_mismatch": (
                [{
                    **candidate(),
                    "headRepository": {"nameWithOwner": "other/guru-trellis"},
                }],
                "head repository fields are inconsistent",
            ),
        }
        for name, (values, message) in cases.items():
            with self.subTest(name=name), mock.patch.object(
                GTT,
                "validate_github_remote_repository",
                return_value="castbox/guru-trellis",
            ), mock.patch.object(GTT, "gh_json", return_value=values) as gh:
                with self.assertRaisesRegex(GTT.WorkflowError, message):
                    GTT.resolve_closeout_pull_request(
                        Path("/repo"),
                        "castbox/guru-trellis",
                        "feat/208",
                        "main",
                    )
                gh.assert_called_once()

    def test_stale_publication_blocks_before_recovery_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            task_dir = root / ".trellis/tasks/repair-ready-task"
            task_dir.mkdir(parents=True)
            (task_dir / "task.json").write_text(
                json.dumps({"status": "completed"}) + "\n",
                encoding="utf-8",
            )
            result = GTT.finalization_publication_owner_result(
                root,
                task_dir,
                {
                    "profile": "publication_ready",
                    "task_ref": ".trellis/tasks/repair-ready-task",
                    "branch_review_commit": "b" * 40,
                },
            )
        self.assertEqual(
            result,
            {
                "owner_status": "stale",
                "branch_review_commit": "b" * 40,
                "stale_reason": "publication_review_stale",
            },
        )

    def test_plan_backed_reprepare_remains_bound_to_plan_commit(self) -> None:
        task_ref = ".trellis/tasks/08-17-253-plan-backed"
        plan_commit = "c" * 40
        publication_head = "d" * 40
        context = {
            "plan": {
                "git": {
                    "branch_review_commit": plan_commit,
                    "publication_head": publication_head,
                }
            },
            "plan_ref": "finalization:" + "e" * 64,
            "transaction_state": "reprepare_required",
            "publication_status": "current",
            "publication_stale_reason": None,
            "publication_branch_review_commit": "f" * 40,
            "reprepare_reason_code": GTT.FINALIZATION_REPREPARE_ARCHIVE_MONTH,
        }
        route = {
            "typed_exit": "reprepare_required",
            "consumer": copy.deepcopy(
                GTT.FINALIZATION_CONSUMERS["reprepare_required"]
            ),
            "output": {
                "exit_id": "reprepare_required",
                "task_ref": task_ref,
                "reason_code": GTT.FINALIZATION_REPREPARE_ARCHIVE_MONTH,
                "branch_review_commit": plan_commit,
                "publication_head": publication_head,
            },
        }
        with mock.patch.object(GTT, "finalization_package_root", return_value=PACKAGE):
            GTT.finalization_validate_route(
                Path("/repo"), {"task_ref": task_ref}, context, route
            )
            invalid = copy.deepcopy(route)
            invalid["output"]["branch_review_commit"] = context[
                "publication_branch_review_commit"
            ]
            with self.assertRaises(GTT.WorkflowError):
                GTT.finalization_validate_route(
                    Path("/repo"), {"task_ref": task_ref}, context, invalid
                )

    def test_archive_conflict_fails_before_finalizer_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive_locator = (
                f".trellis/tasks/archive/{GTT.current_archive_month()}/repair-ready-task"
            )
            (root / archive_locator).mkdir(parents=True)
            with self.assertRaises(GTT.WorkflowError) as raised:
                GTT.assert_closeout_archive_path_preflight(root, archive_locator)
        self.assertEqual(
            raised.exception.payload,
            {
                "stage": "archive-locator-preflight",
                "archive_locator": archive_locator,
            },
        )

    def test_unknown_transaction_state_fails_closed_on_read(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            task_dir = root / ".trellis/tasks/repair-ready-task"
            task_dir.mkdir(parents=True)
            plan = {
                "plan_digest": "d" * 64,
                "task": {"active_locator": ".trellis/tasks/repair-ready-task"},
                "git": {
                    "repo": "castbox/guru-trellis",
                    "base_branch": "main",
                    "head_branch": "feat/208",
                    "branch_review_commit": "b" * 40,
                    "publication_head": "b" * 40,
                },
                "publish": {"title": "current", "body": "Closes #208"},
                }
            transaction = GTT.finalization_transaction_from_plan(
                plan,
                next_transition="bind_pr",
                pr={
                    "number": 59,
                    "url": "https://github.com/castbox/guru-trellis/pull/59",
                },
                mode="existing_pr_recovery",
                adopted_pr={
                    "number": 59,
                    "url": "https://github.com/castbox/guru-trellis/pull/59",
                    "initial_is_draft": False,
                    "pre_push_remote_head": "a" * 40,
                },
            )
            transaction["next_transition"] = "unknown"
            with mock.patch.object(GTT, "finalization_package_root", return_value=PACKAGE):
                path = GTT.finalization_transaction_path(root, task_dir)
                GTT.write_json(path, transaction)
                with self.assertRaisesRegex(
                    GTT.WorkflowError, "transaction is invalid"
                ) as raised:
                    GTT.finalization_read_transaction(root, task_dir)
        self.assertTrue(raised.exception.payload["errors"])

    def test_existing_pr_recovery_rejects_remote_head_drift(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "publish": {"title": "当前标题", "body": "Closes #208"},
        }
        pr = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
            "headRefOid": "a" * 40,
            "isDraft": True,
            "title": "旧标题",
            "body": "Closes #207",
        }
        with self.assertRaises(GTT.WorkflowError) as remote_error:
            GTT.classify_existing_pr_recovery(Path("/repo"), plan, pr, "c" * 40)
        self.assertEqual(remote_error.exception.payload["reason_code"], "existing_pr_remote_head_mismatch")

    def test_fresh_existing_pr_recovery_rejects_unbound_equal_head(self) -> None:
        head = "b" * 40
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": head,
                "publication_head": head,
            },
            "publish": {"title": "current", "body": "Closes #208"},
        }
        pr = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
            "headRefOid": head,
            "isDraft": False,
            "title": "current",
            "body": "Closes #208",
        }
        with self.assertRaises(GTT.WorkflowError) as raised:
            GTT.classify_existing_pr_recovery(Path("/repo"), plan, pr, head)
        self.assertEqual(
            raised.exception.payload["reason_code"],
            "existing_pr_unbound_equal_head",
        )

    def test_exact_ordinary_transaction_adopts_unbound_equal_head(self) -> None:
        head = "b" * 40
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/338"},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "fix/338",
                "base_branch": "main",
                "branch_review_commit": head,
                "publication_head": head,
            },
            "publish": {
                "title": "修复 Finalizer equal-HEAD 恢复",
                "body": "## 变更摘要\n\nCloses #338",
            },
        }
        transaction = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="push_content",
            pre_push_remote_head="a" * 40,
        )
        pr = {
            "number": 337,
            "url": "https://github.com/castbox/guru-trellis/pull/337",
            "headRefOid": head,
            "isDraft": False,
            "title": plan["publish"]["title"],
            "body": plan["publish"]["body"] + "\n",
        }
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value=head),
        ):
            state, recovery = GTT.finalization_existing_pr_recovery_context(
                Path("/repo"), plan, transaction, "content_pushed"
            )
        self.assertEqual(state, "existing_pr_recovery")
        self.assertEqual(recovery["pr"], {"number": 337, "url": pr["url"]})
        self.assertEqual(recovery["ancestry"], "equal")
        self.assertFalse(recovery["push_required"])
        self.assertTrue(recovery["metadata_update_required"])
        self.assertEqual(recovery["ready_action"], "preserve_ready")
        self.assertEqual(
            recovery["metadata_comparison"],
            {
                "live_title": plan["publish"]["title"],
                "live_body": plan["publish"]["body"] + "\n",
                "title_matches": True,
                "body_matches": False,
            },
        )

    def test_unbound_equal_head_recovery_requires_exact_ordinary_stage(self) -> None:
        head = "b" * 40
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/338"},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "fix/338",
                "base_branch": "main",
                "branch_review_commit": head,
                "publication_head": head,
            },
            "publish": {"title": "current", "body": "Closes #338"},
        }
        ordinary = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="push_content",
            pre_push_remote_head="a" * 40,
        )
        wrong_stage = copy.deepcopy(ordinary)
        wrong_stage["next_transition"] = "bind_pr"
        wrong_stage.pop("pre_push_remote_head")
        with mock.patch.object(GTT, "resolve_closeout_pull_request") as resolve_pr:
            state, recovery = GTT.finalization_existing_pr_recovery_context(
                Path("/repo"), plan, wrong_stage, "content_pushed"
            )
        self.assertEqual(state, "content_pushed")
        self.assertIsNone(recovery)
        resolve_pr.assert_not_called()

        identity_drift = copy.deepcopy(ordinary)
        identity_drift["plan_digest"] = "e" * 64
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request") as drift_resolve,
            self.assertRaisesRegex(
                GTT.WorkflowError,
                "transaction no longer matches",
            ),
        ):
            GTT.finalization_existing_pr_recovery_context(
                Path("/repo"), plan, identity_drift, "content_pushed"
            )
        drift_resolve.assert_not_called()

    def test_unbound_ordinary_recovery_rejects_non_equal_open_pr_without_fallback(self) -> None:
        publication_head = "b" * 40
        remote_head = "a" * 40
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/338"},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "fix/338",
                "base_branch": "main",
                "branch_review_commit": publication_head,
                "publication_head": publication_head,
            },
            "publish": {"title": "current", "body": "Closes #338"},
        }
        transaction = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="push_content",
            pre_push_remote_head=remote_head,
        )
        pr = {
            "number": 337,
            "url": "https://github.com/castbox/guru-trellis/pull/337",
            "headRefOid": remote_head,
            "isDraft": False,
            "title": "current",
            "body": "Closes #338",
        }
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
            mock.patch.object(
                GTT, "closeout_remote_branch_head", return_value=remote_head
            ),
            mock.patch.object(GTT, "finalization_write_transaction") as write,
            self.assertRaises(GTT.WorkflowError) as raised,
        ):
            GTT.classify_unbound_equal_head_recovery(
                Path("/repo"), plan, transaction
            )
        self.assertEqual(
            raised.exception.payload["reason_code"],
            "existing_pr_unbound_equal_head_required",
        )
        write.assert_not_called()

    def test_unbound_ordinary_recovery_does_not_consult_terminal_prs(self) -> None:
        head = "b" * 40
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/338"},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "fix/338",
                "base_branch": "main",
                "branch_review_commit": head,
                "publication_head": head,
            },
            "publish": {"title": "current", "body": "Closes #338"},
        }
        transaction = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="push_content",
            pre_push_remote_head="a" * 40,
        )
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=None),
            mock.patch.object(
                GTT,
                "resolve_closeout_terminal_pull_requests",
            ) as terminal_prs,
        ):
            recovery = GTT.classify_unbound_equal_head_recovery(
                Path("/repo"),
                plan,
                transaction,
            )
        self.assertIsNone(recovery)
        terminal_prs.assert_not_called()

    def test_transaction_bound_resume_ignores_historical_terminal_and_keeps_remote_guard(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            sandbox = Path(raw)
            root = sandbox / "business"
            root.mkdir()
            remote = sandbox / "business.git"
            subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
            for command in (
                ["git", "init", "-q", "-b", "main"],
                ["git", "config", "user.name", "Guru Test"],
                ["git", "config", "user.email", "guru@example.invalid"],
                ["git", "remote", "add", "origin", str(remote)],
            ):
                GTT.run_stdout(command, cwd=root)

            (root / "history.txt").write_text("generation 1\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "history.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-qm", "generation 1"], cwd=root)
            historical_head = GTT.current_head(root)
            branch = "fix/454-reactivated"
            GTT.run_stdout(["git", "switch", "-qc", branch], cwd=root)
            GTT.run_stdout(["git", "push", "-qu", "origin", branch], cwd=root)

            (root / "history.txt").write_text(
                "generation 2 review\n", encoding="utf-8"
            )
            GTT.run_stdout(["git", "add", "history.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-qm", "generation 2 review"], cwd=root)
            branch_review_head = GTT.current_head(root)
            GTT.run_stdout(
                [
                    "git",
                    "push",
                    "-q",
                    "origin",
                    f"{branch_review_head}:refs/tags/review-snapshot",
                ],
                cwd=root,
            )

            (root / "history.txt").write_text(
                "generation 2 publication\n", encoding="utf-8"
            )
            GTT.run_stdout(["git", "add", "history.txt"], cwd=root)
            GTT.run_stdout(
                ["git", "commit", "-qm", "generation 2 publication"], cwd=root
            )
            publication_head = GTT.current_head(root)
            self.assertTrue(
                GTT.is_ancestor(root, historical_head, branch_review_head)
            )
            self.assertTrue(
                GTT.is_ancestor(root, branch_review_head, publication_head)
            )

            plan = {
                "plan_digest": "d" * 64,
                "task": {"active_locator": ".trellis/tasks/454"},
                "git": {
                    "repo": "castbox/guru-trellis",
                    "remote": "origin",
                    "head_branch": branch,
                    "base_branch": "main",
                    "branch_review_commit": branch_review_head,
                    "publication_head": publication_head,
                },
                "publish": {"title": "generation 2", "body": "Closes #454"},
            }
            transaction = GTT.finalization_transaction_from_plan(
                plan,
                next_transition="push_content",
                pre_push_remote_head=historical_head,
            )
            historical_terminal = [
                {
                    "number": 453,
                    "url": "https://github.com/castbox/guru-trellis/pull/453",
                    "state": "MERGED",
                    "headRefOid": historical_head,
                }
            ]
            with (
                mock.patch.object(
                    GTT, "resolve_closeout_pull_request", return_value=None
                ),
                mock.patch.object(
                    GTT,
                    "resolve_closeout_terminal_pull_requests",
                    return_value=historical_terminal,
                ) as terminal_prs,
            ):
                state, recovery = GTT.finalization_existing_pr_recovery_context(
                    root,
                    plan,
                    transaction,
                    "prepared",
                )
                self.assertEqual(
                    GTT.finalization_pre_mutation_remote_preflight(
                        root, plan, transaction
                    ),
                    (None, historical_head),
                )
            self.assertEqual(state, "prepared")
            self.assertIsNone(recovery)
            terminal_prs.assert_not_called()

            GTT.run_stdout(
                [
                    "git",
                    f"--git-dir={remote}",
                    "update-ref",
                    f"refs/heads/{branch}",
                    branch_review_head,
                ],
                cwd=sandbox,
            )
            with (
                mock.patch.object(
                    GTT, "resolve_closeout_pull_request", return_value=None
                ),
                self.assertRaises(GTT.WorkflowError) as raised,
            ):
                GTT.finalization_pre_mutation_remote_preflight(
                    root, plan, transaction
                )
            self.assertEqual(
                raised.exception.payload,
                {
                    "reason_code": "finalizer_remote_head_drift",
                    "remote_head": branch_review_head,
                    "allowed_heads": sorted([historical_head, publication_head]),
                },
            )

            GTT.run_stdout(
                [
                    "git",
                    "push",
                    "-q",
                    "origin",
                    f"{publication_head}:refs/heads/{branch}",
                ],
                cwd=root,
            )
            with (
                mock.patch.object(
                    GTT, "resolve_closeout_pull_request", return_value=None
                ),
            ):
                self.assertEqual(
                    GTT.finalization_pre_mutation_remote_preflight(
                        root, plan, transaction
                    ),
                    (None, publication_head),
                )

            (root / "history.txt").write_text("ahead\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "history.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-qm", "remote ahead"], cwd=root)
            ahead_head = GTT.current_head(root)
            GTT.run_stdout(["git", "push", "-q", "origin", branch], cwd=root)
            GTT.run_stdout(
                ["git", "reset", "--hard", "-q", publication_head], cwd=root
            )

            GTT.run_stdout(
                ["git", "switch", "-qc", "diverged", historical_head], cwd=root
            )
            (root / "diverged.txt").write_text("diverged\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "diverged.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-qm", "remote diverged"], cwd=root)
            diverged_head = GTT.current_head(root)
            GTT.run_stdout(
                ["git", "push", "-q", "--force", "origin", f"HEAD:{branch}"],
                cwd=root,
            )
            GTT.run_stdout(["git", "switch", "-q", branch], cwd=root)

            peer = sandbox / "peer"
            GTT.run_stdout(
                ["git", "clone", "-q", "--branch", branch, str(remote), str(peer)],
                cwd=sandbox,
            )
            GTT.run_stdout(["git", "config", "user.name", "Guru Peer"], cwd=peer)
            GTT.run_stdout(
                ["git", "config", "user.email", "peer@example.invalid"], cwd=peer
            )
            (peer / "peer.txt").write_text("unknown locally\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "peer.txt"], cwd=peer)
            GTT.run_stdout(["git", "commit", "-qm", "remote unknown"], cwd=peer)
            unknown_head = GTT.current_head(peer)
            GTT.run_stdout(["git", "push", "-q", "origin", branch], cwd=peer)
            self.assertNotEqual(
                GTT.run(
                    ["git", "cat-file", "-e", f"{unknown_head}^{{commit}}"],
                    cwd=root,
                    check=False,
                ).returncode,
                0,
            )

            for drift_name, remote_head in (
                ("ahead", ahead_head),
                ("diverged", diverged_head),
                ("unknown", unknown_head),
            ):
                with self.subTest(drift=drift_name):
                    GTT.run_stdout(
                        [
                            "git",
                            f"--git-dir={remote}",
                            "update-ref",
                            f"refs/heads/{branch}",
                            remote_head,
                        ],
                        cwd=sandbox,
                    )
                    with (
                        mock.patch.object(
                            GTT, "resolve_closeout_pull_request", return_value=None
                        ),
                        self.assertRaises(GTT.WorkflowError) as raised,
                    ):
                        GTT.finalization_pre_mutation_remote_preflight(
                            root, plan, transaction
                        )
                    self.assertEqual(
                        raised.exception.payload["reason_code"],
                        "finalizer_remote_head_drift",
                    )
                    self.assertEqual(
                        raised.exception.payload["remote_head"], remote_head
                    )

    def test_base_evolution_fallback_uses_real_merge_topology(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for command in (
                ["git", "init", "-q", "-b", "main"],
                ["git", "config", "user.name", "Guru Test"],
                ["git", "config", "user.email", "guru@example.invalid"],
            ):
                GTT.run_stdout(command, cwd=root)
            (root / "business.txt").write_text("reviewed\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "business.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "base"], cwd=root)
            base_before = GTT.current_head(root)
            GTT.run_stdout(["git", "switch", "-q", "-c", "fix/344"], cwd=root)
            (root / "publication.txt").write_text("published\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "publication.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "publication"], cwd=root)
            old_head = GTT.current_head(root)
            GTT.run_stdout(["git", "switch", "-q", "main"], cwd=root)
            (root / "base-1.txt").write_text("one\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "base-1.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "base one"], cwd=root)
            (root / "base-2.txt").write_text("two\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "base-2.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "base two"], cwd=root)
            base_after = GTT.current_head(root)
            GTT.run_stdout(["git", "switch", "-q", "fix/344"], cwd=root)
            GTT.run_stdout(
                ["git", "merge", "--no-ff", "-q", "main", "-m", "merge base"],
                cwd=root,
            )
            current_head = GTT.current_head(root)
            plan = {
                "task": {"active_locator": ".trellis/tasks/344"},
                "git": {
                    "repo": "castbox/guru-trellis",
                    "remote": "origin",
                    "head_branch": "fix/344",
                    "base_branch": "main",
                    "branch_review_commit": current_head,
                    "publication_head": current_head,
                },
                    "publish": {"title": "current", "body": "Closes #344"},
            }
            transaction = {
                "mode": "ordinary_publication",
                "next_transition": "push_content",
                "pr": None,
                "adopted_pr": None,
                "task_ref": ".trellis/tasks/344",
                "repo_ref": "castbox/guru-trellis",
                "base_branch": "main",
                "branch": "fix/344",
                "publication": {"title": "current", "body": "Closes #344"},
                    "branch_review_commit": old_head,
                "publication_head": old_head,
            }
            self.assertTrue(GTT.is_ancestor(root, base_before, old_head))
            self.assertTrue(GTT.is_ancestor(root, base_after, current_head))
            self.assertFalse(GTT.is_ancestor(root, base_after, old_head))
            pr = {
                "number": 337,
                "url": "https://github.com/castbox/guru-trellis/pull/337",
                "headRefOid": old_head,
                "isDraft": False,
                "title": "current",
                "body": "Closes #344",
            }
            with (
                mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
                mock.patch.object(GTT, "closeout_remote_branch_head", return_value=old_head),
            ):
                recovery = GTT.classify_provenance_tail_transaction_rebind(
                    root, plan, transaction
                )
            self.assertEqual(recovery["ancestry"], "strict_ancestor")
            self.assertTrue(recovery["push_required"])
            self.assertEqual(recovery["pre_push_remote_head"], old_head)
            self.assertEqual(recovery["publication_head"], current_head)

            publication_drift = copy.deepcopy(plan)
            publication_drift["publish"] = {
                "title": "fresh reviewed title",
                "body": "Closes #344\n\nFresh Publication review evidence.",
            }
            with (
                mock.patch.object(GTT, "resolve_closeout_pull_request") as resolve_pr,
                self.assertRaises(GTT.WorkflowError) as publication_error,
            ):
                GTT.classify_provenance_tail_transaction_rebind(
                    root, publication_drift, transaction
                )
            self.assertEqual(
                publication_error.exception.payload["reason_code"],
                "provenance_tail_transaction_rebind_invalid",
            )
            self.assertIn(
                "publication", publication_error.exception.payload["errors"]
            )
            resolve_pr.assert_not_called()

            (root / "business-after-merge.txt").write_text("drift\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "business-after-merge.txt"], cwd=root)
            GTT.run_stdout(
                ["git", "commit", "-q", "-m", "business drift"], cwd=root
            )
            with mock.patch.object(
                GTT, "resolve_closeout_pull_request"
            ) as resolve_pr, self.assertRaises(GTT.WorkflowError) as drift_error:
                GTT.classify_provenance_tail_transaction_rebind(
                    root, plan, transaction
                )
            self.assertEqual(
                drift_error.exception.payload["reason_code"],
                "provenance_tail_transaction_rebind_invalid",
            )
            self.assertIn(
                "provenance_tail_publication_head_not_current",
                drift_error.exception.payload["errors"],
            )
            resolve_pr.assert_not_called()

    def test_fresh_reviewed_descendant_rebind_uses_current_reviewed_head_without_tail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for command in (
                ["git", "init", "-q", "-b", "main"],
                ["git", "config", "user.name", "Guru Test"],
                ["git", "config", "user.email", "guru@example.invalid"],
            ):
                GTT.run_stdout(command, cwd=root)

            (root / "base.txt").write_text("base\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "base.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-qm", "base"], cwd=root)
            base_before = GTT.current_head(root)
            GTT.run_stdout(["git", "switch", "-q", "-c", "fix/358"], cwd=root)

            (root / "publication.txt").write_text("predecessor\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "publication.txt"], cwd=root)
            GTT.run_stdout(
                ["git", "commit", "-qm", "predecessor publication"], cwd=root
            )
            predecessor_head = GTT.current_head(root)

            (root / "remote-task.txt").write_text("remote\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "remote-task.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-qm", "existing PR head"], cwd=root)
            remote_head = GTT.current_head(root)

            GTT.run_stdout(["git", "switch", "-q", "main"], cwd=root)
            (root / "base-evolution.txt").write_text("current base\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "base-evolution.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-qm", "advance base"], cwd=root)
            selected_base_head = GTT.current_head(root)
            GTT.run_stdout(["git", "switch", "-q", "fix/358"], cwd=root)
            GTT.run_stdout(
                ["git", "merge", "--no-ff", "-q", "main", "-m", "merge base"],
                cwd=root,
            )
            (root / "reviewed-source.txt").write_text("current\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "reviewed-source.txt"], cwd=root)
            GTT.run_stdout(
                ["git", "commit", "-qm", "fresh reviewed task content"], cwd=root
            )
            reviewed_head = GTT.current_head(root)

            self.assertTrue(GTT.is_ancestor(root, predecessor_head, reviewed_head))
            self.assertTrue(GTT.is_ancestor(root, remote_head, reviewed_head))
            self.assertTrue(GTT.is_ancestor(root, selected_base_head, reviewed_head))
            self.assertFalse(
                GTT.is_ancestor(root, selected_base_head, predecessor_head)
            )
            self.assertEqual(
                GTT.provenance_tail_transaction_rebind_errors(
                    root,
                    {
                        "task": {"active_locator": ".trellis/tasks/358"},
                        "git": {
                            "repo": "castbox/guru-trellis",
                            "remote": "origin",
                            "head_branch": "fix/358",
                            "base_branch": "main",
                            "branch_review_commit": reviewed_head,
                            "publication_head": reviewed_head,
                        },
                        "publish": {
                            "title": "fresh reviewed title",
                            "body": "Closes #358",
                        },
                    },
                    {
                        "task_ref": ".trellis/tasks/358",
                        "repo_ref": "castbox/guru-trellis",
                        "base_branch": "main",
                        "branch": "fix/358",
                        "publication": {
                            "title": "predecessor title",
                            "body": "Closes #358",
                        },
                        "branch_review_commit": predecessor_head,
                        "publication_head": predecessor_head,
                    },
                ),
                [
                    "provenance_tail_changed_paths_invalid",
                    "provenance_tail_parent_mismatch",
                    "publication",
                ],
            )

            plan = {
                "task": {"active_locator": ".trellis/tasks/358"},
                "git": {
                    "repo": "castbox/guru-trellis",
                    "remote": "origin",
                    "head_branch": "fix/358",
                    "base_branch": "main",
                    "branch_review_commit": reviewed_head,
                    "publication_head": reviewed_head,
                },
                "publish": {
                    "title": "fresh reviewed title",
                    "body": "Closes #358",
                },
            }
            transaction = {
                "mode": "ordinary_publication",
                "next_transition": "push_content",
                "pr": None,
                "adopted_pr": None,
                "task_ref": ".trellis/tasks/358",
                "repo_ref": "castbox/guru-trellis",
                "base_branch": "main",
                "branch": "fix/358",
                "publication": {
                    "title": "predecessor title",
                    "body": "Closes #358",
                },
                "branch_review_commit": predecessor_head,
                "publication_head": predecessor_head,
            }
            pr = {
                "number": 337,
                "url": "https://github.com/castbox/guru-trellis/pull/337",
                "headRefOid": remote_head,
                "isDraft": False,
                "title": "predecessor title",
                "body": "Closes #358",
            }
            with (
                mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
                mock.patch.object(
                    GTT, "closeout_remote_branch_head", return_value=remote_head
                ),
            ):
                recovery = GTT.classify_provenance_tail_transaction_rebind(
                    root, plan, transaction
                )

            self.assertEqual(recovery["mode"], "existing_pr_recovery")
            self.assertEqual(recovery["pr"], {"number": 337, "url": pr["url"]})
            self.assertEqual(recovery["ancestry"], "strict_ancestor")
            self.assertTrue(recovery["push_required"])
            self.assertEqual(recovery["pre_push_remote_head"], remote_head)
            self.assertEqual(recovery["publication_head"], reviewed_head)
            self.assertTrue(recovery["metadata_update_required"])

            sibling_tree = GTT.run_stdout(
                ["git", "rev-parse", f"{remote_head}^{{tree}}"], cwd=root
            )
            sibling_remote = GTT.run_stdout(
                [
                    "git", "commit-tree", sibling_tree,
                    "-p", base_before,
                    "-m", "sibling remote",
                ],
                cwd=root,
            )
            reviewed_tree = GTT.run_stdout(
                ["git", "rev-parse", f"{reviewed_head}^{{tree}}"], cwd=root
            )
            merged_reviewed_head = GTT.run_stdout(
                [
                    "git", "commit-tree", reviewed_tree,
                    "-p", reviewed_head,
                    "-p", sibling_remote,
                    "-m", "reviewed merge",
                ],
                cwd=root,
            )
            GTT.run_stdout(
                ["git", "reset", "--hard", "-q", merged_reviewed_head], cwd=root
            )
            sibling_plan = copy.deepcopy(plan)
            sibling_plan["git"]["branch_review_commit"] = merged_reviewed_head
            sibling_plan["git"]["publication_head"] = merged_reviewed_head
            sibling_pr = {**pr, "headRefOid": sibling_remote}
            with (
                mock.patch.object(
                    GTT, "resolve_closeout_pull_request", return_value=sibling_pr
                ),
                mock.patch.object(
                    GTT, "closeout_remote_branch_head", return_value=sibling_remote
                ),
                self.assertRaises(GTT.WorkflowError) as raised,
            ):
                GTT.classify_provenance_tail_transaction_rebind(
                    root, sibling_plan, transaction
                )
            self.assertEqual(
                raised.exception.payload["reason_code"],
                "provenance_tail_transaction_rebind_remote_head_mismatch",
            )
            GTT.run_stdout(["git", "reset", "--hard", "-q", reviewed_head], cwd=root)

            predecessor_tree = GTT.run_stdout(
                ["git", "rev-parse", f"{predecessor_head}^{{tree}}"], cwd=root
            )
            unrelated_predecessor = GTT.run_stdout(
                ["git", "commit-tree", predecessor_tree, "-m", "unrelated predecessor"],
                cwd=root,
            )

            for label, invalid_plan, invalid_transaction in (
                (
                    "reviewed_publication_mismatch",
                    {
                        **copy.deepcopy(plan),
                        "git": {
                            **plan["git"],
                            "branch_review_commit": remote_head,
                        },
                    },
                    transaction,
                ),
                (
                    "predecessor_not_ancestor",
                    plan,
                    {
                        **copy.deepcopy(transaction),
                        "branch_review_commit": unrelated_predecessor,
                        "publication_head": unrelated_predecessor,
                    },
                ),
            ):
                with self.subTest(label=label), mock.patch.object(
                    GTT, "resolve_closeout_pull_request"
                ) as resolve_pr, self.assertRaises(GTT.WorkflowError) as raised:
                    GTT.classify_provenance_tail_transaction_rebind(
                        root, invalid_plan, invalid_transaction
                    )
                self.assertEqual(
                    raised.exception.payload["reason_code"],
                    "provenance_tail_transaction_rebind_invalid",
                )
                resolve_pr.assert_not_called()

            GTT.run_stdout(["git", "branch", "-f", "main", base_before], cwd=root)
            with mock.patch.object(
                GTT, "resolve_closeout_pull_request"
            ) as resolve_pr, self.assertRaises(GTT.WorkflowError) as raised:
                GTT.classify_provenance_tail_transaction_rebind(
                    root, plan, transaction
                )
            self.assertEqual(
                raised.exception.payload["reason_code"],
                "provenance_tail_transaction_rebind_invalid",
            )
            resolve_pr.assert_not_called()

            GTT.run_stdout(
                ["git", "branch", "-f", "main", selected_base_head], cwd=root
            )
            (root / "unreviewed.txt").write_text("drift\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "unreviewed.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-qm", "unreviewed drift"], cwd=root)
            with mock.patch.object(
                GTT, "resolve_closeout_pull_request"
            ) as resolve_pr, self.assertRaises(GTT.WorkflowError) as raised:
                GTT.classify_provenance_tail_transaction_rebind(
                    root, plan, transaction
                )
            self.assertEqual(
                raised.exception.payload["reason_code"],
                "provenance_tail_transaction_rebind_invalid",
            )
            self.assertIn(
                "provenance_tail_publication_head_not_current",
                raised.exception.payload["errors"],
            )
            resolve_pr.assert_not_called()

    def test_unbound_equal_head_conversion_preserves_plan_identity(self) -> None:
        head = "b" * 40
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/338"},
            "git": {
                "repo": "castbox/guru-trellis",
                "base_branch": "main",
                "head_branch": "fix/338",
                "branch_review_commit": head,
                "publication_head": head,
            },
            "publish": {"title": "current", "body": "Closes #338"},
        }
        ordinary = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="push_content",
            pre_push_remote_head="a" * 40,
        )
        pr = {
            "number": 337,
            "url": "https://github.com/castbox/guru-trellis/pull/337",
        }
        recovery = {
            "mode": "existing_pr_recovery",
            "pr": copy.deepcopy(pr),
            "initial_state": "ready",
            "initial_is_draft": False,
            "pre_push_remote_head": head,
            "publication_head": head,
            "ancestry": "equal",
            "push_required": False,
            "metadata_update_required": True,
            "metadata_comparison": {
                "live_title": "current",
                "live_body": "Closes #338\n",
                "title_matches": True,
                "body_matches": False,
            },
            "ready_action": "preserve_ready",
        }
        converted = GTT.finalization_convert_unbound_equal_head_transaction(
            plan, ordinary, pr, recovery
        )
        self.assertEqual(converted["mode"], "existing_pr_recovery")
        self.assertEqual(converted["next_transition"], "bind_pr")
        self.assertEqual(converted["pr"], pr)
        self.assertEqual(
            converted["adopted_pr"],
            {
                **pr,
                "initial_is_draft": False,
                "pre_push_remote_head": head,
                "metadata_update_required": True,
                "metadata_comparison": recovery["metadata_comparison"],
            },
        )
        for field in (
            "task_ref",
            "repo_ref",
            "base_branch",
            "branch",
            "branch_review_commit",
            "publication_head",
            "plan_digest",
            "publication",
        ):
            self.assertEqual(converted[field], ordinary[field])
        self.assertNotIn("pre_push_remote_head", converted)

    def test_equal_head_bind_resume_requires_original_metadata_decision(self) -> None:
        head = "b" * 40
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/338"},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "base_branch": "main",
                "head_branch": "fix/338",
                "branch_review_commit": head,
                "publication_head": head,
            },
            "publish": {"title": "current", "body": "Closes #338"},
        }
        pr_identity = {
            "number": 337,
            "url": "https://github.com/castbox/guru-trellis/pull/337",
        }
        comparison = {
            "live_title": "current",
            "live_body": "Closes #338\n",
            "title_matches": True,
            "body_matches": False,
        }
        adopted_pr = {
            **pr_identity,
            "initial_is_draft": False,
            "pre_push_remote_head": head,
            "metadata_update_required": True,
            "metadata_comparison": comparison,
        }
        transaction = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="bind_pr",
            pr=pr_identity,
            mode="existing_pr_recovery",
            adopted_pr=adopted_pr,
        )
        live_pr = {
            **pr_identity,
            "headRefName": "fix/338",
            "baseRefName": "main",
            "headRefOid": head,
            "headRepository": {"nameWithOwner": "castbox/guru-trellis"},
            "headRepositoryOwner": {"login": "castbox"},
            "isCrossRepository": False,
            "isDraft": False,
            "title": comparison["live_title"],
            "body": comparison["live_body"],
        }

        def preflight(current_transaction: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
            with (
                mock.patch.object(
                    GTT, "resolve_closeout_pull_request", return_value=live_pr
                ),
                mock.patch.object(
                    GTT, "closeout_remote_branch_head", return_value=head
                ),
            ):
                return GTT.finalization_pre_mutation_remote_preflight(
                    Path("/repo"), plan, current_transaction
                )

        self.assertEqual(preflight(transaction), (live_pr, head))

        for missing_field in (
            "metadata_comparison",
            "metadata_update_required",
        ):
            with self.subTest(missing_field=missing_field):
                missing = copy.deepcopy(transaction)
                missing["adopted_pr"].pop(missing_field)
                with self.assertRaises(GTT.WorkflowError) as missing_error:
                    preflight(missing)
                self.assertEqual(
                    missing_error.exception.payload["reason_code"],
                    "existing_pr_transaction_drift",
                )

        inconsistent = copy.deepcopy(transaction)
        inconsistent["adopted_pr"]["metadata_update_required"] = False
        with self.assertRaises(GTT.WorkflowError) as inconsistent_error:
            preflight(inconsistent)
        self.assertEqual(
            inconsistent_error.exception.payload["reason_code"],
            "existing_pr_transaction_drift",
        )

        live_pr["body"] = plan["publish"]["body"]
        self.assertEqual(preflight(transaction), (live_pr, head))
        with (
            mock.patch.object(
                GTT, "resolve_closeout_pull_request", return_value=live_pr
            ),
            mock.patch.object(GTT, "current_head", return_value=head),
            mock.patch.object(
                GTT, "closeout_task_dir_from_plan", return_value=Path("/repo/task")
            ),
            mock.patch.object(
                GTT, "validate_closeout_pull_request_identity"
            ) as validate_identity,
            mock.patch.object(GTT, "update_pull_request_metadata") as update,
        ):
            rebound = GTT.ensure_closeout_bound_pr(
                Path("/repo"), plan, plan["publish"]["body"], transaction
            )
        self.assertEqual(rebound, live_pr)
        update.assert_not_called()
        validate_identity.assert_called_once()

        live_pr["body"] = "changed before bind\n\nCloses #338"
        with self.assertRaises(GTT.WorkflowError) as drift_error:
            preflight(transaction)
        self.assertEqual(
            drift_error.exception.payload["reason_code"],
            "existing_pr_recovery_drift",
        )

    def test_unbound_equal_head_adoption_writes_once_and_blocks_preview_drift(self) -> None:
        head = "b" * 40
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/338"},
            "git": {
                "repo": "castbox/guru-trellis",
                "base_branch": "main",
                "head_branch": "fix/338",
                "branch_review_commit": head,
                "publication_head": head,
            },
            "publish": {"title": "current", "body": "Closes #338"},
        }
        ordinary = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="push_content",
            pre_push_remote_head="a" * 40,
        )
        recovery = {
            "mode": "existing_pr_recovery",
            "pr": {
                "number": 337,
                "url": "https://github.com/castbox/guru-trellis/pull/337",
            },
            "initial_state": "ready",
            "initial_is_draft": False,
            "pre_push_remote_head": head,
            "publication_head": head,
            "ancestry": "equal",
            "push_required": False,
            "metadata_update_required": True,
            "metadata_comparison": {
                "live_title": "current",
                "live_body": "Closes #338\n",
                "title_matches": True,
                "body_matches": False,
            },
            "ready_action": "preserve_ready",
        }
        with (
            mock.patch.object(
                GTT,
                "classify_unbound_equal_head_recovery",
                return_value=copy.deepcopy(recovery),
            ),
            mock.patch.object(GTT, "finalization_write_transaction") as write,
        ):
            converted = GTT.finalization_adopt_unbound_equal_head_transaction(
                Path("/repo"),
                Path("/repo/.trellis/tasks/338"),
                plan,
                ordinary,
                recovery,
            )
        self.assertEqual(converted["next_transition"], "bind_pr")
        write.assert_called_once_with(
            Path("/repo"),
            Path("/repo/.trellis/tasks/338"),
            converted,
        )

        drifted = copy.deepcopy(recovery)
        drifted["metadata_comparison"]["live_body"] = "different\nCloses #338"
        with (
            mock.patch.object(
                GTT,
                "classify_unbound_equal_head_recovery",
                return_value=drifted,
            ),
            mock.patch.object(GTT, "finalization_write_transaction") as drift_write,
            self.assertRaises(GTT.WorkflowError) as raised,
        ):
            GTT.finalization_adopt_unbound_equal_head_transaction(
                Path("/repo"),
                Path("/repo/.trellis/tasks/338"),
                plan,
                ordinary,
                recovery,
            )
        self.assertEqual(
            raised.exception.payload["reason_code"],
            "existing_pr_recovery_drift",
        )
        drift_write.assert_not_called()

    def test_reprepare_state_precedes_existing_pr_recovery(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
            }
        }
        transaction = {"mode": "existing_pr_recovery"}
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request") as resolve_pr,
            mock.patch.object(GTT, "finalization_pre_mutation_remote_preflight") as preflight,
        ):
            state, recovery = GTT.finalization_existing_pr_recovery_context(
                Path("/repo"), plan, transaction, "reprepare_required"
            )
        self.assertEqual(state, "reprepare_required")
        self.assertIsNone(recovery)
        resolve_pr.assert_not_called()
        preflight.assert_not_called()

    def test_transaction_recovery_binding_survives_each_transition(self) -> None:
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/208"},
            "git": {
                "repo": "castbox/guru-trellis",
                "base_branch": "main",
                "head_branch": "feat/208",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "publish": {"title": "当前标题", "body": "Closes #208"},
        }
        pr = {"number": 59, "url": "https://github.com/castbox/guru-trellis/pull/59"}
        adopted = {
            **pr,
            "initial_is_draft": False,
            "pre_push_remote_head": "a" * 40,
        }
        transaction = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="push_content",
            pr=pr,
            pre_push_remote_head="a" * 40,
            mode="existing_pr_recovery",
            adopted_pr=adopted,
        )
        jsonschema.Draft202012Validator(
            load("schemas/finalization-transaction.schema.json")
        ).validate(transaction)
        advanced = GTT.finalization_advance_transaction(
            plan, transaction, next_transition="bind_pr"
        )
        self.assertEqual(advanced["mode"], "existing_pr_recovery")
        self.assertEqual(advanced["adopted_pr"], adopted)
        self.assertEqual(advanced["pr"], pr)
        self.assertNotIn("pre_push_remote_head", advanced)

        equal_adopted = {
            **pr,
            "initial_is_draft": False,
            "pre_push_remote_head": "b" * 40,
            "metadata_update_required": True,
            "metadata_comparison": {
                "live_title": "当前标题",
                "live_body": "Closes #208\n",
                "title_matches": True,
                "body_matches": False,
            },
        }
        equal_transaction = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="bind_pr",
            pr=pr,
            mode="existing_pr_recovery",
            adopted_pr=equal_adopted,
        )
        jsonschema.Draft202012Validator(
            load("schemas/finalization-transaction.schema.json")
        ).validate(equal_transaction)
        equal_advanced = GTT.finalization_advance_transaction(
            plan, equal_transaction, next_transition="archive"
        )
        self.assertEqual(equal_advanced["adopted_pr"], equal_adopted)

    def test_transaction_schema_keeps_publication_modes_mutually_exclusive(self) -> None:
        schema = jsonschema.Draft202012Validator(
            load("schemas/finalization-transaction.schema.json")
        )
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/208"},
            "git": {
                "repo": "castbox/guru-trellis",
                "base_branch": "main",
                "head_branch": "feat/208",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "publish": {"title": "current", "body": "Closes #208"},
        }
        ordinary = GTT.finalization_transaction_from_plan(
            plan, next_transition="push_content", pre_push_remote_head=""
        )
        recovery = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="bind_pr",
            pr={"number": 59, "url": "https://github.com/castbox/guru-trellis/pull/59"},
            mode="existing_pr_recovery",
            adopted_pr={
                "number": 59,
                "url": "https://github.com/castbox/guru-trellis/pull/59",
                "initial_is_draft": False,
                "pre_push_remote_head": "a" * 40,
            },
        )
        schema.validate(ordinary)
        schema.validate(recovery)
        ordinary["adopted_pr"] = copy.deepcopy(recovery["adopted_pr"])
        recovery.pop("adopted_pr")
        self.assertFalse(schema.is_valid(ordinary))
        self.assertFalse(schema.is_valid(recovery))

    def test_ordinary_preflight_still_rejects_an_open_pr(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            }
        }
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value={"number": 59}),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="a" * 40),
            mock.patch.object(GTT, "is_ancestor", return_value=True),
            self.assertRaises(GTT.WorkflowError) as raised,
        ):
            GTT.finalization_pre_mutation_remote_preflight(Path("/repo"), plan, None)
        self.assertEqual(raised.exception.payload["reason_code"], "pre_finalizer_remote_state_exists")

    def test_ordinary_preflight_rejects_remote_left_by_terminal_pr(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            }
        }
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=None),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="b" * 40),
            self.assertRaises(GTT.WorkflowError) as raised,
        ):
            GTT.finalization_pre_mutation_remote_preflight(Path("/repo"), plan, None)
        self.assertEqual(
            raised.exception.payload["reason_code"],
            "pre_finalizer_remote_state_exists",
        )

    def test_ordinary_preflight_rejects_terminal_exact_pr_before_push(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            }
        }
        terminal = [{"number": 59, "url": "https://github.com/castbox/guru-trellis/pull/59", "state": "MERGED"}]
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=None),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="a" * 40),
            mock.patch.object(GTT, "is_ancestor", return_value=True),
            mock.patch.object(
                GTT, "resolve_closeout_terminal_pull_requests", return_value=terminal
            ),
            self.assertRaises(GTT.WorkflowError) as raised,
        ):
            GTT.finalization_pre_mutation_remote_preflight(Path("/repo"), plan, None)
        self.assertEqual(
            raised.exception.payload["reason_code"],
            "pre_finalizer_terminal_pr_exists",
        )
        self.assertEqual(raised.exception.payload["pull_requests"], terminal)

    def test_terminal_pr_discovery_binds_same_repository_and_state(self) -> None:
        values = [
            {
                "number": 59,
                "url": "https://github.com/castbox/guru-trellis/pull/59",
                "state": "CLOSED",
                "headRefName": "feat/208",
                "baseRefName": "main",
                "headRepository": {"nameWithOwner": "castbox/guru-trellis"},
                "headRepositoryOwner": {"login": "castbox"},
                "isCrossRepository": False,
            }
        ]
        with (
            mock.patch.object(
                GTT,
                "validate_github_remote_repository",
                return_value="castbox/guru-trellis",
            ),
            mock.patch.object(GTT, "gh_json", return_value=values) as gh,
        ):
            result = GTT.resolve_closeout_terminal_pull_requests(
                Path("/repo"),
                "castbox/guru-trellis",
                "feat/208",
                "main",
            )
        self.assertEqual(
            result,
            [{"number": 59, "url": values[0]["url"], "state": "CLOSED"}],
        )
        self.assertIn("closed", gh.call_args.args[0])

    def test_recovery_payload_drift_after_binding_fails_closed(self) -> None:
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/208"},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "publish": {"title": "current", "body": "Closes #208"},
        }
        pr_identity = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
        }
        transaction = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="archive",
            pr=pr_identity,
            mode="existing_pr_recovery",
            adopted_pr={
                **pr_identity,
                "initial_is_draft": False,
                "pre_push_remote_head": "a" * 40,
            },
        )
        live_pr = {
            **pr_identity,
            "headRefOid": "b" * 40,
            "isDraft": False,
            "title": "drifted",
            "body": "Closes #208",
        }
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=live_pr),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="b" * 40),
            mock.patch.object(GTT, "validate_closeout_remote_pull_request_binding"),
            self.assertRaises(GTT.WorkflowError) as raised,
        ):
            GTT.finalization_pre_mutation_remote_preflight(
                Path("/repo"), plan, transaction
            )
        self.assertIn("title differs", str(raised.exception))

    def test_ready_recovery_preserves_ready_pr_without_creation_or_transition(self) -> None:
        pr = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
            "headRefOid": "b" * 40,
            "isDraft": False,
            "title": "当前标题",
            "body": "Closes #208",
        }
        plan = {
            "git": {"repo": "castbox/guru-trellis", "remote": "origin", "head_branch": "feat/208", "base_branch": "main"},
            "publish": {"title": "当前标题", "body": "Closes #208"},
        }
        transaction = {
            "mode": "existing_pr_recovery",
            "pr": {"number": 59, "url": pr["url"]},
            "adopted_pr": {"number": 59, "url": pr["url"], "initial_is_draft": False, "pre_push_remote_head": "a" * 40},
        }
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
            mock.patch.object(GTT, "current_head", return_value="b" * 40),
            mock.patch.object(GTT, "validate_closeout_remote_pull_request_binding"),
            mock.patch.object(GTT, "validate_closeout_pull_request_identity"),
            mock.patch.object(GTT, "closeout_task_dir_from_plan", return_value=Path("/repo/task")),
            mock.patch.object(GTT, "update_pull_request_metadata") as update,
            mock.patch.object(GTT, "ensure_closeout_draft_pr") as create,
        ):
            result = GTT.ensure_closeout_bound_pr(
                Path("/repo"), plan, "Closes #208", transaction
            )
        self.assertEqual(result, pr)
        update.assert_not_called()
        create.assert_not_called()

    def test_draft_recovery_converges_metadata_once_without_pr_creation(self) -> None:
        old_pr = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
            "headRefOid": "b" * 40,
            "isDraft": True,
            "title": "old",
            "body": "Closes #208",
        }
        current_pr = {**old_pr, "title": "current", "body": "Summary\n\nCloses #208"}
        plan = {
            "git": {"repo": "castbox/guru-trellis", "remote": "origin", "head_branch": "feat/208", "base_branch": "main"},
            "publish": {"title": "current", "body": "Summary\n\nCloses #208"},
        }
        transaction = {
            "mode": "existing_pr_recovery",
            "pr": {"number": 59, "url": old_pr["url"]},
            "adopted_pr": {"number": 59, "url": old_pr["url"], "initial_is_draft": True, "pre_push_remote_head": "a" * 40},
        }
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", side_effect=[old_pr, current_pr, current_pr]),
            mock.patch.object(GTT, "current_head", return_value="b" * 40),
            mock.patch.object(GTT, "validate_closeout_remote_pull_request_binding"),
            mock.patch.object(GTT, "validate_closeout_pull_request_identity"),
            mock.patch.object(GTT, "closeout_task_dir_from_plan", return_value=Path("/repo/task")),
            mock.patch.object(GTT, "update_pull_request_metadata") as update,
            mock.patch.object(GTT, "ensure_closeout_draft_pr") as create,
        ):
            first = GTT.ensure_closeout_bound_pr(
                Path("/repo"), plan, plan["publish"]["body"], transaction
            )
            second = GTT.ensure_closeout_bound_pr(
                Path("/repo"), plan, plan["publish"]["body"], transaction
            )
        self.assertEqual(first, current_pr)
        self.assertEqual(second, current_pr)
        update.assert_called_once_with(
            Path("/repo"),
            "castbox/guru-trellis",
            59,
            "current",
            "Summary\n\nCloses #208",
        )
        create.assert_not_called()

    def test_archived_ready_recovery_preserves_ready_state(self) -> None:
        plan = {
            "plan_digest": "d" * 64,
            "git": {"repo": "castbox/guru-trellis", "remote": "origin", "head_branch": "feat/208", "base_branch": "main"},
        }
        pr = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
            "headRefOid": "c" * 40,
            "isDraft": False,
            "title": "current",
            "body": "Closes #208",
        }
        transaction = {
            "mode": "existing_pr_recovery",
            "adopted_pr": {"number": 59, "url": pr["url"], "initial_is_draft": False, "pre_push_remote_head": "b" * 40},
        }
        args = SimpleNamespace(expected_plan_digest="d" * 64, finalization_gate={})
        with (
            mock.patch.object(GTT, "require_gh_auth"),
            mock.patch.object(GTT, "current_head", return_value="c" * 40),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="c" * 40),
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
            mock.patch.object(GTT, "validate_closeout_remote_pull_request_identity") as validate,
            mock.patch.object(GTT, "reconcile_closeout_task_mappings") as reconcile,
            mock.patch.object(GTT, "ensure_closeout_pr_ready", return_value={"status": "ready", "pr": pr}) as ready,
        ):
            result = GTT.resume_archived_closeout(
                Path("/repo"),
                args,
                Path("/repo/archive"),
                committed_plan=plan,
                committed_archive={"commit": "c" * 40, "summary_pr": pr},
                finalization_transaction=transaction,
            )
        self.assertEqual(result["stage"], "ready")
        self.assertFalse(validate.call_args.kwargs["expected_draft"])
        reconcile.assert_called_once_with(Path("/repo"), Path("/repo/archive"), plan)
        ready.assert_called_once()

    def test_archive_month_reprepare_preserves_adopted_pr_transaction(self) -> None:
        plan = {
            "plan_digest": "e" * 64,
            "task": {"active_locator": ".trellis/tasks/208"},
            "git": {
                "repo": "castbox/guru-trellis",
                "base_branch": "main",
                "head_branch": "feat/208",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "publish": {"title": "current", "body": "Closes #208"},
        }
        previous = {
            "mode": "existing_pr_recovery",
            "pr": {
                "number": 59,
                "url": "https://github.com/castbox/guru-trellis/pull/59",
            },
            "adopted_pr": {
                "number": 59,
                "url": "https://github.com/castbox/guru-trellis/pull/59",
                "initial_is_draft": False,
                "pre_push_remote_head": "a" * 40,
            },
        }
        replacement = GTT.finalization_reprepared_transaction(
            plan,
            previous,
            pre_push_remote_head="a" * 40,
        )
        self.assertEqual(replacement["mode"], "existing_pr_recovery")
        self.assertEqual(replacement["pr"], previous["pr"])
        self.assertEqual(replacement["adopted_pr"], previous["adopted_pr"])
        self.assertEqual(replacement["next_transition"], "push_content")
        self.assertEqual(replacement["pre_push_remote_head"], "a" * 40)

    def test_content_push_uses_exact_publication_refspec(self) -> None:
        plan = {
            "plan_digest": "d" * 64,
            "git": {"remote": "origin", "head_branch": "feat/208", "branch_review_commit": "b" * 40, "publication_head": "b" * 40, "repo": "castbox/guru-trellis", "base_branch": "main"},
        }
        prepared = {"plan": plan, "task": {}}
        with (
            mock.patch.object(GTT, "validate_closeout_reviewed_content"),
            mock.patch.object(GTT, "current_head", return_value="b" * 40),
            mock.patch.object(GTT, "run_stdout") as run_stdout,
            mock.patch.object(GTT, "validate_publish_identity_and_remote_head"),
        ):
            GTT.execute_closeout_content_push(
                Path("/repo"), Path("/repo/task"), {}, prepared
            )
        self.assertEqual(
            run_stdout.call_args.args[0],
            ["git", "push", "-u", "origin", f"{'b' * 40}:refs/heads/feat/208"],
        )

    def test_archived_archive_stage_is_pending_ready_recovery(self) -> None:
        temp_root = tempfile.mkdtemp(prefix="finalizer-archived-recovery-")
        root = Path(temp_root)
        task_dir = root / ".trellis/tasks/archive/251"
        task_dir.mkdir(parents=True)
        task_ref = ".trellis/tasks/251"
        transaction = {
            "task_ref": task_ref,
            "next_transition": "archive",
            "repo_ref": "castbox/guru-trellis",
            "base_branch": "main",
            "branch": "fix/251",
            "remote": "origin",
            "branch_review_commit": "a" * 40,
            "publication_head": "b" * 40,
            "plan_digest": "c" * 64,
            "publication": {"title": "title", "body": "body"},
            "mode": "existing_pr_recovery",
            "pr": {"number": 59, "url": "https://github.com/castbox/guru-trellis/pull/59"},
            "adopted_pr": {"initial_is_draft": True},
        }
        pr = {
            "number": 59,
            "url": transaction["pr"]["url"],
            "isDraft": True,
            "headRefOid": "d" * 40,
        }
        summary = {
            "task": {"artifact_dir": task_ref, "archive_dir": ".trellis/tasks/archive/251"},
            "github": {"pr_url": pr["url"]},
            "index": {"search_terms": {"pr_refs": ["PR #59"]}},
        }
        (task_dir / GTT.FINISH_SUMMARY_ARTIFACT).write_text("{}\n", encoding="utf-8")
        with (
            mock.patch.object(GTT, "repo_relative", return_value=".trellis/tasks/archive/251"),
            mock.patch.object(GTT, "task_json", return_value={"status": "completed"}),
            mock.patch.object(GTT, "publish_config", return_value={"remote": "origin"}),
            mock.patch.object(GTT, "load_config", return_value={}),
            mock.patch.object(GTT, "validate_github_remote_repository", return_value="castbox/guru-trellis"),
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
            mock.patch.object(GTT, "canonical_pull_request_url", return_value=pr["url"]),
            mock.patch.object(GTT, "current_head", return_value="d" * 40),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="d" * 40),
            mock.patch.object(GTT, "read_json", return_value=summary),
            mock.patch.object(GTT, "validate_finish_summary"),
        ):
            context = GTT.finalization_current_archived_context(
                root,
                task_dir,
                {"task_ref": task_ref},
                transaction,
            )
        self.assertEqual(context["transaction_state"], "archived")
        self.assertFalse(context["published_transition_complete"])
        self.assertIsNone(context["published_pr"])
        self.assertEqual(context["plan"]["git"]["publication_head"], "d" * 40)
        shutil.rmtree(temp_root)

    def test_archived_archive_stage_preserves_ready_pr_recovery(self) -> None:
        temp_root = tempfile.mkdtemp(prefix="finalizer-archived-ready-recovery-")
        root = Path(temp_root)
        task_dir = root / ".trellis/tasks/archive/251"
        task_dir.mkdir(parents=True)
        task_ref = ".trellis/tasks/251"
        transaction = {
            "task_ref": task_ref,
            "next_transition": "archive",
            "repo_ref": "castbox/guru-trellis",
            "base_branch": "main",
            "branch": "fix/251",
            "remote": "origin",
            "branch_review_commit": "a" * 40,
            "publication_head": "b" * 40,
            "plan_digest": "c" * 64,
            "publication": {"title": "title", "body": "body"},
            "mode": "existing_pr_recovery",
            "pr": {"number": 59, "url": "https://github.com/castbox/guru-trellis/pull/59"},
            "adopted_pr": {"initial_is_draft": False},
        }
        pr = {
            "number": 59,
            "url": transaction["pr"]["url"],
            "isDraft": False,
            "headRefOid": "d" * 40,
        }
        summary = {
            "task": {"artifact_dir": task_ref, "archive_dir": ".trellis/tasks/archive/251"},
            "github": {"pr_url": pr["url"]},
            "index": {"search_terms": {"pr_refs": ["PR #59"]}},
        }
        (task_dir / GTT.FINISH_SUMMARY_ARTIFACT).write_text("{}\n", encoding="utf-8")
        with (
            mock.patch.object(GTT, "repo_relative", return_value=".trellis/tasks/archive/251"),
            mock.patch.object(GTT, "task_json", return_value={"status": "completed"}),
            mock.patch.object(GTT, "publish_config", return_value={"remote": "origin"}),
            mock.patch.object(GTT, "load_config", return_value={}),
            mock.patch.object(GTT, "validate_github_remote_repository", return_value="castbox/guru-trellis"),
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
            mock.patch.object(GTT, "canonical_pull_request_url", return_value=pr["url"]),
            mock.patch.object(GTT, "current_head", return_value="d" * 40),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="d" * 40),
            mock.patch.object(GTT, "read_json", return_value=summary),
            mock.patch.object(GTT, "validate_finish_summary"),
        ):
            context = GTT.finalization_current_archived_context(
                root, task_dir, {"task_ref": task_ref}, transaction
            )
        self.assertEqual(context["transaction_state"], "archived")
        self.assertFalse(context["published_transition_complete"])
        shutil.rmtree(temp_root)


if __name__ == "__main__":
    unittest.main()
