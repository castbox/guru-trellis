from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
import unittest

import apply_guru_team_trellis_preset as preset
import verify_dogfood_platform_selection as dogfood


REPO = Path(__file__).resolve().parents[5]
PACKAGE_IDS = ("guru-check-task", "guru-orchestrate-issue-dag", "guru-orchestrate-issue-sequence")
ROOTS = (".agents/skills", ".claude/skills", ".codex/skills", ".cursor/skills")


class DogfoodPlatformSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        canonical = REPO / "trellis/skills/guru-team"
        selected = self.repo / "trellis/skills/guru-team"
        selected.mkdir(parents=True)
        registry = json.loads((canonical / "registry.json").read_text())
        registry["skills"] = [row for row in registry["skills"] if row["id"] in PACKAGE_IDS]
        (selected / "registry.json").write_text(json.dumps(registry), encoding="utf-8")
        for entry in registry["skills"]:
            package = canonical / entry["package"]
            roots = ROOTS if entry["id"] == "guru-check-task" else (".codex/skills",)
            for source in preset.skill_platform_public_files(package):
                inner = source.relative_to(package)
                for target in [selected / entry["package"] / inner, *[self.repo / root / entry["id"] / inner for root in roots]]:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
        manifest = self.repo / ".trellis/guru-team/extension.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({section: {"selected_platforms": list(dogfood.DOGFOOD_PLATFORM_FLAGS)} for section in ("install", "skill_packages", "overlays")}), encoding="utf-8")
        for flag in dogfood.DOGFOOD_PLATFORM_FLAGS:
            entry = Path(dogfood.DESCRIPTORS_BY_FLAG[flag]["entry_path"])
            source = REPO / "trellis/presets/guru-team/overlays" / entry
            for target in (self.repo / entry, self.repo / "trellis/presets/guru-team/overlays" / entry):
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

    def test_mixed_common_and_codex_only_packages_have_distinct_valid_roots(self) -> None:
        self.assertEqual(dogfood.verify(self.repo)["status"], "ok")
        for package_id in PACKAGE_IDS[1:]:
            self.assertTrue((self.repo / ".codex/skills" / package_id / "agents/openai.yaml").is_file())
            self.assertFalse((self.repo / ".agents/skills" / package_id).exists())

    def test_codex_only_package_in_shared_or_claude_root_is_rejected(self) -> None:
        package_id = PACKAGE_IDS[1]
        for root in (".agents/skills", ".claude/skills"):
            with self.subTest(root=root):
                misplaced = self.repo / root / package_id
                shutil.copytree(self.repo / ".codex/skills" / package_id, misplaced)
                with self.assertRaisesRegex(dogfood.DogfoodDriftError, "file set drift"):
                    dogfood.verify(self.repo)
                shutil.rmtree(misplaced)

    def test_identical_common_package_edit_across_roots_still_differs_from_source(self) -> None:
        for root in ROOTS:
            path = self.repo / root / "guru-check-task/SKILL.md"
            path.write_bytes(path.read_bytes() + b"\nStale projected content.\n")
        with self.assertRaisesRegex(dogfood.DogfoodDriftError, "byte drift"):
            dogfood.verify(self.repo)

    def test_codex_only_metadata_is_required_in_its_own_projection(self) -> None:
        (self.repo / ".codex/skills" / PACKAGE_IDS[1] / "agents/openai.yaml").unlink()
        with self.assertRaisesRegex(dogfood.DogfoodDriftError, "file set drift"):
            dogfood.verify(self.repo)


if __name__ == "__main__":
    unittest.main()
