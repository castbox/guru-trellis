from __future__ import annotations

import os
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from common import git, index_tree_digest, resolve_commit
from runtime.io import CommandError


from runtime.git_merge import git_path, other_sequencer, require_merge_state


def task_metadata_snapshot(repo: Path, task_ref: str) -> tuple[str, bytes, bytes]:
    """Preserve the current, publicly validated Task record without staging it."""
    path = str(Path(task_ref) / "task.json")
    target = repo / path
    if target.is_symlink() or not target.is_file():
        raise CommandError("stale_identity", "task_ref", "Use the current regular Task record.", 3)
    entry = subprocess.run(["git", "ls-files", "--stage", "-z", "--", path], cwd=repo,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
    return path, target.read_bytes(), entry


def require_resolved_worktree(repo: Path, metadata: tuple[str, bytes, bytes],
                              *, terminal: bool = False) -> None:
    """Only the exact current Task record may differ outside the reviewed tree."""
    path = metadata[0]
    if task_metadata_snapshot(repo, str(Path(path).parent)) != metadata:
        raise CommandError("stale_identity", "task_metadata", "Preserve the current Task bytes and index entry.", 3)
    args = ["git", "status", "--porcelain=v1", "-z", "--no-renames", "--untracked-files=all", "--ignore-submodules=none"]
    status = subprocess.run(args, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
    for row in filter(None, status.split(b"\0")):
        state, changed = row[:2], row[3:]
        metadata_states = {b" M"} if terminal else {b" M", b"MM", b"AM"}
        if changed == os.fsencode(path) and state in metadata_states:
            continue
        if terminal or state[1:] != b" " or state[:1] in {b"?", b"U"}:
            raise CommandError("stale_identity", "worktree", "Stage every resolved business change; preserve only current Task metadata.", 3)


def commit_facts(repo: Path, commit: str) -> tuple[list[str], str, str]:
    return (git(repo, "show", "-s", "--format=%P", commit).split(),
            git(repo, "show", "-s", "--format=%T", commit),
            git(repo, "show", "-s", "--format=%B", commit).rstrip("\n"))


@contextmanager
def tree_index(repo: Path, tree: str) -> Iterator[Path]:
    if git(repo, "cat-file", "-t", tree, check=False) != "tree":
        raise CommandError("stale_identity", "stage0_tree", "Use a readable stage-0 tree object.", 3)
    with tempfile.TemporaryDirectory(prefix="guru-resolved-index-") as directory:
        index = Path(directory) / "index"
        loaded = subprocess.run(["git", "read-tree", tree], cwd=repo,
                                env={**os.environ, "GIT_INDEX_FILE": str(index)},
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if loaded.returncode:
            raise CommandError("stale_identity", "stage0_tree", "Read the exact reviewed tree object.", 3)
        yield index


def _index_entries(repo: Path, index: Path | None = None) -> dict[bytes, bytes]:
    entries = subprocess.run(["git", "ls-files", "--stage", "-z"], cwd=repo,
                             env={**os.environ, "GIT_INDEX_FILE": str(index)} if index else None,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
    return {path: metadata for entry in entries.split(b"\0") if entry
            for metadata, path in [entry.split(b"\t", 1)]}


def validate_integration_paths(repo: Path, prior: str, tree: str, paths: list[str],
                               index: Path, *, live_index: bool) -> None:
    changed = subprocess.run(["git", "diff", "--no-renames", "--name-only", "-z", prior, tree],
                             cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
    selected = {os.fsencode(path) for path in paths}
    if not set(filter(None, changed.split(b"\0"))) <= selected:
        raise CommandError("stale_identity", "integration_paths",
                           "Keep every candidate change inside the reviewed integration paths.", 3)
    if not live_index:
        return
    candidate, actual = _index_entries(repo, index), _index_entries(repo)
    if any(candidate.get(path) != actual.get(path) for path in selected):
        raise CommandError("stale_identity", "repository.index",
                           "The reviewed integration paths differ from the live stage-0 index.", 3)
    unstaged = subprocess.run(["git", "diff", "--quiet", "--", *paths], cwd=repo,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if unstaged.returncode or git(repo, "ls-files", "--others", "--exclude-standard", "--", *paths):
        raise CommandError("stale_identity", "worktree",
                           "Stage the reviewed integration paths before reconciliation.", 3)


def verify_commit(repo: Path, commit: str, parents: list[str], tree: str, message: str,
                  digest: str, *, recovery: bool = False) -> None:
    code = "stale_identity" if recovery else "reconciliation_failed"
    if commit_facts(repo, commit) != (parents, tree, message):
        raise CommandError(code, "reconciled_task_head",
                           "Use exactly the reviewed parents, tree, and commit message.", 3)
    with tree_index(repo, tree) as index:
        if index_tree_digest(repo, index_file=index) != digest:
            raise CommandError(code, "candidate_tree_sha256", "Use the reviewed committed tree digest.", 3)
    require_merge_state(repo, None)


def commit_tree(repo: Path, parents: list[str], tree: str, message: str, digest: str,
                *, index: Path | None = None) -> str:
    commit = subprocess.run(["git", "commit", "-m", message], cwd=repo, text=True,
                            env={**os.environ, "GIT_INDEX_FILE": str(index)} if index else None,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if commit.returncode:
        raise CommandError("reconciliation_failed", "commit",
                           commit.stderr.strip() or "The local reconciliation commit failed.", 3)
    head = resolve_commit(repo, "HEAD", "HEAD")
    verify_commit(repo, head, parents, tree, message, digest)
    return head
