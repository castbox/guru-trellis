from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import dataclass, replace
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable, Iterator, Literal, Sequence

from .branch_resolution import Ownership, OwnershipCurrent
from .branch_store import TaskLifecycleKey, normalize_branch_name
from .errors import LifecycleContractError
from .git_facts import RepositoryFacts, is_ancestor
from .source import normalize_repo_ref


RESOURCE_LEDGER_SCHEMA_VERSION = "1.0"
ResourceKind = Literal["local_branch", "linked_worktree", "remote_branch"]
AcquisitionOrigin = Literal[
    "caller_preexisting",
    "guru_created",
    "conservative_recovery",
    "publication",
    "retained_control",
]
ResourceOwnership = Literal["guru_owned", "caller_owned"]
ResourceState = Literal["current", "cleanup_pending", "retained", "resolved"]
ResponsibilityRole = Literal[
    "current_branch",
    "current_worktree",
    "current_delivery",
    "retired_cleanup",
    "manual_only",
    "retained_control",
    "superseded",
]

_LEDGER_FIELDS = {
    "schema_version",
    "task_id",
    "lifecycle_generation",
    "ledger_revision",
    "finish_result_id",
    "finish_head",
    "resources",
}
_RESOURCE_FIELDS = {
    "resource_id",
    "kind",
    "acquisition_origin",
    "ownership",
    "portable_ref",
    "binding_epoch",
    "binding_revision",
    "state",
    "responsibility_role",
    "expected_cleanup_head",
}
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_REMOTE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
_COMMIT = re.compile(r"^[0-9a-f]{40}$")
_RETAINED_CONTROL_REF = re.compile(
    r"^refs/heads/(?=guru-task-lifecycle(?:/|$))(?!-)(?!HEAD$)(?!/)"
    r"(?!.*[\x00-\x20\x7f])"
    r"(?!.*(?:^|/)\.)(?!.*(?:^|/)[^/]*\.lock(?:/|$))"
    r"(?!.*\.\.)(?!.*@\{)(?!.*[ ~^:?*\[\]\\])"
    r"(?!.*[./]$)[^/]+(?:/[^/]+)*$"
)


def _normalize_nonnegative(value: Any, field_path: str) -> int:
    if type(value) is not int or value < 0:
        raise LifecycleContractError(
            "resource_ledger_conflict",
            field_path,
            "Use one non-negative integer ledger, epoch or revision value.",
        )
    return value


def _normalize_full_branch_ref(
    value: Any,
    *,
    field_path: str,
    allow_retained: bool = False,
) -> str:
    if not isinstance(value, str) or not value.startswith("refs/heads/"):
        raise LifecycleContractError(
            "invalid_resource_ref",
            field_path,
            "Use one full refs/heads portable branch identity.",
        )
    branch = value.removeprefix("refs/heads/")
    if _is_retained_control_ref(value):
        if allow_retained:
            return value
        raise LifecycleContractError(
            "retained_control_ref_forbidden",
            field_path,
            "Keep lifecycle receipt refs outside ordinary branch ownership.",
        )
    normalize_branch_name(branch, field_path=field_path)
    return value


def _is_retained_control_ref(value: str) -> bool:
    return isinstance(value, str) and _RETAINED_CONTROL_REF.fullmatch(value) is not None


def _normalize_cleanup_head(value: Any, field_path: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not _COMMIT.fullmatch(value):
        raise LifecycleContractError(
            "resource_ledger_conflict",
            field_path,
            "Use one exact 40-hex cleanup commit identity or null.",
        )
    return value


def _normalize_remote_name(value: Any) -> str:
    if (
        not isinstance(value, str)
        or not _REMOTE_NAME.fullmatch(value)
        or ".." in value
        or value.endswith((".", "/", ".lock"))
        or "/." in value
        or "//" in value
    ):
        raise LifecycleContractError(
            "invalid_resource_ref",
            "portable_ref.remote_name",
            "Use one portable Git remote name.",
        )
    return value


def _portable_ref_key(value: dict[str, str]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _resource_id(
    key: TaskLifecycleKey,
    kind: ResourceKind,
    portable_ref: dict[str, str],
    binding_epoch: int,
    binding_revision: int,
    role: ResponsibilityRole,
) -> str:
    identity = {
        "task_id": key.task_id,
        "lifecycle_generation": key.lifecycle_generation,
        "kind": kind,
        "portable_ref": portable_ref,
        "binding_epoch": binding_epoch,
        "binding_revision": binding_revision,
        "responsibility_role": role,
    }
    digest = sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return f"resource:{digest[:32]}"


def _branch_portable_ref(branch_name: str) -> dict[str, str]:
    branch = normalize_branch_name(branch_name)
    return {"kind": "local_branch", "ref": f"refs/heads/{branch}"}


def _worktree_portable_ref(branch_name: str) -> dict[str, str]:
    branch = normalize_branch_name(branch_name)
    return {"kind": "linked_worktree", "branch_ref": f"refs/heads/{branch}"}


def _remote_portable_ref(
    remote_name: str, repo_ref: str, branch_ref: str, *, retained: bool = False
) -> dict[str, str]:
    return {
        "kind": "remote_branch",
        "remote_name": _normalize_remote_name(remote_name),
        "repository_ref": normalize_repo_ref(repo_ref),
        "ref": _normalize_full_branch_ref(
            branch_ref,
            field_path="portable_ref.ref",
            allow_retained=retained,
        ),
    }


def _normalize_portable_ref(
    kind: ResourceKind,
    value: Any,
    *,
    role: ResponsibilityRole,
) -> dict[str, str]:
    if not isinstance(value, dict):
        raise LifecycleContractError(
            "resource_ledger_conflict",
            "portable_ref",
            "Use one closed portable resource reference.",
        )
    retained = role == "retained_control"
    if kind == "local_branch" and set(value) == {"kind", "ref"} and value.get("kind") == kind:
        return {
            "kind": kind,
            "ref": _normalize_full_branch_ref(
                value.get("ref"),
                field_path="portable_ref.ref",
                allow_retained=retained,
            ),
        }
    if (
        kind == "linked_worktree"
        and set(value) == {"kind", "branch_ref"}
        and value.get("kind") == kind
    ):
        return {
            "kind": kind,
            "branch_ref": _normalize_full_branch_ref(
                value.get("branch_ref"),
                field_path="portable_ref.branch_ref",
            ),
        }
    if (
        kind == "remote_branch"
        and set(value) == {"kind", "remote_name", "repository_ref", "ref"}
        and value.get("kind") == kind
    ):
        return _remote_portable_ref(
            value.get("remote_name"),
            value.get("repository_ref"),
            value.get("ref"),
            retained=retained,
        )
    raise LifecycleContractError(
        "resource_ledger_conflict",
        "portable_ref",
        "Keep resource kind and portable reference shape aligned.",
    )


@dataclass(frozen=True)
class ResourceIncarnation:
    resource_id: str
    kind: ResourceKind
    acquisition_origin: AcquisitionOrigin
    ownership: ResourceOwnership
    portable_ref: dict[str, str]
    binding_epoch: int
    binding_revision: int
    state: ResourceState
    responsibility_role: ResponsibilityRole
    expected_cleanup_head: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.resource_id, str) or not _IDENTIFIER.fullmatch(self.resource_id):
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "resource_id",
                "Use one stable resource incarnation identifier.",
            )
        if self.kind not in {"local_branch", "linked_worktree", "remote_branch"}:
            raise LifecycleContractError(
                "resource_ledger_conflict", "kind", "Use one declared resource kind."
            )
        if self.acquisition_origin not in {
            "caller_preexisting",
            "guru_created",
            "conservative_recovery",
            "publication",
            "retained_control",
        }:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "acquisition_origin",
                "Use one declared acquisition origin.",
            )
        if self.ownership not in {"guru_owned", "caller_owned"}:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "ownership",
                "Unknown ownership must be stored conservatively as caller_owned.",
            )
        if self.state not in {"current", "cleanup_pending", "retained", "resolved"}:
            raise LifecycleContractError(
                "resource_ledger_conflict", "state", "Use one declared resource state."
            )
        if self.responsibility_role not in {
            "current_branch",
            "current_worktree",
            "current_delivery",
            "retired_cleanup",
            "manual_only",
            "retained_control",
            "superseded",
        }:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "responsibility_role",
                "Use one declared responsibility role.",
            )
        object.__setattr__(
            self,
            "portable_ref",
            _normalize_portable_ref(
                self.kind,
                self.portable_ref,
                role=self.responsibility_role,
            ),
        )
        _normalize_nonnegative(self.binding_epoch, "binding_epoch")
        _normalize_nonnegative(self.binding_revision, "binding_revision")
        object.__setattr__(
            self,
            "expected_cleanup_head",
            _normalize_cleanup_head(self.expected_cleanup_head, "expected_cleanup_head"),
        )
        expected = {
            "current_branch": ("local_branch", "current"),
            "current_worktree": ("linked_worktree", "current"),
            "current_delivery": ("remote_branch", "current"),
            "retired_cleanup": (self.kind, "cleanup_pending"),
            "manual_only": (self.kind, "retained"),
            "retained_control": (self.kind, "retained"),
            "superseded": (self.kind, "resolved"),
        }[self.responsibility_role]
        if (self.kind, self.state) != expected:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "responsibility_role",
                "Keep resource kind, state and responsibility role consistent.",
            )
        if self.responsibility_role == "retired_cleanup" and self.ownership != "guru_owned":
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "ownership",
                "Only Guru-owned resources enter ordinary cleanup responsibility.",
            )
        if (
            self.kind == "remote_branch"
            and self.ownership == "guru_owned"
            and self.responsibility_role in {"current_delivery", "retired_cleanup"}
            and self.expected_cleanup_head is None
        ):
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "expected_cleanup_head",
                "Keep an exact published HEAD for Guru-owned remote cleanup responsibility.",
            )
        if self.responsibility_role in {"manual_only", "retained_control"} and self.ownership != "caller_owned":
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "ownership",
                "Retained and unknown responsibility remains caller-owned.",
            )
        if self.responsibility_role == "retained_control":
            if self.acquisition_origin != "retained_control":
                raise LifecycleContractError(
                    "resource_ledger_conflict",
                    "acquisition_origin",
                    "Retained control refs use the retained_control acquisition origin.",
                )
            ref = self.portable_ref.get("ref", "")
            if not _is_retained_control_ref(ref):
                raise LifecycleContractError(
                    "resource_ledger_conflict",
                    "portable_ref.ref",
                    "Use the retained-control role only for guru-task-lifecycle refs.",
                )

    @property
    def branch_ref(self) -> str:
        return self.portable_ref.get("ref") or self.portable_ref["branch_ref"]

    def as_dict(self) -> dict[str, Any]:
        return {
            "resource_id": self.resource_id,
            "kind": self.kind,
            "acquisition_origin": self.acquisition_origin,
            "ownership": self.ownership,
            "portable_ref": dict(self.portable_ref),
            "binding_epoch": self.binding_epoch,
            "binding_revision": self.binding_revision,
            "state": self.state,
            "responsibility_role": self.responsibility_role,
            "expected_cleanup_head": self.expected_cleanup_head,
        }

    @classmethod
    def from_dict(cls, payload: Any) -> ResourceIncarnation:
        if not isinstance(payload, dict) or set(payload) != _RESOURCE_FIELDS:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "resources",
                "Use the closed resource incarnation record.",
            )
        return cls(**payload)


@dataclass(frozen=True)
class ResourceLedger:
    task_id: str
    lifecycle_generation: int
    ledger_revision: int
    resources: tuple[ResourceIncarnation, ...]
    finish_result_id: str | None = None
    finish_head: str | None = None
    schema_version: str = RESOURCE_LEDGER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        key = TaskLifecycleKey(self.task_id, self.lifecycle_generation)
        object.__setattr__(self, "task_id", key.task_id)
        object.__setattr__(self, "lifecycle_generation", key.lifecycle_generation)
        _normalize_nonnegative(self.ledger_revision, "ledger_revision")
        if self.schema_version != RESOURCE_LEDGER_SCHEMA_VERSION:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "schema_version",
                "Use the current resource ledger schema version.",
            )
        if (self.finish_result_id is None) != (self.finish_head is None):
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "finish_result_id",
                "Keep the Finish result and HEAD together in one sealed ledger.",
            )
        if self.finish_result_id is not None:
            _identifier(self.finish_result_id, "finish_result_id")
            _normalize_cleanup_head(self.finish_head, "finish_head")
        resources = tuple(self.resources)
        if self.finish_result_id is not None and any(row.state == "current" for row in resources):
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "resources",
                "A sealed Finish ledger cannot retain current resources.",
            )
        if len({row.resource_id for row in resources}) != len(resources):
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "resources",
                "Keep every resource incarnation id unique.",
            )
        current_branches = [row for row in resources if row.responsibility_role == "current_branch"]
        current_worktrees = [row for row in resources if row.responsibility_role == "current_worktree"]
        current_delivery = [row for row in resources if row.responsibility_role == "current_delivery"]
        if len(current_branches) > 1 or len(current_worktrees) > 1 or len(current_delivery) > 1:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "resources",
                "Keep at most one current branch, worktree and delivery resource.",
            )
        if (current_worktrees or current_delivery) and not current_branches:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "resources",
                "Keep one current branch for every current worktree or delivery resource.",
            )
        if current_branches:
            branch = current_branches[0]
            for row in (*current_worktrees, *current_delivery):
                if (
                    row.binding_epoch != branch.binding_epoch
                    or row.binding_revision != branch.binding_revision
                ):
                    raise LifecycleContractError(
                        "resource_ledger_conflict",
                        "resources",
                        "Keep current resource epoch and revision aligned.",
                    )
            for row in (*current_worktrees, *current_delivery):
                if row.branch_ref != branch.branch_ref:
                    raise LifecycleContractError(
                        "resource_ledger_conflict",
                        "resources",
                        "Keep current branch, worktree and delivery refs aligned.",
                    )
        unresolved: set[tuple[str, str]] = set()
        for row in resources:
            if row.state == "resolved":
                continue
            identity = (row.kind, _portable_ref_key(row.portable_ref))
            if identity in unresolved:
                raise LifecycleContractError(
                    "resource_ledger_conflict",
                    "resources",
                    "Keep one unresolved incarnation per portable resource ref.",
                )
            unresolved.add(identity)
        object.__setattr__(self, "resources", resources)

    @property
    def key(self) -> TaskLifecycleKey:
        return TaskLifecycleKey(self.task_id, self.lifecycle_generation)

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "task_id": self.task_id,
            "lifecycle_generation": self.lifecycle_generation,
            "ledger_revision": self.ledger_revision,
            "finish_result_id": self.finish_result_id,
            "finish_head": self.finish_head,
            "resources": [row.as_dict() for row in self.resources],
        }

    @classmethod
    def from_dict(cls, payload: Any) -> ResourceLedger:
        if not isinstance(payload, dict) or set(payload) != _LEDGER_FIELDS:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "ledger",
                "Use the closed resource ledger record.",
            )
        resources = payload.get("resources")
        if not isinstance(resources, list):
            raise LifecycleContractError(
                "resource_ledger_conflict", "resources", "Use one resource array."
            )
        return cls(
            task_id=payload.get("task_id"),
            lifecycle_generation=payload.get("lifecycle_generation"),
            ledger_revision=payload.get("ledger_revision"),
            resources=tuple(ResourceIncarnation.from_dict(row) for row in resources),
            finish_result_id=payload.get("finish_result_id"),
            finish_head=payload.get("finish_head"),
            schema_version=payload.get("schema_version"),
        )


@dataclass(frozen=True)
class ResourceLedgerSnapshot:
    path: Path
    content: bytes | None


@dataclass(frozen=True)
class CleanupResource:
    resource_id: str
    kind: ResourceKind
    portable_ref: dict[str, str]
    expected_cleanup_head: str | None

    def __post_init__(self) -> None:
        _identifier(self.resource_id, "resource_id")
        if self.kind not in {"local_branch", "linked_worktree", "remote_branch"}:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "kind",
                "Use one declared cleanup resource kind.",
            )
        object.__setattr__(
            self,
            "portable_ref",
            _normalize_portable_ref(
                self.kind,
                self.portable_ref,
                role="retired_cleanup",
            ),
        )
        object.__setattr__(
            self,
            "expected_cleanup_head",
            _normalize_cleanup_head(self.expected_cleanup_head, "expected_cleanup_head"),
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "resource_id": self.resource_id,
            "kind": self.kind,
            "portable_ref": dict(self.portable_ref),
            "expected_cleanup_head": self.expected_cleanup_head,
        }


@dataclass(frozen=True)
class CleanupResolution:
    resolution_kind: Literal[
        "ordinary_cleanup", "manual_selection_required", "already_clean"
    ]
    key: TaskLifecycleKey
    finish_result_id: str
    inventory_id: str | None = None
    resources: tuple[CleanupResource, ...] = ()
    reason_code: str | None = None

    def __post_init__(self) -> None:
        if self.resolution_kind not in {
            "ordinary_cleanup",
            "manual_selection_required",
            "already_clean",
        }:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "resolution_kind",
                "Use one declared Cleanup resolution kind.",
            )
        object.__setattr__(
            self,
            "key",
            TaskLifecycleKey(self.key.task_id, self.key.lifecycle_generation),
        )
        object.__setattr__(
            self,
            "finish_result_id",
            _identifier(self.finish_result_id, "finish_result_id"),
        )
        resources = tuple(self.resources)
        if not all(isinstance(row, CleanupResource) for row in resources):
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "resources",
                "Use only validated CleanupResource records.",
            )
        object.__setattr__(self, "resources", resources)
        if self.resolution_kind == "ordinary_cleanup":
            if not resources or self.reason_code is not None:
                raise LifecycleContractError(
                    "resource_ledger_conflict",
                    "resources",
                    "Ordinary Cleanup requires a non-empty resource set and no reason code.",
                )
            if any(row.expected_cleanup_head is None for row in resources):
                raise LifecycleContractError(
                    "resource_ledger_conflict",
                    "resources.expected_cleanup_head",
                    "Ordinary Cleanup requires an exact sealed HEAD for every resource.",
                )
            object.__setattr__(
                self,
                "inventory_id",
                _identifier(self.inventory_id, "inventory_id"),
            )
            return
        if self.resolution_kind == "already_clean":
            if resources or self.reason_code is not None:
                raise LifecycleContractError(
                    "resource_ledger_conflict",
                    "resources",
                    "Already-clean resolution carries no resources or reason code.",
                )
            object.__setattr__(
                self,
                "inventory_id",
                _identifier(self.inventory_id, "inventory_id"),
            )
            return
        if self.inventory_id is not None:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "inventory_id",
                "Manual selection does not claim a sealed inventory identity.",
            )
        object.__setattr__(
            self,
            "reason_code",
            _identifier(self.reason_code, "reason_code"),
        )

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": "1.0",
            "task_id": self.key.task_id,
            "lifecycle_generation": self.key.lifecycle_generation,
            "finish_result_id": self.finish_result_id,
            "resolution_kind": self.resolution_kind,
        }
        if self.resolution_kind == "ordinary_cleanup":
            payload.update(
                inventory_id=self.inventory_id,
                resources=[row.as_dict() for row in self.resources],
            )
        elif self.resolution_kind == "already_clean":
            payload["inventory_id"] = self.inventory_id
        else:
            payload.update(
                reason_code=self.reason_code,
                candidates=[row.as_dict() for row in self.resources],
            )
        return payload


def _origin_for(ownership: ResourceOwnership) -> AcquisitionOrigin:
    return "guru_created" if ownership == "guru_owned" else "caller_preexisting"


def _stored_ownership(value: Ownership, field_path: str) -> ResourceOwnership:
    if value == "guru_owned":
        return "guru_owned"
    if value in {"caller_owned", "not_applicable"}:
        return "caller_owned"
    raise LifecycleContractError(
        "resource_ledger_conflict",
        field_path,
        "Use guru_owned, caller_owned or not_applicable at the C4 port boundary.",
    )


def _new_resource(
    key: TaskLifecycleKey,
    *,
    kind: ResourceKind,
    portable_ref: dict[str, str],
    epoch: int,
    revision: int,
    ownership: ResourceOwnership,
    origin: AcquisitionOrigin,
    state: ResourceState,
    role: ResponsibilityRole,
    expected_cleanup_head: str | None = None,
) -> ResourceIncarnation:
    return ResourceIncarnation(
        resource_id=_resource_id(key, kind, portable_ref, epoch, revision, role),
        kind=kind,
        acquisition_origin=origin,
        ownership=ownership,
        portable_ref=portable_ref,
        binding_epoch=epoch,
        binding_revision=revision,
        state=state,
        responsibility_role=role,
        expected_cleanup_head=expected_cleanup_head,
    )


def _retire(row: ResourceIncarnation, cleanup_head: str | None) -> ResourceIncarnation:
    if row.ownership == "guru_owned":
        return replace(
            row,
            state="cleanup_pending",
            responsibility_role="retired_cleanup",
            expected_cleanup_head=cleanup_head or row.expected_cleanup_head,
        )
    return replace(
        row,
        state="retained",
        responsibility_role="manual_only",
        expected_cleanup_head=cleanup_head or row.expected_cleanup_head,
    )


def _identifier(value: Any, field_path: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise LifecycleContractError(
            "resource_ledger_conflict",
            field_path,
            "Use one portable identifier.",
        )
    return value


class ResourceLedgerStore:
    """Git common-dir ownership store and concrete C4 OwnershipPort."""

    def __init__(self, repository: RepositoryFacts) -> None:
        self.repository = repository
        self.root = repository.common_dir / "trellis" / "task-resources"

    def path_for(self, key: TaskLifecycleKey) -> Path:
        normalized = TaskLifecycleKey(key.task_id, key.lifecycle_generation)
        return self.root / normalized.task_id / f"{normalized.lifecycle_generation}.json"

    def snapshot(self, key: TaskLifecycleKey) -> ResourceLedgerSnapshot:
        path = self.path_for(key)
        try:
            if path.is_symlink():
                raise LifecycleContractError(
                    "resource_ledger_conflict",
                    str(path),
                    "Replace the symlink-backed resource ledger with one regular record.",
                )
            return ResourceLedgerSnapshot(
                path=path,
                content=path.read_bytes() if path.exists() else None,
            )
        except OSError as exc:
            raise LifecycleContractError(
                "resource_ledger_unavailable",
                str(path),
                "Restore readable Git common-dir resource control state.",
            ) from exc

    def restore(self, key: TaskLifecycleKey, snapshot: ResourceLedgerSnapshot) -> None:
        if snapshot.path != self.path_for(key):
            raise LifecycleContractError(
                "resource_ledger_conflict",
                str(snapshot.path),
                "Restore only the exact lifecycle ledger snapshot.",
            )
        if snapshot.content is None:
            try:
                snapshot.path.unlink(missing_ok=True)
                parent = snapshot.path.parent
                if parent.exists() and not any(parent.iterdir()):
                    parent.rmdir()
            except OSError as exc:
                raise LifecycleContractError(
                    "resource_ledger_rollback_failed",
                    str(snapshot.path),
                    "Restore the exact pre-transaction resource ledger state.",
                ) from exc
            return
        self._write_bytes(snapshot.path, snapshot.content)

    def read(self, key: TaskLifecycleKey) -> ResourceLedger | None:
        path = self.path_for(key)
        if not path.exists():
            return None
        if path.is_symlink() or not path.is_file():
            raise LifecycleContractError(
                "resource_ledger_conflict",
                str(path),
                "Keep exactly one regular resource ledger for the lifecycle key.",
            )
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            ledger = ResourceLedger.from_dict(payload)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, TypeError, LifecycleContractError) as exc:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                str(path),
                "Repair the closed resource ledger JSON record.",
            ) from exc
        if ledger.key != TaskLifecycleKey(key.task_id, key.lifecycle_generation):
            raise LifecycleContractError(
                "resource_ledger_conflict",
                str(path),
                "Keep ledger identity equal to its common-dir lifecycle key.",
            )
        return ledger

    def iter_ledgers(self) -> Iterator[ResourceLedger]:
        if not self.root.exists():
            return
        if self.root.is_symlink() or not self.root.is_dir():
            raise LifecycleContractError(
                "resource_ledger_conflict",
                str(self.root),
                "Keep the resource-ledger root as one regular directory.",
            )
        for task_dir in sorted(self.root.iterdir(), key=lambda item: item.name):
            if task_dir.is_symlink() or not task_dir.is_dir():
                raise LifecycleContractError(
                    "resource_ledger_conflict",
                    str(task_dir),
                    "Keep only lifecycle-key directories below the ledger root.",
                )
            for path in sorted(task_dir.iterdir(), key=lambda item: item.name):
                if path.suffix != ".json" or not path.stem.isdecimal():
                    raise LifecycleContractError(
                        "resource_ledger_conflict",
                        str(path),
                        "Keep only <generation>.json resource ledgers.",
                    )
                ledger = self.read(TaskLifecycleKey(task_dir.name, int(path.stem)))
                assert ledger is not None
                yield ledger

    def read_current(self, key: TaskLifecycleKey) -> OwnershipCurrent | None:
        ledger = self.read(key)
        if ledger is None:
            return None
        current = [
            row
            for row in ledger.resources
            if row.responsibility_role == "current_branch" and row.state == "current"
        ]
        if not current:
            return None
        branch = current[0]
        return OwnershipCurrent(
            ledger.task_id,
            ledger.lifecycle_generation,
            branch.binding_epoch,
            branch.binding_revision,
            branch.branch_ref.removeprefix("refs/heads/"),
        )

    def establish_current(
        self,
        key: TaskLifecycleKey,
        *,
        binding_epoch: int,
        binding_revision: int,
        branch_name: str,
        branch_ownership: Ownership,
        worktree_ownership: Ownership,
    ) -> OwnershipCurrent:
        normalized = TaskLifecycleKey(key.task_id, key.lifecycle_generation)
        if self.read(normalized) is not None:
            raise LifecycleContractError(
                "resource_ownership_conflict",
                str(self.path_for(normalized)),
                "Recover the existing ledger instead of replacing its ownership history.",
            )
        current = OwnershipCurrent(
            normalized.task_id,
            normalized.lifecycle_generation,
            binding_epoch,
            binding_revision,
            branch_name,
        )
        branch_owner = _stored_ownership(branch_ownership, "branch_ownership")
        if branch_ownership == "not_applicable":
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "branch_ownership",
                "A current local branch must have Guru or caller ownership.",
            )
        resources = [
            _new_resource(
                normalized,
                kind="local_branch",
                portable_ref=_branch_portable_ref(branch_name),
                epoch=binding_epoch,
                revision=binding_revision,
                ownership=branch_owner,
                origin=_origin_for(branch_owner),
                state="current",
                role="current_branch",
            )
        ]
        if worktree_ownership != "not_applicable":
            worktree_owner = _stored_ownership(worktree_ownership, "worktree_ownership")
            resources.append(
                _new_resource(
                    normalized,
                    kind="linked_worktree",
                    portable_ref=_worktree_portable_ref(branch_name),
                    epoch=binding_epoch,
                    revision=binding_revision,
                    ownership=worktree_owner,
                    origin=_origin_for(worktree_owner),
                    state="current",
                    role="current_worktree",
                )
            )
        self._write(ResourceLedger(normalized.task_id, normalized.lifecycle_generation, 1, tuple(resources)))
        established = self.read_current(normalized)
        if established != current:
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "post_state",
                "Keep the persisted ownership projection equal to the established branch binding.",
            )
        return established

    def recover_active_missing(
        self,
        key: TaskLifecycleKey,
        *,
        binding_epoch: int,
        binding_revision: int,
        branch_name: str,
        live_branch_present: bool,
        linked_worktree_present: bool,
        remote_delivery: tuple[str, str, str] | None = None,
    ) -> OwnershipCurrent:
        if not live_branch_present:
            raise LifecycleContractError(
                "resource_ownership_missing",
                "live_branch",
                "Validate one live current branch before conservative active recovery.",
            )
        normalized = TaskLifecycleKey(key.task_id, key.lifecycle_generation)
        current = OwnershipCurrent(
            normalized.task_id,
            normalized.lifecycle_generation,
            binding_epoch,
            binding_revision,
            branch_name,
        )
        resources = [
            _new_resource(
                normalized,
                kind="local_branch",
                portable_ref=_branch_portable_ref(branch_name),
                epoch=binding_epoch,
                revision=binding_revision,
                ownership="caller_owned",
                origin="conservative_recovery",
                state="current",
                role="current_branch",
            )
        ]
        if linked_worktree_present:
            resources.append(
                _new_resource(
                    normalized,
                    kind="linked_worktree",
                    portable_ref=_worktree_portable_ref(branch_name),
                    epoch=binding_epoch,
                    revision=binding_revision,
                    ownership="caller_owned",
                    origin="conservative_recovery",
                    state="current",
                    role="current_worktree",
                )
            )
        if remote_delivery is not None:
            remote_name, repo_ref, remote_ref = remote_delivery
            portable = _remote_portable_ref(remote_name, repo_ref, remote_ref)
            resources.append(
                _new_resource(
                    normalized,
                    kind="remote_branch",
                    portable_ref=portable,
                    epoch=binding_epoch,
                    revision=binding_revision,
                    ownership="caller_owned",
                    origin="conservative_recovery",
                    state="current",
                    role="current_delivery",
                )
            )
        expected = ResourceLedger(
            normalized.task_id,
            normalized.lifecycle_generation,
            1,
            tuple(resources),
        )
        existing = self.read(normalized)
        if existing is not None:
            if existing == expected:
                return current
            raise LifecycleContractError(
                "resource_ownership_conflict",
                str(self.path_for(normalized)),
                "Recover only the exact conservative active-missing successor.",
            )
        self._write(expected)
        if self.read(normalized) != expected:
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "post_state",
                "Keep conservative recovery equal to the exact persisted successor.",
            )
        return current

    def rebind_current(
        self,
        key: TaskLifecycleKey,
        *,
        expected_epoch: int,
        expected_revision: int,
        source_branch_name: str,
        target_branch_name: str,
        expected_cleanup_head: str,
        target_branch_ownership: Ownership,
        target_worktree_ownership: Ownership | None,
        worktree_reassociated: bool,
    ) -> OwnershipCurrent:
        ledger = self.read(key)
        current = self.read_current(key)
        source = normalize_branch_name(source_branch_name)
        target = normalize_branch_name(target_branch_name)
        _normalize_cleanup_head(expected_cleanup_head, "expected_cleanup_head")
        if (
            ledger is None
            or current is None
            or current.binding_epoch != expected_epoch
            or current.binding_revision != expected_revision
            or current.branch_name != source
        ):
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "ownership",
                "Repeat rebind against the fresh current ledger epoch, revision and branch.",
            )
        successor_revision = expected_revision + 1
        resources: list[ResourceIncarnation] = []
        reassociated_owner: ResourceOwnership | None = None
        for row in ledger.resources:
            if row.responsibility_role == "current_branch":
                resources.append(_retire(row, expected_cleanup_head))
            elif row.responsibility_role == "current_worktree":
                if worktree_reassociated:
                    reassociated_owner = row.ownership
                    resources.append(
                        replace(row, state="resolved", responsibility_role="superseded")
                    )
                else:
                    resources.append(_retire(row, expected_cleanup_head))
            elif row.responsibility_role == "current_delivery":
                resources.append(_retire(row, row.expected_cleanup_head))
            else:
                resources.append(row)

        branch_owner = _stored_ownership(target_branch_ownership, "target_branch_ownership")
        if target_branch_ownership == "not_applicable":
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "target_branch_ownership",
                "A current target branch must have Guru or caller ownership.",
            )
        resources.append(
            _new_resource(
                key,
                kind="local_branch",
                portable_ref=_branch_portable_ref(target),
                epoch=expected_epoch,
                revision=successor_revision,
                ownership=branch_owner,
                origin=_origin_for(branch_owner),
                state="current",
                role="current_branch",
            )
        )
        worktree_owner: ResourceOwnership | None = reassociated_owner
        if not worktree_reassociated and target_worktree_ownership not in {None, "not_applicable"}:
            worktree_owner = _stored_ownership(
                target_worktree_ownership,
                "target_worktree_ownership",
            )
        if worktree_owner is not None:
            resources.append(
                _new_resource(
                    key,
                    kind="linked_worktree",
                    portable_ref=_worktree_portable_ref(target),
                    epoch=expected_epoch,
                    revision=successor_revision,
                    ownership=worktree_owner,
                    origin=_origin_for(worktree_owner),
                    state="current",
                    role="current_worktree",
                )
            )
        successor = ResourceLedger(
            ledger.task_id,
            ledger.lifecycle_generation,
            ledger.ledger_revision + 1,
            tuple(resources),
        )
        self._write(successor)
        projected = self.read_current(key)
        expected = OwnershipCurrent(
            key.task_id,
            key.lifecycle_generation,
            expected_epoch,
            successor_revision,
            target,
        )
        if projected != expected:
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "post_state",
                "Keep rebind ownership equal to the exact successor branch revision.",
            )
        return expected

    def record_remote_delivery(
        self,
        key: TaskLifecycleKey,
        *,
        expected_epoch: int,
        expected_revision: int,
        remote_name: str,
        repository_ref: str,
        branch_ref: str,
        ownership: Ownership,
        expected_cleanup_head: str | None = None,
    ) -> ResourceIncarnation:
        ledger = self.read(key)
        current = self.read_current(key)
        if (
            ledger is None
            or current is None
            or current.binding_epoch != expected_epoch
            or current.binding_revision != expected_revision
        ):
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "remote_delivery",
                "Record remote responsibility only against the current ledger revision.",
            )
        owner = _stored_ownership(ownership, "ownership")
        if ownership == "not_applicable":
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "ownership",
                "A remote delivery resource must have Guru or caller ownership.",
            )
        portable = _remote_portable_ref(remote_name, repository_ref, branch_ref)
        resource = _new_resource(
            key,
            kind="remote_branch",
            portable_ref=portable,
            epoch=expected_epoch,
            revision=expected_revision,
            ownership=owner,
            origin="publication" if owner == "guru_owned" else "caller_preexisting",
            state="current",
            role="current_delivery",
            expected_cleanup_head=expected_cleanup_head,
        )
        deliveries = [
            row for row in ledger.resources
            if row.responsibility_role == "current_delivery"
        ]
        if deliveries:
            existing = deliveries[0]
            if (
                len(deliveries) == 1
                and existing.resource_id == resource.resource_id
                and existing.portable_ref == resource.portable_ref
                and existing.ownership == resource.ownership
                and existing.binding_epoch == resource.binding_epoch
                and existing.binding_revision == resource.binding_revision
            ):
                if existing.expected_cleanup_head == expected_cleanup_head:
                    return existing
                if expected_cleanup_head is not None and (
                    existing.expected_cleanup_head is None
                    or is_ancestor(
                        self.repository,
                        existing.expected_cleanup_head,
                        expected_cleanup_head,
                    )
                ):
                    successor = replace(existing, expected_cleanup_head=expected_cleanup_head)
                    self._write(
                        ResourceLedger(
                            ledger.task_id,
                            ledger.lifecycle_generation,
                            ledger.ledger_revision + 1,
                            tuple(
                                successor if row.resource_id == existing.resource_id else row
                                for row in ledger.resources
                            ),
                        )
                    )
                    persisted = self.read(key)
                    if persisted is not None and successor in persisted.resources:
                        return successor
                    raise LifecycleContractError(
                        "resource_ownership_conflict",
                        "post_state",
                        "Keep the advanced remote delivery in the current incarnation.",
                    )
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "remote_delivery",
                "Keep the current remote identity and advance only its published HEAD.",
            )
        self._write(
            ResourceLedger(
                ledger.task_id,
                ledger.lifecycle_generation,
                ledger.ledger_revision + 1,
                (*ledger.resources, resource),
            )
        )
        persisted = self.read(key)
        if persisted is None:
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "post_state",
                "Keep the remote delivery successor readable after mutation.",
            )
        stored = [
            row for row in persisted.resources
            if row.responsibility_role == "current_delivery"
        ]
        if stored != [resource]:
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "post_state",
                "Keep the persisted remote delivery equal to the exact successor.",
            )
        return stored[0]

    def record_retained_control_ref(
        self,
        key: TaskLifecycleKey,
        *,
        remote_name: str,
        repository_ref: str,
        branch_ref: str,
    ) -> ResourceIncarnation:
        ledger = self.read(key)
        if ledger is None:
            raise LifecycleContractError(
                "resource_ownership_missing",
                "ledger",
                "Establish the lifecycle ledger before recording retained control refs.",
            )
        portable = _remote_portable_ref(
            remote_name, repository_ref, branch_ref, retained=True
        )
        resource = _new_resource(
            key,
            kind="remote_branch",
            portable_ref=portable,
            epoch=0,
            revision=ledger.ledger_revision,
            ownership="caller_owned",
            origin="retained_control",
            state="retained",
            role="retained_control",
        )
        self._write(
            replace(
                ledger,
                ledger_revision=ledger.ledger_revision + 1,
                resources=(*ledger.resources, resource),
            )
        )
        return resource

    def branch_has_unresolved_incarnation(
        self,
        branch_name: str,
        *,
        key: TaskLifecycleKey,
        allowed_current_epoch: int | None,
        allowed_current_revision: int | None,
    ) -> bool:
        branch_ref = f"refs/heads/{normalize_branch_name(branch_name)}"
        normalized_key = TaskLifecycleKey(key.task_id, key.lifecycle_generation)
        for ledger in self.iter_ledgers():
            for row in ledger.resources:
                if row.state == "resolved" or row.kind == "remote_branch" or row.branch_ref != branch_ref:
                    continue
                allowed = (
                    ledger.key == normalized_key
                    and row.state == "current"
                    and row.binding_epoch == allowed_current_epoch
                    and row.binding_revision == allowed_current_revision
                )
                if not allowed:
                    return True
        return False

    def seal_for_finish(
        self,
        key: TaskLifecycleKey,
        *,
        finish_result_id: str,
        finish_head: str,
    ) -> dict[str, Any]:
        finish_id = _identifier(finish_result_id, "finish_result_id")
        exact_finish_head = _normalize_cleanup_head(finish_head, "finish_head")
        if exact_finish_head is None:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "finish_head",
                "Seal current Guru-owned resources against one exact Finish HEAD.",
            )
        ledger = self.read(key)
        if ledger is None:
            raise LifecycleContractError(
                "resource_ownership_missing",
                "ledger",
                "Use terminal missing resolution instead of inventing ownership.",
            )
        if ledger.finish_result_id is not None:
            if (ledger.finish_result_id, ledger.finish_head) != (finish_id, exact_finish_head):
                raise LifecycleContractError(
                    "resource_ledger_conflict",
                    "finish_result_id",
                    "Retry only the exact sealed Finish result and HEAD.",
                )
            return {
                "schema_version": "1.0",
                "task_id": ledger.task_id,
                "lifecycle_generation": ledger.lifecycle_generation,
                "finish_result_id": finish_id,
                "finish_head": exact_finish_head,
                "ledger_revision": ledger.ledger_revision,
                "inventory_id": self._inventory_id(ledger),
            }
        sealed: list[ResourceIncarnation] = []
        for row in ledger.resources:
            if row.state == "current":
                cleanup_head = (
                    exact_finish_head
                    if row.ownership == "guru_owned"
                    else row.expected_cleanup_head
                )
                sealed.append(_retire(row, cleanup_head))
            else:
                sealed.append(row)
        if not any(row.state == "current" for row in ledger.resources):
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "resources",
                "Seal one current resource bundle or retry its existing Finish identity.",
            )
        successor = replace(
            ledger,
            ledger_revision=ledger.ledger_revision + 1,
            resources=tuple(sealed),
            finish_result_id=finish_id,
            finish_head=exact_finish_head,
        )
        self._write(successor)
        inventory_id = self._inventory_id(successor)
        return {
            "schema_version": "1.0",
            "task_id": successor.task_id,
            "lifecycle_generation": successor.lifecycle_generation,
            "finish_result_id": finish_id,
            "finish_head": exact_finish_head,
            "ledger_revision": successor.ledger_revision,
            "inventory_id": inventory_id,
        }

    def cleanup_resolution(
        self,
        key: TaskLifecycleKey,
        *,
        finish_result_id: str,
        inventory_id: str,
    ) -> CleanupResolution:
        finish_id = _identifier(finish_result_id, "finish_result_id")
        expected_inventory = _identifier(inventory_id, "inventory_id")
        ledger = self.read(key)
        if ledger is None:
            return CleanupResolution(
                "manual_selection_required",
                TaskLifecycleKey(key.task_id, key.lifecycle_generation),
                finish_id,
                reason_code="terminal_resource_ledger_missing",
            )
        if ledger.finish_result_id != finish_id:
            raise LifecycleContractError(
                "resource_ledger_conflict",
                "finish_result_id",
                "Resolve Cleanup only for the exact sealed Finish result.",
            )
        current_inventory = self._inventory_id(ledger)
        if current_inventory != expected_inventory:
            raise LifecycleContractError(
                "resource_inventory_stale",
                "inventory_id",
                "Rebuild Cleanup resolution from the fresh sealed resource inventory.",
            )
        resources = tuple(
            CleanupResource(
                row.resource_id,
                row.kind,
                row.portable_ref,
                row.expected_cleanup_head,
            )
            for row in ledger.resources
            if row.ownership == "guru_owned"
            and row.state == "cleanup_pending"
            and row.responsibility_role == "retired_cleanup"
            and not _is_retained_control_ref(row.portable_ref.get("ref", ""))
        )
        if not resources:
            return CleanupResolution(
                "already_clean",
                ledger.key,
                finish_id,
                inventory_id=current_inventory,
            )
        return CleanupResolution(
            "ordinary_cleanup",
            ledger.key,
            finish_id,
            inventory_id=current_inventory,
            resources=resources,
        )

    def resolve_for_cleanup(
        self,
        key: TaskLifecycleKey,
        *,
        finish_result_id: str,
        inventory_id: str,
        resource_ids: Sequence[str],
    ) -> str:
        resolution = self.cleanup_resolution(
            key, finish_result_id=finish_result_id, inventory_id=inventory_id
        )
        if resolution.resolution_kind == "manual_selection_required":
            raise LifecycleContractError(
                "resource_ownership_missing", "ledger", "Resolve terminal missing ownership manually."
            )
        expected = {row.resource_id for row in resolution.resources}
        selected = set(resource_ids)
        if len(selected) != len(resource_ids) or selected != expected:
            raise LifecycleContractError(
                "resource_inventory_stale", "resource_ids", "Resolve exactly the sealed pending Guru-owned resources."
            )
        ledger = self.read(key)
        assert ledger is not None
        if not selected:
            return self._inventory_id(ledger)
        successor = replace(
            ledger,
            ledger_revision=ledger.ledger_revision + 1,
            resources=tuple(
                replace(row, state="resolved", responsibility_role="superseded")
                if row.resource_id in selected else row
                for row in ledger.resources
            ),
        )
        self._write(successor)
        return self._inventory_id(successor)

    def resolve_selected_cleanup(
        self,
        key: TaskLifecycleKey,
        *,
        finish_result_id: str,
        resource_ids: Sequence[str],
    ) -> str:
        ledger = self.read(key)
        if ledger is None or ledger.finish_result_id != finish_result_id:
            raise LifecycleContractError(
                "resource_ownership_conflict", "finish_result_id", "Select the exact sealed Finish lifecycle."
            )
        selected = set(resource_ids)
        eligible = {
            row.resource_id for row in ledger.resources
            if row.ownership == "caller_owned" and row.state == "retained"
            and row.responsibility_role == "manual_only"
        }
        if not selected or len(selected) != len(resource_ids) or not selected <= eligible:
            raise LifecycleContractError(
                "resource_ownership_conflict", "resource_ids", "Resolve only exact selected caller-owned retained resources."
            )
        successor = replace(
            ledger,
            ledger_revision=ledger.ledger_revision + 1,
            resources=tuple(
                replace(row, state="resolved", responsibility_role="superseded")
                if row.resource_id in selected else row
                for row in ledger.resources
            ),
        )
        self._write(successor)
        return self._inventory_id(successor)

    def resolve_handoff_cleanup(
        self,
        key: TaskLifecycleKey,
        *,
        resource_ids: Sequence[str],
    ) -> str:
        ledger = self.read(key)
        if ledger is None:
            raise LifecycleContractError(
                "resource_ownership_missing", "ledger", "Recover the source handoff resource ledger."
            )
        selected = set(resource_ids)
        pending = {
            row.resource_id for row in ledger.resources
            if row.ownership == "guru_owned" and row.state == "cleanup_pending"
            and row.responsibility_role == "retired_cleanup"
        }
        if not selected or len(selected) != len(resource_ids) or not selected <= pending:
            raise LifecycleContractError(
                "resource_ownership_conflict", "resource_ids", "Resolve only the selected pending source handoff incarnations."
            )
        successor = replace(
            ledger,
            ledger_revision=ledger.ledger_revision + 1,
            resources=tuple(
                replace(row, state="resolved", responsibility_role="superseded")
                if row.resource_id in selected else row
                for row in ledger.resources
            ),
        )
        self._write(successor)
        return self._inventory_id(successor)

    def terminal_missing_resolution(
        self,
        key: TaskLifecycleKey,
        *,
        finish_result_id: str,
        candidates: Sequence[CleanupResource] = (),
    ) -> CleanupResolution:
        if self.read(key) is not None:
            raise LifecycleContractError(
                "resource_ownership_conflict",
                "ledger",
                "Use ledger-backed Cleanup resolution while terminal ownership exists.",
            )
        return CleanupResolution(
            "manual_selection_required",
            TaskLifecycleKey(key.task_id, key.lifecycle_generation),
            _identifier(finish_result_id, "finish_result_id"),
            resources=tuple(candidates),
            reason_code="terminal_resource_ledger_missing",
        )

    @staticmethod
    def _inventory_id(ledger: ResourceLedger) -> str:
        responsibility = [
            row.as_dict()
            for row in ledger.resources
            if row.responsibility_role not in {"superseded"}
        ]
        payload = {
            "task_id": ledger.task_id,
            "lifecycle_generation": ledger.lifecycle_generation,
            "ledger_revision": ledger.ledger_revision,
            "resources": responsibility,
        }
        digest = sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return f"resource-inventory:{digest[:32]}"

    def _write(self, ledger: ResourceLedger) -> None:
        payload = json.dumps(
            ledger.as_dict(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8") + b"\n"
        self._write_bytes(self.path_for(ledger.key), payload)

    @staticmethod
    def _write_bytes(path: Path, payload: bytes) -> None:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
            try:
                with os.fdopen(descriptor, "wb") as stream:
                    stream.write(payload)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, path)
            except Exception:
                try:
                    os.unlink(temporary)
                except OSError:
                    pass
                raise
        except OSError as exc:
            raise LifecycleContractError(
                "resource_ledger_write_failed",
                str(path),
                "Restore writable common-dir control state and resume the same transaction.",
            ) from exc


__all__ = [
    "AcquisitionOrigin",
    "CleanupResolution",
    "CleanupResource",
    "RESOURCE_LEDGER_SCHEMA_VERSION",
    "ResourceIncarnation",
    "ResourceKind",
    "ResourceLedger",
    "ResourceLedgerSnapshot",
    "ResourceLedgerStore",
    "ResourceOwnership",
    "ResourceState",
    "ResponsibilityRole",
]
