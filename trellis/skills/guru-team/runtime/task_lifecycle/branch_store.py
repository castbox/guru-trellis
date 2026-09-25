from __future__ import annotations

import json
import os
import secrets
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from .errors import LifecycleContractError
from .git_facts import RepositoryFacts
from .identity import normalize_generation, normalize_task_id
from .source import normalize_branch_ref


BRANCH_BINDING_SCHEMA_VERSION = "1.0"
_RECORD_FIELDS = {
    "schema_version",
    "task_id",
    "lifecycle_generation",
    "binding_epoch",
    "binding_revision",
    "branch_name",
}


def _new_binding_epoch() -> int:
    return secrets.randbits(63)


def normalize_branch_name(value: Any, *, field_path: str = "branch_name") -> str:
    if isinstance(value, str) and any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise LifecycleContractError(
            "invalid_branch_ref",
            field_path,
            "Use one portable branch name without ASCII control characters or DEL.",
        )
    normalized = normalize_branch_ref(value, field_path=field_path)
    if normalized.startswith("refs/"):
        raise LifecycleContractError(
            "invalid_branch_ref",
            field_path,
            "Use one portable branch name without a refs namespace.",
        )
    return normalized


@dataclass(frozen=True)
class TaskLifecycleKey:
    task_id: str
    lifecycle_generation: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "task_id", normalize_task_id(self.task_id))
        object.__setattr__(
            self,
            "lifecycle_generation",
            normalize_generation(self.lifecycle_generation),
        )


@dataclass(frozen=True)
class BranchBinding:
    task_id: str
    lifecycle_generation: int
    binding_epoch: int
    binding_revision: int
    branch_name: str
    schema_version: str = BRANCH_BINDING_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "task_id", normalize_task_id(self.task_id))
        object.__setattr__(
            self,
            "lifecycle_generation",
            normalize_generation(self.lifecycle_generation),
        )
        if type(self.binding_epoch) is not int or self.binding_epoch < 0:
            raise LifecycleContractError(
                "invalid_binding_epoch",
                "binding_epoch",
                "Use one non-negative integer opaque binding epoch.",
            )
        if type(self.binding_revision) is not int or self.binding_revision < 0:
            raise LifecycleContractError(
                "invalid_binding_revision",
                "binding_revision",
                "Use one non-negative integer binding revision.",
            )
        object.__setattr__(self, "branch_name", normalize_branch_name(self.branch_name))
        if self.schema_version != BRANCH_BINDING_SCHEMA_VERSION:
            raise LifecycleContractError(
                "branch_binding_schema_mismatch",
                "schema_version",
                "Use the current TaskBranchBinding schema version.",
            )

    @property
    def key(self) -> TaskLifecycleKey:
        return TaskLifecycleKey(self.task_id, self.lifecycle_generation)

    @property
    def branch_ref(self) -> str:
        return f"refs/heads/{self.branch_name}"

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "task_id": self.task_id,
            "lifecycle_generation": self.lifecycle_generation,
            "binding_epoch": self.binding_epoch,
            "binding_revision": self.binding_revision,
            "branch_name": self.branch_name,
        }


@dataclass(frozen=True)
class BranchBindingSnapshot:
    path: Path
    content: bytes | None


class BranchBindingStore:
    def __init__(self, repository: RepositoryFacts) -> None:
        self.repository = repository
        self.root = repository.common_dir / "trellis" / "task-branches"

    def path_for(self, key: TaskLifecycleKey) -> Path:
        normalized = TaskLifecycleKey(key.task_id, key.lifecycle_generation)
        return self.root / normalized.task_id / f"{normalized.lifecycle_generation}.json"

    def snapshot(self, key: TaskLifecycleKey) -> BranchBindingSnapshot:
        path = self.path_for(key)
        try:
            if path.is_symlink():
                raise LifecycleContractError(
                    "branch_binding_conflict",
                    str(path),
                    "Replace the symlink-backed control record with one regular TaskBranchBinding record.",
                )
            content = path.read_bytes() if path.exists() else None
        except OSError as exc:
            raise LifecycleContractError(
                "branch_binding_unavailable",
                str(path),
                "Restore readable Git common-dir TaskBranchBinding control state.",
            ) from exc
        return BranchBindingSnapshot(path=path, content=content)

    def restore(self, snapshot: BranchBindingSnapshot) -> None:
        if snapshot.path != snapshot.path.resolve():
            raise LifecycleContractError(
                "branch_binding_conflict",
                str(snapshot.path),
                "Restore only the exact common-dir TaskBranchBinding snapshot.",
            )
        if snapshot.content is None:
            try:
                snapshot.path.unlink(missing_ok=True)
                parent = snapshot.path.parent
                if parent.exists() and not any(parent.iterdir()):
                    parent.rmdir()
            except OSError as exc:
                raise LifecycleContractError(
                    "branch_binding_rollback_failed",
                    str(snapshot.path),
                    "Restore the exact pre-transaction TaskBranchBinding state before continuing.",
                ) from exc
            return
        self._write_bytes(snapshot.path, snapshot.content)

    def read(self, key: TaskLifecycleKey) -> BranchBinding | None:
        path = self.path_for(key)
        if not path.exists():
            return None
        if path.is_symlink() or not path.is_file():
            raise LifecycleContractError(
                "branch_binding_conflict",
                str(path),
                "Keep exactly one regular TaskBranchBinding record for the lifecycle key.",
            )
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise LifecycleContractError(
                "branch_binding_conflict",
                str(path),
                "Repair the closed TaskBranchBinding JSON record.",
            ) from exc
        if not isinstance(payload, dict) or set(payload) != _RECORD_FIELDS:
            raise LifecycleContractError(
                "branch_binding_conflict",
                str(path),
                "Use only schema_version, task_id, lifecycle_generation, binding_epoch, binding_revision and branch_name.",
            )
        try:
            binding = BranchBinding(**payload)
        except (TypeError, LifecycleContractError) as exc:
            raise LifecycleContractError(
                "branch_binding_conflict",
                str(path),
                "Repair the TaskBranchBinding schema, identity, revision and branch values.",
            ) from exc
        expected = TaskLifecycleKey(key.task_id, key.lifecycle_generation)
        if binding.key != expected:
            raise LifecycleContractError(
                "branch_binding_conflict",
                str(path),
                "Keep the record identity equal to its common-dir lifecycle key.",
            )
        return binding

    def iter_bindings(self) -> Iterator[BranchBinding]:
        if not self.root.exists():
            return
        if self.root.is_symlink() or not self.root.is_dir():
            raise LifecycleContractError(
                "branch_binding_conflict",
                str(self.root),
                "Keep the TaskBranchBinding root as one regular common-dir directory.",
            )
        for task_dir in sorted(self.root.iterdir(), key=lambda item: item.name):
            if task_dir.is_symlink() or not task_dir.is_dir():
                raise LifecycleContractError(
                    "branch_binding_conflict",
                    str(task_dir),
                    "Keep only lifecycle-key directories below the TaskBranchBinding root.",
                )
            for path in sorted(task_dir.iterdir(), key=lambda item: item.name):
                if path.suffix != ".json" or not path.stem.isdecimal():
                    raise LifecycleContractError(
                        "branch_binding_conflict",
                        str(path),
                        "Keep only <generation>.json TaskBranchBinding records.",
                    )
                key = TaskLifecycleKey(task_dir.name, int(path.stem))
                binding = self.read(key)
                assert binding is not None
                yield binding

    def branch_owner(
        self,
        branch_name: str,
        *,
        excluding: TaskLifecycleKey | None = None,
    ) -> BranchBinding | None:
        expected = normalize_branch_name(branch_name)
        owners = [
            row
            for row in self.iter_bindings()
            if row.branch_name == expected and (excluding is None or row.key != excluding)
        ]
        if len(owners) > 1:
            raise LifecycleContractError(
                "branch_binding_conflict",
                "branch_name",
                "Repair duplicate current branch associations before lifecycle mutation.",
            )
        return owners[0] if owners else None

    def establish(
        self,
        key: TaskLifecycleKey,
        branch_name: str,
        *,
        binding_epoch: int | None = None,
        binding_revision: int = 0,
    ) -> BranchBinding:
        normalized_key = TaskLifecycleKey(key.task_id, key.lifecycle_generation)
        if self.read(normalized_key) is not None:
            raise LifecycleContractError(
                "branch_binding_already_exists",
                str(self.path_for(normalized_key)),
                "Use rebind for an existing association or recover the exact prior result.",
            )
        if binding_epoch is None and binding_revision != 0:
            raise LifecycleContractError(
                "invalid_binding_revision",
                "binding_revision",
                "Create a new binding epoch only at revision zero, or reuse the surviving epoch.",
            )
        owner = self.branch_owner(branch_name, excluding=normalized_key)
        if owner is not None:
            raise LifecycleContractError(
                "branch_already_bound",
                "branch_name",
                "Choose a branch not currently associated with another active task lifecycle.",
            )
        binding = BranchBinding(
            task_id=normalized_key.task_id,
            lifecycle_generation=normalized_key.lifecycle_generation,
            binding_epoch=_new_binding_epoch() if binding_epoch is None else binding_epoch,
            binding_revision=binding_revision,
            branch_name=branch_name,
        )
        self._write(binding, exclusive=True)
        return binding

    def advance(
        self,
        key: TaskLifecycleKey,
        *,
        expected_epoch: int,
        expected_revision: int,
        branch_name: str,
    ) -> BranchBinding:
        current = self.read(key)
        if current is None:
            raise LifecycleContractError(
                "branch_binding_required",
                str(self.path_for(key)),
                "Establish the missing current branch association before rebind.",
            )
        if type(expected_epoch) is not int or current.binding_epoch != expected_epoch:
            raise LifecycleContractError(
                "branch_binding_epoch_conflict",
                "binding_epoch",
                "Repeat the mutation against the fresh current binding epoch.",
            )
        if type(expected_revision) is not int or current.binding_revision != expected_revision:
            raise LifecycleContractError(
                "branch_binding_revision_conflict",
                "binding_revision",
                "Repeat the mutation against the fresh current binding revision.",
            )
        target = normalize_branch_name(branch_name)
        if target == current.branch_name:
            raise LifecycleContractError(
                "branch_binding_unchanged",
                "branch_name",
                "Use a different reviewed target branch for a revision advance.",
            )
        owner = self.branch_owner(target, excluding=current.key)
        if owner is not None:
            raise LifecycleContractError(
                "branch_already_bound",
                "branch_name",
                "Choose a branch not currently associated with another active task lifecycle.",
            )
        successor = BranchBinding(
            task_id=current.task_id,
            lifecycle_generation=current.lifecycle_generation,
            binding_epoch=current.binding_epoch,
            binding_revision=current.binding_revision + 1,
            branch_name=target,
        )
        self._write(successor, exclusive=False)
        return successor

    def retire_generation(
        self,
        key: TaskLifecycleKey,
        *,
        expected_epoch: int,
        expected_revision: int,
        expected_branch_name: str,
    ) -> BranchBinding | None:
        current = self.read(key)
        if current is None:
            return None
        if (
            type(expected_epoch) is not int
            or type(expected_revision) is not int
            or current.binding_epoch != expected_epoch
            or current.binding_revision != expected_revision
            or current.branch_name != normalize_branch_name(expected_branch_name)
        ):
            raise LifecycleContractError(
                "branch_binding_conflict",
                "binding",
                "Retire only the exact completed generation's branch association.",
            )
        try:
            self.path_for(key).unlink()
        except OSError as exc:
            raise LifecycleContractError(
                "branch_binding_write_failed",
                "binding",
                "Restore writable branch control state before retiring the generation.",
            ) from exc
        return current

    def _write(self, binding: BranchBinding, *, exclusive: bool) -> None:
        path = self.path_for(binding.key)
        if exclusive and path.exists():
            raise LifecycleContractError(
                "branch_binding_already_exists",
                str(path),
                "Recover the existing binding instead of replacing it.",
            )
        payload = json.dumps(
            binding.as_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8") + b"\n"
        self._write_bytes(path, payload)

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
                "branch_binding_write_failed",
                str(path),
                "Restore writable Git common-dir control state and repeat the exact transaction.",
            ) from exc


__all__ = [
    "BRANCH_BINDING_SCHEMA_VERSION",
    "BranchBinding",
    "BranchBindingSnapshot",
    "BranchBindingStore",
    "TaskLifecycleKey",
    "normalize_branch_name",
]
