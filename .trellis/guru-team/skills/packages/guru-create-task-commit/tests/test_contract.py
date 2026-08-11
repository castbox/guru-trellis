from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class TaskCommitPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.interface = self.read_json("interface.json")

    def read_json(self, relative: str) -> dict[str, object]:
        return json.loads((self.package / relative).read_text(encoding="utf-8"))

    @staticmethod
    def nested_keys(value: object) -> set[str]:
        if isinstance(value, dict):
            return set(value) | {
                key
                for item in value.values()
                for key in TaskCommitPackageContractTests.nested_keys(item)
            }
        if isinstance(value, list):
            return {
                key
                for item in value
                for key in TaskCommitPackageContractTests.nested_keys(item)
            }
        return set()

    def test_identity_modes_stages_and_exits(self) -> None:
        self.assertEqual(self.interface["id"], "guru-create-task-commit")
        self.assertEqual(self.interface["schema_version"], "1.4")
        self.assertEqual(self.interface["judgment_mode"], "semantic")
        self.assertEqual(
            self.interface["ordered_stages"],
            [
                "forward_behavior",
                "ai_review_gate",
                "conditional_human_confirmation",
                "recorder_validator",
                "typed_exit",
            ],
        )
        modes = self.interface["modes"]
        self.assertEqual(modes["workflow"]["routing"], "global_workflow")
        self.assertEqual(modes["standalone"]["routing"], "direct_discovery")
        self.assertEqual(
            modes["workflow"]["entry_precondition_ids"],
            modes["standalone"]["entry_precondition_ids"],
        )
        self.assertEqual(
            [item["id"] for item in self.interface["external_exits"]],
            ["committed", "revision-required", "blocked"],
        )
        self.assertNotIn(
            "commit_authorization",
            modes["workflow"]["entry_precondition_ids"],
        )

    def test_candidate_builder_precedes_validator_and_executor(self) -> None:
        validators = self.interface["validators"]
        self.assertEqual(
            [item["id"] for item in validators],
            [
                "candidate_builder",
                "candidate_validator",
                "exact_executor",
                "public_invocation",
            ],
        )
        self.assertEqual(
            validators[0]["runtime_command"], "prepare-task-commit"
        )
        self.assertIn("before any confirmation", validators[0]["objective_scope"])
        self.assertIn("shared parser", validators[0]["objective_scope"])
        self.assertIn("private runtime cleanup", validators[2]["objective_scope"])

    def test_public_inputs_are_five_field_current_seeds(self) -> None:
        public = self.interface["public_contracts"]["input"]
        self.assertEqual(
            public["aggregate_schema"]["schema_id"],
            "guru-production-create-task-commit-input-aggregate-3.0",
        )
        expected_profiles = {
            "initial_commit",
            "revision_reentry",
            "finding_fix_commit",
            "recovery_resume",
        }
        self.assertEqual({item["id"] for item in public["profiles"]}, expected_profiles)
        for profile in public["profiles"]:
            with self.subTest(profile=profile["id"]):
                schema = self.read_json(profile["schema"]["path"])
                example = self.read_json(profile["example"]["path"])
                self.assertEqual(schema["$id"], profile["schema"]["schema_id"])
                self.assertEqual(
                    set(schema["required"]),
                    {"profile", "mode", "task_ref", "source_exit", "phase2_commit_anchor"},
                )
                self.assertEqual(set(schema["properties"]), set(schema["required"]))
                self.assertFalse(schema["additionalProperties"])
                self.assertEqual(set(example), set(schema["required"]))
                self.assertTrue(
                    self.nested_keys(example).isdisjoint(
                        {
                            "authorization",
                            "human_authorization",
                            "freshness",
                            "result",
                            "check_ref",
                            "exit_intent",
                            "message_intent",
                            "path_authorizations",
                        }
                    )
                )

    @unittest.skipUnless(
        importlib.util.find_spec("jsonschema"), "jsonschema is optional"
    )
    def test_current_schemas_validate_examples_and_reject_removed_candidate_fields(self) -> None:
        from jsonschema import Draft202012Validator

        aggregate = self.read_json("schemas/public-input.schema.json")
        Draft202012Validator.check_schema(aggregate)
        for profile in self.interface["public_contracts"]["input"]["profiles"]:
            profile_schema = self.read_json(profile["schema"]["path"])
            example = self.read_json(profile["example"]["path"])
            Draft202012Validator.check_schema(profile_schema)
            self.assertEqual(
                list(Draft202012Validator(profile_schema).iter_errors(example)), []
            )

        schema = self.read_json("schemas/task-commit-candidate.schema.json")
        candidate = self.read_json("examples/task-commit-candidate.json")
        self.assertEqual(schema["$id"], "https://github.com/castbox/guru-trellis/schemas/guru-task-commit-candidate-5.0.json")
        self.assertEqual(candidate["schema_version"], "5.0")
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        self.assertEqual(list(validator.iter_errors(candidate)), [])
        for field, value in (
            ("authorization", {"status": "confirmed"}),
            ("freshness", {"digest": "a" * 64}),
            ("result", {"status": "committed"}),
        ):
            with self.subTest(field=field):
                invalid = copy.deepcopy(candidate)
                invalid[field] = value
                self.assertTrue(list(validator.iter_errors(invalid)))
        invalid_message = copy.deepcopy(candidate)
        invalid_message["message"]["sha256"] = "a" * 64
        self.assertTrue(list(validator.iter_errors(invalid_message)))
        legacy = copy.deepcopy(candidate)
        legacy["$schema"] = "https://github.com/castbox/guru-trellis/schemas/guru-task-commit-candidate-4.0.json"
        legacy["schema_version"] = "4.0"
        self.assertTrue(list(validator.iter_errors(legacy)))

    def test_candidate_message_is_canonical_and_has_no_digest_or_authorization_chain(self) -> None:
        candidate = self.read_json("examples/task-commit-candidate.json")
        message = candidate["message"]
        subject = (
            f'{message["type"]}({message["scope"]}): #123 {message["summary"]}'
        )
        body = (
            f'背景：\n{message["background"]}\n\n'
            f'变更：\n{message["changes"]}\n\n'
            f'边界：\n{message["boundaries"]}\n\n'
            f'验证：\n{message["validations"]}\n\n'
            "Refs #123"
        )
        self.assertEqual(message["subject"], subject)
        self.assertEqual(message["body"], body)
        self.assertEqual(message["bytes"], f"{subject}\n\n{body}\n")
        self.assertTrue(
            self.nested_keys(candidate).isdisjoint(
                {
                    "authorization",
                    "human_authorization",
                    "freshness",
                    "result",
                    "check_ref",
                    "plan_digest",
                    "sha256",
                }
            )
        )

    def test_candidate_has_no_branch_classification_or_operation_authority(self) -> None:
        candidate = self.read_json("examples/task-commit-candidate.json")
        removed = {
            "routine_auto_" + "commit_facts",
            "routine_auto_" + "commit_eligible",
            "dedicated_task_worktree",
            "dedicated_task_" + "branch",
            "default_branch_" + "excluded",
            "protected_branch_" + "excluded",
            "shared_branch_" + "excluded",
            "other_task_branch_" + "excluded",
            "remote_branch_absent",
            "open_pull_request_absent",
            "authorization",
            "confirmation",
            "human_authorization",
        }
        self.assertTrue(self.nested_keys(candidate).isdisjoint(removed))

    def test_current_repository_surfaces_do_not_reintroduce_removed_eligibility(self) -> None:
        repo = self.package.parents[4]
        banned = (
            "routine_auto_" + "commit_facts",
            "routine_auto_" + "commit_eligible",
            "dedicated_task_" + "branch",
            "default_branch_" + "excluded",
            "protected_branch_" + "excluded",
            "shared_branch_" + "excluded",
            "other_task_branch_" + "excluded",
            "/rules/" + "branches/",
        )
        findings: list[str] = []
        for path in repo.rglob("*"):
            relative = path.relative_to(repo)
            if (
                not path.is_file()
                or ".git" in relative.parts
                or "__pycache__" in relative.parts
                or relative.parts[:2] == (".trellis", "tasks")
            ):
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for term in banned:
                if term in content:
                    findings.append(f"{relative}:{term}")
        self.assertEqual(findings, [])

    def test_outputs_are_minimal_and_each_projection_has_one_consumer(self) -> None:
        contracts = self.interface["public_contracts"]
        expected_fields = {
            "committed": {"exit_id", "task_ref", "base_ref", "branch_review_commit"},
            "revision-required": {"exit_id", "task_ref"},
            "blocked": {"exit_id"},
        }
        output_ids = {item["exit_id"] for item in contracts["outputs"]}
        projection_ids = {item["exit_id"] for item in contracts["projections"]}
        self.assertEqual(output_ids, set(expected_fields))
        self.assertEqual(projection_ids, output_ids)
        for output in contracts["outputs"]:
            with self.subTest(exit_id=output["exit_id"]):
                schema = self.read_json(output["schema"]["path"])
                example = self.read_json(output["example"]["path"])
                self.assertEqual(set(schema["required"]), expected_fields[output["exit_id"]])
                self.assertEqual(set(schema["properties"]), set(schema["required"]))
                self.assertEqual(set(example), set(schema["required"]))
                self.assertEqual(len(output["consumer_use_ids"]), 1)
        private = contracts["private_artifacts"]
        self.assertEqual([item["id"] for item in private], ["task_commit_candidate"])
        self.assertEqual(private[0]["persistence"], "ignored_runtime")
        self.assertIn("candidate-5.0", private[0]["schema"]["schema_id"])

    def test_wrappers_are_executable_thin_and_fail_outside_complete_preset(self) -> None:
        wrapper_names = (
            "prepare-task-commit.sh",
            "check-task-commit-plan.sh",
            "create-task-commit.sh",
        )
        for name in wrapper_names:
            with self.subTest(name=name):
                wrapper = self.package / "scripts" / name
                content = wrapper.read_text(encoding="utf-8")
                self.assertTrue(os.access(wrapper, os.X_OK))
                self.assertIn("run-skill-command.sh", content)
                self.assertIn("--package-root \"$PACKAGE_ROOT\" --validator", content)
                self.assertNotIn("git add", content)
                self.assertNotIn("python3", content)

        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "guru-create-task-commit"
            shutil.copytree(self.package, copied)
            for name in wrapper_names:
                with self.subTest(package_only=name):
                    result = subprocess.run(
                        [str(copied / "scripts" / name), "--help"],
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False,
                    )
                    self.assertEqual(result.returncode, 2, result)
                    self.assertIn("not self-contained or portable", result.stderr)
                    self.assertIn(
                        "Install or upgrade the complete Guru Team preset",
                        result.stderr,
                    )

    def test_candidate_is_private_current_runtime_state(self) -> None:
        contract = (self.package / "references/contract.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            ".trellis/.runtime/guru-team/task-commit-plans/",
            "before any required confirmation",
            "deletes the private candidate",
            "authorization",
            "ignored",
        ):
            self.assertIn(phrase, contract)
        self.assertEqual(
            self.interface["public_contracts"]["private_artifacts"][0]["schema"]["path"],
            "schemas/task-commit-candidate.schema.json",
        )
        self.assertFalse((self.package / "examples/task-commit-plan.json").exists())
        self.assertFalse((self.package / "schemas/task-commit-plan.schema.json").exists())

    def test_eval_public_inputs_do_not_reintroduce_removed_fields(self) -> None:
        evals = self.read_json("evals/evals.json")
        self.assertEqual(evals["skill_name"], "guru-create-task-commit")
        for eval_case in evals["evals"]:
            input_paths = [
                path for path in eval_case["files"] if path.endswith("-input.json")
            ]
            self.assertEqual(len(input_paths), 1)
            value = self.read_json(input_paths[0])
            self.assertEqual(
                set(value),
                {"profile", "mode", "task_ref", "source_exit", "phase2_commit_anchor"},
            )
            self.assertTrue(
                self.nested_keys(value).isdisjoint(
                    {
                        "authorization",
                        "human_authorization",
                        "freshness",
                        "result",
                        "check_ref",
                        "exit_intent",
                    }
                )
            )


if __name__ == "__main__":
    unittest.main()
