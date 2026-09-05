from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any

from common import call_owner, parse_arguments


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _o(package_root: Path):
    return _load_module("finalize_owner", package_root / "runtime/owner.py")


def _transaction(package_root: Path):
    return _load_module(
        "finalize_transaction",
        package_root / "runtime/transaction.py",
    )


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--review-input")
    parser.add_argument("--confirmed-preview-sha256")
    parser.add_argument("--owner-result")
    for name in ("repo", "base_branch", "remote", "title", "task_name"):
        parser.add_argument("--" + name.replace("_", "-"))
    parser.add_argument("--validation", action="append")
    return parse_arguments(parser, argv)


def _run_compatibility(owner: Any, args: argparse.Namespace) -> dict[str, Any]:
    root = owner.repo_root(Path(args.root or "."))
    public_input, _ = owner.finalization_public_input(root, args.input)
    owner_result, owner_path = owner.finalization_gate_input(
        root,
        public_input,
        args.owner_result,
    )
    checked, plan = owner.check_finalization_gate_result(
        root,
        args,
        public_input,
        owner_result,
        owner_path,
    )
    exit_id = str((checked.get("route") or {}).get("typed_exit") or "")
    payload = (checked.get("route") or {}).get("output")
    if payload == owner.FINALIZATION_EXECUTOR_OUTPUT_MARKER:
        closeout = plan.get("plan")
        pr = plan.get("published_pr")
        if not isinstance(closeout, dict) or not isinstance(pr, dict):
            raise owner.WorkflowError(
                "Finalization terminal output is not materializable.",
                exit_code=2,
            )
        payload = owner.finalization_gate_with_ready_for_merge_output(
            root,
            plan["task_dir"],
            checked,
            closeout,
            pr,
        )["route"]["output"]
    schema, _ = owner.stage0_output_contract(
        owner.FINALIZE_TASK_SKILL_ID,
        owner.finalization_package_root(root),
        owner.finalization_interface(root),
        exit_id,
    )
    errors = owner.skill_json_schema_validation_errors(
        payload,
        schema,
        f"finalization output {exit_id}",
    )
    if errors:
        raise owner.WorkflowError(
            "Finalization typed output invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    if exit_id == "ready_for_merge":
        owner.finalization_retire_current_state(root, plan["task_dir"])
    return payload


def run(
    package_root: Path,
    command: dict[str, Any],
    argv: list[str],
) -> dict[str, Any]:
    del command
    args = _parse_args(argv)
    owner = _o(package_root)

    def invoke_owner() -> dict[str, Any]:
        has_review = bool(args.review_input)
        has_owner_result = bool(args.owner_result)
        if has_review == has_owner_result:
            raise owner.WorkflowError(
                "Finalization public invocation requires exactly one of --review-input or --owner-result.",
                exit_code=2,
            )
        if has_owner_result:
            if args.confirmed_preview_sha256:
                raise owner.WorkflowError(
                    "Finalization compatibility invocation cannot accept --confirmed-preview-sha256.",
                    exit_code=2,
                )
            return _run_compatibility(owner, args)
        return _transaction(package_root).execute_confirmed_transaction(owner, args)

    return call_owner(owner, invoke_owner, public=True)
