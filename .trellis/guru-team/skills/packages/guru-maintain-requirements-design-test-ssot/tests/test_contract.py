import json
import subprocess
import unittest
from pathlib import Path


class RequirementsDesignTestSSOTContractTest(unittest.TestCase):
    def setUp(self):
        self.package = Path(__file__).parents[1]

    def invoke(self, example: str, owner: dict) -> subprocess.CompletedProcess[str]:
        public_input = json.loads((self.package / "examples" / example).read_text())
        owner = {
            "profile": public_input["profile"],
            "mode": public_input["mode"],
            "continuation_id": public_input["continuation_id"],
            "ai_review_gate": {
                "status": "blocked" if owner["typed_exit"] == "blocked" else "passed",
                "reviewed_scope": "Current Requirements Design Test authority and selected profile.",
                "evidence_summary": "Live authority, contribution, traceability, and Architecture Baseline identity were reread.",
                "findings": [],
                "conclusion": "The selected typed exit is semantically justified.",
            },
            "consumer": {
                "ssot_current": {"kind": "workflow", "id": "guru-requirements-design-test-ssot-current-router"},
                "sync_required": {"kind": "skill", "id": "guru-maintain-requirements-design-test-ssot"},
                "revision_required": {"kind": "workflow", "id": "guru-requirements-design-test-ssot-planning-router"},
                "baseline_incomplete": {"kind": "workflow", "id": "guru-requirements-design-test-ssot-bootstrap-router"},
                "blocked": {"kind": "stop", "id": "requirements-design-test-ssot-blocked"},
            }[owner["typed_exit"]],
            **owner,
        }
        return subprocess.run(
            [str(self.package / "scripts/invoke.sh"), "--invocation", "-"],
            input=json.dumps({"public_input": public_input, "owner_result": owner}),
            text=True,
            capture_output=True,
            check=False,
        )

    def test_declares_four_profiles_five_exits_and_unique_consumers(self):
        interface = json.loads((self.package / "interface.json").read_text())
        profiles = {item["id"] for item in interface["public_contracts"]["input"]["profiles"]}
        self.assertEqual(profiles, {"bootstrap_foundation", "task_impact_sync", "promotion", "repair"})
        exits = interface["external_exits"]
        self.assertEqual({item["id"] for item in exits}, {"ssot_current", "sync_required", "revision_required", "baseline_incomplete", "blocked"})
        self.assertEqual(len({(item["consumer"]["kind"], item["consumer"]["id"]) for item in exits}), 5)

    def test_each_typed_exit_projects_only_its_minimal_contract(self):
        cases = [
            ("public-input-impact.json", {"typed_exit": "ssot_current", "authority_locator": "docs", "active_version": "1.0", "status": "active", "applicability_scope": "repository", "freshness": "authority-v1"}),
            ("public-input-promotion.json", {"typed_exit": "sync_required", "authority_locator": "docs", "target_version": "1.1", "contribution_locator": "docs/requirements-design-test-contributions/example", "sync_kind": "promotion", "freshness": "authority-v1"}),
            ("public-input-impact.json", {"typed_exit": "revision_required", "task_locator": ".trellis/tasks/example", "affected_scope": "traceability", "authority_locator": "docs", "authority_version": "1.0", "revision_code": "traceability_revision"}),
            ("public-input-bootstrap.json", {"typed_exit": "baseline_incomplete", "authority_locator": "docs", "known_status": "partial", "applicability_scope": "repository", "missing_layer_code": "test"}),
            ("public-input-repair.json", {"typed_exit": "blocked", "reason_code": "stale_identity", "remediation": "Reread the authority."}),
        ]
        for example, owner in cases:
            with self.subTest(exit=owner["typed_exit"]):
                result = self.invoke(example, owner)
                self.assertEqual(result.returncode, 0, result.stderr)
                output = json.loads(result.stdout)
                self.assertEqual(output["exit_id"], owner["typed_exit"])
                self.assertNotIn("profile", output)
                self.assertNotIn("continuation_id", output)

    def test_stale_owner_identity_fails_closed(self):
        public_input = json.loads((self.package / "examples/public-input-bootstrap.json").read_text())
        owner = {"profile": "bootstrap_foundation", "mode": "workflow", "continuation_id": "stale", "ai_review_gate": {"status": "blocked", "reviewed_scope": "authority", "evidence_summary": "live facts", "findings": ["stale"], "conclusion": "blocked"}, "typed_exit": "blocked", "consumer": {"kind": "stop", "id": "requirements-design-test-ssot-blocked"}, "reason_code": "stale_identity", "remediation": "Reread."}
        result = subprocess.run([str(self.package / "scripts/invoke.sh"), "--invocation", "-"], input=json.dumps({"public_input": public_input, "owner_result": owner}), text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["code"], "stale_identity")

    def test_gate_consumer_and_freshness_are_checked(self):
        public_input = json.loads((self.package / "examples/public-input-impact.json").read_text())
        owner = {
            "profile": "task_impact_sync",
            "mode": "workflow",
            "continuation_id": public_input["continuation_id"],
            "ai_review_gate": {"status": "passed", "reviewed_scope": "authority", "evidence_summary": "live facts", "findings": [], "conclusion": "current"},
            "typed_exit": "ssot_current",
            "consumer": {"kind": "workflow", "id": "guru-requirements-design-test-ssot-current-router"},
            "authority_locator": "docs",
            "active_version": "1.0",
            "status": "active",
            "applicability_scope": "repository",
            "freshness": "stale",
        }
        result = subprocess.run([str(self.package / "scripts/invoke.sh"), "--invocation", "-"], input=json.dumps({"public_input": public_input, "owner_result": owner}), text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["code"], "stale_identity")
        owner["freshness"] = public_input["authority_freshness"]
        owner["consumer"] = {"kind": "stop", "id": "requirements-design-test-ssot-blocked"}
        result = subprocess.run([str(self.package / "scripts/invoke.sh"), "--invocation", "-"], input=json.dumps({"public_input": public_input, "owner_result": owner}), text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["code"], "semantic_result_invalid")

    def test_parallel_contributions_are_task_owned_and_distinct(self):
        first = "docs/requirements-design-test-contributions/task-a"
        second = "docs/requirements-design-test-contributions/task-b"
        self.assertNotEqual(first, second)
        self.assertFalse(first.startswith("docs/requirements/versions/"))
        self.assertFalse(second.startswith("docs/design/versions/"))

    def test_contract_keeps_provenance_and_architecture_boundaries(self):
        contract = (self.package / "SKILL.md").read_text()
        for marker in ("code_recovered", "inferred", "unverified", "Architecture Baseline", "predecessor/successor"):
            self.assertIn(marker, contract)


if __name__ == "__main__":
    unittest.main()
