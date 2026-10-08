from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError, fail, read_json, write_json
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.checkout_acquisition import CheckoutAcquisitionPlan, CheckoutAcquisitionResult, acquire_checkout
from runtime.task_lifecycle.composition import (
    bind_created_session, establish_created_control_state, prepare_creation_inputs,
    recover_created_control_state,
)
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import find_registration, inspect_registered_worktree, inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.session_adapter import resolve_session


PACKAGE = Path(__file__).resolve().parents[1]
TASK_DATE_TIMEZONE = ZoneInfo("Asia/Shanghai")


def _task_date_prefix() -> str:
    return datetime.now(TASK_DATE_TIMEZONE).strftime("%m-%d")


def _require_current_task_date(task_ref: str) -> None:
    if Path(task_ref).name[:5] != _task_date_prefix():
        raise LifecycleContractError("creation_date_stale", "task_ref", "Review a TaskRef for the current Shanghai business date.")


def _plan(root: Path, data: dict[str, Any]) -> CheckoutAcquisitionPlan:
    value = data["acquisition"]
    return CheckoutAcquisitionPlan(
        route=value["route"], repository_context=root,
        task_id=data["creation"]["task_id"], task_ref=data["creation"]["task_ref"],
        lifecycle_generation=0, branch_ref=value["branch_ref"],
        expected_status="planning", decision_head=value["decision_head"],
        transaction_id=value["transaction_id"], result_id=value["result_id"],
        provision_disposition=value.get("provision_disposition"),
        invocation_checkout=Path(value["invocation_checkout"]).resolve() if "invocation_checkout" in value else None,
        target_path=Path(value["checkout_root"]).resolve() if "checkout_root" in value else None,
        forbidden_branch_refs=(data["creation"]["selected_base_ref"], data["creation"]["delivery_target"]["branch_ref"]),
        task_artifact_expectation="absent",
    )


def _created_result(inputs: Any) -> dict[str, Any]:
    return {
        "exit_id": "created", "task_id": inputs.task_id,
        "task_ref": inputs.task_ref, "lifecycle_generation": 0,
    }


def _create_official_task(checkout: Path, inputs: Any, task: dict[str, Any]) -> None:
    task_path = checkout / inputs.task_ref
    if task_path.exists():
        raise LifecycleContractError("task_identity_already_exists", "task_ref", "Resolve the existing task before creation.")
    directory = Path(inputs.task_ref).name
    if len(directory) < 7 or directory[2:3] != "-" or directory[5:6] != "-":
        raise LifecycleContractError("invalid_task_ref", "task_ref", "Use the official date-prefixed task locator.")
    slug = directory[6:]
    _require_current_task_date(inputs.task_ref)
    script = checkout / ".trellis/scripts/task.py"
    if not script.is_file():
        raise LifecycleContractError("official_task_store_missing", "task.py", "Install the Fixed Fork task store in the selected checkout.")
    command = [
        sys.executable, str(script), "create", task["title"],
        "--description", task["description"], "--slug", slug,
        "--task-id", inputs.task_id,
        "--source-json", json.dumps(inputs.reviewed_source, separators=(",", ":")),
        "--base-branch", inputs.selected_base_ref.removeprefix("refs/heads/"),
        "--no-start",
    ]
    completed = subprocess.run(
        command, cwd=checkout, text=True, capture_output=True, check=False,
        env={**os.environ, "TZ": "Asia/Shanghai"},
    )
    if completed.returncode and _task_date_prefix() != directory[:5]:
        raise LifecycleContractError("creation_date_stale", "task_ref", "Review a TaskRef for the current Shanghai business date.")
    if completed.returncode or not (task_path / "task.json").is_file():
        raise LifecycleContractError("official_task_create_failed", "task.py create", "Resolve the official task creation failure without forcing an existing task.")
    metadata_path = task_path / "task.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise LifecycleContractError("official_task_create_failed", "task.json", "Read the new official task artifact.") from exc
    if (metadata.get("status") != "planning" or metadata.get("name") != slug
            or metadata.get("id") != inputs.task_id or metadata.get("source") != inputs.reviewed_source):
        raise LifecycleContractError("official_task_create_failed", "task.json", "Use the exact new planning task.")
    for legacy in (
        "branch", "base_head", "entry_head", "workspace_slug",
        "workspace_path", "workspace_mode", "source_checkout",
        "issue", "issue_url", "source_issue_url", "close_issues", "related_issues",
        "followup_issues", "archive_dir",
    ):
        metadata.pop(legacy, None)
    metadata["lifecycle_generation"] = 0
    metadata["scope"] = task["scope"]
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _recover_acquired(plan: CheckoutAcquisitionPlan) -> CheckoutAcquisitionResult:
    expected = plan.invocation_checkout if plan.route == "adopt_invocation_checkout" else plan.target_path
    repository = inspect_repository(plan.repository_context)
    registration = find_registration(repository, expected) if expected is not None else None
    if registration is None:
        raise LifecycleContractError("creation_result_mismatch", "checkout", "Recover only the reviewed checkout path.")
    checkout = inspect_registered_worktree(repository, registration)
    if checkout.inspection_error or checkout.branch_ref != plan.request().branch_ref or checkout.head != plan.decision_head:
        raise LifecycleContractError("creation_result_mismatch", "checkout", "Recover only the reviewed branch and decision HEAD.")
    disposition = plan.provision_disposition
    created_branch = plan.route == "provision_linked_worktree" and disposition == "new_branch"
    created_worktree = plan.route == "provision_linked_worktree" and disposition != "existing_checkout"
    return CheckoutAcquisitionResult(
        route=plan.route, action="recovered", checkout=checkout,
        transaction_id=plan.transaction_id, result_id=plan.result_id,
        branch_ownership="guru_owned" if created_branch else "caller_owned",
        worktree_ownership=("not_applicable" if checkout.topology == "primary" else
                            "guru_owned" if created_worktree else "caller_owned"),
        created_branch=created_branch, created_worktree=created_worktree,
    )


def _official_port(checkout: Path) -> Any:
    module_path = PACKAGE.parent / "guru-bind-task-session/runtime/invoke.py"
    spec = importlib.util.spec_from_file_location("guru_creation_session_port", module_path)
    if spec is None or spec.loader is None:
        raise LifecycleContractError("official_session_unavailable", "session", "Install the Fixed Fork session API.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.official_port(checkout)


def invoke(root: Path, data: dict[str, Any]) -> dict[str, Any]:
    validate_json(data, PACKAGE / "schemas/public-input.schema.json", "input")
    plan = _plan(root, data)
    try:
        if data["action"] == "recover_created_task_result":
            # Recovery must not run the pre-creation uniqueness check or repeat mutation.
            from runtime.task_lifecycle.composition import CreationInputs
            creation = data["creation"]
            inputs = CreationInputs(
                creation["task_id"], creation["task_ref"], creation["source_profile"],
                creation["reviewed_source"], creation["accepted_scope_identity"],
                creation["delivery_target"], creation["selected_base_ref"],
                creation["reviewed_base_head"], plan,
            )
            acquired = _recover_acquired(plan)
            key = TaskLifecycleKey(inputs.task_id, 0)
            binding = BranchBindingStore(inspect_repository(root)).read(key)
            if binding is None:
                raise LifecycleContractError("creation_result_mismatch", "binding", "Recover the completed initial binding.")
            recover_created_control_state(inputs, acquired, expected_result_id=inputs.result_id)
            official = _official_port(acquired.checkout.path)
            current = resolve_session(official, acquired.checkout.path)
            if current.status == "session_resolved":
                if current.lifecycle != key or current.task_ref != inputs.task_ref:
                    return {"exit_id": "blocked", "reason_code": "session_current_task_conflict"}
            elif current.status == "explicit_task_mode" and current.reason_code == "session_record_missing":
                session = bind_created_session(
                    official, inputs, acquired,
                )
                if session.status != "session_bound":
                    return {"exit_id": "blocked", "reason_code": session.reason_code or session.status}
            elif current.status != "explicit_task_mode" or current.reason_code != "context_key_unavailable":
                return {"exit_id": "blocked", "reason_code": current.reason_code or current.status}
        else:
            _require_current_task_date(data["creation"]["task_ref"])
            inputs = prepare_creation_inputs(root, data["creation"], plan)
            acquired: CheckoutAcquisitionResult | None = None

            def materialize(result: CheckoutAcquisitionResult) -> None:
                nonlocal acquired
                acquired = result
                checkout = result.checkout.path
                key = TaskLifecycleKey(inputs.task_id, 0)
                repository = inspect_repository(root)
                branches = BranchBindingStore(repository)
                resources = ResourceLedgerStore(repository)
                before_branch = branches.snapshot(key)
                before_resources = resources.snapshot(key)
                try:
                    _create_official_task(checkout, inputs, data["task"])
                    establish_created_control_state(inputs, result)
                except Exception:
                    try:
                        resources.restore(key, before_resources)
                    finally:
                        branches.restore(before_branch)
                        task_path = checkout / inputs.task_ref
                        if task_path.is_dir():
                            shutil.rmtree(task_path)
                    raise

            acquire_checkout(plan, post_acquire=materialize)
            if acquired is None:
                raise LifecycleContractError("creation_result_mismatch", "acquisition", "Complete the reviewed acquisition.")
            # Session binding follows the durable task/control transaction. A missing
            # context key is an explicit-task result; a session write failure is reported
            # without deleting the task that was already created.
            session = bind_created_session(_official_port(acquired.checkout.path), inputs, acquired)
            if session.status not in {"session_bound", "explicit_task_mode"}:
                return {"exit_id": "blocked", "reason_code": session.reason_code or session.status}
        return _created_result(inputs)
    except LifecycleContractError as exc:
        if exc.code in {"creation_base_stale", "creation_date_stale"}:
            return {"exit_id": "refresh_review", "reason_code": exc.code}
        diagnostic = {}
        if exc.code in {
            "task_identity_already_exists", "invalid_task_identity", "invalid_task_metadata",
            "invalid_task_id", "unsupported_legacy_task", "invalid_lifecycle_generation",
            "invalid_task_ref", "task_not_found",
        }:
            diagnostic = {"diagnostic": {"field_path": exc.field_path, "remediation": exc.remediation}}
        if exc.code in {"task_identity_already_exists", "creation_identity_mismatch", "creation_control_state_exists", "creation_result_mismatch", "invalid_task_identity"}:
            return {"exit_id": "invalid_task_state", "reason_code": exc.code, **diagnostic}
        return {"exit_id": "blocked", "reason_code": exc.code, **diagnostic}


def run(package_root: Path, command: dict, argv: list[str]) -> dict[str, Any]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    data = read_json(args.input, "input")
    command_id = command.get("id", "invoke-guru-create-task")
    if command_id == "record-task-plan":
        validate_json(data, package_root / "schemas/public-input.schema.json", "input")
        if data["action"] != "create_task":
            raise CommandError("invalid_arguments", "action", "Record only a fresh task creation plan.")
        _require_current_task_date(data["creation"]["task_ref"])
        try:
            prepare_creation_inputs(Path(args.root).resolve(), data["creation"], _plan(Path(args.root).resolve(), data))
        except LifecycleContractError as exc:
            raise CommandError("stale_identity", exc.field_path, f"{exc.code}: {exc.remediation}", 3) from exc
        return {"status": "ready", "task_id": data["creation"]["task_id"]}
    if command_id in {"check-task-creation-result", "recover-created-task-result"}:
        data = {**data, "action": "recover_created_task_result"}
    elif command_id == "create-task":
        data = {**data, "action": "create_task"}
    output = invoke(Path(args.root).resolve(), data)
    validate_json(output, package_root / "schemas/public-output.schema.json", "stdout")
    return output


def main(argv: list[str]) -> int:
    try:
        output = run(PACKAGE, {}, argv)
        write_json(output)
        return 0
    except LifecycleContractError as exc:
        return fail(CommandError("stale_identity", exc.field_path, exc.remediation, 3))
    except CommandError as exc:
        return fail(exc)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
