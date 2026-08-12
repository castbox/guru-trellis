#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


def run(*args: str, cwd: Path) -> str:
    return subprocess.run(
        list(args), cwd=cwd, check=True, text=True, capture_output=True
    ).stdout.strip()


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def run_json(wrapper: Path, root: Path, *args: str) -> dict[str, Any]:
    completed = subprocess.run(
        [str(wrapper), "--root", str(root), *args, "--json"],
        cwd=root,
        check=False,
        text=True,
        capture_output=True,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"installed wrapper returned invalid JSON: {wrapper}: "
            f"{completed.stdout or completed.stderr}"
        ) from exc
    if completed.returncode != 0 or not isinstance(payload, dict):
        raise AssertionError(
            f"installed wrapper failed: {wrapper}: {completed.returncode}: {payload}"
        )
    return payload


def build_plan(package: Path, source: Path, base_head: str) -> dict[str, Any]:
    sha = "1" * 64
    prerequisite = {
        "skill_id": "guru-sync-base",
        "schema_id": "fixture-result-1.0",
        "typed_exit": "synced",
        "artifact": "call-local:fixture",
        "payload_sha256": sha,
        "facts_sha256": sha,
        "content_sha256": None,
        "linkage_sha256": None,
    }
    plan: dict[str, Any] = {
        "schema_version": "2.0",
        "skill_id": "guru-create-task-workspace",
        "generated_at": "2026-08-12T00:00:00Z",
        "mode": "standalone",
        "invocation": {
            "caller": "installed-fixture",
            "target_kind": "existing_issue",
            "action_scope": "workspace_and_task_mutation",
            "resume_identity": "installed-package-public-fixture",
        },
        "prerequisites": {
            name: {
                **copy.deepcopy(prerequisite),
                "skill_id": skill_id,
                "typed_exit": typed_exit,
            }
            for name, skill_id, typed_exit in (
                ("base", "guru-sync-base", "synced"),
                ("clarity", "guru-clarify-requirements", "clear"),
                ("wording", "guru-review-contract-wording", "pass"),
                ("readiness", "guru-review-change-request", "ready"),
            )
        },
        "target": {
            "kind": "existing_issue",
            "repo": "example/installed-fixture",
            "issue_number": 112,
            "url": "https://github.com/example/installed-fixture/issues/112",
            "state": "open",
            "updated_at": "2026-08-12T00:00:00Z",
            "title_sha256": sha,
            "body_sha256": sha,
            "draft": None,
            "disposition_sha256": sha,
            "duplicate_decision_sha256": sha,
            "created_issue_binding_sha256": None,
            "created_issue_result": None,
        },
        "scope": {
            "primary": None,
            "close": [],
            "related": [],
            "followup": [],
            "scope_sha256": sha,
        },
        "base": {
            "selected_base": "main",
            "remote": "origin",
            "base_ref": "HEAD",
            "decision_head": base_head,
            "local_head": base_head,
            "remote_head": base_head,
            "post_sync_resolution_sha256": sha,
            "sync_facts_sha256": sha,
        },
        "naming": {
            "branch_name": "feat/112-installed-task-workspace",
            "workspace_slug": "112-installed-task-workspace",
            "task_slug": "112-installed-task-workspace",
            "task_title": "#112 Verify installed task workspace",
            "reason": "Bind the isolated fixture workspace to its issue.",
            "branch_disposition": "create_new",
            "workspace_disposition": "create_new",
            "task_disposition": "create_new",
        },
        "assignee": {
            "login": "fixture-maintainer",
            "source": "explicit_input",
            "candidates": [],
            "resolution_evidence": "The fixture provides the reviewed assignee.",
        },
        "side_effects": {
            "operations": [
                "create_branch",
                "create_worktree",
                "create_task",
                "write_task_artifacts",
                "write_runtime_mappings",
            ],
            "task_artifacts": [],
            "runtime_mappings": [],
            "command_argv": ["create-task-workspace", "--input", "plan.json"],
            "stop_after": "created_workspace",
        },
        "ai_review_gate": {
            "status": "passed",
            "reviewer": "installed task workspace verifier",
            "reviewed_plan_sha256": sha,
            "summary": "The isolated installed-package fixture is reviewed.",
            "evidence": ["The fixture has one bounded workspace mutation."],
        },
        "freshness": {
            "captured_at": "2026-08-12T00:00:00Z",
            "reviewable_plan_sha256": sha,
            "plan_sha256": sha,
        },
    }
    issue_number = 112
    task_slug = "112-installed-task-workspace"
    task_dir = f".trellis/tasks/{datetime.now().strftime('%m-%d')}-{task_slug}"
    issue_url = f"https://github.com/example/installed-fixture/issues/{issue_number}"
    plan["mode"] = "standalone"
    plan["invocation"].update(
        {
            "target_kind": "existing_issue",
            "action_scope": "workspace_and_task_mutation",
            "resume_identity": "installed-package-public-fixture",
        }
    )
    plan["target"].update(
        {
            "repo": "example/installed-fixture",
            "issue_number": issue_number,
            "url": issue_url,
            "state": "open",
            "draft": None,
            "created_issue_binding_sha256": None,
            "created_issue_result": None,
        }
    )
    scope_item = {
        "number": issue_number,
        "url": issue_url,
        "title": "Verify installed task workspace execution",
        "reason": "Exercise the installed package through its public commands.",
    }
    plan["scope"].update(
        {"primary": scope_item, "close": [copy.deepcopy(scope_item)], "related": [], "followup": []}
    )
    plan["scope"]["scope_sha256"] = digest(
        {key: value for key, value in plan["scope"].items() if key != "scope_sha256"}
    )
    plan["base"].update(
        {
            "selected_base": "main",
            "base_ref": "HEAD",
            "decision_head": base_head,
            "local_head": base_head,
            "remote_head": base_head,
        }
    )
    plan["naming"].update(
        {
            "branch_name": f"feat/{task_slug}",
            "workspace_slug": task_slug,
            "task_slug": task_slug,
            "task_title": f"#{issue_number} Verify installed task workspace",
            "branch_disposition": "create_new",
            "workspace_disposition": "create_new",
            "task_disposition": "create_new",
        }
    )
    plan["assignee"].update(
        {
            "login": "fixture-maintainer",
            "source": "explicit_input",
            "candidates": [],
            "resolution_evidence": "The fixture provides the exact reviewed assignee.",
        }
    )
    plan["side_effects"].update(
        {
            "task_artifacts": [f"{task_dir}/issue-scope-ledger.json"],
            "runtime_mappings": [
                f".trellis/.runtime/guru-team/workspaces/{task_slug}.json",
                f".trellis/.runtime/guru-team/tasks/{task_slug}.json",
            ],
        }
    )
    reviewable_keys = (
        "schema_version",
        "skill_id",
        "mode",
        "invocation",
        "prerequisites",
        "target",
        "scope",
        "base",
        "naming",
        "assignee",
        "side_effects",
    )
    reviewable_sha256 = digest({key: copy.deepcopy(plan[key]) for key in reviewable_keys})
    plan["ai_review_gate"].update(
        {
            "status": "passed",
            "reviewed_plan_sha256": reviewable_sha256,
            "summary": "The isolated installed-package fixture is fully reviewed.",
        }
    )
    plan["freshness"]["reviewable_plan_sha256"] = reviewable_sha256
    unsigned = copy.deepcopy(plan)
    unsigned["freshness"].pop("plan_sha256", None)
    plan["freshness"]["plan_sha256"] = digest(unsigned)
    return plan


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--installed-repo", required=True)
    parser.add_argument("--work-root", required=True)
    parser.add_argument("--existing-developer-identity", action="store_true")
    args = parser.parse_args()
    installed_repo = Path(args.installed_repo).resolve()
    work_root = Path(args.work_root).resolve()
    source = work_root / "installed-task-workspace-source"
    if source.exists():
        raise RuntimeError(f"installed task workspace fixture already exists: {source}")
    source.mkdir(parents=True)
    (source / ".trellis/guru-team").mkdir(parents=True)
    (source / ".trellis/guru-team/config.yml").write_text(
        "workspace_mode: worktree\nworktree_root:\nbase_branch: main\n"
    )
    (source / ".gitignore").write_text(
        ".trellis/.developer\n.trellis/.runtime/\n__pycache__/\n*.py[cod]\n"
    )
    (source / "README.md").write_text("# Installed task workspace fixture\n")
    run("git", "init", "-q", "-b", "main", cwd=source)
    run("git", "config", "user.name", "Installed Fixture", cwd=source)
    run("git", "config", "user.email", "installed-fixture@example.invalid", cwd=source)
    run("git", "add", ".", cwd=source)
    run("git", "commit", "-qm", "fixture base", cwd=source)
    base_head = run("git", "rev-parse", "HEAD", cwd=source)

    identity = source / ".trellis/.developer"
    identity_bytes = b"name=existing-installed-identity\n"
    if args.existing_developer_identity:
        identity.write_bytes(identity_bytes)

    package = (
        installed_repo
        / ".trellis/guru-team/skills/packages/guru-create-task-workspace"
    )
    wrappers = package / "scripts"
    plan = build_plan(package, source, base_head)
    plan_path = source / "plan.json"
    write_json(plan_path, plan)
    recorded = run_json(
        wrappers / "record-task-workspace-plan.sh", source, "--input", str(plan_path)
    )
    if recorded != plan:
        raise AssertionError("installed recorder changed the reviewed plan")
    result = run_json(
        wrappers / "create-task-workspace.sh", source, "--input", str(plan_path)
    )
    result_path = source / "result.json"
    write_json(result_path, result)
    checked = run_json(
        wrappers / "check-task-workspace-result.sh",
        source,
        "--plan-input",
        str(plan_path),
        "--input",
        str(result_path),
    )
    invocation_path = source / "invocation.json"
    write_json(invocation_path, {"result": checked})
    public_output = run_json(
        wrappers / "invoke.sh", source, "--invocation", str(invocation_path)
    )
    if public_output != {"exit_id": "created"}:
        raise AssertionError(f"unexpected installed public output: {public_output}")

    created = checked["created_workspace"]
    workspace = source.parent / f"{source.name}-worktrees" / created["workspace_slug"]
    task_dir = workspace / created["task_artifact_dir"]
    task_data = json.loads((task_dir / "task.json").read_text())
    ledger = task_dir / "issue-scope-ledger.json"
    if checked["checker"]["status"] != "passed" or not ledger.is_file():
        raise AssertionError("installed checker did not validate the created workspace")
    if task_data.get("creator") != "fixture-maintainer":
        raise AssertionError("installed runtime depended on developer identity for creator")
    if args.existing_developer_identity and identity.read_bytes() != identity_bytes:
        raise AssertionError("installed runtime changed source developer identity")
    target_identity = workspace / ".trellis/.developer"
    if target_identity.exists():
        raise AssertionError("installed runtime copied private developer identity")
    for mapping in plan["side_effects"]["runtime_mappings"]:
        if not (source / mapping).is_file():
            raise AssertionError(f"installed runtime did not write mapping: {mapping}")
    if (source / ".trellis/workspace").exists() or (workspace / ".trellis/workspace").exists():
        raise AssertionError("installed runtime created workspace journal state")

    print(
        json.dumps(
            {
                "status": "ok",
                "typed_exit": checked["typed_exit"],
                "checker_status": checked["checker"]["status"],
                "task_artifact_dir": created["task_artifact_dir"],
                "artifact_names": ["issue-scope-ledger.json"],
                "source_developer_identity": identity.exists(),
                "target_developer_identity": target_identity.exists(),
                "developer_identity_preserved": args.existing_developer_identity,
                "task_creator": task_data.get("creator"),
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
