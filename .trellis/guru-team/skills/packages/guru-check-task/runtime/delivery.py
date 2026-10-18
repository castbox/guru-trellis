"""Delivery-scoped Check recorder/validator; the AI still owns all judgments."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from common import content_identity, dirty_paths, git, validate_candidate_classifications
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.delivery_projection.gates import record_gate, rework
from runtime.io import CommandError
from runtime.reviewed_content import reviewed_content_metadata_path
from runtime.schema import validate_json
from runtime.task_lifecycle.active_checkout import resolve_active_task_checkout
from runtime.task_lifecycle.errors import LifecycleContractError


def _binding(projection, public):
    try:
        resolve_active_task_checkout(projection.root, public["task_ref"])
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    key = public["delivery_key"]
    delivery = projection.resolve(key)
    planning = delivery["results"]["planning"]
    if planning is None or planning["result_id"] != public["planning_accepted_result_id"]:
        raise CommandError("stale_identity", "planning_accepted_result_id", "Consume the current public Planning result.", 3)
    if projection.gate_applicability(key)["planning"]["kind"] != "applicable":
        raise CommandError("stale_identity", "planning", "Reenter the affected Planning owner.", 3)
    try:
        projection._call(projection.api.delivery_store.verify_candidate, projection.root, delivery["candidate"])
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    if delivery["candidate"]["head_ref"] != git(projection.root, "rev-parse", "HEAD"):
        raise CommandError("stale_identity", "candidate.head_ref", "Begin Check for the actual current candidate.", 3)
    return delivery


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
    resolved = profile == "delivery_resolved_reconciliation"
    if (exit_id == "resolved_reconciliation_passed" and not resolved) or (resolved and exit_id == "passed"):
        raise CommandError("schema_mismatch", "typed_exit", "Use the resolved-tree pass only for its dedicated Check profile.")
    output = {"exit_id": exit_id}
    if exit_id != "blocked":
        output.update(task_ref=public["task_ref"], delivery_key=public["delivery_key"])
    if exit_id == "passed":
        evidence = [authority_ref(projection.planning_directory(public["delivery_key"]) / name, repo)
                    for name in ("prd.md", "design.md", "implement.md")]
        identity = hashlib.sha256(json.dumps({"key": public["delivery_key"], "candidate": candidate,
                                             "semantic": owner}, sort_keys=True).encode()).hexdigest()
        result_id = "check:" + identity
        prior = delivery["results"]["check"]
        if (prior is None or prior["result_id"] != result_id) and owner["reviewed_content_sha256"] != content_identity(repo):
            raise CommandError("stale_identity", "reviewed_content_sha256", "Rerun the current semantic Check after content changes.", 3)
        record_gate(projection, public["delivery_key"], "check", result_id, "passed", evidence, [])
        output["check_result_id"] = result_id
    elif exit_id == "resolved_reconciliation_passed":
        if owner["reviewed_content_sha256"] != content_identity(repo):
            raise CommandError("stale_identity", "reviewed_content_sha256", "Review the current resolved tree before the exact reconciliation commit.", 3)
        # This result authorizes no mutation and creates no public candidate
        # gate: the resolved tree has not been committed yet. Reconcile owns
        # that exact action, then a fresh formal Check owns the new HEAD.
        output["phase2_commit_anchor"] = owner["phase2_capture_commit"]
    elif exit_id == "implementation_required":
        output["finding_refs"] = [row["id"] for row in owner["semantic_review"]["findings"] if row["status"] == "open"]
        rework(projection, public["delivery_key"], "check", "implementation",
               authority_ref(projection.planning_directory(public["delivery_key"]) / "implement.md", repo),
               ["readiness"])
    elif exit_id == "planning_stale":
        output.update(planning_route=owner["route"], proposal_refs=[row["id"] for row in owner["semantic_review"]["scope_decisions"]])
        rework(projection, public["delivery_key"], "check", "planning",
               authority_ref(projection.planning_directory(public["delivery_key"]) / "prd.md", repo),
               ["planning", "check", "full_review", "readiness"])
    validate_json(output, package / "schemas" / ("public-output-delivery-" + exit_id.replace("_", "-") + "-1.0.schema.json"), "stdout")
    return output
