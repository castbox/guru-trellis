"""Candidate entry projections through the existing preset inventory owner.

This checks the managed mapping and copy primitives. Actual matching installation
and native Agent behavior require their separate original validation owners.
"""
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

import apply_guru_team_trellis_preset as preset


class CandidateProjectionTests(unittest.TestCase):
    def test_candidate_entry_and_nested_runtime_share_original_managed_projection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / ".trellis/guru-team"
            mappings = preset.managed_source_projections(root, destination, {"codex"})
            expected = {
                Path(".trellis/guru-team/scripts/bash/construct-delivery-candidate.sh"):
                    "trellis/workflows/guru-team/scripts/bash/construct-delivery-candidate.sh",
                Path(".trellis/guru-team/runtime/delivery_projection/candidate_cli.py"):
                    "trellis/skills/guru-team/runtime/delivery_projection/candidate_cli.py",
                Path(".trellis/guru-team/skills/packages/guru-author-task-plan/references/authoring.md"):
                    "trellis/skills/guru-team/packages/guru-author-task-plan/references/authoring.md",
            }
            for target, source_relative in expected.items():
                with self.subTest(target=target):
                    source = preset.guru_root_from_script() / source_relative
                    self.assertEqual(mappings[target], source)
                    installed = root / target
                    self.assertEqual(preset.copy_managed(source, installed)["action"], "installed")
                    self.assertEqual(installed.read_bytes(), preset.canonical_bytes(source))
                    self.assertEqual(preset.copy_managed(source, installed)["action"], "unchanged")
            wrapper = destination / "scripts/bash/construct-delivery-candidate.sh"
            preset.ensure_executable(wrapper)
            self.assertTrue(os.access(wrapper, os.X_OK))


if __name__ == "__main__":
    unittest.main()
