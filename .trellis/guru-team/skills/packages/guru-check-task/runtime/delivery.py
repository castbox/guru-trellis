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
