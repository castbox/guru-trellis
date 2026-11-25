"""Call-local execution facts; no selection, formal write or review judgment."""
from __future__ import annotations

import argparse
import errno
import os
import stat
import tempfile
from pathlib import Path

from common import checkpoint, rel, root, task
from runtime.delivery_projection.adapter import DeliveryProjection, official_session_port
from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from runtime.task_lifecycle.errors import LifecycleContractError


def _failure(operation: str, location: str, exc: Exception) -> dict:
    # Wrapped public readers may retain an OS cause. Never infer a lost errno.
    cause = exc
    while cause.__cause__ is not None:
        cause = cause.__cause__
    return {"operation": operation, "location": location, "status": "failed",
            "exception_class": type(cause).__name__,
            "errno": cause.errno if isinstance(cause, OSError) else None}


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


def _selection_facts(projection: DeliveryProjection, key: dict) -> None:
    # Use the original read-only preflight. Missing binding/selection is not
    # repaired here, including when final_plan runs with a context key.
    try:
        projection.selection_preflight(key)
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", "session",
                           "Resolve the existing session through its original owner: " + exc.code,
                           3) from exc


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
    ok, _ = _observe(checks, "read_task_delivery", task_location,
                            lambda: projection.resolve(key))
    if ok:
        # Reuse the same explicit-object checks as the final-plan owner. This
        # validates Task/C4/checkout/profile without selecting or binding.
        ok, _ = _observe(checks, "read_explicit_checkout", "<checkout>",
                         lambda: projection._explicit_current(key))
    if ok:
        _selection_facts(projection, key)
        checks.append({"operation": "read_session_selection", "location": "<git-common-dir>/trellis/sessions",
                       "status": "available"})
    refs = (("HEAD", "<checkout>/HEAD"),) if args.purpose == "planning" else (
        (args.base_ref, "<git-object>/base"), (args.head_ref, "<git-object>/head"))
    for ref, location in refs:
        _observe(checks, "read_commit", location, lambda ref=ref: projection.commit(ref))
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
            if projection.has_context():
                official = official_session_port(repo)
                facts = official.repository_facts(repo)
                # A fixed non-session filename obtains the official directory;
                # no actual context key is placed in output or written.
                sessions = official.session_path(repo, "execution-facts", facts).parent
                targets.append((sessions, facts.common_dir or repo, "<git-common-dir>/trellis/sessions"))
            if args.purpose == "branch_review":
                target = checkpoint(repo, task_dir, key).parent
                targets.extend(((task_dir, repo, "<checkout>/" + rel(repo, task_dir)),
                                (target, repo, "<checkout>/" + rel(repo, target)),
                                (Path(tempfile.gettempdir()).resolve(), Path(tempfile.gettempdir()).resolve(), "<temporary-directory>")))
            for directory, boundary, location in targets:
                if args.probe_writes:
                    checks.extend(probe_directory(directory, boundary, location))
                else:
                    checks.append({"operation": "probe_directory_write", "location": location, "status": "not_probed"})
    output = {"checks": checks}
    validate_json(output, package_root / "schemas/execution-facts-output-1.0.schema.json", "stdout")
    return output
