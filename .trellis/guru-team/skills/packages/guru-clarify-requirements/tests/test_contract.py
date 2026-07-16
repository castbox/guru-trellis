from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class RequirementsClarificationPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.interface = json.loads((self.package / "interface.json").read_text(encoding="utf-8"))
        self.example = json.loads(
            (self.package / "examples/requirements-clarification.json").read_text(encoding="utf-8")
        )

    def test_identity_modes_semantic_stages_runtime_and_exits(self) -> None:
        self.assertEqual(self.interface["id"], "guru-clarify-requirements")
        self.assertEqual(self.interface["schema_version"], "1.2")
        self.assertEqual(self.interface["judgment_mode"], "semantic")
        workflow = self.interface["modes"]["workflow"]
        standalone = self.interface["modes"]["standalone"]
        self.assertEqual(workflow["entry_precondition_ids"], standalone["entry_precondition_ids"])
        self.assertEqual(
            workflow["entry_precondition_ids"],
            ["runtime_dependency", "review_target", "context_evidence", "source_authority", "invocation_freshness"],
        )
        self.assertEqual(
            self.interface["ordered_stages"],
            ["forward_behavior", "ai_review_gate", "conditional_human_confirmation", "recorder_validator", "typed_exit"],
        )
        self.assertEqual(
            {item["id"]: item["runtime_command"] for item in self.interface["validators"]},
            {
                "clarification_recorder": "record-requirements-clarification",
                "clarification_checker": "check-requirements-clarification",
            },
        )
        self.assertEqual(
            [item["id"] for item in self.interface["external_exits"]],
            ["clear", "needs_context", "refresh_context", "new_task", "blocked"],
        )
        self.assertEqual(
            [item["consumer"] for item in self.interface["external_exits"]],
            [
                {"kind": "workflow", "id": "guru-review-contract-wording"},
                {"kind": "skill", "id": "guru-discover-change-context"},
                {"kind": "skill", "id": "guru-sync-base"},
                {"kind": "workflow", "id": "guru-full-task-intake-chain"},
                {"kind": "stop", "id": "requirements-clarification-blocked"},
            ],
        )

    def test_contract_keeps_semantic_and_mutation_boundaries(self) -> None:
        skill = " ".join((self.package / "SKILL.md").read_text(encoding="utf-8").split())
        contract = " ".join((self.package / "references/contract.md").read_text(encoding="utf-8").split())
        for phrase in (
            "one highest-value question per round",
            "stdout-only",
            "no mutation executor",
            "not self-contained or portable",
        ):
            self.assertIn(phrase, skill)
        for phrase in (
            "repository-answerable question",
            "answer_status=partial",
            "proposal-digest-bound confirmation",
            "optional_mechanism_origin=true",
            "There is no mutation executor",
            "Success returns `refresh_context`",
            "guru-approve-task-plan",
            "guru-check-task",
            "guru-review-branch",
            "`blocked` if and only if",
        ):
            self.assertIn(phrase, contract)

    def test_wrappers_are_dispatcher_only_executable_and_have_no_mutation(self) -> None:
        wrappers = {
            "record-requirements-clarification.sh": "clarification_recorder",
            "check-requirements-clarification.sh": "clarification_checker",
        }
        for name, validator in wrappers.items():
            path = self.package / "scripts" / name
            content = path.read_text(encoding="utf-8")
            self.assertTrue(path.stat().st_mode & 0o100)
            self.assertIn("run-skill-command.sh", content)
            self.assertIn(f"--validator {validator}", content)
            self.assertNotIn("guru_team_trellis.py", content)
            self.assertNotIn("gh issue", content)
            self.assertNotIn("issue create", content)

    def test_package_only_copy_fails_with_full_preset_remediation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "guru-clarify-requirements"
            shutil.copytree(self.package, copied)
            for name in (
                "record-requirements-clarification.sh",
                "check-requirements-clarification.sh",
            ):
                result = subprocess.run(
                    [str(copied / "scripts" / name), "--help"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(result.returncode, 2, result)
                self.assertIn("not self-contained or portable", result.stderr)
                self.assertIn("Install or upgrade the complete Guru Team preset", result.stderr)

    @unittest.skipIf(importlib.util.find_spec("jsonschema") is None, "jsonschema unavailable")
    def test_closed_schema_and_core_invariants(self) -> None:
        from jsonschema import Draft202012Validator

        schema = json.loads(
            (self.package / "schemas/requirements-clarification.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
        self.assertEqual(list(validator.iter_errors(self.example)), [])

        unknown = copy.deepcopy(self.example)
        unknown["unexpected"] = True
        self.assertNotEqual(list(validator.iter_errors(unknown)), [])

        partial = copy.deepcopy(self.example)
        partial["clarification_rounds"] = [{
            "round_id": "round_1", "question_id": "intent", "atomic_group_id": None,
            "atomic_group_reason": None, "category": "product_intent", "question": "Which behavior?",
            "answer_summary": "Only part was answered.", "answer_status": "partial",
            "affected_contracts": ["requirements"], "opened_question_ids": ["intent"],
            "closed_question_ids": ["intent"],
        }]
        self.assertNotEqual(list(validator.iter_errors(partial)), [])

        new_task = copy.deepcopy(self.example)
        new_task["typed_exit"] = "new_task"
        new_task["consumer"] = {"kind": "workflow", "id": "guru-full-task-intake-chain"}
        new_task["source_actions"] = [{
            "action_id": "new_issue", "kind": "new_issue_draft",
            "target": {"repo": "example/guru-extension"},
            "payload": {"title": "Independent delivery", "body": "Reviewed scope"},
            "preimage_sha256": None, "payload_sha256": "0" * 64,
            "action_digest": "0" * 64, "status": "draft_ready",
            "mutation_evidence": None,
        }]
        self.assertEqual(list(validator.iter_errors(new_task)), [])
        for nested_field in ("target", "payload"):
            with self.subTest(nested_field=nested_field):
                unknown_nested = copy.deepcopy(new_task)
                unknown_nested["source_actions"][0][nested_field]["unexpected"] = True
                self.assertNotEqual(list(validator.iter_errors(unknown_nested)), [])

        github_action = copy.deepcopy(self.example)
        github_action["typed_exit"] = "refresh_context"
        github_action["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
        github_action["source_actions"] = [{
            "action_id": "comment", "kind": "issue_comment",
            "target": {"repo": "example/guru-extension", "issue_number": 7},
            "payload": {"body": "Confirmed clarification."},
            "preimage_sha256": "1" * 64, "payload_sha256": "0" * 64,
            "action_digest": "0" * 64, "status": "executed",
            "mutation_evidence": {"source": "ai-reviewed-gh", "unexpected": True},
        }]
        self.assertNotEqual(list(validator.iter_errors(github_action)), [])
        github_action["source_actions"][0]["mutation_evidence"].pop("unexpected")
        self.assertEqual(list(validator.iter_errors(github_action)), [])

        blocked = copy.deepcopy(self.example)
        blocked["typed_exit"] = "blocked"
        blocked["consumer"] = {"kind": "stop", "id": "requirements-clarification-blocked"}
        blocked["error"] = {"codes": ["semantic_gate_blocked"], "summary": "The gate is blocked."}
        self.assertNotEqual(list(validator.iter_errors(blocked)), [])
        blocked["ai_review_gate"]["status"] = "blocked"
        self.assertEqual(list(validator.iter_errors(blocked)), [])

        active_missing = copy.deepcopy(self.example)
        active_missing["invocation_context"] = {
            "kind": "active_task_scope_change", "caller": "active task", "task_locator": ".trellis/tasks/example"
        }
        self.assertNotEqual(list(validator.iter_errors(active_missing)), [])

        serialized = json.dumps(self.example, ensure_ascii=False)
        self.assertNotIn("/Users/", serialized)
        self.assertNotIn(".trellis/workspace/", serialized)
        self.assertNotIn(".trellis/.runtime/", serialized)

    @unittest.skipIf(importlib.util.find_spec("jsonschema") is None, "jsonschema unavailable")
    def test_action_bodies_allow_multiline_markdown_and_reject_controls(self) -> None:
        from jsonschema import Draft202012Validator

        schema = json.loads(
            (self.package / "schemas/requirements-clarification.schema.json").read_text(encoding="utf-8")
        )
        validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
        markdown = "# Clarification\n\n- first\tvalue\r\n- second"

        def action_payload(kind: str, body: str) -> dict[str, object]:
            payload = copy.deepcopy(self.example)
            if kind == "new_issue_draft":
                payload["typed_exit"] = "new_task"
                payload["consumer"] = {"kind": "workflow", "id": "guru-full-task-intake-chain"}
                target = {"repo": "example/guru-extension"}
                action_body = {"title": "Independent delivery", "body": body}
                status = "draft_ready"
                preimage = None
            else:
                payload["typed_exit"] = "refresh_context"
                payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
                target = {"repo": "example/guru-extension", "issue_number": 7}
                action_body = {"body": body}
                status = "pending"
                preimage = "1" * 64
            payload["source_actions"] = [{
                "action_id": "source_action", "kind": kind, "target": target,
                "payload": action_body, "preimage_sha256": preimage,
                "payload_sha256": "0" * 64, "action_digest": "0" * 64,
                "status": status, "mutation_evidence": None,
            }]
            return payload

        for kind in ("issue_comment", "issue_body_edit", "new_issue_draft"):
            with self.subTest(kind=kind, value="multiline_markdown"):
                self.assertEqual(list(validator.iter_errors(action_payload(kind, markdown))), [])
            for label, control in (("nul", "\x00"), ("other_c0", "\x01"), ("del", "\x7f")):
                with self.subTest(kind=kind, value=label):
                    self.assertNotEqual(
                        list(validator.iter_errors(action_payload(kind, markdown + control))),
                        [],
                    )


if __name__ == "__main__":
    unittest.main()
