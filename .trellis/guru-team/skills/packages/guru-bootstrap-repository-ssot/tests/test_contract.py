import json
import subprocess
import unittest
from pathlib import Path


class BootstrapRepositorySSOTContractTest(unittest.TestCase):
    def setUp(self):
        self.package = Path(__file__).parents[1]

    def test_declares_four_profiles_and_exits(self):
        interface = json.loads((self.package / "interface.json").read_text())
        profiles = {item["id"] for item in interface["public_contracts"]["input"]["profiles"]}
        self.assertEqual(profiles, {"new_repository", "existing_repository", "repair"})
        self.assertEqual({item["id"] for item in interface["external_exits"]}, {"completed", "baseline_incomplete", "repair_required", "blocked"})

    def test_public_invocation_projects_owner_exit(self):
        envelope = {"public_input": {"profile": "new_repository", "source_exit": "start", "mode": "workflow", "continuation_id": "test"}, "owner_result": {"profile": "new_repository", "continuation_id": "test", "typed_exit": "baseline_incomplete"}}
        result = subprocess.run([str(self.package / "scripts/invoke.sh"), "--invocation", "-"], input=json.dumps(envelope), text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["exit_id"], "baseline_incomplete")

    def test_eval_owner_staging_is_bootstrap_owned(self):
        corpus = json.loads((self.package / "evals/evals.json").read_text())
        recipes = set()
        profiles = set()
        for case in corpus["evals"]:
            profiles.add(case["input_profile_id"])
            for relative in case["files"]:
                payload = json.loads((self.package / relative).read_text())
                staging = payload.get("owner_staging")
                if staging:
                    recipes.add(staging["recipe"])
        self.assertEqual(profiles, {"new_repository", "existing_repository", "repair"})
        self.assertEqual(
            recipes,
            {
                "bootstrap-baseline-incomplete",
                "bootstrap-completed",
                "bootstrap-repair-required",
                "bootstrap-blocked",
            },
        )


if __name__ == "__main__":
    unittest.main()
