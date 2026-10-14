"""Preset managed-Python bootstrap transport; no installation policy decisions."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def ensure_managed_python_runtime(
    repo: Path,
    guru_root: Path,
    *,
    activate: bool = False,
    python: str = "python3",
) -> dict[str, Any]:
    runtime_assets = guru_root / "trellis/skills/guru-team/runtime"
    bootstrap = runtime_assets / "bootstrap.py"
    if not bootstrap.is_file() or bootstrap.is_symlink():
        raise_managed_runtime_error()
    selected = shutil.which(python) or python
    if os.path.dirname(selected):
        selected = os.path.abspath(selected)
    command = [
            sys.executable,
            str(bootstrap),
            "--repo",
            str(repo),
            "--runtime-assets",
            str(runtime_assets),
            "--python",
            selected,
            "--json",
        ]
    if not activate:
        command.append("--no-activate")
    proc = subprocess.run(
        command,
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    raw = proc.stdout.strip() or proc.stderr.strip()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        payload = {
            "code": "runtime_dependency_missing",
            "field_path": "runtime",
            "dependency": "python-runtime",
            "runtime_identity": None,
            "remediation": "trellis/presets/guru-team/scripts/bash/apply.sh --repo .",
        }
        raise SystemExit(json.dumps(payload, sort_keys=True)) from None
    if proc.returncode != 0 or payload.get("status") != "ok":
        error = {
            "code": str(payload.get("code") or "runtime_dependency_missing"),
            "field_path": str(payload.get("field_path") or "runtime"),
            "dependency": str(payload.get("dependency") or "python-runtime"),
            "runtime_identity": payload.get("runtime_identity"),
            "remediation": str(payload.get("remediation") or "trellis/presets/guru-team/scripts/bash/apply.sh --repo ."),
        }
        raise SystemExit(json.dumps(error, sort_keys=True))
    return payload


def raise_managed_runtime_error(runtime_identity: str | None = None) -> None:
    payload = {
        "code": "runtime_dependency_missing",
        "field_path": "runtime",
        "dependency": "python-runtime",
        "runtime_identity": runtime_identity,
        "remediation": "trellis/presets/guru-team/scripts/bash/apply.sh --repo .",
    }
    raise SystemExit(json.dumps(payload, sort_keys=True))
