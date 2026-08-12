from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


EXTENSION_MANIFEST = Path(".trellis/guru-team/extension.json")
HUMAN_ARTIFACTS = (
    ("PRD", "prd.md", "需求、范围、验收标准"),
    ("Design", "design.md", "技术设计与取舍"),
    ("Implement Plan", "implement.md", "执行计划与验证计划"),
)
def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".trellis").is_dir():
            return candidate
    process = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=current,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != 0:
        raise ValueError("Could not resolve a Trellis repository root.")
    return Path(process.stdout.strip()).resolve()


def extension_payload(root: Path) -> dict[str, Any]:
    path = root / EXTENSION_MANIFEST
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"status": "missing", "path": EXTENSION_MANIFEST.as_posix()}
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {
            "status": "invalid",
            "path": EXTENSION_MANIFEST.as_posix(),
            "error": f"invalid: {exc}",
        }
    if not isinstance(payload, dict):
        return {
            "status": "invalid",
            "path": EXTENSION_MANIFEST.as_posix(),
            "error": "invalid: JSON root is not an object",
        }

    extension = payload.get("extension") if isinstance(payload.get("extension"), dict) else {}
    source = payload.get("source") if isinstance(payload.get("source"), dict) else {}
    install = payload.get("install") if isinstance(payload.get("install"), dict) else {}
    tested = extension.get("tested") if isinstance(extension.get("tested"), dict) else {}
    return {
        "status": "ok",
        "path": EXTENSION_MANIFEST.as_posix(),
        "schema_version": payload.get("schema_version"),
        "extension_id": extension.get("extension_id"),
        "version": extension.get("version"),
        "workflow_template_id": extension.get("workflow_template_id"),
        "target_trellis_cli": extension.get("target_trellis_cli"),
        "tested_trellis_cli": tested.get("trellis_cli") if isinstance(tested.get("trellis_cli"), list) else [],
        "installed_at": payload.get("installed_at"),
        "source_repo": source.get("repo"),
        "source_ref": source.get("ref"),
        "source_commit": source.get("commit"),
        "source_tree_state": source.get("tree_state"),
        "source_is_mutable_ref": source.get("is_mutable_ref"),
        "selected_platforms": install.get("selected_platforms") if isinstance(install.get("selected_platforms"), list) else [],
        "all_platforms": install.get("all_platforms"),
    }


def version(root: Path) -> dict[str, Any]:
    resolved = repo_root(root)
    return {
        "status": "ok",
        "repo_root": str(resolved),
        "guru_team_extension": extension_payload(resolved),
    }


def _run(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(arguments, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def _config(root: Path) -> dict[str, Any]:
    values: dict[str, Any] = {"github_repo": "", "base_branch": "", "base_branch_candidates": ["dev", "develop", "main", "master"], "worktree_root": "", "source_issue_required": False, "duplicate_search_required": True, "duplicate_candidate_limit": 5}
    path = root / ".trellis/guru-team/config.yml"
    if not path.is_file():
        return values
    active_list: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        text = line.strip()
        if text.startswith("- ") and active_list:
            values.setdefault(active_list, []).append(text[2:].strip().strip("'\""))
            continue
        if ":" not in text or len(line) != len(line.lstrip()):
            continue
        key, value = (part.strip() for part in text.split(":", 1))
        active_list = key if not value else None
        if not value:
            if key in values and isinstance(values[key], list):
                values[key] = []
        elif value.casefold() in {"true", "false"}:
            values[key] = value.casefold() == "true"
        elif value.isdigit():
            values[key] = int(value)
        else:
            values[key] = value.strip("'\"")
    return values


def _git(root: Path, *arguments: str, required: bool = True) -> str:
    process = _run(root, "git", *arguments)
    if required and process.returncode:
        raise ValueError(process.stderr.strip() or f"git {' '.join(arguments)} failed")
    return process.stdout.strip()


def _origin_repo(root: Path) -> str:
    value = _git(root, "remote", "get-url", "origin", required=False)
    match = re.search(r"github\.com[/:]([^/]+)/([^/]+?)(?:\.git)?$", value)
    return f"{match.group(1)}/{match.group(2)}" if match else ""


def _base(root: Path, config: dict[str, Any]) -> tuple[str, list[str]]:
    configured = str(config.get("base_branch") or "").strip()
    candidates = [configured] if configured else [str(item) for item in config.get("base_branch_candidates", [])]
    available = [name for name in candidates if _run(root, "git", "show-ref", "--verify", "--quiet", f"refs/heads/{name}").returncode == 0 or _run(root, "git", "show-ref", "--verify", "--quiet", f"refs/remotes/origin/{name}").returncode == 0]
    if not available:
        raise ValueError("Could not resolve a configured base branch.")
    return available[0], candidates


def check_env(root: Path) -> dict[str, Any]:
    root = repo_root(root)
    config = _config(root)
    repo = str(config.get("github_repo") or "").strip() or _origin_repo(root)
    base, candidates = _base(root, config)
    gh_installed = shutil.which("gh") is not None
    authenticated = gh_installed and _run(root, "gh", "auth", "status").returncode == 0
    accessible = authenticated and bool(repo) and _run(root, "gh", "repo", "view", repo, "--json", "nameWithOwner").returncode == 0
    warnings: list[str] = []
    next_steps: list[str] = []
    if not repo:
        warnings.append("github_repo is not configured and could not be inferred from the Git origin remote.")
        next_steps.append("Configure github_repo or a GitHub origin remote.")
    if not gh_installed:
        warnings.append("GitHub CLI is not installed.")
        next_steps.append("Install GitHub CLI before GitHub-backed workflow operations.")
    elif not authenticated:
        warnings.append("GitHub CLI is not authenticated.")
        next_steps.append("Run gh auth login and retry.")
    elif repo and not accessible:
        warnings.append("Authenticated GitHub CLI cannot access the target repository.")
        next_steps.append("Verify github_repo and repository access.")
    extension = extension_payload(root)
    if extension["status"] != "ok":
        warnings.append("Guru Team extension manifest is missing or invalid.")
        next_steps.append("Re-apply the Guru Team preset.")
    payload: dict[str, Any] = {"status": "ok", "repo_root": str(root), "github_repo": repo, "trellis_installed": True, "guru_team_extension": extension, "gh_installed": gh_installed, "gh_authenticated": authenticated, "gh_repo_accessible": accessible, "current_branch": _git(root, "branch", "--show-current"), "base_branch": base, "base_branch_candidates": candidates, "dirty": bool(_git(root, "status", "--porcelain")), "worktree_root": str(config.get("worktree_root") or root.parent), "existing_worktrees": _git(root, "worktree", "list", "--porcelain").splitlines()}
    if warnings:
        payload["warnings"] = warnings
        payload["next_steps"] = next_steps
    return payload


def _task_dir(root: Path, value: str | None) -> Path:
    if value:
        candidates = (Path(value), root / value, root / ".trellis/tasks" / value)
    else:
        process = _run(root, "python3", "./.trellis/scripts/task.py", "current")
        candidates = (root / process.stdout.strip(),) if process.returncode == 0 and process.stdout.strip() else ()
    for candidate in candidates:
        resolved = candidate if candidate.is_absolute() else root / candidate
        if resolved.is_dir() and not resolved.is_symlink():
            return resolved.resolve()
    raise ValueError("Could not resolve current Trellis task. Pass --task <task-dir>.")


def human_artifacts(root: Path, task: str | None) -> dict[str, Any]:
    root = repo_root(root)
    task_dir = _task_dir(root, task)
    relative = task_dir.relative_to(root).as_posix()
    artifacts = []
    for label, filename, purpose in HUMAN_ARTIFACTS:
        path = task_dir / filename
        exists = path.is_file()
        artifacts.append({"label": label, "filename": filename, "purpose": purpose, "exists": exists, "status": "已生成" if exists else "未生成", "path": path.relative_to(root).as_posix(), "absolute_path": str(path), "link": str(path) if exists else ""})
    return {"status": "ok", "task_dir": str(task_dir), "task_dir_relative": relative, "archived": relative.startswith(".trellis/tasks/archive/"), "markdown_artifacts": artifacts}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="guru-team-utility")
    commands = parser.add_subparsers(dest="command", required=True)
    version_parser = commands.add_parser("version")
    version_parser.add_argument("--root")
    version_parser.add_argument("--json", action="store_true")
    environment = commands.add_parser("check-env")
    environment.add_argument("--root")
    environment.add_argument("--json", action="store_true")
    artifacts = commands.add_parser("resolve-human-artifacts")
    artifacts.add_argument("--root")
    artifacts.add_argument("--json", action="store_true")
    artifacts.add_argument("--task")
    args = parser.parse_args(argv)
    try:
        root = Path(args.root or Path.cwd())
        if args.command == "version":
            payload = version(root)
        elif args.command == "check-env":
            payload = check_env(root)
        elif args.command == "resolve-human-artifacts":
            payload = human_artifacts(root, args.task)
        else:
            payload = human_artifacts(root, args.task)
    except (OSError, ValueError) as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
