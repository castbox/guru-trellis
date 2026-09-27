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


PACKAGE = Path(__file__).resolve().parents[1]


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode()).hexdigest()


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def _label_identity(labels: list[str]) -> list[str]:
    return sorted({label.casefold() for label in labels})


def _reviewed_label_identity(target: dict[str, Any], labels: list[str]) -> str:
    return _digest({"reviewed_target": target["identity_sha256"], "labels": _label_identity(labels)})


def _reviewed_target(draft: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
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
        "draft_id": target["draft_id"],
        "source_request_sha256": source_request_sha256,
        "title_sha256": title_sha256,
        "body_sha256": body_sha256,
    }
    return {
        **identity,
        "identity_sha256": _digest(identity),
        "content_sha256": _digest({"title_sha256": title_sha256, "body_sha256": body_sha256}),
    }


def _gh(*arguments: str) -> str:
    completed = subprocess.run(["gh", *arguments], text=True, capture_output=True, check=False)
    if completed.returncode:
        raise CommandError("stale_identity", "github_issue", "Reread the GitHub Issue creation authority and retry only after resolving the provider error.", 3)
    return completed.stdout.strip()


def _utc(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise CommandError("stale_identity", "createdAt", "Reread the reviewed time and live Issue creation facts.", 3) from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise CommandError("stale_identity", "createdAt", "Use one UTC timestamp for the reviewed Issue creation.", 3)
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
                          "--json", "number,url,title,body,labels,state,createdAt"))


def _result(repo: str, issue: dict[str, Any]) -> dict[str, Any]:
    return {"exit_id": "created", "repo_ref": repo, "number": issue["number"], "url": issue["url"]}


def invoke(data: dict[str, Any], *, command_id: str = "invoke-guru-create-issue") -> dict[str, Any]:
    validate_json(data, PACKAGE / "schemas/public-input.schema.json", "input")
    draft = data["draft"]
    if (data["reviewed_target"] != _reviewed_target(draft, data["reviewed_target"])
            or data["reviewed_label_identity_sha256"] != _reviewed_label_identity(
                data["reviewed_target"], draft["labels"])):
        return {"exit_id": "refresh_review", "reason_code": "reviewed_draft_stale"}
    repo = draft["repo_ref"]
    reviewed_at = _utc(data["reviewed_at"])
    created_body = _created_body(data, reviewed_at)
    action = data["action"]
    if command_id == "record-issue-creation-plan":
        if action != "create_issue":
            raise CommandError("invalid_arguments", "action", "Record only a reviewed Issue creation plan.")
        return {"status": "ready", "repo_ref": repo, "title": draft["title"]}
    if command_id in {"recover-created-issue-result", "check-issue-creation-result"}:
        action = "recover_created_issue_result"
    elif command_id == "create-issue":
        action = "create_issue"
    if action == "create_issue":
        if not _wait_for_creation_floor(reviewed_at):
            return {"exit_id": "refresh_review", "reason_code": "reviewed_time_not_current"}
        command = ["issue", "create", "--repo", repo, "--title", draft["title"], "--body", created_body]
        for label in draft["labels"]:
            command.extend(["--label", label])
        url = _gh(*command)
        try:
            number = int(url.rstrip("/").rsplit("/", 1)[-1])
        except ValueError:
            return {"exit_id": "blocked", "reason_code": "creation_result_unresolved"}
        issue = _read_issue(repo, number)
        if not _same_issue(issue, draft, reviewed_at, created_body) or issue.get("url") != url:
            return {"exit_id": "blocked", "reason_code": "created_issue_identity_mismatch"}
        return _result(repo, issue)
    # Search is discovery only; recover after exact content validation and
    # uniqueness, never by reissuing the mutation or trusting a title alone.
    candidates = json.loads(_gh("issue", "list", "--repo", repo, "--state", "all", "--limit", "1000",
                                "--search", f'"{draft["title"]}" in:title created:>={reviewed_at.date().isoformat()}',
                                "--json", "number"))
    if not isinstance(candidates, list) or len(candidates) >= 1000:
        return {"exit_id": "blocked", "reason_code": "created_issue_result_not_unique"}
    matches = [_read_issue(repo, item["number"]) for item in candidates if type(item.get("number")) is int]
    exact = [item for item in matches if _same_issue(item, draft, reviewed_at, created_body)]
    if len(exact) != 1:
        return {"exit_id": "blocked", "reason_code": "created_issue_result_not_unique"}
    return _result(repo, exact[0])


def run(package_root: Path, command: dict, argv: list[str]) -> dict[str, Any]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    output = invoke(read_json(args.input, "input"), command_id=command.get("id", "invoke-guru-create-issue"))
    if "exit_id" in output:
        validate_json(output, package_root / "schemas/public-output.schema.json", "stdout")
    return output


def main(argv: list[str]) -> int:
    try:
        write_json(run(PACKAGE, {}, argv))
        return 0
    except CommandError as exc:
        return fail(exc)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
