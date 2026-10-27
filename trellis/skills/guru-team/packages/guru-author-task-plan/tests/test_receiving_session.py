"""Normal owner recovery and first-failure diagnostics on the installed API.

These are package integration/validator tests. Synthetic contexts and fixture
semantic decisions do not establish native Agent continuation.
"""
import contextlib
import io
import json
import os
import subprocess
import unittest
from unittest.mock import patch

import test_planning_chain as planning
from support import owner_module
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.io import CommandError
from runtime.task_lifecycle.errors import LifecycleContractError


class ReceivingSessionTests(unittest.TestCase):
    def setUp(self):
        self.chain = planning.PlanningChainTest()
        self.chain.setUp()
        self.addCleanup(self.chain.doCleanups)
        self.chain.docs()
        self.projection = self.chain.fixture.projection
        self.candidate = {"design_facts": ["Retain the current application owners."],
                          "constraint_refs": ["docs/source.md#Design"]}
        self.public = {"profile": "delivery_initial_review", "mode": "workflow",
                       "task_ref": self.chain.ref, "delivery_key": self.chain.key,
                       "source_selection": [{"locator": "docs/source.md", "section": "Design",
                                             "authority_kind": "design_constraint"}]}
        self.output = {"exit_id": "requirements_ready", "task_ref": self.chain.ref,
                       "delivery_key": self.chain.key, "candidate": self.candidate}

    def failures(self, field, *owner_tokens):
        chain = self.chain
        for name, run in (
            ("Author", lambda: chain.author(self.public, self.output, expected=3)),
            ("Architecture", lambda: chain.architecture(self.candidate, expected=3)),
        ):
            with self.subTest(owner=name):
                error = run()
                self.assertEqual((error["code"], error["field_path"]), ("stale_identity", field))
                for token in owner_tokens:
                    self.assertIn(token, error["remediation"])

    def bind_receiver(self):
        chain = self.chain
        public = {"profile": "delivery_rebind_missing_session", "mode": "workflow",
                  "task_id": chain.key["task_id"], "lifecycle_generation": 0,
                  "continuation_id": "receiving-session"}
        path = chain.root / "binding-input.json"
        path.write_text(json.dumps(public))
        return chain.command("guru-bind-task-session", "invoke-guru-bind-task-session",
                             ["--input", str(path), "--owner-result", "-"], {
                                 **public, "route": "rebind", "resume_target": "guru-current-phase-router",
                                 "ai_review_gate": {"status": "passed", "summary": "Fixture exact missing-pointer recovery."}})

    def select_receiver(self):
        chain = self.chain
        public = {"profile": "delivery_selection", "mode": "workflow",
                  "task_ref": chain.ref, "delivery_key": chain.key}
        path = chain.root / "selection-input.json"
        path.write_text(json.dumps(public))
        return chain.command("guru-create-delivery", "invoke-guru-create-delivery",
                             ["--input", str(path), "--owner-result", "-"],
                             {"typed_exit": "created", "reason": "Fixture explicit same-slice selection."})

    def test_fresh_receiver_uses_original_bind_and_selection_without_replanning(self):
        chain = self.chain
        record = self.projection.read_record()
        plans = {p: p.read_bytes() for p in chain.directory.iterdir() if p.is_file()}
        refs = subprocess.check_output(["git", "show-ref"], cwd=chain.root)
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "fresh-receiving-session"}):
            self.assertEqual(self.projection.current()["kind"], "no_current_task")
            self.failures("session.task", "guru-bind-task-session")
            self.assertEqual(self.bind_receiver()["exit_id"], "session_rebound")
            self.assertEqual(self.projection.current()["kind"], "no_current_delivery")
            self.failures("session.delivery", "guru-create-delivery:delivery_selection")
            selected = self.select_receiver()
            self.assertEqual(selected["delivery_key"], chain.key)
            self.assertEqual(self.projection.current()["key"], chain.key)
            self.assertEqual(chain.author(self.public, self.output), self.output)
            self.assertEqual(chain.architecture(self.candidate)["planning_purpose"], "candidate_assessment")
            self.assertEqual(self.projection.read_record(), record)
        self.assertEqual(self.projection.current()["key"], chain.key)  # original session unchanged
        self.assertEqual({p: p.read_bytes() for p in plans}, plans)
        self.assertEqual(subprocess.check_output(["git", "show-ref"], cwd=chain.root), refs)

    def test_existing_plan_resumes_wording_approval_and_activation_on_same_key(self):
        chain = self.chain
        candidate = chain.architecture(self.candidate)
        planned = chain.author({"profile": "delivery_solution_planning", "mode": "workflow",
            "task_ref": chain.ref, "delivery_key": chain.key,
            "architecture_assessment": {name: candidate[name] for name in (
                "planning_purpose", "baseline_identity", "constitution_identity", "impact_kind", "impact_reason")}},
            {"exit_id": "plan_ready", "task_ref": chain.ref, "delivery_key": chain.key})
        self.assertEqual(planned["exit_id"], "plan_ready")
        before = self.projection.read_record()
        plans = {p: p.read_bytes() for p in chain.directory.iterdir() if p.is_file()}
        # This receiver's outstanding work is Wording/final Architecture/Approval,
        # so recovery never calls initial Author again.
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "existing-plan-receiver"}):
            self.assertEqual(self.bind_receiver()["exit_id"], "session_rebound")
            self.select_receiver()
            self.assertEqual(chain.wording()["exit_id"], "pass")
            approved = chain.approve(chain.architecture())
            self.assertEqual(approved["exit_id"], "approved")
            self.assertEqual(self.projection.read_record(), before)
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "activation-receiver"}):
            self.assertEqual(self.bind_receiver()["exit_id"], "session_rebound")
            self.select_receiver()
            public = {"profile": "delivery_activation", "mode": "workflow", "task_ref": chain.ref,
                      "delivery_key": chain.key, "planning_result_id": approved["planning_result_id"], "action": "activate"}
            path = chain.root / "activation-input.json"
            path.write_text(json.dumps(public))
            activated = chain.command("guru-activate-delivery", "invoke-guru-activate-delivery",
                ["--input", str(path), "--owner-result", "-"],
                {"typed_exit": "delivery_started", "reason": "Fixture current original plan transition."})
            self.assertEqual(activated["delivery_key"], chain.key)
            self.assertEqual(self.projection.current()["delivery"]["phase"], "implementing")
        self.assertEqual({p: p.read_bytes() for p in plans}, plans)
        self.assertEqual(len(self.projection.read_record()["deliveries"]), 1)
        self.assertEqual(self.projection.current()["key"], chain.key)

    def test_real_generation_advance_preserves_earlier_explicit_key_diagnostic(self):
        chain = self.chain
        chain.fixture.stop(chain.key)
        scope = self.projection.read_record()["accepted_scope"]
        key = {name: chain.key[name] for name in ("task_id", "lifecycle_generation")}
        completion = {"result_id": "generation-completion", "owner_id": "guru-review-task-completion",
                      "evidence": [scope], "lifecycle_generation": 0, "accepted_scope": scope,
                      "delivery_result_ids": [], "outcome": "completed"}
        self.projection.apply({"api_version": "1.0", "operation": "complete_task", "key": key,
                               "owner_role": "completion", "owner_id": completion["owner_id"], "result": completion})
        closure = {"result_id": "generation-closure", "owner_id": "guru-complete-task-closure",
                   "evidence": [scope], "lifecycle_generation": 0, "completion_result_id": completion["result_id"],
                   "disposition": "no_mutation", "source_result": None}
        self.projection.apply({"api_version": "1.0", "operation": "close_task", "key": key,
                               "owner_role": "closure", "owner_id": closure["owner_id"], "result": closure})
        self.projection.scope(scope, reopen=True)
        subprocess.run(["git", "checkout", "-qb", "task-generation-1"], cwd=chain.root,
                       check=True, capture_output=True)
        repository = planning.inspect_repository(chain.root)
        new_key = planning.TaskLifecycleKey(chain.key["task_id"], 1)
        planning.BranchBindingStore(repository).establish(new_key, "task-generation-1")
        planning.ResourceLedgerStore(repository).establish_current(new_key, binding_revision=0,
            branch_name="task-generation-1", branch_ownership="caller_owned", worktree_ownership="not_applicable")
        environment = {name: value for name, value in os.environ.items()
                       if not name.startswith(("TRELLIS_", "CODEX_", "CLAUDE_", "CURSOR_"))}
        with patch.dict(os.environ, environment, clear=True):
            self.failures("delivery_key", "current generation")
        self.assertEqual(self.projection.read_record()["lifecycle_generation"], 1)
        self.assertEqual(len(self.projection.read_record()["deliveries"]), 1)

    def test_different_selection_is_not_overwritten(self):
        other = self.chain.fixture.create()
        self.assertNotEqual(other, self.chain.key)
        before = self.projection.current()
        self.failures("current.key", "original owner")
        self.assertEqual(self.projection.current(), before)
        self.assertEqual(len(self.projection.read_record()["deliveries"]), 2)

    def test_real_phase_change_reports_phase_before_scope_or_content(self):
        self.chain.fixture.planning(self.chain.key)
        self.assertEqual(self.projection.resolve(self.chain.key)["phase"], "implementing")
        self.failures("delivery.phase", "stage owner", "planning")

    def test_real_scope_change_reports_scope_without_rewriting_slice(self):
        path = self.chain.task / "prd.md"
        path.write_text("New whole-Task scope through the original public writer.\n")
        self.projection.scope(authority_ref(path, self.chain.root))
        before = self.projection.resolve(self.chain.key)
        self.failures("delivery.scope_ref.authority", "Clarify", "scope-revision")
        self.assertEqual(self.projection.resolve(self.chain.key), before)

    def test_no_context_retains_explicit_path_and_terminal_stop(self):
        environment = {k: v for k, v in os.environ.items()
                       if not k.startswith(("TRELLIS_", "CODEX_", "CLAUDE_", "CURSOR_"))}
        with patch.dict(os.environ, environment, clear=True):
            self.assertFalse(self.projection.has_context())
            self.assertEqual(chain_result := self.chain.author(self.public, self.output), self.output)
            self.assertEqual(chain_result["delivery_key"], self.chain.key)
            self.assertEqual(self.chain.architecture(self.candidate)["exit_id"], "baseline_current")
            self.assertEqual(self.projection.current()["kind"], "no_current_task")
            self.chain.fixture.stop(self.chain.key)
            self.assertEqual(self.projection.current(self.chain.key)["kind"], "terminal_delivery")
            self.failures("delivery.phase", "terminal/release")

    def test_query_error_keeps_original_error_and_does_not_become_missing_task(self):
        # Unit boundary: an ordinary public API/read failure, not fabricated
        # persistent session state or a claim of native error recovery.
        with patch.object(DeliveryProjection, "current", return_value={
            "kind": "error", "code": "stale_binding", "message": "Installed session reader could not resolve the current binding.",
        }):
            author = owner_module(planning.PACKAGE)
            architecture_package = planning.PACKAGE.parent / "guru-maintain-architecture-baseline"
            architecture = owner_module(architecture_package)
            envelope = self.chain.architecture_envelope(self.candidate)
            calls = (
                lambda: author.execute(planning.PACKAGE, self.chain.root, self.public, {
                    "public_input": self.public, "output": self.output,
                    "ai_review_gate": {"status": "passed", "summary": "Fixture current query boundary."}}),
                lambda: architecture.run(architecture_package, {}, ["--invocation", "-"]),
            )
            for call in calls:
                with contextlib.chdir(self.chain.root), patch("sys.stdin", io.StringIO(json.dumps(envelope))):
                    with self.assertRaises(CommandError) as raised:
                        call()
                error = raised.exception
                self.assertEqual((error.code, error.field_path), ("stale_identity", "current.error"))
                self.assertIn("stale_binding", error.remediation)
                self.assertIn("not treat this as a missing binding", error.remediation)

    def test_author_preserves_installation_first_failure_before_delivery_guard(self):
        author = owner_module(planning.PACKAGE)
        # A normal incomplete installation fails while resolving the Task,
        # before current() is available. Preserve that actual provider error.
        original = LifecycleContractError("unsupported_delivery_api", "installed.delivery_api",
                                          "Restore the complete matching installation through its original owner.")
        with patch.object(author, "DeliveryProjection", side_effect=original):
            with self.assertRaises(CommandError) as raised:
                author.execute(planning.PACKAGE, self.chain.root, self.public, {
                    "public_input": self.public, "output": self.output,
                    "ai_review_gate": {"status": "passed", "summary": "Fixture installation read boundary."}})
        self.assertEqual((raised.exception.code, raised.exception.field_path),
                         ("stale_identity", original.field_path))
        self.assertIn(original.code, raised.exception.remediation)
        self.assertIn(original.remediation, raised.exception.remediation)
