#!/usr/bin/env python3
"""Run a complete closeout transaction through an installed Guru Team preset."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = "owner/repo"
BASE_BRANCH = "main"


def run(command: list[str], cwd: Path, *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {' '.join(command)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def git(root: Path, real_git: str, *args: str) -> str:
    return run([real_git, *args], root).stdout.strip()


def write_executable(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def load_installed_companion(root: Path) -> Any:
    path = root / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
    spec = importlib.util.spec_from_file_location("installed_guru_team_trellis", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load installed companion: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def ensure_baseline(root: Path, real_git: str, remote: Path, after_update: bool) -> str:
    git(root, real_git, "config", "user.name", "Installed Closeout Smoke")
    git(root, real_git, "config", "user.email", "installed-closeout@example.com")
    if not remote.exists():
        run([real_git, "init", "--bare", "-q", str(remote)], root.parent)
    remotes = git(root, real_git, "remote").splitlines()
    if "origin" in remotes:
        git(root, real_git, "remote", "set-url", "origin", str(remote))
    else:
        git(root, real_git, "remote", "add", "origin", str(remote))

    current = git(root, real_git, "branch", "--show-current")
    if after_update and current != BASE_BRANCH:
        git(root, real_git, "switch", BASE_BRANCH)
    elif not current:
        git(root, real_git, "branch", "-M", BASE_BRANCH)
    git(root, real_git, "add", "-A")
    if git(root, real_git, "status", "--porcelain"):
        message = "chore: refresh installed assets" if after_update else "chore: install Guru Team preset"
        git(root, real_git, "commit", "-m", message)
    git(root, real_git, "push", "-u", "origin", BASE_BRANCH)
    return git(root, real_git, "rev-parse", "HEAD")


def valid_pr_body(issue: int) -> str:
    return f"""## 变更摘要

- 验证 clean throwaway 安装后的完整 closeout 事务。

## 影响范围

- 已安装 Guru Team finish-work wrapper
- task-local closeout artifacts

## 验证结果

- dry-run digest 与 formal expected digest 一致。
- draft、archive、三方 HEAD 与 ready 状态全部通过。

## Review Gate

- 最终放行审查 fixture 结论通过。
- Reviewed HEAD 绑定真实 Git commit。

## Docs SSOT

- 策略：no_docs_update_needed。
- durable docs：安装 smoke 不改变产品文档合同。
- task delta merge：无需要合并的任务 delta。
- task-history-only：仅保留本次 throwaway 验证证据。
- follow-up：无。

## Issue 关闭范围

- Closes #{issue}

## 安全说明

- fake GitHub store 不包含 token、secret、客户数据或签名 URL。
"""


def write_fixture(root: Path, gtt: Any, real_git: str, case_name: str, issue: int) -> tuple[Path, str, str]:
    branch = f"fix/{issue}-installed-closeout-{case_name}"
    git(root, real_git, "switch", "-C", branch, BASE_BRANCH)
    smoke_path = root / f"installed-closeout-{case_name}.txt"
    smoke_path.write_text(f"installed closeout smoke {case_name}\n", encoding="utf-8")
    git(root, real_git, "add", smoke_path.name)
    git(root, real_git, "commit", "-m", f"test(closeout): #{issue} 验证安装后收尾事务")
    reviewed_head = git(root, real_git, "rev-parse", "HEAD")
    base_head = git(root, real_git, "rev-parse", BASE_BRANCH)

    task_dir = root / ".trellis/tasks" / f"07-11-{issue}-installed-closeout-{case_name}"
    reviews_dir = task_dir / "reviews"
    reviews_dir.mkdir(parents=True)
    context = {
        "schema_version": "1.0",
        "source_issue": {
            "number": issue,
            "url": f"https://github.com/{REPO}/issues/{issue}",
            "title": "installed closeout smoke",
            "created_by_workflow": False,
        },
        "source_repo": {"repo": REPO, "url": f"https://github.com/{REPO}"},
        "task_slug": f"{issue}-installed-closeout-{case_name}",
        "task_title": f"#{issue} 验证安装后 closeout",
        "task_artifact_dir": task_dir.relative_to(root).as_posix(),
        "branch_name": branch,
        "base_branch": BASE_BRANCH,
        "base_ref": BASE_BRANCH,
        "base_head_sha": base_head,
        "remote_head_sha": base_head,
        "workspace_slug": "",
        "task_workspace_id": f"{issue}-installed-closeout-{case_name}",
        "assignee": "throwaway",
        "actor": {"login": "throwaway"},
        "issue_scope_ledger_seed": {},
        "intake_summary": {},
    }
    task = {
        "id": f"{issue}-installed-closeout-{case_name}",
        "name": f"{issue}-installed-closeout-{case_name}",
        "title": f"#{issue} 验证安装后 closeout",
        "status": "in_progress",
        "base_branch": BASE_BRANCH,
    }
    ledger = {
        "primary_issue": {"number": issue, "acceptance_evidence": ["installed closeout smoke passed"]},
        "close_issues": [{"number": issue, "acceptance_evidence": ["installed closeout smoke passed"]}],
        "related_issues": [],
        "followup_issues": [],
    }
    index = {
        "schema_version": 1,
        "index": {
            "problem": "安装产物缺少完整 closeout 开箱即用证据。",
            "outcome": "已安装 wrapper 完成 draft、archive 与 ready 事务。",
            "changed_behavior": ["throwaway 安装验证执行真实 closeout 事务。"],
            "affected_surfaces": [{
                "kind": "workflow",
                "name": "finish-work",
                "paths": [smoke_path.name],
                "change": "验证安装后的事务入口。",
            }],
            "contract_changes": [],
            "search_terms": {
                "commands": ["finish-work.sh"],
                "config_keys": [],
                "schema_fields": ["closeout_plan_digest"],
                "symbols": ["prepare_closeout"],
                "phrases": [
                    "旧 finish-work archive 后失败问题",
                    "closeout_plan_digest schema 合同",
                    "draft-to-ready 收尾事务已完成",
                ],
            },
        },
    }
    gtt.write_json(task_dir / "task-start-context.json", context)
    gtt.write_json(task_dir / "task.json", task)
    gtt.write_json(task_dir / "issue-scope-ledger.json", ledger)
    gtt.write_json(task_dir / "finish-summary-index.json", index)
    (task_dir / "pr-body.md").write_bytes(valid_pr_body(issue).encode("utf-8"))

    raw_report = reviews_dir / "round-001-final-release.md"
    raw_report.write_text(
        "# 最终放行审查原始报告\n\n## 证据\n\n- 完整安装 closeout fixture 已审查。\n\n## 结论\n\n- 0 findings，允许进入事务验证。\n",
        encoding="utf-8",
    )
    raw_digest = gtt.file_digest(root, raw_report)
    round_item = {
        "round": 1,
        "logical_role": "最终放行审查代理",
        "agent_id": f"installed-closeout-review-{issue}",
        "platform_nickname": "Installed Closeout Review",
        "reviewed_head": reviewed_head,
        "findings_count": 0,
        "reuse_policy": "最终放行审查代理必须是 fresh new agent，并完整审查当前 diff。",
        "reuse_decision": "new-agent",
        "review_report_path": raw_digest["path"],
        "review_report_sha256": raw_digest["sha256"],
        "review_report_size_bytes": raw_digest["size_bytes"],
        "review_report_modified_at": raw_digest["modified_at"],
    }
    assignment = {
        "schema_version": "1.1",
        "task": task_dir.relative_to(root).as_posix(),
        "head": reviewed_head,
        "agents": [{
            "logical_role": "最终放行审查代理",
            "agent_id": f"installed-closeout-review-{issue}",
            "platform_nickname": "Installed Closeout Review",
            "assigned_at": "2026-07-11T00:00:00Z",
            "assigned_head": reviewed_head,
            "reason": "installed closeout smoke fixture 独立审查。",
        }],
        "liveness": {},
        "review_rounds": [round_item],
        "reuse_decisions": [],
        "status_events": [],
    }
    gtt.write_json(task_dir / "agent-assignment.json", assignment)
    (task_dir / "review.md").write_text(
        "# 审查报告\n\n## 审查轮次\n\n- [Round 1](reviews/round-001-final-release.md)\n\n"
        "## 证据\n\n- 已审查安装后的完整 closeout fixture。\n\n## 结论\n\n- 0 findings，最终放行通过。\n",
        encoding="utf-8",
    )

    config = gtt.load_config(root)
    assignment_summary = gtt.summarize_agent_assignment(
        root, task_dir, task_dir / "agent-assignment.json", assignment
    )
    gate = gtt.build_review_gate_payload(
        root=root,
        task_dir=task_dir,
        config=config,
        task_context=context,
        base_branch=BASE_BRANCH,
        pass_gate=True,
        findings=[],
        observations=[],
        followup_candidates=[],
        command=["installed-closeout-smoke"],
        summary="安装后的完整 closeout fixture 已通过独立审查。",
        evidence=["真实 Git branch/bare remote 与安装 wrapper 将执行完整事务。"],
        reviewer=f"installed-closeout-review-{issue}",
        review_source="independent-agent",
        review_report=gtt.file_digest(root, task_dir / "review.md"),
        agent_assignment=assignment_summary,
        review_reports=gtt.review_reports_from_assignment(root, task_dir, assignment),
    )
    gtt.write_json(task_dir / "review-gate.json", gate)
    _path, _payload, gate_errors = gtt.validate_review_gate(root, task_dir, config, True)
    if gate_errors:
        raise RuntimeError("invalid installed closeout review gate: " + "; ".join(gate_errors))
    return task_dir, branch, reviewed_head


def install_fake_commands(fake_bin: Path) -> None:
    fake_bin.mkdir(parents=True, exist_ok=True)
    write_executable(
        fake_bin / "git",
        """#!/usr/bin/env python3
import os
import sys

args = sys.argv[1:]
if args[:2] == ["remote", "get-url"]:
    print("https://github.com/owner/repo.git")
    raise SystemExit(0)
real_git = os.environ["INSTALLED_CLOSEOUT_REAL_GIT"]
os.execv(real_git, [real_git, *args])
""",
    )
    write_executable(
        fake_bin / "gh",
        """#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path

args = sys.argv[1:]
store_path = Path(os.environ["INSTALLED_CLOSEOUT_PR_STORE"])
real_git = os.environ["INSTALLED_CLOSEOUT_REAL_GIT"]
remote = os.environ["INSTALLED_CLOSEOUT_REMOTE"]
branch = os.environ["INSTALLED_CLOSEOUT_BRANCH"]
number = int(os.environ["INSTALLED_CLOSEOUT_PR_NUMBER"])

def value(flag):
    return args[args.index(flag) + 1]

def remote_head():
    proc = subprocess.run(
        [real_git, "ls-remote", "--heads", remote, branch],
        text=True,
        capture_output=True,
        check=True,
    )
    rows = [line.split() for line in proc.stdout.splitlines() if line.strip()]
    return rows[0][0] if len(rows) == 1 else ""

def load():
    return json.loads(store_path.read_text(encoding="utf-8")) if store_path.exists() else None

def save(payload):
    store_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")

if args[:2] == ["auth", "status"]:
    raise SystemExit(0)
if args[:2] == ["pr", "list"]:
    payload = load()
    if payload:
        payload["headRefOid"] = remote_head()
        save(payload)
        print(json.dumps([{**payload, "headRefName": branch, "baseRefName": "main"}], ensure_ascii=False))
    else:
        print("[]")
    raise SystemExit(0)
if args[:2] == ["pr", "create"]:
    body = Path(value("--body-file")).read_text(encoding="utf-8")
    payload = {
        "number": number,
        "url": f"https://github.com/owner/repo/pull/{number}",
        "title": value("--title"),
        "body": body,
        "isDraft": True,
        "state": "OPEN",
        "headRefOid": remote_head(),
        "headRepository": {"nameWithOwner": "owner/repo"},
        "headRepositoryOwner": {"login": "owner"},
        "isCrossRepository": False,
    }
    save(payload)
    print(payload["url"])
    raise SystemExit(0)
if args[:2] == ["pr", "ready"]:
    payload = load()
    if not payload:
        raise SystemExit(2)
    payload["isDraft"] = False
    payload["headRefOid"] = remote_head()
    save(payload)
    raise SystemExit(0)
print("unsupported fake gh command: " + " ".join(args), file=sys.stderr)
raise SystemExit(2)
""",
    )


def run_closeout(root: Path, task_dir: Path, branch: str, issue: int, real_git: str, remote: Path) -> dict[str, Any]:
    wrapper = root / ".trellis/guru-team/scripts/bash/finish-work.sh"
    if not wrapper.is_file() or not os.access(wrapper, os.X_OK):
        raise RuntimeError(f"installed finish-work wrapper is missing or not executable: {wrapper}")
    fake_bin = root.parent / f"fake-closeout-bin-{issue}"
    install_fake_commands(fake_bin)
    store = root.parent / f"installed-closeout-pr-{issue}.json"
    store.unlink(missing_ok=True)
    env = dict(os.environ)
    env.update({
        "PATH": f"{fake_bin}{os.pathsep}{env.get('PATH', '')}",
        "INSTALLED_CLOSEOUT_REAL_GIT": real_git,
        "INSTALLED_CLOSEOUT_REMOTE": str(remote),
        "INSTALLED_CLOSEOUT_BRANCH": branch,
        "INSTALLED_CLOSEOUT_PR_NUMBER": str(issue),
        "INSTALLED_CLOSEOUT_PR_STORE": str(store),
    })
    task_rel = task_dir.relative_to(root).as_posix()
    common = [
        str(wrapper),
        "--root", str(root),
        "--json",
        "--from-trellis-finish-work",
        "--task", task_rel,
        "--repo", REPO,
        "--base-branch", BASE_BRANCH,
        "--remote", "origin",
        "--title", f"#{issue} 验证安装后 closeout",
        "--finish-summary-index-file", f"{task_rel}/finish-summary-index.json",
        "--body-file", f"{task_rel}/pr-body.md",
    ]
    dry = run([*common, "--dry-run"], root, env=env)
    dry_payload = json.loads(dry.stdout)
    digest = dry_payload["closeout_plan_digest"]
    formal = run([*common, "--expected-plan-digest", digest], root, env=env)
    payload = json.loads(formal.stdout)

    archived = Path(payload["archived_task_dir"])
    if not archived.is_dir() or task_dir.exists():
        raise RuntimeError("installed closeout did not move the active task to archive")
    local_head = git(root, real_git, "rev-parse", "HEAD")
    remote_rows = git(root, real_git, "ls-remote", "--heads", "origin", branch).split()
    remote_head = remote_rows[0] if remote_rows else ""
    pr = json.loads(store.read_text(encoding="utf-8"))
    if not (local_head == remote_head == pr.get("headRefOid")):
        raise RuntimeError("installed closeout local/remote/PR HEAD values differ")
    if pr.get("isDraft") is not False:
        raise RuntimeError("installed closeout PR did not transition to ready")
    if git(root, real_git, "status", "--porcelain"):
        raise RuntimeError("installed closeout left the throwaway repository dirty")
    summary = json.loads((archived / "finish-summary.json").read_text(encoding="utf-8"))
    expected_url = f"https://github.com/{REPO}/pull/{issue}"
    if summary["github"]["pr_url"] != expected_url:
        raise RuntimeError("installed closeout summary PR URL is not canonical")
    if summary["index"]["search_terms"]["pr_refs"] != [f"PR #{issue}"]:
        raise RuntimeError("installed closeout summary PR ref is not unique")
    return {
        "status": "ok",
        "issue": issue,
        "branch": branch,
        "digest": digest,
        "archived_task_dir": str(archived),
        "local_head": local_head,
        "remote_head": remote_head,
        "pr_head": pr["headRefOid"],
        "pr_url": pr["url"],
        "pr_ready": not pr["isDraft"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--case", choices=["initial", "after-update"], required=True)
    args = parser.parse_args()
    root = Path(args.repo).resolve()
    real_git = shutil.which("git")
    if not real_git:
        raise RuntimeError("git not found")
    remote = root.parent / "installed-closeout-remote.git"
    after_update = args.case == "after-update"
    ensure_baseline(root, real_git, remote, after_update)
    gtt = load_installed_companion(root)
    issue = 106 if after_update else 105
    task_dir, branch, _reviewed_head = write_fixture(root, gtt, real_git, args.case, issue)
    payload = run_closeout(root, task_dir, branch, issue, real_git, remote)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
