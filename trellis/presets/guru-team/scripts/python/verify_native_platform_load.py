#!/usr/bin/env python3
"""Verify native platform discovery for installed Guru Team projections."""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any


class NativeLoadError(RuntimeError):
    """A native platform failed to discover its installed Guru projection."""


def _load_json(path: Path, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise NativeLoadError(f"cannot read {label}: {exc}") from exc


def _read_catalog(url: str, label: str) -> Any:
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return json.loads(response.read().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise NativeLoadError(f"cannot read OpenCode native {label} catalog: {exc}") from exc


def _load_opencode_catalogs(
    executable: str,
    target: Path,
    environment: dict[str, str],
    work_root: Path,
    log_name: str,
) -> tuple[Any, Any, str]:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    process = subprocess.Popen(
        (executable, "serve", "--hostname", "127.0.0.1", "--port", str(port)),
        cwd=target,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    try:
        base = f"http://127.0.0.1:{port}"
        for _ in range(100):
            if process.poll() is not None:
                raise NativeLoadError("OpenCode native catalog server exited before readiness")
            try:
                skills = _read_catalog(base + "/skill", "skill")
                commands = _read_catalog(base + "/command", "command")
                break
            except NativeLoadError:
                time.sleep(0.1)
        else:
            raise NativeLoadError("OpenCode native catalog server did not become ready")
    finally:
        process.terminate()
        try:
            output, _ = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            output, _ = process.communicate(timeout=10)
        (work_root / log_name).write_text(output or "", encoding="utf-8")
    version = subprocess.run(
        (executable, "--version"),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if version.returncode != 0 or not version.stdout.strip():
        raise NativeLoadError("OpenCode version probe failed")
    return skills, commands, version.stdout.strip()


def _isolated_opencode_catalogs(
    executable: str,
    target: Path,
    work_root: Path,
    *,
    disable_external_skills: bool,
) -> tuple[Any, Any, str]:
    prefix = "opencode-native-home-" if disable_external_skills else "opencode-home-"
    with tempfile.TemporaryDirectory(prefix=prefix, dir=work_root) as directory:
        isolated_home = Path(directory)
        environment = os.environ.copy()
        environment["HOME"] = str(isolated_home)
        if disable_external_skills:
            environment["OPENCODE_DISABLE_EXTERNAL_SKILLS"] = "1"
        else:
            environment.pop("OPENCODE_DISABLE_EXTERNAL_SKILLS", None)
        for variable, relative in (
            ("XDG_DATA_HOME", "data"),
            ("XDG_CONFIG_HOME", "config"),
            ("XDG_CACHE_HOME", "cache"),
            ("XDG_STATE_HOME", "state"),
        ):
            path = isolated_home / relative
            path.mkdir(parents=True, exist_ok=True)
            environment[variable] = str(path)
        return _load_opencode_catalogs(
            executable,
            target,
            environment,
            work_root,
            "opencode-native-server.log"
            if disable_external_skills
            else "opencode-server.log",
        )


def _guru_skills(catalog: Any, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(catalog, list):
        raise NativeLoadError(f"OpenCode {label} skill discovery did not return an array")
    return {
        row["name"]: row
        for row in catalog
        if isinstance(row, dict)
        and isinstance(row.get("name"), str)
        and row["name"].startswith("guru-")
    }


def _verify_command(catalog: Any, target: Path, label: str) -> None:
    if not isinstance(catalog, list):
        raise NativeLoadError(f"OpenCode {label} command discovery did not return an array")
    command = next(
        (
            row
            for row in catalog
            if isinstance(row, dict) and row.get("name") == "guru-finish-work"
        ),
        None,
    )
    if not isinstance(command, dict) or not isinstance(command.get("template"), str):
        raise NativeLoadError(f"OpenCode {label} discovery did not find guru-finish-work")
    expected_template = (
        target / ".opencode/commands/guru-finish-work.md"
    ).read_text(encoding="utf-8").removesuffix("\n")
    if command["template"] != expected_template:
        raise NativeLoadError(
            f"OpenCode {label} guru-finish-work template disagrees with installed bytes"
        )


def verify_native_platform_load(
    target: Path,
    platform: str,
    work_root: Path,
) -> dict[str, Any]:
    """Use the platform's native loader and verify its Guru command/skill catalog."""
    if platform != "opencode":
        return {"status": "not_applicable", "platform": platform}

    executable = shutil.which("opencode")
    if executable is None:
        raise NativeLoadError("OpenCode actual-load verification requires opencode on PATH")

    registry = _load_json(
        target / ".trellis/guru-team/skills/registry.json",
        "installed skill registry",
    )
    active_ids = sorted(
        row["id"]
        for row in registry.get("skills", [])
        if isinstance(row, dict) and row.get("state") == "active"
    )
    work_root.mkdir(parents=True, exist_ok=True)
    skills, commands, version = _isolated_opencode_catalogs(
        executable, target, work_root, disable_external_skills=False
    )
    native_skills, native_commands, native_version = _isolated_opencode_catalogs(
        executable, target, work_root, disable_external_skills=True
    )
    if native_version != version:
        raise NativeLoadError("OpenCode version changed between native load probes")

    guru_skills = _guru_skills(skills, "default")
    guru_native_skills = _guru_skills(native_skills, "native-only")
    for label, discovered in (
        ("default", guru_skills),
        ("native-only", guru_native_skills),
    ):
        if sorted(discovered) != active_ids:
            raise NativeLoadError(
                f"OpenCode {label} skill discovery disagrees with the active registry"
            )

    native_skill_root = (target / ".opencode/skills").resolve()
    shared_skill_root = (target / ".agents/skills").resolve()
    claude_skill_root = (target / ".claude/skills").resolve()
    selected_roots: Counter[str] = Counter()
    for skill_id, row in guru_skills.items():
        native = (native_skill_root / skill_id / "SKILL.md").resolve()
        shared = (shared_skill_root / skill_id / "SKILL.md").resolve()
        claude = (claude_skill_root / skill_id / "SKILL.md").resolve()
        location = row.get("location")
        selected = Path(location).resolve() if isinstance(location, str) else None
        allowed = {native: "native", shared: "shared", claude: "claude"}
        if selected not in allowed:
            raise NativeLoadError(
                f"OpenCode default discovery loaded {skill_id} from unexpected location {location!r}"
            )
        if not native.is_file() or not selected.is_file():
            raise NativeLoadError(f"OpenCode default discovery selected missing {skill_id} bytes")
        if selected.read_bytes() != native.read_bytes():
            raise NativeLoadError(
                f"OpenCode default discovery loaded {skill_id} bytes that disagree with native projection"
            )
        selected_roots[allowed[selected]] += 1

    for skill_id, row in guru_native_skills.items():
        expected = (native_skill_root / skill_id / "SKILL.md").resolve()
        location = row.get("location")
        if not isinstance(location, str) or Path(location).resolve() != expected:
            raise NativeLoadError(
                f"OpenCode native-only discovery loaded {skill_id} from an unexpected location"
            )

    _verify_command(commands, target, "default")
    _verify_command(native_commands, target, "native-only")

    return {
        "status": "passed",
        "platform": "opencode",
        "opencode_version": version,
        "skill_count": len(guru_skills),
        "skills": sorted(guru_skills),
        "default_selected_roots": dict(sorted(selected_roots.items())),
        "native_only_skill_count": len(guru_native_skills),
        "command": "guru-finish-work",
        "isolated_home": True,
        "external_skills_disabled_for_native_probe": True,
    }
