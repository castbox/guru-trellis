"""Shared read-only merge-operation facts for Check and Reconcile."""
from pathlib import Path
import subprocess
from runtime.io import CommandError

def _git(repo, *args):
    result = subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True)
    if result.returncode:
        raise CommandError("stale_identity", "repository", result.stderr.strip() or "Repair Git state.", 3)
    return result.stdout.strip()


def git_path(repo: Path, name: str) -> Path:
    path = Path(_git(repo, "rev-parse", "--git-path", name))
    return path if path.is_absolute() else repo / path


def other_sequencer(repo: Path) -> str | None:
    for name in ("CHERRY_PICK_HEAD", "REVERT_HEAD", "REBASE_HEAD", "BISECT_LOG",
                 "sequencer", "rebase-merge", "rebase-apply"):
        if git_path(repo, name).exists():
            return name
    return None


def require_merge_state(repo: Path, new_base: str | None) -> None:
    other = other_sequencer(repo)
    if other:
        raise CommandError("stale_identity", "repository.operation",
                           f"Finish or abort the other Git operation: {other}.", 3)
    path = git_path(repo, "MERGE_HEAD")
    if new_base is None:
        if path.exists():
            raise CommandError("stale_identity", "repository.operation",
                               "Recover only a terminal Git merge state.", 3)
        return
    if not path.is_file() or path.is_symlink():
        raise CommandError("stale_identity", "merge_head", "Use the active reviewed merge operation.", 3)
    if [line.strip() for line in path.read_text().splitlines() if line.strip()] != [new_base]:
        raise CommandError("stale_identity", "merge_head", "Bind exactly one reviewed MERGE_HEAD.", 3)
    if _git(repo, "ls-files", "--unmerged"):
        raise CommandError("stale_identity", "repository.index", "Resolve every conflict before reconciliation.", 3)


