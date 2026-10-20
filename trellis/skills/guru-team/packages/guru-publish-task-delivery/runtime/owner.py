from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

from runtime.task_lifecycle import LifecycleContractError, resolve_active_task_checkout
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.schema import validate_json


SKILL_ID = "guru-publish-task-delivery"
STAGES = ("ensure_draft", "push_content", "bind_pr", "converge_metadata", "mark_ready", "ready", "draft", "draft_revision")
TERMINALS = {"ready", "draft", "draft_revision"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
CYCLE_REF = re.compile(r"^delivery-cycle:v1:[0-9a-f]{64}$")
TASK_REF = re.compile(r"^\.trellis/tasks/[A-Za-z0-9._/-]+$")
REPO_REF = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
REPREPARE_REQUIRED_CODES = frozenset(
    {"private_state_invalid", "private_state_missing", "task_identity_stale", "repository_identity_stale"}
)
CLOSING = re.compile(
    r"(?im)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s*"
    r"(?:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)?#[1-9][0-9]*\b"
)


class WorkflowError(RuntimeError):
    def __init__(self, message: str, *, code: str = "publication_stale", payload: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.payload = payload or {}


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def read_json(locator: str | Path) -> dict[str, Any]:
    path = Path(locator)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"Cannot read JSON: {path}", code="invalid_json") from exc
    if not isinstance(value, dict):
        raise WorkflowError(f"JSON object required: {path}", code="schema_mismatch")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(canonical(value))
    os.replace(temporary, path)


def _run(root: Path, command: list[str], *, allow_failure: bool = False) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if completed.returncode and not allow_failure:
        raise WorkflowError(
            f"Command failed: {' '.join(command)}",
            code="external_command_failed",
            payload={"command": command[0], "stderr": completed.stderr.strip()},
        )
    return completed


def repo_root(path: Path) -> Path:
    completed = _run(path.resolve(), ["git", "rev-parse", "--show-toplevel"])
    return Path(completed.stdout.strip()).resolve()


def git_text(root: Path, *args: str) -> str:
    return _run(root, ["git", *args]).stdout.strip()


def is_ancestor(root: Path, older: str, newer: str) -> bool:
    return _run(root, ["git", "merge-base", "--is-ancestor", older, newer], allow_failure=True).returncode == 0


def gh_json(root: Path, command: list[str]) -> Any:
    completed = _run(root, ["gh", *command])
    try:
        return json.loads(completed.stdout or "null")
    except json.JSONDecodeError as exc:
        raise WorkflowError("GitHub command returned invalid JSON.", code="external_command_failed") from exc


def validate_public_input(value: dict[str, Any]) -> dict[str, Any]:
    if value.get("profile") in {"delivery_remote_draft_recovery", "delivery_remote_ready_recovery"}:
        package = Path(__file__).resolve().parents[1]
        name = value["profile"].replace("_", "-")
        validate_json(value, package / f"schemas/public-{name}-input-1.0.schema.json", "input")
        if CLOSING.search(value["pr_body"]):
            raise WorkflowError("Delivery PR body contains a closing keyword.", code="closing_keyword_forbidden")
        return value
    delivery_profile = str(value.get("profile", "")).startswith("delivery_")
    profile = str(value.get("profile", "")).removeprefix("delivery_")
    common = {"profile", "mode", "task_ref"}
    if profile == "review_ready":
        required = common | {"delivery_cycle_ref", "reviewed_head", "pr_title", "pr_body", "remaining_work_state"}
    elif profile == "draft_publish":
        required = common | {"delivery_key", "base_ref", "candidate_head", "pr_title", "pr_body"}
    elif profile == "return_to_draft":
        required = common | {"delivery_key", "revision_reason"}
    elif profile == "same_plan_resume":
        required = common | {"transaction_ref"}
    elif profile == "reprepare_publication":
        required = common | {"reason_code"}
    else:
        raise WorkflowError("Unknown publication input profile.", code="schema_mismatch")
    if delivery_profile:
        required.add("delivery_key")
        if profile == "review_ready":
            required.remove("delivery_cycle_ref")
            required.add("readiness_result_id")
    if set(value) != required:
        raise WorkflowError("Publication input fields do not match the selected closed profile.", code="schema_mismatch")
    if value.get("mode") not in {"workflow", "standalone"}:
        raise WorkflowError("Unsupported publication mode.", code="schema_mismatch")
    if not isinstance(value.get("task_ref"), str) or TASK_REF.fullmatch(value["task_ref"]) is None:
        raise WorkflowError("Invalid task_ref.", code="schema_mismatch")
    if profile in {"draft_publish", "return_to_draft"} and not delivery_profile:
        raise WorkflowError("Draft entries require the current public Delivery identity.", code="schema_mismatch")
    if profile in {"review_ready", "draft_publish"}:
        if profile == "review_ready" and not delivery_profile and (not isinstance(value["delivery_cycle_ref"], str) or CYCLE_REF.fullmatch(value["delivery_cycle_ref"]) is None):
            raise WorkflowError("delivery_cycle_ref must use the current closed identity.", code="schema_mismatch")
        if not isinstance(value.get("reviewed_head", value.get("candidate_head")), str) or SHA40.fullmatch(value.get("reviewed_head", value.get("candidate_head", ""))) is None:
            raise WorkflowError("reviewed_head must be a full lowercase commit id.", code="schema_mismatch")
        for field in (("pr_title", "pr_body", "remaining_work_state") if profile == "review_ready" else ("pr_title", "pr_body", "base_ref")):
            if not isinstance(value[field], str) or not value[field].strip():
                raise WorkflowError(f"{field} is required.", code="schema_mismatch")
        if profile == "review_ready" and value["remaining_work_state"] not in {"none", "remaining"}:
            raise WorkflowError("remaining_work_state must be none or remaining.", code="schema_mismatch")
        if CLOSING.search(value["pr_body"]):
            raise WorkflowError("Delivery PR body contains a closing keyword.", code="closing_keyword_forbidden")
    elif profile == "same_plan_resume":
        if not isinstance(value["transaction_ref"], str) or SHA64.fullmatch(value["transaction_ref"]) is None:
            raise WorkflowError("transaction_ref must be a lowercase SHA-256 value.", code="schema_mismatch")
    elif profile == "return_to_draft":
        if not isinstance(value["revision_reason"], str) or not value["revision_reason"].strip():
            raise WorkflowError("State the concrete same-Delivery revision reason.", code="schema_mismatch")
    elif not isinstance(value["reason_code"], str) or not value["reason_code"]:
        raise WorkflowError("reason_code is required.", code="schema_mismatch")
    return value


def validate_review(value: dict[str, Any], expected_exit: str = "ready_for_merge") -> dict[str, Any]:
    required = {"schema_version", "skill_id", "review", "route"}
    if set(value) != required or value.get("schema_version") != "1.0" or value.get("skill_id") != SKILL_ID:
        raise WorkflowError("Semantic review identity is invalid.", code="schema_mismatch")
    review = value.get("review")
    route = value.get("route")
    if not isinstance(review, dict) or set(review) != {"status", "summary"}:
        raise WorkflowError("Semantic review shape is invalid.", code="schema_mismatch")
    if review.get("status") != "passed" or not isinstance(review.get("summary"), str) or not review["summary"].strip():
        raise WorkflowError("A passed semantic publication review is required.", code="schema_mismatch")
    if not isinstance(route, dict) or set(route) != {"typed_exit"} or route.get("typed_exit") != expected_exit:
        raise WorkflowError("Semantic review route must match the selected publication action.", code="schema_mismatch")
    return value


def task_context(root: Path, task_ref: str) -> tuple[Path, dict[str, Any]]:
    task_dir = (root / task_ref).resolve()
    if root not in task_dir.parents or not task_dir.is_dir():
        raise WorkflowError("Task locator is outside the repository or missing.", code="unsafe_path")
    task = read_json(task_dir / "task.json")
    if task.get("schema_version") == "2.0":
        task = DeliveryProjection(root, task_ref).read_record()
    elif task.get("status") != "in_progress":
        raise WorkflowError("Delivery publication requires an active task.", code="task_not_active")
    try:
        branch = resolve_active_task_checkout(root, task_ref).branch_name
    except LifecycleContractError as exc:
        raise WorkflowError(exc.remediation, code="task_identity_stale") from exc
    base = task.get("base_branch")
    if not isinstance(base, str) or not base:
        raise WorkflowError("Task base branch is incomplete.", code="task_identity_stale")
    return task_dir, {**task, "branch": branch}


def repository_identity(root: Path) -> str:
    from runtime.task_lifecycle.identity import origin_matches
    value = gh_json(root, ["repo", "view", git_text(root, "remote", "get-url", "origin"), "--json", "nameWithOwner"])
    repo = value.get("nameWithOwner") if isinstance(value, dict) else None
    if not isinstance(repo, str) or REPO_REF.fullmatch(repo) is None or not origin_matches(root, repo):
        raise WorkflowError("Cannot resolve canonical GitHub repository identity.", code="repository_identity_stale")
    return repo


def remote_head(root: Path, branch: str) -> str | None:
    completed = _run(root, ["git", "ls-remote", "--heads", "origin", f"refs/heads/{branch}"])
    line = completed.stdout.strip()
    if not line:
        return None
    head = line.split()[0]
    if SHA40.fullmatch(head) is None:
        raise WorkflowError("Remote branch returned an invalid commit id.", code="remote_identity_stale")
    return head


def list_open_prs(root: Path, branch: str) -> list[dict[str, Any]]:
    fields = "number,url,state,isDraft,title,body,headRefName,headRefOid,baseRefName,headRepositoryOwner"
    value = gh_json(root, ["pr", "list", "--repo", repository_identity(root), "--state", "open", "--head", branch, "--json", fields])
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise WorkflowError("GitHub PR listing has invalid shape.", code="external_command_failed")
    return value


def same_repo_pr(pr: dict[str, Any], repo_ref: str, branch: str, base: str) -> bool:
    owner = repo_ref.split("/", 1)[0].lower()
    head_owner = pr.get("headRepositoryOwner")
    if isinstance(head_owner, dict):
        head_owner = head_owner.get("login")
    return (
        pr.get("state") == "OPEN"
        and pr.get("headRefName") == branch
        and pr.get("baseRefName") == base
        and isinstance(pr.get("url"), str)
        and pr["url"].startswith(f"https://github.com/{repo_ref}/pull/")
        and isinstance(head_owner, str)
        and head_owner.lower() == owner
    )


def normalize_pr(pr: dict[str, Any]) -> dict[str, Any]:
    number = pr.get("number")
    head = pr.get("headRefOid")
    if not isinstance(number, int) or number < 1 or not isinstance(head, str) or SHA40.fullmatch(head) is None:
        raise WorkflowError("GitHub PR identity is incomplete.", code="pr_identity_stale")
    return {
        "number": number,
        "url": pr.get("url"),
        "state": pr.get("state"),
        "is_draft": bool(pr.get("isDraft")),
        "title": pr.get("title"),
        "body": pr.get("body"),
        "head_branch": pr.get("headRefName"),
        "head_sha": head,
        "base_branch": pr.get("baseRefName"),
        "head_owner": (pr.get("headRepositoryOwner") or {}).get("login") if isinstance(pr.get("headRepositoryOwner"), dict) else pr.get("headRepositoryOwner"),
    }


def read_pr(root: Path, number: int) -> dict[str, Any]:
    fields = "number,url,state,isDraft,title,body,headRefName,headRefOid,baseRefName,headRepositoryOwner"
    value = gh_json(root, ["pr", "view", str(number), "--repo", repository_identity(root), "--json", fields])
    if not isinstance(value, dict):
        raise WorkflowError("GitHub PR read has invalid shape.", code="external_command_failed")
    return normalize_pr(value)


def transaction_ref(public_input: dict[str, Any]) -> str:
    if public_input["profile"].removeprefix("delivery_") == "same_plan_resume":
        return public_input["transaction_ref"]
    if public_input["profile"] in {"delivery_draft_publish", "delivery_return_to_draft", "delivery_remote_draft_recovery", "delivery_remote_ready_recovery"}:
        return digest({"skill_id": SKILL_ID, "input": public_input})
    identity = {"delivery_key": public_input["delivery_key"], "readiness_result_id": public_input["readiness_result_id"]} if "delivery_key" in public_input else {"delivery_cycle_ref": public_input["delivery_cycle_ref"]}
    return digest({"skill_id": SKILL_ID, "task_ref": public_input["task_ref"], **identity})


def unique_task_transaction(root: Path, task_ref: str, delivery_key: dict | None = None) -> dict[str, Any]:
    owner_dir = root / ".trellis/.runtime/guru-team/guru-publish-task-delivery"
    matches: list[dict[str, Any]] = []
    if owner_dir.is_dir():
        for path in sorted(owner_dir.glob("*.json")):
            if path.name.endswith(".gate.json"):
                continue
            value = read_json(path)
            if isinstance(value.get("input"), dict) and value["input"].get("task_ref") == task_ref and (delivery_key is None or value["input"].get("delivery_key") == delivery_key):
                if value.get("stage") in TERMINALS:
                    continue
                validate_transaction(value)
                matches.append(value)
    if len(matches) != 1:
        raise WorkflowError("Reprepare requires exactly one active task publication transaction.", code="private_state_invalid")
    return matches[0]


def transaction_path(root: Path, ref: str) -> Path:
    if SHA64.fullmatch(ref) is None:
        raise WorkflowError("Invalid transaction reference.", code="unsafe_path")
    return root / ".trellis/.runtime/guru-team/guru-publish-task-delivery" / f"{ref}.json"


def load_transaction(root: Path, ref: str) -> dict[str, Any] | None:
    path = transaction_path(root, ref)
    return read_json(path) if path.is_file() else None


def save_transaction(root: Path, transaction: dict[str, Any]) -> None:
    transaction["transaction_sha256"] = digest({key: value for key, value in transaction.items() if key != "transaction_sha256"})
    write_json(transaction_path(root, transaction["transaction_ref"]), transaction)


def validate_transaction(transaction: dict[str, Any]) -> None:
    if transaction.get("schema_version") != "2.0" or transaction.get("skill_id") != SKILL_ID:
        raise WorkflowError("Private transaction identity is invalid.", code="private_state_invalid")
    if transaction.get("action") not in {"ready", "draft_publish", "return_to_draft"} or transaction.get("terminal") != {"ready":"ready", "draft_publish":"draft", "return_to_draft":"draft_revision"}.get(transaction.get("action")):
        raise WorkflowError("Private action/terminal contract is invalid.", code="private_state_invalid")
    if transaction.get("stage") not in STAGES or SHA64.fullmatch(str(transaction.get("transaction_ref", ""))) is None:
        raise WorkflowError("Private transaction stage/reference is invalid.", code="private_state_invalid")
    actual = transaction.get("transaction_sha256")
    expected = digest({key: value for key, value in transaction.items() if key != "transaction_sha256"})
    if actual != expected:
        raise WorkflowError("Private transaction digest is stale.", code="private_state_invalid")


def plan_from_input(root: Path, public_input: dict[str, Any]) -> dict[str, Any]:
    if public_input["profile"].removeprefix("delivery_") == "reprepare_publication":
        existing = unique_task_transaction(root, public_input["task_ref"], public_input.get("delivery_key"))
        ref = existing["transaction_ref"]
    else:
        ref = transaction_ref(public_input)
        existing = load_transaction(root, ref)
    if public_input["profile"].removeprefix("delivery_") in {"same_plan_resume", "reprepare_publication"}:
        if existing is None:
            raise WorkflowError("Requested publication transaction does not exist.", code="private_state_missing")
        validate_transaction(existing)
        source = existing["input"]
        if any(public_input.get(field) != source.get(field) for field in ("task_ref", "delivery_key")):
            raise WorkflowError("Resume the exact original Task/Delivery transaction.", code="private_state_invalid")
    else:
        source = public_input
        if existing is not None:
            try:
                validate_transaction(existing)
            except WorkflowError as exc:
                if exc.code == "private_state_invalid":
                    exc.payload["retire_transaction_ref"] = ref
                raise
            if existing.get("input") != source:
                raise WorkflowError("Publication transaction input drifted.", code="private_state_invalid")

    if source["profile"] in {"delivery_remote_draft_recovery", "delivery_remote_ready_recovery"}:
        from remote_recovery import plan
        return plan(root, source, existing, ref)
    if source["profile"] in {"delivery_draft_publish", "delivery_return_to_draft"}:
        from draft import plan
        return plan(root, source, existing, ref)

    if "delivery_key" in source and existing is not None and existing["stage"] == "ready":
        # Recover the original remote fact before requiring an active checkout
        # or current gate. The continuation decision is made separately below.
        return {"typed_exit": "historical_terminal", "output": ready_output(root, existing)}
    task_dir, task = task_context(root, source["task_ref"])
    selected = None
    if "delivery_key" in source:
        projection = DeliveryProjection(root, source["task_ref"])
        selected = projection.resolve(source["delivery_key"])
        terminal_recovery = existing is not None and existing["stage"] == "ready"
        if not terminal_recovery:
            readiness = selected["results"]["readiness"]
            if (readiness is None or readiness["result_id"] != source["readiness_result_id"]
                    or projection.gate_applicability(source["delivery_key"])["readiness"]["kind"] != "applicable"
                    or selected["candidate"]["head_ref"] != source["reviewed_head"]):
                return {"typed_exit":"review_stale","output":{"exit_id":"review_stale","task_ref":source["task_ref"],"delivery_key":source["delivery_key"],"stale_reason":"readiness_changed"}}

    if "delivery_key" in source and terminal_recovery:
        return {"typed_exit": "historical_terminal", "output": ready_output(root, existing)}
    reviewed_head = source["reviewed_head"]
    live_head = git_text(root, "rev-parse", "HEAD")
    if live_head != reviewed_head:
        return {"typed_exit": "review_stale", "output": {"exit_id": "review_stale", "task_ref": source["task_ref"], **({"delivery_key": source["delivery_key"]} if "delivery_key" in source else {}), "stale_reason": "reviewed_head_changed"}}
    repo_ref = repository_identity(root)
    branch = task["branch"]
    base = task["base_branch"]
    remote = remote_head(root, branch)
    candidates = list_open_prs(root, branch)
    same_repo = [normalize_pr(item) for item in candidates if same_repo_pr(item, repo_ref, branch, base)]
    foreign = [item for item in candidates if not same_repo_pr(item, repo_ref, branch, base)]
    if foreign:
        return blocked("foreign_or_mismatched_open_pr", "Close or retarget the fork-owned or mismatched Open PR before publishing this Delivery.")
    if len(same_repo) > 1:
        return blocked("multiple_open_prs", "Reduce the current head branch to one same-repository Open PR.")
    pr = same_repo[0] if same_repo else None
    if pr and pr["head_sha"] != reviewed_head and not is_ancestor(root, pr["head_sha"], reviewed_head):
        return blocked("pr_head_not_ancestor", "Re-review or repair the existing PR branch; its head is not the reviewed Delivery lineage.")
    if remote and remote != reviewed_head and not is_ancestor(root, remote, reviewed_head):
        return blocked("remote_head_not_ancestor", "Repair the remote branch lineage before publication.")
    if pr and remote != pr["head_sha"]:
        return blocked("remote_pr_head_mismatch", "Converge the remote branch and PR head before publication.")
    plan_identity = {
        "task_ref": source["task_ref"],
        **({"delivery_key": source["delivery_key"]} if "delivery_key" in source else {"delivery_cycle_ref": source["delivery_cycle_ref"]}),
        "repo_ref": repo_ref,
        "base_branch": base,
        "head_branch": branch,
        "reviewed_head": reviewed_head,
        "pr_title": source["pr_title"],
        "pr_body_sha256": hashlib.sha256(source["pr_body"].encode()).hexdigest(),
        "maximum_side_effects": ["push_content", "bind_pr", "converge_metadata", "mark_ready"],
    }
    return {
        "typed_exit": "preview",
        "task_dir": str(task_dir.relative_to(root)),
        "transaction_ref": ref,
        "transaction_stage": existing["stage"] if existing else "push_content",
        "confirmation_identity": digest(plan_identity),
        "plan_identity": plan_identity,
        "input": source,
        "public_candidate": selected["candidate"] if selected else None,
        "repo_ref": repo_ref,
        "base_branch": base,
        "head_branch": branch,
        "remote_head": remote,
        "candidate_pr": pr,
        "push_required": remote != reviewed_head,
        "create_pr_required": pr is None,
        "metadata_convergence_required": bool(pr and (pr["title"] != source["pr_title"] or pr["body"] != source["pr_body"])),
        "ready_transition_required": bool(pr and pr["is_draft"]),
        "terminal_recovery": bool(existing and existing["stage"] == "ready"),
    }


def blocked(reason_code: str, remediation: str) -> dict[str, Any]:
    return {"typed_exit": "blocked", "output": {"exit_id": "blocked", "reason_code": reason_code, "remediation": remediation}}


def expected_publication_exit(root, public):
    source = public
    if public["profile"] in {"delivery_same_plan_resume", "delivery_reprepare_publication"}:
        tx = (load_transaction(root, public["transaction_ref"]) if "transaction_ref" in public
              else unique_task_transaction(root, public["task_ref"], public.get("delivery_key")))
        if tx is None:
            raise WorkflowError("Recover the exact original publication transaction.", code="private_state_missing")
        source = tx["input"]
    return {"delivery_draft_publish": "draft_published", "delivery_remote_draft_recovery": "draft_published", "delivery_return_to_draft": "draft_revision_ready"}.get(source["profile"], "ready_for_merge")


def retire_completed(root, new_transaction):
    """Keep one same-operation recovery result per Delivery, not a journal."""
    directory = transaction_path(root, new_transaction["transaction_ref"]).parent
    for path in directory.glob("*.json") if directory.is_dir() else ():
        if path.name.endswith(".gate.json") or path.stem == new_transaction["transaction_ref"]:
            continue
        old = read_json(path)
        if old.get("input", {}).get("delivery_key") != new_transaction["input"].get("delivery_key"):
            continue
        validate_transaction(old)
        if old.get("base_ref") and new_transaction.get("base_ref") and old["base_ref"] != new_transaction["base_ref"]:
            raise WorkflowError("Retain the original Delivery content baseline for Draft updates.", code="publication_stale")
        if old["stage"] not in TERMINALS:
            raise WorkflowError("Recover the unfinished original publication action before a new action.", code="private_state_invalid")
        if old["terminal"] == "ready":
            ready_output(root, old)
        else:
            from draft import output
            output(root, old)
        path.unlink()
        path.with_suffix(".gate.json").unlink(missing_ok=True)


def initial_transaction(context: dict[str, Any]) -> dict[str, Any]:
    candidate = context.get("candidate_pr")
    return {
        "schema_version": "2.0",
        "skill_id": SKILL_ID,
        "transaction_ref": context["transaction_ref"],
        "action": "ready",
        "terminal": "ready",
        "stage": "push_content",
        "input": context["input"],
        "public_candidate": context.get("public_candidate"),
        "repo_ref": context["repo_ref"],
        "base_branch": context["base_branch"],
        "head_branch": context["head_branch"],
        "reviewed_head": context["input"]["reviewed_head"],
        "initial_remote_head": context["remote_head"],
        "candidate_pr": candidate,
        "bound_pr": None,
        "decisions": {
            "push_required": context["push_required"],
            "create_pr_required": context["create_pr_required"],
            "metadata": None,
            "ready": None,
        },
    }


def exact_context(root: Path, transaction: dict[str, Any]) -> dict[str, Any]:
    validate_transaction(transaction)
    context = plan_from_input(root, transaction["input"])
    if context.get("typed_exit") != "preview":
        raise WorkflowError("Publication transaction no longer has a current reviewed plan.", code="publication_stale")
    for field in ("repo_ref", "base_branch", "head_branch"):
        if context[field] != transaction[field]:
            raise WorkflowError(f"Publication {field} changed.", code="publication_stale")
    return context


def persist_binding_decisions(root: Path, transaction: dict[str, Any], pr: dict[str, Any]) -> None:
    source = transaction["input"]
    metadata = {
        "original_title": pr["title"],
        "original_body_sha256": hashlib.sha256(str(pr["body"]).encode()).hexdigest(),
        "title_matches": pr["title"] == source["pr_title"],
        "body_matches": pr["body"] == source["pr_body"],
        "mutation_required": pr["title"] != source["pr_title"] or pr["body"] != source["pr_body"],
    }
    transaction["bound_pr"] = {"number": pr["number"], "url": pr["url"], "head_sha": pr["head_sha"]}
    transaction["decisions"]["metadata"] = metadata
    transaction["decisions"]["ready"] = {"original_is_draft": pr["is_draft"], "mutation_required": pr["is_draft"]}
    transaction["stage"] = "converge_metadata"
    save_transaction(root, transaction)


def find_bindable_pr(root: Path, transaction: dict[str, Any]) -> dict[str, Any] | None:
    if "existing_pr_number" in transaction:
        pr = read_pr(root, transaction["existing_pr_number"])
        raw = {"state": pr["state"], "headRefName": pr["head_branch"], "baseRefName": pr["base_branch"],
               "url": pr["url"], "headRepositoryOwner": pr["head_owner"]}
        if not same_repo_pr(raw, transaction["repo_ref"], transaction["head_branch"], transaction["base_branch"]):
            raise WorkflowError("The exact recovery PR changed repository, target or remote ref.", code="pr_identity_stale")
        return pr
    candidates = list_open_prs(root, transaction["head_branch"])
    same_repo = [normalize_pr(item) for item in candidates if same_repo_pr(item, transaction["repo_ref"], transaction["head_branch"], transaction["base_branch"])]
    if len(candidates) != len(same_repo):
        raise WorkflowError("A fork-owned or mismatched PR exists for the Delivery branch.", code="pr_identity_stale")
    if len(same_repo) > 1:
        raise WorkflowError("Multiple Open PRs exist for the Delivery branch.", code="pr_identity_stale")
    return same_repo[0] if same_repo else None


def push_content(root: Path, transaction: dict[str, Any]) -> None:
    remote = remote_head(root, transaction["head_branch"])
    head = transaction["reviewed_head"]
    if remote == head:
        transaction["stage"] = "bind_pr"
        save_transaction(root, transaction)
        return
    if remote != transaction["initial_remote_head"]:
        raise WorkflowError("Remote HEAD differs from this action's original preimage/postimage.", code="publication_stale")
    if transaction["terminal"] == "draft":
        current_pr = find_bindable_pr(root, transaction)
        if current_pr is not None and not current_pr["is_draft"]:
            raise WorkflowError("Confirm this same PR is Draft before pushing unreviewed content.", code="publication_stale")
    if remote and not is_ancestor(root, remote, head):
        raise WorkflowError("Remote branch is not a reviewed ancestor.", code="publication_stale")
    _run(root, ["git", "push", "origin", f"{head}:refs/heads/{transaction['head_branch']}"])
    if remote_head(root, transaction["head_branch"]) != head:
        raise WorkflowError("Publication push did not converge to the reviewed head.", code="external_command_failed")
    transaction["stage"] = "bind_pr"
    save_transaction(root, transaction)


def bind_pr(root: Path, transaction: dict[str, Any]) -> None:
    head = transaction["reviewed_head"]
    pr = find_bindable_pr(root, transaction)
    if pr is not None:
        if pr["head_sha"] != head:
            raise WorkflowError("Open PR head does not equal the pushed reviewed head.", code="pr_identity_stale")
        persist_binding_decisions(root, transaction, pr)
        return
    if "existing_pr_number" in transaction:
        raise WorkflowError("The explicit recovery PR is unavailable; do not create another PR.", code="pr_identity_stale")
    transaction["decisions"]["create_pr_required"] = True
    save_transaction(root, transaction)
    source = transaction["input"]
    completed = _run(
        root,
        ["gh", "pr", "create", "--repo", transaction["repo_ref"], "--draft", "--base", transaction["base_branch"], "--head", transaction["head_branch"], "--title", source["pr_title"], "--body", source["pr_body"]],
        allow_failure=True,
    )
    pr = find_bindable_pr(root, transaction)
    if pr is None:
        raise WorkflowError(
            "PR creation did not yield one recoverable Open PR.",
            code="external_command_failed",
            payload={"stderr": completed.stderr.strip()},
        )
    if pr["head_sha"] != head:
        raise WorkflowError("Created PR is not at the reviewed head.", code="pr_identity_stale")
    persist_binding_decisions(root, transaction, pr)


def converge_metadata(root: Path, transaction: dict[str, Any]) -> None:
    bound = transaction.get("bound_pr")
    decision = transaction["decisions"].get("metadata")
    if not isinstance(bound, dict) or not isinstance(decision, dict):
        raise WorkflowError("PR binding decision is missing.", code="private_state_invalid")
    pr = read_pr(root, bound["number"])
    source = transaction["input"]
    if pr["head_sha"] != transaction["reviewed_head"] or pr["state"] != "OPEN":
        raise WorkflowError("Bound PR identity drifted before metadata convergence.", code="pr_identity_stale")
    desired = pr["title"] == source["pr_title"] and pr["body"] == source["pr_body"]
    original = pr["title"] == decision["original_title"] and hashlib.sha256(str(pr["body"]).encode()).hexdigest() == decision["original_body_sha256"]
    if not desired:
        if not decision["mutation_required"] or not original:
            raise WorkflowError("Bound PR metadata drifted outside the recorded convergence decision.", code="pr_identity_stale")
        _run(root, ["gh", "pr", "edit", str(pr["number"]), "--repo", transaction["repo_ref"], "--title", source["pr_title"], "--body", source["pr_body"]], allow_failure=True)
        pr = read_pr(root, bound["number"])
        if pr["title"] != source["pr_title"] or pr["body"] != source["pr_body"]:
            raise WorkflowError("PR metadata mutation did not converge.", code="external_command_failed")
    transaction["stage"] = "draft" if transaction["terminal"] == "draft" else "mark_ready"
    save_transaction(root, transaction)


def mark_ready(root: Path, transaction: dict[str, Any]) -> None:
    bound = transaction.get("bound_pr")
    decision = transaction["decisions"].get("ready")
    if not isinstance(bound, dict) or not isinstance(decision, dict):
        raise WorkflowError("Ready decision is missing.", code="private_state_invalid")
    pr = read_pr(root, bound["number"])
    if pr["head_sha"] != transaction["reviewed_head"] or pr["state"] != "OPEN":
        raise WorkflowError("Bound PR identity drifted before Ready transition.", code="pr_identity_stale")
    if pr["is_draft"]:
        if not decision["mutation_required"] or decision["original_is_draft"] is not True:
            raise WorkflowError("Draft state drifted outside the recorded Ready decision.", code="pr_identity_stale")
        _run(root, ["gh", "pr", "ready", str(pr["number"]), "--repo", transaction["repo_ref"]], allow_failure=True)
        pr = read_pr(root, bound["number"])
        if pr["is_draft"]:
            raise WorkflowError("Ready mutation did not converge.", code="external_command_failed")
    transaction["stage"] = "ready"
    save_transaction(root, transaction)


def ready_output(root: Path, transaction: dict[str, Any]) -> dict[str, Any]:
    bound = transaction.get("bound_pr")
    if not isinstance(bound, dict):
        raise WorkflowError("Ready transaction is missing its PR binding.", code="private_state_invalid")
    pr = read_pr(root, bound["number"])
    source = transaction["input"]
    if (
        pr["state"] not in {"OPEN", "MERGED"}
        or pr["is_draft"]
        or pr["head_sha"] != transaction["reviewed_head"]
        or pr["title"] != source["pr_title"]
        or pr["body"] != source["pr_body"]
    ):
        raise WorkflowError("Ready publication terminal facts drifted.", code="publication_stale")
    if "delivery_key" in source:
        projection = DeliveryProjection(root, source["task_ref"])
        selected = projection.resolve(source["delivery_key"])
        candidate = transaction["public_candidate"]
        original_publication = transaction.get("public_publication")
        result_id = original_publication["result_id"] if original_publication else "publication:" + transaction["transaction_ref"]
        owner_id = projection.declaration()["owners"]["publication"]
        pr_ref = {"locator": f"https://github.com/{transaction['repo_ref']}/pull/{pr['number']}", "revision": "sha256:" + hashlib.sha256(pr["body"].encode("utf-8")).hexdigest()}
        fact = {"result_id": result_id, "owner_id": owner_id, "evidence": [pr_ref], "profile": "pull_request",
                "candidate": candidate, "repo_ref": transaction["repo_ref"], "pr_number": pr["number"],
                "reviewed_head": transaction["reviewed_head"], "target_ref": transaction["base_branch"], "publication_ref": pr_ref}
        if original_publication is not None:
            fact = original_publication
        try:
            projection.apply({"api_version":"1.0", "operation":"record_publication", "key":source["delivery_key"],
                "owner_role":"publication", "owner_id":owner_id, "expected_phase":selected["phase"], "result":fact,
                "historical_success":True})
        except LifecycleContractError as exc:
            raise WorkflowError(str(exc), code="external_command_failed") from exc
        current = projection.resolve(source["delivery_key"])
        readiness = current["results"]["readiness"]
        if (pr["state"] == "MERGED" or (source["profile"] != "delivery_remote_ready_recovery" and git_text(root, "rev-parse", "HEAD") != source["reviewed_head"])
                or readiness is None or readiness["result_id"] != source["readiness_result_id"]
                or projection.gate_applicability(source["delivery_key"])["readiness"]["kind"] != "applicable"):
            return {"exit_id":"review_stale", "task_ref":source["task_ref"], "delivery_key":source["delivery_key"], "stale_reason":"historical_success_current_readiness_changed"}
        return {"exit_id":"ready_for_merge", "task_ref":source["task_ref"], "delivery_key":source["delivery_key"],
                "repo_ref":transaction["repo_ref"], "pr_number":pr["number"], "expected_head_sha":transaction["reviewed_head"],
                "publication_body_sha256":hashlib.sha256(source["pr_body"].encode()).hexdigest(), "publication_result_id":result_id}
    return {
        "exit_id": "ready_for_merge",
        "task_ref": source["task_ref"],
        **({"delivery_key": source["delivery_key"]} if "delivery_key" in source else {"delivery_cycle_ref": source["delivery_cycle_ref"]}),
        "repo_ref": transaction["repo_ref"],
        "pr_number": pr["number"],
        "expected_head_sha": transaction["reviewed_head"],
        "publication_body_sha256": hashlib.sha256(source["pr_body"].encode()).hexdigest(),
    }


def execute(root: Path, context: dict[str, Any]) -> dict[str, Any]:
    transaction = load_transaction(root, context["transaction_ref"])
    if transaction is None:
        if context["input"]["profile"] in {"delivery_remote_draft_recovery", "delivery_remote_ready_recovery"}:
            from remote_recovery import initial
            transaction = initial(context)
        elif context["input"]["profile"] in {"delivery_draft_publish", "delivery_return_to_draft"}:
            from draft import initial
            transaction = initial(context)
        else:
            transaction = initial_transaction(context)
        retire_completed(root, transaction)
        save_transaction(root, transaction)
    validate_transaction(transaction)
    exact_context(root, transaction)
    while True:
        stage = transaction["stage"]
        if stage == "ensure_draft":
            from draft import ensure_draft
            ensure_draft(root, transaction)
        elif stage == "push_content":
            push_content(root, transaction)
        elif stage == "bind_pr":
            bind_pr(root, transaction)
        elif stage == "converge_metadata":
            converge_metadata(root, transaction)
        elif stage == "mark_ready":
            mark_ready(root, transaction)
        elif stage == "ready":
            return ready_output(root, transaction)
        elif stage in {"draft", "draft_revision"}:
            from draft import output
            return output(root, transaction)
        transaction = load_transaction(root, context["transaction_ref"])
        if transaction is None:
            raise WorkflowError("Publication transaction disappeared.", code="private_state_missing")


def record_gate(root: Path, context: dict[str, Any], review: dict[str, Any]) -> Path:
    gate = {
        "schema_version": "1.0",
        "skill_id": SKILL_ID,
        "transaction_ref": context["transaction_ref"],
        "confirmation_identity": context["confirmation_identity"],
        "review": review["review"],
        "route": review["route"],
    }
    gate["gate_sha256"] = digest(gate)
    path = transaction_path(root, context["transaction_ref"]).with_suffix(".gate.json")
    write_json(path, gate)
    return path


def check_gate(root: Path, context: dict[str, Any], gate_path: Path) -> dict[str, Any]:
    gate = read_json(gate_path)
    actual = gate.pop("gate_sha256", None)
    if actual != digest(gate):
        raise WorkflowError("Publication semantic gate digest is stale.", code="private_state_invalid")
    if gate.get("transaction_ref") != context["transaction_ref"] or gate.get("confirmation_identity") != context["confirmation_identity"]:
        raise WorkflowError("Publication semantic gate no longer matches the live plan.", code="publication_stale")
    gate["gate_sha256"] = actual
    return gate


def preview(root: Path, input_path: str) -> dict[str, Any]:
    public_input = validate_public_input(read_json(input_path))
    return plan_from_input(root, public_input)


def project_review_stale(root: Path, output: dict[str, Any]) -> dict[str, Any]:
    if output.get("exit_id") != "review_stale" or "delivery_key" not in output:
        return output
    projection = DeliveryProjection(root, output["task_ref"])
    selected = projection.resolve(output["delivery_key"])
    # Publication owns this fixed backward transition. A changed candidate or
    # missing earlier gate still returns the real gap; no phase produces pass.
    if selected["phase"] == "publishing" and projection.gate_applicability(output["delivery_key"])["full_review"]["kind"] == "applicable":
        from runtime.delivery_projection.adapter import authority_ref
        from runtime.delivery_projection.gates import rework
        reason = authority_ref(projection.planning_directory(output["delivery_key"]) / "implement.md", root)
        rework(projection, output["delivery_key"], "publication", "readiness", reason, ["readiness"])
    return output


def invoke(root: Path, input_path: str, review_path: str, confirmed: str | None) -> dict[str, Any]:
    public_input = validate_public_input(read_json(input_path))
    review_input = read_json(review_path)
    try:
        context = plan_from_input(root, public_input)
    except WorkflowError as exc:
        if exc.code in {"private_state_invalid", "private_state_missing"}:
            if (
                public_input["profile"].removeprefix("delivery_") == "review_ready"
                and exc.payload.get("retire_transaction_ref") == transaction_ref(public_input)
            ):
                transaction_path(root, exc.payload["retire_transaction_ref"]).unlink(missing_ok=True)
            return project_review_stale(root, {"exit_id": "review_stale", "task_ref": public_input["task_ref"], **({"delivery_key":public_input["delivery_key"]} if "delivery_key" in public_input else {}), "stale_reason": exc.code})
        if exc.code in REPREPARE_REQUIRED_CODES:
            return {"exit_id": "reprepare_required", "task_ref": public_input["task_ref"], **({"delivery_key":public_input["delivery_key"]} if "delivery_key" in public_input else {}), "reason_code": exc.code}
        raise
    review = validate_review(review_input, expected_publication_exit(root, public_input))
    if context.get("typed_exit") != "preview":
        return project_review_stale(root, context["output"])
    if not context["terminal_recovery"]:
        if not isinstance(confirmed, str) or confirmed != context["confirmation_identity"]:
            return blocked("confirmation_identity_mismatch", "Preview and confirm the current publication plan before mutation.")["output"]
    gate_path = record_gate(root, context, review)
    check_gate(root, context, gate_path)
    try:
        return execute(root, context)
    except WorkflowError as exc:
        transaction = load_transaction(root, context["transaction_ref"])
        if transaction is not None and exc.code in {"external_command_failed"}:
            return {"exit_id": "resume_publication", "task_ref": context["input"]["task_ref"], **({"delivery_key":context["input"]["delivery_key"]} if "delivery_key" in context["input"] else {}), "transaction_ref": context["transaction_ref"]}
        if exc.code in REPREPARE_REQUIRED_CODES:
            return {"exit_id": "reprepare_required", "task_ref": context["input"]["task_ref"], **({"delivery_key":context["input"]["delivery_key"]} if "delivery_key" in context["input"] else {}), "reason_code": exc.code}
        raise


def parser(kind: str) -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--root")
    value.add_argument("--input", required=True)
    if kind in {"record", "invoke"}:
        value.add_argument("--review-input", required=True)
    if kind == "invoke":
        value.add_argument("--confirmed-preview-sha256")
    if kind in {"check", "execute"}:
        value.add_argument("--gate", required=True)
    return value
