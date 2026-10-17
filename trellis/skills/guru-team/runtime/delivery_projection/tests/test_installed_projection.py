"""Directed integration against the explicitly selected installed upstream API.

GURU_UPSTREAM_DELIVERY_SCRIPTS must identify the reviewed installed package's
templates/trellis/scripts directory. No fabricated aggregate fixtures or native
implementation fallback are used. These tests perform only local operations.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.identity import resolve_task_id
from runtime.task_lifecycle.session_adapter import bind_session, resolve_session


OWNERS = {
    "task_scope": "guru-task-scope-projection", "creation": "guru-create-delivery",
    "planning": "guru-activate-delivery", "implementation": "guru-delivery-implementation-projection",
    "check": "guru-check-task", "full_review": "guru-review-branch", "readiness": "guru-review-task-delivery",
    "publication": "guru-publish-task-delivery", "delivery": "guru-merge-task-delivery",
    "completion": "guru-review-task-completion", "closure": "guru-complete-task-closure",
}
DECLARATION = {"delivery_api": "1.0", "task_schema": "2.0", "profiles": ["pull_request"], "owners": OWNERS}


class InstalledProjectionTests(unittest.TestCase):
    def setUp(self):
        scripts = Path(os.environ.get("GURU_UPSTREAM_DELIVERY_SCRIPTS", ""))
        if not (scripts / "common/delivery_store.py").is_file():
            self.fail("Set GURU_UPSTREAM_DELIVERY_SCRIPTS to the reviewed installed upstream candidate; missing dependency is not a pass.")
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        subprocess.run(["git", "init", "-b", "task"], cwd=self.root, capture_output=True, check=True)
        shutil.copytree(scripts, self.root / ".trellis/scripts")
        (self.root / ".trellis/.developer").write_text("projection-test\n")
        version = json.loads((scripts.parents[3] / "package.json").read_text())["version"]
        (self.root / ".trellis/.version").write_text(version + "\n")
        (self.root / ".trellis/workflow.md").write_text("[trellis-runtime-contract]\n" + json.dumps(DECLARATION) + "\n[/trellis-runtime-contract]\n")
        self.environment = patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "projection-test"})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        completed = subprocess.run([sys.executable, str(self.root / ".trellis/scripts/task.py"), "create", "投影验证",
                                    "--description", "同 Task 两个 Delivery 与事实恢复", "--slug", "projection", "--task-id", "projection-task",
                                    "--schema-version", "2.0", "--source-json", '{"kind":"no_issue"}', "--base-branch", "task", "--no-start"],
                                   cwd=self.root, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.task = next((self.root / ".trellis/tasks").glob("*/task.json")).parent
        self.task_ref = self.task.relative_to(self.root).as_posix()
        self.projection = DeliveryProjection(self.root, self.task_ref)
        (self.task / "prd.md").write_text("整体scope\n")
        self.scope = authority_ref(self.task / "prd.md", self.root)
        self.projection.scope(self.scope)

    def create(self) -> dict:
        key = {"task_id": "projection-task", "lifecycle_generation": 0, "delivery_id": str(uuid.uuid4())}
        operation = {"api_version": "1.0", "operation": "create_delivery", "key": key,
                     "owner_role": "creation", "owner_id": OWNERS["creation"],
                     "scope_ref": {"authority": self.scope, "anchors": ["验收"]}, "profile": "pull_request"}
        first = self.projection.apply(operation)
        self.assertTrue(first["changed"])
        self.assertFalse(self.projection.apply(operation)["changed"])  # same identity after lost stdout
        self.projection.select(key)
        return key

    def planning(self, key: dict) -> dict:
        plan = self.projection.planning_directory(key) / "design.md"
        plan.write_text("已由Planning owner实际审核的计划\n")
        result = {"result_id": "planning-" + key["delivery_id"], "owner_role": "planning", "owner_id": OWNERS["planning"],
                  "outcome": "accepted", "scope_ref": self.projection.resolve(key)["scope_ref"], "plan_ref": authority_ref(plan, self.root),
                  "candidate": None, "predecessor_result_id": None, "obligations": [], "evidence": [self.scope]}
        self.projection.apply({"api_version": "1.0", "operation": "record_gate", "key": key, "owner_role": "planning",
                               "owner_id": OWNERS["planning"], "expected_phase": "planning", "result": result})
        return result

    def stop(self, key: dict):
        delivery = self.projection.resolve(key)
        role = "planning" if delivery["phase"] == "planning" else "implementation"
        result = {"result_id": "stop-" + key["delivery_id"], "owner_id": OWNERS[role],
                  "evidence": [self.scope], "reason": self.scope, "scope_decision": self.scope}
        return self.projection.apply({"api_version": "1.0", "operation": "stop", "key": key, "owner_role": role,
                                      "owner_id": OWNERS[role], "expected_phase": delivery["phase"], "result": result})

    def test_two_deliveries_keep_plan_and_explicit_selection(self):
        first = self.create()
        first_plan = self.projection.planning_directory(first) / "design.md"
        first_plan.write_text("D1唯一计划\n")
        self.stop(first)
        self.assertEqual(self.projection.current()["kind"], "no_current_delivery")
        second = self.create()
        self.assertNotEqual(first, second)
        self.assertEqual(first_plan.read_text(), "D1唯一计划\n")
        self.assertEqual(self.projection.current()["key"], second)
        self.assertEqual(resolve_task_id(self.root, "projection-task").task_ref, self.task_ref)
        self.assertNotIn("status", self.projection.read_record())

    def test_planning_rework_retains_identity_and_candidate_content(self):
        key = self.create()
        planning = self.planning(key)
        file = self.root / "implementation.txt"
        file.write_text("候选内容\n")
        candidate = self.projection.candidate(["implementation.txt"], kind="git_free")
        self.projection.begin_check(key, candidate)
        self.projection.apply({"api_version": "1.0", "operation": "rework", "key": key, "owner_role": "check",
                               "owner_id": OWNERS["check"], "expected_phase": "checking", "target_role": "planning",
                               "reason": self.scope, "affected_results": ["planning", "check", "full_review", "readiness"]})
        self.assertEqual(self.projection.current()["key"], key)
        self.assertEqual(self.projection.resolve(key)["phase"], "planning")
        self.assertEqual(file.read_text(), "候选内容\n")
        self.assertEqual(self.projection.gate_applicability(key)["planning"]["kind"], "missing")

    def test_candidate_kind_preserves_git_free_permissions_inside_git_checkout(self):
        file = self.root / "implementation.txt"
        file.write_text("同一候选内容\n")
        candidates = {}
        for mode in (0o600, 0o640):
            file.chmod(mode)
            candidates[mode] = {
                "git": self.projection.candidate(["implementation.txt"]),
                "git_free": self.projection.candidate(["implementation.txt"], kind="git_free"),
            }
            for candidate in candidates[mode].values():
                self.projection.api.delivery_store.verify_candidate(self.projection.root, candidate)
            self.assertNotEqual(candidates[mode]["git"]["content_ref"],
                                candidates[mode]["git_free"]["content_ref"])
        self.assertEqual(candidates[0o600]["git"]["content_ref"], candidates[0o640]["git"]["content_ref"])
        self.assertNotEqual(candidates[0o600]["git_free"]["content_ref"], candidates[0o640]["git_free"]["content_ref"])

    def test_implementation_withdrawal_releases_selection_and_recovers_same_fact(self):
        key = self.create()
        self.planning(key)
        reason = {"result_id": "implementation-withdrawal", "reason": self.scope,
                  "scope_decision": self.scope, "evidence": [self.scope]}
        task_key = self.projection.stop_implementation(key, reason)
        self.assertEqual(self.projection.resolve(key)["phase"], "stopped")
        self.assertEqual(self.projection.current()["kind"], "no_current_delivery")
        self.assertEqual(self.projection.stop_implementation(key, reason), task_key)
        self.assertNotIn("status", self.projection.read_record())

    def test_task_rebind_preserves_current_delivery(self):
        key = self.create()
        # Use the real public official session port, without Guru session substitutes.
        package = Path(__file__).resolve().parents[3] / "packages/guru-bind-task-session/runtime/invoke.py"
        spec = importlib.util.spec_from_file_location("projection_session_owner", package)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        official = module.official_port(self.root)
        lifecycle = {"task_id": key["task_id"], "lifecycle_generation": key["lifecycle_generation"]}
        result = bind_session(official, self.root, lifecycle)
        self.assertEqual(result.status, "session_bound")
        self.assertEqual(resolve_session(official, self.root).status, "session_resolved")
        self.assertEqual(self.projection.current()["key"], key)

    def test_completion_reopen_retains_history_without_empty_delivery(self):
        key = self.create()
        self.stop(key)
        record = self.projection.read_record()
        completion = {"result_id": "completed-scope", "owner_id": OWNERS["completion"], "evidence": [self.scope],
                      "lifecycle_generation": 0, "accepted_scope": self.scope, "delivery_result_ids": [], "outcome": "completed"}
        task_key = {"task_id": key["task_id"], "lifecycle_generation": 0}
        self.projection.apply({"api_version": "1.0", "operation": "complete_task", "key": task_key, "owner_role": "completion",
                               "owner_id": OWNERS["completion"], "result": completion})
        closure = {"result_id": "closed-scope", "owner_id": OWNERS["closure"], "evidence": [self.scope], "lifecycle_generation": 0,
                   "completion_result_id": completion["result_id"], "disposition": "no_mutation", "source_result": None}
        self.projection.apply({"api_version": "1.0", "operation": "close_task", "key": task_key, "owner_role": "closure", "owner_id": OWNERS["closure"], "result": closure})
        receipt = self.projection.scope(self.scope, reopen=True)
        self.assertEqual(receipt["key"]["lifecycle_generation"], 1)
        self.assertEqual(self.projection.read_record()["deliveries"], record["deliveries"])
        self.assertEqual(self.projection.current()["kind"], "no_current_delivery")
        self.assertEqual(self.projection.planning_directory(key), (self.task / self.projection.resolve(key)["planning_root"]).resolve())

    def test_installer_checks_actual_target_capabilities_before_writing(self):
        source = Path(__file__).resolve().parents[6]
        path = source / "trellis/presets/guru-team/scripts/python/delivery_installation.py"
        spec = importlib.util.spec_from_file_location("capability_install_diagnosis", path)
        diagnosis = importlib.util.module_from_spec(spec); spec.loader.exec_module(diagnosis)
        before = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(diagnosis.diagnose_delivery_installation(source, self.root)["status"], "supported_candidate")
        self.assertEqual(before, {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        # An interrupted package install can leave this real target module incomplete.
        target = self.root / ".trellis/scripts/common/delivery_session.py"
        target.write_text('"""Incomplete installation; public session API unavailable."""\n')
        before = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = diagnosis.diagnose_delivery_installation(source, self.root)
        self.assertEqual((result["status"], result["code"]), ("blocked", "unsupported_delivery_api"))
        self.assertTrue(result["missing_capabilities"])
        self.assertEqual(before, {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_installer_blocks_real_legacy_task_before_writing(self):
        source = Path(__file__).resolve().parents[6]
        path = source / "trellis/presets/guru-team/scripts/python/delivery_installation.py"
        spec = importlib.util.spec_from_file_location("projection_install_diagnosis", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            subprocess.run(["git", "init", "-b", "legacy"], cwd=target, capture_output=True, check=True)
            shutil.copytree(self.root / ".trellis/scripts", target / ".trellis/scripts")
            (target / ".trellis/workflow.md").write_text("Legacy pinned workflow\n")
            (target / ".trellis/.developer").write_text("projection-test\n")
            result = subprocess.run([sys.executable, str(target / ".trellis/scripts/task.py"), "create", "旧安装活动Task",
                                     "--description", "迁移前真实旧记录", "--slug", "legacy", "--no-start"],
                                    cwd=target, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            # The supplied source is the actual current Guru Delivery candidate.
            diagnosis = module.diagnose_delivery_installation(source, target)
            self.assertEqual(diagnosis["code"], "upstream_delivery_migration_required")
            before = {p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            with self.assertRaises(SystemExit):
                module.require_delivery_installation(source, target)
            after = {p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_uninstalled_dependency_does_not_use_source_fallback(self):
        with tempfile.TemporaryDirectory() as other:
            with self.assertRaisesRegex(LifecycleContractError, "unsupported_delivery_api"):
                DeliveryProjection(Path(other), self.task_ref)

    def test_creation_owner_uses_public_schema2_and_recovers_same_resources(self):
        def git(*args):
            return subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True, check=True).stdout.strip()
        git("config", "user.name", "Projection Test")
        git("config", "user.email", "projection@example.invalid")
        git("add", ".")
        git("commit", "-qm", "local test fixture")
        head = git("rev-parse", "HEAD")
        checkout = self.root / "linked"
        git("worktree", "add", "-b", "delivery-creation", str(checkout), "task")
        ref = ".trellis/tasks/" + datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%m-%d") + "-created-task"
        payload = {"profile": "delivery_task_creation", "action": "create_task",
                   "creation": {"task_id": "created-task", "task_ref": ref, "source_profile": "standalone_request",
                                "reviewed_source": {"kind": "no_issue"}, "accepted_scope_identity": "task-scope",
                                "delivery_target": {"repo_ref": "example/project", "branch_ref": "main"},
                                "selected_base_ref": "task", "reviewed_base_head": head},
                   "acquisition": {"route": "adopt_invocation_checkout", "branch_ref": "delivery-creation",
                                   "decision_head": head, "transaction_id": "creation-test", "result_id": "creation-test",
                                   "invocation_checkout": str(checkout)},
                   "task": {"title": "正式Task创建", "description": "公共schema2与真实身份恢复", "scope": "整体需求"}}
        path = Path(__file__).resolve().parents[3] / "packages/guru-create-task/runtime/invoke.py"
        spec = importlib.util.spec_from_file_location("projection_create_owner", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "creation-test"}):
            output = module.invoke(checkout, payload)
            self.assertEqual(output["exit_id"], "created", output)
            metadata_path = checkout / ref / "task.json"
            record = json.loads(metadata_path.read_text())
            self.assertEqual(record["schema_version"], "2.0")
            self.assertNotIn("status", record)
            self.assertEqual(record["deliveries"], [])
            original = metadata_path.read_bytes()
            payload["action"] = "recover_created_task_result"
            self.assertEqual(module.invoke(checkout, payload), output)
            self.assertEqual(metadata_path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
