from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .branch_store import BranchBindingStore, TaskLifecycleKey
from .errors import LifecycleContractError
from .git_facts import find_registration, inspect_registered_worktree, inspect_repository
from .identity import TaskArtifactIdentity, resolve_task_ref


@dataclass(frozen=True)
class ActiveTaskCheckout:
    artifact: TaskArtifactIdentity
    branch_name: str


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
