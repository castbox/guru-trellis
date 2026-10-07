"""Migration-private preimages and ordinary-work freshness, never Git rollback."""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path


class MigrationError(ValueError):
    pass


def run(argv: list[str], root: Path) -> str:
    result = subprocess.run(argv, cwd=root, text=True, capture_output=True)
    if result.returncode:
        # Commands may report private business content. Do not echo their output.
        raise MigrationError(f"Command failed ({result.returncode}): {Path(argv[0]).name}")
    return result.stdout


def git(root: Path, *argv: str) -> str:
    return run(["git", *argv], root).strip()


def relative_file(root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or relative != path.as_posix() or ".." in path.parts or "." in path.parts:
        raise MigrationError(f"Non-canonical migration path: {relative}")
    current = root
    for component in path.parts:
        current /= component
        if current.is_symlink():
            raise MigrationError(f"Symlink migration path: {relative}")
    if current.exists() and not current.is_file():
        raise MigrationError(f"Non-file migration path: {relative}")
    return current


def state(path: Path) -> dict:
    if not path.exists():
        return {"sha256": None, "mode": None}
    if path.is_symlink() or not path.is_file():
        raise MigrationError("Migration footprint contains a non-regular file")
    return {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "mode": stat.S_IMODE(path.stat().st_mode)}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_files(root: Path) -> list[str]:
    # Ignored runtime and historical traces are intentionally not a business index.
    result = run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], root)
    return sorted(set(result.split("\0")) - {""})


def business_state(root: Path, managed_paths: set[str], projections: dict[str, dict] | None = None) -> str:
    facts = {
        "head": git(root, "rev-parse", "HEAD"),
        "index": git(root, "ls-files", "--stage", "-z"),
        "files": {p: state(relative_file(root, p)) for p in repo_files(root)
                  if p not in managed_paths and not p.startswith((".trellis/tasks/archive/", ".trellis/workspace/", ".trellis/agent-traces/")) and p != ".trellis/.developer"},
    }
    for path, projected in (projections or {}).items():
        if path in facts["files"]:
            facts["files"][path] = projected
    # Only this local rollback comparison token persists, never a business index.
    return hashlib.sha256(json.dumps(facts, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def snapshot(root: Path, recovery: Path, paths: set[str], controls: dict[str, Path]) -> dict:
    rows = {}
    destinations = {f"repo:{p}": relative_file(root, p) for p in paths}
    destinations.update({f"control:{k}": p for k, p in controls.items()})
    for index, (key, path) in enumerate(sorted(destinations.items())):
        row = state(path)
        row["backup"] = f"preimages/{index}"
        if row["sha256"] is not None:
            backup = recovery / row["backup"]
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_bytes(path.read_bytes())
        rows[key] = row
    return rows


def destinations(root: Path, checkpoint: dict) -> dict[str, Path]:
    paths = {k: relative_file(root, k[5:]) for k in checkpoint["preimages"] if k.startswith("repo:")}
    paths.update({f"control:{k}": Path(v) for k, v in checkpoint["controls"].items()})
    return paths


def current_baseline(root: Path, checkpoint: dict) -> dict:
    return {k: state(p) for k, p in destinations(root, checkpoint).items()}


def content_token(paths: dict[str, Path]) -> str:
    facts = {key: state(path) for key, path in sorted(paths.items())}
    return hashlib.sha256(json.dumps(facts, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def task_token(root: Path, checkpoint: dict) -> str:
    plan = checkpoint["plan"]["core_plan"]
    # Preserved deferred task preimages are also part of rollback restoration.
    return content_token({row["task_ref"]: relative_file(root, row["task_ref"] + "/task.json")
                          for row in plan["tasks"] + plan.get("deferred_tasks", []) + plan.get("current_tasks", [])})


def control_token(checkpoint: dict) -> str:
    # The preset owns its Python pointers, including aliases of the same path.
    pointers = {Path(checkpoint["controls"][key]).resolve()
                for key in ("python_common", "python_checkout") if key in checkpoint["controls"]}
    return content_token({key: Path(path) for key, path in checkpoint["controls"].items()
                          if Path(path).resolve() not in pointers})


def restore(root: Path, recovery: Path, checkpoint: dict) -> None:
    # Caller has checked the post-write baseline and ordinary new-work boundary.
    for key, path in destinations(root, checkpoint).items():
        row = checkpoint["preimages"][key]
        if row["sha256"] is None:
            path.unlink(missing_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((recovery / row["backup"]).read_bytes())
            os.chmod(path, row["mode"])
