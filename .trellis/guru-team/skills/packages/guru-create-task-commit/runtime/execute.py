from __future__ import annotations

import argparse
import os
import shlex
import stat
import subprocess
from pathlib import Path

from common import capture_snapshot, git, load, parse, repo_rel, root, validate_candidate
from runtime.io import CommandError
from runtime.temporary_lifecycle import temporary_directory


HOOK_NAMES = ("pre-commit", "prepare-commit-msg", "commit-msg", "post-commit")


def index_entries(repo: Path, excluded: set[str] | None = None) -> dict[str, str]:
    excluded = excluded or set()
    process = subprocess.run(
        ["git", "ls-files", "--stage", "-z"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise CommandError(
            "stale_identity",
            "index",
            process.stderr.decode(errors="replace").strip() or "Read the live index.",
            3,
        )
    result: dict[str, str] = {}
    for record in process.stdout.split(b"\0"):
        if not record:
            continue
        metadata, separator, path = record.partition(b"\t")
        if not separator:
            raise CommandError(
                "stale_identity", "index", "Git returned an invalid index entry.", 3
            )
        name = path.decode("utf-8")
        if name not in excluded:
            result[name] = metadata.decode("ascii")
    return result


def _hook_path(repo: Path, name: str) -> Path:
    configured = git(
        repo, "config", "--path", "--get", "core.hooksPath", check=False
    ).stdout.strip()
    if configured:
        root = Path(configured)
        if not root.is_absolute():
            root = repo / root
        return root / name
    value = git(
        repo,
        "rev-parse",
        "--path-format=absolute",
        "--git-path",
        f"hooks/{name}",
    ).stdout.strip()
    return Path(value)


def _install_hook_proxies(repo: Path, proxy_root: Path, log_path: Path) -> None:
    proxy_root.mkdir(mode=0o700)
    for name in HOOK_NAMES:
        original = _hook_path(repo, name)
        proxy = proxy_root / name
        script = [
            "#!/bin/sh",
            "set +e",
            f"original={shlex.quote(str(original))}",
            "if [ -x \"$original\" ]; then",
            "  \"$original\" \"$@\"",
            "  rc=$?",
            "else",
            "  rc=0",
            "fi",
            f"printf '%s\\t%s\\n' {shlex.quote(name)} \"$rc\" >> {shlex.quote(str(log_path))}",
            "exit \"$rc\"",
            "",
        ]
        proxy.write_text("\n".join(script))
        proxy.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)


def _hook_results(log_path: Path) -> list[dict[str, object]]:
    if not log_path.is_file():
        return []
    results = []
    for line in log_path.read_text().splitlines():
        name, separator, value = line.partition("\t")
        if not separator or name not in HOOK_NAMES:
            continue
        try:
            exit_code = int(value)
        except ValueError:
            continue
        results.append({"name": name, "exit_code": exit_code})
    return results


def _commit_failure(
    *,
    stage: str,
    message: str,
    pre_commit_head: str,
    commit_sha: str | None,
    hook_results: list[dict[str, object]],
) -> CommandError:
    response: dict[str, object] = {
        "code": "stale_identity",
        "field_path": "commit_transaction",
        "remediation": message,
        "transaction_stage": stage,
        "pre_commit_head": pre_commit_head,
        "hook_results": hook_results,
    }
    if commit_sha:
        response["created_commit_sha"] = commit_sha
    return CommandError(
        "stale_identity",
        "commit_transaction",
        message,
        3,
        response=response,
    )


def _materialize_exact_index(repo: Path, candidate: dict, env: dict[str, str]) -> str:
    pre = candidate["git"]["pre_commit_head"]
    git(repo, "read-tree", pre, env=env)
    git(repo, "add", "-A", "--", *candidate["exact_stage_paths"], env=env)
    return git(repo, "write-tree", env=env).stdout.strip()


def _raw_commit_message(repo: Path, commit: str) -> str:
    process = subprocess.run(
        ["git", "cat-file", "commit", commit],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise CommandError(
            "stale_identity",
            "commit",
            process.stderr.decode(errors="replace").strip() or "Read the created commit object.",
            3,
        )
    _headers, separator, message = process.stdout.partition(b"\n\n")
    if not separator:
        raise CommandError(
            "stale_identity", "commit", "Git returned an invalid commit object.", 3
        )
    return message.decode("utf-8")


def _verify_commit(
    repo: Path,
    commit: str,
    pre: str,
    expected_tree: str,
    message: str,
    hook_results: list[dict[str, object]],
) -> None:
    parents = git(repo, "show", "-s", "--format=%P", commit).stdout.strip().split()
    if parents != [pre]:
        raise _commit_failure(
            stage="pre_publication_validation",
            message="The transaction commit parent changed; reprepare and review the candidate.",
            pre_commit_head=pre,
            commit_sha=commit,
            hook_results=hook_results,
        )
    actual_tree = git(repo, "show", "-s", "--format=%T", commit).stdout.strip()
    actual_message = _raw_commit_message(repo, commit)
    if actual_tree != expected_tree or actual_message != message:
        raise _commit_failure(
            stage="pre_publication_validation",
            message="A commit hook changed the reviewed tree or message; reprepare and review the candidate.",
            pre_commit_head=pre,
            commit_sha=commit,
            hook_results=hook_results,
        )


def _registered_worktrees(repo: Path) -> set[Path]:
    process = git(repo, "worktree", "list", "--porcelain")
    return {
        Path(line.removeprefix("worktree ")).resolve()
        for line in process.stdout.splitlines()
        if line.startswith("worktree ")
    }


def _remove_transaction_worktree(repo: Path, transaction: Path) -> bool:
    removed = git(
        repo, "worktree", "remove", "--force", str(transaction), check=False
    ).returncode == 0
    git(repo, "worktree", "prune", check=False)
    return removed and transaction.resolve() not in _registered_worktrees(repo)


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--task")
    parser.add_argument("--candidate-artifact", required=True)
    args = parse(parser, argv)
    repo = root(package_root, args.root)
    candidate = load(repo, package_root, args.candidate_artifact, "candidate_artifact")
    exit_id = validate_candidate(package_root, repo, candidate)
    if exit_id != "committed":
        return {
            "status": "not_committed",
            "typed_exit": exit_id,
            "task_ref": candidate["task"]["path"],
        }

    pre = candidate["git"]["pre_commit_head"]
    branch = git(repo, "symbolic-ref", "HEAD").stdout.strip()
    exact = set(candidate["exact_stage_paths"])
    candidate_path = Path(args.candidate_artifact)
    candidate_path = candidate_path if candidate_path.is_absolute() else repo / candidate_path
    live_snapshot_excluded = {repo_rel(repo, candidate_path)}
    live_worktree_before = capture_snapshot(repo, live_snapshot_excluded)
    live_index_before = index_entries(repo)
    unrelated_index_before = index_entries(repo, exact)
    with temporary_directory("task_commit_input") as temporary:
        temp_root = Path(temporary)
        transaction = temp_root / "worktree"
        index_path = temp_root / "index"
        message_path = temp_root / "message"
        hooks_root = temp_root / "hooks"
        hook_log = temp_root / "hook-results"
        message_path.write_text(candidate["message"]["bytes"])
        message_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
        _install_hook_proxies(repo, hooks_root, hook_log)
        env = {
            "GIT_INDEX_FILE": str(index_path),
            "GIT_EDITOR": ":",
            "GIT_SEQUENCE_EDITOR": ":",
        }
        worktree_created = False
        created_commit = None
        live_ref_published = False
        results: list[dict[str, object]] = []
        try:
            git(repo, "worktree", "add", "--detach", "--no-checkout", str(transaction), pre)
            worktree_created = True
            expected_tree = _materialize_exact_index(repo, candidate, env)
            git(transaction, "checkout-index", "--all", "--force", env=env)
            if git(transaction, "write-tree", env=env).stdout.strip() != expected_tree:
                raise _commit_failure(
                    stage="pre_hook_validation",
                    message="The isolated candidate index changed before hooks ran.",
                    pre_commit_head=pre,
                    commit_sha=None,
                    hook_results=[],
                )

            commit_process = subprocess.run(
                [
                    "git",
                    "-c",
                    f"core.hooksPath={hooks_root}",
                    "commit",
                    "--cleanup=verbatim",
                    "-F",
                    str(message_path),
                ],
                cwd=transaction,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, **env},
            )
            results = _hook_results(hook_log)
            transaction_head = git(
                transaction, "rev-parse", "HEAD", check=False
            ).stdout.strip()
            created_commit = transaction_head if transaction_head and transaction_head != pre else None
            failed_hook = next((row for row in results if row["exit_code"] != 0), None)
            if commit_process.returncode or failed_hook:
                stage = "post_commit" if created_commit else "pre_commit"
                detail = (
                    f"Repository {failed_hook['name']} hook rejected the transaction."
                    if failed_hook
                    else commit_process.stderr.strip() or "Repository commit hooks rejected the transaction."
                )
                raise _commit_failure(
                    stage=stage,
                    message=detail,
                    pre_commit_head=pre,
                    commit_sha=created_commit,
                    hook_results=results,
                )
            if not created_commit:
                raise _commit_failure(
                    stage="commit_creation",
                    message="Git reported success without creating the reviewed transaction commit.",
                    pre_commit_head=pre,
                    commit_sha=None,
                    hook_results=results,
                )

            transaction_tree = git(transaction, "write-tree", env=env).stdout.strip()
            transaction_status = subprocess.run(
                ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
                cwd=transaction,
                env={**os.environ, **env},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if transaction_status.returncode or transaction_status.stdout or transaction_tree != expected_tree:
                raise _commit_failure(
                    stage="post_commit_validation",
                    message="A commit hook changed the reviewed transaction index or worktree.",
                    pre_commit_head=pre,
                    commit_sha=created_commit,
                    hook_results=results,
                )
            if message_path.read_text() != candidate["message"]["bytes"]:
                raise _commit_failure(
                    stage="pre_publication_validation",
                    message="A commit hook changed the reviewed message file.",
                    pre_commit_head=pre,
                    commit_sha=created_commit,
                    hook_results=results,
                )
            _verify_commit(
                repo,
                created_commit,
                pre,
                expected_tree,
                candidate["message"]["bytes"],
                results,
            )
            if (
                git(repo, "rev-parse", "HEAD").stdout.strip() != pre
                or index_entries(repo) != live_index_before
                or capture_snapshot(repo, live_snapshot_excluded) != live_worktree_before
            ):
                raise _commit_failure(
                    stage="pre_publication_validation",
                    message="The live branch, semantic index, or worktree changed before transaction publication.",
                    pre_commit_head=pre,
                    commit_sha=created_commit,
                    hook_results=results,
                )

            git(repo, "update-ref", branch, created_commit, pre)
            live_ref_published = True
            try:
                git(repo, "reset", "-q", created_commit, "--", *candidate["exact_stage_paths"])
            except CommandError as error:
                raise _commit_failure(
                    stage="live_ref_published",
                    message="The commit was published but the live index refresh failed; resume recovery for the created commit.",
                    pre_commit_head=pre,
                    commit_sha=created_commit,
                    hook_results=results,
                ) from error
        finally:
            index_path.unlink(missing_ok=True)
            if worktree_created and not _remove_transaction_worktree(repo, transaction):
                raise _commit_failure(
                    stage="live_ref_published" if live_ref_published else "transaction_cleanup",
                    message="The temporary commit worktree could not be removed; remove its stale worktree registration before retrying.",
                    pre_commit_head=pre,
                    commit_sha=created_commit,
                    hook_results=results,
                )

    if index_entries(repo, exact) != unrelated_index_before:
        raise _commit_failure(
            stage="live_ref_published",
            message="The commit was published but unrelated semantic index entries changed; resume recovery for the created commit.",
            pre_commit_head=pre,
            commit_sha=created_commit,
            hook_results=results,
        )
    if git(
        repo,
        "diff",
        "--cached",
        "--quiet",
        created_commit,
        "--",
        *candidate["exact_stage_paths"],
        check=False,
    ).returncode:
        raise _commit_failure(
            stage="live_ref_published",
            message="The commit was published but reviewed paths remain staged; resume recovery for the created commit.",
            pre_commit_head=pre,
            commit_sha=created_commit,
            hook_results=results,
        )
    if git(repo, "rev-parse", "HEAD").stdout.strip() != created_commit:
        raise _commit_failure(
            stage="live_ref_published",
            message="The commit was created but the live ref publication postcondition failed; resume recovery for the created commit.",
            pre_commit_head=pre,
            commit_sha=created_commit,
            hook_results=results,
        )

    candidate_path.unlink(missing_ok=True)
    phase2 = (
        repo
        / ".trellis/.runtime/guru-team/owner-checkpoints"
        / Path(candidate["task"]["path"]).name
        / "phase2-check.json"
    )
    phase2.unlink(missing_ok=True)
    return {
        "status": "committed",
        "exit": "committed",
        "pre_commit_head": pre,
        "commit_sha": created_commit,
    }
