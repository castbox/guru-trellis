import json
import subprocess
import unittest
from pathlib import Path


class ArchitectureBaselineContractTest(unittest.TestCase):
    def setUp(self):
        self.package = Path(__file__).parents[1]

    def test_declares_four_profiles_and_exits(self):
        interface = json.loads((self.package / "interface.json").read_text())
        profiles = {item["id"] for item in interface["public_contracts"]["input"]["profiles"]}
        self.assertEqual(profiles, {"bootstrap_foundation", "task_impact_sync", "promotion", "repair"})
        self.assertEqual({item["id"] for item in interface["external_exits"]}, {"baseline_current", "sync_required", "baseline_incomplete", "architecture_conflict", "contract_incomplete", "fitness_regression", "blocked"})

    def test_public_invocation_projects_owner_exit(self):
        envelope = {"public_input": {"profile": "bootstrap_foundation", "source_exit": "start", "mode": "workflow", "continuation_id": "test"}, "owner_result": {"profile": "bootstrap_foundation", "continuation_id": "test", "typed_exit": "baseline_incomplete"}}
        result = subprocess.run([str(self.package / "scripts/invoke.sh"), "--invocation", "-"], input=json.dumps(envelope), text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["exit_id"], "baseline_incomplete")


if __name__ == "__main__":
    unittest.main()
