"""Exercise routing references through the existing matrix consumers."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import verify_trellis_compatibility_matrix as matrix


REFERENCE = '<!-- guru-routing-reference: {"path":"references/routing.md"} -->\n'


def graph(skill: str) -> str:
    return '<!-- guru-skill-invoke: ' + json.dumps({"skill": skill, "required": True}) + ' -->\n'


class StepContextRoutingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="guru-step-routing-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def reference(self, extension: Path, skill: str) -> Path:
        path = extension / "references/routing.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(graph(skill), encoding="utf-8")
        return path

    def test_source_and_installed_snapshots_read_their_explicit_reference(self):
        source = self.root / "source/trellis/workflows/guru-team"
        installed = self.root / "project/.trellis/guru-team"
        self.reference(source, "guru-sync-base")
        self.reference(installed, "guru-author-task-plan")
        for workflow, extension, skill in (
            (source / "workflow.md", source, "guru-sync-base"),
            (installed.parent / "workflow.md", installed, "guru-author-task-plan"),
        ):
            with self.subTest(workflow=workflow):
                workflow.write_text(REFERENCE, encoding="utf-8")
                result = matrix._workflow_markers(workflow, extension)
                self.assertEqual([{"skill": skill, "required": True}],
                                 [json.loads(value) for value in result["skill_invokes"]])

    def test_inline_is_only_an_explicit_before_observation(self):
        workflow = self.root / "before.md"
        workflow.write_text(graph("guru-sync-base"), encoding="utf-8")
        with self.assertRaises(matrix.MatrixError):
            matrix._workflow_markers(workflow, self.root)
        result = matrix._workflow_markers(workflow, self.root, before_observation=True)
        self.assertEqual("guru-sync-base", json.loads(result["skill_invokes"][0])["skill"])

    def test_missing_new_reference_never_falls_back_to_inline(self):
        workflow = self.root / "workflow.md"
        workflow.write_text(REFERENCE + graph("guru-sync-base"), encoding="utf-8")
        with self.assertRaises(matrix.MatrixError):
            matrix._workflow_markers(workflow, self.root, before_observation=True)

    def test_local_preview_reads_candidate_assets_before_they_are_installed(self):
        target = self.root / "target"
        source = self.root / "source"
        extension = source / "trellis/workflows/guru-team"
        self.reference(extension, "guru-sync-base")
        (extension / "workflow.md").write_text(REFERENCE, encoding="utf-8")
        # An old installed reference must not be used for the new preview.
        self.reference(target / ".trellis/guru-team", "guru-author-task-plan")
        workflow = target / ".trellis/workflow.md"
        workflow.write_text("before\n", encoding="utf-8")
        expected = self.root / "before.md"
        expected.write_text("before\n", encoding="utf-8")
        matrix._preview_and_switch_workflow(
            target, (), {}, "local", source, expected, True, self.root,
        )
        self.assertEqual(REFERENCE, workflow.read_text(encoding="utf-8"))
        self.assertFalse(Path(str(workflow) + ".new").exists())

    def test_missing_candidate_reference_stops_before_switch(self):
        target = self.root / "target"
        source = self.root / "source"
        extension = source / "trellis/workflows/guru-team"
        extension.mkdir(parents=True)
        (extension / "workflow.md").write_text(REFERENCE, encoding="utf-8")
        self.reference(target / ".trellis/guru-team", "guru-sync-base")
        workflow = target / ".trellis/workflow.md"
        workflow.write_text("before\n", encoding="utf-8")
        expected = self.root / "before.md"
        expected.write_text("before\n", encoding="utf-8")
        with self.assertRaises(matrix.MatrixError):
            matrix._preview_and_switch_workflow(
                target, (), {}, "local", source, expected, True, self.root,
            )
        self.assertEqual("before\n", workflow.read_text(encoding="utf-8"))
        self.assertTrue(Path(str(workflow) + ".new").exists())


if __name__ == "__main__":
    unittest.main()
