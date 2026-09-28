from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import CheckoutStateSnapshot, discover_worktree_facts, inspect_repository, is_ancestor, local_branch_head
from runtime.task_lifecycle.rebind import RebindPlan, execute_rebind, prepare_rebind, recover_rebind
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


def _plan_json(plan: RebindPlan, base_ref: str, base_head: str) -> dict:
    before = plan.pre_state
    return {
        "route": plan.route, "task_id": plan.key.task_id, "lifecycle_generation": plan.key.lifecycle_generation,
        "task_ref": plan.task_ref, "expected_status": plan.expected_status,
        "current_checkout": str(plan.current_checkout), "target_branch_name": plan.target_branch_name,
        "expected_revision": plan.expected_revision,
        "pre_state": {"path": str(before.path), "head": before.head, "branch_ref": before.branch_ref,
                      "index_sha256": before.index_sha256, "worktree_sha256": before.worktree_sha256,
                      "status_sha256": before.status_sha256},
        "target_checkout": str(plan.target_checkout) if plan.target_checkout else None,
        "target_head": plan.target_head, "selected_base_ref": base_ref, "reviewed_base_head": base_head,
    }


def _plan_from_json(data: dict) -> RebindPlan:
    before = data["pre_state"]
    return RebindPlan(
        route=data["route"], key=TaskLifecycleKey(data["task_id"], data["lifecycle_generation"]),
        task_ref=data["task_ref"], expected_status=data["expected_status"],
        current_checkout=Path(data["current_checkout"]), target_branch_name=data["target_branch_name"],
        expected_revision=data["expected_revision"],
        pre_state=CheckoutStateSnapshot(
            path=Path(before["path"]), head=before["head"], branch_ref=before["branch_ref"],
            index_sha256=before["index_sha256"], worktree_sha256=before["worktree_sha256"],
            status_sha256=before["status_sha256"],
        ),
        target_checkout=Path(data["target_checkout"]) if data["target_checkout"] else None,
        target_head=data["target_head"],
    )


def prepare(root: Path, data: dict) -> dict:
    package = Path(__file__).resolve().parents[1]
    validate_json(data, package / "schemas/public-plan-request.schema.json", "input")
    repository = inspect_repository(root)
    current = Path(data["current_checkout"]).resolve()
    matches = [row for row in discover_worktree_facts(repository) if row.path == current]
    if len(matches) != 1 or matches[0].inspection_error or not matches[0].clean:
        raise LifecycleContractError("dirty_or_unregistered_checkout", "current_checkout", "Review one clean registered current checkout.")
    base_ref = data["selected_base_ref"]
    base_head = local_branch_head(repository, base_ref)
    if base_head != data["reviewed_base_head"] or not is_ancestor(repository, matches[0].head, base_head):
        raise LifecycleContractError("rebind_base_stale", "selected_base_ref", "Reconcile current HEAD into the reviewed target base first.")
    plan = prepare_rebind(
        repository, BranchBindingStore(repository), ResourceLedgerStore(repository),
        route=data["route"], key=TaskLifecycleKey(data["task_id"], data["lifecycle_generation"]),
        task_ref=data["task_ref"], expected_status=data["expected_status"],
        current_checkout=current, target_branch_name=data["target_branch_name"],
    )
    return _plan_json(plan, base_ref, base_head)


def invoke(root: Path, data: dict) -> dict:
    package = Path(__file__).resolve().parents[1]
    validate_json(data, package / "schemas/public-input.schema.json", "input")
    plan_data = data["plan"]
    try:
        repository = inspect_repository(root)
        plan = _plan_from_json(plan_data)
        store, ownership = BranchBindingStore(repository), ResourceLedgerStore(repository)
        if data["action"] == "execute":
            request = {key: plan_data[key] for key in (
                "route", "task_id", "task_ref", "lifecycle_generation", "expected_status",
                "current_checkout", "target_branch_name", "selected_base_ref", "reviewed_base_head",
            )}
            if prepare(root, request) != plan_data:
                return {"exit_id": "refresh_review", "task_id": plan.key.task_id,
                        "lifecycle_generation": plan.key.lifecycle_generation}
            result = execute_rebind(repository, store, ownership, plan)
        else:
            result = recover_rebind(repository, store, ownership, plan)
        return {"exit_id": "rebound", "task_id": result.binding.task_id,
                "lifecycle_generation": result.binding.lifecycle_generation}
    except LifecycleContractError as exc:
        if exc.code in {"rebind_base_stale", "rebind_plan_stale"}:
            return {"exit_id": "refresh_review", "task_id": plan_data["task_id"],
                    "lifecycle_generation": plan_data["lifecycle_generation"]}
        if exc.code in {"invalid_task_id", "invalid_task_ref", "invalid_lifecycle_generation", "task_artifact_mismatch"}:
            return {"exit_id": "invalid_task_state", "reason_code": exc.code}
        return {"exit_id": "blocked", "reason_code": exc.code}


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    data = read_json(args.input, "input")
    root = Path(args.root).resolve()
    command_id = command.get("id", "invoke-guru-rebind-task-branch")
    if command_id == "record-task-branch-rebind-plan":
        try:
            return {"status": "prepared", "plan": prepare(root, data)}
        except LifecycleContractError as exc:
            raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    if command_id in {"check-task-branch-rebind-result", "recover-task-branch-rebind-result"} and data.get("action") != "recover":
        raise CommandError("invalid_arguments", "action", "Use read-only recovery for this command.")
    if command_id == "rebind-task-branch" and data.get("action") != "execute":
        raise CommandError("invalid_arguments", "action", "Use the reviewed execution action.")
    output = invoke(root, data)
    validate_json(output, package_root / "schemas/public-output.schema.json", "stdout")
    return output
