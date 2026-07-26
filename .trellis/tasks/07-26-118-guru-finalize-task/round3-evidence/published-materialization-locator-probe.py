#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import tempfile
from pathlib import Path
from unittest import mock


REPO = Path(__file__).resolve().parents[4]
RUNTIME = REPO / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py"
PACKAGE = REPO / "trellis/skills/guru-team/packages/guru-finalize-task"


def load_runtime():
    spec = importlib.util.spec_from_file_location("gtt_round3_published_probe", RUNTIME)
    if spec is None or spec.loader is None:
        raise RuntimeError("runtime import spec is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    runtime = load_runtime()
    results: dict[str, object] = {}

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        active_ref = ".trellis/tasks/07-26-normal-finalization"
        archive_ref = ".trellis/tasks/archive/2026-07/07-26-normal-finalization"
        active = root / active_ref
        archive = root / archive_ref
        active.mkdir(parents=True)
        runtime.write_json(
            active / "task.json",
            {
                "id": "07-26-normal-finalization",
                "name": "07-26-normal-finalization",
                "title": "Normal finalization probe",
                "status": "in_progress",
                "branch": "feat/118",
                "base_branch": "main",
            },
        )

        reviewed_head = "a" * 40
        plan_ref = "closeout-plan:" + "b" * 64
        public_input = {
            "profile": "verification_verified",
            "mode": "workflow",
            "task_ref": active_ref,
            "plan_ref": plan_ref,
            "reviewed_head": reviewed_head,
            "verification_ref": "extension-verification:current",
            "reentry_intent": "Continue the same reviewed finalization plan.",
        }
        context = {
            "task_dir": active,
            "transaction_state": "evidence_pushed",
            "publication_status": "current",
            "publication_stale_reason": None,
            "plan_ref": plan_ref,
            "plan": {
                "git": {
                    "repo": "castbox/guru-trellis",
                    "reviewed_work_head": reviewed_head,
                },
                "marketplace": {"required": True},
                "task": {
                    "active_locator": active_ref,
                    "archive_locator": archive_ref,
                },
            },
            "verification": ({}, {"typed_exit": "verified"}),
        }
        public_output = {
            "exit_id": "published",
            "task_ref": active_ref,
            "pr_number": 118,
            "pr_url": "https://github.com/castbox/guru-trellis/pull/118",
        }
        early_gate = {
            "route": {
                "typed_exit": "published",
                "consumer": runtime.FINALIZATION_CONSUMERS["published"],
                "output": public_output,
            }
        }

        def invoke_checked_gate(
            checked_input: dict[str, object],
            checked_context: dict[str, object],
            checked_gate: dict[str, object],
        ) -> tuple[dict[str, object], int]:
            executor = mock.Mock(
                side_effect=AssertionError(
                    "public wrapper must not execute transition implicitly"
                )
            )
            with (
                mock.patch.object(
                    runtime,
                    "stage0_invocation_identity",
                    return_value=(runtime.FINALIZE_TASK_SKILL_ID, PACKAGE),
                ),
                mock.patch.object(
                    runtime,
                    "stage0_public_interface",
                    return_value=runtime.read_json(PACKAGE / "interface.json"),
                ),
                mock.patch.object(runtime, "stage0_repo_root", return_value=root),
                mock.patch.object(
                    runtime,
                    "stage0_structured_input",
                    return_value=checked_input,
                ),
                mock.patch.object(
                    runtime,
                    "finalization_gate_input",
                    return_value=(
                        checked_gate,
                        active / "task-finalization-gate.json",
                    ),
                ),
                mock.patch.object(
                    runtime,
                    "check_finalization_gate_result",
                    return_value=(checked_gate, checked_context),
                ),
                mock.patch.object(
                    runtime,
                    "cmd_execute_finalization_transition",
                    executor,
                ),
            ):
                emitted = runtime.cmd_invoke_stage0_skill(
                    argparse.Namespace(input="unused.json", owner_result=None)
                )
            return emitted, executor.call_count

        with mock.patch.object(
            runtime,
            "finalization_package_root",
            return_value=PACKAGE,
        ):
            runtime.finalization_validate_route(
                root,
                public_input,
                context,
                early_gate["route"],
            )
        emitted, executor_call_count = invoke_checked_gate(
            public_input,
            context,
            early_gate,
        )
        results["early_public_dto"] = {
            "transaction_state": context["transaction_state"],
            "route_accepted": True,
            "emitted_exit": emitted["exit_id"],
            "executor_call_count": executor_call_count,
        }

        publication_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": active_ref,
            "reviewed_head": reviewed_head,
            "publication_ref": "publication:current",
            "finalization_intent": "Finalize the reviewed task.",
        }
        prepared_context = copy.deepcopy(context)
        prepared_context["transaction_state"] = "prepared"
        prepared_context["verification"] = None
        verification_gate = {
            "route": {
                "typed_exit": "verification_required",
                "consumer": runtime.FINALIZATION_CONSUMERS[
                    "verification_required"
                ],
                "output": {
                    "exit_id": "verification_required",
                    "task_ref": active_ref,
                    "plan_ref": plan_ref,
                    "repo_ref": "other/repository",
                    "reviewed_head": reviewed_head,
                    "verification_target": "extension-installation",
                },
            }
        }
        with mock.patch.object(
            runtime,
            "finalization_package_root",
            return_value=PACKAGE,
        ):
            runtime.finalization_validate_route(
                root,
                publication_input,
                prepared_context,
                verification_gate["route"],
            )
        verification_emitted, verification_executor_calls = invoke_checked_gate(
            publication_input,
            prepared_context,
            verification_gate,
        )
        results["prepared_verification_required"] = {
            "transaction_state": prepared_context["transaction_state"],
            "route_accepted": True,
            "emitted_exit": verification_emitted["exit_id"],
            "emitted_repo_ref": verification_emitted["repo_ref"],
            "plan_repo_ref": prepared_context["plan"]["git"]["repo"],
            "executor_call_count": verification_executor_calls,
        }

        resume_gate = {
            "route": {
                "typed_exit": "resume_finalization",
                "consumer": runtime.FINALIZATION_CONSUMERS[
                    "resume_finalization"
                ],
                "output": {
                    "exit_id": "resume_finalization",
                    "task_ref": active_ref,
                    "plan_ref": plan_ref,
                },
            }
        }
        with mock.patch.object(
            runtime,
            "finalization_package_root",
            return_value=PACKAGE,
        ):
            runtime.finalization_validate_route(
                root,
                publication_input,
                prepared_context,
                resume_gate["route"],
            )
        results["prepared_resume_finalization"] = {
            "transaction_state": prepared_context["transaction_state"],
            "route_accepted": True,
        }

        marker_gate = copy.deepcopy(early_gate)
        marker_gate["route"]["output"] = runtime.FINALIZATION_EXECUTOR_OUTPUT_MARKER
        with mock.patch.object(
            runtime,
            "finalization_package_root",
            return_value=PACKAGE,
        ):
            materialized = runtime.finalization_gate_with_published_output(
                root,
                active,
                marker_gate,
                context["plan"],
                {
                    "number": 118,
                    "url": "https://github.com/castbox/guru-trellis/pull/118",
                },
            )
        archive.parent.mkdir(parents=True)
        active.rename(archive)
        locator_error = None
        try:
            runtime.finalization_task_dir(root, public_input)
        except runtime.WorkflowError as exc:
            locator_error = str(exc)
        results["post_archive_locator"] = {
            "materialized_task_ref": materialized["route"]["output"]["task_ref"],
            "active_exists": active.exists(),
            "archive_exists": archive.exists(),
            "resolved_archive_ref": runtime.repo_relative(
                root,
                runtime.resolve_finish_work_task_dir(root, public_input["task_ref"]),
            ),
            "finalization_task_dir_status": "blocked" if locator_error else "passed",
            "message": locator_error,
            "public_example_task_ref": json.loads(
                (PACKAGE / "examples/public-published-output.json").read_text(
                    encoding="utf-8"
                )
            )["task_ref"],
        }

    print(json.dumps(results, indent=2, sort_keys=True))
    if results["early_public_dto"] != {
        "transaction_state": "evidence_pushed",
        "route_accepted": True,
        "emitted_exit": "published",
        "executor_call_count": 0,
    }:
        return 2
    if results["prepared_verification_required"] != {
        "transaction_state": "prepared",
        "route_accepted": True,
        "emitted_exit": "verification_required",
        "emitted_repo_ref": "other/repository",
        "plan_repo_ref": "castbox/guru-trellis",
        "executor_call_count": 0,
    }:
        return 3
    if results["prepared_resume_finalization"] != {
        "transaction_state": "prepared",
        "route_accepted": True,
    }:
        return 4
    post_archive = results["post_archive_locator"]
    if not isinstance(post_archive, dict):
        return 5
    if (
        post_archive["materialized_task_ref"] != active_ref
        or post_archive["active_exists"] is not False
        or post_archive["archive_exists"] is not True
        or post_archive["resolved_archive_ref"] != archive_ref
        or post_archive["finalization_task_dir_status"] != "blocked"
    ):
        return 6
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
