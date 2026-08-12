from __future__ import annotations
import hashlib,json
from runtime.io import CommandError
from runtime.schema import validate_json

CONSUMERS={"clear":{"kind":"workflow","id":"guru-requirements-clear-router"},"needs_context":{"kind":"skill","id":"guru-discover-change-context"},"refresh_context":{"kind":"skill","id":"guru-sync-base"},"retarget_context":{"kind":"skill","id":"guru-sync-base"},"new_task":{"kind":"workflow","id":"guru-full-task-intake-chain"},"blocked":{"kind":"stop","id":"requirements-clarification-blocked"}}
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def validate_owner(package,payload):
    validate_json(payload,package/"schemas/requirements-clarification.schema.json","input")
    exit_id=payload.get("typed_exit")
    if payload.get("consumer")!=CONSUMERS.get(exit_id): raise CommandError("semantic_result_invalid","input.consumer","Match the declared typed-exit consumer.",3)
    gate=(payload.get("ai_review_gate") or {}).get("status")
    if exit_id=="blocked" and gate!="blocked": raise CommandError("semantic_result_invalid","input.ai_review_gate.status","Blocked requires the AI gate to be blocked.",3)
    if exit_id!="blocked" and gate!="passed": raise CommandError("semantic_result_invalid","input.ai_review_gate.status","A non-blocked exit requires a passed AI gate.",3)
    return payload
