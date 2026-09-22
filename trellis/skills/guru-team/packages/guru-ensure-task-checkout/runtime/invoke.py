from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from runtime.io import CommandError, read_json


def _validate(package_root: Path, schema_name: str, value: dict, field_path: str) -> None:
    schema_path = package_root / "schemas" / schema_name
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda item: list(item.path))
    if errors:
        location = ".".join(str(part) for part in errors[0].path)
        raise CommandError(
            "schema_mismatch",
            f"{field_path}.{location}" if location else field_path,
            "Provide a value matching the declared checkout package schema.",
        )


def _project(value: dict) -> dict:
    exit_id = value["typed_exit"]
    if exit_id == "checkout_ready":
        return {
            "exit_id": exit_id,
            "task_artifact": value["task_artifact"],
            "branch_binding_ref": value["branch_binding_ref"],
            "result_ref": value["result_ref"],
        }
    if exit_id == "resume_checkout_acquisition":
        return {"exit_id": exit_id, "transaction_ref": value["transaction_ref"], "reason": value["reason"]}
    return {"exit_id": "blocked", "reason": value["reason"]}


def _validate_identity(public_input: dict, semantic: dict) -> None:
    profile = public_input["profile"]
    exit_id = semantic["typed_exit"]
    if profile == "ensure_checkout":
        artifact = public_input["task_artifact"]
        binding = public_input["branch_binding_ref"]
        if (artifact["task_id"], artifact["lifecycle_generation"]) != (
            binding["task_id"],
            binding["lifecycle_generation"],
        ):
            raise CommandError(
                "schema_mismatch",
                "input.branch_binding_ref",
                "Use task artifact and branch binding references for the same lifecycle.",
            )
    if exit_id == "checkout_ready":
        if profile != "ensure_checkout":
            raise CommandError("schema_mismatch", "semantic_result.typed_exit", "Use ensure_checkout input for checkout_ready.")
        if semantic["task_artifact"] != public_input["task_artifact"]:
            raise CommandError("schema_mismatch", "semantic_result.task_artifact", "Keep the reviewed task artifact unchanged.")
        if semantic["branch_binding_ref"] != public_input["branch_binding_ref"]:
            raise CommandError("schema_mismatch", "semantic_result.branch_binding_ref", "Keep the reviewed branch binding unchanged.")
        lifecycle = (semantic["task_artifact"]["task_id"], semantic["task_artifact"]["lifecycle_generation"])
        result_lifecycle = (semantic["result_ref"]["task_id"], semantic["result_ref"]["lifecycle_generation"])
        if lifecycle != result_lifecycle:
            raise CommandError("schema_mismatch", "semantic_result.result_ref", "Use a result reference for the reviewed lifecycle.")
    elif exit_id == "resume_checkout_acquisition":
        if profile != "resume_checkout_acquisition":
            raise CommandError("schema_mismatch", "semantic_result.typed_exit", "Use the recovery profile for the resume exit.")
        if semantic["transaction_ref"] != public_input["transaction_ref"]:
            raise CommandError("schema_mismatch", "semantic_result.transaction_ref", "Keep the recovery transaction identity unchanged.")


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Provide --input and --semantic-result once.") from exc
    public_input = read_json(args.input, "input")
    semantic = read_json(args.semantic_result, "semantic_result")
    profile = public_input.get("profile")
    input_schema = {
        "ensure_checkout": "public-ensure-input.schema.json",
        "resume_checkout_acquisition": "public-resume-input.schema.json",
    }.get(profile)
    if input_schema is None:
        raise CommandError("invalid_arguments", "input.profile", "Use one declared checkout input profile.")
    _validate(package_root, input_schema, public_input, "input")
    _validate(package_root, "semantic-result.schema.json", semantic, "semantic_result")
    _validate_identity(public_input, semantic)
    output = _project(semantic)
    output_schema = {
        "checkout_ready": "public-checkout-ready-output.schema.json",
        "resume_checkout_acquisition": "public-resume-output.schema.json",
        "blocked": "public-blocked-output.schema.json",
    }[output["exit_id"]]
    _validate(package_root, output_schema, output, "output")
    return output
