from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / "trellis/skills/guru-team"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


preset = load_module(
    "guru_team_preset_integration",
    REPO / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py",
)


class SkillPackageIntegrationTests(unittest.TestCase):
    def run_json(self, *arguments: str, cwd: Path = REPO) -> dict:
        process = subprocess.run(
            list(arguments), cwd=cwd, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        payload = json.loads(process.stdout)
        self.assertIsInstance(payload, dict)
        return payload

    def test_source_command_graph_is_closed(self) -> None:
        payload = self.run_json(
            str(REPO / "trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh"),
            "--root", str(REPO), "--mode", "source", "--json",
        )
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["active_packages"], 15)
        self.assertEqual(payload["complete_package_commands"], 15)
        self.assertGreater(payload["commands"], 0)

    def test_contract_and_eval_discovery_use_shared_runtime(self) -> None:
        contract = self.run_json(
            str(REPO / "trellis/workflows/guru-team/scripts/bash/discover-skill-contract.sh"),
            "--root", str(REPO), "--mode", "source",
            "--skill", "guru-sync-base", "--json",
        )
        self.assertEqual(contract["skill_id"], "guru-sync-base")
        evaluations = self.run_json(
            str(REPO / "trellis/workflows/guru-team/scripts/bash/discover-skill-evals.sh"),
            "--root", str(REPO), "--mode", "source",
            "--skill", "guru-sync-base", "--json",
        )
        self.assertEqual(evaluations["skill_id"], "guru-sync-base")
        self.assertTrue(evaluations["case_ids"])

    def test_public_wrapper_reaches_package_owner(self) -> None:
        wrapper = SKILLS / "packages/guru-select-workflow-mode/scripts/invoke.sh"
        process = subprocess.run(
            [str(wrapper), "--help"], cwd=REPO, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertNotIn("guru_team_trellis.py", wrapper.read_text(encoding="utf-8"))

    def test_installed_tree_and_platform_projections_are_private_runtime_free(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repo"
            (target / ".trellis").mkdir(parents=True)
            (target / ".trellis/workflow.md").write_bytes(
                (REPO / "trellis/workflows/guru-team/workflow.md").read_bytes()
            )
            preset.install_assets(
                REPO / "trellis/workflows/guru-team",
                target / ".trellis/guru-team",
                target,
                {"codex", "cursor", "claude"},
            )
            installed = self.run_json(
                str(target / ".trellis/guru-team/scripts/bash/check-skill-packages.sh"),
                "--root", str(target), "--mode", "installed", "--json",
                cwd=target,
            )
            self.assertEqual(installed["status"], "passed")
            self.assertEqual(len(installed["facts"]["active_ids"]), 15)
            self.assertFalse((target / ".trellis/guru-team/scripts/python/guru_team_trellis.py").exists())
            for projection in (target / ".agents/skills", target / ".codex/skills", target / ".cursor/skills"):
                for path in projection.rglob("*"):
                    self.assertNotIn(path.name, {"runtime", "tests", "errors"})

    def test_active_runtime_has_no_monolith_dependency(self) -> None:
        active_roots = (
            REPO / "trellis/skills/guru-team/runtime",
            REPO / "trellis/skills/guru-team/packages",
            REPO / "trellis/workflows/guru-team/scripts/bash",
        )
        offenders = []
        for root in active_roots:
            for path in root.rglob("*"):
                if path.is_file() and path.suffix in {".py", ".sh"}:
                    text = path.read_text(encoding="utf-8", errors="replace")
                    if (
                        "guru_team_trellis.py" in text
                        and path.name != "validate.py"
                        and "/tests/" not in path.as_posix()
                    ):
                        offenders.append(path.relative_to(REPO).as_posix())
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
