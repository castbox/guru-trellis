"""Apply a completed original stage-owner scope judgment through upstream rework."""
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle import LifecycleContractError
from .adapter import DeliveryProjection
from .gates import rework


def revise(root, package, public, semantic, *, owner_role, expected_phase):
    validate_json(public, package / "schemas/public-delivery-scope-revision-input-1.0.schema.json", "input")
    validate_json(semantic, package / "schemas/delivery-scope-revision-review-1.0.schema.json", "semantic_result")
    if semantic["public_input"] != public:
        raise CommandError("stale_identity", "public_input", "Review the exact current scope revision.", 3)
    projection = DeliveryProjection(root, public["task_ref"])
    try:
        record = projection.read_record()
        scope = public["scope_ref"]
        if scope["authority"] != record["accepted_scope"]:
            raise CommandError("stale_identity", "scope_ref", "Consume actual original Clarify accepted scope.", 3)
        projection._call(projection.api.delivery_store.verify_authority, root, scope["authority"])
        delivery = projection.resolve(public["delivery_key"])
        recovered = (delivery["phase"] == "planning" and delivery["scope_ref"] == scope
                     and all(value is None for value in delivery["results"].values()))
        if not recovered:
            if delivery["phase"] != expected_phase:
                raise CommandError("stale_identity", "phase", "Return to the actual current scope revision stage owner.", 3)
            rework(projection, public["delivery_key"], owner_role, "planning",
                   scope["authority"], ["planning", "check", "full_review", "readiness"],
                   scope_ref=scope)
        output = {name: public[name] for name in ("mode", "task_ref", "delivery_key", "source_selection", "revision_refs")}
        output["exit_id"] = "delivery_scope_revised"
        validate_json(output, package / "schemas/public-delivery-scope-revised-output-1.0.schema.json", "stdout")
        return output
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
