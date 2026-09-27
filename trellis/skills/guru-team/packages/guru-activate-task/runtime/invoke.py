from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError, fail, read_json, write_json
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import TaskLifecycleKey
from runtime.task_lifecycle.composition import activate_task_status, prepare_activation_inputs, recover_activation_inputs
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.session_adapter import SessionAdapterResult, resolve_session


def _binding_module() -> Any:
    module_path = Path(__file__).resolve().parents[2] / "guru-bind-task-session/runtime/invoke.py"
    spec = importlib.util.spec_from_file_location("guru_activation_session_port", module_path)
    if spec is None or spec.loader is None:
        raise LifecycleContractError("official_session_unavailable", "session", "Install the Fixed Fork session API.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _official_port(checkout: Path) -> Any:
    return _binding_module().official_port(checkout)


def invoke(root: Path, data: dict) -> dict:
    package = Path(__file__).resolve().parents[1]
    validate_json(data, package / "schemas/public-input.schema.json", "input")
    activation = data["activation"]
    key = TaskLifecycleKey(activation["task_id"], activation["lifecycle_generation"])
    try:
        official = _official_port(root)
        scoped = _binding_module()._current_lifecycle(
            root, {"task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation}, official,
        )
        if scoped.workspace.resolve() != root.resolve():
            raise LifecycleContractError(
                "activation_checkout_mismatch", "root",
                "Invoke activation from the current bound task checkout.",
            )
        if activation["session_mode"] == "session_bound":
            # The binding owner scopes the official resolver to the current
            # branch checkout; a retained old checkout may contain the same task.
            session = resolve_session(scoped, root)
            if session.status != "session_resolved" or session.lifecycle != key or session.task_ref != activation["task_ref"]:
                raise LifecycleContractError("activation_session_mismatch", "session", "Rebind or switch to the reviewed current task before activation.")
            session = SessionAdapterResult("session_bound", key, session.context_key, session.task_ref)
        else:
            session = resolve_session(scoped, root)
            if session.status != "explicit_task_mode" or session.reason_code != "context_key_unavailable":
                raise LifecycleContractError("activation_session_mismatch", "session", "Resolve the current session route before activation.")
            session = SessionAdapterResult("explicit_task_mode", key, reason_code="context_key_unavailable")
        if data["action"] == "recover_activation":
            result = recover_activation_inputs(root, activation, session)
        else:
            result = prepare_activation_inputs(root, activation, session)
            activate_task_status(root, result)
    except LifecycleContractError as exc:
        if exc.code in {"activation_approval_stale", "activation_base_stale", "activation_head_stale"}:
            return {"exit_id": "refresh_review", "task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation}
        if exc.code in {"activation_identity_stale", "activation_status_mismatch", "invalid_task_identity", "invalid_task_ref", "task_not_found"}:
            return {"exit_id": "invalid_task_state", "reason_code": exc.code}
        return {"exit_id": "blocked", "reason_code": exc.code}
    return {
        "exit_id": "activated", "task_id": result.task_id,
        "task_ref": result.task_ref, "lifecycle_generation": result.lifecycle_generation,
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
