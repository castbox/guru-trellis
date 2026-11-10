from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError, fail, read_json, write_json
from runtime.schema import validate_json
from runtime.delivery_projection.adapter import official_session_port
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import discover_worktree_facts, inspect_repository
from runtime.task_lifecycle.identity import resolve_task_id, task_resource_state
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


def invoke(root: Path, data: dict) -> dict:
    package = Path(__file__).resolve().parents[1]
    validate_json(data, package / "schemas/public-input.schema.json", "input")
    if data["profile"] == "delivery_current_task":
        try:
            return current_context(root)
        except LifecycleContractError as exc:
            raise CommandError(exc.code, exc.field_path, exc.remediation, 3) from exc
    return resolve_checkout(root, TaskLifecycleKey(data["task_id"], data["lifecycle_generation"]))


def resolve_checkout(root: Path, key: TaskLifecycleKey) -> dict:
    repository = inspect_repository(root)
    binding = BranchBindingStore(repository).read(key)
    if binding is None:
        return {"exit_id": "binding_required", "task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation}
    ownership = ResourceLedgerStore(repository).read_current(key)
    if ownership is None:
        return {"exit_id": "binding_required", "task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation}
    if (ownership.binding_revision, ownership.branch_name) != (
        binding.binding_revision, binding.branch_name
    ):
        return {"exit_id": "invalid_task_state", "reason_code": "binding_ownership_mismatch"}
    candidates = [row for row in discover_worktree_facts(repository) if row.registration.registered_branch_ref == binding.branch_ref]
    if not candidates:
        return {"exit_id": "checkout_required", "task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation}
    if len(candidates) != 1:
        return {"exit_id": "invalid_task_state", "reason_code": "ambiguous_checkout"}
    current = candidates[0]
    if current.inspection_error or current.common_dir != repository.common_dir or current.branch_ref != binding.branch_ref:
        return {"exit_id": "invalid_task_state", "reason_code": "checkout_identity_mismatch"}
    try:
        task = resolve_task_id(current.path, key.task_id)
    except LifecycleContractError as exc:
        if exc.code == "task_not_found":
            return {"exit_id": "invalid_task_state", "reason_code": "task_artifact_mismatch"}
        raise
    if task.lifecycle_state != "active" or task.lifecycle_generation != key.lifecycle_generation:
        return {"exit_id": "invalid_task_state", "reason_code": "task_identity_stale"}
    metadata = json.loads((current.path / task.task_ref / "task.json").read_text(encoding="utf-8"))
    if task_resource_state(current.path, metadata) != "active":
        return {"exit_id": "invalid_task_state", "reason_code": "task_status_mismatch"}
    return {
        "exit_id": "checkout_resolved", "task_id": key.task_id, "task_ref": task.task_ref,
        "lifecycle_generation": key.lifecycle_generation, "checkout_path": str(current.path),
    }


def current_error(error: object, code: str, field_path: str) -> CommandError:
    if isinstance(error, dict):
        return CommandError(
            error.get("code", code), error.get("field_path", field_path),
            error.get("remediation") or error.get("message") or str(error), 3,
        )
    message = str(error)
    original_code, separator, _ = message.partition(":")
    if separator and original_code.replace("_", "").isalnum():
        code = original_code
    return CommandError(code, field_path, message, 3)


def current_context(root: Path) -> dict:
    if official_session_port(root).resolve_context_key() is None:
        return {"exit_id": "context_unavailable", "reason_code": "context_key_unavailable"}
    script = root / ".trellis/scripts/task.py"
    if not script.is_file():
        raise CommandError("unsupported_delivery_api", "upstream.task.current", "Install the reviewed public task.py current --json entry.", 3)
    result = subprocess.run(
        [sys.executable, str(script), "current", "--json"],
        cwd=root, capture_output=True, text=True,
    )
    try:
        payload = json.loads(result.stdout)
    except ValueError as exc:
        if result.returncode and result.stderr.strip():
            diagnostic = result.stderr.strip()
            try:
                error = json.loads(diagnostic)
            except ValueError:
                error = diagnostic.removeprefix("Error: ")
            raise current_error(error, "current_query_failed", "upstream.task.current") from exc
        raise CommandError("invalid_current_output", "upstream.task.current", "Read the public task.py current --json diagnostic and restore its runtime before retrying.", 3) from exc
    if not isinstance(payload, dict):
        raise CommandError("invalid_current_output", "upstream.task.current", "Restore the public current JSON object before retrying.", 3)
    if payload.get("error"):
        raise current_error(payload["error"], "stale_binding", "current_task")
    if "code" in payload:
        raise current_error(payload, "current_query_failed", "current_task")
    if payload.get("stale"):
        raise CommandError("stale_binding", "current_task", "Resolve the stale binding through the original session owner.", 3)
    task = payload.get("current_task")
    if task is None and result.returncode == 1 and payload.get("source") == "none":
        return {"exit_id": "no_current_task"}
    if result.returncode != 0 or not isinstance(task, dict):
        raise CommandError("current_query_failed", "current_task", "Resolve the original public current query failure before retrying.", 3)
    if task.get("schema_version") != "2.0":
        raise CommandError("unsupported_task_schema", "current_task.schema_version", "Use the original Task lifecycle owner for this Task schema.", 3)
    key = TaskLifecycleKey(task["id"], task["lifecycle_generation"])
    resolved = resolve_checkout(root, key)
    if resolved["exit_id"] != "checkout_resolved":
        return resolved
    if (task.get("dir") != resolved["task_ref"]
            or payload.get("task_workspace_root") != resolved["checkout_path"]):
        return {"exit_id": "invalid_task_state", "reason_code": "checkout_identity_mismatch"}
    selection = task["current_delivery"]
    if selection["kind"] == "error":
        raise current_error(selection, "stale_binding", "current_task.current_delivery")
    if selection["kind"] == "terminal_delivery":
        raise CommandError("terminal_delivery", "current_task.current_delivery", "Return to the original terminal Delivery lifecycle owner.", 3)
    resolved["exit_id"] = "current_context_ready"
    if selection["kind"] == "no_current_delivery":
        expected_key = {"task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation}
    elif selection["kind"] == "current":
        delivery = selection["delivery"]
        expected_key = {"task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation, "delivery_id": delivery["id"]}
        if delivery["lifecycle_generation"] != key.lifecycle_generation:
            return {"exit_id": "invalid_task_state", "reason_code": "task_identity_stale"}
        resolved["current_delivery"] = {
            "delivery_key": expected_key, "phase": delivery["phase"],
            "planning_root": delivery["planning_root"],
        }
    else:
        raise CommandError("invalid_current_output", "current_task.current_delivery.kind", "Read the exact public current selection diagnostic before retrying.", 3)
    if selection["key"] != expected_key:
        return {"exit_id": "invalid_task_state", "reason_code": "task_identity_stale"}
    return resolved


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    output = invoke(Path(args.root).resolve(), read_json(args.input, "input"))
    validate_json(output, package_root / "schemas/public-output.schema.json", "stdout")
    return output


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    try:
        args = parser.parse_args(argv)
        package = Path(__file__).resolve().parents[1]
        output = invoke(Path(args.root).resolve(), read_json(args.input, "input"))
        validate_json(output, package / "schemas/public-output.schema.json", "stdout")
        write_json(output)
        return 0
    except LifecycleContractError as exc:
        return fail(CommandError("stale_identity", exc.field_path, exc.remediation, 3))
    except CommandError as exc:
        return fail(exc)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
