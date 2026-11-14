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
    schema = "public-" + profile.replace("_", "-") + "-input-1.0.schema.json"
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
    from common import validate_result, check_receipt
    public, owner = validate(package, envelope)
    expected_gate = "blocked" if owner["typed_exit"]=="blocked" else "reroute" if owner["typed_exit"]=="requirements_gap" else "passed"
    if owner["ai_review_gate"]["status"] != expected_gate:
        raise CommandError("schema_mismatch", "ai_review_gate.status", "Complete this owner's actual semantic gate before serialization.")
    wording = validate_result(package, owner["wording_review"])
    locator = f"https://github.com/{public['issue']['repo_ref']}/issues/{public['issue']['number']}"
    if wording["profile"] != "change_request" or wording["mode"] != public["mode"] or wording["scope"]["identity"] != "change_request:" + locator:
        raise CommandError("stale_identity", "wording_review.scope", "Run the original complete title/body wording scanner for this Issue.", 3)
    check_receipt(wording, envelope.get("validation_receipt"))
    if owner["typed_exit"] == "supplemented" and wording["typed_exit"] != "pass":
        raise CommandError("schema_mismatch", "wording_review.typed_exit", "Only actual wording pass completes a supplement; changed content must be reread and reviewed.")
    if operation == "record": return copy.deepcopy(owner)
    if operation == "check": return {"status": "passed", "typed_exit": owner["typed_exit"]}
    output = {"exit_id": owner["typed_exit"]}
    if output["exit_id"] != "blocked":
        output.update(identity(public), source_refs=owner["source_refs"])
        if output["exit_id"] == "supplemented": output["result_summary"] = owner["result_summary"]
        else: output["gap"] = owner.get("gap", "")
    name = "public-" + output["exit_id"].replace("_", "-") + "-output-1.0.schema.json"
    if output["exit_id"] == "blocked": name = "public-blocked-output.schema.json"
    validate_json(output, package / "schemas" / name, "stdout")
    return output
