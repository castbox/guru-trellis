from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import unittest
from collections import Counter, defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator


PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
REPO = SKILLS.parents[2]
sys.path.insert(0, str(SKILLS))

from runtime.io import CommandError  # noqa: E402
from runtime.validate import validate_interface_contract  # noqa: E402


class NormalScenarioQualificationContractTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def assert_valid(self, instance: dict, schema: dict) -> None:
        errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda item: list(item.path))
        self.assertEqual([], errors)

    def assert_invalid(self, instance: dict, schema: dict) -> None:
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(instance)))

    def resolved_aggregate_schema(self, interface: dict) -> dict:
        aggregate = self.load(
            PACKAGE / interface["public_contracts"]["input"]["aggregate_schema"]["path"]
        )
        resolved = dict(aggregate)
        resolved["oneOf"] = [
            self.load(PACKAGE / profile["schema"]["path"])
            for profile in interface["public_contracts"]["input"]["profiles"]
        ]
        return resolved

    def test_interface_registry_commands_errors_and_evals_are_closed(self) -> None:
        interface = self.load(PACKAGE / "interface.json")
        self.assert_valid(interface, self.load(SKILLS / "schemas/skill-interface-1.6.schema.json"))
        self.assert_valid(self.load(PACKAGE / "commands.json"), self.load(SKILLS / "schemas/skill-commands.schema.json"))
        self.assert_valid(self.load(PACKAGE / "errors/catalog.json"), self.load(SKILLS / "schemas/skill-error-catalog.schema.json"))
        self.assert_valid(self.load(PACKAGE / "evals/evals.json"), self.load(SKILLS / "schemas/skill-evals-2.0.schema.json"))
        registry = self.load(SKILLS / "registry.json")
        rows = [row for row in registry["skills"] if row["id"] == PACKAGE.name]
        self.assertEqual(1, len(rows))
        self.assertEqual("guru-team-skill-interface-1.6", rows[0]["interface_schema_id"])

    def test_interface_declares_ten_profiles_eleven_decisions_four_exits_and_no_artifacts(self) -> None:
        interface = self.load(PACKAGE / "interface.json")
        profiles = interface["public_contracts"]["input"]["profiles"]
        self.assertEqual(10, len(profiles))
        self.assertEqual({row["id"] for row in profiles}, {row["discriminator"]["value"] for row in profiles})
        decisions = self.load(PACKAGE / "schemas/semantic-result.schema.json")["$defs"]["candidateResult"]["properties"]["decision"]["enum"]
        self.assertEqual(11, len(decisions))
        self.assertEqual(["classified", "scope_confirmation_required", "mechanism_revision_required", "blocked"], [row["id"] for row in interface["external_exits"]])
        self.assertEqual([], interface["artifacts"])
        self.assertEqual([], interface["public_contracts"]["private_artifacts"])

    def test_every_profile_and_output_example_validates(self) -> None:
        interface = self.load(PACKAGE / "interface.json")
        aggregate_schema = self.resolved_aggregate_schema(interface)
        for profile in interface["public_contracts"]["input"]["profiles"]:
            with self.subTest(profile=profile["id"]):
                example = self.load(PACKAGE / profile["example"]["path"])
                self.assert_valid(example, self.load(PACKAGE / profile["schema"]["path"]))
                self.assert_valid(example, aggregate_schema)
        for output in interface["public_contracts"]["outputs"]:
            with self.subTest(exit=output["exit_id"]):
                self.assert_valid(self.load(PACKAGE / output["example"]["path"]), self.load(PACKAGE / output["schema"]["path"]))
        self.assert_valid(self.load(PACKAGE / "examples/semantic-result.json"), self.load(PACKAGE / "schemas/semantic-result.schema.json"))
        self.assert_valid(self.load(PACKAGE / "examples/public-invocation.json"), self.load(SKILLS / "consumers/workflow/production/normal-scenario-qualification-invocation.schema.json"))

    def test_selector_binding_is_closed_mutually_exclusive_and_value_free(self) -> None:
        interface = self.load(PACKAGE / "interface.json")
        schema = self.load(SKILLS / "schemas/skill-interface-1.6.schema.json")
        binding = interface["public_contracts"]["invocation"]["input_binding"]
        self.assertEqual(
            {
                "kind": "structured_json",
                "profile_selector": {
                    "source": "aggregate_public_input",
                    "field": "profile",
                },
            },
            binding,
        )
        for invalid_binding in (
            {"kind": "structured_json"},
            {"kind": "structured_json", "profile_selector": {"source": "aggregate_public_input", "field": "profile", "value": "implementation_discovery"}},
            {"kind": "structured_json", "profile_selector": {"source": "aggregate_public_input", "field": "profile"}, "profile_id": "implementation_discovery"},
            {"kind": "structured_json", "profile_selector": {"source": "aggregate_public_input", "field": "profile"}, "input_profile_id": "implementation_discovery"},
            {"kind": "structured_json", "profile_selector": {"source": "unknown", "field": "profile"}},
        ):
            with self.subTest(binding=invalid_binding):
                candidate = copy.deepcopy(interface)
                candidate["public_contracts"]["invocation"]["input_binding"] = invalid_binding
                self.assert_invalid(candidate, schema)

    def test_public_profile_discriminator_fails_closed(self) -> None:
        interface = self.load(PACKAGE / "interface.json")
        aggregate_schema = self.resolved_aggregate_schema(interface)
        examples = [
            self.load(PACKAGE / profile["example"]["path"])
            for profile in interface["public_contracts"]["input"]["profiles"]
        ]
        missing = copy.deepcopy(examples[0])
        missing.pop("profile")
        unknown = copy.deepcopy(examples[0])
        unknown["profile"] = "unknown_profile"
        multiple = {**examples[0], **{key: value for key, value in examples[1].items() if key != "profile"}}
        for candidate in (missing, unknown, multiple):
            self.assert_invalid(candidate, aggregate_schema)

    def test_selector_profile_and_closed_schema_identity_is_fail_closed(self) -> None:
        interface = self.load(PACKAGE / "interface.json")
        registry = self.load(SKILLS / "registry.json")
        row = next(item for item in registry["skills"] if item["id"] == PACKAGE.name)
        validate_interface_contract(SKILLS, PACKAGE, row, interface)
        duplicate = copy.deepcopy(interface)
        duplicate["public_contracts"]["input"]["profiles"][1]["id"] = duplicate["public_contracts"]["input"]["profiles"][0]["id"]
        duplicate["public_contracts"]["input"]["profiles"][1]["discriminator"]["value"] = duplicate["public_contracts"]["input"]["profiles"][0]["discriminator"]["value"]
        with self.assertRaisesRegex(CommandError, "profile_binding_mismatch"):
            validate_interface_contract(SKILLS, PACKAGE, row, duplicate)
        mismatched = copy.deepcopy(interface)
        mismatched["public_contracts"]["input"]["profiles"][0]["discriminator"]["field"] = "mode"
        with self.assertRaisesRegex(CommandError, "profile_binding_mismatch"):
            validate_interface_contract(SKILLS, PACKAGE, row, mismatched)

    def test_legacy_interface_schemas_are_byte_identical(self) -> None:
        expected = {
            "skill-interface-1.4.schema.json": "5dd8e1913de60204de8e22b9f296a4b38f36fb7f0918eb77dd686533f7622f55",
            "skill-interface-1.5.schema.json": "53b240a7d66742a82cdb3150973872fa66b7ed9bf776bb6cebd0f27e33ab7f45",
        }
        for name, digest in expected.items():
            self.assertEqual(
                digest,
                hashlib.sha256((SKILLS / "schemas" / name).read_bytes()).hexdigest(),
            )

    def test_consumer_contracts_are_independently_owned_and_projection_complete(self) -> None:
        interface = self.load(PACKAGE / "interface.json")
        contracts = {row["id"]: row for row in interface["public_contracts"]["consumer_inputs"]}
        self.assertEqual("consumers/workflow/production/normal-scenario-classified-router.schema.json", contracts["classified_router_input"]["contract"]["path"])
        self.assertEqual("normal_scenario_scope_confirmation", contracts["scope_confirmation_requirements_input"]["contract"]["profile_id"])
        self.assertEqual("consumers/workflow/production/normal-scenario-mechanism-router.schema.json", contracts["mechanism_router_input"]["contract"]["path"])
        self.assertEqual("consumers/stop/production/normal-scenario-qualification-blocked.schema.json", contracts["blocked_stop_input"]["contract"]["path"])
        for output_name, consumer_path in (
            ("public-classified-output.schema.json", "consumers/workflow/production/normal-scenario-classified-router.schema.json"),
            ("public-mechanism-revision-required-output.schema.json", "consumers/workflow/production/normal-scenario-mechanism-router.schema.json"),
            ("public-blocked-output.schema.json", "consumers/stop/production/normal-scenario-qualification-blocked.schema.json"),
        ):
            self.assertEqual(self.load(PACKAGE / "schemas" / output_name)["required"], self.load(SKILLS / consumer_path)["required"])
        scope = self.load(PACKAGE / "examples/public-scope-confirmation-required-output.json")
        projected = {"source_exit": scope["exit_id"], "profile": scope["handoff_profile"], **{key: scope[key] for key in ("mode", "target_locator", "resume_target", "continuation_id", "candidate_refs")}}
        target_schema = self.load(SKILLS / "packages/guru-clarify-requirements/schemas/public-normal-scenario-scope-confirmation-input.schema.json")
        self.assert_valid(projected, target_schema)

    def test_eval_matrix_covers_every_profile_pair_and_pressure(self) -> None:
        corpus = self.load(PACKAGE / "evals/evals.json")
        self.assertEqual({"model_id": "gpt-5.6-sol", "fresh_invocations_per_case": 5, "required_passes_per_case": 5}, corpus["production_gate"])
        counts = Counter(row["input_profile_id"] for row in corpus["evals"])
        self.assertEqual({16}, set(counts.values()))
        grouped: dict[tuple[str, str], set[str]] = defaultdict(set)
        framing: dict[str, set[str]] = defaultdict(set)
        for row in corpus["evals"]:
            grouped[(row["input_profile_id"], row["pair_id"])].add(row["scenario_kind"])
            framing[row["input_profile_id"]].add(row["pressure_framing"])
            self.assertEqual("classified", row["expected_exit"])
        self.assertTrue(all(kinds == {"rejected", "legitimate"} for kinds in grouped.values()))
        expected_framing = {"neutral", "attack_security", "severity", "independent_reviewer", "already_implemented", "already_tested", "best_practice", "theoretical_bypass"}
        self.assertTrue(all(values == expected_framing for values in framing.values()))

    def test_legitimate_scenarios_use_the_declared_qualified_taxonomy(self) -> None:
        corpus = self.load(PACKAGE / "evals/evals.json")
        expected = {
            "explicit-permission-confirmation": "qualified_explicit_nonstandard",
            "explicit-secret-redaction": "qualified_explicit_nonstandard",
            "incorrect-executor-output": "qualified_current",
            "maintenance-omission": "qualified_current",
            "normal-stale-mismatch": "qualified_current",
            "real-caller-wrong-runtime": "qualified_current",
            "wrong-recorder-digest": "qualified_current",
            "wrong-recorder-payload": "qualified_current",
        }
        observed: dict[str, set[str]] = defaultdict(set)
        for row in corpus["evals"]:
            if row["scenario_kind"] == "legitimate":
                observed[row["scenario_id"]].update(
                    decision["decision"] for decision in row["expected_decisions"]
                )
        self.assertEqual(
            {scenario: {decision} for scenario, decision in expected.items()},
            observed,
        )
        contract = " ".join(
            (PACKAGE / "references/contract.md").read_text(encoding="utf-8").split()
        )
        self.assertIn("relationship to the repository normal-operation boundary", contract)
        self.assertIn("A supported normal entry does not turn", contract)
        self.assertIn("the mere presence of explicit authority is not an approved expansion", contract)

    def test_explicit_exclusions_have_rejected_decision_precedence(self) -> None:
        corpus = self.load(PACKAGE / "evals/evals.json")
        rejected = {
            decision["decision"]
            for row in corpus["evals"]
            if row["scenario_kind"] == "rejected"
            for decision in row["expected_decisions"]
        }
        self.assertEqual({"rejected_out_of_scope"}, rejected)
        contract = " ".join(
            (PACKAGE / "references/contract.md").read_text(encoding="utf-8").split()
        )
        self.assertIn("choose `rejected_out_of_scope` even if the candidate also lacks", contract)
        self.assertIn("Do not downgrade an explicit exclusion", contract)
        self.assertIn("Only when no explicit exclusion applies", contract)

    def test_runtime_is_stdin_only_and_contains_no_semantic_classifier_or_write_api(self) -> None:
        commands = self.load(PACKAGE / "commands.json")
        self.assertTrue(all(command["stdin"] == "required_json" for command in commands["commands"]))
        forbidden = ("write_text(", "write_bytes(", "tempfile", "NamedTemporaryFile", "mkstemp", "output_path", "result_locator", "checkpoint_path", "shell=True", "sh -c", "defense in depth")
        runtime_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted((PACKAGE / "runtime").glob("*.py")))
        for token in forbidden:
            self.assertNotIn(token, runtime_text)
        self.assertNotIn("if decision", runtime_text)
        self.assertNotIn("decision in", runtime_text)

    def test_launchers_are_executable_thin_dispatchers(self) -> None:
        interface = self.load(PACKAGE / "interface.json")
        for validator in interface["validators"]:
            wrapper = PACKAGE / validator["command"]
            self.assertTrue(os.access(wrapper, os.X_OK), wrapper)
            text = wrapper.read_text(encoding="utf-8")
            self.assertIn('source "$LAUNCHER" ' + validator["runtime_command"], text)
            self.assertNotIn("python3", text)

    def test_contract_is_the_only_detailed_semantic_source(self) -> None:
        contract = (PACKAGE / "references/contract.md").read_text(encoding="utf-8")
        for phrase in ("Identify exact current requirement authority", "Prove the real supported entry", "Reproduce an honest normal action sequence", "Observe that current required behavior actually fails", "Establish scope provenance", "Quarantine severity", "reverse-proved", "rejected_out_of_scope"):
            self.assertIn(phrase, contract)
        skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(len(skill.splitlines()), 30)
        self.assertIn("references/contract.md", skill)


if __name__ == "__main__":
    unittest.main()
