#!/usr/bin/env python3
"""Verify guru-trellis dogfood against its exact installed platform selection."""

from __future__ import annotations

import argparse
import filecmp
import json
import sys
from pathlib import Path

from apply_guru_team_trellis_preset import skill_platform_public_files, skill_registry_entries
from guru_platform_inventory import PLATFORM_BY_FLAG
from platform_projection_contract import (
    DESCRIPTORS_BY_FLAG,
    DOGFOOD_PLATFORM_FLAGS,
    PlatformContractError,
    installed_selection,
)


class DogfoodDriftError(RuntimeError):
    pass


def _tree_files(root: Path) -> dict[str, Path]:
    if not root.is_dir() or root.is_symlink():
        return {}
    return {
        path.relative_to(root).as_posix(): path
        for skill_root in root.glob("guru-*")
        if skill_root.is_dir() and not skill_root.is_symlink()
        for path in skill_root.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    }


def _assert_projection(left_files: dict[str, Path], right: Path, label: str) -> None:
    right_files = _tree_files(right)
    if set(left_files) != set(right_files):
        raise DogfoodDriftError(
            f"{label} file set drift: left_only={sorted(set(left_files)-set(right_files))} "
            f"right_only={sorted(set(right_files)-set(left_files))}"
        )
    changed = [
        relative for relative in sorted(left_files)
        if not filecmp.cmp(left_files[relative], right_files[relative], shallow=False)
    ]
    if changed:
        raise DogfoodDriftError(f"{label} byte drift: {changed}")


def verify(repo: Path) -> dict[str, object]:
    manifest_path = repo / ".trellis/guru-team/extension.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DogfoodDriftError(f"cannot read installed manifest: {exc}") from exc
    if not isinstance(manifest, dict):
        raise DogfoodDriftError("installed manifest root must be an object")
    try:
        selected = installed_selection(manifest)
    except PlatformContractError as exc:
        raise DogfoodDriftError(str(exc)) from exc
    if selected != DOGFOOD_PLATFORM_FLAGS:
        raise DogfoodDriftError(
            f"dogfood selection must be {list(DOGFOOD_PLATFORM_FLAGS)}, got {list(selected)}"
        )

    checked_roots: list[str] = []
    selected_roots = {Path(".agents/skills")}
    for flag in selected:
        for relative_root in PLATFORM_BY_FLAG[flag].skill_roots:
            selected_roots.add(relative_root)
            if relative_root == Path(".agents/skills"):
                continue
            checked_roots.append(relative_root.as_posix())
        descriptor = DESCRIPTORS_BY_FLAG[flag]
        entry = repo / descriptor["entry_path"]
        source = repo / "trellis/presets/guru-team/overlays" / descriptor["entry_path"]
        if not entry.is_file() or entry.is_symlink():
            raise DogfoodDriftError(f"missing selected dogfood entry {descriptor['entry_path']}")
        if source.is_file() and not filecmp.cmp(source, entry, shallow=False):
            raise DogfoodDriftError(f"selected dogfood entry drift {descriptor['entry_path']}")

    canonical_root = repo / "trellis/skills/guru-team"
    try:
        _, entries = skill_registry_entries(canonical_root)
        active = [entry for entry in entries if entry.get("state") == "active"]
        for relative_root in sorted(selected_roots):
            root_platforms = {
                flag for flag in selected
                if relative_root in PLATFORM_BY_FLAG[flag].skill_roots
            }
            if relative_root == Path(".agents/skills"):
                root_platforms.add("shared")
            expected: dict[str, Path] = {}
            for entry in active:
                interface = json.loads((canonical_root / entry["interface"]).read_text(encoding="utf-8"))
                if entry.get("supported_platforms") != interface.get("platform_destinations"):
                    raise DogfoodDriftError(f"canonical registry/interface platform drift for {entry['id']}")
                supported = set(entry["supported_platforms"])
                if "shared" not in supported and not root_platforms.intersection(supported):
                    continue
                package = canonical_root / entry["package"]
                for source in skill_platform_public_files(package):
                    expected[f"{entry['id']}/{source.relative_to(package).as_posix()}"] = source
            _assert_projection(expected, repo / relative_root, f"{relative_root.as_posix()} skill projection")
    except (OSError, ValueError, SystemExit) as exc:
        raise DogfoodDriftError(f"cannot resolve canonical package projections: {exc}") from exc

    for flag, core in PLATFORM_BY_FLAG.items():
        if flag in selected:
            continue
        for relative_root in core.skill_roots:
            if relative_root in selected_roots:
                continue
            if any((repo / relative_root).glob("guru-*")):
                raise DogfoodDriftError(f"unselected dogfood skill projection exists for {flag}")
        entry = repo / DESCRIPTORS_BY_FLAG[flag]["entry_path"]
        if entry.exists():
            raise DogfoodDriftError(f"unselected dogfood entry exists for {flag}: {entry.relative_to(repo)}")

    leaked = sorted(
        path.relative_to(repo).as_posix()
        for root in selected_roots
        for path in (repo / root).glob("guru-*/tests")
        if path.exists()
    )
    if leaked:
        raise DogfoodDriftError(f"dogfood public projections leaked package-private tests: {leaked}")
    return {
        "status": "ok",
        "selected_platforms": list(selected),
        "shared_root": ".agents/skills",
        "checked_native_roots": sorted(checked_roots),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        payload = verify(args.repo.resolve())
    except DogfoodDriftError as exc:
        payload = {"status": "error", "detail": str(exc)}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        else:
            print(str(exc), file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
