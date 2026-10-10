"""Focused installed producer chains for #250; no native semantic claims."""
from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_ROOT))
import verify_installed_phase0_transcript as transcript
from test_discovery_stdin_integration import run_preset_install
from test_readiness_transition_integration import producers
from jsonschema import Draft202012Validator
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository

SOURCE = Path(__file__).resolve().parents[5]


class InstalledIntakeProfilesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="guru-250-profiles-")
        cls.work = Path(cls.temp.name)
        cls.installed = cls.work / "installed"
        (cls.installed / ".trellis").mkdir(parents=True)
        shutil.copy2(SOURCE / "trellis/workflows/guru-team/workflow.md", cls.installed / ".trellis/workflow.md")
        shutil.copytree(SOURCE / ".trellis/scripts", cls.installed / ".trellis/scripts", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        applied = run_preset_install(cls.installed)
        if applied.returncode:
            raise RuntimeError(applied.stdout[-3000:] + applied.stderr)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def author(self, owner):
        owner = copy.deepcopy(owner)
        owner.pop("content_identity", None)
        owner["review_target"].pop("facts_sha256", None)
        if owner["target_disposition"]:
            owner["target_disposition"].pop("disposition_digest", None)
        for row in owner["scope_proposals"]:
            row.pop("proposal_digest", None)
        for row in owner["source_actions"]:
            row.pop("action_digest", None)
            row.pop("payload_sha256", None)
        return owner

    def clarify(self, root, env, public, transition, authored):
        skill = "guru-clarify-requirements"
        owner = transcript.record_semantic(root, env, skill, "record-requirements-clarification.sh",
                                          ["--input", "-", "--mode", public["mode"]], self.author(authored))
        transcript.record_semantic(root, env, skill, "check-requirements-clarification.sh",
                                   ["--input", "-"], owner)
        return transcript.invoke_public(root, env, skill, {
            "schema_version": "1.0", "public_input": public, "transition": transition,
            "owner_context": {}, "owner_result": owner,
        }, authored["typed_exit"])[0]

    def project(self, root, skill, actual):
        public, _ = transcript.project_installed_output(root, skill, actual["exit_id"], actual)
        package = root / ".trellis/guru-team/skills/packages" / skill
        interface = json.loads((package / "interface.json").read_text())
        projection = next(row for row in interface["public_contracts"]["projections"] if row["exit_id"] == actual["exit_id"])
        consumer = next(row for row in interface["public_contracts"]["consumer_inputs"] if row["id"] == projection["consumer_input_id"])
        contract = consumer.get("contract", {})
        if contract.get("profile_selector"):
            self.assertEqual({"source": "producer_output", "field": "handoff_profile"}, contract["profile_selector"])
            self.assertEqual(actual["handoff_profile"], public["profile"])
        return public

    def validate_clarify_input(self, root, public):
        package = root / ".trellis/guru-team/skills/packages/guru-clarify-requirements"
        interface = json.loads((package / "interface.json").read_text())
        selected = next(row for row in interface["public_contracts"]["input"]["profiles"] if row["id"] == public["profile"])
        schema = json.loads((package / selected["schema"]["path"]).read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(public)))

    def test_four_context_returns_repeat_and_live_task_change(self):
        root, env, _, _, discovery, _, _, clarity_owner, _ = producers(self.installed, self.work / "returns")
        task_ref = ".trellis/tasks/250-return"
        task_dir = root / task_ref
        task_dir.mkdir(parents=True)
        task = {"id": "250-return", "name": "return", "title": "Return", "description": "Return fixture",
                "status": "in_progress", "priority": "P2", "createdAt": "2026-01-01", "notes": "",
                "lifecycle_generation": 0, "source": {"kind": "no_issue"}, "children": [], "relatedFiles": [], "meta": {},
                **{k: None for k in ("dev_type", "scope", "package", "completedAt", "base_branch", "worktree_path", "commit", "pr_url", "parent")}}
        (task_dir / "task.json").write_text(json.dumps(task))
        with (root / ".git/info/exclude").open("a") as stream:
            stream.write("\n.trellis/tasks/\n")
        BranchBindingStore(inspect_repository(root)).establish(TaskLifecycleKey(task["id"], 0), "main")
        entries = [("standard_intake", "reuse"), ("reviewed_plan_intake", "reuse"),
                   ("active_task_scope_change", "no_issue"), ("active_task_scope_change", "reference_only"),
                   ("standalone_review", "no_issue")]
        for profile, source_relation in entries:
            with self.subTest(profile=profile, source_relation=source_relation):
                if profile == "active_task_scope_change":
                    task["source"] = ({"kind": "no_issue"} if source_relation == "no_issue" else
                                      {"kind": "issue", "repo_ref": "example/guru-extension", "number": 145, "disposition": "reference_only"})
                    (task_dir / "task.json").write_text(json.dumps(task))
                public = self.project(root, "guru-discover-change-context", discovery)
                public["profile"] = profile
                transition = copy.deepcopy(discovery["transition"])
                owner = copy.deepcopy(clarity_owner)
                if profile == "reviewed_plan_intake":
                    public["source_locators"] = [{"locator": public["target_locator"], "section": "body"}]
                    transition["source_locators"] = public["source_locators"]
                if profile in {"active_task_scope_change", "standalone_review"}:
                    public.pop("duplicate_snapshot")
                    public["resume_target"] = "guru-approve-task-plan" if profile == "active_task_scope_change" else "guru-standalone-caller"
                    owner["invocation_context"].update(kind=profile, resume_target=public["resume_target"])
                if profile == "standalone_review":
                    public["mode"] = owner["mode"] = transition["mode"] = "standalone"
                if profile == "active_task_scope_change":
                    owner["target_disposition"] = None
                    public.update(task_locator=task_ref, task_id=task["id"], lifecycle_generation=0)
                    owner["invocation_context"]["task_locator"] = task_ref
                for cycle in range(2):
                    owner["typed_exit"] = "needs_context"
                    owner["consumer"] = {"kind": "skill", "id": "guru-discover-change-context"}
                    owner["context_evidence"] = {"status": "missing", "evidence_refs": ["repository.current_owner"], "missing_reason": "Current owner evidence requires another repository read."}
                    requested = self.clarify(root, env, public, transition, owner)
                    request_input = self.project(root, "guru-clarify-requirements", requested)
                    context_owner, _, request_input = transcript.checked_context_owner_for_issue(root, env, request_input, requested["transition"])
                    returning, _ = transcript.invoke_public(root, env, "guru-discover-change-context", {
                        "schema_version": "1.0", "public_input": request_input, "transition": requested["transition"],
                        "owner_context": {}, "owner_result": context_owner,
                    }, "context_ready")
                    public = self.project(root, "guru-discover-change-context", returning)
                    self.validate_clarify_input(root, public)
                    self.assertEqual(profile, public["profile"])
                    self.assertEqual(discovery["transition"]["continuation_id"], public["continuation_id"])
                    transition = returning["transition"]
                if profile == "active_task_scope_change":
                    owner["scope_proposals"] = [{"proposal_id": "current_scope", "scenario": "Retain the current task scope.", "trigger_evidence": [task_ref],
                        "proposed_contracts": ["task scope"], "cost": "Current planning reread.", "alternatives": ["Defer the added scope."],
                        "consequence_if_omitted": "The supported scope choice remains unresolved.", "origin_requirement_status": "explicit",
                        "optional_mechanism_origin": False, "decision": "accepted_current"}]
                    owner["active_task_evidence"] = {"task_locator": task_ref, "github_authority_facts_sha256": owner["review_target"]["facts_sha256"],
                        "planning_documents": [{"path": task_ref + "/" + name, "content_sha256": "1" * 64} for name in ("prd.md", "design.md", "implement.md")],
                        "decision_trail": None, "reentry_owners": ["guru-approve-task-plan", "guru-check-task", "guru-review-branch"]}
                owner["typed_exit"] = "clear"
                owner["consumer"] = {"kind": "workflow", "id": "guru-requirements-clear-router"}
                owner["context_evidence"] = clarity_owner["context_evidence"]
                cleared = self.clarify(root, env, public, transition, owner)
                self.assertEqual(profile, cleared["profile"])
                self.assertEqual(owner["invocation_context"]["resume_target"], cleared["resume_target"])
        # A normal generation change requires fresh active input, not a preserved old return.
        task["lifecycle_generation"] = 1
        (task_dir / "task.json").write_text(json.dumps(task))
        request_input["return_identity"] = {"profile": "active_task_scope_change", "target_locator": discovery["handoff_target_locator"],
                                          "continuation_id": discovery["handoff_continuation_id"], "task_locator": task_ref,
                                          "task_id": task["id"], "lifecycle_generation": 0, "resume_target": "guru-approve-task-plan"}
        skill = "guru-discover-change-context"
        authored = transcript.context_owner_for_issue(root, env)
        result = transcript.run([root / f".trellis/guru-team/skills/packages/{skill}/scripts/record-context-discovery.sh", "--invocation", "-"],
                                cwd=root, env=env, stdin={"schema_version": "1.0", "public_input": request_input, "transition": requested["transition"], "owner_context": {}, "owner_result": authored}, check=False)
        self.assertEqual(3, result.returncode, result.stdout)
        self.assertEqual("stale_identity", json.loads(result.stdout)["code"])

    def test_source_selection_reaches_current_task_intake(self):
        selection = [{"locator": "https://github.com/example/guru-extension/issues/145", "section": "body/interface", "authority_kind": "design_constraint"},
                     {"locator": "https://github.com/example/guru-extension/issues/145", "section": "body/candidate", "authority_kind": "advisory"}]
        root, env, source, source_path, discovery, clarity, wording, _, _ = producers(self.installed, self.work / "sources", selection)
        self.assertEqual(selection, clarity["source_selection"])
        self.assertEqual(selection, wording["transition"]["source_selection"])
        owner, checked = transcript.checked_readiness_owner_for_issue(root, env, wording["transition"], source_path, "ready")
        envelope = transcript.readiness_invocation(wording["transition"], source, owner)
        envelope["validation_receipt"] = checked["validation_receipt"]
        ready, _ = transcript.invoke_public(root, env, "guru-review-change-request", envelope, "ready")
        projected = self.project(root, "guru-review-change-request", ready)
        self.assertEqual(selection, projected["transition"]["source_selection"])
        schema = json.loads((root / ".trellis/guru-team/skills/packages/guru-review-change-request/consumers/workflow/stage0/task-intake-ready.schema.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(projected)))
        # Readiness's current re-entry preserves the original reviewed source input.
        transition = copy.deepcopy(discovery["transition"])
        transition["clarify_profile"] = "reviewed_plan_intake"
        transition["source_locators"] = [{"locator": selection[0]["locator"], "section": "body"}]
        owner, checked = transcript.checked_readiness_owner_for_issue(root, env, transition, source_path, "clarify_requirements")
        envelope = transcript.readiness_invocation(transition, source, owner)
        envelope["validation_receipt"] = checked["validation_receipt"]
        reentry, _ = transcript.invoke_public(root, env, "guru-review-change-request", envelope, "clarify_requirements")
        public = self.project(root, "guru-review-change-request", reentry)
        public["duplicate_snapshot"] = discovery["duplicate_snapshot"]
        self.validate_clarify_input(root, public)
        self.assertEqual(transition["source_locators"], public["source_locators"])

    def test_actual_qualifiers_return_to_original_owner(self):
        root, env, _, _, discovery, _, _, owner, _ = producers(self.installed, self.work / "qualifiers")
        head = transcript.run(["git", "rev-parse", "HEAD"], cwd=root).stdout.strip()
        for qualifier, profile in (("guru-qualify-normal-scenario", "normal_scenario_scope_confirmation"),
                                   ("guru-qualify-solution-mechanism", "solution_mechanism_scope_confirmation")):
            with self.subTest(qualifier=qualifier):
                target = discovery["handoff_target_locator"]
                public = {"profile": "task_free_pre_write", "mode": "workflow", "caller": "guru-execute-task-free-change", "target_locator": target,
                          "target": {"repo_locator": ".", "request_locator": target, "checkout_head": head, "bounded_paths": [".trellis/workflow.md"]},
                          "candidate_refs": ["candidate-1"], "candidate_locators": [{"candidate_ref": "candidate-1", "locators": ["path:.trellis/workflow.md"]}]}
                semantic = {"schema_version": "1.0", "skill_id": qualifier, "public_input": public,
                            "candidate_results": [{"candidate_ref": "candidate-1", "decision": "scope_confirmation_required", "reason": "A supported scope choice needs clarification.",
                                "witness": {"requirement_refs": ["path:.trellis/workflow.md"], "supported_entry_refs": ["path:.trellis/workflow.md"], "existing_caller_refs": [public["caller"]],
                                            "honest_action_sequence": ["Invoke the supported owner with an unresolved scope choice."], "defect_observation": "The current authority leaves this legitimate choice unresolved.", "excluded_assumptions": []}}],
                            "ai_review_gate": {"status": "passed", "reviewed_candidate_refs": ["candidate-1"], "summary": "Reviewed the current scope choice."},
                            "typed_exit": "scope_confirmation_required", "consumer": {"kind": "skill", "id": "guru-clarify-requirements"}}
                scripts = root / ".trellis/guru-team/skills/packages" / qualifier / "scripts"
                suffix = "normal-scenario-qualification" if qualifier.endswith("normal-scenario") else "solution-mechanism-qualification"
                recorded = transcript.record_semantic(root, env, qualifier, f"record-{suffix}.sh", ["--input", "-"], semantic)
                checked = transcript.json_stdout(transcript.run([scripts / f"check-{suffix}.sh", "--input", "-"], cwd=root, env=env, stdin=recorded), "qualification check")
                checked = transcript.project_intermediate(root, checked)
                scope, _ = transcript.invoke_public(root, env, qualifier, checked, "scope_confirmation_required")
                clarify_input = self.project(root, qualifier, scope)
                self.validate_clarify_input(root, clarify_input)
                self.assertEqual(profile, clarify_input["profile"])
                current_owner = copy.deepcopy(owner)
                current_owner["invocation_context"].update(kind=profile, caller=qualifier, resume_target=scope["resume_target"])
                transition = copy.deepcopy(discovery["transition"])
                transition["continuation_id"] = clarify_input["continuation_id"]
                cleared = self.clarify(root, env, clarify_input, transition, current_owner)
                self.assertEqual("guru-execute-task-free-change", cleared["resume_target"])
                self.assertEqual(profile, cleared["profile"])


if __name__ == "__main__":
    unittest.main()
