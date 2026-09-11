from __future__ import annotations

import copy
import datetime
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import verify_installed_phase0_transcript as transcript
from test_discovery_stdin_integration import run_preset_install
from test_readiness_transition_integration import producers, snapshot

SOURCE = Path(__file__).resolve().parents[5]


class WorkspaceInvocationIntegrationTests(unittest.TestCase):
    def test_published_authoring_to_created_initial_and_reapply(self):
        with tempfile.TemporaryDirectory(prefix="guru-389-installed-") as tmp:
            work = Path(tmp)
            installed = work / "installed"
            (installed / ".trellis").mkdir(parents=True)
            shutil.copy2(SOURCE / "trellis/workflows/guru-team/workflow.md", installed / ".trellis/workflow.md")
            shutil.copytree(SOURCE / ".trellis/scripts", installed / ".trellis/scripts", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            for phase in ("initial", "reapply"):
                with self.subTest(phase=phase):
                    result = run_preset_install(installed, all_platforms=True)
                    self.assertEqual(result.returncode, 0, result.stdout[-3000:] + result.stderr)
                    self.check_chain(installed, work / phase)

    def check_chain(self, installed, chain):
        root, env, source, source_path, _, _, wording, _, _ = producers(installed, chain)
        owner, checked = transcript.checked_readiness_owner_for_issue(root, env, wording["transition"], source_path, "ready")
        envelope = transcript.readiness_invocation(wording["transition"], source, owner)
        envelope["validation_receipt"] = checked["validation_receipt"]
        ready, _ = transcript.invoke_public(root, env, "guru-review-change-request", envelope, "ready")
        transition = ready["transition"]
        issue = transcript.live_issue(root, env)
        slug = "145-workspace-authoring-regression"
        task_dir = ".trellis/tasks/" + datetime.datetime.now().astimezone().strftime("%m-%d-") + slug
        scope_ref = {"number": issue["number"], "url": issue["url"], "title": issue["title"], "reason": "The fixture delivery unit has one primary and close issue."}
        # The fixture supplies only owner decisions. The production recorder,
        # not a test reconstruction helper, derives every plan identity.
        authoring = {
            "scope": {"primary": scope_ref, "close": [copy.deepcopy(scope_ref)], "related": [], "followup": []},
            "naming": {"branch_name": "feat/" + slug, "workspace_slug": slug, "task_slug": slug, "task_title": "#145 Workspace authoring regression", "reason": "Isolated fixture verifies the published call contract.", "branch_disposition": "create_new", "workspace_disposition": "create_new", "task_disposition": "create_new"},
            "assignee": {"login": "stage0-transcript", "source": "single_issue_assignee", "candidates": ["stage0-transcript"], "resolution_evidence": "The fixture issue has one assignee."},
            "side_effects": {"operations": ["create_branch", "create_worktree", "create_task", "write_task_artifacts", "write_runtime_mappings"], "task_artifacts": [task_dir + "/issue-scope-ledger.json"], "runtime_mappings": [f".trellis/.runtime/guru-team/workspaces/{slug}.json", f".trellis/.runtime/guru-team/tasks/{slug}.json"], "command_argv": ["create-task-workspace", "--invocation", "-"], "stop_after": "created_workspace"},
            "ai_review_gate": {"status": "passed", "reviewer": "integration-fixture", "summary": "The fixture decisions preserve the actual readiness scope and enumerate only disposable local effects.", "evidence": ["Actual readiness_current output", "Current fixture issue"]},
        }
        invocation = {"schema_version": "1.0", "transition": transition, "authoring": authoring}
        before = snapshot(root)
        plan = self.call(root, env, "record-task-workspace-plan.sh", invocation)
        self.assertEqual(snapshot(root), before)
        self.assertEqual(plan["scope"]["primary"], scope_ref)
        self.assertNotIn("content_sha256", plan["target"])
        self.assertEqual(plan["base"]["decision_head"], transition["base"]["decision_head"])
        invalid = copy.deepcopy(invocation)
        invalid["authoring"]["naming"].pop("branch_name")
        error = self.call(root, env, "record-task-workspace-plan.sh", invalid, expected=2)
        self.assertIn("branch_name", error["field_path"])
        error = self.call(root, env, "create-task-workspace.sh", plan, expected=2)
        self.assertIn("invocation", error["field_path"])
        self.assertEqual(snapshot(root), before)
        mutation = {"schema_version": "1.0", "transition": transition, "plan": plan}
        result = self.call(root, env, "create-task-workspace.sh", mutation)
        result = self.call(root, env, "check-task-workspace-result.sh", {**mutation, "result": result})
        public, _ = transcript.invoke_public(root, env, "guru-create-task-workspace", {"schema_version": "1.0", "public_input": {"profile": "execute_reviewed_plan", "mode": "workflow"}, "transition": transition, "owner_plan": plan, "owner_result": result}, "created")
        self.assertEqual(public, {"exit_id": "created"})
        created = result["created_workspace"]
        self.assertTrue(created["workspace_boundary_match"])
        self.assertFalse(created["workspace_journal_created"])
        self.assertEqual(created["issue_number"], issue["number"])
        self.assertEqual(created["task_status"], "planning")
        for mapping in created["runtime_mappings"]:
            self.assertTrue((root / mapping["path"]).is_file())
            self.assertTrue(mapping["ignored"])

    def call(self, root, env, command, envelope, expected=0):
        path = root / ".trellis/guru-team/skills/packages/guru-create-task-workspace/scripts" / command
        result = transcript.run([path, "--root", root, "--invocation", "-"], cwd=root, env=env, stdin=envelope, check=False)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)


if __name__ == "__main__":
    unittest.main()
