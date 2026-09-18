from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json


def load(root: Path, package_root: Path, value: str, field: str) -> dict:
    path = Path(value)
    choices = [path] if path.is_absolute() else [root / path, package_root / path]
    source = next((candidate for candidate in choices if candidate.is_file() and not candidate.is_symlink()), None)
    if source is None:
        raise CommandError("invalid_json", field, "Provide one regular JSON file.")
    try:
        payload = json.loads(source.read_text())
    except json.JSONDecodeError as exc:
        raise CommandError("invalid_json", field, "Provide valid JSON.") from exc
    if not isinstance(payload, dict):
        raise CommandError("invalid_json", field, "Provide one object.")
    return payload


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode:
        raise CommandError("stale_identity", "bookkeeping", proc.stderr.strip() or "Refresh the reviewed Git facts.", 3)
    return proc


def gh(repo_ref: str, *args: str) -> str:
    proc = subprocess.run(["gh", *args, "--repo", repo_ref], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise CommandError("stale_identity", "bookkeeping.github", proc.stderr.strip() or "Refresh the reviewed GitHub facts.", 3)
    return proc.stdout


def gh_json(repo_ref: str, *args: str):
    try:
        return json.loads(gh(repo_ref, *args))
    except json.JSONDecodeError as exc:
        raise CommandError("invalid_json", "bookkeeping.github", "GitHub returned invalid JSON.") from exc


def finish_ref(public: dict) -> str:
    suffix = hashlib.sha256((public["task_ref"] + public["closure_ref"]).encode()).hexdigest()[:16]
    return "finish:v1:" + suffix


def transaction_path(root: Path, public: dict) -> Path:
    return root / ".trellis/.runtime/guru-team/finish" / (finish_ref(public).split(":")[-1] + ".json")


def write_transaction(path: Path, payload: dict, package_root: Path) -> None:
    validate_json(payload, package_root / "schemas/finish-transaction.schema.json", "finish_transaction")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def read_transaction(path: Path, public: dict, bookkeeping: dict, package_root: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise CommandError("stale_identity", "finish_transaction", "Discard the invalid private Finish transaction before retry.", 3) from exc
    validate_json(payload, package_root / "schemas/finish-transaction.schema.json", "finish_transaction")
    expected = {"task_ref": public["task_ref"], "closure_ref": public["closure_ref"], "finish_ref": finish_ref(public), "repo_ref": bookkeeping["repo_ref"], "base_branch": bookkeeping["base_branch"], "head_branch": bookkeeping["head_branch"]}
    if any(payload.get(key) != value for key, value in expected.items()):
        raise CommandError("stale_identity", "finish_transaction", "The private Finish transaction belongs to another identity.", 3)
    return payload


def lifecycle_roots(public: dict, semantic: dict) -> tuple[Path, str, Path, tuple[str, ...]]:
    task_dir = Path(public["task_ref"])
    archive_ref = semantic["bookkeeping"]["archive_ref"]
    if archive_ref not in semantic["allowlist"] or archive_ref.count("/") != 4 or Path(archive_ref).name != task_dir.name or public["task_ref"] not in semantic["allowlist"]:
        raise CommandError("stale_identity", "semantic_result.allowlist", "Finish requires one exact active path and one exact final archive root.", 3)
    archive_roots = [entry for entry in semantic["allowlist"] if entry.startswith(".trellis/tasks/archive/")]
    if any(entry.count("/") != 4 or Path(entry).name != task_dir.name for entry in archive_roots):
        raise CommandError("stale_identity", "semantic_result.allowlist", "Every archive root must belong to the current task identity.", 3)
    permitted = tuple(sorted({public["task_ref"], *archive_roots}))
    if any(not (entry == public["task_ref"] or entry.startswith(public["task_ref"] + "/") or entry.startswith(".trellis/tasks/archive/")) for entry in semantic["allowlist"]):
        raise CommandError("stale_identity", "semantic_result.allowlist", "Finish allowlist contains paths outside task lifecycle storage.", 3)
    return task_dir, archive_ref, Path(archive_ref), permitted


def changed_paths(root: Path) -> set[str]:
    paths = set(git(root, "diff", "--name-only", "HEAD").stdout.splitlines())
    paths.update(git(root, "diff", "--cached", "--name-only").stdout.splitlines())
    paths.update(git(root, "ls-files", "--others", "--exclude-standard").stdout.splitlines())
    return {path for path in paths if path}


def path_allowed(path: str, allowlist: tuple[str, ...]) -> bool:
    return any(path == allowed or path.startswith(allowed + "/") for allowed in allowlist)


def verify_payload(bookkeeping: dict) -> None:
    text = "\n".join([bookkeeping["commit_subject"], bookkeeping["commit_body"], bookkeeping["pr_title"], bookkeeping["pr_body"], bookkeeping["merge_subject"], bookkeeping["merge_body"]])
    if re.search(r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?[ \t]*(?:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)?#[1-9][0-9]*\b", text):
        raise CommandError("stale_identity", "semantic_result.bookkeeping", "Bookkeeping payload must not close an Issue.", 3)
    if "Guru-Delivery-Task:" in text or "Guru-Delivery-Cycle:" in text:
        raise CommandError("stale_identity", "semantic_result.bookkeeping", "Bookkeeping payload must not publish a business Delivery identity.", 3)


def project_archive(root: Path, public: dict, task_ref: Path, archive_ref: str, archive_path: Path) -> None:
    task_dir = root / task_ref
    archive_dir = root / archive_path
    if archive_dir.exists():
        raise CommandError("stale_identity", "archive_ref", "Target archive already exists; rebuild the reviewed Finish transaction.", 3)
    task_path = task_dir / "task.json"
    if not task_path.is_file() or task_path.is_symlink():
        raise CommandError("stale_identity", "task_ref", "Active task metadata is missing or unsafe.", 3)
    task = json.loads(task_path.read_text())
    if task.get("id") and task.get("id") != task_dir.name:
        raise CommandError("stale_identity", "task.json.id", "Task identity does not match the active locator.", 3)
    task["status"] = "completed"
    task["completedAt"] = datetime.now(timezone.utc).date().isoformat()
    task["archive_dir"] = archive_ref
    archive_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(task_dir), str(archive_dir))
    (archive_dir / "task.json").write_text(json.dumps(task, ensure_ascii=False, indent=2) + "\n")
    branch = git(root, "branch", "--show-current").stdout.strip() or "detached"
    summary = {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "generator": "guru-team.finalize-task",
        "task": {"slug": archive_dir.name, "title": task.get("title", archive_dir.name), "status": "completed", "artifact_dir": public["task_ref"], "archive_dir": archive_ref},
        "git": {"base_branch": task.get("base_branch", "main"), "branch": branch, "commits": [], "changed_paths": []},
        "github": {"pr_url": ""},
        "artifacts": {key: name for key, name in (("prd", "prd.md"), ("design", "design.md"), ("implement", "implement.md")) if (archive_dir / name).is_file()},
        "index": {"problem": task.get("title", archive_dir.name), "outcome": "任务已完成并归档。", "changed_behavior": ["持久化 Completion、Closure 与 Finish 终态"], "affected_surfaces": [{"kind": "task-artifact", "name": "task archive", "paths": [archive_ref], "change": "归档当前 task 并写入完成摘要。"}], "contract_changes": [], "search_terms": {"issue_refs": [], "pr_refs": [], "branches": [branch], "paths": [], "commands": [], "config_keys": [], "schema_fields": [], "symbols": [], "phrases": ["完成任务归档", "写入完成摘要", "保留 task identity"]}, "retrieval_text": f"{task.get('title', archive_dir.name)}；完成任务归档；写入完成摘要；保留 task identity"},
    }
    schema = root / ".trellis/guru-team/schemas/finish-summary.schema.json"
    if schema.is_file():
        validate_json(summary, schema, "finish_summary")
    (archive_dir / "finish-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")


def current_remote_head(root: Path, base_branch: str) -> str:
    git(root, "fetch", "--no-tags", "origin", f"refs/heads/{base_branch}:refs/remotes/origin/{base_branch}")
    return git(root, "rev-parse", f"refs/remotes/origin/{base_branch}").stdout.strip()


def exact_pr(repo_ref: str, number: int, bookkeeping: dict, expected_head: str) -> dict:
    pr = gh_json(repo_ref, "pr", "view", str(number), "--json", "number,url,state,isDraft,title,body,headRefName,headRefOid,baseRefName,mergedAt,mergeCommit")
    required = {"number", "url", "state", "isDraft", "title", "body", "headRefName", "headRefOid", "baseRefName"}
    if not isinstance(pr, dict) or not required.issubset(pr):
        raise CommandError("stale_identity", "bookkeeping.pr", "GitHub returned incomplete bookkeeping PR facts.", 3)
    if pr["number"] != number or pr["title"] != bookkeeping["pr_title"] or pr["body"] != bookkeeping["pr_body"] or pr["headRefName"] != bookkeeping["head_branch"] or pr["headRefOid"] != expected_head or pr["baseRefName"] != bookkeeping["base_branch"] or pr["isDraft"]:
        raise CommandError("stale_identity", "bookkeeping.pr", "The live bookkeeping PR differs from the reviewed payload or expected head.", 3)
    return pr


def publish(root: Path, public: dict, bookkeeping: dict, allowlist: tuple[str, ...], transaction_file: Path, transaction: dict | None, package_root: Path) -> dict:
    verify_payload(bookkeeping)
    if git(root, "branch", "--show-current").stdout.strip() != bookkeeping["head_branch"]:
        raise CommandError("stale_identity", "bookkeeping.head_branch", "Run Finish only in the reviewed task worktree and branch.", 3)
    if bookkeeping["head_branch"] == bookkeeping["base_branch"]:
        raise CommandError("stale_identity", "bookkeeping.head_branch", "Bookkeeping must not commit directly on the target base branch.", 3)
    if current_remote_head(root, bookkeeping["base_branch"]) != bookkeeping["expected_base_head"]:
        raise CommandError("stale_identity", "bookkeeping.expected_base_head", "The target baseline changed before bookkeeping publication.", 3)
    if transaction is None:
        paths = changed_paths(root)
        if not paths or any(not path_allowed(path, allowlist) for path in paths):
            raise CommandError("stale_identity", "semantic_result.allowlist", "The bookkeeping diff is empty or contains a path outside the reviewed lifecycle allowlist.", 3)
        parent_head = git(root, "rev-parse", "HEAD").stdout.strip()
        if git(root, "merge-base", "--is-ancestor", parent_head, bookkeeping["expected_base_head"], check=False).returncode:
            raise CommandError("stale_identity", "bookkeeping.expected_base_head", "The business branch is not contained in the reviewed target baseline.", 3)
        transaction = {"schema_version": "1.0", "stage": "publish_prepared", "task_ref": public["task_ref"], "closure_ref": public["closure_ref"], "finish_ref": finish_ref(public), "repo_ref": bookkeeping["repo_ref"], "base_branch": bookkeeping["base_branch"], "head_branch": bookkeeping["head_branch"], "expected_base_head": bookkeeping["expected_base_head"], "archive_ref": bookkeeping["archive_ref"], "parent_head": parent_head}
        write_transaction(transaction_file, transaction, package_root)
    parent_head = transaction["parent_head"]
    if transaction["stage"] == "publish_prepared":
        live_head = git(root, "rev-parse", "HEAD").stdout.strip()
        if live_head == parent_head:
            git(root, "add", "-A", "--", *allowlist)
            if any(not path_allowed(path, allowlist) for path in set(git(root, "diff", "--cached", "--name-only").stdout.splitlines())):
                raise CommandError("stale_identity", "semantic_result.allowlist", "Staging escaped the reviewed bookkeeping allowlist.", 3)
            message = bookkeeping["commit_subject"] + ("\n\n" + bookkeeping["commit_body"] if bookkeeping["commit_body"] else "")
            git(root, "commit", "-m", message)
            live_head = git(root, "rev-parse", "HEAD").stdout.strip()
        elif git(root, "rev-parse", f"{live_head}^").stdout.strip() != parent_head:
            raise CommandError("stale_identity", "finish_transaction", "Local HEAD escaped the prepared bookkeeping transaction.", 3)
        else:
            expected_message = bookkeeping["commit_subject"] + ("\n\n" + bookkeeping["commit_body"] if bookkeeping["commit_body"] else "")
            actual_message = git(root, "show", "-s", "--format=%B", live_head).stdout.rstrip("\n")
            recovered_paths = set(git(root, "diff", "--name-only", parent_head, live_head).stdout.splitlines())
            if actual_message != expected_message or not recovered_paths or any(not path_allowed(path, allowlist) for path in recovered_paths):
                raise CommandError("stale_identity", "finish_transaction", "The recovered commit does not match the reviewed bookkeeping message and allowlist.", 3)
        transaction.update({"stage": "committed", "commit": live_head})
        write_transaction(transaction_file, transaction, package_root)
    commit = transaction["commit"]
    if git(root, "rev-parse", "HEAD").stdout.strip() != commit or changed_paths(root):
        raise CommandError("stale_identity", "finish_transaction", "The committed bookkeeping candidate is no longer exact and clean.", 3)
    remote = git(root, "ls-remote", "--heads", "origin", f"refs/heads/{bookkeeping['head_branch']}").stdout.strip().split()
    if remote and remote[0] not in {parent_head, commit}:
        raise CommandError("stale_identity", "bookkeeping.head_branch", "The remote bookkeeping branch moved outside this Finish transaction.", 3)
    if not remote or remote[0] != commit:
        git(root, "push", "origin", f"HEAD:refs/heads/{bookkeeping['head_branch']}")
    rows = gh_json(bookkeeping["repo_ref"], "pr", "list", "--state", "open", "--head", bookkeeping["head_branch"], "--base", bookkeeping["base_branch"], "--json", "number,url,state,isDraft,title,body,headRefName,headRefOid,baseRefName")
    if not isinstance(rows, list) or len(rows) > 1:
        raise CommandError("stale_identity", "bookkeeping.pr", "Bookkeeping PR discovery is ambiguous.", 3)
    if rows:
        number = rows[0].get("number")
    else:
        url = gh(bookkeeping["repo_ref"], "pr", "create", "--base", bookkeeping["base_branch"], "--head", bookkeeping["head_branch"], "--title", bookkeeping["pr_title"], "--body", bookkeeping["pr_body"]).strip()
        match = re.fullmatch(r"https://github\.com/[^/]+/[^/]+/pull/([1-9][0-9]*)", url)
        if not match:
            raise CommandError("stale_identity", "bookkeeping.pr", "GitHub did not return one canonical bookkeeping PR URL.", 3)
        number = int(match.group(1))
    pr = exact_pr(bookkeeping["repo_ref"], int(number), bookkeeping, commit)
    transaction.update({"stage": "pr_open", "pr_number": pr["number"], "pr_url": pr["url"]})
    write_transaction(transaction_file, transaction, package_root)
    return transaction


def verify_target(root: Path, transaction: dict, public: dict) -> str:
    target_head = current_remote_head(root, transaction["base_branch"])
    archive_probe = git(root, "cat-file", "-e", f"{target_head}:{transaction['archive_ref']}/task.json", check=False)
    summary_probe = git(root, "cat-file", "-e", f"{target_head}:{transaction['archive_ref']}/finish-summary.json", check=False)
    active_probe = git(root, "cat-file", "-e", f"{target_head}:{public['task_ref']}/task.json", check=False)
    if archive_probe.returncode or summary_probe.returncode or active_probe.returncode == 0:
        raise CommandError("stale_identity", "bookkeeping.target", "The target baseline does not contain the unique terminal archive state.", 3)
    return target_head


def merge(root: Path, public: dict, bookkeeping: dict, transaction: dict, transaction_file: Path, package_root: Path) -> dict:
    pr = exact_pr(bookkeeping["repo_ref"], transaction["pr_number"], bookkeeping, transaction["commit"])
    if str(pr["state"]).upper() != "MERGED":
        if current_remote_head(root, bookkeeping["base_branch"]) != transaction["expected_base_head"]:
            raise CommandError("stale_identity", "bookkeeping.expected_base_head", "The target baseline changed before bookkeeping merge.", 3)
        gh(bookkeeping["repo_ref"], "pr", "merge", str(transaction["pr_number"]), "--merge", "--match-head-commit", transaction["commit"], "--subject", bookkeeping["merge_subject"], "--body", bookkeeping["merge_body"])
        pr = exact_pr(bookkeeping["repo_ref"], transaction["pr_number"], bookkeeping, transaction["commit"])
    if str(pr["state"]).upper() != "MERGED" or not pr.get("mergedAt") or not isinstance(pr.get("mergeCommit"), dict) or not pr["mergeCommit"].get("oid"):
        raise CommandError("stale_identity", "bookkeeping.pr", "The bookkeeping PR is not terminally merged.", 3)
    target_head = verify_target(root, transaction, public)
    if target_head != pr["mergeCommit"]["oid"]:
        raise CommandError("stale_identity", "bookkeeping.target", "The target branch no longer points at the verified bookkeeping merge.", 3)
    transaction.update({"stage": "success", "target_head": target_head})
    write_transaction(transaction_file, transaction, package_root)
    return transaction


def resume(public: dict, reason_code: str, remediation: str) -> dict:
    return {"exit_id": "resume_finish", "task_ref": public["task_ref"], "closure_exit": public["closure_exit"], "closure_ref": public["closure_ref"]}


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    parser.add_argument("--confirmed-finish", action="store_true")
    parser.add_argument("--confirmed-bookkeeping-publish", action="store_true")
    parser.add_argument("--confirmed-bookkeeping-merge", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the finish command contract.") from exc
    root = Path(args.root or ".").resolve()
    public = load(root, package_root, args.input, "input")
    semantic = load(root, package_root, args.semantic_result, "semantic_result")
    validate_json(public, package_root / "schemas/public-input.schema.json", "input")
    validate_json(semantic, package_root / "schemas/semantic-result.schema.json", "semantic_result")
    if public["profile"] != semantic["profile"] or public["mode"] != semantic["mode"]:
        raise CommandError("stale_identity", "semantic_result", "Finish identity differs from Closure.", 3)
    route = semantic["route"]
    if route["typed_exit"] != "success":
        out = {"exit_id": route["typed_exit"]}
        validate_json(out, package_root / "schemas/public-output.schema.json", "stdout")
        return out
    bookkeeping = semantic["bookkeeping"]
    task_ref, archive_ref, archive_path, allowlist = lifecycle_roots(public, semantic)
    task_dir = root / task_ref
    archive_dir = root / archive_path
    if task_dir.is_dir():
        if not args.confirmed_finish:
            return resume(public, "confirmation_required", "Confirm the reviewed local archive projection.")
        project_archive(root, public, task_ref, archive_ref, archive_path)
        return resume(public, "bookkeeping_publication_required", "Review and confirm the exact bookkeeping commit, push and PR payload.")
    if not archive_dir.is_dir():
        raise CommandError("stale_identity", "task_ref", "Active task or its current archive is missing.", 3)
    transaction_file = transaction_path(root, public)
    transaction = read_transaction(transaction_file, public, bookkeeping, package_root)
    if transaction is None or transaction.get("stage") in {"projected", "publish_prepared", "committed"}:
        if not args.confirmed_bookkeeping_publish:
            return resume(public, "bookkeeping_publication_confirmation_required", "Confirm the reviewed bookkeeping commit, push and PR creation.")
        transaction = publish(root, public, bookkeeping, allowlist, transaction_file, transaction, package_root)
    if transaction.get("stage") == "pr_open":
        if not args.confirmed_bookkeeping_merge:
            return resume(public, "bookkeeping_merge_confirmation_required", "Confirm the exact expected-head bookkeeping PR merge.")
        transaction = merge(root, public, bookkeeping, transaction, transaction_file, package_root)
    if transaction.get("stage") != "success":
        return resume(public, "bookkeeping_verification_required", "Recover and verify the same bookkeeping transaction.")
    target_head = verify_target(root, transaction, public)
    if target_head != transaction["target_head"]:
        raise CommandError("stale_identity", "bookkeeping.target", "The verified target baseline changed after Finish success.", 3)
    out = {"exit_id": "success", "task_ref": public["task_ref"], "archive_ref": archive_ref, "finish_ref": finish_ref(public)}
    validate_json(out, package_root / "schemas/public-output.schema.json", "stdout")
    return out


if __name__ == "__main__":
    try:
        print(json.dumps(run(Path(__file__).parents[1], {}, sys.argv[1:]), ensure_ascii=False))
    except CommandError as exc:
        print(json.dumps({"code": exc.code, "field_path": exc.field_path, "remediation": exc.remediation}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(exc.exit_status)
