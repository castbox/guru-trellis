"""Read project worktree path facts without selecting or acquiring a checkout."""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from runtime.base_selection import _scalar
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import RepositoryFacts, inspect_repository, list_worktree_registrations


CONFIG_PATH = Path(".trellis/guru-team/config.yml")


@dataclass(frozen=True)
class WorktreePaths:
    primary_root: Path
    config_path: Path
    worktree_root: Path

    def target(self, name: str, checkout_root: str | None = None) -> Path:
        if not name or name in {".", ".."} or "/" in name or "\\" in name:
            raise LifecycleContractError("invalid_worktree_name", "worktree_name", "Use one directory name for the new worktree.")
        target = (self.worktree_root / name).resolve()
        if checkout_root is not None:
            planned = Path(checkout_root)
            if not planned.is_absolute() or planned.resolve() != target:
                raise LifecycleContractError("configured_checkout_mismatch", "checkout_root", f"Review the configured target {target} and correct the plan before creation.")
        return target


def _primary_root(repository: RepositoryFacts) -> Path:
    if repository.git_dir == repository.common_dir:
        return repository.context_path

    def verified(candidate: Path) -> bool:
        try:
            facts = inspect_repository(candidate)
        except LifecycleContractError:
            return False
        return (facts.context_path == candidate.resolve()
                and facts.common_dir == repository.common_dir
                and facts.git_dir == repository.common_dir)

    configured = subprocess.run(
        ["git", f"--git-dir={repository.common_dir}", "config", "--get", "core.worktree"],
        text=True, capture_output=True, check=False,
    )
    configured_path = None
    if configured.returncode == 0 and configured.stdout.strip():
        path = Path(configured.stdout.strip())
        configured_path = (repository.common_dir / path).resolve() if not path.is_absolute() else path.resolve()
        if verified(configured_path):
            return configured_path
    registrations = list_worktree_registrations(repository)
    # The primary slot is only a candidate: separate gitdirs can list metadata here.
    if registrations and not registrations[0].bare:
        candidate = registrations[0].path
        if candidate != configured_path and verified(candidate):
            return candidate
    raise LifecycleContractError("primary_anchor_unavailable", "git.primary_root", "Run from the primary checkout or configure a verifiable core.worktree for this Git common directory.")


def _configured_root(root: Path) -> str:
    path = root / CONFIG_PATH
    if not path.is_file():
        return ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw[:1].isspace() or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        if key.strip() != "worktree_root":
            continue
        # The existing scalar subset permits quotes and ordinary inline comments.
        quote = None
        for index, char in enumerate(value):
            if char in {"'", '"'} and (index == 0 or value[index - 1] != "\\"):
                quote = None if quote == char else char if quote is None else quote
            if char == "#" and quote is None and (index == 0 or value[index - 1].isspace()):
                value = value[:index]
                break
        scalar = _scalar(value)
        if scalar is None:
            return ""
        if not isinstance(scalar, str):
            raise LifecycleContractError("invalid_worktree_root", "config.worktree_root", "Use an empty, relative or absolute path scalar.")
        return scalar
    return ""


def _resolve_root(primary: Path, value: str) -> Path:
    if not value:
        return (primary.parent / f"{primary.name}-worktrees").resolve()
    path = Path(value)
    return (primary / path).resolve() if not path.is_absolute() else path.resolve()


def resolve_worktree_paths(start: Path) -> WorktreePaths:
    repository = inspect_repository(start)
    primary = _primary_root(repository)
    root = _resolve_root(primary, _configured_root(primary))
    invocation = repository.context_path
    if invocation != primary:
        local = _configured_root(invocation)
        if local and _resolve_root(primary, local) != root:
            raise LifecycleContractError("worktree_config_conflict", "config.worktree_root", "Reconcile the nonempty invocation worktree_root with the primary project configuration before creating a worktree.")
    return WorktreePaths(primary, primary / CONFIG_PATH, root)
