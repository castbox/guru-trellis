"""Historical Check reader prerequisites; no current quality judgment or pass."""
from __future__ import annotations

import base64
import json
from pathlib import Path
import stat
import subprocess
from typing import Any

from adapters.eval.eval_support import package_tree_sha256


def stage(request: dict[str, Any], fixture: Path) -> tuple[Path, Path, dict[str, str]]:
    package = fixture / ".trellis/guru-team/skills/packages/guru-check-task"
    if package_tree_sha256(package) != package_tree_sha256(Path(request["package_root"])):
        raise ValueError("legacy reader installed package differs from source")
    task_ref = ".trellis/tasks/example-task"
    key = {"task_id": "example-task", "lifecycle_generation": 0}
    source = fixture / task_ref / "task.json"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(json.dumps({
        "id": "example-task", "name": "example-task", "status": "in_progress",
    }) + "\n", encoding="utf-8")
    control_ref = ".trellis/.runtime/guru-team/owner-checkpoints/example-task/phase2-check.json"
    control = fixture / control_ref
    control.parent.mkdir(parents=True, exist_ok=True)
    control.write_bytes((package / "evals/files/legacy-control-retirement-source-gate.json").read_bytes())
    control.chmod(0o640)

    def helper(public: dict[str, Any]) -> dict[str, Any]:
        result = subprocess.run(
            ["bash", str(package / "scripts/legacy-maintenance.sh"),
             "--root", str(fixture), "--input", "-"],
            input=json.dumps(public), text=True, capture_output=True, cwd=fixture,
            check=False,
        )
        if result.returncode:
            raise ValueError("legacy reader prerequisite failed: " + result.stdout + result.stderr)
        value = json.loads(result.stdout)
        return value.get("result", value)

    identity = {"root": str(fixture), "key": key, "task_ref": task_ref}
    inspected = helper({
        "profile": "legacy_control_inspection", **identity, "control_refs": [control_ref],
    })
    frozen = helper({
        "profile": "legacy_control_freeze", **identity,
        "controls": inspected["controls"],
        "source": {"content_base64": base64.b64encode(source.read_bytes()).decode(),
                   "mode": stat.S_IMODE(source.stat().st_mode)},
        "operation_id": "eval-legacy-reader",
    })
    # Physical preservation is a reader precondition, not an archive-producer result.
    preserved_ref = ".trellis/tasks/archive/2026-10/example-task/task.json"
    preserved = fixture / preserved_ref
    preserved.parent.mkdir(parents=True, exist_ok=True)
    source.replace(preserved)
    source.parent.rmdir()
    public = {
        "profile": "legacy_control_retirement", **identity,
        "control_refs": [control_ref], "preserved_source_ref": preserved_ref,
        "recovery_ref": frozen["recovery_ref"],
    }
    target = fixture / ".trellis/.runtime/guru-team/evals/public-input.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(public, indent=2) + "\n", encoding="utf-8")
    # Leave formal retirement to the shared adapter's traced public invocation.
    return package, fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh", {}
