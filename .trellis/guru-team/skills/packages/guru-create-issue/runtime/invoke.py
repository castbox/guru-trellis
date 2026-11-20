from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError, fail, read_json, write_json
from runtime.schema import validate_json
from runtime.content_identity import title_body_identity


PACKAGE = Path(__file__).resolve().parents[1]
DIRECT_PROFILE = "issue_creation_direct"
CREATE = "create_issue"
RECOVER = "recover_created_issue_result"


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode()).hexdigest()


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def _label_identity(labels: list[str]) -> list[str]:
    return sorted({label.casefold() for label in labels})


def _reviewed_label_identity(target: dict[str, Any], labels: list[str]) -> str:
    return _digest({"reviewed_target": target["identity_sha256"], "labels": _label_identity(labels)})


def _reviewed_target(draft: dict[str, Any], draft_id: str) -> dict[str, Any]:
    title_sha256 = _sha(draft["title"])
    body_sha256 = _sha(draft["body"])
    source_request_sha256 = _digest({
        "kind": "draft",
        "repo": draft["repo_ref"],
        "issue_number": None,
        "url": None,
        "state": "draft",
        "updated_at": None,
        "body_sha256": body_sha256,
    })
    identity = {
        "kind": "proposed_draft",
        "repo": draft["repo_ref"],
        "draft_id": draft_id,
        "source_request_sha256": source_request_sha256,
        "title_sha256": title_sha256,
        "body_sha256": body_sha256,
    }
    return {
        **identity,
        "identity_sha256": _digest(identity),
        "content_sha256": title_body_identity(draft["title"], draft["body"]),
    }


def _gh(*arguments: str, step: str) -> str:
    recovery = (
        "Keep the original reviewed payload and reviewed_at. "
        "Resume with invoke.sh --input - and action=recover_created_issue_result."
    )
    try:
        completed = subprocess.run(["gh", *arguments], text=True, capture_output=True, check=False)
    except FileNotFoundError as exc:
        raise CommandError("stale_identity", step, f"GitHub CLI is unavailable. Install gh. {recovery}", 3) from exc
    if completed.returncode:
        raise CommandError(
            "stale_identity", step, f"GitHub CLI exited with status {completed.returncode}. {recovery}", 3,
        )
    return completed.stdout.strip()


def _utc(value: str, field_path: str = "createdAt") -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise CommandError("stale_identity", field_path, "Use the original UTC timestamp for the selected Issue attempt.", 3) from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise CommandError("stale_identity", field_path, "Use one UTC timestamp for the reviewed Issue creation.", 3)
    return parsed.astimezone(timezone.utc)


def _creation_floor(reviewed_at: datetime) -> datetime:
    # GitHub's createdAt readback can discard subsecond precision.
    return reviewed_at.replace(microsecond=0) + timedelta(seconds=1)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _wait_for_creation_floor(reviewed_at: datetime) -> bool:
    now = _utc_now()
    if now < reviewed_at or now - reviewed_at > timedelta(seconds=60):
        return False
    floor = _creation_floor(reviewed_at)
    remaining = (floor - now).total_seconds()
    while remaining > 0:
        time.sleep(remaining)
        remaining = (floor - _utc_now()).total_seconds()
    return True


def _created_body(data: dict[str, Any], reviewed_at: datetime) -> str:
    # The stable marker distinguishes this attempt from a later identical draft.
    attempt_id = _digest({
        "reviewed_target": data["reviewed_target"]["identity_sha256"],
        "reviewed_label_identity_sha256": data["reviewed_label_identity_sha256"],
        "reviewed_at": reviewed_at.isoformat(),
    })
    return f'{data["draft"]["body"]}\n\n<!-- guru-create-issue:{attempt_id} -->'


def _same_issue(record: dict[str, Any], draft: dict[str, Any], reviewed_at: datetime, created_body: str) -> bool:
    labels = record.get("labels")
    names = [row.get("name") for row in labels] if isinstance(labels, list) and all(isinstance(row, dict) for row in labels) else []
    return (
        record.get("title") == draft["title"]
        and record.get("body") == created_body
        and isinstance(labels, list)
        and all(isinstance(name, str) and name for name in names)
        and _label_identity(names) == _label_identity(draft["labels"])
        and record.get("state") == "OPEN"
        and type(record.get("number")) is int
        and _utc(record.get("createdAt")) >= _creation_floor(reviewed_at)
    )


def _read_issue(repo: str, number: int) -> dict[str, Any]:
    return json.loads(_gh("issue", "view", str(number), "--repo", repo,
                          "--json", "number,url,title,body,labels,state,createdAt", step="github_issue.readback"))


def _result(repo: str, issue: dict[str, Any]) -> dict[str, Any]:
    return {"exit_id": "created", "repo_ref": repo, "number": issue["number"], "url": issue["url"]}


def _review_comment(data: dict[str, Any], issue: dict[str, Any], *, recover: bool, read_only: bool) -> dict[str, Any]:
    repo = data["draft"]["repo_ref"]
    number = issue["number"]
    attempt = _digest({"created_body": issue["body"]})
    body = data["review_comment_body"] + f"\n\n<!-- guru-create-issue-review:{attempt} -->"
    endpoint = f"repos/{repo}/issues/{number}/comments"
    if recover:
        pages = json.loads(_gh("api", "--paginate", "--slurp", endpoint, step="github_issue.review_comment_list"))
        comments = [row for page in pages for row in page] if isinstance(pages, list) and all(isinstance(page, list) for page in pages) else None
        if comments is None:
            return {"exit_id": "blocked", "reason_code": "review_comment_result_unresolved"}
        marker = f"<!-- guru-create-issue-review:{attempt} -->"
        matches = [row for row in comments if marker in str(row.get("body", ""))]
        if any(row.get("body") != body for row in matches):
            return {"exit_id": "blocked", "reason_code": "review_comment_payload_mismatch"}
        if len(matches) > 1:
            return {"exit_id": "blocked", "reason_code": "review_comment_result_not_unique"}
        if matches:
            comment = matches[0]
        elif read_only:
            return {"exit_id": "blocked", "reason_code": "review_comment_missing"}
        else:
            # A complete successful listing established that the remaining action
            # has not completed. A failed/unknown listing never reaches this POST.
            comment = json.loads(_gh("api", "--method", "POST", endpoint, "--raw-field", "body=" + body,
                                     step="github_issue.review_comment_create"))
    else:
        comment = json.loads(_gh("api", "--method", "POST", endpoint, "--raw-field", "body=" + body,
                                 step="github_issue.review_comment_create"))
    comment_id = comment.get("id")
    if type(comment_id) is not int:
        return {"exit_id": "blocked", "reason_code": "review_comment_result_unresolved"}
    live = json.loads(_gh("api", f"repos/{repo}/issues/comments/{comment_id}",
                          step="github_issue.review_comment_readback"))
    expected_issue = f"https://api.github.com/repos/{repo}/issues/{number}"
    if live.get("id") != comment_id or live.get("body") != body or live.get("issue_url") != expected_issue:
        return {"exit_id": "blocked", "reason_code": "review_comment_identity_mismatch"}
    return _result(repo, issue)


def prepare(data: dict[str, Any]) -> dict[str, Any]:
    validate_json(data, PACKAGE / "schemas/prepare-input-1.0.schema.json", "input")
    _utc(data["reviewed_at"], "input.reviewed_at")
    draft = data["draft"]
    target = _reviewed_target(draft, data["draft_id"])
    result = {
        "profile": DIRECT_PROFILE,
        "action": CREATE,
        "ready_target_kind": "proposed_draft",
        "reviewed_target": target,
        "reviewed_label_identity_sha256": _reviewed_label_identity(target, draft["labels"]),
        "draft": draft,
        "reviewed_at": data["reviewed_at"],
        "review_comment_body": data["review_comment_body"],
        "reviewed_comment_sha256": _sha(data["review_comment_body"]),
    }
    validate_json(result, PACKAGE / "schemas/public-input-direct-1.0.schema.json", "stdout.result")
    return result


def invoke(data: dict[str, Any], *, command_id: str = "invoke-guru-create-issue") -> dict[str, Any]:
    direct = data.get("profile") == DIRECT_PROFILE
    schema = "public-input-direct-1.0.schema.json" if direct else "public-input-2.0.schema.json"
    validate_json(data, PACKAGE / "schemas" / schema, "input")
    refresh_exit = "direct_review_refresh" if direct else "refresh_review"
    action = data["action"]
    if command_id in {"recover-created-issue-result", "check-issue-creation-result"}:
        action = RECOVER
    elif command_id == "create-issue":
        action = CREATE
    draft = data["draft"]
    target = data["reviewed_target"]
    if (target != _reviewed_target(draft, target["draft_id"])
            or data["reviewed_label_identity_sha256"] != _reviewed_label_identity(target, draft["labels"])
            or (direct and data["reviewed_comment_sha256"] != _sha(data["review_comment_body"]))):
        if direct and action == RECOVER:
            return {"exit_id": "blocked", "reason_code": "original_attempt_payload_mismatch"}
        return {"exit_id": refresh_exit, "reason_code": "reviewed_draft_stale"}
    repo = draft["repo_ref"]
    reviewed_at = _utc(data["reviewed_at"], "input.reviewed_at" if direct else "createdAt")
    created_body = _created_body(data, reviewed_at)
    if command_id == "record-issue-creation-plan":
        if action != CREATE:
            raise CommandError("invalid_arguments", "action", "Record only a reviewed Issue creation plan.")
        return {"status": "ready", "repo_ref": repo, "title": draft["title"]}
    if action == CREATE:
        if not _wait_for_creation_floor(reviewed_at):
            return {"exit_id": refresh_exit, "reason_code": "reviewed_time_not_current"}
        command = ["issue", "create", "--repo", repo, "--title", draft["title"], "--body", created_body]
        for label in draft["labels"]:
            command.extend(["--label", label])
        url = _gh(*command, step="github_issue.create")
        try:
            number = int(url.rstrip("/").rsplit("/", 1)[-1])
        except ValueError:
            return {"exit_id": "blocked", "reason_code": "creation_result_unresolved"}
        issue = _read_issue(repo, number)
        if not _same_issue(issue, draft, reviewed_at, created_body) or issue.get("url") != url:
            return {"exit_id": "blocked", "reason_code": "created_issue_identity_mismatch"}
        return _review_comment(data, issue, recover=False, read_only=False)
    # Search is discovery only; recover after exact content validation and
    # uniqueness, never by reissuing the mutation or trusting a title alone.
    candidates = json.loads(_gh("issue", "list", "--repo", repo, "--state", "all", "--limit", "1000",
                                "--search", f'"{draft["title"]}" in:title created:>={reviewed_at.date().isoformat()}',
                                "--json", "number", step="github_issue.recovery_search"))
    if not isinstance(candidates, list) or len(candidates) >= 1000:
        return {"exit_id": "blocked", "reason_code": "created_issue_result_not_unique"}
    matches = [_read_issue(repo, item["number"]) for item in candidates if type(item.get("number")) is int]
    exact = [item for item in matches if _same_issue(item, draft, reviewed_at, created_body)]
    if len(exact) != 1:
        return {"exit_id": "blocked", "reason_code": "created_issue_result_not_unique"}
    return _review_comment(data, exact[0], recover=True, read_only=command_id == "check-issue-creation-result")


def run(package_root: Path, command: dict, argv: list[str]) -> dict[str, Any]:
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument("--input", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments.--input", "Retry this command with --input - and one JSON object on stdin.") from exc
    data = read_json(args.input, "input")
    command_id = command.get("id", "invoke-guru-create-issue")
    if command_id == "prepare-issue-creation":
        return prepare(data)
    output = invoke(data, command_id=command_id)
    if "exit_id" in output:
        validate_json(output, package_root / "schemas/public-output-2.0.schema.json", "stdout")
    return output


def main(argv: list[str]) -> int:
    try:
        write_json(run(PACKAGE, {}, argv))
        return 0
    except CommandError as exc:
        return fail(exc)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
