"""Validate one original Check rollback and project its planning handoff."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

from common import content_identity, dirty_paths, resolved_content_identity, validate_candidate_classifications
from delivery import _current_delivery, _candidate_binding, planning_stale_output
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.io import CommandError
from runtime.reviewed_content import reviewed_content_metadata_path
from runtime.schema import validate_json


def rollback_binding(projection, public, delivery):
    planning = delivery["results"]["planning"]
    if planning is None or planning["result_id"] != public["planning_accepted_result_id"]:
        raise CommandError("stale_identity", "planning_accepted_result_id", "Read the actual original public Planning result for this Check input.", 3)
    if delivery["candidate"] is None:
        raise CommandError("stale_identity", "original_delivery.candidate", "Original Check needs its actual candidate; return incomplete historical evidence to original Planning.", 3)
    if planning["scope_ref"] != delivery["scope_ref"] or planning["plan_ref"] != delivery["plan_ref"]:
        raise CommandError("stale_identity", "original_delivery.results.planning", "Use the matching original scope and plan from the retained public query.", 3)
    directory = projection.task_dir / delivery["planning_root"]
    locators = [(directory / name).relative_to(projection.root).as_posix()
                for name in ("prd.md", "design.md", "implement.md")]
    evidence = []
    for locator in locators:
        matches = [ref for ref in planning["evidence"] if ref["locator"] == locator]
        if len(matches) != 1:
            raise CommandError("stale_identity", "original_delivery.results.planning.evidence", "Original Planning must retain the three planning AuthorityRefs; return missing original evidence to the Planning owner.", 3)
        evidence.append(matches[0])
    return copy.deepcopy({"delivery_key": public["delivery_key"],
                          "planning_accepted_result_id": planning["result_id"],
                          "scope_ref": delivery["scope_ref"], "plan_ref": delivery["plan_ref"],
                          "candidate": delivery["candidate"], "planning_evidence": evidence})


def validate_result_content(projection, owner, delivery, original_input):
    _candidate_binding(projection, delivery)
    candidate = delivery["candidate"]
    if owner["phase2_capture_commit"] != candidate["head_ref"]:
        raise CommandError("stale_identity", "phase2_capture_commit", "Return changed HEAD to the original implementation/Check owner.", 3)
    current_content = (resolved_content_identity(projection.root, original_input, delivery)
                       if original_input["profile"] == "delivery_resolved_reconciliation"
                       else content_identity(projection.root))
    if owner["reviewed_content_sha256"] != current_content:
        raise CommandError("stale_identity", "reviewed_content_sha256", "Return changed business content to original implementation/Check; preserve current edits.", 3)
    dirty = {path for path in dirty_paths(projection.root) if not reviewed_content_metadata_path(path)}
    if not (dirty | set(candidate["paths"])).issubset(owner["reviewed_paths"]):
        raise CommandError("stale_identity", "reviewed_paths", "Review the actual original candidate and all current changed paths.", 3)


def validate_recovery_binding(projection, public, binding, delivery):
    original = public["original_check_input"]
    for name, parser in (("scope_ref", "slice_scope"), ("plan_ref", "authority"), ("candidate", "candidate")):
        projection._call(getattr(projection.api.delivery_schema, parser), binding[name])
    if (binding["delivery_key"] != public["delivery_key"]
            or binding["planning_accepted_result_id"] != original["planning_accepted_result_id"]):
        raise CommandError("stale_identity", "rollback_binding", "Use the original Check input and its same Task/Delivery rollback.", 3)
    if delivery["phase"] != "planning":
        raise CommandError("stale_identity", "delivery.phase", "Resume the actual current stage owner; this rollback can recover only in planning.", 3)
    if any(delivery["results"][name] is not None for name in ("planning", "check", "full_review", "readiness")):
        raise CommandError("stale_identity", "delivery.results", "Consume the new stage result through its original owner; do not reuse this rollback.", 3)
    record = projection.read_record()
    if binding["scope_ref"] != delivery["scope_ref"] or binding["scope_ref"]["authority"] != record["accepted_scope"]:
        raise CommandError("stale_identity", "scope_ref", "Return the actual changed scope to original Clarify and Planning.", 3)
    if binding["plan_ref"] != delivery["plan_ref"]:
        raise CommandError("stale_identity", "plan_ref", "Return the actual changed plan to original Planning.", 3)
    if binding["candidate"] != delivery["candidate"]:
        raise CommandError("stale_identity", "candidate", "Return the changed candidate to original implementation/Check.", 3)
    verify_binding_authorities(projection, binding)


def verify_binding_authorities(projection, binding):
    projection._call(projection.api.delivery_store.verify_authority, projection.root, binding["scope_ref"]["authority"])
    for reference in [binding["plan_ref"], *binding["planning_evidence"]]:
        if authority_ref(projection.root / reference["locator"], projection.root) != reference:
            raise CommandError("stale_identity", "planning_evidence." + reference["locator"], "Planning bytes changed; original Planning must judge the actual revision.", 3)


def blocked_source(field, remediation):
    sys.stderr.write("blocked: " + field + ": " + remediation + "\n")
    return {"exit_id": "blocked"}


def invoke(package: Path, repo: Path, public: dict, owner: dict) -> dict:
    validate_json(public, package / "schemas/public-delivery-planning-stale-recovery-input-1.0.schema.json", "input")
    validate_json(owner, package / "schemas/delivery-planning-stale-recovery-owner-1.0.schema.json", "owner_result")
    original_input = public["original_check_input"]
    for field in ("task_ref", "mode", "delivery_key"):
        if original_input[field] != public[field]:
            raise CommandError("stale_identity", "original_check_input." + field, "Use the same original Task, mode and Delivery.", 3)
    original = owner["original_result"]
    for field in ("task_ref", "mode"):
        if original[field] != public[field]:
            raise CommandError("stale_identity", "original_result." + field, "Read this exact original Check result.", 3)
    projection = DeliveryProjection(repo, public["task_ref"])
    delivery = _current_delivery(projection, public)
    binding = original.get("rollback_binding")
    if binding is None:
        source = owner.get("original_delivery")
        if source is None:
            return blocked_source("owner_result.original_delivery", "Retain the actual original public query with Planning and candidate. Original Check must obtain that source, or original Planning/Clarify must judge current scope afresh.")
        if source["key"] != public["delivery_key"]:
            raise CommandError("stale_identity", "original_delivery.key", "Read the exact original public Delivery query.", 3)
        historical = projection._call(projection.api.delivery_schema.delivery_record, source["delivery"])
        if (historical["id"] != public["delivery_key"]["delivery_id"]
                or historical["lifecycle_generation"] != public["delivery_key"]["lifecycle_generation"]):
            raise CommandError("stale_identity", "original_delivery.delivery", "Read the same original Delivery and generation.", 3)
        planning = historical["results"]["planning"]
        if planning is None:
            return blocked_source("owner_result.original_delivery.results.planning", "The original public query does not retain Planning. Original Check needs the actual source; original Planning/Clarify must otherwise judge current scope afresh.")
        if historical["candidate"] is None:
            return blocked_source("owner_result.original_delivery.candidate", "Original candidate is missing. Original Check needs the actual source; original Planning/Clarify must otherwise judge current scope afresh.")
        directory = projection.task_dir / historical["planning_root"]
        for name in ("prd.md", "design.md", "implement.md"):
            locator = (directory / name).relative_to(projection.root).as_posix()
            if not any(ref["locator"] == locator for ref in planning["evidence"]):
                return blocked_source("owner_result.original_delivery.results.planning.evidence." + name,
                                      "Original Planning evidence is incomplete. Original Check needs the actual source; original Planning/Clarify must otherwise judge current scope afresh.")
        binding = rollback_binding(projection, original_input, historical)
    validate_json(binding, package / "schemas/delivery-rollback-binding-1.0.schema.json", "rollback_binding")
    validate_recovery_binding(projection, public, binding, delivery)
    validate_candidate_classifications(original)
    validate_result_content(projection, original, delivery, original_input)
    selected = owner.get("corrected_result", original)
    validate_candidate_classifications(selected)
    for field in ("task_ref", "mode", "phase2_capture_commit", "reviewed_content_sha256"):
        if selected[field] != original[field]:
            raise CommandError("stale_identity", "corrected_result." + field, "Correct only this same rollback after current semantic judgment.", 3)
    if selected.get("rollback_binding", binding) != binding:
        raise CommandError("stale_identity", "corrected_result.rollback_binding", "Retain this original rollback binding.", 3)
    validate_result_content(projection, selected, delivery, original_input)
    output = planning_stale_output(public, selected)
    validate_json(output, package / "schemas/public-output-delivery-planning-stale-1.0.schema.json", "stdout")
    return output
