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
from unittest import mock


PACKAGE = Path(__file__).resolve().parents[1]
PACKAGE_LAYOUTS = (
    (
        "canonical",
        Path("trellis/skills/guru-team/packages/guru-review-task-publication"),
    ),
    (
        "installed-shared",
        Path(
            ".trellis/guru-team/skills/packages/"
            "guru-review-task-publication"
        ),
    ),
    (
        "agents",
        Path(".agents/skills/guru-review-task-publication"),
    ),
    (
        "codex",
        Path(".codex/skills/guru-review-task-publication"),
    ),
    (
        "cursor",
        Path(".cursor/skills/guru-review-task-publication"),
    ),
    (
        "claude",
        Path(".claude/skills/guru-review-task-publication"),
    ),
)


def package_repo_root() -> Path:
    for candidate in PACKAGE.parents:
        if any(candidate / relative == PACKAGE for _, relative in PACKAGE_LAYOUTS):
            return candidate
    raise RuntimeError(f"Unsupported publication package test layout: {PACKAGE}")


def load_runtime():
    candidates: list[Path] = []
    for parent in PACKAGE.parents:
        candidates.extend([
            parent / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py",
            parent / ".trellis/guru-team/scripts/python/guru_team_trellis.py",
        ])
    runtime_path = next((path for path in candidates if path.is_file()), None)
    if runtime_path is None:
            raise RuntimeError("Current Guru Team runtime not found for package tests.")
    spec = importlib.util.spec_from_file_location(
        "task_publication_package_runtime",
        runtime_path,
    )
    if spec is None or spec.loader is None:
            raise RuntimeError("Current Guru Team runtime could not be loaded.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GTT = load_runtime()


class TaskPublicationContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        cls.readiness_schema = json.loads(
            (PACKAGE / "schemas/pr-readiness.schema.json").read_text(encoding="utf-8")
        )
        cls.readiness_example = json.loads(
            (PACKAGE / "examples/pr-readiness.json").read_text(encoding="utf-8")
        )

    def test_two_profiles_and_semantic_stage_order(self) -> None:
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
        profiles = self.interface["public_contracts"]["input"]["profiles"]
        self.assertEqual(
            [item["id"] for item in profiles],
            ["publication_review", "publication_review_stale"],
        )
        self.assertEqual(
            self.interface["public_contracts"]["input"]["aggregate_schema"][
                "schema_id"
            ],
            "guru-production-review-task-publication-input-aggregate-4.0",
        )
        self.assertEqual(
            profiles[1]["schema"]["schema_id"],
            "guru-production-review-task-publication-input-publication-review-stale-3.0",
        )

    def test_stale_profile_contains_only_direct_reentry_inputs(self) -> None:
        schema = json.loads(
            (
                PACKAGE
                / "schemas/public-publication-review-stale-input.schema.json"
            ).read_text(encoding="utf-8")
        )
        expected = {
            "profile",
            "mode",
            "task_ref",
            "branch_review_commit",
            "stale_reason",
            "review_intent",
        }
        self.assertEqual(set(schema["properties"]), expected)
        self.assertEqual(set(schema["required"]), expected)
        for relative in (
            "examples/public-publication-review-stale-input.json",
            "examples/public-publication-review-stale-authoring.json",
            "evals/files/stale-reentry-ready-input.json",
        ):
            payload = json.loads((PACKAGE / relative).read_text(encoding="utf-8"))
            self.assertNotIn("reentry_context", payload, relative)

    def test_three_minimal_exits_have_unique_consumers(self) -> None:
        exits = self.interface["external_exits"]
        self.assertEqual(
            [item["id"] for item in exits],
            ["ready", "return_to_task_work", "blocked"],
        )
        self.assertEqual(
            len({(item["consumer"]["kind"], item["consumer"]["id"]) for item in exits}),
            3,
        )

    def test_initial_authoring_partition_is_target_owned(self) -> None:
        branch = json.loads(
            (
                PACKAGE.parent
                / "guru-review-branch"
                / "interface.json"
            ).read_text(encoding="utf-8")
        )
        consumer = next(
            item
            for item in branch["public_contracts"]["consumer_inputs"]
            if item["id"] == "publication_seed_input"
        )
        contract = consumer["contract"]
        self.assertEqual(contract["kind"], "skill_input_authoring_seed")
        self.assertEqual(contract["seed_fields"], ["task_ref", "branch_review_commit"])
        self.assertEqual(contract["authoring_fields"], ["profile", "mode", "review_intent"])

    def test_public_outputs_exclude_private_review_state(self) -> None:
        forbidden = {
            "semantic_review",
            "findings",
            "deterministic_bindings",
            "publish_inputs",
            "facts_sha256",
            "artifact_path",
            "publication_ref",
            "review_ref",
            "human_confirmation",
        }
        for output in self.interface["public_contracts"]["outputs"]:
            schema = json.loads((PACKAGE / output["schema"]["path"]).read_text(encoding="utf-8"))
            self.assertFalse(forbidden & set(schema["properties"]))

    def test_pr_readiness_is_one_private_gate(self) -> None:
        private = self.interface["public_contracts"]["private_artifacts"]
        self.assertEqual([item["id"] for item in private], ["publication_readiness"])
        self.assertEqual(private[0]["kind"], "gate_evidence")
        self.assertEqual(
            private[0]["persistence"],
            "ignored_runtime",
        )

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_readiness_example_is_schema_and_runtime_semantic_valid(self) -> None:
        from jsonschema import Draft202012Validator

        Draft202012Validator.check_schema(self.readiness_schema)
        validator = Draft202012Validator(self.readiness_schema)
        self.assertEqual(list(validator.iter_errors(self.readiness_example)), [])
        self.assertEqual(
            GTT.task_publication_semantic_errors(
                self.readiness_example,
                branch_review_commit=self.readiness_example[
                    "branch_review_commit"
                ],
            ),
            [],
        )

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_schema_valid_runtime_invalid_duplicate_finding_refs_fail_closed(self) -> None:
        from jsonschema import Draft202012Validator

        finding = {
            "finding_ref": "PUB-001",
            "dimension": "pr_body_quality",
            "summary": "The metadata fix was reviewed and closed.",
            "scope_basis": "The publication contract owns this metadata.",
            "evidence_refs": ["pr_payload"],
            "affected_artifacts": ["pr_payload"],
            "route_class": "metadata_revision",
            "status": "closed",
            "closure_evidence": ["pr_payload#fixed"],
        }
        invalid = copy.deepcopy(self.readiness_example)
        invalid["findings"] = [finding, copy.deepcopy(finding)]
        self.assertEqual(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid)),
            [],
        )
        self.assertIn(
            "publication finding refs must be unique and non-empty",
            GTT.task_publication_semantic_errors(
                invalid,
                branch_review_commit=invalid["branch_review_commit"],
            ),
        )

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_empty_closed_finding_evidence_fails_schema_and_runtime(self) -> None:
        from jsonschema import Draft202012Validator

        invalid = copy.deepcopy(self.readiness_example)
        invalid["findings"] = [{
            "finding_ref": "PUB-EMPTY",
            "dimension": "pr_body_quality",
            "summary": "",
            "scope_basis": "",
            "evidence_refs": [],
            "affected_artifacts": [],
            "route_class": "metadata_revision",
            "status": "closed",
            "closure_evidence": [],
        }]
        self.assertTrue(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid))
        )
        self.assertIn(
            "publication finding evidence must be non-empty",
            GTT.task_publication_semantic_errors(
                invalid,
                branch_review_commit=invalid["branch_review_commit"],
            ),
        )

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_gate_schema_rejects_removed_process_and_binding_fields(self) -> None:
        from jsonschema import Draft202012Validator

        for field in (
            "generated_at",
            "facts_sha256",
            "deterministic_bindings",
            "review_identity",
            "review_ref",
            "publication_ref",
            "supersedes_publication_ref",
            "revision_history",
            "reviewer_process",
            "human_confirmation",
        ):
            with self.subTest(field=field):
                invalid = copy.deepcopy(self.readiness_example)
                invalid[field] = "forbidden"
                self.assertTrue(
                    list(
                        Draft202012Validator(self.readiness_schema).iter_errors(
                            invalid
                        )
                    )
                )

    def semantic_errors(self, payload: dict) -> list[str]:
        return GTT.task_publication_semantic_errors(
            payload,
            branch_review_commit=payload["branch_review_commit"],
        )

    @staticmethod
    def open_finding(
        *,
        finding_ref: str,
        dimension: str,
        route_class: str,
    ) -> dict:
        return {
            "finding_ref": finding_ref,
            "dimension": dimension,
            "summary": "The current publication review cannot complete.",
            "scope_basis": "The approved publication contract owns this route.",
            "evidence_refs": ["review-gate.json"],
            "affected_artifacts": ["pr_payload"],
            "route_class": route_class,
            "status": "open",
            "closure_evidence": [],
        }

    def return_payload(self) -> dict:
        payload = copy.deepcopy(self.readiness_example)
        payload["route"] = {"typed_exit": "return_to_task_work"}
        payload["dimensions"][0]["status"] = "finding"
        payload["findings"] = [
            self.open_finding(
                finding_ref="PUB-WORK-001",
                dimension="diff_outcome_consistency",
                route_class="task_work",
            )
        ]
        payload["conclusions"]["issue_scope"]["status"] = "finding"
        return payload

    def blocked_payload(self) -> dict:
        payload = copy.deepcopy(self.readiness_example)
        payload["route"] = {
            "typed_exit": "blocked",
            "reason_code": "external-publication-dependency",
            "remediation": "Restore the external dependency and re-enter.",
        }
        payload["dimensions"][-1]["status"] = "blocked"
        payload["findings"] = [
            self.open_finding(
                finding_ref="PUB-BLOCK-001",
                dimension="artifact_binding_freshness",
                route_class="external_blocker",
            )
        ]
        payload["conclusions"]["safety_deployment"]["status"] = "blocked"
        return payload

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_ready_rejects_nonpassed_conclusion_in_schema_and_runtime(self) -> None:
        from jsonschema import Draft202012Validator

        invalid = copy.deepcopy(self.readiness_example)
        invalid["conclusions"]["issue_scope"]["status"] = "blocked"
        self.assertTrue(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid))
        )
        self.assertIn(
            "ready requires every publication conclusion to pass",
            self.semantic_errors(invalid),
        )

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_return_rejects_all_passed_dimensions_in_schema_and_runtime(self) -> None:
        from jsonschema import Draft202012Validator

        invalid = self.return_payload()
        invalid["dimensions"][0]["status"] = "passed"
        self.assertTrue(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid))
        )
        errors = self.semantic_errors(invalid)
        self.assertIn(
            "return_to_task_work requires a finding publication dimension",
            errors,
        )
        self.assertIn(
            "open publication finding must reference a non-passed dimension",
            errors,
        )

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_blocked_rejects_reason_only_semantics_in_schema_and_runtime(self) -> None:
        from jsonschema import Draft202012Validator

        invalid = copy.deepcopy(self.readiness_example)
        invalid["route"] = {
            "typed_exit": "blocked",
            "reason_code": "external-publication-dependency",
            "remediation": "Restore the external dependency and re-enter.",
        }
        self.assertTrue(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid))
        )
        errors = self.semantic_errors(invalid)
        self.assertIn("blocked requires a blocked publication dimension", errors)
        self.assertIn("blocked requires an open external_blocker finding", errors)
        self.assertIn("blocked requires a blocked publication conclusion", errors)

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_valid_ready_return_and_blocked_unions_pass_both_layers(self) -> None:
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(self.readiness_schema)
        for name, payload in (
            ("ready", copy.deepcopy(self.readiness_example)),
            ("return_to_task_work", self.return_payload()),
            ("blocked", self.blocked_payload()),
        ):
            with self.subTest(exit=name):
                self.assertEqual(list(validator.iter_errors(payload)), [])
                self.assertEqual(self.semantic_errors(payload), [])

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_runtime_binds_open_findings_to_matching_nonpassed_dimensions(self) -> None:
        from jsonschema import Draft202012Validator

        invalid_return = self.return_payload()
        invalid_return["findings"][0][
            "dimension"
        ] = "pr_body_quality"
        self.assertEqual(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid_return)),
            [],
        )
        self.assertIn(
            "return_to_task_work open findings must reference finding dimensions",
            self.semantic_errors(invalid_return),
        )

        invalid_blocked = self.blocked_payload()
        invalid_blocked["findings"][0][
            "dimension"
        ] = "pr_body_quality"
        self.assertEqual(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid_blocked)),
            [],
        )
        self.assertIn(
            "blocked open findings must reference blocked dimensions",
            self.semantic_errors(invalid_blocked),
        )

    def test_stale_reentry_does_not_expand_the_owner_checkpoint(self) -> None:
        properties = set(self.readiness_schema["properties"])
        self.assertFalse(
            properties
            & {
                "profile",
                "mode",
                "review_intent",
                "stale_reason",
                "reentry_context",
                "supersedes_publication_ref",
            }
        )

    def test_ready_checker_runs_the_shared_finalizer_preflight(self) -> None:
        root = Path("/repo")
        task_dir = root / self.readiness_example["task_ref"]
        with (
            mock.patch.object(GTT, "task_publication_schema", return_value={}),
            mock.patch.object(
                GTT, "skill_json_schema_validation_errors", return_value=[]
            ),
            mock.patch.object(GTT, "load_config", return_value={}),
            mock.patch.object(
                GTT,
                "current_head",
                return_value=self.readiness_example["branch_review_commit"],
            ),
            mock.patch.object(
                GTT,
                "review_branch_content_continuity_errors",
                return_value=[],
            ),
            mock.patch.object(
                GTT,
                "reviewed_content_identity",
                return_value={
                    "algorithm": "guru-reviewed-content-1.0",
                    "sha256": self.readiness_example["reviewed_content_sha256"],
                },
            ),
            mock.patch.object(
                GTT,
                "task_publication_entry_precondition_bindings",
                return_value=({}, [], {}, {}),
            ),
            mock.patch.object(
                GTT, "task_publication_closeout_preflight"
            ) as preflight,
        ):
            errors = GTT.task_publication_check_errors(
                root,
                task_dir,
                copy.deepcopy(self.readiness_example),
            )
        self.assertEqual(errors, [])
        preflight.assert_called_once_with(
            root,
            task_dir,
            self.readiness_example["branch_review_commit"],
            self.readiness_example["pr_payload"],
        )

    def test_only_content_identity_drift_allows_return_to_task_work(
        self,
    ) -> None:
        root = Path("/repo")
        task_dir = root / self.readiness_example["task_ref"]

        def checked(
            payload: dict,
            *,
            continuity_errors: list[str] | None = None,
        ) -> list[str]:
            continuity_errors = continuity_errors or [
                GTT.BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX + "identity mismatch"
            ]
            with (
                mock.patch.object(GTT, "task_publication_schema", return_value={}),
                mock.patch.object(
                    GTT, "skill_json_schema_validation_errors", return_value=[]
                ),
                mock.patch.object(GTT, "load_config", return_value={}),
                mock.patch.object(GTT, "current_head", return_value="d" * 40),
                mock.patch.object(
                    GTT,
                    "review_branch_content_continuity_errors",
                    return_value=continuity_errors,
                ),
                mock.patch.object(
                    GTT,
                    "reviewed_content_identity",
                    return_value={
                        "algorithm": "guru-reviewed-content-1.0",
                        "sha256": "d" * 64,
                    },
                ),
                mock.patch.object(
                    GTT,
                    "task_publication_entry_precondition_bindings",
                    return_value=({}, [], {}, {}),
                ),
                mock.patch.object(GTT, "task_publication_closeout_preflight"),
                mock.patch.object(GTT, "task_publication_semantic_errors", return_value=[]),
            ):
                return GTT.task_publication_check_errors(root, task_dir, payload)

        returning = self.return_payload()
        self.assertEqual(checked(returning), [])

        ready = copy.deepcopy(self.readiness_example)
        self.assertTrue(
            any(
                "reviewed content" in error and "stale" in error
                for error in checked(ready)
            )
        )

        blocked = self.blocked_payload()
        self.assertTrue(
            any(
                "reviewed content" in error and "stale" in error
                for error in checked(blocked)
            )
        )

        for case, continuity_errors in (
            (
                "non-ancestor",
                ["Branch Review review_commit is not an ancestor of the current HEAD."],
            ),
            (
                "identity-unreadable",
                ["Branch Review could not calculate reviewed-content continuity."],
            ),
        ):
            with self.subTest(case=case):
                self.assertTrue(
                    any(
                        "reviewed content is stale" in error
                        for error in checked(
                            returning,
                            continuity_errors=continuity_errors,
                        )
                    )
                )

        invalid = copy.deepcopy(returning)
        invalid["branch_review_commit"] = "not-a-sha"
        self.assertTrue(
            any(
                "branch_review_commit is invalid" in error
                for error in checked(invalid)
            )
        )

    def test_both_modes_declare_exact_eight_entry_preconditions(self) -> None:
        expected = [
            "runtime_dependency",
            "task_workspace",
            "task_identity",
            "branch_review_handoff",
            "issue_scope_ledger",
            "publication_content",
            "review_range_and_working_tree",
            "invocation_freshness",
        ]
        self.assertEqual(
            self.interface["modes"]["workflow"]["entry_precondition_ids"],
            expected,
        )
        self.assertEqual(
            self.interface["modes"]["standalone"]["entry_precondition_ids"],
            expected,
        )

    def test_interface_validator_commands_resolve_dispatcher_in_all_supported_layouts(
        self,
    ) -> None:
        repo_root = package_repo_root()
        validator_ids = (
            "publication_review_recorder",
            "publication_review_checker",
        )
        validators = {
            item["id"]: item
            for item in self.interface["validators"]
            if item["id"] in validator_ids
        }
        self.assertEqual(set(validators), set(validator_ids))
        env = os.environ.copy()
        env.pop("GURU_TEAM_DISPATCHER", None)

        present_layouts = {
            name
            for name, relative in PACKAGE_LAYOUTS
            if (repo_root / relative).is_dir()
        }
        if "canonical" in present_layouts:
            self.assertEqual(
                present_layouts,
                {name for name, _ in PACKAGE_LAYOUTS},
            )

        for layout, relative in PACKAGE_LAYOUTS:
            package_root = repo_root / relative
            if not package_root.is_dir():
                continue
            for validator_id in validator_ids:
                validator = validators[validator_id]
                command = package_root / validator["command"]
                with self.subTest(layout=layout, validator=validator_id):
                    result = subprocess.run(
                        [str(command), "--help"],
                        cwd=repo_root,
                        env=env,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False,
                    )
                    if layout == "canonical":
                        self.assertEqual(result.returncode, 2, result.stderr)
                        self.assertIn(
                            "not an audited installed or discovery layout",
                            result.stderr,
                        )
                    else:
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertIn(
                            "usage: guru_team_trellis.py "
                            f"{validator['runtime_command']}",
                            result.stdout,
                        )

    def test_interface_validator_commands_reject_unsupported_package_layout(
        self,
    ) -> None:
        validators = {
            item["id"]: item
            for item in self.interface["validators"]
            if item["id"] in {
                "publication_review_recorder",
                "publication_review_checker",
            }
        }
        env = os.environ.copy()
        env.pop("GURU_TEAM_DISPATCHER", None)
        with tempfile.TemporaryDirectory() as temp:
            unsupported = Path(temp) / "unsupported-publication-package"
            shutil.copytree(PACKAGE, unsupported)
            for validator_id, validator in validators.items():
                with self.subTest(validator=validator_id):
                    result = subprocess.run(
                        [str(unsupported / validator["command"]), "--help"],
                        env=env,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "unsupported Skill package root "
                        "for guru-review-task-publication",
                        result.stderr,
                    )


if __name__ == "__main__":
    unittest.main()
