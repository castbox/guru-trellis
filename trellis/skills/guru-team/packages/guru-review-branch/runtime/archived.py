"""Read-only archived review identity; no active-task preparation or repair."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

from common import ancestor, digest, git, load, rel, task
from runtime.io import CommandError


def stale(field, message):
    raise CommandError("stale_identity", field, message, 3)


def config_values(repo):
    # Consume the existing simple scalar/one-level configuration grammar.
    values = {"runtime_root": ".trellis/.runtime/guru-team", "github_repo": "", "publish.remote": "origin"}
    path = repo / ".trellis/guru-team/config.yml"
    parent = ""
    if path.is_file():
        for raw in path.read_text().splitlines():
            line = raw.split("#", 1)[0].rstrip()
            if ":" not in line:
                continue
            key, value = line.strip().split(":", 1)
            if not line.startswith(" "):
                parent = key
                target = key
            else:
                target = parent + "." + key
            if target in values:
                values[target] = value.strip().strip("\"'")
    values["runtime_root"] = values["runtime_root"] or ".trellis/.runtime/guru-team"
    values["publish.remote"] = values["publish.remote"] or "origin"
    return values


def gh(repo, repository, *args):
    try:
        result = subprocess.run(["gh", *args], cwd=repo, text=True, capture_output=True)
    except OSError:
        stale("github", "Install authenticated gh and retry the archived review.")
    if result.returncode:
        stale("github", "Recheck gh authentication and access to the bound repository; retry the current review.")
    try:
        return json.loads(result.stdout)
    except (ValueError, TypeError):
        stale("github", "GitHub returned incomplete JSON for the bound repository.")


def facts(package_root, repo, public):
    task_dir = task(repo, public["task_ref"])
    task_ref = rel(repo, task_dir)
    if not re.fullmatch(r"\.trellis/tasks/archive/\d{4}-\d{2}/[^/]+", task_ref):
        stale("task_ref", "Use the exact completed archive locator.")
    metadata = load(repo, package_root, str(task_dir / "task.json"), "task")
    summary = load(repo, package_root, str(task_dir / "finish-summary.json"), "archive")
    branch, base = metadata.get("branch"), metadata.get("base_branch")
    summary_task, summary_git = summary.get("task") or {}, summary.get("git") or {}
    if (not isinstance(summary_task, dict) or not isinstance(summary_git, dict)
        or summary_task.get("archive_dir") != task_ref
        or summary_task.get("slug") != task_dir.name
        or summary_task.get("status") != "completed"
        or summary_git.get("branch") != branch
        or summary_git.get("base_branch") != base):
        stale("archive", "Archive summary and completed task identity must agree.")
    active = summary_task.get("artifact_dir")
    if not isinstance(active, str) or not active.startswith(".trellis/tasks/") or active.startswith(".trellis/tasks/archive/") or (repo / active).exists():
        stale("archive", "Require the original active locator to be absent after archive.")
    head = git(repo, "rev-parse", "HEAD")
    if metadata.get("status") != "completed" or not isinstance(branch, str) or not branch or not isinstance(base, str) or not base:
        stale("task", "Archived review requires completed task branch/base identity.")
    if head != public["branch_review_commit"] or git(repo, "branch", "--show-current") != branch:
        stale("branch_review_commit", "Review the exact current archived branch HEAD.")
    if git(repo, "status", "--porcelain=v1", "--untracked-files=all"):
        stale("worktree", "Archived review requires a completely clean checkout.")
    for name in ("task.json", "finish-summary.json", "prd.md", "design.md", "implement.md"):
        path = task_dir / name
        if not path.is_file() or path.is_symlink() or not git(repo, "ls-tree", head, "--", f"{task_ref}/{name}"):
            stale("archive", "Review requires committed archive planning and finish-summary files.")
    config = config_values(repo)
    runtime = repo / config["runtime_root"]
    slug = metadata.get("id") or metadata.get("name")
    mapping = load(repo, package_root, str(runtime / "tasks" / f"{slug}.json"), "task_mapping")
    workspace = mapping.get("workspace_slug")
    if not workspace or any(mapping.get(k) != v for k, v in {
        "schema_version": "1.0", "task_slug": slug,
        "workspace_path": str(repo), "task_artifact_dir": task_ref,
    }.items()):
        stale("task_mapping", "Require current archived mapping; read-only review never repairs locators.")
    work = load(repo, package_root, str(runtime / "workspaces" / f"{workspace}.json"), "workspace_mapping")
    if any(work.get(k) != v for k, v in {
        "schema_version": "1.0", "workspace_slug": workspace,
        "workspace_path": str(repo), "branch_name": branch,
    }.items()):
        stale("workspace_mapping", "Require the existing exact task workspace mapping.")
    source = work.get("source_checkout")
    if not isinstance(source, str) or not Path(source).is_dir():
        stale("workspace_mapping", "Require the existing source checkout identity.")
    source_root = Path(source).resolve()
    source_runtime = source_root / config_values(source_root)["runtime_root"]
    for group, key, expected in (("tasks", slug, mapping), ("workspaces", workspace, work)):
        other = load(repo, package_root, str(source_runtime / group / f"{key}.json"), "source_mapping")
        if {k: v for k, v in other.items() if k != "updated_at"} != {k: v for k, v in expected.items() if k != "updated_at"}:
            stale("source_mapping", "Both existing mappings must agree; archived review never reconciles them.")
    records = git(repo, "worktree", "list", "--porcelain").split("\n\n")
    if not any(f"worktree {repo}" in row.splitlines() and f"branch refs/heads/{branch}" in row.splitlines() for row in records):
        stale("worktree", "Require the registered task branch/worktree pair.")
    remote = config["publish.remote"]
    url = git(repo, "remote", "get-url", remote)
    match = re.fullmatch(r"(?:https://github.com/|git@github.com:|ssh://git@github.com/)([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?", url)
    if not match or (config["github_repo"] and config["github_repo"].lower() != match[1].lower()):
        stale("repository", "Require the configured publish remote to match the GitHub repository.")
    repository = match[1]
    base = base.removeprefix("origin/")
    base_ref = next((ref for ref in (f"refs/remotes/origin/{base}", f"refs/heads/{base}") if git(repo, "rev-parse", "--verify", ref, check=False)), None)
    if not base_ref:
        stale("base_ref", "Selected base must already exist locally; archived review never fetches.")
    base_head = git(repo, "rev-parse", f"{base_ref}^{{commit}}")
    if not ancestor(repo, base_head, head):
        stale("base_ref", "Selected base must precede the archived review HEAD.")
    try:
        auth = subprocess.run(["gh", "auth", "status"], cwd=repo, capture_output=True)
    except OSError:
        stale("github", "Install authenticated gh before archived review.")
    if auth.returncode:
        stale("github", "Authenticate gh before archived review.")
    policy = gh(repo, repository, "api", f"repos/{repository}")
    if not isinstance(policy, dict) or str(policy.get("full_name", "")).lower() != repository.lower():
        stale("repository", "GitHub repository identity is incomplete.")
    live_base = gh(repo, repository, "api", f"repos/{repository}/git/ref/heads/{quote(base, safe='')}")
    if not isinstance(live_base, dict) or live_base.get("ref") != f"refs/heads/{base}" or not isinstance(live_base.get("object"), dict) or live_base["object"].get("sha") != base_head or live_base["object"].get("type") != "commit":
        stale("reviewed_base_head", "Local selected base and live GitHub base differ; start a fresh review after base synchronization by its owner.")
    prs = gh(repo, repository, "pr", "list", "--repo", repository, "--head", branch, "--base", base, "--state", "open", "--json", "number,url,state,isDraft,headRefName,baseRefName,headRefOid,headRepository,isCrossRepository,title,body")
    if not isinstance(prs, list) or len(prs) != 1:
        stale("pull_request", "Require one exact existing Open Ready PR; never select a replacement.")
    pr = prs[0]
    expected = {"state": "OPEN", "isDraft": False, "headRefName": branch, "baseRefName": base, "headRefOid": head, "isCrossRepository": False}
    if not isinstance(pr, dict) or any(pr.get(k) != v for k, v in expected.items()) or not isinstance(pr.get("title"), str) or not isinstance(pr.get("body"), str):
        stale("pull_request", "Existing PR branch, HEAD, Ready state and exact payload must remain current.")
    head_repo = pr.get("headRepository") or {}
    if not isinstance(head_repo, dict) or str(head_repo.get("nameWithOwner", "")).lower() != repository.lower():
        stale("pull_request", "Require the exact same-repository PR head.")
    if type(pr.get("number")) is not int or pr["number"] < 1 or pr.get("url") != f"https://github.com/{repository}/pull/{pr['number']}":
        stale("pull_request", "Require complete canonical PR identity.")
    if not isinstance(summary.get("github"), dict) or summary["github"].get("pr_url") != pr["url"] or (metadata.get("pr_url") and metadata["pr_url"] != pr["url"]):
        stale("pull_request", "Task PR locator must match the existing PR.")
    snapshot = digest({"title": pr["title"], "body": pr["body"]})
    if snapshot != public["pr_payload_snapshot_sha256"]:
        stale("pr_payload_snapshot_sha256", "PR title/body changed; request a fresh archived review snapshot.")
    remote_head = git(repo, "ls-remote", "--heads", remote, f"refs/heads/{branch}")
    if remote_head.split() != [head, f"refs/heads/{branch}"]:
        stale("branch_review_commit", "Remote branch must still equal the archived review HEAD.")
    return {"base_ref": base_ref, "base_head": base_head, "pr_number": pr["number"], "repo_ref": repository}
