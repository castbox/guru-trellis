from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

from .errors import LifecycleContractError


@dataclass(frozen=True)
class RepositoryFacts:
    context_path: Path
    common_dir: Path
    git_dir: Path


@dataclass(frozen=True)
class WorktreeRegistration:
    path: Path
    registered_head: str
    registered_branch_ref: str | None
    detached: bool
    bare: bool
    locked: str | None
    prunable: str | None


@dataclass(frozen=True)
class WorktreeFacts:
    path: Path
    common_dir: Path | None
    git_dir: Path | None
    head: str | None
    branch_ref: str | None
    topology: str
    dirty_paths: tuple[str, ...]
    discovered_at: str
    registration: WorktreeRegistration
    inspection_error: str | None = None

    @property
    def clean(self) -> bool:
        return not self.dirty_paths


def _git(
    args: Sequence[str],
    *,
    cwd: Path | None = None,
    common_dir: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    command = ["git"]
    if common_dir is not None:
        command.append(f"--git-dir={common_dir}")
    command.extend(args)
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError as exc:
        raise LifecycleContractError(
            "git_fact_unavailable",
            "git",
            "Restore a readable Git repository and repeat the live fact inspection.",
        ) from exc
    if check and completed.returncode != 0:
        raise LifecycleContractError(
            "git_fact_unavailable",
            "git",
            "Restore a readable Git repository and repeat the live fact inspection.",
        )
    return completed


def _absolute_git_path(checkout: Path, value: str) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = checkout / candidate
    return candidate.resolve()


def inspect_repository(context_path: Path | str) -> RepositoryFacts:
    context = Path(context_path).resolve()
    top = _git(["rev-parse", "--show-toplevel"], cwd=context).stdout.strip()
    git_dir = _git(["rev-parse", "--absolute-git-dir"], cwd=context).stdout.strip()
    common = _git(["rev-parse", "--git-common-dir"], cwd=context).stdout.strip()
    return RepositoryFacts(
        context_path=Path(top).resolve(),
        common_dir=_absolute_git_path(context, common),
        git_dir=Path(git_dir).resolve(),
    )


def _parse_worktree_porcelain(payload: str) -> tuple[WorktreeRegistration, ...]:
    records: list[WorktreeRegistration] = []
    current: dict[str, str | bool] = {}

    def flush() -> None:
        if not current:
            return
        path = current.get("worktree")
        head = current.get("HEAD")
        if not isinstance(path, str) or not isinstance(head, str):
            raise LifecycleContractError(
                "invalid_worktree_porcelain",
                "git.worktree_list",
                "Repair the Git worktree registry before resolving a checkout.",
            )
        records.append(
            WorktreeRegistration(
                path=Path(path).resolve(),
                registered_head=head,
                registered_branch_ref=current.get("branch") if isinstance(current.get("branch"), str) else None,
                detached=current.get("detached") is True,
                bare=current.get("bare") is True,
                locked=current.get("locked") if isinstance(current.get("locked"), str) else None,
                prunable=current.get("prunable") if isinstance(current.get("prunable"), str) else None,
            )
        )
        current.clear()

    for item in payload.split("\0"):
        if not item:
            flush()
            continue
        key, separator, value = item.partition(" ")
        current[key] = value if separator else True
    flush()
    return tuple(records)


def list_worktree_registrations(repository: RepositoryFacts) -> tuple[WorktreeRegistration, ...]:
    completed = _git(["worktree", "list", "--porcelain", "-z"], common_dir=repository.common_dir)
    return _parse_worktree_porcelain(completed.stdout)


def _dirty_paths(path: Path) -> tuple[str, ...]:
    payload = _git(
        ["status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=path,
    ).stdout
    rows = [item for item in payload.split("\0") if item]
    return tuple(sorted(rows))


def inspect_registered_worktree(
    repository: RepositoryFacts,
    registration: WorktreeRegistration,
) -> WorktreeFacts:
    discovered_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        local = inspect_repository(registration.path)
        head = _git(["rev-parse", "--verify", "HEAD^{commit}"], cwd=registration.path).stdout.strip()
        symbolic = _git(["symbolic-ref", "-q", "HEAD"], cwd=registration.path, check=False)
        branch_ref = symbolic.stdout.strip() if symbolic.returncode == 0 else None
        registrations = list_worktree_registrations(repository)
        primary_path = registrations[0].path if registrations else registration.path
        return WorktreeFacts(
            path=registration.path,
            common_dir=local.common_dir,
            git_dir=local.git_dir,
            head=head,
            branch_ref=branch_ref,
            topology="primary" if registration.path == primary_path else "linked",
            dirty_paths=_dirty_paths(registration.path),
            discovered_at=discovered_at,
            registration=registration,
        )
    except LifecycleContractError as exc:
        if exc.code != "git_fact_unavailable":
            raise
        return WorktreeFacts(
            path=registration.path,
            common_dir=None,
            git_dir=None,
            head=None,
            branch_ref=None,
            topology="registered",
            dirty_paths=(),
            discovered_at=discovered_at,
            registration=registration,
            inspection_error=exc.code,
        )


def discover_worktree_facts(repository: RepositoryFacts) -> tuple[WorktreeFacts, ...]:
    registrations = list_worktree_registrations(repository)
    return tuple(inspect_registered_worktree(repository, row) for row in registrations)


def find_registration(repository: RepositoryFacts, path: Path | str) -> WorktreeRegistration | None:
    expected = Path(path).resolve()
    return next((row for row in list_worktree_registrations(repository) if row.path == expected), None)


def local_branch_head(repository: RepositoryFacts, branch_ref: str) -> str | None:
    completed = _git(
        ["rev-parse", "--verify", "--quiet", f"{branch_ref}^{{commit}}"],
        common_dir=repository.common_dir,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def branch_checked_out_paths(repository: RepositoryFacts, branch_ref: str) -> tuple[Path, ...]:
    return tuple(
        row.path
        for row in list_worktree_registrations(repository)
        if row.registered_branch_ref == branch_ref
    )


def run_common_git(repository: RepositoryFacts, args: Iterable[str]) -> subprocess.CompletedProcess[str]:
    return _git(list(args), common_dir=repository.common_dir)


__all__ = [
    "RepositoryFacts",
    "WorktreeFacts",
    "WorktreeRegistration",
    "branch_checked_out_paths",
    "discover_worktree_facts",
    "find_registration",
    "inspect_registered_worktree",
    "inspect_repository",
    "list_worktree_registrations",
    "local_branch_head",
    "run_common_git",
]
