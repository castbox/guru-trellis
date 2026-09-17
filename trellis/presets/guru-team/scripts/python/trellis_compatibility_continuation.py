"""Continuation and preservation helpers for the Trellis matrix runner."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence


def python_residue(root: Path, sorted_strings: Callable[[Any], list[str]]) -> list[str]:
    return sorted_strings(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.name == "__pycache__"
        or (path.is_file() and path.suffix in {".pyc", ".pyo"})
    )


def assert_no_python_residue(
    root: Path,
    *,
    residue_reader: Callable[[Path], list[str]],
    error_type: type[RuntimeError],
) -> None:
    residue = residue_reader(root)
    if residue:
        raise error_type(
            f"disposable matrix root contains Python bytecode residue: {residue}"
        )


def read_installed_continuation(
    target: Path,
    log: Path,
    *,
    label: str,
    run: Callable[..., str],
    error_type: type[RuntimeError],
) -> str:
    script = target / ".trellis/scripts/get_context.py"
    if not script.is_file() or script.is_symlink():
        raise error_type("installed upstream get_context.py is unavailable")
    output = run(
        (sys.executable, "-B", str(script), "--mode", "continuation"),
        cwd=target,
        env={"PYTHONDONTWRITEBYTECODE": "1"},
        capture=True,
        log=log,
    )
    if not output.strip():
        raise error_type(f"installed continuation read is empty after {label}")
    return output


def snapshot_regular_files(
    target: Path,
    roots: Sequence[Path],
    *,
    error_type: type[RuntimeError],
) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for relative in roots:
        path = target / relative
        candidates = (
            [path]
            if path.is_file() or path.is_symlink()
            else sorted(path.rglob("*"))
            if path.is_dir()
            else []
        )
        for candidate in candidates:
            if candidate.is_symlink() or not candidate.is_file():
                if candidate.is_symlink():
                    raise error_type(
                        "upstream-owned preservation path is a symlink: "
                        f"{candidate.relative_to(target).as_posix()}"
                    )
                continue
            candidate_relative = candidate.relative_to(target).as_posix()
            snapshot[candidate_relative] = hashlib.sha256(
                candidate.read_bytes()
            ).hexdigest()
    return dict(sorted(snapshot.items()))


def upstream_owned_snapshot(
    target: Path,
    platform: str,
    *,
    platform_upstream_paths: Mapping[str, Sequence[Path]],
    snapshot_reader: Callable[[Path, Sequence[Path]], dict[str, str]],
    error_type: type[RuntimeError],
) -> dict[str, str]:
    if platform not in platform_upstream_paths:
        raise error_type(f"unsupported upstream snapshot platform: {platform}")
    required = (
        Path(".trellis/scripts/get_context.py"),
        Path(".trellis/scripts/common/continuation_contract.py"),
        Path(".trellis/scripts/common/git_context.py"),
    )
    optional_shared_entries = (
        Path(".agents/skills/trellis-start"),
        Path(".agents/skills/trellis-continue"),
        Path(".agents/skills/trellis-meta"),
    )
    snapshot = snapshot_reader(
        target,
        (*required, *optional_shared_entries, *platform_upstream_paths[platform]),
    )
    for relative in required:
        if relative.as_posix() not in snapshot:
            raise error_type(
                f"missing upstream-owned continuation helper: {relative.as_posix()}"
            )
    platform_prefixes = tuple(
        relative.as_posix() for relative in platform_upstream_paths[platform]
    )
    if not any(
        path == prefix or path.startswith(prefix + "/")
        for path in snapshot
        for prefix in platform_prefixes
    ):
        raise error_type(f"missing upstream-owned {platform} platform projection")
    return snapshot


def round_trip_workflow_continuation(
    target: Path,
    binary: Sequence[str],
    env: Mapping[str, str],
    workflow_source: str,
    repo_root: Path,
    local_sample: bool,
    work_root: Path,
    *,
    sidecars: Callable[[Path], list[str]],
    run: Callable[..., str],
    preview_and_switch_workflow: Callable[..., None],
    read_continuation: Callable[..., str],
    error_type: type[RuntimeError],
) -> dict[str, Any]:
    work_root.mkdir(parents=True, exist_ok=True)
    workflow = target / ".trellis/workflow.md"
    canonical = repo_root / "trellis/workflows/guru-team/workflow.md"
    if not workflow.is_file() or workflow.is_symlink() or not canonical.is_file():
        raise error_type("Guru workflow is unavailable before round-trip")
    guru_bytes = workflow.read_bytes()
    if guru_bytes != canonical.read_bytes():
        raise error_type("active Guru workflow does not match the exact candidate")
    guru_continuation = read_continuation(
        target, work_root / "guru-before.log", label="initial Guru selection"
    )
    native_continuations: list[str] = []
    guru_continuations = [guru_continuation]
    for iteration in (1, 2):
        if sidecars(target):
            raise error_type("workflow round-trip started with an unresolved sidecar")
        run(
            (*binary, "workflow", "--template", "native", "--force"),
            cwd=target,
            env=env,
            log=work_root / f"native-switch-{iteration}.log",
        )
        native_bytes = workflow.read_bytes()
        if native_bytes == guru_bytes:
            raise error_type("native workflow switch retained stale Guru bytes")
        native_continuation = read_continuation(
            target,
            work_root / f"native-continuation-{iteration}.log",
            label=f"native switch {iteration}",
        )
        if native_continuation == guru_continuation:
            raise error_type("native workflow switch retained stale Guru continuation")
        native_continuations.append(native_continuation)
        switch_root = work_root / f"guru-switch-{iteration}"
        switch_root.mkdir()
        preview_and_switch_workflow(
            target,
            binary,
            env,
            workflow_source,
            repo_root,
            repo_root,
            local_sample,
            switch_root,
            expected_current=native_bytes,
        )
        restored = read_continuation(
            target,
            work_root / f"guru-continuation-{iteration}.log",
            label=f"Guru switch {iteration}",
        )
        if workflow.read_bytes() != guru_bytes or restored != guru_continuation:
            raise error_type("Guru workflow switch did not restore exact continuation")
        guru_continuations.append(restored)
    if len(set(native_continuations)) != 1 or len(set(guru_continuations)) != 1:
        raise error_type("workflow round-trip continuation identity is unstable")
    if sidecars(target):
        raise error_type("workflow round-trip left an unresolved sidecar")
    return {
        "status": "passed",
        "sequence": ["native", "guru-team", "native", "guru-team"],
        "native_continuation_sha256": hashlib.sha256(
            native_continuations[0].encode("utf-8")
        ).hexdigest(),
        "guru_continuation_sha256": hashlib.sha256(
            guru_continuation.encode("utf-8")
        ).hexdigest(),
    }


def reapply_preset_with_preservation(
    source_root: Path,
    target: Path,
    platform: str,
    log: Path,
    continuation_log_root: Path,
    *,
    previous_root: Path | None,
    read_continuation: Callable[..., str],
    upstream_snapshot: Callable[[Path, str], dict[str, str]],
    apply_preset: Callable[..., dict[str, Any]],
    error_type: type[RuntimeError],
) -> dict[str, Any]:
    workflow = target / ".trellis/workflow.md"
    workflow_before = workflow.read_bytes()
    continuation_before = read_continuation(
        target,
        continuation_log_root / "continuation-before-reapply.log",
        label="preset reapply precondition",
    )
    upstream_before = upstream_snapshot(target, platform)
    result = apply_preset(
        source_root,
        target,
        platform,
        log,
        previous_root=previous_root,
    )
    continuation_after = read_continuation(
        target,
        continuation_log_root / "continuation-after-reapply.log",
        label="preset reapply",
    )
    if workflow.read_bytes() != workflow_before:
        raise error_type("preset reapply modified the selected Guru workflow")
    if continuation_after != continuation_before:
        raise error_type("preset reapply modified the selected Guru continuation")
    upstream_after = upstream_snapshot(target, platform)
    if upstream_after != upstream_before:
        before_paths = set(upstream_before)
        after_paths = set(upstream_after)
        changed = sorted(
            path
            for path in before_paths & after_paths
            if upstream_before[path] != upstream_after[path]
        )
        raise error_type(
            "preset reapply modified upstream-owned entries or helpers: "
            f"added={sorted(after_paths - before_paths)} "
            f"removed={sorted(before_paths - after_paths)} changed={changed}"
        )
    return {
        **result,
        "upstream_file_count": len(upstream_before),
        "workflow_sha256": hashlib.sha256(workflow_before).hexdigest(),
        "continuation_sha256": hashlib.sha256(
            continuation_before.encode("utf-8")
        ).hexdigest(),
    }
