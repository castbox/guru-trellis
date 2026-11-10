"""Delivery-scoped Check recorder/validator; the AI still owns all judgments."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from common import content_identity, skill_content_identity, dirty_paths, git, validate_candidate_classifications
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.delivery_projection.gates import record_gate, rework
from runtime.io import CommandError
from runtime.reviewed_content import ReviewedContentError, reviewed_content_identity, reviewed_content_metadata_path
from runtime.schema import validate_json
from runtime.task_lifecycle.active_checkout import resolve_active_task_checkout
from runtime.task_lifecycle.errors import LifecycleContractError


def _identity_binding(projection, public):
    try:
        resolve_active_task_checkout(projection.root, public["task_ref"])
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    key = public["delivery_key"]
    return projection.resolve(key)


def _current_delivery(projection, public):
    delivery = _identity_binding(projection, public)
    key = public["delivery_key"]
    current = projection.current(key)
    if current.get("kind") != "current" or current.get("key") != key:
        raise CommandError("stale_identity", "delivery_key", "Resolve this same Delivery through the original identity/selection owner.", 3)
    return delivery


def _candidate_binding(projection, delivery):
    try:
        projection._call(projection.api.delivery_store.verify_candidate, projection.root, delivery["candidate"])
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    if delivery["candidate"]["head_ref"] != git(projection.root, "rev-parse", "HEAD"):
        raise CommandError("stale_identity", "candidate.head_ref", "Begin Check for the actual current candidate.", 3)
    return delivery



def _binding(projection, public):
    delivery = _identity_binding(projection, public)
    planning = delivery["results"]["planning"]
    if planning is None or planning["result_id"] != public["planning_accepted_result_id"]:
        raise CommandError("stale_identity", "planning_accepted_result_id", "Consume the current public Planning result.", 3)
    if projection.gate_applicability(public["delivery_key"])["planning"]["kind"] != "applicable":
        raise CommandError("stale_identity", "planning", "Reenter the affected Planning owner.", 3)
    _candidate_binding(projection, delivery)
    return delivery


def planning_stale_output(public, owner):
    changes = [row["id"] for row in owner["semantic_review"]["scope_decisions"]
               if row["disposition"] == "scope_change_required"]
    output = {"exit_id": "planning_stale", "task_ref": public["task_ref"],
              "delivery_key": public["delivery_key"], "planning_route": owner["route"],
              "proposal_refs": []}
    if owner["route"] == "reapprove_plan":
        if changes:
            raise CommandError("schema_mismatch", "route", "Return real scope changes to original Clarify; reapprove_plan carries only current-scope repair actions.")
        output["revision_actions"] = [owner["reason"]]
    else:
        output["proposal_refs"] = changes
    return output

def invoke(package: Path, repo: Path, public: dict, owner: dict) -> dict:
    profile = public["profile"]
    validate_json(public, package / "schemas" / ("public-" + profile.replace("_", "-") + "-input-1.0.schema.json"), "input")
    validate_json(owner, package / "schemas/phase2-check.schema.json", "owner_result")
    validate_candidate_classifications(owner)
    if owner["task_ref"] != public["task_ref"] or owner["mode"] != public["mode"]:
        raise CommandError("stale_identity", "owner_result", "Review the exact Delivery input.", 3)
    projection = DeliveryProjection(repo, public["task_ref"])
    delivery = _binding(projection, public)
    candidate = delivery["candidate"]
    dirty = {path for path in dirty_paths(repo) if not reviewed_content_metadata_path(path)}
    if not dirty.issubset(owner["reviewed_paths"]) or not set(candidate["paths"]).issubset(owner["reviewed_paths"]):
        raise CommandError("stale_identity", "reviewed_paths", "Review all current candidate paths and business changes.", 3)
    if owner["phase2_capture_commit"] != candidate["head_ref"]:
        raise CommandError("stale_identity", "phase2_capture_commit", "Check the exact current candidate HEAD.", 3)
    # The old whole-worktree token includes the public Task record written by
    # this very gate. The new local token is the upstream candidate reference;
    # the existing semantic payload is retained, never interpreted as authority.
    exit_id = owner["typed_exit"]
    candidate_check = profile == "delivery_candidate_check"
    if (candidate_check and exit_id in {"passed", "resolved_reconciliation_passed"}) or (not candidate_check and exit_id == "candidate_checked"):
        raise CommandError("schema_mismatch", "typed_exit", "Use candidate_checked only for candidate Check; final profiles retain their final gate meaning.")
    if candidate_check and delivery["phase"] != "checking":
        raise CommandError("stale_identity", "delivery.phase", "Implementation must begin_check the actual candidate before a fresh candidate Check; phase never supplies a pass.", 3)
    resolved = profile == "delivery_resolved_reconciliation"
    if (exit_id == "resolved_reconciliation_passed" and not resolved) or (resolved and exit_id == "passed"):
        raise CommandError("schema_mismatch", "typed_exit", "Use the resolved-tree pass only for its dedicated Check profile.")
    output = {"exit_id": exit_id}
    pending_rework = None
    pending_gate = None
    if exit_id != "blocked":
        output.update(task_ref=public["task_ref"], delivery_key=public["delivery_key"])
    if exit_id == "candidate_checked":
        if owner["reviewed_content_sha256"] != content_identity(repo):
            raise CommandError("stale_identity", "reviewed_content_sha256", "Review the complete current candidate before final integration.", 3)
        try:
            current = reviewed_content_identity(repo)
        except ReviewedContentError as exc:
            raise CommandError("stale_identity", "candidate", str(exc), 3) from exc
        output["candidate"] = {"head": candidate["head_ref"], "content_identity": "sha256:" + current["sha256"]}
        # Candidate judgment is complete. The existing Check owner returns to
        # implementation; retained real gates are history, never a new pass.
        pending_rework = ("implementation", "implement.md", ["readiness"])
    elif exit_id == "passed":
        evidence = [authority_ref(projection.planning_directory(public["delivery_key"]) / name, repo)
                    for name in ("prd.md", "design.md", "implement.md")]
        identity = hashlib.sha256(json.dumps({"key": public["delivery_key"], "candidate": candidate,
                                             "semantic": owner}, sort_keys=True).encode()).hexdigest()
        result_id = "check:" + identity
        prior = delivery["results"]["check"]
        if (prior is None or prior["result_id"] != result_id) and owner["reviewed_content_sha256"] != content_identity(repo):
            raise CommandError("stale_identity", "reviewed_content_sha256", "Rerun the current semantic Check after content changes.", 3)
        pending_gate = (result_id, evidence)
        output["check_result_id"] = result_id
    elif exit_id == "resolved_reconciliation_passed":
        if owner["reviewed_content_sha256"] != skill_content_identity(package, repo, public["task_ref"], public["mode"], public):
            raise CommandError("stale_identity", "reviewed_content_sha256", "Review the current resolved tree before the exact reconciliation commit.", 3)
        # This result authorizes no mutation and creates no public candidate
        # gate: the resolved tree has not been committed yet. Reconcile owns
        # that exact action, then a fresh formal Check owns the new HEAD.
        output["phase2_commit_anchor"] = owner["phase2_capture_commit"]
    elif exit_id == "implementation_required":
        output["finding_refs"] = [row["id"] for row in owner["semantic_review"]["findings"] if row["status"] == "open"]
        pending_rework = ("implementation", "implement.md", ["readiness"])
    elif exit_id == "planning_stale":
        from planning_recovery import rollback_binding, validate_result_content, verify_binding_authorities
        expected = rollback_binding(projection, public, delivery)
        if owner.get("rollback_binding") != expected:
            raise CommandError("stale_identity", "rollback_binding", "Record the planning_stale result with --skill-input before the first rework; use the recovery profile only after actual rollback.", 3)
        verify_binding_authorities(projection, expected)
        validate_result_content(projection, owner, delivery, public)
        output = planning_stale_output(public, owner)
        pending_rework = ("planning", "prd.md", ["planning", "check", "full_review", "readiness"])
    validate_json(output, package / "schemas" / ("public-output-delivery-" + exit_id.replace("_", "-") + "-1.0.schema.json"), "stdout")
    if pending_rework is not None:
        target, plan_name, invalidated = pending_rework
        rework(projection, public["delivery_key"], "check", target,
               authority_ref(projection.planning_directory(public["delivery_key"]) / plan_name, repo),
               invalidated)
    if pending_gate is not None:
        result_id, evidence = pending_gate
        record_gate(projection, public["delivery_key"], "check", result_id, "passed", evidence, [])
    return output
