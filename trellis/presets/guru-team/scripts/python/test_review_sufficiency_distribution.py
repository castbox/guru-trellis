#!/usr/bin/env python3
"""Check readable provider rules through the real preset install/reapply writer.

These tests prove distribution and dependency direction, not Agent behavior.
"""

from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

import test_apply_guru_team_trellis_preset as installer_tests

setUpModule = installer_tests.setUpModule
tearDownModule = installer_tests.tearDownModule


class ReviewSufficiencyDistributionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = installer_tests.PlatformOverlayInstallerTest()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)

    def test_provider_rules_and_consumers_survive_install_reapply_and_local_edit(self) -> None:
        from guru_platform_inventory import selected_skill_roots

        fixture = self.fixture
        repo = fixture.repo
        platforms = {"claude", "codex", "cursor"}
        source_packages = fixture.guru_root / "trellis/skills/guru-team/packages"
        consumers = (
            "guru-clarify-requirements", "guru-review-change-request",
            "guru-review-contract-wording", "guru-approve-task-plan",
            "guru-review-change", "guru-check-task", "guru-review-branch",
            "guru-review-task-delivery", "guru-review-task-completion",
            "guru-maintain-architecture-baseline",
            "guru-maintain-requirements-design-test-ssot",
            "guru-verify-extension-installation",
        )
        spec_relative = Path(".trellis/spec/workflow/review-sufficiency.md")
        source_spec = fixture.guru_root / "trellis/presets/guru-team/spec/workflow/review-sufficiency.md"
        canonical = source_spec.read_bytes()
        target_spec = repo / spec_relative
        user_file = repo / "docs/project-notes.md"
        user_file.parent.mkdir(parents=True)
        user_bytes = b"# Existing project notes\r\nKeep these bytes.\r\n"
        user_file.write_bytes(user_bytes)

        def check_readable_provider() -> None:
            self.assertEqual(target_spec.read_bytes(), canonical)
            manifest = json.loads((fixture.install_dst / "extension.json").read_text())
            self.assertEqual(
                manifest["install"]["managed_asset_hashes"][spec_relative.as_posix()],
                hashlib.sha256(canonical).hexdigest(),
            )
            roots = [
                fixture.install_dst / "skills/packages",
                *(repo / root for root in selected_skill_roots(platforms)),
            ]
            for root in roots:
                for consumer in consumers:
                    entry = root / consumer / "SKILL.md"
                    with self.subTest(projection=root, consumer=consumer):
                        # Compare canonical and installed bytes; this does not
                        # prove that an Agent loads the semantic rules.
                        self.assertEqual(entry.read_bytes(), (source_packages / consumer / "SKILL.md").read_bytes())
                method_relative = Path("guru-review-change/references/review-method.md")
                method = root / method_relative
                self.assertEqual(method.read_bytes(), (source_packages / method_relative).read_bytes())
                links = re.findall(r"\]\(([^)]+)\)", method.read_text())
                for link in links:
                    linked = (method.parent / link.split("#", 1)[0]).resolve()
                    self.assertTrue(linked.is_file(), link)
                    self.assertNotIn("guru-check-task", linked.parts)
                    self.assertNotIn("guru-review-branch", linked.parts)
                for link in re.findall(r"\]\(([^)]+)\)", target_spec.read_text()):
                    linked = target_spec.parent / link.split("#", 1)[0]
                    self.assertTrue(linked.is_file(), link)
                    expected = source_spec.parent / link.split("#", 1)[0]
                    self.assertEqual(linked.read_bytes(), expected.read_bytes())

        first = fixture.install(platforms)
        self.assertEqual(first["skill_installed_validation"]["returncode"], 0)
        check_readable_provider()
        second = fixture.install(platforms)
        self.assertEqual(second["skill_installed_validation"]["returncode"], 0)
        check_readable_provider()
        self.assertEqual(user_file.read_bytes(), user_bytes)
        self.assertEqual([p for p in repo.rglob("*") if p.suffix in {".new", ".bak"}], [])

        manifest_path = fixture.install_dst / "extension.json"
        previous_manifest = manifest_path.read_bytes()
        local = canonical + b"\n# Local review guidance\n"
        target_spec.write_bytes(local)
        conflict = fixture.install(platforms)
        self.assertEqual(conflict["skill_packages"]["status"], "conflict")
        self.assertEqual(target_spec.read_bytes(), local)
        self.assertEqual(target_spec.with_name(target_spec.name + ".new").read_bytes(), canonical)
        self.assertEqual(manifest_path.read_bytes(), previous_manifest)
        self.assertIn(
            {"path": spec_relative.as_posix(), "reason": "unknown_local_spec_edit", "sidecar": spec_relative.as_posix() + ".new"},
            conflict["skill_packages"]["conflicts"],
        )


if __name__ == "__main__":
    unittest.main()
