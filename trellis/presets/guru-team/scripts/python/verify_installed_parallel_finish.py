#!/usr/bin/env python3
"""Verify task-local A/B Finish, merge-order, recovery and reachability facts.

This compatibility harness intentionally does not implement a public Acceptance
or cleanup owner.  It exercises two isolated normal-path task topologies with
the installed official Trellis task runtime.  The real GitHub ``github_pr``
route remains a separate externally confirmed gate.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Mapping, Sequence


class ParallelFinishError(RuntimeError):
    """The deterministic compatibility fixture failed."""


def run(
    argv: Sequence[str],
    cwd: Path,
    *,
    env: Mapping[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    process_env = os.environ.copy()
    process_env["PYTHONDONTWRITEBYTECODE"] = "1"
    if env:
        process_env.update(env)
    result = subprocess.run(
        list(argv), cwd=cwd, env=process_env, text=True, capture_output=True, check=False
    )
    if check and result.returncode != 0:
        raise ParallelFinishError(
            f"command failed ({result.returncode}): {' '.join(argv)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def git(root: Path, *args: str, check: bool = True) -> str:
    return run(("git", *args), root, check=check).stdout.strip()


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def configure_repo(root: Path) -> None:
    git(root, "config", "user.name", "Guru Team A/B Fixture")
    git(root, "config", "user.email", "guru-team-ab@example.invalid")


def initialize_developer(root: Path, name: str) -> None:
    run((sys.executable, ".trellis/scripts/init_developer.py", name), root)
    developer = root / ".trellis/.developer"
    workspace = root / ".trellis/workspace" / name
    if not developer.is_file() or not workspace.is_dir():
        raise ParallelFinishError("official developer initialization did not complete")
    for path in (developer, workspace / "journal-1.md", workspace / "index.md"):
        ignored = run(
            ("git", "check-ignore", "-q", path.relative_to(root).as_posix()),
            root,
            check=False,
        )
        if ignored.returncode != 0:
            raise ParallelFinishError(
                f"developer runtime path is not ignored: {path.relative_to(root)}"
            )


def bootstrap_installed_runtime(root: Path) -> dict[str, Any]:
    runtime = root / ".trellis/guru-team/runtime"
    bootstrap = runtime / "bootstrap.py"
    if not bootstrap.is_file():
        raise ParallelFinishError("installed runtime bootstrap is unavailable")
    payload = json.loads(
        run(
            (
                sys.executable,
                str(bootstrap),
                "--repo",
                str(root),
                "--runtime-assets",
                str(runtime),
                "--python",
                sys.executable,
                "--json",
            ),
            root,
        ).stdout
    )
    pointer = Path(git(root, "rev-parse", "--git-path", "guru-team/python/active.json"))
    if not pointer.is_absolute():
        pointer = root / pointer
    if payload.get("status") != "ok" or not pointer.is_file():
        raise ParallelFinishError("installed runtime bootstrap did not bind the clone")
    return payload


def load_closeout_helper() -> Any:
    path = Path(__file__).with_name("verify_installed_closeout.py")
    spec = importlib.util.spec_from_file_location("verify_installed_closeout", path)
    if spec is None or spec.loader is None:
        raise ParallelFinishError("cannot load installed closeout helper")
    module = importlib.util.module_from_spec(spec)
    script_root = str(path.parent)
    inserted = script_root not in sys.path
    if inserted:
        sys.path.insert(0, script_root)
    try:
        spec.loader.exec_module(module)
    finally:
        if inserted:
            sys.path.remove(script_root)
    return module


def copy_installed_repository(installed_repo: Path, target: Path) -> None:
    if not (installed_repo / ".trellis/guru-team/extension.json").is_file():
        raise ParallelFinishError("installed repository has no Guru Team manifest")
    installed_repo = installed_repo.resolve()

    def ignore(directory: str, names: list[str]) -> set[str]:
        relative = Path(directory).resolve().relative_to(installed_repo)
        ignored = {
            name
            for name in names
            if name == "__pycache__"
            or name.endswith((".pyc", ".pyo"))
            or name.startswith("installed-closeout-")
        }
        if relative == Path(".trellis"):
            ignored.update({".runtime", "tasks", "workspace"})
        return ignored

    for source in sorted(installed_repo.iterdir(), key=lambda item: item.name):
        relative = Path(source.name)
        if relative == Path(".git") or source.name.startswith("installed-closeout-"):
            continue
        destination = target / relative
        if source.is_dir():
            shutil.copytree(source, destination, ignore=ignore)
        else:
            shutil.copy2(source, destination)


@contextmanager
def temporary_environment(values: Mapping[str, str]):
    previous = {key: os.environ.get(key) for key in values}
    os.environ.update(values)
    try:
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def initialize_seed(installed_repo: Path, root: Path) -> tuple[Path, Path, str, bytes]:
    remote = root / "remote.git"
    seed = root / "seed"
    run(("git", "init", "--bare", "-q", str(remote)), root)
    run(("git", "init", "-q", str(seed)), root)
    configure_repo(seed)
    git(seed, "branch", "-M", "main")
    copy_installed_repository(installed_repo, seed)
    ignore_path = seed / ".gitignore"
    existing_ignore = ignore_path.read_text(encoding="utf-8") if ignore_path.is_file() else ""
    required_ignores = (
        ".trellis/.runtime/",
        ".trellis/workspace/",
        "__pycache__/",
        "*.py[cod]",
    )
    missing_ignores = [row for row in required_ignores if row not in existing_ignore.splitlines()]
    if existing_ignore and not existing_ignore.endswith("\n"):
        existing_ignore += "\n"
    ignore_path.write_text(
        existing_ignore + "".join(f"{row}\n" for row in missing_ignores),
        encoding="utf-8",
    )
    (seed / "README.md").write_text("# Parallel Finish fixture\n", encoding="utf-8")
    sibling = seed / ".trellis/tasks/08-19-sibling/task.json"
    sibling_payload = {
        "id": "sibling",
        "name": "sibling",
        "title": "Sibling fixture task",
        "status": "in_progress",
        "branch": "feat/sibling",
        "base_branch": "main",
        "creator": "fixture",
        "assignee": "fixture",
        "parent": None,
        "children": [],
    }
    write_json(sibling, sibling_payload)
    sibling_bytes = sibling.read_bytes()
    git(seed, "add", ".")
    git(seed, "commit", "-q", "-m", "chore: initialize parallel finish fixture")
    base = git(seed, "rev-parse", "HEAD")
    git(seed, "remote", "add", "origin", str(remote))
    git(seed, "push", "-q", "-u", "origin", "main")
    return remote, seed, base, sibling_bytes


def installed_owners(closeout: Any, root: Path) -> dict[str, Any]:
    return {
        skill_id: closeout.InstalledPackageClient(root, skill_id)
        for skill_id in (
            "guru-approve-task-plan",
            "guru-check-task",
            "guru-create-task-commit",
            "guru-review-branch",
            "guru-review-task-publication",
        )
    }


def fake_publication_environment(
    closeout: Any,
    root: Path,
    remote: Path,
    branch: str,
    issue: int,
    *,
    gh_sentinel: Path | None = None,
    gh_log: Path | None = None,
) -> dict[str, str]:
    real_git = shutil.which("git")
    if not real_git:
        raise ParallelFinishError("git not found")
    fake_bin = root / f"fake-publication-bin-{issue}"
    closeout.install_fake_commands(fake_bin)
    path_parts = [str(fake_bin)]
    if gh_sentinel is not None:
        path_parts.insert(0, str(gh_sentinel))
    values = {
        "PATH": os.pathsep.join([*path_parts, os.environ.get("PATH", "")]),
        "INSTALLED_CLOSEOUT_REAL_GIT": real_git,
        "INSTALLED_CLOSEOUT_REMOTE": str(remote),
        "INSTALLED_CLOSEOUT_BRANCH": branch,
        "INSTALLED_CLOSEOUT_PR_NUMBER": str(issue),
        "INSTALLED_CLOSEOUT_PR_STORE": str(root / f"publication-pr-{issue}.json"),
        "INSTALLED_CLOSEOUT_MUTATION_STORE": str(
            root / f"publication-mutations-{issue}.txt"
        ),
    }
    if gh_log is not None:
        values["GURU_GH_CALL_LOG"] = str(gh_log)
    return values


def run_phase0(installed_repo: Path, work_root: Path, checkpoint: str) -> dict[str, Any]:
    helper = Path(__file__).with_name("verify_installed_phase0_transcript.py")
    grading = Path(__file__).resolve().parents[2] / "tests/semantic-retrieval-grading.json"
    runtime = installed_repo / ".trellis/guru-team/runtime"
    resolver = runtime / "resolve-python.sh"
    payload = json.loads(
        run(
            (
                str(resolver),
                str(installed_repo),
                str(runtime),
                str(helper),
                "--installed-repo",
                str(installed_repo),
                "--work-root",
                str(work_root),
                "--checkpoint",
                checkpoint,
                "--semantic-grading",
                str(grading),
            ),
            installed_repo,
        ).stdout
    )
    if (
        payload.get("status") != "ok"
        or len(payload.get("six_step_transcript", [])) != 6
        or payload.get("workspace", {}).get("actual_exit") != "created"
    ):
        raise ParallelFinishError(f"{checkpoint} Phase 0 transcript did not pass")
    return {
        "status": "passed",
        "step_count": 6,
        "workspace_exit": "created",
        "exit_family_count": payload.get("exit_family_count"),
    }


def run_installed_lifecycle(
    closeout: Any,
    root: Path,
    remote: Path,
    case_name: str,
    issue: int,
    *,
    gh_sentinel: Path | None = None,
    gh_log: Path | None = None,
) -> tuple[Path, str, str]:
    real_git = shutil.which("git")
    if not real_git:
        raise ParallelFinishError("git not found")
    branch = f"fix/{issue}-installed-closeout-{case_name}"
    environment = fake_publication_environment(
        closeout,
        root,
        remote,
        branch,
        issue,
        gh_sentinel=gh_sentinel,
        gh_log=gh_log,
    )
    with temporary_environment(environment):
        task, actual_branch, review_commit = closeout.write_fixture(
            root,
            installed_owners(closeout, root),
            real_git,
            case_name,
            issue,
            repo_ref=closeout.REPO,
        )
    if actual_branch != branch:
        raise ParallelFinishError("installed lifecycle returned an unexpected branch")
    return task, branch, review_commit


def task_payload(token: str, branch: str) -> dict[str, Any]:
    return {
        "id": f"parallel-{token}",
        "name": f"parallel-{token}",
        "title": f"Parallel Finish {token.upper()}",
        "status": "completed",
        "branch": branch,
        "base_branch": "main",
        "creator": "fixture",
        "assignee": "fixture",
        "scope": f"Compatibility fixture {token.upper()}",
        "parent": None,
        "children": [],
    }


def create_task_work(root: Path, token: str, branch: str) -> tuple[Path, str]:
    task = root / f".trellis/tasks/08-19-parallel-{token}"
    write_json(task / "task.json", task_payload(token, branch))
    (task / "prd.md").write_text(
        f"# Parallel Finish {token.upper()}\n\nTask-local compatibility fixture.\n",
        encoding="utf-8",
    )
    business = root / "business" / f"{token}.txt"
    business.parent.mkdir(parents=True, exist_ok=True)
    business.write_text(f"parallel task {token}\n", encoding="utf-8")
    git(root, "add", task.relative_to(root).as_posix(), business.relative_to(root).as_posix())
    git(root, "commit", "-q", "-m", f"feat: implement parallel task {token}")
    return task, git(root, "rev-parse", "HEAD")


def archive_task(
    root: Path,
    task: Path,
    token: str,
    sibling_bytes: bytes,
    *,
    fail_before_archive: bool = False,
) -> tuple[Path, str]:
    if fail_before_archive:
        if not task.is_dir():
            raise ParallelFinishError("failure injection lost the active task")
        raise ParallelFinishError(f"finish_before_archive:{token}")
    task_relative = task.relative_to(root).as_posix()
    run(
        (sys.executable, ".trellis/scripts/task.py", "archive", task_relative, "--no-commit"),
        root,
    )
    matches = sorted((root / ".trellis/tasks/archive").glob(f"*/*parallel-{token}"))
    if len(matches) != 1 or task.exists():
        raise ParallelFinishError(f"archive did not move only task {token}")
    sibling = root / ".trellis/tasks/08-19-sibling/task.json"
    if sibling.read_bytes() != sibling_bytes:
        raise ParallelFinishError(f"Finish {token} changed sibling task bytes")
    archived = matches[0]
    archived_payload = json.loads((archived / "task.json").read_text(encoding="utf-8"))
    if archived_payload.get("parent") is not None or archived_payload.get("children") != []:
        raise ParallelFinishError(f"Finish {token} changed parent/child identity")
    git(root, "add", "-A", ".trellis/tasks")
    git(root, "commit", "-q", "-m", f"chore(task): archive parallel {token}")
    return archived, git(root, "rev-parse", "HEAD")


def finish_none(
    root: Path,
    task: Path,
    branch: str,
    review_commit: str,
    sibling_bytes: bytes,
    *,
    fail_before_archive: bool = False,
) -> tuple[Path, str, list[str]]:
    if fail_before_archive:
        if not task.is_dir():
            raise ParallelFinishError("failure injection lost the active task")
        raise ParallelFinishError("finish_before_archive:b")
    task_relative = task.relative_to(root).as_posix()
    run(
        (sys.executable, ".trellis/scripts/task.py", "archive", task_relative, "--no-commit"),
        root,
    )
    matches = sorted((root / ".trellis/tasks/archive").glob(f"*/{task.name}"))
    if len(matches) != 1 or task.exists():
        raise ParallelFinishError("B none Finish did not move only its task")
    archived = matches[0]
    run(
        (
            sys.executable,
            ".trellis/scripts/add_session.py",
            "--title",
            "Parallel Finish B",
            "--commit",
            review_commit,
            "--summary",
            "Installed current/none compatibility lifecycle completed.",
            "--branch",
            branch,
            "--change",
            "Archived only the B task-local path.",
            "--test",
            "Planning, Phase 2, Branch Review and publication review passed.",
            "--next-step",
            "No GitHub PR route is allowed for B.",
            "--no-commit",
        ),
        root,
    )
    sibling = root / ".trellis/tasks/08-19-sibling/task.json"
    if sibling.read_bytes() != sibling_bytes:
        raise ParallelFinishError("B none Finish changed sibling task bytes")
    archived_payload = json.loads((archived / "task.json").read_text(encoding="utf-8"))
    if archived_payload.get("parent") not in (None, "") or archived_payload.get(
        "children", []
    ) != []:
        raise ParallelFinishError("B none Finish changed parent/child identity")
    workspace_files = sorted(
        path
        for path in (root / ".trellis/workspace").rglob("*")
        if path.is_file()
    )
    if not workspace_files:
        raise ParallelFinishError("B upstream Finish did not run add_session.py")
    if not any(
        "Parallel Finish B" in path.read_text(encoding="utf-8")
        for path in workspace_files
        if path.name.startswith("journal-")
    ):
        raise ParallelFinishError("B upstream Finish did not append its session journal")
    for path in workspace_files:
        ignored = run(
            ("git", "check-ignore", "-q", path.relative_to(root).as_posix()),
            root,
            check=False,
        )
        if ignored.returncode != 0:
            raise ParallelFinishError("B workspace journal is not ignored")
    tracked_status = git(root, "status", "--short")
    if ".trellis/workspace/" in tracked_status:
        raise ParallelFinishError("B none Finish added workspace journal to tracked diff")
    git(root, "add", "-A", ".trellis/tasks")
    git(root, "commit", "-q", "-m", "chore(task): archive parallel b")
    return (
        archived,
        git(root, "rev-parse", "HEAD"),
        [path.relative_to(root).as_posix() for path in workspace_files],
    )


def make_gh_sentinel(root: Path) -> tuple[Path, Path]:
    bin_dir = root / "sentinel-bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    calls = root / "gh-calls.log"
    script = bin_dir / "gh"
    script.write_text(
        "#!/bin/sh\nprintf '%s\\n' \"$*\" >> \"$GURU_GH_CALL_LOG\"\nexit 91\n",
        encoding="utf-8",
    )
    script.chmod(script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return calls, bin_dir


def branch_metadata_paths(root: Path, branch: str) -> list[str]:
    output = git(root, "diff", "--name-only", f"origin/main...origin/{branch}")
    return sorted(path for path in output.splitlines() if path.startswith(".trellis/"))


def merge_order(
    remote: Path,
    root: Path,
    order: tuple[str, str],
    branches: Mapping[str, str],
) -> dict[str, Any]:
    clone = root / f"merge-{order[0]}-then-{order[1]}"
    run(("git", "clone", "-q", str(remote), str(clone)), root)
    configure_repo(clone)
    retained = f"matrix/{order[0]}-then-{order[1]}"
    git(clone, "checkout", "-q", "-b", retained, "origin/main")
    for token in order:
        result = run(
            ("git", "merge", "--no-ff", "--no-edit", f"origin/{branches[token]}"),
            clone,
            check=False,
        )
        if result.returncode != 0:
            raise ParallelFinishError(
                f"merge order {order} conflicted on {token}: {result.stdout}{result.stderr}"
            )
    head = git(clone, "rev-parse", "HEAD")
    git(clone, "push", "-q", "-u", "origin", retained)
    return {"order": list(order), "retained_ref": retained, "head": head}


def assert_reachable(root: Path, commits: Sequence[str], refs: Sequence[str]) -> None:
    for commit in commits:
        if not any(
            run(("git", "merge-base", "--is-ancestor", commit, ref), root, check=False).returncode
            == 0
            for ref in refs
        ):
            raise ParallelFinishError(f"protected commit is unreachable: {commit}")


def verify_archived_history(
    root: Path,
    archived_task: Path,
    *,
    pr_number: int,
) -> dict[str, Any]:
    preview = (
        root
        / ".trellis/guru-team/skills/packages/guru-discover-change-context/scripts/preview-change-context-history.sh"
    )
    payload = json.loads(
        run(
            (
                str(preview),
                "--root",
                str(root),
                "--json",
                "--query-json",
                json.dumps({"pr_refs": [f"PR #{pr_number}"]}, sort_keys=True),
            ),
            root,
        ).stdout
    )
    expected = (archived_task / "finish-summary.json").relative_to(root).as_posix()
    candidates = payload.get("candidates")
    invalid = payload.get("invalid")
    if invalid != [] or not isinstance(candidates, list) or len(candidates) != 1:
        raise ParallelFinishError("archived history preview was not uniquely discoverable")
    candidate = candidates[0]
    matched = candidate.get("matched_clues")
    score = candidate.get("score")
    if (
        candidate.get("finish_summary_path") != expected
        or not isinstance(matched, dict)
        or matched.get("pr_refs") != [f"PR #{pr_number}"]
        or not isinstance(score, dict)
        or not isinstance(score.get("total"), int)
        or score["total"] <= 0
    ):
        raise ParallelFinishError("archived history preview selected the wrong Finish summary")
    return {
        "status": "passed",
        "candidate_count": 1,
        "finish_summary_path": expected,
        "matched_pr_ref": f"PR #{pr_number}",
    }


def run_fixture(installed_repo: Path, work_root: Path) -> dict[str, Any]:
    installed_repo = installed_repo.resolve()
    work_root = work_root.resolve()
    if work_root.exists() and any(work_root.iterdir()):
        raise ParallelFinishError(f"work root must be empty: {work_root}")
    work_root.mkdir(parents=True, exist_ok=True)
    closeout = load_closeout_helper()
    remote, seed, base, sibling_bytes = initialize_seed(installed_repo, work_root)

    a_control = work_root / "a-control"
    run(("git", "clone", "-q", str(remote), str(a_control)), work_root)
    configure_repo(a_control)
    a_worktree = work_root / "a-worktree"
    git(a_control, "worktree", "add", "-q", "--detach", str(a_worktree), "origin/main")
    configure_repo(a_worktree)
    initialize_developer(a_worktree, "parallel-a")
    bootstrap_installed_runtime(a_worktree)
    phase0_a = run_phase0(a_worktree, work_root / "phase0-a", "parallel-a")
    a_task, a_branch, a_work = run_installed_lifecycle(
        closeout,
        a_worktree,
        remote,
        "parallel-a",
        301,
    )
    a_closeout = closeout.run_closeout(
        a_worktree,
        a_task,
        a_branch,
        301,
        a_work,
        shutil.which("git") or "git",
        remote,
        terminal_recovery_only=True,
        provider_failure_once=True,
    )
    a_archive = Path(a_closeout["archived_task_dir"])
    a_finish = str(a_closeout["local_head"])
    sibling_a = a_worktree / ".trellis/tasks/08-19-sibling/task.json"
    if sibling_a.read_bytes() != sibling_bytes:
        raise ParallelFinishError("A github_pr Finish changed sibling task bytes")

    b_current = work_root / "b-current"
    run(("git", "clone", "-q", str(remote), str(b_current)), work_root)
    configure_repo(b_current)
    initialize_developer(b_current, "parallel-b")
    bootstrap_installed_runtime(b_current)
    phase0_b = run_phase0(b_current, work_root / "phase0-b", "parallel-b")
    gh_calls, gh_sentinel = make_gh_sentinel(work_root / "b-provider")
    b_task, b_branch, b_work = run_installed_lifecycle(
        closeout,
        b_current,
        remote,
        "parallel-b",
        302,
        gh_sentinel=gh_sentinel,
        gh_log=gh_calls,
    )
    injected = False
    try:
        finish_none(
            b_current,
            b_task,
            b_branch,
            b_work,
            sibling_bytes,
            fail_before_archive=True,
        )
    except ParallelFinishError as exc:
        if str(exc) != "finish_before_archive:b" or not b_task.is_dir():
            raise
        injected = True
    if not injected:
        raise ParallelFinishError("B Finish failure injection did not execute")
    with temporary_environment(
        {
            "PATH": f"{gh_sentinel}{os.pathsep}{os.environ.get('PATH', '')}",
            "GURU_GH_CALL_LOG": str(gh_calls),
        }
    ):
        b_archive, b_finish, b_workspace_files = finish_none(
            b_current,
            b_task,
            b_branch,
            b_work,
            sibling_bytes,
        )
    if gh_calls.exists() and gh_calls.read_text(encoding="utf-8").strip():
        raise ParallelFinishError("B none route read or created a GitHub PR")
    git(b_current, "push", "-q", "-u", "origin", b_branch)

    git(seed, "fetch", "-q", "origin")
    metadata_a = branch_metadata_paths(seed, a_branch)
    metadata_b = branch_metadata_paths(seed, b_branch)
    intersection = sorted(set(metadata_a) & set(metadata_b))
    if intersection:
        raise ParallelFinishError(f"A/B tracked metadata intersects: {intersection}")
    forbidden_prefixes = (".trellis/workspace/", ".trellis/.runtime/")
    forbidden_exact = {".trellis/tasks/index.md", ".trellis/workspace/index.md"}
    if any(
        path.startswith(forbidden_prefixes)
        or path in forbidden_exact
        or "handoff" in path.lower()
        for path in metadata_a + metadata_b
    ):
        raise ParallelFinishError("A/B tracked diff contains shared workspace/runtime state")

    branches = {"a": a_branch, "b": b_branch}
    orders = [
        merge_order(remote, work_root, ("a", "b"), branches),
        merge_order(remote, work_root, ("b", "a"), branches),
    ]
    retained_refs = [f"origin/{row['retained_ref']}" for row in orders]
    git(seed, "fetch", "-q", "origin")
    protected = [a_work, a_finish, b_work, b_finish]
    assert_reachable(seed, protected, retained_refs)
    archived_history = verify_archived_history(
        a_worktree,
        a_archive,
        pr_number=301,
    )

    failed_delete = run(
        ("git", "branch", "-D", b_branch), b_current, check=False
    )
    if failed_delete.returncode == 0:
        raise ParallelFinishError("cleanup failure injection unexpectedly deleted checked-out B branch")
    git(b_current, "checkout", "-q", "--detach", "origin/main")
    git(b_current, "branch", "-D", b_branch)
    git(a_control, "worktree", "remove", "--force", str(a_worktree))
    git(a_control, "branch", "-D", a_branch)
    git(seed, "push", "-q", "origin", "--delete", a_branch, b_branch)
    git(seed, "fetch", "-q", "--prune", "origin")
    assert_reachable(seed, protected, retained_refs)

    result = {
        "schema_version": "1.0",
        "status": "passed",
        "base_commit": base,
        "a": {
            "workspace_mode": "worktree",
            "finish_entry": "github_pr",
            "phase0": phase0_a,
            "planning": "passed",
            "phase2_check": "passed",
            "branch_review": "passed",
            "publication_review": "passed",
            "acceptance": "fixture_local_passed",
            "work_commit": a_work,
            "finish_commit": a_finish,
            "archive_locator": a_archive.relative_to(a_worktree).as_posix(),
            "history_discovery": archived_history,
            "provider_failure_recovered": a_closeout[
                "provider_failure_recovered"
            ],
            "local_pr_url": a_closeout["pr_url"],
            "real_github_verified": False,
        },
        "b": {
            "workspace_mode": "current",
            "finish_entry": "none",
            "phase0": phase0_b,
            "planning": "passed",
            "phase2_check": "passed",
            "branch_review": "passed",
            "publication_review": "passed",
            "acceptance": "fixture_local_passed",
            "work_commit": b_work,
            "finish_commit": b_finish,
            "archive_locator": b_archive.relative_to(b_current).as_posix(),
            "github_pr_call_count": 0,
            "finish_recovery": "same_task_remaining_action",
            "workspace_journal_files": b_workspace_files,
            "workspace_journal_tracked": False,
        },
        "metadata_intersection": intersection,
        "merge_orders": orders,
        "cleanup_failure_recovered": True,
        "protected_commits_reachable_after_cleanup": True,
        "external_boundary": "A requires a separately confirmed dedicated disposable GitHub repository",
    }
    (work_root / "parallel-finish-summary.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--installed-repo", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = run_fixture(args.installed_repo, args.work_root)
    except (ParallelFinishError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
