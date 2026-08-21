from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any
from common import config, resolve_workspace
from runtime.io import CommandError


REVIEWED_BASE_PROVENANCE_FIELDS = {
    "source", "selected_base", "remote", "ordered_candidates",
    "decision_head", "local_base_head", "remote_base_head",
    "post_sync_resolution_sha256",
}


def run(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def git(root: Path, *arguments: str, required: bool = True) -> str:
    process = run(root, "git", *arguments)
    if required and process.returncode:
        raise ValueError(process.stderr.strip() or f"git {' '.join(arguments)} failed")
    return process.stdout.strip()


def origin_repo(root: Path) -> str:
    value = git(root, "remote", "get-url", "origin", required=False)
    match = re.search(r"github\.com[/:]([^/]+)/([^/]+?)(?:\.git)?$", value)
    return f"{match.group(1)}/{match.group(2)}" if match else ""


def live_base(
    root: Path,
    values: dict[str, Any],
    base_assertion: str | None,
    remote: str,
) -> tuple[str, str, list[str]]:
    if base_assertion:
        return "explicit", base_assertion, [base_assertion]

    configured = values.get("base_branch", "")
    if configured is None:
        configured = ""
    if not isinstance(configured, str):
        raise ValueError("Configured base branch must be a scalar string.")
    configured = configured.strip()
    if configured:
        return "config", configured, [configured]

    raw_candidates = values.get("base_branch_candidates", [])
    if not isinstance(raw_candidates, list) or any(not isinstance(item, str) for item in raw_candidates):
        raise ValueError("Configured base candidates must be a list of branch names.")
    candidates: list[str] = []
    for item in raw_candidates:
        item = item.strip()
        if item and item not in candidates:
            candidates.append(item)
    for candidate in candidates:
        if (
            run(root, "git", "show-ref", "--verify", "--quiet", f"refs/heads/{candidate}").returncode == 0
            or run(root, "git", "show-ref", "--verify", "--quiet", f"refs/remotes/{remote}/{candidate}").returncode == 0
        ):
            return "config-candidate", candidate, candidates

    process = run(root, "git", "ls-remote", "--symref", remote, "HEAD")
    matches = [] if process.returncode else [
        match.group(1)
        for line in process.stdout.splitlines()
        if (match := re.fullmatch(r"ref: refs/heads/([^\t]+)\tHEAD", line))
    ]
    if len(matches) != 1:
        raise ValueError("Could not resolve the remote default base branch.")
    selected = matches[0]
    if selected not in candidates:
        candidates.append(selected)
    return "remote-default", selected, candidates


def json_argument(value: str | None) -> dict[str, Any]:
    if not value:
        raise ValueError("reviewed base provenance is required")
    try:
        payload = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError("reviewed base provenance must be one JSON object") from exc
    if not isinstance(payload, dict):
        raise ValueError("reviewed base provenance must be one JSON object")
    return payload


def digest(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def reviewed_base_freshness(
    root: Path,
    values: dict[str, Any],
    provenance: dict[str, Any],
    base_assertion: str | None,
) -> dict[str, Any]:
    if set(provenance) != REVIEWED_BASE_PROVENANCE_FIELDS:
        raise ValueError("Reviewed base provenance must contain exactly eight fields.")
    source = provenance.get("source")
    if source not in {"explicit", "config", "config-candidate", "remote-default"}:
        raise ValueError("Reviewed base provenance source is invalid.")
    selected = provenance.get("selected_base")
    remote = provenance.get("remote")
    candidates = provenance.get("ordered_candidates")
    if not isinstance(selected, str) or not selected or not isinstance(remote, str) or not remote:
        raise ValueError("Reviewed base provenance branch or remote is invalid.")
    if (
        not isinstance(candidates, list)
        or not candidates
        or any(not isinstance(item, str) or not item for item in candidates)
        or len(candidates) != len(set(candidates))
        or selected not in candidates
    ):
        raise ValueError("Reviewed base provenance candidates are invalid.")
    for field in ("decision_head", "local_base_head", "remote_base_head"):
        if not re.fullmatch(r"[0-9a-f]{40}", str(provenance.get(field) or "")):
            raise ValueError(f"Reviewed base provenance {field} is invalid.")
    reviewed_digest = str(provenance.get("post_sync_resolution_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", reviewed_digest):
        raise ValueError("Reviewed base provenance digest is invalid.")
    current_source, resolved, current_candidates = live_base(
        root, values, base_assertion, remote
    )
    if (
        current_source != source
        or resolved != selected
        or candidates != current_candidates
    ):
        raise ValueError("Reviewed base provenance no longer matches current resolution.")
    decision = {
        "branch": git(root, "branch", "--show-current"),
        "head": git(root, "rev-parse", "HEAD"),
        "clean": not bool(git(root, "status", "--porcelain")),
    }
    resolution = {
        "schema_version": "1.0",
        "skill_id": "guru-sync-base",
        "status": "resolved",
        "source": source,
        "selected_base": selected,
        "remote": remote,
        "candidates": candidates,
        "decision_checkout": decision,
    }
    if digest(resolution) != reviewed_digest:
        raise ValueError("Reviewed base provenance no longer matches current resolution.")
    local_ref = f"refs/heads/{selected}"
    remote_ref = f"refs/remotes/{remote}/{selected}"
    if (
        not decision["clean"]
        or decision["head"] != provenance["decision_head"]
        or git(root, "rev-parse", "--verify", local_ref) != provenance["local_base_head"]
        or git(root, "rev-parse", "--verify", remote_ref) != provenance["remote_base_head"]
    ):
        raise ValueError("Reviewed base provenance is stale against current Git facts.")
    fetched = run(
        root, "git", "fetch", "--no-tags", remote,
        f"refs/heads/{selected}:refs/remotes/{remote}/{selected}",
    )
    if fetched.returncode:
        raise ValueError(fetched.stderr.strip() or "Reviewed base remote refresh failed.")
    if (
        git(root, "rev-parse", "HEAD") != provenance["decision_head"]
        or git(root, "rev-parse", "--verify", local_ref) != provenance["local_base_head"]
        or git(root, "rev-parse", "--verify", remote_ref) != provenance["remote_base_head"]
        or git(root, "status", "--porcelain")
    ):
        raise ValueError("Reviewed base changed during remote refresh.")
    freshness = {
        "remote": remote,
        "base_branch": selected,
        "base_ref": selected,
        "remote_ref": f"{remote}/{selected}",
        "local_head_before": provenance["local_base_head"],
        "local_head_after": provenance["local_base_head"],
        "remote_head": provenance["remote_base_head"],
        "remote_head_source": "fetched",
        "fetch_attempted": True,
        "fetch_performed": True,
        "fast_forwarded": False,
        "fresh": True,
        "status": "fresh",
        "base_ref_for_worktree": selected,
        "resolution": {"source": source, "selected_base": selected, "remote": remote, "candidates": candidates, "resolution_sha256": reviewed_digest},
        "reviewed_resolution_sha256": reviewed_digest,
        "post_sync_resolution": resolution,
        "post_sync_resolution_sha256": reviewed_digest,
        "decision_checkout": {"branch": decision["branch"], "head_before": provenance["decision_head"], "head_after": provenance["decision_head"], "clean_before": True, "clean_after": True},
        "three_way_equal": provenance["decision_head"] == provenance["local_base_head"] == provenance["remote_base_head"],
    }
    freshness["facts_sha256"] = digest(freshness)
    return freshness


def prepare(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    root = root.resolve()
    values = config(root)
    requirement = " ".join(args.requirement).strip()
    if not requirement:
        raise ValueError("No requirement description provided.")
    provenance = json_argument(args.reviewed_base_provenance)
    freshness = reviewed_base_freshness(root, values, provenance, args.base_branch)
    selected = freshness["base_branch"]
    candidates = freshness["resolution"]["candidates"]
    repo = str(values.get("github_repo") or "").strip() or origin_repo(root)
    if not repo:
        raise ValueError("Could not resolve GitHub repo.")
    if shutil.which("gh") is None or run(root, "gh", "auth", "status").returncode:
        raise ValueError("GitHub CLI authentication is unavailable.")
    issue_match = re.search(r"(?:github\.com/([^/]+/[^/]+)/issues/|#)(\d+)", requirement)
    issue = None
    if args.reuse_issue or issue_match:
        number = args.reuse_issue or int(issue_match.group(2))
        target_repo = issue_match.group(1) if issue_match and issue_match.group(1) else repo
        process = run(root, "gh", "issue", "view", str(number), "--repo", target_repo, "--json", "number,url,title,body")
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
    resolve_workspace(root, workspace_slug)
    proposed = None if issue else {"repo": repo, "title": title, "body": requirement, "labels": []}
    return {
        "schema_version": "1.2", "source_repo": repo,
        "source_issue": ({"number": issue["number"], "url": issue["url"], "title": issue["title"], "created_by_workflow": False} if issue else None),
        "proposed_issue": proposed, "slug": slug, "naming_quality": {"status": "generated"},
        "task_slug": task_slug, "task_title": args.title or (f"#{issue_token} {title}" if issue else f"[proposed-issue] {title}"),
        "branch_name": branch, "workspace_slug": workspace_slug, "base_branch": selected,
        "base_branch_candidates": candidates, "base_freshness": freshness,
        "duplicate_search": {"performed": False, "candidates": []},
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="prepare-task")
    parser.add_argument("--root")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--short-name")
    parser.add_argument("--reuse-issue", type=int)
    parser.add_argument("--force-new", action="store_true")
    parser.add_argument("--issue-title")
    parser.add_argument("--reviewed-base-provenance")
    parser.add_argument("--base-branch")
    parser.add_argument("--branch")
    parser.add_argument("--task-slug")
    parser.add_argument("--workspace-slug")
    parser.add_argument("--title")
    parser.add_argument("--assignee")
    parser.add_argument("--priority")
    parser.add_argument("--description")
    parser.add_argument("--worktree", action="store_true")
    parser.add_argument("requirement", nargs="*")
    args = parser.parse_args(argv)
    try:
        payload = prepare(Path(args.root or Path.cwd()), args)
    except (CommandError, OSError, ValueError) as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
