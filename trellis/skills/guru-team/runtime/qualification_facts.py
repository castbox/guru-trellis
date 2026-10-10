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
        raise CommandError("stale_identity", "public_input.target", "Reread the current Git identity and rerun qualification.", 3)
    return proc.stdout.strip()


def verify_current_facts(public_input: dict, repo: Path) -> None:
    target = public_input["target"]
    current_head = _git(repo, "rev-parse", "HEAD")
    current_fields = {"checkout_head", "task_head", "review_head", "review_commit"}
    for key, value in target.items():
        if key.endswith("_head") or key == "review_commit":
            _git(repo, "cat-file", "-e", f"{value}^{{commit}}")
            if key in current_fields and value != current_head:
                raise CommandError("stale_identity", f"public_input.target.{key}", "Reread the current checkout HEAD and rerun qualification.", 3)
        if key.endswith("_path"):
            _validate_repo_path(repo, value, f"public_input.target.{key}", must_exist=True)
        elif key.endswith("_paths"):
            for index, item in enumerate(value):
                _validate_repo_path(repo, item, f"public_input.target.{key}.{index}", must_exist=False)
    if "planning_identity" in target:
        if "planning_paths" in target:
            planning_paths = target["planning_paths"]
        else:
            task_ref = target["task_ref"]
            task_path = Path(task_ref)
            if task_path.parts[:2] != (".trellis", "tasks"):
                task_path = Path(".trellis/tasks") / task_path
            planning_paths = [(task_path / name).as_posix() for name in ("prd.md", "design.md", "implement.md")]
        if target["planning_identity"] != file_set_identity(repo, planning_paths):
            raise CommandError("stale_identity", "public_input.target.planning_identity", "Reread the current planning files and rerun qualification.", 3)
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
        raise CommandError("stale_identity", field, "Reread the current repository locator and rerun qualification.", 3)
