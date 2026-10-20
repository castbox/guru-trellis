"""Exercise the public schema wrapper without changing a checkout's active runtime."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

try:
    from .temporary_lifecycle import temporary_directory
    from .bootstrap_transport import native_bash, wrapper_call
except ImportError:  # bootstrap.py is also a direct stdlib-only entry.
    from temporary_lifecycle import temporary_directory
    from bootstrap_transport import native_bash, wrapper_call


def check_public_wrapper(assets: Path, runtime_id: str, target: Path) -> None:
    skills = assets.parent if (assets.parent / "packages").is_dir() else assets.parent / "skills"
    check = json.loads((assets / "python-runtime.json").read_text(encoding="utf-8"))["public_wrapper_check"]
    package_id = check["package"]
    package = skills / "packages" / package_id
    if not (package / "scripts/invoke.sh").is_file() or not (skills / "schemas").is_dir():
        raise ValueError("matching public wrapper assets are missing")
    with temporary_directory("python_runtime_check") as view:
        runtime = view / ".trellis/guru-team/runtime"
        installed_skills = runtime.parent / "skills"
        ignore = shutil.ignore_patterns("tests", "__pycache__", "*.pyc", "*.pyo")
        shutil.copytree(assets, runtime, ignore=ignore)
        shutil.copytree(package, installed_skills / "packages" / package_id, ignore=ignore)
        shutil.copytree(skills / "schemas", installed_skills / "schemas", ignore=ignore)
        # A disposable copy checks the same interpreter/dependency bytes without
        # moving the prior cache entry or requiring directory-symlink privileges.
        cache = view / "cache"
        cache.mkdir()
        shutil.copytree(target, cache / runtime_id)
        pointer = view / ".trellis/.runtime/guru-team/python/active.json"
        pointer.parent.mkdir(parents=True)
        interpreter = cache / runtime_id / "venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        pointer.write_text(json.dumps({"schema_version": "2.0", "cache_scope": "user",
                                       "runtime_id": runtime_id, "interpreter": interpreter.as_posix()},
                                      sort_keys=True, ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="\n")
        environment = os.environ.copy()
        environment.pop("PYTHONHOME", None)
        environment.pop("VIRTUAL_ENV", None)
        environment["GURU_TEAM_PYTHON_CACHE_ROOT"] = cache.as_posix()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        wrapper = installed_skills / "packages" / package_id / "scripts/invoke.sh"
        bash = native_bash()
        for case in check["cases"]:
            command, payload_input = wrapper_call(bash, wrapper, case["arguments"])
            result = subprocess.run(
                command, input=payload_input,
                cwd=view, env=environment, text=True, encoding="utf-8", stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=False,
            )
            payload = json.loads(result.stdout)
            if result.returncode != case["expected_returncode"] or any(
                payload.get(key) != value for key, value in case["expected_output"].items()
            ):
                raise ValueError("public schema wrapper runtime check failed")
