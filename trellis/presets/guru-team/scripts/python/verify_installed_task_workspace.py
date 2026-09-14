from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

from verify_throwaway_python_routing import runtime_checkpoint
from verify_installed_phase0_transcript import six_step_transcript


LEGACY_ROOTS = (
    Path(".trellis/.developer"),
    Path(".trellis/workspace"),
    Path(".trellis/agent-traces"),
)


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()


def legacy_snapshot(root: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for legacy_root in LEGACY_ROOTS:
        path = root / legacy_root
        try:
            root_metadata = path.lstat()
        except FileNotFoundError:
            continue
        candidates = [path]
        if stat.S_ISDIR(root_metadata.st_mode):
            for current, directories, files in os.walk(path, followlinks=False):
                current_path = Path(current)
                candidates.extend(
                    current_path / name for name in sorted(directories + files)
                )
        for candidate in candidates:
            relative = candidate.relative_to(root).as_posix()
            metadata = candidate.lstat()
            mode = stat.S_IMODE(metadata.st_mode)
            if stat.S_ISLNK(metadata.st_mode):
                rows[relative] = {
                    "kind": "symlink",
                    "mode": mode,
                    "target": os.readlink(candidate),
                }
            elif stat.S_ISDIR(metadata.st_mode):
                rows[relative] = {"kind": "directory", "mode": mode}
            elif stat.S_ISREG(metadata.st_mode):
                rows[relative] = {
                    "kind": "file",
                    "mode": mode,
                    "sha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
                }
            else:
                raise AssertionError(f"unsupported legacy fixture path: {relative}")
    return rows


def seed_legacy_fixture(root: Path, profile: str) -> dict[str, dict[str, Any]]:
    if profile == "absent":
        return {}
    payloads = {
        "present-a": {
            ".trellis/.developer": (b"name=legacy-a\n", 0o640),
            ".trellis/workspace/index.md": (b"# Legacy workspace A\n", 0o600),
            ".trellis/workspace/alice/index.md": (b"# Alice\n", 0o640),
            ".trellis/workspace/alice/journal.md": (b"legacy journal a\n", 0o600),
            ".trellis/agent-traces/a.jsonl": (b'{"trace":"a"}\n', 0o640),
        },
        "present-b": {
            ".trellis/.developer": (b"name=legacy-b\n", 0o600),
            ".trellis/workspace/index.md": (b"# Legacy workspace B\n", 0o640),
            ".trellis/workspace/bob/index.md": (b"# Bob\n", 0o600),
            ".trellis/workspace/bob/journal.md": (b"legacy journal b\nsecond line\n", 0o640),
            ".trellis/workspace/bob/archive/old.md": (b"old entry\n", 0o600),
            ".trellis/agent-traces/b.jsonl": (b'{"trace":"b","step":2}\n', 0o600),
        },
    }.get(profile)
    if payloads is None:
        raise AssertionError(f"unsupported legacy profile: {profile}")
    for relative, (content, mode) in payloads.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        path.chmod(mode)
    symlinks = {
        "present-a": {
            ".trellis/workspace/alice/latest.md": "journal.md",
        },
        "present-b": {
            ".trellis/workspace/bob/archive/missing.md": "not-created.md",
        },
    }[profile]
    for relative, target in symlinks.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(target)
    return legacy_snapshot(root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--installed-repo", required=True)
    parser.add_argument("--work-root", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument(
        "--legacy-profile",
        choices=("absent", "present-a", "present-b"),
        default="absent",
    )
    args = parser.parse_args()
    installed_repo = Path(args.installed_repo).resolve()
    work_root = Path(args.work_root).resolve()
    legacy_before: dict[str, dict[str, Any]] = {}

    def setup_owner(root: Path) -> None:
        legacy_before.update(seed_legacy_fixture(root, args.legacy_profile))

    _, _, result = six_step_transcript(
        installed_repo, work_root / "installed-task-workspace",
        repo="example/installed-fixture", issue=112,
        task_slug="112-installed-task-workspace",
        branch_name="feat/112-installed-task-workspace",
        task_title="#112 Verify installed task workspace",
        setup_owner=setup_owner,
    )
    source = Path(result["owner_repo"])
    workspace = Path(result["workspace_path"])
    task_dir = workspace / result["task_artifact_dir"]
    task_data = json.loads((task_dir / "task.json").read_text())
    if result["checker_status"] != "passed":
        raise AssertionError("installed checker did not validate the created workspace")
    if task_data.get("creator") != "stage0-transcript":
        raise AssertionError("installed runtime depended on developer identity for creator")
    legacy_after = legacy_snapshot(source)
    if legacy_after != legacy_before:
        raise AssertionError("installed runtime changed legacy path, bytes, or mode state")
    target_identity = workspace / ".trellis/.developer"
    if target_identity.exists():
        raise AssertionError("installed runtime copied private developer identity")
    for legacy_root in LEGACY_ROOTS:
        if (workspace / legacy_root).exists():
            raise AssertionError(f"installed runtime copied legacy state: {legacy_root}")

    lifecycle_outcome = {
        "typed_exit": result["actual_exit"],
        "checker_status": result["checker_status"],
        "artifact_names": sorted(path.name for path in task_dir.iterdir() if path.is_file()),
        "task_creator": task_data.get("creator"),
        "target_legacy_state_absent": True,
    }

    print(
        json.dumps(
            {
                "status": "ok",
                "typed_exit": result["actual_exit"],
                "checker_status": result["checker_status"],
                "task_artifact_dir": result["task_artifact_dir"],
                "artifact_names": lifecycle_outcome["artifact_names"],
                "legacy_profile": args.legacy_profile,
                "activation": result["activation"],
                "source_developer_identity": (source / ".trellis/.developer").exists(),
                "target_developer_identity": target_identity.exists(),
                "legacy_preserved": legacy_after == legacy_before,
                "legacy_path_count": len(legacy_after),
                "legacy_snapshot_sha256": digest(legacy_after),
                "lifecycle_outcome_sha256": digest(lifecycle_outcome),
                "task_creator": task_data.get("creator"),
                "source_workspace_journal": (source / ".trellis/workspace").exists(),
                "target_workspace_journal": False,
                "runtime_checkpoint": runtime_checkpoint(
                    installed_repo,
                    installed_repo / ".trellis/guru-team/runtime",
                    f"task-workspace-{args.checkpoint}",
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
