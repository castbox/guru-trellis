from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
from pathlib import Path
from typing import Any


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
    proc = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise ReviewedContentError(
            "Could not capture the reviewed-content Git snapshot.",
            {"stderr": proc.stderr.decode("utf-8", "replace")},
        )
    fields = proc.stdout.split(b"\0")
    records: list[dict[str, Any]] = []
    index = 0
    while index < len(fields):
        field = fields[index]
        index += 1
        if not field:
            continue
        if len(field) < 4:
            raise ReviewedContentError("Git returned an invalid porcelain status record.")
        status_text = field[:2].decode("ascii", "strict")
        if status_text in {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}:
            raise ReviewedContentError(
                "Reviewed Git state contains an unresolved merge entry."
            )
        path = field[3:].decode("utf-8", "strict")
        renamed_from: str | None = None
        relation_kinds = {item for item in status_text if item in {"R", "C"}}
        if len(relation_kinds) > 1:
            raise ReviewedContentError(
                "Git returned an ambiguous rename/copy status record."
            )
        if relation_kinds:
            if index >= len(fields) or not fields[index]:
                raise ReviewedContentError(
                    "Git returned an incomplete rename/copy status record."
                )
            source = fields[index].decode("utf-8", "strict")
            index += 1
            if relation_kinds == {"R"}:
                renamed_from = source
        records.append(
            {"status_text": status_text, "path": path, "renamed_from": renamed_from}
        )
    return records


def _index_identity(root: Path, path: str) -> tuple[str | None, str | None]:
    proc = subprocess.run(
        ["git", "--literal-pathspecs", "ls-files", "-s", "-z", "--", path],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise ReviewedContentError(
            "Could not read the reviewed-content index identity.",
            {"stderr": proc.stderr.decode("utf-8", "replace")},
        )
    records = [record for record in proc.stdout.split(b"\0") if record]
    if not records:
        return None, None
    if len(records) != 1:
        raise ReviewedContentError("Reviewed-content index identity is ambiguous.")
    metadata_raw, separator, record_path = records[0].partition(b"\t")
    metadata = metadata_raw.decode("ascii", "strict").split()
    if (
        not separator
        or record_path.decode("utf-8", "strict") != path
        or len(metadata) != 3
        or metadata[2] != "0"
    ):
        raise ReviewedContentError("Reviewed-content index identity is invalid.")
    return metadata[1], metadata[0]


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


def _gitlink_worktree_head(root: Path, path: str) -> str:
    target = root / path
    try:
        metadata = target.lstat()
    except FileNotFoundError as exc:
        raise ReviewedContentError(
            "Reviewed-content gitlink worktree is not initialized.", {"path": path}
        ) from exc
    if not stat.S_ISDIR(metadata.st_mode):
        raise ReviewedContentError(
            "Reviewed-content gitlink worktree is not an exact directory.",
            {"path": path},
        )
    top = subprocess.run(
        ["git", "-C", str(target), "rev-parse", "--show-toplevel"],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    try:
        exact = target.resolve(strict=True)
        reported = (
            Path(top.stdout.decode("utf-8", "strict").rstrip("\n")).resolve(strict=True)
            if top.returncode == 0
            else None
        )
    except (OSError, RuntimeError) as exc:
        raise ReviewedContentError(
            "Reviewed-content gitlink worktree root is ambiguous.", {"path": path}
        ) from exc
    if reported != exact:
        raise ReviewedContentError(
            "Reviewed-content gitlink worktree is uninitialized or root-mismatched.",
            {"path": path},
        )
    head_proc = subprocess.run(
        ["git", "-C", str(target), "rev-parse", "--verify", "HEAD^{commit}"],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    head = head_proc.stdout.decode("ascii", "strict").strip() if head_proc.returncode == 0 else ""
    status_proc = subprocess.run(
        [
            "git", "-C", str(target), "status", "--porcelain=v1", "-z",
            "--untracked-files=all", "--ignore-submodules=none",
        ],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if not _oid(head) or status_proc.returncode != 0 or status_proc.stdout:
        raise ReviewedContentError(
            "Reviewed-content gitlink identity is unavailable or dirty.",
            {"path": path},
        )
    return head


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
    for record in _status_records(root):
        path = str(record["path"])
        renamed_from = record.get("renamed_from")
        if isinstance(renamed_from, str) and not reviewed_content_metadata_path(renamed_from):
            overlays.append({"path": renamed_from, "deleted": True})
        if reviewed_content_metadata_path(path):
            continue
        status_text = str(record["status_text"])
        index_oid, index_mode = _index_identity(root, path)
        if "D" in status_text:
            overlays.append({"path": path, "deleted": True})
            continue
        if index_mode == "160000":
            oid = _gitlink_worktree_head(root, path)
            if status_text[0] not in {" ", "?"} and index_oid != oid:
                raise ReviewedContentError(
                    "Reviewed-content gitlink index pointer does not match its worktree binding.",
                    {"path": path},
                )
            overlays.append(
                {"path": path, "deleted": False, "mode": "160000", "oid": oid, "index_oid": index_oid}
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
    for path, entry in entries.items():
        if entry["mode"] != "160000":
            continue
        expected = str(overlays.get(path, {}).get("oid") or recorded.get(path) or "")
        expected_index = str(
            overlays.get(path, {}).get("index_oid") or recorded.get(path) or ""
        )
        if not _oid(expected) or not _oid(expected_index):
            raise ReviewedContentError(
                "Reviewed-content gitlink binding is unavailable or ambiguous.",
                {"path": path},
            )
        current_index, current_mode = _index_identity(root, path)
        if current_index != expected_index or current_mode != "160000":
            raise ReviewedContentError(
                "Reviewed-content gitlink index binding drifted after capture.",
                {"path": path},
            )
        target = root / path
        deinitialized = not target.exists()
        if target.is_dir():
            try:
                with os.scandir(target) as children:
                    deinitialized = next(children, None) is None
            except OSError as exc:
                raise ReviewedContentError(
                    "Reviewed-content gitlink worktree root is ambiguous.", {"path": path}
                ) from exc
        if deinitialized:
            if path in overlays:
                raise ReviewedContentError(
                    "Reviewed-content gitlink overlay requires an initialized worktree.",
                    {"path": path},
                )
        elif _gitlink_worktree_head(root, path) != expected:
            raise ReviewedContentError(
                "Reviewed-content gitlink worktree HEAD drifted after capture.",
                {"path": path},
            )
        entry["oid"] = expected


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
    recorded_gitlinks = {
        path: entry["oid"] for path, entry in entries.items() if entry["mode"] == "160000"
    }
    if include_worktree:
        gitlink_overlays: dict[str, dict[str, Any]] = {}
        for overlay in _worktree_overlays(root):
            path = str(overlay["path"])
            existing = entries.get(path)
            if overlay.get("deleted"):
                if existing is not None and existing["mode"] == "160000":
                    raise ReviewedContentError(
                        "Reviewed-content gitlink deletion or replacement is unsupported.",
                        {"path": path},
                    )
                entries.pop(path, None)
                continue
            mode = str(overlay["mode"])
            if existing is not None and existing["mode"] == "160000" and mode != "160000":
                raise ReviewedContentError(
                    "Reviewed-content gitlink deletion or replacement is unsupported.",
                    {"path": path},
                )
            entries[path] = {"path": path, "mode": mode, "oid": str(overlay["oid"])}
            if mode == "160000":
                gitlink_overlays[path] = overlay
        _validate_gitlinks(root, entries, recorded_gitlinks, gitlink_overlays)
    canonical_entries = sorted(entries.values(), key=lambda item: item["path"].encode("utf-8"))
    payload = {"algorithm": REVIEWED_CONTENT_ALGORITHM, "entries": canonical_entries}
    sha256 = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    return {"algorithm": REVIEWED_CONTENT_ALGORITHM, "sha256": sha256}
