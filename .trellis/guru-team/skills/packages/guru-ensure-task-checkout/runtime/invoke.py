from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError, fail, read_json, write_json
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import discover_worktree_facts, inspect_repository
from runtime.task_lifecycle.identity import resolve_task_id
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


def invoke(root: Path, data: dict) -> dict:
    package = Path(__file__).resolve().parents[1]
    validate_json(data, package / "schemas/public-input.schema.json", "input")
    repository = inspect_repository(root)
    key = TaskLifecycleKey(data["task_id"], data["lifecycle_generation"])
    binding = BranchBindingStore(repository).read(key)
    if binding is None:
        return {"exit_id": "binding_required", "task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation}
    ownership = ResourceLedgerStore(repository).read_current(key)
    if ownership is None:
        return {"exit_id": "binding_required", "task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation}
    if (ownership.binding_epoch, ownership.binding_revision, ownership.branch_name) != (
        binding.binding_epoch, binding.binding_revision, binding.branch_name
    ):
        return {"exit_id": "invalid_task_state", "reason_code": "binding_ownership_mismatch"}
    candidates = [row for row in discover_worktree_facts(repository) if row.registration.registered_branch_ref == binding.branch_ref]
    if not candidates:
        return {"exit_id": "checkout_required", "task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation}
    if len(candidates) != 1:
        return {"exit_id": "invalid_task_state", "reason_code": "ambiguous_checkout"}
    current = candidates[0]
    if current.inspection_error or current.common_dir != repository.common_dir or current.branch_ref != binding.branch_ref:
        return {"exit_id": "invalid_task_state", "reason_code": "checkout_identity_mismatch"}
    try:
        task = resolve_task_id(current.path, key.task_id)
    except LifecycleContractError as exc:
        if exc.code == "task_not_found":
            return {"exit_id": "invalid_task_state", "reason_code": "task_artifact_mismatch"}
        raise
    if task.lifecycle_state != "active" or task.lifecycle_generation != key.lifecycle_generation:
        return {"exit_id": "invalid_task_state", "reason_code": "task_identity_stale"}
    metadata = json.loads((current.path / task.task_ref / "task.json").read_text(encoding="utf-8"))
    if metadata.get("status") not in {"planning", "in_progress"}:
        return {"exit_id": "invalid_task_state", "reason_code": "task_status_mismatch"}
    return {
        "exit_id": "checkout_resolved", "task_id": key.task_id, "task_ref": task.task_ref,
        "lifecycle_generation": key.lifecycle_generation, "checkout_path": str(current.path),
    }


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    output = invoke(Path(args.root).resolve(), read_json(args.input, "input"))
    validate_json(output, package_root / "schemas/public-output.schema.json", "stdout")
    return output


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    try:
        args = parser.parse_args(argv)
        package = Path(__file__).resolve().parents[1]
        output = invoke(Path(args.root).resolve(), read_json(args.input, "input"))
        validate_json(output, package / "schemas/public-output.schema.json", "stdout")
        write_json(output)
        return 0
    except LifecycleContractError as exc:
        return fail(CommandError("stale_identity", exc.field_path, exc.remediation, 3))
    except CommandError as exc:
        return fail(exc)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
