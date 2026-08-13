from __future__ import annotations

import argparse
from pathlib import Path

from check import checked_gate
from common import (
    RETIRED_EXITS,
    load,
    parse,
    rel,
    retire_checkpoint,
    root,
    task,
    validate_public_binding,
)
from runtime.io import CommandError
from runtime.schema import validate_json


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--task")
    parser.add_argument("--invocation")
    parser.add_argument("--input")
    args = parse(parser, argv)
    repo = root(package_root, args.root)
    if bool(args.invocation) == bool(args.input):
        raise CommandError(
            "invalid_arguments",
            "invocation",
            "Provide exactly one public input locator or invocation envelope.",
        )
    if args.invocation:
        envelope = load(repo, package_root, args.invocation, "invocation")
        if set(envelope) != {"public_input"} or not isinstance(
            envelope["public_input"], dict
        ):
            raise CommandError(
                "invalid_arguments",
                "invocation",
                "Provide only the public_input invocation member.",
            )
        public = envelope["public_input"]
    else:
        public = load(repo, package_root, args.input, "input")
    task_dir = task(repo, args.task or public.get("task_ref"))
    if public.get("task_ref") != rel(repo, task_dir):
        raise CommandError(
            "stale_identity", "task", "Invoke the exact task-owned checkpoint.", 3
        )
    owner = checked_gate(package_root, repo, task_dir)
    validate_public_binding(package_root, repo, public, owner)
    exit_id = owner["typed_exit"]
    if exit_id == "passed":
        output = {
            "exit_id": exit_id,
            "task_ref": owner["task_dir"],
            "branch_review_commit": owner["review_commit"],
        }
        schema = "public-passed-output.schema.json"
    elif exit_id == "continuity_passed":
        pair = owner["integration_pair"]
        output = {
            "exit_id": exit_id,
            "task_ref": owner["task_dir"],
            "branch_review_commit": owner["review_commit"],
            **{
                key: pair[key]
                for key in (
                    "task_head",
                    "old_base_head",
                    "new_base_head",
                    "candidate_tree_sha256",
                    "resume_target",
                )
            },
        }
        schema = "public-continuity-passed-output.schema.json"
    elif exit_id == "implementation_required":
        output = {
            "exit_id": exit_id,
            "task_ref": owner["task_dir"],
            "branch_review_commit": owner["review_commit"],
            "finding_refs": [
                finding["finding_ref"]
                for finding in owner["semantic_review"]["qualified_findings"]
                if finding["status"] == "open"
            ],
        }
        schema = "public-implementation-required-output.schema.json"
    elif exit_id == "scope_confirmation_required":
        output = {
            "exit_id": exit_id,
            "task_ref": owner["task_dir"],
            "proposal_refs": [
                proposal["proposal_ref"]
                for proposal in owner["semantic_review"]["scope_proposals"]
            ],
        }
        schema = "public-scope-confirmation-required-output.schema.json"
    elif exit_id == "blocked":
        output = {"exit_id": "blocked"}
        schema = "public-blocked-output.schema.json"
    else:
        raise CommandError(
            "schema_mismatch", "typed_exit", "Return one declared typed exit."
        )
    validate_json(output, package_root / "schemas" / schema, "stdout")
    if exit_id in RETIRED_EXITS:
        retire_checkpoint(repo, task_dir)
    return output
