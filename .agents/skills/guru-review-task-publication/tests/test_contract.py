from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]


def load_runtime():
    candidates: list[Path] = []
    for parent in PACKAGE.parents:
        candidates.extend([
            parent / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py",
            parent / ".trellis/guru-team/scripts/python/guru_team_trellis.py",
        ])
    runtime_path = next((path for path in candidates if path.is_file()), None)
    if runtime_path is None:
        raise RuntimeError("Compatible Guru Team runtime not found for package tests.")
    spec = importlib.util.spec_from_file_location(
        "task_publication_package_runtime",
        runtime_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Compatible Guru Team runtime could not be loaded.")
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
            ["forward_behavior", "ai_review_gate", "conditional_human_confirmation", "recorder_validator", "typed_exit"],
        )
        profiles = self.interface["public_contracts"]["input"]["profiles"]
        self.assertEqual(
            [item["id"] for item in profiles],
            ["publication_review", "publication_review_stale"],
        )

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
        self.assertEqual(contract["seed_fields"], ["task_ref", "reviewed_head", "review_ref"])
        self.assertEqual(contract["authoring_fields"], ["profile", "mode", "review_intent"])

    def test_public_outputs_exclude_private_review_state(self) -> None:
        forbidden = {
            "semantic_review",
            "findings",
            "deterministic_bindings",
            "publish_inputs",
            "facts_sha256",
            "artifact_path",
        }
        for output in self.interface["public_contracts"]["outputs"]:
            schema = json.loads((PACKAGE / output["schema"]["path"]).read_text(encoding="utf-8"))
            self.assertFalse(forbidden & set(schema["properties"]))

    def test_pr_readiness_is_one_private_gate(self) -> None:
        private = self.interface["public_contracts"]["private_artifacts"]
        self.assertEqual([item["id"] for item in private], ["publication_readiness"])
        self.assertEqual(private[0]["kind"], "gate_evidence")
        self.assertEqual(private[0]["persistence"], "task_local_tracked")

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_readiness_example_is_schema_and_runtime_semantic_valid(self) -> None:
        from jsonschema import Draft202012Validator

        Draft202012Validator.check_schema(self.readiness_schema)
        validator = Draft202012Validator(self.readiness_schema)
        self.assertEqual(list(validator.iter_errors(self.readiness_example)), [])
        identity = self.readiness_example["review_identity"]
        self.assertEqual(
            GTT.task_publication_semantic_errors(
                self.readiness_example,
                reviewed_head=identity["reviewed_head"],
                review_ref=identity["review_ref"],
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
            "evidence_refs": ["pr-body.md"],
            "affected_artifacts": ["pr-body.md"],
            "route_class": "metadata_revision",
            "status": "closed",
            "closure_evidence": ["pr-body.md#fixed"],
        }
        invalid = copy.deepcopy(self.readiness_example)
        invalid["semantic_review"]["findings"] = [finding, copy.deepcopy(finding)]
        self.assertEqual(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid)),
            [],
        )
        identity = invalid["review_identity"]
        self.assertIn(
            "publication finding refs must be unique and non-empty",
            GTT.task_publication_semantic_errors(
                invalid,
                reviewed_head=identity["reviewed_head"],
                review_ref=identity["review_ref"],
            ),
        )

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_empty_closed_finding_evidence_fails_schema_and_runtime(self) -> None:
        from jsonschema import Draft202012Validator

        invalid = copy.deepcopy(self.readiness_example)
        invalid["semantic_review"]["findings"] = [{
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
        identity = invalid["review_identity"]
        self.assertIn(
            "publication finding evidence and closure must be non-empty",
            GTT.task_publication_semantic_errors(
                invalid,
                reviewed_head=identity["reviewed_head"],
                review_ref=identity["review_ref"],
            ),
        )

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_ready_exit_rejects_any_failed_entry_precondition(self) -> None:
        from jsonschema import Draft202012Validator

        invalid = copy.deepcopy(self.readiness_example)
        invalid["deterministic_bindings"]["entry_preconditions"]["phase2_check"][
            "status"
        ] = "failed"
        self.assertTrue(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid))
        )

    def semantic_errors(self, payload: dict) -> list[str]:
        identity = payload["review_identity"]
        return GTT.task_publication_semantic_errors(
            payload,
            reviewed_head=identity["reviewed_head"],
            review_ref=identity["review_ref"],
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
            "evidence_refs": ["review.md"],
            "affected_artifacts": ["pr-body.md"],
            "route_class": route_class,
            "status": "open",
            "closure_evidence": ["Open route evidence is recorded."],
        }

    def return_payload(self) -> dict:
        payload = copy.deepcopy(self.readiness_example)
        payload["typed_exit"] = "return_to_task_work"
        payload["consumer"] = {
            "kind": "workflow",
            "id": "guru-task-publication-work-router",
        }
        payload["semantic_review"]["ai_review_gate"]["status"] = "return_to_task_work"
        payload["semantic_review"]["dimensions"][0]["status"] = "finding"
        payload["semantic_review"]["findings"] = [
            self.open_finding(
                finding_ref="PUB-WORK-001",
                dimension="diff_outcome_consistency",
                route_class="task_work",
            )
        ]
        payload["semantic_review"]["conclusions"]["issue_scope"]["status"] = "finding"
        return payload

    def blocked_payload(self) -> dict:
        payload = copy.deepcopy(self.readiness_example)
        payload["typed_exit"] = "blocked"
        payload["consumer"] = {
            "kind": "stop",
            "id": "task-publication-review-blocked",
        }
        payload["reason_code"] = "external-publication-dependency"
        payload["remediation"] = "Restore the external dependency and re-enter."
        payload["semantic_review"]["ai_review_gate"]["status"] = "blocked"
        payload["semantic_review"]["dimensions"][-1]["status"] = "blocked"
        payload["semantic_review"]["findings"] = [
            self.open_finding(
                finding_ref="PUB-BLOCK-001",
                dimension="artifact_binding_freshness",
                route_class="external_blocker",
            )
        ]
        payload["semantic_review"]["conclusions"]["safety_deployment"]["status"] = "blocked"
        return payload

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_ready_rejects_nonpassed_conclusion_in_schema_and_runtime(self) -> None:
        from jsonschema import Draft202012Validator

        invalid = copy.deepcopy(self.readiness_example)
        invalid["semantic_review"]["conclusions"]["issue_scope"]["status"] = "blocked"
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
        invalid["semantic_review"]["dimensions"][0]["status"] = "passed"
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
        invalid["typed_exit"] = "blocked"
        invalid["consumer"] = {
            "kind": "stop",
            "id": "task-publication-review-blocked",
        }
        invalid["reason_code"] = "external-publication-dependency"
        invalid["remediation"] = "Restore the external dependency and re-enter."
        invalid["semantic_review"]["ai_review_gate"]["status"] = "blocked"
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
        invalid_return["semantic_review"]["findings"][0][
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
        invalid_blocked["semantic_review"]["findings"][0][
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

    def test_stale_semantics_require_exact_replacement_fields(self) -> None:
        invalid = copy.deepcopy(self.readiness_example)
        invalid.update({
            "profile": "publication_review_stale",
            "review_intent": "stale_reentry_review",
        })
        identity = invalid["review_identity"]
        errors = GTT.task_publication_semantic_errors(
            invalid,
            reviewed_head=identity["reviewed_head"],
            review_ref=identity["review_ref"],
        )
        for field in ("stale_reason", "reentry_context", "supersedes_publication_ref"):
            self.assertIn(
                f"stale publication requires non-empty {field}",
                errors,
            )

    def test_both_modes_declare_exact_twelve_entry_preconditions(self) -> None:
        expected = [
            "runtime_dependency",
            "task_workspace",
            "task_identity",
            "branch_review_handoff",
            "planning_approval",
            "phase2_check",
            "issue_scope_ledger",
            "docs_ssot_reconciliation",
            "branch_review_evidence",
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


if __name__ == "__main__":
    unittest.main()
