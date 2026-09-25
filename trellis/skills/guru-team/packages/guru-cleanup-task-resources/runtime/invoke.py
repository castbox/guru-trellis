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
        "exit_id": "manual_selection_required" if public["profile"] == "manual" or code == "terminal_resource_ledger_missing" else "remaining_resources",
        "task_id": public["task_id"],
        "lifecycle_generation": public["lifecycle_generation"],
        "finish_result_id": public["finish_result_id"],
        "reason_code": code,
        "reason_refs": [public["task_id"]],
    }


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
    identity = {field: public[field] for field in ("task_id", "lifecycle_generation", "finish_result_id", "selected_targets")}
    digest = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:32]
    path = store.repository.common_dir / "guru-team" / "cleanup-results" / public["task_id"] / f'manual-{digest}.json'
    return path, identity


def normal_receipt(store: ResourceLedgerStore, public: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    identity = {field: public[field] for field in ("task_id", "lifecycle_generation", "finish_result_id", "inventory_id")}
    digest = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:32]
    path = store.repository.common_dir / "guru-team" / "cleanup-results" / public["task_id"] / f'normal-{digest}.json'
    return path, identity


def manual_targets_current(root: Path, store: ResourceLedgerStore, resources: list[dict[str, Any]]) -> bool:
    selected = {(row["kind"], json.dumps(row["portable_ref"], sort_keys=True)) for row in resources}
    for ledger in store.iter_ledgers():
        for row in ledger.resources:
            if row.state == "current" and (row.kind, json.dumps(row.portable_ref, sort_keys=True)) in selected:
                return True
    for binding in BranchBindingStore(store.repository).iter_bindings():
        try:
            task = resolve_task_id(root, binding.task_id)
        except LifecycleContractError:
            continue
        if task.lifecycle_state != "active" or task.lifecycle_generation != binding.lifecycle_generation:
            continue
        if any(row["portable_ref"].get("ref", row["portable_ref"].get("branch_ref")) == binding.branch_ref for row in resources):
            return True
    return False


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
                        out = pending(public, resolution.reason_code or "manual_selection_required")
                        resources = []
                    else:
                        resources = [item.as_dict() for item in resolution.resources]
                        out = {}
            else:
                ledger = store.read(key)
                if ledger is not None and ledger.finish_result_id != public["finish_result_id"]:
                    raise LifecycleContractError("resource_ledger_conflict", "finish_result_id", "Select the current Finish result.")
                resources = public["selected_targets"]
                out = {}
                receipt_path, receipt_identity = manual_receipt(store, public)
                if receipt_path.is_file():
                    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                    if receipt.get("identity") != receipt_identity:
                        raise LifecycleContractError("resource_inventory_stale", "manual_receipt", "Recover the exact selected cleanup result.")
                    out = receipt["output"]
                    resources = []
                elif ledger is None:
                    task = resolve_task_id(root, key.task_id)
                    if task.lifecycle_state != "archived" or task.lifecycle_generation != key.lifecycle_generation:
                        raise LifecycleContractError("archived_lifecycle_stale", "task", "Select a normally finished archived lifecycle.")
                if ledger is not None:
                    eligible = {row.resource_id: row for row in ledger.resources if row.ownership == "caller_owned" and row.state == "retained" and row.responsibility_role == "manual_only"}
                    if not out and any(
                        item["resource_id"] not in eligible
                        or item["kind"] != eligible[item["resource_id"]].kind
                        or item["portable_ref"] != eligible[item["resource_id"]].portable_ref
                        or (
                            eligible[item["resource_id"]].expected_cleanup_head is not None
                            and item["expected_cleanup_head"] != eligible[item["resource_id"]].expected_cleanup_head
                        )
                        for item in resources
                    ):
                        raise LifecycleContractError("resource_ownership_conflict", "selected_targets", "Select only exact caller-owned retired resources.")
                if not out and manual_targets_current(root, store, resources):
                    raise LifecycleContractError("resource_in_current_use", "selected_targets", "Do not delete any active task's current resource.")
        except LifecycleContractError as exc:
            out = blocked(exc.code, exc.field_path)
            resources = []
        if not out:
            scheduled_worktree_refs = frozenset(item["portable_ref"]["branch_ref"] for item in resources if item["kind"] == "linked_worktree")
            conflicts = [code for item in resources for present, code in [inspect_resource(root, item, scheduled_worktree_refs)] if code]
            if conflicts:
                out = blocked(conflicts[0], public["task_id"])
            elif route == "remaining_resources" or (resources and not args.confirmed_cleanup):
                out = pending(public, "confirmation_required")
            else:
                remaining = []
                for item in sorted(resources, key=lambda row: ORDER[row["kind"]]):
                    present, conflict = inspect_resource(root, item)
                    if conflict:
                        out = blocked(conflict, item["resource_id"])
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
                                successor_id = (store.resolve_selected_cleanup(key, finish_result_id=public["finish_result_id"], resource_ids=[item["resource_id"] for item in resources])
                                                if store.read(key) is not None else "manual-selected:" + hashlib.sha256(json.dumps(resources, sort_keys=True).encode()).hexdigest()[:24])
                        except LifecycleContractError as exc:
                            out = blocked(exc.code, exc.field_path)
                        else:
                            out = cleaned(public, successor_id)
                            if public["profile"] in {"normal", "manual"}:
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
