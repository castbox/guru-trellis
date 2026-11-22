from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[1]
REPO = SKILLS.parents[2]
PACKAGE_IDS = (
    "guru-review-branch",
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
        self.assertLessEqual(set(schema["required"]), set(payload))
        self.assertFalse(set(payload) - set(schema["properties"]))
        for field, rules in schema["properties"].items():
            if "const" in rules:
                self.assertEqual(payload[field], rules["const"])
            if "pattern" in rules and field in payload:
                self.assertRegex(str(payload[field]), re.compile(rules["pattern"]))

    def edge(self, producer_id: str, exit_id: str) -> tuple[dict, dict, dict]:
        package = self.package(producer_id)
        interface = self.interface(producer_id)
        outputs = interface["public_contracts"]["outputs"]
        projections = interface["public_contracts"]["projections"]
        inputs = interface["public_contracts"]["consumer_inputs"]
        output = next(item for item in outputs if item["exit_id"] == exit_id)
        projection = next(item for item in projections if item["exit_id"] == exit_id)
        consumer = next(item for item in inputs if item["id"] == projection["consumer_input_id"])
        payload = read_json(package / output["example"]["path"])
        if projection["operation"] != "direct":
            payload = {row["target"]: payload[row["source"]] for row in projection["mappings"]}
        return payload, consumer["consumer"], consumer["contract"]

    def test_packages_are_active_integrated_with_production_markers(self) -> None:
        registry = read_json(SKILLS / "registry.json")
        entries = {item["id"]: item for item in registry["skills"]}
        workflow = "\n".join((REPO / path).read_text(encoding="utf-8") for path in (
            "trellis/workflows/guru-team/workflow.md", "trellis/workflows/guru-team/references/routing.md"))
        for skill_id in PACKAGE_IDS:
            self.assertEqual(entries[skill_id]["state"], "active")
            self.assertEqual(entries[skill_id].get("workflow_integration_state", "integrated"), "integrated")
            self.assertRegex(workflow, r'"skill"\s*:\s*"'+re.escape(skill_id)+r'"')

    def test_current_graph_has_one_publication_writer_and_no_split_ready_consumer(self) -> None:
        registry = read_json(SKILLS / "registry.json")
        active = {entry["id"] for entry in registry["skills"] if entry["state"] == "active"}
        self.assertNotIn("guru-review-task-delivery", active)
        workflow = (REPO / "trellis/workflows/guru-team/workflow.md").read_text()
        declaration = workflow.split("[trellis-runtime-contract]", 1)[1].split("[/trellis-runtime-contract]", 1)[0]
        owners = json.loads(declaration)["owners"]
        self.assertEqual(owners["readiness"], "guru-publish-task-delivery")
        self.assertEqual(owners["publication"], "guru-publish-task-delivery")
        payload, consumer, contract = self.edge("guru-review-branch", "passed")
        self.assertEqual(consumer, {"kind": "workflow", "id": "guru-publication-entry-router"})
        self.assert_schema_shape(payload, read_json(self.package("guru-review-branch") / contract["path"]))

    def test_publication_preview_and_refresh_edges_preserve_the_exact_payload(self) -> None:
        publish = "guru-publish-task-delivery"
        payload, consumer, contract = self.edge(publish, "publication_prepared")
        self.assertEqual(consumer, {"kind": "workflow", "id": "guru-publication-preview-router"})
        self.assert_schema_shape(payload, read_json(self.package(publish) / contract["path"]))
        from sys import path as module_paths
        if str(SKILLS) not in module_paths:
            module_paths.insert(0, str(SKILLS))
        from runtime.schema import validate_json
        input_contract = self.interface(publish)["public_contracts"]["input"]
        execute = next(profile for profile in input_contract["profiles"] if profile["id"] == "delivery_execute_publication")
        validate_json(
            {"profile": "delivery_execute_publication", "prepared": payload},
            self.package(publish) / execute["schema"]["path"],
            "execute",
        )
        for producer, exit_id in ((publish, "review_stale"), ("guru-merge-task-delivery", "review_refresh_required")):
            with self.subTest(producer=producer):
                payload, consumer, contract = self.edge(producer, exit_id)
                self.assertEqual(consumer, {"kind": "workflow", "id": "guru-publication-review-router"})
                self.assert_schema_shape(payload, read_json(self.package(producer) / contract["path"]))

    def test_merge_receives_distinct_current_and_historical_calls(self) -> None:
        for exit_id, profile in (
            ("ready_for_merge", "delivery_ready_for_merge"),
            ("merged_recovery_required", "delivery_merged_recovery"),
            ("merged_adoption_required", "delivery_adopt_merged_pr"),
        ):
            with self.subTest(exit_id=exit_id):
                producer = "guru-publish-task-delivery"
                payload, consumer, contract = self.edge(producer, exit_id)
                self.assertEqual(consumer, {"kind": "skill", "id": "guru-merge-task-delivery"})
                self.assertEqual(contract["profile_id"], profile)
                authoring_path = self.package(producer) / contract["authoring_example"]["path"]
                authored = read_json(authoring_path)
                inbound = {**payload, **{key: authored[key] for key in contract["authoring_fields"]}}
                self.assert_schema_shape(inbound, self.profile_schema(consumer["id"], profile))

    def test_delivery_contracts_exclude_terminal_lifecycle_and_bind_identity(self) -> None:
        forbidden = {"completed", "closure", "archive", "finish", "cleanup"}
        for skill_id in PACKAGE_IDS[1:]:
            interface = self.interface(skill_id)
            serialized = json.dumps(
                interface["public_contracts"]["outputs"], ensure_ascii=False
            ).lower()
            for token in forbidden:
                # Withdrawal has a Completion consumer, never a completion claim.
                self.assertNotIn(token, serialized)
        ready = read_json(
            self.package("guru-publish-task-delivery") / "examples/public-output-publication-prepared-1.0.json"
        )
        self.assertRegex(ready["pr_body"], r"Refs #\d+")
        self.assertNotRegex(ready["pr_body"], r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#")
        owner = (
            self.package("guru-merge-task-delivery") / "runtime/owner.py"
        ).read_text(encoding="utf-8")
        self.assertIn("Guru-Task-Identity", owner)
        self.assertIn("Guru-Delivery-Identity", owner)
        self.assertIn("Guru-Task-Generation", owner)
        self.assertIn("Guru-Delivery-Head", owner)
        self.assertIn('"--merge", "--match-head-commit"', owner)
        self.assertNotIn('"--squash"', owner)
        self.assertNotIn('"--rebase"', owner)


if __name__ == "__main__":
    unittest.main()
