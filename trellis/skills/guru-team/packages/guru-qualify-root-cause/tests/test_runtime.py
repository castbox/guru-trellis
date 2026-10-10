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


class RootCauseRuntimeTest(unittest.TestCase):
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
            "branch_review_candidate_set": "guru-review-branch", "publication_candidate_set": "guru-review-task-delivery",
        }
        planning_paths = [".trellis/tasks/current/prd.md", ".trellis/tasks/current/design.md", ".trellis/tasks/current/implement.md"]
        planning_identity = qualification_common.file_set_identity(self.repo, planning_paths)
        targets = {
            "task_free_pre_write": {"repo_locator":".","request_locator":"request:test","checkout_head":self.head,"bounded_paths":["AGENTS.md"]},
            "task_free_evolution": {"repo_locator":".","request_locator":"request:test","checkout_head":self.head,"approved_paths":["AGENTS.md"],"edited_paths":["AGENTS.md"]},
            "requirements_scope_set": {"repo_locator":".","authority_kind":"active_task","authority_locator":".trellis/tasks/current","authority_identity":"current-task","scope_locator":"path:AGENTS.md"},
            "change_request_candidate_set": {"repo_locator":".","request_locator":"request:test","request_identity":"current-request","readiness_locators":["path:AGENTS.md"]},
            "planning_scenario_set": {"repo_locator":".","task_ref":"current","planning_paths":planning_paths,"planning_identity":planning_identity},
            "implementation_discovery": {"repo_locator":".","task_ref":"current","planning_identity":planning_identity,"checkout_head":self.head,"diff_locator":"HEAD^...HEAD"},
            "base_impact_candidate_set": {"repo_locator":".","task_ref":"current","old_base_head":self.head,"new_base_head":self.head,"task_head":self.head,"base_pair_locator":"HEAD...HEAD"},
            "phase2_candidate_set": {"repo_locator":".","task_ref":"current","checkout_head":self.head,"planning_identity":planning_identity,"diff_locator":"HEAD^...HEAD"},
            "branch_review_candidate_set": {"repo_locator":".","task_ref":"current","base_head":self.head,"review_head":self.head,"review_commit":self.head,"range_locator":"HEAD...HEAD"},
            "publication_candidate_set": {"repo_locator":".","task_ref":"current","review_commit":self.head,"publication_payload_locator":"pull-request:draft","publication_payload_identity":"b"*64},
        }
        return {"profile":profile,"mode":mode,"caller":callers[profile],"target_locator":".trellis/tasks/current","target":targets[profile],"candidate_refs":["candidate-1"],"candidate_locators":[{"candidate_ref":"candidate-1","locators":["path:AGENTS.md"]}]}

    def semantic(self, goal="ordinary_feature", classification="not_incident_applicable", exit_id="classified", profile="implementation_discovery", mode="workflow"):
        branches = json.loads((PACKAGE / "schemas/semantic-result.schema.json").read_text())["$defs"]["candidateResult"]["oneOf"]
        branch = next(row for row in branches if row["properties"]["goal"]["const"] == goal)
        evidence = {key: (["Collect the first-failure observation."] if field.get("type") == "array" else "Current reviewed evidence for " + key) for key, field in branch["properties"]["evidence"]["properties"].items()}
        return {"schema_version":"1.0", "skill_id":"guru-qualify-root-cause", "public_input":self.public_input(profile, mode), "candidate_results":[{"candidate_ref":"candidate-1", "goal":goal, "classification":classification, "reason":"Reviewed current candidate facts.", "evidence":evidence}], "ai_review_gate":{"status":"passed", "reviewed_candidate_refs":["candidate-1"], "summary":"Reviewed the entire current set."}, "typed_exit":exit_id, "consumer":qualification_common.CONSUMERS[exit_id]}

    def invoke(self, semantic):
        with mock.patch("sys.stdin", io.StringIO(json.dumps({"schema_version":"1.0", "semantic_result":semantic}))):
            return qualification_invoke.run(PACKAGE, {}, ["--invocation", "-"])

    def test_all_profile_modes_no_repo_residue(self):
        for profile in qualification_common.PROFILE_SCHEMAS:
            for mode in ("workflow", "standalone"):
                before = sorted(str(p.relative_to(self.repo)) for p in self.repo.rglob("*"))
                output = self.invoke(self.semantic(profile=profile, mode=mode))
                self.assertEqual("classified", output["exit_id"])
                self.assertEqual(profile, output["profile"])
                self.assertEqual({"exit_id", "profile", "continuation_id", "candidate_dispositions"}, set(output))
                self.assertEqual(before, sorted(str(p.relative_to(self.repo)) for p in self.repo.rglob("*")))

    def test_goals_classifications_and_exit_specific_projection(self):
        cases = [("ordinary_feature","not_incident_applicable","classified"), ("diagnosis","diagnosis_incomplete","classified"), ("mitigation","mitigation_only","classified"), ("protection","protection_invariant_eligible","classified"), ("root_cause_fix","root_cause_mechanism_eligible","classified"), ("root_cause_fix","diagnosis_incomplete","diagnosis_required"), ("root_cause_fix","symptom_suppression_rejected","mechanism_revision_required"), ("diagnosis","blocked","blocked")]
        for goal, classification, exit_id in cases:
            output = self.invoke(self.semantic(goal, classification, exit_id))
            self.assertEqual(exit_id, output["exit_id"])
            self.assertNotIn("evidence", output)
            self.assertNotIn("candidate_results", output)

    def test_mixed_set_priority_and_only_actionable_refs(self):
        result = self.semantic("root_cause_fix","diagnosis_incomplete","mechanism_revision_required")
        suppression = copy.deepcopy(result["candidate_results"][0]); suppression.update(candidate_ref="candidate-2",classification="symptom_suppression_rejected")
        result["candidate_results"].append(suppression)
        result["public_input"]["candidate_refs"].append("candidate-2")
        result["public_input"]["candidate_locators"].append({"candidate_ref":"candidate-2","locators":["path:AGENTS.md"]})
        result["ai_review_gate"]["reviewed_candidate_refs"].append("candidate-2")
        output=self.invoke(result)
        self.assertEqual(["candidate-2"], [row["candidate_ref"] for row in output["revision_candidates"]])

    def test_stale_planning_and_head_fail_then_fresh_reentry(self):
        original = self.semantic()
        (self.repo / ".trellis/tasks/current/prd.md").write_text("normal planning revision\n")
        with self.assertRaises(CommandError) as error:
            self.invoke(original)
        self.assertEqual("stale_identity", error.exception.code)
        self.assertEqual("classified", self.invoke(self.semantic())["exit_id"])
        subprocess.run(["git","add","."],cwd=self.repo,check=True)
        subprocess.run(["git","commit","-qm","normal revision"],cwd=self.repo,check=True)
        with self.assertRaises(CommandError): self.invoke(original)

    def test_real_public_wrapper_commands_and_no_qualification_residue(self):
        actual_repo = PACKAGE.parents[4]
        actual_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=actual_repo, text=True).strip()
        def snapshot():
            status = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=all"], cwd=actual_repo)
            runtime = actual_repo / ".trellis/.runtime/guru-team"
            files = sorted(str(p.relative_to(runtime)) for p in runtime.rglob("*") if p.is_file()) if runtime.exists() else []
            return status, files
        for goal, classification, exit_id in [("diagnosis", "diagnosis_incomplete", "classified"), ("root_cause_fix", "diagnosis_incomplete", "diagnosis_required"), ("root_cause_fix", "symptom_suppression_rejected", "mechanism_revision_required"), ("diagnosis", "blocked", "blocked")]:
            result = self.semantic(goal, classification, exit_id, profile="task_free_pre_write")
            result["public_input"].update(target_locator="request:wrapper-test", candidate_locators=[{"candidate_ref":"candidate-1", "locators":["path:README.md"]}])
            result["public_input"]["target"].update(checkout_head=actual_head, bounded_paths=["README.md"])
            before = snapshot()
            transport = json.dumps(result)
            for command in ["record-root-cause-qualification.sh", "check-root-cause-qualification.sh", "invoke.sh"]:
                flag = "--invocation" if command == "invoke.sh" else "--input"
                process = subprocess.run([str(PACKAGE / "scripts" / command), flag, "-"], cwd=actual_repo,
                    input=transport, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.assertEqual(0, process.returncode, process.stderr + process.stdout)
                transport = process.stdout if command == "invoke.sh" else json.dumps(json.loads(process.stdout)["result"])
            self.assertEqual(exit_id, json.loads(transport)["exit_id"])
            self.assertEqual(before, snapshot())

    def test_common_authoring_omission_and_wrong_goal_route_are_rejected(self):
        result=self.semantic("root_cause_fix","diagnosis_incomplete","classified")
        with self.assertRaises(CommandError): self.invoke(result)
        result=self.semantic(); result["candidate_results"]=[]
        with self.assertRaises(CommandError): self.invoke(result)


if __name__ == "__main__": unittest.main()
