from __future__ import annotations

import json
import unittest
from pathlib import Path

import jsonschema


PACKAGE = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def interface(self) -> dict:
        return self.load(PACKAGE / "interface.json")

    def projection_payload(self, projection: dict, output: dict) -> dict:
        if projection["operation"] == "direct":
            return dict(output)
        return {
            mapping["target"]: output[mapping["source"]]
            for mapping in projection["mappings"]
        }

    def test_json_and_schemas(self) -> None:
        for path in PACKAGE.rglob("*.json"):
            with self.subTest(path=path.relative_to(PACKAGE)):
                value = json.loads(path.read_text(encoding="utf-8"))
                if path.name.endswith(".schema.json"):
                    jsonschema.Draft202012Validator.check_schema(value)

    def test_examples_validate(self) -> None:
        pairs = {
            "public-review-ready-input.json": "public-review-ready-input.schema.json",
            "public-same-plan-resume-input.json": "public-same-plan-resume-input.schema.json",
            "public-reprepare-publication-input.json": "public-reprepare-publication-input.schema.json",
            "semantic-review.json": "semantic-review.schema.json",
            "public-ready-for-merge-output.json": "public-ready-for-merge-output.schema.json",
            "public-review-stale-output.json": "public-review-stale-output.schema.json",
            "public-resume-publication-output.json": "public-resume-publication-output.schema.json",
            "public-reprepare-required-output.json": "public-reprepare-required-output.schema.json",
            "public-blocked-output.json": "public-blocked-output.schema.json",
            "public-invocation-error.json": "public-invocation-error.schema.json",
        }
        for example, schema in pairs.items():
            with self.subTest(example=example):
                jsonschema.Draft202012Validator(json.loads((PACKAGE / "schemas" / schema).read_text())).validate(json.loads((PACKAGE / "examples" / example).read_text()))

    def test_interface_is_delivery_only(self) -> None:
        interface = self.interface()
        self.assertEqual(interface["judgment_mode"], "semantic")
        self.assertEqual([item["id"] for item in interface["external_exits"]], ["ready_for_merge", "review_stale", "resume_publication", "reprepare_required", "blocked"])
        self.assertEqual(interface["public_contracts"]["private_artifacts"][0]["persistence"], "ignored_runtime")
        exit_ids = {item["id"] for item in interface["external_exits"]}
        self.assertTrue(exit_ids.isdisjoint({"completed", "archived", "issue_closed", "cleanup"}))
        self.assertFalse(any(token in exit_id for exit_id in exit_ids for token in ("archive", "finish", "completion", "cleanup")))

    def test_stage_order_is_closed(self) -> None:
        source = (PACKAGE / "runtime/owner.py").read_text()
        self.assertIn('(\"push_content\", \"bind_pr\", \"converge_metadata\", \"mark_ready\", \"ready\")', source)

    def test_declared_json_schema_consumer_paths_exist_and_validate(self) -> None:
        interface = self.interface()
        consumers = interface["public_contracts"]["consumer_inputs"]
        for consumer in consumers:
            contract = consumer["contract"]
            if contract["kind"] != "json_schema":
                continue
            with self.subTest(consumer=consumer["id"]):
                target_path = PACKAGE / contract["path"]
                self.assertTrue(target_path.is_file(), target_path)
                schema = self.load(target_path)
                jsonschema.Draft202012Validator.check_schema(schema)

    def test_review_stale_projection_authoring_matches_delivery_review_profile(self) -> None:
        interface = self.interface()
        consumer = next(
            item for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "review_stale_input"
        )
        authoring = self.load(PACKAGE / consumer["contract"]["authoring_example"]["path"])
        projection = next(
            item for item in interface["public_contracts"]["projections"]
            if item["id"] == "project_review_stale"
        )
        self.assertEqual(consumer["contract"]["profile_id"], "delivery_review")
        self.assertEqual(consumer["contract"]["seed_fields"], ["task_ref"])
        self.assertEqual(consumer["contract"]["authoring_fields"], ["profile", "mode", "branch_review_commit"])
        self.assertEqual(set(authoring), {"profile", "mode", "branch_review_commit"})
        self.assertEqual([mapping["source"] for mapping in projection["mappings"]], ["task_ref"])

    def test_review_stale_projection_matches_review_owned_profile(self) -> None:
        interface = self.interface()
        consumer = next(
            item
            for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "review_stale_input"
        )
        projection = next(
            item
            for item in interface["public_contracts"]["projections"]
            if item["id"] == "project_review_stale"
        )
        self.assertEqual(consumer["contract"]["profile_id"], "delivery_review")
        self.assertEqual(consumer["contract"]["seed_fields"], ["task_ref"])
        self.assertEqual(consumer["contract"]["authoring_fields"], ["profile", "mode", "branch_review_commit"])
        self.assertEqual(
            [mapping["source"] for mapping in projection["mappings"]],
            ["task_ref"],
        )


if __name__ == "__main__":
    unittest.main()
