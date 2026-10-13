"""Test-only binding to explicitly supplied, reviewed upstream Python assets."""
import os
import shutil
from pathlib import Path


def scripts_source() -> Path:
    selected = os.environ.get("GURU_UPSTREAM_DELIVERY_SCRIPTS")
    if selected:
        source = Path(selected)
    elif os.environ.get("TRELLIS_FIXED_FORK_SOURCE"):
        source = Path(os.environ["TRELLIS_FIXED_FORK_SOURCE"]) / "packages/cli/src/templates/trellis/scripts"
    else:
        raise RuntimeError("Provide the fixed reviewed upstream candidate assets for Delivery tests.")
    if not (source / "common/delivery_schema.py").is_file():
        raise RuntimeError("Selected upstream candidate does not provide Delivery API 1.0.")
    return source


def install_common(root: Path) -> None:
    destination = root / ".trellis/scripts/common"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(scripts_source() / "common", destination, dirs_exist_ok=True)


def public_task(metadata: dict) -> dict:
    defaults = {"id": "fixture", "name": "fixture", "lifecycle_generation": 0,
                "source": {"kind": "no_issue"}, "title": "Fixture", "description": "Reviewed fixture",
                "dev_type": None, "scope": None, "package": None, "priority": "P2", "createdAt": "2026-10-12",
                "base_branch": "main", "worktree_path": None, "children": [], "parent": None,
                "relatedFiles": [], "notes": "", "meta": {}}
    data = {key: value for key, value in {**defaults, **metadata}.items() if key not in {"status", "completedAt", "commit", "pr_url"}}
    data.update(schema_version="2.0", accepted_scope=None, deliveries=[], completion_results=[], closure_results=[])
    return data
