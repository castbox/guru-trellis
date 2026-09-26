from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError, fail, read_json, write_json
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import TaskLifecycleKey
from runtime.task_lifecycle.composition import activate_task_status, prepare_activation_inputs, recover_activation_inputs
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.session_adapter import SessionAdapterResult


def invoke(root: Path, data: dict) -> dict:
    package = Path(__file__).resolve().parents[1]
    validate_json(data, package / "schemas/public-input.schema.json", "input")
    activation = data["activation"]
    key = TaskLifecycleKey(activation["task_id"], activation["lifecycle_generation"])
    session = SessionAdapterResult(activation["session_mode"], key)
    try:
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
