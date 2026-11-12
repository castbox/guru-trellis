"""Factual bindings for the two qualification-confirmation continuations."""
from __future__ import annotations

import hashlib
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.qualification_facts import confirmation_source

CONFIRMATION_PROFILES = frozenset({"normal_scenario_scope_confirmation", "solution_mechanism_scope_confirmation"})

def confirmation_identity(value):
    return {key: value[key] for key in ("profile", "target_locator", "continuation_id", "resume_target", "candidate_refs", "task_ref", "delivery_key") if key in value}




def validate_actions(owner):
    if owner.get("invocation_context", {}).get("kind") not in CONFIRMATION_PROFILES:
        return
    actions = {row["action_id"]: row for row in owner["source_actions"] if row["kind"] != "none"}
    results = {row["action_id"]: row for row in owner["mutation_results"]}
    for round_ in owner["clarification_rounds"]:
        if round_["authority_impact"] == "load_bearing":
            ids = round_["authority_action_ids"]
            if not ids or any(key not in actions for key in ids) or owner["typed_exit"] != "refresh_context":
                raise CommandError("semantic_result_invalid", "clarification_rounds.authority_action_ids", "Record the completed authority action and return through context refresh.", 3)
    for key, action in actions.items():
        if owner["typed_exit"] != "refresh_context" or owner["target_disposition"] is None:
            raise CommandError("semantic_result_invalid", "source_actions", "An authority mutation requires its current disposition and context refresh.", 3)
        result = results.get(key)
        if action["kind"] not in {"issue_comment", "issue_body_edit", "proposed_draft_update"} or action["status"] not in {"executed", "validated"}:
            raise CommandError("semantic_result_invalid", "source_actions", "Use the completed source action for this confirmation authority.", 3)
        body = hashlib.sha256(action["payload"]["body"].encode()).hexdigest()
        if not result or result["kind"] != action["kind"] or result["action_digest"] != action["action_digest"] or result["content_sha256"] != body:
            raise CommandError("stale_identity", "mutation_results", "Match the completed action payload and its live reread result.", 3)
        target = owner["review_target"]
        if action["preimage_sha256"] != target["body_sha256"]:
            raise CommandError("stale_identity", "source_actions.preimage_sha256", "Use the reviewed authority preimage for the completed action.", 3)
        if target["kind"] == "issue":
            url_matches = (result["url"] == target["url"] if action["kind"] == "issue_body_edit"
                           else result["url"].startswith(target["url"] + "#issuecomment-"))
            if action["target"] != {"repo": target["repo"], "issue_number": target["issue_number"]} or not url_matches:
                raise CommandError("stale_identity", "source_actions.target", "Mutate only the reviewed source Issue.", 3)


def bind_confirmation(package, public, transition, owner):
    identity = confirmation_identity(public)
    context = owner["invocation_context"]
    for key, value in identity.items():
        other = context.get("kind") if key == "profile" else context.get(key)
        if other != value:
            raise CommandError("stale_identity", "invocation_context." + key, "Preserve the original qualification object and continuation.", 3)
    if context.get("task_locator") != public.get("task_ref"):
        raise CommandError("stale_identity", "invocation_context.task_locator", "Preserve the original Task reference or null for a non-Task confirmation.", 3)
    authority = confirmation_source(Path((transition or {}).get("repo_locator") or ".").resolve(), identity)["locator"]
    if owner["typed_exit"] == "blocked":
        return
    missing = owner["typed_exit"] == "needs_context"
    if not isinstance(transition, dict):
        raise CommandError("stale_identity", "transition", "Obtain the original Sync baseline before requesting confirmation context.", 3)
    if missing and transition.get("stage") == "base_current":
        validate_json(transition, package.parents[1] / "consumers/workflow/stage0/transitions/base-current-2.0.schema.json", "transition")
        return
    validate_json(transition, package.parents[1] / "consumers/workflow/stage0/transitions/context-current-4.0.schema.json", "transition")
    expected = {**identity, "clarify_profile": identity["profile"]}
    expected.pop("profile")
    for key, value in expected.items():
        if transition.get(key) != value:
            raise CommandError("stale_identity", "transition." + key, "Obtain current context for this exact qualification continuation.", 3)
    if transition.get("authority_locator") != authority:
        raise CommandError("stale_identity", "transition.authority_locator", "Reread the actual source relation through the original context producer.", 3)
    target = owner["review_target"]
    if target["kind"] == "issue" and target["url"] != authority:
        raise CommandError("stale_identity", "review_target.url", "Review the actual source Issue separately from the Task target.", 3)
    if not missing and transition["authority_content_sha256"] != target["body_sha256"]:
        raise CommandError("stale_identity", "transition.authority_content_sha256", "The authority changed. Request fresh context through the original producer.", 3)
    if owner["typed_exit"] == "clear" and target["state"] == "closed":
        raise CommandError("stale_identity", "review_target.state", "Resolve the closed source through its original owner.", 3)
    snapshot = public.get("authority_duplicate_snapshot")
    if snapshot is not None and (snapshot["target_locator"] != authority or snapshot["authority_content_sha256"] != transition["authority_content_sha256"]):
        raise CommandError("stale_identity", "authority_duplicate_snapshot", "Obtain the current authority snapshot from Discovery.", 3)
    disposition = owner["target_disposition"]
    if disposition is not None and "delivery_key" in public and disposition["disposition"] not in {"keep_current_open_issue", "keep_current_draft"}:
        raise CommandError("semantic_result_invalid", "target_disposition", "Return a Task source change to its original source/scope owner.", 3)
    if "delivery_key" in public and target["kind"] == "draft" and any(row["kind"] != "none" for row in owner["source_actions"]):
        raise CommandError("semantic_result_invalid", "source_actions", "Return accepted no-Issue scope changes to the whole-scope owner.", 3)
    if disposition is not None and not missing:
        if snapshot is None:
            raise CommandError("stale_identity", "authority_duplicate_snapshot", "Request Discovery context before deciding authority disposition.", 3)
        rows = disposition["duplicate_candidates"]
        expected_candidates = [{**item, "identity": f"#{item['number']}", "state": "open",
                                "decision": next((r["decision"] for r in rows if r["repo"] == item["repo"] and r["number"] == item["number"]), None),
                                "reason": next((r["reason"] for r in rows if r["repo"] == item["repo"] and r["number"] == item["number"]), None)} for item in snapshot["candidates"]]
        if (rows != expected_candidates or disposition["duplicate_query"] != snapshot["query"] or
            disposition["duplicate_checked_at"] != snapshot["checked_at"] or disposition["duplicate_facts_sha256"] != snapshot["facts_sha256"]):
            raise CommandError("stale_identity", "target_disposition", "Use the actual Discovery authority facts for this disposition.", 3)
