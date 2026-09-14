"""Check documented package locations, not semantic or lifecycle success."""

from __future__ import annotations

import os
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[4]
PACKAGES = ROOT / "trellis/skills/guru-team/packages"
ENTRIES = {
    "guru-discover-change-context": (
        "record-context-discovery.sh", "check-context-discovery.sh", "invoke.sh",
    ),
    "guru-clarify-requirements": (
        "record-requirements-clarification.sh", "check-requirements-clarification.sh", "invoke.sh",
    ),
    "guru-review-contract-wording": (
        "record-contract-wording-review.sh", "check-contract-wording-review.sh", "invoke.sh",
    ),
    "guru-review-change-request": (
        "record-change-request-review.sh", "check-change-request-review.sh", "invoke.sh",
    ),
    "guru-create-task-workspace": (
        "record-task-workspace-plan.sh", "create-task-workspace.sh",
        "check-task-workspace-result.sh", "invoke.sh",
    ),
}


class InstalledEntryLocationTests(unittest.TestCase):
    def check_contract(self, discovery: Path, package: Path, skill: str) -> None:
        text = "\n".join((discovery / name).read_text(encoding="utf-8")
                         for name in ("SKILL.md", "references/contract.md"))
        expected_root = f".trellis/guru-team/skills/packages/{skill}"
        self.assertIn(expected_root, text)
        self.assertIn("repository root", text)
        for name in ENTRIES[skill]:
            with self.subTest(skill=skill, script=name, discovery=discovery):
                self.assertIn(name, text)
                self.assertTrue((package / "scripts" / name).is_file())
                self.assertTrue(os.access(package / "scripts" / name, os.X_OK))
        for relative in set(re.findall(r"(?:schemas|examples)/[A-Za-z0-9_.-]+\.json", text)):
            with self.subTest(skill=skill, asset=relative, discovery=discovery):
                self.assertTrue((package / relative).is_file(), relative)

    def test_canonical_contracts_resolve_to_real_package_assets(self) -> None:
        for skill in ENTRIES:
            self.check_contract(PACKAGES / skill, PACKAGES / skill, skill)

    @unittest.skipUnless(os.environ.get("GURU_ENTRY_INSTALLED_REPO"),
                         "Explicit installed target required for projection checks")
    def test_actual_agent_projections_use_full_installed_package(self) -> None:
        installed = Path(os.environ["GURU_ENTRY_INSTALLED_REPO"])
        checked = 0
        for platform in (".agents", ".codex", ".claude", ".cursor"):
            for skill in ENTRIES:
                discovery = installed / platform / "skills" / skill
                if not discovery.is_dir():
                    continue
                package = installed / ".trellis/guru-team/skills/packages" / skill
                self.check_contract(discovery, package, skill)
                checked += 1
        self.assertGreaterEqual(checked, len(ENTRIES))


if __name__ == "__main__":
    unittest.main()
