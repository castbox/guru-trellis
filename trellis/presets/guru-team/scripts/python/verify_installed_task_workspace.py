#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def run(*args: str, cwd: Path) -> str:
    return subprocess.run(
        list(args), cwd=cwd, check=True, text=True, capture_output=True
    ).stdout.strip()


def load_runtime(installed_repo: Path):
    runtime_path = (
        installed_repo
        / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
    )
    spec = importlib.util.spec_from_file_location(
        "installed_task_workspace_runtime", runtime_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load installed runtime: {runtime_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def digest(token: str, value: str) -> str:
    return hashlib.sha256(f"{token}:{value}".encode()).hexdigest()


def prerequisite_payloads(
    *, issue_number: int, token: str, base_head: str, title: str, body: str
) -> dict[str, dict[str, Any]]:
    disposition = digest(token, "disposition")
    duplicate = digest(token, "duplicate")
    return {
        "base": {
            "skill_id": "guru-sync-base",
            "status": "synced",
            "facts_sha256": digest(token, "base-facts"),
            "resolution": {"selected_base": "main", "remote": "origin"},
            "decision_checkout": {"head_after": base_head},
            "git": {
                "local_head_after": base_head,
                "remote_head_after": base_head,
                "remote_ref": "main",
            },
        },
        "context": {
            "skill_id": "guru-discover-change-context",
            "typed_exit": "context_ready",
            "snapshot_identity": {
                "snapshot_sha256": digest(token, "snapshot"),
                "live_change_sha256": digest(token, "live-change"),
            },
            "fixture": token,
        },
        "clarity": {
            "skill_id": "guru-clarify-requirements",
            "typed_exit": "clear",
            "content_identity": {
                "result_sha256": digest(token, "clarity-result"),
                "content_sha256": digest(token, "clarity-content"),
                "context_sha256": digest(token, "clarity-context"),
            },
            "review_target": {"state": "open"},
            "target_disposition": {
                "disposition_digest": disposition,
                "duplicate_facts_sha256": duplicate,
            },
        },
        "wording": {
            "skill_id": "guru-review-contract-wording",
            "typed_exit": "pass",
            "facts_sha256": digest(token, "wording-facts"),
            "scope": {"scope_sha256": digest(token, "wording-scope")},
            "scan": {"scan_sha256": digest(token, "wording-scan")},
        },
        "readiness": {
            "skill_id": "guru-review-change-request",
            "typed_exit": "ready",
            "facts_sha256": digest(token, "readiness-facts"),
            "target": {
                "kind": "existing_issue",
                "repo": "example/installed-fixture",
                "issue_number": issue_number,
                "url": f"https://github.com/example/installed-fixture/issues/{issue_number}",
                "updated_at": "2026-07-18T00:00:00Z",
                "title_sha256": hashlib.sha256(title.encode()).hexdigest(),
                "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
                "content_sha256": digest(token, "readiness-content"),
            },
            "evidence_linkage": {
                "linkage_sha256": digest(token, "readiness-linkage")
            },
            "semantic_review": {
                "scope_conclusion": {
                    "close_issues": [issue_number],
                    "related_issues": [],
                    "followup_issues": [],
                }
            },
        },
    }


def build_plan(
    runtime: Any, source: Path, *, issue_number: int, token: str, base_head: str
) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    title = "Verify installed task workspace execution"
    body = "Execute the installed task workspace runtime without developer identity."
    payloads = prerequisite_payloads(
        issue_number=issue_number,
        token=token,
        base_head=base_head,
        title=title,
        body=body,
    )
    readiness_target = payloads["readiness"]["target"]
    readiness_target["identity_sha256"] = runtime.context_digest(
        runtime.change_request_review_target_identity_projection(readiness_target)
    )
    readiness_target["content_sha256"] = runtime.context_digest(
        {
            "title_sha256": readiness_target["title_sha256"],
            "body_sha256": readiness_target["body_sha256"],
        }
    )
    readiness_prerequisites = {
        "context": {
            "payload_sha256": runtime.context_digest(payloads["context"]),
            "status": "current",
            "error_codes": [],
            "base_head": base_head,
            "current_state_sha256": digest(token, "current-state"),
            "history_sha256": digest(token, "history"),
            "duplicate_sha256": digest(token, "duplicate"),
        },
        "clarity": {
            "payload_sha256": runtime.context_digest(payloads["clarity"]),
            "status": "current",
            "error_codes": [],
            "facts_sha256": payloads["clarity"]["content_identity"]["result_sha256"],
            "disposition_sha256": payloads["clarity"]["target_disposition"]["disposition_digest"],
        },
        "wording": {
            "payload_sha256": runtime.context_digest(payloads["wording"]),
            "status": "current",
            "error_codes": [],
            "facts_sha256": payloads["wording"]["facts_sha256"],
        },
    }
    readiness_linkage = runtime.change_request_review_linkage(
        readiness_target, readiness_prerequisites
    )
    payloads["readiness"]["prerequisites"] = readiness_prerequisites
    payloads["readiness"]["evidence_linkage"] = readiness_linkage
    scope_conclusion = payloads["readiness"]["semantic_review"]["scope_conclusion"]
    payloads["readiness"]["semantic_review"]["ai_review_gate"] = {
        "reviewed_linkage_sha256": readiness_linkage["linkage_sha256"],
        "scope_conclusion_sha256": runtime.context_digest(scope_conclusion),
    }
    input_root = source / ".fixture-inputs" / token
    input_root.mkdir(parents=True)
    prerequisites: dict[str, dict[str, Any]] = {}
    for key, payload in payloads.items():
        relative = f".fixture-inputs/{token}/{key}.json"
        path = source / relative
        runtime.write_json(path, payload)
        prerequisites[key] = runtime.task_workspace_prerequisite_projection(
            key, relative, payload, hashlib.sha256(path.read_bytes()).hexdigest()
        )

    task_slug = f"{issue_number}-installed-task-workspace"
    task_dir = f".trellis/tasks/{datetime.now().strftime('%m-%d')}-{task_slug}"
    target_url = f"https://github.com/example/installed-fixture/issues/{issue_number}"
    scope_item = {
        "number": issue_number,
        "url": target_url,
        "title": title,
        "reason": "Installed runtime no-developer execution fixture.",
    }
    plan: dict[str, Any] = {
        "schema_version": "1.0",
        "skill_id": "guru-create-task-workspace",
        "generated_at": "2026-07-18T00:00:00Z",
        "mode": "workflow",
        "invocation": {
            "caller": "guru-review-change-request:ready",
            "target_kind": "existing_issue",
            "action_scope": "workspace_and_task_mutation",
            "resume_identity": "installed-no-developer-fixture",
        },
        "prerequisites": prerequisites,
        "target": {
            "kind": "existing_issue",
            "repo": "example/installed-fixture",
            "issue_number": issue_number,
            "url": target_url,
            "state": "open",
            "updated_at": "2026-07-18T00:00:00Z",
            "title_sha256": hashlib.sha256(title.encode()).hexdigest(),
            "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
            "draft": None,
            "disposition_sha256": payloads["clarity"]["target_disposition"][
                "disposition_digest"
            ],
            "duplicate_decision_sha256": payloads["clarity"][
                "target_disposition"
            ]["duplicate_facts_sha256"],
            "created_issue_binding_sha256": None,
        },
        "scope": {
            "primary": scope_item,
            "close": [scope_item],
            "related": [],
            "followup": [],
            "scope_sha256": "0" * 64,
        },
        "base": {
            "selected_base": "main",
            "remote": "origin",
            "base_ref": "main",
            "decision_head": base_head,
            "local_head": base_head,
            "remote_head": base_head,
            "sync_facts_sha256": payloads["base"]["facts_sha256"],
        },
        "naming": {
            "branch_name": f"feat/{task_slug}",
            "workspace_slug": task_slug,
            "task_slug": task_slug,
            "task_title": f"#{issue_number} Verify installed task workspace",
            "reason": "Names bind the issue number and installed workspace action.",
            "branch_disposition": "create_new",
            "workspace_disposition": "create_new",
            "task_disposition": "create_new",
        },
        "assignee": {
            "login": "fixture-maintainer",
            "source": "explicit_input",
            "candidates": [],
            "resolution_evidence": "The fixture provides the exact reviewed assignee.",
        },
        "side_effects": {
            "operations": [
                "create_branch",
                "create_worktree",
                "create_task",
                "write_task_artifacts",
                "write_runtime_mappings",
            ],
            "task_artifacts": [
                f"{task_dir}/{name}"
                for name in runtime.TASK_WORKSPACE_ARTIFACT_NAMES
            ],
            "runtime_mappings": [
                f".trellis/.runtime/guru-team/workspaces/{task_slug}.json",
                f".trellis/.runtime/guru-team/tasks/{task_slug}.json",
            ],
            "command_argv": [
                "create-task-workspace",
                "--input",
                f".fixture-inputs/{token}/plan.json",
            ],
            "stop_after": "created_workspace",
        },
        "confirmations": {
            "github_issue_mutation": {
                "status": "not_in_current_invocation",
                "source": None,
                "reviewed_plan_sha256": None,
                "evidence": None,
                "confirmation_sha256": None,
            },
            "workspace_and_task_mutation": {
                "status": "confirmed",
                "source": "explicit_user_confirmation",
                "reviewed_plan_sha256": "0" * 64,
                "evidence": "The exact disposable workspace mutation is confirmed.",
                "confirmation_sha256": "0" * 64,
            },
        },
        "ai_review_gate": {
            "status": "passed",
            "reviewer": "installed task workspace verifier",
            "reviewed_plan_sha256": "0" * 64,
            "summary": "The target, names, assignee and isolated metadata are complete.",
            "evidence": [
                "The invocation authorizes exactly one disposable workspace and task.",
                "Source and target developer identity and workspace journal are absent.",
            ],
        },
        "freshness": {
            "captured_at": "2026-07-18T00:00:00Z",
            "reviewable_plan_sha256": "0" * 64,
            "plan_sha256": "0" * 64,
        },
    }
    plan["scope"]["scope_sha256"] = runtime.task_workspace_scope_digest(
        plan["scope"]
    )
    reviewable = runtime.context_digest(
        runtime.task_workspace_reviewable_projection(plan)
    )
    confirmation = plan["confirmations"]["workspace_and_task_mutation"]
    confirmation["reviewed_plan_sha256"] = reviewable
    confirmation["confirmation_sha256"] = runtime.task_workspace_confirmation_digest(
        confirmation
    )
    plan["ai_review_gate"]["reviewed_plan_sha256"] = reviewable
    plan["freshness"]["reviewable_plan_sha256"] = reviewable
    plan["freshness"]["plan_sha256"] = runtime.task_workspace_plan_digest(plan)
    plan_path = input_root / "plan.json"
    runtime.write_json(plan_path, plan)
    live_issue = {
        "repo": "example/installed-fixture",
        "issue_number": issue_number,
        "url": target_url,
        "state": "open",
        "updated_at": "2026-07-18T00:00:00Z",
        "title_sha256": plan["target"]["title_sha256"],
        "body_sha256": plan["target"]["body_sha256"],
        "title": title,
        "body": body,
        "assignees": [],
    }
    return plan_path, plan, live_issue


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--installed-repo", required=True)
    parser.add_argument("--work-root", required=True)
    args = parser.parse_args()
    installed_repo = Path(args.installed_repo).resolve()
    work_root = Path(args.work_root).resolve()
    source = work_root / "installed-task-workspace-source"
    worktrees = work_root / "installed-task-worktrees"
    if source.exists() or worktrees.exists():
        raise RuntimeError("installed task workspace fixture paths already exist")
    source.mkdir(parents=True)
    runtime = load_runtime(installed_repo)

    shutil.copytree(
        installed_repo / ".trellis/scripts",
        source / ".trellis/scripts",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )
    schema_source = (
        installed_repo
        / ".trellis/guru-team/skills/packages/guru-create-task-workspace/schemas"
    )
    schema_target = (
        source
        / ".trellis/guru-team/skills/packages/guru-create-task-workspace/schemas"
    )
    schema_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(schema_source, schema_target)
    (source / ".trellis/guru-team/config.yml").write_text(
        f"workspace_mode: worktree\nworktree_root: {worktrees}\n",
        encoding="utf-8",
    )
    (source / ".trellis/config.yaml").write_text(
        "session_auto_commit: false\n", encoding="utf-8"
    )
    (source / ".gitignore").write_text(
        ".trellis/.runtime/\n__pycache__/\n*.py[cod]\n", encoding="utf-8"
    )
    (source / "README.md").write_text(
        "# Installed task workspace fixture\n", encoding="utf-8"
    )
    run("git", "init", "-q", cwd=source)
    run("git", "branch", "-M", "main", cwd=source)
    run("git", "config", "user.name", "Installed Fixture", cwd=source)
    run("git", "config", "user.email", "installed-fixture@example.invalid", cwd=source)
    run("git", "add", ".", cwd=source)
    run("git", "commit", "-qm", "fixture base", cwd=source)
    base_head = run("git", "rev-parse", "HEAD", cwd=source)

    plan_path, plan, live_issue = build_plan(
        runtime,
        source,
        issue_number=112,
        token="installed",
        base_head=base_head,
    )
    real_prepare_workspace = runtime.prepare_workspace

    def prepare_and_copy_inputs(*call_args: Any, **call_kwargs: Any):
        mode, workspace, ready = real_prepare_workspace(*call_args, **call_kwargs)
        if ready and workspace.resolve() != source.resolve():
            shutil.copytree(
                plan_path.parent,
                workspace / ".fixture-inputs/installed",
                dirs_exist_ok=True,
            )
        return mode, workspace, ready

    runtime.task_workspace_prerequisite_errors = lambda *_args, **_kwargs: []
    runtime.task_workspace_live_issue = lambda *_args, **_kwargs: copy.deepcopy(
        live_issue
    )
    runtime.prepare_workspace = prepare_and_copy_inputs
    command_args = argparse.Namespace(root=str(source), input=str(plan_path))
    recorded = runtime.cmd_record_task_workspace_plan(command_args)
    if recorded != plan:
        raise AssertionError("installed recorder changed the reviewed plan")
    result = runtime.cmd_create_task_workspace(
        argparse.Namespace(
            root=str(source),
            input=str(plan_path),
            cancelled=False,
            refresh_review=False,
            reason=None,
        )
    )
    result_path = plan_path.parent / "result.json"
    runtime.write_json(result_path, result)
    checked = runtime.cmd_check_task_workspace_result(
        argparse.Namespace(
            root=str(source), input=str(result_path), plan_input=str(plan_path)
        )
    )
    created = result["created_workspace"]
    workspace = worktrees / created["workspace_slug"]
    task_dir = workspace / created["task_artifact_dir"]
    if checked["checker"]["status"] != "passed":
        raise AssertionError(checked)
    if (source / ".trellis/.developer").exists() or (
        source / ".trellis/workspace"
    ).exists():
        raise AssertionError("installed runtime created source developer/workspace state")
    if (workspace / ".trellis/.developer").exists() or (
        workspace / ".trellis/workspace"
    ).exists():
        raise AssertionError("installed runtime created target developer/workspace state")
    expected_artifacts = set(runtime.TASK_WORKSPACE_ARTIFACT_NAMES)
    if {path.name for path in task_dir.iterdir() if path.is_file()} & expected_artifacts != expected_artifacts:
        raise AssertionError("installed runtime did not write all task-local Intake artifacts")
    print(
        json.dumps(
            {
                "status": "ok",
                "typed_exit": result["typed_exit"],
                "checker_status": checked["checker"]["status"],
                "task_artifact_dir": created["task_artifact_dir"],
                "artifact_names": sorted(expected_artifacts),
                "source_developer_identity": False,
                "target_developer_identity": False,
                "source_workspace_journal": False,
                "target_workspace_journal": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
