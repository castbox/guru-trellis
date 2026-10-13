from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

PACKAGE = Path(os.environ.get("SOURCE530_TASKCOMMIT_PACKAGE", Path(__file__).resolve().parents[1]))
SKILLS = PACKAGE.parents[1]
KERNEL = SKILLS if (SKILLS / "runtime").is_dir() else SKILLS.parent
sys.path.insert(0, str(KERNEL))
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository

TASK = ".trellis/tasks/10-12-reentry-fixture"


class CommittedReentryTest(unittest.TestCase):
    """Real wrappers/Git; semantic authoring is fixture data, not AI review proof."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        self.inputs = Path(self.tmp.name) / "inputs"
        self.inputs.mkdir()
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Reentry Fixture")
        self.git("config", "user.email", "reentry@example.invalid")
        (self.repo / ".gitignore").write_text(".trellis/.runtime/\n.trellis/guru-team/\n")
        constitution = self.repo / "docs/architecture/00-foundation/design-constitution.md"
        constitution.parent.mkdir(parents=True)
        constitution.write_text("# Fixture design constitution\nFive current project principles.\n")
        (self.repo / "base.txt").write_text("base\n")
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        self.old_base = self.git("rev-parse", "HEAD")
        self.git("switch", "-qc", "feature/reentry")
        task = self.repo / TASK
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps({"id": "reentry-fixture", "lifecycle_generation": 0, "source": {"kind": "no_issue"}, "name": "reentry-fixture", "title": "Reentry fixture", "description": "Real wrapper fixture", "status": "in_progress", "dev_type": None, "scope": "local fixture", "package": None, "priority": "P2", "createdAt": "2026-10-12", "completedAt": None, "base_branch": "main", "worktree_path": None, "commit": None, "pr_url": None, "children": [], "parent": None, "relatedFiles": [], "notes": "", "meta": {}}))
        (task / "prd.md").write_text("Fixture task: update task.txt.\n")
        (self.repo / "task.txt").write_text("task\n")
        BranchBindingStore(inspect_repository(self.repo)).establish(TaskLifecycleKey("reentry-fixture", 0), "feature/reentry")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, text=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()

    def write(self, name, value):
        path = self.inputs / name
        path.write_text(json.dumps(value, ensure_ascii=False))
        return str(path)

    def call(self, skill, script, *args, stdin=None, ok=True):
        command = ["bash", str(PACKAGE.parent / skill / "scripts" / script), "--root", str(self.repo), *map(str, args), "--json"]
        result = subprocess.run(command, input=None if stdin is None else json.dumps(stdin), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            payload = json.loads(result.stdout or result.stderr)
        except ValueError:
            self.fail(f"{command}: {result.returncode}: {result.stdout}\n{result.stderr}")
        if ok:
            self.assertEqual(0, result.returncode, payload)
        else:
            self.assertNotEqual(0, result.returncode, payload)
        if payload.get("formal_exit") is False:
            self.assertEqual("1.0", payload["schema_version"])
            return payload["result"]
        return payload

    def phase2(self, mode="workflow"):
        example = json.loads((PACKAGE.parent / "guru-check-task/examples/phase2-check.json").read_text())
        keys = {"mode", "reviewed_paths", "validation", "docs_ssot", "delivery_policy", "candidate_classifications", "semantic_review", "typed_exit", "route", "reason", "consumer"}
        authoring = {key: value for key, value in example.items() if key in keys}
        authoring["mode"] = mode
        authoring["reviewed_paths"] = self.git("ls-files", "--cached", "--others", "--exclude-standard").splitlines()
        recorded = self.call("guru-check-task", "record-phase2-check.sh", "--task", TASK, "--input", self.write("phase2.json", authoring))
        self.call("guru-check-task", "check-phase2-check.sh", "--task", TASK)
        public = {"profile": "initial_check", "mode": mode, "task_ref": TASK, "source_exit": "implementation_complete"}
        return self.call("guru-check-task", "invoke.sh", "--input", self.write("phase2-public.json", public), "--owner-result", recorded["artifact_path"])

    def prepare(self, passed, ok=True):
        # The first status column can be a space; stripping stdout drops it.
        paths = subprocess.run(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=self.repo, text=True, check=True, stdout=subprocess.PIPE).stdout.splitlines()
        classifications = [{"path": path[3:], "category": "task-reviewed", "reason": "Fixture scope.", "coverage_source": "current Phase2 fixture"} for path in paths]
        authoring = {"path_classifications": classifications, "message": {"type": "fix", "scope": "fixture", "summary": "验证任务提交", "background": "验证正常链路。", "changes": "提交真实任务增量。", "boundaries": "只作用临时仓库。", "validations": "真实 wrapper 回归。"}, "ai_review": {"status": "passed", "summary": "Fixture-only semantic authoring.", "evidence": ["Fixture current scope."]}}
        public = {"profile": "initial_commit", "mode": "workflow", "task_ref": TASK, "source_exit": passed["exit_id"], "phase2_commit_anchor": passed["phase2_commit_anchor"]}
        return self.call("guru-create-task-commit", "prepare-task-commit.sh", "--input", self.write("commit-public.json", public), "--candidate-json", self.write("commit-authoring.json", authoring), ok=ok)

    def commit_dirty(self):
        passed = self.phase2()
        prepared = self.prepare(passed)
        self.assertTrue(prepared["exact_stage_paths"])
        committed = self.call("guru-create-task-commit", "invoke.sh", "--candidate-artifact", prepared["candidate_artifact"])
        self.assertEqual("committed", committed["exit_id"])
        self.assertEqual("", self.git("status", "--porcelain"))
        return committed

    def guard(self, profile):
        public = {"profile": profile, "mode": "workflow", "task_ref": TASK, "task_head": self.git("rev-parse", "HEAD"), "selected_base_ref": "main", "resume_target": "branch_review" if profile == "post_commit" else "task_commit"}
        return self.call("guru-reconcile-task-base", "guard-task-base-pair.sh", "--input", self.write("guard.json", public))

    def reconcile(self):
        prior = self.git("rev-parse", "HEAD")
        self.git("switch", "main")
        (self.repo / "base.txt").write_text(f"advanced base after {prior}\n")
        self.git("commit", "-qam", "advance base")
        new_base = self.git("rev-parse", "HEAD")
        self.git("switch", "feature/reentry")
        self.assertEqual("new_pair", self.guard("post_commit")["status"])
        candidate = self.call("guru-reconcile-task-base", "execute-base-candidate.sh", "--request", self.write("candidate.json", {"task_head": prior, "new_base_head": new_base, "validation_commands": []}))
        public = {"profile": "post_commit", "mode": "workflow", "task_ref": TASK, "task_head": prior, "selected_base_ref": "main", "resume_target": "branch_review"}
        request = {"profile": "post_commit", "task_ref": TASK, "branch": "feature/reentry", "prior_task_head": prior, "selected_base_ref": "main", "old_base_head": self.old_base, "new_base_head": new_base, "resume_target": "branch_review", "candidate_tree_sha256": candidate["candidate_tree_sha256"], "commit_message": "chore(base): 整合临时基线"}
        receipt = self.call("guru-reconcile-task-base", "execute-base-reconciliation.sh", "--request", self.write("reconcile.json", request))
        gate = {"authority_impact": "unchanged", "task_content_impact": "unchanged", "integration_impact": "compatible", "reviewed_scope": ["authority", "planning", "delta"], "key_delta_refs": ["base.txt"], "validation_evidence": ["Fixture candidate clean."], "unverified_boundaries": [], "summary": "Fixture-only compatible gate.", "typed_exit": "reconciled", "route_payload": {"candidate_tree_sha256": candidate["candidate_tree_sha256"], "relevant_paths": ["base.txt"]}}
        recorded = self.call("guru-reconcile-task-base", "record-base-reconciliation.sh", "--skill-input", self.write("reconcile-public.json", public), "--semantic-review-file", self.write("reconcile-gate.json", gate), "--typed-exit", "reconciled", "--reconciliation-result", self.write("reconcile-result.json", receipt))
        output = self.call("guru-reconcile-task-base", "invoke.sh", "--invocation", self.write("reconcile-envelope.json", {"public_input": public, "owner_result": recorded}))
        self.assertEqual("reconciled", output["exit_id"])
        self.assertEqual("phase2", output["resume_target"])
        self.old_base = new_base
        return output

    def reentry(self, passed, status="passed", ok=True, extra=(), mode="workflow"):
        public = {"profile": "committed_reentry", "mode": mode, "task_ref": TASK, "source_exit": passed["exit_id"], "phase2_commit_anchor": passed["phase2_commit_anchor"]}
        return self.call("guru-create-task-commit", "invoke.sh", "--committed-reentry", "-", *extra, stdin={"public_input": public, "owner_result": {"status": status, "summary": "Fixture current clean candidate.", "evidence": ["Fixture complete range and Phase2."]}}, ok=ok)

    def install_fixture_packages(self, *skill_ids):
        """Copy test runtime assets; this is not installer acceptance evidence."""
        installed = self.repo / ".trellis/guru-team"
        shutil.copytree(KERNEL / "runtime", installed / "runtime")
        shutil.copytree(SKILLS / "schemas", installed / "skills/schemas")
        for skill_id in skill_ids:
            shutil.copytree(PACKAGE.parent / skill_id, installed / "skills/packages" / skill_id)
        source_repo = next(parent for parent in PACKAGE.parents if (parent / ".git").exists())
        source_common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=source_repo, text=True, check=True, stdout=subprocess.PIPE).stdout.strip()
        runtime_state = self.repo / ".git/guru-team/python/active.json"
        runtime_state.parent.mkdir(parents=True)
        shutil.copy2(Path(source_common) / "guru-team/python/active.json", runtime_state)
        return installed

    def architecture(self, committed):
        """Invoke the actual Architecture wrapper at the current fixture range."""
        package = PACKAGE.parent / "guru-maintain-architecture-baseline"
        installed = self.install_fixture_packages(package.name)
        public = json.loads((package / "examples/public-input-impact.json").read_text())
        public.update(source_exit=committed["exit_id"], stage="branch_review", task_locator=committed["task_ref"], freshness_identity=committed["branch_review_commit"], committed_range={"base_ref": committed["base_ref"], "base_head": self.git("rev-parse", committed["base_ref"]), "review_head": committed["branch_review_commit"]})
        owner = {key: public[key] for key in ("schema_version", "profile", "mode", "continuation_id", "stage", "task_locator", "baseline", "constitution", "project_contract", "freshness_identity")}
        owner.update(input_sha256=hashlib.sha256(json.dumps(public, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest(), typed_exit="baseline_current", consumer={"kind": "workflow", "id": "guru-architecture-baseline-current-router"}, baseline_identity=public["baseline"]["identity"], constitution_identity=public["constitution"]["identity"], impact_kind="no_architecture_impact", impact_reason="The fixture changes task text only and retains all project boundaries.", promotion_state="no_change", ai_review_gate={"status": "passed", "reviewed_scope": "Fixture complete current committed range.", "evidence_summary": "Fixture-only authoring at the exact branch review range.", "findings": [], "conclusion": "Fixture no-impact projection."})
        result = subprocess.run(["bash", str(installed / "skills/packages" / package.name / "scripts/invoke.sh"), "--invocation", "-", "--json"], input=json.dumps({"public_input": public, "owner_result": owner}), cwd=self.repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def snapshot(self):
        return tuple(self.git(*args) for args in [("rev-parse", "HEAD", "HEAD^{tree}"), ("ls-files", "--stage"), ("status", "--porcelain=v1", "--untracked-files=all"), ("rev-list", "--count", "HEAD"), ("reflog", "--format=%H")])

    def test_real_reconcile_clean_reentry_and_initial_full_review(self):
        self.commit_dirty()
        self.reconcile()
        passed = self.phase2()
        self.assertEqual("unchanged", self.guard("post_check")["status"])
        # Original route still reproduces the exact clean-candidate failure.
        failed = self.prepare(passed, ok=False)
        self.assertEqual("schema_mismatch", failed["code"])
        self.assertIn("exact_stage_paths", failed["field_path"])
        hook_marker = self.repo / ".git/reentry-hook-ran"
        hook = self.repo / ".git/hooks/pre-commit"
        hook.write_text(f"#!/bin/sh\ntouch '{hook_marker}'\nexit 1\n")
        hook.chmod(0o755)
        before = self.snapshot()
        runtime_files = set((self.repo / ".trellis/.runtime").rglob("*.json"))
        output = self.reentry(passed)
        self.assertEqual(before, self.snapshot())
        self.assertFalse(hook_marker.exists())
        self.assertEqual("committed", output["exit_id"])
        self.assertEqual(self.git("rev-parse", "HEAD"), output["branch_review_commit"])
        self.assertEqual("unchanged", self.guard("post_commit")["status"])
        checkpoint = self.repo / ".trellis/.runtime/guru-team/owner-checkpoints" / Path(TASK).name / "phase2-check.json"
        self.assertFalse(checkpoint.exists())
        self.assertEqual(runtime_files - {checkpoint}, set((self.repo / ".trellis/.runtime").rglob("*.json")))
        self.assertFalse(list((self.repo / ".trellis/.runtime/guru-team/task-commit-plans").rglob("*.json")))
        # Only the earlier dirty invocation owns a receipt; reentry adds none.
        receipts = list((self.repo / ".trellis/.runtime/guru-team/task-commit-results").rglob("*.json"))
        self.assertEqual(1, len(receipts))
        # Base can move again after the clean candidate was handed off.
        # The actual Reconcile output still returns to fresh Phase2, then the
        # same TaskCommit owner verifies the newer integration candidate.
        hook.unlink()
        self.reconcile()
        passed = self.phase2()
        self.assertEqual("unchanged", self.guard("post_check")["status"])
        before = self.snapshot()
        output = self.reentry(passed)
        self.assertEqual(before, self.snapshot())
        self.assertEqual("unchanged", self.guard("post_commit")["status"])
        architecture = self.architecture(output)
        self.assertEqual("baseline_current", architecture["exit_id"])
        self.assertEqual("branch_review", architecture["stage"])
        self.assertEqual(output["branch_review_commit"], architecture["freshness_identity"])
        self.assertEqual(before, self.snapshot())
        public = {"profile": "branch_review", "mode": "workflow", "task_ref": output["task_ref"], "base_ref": output["base_ref"], "branch_review_commit": output["branch_review_commit"], "review_intent": "initial_review"}
        example = json.loads((PACKAGE.parent / "guru-review-branch/examples/review-gate.json").read_text())
        authoring = {key: example[key] for key in ("delivery_review", "candidate_classifications", "semantic_review", "verification_evidence")}
        self.call("guru-review-branch", "review-branch.sh", "--task", TASK, "--skill-input", self.write("review-public.json", public), "--semantic-review-file", self.write("review-authoring.json", authoring), "--typed-exit", "passed")
        review_checkpoint = self.repo / ".trellis/.runtime/guru-team/owner-checkpoints" / Path(TASK).name / "review-gate.json"
        captured = json.loads(review_checkpoint.read_text())
        self.assertEqual("initial_review", captured["review_intent"])
        self.assertEqual(self.git("rev-parse", "main"), captured["base_head"])
        self.assertEqual(output["branch_review_commit"], captured["review_commit"])
        self.assertEqual("passed", self.call("guru-review-branch", "check-review-gate.sh", "--task", TASK)["typed_exit"])
        reviewed = self.call("guru-review-branch", "invoke.sh", "--input", self.write("review-public.json", public))
        self.assertEqual("passed", reviewed["exit_id"])

    def test_dirty_increment_rejected_by_readonly_and_committed_by_existing_path(self):
        self.commit_dirty()
        passed = self.phase2()
        (self.repo / "task.txt").write_text("next task increment\n")
        self.assertEqual("worktree", self.reentry(passed, ok=False)["field_path"])
        before = int(self.git("rev-list", "--count", "HEAD"))
        output = self.commit_dirty()
        self.assertEqual(before + 1, int(self.git("rev-list", "--count", "HEAD")))
        self.assertEqual(output["branch_review_commit"], self.git("rev-parse", "HEAD"))

    def test_current_content_history_base_and_branch_mismatch_reject(self):
        self.commit_dirty()
        passed = self.phase2()
        (self.repo / "task.txt").write_text("new committed content\n")
        self.git("commit", "-qam", "new content")
        self.assertEqual("phase2_result", self.reentry(passed, ok=False)["field_path"])
        passed = self.phase2()
        # A real executable-mode commit changes HEAD while Phase2's existing
        # worktree-content identity continues to match the same file bytes.
        (self.repo / "task.txt").chmod(0o755)
        self.git("commit", "-qam", "make fixture task executable")
        self.assertEqual("phase2_commit_anchor", self.reentry(passed, ok=False)["field_path"])
        passed = self.phase2()
        self.git("switch", "main")
        (self.repo / "base.txt").write_text("new base\n")
        self.git("commit", "-qam", "base evolution")
        self.git("switch", "feature/reentry")
        self.assertEqual("base_ref", self.reentry(passed, ok=False)["field_path"])
        self.git("switch", "-qc", "feature/other")
        self.assertEqual("worktree", self.reentry(passed, ok=False)["field_path"])

    def test_standalone_uses_fresh_phase2_and_consumes_checkpoint_once(self):
        self.commit_dirty()
        passed = self.phase2(mode="standalone")
        before = self.snapshot()
        self.assertEqual("phase2_commit_anchor", self.reentry(passed, ok=False)["field_path"])
        output = self.reentry(passed, mode="standalone")
        self.assertEqual("committed", output["exit_id"])
        self.assertEqual(before, self.snapshot())
        self.assertEqual("phase2_result", self.reentry(passed, mode="standalone", ok=False)["field_path"])

    def test_no_task_range_cannot_become_a_committed_candidate(self):
        self.commit_dirty()
        passed = self.phase2()
        self.git("switch", "main")
        self.git("merge", "--ff-only", "feature/reentry")
        self.git("switch", "feature/reentry")
        before = self.snapshot()
        self.assertEqual("base_ref", self.reentry(passed, ok=False)["field_path"])
        self.assertEqual(before, self.snapshot())

    def test_active_merge_nonpass_and_mutually_exclusive_arguments(self):
        self.commit_dirty()
        passed = self.phase2()
        before = self.snapshot()
        self.assertEqual("blocked", self.reentry(passed, status="blocked")["exit_id"])
        self.assertEqual(before, self.snapshot())
        self.assertEqual("revision-required", self.reentry(passed, status="revision-required")["exit_id"])
        self.assertEqual("conflicting_arguments", self.reentry(passed, ok=False, extra=("--invocation", "-"))["code"])
        self.git("switch", "main")
        (self.repo / "base.txt").write_text("merge base\n")
        self.git("commit", "-qam", "advance")
        self.git("switch", "feature/reentry")
        self.git("merge", "--no-commit", "--no-ff", "main")
        self.assertEqual("git_operation_state", self.reentry(passed, ok=False)["field_path"])

    def test_eval_recipe_and_native_boundary_use_actual_public_outputs(self):
        from adapters.eval.eval_constants import OWNER_INVOCATION
        from adapters.eval.native_adapter import start_public_runtime_boundary
        from adapters.eval.owner_runtime import compose_production_owner_command_runtime
        from adapters.eval.production_fixtures import production_committed_reentry_invocation

        installed = self.install_fixture_packages("guru-check-task", "guru-activate-task", "guru-create-task-commit")
        target = installed / "scripts/bash/run-skill-command.sh"
        durable = self.repo / "docs/requirements.md"
        durable.write_text("# Fixture requirement\nThe task changes fixture text.\n")
        self.phase2()
        checked = self.call("guru-check-task", "check-phase2-check.sh", "--task", TASK)

        def write_json(path, value):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value))

        runtime = SimpleNamespace(write_json=write_json, read_json=lambda path: json.loads(path.read_text()), diff_base_ref=lambda repo, branch: branch, changed_files=lambda repo, revision: self.git("diff", "--name-only", revision).splitlines(), git_status_paths=lambda repo: [line[3:] for line in subprocess.run(["git", "status", "--short", "--untracked-files=all"], cwd=repo, text=True, check=True, stdout=subprocess.PIPE).stdout.splitlines()])
        compose_production_owner_command_runtime(target, runtime)
        public = json.loads((PACKAGE / "evals/files/committed-reentry-input.json").read_text())
        production_committed_reentry_invocation(runtime, self.repo, self.repo / TASK, checked, public)
        envelope = json.loads((self.repo / OWNER_INVOCATION).read_text())
        self.assertEqual(self.git("rev-parse", "HEAD"), envelope["public_input"]["phase2_commit_anchor"])
        self.assertEqual("", self.git("status", "--porcelain"))
        before = self.snapshot()
        execution_root = self.inputs / "native-boundary"
        execution_root.mkdir()
        projection = self.inputs / "model-package"
        package = installed / "skills/packages/guru-create-task-commit"
        boundary, thread, stop = start_public_runtime_boundary(execution_root, target, package, projection, projection / "scripts/invoke.sh", {})
        try:
            result = subprocess.run([str(boundary), "--package-root", str(projection), "--committed-reentry", "-", "--json"], text=True, capture_output=True, timeout=30)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual("committed", output["exit_id"])
            self.assertEqual(envelope["public_input"]["phase2_commit_anchor"], output["branch_review_commit"])
            self.assertEqual(before, self.snapshot())
        finally:
            stop.set()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
