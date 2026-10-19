"""Exercise managed LF policy through real Git checkout and installer entries."""
from __future__ import annotations

import importlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE_ROOT = Path(os.environ.get("GURU_NATIVE_TARGET_ROOT", Path(__file__).resolve().parents[5])).resolve()


def run(command: list[str], cwd: Path, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=cwd, capture_output=True, **kwargs)


def git(root: Path, *args: str) -> bytes:
    result = run(["git", "-c", "core.longpaths=true", *args], root)
    if result.returncode:
        raise AssertionError(result.stderr.decode("utf-8"))
    return result.stdout


def commit(root: Path) -> None:
    git(root, "add", "--all")
    git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "managed fixture")


class ManagedTextEolTests(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(SOURCE_ROOT / "trellis/presets/guru-team/scripts/python"))
        self.preset = importlib.import_module("apply_guru_team_trellis_preset")
        self.eol = importlib.import_module("managed_text_eol")
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_canonical_checkout_policy_preserves_text_and_lock_bytes(self):
        seed = self.root / "canonical"
        seed.mkdir()
        git(seed, "init", "-q")
        git(seed, "config", "core.autocrlf", "false")
        shutil.copyfile(SOURCE_ROOT / ".gitattributes", seed / ".gitattributes")
        relatives = (
            "trellis/skills/guru-team/registry.json",
            "trellis/skills/guru-team/runtime/requirements.lock",
            "trellis/presets/guru-team/source/trellis-source.json",
            "trellis/presets/guru-team/spec/workflow/clear-technical-writing.md",
            "trellis/workflows/guru-team/workflow.md",
        )
        for relative in relatives:
            destination = seed / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE_ROOT / relative, destination)
        commit(seed)
        checkout = self.root / "canonical-clone"
        git(self.root, "clone", "--quiet", "--no-local", "--config", "core.autocrlf=true", str(seed), str(checkout))
        for relative in relatives:
            self.assertEqual((checkout / relative).read_bytes(), (SOURCE_ROOT / relative).read_bytes(), relative)

    def test_normal_old_checkout_recovers_and_upgrade_preserves_raw_backup(self):
        source = self.root / "canonical.md"
        source.write_bytes("中文 contract\n".encode("utf-8"))
        seed = self.root / "seed"
        seed.mkdir()
        git(seed, "init", "-q")
        relative = Path(".agents/skills/guru-example/SKILL.md")
        first = self.preset.copy_provenance_managed(source, seed / relative, seed, {}, True)
        commit(seed)
        for upgrade in (False, True):
            with self.subTest(upgrade=upgrade):
                checkout = self.root / ("upgrade" if upgrade else "same")
                git(self.root, "clone", "--quiet", "--no-local", "--config", "core.autocrlf=true", str(seed), str(checkout))
                target = checkout / relative
                original = target.read_bytes()
                self.assertIn(b"\r\n", original)
                if upgrade:
                    source.write_bytes("中文 contract\nnew behavior\n".encode("utf-8"))
                result = self.preset.copy_provenance_managed(source, target, checkout, {relative.as_posix(): first["sha256"]}, True)
                self.assertEqual(result["action"], "updated_managed")
                self.assertEqual(target.read_bytes(), source.read_bytes())
                if upgrade:
                    self.assertEqual(target.with_name("SKILL.md.bak").read_bytes(), original)
                else:
                    self.assertFalse(target.with_name("SKILL.md.bak").exists())

    def test_content_edit_and_lock_keep_original_conflict_behavior(self):
        for filename in ("SKILL.md", "requirements.lock"):
            with self.subTest(filename=filename):
                source = self.root / filename
                source.write_bytes(b"managed\n")
                repo = self.root / filename.replace(".", "-")
                repo.mkdir()
                target = repo / filename
                first = self.preset.copy_provenance_managed(source, target, repo, {}, True)
                target.write_bytes(b"managed\r\n" + (b"user edit\r\n" if filename.endswith("md") else b""))
                before = target.read_bytes()
                result = self.preset.copy_provenance_managed(source, target, repo, {filename: first["sha256"]}, True)
                self.assertEqual(result["action"], "conflict")
                self.assertEqual(target.read_bytes(), before)
                self.assertEqual(target.with_name(filename + ".new").read_bytes(), source.read_bytes())

    def test_attributes_preserve_user_bytes_and_detect_real_nested_and_info_rules(self):
        repo = self.root / "repo"
        repo.mkdir()
        git(repo, "init", "-q")
        stage = self.root / "stage"
        stage.mkdir()
        original = b"# user comment\r\n*.custom -text\r\n"
        (repo / ".gitattributes").write_bytes(original)
        path = Path(".trellis/guru-team/runtime/probe.py")
        paths = {path, Path(".trellis/guru-team/runtime/requirements.lock")}
        self.eol.prepare_attributes(repo, stage, paths)
        content = (stage / ".gitattributes").read_bytes()
        self.assertTrue(content.startswith(original))
        content += b"# trailing user bytes\r\n"
        self.assertEqual(self.eol.render_attributes(content, paths), content)
        with self.assertRaisesRegex(SystemExit, "malformed"):
            self.eol.render_attributes(content + self.eol.START + b"\n", paths)
        nested = repo / ".trellis/guru-team/.gitattributes"
        nested.parent.mkdir(parents=True)
        nested.write_bytes(b"*.py text eol=crlf\n")
        with self.assertRaisesRegex(SystemExit, "eol=crlf"):
            self.eol.prepare_attributes(repo, stage, paths)
        nested.unlink()
        (stage / nested.relative_to(repo)).unlink()
        (repo / ".git/info/attributes").write_bytes(b"*.py -text\n")
        with self.assertRaisesRegex(SystemExit, "text=unset"):
            self.eol.prepare_attributes(repo, stage, paths)


class ManagedTextInstallTests(unittest.TestCase):
    def test_real_install_clone_validate_reapply(self):
        """Existing initialized upstream fixture; no CLI-init or Agent claim."""
        with tempfile.TemporaryDirectory(prefix="guru-native-eol-") as temporary:
            root = Path(temporary)
            seed = root / "中文 seed"
            seed.mkdir()
            git(seed, "init", "-q")
            trellis = seed / ".trellis"
            trellis.mkdir()
            upstream_scripts = Path(os.environ.get("GURU_UPSTREAM_DELIVERY_SCRIPTS", SOURCE_ROOT / ".trellis/scripts")).resolve()
            upstream_version = upstream_scripts.parent / ".version"
            lock = json.loads((SOURCE_ROOT / "trellis/presets/guru-team/source/trellis-source.json").read_bytes())
            self.assertEqual(upstream_version.read_text(encoding="utf-8").strip(), lock["cli_version"], "fixture requires actually installed source-locked upstream scripts")
            shutil.copytree(upstream_scripts, trellis / "scripts", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copyfile(upstream_version, trellis / ".version")
            (trellis / "workflow.md").write_bytes((SOURCE_ROOT / "trellis/workflows/guru-team/workflow.md").read_bytes())
            (seed / ".gitattributes").write_bytes(b"# user-owned rule\r\n*.custom -text\r\n")
            installer = SOURCE_ROOT / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"
            environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}

            def apply(target):
                result = run([sys.executable, str(installer), "--repo", str(target), "--python", sys.executable, "--platform", "codex", "--json"], SOURCE_ROOT, env=environment)
                self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8") + result.stdout.decode("utf-8")[-3000:])
                payload = json.loads(result.stdout)
                self.assertEqual(payload["guru_team_extension"]["target_trellis_cli"], lock["cli_version"])
                self.assertEqual(payload["guru_team_extension"]["tested_trellis_cli"], [lock["cli_version"]])
                return payload

            apply(seed)
            original = (seed / ".gitattributes").read_bytes()
            self.assertTrue(original.startswith(b"# user-owned rule\r\n*.custom -text\r\n"))
            # Keep the mixed user-owned attributes file exact in this fixture.
            git(seed, "config", "core.autocrlf", "false")
            commit(seed)
            for autocrlf in ("true", "false"):
                with self.subTest(autocrlf=autocrlf):
                    checkout = root / ("clone-" + autocrlf)
                    git(root, "clone", "--quiet", "--no-local", "--config", "core.autocrlf=" + autocrlf, str(seed), str(checkout))
                    for relative in (".trellis/spec/workflow/clear-technical-writing.md", ".trellis/guru-team/skills/registry.json"):
                        self.assertNotIn(b"\r\n", (checkout / relative).read_bytes(), "normal_checkout_raw_drift: " + relative)
                    runtime = checkout / ".trellis/guru-team"
                    validation = run([sys.executable, "-m", "runtime.validate", "--json", "--mode", "installed", "--root", str(checkout)], checkout, env={**environment, "PYTHONPATH": str(runtime)})
                    self.assertEqual(validation.returncode, 0, validation.stdout.decode("utf-8")[-3000:] + validation.stderr.decode("utf-8"))
                    result = apply(checkout)
                    self.assertEqual(result["skill_installed_validation"]["returncode"], 0)
                    self.assertEqual(result["managed_backups"], [])
                    self.assertFalse(list(runtime.rglob("*.new")))
                    self.assertFalse(list(runtime.rglob("*.bak")))
                    if autocrlf == "true":
                        pointer = checkout / ".git/guru-team/python/active.json"
                        pointer_before = pointer.read_bytes()
                        attributes_before = (checkout / ".gitattributes").read_bytes()
                        registry_before = (runtime / "skills/registry.json").read_bytes()
                        (runtime / ".gitattributes").write_bytes(b"*.json text eol=crlf\n")
                        blocked = run([sys.executable, str(installer), "--repo", str(checkout), "--python", sys.executable, "--platform", "codex"], SOURCE_ROOT, env=environment)
                        self.assertNotEqual(blocked.returncode, 0)
                        self.assertIn(b"managed_text_attributes_conflict", blocked.stderr)
                        self.assertEqual(pointer.read_bytes(), pointer_before)
                        self.assertEqual((checkout / ".gitattributes").read_bytes(), attributes_before)
                        self.assertEqual((runtime / "skills/registry.json").read_bytes(), registry_before)


if __name__ == "__main__":
    unittest.main()
