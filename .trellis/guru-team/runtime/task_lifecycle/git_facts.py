from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
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


@dataclass(frozen=True)
class CheckoutStateSnapshot:
    path: Path
    head: str
    branch_ref: str
    index_sha256: str
    worktree_sha256: str
    status_sha256: str


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


def list_local_branch_refs(repository: RepositoryFacts) -> tuple[tuple[str, str], ...]:
    payload = _git(
        [
            "for-each-ref",
            "--format=%(refname)%00%(objectname)%00",
            "refs/heads",
        ],
        common_dir=repository.common_dir,
    ).stdout
    fields = payload.split("\0")
    rows: list[tuple[str, str]] = []
    for index in range(0, len(fields) - 1, 2):
        branch_ref = fields[index].strip()
        head = fields[index + 1].strip()
        if branch_ref and head:
            rows.append((branch_ref, head))
    return tuple(sorted(rows))


def commit_path_bytes(repository: RepositoryFacts, commit: str, path: str) -> bytes | None:
    completed = subprocess.run(
        ["git", f"--git-dir={repository.common_dir}", "show", f"{commit}:{path}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode == 0:
        return completed.stdout
    missing = subprocess.run(
        ["git", f"--git-dir={repository.common_dir}", "cat-file", "-e", f"{commit}^{{commit}}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if missing.returncode != 0:
        raise LifecycleContractError(
            "git_fact_unavailable",
            "commit",
            "Use one live commit identity from the selected repository.",
        )
    return None


def is_ancestor(repository: RepositoryFacts, ancestor: str, descendant: str) -> bool:
    completed = _git(
        ["merge-base", "--is-ancestor", ancestor, descendant],
        common_dir=repository.common_dir,
        check=False,
    )
    if completed.returncode not in {0, 1}:
        raise LifecycleContractError(
            "git_fact_unavailable",
            "ancestry",
            "Restore readable commit ancestry before branch mutation.",
        )
    return completed.returncode == 0


def git_operation_in_progress(checkout: Path | str) -> bool:
    path = Path(checkout).resolve()
    names = (
        "MERGE_HEAD",
        "CHERRY_PICK_HEAD",
        "REVERT_HEAD",
        "BISECT_LOG",
        "rebase-apply",
        "rebase-merge",
        "sequencer",
    )
    for name in names:
        resolved = _git(["rev-parse", "--git-path", name], cwd=path).stdout.strip()
        candidate = Path(resolved)
        if not candidate.is_absolute():
            candidate = path / candidate
        if candidate.exists():
            return True
    return False


def run_checkout_git(checkout: Path | str, args: Iterable[str]) -> subprocess.CompletedProcess[str]:
    return _git(list(args), cwd=Path(checkout).resolve())


def _git_bytes(checkout: Path, args: Sequence[str]) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=checkout,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise LifecycleContractError(
            "git_fact_unavailable",
            "checkout_state",
            "Restore a readable checkout before capturing mutation pre-state.",
        )
    return completed.stdout


def _index_identity(checkout: Path) -> str:
    raw_path = _git(["rev-parse", "--git-path", "index"], cwd=checkout).stdout.strip()
    index_path = Path(raw_path)
    if not index_path.is_absolute():
        index_path = checkout / index_path
    try:
        payload = index_path.read_bytes()
    except OSError as exc:
        raise LifecycleContractError(
            "git_fact_unavailable",
            "checkout_index",
            "Restore readable index bytes before branch mutation.",
        ) from exc
    return sha256(payload).hexdigest()


def _worktree_identity(checkout: Path) -> str:
    names = _git_bytes(
        checkout,
        ["ls-files", "-z", "--cached", "--others", "--exclude-standard"],
    ).split(b"\0")
    digest = sha256()
    for raw_name in sorted(item for item in names if item):
        name = raw_name.decode("utf-8", errors="surrogateescape")
        path = checkout / name
        digest.update(len(raw_name).to_bytes(8, "big"))
        digest.update(raw_name)
        try:
            if path.is_symlink():
                payload = path.readlink().as_posix().encode("utf-8", errors="surrogateescape")
                kind = b"symlink"
            elif path.is_file():
                payload = path.read_bytes()
                kind = b"file"
            elif path.exists():
                payload = b""
                kind = b"other"
            else:
                payload = b""
                kind = b"missing"
        except OSError as exc:
            raise LifecycleContractError(
                "git_fact_unavailable",
                name,
                "Restore readable working-tree bytes before branch mutation.",
            ) from exc
        digest.update(kind)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def capture_checkout_state(checkout: Path | str) -> CheckoutStateSnapshot:
    path = Path(checkout).resolve()
    head = _git(["rev-parse", "--verify", "HEAD^{commit}"], cwd=path).stdout.strip()
    symbolic = _git(["symbolic-ref", "-q", "HEAD"], cwd=path, check=False)
    if symbolic.returncode != 0:
        raise LifecycleContractError(
            "detached_checkout",
            "checkout",
            "Use one branch-bound registered checkout for branch mutation.",
        )
    branch_ref = symbolic.stdout.strip()
    status = _git_bytes(path, ["status", "--porcelain=v2", "-z", "--untracked-files=all"])
    return CheckoutStateSnapshot(
        path=path,
        head=head,
        branch_ref=branch_ref,
        index_sha256=_index_identity(path),
        worktree_sha256=_worktree_identity(path),
        status_sha256=sha256(status).hexdigest(),
    )


def branch_checked_out_paths(repository: RepositoryFacts, branch_ref: str) -> tuple[Path, ...]:
    return tuple(
        row.path
        for row in list_worktree_registrations(repository)
        if row.registered_branch_ref == branch_ref
    )


def run_common_git(repository: RepositoryFacts, args: Iterable[str]) -> subprocess.CompletedProcess[str]:
    return _git(list(args), common_dir=repository.common_dir)


__all__ = [
    "CheckoutStateSnapshot",
    "RepositoryFacts",
    "WorktreeFacts",
    "WorktreeRegistration",
    "branch_checked_out_paths",
    "capture_checkout_state",
    "commit_path_bytes",
    "discover_worktree_facts",
    "find_registration",
    "git_operation_in_progress",
    "inspect_registered_worktree",
    "inspect_repository",
    "is_ancestor",
    "list_local_branch_refs",
    "list_worktree_registrations",
    "local_branch_head",
    "run_checkout_git",
    "run_common_git",
]
