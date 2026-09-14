from __future__ import annotations
import copy,hashlib,json
from runtime.io import CommandError
from runtime.schema import validate_json

CONSUMERS={"clear":{"kind":"workflow","id":"guru-requirements-clear-router"},"needs_context":{"kind":"skill","id":"guru-discover-change-context"},"refresh_context":{"kind":"skill","id":"guru-sync-base"},"retarget_context":{"kind":"skill","id":"guru-sync-base"},"new_task":{"kind":"workflow","id":"guru-full-task-intake-chain"},"blocked":{"kind":"stop","id":"requirements-clarification-blocked"}}
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def validate_shape(package,payload):
    validate_json(payload,package/"schemas/requirements-clarification.schema.json","input")
    exit_id=payload.get("typed_exit")
    if payload.get("consumer")!=CONSUMERS.get(exit_id): raise CommandError("semantic_result_invalid","input.consumer","Match the declared typed-exit consumer.",3)
    gate=(payload.get("ai_review_gate") or {}).get("status")
    if exit_id=="blocked" and gate!="blocked": raise CommandError("semantic_result_invalid","input.ai_review_gate.status","Blocked requires the AI gate to be blocked.",3)
    if exit_id!="blocked" and gate!="passed": raise CommandError("semantic_result_invalid","input.ai_review_gate.status","A non-blocked exit requires a passed AI gate.",3)
    return payload


IDENTITY_FIELDS = (
    "target_sha256", "disposition_sha256", "content_sha256", "context_sha256",
    "scope_sha256", "action_sha256", "payload_sha256", "result_sha256",
)


def facts_digest(value):
    # Target/proposal bindings retain their existing newline-terminated encoding.
    return hashlib.sha256((json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    ensure_ascii=False) + "\n").encode()).hexdigest()


def derived_slots(payload):
    """Only these owner-local fields may be omitted during authoring."""
    if not isinstance(payload, dict):
        return
    yield payload, "content_identity", {key: "0" * 64 for key in IDENTITY_FIELDS}
    target = payload.get("review_target")
    if isinstance(target, dict):
        yield target, "facts_sha256", "0" * 64
    disposition = payload.get("target_disposition")
    if isinstance(disposition, dict):
        yield disposition, "disposition_digest", "0" * 64
    for collection, fields in (("scope_proposals", ("proposal_digest",)),
                               ("source_actions", ("payload_sha256", "action_digest"))):
        rows = payload.get(collection)
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict):
                    for field in fields:
                        placeholder = None if field == "payload_sha256" and row.get("payload") is None else "0" * 64
                        yield row, field, placeholder


def derive_owner(package, payload, *, authoring=False):
    shape = copy.deepcopy(payload)
    if authoring:
        for row, field, placeholder in derived_slots(shape):
            row.setdefault(field, placeholder)
    # Validate every semantic field before deriving anything. Placeholders are
    # validation-only, never defaults for decisions, evidence, targets or gates.
    validate_shape(package, shape)
    result = copy.deepcopy(payload)

    def bind(row, field, value, path):
        if field in row and row[field] != value:
            raise CommandError("stale_identity", f"{path}.{field}",
                               "Reread current content and repeat recording without stale derived values.", 3)
        row[field] = value

    target = result["review_target"]
    bind(target, "facts_sha256", facts_digest({key: value for key, value in target.items()
                                              if key != "facts_sha256"}), "input.review_target")
    disposition = result["target_disposition"]
    if disposition is not None:
        bind(disposition, "disposition_digest", facts_digest({
            key: value for key, value in disposition.items()
            if key not in {"disposition_digest", "duplicate_facts_sha256"}
        }), "input.target_disposition")
    for index, proposal in enumerate(result["scope_proposals"]):
        bind(proposal, "proposal_digest", facts_digest({key: value for key, value in proposal.items()
                                                       if key != "proposal_digest"}), f"input.scope_proposals.{index}")
    actions = result["source_actions"]
    for index, action in enumerate(actions):
        path = f"input.source_actions.{index}"
        bind(action, "payload_sha256", digest(action["payload"]) if action["payload"] is not None else None, path)
        bind(action, "action_digest", digest({key: action[key] for key in (
            "action_id", "kind", "target", "payload", "preimage_sha256", "payload_sha256"
        )}), path)
    unsigned = {key: value for key, value in result.items() if key != "content_identity"}
    content = {key: result[key] for key in (
        "confirmed_facts", "repository_answerable_questions", "clarification_rounds",
        "open_questions", "affected_contracts", "reason",
    )}
    identity = {
        "target_sha256": digest(target),
        "disposition_sha256": digest(disposition),
        "content_sha256": digest(content),
        "context_sha256": digest(result["context_evidence"]),
        "scope_sha256": digest(result["scope_proposals"]),
        "action_sha256": digest(actions),
        "payload_sha256": digest([action["payload"] for action in actions]),
        "result_sha256": digest(unsigned),
    }
    bind(result, "content_identity", identity, "input")
    validate_shape(package, result)
    return result


def validate_owner(package, payload):
    return derive_owner(package, payload)
