"""Behavior regressions for Guru product filtering and documented syntax checks."""

from __future__ import annotations

import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(REPO / "trellis/skills/guru-team"))

import apply_guru_team_trellis_preset as installer
import verify_dogfood_platform_selection as dogfood
from runtime import bootstrap_check, eval_runner, installed


def snapshot(root: Path) -> dict[str, tuple[bytes, int, int]]:
    return {
        path.relative_to(root).as_posix(): (
            path.read_bytes(), path.stat().st_mode, path.stat().st_mtime_ns
        )
        for path in root.rglob("*") if path.is_file()
    }


def compile_caches(source: Path) -> None:
    # Explicit compilation is confined to disposable regression fixtures.
    py_compile.compile(str(source), doraise=True)
    for suffix in (".pyc", ".pyo"):
        py_compile.compile(str(source), cfile=str(source.with_suffix(suffix)), doraise=True)


class BytecodeHygieneTests(unittest.TestCase):
    def test_complete_verify_on_real_installed_projections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            manifest = Path(".trellis/guru-team/extension.json")
            (repo / manifest).parent.mkdir(parents=True)
            shutil.copy2(REPO / manifest, repo / manifest)
            roots = {Path(".agents/skills")}
            for flag in dogfood.DOGFOOD_PLATFORM_FLAGS:
                roots.update(dogfood.PLATFORM_BY_FLAG[flag].skill_roots)
                entry = Path(dogfood.DESCRIPTORS_BY_FLAG[flag]["entry_path"])
                (repo / entry).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(REPO / entry, repo / entry)
                canonical = Path("trellis/presets/guru-team/overlays") / entry
                (repo / canonical).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(REPO / canonical, repo / canonical)
            for root in roots:
                for package in (REPO / root).glob("guru-*"):
                    shutil.copytree(package, repo / root / package.name)
            self.assertEqual(dogfood.verify(repo)["status"], "ok")
            sources = [repo / root / "guru-check-task/evals/files/native-range-boundary.py"
                       for root in sorted(roots)]
            for source in sources:
                compile_caches(source)
            before = snapshot(repo)
            self.assertEqual(dogfood.verify(repo)["status"], "ok")
            self.assertEqual(snapshot(repo), before)
            # Recompile changed disposable source, then restore its product bytes.
            for source in sources:
                original = source.read_bytes()
                source.write_bytes(original + b"\n# changed cache payload\n")
                compile_caches(source)
                source.write_bytes(original)
                py_compile.compile(str(source), cfile=str(source.parent / "extra.pyo"), doraise=True)
            before = snapshot(repo)
            self.assertEqual(dogfood.verify(repo)["status"], "ok")
            self.assertEqual(snapshot(repo), before)
            product = repo / ".codex/skills/guru-check-task/SKILL.md"
            original = product.read_bytes()
            product.write_bytes(original + b"\nChanged product.\n")
            with self.assertRaisesRegex(dogfood.DogfoodDriftError, "byte drift"):
                dogfood.verify(repo)
            product.write_bytes(original)
            product.unlink()
            with self.assertRaisesRegex(dogfood.DogfoodDriftError, "file set drift"):
                dogfood.verify(repo)

    def test_existing_selectors_and_digest_keep_their_scopes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "package"
            shutil.copytree(REPO / "trellis/skills/guru-team/packages/guru-check-task", package)
            source = package / "evals/files/native-range-boundary.py"
            errors: list[str] = []
            def inventories():
                return (installer.skill_package_source_files(package),
                        installed.collect_files(root, package, "fixture", errors),
                        eval_runner.tree_sha256(package))
            baseline = inventories()
            compile_caches(source)
            before = snapshot(package)
            self.assertEqual(inventories(), baseline)
            self.assertEqual(snapshot(package), before)
            source.write_bytes(source.read_bytes() + b"\n# product change\n")
            self.assertNotEqual(inventories()[2], baseline[2])
            source.unlink()
            changed = inventories()
            self.assertNotEqual(changed[0], baseline[0])
            self.assertNotEqual(changed[1], baseline[1])
            self.assertNotEqual(changed[2], baseline[2])
            self.assertEqual(errors, [])
            private = package / "tests/bytecode-scope-fixture.py"
            private.parent.mkdir(exist_ok=True)
            before_digest = eval_runner.tree_sha256(package)
            private.write_text("value = 1\n")
            self.assertIn(private, installer.skill_package_source_files(package))
            self.assertIn(private, installed.collect_files(root, package, "fixture", errors))
            self.assertEqual(eval_runner.tree_sha256(package), before_digest)

    def test_bootstrap_product_copy_excludes_caches_and_preserves_runtime_cache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            assets = root / "skills/runtime"
            package = assets.parent / "packages/example"
            schemas = assets.parent / "schemas"
            for tree in (assets, package, schemas):
                tree.mkdir(parents=True)
                source = tree / "module.py"
                source.write_text("value = 1\n")
                compile_caches(source)
                (tree / "tests").mkdir()
                (tree / "tests/private.txt").write_text("private")
            (package / "scripts").mkdir()
            (package / "scripts/invoke.sh").write_text("unused")
            check = {"package": "example", "cases": [{"arguments": [], "expected_returncode": 0,
                                                       "expected_output": {"exit_id": "blocked"}}]}
            (assets / "python-runtime.json").write_text(json.dumps({"public_wrapper_check": check}))
            target = root / "target"
            target.mkdir()
            cache_source = target / "dependency.py"
            cache_source.write_text("value = 2\n")
            compile_caches(cache_source)
            before = snapshot(root)
            def observe(argv, **kwargs):
                view = Path(kwargs["cwd"])
                for relative in ("runtime", "skills/packages/example", "skills/schemas"):
                    tree = view / ".trellis/guru-team" / relative
                    self.assertEqual((tree / "module.py").read_text(), "value = 1\n")
                    self.assertEqual({path.suffix for path in tree.rglob("*") if path.is_file()}
                                     & {".pyc", ".pyo"}, set())
                    self.assertFalse((tree / "__pycache__").exists())
                    self.assertFalse((tree / "tests").exists())
                self.assertEqual(snapshot(view / "cache/fixture"), snapshot(target))
                return subprocess.CompletedProcess(argv, 0, '{"exit_id":"blocked"}', "")
            # Only the external wrapper is replaced; all product copies run normally.
            with mock.patch.object(bootstrap_check.subprocess, "run", side_effect=observe) as run:
                bootstrap_check.check_public_wrapper(assets, "fixture", target)
            self.assertEqual(run.call_count, 1)
            self.assertEqual(snapshot(root), before)

    def test_documented_memory_compile_checks_syntax_without_execution_or_writes(self) -> None:
        guidance = REPO / "trellis/presets/guru-team/spec/workflow/quality-guidelines.md"
        blocks = re.findall(r"```bash\n(.*?)\n```", guidance.read_text(), re.DOTALL)
        commands = [block for block in blocks if "compile(" in block]
        self.assertEqual(len(commands), 1, "expected the one documented memory syntax command")
        command = commands[0]
        paths = (
            "trellis/skills/guru-team/runtime/example.py",
            "trellis/skills/guru-team/packages/example/runtime/example.py",
            "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in paths:
                source = root / relative
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text("raise RuntimeError('module must not execute')\n")
                compile_caches(source)
            before = snapshot(root)
            def execute():
                return subprocess.run(["bash", "-c", command], cwd=root, capture_output=True,
                                      text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
            result = execute()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(snapshot(root), before)
            for relative in paths:
                source = root / relative
                original = source.read_bytes()
                source.write_text("def broken(:\n")
                before = snapshot(root)
                result = execute()
                self.assertNotEqual(result.returncode, 0, relative)
                self.assertIn(relative, result.stderr)
                self.assertIn("SyntaxError", result.stderr)
                self.assertEqual(snapshot(root), before)
                source.write_bytes(original)


if __name__ == "__main__":
    unittest.main()
