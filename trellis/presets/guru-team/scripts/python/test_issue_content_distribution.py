#!/usr/bin/env python3
"""Exercise the common Issue body through the real preset projection writer.

This checks installed bytes and readable links, not Agent writing quality.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import test_apply_guru_team_trellis_preset as installer_tests


setUpModule = installer_tests.setUpModule
tearDownModule = installer_tests.tearDownModule


class IssueContentDistributionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = installer_tests.PlatformOverlayInstallerTest()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)

    def test_shared_body_and_entry_links_survive_install_and_reapply(self) -> None:
        from guru_platform_inventory import PLATFORM_FLAGS, selected_skill_roots

        repo = self.fixture.repo
        source = self.fixture.guru_root / "trellis/skills/guru-team/packages"
        clarify = "guru-clarify-requirements"
        body = Path(clarify) / "references/issue-content.md"
        assets = [body]
        for kind in ("brief", "detailed", "revision"):
            assets.append(Path(clarify) / "examples/issue-content" / kind / "process.md")
        owners = (
            clarify,
            "guru-review-contract-wording",
            "guru-review-change-request",
            "guru-create-issue",
        )
        for owner in owners:
            assets.append(Path(owner) / "SKILL.md")
            contract = Path(owner) / "references/contract.md"
            if (source / contract).exists():
                assets.append(contract)

        # Both the full runtime tree and every declared discovery tree must
        # resolve the same cross-package reference after real installation.
        roots = [
            self.fixture.install_dst / "skills/packages",
            *(repo / root for root in selected_skill_roots(PLATFORM_FLAGS)),
        ]
        user_file = repo / "docs/local-project-notes.md"
        user_file.parent.mkdir(parents=True, exist_ok=True)
        user_bytes = b"# Project notes\r\nKeep the user's existing content.\r\n"
        user_file.write_bytes(user_bytes)

        def assert_readable_assets() -> None:
            for root in roots:
                for relative in assets:
                    with self.subTest(projection=root, asset=relative):
                        expected = (source / relative).read_bytes()
                        self.assertTrue(expected, f"empty content asset: {relative}")
                        self.assertEqual((root / relative).read_bytes(), expected)

                readers = [root / relative for relative in assets]
                for reader in readers:
                    links = re.findall(r"\]\(([^)]+)\)", reader.read_text(encoding="utf-8"))
                    content_links = [
                        link for link in links
                        if link.split("#", 1)[0].endswith("issue-content.md")
                    ]
                    if reader != root / body:
                        self.assertTrue(content_links, f"missing content locator: {reader}")
                    for link in content_links:
                        resolved = (reader.parent / link.split("#", 1)[0]).resolve()
                        self.assertEqual(resolved, (root / body).resolve())
                        self.assertEqual(resolved.read_bytes(), (source / body).read_bytes())

                # The common body's source-preservation dependency must also
                # resolve in each real projection, without another rule copy.
                reader = root / body
                links = re.findall(r"\]\(([^)]+)\)", reader.read_text(encoding="utf-8"))
                planning_links = [
                    link for link in links
                    if link.split("#", 1)[0].endswith("planning-body.md")
                ]
                self.assertTrue(planning_links)
                for link in planning_links:
                    target = (reader.parent / link.split("#", 1)[0]).resolve()
                    expected = Path("guru-author-task-plan/references/planning-body.md")
                    self.assertEqual(target, (root / expected).resolve())
                    self.assertEqual(target.read_bytes(), (source / expected).read_bytes())

            writing = Path("spec/workflow/clear-technical-writing.md")
            self.assertEqual(
                (repo / ".trellis" / writing).read_bytes(),
                (self.fixture.guru_root / "trellis/presets/guru-team" / writing).read_bytes(),
            )

        installed = self.fixture.install(set(PLATFORM_FLAGS))
        self.assertEqual(installed["skill_installed_validation"]["returncode"], 0)
        assert_readable_assets()
        repeated = self.fixture.install(set(PLATFORM_FLAGS))
        self.assertEqual(repeated["skill_installed_validation"]["returncode"], 0)
        assert_readable_assets()
        self.assertEqual(user_file.read_bytes(), user_bytes)
        self.assertEqual(
            [path for path in repo.rglob("*") if path.suffix in {".new", ".bak"}],
            [],
        )


if __name__ == "__main__":
    unittest.main()
