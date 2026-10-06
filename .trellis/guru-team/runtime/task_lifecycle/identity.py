from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterator

from .errors import LifecycleContractError
from .git_facts import commit_path_bytes, inspect_repository
from .source import normalize_repo_ref, normalize_source


TASK_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
ACTIVE_TASK_REF = re.compile(r"^\.trellis/tasks/(?!archive(?:/|$))[^/]+$")
ARCHIVE_TASK_REF = re.compile(r"^\.trellis/tasks/archive/[0-9]{4}-[0-9]{2}/[^/]+$")
LEGACY_URL_ISSUE_HINT = re.compile(r"^GitHub issue: https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/issues/([1-9][0-9]*)$")
_MISSING = object()
_CURRENT_TASK_FIELDS = frozenset({
    "id", "name", "lifecycle_generation", "source", "title", "description",
    "status", "dev_type", "scope", "package", "priority", "createdAt",
    "completedAt", "base_branch", "worktree_path", "commit", "pr_url",
    "children", "parent", "relatedFiles", "notes", "meta",
})
_LEGACY_TASK_FIELDS = (_CURRENT_TASK_FIELDS - {"lifecycle_generation", "source"}) | {
    "branch", "creator", "assignee", "subtasks",
}


@dataclass(frozen=True)
class TaskArtifactIdentity:
    task_id: str
    task_ref: str
    lifecycle_generation: int
    lifecycle_state: str
    legacy: bool = False

    @property
    def lifecycle_key(self) -> tuple[str, int]:
        return self.task_id, self.lifecycle_generation

    def as_dto(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_ref": self.task_ref,
            "lifecycle_generation": self.lifecycle_generation,
        }


@dataclass(frozen=True)
class ArchivedIssueCandidate:
    task_id: str
    task_ref: str
    lifecycle_generation: int
    archive_head: str


def normalize_task_id(value: Any, *, field_path: str = "task_id") -> str:
    if not isinstance(value, str) or not TASK_ID_PATTERN.fullmatch(value):
        raise LifecycleContractError(
            "invalid_task_id",
            field_path,
            "Use an [A-Za-z0-9][A-Za-z0-9._-]* value.",
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


def _read_task_metadata(repo_root: Path, task_ref: str) -> dict[str, Any]:
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
    except LifecycleContractError:
        raise
    except (OSError, ValueError) as exc:
        raise LifecycleContractError("invalid_task_ref", ref, "Keep the task artifact inside the selected repository.") from exc
    if not isinstance(data, dict):
        raise LifecycleContractError("invalid_task_metadata", f"{ref}/task.json", "Use one task metadata object.")
    return data


def _read_identity(repo_root: Path, task_ref: str) -> TaskArtifactIdentity:
    ref = normalize_task_ref(task_ref)
    data = _read_task_metadata(repo_root, ref)
    archived = ref.startswith(".trellis/tasks/archive/")
    current = _current_task_metadata(data, archived=archived)
    legacy = not current and (archived or _known_legacy_active_metadata(data))
    if not current and not legacy:
        raise LifecycleContractError("unsupported_legacy_task", ref, "The task metadata does not match the current upstream schema.")
    return TaskArtifactIdentity(
        normalize_task_id(data.get("id"), field_path=f"{ref}/task.json.id"),
        ref,
        0 if legacy else lifecycle_generation(data, field_path=f"{ref}/task.json.lifecycle_generation"),
        "archived" if archived else "active",
        legacy,
    )


def _known_legacy_active_metadata(data: dict[str, Any]) -> bool:
    """Recognize old headers for reservation only, never lifecycle use."""

    if (
        not set(data) <= _LEGACY_TASK_FIELDS
        or not {"id", "name", "title", "status", "creator", "assignee"} <= set(data)
    ):
        return False
    strings = {"id", "name", "title", "description", "status", "priority", "createdAt", "notes", "creator", "assignee"}
    nullable = {"dev_type", "scope", "package", "completedAt", "base_branch", "worktree_path", "commit", "pr_url", "parent", "branch"}
    return (
        all(isinstance(data[field], str) for field in strings & set(data))
        and all(data[field] is None or isinstance(data[field], str) for field in nullable & set(data))
        and all(isinstance(data[field], list) and all(isinstance(item, str) for item in data[field])
                for field in {"children", "relatedFiles", "subtasks"} & set(data))
        and ("meta" not in data or isinstance(data["meta"], dict))
    )


def _current_task_metadata(data: dict[str, Any], *, archived: bool) -> bool:
    if set(data) not in (_CURRENT_TASK_FIELDS, _CURRENT_TASK_FIELDS | {"branch"}):
        return False
    try:
        lifecycle_generation(data)
        normalize_source(data["source"])
    except LifecycleContractError:
        return False
    required_strings = ("name", "title", "description", "status", "priority", "createdAt", "notes")
    nullable_strings = ("dev_type", "scope", "package", "completedAt", "base_branch", "worktree_path", "commit", "pr_url", "parent")
    return (
        (not archived or data["status"] == "completed")
        and all(isinstance(data[field], str) for field in required_strings)
        and all(data[field] is None or isinstance(data[field], str) for field in nullable_strings)
        and all(isinstance(data[field], list) and all(isinstance(item, str) for item in data[field])
                for field in ("children", "relatedFiles"))
        and isinstance(data["meta"], dict)
        and ("branch" not in data or data["branch"] is None or isinstance(data["branch"], str))
    )


def _task_identities(repo_root: Path) -> tuple[TaskArtifactIdentity, ...]:
    root = repo_root.resolve()
    rows = []
    for ref in _task_refs(root):
        try:
            rows.append(_read_identity(root, ref))
        except LifecycleContractError:
            if not ref.startswith(".trellis/tasks/archive/"):
                raise
    return tuple(rows)


def task_inventory(repo_root: Path) -> tuple[TaskArtifactIdentity, ...]:
    return tuple(row for row in _task_identities(repo_root) if not row.legacy)


def task_identity_exists(repo_root: Path, task_id: str, task_ref: str) -> bool:
    """Check one proposed identity without requiring unrelated history to be unique."""

    key = task_id_key(task_id)
    ref = normalize_task_ref(task_ref)
    root = repo_root.resolve()
    for item in _task_refs(root):
        if item == ref:
            return True
        if not item.startswith(".trellis/tasks/archive/"):
            if not (root / item / "task.json").exists():
                continue
            existing = _read_identity(root, item)
            if existing.task_id.casefold() == key:
                return True
            continue
        try:
            data = _read_task_metadata(root, item)
            existing_key = task_id_key(data.get("id"), field_path=f"{item}/task.json.id")
        except LifecycleContractError as exc:
            if exc.code in {"task_not_found", "invalid_task_metadata", "invalid_task_id"}:
                continue
            raise
        if existing_key == key:
            return True
    return False


def resolve_task_ref(repo_root: Path, task_ref: Any, *, expected_task_id: Any | None = None) -> TaskArtifactIdentity:
    selected = _read_identity(repo_root.resolve(), normalize_task_ref(task_ref))
    if selected.legacy:
        raise LifecycleContractError("unsupported_legacy_task", selected.task_ref, "Old records reserve identity but are not lifecycle candidates.")
    rows = _task_identities(repo_root)
    current = next((row for row in rows if row.task_ref == selected.task_ref), None)
    if current is None:
        raise LifecycleContractError(
            "invalid_task_ref", selected.task_ref, "Resolve one canonical task artifact from the repository inventory."
        )
    if len([row for row in rows if row.task_id.casefold() == current.task_id.casefold()]) > 1:
        raise LifecycleContractError("task_id_casefold_collision", "task_id", "Resolve the duplicate TaskId before lifecycle use.")
    if expected_task_id is not None and current.task_id != normalize_task_id(expected_task_id, field_path="expected_task_id"):
        raise LifecycleContractError(
            "invalid_task_identity", "expected_task_id", "Use the immutable TaskId declared by the selected task artifact."
        )
    return current


def resolve_task_id(repo_root: Path, task_id: Any) -> TaskArtifactIdentity:
    requested = normalize_task_id(task_id)
    rows = _task_identities(repo_root)
    matches = [row for row in rows if row.task_id.casefold() == requested.casefold()]
    if not matches:
        raise LifecycleContractError("task_not_found", "task_id", "Select an existing active or archived TaskId.")
    if len(matches) != 1:
        raise LifecycleContractError("task_id_casefold_collision", "task_id", "Resolve duplicate canonical task artifacts.")
    if matches[0].legacy:
        raise LifecycleContractError("unsupported_legacy_task", matches[0].task_ref, "Old records reserve identity but are not lifecycle candidates.")
    if matches[0].task_id != requested:
        raise LifecycleContractError("invalid_task_identity", "task_id", "Use the exact TaskId spelling.")
    return matches[0]


def discover_archived_issue_candidate(
    repo_root: Path, repo_ref: str, issue_number: int, archive_head: str,
) -> ArchivedIssueCandidate:
    """Locate one exact Issue archive; legacy matches are diagnostic only."""

    repository = inspect_repository(repo_root)
    source_repo = normalize_repo_ref(repo_ref)
    if type(issue_number) is not int or issue_number < 1:
        raise LifecycleContractError("invalid_source_relation", "issue_number", "Use a positive source Issue number.")
    matches: list[ArchivedIssueCandidate] = []
    origin_is_source = origin_matches(repository.context_path, source_repo)
    identities = _task_identities(repo_root)
    for artifact in identities:
        if artifact.lifecycle_state != "archived":
            continue
        summary_ref = f"{artifact.task_ref}/finish-summary.json"
        task_ref = f"{artifact.task_ref}/task.json"
        summary_bytes = commit_path_bytes(repository, archive_head, summary_ref)
        task_bytes = commit_path_bytes(repository, archive_head, task_ref)
        if summary_bytes is None or task_bytes is None:
            continue
        try:
            summary = json.loads(summary_bytes)
            task = json.loads(task_bytes)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(summary, dict) or not isinstance(task, dict):
            continue
        if "source" in task:
            try:
                source = normalize_source(task["source"])
            except LifecycleContractError:
                continue
            matched = (source.get("kind"), source.get("repo_ref"), source.get("number"), source.get("disposition")) == (
                "issue", source_repo, issue_number, "exact_source",
            )
        else:
            clues: list[set[int]] = []
            github = summary.get("github", {})
            indexed = github.get("source_issues") if isinstance(github, dict) else None
            if origin_is_source and isinstance(indexed, list) and indexed:
                numbers = {number for number in indexed if type(number) is int and number > 0}
                if numbers:
                    clues.append(numbers)
            scope = task.get("scope", "")
            url_hint = LEGACY_URL_ISSUE_HINT.fullmatch(scope) if isinstance(scope, str) else None
            if url_hint and url_hint[1] == source_repo:
                clues.append({int(url_hint[2])})
            if url_hint and url_hint[1] != source_repo and any(issue_number in clue for clue in clues):
                raise LifecycleContractError("archived_issue_candidate_not_unique", "source_issue", "Conflicting archive Issue repositories require manual disposition.")
            if len(clues) > 1 and any(clue != clues[0] for clue in clues[1:]) and any(issue_number in clue for clue in clues):
                raise LifecycleContractError("archived_issue_candidate_not_unique", "source_issue", "Conflicting archive Issue clues require manual disposition.")
            matched = bool(clues) and all(clue == {issue_number} for clue in clues)
        if not matched:
            continue
        if (
            task.get("id") != artifact.task_id
            or (not artifact.legacy and normalize_generation(task.get("lifecycle_generation", 0)) != artifact.lifecycle_generation)
            or task.get("status") != "completed"
            or summary.get("task", {}).get("archive_dir") != artifact.task_ref
            or summary.get("task", {}).get("status") != "completed"
        ):
            continue
        matches.append(ArchivedIssueCandidate(artifact.task_id, artifact.task_ref, artifact.lifecycle_generation, archive_head))
    if not matches:
        raise LifecycleContractError(
            "archived_issue_candidate_not_found", "source_issue",
            "No archive has a unique exact source Issue clue; continue normal task discovery.",
        )
    if len(matches) != 1:
        raise LifecycleContractError(
            "archived_issue_candidate_not_unique", "source_issue",
            "Review the exact source Issue and archive Git identity before Reactivate.",
        )
    if any(row.legacy for row in identities if row.task_ref == matches[0].task_ref):
        raise LifecycleContractError("unsupported_legacy_task", matches[0].task_ref, "Old archives are read-only diagnostics, not Reactivate candidates.")
    return matches[0]


def origin_matches(repo_root: Path, repo_ref: str) -> bool:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"], cwd=repo_root, text=True, capture_output=True, check=False,
    )
    if result.returncode != 0:
        return False
    url = result.stdout.strip().casefold()
    repo_ref = repo_ref.casefold()
    return url in (f"https://github.com/{repo_ref}", f"https://github.com/{repo_ref}.git",
                   f"git@github.com:{repo_ref}", f"git@github.com:{repo_ref}.git",
                   f"ssh://git@github.com/{repo_ref}", f"ssh://git@github.com/{repo_ref}.git")


__all__ = [
    "ArchivedIssueCandidate", "TaskArtifactIdentity", "discover_archived_issue_candidate", "lifecycle_generation", "normalize_generation", "normalize_task_id",
    "normalize_task_ref", "origin_matches", "resolve_task_id", "resolve_task_ref", "task_id_key", "task_inventory",
]
