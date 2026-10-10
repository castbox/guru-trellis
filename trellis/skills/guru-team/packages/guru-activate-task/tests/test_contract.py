from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.session_adapter import bind_session, resolve_session
from runtime.task_lifecycle.rebind import execute_rebind, prepare_rebind


PACKAGE = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PACKAGE.parents[4]
SPEC = importlib.util.spec_from_file_location("activate_task", PACKAGE / "runtime/invoke.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
from execution_result import execution_result_path, retire_execution_result


class ActivateTaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-q", "-b", "main")
        task = self.root / ".trellis/tasks/demo"
        task.mkdir(parents=True)
        self.task_file = task / "task.json"
        self.task_file.write_text(json.dumps({
            "id": "demo", "name": "demo", "status": "planning", "lifecycle_generation": 0,
            "source": {"kind": "no_issue"}, "title": "Demo", "description": "Reviewed scope",
            "dev_type": None, "scope": None, "package": None, "priority": "P2",
            "createdAt": "2026-10-10", "completedAt": None, "base_branch": "main",
            "worktree_path": None, "commit": None, "pr_url": None, "children": [],
            "parent": None, "relatedFiles": [], "notes": "", "meta": {},
        }), encoding="utf-8")
        (self.root / ".gitignore").write_text(".trellis/.runtime/\n", encoding="utf-8")
        for name in ("prd.md", "design.md", "implement.md"):
            (task / name).write_text(f"# {name}\n", encoding="utf-8")
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture")
        self.head = self.git("rev-parse", "HEAD")
        repository = inspect_repository(self.root)
        self.key = TaskLifecycleKey("demo", 0)
        binding = BranchBindingStore(repository).establish(self.key, "main")
        ResourceLedgerStore(repository).establish_current(
            self.key, binding_revision=0,
            branch_name="main", branch_ownership="caller_owned", worktree_ownership="not_applicable",
        )
        self.planning_digest = self.planning_identity()
        self.payload = {
            "profile": "task_activation", "action": "activate", "mode": "workflow",
            "activation": {
                "task_id": "demo", "task_ref": ".trellis/tasks/demo", "lifecycle_generation": 0,
                "planning_result_id": f"planning:{self.planning_digest}", "selected_base_ref": "main",
                "continuity": {"kind": "base_current", "task_head": self.head, "base_head": self.head},
                "session_mode": "explicit_task_mode",
            },
        }

    def planning_identity(self) -> str:
        task_ref = ".trellis/tasks/demo"
        paths = [f"{task_ref}/{name}" for name in ("prd.md", "design.md", "implement.md")]
        files = [
            {"path": path, "content_sha256": hashlib.sha256((self.root / path).read_bytes()).hexdigest()}
            for path in paths
        ]
        digest = hashlib.sha256(
            json.dumps(files, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        ).hexdigest()
        return digest

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def invoke(self, payload: dict) -> dict:
        class NoContextPort:
            @staticmethod
            def resolve_context_key(platform_input=None, platform=None):
                return None

            @staticmethod
            def repository_facts(root):
                return SimpleNamespace(common_dir=root / ".git", worktrees=(root,))

            @staticmethod
            def resolve_task_identity(facts, task_id, lifecycle_generation):
                workspace = facts.worktrees[0]
                return SimpleNamespace(task_ref=".trellis/tasks/demo", workspace=workspace,
                                       task_path=workspace / ".trellis/tasks/demo")

        with patch.object(MODULE, "_official_port", return_value=NoContextPort()):
            output = MODULE.invoke(self.root, payload)
        validate_json(output, PACKAGE / "schemas/public-output.schema.json", "output")
        return output

    def test_activation_requires_live_session_route_and_rechecks_recovery(self) -> None:
        old_checkout = Path(self.temporary.name) / "old-checkout"
        self.git("worktree", "add", "-q", "-b", "codex/old-copy", str(old_checkout), "HEAD")

        class SessionPort:
            def __init__(self, old):
                self.old = old
                self.current = None
                self.writes = 0

            def resolve_context_key(self, platform_input=None, platform=None):
                return "codex-test"

            def repository_facts(self, root):
                return SimpleNamespace(common_dir=root / ".git", worktrees=(root, self.old))

            def session_path(self, root, key, facts):
                return facts.common_dir / "sessions" / f"{key}.json"

            def record_exists(self, path):
                return self.current is not None

            def read_record(self, path, root, facts):
                return SimpleNamespace(data=self.current, task_id=self.current["task_id"],
                                       lifecycle_generation=self.current["lifecycle_generation"])

            def resolve_task_identity(self, facts, task_id, lifecycle_generation):
                if len(facts.worktrees) != 1:
                    raise ValueError("ambiguous_task_identity")
                refs = {"demo": ".trellis/tasks/demo", "another-task": ".trellis/tasks/another-task"}
                workspace = facts.worktrees[0]
                return SimpleNamespace(task_ref=refs[task_id], workspace=workspace,
                                       task_path=workspace / refs[task_id])

            def write_record(self, path, data, root):
                self.writes += 1

        port = SessionPort(old_checkout)
        bound = json.loads(json.dumps(self.payload))
        bound["activation"]["session_mode"] = "session_bound"

        def run(data, checkout=None):
            with patch.object(MODULE, "_official_port", return_value=port):
                return MODULE.invoke(checkout or self.root, data)

        self.assertEqual(run(bound), {"exit_id": "blocked", "reason_code": "activation_session_mismatch"})
        port.current = {"schema_version": 2, "task_id": "another-task", "lifecycle_generation": 0}
        self.assertEqual(run(bound), {"exit_id": "blocked", "reason_code": "activation_session_mismatch"})
        self.assertEqual(run(self.payload), {"exit_id": "blocked", "reason_code": "activation_session_mismatch"})
        self.assertEqual(json.loads(self.task_file.read_text())["status"], "planning")

        port.current = {"schema_version": 2, "task_id": "demo", "lifecycle_generation": 0}
        self.assertEqual(resolve_session(port, self.root).status, "session_invalid")
        self.assertEqual(run(bound, old_checkout),
                         {"exit_id": "blocked", "reason_code": "activation_checkout_mismatch"})
        self.assertEqual(json.loads((old_checkout / ".trellis/tasks/demo/task.json").read_text())["status"], "planning")
        self.assertEqual(run(bound)["exit_id"], "activated")
        after = self.task_file.read_bytes()
        self.assertEqual(run({**bound, "action": "recover_activation"}, old_checkout),
                         {"exit_id": "blocked", "reason_code": "activation_checkout_mismatch"})
        self.assertEqual(json.loads((old_checkout / ".trellis/tasks/demo/task.json").read_text())["status"], "planning")
        port.current = {"schema_version": 2, "task_id": "another-task", "lifecycle_generation": 0}
        self.assertEqual(run({**bound, "action": "recover_activation"}),
                         {"exit_id": "blocked", "reason_code": "activation_session_mismatch"})
        self.assertEqual(self.task_file.read_bytes(), after)
        self.assertEqual(port.writes, 0)

    def test_activation_status_only_and_read_only_recovery(self) -> None:
        before = json.loads(self.task_file.read_text(encoding="utf-8"))
        self.assertEqual(self.invoke(self.payload)["exit_id"], "activated")
        after = self.task_file.read_bytes()
        self.assertEqual(json.loads(after), {**before, "status": "in_progress"})
        self.assertNotIn("branch", json.loads(after))
        recovery = {**self.payload, "action": "recover_activation", "mode": "standalone"}
        self.assertEqual(self.invoke(recovery)["exit_id"], "activated")
        self.assertEqual(self.task_file.read_bytes(), after)
        self.assertEqual(self.invoke(self.payload), {"exit_id": "invalid_task_state", "reason_code": "activation_status_mismatch"})

    def test_recovery_before_mutation_and_stale_head(self) -> None:
        recovery = {**self.payload, "action": "recover_activation"}
        self.assertEqual(self.invoke(recovery)["exit_id"], "invalid_task_state")
        self.assertEqual(json.loads(self.task_file.read_text())["status"], "planning")
        (self.root / "README.md").write_text("ordinary commit after reviewed continuity\n")
        self.git("add", "README.md")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "normal follow-on")
        self.assertEqual(self.invoke(self.payload)["exit_id"], "refresh_review")
        self.assertEqual(json.loads(self.task_file.read_text())["status"], "planning")

    def test_activation_rejects_stale_planning_identity(self) -> None:
        (self.root / ".trellis/tasks/demo/design.md").write_text("changed\n", encoding="utf-8")
        self.assertEqual(self.invoke(self.payload)["exit_id"], "refresh_review")

    def approved_projection(self) -> dict:
        checkpoint = self.root / ".trellis/.runtime/guru-team/owner-checkpoints/demo/planning-approval.json"
        approval_package = PACKAGE.parent / "guru-approve-task-plan"
        complete = json.loads((approval_package / "examples/planning-approval.json").read_text(encoding="utf-8"))
        authoring = {key: complete[key] for key in (
            "mode", "authority_refs", "delivery_policy", "docs_ssot_plan",
            "semantic_review", "typed_exit", "consumer", "reason",
        )}
        authoring["mode"] = "workflow"
        owner_input = self.root / "owner-input.json"
        owner_input.write_text(json.dumps(authoring), encoding="utf-8")
        public_input = self.root / "public-input.json"
        profile = "initial_review" if json.loads(self.task_file.read_text())["status"] == "planning" else "revision_reentry"
        public = {"profile": profile, "mode": "workflow", "task_ref": ".trellis/tasks/demo", "source_exit": "planning_ready" if profile == "initial_review" else "revision_required"}
        if profile == "revision_reentry":
            public["reentry_reason"] = "task_local_revision"
        public_input.write_text(json.dumps(public), encoding="utf-8")
        for script, arguments in (
            ("record-planning-approval.sh", ["--task", ".trellis/tasks/demo", "--input", str(owner_input)]),
            ("check-planning-approval.sh", ["--task", ".trellis/tasks/demo"]),
            ("invoke.sh", ["--input", str(public_input), "--owner-result", str(checkpoint)]),
        ):
            result = subprocess.run(
                [str(approval_package / "scripts" / script), "--root", str(self.root), *arguments],
                cwd=self.root, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
        approved = json.loads(result.stdout)
        self.planning_digest = self.planning_identity()
        self.assertEqual(approved, {
            "exit_id": "approved", "task_ref": ".trellis/tasks/demo",
            "planning_result_id": f"planning:{self.planning_digest}",
        })
        self.assertFalse(checkpoint.exists())
        self.payload["activation"]["planning_result_id"] = approved["planning_result_id"]
        return approved

    @staticmethod
    def recovery_input(payload: dict) -> dict:
        # Public recovery intentionally carries no planning token or continuity.
        return {"profile": "task_activation", "action": "recover_execution", "mode": payload["mode"],
                "activation": {key: payload["activation"][key] for key in (
                    "task_id", "task_ref", "lifecycle_generation", "session_mode",
                )}}

    def copy_official(self) -> Path:
        common = self.root / ".trellis/scripts/common"
        if not common.exists():
            shutil.copytree(SOURCE_ROOT / ".trellis/scripts/common", common)
        return common

    def public_invoke(self, payload: dict, *, context_key: str | None = None) -> dict:
        # Use the real Fixed Fork session API and the actual shell/managed
        # dispatcher. No mocked session port or caller-authored result record.
        common = self.copy_official()
        environment = os.environ.copy()
        active_source = (common / "active_task.py").read_text()
        import re
        for name in re.findall(r'"([A-Z][A-Z0-9_]+)"', active_source):
            environment.pop(name, None)
        if context_key:
            environment["TRELLIS_CONTEXT_ID"] = context_key
        result = subprocess.run(
            [str(PACKAGE / "scripts/invoke.sh"), "--root", str(self.root), "--input", "-"],
            cwd=self.root, input=json.dumps(payload), text=True, capture_output=True, env=environment,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def control_bytes(self) -> dict:
        return {str(path.relative_to(self.root)): path.read_bytes()
                for path in (self.root / ".git/guru-team").rglob("*.json")}

    def test_public_chain_active_replan_resume_and_same_result_recovery(self) -> None:
        self.approved_projection()
        self.assertEqual(self.public_invoke(self.payload)["exit_id"], "activated")
        checkpoint = execution_result_path(self.root, ".trellis/tasks/demo")
        first_checkpoint = checkpoint.read_bytes()
        after_activation = self.task_file.read_bytes()
        self.assertEqual(self.public_invoke({**self.payload, "action": "recover_activation"})["exit_id"], "activated")
        self.assertEqual(checkpoint.read_bytes(), first_checkpoint)
        self.assertEqual(self.task_file.read_bytes(), after_activation)
        (self.root / ".trellis/tasks/demo/design.md").write_text("# Updated accepted active plan\n")
        self.approved_projection()
        before = self.task_file.read_bytes()
        controls = self.control_bytes()
        branches = self.git("show-ref", "--heads")
        worktrees = self.git("worktree", "list", "--porcelain")
        resume = {**self.payload, "action": "resume_execution"}
        expected = {"exit_id": "execution_resumed", "task_id": "demo", "task_ref": ".trellis/tasks/demo", "lifecycle_generation": 0}
        self.assertEqual(self.public_invoke(resume), expected)
        completed = checkpoint.read_bytes()
        self.assertEqual(json.loads(completed)["operation"], "resume_execution")
        # Deliberately discard a real invocation result; recovery must derive
        # only the same completed result and remain byte-for-byte read-only.
        self.assertEqual(self.public_invoke({**resume, "action": "recover_activation"}), {"exit_id": "blocked", "reason_code": "execution_operation_mismatch"})
        recover = self.recovery_input(resume)
        del resume
        self.payload.clear()
        (self.root / "owner-input.json").unlink()
        (self.root / "public-input.json").unlink()
        self.assertNotIn("planning_result_id", recover["activation"])
        self.assertNotIn("continuity", recover["activation"])
        self.assertEqual(self.public_invoke(recover), expected)
        self.assertEqual(self.task_file.read_bytes(), before)
        self.assertEqual(checkpoint.read_bytes(), completed)
        self.assertEqual(self.control_bytes(), controls)
        self.assertEqual(self.git("show-ref", "--heads"), branches)
        self.assertEqual(self.git("worktree", "list", "--porcelain"), worktrees)

    def test_resume_requires_active_task_and_recovery_requires_completed_resume(self) -> None:
        self.approved_projection()
        resume = {**self.payload, "action": "resume_execution"}
        self.assertEqual(self.public_invoke(resume)["exit_id"], "invalid_task_state")
        self.assertEqual(self.public_invoke(self.recovery_input(resume))["exit_id"], "invalid_task_state")
        self.public_invoke(self.payload)
        self.assertEqual(self.public_invoke(self.recovery_input(resume)), {"exit_id": "blocked", "reason_code": "execution_operation_mismatch"})
        self.assertTrue(retire_execution_result(self.root, task_ref=".trellis/tasks/demo"))
        self.assertEqual(self.public_invoke(self.recovery_input(resume)), {"exit_id": "blocked", "reason_code": "execution_result_missing"})
        self.assertEqual(self.public_invoke({**resume, "action": "recover_activation"})["exit_id"], "activated")

    def test_recovery_and_retirement_retain_normal_stale_planning(self) -> None:
        self.approved_projection()
        self.public_invoke(self.payload)
        (self.root / ".trellis/tasks/demo/design.md").write_text("# Active replan\n")
        self.approved_projection()
        resume = {**self.payload, "action": "resume_execution"}
        self.public_invoke(resume)
        checkpoint = execution_result_path(self.root, ".trellis/tasks/demo")
        completed = checkpoint.read_bytes()
        metadata = self.task_file.read_bytes()
        (self.root / ".trellis/tasks/demo/prd.md").write_text("# Ordinary later requirements revision\n")
        self.assertEqual(self.public_invoke(self.recovery_input(resume))["exit_id"], "refresh_review")
        self.assertFalse(retire_execution_result(self.root, task_ref=".trellis/tasks/demo"))
        self.assertEqual(checkpoint.read_bytes(), completed)
        self.assertEqual(self.task_file.read_bytes(), metadata)
        self.approved_projection()
        # A fresh plan cannot turn the old completed result into new execution.
        self.assertEqual(self.public_invoke(self.recovery_input(self.payload))["exit_id"], "refresh_review")
        self.assertEqual(checkpoint.read_bytes(), completed)

    def test_recovery_and_retirement_retain_normal_continuity_change(self) -> None:
        self.approved_projection()
        self.public_invoke(self.payload)
        resume = {**self.payload, "action": "resume_execution"}
        self.public_invoke(resume)
        checkpoint = execution_result_path(self.root, ".trellis/tasks/demo")
        completed = checkpoint.read_bytes()
        (self.root / "README.md").write_text("ordinary next commit\n")
        self.git("add", "README.md")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "next")
        self.assertEqual(self.public_invoke(self.recovery_input(resume))["exit_id"], "refresh_review")
        self.assertFalse(retire_execution_result(self.root, task_ref=".trellis/tasks/demo"))
        self.assertEqual(checkpoint.read_bytes(), completed)

    def test_recovery_rereads_real_official_session_after_context_change(self) -> None:
        self.copy_official()
        official = MODULE._official_port(self.root)
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "test-demo-current"}):
            bound = bind_session(official, self.root, {"task_id": self.key.task_id, "lifecycle_generation": self.key.lifecycle_generation})
        self.assertEqual(bound.status, "session_bound")
        self.approved_projection()
        self.payload["activation"]["session_mode"] = "session_bound"
        self.public_invoke(self.payload, context_key="test-demo-current")
        resume = {**self.payload, "action": "resume_execution"}
        self.public_invoke(resume, context_key="test-demo-current")
        checkpoint = execution_result_path(self.root, ".trellis/tasks/demo")
        completed = checkpoint.read_bytes()
        before = self.task_file.read_bytes()
        self.assertEqual(self.public_invoke(self.recovery_input(resume), context_key="test-demo-current")["exit_id"], "execution_resumed")
        self.assertEqual(self.public_invoke(self.recovery_input(resume), context_key="test-new-unbound-session"), {"exit_id": "blocked", "reason_code": "activation_session_mismatch"})
        self.assertEqual(checkpoint.read_bytes(), completed)
        self.assertEqual(self.task_file.read_bytes(), before)

    def test_completed_execution_detects_formal_rebind_revision(self) -> None:
        self.copy_official()
        self.approved_projection()
        self.public_invoke(self.payload)
        # A supported rebind operates on a clean current task artifact.
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "current active task")
        self.payload["activation"]["continuity"] = {"kind": "base_current", "task_head": self.git("rev-parse", "HEAD"), "base_head": self.git("rev-parse", "main")}
        self.approved_projection()
        resume = {**self.payload, "action": "resume_execution"}
        self.public_invoke(resume)
        # Authoring input files are test transport, not task work.
        (self.root / "owner-input.json").unlink()
        (self.root / "public-input.json").unlink()
        self.git("add", ".")
        # Removing the now-tracked transport files is ordinary fixture work;
        # commit it before recording the final clean execution continuity.
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "retire fixture transport")
        resume["activation"]["continuity"] = {"kind": "base_current", "task_head": self.git("rev-parse", "HEAD"), "base_head": self.git("rev-parse", "main")}
        self.public_invoke(resume)
        checkpoint = execution_result_path(self.root, ".trellis/tasks/demo")
        completed = checkpoint.read_bytes()
        metadata = self.task_file.read_bytes()
        repository = inspect_repository(self.root)
        store, ledger = BranchBindingStore(repository), ResourceLedgerStore(repository)
        plan = prepare_rebind(repository, store, ledger, route="same_checkout_new_ref", key=self.key, task_ref=".trellis/tasks/demo", expected_status="in_progress", current_checkout=self.root, target_branch_name="codex/demo-rebound")
        result = execute_rebind(repository, store, ledger, plan)
        self.assertEqual(result.binding.binding_revision, 1)
        self.assertEqual(self.public_invoke(self.recovery_input(resume))["exit_id"], "refresh_review")
        self.assertFalse(retire_execution_result(self.root, task_ref=".trellis/tasks/demo"))
        self.assertEqual(checkpoint.read_bytes(), completed)
        self.assertEqual(self.task_file.read_bytes(), metadata)

    def test_cross_repository_source_and_no_issue_identity_survive_execution(self) -> None:
        metadata = json.loads(self.task_file.read_text())
        metadata["source"] = {"kind": "issue", "repo_ref": "castbox/ai-chat-roleplay-backend", "number": 148, "disposition": "exact_source"}
        self.task_file.write_text(json.dumps(metadata))
        self.approved_projection()
        self.public_invoke(self.payload)
        active = self.task_file.read_bytes()
        self.approved_projection()
        self.public_invoke({**self.payload, "action": "resume_execution"})
        self.assertEqual(self.task_file.read_bytes(), active)
        self.assertEqual(json.loads(active)["source"], metadata["source"])
        self.assertFalse({"coordination", "related_work", "parent_issue"}.intersection(json.loads(active)))

    def test_approved_projection_activates_after_producer_retires_checkpoint(self) -> None:
        self.approved_projection()
        self.assertEqual(self.invoke(self.payload)["exit_id"], "activated")

    def test_approval_projection_rejects_changed_plan_after_checkpoint_retirement(self) -> None:
        self.approved_projection()
        (self.root / ".trellis/tasks/demo/design.md").write_text("changed after approval\n", encoding="utf-8")
        self.assertEqual(self.invoke(self.payload)["exit_id"], "refresh_review")
        self.assertEqual(json.loads(self.task_file.read_text(encoding="utf-8"))["status"], "planning")


if __name__ == "__main__":
    unittest.main()
