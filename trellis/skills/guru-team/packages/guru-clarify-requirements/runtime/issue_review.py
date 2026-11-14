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


def local_clarification(package, authored, *, authoring=False):
    from common import digest, facts_digest
    value = copy.deepcopy(authored)
    shape = copy.deepcopy(value)
    if authoring:
        shape.get("review_target", {}).setdefault("facts_sha256", "0" * 64)
        for proposal in shape.get("scope_proposals", []):
            proposal.setdefault("proposal_digest", "0" * 64)
        for action in shape.get("source_actions", []):
            action.setdefault("payload_sha256", None if action.get("payload") is None else "0" * 64)
            action.setdefault("action_digest", "0" * 64)
    validate_json(shape, package / "schemas/issue-clarification-1.0.schema.json", "clarification")
    def bind(row, key, expected):
        if key in row and row[key] != expected:
            raise CommandError("stale_identity", "clarification." + key, "Reread current local content and record its actual facts.", 3)
        row[key] = expected
    target = value["review_target"]
    bind(target, "facts_sha256", facts_digest({k:v for k,v in target.items() if k!="facts_sha256"}))
    for proposal in value["scope_proposals"]:
        bind(proposal,"proposal_digest",facts_digest({k:v for k,v in proposal.items() if k!="proposal_digest"}))
    for action in value["source_actions"]:
        bind(action,"payload_sha256",digest(action["payload"]) if action["payload"] is not None else None)
        bind(action,"action_digest",digest({k:action[k] for k in ("action_id","kind","target","payload","preimage_sha256","payload_sha256")}))
    validate_json(value, package / "schemas/issue-clarification-1.0.schema.json", "clarification")
    from confirmation import validate_issue_actions
    validate_issue_actions(value)
    return value


def execute(package, envelope, operation):
    if operation == "invoke":
        validate_json(envelope, package.parents[1] / "consumers/workflow/stage0/invocations/semantic-owner-2.0.schema.json", "invocation")
    if operation == "record":
        envelope = copy.deepcopy(envelope)
        envelope["owner_result"]["clarification"] = local_clarification(package, envelope["owner_result"]["clarification"], authoring=True)
    public, owner = validate(package, envelope)
    expected_gate = "blocked" if owner["typed_exit"]=="blocked" else "reroute" if owner["typed_exit"]=="requirements_gap" else "passed"
    if owner["ai_review_gate"]["status"] != expected_gate:
        raise CommandError("schema_mismatch", "ai_review_gate.status", "Complete this owner's actual semantic gate before serialization.")
    clarification = local_clarification(package, owner["clarification"])
    target = clarification["review_target"]
    if target["kind"] != "issue" or target["repo"] != public["issue"]["repo_ref"] or target["issue_number"] != public["issue"]["number"] or clarification["mode"] != public["mode"]:
        raise CommandError("stale_identity", "clarification.review_target", "Review the original Issue in the same mode.", 3)
    if owner["source_selection"] != clarification["source_selection"]:
        raise CommandError("stale_identity", "source_selection", "Use this Clarify owner's actual source selection.", 3)
    expected = {"clear": "supplemented", "refresh_context": "supplemented", "needs_context": "needs_context", "blocked": "blocked"}.get(clarification["typed_exit"])
    if owner["typed_exit"] != expected:
        raise CommandError("schema_mismatch", "typed_exit", "Preserve the actual clarification result or return target changes to full Intake.")
    if operation == "record":
        value = copy.deepcopy(owner); value["clarification"] = clarification; return value
    if operation == "check":
        from confirmation import check_live_issue_actions
        check_live_issue_actions(clarification)
        return {"status": "passed", "typed_exit": owner["typed_exit"]}
    output = {"exit_id": owner["typed_exit"]}
    if output["exit_id"] == "supplemented":
        output.update(identity(public), result_summary=owner["result_summary"], source_refs=owner["source_refs"], source_selection=owner["source_selection"])
        name = "public-supplemented-output-1.0.schema.json"
    elif output["exit_id"] == "needs_context":
        output.update(handoff_profile="context_request", handoff_mode=public["mode"], issue=public["issue"], base_source=public["base_source"], handoff_continuation_id=public["continuation_id"], gap=public["gap"], return_identity={"profile":"issue_readiness_supplement", **identity(public), "gap":public["gap"]})
        name = "public-issue-needs-context-output-1.0.schema.json"
    else: name = "public-blocked-output.schema.json"
    validate_json(output, package / "schemas" / name, "stdout")
    return output
