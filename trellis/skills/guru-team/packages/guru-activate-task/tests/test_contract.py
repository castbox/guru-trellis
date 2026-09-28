from __future__ import annotations

import hashlib
import importlib.util
import json
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
from runtime.task_lifecycle.session_adapter import resolve_session


PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("activate_task", PACKAGE / "runtime/invoke.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ActivateTaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-q", "-b", "main")
        task = self.root / ".trellis/tasks/demo"
        task.mkdir(parents=True)
        self.task_file = task / "task.json"
        self.task_file.write_text(json.dumps({"id": "demo", "status": "planning", "lifecycle_generation": 0, "base_branch": "main"}), encoding="utf-8")
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
        self.planning_digest = self.write_planning_approval()
        self.payload = {
            "profile": "task_activation", "action": "activate", "mode": "workflow",
            "activation": {
                "task_id": "demo", "task_ref": ".trellis/tasks/demo", "lifecycle_generation": 0,
                "planning_result_id": f"planning:{self.planning_digest}", "selected_base_ref": "main",
                "continuity": {"kind": "base_current", "task_head": self.head, "base_head": self.head},
                "session_mode": "explicit_task_mode",
            },
        }

    def write_planning_approval(self) -> str:
        task_ref = ".trellis/tasks/demo"
        paths = [f"{task_ref}/{name}" for name in ("prd.md", "design.md", "implement.md")]
        files = [
            {"path": path, "content_sha256": hashlib.sha256((self.root / path).read_bytes()).hexdigest()}
            for path in paths
        ]
        digest = hashlib.sha256(
            json.dumps(files, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        ).hexdigest()
        source = PACKAGE.parent / "guru-approve-task-plan/examples/planning-approval.json"
        approval = json.loads(source.read_text(encoding="utf-8"))
        approval.update({
            "task_ref": task_ref,
            "planning_paths": paths,
            "reviewed_content_sha256": digest,
        })
        checkpoint = self.root / ".trellis/.runtime/guru-team/owner-checkpoints/demo/planning-approval.json"
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        checkpoint.write_text(json.dumps(approval), encoding="utf-8")
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
        stale = json.loads(json.dumps(self.payload))
        stale["activation"]["continuity"]["task_head"] = "a" * 40
        self.assertEqual(self.invoke(stale)["exit_id"], "refresh_review")
        self.assertEqual(json.loads(self.task_file.read_text())["status"], "planning")

    def test_activation_rejects_stale_planning_identity(self) -> None:
        stale = json.loads(json.dumps(self.payload))
        stale["activation"]["planning_result_id"] = f"planning:{'b' * 64}"
        self.assertEqual(self.invoke(stale)["exit_id"], "refresh_review")
        checkpoint = self.root / ".trellis/.runtime/guru-team/owner-checkpoints/demo/planning-approval.json"
        checkpoint.unlink()
        (self.root / ".trellis/tasks/demo/design.md").write_text("changed\n", encoding="utf-8")
        self.assertEqual(self.invoke(self.payload)["exit_id"], "refresh_review")

    def approved_projection(self) -> dict:
        checkpoint = self.root / ".trellis/.runtime/guru-team/owner-checkpoints/demo/planning-approval.json"
        checkpoint.unlink()
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
        public_input.write_text(json.dumps({"mode": "workflow", "task_ref": ".trellis/tasks/demo"}), encoding="utf-8")
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
        self.assertEqual(approved, {
            "exit_id": "approved", "task_ref": ".trellis/tasks/demo",
            "planning_result_id": f"planning:{self.planning_digest}",
        })
        self.assertFalse(checkpoint.exists())
        self.payload["activation"]["planning_result_id"] = approved["planning_result_id"]
        return approved

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
