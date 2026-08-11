from __future__ import annotations

import json
import unittest
from pathlib import Path

import jsonschema


PACKAGE = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((PACKAGE / relative).read_text(encoding="utf-8"))


class FinalizeTaskContractTests(unittest.TestCase):
    def test_current_contract_has_no_verifier_edge_or_reentry(self) -> None:
        interface = load("interface.json")
        contracts = interface["public_contracts"]
        self.assertEqual(
            contracts["input"]["aggregate_schema"],
            {
                "schema_id": "guru-finalize-task-input-aggregate-6.0",
                "path": "schemas/public-input-6.0.schema.json",
            },
        )
        self.assertEqual(
            [item["id"] for item in contracts["input"]["profiles"]],
            ["publication_ready", "same_plan_resume", "reprepare_preview", "standalone_finalization"],
        )
        self.assertEqual(
            [item["exit_id"] for item in contracts["outputs"]],
            ["publication_review_stale", "resume_finalization", "reprepare_required", "ready_for_merge", "blocked"],
        )
        serialized = json.dumps(contracts, sort_keys=True)
        for retired in (
            "verification_required",
            "verification_verified",
            "standalone_verification_not_required",
            "guru-verify-extension-installation",
        ):
            self.assertNotIn(retired, serialized)

    def test_current_gate_and_transaction_remove_verify(self) -> None:
        gate = load("schemas/task-finalization-gate.schema.json")
        transaction = load("schemas/finalization-transaction.schema.json")
        self.assertEqual(gate["properties"]["schema_version"]["const"], "4.0")
        exits = gate["properties"]["route"]["properties"]["typed_exit"]["enum"]
        self.assertNotIn("verification_required", exits)
        self.assertEqual(transaction["properties"]["schema_version"]["const"], "2.0")
        self.assertNotIn("verify", transaction["properties"]["next_transition"]["enum"])
        self.assertNotIn("verification_ref", transaction["properties"])

    def test_current_input_examples_validate(self) -> None:
        interface = load("interface.json")
        for profile in interface["public_contracts"]["input"]["profiles"]:
            schema = load(profile["schema"]["path"])
            example = load(profile["example"]["path"])
            jsonschema.Draft202012Validator(schema).validate(example)


if __name__ == "__main__":
    unittest.main()
