from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

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
                    result = run_preset_install(installed)
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
        # The fixture supplies only owner decisions. The production recorder,
        # not a test reconstruction helper, derives every plan identity.
        authoring = {
            "naming": {"branch_name": "feat/" + slug, "workspace_slug": slug, "task_slug": slug, "task_title": "#145 Workspace authoring regression", "reason": "Isolated fixture verifies the published call contract.", "branch_disposition": "create_new", "workspace_disposition": "create_new", "task_disposition": "create_new"},
            "assignee": {"login": "stage0-transcript", "source": "single_issue_assignee", "candidates": ["stage0-transcript"], "resolution_evidence": "The fixture issue has one assignee."},
            "side_effects": {"operations": ["create_branch", "create_worktree", "create_task", "write_runtime_mappings"], "runtime_mappings": [f".trellis/.runtime/guru-team/workspaces/{slug}.json", f".trellis/.runtime/guru-team/tasks/{slug}.json"], "command_argv": ["create-task-workspace", "--invocation", "-"], "stop_after": "created_workspace"},
            "ai_review_gate": {"status": "passed", "reviewer": "integration-fixture", "summary": "The fixture decisions preserve the actual readiness scope and enumerate only disposable local effects.", "evidence": ["Actual readiness_current output", "Current fixture issue"]},
        }
        invocation = {"schema_version": "1.0", "transition": transition, "authoring": authoring}
        before = snapshot(root)
        plan = self.call(root, env, "record-task-workspace-plan.sh", invocation)
        self.assertEqual(snapshot(root), before)
        self.assertNotIn("scope", plan)
        self.assertNotIn("task_artifacts", plan["side_effects"])
        self.assertNotIn("write_task_artifacts", plan["side_effects"]["operations"])
        self.assertNotIn("content_sha256", plan["target"])
        self.assertEqual(plan["base"]["decision_head"], transition["base"]["decision_head"])
        invalid = copy.deepcopy(invocation)
        invalid["authoring"]["naming"].pop("branch_name")
        error = self.call(root, env, "record-task-workspace-plan.sh", invalid, expected=2)
        self.assertIn("branch_name", error["field_path"])
        error = self.call(root, env, "create-task-workspace.sh", plan, expected=2)
        self.assertIn("invocation", error["field_path"])
        self.assertEqual(snapshot(root), before)
        created_issue = self.checked_recovered_issue(root, env, transition, plan, issue)
        plan["target"].update(
            {
                "created_issue_binding_sha256": created_issue["created_issue"]["facts_sha256"],
                "created_issue_result": created_issue,
            }
        )
        self.refresh_plan(plan)
        plan = self.call(
            root,
            env,
            "record-task-workspace-plan.sh",
            {"schema_version": "1.0", "transition": transition, "plan": plan},
        )
        mutation = {"schema_version": "1.0", "transition": transition, "plan": plan}
        result = self.call(root, env, "create-task-workspace.sh", mutation)
        result = self.call(root, env, "check-task-workspace-result.sh", {**mutation, "result": result})
        public, _ = transcript.invoke_public(root, env, "guru-create-task-workspace", {"schema_version": "1.0", "public_input": {"profile": "execute_reviewed_plan", "mode": "workflow"}, "transition": transition, "owner_plan": plan, "owner_result": result}, "created")
        self.assertEqual(public, {"exit_id": "created"})
        created = result["created_workspace"]
        self.assertTrue(created["workspace_boundary_match"])
        self.assertEqual(created["issue_number"], issue["number"])
        self.assertEqual(created["task_status"], "planning")
        for mapping in created["runtime_mappings"]:
            self.assertTrue((root / mapping["path"]).is_file())
            self.assertTrue(mapping["ignored"])

    def checked_recovered_issue(self, root, env, transition, workspace_plan, issue):
        self.enable_exact_recovery(env, issue)
        draft = copy.deepcopy(workspace_plan)
        reviewed = transcript.digest(
            {"title": issue["title"], "body": issue["body"], "labels": []}
        )
        draft["invocation"].update(
            {"target_kind": "reviewed_draft", "action_scope": "github_issue_mutation"}
        )
        draft["target"].update(
            {
                "kind": "reviewed_draft",
                "issue_number": None,
                "url": None,
                "state": None,
                "updated_at": None,
                "draft": {
                    "draft_id": "installed-recovery",
                    "source_request_sha256": "1" * 64,
                    "title": issue["title"],
                    "body": issue["body"],
                    "labels": [],
                    "reviewed_draft_sha256": reviewed,
                },
                "created_issue_binding_sha256": None,
                "created_issue_result": None,
            }
        )
        draft["side_effects"].update(
            {
                "operations": ["create_issue"],
                "runtime_mappings": [],
                "command_argv": ["create-task-workspace", "--invocation", "-"],
                "stop_after": "created_issue_refresh",
            }
        )
        draft["freshness"]["captured_at"] = "2025-12-31T23:59:59Z"
        self.refresh_plan(draft)
        draft = self.call(
            root,
            env,
            "record-task-workspace-plan.sh",
            {"schema_version": "1.0", "transition": transition, "plan": draft},
        )
        mutation = {"schema_version": "1.0", "transition": transition, "plan": draft}
        result = self.call(root, env, "create-task-workspace.sh", mutation)
        checked = self.call(
            root,
            env,
            "check-task-workspace-result.sh",
            {**mutation, "result": result},
        )
        self.assertEqual(
            ("3.0", "created_issue", "refresh_review", "passed"),
            (
                checked["schema_version"],
                checked["variant"],
                checked["typed_exit"],
                checked["checker"]["status"],
            ),
        )
        self.assertNotIn("issue.create", transcript.operation_counts(env))
        return checked

    def enable_exact_recovery(self, env, issue):
        fake_gh = Path(shutil.which("gh", path=env["PATH"]) or "")
        self.assertTrue(fake_gh.is_file())
        original = fake_gh.with_name("gh-transcript-original")
        fake_gh.rename(original)
        recovery = {
            **issue,
            "createdAt": "2026-01-01T00:00:00Z",
            "labels": [],
        }
        fake_gh.write_text(
            f"#!{sys.executable}\n"
            "import json,subprocess,sys\n"
            f"original={str(original)!r}\n"
            f"recovery={recovery!r}\n"
            "args=sys.argv[1:]\n"
            "if args[:2]==['issue','list']:\n"
            " print(json.dumps([recovery]));raise SystemExit(0)\n"
            "raise SystemExit(subprocess.run([original,*args]).returncode)\n",
            encoding="utf-8",
        )
        fake_gh.chmod(0o755)

    def refresh_plan(self, plan):
        reviewable = {
            key: copy.deepcopy(plan[key])
            for key in (
                "schema_version",
                "skill_id",
                "mode",
                "invocation",
                "prerequisites",
                "target",
                "base",
                "naming",
                "assignee",
                "side_effects",
            )
        }
        reviewed = transcript.digest(reviewable)
        plan["ai_review_gate"]["reviewed_plan_sha256"] = reviewed
        plan["freshness"]["reviewable_plan_sha256"] = reviewed
        unsigned = copy.deepcopy(plan)
        unsigned["freshness"].pop("plan_sha256", None)
        plan["freshness"]["plan_sha256"] = transcript.digest(unsigned)
        return plan

    def call(self, root, env, command, envelope, expected=0):
        path = root / ".trellis/guru-team/skills/packages/guru-create-task-workspace/scripts" / command
        result = transcript.run([path, "--root", root, "--invocation", "-"], cwd=root, env=env, stdin=envelope, check=False)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)


if __name__ == "__main__":
    unittest.main()
