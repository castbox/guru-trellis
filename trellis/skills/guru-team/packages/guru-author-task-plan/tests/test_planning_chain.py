"""Real installed wrapper continuity. Fixture gates are not native AI evidence."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
REPO = SKILLS.parents[2]
sys.path.insert(0, str(SKILLS))
from adapters.eval.fixture_io import stage_clean_installed_owner_repo
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class PlanningChainTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root, _ = stage_clean_installed_owner_repo(
            Path(self.temp.name), REPO / ".trellis/guru-team/scripts/bash/run-skill-command.sh", PACKAGE)
        self.ref = ".trellis/tasks/demo"
        self.task = self.root / self.ref
        self.task.mkdir(parents=True)
        self.metadata = {
            "id": "demo", "name": "demo", "status": "planning", "lifecycle_generation": 0,
            "source": {"kind": "no_issue"}, "title": "Planning wrapper fixture", "description": "Same-task continuity",
            "dev_type": None, "scope": None, "package": None, "priority": "P2",
            "createdAt": "2026-10-10", "completedAt": None, "base_branch": "main",
            "worktree_path": None, "commit": None, "pr_url": None, "children": [],
            "parent": None, "relatedFiles": [], "notes": "", "meta": {},
        }
        (self.task / "task.json").write_text(json.dumps(self.metadata))
        (self.task / "prd.md").write_text("# Requirements\nCurrent interface and owner commitments are retained.\n")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "planning fixture"], cwd=self.root, check=True)
        repository = inspect_repository(self.root)
        key = TaskLifecycleKey("demo", 0)
        BranchBindingStore(repository).establish(key, "main")
        ResourceLedgerStore(repository).establish_current(
            key, binding_revision=0, branch_name="main", branch_ownership="caller_owned",
            worktree_ownership="not_applicable")
        self.packages = self.root / ".trellis/guru-team/skills/packages"

    def command(self, skill, script, args, value=None):
        root_args = [] if script == "invoke.sh" else ["--root", str(self.root)]
        process = subprocess.run(
            [str(self.packages / skill / "scripts" / script), *root_args, *args],
            cwd=self.root, text=True, input=json.dumps(value) if value is not None else None,
            capture_output=True)
        self.assertEqual(0, process.returncode, process.stdout + process.stderr)
        return json.loads(process.stdout)

    def author(self, public, output):
        path = self.root / "public-author-input.json"
        path.write_text(json.dumps(public))
        owner = {"public_input": public, "output": output,
                 "ai_review_gate": {"status": "passed", "summary": "Deterministic fixture gate; native semantics evaluated separately."}}
        return self.command(PACKAGE.name, "invoke.sh", ["--input", str(path), "--owner-result", "-"], owner)

    def architecture(self, author_output, purpose):
        package = self.packages / "guru-maintain-architecture-baseline"
        public = json.loads((package / "examples/public-input-candidate-assessment-3.0.json").read_text())
        public.update(task_locator=author_output["task_ref"], planning_purpose=purpose)
        if purpose == "candidate_assessment":
            public["candidate"] = author_output["candidate"]
            current = digest(public["candidate"])
        else:
            public.pop("candidate")
            public["design_locator"] = self.ref + "/design.md"
            current = hashlib.sha256((self.task / "design.md").read_bytes()).hexdigest()
        public["freshness_identity"] = "sha256:" + current
        constitution = self.root / public["constitution"]["authority_locator"]
        constitution.parent.mkdir(parents=True, exist_ok=True)
        constitution.write_text("# Current fixture constitution\nOne existing transport owner.\n")
        owner = {key: copy.deepcopy(public[key]) for key in (
            "schema_version", "profile", "mode", "continuation_id", "stage", "task_locator",
            "baseline", "constitution", "project_contract", "freshness_identity", "planning_purpose")}
        owner.update(input_sha256=digest(public), typed_exit="baseline_current",
                     baseline_identity=public["baseline"]["identity"],
                     constitution_identity=public["constitution"]["identity"],
                     impact_kind="no_architecture_impact", impact_reason="Fixture preserves existing responsibilities.",
                     consumer={"kind": "workflow", "id": "guru-architecture-baseline-current-router"},
                     ai_review_gate={"status": "passed", "reviewed_scope": "Fixture candidate and current authority",
                                     "evidence_summary": "Fixture comparison only", "findings": [],
                                     "conclusion": "No boundary change in this deterministic fixture"})
        if purpose == "final_plan":
            owner["promotion_state"] = "no_change"
        return self.command("guru-maintain-architecture-baseline", "invoke.sh", ["--invocation", "-"],
                            {"public_input": public, "owner_result": owner})

    def test_actual_changed_wording_stdout_enters_author_reentry(self):
        wording_package = self.packages / "guru-review-contract-wording"
        for name in ("design.md", "implement.md"):
            (self.task / name).write_text("# Original planning\nCurrent source commitment retained.\n")
        for name in ("implement.jsonl", "check.jsonl"):
            (self.task / name).write_text(json.dumps({"file": ".trellis/spec/workflow/index.md", "reason": "Current contract"}) + "\n")
        path = self.task / "design.md"
        preimage = hashlib.sha256(path.read_bytes()).hexdigest()
        path.write_text("# Current planning\nThe original source commitment is retained.\n")
        selectors = ["--mode", "workflow", "--profile", "planning_artifacts", "--task", self.ref]
        scan = self.command(wording_package.name, "record-contract-wording-review.sh", [*selectors, "--scan-only"])["result"]
        example = json.loads((wording_package / "examples/contract-wording-review.json").read_text())
        gate = example["semantic_review"]["ai_review_gate"]
        gate.update(status="passed", reviewed_scan_sha256=scan["scan"]["scan_sha256"],
                    checked_dimensions=dict.fromkeys(gate["checked_dimensions"], True),
                    planning_checked_dimensions=dict.fromkeys((
                        "no_requirement_weakening", "source_issue_semantics_preserved", "conditional_paths_have_conditions",
                        "no_parallel_implementation_paths", "gates_have_machine_verifiable_conditions",
                        "acceptance_criteria_are_deterministic", "external_quotes_are_labeled_non_contract"), True))
        authored = {"generated_at": "2026-10-11T00:00:00Z", "typed_exit": "content_changed", "classifications": [],
                    "ai_review_gate": gate, "revisions": [{"revision_id": "equivalent-wording", "locator": self.ref + "/design.md",
                        "before_sha256": preimage, "after_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "reason": "Equivalent current wording clarified in this fixture.", "rescan_sha256": scan["scan"]["scan_sha256"]}]}
        record = self.command(wording_package.name, "record-contract-wording-review.sh", [*selectors, "--input", "-"], authored)["result"]
        checked = self.command(wording_package.name, "check-contract-wording-review.sh", ["--task", self.ref, "--input", "-"], record)["result"]
        wording = self.command(wording_package.name, "invoke.sh", ["--invocation", "-"], {
            "public_input": {"profile": "planning_artifacts", "source_exit": "plan_ready", "mode": "workflow",
                "task_locator": self.ref, "planning_artifacts": ["prd.md", "design.md", "implement.md"], "continuation_id": "current-fixture"},
            "owner_result": record, "validation_receipt": checked["validation_receipt"]})
        public = {"profile": "wording_reentry", "mode": "workflow",
                  "task_ref": wording["task_ref"], "change_refs": wording["change_refs"]}
        output = self.author(public, {"exit_id": "plan_ready", "task_ref": wording["task_ref"]})
        self.assertEqual(self.ref, output["task_ref"])
        self.assertEqual("plan_ready", output["exit_id"])
        self.assertEqual([self.ref + "/design.md"], public["change_refs"])

    def test_actual_stdout_chain_distinguishes_candidate_final_and_revision(self):
        initial = {"profile": "initial_review", "mode": "workflow", "task_ref": self.ref,
                   "source_selection": [{"locator": "docs/source.md", "section": "Design A", "authority_kind": "design_constraint"}]}
        ready = self.author(initial, {"exit_id": "requirements_ready", "task_ref": self.ref,
                                    "candidate": {"design_facts": ["One existing transport owner handles protocol forwarding."],
                                                  "constraint_refs": ["docs/source.md#Design-A"]}})
        self.assertFalse((self.task / "design.md").exists())
        candidate = self.architecture(ready, "candidate_assessment")
        self.assertNotIn("promotion_state", candidate)
        assessment = {key: candidate[key] for key in (
            "planning_purpose", "baseline_identity", "constitution_identity", "impact_kind", "impact_reason")}
        solution = {"profile": "solution_planning", "mode": "workflow", "task_ref": candidate["task_locator"],
                    "architecture_assessment": assessment}
        for name in ("design.md", "implement.md"):
            (self.task / name).write_text("# Current planning\nThe source commitments have concrete retained landing points.\n")
        for name in ("implement.jsonl", "check.jsonl"):
            (self.task / name).write_text(json.dumps({"file": ".trellis/spec/workflow/index.md", "reason": "Current contract"}) + "\n")
        planned = self.author(solution, {"exit_id": "plan_ready", "task_ref": candidate["task_locator"]})
        wording_input = {"profile": "planning_artifacts", "source_exit": planned["exit_id"], "mode": "workflow",
                         "task_locator": planned["task_ref"], "planning_artifacts": ["prd.md", "design.md", "implement.md"],
                         "continuation_id": "same-planning-chain"}
        scan = self.command("guru-review-contract-wording", "record-contract-wording-review.sh",
                            ["--mode", "workflow", "--profile", "planning_artifacts", "--task", self.ref, "--scan-only"])["result"]
        dimensions = ("complete_profile_scope", "all_hits_classified", "zero_unchecked_hits", "product_semantics_preserved",
                      "retained_reasons_sufficient", "zero_hits_not_requirement_review")
        planning_dimensions = ("no_requirement_weakening", "source_issue_semantics_preserved", "conditional_paths_have_conditions",
                               "no_parallel_implementation_paths", "gates_have_machine_verifiable_conditions",
                               "acceptance_criteria_are_deterministic", "external_quotes_are_labeled_non_contract")
        auth = {"revisions": [], "classifications": [{"hit_id": hit["hit_id"], "classification": "term_definition", "reason": "Fixture term definition"} for hit in scan["scan"]["hits"]],
                "typed_exit": "pass", "ai_review_gate": {"status": "passed", "reviewer": "deterministic-fixture",
                    "summary": "Fixture transport test", "checked_dimensions": dict.fromkeys(dimensions, True),
                    "planning_checked_dimensions": dict.fromkeys(planning_dimensions, True)}}
        record = self.command("guru-review-contract-wording", "record-contract-wording-review.sh",
                              ["--mode", "workflow", "--profile", "planning_artifacts", "--task", self.ref, "--input", "-"], auth)["result"]
        record_path = self.root / "wording-record.json"
        record_path.write_text(json.dumps(record))
        checked = self.command("guru-review-contract-wording", "check-contract-wording-review.sh",
                               ["--input", str(record_path), "--task", self.ref])["result"]
        wording = self.command("guru-review-contract-wording", "invoke.sh", ["--invocation", "-"],
                              {"public_input": wording_input, "owner_result": record, "validation_receipt": checked["validation_receipt"]})
        self.assertEqual("pass", wording["exit_id"])
        final = self.architecture(planned, "final_plan")
        self.assertEqual("final_plan", final["planning_purpose"])
        self.assertEqual("no_change", final["promotion_state"])
        approval_package = self.packages / "guru-approve-task-plan"
        checkpoint = json.loads((approval_package / "examples/planning-approval.json").read_text())
        authored = {key: checkpoint[key] for key in ("mode", "authority_refs", "delivery_policy", "docs_ssot_plan", "semantic_review", "typed_exit", "consumer", "reason")}
        authored.update(typed_exit="revision_required", consumer={"kind": "workflow", "id": "guru-task-plan-approval-revision-router"})
        authored["semantic_review"].update(status="revision_required", revision_actions=["Define the policy validation boundary."])
        self.command("guru-approve-task-plan", "record-planning-approval.sh", ["--task", final["task_locator"], "--input", "-"], authored)
        self.command("guru-approve-task-plan", "check-planning-approval.sh", ["--task", final["task_locator"], "--require-exit", "revision_required"])
        private = self.root / ".trellis/.runtime/guru-team/owner-checkpoints/demo/planning-approval.json"
        revision = self.command("guru-approve-task-plan", "invoke.sh", ["--input", "-", "--owner-result", str(private)],
                                {"profile": "initial_review", "mode": "workflow", "task_ref": final["task_locator"]})
        self.assertEqual(authored["semantic_review"]["revision_actions"], revision["revision_actions"])
        revised_input = {"profile": "approval_revision", "mode": "workflow", **{key: revision[key] for key in ("task_ref", "revision_actions")}}
        self.assertEqual("plan_ready", self.author(revised_input, planned)["exit_id"])
        self.assertEqual(self.metadata, json.loads((self.task / "task.json").read_text()))

    def test_installed_author_profiles_and_both_delivery_reasons_preserve_identity(self):
        for name in ("design.md", "implement.md"):
            (self.task / name).write_text("# Current fixture planning\n")
        for name in ("implement.jsonl", "check.jsonl"):
            (self.task / name).write_text(json.dumps({"file": ".trellis/spec/workflow/index.md", "reason": "Fixture context"}) + "\n")
        interface = json.loads((PACKAGE / "interface.json").read_text())
        profiles = interface["public_contracts"]["input"]["profiles"]
        for row in profiles:
            public = json.loads((PACKAGE / row["example"]["path"]).read_text())
            public["task_ref"] = self.ref
            reasons = ("delivery_policy_gap", "next_independent_delivery") if row["id"] == "delivery_plan_revision" else (None,)
            for reason in reasons:
                with self.subTest(profile=row["id"], reason=reason):
                    if reason:
                        public["revision_reason"] = reason
                    output = {"exit_id": "plan_ready", "task_ref": self.ref}
                    if row["id"] in {"initial_review", "active_task_scope_change", "requirements_revision", "architecture_conflict_resolution"}:
                        output = {"exit_id": "requirements_ready", "task_ref": self.ref,
                                  "candidate": {"design_locator": self.ref + "/design.md"}}
                    self.assertEqual(output, self.author(public, output))
        self.assertEqual(self.metadata, json.loads((self.task / "task.json").read_text()))


if __name__ == "__main__":
    unittest.main()
