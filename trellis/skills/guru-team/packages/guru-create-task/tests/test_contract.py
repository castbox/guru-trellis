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
from types import SimpleNamespace
from unittest.mock import patch
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json
from runtime.task_lifecycle.session_adapter import bind_session, resolve_session


PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("guru_create_task_candidate", PACKAGE / "runtime/invoke.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
SOURCE = PACKAGE.parents[4]


class CreateTaskTests(unittest.TestCase):
    def setUp(self) -> None:
        retained = os.environ.get("GURU_CREATE_TASK_INSTALLED_FIXTURE_ROOT")
        if retained and self._testMethodName == "test_clean_installed_mixed_history_public_creation_and_rejection":
            # Optional inspection locator for this representative installed probe.
            # Require a new directory; reruns never replace an existing fixture.
            fixture = Path(retained).resolve()
            fixture.mkdir(parents=True, exist_ok=False)
            self.temporary = SimpleNamespace(name=str(fixture))
        else:
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
                "scope": "Reviewed scope",
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
        self.assertNotIn("delivery_target", task)
        self.assertNotIn("creator", task)
        self.assertNotIn("assignee", task)
        self.assertNotIn("branch", task)
        self.assertIsNone(task["worktree_path"])
        before = self.git("status", "--porcelain")
        self.assertEqual(self.invoke({**self.payload, "action": "recover_created_task_result"}), result)
        self.assertEqual(self.git("status", "--porcelain"), before)
        self.assertEqual(self.invoke(self.payload)["exit_id"], "invalid_task_state")

    def test_unrelated_legacy_archive_does_not_block_creation(self) -> None:
        prefix = "01-01" if Path(self.ref).name[:5] != "01-01" else "01-02"
        prior = self.root / ".trellis/tasks/archive/2025-01" / f"{prefix}-historical-task"
        prior.mkdir(parents=True)
        (prior / "task.json").write_text(json.dumps({
            "id": "historical-task-id", "name": "example-task", "status": "completed",
            "lifecycle_generation": 0,
        }), encoding="utf-8")
        self.git("add", ".trellis/tasks/archive")
        self.git("commit", "-qm", "historical task")
        head = self.git("rev-parse", "HEAD")
        self.git("branch", "-f", "main", head)
        self.payload["creation"]["reviewed_base_head"] = head
        self.payload["acquisition"]["decision_head"] = head
        result = self.invoke(self.payload)
        self.assertEqual(result["exit_id"], "created", result)
        current = json.loads((self.root / self.ref / "task.json").read_text(encoding="utf-8"))
        self.assertEqual(current["id"], "example-task")
        self.assertEqual(json.loads((prior / "task.json").read_text(encoding="utf-8"))["id"],
                         "historical-task-id")

    def test_stale_base_and_invocation_head_are_distinct(self) -> None:
        stale = json.loads(json.dumps(self.payload))
        stale["creation"]["reviewed_base_head"] = "a" * 40
        self.assertEqual(self.invoke(stale)["exit_id"], "refresh_review")
        mismatch = json.loads(json.dumps(self.payload))
        mismatch["acquisition"]["decision_head"] = "a" * 40
        self.assertEqual(self.invoke(mismatch)["exit_id"], "blocked")
        self.assertFalse((self.root / self.ref).exists())

    def test_retired_personnel_input_is_rejected_before_creation(self) -> None:
        for field in ("creator", "assignee"):
            with self.subTest(field=field):
                old = json.loads(json.dumps(self.payload))
                old["task"][field] = "team"
                with self.assertRaises(MODULE.CommandError):
                    self.invoke(old)
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
        self.assertEqual(official_calls[0][official_calls[0].index("--slug") + 1], "example-task")
        self.assertEqual(official_calls[0][official_calls[0].index("--task-id") + 1],
                         self.payload["creation"]["task_id"])
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
        self.assertEqual(self.invoke_with_port(recovery, BrokenSessionPort()),
                         {"exit_id": "blocked", "reason_code": "official_session_record_invalid"})
        self.assertEqual(self.invoke(recovery)["exit_id"], "created")

    def test_recovery_preserves_a_later_current_task_route(self) -> None:
        class SessionPort:
            def __init__(self, task_ref):
                self.task_ref = task_ref
                self.records = {}
                self.writes = 0

            def resolve_context_key(self, platform_input=None, platform=None):
                return "codex-test"

            def repository_facts(self, root):
                return SimpleNamespace(common_dir=root / ".git")

            def session_path(self, root, key, facts):
                return facts.common_dir / "sessions" / f"{key}.json"

            def record_exists(self, path):
                return path in self.records

            def read_record(self, path, root, facts):
                data = self.records[path]
                return SimpleNamespace(data=data, task_id=data["task_id"],
                                       lifecycle_generation=data["lifecycle_generation"])

            def write_record(self, path, data, root):
                self.writes += 1
                self.records[path] = data

            def resolve_task_identity(self, facts, task_id, lifecycle_generation):
                refs = {"example-task": self.task_ref, "another-task": ".trellis/tasks/another-task"}
                return SimpleNamespace(task_ref=refs[task_id])

        port = SessionPort(self.ref)
        created = self.invoke_with_port(self.payload, port)
        recovery = {**self.payload, "action": "recover_created_task_result"}
        self.assertEqual(self.invoke_with_port(recovery, port), created)
        self.assertEqual(port.writes, 1)

        port.records.clear()
        self.assertEqual(self.invoke_with_port(recovery, port), created)
        self.assertEqual(port.writes, 2)

        self.assertEqual(bind_session(port, self.root, {"task_id": "another-task",
                                                       "lifecycle_generation": 0}).status, "session_bound")
        self.assertEqual(self.invoke_with_port(recovery, port),
                         {"exit_id": "blocked", "reason_code": "session_current_task_conflict"})
        self.assertEqual(port.writes, 3)
        self.assertEqual(resolve_session(port, self.root).lifecycle.task_id, "another-task")

    def test_merged_fixed_fork_official_store_and_session_port(self) -> None:
        if not os.environ.get("TRELLIS_FIXED_FORK_SOURCE"):
            self.skipTest("Set TRELLIS_FIXED_FORK_SOURCE to the merged Fixed Fork checkout")
        real_run = subprocess.run
        created = []

        def capture_create(command, **options):
            if len(command) > 1 and str(command[1]).endswith("/.trellis/scripts/task.py"):
                self.assertEqual(options["env"]["TZ"], "Asia/Shanghai")
                created.append(command)
            return real_run(command, **options)

        with patch.dict(os.environ, {"TZ": "UTC"}), patch.object(MODULE.subprocess, "run", side_effect=capture_create):
            result = MODULE.invoke(self.root, self.payload)
        self.assertEqual(result["exit_id"], "created")
        self.assertEqual(len(created), 1)
        source_index = created[0].index("--source-json")
        self.assertEqual(json.loads(created[0][source_index + 1]), {"kind": "no_issue"})
        self.assertEqual(MODULE.invoke(self.root, {**self.payload, "action": "recover_created_task_result"}), result)
        data = json.loads((self.root / self.ref / "task.json").read_text())
        self.assertEqual((data["id"], data["source"], data["lifecycle_generation"]),
                         ("example-task", {"kind": "no_issue"}, 0))

    def assert_public_creation_and_recovery(self, source: dict) -> None:
        # Real public launchers, the official writer, and the production source reader.
        env = {key: value for key, value in os.environ.items()
               if not key.startswith(("TRELLIS_", "CODEX_", "CLAUDE_", "CURSOR_", "GIT_"))}

        def public(package: Path, payload: dict) -> dict:
            completed = subprocess.run(
                ["bash", str(package / "scripts/invoke.sh"), "--root", str(self.root), "--input", "-"],
                input=json.dumps(payload), text=True, capture_output=True, env=env, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            return json.loads(completed.stdout)

        request = json.loads(json.dumps(self.payload))
        request["creation"].update(source_profile="existing_issue" if source["kind"] == "issue"
                                   else "standalone_request", reviewed_source=source)
        created = public(PACKAGE, request)
        self.assertEqual(created, {"exit_id": "created", "task_id": "example-task",
                                  "task_ref": self.ref, "lifecycle_generation": 0})
        metadata_path = self.root / self.ref / "task.json"
        before = metadata_path.read_bytes()
        self.assertEqual(json.loads(before)["source"], source)
        recovered = public(PACKAGE, {**request, "action": "recover_created_task_result"})
        self.assertEqual(recovered, created)
        self.assertEqual(metadata_path.read_bytes(), before)
        identity = public(PACKAGE.parent / "guru-establish-task-identity", {
            "profile": "active_task", "mode": "standalone", "task_id": "example-task",
            "task_ref": self.ref, "lifecycle_generation": 0,
        })
        self.assertEqual(identity["exit_id"], "identity_established")
        self.assertEqual(identity["source"], source)

    def public_call(self, packages: Path, skill: str, payload: dict, *, validator: str | None = None, root: Path | None = None):
        env = {key: value for key, value in os.environ.items()
               if not key.startswith(("TRELLIS_", "CODEX_", "CLAUDE_", "CURSOR_", "GIT_"))}
        env["TRELLIS_CONTEXT_ID"] = "mixed-task-fixture"
        if validator:
            wrapper = (SOURCE / "trellis/workflows/guru-team/scripts/bash/run-skill-command.sh"
                       if packages == PACKAGE.parent else packages.parent.parent / "scripts/bash/run-skill-command.sh")
            command = ["bash", str(wrapper),
                       "--package-root", str(packages / skill), "--validator", validator, "--"]
        else:
            command = ["bash", str(packages / skill / "scripts/invoke.sh")]
        if skill == "guru-bind-task-session":
            # Contract fixture for the semantic resume owner after the preceding
            # public creation/checkout assertions establish this exact lifecycle.
            owner = {**payload, "route": "resume", "resume_target": "phase-1",
                     "ai_review_gate": {"status": "passed", "summary": "Fixture resumes the just-created planning lifecycle."}}
            owner_path = Path(self.temporary.name) / "resume-owner.json"
            owner_path.write_text(json.dumps(owner))
            command += ["--owner-result", str(owner_path)]
        completed = subprocess.run([*command, "--root", str(root or self.root), "--input", "-"],
                                   input=json.dumps(payload), text=True, capture_output=True, env=env)
        self.assertTrue(completed.stdout.strip(), completed.stderr)
        output = json.loads(completed.stdout)
        if completed.returncode == 0 and validator and validator != "public_invocation":
            from runtime.io import project_intermediate_receipt
            output = project_intermediate_receipt(output, packages.parent / "schemas")
        return completed, output

    def mixed_sibling(self) -> Path:
        sibling = Path(self.temporary.name) / "historical"
        self.git("worktree", "add", "-q", "-b", "historical", str(sibling))
        path = sibling / ".trellis/tasks/09-23-old/task.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({"id": "historical-task", "name": "old", "title": "Old task",
                                   "status": "in_progress", "creator": "team", "assignee": "team",
                                   "subtasks": [], "lifecycle_generation": 1}), encoding="utf-8")
        path.chmod(0o640)
        return path.resolve()

    def test_public_mixed_history_create_ensure_bind_and_read_only_recovery(self):
        path = self.mixed_sibling()
        before = (path.read_bytes(), path.stat().st_mode)
        sibling_status = subprocess.check_output(["git", "status", "--porcelain"], cwd=path.parents[3])
        for skill, payload, expected in (
            ("guru-create-task", self.payload, "created"),
            ("guru-ensure-task-checkout", {"profile": "active_task", "mode": "workflow",
                "task_id": "example-task", "lifecycle_generation": 0}, "checkout_resolved"),
            ("guru-bind-task-session", {"profile": "resume_current_task", "mode": "standalone",
                "task_id": "example-task", "lifecycle_generation": 0,
                "continuation_id": "fixture-resume"}, "session_resumed"),
            ("guru-establish-task-identity", {"profile": "active_task", "mode": "standalone",
                "task_id": "example-task", "task_ref": self.ref,
                "lifecycle_generation": 0}, "identity_established"),
            ("guru-create-task", {**self.payload, "action": "recover_created_task_result"}, "created"),
        ):
            completed, output = self.public_call(PACKAGE.parent, skill, payload)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertEqual(output["exit_id"], expected, output)
        self.assertEqual((path.read_bytes(), path.stat().st_mode), before)
        self.assertEqual(subprocess.check_output(["git", "status", "--porcelain"], cwd=path.parents[3]), sibling_status)

    def test_public_non_identity_changes_do_not_block_creation_but_selection_rejects(self):
        path = self.mixed_sibling()
        original = json.loads(path.read_text())
        for changes in ({"lifecycle_generation": "1"}, {"lifecycle_generation": None},
                        {"source": {"kind": "unknown"}}, {"status": None},
                        {"unexpected": "ordinary historical field"}):
            with self.subTest(changes=changes):
                path.write_text(json.dumps({**original, **changes}))
                before = (path.read_bytes(), path.stat().st_mode)
                completed, result = self.public_call(PACKAGE.parent, "guru-create-task", self.payload, validator="record_plan")
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
                self.assertEqual(result["status"], "ready")
                completed, selected = self.public_call(PACKAGE.parent, "guru-establish-task-identity", {
                    "profile": "active_task", "mode": "standalone", "task_id": "historical-task",
                    "task_ref": ".trellis/tasks/09-23-old", "lifecycle_generation": 1,
                }, root=path.parents[3])
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
                self.assertEqual(selected["reason_code"], "unsupported_legacy_task")
                self.assertEqual((path.read_bytes(), path.stat().st_mode), before)
                self.assertFalse((self.root / self.ref).exists())

    def test_public_mixed_history_errors_report_locator_before_mutation(self):
        path = self.mixed_sibling()
        original = json.loads(path.read_text())
        cases = [(dict(original, id="example-task"), "invalid_task_state", "task_identity_already_exists"),
                 (dict(original, id="EXAMPLE-TASK"), "invalid_task_state", "task_identity_already_exists"),
                 (dict(original, id="bad/id"), "blocked", "invalid_task_id"),
                 ({k: v for k, v in original.items() if k != "id"}, "blocked", "invalid_task_id"),
                 ([], "blocked", "invalid_task_metadata"),
                 ("broken JSON", "blocked", "invalid_task_metadata")]
        before_branches = self.git("branch", "--list")
        before_worktrees = self.git("worktree", "list", "--porcelain")
        for metadata, exit_id, reason in cases:
            with self.subTest(reason=reason, metadata=metadata):
                path.write_text(metadata if isinstance(metadata, str) else json.dumps(metadata))
                before = (path.read_bytes(), path.stat().st_mode)
                completed, output = self.public_call(PACKAGE.parent, "guru-create-task", self.payload)
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
                self.assertEqual((output["exit_id"], output["reason_code"]), (exit_id, reason))
                self.assertTrue(output["diagnostic"]["field_path"].startswith(str(path.parent)))
                self.assertTrue(output["diagnostic"]["remediation"])
                if reason == "unsupported_legacy_task":
                    self.assertIn("guru-upgrade-installation", output["diagnostic"]["remediation"])
                validate_json(output, PACKAGE / "consumers/stop/production" / (
                    "invalid-task-state.schema.json" if exit_id == "invalid_task_state" else "blocked.schema.json"), "stop")
                self.assertEqual((path.read_bytes(), path.stat().st_mode), before)
                self.assertFalse((self.root / self.ref).exists())
                self.assertEqual(self.git("branch", "--list"), before_branches)
                self.assertEqual(self.git("worktree", "list", "--porcelain"), before_worktrees)
                self.assertFalse((self.root / ".git/trellis/task-resources/example-task").exists())
        # The normal objective preflight reports its declared invocation error,
        # rather than converting the lifecycle failure into internal_error.
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.json"
            input_path.write_text(json.dumps(self.payload))
            with self.assertRaises(MODULE.CommandError) as caught:
                MODULE.run(PACKAGE, {"id": "record-task-plan"}, ["--root", str(self.root), "--input", str(input_path)])
        self.assertEqual(caught.exception.code, "stale_identity")
        self.assertIn(str(path), caught.exception.field_path)
        completed, error = self.public_call(PACKAGE.parent, "guru-create-task", self.payload, validator="record_plan")
        self.assertEqual(completed.returncode, 3, completed.stdout + completed.stderr)
        self.assertEqual(error["code"], "stale_identity")
        self.assertIn(str(path), error["field_path"])
        self.assertIn("invalid_task_metadata", error["remediation"])

    def test_public_occupied_target_directory_refuses_before_mutation(self):
        directory = self.root / self.ref
        directory.mkdir(parents=True)
        before_branches = self.git("branch", "--list")
        before_worktrees = self.git("worktree", "list", "--porcelain")
        completed, output = self.public_call(PACKAGE.parent, "guru-create-task", self.payload)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(output["reason_code"], "task_identity_already_exists")
        self.assertEqual(output["diagnostic"]["field_path"], str(directory.resolve()))
        self.assertEqual(list(directory.iterdir()), [])
        self.assertEqual(self.git("branch", "--list"), before_branches)
        self.assertEqual(self.git("worktree", "list", "--porcelain"), before_worktrees)
        self.assertFalse((self.root / ".git/trellis/task-resources/example-task").exists())

    def test_optional_diagnostic_preserves_minimal_stop_contracts(self):
        for exit_id, suffix in (("blocked", "blocked"), ("invalid_task_state", "invalid-task-state")):
            minimal = {"exit_id": exit_id, "reason_code": "example"}
            for schema in (PACKAGE / f"schemas/public-{suffix}-output.schema.json",
                           PACKAGE / f"consumers/stop/production/{suffix}.schema.json",
                           PACKAGE / "schemas/public-output.schema.json"):
                validate_json(minimal, schema, "minimal")
                validate_json({**minimal, "diagnostic": {"field_path": "record/task.json", "remediation": "Review this record."}}, schema, "diagnostic")
                with self.assertRaises(MODULE.CommandError):
                    validate_json({**minimal, "diagnostic": {"field_path": "record/task.json"}}, schema, "invalid")

    def test_clean_installed_mixed_history_public_creation_and_rejection(self):
        installer = SOURCE / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"
        (self.root / ".trellis/workflow.md").write_bytes((SOURCE / "trellis/workflows/guru-team/workflow.md").read_bytes())
        (self.root / ".gitignore").write_text(".trellis/.runtime/\n")
        applied = subprocess.run([sys.executable, str(installer), "--repo", str(self.root), "--json"],
                                 text=True, capture_output=True)
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
        self.git("add", ".")
        self.git("commit", "-qm", "install current preset")
        head = self.git("rev-parse", "HEAD")
        self.git("branch", "-f", "main", head)
        self.payload["creation"]["reviewed_base_head"] = head
        self.payload["acquisition"]["decision_head"] = head
        path = self.mixed_sibling()
        before = (path.read_bytes(), path.stat().st_mode)
        packages = self.root / ".trellis/guru-team/skills/packages"
        bad = json.loads(path.read_text()); bad["id"] = "bad/id"
        path.write_text(json.dumps(bad))
        failed, output = self.public_call(packages, "guru-create-task", self.payload)
        self.assertEqual(failed.returncode, 0, failed.stdout + failed.stderr)
        self.assertEqual(output["reason_code"], "invalid_task_id")
        self.assertIn(str(path.parent), output["diagnostic"]["field_path"])
        self.assertFalse((self.root / self.ref).exists())
        path.write_bytes(before[0])
        completed, plan = self.public_call(packages, "guru-create-task", self.payload, validator="record_plan")
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(plan["status"], "ready")
        completed, selected = self.public_call(packages, "guru-establish-task-identity", {
            "profile": "active_task", "mode": "standalone", "task_id": "historical-task",
            "task_ref": ".trellis/tasks/09-23-old", "lifecycle_generation": 1,
        }, root=path.parents[3])
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(selected["reason_code"], "unsupported_legacy_task")
        completed, created = self.public_call(packages, "guru-create-task", self.payload)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(created["exit_id"], "created", created)
        for skill, data, expected in (
            ("guru-ensure-task-checkout", {"profile": "active_task", "mode": "workflow", "task_id": "example-task", "lifecycle_generation": 0}, "checkout_resolved"),
            ("guru-bind-task-session", {"profile": "resume_current_task", "mode": "standalone", "task_id": "example-task", "lifecycle_generation": 0, "continuation_id": "installed-resume"}, "session_resumed"),
            ("guru-establish-task-identity", {"profile": "active_task", "mode": "standalone", "task_id": "example-task", "task_ref": self.ref, "lifecycle_generation": 0}, "identity_established"),
            ("guru-create-task", {**self.payload, "action": "recover_created_task_result"}, "created"),
        ):
            completed, result = self.public_call(packages, skill, data)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertEqual(result["exit_id"], expected, result)
        self.assertEqual((path.read_bytes(), path.stat().st_mode), before)

    def test_public_reference_only_creation_recovery_and_source_identity(self) -> None:
        self.assert_public_creation_and_recovery({"kind": "issue", "repo_ref": "castbox/guru-trellis",
                                                 "number": 490, "disposition": "reference_only"})

    def test_public_exact_source_creation_recovery_and_source_identity(self) -> None:
        self.assert_public_creation_and_recovery({"kind": "issue", "repo_ref": "castbox/guru-trellis",
                                                 "number": 490, "disposition": "exact_source"})

    def test_public_no_issue_creation_recovery_and_source_identity(self) -> None:
        self.assert_public_creation_and_recovery({"kind": "no_issue"})

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
