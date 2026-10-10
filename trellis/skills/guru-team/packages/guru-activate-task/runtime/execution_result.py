from __future__ import annotations

from pathlib import Path

from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.composition import ActivationInputs, _current_planning_identity
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import discover_worktree_facts, inspect_repository, is_ancestor, local_branch_head
from runtime.task_lifecycle.identity import normalize_task_ref, resolve_task_ref
from runtime.task_lifecycle.checkout_resolution import canonical_head_ref
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


PACKAGE = Path(__file__).resolve().parents[1]


def execution_result_path(root: Path, task_ref: str) -> Path:
    ref = normalize_task_ref(task_ref)
    return root / ".trellis/.runtime/guru-team/owner-checkpoints" / Path(ref).name / "execution-result.json"


def _snapshot(root: Path, inputs: ActivationInputs, operation: str) -> dict:
    repository = inspect_repository(root)
    key = TaskLifecycleKey(inputs.task_id, inputs.lifecycle_generation)
    binding = BranchBindingStore(repository).read(key)
    if binding is None:
        raise LifecycleContractError("activation_branch_unresolved", "branch_binding", "Resolve the current lifecycle binding.")
    return {
        "schema_version": "1.0", "operation": operation,
        "task_id": inputs.task_id, "task_ref": inputs.task_ref,
        "lifecycle_generation": inputs.lifecycle_generation,
        "planning_result_id": inputs.planning_result_id,
        "selected_base_ref": inputs.selected_base_ref,
        "continuity": inputs.continuity, "binding_revision": binding.binding_revision,
    }


def _read(root: Path, task_ref: str) -> dict | None:
    path = execution_result_path(root, task_ref)
    if not path.exists():
        return None
    result = read_json(str(path), "execution_result")
    validate_json(result, PACKAGE / "schemas/execution-result.schema.json", "execution_result")
    return result


def record_execution_result(root: Path, inputs: ActivationInputs, *, operation: str) -> None:
    """Record only a completed owner operation, never a plan judgment or acceptance."""
    import json

    result = _snapshot(root, inputs, operation)
    validate_json(result, PACKAGE / "schemas/execution-result.schema.json", "execution_result")
    path = execution_result_path(root, inputs.task_ref)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_execution_result(
    root: Path, inputs: ActivationInputs, *, operation: str, required: bool = True,
) -> None:
    """Recover the same completed operation without rewriting its bytes."""
    result = _read(root, inputs.task_ref)
    if result is None:
        if required:
            raise LifecycleContractError("execution_result_missing", "execution_result", "Return to fresh Planning if no completed resume result remains.")
        return
    if result["operation"] != operation:
        raise LifecycleContractError("execution_operation_mismatch", "operation", "Use the recovery action for the actual completed operation.")
    if result != _snapshot(root, inputs, operation):
        raise LifecycleContractError("execution_result_stale", "execution_result", "Reread current planning, lifecycle and continuity through their owners.")


def execution_recovery_payload(root: Path, identity: dict) -> dict:
    """Restore operation inputs from this owner's actual completed result.

    The caller needs only current lifecycle/session identity after both the
    original approved DTO and invocation input were lost.
    """
    current = resolve_task_ref(root, identity["task_ref"], expected_task_id=identity["task_id"])
    if current.lifecycle_state != "active" or current.lifecycle_generation != identity["lifecycle_generation"]:
        raise LifecycleContractError("activation_identity_stale", "task_ref", "Resolve the current active incarnation.")
    task = read_json(str(root / current.task_ref / "task.json"), "task")
    if task["status"] != "in_progress":
        raise LifecycleContractError("activation_status_mismatch", "task.status", "Recover execution only for the current in_progress task.")
    result = _read(root, identity["task_ref"])
    if result is None:
        raise LifecycleContractError("execution_result_missing", "execution_result", "Return to fresh Planning if no completed resume result remains.")
    if result["operation"] != "resume_execution":
        raise LifecycleContractError("execution_operation_mismatch", "operation", "Recover only the actual completed resume operation.")
    fields = ("task_id", "task_ref", "lifecycle_generation")
    if any(result[field] != identity[field] for field in fields):
        raise LifecycleContractError("execution_result_stale", "execution_result", "Resolve the original current lifecycle before result recovery.")
    return {**{field: result[field] for field in (
        *fields, "planning_result_id", "selected_base_ref", "continuity",
    )}, "session_mode": identity["session_mode"]}


def retire_execution_result(
    root: Path, *, task_ref: str,
) -> bool:
    """Called only after Check validates its current passed output.

    Check supplies its current identity, never reads this private record, and
    never supplies an approval flag. Absence or ordinary stale state retains
    compatibility with old tasks and does not overturn an independent Check.
    """
    root = root.resolve()
    try:
        result = _read(root, task_ref)
        if result is None:
            return False
        identity = resolve_task_ref(root, task_ref)
        task_id, lifecycle_generation = identity.task_id, identity.lifecycle_generation
        if (result["task_id"], result["task_ref"], result["lifecycle_generation"]) != (
            task_id, task_ref, lifecycle_generation,
        ):
            return False
        task = read_json(str(root / task_ref / "task.json"), "task")
        if identity.lifecycle_state != "active" or identity.lifecycle_generation != lifecycle_generation or task["status"] != "in_progress":
            return False
        if result["planning_result_id"] != _current_planning_identity(root, task_ref):
            return False
        repository = inspect_repository(root)
        key = TaskLifecycleKey(task_id, lifecycle_generation)
        binding = BranchBindingStore(repository).read(key)
        ownership = ResourceLedgerStore(repository).read_current(key)
        if binding is None or ownership is None or (
            binding.binding_revision, binding.branch_name
        ) != (ownership.binding_revision, ownership.branch_name) or binding.binding_revision != result["binding_revision"]:
            return False
        current = [row.path for row in discover_worktree_facts(repository) if row.branch_ref == binding.branch_ref]
        if current != [root]:
            return False
        base_ref = canonical_head_ref(result["selected_base_ref"], field_path="selected_base_ref")
        continuity = result["continuity"]
        base_head = continuity["base_head"] if continuity["kind"] == "base_current" else continuity["new_base_head"]
        if task["base_branch"] != base_ref.removeprefix("refs/heads/") or local_branch_head(repository, binding.branch_ref) != continuity["task_head"]:
            return False
        if local_branch_head(repository, base_ref) != base_head or not is_ancestor(repository, base_head, continuity["task_head"]):
            return False
    except (CommandError, LifecycleContractError, OSError, ValueError):
        return False
    path = execution_result_path(root, task_ref)
    path.unlink()
    if not any(path.parent.iterdir()):
        path.parent.rmdir()
    return True
