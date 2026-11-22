"""Exercise the source CLI with live Git worktrees and the installed Delivery API."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from uuid import uuid4

REPO = Path(__file__).resolve().parents[4]
GURU = REPO / "trellis/skills/guru-team"
WORKFLOW = REPO / "trellis/workflows/guru-team/workflow.md"
CLI = WORKFLOW.parent / "scripts/bash/read-continuation-context.sh"
sys.path.insert(0, str(GURU))

from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.delivery_projection.tests.upstream_fixture import scripts_source

CONTEXT = "continuation-reader-test"


def fixture_owner(name):
    path = GURU / "packages" / name / "runtime/invoke.py"
    spec = importlib.util.spec_from_file_location("fixture_" + name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def files(root):
    return {
        path.relative_to(root).as_posix(): (path.read_bytes(), path.stat().st_mode)
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


class ReadContinuationContextTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="guru-continuation-")
        self.addCleanup(self.temporary.cleanup)
        base = Path(self.temporary.name).resolve()
        self.root = base / "main"
        self.root.mkdir()
        self.environment = {
            **os.environ,
            "TRELLIS_CONTEXT_ID": CONTEXT,
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        self.git("init", "-qb", "main")
        self.git("config", "user.name", "Continuation Fixture")
        self.git("config", "user.email", "continuation@example.invalid")
        trellis = self.root / ".trellis"
        shutil.copytree(scripts_source(), trellis / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy2(WORKFLOW, trellis / "workflow.md")
        (trellis / ".developer").write_text("continuation-fixture\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Install reviewed fixture")
        self.workspaces = {name: base / name for name in ("a", "b")}
        self.refs = {name: ".trellis/tasks/" + name for name in self.workspaces}
        # Use current original writers to establish both Task identities (including
        # their branch and checkout controls) in the throwaway repository.
        for name, checkout in self.workspaces.items():
            self.git("worktree", "add", "-qb", f"task/{name}", str(checkout), "main")
            self.command([
                sys.executable, ".trellis/scripts/task.py", "create", f"Task {name}",
                "--description", "Continuation CLI fixture", "--slug", name,
                "--task-id", name, "--schema-version", "2.0",
                "--source-json", '{"kind":"no_issue"}', "--base-branch", "main", "--no-start",
            ], cwd=checkout)
            task = next((checkout / ".trellis/tasks").glob("*/task.json")).parent
            self.refs[name] = task.relative_to(checkout).as_posix()
            self.git("add", self.refs[name], cwd=checkout)
            self.git("commit", "-qm", f"Create Task {name}", cwd=checkout)
            selected = {
                "profile": "delivery_active_task", "mode": "standalone",
                "task_id": name, "task_ref": self.refs[name], "lifecycle_generation": 0,
            }
            result = fixture_owner("guru-establish-task-branch-binding").invoke(
                checkout, {**selected, "action": "establish"},
            )
            self.assertEqual(result["exit_id"], "binding_established", result)

    def command(self, argv, *, cwd=None, environment=None, payload=None, exit_code=0):
        result = subprocess.run(
            argv, cwd=cwd or self.root, env=environment or self.environment,
            input=payload, capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(result.returncode, exit_code, result.stderr + result.stdout)
        return result.stdout

    def git(self, *args, cwd=None):
        return self.command(["git", *args], cwd=cwd)

    def task_pin(self, name):
        return {
            "task_id": name, "lifecycle_generation": 0, "task_ref": self.refs[name],
        }

    def bind(self, name, *, current=None):
        public = {
            "profile": "delivery_switch_task" if current else "delivery_rebind_missing_session",
            "mode": "standalone", "task_id": name, "lifecycle_generation": 0,
            "continuation_id": "continuation-fixture",
        }
        if current:
            public.update(current_task_id=current, current_lifecycle_generation=0)
        semantic = {
            **public, "route": "switch" if current else "rebind", "resume_target": "phase-2",
            "ai_review_gate": {"status": "passed", "summary": "Bind the isolated test session."},
        }
        with patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": CONTEXT, "PYTHONDONTWRITEBYTECODE": "1"}):
            result = fixture_owner("guru-bind-task-session").execute(
                self.workspaces[name], json.dumps(public), json.dumps(semantic),
            )
        self.assertEqual(result["exit_id"], "task_switched" if current else "session_rebound", result)

    def make_delivery(self, name):
        pin = self.task_pin(name)
        projection = DeliveryProjection(self.workspaces[name], pin.pop("task_ref"))
        scope = authority_ref(projection.task_dir / "prd.md", projection.root)
        if not projection.read_record()["accepted_scope"]:
            projection.scope(scope)
        key = {**pin, "delivery_id": str(uuid4())}
        projection.apply({
            "api_version": "1.0", "operation": "create_delivery",
            "key": key, "owner_role": "creation", "owner_id": "guru-create-delivery",
            "profile": "pull_request", "scope_ref": {"authority": scope, "anchors": ["scope"]},
        })
        return projection, key

    def select(self, name, key):
        selected = self.command([
            sys.executable, ".trellis/scripts/delivery.py", "select", "--task",
            self.refs[name], "--delivery", key["delivery_id"],
        ], cwd=self.workspaces[name])
        self.assertEqual(json.loads(selected)["key"], key)

    def snapshot(self):
        return (
            self.git("for-each-ref"), self.git("worktree", "list", "--porcelain"),
            files(self.root / ".git/trellis"),
            files(self.root / ".trellis/.runtime"),
            files(self.root / ".trellis/tasks"),
            tuple(files(path / ".trellis/tasks") for path in self.workspaces.values()),
            tuple(files(path / ".trellis/.runtime") for path in self.workspaces.values()),
        )

    def query(self, data=None, *, exit_code=0):
        argv = ["bash", str(CLI), "--root", str(self.root)]
        if data is not None:
            argv.extend(["--input", "-"])
        before = self.snapshot()
        response = self.command(
            argv, payload=json.dumps(data) if data is not None else None, exit_code=exit_code,
        )
        self.assertEqual(self.snapshot(), before, "The query changed Task, session, or Git resources")
        return json.loads(response)

    @staticmethod
    def request(intent="continue_session", **fields):
        return {"schema_version": "1.0", "intent": intent, **fields}

    def assert_task(self, result, name):
        self.assertEqual(result["task"], {
            **self.task_pin(name), "checkout_path": str(self.workspaces[name]),
        })

    def assert_delivery(self, result, key, phase):
        self.assertEqual(result["delivery"], {
            "delivery_id": key["delivery_id"], "phase": phase,
            "planning_root": "deliveries/" + key["delivery_id"],
        })

    def test_no_task_missing_binding_and_explicit_read_are_distinct(self):
        self.assertEqual(self.query(), {
            "schema_version": "1.0", "kind": "no_current_task", "mode": "session",
        })
        absent = self.query(self.request(task=self.task_pin("a")))
        self.assertEqual(absent["kind"], "binding_required", absent)
        self.assertEqual(absent["diagnostic"]["owner"], "guru-bind-task-session")
        explicit = self.query(self.request("inspect_task", task=self.task_pin("a")))
        self.assertEqual((explicit["kind"], explicit["mode"]), ("no_current_delivery", "explicit"))
        self.assert_task(explicit, "a")
        self.assertNotIn("reuse", explicit)
        self.assertEqual(self.query()["kind"], "no_current_task")

    def test_same_session_reuses_facts_and_refreshes_selection_and_task_switch(self):
        self.bind("a")
        no_delivery = self.query()
        self.assertEqual(no_delivery["kind"], "no_current_delivery")
        self.assert_task(no_delivery, "a")
        self.assertNotIn("delivery", no_delivery)
        _, first_key = self.make_delivery("a")
        _, second_key = self.make_delivery("a")
        self.select("a", first_key)
        first = self.query()
        self.assertEqual(first["kind"], "current")
        self.assert_delivery(first, first_key, "planning")
        self.assertEqual(self.query(self.request(previous=first)), first)
        self.select("a", second_key)
        changed = self.query(self.request(previous=first))
        self.assert_task(changed, "a")
        self.assert_delivery(changed, second_key, "planning")
        for dependency in ("origin", "task", "checkout"):
            self.assertEqual(first["reuse"][dependency], changed["reuse"][dependency])
        self.assertNotEqual(first["reuse"]["delivery"], changed["reuse"]["delivery"])
        self.bind("b", current="a")
        switched = self.query(self.request(previous=changed))
        self.assertEqual(switched["kind"], "no_current_delivery")
        self.assert_task(switched, "b")
        self.assertEqual(switched["reuse"]["origin"], changed["reuse"]["origin"])
        for dependency in ("task", "checkout"):
            self.assertNotEqual(switched["reuse"][dependency], changed["reuse"][dependency])

    def test_conflicting_assertion_does_not_replace_a_valid_session(self):
        self.bind("a")
        conflict = self.query(self.request(task=self.task_pin("b")), exit_code=1)
        self.assertEqual(conflict["kind"], "error")
        self.assertTrue(conflict["diagnostic"]["code"])
        self.assertTrue(conflict["diagnostic"]["remediation"])
        self.assert_task(self.query(), "a")

    def test_previous_facts_do_not_restore_a_detached_bound_checkout(self):
        self.bind("a")
        previous = self.query()
        self.assert_task(previous, "a")
        self.git("switch", "--detach", cwd=self.workspaces["a"])
        result = self.query(self.request(previous=previous), exit_code=1)
        self.assertEqual(result["kind"], "error")
        self.assertEqual(result["diagnostic"]["owner"], "guru-ensure-task-checkout")
        self.assertTrue(result["diagnostic"]["remediation"])

    def test_explicit_terminal_delivery_keeps_its_exact_phase(self):
        projection, key = self.make_delivery("a")
        scope = projection.read_record()["accepted_scope"]
        projection.apply({
            "api_version": "1.0", "operation": "stop", "key": key,
            "owner_role": "planning", "owner_id": "guru-activate-delivery",
            "expected_phase": "planning",
            "result": {
                "result_id": "continuation-stop", "owner_id": "guru-activate-delivery",
                "reason": scope, "scope_decision": scope, "evidence": [scope],
            },
        })
        terminal = self.query(self.request(
            "inspect_task", task=self.task_pin("a"), delivery_id=key["delivery_id"],
        ))
        self.assertEqual(terminal["kind"], "terminal_delivery", terminal)
        self.assert_task(terminal, "a")
        self.assert_delivery(terminal, key, "stopped")
        self.assertEqual(self.query()["kind"], "no_current_task")

    def test_exact_delivery_read_preserves_native_gate_applicability(self):
        self.bind("a")
        _, key = self.make_delivery("a")
        self.select("a", key)
        located = self.query()
        self.assertEqual(located["kind"], "current")
        self.assertEqual(located["delivery"]["phase"], "planning")
        native = json.loads(self.command(
            [sys.executable, ".trellis/scripts/delivery.py", "current", "--json"],
            cwd=self.workspaces["a"],
        ))
        self.assertEqual(native["key"], key)
        self.assertFalse(native["delivery"]["results"]["planning"])
        with self.subTest("exact read retains the original record and its result applicability"):
            payload = {"schema_version": "1.0", "task": self.task_pin("a"),
                       "delivery_id": located["delivery"]["delivery_id"]}
            before = self.snapshot()
            exact = json.loads(self.command([
                "bash", str(CLI), "--root", located["task"]["checkout_path"],
                "--delivery-record", "-",
            ], payload=json.dumps(payload)))
            self.assertEqual(self.snapshot(), before)
            for field in ("key", "delivery", "gate_applicability"):
                self.assertEqual(exact[field], native[field])

    def test_git_common_predecessor_preserves_native_maintenance_route(self):
        # Create the Task and its schema-2 session through the original writers.
        workflow = self.root / ".trellis/workflow.md"
        current = workflow.read_text()
        workflow.write_text("# Predecessor workflow\n")
        self.command([
            sys.executable, ".trellis/scripts/task.py", "create", "Predecessor",
            "--description", "Legacy diagnostic regression", "--slug", "predecessor",
            "--task-id", "predecessor", "--schema-version", "legacy", "--no-start",
        ])
        task = next((self.root / ".trellis/tasks").glob("*-predecessor/task.json"))
        self.command([
            sys.executable, ".trellis/scripts/task.py", "start",
            str(task.parent.relative_to(self.root)), "--allow-empty-context",
        ])
        workflow.write_text(current)
        native = json.loads(self.command(
            [sys.executable, ".trellis/scripts/delivery.py", "current", "--json"],
            exit_code=1,
        ))
        self.assertEqual(native["code"], "maintenance_required", native)
        self.assertIn("maintain inspect-task", native["message"])
        result = self.query(exit_code=1)
        self.assertEqual(result["kind"], "error")
        self.assertEqual(result["diagnostic"]["code"], native["code"])
        self.assertEqual(result["diagnostic"]["message"], native["message"])
        self.assertEqual(result["diagnostic"]["owner"], "guru-maintain-legacy-task")

    def test_known_predecessor_passes_through_native_diagnostic(self):
        # Use the old local carrier and predecessor record shape supported by
        # the native maintenance diagnostic. The current writers reject them.
        task = self.root / ".trellis/tasks/predecessor"
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps({
            "id": "predecessor", "name": "predecessor", "title": "Previous Task",
            "status": "in_progress", "creator": "fixture", "assignee": "fixture",
        }))
        carrier = self.root / ".trellis/.runtime/sessions" / f"{CONTEXT}.json"
        carrier.parent.mkdir(parents=True)
        carrier.write_text(json.dumps({"current_task": ".trellis/tasks/predecessor"}))
        native = json.loads(self.command(
            [sys.executable, ".trellis/scripts/delivery.py", "current", "--json"],
            exit_code=1,
        ))
        self.assertEqual(native["code"], "maintenance_required", native)
        self.assertIn("maintain inspect-task", native["message"])
        result = self.query(exit_code=1)
        self.assertEqual(result["kind"], "error")
        self.assertEqual(result["diagnostic"]["code"], native["code"])
        self.assertEqual(
            result["diagnostic"]["message"],
            native["message"].replace(f"/{CONTEXT}.json", "/<current-session>.json"),
        )
        self.assertEqual(result["diagnostic"]["owner"], "guru-maintain-legacy-task")

if __name__ == "__main__":
    unittest.main()
