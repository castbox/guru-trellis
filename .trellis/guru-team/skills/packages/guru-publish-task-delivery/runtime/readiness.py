"""Validate and project AI-authored Publication readiness."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from owner import CLOSING as _CLOSING_KEYWORD
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle.identity import origin_matches


DIMENSION_IDS = [
    "requirement_authority",
    "delivery_policy",
    "slice_completeness",
    "independent_delivery",
    "implementation_quality",
    "validation_truthfulness",
    "docs_rdt_architecture",
    "branch_review_freshness",
    "pr_payload_truthfulness",
    "base_and_live_facts",
]


def validate_semantic(package_root: Path, repo: Path, public: dict[str, Any], semantic: dict[str, Any], source: dict[str, Any]) -> str:
    validate_json(semantic, package_root / "schemas/semantic-publication-readiness-1.0.schema.json", "semantic_result")
    if semantic["profile"] != public["profile"] or semantic["mode"] != public["mode"]:
        raise CommandError("schema_mismatch", "semantic_result", "Author the result for the exact public input.")
    dimensions = semantic["dimensions"]
    if [item["id"] for item in dimensions] != DIMENSION_IDS:
        raise CommandError("schema_mismatch", "dimensions", "Use the exact ordered Publication readiness dimensions.")
    for key in ("candidate_ref", "finding_ref", "proposal_ref"):
        collections = {
            "candidate_ref": semantic["candidate_classifications"],
            "finding_ref": semantic["findings"],
            "proposal_ref": semantic["scope_proposals"],
        }
        refs = [item[key] for item in collections[key]]
        if len(refs) != len(set(refs)):
            raise CommandError("schema_mismatch", key, "Use unique semantic references.")
    candidate_refs = {item["candidate_ref"] for item in semantic["candidate_classifications"]}
    if any(item["candidate_ref"] not in candidate_refs for item in semantic["findings"] + semantic["scope_proposals"]):
        raise CommandError("schema_mismatch", "candidate_classifications", "Bind every finding and proposal to a classified candidate.")
    dimension_status = {item["id"]: item["status"] for item in dimensions}
    for finding in semantic["findings"]:
        if finding["dimension"] not in dimension_status:
            raise CommandError("schema_mismatch", "findings.dimension", "Bind findings to one declared dimension.")
        if finding["status"] == "open" and finding["closure_evidence"]:
            raise CommandError("schema_mismatch", "findings.closure_evidence", "Open findings have no closure evidence.")
        if finding["status"] == "closed" and not finding["closure_evidence"]:
            raise CommandError("schema_mismatch", "findings.closure_evidence", "Closed findings require closure evidence.")
    policy = semantic["delivery_policy"]
    state = "remaining" if policy["remaining_work_refs"] else "none"
    if semantic["remaining_work_state"] != state:
        raise CommandError("schema_mismatch", "remaining_work_state", "Match the approved remaining-work set.")
    route = semantic["route"]
    exit_id = route["typed_exit"]
    open_findings = [item for item in semantic["findings"] if item["status"] == "open"]
    open_proposals = [item for item in semantic["scope_proposals"] if item["status"] == "open"]
    open_classes = {item["route_class"] for item in open_findings}
    conclusions = semantic["conclusions"].values()
    all_passed = all(item["status"] == "passed" for item in dimensions) and all(
        item["status"] == "passed" for item in conclusions
    )
    if exit_id == "ready":
        if not all_passed or open_findings or open_proposals:
            raise CommandError("schema_mismatch", "route", "Ready requires a fully passing current review.")
    elif exit_id == "planning_revision_required":
        if open_classes != {"planning_revision"} or open_proposals:
            raise CommandError("schema_mismatch", "route", "Planning re-entry requires only planning findings.")
    elif exit_id == "implementation_required":
        if "implementation" not in open_classes or "external_blocker" in open_classes or open_proposals:
            raise CommandError("schema_mismatch", "route", "Implementation re-entry requires current-slice findings only.")
    elif exit_id == "scope_confirmation_required":
        if not open_proposals or open_findings:
            raise CommandError("schema_mismatch", "route", "Scope confirmation requires proposals and no open findings.")
    elif exit_id == "blocked":
        blocked = any(item["status"] == "blocked" for item in dimensions) or any(
            item["status"] == "blocked" for item in conclusions
        )
        if "external_blocker" not in open_classes or not blocked or open_proposals:
            raise CommandError("schema_mismatch", "route", "Blocked requires one concrete external evidence blocker.")
    else:
        raise CommandError("schema_mismatch", "route.typed_exit", "Use one declared typed exit.")
    body = semantic["pr_payload"]["body"]
    if _CLOSING_KEYWORD.search(body):
        raise CommandError("schema_mismatch", "pr_payload.body", "Delivery PRs use Refs only; remove closing keywords.")
    if source["kind"] == "issue":
        qualified = re.search(
            rf"(?i)\bRefs\s+{re.escape(source['repo_ref'])}#{source['number']}\b", body
        )
        local = origin_matches(repo, source["repo_ref"]) and re.search(
            rf"(?i)\bRefs\s+#?{source['number']}\b", body
        )
        if not qualified and not local:
            raise CommandError("schema_mismatch", "pr_payload.body", "Reference the exact task Issue with Refs only.")
    return exit_id


def project_output(public, semantic):
    exit_id = semantic["route"]["typed_exit"]
    if exit_id == "blocked":
        return {"exit_id": exit_id, "reason_code": semantic["route"]["reason_code"],
                "remediation": semantic["route"]["remediation"]}
    output = {"exit_id": exit_id, "task_ref": public["task_ref"], "delivery_key": public["delivery_key"]}
    if exit_id == "scope_confirmation_required":
        return {**output, "proposal_refs": [item["proposal_ref"] for item in semantic["scope_proposals"]
                                             if item["status"] == "open"]}
    planning = exit_id == "planning_revision_required"
    refs = [item["finding_ref"] for item in semantic["findings"]
            if item["status"] == "open" and item["route_class"] == ("planning_revision" if planning else "implementation")]
    return {**output, **({"reason_refs": refs} if planning else {"finding_refs": refs, "resume_target": "phase-2"})}
