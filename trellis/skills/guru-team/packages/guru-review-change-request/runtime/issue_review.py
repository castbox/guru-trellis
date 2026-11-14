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
    from common import DIMENSIONS, digest, live_issue_source
    public, owner = validate(package, envelope)
    source = envelope.get("owner_context", {}).get("change_request")
    if not isinstance(source, dict) or source.get("kind") != "issue" or source.get("repo") != public["issue"]["repo_ref"] or source.get("number") != public["issue"]["number"]:
        raise CommandError("stale_identity", "owner_context.change_request", "Read the same live Issue.", 3)
    if [row["id"] for row in owner["dimensions"]] != list(DIMENSIONS):
        raise CommandError("schema_mismatch", "dimensions", "Review all ten original readiness dimensions in order.")
    exit_id = owner["typed_exit"]
    if exit_id.startswith("supplement_") and not owner.get("gap"):
        raise CommandError("schema_mismatch", "gap", "Describe the actual earliest missing coverage.")
    expected = "passed" if exit_id == "ready" else "blocked" if exit_id == "blocked" else "reroute"
    if owner["ai_review_gate"]["status"] != expected:
        raise CommandError("schema_mismatch", "ai_review_gate.status", "Use the completed semantic gate for the selected exit.")
    # The adjacent check receipt binds supplied bytes only. It is not authority
    # for readiness or a public cross-Skill freshness token.
    receipt = {"result_sha256": digest(owner), "input_sha256": digest(public), "source_sha256": digest(source)}
    if operation == "record":
        return copy.deepcopy(owner)
    if operation == "check":
        live_issue_source(source)
        return {"status": "passed", "validation_receipt": receipt}
    if envelope.get("validation_receipt") != receipt:
        raise CommandError("stale_identity", "validation_receipt", "Run the original readiness check for these current bytes.", 3)
    output = {"exit_id": exit_id}
    if exit_id != "blocked":
        output.update(identity(public))
        if exit_id == "ready": output["source_selection"] = owner["source_selection"]
        if exit_id.startswith("supplement_"): output["gap"] = owner["gap"]
    name = "public-issue-ready-output-1.0" if exit_id == "ready" else "public-" + exit_id.replace("_", "-") + "-output-1.0"
    if exit_id == "blocked": name = "public-blocked-output"
    validate_json(output, package / "schemas" / (name + ".schema.json"), "stdout")
    return output
