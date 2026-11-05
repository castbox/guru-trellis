from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
from pathlib import Path
from typing import Any

from runtime.parent_git import ParentGitError, index_entries, parent_status_records


REVIEWED_CONTENT_ALGORITHM = "guru-reviewed-content-1.0"
REVIEWED_CONTENT_METADATA_PREFIXES = (
    ".trellis/tasks",
    ".trellis/workspace",
    ".trellis/.runtime",
)
PROVENANCE_TAIL_MANIFEST_PATH = ".trellis/guru-team/extension.json"
OS_NOISE_NAMES = frozenset({".DS_Store"})


class ReviewedContentError(RuntimeError):
    def __init__(self, message: str, payload: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.payload = payload or {}


def os_noise_path(path: str) -> bool:
    return Path(path).name in OS_NOISE_NAMES


def reviewed_content_metadata_path(path: str) -> bool:
    return (
        path == PROVENANCE_TAIL_MANIFEST_PATH
        or os_noise_path(path)
        or any(
            path == prefix or path.startswith(prefix + "/")
            for prefix in REVIEWED_CONTENT_METADATA_PREFIXES
        )
    )


def _oid(value: str) -> bool:
    return re.fullmatch(r"[0-9a-f]{40,64}", value) is not None


def _tree_entries(root: Path, commit: str) -> dict[str, dict[str, str]]:
    if not isinstance(commit, str) or not commit.strip():
        raise ReviewedContentError(
            "Reviewed-content commit must be a non-empty Git revision."
        )
    proc = subprocess.run(
        ["git", "ls-tree", "-r", "-z", "--full-tree", commit.strip()],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise ReviewedContentError(
            "Could not read the reviewed-content commit tree.",
            {"stderr": proc.stderr.decode("utf-8", "replace")},
        )
    entries: dict[str, dict[str, str]] = {}
    for record in proc.stdout.split(b"\0"):
        if not record:
            continue
        metadata_raw, separator, path_raw = record.partition(b"\t")
        if not separator:
            raise ReviewedContentError(
                "Git returned an invalid reviewed-content tree record."
            )
        try:
            path = path_raw.decode("utf-8", "strict")
            metadata = metadata_raw.decode("ascii", "strict").split()
        except UnicodeDecodeError as exc:
            raise ReviewedContentError(
                "Reviewed-content tree paths must be valid UTF-8."
            ) from exc
        if len(metadata) != 3:
            raise ReviewedContentError(
                "Git returned incomplete reviewed-content tree metadata."
            )
        mode, object_type, oid = metadata
        valid_type = (
            (mode == "160000" and object_type == "commit")
            or (mode in {"100644", "100755", "120000"} and object_type == "blob")
        )
        parts = path.split("/")
        if (
            not valid_type
            or not _oid(oid)
            or not path
            or path.startswith("/")
            or any(part in {"", ".", ".."} for part in parts)
            or path in entries
        ):
            raise ReviewedContentError(
                "Reviewed-content tree contains an unsupported or ambiguous entry.",
                {"path": path},
            )
        if not reviewed_content_metadata_path(path):
            entries[path] = {"path": path, "mode": mode, "oid": oid}
    return entries


def _status_records(root: Path) -> list[dict[str, Any]]:
    try:
        return parent_status_records(root)
    except ParentGitError as exc:
        raise ReviewedContentError(str(exc)) from exc


def _worktree_content(root: Path, path: str) -> tuple[bytes | None, str | None]:
    target = root / path
    try:
        metadata = target.lstat()
    except FileNotFoundError:
        return None, None
    if stat.S_ISLNK(metadata.st_mode):
        return os.fsencode(os.readlink(target)), "120000"
    if not stat.S_ISREG(metadata.st_mode):
        return None, None
    return target.read_bytes(), "100755" if metadata.st_mode & stat.S_IXUSR else "100644"


def _blob_oid(root: Path, content: bytes) -> str:
    proc = subprocess.run(
        ["git", "hash-object", "--stdin"],
        cwd=str(root),
        input=content,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    oid = proc.stdout.decode("ascii", "strict").strip() if proc.returncode == 0 else ""
    if not _oid(oid):
        raise ReviewedContentError(
            "Could not calculate a reviewed-content blob identity.",
            {"stderr": proc.stderr.decode("utf-8", "replace")},
        )
    return oid


def _worktree_overlays(root: Path) -> list[dict[str, Any]]:
    overlays: list[dict[str, Any]] = []
    try:
        index = index_entries(root)
    except ParentGitError as exc:
        raise ReviewedContentError(str(exc)) from exc
    for record in _status_records(root):
        path = str(record["path"])
        renamed_from = record.get("renamed_from")
        if isinstance(renamed_from, str) and not reviewed_content_metadata_path(renamed_from):
            overlays.append({"path": renamed_from, "deleted": True})
        if reviewed_content_metadata_path(path):
            continue
        status_text = str(record["status_text"])
        index_entry = index.get(path, {})
        index_oid, index_mode = index_entry.get("oid"), index_entry.get("mode")
        if "D" in status_text:
            overlays.append({"path": path, "deleted": True})
            continue
        if index_mode == "160000":
            overlays.append(
                {"path": path, "deleted": False, "mode": "160000", "oid": index_oid}
            )
            continue
        content, mode = _worktree_content(root, path)
        if content is None or mode is None:
            raise ReviewedContentError(
                "Reviewed-content worktree entry is unavailable or unsupported.",
                {"path": path},
            )
        overlays.append(
            {"path": path, "deleted": False, "mode": mode, "oid": _blob_oid(root, content)}
        )
    return sorted(
        overlays,
        key=lambda item: (item["path"].encode("utf-8"), 0 if item.get("deleted") else 1),
    )


def _validate_gitlinks(
    root: Path,
    entries: dict[str, dict[str, str]],
    recorded: dict[str, str],
    overlays: dict[str, dict[str, Any]],
) -> None:
    """Validate parent index bindings for identity and promotion reconstruction."""
    try:
        current = index_entries(root)
    except ParentGitError as exc:
        raise ReviewedContentError(str(exc)) from exc
    for path, entry in entries.items():
        if entry["mode"] != "160000":
            continue
        expected = overlays.get(path, {}).get("oid") or recorded.get(path)
        if current.get(path) != {"path": path, "mode": "160000", "oid": expected}:
            raise ReviewedContentError(
                "Reviewed-content parent gitlink index binding changed during capture.",
                {"path": path},
            )


def reviewed_content_identity(
    root: Path,
    commit: str = "HEAD",
    include_worktree: bool = True,
) -> dict[str, str]:
    root = Path(root)
    if include_worktree:
        resolved = subprocess.run(
            ["git", "rev-parse", commit], cwd=str(root), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=str(root), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if resolved.returncode != 0 or head.returncode != 0 or resolved.stdout.strip() != head.stdout.strip():
            raise ReviewedContentError(
                "Reviewed-content worktree overlays require the current HEAD commit."
            )
    entries = _tree_entries(root, commit)
    if include_worktree:
        recorded_gitlinks = {path: row["oid"] for path, row in entries.items()
                             if row["mode"] == "160000"}
        gitlink_overlays = {}
        for overlay in _worktree_overlays(root):
            path = str(overlay["path"])
            if overlay.get("deleted"):
                entries.pop(path, None)
                continue
            entries[path] = {"path": path, "mode": str(overlay["mode"]), "oid": str(overlay["oid"])}
            if overlay["mode"] == "160000":
                gitlink_overlays[path] = overlay
        _validate_gitlinks(root, entries, recorded_gitlinks, gitlink_overlays)
    canonical_entries = sorted(entries.values(), key=lambda item: item["path"].encode("utf-8"))
    payload = {"algorithm": REVIEWED_CONTENT_ALGORITHM, "entries": canonical_entries}
    sha256 = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    return {"algorithm": REVIEWED_CONTENT_ALGORITHM, "sha256": sha256}
