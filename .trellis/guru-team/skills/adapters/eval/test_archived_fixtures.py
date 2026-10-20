"""Historical archived transport runs against its pinned source, not #434."""
from __future__ import annotations

import io
import os
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILLS))

from adapters.eval import archived_fixtures as archived


class ArchivedSourceVersionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repository = next(parent for parent in SKILLS.parents if (parent / ".git").exists())

    def test_current_graph_rejects_archived_recipes(self):
        packages = SKILLS / "packages"
        registry = archived.read(SKILLS / "registry.json")
        active = {row["id"] for row in registry["skills"] if row["state"] == "active"}
        for name in archived.RETIRED_PACKAGES:
            self.assertNotIn(name, active)
            self.assertFalse((packages / name / "interface.json").exists())
        with tempfile.TemporaryDirectory(prefix="guru-current-archive-reject-") as temp:
            fixture = Path(temp)
            with self.assertRaisesRegex(ValueError, "requires the pinned-old package graph"):
                archived.stage_archived_owner_execution(
                    {"skill_id": archived.MERGE}, fixture, fixture / "target",
                    packages / archived.MERGE, "merge-archived-review", fixture / "missing-input.json",
                )

    def test_archived_transport_executes_at_pinned_old_source_version(self):
        with tempfile.TemporaryDirectory(prefix="guru-pinned-old-archive-") as temp:
            snapshot = Path(temp)
            result = subprocess.run(
                ["git", "archive", "--format=tar", archived.PINNED_OLD_SOURCE_SHA,
                 ".trellis/scripts", ".trellis/guru-team/scripts", ".trellis/guru-team/schemas",
                 ".trellis/workflow.md", "trellis/skills/guru-team"],
                cwd=self.repository, capture_output=True, check=True,
            )
            with tarfile.open(fileobj=io.BytesIO(result.stdout)) as archive:
                archive.extractall(snapshot, filter="data")
            old_skills = snapshot / "trellis/skills/guru-team"
            for name in archived.RETIRED_PACKAGES:
                self.assertTrue((old_skills / "packages" / name / "interface.json").is_file())
            completed = subprocess.run(
                [sys.executable, "-B", "-m", "unittest", "adapters.eval.test_archived_fixtures", "-v"],
                cwd=old_skills, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                text=True, capture_output=True, timeout=240,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertIn("Ran 3 tests", completed.stderr)
            self.assertIn("OK", completed.stderr)
            self.assertNotIn("skipped", completed.stderr)


if __name__ == "__main__":
    unittest.main()
