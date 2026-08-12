from __future__ import annotations

import argparse
import hashlib
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
REVIEWED_BASE_PROVENANCE_FIELDS = {
    "source", "selected_base", "remote", "ordered_candidates",
    "decision_head", "local_base_head", "remote_base_head",
    "post_sync_resolution_sha256",
}


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


def _json_argument(value: str | None, label: str) -> dict[str, Any]:
    if not value:
        raise ValueError(f"{label} is required")
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        path = Path(value)
        payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be one JSON object")
    return payload


def _digest(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _reviewed_base_freshness(
    root: Path,
    config: dict[str, Any],
    provenance: dict[str, Any],
    base_assertion: str | None,
) -> dict[str, Any]:
    if set(provenance) != REVIEWED_BASE_PROVENANCE_FIELDS:
        raise ValueError("Reviewed base provenance must contain exactly eight fields.")
    source = provenance.get("source")
    if source not in {"explicit", "config", "config-candidate", "remote-default"}:
        raise ValueError("Reviewed base provenance source is invalid.")
    base = provenance.get("selected_base")
    remote = provenance.get("remote")
    candidates = provenance.get("ordered_candidates")
    if not isinstance(base, str) or not base or not isinstance(remote, str) or not remote:
        raise ValueError("Reviewed base provenance branch or remote is invalid.")
    if (
        not isinstance(candidates, list)
        or not candidates
        or any(not isinstance(item, str) or not item for item in candidates)
        or len(candidates) != len(set(candidates))
        or base not in candidates
    ):
        raise ValueError("Reviewed base provenance candidates are invalid.")
    for field in ("decision_head", "local_base_head", "remote_base_head"):
        if not re.fullmatch(r"[0-9a-f]{40}", str(provenance.get(field) or "")):
            raise ValueError(f"Reviewed base provenance {field} is invalid.")
    reviewed_digest = str(provenance.get("post_sync_resolution_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", reviewed_digest):
        raise ValueError("Reviewed base provenance digest is invalid.")
    if base_assertion and base_assertion != base:
        raise ValueError("Reviewed base provenance does not match --base-branch.")

    resolved_base, _ = _base(root, config)
    if resolved_base != base or candidates != [base]:
        raise ValueError("Reviewed base provenance no longer matches current resolution.")
    decision = {
        "branch": _git(root, "branch", "--show-current"),
        "head": _git(root, "rev-parse", "HEAD"),
        "clean": not bool(_git(root, "status", "--porcelain")),
    }
    resolution = {
        "schema_version": "1.0",
        "skill_id": "guru-" + "sync-base",
        "status": "resolved",
        "source": source,
        "selected_base": base,
        "remote": remote,
        "candidates": candidates,
        "decision_checkout": decision,
    }
    if _digest(resolution) != reviewed_digest:
        raise ValueError("Reviewed base provenance no longer matches current resolution.")
    local_ref = f"refs/heads/{base}"
    remote_ref = f"refs/remotes/{remote}/{base}"
    if (
        not decision["clean"]
        or decision["head"] != provenance["decision_head"]
        or _git(root, "rev-parse", "--verify", local_ref) != provenance["local_base_head"]
        or _git(root, "rev-parse", "--verify", remote_ref) != provenance["remote_base_head"]
    ):
        raise ValueError("Reviewed base provenance is stale against current Git facts.")
    fetched = _run(
        root,
        "git", "fetch", "--no-tags", remote,
        f"refs/heads/{base}:refs/remotes/{remote}/{base}",
    )
    if fetched.returncode:
        raise ValueError(fetched.stderr.strip() or "Reviewed base remote refresh failed.")
    if (
        _git(root, "rev-parse", "HEAD") != provenance["decision_head"]
        or _git(root, "rev-parse", "--verify", local_ref) != provenance["local_base_head"]
        or _git(root, "rev-parse", "--verify", remote_ref) != provenance["remote_base_head"]
        or _git(root, "status", "--porcelain")
    ):
        raise ValueError("Reviewed base changed during remote refresh.")

    decision_checkout = {
        "branch": decision["branch"],
        "head_before": provenance["decision_head"],
        "head_after": provenance["decision_head"],
        "clean_before": True,
        "clean_after": True,
    }
    freshness = {
        "remote": remote,
        "base_branch": base,
        "base_ref": base,
        "remote_ref": f"{remote}/{base}",
        "local_head_before": provenance["local_base_head"],
        "local_head_after": provenance["local_base_head"],
        "remote_head": provenance["remote_base_head"],
        "remote_head_source": "fetched",
        "fetch_attempted": True,
        "fetch_performed": True,
        "fast_forwarded": False,
        "fresh": True,
        "status": "fresh",
        "base_ref_for_worktree": base,
        "resolution": {
            "source": source,
            "selected_base": base,
            "remote": remote,
            "candidates": candidates,
            "resolution_sha256": reviewed_digest,
        },
        "reviewed_resolution_sha256": reviewed_digest,
        "post_sync_resolution": resolution,
        "post_sync_resolution_sha256": reviewed_digest,
        "decision_checkout": decision_checkout,
        "three_way_equal": (
            provenance["decision_head"]
            == provenance["local_base_head"]
            == provenance["remote_base_head"]
        ),
    }
    freshness["facts_sha256"] = _digest(freshness)
    return freshness


def prepare(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(root)
    config = _config(root)
    requirement = " ".join(args.requirement).strip()
    if not requirement:
        raise ValueError("No requirement description provided.")
    provenance = _json_argument(args.reviewed_base_provenance, "reviewed base provenance")
    base, candidates = _base(root, config)
    freshness = _reviewed_base_freshness(root, config, provenance, args.base_branch)
    repo = str(config.get("github_repo") or "").strip() or _origin_repo(root)
    if not repo:
        raise ValueError("Could not resolve GitHub repo.")
    if shutil.which("gh") is None or _run(root, "gh", "auth", "status").returncode:
        raise ValueError("GitHub CLI authentication is unavailable.")
    issue_match = re.search(r"(?:github\.com/([^/]+/[^/]+)/issues/|#)(\d+)", requirement)
    issue = None
    if args.reuse_issue or issue_match:
        number = args.reuse_issue or int(issue_match.group(2))
        target_repo = issue_match.group(1) if issue_match and issue_match.group(1) else repo
        process = _run(root, "gh", "issue", "view", str(number), "--repo", target_repo, "--json", "number,url,title,body")
        if process.returncode:
            raise ValueError(process.stderr.strip() or "GitHub issue lookup failed.")
        issue = json.loads(process.stdout)
        repo = target_repo
    title = str(issue.get("title") if issue else args.issue_title or requirement.splitlines()[0][:80]).strip()
    slug = re.sub(r"[^a-z0-9]+", "-", title.casefold()).strip("-")[:48] or "task"
    issue_token = str(issue["number"]) if issue else "new"
    branch = args.branch or f"feat/{issue_token}-{slug}"
    task_slug = args.task_slug or f"{issue_token}-{slug}"
    workspace_slug = args.workspace_slug or task_slug
    proposed = None if issue else {"repo": repo, "title": title, "body": requirement, "labels": []}
    return {"schema_version": "1.2", "source_repo": repo, "source_issue": ({"number": issue["number"], "url": issue["url"], "title": issue["title"], "created_by_workflow": False} if issue else None), "proposed_issue": proposed, "slug": slug, "naming_quality": {"status": "generated"}, "task_slug": task_slug, "task_title": args.title or (f"#{issue_token} {title}" if issue else f"[proposed-issue] {title}"), "branch_name": branch, "workspace_slug": workspace_slug, "base_branch": base, "base_branch_candidates": candidates, "base_freshness": freshness, "duplicate_search": {"performed": False, "candidates": []}}


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
    prepare_parser = commands.add_parser("prepare")
    prepare_parser.add_argument("--root")
    prepare_parser.add_argument("--json", action="store_true")
    prepare_parser.add_argument("--short-name")
    prepare_parser.add_argument("--reuse-issue", type=int)
    prepare_parser.add_argument("--force-new", action="store_true")
    prepare_parser.add_argument("--issue-title")
    prepare_parser.add_argument("--reviewed-base-provenance")
    prepare_parser.add_argument("--base-branch")
    prepare_parser.add_argument("--branch")
    prepare_parser.add_argument("--task-slug")
    prepare_parser.add_argument("--workspace-slug")
    prepare_parser.add_argument("--title")
    prepare_parser.add_argument("--assignee")
    prepare_parser.add_argument("--priority")
    prepare_parser.add_argument("--description")
    prepare_parser.add_argument("--worktree", action="store_true")
    prepare_parser.add_argument("requirement", nargs="*")
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
            payload = prepare(root, args)
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
