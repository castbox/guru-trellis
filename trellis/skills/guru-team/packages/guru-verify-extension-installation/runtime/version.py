from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from runtime.io import CommandError


EXTENSION_MANIFEST = Path(".trellis/guru-team/extension.json")


def _repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".trellis").is_dir():
            return candidate
    process = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=current,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != 0:
        raise CommandError(
            "invalid_arguments",
            "arguments.--root",
            "Pass a path inside a Trellis repository.",
        )
    return Path(process.stdout.strip()).resolve()


def extension_payload(root: Path) -> dict[str, Any]:
    path = root / EXTENSION_MANIFEST
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"status": "missing", "path": EXTENSION_MANIFEST.as_posix()}
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {
            "status": "invalid",
            "path": EXTENSION_MANIFEST.as_posix(),
            "error": f"invalid: {exc}",
        }
    if not isinstance(payload, dict):
        return {
            "status": "invalid",
            "path": EXTENSION_MANIFEST.as_posix(),
            "error": "invalid: JSON root is not an object",
        }

    extension = payload.get("extension") if isinstance(payload.get("extension"), dict) else {}
    source = payload.get("source") if isinstance(payload.get("source"), dict) else {}
    install = payload.get("install") if isinstance(payload.get("install"), dict) else {}
    tested = extension.get("tested") if isinstance(extension.get("tested"), dict) else {}
    return {
        "status": "ok",
        "path": EXTENSION_MANIFEST.as_posix(),
        "schema_version": payload.get("schema_version"),
        "extension_id": extension.get("extension_id"),
        "version": extension.get("version"),
        "workflow_template_id": extension.get("workflow_template_id"),
        "target_trellis_cli": extension.get("target_trellis_cli"),
        "tested_trellis_cli": tested.get("trellis_cli")
        if isinstance(tested.get("trellis_cli"), list)
        else [],
        "installed_at": payload.get("installed_at"),
        "source_repo": source.get("repo"),
        "source_ref": source.get("ref"),
        "source_commit": source.get("commit"),
        "source_tree_state": source.get("tree_state"),
        "source_is_mutable_ref": source.get("is_mutable_ref"),
        "selected_platforms": install.get("selected_platforms")
        if isinstance(install.get("selected_platforms"), list)
        else [],
        "all_platforms": install.get("all_platforms"),
    }


def run(argv: list[str]) -> dict[str, Any]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError(
            "invalid_arguments",
            "arguments",
            "Use the exact command help contract.",
        ) from exc
    root = _repo_root(Path(args.root or Path.cwd()))
    return {
        "status": "ok",
        "repo_root": str(root),
        "guru_team_extension": extension_payload(root),
    }
