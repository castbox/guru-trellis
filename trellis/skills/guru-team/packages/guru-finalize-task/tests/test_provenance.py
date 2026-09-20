from __future__ import annotations

from support import *  # noqa: F403


class FinalizeTaskProvenanceTests(unittest.TestCase):
    def test_initial_installed_preview_accepts_immutable_provenance_without_tail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize_provenance_git_repo(root, "castbox/business-repo")
            task_ref = ".trellis/tasks/08-26-initial-installed-publication"
            task_dir = root / task_ref
            task_dir.mkdir(parents=True)
            (task_dir / "task.json").write_text(
                json.dumps({"status": "in_progress"}) + "\n",
                encoding="utf-8",
            )
            manifest_path = root / GTT.PROVENANCE_TAIL_MANIFEST_PATH
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(
                json.dumps(
                    provenance_manifest("castbox/guru-trellis", "b" * 40),
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            reviewed = commit_provenance_fixture(root, "reviewed business task")
            plan = {
                "plan_digest": "c" * 64,
                "git": {
                    "repo": "castbox/business-repo",
                    "remote": "origin",
                    "base_branch": "main",
                    "head_branch": "fix/311-installed-preview",
                    "branch_review_commit": reviewed,
                    "publication_head": reviewed,
                },
                "publish": {
                    "title": "fix: installed preview provenance",
                    "body": "Closes #311",
                },
                "task": {"active_locator": task_ref},
            }
            prepared = {
                "plan": plan,
                "plan_digest": plan["plan_digest"],
                "task": {"status": "in_progress"},
                "task_context": {},
                "body": plan["publish"]["body"],
                "month_supersession": None,
                "pre_pr_reprepare": None,
                "migration_normalization": None,
                "reviewed_content_head": reviewed,
                "publication_head": reviewed,
                "metadata_tail": None,
            }
            public_input = {
                "profile": "publication_ready",
                "mode": "workflow",
                "task_ref": task_ref,
                "branch_review_commit": reviewed,
                "pr_title": plan["publish"]["title"],
                "pr_body": plan["publish"]["body"],
            }
            publication = {
                "status": "ok",
                "owner_status": "current",
                "typed_exit": "ready",
                "task_ref": task_ref,
                "branch_review_commit": reviewed,
            }
            args = SimpleNamespace(root=str(root))
            no_op = mock.Mock()
            with (
                mock.patch.object(GTT, "load_config", return_value={}),
                mock.patch.object(GTT, "finalization_read_transaction", return_value=None),
                mock.patch.object(GTT, "finalization_publication_owner_result", return_value=publication),
                mock.patch.object(GTT, "load_task_runtime_identity", return_value={}),
                mock.patch.object(GTT, "assert_workspace_boundary", no_op),
                mock.patch.object(GTT, "prepare_closeout", return_value=prepared),
                mock.patch.object(GTT, "review_branch_content_continuity_errors", return_value=[]),
                mock.patch.object(GTT, "closeout_remote_branch_head", return_value="") as remote_head,
                mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=None) as resolve_pr,
                mock.patch.object(GTT, "push_closeout_branch_if_needed") as push_branch,
                mock.patch.object(GTT, "create_pull_request") as create_pr,
                mock.patch.object(GTT, "run_gh_command") as ready_pr,
                mock.patch.object(GTT, "execute_archive_metadata_transaction") as archive_task,
            ):
                context = GTT.finalization_preview_context(root, args, public_input)

            self.assertEqual(context["transaction_state"], "prepared")
            self.assertIsNone(context.get("reprepare_reason_code"))
            self.assertEqual(context["publication_mode"], "ordinary_publication")
            self.assertIsNone(context["existing_pr_recovery"])
            remote_head.assert_called_once_with(root, plan)
            resolve_pr.assert_called_once_with(
                root,
                plan["git"]["repo"],
                plan["git"]["head_branch"],
                plan["git"]["base_branch"],
                plan["git"]["remote"],
            )
            push_branch.assert_not_called()
            create_pr.assert_not_called()
            ready_pr.assert_not_called()
            archive_task.assert_not_called()

    def test_provenance_tail_accepts_only_semantic_spec_managed_hash(self) -> None:
        head = "a" * 40
        target_repo = "castbox/guru-trellis"
        before = provenance_manifest(
            target_repo,
            "c" * 40,
            tree_state="dirty",
            is_mutable_ref=True,
        )
        after = copy.deepcopy(before)
        after["installed_at"] = "after"
        after["source"].update(
            {
                "ref": head,
                "commit": head,
                "tree_state": "clean",
                "is_mutable_ref": False,
            }
        )
        after["install"]["managed_asset_hashes"] = {
            ".trellis/spec/workflow/semantic-retrieval.md": "b" * 64,
        }

        self.assertEqual(
            GTT.provenance_tail_manifest_errors(
                before,
                after,
                head,
                target_repo,
            ),
            [],
        )

        for field, value in (
            ("unexpected_install_field", True),
            ("managed_asset_hashes", {".trellis/spec/workflow/other.md": "c" * 64}),
        ):
            with self.subTest(field=field):
                invalid = json.loads(json.dumps(after))
                if field == "managed_asset_hashes":
                    invalid["install"][field].update(value)
                else:
                    invalid["install"][field] = value
                self.assertIn(
                    "provenance_tail_manifest_fields_outside_allowlist",
                    GTT.provenance_tail_manifest_errors(
                        before,
                        invalid,
                        head,
                        target_repo,
                    ),
                )

    def test_provenance_tail_file_action_transition_is_closed(self) -> None:
        head = "a" * 40
        target_repo = "castbox/guru-trellis"
        before = provenance_manifest(
            target_repo,
            "c" * 40,
            tree_state="dirty",
            is_mutable_ref=True,
        )
        before.update(provenance_file_action_sections("installed"))
        after = copy.deepcopy(before)
        after["installed_at"] = "after"
        after["source"].update(
            {
                "ref": head,
                "commit": head,
                "tree_state": "clean",
                "is_mutable_ref": False,
            }
        )
        for container in GTT.PROVENANCE_TAIL_FILE_ACTION_CONTAINERS:
            section_name, field_name = container.split(".", 1)
            for item in after[section_name][field_name]:
                item["action"] = "unchanged"

        self.assertNotIn(
            "skill_packages.files",
            GTT.PROVENANCE_TAIL_ALLOWED_FIELDS,
        )
        self.assertNotIn("overlays.files", GTT.PROVENANCE_TAIL_ALLOWED_FIELDS)
        self.assertEqual(
            GTT.provenance_tail_manifest_errors(
                before,
                after,
                head,
                target_repo,
            ),
            [],
        )
        for container in GTT.PROVENANCE_TAIL_FILE_ACTION_CONTAINERS:
            self.assertTrue(
                GTT.provenance_tail_safe_file_action_transition(
                    before,
                    after,
                    container,
                )
            )

        def reverse_action(before_value: dict, after_value: dict) -> None:
            before_value["skill_packages"]["files"][0]["action"] = "unchanged"
            after_value["skill_packages"]["files"][0]["action"] = "installed"

        def mutate_after_action(_before_value: dict, after_value: dict) -> None:
            after_value["overlays"]["files"][0]["action"] = "updated_managed"

        def mutate_path(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"][0]["path"] += ".changed"

        def mutate_hash(_before_value: dict, after_value: dict) -> None:
            after_value["overlays"]["files"][0]["sha256"] = "f" * 64

        def mutate_mode(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"][0]["executable"] = True

        def mutate_mode_type(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"][0]["executable"] = 0

        def mutate_source(_before_value: dict, after_value: dict) -> None:
            after_value["overlays"]["files"][0]["source"] += ".changed"

        def mutate_destination(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"][0]["destination"] = "other"

        def mutate_platform(_before_value: dict, after_value: dict) -> None:
            after_value["overlays"]["files"][0]["platform"] = "cursor"

        def add_entry(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"].append(
                copy.deepcopy(after_value["skill_packages"]["files"][0])
            )

        def remove_entry(_before_value: dict, after_value: dict) -> None:
            after_value["overlays"]["files"].pop()

        def reorder_entries(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"].reverse()

        def replace_with_non_object(_before_value: dict, after_value: dict) -> None:
            after_value["overlays"]["files"][0] = "not-an-object"

        def replace_with_non_list(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"] = "not-a-list"

        cases = (
            ("unchanged_to_installed", reverse_action),
            ("installed_to_updated_managed", mutate_after_action),
            ("path", mutate_path),
            ("hash", mutate_hash),
            ("mode", mutate_mode),
            ("mode_type", mutate_mode_type),
            ("source", mutate_source),
            ("destination", mutate_destination),
            ("platform", mutate_platform),
            ("entry_added", add_entry),
            ("entry_removed", remove_entry),
            ("entry_reordered", reorder_entries),
            ("non_object_entry", replace_with_non_object),
            ("non_list_container", replace_with_non_list),
        )
        for name, mutate in cases:
            with self.subTest(case=name):
                invalid_before = copy.deepcopy(before)
                invalid_after = copy.deepcopy(after)
                mutate(invalid_before, invalid_after)
                self.assertIn(
                    "provenance_tail_manifest_fields_outside_allowlist",
                    GTT.provenance_tail_manifest_errors(
                        invalid_before,
                        invalid_after,
                        head,
                        target_repo,
                    ),
                )

    def test_provenance_source_binding_is_closed_for_self_hosted_and_installed(self) -> None:
        reviewed = "a" * 40
        source_commit = "b" * 40
        self_hosted = GTT.provenance_source_binding(
            provenance_manifest(
                "castbox/guru-trellis",
                source_commit,
                tree_state="dirty",
                is_mutable_ref=True,
            ),
            "castbox/guru-trellis",
            reviewed,
        )
        self.assertEqual(self_hosted["mode"], "self_hosted")
        self.assertEqual(self_hosted["source_commit"], reviewed)
        self.assertEqual(self_hosted["source_ref"], reviewed)

        installed = GTT.provenance_source_binding(
            provenance_manifest("castbox/guru-trellis", source_commit),
            "castbox/business-repo",
            reviewed,
        )
        self.assertEqual(installed["mode"], "installed")
        self.assertEqual(installed["source_commit"], source_commit)
        self.assertEqual(
            installed["source_locator"],
            "https://github.com/castbox/guru-trellis.git",
        )

        invalid_cases = {
            "missing_repo": lambda payload: payload["source"].pop("repo"),
            "malformed_repo": lambda payload: payload["source"].update(
                {"repo": "ssh://git@example.com/castbox/guru-trellis.git"}
            ),
            "noncanonical_github_locator": lambda payload: payload["source"].update(
                {"repo": "git@github.com:castbox/guru-trellis.git"}
            ),
            "short_commit": lambda payload: payload["source"].update(
                {"ref": "abc123", "commit": "abc123"}
            ),
            "dirty": lambda payload: payload["source"].update(
                {"tree_state": "dirty"}
            ),
            "mutable": lambda payload: payload["source"].update(
                {"is_mutable_ref": True}
            ),
            "ref_commit_mismatch": lambda payload: payload["source"].update(
                {"ref": "c" * 40}
            ),
        }
        for name, mutate in invalid_cases.items():
            with self.subTest(name=name):
                payload = provenance_manifest("castbox/guru-trellis", source_commit)
                mutate(payload)
                binding, errors = GTT.provenance_source_binding_errors(
                    payload,
                    "castbox/business-repo",
                    reviewed,
                )
                self.assertIsNone(binding)
                self.assertTrue(errors)

    def test_provenance_apply_platform_args_preserve_exact_manifest_selection(self) -> None:
        cases = {
            "claude": (["claude"], ["--platform", "claude"]),
            "codex": (["codex"], ["--platform", "codex"]),
            "cursor": (["cursor"], ["--platform", "cursor"]),
            "codex_cursor": (
                ["codex", "cursor"],
                ["--platform", "codex", "--platform", "cursor"],
            ),
            "all_explicit": (
                ["claude", "codex", "cursor"],
                [
                    "--platform",
                    "claude",
                    "--platform",
                    "codex",
                    "--platform",
                    "cursor",
                ],
            ),
            "opencode": (
                ["opencode"],
                ["--platform", "opencode"],
            ),
        }
        for name, (selected, expected) in cases.items():
            with self.subTest(name=name):
                manifest = provenance_manifest(
                    "castbox/guru-trellis",
                    "b" * 40,
                    selected_platforms=selected,
                )
                self.assertEqual(
                    GTT.provenance_apply_platform_args(manifest),
                    expected,
                )

    def test_provenance_apply_platform_args_reject_invalid_manifest_selection(self) -> None:
        cases = {
            "manifest_missing": lambda payload: payload.clear(),
            "install_missing": lambda payload: payload.pop("install"),
            "selected_missing": lambda payload: payload["install"].pop(
                "selected_platforms"
            ),
            "selected_type": lambda payload: payload["install"].update(
                {"selected_platforms": "claude"}
            ),
            "member_type": lambda payload: payload["install"].update(
                {"selected_platforms": ["claude", 1]}
            ),
            "empty": lambda payload: payload["install"].update(
                {"selected_platforms": []}
            ),
            "duplicate": lambda payload: payload["install"].update(
                {"selected_platforms": ["claude", "claude"]}
            ),
            "unsorted": lambda payload: payload["install"].update(
                {"selected_platforms": ["cursor", "codex"]}
            ),
            "unknown": lambda payload: payload["install"].update(
                {"selected_platforms": ["gemini"]}
            ),
            "locator_mismatch": lambda payload: payload["overlays"].update(
                {"selected_platforms": ["codex"]}
            ),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                manifest = provenance_manifest(
                    "castbox/guru-trellis",
                    "b" * 40,
                )
                mutate(manifest)
                with self.assertRaises(GTT.WorkflowError) as raised:
                    GTT.provenance_apply_platform_args(manifest)
                self.assertEqual(
                    raised.exception.payload["reason_code"],
                    "provenance_platform_selection_invalid",
                )

    def test_invalid_provenance_platform_selection_stops_before_source_or_apply(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            initialize_provenance_git_repo(root, "castbox/guru-trellis")
            write_provenance_apply_fixture(root)
            manifest = provenance_manifest(
                "castbox/guru-trellis",
                "b" * 40,
                tree_state="dirty",
                is_mutable_ref=True,
                selected_platforms=["claude"],
            )
            manifest["overlays"]["selected_platforms"] = ["codex"]
            manifest_path = root / GTT.PROVENANCE_TAIL_MANIFEST_PATH
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            reviewed = commit_provenance_fixture(root, "reviewed task")
            parent_bytes = manifest_path.read_bytes()
            observed: list[tuple[list[str], Path | None]] = []
            with (
                mock.patch.object(
                    GTT,
                    "run",
                    side_effect=local_source_fetch_runner(root, observed),
                ),
                mock.patch.object(
                    GTT,
                    "prepare_provenance_extension_source_checkout",
                    wraps=GTT.prepare_provenance_extension_source_checkout,
                ) as prepare_source,
                mock.patch.object(
                    GTT,
                    "commit_provenance_metadata_tail",
                    wraps=GTT.commit_provenance_metadata_tail,
                ) as commit_tail,
            ):
                with self.assertRaises(GTT.WorkflowError) as raised:
                    GTT.prepare_provenance_metadata_tail(
                        root,
                        reviewed,
                        "castbox/guru-trellis",
                    )
            self.assertEqual(
                raised.exception.payload["reason_code"],
                "provenance_platform_selection_invalid",
            )
            prepare_source.assert_not_called()
            commit_tail.assert_not_called()
            self.assertFalse(
                any(
                    len(cmd) > 1
                    and cmd[1].endswith("apply_guru_team_trellis_preset.py")
                    for cmd, _cwd in observed
                )
            )
            self.assertEqual(GTT.current_head(root), reviewed)
            self.assertEqual(manifest_path.read_bytes(), parent_bytes)
            self.assertEqual(GTT.provenance_tail_git_status_paths(root), [])
            self.assertEqual(len(GTT.worktree_records(root)), 1)

    def test_provenance_tail_preparation_preserves_platform_selection_matrix(self) -> None:
        cases = {
            "claude": ["claude"],
            "codex": ["codex"],
            "cursor": ["cursor"],
            "codex_cursor": ["codex", "cursor"],
            "all_explicit": ["claude", "codex", "cursor"],
            "opencode": ["opencode"],
        }
        for name, selected in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                initialize_provenance_git_repo(root, "castbox/guru-trellis")
                write_provenance_apply_fixture(root)
                manifest_path = root / GTT.PROVENANCE_TAIL_MANIFEST_PATH
                manifest_path.parent.mkdir(parents=True)
                manifest_path.write_text(
                    json.dumps(
                        provenance_manifest(
                            "castbox/guru-trellis",
                            "b" * 40,
                            tree_state="dirty",
                            is_mutable_ref=True,
                            selected_platforms=selected,
                        ),
                        ensure_ascii=False,
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                reviewed = commit_provenance_fixture(root, "reviewed task")
                observed: list[tuple[list[str], Path | None]] = []
                with mock.patch.object(
                    GTT,
                    "run",
                    side_effect=local_source_fetch_runner(root, observed),
                ):
                    result = GTT.prepare_provenance_metadata_tail(
                    root,
                    reviewed,
                    "castbox/guru-trellis",
                )

                applied = json.loads(manifest_path.read_text(encoding="utf-8"))
                for locator in ("install", "skill_packages", "overlays"):
                    self.assertEqual(
                        applied[locator]["selected_platforms"],
                        selected,
                    )
                changed_paths = subprocess.run(
                    [
                        "git",
                        "diff-tree",
                        "--no-commit-id",
                        "--name-only",
                        "-r",
                        result["publication_head"],
                    ],
                    cwd=root,
                    check=True,
                    text=True,
                    stdout=subprocess.PIPE,
                ).stdout.splitlines()
                self.assertEqual(
                    changed_paths,
                    [GTT.PROVENANCE_TAIL_MANIFEST_PATH],
                )
                apply_calls = [
                    cmd
                    for cmd, _cwd in observed
                    if len(cmd) > 1
                    and cmd[1].endswith("apply_guru_team_trellis_preset.py")
                ]
                self.assertEqual(apply_calls, [])
                self.assertEqual(len(GTT.worktree_records(root)), 1)

    def test_provenance_tail_preparation_separates_self_hosted_source_and_target(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            initialize_provenance_git_repo(root, "castbox/guru-trellis")
            write_provenance_apply_fixture(root)
            manifest_path = root / GTT.PROVENANCE_TAIL_MANIFEST_PATH
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(
                json.dumps(
                    provenance_manifest(
                        "castbox/guru-trellis",
                        "b" * 40,
                        tree_state="dirty",
                        is_mutable_ref=True,
                    ),
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            parent_bytes = manifest_path.read_bytes()
            commit_provenance_fixture(root, "preset installed")
            (root / "task.txt").write_text("reviewed\n", encoding="utf-8")
            reviewed = commit_provenance_fixture(root, "reviewed task")
            plan = {
                "git": {
                    "branch_review_commit": reviewed,
                    "repo": "castbox/guru-trellis",
                }
            }
            self.assertTrue(
                GTT.finalizer_pre_pr_provenance_tail_required(root, plan)
            )

            observed: list[tuple[list[str], Path | None]] = []
            with mock.patch.object(
                GTT,
                "run",
                side_effect=local_source_fetch_runner(root, observed),
            ):
                result = GTT.prepare_provenance_metadata_tail(
                    root,
                    reviewed,
                    "castbox/guru-trellis",
                )

            self.assertEqual(result["reviewed_content_head"], reviewed)
            self.assertNotEqual(result["publication_head"], reviewed)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            parent = json.loads(parent_bytes.decode("utf-8"))
            self.assertEqual(manifest["source"]["ref"], reviewed)
            self.assertEqual(manifest["source"]["commit"], reviewed)
            self.assertEqual(manifest["installed_at"], parent["installed_at"])
            self.assertEqual(manifest["install"], parent["install"])
            self.assertEqual(manifest["skill_packages"], parent["skill_packages"])
            self.assertEqual(manifest["overlays"], parent["overlays"])
            self.assertFalse(
                GTT.finalizer_pre_pr_provenance_tail_required(root, plan)
            )
            apply_calls = [
                (cmd, cwd)
                for cmd, cwd in observed
                if len(cmd) > 1
                and cmd[1].endswith("apply_guru_team_trellis_preset.py")
            ]
            self.assertEqual(apply_calls, [])
            self.assertEqual(len(GTT.worktree_records(root)), 1)

    def test_initial_provenance_reprepare_accepts_absent_remote_only(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            task_dir = root / ".trellis/tasks/08-27-provenance-reprepare"
            task_dir.mkdir(parents=True)
            reviewed = "a" * 40
            plan = {
                "git": {
                    "reviewed_content_head": reviewed,
                    "branch_review_commit": reviewed,
                    "head_branch": "fix/311-provenance-reprepare",
                    "base_branch": "main",
                    "remote": "origin",
                    "repo": "castbox/business-repo",
                },
                "task": {
                    "active_locator": task_dir.relative_to(root).as_posix(),
                    "archive_locator": (
                        ".trellis/tasks/archive/2026-08/08-27-provenance-reprepare"
                    ),
                },
            }
            worktrees = [
                {
                    "branch": "refs/heads/fix/311-provenance-reprepare",
                    "worktree": str(root),
                }
            ]
            with (
                mock.patch.object(GTT, "current_head", return_value=reviewed),
                mock.patch.object(GTT, "worktree_records", return_value=worktrees),
                mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=None),
                mock.patch.object(GTT, "closeout_remote_branch_head", return_value=""),
            ):
                facts = GTT.finalizer_pre_pr_provenance_reprepare_preflight(
                    root,
                    task_dir,
                    plan,
                )
            self.assertEqual(facts["remote_head"], "")
            self.assertEqual(facts["reviewed_content_head"], reviewed)

            with (
                mock.patch.object(GTT, "current_head", return_value=reviewed),
                mock.patch.object(GTT, "worktree_records", return_value=worktrees),
                mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=None),
                mock.patch.object(
                    GTT, "closeout_remote_branch_head", return_value="b" * 40
                ),
                mock.patch.object(GTT, "is_ancestor", return_value=False),
                self.assertRaises(GTT.WorkflowError) as caught,
            ):
                GTT.finalizer_pre_pr_provenance_reprepare_preflight(
                    root,
                    task_dir,
                    plan,
                )
            self.assertEqual(
                caught.exception.payload["reason_code"],
                "provenance_reprepare_remote_not_reviewed_head",
            )

    def test_installed_provenance_with_immutable_source_needs_no_tail(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            sandbox = Path(raw)
            source_repo = sandbox / "source"
            source_repo.mkdir()
            initialize_provenance_git_repo(source_repo, "castbox/guru-trellis")
            write_provenance_apply_fixture(source_repo)
            source_head = commit_provenance_fixture(source_repo, "source preset")

            target = sandbox / "business"
            target.mkdir()
            initialize_provenance_git_repo(target, "castbox/business-repo")
            manifest_path = target / GTT.PROVENANCE_TAIL_MANIFEST_PATH
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(
                json.dumps(
                    provenance_manifest("castbox/guru-trellis", source_head),
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (target / "business.txt").write_text("reviewed\n", encoding="utf-8")
            reviewed = commit_provenance_fixture(target, "reviewed business task")
            self.assertFalse(
                (
                    target
                    / "trellis/presets/guru-team/scripts/python/"
                    "apply_guru_team_trellis_preset.py"
                ).exists()
            )
            plan = {
                "git": {
                    "branch_review_commit": reviewed,
                    "repo": "castbox/business-repo",
                }
            }
            self.assertFalse(
                GTT.finalizer_pre_pr_provenance_tail_required(target, plan)
            )

            before = manifest_path.read_bytes()
            self.assertEqual(GTT.current_head(target), reviewed)
            self.assertEqual(GTT.provenance_tail_git_status_paths(target), [])
            self.assertEqual(manifest_path.read_bytes(), before)

    def test_installed_source_fetch_must_resolve_the_manifest_oid(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            sandbox = Path(raw)
            source_repo = sandbox / "source"
            source_repo.mkdir()
            initialize_provenance_git_repo(source_repo, "castbox/guru-trellis")
            write_provenance_apply_fixture(source_repo)
            actual_head = commit_provenance_fixture(source_repo, "source preset")
            expected_head = "d" * 40
            binding = GTT.provenance_source_binding(
                provenance_manifest("castbox/guru-trellis", expected_head),
                "castbox/business-repo",
                "e" * 40,
            )
            original_run = GTT.run

            def fetch_other_oid(cmd, cwd=None, check=True, env=None):
                if cmd[:4] == ["git", "fetch", "--depth=1", "origin"]:
                    cmd = ["git", "fetch", "--depth=1", str(source_repo), actual_head]
                return original_run(cmd, cwd=cwd, check=check, env=env)

            source_checkout = sandbox / "checkout"
            with mock.patch.object(GTT, "run", side_effect=fetch_other_oid):
                with self.assertRaises(GTT.WorkflowError) as raised:
                    GTT.prepare_provenance_extension_source_checkout(
                        source_repo,
                        source_checkout,
                        binding,
                    )
            self.assertEqual(
                raised.exception.payload["reason_code"],
                "provenance_source_fetch_mismatch",
            )

    def test_installed_source_fetch_falls_back_to_head_only_for_not_our_ref(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            sandbox = Path(raw)
            source_repo = sandbox / "source"
            source_repo.mkdir()
            initialize_provenance_git_repo(source_repo, "castbox/guru-trellis")
            write_provenance_apply_fixture(source_repo)
            source_head = commit_provenance_fixture(source_repo, "source preset")
            target = sandbox / "business"
            target.mkdir()
            initialize_provenance_git_repo(target, "castbox/business-repo")
            expected = GTT.provenance_source_binding(
                provenance_manifest("castbox/guru-trellis", source_head),
                "castbox/business-repo",
                "e" * 40,
            )
            original_run = GTT.run
            calls: list[list[str]] = []

            def fetch_with_refusal(cmd, cwd=None, check=True, env=None):
                if cmd[:4] == ["git", "fetch", "--depth=1", "origin"]:
                    calls.append(cmd)
                    if cmd[-1] == source_head:
                        return subprocess.CompletedProcess(cmd, 1, "", "fatal: couldn't find remote ref\nnot our ref")
                    cmd = ["git", "fetch", "--depth=1", str(source_repo), source_head]
                return original_run(cmd, cwd=cwd, check=check, env=env)

            checkout = sandbox / "checkout"
            with mock.patch.object(GTT, "run", side_effect=fetch_with_refusal):
                GTT.prepare_provenance_extension_source_checkout(
                    source_repo,
                    checkout,
                    expected,
                )
            self.assertEqual([call[-1] for call in calls], [source_head, "HEAD"])

    def test_provenance_tail_producer_rejects_manifest_boundary_drift(self) -> None:
        parent = provenance_manifest("castbox/guru-trellis", "b" * 40)
        binding = GTT.provenance_source_binding(
            parent,
            "castbox/guru-trellis",
            "c" * 40,
        )
        postimage = GTT.provenance_tail_manifest_postimage(parent, binding)
        postimage["unexpected"] = True
        self.assertIn(
            "provenance_tail_manifest_fields_outside_allowlist",
            GTT.provenance_tail_manifest_errors(
                parent,
                postimage,
                "c" * 40,
                "castbox/guru-trellis",
            ),
        )

    def test_provenance_tail_transaction_rebind_classifies_strict_ancestor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            GTT.run_stdout(["git", "init", "-q"], cwd=root)
            GTT.run_stdout(["git", "config", "user.name", "Guru Test"], cwd=root)
            GTT.run_stdout(
                ["git", "config", "user.email", "guru@example.invalid"], cwd=root
            )
            GTT.run_stdout(["git", "branch", "-M", "fix/342"], cwd=root)
            manifest_path = root / GTT.PROVENANCE_TAIL_MANIFEST_PATH
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(
                json.dumps(
                    provenance_manifest(
                        "castbox/guru-trellis",
                        "c" * 40,
                        tree_state="dirty",
                        is_mutable_ref=True,
                    ),
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            GTT.run_stdout(["git", "add", "."], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "old publication"], cwd=root)
            old_head = GTT.current_head(root)

            before = json.loads(manifest_path.read_text(encoding="utf-8"))
            after = GTT.provenance_tail_manifest_postimage(
                before,
                {
                    "source_locator": "https://github.com/castbox/guru-trellis.git",
                    "source_ref": old_head,
                    "source_commit": old_head,
                },
            )
            manifest_path.write_text(
                json.dumps(after, indent=2) + "\n",
                encoding="utf-8",
            )
            GTT.run_stdout(["git", "add", "."], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "provenance tail"], cwd=root)
            current_head = GTT.current_head(root)

            current_plan = {
                "plan_digest": "d" * 64,
                "task": {"active_locator": ".trellis/tasks/342"},
                "git": {
                    "repo": "castbox/guru-trellis",
                    "remote": "origin",
                    "head_branch": "fix/342",
                    "base_branch": "main",
                    "branch_review_commit": current_head,
                    "publication_head": current_head,
                },
                "publish": {"title": "current", "body": "Closes #342"},
            }
            predecessor_plan = copy.deepcopy(current_plan)
            predecessor_plan["plan_digest"] = "e" * 64
            predecessor_plan["git"]["branch_review_commit"] = old_head
            predecessor_plan["git"]["publication_head"] = old_head
            transaction = GTT.finalization_transaction_from_plan(
                predecessor_plan,
                next_transition="push_content",
                pre_push_remote_head="a" * 40,
            )
            pr = {
                "number": 337,
                "url": "https://github.com/castbox/guru-trellis/pull/337",
                "headRefOid": old_head,
                "isDraft": False,
                "title": "current",
                "body": "Closes #342",
            }
            with (
                mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
                mock.patch.object(
                    GTT, "closeout_remote_branch_head", return_value=old_head
                ),
            ):
                recovery = GTT.classify_provenance_tail_transaction_rebind(
                    root,
                    current_plan,
                    transaction,
                )
            self.assertEqual(recovery["ancestry"], "strict_ancestor")
            self.assertTrue(recovery["push_required"])
            self.assertEqual(recovery["pre_push_remote_head"], old_head)
            self.assertEqual(recovery["publication_head"], current_head)
            self.assertFalse(recovery["metadata_update_required"])

            active_task_dir = root / current_plan["task"]["active_locator"]
            active_task_dir.mkdir(parents=True)
            finish_summary = active_task_dir / GTT.FINISH_SUMMARY_ARTIFACT
            finish_summary.write_text("{}\n", encoding="utf-8")
            with self.assertRaises(GTT.WorkflowError) as archive_error:
                GTT.classify_provenance_tail_transaction_rebind(
                    root,
                    current_plan,
                    transaction,
                )
            self.assertEqual(
                archive_error.exception.payload["reason_code"],
                "provenance_tail_transaction_rebind_invalid",
            )
            self.assertIn("archive_state", archive_error.exception.payload["errors"])
            finish_summary.unlink()

            for field, mutate in (
                ("task_ref", lambda value: value.update(task_ref=".trellis/tasks/other")),
                ("repo_ref", lambda value: value.update(repo_ref="castbox/other")),
                ("base_branch", lambda value: value.update(base_branch="dev")),
                ("branch", lambda value: value.update(branch="fix/other")),
            ):
                with self.subTest(field=field):
                    drifted = copy.deepcopy(transaction)
                    mutate(drifted)
                    with self.assertRaises(GTT.WorkflowError) as drift_error:
                        GTT.classify_provenance_tail_transaction_rebind(
                            root,
                            current_plan,
                            drifted,
                        )
                    self.assertEqual(
                        drift_error.exception.payload["reason_code"],
                        "provenance_tail_transaction_rebind_invalid",
                    )

            for field, value in (
                ("mode", "existing_pr_recovery"),
                ("next_transition", "archive"),
                ("pr", {"number": 337, "url": pr["url"]}),
                ("adopted_pr", {"number": 337, "url": pr["url"]}),
            ):
                with self.subTest(non_candidate=field):
                    non_candidate = copy.deepcopy(transaction)
                    non_candidate[field] = value
                    self.assertIsNone(
                        GTT.classify_provenance_tail_transaction_rebind(
                            root,
                            current_plan,
                            non_candidate,
                        )
                    )

            with (
                mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
                mock.patch.object(
                    GTT, "closeout_remote_branch_head", return_value="a" * 40
                ),
                self.assertRaises(GTT.WorkflowError) as remote_error,
            ):
                GTT.classify_provenance_tail_transaction_rebind(
                    root,
                    current_plan,
                    transaction,
                )
            self.assertEqual(
                remote_error.exception.payload["reason_code"],
                "provenance_tail_transaction_rebind_remote_head_mismatch",
            )

            business_path = root / "business.txt"
            business_path.write_text("changed\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "."], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "business change"], cwd=root)
            invalid_plan = copy.deepcopy(current_plan)
            invalid_plan["plan_digest"] = "f" * 64
            invalid_plan["git"]["branch_review_commit"] = GTT.current_head(root)
            invalid_plan["git"]["publication_head"] = GTT.current_head(root)
            with self.assertRaises(GTT.WorkflowError) as raised:
                GTT.classify_provenance_tail_transaction_rebind(
                    root,
                    invalid_plan,
                    transaction,
                )
            self.assertEqual(
                raised.exception.payload["reason_code"],
                "provenance_tail_transaction_rebind_invalid",
            )

    def test_provenance_tail_inapplicable_base_evolution_falls_back_to_existing_pr(self) -> None:
        plan = {
            "task": {"active_locator": ".trellis/tasks/344"},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "fix/344",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
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
            "branch_review_commit": "a" * 40,
            "publication_head": "a" * 40,
        }
        recovery = {
            "mode": "existing_pr_recovery",
            "ancestry": "strict_ancestor",
            "push_required": True,
            "pre_push_remote_head": "a" * 40,
            "publication_head": "b" * 40,
        }
        with (
            mock.patch.object(
                GTT,
                "provenance_tail_transaction_rebind_errors",
                return_value=[
                    "provenance_tail_changed_paths_invalid",
                    "provenance_tail_parent_mismatch",
                ],
            ),
            mock.patch.object(
                GTT,
                "provenance_tail_transaction_rebind_is_base_evolution",
                return_value=True,
            ),
            mock.patch.object(
                GTT,
                "resolve_closeout_pull_request",
                return_value={
                    "number": 337,
                    "url": "https://github.com/castbox/guru-trellis/pull/337",
                    "headRefOid": "a" * 40,
                    "isDraft": False,
                    "title": "current",
                    "body": "Closes #344",
                },
            ),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="a" * 40),
            mock.patch.object(
                GTT,
                "classify_existing_pr_recovery",
                return_value=recovery,
            ) as classify_existing,
        ):
            actual = GTT.classify_provenance_tail_transaction_rebind(
                Path("/repo"), plan, transaction
            )
        self.assertEqual(actual, recovery)
        classify_existing.assert_called_once()

    def test_provenance_tail_publication_metadata_drift_keeps_existing_pr_recovery(self) -> None:
        plan = {
            "task": {"active_locator": ".trellis/tasks/353"},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "fix/353",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "publish": {"title": "new title", "body": "Closes #353"},
        }
        transaction = {
            "mode": "ordinary_publication",
            "next_transition": "push_content",
            "pr": None,
            "adopted_pr": None,
            "task_ref": ".trellis/tasks/353",
            "repo_ref": "castbox/guru-trellis",
            "base_branch": "main",
            "branch": "fix/353",
            "publication": {"title": "old title", "body": "Closes #353"},
            "branch_review_commit": "a" * 40,
            "publication_head": "a" * 40,
        }
        recovery = {
            "mode": "existing_pr_recovery",
            "ancestry": "strict_ancestor",
            "push_required": True,
            "pre_push_remote_head": "a" * 40,
            "publication_head": "b" * 40,
        }
        pr = {
            "number": 337,
            "url": "https://github.com/castbox/guru-trellis/pull/337",
            "headRefOid": "a" * 40,
            "isDraft": False,
            "title": "old title",
            "body": "Closes #353",
        }
        with (
            mock.patch.object(
                GTT,
                "provenance_tail_transaction_rebind_errors",
                return_value=[
                    "publication",
                    "provenance_tail_changed_paths_invalid",
                    "provenance_tail_parent_mismatch",
                ],
            ),
            mock.patch.object(
                GTT,
                "provenance_tail_transaction_rebind_base_evolution_tail_parent",
                return_value="b" * 40,
            ),
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="a" * 40),
            mock.patch.object(
                GTT,
                "classify_existing_pr_recovery",
                return_value=recovery,
            ) as classify_existing,
        ):
            actual = GTT.classify_provenance_tail_transaction_rebind(
                Path("/repo"), plan, transaction
            )
        self.assertEqual(actual, recovery)
        classify_existing.assert_called_once()

    def test_ordinary_provenance_tail_reprepare_preflight_requires_old_remote_head(self) -> None:
        plan = {
            "task": {"active_locator": ".trellis/tasks/353"},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "fix/353",
                "base_branch": "main",
                "branch_review_commit": "a" * 40,
                "reviewed_content_head": "a" * 40,
                "publication_head": "b" * 40,
            },
        }
        transaction = {
            "mode": "ordinary_publication",
            "next_transition": "push_content",
            "pr": None,
            "adopted_pr": None,
            "task_ref": ".trellis/tasks/353",
            "repo_ref": "castbox/guru-trellis",
            "base_branch": "main",
            "branch": "fix/353",
            "branch_review_commit": "a" * 40,
            "publication_head": "a" * 40,
        }
        with (
            mock.patch.object(GTT, "repo_relative", return_value=".trellis/tasks/353"),
            mock.patch.object(
                GTT,
                "finalizer_pre_pr_provenance_tail_required",
                return_value=True,
            ),
            mock.patch.object(
                GTT,
                "provenance_tail_transaction_reprepare_eligible",
                return_value=True,
            ),
            mock.patch.object(GTT, "is_ancestor", return_value=True),
            mock.patch.object(
                GTT,
                "closeout_remote_branch_head",
                side_effect=["a" * 40, "c" * 40],
            ),
            mock.patch.object(GTT, "current_head", return_value="b" * 40),
        ):
            facts = GTT.finalizer_current_transaction_provenance_reprepare_preflight(
                Path("/repo"),
                Path("/repo/.trellis/tasks/353"),
                transaction,
                plan,
            )
            self.assertEqual(facts["reviewed_content_head"], "a" * 40)
            self.assertEqual(facts["remote_head"], "a" * 40)
            self.assertIsNone(facts["base_evolution"])
            with self.assertRaises(GTT.WorkflowError) as raised:
                GTT.finalizer_current_transaction_provenance_reprepare_preflight(
                    Path("/repo"),
                    Path("/repo/.trellis/tasks/353"),
                    transaction,
                    plan,
                )
        self.assertEqual(
            raised.exception.payload["reason_code"],
            "provenance_reprepare_remote_not_reviewed_head",
        )

    def test_base_evolution_provenance_tail_rejects_invalid_real_topologies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for command in (
                ["git", "init", "-q", "-b", "main"],
                ["git", "config", "user.name", "Guru Test"],
                ["git", "config", "user.email", "guru@example.invalid"],
            ):
                GTT.run_stdout(command, cwd=root)
            manifest_path = root / GTT.PROVENANCE_TAIL_MANIFEST_PATH
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(
                json.dumps(
                    provenance_manifest(
                        "castbox/guru-trellis",
                        "c" * 40,
                        tree_state="dirty",
                        is_mutable_ref=True,
                    ),
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (root / "base.txt").write_text("base\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "."], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "base"], cwd=root)
            GTT.run_stdout(["git", "switch", "-q", "-c", "fix/347"], cwd=root)
            (root / "publication.txt").write_text("published\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "publication.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "publication"], cwd=root)
            old_head = GTT.current_head(root)
            GTT.run_stdout(["git", "switch", "-q", "main"], cwd=root)
            for index in (1, 2):
                path = root / f"base-{index}.txt"
                path.write_text(f"base {index}\n", encoding="utf-8")
                GTT.run_stdout(["git", "add", path.name], cwd=root)
                GTT.run_stdout(
                    ["git", "commit", "-q", "-m", f"base {index}"], cwd=root
                )
            GTT.run_stdout(["git", "switch", "-q", "fix/347"], cwd=root)
            GTT.run_stdout(
                ["git", "merge", "--no-ff", "-q", "main", "-m", "merge base"],
                cwd=root,
            )
            merge_head = GTT.current_head(root)
            plan = {
                "task": {"active_locator": ".trellis/tasks/347"},
                "git": {
                    "repo": "castbox/guru-trellis",
                    "remote": "origin",
                    "head_branch": "fix/347",
                    "base_branch": "main",
                    "branch_review_commit": merge_head,
                    "publication_head": merge_head,
                },
                "publish": {"title": "current", "body": "Closes #347"},
            }
            transaction = {
                "mode": "ordinary_publication",
                "next_transition": "push_content",
                "pr": None,
                "adopted_pr": None,
                "task_ref": ".trellis/tasks/347",
                "repo_ref": "castbox/guru-trellis",
                "base_branch": "main",
                "branch": "fix/347",
                "publication": {"title": "current", "body": "Closes #347"},
                "branch_review_commit": old_head,
                "publication_head": old_head,
            }

            def reset_to(commit: str) -> None:
                GTT.run_stdout(["git", "reset", "--hard", "-q", commit], cwd=root)
                GTT.run_stdout(["git", "clean", "-fd", "-q"], cwd=root)

            def commit_tail(
                parent: str,
                message: str,
                *,
                invalid_field: bool = False,
                extra_path: bool = False,
            ) -> str:
                before = json.loads(manifest_path.read_text(encoding="utf-8"))
                after = GTT.provenance_tail_manifest_postimage(
                    before,
                    {
                        "source_locator": "https://github.com/castbox/guru-trellis.git",
                        "source_ref": parent,
                        "source_commit": parent,
                    },
                )
                if invalid_field:
                    after["unexpected"] = True
                manifest_path.write_text(
                    json.dumps(after, indent=2) + "\n", encoding="utf-8"
                )
                GTT.run_stdout(["git", "add", GTT.PROVENANCE_TAIL_MANIFEST_PATH], cwd=root)
                if extra_path:
                    (root / "extra.txt").write_text("extra\n", encoding="utf-8")
                    GTT.run_stdout(["git", "add", "extra.txt"], cwd=root)
                GTT.run_stdout(["git", "commit", "-q", "-m", message], cwd=root)
                return GTT.current_head(root)

            def assert_blocked(publication_head: str) -> None:
                current_plan = copy.deepcopy(plan)
                current_plan["git"]["branch_review_commit"] = merge_head
                current_plan["git"]["publication_head"] = publication_head
                for payload_drift in (False, True):
                    with self.subTest(
                        publication_head=publication_head,
                        payload_drift=payload_drift,
                    ):
                        candidate_plan = copy.deepcopy(current_plan)
                        if payload_drift:
                            candidate_plan["publish"] = {
                                "title": "fresh reviewed title",
                                "body": "Closes #347\n\nFresh Publication review evidence.",
                            }
                        with (
                            mock.patch.object(
                                GTT, "resolve_closeout_pull_request"
                            ) as resolve_pr,
                            self.assertRaises(GTT.WorkflowError) as raised,
                        ):
                            GTT.classify_provenance_tail_transaction_rebind(
                                root, candidate_plan, transaction
                            )
                        self.assertEqual(
                            raised.exception.payload["reason_code"],
                            "provenance_tail_transaction_rebind_invalid",
                        )
                        resolve_pr.assert_not_called()

            reset_to(merge_head)
            assert_blocked(
                commit_tail(merge_head, "invalid manifest tail", invalid_field=True)
            )

            reset_to(merge_head)
            assert_blocked(
                commit_tail(merge_head, "tail with extra path", extra_path=True)
            )

            reset_to(merge_head)
            first_tail = commit_tail(merge_head, "first legal tail")
            second_tail = commit_tail(first_tail, "second legal tail")
            assert_blocked(second_tail)

            reset_to(merge_head)
            (root / "business-drift.txt").write_text("drift\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "business-drift.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "business drift"], cwd=root)
            business_head = GTT.current_head(root)
            assert_blocked(commit_tail(business_head, "tail after business drift"))

            reset_to(merge_head)
            GTT.run_stdout(["git", "switch", "-q", "-c", "tail-side"], cwd=root)
            commit_tail(merge_head, "side provenance tail")
            GTT.run_stdout(["git", "switch", "-q", "fix/347"], cwd=root)
            GTT.run_stdout(
                ["git", "merge", "--no-ff", "-q", "tail-side", "-m", "merge tail"],
                cwd=root,
            )
            assert_blocked(GTT.current_head(root))

    def test_provenance_tail_rebind_accepts_base_evolution_and_task_commit_before_tail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for command in (
                ["git", "init", "-q", "-b", "main"],
                ["git", "config", "user.name", "Guru Test"],
                ["git", "config", "user.email", "guru@example.invalid"],
            ):
                GTT.run_stdout(command, cwd=root)

            manifest_path = root / GTT.PROVENANCE_TAIL_MANIFEST_PATH
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(
                json.dumps(
                    provenance_manifest(
                        "castbox/guru-trellis",
                        "c" * 40,
                        tree_state="dirty",
                        is_mutable_ref=True,
                    ),
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (root / "publication.txt").write_text("published\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "."], cwd=root)
            GTT.run_stdout(["git", "commit", "-qm", "publication"], cwd=root)
            old_head = GTT.current_head(root)
            GTT.run_stdout(["git", "switch", "-q", "-c", "fix/355"], cwd=root)

            GTT.run_stdout(["git", "switch", "-q", "main"], cwd=root)
            (root / "base-evolution.txt").write_text("base\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "base-evolution.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-qm", "base evolution"], cwd=root)
            GTT.run_stdout(["git", "switch", "-q", "fix/355"], cwd=root)
            GTT.run_stdout(
                ["git", "merge", "--no-ff", "-q", "main", "-m", "merge base"],
                cwd=root,
            )

            task_projection = root / ".trellis/tasks/355/projection.json"
            task_projection.parent.mkdir(parents=True)
            task_projection.write_text("{\"current\": true}\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", ".trellis/tasks/355/projection.json"], cwd=root)
            GTT.run_stdout(["git", "commit", "-qm", "refresh task projection"], cwd=root)
            reviewed_head = GTT.current_head(root)

            before = json.loads(manifest_path.read_text(encoding="utf-8"))
            after = GTT.provenance_tail_manifest_postimage(
                before,
                {
                    "source_locator": "https://github.com/castbox/guru-trellis.git",
                    "source_ref": reviewed_head,
                    "source_commit": reviewed_head,
                },
            )
            manifest_path.write_text(
                json.dumps(after, indent=2) + "\n", encoding="utf-8"
            )
            GTT.run_stdout(["git", "add", GTT.PROVENANCE_TAIL_MANIFEST_PATH], cwd=root)
            GTT.run_stdout(["git", "commit", "-qm", "provenance tail"], cwd=root)
            publication_head = GTT.current_head(root)

            plan = {
                "plan_digest": "d" * 64,
                "task": {"active_locator": ".trellis/tasks/355"},
                "git": {
                    "repo": "castbox/guru-trellis",
                    "remote": "origin",
                    "head_branch": "fix/355",
                    "base_branch": "main",
                    "branch_review_commit": reviewed_head,
                    "publication_head": publication_head,
                },
                "publish": {"title": "current", "body": "Closes #355"},
            }
            transaction_plan = copy.deepcopy(plan)
            transaction_plan["git"]["branch_review_commit"] = old_head
            transaction_plan["git"]["publication_head"] = old_head
            transaction = GTT.finalization_transaction_from_plan(
                transaction_plan,
                next_transition="push_content",
                pre_push_remote_head=old_head,
            )
            pr = {
                "number": 337,
                "url": "https://github.com/castbox/guru-trellis/pull/337",
                "headRefOid": old_head,
                "isDraft": False,
                "title": "current",
                "body": "Closes #355",
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
            self.assertEqual(recovery["publication_head"], publication_head)


if __name__ == "__main__":
    unittest.main()
