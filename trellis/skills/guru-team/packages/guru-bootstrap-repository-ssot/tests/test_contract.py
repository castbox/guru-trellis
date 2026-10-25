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

    def invoke(self, public, owner):
        return subprocess.run([str(self.package / "scripts/invoke.sh"), "--invocation", "-"],
                              input=json.dumps({"public_input": public, "owner_result": owner}),
                              text=True, capture_output=True)

    def test_repair_stdout_projects_to_original_caller_context_and_real_consumer(self):
        import copy
        interface = json.loads((self.package / "interface.json").read_text())["public_contracts"]
        projection = next(row for row in interface["projections"] if row["exit_id"] == "repair_required")
        target = next(row["contract"] for row in interface["consumer_inputs"]
                      if row["id"] == projection["consumer_input_id"])
        for profile, mode in (("new_repository", "workflow"), ("existing_repository", "standalone")):
            original = {"profile": profile, "source_exit": "start", "mode": mode,
                        "continuation_id": "same-bootstrap", "repo_locator": ".",
                        "baseline": {"identity": "original"}, "scope": {"locator": "requirements.md"}}
            if profile == "existing_repository":
                original["contribution"] = {"locator": "docs/contribution.md"}
            producer = self.invoke(original, {"profile": profile, "continuation_id": original["continuation_id"],
                                              "typed_exit": "repair_required"})
            self.assertEqual(producer.returncode, 0, producer.stdout + producer.stderr)
            output = json.loads(producer.stdout)
            seed = {row["target"]: output[row["source"]] for row in projection["mappings"]}
            self.assertEqual(set(seed), set(target["seed_fields"]))
            repair = {**seed, "profile": "repair", **{key: copy.deepcopy(value) for key, value in original.items()
                                                        if key not in {"profile", "source_exit"}}}
            owner = {"profile": "repair", "continuation_id": original["continuation_id"], "typed_exit": "completed"}
            consumer = self.invoke(repair, owner)
            self.assertEqual(consumer.returncode, 0, consumer.stdout + consumer.stderr)
            self.assertEqual(json.loads(consumer.stdout), {"exit_id": "completed"})
            for missing in ("mode", "continuation_id"):
                bad = copy.deepcopy(repair); bad.pop(missing)
                self.assertNotEqual(self.invoke(bad, owner).returncode, 0)
            for field in ("source_exit", "continuation_id", "repo_locator"):
                blank = {**repair, field: ""}
                matching = {**owner, "continuation_id": blank["continuation_id"]}
                rejected = self.invoke(blank, matching)
                self.assertEqual(rejected.returncode, 2, rejected.stdout)
                self.assertEqual(json.loads(rejected.stdout)["code"], "schema_mismatch")
            for retired in ("authority", "projection"):
                rejected = self.invoke({**repair, retired: {}}, owner)
                self.assertEqual(rejected.returncode, 2, rejected.stdout)
            for field in ("profile", "continuation_id"):
                stale = {**owner, field: "different"}
                result = self.invoke(repair, stale)
                self.assertEqual(result.returncode, 3, result.stdout)
                self.assertEqual(json.loads(result.stdout)["code"], "stale_identity")

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
