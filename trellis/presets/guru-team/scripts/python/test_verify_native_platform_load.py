from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).with_name("verify_native_platform_load.py")
SPEC = importlib.util.spec_from_file_location("verify_native_platform_load", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load native platform verifier")
NATIVE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(NATIVE)


class NativePlatformLoadTests(unittest.TestCase):
    def fixture(self, root: Path) -> Path:
        target = root / "project"
        skill = target / ".opencode/skills/guru-example/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("---\nname: guru-example\ndescription: Fixture.\n---\n", encoding="utf-8")
        command = target / ".opencode/commands/guru-finish-work.md"
        command.parent.mkdir(parents=True)
        command.write_text("# Guru Finish Work\n", encoding="utf-8")
        registry = target / ".trellis/guru-team/skills/registry.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(
            json.dumps({"skills": [{"id": "guru-example", "state": "active"}]}),
            encoding="utf-8",
        )
        return target

    def catalogs(self, target: Path):
        return (
            [{
                "name": "guru-example",
                "location": str(target / ".opencode/skills/guru-example/SKILL.md"),
            }],
            [{"name": "guru-finish-work", "template": "# Guru Finish Work"}],
            "1.18.30",
        )

    def test_opencode_native_discovery_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = self.fixture(root)
            with mock.patch.object(NATIVE.shutil, "which", return_value="/fixture/opencode"), mock.patch.object(
                NATIVE, "_load_opencode_catalogs", return_value=self.catalogs(target)
            ):
                result = NATIVE.verify_native_platform_load(target, "opencode", root / "work")
            self.assertEqual(result["status"], "passed")
            self.assertEqual(result["skills"], ["guru-example"])
            self.assertEqual(result["default_selected_roots"], {"native": 1})
            self.assertEqual(result["native_only_skill_count"], 1)
            self.assertEqual(result["command"], "guru-finish-work")

    def test_opencode_default_discovery_accepts_byte_identical_shared_projection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = self.fixture(root)
            shared = target / ".agents/skills/guru-example/SKILL.md"
            shared.parent.mkdir(parents=True)
            shared.write_bytes((target / ".opencode/skills/guru-example/SKILL.md").read_bytes())

            def catalogs(_executable, _target, environment, _work_root, _log_name):
                location = (
                    target / ".opencode/skills/guru-example/SKILL.md"
                    if environment.get("OPENCODE_DISABLE_EXTERNAL_SKILLS") == "1"
                    else shared
                )
                return (
                    [{"name": "guru-example", "location": str(location)}],
                    [{"name": "guru-finish-work", "template": "# Guru Finish Work"}],
                    "1.18.30",
                )

            with mock.patch.object(NATIVE.shutil, "which", return_value="/fixture/opencode"), mock.patch.object(
                NATIVE, "_load_opencode_catalogs", side_effect=catalogs
            ):
                result = NATIVE.verify_native_platform_load(target, "opencode", root / "work")
            self.assertEqual(result["default_selected_roots"], {"shared": 1})

    def test_opencode_default_discovery_accepts_byte_identical_claude_projection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = self.fixture(root)
            claude = target / ".claude/skills/guru-example/SKILL.md"
            claude.parent.mkdir(parents=True)
            claude.write_bytes((target / ".opencode/skills/guru-example/SKILL.md").read_bytes())

            def catalogs(_executable, _target, environment, _work_root, _log_name):
                location = (
                    target / ".opencode/skills/guru-example/SKILL.md"
                    if environment.get("OPENCODE_DISABLE_EXTERNAL_SKILLS") == "1"
                    else claude
                )
                return (
                    [{"name": "guru-example", "location": str(location)}],
                    [{"name": "guru-finish-work", "template": "# Guru Finish Work"}],
                    "1.18.30",
                )

            with mock.patch.object(NATIVE.shutil, "which", return_value="/fixture/opencode"), mock.patch.object(
                NATIVE, "_load_opencode_catalogs", side_effect=catalogs
            ):
                result = NATIVE.verify_native_platform_load(target, "opencode", root / "work")
            self.assertEqual(result["default_selected_roots"], {"claude": 1})

    def test_opencode_skill_location_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = self.fixture(root)
            with mock.patch.object(NATIVE.shutil, "which", return_value="/fixture/opencode"), mock.patch.object(
                NATIVE,
                "_load_opencode_catalogs",
                return_value=([{"name": "guru-example", "location": "/wrong/SKILL.md"}], [], "1.18.30"),
            ), self.assertRaisesRegex(NATIVE.NativeLoadError, "unexpected location"):
                NATIVE.verify_native_platform_load(target, "opencode", root / "work")

    def test_opencode_discovery_does_not_reuse_a_previous_home(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = self.fixture(root)
            work = root / "work"
            stale_home = work / "opencode-home"
            stale_home.mkdir(parents=True)
            (stale_home / "stale-catalog").write_text("old", encoding="utf-8")
            observed_homes = []

            def catalogs(_executable, _target, environment, _work_root, _log_name):
                observed_homes.append(Path(environment["HOME"]))
                self.assertFalse((Path(environment["HOME"]) / "stale-catalog").exists())
                return self.catalogs(target)

            with mock.patch.object(NATIVE.shutil, "which", return_value="/fixture/opencode"), mock.patch.object(
                NATIVE, "_load_opencode_catalogs", side_effect=catalogs
            ):
                NATIVE.verify_native_platform_load(target, "opencode", work)
                NATIVE.verify_native_platform_load(target, "opencode", work)

            self.assertEqual(len(observed_homes), 4)
            self.assertEqual(len(set(observed_homes)), 4)
            self.assertTrue(all(home.parent == work for home in observed_homes))
            self.assertTrue(all(not home.exists() for home in observed_homes))

    def test_other_platform_is_not_applicable(self) -> None:
        result = NATIVE.verify_native_platform_load(Path("/unused"), "codex", Path("/unused"))
        self.assertEqual(result, {"status": "not_applicable", "platform": "codex"})
