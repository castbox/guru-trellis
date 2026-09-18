from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

from runtime.io import CommandError
from runtime.schema import validate_json


DIMENSION_IDS = [
    "requirement_authority",
    "delivery_policy",
    "slice_completeness",
    "independent_delivery",
    "implementation_quality",
    "validation_truthfulness",
    "docs_rdt_architecture",
    "branch_review_freshness",
    "pr_payload_truthfulness",
    "base_and_live_facts",
]
OUTPUT_SCHEMAS = {
    "ready": "public-ready-output.schema.json",
    "planning_revision_required": "public-planning-revision-required-output.schema.json",
    "implementation_required": "public-implementation-required-output.schema.json",
    "scope_confirmation_required": "public-scope-confirmation-required-output.schema.json",
    "blocked": "public-blocked-output.schema.json",
}
_CLOSING_KEYWORD = re.compile(
    r"(?im)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s*"
    r"(?:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)?#[1-9][0-9]*\b"
)
_ISSUE_URL = re.compile(r"github\.com/[^/]+/[^/]+/issues/(\d+)")


def parse(parser: argparse.ArgumentParser, argv: list[str]) -> argparse.Namespace:
    parser.add_argument("--json", action="store_true")
    try:
        return parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError(
            "invalid_arguments", "arguments", "Use the exact command help contract."
        ) from exc


def repo_root(value: str | None) -> Path:
    candidate = Path(value or ".").resolve()
    process = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=candidate,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise CommandError("unsafe_path", "root", "Use one Git repository root.")
    root = Path(process.stdout.strip()).resolve()
    if root != candidate:
        raise CommandError("unsafe_path", "root", "Use the exact Git repository root.")
    return root


def _lstat_below(boundary: Path, target: Path, field: str, final_kind: str) -> None:
    boundary = boundary.resolve()
    try:
        relative = target.relative_to(boundary)
    except ValueError as exc:
        raise CommandError("unsafe_path", field, "Use a path below its owner root.") from exc
    current = boundary
    for index, part in enumerate(relative.parts):
        current = current / part
        try:
            metadata = current.lstat()
        except FileNotFoundError as exc:
            raise CommandError("unsafe_path", field, "Use an existing owner path.") from exc
        if stat.S_ISLNK(metadata.st_mode):
            raise CommandError("unsafe_path", field, "Owner paths must not contain symlinks.")
        final = index == len(relative.parts) - 1
        if not final and not stat.S_ISDIR(metadata.st_mode):
            raise CommandError("unsafe_path", field, "Owner ancestors must be directories.")
        if final and final_kind == "directory" and not stat.S_ISDIR(metadata.st_mode):
            raise CommandError("unsafe_path", field, "Use one regular directory.")
        if final and final_kind == "file" and not stat.S_ISREG(metadata.st_mode):
            raise CommandError("unsafe_path", field, "Use one regular file.")


def load_json(repo: Path, package_root: Path, locator: str, field: str) -> dict[str, Any]:
    if locator == "-":
        raw = sys.stdin.read()
    else:
        path = Path(str(locator or ""))
        choices = [path] if path.is_absolute() else [repo / path, package_root / path]
        source = next((item for item in choices if item.is_file() and not item.is_symlink()), None)
        if source is None:
            raise CommandError("unsafe_path", field, "Use one regular JSON file.")
        raw = source.read_text()
    try:
        value = json.loads(raw)
    except Exception as exc:
        raise CommandError("invalid_json", field, "Provide one valid JSON object.") from exc
    if not isinstance(value, dict):
        raise CommandError("invalid_json", field, "Provide one valid JSON object.")
    return value


def task_dir(repo: Path, task_ref: str) -> Path:
    raw = str(task_ref or "")
    relative = Path(raw)
    if (
        not raw.startswith(".trellis/tasks/")
        or relative.as_posix() != raw
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        raise CommandError("unsafe_path", "task_ref", "Use one normalized active task path.")
    target = repo / relative
    _lstat_below(repo, target, "task_ref", "directory")
    tasks_root = (repo / ".trellis/tasks").resolve()
    if not target.resolve().is_relative_to(tasks_root):
        raise CommandError("unsafe_path", "task_ref", "Use one task below .trellis/tasks.")
    return target


def rel(repo: Path, path: Path) -> str:
    return path.resolve().relative_to(repo.resolve()).as_posix()


def git(repo: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if process.returncode:
        raise CommandError(
            "stale_identity",
            "repository",
            process.stderr.strip() or "Repair the current Git state.",
            3,
        )
    return process.stdout.strip()


def dirty_paths(repo: Path) -> list[str]:
    raw = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if raw.returncode:
        raise CommandError("stale_identity", "worktree", "Read current Git status.", 3)
    paths: list[str] = []
    for row in raw.stdout.split(b"\0"):
        if not row:
            continue
        try:
            path = row[3:].decode("utf-8", "strict")
        except UnicodeDecodeError as exc:
            raise CommandError("stale_identity", "worktree", "Dirty paths must be UTF-8.", 3) from exc
        if not path.startswith(".trellis/.runtime/"):
            paths.append(path)
    return paths


def task_facts(repo: Path, target: Path) -> dict[str, str]:
    metadata_path = target / "task.json"
    _lstat_below(repo, metadata_path, "task_ref", "file")
    try:
        metadata = json.loads(metadata_path.read_text())
    except Exception as exc:
        raise CommandError("invalid_json", "task_ref", "Repair current task.json.") from exc
    if not isinstance(metadata, dict) or metadata.get("status") != "in_progress":
        raise CommandError("stale_identity", "task_ref", "Use one active in_progress task.", 3)
    branch = git(repo, "branch", "--show-current")
    if not branch or metadata.get("branch") != branch:
        raise CommandError("stale_identity", "task.branch", "Use the task's current branch.", 3)
    workspace = metadata.get("worktree_path")
    if not isinstance(workspace, str) or Path(workspace).resolve() != repo:
        raise CommandError("stale_identity", "task.worktree_path", "Use the task's current worktree.", 3)
    base_branch = metadata.get("base_branch")
    if not isinstance(base_branch, str) or not base_branch.strip():
        raise CommandError("stale_identity", "task.base_branch", "Restore the task base branch.", 3)
    remote_ref = f"refs/remotes/origin/{base_branch}"
    probe = subprocess.run(
        ["git", "rev-parse", "--verify", remote_ref],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    base_ref = remote_ref if probe.returncode == 0 else base_branch
    return {
        "branch": branch,
        "base_ref": base_ref,
        "base_head": git(repo, "rev-parse", base_ref),
        "head": git(repo, "rev-parse", "HEAD"),
        "scope": str(metadata.get("scope") or ""),
    }


def checkpoint(repo: Path, target: Path) -> Path:
    return repo / ".trellis/.runtime/guru-team/owner-checkpoints" / target.name / "delivery-review-gate.json"


def _prepare_parent(repo: Path, target: Path) -> None:
    current = repo.resolve()
    for part in target.parent.relative_to(repo).parts:
        current = current / part
        if not current.exists():
            current.mkdir()
        metadata = current.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise CommandError("unsafe_path", "checkpoint", "Checkpoint ancestors must be directories.")


def store_checkpoint(repo: Path, target: Path, value: dict[str, Any]) -> tuple[Path, bool]:
    path = checkpoint(repo, target)
    _prepare_parent(repo, path)
    duplicate = False
    if path.exists() or path.is_symlink():
        _lstat_below(repo, path, "checkpoint", "file")
        try:
            existing = json.loads(path.read_text())
        except Exception as exc:
            raise CommandError("invalid_json", "checkpoint", "Remove the invalid private gate.") from exc
        duplicate = _without_generated(existing) == _without_generated(value)
    if not duplicate:
        path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    return path, duplicate


def load_checkpoint(repo: Path, target: Path) -> tuple[Path, dict[str, Any]]:
    path = checkpoint(repo, target)
    _lstat_below(repo, path, "checkpoint", "file")
    try:
        value = json.loads(path.read_text())
    except Exception as exc:
        raise CommandError("invalid_json", "checkpoint", "Record one valid private gate.") from exc
    if not isinstance(value, dict):
        raise CommandError("invalid_json", "checkpoint", "Record one valid private gate.")
    return path, value


def retire_checkpoint(repo: Path, target: Path) -> None:
    path, _ = load_checkpoint(repo, target)
    path.unlink()
    try:
        path.parent.rmdir()
    except OSError:
        pass


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _without_generated(value: dict[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(item) for key, item in value.items() if key != "generated_at"}


def cycle_ref(task_ref: str, reviewed_head: str, payload: dict[str, str]) -> str:
    return "delivery-cycle:v1:" + digest(
        {"task_ref": task_ref, "reviewed_head": reviewed_head, "pr_payload": payload}
    )


def validate_semantic(package_root: Path, public: dict[str, Any], semantic: dict[str, Any], scope: str) -> str:
    validate_json(semantic, package_root / "schemas/semantic-result.schema.json", "semantic_result")
    if semantic["profile"] != public["profile"] or semantic["mode"] != public["mode"]:
        raise CommandError("schema_mismatch", "semantic_result", "Author the result for the exact public input.")
    dimensions = semantic["dimensions"]
    if [item["id"] for item in dimensions] != DIMENSION_IDS:
        raise CommandError("schema_mismatch", "dimensions", "Use the exact ordered Delivery Review dimensions.")
    for key in ("candidate_ref", "finding_ref", "proposal_ref"):
        collections = {
            "candidate_ref": semantic["candidate_classifications"],
            "finding_ref": semantic["findings"],
            "proposal_ref": semantic["scope_proposals"],
        }
        refs = [item[key] for item in collections[key]]
        if len(refs) != len(set(refs)):
            raise CommandError("schema_mismatch", key, "Use unique semantic references.")
    candidate_refs = {item["candidate_ref"] for item in semantic["candidate_classifications"]}
    if any(item["candidate_ref"] not in candidate_refs for item in semantic["findings"] + semantic["scope_proposals"]):
        raise CommandError("schema_mismatch", "candidate_classifications", "Bind every finding and proposal to a classified candidate.")
    dimension_status = {item["id"]: item["status"] for item in dimensions}
    for finding in semantic["findings"]:
        if finding["dimension"] not in dimension_status:
            raise CommandError("schema_mismatch", "findings.dimension", "Bind findings to one declared dimension.")
        if finding["status"] == "open" and finding["closure_evidence"]:
            raise CommandError("schema_mismatch", "findings.closure_evidence", "Open findings have no closure evidence.")
        if finding["status"] == "closed" and not finding["closure_evidence"]:
            raise CommandError("schema_mismatch", "findings.closure_evidence", "Closed findings require closure evidence.")
    policy = semantic["delivery_policy"]
    state = "remaining" if policy["remaining_work_refs"] else "none"
    if semantic["remaining_work_state"] != state:
        raise CommandError("schema_mismatch", "remaining_work_state", "Match the approved remaining-work set.")
    route = semantic["route"]
    exit_id = route["typed_exit"]
    open_findings = [item for item in semantic["findings"] if item["status"] == "open"]
    open_proposals = [item for item in semantic["scope_proposals"] if item["status"] == "open"]
    open_classes = {item["route_class"] for item in open_findings}
    conclusions = semantic["conclusions"].values()
    all_passed = all(item["status"] == "passed" for item in dimensions) and all(
        item["status"] == "passed" for item in conclusions
    )
    if exit_id == "ready":
        if not all_passed or open_findings or open_proposals:
            raise CommandError("schema_mismatch", "route", "Ready requires a fully passing current review.")
    elif exit_id == "planning_revision_required":
        if open_classes != {"planning_revision"} or open_proposals:
            raise CommandError("schema_mismatch", "route", "Planning re-entry requires only planning findings.")
    elif exit_id == "implementation_required":
        if "implementation" not in open_classes or "external_blocker" in open_classes or open_proposals:
            raise CommandError("schema_mismatch", "route", "Implementation re-entry requires current-slice findings only.")
    elif exit_id == "scope_confirmation_required":
        if not open_proposals or open_findings:
            raise CommandError("schema_mismatch", "route", "Scope confirmation requires proposals and no open findings.")
    elif exit_id == "blocked":
        blocked = any(item["status"] == "blocked" for item in dimensions) or any(
            item["status"] == "blocked" for item in conclusions
        )
        if "external_blocker" not in open_classes or not blocked or open_proposals:
            raise CommandError("schema_mismatch", "route", "Blocked requires one concrete external evidence blocker.")
    else:
        raise CommandError("schema_mismatch", "route.typed_exit", "Use one declared typed exit.")
    body = semantic["pr_payload"]["body"]
    if _CLOSING_KEYWORD.search(body):
        raise CommandError("schema_mismatch", "pr_payload.body", "Delivery PRs use Refs only; remove closing keywords.")
    match = _ISSUE_URL.search(scope)
    if match and not re.search(rf"(?i)\bRefs\s+#?{re.escape(match.group(1))}\b", body):
        raise CommandError("schema_mismatch", "pr_payload.body", "Reference the task Issue with Refs only.")
    return exit_id


def validate_gate(package_root: Path, repo: Path, value: dict[str, Any], expected_exit: str | None = None) -> dict[str, Any]:
    validate_json(value, package_root / "schemas/delivery-review-gate.schema.json", "checkpoint")
    validate_json(
        value["semantic_result"],
        package_root / "schemas/semantic-result.schema.json",
        "checkpoint.semantic_result",
    )
    unsigned = {key: copy.deepcopy(item) for key, item in value.items() if key not in {"generated_at", "facts_sha256"}}
    if value["facts_sha256"] != digest(unsigned):
        raise CommandError("stale_identity", "facts_sha256", "Repeat Delivery Review from current facts.", 3)
    target = task_dir(repo, value["task_ref"])
    facts = task_facts(repo, target)
    if facts["head"] != value["reviewed_head"] or value["branch_review_commit"] != value["reviewed_head"]:
        raise CommandError("stale_identity", "reviewed_head", "Repeat review for current committed HEAD.", 3)
    if facts["base_ref"] != value["base_ref"] or facts["base_head"] != value["base_head"]:
        raise CommandError("stale_identity", "base_head", "Repeat review for the current base.", 3)
    if dirty_paths(repo):
        raise CommandError("stale_identity", "worktree", "Commit or remove all post-review changes.", 3)
    exit_id = validate_semantic(
        package_root,
        {"profile": value["profile"], "mode": value["mode"]},
        value["semantic_result"],
        facts["scope"],
    )
    if expected_exit and exit_id != expected_exit:
        raise CommandError("stale_identity", "typed_exit", "Use the current checked typed exit.", 3)
    return value


def project_output(gate: dict[str, Any]) -> dict[str, Any]:
    semantic = gate["semantic_result"]
    exit_id = semantic["route"]["typed_exit"]
    output: dict[str, Any] = {"exit_id": exit_id}
    if exit_id == "ready":
        output.update(
            {
                "task_ref": gate["task_ref"],
                "delivery_cycle_ref": gate["delivery_cycle_ref"],
                "reviewed_head": gate["reviewed_head"],
                "pr_title": semantic["pr_payload"]["title"],
                "pr_body": semantic["pr_payload"]["body"],
                "remaining_work_state": semantic["remaining_work_state"],
            }
        )
    elif exit_id == "planning_revision_required":
        output.update(
            {
                "task_ref": gate["task_ref"],
                "reason_refs": [
                    item["finding_ref"]
                    for item in semantic["findings"]
                    if item["status"] == "open" and item["route_class"] == "planning_revision"
                ],
            }
        )
    elif exit_id == "implementation_required":
        output.update(
            {
                "task_ref": gate["task_ref"],
                "finding_refs": [
                    item["finding_ref"]
                    for item in semantic["findings"]
                    if item["status"] == "open" and item["route_class"] == "implementation"
                ],
                "resume_target": "phase-2",
            }
        )
    elif exit_id == "scope_confirmation_required":
        output.update(
            {
                "task_ref": gate["task_ref"],
                "proposal_refs": [
                    item["proposal_ref"]
                    for item in semantic["scope_proposals"]
                    if item["status"] == "open"
                ],
            }
        )
    elif exit_id == "blocked":
        output.update(
            {
                "reason_code": semantic["route"]["reason_code"],
                "remediation": semantic["route"]["remediation"],
            }
        )
    return output
