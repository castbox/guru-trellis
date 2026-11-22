from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .branch_store import BranchBinding, BranchBindingStore, TaskLifecycleKey
from .errors import LifecycleContractError
from .git_facts import (
    RepositoryFacts, WorktreeFacts, find_registration, inspect_registered_worktree,
    inspect_repository, list_worktree_registrations,
)
from .identity import TaskArtifactIdentity, resolve_task_ref
from .resource_ledger import ResourceLedgerStore


@dataclass(frozen=True)
class ActiveTaskCheckout:
    artifact: TaskArtifactIdentity
    branch_name: str


def read_bound_checkout(repository: RepositoryFacts, key: TaskLifecycleKey) -> tuple[BranchBinding, WorktreeFacts]:
    """Read the exact C4/C5 checkout relationship for a known lifecycle."""
    binding = BranchBindingStore(repository).read(key)
    ownership = ResourceLedgerStore(repository).read_current(key) if binding is not None else None
    if binding is None or ownership is None:
        raise LifecycleContractError("binding_required", "branch_binding",
                                     "Establish the current branch binding and resource ownership.")
    if (ownership.binding_revision, ownership.branch_name) != (binding.binding_revision, binding.branch_name):
        raise LifecycleContractError("binding_ownership_mismatch", "resource_ledger",
                                     "Resolve the conflicting branch association through the original branch owner.")
    registrations = list_worktree_registrations(repository)
    candidates = [row for row in registrations if row.registered_branch_ref == binding.branch_ref]
    if not candidates:
        raise LifecycleContractError("checkout_required", "checkout",
                                     "Acquire or recover the registered checkout through the original owner.")
    if len(candidates) != 1:
        raise LifecycleContractError("ambiguous_checkout", "checkout",
                                     "Resolve the multiple registered checkouts for the bound branch.")
    current = inspect_registered_worktree(repository, candidates[0], registrations=registrations, include_dirty=False)
    if (current.inspection_error or current.common_dir != repository.common_dir
            or current.branch_ref != binding.branch_ref):
        raise LifecycleContractError("checkout_identity_mismatch", "checkout",
                                     "Use the registered checkout of the current bound branch.")
    return binding, current


def resolve_active_task_checkout(repo_root: Path, task_ref: str) -> ActiveTaskCheckout:
    artifact = resolve_task_ref(repo_root, task_ref)
    if artifact.lifecycle_state != "active":
        raise LifecycleContractError("task_not_active", "task_ref", "Use one active task artifact.")
    repository = inspect_repository(repo_root)
    binding = BranchBindingStore(repository).read(TaskLifecycleKey(artifact.task_id, artifact.lifecycle_generation))
    if binding is None:
        raise LifecycleContractError("branch_binding_missing", "branch_binding", "Establish the current task branch binding.")
    registration = find_registration(repository, repo_root)
    if registration is None:
        raise LifecycleContractError("worktree_not_registered", "worktree", "Use the registered task checkout.")
    checkout = inspect_registered_worktree(repository, registration)
    if (checkout.inspection_error or checkout.common_dir != repository.common_dir
            or checkout.branch_ref != binding.branch_ref
            or registration.registered_branch_ref != binding.branch_ref
            or checkout.head != registration.registered_head):
        raise LifecycleContractError("task_checkout_stale", "worktree", "Use the task branch checked out in this worktree.")
    return ActiveTaskCheckout(artifact, binding.branch_name)
