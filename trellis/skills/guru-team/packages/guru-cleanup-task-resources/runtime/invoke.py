from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.handoff_cleanup import read_handoff_cleanup_inventory
from runtime.task_lifecycle.identity import resolve_task_id
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


ORDER = {"linked_worktree": 0, "local_branch": 1, "remote_branch": 2}


def load(root: Path, package: Path, value: str, field: str) -> dict[str, Any]:
    path = Path(value)
    choices = [path] if path.is_absolute() else [root / path, package / path]
    source = next((candidate for candidate in choices if candidate.is_file() and not candidate.is_symlink()), None)
    if source is None:
        raise CommandError("invalid_json", field, "Provide one regular JSON file.")
    try:
        payload = json.loads(source.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("invalid_json", field, "Provide valid JSON.") from exc
    if not isinstance(payload, dict):
        raise CommandError("invalid_json", field, "Provide one object.")
    return payload


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)
    if check and proc.returncode:
        raise CommandError("stale_identity", "resource", proc.stderr.strip() or "Refresh live Git resources.", 3)
    return proc


def blocked(code: str, ref: str) -> dict[str, Any]:
    return {"exit_id": "blocked", "reason_code": code, "reason_refs": [ref]}


def pending(public: dict[str, Any], code: str) -> dict[str, Any]:
    return {
        "exit_id": "remaining_resources",
        "task_id": public["task_id"],
        "lifecycle_generation": public["lifecycle_generation"],
        "finish_result_id": public["finish_result_id"],
        "reason_code": code,
        "reason_refs": [public["task_id"]],
    }


def manual_required(public: dict[str, Any], candidates: list[dict[str, Any]]) -> dict[str, Any]:
    return {"exit_id": "manual_cleanup_required", "task_id": public["task_id"],
            "lifecycle_generation": public["lifecycle_generation"],
            "finish_result_id": public["finish_result_id"], "candidates": candidates}


def worktrees(root: Path) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in git(root, "worktree", "list", "--porcelain").stdout.splitlines() + [""]:
        if not line:
            if "worktree" in current:
                result.append(current)
            current = {}
        else:
            key, _, value = line.partition(" ")
            current[key] = value
    return result


def remote_matches(root: Path, ref: dict[str, str]) -> bool:
    url = git(root, "remote", "get-url", ref["remote_name"]).stdout.strip()
    match = re.search(r"(?:github\.com[:/])([^/]+/[^/]+?)(?:\.git)?$", url)
    return match is not None and match.group(1).lower() == ref["repository_ref"].lower()


def discover_candidates(root: Path) -> dict[str, tuple[dict[str, Any], dict[str, Any]]]:
    repository = inspect_repository(root)
    registered = worktrees(root)
    result: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}

    def add(kind: str, branch_ref: str, portable_ref: dict[str, str], head: str,
            checkout_path: str | None = None) -> None:
        identity = {"repository": str(repository.common_dir), "kind": kind,
                    "portable_ref": portable_ref, "head": head, "checkout_path": checkout_path}
        candidate_id = "cleanup-candidate:" + hashlib.sha256(
            json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()[:32]
        dto = {"candidate_id": candidate_id, "kind": kind,
               "branch_name": branch_ref.removeprefix("refs/heads/"),
               "registered_worktree_state": "registered" if checkout_path or any(
                   row.get("branch") == branch_ref for row in registered) else "not_registered",
               "remote_identity": portable_ref.get("repository_ref"), "live_head": head}
        if kind == "remote_branch":
            dto["remote_name"] = portable_ref["remote_name"]
        if checkout_path:
            dto["checkout_path"] = checkout_path
        item = {"resource_id": candidate_id, "kind": kind,
                "portable_ref": portable_ref, "expected_cleanup_head": head}
        result[candidate_id] = (dto, item)

    for row in registered:
        branch_ref = row.get("branch")
        if branch_ref and row.get("HEAD"):
            add("linked_worktree", branch_ref,
                {"kind": "linked_worktree", "branch_ref": branch_ref},
                row["HEAD"], row["worktree"])
    for line in git(root, "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads").stdout.splitlines():
        branch_ref, head = line.split()
        add("local_branch", branch_ref, {"kind": "local_branch", "ref": branch_ref}, head)
    for remote_name in git(root, "remote").stdout.splitlines():
        url = git(root, "remote", "get-url", remote_name).stdout.strip()
        match = re.search(r"(?:github\.com[:/])([^/]+/[^/]+?)(?:\.git)?$", url)
        if match is None:
            continue
        repository_ref = match.group(1)
        for line in git(root, "ls-remote", "--heads", remote_name).stdout.splitlines():
            head, branch_ref = line.split()
            add("remote_branch", branch_ref,
                {"kind": "remote_branch", "remote_name": remote_name,
                 "repository_ref": repository_ref, "ref": branch_ref}, head)
    return result


def inspect_resource(root: Path, item: dict[str, Any], scheduled_worktree_refs: frozenset[str] = frozenset()) -> tuple[bool, str | None]:
    kind, ref = item["kind"], item["portable_ref"]
    expected = item["expected_cleanup_head"]
    if kind == "linked_worktree":
        matches = [row for row in worktrees(root) if row.get("branch") == ref["branch_ref"]]
        if len(matches) > 1:
            return False, "worktree_ambiguous"
        if not matches:
            return False, None
        path = Path(matches[0]["worktree"]).resolve()
        if path == root.resolve() or git(path, "rev-parse", "HEAD").stdout.strip() != expected:
            return False, "worktree_identity_changed"
        if git(path, "status", "--porcelain=v1", "--untracked-files=all").stdout:
            return False, "worktree_dirty"
        return True, None
    if kind == "local_branch":
        result = git(root, "show-ref", "--verify", ref["ref"], check=False)
        if result.returncode:
            return False, None
        if git(root, "rev-parse", ref["ref"]).stdout.strip() != expected:
            return False, "branch_head_changed"
        if ref["ref"] not in scheduled_worktree_refs and any(row.get("branch") == ref["ref"] for row in worktrees(root)):
            return False, "branch_checked_out"
        return True, None
    if not remote_matches(root, ref):
        return False, "remote_repository_changed"
    rows = git(root, "ls-remote", "--heads", ref["remote_name"], ref["ref"]).stdout.splitlines()
    if not rows:
        return False, None
    if len(rows) != 1 or rows[0].split() != [expected, ref["ref"]]:
        return False, "remote_head_changed"
    return True, None


def remove_resource(root: Path, item: dict[str, Any]) -> bool:
    kind, ref = item["kind"], item["portable_ref"]
    if kind == "linked_worktree":
        rows = [row for row in worktrees(root) if row.get("branch") == ref["branch_ref"]]
        return not rows or git(root, "worktree", "remove", rows[0]["worktree"], check=False).returncode == 0
    if kind == "local_branch":
        return git(root, "update-ref", "-d", ref["ref"], item["expected_cleanup_head"], check=False).returncode == 0
    return git(root, "push", "--force-with-lease=" + ref["ref"] + ":" + item["expected_cleanup_head"], ref["remote_name"], ":" + ref["ref"], check=False).returncode == 0


def cleaned(public: dict[str, Any], inventory_id: str) -> dict[str, Any]:
    identity = {"task_id": public["task_id"], "lifecycle_generation": public["lifecycle_generation"], "finish_result_id": public["finish_result_id"], "inventory_id": inventory_id}
    suffix = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:24]
    return {"exit_id": "cleaned", "task_id": public["task_id"], "lifecycle_generation": public["lifecycle_generation"], "cleanup_result_id": "cleanup-result:" + suffix}


def manual_receipt(store: ResourceLedgerStore, public: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    identity = {field: public[field] for field in ("task_id", "lifecycle_generation", "finish_result_id", "selected_candidate_ids")}
    digest = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:32]
    path = store.repository.common_dir / "guru-team" / "cleanup-results" / public["task_id"] / f'selected-{digest}.json'
    return path, identity


def normal_receipt(store: ResourceLedgerStore, public: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    identity = {field: public[field] for field in ("task_id", "lifecycle_generation", "finish_result_id", "inventory_id")}
    digest = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:32]
    path = store.repository.common_dir / "guru-team" / "cleanup-results" / public["task_id"] / f'normal-{digest}.json'
    return path, identity


def manual_targets_current(store: ResourceLedgerStore, resources: list[dict[str, Any]]) -> bool:
    selected = {(row["kind"], json.dumps(row["portable_ref"], sort_keys=True)) for row in resources}
    for ledger in store.iter_ledgers():
        for row in ledger.resources:
            if row.state == "current" and (row.kind, json.dumps(row.portable_ref, sort_keys=True)) in selected:
                return True
    for binding in BranchBindingStore(store.repository).iter_bindings():
        if any(row["portable_ref"].get("ref", row["portable_ref"].get("branch_ref")) == binding.branch_ref for row in resources):
            return True
    selected_branches = {row["portable_ref"].get("ref", row["portable_ref"].get("branch_ref"))
                         for row in resources if row["kind"] in {"local_branch", "linked_worktree"}}
    local_branches = git(store.repository.context_path, "for-each-ref", "--format=%(refname)", "refs/heads").stdout.splitlines()
    retained = [branch for branch in local_branches if branch not in selected_branches]
    for branch in selected_branches:
        if branch not in local_branches:
            continue
        active_artifacts = [path for path in git(store.repository.context_path, "ls-tree", "-r", "--name-only",
                                                branch, "--", ".trellis/tasks").stdout.splitlines()
                            if re.fullmatch(r"\.trellis/tasks/[^/]+/task\.json", path)]
        if any(not any(
            git(store.repository.context_path, "merge-base", "--is-ancestor", branch, survivor,
                check=False).returncode == 0
            and git(store.repository.context_path, "cat-file", "-e", f"{survivor}:{path}",
                    check=False).returncode == 0
            for survivor in retained
        ) for path in active_artifacts):
            return True
    return False


def require_manual_finish_result(store: ResourceLedgerStore, package_root: Path, key: TaskLifecycleKey,
                                 finish_result_id: str, archive_ref: str) -> dict[str, Any]:
    path = (store.repository.common_dir / "guru-team" / "finish-results" /
            key.task_id / f"{key.lifecycle_generation}-manual.json")
    if not path.is_file() or path.is_symlink():
        raise LifecycleContractError("manual_finish_result_missing", "finish_result_id", "Recover the exact terminal Finish result before selecting resources.")
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
        validate_json(result, package_root.parent / "guru-finish-task/schemas/manual-finish-result.schema.json", "manual_finish_result")
    except (OSError, json.JSONDecodeError, CommandError) as exc:
        raise LifecycleContractError("manual_finish_result_stale", "finish_result_id", "Recover a valid terminal Finish result.") from exc
    if any(result[field] != value for field, value in {
        "task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation,
        "finish_result_id": finish_result_id, "archive_ref": archive_ref,
    }.items()):
        raise LifecycleContractError("manual_finish_result_stale", "finish_result_id", "Select the current archived Finish result.")
    return result


def require_missing_terminal(store: ResourceLedgerStore, package_root: Path,
                             key: TaskLifecycleKey, finish_result_id: str, root: Path) -> dict[str, Any]:
    task = resolve_task_id(root, key.task_id)
    if task.lifecycle_state != "archived" or task.lifecycle_generation != key.lifecycle_generation:
        raise LifecycleContractError("archived_lifecycle_stale", "task", "Select a normally finished archived lifecycle.")
    return require_manual_finish_result(store, package_root, key, finish_result_id, task.task_ref)


def handoff_cleanup(root: Path, public: dict[str, Any], *, confirmed: bool) -> dict[str, Any]:
    repository = inspect_repository(root)
    reference = public["handoff_inventory"]
    if (reference["task_id"], reference["lifecycle_generation"]) != (public["task_id"], public["lifecycle_generation"]):
        return blocked("handoff_inventory_stale", reference["inventory_id"])
    receipt = (repository.common_dir / "guru-team" / "handoff-cleanup-results" /
               reference["task_id"] / str(reference["lifecycle_generation"]) / f'{reference["handoff_id"]}.json')
    if receipt.is_file():
        recorded = json.loads(receipt.read_text(encoding="utf-8"))
        if recorded.get("inventory_ref") != reference:
            return blocked("handoff_inventory_stale", reference["inventory_id"])
        return recorded["output"]
    try:
        inventory = read_handoff_cleanup_inventory(repository, reference)
    except LifecycleContractError as exc:
        return blocked(exc.code, exc.field_path)
    resources = inventory["resources"]
    handoff = inventory["handoff_ref"]
    result_id = "cleanup-result:" + hashlib.sha256(
        json.dumps(reference, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:24]
    result = {"task_id": reference["task_id"], "lifecycle_generation": reference["lifecycle_generation"],
              "cleanup_result_id": result_id}
    def remaining(code: str) -> dict[str, Any]:
        return {"exit_id": "handoff_cleanup_remaining", "task_id": reference["task_id"],
                "lifecycle_generation": reference["lifecycle_generation"], "handoff_inventory": reference,
                "handoff_ref": handoff,
                "cleanup_result": result, "reason": {"reason_code": code, "reason_refs": [reference["inventory_id"]]}}
    scheduled = frozenset(row["portable_ref"]["branch_ref"] for row in resources if row["kind"] == "linked_worktree")
    conflicts = [code for row in resources for _present, code in [inspect_resource(root, row, scheduled)] if code]
    if conflicts:
        return blocked(conflicts[0], reference["inventory_id"])
    if not confirmed:
        return remaining("confirmation_required")
    for row in sorted(resources, key=lambda item: ORDER[item["kind"]]):
        present, code = inspect_resource(root, row)
        if code:
            return blocked(code, row["resource_id"])
        if present and not remove_resource(root, row):
            return remaining("deletion_incomplete")
    if any(inspect_resource(root, row)[0] for row in resources):
        return remaining("deletion_incomplete")
    try:
        ResourceLedgerStore(repository).resolve_handoff_cleanup(
            TaskLifecycleKey(reference["task_id"], reference["lifecycle_generation"]),
            resource_ids=[row["resource_id"] for row in resources],
        )
    except LifecycleContractError as exc:
        return blocked(exc.code, exc.field_path)
    output = {"exit_id": "handoff_cleanup_complete", "handoff_ref": handoff, "cleanup_result": result}
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps({"inventory_ref": reference, "output": output}, sort_keys=True) + "\n", encoding="utf-8")
    return output


def run(package_root: Path, command: dict, argv: list[str]) -> dict[str, Any]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    parser.add_argument("--confirmed-cleanup", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the cleanup command contract.") from exc
    root = Path(args.root or ".").resolve()
    public = load(root, package_root, args.input, "input")
    semantic = load(root, package_root, args.semantic_result, "semantic_result")
    validate_json(public, package_root / "schemas/public-input.schema.json", "input")
    validate_json(semantic, package_root / "schemas/semantic-result.schema.json", "semantic_result")
    if (public["profile"], public["mode"]) != (semantic["profile"], semantic["mode"]):
        raise CommandError("stale_identity", "semantic_result", "Cleanup profile and mode differ.", 3)
    route = semantic["route"]["typed_exit"]
    allowed_routes = {
        "normal": {"cleaned", "remaining_resources", "blocked"},
        "select_explicit_cleanup_targets": {"cleaned", "manual_cleanup_required", "blocked"},
        "machine_handoff": {"handoff_cleanup_complete", "handoff_cleanup_remaining", "blocked"},
    }
    if route not in allowed_routes[public["profile"]]:
        raise CommandError("schema_mismatch", "semantic_result.route.typed_exit", "Select an exit for this cleanup profile.")
    if route == "blocked":
        out = blocked(semantic["route"]["reason_code"], public["task_id"])
    elif public["profile"] == "machine_handoff":
        out = handoff_cleanup(root, public, confirmed=args.confirmed_cleanup and route == "handoff_cleanup_complete")
    else:
        store = ResourceLedgerStore(inspect_repository(root))
        key = TaskLifecycleKey(public["task_id"], public["lifecycle_generation"])
        try:
            if public["profile"] == "normal":
                receipt_path, receipt_identity = normal_receipt(store, public)
                ledger = store.read(key)
                if ledger is not None and ledger.finish_result_id != public["finish_result_id"]:
                    raise LifecycleContractError("resource_ledger_conflict", "finish_result_id", "Recover only the exact sealed Finish result.")
                if receipt_path.is_file():
                    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                    if receipt.get("identity") != receipt_identity:
                        raise LifecycleContractError("resource_inventory_stale", "normal_receipt", "Recover the exact sealed Cleanup result.")
                    out = receipt["output"]
                    resources = []
                else:
                    resolution = store.cleanup_resolution(key, finish_result_id=public["finish_result_id"], inventory_id=public["inventory_id"])
                    if resolution.resolution_kind == "manual_selection_required":
                        require_missing_terminal(store, package_root, key, public["finish_result_id"], root)
                        out = manual_required(public, [dto for dto, _item in discover_candidates(root).values()])
                        resources = []
                    else:
                        resources = [item.as_dict() for item in resolution.resources]
                        out = {}
            else:
                ledger = store.read(key)
                if ledger is not None and ledger.finish_result_id != public["finish_result_id"]:
                    raise LifecycleContractError("resource_ledger_conflict", "finish_result_id", "Select the current Finish result.")
                out = {}
                receipt_path, receipt_identity = manual_receipt(store, public)
                if receipt_path.is_file():
                    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                    if receipt.get("identity") != receipt_identity:
                        raise LifecycleContractError("resource_inventory_stale", "manual_receipt", "Recover the exact selected cleanup result.")
                    out = receipt["output"]
                    resources = []
                    candidates = {}
                else:
                    candidates = discover_candidates(root)
                    selected = public["selected_candidate_ids"]
                    resources = [candidates[candidate_id][1] for candidate_id in selected if candidate_id in candidates]
                    if not selected:
                        terminal = None
                        if ledger is None:
                            terminal = require_missing_terminal(store, package_root, key, public["finish_result_id"], root)
                        head_branch = terminal.get("head_branch") if terminal else None
                        branch_still_present = any(dto["branch_name"] == head_branch for dto, _item in candidates.values())
                        if ledger is not None or not head_branch or branch_still_present or not args.confirmed_cleanup or route != "cleaned":
                            out = manual_required(public, [dto for dto, _item in candidates.values()])
                    elif len(resources) != len(selected):
                        out = blocked("cleanup_candidate_stale", "selected_candidate_ids")
                    elif ledger is None:
                        require_missing_terminal(store, package_root, key, public["finish_result_id"], root)
                if ledger is not None:
                    eligible = {(row.kind, json.dumps(row.portable_ref, sort_keys=True)): row for row in ledger.resources if row.ownership == "caller_owned" and row.state == "retained" and row.responsibility_role == "manual_only"}
                    if not out and any(
                        (item["kind"], json.dumps(item["portable_ref"], sort_keys=True)) not in eligible
                        for item in resources
                    ):
                        raise LifecycleContractError("resource_ownership_conflict", "selected_candidate_ids", "Select only exact caller-owned retired resources.")
                if not out and manual_targets_current(store, resources):
                    raise LifecycleContractError("resource_in_current_use", "selected_candidate_ids", "Do not delete any active task's current resource.")
        except LifecycleContractError as exc:
            out = blocked(exc.code, exc.field_path)
            resources = []
        if not out:
            scheduled_worktree_refs = frozenset(item["portable_ref"]["branch_ref"] for item in resources if item["kind"] == "linked_worktree")
            conflicts = [code for item in resources for present, code in [inspect_resource(root, item, scheduled_worktree_refs)] if code]
            if conflicts:
                out = blocked(conflicts[0], public["task_id"])
            elif route in {"remaining_resources", "manual_cleanup_required"} or (resources and not args.confirmed_cleanup):
                out = (manual_required(public, [dto for dto, _item in candidates.values()])
                       if public["profile"] == "select_explicit_cleanup_targets"
                       else pending(public, "confirmation_required"))
            else:
                remaining = []
                for item in sorted(resources, key=lambda row: ORDER[row["kind"]]):
                    present, conflict = inspect_resource(root, item)
                    if conflict:
                        out = blocked(conflict, item["resource_id"])
                        break
                    if public["profile"] == "select_explicit_cleanup_targets" and manual_targets_current(store, [item]):
                        out = blocked("resource_in_current_use", item["resource_id"])
                        break
                    if present and not remove_resource(root, item):
                        remaining.append(item["resource_id"])
                else:
                    out = {}
                if not out:
                    for item in resources:
                        present, conflict = inspect_resource(root, item)
                        if conflict:
                            out = blocked(conflict, item["resource_id"])
                            break
                        if present:
                            remaining.append(item["resource_id"])
                if not out:
                    if remaining:
                        out = pending(public, "deletion_incomplete")
                    else:
                        try:
                            if public["profile"] == "normal":
                                successor_id = store.resolve_for_cleanup(key, finish_result_id=public["finish_result_id"], inventory_id=public["inventory_id"], resource_ids=[item["resource_id"] for item in resources])
                            else:
                                successor_id = (store.resolve_selected_cleanup(key, finish_result_id=public["finish_result_id"], resource_ids=[next(row.resource_id for row in store.read(key).resources if row.kind == item["kind"] and row.portable_ref == item["portable_ref"]) for item in resources])
                                                if store.read(key) is not None else "manual-selected:" + hashlib.sha256(json.dumps(resources, sort_keys=True).encode()).hexdigest()[:24])
                        except LifecycleContractError as exc:
                            out = blocked(exc.code, exc.field_path)
                        else:
                            out = cleaned(public, successor_id)
                            if public["profile"] in {"normal", "select_explicit_cleanup_targets"}:
                                receipt_path, identity = (normal_receipt(store, public) if public["profile"] == "normal"
                                                          else manual_receipt(store, public))
                                receipt_path.parent.mkdir(parents=True, exist_ok=True)
                                receipt_path.write_text(json.dumps({"identity": identity, "output": out}, sort_keys=True) + "\n", encoding="utf-8")
    validate_json(out, package_root / "schemas/public-output.schema.json", "stdout")
    return out


if __name__ == "__main__":
    try:
        print(json.dumps(run(Path(__file__).parents[1], {}, sys.argv[1:]), ensure_ascii=False))
    except CommandError as exc:
        print(json.dumps({"code": exc.code, "field_path": exc.field_path, "remediation": exc.remediation}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(exc.exit_status)
