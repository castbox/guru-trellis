from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from argparse import Namespace
from pathlib import Path
from typing import Any
from urllib.parse import quote

from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.task_lifecycle import LifecycleContractError


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
    validate_json(query, package_root / "schemas/delivery-history-query-aggregate.schema.json", "input")
    return query


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "GIT_NO_LAZY_FETCH": "1"},
    )
    if proc.returncode:
        raise CommandError(
            "stale_identity",
            "repository",
            proc.stderr.strip() or "Refresh the target-base Git history and retry.",
            3,
        )
    return proc.stdout.strip()


def first_parent_history(root: Path, commit: str) -> list[list[str]]:
    """Require the real root, not Git's successful stop at a shallow boundary."""
    git(root, "cat-file", "-e", commit + "^{commit}")
    rows = [line.split() for line in git(root, "rev-list", "--first-parent", "--parents", commit).splitlines()]
    shallow_path = Path(git(root, "rev-parse", "--git-path", "shallow"))
    if not shallow_path.is_absolute():
        shallow_path = root / shallow_path
    shallow = set(shallow_path.read_text().splitlines()) if shallow_path.is_file() else set()
    if not rows or rows[0][0] != commit or any(row[0] in shallow for row in rows) or len(rows[-1]) != 1:
        raise CommandError("stale_identity", "history.completeness", "Prepare the complete fixed-cutoff first-parent history and retry this query.", 3)
    return rows


class HistoryContext:
    """Call-local Git preparation; never fetch into the caller's common-dir."""

    def __init__(self, root: Path, repo_ref: str, cutoff: str):
        self.root = root
        self.repo_ref = repo_ref
        self.cutoff = cutoff
        self.temporary = None
        self.fetched: set[str] = set()
        self.required: list[str] = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if self.temporary is not None:
            self.temporary.cleanup()

    def fetch(self, commit: str) -> None:
        if self.temporary is None:
            self.temporary = tempfile.TemporaryDirectory(prefix="guru-delivery-history-")
            self.root = Path(self.temporary.name)
            git(self.root, "init", "--bare")
        if commit in self.fetched:
            return
        self.fetched.add(commit)
        proc = subprocess.run(
            ["git", "fetch", "--no-write-fetch-head", "--no-tags", "--no-recurse-submodules",
             "--no-auto-maintenance", "https://github.com/" + self.repo_ref + ".git", commit],
            cwd=self.root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if proc.returncode:
            error = proc.stderr.casefold()
            if any(token in error for token in ("authentication", "401", "could not read username")):
                reason = "Git authentication failed"
            elif any(token in error for token in ("permission denied", "403", "access denied")):
                reason = "Git permission denied"
            elif any(token in error for token in ("could not resolve", "failed to connect", "timed out", "network")):
                reason = "Git network unavailable"
            elif any(token in error for token in ("not our ref", "couldn't find remote ref", "does not appear to be a git repository")):
                reason = "Required repository or immutable commit unavailable"
            else:
                reason = "Git object transfer failed"
            raise CommandError("stale_identity", "history.preparation", reason + "; restore access to the selected immutable history and retry this query.", 3)

    def prepare(self, commit: str, reader):
        if commit not in self.required:
            self.required.append(commit)
        try:
            return reader(self.root)
        except CommandError:
            # A caller may have the commit but not its parents, trees or blobs.
            # Switch once to a complete isolated context, then verify again.
            for target in self.required:
                self.fetch(target)
            return reader(self.root)

    def history(self, commit: str) -> list[list[str]]:
        return self.prepare(commit, lambda root: first_parent_history(root, commit))

    def candidate(self, head: str, paths: list[str]) -> None:
        def readable(root):
            git(root, "cat-file", "-e", head + "^{commit}")
            for locator in paths:
                row = git(root, "ls-tree", head, "--", locator)
                if row:
                    blob = row.split("\t", 1)[0].split()[2]
                    git(root, "cat-file", "-e", blob)
        self.prepare(head, readable)


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
    schema2 = "Guru-Delivery-Schema: 2" in lines
    trailer_keys = (*TRAILER_KEYS, "Guru-Delivery-Identity", "Guru-Task-Generation") if schema2 else TRAILER_KEYS
    key_lines = {
        key: [line for line in lines if line.startswith(key + ":")]
        for key in trailer_keys
    }
    if any(len(values) != 1 for values in key_lines.values()):
        raise CommandError(
            "stale_identity",
            "history.merge_commit.trailers",
            "Require each Delivery trailer exactly once.",
            3,
        )
    if len(lines) < len(trailer_keys)+2 or lines[-len(trailer_keys)-1] != "" or lines[-len(trailer_keys):] != [
        key_lines[key][0] for key in trailer_keys
    ]:
        raise CommandError(
            "stale_identity",
            "history.merge_commit.trailers",
            "Require the exact three-field Delivery trailer block at the end of the merge message.",
            3,
        )
    values = {
        key: key_lines[key][0].split(":", 1)[1].strip()
        for key in trailer_keys
    }
    if values["Guru-Task-Identity"] != task_identity:
        raise CommandError(
            "stale_identity",
            "history.merge_commit.task_identity",
            "Use one exact stable task identity per Delivery merge.",
            3,
        )
    if values["Guru-Delivery-Schema"] not in {"1", "2"}:
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
    result = {"task_identity": task_identity, "reviewed_head": reviewed_head}
    if schema2:
        import uuid
        try:
            delivery_id = str(uuid.UUID(values["Guru-Delivery-Identity"]))
            generation = int(values["Guru-Task-Generation"])
            if delivery_id != values["Guru-Delivery-Identity"] or generation < 0:
                raise ValueError("invalid identity")
        except ValueError as exc:
            raise CommandError("stale_identity", "history.merge_commit.identity", "Read the exact public Delivery identity trailers.", 3) from exc
        result["delivery_key"] = {"task_id": task_identity, "delivery_id": delivery_id, "lifecycle_generation": generation}
    return result


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
    if not HEX40.fullmatch(remote_base_head):
        raise CommandError("github_response_incomplete", "github.base_ref", "Read one full immutable target-base commit SHA.")

    recorded = {}
    if query["schema_version"] == "2.0":
        from manual_recovery import commit_candidate
        try:
            projection = DeliveryProjection(root, query["task_ref"])
            record = projection.read_record()
            if record["id"] != query["task_identity"]:
                raise CommandError("stale_identity", "history.task_identity", "Read this exact public Task history.", 3)
            for delivery in record["deliveries"]:
                fact = delivery["delivery_result"]
                if (fact is None or fact["profile"] != "pull_request"
                        or fact["repo_ref"].casefold() != query["repo_ref"].casefold()
                        or fact["target_ref"] != query["base_ref"]):
                    continue
                merge = fact["merge_commit"]
                if merge in recorded:
                    raise CommandError("stale_identity", "history.delivery_identity", "Require one public Delivery per immutable merge.", 3)
                if fact["candidate"]["head_ref"] != fact["reviewed_head"]:
                    raise CommandError("stale_identity", "history.candidate", "Read the actual recorded candidate head.", 3)
                recorded[merge] = {"fact": fact, "key": {"task_id": record["id"],
                    "lifecycle_generation": delivery["lifecycle_generation"], "delivery_id": delivery["id"]}}
        except LifecycleContractError as exc:
            raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    with HistoryContext(root, query["repo_ref"], remote_base_head) as context:
        rows = context.history(remote_base_head)
        shas = [row[0] for row in reversed(rows) if len(row) > 2]
        outside = [sha for sha in recorded if sha not in shas]
        outside_history = {sha: {row[0] for row in context.history(sha)} for sha in outside}
        for public_fact in recorded.values():
            fact = public_fact["fact"]
            context.candidate(fact["reviewed_head"], fact["candidate"]["paths"])
            try:
                actual_candidate = commit_candidate(projection, fact, fact["reviewed_head"], git_root=context.root)
            except LifecycleContractError as exc:
                raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
            if actual_candidate != fact["candidate"]:
                raise CommandError("stale_identity", "history.candidate", "Read the immutable recorded candidate bytes and modes.", 3)
        deliveries: list[dict[str, Any]] = []
        seen_heads: set[str] = set()
        seen_prs: set[int] = set()
        for sha in shas + outside:
            message = git(context.root, "show", "-s", "--format=%B", sha)
            trailers = parse_delivery_trailers(message, query["task_identity"])
            public_fact = recorded.get(sha)
            if trailers is None:
                if public_fact is None:
                    continue
                if any(line.startswith("Guru-Task-Identity:") for line in message.splitlines()):
                    raise CommandError("stale_identity", "history.delivery_identity", "Cross-check the recorded Task with the merge's actual Task trailers.", 3)
                trailers = {"task_identity": query["task_identity"],
                            "reviewed_head": public_fact["fact"]["reviewed_head"], "delivery_key": public_fact["key"]}
            elif public_fact is not None:
                if (trailers["reviewed_head"] != public_fact["fact"]["reviewed_head"]
                        or trailers.get("delivery_key", public_fact["key"]) != public_fact["key"]):
                    raise CommandError("stale_identity", "history.delivery_identity", "Cross-check public fact and legal trailer history before deduplication.", 3)
                trailers["delivery_key"] = public_fact["key"]
            reviewed_head = trailers["reviewed_head"]
            context.prepare(reviewed_head, lambda source: git(source, "cat-file", "-e", reviewed_head + "^{commit}"))
            commit = commit_facts(context.root, sha)
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
            if public_fact is not None and pr_number != public_fact["fact"]["pr_number"]:
                raise CommandError("stale_identity", "history.pr_number", "Read the PR belonging to the recorded public result.", 3)
            if reviewed_head in seen_heads or pr_number in seen_prs:
                raise CommandError(
                    "stale_identity",
                    "history.delivery_identity",
                    "Require one unique reviewed head, PR and merge commit per Delivery.",
                    3,
                )
            seen_heads.add(reviewed_head)
            seen_prs.add(pr_number)
            if sha in outside:
                # Only a verified recorded Delivery on the same first-parent line
                # after B1 may be excluded. Its existence never changes this cutoff.
                if sha == remote_base_head or remote_base_head not in outside_history[sha]:
                    raise CommandError("stale_identity", "history.base_ref", "Recorded Delivery is neither covered by the cutoff nor a verified first-parent successor.", 3)
                continue
            deliveries.append({
                "task_identity": query["task_identity"],
                "reviewed_head": reviewed_head,
                "pr_number": pr_number,
                "merge_commit_sha": sha,
                "base_ref": query["base_ref"],
                **({"delivery_key": trailers["delivery_key"]} if "delivery_key" in trailers else {}),
            })

    result = {
        "schema_version": "3.0",
        "status": "discovered",
        "task_identity": query["task_identity"],
        "repo_ref": query["repo_ref"],
        "base_ref": query["base_ref"],
        "cutoff_commit": remote_base_head,
        "deliveries": deliveries,
    }
    validate_json(result, package_root / "schemas/delivery-history-result-3.0.schema.json", "stdout")
    return result


def cmd_discover(package_root: Path, args: Namespace) -> dict[str, Any]:
    root = repo_root(args.root)
    query = load_query(root, package_root, args.input)
    return discover(root, package_root, query)
