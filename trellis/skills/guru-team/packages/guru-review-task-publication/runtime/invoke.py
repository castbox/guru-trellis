from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

from common import call_owner, parse_arguments
from runtime.io import CommandError
from runtime.schema import validate_json


PUBLIC_INPUT_SCHEMAS = {
    "publication_review": "public-publication-review-input.schema.json",
    "publication_review_stale": "public-publication-review-stale-input.schema.json",
}
PUBLIC_OUTPUT_SCHEMAS = {
    "ready": "public-ready-output-4.0.schema.json",
    "return_to_task_work": "public-return-to-task-work-output.schema.json",
    "blocked": "public-blocked-output.schema.json",
}


def _owner(root: Path):
    spec = importlib.util.spec_from_file_location(
        "publication_owner",
        root / "runtime/owner.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _read_public_input(owner, value: str) -> dict:
    if value == "-":
        return owner.skill_json_loads(sys.stdin.read(), "public input")
    return owner.read_json(Path(value))


def _validate_public_input(package_root: Path, public: dict) -> None:
    profile = public.get("profile")
    schema_name = PUBLIC_INPUT_SCHEMAS.get(profile)
    if schema_name is None:
        raise CommandError(
            "schema_mismatch",
            "input.profile",
            "Use one declared Publication public input profile.",
        )
    validate_json(public, package_root / "schemas" / schema_name, "input")


def _project_output(owner_result: dict) -> dict:
    route = owner_result.get("route")
    exit_id = str(route.get("typed_exit") if isinstance(route, dict) else "")
    if exit_id == "ready":
        pr_payload = owner_result["pr_payload"]
        return {
            "exit_id": exit_id,
            "task_ref": owner_result["task_ref"],
            "branch_review_commit": owner_result["branch_review_commit"],
            "pr_title": pr_payload["title"],
            "pr_body": pr_payload["body"],
        }
    if exit_id == "return_to_task_work":
        return {
            "exit_id": exit_id,
            "task_ref": owner_result["task_ref"],
            "finding_refs": [
                finding["finding_ref"]
                for finding in owner_result["findings"]
                if finding.get("status") == "open"
                and finding.get("route_class") == "task_work"
            ],
            "resume_target": "phase-2",
        }
    if exit_id == "blocked":
        return {
            "exit_id": exit_id,
            "reason_code": route["reason_code"],
            "remediation": route["remediation"],
        }
    raise CommandError(
        "schema_mismatch",
        "owner_result.route.typed_exit",
        "Return one declared Publication typed exit.",
    )


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    args = parse_arguments(parser, argv)
    owner = _owner(package_root)

    def invoke_owner() -> dict:
        root = owner.repo_root(Path(args.root or "."))
        public = _read_public_input(owner, args.input)
        _validate_public_input(package_root, public)
        supplied_owner_result = owner.read_json(Path(args.owner_result))
        task = owner.resolve_task_dir(root, public["task_ref"])
        checked = owner.cmd_check_task_publication_review(
            argparse.Namespace(
                root=str(root),
                task=public["task_ref"],
                expected_exit=None,
            )
        )
        checked_owner_result = checked.get("owner_result")
        if supplied_owner_result != checked_owner_result:
            raise owner.WorkflowError(
                "Publication owner result is not the exact checker-passed result.",
                exit_code=2,
                payload={
                    "error_code": "publication_freshness_failed",
                    "field_path": "publication.owner_result",
                    "recovery": "Re-run the Publication checker and invoke with its exact current result.",
                },
            )
        if (
            checked_owner_result.get("task_ref") != public["task_ref"]
            or checked_owner_result.get("branch_review_commit")
            != public["branch_review_commit"]
        ):
            raise owner.WorkflowError(
                "Publication public input does not match the checker-passed owner result.",
                exit_code=2,
                payload={
                    "error_code": "publication_input_invalid",
                    "field_path": "input.branch_review_commit",
                    "recovery": "Use the task and reviewed commit from the checker-passed Publication result.",
                },
            )

        output = _project_output(checked_owner_result)
        validate_json(
            output,
            package_root / "schemas" / PUBLIC_OUTPUT_SCHEMAS[output["exit_id"]],
            "stdout",
        )

        checkpoint = owner.task_publication_path(root, task)
        if not checkpoint.is_file() or checkpoint.is_symlink():
            raise owner.WorkflowError(
                "Publication checkpoint disappeared before successful consumption.",
                exit_code=2,
            )
        checkpoint.unlink()
        try:
            checkpoint.parent.rmdir()
        except OSError:
            pass
        return output

    return call_owner(owner, invoke_owner)
