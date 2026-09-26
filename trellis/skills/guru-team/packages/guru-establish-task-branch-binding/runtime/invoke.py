from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError, fail, read_json, write_json
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_resolution import establish_branch_binding, recover_established_branch_binding, resolve_establishment
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.identity import resolve_task_ref
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


def _candidate(row) -> dict:
    return {
        "candidate_id": row.candidate_id, "branch_name": row.branch_name,
        "kind": row.kind, "checkout_path": str(row.checkout_path) if row.checkout_path else None,
        "head": row.head, "valid": row.valid, "reason_code": row.reason_code,
    }


def invoke(root: Path, data: dict) -> dict:
    package = Path(__file__).resolve().parents[1]
    validate_json(data, package / "schemas/public-input.schema.json", "input")
    key = TaskLifecycleKey(data["task_id"], data["lifecycle_generation"])
    try:
        artifact = resolve_task_ref(root, data["task_ref"], expected_task_id=key.task_id)
        if artifact.lifecycle_state != "active" or artifact.lifecycle_generation != key.lifecycle_generation:
            return {"exit_id": "invalid_task_state", "reason_code": "task_identity_stale"}
        repository = inspect_repository(root)
        store = BranchBindingStore(repository)
        ownership = ResourceLedgerStore(repository)
        args = dict(key=key, task_ref=artifact.task_ref, expected_status=data["expected_status"])
        if data["action"] == "recover":
            result = recover_established_branch_binding(repository, store, ownership, **args, **data["recovery"])
        else:
            resolution = resolve_establishment(repository, store, ownership, **args)
            if resolution.kind == "already_established":
                result = resolution
            elif data.get("selected_candidate_id") is None and resolution.kind == "selection_required":
                result = resolution
            else:
                selected = data.get("selected_candidate_id")
                candidates = resolution.valid_candidates
                if selected is not None:
                    candidates = tuple(row for row in candidates if row.candidate_id == selected)
                head = candidates[0].head if len(candidates) == 1 else data.get("expected_candidate_head", "")
                result = establish_branch_binding(
                    repository, store, ownership, **args,
                    selected_candidate_id=selected,
                    expected_candidate_head=data.get("expected_candidate_head", head),
                )
        if result.kind == "selection_required":
            return {
                "exit_id": "selection_required", "task_id": key.task_id,
                "lifecycle_generation": key.lifecycle_generation,
                "reason_code": result.reason_code,
                "candidates": [_candidate(row) for row in result.candidates],
            }
        return {"exit_id": "binding_established", "task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation}
    except LifecycleContractError as exc:
        if exc.code in {"invalid_task_id", "invalid_task_ref", "invalid_lifecycle_generation", "task_not_found", "task_identity_mismatch"}:
            return {"exit_id": "invalid_task_state", "reason_code": exc.code}
        return {"exit_id": "blocked", "reason_code": exc.code}


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    data = read_json(args.input, "input")
    validate_json(data, package_root / "schemas/public-input.schema.json", "input")
    command_id = command.get("id", "invoke-guru-establish-task-branch-binding")
    if command_id in {"discover-task-branch-binding-candidates", "record-task-branch-binding-plan"}:
        if data["action"] != "establish":
            raise CommandError("invalid_arguments", "action", "Discovery and plan validation must not recover or mutate.")
        repository = inspect_repository(Path(args.root).resolve())
        key = TaskLifecycleKey(data["task_id"], data["lifecycle_generation"])
        artifact = resolve_task_ref(Path(args.root).resolve(), data["task_ref"], expected_task_id=key.task_id)
        if artifact.lifecycle_state != "active" or artifact.lifecycle_generation != key.lifecycle_generation:
            raise CommandError("stale_identity", "task_ref", "Resolve the current active task incarnation.", 3)
        resolution = resolve_establishment(
            repository, BranchBindingStore(repository), ResourceLedgerStore(repository),
            key=key, task_ref=artifact.task_ref, expected_status=data["expected_status"],
        )
        return {"status": resolution.kind, "reason_code": resolution.reason_code,
                "candidates": [_candidate(row) for row in resolution.candidates]}
    if command_id in {"recover-established-task-branch-binding-result", "check-task-branch-binding-result"}:
        if data["action"] != "recover":
            raise CommandError("invalid_arguments", "action", "Use the read-only recovery action for this command.")
    elif command_id == "establish-task-branch-binding" and data["action"] != "establish":
        raise CommandError("invalid_arguments", "action", "Use the establishment action for this command.")
    output = invoke(Path(args.root).resolve(), data)
    validate_json(output, package_root / "schemas/public-output.schema.json", "stdout")
    return output


def main(argv: list[str]) -> int:
    try:
        write_json(run(Path(__file__).resolve().parents[1], {}, argv))
        return 0
    except CommandError as exc:
        return fail(exc)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
