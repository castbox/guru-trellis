"""Call-local execution facts; no selection, formal write or review judgment."""
from __future__ import annotations

import argparse
import errno
import os
import stat
import tempfile
from pathlib import Path

from common import checkpoint, dirty_paths, rel, root, task
from runtime.delivery_projection.adapter import DeliveryProjection, official_session_port
from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.session_adapter import session_read_reason


def _failure(operation: str, location: str, exc: Exception) -> dict:
    # Wrapped public readers may retain an OS cause. Never infer a lost errno.
    cause = exc
    while cause.__cause__ is not None:
        cause = cause.__cause__
    failure = {"operation": operation, "location": location, "status": "failed",
               "exception_class": type(cause).__name__,
               "errno": cause.errno if isinstance(cause, OSError) else None}
    if isinstance(exc, LifecycleContractError):
        failure.update(reason_code=exc.code, field_path=exc.field_path)
    return failure


def _observe(checks: list[dict], operation: str, location: str, action):
    try:
        value = action()
    except (OSError, ValueError, RuntimeError) as exc:
        checks.append(_failure(operation, location, exc))
        return False, None
    checks.append({"operation": operation, "location": location, "status": "available"})
    return True, value


def probe_directory(directory: Path, boundary: Path, location: str) -> list[dict]:
    """Exercise same-directory writes and remove only this call's temporary items."""
    checks: list[dict] = []
    created: list[Path] = []
    temporary: Path | None = None
    operation = "inspect_write_directory"
    try:
        current = boundary
        parts = directory.relative_to(boundary).parts
        for index in range(len(parts) + 1):
            if index:
                current = current / parts[index - 1]
            operation = "inspect_write_directory"
            try:
                metadata = current.lstat()
            except FileNotFoundError:
                operation = "create_write_directory"
                current.mkdir()
                created.append(current)
                metadata = current.lstat()
            if not stat.S_ISDIR(metadata.st_mode):
                raise NotADirectoryError(errno.ENOTDIR, "Probe requires a regular directory")
        operation = "create_temporary_file"
        descriptor, name = tempfile.mkstemp(prefix=".guru-review-execution-", dir=directory)
        temporary = Path(name)
        operation = "write_temporary_file"
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(b"Guru review execution probe\n")
        operation = "rename_temporary_file"
        renamed = temporary.with_name(temporary.name + ".renamed")
        temporary.rename(renamed)
        temporary = renamed
        operation = "delete_temporary_file"
        temporary.unlink()
        temporary = None
        checks.append({"operation": "probe_directory_write", "location": location,
                       "status": "available"})
    except (OSError, ValueError) as exc:
        checks.append(_failure(operation, location, exc))
    finally:
        if temporary is not None:
            try:
                temporary.unlink()
            except OSError as exc:
                checks.append(_failure("cleanup_temporary_file", location, exc))
        for path in reversed(created):
            try:
                path.rmdir()
            except OSError as exc:
                checks.append(_failure("cleanup_write_directory", location, exc))
    return checks


def _selection_write_needed(projection: DeliveryProjection, key: dict) -> bool:
    # Use the original read-only preflight. Missing binding/selection is not
    # repaired here, including when final_plan runs with a context key.
    try:
        return projection.selection_preflight(key)
    except LifecycleContractError as exc:
        detail = exc.code
        if exc.code == "stale_binding":
            reason = session_read_reason(exc.remediation)
            if reason:
                detail += f" ({reason})"
        raise CommandError("stale_identity", "session",
                           f"Resolve the existing session through its original owner: {detail}", 3) from exc


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--delivery-key", required=True)
    parser.add_argument("--purpose", choices=("planning", "branch_review"), required=True)
    parser.add_argument("--planning-purpose", choices=("candidate_assessment", "final_plan"))
    parser.add_argument("--base-ref")
    parser.add_argument("--head-ref")
    parser.add_argument("--probe-writes", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the declared execution query arguments.") from exc
    if args.purpose == "planning":
        if args.planning_purpose is None or args.base_ref is not None or args.head_ref is not None:
            raise CommandError("invalid_arguments", "arguments", "Planning requires --planning-purpose and observes HEAD; omit --base-ref and --head-ref.")
    elif args.planning_purpose is not None or not args.base_ref or not args.head_ref:
        raise CommandError("invalid_arguments", "arguments", "Branch Review requires --base-ref and --head-ref; omit --planning-purpose.")
    repo = root(package_root, args.root)
    task_dir = task(repo, args.task)
    key = read_json(args.delivery_key, "delivery_key")
    checks: list[dict] = []
    projection = DeliveryProjection(repo, rel(repo, task_dir))
    task_location = "<checkout>/" + rel(repo, task_dir) + "/task.json"
    ok, delivery = _observe(checks, "read_task_delivery", task_location,
                            lambda: projection.resolve(key))
    if ok:
        # Reuse the same explicit-object checks as the final-plan owner. This
        # validates Task/C4/checkout/profile without selecting or binding.
        ok, _ = _observe(checks, "read_explicit_checkout", "<checkout>",
                         lambda: projection._explicit_current(key))
    planning_purpose = args.purpose == "planning"
    if ok:
        phases = {"planning"} if planning_purpose else {"checking", "reviewing"}

        def check_phase():
            if delivery["phase"] not in phases:
                raise LifecycleContractError("stale_delivery_phase", "delivery.phase",
                                             "Resume the original owner for the current phase.")

        ok, _ = _observe(checks, "match_delivery_phase", task_location, check_phase)
    refs = (("HEAD", "<checkout>/HEAD"),) if planning_purpose else (
        (args.base_ref, "<git-object>/base"), (args.head_ref, "<git-object>/head"),
        ("HEAD", "<checkout>/HEAD"))
    commits = {}
    for ref, location in refs:
        readable, commit = _observe(checks, "read_commit", location, lambda ref=ref: projection.commit(ref))
        if readable:
            commits[location] = commit
    ok = ok and len(commits) == len(refs)
    if ok and not planning_purpose:
        candidate = delivery["candidate"]

        def match_commit(location, expected):
            if commits[location] != expected:
                raise LifecycleContractError("stale_review_candidate", "candidate",
                                             "Use the Delivery's fixed candidate and current checkout.")

        for location, field in (("<git-object>/base", "base_ref"), ("<git-object>/head", "head_ref"),
                                ("<checkout>/HEAD", "head_ref")):
            matched, _ = _observe(checks, "match_review_candidate", location,
                                  lambda location=location, field=field: match_commit(
                                      location, candidate[field] if candidate and candidate["kind"] == "git" else None))
            ok = ok and matched
    if ok and not planning_purpose:
        def require_clean_checkout():
            if dirty_paths(repo, projection.task_ref):
                raise LifecycleContractError("dirty_checkout", "worktree",
                                             "Use a clean committed review candidate.")

        ok, _ = _observe(checks, "match_clean_checkout", "<checkout>", require_clean_checkout)
    session_write_needed = False
    if ok and projection.has_context():
        session_write_needed = _selection_write_needed(projection, key)
        checks.append({"operation": "read_session_selection", "location": "<git-common-dir>/trellis/sessions",
                       "status": "available"})
    if ok:
        planning = projection.planning_directory(key)
        if args.purpose == "branch_review":
            objects = ("prd.md", "design.md", "implement.md")
        elif args.planning_purpose == "final_plan":
            objects = ("design.md",)
        else:
            # The first candidate may exist only as call-local design_facts.
            # Future Author design/implementation bodies are not prerequisites.
            objects = ("prd.md",)
        for name in objects:
            # Read capability only; never inject the planning narrative.
            def read_first_byte(path=planning / name):
                with path.open("rb") as stream:
                    stream.read(1)
            _observe(checks, "read_planning_object", "<checkout>/" + rel(repo, planning / name), read_first_byte)
        final_plan = args.purpose == "planning" and args.planning_purpose == "final_plan"
        if not final_plan:
            targets = []
            if session_write_needed:
                official = official_session_port(repo)
                facts = official.repository_facts(repo)
                # A fixed non-session filename obtains the official directory;
                # no actual context key is placed in output or written.
                sessions = official.session_path(repo, "execution-facts", facts).parent
                targets.append((sessions, facts.common_dir or repo, "<git-common-dir>/trellis/sessions"))
            if args.purpose == "branch_review":
                target = checkpoint(repo, task_dir, key).parent
                targets.extend(((task_dir, repo, "<checkout>/" + rel(repo, task_dir)),
                                (target, repo, "<checkout>/" + rel(repo, target))))
            for directory, boundary, location in targets:
                if args.probe_writes:
                    checks.extend(probe_directory(directory, boundary, location))
                else:
                    checks.append({"operation": "probe_directory_write", "location": location, "status": "not_probed"})
            if args.purpose == "branch_review":
                location = "<temporary-directory>"
                if args.probe_writes:
                    available, temp_dir = _observe(checks, "resolve_temporary_directory", location, tempfile.gettempdir)
                    if available:
                        directory = Path(temp_dir).resolve()
                        checks.extend(probe_directory(directory, directory, location))
                else:
                    checks.append({"operation": "probe_directory_write", "location": location, "status": "not_probed"})
    output = {"checks": checks}
    validate_json(output, package_root / "schemas/execution-facts-output-1.0.schema.json", "stdout")
    return output
