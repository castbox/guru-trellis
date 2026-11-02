"""Shared environment discovery through actual bootstrap and public wrappers."""
from __future__ import annotations

import json
import io
import tarfile
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from runtime import bootstrap as owner

ASSETS = Path(__file__).resolve().parents[1]


class RuntimeSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="guru-runtime-selection-")
        cls.directory = Path(cls.temporary.name)
        cls.environment = mock.patch.dict(os.environ, {"GURU_TEAM_PYTHON_CACHE_ROOT": str(cls.directory / "cache")})
        cls.environment.start()
        cls.first = owner.bootstrap(cls.directory / "seed", ASSETS, Path(sys.executable), explicit_python=False)

    @classmethod
    def tearDownClass(cls):
        cls.environment.stop()
        cls.temporary.cleanup()

    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(dir=self.directory, prefix="repo-"))

    def command(self, *arguments, repo=None, assets=ASSETS, environment=None):
        return subprocess.run([str(assets / "manage-python.sh"), str(repo or self.repo), str(assets),
                               *arguments], text=True, capture_output=True,
                              env=environment or os.environ.copy(), check=False)

    def test_readonly_check_then_resolve_without_pointer_reuses_physical_environment(self):
        before = sorted(path.name for path in owner.user_cache_root().iterdir())
        checked = self.command("--check", "--json")
        self.assertEqual(0, checked.returncode, checked.stderr)
        self.assertEqual(self.first["interpreter"], json.loads(checked.stdout)["interpreter"])
        pointer = owner.active_pointer_path(self.repo)
        self.assertFalse(pointer.exists())
        resolved = self.command("--resolve-active", "--json")
        self.assertEqual(0, resolved.returncode, resolved.stderr)
        self.assertEqual(self.first["runtime_identity"], json.loads(resolved.stdout)["runtime_identity"])
        self.assertEqual(before, sorted(path.name for path in owner.user_cache_root().iterdir()))
        selection = json.loads(pointer.read_text())
        self.assertEqual("automatic", selection["selection_mode"])
        self.assertFalse((self.repo / ".trellis/tasks").exists())
        self.assertFalse((self.repo / ".trellis/.runtime/guru-team/python/venv").exists())

    def test_ordinary_git_linked_worktree_runs_installed_package_without_activation(self):
        runtime = self.repo / ".trellis/guru-team/runtime"
        shutil.copytree(ASSETS, runtime, ignore=shutil.ignore_patterns("tests", "__pycache__"))
        skills = runtime.parent / "skills"
        shutil.copytree(ASSETS.parent / "schemas", skills / "schemas")
        package = "guru-select-workflow-mode"
        shutil.copytree(ASSETS.parent / "packages" / package, skills / "packages" / package)
        def git(*args):
            subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, check=True)
        git("init", "-qb", "main")
        git("add", ".")
        git("-c", "user.name=Runtime Test", "-c", "user.email=runtime@example.invalid", "commit", "-qm", "installed fixture")
        linked = self.repo.parent / (self.repo.name + "-linked")
        git("worktree", "add", "-qb", "external", str(linked))
        try:
            runtime = linked / ".trellis/guru-team/runtime"
            package_root = runtime.parent / "skills/packages" / package
            manifest = json.loads((ASSETS / "python-runtime.json").read_text())
            invocation = manifest["public_wrapper_check"]["cases"][0]["arguments"]
            result = subprocess.run([str(package_root / "scripts/invoke.sh"), *invocation],
                                    cwd=linked, text=True, capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("blocked", json.loads(result.stdout)["exit_id"])
            selected = owner.validate_active(linked, runtime)
            self.assertEqual(self.first["interpreter"], selected["interpreter"])
            self.assertFalse((self.repo / ".git/guru-team/python/active.json").exists())
        finally:
            git("worktree", "remove", "--force", str(linked))
        self.assertTrue(Path(self.first["interpreter"]).exists())

    def test_lock_switch_and_return_keep_per_requirement_hints(self):
        original = owner.validate_active(self.repo, ASSETS, cache_selection=True)
        pointer = owner.active_pointer_path(self.repo)
        assets = self.repo / "different/runtime"
        shutil.copytree(ASSETS, assets, ignore=shutil.ignore_patterns("tests", "__pycache__"))
        shutil.copytree(ASSETS.parent / "schemas", assets.parent / "schemas")
        shutil.copytree(ASSETS.parent / "packages/guru-select-workflow-mode",
                        assets.parent / "packages/guru-select-workflow-mode")
        with (assets / "requirements.lock").open("a") as handle:
            handle.write("\n# changed dependency requirement fixture\n")
        second = owner.bootstrap(self.repo, assets, Path(sys.executable), explicit_python=False)
        self.assertNotEqual(original["runtime_identity"], second["runtime_identity"])
        self.assertEqual(original["runtime_identity"], owner.validate_active(self.repo, ASSETS, cache_selection=True)["runtime_identity"])
        self.assertEqual(second["runtime_identity"], owner.validate_active(self.repo, assets)["runtime_identity"])
        self.assertEqual(2, len(json.loads(pointer.read_text())["hints"]))

    def test_explicit_class_with_no_matching_requirement_does_not_fallback(self):
        owner.bootstrap(self.repo, ASSETS, Path(sys.executable), explicit_python=True)
        pointer = owner.active_pointer_path(self.repo)
        before = pointer.read_bytes()
        assets = self.repo / "runtime"
        shutil.copytree(ASSETS, assets)
        with (assets / "requirements.lock").open("a") as handle:
            handle.write("\n# unavailable explicit requirement\n")
        result = self.command("--resolve-active", "--json", assets=assets)
        self.assertEqual(2, result.returncode)
        self.assertEqual("explicit_runtime_unavailable", json.loads(result.stderr)["code"])
        self.assertEqual(before, pointer.read_bytes())

    def test_real_minor_classes_and_automatic_hint_stability(self):
        second_python = os.environ.get("GURU_RUNTIME_SECOND_PYTHON")
        if not second_python:
            self.skipTest("Provide GURU_RUNTIME_SECOND_PYTHON for a real second interpreter class")
        original = owner.validate_active(self.repo, ASSETS, cache_selection=True)
        other = owner.bootstrap(self.directory / "second-seed", ASSETS, Path(second_python), explicit_python=True)
        self.assertNotEqual(original["runtime_identity"], other["runtime_identity"])
        before = owner.active_pointer_path(self.repo).read_bytes()
        env = {**os.environ, "PATH": str(Path(second_python).parent) + os.pathsep + os.environ["PATH"]}
        resolved = self.command("--resolve-active", "--json", environment=env)
        self.assertEqual(original["runtime_identity"], json.loads(resolved.stdout)["runtime_identity"])
        self.assertEqual(before, owner.active_pointer_path(self.repo).read_bytes())
        owner.bootstrap(self.repo, ASSETS, Path(second_python), explicit_python=True)
        self.assertEqual(other["runtime_identity"], owner.validate_active(self.repo, ASSETS)["runtime_identity"])
        cache = self.repo / "only-other-class"
        shutil.copytree(owner.runtime_target(original["runtime_identity"]), cache / original["runtime_identity"])
        with mock.patch.dict(os.environ, {"GURU_TEAM_PYTHON_CACHE_ROOT": str(cache)}):
            with self.assertRaises(owner.BootstrapError) as raised:
                owner.validate_active(self.repo, ASSETS)
        self.assertEqual("explicit_runtime_unavailable", raised.exception.code)

    def test_default_and_explicit_install_selection_modes_and_failed_repair(self):
        automatic = self.command("--repair", "--json")
        self.assertEqual(0, automatic.returncode, automatic.stderr)
        pointer = owner.active_pointer_path(self.repo)
        self.assertEqual("automatic", json.loads(pointer.read_text())["selection_mode"])
        explicit = self.command("--repair", "--python", sys.executable, "--json")
        self.assertEqual(0, explicit.returncode, explicit.stderr)
        self.assertEqual("explicit", json.loads(pointer.read_text())["selection_mode"])
        before = pointer.read_bytes()
        failed = self.command("--repair", "--python", str(self.repo / "missing-python"), "--json")
        self.assertEqual(2, failed.returncode)
        self.assertEqual("interpreter_unavailable", json.loads(failed.stderr)["code"])
        self.assertEqual(before, pointer.read_bytes())
        self.assertEqual(self.first["interpreter"], owner.validate_active(self.repo, ASSETS)["interpreter"])

    def test_original_v2_producer_valid_and_missing_cache_migrate_once(self):
        source = self.repo / "old-source"
        source.mkdir()
        archive = subprocess.run(["git", "-C", str(ASSETS.parents[3]), "archive",
                                  "610a810d45bb30173906d55c77709389adf1cf31",
                                  "trellis/skills/guru-team/runtime",
                                  "trellis/skills/guru-team/packages/guru-select-workflow-mode",
                                  "trellis/skills/guru-team/schemas"], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as contents:
            contents.extractall(source, filter="data")
        old_assets = source / "trellis/skills/guru-team/runtime"
        legacy_repo = self.repo / "legacy"
        legacy_repo.mkdir()
        produced = subprocess.run([sys.executable, str(old_assets / "bootstrap.py"),
                                   "--repo", str(legacy_repo), "--runtime-assets", str(old_assets),
                                   "--python", sys.executable, "--checkout-local", "--json"],
                                  text=True, capture_output=True)
        self.assertEqual(0, produced.returncode, produced.stdout + produced.stderr)
        legacy_pointer = legacy_repo / ".trellis/.runtime/guru-team/python/active.json"
        pointer = owner.active_pointer_path(legacy_repo)
        before = legacy_pointer.read_bytes()
        self.assertEqual("2.0", json.loads(before)["schema_version"])
        checked = self.command("--check", "--json", repo=legacy_repo)
        self.assertEqual(0, checked.returncode, checked.stderr)
        self.assertFalse(pointer.exists())
        self.assertEqual(before, legacy_pointer.read_bytes())
        resolved = self.command("--resolve-active", "--json", repo=legacy_repo)
        self.assertEqual(self.first["interpreter"], json.loads(resolved.stdout)["interpreter"])
        self.assertEqual("3.0", json.loads(pointer.read_bytes())["schema_version"])
        self.assertEqual(before, legacy_pointer.read_bytes())
        old_resolved = subprocess.run([sys.executable, str(old_assets / "bootstrap.py"),
                                       "--repo", str(legacy_repo), "--runtime-assets", str(old_assets),
                                       "--resolve-active", "--json"], text=True, capture_output=True)
        self.assertEqual(0, old_resolved.returncode, old_resolved.stderr)
        self.assertEqual(self.first["interpreter"], json.loads(old_resolved.stdout)["interpreter"])
        self.assertEqual(before, legacy_pointer.read_bytes())
        # Produce v2 again with the original supported writer, then remove only
        # this test's cache entry. No pointer fabrication is needed.
        missing_repo = self.repo / "missing-legacy"
        missing_repo.mkdir()
        cache = self.repo / "legacy-cache"
        env = {**os.environ, "GURU_TEAM_PYTHON_CACHE_ROOT": str(cache)}
        command = [sys.executable, str(old_assets / "bootstrap.py"), "--repo", str(missing_repo),
                   "--runtime-assets", str(old_assets), "--python", sys.executable,
                   "--checkout-local", "--json"]
        old = subprocess.run(command, text=True, capture_output=True, env=env)
        self.assertEqual(0, old.returncode, old.stdout + old.stderr)
        old_result = json.loads(old.stdout)
        shutil.rmtree(Path(old_result["interpreter"]).parents[2])
        missing = self.command("--check", "--json", repo=missing_repo, environment=env)
        self.assertEqual("managed_runtime_missing", json.loads(missing.stdout)["code"])
        repaired = self.command("--repair", "--json", repo=missing_repo, environment=env)
        self.assertEqual(0, repaired.returncode, repaired.stdout + repaired.stderr)
        self.assertEqual("3.0", json.loads(owner.active_pointer_path(missing_repo).read_bytes())["schema_version"])

    def test_independent_missing_seed_and_lock_source_are_actionable(self):
        env = {**os.environ, "PATH": "", "GURU_TEAM_PYTHON_CACHE_ROOT": str(self.repo / "empty-cache")}
        no_seed = subprocess.run([shutil.which("bash"), str(ASSETS / "manage-python.sh"),
                                  str(self.repo), str(ASSETS), "--check", "--json"],
                                 env=env, text=True, capture_output=True)
        self.assertEqual(2, no_seed.returncode)
        self.assertEqual("interpreter_unavailable", json.loads(no_seed.stderr)["code"])
        owner.bootstrap(self.repo, ASSETS, Path(sys.executable))
        pointer = owner.active_pointer_path(self.repo)
        before = pointer.read_bytes()
        incomplete = self.repo / "incomplete-assets"
        incomplete.mkdir()
        for name in ("bootstrap.py", "bootstrap_check.py", "bootstrap_transport.py", "temporary_lifecycle.py", "temporary-inventory.json", "python-runtime.json", "manage-python.sh"):
            shutil.copy2(ASSETS / name, incomplete / name)
        unchecked_repo = self.repo / "no-selection"
        missing_check = self.command("--check", "--json", repo=unchecked_repo, assets=incomplete)
        self.assertEqual("runtime_assets_missing", json.loads(missing_check.stdout)["code"])
        self.assertEqual("runtime-lock", json.loads(missing_check.stdout)["dependency"])
        self.assertFalse(owner.active_pointer_path(unchecked_repo).exists())
        missing_lock = self.command("--repair", "--python", sys.executable, "--json", assets=incomplete)
        self.assertEqual(2, missing_lock.returncode)
        payload = json.loads(missing_lock.stdout)
        self.assertEqual("runtime_assets_missing", payload["code"])
        self.assertEqual("runtime-lock", payload["dependency"])
        self.assertEqual(before, pointer.read_bytes())

    def test_public_resolver_preserves_business_python_arguments(self):
        arguments = ["--python", "application-value", "--python=another-application-value"]
        result = subprocess.run([str(ASSETS / "resolve-python.sh"), str(self.repo), str(ASSETS),
                                 "-c", "import json,sys; print(json.dumps(sys.argv[1:]))", *arguments],
                                text=True, capture_output=True, env=os.environ.copy())
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(arguments, json.loads(result.stdout))
        # The owner's explicit seed argument still applies before its boundary.
        selected = self.command("--repair", "--python", sys.executable, "--json")
        self.assertEqual(0, selected.returncode, selected.stdout + selected.stderr)
        self.assertEqual(self.first["runtime_identity"], json.loads(selected.stdout)["runtime_identity"])
        self.assertEqual("explicit", owner.read_selection(self.repo)["selection_mode"])

    def test_windows_dispatch_waits_and_preserves_business_streams(self):
        # Exercise the Windows dispatch branch with a real child on this host.
        driver = """
import os, sys
from types import SimpleNamespace
from runtime import bootstrap
def unexpected_exec(*arguments):
    raise AssertionError("Windows dispatch must wait for the selected child")
bootstrap.os = SimpleNamespace(**{**vars(os), "name": "nt", "execv": unexpected_exec})
bootstrap.validate_active = lambda *args, **kwargs: {
    "runtime_identity": "selected-runtime", "interpreter": sys.executable,
}
sys.argv = ["bootstrap.py", *sys.argv[1:]]
raise SystemExit(bootstrap.main())
"""
        business = """
import json, sys
sys.stdout.buffer.write(sys.stdin.buffer.read())
sys.stderr.write(json.dumps(sys.argv[1:], ensure_ascii=False))
raise SystemExit(int(sys.argv[1]))
"""
        payload = "stdin 中文\x00\n".encode("utf-8")
        environment = {**os.environ, "PYTHONPATH": str(ASSETS.parent)}
        for returncode in (0, 2):
            with self.subTest(returncode=returncode):
                arguments = [str(returncode), "中文 空格", "--python=application-value"]
                result = subprocess.run([
                    self.first["interpreter"], "-c", driver,
                    "--repo", str(self.repo), "--runtime-assets", str(ASSETS),
                    "--exec-active", "--", "-c", business, *arguments,
                ], input=payload, capture_output=True, env=environment, check=False)
                self.assertEqual(returncode, result.returncode, result.stderr)
                self.assertEqual(payload, result.stdout)
                self.assertEqual(arguments, json.loads(result.stderr))

    def test_validate_active_rejects_other_available_cache(self):
        second_python = os.environ.get("GURU_RUNTIME_SECOND_PYTHON")
        if not second_python:
            self.skipTest("Provide GURU_RUNTIME_SECOND_PYTHON for two real available caches")
        selected = owner.bootstrap(self.repo, ASSETS, Path(second_python), explicit_python=False)
        self.assertNotEqual(self.first["runtime_identity"], selected["runtime_identity"])
        self.assertTrue(Path(self.first["interpreter"]).is_file())
        pointer = owner.active_pointer_path(self.repo)
        before = pointer.read_bytes()
        rejected = self.command("--validate-active", self.first["runtime_identity"], "--json")
        self.assertEqual(2, rejected.returncode)
        self.assertEqual("managed_runtime_missing", json.loads(rejected.stderr)["code"])
        checked = self.command("--check", "--json")
        self.assertEqual(0, checked.returncode, checked.stdout + checked.stderr)
        self.assertEqual(selected["runtime_identity"], json.loads(checked.stdout)["runtime_identity"])
        self.assertEqual(before, pointer.read_bytes())
        accepted = self.command("--validate-active", selected["runtime_identity"], "--json")
        self.assertEqual(0, accepted.returncode, accepted.stdout + accepted.stderr)
        self.assertEqual(selected["runtime_identity"], json.loads(accepted.stdout)["runtime_identity"])
        self.assertEqual(before, pointer.read_bytes())

    def test_cache_order_is_stable_when_no_hint_exists(self):
        ids = ["b" * 24, "a" * 24]
        cache = self.repo / "cache"
        for value in ids:
            (cache / value).mkdir(parents=True)
        selection_class = {"python_minor": 12}
        def resolve(assets, value):
            return {"status": "ok", "runtime_identity": value, "interpreter": value}
        real_read = owner.read_json
        def read(path):
            return {"identity": selection_class} if path.name == "metadata.json" else real_read(path)
        with mock.patch.object(owner, "user_cache_root", return_value=cache), \
             mock.patch.object(owner, "resolve_runtime", side_effect=resolve), \
             mock.patch.object(owner, "read_json", side_effect=read):
            selected = owner.validate_active(self.repo, ASSETS)
        self.assertEqual("a" * 24, selected["runtime_identity"])


if __name__ == "__main__":
    unittest.main()
