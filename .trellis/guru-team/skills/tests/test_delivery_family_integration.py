from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[1]
REPO = SKILLS.parents[2]
PACKAGE_IDS = (
    "guru-review-task-delivery",
    "guru-publish-task-delivery",
    "guru-merge-task-delivery",
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class DeliveryFamilyIntegrationTest(unittest.TestCase):
    def package(self, skill_id: str) -> Path:
        return SKILLS / "packages" / skill_id

    def interface(self, skill_id: str) -> dict:
        return read_json(self.package(skill_id) / "interface.json")

    def profile_schema(self, skill_id: str, profile_id: str) -> dict:
        interface = self.interface(skill_id)
        profile = next(
            item for item in interface["public_contracts"]["input"]["profiles"]
            if item["id"] == profile_id
        )
        return read_json(self.package(skill_id) / profile["schema"]["path"])

    def assert_schema_shape(self, payload: dict, schema: dict) -> None:
        self.assertEqual(set(payload), set(schema["required"]))
        self.assertFalse(set(payload) - set(schema["properties"]))
        for field, rules in schema["properties"].items():
            if "const" in rules:
                self.assertEqual(payload[field], rules["const"])
            if "pattern" in rules:
                self.assertRegex(str(payload[field]), re.compile(rules["pattern"]))

    def project_seed(self, producer_id: str, projection_id: str) -> tuple[dict, dict]:
        package = self.package(producer_id)
        interface = self.interface(producer_id)
        projection = next(
            item for item in interface["public_contracts"]["projections"]
            if item["id"] == projection_id
        )
        consumer_input = next(
            item for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == projection["consumer_input_id"]
        )
        output = next(
            item for item in interface["public_contracts"]["outputs"]
            if item["exit_id"] == projection["exit_id"]
        )
        payload = read_json(package / output["example"]["path"])
        seed = {
            mapping["target"]: payload[mapping["source"]]
            for mapping in projection.get("mappings", [])
        }
        contract = consumer_input["contract"]
        authoring = read_json(package / contract["authoring_example"]["path"])
        return {**seed, **authoring}, contract

    def test_packages_are_active_deferred_without_production_markers(self) -> None:
        registry = read_json(SKILLS / "registry.json")
        entries = {item["id"]: item for item in registry["skills"]}
        workflow = (REPO / "trellis/workflows/guru-team/workflow.md").read_text(
            encoding="utf-8"
        )
        for skill_id in PACKAGE_IDS:
            self.assertEqual(entries[skill_id]["state"], "active")
            self.assertEqual(entries[skill_id]["workflow_integration_state"], "deferred")
            self.assertNotIn(f'"skill":"{skill_id}"', workflow)

    def test_review_ready_projects_to_publish_review_ready(self) -> None:
        payload, contract = self.project_seed(
            "guru-review-task-delivery", "project_ready"
        )
        self.assertEqual(contract["profile_id"], "review_ready")
        self.assert_schema_shape(
            payload,
            self.profile_schema("guru-publish-task-delivery", "review_ready"),
        )

    def test_publish_ready_projects_to_merge_ready(self) -> None:
        payload, contract = self.project_seed(
            "guru-publish-task-delivery", "project_ready_for_merge"
        )
        self.assertEqual(contract["profile_id"], "ready_for_merge")
        self.assert_schema_shape(
            payload,
            self.profile_schema("guru-merge-task-delivery", "ready_for_merge"),
        )

    def test_publish_and_merge_stale_routes_author_fresh_review_input(self) -> None:
        for producer, projection in (
            ("guru-publish-task-delivery", "project_review_stale"),
            ("guru-merge-task-delivery", "project_review_refresh_required"),
        ):
            with self.subTest(producer=producer):
                payload, contract = self.project_seed(producer, projection)
                self.assertEqual(contract["profile_id"], "delivery_review")
                self.assert_schema_shape(
                    payload,
                    self.profile_schema("guru-review-task-delivery", "delivery_review"),
                )

    def test_delivery_contracts_exclude_terminal_lifecycle_and_bind_identity(self) -> None:
        forbidden = {"completed", "closure", "archive", "finish", "cleanup"}
        for skill_id in PACKAGE_IDS:
            interface = self.interface(skill_id)
            serialized = json.dumps(
                interface["public_contracts"]["outputs"], ensure_ascii=False
            ).lower()
            for token in forbidden:
                self.assertNotIn(token, serialized)
        ready = read_json(
            self.package("guru-review-task-delivery") / "examples/public-ready-output.json"
        )
        self.assertIn("Refs #435", ready["pr_body"])
        self.assertNotRegex(ready["pr_body"], r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#")
        owner = (
            self.package("guru-merge-task-delivery") / "runtime/owner.py"
        ).read_text(encoding="utf-8")
        self.assertIn("Guru-Task-Identity", owner)
        self.assertIn("Guru-Delivery-Schema: 1", owner)
        self.assertIn("Guru-Delivery-Head", owner)
        self.assertIn('"--merge", "--match-head-commit"', owner)
        self.assertNotIn('"--squash"', owner)
        self.assertNotIn('"--rebase"', owner)


if __name__ == "__main__":
    unittest.main()
