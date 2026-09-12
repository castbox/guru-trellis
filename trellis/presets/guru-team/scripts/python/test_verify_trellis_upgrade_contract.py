from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO = Path(__file__).resolve().parents[5]
VERIFIER = REPO / "trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh"
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

    def fork_fixture(self, root: Path) -> tuple[Path, Path]:
        root = root.resolve()
        source, repo = root / "fork checkout", root / "extension"
        source.mkdir()
        files = {
            "package.json": json.dumps({"packageManager": "pnpm@10.32.1"}),
            "packages/cli/package.json": json.dumps({"version": "0.6.17", "type": "module"}),
            "packages/cli/bin/trellis.js": 'import("../dist/cli/index.js");\n',
            "packages/cli/dist/cli/index.js": 'console.log("0.6.17");\n',
            "packages/core/dist/index.js": "export {};\n",
            "packages/cli/src/templates/trellis/example.md": "template\n",
            "packages/cli/dist/templates/trellis/example.md": "template\n",
            ".gitignore": "**/dist/\n",
        }
        for relative, content in files.items():
            path = source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        def git(*args):
            return subprocess.run(("git", *args), cwd=source, check=True,
                                  text=True, capture_output=True).stdout.strip()
        git("init", "-q")
        git("add", ".")
        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "commit", "-qm", "source fixture")
        (source / "packages/cli/dist/.guru-source-commit").write_text(git("rev-parse", "HEAD") + "\n")
        git("remote", "add", "upstream", "https://github.com/castbox/Trellis.git")
        lock = repo / "trellis/presets/guru-team/source/trellis-source.json"
        lock.parent.mkdir(parents=True)
        lock.write_text(json.dumps({"schema_version": "1.0",
            "repository": "https://github.com/castbox/Trellis.git", "commit": git("rev-parse", "HEAD"),
            "cli_version": "0.6.17", "package_manager": "pnpm@10.32.1"}))
        return repo, source

    def test_fork_source_uses_real_node_esm_entry_and_observed_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, source = self.fork_fixture(Path(directory))
            result = self.matrix.validate_fork_source(repo, source)
            self.assertEqual(result["cli_version"], "0.6.17")
            self.assertEqual(result["command"][1], str(source / "packages/cli/bin/trellis.js"))
            self.assertEqual(result["template_count"], 1)
            self.assertEqual(result["commit"], json.loads((repo /
                "trellis/presets/guru-team/source/trellis-source.json").read_text())["commit"])

    def test_fork_source_rejects_wrong_stale_missing_and_dirty_inputs(self) -> None:
        cases = ("head", "schema", "manager", "version", "remote", "dirty", "missing", "template", "runtime")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                repo, source = self.fork_fixture(Path(directory))
                lock_path = repo / "trellis/presets/guru-team/source/trellis-source.json"
                lock = json.loads(lock_path.read_text())
                if case in ("head", "schema", "manager", "version"):
                    key, value = {"head": ("commit", "0" * 40), "schema": ("schema_version", "2.0"),
                                  "manager": ("package_manager", "pnpm@9.0.0"),
                                  "version": ("cli_version", "0.6.15")}[case]
                    lock[key] = value
                    lock_path.write_text(json.dumps(lock))
                elif case == "remote":
                    subprocess.run(("git", "remote", "set-url", "upstream",
                                    "https://github.com/mindfold-ai/Trellis.git"), cwd=source, check=True)
                elif case == "dirty":
                    (source / "packages/cli/bin/trellis.js").write_text("changed\n")
                elif case == "missing":
                    (source / "packages/cli/dist/cli/index.js").unlink()
                elif case == "template":
                    (source / "packages/cli/dist/templates/trellis/example.md").write_text("old\n")
                else:
                    (source / "packages/cli/dist/cli/index.js").write_text('console.log("0.6.15");\n')
                with self.assertRaises(self.matrix.MatrixError):
                    self.matrix.validate_fork_source(repo, source)

    def test_full_mode_blocks_before_creating_resources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, source = self.fork_fixture(root)
            args = argparse.Namespace(repo_root=repo, fork_source=source,
                                      mode="full", work_root=root / "work")
            with self.assertRaisesRegex(self.matrix.MatrixError, "requires --predecessor-source") as raised:
                self.matrix.run_matrix(args)
            failure = self.matrix.matrix_failure_payload(raised.exception)["failure"]
            self.assertEqual(failure["stage"], "pre-matrix")
            self.assertEqual(failure["command_label"], "predecessor-source-validation")
            self.assertFalse(args.work_root.exists())

    def test_full_public_dispatch_reaches_catalog_with_verified_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, source = self.fork_fixture(root)
            commit = json.loads((repo / "trellis/presets/guru-team/source/trellis-source.json").read_text())["commit"]
            args = argparse.Namespace(repo_root=repo, fork_source=source, mode="full",
                predecessor_source=source, predecessor_commit=commit, before_cli="0.6.17")
            with mock.patch.object(self.matrix, "_run_historical_matrix", return_value={"status": "passed"}) as catalog:
                self.assertEqual(self.matrix.run_matrix(args), {"status": "passed"})
            catalog.assert_called_once()
            self.assertEqual(catalog.call_args.kwargs["predecessor"]["commit"], commit)
            self.assertEqual(catalog.call_args.kwargs["source"]["command"],
                             catalog.call_args.kwargs["predecessor"]["command"])
            self.assertEqual(args.target_cli, "0.6.17")

    def test_predecessor_accepts_flat_build_and_rejects_wrong_identity(self) -> None:
        import shutil

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, source = self.fork_fixture(root)
            flat = root / "old fork"
            shutil.copytree(source / "packages/cli", flat)
            (flat / ".gitignore").write_text("dist/\n")
            def git(*args):
                return subprocess.run(("git", *args), cwd=flat, check=True,
                                      text=True, capture_output=True).stdout.strip()
            git("init", "-q")
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "flat")
            (flat / "dist/.guru-source-commit").write_text(git("rev-parse", "HEAD") + "\n")
            git("remote", "add", "origin", "https://github.com/castbox/Trellis.git")
            args = argparse.Namespace(repo_root=repo, predecessor_source=flat,
                predecessor_commit=git("rev-parse", "HEAD"), before_cli="0.6.17")
            result = self.matrix.validate_predecessor_source(args)
            self.assertEqual(result["command"][1], str(flat.resolve() / "bin/trellis.js"))
            args.before_cli = "0.6.5"
            with self.assertRaisesRegex(self.matrix.MatrixError, "version/package manager"):
                self.matrix.validate_predecessor_source(args)
            args.before_cli = "0.6.17"
            args.predecessor_commit = "0" * 40
            with self.assertRaisesRegex(self.matrix.MatrixError, "HEAD"):
                self.matrix.validate_predecessor_source(args)

    def test_full_catalog_runs_cells_parallel_check_and_owner_representative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            repo, source = self.fork_fixture(root)
            commit = json.loads((repo / "trellis/presets/guru-team/source/trellis-source.json").read_text())["commit"]
            args = argparse.Namespace(repo_root=repo, fork_source=source, mode="full",
                predecessor_source=source, predecessor_commit=commit, before_cli="0.6.17",
                before_tag="before", work_root=root / "install/matrix", workflow_source="fixture",
                allow_local_sample=False)
            cells = [{"cell_id": "codex-" + scenario, "platform": "codex", "scenario": scenario}
                     for scenario in ("clean", "existing")]
            def cell(**kwargs):
                target = kwargs["cell_root"] / "project"
                target.mkdir()
                (target / "installed-marker").write_text("installed")
                self.assertEqual(kwargs["predecessor"]["commit"], commit)
                return {"status": "passed", "workflow_sample": "exact_marketplace"}
            real_run = self.matrix._run
            def run(command, **kwargs):
                if any(str(part).endswith("verify_installed_parallel_finish.py") for part in command):
                    return '{"status":"passed"}'
                return real_run(command, **kwargs)
            with mock.patch.object(self.matrix, "build_matrix", return_value={
                    "cells": cells, "platform_inventory_sha256": "platforms", "matrix_sha256": "matrix"}), \
                 mock.patch.object(self.matrix, "source_state", return_value={"head": commit, "identity_sha256": "state"}), \
                 mock.patch.object(self.matrix, "resolve_before_tag", return_value={
                    "before_tag": "before", "before_commit": commit, "before_tag_object": commit}), \
                 mock.patch.object(self.matrix, "_run_cell", side_effect=cell) as run_cell, \
                 mock.patch.object(self.matrix, "_run", side_effect=run):
                result = self.matrix.run_matrix(args)
            self.assertEqual(run_cell.call_count, 2)
            self.assertEqual(result["mode"], "full")
            self.assertEqual(result["parallel_finish"]["status"], "passed")
            self.assertEqual((root / "install/project/installed-marker").read_text(), "installed")

    def test_existing_cell_seeds_before_command_then_updates_target_command(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            before = ("node", "/before/bin/trellis.js")
            target = ("node", "/target/packages/cli/bin/trellis.js")
            projection = {"projection_sha256": "projection"}
            with mock.patch.object(self.matrix, "validate_fork_source", return_value={"command": target}), \
                 mock.patch.object(self.matrix, "_init_git_repo"), \
                 mock.patch.object(self.matrix, "_assert_version", side_effect=["0.6.5", "0.6.17"]), \
                 mock.patch.object(self.matrix, "_export_git_tree"), \
                 mock.patch.object(self.matrix, "_install_workflow", return_value=False) as init, \
                 mock.patch.object(self.matrix, "_docs_authority_snapshot", return_value={}), \
                 mock.patch.object(self.matrix, "_apply_preset", return_value={}), \
                 mock.patch.object(self.matrix, "capability_projection", return_value=projection), \
                 mock.patch.object(self.matrix, "installed_capability_projection", return_value=projection), \
                 mock.patch.object(self.matrix, "_load_json", return_value={"extension": {"version": "0.6.5-guru.36"}}), \
                 mock.patch.object(self.matrix, "_run", return_value="MIGRATION REQUIRED") as run, \
                 mock.patch.object(self.matrix, "_workflow_source_requires_local_sample", return_value=False), \
                 mock.patch.object(self.matrix, "_preview_and_switch_workflow") as switch, \
                 mock.patch.object(self.matrix, "_assert_docs_authority"), \
                 mock.patch.object(self.matrix, "compare_capabilities", return_value={"comparison_sha256": "comparison"}), \
                 mock.patch.object(self.matrix, "_assert_projection_consistency"), \
                 mock.patch.object(self.matrix, "validate_cell", return_value={}):
                result = self.matrix._run_cell(repo_root=root, cell_root=root / "cell", platform="codex",
                    scenario="existing", workflow_source="fixture", before_tag="before",
                    before_cli="0.6.5", target_cli="0.6.17", allow_local_sample=False,
                    fork_source=root / "fork", predecessor={"command": before})
            self.assertEqual(init.call_args.args[1], before)
            self.assertEqual([call.args[0] for call in run.call_args_list], [
                (*target, "update", "--dry-run"),
                (
                    *target,
                    "update",
                    "--force",
                    "--migrate",
                    "--assignee",
                    "matrix-owner",
                    "--skip-all",
                ),
            ])
            self.assertEqual(switch.call_args.args[1], target)
            self.assertEqual(result["update_mode"], "migrate")

    def test_dry_run_retirement_migration_markers(self) -> None:
        for output in (
            "MIGRATION REQUIRED",
            "Retirement conflicts: .trellis/config.yaml, AGENTS.md",
        ):
            with self.subTest(output=output):
                self.assertTrue(
                    self.matrix._dry_run_requires_retirement_migration(output)
                )
        self.assertFalse(
            self.matrix._dry_run_requires_retirement_migration(
                "This will UPGRADE: 0.6.16 to 0.6.17"
            )
        )

    def test_install_workflow_uses_version_specific_explicit_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            with mock.patch.object(
                self.matrix, "_workflow_source_requires_local_sample", return_value=False
            ), mock.patch.object(self.matrix, "_run") as runner:
                for version, expected in (
                    ("0.6.16", ("--user", "matrix-owner")),
                    (
                        "0.6.17",
                        (
                            "--creator",
                            "matrix-owner",
                            "--assignee",
                            "matrix-owner",
                        ),
                    ),
                ):
                    with self.subTest(version=version):
                        self.matrix._install_workflow(
                            target,
                            ("node", "trellis.js"),
                            {},
                            "codex",
                            "fixture",
                            root,
                            False,
                            version,
                            root / f"{version}.log",
                        )
                        command = runner.call_args.args[0]
                        start = command.index(expected[0])
                        self.assertEqual(command[start : start + len(expected)], expected)

    def test_install_workflow_uses_native_init_for_unpublished_local_sample(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            candidate = root / "trellis/workflows/guru-team/workflow.md"
            candidate.parent.mkdir(parents=True)
            candidate.write_text("# Local candidate\n", encoding="utf-8")
            installed = target / ".trellis/workflow.md"
            installed.parent.mkdir()
            installed.write_text("# Native\n", encoding="utf-8")
            with mock.patch.object(
                self.matrix, "_workflow_source_requires_local_sample", return_value=True
            ), mock.patch.object(self.matrix, "_run") as runner:
                local_sample = self.matrix._install_workflow(
                    target,
                    ("node", "trellis.js"),
                    {},
                    "codex",
                    "gh:castbox/guru-trellis/trellis#main",
                    root,
                    True,
                    "0.6.17",
                    root / "init.log",
                )
            command = runner.call_args.args[0]
            self.assertTrue(local_sample)
            self.assertEqual(command[command.index("--workflow") + 1], "native")
            self.assertNotIn("--workflow-source", command)
            self.assertEqual(installed.read_text(encoding="utf-8"), "# Local candidate\n")

    def test_local_sample_workflow_switch_uses_exact_local_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            workflow = target / ".trellis/workflow.md"
            workflow.parent.mkdir(parents=True)
            workflow.write_text("# Previous\n", encoding="utf-8")
            previous = root / "previous/trellis/workflows/guru-team/workflow.md"
            previous.parent.mkdir(parents=True)
            previous.write_text("# Previous\n", encoding="utf-8")
            candidate = root / "trellis/workflows/guru-team/workflow.md"
            candidate.parent.mkdir(parents=True)
            candidate.write_text(
                "# Candidate\n<!-- guru-skill-invoke: {} -->\n",
                encoding="utf-8",
            )
            with mock.patch.object(self.matrix, "_run") as runner:
                self.matrix._preview_and_switch_workflow(
                    target,
                    ("node", "trellis.js"),
                    {},
                    "gh:castbox/guru-trellis/trellis#main",
                    root,
                    root / "previous",
                    True,
                    root / "work",
                )
            runner.assert_not_called()
            self.assertEqual(workflow.read_bytes(), candidate.read_bytes())
            self.assertFalse((target / ".trellis/workflow.md.new").exists())
            self.assertFalse((target / ".trellis/workflow.md.bak").exists())

    def test_standalone_shell_env_forwards_full_and_explicit_focused(self) -> None:
        import shutil
        import sys

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shell = root / VERIFIER.relative_to(REPO)
            shell.parent.mkdir(parents=True)
            shutil.copy2(VERIFIER, shell)
            runtime = root / "trellis/skills/guru-team/runtime"
            runtime.mkdir(parents=True)
            (runtime / "bootstrap.py").write_text('print("{}")\n')
            resolver = runtime / "resolve-python.sh"
            resolver.write_text(f'#!/bin/sh\nshift 2\nexec "{sys.executable}" "$@"\n')
            resolver.chmod(0o755)
            helpers = shell.parent / "verify-throwaway-runtime-helpers.sh"
            helpers.write_text(f'source_python() {{ "{sys.executable}" "$@"; }}\nassert_source_runtime_checkpoint() {{ :; }}\n')
            scripts = shell.parent.parent / "python"
            scripts.mkdir()
            (scripts / "verify_throwaway_python_routing.py").write_text('print("{}")\n')
            (scripts / MATRIX_HELPER.name).write_text('import json, sys\nprint(json.dumps(sys.argv[1:]))\n')
            env = {**os.environ, "TRELLIS_FORK_SOURCE": str(root / "target fork"),
                   "TRELLIS_PREDECESSOR_SOURCE": str(root / "before fork"),
                   "TRELLIS_PREDECESSOR_COMMIT": "a" * 40}
            for options, expected_mode, expected_source in (
                ([], "full", env["TRELLIS_FORK_SOURCE"]),
                (["--mode", "focused", "--fork-source", str(root / "explicit fork")], "focused", str(root / "explicit fork")),
            ):
                result = subprocess.run([str(shell), str(root / expected_mode), *options],
                                        env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                argv = json.loads(result.stdout.splitlines()[-1])
                self.assertEqual(argv[0], "run")
                for flag, value in (("--mode", expected_mode), ("--fork-source", expected_source),
                    ("--predecessor-source", env["TRELLIS_PREDECESSOR_SOURCE"]),
                    ("--predecessor-commit", "a" * 40)):
                    self.assertEqual(argv[argv.index(flag) + 1], value)

    def test_focused_mode_passes_exact_command_and_labels_its_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, source = self.fork_fixture(root)
            args = argparse.Namespace(repo_root=repo, fork_source=source, mode="focused",
                work_root=root / "work", platform="codex", workflow_source="fixture", allow_local_sample=False)
            def init(target, command, *unused):
                (target / ".trellis/spec").mkdir(parents=True)
                (target / ".trellis/guru-team").mkdir()
                (target / ".trellis/guru-team/trellis-source.json").write_bytes(
                    (repo / "trellis/presets/guru-team/source/trellis-source.json").read_bytes())
                (target / ".trellis/.version").write_text("0.6.17")
                self.assertEqual(command[1], str(source / "packages/cli/bin/trellis.js"))
                return False
            with mock.patch.object(self.matrix, "_install_workflow", side_effect=init), \
                 mock.patch.object(self.matrix, "_apply_preset", return_value={}), \
                 mock.patch.object(self.matrix, "_assert_template_hashes", return_value={}), \
                 mock.patch.object(self.matrix, "_run", wraps=self.matrix._run) as runner, \
                 mock.patch.object(self.matrix, "_preview_and_switch_workflow"):
                result = self.matrix.run_matrix(args)
            updates = [call.args[0] for call in runner.call_args_list if "update" in call.args[0]]
            self.assertEqual(updates, [(*result["source"]["command"], "update", "--skip-all")] * 2)
            self.assertEqual(result["same_candidate_update_count"], 2)
            self.assertFalse(result["predecessor_upgrade_verified"])
            self.assertFalse(result["full_matrix_verified"])
            self.assertTrue((args.work_root / "focused-summary.json").is_file())

    def create_shallow_before_tag_fixture(
        self,
        root: Path,
        *,
        push_tag: bool = True,
    ) -> tuple[Path, str, str, str, str]:
        remote = root / "origin.git"
        source = root / "source"
        checkout = root / "checkout"
        tag_name = "v0.6.5-guru.10"
        subprocess.run(("git", "init", "--bare", "--quiet", str(remote)), check=True)
        subprocess.run(("git", "init", "--quiet", str(source)), check=True)
        subprocess.run(
            ("git", "config", "user.email", "matrix@example.com"),
            cwd=source,
            check=True,
        )
        subprocess.run(
            ("git", "config", "user.name", "Matrix Test"),
            cwd=source,
            check=True,
        )
        tracked = source / "tracked.txt"
        tracked.write_text("before\n", encoding="utf-8")
        subprocess.run(("git", "add", "tracked.txt"), cwd=source, check=True)
        subprocess.run(
            ("git", "commit", "--quiet", "-m", "before"),
            cwd=source,
            check=True,
        )
        subprocess.run(
            ("git", "tag", "-a", tag_name, "-m", "before tag"),
            cwd=source,
            check=True,
        )
        tag_object = subprocess.run(
            ("git", "rev-parse", tag_name),
            cwd=source,
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        before_commit = subprocess.run(
            ("git", "rev-parse", f"{tag_name}^{{commit}}"),
            cwd=source,
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        tracked.write_text("candidate\n", encoding="utf-8")
        subprocess.run(("git", "add", "tracked.txt"), cwd=source, check=True)
        subprocess.run(
            ("git", "commit", "--quiet", "-m", "candidate"),
            cwd=source,
            check=True,
        )
        candidate = subprocess.run(
            ("git", "rev-parse", "HEAD"),
            cwd=source,
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        subprocess.run(
            ("git", "remote", "add", "origin", str(remote)),
            cwd=source,
            check=True,
        )
        subprocess.run(
            ("git", "push", "--quiet", "origin", "HEAD:refs/heads/main"),
            cwd=source,
            check=True,
        )
        if push_tag:
            subprocess.run(
                ("git", "push", "--quiet", "origin", f"refs/tags/{tag_name}"),
                cwd=source,
                check=True,
            )
        subprocess.run(("git", "init", "--quiet", str(checkout)), check=True)
        subprocess.run(
            ("git", "remote", "add", "origin", str(remote)),
            cwd=checkout,
            check=True,
        )
        subprocess.run(
            ("git", "fetch", "--depth=1", "origin", candidate),
            cwd=checkout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        subprocess.run(
            ("git", "checkout", "--quiet", "--detach", "FETCH_HEAD"),
            cwd=checkout,
            check=True,
        )
        return checkout, tag_name, tag_object, before_commit, candidate

    def one_cell_matrix(self) -> dict[str, object]:
        return {
            "platform_inventory_sha256": "inventory",
            "matrix_sha256": "matrix",
            "cells": [
                {
                    "cell_id": "codex-clean",
                    "platform": "codex",
                    "scenario": "clean",
                }
            ],
        }

    def matrix_args(
        self,
        checkout: Path,
        work_root: Path,
        before_tag: str,
    ) -> argparse.Namespace:
        return argparse.Namespace(
            repo_root=checkout,
            work_root=work_root,
            workflow_source="gh:castbox/guru-trellis/trellis#candidate",
            before_tag=before_tag,
            before_cli="0.6.5",
            target_cli="0.6.15",
            allow_local_sample=False,
            fork_source=checkout,
        )

    def test_default_entry_delegates_to_live_manifest_matrix(self) -> None:
        dispatch = self.text.index(
            'if [[ "$VERIFY_MODE" == full || "$VERIFY_MODE" == focused ]]; then'
        )
        segment = self.text[dispatch:]
        self.assertTrue(segment.rstrip().endswith("exit 0\nfi"))
        self.assertIn('source_python "$COMPATIBILITY_MATRIX_HELPER" "${MATRIX_ARGS[@]}"', segment)
        self.assertIn('--fork-source "$FORK_SOURCE"', segment)
        self.assertIn('--mode "$VERIFY_MODE"', segment)

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

    def test_before_tag_exact_fetch_resolves_identity_and_enters_first_cell(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout, tag_name, tag_object, before_commit, candidate = (
                self.create_shallow_before_tag_fixture(root)
            )
            missing = subprocess.run(
                ("git", "rev-parse", "--verify", f"refs/tags/{tag_name}"),
                cwd=checkout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(missing.returncode, 0)
            with mock.patch.object(
                self.matrix,
                "build_matrix",
                return_value=self.one_cell_matrix(),
            ), mock.patch.object(
                self.matrix,
                "source_state",
                return_value={"head": candidate, "identity_sha256": "source"},
            ), mock.patch.object(
                self.matrix,
                "_run_cell",
                side_effect=self.matrix.MatrixError("sentinel cell failure"),
            ) as run_cell, mock.patch.object(
                self.matrix,
                "_run",
                wraps=self.matrix._run,
            ) as run_command:
                with self.assertRaises(self.matrix.MatrixError) as raised:
                    self.matrix._run_historical_matrix(
                        self.matrix_args(checkout, root / "work", tag_name)
                    )

            fetches = [
                call.args[0]
                for call in run_command.call_args_list
                if call.args and tuple(call.args[0])[:2] == ("git", "fetch")
            ]
            self.assertEqual(
                fetches,
                [
                    (
                        "git",
                        "fetch",
                        "--no-tags",
                        "--depth=1",
                        "origin",
                        f"refs/tags/{tag_name}:refs/tags/{tag_name}",
                    )
                ],
            )
            self.assertEqual(raised.exception.stage, "matrix-cell")
            self.assertEqual(raised.exception.cell_id, "codex-clean")
            run_cell.assert_called_once()
            self.assertEqual(
                subprocess.run(
                    ("git", "rev-parse", f"refs/tags/{tag_name}"),
                    cwd=checkout,
                    text=True,
                    stdout=subprocess.PIPE,
                    check=True,
                ).stdout.strip(),
                tag_object,
            )
            self.assertEqual(
                subprocess.run(
                    ("git", "rev-parse", f"refs/tags/{tag_name}^{{commit}}"),
                    cwd=checkout,
                    text=True,
                    stdout=subprocess.PIPE,
                    check=True,
                ).stdout.strip(),
                before_commit,
            )

    def test_before_tag_local_identity_performs_no_fetch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout, tag_name, tag_object, before_commit, _ = (
                self.create_shallow_before_tag_fixture(root)
            )
            subprocess.run(
                (
                    "git",
                    "fetch",
                    "--no-tags",
                    "--depth=1",
                    "origin",
                    f"refs/tags/{tag_name}:refs/tags/{tag_name}",
                ),
                cwd=checkout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            with mock.patch.object(self.matrix, "_run") as run_command:
                identity = self.matrix.resolve_before_tag(checkout, tag_name)
            run_command.assert_not_called()
            self.assertEqual(
                identity,
                {
                    "before_tag": tag_name,
                    "before_tag_object": tag_object,
                    "before_commit": before_commit,
                    "fetch_performed": False,
                },
            )

    def test_before_tag_existing_noncommit_ref_is_pre_matrix_failure_without_fetch_or_cells(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout, tag_name, _, _, candidate = self.create_shallow_before_tag_fixture(
                root
            )
            blob = subprocess.run(
                ("git", "hash-object", "tracked.txt"),
                cwd=checkout,
                text=True,
                stdout=subprocess.PIPE,
                check=True,
            ).stdout.strip()
            subprocess.run(
                (
                    "git",
                    "-c",
                    "user.name=Matrix Test",
                    "-c",
                    "user.email=matrix@example.com",
                    "tag",
                    "-a",
                    tag_name,
                    blob,
                    "-m",
                    "non-commit before tag",
                ),
                cwd=checkout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            with mock.patch.object(
                self.matrix,
                "build_matrix",
                return_value=self.one_cell_matrix(),
            ), mock.patch.object(
                self.matrix,
                "source_state",
                return_value={"head": candidate, "identity_sha256": "source"},
            ), mock.patch.object(
                self.matrix,
                "_run",
            ) as run_command, mock.patch.object(
                self.matrix,
                "_run_cell",
            ) as run_cell:
                with self.assertRaises(self.matrix.MatrixError) as raised:
                    self.matrix._run_historical_matrix(
                        self.matrix_args(checkout, root / "work", tag_name)
                    )
            failure = self.matrix.matrix_failure_payload(raised.exception)["failure"]
            self.assertEqual(failure["stage"], "pre-matrix")
            self.assertIsNone(failure["cell_id"])
            self.assertIn("not a resolvable commit", str(raised.exception))
            self.assertIn("expected commit type", failure["error_tail"])
            run_command.assert_not_called()
            run_cell.assert_not_called()
            self.assertEqual(list((root / "work").iterdir()), [])

    def test_before_tag_missing_remote_is_pre_matrix_failure_with_zero_cells(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout, tag_name, _, _, candidate = self.create_shallow_before_tag_fixture(
                root,
                push_tag=False,
            )
            with mock.patch.object(
                self.matrix,
                "build_matrix",
                return_value=self.one_cell_matrix(),
            ), mock.patch.object(
                self.matrix,
                "source_state",
                return_value={"head": candidate, "identity_sha256": "source"},
            ), mock.patch.object(self.matrix, "_run_cell") as run_cell:
                with self.assertRaises(self.matrix.MatrixError) as raised:
                    self.matrix._run_historical_matrix(
                        self.matrix_args(checkout, root / "work", tag_name)
                    )
            failure = self.matrix.matrix_failure_payload(raised.exception)["failure"]
            self.assertEqual(failure["stage"], "pre-matrix")
            self.assertIsNone(failure["cell_id"])
            run_cell.assert_not_called()
            self.assertEqual(list((root / "work").iterdir()), [])

    def test_malformed_before_tag_is_pre_matrix_failure_without_fetch_or_cells(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "checkout"
            checkout.mkdir()
            with mock.patch.object(
                self.matrix,
                "build_matrix",
                return_value=self.one_cell_matrix(),
            ), mock.patch.object(
                self.matrix,
                "source_state",
                return_value={"head": "a" * 40, "identity_sha256": "source"},
            ), mock.patch.object(self.matrix, "_run") as run_command, mock.patch.object(
                self.matrix,
                "_run_cell",
            ) as run_cell:
                with self.assertRaises(self.matrix.MatrixError) as raised:
                    self.matrix._run_historical_matrix(
                        self.matrix_args(checkout, root / "work", "../bad^{commit}")
                    )
            failure = self.matrix.matrix_failure_payload(raised.exception)["failure"]
            self.assertEqual(failure["stage"], "pre-matrix")
            self.assertIsNone(failure["cell_id"])
            run_command.assert_not_called()
            run_cell.assert_not_called()
            self.assertEqual(list((root / "work").iterdir()), [])

    def test_matrix_executor_uses_exact_upgrade_and_conditional_migrate(self) -> None:
        dry_run = self.matrix_text.index('(*binary, "update", "--dry-run")')
        conditional = self.matrix_text.index(
            "if _dry_run_requires_retirement_migration(dry_run):", dry_run
        )
        migrate = self.matrix_text.index(
            '"--force",\n                    "--migrate",\n                    "--assignee",', conditional
        )
        normal = self.matrix_text.index(
            '(*binary, "update", "--skip-all")', migrate
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
        self.assertNotIn('"upgrade", "--tag"', self.matrix_text)
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
            workflow_function.index('"--force"'),
        )
        self.assertNotIn('input_text="y\\n"', workflow_function)
        self.assertNotIn('"latest"', self.matrix_text)

    def test_managed_workflow_preview_and_force_switch_are_content_bound(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target, current, previous, work = (
                root / "target", root / "current", root / "previous", root / "work"
            )
            workflow = target / ".trellis/workflow.md"
            candidate = current / "trellis/workflows/guru-team/workflow.md"
            before = previous / "trellis/workflows/guru-team/workflow.md"
            for path, value in ((workflow, "before\n"), (before, "before\n"), (candidate, "candidate\n")):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(value, encoding="utf-8")
            work.mkdir()
            calls: list[tuple[str, ...]] = []

            def fake_run(argv, **kwargs):
                args = tuple(str(value) for value in argv)
                calls.append(args)
                if "--create-new" in args:
                    Path(str(workflow) + ".new").write_text("candidate\n", encoding="utf-8")
                elif "--force" in args:
                    workflow.write_text("candidate\n", encoding="utf-8")
                return ""

            with mock.patch.object(self.matrix, "_run", side_effect=fake_run):
                self.matrix._preview_and_switch_workflow(
                    target, ("node", "/fixture/bin/trellis.js"), {}, "gh:example/workflows#candidate",
                    current, previous, False, work,
                )
            self.assertEqual(workflow.read_text(), "candidate\n")
            self.assertIn("--create-new", calls[0])
            self.assertIn("--force", calls[1])
            self.assertFalse(Path(str(workflow) + ".new").exists())

    def test_workflow_switch_preserves_user_edits_and_existing_sidecars(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target, current, previous = root / "target", root / "current", root / "previous"
            workflow = target / ".trellis/workflow.md"
            candidate = current / "trellis/workflows/guru-team/workflow.md"
            before = previous / "trellis/workflows/guru-team/workflow.md"
            for path, value in ((workflow, "user edit\n"), (before, "managed\n"), (candidate, "candidate\n")):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(value, encoding="utf-8")
            with mock.patch.object(self.matrix, "_run") as runner:
                with self.assertRaisesRegex(self.matrix.MatrixError, "not the expected managed"):
                    self.matrix._preview_and_switch_workflow(
                        target, ("node", "/fixture/bin/trellis.js"), {}, "source", current, previous, False, root,
                    )
                runner.assert_not_called()
            self.assertEqual(workflow.read_text(), "user edit\n")

            workflow.write_text("managed\n", encoding="utf-8")
            sidecar = Path(str(workflow) + ".new")
            sidecar.write_text("unresolved\n", encoding="utf-8")
            with mock.patch.object(self.matrix, "_run") as runner:
                with self.assertRaisesRegex(self.matrix.MatrixError, "unresolved"):
                    self.matrix._preview_and_switch_workflow(
                        target, ("node", "/fixture/bin/trellis.js"), {}, "source", current, previous, False, root,
                    )
                runner.assert_not_called()
            self.assertEqual(sidecar.read_text(), "unresolved\n")

    def test_workflow_switch_preserves_dangling_new_and_backup_symlinks(self) -> None:
        for suffix in (".new", ".bak"):
            with self.subTest(sidecar=suffix), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                target, current, previous = (
                    root / "target",
                    root / "current",
                    root / "previous",
                )
                workflow = target / ".trellis/workflow.md"
                candidate = current / "trellis/workflows/guru-team/workflow.md"
                before = previous / "trellis/workflows/guru-team/workflow.md"
                for path in (workflow, candidate, before):
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("managed\n", encoding="utf-8")
                sidecar = Path(str(workflow) + suffix)
                dangling_target = root / f"missing{suffix}"
                sidecar.symlink_to(dangling_target)

                self.assertTrue(sidecar.is_symlink())
                self.assertFalse(sidecar.exists())
                with mock.patch.object(self.matrix, "_run") as runner:
                    with self.assertRaisesRegex(self.matrix.MatrixError, "unresolved"):
                        self.matrix._preview_and_switch_workflow(
                            target,
                            ("node", "/fixture/bin/trellis.js"),
                            {},
                            "source",
                            current,
                            previous,
                            False,
                            root,
                        )
                    runner.assert_not_called()
                self.assertTrue(sidecar.is_symlink())
                self.assertEqual(sidecar.readlink(), dangling_target)

    def test_workflow_switch_retains_bad_preview_and_primary_switch_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target, current, previous = root / "target", root / "current", root / "previous"
            workflow = target / ".trellis/workflow.md"
            candidate = current / "trellis/workflows/guru-team/workflow.md"
            before = previous / "trellis/workflows/guru-team/workflow.md"
            for path, value in ((workflow, "managed\n"), (before, "managed\n"), (candidate, "candidate\n")):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(value, encoding="utf-8")

            def mismatched_preview(argv, **kwargs):
                Path(str(workflow) + ".new").write_text("other\n", encoding="utf-8")
                return ""

            with mock.patch.object(self.matrix, "_run", side_effect=mismatched_preview):
                with self.assertRaisesRegex(self.matrix.MatrixError, "does not match"):
                    self.matrix._preview_and_switch_workflow(
                        target, ("node", "/fixture/bin/trellis.js"), {}, "source", current, previous, False, root,
                    )
            self.assertEqual(Path(str(workflow) + ".new").read_text(), "other\n")

            Path(str(workflow) + ".new").unlink()
            calls = 0

            def failing_switch(argv, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 1:
                    Path(str(workflow) + ".new").write_text("candidate\n", encoding="utf-8")
                    return ""
                raise self.matrix.MatrixError("primary workflow switch failure")

            with mock.patch.object(self.matrix, "_run", side_effect=failing_switch):
                with self.assertRaisesRegex(self.matrix.MatrixError, "primary workflow switch failure"):
                    self.matrix._preview_and_switch_workflow(
                        target, ("node", "/fixture/bin/trellis.js"), {}, "source", current, previous, False, root,
                    )

    def test_matrix_retains_legacy_representative_and_runs_parallel_finish(self) -> None:
        run_matrix = self.matrix_text[self.matrix_text.index("def run_matrix(") :]
        self.assertIn('verify_installed_parallel_finish.py', run_matrix)
        self.assertIn('parallel_finish.get("status") != "passed"', run_matrix)
        self.assertIn('legacy_representative = work_root.parent / "project"', run_matrix)
        self.assertIn('"representative_root": "project"', run_matrix)
        self.assertIn('"external_boundaries"', run_matrix)

    def test_matrix_failure_projection_is_bounded_structured_and_secret_safe(self) -> None:
        failure = self.matrix.MatrixError(
            "cell command failed",
            stage="matrix-cell",
            cell_id="codex-clean",
            command_label="run-skill-evals.sh",
            exit_code=17,
            error_tail=(
                "prefix\nhttps://user:password@example.com/repo.git\n"
                "github_pat_SECRET\nAuthorization: Bearer bearer-secret\n"
                "GITHUB_TOKEN=environment-secret\n"
                "https://example.com/object?X-Amz-Signature=signed-secret\n"
                "https://example.com/object?X-Amz-Credential=aws-access-id%2Fscope\n"
                "https://example.com/object?X-Goog-Credential=gcp-access-id%2Fscope\n"
                "-----BEGIN PRIVATE KEY-----\nprivate-secret\n"
                "-----END PRIVATE KEY-----\n"
                + ("x" * 3000)
            ),
        )
        payload = self.matrix.matrix_failure_payload(failure)
        self.assertEqual(payload["status"], "failed")
        self.assertEqual(payload["failure"]["stage"], "matrix-cell")
        self.assertEqual(payload["failure"]["cell_id"], "codex-clean")
        self.assertEqual(payload["failure"]["command_label"], "run-skill-evals.sh")
        self.assertEqual(payload["failure"]["exit_code"], 17)
        self.assertLessEqual(len(payload["failure"]["error_tail"]), 2000)
        serialized = json.dumps(payload)
        self.assertNotIn("github_pat_SECRET", serialized)
        self.assertNotIn("user:password", serialized)
        self.assertNotIn("bearer-secret", serialized)
        self.assertNotIn("environment-secret", serialized)
        self.assertNotIn("signed-secret", serialized)
        self.assertNotIn("aws-access-id", serialized)
        self.assertNotIn("gcp-access-id", serialized)
        self.assertNotIn("private-secret", serialized)

    def test_matrix_command_label_uses_the_invoked_helper_not_temporary_paths(self) -> None:
        self.assertEqual(
            self.matrix._stable_command_label(
                (
                    "/tmp/project/.trellis/guru-team/runtime/resolve-python.sh",
                    "/tmp/project",
                    "/tmp/project/.trellis/guru-team/runtime",
                    "/source/verify_installed_closeout.py",
                    "--repo",
                    "/tmp/project",
                )
            ),
            "verify_installed_closeout.py",
        )
        self.assertEqual(
            self.matrix._stable_command_label(("python3", "-m", "unittest")),
            "python3",
        )

    def test_matrix_run_reports_bounded_timeout_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as directory, mock.patch.dict(
            os.environ, {"GURU_MATRIX_COMMAND_TIMEOUT_SECONDS": "0.01"}
        ), mock.patch.object(
            self.matrix.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired(("sleep", "1"), 0.01, output="partial"),
        ):
            with self.assertRaises(self.matrix.MatrixError) as raised:
                self.matrix._run(("sleep", "1"), cwd=Path(directory))
        self.assertIn("command timed out after 0.010s", str(raised.exception))
        self.assertEqual(raised.exception.command_label, "sleep")
        self.assertEqual(raised.exception.exit_code, 124)
        self.assertIn("partial", raised.exception.error_tail)

    def test_matrix_failure_context_distinguishes_pre_cell_and_post_stages(self) -> None:
        pre = self.matrix.matrix_failure_payload(self.matrix.MatrixError("pre"))
        self.assertEqual(pre["failure"]["stage"], "pre-matrix")
        self.assertIsNone(pre["failure"]["cell_id"])

        cell = self.matrix.MatrixError(
            "command failed",
            command_label="git",
            exit_code=9,
            error_tail="failed",
        ).with_context("matrix-cell", "cursor-existing")
        projected_cell = self.matrix.matrix_failure_payload(cell)
        self.assertEqual(projected_cell["failure"]["stage"], "matrix-cell")
        self.assertEqual(projected_cell["failure"]["cell_id"], "cursor-existing")

        post = cell.with_context("post-matrix", None)
        projected_post = self.matrix.matrix_failure_payload(post)
        self.assertEqual(projected_post["failure"]["stage"], "post-matrix")
        self.assertIsNone(projected_post["failure"]["cell_id"])

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

    def test_python_matrix_runs_installed_smokes_through_target_resolver(self) -> None:
        target, source, work = Path("/fixture/target"), Path("/fixture/source"), Path("/fixture/work")
        def load(path):
            if path.name == "evals.json":
                return {"evals": [{"input_profile_id": "normal"}]}
            return {"public_contracts": {"input": {"profiles": [{"id": "normal"}]}}}
        def run(argv, **kwargs):
            if Path(argv[0]).name == "run-skill-evals.sh":
                return json.dumps({"status": "passed", "cases": [{}]})
            if any(
                Path(str(part)).name == "verify_installed_task_workspace.py"
                for part in argv
            ):
                return json.dumps({
                    "status": "ok",
                    "legacy_preserved": True,
                    "lifecycle_outcome_sha256": "a" * 64,
                })
            return json.dumps({"status": "ok"})
        for scenario, closeout_case in (("clean", "initial"), ("existing", "after-update")):
            with self.subTest(scenario=scenario), \
                 mock.patch.object(self.matrix, "_load_json", side_effect=load), \
                 mock.patch.object(
                     self.matrix,
                     "_prepare_clean_candidate_source",
                     return_value=source,
                 ) as prepare_clean, \
                 mock.patch.object(self.matrix, "_apply_preset") as apply_clean, \
                 mock.patch.object(self.matrix, "_run", side_effect=run) as invoked:
                result = self.matrix._run_installed_smokes(target, source, work, scenario, "codex")
                prepare_clean.assert_called_once_with(
                    source, work / "clean-candidate-source"
                )
                apply_clean.assert_called_once_with(
                    source,
                    target,
                    "codex",
                    work / "preset-clean-provenance.log",
                )
                self.assertEqual(result["runtime_smokes"], [
                    "closeout",
                    "phase0",
                    "task_workspace_absent",
                    "task_workspace_present_a",
                    "task_workspace_present_b",
                ])
                self.assertEqual(result["legacy_workspace_outcome_sha256"], "a" * 64)
                calls = [call.args[0] for call in invoked.call_args_list
                         if Path(call.args[0][0]).name == "resolve-python.sh"]
                self.assertEqual(len(calls), 5)
                for argv in calls:
                    self.assertEqual(argv[:3], (str(target / ".trellis/guru-team/runtime/resolve-python.sh"),
                                               str(target), str(target / ".trellis/guru-team/runtime")))
                self.assertEqual(Path(calls[0][3]).name, "verify_installed_closeout.py")
                self.assertEqual(calls[0][calls[0].index("--case") + 1], closeout_case)

    def test_capability_projection_is_compact_and_complete(self) -> None:
        projection = self.matrix.capability_projection(REPO)

        self.assertRegex(projection["projection_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(len(projection["skill_api"]["interfaces"]), 23)
        self.assertEqual(len(projection["workflow"]["skill_invokes"]), 22)
        self.assertEqual(len(projection["workflow"]["skill_exits"]), 95)
        self.assertEqual(len(projection["workflow"]["workflow_targets"]), 35)
        self.assertEqual(len(projection["workflow"]["stop_targets"]), 24)
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
        self.assertEqual(version_only["additive_differences"], [])

        after = json.loads(json.dumps(before))
        after["workflow"]["skill_invokes"].append(
            '{"required":true,"skill":"guru-new-capability"}'
        )
        additive = self.matrix.compare_capabilities(before, after)
        self.assertTrue(additive["capabilities_preserved"])
        self.assertEqual(additive["blocking_differences"], [])
        self.assertEqual(
            additive["additive_differences"],
            [
                {
                    "group": "workflow",
                    "added": {
                        "skill_invokes": [
                            '{"required":true,"skill":"guru-new-capability"}'
                        ]
                    },
                }
            ],
        )

        after = json.loads(json.dumps(before))
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
        self.assertTrue(identity_drift["capabilities_preserved"])
        self.assertEqual(identity_drift["blocking_differences"], [])
        self.assertEqual(
            identity_drift["extension_identity"],
            {
                "before": {"extension_id": before["extension"]["extension_id"]},
                "after": {"extension_id": "guru-team-drifted"},
                "consistent": False,
            },
        )

        after = json.loads(json.dumps(before))
        after["distribution"]["skill_package_files_and_modes"] = after[
            "distribution"
        ]["skill_package_files_and_modes"][1:]
        projection_change = self.matrix.compare_capabilities(before, after)
        self.assertTrue(projection_change["capabilities_preserved"])
        self.assertEqual(projection_change["blocking_differences"], [])

        after = json.loads(json.dumps(before))
        after["skill_api"]["typed_output_schema_ids"] = []
        api_projection_change = self.matrix.compare_capabilities(before, after)
        self.assertTrue(api_projection_change["capabilities_preserved"])
        self.assertEqual(api_projection_change["blocking_differences"], [])

    def test_source_and_installed_consumers_block_identity_drift_independently(self) -> None:
        before = self.matrix.capability_projection(REPO)
        after = json.loads(json.dumps(before))
        after["extension"]["extension_id"] = "guru-team-drifted"
        comparison = self.matrix.compare_capabilities(before, after)

        self.assertTrue(comparison["capabilities_preserved"])
        self.assertFalse(comparison["extension_identity"]["consistent"])
        for projection_name in ("source", "installed"):
            with self.subTest(projection=projection_name), self.assertRaisesRegex(
                self.matrix.MatrixError,
                rf"^{projection_name} extension identity changed:",
            ):
                self.matrix._assert_projection_consistency(
                    comparison, projection_name
                )

        self.assertIn(
            '_assert_projection_consistency(comparison, "source")',
            self.matrix_text,
        )
        self.assertIn(
            '_assert_projection_consistency(installed_comparison, "installed")',
            self.matrix_text,
        )

    def test_installed_projection_and_template_hash_classification_are_current(self) -> None:
        installed = self.matrix.installed_capability_projection(REPO)
        comparison = self.matrix.compare_capabilities(installed, installed)
        template_hashes = self.matrix._assert_template_hashes(REPO, REPO)

        self.assertTrue(comparison["capabilities_preserved"])
        self.assertEqual(len(installed["skill_api"]["interfaces"]), 23)
        self.assertEqual(installed["distribution"]["platforms"], ["claude", "codex", "cursor"])
        self.assertEqual(template_hashes["unknown_drift_count"], 0)
        self.assertGreater(template_hashes["entry_count"], 0)

    def test_arbitrary_agents_edits_fail_hash_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / "source", Path(directory) / "target"
            for root in (source, target):
                (root / ".trellis").mkdir(parents=True)
                (root / "AGENTS.md").write_text("official\n")
                (root / ".trellis/.template-hashes.json").write_text(json.dumps({
                    "__version": 2, "hashes": {
                        "AGENTS.md": hashlib.sha256(b"official\n").hexdigest()
                    }
                }))
            self.matrix._assert_template_hashes(target, source)
            (target / "AGENTS.md").write_text("unrelated local edit\n")
            with self.assertRaisesRegex(self.matrix.MatrixError, "AGENTS.md"):
                self.matrix._assert_template_hashes(target, source)

    def test_agents_preset_delta_requires_original_hash_and_exact_block(self) -> None:
        import apply_guru_team_trellis_preset as preset

        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / "source", Path(directory) / "target"
            original = b"official\n"
            for root in (source, target):
                (root / ".trellis").mkdir(parents=True)
                (root / "AGENTS.md").write_bytes(original)
                (root / ".trellis/.template-hashes.json").write_text(json.dumps({
                    "__version": 2, "hashes": {"AGENTS.md": hashlib.sha256(original).hexdigest()},
                }))
            projected = original + b"\n" + preset.AGENTS_AI_FIRST_BLOCK.encode("utf-8")
            (target / "AGENTS.md").write_bytes(projected)
            result = self.matrix._assert_template_hashes(target, source)
            self.assertEqual(result["known_preset_projection_paths"], ["AGENTS.md"])
            for changed in (b"other\n" + projected, projected + b"extra\n", projected.replace(b"AI-first", b"AI-first-edited", 1)):
                (target / "AGENTS.md").write_bytes(changed)
                with self.assertRaisesRegex(self.matrix.MatrixError, "AGENTS.md"):
                    self.matrix._assert_template_hashes(target, source)

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
                "    print(json.dumps({'status':'conflict','new_copies':[],'managed_backups':[],"
                "'skill_packages':{'sidecars':[relative.as_posix()+'.bak']},'overlays':{'sidecars':[]}}))\n"
                "    raise SystemExit(2)\n"
                "print(json.dumps({'status':'ok','new_copies':[],'managed_backups':[],"
                "'skill_packages':{'sidecars':[]},'overlays':{'sidecars':[]}}))\n"
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

    def test_existing_preset_reapply_reconciles_all_declared_backup_owners(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            previous = root / "previous"
            target = root / "target"
            relatives = {
                "managed": Path(".trellis/guru-team/scripts/python/value.py"),
                "skill": Path(".agents/skills/guru-example/SKILL.md"),
                "overlay": Path(".codex/prompts/guru-example.md"),
            }
            for relative in relatives.values():
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
            serialized = {key: value.as_posix() for key, value in relatives.items()}
            installer.write_text(
                "import json,sys\n"
                "from pathlib import Path\n"
                "repo=Path(sys.argv[sys.argv.index('--repo')+1])\n"
                f"relatives={serialized!r}\n"
                "paths={key:Path(value) for key,value in relatives.items()}\n"
                "if (repo/paths['managed']).read_text() == 'before\\n':\n"
                "    for relative in paths.values():\n"
                "        current=repo/relative\n"
                "        Path(str(current)+'.bak').write_bytes(current.read_bytes())\n"
                "        current.write_text('candidate\\n')\n"
                "    print(json.dumps({\n"
                "        'status':'conflict',\n"
                "        'new_copies':[],\n"
                "        'managed_backups':[paths['managed'].as_posix()+'.bak'],\n"
                "        'skill_packages':{'sidecars':[paths['skill'].as_posix()+'.bak']},\n"
                "        'overlays':{'sidecars':[paths['overlay'].as_posix()+'.bak']},\n"
                "    }))\n"
                "    raise SystemExit(2)\n"
                "print(json.dumps({\n"
                "    'status':'ok',\n"
                "    'new_copies':[],\n"
                "    'managed_backups':[],\n"
                "    'skill_packages':{'sidecars':[]},\n"
                "    'overlays':{'sidecars':[]},\n"
                "}))\n"
            )

            result = self.matrix._apply_preset(
                source,
                target,
                "claude",
                root / "preset.log",
                previous_root=previous,
            )

            expected = sorted(
                relative.as_posix() + ".bak" for relative in relatives.values()
            )
            self.assertEqual(result["status"], "passed")
            self.assertEqual(result["reconciled_backups"], expected)
            for relative in relatives.values():
                self.assertEqual((target / relative).read_text(), "candidate\n")
                self.assertFalse(Path(str(target / relative) + ".bak").exists())

    def test_existing_preset_reapply_preserves_declared_new_copy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            previous = root / "previous"
            target = root / "target"
            relative = Path(".trellis/workflow.md")
            for base in (source, previous, target):
                path = base / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("before\n")
            installer = (
                source
                / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"
            )
            installer.parent.mkdir(parents=True, exist_ok=True)
            invocation_count = root / "invocation-count"
            installer.write_text(
                "import json,sys\n"
                "from pathlib import Path\n"
                "repo=Path(sys.argv[sys.argv.index('--repo')+1])\n"
                f"relative=Path({relative.as_posix()!r})\n"
                f"count=Path({str(invocation_count)!r})\n"
                "count.write_text(str(int(count.read_text())+1) if count.exists() else '1')\n"
                "new_copy=Path(str(repo/relative)+'.new')\n"
                "new_copy.write_text('candidate\\n')\n"
                "print(json.dumps({\n"
                "    'status':'conflict',\n"
                "    'new_copies':[relative.as_posix()+'.new'],\n"
                "    'managed_backups':[],\n"
                "    'skill_packages':{'sidecars':[]},\n"
                "    'overlays':{'sidecars':[]},\n"
                "}))\n"
                "raise SystemExit(2)\n"
            )

            with self.assertRaisesRegex(
                self.matrix.MatrixError, "unexpected preset migration sidecar"
            ):
                self.matrix._apply_preset(
                    source,
                    target,
                    "claude",
                    root / "preset.log",
                    previous_root=previous,
                )

            self.assertEqual(invocation_count.read_text(), "1")
            self.assertEqual(Path(str(target / relative) + ".new").read_text(), "candidate\n")

    def test_preset_subprocess_failure_preserves_command_and_exit_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            target = root / "target"
            installer = (
                source
                / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"
            )
            installer.parent.mkdir(parents=True)
            installer.write_text(
                "import json\n"
                "print(json.dumps({'status': 'failed'}))\n"
                "raise SystemExit(9)\n",
                encoding="utf-8",
            )

            with self.assertRaises(self.matrix.MatrixError) as raised:
                self.matrix._apply_preset(
                    source,
                    target,
                    "codex",
                    root / "preset.log",
                )

            self.assertEqual(
                raised.exception.command_label,
                "apply_guru_team_trellis_preset.py",
            )
            self.assertEqual(raised.exception.exit_code, 9)
            self.assertIn('"status": "failed"', raised.exception.error_tail)

    def test_cli_install_and_upgrade_stay_in_disposable_prefix(self) -> None:
        self.assertNotIn('npm install', self.text)
        self.assertNotIn('trellis upgrade --tag', self.text)
        self.assertNotIn("trellis()", self.text)
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run((str(VERIFIER), directory), capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--fork-source is required", result.stderr)

    def test_finish_work_compatibility_wrapper_exposes_shared_runtime(self) -> None:
        wrapper = FINISH_WORK_WRAPPER.read_text(encoding="utf-8")
        self.assertIn(
            'export PYTHONPATH="$RUNTIME:$GURU_ROOT${PYTHONPATH:+:$PYTHONPATH}"',
            wrapper,
        )
        self.assertIn('"$RUNTIME/legacy.py" finish-work "$@"', wrapper)


if __name__ == "__main__":
    unittest.main()
