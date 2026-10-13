"""Project the existing semantic readiness review for one public Delivery."""
from __future__ import annotations

import hashlib
import json

from common import project_output, validate_semantic
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.delivery_projection.gates import record_gate, rework
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle.active_checkout import resolve_active_task_checkout
from runtime.task_lifecycle.errors import LifecycleContractError


def invoke(package, repo, public, semantic):
    refresh = public["profile"] == "delivery_readiness_refresh"
    validate_json(public, package / ("schemas/public-delivery-readiness-refresh-input-1.0.schema.json" if refresh else "schemas/public-delivery-delivery-review-input-1.0.schema.json"), "input")
    try:
        resolve_active_task_checkout(repo, public["task_ref"])
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    projection = DeliveryProjection(repo, public["task_ref"])
    delivery = projection.resolve(public["delivery_key"])
    review = delivery["results"]["full_review"]
    if refresh:
        if review is None or projection.gate_applicability(public["delivery_key"])["full_review"]["kind"] != "applicable":
            raise CommandError("stale_identity", "full_review", "Return to independent full Review for the changed candidate.", 3)
        # Route reason is read by this owner before authoring the full semantic
        # round. Exact public identity is read, never inferred from phase.
        public = {**public, "full_review_result_id": review["result_id"], "branch_review_commit": delivery["candidate"]["head_ref"]}
    if (review is None or review["result_id"] != public["full_review_result_id"]
            or projection.gate_applicability(public["delivery_key"])["full_review"]["kind"] != "applicable"
            or delivery["candidate"]["head_ref"] != public["branch_review_commit"]):
        raise CommandError("stale_identity", "full_review_result_id", "Consume the current independent complete Review.", 3)
    projection._call(projection.api.delivery_store.verify_candidate, repo, delivery["candidate"])
    exit_id = validate_semantic(package, repo, {"profile": "delivery_review", "mode": public["mode"]},
                                semantic, projection.read_record()["source"])
    # This source policy/payload projection is retained from its original owner;
    # no cycle identifier is elevated into a public Delivery identity.
    output = project_output({"semantic_result": semantic, "task_ref": public["task_ref"],
                             "reviewed_head": public["branch_review_commit"], "delivery_cycle_ref": "unused"})
    output.pop("delivery_cycle_ref", None)
    if exit_id != "blocked":
        output["delivery_key"] = public["delivery_key"]
    if exit_id == "ready":
        result_id = "readiness:" + hashlib.sha256(json.dumps({"key": public["delivery_key"], "semantic": semantic,
            "candidate": delivery["candidate"], "predecessor": review["result_id"]}, sort_keys=True).encode()).hexdigest()
        record_gate(projection, public["delivery_key"], "readiness", result_id, "ready",
                    [authority_ref(projection.planning_directory(public["delivery_key"]) / "implement.md", repo)], [])
        output["readiness_result_id"] = result_id
    elif exit_id in {"planning_revision_required", "implementation_required"}:
        planning = exit_id == "planning_revision_required"
        rework(projection, public["delivery_key"], "readiness", "planning" if planning else "implementation",
               authority_ref(projection.planning_directory(public["delivery_key"]) / ("prd.md" if planning else "implement.md"), repo),
               ["planning", "check", "full_review", "readiness"] if planning else ["check", "full_review", "readiness"])
    validate_json(output, package / "schemas" / ("public-output-delivery-" + exit_id.replace("_", "-") + "-1.0.schema.json"), "stdout")
    return output
