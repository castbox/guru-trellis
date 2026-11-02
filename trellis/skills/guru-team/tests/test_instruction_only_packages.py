from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / "trellis/skills/guru-team"
sys.path.insert(0, str(SKILLS))
sys.path.insert(0, str(REPO / "trellis/presets/guru-team/scripts/python"))
from runtime.discovery import discover  # noqa: E402
from runtime.io import CommandError  # noqa: E402
from runtime.validate import validate, validate_instruction_package, validate_interface_contract  # noqa: E402
import apply_guru_team_trellis_preset as preset  # noqa: E402


IDS = ("guru-orchestrate-issue-dag", "guru-orchestrate-issue-sequence")


class InstructionOnlyPackageTests(unittest.TestCase):
    def package(self, package_id: str):
        row = next(row for row in json.loads((SKILLS / "registry.json").read_text())["skills"] if row["id"] == package_id)
        package = SKILLS / row["package"]
        interface = json.loads((package / "interface.json").read_text())
        return row, package, interface

    def test_native_conversation_contract_discovers_without_a_cli_wrapper(self) -> None:
        for package_id in IDS:
            with self.subTest(package=package_id):
                row, package, interface = self.package(package_id)
                validate_interface_contract(SKILLS, package, row, interface)
                validate_instruction_package(package, row, interface, source=True)
                result = discover(SKILLS, package_id)
                self.assertEqual(result["input"]["kind"], "conversation")
                self.assertEqual(result["invocation"], {"kind": "agent", "entrypoint": "SKILL.md", "explicit_only": True})
                self.assertEqual([item["exit_id"] for item in result["outputs"]], [item["id"] for item in interface["external_exits"]])
                for legacy_asset in ("commands.json", "scripts", "runtime", "errors"):
                    self.assertFalse((package / legacy_asset).exists())

    def test_command_interfaces_keep_their_existing_required_runtime_contract(self) -> None:
        package_id = "guru-review-change"
        row, package, interface = self.package(package_id)
        incomplete = copy.deepcopy(interface)
        del incomplete["validators"]
        with self.assertRaises(CommandError) as result:
            validate_interface_contract(SKILLS, package, row, incomplete)
        self.assertEqual(result.exception.code, "schema_mismatch")

    def test_omitted_native_explicit_policy_is_a_package_error(self) -> None:
        row, package, interface = self.package(IDS[0])
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / package.name
            shutil.copytree(package, candidate)
            metadata = candidate / "agents/openai.yaml"
            metadata.write_text("interface:\n  display_name: Orchestrator\n", encoding="utf-8")
            with self.assertRaises(CommandError) as result:
                validate_instruction_package(candidate, row, interface, source=True)
        self.assertEqual(result.exception.code, "projection_invalid")

    def test_installer_preserves_metadata_and_only_projects_to_codex(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installed = root / ".trellis/guru-team"
            result = preset.install_skill_packages(root, REPO, installed, {"codex", "claude"}, None)
            self.assertEqual(result["status"], "ok", result["conflicts"])
            for package_id in IDS:
                row, package, interface = self.package(package_id)
                projected = root / ".codex/skills" / package_id
                self.assertEqual((projected / "agents/openai.yaml").read_bytes(), (package / "agents/openai.yaml").read_bytes())
                self.assertFalse((projected / "tests").exists())
                runtime_package = installed / "skills/packages" / package_id
                self.assertFalse((runtime_package / "tests").exists())
                validate_instruction_package(runtime_package, row, interface, source=False)
                self.assertFalse((root / ".agents/skills" / package_id).exists())
                self.assertFalse((root / ".claude/skills" / package_id).exists())
            for relative in (".agents/skills", ".claude/skills", ".codex/skills"):
                self.assertEqual(validate(REPO, "source", root / relative)["status"], "passed")
            misplaced = root / ".claude/skills" / IDS[0]
            shutil.copytree(root / ".codex/skills" / IDS[0], misplaced)
            with self.assertRaises(CommandError) as failure:
                validate(REPO, "source", root / ".claude/skills")
            self.assertEqual(failure.exception.code, "projection_invalid")
            shutil.rmtree(misplaced)
            reapplied = preset.install_skill_packages(root, REPO, installed, {"codex", "claude"}, {"skill_packages": result})
            self.assertEqual(reapplied["status"], "ok", reapplied["conflicts"])
            self.assertEqual(reapplied["sidecars"], [])
            switched = preset.install_skill_packages(root, REPO, installed, {"claude"}, {"skill_packages": reapplied})
            self.assertEqual(switched["status"], "ok", switched["conflicts"])
            for package_id in IDS:
                self.assertFalse((root / ".codex/skills" / package_id).exists())
                self.assertTrue((installed / "skills/packages" / package_id / "SKILL.md").is_file())
            restored = preset.install_skill_packages(root, REPO, installed, {"codex", "claude"}, {"skill_packages": switched})
            self.assertEqual(restored["status"], "ok", restored["conflicts"])
            # An ordinary local metadata edit uses the existing conflict path.
            metadata = root / ".codex/skills" / IDS[0] / "agents/openai.yaml"
            edited = metadata.read_text() + "# local display preference\n"
            metadata.write_text(edited, encoding="utf-8")
            conflicted = preset.install_skill_packages(root, REPO, installed, {"codex", "claude"}, {"skill_packages": restored})
            self.assertEqual(conflicted["status"], "conflict")
            self.assertEqual(metadata.read_text(), edited)
            self.assertIn(metadata.relative_to(root).as_posix() + ".new", conflicted["sidecars"])


if __name__ == "__main__":
    unittest.main()
