from __future__ import annotations

import argparse
import copy
import re
from pathlib import Path
from typing import Any

COMPONENT_PATH_COMMAND_INVOCATIONS = 5
PUBLIC_INVOKE_COMMAND_INVOCATIONS = 1
COMPONENT_PATH_FULL_PREVIEW_READS = 5
PUBLIC_INVOKE_FULL_PREVIEW_READS = 1


def invoke_budget() -> dict[str, int]:
    return {
        "component_path_command_invocations": COMPONENT_PATH_COMMAND_INVOCATIONS,
        "public_invoke_command_invocations": PUBLIC_INVOKE_COMMAND_INVOCATIONS,
        "command_reduction_percent": 80,
        "component_path_full_preview_reads": COMPONENT_PATH_FULL_PREVIEW_READS,
        "public_invoke_full_preview_reads": PUBLIC_INVOKE_FULL_PREVIEW_READS,
        "full_preview_read_reduction_percent": 80,
    }


def _count(counters: dict[str, int], operation: str) -> None:
    counters[operation] = counters.get(operation, 0) + 1


def _blocked_output(owner: Any, root: Path, remediation: str) -> dict[str, Any]:
    output = {
        "exit_id": "blocked",
        "reason_code": "invalid_private_state",
        "remediation": remediation,
    }
    errors = owner.skill_json_schema_validation_errors(
        output,
        owner.finalization_output_contract(root, "blocked"),
        "task finalization public invocation blocked output",
    )
    if errors:
        raise owner.WorkflowError(
            "Task finalization public invocation blocked output is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return output


def _project_output(owner: Any, root: Path, result: dict[str, Any]) -> dict[str, Any]:
    output = result.get("output")
    exit_id = str(result.get("typed_exit") or "")
    if not isinstance(output, dict) or output.get("exit_id") != exit_id:
        raise owner.WorkflowError(
            "Task finalization public invocation did not produce one materialized typed exit.",
            exit_code=2,
        )
    errors = owner.skill_json_schema_validation_errors(
        output,
        owner.finalization_output_contract(root, exit_id),
        f"task finalization public invocation output {exit_id}",
    )
    if errors:
        raise owner.WorkflowError(
            "Task finalization public invocation typed output is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return output


def _record_checked_gate(
    owner: Any,
    root: Path,
    public_input: dict[str, Any],
    reviewed: dict[str, Any],
    context: dict[str, Any],
    counters: dict[str, int],
) -> tuple[dict[str, Any], Path]:
    recorded = owner.finalization_record_gate_result(
        root,
        public_input,
        reviewed,
        context,
        dry_run=False,
        include_private=True,
    )
    _count(counters, "semantic.record")
    gate = recorded.get("gate")
    gate_path = recorded.get("gate_path")
    if not isinstance(gate, dict) or not isinstance(gate_path, Path):
        raise owner.WorkflowError(
            "Task finalization public invocation recorder did not retain its private gate.",
            exit_code=2,
        )
    checked, _ = owner.check_finalization_gate_context(
        root,
        public_input,
        gate,
        gate_path,
        context,
        allow_pending_transition=True,
    )
    _count(counters, "objective.check")
    return checked, gate_path


def _mapped_reprepare_review(
    owner: Any,
    root: Path,
    reviewed: dict[str, Any],
    public_input: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    reason_code = context.get("reprepare_reason_code")
    plan = context.get("plan")
    if not isinstance(plan, dict) or reason_code not in {
        owner.FINALIZATION_REPREPARE_ARCHIVE_MONTH,
        owner.FINALIZATION_REPREPARE_PROVENANCE_TAIL,
    }:
        raise owner.WorkflowError(
            "Task finalization public invocation encountered an unmapped reprepare state.",
            exit_code=2,
        )
    output = (
        copy.deepcopy(owner.FINALIZATION_EXECUTOR_OUTPUT_MARKER)
        if reason_code == owner.FINALIZATION_REPREPARE_PROVENANCE_TAIL
        else owner.finalization_reprepare_public_output(
            root,
            task_ref=public_input["task_ref"],
            reason_code=reason_code,
            branch_review_commit=plan["git"]["branch_review_commit"],
            publication_head=(
                plan["git"].get("publication_head")
                or plan["git"]["branch_review_commit"]
            ),
        )
    )
    return {
        "schema_version": reviewed["schema_version"],
        "skill_id": reviewed["skill_id"],
        "review": copy.deepcopy(reviewed["review"]),
        "route": {
            "typed_exit": "reprepare_required",
            "consumer": copy.deepcopy(
                owner.FINALIZATION_CONSUMERS["reprepare_required"]
            ),
            "output": output,
        },
    }


def execute_confirmed_transaction(
    owner: Any,
    args: argparse.Namespace,
    *,
    counters: dict[str, int] | None = None,
) -> dict[str, Any]:
    operation_counts = counters if counters is not None else {}
    operation_counts.setdefault("terminal.post_exit_operation", 0)
    root = owner.repo_root(Path(args.root or "."))
    public_input, _ = owner.finalization_public_input(root, args.input)
    reviewed = owner.finalization_semantic_review_input(root, args.review_input)
    context = owner.finalization_preview_context(root, args, public_input)
    _count(operation_counts, "preview.read")
    confirmed = str(args.confirmed_preview_sha256 or "")
    expected = owner.finalization_confirmation_identity(public_input, context)
    requested_exit = str((reviewed.get("route") or {}).get("typed_exit") or "")
    terminal_recovery = (
        requested_exit == "ready_for_merge"
        and context.get("transaction_state") == "ready"
        and context.get("published_transition_complete") is True
    )
    if requested_exit == "ready_for_merge" and not terminal_recovery:
        if re.fullmatch(r"[0-9a-f]{64}", confirmed) is None or confirmed != expected:
            _count(operation_counts, "public.project")
            return _blocked_output(
                owner,
                root,
                "Run preview-finalization again and obtain a new dialogue-local confirmation for the changed plan.",
            )

    if (
        requested_exit == "ready_for_merge"
        and context.get("transaction_state") == "reprepare_required"
    ):
        mapped_review = _mapped_reprepare_review(
            owner,
            root,
            reviewed,
            public_input,
            context,
        )
        mapped_gate, _ = _record_checked_gate(
            owner,
            root,
            public_input,
            mapped_review,
            context,
            operation_counts,
        )
        reprepare_result = owner.execute_finalization_transition_result(
            root,
            args,
            public_input,
            mapped_gate,
            context,
        )
        _count(operation_counts, "transition.execute")
        _count(operation_counts, "mapped.reprepare")
        reprepare_output = _project_output(owner, root, reprepare_result)
        public_input = {
            "profile": "reprepare_preview",
            "mode": public_input["mode"],
            "task_ref": reprepare_output["task_ref"],
            "reason_code": reprepare_output["reason_code"],
            "branch_review_commit": reprepare_output["branch_review_commit"],
            "publication_head": reprepare_output["publication_head"],
        }
        context = owner.finalization_preview_context(root, args, public_input)
        _count(operation_counts, "preview.read")
        if owner.finalization_confirmation_identity(public_input, context) != confirmed:
            _count(operation_counts, "public.project")
            return _blocked_output(
                owner,
                root,
                "The deterministic reprepare changed scope, authority, PR payload, publication mode, or side effects; run a new preview and confirm the new plan.",
            )

    gate, _ = _record_checked_gate(
        owner,
        root,
        public_input,
        reviewed,
        context,
        operation_counts,
    )
    result = owner.execute_finalization_transition_result(
        root,
        args,
        public_input,
        gate,
        context,
    )
    _count(operation_counts, "transition.execute")
    output = _project_output(owner, root, result)
    _count(operation_counts, "public.project")
    if output["exit_id"] == "ready_for_merge" and not result.get(
        "retired_owner_state"
    ):
        task_dir = Path(
            result.get("archived_task_dir")
            or result.get("task_dir")
            or context["task_dir"]
        )
        owner.finalization_retire_current_state(root, task_dir)
        _count(operation_counts, "owner_state.cleanup")
    return output
