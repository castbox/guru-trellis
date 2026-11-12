"""Shared deterministic Git, locator and planning facts; no semantic decisions."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from runtime.io import CommandError


def digest(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def file_set_identity(repo: Path, paths: list[str]) -> str:
    rows = []
    for path in sorted(paths):
        _validate_repo_path(repo, path, "public_input.target.planning_paths", must_exist=True)
        rows.append({"path": path, "content_sha256": hashlib.sha256((repo / path).read_bytes()).hexdigest()})
    return digest(rows)


def _validate_locator(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise CommandError("unsafe_path", field, "Use a non-empty call-local locator.")
    path_value = value[5:] if value.startswith("path:") else value
    if path_value.startswith("/") or ".." in Path(path_value).parts:
        raise CommandError("unsafe_path", field, "Use a repository-relative locator without parent traversal.")


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise CommandError("stale_identity", "public_input.target", "Return to the original caller, reread current Git facts and applicability, and construct any required fresh invocation without replaying this envelope.", 3)
    return proc.stdout.strip()


def _delivery_planning_directory(repo: Path, target: dict) -> Path:
    """Resolve the caller's object through the original identity and selection owners."""
    from runtime.delivery_projection.adapter import DeliveryProjection
    from runtime.task_lifecycle.errors import LifecycleContractError
    from runtime.task_lifecycle.branch_resolution import _control_state
    from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
    from runtime.task_lifecycle.git_facts import inspect_repository
    from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore

    task_path = Path(target["task_ref"])
    if task_path.parts[:2] != (".trellis", "tasks"):
        task_path = Path(".trellis/tasks") / task_path
    _validate_locator(task_path.as_posix(), "public_input.target.task_ref")
    try:
        projection = DeliveryProjection(repo, task_path.as_posix())
        key = target["delivery_key"]
        # Public parsing validates the opaque key before the shared checkout
        # reader accesses its identity. Context selection is checked separately.
        projection.resolve(key)
        projection._require_explicit_task(key)
        repository = inspect_repository(repo)
        binding, ownership = _control_state(BranchBindingStore(repository), ResourceLedgerStore(repository),
                                             TaskLifecycleKey(key["task_id"], key["lifecycle_generation"]))
        if binding is None or ownership is None:
            raise LifecycleContractError("branch_association_missing", "control_state",
                                         "Return to the original Branch/Ensure owner for current C4/C5 facts.")
        current = projection.current(key)
        if current.get("kind") == "error":
            raise LifecycleContractError(current["code"], "session", current["message"])
        if current.get("kind") != "current" or current.get("key") != key:
            raise CommandError("stale_identity", "public_input.target.delivery_key",
                               "Return to the original identity/selection owner for this exact current Delivery; an available context cannot use explicit fallback.", 3)
        return projection.planning_directory(key).relative_to(repo.resolve())
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc


def verify_current_facts(public_input: dict, repo: Path) -> None:
    target = public_input["target"]
    planning_directory = _delivery_planning_directory(repo, target) if "delivery_key" in target else None
    current_head = _git(repo, "rev-parse", "HEAD")
    current_fields = {"checkout_head", "task_head", "review_head", "review_commit"}
    for key, value in target.items():
        if key.endswith("_head") or key == "review_commit":
            _git(repo, "cat-file", "-e", f"{value}^{{commit}}")
            if key in current_fields and value != current_head:
                raise CommandError("stale_identity", f"public_input.target.{key}", "Return to the original caller, reread current HEAD and applicability, and construct any required fresh invocation without replaying this envelope.", 3)
        if key.endswith("_path"):
            _validate_repo_path(repo, value, f"public_input.target.{key}", must_exist=True)
        elif key.endswith("_paths"):
            for index, item in enumerate(value):
                _validate_repo_path(repo, item, f"public_input.target.{key}.{index}", must_exist=False)
    if "planning_identity" in target:
        planning_paths = [(planning_directory / name).as_posix() for name in ("prd.md", "design.md", "implement.md")]
        if "planning_paths" in target and set(target["planning_paths"]) != set(planning_paths):
            raise CommandError("stale_identity", "public_input.target.planning_paths",
                               "Use the exact three planning files belonging to the supplied DeliveryKey.", 3)
        if target["planning_identity"] != file_set_identity(repo, planning_paths):
            raise CommandError("stale_identity", "public_input.target.planning_identity", "Return to the original caller, reread current planning and applicability, and construct any required fresh invocation without replaying this envelope.", 3)
    if "author_identity" in target:
        if target["author_identity"] != file_set_identity(repo, target["author_paths"]):
            raise CommandError("stale_identity", "public_input.target.author_identity", "Return to Author, reread current source/candidate evidence and applicability, and construct any required fresh invocation without replaying this envelope.", 3)
    for row in public_input["candidate_locators"]:
        for locator in row["locators"]:
            if locator.startswith("path:"):
                _validate_repo_path(repo, locator[5:].split(":", 1)[0], f"candidate.{row['candidate_ref']}", must_exist=True)


def _validate_repo_path(repo: Path, value: str, field: str, *, must_exist: bool) -> None:
    _validate_locator(value, field)
    candidate = repo / value
    current = repo
    for part in Path(value).parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise CommandError("unsafe_path", field, "Do not read qualification evidence through a symlink.")
    if must_exist and not candidate.is_file():
        raise CommandError("stale_identity", field, "Return to the original caller, reread the current locator and applicability, and construct any required fresh invocation without replaying this envelope.", 3)
