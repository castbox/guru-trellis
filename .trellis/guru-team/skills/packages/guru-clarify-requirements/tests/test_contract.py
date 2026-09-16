from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class RequirementsClarificationPackageContractTests(unittest.TestCase):
    def test_current_ai_owns_unexecuted_review_without_external_handoff(self) -> None:
        package = Path(__file__).resolve().parents[1]
        for path in ("SKILL.md", "references/contract.md"):
            with self.subTest(path=path):
                text = " ".join((package / path).read_text(encoding="utf-8").split())
                self.assertIn("The current executing AI is this Skill's semantic owner", text)
                self.assertIn("`owner_not_yet_executed`", text)
                self.assertIn("not a typed", text)
                self.assertIn("agent ID", text)
                self.assertIn("subagent evidence", text)
                self.assertIn("pre-existing owner result", text)
        contract = " ".join((package / "references/contract.md").read_text(encoding="utf-8").split())
        self.assertIn("ask exactly one highest-value user question per round", contract)
        self.assertIn("Pass only actual public invoke stdout", contract)
        self.assertIn("never read or reconstruct producer-private results", contract)
        self.assertIn("declared blocker or re-entry route when a real gap remains", contract)
        interface = json.loads((package / "interface.json").read_text(encoding="utf-8"))
        self.assertEqual(interface["judgment_mode"], "semantic")
        self.assertNotIn("owner_not_yet_executed", [row["id"] for row in interface["external_exits"]])

    def command(self, script, payload, *args):
        return subprocess.run(
            [str(self.package / "scripts" / script), "--json", *args],
            input=json.dumps(payload), text=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False,
        )

    def authoring(self, owner):
        value = copy.deepcopy(owner)
        value.pop("content_identity", None)
        value["review_target"].pop("facts_sha256", None)
        if value["target_disposition"] is not None:
            value["target_disposition"].pop("disposition_digest", None)
        for proposal in value["scope_proposals"]:
            proposal.pop("proposal_digest", None)
        for action in value["source_actions"]:
            action.pop("payload_sha256", None)
            action.pop("action_digest", None)
        return value

    def record_owner(self, owner):
        result = self.command("record-requirements-clarification.sh", self.authoring(owner),
                              "--mode", owner["mode"], "--input", "-")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.interface = json.loads((self.package / "interface.json").read_text(encoding="utf-8"))
        self.example = json.loads(
            (self.package / "examples/requirements-clarification.json").read_text(encoding="utf-8")
        )

    def test_identity_modes_semantic_stages_runtime_and_exits(self) -> None:
        self.assertEqual(self.interface["id"], "guru-clarify-requirements")
        self.assertEqual(self.interface["schema_version"], "1.4")
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
                "public_invocation": "invoke-guru-clarify-requirements",
            },
        )
        self.assertEqual(
            [item["id"] for item in self.interface["external_exits"]],
            ["clear", "needs_context", "refresh_context", "retarget_context", "new_task", "blocked"],
        )
        self.assertEqual(
            [item["consumer"] for item in self.interface["external_exits"]],
            [
                {"kind": "workflow", "id": "guru-requirements-clear-router"},
                {"kind": "skill", "id": "guru-discover-change-context"},
                {"kind": "skill", "id": "guru-sync-base"},
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
            "dedicated dialogue-local choice",
            "optional_mechanism_origin=true",
            "mechanism_removed",
            "current transient `context_evidence` digest",
            "update time are reread directly",
            "writes no authorization fields",
            "does not require a second Discovery result",
            "There is no mutation executor",
            "Success returns `refresh_context`",
            "compact owner-result `decision_trail`",
            "remote authority locator and content checksum",
            "validates that shape before calculating values",
            "Supplied derived values are consistency assertions",
            "`blocked` if and only if",
        ):
            self.assertIn(phrase, contract)
        self.assertNotIn("dialogue-local authorization", contract)
        self.assertNotIn("user_confirmation", contract)
        self.assertNotIn("context_before_task_update_sha256", contract)
        self.assertNotIn("preserve the decision trail", contract)
        for filename in ("record-requirements-clarification.sh", "check-requirements-clarification.sh", "invoke.sh"):
            path = f".trellis/guru-team/skills/packages/guru-clarify-requirements/scripts/{filename}"
            self.assertIn(path, skill)
            self.assertIn(path, contract)
            self.assertTrue((self.package / "scripts" / filename).is_file())

    def test_wrappers_are_package_local_launcher_only_and_have_no_mutation(self) -> None:
        wrappers = {
            "record-requirements-clarification.sh": "clarification_recorder",
            "check-requirements-clarification.sh": "clarification_checker",
        }
        for name, validator in wrappers.items():
            path = self.package / "scripts" / name
            content = path.read_text(encoding="utf-8")
            self.assertTrue(path.stat().st_mode & 0o100)
            self.assertIn("runtime/launch.sh", content)
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
            "authority_impact": "load_bearing", "authority_action_ids": [],
            "affected_contracts": ["requirements"], "opened_question_ids": ["intent"],
            "closed_question_ids": ["intent"],
        }]
        self.assertNotEqual(list(validator.iter_errors(partial)), [])

        answered_without_evidence = copy.deepcopy(self.example)
        answered_without_evidence["repository_answerable_questions"][0]["evidence_refs"] = []
        self.assertNotEqual(list(validator.iter_errors(answered_without_evidence)), [])

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

        refresh_without_disposition = copy.deepcopy(github_action)
        refresh_without_disposition["target_disposition"] = None
        self.assertNotEqual(
            list(validator.iter_errors(refresh_without_disposition)),
            [],
        )

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

    def test_normal_scenario_scope_confirmation_is_closed_candidate_only_input(self) -> None:
        from jsonschema import Draft202012Validator

        schema = json.loads(
            (self.package / "schemas/public-normal-scenario-scope-confirmation-input.schema.json").read_text(
                encoding="utf-8"
            )
        )
        example = json.loads(
            (self.package / "examples/public-normal-scenario-scope-confirmation-input.json").read_text(
                encoding="utf-8"
            )
        )
        validator = Draft202012Validator(schema)
        self.assertEqual(list(validator.iter_errors(example)), [])
        profiles = {
            item["id"]: item
            for item in self.interface["public_contracts"]["input"]["profiles"]
        }
        self.assertIn("normal_scenario_scope_confirmation", profiles)
        self.assertEqual(
            profiles["normal_scenario_scope_confirmation"]["schema"]["path"],
            "schemas/public-normal-scenario-scope-confirmation-input.schema.json",
        )
        for field, value in (
            ("decisions", []),
            ("reasons", ["caller-classified"]),
            ("severity", "P0"),
            ("authorization", "confirmed"),
            ("result_locator", ".trellis/.runtime/qualification.json"),
        ):
            with self.subTest(field=field):
                invalid = copy.deepcopy(example)
                invalid[field] = value
                self.assertNotEqual(list(validator.iter_errors(invalid)), [])
        duplicate = copy.deepcopy(example)
        duplicate["candidate_refs"].append(duplicate["candidate_refs"][0])
        self.assertNotEqual(list(validator.iter_errors(duplicate)), [])
        empty = copy.deepcopy(example)
        empty["candidate_refs"] = []
        self.assertNotEqual(list(validator.iter_errors(empty)), [])

    def test_package_local_record_check_and_closed_json_error(self) -> None:
        source = self.package / "examples/requirements-clarification.json"
        record = subprocess.run(
            [str(self.package / "scripts/record-requirements-clarification.sh"), "--json", "--mode", "standalone", "--input", str(source)],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(record.returncode, 0, record)
        owner = json.loads(record.stdout)
        check = subprocess.run(
            [str(self.package / "scripts/check-requirements-clarification.sh"), "--json", "--input", "-", "--expected-result-sha256", owner["content_identity"]["result_sha256"]],
            input=record.stdout, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(check.returncode, 0, check)
        self.assertEqual(json.loads(check.stdout)["typed_exit"], owner["typed_exit"])
        self.assertNotIn("guru_team_trellis", record.stdout + record.stderr + check.stdout + check.stderr)

        invalid = subprocess.run(
            [str(self.package / "scripts/check-requirements-clarification.sh"), "--json", "--input", "{"],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertNotEqual(invalid.returncode, 0)
        self.assertEqual(json.loads(invalid.stdout)["code"], "invalid_json")
        self.assertNotIn("Traceback", invalid.stdout + invalid.stderr)

    def test_current_issue_blocked_conflict_retains_target_through_public_wrapper(self) -> None:
        # Shape/transport evidence only; native semantic fidelity is reviewed separately.
        for path in ("SKILL.md", "references/contract.md"):
            text = " ".join((self.package / path).read_text(encoding="utf-8").split())
            self.assertIn("Record only clarification rounds and answers that actually occurred", text)
            self.assertIn("unasked, or unanswered choices are not refused, deferred, or answered", text)
        contract = " ".join((self.package / "references/contract.md").read_text(encoding="utf-8").split())
        self.assertIn("`answer_status=refused` requires an actual user refusal", contract)
        self.assertIn("`clarification_rounds=[]`", contract)
        self.assertIn("`target_disposition=null` is not a blocked shortcut", contract)
        self.assertIn("Only successful public invoke stdout is the final DTO", contract)
        self.assertIn("Never hand-write a blocked DTO", contract)
        public = json.loads((self.package / "examples/public-initial-change-request-input-2.0.json").read_text())
        public["source_exit"] = "context_ready"
        snapshot = copy.deepcopy(public["duplicate_snapshot"])
        owner = copy.deepcopy(self.example)
        owner["mode"] = public["mode"]
        owner["invocation_context"]["kind"] = "initial_issue"
        owner["review_target"].update(
            kind="issue", issue_number=145, url=public["target_locator"], state="open",
            updated_at=snapshot["checked_at"], body_sha256=snapshot["authority_content_sha256"],
        )
        owner["target_disposition"].update(
            disposition="keep_current_open_issue",
            duplicate_query=snapshot["query"], duplicate_checked_at=snapshot["checked_at"],
            duplicate_facts_sha256=snapshot["facts_sha256"],
            decision_summary="The known open issue remains the target; the empty duplicate search does not resolve its scope conflict.",
        )
        reason = "The source requires incompatible delivery scopes; no priority choice or user answer is available."
        owner.update(
            typed_exit="blocked",
            consumer={"kind": "stop", "id": "requirements-clarification-blocked"},
            reason=reason,
            error={"codes": ["semantic_gate_blocked"], "summary": reason},
            confirmed_facts=[{
                "fact_id": "scope_conflict", "summary": reason,
                "evidence_refs": ["review_target.body_sha256"],
                "affected_contracts": ["requirements"],
            }],
            repository_answerable_questions=[],
            clarification_rounds=[],
            open_questions=[],
        )
        owner["ai_review_gate"].update(
            status="blocked", summary=reason, load_bearing_conclusions=[reason],
            findings=[{
                "finding_id": "scope_conflict", "severity": "P2", "status": "open",
                "summary": reason, "evidence_refs": ["review_target.body_sha256"],
            }],
        )
        recorded = self.record_owner(owner)
        self.assertEqual(recorded["clarification_rounds"], [])
        self.assertEqual(recorded["open_questions"], [])
        self.assertEqual(recorded["reason"], reason)
        self.assertEqual(recorded["ai_review_gate"], owner["ai_review_gate"])
        checked = self.command("check-requirements-clarification.sh", recorded, "--input", "-")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertEqual(json.loads(checked.stdout)["typed_exit"], "blocked")
        self.assertEqual(recorded["target_disposition"]["disposition"], "keep_current_open_issue")
        self.assertEqual(recorded["target_disposition"]["duplicate_facts_sha256"], snapshot["facts_sha256"])
        transition = json.loads((self.package / "examples/public-clear-output-2.0.json").read_text())["transition"]
        for field in ("clarity_result_sha256", "target_content_sha256", "clarity", "target_disposition"):
            transition.pop(field)
        transition.update(stage="context_current", target_locator=public["target_locator"],
                          authority_content_sha256=snapshot["authority_content_sha256"])
        envelope = {"schema_version": "1.0", "public_input": public, "transition": transition,
                    "owner_context": {}, "owner_result": recorded}
        invoked = self.command("invoke.sh", envelope, "--invocation", "-")
        self.assertEqual(invoked.returncode, 0, invoked.stdout + invoked.stderr)
        self.assertEqual(json.loads(invoked.stdout), {"exit_id": "blocked"})
        self.assertEqual(public["duplicate_snapshot"], snapshot)

    def test_public_invoke_validates_checked_semantic_owner_output(self) -> None:
        from jsonschema import Draft202012Validator

        owner = json.loads((self.package / "examples/requirements-clarification.json").read_text())
        typed = json.loads((self.package / "examples/public-clear-output-2.0.json").read_text())
        transition = copy.deepcopy(typed["transition"])
        transition["stage"] = "context_current"
        transition["transition_id"] = "context_current:222222222222222222222222"
        transition["mode"] = "standalone"
        transition["target_locator"] = "#145"
        for field in ("clarity_result_sha256", "target_content_sha256", "clarity", "target_disposition"):
            transition.pop(field, None)
        public_input = {
            "profile": "standalone_review",
            "source_exit": "start",
            "mode": "standalone",
            "target_locator": "#145",
            "continuation_id": "stage0-current",
        }
        invocation = {
            "schema_version": "1.0",
            "public_input": public_input,
            "transition": transition,
            "owner_context": {},
            "owner_result": owner,
        }
        schema = json.loads(
            (self.package.parents[1] / "consumers/workflow/stage0/invocations/semantic-owner.schema.json").read_text()
        )
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(invocation)), [])
        result = subprocess.run(
            [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
            input=json.dumps(invocation), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(result.returncode, 0, result)
        output = json.loads(result.stdout)
        self.assertEqual(output["exit_id"], "clear")
        self.assertEqual(output["resume_target"], owner["invocation_context"]["resume_target"])
        self.assertEqual(output["continuation_id"], public_input["continuation_id"])
        self.assertEqual(output["transition"]["stage"], "clarity_current")
        self.assertEqual(output["transition"]["clarity_result_sha256"], owner["content_identity"]["result_sha256"])
        self.assertNotIn("typed_output", output)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

        extra = copy.deepcopy(invocation)
        extra["typed_output"] = typed
        rejected = subprocess.run(
            [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
            input=json.dumps(extra), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("schema_mismatch", rejected.stdout)

        stale = copy.deepcopy(invocation)
        stale["public_input"]["target_locator"] = "#999"
        rejected = subprocess.run(
            [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
            input=json.dumps(stale), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("stale_identity", rejected.stdout)

        missing = copy.deepcopy(invocation)
        del missing["owner_context"]
        rejected = subprocess.run(
            [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
            input=json.dumps(missing), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("schema_mismatch", rejected.stdout)

    def test_public_invoke_projects_active_task_clear_null_disposition_as_retained(self) -> None:
        from jsonschema import Draft202012Validator

        owner = json.loads((self.package / "examples/requirements-clarification.json").read_text())
        owner["mode"] = "workflow"
        owner["invocation_context"] = {
            "kind": "active_task_scope_change",
            "caller": "active task scope clarification",
            "task_locator": ".trellis/tasks/current",
            "resume_target": "guru-resume-branch-review",
        }
        owner["target_disposition"] = None
        owner["scope_proposals"] = [{
            "proposal_id": "active_scope_update",
            "scenario": "Keep the current task and accept the clarified scope.",
            "trigger_evidence": ["active-task:current"],
            "proposed_contracts": ["task scope"],
            "cost": "Narrow task-local planning refresh.",
            "alternatives": ["Return to the prior task scope."],
            "consequence_if_omitted": "The accepted clarification is not reflected in the active task.",
            "origin_requirement_status": "necessary_correctness",
            "optional_mechanism_origin": False,
            "decision": "accepted_current",
            "proposal_digest": "9" * 64,
        }]
        owner["active_task_evidence"] = {
            "task_locator": ".trellis/tasks/current",
            "github_authority_facts_sha256": "8" * 64,
            "planning_documents": [
                {"path": ".trellis/tasks/current/prd.md", "content_sha256": "6" * 64},
                {"path": ".trellis/tasks/current/design.md", "content_sha256": "5" * 64},
                {"path": ".trellis/tasks/current/implement.md", "content_sha256": "4" * 64},
            ],
            "decision_trail": None,
            "reentry_owners": ["guru-approve-task-plan", "guru-check-task", "guru-review-branch"],
        }
        owner = self.record_owner(owner)
        typed = json.loads((self.package / "examples/public-clear-output-2.0.json").read_text())
        transition = copy.deepcopy(typed["transition"])
        transition["stage"] = "context_current"
        transition["transition_id"] = "context_current:222222222222222222222222"
        transition["mode"] = "workflow"
        transition["target_locator"] = "#145"
        for field in ("clarity_result_sha256", "target_content_sha256", "clarity", "target_disposition"):
            transition.pop(field, None)
        public_input = json.loads((self.package / "examples/public-active-task-scope-change-input.json").read_text())
        invocation = {
            "schema_version": "1.0",
            "public_input": public_input,
            "transition": transition,
            "owner_context": {},
            "owner_result": owner,
        }
        schema = json.loads(
            (self.package.parents[1] / "consumers/workflow/stage0/invocations/semantic-owner.schema.json").read_text()
        )
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(invocation)), [])
        result = subprocess.run(
            [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
            input=json.dumps(invocation), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(result.returncode, 0, result)
        output = json.loads(result.stdout)
        self.assertEqual(output["exit_id"], "clear")
        self.assertEqual(output["target_disposition"], "retained")
        self.assertEqual(
            output["transition"]["target_disposition"],
            {
                "disposition_sha256": owner["content_identity"]["disposition_sha256"],
                "duplicate_facts_sha256": owner["content_identity"]["disposition_sha256"],
            },
        )
        self.assertNotIn("Traceback", result.stdout + result.stderr)

        standalone = copy.deepcopy(invocation)
        standalone["public_input"] = {
            "profile": "standalone_review",
            "source_exit": "start",
            "mode": "standalone",
            "target_locator": "#145",
            "continuation_id": "stage0-current",
        }
        standalone["transition"]["mode"] = "standalone"
        standalone["owner_result"]["mode"] = "standalone"
        standalone["owner_result"]["invocation_context"] = {
            "kind": "standalone_review",
            "caller": "standalone requirements review",
            "task_locator": None,
            "resume_target": "guru-standalone-caller",
        }
        standalone["owner_result"]["scope_proposals"] = []
        standalone["owner_result"]["active_task_evidence"] = None
        rejected = subprocess.run(
            [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
            input=json.dumps(standalone), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertEqual(json.loads(rejected.stdout)["field_path"], "input.target_disposition")
        self.assertNotIn("Traceback", rejected.stdout + rejected.stderr)

    def test_needs_context_rejects_missing_or_malformed_base_as_json_command_error(self) -> None:
        owner = json.loads((self.package / "examples/requirements-clarification.json").read_text())
        owner["typed_exit"] = "needs_context"
        owner["consumer"] = {"kind": "skill", "id": "guru-discover-change-context"}
        owner["context_evidence"] = {"status": "missing", "evidence_refs": ["current-session:missing"], "missing_reason": "Base context is unavailable."}
        owner["target_disposition"] = None
        owner = self.record_owner(owner)
        public_input = {
            "profile": "standalone_review",
            "source_exit": "start",
            "mode": "standalone",
            "target_locator": "#145",
            "continuation_id": "stage0-current",
        }
        base = {
            "source": "explicit",
            "selected_base": "main",
            "remote": "origin",
            "ordered_candidates": ["main"],
            "decision_head": "1" * 40,
            "local_base_head": "1" * 40,
            "remote_base_head": "1" * 40,
            "post_sync_resolution_sha256": "1" * 64,
        }

        def invoke(value: dict) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
                input=json.dumps(value), text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )

        for label, malformed_base in (
            ("missing_required_field", {key: value for key, value in base.items() if key != "selected_base"}),
            ("wrong_required_field_type", {**base, "post_sync_resolution_sha256": 7}),
            ("source_array", {**base, "source": ["explicit"]}),
            ("source_object", {**base, "source": {"kind": "explicit"}}),
        ):
            with self.subTest(label=label):
                invocation = {
                    "schema_version": "1.0",
                    "public_input": public_input,
                    "transition": {
                        "stage": "context_current",
                        "mode": "standalone",
                        "repo_locator": ".",
                        "base": malformed_base,
                    },
                    "owner_context": {},
                    "owner_result": owner,
                }
                rejected = invoke(invocation)
                self.assertNotEqual(rejected.returncode, 0)
                error = json.loads(rejected.stdout)
                self.assertEqual(error["code"], "stale_identity")
                self.assertEqual(error["field_path"], "transition.base")
                self.assertNotIn("Traceback", rejected.stdout + rejected.stderr)


    def test_minimal_authoring_and_full_result_are_identical(self):
        owner = self.record_owner(self.example)
        self.assertEqual(owner, self.example)
        full = self.command("record-requirements-clarification.sh", owner,
                            "--mode", "standalone", "--input", "-")
        self.assertEqual(full.returncode, 0, full.stdout)
        self.assertEqual(json.loads(full.stdout), owner)

    def test_authoring_requires_semantic_shape_and_binds_proposals(self):
        proposal = {
            "proposal_id": "current_scope", "scenario": "Keep current scope",
            "trigger_evidence": ["current:scope"], "proposed_contracts": ["requirements"],
            "cost": "Small", "alternatives": ["Defer"],
            "consequence_if_omitted": "Scope is unclear",
            "origin_requirement_status": "explicit", "optional_mechanism_origin": False,
            "decision": "accepted_current",
        }
        source = self.authoring(self.example)
        source["scope_proposals"] = [proposal]
        variants = []
        for field in ("ai_review_gate", "typed_exit", "consumer", "source_actions", "review_target"):
            value = copy.deepcopy(source)
            del value[field]
            variants.append((field, value))
        for field in ("decision", "scenario"):
            value = copy.deepcopy(source)
            del value["scope_proposals"][0][field]
            variants.append((field, value))
        for field, malformed in (("source_actions", None), ("scope_proposals", {}),
                                 ("review_target", []), ("ai_review_gate", {"status": "passed"}),
                                 ("content_identity", {})):
            variants.append((field, {**source, field: malformed}))
        for label, value in variants:
            with self.subTest(label=label):
                result = self.command("record-requirements-clarification.sh", value,
                                      "--mode", "standalone", "--input", "-")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(json.loads(result.stdout)["code"], "schema_mismatch")
                self.assertNotIn("Traceback", result.stdout + result.stderr)
        recorded = self.record_owner(source)
        unsigned = {key: value for key, value in proposal.items() if key != "proposal_digest"}
        encoded = json.dumps(unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
        self.assertEqual(recorded["scope_proposals"][0]["proposal_digest"],
                         hashlib.sha256(encoded.encode()).hexdigest())
        recorded["scope_proposals"][0]["scenario"] = "Updated scope scenario"
        stale = self.command("check-requirements-clarification.sh", recorded, "--input", "-")
        self.assertNotEqual(stale.returncode, 0)
        self.assertEqual(json.loads(stale.stdout)["field_path"], "input.scope_proposals.0.proposal_digest")

    def test_changed_content_rejects_old_bindings_in_record_and_check(self):
        owner = copy.deepcopy(self.example)
        source_body = "Reviewed requirement body\n\nCurrent acceptance criteria."
        updated_source_body = source_body + "\nAdditional accepted criterion."
        owner["review_target"]["body_sha256"] = hashlib.sha256(source_body.encode()).hexdigest()
        owner["typed_exit"] = "new_task"
        owner["consumer"] = {"kind": "workflow", "id": "guru-full-task-intake-chain"}
        owner["source_actions"] = [{
            "action_id": "draft", "kind": "new_issue_draft",
            "target": {"repo": "example/guru-extension"},
            "payload": {"title": "Current title", "body": "Reviewed body\n\nSecond line"},
            "preimage_sha256": None, "status": "draft_ready", "mutation_evidence": None,
        }]
        owner = self.record_owner(owner)
        canonical = lambda value: hashlib.sha256(json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()).hexdigest()
        action = owner["source_actions"][0]
        self.assertEqual(action["payload_sha256"], canonical(action["payload"]))
        self.assertEqual(action["action_digest"], canonical({key: action[key] for key in (
            "action_id", "kind", "target", "payload", "preimage_sha256", "payload_sha256"
        )}))
        self.assertEqual(owner["content_identity"]["result_sha256"], canonical({
            key: value for key, value in owner.items() if key != "content_identity"
        }))
        variants = []
        for path, value in (
            (("reason",), "Updated scope reason"),
            (("review_target", "body_sha256"), hashlib.sha256(updated_source_body.encode()).hexdigest()),
            (("target_disposition", "decision_summary"), "Updated disposition"),
            (("source_actions", 0, "payload", "body"), "Updated body"),
            (("source_actions", 0, "target", "repo"), "example/another"),
        ):
            stale = copy.deepcopy(owner)
            current = stale
            for part in path[:-1]:
                current = current[part]
            current[path[-1]] = value
            variants.append(stale)
        for stale in variants:
            for script, args in (
                ("record-requirements-clarification.sh", ("--mode", "standalone")),
                ("check-requirements-clarification.sh", ()),
            ):
                with self.subTest(script=script, stale=stale):
                    result = self.command(script, stale, *args, "--input", "-")
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(json.loads(result.stdout)["code"], "stale_identity")
                    self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_invoke_checks_bindings_and_preserves_upstream_duplicate_token(self):
        public = json.loads((self.package / "examples/public-initial-change-request-input-2.0.json").read_text())
        public["source_exit"] = "context_ready"
        snapshot = public["duplicate_snapshot"]
        snapshot["candidates"] = [{
            "repo": "example/guru-extension", "number": 9,
            "url": "https://github.com/example/guru-extension/issues/9",
            "updated_at": "2026-01-01T00:00:00Z", "facts_sha256": "8" * 64,
        }]
        owner = self.authoring(self.example)
        owner["mode"] = "workflow"
        disposition = owner["target_disposition"]
        disposition.update({
            "duplicate_query": snapshot["query"], "duplicate_checked_at": snapshot["checked_at"],
            "duplicate_facts_sha256": snapshot["facts_sha256"],
            "duplicate_candidates": [{**snapshot["candidates"][0], "identity": "#9", "state": "open",
                                      "decision": "rejected", "reason": "Different delivery goal"}],
        })
        owner = self.record_owner(owner)
        self.assertEqual(owner["target_disposition"]["duplicate_facts_sha256"], snapshot["facts_sha256"])
        self.assertEqual(owner["target_disposition"]["duplicate_candidates"][0]["facts_sha256"], "8" * 64)
        transition = json.loads((self.package / "examples/public-clear-output-2.0.json").read_text())["transition"]
        for field in ("clarity_result_sha256", "target_content_sha256", "clarity", "target_disposition"):
            transition.pop(field)
        transition.update(stage="context_current", target_locator=public["target_locator"],
                          authority_content_sha256=snapshot["authority_content_sha256"])
        envelope = {"schema_version": "1.0", "public_input": public,
                    "transition": transition, "owner_context": {}, "owner_result": owner}
        result = self.command("invoke.sh", envelope, "--invocation", "-")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["transition"]["target_disposition"]["duplicate_facts_sha256"],
                         snapshot["facts_sha256"])
        for label in ("content_changed", "snapshot_refreshed", "unrecorded_authoring"):
            stale = copy.deepcopy(envelope)
            if label == "content_changed":
                stale["owner_result"]["confirmed_facts"][0]["summary"] = "Updated source content"
            elif label == "snapshot_refreshed":
                refreshed = stale["public_input"]["duplicate_snapshot"]
                refreshed["query"] += " accepted criterion"
                refreshed["checked_at"] = "2026-01-01T00:05:00Z"
                unsigned_snapshot = {key: value for key, value in refreshed.items() if key != "facts_sha256"}
                refreshed["facts_sha256"] = hashlib.sha256(json.dumps(
                    unsigned_snapshot, sort_keys=True, separators=(",", ":"), ensure_ascii=False
                ).encode()).hexdigest()
            else:
                stale["owner_result"] = self.authoring(owner)
            rejected = self.command("invoke.sh", stale, "--invocation", "-")
            self.assertNotEqual(rejected.returncode, 0)
            self.assertEqual(json.loads(rejected.stdout)["code"],
                             "schema_mismatch" if label == "unrecorded_authoring" else "stale_identity")
            self.assertNotIn("Traceback", rejected.stdout + rejected.stderr)


if __name__ == "__main__":
    unittest.main()
