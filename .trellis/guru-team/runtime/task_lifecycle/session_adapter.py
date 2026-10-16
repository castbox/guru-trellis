from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Literal, Protocol

from .branch_store import TaskLifecycleKey
from .errors import LifecycleContractError
from .schema import validate_dto


SessionAdapterStatus = Literal[
    "session_bound",
    "session_resolved",
    "explicit_task_mode",
    "session_write_failed",
    "session_invalid",
]


class OfficialSessionPort(Protocol):
    """Narrow adapter over the installed Fixed Fork session APIs."""

    def resolve_context_key(
        self,
        platform_input: dict[str, Any] | None = None,
        platform: str | None = None,
    ) -> str | None: ...

    def repository_facts(self, root: Path) -> Any: ...

    def session_path(self, root: Path, key: str, facts: Any) -> Path: ...

    def record_exists(self, path: Path) -> bool: ...

    def read_record(self, path: Path, root: Path, facts: Any) -> Any: ...

    def write_record(self, path: Path, data: dict[str, Any], root: Path) -> None: ...

    def resolve_task_identity(
        self,
        facts: Any,
        task_id: str,
        lifecycle_generation: int,
    ) -> Any: ...


@dataclass(frozen=True)
class SessionAdapterResult:
    status: SessionAdapterStatus
    lifecycle: TaskLifecycleKey | None
    context_key: str | None = None
    task_ref: str | None = None
    reason_code: str | None = None


def _lifecycle(payload: dict[str, Any]) -> TaskLifecycleKey:
    validated = validate_dto("TaskLifecycleDTO", payload)
    return TaskLifecycleKey(
        validated["task_id"],
        validated["lifecycle_generation"],
    )


def _record(key: TaskLifecycleKey) -> dict[str, Any]:
    return {
        "schema_version": 3,
        "task_id": key.task_id,
        "lifecycle_generation": key.lifecycle_generation,
        "delivery_id": None,
    }


def _record_identity(record: Any, *, field_path: str) -> TaskLifecycleKey:
    data = getattr(record, "data", None)
    if isinstance(data, dict) and data.get("schema_version") == 3:
        # read_record is the public parser; do not copy its Delivery session schema.
        return _lifecycle({"task_id": record.task_id, "lifecycle_generation": record.lifecycle_generation})
    raise LifecycleContractError("session_record_invalid", field_path,
                                 "Use the installed public schema-3 session binding. Old bindings require upstream migration before Delivery execution.")


def _resolved_task_ref(resolved: Any) -> str:
    task_ref = getattr(resolved, "task_ref", None)
    if not isinstance(task_ref, str) or not task_ref:
        raise LifecycleContractError(
            "session_task_resolution_invalid",
            "official_session.resolve_task_identity",
            "Resolve the current TaskRef through the Fixed Fork TaskId resolver.",
        )
    return task_ref


def _context_key(
    official: OfficialSessionPort,
    platform_input: dict[str, Any] | None,
    platform: str | None,
) -> str | None:
    try:
        value = official.resolve_context_key(platform_input, platform)
    except (OSError, RuntimeError, ValueError):
        return None
    return value if isinstance(value, str) and value else None


def bind_session(
    official: OfficialSessionPort,
    repo_root: Path | str,
    lifecycle: dict[str, Any],
    *,
    platform_input: dict[str, Any] | None = None,
    platform: str | None = None,
) -> SessionAdapterResult:
    """Bind Task identity without replacing an existing Delivery selection."""

    key = _lifecycle(lifecycle)
    context_key = _context_key(official, platform_input, platform)
    if context_key is None:
        return SessionAdapterResult(
            "explicit_task_mode",
            key,
            reason_code="context_key_unavailable",
        )

    root = Path(repo_root).resolve()
    try:
        facts = official.repository_facts(root)
        path = official.session_path(root, context_key, facts)
        resolved = official.resolve_task_identity(
            facts,
            key.task_id,
            key.lifecycle_generation,
        )
        task_ref = _resolved_task_ref(resolved)
    except (LifecycleContractError, OSError, RuntimeError, ValueError):
        return SessionAdapterResult(
            "session_invalid",
            key,
            context_key=context_key,
            reason_code="official_session_target_invalid",
        )

    try:
        payload = _record(key)
        workspace = getattr(resolved, "workspace", root)
        from ..delivery_projection.adapter import DeliveryProjection
        DeliveryProjection(workspace, task_ref).read_record()
        if official.record_exists(path):
            prior = official.read_record(path, root, facts)
            if _record_identity(prior, field_path="official_session.record") == key:
                payload = prior.data
        official.write_record(path, payload, root)
    except (OSError, RuntimeError, ValueError):
        return SessionAdapterResult(
            "session_write_failed",
            key,
            context_key=context_key,
            reason_code="official_session_write_failed",
        )

    try:
        stored = official.read_record(path, root, facts)
        stored_key = _record_identity(stored, field_path="official_session.record")
        if stored_key != key:
            raise LifecycleContractError(
                "session_record_invalid",
                "official_session.record",
                "Keep the stored lifecycle identity equal to the requested TaskLifecycleDTO.",
            )
    except (LifecycleContractError, OSError, RuntimeError, ValueError):
        return SessionAdapterResult(
            "session_invalid",
            key,
            context_key=context_key,
            reason_code="official_session_post_write_invalid",
        )
    return SessionAdapterResult(
        "session_bound",
        key,
        context_key=context_key,
        task_ref=task_ref,
    )


def resolve_session(
    official: OfficialSessionPort,
    repo_root: Path | str,
    *,
    platform_input: dict[str, Any] | None = None,
    platform: str | None = None,
) -> SessionAdapterResult:
    """Resolve a public schema-3 binding and fresh TaskRef, never a stored locator."""

    context_key = _context_key(official, platform_input, platform)
    if context_key is None:
        return SessionAdapterResult(
            "explicit_task_mode",
            None,
            reason_code="context_key_unavailable",
        )

    root = Path(repo_root).resolve()
    try:
        facts = official.repository_facts(root)
        path = official.session_path(root, context_key, facts)
        if not official.record_exists(path):
            return SessionAdapterResult(
                "explicit_task_mode",
                None,
                context_key=context_key,
                reason_code="session_record_missing",
            )
        record = official.read_record(path, root, facts)
        key = _record_identity(record, field_path="official_session.record")
        resolved = official.resolve_task_identity(
            facts,
            key.task_id,
            key.lifecycle_generation,
        )
        from ..delivery_projection.adapter import DeliveryProjection
        DeliveryProjection(getattr(resolved, "workspace", root), _resolved_task_ref(resolved)).read_record()
        return SessionAdapterResult(
            "session_resolved",
            key,
            context_key=context_key,
            task_ref=_resolved_task_ref(resolved),
        )
    except (LifecycleContractError, OSError, RuntimeError, ValueError):
        return SessionAdapterResult(
            "session_invalid",
            None,
            context_key=context_key,
            reason_code="official_session_record_invalid",
        )


__all__ = [
    "OfficialSessionPort",
    "SessionAdapterResult",
    "SessionAdapterStatus",
    "bind_session",
    "resolve_session",
]
