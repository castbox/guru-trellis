from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path, PurePosixPath

from runtime.io import CommandError
from runtime.schema import validate_json


def validate_input(package_root: Path, public_input: dict) -> None:
    validate_json(public_input, package_root / "schemas/public-input.schema.json", "public_input")
    for index, value in enumerate(public_input.get("paths", [])):
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or "\x00" in value:
            raise CommandError("invalid_scope", f"public_input.paths.{index}", "Use literal paths within the selected Git repository.")


def _git(root: Path, *args: str, field: str = "repository", missing_status: int | None = None) -> bytes:
    environment = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args], env=environment,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
    except OSError as exc:
        raise CommandError("git_unavailable", field, "Make Git and the selected repository available.") from exc
    if result.returncode == missing_status:
        return b""
    if result.returncode:
        # Do not echo repository contents or configured external command output.
        raise CommandError("git_unavailable", field, "Use an accessible Git working tree and existing commit references.")
    return result.stdout


def capture(package_root: Path, public_input: dict) -> dict:
    validate_input(package_root, public_input)
    requested = Path(public_input["repository"]).resolve()
    root = Path(os.fsdecode(_git(requested, "rev-parse", "--show-toplevel")).rstrip("\n")).resolve()
    if public_input["profile"] == "committed_range":
        base = _git(root, "rev-parse", "--verify", "--end-of-options", f"{public_input['base']}^{{commit}}", field="public_input.base").decode().strip()
        head = _git(root, "rev-parse", "--verify", "--end-of-options", f"{public_input['head']}^{{commit}}", field="public_input.head").decode().strip()
    else:
        head = _git(root, "rev-parse", "--verify", "--quiet", "HEAD^{commit}", missing_status=1).decode().strip() or None
        if head is None:
            # A newly initialized branch has a symbolic HEAD but no commit yet.
            _git(root, "symbolic-ref", "--quiet", "HEAD", field="repository.HEAD")
        base = head
    paths = [str(PurePosixPath(path)) for path in public_input.get("paths", [])]
    selectors = [] if "." in paths else [f":(top,literal){path}" for path in paths]
    digest = hashlib.sha256()

    def bind(label: str, value: bytes) -> None:
        name = label.encode()
        digest.update(len(name).to_bytes(8, "big"))
        digest.update(name)
        digest.update(len(value).to_bytes(8, "big"))
        digest.update(value)

    bind("selection", json.dumps(public_input, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode())
    bind("repository_root", os.fsencode(root))
    bind("base", json.dumps(base).encode())
    bind("head", json.dumps(head).encode())
    options = ["--no-ext-diff", "--no-textconv", "--no-color", "--binary", "--full-index", "--no-renames", "--ignore-submodules=none"]
    if public_input["profile"] == "committed_range":
        bind("committed", _git(root, "diff", *options, base, head, "--", *selectors))
    else:
        baseline = [head] if head is not None else []
        bind("staged", _git(root, "diff", *options, "--cached", *baseline, "--", *selectors))
        bind("unstaged", _git(root, "diff", *options, "--", *selectors))
        untracked = _git(root, "ls-files", "--others", "--exclude-standard", "-z", "--", *selectors)
        for raw in sorted(path for path in untracked.split(b"\x00") if path):
            path = root / os.fsdecode(raw)
            try:
                mode = path.lstat().st_mode
                if stat.S_ISLNK(mode):
                    content = os.fsencode(os.readlink(path))
                    kind = "symlink"
                elif stat.S_ISREG(mode):
                    content = path.read_bytes()
                    kind = "executable" if mode & stat.S_IXUSR else "file"
                else:
                    raise CommandError("unsupported_content", "public_input.paths", "Select regular Git files or symlinks; review submodule contents in their own repository.")
            except OSError as exc:
                raise CommandError("content_unavailable", "public_input.paths", "Reread the selected files and recapture the review scope.") from exc
            bind(f"untracked:{kind}", raw)
            bind("content", content)
    snapshot = {
        "schema_version": "1.0", "repository_root": str(root),
        "base_oid": base, "head_oid": head, "content_identity": digest.hexdigest(),
    }
    validate_json(snapshot, package_root / "schemas/snapshot.schema.json", "snapshot")
    return snapshot
