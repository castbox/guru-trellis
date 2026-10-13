"""Two original Clarify continuations: scope judgment, then scope publication.

The first never writes planning or public scope. The second consumes the sole
Author's whole-Task requirements and performs the installed public operation.
"""
from __future__ import annotations

from pathlib import Path

from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle.errors import LifecycleContractError


PROFILES = {"delivery_active_task_scope_change", "delivery_task_scope_revision",
            "task_scope_requirements_acceptance"}


def invoke(package: Path, root: Path, public: dict, owner: dict) -> dict:
    profile = public["profile"]
    validate_json(public, package / ("schemas/public-" + profile.replace("_", "-") + "-input.schema.json"), "public_input")
    validate_json(owner, package / "schemas/semantic-scope-continuation-2.0.schema.json", "owner_result")
    if owner["public_input"] != public:
        raise CommandError("stale_identity", "owner_result.public_input", "Review this exact scope continuation.", 3)
    if (owner["typed_exit"] == "blocked") != (owner["ai_review_gate"]["status"] == "blocked"):
        raise CommandError("schema_mismatch", "ai_review_gate.status", "Bind the gate to the actual scope outcome.")
    if owner["typed_exit"] == "blocked":
        return {"exit_id": "blocked"}
    try:
        projection = DeliveryProjection(root, public["task_ref"])
        record = projection.read_record()
        task_key = {"task_id": record["id"], "lifecycle_generation": record["lifecycle_generation"]}
        if profile == "delivery_active_task_scope_change":
            projection.resolve(public["delivery_key"])
            if {name: public["delivery_key"][name] for name in task_key} != task_key:
                raise CommandError("stale_identity", "delivery_key", "Resolve the affected current generation.", 3)
        elif profile == "delivery_task_scope_revision" and public["task_key"] != task_key:
            raise CommandError("stale_identity", "task_key", "Reread this Task's current generation.", 3)
        if profile == "task_scope_requirements_acceptance":
            expected = public["task_ref"] + "/prd.md"
            if public["requirements_locator"] != expected:
                raise CommandError("stale_identity", "requirements_locator", "Consume the actual scope-only Author root PRD.", 3)
            authority = authority_ref(root / expected, root)
            projection._call(projection.api.delivery_store.verify_authority, root, authority)
            if owner.get("authority") != authority:
                raise CommandError("stale_identity", "authority", "Review the current whole-Task requirements before accepting scope.", 3)
            if owner["source_selection"] != public["source_selection"] or owner["revision_refs"] != public["revision_refs"]:
                raise CommandError("stale_identity", "source_selection", "Refresh original Clarify selection; do not infer it from the PRD.", 3)
            if owner["scope_action"] == "no_change" and authority != record["accepted_scope"]:
                raise CommandError("stale_identity", "authority", "A changed requirements version needs a fresh scope disposition.", 3)
            projection.apply({"api_version": "1.0", "operation": "accept_scope", "key": task_key,
                              "owner_role": "task_scope", "owner_id": projection.declaration()["owners"]["task_scope"],
                              "authority": authority})
        elif "authority" in owner:
            raise CommandError("schema_mismatch", "owner_result.authority", "Source judgment hands requirements to Author; publication follows its actual output.")
        output = {"exit_id": "scope_ready", "profile": profile, "mode": public["mode"],
                  "task_ref": public["task_ref"], "source_selection": owner["source_selection"],
                  "revision_refs": owner["revision_refs"], "scope_action": owner["scope_action"]}
        if profile == "task_scope_requirements_acceptance":
            output["task_key"] = task_key
        validate_json(output, package / "schemas/public-scope-ready-output-2.0.schema.json", "stdout")
        return output
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
