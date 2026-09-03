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

from verify_throwaway_python_routing import runtime_checkpoint


REPO = "microsoft/powertoys"
REMOTE_REPO = "microsoft/PowerToys"
BASE_BRANCH = "main"


def run(command: list[str], cwd: Path, *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    process_env = dict(os.environ if env is None else env)
    process_env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=cwd, env=process_env, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {' '.join(command)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def single_json_stdout(result: subprocess.CompletedProcess[str], label: str) -> dict[str, Any]:
    if not result.stdout.endswith("\n") or result.stdout.count("\n") != 1:
        raise RuntimeError(f"{label} did not emit exactly one JSON line")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{label} stdout is not one complete JSON object") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"{label} stdout is not a JSON object")
    return payload


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
            "invoke-happy-path-v1.sh",
            "--root", str(root),
            "--candidate-artifact", candidates[0].relative_to(root).as_posix(),
        )
        run(["git", "reset", "--mixed", "HEAD"], root)
        return {
            "exit": executed["exit_id"],
            "commit_sha": executed["branch_review_commit"],
            "task_ref": executed["task_ref"],
            "base_ref": executed["base_ref"],
        }

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


def write_fixture(
    root: Path,
    owners: dict[str, Any],
    real_git: str,
    case_name: str,
    issue: int,
    *,
    repo_ref: str = REPO,
) -> tuple[Path, str, str]:
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
        "url": f"https://github.com/{repo_ref}/issues/{issue}",
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
    publication_input_path = (
        root / ".trellis/.runtime/guru-team/installed-closeout/publication-input.json"
    )
    write_json(publication_input_path, publication_input)
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
    fixture_remote_url = git(root, real_git, "remote", "get-url", "origin")
    publication_package = root / ".trellis/guru-team/skills/packages/guru-review-task-publication"
    publication_facade = publication_package / "scripts/review-task-publication.sh"
    checked_publication = single_json_stdout(
        run(
            [
                str(publication_facade),
                "--root", str(root),
                "--input", publication_input_path.relative_to(root).as_posix(),
                "--semantic-result", authoring_path.relative_to(root).as_posix(),
            ],
            root,
        ),
        "installed Publication Happy Path facade",
    )
    if checked_publication.get("exit_id") != "ready":
        raise RuntimeError("installed Publication facade did not return ready")
    if git(root, real_git, "remote", "get-url", "origin") != fixture_remote_url:
        raise RuntimeError("publication fixture changed the real origin remote")
    return task_dir, branch, str(checked_publication["branch_review_commit"])


def install_fake_commands(fake_bin: Path) -> None:
    fake_bin.mkdir(parents=True, exist_ok=True)
    managed_shebang = f"#!{sys.executable}\n"
    write_executable(
        fake_bin / "git",
        managed_shebang + """
import os
import subprocess
import sys

args = sys.argv[1:]
real_git = os.environ["INSTALLED_CLOSEOUT_REAL_GIT"]
configured = subprocess.run(
    [real_git, "config", "--get", "remote.origin.url"],
    text=True,
    capture_output=True,
    check=False,
).stdout.strip()
canonical_source = "https://github.com/castbox/guru-trellis.git"
visible_origin = (
    canonical_source
    if configured == canonical_source
    else "https://github.com/microsoft/PowerToys.git"
)
if args == ["config", "--null", "--show-origin", "--get-all", "remote.origin.url"]:
    sys.stdout.buffer.write(("command line:\\0" + visible_origin + "\\0").encode())
    raise SystemExit(0)
if args == ["config", "--null", "--show-origin", "--get-all", "remote.origin.pushurl"]:
    raise SystemExit(1)
if args[:2] == ["remote", "get-url"]:
    print(visible_origin)
    raise SystemExit(0)
if args[:3] == ["fetch", "--depth=1", "origin"] and configured == canonical_source:
    source_repo = os.environ["INSTALLED_CLOSEOUT_EXTENSION_SOURCE_REPO"]
    os.execv(real_git, [real_git, "fetch", "--depth=1", source_repo, *args[3:]])
if args[:3] == ["ls-remote", "--heads", "origin"]:
    remote = os.environ["INSTALLED_CLOSEOUT_REMOTE"]
    os.execv(real_git, [real_git, "ls-remote", "--heads", remote, *args[3:]])
os.execv(real_git, [real_git, *args])
""",
    )
    write_executable(
        fake_bin / "gh",
        managed_shebang + """
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
mutation_path = Path(os.environ["INSTALLED_CLOSEOUT_MUTATION_STORE"])

def mutate(operation):
    rows = mutation_path.read_text(encoding="utf-8").splitlines() if mutation_path.exists() else []
    mutation_path.write_text("\\n".join([*rows, operation]) + "\\n", encoding="utf-8")

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

def remote_ref(ref):
    proc = subprocess.run(
        [real_git, "ls-remote", "--heads", remote, ref],
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
        "state": "CLOSED" if (load() or {}).get("state") == "MERGED" and os.environ.get("INSTALLED_CLOSEOUT_CLOSURE_MISMATCH") != "1" else "OPEN",
        "closedAt": "2026-08-12T10:00:01Z" if (load() or {}).get("state") == "MERGED" and os.environ.get("INSTALLED_CLOSEOUT_CLOSURE_MISMATCH") != "1" else None,
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
    fail_marker = os.environ.get("INSTALLED_CLOSEOUT_FAIL_PR_CREATE_ONCE")
    if fail_marker and not Path(fail_marker).exists():
        Path(fail_marker).write_text("failed-once\\n", encoding="utf-8")
        mutate("pr_create_failed")
        raise SystemExit(73)
    mutate("pr_create")
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
    mutate("pr_ready")
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
if len(args) >= 2 and args[0] == "api" and args[1].startswith("repos/microsoft/powertoys/git/ref/heads/"):
    ref = args[1].split("/git/ref/heads/", 1)[1]
    payload = load() or {}
    current = (payload.get("mergeCommit") or {}).get("oid") if payload.get("state") == "MERGED" else remote_ref(ref)
    print(json.dumps({"ref": f"refs/heads/{ref}", "object": {"sha": current}}))
    raise SystemExit(0)
if len(args) >= 2 and args[0] == "api" and args[1].startswith("repos/microsoft/powertoys/git/commits/"):
    payload = load() or {}
    commit = payload.get("commit")
    if not commit or args[1].rsplit("/", 1)[1] != commit.get("sha"):
        raise SystemExit(2)
    print(json.dumps(commit, ensure_ascii=False))
    raise SystemExit(0)
if len(args) >= 3 and args[:2] == ["pr", "merge"]:
    mutate("pr_merge")
    payload = load()
    if not payload or int(args[2]) != number:
        raise SystemExit(2)
    expected_head = value("--match-head-commit")
    subject = value("--subject")
    body = Path(value("--body-file")).read_text(encoding="utf-8")
    if expected_head != remote_head() or "--merge" not in args or not subject.startswith("chore(merge): #") or not body:
        raise SystemExit(2)
    merge_sha = "2" * 40
    payload.update({
        "state": "MERGED",
        "mergedAt": "2026-08-12T10:00:00Z",
        "mergeCommit": {"oid": merge_sha},
        "commit": {
            "sha": merge_sha,
            "message": subject + "\\n\\n" + body,
            "parents": [{"sha": remote_ref("main")}, {"sha": expected_head}],
        },
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
    *,
    terminal_recovery_only: bool = False,
    closure_mismatch: bool = False,
    provider_failure_once: bool = False,
) -> dict[str, Any]:
    package = (
        root / ".trellis/guru-team/skills/packages/guru-finalize-task"
    )
    wrappers = {
        name: package / "scripts" / f"{name}.sh"
        for name in (
            "preview-finalization",
            "finalize-task-happy-path",
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
    mutations = root.parent / f"installed-closeout-mutations-{issue}.txt"
    provider_failure_marker = (
        root.parent / f"installed-closeout-provider-failure-{issue}.sentinel"
    )
    store.unlink(missing_ok=True)
    mutations.unlink(missing_ok=True)
    provider_failure_marker.unlink(missing_ok=True)
    env = dict(os.environ)
    env.update({
        "PATH": f"{fake_bin}{os.pathsep}{env.get('PATH', '')}",
        "INSTALLED_CLOSEOUT_REAL_GIT": real_git,
        "INSTALLED_CLOSEOUT_EXTENSION_SOURCE_REPO": str(
            Path(__file__).resolve().parents[5]
        ),
        "INSTALLED_CLOSEOUT_REMOTE": str(remote),
        "INSTALLED_CLOSEOUT_BRANCH": branch,
        "INSTALLED_CLOSEOUT_PR_NUMBER": str(issue),
        "INSTALLED_CLOSEOUT_PR_STORE": str(store),
        "INSTALLED_CLOSEOUT_MUTATION_STORE": str(mutations),
        "INSTALLED_CLOSEOUT_CLOSURE_MISMATCH": "1" if closure_mismatch else "0",
        "INSTALLED_CLOSEOUT_FAIL_PR_CREATE_ONCE": (
            str(provider_failure_marker) if provider_failure_once else ""
        ),
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

    def write_semantic_review() -> None:
        semantic_review.write_text(
            json.dumps(
                {
                    "schema_version": "3.0",
                    "skill_id": "guru-finalize-task",
                    "review": {
                        "status": "passed",
                        "summary": "The installed Finalizer plan is sufficient for the "
                        "complete non-extension closeout transaction.",
                    },
                    "route": {
                        "typed_exit": "ready_for_merge",
                        "consumer": {"kind": "skill", "id": "guru-merge-task-pr"},
                        "output": {"materialization": "executor"},
                    },
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    write_semantic_review()
    semantic_review_rel = semantic_review.relative_to(root).as_posix()
    common_options = [
        "--root", str(root),
        "--input", finalization_input.relative_to(root).as_posix(),
        "--repo", REPO,
        "--base-branch", BASE_BRANCH,
        "--remote", "origin",
    ]
    preview_command = [
        str(wrappers["preview-finalization"]),
        *common_options,
        "--json",
    ]

    resolved_gh = subprocess.run(
        ["/bin/sh", "-c", "command -v gh"],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if resolved_gh.returncode != 0 or Path(resolved_gh.stdout.strip()) != fake_bin / "gh":
        raise RuntimeError(
            "installed Finalizer fixture did not resolve the expected fake gh: "
            f"{resolved_gh.stdout.strip()} {resolved_gh.stderr.strip()}"
        )
    fake_auth = subprocess.run(
        [resolved_gh.stdout.strip(), "auth", "status"],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if fake_auth.returncode != 0:
        raise RuntimeError(
            "installed Finalizer fixture fake gh auth self-check failed: "
            f"{fake_auth.stdout.strip()} {fake_auth.stderr.strip()}"
        )

    dry_payload = json.loads(run(preview_command, root, env=env).stdout)
    initial_finalizer_state = dry_payload.get("transaction_state")
    if (
        dry_payload.get("side_effects") is not False
        or initial_finalizer_state not in {"prepared", "reprepare_required"}
    ):
        raise RuntimeError("installed Finalizer preview was not ready for the Happy Path facade")
    digest = dry_payload["closeout_plan_digest"]
    confirmation_identity = dry_payload.get("confirmation_identity")
    if not isinstance(confirmation_identity, str):
        raise RuntimeError("installed Finalizer preview omitted its confirmation identity")
    facade_command = [
        str(wrappers["finalize-task-happy-path"]),
        *common_options,
        "--review-input", semantic_review_rel,
        "--confirmed-preview-sha256", confirmation_identity,
    ]

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
            for command in (preview_command, facade_command):
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

    if not terminal_recovery_only:
        for archive_component in ("archive-root", "archive-month"):
            for scope in ("inside", "outside"):
                verify_archive_path_symlink_case(archive_component, scope)

    try:
        if terminal_recovery_only:
            raise StopIteration
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
        for command in (preview_command, facade_command):
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
    except StopIteration:
        pass
    finally:
        if original_config is None:
            config_path.unlink(missing_ok=True)
        else:
            config_path.write_bytes(original_config)

    provider_failure_recovered = False
    if provider_failure_once:
        failed_provider = subprocess.run(
            facade_command,
            cwd=root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        if failed_provider.returncode == 0 or not provider_failure_marker.is_file():
            raise RuntimeError("installed provider failure injection did not fail once")
        if not task_dir.is_dir():
            raise RuntimeError("installed provider failure moved the active task")
        provider_failure_recovered = True
        env["INSTALLED_CLOSEOUT_FAIL_PR_CREATE_ONCE"] = ""

    payload = single_json_stdout(
        run(facade_command, root, env=env),
        "installed Finalizer Happy Path facade",
    )
    if payload.get("exit_id") != "ready_for_merge":
        raise RuntimeError("installed Finalizer facade did not complete the reviewed plan")
    mutations_after_finalizer = mutations.read_bytes()
    recovered_finalizer = single_json_stdout(
        run(facade_command, root, env=env),
        "installed Finalizer terminal recovery",
    )
    if recovered_finalizer != payload:
        raise RuntimeError("installed Finalizer terminal recovery changed its ready_for_merge DTO")
    if mutations.read_bytes() != mutations_after_finalizer:
        raise RuntimeError("installed Finalizer terminal recovery repeated a GitHub mutation")

    archived = (
        root
        / ".trellis/tasks/archive"
        / datetime.now().strftime("%Y-%m")
        / task_dir.name
    )
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
    ready_payload = payload
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
        raise RuntimeError("installed Finalizer facade returned an invalid ready_for_merge DTO")
    merge_package = (
        root / ".trellis/guru-team/skills/packages/guru-merge-task-pr"
    )
    merge_wrappers = {
        "complete-task-pr-merge": merge_package / "scripts/complete-task-pr-merge.sh",
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
                "schema_version": "2.0",
                "profile": "ready_for_merge",
                "mode": "workflow",
                **{key: value for key, value in ready_payload.items() if key != "exit_id"},
                "reviewed_merge_message": {
                    "primary_issue": issue,
                    "summary": "验证安装态 Merge Skill 中文提交消息承接",
                    "subject": f"chore(merge): #{issue} 合并 #{issue} 验证安装态 Merge Skill 中文提交消息承接",
                    "body": (
                        "合并：\n"
                        f"合入 `{branch}` 到 `main`，保留 PR 内部提交历史。\n\n"
                        "范围：\n"
                        f"本次 PR 完成 #{issue}：验证安装态 Merge Skill 中文提交消息承接。\n\n"
                        "审计：\n"
                        "Trellis task archive、review gate、finish-summary 和 readiness 提交保留在 PR 分支历史中，用于审计任务过程。\n\n"
                        f"PR: #{issue}\n"
                        f"Refs #{issue}"
                    ),
                },
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
    merge_facade_command = [
        str(merge_wrappers["complete-task-pr-merge"]),
        "--root", str(root),
        "--input", merge_input_rel,
        "--review-input", merge_review_rel,
    ]
    expected_merge_exit = "closure_mismatch" if closure_mismatch else "merged"
    merged_payload = single_json_stdout(
        run(
            merge_facade_command,
            root,
            env=env,
        ),
        "installed Merge Happy Path facade",
    )
    if merged_payload.get("exit_id") != expected_merge_exit:
        raise RuntimeError("installed Merge facade did not complete the expected-head merge")
    mutations_after_merge = mutations.read_bytes()
    recovered_merge = single_json_stdout(
        run(
            merge_facade_command,
            root,
            env=env,
        ),
        "installed Merge terminal recovery",
    )
    if recovered_merge != merged_payload:
        raise RuntimeError("installed Merge terminal recovery changed its terminal DTO")
    if mutations.read_bytes() != mutations_after_merge:
        raise RuntimeError("installed Merge terminal recovery repeated the merge mutation")
    if (
        merged_payload.get("exit_id") != expected_merge_exit
        or merged_payload.get("repo_ref") != REPO
        or merged_payload.get("pr_number") != issue
        or merged_payload.get("merge_commit_sha") != "2" * 40
    ):
        raise RuntimeError("installed Merge facade returned an invalid merged DTO")
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
        "after_archive_hook_preflight": not terminal_recovery_only,
        "archive_path_symlink_preflight": not terminal_recovery_only,
        "provider_failure_recovered": provider_failure_recovered,
        "finalizer_initial_state": initial_finalizer_state,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--case", choices=["initial", "after-update"], required=True)
    parser.add_argument("--terminal-recovery-only", action="store_true")
    parser.add_argument("--closure-mismatch", action="store_true")
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
        terminal_recovery_only=args.terminal_recovery_only,
        closure_mismatch=args.closure_mismatch,
    )
    payload["runtime_checkpoint"] = runtime_checkpoint(
        root,
        root / ".trellis/guru-team/runtime",
        f"closeout-{args.case}",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
