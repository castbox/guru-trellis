from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from argparse import Namespace
from pathlib import Path
from typing import Any
from urllib.parse import quote

from runtime.io import CommandError
from runtime.schema import validate_json


TRAILER_KEYS = (
    "Guru-Task-Identity",
    "Guru-Delivery-Schema",
    "Guru-Delivery-Head",
)
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def repo_root(value: str | None) -> Path:
    root = Path(value or ".").resolve()
    if not (root / ".git").exists():
        raise CommandError("unsafe_path", "root", "Use the exact Git worktree root.")
    return root


def load_query(root: Path, package_root: Path, value: str) -> dict[str, Any]:
    if value == "-":
        raw = sys.stdin.read()
    else:
        path = Path(value)
        candidates = [path] if path.is_absolute() else [root / path, package_root / path]
        resolved = next(
            (item for item in candidates if item.is_file() and not item.is_symlink()),
            None,
        )
        if resolved is None:
            raise CommandError("unsafe_path", "input", "Use one existing regular JSON file.")
        raw = resolved.read_text(encoding="utf-8")
    try:
        query = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("invalid_arguments", "input", "Provide one valid JSON object.") from exc
    validate_json(query, package_root / "schemas/delivery-history-query.schema.json", "input")
    return query


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode:
        raise CommandError(
            "stale_identity",
            "repository",
            proc.stderr.strip() or "Refresh the target-base Git history and retry.",
            3,
        )
    return proc.stdout.strip()


def resolve_base(root: Path, base_ref: str) -> tuple[str, str]:
    candidates = (f"refs/remotes/origin/{base_ref}", f"refs/heads/{base_ref}")
    for candidate in candidates:
        proc = subprocess.run(
            ["git", "rev-parse", "--verify", f"{candidate}^{{commit}}"],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode == 0:
            return candidate, proc.stdout.strip()
    raise CommandError(
        "stale_identity",
        "input.base_ref",
        "Fetch or restore the exact target-base ref before Delivery discovery.",
        3,
    )


def _github_error(proc: subprocess.CompletedProcess[str], operation: str) -> CommandError:
    text = proc.stderr.casefold()
    if "not logged" in text or "authentication" in text or "http 401" in text:
        code, field, remediation = (
            "github_auth_failed",
            "github.auth",
            "Repair GitHub authentication and retry.",
        )
    elif "http 403" in text or "forbidden" in text or "permission" in text:
        code, field, remediation = (
            "github_permission_denied",
            "github.permission",
            "Resolve repository permission and retry.",
        )
    elif "could not resolve to a repository" in text or "http 404" in text:
        code, field, remediation = (
            "github_repo_access_denied",
            "github.repository",
            "Verify repository identity and access.",
        )
    else:
        code, field, remediation = (
            "github_api_unavailable",
            "github.provider",
            "Retry after provider or network recovery.",
        )
    return CommandError(code, field, remediation, response={"operation": operation})


def require_gh(root: Path) -> None:
    if shutil.which("gh") is None:
        raise CommandError("github_cli_missing", "github.cli", "Install GitHub CLI and retry.")
    proc = subprocess.run(
        ["gh", "auth", "status"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode:
        raise _github_error(proc, "auth status")


def gh_value(root: Path, args: list[str], operation: str) -> Any:
    proc = subprocess.run(
        ["gh", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode:
        raise _github_error(proc, operation)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise CommandError(
            "github_response_incomplete",
            "github.response",
            "Repair the adapter/query contract and reread live facts.",
        ) from exc


def parse_delivery_trailers(message: str, task_identity: str) -> dict[str, str] | None:
    normalized = message.rstrip("\n")
    lines = normalized.split("\n")
    task_lines = [line for line in lines if line.startswith("Guru-Task-Identity:")]
    if not task_lines:
        return None
    task_values = [line.split(":", 1)[1].strip() for line in task_lines]
    if task_identity not in task_values:
        return None
    if "\r" in normalized:
        raise CommandError(
            "stale_identity",
            "history.merge_commit.message",
            "Use the exact LF-only Delivery trailer contract.",
            3,
        )
    key_lines = {
        key: [line for line in lines if line.startswith(key + ":")]
        for key in TRAILER_KEYS
    }
    if any(len(values) != 1 for values in key_lines.values()):
        raise CommandError(
            "stale_identity",
            "history.merge_commit.trailers",
            "Require each Delivery trailer exactly once.",
            3,
        )
    if len(lines) < 5 or lines[-4] != "" or lines[-3:] != [
        key_lines[key][0] for key in TRAILER_KEYS
    ]:
        raise CommandError(
            "stale_identity",
            "history.merge_commit.trailers",
            "Require the exact three-field Delivery trailer block at the end of the merge message.",
            3,
        )
    values = {
        key: key_lines[key][0].split(":", 1)[1].strip()
        for key in TRAILER_KEYS
    }
    if values["Guru-Task-Identity"] != task_identity:
        raise CommandError(
            "stale_identity",
            "history.merge_commit.task_identity",
            "Use one exact stable task identity per Delivery merge.",
            3,
        )
    if values["Guru-Delivery-Schema"] != "1":
        raise CommandError(
            "stale_identity",
            "history.merge_commit.schema",
            "Use Delivery trailer schema 1.",
            3,
        )
    reviewed_head = values["Guru-Delivery-Head"]
    if not HEX40.fullmatch(reviewed_head):
        raise CommandError(
            "stale_identity",
            "history.merge_commit.reviewed_head",
            "Use the exact 40-hex reviewed head.",
            3,
        )
    return {"task_identity": task_identity, "reviewed_head": reviewed_head}


def commit_facts(root: Path, sha: str) -> dict[str, Any]:
    row = git(root, "rev-list", "--parents", "-n", "1", sha).split()
    if len(row) != 3 or row[0] != sha:
        raise CommandError(
            "stale_identity",
            "history.merge_commit.parents",
            "Require one exact two-parent Delivery merge commit.",
            3,
        )
    return {
        "sha": sha,
        "message": git(root, "show", "-s", "--format=%B", sha),
        "parents": row[1:],
    }


def associated_pr(root: Path, repo_ref: str, merge_sha: str) -> dict[str, Any]:
    raw = gh_value(
        root,
        [
            "api",
            "-H",
            "Accept: application/vnd.github+json",
            f"repos/{repo_ref}/commits/{merge_sha}/pulls",
        ],
        "commit pull requests",
    )
    if not isinstance(raw, list):
        raise CommandError(
            "github_response_incomplete",
            "github.commit_pulls",
            "Reread the merge commit PR association.",
        )
    matches = [
        item for item in raw
        if isinstance(item, dict) and item.get("merge_commit_sha") == merge_sha
    ]
    if len(matches) != 1:
        raise CommandError(
            "stale_identity",
            "github.commit_pulls",
            "Require exactly one merged PR for each Delivery merge commit.",
            3,
        )
    return matches[0]


def validate_pr(
    raw: dict[str, Any],
    *,
    repo_ref: str,
    base_ref: str,
    merge_sha: str,
    reviewed_head: str,
) -> int:
    try:
        number = int(raw["number"])
        state = str(raw["state"]).upper()
        merged_at = raw["merged_at"]
        merge_commit_sha = str(raw["merge_commit_sha"])
        base_name = str(raw["base"]["ref"])
        base_repo = str(raw["base"]["repo"]["full_name"])
        head_sha = str(raw["head"]["sha"])
        head_repo = str(raw["head"]["repo"]["full_name"])
    except (KeyError, TypeError, ValueError) as exc:
        raise CommandError(
            "github_response_incomplete",
            "github.pull_request",
            "Reread the complete merged PR identity.",
        ) from exc
    if (
        number < 1
        or state != "CLOSED"
        or not merged_at
        or merge_commit_sha != merge_sha
        or base_name != base_ref
        or base_repo.casefold() != repo_ref.casefold()
        or head_repo.casefold() != repo_ref.casefold()
        or head_sha != reviewed_head
    ):
        raise CommandError(
            "stale_identity",
            "github.pull_request",
            "Cross-check repository, base, reviewed head and merge identity from the exact merged PR.",
            3,
        )
    return number


def discover(root: Path, package_root: Path, query: dict[str, Any]) -> dict[str, Any]:
    ref_name, local_base_head = resolve_base(root, query["base_ref"])
    require_gh(root)
    raw_repo = gh_value(root, ["api", f"repos/{query['repo_ref']}"], "repository")
    if (
        not isinstance(raw_repo, dict)
        or str(raw_repo.get("full_name") or "").casefold() != query["repo_ref"].casefold()
    ):
        raise CommandError(
            "stale_identity",
            "github.repository",
            "Use the exact repository identity.",
            3,
        )
    raw_base = gh_value(
        root,
        [
            "api",
            f"repos/{query['repo_ref']}/git/ref/heads/{quote(query['base_ref'], safe='')}",
        ],
        "base ref",
    )
    try:
        remote_base_head = str(raw_base["object"]["sha"])
    except (KeyError, TypeError) as exc:
        raise CommandError(
            "github_response_incomplete",
            "github.base_ref",
            "Reread the exact target-base ref.",
        ) from exc
    if remote_base_head != local_base_head:
        raise CommandError(
            "stale_identity",
            "history.base_ref",
            f"Refresh {ref_name} to the current remote target-base head.",
            3,
        )

    shas = git(root, "rev-list", "--first-parent", "--merges", "--reverse", local_base_head)
    deliveries: list[dict[str, Any]] = []
    seen_heads: set[str] = set()
    seen_prs: set[int] = set()
    for sha in shas.splitlines():
        commit = commit_facts(root, sha)
        trailers = parse_delivery_trailers(commit["message"], query["task_identity"])
        if trailers is None:
            continue
        reviewed_head = trailers["reviewed_head"]
        if commit["parents"][1] != reviewed_head:
            raise CommandError(
                "stale_identity",
                "history.merge_commit.parents",
                "Require parent 2 to equal the reviewed Delivery head.",
                3,
            )
        raw_pr = associated_pr(root, query["repo_ref"], sha)
        pr_number = validate_pr(
            raw_pr,
            repo_ref=query["repo_ref"],
            base_ref=query["base_ref"],
            merge_sha=sha,
            reviewed_head=reviewed_head,
        )
        if reviewed_head in seen_heads or pr_number in seen_prs:
            raise CommandError(
                "stale_identity",
                "history.delivery_identity",
                "Require one unique reviewed head, PR and merge commit per Delivery.",
                3,
            )
        seen_heads.add(reviewed_head)
        seen_prs.add(pr_number)
        deliveries.append({
            "task_identity": query["task_identity"],
            "reviewed_head": reviewed_head,
            "pr_number": pr_number,
            "merge_commit_sha": sha,
            "base_ref": query["base_ref"],
        })

    result = {
        "schema_version": "1.0",
        "status": "discovered",
        "task_identity": query["task_identity"],
        "repo_ref": query["repo_ref"],
        "base_ref": query["base_ref"],
        "deliveries": deliveries,
    }
    validate_json(result, package_root / "schemas/delivery-history-result.schema.json", "stdout")
    return result


def cmd_discover(package_root: Path, args: Namespace) -> dict[str, Any]:
    root = repo_root(args.root)
    query = load_query(root, package_root, args.input)
    return discover(root, package_root, query)
