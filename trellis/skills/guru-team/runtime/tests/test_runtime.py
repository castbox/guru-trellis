from __future__ import annotations

import ast
import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import sys
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runtime.validate import _package_paths


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT.parent
def bootstrap_runtime(repo: Path, runtime_assets: Path = ROOT) -> dict[str, object]:
    result = subprocess.run(
        [
            sys.executable,
            str(runtime_assets / "bootstrap.py"),
            "--repo",
            str(repo),
            "--runtime-assets",
            str(runtime_assets),
            "--python",
            sys.executable,
            "--json",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result)
    return json.loads(result.stdout)


def copy_active_runtime(repo: Path) -> None:
    bootstrap_runtime(repo)


class SharedRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cache = tempfile.TemporaryDirectory()
        cls.repo_directory = tempfile.TemporaryDirectory()
        cls.repo = Path(cls.repo_directory.name) / "repo"
        cls.repo.mkdir()
        cls.cache_environment = mock.patch.dict(
            os.environ,
            {"GURU_TEAM_PYTHON_CACHE_ROOT": cls.cache.name},
        )
        cls.cache_environment.start()
        cls.runtime_result = bootstrap_runtime(cls.repo)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.cache_environment.stop()
        cls.repo_directory.cleanup()
        cls.cache.cleanup()

    def test_managed_runtime_reuses_same_identity_and_probes_draft_2020_12(self) -> None:
        self.assertEqual(self.runtime_result["status"], "ok")
        self.assertIn(self.runtime_result["action"], {"installed", "reused", "repaired"})
        second = bootstrap_runtime(self.repo)
        self.assertEqual(second["action"], "reused")
        self.assertEqual(second["runtime_identity"], self.runtime_result["runtime_identity"])

        from runtime.bootstrap import active_pointer_path

        active = json.loads(active_pointer_path(self.repo).read_text())
        managed_python = Path(str(self.runtime_result["interpreter"]))
        self.assertEqual(active["cache_scope"], "user")
        self.assertEqual(active["runtime_id"], self.runtime_result["runtime_identity"])
        probe = subprocess.run(
            [str(managed_python), str(ROOT / "probe.py"), "--manifest", str(ROOT / "python-runtime.json"), "--json"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(probe.returncode, 0, probe)
        self.assertEqual(json.loads(probe.stdout)["draft"], "2020-12")

    def test_lock_change_changes_runtime_identity(self) -> None:
        from runtime.bootstrap import runtime_identity

        with tempfile.TemporaryDirectory() as tmp:
            assets = Path(tmp)
            shutil.copy2(ROOT / "python-runtime.json", assets / "python-runtime.json")
            shutil.copy2(ROOT / "requirements.lock", assets / "requirements.lock")
            original, _ = runtime_identity(assets, Path(sys.executable))
            with (assets / "requirements.lock").open("a", encoding="utf-8") as handle:
                handle.write("\n# identity drift\n")
            changed, _ = runtime_identity(assets, Path(sys.executable))
        self.assertNotEqual(original, changed)

    def test_runtime_identity_binds_platform_architecture_and_abi(self) -> None:
        from runtime.bootstrap import runtime_identity

        _, identity = runtime_identity(ROOT, Path(sys.executable))
        self.assertEqual(
            {
                "os_name",
                "machine",
                "python_abi_tag",
                "python_platform_tag",
            },
            set(identity) & {
                "os_name",
                "machine",
                "python_abi_tag",
                "python_platform_tag",
            },
        )
        self.assertTrue(all(identity[key] for key in ("os_name", "machine", "python_abi_tag", "python_platform_tag")))

    def test_user_cache_root_follows_supported_os_conventions(self) -> None:
        from runtime.bootstrap import user_cache_root

        home = Path("/Users/example")
        self.assertEqual(
            user_cache_root({}, system_name="Darwin", home=home),
            home / "Library/Caches/guru-team/python",
        )
        self.assertEqual(
            user_cache_root({}, system_name="Linux", home=Path("/home/example")),
            Path("/home/example/.cache/guru-team/python"),
        )
        self.assertEqual(
            user_cache_root({"XDG_CACHE_HOME": "/cache"}, system_name="Linux", home=Path("/home/example")),
            Path("/cache/guru-team/python"),
        )
        self.assertEqual(
            user_cache_root({"LOCALAPPDATA": "C:/Local"}, system_name="Windows", home=Path("C:/Users/example")),
            Path("C:/Local/GuruTeam/python"),
        )

    def test_different_repositories_reuse_same_immutable_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first_repo = Path(tmp) / "first"
            second_repo = Path(tmp) / "second"
            first_repo.mkdir()
            second_repo.mkdir()
            first = bootstrap_runtime(first_repo)
            second = bootstrap_runtime(second_repo)
            self.assertEqual(first["runtime_identity"], second["runtime_identity"])
            self.assertEqual(first["interpreter"], second["interpreter"])
            self.assertEqual(second["action"], "reused")

    def test_damaged_managed_runtime_is_repaired(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(
            os.environ,
            {"GURU_TEAM_PYTHON_CACHE_ROOT": str(Path(tmp) / "cache")},
        ):
            repo = Path(tmp) / "repo"
            repo.mkdir()
            installed = bootstrap_runtime(repo)
            damaged_python = Path(str(installed["interpreter"]))
            damaged_python.unlink()
            repaired = bootstrap_runtime(repo)
            self.assertEqual(repaired["action"], "repaired")
            self.assertEqual(repaired["runtime_identity"], installed["runtime_identity"])
            self.assertTrue(damaged_python.is_file())

    def test_failed_candidate_preserves_active_runtime(self) -> None:
        from runtime import bootstrap as managed

        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(
            os.environ,
            {"GURU_TEAM_PYTHON_CACHE_ROOT": str(Path(tmp) / "cache")},
        ):
            repo = Path(tmp) / "repo"
            repo.mkdir()
            pointer = managed.active_pointer_path(repo)
            pointer.parent.mkdir(parents=True)
            pointer.write_text("prior\n")
            before = pointer.read_bytes()
            runtime_root = managed.user_cache_root()
            real_run = managed.subprocess.run

            def fail_venv(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
                if argv[1:3] == ["-m", "venv"]:
                    return subprocess.CompletedProcess(argv, 1, "", "failed")
                return real_run(argv, **kwargs)

            with mock.patch.object(managed.subprocess, "run", side_effect=fail_venv):
                with self.assertRaises(managed.BootstrapError):
                    managed.bootstrap(repo, ROOT, Path(sys.executable))
            self.assertEqual(pointer.read_bytes(), before)
            self.assertEqual(list(runtime_root.glob(".*.candidate-*")), [])

    def test_failed_hash_locked_install_preserves_active_runtime(self) -> None:
        from runtime import bootstrap as managed

        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(
            os.environ,
            {"GURU_TEAM_PYTHON_CACHE_ROOT": str(Path(tmp) / "cache")},
        ):
            repo = Path(tmp) / "repo"
            repo.mkdir()
            pointer = managed.active_pointer_path(repo)
            pointer.parent.mkdir(parents=True)
            pointer.write_text("prior\n")
            before = pointer.read_bytes()
            runtime_root = managed.user_cache_root()
            real_run = managed.subprocess.run

            def fail_install(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
                if argv[1:3] == ["-m", "venv"]:
                    venv_dir = Path(argv[3])
                    python = managed.venv_python(venv_dir)
                    python.parent.mkdir(parents=True)
                    shutil.copy2(sys.executable, python)
                    python.chmod(0o755)
                    return subprocess.CompletedProcess(argv, 0, "", "")
                if argv[1:4] == ["-m", "pip", "--version"]:
                    return subprocess.CompletedProcess(argv, 0, "pip test", "")
                if argv[1:3] == ["-m", "pip"] and "install" in argv:
                    return subprocess.CompletedProcess(argv, 1, "", "network unavailable")
                return real_run(argv, **kwargs)

            with mock.patch.object(managed.subprocess, "run", side_effect=fail_install):
                with self.assertRaisesRegex(managed.BootstrapError, "hash-locked"):
                    managed.bootstrap(repo, ROOT, Path(sys.executable))
            self.assertEqual(pointer.read_bytes(), before)
            self.assertEqual(list(runtime_root.glob(".*.candidate-*")), [])

    def test_prepared_new_identity_preserves_active_until_explicit_activation(self) -> None:
        from runtime import bootstrap as managed

        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(
            os.environ,
            {"GURU_TEAM_PYTHON_CACHE_ROOT": str(Path(tmp) / "cache")},
        ):
            repo = Path(tmp) / "repo"
            assets = Path(tmp) / "assets"
            repo.mkdir()
            shutil.copytree(ROOT, assets)
            first = managed.bootstrap(repo, assets, Path(sys.executable))
            active_path = managed.active_pointer_path(repo)
            before = active_path.read_bytes()
            with (assets / "requirements.lock").open("a", encoding="utf-8") as handle:
                handle.write("\n# staged identity change\n")
            prepared = managed.bootstrap(repo, assets, Path(sys.executable), activate=False)
            self.assertNotEqual(prepared["runtime_identity"], first["runtime_identity"])
            self.assertEqual(active_path.read_bytes(), before)
            activated = managed.bootstrap(repo, assets, Path(sys.executable), activate=True)
            self.assertEqual(activated["action"], "reused")
            self.assertEqual(activated["runtime_identity"], prepared["runtime_identity"])
            self.assertNotEqual(active_path.read_bytes(), before)

    def test_bootstrap_failure_reports_computed_runtime_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shim = root / "python"
            shim.write_text(
                "#!/bin/sh\n"
                "if [ \"$1\" = \"-c\" ]; then\n"
                "  echo '{\"implementation\":\"CPython\",\"major\":3,\"minor\":12,\"os_name\":\"TestOS\",\"machine\":\"test-arch\",\"abi_tag\":\"cpython-312\",\"platform_tag\":\"test-platform\"}'\n"
                "  exit 0\n"
                "fi\n"
                "exit 1\n",
                encoding="utf-8",
            )
            shim.chmod(0o755)
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "bootstrap.py"),
                    "--repo",
                    str(root),
                    "--runtime-assets",
                    str(ROOT),
                    "--python",
                    str(shim),
                    "--json",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertRegex(payload["runtime_identity"], r"^[0-9a-f]{24}$")

    def test_resolver_failure_is_stable_json_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            result = subprocess.run(
                [str(ROOT / "resolve-python.sh"), str(repo), str(ROOT), "-c", "print('unexpected')"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        payload = json.loads(result.stderr)
        self.assertEqual(
            set(payload),
            {"code", "field_path", "dependency", "runtime_identity", "remediation"},
        )
        self.assertEqual(payload["code"], "runtime_not_bootstrapped")
        self.assertNotIn("Traceback", result.stderr)

    def test_resolver_distinguishes_missing_shared_cache_entry(self) -> None:
        from runtime.bootstrap import active_pointer_path, canonical_json

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            pointer = active_pointer_path(repo)
            pointer.parent.mkdir(parents=True)
            pointer.write_bytes(canonical_json({
                "schema_version": "2.0",
                "cache_scope": "user",
                "runtime_id": "0" * 24,
                "interpreter": "venv/bin/python",
            }) + b"\n")
            result = subprocess.run(
                [str(ROOT / "resolve-python.sh"), str(repo), str(ROOT), "-c", "print('unexpected')"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stderr)
        self.assertEqual(payload["code"], "managed_runtime_missing")
        self.assertEqual(payload["runtime_identity"], "0" * 24)

    def test_linked_worktree_uses_git_common_pointer_and_shared_runtime(self) -> None:
        from runtime.bootstrap import active_pointer_path

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            worktree = Path(tmp) / "worktree"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Runtime Test"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "runtime@example.invalid"], cwd=repo, check=True)
            (repo / "README.md").write_text("runtime test\n")
            subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "test: initial"], cwd=repo, check=True)
            installed = bootstrap_runtime(repo)
            subprocess.run(["git", "worktree", "add", "-q", "-b", "test/worktree", str(worktree)], cwd=repo, check=True)
            self.assertEqual(active_pointer_path(repo), active_pointer_path(worktree))
            result = subprocess.run(
                [str(ROOT / "resolve-python.sh"), str(worktree), str(ROOT), "-c", "import jsonschema;print(jsonschema.__version__)"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            self.assertTrue(result.stdout.strip())
            self.assertEqual(installed["runtime_identity"], json.loads(active_pointer_path(worktree).read_text())["runtime_id"])

    def test_linked_worktree_resolves_common_pointer_without_git_on_path(self) -> None:
        from runtime.bootstrap import active_pointer_path

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            worktree = Path(tmp) / "worktree"
            command_bin = Path(tmp) / "commands"
            repo.mkdir()
            command_bin.mkdir()
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Runtime Test"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "runtime@example.invalid"], cwd=repo, check=True)
            (repo / "README.md").write_text("runtime test\n")
            subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "test: initial"], cwd=repo, check=True)
            installed = bootstrap_runtime(repo)
            subprocess.run(["git", "worktree", "add", "-q", "-b", "test/no-git-path", str(worktree)], cwd=repo, check=True)
            for command in ("bash", "sed", "tr"):
                command_path = shutil.which(command)
                self.assertIsNotNone(command_path)
                (command_bin / command).symlink_to(str(command_path))
            environment = os.environ.copy()
            environment["PATH"] = str(command_bin)
            result = subprocess.run(
                [str(ROOT / "resolve-python.sh"), str(worktree), str(ROOT), "-c", "import jsonschema;print('ok')"],
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            self.assertEqual(result.stdout.strip(), "ok")
            self.assertEqual(active_pointer_path(repo), active_pointer_path(worktree))
            self.assertEqual(installed["runtime_identity"], json.loads(active_pointer_path(worktree).read_text())["runtime_id"])

    def test_linked_worktrees_with_different_contracts_keep_independent_runtime_selection(self) -> None:
        from runtime.bootstrap import active_pointer_path

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            first_worktree = root / "worktree-a"
            second_worktree = root / "worktree-b"
            first_assets = root / "assets-a"
            second_assets = root / "assets-b"
            repo.mkdir()
            shutil.copytree(ROOT, first_assets)
            shutil.copytree(ROOT, second_assets)
            with (second_assets / "requirements.lock").open("a", encoding="utf-8") as handle:
                handle.write("\n# second checkout identity\n")
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Runtime Test"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "runtime@example.invalid"], cwd=repo, check=True)
            (repo / "README.md").write_text("runtime test\n")
            subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "test: initial"], cwd=repo, check=True)
            subprocess.run(["git", "worktree", "add", "-q", "-b", "test/runtime-a", str(first_worktree)], cwd=repo, check=True)
            subprocess.run(["git", "worktree", "add", "-q", "-b", "test/runtime-b", str(second_worktree)], cwd=repo, check=True)

            first = bootstrap_runtime(first_worktree, first_assets)
            second = bootstrap_runtime(second_worktree, second_assets)

            self.assertNotEqual(first["runtime_identity"], second["runtime_identity"])
            self.assertNotEqual(active_pointer_path(first_worktree), active_pointer_path(second_worktree))
            self.assertEqual(first["runtime_identity"], json.loads(active_pointer_path(first_worktree).read_text())["runtime_id"])
            self.assertEqual(second["runtime_identity"], json.loads(active_pointer_path(second_worktree).read_text())["runtime_id"])
            for worktree, assets, expected in (
                (first_worktree, first_assets, first["runtime_identity"]),
                (second_worktree, second_assets, second["runtime_identity"]),
            ):
                result = subprocess.run(
                    [str(assets / "resolve-python.sh"), str(worktree), str(assets), "-c", "import jsonschema;print('ok')"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result)
                self.assertEqual(result.stdout.strip(), "ok")
                self.assertEqual(expected, json.loads(active_pointer_path(worktree).read_text())["runtime_id"])

    def test_resolver_preserves_validator_error_classification(self) -> None:
        from runtime.bootstrap import active_pointer_path

        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(
            os.environ,
            {"GURU_TEAM_PYTHON_CACHE_ROOT": str(Path(tmp) / "cache")},
        ):
            repo = Path(tmp) / "repo"
            repo.mkdir()
            bootstrap_runtime(repo)
            pointer_path = active_pointer_path(repo)
            pointer = json.loads(pointer_path.read_text())
            pointer["cache_scope"] = "checkout"
            pointer_path.write_text(json.dumps(pointer, sort_keys=True, separators=(",", ":")) + "\n")
            result = subprocess.run(
                [str(ROOT / "resolve-python.sh"), str(repo), str(ROOT), "-c", "print('unexpected')"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stderr)
        self.assertEqual(payload["code"], "managed_runtime_missing")
        self.assertEqual(payload["dependency"], "python-runtime")

    def test_public_wrapper_uses_managed_runtime_when_path_python_has_no_jsonschema(self) -> None:
        no_site_packages = subprocess.run(
            [sys.executable, "-S", "-c", "import importlib.util; assert importlib.util.find_spec('jsonschema') is None"],
            check=False,
        )
        self.assertEqual(no_site_packages.returncode, 0)
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            installed_root = repo / ".trellis/guru-team"
            copy_active_runtime(repo)
            shutil.copytree(ROOT, installed_root / "runtime")
            package = SKILLS / "packages/guru-select-workflow-mode"
            shutil.copytree(package, installed_root / "skills/packages/guru-select-workflow-mode")
            projected = repo / ".agents/skills/guru-select-workflow-mode"
            shutil.copytree(package, projected)
            shim_dir = repo / "path-bin"
            shim_dir.mkdir()
            shim = shim_dir / "python3"
            shim.write_text(f"#!/bin/sh\nexec {sys.executable} -S \"$@\"\n", encoding="utf-8")
            shim.chmod(0o755)
            result = subprocess.run(
                [
                    str(projected / "scripts/invoke.sh"),
                    "--input",
                    str(projected / "examples/public-input.json"),
                    "--owner-result",
                    str(projected / "examples/workflow-mode-selection.json"),
                    "--json",
                ],
                cwd=repo,
                env={**os.environ, "PATH": f"{shim_dir}:/usr/bin:/bin"},
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result)
        payload = json.loads(result.stdout)
        self.assertEqual(payload, {"exit_id": "task_free"})

    def test_command_runtime_consumes_one_global_json_flag(self) -> None:
        from runtime.command import _consume_global_json_flag, _validate_argument_cardinality
        from runtime.io import CommandError

        self.assertEqual(
            _consume_global_json_flag(["--root", ".", "--json", "--input", "value"]),
            ["--root", ".", "--input", "value"],
        )
        with self.assertRaises(CommandError) as raised:
            _consume_global_json_flag(["--json", "--json"])
        self.assertEqual(raised.exception.code, "conflicting_arguments")
        command = {
            "arguments": [
                {"flag": "--profile", "repeatable": False, "conflicts": []},
                {"flag": "--path", "repeatable": True, "conflicts": []},
                {"flag": "--resolve-only", "repeatable": False, "conflicts": ["--execute"]},
                {"flag": "--execute", "repeatable": False, "conflicts": ["--resolve-only"]},
            ]
        }
        with self.assertRaises(CommandError) as repeated:
            _validate_argument_cardinality(command, ["--profile", "one", "--profile=two"])
        self.assertEqual(repeated.exception.code, "conflicting_arguments")
        _validate_argument_cardinality(command, ["--path", "one", "--path=two"])
        with self.assertRaises(CommandError) as conflicting:
            _validate_argument_cardinality(command, ["--resolve-only", "--execute"])
        self.assertEqual(conflicting.exception.code, "conflicting_arguments")

    def test_command_error_can_preserve_declared_private_stderr_payload(self) -> None:
        from runtime.io import CommandError, fail

        stdout = StringIO()
        stderr = StringIO()
        error = CommandError(
            "finalization_stale",
            "finalization",
            "Reprepare.",
            3,
            response={"status": "error", "stage": "archive-path-preflight"},
            response_stream="stderr",
        )
        with redirect_stdout(stdout), redirect_stderr(stderr):
            self.assertEqual(fail(error), 3)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(
            json.loads(stderr.getvalue()),
            {"status": "error", "stage": "archive-path-preflight"},
        )

    def test_kernel_inventory_is_closed_and_contains_no_business_cli(self) -> None:
        from runtime.validate import APPROVED_KERNEL_FILES

        actual = {path.name for path in ROOT.iterdir() if path.is_file()}
        self.assertEqual(actual, APPROVED_KERNEL_FILES)
        self.assertNotIn("utility.py", actual)

    def test_contract_discovery_projects_every_active_public_contract(self) -> None:
        from runtime.discovery import discover

        registry = json.loads((SKILLS / "registry.json").read_text(encoding="utf-8"))
        active = [row for row in registry["skills"] if row["state"] == "active"]
        self.assertEqual(len(active), 18)
        for row in active:
            with self.subTest(skill=row["id"]):
                payload = discover(SKILLS, row["id"])
                interface = json.loads((SKILLS / row["interface"]).read_text(encoding="utf-8"))
                contracts = interface["public_contracts"]
                self.assertEqual(payload, {
                    "status": "ok",
                    "skill_id": row["id"],
                    "interface_schema_id": row["interface_schema_id"],
                    "input": contracts["input"],
                    "invocation": contracts["invocation"],
                    "outputs": contracts["outputs"],
                    "consumer_inputs": contracts["consumer_inputs"],
                    "projections": contracts["projections"],
                    "private_artifacts": contracts["private_artifacts"],
                })

    def test_contract_discovery_wrapper_and_unknown_skill_error(self) -> None:
        wrapper = Path(__file__).resolve().parents[4] / "workflows/guru-team/scripts/bash/discover-skill-contract.sh"
        root = Path(__file__).resolve().parents[5]
        current_checkout_environment = os.environ.copy()
        current_checkout_environment.pop("GURU_TEAM_PYTHON_CACHE_ROOT", None)
        success = subprocess.run(
            [str(wrapper), "--root", str(root), "--mode", "source", "--skill", "guru-sync-base", "--json"],
            env=current_checkout_environment,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(success.returncode, 0, success)
        self.assertEqual(json.loads(success.stdout)["skill_id"], "guru-sync-base")
        failure = subprocess.run(
            [str(wrapper), "--root", str(root), "--mode", "source", "--skill", "guru-missing-skill", "--json"],
            env=current_checkout_environment,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(failure.returncode, 2, failure)
        self.assertEqual(failure.stdout, "")
        self.assertEqual(set(json.loads(failure.stderr)), {"code", "field_path", "remediation"})

    def test_launcher_direct_contract_and_missing_arguments(self) -> None:
        launcher = ROOT / "launch.sh"
        package = SKILLS / "packages/guru-sync-base"
        current_checkout_environment = os.environ.copy()
        current_checkout_environment.pop("GURU_TEAM_PYTHON_CACHE_ROOT", None)
        direct = subprocess.run(
            [str(launcher), str(package), "sync-base", "--help"],
            env=current_checkout_environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(direct.returncode, 0, direct)
        self.assertIn("usage: sync-base", direct.stdout)
        self.assertEqual(direct.stderr, "")

        missing = subprocess.run(
            [str(launcher)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(missing.returncode, 2, missing)
        payload = json.loads(missing.stdout)
        self.assertEqual(payload["code"], "invalid_arguments")
        self.assertNotIn("unbound variable", missing.stdout + missing.stderr)

    def test_platform_projection_routes_to_installed_package(self) -> None:
        skill_id = "guru-sync-base"
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            installed_root = repo / ".trellis/guru-team"
            copy_active_runtime(repo)
            shutil.copytree(ROOT, installed_root / "runtime")
            shutil.copytree(
                SKILLS / "packages" / skill_id,
                installed_root / "skills/packages" / skill_id,
            )
            for platform in (".agents", ".claude", ".codex", ".cursor"):
                projection = repo / platform / "skills" / skill_id
                (projection / "scripts").mkdir(parents=True)
                shutil.copy2(
                    SKILLS / "packages" / skill_id / "scripts/invoke.sh",
                    projection / "scripts/invoke.sh",
                )
                result = subprocess.run(
                    [str(projection / "scripts/invoke.sh"), "--help"],
                    cwd=repo,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result)
                self.assertIn("usage: invoke-guru-sync-base", result.stdout)
                self.assertEqual(result.stderr, "")

    def test_platform_projection_uses_installed_repo_as_default_root(self) -> None:
        skill_id = "guru-discover-change-context"
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp)
            repo = outside / "repo"
            repo.mkdir()
            subprocess.run(
                ["git", "init", "-q", "-b", "feat/context", str(repo)],
                check=True,
            )
            (repo / ".gitignore").write_text(".trellis/.runtime/\n", encoding="utf-8")
            installed_root = repo / ".trellis/guru-team"
            copy_active_runtime(repo)
            shutil.copytree(ROOT, installed_root / "runtime")
            shutil.copytree(
                SKILLS / "packages" / skill_id,
                installed_root / "skills/packages" / skill_id,
            )
            projection = repo / ".agents" / "skills" / skill_id
            (projection / "scripts").mkdir(parents=True)
            shutil.copy2(
                SKILLS / "packages" / skill_id / "scripts/invoke.sh",
                projection / "scripts/invoke.sh",
            )
            task = repo / ".trellis/tasks/08-12-context"
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps({
                "id": "08-12-context",
                "status": "in_progress",
                "branch": "feat/context",
            }))
            subprocess.run(["git", "config", "user.name", "Kernel Test"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "kernel@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "test: add installed runtime"], cwd=repo, check=True)
            owner = json.loads((
                installed_root
                / "skills/packages"
                / skill_id
                / "examples/change-context-owner-result.json"
            ).read_text())
            public_output = json.loads((
                installed_root
                / "skills/packages"
                / skill_id
                / "examples/public-context-ready-output-3.0.json"
            ).read_text())
            owner["mode"] = "workflow"
            invocation = outside / "invocation.json"
            invocation.write_text(json.dumps({
                "schema_version": "1.0",
                "public_input": {
                    "profile": "pre_task",
                    "source_exit": "synced",
                    "mode": "workflow",
                    "repo_locator": "example/repo",
                    "base_branch": "main",
                    "continuation_id": "outside-cwd",
                },
                "transition": {
                    "repo_locator": ".",
                    "base": public_output["transition"]["base"],
                },
                "owner_context": {},
                "owner_result": owner,
            }))
            result = subprocess.run(
                [
                    str(projection / "scripts/invoke.sh"),
                    "--invocation",
                    str(invocation),
                    "--active-task",
                    ".trellis/tasks/08-12-context",
                ],
                cwd=outside,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            self.assertEqual(json.loads(result.stdout)["exit_id"], "context_ready")
            self.assertEqual(result.stderr, "")

    def test_source_and_installed_layouts(self) -> None:
        source = _package_paths(Path("/repo"), "source")
        self.assertEqual(source[0], Path("/repo/trellis/skills/guru-team"))
        self.assertEqual(source[3], Path("/repo/trellis/skills/guru-team/runtime"))
        installed = _package_paths(Path("/repo"), "installed")
        self.assertEqual(installed[0], Path("/repo/.trellis/guru-team/skills"))
        self.assertEqual(installed[3], Path("/repo/.trellis/guru-team/runtime"))
    def test_command_and_error_contracts_for_pilots(self) -> None:
        from jsonschema import Draft202012Validator
        command_schema = json.loads((SKILLS / "schemas/skill-commands.schema.json").read_text())
        error_schema = json.loads((SKILLS / "schemas/skill-error-catalog.schema.json").read_text())
        for package_id in ("guru-sync-base", "guru-clarify-requirements"):
            package = SKILLS / "packages" / package_id
            commands = json.loads((package / "commands.json").read_text())
            errors = json.loads((package / "errors/catalog.json").read_text())
            self.assertEqual(list(Draft202012Validator(command_schema).iter_errors(commands)), [])
            self.assertEqual(list(Draft202012Validator(error_schema).iter_errors(errors)), [])
            codes = {item["code"] for item in errors["errors"]}
            self.assertEqual(len(codes), len(errors["errors"]))
            for command in commands["commands"]:
                self.assertEqual(command["owner"], package_id)
                self.assertTrue((package / command["entrypoint"]).is_file())
                self.assertLessEqual(set(command["errors"]), codes)

    def test_kernel_has_no_skill_specific_branching(self) -> None:
        forbidden = ("guru-sync-base", "guru-clarify-requirements", "typed_exit", "profile")
        forbidden_functions = {"prepare", "reviewed_base_freshness", "_reviewed_base_freshness"}
        for path in ROOT.glob("*.py"):
            if path.name == "validate.py":
                continue
            source = path.read_text()
            tree = ast.parse(source)
            from runtime.validate import _fold_string
            folded = {value for node in ast.walk(tree) if (value := _fold_string(node)) is not None}
            self.assertFalse(set(forbidden) & folded, path)
            functions = {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
            self.assertFalse(forbidden_functions & functions, path)

    def test_kernel_guard_folds_concatenated_skill_ids(self) -> None:
        from runtime.validate import _fold_string
        tree = ast.parse('SKILL = "guru-" + "sync-base"')
        values = [_fold_string(node) for node in ast.walk(tree)]
        self.assertIn("guru-sync-base", values)

    def test_compat_dispatch_resolves_validator_metadata(self) -> None:
        package = SKILLS / "packages/guru-sync-base"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "runtime.compat",
                "--package-root",
                str(package),
                "--validator",
                "sync_executor",
                "--",
                "--help",
            ],
            cwd=SKILLS,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("usage: sync-base", result.stdout)


class QualificationNativeIsolationTests(unittest.TestCase):
    def test_production_phase2_inputs_close_schema_5_for_every_exit(self) -> None:
        from adapters.eval import native_adapter
        from jsonschema import Draft202012Validator

        class FixtureRuntime:
            @staticmethod
            def read_json(_path: Path) -> dict[str, str]:
                return {"base_branch": "main"}

            @staticmethod
            def diff_base_ref(_fixture: Path, _base: str) -> str:
                return "origin/main"

            @staticmethod
            def changed_files(_fixture: Path, _range: str) -> list[str]:
                return ["src/production-eval.txt"]

            @staticmethod
            def git_status_paths(_fixture: Path) -> list[str]:
                return []

            @staticmethod
            def write_json(path: Path, payload: dict[str, object]) -> None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(payload), encoding="utf-8")

        schema = json.loads(
            (
                SKILLS
                / "packages/guru-check-task/schemas/phase2-check.schema.json"
            ).read_text(encoding="utf-8")
        )
        expected = {
            "passed": ("candidate:phase2:no-defect", "rejected_not_reproduced"),
            "implementation_required": (
                "candidate:phase2:defect",
                "qualified_current",
            ),
            "planning_stale": (
                "candidate:phase2:scope",
                "qualified_approved_expansion",
            ),
            "blocked": ("candidate:phase2:no-defect", "rejected_not_reproduced"),
        }
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            task = fixture / ".trellis/tasks/phase2-eval"
            package = SKILLS / "packages/guru-check-task"
            for exit_id, (candidate_ref, decision) in expected.items():
                with self.subTest(exit_id=exit_id):
                    path = native_adapter.production_phase2_input(
                        FixtureRuntime(), fixture, task, package, exit_id
                    )
                    payload = json.loads(path.read_text(encoding="utf-8"))
                    current = {
                        "schema_version": "5.0",
                        "skill_id": "guru-check-task",
                        "task_ref": ".trellis/tasks/phase2-eval",
                        "phase2_capture_commit": "1" * 40,
                        "reviewed_content_sha256": "2" * 64,
                        **payload,
                    }
                    errors = list(Draft202012Validator(schema).iter_errors(current))
                    self.assertEqual([], errors)
                    self.assertEqual(
                        [(candidate_ref, decision)],
                        [
                            (row["candidate_ref"], row["decision"])
                            for row in payload["candidate_classifications"]
                        ],
                    )
                    linked_refs = {
                        row["candidate_ref"]
                        for key in ("scope_decisions", "findings")
                        for row in payload["semantic_review"][key]
                    }
                    self.assertLessEqual(linked_refs, {candidate_ref})

    def test_production_branch_review_inputs_close_schema_5_for_every_exit(self) -> None:
        from adapters.eval import native_adapter
        from jsonschema import Draft202012Validator

        schema = json.loads(
            (
                SKILLS
                / "packages/guru-review-branch/schemas/review-gate-5.0.schema.json"
            ).read_text(encoding="utf-8")
        )
        expected = {
            "passed": ["rejected_not_reproduced"] * 3,
            "implementation_required": ["qualified_current"],
            "scope_confirmation_required": ["rejected_no_authority"],
            "blocked": ["rejected_not_reproduced"] * 3,
        }
        for exit_id, decisions in expected.items():
            with self.subTest(exit_id=exit_id):
                candidates = native_adapter.production_review_candidate(
                    exit_id,
                    "1" * 40,
                )
                classifications = [
                    native_adapter.production_review_classification(item)
                    for item in candidates
                ]
                semantic_candidates = [
                    native_adapter.production_review_semantic_candidate(item)
                    for item in candidates
                ]
                semantic = {
                    "qualified_findings": [
                        item for item in semantic_candidates
                        if item["disposition"] == "qualified_finding"
                    ],
                    "scope_proposals": [
                        item for item in semantic_candidates
                        if item["disposition"] == "scope_proposal"
                    ],
                    "observations": [],
                    "followup_candidates": [],
                    "rejected_candidates": [
                        item for item in semantic_candidates
                        if item["disposition"] == "rejected_candidate"
                    ],
                    "ai_review_gate": {
                        "status": exit_id,
                        "summary": "Reviewed the complete current range.",
                    },
                }
                payload = {
                    "schema_version": "5.0",
                    "skill_id": "guru-review-branch",
                    "generated_at": "2026-08-16T00:00:00Z",
                    "task_dir": ".trellis/tasks/branch-review-eval",
                    "mode": "workflow",
                    "profile": "branch_review",
                    "review_intent": "initial_review",
                    "typed_exit": exit_id,
                    "review_commit": "1" * 40,
                    "reviewed_content_sha256": "2" * 64,
                    "base_ref": "origin/main",
                    "base_head": "3" * 40,
                    "integration_pair": None,
                    "candidate_classifications": classifications,
                    "semantic_review": semantic,
                    "verification_evidence": {
                        "reviewer": "independent-reviewer",
                        "review_source": "independent-agent",
                        "evidence": ["Reviewed the complete current range."],
                    },
                    "facts_sha256": "4" * 64,
                }
                errors = list(Draft202012Validator(schema).iter_errors(payload))
                self.assertEqual([], errors)
                self.assertEqual(decisions, [row["decision"] for row in classifications])
                classified_refs = {row["candidate_ref"] for row in classifications}
                semantic_refs = {
                    row["candidate_ref"]
                    for key in (
                        "qualified_findings",
                        "scope_proposals",
                        "observations",
                        "followup_candidates",
                        "rejected_candidates",
                    )
                    for row in semantic[key]
                }
                self.assertEqual(classified_refs, semantic_refs)

    def test_model_request_uses_protocol_2_and_hides_control_identity(self) -> None:
        from adapters.eval import native_adapter

        request = {
            "skill_id": native_adapter.QUALIFICATION_SKILL,
            "case_id": "case-secret-identity",
            "invocation_id": "1" * 64,
            "invocation_index": 4,
            "input_profile_id": "implementation_discovery",
            "pair_id": "pair-secret-identity",
            "pressure_framing": "severity",
            "expected_exit": "classified",
            "expected_decisions": [{"decision": "qualified_current"}],
            "prompt": "Review one call-local candidate against current authority.",
            "interface": {
                "public_invocation": {
                    "wrapper": "scripts/invoke.sh",
                    "input_binding": {
                        "kind": "structured_json",
                        "profile_selector": {
                            "source": "aggregate_public_input",
                            "field": "profile",
                        },
                    },
                    "example_argv": ["--invocation", "-"],
                },
            },
        }
        hashes = set()
        for root_name in ("first-random-root", "second-random-root"):
            with tempfile.TemporaryDirectory() as tmp:
                model_root = Path(tmp) / root_name
                projection = model_root / "public-package"
                repository = model_root / "evidence/repository"
                evidence = model_root / "evidence/case/evidence-01.json"
                projection.mkdir(parents=True)
                repository.mkdir(parents=True)
                evidence.parent.mkdir(parents=True, exist_ok=True)
                evidence.write_text("{}", encoding="utf-8")
                payload = native_adapter.qualification_model_request(
                    request,
                    model_root=model_root,
                    projection_root=projection,
                    repository_root=repository,
                    evidence_paths=[evidence],
                )
                encoded = json.dumps(payload, sort_keys=True)
                self.assertEqual(payload["schema_version"], "3.0")
                self.assertEqual(
                    payload["protocol"],
                    "guru-qualification-production-prompt-2.0",
                )
                self.assertEqual(payload["public_package_root"], "public-package")
                self.assertEqual(
                    payload["repository_evidence_root"],
                    "evidence/repository",
                )
                self.assertEqual(
                    payload["public_invocation"]["input_binding"]["profile_selector"],
                    {"source": "aggregate_public_input", "field": "profile"},
                )
                for forbidden in (
                    "case_id",
                    "case-secret-identity",
                    "invocation_id",
                    "invocation_index",
                    "input_profile_id",
                    "pair_id",
                    "pair-secret-identity",
                    "pressure_framing",
                    "expected_exit",
                    "expected_decisions",
                ):
                    self.assertNotIn(forbidden, encoded)
                hashes.add(
                    native_adapter.qualification_prompt_sha256(
                        payload,
                        "2" * 64,
                        "gpt-5.6-sol",
                    )
                )
        self.assertEqual(len(hashes), 1)

    def test_codex_argv_uses_one_neutral_root_without_add_dir(self) -> None:
        from adapters.eval import native_adapter

        with tempfile.TemporaryDirectory() as tmp:
            model_root = Path(tmp) / "model-root"
            model_root.mkdir()
            request = {
                "schema_version": "3.0",
                "skill_id": native_adapter.QUALIFICATION_SKILL,
                "model_id": "gpt-5.6-sol",
                "workdir": str(Path(tmp) / "private-workdir"),
                "_model_root": str(model_root),
            }
            argv, output = native_adapter.native_argv(
                "codex",
                "/usr/bin/codex",
                request,
                "model-visible-context",
                model_root / "native-context.txt",
                Path(tmp) / "private/native-request.json",
                model_root / "public-package",
            )
        self.assertNotIn("--add-dir", argv)
        self.assertNotIn("--ignore-user-config", argv)
        self.assertIn("--strict-config", argv)
        self.assertEqual(argv.count("--skip-git-repo-check"), 1)
        self.assertEqual(
            argv.index("--skip-git-repo-check"),
            argv.index("--strict-config") + 1,
        )
        self.assertEqual(argv.index("--cd"), argv.index("--skip-git-repo-check") + 1)
        self.assertEqual(argv[argv.index("--cd") + 1], str(model_root.resolve()))
        self.assertEqual(argv[argv.index("--model") + 1], "gpt-5.6-sol")
        self.assertEqual(output, (model_root / "output/native-last-message.txt").resolve())
        request.pop("skill_id")
        request["model_id"] = "gpt-5.6"
        with self.assertRaisesRegex(ValueError, "model identity"):
            native_adapter.native_argv(
                "codex",
                "/usr/bin/codex",
                request,
                "model-visible-context",
                model_root / "native-context.txt",
                Path(tmp) / "private/native-request.json",
                model_root / "public-package",
            )

    def test_native_environment_is_explicit_and_secret_free(self) -> None:
        from adapters.eval import native_adapter

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            environment = native_adapter.minimal_native_environment(
                {
                    "PATH": "/usr/bin:/bin",
                    "HOME": "/example/home",
                    "LANG": "C.UTF-8",
                    "GITHUB_PERSONAL_TOKEN": "must-not-leak",
                    "OPENAI_API_KEY": "must-not-leak",
                    "UNRELATED_PARENT_VALUE": "must-not-inherit",
                },
                cwd=root / "model",
                codex_home=root / "private/codex-home",
                control={"GURU_TEAM_NATIVE_REQUEST": str(root / "private/request.json")},
            )
        self.assertEqual(
            set(environment),
            {
                "PATH",
                "HOME",
                "LANG",
                "PWD",
                "PYTHONDONTWRITEBYTECODE",
                "CODEX_HOME",
                "GURU_TEAM_NATIVE_REQUEST",
            },
        )
        self.assertNotIn("must-not-leak", json.dumps(environment))
        self.assertEqual(
            native_adapter.recorded_native_environment(environment),
            dict(sorted(environment.items())),
        )

    def test_external_codex_home_is_owner_private_and_outside_run_root(self) -> None:
        from adapters.eval import native_adapter

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_root = root / "run"
            codex_home = root / "auth-home"
            run_root.mkdir()
            codex_home.mkdir(mode=0o700)
            auth = codex_home / "auth.json"
            auth.write_text("{}", encoding="utf-8")
            auth.chmod(0o600)
            selected = native_adapter.external_codex_home(
                {"CODEX_HOME": str(codex_home)},
                run_root,
            )
            self.assertEqual(selected, codex_home.resolve())
            native_adapter.write_codex_permission_profile(
                selected,
                run_root / "model-root",
                [selected, run_root],
            )
            self.assertEqual(stat.S_IMODE(selected.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(auth.stat().st_mode), 0o600)
            self.assertEqual(
                stat.S_IMODE((selected / "config.toml").stat().st_mode),
                0o600,
            )
            self.assertEqual(list(run_root.rglob("auth.json")), [])
            with self.assertRaisesRegex(ValueError, "outside"):
                native_adapter.external_codex_home(
                    {"CODEX_HOME": str(run_root / "nested-home")},
                    run_root,
                )

    def test_permission_profile_allows_model_root_and_denies_private_roots(self) -> None:
        from adapters.eval import native_adapter

        codex = shutil.which("codex")
        if codex is None:
            self.skipTest("Codex CLI is unavailable for the no-model sandbox probe")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model_root = root / "model-root"
            private_root = root / "private-control"
            real_worktree = root / "real-worktree"
            corpus = root / "corpus.json"
            auth = root / "auth.json"
            for directory in (model_root, private_root, real_worktree):
                directory.mkdir()
            (private_root / "control.json").write_text("{}", encoding="utf-8")
            (real_worktree / "README.md").write_text("private", encoding="utf-8")
            corpus.write_text("{}", encoding="utf-8")
            auth.write_text("{}", encoding="utf-8")
            codex_home = private_root / "codex-home"
            denied = [
                private_root,
                real_worktree,
                corpus,
                auth,
                Path("/tmp"),
                Path("/private/tmp"),
            ]
            native_adapter.write_codex_permission_profile(
                codex_home,
                model_root,
                denied,
            )
            environment = native_adapter.minimal_native_environment(
                dict(os.environ),
                cwd=model_root,
                codex_home=codex_home,
            )
            result = native_adapter.run_codex_permission_probe(
                codex,
                environment,
                model_root,
                native_adapter.canonical_permission_paths(denied),
            )
        self.assertEqual(result["returncode"], 0, result)
        self.assertTrue(result["result"]["positive"])
        self.assertEqual(
            set(result["result"]["denied"]),
            {str(path) for path in native_adapter.canonical_permission_paths(denied)},
        )

    def test_permission_probe_uses_resolved_base_interpreter(self) -> None:
        from adapters.eval import native_adapter

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            denied_root = root / "managed-cache"
            managed_python = denied_root / "runtime/venv/bin/python"
            base_interpreter = Path(str(sys._base_executable)).resolve()
            with (
                mock.patch.object(native_adapter.sys, "_base_executable", str(base_interpreter)),
                mock.patch.object(native_adapter.sys, "executable", str(managed_python)),
            ):
                argv = native_adapter.permission_probe_argv(
                    "/usr/bin/codex",
                    root / "model-root",
                    root / "model-root/permission-probe.py",
                    [denied_root, Path("/tmp"), Path("/private/tmp")],
                )
        self.assertEqual(Path(argv[6]), base_interpreter)
        self.assertNotEqual(argv[6], str(managed_python))

    def test_permission_probe_rejects_invalid_base_interpreter(self) -> None:
        from adapters.eval import native_adapter

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with (
                mock.patch.object(native_adapter.sys, "_base_executable", str(root / "missing-python")),
                mock.patch.object(native_adapter.sys, "executable", str(root / "managed/venv/bin/python")),
            ):
                with self.assertRaisesRegex(ValueError, "base interpreter is unavailable"):
                    native_adapter.permission_probe_argv(
                        "/usr/bin/codex",
                        root / "model-root",
                        root / "model-root/permission-probe.py",
                        [root / "managed", Path("/tmp"), Path("/private/tmp")],
                    )

    def test_permission_probe_rejects_base_interpreter_inside_denied_path(self) -> None:
        from adapters.eval import native_adapter

        base_interpreter = Path(str(sys._base_executable)).resolve()
        self.assertTrue(base_interpreter.is_file())
        self.assertTrue(os.access(base_interpreter, os.X_OK))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with (
                mock.patch.object(
                    native_adapter.sys,
                    "_base_executable",
                    str(base_interpreter),
                ),
                mock.patch.object(
                    native_adapter.sys,
                    "executable",
                    str(root / "managed/venv/bin/python"),
                ),
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "^permission probe base interpreter is inside a denied path$",
                ):
                    native_adapter.permission_probe_argv(
                        "/usr/bin/codex",
                        root / "model-root",
                        root / "model-root/permission-probe.py",
                        [base_interpreter, Path("/tmp"), Path("/private/tmp")],
                    )

    def test_permission_probe_from_tmp_managed_venv_denies_private_roots(self) -> None:
        codex = shutil.which("codex")
        if codex is None:
            self.skipTest("Codex CLI is unavailable for the managed-venv no-model sandbox probe")
        base_interpreter = Path(str(sys._base_executable)).resolve()
        with tempfile.TemporaryDirectory(prefix="guru-permission-probe-", dir="/tmp") as tmp:
            root = Path(tmp)
            venv = root / "managed/venv"
            created = subprocess.run(
                [str(base_interpreter), "-m", "venv", "--without-pip", str(venv)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(created.returncode, 0, created)
            managed_python = venv / "bin/python"
            child_code = """
import importlib.util,json,os,sys
from pathlib import Path
adapter_path,codex,root_value=sys.argv[1:]
root=Path(root_value)
spec=importlib.util.spec_from_file_location("managed_venv_native_adapter",adapter_path)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
model_root=root/"model-root";private_root=root/"private-control";worktree=root/"source-worktree"
corpus=root/"corpus.json";auth=root/"auth.json";codex_home=private_root/"codex-home"
for directory in (model_root,private_root,worktree): directory.mkdir(parents=True)
(private_root/"control.json").write_text("{}",encoding="utf-8")
(worktree/"README.md").write_text("private",encoding="utf-8")
corpus.write_text("{}",encoding="utf-8");auth.write_text("{}",encoding="utf-8")
denied=[private_root,worktree,corpus,auth,Path("/tmp"),Path("/private/tmp")]
module.write_codex_permission_profile(codex_home,model_root,denied)
environment=module.minimal_native_environment(dict(os.environ),cwd=model_root,codex_home=codex_home)
canonical=module.canonical_permission_paths(denied)
result=module.run_codex_permission_probe(codex,environment,model_root,canonical)
payload={"sys_executable":sys.executable,"sys_base_executable":sys._base_executable,"selected_interpreter":result["argv"][6],"canonical_denied":[str(path) for path in canonical],"probe":result}
print(json.dumps(payload,sort_keys=True));raise SystemExit(0 if result["returncode"]==0 else 1)
"""
            environment = os.environ.copy()
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            result = subprocess.run(
                [
                    str(managed_python),
                    "-c",
                    child_code,
                    str(SKILLS / "adapters/eval/native_adapter.py"),
                    codex,
                    str(root),
                ],
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            payload = json.loads(result.stdout)
        self.assertEqual(
            Path(payload["sys_executable"]),
            root.resolve() / "managed/venv/bin/python",
        )
        self.assertEqual(Path(payload["sys_base_executable"]).resolve(), base_interpreter)
        self.assertEqual(Path(payload["selected_interpreter"]), base_interpreter)
        self.assertFalse(str(base_interpreter).startswith(("/tmp/", "/private/tmp/")))
        self.assertTrue(payload["probe"]["result"]["positive"])
        self.assertEqual(
            set(payload["probe"]["result"]["denied"]),
            set(payload["canonical_denied"]),
        )

    def test_repository_projection_omits_control_auth_corpus_and_runtime(self) -> None:
        from adapters.eval import native_adapter

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "owner"
            destination = root / "projection"
            (source / ".git").mkdir(parents=True)
            (source / ".trellis/.runtime").mkdir(parents=True)
            (source / ".trellis/guru-team/runtime").mkdir(parents=True)
            (source / ".trellis/guru-team/skills/adapters/eval").mkdir(parents=True)
            (source / ".trellis/guru-team/skills/packages/guru-qualify-normal-scenario/runtime").mkdir(parents=True)
            (source / "package/evals").mkdir(parents=True)
            (source / "package/tests").mkdir(parents=True)
            (source / ".git/config").write_text("private", encoding="utf-8")
            (source / ".trellis/.runtime/result.json").write_text("{}", encoding="utf-8")
            (source / ".trellis/guru-team/runtime/private.py").write_text("pass\n", encoding="utf-8")
            (source / ".trellis/guru-team/skills/adapters/eval/native.py").write_text("pass\n", encoding="utf-8")
            (source / ".trellis/guru-team/skills/packages/guru-qualify-normal-scenario/runtime/private.py").write_text("pass\n", encoding="utf-8")
            (source / "package/evals/evals.json").write_text("{}", encoding="utf-8")
            (source / "package/tests/test_contract.py").write_text("pass\n", encoding="utf-8")
            (source / "auth.json").write_text("{}", encoding="utf-8")
            (source / ".env").write_text("SECRET=value", encoding="utf-8")
            native_adapter.stage_repository_projection(source, destination)
            files = {
                path.relative_to(destination).as_posix()
                for path in destination.rglob("*")
                if path.is_file()
            }
        self.assertEqual(files, {"package/tests/test_contract.py"})


if __name__ == "__main__":
    unittest.main()
