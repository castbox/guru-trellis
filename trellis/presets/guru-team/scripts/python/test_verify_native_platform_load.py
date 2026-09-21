from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).with_name("verify_native_platform_load.py")
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("verify_native_platform_load", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load native platform verifier")
NATIVE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(NATIVE)


class NativePlatformLoadTests(unittest.TestCase):
    def fixture(self, root: Path, platform: str) -> Path:
        target = root / "project"
        descriptor = NATIVE.DESCRIPTORS_BY_FLAG[platform]
        core = NATIVE.PLATFORM_BY_FLAG[platform]
        roots = tuple(dict.fromkeys((Path(".agents/skills"), *core.skill_roots)))
        content = "---\nname: guru-example\ndescription: Fixture.\n---\n"
        for relative_root in roots:
            skill = target / relative_root / "guru-example/SKILL.md"
            skill.parent.mkdir(parents=True, exist_ok=True)
            skill.write_text(content, encoding="utf-8")
        entry = target / descriptor["entry_path"]
        entry.parent.mkdir(parents=True, exist_ok=True)
        entry.write_text("# Guru Finish Work\n", encoding="utf-8")
        registry = target / ".trellis/guru-team/skills/registry.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(
            json.dumps({"skills": [{"id": "guru-example", "state": "active"}]}),
            encoding="utf-8",
        )
        manifest = {
            section: {"selected_platforms": [platform]}
            for section in ("install", "skill_packages", "overlays")
        }
        (target / ".trellis/guru-team/extension.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        return target

    @staticmethod
    def catalogs(target: Path):
        return (
            [{
                "name": "guru-example",
                "location": str(target / ".opencode/skills/guru-example/SKILL.md"),
            }],
            [{"name": "guru-finish-work", "template": "# Guru Finish Work"}],
            "1.18.30",
        )

    def test_every_platform_has_projection_parity(self) -> None:
        for platform in NATIVE.PLATFORM_BY_FLAG:
            if platform == "opencode":
                continue
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                target = self.fixture(root, platform)
                result = NATIVE.verify_native_platform_load(target, platform, root / "work")
                self.assertEqual(result["status"], "passed")
                self.assertEqual(result["actual_load"], "projection_parity")
                self.assertEqual(result["selected_platforms"], [platform])
                self.assertEqual(result["package_private_tests"], "excluded")

    def test_opencode_native_discovery_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = self.fixture(root, "opencode")
            with mock.patch.object(NATIVE.shutil, "which", return_value="/fixture/opencode"), mock.patch.object(
                NATIVE, "_load_opencode_catalogs", return_value=self.catalogs(target)
            ):
                result = NATIVE.verify_native_platform_load(target, "opencode", root / "work")
            self.assertEqual(result["status"], "passed")
            self.assertEqual(result["actual_load"], "opencode_catalog")
            self.assertEqual(result["skills"], ["guru-example"])
            self.assertEqual(result["default_selected_roots"], {"native": 1})
            self.assertEqual(result["command"], "guru-finish-work")

    def test_package_private_tests_fail_for_any_platform(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = self.fixture(root, "cursor")
            leaked = target / ".cursor/skills/guru-example/tests/test_private.py"
            leaked.parent.mkdir(parents=True)
            leaked.write_text("raise AssertionError\n", encoding="utf-8")
            with self.assertRaisesRegex(NATIVE.NativeLoadError, "package-private tests"):
                NATIVE.verify_native_platform_load(target, "cursor", root / "work")

    def test_manifest_selection_must_match_requested_platform(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = self.fixture(root, "cursor")
            with self.assertRaisesRegex(NATIVE.NativeLoadError, "exact selected platform"):
                NATIVE.verify_native_platform_load(target, "codex", root / "work")

    def test_unknown_platform_fails(self) -> None:
        with self.assertRaisesRegex(NATIVE.NativeLoadError, "unknown platform"):
            NATIVE.verify_native_platform_load(Path("/unused"), "unknown", Path("/unused"))


if __name__ == "__main__":
    unittest.main()
