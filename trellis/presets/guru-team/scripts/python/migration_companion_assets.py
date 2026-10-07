"""Execute reviewed companion preservation through existing preset provenance."""
from __future__ import annotations

import filecmp
from pathlib import Path
from typing import Callable


def install_companions(
    src: Path,
    dst: Path,
    repo: Path,
    managed_paths: tuple[Path, ...],
    previous_manifest: dict | None,
    preserved: set[str],
    copy_managed: Callable,
    copy_managed_spec: Callable,
) -> list[dict[str, str]]:
    companion_paths = {(dst / relative).relative_to(repo).as_posix() for relative in managed_paths}
    if not preserved <= companion_paths:
        raise SystemExit("Migration preservation is limited to exact companion assets")
    previous_owned = set(previous_manifest.get("install", {}).get("managed_assets", [])) if previous_manifest else set()
    results = []
    for relative in managed_paths:
        target = dst / relative
        rel_path = target.relative_to(repo).as_posix()
        if rel_path in preserved:
            if not target.is_file():
                raise SystemExit("A reviewed preserved companion preimage is missing")
            # Existing managed_assets provenance omits local ownership. A later
            # ordinary reapply can preserve/conflict, never silently overwrite.
            continue
        if (previous_manifest and rel_path not in previous_owned and target.exists()
                and not filecmp.cmp(src / relative, target, shallow=False)):
            result = copy_managed_spec(src / relative, target, repo, previous_manifest)
        else:
            result = copy_managed(src / relative, target)
        results.append(result)
    return results


def collect_companion_results(
    repo: Path, results: list[dict[str, str]], installed: list[str],
    unchanged: list[str], updated: list[str], backups: list[str],
    new_copies: list[str], sidecars: list[str], conflicts: list[dict],
) -> None:
    actions = {"installed": installed, "unchanged": unchanged, "updated_managed": updated}
    for result in results:
        rel_path = Path(result["path"]).relative_to(repo).as_posix()
        action = result["action"]
        if action in actions:
            actions[action].append(rel_path)
            if result.get("backup"):
                backups.append(Path(result["backup"]).relative_to(repo).as_posix())
        else:
            sidecar = Path(result["sidecar"]).relative_to(repo).as_posix()
            new_copies.append(sidecar)
            sidecars.append(sidecar)
            conflicts.append({"path": rel_path, "reason": "preserved_companion_customization", "sidecar": sidecar})


def ensure_companion_modes(dst: Path, repo: Path, paths: tuple[Path, ...], preserved: set[str], results: list[dict[str, str]], ensure_executable: Callable) -> None:
    skipped = preserved | {Path(row["path"]).relative_to(repo).as_posix() for row in results if row["action"] == "conflict"}
    for relative in paths:
        script = dst / relative
        if relative.parts[:2] == ("scripts", "bash") and script.exists() and script.relative_to(repo).as_posix() not in skipped:
            ensure_executable(script)
