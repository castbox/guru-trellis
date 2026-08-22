from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
VERIFIER = REPO / "trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh"
SCHEMAS = REPO / "trellis/skills/guru-team/schemas"
EXTENSION = REPO / "trellis/guru-team-extension.json"
PHASE2_EXAMPLE = (
    REPO
    / "trellis/skills/guru-team/packages/guru-check-task/examples/phase2-check.json"
)
PHASE2_RECORDER = (
    REPO / "trellis/skills/guru-team/packages/guru-check-task/runtime/record.py"
)
FINISH_WORK_WRAPPER = REPO / "trellis/workflows/guru-team/scripts/bash/finish-work.sh"
MATRIX_HELPER = (
    REPO
    / "trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py"
)


def load_matrix_helper():
    spec = importlib.util.spec_from_file_location(
        "verify_trellis_compatibility_matrix", MATRIX_HELPER
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load compatibility matrix helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VerifyTrellisUpgradeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = VERIFIER.read_text(encoding="utf-8")
        cls.matrix_text = MATRIX_HELPER.read_text(encoding="utf-8")
        cls.matrix = load_matrix_helper()

    def test_default_entry_delegates_to_live_manifest_matrix(self) -> None:
        dispatch = self.text.index(
            'if [[ "${GURU_TEAM_THROWAWAY_SINGLE_REPO_COMPATIBILITY:-0}" != "1" ]]'
        )
        legacy_target = self.text.index('mkdir "$TARGET"', dispatch)
        self.assertLess(dispatch, legacy_target)
        segment = self.text[dispatch:legacy_target]
        self.assertIn('source_python "$COMPATIBILITY_MATRIX_HELPER" "${MATRIX_ARGS[@]}"', segment)
        self.assertIn('--before-tag "v0.6.5-guru.10"', segment)
        self.assertIn('--before-cli "0.6.5"', segment)
        self.assertIn('--target-cli "$TRELLIS_TARGET_VERSION"', segment)
        self.assertIn('TRELLIS_TARGET_VERSION="${TRELLIS_TARGET_VERSION:-0.6.15}"', self.text)
        self.assertIn('TRELLIS_UPGRADE_TAG="${TRELLIS_UPGRADE_TAG:-0.6.15}"', self.text)

    def test_empty_cleanup_preserves_the_primary_verifier_failure(self) -> None:
        self.assertIn('if [[ "${#GURU_TEMP_FILES[@]}" -gt 0 ]]; then', self.text)
        with tempfile.TemporaryDirectory() as directory:
            work_dir = Path(directory)
            (work_dir / "project").mkdir()
            result = subprocess.run(
                (str(VERIFIER), str(work_dir)),
                cwd=REPO,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Target already exists", result.stderr)
        self.assertNotIn("GURU_TEMP_FILES[@]: unbound variable", result.stderr)

    def test_nonempty_cleanup_removes_only_allowed_temporary_files(self) -> None:
        cleanup_start = self.text.index("GURU_TEMP_FILES=()")
        cleanup_end = self.text.index("trap cleanup_guru_temporary_objects", cleanup_start)
        cleanup_source = self.text[cleanup_start:cleanup_end]
        with tempfile.TemporaryDirectory() as directory:
            work_dir = Path(directory)
            allowed = work_dir / "guru-task-commit-input.allowed"
            unrelated = work_dir / "unrelated.txt"
            allowed.write_text("temporary\n", encoding="utf-8")
            unrelated.write_text("preserve\n", encoding="utf-8")
            script = f"""set -euo pipefail
WORK_DIR={json.dumps(str(work_dir))}
GURU_AUTO_WORK_DIR=0
{cleanup_source}
GURU_TEMP_FILES+=({json.dumps(str(allowed))})
GURU_TEMP_FILES+=({json.dumps(str(unrelated))})
trap cleanup_guru_temporary_objects EXIT
printf '%s\\n' 'primary verifier failure' >&2
exit 23
"""
            result = subprocess.run(
                ("bash", "-c", script),
                cwd=REPO,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 23)
            self.assertIn("primary verifier failure", result.stderr)
            self.assertFalse(allowed.exists())
            self.assertTrue(unrelated.exists())

    def test_live_platform_authorities_derive_exact_six_cell_matrix(self) -> None:
        inventory = self.matrix.derive_platform_inventory(REPO)
        plan = self.matrix.build_matrix(REPO)

        self.assertEqual(inventory["platforms"], ["claude", "codex", "cursor"])
        self.assertEqual(plan["cell_count"], 6)
        self.assertEqual(
            [cell["cell_id"] for cell in plan["cells"]],
            [
                "claude-clean",
                "claude-existing",
                "codex-clean",
                "codex-existing",
                "cursor-clean",
                "cursor-existing",
            ],
        )
        self.assertTrue(all(cell["shared_projection"] for cell in plan["cells"]))

    def test_matrix_executor_uses_exact_upgrade_and_conditional_migrate(self) -> None:
        upgrade = self.matrix_text.index('(str(binary), "upgrade", "--tag", target_cli)')
        dry_run = self.matrix_text.index('(str(binary), "update", "--dry-run")', upgrade)
        conditional = self.matrix_text.index('if "MIGRATION REQUIRED" in dry_run:', dry_run)
        migrate = self.matrix_text.index(
            '(str(binary), "update", "--migrate", "--skip-all")', conditional
        )
        normal = self.matrix_text.index(
            '(str(binary), "update", "--skip-all")', migrate
        )
        workflow_call = self.matrix_text.index(
            "_preview_and_switch_workflow(", normal
        )
        reapply = self.matrix_text.index(
            "reapplied_preset = _apply_preset(", workflow_call
        )
        reapply_call = self.matrix_text[
            reapply : self.matrix_text.index("\n        )", reapply) + len("\n        )")
        ]
        self.assertLess(upgrade, dry_run)
        self.assertLess(dry_run, conditional)
        self.assertLess(conditional, migrate)
        self.assertLess(migrate, normal)
        self.assertLess(normal, workflow_call)
        self.assertLess(workflow_call, reapply)
        self.assertIn("previous_root=source_root", reapply_call)
        workflow_function = self.matrix_text[
            self.matrix_text.index("def _preview_and_switch_workflow(") :
            self.matrix_text.index("\ndef _sidecars(")
        ]
        self.assertLess(
            workflow_function.index('"--create-new"'),
            workflow_function.index('input_text="y\\n"'),
        )
        self.assertNotIn('"--force"', workflow_function)
        self.assertNotIn('"latest"', self.matrix_text)

    def test_matrix_retains_legacy_representative_and_runs_parallel_finish(self) -> None:
        run_matrix = self.matrix_text[self.matrix_text.index("def run_matrix(") :]
        self.assertIn('verify_installed_parallel_finish.py', run_matrix)
        self.assertIn('parallel_finish.get("status") != "passed"', run_matrix)
        self.assertIn('legacy_representative = work_root.parent / "project"', run_matrix)
        self.assertIn('"representative_root": "project"', run_matrix)
        self.assertIn('"external_boundaries"', run_matrix)

    def test_matrix_runs_installed_profile_corpora_and_binds_platform_projection(self) -> None:
        smoke = self.matrix_text[
            self.matrix_text.index("def _run_installed_smokes(") :
            self.matrix_text.index("\ndef validate_cell(")
        ]
        self.assertIn('wrappers / "run-skill-evals.sh"', smoke)
        self.assertIn('"--adapter",\n                "shared"', smoke)
        self.assertIn('"platform_projection": platform', smoke)
        self.assertIn('"guru-maintain-requirements-design-test-ssot"', smoke)
        self.assertIn('"guru-maintain-architecture-baseline"', smoke)
        self.assertIn('"guru-bootstrap-repository-ssot"', smoke)
        self.assertIn("covered_profiles != declared_profiles", smoke)
        self.assertNotIn('"--help"', smoke)

    def test_capability_projection_is_compact_and_complete(self) -> None:
        projection = self.matrix.capability_projection(REPO)

        self.assertRegex(projection["projection_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(len(projection["skill_api"]["interfaces"]), 21)
        self.assertEqual(len(projection["workflow"]["skill_invokes"]), 20)
        self.assertEqual(len(projection["workflow"]["skill_exits"]), 87)
        self.assertEqual(len(projection["workflow"]["workflow_targets"]), 33)
        self.assertEqual(len(projection["workflow"]["stop_targets"]), 21)
        self.assertEqual(
            projection["distribution"]["platforms"],
            ["claude", "codex", "cursor"],
        )
        self.assertGreater(
            len(projection["distribution"]["skill_package_files_and_modes"]),
            4000,
        )
        self.assertGreater(
            len(projection["distribution"]["managed_asset_files_and_modes"]),
            0,
        )

    def test_source_state_binds_head_tracked_delta_and_untracked_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            subprocess.run(("git", "init", "-q"), cwd=repo, check=True)
            subprocess.run(
                ("git", "config", "user.name", "Matrix Test"), cwd=repo, check=True
            )
            subprocess.run(
                ("git", "config", "user.email", "matrix@example.invalid"),
                cwd=repo,
                check=True,
            )
            tracked = repo / "tracked.txt"
            tracked.write_text("base\n")
            subprocess.run(("git", "add", "tracked.txt"), cwd=repo, check=True)
            subprocess.run(
                ("git", "commit", "-q", "-m", "base"), cwd=repo, check=True
            )

            clean = self.matrix.source_state(repo)
            self.assertFalse(clean["dirty"])
            self.assertEqual(clean["untracked_files"], [])
            self.assertEqual(
                clean["candidate_tree"],
                subprocess.run(
                    ("git", "rev-parse", "HEAD^{tree}"),
                    cwd=repo,
                    check=True,
                    text=True,
                    stdout=subprocess.PIPE,
                ).stdout.strip(),
            )

            tracked.write_text("candidate\n")
            untracked = repo / "new.sh"
            untracked.write_text("#!/bin/sh\n")
            untracked.chmod(0o755)
            dirty = self.matrix.source_state(repo)
            self.assertTrue(dirty["dirty"])
            self.assertEqual(dirty["head"], clean["head"])
            self.assertNotEqual(dirty["identity_sha256"], clean["identity_sha256"])
            self.assertNotEqual(dirty["candidate_tree"], clean["candidate_tree"])
            self.assertEqual(
                dirty["untracked_files"],
                [
                    {
                        "path": "new.sh",
                        "mode": "100755",
                        "sha256": hashlib.sha256(b"#!/bin/sh\n").hexdigest(),
                    }
                ],
            )

            tracked.write_text("different candidate\n")
            changed = self.matrix.source_state(repo)
            self.assertNotEqual(
                changed["identity_sha256"], dirty["identity_sha256"]
            )

    def test_docs_authority_snapshot_covers_versioned_bodies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "repo"
            self.matrix._init_git_repo(target)
            projection = target / ".trellis/spec/docs/index.md"
            projection.parent.mkdir(parents=True, exist_ok=True)
            projection.write_text("# Minimal projection\n")
            snapshot = self.matrix._docs_authority_snapshot(target)

            self.assertEqual(len(snapshot), 8)
            self.assertTrue(
                all(
                    f"docs/{domain}/versions/current-business/authority.md"
                    in snapshot
                    for domain in ("requirements", "design", "test", "architecture")
                )
            )
            self.matrix._assert_docs_authority(target, snapshot)

            removed = (
                target
                / "docs/requirements/versions/current-business/authority.md"
            )
            removed.unlink()
            with self.assertRaisesRegex(
                self.matrix.MatrixError, "changed Docs authority"
            ):
                self.matrix._assert_docs_authority(target, snapshot)

    def test_overlay_mode_projection_ignores_archive_umask_but_preserves_executable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "entry.md"
            path.write_text("entry\n")

            path.chmod(0o644)
            self.assertEqual(self.matrix._executable_projection(path), 0)
            path.chmod(0o664)
            self.assertEqual(self.matrix._executable_projection(path), 0)
            path.chmod(0o755)
            self.assertEqual(self.matrix._executable_projection(path), 1)

    def test_capability_comparison_isolates_version_binding(self) -> None:
        before = self.matrix.capability_projection(REPO)
        after = json.loads(json.dumps(before))
        after["extension"]["version"] = "0.6.15-guru.test"
        after["extension"]["target_trellis_cli"] = "0.6.15"
        after["extension"]["requires_trellis_cli"] = "0.6.15"
        after["extension"]["tested_trellis_cli"] = ["0.6.15"]

        version_only = self.matrix.compare_capabilities(before, after)
        self.assertTrue(version_only["capabilities_preserved"])
        self.assertEqual(version_only["blocking_differences"], [])

        after["workflow"]["skill_invokes"] = after["workflow"]["skill_invokes"][1:]
        lost = self.matrix.compare_capabilities(before, after)
        self.assertFalse(lost["capabilities_preserved"])
        self.assertEqual(
            [difference["group"] for difference in lost["blocking_differences"]],
            ["workflow"],
        )

        after = json.loads(json.dumps(before))
        after["extension"]["extension_id"] = "guru-team-drifted"
        identity_drift = self.matrix.compare_capabilities(before, after)
        self.assertFalse(identity_drift["capabilities_preserved"])
        self.assertEqual(
            [
                difference["group"]
                for difference in identity_drift["blocking_differences"]
            ],
            ["extension_identity"],
        )

        after = json.loads(json.dumps(before))
        after["distribution"]["skill_package_files_and_modes"] = after[
            "distribution"
        ]["skill_package_files_and_modes"][1:]
        mode_loss = self.matrix.compare_capabilities(before, after)
        self.assertFalse(mode_loss["capabilities_preserved"])
        self.assertEqual(
            [difference["group"] for difference in mode_loss["blocking_differences"]],
            ["distribution"],
        )

    def test_installed_projection_and_template_hash_classification_are_current(self) -> None:
        installed = self.matrix.installed_capability_projection(REPO)
        comparison = self.matrix.compare_capabilities(installed, installed)
        template_hashes = self.matrix._assert_template_hashes(REPO, REPO)

        self.assertTrue(comparison["capabilities_preserved"])
        self.assertEqual(len(installed["skill_api"]["interfaces"]), 21)
        self.assertEqual(installed["distribution"]["platforms"], ["claude", "codex", "cursor"])
        self.assertEqual(template_hashes["unknown_drift_count"], 0)
        self.assertGreater(template_hashes["entry_count"], 0)

    def test_managed_asset_hashes_are_a_verified_subset_of_managed_assets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            source = root / "source"
            hashed = target / "managed/hashed.txt"
            unhashed = target / "managed/unhashed.txt"
            managed_script = target / ".trellis/guru-team/scripts/bash/managed.sh"
            overlay_target = target / "overlay.sh"
            overlay_source = source / "canonical/overlay.sh"
            for path, content in (
                (hashed, b"hashed\n"),
                (unhashed, b"unhashed\n"),
                (managed_script, b"#!/bin/sh\n"),
                (overlay_target, b"#!/bin/sh\n"),
                (overlay_source, b"#!/bin/sh\n"),
            ):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            overlay_target.chmod(0o755)
            overlay_source.chmod(0o755)
            managed_script.chmod(0o755)

            installed = {
                "skill_packages": {
                    "files": [
                        {"path": "managed/hashed.txt", "executable": False},
                        {"path": "managed/unhashed.txt", "executable": False},
                    ]
                },
                "overlays": {
                    "files": [
                        {
                            "path": "overlay.sh",
                            "source": "canonical/overlay.sh",
                            "executable": True,
                        }
                    ]
                },
                "install": {
                    "managed_assets": [
                        "managed/hashed.txt",
                        "managed/unhashed.txt",
                        ".trellis/guru-team/scripts/bash/managed.sh",
                    ],
                    "managed_asset_hashes": {
                        "managed/hashed.txt": hashlib.sha256(
                            hashed.read_bytes()
                        ).hexdigest()
                    },
                },
            }

            self.matrix._assert_installed_file_modes(target, installed, source)

            managed_script.chmod(0o644)
            with self.assertRaisesRegex(
                self.matrix.MatrixError, "managed asset mode drift"
            ):
                self.matrix._assert_installed_file_modes(target, installed, source)

            managed_script.chmod(0o755)
            installed["install"]["managed_asset_hashes"] = {
                "managed/not-declared.txt": "0" * 64
            }
            with self.assertRaisesRegex(
                self.matrix.MatrixError, "managed asset path/hash inventory mismatch"
            ):
                self.matrix._assert_installed_file_modes(target, installed, source)

    def test_existing_preset_reapply_reconciles_exact_before_backups(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            previous = root / "previous"
            target = root / "target"
            relative = Path(
                ".trellis/guru-team/skills/packages/example/runtime/value.txt"
            )
            for base, value in (
                (source, "candidate\n"),
                (previous, "before\n"),
                (target, "before\n"),
            ):
                path = base / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(value)
            installer = (
                source
                / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"
            )
            installer.parent.mkdir(parents=True, exist_ok=True)
            installer.write_text(
                "import json,sys\n"
                "from pathlib import Path\n"
                "repo=Path(sys.argv[sys.argv.index('--repo')+1])\n"
                f"relative=Path({relative.as_posix()!r})\n"
                "current=repo/relative\n"
                "backup=Path(str(current)+'.bak')\n"
                "if current.read_text() == 'before\\n':\n"
                "    backup.write_bytes(current.read_bytes())\n"
                "    current.write_text('candidate\\n')\n"
                "    print(json.dumps({'status':'conflict','skill_packages':{'sidecars':[relative.as_posix()+'.bak']}}))\n"
                "    raise SystemExit(2)\n"
                "print(json.dumps({'status':'ok','skill_packages':{'sidecars':[]}}))\n"
            )

            result = self.matrix._apply_preset(
                source,
                target,
                "claude",
                root / "preset.log",
                previous_root=previous,
            )

            self.assertEqual(result["status"], "passed")
            self.assertEqual(
                result["reconciled_backups"], [relative.as_posix() + ".bak"]
            )
            self.assertEqual((target / relative).read_text(), "candidate\n")
            self.assertFalse(Path(str(target / relative) + ".bak").exists())
            self.assertIn(
                "reconciled known upgrade backups",
                (root / "preset.log").read_text(),
            )

    def test_cli_install_and_upgrade_stay_in_disposable_prefix(self) -> None:
        self.assertIn('TRELLIS_CLI_PREFIX="$WORK_DIR/trellis-cli-prefix"', self.text)
        self.assertIn(
            'npm_config_prefix="$TRELLIS_CLI_PREFIX" npm install -g "$TRELLIS_PRE_UPGRADE_PACKAGE"',
            self.text,
        )
        self.assertIn('export npm_config_prefix="$TRELLIS_CLI_PREFIX"', self.text)
        self.assertIn('TRELLIS_CLI_BIN="$TRELLIS_CLI_PREFIX/bin/trellis"', self.text)
        self.assertIn('trellis upgrade --tag "$TRELLIS_UPGRADE_TAG"', self.text)
        self.assertIn('trellis-version-before-upgrade.txt', self.text)
        self.assertIn('trellis-version-after-upgrade.txt', self.text)
        self.assertIn('trellis upgrade escaped the isolated npm prefix', self.text)

    def test_initial_install_upgrade_update_preview_and_reapply_order_is_closed(self) -> None:
        initial = self.text.index("trellis init -y --claude --codex --cursor")
        upgrade = self.text.index('trellis upgrade --tag "$TRELLIS_UPGRADE_TAG"')
        dry_run = self.text.index("trellis update --dry-run 2>&1", upgrade)
        migrate_branch = self.text.index('if grep -Fq "MIGRATION REQUIRED"', dry_run)
        migrate = self.text.index("trellis update --migrate --skip-all", migrate_branch)
        normal_update = self.text.index("    trellis update --skip-all\n", migrate)
        preview = self.text.index(
            'trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --create-new',
            normal_update,
        )
        switch = self.text.index(
            'trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force',
            preview,
        )
        reapply = self.text.index(
            'apply_guru_team_trellis_preset.py" \\\n  --repo "$TARGET"',
            switch,
        )
        self.assertLess(initial, upgrade)
        self.assertLess(upgrade, dry_run)
        self.assertLess(dry_run, migrate_branch)
        self.assertLess(migrate_branch, migrate)
        self.assertLess(migrate, normal_update)
        self.assertLess(normal_update, preview)
        self.assertLess(preview, switch)
        self.assertLess(switch, reapply)
        primary_update_segment = self.text[upgrade:reapply]
        self.assertNotIn("trellis update --force", primary_update_segment)
        self.assertIn("trellis update --migrate --skip-all", primary_update_segment)
        self.assertIn("trellis update --skip-all", primary_update_segment)
        self.assertIn('printf \'%s\\n\' "migrate" >"$WORK_DIR/trellis-update-mode.txt"', primary_update_segment)
        self.assertIn('printf \'%s\\n\' "update" >"$WORK_DIR/trellis-update-mode.txt"', primary_update_segment)

    def test_post_reapply_gate_checks_ownership_and_recursive_sidecars(self) -> None:
        self.assertIn('ownership_checkpoint "post-preset-reapply-before-final-checks"', self.text)
        self.assertIn(
            'FINAL_SIDECARS="$(find "$TARGET" -type f \\( -name \'*.new\' -o -name \'*.bak\' \\) -print)"',
            self.text,
        )
        self.assertIn("Unexpected .new/.bak sidecars after preview, switch, update, and preset reapply", self.text)

    def test_finish_work_compatibility_wrapper_exposes_shared_runtime(self) -> None:
        wrapper = FINISH_WORK_WRAPPER.read_text(encoding="utf-8")
        self.assertIn(
            'export PYTHONPATH="$RUNTIME:$GURU_ROOT${PYTHONPATH:+:$PYTHONPATH}"',
            wrapper,
        )
        self.assertIn('"$RUNTIME/legacy.py" finish-work "$@"', wrapper)

    def test_embedded_installed_schema_inventory_matches_canonical_source(self) -> None:
        inventory_anchor = 'skills_root = root / ".trellis/guru-team/skills"'
        assertion_start = self.text.index("assert {", self.text.index(inventory_anchor))
        literal_start = self.text.index("} == {", assertion_start) + len("} == ")
        literal_end = self.text.index("\n}\nfor artifact", literal_start) + 2
        embedded_inventory = ast.literal_eval(self.text[literal_start:literal_end])
        canonical_inventory = {path.name for path in SCHEMAS.iterdir() if path.is_file()}

        self.assertEqual(embedded_inventory, canonical_inventory)

    def test_embedded_installed_public_api_expectations_match_canonical_source(self) -> None:
        contract_anchor = 'assert api["skill_contracts"]["contract_manifests"] == '
        contract_start = self.text.index(contract_anchor) + len(contract_anchor)
        contract_end = self.text.index(
            '\nassert api["skill_evals"]["schema_id"]',
            contract_start,
        )
        embedded_contracts = ast.literal_eval(self.text[contract_start:contract_end])

        run_schemas_anchor = 'assert api["skill_evals"]["run_schema_ids"] == '
        run_schemas_start = self.text.index(run_schemas_anchor) + len(run_schemas_anchor)
        run_schemas_end = self.text.index("\n", run_schemas_start)
        embedded_run_schemas = ast.literal_eval(
            self.text[run_schemas_start:run_schemas_end]
        )

        public_api = json.loads(EXTENSION.read_text(encoding="utf-8"))["public_api"]
        self.assertEqual(
            embedded_contracts,
            public_api["skill_contracts"]["contract_manifests"],
        )
        self.assertEqual(
            embedded_run_schemas,
            public_api["skill_evals"]["run_schema_ids"],
        )
        self.assertIn(
            'test -f "$TARGET/.trellis/guru-team/skills/contracts/production-current-4.0.json"',
            self.text,
        )

    def test_phase2_smoke_matches_current_recorder_and_stops_on_command_error(self) -> None:
        function_start = self.text.index("record_throwaway_phase2() {")
        function_end = self.text.index("\n}\n\nPHASE2_DTO=", function_start) + 2
        function = self.text[function_start:function_end]

        projection_anchor = "    for key in "
        projection_start = function.index(projection_anchor) + len(projection_anchor)
        projection_end = function.index("\n}", projection_start)
        projected_keys = set(
            ast.literal_eval(function[projection_start:projection_end])
        )

        recorder_tree = ast.parse(PHASE2_RECORDER.read_text(encoding="utf-8"))
        recorder_keys = next(
            set(ast.literal_eval(node.value))
            for node in ast.walk(recorder_tree)
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "expected"
                for target in node.targets
            )
        )
        example = json.loads(PHASE2_EXAMPLE.read_text(encoding="utf-8"))

        self.assertEqual(projected_keys, recorder_keys)
        self.assertIn(
            f'recorded["schema_version"] == "{example["schema_version"]}"',
            function,
        )
        self.assertEqual(
            function.count('|| { rm -f "$input_path"; return 1; }'),
            2,
        )
        self.assertEqual(
            function.count('|| { rm -f "$public_input"; return 1; }'),
            1,
        )
        self.assertGreaterEqual(function.count("|| return 1"), 3)


if __name__ == "__main__":
    unittest.main()
