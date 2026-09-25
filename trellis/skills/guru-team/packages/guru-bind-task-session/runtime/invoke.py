from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.checkout_resolution import CheckoutRequest, validate_candidate
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import discover_worktree_facts, inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.schema import validate_dto
from runtime.task_lifecycle.session_adapter import bind_session, resolve_session


PROFILE_ROUTES = {
    "resume_current_task": "resume",
    "rebind_missing_session": "rebind",
    "switch_task": "switch",
    "reactivate_rebind": "reactivate",
    "manual_recovery": "manual_recovery",
}
EXITS = {
    "resume": "session_resumed",
    "rebind": "session_rebound",
    "switch": "task_switched",
    "reactivate": "reactivate_rebound",
    "manual_recovery": "session_manually_recovered",
}


def official_port(root: Path) -> Any:
    """Load the installed Fixed Fork API, never an alternate session store."""
    init = root / ".trellis/scripts/common/__init__.py"
    if not init.is_file():
        raise CommandError("stale_identity", "official_session", "Install the Fixed Fork schema-2 session API.", 3)
    spec = importlib.util.spec_from_file_location(
        "guru_bind_target_common", init, submodule_search_locations=[str(init.parent)]
    )
    if spec is None or spec.loader is None:
        raise CommandError("stale_identity", "official_session", "Load the Fixed Fork session API.", 3)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    store = module.session_storage
    required = (
        "repository_facts", "session_path", "record_exists", "read_record",
        "write_record", "resolve_task_identity",
    )
    if not all(callable(getattr(store, name, None)) for name in required):
        raise CommandError("stale_identity", "official_session", "Install the Fixed Fork schema-2 session API.", 3)
    return SimpleNamespace(resolve_context_key=module.resolve_context_key, **{
        name: getattr(store, name) for name in required
    })


def _blocked(package: Path, code: str, ref: str) -> dict[str, Any]:
    output = {"exit_id": "binding_blocked", "reason_code": code, "reason_refs": [ref]}
    validate_json(output, package / "schemas/public-blocked-output.schema.json", "stdout")
    return output


def _record(official: Any, root: Path) -> tuple[str, Any | None]:
    try:
        key = official.resolve_context_key()
    except (OSError, RuntimeError, ValueError):
        key = None
    if not isinstance(key, str) or not key:
        return "explicit_task_mode", None
    facts = official.repository_facts(root)
    path = official.session_path(root, key, facts)
    if not official.record_exists(path):
        return "missing", None
    record = official.read_record(path, root, facts)
    if record.data != {
        "schema_version": 2,
        "task_id": record.task_id,
        "lifecycle_generation": record.lifecycle_generation,
    }:
        raise ValueError("invalid_session_record")
    return "present", record


def _current_lifecycle(root: Path, lifecycle: dict[str, Any], resolved: Any) -> None:
    key = TaskLifecycleKey(lifecycle["task_id"], lifecycle["lifecycle_generation"])
    repository = inspect_repository(root)
    binding = BranchBindingStore(repository).read(key)
    ownership = ResourceLedgerStore(repository).read_current(key)
    if binding is None or ownership is None or (
        binding.binding_epoch, binding.binding_revision, binding.branch_name
    ) != (ownership.binding_epoch, ownership.binding_revision, ownership.branch_name):
        raise LifecycleContractError(
            "session_branch_unresolved", "branch_binding",
            "Resolve one current branch binding and matching resource ownership before session binding.",
        )
    task_ref = getattr(resolved, "task_ref", None)
    workspace = getattr(resolved, "workspace", None)
    task_path = getattr(resolved, "task_path", None)
    if not isinstance(task_ref, str) or not isinstance(workspace, Path) or not isinstance(task_path, Path):
        raise LifecycleContractError(
            "session_task_resolution_invalid", "official_session.resolve_task_identity",
            "Resolve the exact task artifact and workspace through the Fixed Fork resolver.",
        )
    try:
        status = json.loads((task_path / "task.json").read_text(encoding="utf-8"))["status"]
    except (OSError, ValueError, KeyError) as exc:
        raise LifecycleContractError(
            "session_task_resolution_invalid", "task.status", "Read the current task status.",
        ) from exc
    if not isinstance(status, str) or status not in {"planning", "in_progress"}:
        raise LifecycleContractError(
            "session_task_status_invalid", "task.status", "Bind an active task lifecycle.",
        )
    request = CheckoutRequest(repository, key.task_id, task_ref, key.lifecycle_generation,
                              binding.branch_ref, status)
    candidates = tuple(validate_candidate(request, row) for row in discover_worktree_facts(repository))
    # Dirty work is valid for resumption; all identity/artifact failures remain conflicts.
    if any(row.status == "authority_conflict" for row in candidates):
        raise LifecycleContractError(
            "session_checkout_conflict", "checkout", "Resolve conflicting live checkout facts first.",
        )
    valid = [row for row in candidates if row.valid or row.reason_code == "dirty_checkout"]
    if len(valid) != 1 or valid[0].facts.path != workspace.resolve():
        raise LifecycleContractError(
            "session_checkout_unresolved", "checkout", "Resolve one current checkout for this task lifecycle.",
        )


def execute(root: Path, input_value: str, owner_value: str, *, official: Any | None = None) -> dict[str, Any]:
    package = Path(__file__).resolve().parents[1]
    public = read_json(input_value, "input")
    owner = read_json(owner_value, "owner_result")
    validate_json(public, package / "schemas/public-input.schema.json", "input")
    validate_json(owner, package / "schemas/semantic-result.schema.json", "owner_result")
    for field in ("profile", "mode", "task_id", "lifecycle_generation", "continuation_id"):
        if owner[field] != public[field]:
            return _blocked(package, "stale_semantic_result", field)
    profile = public["profile"]
    if owner["route"] != PROFILE_ROUTES[profile]:
        return _blocked(package, "route_mismatch", "owner_result.route")
    for field in ("current_task_id", "current_lifecycle_generation"):
        if public.get(field) != owner.get(field):
            return _blocked(package, "stale_semantic_result", field)
    lifecycle = {"task_id": public["task_id"], "lifecycle_generation": public["lifecycle_generation"]}
    validate_dto("TaskLifecycleDTO", lifecycle)
    root = root.resolve()
    official = official if official is not None else official_port(root)

    try:
        # The official resolver is the sole authority for current TaskId/generation.
        facts = official.repository_facts(root)
        resolved = official.resolve_task_identity(facts, lifecycle["task_id"], lifecycle["lifecycle_generation"])
        _current_lifecycle(root, lifecycle, resolved)
        state, record = _record(official, root)
        already_current = state == "present" and (record.task_id, record.lifecycle_generation) == (
            public["task_id"], public["lifecycle_generation"]
        )
        if state == "present":
            if profile == "resume_current_task":
                if (record.task_id, record.lifecycle_generation) != (public["task_id"], public["lifecycle_generation"]):
                    return _blocked(package, "session_target_mismatch", "session")
                resolved = resolve_session(official, root)
                if resolved.status != "session_resolved" or resolved.lifecycle is None:
                    return _blocked(package, "session_invalid", "session")
            elif profile == "switch_task":
                source = (public["current_task_id"], public["current_lifecycle_generation"])
                if (record.task_id, record.lifecycle_generation) != source or source == (public["task_id"], public["lifecycle_generation"]):
                    return _blocked(package, "session_source_mismatch", "session")
                source_resolved = official.resolve_task_identity(facts, *source)
                _current_lifecycle(root, {"task_id": source[0], "lifecycle_generation": source[1]}, source_resolved)
            elif profile == "reactivate_rebind":
                if not already_current and (record.task_id != public["task_id"] or record.lifecycle_generation >= public["lifecycle_generation"]):
                    return _blocked(package, "session_target_mismatch", "session")
            elif profile == "manual_recovery" and not already_current:
                return _blocked(package, "session_target_mismatch", "session")
            elif not already_current:
                return _blocked(package, "session_target_mismatch", "session")
        elif state == "missing" and profile in {"resume_current_task", "switch_task"}:
            return _blocked(package, "session_missing", "session")
        if state == "explicit_task_mode":
            output = {"exit_id": "explicit_task_mode", **lifecycle}
        elif profile == "resume_current_task" or already_current:
            output = {"exit_id": EXITS[owner["route"]], **lifecycle, "resume_target": owner["resume_target"]}
        else:
            result = bind_session(official, root, lifecycle)
            if result.status == "explicit_task_mode":
                output = {"exit_id": "explicit_task_mode", **lifecycle}
            elif result.status != "session_bound" or result.lifecycle is None or result.lifecycle.task_id != lifecycle["task_id"] or result.lifecycle.lifecycle_generation != lifecycle["lifecycle_generation"]:
                return _blocked(package, result.reason_code or "session_invalid", "session")
            else:
                output = {"exit_id": EXITS[owner["route"]], **lifecycle, "resume_target": owner["resume_target"]}
    except LifecycleContractError as exc:
        return _blocked(package, exc.code, exc.field_path)
    except (OSError, RuntimeError, ValueError, AttributeError) as exc:
        reason = str(exc).partition(":")[0]
        known = {
            "stale_lifecycle_generation", "stale_task_identity", "ambiguous_task_identity",
            "task_id_casefold_collision", "unsupported_binding_schema", "invalid_binding_fields",
        }
        code = reason if reason in known else "session_identity_invalid"
        ref = "task_id" if code in known - {"unsupported_binding_schema", "invalid_binding_fields"} else "session"
        return _blocked(package, code, ref)
    schema = "public-explicit-output.schema.json" if output["exit_id"] == "explicit_task_mode" else "public-output.schema.json"
    validate_json(output, package / "schemas" / schema, "stdout")
    return output


def run(package_root: Path, command: dict, argv: list[str]):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    args = parser.parse_args(argv)
    return execute(Path(args.root), args.input, args.owner_result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    args = parser.parse_args()
    print(json.dumps(execute(Path(args.root), args.input, args.owner_result), ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    try:
        main()
    except CommandError as exc:
        print(json.dumps({"code": exc.code, "field_path": exc.field_path, "remediation": exc.remediation}, ensure_ascii=False))
        raise SystemExit(exc.exit_status)
