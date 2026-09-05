from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import jsonschema


PACKAGE = Path(__file__).resolve().parents[1]
SKILLS_ROOT = PACKAGE.parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class RestoreArchivedTaskContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.interface = load_json(PACKAGE / "interface.json")

    def test_interface_matches_current_closed_interface_schema(self) -> None:
        schema = load_json(SKILLS_ROOT / "schemas/skill-interface-1.4.schema.json")
        errors = list(jsonschema.Draft202012Validator(schema).iter_errors(self.interface))
        self.assertEqual([], errors)

    def test_frontmatter_and_identity_are_exact(self) -> None:
        text = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\nname: ([^\n]+)\ndescription: ([^\n]+)\n---\n", text)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(self.interface["name"], match.group(1))
        self.assertEqual(self.interface["description"], match.group(2))
        self.assertEqual("guru-restore-archived-task", self.interface["id"])

    def test_semantic_contract_has_two_distinct_exits_and_same_modes(self) -> None:
        self.assertEqual("semantic", self.interface["judgment_mode"])
        self.assertEqual(
            ["forward_behavior", "ai_review_gate", "conditional_human_confirmation", "recorder_validator", "typed_exit"],
            self.interface["ordered_stages"],
        )
        self.assertEqual(["restored_to_phase2", "restore_blocked"], [item["id"] for item in self.interface["external_exits"]])
        exits = {item["id"]: item["consumer"] for item in self.interface["external_exits"]}
        self.assertEqual({"kind": "workflow", "id": "guru-resume-implementation"}, exits["restored_to_phase2"])
        self.assertEqual({"kind": "stop", "id": "task-pr-phase2-reentry-blocked"}, exits["restore_blocked"])
        self.assertEqual(self.interface["modes"]["workflow"]["entry_precondition_ids"], self.interface["modes"]["standalone"]["entry_precondition_ids"])
        self.assertEqual({"shared", "codex", "cursor", "claude"}, set(self.interface["platform_destinations"]))

    def test_declared_files_exist_and_are_regular(self) -> None:
        paths = {item["path"] for section in ("artifacts", "schemas") for item in self.interface[section]}
        paths.update(self.interface["tests"])
        for item in self.interface["public_contracts"]["consumer_inputs"]:
            contract = item["contract"]
            paths.add(contract.get("path", contract.get("authoring_example", {}).get("path", "")))
        paths.add("references/contract.md")
        paths.add("commands.json")
        paths.add("errors/catalog.json")
        for relative in paths:
            with self.subTest(path=relative):
                path = PACKAGE / relative
                self.assertTrue(path.is_file())
                self.assertFalse(path.is_symlink())

    def test_examples_validate_against_their_closed_schemas(self) -> None:
        profiles = self.interface["public_contracts"]["input"]["profiles"]
        for profile in profiles:
            schema = load_json(PACKAGE / profile["schema"]["path"])
            example = load_json(PACKAGE / profile["example"]["path"])
            self.assertEqual([], list(jsonschema.Draft202012Validator(schema).iter_errors(example)))
        for relative, schema_relative in (
            ("examples/public-semantic-review.json", "schemas/semantic-review-input.schema.json"),
            ("examples/live-facts.json", "schemas/live-facts.schema.json"),
        ):
            schema = load_json(PACKAGE / schema_relative)
            example = load_json(PACKAGE / relative)
            self.assertEqual([], list(jsonschema.Draft202012Validator(schema).iter_errors(example)))
        for output in self.interface["public_contracts"]["outputs"]:
            schema = load_json(PACKAGE / output["schema"]["path"])
            example = load_json(PACKAGE / output["example"]["path"])
            self.assertEqual([], list(jsonschema.Draft202012Validator(schema).iter_errors(example)))
        self.assertEqual({"exit_id", "task_ref", "resume_target"}, set(load_json(PACKAGE / "examples/public-restored-output.json")))

    def test_public_outputs_do_not_leak_private_or_authorization_state(self) -> None:
        forbidden = {"authorization", "confirmation", "workspace_path", "local_path", "checkpoint", "payload", "gate"}
        for output in self.interface["public_contracts"]["outputs"]:
            schema = load_json(PACKAGE / output["schema"]["path"])
            self.assertFalse(forbidden.intersection(schema["properties"]))

    def test_commands_bind_one_runtime_validator_and_declared_schemas(self) -> None:
        commands = load_json(PACKAGE / "commands.json")
        self.assertEqual("guru-restore-archived-task", commands["package_id"])
        self.assertEqual({"restore_executor"}, {item["validator_id"] for item in commands["commands"]})
        self.assertEqual({"restore_executor"}, {item["id"] for item in self.interface["validators"]})
        self.assertIn("schemas/public-restore-input.schema.json", commands["commands"][0]["schema_bindings"])
        self.assertIn("schemas/live-facts.schema.json", commands["commands"][0]["schema_bindings"])
        self.assertEqual("repo_write", commands["commands"][0]["side_effect"])
        self.assertEqual([], self.interface["public_contracts"]["private_artifacts"])

    def test_merge_reentry_seed_is_exact_and_authoring_is_minimal(self) -> None:
        consumer = next(item for item in self.interface["public_contracts"]["consumer_inputs"] if item["id"] == "merge_phase2_reentry_input")
        contract = consumer["contract"]
        self.assertEqual("skill_input_authoring_seed", contract["kind"])
        self.assertEqual([
            "exit_id", "repo_ref", "pr_number", "pr_url", "expected_head_sha",
            "expected_base_branch", "expected_head_branch", "issue_number", "task_id",
            "archive_locator", "active_locator", "archive_commit", "finding_refs", "resume_target",
        ], contract["seed_fields"])
        self.assertEqual(["schema_version", "profile", "mode"], contract["authoring_fields"])

    def test_eval_corpus_has_required_normal_and_blocked_cases(self) -> None:
        corpus = load_json(PACKAGE / "evals/evals.json")
        schema = load_json(SKILLS_ROOT / "schemas/skill-evals.schema.json")
        self.assertEqual(
            [], list(jsonschema.Draft202012Validator(schema).iter_errors(corpus))
        )
        cases = {item["id"]: item for item in corpus["evals"]}
        self.assertEqual({"success", "idempotent", "external-blocker", "head-drift", "scope-drift", "dirty-worktree", "active-task-conflict", "merged-pr"}, set(cases))
        self.assertEqual({"restored_to_phase2", "restore_blocked"}, {item["expected_exit"] for item in cases.values()})
        for case in cases.values():
            for relative in case["files"]:
                self.assertTrue((PACKAGE / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
