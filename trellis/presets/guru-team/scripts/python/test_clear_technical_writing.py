#!/usr/bin/env python3
"""Verify writing-standard distribution through the existing preset installer."""

from __future__ import annotations

import json
import re
import tomllib
import unittest

import test_apply_guru_team_trellis_preset as installer_tests


setUpModule = installer_tests.setUpModule
tearDownModule = installer_tests.tearDownModule
preset = installer_tests.preset


class ClearTechnicalWritingInstallerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = installer_tests.PlatformOverlayInstallerTest()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.repo = self.fixture.repo
        self.guru_root = self.fixture.guru_root
        self.install_dst = self.fixture.install_dst

    def test_writing_references_resolve_after_complete_install_and_reapply(self) -> None:
        from guru_platform_inventory import PLATFORM_FLAGS, selected_skill_roots

        agents = self.repo / "AGENTS.md"
        user_instructions = b"# Project instructions\r\nPreserve these exact bytes.\r\n"
        agents.write_bytes(user_instructions)
        first = self.fixture.install(set(PLATFORM_FLAGS))
        self.assertEqual(first["skill_installed_validation"]["returncode"], 0)
        installed_spec = self.repo / ".trellis/spec/workflow/clear-technical-writing.md"
        canonical_spec = self.guru_root / "trellis/presets/guru-team/spec/workflow/clear-technical-writing.md"
        self.assertEqual(installed_spec.read_bytes(), canonical_spec.read_bytes())

        def resolve_writing_reference(text: str) -> None:
            references = re.findall(r"`(\.trellis/spec/workflow/clear-technical-writing\.md)`", text)
            self.assertTrue(references, "entry must locate the installed writing standard")
            for reference in references:
                self.assertEqual((self.repo / reference).resolve(), installed_spec.resolve())
                self.assertTrue((self.repo / reference).is_file())

        resolve_writing_reference(agents.read_text())
        resolve_writing_reference((self.repo / ".trellis/workflow.md").read_text())
        for relative in preset.GURU_OVERLAY_ENTRY_PATHS.values():
            with self.subTest(entry=relative):
                entry = self.repo / relative
                if entry.suffix == ".json":
                    text = json.loads(entry.read_text())["command"]
                elif entry.suffix == ".toml":
                    text = tomllib.loads(entry.read_text())["prompt"]
                else:
                    text = entry.read_text()
                    if text.startswith("---\n"):
                        self.assertIn("\n---\n", text[4:])
                        text = text.split("\n---\n", 1)[1]
                resolve_writing_reference(text)
        registry = json.loads((self.install_dst / "skills/registry.json").read_text())
        for root in selected_skill_roots(PLATFORM_FLAGS):
            for row in registry["skills"]:
                if row["state"] == "active":
                    with self.subTest(root=root, skill=row["id"]):
                        resolve_writing_reference((self.repo / root / row["id"] / "SKILL.md").read_text())
        before_agents = agents.read_bytes()
        repeated = self.fixture.install(set(PLATFORM_FLAGS))
        self.assertEqual(repeated["skill_installed_validation"]["returncode"], 0)
        self.assertTrue(agents.read_bytes().startswith(user_instructions))
        self.assertEqual(agents.read_bytes(), before_agents)
        self.assertEqual(installed_spec.read_bytes(), canonical_spec.read_bytes())
        self.assertEqual(
            [path for path in self.repo.rglob("*") if path.suffix in {".new", ".bak"}],
            [],
        )


if __name__ == "__main__":
    unittest.main()
