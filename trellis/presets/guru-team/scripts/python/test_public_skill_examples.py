from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import apply_guru_team_trellis_preset as preset


class PublicSkillExampleProjectionTests(unittest.TestCase):
    def test_instruction_examples_reach_platform_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mappings = preset.managed_source_projections(root, root / ".trellis/guru-team", {"codex"})
            examples = {
                "guru-check-task": ("phase2-authoring.json", "phase2-rejected-candidates.json"),
                "guru-create-task": ("public-create-issue-input.json",),
            }
            for skill_root in (".agents/skills", ".codex/skills"):
                for package, names in examples.items():
                    for name in names:
                        target = Path(skill_root) / package / "examples" / name
                        self.assertIn(target, mappings)
                        self.assertEqual(mappings[target].read_bytes(), (
                            preset.guru_root_from_script() / "trellis/skills/guru-team/packages" / package / "examples" / name
                        ).read_bytes())

    def test_mode_call_examples_reach_shared_and_codex_projections(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mappings = preset.managed_source_projections(root, root / ".trellis/guru-team", {"codex"})
            for skill_root in (".agents/skills", ".codex/skills"):
                for example in ("public-input.json", "workflow-mode-selection.json"):
                    with self.subTest(skill_root=skill_root, example=example):
                        target = Path(skill_root) / "guru-select-workflow-mode/examples" / example
                        self.assertTrue(target in mappings, str(target))
                        source = mappings[target]
                        preset.copy_managed(source, root / target)
                        self.assertEqual((root / target).read_bytes(), preset.canonical_bytes(source))

    def test_only_explicit_public_examples_override_artifact_exclusion(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory)
            examples = ("input", "owner", "output", "invocation_error", "checkpoint", "unused")
            interface = {
                "id": "example-skill",
                "artifacts": [{"id": name, "path": f"examples/{name}.json"} for name in examples],
                "public_contracts": {
                    "input": {"profiles": [{"example": {"path": "examples/input.json"}}]},
                    "invocation": {
                        "example_argv": ["--input", "examples/input.json", "--owner-result", "examples/owner.json"],
                        "error_example": {"path": "examples/invocation_error.json"},
                    },
                    "outputs": [{"example": {"path": "examples/output.json"}}],
                    "private_artifacts": [{"schema": {"path": "schemas/checkpoint.json"}}],
                },
            }
            (package / "interface.json").write_text(json.dumps(interface), encoding="utf-8")
            for relative in [*[f"examples/{name}.json" for name in examples], "runtime/invoke.py", "schemas/checkpoint.json"]:
                path = package / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}", encoding="utf-8")
            projected = {path.relative_to(package).as_posix() for path in preset.skill_platform_public_files(package)}
            self.assertEqual(projected, {"interface.json", "examples/input.json", "examples/owner.json", "examples/output.json", "examples/invocation_error.json"})


if __name__ == "__main__":
    unittest.main()
