"""Focused installer/runtime behavior; synthetic interpreter identities are fixtures."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from runtime import bootstrap as managed

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
SCRIPTS = REPO / "trellis/presets/guru-team/scripts"


class PythonSelectionTests(unittest.TestCase):
    def test_default_path_and_explicit_selection_and_no_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            shim = directory / "python3"
            shim.symlink_to(sys.executable)
            with mock.patch.dict(os.environ, {"PATH": str(directory)}):
                self.assertEqual(managed.select_python(), shim)
                self.assertEqual(managed.select_python(sys.executable), Path(sys.executable))
                with self.assertRaises(managed.BootstrapError) as error:
                    managed.select_python(directory / "missing")
                self.assertEqual(error.exception.code, "interpreter_unavailable")
                shim.unlink()
                shim.write_text("not executable")
                with self.assertRaises(managed.BootstrapError):
                    managed.select_python()

    def test_minor_changes_identity_patch_and_path_do_not_fixture(self):
        original = {"implementation": "CPython", "major": 3, "minor": 15,
                    "os_name": "FixtureOS", "machine": "fixture", "abi_tag": "cpython-315",
                    "platform_tag": "fixture", "patch": 0}
        with mock.patch.object(managed.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, json.dumps(original), "")
            first, identity = managed.runtime_identity(ROOT, Path(sys.executable))
            self.assertEqual(identity["python_minor"], 15)
            original["patch"] = 1
            run.return_value = subprocess.CompletedProcess([], 0, json.dumps(original), "")
            with tempfile.TemporaryDirectory() as tmp:
                alias = Path(tmp) / "python3"
                alias.symlink_to(sys.executable)
                self.assertEqual(managed.runtime_identity(ROOT, alias)[0], first)
            original["minor"] = 16
            run.return_value = subprocess.CompletedProcess([], 0, json.dumps(original), "")
            self.assertNotEqual(managed.runtime_identity(ROOT, Path(sys.executable))[0], first)
            original["major"] = 2
            run.return_value = subprocess.CompletedProcess([], 0, json.dumps(original), "")
            with self.assertRaises(managed.BootstrapError) as error:
                managed.runtime_identity(ROOT, Path(sys.executable))
            self.assertEqual(error.exception.code, "python3_required")

    def test_apply_shell_explicit_override_and_actionable_launch_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            unavailable = directory / "missing"
            inert = directory / "inert"
            inert.write_text("not executable")
            non_python3 = directory / "old-python"
            non_python3.write_text("#!/bin/sh\nexit 1\n")
            non_python3.chmod(0o755)
            for interpreter, expected in ((unavailable, "interpreter_unavailable"),
                                           (inert, "interpreter_unavailable"),
                                           (non_python3, "python3_required")):
                result = subprocess.run(["bash", str(SCRIPTS / "bash/apply.sh"), "--python", str(interpreter), "--version"],
                                        text=True, capture_output=True)
                self.assertEqual(result.returncode, 2)
                payload = json.loads(result.stderr)
                self.assertEqual(payload["code"], expected)
                self.assertIn("--python", payload["remediation"])
            # A broken default cannot override the explicit interpreter.
            (directory / "python3").symlink_to(non_python3)
            result = subprocess.run(["bash", str(SCRIPTS / "bash/apply.sh"), "--python", sys.executable, "--version"],
                                    env={**os.environ, "PATH": str(directory) + ":/usr/bin:/bin"},
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result)

    def test_installer_direct_default_does_not_use_its_runner_as_selection(self):
        sys.path.insert(0, str(SCRIPTS / "python"))
        import managed_python_runtime as installer
        result = {"status": "ok", "interpreter": sys.executable}
        with mock.patch.object(installer.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, json.dumps(result), "")) as run:
            installer.ensure_managed_python_runtime(REPO, REPO)
            command = run.call_args.args[0]
            self.assertEqual(command[command.index("--python") + 1], os.path.abspath(shutil.which("python3")))
            installer.ensure_managed_python_runtime(REPO, REPO, python=sys.executable)
            command = run.call_args.args[0]
            self.assertEqual(command[command.index("--python") + 1], sys.executable)


class RuntimeUpdateFailureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temporary.name)
        with mock.patch.dict(os.environ, {"GURU_TEAM_PYTHON_CACHE_ROOT": str(cls.root / "baseline-cache")}):
            cls.baseline = managed.bootstrap(cls.root, ROOT, Path(sys.executable), activate=False)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def setUp(self):
        self.case = tempfile.TemporaryDirectory()
        self.addCleanup(self.case.cleanup)
        self.root = Path(self.case.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.cache = self.root / "cache"
        self.cache.mkdir()
        self.target = self.cache / self.baseline["runtime_identity"]
        shutil.copytree(Path(self.baseline["interpreter"]).parents[2], self.target, symlinks=True)
        self.environment = mock.patch.dict(os.environ, {"GURU_TEAM_PYTHON_CACHE_ROOT": str(self.cache)})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        managed.write_active(self.repo, self.baseline["runtime_identity"])

    def snapshot(self):
        return {path.relative_to(self.target).as_posix():
                (path.lstat().st_mode, os.readlink(path) if path.is_symlink() else path.read_bytes())
                for path in self.target.rglob("*") if path.is_file() or path.is_symlink()}

    def broken_wrapper_assets(self):
        assets = self.root / "assets/runtime"
        shutil.copytree(ROOT, assets, ignore=shutil.ignore_patterns("tests", "__pycache__"))
        for name in ("packages", "schemas"):
            shutil.copytree(ROOT.parent / name, assets.parent / name, ignore=shutil.ignore_patterns("tests", "__pycache__"))
        # Controlled source implementation defect: the real wrapper imports this module.
        (assets / "schema.py").write_text("raise RuntimeError('runtime-check fixture')\n")
        return assets

    def test_same_identity_reuse_and_real_wrapper_failure_preserve_environment(self):
        before = self.snapshot()
        pointer = managed.active_pointer_path(self.repo).read_bytes()
        reused = managed.bootstrap(self.repo, ROOT, Path(sys.executable))
        self.assertEqual(reused["action"], "reused")
        self.assertEqual(self.snapshot(), before)
        assets = self.broken_wrapper_assets()
        with self.assertRaises(managed.BootstrapError) as error:
            managed.bootstrap(self.repo, assets, Path(sys.executable))
        self.assertEqual(error.exception.code, "managed_runtime_check_failed")
        self.assertEqual(managed.active_pointer_path(self.repo).read_bytes(), pointer)
        self.assertEqual(self.snapshot(), before)

    def test_same_identity_repair_failure_preserves_old_target_and_pointer(self):
        managed.venv_python(self.target / "venv").unlink()
        before = self.snapshot()
        pointer = managed.active_pointer_path(self.repo).read_bytes()
        assets = self.broken_wrapper_assets()
        with self.assertRaises(managed.BootstrapError) as error:
            managed.bootstrap(self.repo, assets, Path(sys.executable))
        self.assertEqual(error.exception.code, "managed_runtime_check_failed")
        self.assertEqual(managed.active_pointer_path(self.repo).read_bytes(), pointer)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(list(self.cache.glob(".*.candidate-*")), [])

    def test_dependency_failure_preserves_old_target_and_pointer(self):
        managed.venv_python(self.target / "venv").unlink()
        before = self.snapshot()
        pointer = managed.active_pointer_path(self.repo).read_bytes()
        real_run = subprocess.run

        def fail_install(argv, **kwargs):
            if argv[1:4] == ["-m", "pip", "install"]:
                return subprocess.CompletedProcess(argv, 1, b"", b"fixture install failure")
            return real_run(argv, **kwargs)

        with mock.patch.object(managed.subprocess, "run", side_effect=fail_install):
            with self.assertRaises(managed.BootstrapError) as error:
                managed.bootstrap(self.repo, ROOT, Path(sys.executable))
        self.assertEqual(error.exception.code, "dependency_install_failed")
        self.assertEqual(managed.active_pointer_path(self.repo).read_bytes(), pointer)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(list(self.cache.glob(".*.candidate-*")), [])


if __name__ == "__main__":
    unittest.main()
