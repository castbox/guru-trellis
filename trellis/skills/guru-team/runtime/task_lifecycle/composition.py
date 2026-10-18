from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

from .branch_store import BranchBinding, BranchBindingStore, TaskLifecycleKey
from .checkout_acquisition import CheckoutAcquisitionPlan, CheckoutAcquisitionResult
from .checkout_resolution import canonical_head_ref
from .errors import LifecycleContractError
from .git_facts import TaskObjectReader, find_registration, inspect_registered_worktree, inspect_repository, is_ancestor, list_task_history_branch_refs, list_worktree_registrations, local_branch_head
from .identity import lifecycle_generation, normalize_task_id, normalize_task_ref, resolve_task_ref, task_identity_reservation, task_resource_state
from .resource_ledger import ResourceLedgerStore
from .schema import load_contract, validate_dto
from .session_adapter import OfficialSessionPort, SessionAdapterResult, bind_session
from .source import normalize_delivery_target, normalize_source


def _input(name: str, payload: Any) -> dict[str, Any]:
    from jsonschema import Draft202012Validator

    schema = load_contract(name)
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    if errors:
        first = min(errors, key=lambda error: (len(error.path), tuple(map(str, error.path))))
        field = ".".join(map(str, first.path)) or name
        raise LifecycleContractError("input_schema_mismatch", field, "Provide the exact closed C6 input requirements.")
    return deepcopy(payload)


@dataclass(frozen=True)
class CreationInputs:
    task_id: str
    task_ref: str
    source_profile: str
    reviewed_source: dict[str, Any]
    accepted_scope_identity: str
    delivery_target: dict[str, str]
    selected_base_ref: str
    reviewed_base_head: str
    acquisition: CheckoutAcquisitionPlan

    @property
    def result_id(self) -> str:
        return f"task-created:{self.task_id}"


def _created_checkout(inputs: CreationInputs, result: CheckoutAcquisitionResult) -> None:
    plan = inputs.acquisition
    repository = inspect_repository(plan.repository_context)
    if plan.route == "adopt_invocation_checkout":
        expected_path = plan.invocation_checkout
        expected_branch_owner = "caller_owned"
        expected_worktree_owner = "not_applicable" if result.checkout.topology == "primary" else "caller_owned"
        expected_created = (False, False)
    else:
        expected_path = plan.target_path
        expected_branch_owner = "guru_owned" if plan.provision_disposition == "new_branch" else "caller_owned"
        expected_worktree_owner = "caller_owned" if plan.provision_disposition == "existing_checkout" else "guru_owned"
        expected_created = (plan.provision_disposition == "new_branch", plan.provision_disposition != "existing_checkout")
    if (
        result.route != plan.route
        or result.transaction_id != plan.transaction_id
        or result.result_id != plan.result_id
        or expected_path is None or result.checkout.path != expected_path.resolve()
        or result.branch_ownership != expected_branch_owner
        or result.worktree_ownership != expected_worktree_owner
        or (result.created_branch, result.created_worktree) != expected_created
        or result.checkout.common_dir != repository.common_dir
        or result.checkout.branch_ref != canonical_head_ref(plan.branch_ref)
        or result.checkout.head != plan.decision_head
    ):
        raise LifecycleContractError("creation_acquisition_mismatch", "checkout_result", "Use the exact reviewed acquisition result.")
    registration = find_registration(repository, result.checkout.path)
    if registration is None:
        raise LifecycleContractError("creation_checkout_stale", "checkout_result", "Resolve the acquired registered checkout.")
    live = inspect_registered_worktree(repository, registration)
    if (
        live.inspection_error
        or live.git_dir != result.checkout.git_dir
        or live.branch_ref != result.checkout.branch_ref
        or live.head != result.checkout.head
    ):
        raise LifecycleContractError("creation_checkout_stale", "checkout_result", "Resolve the exact current acquisition checkout.")
    artifact = resolve_task_ref(live.path, inputs.task_ref, expected_task_id=inputs.task_id)
    if artifact.lifecycle_state != "active" or artifact.lifecycle_generation != 0:
        raise LifecycleContractError("creation_identity_mismatch", "task_ref", "Use the newly created planning task incarnation.")
    try:
        metadata = json.loads((live.path / inputs.task_ref / "task.json").read_text(encoding="utf-8"))
        source = normalize_source(metadata.get("source"))
    except (OSError, ValueError, LifecycleContractError) as exc:
        raise LifecycleContractError("creation_identity_mismatch", "task_ref", "Read the created planning task.") from exc
    if task_resource_state(live.path, metadata) != "active" or source != inputs.reviewed_source or metadata.get("base_branch") != inputs.selected_base_ref.removeprefix("refs/heads/"):
        raise LifecycleContractError("creation_identity_mismatch", "task_ref", "Recover only the exact reviewed task source and base.")


def establish_created_control_state(inputs: CreationInputs, result: CheckoutAcquisitionResult) -> BranchBinding:
    """Compose initial branch and C5 ownership from the exact acquisition disposition."""

    _created_checkout(inputs, result)
    repository = inspect_repository(inputs.acquisition.repository_context)
    key = TaskLifecycleKey(inputs.task_id, 0)
    branches = BranchBindingStore(repository)
    resources = ResourceLedgerStore(repository)
    if branches.read(key) is not None or resources.read(key) is not None:
        raise LifecycleContractError("creation_control_state_exists", "control_state", "Recover the exact existing result instead of creating it twice.")
    before_branch = branches.snapshot(key)
    before_resources = resources.snapshot(key)
    try:
        binding = branches.establish(key, inputs.acquisition.branch_ref.removeprefix("refs/heads/"))
        resources.establish_current(
            key,
            binding_revision=binding.binding_revision,
            branch_name=binding.branch_name,
            branch_ownership=result.branch_ownership,
            worktree_ownership=result.worktree_ownership,
        )
        return binding
    except Exception:
        try:
            resources.restore(key, before_resources)
        finally:
            branches.restore(before_branch)
        raise


def recover_created_control_state(
    inputs: CreationInputs, result: CheckoutAcquisitionResult, *, expected_result_id: str,
) -> BranchBinding:
    """Rematerialize an exact result without repeating a task or control-state write."""

    if expected_result_id != inputs.result_id:
        raise LifecycleContractError("creation_result_mismatch", "result_id", "Recover the stable task creation result identity.")
    _created_checkout(inputs, result)
    repository = inspect_repository(inputs.acquisition.repository_context)
    key = TaskLifecycleKey(inputs.task_id, 0)
    binding = BranchBindingStore(repository).read(key)
    ledger = ResourceLedgerStore(repository).read(key)
    if (
        binding is None or ledger is None or binding.binding_revision != 0
        or binding.branch_ref != canonical_head_ref(inputs.acquisition.branch_ref)
    ):
        raise LifecycleContractError("creation_result_mismatch", "control_state", "Recover only the exact initial branch result.")
    current = [row for row in ledger.resources if row.state == "current"]
    expected = {"current_branch"}
    if result.worktree_ownership != "not_applicable":
        expected.add("current_worktree")
    if (
        ledger.ledger_revision != 1
        or {row.responsibility_role for row in current} != expected
        or any(row.binding_revision != 0 for row in current)
        or any(row.branch_ref != binding.branch_ref for row in current if row.responsibility_role in {"current_branch", "current_worktree"})
        or any(row.ownership != result.branch_ownership for row in current if row.responsibility_role == "current_branch")
        or any(row.ownership != result.worktree_ownership for row in current if row.responsibility_role == "current_worktree")
    ):
        raise LifecycleContractError("creation_result_mismatch", "resource_ledger", "Recover only the exact acquisition ownership.")
    return binding


def bind_created_session(
    official: OfficialSessionPort,
    inputs: CreationInputs,
    result: CheckoutAcquisitionResult,
    *,
    platform_input: dict[str, Any] | None = None,
    platform: str | None = None,
) -> SessionAdapterResult:
    """Bind a completed creation; session failure never undoes task ownership."""

    recover_created_control_state(
        inputs, result, expected_result_id=inputs.result_id,
    )
    return bind_session(
        official,
        result.checkout.path,
        {"task_id": inputs.task_id, "lifecycle_generation": 0},
        platform_input=platform_input,
        platform=platform,
    )


def prepare_creation_inputs(
    repo_root: Path | str,
    payload: dict[str, Any],
    acquisition: CheckoutAcquisitionPlan,
) -> CreationInputs:
    """Check the reviewed create requirements before a package owns any mutation."""

    data = _input("task-creation-input.schema.json", payload)
    task_id = normalize_task_id(data["task_id"])
    task_ref = normalize_task_ref(data["task_ref"])
    source = normalize_source(data["reviewed_source"])
    target = normalize_delivery_target(data["delivery_target"])
    selected_base = canonical_head_ref(data["selected_base_ref"], field_path="selected_base_ref")
    expected_kind = "issue" if data["source_profile"] == "existing_issue" else "no_issue"
    if source["kind"] != expected_kind:
        raise LifecycleContractError("source_profile_mismatch", "reviewed_source", "Use the reviewed source profile.")
    repository = inspect_repository(repo_root)
    if local_branch_head(repository, selected_base) != data["reviewed_base_head"]:
        raise LifecycleContractError("creation_base_stale", "reviewed_base_head", "Refresh the reviewed base authority.")
    if acquisition.decision_head != data["reviewed_base_head"]:
        raise LifecycleContractError("creation_acquisition_mismatch", "acquisition.decision_head", "Use the acquisition plan for the reviewed base head.")
    if inspect_repository(acquisition.repository_context).common_dir != repository.common_dir:
        raise LifecycleContractError("creation_repository_mismatch", "acquisition", "Use the selected repository.")
    if (
        acquisition.task_id != task_id
        or acquisition.task_ref != task_ref
        or acquisition.lifecycle_generation != 0
        or acquisition.task_artifact_expectation != "absent"
        or acquisition.expected_status != "active"
        or acquisition.route not in {"adopt_invocation_checkout", "provision_linked_worktree"}
    ):
        raise LifecycleContractError("creation_acquisition_mismatch", "acquisition", "Acquire the exact pre-task generation-zero checkout.")
    request = acquisition.request()
    if request.branch_ref in {canonical_head_ref(target["branch_ref"]), selected_base}:
        raise LifecycleContractError("delivery_or_base_branch_forbidden", "acquisition.branch_ref", "Select a non-base, non-delivery task branch.")
    if acquisition.route == "adopt_invocation_checkout":
        if acquisition.invocation_checkout is None or acquisition.provision_disposition is not None:
            raise LifecycleContractError("creation_acquisition_mismatch", "acquisition", "Bind the exact invocation checkout.")
        invocation = inspect_repository(acquisition.invocation_checkout)
        if invocation.git_dir == invocation.common_dir:
            raise LifecycleContractError(
                "primary_checkout_requires_isolation", "acquisition.invocation_checkout",
                "Review a clean linked non-base checkout for adoption or provision a linked worktree before creating the task.",
            )
    elif acquisition.provision_disposition not in {"new_branch", "existing_branch", "existing_checkout"}:
        raise LifecycleContractError("creation_acquisition_mismatch", "acquisition", "Bind the reviewed provision disposition.")
    for registration in list_worktree_registrations(repository):
        if registration.bare:
            continue
        if not registration.path.is_dir():
            raise LifecycleContractError("creation_checkout_stale", "git.worktree_list", "Resolve registered task checkouts before creation.")
        try:
            occupied = task_identity_reservation(registration.path, task_id, task_ref)
        except LifecycleContractError as exc:
            raise LifecycleContractError(
                exc.code, str(registration.path / exc.field_path), exc.remediation,
            ) from exc
        if occupied is not None:
            raise LifecycleContractError(
                "task_identity_already_exists", str(registration.path / occupied),
                "Resolve the existing task or select an unused TaskId and TaskRef.",
            )
    with TaskObjectReader(repository) as reader:
        for _branch_ref, head in list_task_history_branch_refs(repository):
            paths = [path for path in reader.paths_under(head, ".trellis/tasks")
                     if re.fullmatch(r"\.trellis/tasks/(?:archive/.+/)?[^/]+/task\.json", path)]
            committed = reader.prepare(head, paths)
            for path in paths:
                payload = reader.read_path(committed, path)
                try:
                    metadata = json.loads(payload) if payload is not None else None
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    if path.removesuffix("/task.json") == task_ref:
                        raise LifecycleContractError("invalid_task_identity", f"{_branch_ref}:{path}", "Resolve the task artifact on the local branch.") from exc
                    continue
                if not isinstance(metadata, dict):
                    if path.removesuffix("/task.json") == task_ref:
                        raise LifecycleContractError("invalid_task_identity", f"{_branch_ref}:{path}", "Resolve the task artifact on the local branch.")
                    continue
                if (
                    str(metadata.get("id", "")).casefold() == task_id.casefold()
                    or path.removesuffix("/task.json") == task_ref
                ):
                    raise LifecycleContractError("task_identity_already_exists", f"{_branch_ref}:{path}", "Resolve the existing task or select an unused TaskId and TaskRef.")
    for ledger in ResourceLedgerStore(repository).iter_ledgers(task_id=task_id):
        if ledger.task_id.casefold() == task_id.casefold() and any(row.state != "resolved" for row in ledger.resources):
            raise LifecycleContractError(
                "task_identity_already_exists", str(ResourceLedgerStore(repository).path_for(TaskLifecycleKey(ledger.task_id, ledger.lifecycle_generation))),
                "Resolve the existing task resource ledger before reusing its TaskId.",
            )
    return CreationInputs(
        task_id, task_ref, data["source_profile"], source, data["accepted_scope_identity"],
        target, selected_base, data["reviewed_base_head"], acquisition,
    )


__all__ = [
    "CreationInputs", "bind_created_session", "establish_created_control_state",
    "prepare_creation_inputs", "recover_created_control_state",
]
