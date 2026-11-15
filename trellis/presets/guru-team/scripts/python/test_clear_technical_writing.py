#!/usr/bin/env python3
"""Verify writing-standard distribution through the existing preset installer."""

from __future__ import annotations

import json
import re
import tomllib
import unittest
from pathlib import Path

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
        from guru_platform_inventory import PLATFORM_BY_FLAG, PLATFORM_FLAGS, selected_skill_roots

        agents = self.repo / "AGENTS.md"
        user_instructions = b"# Project instructions\r\nPreserve these exact bytes.\r\n"
        agents.write_bytes(user_instructions)
        first = self.fixture.install(set(PLATFORM_FLAGS))
        self.assertEqual(first["skill_installed_validation"]["returncode"], 0)
        installed_spec = self.repo / ".trellis/spec/workflow/clear-technical-writing.md"
        canonical_spec = self.guru_root / "trellis/presets/guru-team/spec/workflow/clear-technical-writing.md"
        self.assertEqual(installed_spec.read_bytes(), canonical_spec.read_bytes())
        workflow_spec_root = self.repo / ".trellis/spec/workflow"
        source_spec_root = self.guru_root / "trellis/presets/guru-team/spec/workflow"
        self.assertEqual(
            (workflow_spec_root / "companion-scripts.md").read_bytes(),
            (source_spec_root / "companion-scripts.md").read_bytes(),
        )

        def resolve_method_before_long_body(text: str, spec_root: Path) -> None:
            references = list(re.finditer(
                r"`([^`]*companion-scripts\.md)#(reading-required-contracts-in-full)`", text
            ))
            self.assertTrue(references, "entry must locate the short reading method")
            first_long_body = text.index("clear-technical-writing.md")
            self.assertLess(references[0].start(), first_long_body)
            for reference in references:
                path = reference.group(1)
                target = self.repo / path if "/" in path else spec_root / path
                self.assertEqual(target.resolve(), (spec_root / "companion-scripts.md").resolve())
                body = target.read_text()
                headings = re.findall(r"^## (.+)$", body, re.MULTILINE)
                matches = [heading for heading in headings
                           if heading.lower().replace(" ", "-") == reference.group(2)]
                self.assertEqual(matches, ["Reading Required Contracts In Full"])
                section = body.split("## " + matches[0] + "\n", 1)[1].split("\n## ", 1)[0]
                self.assertTrue(section.strip(), "navigation must resolve to an actual method body")

        def review_provider_references(text: str, spec_root: Path) -> None:
            resolve_method_before_long_body(text, spec_root)
            self.assertLess(text.index("Resolve the complete Guru source or installation"),
                            text.index("companion-scripts.md#"))
            self.assertLess(text.index("companion-scripts.md#"),
                            text.index("`review-sufficiency.md`"))
            for name in ("clear-technical-writing.md", "review-sufficiency.md"):
                self.assertTrue((spec_root / name).is_file())

        def resolve_writing_reference(text: str) -> None:
            references = re.findall(r"`(\.trellis/spec/workflow/clear-technical-writing\.md)`", text)
            if not references:
                # Provider-relative and installed short-name entries are valid
                # navigation forms; the actual installed body must still exist.
                self.assertIn("clear-technical-writing", text)
                self.assertTrue("`.trellis/spec/workflow`" in text
                                or "Read installed clear-technical-writing" in text)
                references = [".trellis/spec/workflow/clear-technical-writing.md"]
            for reference in references:
                self.assertEqual((self.repo / reference).resolve(), installed_spec.resolve())
                self.assertTrue((self.repo / reference).is_file())

        resolve_writing_reference(agents.read_text())
        resolve_method_before_long_body(agents.read_text(), workflow_spec_root)
        workflow = (self.repo / ".trellis/workflow.md").read_text()
        resolve_writing_reference(workflow)
        for start, end in (("## Phase Index", "## Phase 1: Plan"),
                           ("[trellis-continuation]", "[/trellis-continuation]"),
                           ("### Caller entry details", "### No-Task entry")):
            section = workflow.split(start, 1)[1].split(end, 1)[0]
            resolve_method_before_long_body(section, workflow_spec_root)
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
                resolve_method_before_long_body(text, workflow_spec_root)
        source_review = self.guru_root / "trellis/skills/guru-team/packages/guru-review-change/SKILL.md"
        review_provider_references(source_review.read_text(), source_spec_root)
        registry = json.loads((self.install_dst / "skills/registry.json").read_text())
        for root in selected_skill_roots(PLATFORM_FLAGS):
            for row in registry["skills"]:
                if row["state"] == "active":
                    with self.subTest(root=root, skill=row["id"]):
                        skill = self.repo / root / row["id"] / "SKILL.md"
                        root_platforms = {flag for flag in PLATFORM_FLAGS
                                          if root in PLATFORM_BY_FLAG[flag].skill_roots}
                        supported = set(row["supported_platforms"])
                        if "shared" not in supported and not root_platforms.intersection(supported):
                            self.assertFalse(skill.exists())
                            continue
                        self.assertTrue(skill.is_file())
                        if row["id"] == "guru-review-change":
                            self.assertEqual(skill.read_bytes(), source_review.read_bytes())
                            review_provider_references(skill.read_text(), workflow_spec_root)
                        else:
                            resolve_writing_reference(skill.read_text())
        before_agents = agents.read_bytes()
        repeated = self.fixture.install(set(PLATFORM_FLAGS))
        self.assertEqual(repeated["skill_installed_validation"]["returncode"], 0)
        self.assertTrue(agents.read_bytes().startswith(user_instructions))
        self.assertEqual(agents.read_bytes(), before_agents)
        self.assertEqual(installed_spec.read_bytes(), canonical_spec.read_bytes())
        resolve_method_before_long_body(agents.read_text(), workflow_spec_root)
        self.assertEqual(
            (workflow_spec_root / "companion-scripts.md").read_bytes(),
            (source_spec_root / "companion-scripts.md").read_bytes(),
        )
        self.assertEqual(
            [path for path in self.repo.rglob("*") if path.suffix in {".new", ".bak"}],
            [],
        )


if __name__ == "__main__":
    unittest.main()
