"""Call-local immutable objects for Merge candidate snapshots.

Only metadata and blob offsets remain in memory. Both cat-file directions are
regular files, so Git can finish before the response is parsed (#579).
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

from runtime.io import CommandError


ARGV_BYTES = 64 * 1024
COPY_BYTES = 1024 * 1024


def unreadable(message):
    return CommandError("stale_identity", "repository", message, 3)


class CandidateObjects:
    def __init__(self, root, *, no_lazy_fetch=False):
        self.root = Path(root).resolve()
        self.environment = dict(os.environ)
        if no_lazy_fetch:
            self.environment["GIT_NO_LAZY_FETCH"] = "1"
        self.entries = {}
        self.blobs = {}
        self.response = tempfile.TemporaryFile()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.response.close()

    def run(self, args, **kwargs):
        result = subprocess.run(["git", *args], cwd=self.root,
                                env=self.environment,
                                stderr=subprocess.PIPE, **kwargs)
        if result.returncode:
            raise unreadable(result.stderr.decode("utf-8", "replace").strip()
                             or "Refresh the target-base Git objects and retry.")
        return result

    def read(self, head, paths, *, files_only=False):
        # Resolve moving refs on every entry; cache only the resulting immutable
        # commit and each exact path in this actual repository context.
        commit = self.run(["rev-parse", "--verify", head + "^{commit}"],
                          stdout=subprocess.PIPE).stdout.strip().decode("ascii")
        missing = list(dict.fromkeys(path for path in paths if (commit, path) not in self.entries))
        args = ["ls-tree", "-z", commit, "--"]
        fixed_bytes = sum(len(os.fsencode(arg)) + 1 for arg in ["git", *args])
        chunk, used = [], fixed_bytes
        for path in missing:
            size = len(path.encode("utf-8")) + 1
            if chunk and used + size > ARGV_BYTES:
                self.read_entries(commit, args, chunk)
                chunk, used = [], fixed_bytes
            chunk.append(path)
            used += size
        if chunk:
            self.read_entries(commit, args, chunk)
        entries = {path: self.entries[commit, path] for path in paths}
        if files_only:
            for row in entries.values():
                if row is not None and (row[1] != "blob" or row[0] not in {"100644", "100755"}):
                    raise CommandError("stale_identity", "candidate.paths",
                                       "Use the file/mode candidate supported by the installed public API.", 3)
        wanted = {row[2]: row[1] for row in entries.values() if row is not None}
        self.read_blobs({oid: kind for oid, kind in wanted.items() if oid not in self.blobs})
        return entries

    def read_entries(self, commit, args, paths):
        result = self.run([*args, *paths], stdout=subprocess.PIPE).stdout
        rows = {}
        for row in result.split(b"\0"):
            if not row:
                continue
            metadata, path = row.split(b"\t", 1)
            mode, kind, oid = metadata.decode("ascii").split()
            rows[path.decode("utf-8")] = (mode, kind, oid)
        for path in paths:
            self.entries[commit, path] = rows.get(path)

    def read_blobs(self, oids):
        if not oids:
            return
        # Append each completed Git response to one call-local spool. Previously
        # read blobs keep offsets here, without open files or duplicate copies.
        self.response.seek(0, os.SEEK_END)
        start = self.response.tell()
        with tempfile.TemporaryFile() as request:
            for oid in oids:
                request.write(oid.encode("ascii") + b"\n")
            request.seek(0)
            self.run(["cat-file", "--batch"], stdin=request, stdout=self.response)
        end = self.response.seek(0, os.SEEK_END)
        self.response.seek(start)
        pending = {}
        for oid in oids:
            header = self.response.readline(256).split()
            if len(header) != 3 or header[:2] != [oid.encode("ascii"), oids[oid].encode("ascii")] or not header[2].isdigit():
                raise unreadable("Git returned a missing or invalid candidate blob response.")
            size = int(header[2])
            offset = self.response.tell()
            if offset + size >= end:
                raise unreadable("Git returned an incomplete candidate blob response.")
            self.response.seek(size, os.SEEK_CUR)
            if self.response.read(1) != b"\n":
                raise unreadable("Git returned an incomplete candidate blob response.")
            pending[oid] = (offset, size)
        if self.response.tell() != end:
            raise unreadable("Git returned an invalid candidate blob response length.")
        self.blobs.update(pending)

    def snapshot(self, head, paths, destination):
        for locator, row in self.read(head, paths, files_only=True).items():
            if row is None:
                continue
            mode, _, oid = row
            offset, size = self.blobs[oid]
            self.response.seek(offset)
            file = destination / locator
            file.parent.mkdir(parents=True, exist_ok=True)
            with file.open("wb") as output:
                remaining = size
                while remaining:
                    data = self.response.read(min(COPY_BYTES, remaining))
                    if not data:
                        raise unreadable("Git returned an incomplete candidate blob response.")
                    output.write(data)
                    remaining -= len(data)
            file.chmod(0o755 if mode == "100755" else 0o644)
