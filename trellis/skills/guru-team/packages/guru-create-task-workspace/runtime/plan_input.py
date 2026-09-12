"""Package-owned, call-local preparation; semantic decisions stay with the caller."""
from __future__ import annotations

import copy

from common import digest, now, plan_digest, reviewable, validate, validate_schema
from runtime.io import CommandError


def object_field(envelope, name):
    value = envelope.get(name)
    if not isinstance(value, dict):
        raise CommandError(
            "schema_mismatch", f"invocation.{name}",
            f"Provide an object at invocation.{name}; a bare plan is not an invocation envelope.",
        )
    return value


def validate_transition(package_root, transition):
    # Both canonical and installed packages keep the consumer beside packages/.
    path = package_root.parents[1] / "consumers/workflow/stage0/transitions/readiness-current.schema.json"
    validate_schema(transition, path, "invocation.transition")
    pairs = (
        (transition["context_result_sha256"], transition["context_result_sha256"]),
        (transition["clarity_result_sha256"], transition["clarity"]["facts_sha256"]),
        (transition["wording_facts_sha256"], transition["wording"]["facts_sha256"]),
        (transition["readiness_facts_sha256"], transition["readiness"]["facts_sha256"]),
        (transition["readiness_linkage_sha256"], transition["readiness"]["linkage_sha256"]),
        (transition["target_content_sha256"], transition["target"]["content_sha256"]),
        (transition["target_content_sha256"], transition["readiness"]["content_sha256"]),
        (transition["target_content_sha256"], transition["wording"]["target_content_sha256"]),
    )
    fields = ("context_result_sha256", "clarity_result_sha256", "wording_facts_sha256", "readiness_facts_sha256", "readiness_linkage_sha256", "target.content_sha256", "readiness.content_sha256", "wording.target_content_sha256")
    for field, (left, right) in zip(fields, pairs):
        if left != right:
            raise CommandError("stale_identity", f"invocation.transition.{field}", "Use the corresponding same-source identity from the current readiness_current output.", 3)
    return transition


def prerequisite(key, projection, facts, content=None, linkage=None):
    owner, schema, exit_id = {
        "base": ("guru-sync-base", "guru-stage0-transition-base-current-1.0", "synced"),
        "discovery": ("guru-discover-change-context", "guru-stage0-transition-context-current-1.0", "context_ready"),
        "clarity": ("guru-clarify-requirements", "guru-requirements-clarification-2.0", "clear"),
        "wording": ("guru-review-contract-wording", "guru-contract-wording-review-1.0", "pass"),
        "readiness": ("guru-review-change-request", "guru-change-request-review-2.0", "ready"),
    }[key]
    return {
        "skill_id": owner, "schema_id": schema, "typed_exit": exit_id,
        "artifact": f"call-local:{key}", "payload_sha256": digest(projection),
        "facts_sha256": facts, "content_sha256": content, "linkage_sha256": linkage,
    }


def prepare_plan(package_root, envelope):
    validate(package_root, envelope, "record-authoring-input.schema.json", "invocation")
    transition = validate_transition(package_root, envelope["transition"])
    target = transition["target"]
    if target["kind"] != "existing_issue":
        raise CommandError("invalid_arguments", "invocation.transition.target.kind", "Authoring supports ordinary existing issues only. Use the complete-plan compatibility input for a reviewed draft or created-issue provenance.")
    authoring = copy.deepcopy(envelope["authoring"])
    scope = authoring["scope"]
    primary = scope["primary"]
    if primary["number"] != target["issue_number"] or primary["url"] != target["url"]:
        raise CommandError("stale_identity", "invocation.authoring.scope.primary", "Keep the current readiness target as the primary issue.", 3)
    for key in ("close", "related", "followup"):
        numbers = [row["number"] for row in scope[key]]
        if len(numbers) != len(set(numbers)) or set(numbers) != set(transition["scope"][f"{key}_issues"]):
            raise CommandError("stale_identity", f"invocation.authoring.scope.{key}", "Preserve the readiness issue set and provide one detail row per issue.", 3)
    scope["scope_sha256"] = digest(scope)
    base = transition["base"]
    base_projection = {
        "schema_version": "1.0", "transition_id": "base_current:" + base["post_sync_resolution_sha256"][:24],
        "stage": "base_current", "mode": transition["mode"],
        "repo_locator": transition["repo_locator"], "base": copy.deepcopy(base),
    }
    clarity, wording, readiness = (transition[key] for key in ("clarity", "wording", "readiness"))
    captured = now()
    plan = {
        "schema_version": "2.0", "skill_id": "guru-create-task-workspace",
        "generated_at": captured, "mode": transition["mode"],
        "invocation": {"caller": "guru-review-change-request:ready", "target_kind": "existing_issue", "action_scope": "workspace_and_task_mutation", "resume_identity": transition["continuation_id"]},
        "prerequisites": {
            "base": prerequisite("base", base_projection, digest(base_projection)),
            "discovery": prerequisite("discovery", {"context_result_sha256": transition["context_result_sha256"]}, transition["context_result_sha256"]),
            "clarity": prerequisite("clarity", clarity, clarity["facts_sha256"], clarity["content_sha256"], clarity["content_sha256"]),
            "wording": prerequisite("wording", wording, wording["facts_sha256"], wording["scope_sha256"], wording["scan_sha256"]),
            "readiness": prerequisite("readiness", readiness, readiness["facts_sha256"], readiness["content_sha256"], readiness["linkage_sha256"]),
        },
        "target": {
            **{key: target[key] for key in ("kind", "repo", "issue_number", "url", "updated_at", "title_sha256", "body_sha256")},
            "state": "open", "draft": None,
            "disposition_sha256": transition["target_disposition"]["disposition_sha256"],
            "duplicate_decision_sha256": transition["target_disposition"]["duplicate_facts_sha256"],
            "created_issue_binding_sha256": None, "created_issue_result": None,
        },
        "scope": scope,
        "base": {
            "selected_base": base["selected_base"], "remote": base["remote"],
            "base_ref": f"refs/remotes/{base['remote']}/{base['selected_base']}",
            "decision_head": base["decision_head"], "local_head": base["local_base_head"], "remote_head": base["remote_base_head"],
            "post_sync_resolution_sha256": base["post_sync_resolution_sha256"], "sync_facts_sha256": digest(base_projection),
        },
        **{key: authoring[key] for key in ("naming", "assignee", "side_effects", "ai_review_gate")},
        "freshness": {"captured_at": captured},
    }
    reviewed = digest(reviewable(plan))
    plan["ai_review_gate"]["reviewed_plan_sha256"] = reviewed
    plan["freshness"]["reviewable_plan_sha256"] = reviewed
    plan["freshness"]["plan_sha256"] = plan_digest(plan)
    return plan


def load_plan_envelope(package_root, envelope, *, allow_authoring=False):
    if "authoring" in envelope:
        if "plan" in envelope:
            raise CommandError("conflicting_arguments", "invocation.authoring", "Provide authoring or plan, never both.")
        if not allow_authoring:
            raise CommandError("invalid_arguments", "invocation.plan", "Run record-task-workspace-plan first, then put its complete stdout plan at invocation.plan.")
        return prepare_plan(package_root, envelope)
    return object_field(envelope, "plan")
