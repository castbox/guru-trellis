"""Deterministic lifecycle ownership for Guru-created temporary objects.

This module deliberately owns facts only: inventory matching, root containment,
stale probing, cleanup and disposition. Callers retain semantic ownership of
whether an object is eligible for this contract.
"""

from __future__ import annotations

import json
import os
import shutil
import signal
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


DISPOSITIONS = (
    "deleted",
    "retained_live",
    "retained_non_stale",
    "deletion_failed",
    "deletion_unverified",
)


@dataclass(frozen=True)
class InventoryEntry:
    id: str
    owner: str
    kind: str
    prefix: str
    root_env: str
    auto_created: bool = True


INVENTORY: tuple[InventoryEntry, ...] = (
    InventoryEntry("preset_staging", "preset_apply", "directory", "guru-team-preset-stage-", "TMPDIR"),
    InventoryEntry("throwaway_install", "throwaway_install", "directory", "guru-trellis-install.", "TMPDIR"),
    InventoryEntry("extension_verification", "extension_verification", "directory", "guru-extension-verification-", "TMPDIR"),
    InventoryEntry("task_commit_input", "task_commit", "path", "guru-task-commit-input.", "TMPDIR"),
    InventoryEntry("phase2_input", "phase2_verifier", "file", "guru-phase2-input.", "TMPDIR"),
)

_BY_ID = {entry.id: entry for entry in INVENTORY}


def inventory() -> tuple[InventoryEntry, ...]:
    return INVENTORY


def entry(entry_id: str) -> InventoryEntry:
    try:
        return _BY_ID[entry_id]
    except KeyError as exc:
        raise ValueError(f"unknown temporary inventory entry: {entry_id}") from exc


def controlled_root(entry_or_id: InventoryEntry | str, *, environ: dict[str, str] | None = None) -> Path:
    item = entry_or_id if isinstance(entry_or_id, InventoryEntry) else entry(entry_or_id)
    values = environ if environ is not None else os.environ
    raw = values.get(item.root_env) or tempfile.gettempdir()
    root = Path(raw).expanduser()
    if not root.is_absolute() or root.is_symlink():
        raise ValueError(f"unsafe controlled root for {item.id}")
    resolved = root.resolve()
    if not resolved.is_dir():
        raise ValueError(f"controlled root is unavailable for {item.id}")
    return resolved


def _contained(root: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _matches(item: InventoryEntry, root: Path, target: Path) -> bool:
    return (
        _contained(root, target)
        and target.parent.resolve() == root.resolve()
        and target.name.startswith(item.prefix)
        and not target.is_symlink()
    )


def _disposition(path: Path, disposition: str, reason: str | None = None) -> dict[str, object]:
    if disposition not in DISPOSITIONS:
        raise ValueError(disposition)
    value: dict[str, object] = {"path": str(path), "disposition": disposition}
    if reason:
        value["reason"] = reason
    return value


def cleanup(
    entry_or_id: InventoryEntry | str,
    path: Path,
    *,
    live: bool = False,
    stale: bool = True,
    deletion_allowed: bool = True,
    root: Path | None = None,
) -> dict[str, object]:
    item = entry_or_id if isinstance(entry_or_id, InventoryEntry) else entry(entry_or_id)
    root = root or controlled_root(item)
    if not _matches(item, root, path):
        return _disposition(path, "retained_non_stale", "unknown_or_unsafe_inventory_target")
    if live:
        return _disposition(path, "retained_live", "live_or_in_use")
    if not stale:
        return _disposition(path, "retained_non_stale", "not_stale")
    if not deletion_allowed:
        return _disposition(path, "deletion_unverified", "local_deletion_policy_rejected")
    try:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    except OSError as exc:
        return _disposition(path, "deletion_failed", str(exc))
    return _disposition(path, "deleted")


def reap_stale(
    entry_or_id: InventoryEntry | str,
    *,
    root: Path | None = None,
    live_paths: set[Path] | None = None,
    stale_predicate=None,
    deletion_allowed: bool = True,
) -> list[dict[str, object]]:
    item = entry_or_id if isinstance(entry_or_id, InventoryEntry) else entry(entry_or_id)
    root = root or controlled_root(item)
    live_paths = {path.resolve() for path in (live_paths or set())}
    try:
        candidates = sorted(root.iterdir(), key=lambda path: path.name)
    except OSError as exc:
        return [_disposition(root, "deletion_failed", str(exc))]
    results: list[dict[str, object]] = []
    for path in candidates:
        if not _matches(item, root, path):
            continue
        is_live = path.resolve() in live_paths
        is_stale = bool(stale_predicate(path)) if stale_predicate else True
        results.append(cleanup(item, path, live=is_live, stale=is_stale, deletion_allowed=deletion_allowed, root=root))
    return results


@contextmanager
def temporary_directory(entry_or_id: InventoryEntry | str, *, root: Path | None = None) -> Iterator[Path]:
    item = entry_or_id if isinstance(entry_or_id, InventoryEntry) else entry(entry_or_id)
    root = root or controlled_root(item)
    root.mkdir(parents=True, exist_ok=True)
    path = Path(tempfile.mkdtemp(prefix=item.prefix, dir=str(root)))
    try:
        yield path
    finally:
        cleanup(item, path, root=root)


def create_input(entry_or_id: InventoryEntry | str, *, root: Path | None = None) -> tuple[int, Path]:
    item = entry_or_id if isinstance(entry_or_id, InventoryEntry) else entry(entry_or_id)
    if item.kind != "file":
        raise ValueError(f"{item.id} is not a file inventory entry")
    root = root or controlled_root(item)
    root.mkdir(parents=True, exist_ok=True)
    fd, raw = tempfile.mkstemp(prefix=item.prefix, dir=str(root))
    return fd, Path(raw)


def inventory_json() -> str:
    return json.dumps(
        [
            {
                "id": item.id,
                "owner": item.owner,
                "kind": item.kind,
                "controlled_root": {"resolver": item.root_env},
                "exact_prefix": item.prefix,
                "created_by": "guru-team",
                "live_probe": "caller supplied live/in-use state",
                "stale_predicate": "closed object from prior run",
                "normal_cleanup": "cleanup",
                "next_run_recovery": "reap_stale",
                "diagnostic_owner": item.owner,
            }
            for item in INVENTORY
        ],
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    ) + "\n"


__all__ = [
    "DISPOSITIONS",
    "INVENTORY",
    "InventoryEntry",
    "cleanup",
    "controlled_root",
    "create_input",
    "entry",
    "inventory",
    "inventory_json",
    "reap_stale",
    "temporary_directory",
]
