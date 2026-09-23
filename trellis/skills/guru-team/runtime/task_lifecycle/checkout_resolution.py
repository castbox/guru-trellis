from __future__ import annotations

import json
from hashlib import sha256
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from .errors import LifecycleContractError
from .git_facts import (
    RepositoryFacts,
    WorktreeFacts,
    discover_worktree_facts,
    find_registration,
    inspect_registered_worktree,
    inspect_repository,
)
from .identity import normalize_generation, normalize_task_id, normalize_task_ref, task_inventory
from .source import normalize_branch_ref


CandidateStatus = Literal["valid", "invalid_candidate", "authority_conflict"]
ResolutionKind = Literal["checkout_resolved", "selection_required", "authority_conflict"]
TaskArtifactExpectation = Literal["required", "absent"]


def canonical_head_ref(value: Any, *, field_path: str = "branch_ref") -> str:
    normalized = normalize_branch_ref(value, field_path=field_path)
    return normalized if normalized.startswith("refs/heads/") else f"refs/heads/{normalized}"


@dataclass(frozen=True)
class CheckoutRequest:
    repository: RepositoryFacts
    task_id: str
    task_ref: str
    lifecycle_generation: int
    branch_ref: str
    expected_status: str
    expected_head: str | None = None
    forbidden_branch_refs: tuple[str, ...] = ()
    task_artifact_expectation: TaskArtifactExpectation = "required"

    def __post_init__(self) -> None:
        object.__setattr__(self, "task_id", normalize_task_id(self.task_id))
        object.__setattr__(self, "task_ref", normalize_task_ref(self.task_ref))
        object.__setattr__(self, "lifecycle_generation", normalize_generation(self.lifecycle_generation))
        object.__setattr__(self, "branch_ref", canonical_head_ref(self.branch_ref))
        forbidden = tuple(canonical_head_ref(item, field_path="forbidden_branch_refs") for item in self.forbidden_branch_refs)
        object.__setattr__(self, "forbidden_branch_refs", forbidden)
        if self.branch_ref in forbidden:
            raise LifecycleContractError(
                "delivery_or_base_branch_forbidden",
                "branch_ref",
                "Choose a task branch distinct from the reviewed Delivery target and selected base.",
            )
        if self.expected_head is not None and (
            not isinstance(self.expected_head, str)
            or len(self.expected_head) != 40
            or any(character not in "0123456789abcdef" for character in self.expected_head)
        ):
            raise LifecycleContractError(
                "invalid_expected_head",
                "expected_head",
                "Use one lowercase 40-hex reviewed commit identity.",
            )
        if not isinstance(self.expected_status, str) or not self.expected_status:
            raise LifecycleContractError(
                "invalid_expected_status",
                "expected_status",
                "Declare the exact task status required by the current owner.",
            )
        if self.task_artifact_expectation not in {"required", "absent"}:
            raise LifecycleContractError(
                "invalid_task_artifact_expectation",
                "task_artifact_expectation",
                "Use required for an existing lifecycle or absent before task creation.",
            )


@dataclass(frozen=True)
class CheckoutCandidate:
    candidate_id: str
    facts: WorktreeFacts
    status: CandidateStatus
    reason_code: str | None
    reason_refs: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return self.status == "valid"


@dataclass(frozen=True)
class CheckoutResolution:
    kind: ResolutionKind
    candidates: tuple[CheckoutCandidate, ...]
    selected: CheckoutCandidate | None
    reason_code: str

    @property
    def valid_candidates(self) -> tuple[CheckoutCandidate, ...]:
        return tuple(row for row in self.candidates if row.valid)


def _artifact_facts(candidate: WorktreeFacts, request: CheckoutRequest) -> tuple[dict[str, Any] | None, str | None]:
    metadata_path = candidate.path / request.task_ref / "task.json"
    try:
        if metadata_path.is_symlink() or not metadata_path.is_file():
            if request.task_artifact_expectation == "absent":
                try:
                    active_tasks = tuple(
                        row for row in task_inventory(candidate.path) if row.lifecycle_state == "active"
                    )
                except LifecycleContractError:
                    return None, "active_task_inventory_invalid"
                if active_tasks:
                    return {
                        "active_task_refs": [row.task_ref for row in active_tasks],
                    }, "active_task_authority_conflict"
                return None, None
            return None, "task_artifact_missing"
        payload = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, "task_artifact_invalid"
    if not isinstance(payload, dict):
        return None, "task_artifact_invalid"
    if request.task_artifact_expectation == "absent":
        return payload, "task_artifact_already_exists"
    try:
        task_id = normalize_task_id(payload.get("id"), field_path="task_artifact.id")
        generation = normalize_generation(
            payload.get("lifecycle_generation", 0),
            field_path="task_artifact.lifecycle_generation",
        )
    except LifecycleContractError:
        return None, "task_artifact_invalid"
    if task_id != request.task_id or generation != request.lifecycle_generation:
        return payload, "task_artifact_mismatch"
    if payload.get("status") != request.expected_status:
        return payload, "task_status_mismatch"
    return payload, None


def _candidate(
    request: CheckoutRequest,
    facts: WorktreeFacts,
) -> CheckoutCandidate:
    candidate_identity = facts.git_dir or facts.registration.path
    candidate_id = f"checkout:{sha256(str(candidate_identity).encode('utf-8')).hexdigest()[:24]}"
    path_ref = str(facts.path)
    branch_claims_authority = facts.registration.registered_branch_ref == request.branch_ref
    if facts.inspection_error:
        status: CandidateStatus = "authority_conflict" if branch_claims_authority else "invalid_candidate"
        return CheckoutCandidate(candidate_id, facts, status, facts.inspection_error, (path_ref,))
    if facts.common_dir != request.repository.common_dir:
        return CheckoutCandidate(candidate_id, facts, "authority_conflict", "wrong_repository", (path_ref,))
    if facts.branch_ref is None:
        return CheckoutCandidate(candidate_id, facts, "invalid_candidate", "detached_checkout", (path_ref,))
    if facts.branch_ref != request.branch_ref:
        return CheckoutCandidate(candidate_id, facts, "invalid_candidate", "branch_mismatch", (path_ref, facts.branch_ref))
    _, artifact_error = _artifact_facts(facts, request)
    if artifact_error:
        return CheckoutCandidate(candidate_id, facts, "authority_conflict", artifact_error, (path_ref, request.task_ref))
    if request.expected_head is not None and facts.head != request.expected_head:
        return CheckoutCandidate(candidate_id, facts, "authority_conflict", "head_drift", (path_ref, facts.head or "missing"))
    if not facts.clean:
        return CheckoutCandidate(candidate_id, facts, "invalid_candidate", "dirty_checkout", (path_ref, *facts.dirty_paths))
    return CheckoutCandidate(candidate_id, facts, "valid", None, ())


def validate_candidate(
    request: CheckoutRequest,
    facts: WorktreeFacts,
) -> CheckoutCandidate:
    return _candidate(request, facts)


def classify_candidates(candidates: tuple[CheckoutCandidate, ...]) -> CheckoutResolution:
    conflicts = tuple(row for row in candidates if row.status == "authority_conflict")
    if conflicts:
        return CheckoutResolution("authority_conflict", candidates, None, conflicts[0].reason_code or "authority_conflict")
    valid = tuple(row for row in candidates if row.valid)
    if len(valid) == 1:
        return CheckoutResolution("checkout_resolved", candidates, valid[0], "unique_validated_candidate")
    return CheckoutResolution(
        "selection_required",
        candidates,
        None,
        "zero_validated_candidates" if not valid else "multiple_validated_candidates",
    )


def discover_validate_classify(request: CheckoutRequest) -> CheckoutResolution:
    facts = discover_worktree_facts(request.repository)
    candidates = tuple(_candidate(request, row) for row in facts)
    return classify_candidates(candidates)


def _fresh_explicit_candidate(request: CheckoutRequest, target_path: Path) -> CheckoutCandidate:
    registration = find_registration(request.repository, target_path)
    if registration is None:
        foreign_facts: WorktreeFacts | None = None
        try:
            foreign = inspect_repository(target_path)
            foreign_registration = next(
                (row for row in discover_worktree_facts(foreign) if row.path == target_path.resolve()),
                None,
            )
            foreign_facts = foreign_registration
        except LifecycleContractError:
            pass
        if foreign_facts is not None:
            return CheckoutCandidate(
                "explicit-target",
                foreign_facts,
                "authority_conflict",
                "wrong_repository",
                (str(target_path.resolve()),),
            )
        raise LifecycleContractError(
            "target_no_longer_present",
            "target_path",
            "Choose a checkout still registered in the current repository.",
        )
    return _candidate(request, inspect_registered_worktree(request.repository, registration))


def select_or_specify(
    request: CheckoutRequest,
    *,
    selected_candidate_id: str | None = None,
    explicit_target: Path | str | None = None,
) -> CheckoutResolution:
    if (selected_candidate_id is None) == (explicit_target is None):
        raise LifecycleContractError(
            "invalid_checkout_selection",
            "selection",
            "Select one displayed candidate or specify one explicit checkout target.",
        )
    fresh = discover_validate_classify(request)
    if fresh.kind == "authority_conflict":
        return fresh
    if explicit_target is not None:
        target = _fresh_explicit_candidate(request, Path(explicit_target).resolve())
    else:
        assert selected_candidate_id is not None
        matching = tuple(row for row in fresh.candidates if row.candidate_id == selected_candidate_id)
        if len(matching) != 1:
            return CheckoutResolution("selection_required", fresh.candidates, None, "selected_candidate_stale")
        target = matching[0]
    if target.status == "authority_conflict":
        return CheckoutResolution("authority_conflict", fresh.candidates + (target,), None, target.reason_code or "authority_conflict")
    if not target.valid:
        return CheckoutResolution("selection_required", fresh.candidates + (target,), None, target.reason_code or "invalid_candidate")
    revalidated = _fresh_explicit_candidate(request, target.facts.path)
    if not revalidated.valid:
        kind: ResolutionKind = "authority_conflict" if revalidated.status == "authority_conflict" else "selection_required"
        return CheckoutResolution(kind, fresh.candidates + (revalidated,), None, revalidated.reason_code or "target_changed")
    return CheckoutResolution("checkout_resolved", fresh.candidates, revalidated, "selected_target_revalidated")


__all__ = [
    "CheckoutCandidate",
    "CheckoutRequest",
    "CheckoutResolution",
    "TaskArtifactExpectation",
    "canonical_head_ref",
    "classify_candidates",
    "discover_validate_classify",
    "select_or_specify",
    "validate_candidate",
]
