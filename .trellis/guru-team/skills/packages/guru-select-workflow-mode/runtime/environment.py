from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from runtime.io import CommandError


EXTENSION_MANIFEST = Path(".trellis/guru-team/extension.json")


def _run(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".trellis").is_dir():
            return candidate
    process = _run(current, "git", "rev-parse", "--show-toplevel")
    if process.returncode != 0:
        raise CommandError(
            "invalid_arguments",
            "arguments.--root",
            "Pass a path inside a Trellis repository.",
        )
    return Path(process.stdout.strip()).resolve()


def _config(root: Path) -> dict[str, Any]:
    values: dict[str, Any] = {
        "github_repo": "",
        "base_branch": "",
        "base_branch_candidates": ["dev", "develop", "main", "master"],
        "worktree_root": "",
    }
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
        if not value and isinstance(values.get(key), list):
            values[key] = []
        elif value:
            values[key] = value.strip("'\"")
    return values


def _git(root: Path, *arguments: str, required: bool = True) -> str:
    process = _run(root, "git", *arguments)
    if required and process.returncode:
        raise CommandError(
            "environment_unavailable",
            "git",
            process.stderr.strip() or f"git {' '.join(arguments)} failed",
        )
    return process.stdout.strip()


def _origin_repo(root: Path) -> str:
    value = _git(root, "remote", "get-url", "origin", required=False)
    match = re.search(r"github\.com[/:]([^/]+)/([^/]+?)(?:\.git)?$", value)
    return f"{match.group(1)}/{match.group(2)}" if match else ""


def _base(root: Path, config: dict[str, Any]) -> tuple[str, list[str]]:
    configured = str(config.get("base_branch") or "").strip()
    candidates = (
        [configured]
        if configured
        else [str(item) for item in config.get("base_branch_candidates", [])]
    )
    available = [
        name
        for name in candidates
        if _run(root, "git", "show-ref", "--verify", "--quiet", f"refs/heads/{name}").returncode == 0
        or _run(root, "git", "show-ref", "--verify", "--quiet", f"refs/remotes/origin/{name}").returncode == 0
    ]
    if not available:
        raise CommandError(
            "environment_unavailable",
            "base_branch",
            "Configure a base branch that exists locally or under origin.",
        )
    return available[0], candidates


def _extension_payload(root: Path) -> dict[str, Any]:
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
        "tested_trellis_cli": tested.get("trellis_cli")
        if isinstance(tested.get("trellis_cli"), list)
        else [],
        "installed_at": payload.get("installed_at"),
        "source_repo": source.get("repo"),
        "source_ref": source.get("ref"),
        "source_commit": source.get("commit"),
        "source_tree_state": source.get("tree_state"),
        "source_is_mutable_ref": source.get("is_mutable_ref"),
        "selected_platforms": install.get("selected_platforms")
        if isinstance(install.get("selected_platforms"), list)
        else [],
        "all_platforms": install.get("all_platforms"),
    }


def run(argv: list[str]) -> dict[str, Any]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError(
            "invalid_arguments",
            "arguments",
            "Use the exact command help contract.",
        ) from exc
    root = _repo_root(Path(args.root or Path.cwd()))
    config = _config(root)
    repo = str(config.get("github_repo") or "").strip() or _origin_repo(root)
    base, candidates = _base(root, config)
    gh_installed = shutil.which("gh") is not None
    authenticated = gh_installed and _run(root, "gh", "auth", "status").returncode == 0
    accessible = (
        authenticated
        and bool(repo)
        and _run(root, "gh", "repo", "view", repo, "--json", "nameWithOwner").returncode == 0
    )
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
    extension = _extension_payload(root)
    if extension["status"] != "ok":
        warnings.append("Guru Team extension manifest is missing or invalid.")
        next_steps.append("Re-apply the Guru Team preset.")
    payload: dict[str, Any] = {
        "status": "ok",
        "repo_root": str(root),
        "github_repo": repo,
        "trellis_installed": True,
        "guru_team_extension": extension,
        "gh_installed": gh_installed,
        "gh_authenticated": authenticated,
        "gh_repo_accessible": accessible,
        "current_branch": _git(root, "branch", "--show-current"),
        "base_branch": base,
        "base_branch_candidates": candidates,
        "dirty": bool(_git(root, "status", "--porcelain")),
        "worktree_root": str(config.get("worktree_root") or root.parent),
        "existing_worktrees": _git(root, "worktree", "list", "--porcelain").splitlines(),
    }
    if warnings:
        payload.update(warnings=warnings, next_steps=next_steps)
    return payload
