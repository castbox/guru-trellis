"""Objective bindings for this owner's Issue review invocation."""
from __future__ import annotations
import copy
from runtime.io import CommandError
from runtime.schema import validate_json

IDENTITY = ("mode", "issue", "base_source", "continuation_id")

def identity(public):
    return {key: public[key] for key in IDENTITY}

def validate(package, envelope):
    public = envelope["public_input"]
    profile = public["profile"]
    schema = "public-issue-context-request-input-1.0.schema.json" if profile=="context_request" else "public-" + profile.replace("_", "-") + "-input-1.0.schema.json"
    validate_json(public, package / "schemas" / schema, "public_input")
    owner = envelope["owner_result"]
    validate_json(owner, package / "schemas/issue-review-owner-1.0.schema.json", "owner_result")
    if owner["public_input"] != public:
        raise CommandError("stale_identity", "owner_result.public_input", "Rerun this owner for the original Issue, source and continuation.", 3)
    if (owner["typed_exit"] == "blocked") != (owner["ai_review_gate"]["status"] == "blocked"):
        raise CommandError("schema_mismatch", "ai_review_gate.status", "Match the actual blocked judgment and exit.")
    return public, owner


def execute(package, envelope, operation):
    if operation == "invoke":
        validate_json(envelope, package.parents[1] / "consumers/workflow/stage0/invocations/semantic-owner-2.0.schema.json", "invocation")
    public, owner = validate(package, envelope)
    expected_gate = "blocked" if owner["typed_exit"]=="blocked" else "reroute" if owner["typed_exit"]=="requirements_gap" else "passed"
    if owner["ai_review_gate"]["status"] != expected_gate:
        raise CommandError("schema_mismatch", "ai_review_gate.status", "Complete this owner's actual semantic gate before serialization.")
    returning = public.get("return_identity")
    if returning:
        if returning != {"profile":"issue_readiness_supplement", **identity(public), "gap":public["gap"]}:
            raise CommandError("stale_identity", "return_identity", "Return to the original Clarify supplement.", 3)
        if owner["typed_exit"] not in {"context_ready", "blocked"}:
            raise CommandError("schema_mismatch", "typed_exit", "Return requested context to Clarify before Readiness.")
    elif owner["typed_exit"] not in {"supplemented", "blocked"}:
        raise CommandError("schema_mismatch", "typed_exit", "Return the context supplement to Readiness.")
    if operation == "record": return copy.deepcopy(owner)
    if operation == "check": return {"status": "passed", "typed_exit": owner["typed_exit"]}
    output = {"exit_id": owner["typed_exit"]}
    if output["exit_id"] == "context_ready":
        output.update(handoff_profile="issue_readiness_supplement",handoff_mode=public["mode"],handoff_issue=public["issue"],handoff_base_source=public["base_source"],handoff_continuation_id=public["continuation_id"],handoff_gap=public["gap"],context_result=owner["result_summary"],source_refs=owner["source_refs"])
        validate_json(output, package / "schemas/public-issue-context-ready-output-1.0.schema.json", "stdout")
        return output
    if output["exit_id"] != "blocked":
        output.update(identity(public), result_summary=owner["result_summary"], source_refs=owner["source_refs"])
    validate_json(output, package / "schemas" / ("public-supplemented-output-1.0.schema.json" if output["exit_id"] == "supplemented" else "public-blocked-output.schema.json"), "stdout")
    return output
