from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

from .checkout_resolution import (
    CheckoutRequest,
    CheckoutResolution,
    canonical_head_ref,
    discover_validate_classify,
)
from .errors import LifecycleContractError
from .git_facts import (
    WorktreeFacts,
    branch_checked_out_paths,
    find_registration,
    inspect_registered_worktree,
    inspect_repository,
    local_branch_head,
    run_common_git,
)


AcquisitionRoute = Literal["adopt_invocation_checkout", "provision_linked_worktree"]
Ownership = Literal["guru_owned", "caller_owned", "not_applicable"]
ProvisionDisposition = Literal["new_branch", "existing_branch", "existing_checkout"]


@dataclass(frozen=True)
class CheckoutAcquisitionPlan:
    route: AcquisitionRoute
    repository_context: Path
    task_id: str
    task_ref: str
    lifecycle_generation: int
    branch_ref: str
    expected_status: str
    decision_head: str
    transaction_id: str
    result_id: str
    provision_disposition: ProvisionDisposition | None = None
    invocation_checkout: Path | None = None
    target_path: Path | None = None
    forbidden_branch_refs: tuple[str, ...] = ()
    clean_required: bool = True
    task_artifact_expectation: str = "required"

    def request(self) -> CheckoutRequest:
        return CheckoutRequest(
            repository=inspect_repository(self.repository_context),
            task_id=self.task_id,
            task_ref=self.task_ref,
            lifecycle_generation=self.lifecycle_generation,
            branch_ref=self.branch_ref,
            expected_status=self.expected_status,
            expected_head=self.decision_head,
            clean_required=self.clean_required,
            forbidden_branch_refs=self.forbidden_branch_refs,
            task_artifact_expectation=self.task_artifact_expectation,
        )


@dataclass(frozen=True)
class CheckoutAcquisitionResult:
    route: AcquisitionRoute
    action: str
    checkout: WorktreeFacts
    transaction_id: str
    result_id: str
    branch_ownership: Ownership
    worktree_ownership: Ownership
    created_branch: bool
    created_worktree: bool


def _require_identifier(value: str, field_path: str) -> str:
    if not isinstance(value, str) or not value or any(character.isspace() for character in value):
        raise LifecycleContractError(
            "invalid_transaction_identity",
            field_path,
            "Use one non-empty call-local transaction or result identity without whitespace.",
        )
    return value


def _validated_plan(plan: CheckoutAcquisitionPlan) -> CheckoutRequest:
    if plan.route not in {"adopt_invocation_checkout", "provision_linked_worktree"}:
        raise LifecycleContractError(
            "invalid_acquisition_route",
            "route",
            "Use adopt_invocation_checkout or provision_linked_worktree.",
        )
    _require_identifier(plan.transaction_id, "transaction_id")
    _require_identifier(plan.result_id, "result_id")
    if plan.route == "provision_linked_worktree" and plan.provision_disposition not in {
        "new_branch",
        "existing_branch",
        "existing_checkout",
    }:
        raise LifecycleContractError(
            "missing_provision_disposition",
            "provision_disposition",
            "Bind the reviewed live pre-state as new_branch, existing_branch or existing_checkout.",
        )
    if plan.route == "adopt_invocation_checkout" and plan.provision_disposition is not None:
        raise LifecycleContractError(
            "invalid_adopt_plan",
            "provision_disposition",
            "Do not attach a provision disposition to the adopt route.",
        )
    return plan.request()


def _raise_resolution(resolution: CheckoutResolution) -> None:
    raise LifecycleContractError(
        resolution.reason_code,
        "checkout_resolution",
        "Resolve the current checkout authority conflict or select a freshly validated target.",
        {
            "resolution_kind": resolution.kind,
            "candidate_reasons": [row.reason_code for row in resolution.candidates if row.reason_code],
        },
    )


def adopt_invocation_checkout(plan: CheckoutAcquisitionPlan) -> CheckoutAcquisitionResult:
    request = _validated_plan(plan)
    if plan.route != "adopt_invocation_checkout" or plan.invocation_checkout is None:
        raise LifecycleContractError(
            "invalid_adopt_plan",
            "invocation_checkout",
            "Provide the current invocation checkout for the adopt route.",
        )
    resolution = discover_validate_classify(request)
    if resolution.kind != "checkout_resolved" or resolution.selected is None:
        _raise_resolution(resolution)
    checkout = resolution.selected.facts
    if checkout.path != plan.invocation_checkout.resolve():
        raise LifecycleContractError(
            "invocation_checkout_not_unique_candidate",
            "invocation_checkout",
            "Use the unique freshly validated invocation checkout or return to reviewed selection.",
            {"reviewed": str(plan.invocation_checkout.resolve()), "live": str(checkout.path)},
        )
    return CheckoutAcquisitionResult(
        route=plan.route,
        action=f"adopted_{checkout.topology}_checkout",
        checkout=checkout,
        transaction_id=plan.transaction_id,
        result_id=plan.result_id,
        branch_ownership="caller_owned",
        worktree_ownership="not_applicable" if checkout.topology == "primary" else "caller_owned",
        created_branch=False,
        created_worktree=False,
    )


def _exact_post_state(request: CheckoutRequest, target_path: Path | None = None) -> WorktreeFacts:
    resolution = discover_validate_classify(request)
    if resolution.kind != "checkout_resolved" or resolution.selected is None:
        _raise_resolution(resolution)
    facts = resolution.selected.facts
    if target_path is not None and facts.path != target_path.resolve():
        raise LifecycleContractError(
            "acquisition_result_mismatch",
            "target_path",
            "Recover the exact transaction target or repeat semantic target selection.",
            {"expected": str(target_path.resolve()), "actual": str(facts.path)},
        )
    return facts


def _rollback_created(
    request: CheckoutRequest,
    *,
    target_path: Path,
    created_branch: bool,
    created_worktree: bool,
) -> None:
    if created_worktree:
        registration = find_registration(request.repository, target_path)
        if registration is not None:
            facts = inspect_registered_worktree(request.repository, registration)
            exact = (
                facts.common_dir == request.repository.common_dir
                and facts.branch_ref == request.branch_ref
                and facts.head == request.expected_head
                and facts.clean
            )
            if exact:
                run_common_git(request.repository, ["worktree", "remove", str(target_path.resolve())])
    if created_branch:
        current = local_branch_head(request.repository, request.branch_ref)
        checked_out = branch_checked_out_paths(request.repository, request.branch_ref)
        if current == request.expected_head and not checked_out:
            run_common_git(request.repository, ["update-ref", "-d", request.branch_ref, request.expected_head or ""])


def provision_linked_worktree(
    plan: CheckoutAcquisitionPlan,
    *,
    post_acquire: Callable[[CheckoutAcquisitionResult], None] | None = None,
) -> CheckoutAcquisitionResult:
    request = _validated_plan(plan)
    if plan.route != "provision_linked_worktree":
        raise LifecycleContractError(
            "invalid_provision_plan",
            "route",
            "Use provision_linked_worktree for linked checkout acquisition.",
        )
    resolution = discover_validate_classify(request)
    if resolution.kind == "authority_conflict":
        _raise_resolution(resolution)
    if resolution.kind == "checkout_resolved" and resolution.selected is not None:
        if plan.provision_disposition != "existing_checkout":
            raise LifecycleContractError(
                "provision_pre_state_changed",
                "provision_disposition",
                "Repeat semantic review against the fresh existing-checkout topology.",
            )
        if plan.target_path is not None and resolution.selected.facts.path != plan.target_path.resolve():
            raise LifecycleContractError(
                "provision_pre_state_changed",
                "target_path",
                "Repeat semantic review for the exact freshly resolved checkout path.",
                {"reviewed": str(plan.target_path.resolve()), "live": str(resolution.selected.facts.path)},
            )
        result = CheckoutAcquisitionResult(
            route=plan.route,
            action="reused_exact_checkout",
            checkout=resolution.selected.facts,
            transaction_id=plan.transaction_id,
            result_id=plan.result_id,
            branch_ownership="caller_owned",
            worktree_ownership=(
                "not_applicable" if resolution.selected.facts.topology == "primary" else "caller_owned"
            ),
            created_branch=False,
            created_worktree=False,
        )
        if post_acquire is not None:
            post_acquire(result)
        return result
    branch_candidates = [
        row
        for row in resolution.candidates
        if row.facts.registration.registered_branch_ref == request.branch_ref
    ]
    if branch_candidates:
        _raise_resolution(resolution)
    if plan.target_path is None:
        raise LifecycleContractError(
            "missing_target_path",
            "target_path",
            "Provide one reviewed call-local linked-worktree target path.",
        )
    target = plan.target_path.resolve()
    if target.exists() or find_registration(request.repository, target) is not None:
        raise LifecycleContractError(
            "target_path_conflict",
            "target_path",
            "Choose an absent path or the exact registered checkout selected for reuse.",
            {"target_path": str(target)},
        )
    existing_head = local_branch_head(request.repository, request.branch_ref)
    if existing_head is not None and existing_head != request.expected_head:
        raise LifecycleContractError(
            "head_drift",
            "decision_head",
            "Refresh the reviewed branch and decision HEAD before provisioning.",
            {"expected": request.expected_head, "actual": existing_head},
        )
    created_branch = existing_head is None
    live_disposition: ProvisionDisposition = "new_branch" if created_branch else "existing_branch"
    if plan.provision_disposition != live_disposition:
        raise LifecycleContractError(
            "provision_pre_state_changed",
            "provision_disposition",
            "Repeat semantic review against the fresh branch and checkout facts.",
            {"reviewed": plan.provision_disposition, "live": live_disposition},
        )
    created_worktree = False
    try:
        if created_branch:
            short_branch = request.branch_ref.removeprefix("refs/heads/")
            run_common_git(
                request.repository,
                ["worktree", "add", "-b", short_branch, str(target), request.expected_head or ""],
            )
        else:
            short_branch = request.branch_ref.removeprefix("refs/heads/")
            run_common_git(request.repository, ["worktree", "add", str(target), short_branch])
        created_worktree = True
        checkout = _exact_post_state(request, target)
        result = CheckoutAcquisitionResult(
            route=plan.route,
            action="created_branch_and_worktree" if created_branch else "created_worktree_for_existing_branch",
            checkout=checkout,
            transaction_id=plan.transaction_id,
            result_id=plan.result_id,
            branch_ownership="guru_owned" if created_branch else "caller_owned",
            worktree_ownership="guru_owned",
            created_branch=created_branch,
            created_worktree=True,
        )
        if post_acquire is not None:
            post_acquire(result)
        return result
    except Exception:
        _rollback_created(
            request,
            target_path=target,
            created_branch=created_branch,
            created_worktree=created_worktree,
        )
        raise


def recover_checkout_acquisition(plan: CheckoutAcquisitionPlan) -> CheckoutAcquisitionResult:
    request = _validated_plan(plan)
    if plan.route == "adopt_invocation_checkout":
        return adopt_invocation_checkout(plan)
    checkout = _exact_post_state(request)
    target = plan.target_path.resolve() if plan.target_path is not None else None
    if target is not None and checkout.path != target:
        moved_registration = find_registration(request.repository, checkout.path)
        if moved_registration is None:
            raise LifecycleContractError(
                "acquisition_result_mismatch",
                "target_path",
                "Recover only the exact live checkout for this transaction.",
            )
    assert plan.provision_disposition is not None
    branch_ownership: Ownership = "caller_owned"
    worktree_ownership: Ownership
    if plan.provision_disposition == "existing_checkout":
        worktree_ownership = "not_applicable" if checkout.topology == "primary" else "caller_owned"
    else:
        worktree_ownership = "caller_owned"
    return CheckoutAcquisitionResult(
        route=plan.route,
        action="rematerialized_unproven_resource_result",
        checkout=checkout,
        transaction_id=plan.transaction_id,
        result_id=plan.result_id,
        branch_ownership=branch_ownership,
        worktree_ownership=worktree_ownership,
        created_branch=False,
        created_worktree=False,
    )


def acquire_checkout(
    plan: CheckoutAcquisitionPlan,
    *,
    post_acquire: Callable[[CheckoutAcquisitionResult], None] | None = None,
) -> CheckoutAcquisitionResult:
    canonical_head_ref(plan.branch_ref)
    if plan.route == "adopt_invocation_checkout":
        result = adopt_invocation_checkout(plan)
        if post_acquire is not None:
            post_acquire(result)
        return result
    return provision_linked_worktree(plan, post_acquire=post_acquire)


__all__ = [
    "CheckoutAcquisitionPlan",
    "CheckoutAcquisitionResult",
    "acquire_checkout",
    "adopt_invocation_checkout",
    "provision_linked_worktree",
    "recover_checkout_acquisition",
]
