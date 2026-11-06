#!/usr/bin/env python3
"""Exercise planning-body assets through the real preset projection writer.

This proves distribution and reapply behavior, not Agent writing or review.
"""

from __future__ import annotations

import unittest

import test_apply_guru_team_trellis_preset as installer_tests


setUpModule = installer_tests.setUpModule
tearDownModule = installer_tests.tearDownModule


class PlanningBodyDistributionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = installer_tests.PlatformOverlayInstallerTest()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)

    def test_body_assets_are_readable_in_every_projection_after_reapply(self) -> None:
        from guru_platform_inventory import PLATFORM_FLAGS, selected_skill_roots

        repo = self.fixture.repo
        package = "guru-author-task-plan"
        source = self.fixture.guru_root / "trellis/skills/guru-team/packages" / package
        required = [
            "references/planning-body.md",
            "templates/task-prd.md",
            "templates/delivery-prd.md",
            "templates/delivery-design.md",
            "templates/delivery-implement.md",
        ]
        assets = [source / name for name in required]
        for kind in ("detailed", "brief"):
            example = source / "examples/planning-body" / kind
            self.assertTrue(example.is_dir(), f"missing process example: {example}")
            assets.extend(path for path in example.rglob("*") if path.is_file())
        clarify = self.fixture.guru_root / "trellis/skills/guru-team/packages/guru-clarify-requirements"
        decision_assets = [clarify / name for name in (
            "SKILL.md", "references/contract.md", "examples/decision-exploration.md",
        )]

        user_file = repo / "docs/local-project-notes.md"
        user_file.parent.mkdir(parents=True, exist_ok=True)
        user_bytes = b"# Local project notes\r\nPreserve the project-owned file.\r\n"
        user_file.write_bytes(user_bytes)
        installed = self.fixture.install(set(PLATFORM_FLAGS))
        self.assertEqual(installed["skill_installed_validation"]["returncode"], 0,
                         installed["skill_installed_validation"])
        roots = [
            self.fixture.install_dst / "skills/packages" / package,
            *(repo / root / package for root in selected_skill_roots(PLATFORM_FLAGS)),
        ]

        def assert_readable_assets() -> None:
            for asset in assets:
                relative = asset.relative_to(source)
                expected = asset.read_bytes()
                self.assertTrue(expected, f"empty body asset: {relative}")
                for root in roots:
                    with self.subTest(projection=root, asset=relative):
                        self.assertEqual((root / relative).read_bytes(), expected)
            for asset in decision_assets:
                relative = asset.relative_to(clarify)
                destinations = [
                    self.fixture.install_dst / "skills/packages/guru-clarify-requirements",
                    *(repo / root / "guru-clarify-requirements" for root in selected_skill_roots(PLATFORM_FLAGS)),
                ]
                for destination in destinations:
                    with self.subTest(projection=destination, asset=relative):
                        self.assertEqual((destination / relative).read_bytes(), asset.read_bytes())

        assert_readable_assets()
        repeated = self.fixture.install(set(PLATFORM_FLAGS))
        self.assertEqual(repeated["skill_installed_validation"]["returncode"], 0,
                         repeated["skill_installed_validation"])
        assert_readable_assets()
        self.assertEqual(user_file.read_bytes(), user_bytes)
        self.assertEqual(
            [path for path in repo.rglob("*") if path.suffix in {".new", ".bak"}],
            [],
        )


if __name__ == "__main__":
    unittest.main()
