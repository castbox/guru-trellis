from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

from .branch_resolution import Ownership, OwnershipCurrent, OwnershipPort
from .branch_store import BranchBinding, BranchBindingStore, TaskLifecycleKey, normalize_branch_name
from .errors import LifecycleContractError
from .git_facts import (
    CheckoutStateSnapshot,
    RepositoryFacts,
    branch_checked_out_paths,
    capture_checkout_state,
    find_registration,
    git_operation_in_progress,
    inspect_registered_worktree,
    is_ancestor,
    local_branch_head,
    run_checkout_git,
    run_common_git,
)
from .identity import normalize_generation, normalize_task_id, normalize_task_ref


RebindRoute = Literal["same_checkout_new_ref", "existing_target"]


@dataclass(frozen=True)
class RebindPlan:
    route: RebindRoute
    key: TaskLifecycleKey
    task_ref: str
    expected_status: str
    current_checkout: Path
    target_branch_name: str
    expected_revision: int
    pre_state: CheckoutStateSnapshot
    target_checkout: Path | None = None
    target_head: str | None = None

    def __post_init__(self) -> None:
        if self.route not in {"same_checkout_new_ref", "existing_target"}:
            raise LifecycleContractError(
                "invalid_rebind_route",
                "route",
                "Use same_checkout_new_ref or existing_target.",
            )
        object.__setattr__(
            self,
            "key",
            TaskLifecycleKey(self.key.task_id, self.key.lifecycle_generation),
        )
        object.__setattr__(self, "task_ref", normalize_task_ref(self.task_ref))
        object.__setattr__(self, "current_checkout", self.current_checkout.resolve())
        object.__setattr__(self, "target_branch_name", normalize_branch_name(self.target_branch_name))
        if type(self.expected_revision) is not int or self.expected_revision < 0:
            raise LifecycleContractError(
                "invalid_binding_revision",
                "expected_revision",
                "Use the current non-negative binding revision.",
            )
        if self.target_checkout is not None:
            object.__setattr__(self, "target_checkout", self.target_checkout.resolve())


@dataclass(frozen=True)
class RebindResult:
    route: RebindRoute
    binding: BranchBinding
    ownership: OwnershipCurrent
    checkout_path: Path
    head: str
    recovered: bool = False


def _working_artifact_matches(
    checkout: Path,
    *,
    task_ref: str,
    key: TaskLifecycleKey,
    expected_status: str,
) -> bool:
    path = checkout / task_ref / "task.json"
    try:
        if path.is_symlink() or not path.is_file():
            return False
        payload = json.loads(path.read_text(encoding="utf-8"))
        task_id = normalize_task_id(payload.get("id"), field_path="task_artifact.id")
        generation = normalize_generation(
            payload.get("lifecycle_generation", 0),
            field_path="task_artifact.lifecycle_generation",
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, AttributeError, LifecycleContractError):
        return False
    return (
        task_id == key.task_id
        and generation == key.lifecycle_generation
        and payload.get("status") == expected_status
    )


def _current_control_state(
    store: BranchBindingStore,
    ownership_port: OwnershipPort,
    key: TaskLifecycleKey,
) -> tuple[BranchBinding, OwnershipCurrent]:
    binding = store.read(key)
    if binding is None:
        raise LifecycleContractError(
            "branch_binding_required",
            "branch_binding",
            "Establish the missing current branch association before rebind.",
        )
    ownership = ownership_port.read_current(key)
    if ownership is None:
        raise LifecycleContractError(
            "resource_ownership_required",
            "ownership",
            "Establish conservative current ownership before rebind.",
        )
    if (
        ownership.key != key
        or ownership.binding_revision != binding.binding_revision
        or ownership.branch_name != binding.branch_name
    ):
        raise LifecycleContractError(
            "branch_association_conflict",
            "control_state",
            "Repair the binding and ownership current branch/revision mismatch.",
        )
    return binding, ownership


def _registered_facts(repository: RepositoryFacts, checkout: Path):
    registration = find_registration(repository, checkout)
    if registration is None:
        raise LifecycleContractError(
            "checkout_not_registered",
            "checkout",
            "Use one live registered checkout from the current repository.",
        )
    facts = inspect_registered_worktree(repository, registration)
    if facts.inspection_error or facts.common_dir != repository.common_dir:
        raise LifecycleContractError(
            "checkout_authority_conflict",
            "checkout",
            "Repair the registered checkout before branch rebind.",
        )
    return facts


def prepare_rebind(
    repository: RepositoryFacts,
    store: BranchBindingStore,
    ownership_port: OwnershipPort,
    *,
    route: RebindRoute,
    key: TaskLifecycleKey,
    task_ref: str,
    expected_status: str,
    current_checkout: Path | str,
    target_branch_name: str,
) -> RebindPlan:
    binding, _ = _current_control_state(store, ownership_port, key)
    current_path = Path(current_checkout).resolve()
    current = _registered_facts(repository, current_path)
    if current.branch_ref != binding.branch_ref:
        raise LifecycleContractError(
            "branch_association_conflict",
            "current_checkout",
            "Use the unique checkout bound to the current TaskBranchBinding.",
        )
    if git_operation_in_progress(current_path):
        raise LifecycleContractError(
            "git_operation_in_progress",
            "current_checkout",
            "Finish or abort the current Git operation before rebind.",
        )
    if not _working_artifact_matches(
        current_path,
        task_ref=task_ref,
        key=key,
        expected_status=expected_status,
    ):
        raise LifecycleContractError(
            "task_artifact_mismatch",
            "current_checkout",
            "Use the current checkout containing the exact active task artifact.",
        )
    target = normalize_branch_name(target_branch_name)
    if target == binding.branch_name:
        raise LifecycleContractError(
            "already_bound",
            "target_branch_name",
            "Choose a different target branch or recover the existing binding result.",
        )
    if store.branch_owner(target, excluding=key) is not None:
        raise LifecycleContractError(
            "branch_already_bound",
            "target_branch_name",
            "Choose a branch not bound to another active task lifecycle.",
        )
    if ownership_port.branch_has_unresolved_incarnation(
        target,
        key=key,
        allowed_current_revision=None,
    ):
        raise LifecycleContractError(
            "unresolved_resource_incarnation",
            "target_branch_name",
            "Resolve the prior resource responsibility before reusing this Git ref.",
        )
    pre_state = capture_checkout_state(current_path)
    if pre_state.branch_ref != binding.branch_ref:
        raise LifecycleContractError(
            "branch_association_conflict",
            "current_checkout",
            "Repeat rebind planning against the fresh current branch.",
        )

    if route == "same_checkout_new_ref":
        target_ref = f"refs/heads/{target}"
        if local_branch_head(repository, target_ref) is not None or branch_checked_out_paths(repository, target_ref):
            raise LifecycleContractError(
                "target_branch_exists",
                "target_branch_name",
                "Use a branch name absent from local refs and registered checkouts.",
            )
        return RebindPlan(
            route=route,
            key=key,
            task_ref=task_ref,
            expected_status=expected_status,
            current_checkout=current_path,
            target_branch_name=target,
            expected_revision=binding.binding_revision,
            pre_state=pre_state,
            target_head=pre_state.head,
        )

    if route != "existing_target":
        raise LifecycleContractError(
            "invalid_rebind_route",
            "route",
            "Use same_checkout_new_ref or existing_target.",
        )
    if not current.clean:
        raise LifecycleContractError(
            "dirty_checkout",
            "current_checkout",
            "Use same_checkout_new_ref for dirty state or establish a clean existing-target boundary.",
        )
    target_ref = f"refs/heads/{target}"
    target_paths = branch_checked_out_paths(repository, target_ref)
    if len(target_paths) != 1:
        raise LifecycleContractError(
            "target_checkout_not_unique",
            "target_branch_name",
            "Use one uniquely registered target checkout for existing_target.",
        )
    target_facts = _registered_facts(repository, target_paths[0])
    if not target_facts.clean or target_facts.head is None:
        raise LifecycleContractError(
            "target_checkout_not_clean",
            "target_checkout",
            "Use one clean exact target checkout.",
        )
    if not _working_artifact_matches(
        target_facts.path,
        task_ref=task_ref,
        key=key,
        expected_status=expected_status,
    ):
        raise LifecycleContractError(
            "task_artifact_mismatch",
            "target_checkout",
            "Use a target containing the exact active task artifact.",
        )
    if not is_ancestor(repository, pre_state.head, target_facts.head):
        raise LifecycleContractError(
            "rebind_reconcile_required",
            "target_branch_name",
            "Reconcile histories explicitly before existing-target rebind.",
        )
    return RebindPlan(
        route=route,
        key=key,
        task_ref=task_ref,
        expected_status=expected_status,
        current_checkout=current_path,
        target_branch_name=target,
        expected_revision=binding.binding_revision,
        pre_state=pre_state,
        target_checkout=target_facts.path,
        target_head=target_facts.head,
    )


def _assert_same_content(expected: CheckoutStateSnapshot, actual: CheckoutStateSnapshot) -> None:
    if (
        expected.path != actual.path
        or expected.head != actual.head
        or expected.index_sha256 != actual.index_sha256
        or expected.worktree_sha256 != actual.worktree_sha256
        or expected.status_sha256 != actual.status_sha256
    ):
        raise LifecycleContractError(
            "same_checkout_content_changed",
            "current_checkout",
            "Restore exact HEAD, index and working-tree bytes before continuing rebind.",
        )


def _fresh_plan_matches(expected: RebindPlan, actual: RebindPlan) -> bool:
    return (
        expected.route == actual.route
        and expected.key == actual.key
        and expected.task_ref == actual.task_ref
        and expected.expected_status == actual.expected_status
        and expected.current_checkout == actual.current_checkout
        and expected.target_branch_name == actual.target_branch_name
        and expected.expected_revision == actual.expected_revision
        and expected.pre_state == actual.pre_state
        and expected.target_checkout == actual.target_checkout
        and expected.target_head == actual.target_head
    )


def _rollback_same_checkout(
    repository: RepositoryFacts,
    plan: RebindPlan,
) -> None:
    state = capture_checkout_state(plan.current_checkout)
    target_ref = f"refs/heads/{plan.target_branch_name}"
    if state.branch_ref == target_ref:
        run_checkout_git(plan.current_checkout, ["switch", plan.pre_state.branch_ref.removeprefix("refs/heads/")])
    target_head = local_branch_head(repository, target_ref)
    if target_head == plan.pre_state.head and not branch_checked_out_paths(repository, target_ref):
        run_common_git(repository, ["update-ref", "-d", target_ref, plan.pre_state.head])
    restored = capture_checkout_state(plan.current_checkout)
    _assert_same_content(plan.pre_state, restored)
    if restored.branch_ref != plan.pre_state.branch_ref:
        raise LifecycleContractError(
            "rebind_rollback_failed",
            "current_checkout",
            "Restore the exact source branch after failed rebind.",
        )


def execute_rebind(
    repository: RepositoryFacts,
    store: BranchBindingStore,
    ownership_port: OwnershipPort,
    plan: RebindPlan,
    *,
    post_mutation: Callable[[RebindResult], None] | None = None,
) -> RebindResult:
    fresh = prepare_rebind(
        repository,
        store,
        ownership_port,
        route=plan.route,
        key=plan.key,
        task_ref=plan.task_ref,
        expected_status=plan.expected_status,
        current_checkout=plan.current_checkout,
        target_branch_name=plan.target_branch_name,
    )
    if not _fresh_plan_matches(plan, fresh):
        raise LifecycleContractError(
            "rebind_plan_stale",
            "plan",
            "Repeat semantic review against fresh binding, ownership and Git facts.",
        )
    binding_before = store.snapshot(plan.key)
    ownership_before = ownership_port.snapshot(plan.key)
    branch_created = False
    try:
        if plan.route == "same_checkout_new_ref":
            run_checkout_git(plan.current_checkout, ["switch", "-c", plan.target_branch_name])
            branch_created = True
            after_switch = capture_checkout_state(plan.current_checkout)
            _assert_same_content(plan.pre_state, after_switch)
            if after_switch.branch_ref != f"refs/heads/{plan.target_branch_name}":
                raise LifecycleContractError(
                    "rebind_post_state_mismatch",
                    "current_checkout",
                    "Switch only to the reviewed target branch.",
                )
            checkout_path = plan.current_checkout
            target_branch_ownership: Ownership = "guru_owned"
            target_worktree_ownership: Ownership | None = None
            worktree_reassociated = True
        else:
            assert plan.target_checkout is not None and plan.target_head is not None
            checkout_path = plan.target_checkout
            target_facts = _registered_facts(repository, checkout_path)
            if target_facts.head != plan.target_head or not target_facts.clean:
                raise LifecycleContractError(
                    "rebind_plan_stale",
                    "target_checkout",
                    "Repeat semantic review against the fresh exact target checkout.",
                )
            target_branch_ownership = "caller_owned"
            target_worktree_ownership = (
                "not_applicable" if target_facts.topology == "primary" else "caller_owned"
            )
            worktree_reassociated = False

        ownership = ownership_port.rebind_current(
            plan.key,
            expected_revision=plan.expected_revision,
            source_branch_name=plan.pre_state.branch_ref.removeprefix("refs/heads/"),
            target_branch_name=plan.target_branch_name,
            expected_cleanup_head=plan.pre_state.head,
            target_branch_ownership=target_branch_ownership,
            target_worktree_ownership=target_worktree_ownership,
            worktree_reassociated=worktree_reassociated,
        )
        binding = store.advance(
            plan.key,
            expected_revision=plan.expected_revision,
            branch_name=plan.target_branch_name,
        )
        if (
            ownership.binding_revision != binding.binding_revision
            or ownership.branch_name != binding.branch_name
        ):
            raise LifecycleContractError(
                "branch_association_conflict",
                "post_state",
                "Keep rebind ownership and TaskBranchBinding revision/branch equal.",
            )
        result = RebindResult(
            route=plan.route,
            binding=binding,
            ownership=ownership,
            checkout_path=checkout_path,
            head=plan.target_head or plan.pre_state.head,
        )
        if post_mutation is not None:
            post_mutation(result)
        return result
    except Exception as original:
        rollback_error: Exception | None = None
        try:
            ownership_port.restore(plan.key, ownership_before)
            store.restore(binding_before)
            if branch_created:
                _rollback_same_checkout(repository, plan)
        except Exception as exc:
            rollback_error = exc
        if rollback_error is not None:
            raise LifecycleContractError(
                "rebind_rollback_failed",
                "transaction",
                "Resume the same rebind transaction until exact pre-state is restored.",
            ) from rollback_error
        raise original


def recover_rebind(
    repository: RepositoryFacts,
    store: BranchBindingStore,
    ownership_port: OwnershipPort,
    plan: RebindPlan,
) -> RebindResult:
    binding, ownership = _current_control_state(store, ownership_port, plan.key)
    if (
        binding.binding_revision != plan.expected_revision + 1
        or binding.branch_name != plan.target_branch_name
    ):
        raise LifecycleContractError(
            "rebind_result_mismatch",
            "control_state",
            "Recover only the exact successor revision and target branch.",
        )
    if plan.route == "same_checkout_new_ref":
        state = capture_checkout_state(plan.current_checkout)
        _assert_same_content(plan.pre_state, state)
        if state.branch_ref != binding.branch_ref:
            raise LifecycleContractError(
                "rebind_result_mismatch",
                "current_checkout",
                "Recover only the exact same-checkout target branch result.",
            )
        checkout_path = plan.current_checkout
        head = state.head
    else:
        if plan.target_checkout is None or plan.target_head is None:
            raise LifecycleContractError(
                "rebind_result_mismatch",
                "plan",
                "Recover existing_target only from its exact reviewed target facts.",
            )
        target = _registered_facts(repository, plan.target_checkout)
        if (
            target.branch_ref != binding.branch_ref
            or target.head != plan.target_head
            or not target.clean
            or not _working_artifact_matches(
                target.path,
                task_ref=plan.task_ref,
                key=plan.key,
                expected_status=plan.expected_status,
            )
            or not is_ancestor(repository, plan.pre_state.head, plan.target_head)
        ):
            raise LifecycleContractError(
                "rebind_result_mismatch",
                "target_checkout",
                "Recover only the exact clean artifact-compatible target result.",
            )
        checkout_path = target.path
        head = target.head
    return RebindResult(
        route=plan.route,
        binding=binding,
        ownership=ownership,
        checkout_path=checkout_path,
        head=head,
        recovered=True,
    )


__all__ = [
    "RebindPlan",
    "RebindResult",
    "execute_rebind",
    "prepare_rebind",
    "recover_rebind",
]
