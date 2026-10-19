"""Call-local independent complete-range analysis before final Check."""
from pathlib import Path

from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle import LifecycleContractError, resolve_active_task_checkout


def invoke(package: Path, repo: Path, public: dict, review: dict) -> dict:
    from common import git
    validate_json(public, package / "schemas/public-delivery-draft-content-review-input-1.0.schema.json", "input")
    validate_json(review, package / "schemas/draft-content-review-1.0.schema.json", "owner_result")
    projection = DeliveryProjection(repo, public["task_ref"])
    try:
        resolve_active_task_checkout(repo, public["task_ref"])
        projection.selection_preflight(public["delivery_key"])
        delivery = projection.resolve(public["delivery_key"])
        planning = delivery["results"]["planning"]
        if (delivery["phase"] in {"planning", "delivered", "stopped"} or planning is None
                or projection.gate_applicability(public["delivery_key"])["planning"]["kind"] != "applicable"):
            raise CommandError("stale_identity", "planning", "Read the current activated Delivery Planning before early analysis.", 3)
        base, head = public["base_ref"], public["branch_review_commit"]
        if (projection.commit(base) != base or projection.commit(head) != head
                or projection.content_base(public["delivery_key"], development_base=base) != base
                or git(repo, "rev-parse", "HEAD") != head
                or not git(repo, "diff", "--name-only", base, head)):
            raise CommandError("stale_identity", "candidate", "Review the complete fixed base/actual HEAD range; target advancement does not change it.", 3)
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    if review["status"] == "blocked":
        return {"exit_id": "blocked"}
    output = {"task_ref": public["task_ref"], "delivery_key": public["delivery_key"]}
    if review["status"] == "passed":
        output.update(exit_id="draft_content_reviewed", base_ref=base, branch_review_commit=head)
    else:
        output.update(exit_id="draft_revision_required", revision_refs=review["revision_refs"])
    validate_json(output, package / ("schemas/public-output-delivery-" + output["exit_id"].replace("_", "-") + "-1.0.schema.json"), "stdout")
    # No full_review fact or cross-stage checkpoint is written.
    return output
