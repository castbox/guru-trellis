from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Any

from runtime.io import CommandError


ARTIFACTS = (
    ("PRD", "prd.md", "需求、范围、验收标准"),
    ("Design", "design.md", "技术设计与取舍"),
    ("Implement Plan", "implement.md", "执行计划与验证计划"),
)


def _repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".trellis").is_dir():
            return candidate
    process = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=current,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != 0:
        raise CommandError(
            "invalid_arguments",
            "arguments.--root",
            "Pass a path inside a Trellis repository.",
        )
    return Path(process.stdout.strip()).resolve()


def _task_dir(root: Path, value: str | None) -> Path:
    if value:
        supplied = Path(value)
        candidates = (supplied, root / supplied, root / ".trellis/tasks" / supplied)
    else:
        process = subprocess.run(
            ["python3", "./.trellis/scripts/task.py", "current"],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        candidates = (root / process.stdout.strip(),) if process.returncode == 0 and process.stdout.strip() else ()
    for candidate in candidates:
        resolved = candidate if candidate.is_absolute() else root / candidate
        if resolved.is_dir() and not resolved.is_symlink():
            resolved = resolved.resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                continue
            return resolved
    raise CommandError(
        "unsafe_path",
        "arguments.--task",
        "Pass a non-symlink Trellis task directory below the repository root.",
    )


def run(argv: list[str]) -> dict[str, Any]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--task")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError(
            "invalid_arguments",
            "arguments",
            "Use the exact command help contract.",
        ) from exc
    root = _repo_root(Path(args.root or Path.cwd()))
    task_dir = _task_dir(root, args.task)
    relative = task_dir.relative_to(root).as_posix()
    artifacts = []
    for label, filename, purpose in ARTIFACTS:
        path = task_dir / filename
        exists = path.is_file()
        artifacts.append(
            {
                "label": label,
                "filename": filename,
                "purpose": purpose,
                "exists": exists,
                "status": "已生成" if exists else "未生成",
                "path": path.relative_to(root).as_posix(),
                "absolute_path": str(path),
                "link": str(path) if exists else "",
            }
        )
    return {
        "status": "ok",
        "task_dir": str(task_dir),
        "task_dir_relative": relative,
        "archived": relative.startswith(".trellis/tasks/archive/"),
        "markdown_artifacts": artifacts,
    }
