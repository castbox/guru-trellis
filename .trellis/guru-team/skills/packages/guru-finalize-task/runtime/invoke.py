from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any

from common import call_owner, parse_arguments


HAPPY_PATH_COMMAND_ID = "finalize-task-happy-path"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _o(package_root: Path):
    return _load_module("finalize_owner", package_root / "runtime/owner.py")


def _facade(package_root: Path):
    return _load_module("finalize_facade", package_root / "runtime/facade.py")


def _run_legacy(package_root: Path, argv: list[str]) -> dict[str, Any]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    for name in ("repo", "base_branch", "remote", "title", "task_name"):
        parser.add_argument("--" + name.replace("_", "-"))
    parser.add_argument("--validation", action="append")
    args = parse_arguments(parser, argv)
    owner_runtime = _o(package_root)

    def invoke_owner():
        root = owner_runtime.repo_root(Path(args.root or "."))
        public_input, _ = owner_runtime.finalization_public_input(root, args.input)
        owner_result, owner_path = owner_runtime.finalization_gate_input(
            root,
            public_input,
            args.owner_result,
        )
        checked, plan = owner_runtime.check_finalization_gate_result(
            root,
            args,
            public_input,
            owner_result,
            owner_path,
        )
        exit_id = str((checked.get("route") or {}).get("typed_exit") or "")
        payload = (checked.get("route") or {}).get("output")
        if payload == owner_runtime.FINALIZATION_EXECUTOR_OUTPUT_MARKER:
            closeout = plan.get("plan")
            pr = plan.get("published_pr")
            if not isinstance(closeout, dict) or not isinstance(pr, dict):
                raise owner_runtime.WorkflowError(
                    "Finalization terminal output is not materializable.",
                    exit_code=2,
                )
            payload = owner_runtime.finalization_gate_with_ready_for_merge_output(
                root,
                plan["task_dir"],
                checked,
                closeout,
                pr,
            )["route"]["output"]
        schema, _ = owner_runtime.stage0_output_contract(
            owner_runtime.FINALIZE_TASK_SKILL_ID,
            owner_runtime.finalization_package_root(root),
            owner_runtime.finalization_interface(root),
            exit_id,
        )
        errors = owner_runtime.skill_json_schema_validation_errors(
            payload,
            schema,
            f"finalization output {exit_id}",
        )
        if errors:
            raise owner_runtime.WorkflowError(
                "Finalization typed output invalid.",
                exit_code=2,
                payload={"errors": errors},
            )
        if exit_id == "ready_for_merge":
            owner_runtime.finalization_retire_current_state(root, plan["task_dir"])
        return payload

    return call_owner(owner_runtime, invoke_owner, public=True)


def run(
    package_root: Path,
    command: dict[str, Any],
    argv: list[str],
) -> dict[str, Any]:
    if command.get("id") == HAPPY_PATH_COMMAND_ID:
        return _facade(package_root).run(package_root, command, argv)
    return _run_legacy(package_root, argv)
