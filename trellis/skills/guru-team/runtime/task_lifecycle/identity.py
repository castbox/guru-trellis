from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterator

from .errors import LifecycleContractError


TASK_ID_PATTERN = re.compile(r"^(?!.*\.\.)(?!.*(?:\.lock|\.)$)[A-Za-z0-9][A-Za-z0-9._-]*$")
ACTIVE_TASK_REF = re.compile(r"^\.trellis/tasks/(?!archive(?:/|$))[^/]+$")
ARCHIVE_TASK_REF = re.compile(r"^\.trellis/tasks/archive/[0-9]{4}-[0-9]{2}/[^/]+$")
_MISSING = object()


@dataclass(frozen=True)
class TaskArtifactIdentity:
    task_id: str
    task_ref: str
    lifecycle_generation: int
    lifecycle_state: str

    @property
    def lifecycle_key(self) -> tuple[str, int]:
        return self.task_id, self.lifecycle_generation

    def as_dto(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_ref": self.task_ref,
            "lifecycle_generation": self.lifecycle_generation,
        }


def normalize_task_id(value: Any, *, field_path: str = "task_id") -> str:
    if not isinstance(value, str) or not TASK_ID_PATTERN.fullmatch(value):
        raise LifecycleContractError(
            "invalid_task_id",
            field_path,
            "Use a control-ref-safe [A-Za-z0-9][A-Za-z0-9._-]* value without '..', a trailing dot or a .lock suffix.",
        )
    return value


def task_id_key(value: Any, *, field_path: str = "task_id") -> str:
    return normalize_task_id(value, field_path=field_path).casefold()


def normalize_task_ref(value: Any, *, field_path: str = "task_ref") -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise LifecycleContractError(
            "invalid_task_ref", field_path, "Use one canonical repository-relative POSIX task locator."
        )
    path = PurePosixPath(value)
    if path.is_absolute() or path.as_posix() != value or any(part in {"", ".", ".."} for part in path.parts):
        raise LifecycleContractError(
            "invalid_task_ref", field_path, "Use one canonical repository-relative POSIX task locator."
        )
    if not (ACTIVE_TASK_REF.fullmatch(value) or ARCHIVE_TASK_REF.fullmatch(value)):
        raise LifecycleContractError(
            "invalid_task_ref", field_path, "Point to one active task or monthly archived task directory."
        )
    return value


def normalize_generation(value: Any = _MISSING, *, field_path: str = "lifecycle_generation") -> int:
    if value is _MISSING:
        return 0
    if type(value) is not int or value < 0:
        raise LifecycleContractError(
            "invalid_lifecycle_generation", field_path, "Use a non-negative integer; an absent legacy value reads as 0."
        )
    return value


def lifecycle_generation(metadata: dict[str, Any], *, field_path: str = "task.lifecycle_generation") -> int:
    if not isinstance(metadata, dict):
        raise LifecycleContractError("invalid_task_metadata", "task", "Use one task metadata object.")
    return normalize_generation(metadata.get("lifecycle_generation", _MISSING), field_path=field_path)


def _task_refs(repo_root: Path) -> Iterator[str]:
    tasks = repo_root / ".trellis" / "tasks"
    if tasks.is_symlink():
        raise LifecycleContractError(
            "invalid_task_ref", ".trellis/tasks", "Keep the canonical task store free of symlink-backed components."
        )
    if not tasks.is_dir():
        return
    for candidate in sorted(tasks.iterdir(), key=lambda item: item.name):
        if candidate.name == "archive":
            continue
        if candidate.is_symlink():
            raise LifecycleContractError(
                "invalid_task_ref", candidate.relative_to(repo_root).as_posix(),
                "Keep canonical task artifacts free of symlink-backed components.",
            )
        if not candidate.is_dir():
            continue
        yield candidate.relative_to(repo_root).as_posix()
    archive = tasks / "archive"
    if archive.is_symlink():
        raise LifecycleContractError(
            "invalid_task_ref", ".trellis/tasks/archive", "Keep the canonical task archive free of symlink-backed components."
        )
    if not archive.is_dir():
        return
    for month in sorted(archive.iterdir(), key=lambda item: item.name):
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}", month.name):
            continue
        if month.is_symlink():
            raise LifecycleContractError(
                "invalid_task_ref", month.relative_to(repo_root).as_posix(),
                "Keep canonical archive locators free of symlink-backed components.",
            )
        if not month.is_dir():
            continue
        for candidate in sorted(month.iterdir(), key=lambda item: item.name):
            if candidate.is_symlink():
                raise LifecycleContractError(
                    "invalid_task_ref", candidate.relative_to(repo_root).as_posix(),
                    "Keep canonical task artifacts free of symlink-backed components.",
                )
            if not candidate.is_dir():
                continue
            yield candidate.relative_to(repo_root).as_posix()


def _read_identity(repo_root: Path, task_ref: str) -> TaskArtifactIdentity:
    ref = normalize_task_ref(task_ref)
    root = repo_root.resolve()
    directory = root / ref
    metadata = directory / "task.json"
    try:
        current = root
        for part in (*PurePosixPath(ref).parts, "task.json"):
            current /= part
            if current.is_symlink():
                raise LifecycleContractError(
                    "invalid_task_ref", ref, "Keep canonical task artifacts free of symlink-backed components."
                )
        if directory.is_symlink() or not directory.is_dir() or metadata.is_symlink() or not metadata.is_file():
            raise LifecycleContractError("task_not_found", ref, "Resolve a current canonical task artifact.")
        metadata.resolve().relative_to(root)
        data = json.loads(metadata.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise LifecycleContractError("invalid_task_metadata", f"{ref}/task.json", "Repair the task metadata JSON.") from exc
    except (OSError, ValueError) as exc:
        raise LifecycleContractError("invalid_task_ref", ref, "Keep the task artifact inside the selected repository.") from exc
    if not isinstance(data, dict):
        raise LifecycleContractError("invalid_task_metadata", f"{ref}/task.json", "Use one task metadata object.")
    return TaskArtifactIdentity(
        normalize_task_id(data.get("id"), field_path=f"{ref}/task.json.id"),
        ref,
        lifecycle_generation(data, field_path=f"{ref}/task.json.lifecycle_generation"),
        "archived" if ref.startswith(".trellis/tasks/archive/") else "active",
    )


def task_inventory(repo_root: Path) -> tuple[TaskArtifactIdentity, ...]:
    root = repo_root.resolve()
    rows = tuple(_read_identity(root, ref) for ref in _task_refs(root))
    by_fold: dict[str, list[TaskArtifactIdentity]] = {}
    for row in rows:
        by_fold.setdefault(row.task_id.casefold(), []).append(row)
    conflicts = [group for group in by_fold.values() if len(group) > 1]
    if conflicts:
        refs = sorted(row.task_ref for group in conflicts for row in group)
        raise LifecycleContractError(
            "task_id_casefold_collision",
            "task_id",
            "Assign repository-unique exact and case-fold TaskIds before lifecycle resolution.",
            {"task_refs": refs},
        )
    return rows


def resolve_task_ref(repo_root: Path, task_ref: Any, *, expected_task_id: Any | None = None) -> TaskArtifactIdentity:
    selected = _read_identity(repo_root.resolve(), normalize_task_ref(task_ref))
    rows = task_inventory(repo_root)
    current = next((row for row in rows if row.task_ref == selected.task_ref), None)
    if current is None:
        raise LifecycleContractError(
            "invalid_task_ref", selected.task_ref, "Resolve one canonical task artifact from the repository inventory."
        )
    if expected_task_id is not None and current.task_id != normalize_task_id(expected_task_id, field_path="expected_task_id"):
        raise LifecycleContractError(
            "invalid_task_identity", "expected_task_id", "Use the immutable TaskId declared by the selected task artifact."
        )
    return current


def resolve_task_id(repo_root: Path, task_id: Any) -> TaskArtifactIdentity:
    requested = normalize_task_id(task_id)
    rows = task_inventory(repo_root)
    matches = [row for row in rows if row.task_id == requested]
    if not matches:
        raise LifecycleContractError("task_not_found", "task_id", "Select an existing active or archived TaskId.")
    if len(matches) != 1:
        raise LifecycleContractError("invalid_task_identity", "task_id", "Repair duplicate canonical task artifacts.")
    return matches[0]


__all__ = [
    "TaskArtifactIdentity", "lifecycle_generation", "normalize_generation", "normalize_task_id",
    "normalize_task_ref", "resolve_task_id", "resolve_task_ref", "task_id_key", "task_inventory",
]
