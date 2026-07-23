from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]


class ReviewBranchContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        cls.input_schema = json.loads(
            (PACKAGE / "schemas/public-branch-review-input.schema.json").read_text(encoding="utf-8")
        )
        cls.input_example = json.loads(
            (PACKAGE / "examples/public-branch-review-input.json").read_text(encoding="utf-8")
        )

    def test_public_input_is_one_closed_profile(self) -> None:
        profiles = self.interface["public_contracts"]["input"]["profiles"]
        self.assertEqual([item["id"] for item in profiles], ["branch_review"])
        self.assertEqual(
            self.input_schema["required"],
            ["profile", "mode", "task_ref", "base_ref", "committed_head", "review_intent"],
        )
        self.assertFalse(self.input_schema["additionalProperties"])
        self.assertEqual(
            self.input_schema["properties"]["review_intent"]["enum"],
            ["initial_review", "finding_fix_review", "fresh_final_review"],
        )

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "jsonschema is optional")
    def test_public_examples_and_outputs_validate(self) -> None:
        from jsonschema import Draft202012Validator

        Draft202012Validator.check_schema(self.input_schema)
        self.assertEqual(list(Draft202012Validator(self.input_schema).iter_errors(self.input_example)), [])
        for output in self.interface["public_contracts"]["outputs"]:
            schema = json.loads((PACKAGE / output["schema"]["path"]).read_text(encoding="utf-8"))
            example = json.loads((PACKAGE / output["example"]["path"]).read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            self.assertEqual(list(Draft202012Validator(schema).iter_errors(example)), [])
        invalid = copy.deepcopy(self.input_example)
        invalid["planning_approval"] = {}
        self.assertTrue(list(Draft202012Validator(self.input_schema).iter_errors(invalid)))

    def test_thirteen_preconditions_and_semantic_profile(self) -> None:
        expected = [
            "runtime_dependency", "workspace_boundary", "task_identity", "commit_handoff",
            "planning_approval", "phase2_check", "issue_scope_ledger", "docs_ssot_outcome",
            "review_range", "working_tree", "reviewer_assignment", "review_evidence",
            "invocation_freshness",
        ]
        self.assertEqual([item["id"] for item in self.interface["entry_preconditions"]], expected)
        self.assertEqual(self.interface["modes"]["workflow"]["entry_precondition_ids"], expected)
        self.assertEqual(self.interface["modes"]["standalone"]["entry_precondition_ids"], expected)
        self.assertEqual(self.interface["judgment_mode"], "semantic")

    def test_four_minimal_exits_have_unique_consumers(self) -> None:
        exits = self.interface["external_exits"]
        self.assertEqual(
            [item["id"] for item in exits],
            ["passed", "implementation_required", "scope_confirmation_required", "blocked"],
        )
        self.assertEqual(len({(item["consumer"]["kind"], item["consumer"]["id"]) for item in exits}), 4)
        blocked = json.loads((PACKAGE / "schemas/public-blocked-output.schema.json").read_text())
        self.assertEqual(set(blocked["properties"]), {"exit_id"})

    def test_planned_bridge_does_not_claim_target_contract(self) -> None:
        consumer = next(
            item for item in self.interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "publication_seed_input"
        )
        self.assertEqual(
            consumer["contract"],
            {
                "kind": "planned_skill_input_seed",
                "seed_fields": ["task_ref", "reviewed_head", "review_ref"],
            },
        )
        self.assertEqual(consumer["consumer"]["id"], "guru-review-task-publication")

    def test_contract_owns_qualification_and_preserves_upstream(self) -> None:
        text = (
            (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
            + (PACKAGE / "references/contract.md").read_text(encoding="utf-8")
        )
        for phrase in (
            "qualify every candidate before assigning severity",
            "unconfirmed_nonstandard_proposal",
            "official unchanged check/review agent",
            "fresh final reviewer",
            "expected_exit",
        ):
            self.assertIn(phrase, text)
        for forbidden in (
            "trellis/presets/guru-team/overlays/.trellis/agents/check.md",
            "script decides severity",
        ):
            self.assertNotIn(forbidden, text)

    def test_wrappers_are_dispatcher_only(self) -> None:
        for name, validator in (
            ("invoke.sh", "public_invocation"),
            ("review-branch.sh", "review_gate_recorder"),
            ("check-review-gate.sh", "review_gate_checker"),
        ):
            path = PACKAGE / "scripts" / name
            self.assertTrue(path.stat().st_mode & 0o111)
            text = path.read_text(encoding="utf-8")
            self.assertIn("run-skill-command.sh", text)
            self.assertIn(f"--validator {validator}", text)
            self.assertNotIn("guru_team_trellis.py", text)

    def test_package_only_copy_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "guru-review-branch"
            subprocess.run(["cp", "-R", str(PACKAGE), str(copied)], check=True)
            result = subprocess.run(
                [str(copied / "scripts/invoke.sh"), "--help"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                env={**os.environ, "GURU_TEAM_DISPATCHER": ""},
            )
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
