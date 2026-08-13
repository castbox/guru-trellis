#!/usr/bin/env python3
"""Run a complete closeout transaction through an installed Guru Team preset."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


REPO = "microsoft/powertoys"
REMOTE_REPO = "microsoft/PowerToys"
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


def load_installed_eval_adapter(root: Path) -> Any:
    import importlib.util

    path = root / ".trellis/guru-team/skills/adapters/eval/native_adapter.py"
    spec = importlib.util.spec_from_file_location(
        "installed_guru_team_eval_adapter",
        path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load installed eval adapter: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class InstalledPackageClient:
    """Test authoring facade whose production operations use installed wrappers."""

    INDEPENDENT_REVIEW_SOURCE = "independent-agent"
    TASK_PUBLICATION_DIMENSIONS = (
        "diff_outcome_consistency",
        "issue_scope_closure",
        "pr_body_quality",
        "validation_claims",
        "branch_review_summary",
        "docs_ssot_reconciliation",
        "safety_deployment_impact",
        "finish_summary_semantics",
        "metadata_tail_integrity",
        "artifact_binding_freshness",
    )

    def __init__(self, root: Path, skill_id: str) -> None:
        self.root = root
        self.skill_id = skill_id
        self.package = root / ".trellis/guru-team/skills/packages" / skill_id
        self._last_review_gate: str | None = None

    @staticmethod
    def read_json(path: Path) -> dict[str, Any]:
        return read_json(path)

    @staticmethod
    def write_json(path: Path, payload: dict[str, Any]) -> None:
        write_json(path, payload)

    @staticmethod
    def current_head(root: Path) -> str:
        return run(["git", "rev-parse", "HEAD"], root).stdout.strip()

    @staticmethod
    def diff_base_ref(root: Path, base_branch: str) -> str:
        remote = f"origin/{base_branch}"
        probe = subprocess.run(
            ["git", "rev-parse", "--verify", remote],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        return remote if probe.returncode == 0 else base_branch

    @staticmethod
    def changed_files(root: Path, diff_range: str) -> list[str]:
        output = run(["git", "diff", "--name-only", diff_range], root).stdout
        return [line for line in output.splitlines() if line]

    @staticmethod
    def git_status_paths(root: Path) -> list[str]:
        output = run(
            ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
            root,
        ).stdout
        return sorted(
            field[3:].split(" -> ")[-1]
            for field in output.split("\0")
            if field
        )

    def _call(self, script: str, *arguments: str) -> dict[str, Any]:
        wrapper = self.package / "scripts" / script
        if not wrapper.is_file() or not os.access(wrapper, os.X_OK):
            raise RuntimeError(f"installed package wrapper is unavailable: {wrapper}")
        return json.loads(run([str(wrapper), *arguments], self.root).stdout)

    def cmd_record_planning_approval(self, args: argparse.Namespace) -> dict[str, Any]:
        values = ["--root", args.root, "--task", args.task, "--input", args.input]
        if args.dry_run:
            values.append("--dry-run")
        return self._call("record-planning-approval.sh", *values)

    def cmd_check_planning_approval(self, args: argparse.Namespace) -> dict[str, Any]:
        values = ["--root", args.root, "--task", args.task]
        if args.require_exit:
            values.extend(("--require-exit", args.require_exit))
        return self._call("check-planning-approval.sh", *values)

    def cmd_record_phase2_check(self, args: argparse.Namespace) -> dict[str, Any]:
        values = ["--root", args.root, "--task", args.task, "--input", args.input]
        if args.dry_run:
            values.append("--dry-run")
        return self._call("record-phase2-check.sh", *values)

    def cmd_check_phase2_check(self, args: argparse.Namespace) -> dict[str, Any]:
        return self._call(
            "check-phase2-check.sh", "--root", args.root, "--task", args.task
        )

    def build_task_commit_candidate(
        self,
        root: Path,
        task: Path,
        public_input: dict[str, Any],
        authoring: dict[str, Any],
    ) -> tuple[Path, dict[str, Any], dict[str, Any]]:
        staging = root / ".trellis/.runtime/guru-team/installed-closeout"
        public_path = staging / "task-commit-input.json"
        authoring_path = staging / "task-commit-authoring.json"
        write_json(public_path, public_input)
        write_json(authoring_path, authoring)
        prepared = self._call(
            "prepare-task-commit.sh",
            "--root", str(root),
            "--input", public_path.relative_to(root).as_posix(),
            "--candidate-json", authoring_path.relative_to(root).as_posix(),
        )
        candidate_path = root / prepared["candidate_artifact"]
        candidate = read_json(candidate_path)
        return candidate_path, candidate, candidate

    def execute_task_commit_candidate(
        self, root: Path, candidate: dict[str, Any], task: Path
    ) -> dict[str, Any]:
        del candidate
        candidates = sorted(
            (root / ".trellis/.runtime/guru-team/task-commit-plans" / task.name).glob("*.json")
        )
        if len(candidates) != 1:
            raise RuntimeError("installed task commit candidate is ambiguous")
        executed = self._call(
            "create-task-commit.sh",
            "--root", str(root),
            "--task", task.relative_to(root).as_posix(),
            "--candidate-artifact", candidates[0].relative_to(root).as_posix(),
        )
        run(["git", "reset", "--mixed", "HEAD"], root)
        return executed

    def cmd_review_branch(self, args: argparse.Namespace) -> dict[str, Any]:
        result = self._call(
            "review-branch.sh",
            "--root", args.root,
            "--task", args.task,
            "--skill-input", args.skill_input,
            "--semantic-review-file", args.semantic_review_file,
            "--typed-exit", args.typed_exit,
        )
        gate = self.root / ".trellis/.runtime/guru-team/installed-closeout/review-gate.json"
        write_json(gate, result)
        self._last_review_gate = gate.relative_to(self.root).as_posix()
        return result

    def cmd_check_review_gate(self, args: argparse.Namespace) -> dict[str, Any]:
        if not self._last_review_gate:
            raise RuntimeError("installed branch review gate was not recorded")
        values = [
            "--root", args.root,
            "--task", args.task,
            "--input", self._last_review_gate,
        ]
        if args.expected_exit:
            values.extend(("--expected-exit", args.expected_exit))
        return self._call("check-review-gate.sh", *values)


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
- `branch_review_commit` 绑定真实 Git commit，reviewed-content identity 已复核。

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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return payload


def write_fixture_runtime_mappings(root: Path, task_slug: str, task_dir: Path, branch: str) -> None:
    updated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    runtime = root / ".trellis/.runtime/guru-team"
    write_json(runtime / "workspaces" / f"{task_slug}.json", {
        "schema_version": "1.0",
        "workspace_slug": task_slug,
        "workspace_path": str(root),
        "source_checkout": str(root),
        "branch_name": branch,
        "updated_at": updated_at,
    })
    write_json(runtime / "tasks" / f"{task_slug}.json", {
        "schema_version": "1.0",
        "task_slug": task_slug,
        "workspace_slug": task_slug,
        "workspace_path": str(root),
        "task_artifact_dir": task_dir.relative_to(root).as_posix(),
        "updated_at": updated_at,
    })


def write_fixture(root: Path, owners: dict[str, Any], real_git: str, case_name: str, issue: int) -> tuple[Path, str, str]:
    branch = f"fix/{issue}-installed-closeout-{case_name}"
    git(root, real_git, "switch", "-C", branch, BASE_BRANCH)
    smoke_path = root / f"installed-closeout-{case_name}.txt"
    smoke_path.write_text(f"installed closeout smoke {case_name}\n", encoding="utf-8")
    git(root, real_git, "add", smoke_path.name)
    git(root, real_git, "commit", "-m", f"test(closeout): #{issue} 验证安装后收尾事务")
    task_dir = root / ".trellis/tasks" / f"07-11-{issue}-installed-closeout-{case_name}"
    task_dir.mkdir(parents=True)
    task_slug = f"{issue}-installed-closeout-{case_name}"
    task = {
        "id": task_slug,
        "name": task_slug,
        "title": f"#{issue} 验证安装后 closeout",
        "status": "in_progress",
        "branch": branch,
        "base_branch": BASE_BRANCH,
    }
    issue_entry = {
        "number": issue,
        "url": f"https://github.com/{REPO}/issues/{issue}",
        "title": f"#{issue} 验证安装后 closeout",
        "reason": "Installed closeout smoke fully covers this issue.",
    }
    ledger = {
        "schema_version": "2.0",
        "primary_issue": issue_entry,
        "close_issues": [dict(issue_entry)],
        "related_issues": [],
        "followup_issues": [],
    }
    write_json(task_dir / "task.json", task)
    write_json(task_dir / "issue-scope-ledger.json", ledger)
    write_fixture_runtime_mappings(root, task_slug, task_dir, branch)
    for name, content in (
        (
            "prd.md",
            "# 需求\n\n## R1. Production eval\n\n验证安装后的 closeout 事务。\n",
        ),
        ("design.md", "# 设计\n\n使用已安装 Guru Team runtime 完成收尾。\n"),
        ("implement.md", "# 实施\n\n先通过 publication gate，再执行 finish-work。\n"),
    ):
        (task_dir / name).write_text(content, encoding="utf-8")
    adapter = load_installed_eval_adapter(root)

    docs_path = root / "docs/requirements.md"
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    if not docs_path.exists():
        docs_path.write_text(
            "# Requirements\n\nInstalled closeout uses the checked publication gate.\n",
            encoding="utf-8",
        )
    design_path = task_dir / "design.md"
    design_path.write_text(
        "# 设计\n\n## Docs SSOT Plan\n\n"
        "Strategy: ssot_first. Durable requirements own the closeout contract.\n",
        encoding="utf-8",
    )
    task_payload = read_json(task_dir / "task.json")
    task_payload.update({"status": "planning", "branch": branch})
    write_json(task_dir / "task.json", task_payload)
    adapter.production_record_planning(
        owners["guru-approve-task-plan"],
        root,
        task_dir,
        "approved",
    )
    task_payload["status"] = "in_progress"
    write_json(task_dir / "task.json", task_payload)
    checked = adapter.production_record_phase2(
        owners["guru-check-task"],
        root,
        task_dir,
        root / ".trellis/guru-team/skills/packages/guru-check-task",
        "passed",
    )
    adapter.production_commit_for_review(
        owners["guru-create-task-commit"], root, task_dir, checked
    )
    branch_input = {
        "profile": "branch_review",
        "mode": "workflow",
        "task_ref": task_dir.relative_to(root).as_posix(),
        "base_ref": "origin/main",
        "branch_review_commit": "0" * 40,
        "review_intent": "initial_review",
    }
    branch_check = adapter.production_record_review(
        owners["guru-review-branch"],
        root,
        task_dir,
        branch_input,
        "review-passed",
    )
    publication_input = {
        "profile": "publication_review",
        "mode": "workflow",
        "task_ref": task_dir.relative_to(root).as_posix(),
        "branch_review_commit": branch_check["review_commit"],
        "review_intent": "initial_review",
    }
    authoring_path = adapter.production_publication_authoring(
        owners["guru-review-task-publication"],
        root,
        task_dir,
        publication_input,
        "publication-ready",
    )
    authoring = read_json(authoring_path)
    authoring["pr_payload"] = {
        "title": f"完成：#{issue} 验证安装后 closeout",
        "body": valid_pr_body(issue),
    }
    write_json(authoring_path, authoring)
    original_remote_url = git(root, real_git, "remote", "get-url", "origin")
    git(
        root,
        real_git,
        "remote",
        "set-url",
        "origin",
        f"https://github.com/{REMOTE_REPO}.git",
    )
    publication_package = (
        root
        / ".trellis/guru-team/skills/packages/guru-review-task-publication"
    )
    record_publication = publication_package / "scripts/record-task-publication-review.sh"
    check_publication = publication_package / "scripts/check-task-publication-review.sh"
    try:
        run(
            [
                str(record_publication),
                "--root",
                str(root),
                "--task",
                task_dir.relative_to(root).as_posix(),
                "--input",
                authoring_path.relative_to(root).as_posix(),
                "--branch-review-commit",
                publication_input["branch_review_commit"],
            ],
            root,
        )
        checked_publication = json.loads(
            run(
                [
                    str(check_publication),
                    "--root",
                    str(root),
                    "--task",
                    task_dir.relative_to(root).as_posix(),
                    "--expected-exit",
                    "ready",
                ],
                root,
            ).stdout
        )
    finally:
        git(root, real_git, "remote", "set-url", "origin", original_remote_url)
    return task_dir, branch, str(checked_publication["branch_review_commit"])


def install_fake_commands(fake_bin: Path) -> None:
    fake_bin.mkdir(parents=True, exist_ok=True)
    write_executable(
        fake_bin / "git",
        """#!/usr/bin/env python3
import os
import sys

args = sys.argv[1:]
if args == ["config", "--null", "--show-origin", "--get-all", "remote.origin.url"]:
    sys.stdout.buffer.write(b"command line:\\0https://github.com/microsoft/PowerToys.git\\0")
    raise SystemExit(0)
if args == ["config", "--null", "--show-origin", "--get-all", "remote.origin.pushurl"]:
    raise SystemExit(1)
if args[:2] == ["remote", "get-url"]:
    print("https://github.com/microsoft/PowerToys.git")
    raise SystemExit(0)
real_git = os.environ["INSTALLED_CLOSEOUT_REAL_GIT"]
if args[:3] == ["ls-remote", "--heads", "origin"]:
    remote = os.environ["INSTALLED_CLOSEOUT_REMOTE"]
    os.execv(real_git, [real_git, "ls-remote", "--heads", remote, *args[3:]])
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
if len(args) >= 3 and args[:2] == ["issue", "view"]:
    issue_number = int(args[2])
    if issue_number != number:
        raise SystemExit(2)
    print(json.dumps({
        "number": issue_number,
        "state": "CLOSED" if (load() or {}).get("state") == "MERGED" else "OPEN",
        "closedAt": "2026-08-12T10:00:01Z" if (load() or {}).get("state") == "MERGED" else None,
        "url": f"https://github.com/microsoft/powertoys/issues/{issue_number}",
    }))
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
        "url": f"https://github.com/microsoft/PowerToys/pull/{number}",
        "title": value("--title"),
        "body": body,
        "isDraft": True,
        "state": "OPEN",
        "headRefOid": remote_head(),
        "headRepository": {"nameWithOwner": "microsoft/PowerToys"},
        "headRepositoryOwner": {"login": "microsoft"},
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
if len(args) >= 3 and args[:2] == ["pr", "view"]:
    if int(args[2]) != number:
        raise SystemExit(2)
    payload = load()
    if not payload:
        raise SystemExit(2)
    payload["headRefOid"] = remote_head()
    payload.update({
        "baseRefName": "main",
        "headRefName": branch,
        "mergeable": "MERGEABLE",
        "mergeStateStatus": "CLEAN",
        "reviewDecision": "APPROVED",
        "statusCheckRollup": [{"name": "required-ci", "conclusion": "SUCCESS"}],
        "mergedAt": payload.get("mergedAt"),
        "mergeCommit": payload.get("mergeCommit"),
    })
    save(payload)
    print(json.dumps(payload, ensure_ascii=False))
    raise SystemExit(0)
if args[:2] == ["api", "repos/microsoft/powertoys"]:
    print(json.dumps({
        "full_name": "microsoft/PowerToys",
        "allow_merge_commit": True,
        "allow_squash_merge": False,
        "allow_rebase_merge": False,
    }))
    raise SystemExit(0)
if len(args) >= 3 and args[:2] == ["pr", "merge"]:
    payload = load()
    if not payload or int(args[2]) != number:
        raise SystemExit(2)
    expected_head = value("--match-head-commit")
    if expected_head != remote_head() or "--merge" not in args:
        raise SystemExit(2)
    payload.update({
        "state": "MERGED",
        "mergedAt": "2026-08-12T10:00:00Z",
        "mergeCommit": {"oid": expected_head},
    })
    save(payload)
    raise SystemExit(0)
print("unsupported fake gh command: " + " ".join(args), file=sys.stderr)
raise SystemExit(2)
""",
    )


def run_closeout(
    root: Path,
    task_dir: Path,
    branch: str,
    issue: int,
    branch_review_commit: str,
    real_git: str,
    remote: Path,
) -> dict[str, Any]:
    package = (
        root / ".trellis/guru-team/skills/packages/guru-finalize-task"
    )
    wrappers = {
        name: package / "scripts" / f"{name}.sh"
        for name in (
            "preview-finalization",
            "record-finalization-gate",
            "check-finalization-gate",
            "execute-finalization-transition",
            "invoke",
        )
    }
    for name, wrapper in wrappers.items():
        if not wrapper.is_file() or not os.access(wrapper, os.X_OK):
            raise RuntimeError(
                f"installed guru-finalize-task {name} wrapper is missing or not executable: {wrapper}"
            )
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
    runtime_dir = root / ".trellis/.runtime/guru-team/installed-closeout"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    finalization_input = runtime_dir / f"{issue}-publication-ready.json"
    finalization_input.write_text(
        json.dumps(
            {
                "profile": "publication_ready",
                "mode": "workflow",
                "task_ref": task_rel,
                "branch_review_commit": branch_review_commit,
                "pr_title": f"#{issue} 验证安装后 closeout",
                "pr_body": valid_pr_body(issue),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    semantic_review = runtime_dir / f"{issue}-semantic-review.json"
    semantic_review.write_text(
        json.dumps(
            {
                "schema_version": "3.0",
                "skill_id": "guru-finalize-task",
                "review": {
                    "status": "passed",
                    "summary": "The installed Finalizer plan is sufficient for the complete non-extension closeout transaction.",
                },
                "route": {
                    "typed_exit": "ready_for_merge",
                    "consumer": {
                        "kind": "skill",
                        "id": "guru-merge-task-pr",
                    },
                    "output": {"materialization": "executor"},
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    finalization_input_rel = finalization_input.relative_to(root).as_posix()
    semantic_review_rel = semantic_review.relative_to(root).as_posix()
    common_options = [
        "--root", str(root),
        "--json",
        "--input", finalization_input_rel,
        "--repo", REPO,
        "--base-branch", BASE_BRANCH,
        "--remote", "origin",
    ]
    preview_command = [str(wrappers["preview-finalization"]), *common_options]
    record_command = [
        str(wrappers["record-finalization-gate"]),
        *common_options,
        "--review-input",
        semantic_review_rel,
    ]
    check_command = [str(wrappers["check-finalization-gate"]), *common_options]
    execute_command = [
        str(wrappers["execute-finalization-transition"]),
        *common_options,
    ]

    dry_payload = json.loads(run(preview_command, root, env=env).stdout)
    if dry_payload.get("side_effects") is not False:
        raise RuntimeError("installed Finalizer preview reported side effects")
    digest = dry_payload["closeout_plan_digest"]
    recorded_payload = json.loads(run(record_command, root, env=env).stdout)
    if (
        recorded_payload.get("typed_exit") != "ready_for_merge"
        or recorded_payload.get("plan_digest") != digest
    ):
        raise RuntimeError("installed Finalizer recorder did not bind the previewed plan")
    gate_path = Path(recorded_payload["artifact_path"])
    gate_rel = gate_path.relative_to(root).as_posix()
    checked_payload = json.loads(run(check_command, root, env=env).stdout)
    if (
        checked_payload.get("typed_exit") != "ready_for_merge"
        or checked_payload.get("plan_digest") != digest
        or checked_payload.get("transaction_state") != "prepared"
    ):
        raise RuntimeError("installed Finalizer checker did not preserve the prepared plan")

    config_path = root / ".trellis/config.yaml"
    original_config = config_path.read_bytes() if config_path.exists() else None
    hook_sentinel = root / f"installed-after-archive-hook-{issue}.sentinel"
    hook_sentinel.unlink(missing_ok=True)

    def preflight_state() -> dict[str, Any]:
        return {
            "head": git(root, real_git, "rev-parse", "HEAD"),
            "remote": git(root, real_git, "ls-remote", "--heads", "origin", branch),
            "pr_store": store.read_bytes() if store.is_file() else None,
            "git_status": git(root, real_git, "status", "--porcelain"),
            "task": (task_dir / "task.json").read_bytes(),
            "ledger": (task_dir / "issue-scope-ledger.json").read_bytes(),
            "legacy_plan_present": (task_dir / "closeout-plan.json").exists(),
            "readiness": (
                (task_dir / "pr-readiness.json").read_bytes()
                if (task_dir / "pr-readiness.json").is_file()
                else None
            ),
            "finalization_gate": gate_path.read_bytes() if gate_path.is_file() else None,
        }

    def verify_archive_path_symlink_case(component: str, target_scope: str) -> None:
        archive_root = root / ".trellis/tasks/archive"
        month = archive_root / datetime.now().strftime("%Y-%m")
        link_path = archive_root if component == "archive-root" else month
        backup = link_path.with_name(f"{link_path.name}.installed-preflight-backup-{issue}")
        if os.path.lexists(backup):
            raise RuntimeError(f"installed archive symlink backup already exists: {backup}")
        target = (
            root / f".trellis/tasks/installed-archive-symlink-target-{component}"
            if target_scope == "inside"
            else root.parent / f"installed-archive-symlink-target-{component}-{issue}"
        )
        target.mkdir(parents=True)
        sentinel = target / "sentinel.txt"
        sentinel.write_bytes(b"installed-archive-path-sentinel\n")
        archive_root_created = False
        moved_existing = False
        try:
            if component == "archive-month" and not os.path.lexists(archive_root):
                archive_root.mkdir(parents=True)
                archive_root_created = True
            if os.path.lexists(link_path):
                link_path.rename(backup)
                moved_existing = True
            link_path.symlink_to(target, target_is_directory=True)
            before = preflight_state()
            for command in (preview_command, execute_command):
                blocked = subprocess.run(
                    command,
                    cwd=root,
                    env=env,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                if blocked.returncode == 0:
                    raise RuntimeError("installed closeout accepted an archive ancestor symlink")
                try:
                    blocked_payload = json.loads(blocked.stderr)
                except json.JSONDecodeError as exc:
                    raise RuntimeError("installed archive symlink preflight did not return JSON") from exc
                link_rel = link_path.relative_to(root).as_posix()
                dirty_paths = blocked_payload.get("unexpected_dirty_paths")
                blocked_by_publication_owner = isinstance(dirty_paths, list) and any(
                    path == link_rel or path.startswith(f"{link_rel}/")
                    for path in dirty_paths
                    if isinstance(path, str)
                )
                blocked_by_archive_preflight = (
                    blocked_payload.get("stage") == "archive-path-preflight"
                    and blocked_payload.get("component") == component
                )
                if not (blocked_by_publication_owner or blocked_by_archive_preflight):
                    raise RuntimeError("installed archive symlink preflight evidence is incomplete")
                if preflight_state() != before:
                    raise RuntimeError("installed archive symlink preflight changed closeout state")
                if sentinel.read_bytes() != b"installed-archive-path-sentinel\n":
                    raise RuntimeError("installed archive symlink preflight followed or changed its target")
        finally:
            if link_path.is_symlink():
                link_path.unlink()
            if moved_existing:
                backup.rename(link_path)
            elif archive_root_created:
                archive_root.rmdir()
            shutil.rmtree(target, ignore_errors=True)

    for archive_component in ("archive-root", "archive-month"):
        for scope in ("inside", "outside"):
            verify_archive_path_symlink_case(archive_component, scope)

    try:
        existing = original_config.decode("utf-8") if original_config is not None else ""
        if existing and not existing.endswith("\n"):
            existing += "\n"
        config_path.write_text(
            existing
            + "hooks:\n"
            + "  after_archive:\n"
            + f"    - \"touch {hook_sentinel}\"\n",
            encoding="utf-8",
        )
        before = preflight_state()
        for command in (preview_command, execute_command):
            blocked = subprocess.run(
                command,
                cwd=root,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            if blocked.returncode == 0:
                raise RuntimeError(
                    "installed closeout accepted a non-empty official after_archive hook"
                )
            try:
                blocked_payload = json.loads(blocked.stderr)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    "installed hook preflight did not return JSON failure evidence"
                ) from exc
            dirty_paths = blocked_payload.get("unexpected_dirty_paths")
            blocked_by_publication_owner = (
                isinstance(dirty_paths, list)
                and ".trellis/config.yaml" in dirty_paths
            )
            blocked_by_hook_preflight = (
                blocked_payload.get("stage") == "after-archive-hook-preflight"
                and blocked_payload.get("hook_executed") is False
            )
            if not (blocked_by_publication_owner or blocked_by_hook_preflight):
                raise RuntimeError("installed hook preflight failure evidence is incomplete")
            if preflight_state() != before:
                raise RuntimeError("installed hook preflight changed closeout state")
        if hook_sentinel.exists():
            raise RuntimeError("installed hook preflight executed the rejected after_archive hook")
        if not task_dir.is_dir() or json.loads((task_dir / "task.json").read_text(encoding="utf-8"))["status"] != "in_progress":
            raise RuntimeError("installed hook preflight moved or completed the active task")
        if git(root, real_git, "rev-parse", "HEAD") != git(root, real_git, "rev-parse", branch):
            raise RuntimeError("installed hook preflight changed local HEAD")
        if git(root, real_git, "ls-remote", "--heads", "origin", branch):
            raise RuntimeError("installed hook preflight pushed the closeout branch")
        if store.exists():
            raise RuntimeError("installed hook preflight created or queried a persisted PR")
    finally:
        if original_config is None:
            config_path.unlink(missing_ok=True)
        else:
            config_path.write_bytes(original_config)

    payload = json.loads(run(execute_command, root, env=env).stdout)
    if (
        payload.get("typed_exit") != "ready_for_merge"
        or payload.get("closeout_plan_digest") != digest
    ):
        raise RuntimeError("installed Finalizer executor did not complete the reviewed plan")
    checked_after_execute = json.loads(run(check_command, root, env=env).stdout)
    if (
        checked_after_execute.get("typed_exit") != "ready_for_merge"
        or checked_after_execute.get("plan_digest") != digest
        or checked_after_execute.get("transaction_state") != "ready"
    ):
        raise RuntimeError("installed Finalizer checker did not validate the terminal ready marker")

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
    expected_url = f"https://github.com/{REMOTE_REPO}/pull/{issue}"
    if summary["github"]["pr_url"] != expected_url:
        raise RuntimeError("installed closeout summary PR URL is not canonical")
    if summary["index"]["search_terms"]["pr_refs"] != [f"PR #{issue}"]:
        raise RuntimeError("installed closeout summary PR ref is not unique")
    public_invoke = [
        str(wrappers["invoke"]),
        "--input",
        finalization_input_rel,
    ]
    ready_payload = json.loads(
        run([*public_invoke, "--owner-result", gate_rel], root, env=env).stdout
    )
    if (
        ready_payload.get("exit_id") != "ready_for_merge"
        or ready_payload.get("repo_ref") != REPO
        or ready_payload.get("pr_number") != issue
        or ready_payload.get("pr_url") != expected_url
        or ready_payload.get("expected_head_sha") != local_head
        or ready_payload.get("expected_base_branch") != BASE_BRANCH
        or ready_payload.get("expected_head_branch") != branch
        or ready_payload.get("expected_close_issues") != [issue]
    ):
        raise RuntimeError("installed Finalizer public wrapper returned an invalid ready_for_merge DTO")
    if gate_path.exists():
        raise RuntimeError("installed Finalizer public wrapper retained its private gate")
    merge_package = (
        root / ".trellis/guru-team/skills/packages/guru-merge-task-pr"
    )
    merge_wrappers = {
        name: merge_package / "scripts" / f"{name}.sh"
        for name in (
            "preview-task-pr-merge",
            "record-task-pr-merge",
            "check-task-pr-merge",
            "execute-task-pr-merge",
            "invoke",
        )
    }
    for name, wrapper in merge_wrappers.items():
        if not wrapper.is_file() or not os.access(wrapper, os.X_OK):
            raise RuntimeError(
                f"installed guru-merge-task-pr {name} wrapper is missing or not executable: {wrapper}"
            )
    merge_input = runtime_dir / f"{issue}-ready-for-merge.json"
    merge_input.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "profile": "ready_for_merge",
                "mode": "workflow",
                **{key: value for key, value in ready_payload.items() if key != "exit_id"},
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    merge_review = runtime_dir / f"{issue}-merge-semantic-review.json"
    merge_review.write_text(
        json.dumps(
            {
                "semantic_review": {
                    "dimensions": [
                        {
                            "id": identifier,
                            "status": "passed",
                            "summary": "Installed live merge evidence satisfies this dimension.",
                        }
                        for identifier in (
                            "pr_ready",
                            "repository_and_head",
                            "checks_and_reviews",
                            "mergeability",
                            "repository_policy",
                            "close_scope",
                        )
                    ]
                },
                "route": {"typed_exit": "merged", "merge_method": "merge"},
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    merge_input_rel = merge_input.relative_to(root).as_posix()
    merge_review_rel = merge_review.relative_to(root).as_posix()
    merge_common = ["--root", str(root), "--input", merge_input_rel]
    merge_preview = json.loads(
        run([str(merge_wrappers["preview-task-pr-merge"]), *merge_common], root, env=env).stdout
    )
    if merge_preview.get("objective_blockers") != []:
        raise RuntimeError("installed Merge preview did not accept Finalizer expected-head authority")
    merge_record = json.loads(
        run(
            [
                str(merge_wrappers["record-task-pr-merge"]),
                *merge_common,
                "--review-input",
                merge_review_rel,
            ],
            root,
            env=env,
        ).stdout
    )
    merge_gate_rel = merge_record["gate"]
    merge_gate = root / merge_gate_rel
    merge_checked = json.loads(
        run(
            [str(merge_wrappers["check-task-pr-merge"]), *merge_common, "--gate", merge_gate_rel],
            root,
            env=env,
        ).stdout
    )
    if merge_checked.get("typed_exit") != "ready_to_merge":
        raise RuntimeError("installed Merge checker did not bind the expected-head merge")
    merge_executed = json.loads(
        run(
            [str(merge_wrappers["execute-task-pr-merge"]), *merge_common, "--gate", merge_gate_rel],
            root,
            env=env,
        ).stdout
    )
    if merge_executed.get("typed_exit") != "merged":
        raise RuntimeError("installed Merge executor did not complete the expected-head merge")
    merged_payload = json.loads(
        run(
            [str(merge_wrappers["invoke"]), "--input", merge_input_rel, "--gate", merge_gate_rel],
            root,
            env=env,
        ).stdout
    )
    if (
        merged_payload.get("exit_id") != "merged"
        or merged_payload.get("repo_ref") != REPO
        or merged_payload.get("pr_number") != issue
        or merged_payload.get("merge_commit_sha") != local_head
    ):
        raise RuntimeError("installed Merge public wrapper returned an invalid merged DTO")
    if merge_gate.exists():
        raise RuntimeError("installed Merge public wrapper retained its private gate")
    recovered_remote_pr = json.loads(store.read_text(encoding="utf-8"))
    forbidden_terminal = [
        archived / "closeout-plan.json",
        archived / "finalization-transaction.json",
        root / ".trellis/.runtime/guru-team" / task_dir.name / "finalization-transaction.json",
    ]
    if any(path.exists() for path in forbidden_terminal):
        raise RuntimeError("installed Finalizer retained a terminal transaction artifact")
    if recovered_remote_pr.get("number") != issue or recovered_remote_pr.get("url") != expected_url:
        raise RuntimeError("installed fresh archived recovery changed the remote PR identity")
    verifier_artifacts = [
        path
        for state_root in (
            root / ".trellis/tasks",
            root / ".trellis/.runtime/guru-team",
        )
        if state_root.is_dir()
        for path in state_root.rglob("marketplace-verification.json")
    ]
    if verifier_artifacts:
        raise RuntimeError("installed business closeout wrote a marketplace verification artifact")
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
        "public_exit": ready_payload["exit_id"],
        "merge_exit": merged_payload["exit_id"],
        "merge_commit": merged_payload["merge_commit_sha"],
        "verifier_artifacts": 0,
        "terminal_transaction_artifacts": 0,
        "private_owner_checkpoints_consumed": True,
        "fresh_archived_pr_binding": recovered_remote_pr.get("headRefOid") == local_head,
        "after_archive_hook_preflight": True,
        "archive_path_symlink_preflight": True,
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
    owners = {
        skill_id: InstalledPackageClient(root, skill_id)
        for skill_id in (
            "guru-approve-task-plan",
            "guru-check-task",
            "guru-create-task-commit",
            "guru-review-branch",
            "guru-review-task-publication",
        )
    }
    issue = 106 if after_update else 105
    branch = f"fix/{issue}-installed-closeout-{args.case}"
    fake_bin = root.parent / f"fake-closeout-bin-{issue}"
    store = root.parent / f"installed-closeout-pr-{issue}.json"
    install_fake_commands(fake_bin)
    store.unlink(missing_ok=True)
    os.environ.update({
        "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
        "INSTALLED_CLOSEOUT_REAL_GIT": real_git,
        "INSTALLED_CLOSEOUT_REMOTE": str(remote),
        "INSTALLED_CLOSEOUT_BRANCH": branch,
        "INSTALLED_CLOSEOUT_PR_NUMBER": str(issue),
        "INSTALLED_CLOSEOUT_PR_STORE": str(store),
    })
    task_dir, branch, branch_review_commit = write_fixture(
        root, owners, real_git, args.case, issue
    )
    payload = run_closeout(
        root,
        task_dir,
        branch,
        issue,
        branch_review_commit,
        real_git,
        remote,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
