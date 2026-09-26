from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json


PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("guru_create_task_candidate", PACKAGE / "runtime/invoke.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
SOURCE = PACKAGE.parents[4]


class CreateTaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        upstream = os.environ.get("TRELLIS_FIXED_FORK_SOURCE")
        scripts = Path(upstream) / "packages/cli/src/templates/trellis/scripts" if upstream else SOURCE / ".trellis/scripts"
        shutil.copytree(scripts, self.root / ".trellis/scripts")
        (self.root / "README.md").write_text("fixture\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        self.head = self.git("rev-parse", "HEAD")
        self.git("switch", "-q", "-c", "codex/example-task")
        prefix = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%m-%d")
        self.ref = f".trellis/tasks/{prefix}-example-task"
        self.payload = {
            "profile": "task_creation", "action": "create_task",
            "creation": {
                "task_id": "example-task", "task_ref": self.ref,
                "source_profile": "standalone_request", "reviewed_source": {"kind": "no_issue"},
                "accepted_scope_identity": "scope:reviewed",
                "delivery_target": {"repo_ref": "castbox/guru-trellis", "branch_ref": "main"},
                "selected_base_ref": "main", "reviewed_base_head": self.head,
            },
            "acquisition": {
                "route": "adopt_invocation_checkout", "branch_ref": "codex/example-task",
                "decision_head": self.head, "transaction_id": "acquisition:example",
                "result_id": "checkout:example", "invocation_checkout": str(self.root),
            },
            "task": {
                "title": "Example task", "description": "Reviewed delivery scope",
                "creator": "team", "assignee": "team", "scope": "Reviewed scope",
            },
        }

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def invoke(self, data: dict) -> dict:
        class NoContextPort:
            @staticmethod
            def resolve_context_key(platform_input=None, platform=None):
                return None

        with patch.object(MODULE, "_official_port", return_value=NoContextPort()):
            result = MODULE.invoke(self.root, data)
        validate_json(result, PACKAGE / "schemas/public-output.schema.json", "output")
        return result

    def invoke_with_port(self, data: dict, port: object) -> dict:
        with patch.object(MODULE, "_official_port", return_value=port):
            result = MODULE.invoke(self.root, data)
        validate_json(result, PACKAGE / "schemas/public-output.schema.json", "output")
        return result

    def test_invocation_error_example_matches_runtime_error_contract(self) -> None:
        example = json.loads((PACKAGE / "examples/public-invocation-error.json").read_text(encoding="utf-8"))
        validate_json(example, PACKAGE / "schemas/public-invocation-error.schema.json", "invocation_error")
        self.assertEqual(example["code"], "stale_identity")

    def test_adopt_no_issue_create_and_read_only_recovery(self) -> None:
        result = self.invoke(self.payload)
        self.assertEqual(result, {
            "exit_id": "created", "task_id": "example-task", "task_ref": self.ref,
            "lifecycle_generation": 0,
        })
        task = json.loads((self.root / self.ref / "task.json").read_text(encoding="utf-8"))
        self.assertEqual(task["source"], {"kind": "no_issue"})
        self.assertEqual(task["status"], "planning")
        self.assertNotIn("branch", task)
        self.assertNotIn("worktree_path", task)
        before = self.git("status", "--porcelain")
        self.assertEqual(self.invoke({**self.payload, "action": "recover_created_task_result"}), result)
        self.assertEqual(self.git("status", "--porcelain"), before)
        self.assertEqual(self.invoke(self.payload)["exit_id"], "invalid_task_state")

    def test_stale_base_and_invocation_head_are_distinct(self) -> None:
        stale = json.loads(json.dumps(self.payload))
        stale["creation"]["reviewed_base_head"] = "a" * 40
        self.assertEqual(self.invoke(stale)["exit_id"], "refresh_review")
        mismatch = json.loads(json.dumps(self.payload))
        mismatch["acquisition"]["decision_head"] = "a" * 40
        self.assertEqual(self.invoke(mismatch)["exit_id"], "blocked")
        self.assertFalse((self.root / self.ref).exists())

    def test_stale_shanghai_task_date_refreshes_without_creating(self) -> None:
        stale = json.loads(json.dumps(self.payload))
        current = Path(self.ref).name[:5]
        old_prefix = "01-01" if current != "01-01" else "01-02"
        stale["creation"]["task_ref"] = self.ref.replace(current, old_prefix, 1)
        self.assertEqual(self.invoke(stale), {"exit_id": "refresh_review", "reason_code": "creation_date_stale"})
        self.assertFalse((self.root / stale["creation"]["task_ref"]).exists())
        self.assertFalse((self.root / self.ref).exists())

    def test_record_plan_rejects_stale_shanghai_task_date(self) -> None:
        stale = json.loads(json.dumps(self.payload))
        current = Path(self.ref).name[:5]
        stale["creation"]["task_ref"] = self.ref.replace(current, "01-01" if current != "01-01" else "01-02", 1)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "input.json"
            path.write_text(json.dumps(stale), encoding="utf-8")
            with self.assertRaises(MODULE.LifecycleContractError) as caught:
                MODULE.run(PACKAGE, {"id": "record-task-plan"}, ["--root", str(self.root), "--input", str(path)])
        self.assertEqual(caught.exception.code, "creation_date_stale")
        self.assertFalse((self.root / stale["creation"]["task_ref"]).exists())

    def test_created_result_remains_recoverable_on_later_date(self) -> None:
        result = self.invoke(self.payload)
        different_date = "01-01" if Path(self.ref).name[:5] != "01-01" else "01-02"
        with patch.object(MODULE, "_task_date_prefix", return_value=different_date):
            self.assertEqual(self.invoke({**self.payload, "action": "recover_created_task_result"}), result)

    def test_date_flip_during_official_create_leaves_no_task(self) -> None:
        current = Path(self.ref).name[:5]
        next_prefix = "01-01" if current != "01-01" else "01-02"
        original_run = subprocess.run
        official_calls = []

        def run(command, *args, **kwargs):
            if (isinstance(command, list) and len(command) > 2
                    and command[0] == sys.executable and command[2] == "create"):
                official_calls.append(command)
                return subprocess.CompletedProcess(command, 1, "", "task date changed")
            return original_run(command, *args, **kwargs)

        with patch.object(MODULE, "_task_date_prefix", side_effect=[current, current, next_prefix]), \
             patch.object(MODULE.subprocess, "run", side_effect=run):
            self.assertEqual(self.invoke(self.payload),
                             {"exit_id": "refresh_review", "reason_code": "creation_date_stale"})
        self.assertEqual(len(official_calls), 1)
        self.assertEqual(official_calls[0][official_calls[0].index("--slug") + 1], Path(self.ref).name)
        self.assertFalse((self.root / self.ref).exists())

    def test_recovery_retries_incomplete_session_binding_before_created(self) -> None:
        class BrokenSessionPort:
            @staticmethod
            def resolve_context_key(platform_input=None, platform=None):
                return "codex-test"

            @staticmethod
            def repository_facts(root):
                raise OSError("session store unavailable")

        blocked = self.invoke_with_port(self.payload, BrokenSessionPort())
        self.assertEqual(blocked, {"exit_id": "blocked", "reason_code": "official_session_target_invalid"})
        recovery = {**self.payload, "action": "recover_created_task_result"}
        self.assertEqual(self.invoke_with_port(recovery, BrokenSessionPort()), blocked)
        self.assertEqual(self.invoke(recovery)["exit_id"], "created")

    def test_merged_fixed_fork_official_store_and_session_port(self) -> None:
        if not os.environ.get("TRELLIS_FIXED_FORK_SOURCE"):
            self.skipTest("Set TRELLIS_FIXED_FORK_SOURCE to the merged Fixed Fork checkout")
        result = MODULE.invoke(self.root, self.payload)
        self.assertEqual(result["exit_id"], "created")
        self.assertEqual(MODULE.invoke(self.root, {**self.payload, "action": "recover_created_task_result"}), result)
        data = json.loads((self.root / self.ref / "task.json").read_text())
        self.assertEqual((data["id"], data["source"], data["lifecycle_generation"]),
                         ("example-task", {"kind": "no_issue"}, 0))

    def test_provision_new_linked_checkout_and_exact_source(self) -> None:
        self.git("switch", "-q", "main")
        self.git("branch", "-D", "codex/example-task")
        linked = Path(self.temporary.name) / "linked"
        request = json.loads(json.dumps(self.payload))
        request["creation"]["source_profile"] = "existing_issue"
        request["creation"]["reviewed_source"] = {
            "kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454,
            "disposition": "exact_source",
        }
        request["acquisition"] = {
            "route": "provision_linked_worktree", "branch_ref": "codex/example-task",
            "decision_head": self.head, "transaction_id": "acquisition:linked",
            "result_id": "checkout:linked", "provision_disposition": "new_branch",
            "checkout_root": str(linked),
        }
        self.assertEqual(self.invoke(request)["exit_id"], "created")
        data = json.loads((linked / self.ref / "task.json").read_text())
        self.assertEqual(data["source"], request["creation"]["reviewed_source"])
        self.assertEqual(self.invoke({**request, "action": "recover_created_task_result"})["exit_id"], "created")
        self.assertEqual(self.git("branch", "--format=%(refname:short)", "--list", "codex/example-task"),
                         "codex/example-task")


if __name__ == "__main__":
    unittest.main()
