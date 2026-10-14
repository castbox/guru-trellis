#!/usr/bin/env python3
"""Build and resolve the user-scoped Guru Team Python runtime cache."""

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

try:
    from .bootstrap_check import check_public_wrapper
except ImportError:
    from bootstrap_check import check_public_wrapper

REPAIR_COMMAND = "trellis/presets/guru-team/scripts/bash/apply.sh --repo ."


class BootstrapError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        code: str = "runtime_dependency_missing",
        dependency: str = "python-runtime",
        runtime_identity: str | None = None,
        remediation: str = REPAIR_COMMAND,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.dependency = dependency
        self.runtime_identity = runtime_identity
        self.remediation = remediation


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


def select_python(value: str | Path = "python3") -> Path:
    raw = str(value)
    selected = shutil.which(raw)
    if selected is None:
        raise BootstrapError(
            "selected interpreter is unavailable or not executable",
            code="interpreter_unavailable",
            remediation="Make python3 executable on PATH or rerun apply.sh --repo . --python /path/to/python3.",
        )
    # Preserve the venv launch path; resolving its final symlink loses isolation.
    return Path(os.path.abspath(selected))


def runtime_identity(assets: Path, python: Path) -> tuple[str, dict[str, Any]]:
    python = select_python(python)
    manifest = read_json(assets / "python-runtime.json")
    lock_digest = hashlib.sha256((assets / str(manifest["lock_file"])).read_bytes()).hexdigest()
    proc = subprocess.run(
        [
            str(python),
            "-c",
            (
                "import json,platform,sys,sysconfig;"
                "print(json.dumps({'implementation':platform.python_implementation(),"
                "'major':sys.version_info[0],'minor':sys.version_info[1],"
                "'os_name':platform.system() or sys.platform,'machine':platform.machine(),"
                "'abi_tag':getattr(getattr(sys,'implementation',None),'cache_tag','') or '',"
                "'platform_tag':sysconfig.get_platform()}))"
            ),
        ],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode != 0:
        raise BootstrapError("selected interpreter cannot report Python identity", code="interpreter_unavailable", remediation="Run python3 --version; rerun apply.sh --repo . --python /path/to/python3.")
    try:
        python_info = json.loads(proc.stdout)
    except (ValueError, TypeError) as exc:
        raise BootstrapError("selected interpreter cannot report Python identity", code="interpreter_unavailable") from exc
    if python_info.get("major") != manifest["python"]["major"]:
        raise BootstrapError("selected interpreter must be Python 3", code="python3_required",
                             remediation="Select Python 3: apply.sh --repo . --python /path/to/python3.")
    if python_info.get("implementation") != manifest["python"]["implementation"]:
        raise BootstrapError("selected Python implementation is unsupported", code="python_implementation_unsupported",
                             remediation="Select CPython 3: apply.sh --repo . --python /path/to/python3.")
    identity = {
        "runtime_api_version": manifest["runtime_api_version"],
        "venv_layout_version": manifest["venv_layout_version"],
        "lock_sha256": lock_digest,
        "python_implementation": python_info["implementation"],
        "python_major": python_info["major"],
        "python_minor": python_info["minor"],
        "os_name": python_info["os_name"],
        "machine": python_info["machine"],
        "python_abi_tag": python_info["abi_tag"],
        "python_platform_tag": python_info["platform_tag"],
    }
    runtime_id = hashlib.sha256(canonical_json(identity)).hexdigest()[:24]
    return runtime_id, identity


def venv_python(environment: Path) -> Path:
    return environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def user_cache_root(
    environment: dict[str, str] | None = None,
    *,
    system_name: str | None = None,
    home: Path | None = None,
) -> Path:
    values = os.environ if environment is None else environment
    override = values.get("GURU_TEAM_PYTHON_CACHE_ROOT", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    system = system_name or platform.system()
    user_home = home or Path.home()
    if system == "Darwin":
        return user_home / "Library/Caches/guru-team/python"
    if system == "Windows":
        local = values.get("LOCALAPPDATA", "").strip()
        return (Path(local) if local else user_home / "AppData/Local") / "GuruTeam/python"
    xdg = values.get("XDG_CACHE_HOME", "").strip()
    return (Path(xdg).expanduser() if xdg else user_home / ".cache") / "guru-team/python"


def repository_git_dirs(repo: Path) -> tuple[Path | None, Path | None]:
    git_marker = repo / ".git"
    git_dir: Path | None = None
    common_dir: Path | None = None
    if git_marker.is_dir():
        git_dir = git_marker.resolve()
        common_dir = git_dir
    elif git_marker.is_file() and not git_marker.is_symlink():
        try:
            marker = git_marker.read_text(encoding="utf-8").strip()
        except OSError:
            marker = ""
        if marker.startswith("gitdir: "):
            git_dir = Path(marker.removeprefix("gitdir: ").strip())
            if not git_dir.is_absolute():
                git_dir = repo / git_dir
            git_dir = git_dir.resolve()
            if git_dir.is_dir():
                common_dir = git_dir
                commondir = git_dir / "commondir"
                if commondir.is_file() and not commondir.is_symlink():
                    try:
                        common_value = commondir.read_text(encoding="utf-8").strip()
                    except OSError:
                        common_value = ""
                    if common_value:
                        common_candidate = Path(common_value)
                        if not common_candidate.is_absolute():
                            common_candidate = git_dir / common_candidate
                        common_candidate = common_candidate.resolve()
                        if common_candidate.is_dir():
                            common_dir = common_candidate
    return git_dir, common_dir


def repository_state_root(repo: Path, *, for_write: bool = False) -> Path:
    git_dir, common_dir = repository_git_dirs(repo)
    if git_dir is not None and common_dir is not None:
        common_root = common_dir / "guru-team/python"
        if git_dir != common_dir:
            worktree_root = git_dir / "guru-team/python"
            if for_write or (worktree_root / "active.json").is_file():
                return worktree_root
        return common_root
    # Git-less archive fixtures retain a private checkout-local pointer.
    return repo / ".trellis/.runtime/guru-team/python"


def runtime_target(runtime_id: str) -> Path:
    return user_cache_root() / runtime_id


def active_pointer_path(repo: Path, *, for_write: bool = False) -> Path:
    return repository_state_root(repo, for_write=for_write) / "active.json"


def run_probe(python: Path, assets: Path) -> dict[str, Any]:
    proc = subprocess.run(
        [str(python), str(assets / "probe.py"), "--manifest", str(assets / "python-runtime.json"), "--json"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode != 0:
        raise BootstrapError(
            "managed dependency capability probe failed",
            dependency="jsonschema",
        )
    payload = json.loads(proc.stdout)
    if payload.get("status") != "ok":
        raise BootstrapError(
            "managed dependency capability probe failed",
            dependency="jsonschema",
        )
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


def write_active(repo: Path, runtime_id: str) -> None:
    runtime_root = repository_state_root(repo, for_write=True)
    runtime_root.mkdir(parents=True, exist_ok=True)
    pointer = {
        "schema_version": "2.0",
        "cache_scope": "user",
        "runtime_id": runtime_id,
        "interpreter": venv_python(runtime_target(runtime_id) / "venv").as_posix(),
    }
    temporary = runtime_root / "active.json.tmp"
    temporary.write_bytes(canonical_json(pointer) + b"\n")
    temporary.replace(runtime_root / "active.json")


def resolve_runtime(assets: Path, runtime_id: str) -> dict[str, Any]:
    target = runtime_target(runtime_id)
    python = venv_python(target / "venv")
    if not target.is_dir() or not python.is_file() or not os.access(python, os.X_OK):
        raise BootstrapError(
            "managed runtime cache entry is missing",
            code="managed_runtime_missing",
            runtime_identity=runtime_id,
        )
    expected_id, identity = runtime_identity(assets, python)
    if expected_id != runtime_id:
        raise BootstrapError(
            "managed runtime identity is stale",
            code="managed_runtime_missing",
            runtime_identity=runtime_id,
        )
    if existing_state(target, runtime_id, identity, assets) != "reusable":
        raise BootstrapError(
            "managed runtime metadata or capability probe is invalid",
            dependency="jsonschema",
            runtime_identity=runtime_id,
        )
    return {"status": "ok", "runtime_identity": runtime_id, "interpreter": str(python)}


def validate_active(repo: Path, assets: Path, runtime_id: str | None = None) -> dict[str, Any]:
    pointer_path = active_pointer_path(repo)
    if not pointer_path.is_file() or pointer_path.is_symlink():
        raise BootstrapError(
            "managed runtime is not bootstrapped for this repository",
            code="runtime_not_bootstrapped",
        )
    try:
        pointer = read_json(pointer_path)
    except BootstrapError as exc:
        raise BootstrapError(
            "managed runtime pointer is invalid",
            code="managed_runtime_missing",
            runtime_identity=runtime_id,
        ) from exc
    active_id = pointer.get("runtime_id")
    expected_interpreter = venv_python(runtime_target(str(active_id)) / "venv").as_posix()
    if (
        pointer.get("schema_version") != "2.0"
        or pointer.get("cache_scope") != "user"
        or not isinstance(active_id, str)
        or len(active_id) != 24
        or pointer.get("interpreter") != expected_interpreter
        or (runtime_id is not None and active_id != runtime_id)
    ):
        raise BootstrapError(
            "managed runtime pointer is stale",
            code="managed_runtime_missing",
            runtime_identity=runtime_id if runtime_id is not None else (active_id if isinstance(active_id, str) else None),
        )
    return resolve_runtime(assets, active_id)


def bootstrap(repo: Path, assets: Path, python: Path, activate: bool = True) -> dict[str, Any]:
    runtime_root = user_cache_root()
    runtime_root.mkdir(parents=True, exist_ok=True)
    runtime_id, identity = runtime_identity(assets, python)
    target = runtime_root / runtime_id
    repair_target = False
    if target.exists():
        state = existing_state(target, runtime_id, identity, assets) if target.is_dir() else "unknown"
        if state == "unknown":
            raise BootstrapError("target runtime identity exists without valid managed provenance")
        if state == "reusable":
            run_public_wrapper(assets, runtime_id, target)
            if activate:
                write_active(repo, runtime_id)
            return {
                "status": "ok",
                "action": "reused",
                "runtime_identity": runtime_id,
                "interpreter": str(venv_python(target / "venv")),
            }
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
            raise BootstrapError("Python venv or pip bootstrap failed", code="venv_bootstrap_failed", remediation="Check selected Python 3 venv/ensurepip support; rerun apply.sh --repo . --python /path/to/python3.")
        pip = subprocess.run([str(managed_python), "-m", "pip", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if pip.returncode != 0:
            raise BootstrapError("Python venv or pip bootstrap failed", code="venv_bootstrap_failed", remediation="Check selected Python 3 venv/ensurepip support; rerun apply.sh --repo . --python /path/to/python3.")
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
            raise BootstrapError("hash-locked dependency installation failed", code="dependency_install_failed", remediation="Check PyPI access and locked wheel availability for the selected interpreter; retry apply.sh --repo . or select --python /path/to/python3. Do not edit the lock or manifest.")
        probe = run_probe(managed_python, assets)
        metadata = {"schema_version": "1.0", "runtime_id": runtime_id, "identity": identity, "dependencies": probe["dependencies"]}
        (candidate / "metadata.json").write_bytes(json.dumps(metadata, indent=2, sort_keys=True).encode("utf-8") + b"\n")
        run_public_wrapper(assets, runtime_id, candidate)
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
            write_active(repo, runtime_id)
        return {
            "status": "ok",
            "action": "repaired" if repair_target else "installed",
            "runtime_identity": runtime_id,
            "interpreter": str(venv_python(target / "venv")),
        }
    except Exception:
        if candidate.is_dir():
            shutil.rmtree(candidate)
        raise


def run_public_wrapper(assets: Path, runtime_id: str, target: Path) -> None:
    try:
        check_public_wrapper(assets, runtime_id, target)
    except Exception as exc:
        raise BootstrapError(
            "managed public wrapper Draft 2020-12 schema check failed",
            code="managed_runtime_check_failed", runtime_identity=runtime_id,
            dependency="jsonschema",
            remediation="Restore the complete matching Guru Team source/preset and retry apply.sh --repo .; check the selected interpreter with --python /path/to/python3. The previous environment and active pointer are preserved.",
        ) from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--runtime-assets", type=Path, required=True)
    parser.add_argument("--python", default="python3", help="Interpreter command or path; defaults to current PATH python3.")
    parser.add_argument("--print-identity", action="store_true")
    parser.add_argument("--validate-active")
    parser.add_argument("--resolve-active", action="store_true")
    parser.add_argument("--resolve-runtime")
    parser.add_argument("--exec-active", action="store_true")
    parser.add_argument("--print-active-pointer", action="store_true")
    parser.add_argument("--no-activate", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    runtime_id: str | None = None
    try:
        modes = sum(bool(value) for value in (
            args.print_identity,
            args.validate_active,
            args.resolve_active,
            args.resolve_runtime,
            args.exec_active,
            args.print_active_pointer,
        ))
        if modes > 1:
            raise BootstrapError("select exactly one runtime operation")
        if args.print_identity:
            print(runtime_identity(args.runtime_assets.resolve(), select_python(args.python))[0])
            return 0
        if args.print_active_pointer:
            print(active_pointer_path(args.repo.resolve()))
            return 0
        if args.validate_active:
            runtime_id = args.validate_active
            result = validate_active(
                args.repo.resolve(),
                args.runtime_assets.resolve(),
                args.validate_active,
            )
        elif args.resolve_runtime:
            runtime_id = args.resolve_runtime
            result = resolve_runtime(args.runtime_assets.resolve(), runtime_id)
        elif args.resolve_active or args.exec_active:
            result = validate_active(args.repo.resolve(), args.runtime_assets.resolve())
            runtime_id = str(result["runtime_identity"])
            if args.exec_active:
                command = list(args.command)
                if command[:1] == ["--"]:
                    command = command[1:]
                if not command:
                    raise BootstrapError("managed runtime command is missing")
                os.execv(result["interpreter"], [result["interpreter"], *command])
        else:
            runtime_id, _ = runtime_identity(args.runtime_assets.resolve(), select_python(args.python))
            result = bootstrap(
                args.repo.resolve(),
                args.runtime_assets.resolve(),
                select_python(args.python),
                activate=not args.no_activate,
            )
    except Exception as exc:
        payload = {
            "code": exc.code if isinstance(exc, BootstrapError) else "runtime_dependency_missing",
            "field_path": "runtime",
            "dependency": exc.dependency if isinstance(exc, BootstrapError) else "python-runtime",
            "runtime_identity": exc.runtime_identity if isinstance(exc, BootstrapError) and exc.runtime_identity is not None else runtime_id,
            "remediation": exc.remediation if isinstance(exc, BootstrapError) else REPAIR_COMMAND,
        }
        print(
            json.dumps(payload, sort_keys=True),
            file=sys.stderr if args.resolve_active or args.exec_active or args.resolve_runtime or args.validate_active else sys.stdout,
        )
        return 2
    print(json.dumps(result, sort_keys=True) if args.json else result["runtime_identity"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
