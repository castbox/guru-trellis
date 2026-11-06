"""Keep public example production and installed validation on one contract."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

import test_apply_guru_team_trellis_preset as installer_tests


# Reuse the existing interpreter fixture; installer, activation and package
# validators below execute their original implementations without mocks.
setUpModule = installer_tests.setUpModule
tearDownModule = installer_tests.tearDownModule


class PublicExampleInstallationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = installer_tests.PlatformOverlayInstallerTest()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)

    def assert_validation_passed(self, result):
        errors = result.get("errors", [])
        self.assertEqual(result["returncode"], 0, f"{len(errors)} errors: {errors[:3]}")
        self.assertEqual(result["status"], "passed")

    def test_real_install_and_reapply_activate_and_validate_public_examples(self):
        for stage in ("install", "reapply"):
            with self.subTest(stage=stage):
                result = self.fixture.install({"codex"})
                self.assert_validation_passed(result["skill_installed_validation"])
                self.assert_validation_passed(result["skill_activation_validation"])
                installed = installer_tests.preset.run_skill_package_validator(
                    self.fixture.repo, self.fixture.guru_root, "installed", Path(sys.executable)
                )
                self.assert_validation_passed(installed)
                package = Path("guru-select-workflow-mode")
                canonical = self.fixture.guru_root / "trellis/skills/guru-team/packages" / package
                for skill_root in (".agents/skills", ".codex/skills"):
                    projection = self.fixture.repo / skill_root / package
                    for name in ("public-input.json", "workflow-mode-selection.json", "public-invocation-error.json"):
                        relative = Path("examples") / name
                        self.assertEqual((projection / relative).read_bytes(), (canonical / relative).read_bytes())
                    self.assertFalse((projection / "runtime").exists())
                    check_projection = self.fixture.repo / skill_root / "guru-check-task"
                    check_source = self.fixture.guru_root / "trellis/skills/guru-team/packages/guru-check-task"
                    for name in ("phase2-authoring.json", "phase2-rejected-candidates.json"):
                        self.assertEqual(
                            (check_projection / "examples" / name).read_bytes(),
                            (check_source / "examples" / name).read_bytes(),
                        )
                    self.assertFalse((check_projection / "runtime").exists())
                    issue_example = Path(skill_root) / "guru-create-task/examples/public-create-issue-input.json"
                    read_issue = subprocess.run(["cat", str(issue_example)], cwd=self.fixture.repo, text=True, capture_output=True)
                    self.assertEqual(read_issue.returncode, 0, read_issue.stderr)
                    self.assertEqual(json.loads(read_issue.stdout)["creation"]["source_profile"], "existing_issue")
                shared_check_schema = Path(".trellis/guru-team/skills/packages/guru-check-task/schemas/phase2-check.schema.json")
                read_check_schema = subprocess.run(["cat", str(shared_check_schema)], cwd=self.fixture.repo, text=True, capture_output=True)
                self.assertEqual(read_check_schema.returncode, 0, read_check_schema.stderr)
                self.assertIn("semanticReview", json.loads(read_check_schema.stdout)["$defs"])
                sync = self.fixture.install_dst / "skills/packages/guru-sync-base"
                interface = json.loads((sync / "interface.json").read_text())
                envelope_ref = interface["public_contracts"]["invocation"]["call_local"]["envelope"]
                # The public Interface keeps its shared-root relative value.
                envelope_path = Path(".trellis/guru-team/skills") / envelope_ref["path"]
                located = subprocess.run(["cat", str(envelope_path)], cwd=self.fixture.repo, text=True, capture_output=True)
                self.assertEqual(located.returncode, 0, located.stderr)
                self.assertEqual(json.loads(located.stdout)["$id"], envelope_ref["schema_id"])
                installer_tests._ensure_managed_python_runtime(
                    self.fixture.repo, self.fixture.guru_root, activate=True,
                    python=sys.executable, checkout_local=True,
                )
                invoked = subprocess.run([
                    "bash", str(sync / "scripts/invoke.sh"), "--invocation", "-",
                ], cwd=self.fixture.repo, input=json.dumps({
                    "schema_version": "1.0",
                    "public_input": {"source_exit": "start", "mode": "workflow", "route": "original_request"},
                }), text=True, capture_output=True)
                self.assertEqual(invoked.returncode, 0, invoked.stdout + invoked.stderr)
                self.assertEqual(json.loads(invoked.stdout), {"exit_id": "skipped", "continuation_id": "start-original-request"})
                self.assertEqual([path for path in self.fixture.repo.rglob("*") if path.suffix in {".new", ".bak"}], [])


if __name__ == "__main__":
    unittest.main()
