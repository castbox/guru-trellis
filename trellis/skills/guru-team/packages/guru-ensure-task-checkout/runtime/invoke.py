from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError, fail, read_json, write_json
from runtime.schema import validate_json
from runtime.task_lifecycle.active_checkout import read_bound_checkout
from runtime.task_lifecycle.branch_store import TaskLifecycleKey
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.identity import resolve_task_id, task_resource_state


def invoke(root: Path, data: dict) -> dict:
    package = Path(__file__).resolve().parents[1]
    validate_json(data, package / "schemas/public-input.schema.json", "input")
    repository = inspect_repository(root)
    key = TaskLifecycleKey(data["task_id"], data["lifecycle_generation"])
    try:
        _, current = read_bound_checkout(repository, key)
    except LifecycleContractError as exc:
        if exc.code in {"binding_required", "checkout_required"}:
            return {"exit_id": exc.code, "task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation}
        if exc.code in {"binding_ownership_mismatch", "ambiguous_checkout", "checkout_identity_mismatch"}:
            return {"exit_id": "invalid_task_state", "reason_code": exc.code}
        raise
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
