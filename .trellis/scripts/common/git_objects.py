"""Operation-local immutable tree snapshots and bounded, spooled blob reads."""
from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Callable, Protocol, TypeVar


@dataclass(frozen=True)
class TreeEntry:
    mode: str
    kind: str
    oid: str


Fact = TypeVar("Fact")
BATCH_SIZE = 128
CHUNK_SIZE = 64 * 1024


class ByteReader(Protocol):
    def read(self, size: int = -1, /) -> bytes: ...


def read_tree(root: Path, revision: str, scope: str | None = None,
              *, env: dict[str, str] | None = None) -> dict[str, TreeEntry]:
    """Keep literal paths and tree entries (directories must not become deletions)."""
    args = ["git", "-C", str(root), "ls-tree", "-r", "-t", "-z", revision]
    if scope is not None:
        args.extend(["--", scope])
    output = subprocess.run(args, capture_output=True, check=True, timeout=20, env=env).stdout
    entries = {}
    for row in output.split(b"\0"):
        if not row:
            continue
        header, name = row.split(b"\t", 1)
        mode, kind, oid = header.decode("ascii").split(" ")
        entries[name.decode("utf-8", errors="surrogateescape")] = TreeEntry(mode, kind, oid)
    return entries


def read_blob_facts(root: Path, oids: list[str], observe: Callable[[BinaryIO, int], Fact],
                    *, env: dict[str, str] | None = None) -> dict[str, Fact]:
    """Read each unique blob once; observers retain reduced facts, not bodies.

    Regular temporary request/output files avoid duplex-pipe deadlocks. Each
    observer consumes exactly one body using bounded reads; batches and files
    close even when Git or an observer fails.
    """
    unique = list(dict.fromkeys(oids))
    facts = {}
    for offset in range(0, len(unique), BATCH_SIZE):
        batch = unique[offset:offset + BATCH_SIZE]
        with tempfile.TemporaryFile() as requests, tempfile.TemporaryFile() as output:
            requests.write(("\n".join(batch) + "\n").encode("ascii"))
            requests.seek(0)
            subprocess.run(["git", "-C", str(root), "cat-file", "--batch"],
                           stdin=requests, stdout=output, stderr=subprocess.PIPE,
                           check=True, timeout=20, env=env)
            output.seek(0)
            for oid in batch:
                header = output.readline(256).split()
                if len(header) != 3 or header[0].decode("ascii") != oid or header[1] != b"blob":
                    raise ValueError(f"unreadable Git blob: {oid}")
                size = int(header[2])
                if size < 0:
                    raise ValueError(f"invalid Git blob size: {oid}")
                start = output.tell()
                facts[oid] = observe(output, size)
                if output.tell() != start + size or output.read(1) != b"\n":
                    raise ValueError(f"invalid Git blob body: {oid}")
    return facts


def verify_blob_objects(root: Path, oids: list[str], *, env: dict[str, str] | None = None) -> None:
    """Retain actual object availability checks when content SHA256 is reused.

    A tree entry alone does not prove its promised blob is locally available.
    Let Git resolve/fetch the object as before, without rereading its body.
    """
    unique = list(dict.fromkeys(oids))
    for offset in range(0, len(unique), BATCH_SIZE):
        batch = unique[offset:offset + BATCH_SIZE]
        with tempfile.TemporaryFile() as requests, tempfile.TemporaryFile() as output:
            requests.write(("\n".join(batch) + "\n").encode("ascii"))
            requests.seek(0)
            subprocess.run(["git", "-C", str(root), "cat-file", "--batch-check"],
                           stdin=requests, stdout=output, stderr=subprocess.PIPE,
                           check=True, timeout=20, env=env)
            output.seek(0)
            for oid in batch:
                header = output.readline(256).split()
                if (len(header) != 3 or header[0].decode("ascii") != oid
                        or header[1] != b"blob" or not header[2].isdigit()):
                    raise ValueError(f"unreadable Git blob: {oid}")


def hash_blob(stream: ByteReader, size: int) -> str:
    """SHA256 raw content using bounded reads, including empty blobs."""
    import hashlib

    digest = hashlib.sha256()
    while size:
        chunk = stream.read(min(size, CHUNK_SIZE))
        if not chunk:
            raise ValueError("truncated Git blob")
        digest.update(chunk)
        size -= len(chunk)
    return digest.hexdigest()
