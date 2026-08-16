from __future__ import annotations

import copy
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
PACKAGE_RUNTIME = PACKAGE / "runtime"
for path in (SKILLS, PACKAGE_RUNTIME):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from runtime.io import CommandError  # noqa: E402
import check as qualification_check  # noqa: E402
import common as qualification_common  # noqa: E402
import invoke as qualification_invoke  # noqa: E402
import record as qualification_record  # noqa: E402


class NormalScenarioQualificationRuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Package Test"], cwd=self.repo, check=True)
        (self.repo / "AGENTS.md").write_text("normal scenario authority\n", encoding="utf-8")
        task = self.repo / ".trellis/tasks/current"
        task.mkdir(parents=True)
        for name in ("prd.md", "design.md", "implement.md"):
            (task / name).write_text(name + "\n", encoding="utf-8")
        (task / "issue-scope-ledger.json").write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.repo, check=True)
        self.head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
        self.old_cwd = Path.cwd()
        os.chdir(self.repo)

    def tearDown(self) -> None:
        os.chdir(self.old_cwd)
        self.tmp.cleanup()

    def public_input(self, profile: str, mode: str = "workflow") -> dict:
        callers = {
            "task_free_pre_write": "guru-execute-task-free-change", "task_free_evolution": "guru-execute-task-free-change",
            "requirements_scope_set": "guru-clarify-requirements", "change_request_candidate_set": "guru-review-change-request",
            "planning_scenario_set": "guru-approve-task-plan", "implementation_discovery": "guru-phase2-implementation-coordinator",
            "base_impact_candidate_set": "guru-reconcile-task-base", "phase2_candidate_set": "guru-check-task",
            "branch_review_candidate_set": "guru-review-branch", "publication_candidate_set": "guru-review-task-publication",
        }
        targets = {
            "task_free_pre_write": {"repo_locator":".","request_locator":"request:test","checkout_head":self.head,"bounded_paths":["AGENTS.md"]},
            "task_free_evolution": {"repo_locator":".","request_locator":"request:test","checkout_head":self.head,"approved_paths":["AGENTS.md"],"edited_paths":["AGENTS.md"]},
            "requirements_scope_set": {"repo_locator":".","authority_kind":"active_task","authority_locator":".trellis/tasks/current","authority_identity":"current-task","scope_locator":"path:AGENTS.md"},
            "change_request_candidate_set": {"repo_locator":".","request_locator":"request:test","request_identity":"current-request","readiness_locators":["path:AGENTS.md"]},
            "planning_scenario_set": {"repo_locator":".","task_ref":"current","planning_paths":[".trellis/tasks/current/prd.md",".trellis/tasks/current/design.md",".trellis/tasks/current/implement.md"],"scope_ledger_path":".trellis/tasks/current/issue-scope-ledger.json","planning_identity":"a"*64},
            "implementation_discovery": {"repo_locator":".","task_ref":"current","planning_identity":"a"*64,"checkout_head":self.head,"diff_locator":"HEAD^...HEAD"},
            "base_impact_candidate_set": {"repo_locator":".","task_ref":"current","old_base_head":self.head,"new_base_head":self.head,"task_head":self.head,"base_pair_locator":"HEAD...HEAD"},
            "phase2_candidate_set": {"repo_locator":".","task_ref":"current","checkout_head":self.head,"planning_identity":"a"*64,"diff_locator":"HEAD^...HEAD"},
            "branch_review_candidate_set": {"repo_locator":".","task_ref":"current","base_head":self.head,"review_head":self.head,"review_commit":self.head,"range_locator":"HEAD...HEAD"},
            "publication_candidate_set": {"repo_locator":".","task_ref":"current","review_commit":self.head,"publication_payload_locator":"pull-request:draft","publication_payload_identity":"b"*64},
        }
        return {"profile":profile,"mode":mode,"caller":callers[profile],"target_locator":".trellis/tasks/current","target":targets[profile],"candidate_refs":["candidate-1"],"candidate_locators":[{"candidate_ref":"candidate-1","locators":["path:AGENTS.md"]}]}

    def semantic(self, profile: str = "implementation_discovery", exit_id: str = "classified", decision: str = "qualified_current", mode: str = "workflow") -> dict:
        witness = {"requirement_refs":["path:AGENTS.md"],"supported_entry_refs":["path:AGENTS.md"],"existing_caller_refs":[self.public_input(profile, mode)["caller"]],"honest_action_sequence":["Invoke the supported normal caller."],"defect_observation":"The current required behavior was directly observed.","excluded_assumptions":[]}
        consumers = qualification_common.CONSUMERS
        return {"schema_version":"1.0","skill_id":"guru-qualify-normal-scenario","public_input":self.public_input(profile, mode),"candidate_results":[{"candidate_ref":"candidate-1","decision":decision,"reason":"Current AI-owned scope-first conclusion.","witness":witness}],"ai_review_gate":{"status":"passed","reviewed_candidate_refs":["candidate-1"],"summary":"The complete candidate set was reviewed."},"typed_exit":exit_id,"consumer":copy.deepcopy(consumers[exit_id])}

    def invoke(self, semantic: dict) -> dict:
        envelope = {"schema_version":"1.0","semantic_result":semantic}
        with mock.patch("sys.stdin", io.StringIO(json.dumps(envelope))):
            return qualification_invoke.run(PACKAGE, {}, ["--invocation", "-"])

    def inventory(self) -> list[str]:
        return sorted(str(path.relative_to(self.repo)) for path in self.repo.rglob("*") if ".git" not in path.parts)

    def test_all_ten_profiles_in_workflow_and_standalone_are_invocation_local(self) -> None:
        for profile in qualification_common.PROFILE_SCHEMAS:
            for mode in ("workflow", "standalone"):
                before = self.inventory()
                with self.subTest(profile=profile, mode=mode):
                    output = self.invoke(self.semantic(profile, mode=mode))
                    self.assertEqual("classified", output["exit_id"])
                    self.assertEqual(qualification_common.RESUME_TARGETS[profile], output["resume_target"])
                    self.assertEqual("qualified_current", output["candidate_results"][0]["decision"])
                self.assertEqual(before, self.inventory())

    def test_four_typed_exits_and_fixed_consumers(self) -> None:
        cases = (
            ("classified", "qualified_current"),
            ("scope_confirmation_required", "scope_confirmation_required"),
            ("mechanism_revision_required", "mechanism_removed"),
            ("blocked", "blocked"),
        )
        for exit_id, decision in cases:
            with self.subTest(exit=exit_id):
                output = self.invoke(self.semantic(exit_id=exit_id, decision=decision))
                self.assertEqual(exit_id, output["exit_id"])
        scope = self.invoke(self.semantic(exit_id="scope_confirmation_required", decision="scope_confirmation_required"))
        self.assertEqual("normal_scenario_scope_confirmation", scope["handoff_profile"])
        self.assertEqual(["candidate-1"], scope["candidate_refs"])
        self.assertNotIn("candidate_results", scope)
        self.assertEqual({"exit_id":"blocked"}, self.invoke(self.semantic(exit_id="blocked", decision="blocked")))

    def test_runtime_does_not_semantically_derive_route_from_decision(self) -> None:
        output = self.invoke(self.semantic(exit_id="classified", decision="scope_confirmation_required"))
        self.assertEqual("classified", output["exit_id"])
        self.assertEqual("scope_confirmation_required", output["candidate_results"][0]["decision"])

    def test_record_check_pipeline_is_stdin_stdout_only(self) -> None:
        semantic = self.semantic()
        with mock.patch("sys.stdin", io.StringIO(json.dumps(semantic))):
            recorded = qualification_record.run(PACKAGE, {}, ["--input", "-"])
        with mock.patch("sys.stdin", io.StringIO(json.dumps(recorded))):
            envelope = qualification_check.run(PACKAGE, {}, ["--input", "-"])
        with mock.patch("sys.stdin", io.StringIO(json.dumps(envelope))):
            output = qualification_invoke.run(PACKAGE, {}, ["--invocation", "-"])
        self.assertEqual("classified", output["exit_id"])

    def test_fail_closed_shape_identity_and_freshness_cases(self) -> None:
        bad = self.semantic()
        bad["public_input"]["candidate_refs"] = []
        with self.assertRaises(CommandError): self.invoke(bad)
        bad = self.semantic()
        bad["public_input"]["caller"] = "guru-check-task"
        with self.assertRaises(CommandError): self.invoke(bad)
        bad = self.semantic()
        bad["candidate_results"].append(copy.deepcopy(bad["candidate_results"][0]))
        with self.assertRaises(CommandError): self.invoke(bad)
        bad = self.semantic()
        bad["consumer"] = qualification_common.CONSUMERS["blocked"]
        with self.assertRaises(CommandError): self.invoke(bad)
        bad = self.semantic()
        bad["public_input"]["target"]["checkout_head"] = "0" * 40
        with self.assertRaises(CommandError) as raised: self.invoke(bad)
        self.assertEqual("stale_identity", raised.exception.code)

    def test_stdin_only_contract_rejects_every_locator_argument(self) -> None:
        for module, flag in ((qualification_record, "--input"), (qualification_check, "--input"), (qualification_invoke, "--invocation")):
            with self.subTest(module=module.__name__), self.assertRaises(CommandError) as raised:
                module.run(PACKAGE, {}, [flag, "result.json"])
            self.assertEqual("invalid_arguments", raised.exception.code)

    def test_no_qualification_residue_in_tracked_ignored_or_runtime_paths(self) -> None:
        before = self.inventory()
        self.invoke(self.semantic())
        after = self.inventory()
        self.assertEqual(before, after)
        residue = [path for path in self.repo.rglob("*") if any(token in path.name.lower() for token in ("qualification-result", "qualification-report", "candidate-ledger", "rejection-ledger", "checkpoint", ".new", ".bak"))]
        self.assertEqual([], residue)
        self.assertFalse((self.repo / ".trellis/.runtime").exists())


if __name__ == "__main__":
    unittest.main()
