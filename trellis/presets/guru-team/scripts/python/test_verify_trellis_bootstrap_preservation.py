"""Exercise bootstrap post-checks; isolate external maintenance execution only."""
from __future__ import annotations

import base64
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import verify_trellis_compatibility_matrix as matrix


SOURCE = Path(__file__).resolve().parents[5]
PACKAGE = SOURCE / "trellis/skills/guru-team/packages/guru-upgrade-installation"
with mock.patch.object(sys, "path", [str(PACKAGE / "runtime"), str(PACKAGE.parents[1]), *sys.path]):
    import delivery_upgrade


class BootstrapPreservationTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.cell = Path(temporary.name)
        self.target = self.cell / "project"
        self.task_ref = ".trellis/tasks/00-bootstrap-guidelines"
        self.artifact = self.target / self.task_ref / "prd.md"
        self.original = "# Bootstrap guidelines\n保留原始内容。\n".encode()
        self.write(self.artifact, self.original)
        self.template_path = ".trellis/scripts/example.py"
        self.template_original = b"print('original template')\n"
        self.write(self.target / self.template_path, self.template_original, 0o755)
        self.retained_path = ".trellis/agents/example.md"
        self.retained_original = b"# Retained upstream agent\n"
        self.write(self.target / self.retained_path, self.retained_original)
        self.write(self.target / ".trellis/.version", b"0.7.0-castbox.6\n")
        self.write(self.target / ".trellis/.template-hashes.json", json.dumps({
            "hashes": {self.template_path: "previous-template", self.retained_path: "previous-agent"},
        }).encode())
        self.write(self.target / ".trellis/workflow.md", b"# Previous workflow\n")
        self.write(self.target / ".trellis/guru-team/extension.json", json.dumps({
            "extension": {"version": "0.7.0-guru.8"},
            "install": {"selected_platforms": ["codex"]},
        }).encode())
        self.source_ref = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True,
        ).strip()

    @staticmethod
    def write(path: Path, content: bytes, mode: int = 0o644) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        path.chmod(mode)

    def exercise(self, schema: str, change: str | None = None) -> dict:
        task = {"id": "00-bootstrap-guidelines", "schema_version": schema}
        if schema == "2.0":
            task.update(lifecycle_generation=0, deliveries=[])
        self.write(self.target / self.task_ref / "task.json", json.dumps(task).encode())
        # Use the existing producer, including its identity-only artifacts.
        inventory = delivery_upgrade.prepare_inventory(self.target, None)
        inventory["workspaces"][0]["prospective_templates"] = {
            "candidate_sha256": "fixture-template-candidate",
            "files": [{"path": self.template_path, "mode": 0o755}],
            "contents": {self.template_path: base64.b64encode(b"print('updated template')\n").decode()},
        }
        facts = {
            "inventory": inventory, "installed_core": "0.7.0-castbox.6",
            "source_candidate": {}, "fork_candidate": {},
        }
        result = {"exit_id": "tools_upgraded" if schema == "2.0" else "upgraded", "unverified": []}

        def maintain(*args: object, **kwargs: object) -> dict:
            # Model ordinary executor mistakes after the original inventory.
            if change == "bytes":
                self.artifact.write_bytes(b"ordinary unintended rewrite\n")
            elif change == "mode":
                self.artifact.chmod(0o600)
            elif change == "missing":
                self.artifact.unlink()
            return result

        real_run = matrix._run

        def owner_command(argv: tuple[str, ...], **kwargs: object) -> str:
            if argv[0] == "git":
                return real_run(argv, **kwargs)
            script = Path(argv[0]).name
            if script == "preview.sh":
                return json.dumps({"result": {} if "--plan" in argv else facts})
            self.assertEqual(script, "invoke.sh")
            return json.dumps(maintain())

        # Provider checks, branch selection, plan assembly, raw() and both
        # post-checks execute unchanged. These substitutes stop at the owners.
        with mock.patch.object(matrix, "_run", side_effect=owner_command), mock.patch.object(
            matrix, "_upgrade_native_bootstrap_tools", side_effect=maintain,
        ):
            return matrix._upgrade_bootstrap_fixture(
                SOURCE, self.target, self.cell / "fork",
                f"gh:castbox/guru-trellis/trellis#{self.source_ref}", self.cell, {},
            )

    def test_native_preserved_artifact_passes_original_post_check(self) -> None:
        self.assertEqual(self.exercise("2.0")["exit_id"], "tools_upgraded")
        self.assertEqual(self.artifact.read_bytes(), self.original)

    def test_legacy_preservation_keeps_actual_plan_source_content(self) -> None:
        self.assertEqual(self.exercise("1.0")["exit_id"], "upgraded")
        plan = json.loads((self.cell / "upgrade-plan.json").read_text())
        sources = {row["target"]["path"]: row["source"] for row in plan["core_plan"]["files"]}
        # Observe the plan written by the real assembler, using original bytes
        # as the independent expectation for both raw() content consumers.
        for path, expected in (
            (self.template_path, self.template_original),
            (self.retained_path, self.retained_original),
        ):
            with self.subTest(path=path):
                self.assertEqual(base64.b64decode(sources[path]["content_base64"]), expected)
        self.assertEqual(self.artifact.read_bytes(), self.original)

    def test_real_artifact_changes_still_fail_at_each_original_stage(self) -> None:
        for schema, suffix in (("2.0", "tools maintenance"), ("1.0", "upgrade")):
            for change in ("bytes", "mode", "missing"):
                with self.subTest(schema=schema, change=change):
                    self.write(self.artifact, self.original)
                    with self.assertRaises(matrix.MatrixError) as raised:
                        self.exercise(schema, change)
                    self.assertEqual(
                        str(raised.exception),
                        f"bootstrap fixture bytes or modes changed during {suffix}",
                    )


if __name__ == "__main__":
    unittest.main()
