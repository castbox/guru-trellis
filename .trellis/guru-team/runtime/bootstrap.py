#!/usr/bin/env python3
"""Build and activate the repository-local Guru Team Python runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REPAIR_COMMAND = "trellis/presets/guru-team/scripts/bash/apply.sh --repo ."


class BootstrapError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BootstrapError(f"invalid runtime file: {path.name}") from exc
    if not isinstance(payload, dict):
        raise BootstrapError(f"invalid runtime file: {path.name}")
    return payload


def canonical_json(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def runtime_identity(assets: Path, python: Path) -> tuple[str, dict[str, Any]]:
    manifest = read_json(assets / "python-runtime.json")
    lock_digest = hashlib.sha256((assets / str(manifest["lock_file"])).read_bytes()).hexdigest()
    proc = subprocess.run(
        [str(python), "-c", "import json,platform,sys;print(json.dumps({'implementation':platform.python_implementation(),'major':sys.version_info[0],'minor':sys.version_info[1]}))"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode != 0:
        raise BootstrapError("selected Python interpreter is not executable")
    python_info = json.loads(proc.stdout)
    current = f"{python_info['major']}.{python_info['minor']}"
    if (
        python_info["implementation"] != manifest["python"]["implementation"]
        or current not in manifest["python"]["supported_minor_versions"]
    ):
        raise BootstrapError("selected Python interpreter is incompatible")
    identity = {
        "runtime_api_version": manifest["runtime_api_version"],
        "venv_layout_version": manifest["venv_layout_version"],
        "lock_sha256": lock_digest,
        "python_implementation": python_info["implementation"],
        "python_major": python_info["major"],
        "python_minor": python_info["minor"],
    }
    runtime_id = hashlib.sha256(canonical_json(identity)).hexdigest()[:24]
    return runtime_id, identity


def venv_python(environment: Path) -> Path:
    return environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def run_probe(python: Path, assets: Path) -> dict[str, Any]:
    proc = subprocess.run(
        [str(python), str(assets / "probe.py"), "--manifest", str(assets / "python-runtime.json"), "--json"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode != 0:
        raise BootstrapError("managed dependency capability probe failed")
    payload = json.loads(proc.stdout)
    if payload.get("status") != "ok":
        raise BootstrapError("managed dependency capability probe failed")
    return payload


def existing_state(target: Path, runtime_id: str, identity: dict[str, Any], assets: Path) -> str:
    metadata_path = target / "metadata.json"
    if not metadata_path.is_file():
        return "unknown"
    try:
        metadata = read_json(metadata_path)
    except BootstrapError:
        return "unknown"
    python = venv_python(target / "venv")
    if metadata.get("runtime_id") != runtime_id or metadata.get("identity") != identity:
        return "unknown"
    if not python.is_file():
        return "repairable"
    try:
        run_probe(python, assets)
    except BootstrapError:
        return "repairable"
    return "reusable"


def write_active(runtime_root: Path, runtime_id: str) -> None:
    pointer = {"runtime_id": runtime_id, "interpreter": f"{runtime_id}/venv/{'Scripts/python.exe' if os.name == 'nt' else 'bin/python'}"}
    temporary = runtime_root / "active.json.tmp"
    temporary.write_bytes(canonical_json(pointer) + b"\n")
    temporary.replace(runtime_root / "active.json")


def validate_active(repo: Path, assets: Path, python: Path, runtime_id: str) -> dict[str, Any]:
    expected_id, identity = runtime_identity(assets, python)
    if expected_id != runtime_id:
        raise BootstrapError("active runtime identity is stale")
    target = repo / ".trellis/.runtime/guru-team/python" / runtime_id
    if existing_state(target, runtime_id, identity, assets) != "reusable":
        raise BootstrapError("active runtime metadata or capability probe is invalid")
    return {"status": "ok", "runtime_identity": runtime_id}


def bootstrap(repo: Path, assets: Path, python: Path, activate: bool = True) -> dict[str, Any]:
    runtime_root = repo / ".trellis/.runtime/guru-team/python"
    runtime_root.mkdir(parents=True, exist_ok=True)
    runtime_id, identity = runtime_identity(assets, python)
    target = runtime_root / runtime_id
    repair_target = False
    if target.exists():
        state = existing_state(target, runtime_id, identity, assets) if target.is_dir() else "unknown"
        if state == "unknown":
            raise BootstrapError("target runtime identity exists without valid managed provenance")
        if state == "reusable":
            if activate:
                write_active(runtime_root, runtime_id)
            return {"status": "ok", "action": "reused", "runtime_identity": runtime_id}
        repair_target = True

    candidate = runtime_root / f".{runtime_id}.candidate-{os.getpid()}"
    if candidate.exists():
        raise BootstrapError("runtime candidate path already exists")
    candidate.mkdir()
    (candidate / ".guru-team-candidate").write_text(runtime_id + "\n", encoding="utf-8")
    try:
        venv_dir = candidate / "venv"
        create = subprocess.run([str(python), "-m", "venv", str(venv_dir)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        managed_python = venv_python(venv_dir)
        if create.returncode != 0 or not managed_python.is_file():
            raise BootstrapError("Python venv or pip bootstrap failed")
        pip = subprocess.run([str(managed_python), "-m", "pip", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if pip.returncode != 0:
            raise BootstrapError("Python venv or pip bootstrap failed")
        manifest = read_json(assets / "python-runtime.json")
        environment = os.environ.copy()
        for key in ("PIP_INDEX_URL", "PIP_EXTRA_INDEX_URL", "VIRTUAL_ENV", "PYTHONPATH", "PYTHONHOME"):
            environment.pop(key, None)
        environment["PIP_CONFIG_FILE"] = os.devnull
        install = subprocess.run([
            str(managed_python), "-m", "pip", "install", "--require-hashes", "--no-input",
            "--disable-pip-version-check", "--only-binary=:all:",
            "--index-url", str(manifest["package_index"]),
            "-r", str(assets / str(manifest["lock_file"])),
        ], env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if install.returncode != 0:
            raise BootstrapError("hash-locked dependency installation failed")
        probe = run_probe(managed_python, assets)
        metadata = {"schema_version": "1.0", "runtime_id": runtime_id, "identity": identity, "dependencies": probe["dependencies"]}
        (candidate / "metadata.json").write_bytes(json.dumps(metadata, indent=2, sort_keys=True).encode("utf-8") + b"\n")
        (candidate / ".guru-team-candidate").unlink()
        if repair_target:
            backup = runtime_root / f".{runtime_id}.repair-backup-{os.getpid()}"
            target.replace(backup)
            try:
                candidate.replace(target)
            except Exception:
                backup.replace(target)
                raise
            shutil.rmtree(backup)
        else:
            candidate.replace(target)
        if activate:
            write_active(runtime_root, runtime_id)
        return {"status": "ok", "action": "repaired" if repair_target else "installed", "runtime_identity": runtime_id}
    except Exception:
        if candidate.is_dir():
            shutil.rmtree(candidate)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--runtime-assets", type=Path, required=True)
    parser.add_argument("--python", type=Path, default=Path(sys.executable))
    parser.add_argument("--print-identity", action="store_true")
    parser.add_argument("--validate-active")
    parser.add_argument("--no-activate", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    runtime_id: str | None = None
    try:
        if args.print_identity:
            print(runtime_identity(args.runtime_assets.resolve(), args.python.resolve())[0])
            return 0
        if args.validate_active:
            runtime_id = args.validate_active
            result = validate_active(
                args.repo.resolve(),
                args.runtime_assets.resolve(),
                args.python.resolve(),
                args.validate_active,
            )
        else:
            runtime_id, _ = runtime_identity(args.runtime_assets.resolve(), args.python.resolve())
            result = bootstrap(
                args.repo.resolve(),
                args.runtime_assets.resolve(),
                args.python.resolve(),
                activate=not args.no_activate,
            )
    except Exception:
        payload = {"code": "runtime_dependency_missing", "field_path": "runtime", "dependency": "jsonschema", "runtime_identity": runtime_id, "remediation": REPAIR_COMMAND}
        print(json.dumps(payload, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True) if args.json else result["runtime_identity"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
