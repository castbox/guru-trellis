"""Parent-repository Git facts without consulting gitlink worktrees."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path


class ParentGitError(RuntimeError):
    pass


def _git(root: Path, *args: str, allow_missing: bool = False) -> bytes:
    result = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    if result.returncode:
        if allow_missing:
            return b""
        raise ParentGitError(result.stderr.decode("utf-8", "replace").strip()
                             or "Could not read parent Git state.")
    return result.stdout


def index_entries(root: Path) -> dict[str, dict[str, str]]:
    """Return unique stage-0 path/mode/OID entries; absence means untracked."""
    entries = {}
    for raw in filter(None, _git(root, "ls-files", "--stage", "-z").split(b"\0")):
        metadata, path = raw.split(b"\t", 1)
        mode, oid, stage = metadata.decode("ascii").split()
        name = path.decode("utf-8", "strict")
        if stage != "0" or name in entries:
            raise ParentGitError("Resolve every parent index entry before capture.")
        if not re.fullmatch(r"[0-9a-f]{40,64}", oid):
            raise ParentGitError("Parent index returned an invalid object id.")
        entries[name] = {"path": name, "mode": mode, "oid": oid}
    return entries


def head_entries(root: Path, commit: str = "HEAD") -> dict[str, dict[str, str]]:
    """Read the parent tree; an unborn HEAD has no committed entries."""
    if commit == "HEAD" and not _git(root, "rev-parse", "--verify", "HEAD", allow_missing=True):
        return {}
    entries = {}
    for raw in filter(None, _git(root, "ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0")):
        metadata, path = raw.split(b"\t", 1)
        mode, _kind, oid = metadata.decode("ascii").split()
        name = path.decode("utf-8", "strict")
        entries[name] = {"path": name, "mode": mode, "oid": oid}
    return entries


def parent_status_records(root: Path) -> list[dict[str, str | None]]:
    """Project porcelain XY records, retaining cached gitlinks, ignoring children.

    Git's ignore-submodules=all also hides cached gitlink changes. Read those
    changes separately from the parent index/tree rather than inspecting a child.
    A removed gitlink may leave its checkout directory behind; that directory
    is not a new parent worktree file.
    """
    current = index_entries(root)
    committed = head_entries(root)
    gitlink_paths = {p for p, e in current.items() if e["mode"] == "160000"}
    deleted_gitlinks = {p for p, e in committed.items()
                        if e["mode"] == "160000" and p not in current}
    fields = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all",
                  "--ignore-submodules=all").split(b"\0")
    rows = {}
    i = 0
    while i < len(fields):
        field = fields[i]
        i += 1
        if not field:
            continue
        if len(field) < 4:
            raise ParentGitError("Git returned an invalid parent status record.")
        status = field[:2].decode("ascii")
        path = field[3:].decode("utf-8", "strict")
        renamed = copied = None
        kinds = {c for c in status if c in "RC"}
        if kinds:
            if len(kinds) != 1 or i >= len(fields) or not fields[i]:
                raise ParentGitError("Git returned an ambiguous parent rename/copy.")
            source = fields[i].decode("utf-8", "strict")
            i += 1
            if kinds == {"R"}:
                renamed = source
            else:
                copied = source
        if path in gitlink_paths:
            continue
        if any((path == p or path.startswith(p + "/")) and path not in current
               for p in gitlink_paths | deleted_gitlinks):
            continue
        rows[path] = {"status_text": status, "path": path,
                      "renamed_from": renamed, "copied_from": copied}

    cached = _git(root, "diff", "--cached", "--name-status", "-z", "--no-renames",
                  "--ignore-submodules=none").split(b"\0")
    for i in range(0, len(cached) - 1, 2):
        status, name = cached[i], cached[i + 1]
        if not status or not name:
            continue
        path = name.decode("utf-8", "strict")
        old = committed.get(path)
        new = current.get(path)
        if not ((old and old["mode"] == "160000") or (new and new["mode"] == "160000")):
            continue
        previous = rows.get(path)
        # Ordinary replacement content retains its worktree status. Gitlink
        # contents and staged removals derive only from the parent index.
        worktree = previous["status_text"][1] if previous and new and new["mode"] != "160000" else " "
        rows[path] = {"status_text": status[:1].decode("ascii") + worktree,
                      "path": path, "renamed_from": None, "copied_from": None}
    return sorted(rows.values(), key=lambda row: str(row["path"]).encode("utf-8"))
