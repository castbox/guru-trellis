from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Literal, Protocol

from .branch_store import (
    BranchBinding,
    BranchBindingStore,
    TaskLifecycleKey,
    normalize_branch_name,
)
from .errors import LifecycleContractError
from .git_facts import (
    RepositoryFacts,
    commit_path_bytes,
    discover_worktree_facts,
    list_local_branch_refs,
)
from .identity import normalize_generation, normalize_task_id, normalize_task_ref


Ownership = Literal["guru_owned", "caller_owned", "not_applicable"]
CandidateKind = Literal["registered_checkout", "local_branch"]
EstablishmentKind = Literal[
    "already_established",
    "candidate_resolved",
    "binding_established",
    "selection_required",
]


@dataclass(frozen=True)
class OwnershipCurrent:
    task_id: str
    lifecycle_generation: int
    binding_revision: int
    branch_name: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "task_id", normalize_task_id(self.task_id))
        object.__setattr__(
            self,
            "lifecycle_generation",
            normalize_generation(self.lifecycle_generation),
        )
        if type(self.binding_revision) is not int or self.binding_revision < 0:
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "binding_revision",
                "Use one non-negative current resource binding revision.",
            )
        object.__setattr__(self, "branch_name", normalize_branch_name(self.branch_name))

    @property
    def key(self) -> TaskLifecycleKey:
        return TaskLifecycleKey(self.task_id, self.lifecycle_generation)


class OwnershipPort(Protocol):
    """C4 consumes ownership state without defining the C5 ledger implementation."""

    def read_current(self, key: TaskLifecycleKey) -> OwnershipCurrent | None: ...

    def snapshot(self, key: TaskLifecycleKey) -> Any: ...

    def restore(self, key: TaskLifecycleKey, snapshot: Any) -> None: ...

    def establish_current(
        self,
        key: TaskLifecycleKey,
        *,
        binding_revision: int,
        branch_name: str,
        branch_ownership: Ownership,
        worktree_ownership: Ownership,
    ) -> OwnershipCurrent: ...

    def rebind_current(
        self,
        key: TaskLifecycleKey,
        *,
        expected_revision: int,
        source_branch_name: str,
        target_branch_name: str,
        expected_cleanup_head: str,
        target_branch_ownership: Ownership,
        target_worktree_ownership: Ownership | None,
        worktree_reassociated: bool,
    ) -> OwnershipCurrent: ...

    def branch_has_unresolved_incarnation(
        self,
        branch_name: str,
        *,
        key: TaskLifecycleKey,
        allowed_current_revision: int | None,
    ) -> bool: ...


@dataclass(frozen=True)
class BranchCandidate:
    candidate_id: str
    branch_name: str
    head: str
    kind: CandidateKind
    checkout_path: Path | None
    topology: str | None
    valid: bool
    reason_code: str | None


@dataclass(frozen=True)
class EstablishmentResolution:
    kind: EstablishmentKind
    binding: BranchBinding | None
    ownership: OwnershipCurrent | None
    candidates: tuple[BranchCandidate, ...]
    selected: BranchCandidate | None
    reason_code: str

    @property
    def valid_candidates(self) -> tuple[BranchCandidate, ...]:
        return tuple(row for row in self.candidates if row.valid)


def _artifact_matches(
    repository: RepositoryFacts,
    *,
    head: str,
    task_ref: str,
    key: TaskLifecycleKey,
    expected_status: str,
) -> bool:
    payload = commit_path_bytes(repository, head, f"{task_ref}/task.json")
    if payload is None:
        return False
    try:
        metadata = json.loads(payload.decode("utf-8"))
        task_id = normalize_task_id(metadata.get("id"), field_path="task_artifact.id")
        generation = normalize_generation(
            metadata.get("lifecycle_generation", 0),
            field_path="task_artifact.lifecycle_generation",
        )
    except (UnicodeDecodeError, json.JSONDecodeError, AttributeError, LifecycleContractError):
        return False
    return (
        task_id == key.task_id
        and generation == key.lifecycle_generation
        and metadata.get("status") == expected_status
    )


def _candidate_id(branch_name: str, kind: CandidateKind, path: Path | None) -> str:
    identity = f"{branch_name}\0{kind}\0{path or ''}"
    return f"branch:{sha256(identity.encode('utf-8')).hexdigest()[:24]}"


def discover_branch_candidates(
    repository: RepositoryFacts,
    store: BranchBindingStore,
    ownership_port: OwnershipPort,
    *,
    key: TaskLifecycleKey,
    task_ref: str,
    expected_status: str,
    required_branch_name: str | None = None,
    allowed_current_revision: int | None = None,
) -> tuple[BranchCandidate, ...]:
    normalized_key = TaskLifecycleKey(key.task_id, key.lifecycle_generation)
    normalized_ref = normalize_task_ref(task_ref)
    required = normalize_branch_name(required_branch_name) if required_branch_name is not None else None
    candidates: list[BranchCandidate] = []
    registered_refs: set[str] = set()

    for facts in discover_worktree_facts(repository):
        branch_ref = facts.branch_ref or facts.registration.registered_branch_ref
        if branch_ref is None or not branch_ref.startswith("refs/heads/"):
            continue
        branch_name = normalize_branch_name(branch_ref.removeprefix("refs/heads/"))
        if required is not None and branch_name != required:
            continue
        registered_refs.add(branch_ref)
        reason: str | None = None
        if facts.inspection_error:
            reason = facts.inspection_error
        elif facts.common_dir != repository.common_dir:
            reason = "wrong_repository"
        elif facts.branch_ref != branch_ref or facts.head is None:
            reason = "branch_registration_mismatch"
        elif not _artifact_matches(
            repository,
            head=facts.head,
            task_ref=normalized_ref,
            key=normalized_key,
            expected_status=expected_status,
        ):
            reason = "task_artifact_mismatch"
        elif store.branch_owner(branch_name, excluding=normalized_key) is not None:
            reason = "branch_bound_to_other_task"
        elif ownership_port.branch_has_unresolved_incarnation(
            branch_name,
            key=normalized_key,
            allowed_current_revision=allowed_current_revision,
        ):
            reason = "unresolved_resource_incarnation"
        candidates.append(
            BranchCandidate(
                candidate_id=_candidate_id(branch_name, "registered_checkout", facts.path),
                branch_name=branch_name,
                head=facts.head or facts.registration.registered_head,
                kind="registered_checkout",
                checkout_path=facts.path,
                topology=facts.topology,
                valid=reason is None,
                reason_code=reason,
            )
        )

    for branch_ref, head in list_local_branch_refs(repository):
        if branch_ref in registered_refs:
            continue
        branch_name = normalize_branch_name(branch_ref.removeprefix("refs/heads/"))
        if required is not None and branch_name != required:
            continue
        reason = None
        if not _artifact_matches(
            repository,
            head=head,
            task_ref=normalized_ref,
            key=normalized_key,
            expected_status=expected_status,
        ):
            reason = "task_artifact_mismatch"
        elif store.branch_owner(branch_name, excluding=normalized_key) is not None:
            reason = "branch_bound_to_other_task"
        elif ownership_port.branch_has_unresolved_incarnation(
            branch_name,
            key=normalized_key,
            allowed_current_revision=allowed_current_revision,
        ):
            reason = "unresolved_resource_incarnation"
        candidates.append(
            BranchCandidate(
                candidate_id=_candidate_id(branch_name, "local_branch", None),
                branch_name=branch_name,
                head=head,
                kind="local_branch",
                checkout_path=None,
                topology=None,
                valid=reason is None,
                reason_code=reason,
            )
        )
    return tuple(sorted(candidates, key=lambda row: row.candidate_id))


def _control_state(
    store: BranchBindingStore,
    ownership_port: OwnershipPort,
    key: TaskLifecycleKey,
) -> tuple[BranchBinding | None, OwnershipCurrent | None]:
    binding = store.read(key)
    ownership = ownership_port.read_current(key)
    if ownership is not None and ownership.key != key:
        raise LifecycleContractError(
            "resource_ownership_conflict",
            "ownership.task_lifecycle_key",
            "Keep ownership current state bound to the requested task lifecycle key.",
        )
    if binding is not None and ownership is not None and (
        binding.branch_name != ownership.branch_name
        or binding.binding_revision != ownership.binding_revision
    ):
        raise LifecycleContractError(
            "branch_association_conflict",
            "control_state",
            "Repair the binding and ownership current branch/revision mismatch.",
        )
    return binding, ownership


def resolve_establishment(
    repository: RepositoryFacts,
    store: BranchBindingStore,
    ownership_port: OwnershipPort,
    *,
    key: TaskLifecycleKey,
    task_ref: str,
    expected_status: str,
) -> EstablishmentResolution:
    binding, ownership = _control_state(store, ownership_port, key)
    if binding is not None and ownership is not None:
        return EstablishmentResolution(
            "already_established",
            binding,
            ownership,
            (),
            None,
            "binding_and_ownership_current",
        )
    required = binding.branch_name if binding is not None else ownership.branch_name if ownership is not None else None
    revision = (
        binding.binding_revision
        if binding is not None
        else ownership.binding_revision
        if ownership is not None
        else None
    )
    candidates = discover_branch_candidates(
        repository,
        store,
        ownership_port,
        key=key,
        task_ref=task_ref,
        expected_status=expected_status,
        required_branch_name=required,
        allowed_current_revision=revision,
    )
    valid = tuple(row for row in candidates if row.valid)
    if len(valid) != 1:
        return EstablishmentResolution(
            "selection_required",
            binding,
            ownership,
            candidates,
            None,
            "zero_validated_candidates" if not valid else "multiple_validated_candidates",
        )
    return EstablishmentResolution(
        "candidate_resolved",
        binding,
        ownership,
        candidates,
        valid[0],
        "unique_validated_candidate",
    )


def establish_branch_binding(
    repository: RepositoryFacts,
    store: BranchBindingStore,
    ownership_port: OwnershipPort,
    *,
    key: TaskLifecycleKey,
    task_ref: str,
    expected_status: str,
    selected_candidate_id: str | None = None,
) -> EstablishmentResolution:
    resolution = resolve_establishment(
        repository,
        store,
        ownership_port,
        key=key,
        task_ref=task_ref,
        expected_status=expected_status,
    )
    if resolution.kind == "already_established":
        return resolution
    valid = resolution.valid_candidates
    if selected_candidate_id is not None:
        valid = tuple(row for row in valid if row.candidate_id == selected_candidate_id)
    if len(valid) != 1:
        return EstablishmentResolution(
            "selection_required",
            resolution.binding,
            resolution.ownership,
            resolution.candidates,
            None,
            "selected_candidate_stale" if selected_candidate_id is not None else resolution.reason_code,
        )
    selected = valid[0]
    if selected.kind == "local_branch":
        return EstablishmentResolution(
            "selection_required",
            resolution.binding,
            resolution.ownership,
            resolution.candidates,
            None,
            "checkout_acquisition_required",
        )
    binding_before = store.snapshot(key)
    ownership_before = ownership_port.snapshot(key)
    target_revision = (
        resolution.binding.binding_revision
        if resolution.binding is not None
        else resolution.ownership.binding_revision
        if resolution.ownership is not None
        else 0
    )
    try:
        binding = resolution.binding or store.establish(
            key,
            selected.branch_name,
            binding_revision=target_revision,
        )
        ownership = resolution.ownership
        if ownership is None:
            worktree_ownership: Ownership = (
                "not_applicable"
                if selected.kind == "local_branch" or selected.topology == "primary"
                else "caller_owned"
            )
            ownership = ownership_port.establish_current(
                key,
                binding_revision=target_revision,
                branch_name=selected.branch_name,
                branch_ownership="caller_owned",
                worktree_ownership=worktree_ownership,
            )
        current_binding, current_ownership = _control_state(store, ownership_port, key)
        if current_binding != binding or current_ownership != ownership:
            raise LifecycleContractError(
                "branch_association_conflict",
                "post_state",
                "Restore the exact control-state transaction and repeat establishment.",
            )
        return EstablishmentResolution(
            "binding_established",
            current_binding,
            current_ownership,
            resolution.candidates,
            selected,
            "binding_established",
        )
    except Exception:
        try:
            ownership_port.restore(key, ownership_before)
        finally:
            store.restore(binding_before)
        raise


def recover_established_branch_binding(
    repository: RepositoryFacts,
    store: BranchBindingStore,
    ownership_port: OwnershipPort,
    *,
    key: TaskLifecycleKey,
    task_ref: str,
    expected_status: str,
    expected_revision: int,
    expected_branch_name: str,
) -> EstablishmentResolution:
    binding, ownership = _control_state(store, ownership_port, key)
    expected_branch = normalize_branch_name(expected_branch_name)
    if (
        binding is None
        or ownership is None
        or binding.binding_revision != expected_revision
        or binding.branch_name != expected_branch
    ):
        raise LifecycleContractError(
            "branch_binding_result_mismatch",
            "post_state",
            "Recover only the exact established binding and ownership result.",
        )
    candidates = discover_branch_candidates(
        repository,
        store,
        ownership_port,
        key=key,
        task_ref=task_ref,
        expected_status=expected_status,
        required_branch_name=expected_branch,
        allowed_current_revision=expected_revision,
    )
    valid = tuple(row for row in candidates if row.valid)
    if len(valid) != 1:
        raise LifecycleContractError(
            "branch_binding_result_mismatch",
            "candidate",
            "Recover only an exact unique live branch candidate for the established result.",
        )
    return EstablishmentResolution(
        "binding_established",
        binding,
        ownership,
        candidates,
        valid[0],
        "binding_establishment_recovered",
    )


__all__ = [
    "BranchCandidate",
    "EstablishmentResolution",
    "Ownership",
    "OwnershipCurrent",
    "OwnershipPort",
    "discover_branch_candidates",
    "establish_branch_binding",
    "recover_established_branch_binding",
    "resolve_establishment",
]
