from __future__ import annotations

import json
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore

from runtime import schema
from runtime.delivery_projection.tests.upstream_fixture import install_common, public_task, scripts_source
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref, official_session_port
from runtime.delivery_projection.tests.test_installed_projection import DECLARATION, OWNERS
from runtime.io import CommandError
from runtime.task_lifecycle.checkout_resolution import canonical_head_ref
from runtime.task_lifecycle.identity import resolve_task_id

PACKAGE = Path(__file__).resolve().parents[1]


def current_task(status: str, generation: int = 0) -> dict:
    return public_task({
        "id": "demo", "name": "demo", "lifecycle_generation": generation,
        "source": {"kind": "no_issue"}, "title": "Demo",
        "description": "Reviewed task", "status": status,
        "dev_type": None, "scope": None, "package": None, "priority": "P2",
        "createdAt": "2026-09-20", "completedAt": None,
        "base_branch": "main", "worktree_path": None, "commit": None,
        "pr_url": None, "children": [], "parent": None,
        "relatedFiles": [], "notes": "", "meta": {},
    })


class EnsureCheckoutTests(unittest.TestCase):
    def test_binding_then_unique_checkout_resolution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install_common(root)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
            task = root / ".trellis/tasks/demo"
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps(current_task("in_progress")), encoding="utf-8")
            subprocess.run(["git", "add", ".trellis/tasks/demo/task.json"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"],
                cwd=root, check=True,
            )
            repository = inspect_repository(root)
            key = TaskLifecycleKey("demo", 0)
            self.assertEqual(resolve_task_id(root, "demo").task_ref, ".trellis/tasks/demo")
            import importlib.util
            spec = importlib.util.spec_from_file_location("ensure_checkout", PACKAGE / "runtime/invoke.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            payload = {"profile": "delivery_active_task", "mode": "standalone", "task_id": "demo", "lifecycle_generation": 0}
            self.assertEqual(module.invoke(root, payload)["exit_id"], "binding_required")
            binding = BranchBindingStore(repository).establish(key, "main")
            self.assertEqual(module.invoke(root, payload)["exit_id"], "binding_required")
            ResourceLedgerStore(repository).establish_current(
                key, binding_revision=0,
                branch_name="main", branch_ownership="caller_owned", worktree_ownership="not_applicable",
            )
            resolved = module.invoke(root, payload)
            self.assertEqual(resolved["exit_id"], "checkout_resolved", resolved)
            self.assertEqual(resolved["checkout_path"], str(root.resolve()))
            self.assertEqual(canonical_head_ref("main"), binding.branch_ref)
            schema.validate_json(resolved, PACKAGE / "schemas/public-output.schema.json", "output")

    def test_stale_generation_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install_common(root)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
            task = root / ".trellis/tasks/demo"
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps(current_task("planning", 1)), encoding="utf-8")
            subprocess.run(["git", "add", ".trellis/tasks/demo/task.json"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"],
                cwd=root, check=True,
            )
            repository = inspect_repository(root)
            key = TaskLifecycleKey("demo", 0)
            binding = BranchBindingStore(repository).establish(key, "main")
            ResourceLedgerStore(repository).establish_current(
                key, binding_revision=0,
                branch_name="main", branch_ownership="caller_owned", worktree_ownership="not_applicable",
            )
            import importlib.util
            spec = importlib.util.spec_from_file_location("ensure_checkout_stale", PACKAGE / "runtime/invoke.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            payload = {"profile": "delivery_active_task", "mode": "workflow", "task_id": "demo", "lifecycle_generation": 0}
            self.assertEqual(module.invoke(root, payload), {"exit_id": "invalid_task_state", "reason_code": "task_identity_stale"})

    def test_new_task_in_linked_checkout_resolves_from_source_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install_common(root)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
            (root / "README.md").write_text("source\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "base"],
                cwd=root, check=True,
            )
            linked = root / "linked"
            subprocess.run(["git", "worktree", "add", "-q", "-b", "task-branch", str(linked)], cwd=root, check=True)
            task = linked / ".trellis/tasks/demo"
            task.mkdir(parents=True)
            (task / "task.json").write_text(
                json.dumps(current_task("planning")), encoding="utf-8"
            )
            self.assertFalse((root / ".trellis/tasks/demo/task.json").exists())
            repository = inspect_repository(root)
            key = TaskLifecycleKey("demo", 0)
            binding = BranchBindingStore(repository).establish(key, "task-branch")
            ResourceLedgerStore(repository).establish_current(
                key, binding_revision=0,
                branch_name="task-branch", branch_ownership="guru_owned", worktree_ownership="guru_owned",
            )
            import importlib.util
            spec = importlib.util.spec_from_file_location("ensure_checkout_linked", PACKAGE / "runtime/invoke.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            payload = {"profile": "delivery_active_task", "mode": "workflow", "task_id": "demo", "lifecycle_generation": 0}

            output = module.invoke(root, payload)
            self.assertEqual(output["exit_id"], "checkout_resolved", output)
            self.assertEqual(output["task_ref"], ".trellis/tasks/demo")
            self.assertEqual(output["checkout_path"], str(linked.resolve()))
            schema.validate_json(output, PACKAGE / "schemas/public-output.schema.json", "output")

            (task / "task.json").unlink()
            self.assertEqual(
                module.invoke(root, payload),
                {"exit_id": "invalid_task_state", "reason_code": "task_artifact_mismatch"},
            )

    def test_bound_branch_without_registered_checkout_requests_acquisition(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install_common(root)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
            task = root / ".trellis/tasks/demo"
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps(current_task("planning")), encoding="utf-8")
            subprocess.run(["git", "add", ".trellis/tasks/demo/task.json"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"],
                cwd=root, check=True,
            )
            subprocess.run(["git", "branch", "task-branch"], cwd=root, check=True)
            repository = inspect_repository(root)
            key = TaskLifecycleKey("demo", 0)
            binding = BranchBindingStore(repository).establish(key, "task-branch")
            ResourceLedgerStore(repository).establish_current(
                key, binding_revision=0,
                branch_name="task-branch", branch_ownership="caller_owned", worktree_ownership="not_applicable",
            )
            import importlib.util
            spec = importlib.util.spec_from_file_location("ensure_checkout_missing", PACKAGE / "runtime/invoke.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            output = module.invoke(root, {"profile": "delivery_active_task", "mode": "workflow", "task_id": "demo", "lifecycle_generation": 0})
            self.assertEqual(output["exit_id"], "checkout_required", output)
            schema.validate_json(output, PACKAGE / "schemas/public-output.schema.json", "output")


class CurrentContextTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        shutil.copytree(scripts_source(), self.root / ".trellis/scripts", ignore=shutil.ignore_patterns("__pycache__"))
        workflow = "[trellis-runtime-contract]\n" + json.dumps(DECLARATION) + "\n[/trellis-runtime-contract]\n"
        (self.root / ".trellis/workflow.md").write_text(workflow, encoding="utf-8")
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        self.task = self.root / ".trellis/tasks/demo"
        self.task.mkdir(parents=True)
        (self.task / "task.json").write_text(json.dumps(current_task("planning")), encoding="utf-8")
        (self.root / ".gitignore").write_text(".trellis/.runtime/\n", encoding="utf-8")
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture")
        self.repository = inspect_repository(self.root)
        self.key = TaskLifecycleKey("demo", 0)
        self.environment = patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "ensure-current-test"})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        spec = importlib.util.spec_from_file_location("ensure_current_context", PACKAGE / "runtime/invoke.py")
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.official = official_session_port(self.root)
        self.session_path = self.official.session_path(self.root, self.official.resolve_context_key(), self.official.repository_facts(self.root))

    def git(self, *arguments):
        return subprocess.run(["git", *arguments], cwd=self.root, check=True, capture_output=True, text=True).stdout

    def bind(self, generation=0):
        self.official.write_record(self.session_path, {
            "schema_version": 3, "task_id": "demo", "lifecycle_generation": generation, "delivery_id": None,
        }, self.root)

    def controls(self, branch="main"):
        binding = BranchBindingStore(self.repository).establish(self.key, branch)
        ResourceLedgerStore(self.repository).establish_current(
            self.key, binding_revision=binding.binding_revision, branch_name=branch,
            branch_ownership="caller_owned", worktree_ownership="not_applicable",
        )

    def snapshot(self):
        roots = (self.root / ".trellis", self.repository.common_dir)
        return {str(path): path.read_bytes() for directory in roots for path in directory.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts}

    def query(self):
        status = self.git("status", "--porcelain")
        before = self.snapshot()
        try:
            output = self.module.invoke(self.root, {"profile": "delivery_current_task", "mode": "workflow"})
            schema.validate_json(output, PACKAGE / "schemas/public-output.schema.json", "stdout")
            return output
        finally:
            self.assertEqual(before, self.snapshot())
            self.assertEqual(status, self.git("status", "--porcelain"))

    def test_bound_task_without_delivery_and_legacy_profile(self):
        self.bind()
        self.controls()
        output = self.query()
        self.assertEqual(output, {
            "exit_id": "current_context_ready", "task_id": "demo", "lifecycle_generation": 0,
            "task_ref": ".trellis/tasks/demo", "checkout_path": str(self.root),
        })
        explicit = self.module.invoke(self.root, {
            "profile": "delivery_active_task", "mode": "workflow", "task_id": "demo", "lifecycle_generation": 0,
        })
        self.assertEqual(explicit, {**output, "exit_id": "checkout_resolved"})
        interface = json.loads((PACKAGE / "interface.json").read_text())
        schema.validate_json(output, PACKAGE / interface["public_contracts"]["consumer_inputs"][0]["contract"]["path"], "consumer")

    def delivery(self):
        projection = DeliveryProjection(self.root, ".trellis/tasks/demo")
        (self.task / "prd.md").write_text("Accepted scope\n", encoding="utf-8")
        scope = authority_ref(self.task / "prd.md", self.root)
        projection.scope(scope)
        key = {"task_id": "demo", "lifecycle_generation": 0, "delivery_id": str(uuid.uuid4())}
        projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": key,
                          "owner_role": "creation", "owner_id": OWNERS["creation"],
                          "scope_ref": {"authority": scope, "anchors": ["AC1"]}, "profile": "pull_request"})
        projection.select(key)
        plan = projection.planning_directory(key) / "design.md"
        plan.write_text("Reviewed plan\n", encoding="utf-8")
        result = {"result_id": "planning-demo", "owner_role": "planning", "owner_id": OWNERS["planning"],
                  "outcome": "accepted", "scope_ref": projection.resolve(key)["scope_ref"],
                  "plan_ref": authority_ref(plan, self.root), "candidate": None, "predecessor_result_id": None,
                  "obligations": [], "evidence": [scope] * 1000}
        projection.apply({"api_version": "1.0", "operation": "record_gate", "key": key,
                          "owner_role": "planning", "owner_id": OWNERS["planning"],
                          "expected_phase": "planning", "result": result})
        return projection, key

    def test_selected_delivery_large_results_are_not_forwarded(self):
        self.bind()
        self.controls()
        projection, key = self.delivery()
        output = self.query()
        self.assertEqual(set(output), {"exit_id", "task_id", "task_ref", "lifecycle_generation", "checkout_path", "current_delivery"})
        self.assertEqual(output["current_delivery"], {
            "delivery_key": key, "phase": "implementing", "planning_root": projection.resolve(key)["planning_root"],
        })
        self.assertGreater((self.task / "task.json").stat().st_size, 100000)
        self.assertLess(len(json.dumps(output)), 700)
        self.assertNotIn("results", json.dumps(output))

    def test_known_context_without_binding_is_not_missing_context(self):
        self.assertEqual(self.query(), {"exit_id": "no_current_task"})

    def test_missing_context_uses_original_resolver(self):
        self.bind()
        self.controls()
        before = self.snapshot()
        with patch.dict(os.environ, {}, clear=True), patch("os.getcwd", return_value=str(self.root)):
            self.assertIsNone(self.official.resolve_context_key())
            with patch.object(self.module.subprocess, "run") as command:
                output = self.module.invoke(self.root, {"profile": "delivery_current_task", "mode": "workflow"})
                self.assertEqual(output, {"exit_id": "context_unavailable", "reason_code": "context_key_unavailable"})
                command.assert_not_called()
        self.assertEqual(before, self.snapshot())
        schema.validate_json(output, PACKAGE / "schemas/public-output.schema.json", "stdout")

    def test_current_reuses_binding_ownership_and_checkout_routes(self):
        self.bind()
        self.assertEqual(self.query()["exit_id"], "binding_required")
        binding = BranchBindingStore(self.repository).establish(self.key, "main")
        self.assertEqual(self.query()["exit_id"], "binding_required")
        ResourceLedgerStore(self.repository).establish_current(
            self.key, binding_revision=binding.binding_revision + 1, branch_name="main",
            branch_ownership="caller_owned", worktree_ownership="not_applicable",
        )
        self.assertEqual(self.query(), {"exit_id": "invalid_task_state", "reason_code": "binding_ownership_mismatch"})

    def test_bound_branch_without_checkout_preserves_acquisition_route(self):
        self.bind()
        self.git("branch", "task-branch")
        self.controls("task-branch")
        with self.assertRaises(CommandError) as failure:
            self.query()
        self.assertEqual(failure.exception.code, "current_task_checkout_unresolved")
        self.assertIn("task-branches/demo/0.json", failure.exception.remediation)

    def test_stale_session_is_an_error_without_repair(self):
        self.bind()
        self.controls()
        metadata = current_task("planning", 1)
        (self.task / "task.json").write_text(json.dumps(metadata), encoding="utf-8")
        with self.assertRaises(CommandError) as failure:
            self.query()
        self.assertNotEqual(failure.exception.code, "internal_error")
        self.assertIn("demo", failure.exception.remediation)

    def test_original_structured_current_diagnostic_survives(self):
        diagnostic = {"code": "session_record_invalid", "field_path": "session.schema_version", "remediation": "Use the original session recovery owner."}
        for stdout, stderr in ((json.dumps({"error": diagnostic}), ""), ("", json.dumps(diagnostic))):
            with self.subTest(stream="stdout" if stdout else "stderr"):
                completed = subprocess.CompletedProcess([], 1, stdout, stderr)
                with patch.object(self.module.subprocess, "run", return_value=completed):
                    with self.assertRaises(CommandError) as failure:
                        self.module.invoke(self.root, {"profile": "delivery_current_task", "mode": "standalone"})
                self.assertEqual((failure.exception.code, failure.exception.field_path, failure.exception.remediation),
                                 (diagnostic["code"], diagnostic["field_path"], diagnostic["remediation"]))

    def test_public_wrapper_emits_checked_current_projection(self):
        self.bind()
        self.controls()
        before = self.snapshot()
        result = subprocess.run([str(PACKAGE / "scripts/invoke.sh"), "--root", str(self.root), "--input",
                                 json.dumps({"profile": "delivery_current_task", "mode": "standalone"})],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["exit_id"], "current_context_ready")
        self.assertNotIn("current_delivery", output)
        self.assertEqual(output["checkout_path"], str(self.root))
        schema.validate_json(output, PACKAGE / "schemas/public-current-context-ready-output.schema.json", "stdout")
        self.assertEqual(before, self.snapshot())

    def test_help_exposes_both_profiles_through_original_dispatcher(self):
        result = subprocess.run([sys.executable, "-m", "runtime.command", str(PACKAGE),
                                 "invoke-guru-ensure-task-checkout", "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("delivery_current_task: schemas/public-delivery-current-task-input.schema.json ; example: examples/public-current-input.json", result.stdout)
        self.assertIn("delivery_active_task: schemas/public-delivery-active-task-input.schema.json", result.stdout)


if __name__ == "__main__":
    unittest.main()
