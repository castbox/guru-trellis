"""Finite, call-local Git object bytes shared by two fact readers."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile


class GitObjectBatchError(ValueError):
    def __init__(self, message, *, git_failed=False):
        super().__init__(message)
        self.git_failed = git_failed


class GitObjectBatch:
    def __init__(self, root, *, git_dir=None, environment=None):
        self.root = Path(root).resolve()
        self.git_dir = Path(git_dir).resolve() if git_dir is not None else None
        self.environment = dict(os.environ if environment is None else environment)
        self.entries = {}
        self.response = tempfile.TemporaryFile()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.response.close()

    def ensure(self, oids):
        wanted = list(dict.fromkeys(oids))
        pending = [oid for oid in wanted if oid not in self.entries]
        missing = {}
        if pending:
            self.response.seek(0, os.SEEK_END)
            start = self.response.tell()
            with tempfile.TemporaryFile() as request:
                for oid in pending:
                    request.write(oid.encode("ascii") + b"\n")
                request.seek(0)
                command = ["git"]
                if self.git_dir is not None:
                    command.append(f"--git-dir={self.git_dir}")
                command.extend(["cat-file", "--batch"])
                result = subprocess.run(command, cwd=self.root, env=self.environment,
                                        stdin=request, stdout=self.response, stderr=subprocess.PIPE)
                if result.returncode:
                    raise GitObjectBatchError(result.stderr.decode("utf-8", "replace").strip()
                                              or "Read the selected Git objects.", git_failed=True)
            end = self.response.seek(0, os.SEEK_END)
            self.response.seek(start)
            complete = {}
            for oid in pending:
                header = self.response.readline(256).split()
                if header == [oid.encode("ascii"), b"missing"]:
                    # Absence of an object can change after ordinary preparation;
                    # only successful immutable bytes enter the reusable cache.
                    missing[oid] = None
                    continue
                if (len(header) != 3 or header[0] != oid.encode("ascii")
                        or header[1] not in {b"blob", b"tree", b"commit", b"tag"}
                        or not header[2].isdigit()):
                    raise GitObjectBatchError("Git returned an invalid object batch entry.")
                size = int(header[2])
                offset = self.response.tell()
                if offset + size >= end:
                    raise GitObjectBatchError("Git returned an incomplete object batch response.")
                self.response.seek(size, os.SEEK_CUR)
                if self.response.read(1) != b"\n":
                    raise GitObjectBatchError("Git returned an incomplete object batch response.")
                complete[oid] = (header[1].decode("ascii"), offset, size)
            if self.response.tell() != end:
                raise GitObjectBatchError("Git returned an invalid object batch response length.")
            self.entries.update(complete)
        return {oid: self.entries.get(oid) if oid not in missing else None for oid in wanted}

    def read_bytes(self, oid):
        _, offset, size = self.entries[oid]
        self.response.seek(offset)
        data = self.response.read(size)
        if len(data) != size:
            raise GitObjectBatchError("Git returned an incomplete object batch response.")
        return data

    def copy_to(self, oid, output):
        _, offset, remaining = self.entries[oid]
        self.response.seek(offset)
        while remaining:
            data = self.response.read(min(1024 * 1024, remaining))
            if not data:
                raise GitObjectBatchError("Git returned an incomplete object batch response.")
            output.write(data)
            remaining -= len(data)
