"""Creation's deterministic public operation and same-owner result recovery."""
from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path

from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from runtime.task_lifecycle.errors import LifecycleContractError
from creation_result import checkpoint


def invoke(package: Path, root: Path, public: dict, owner: dict) -> dict:
    root = root.resolve()
    profiles = {"delivery_creation": "public-delivery-creation-input.schema.json", "delivery_selection": "public-delivery-selection-input.schema.json"}
    if public.get("profile") not in profiles:
        raise CommandError("schema_mismatch", "profile", "Select the current Delivery Creation or Selection profile.")
    validate_json(public, package / "schemas" / profiles[public["profile"]], "input")
    validate_json(owner, package / "schemas/semantic-result.schema.json", "owner_result")
    if owner["typed_exit"] == "blocked":
        return {"exit_id": "blocked", "reason_code": "semantic_blocked"}
    if owner["typed_exit"] in {"scope_revision_required", "selection_required"}:
        key = public.get("task_key") or {k: v for k, v in public["delivery_key"].items() if k != "delivery_id"}
        return {"exit_id": owner["typed_exit"], "task_key": key, "task_ref": public["task_ref"]}
    expected = "created"
    if owner["typed_exit"] != "created":
        raise CommandError("schema_mismatch", "owner_result.typed_exit", "Return the outcome for this Creation/Selection profile.")
    path = None
    try:
        projection = DeliveryProjection(root, public["task_ref"])
        if public["profile"] == "delivery_selection":
            key = public["delivery_key"]
            delivery = projection.resolve(key)
        else:
            record = projection.read_record()
            task_key = {"task_id": record["id"], "lifecycle_generation": record["lifecycle_generation"]}
            if public["task_key"] != task_key:
                raise LifecycleContractError("stale_lifecycle_generation", "task_key", "Resolve this Task's current generation.")
            path = checkpoint(root, public["task_ref"], public["continuation_id"])
            pending = json.loads(path.read_text()) if path.is_file() else None
            supported = projection.declaration()["profiles"]
            if pending is not None and pending["profile"] not in supported:
                # End only this owner's unsupported, unapplied creation interval.
                # Existing public identity always retains its original recovery input.
                projection._call(projection.api.delivery_operations.parse_operation, pending)
                pending_task = {name: pending["key"][name] for name in ("task_id", "lifecycle_generation")}
                exists = any(row["id"] == pending["key"]["delivery_id"] and
                             row["lifecycle_generation"] == pending["key"]["lifecycle_generation"]
                             for row in record["deliveries"])
                if (pending_task != task_key or pending["scope_ref"] != public["scope_ref"]
                        or pending["scope_ref"]["authority"] != record["accepted_scope"] or exists):
                    raise LifecycleContractError("creation_input_changed", "input", "Recover the exact existing public slice; cannot retire its creation interval.")
                path.unlink()
                pending = None
            if public["delivery_profile"] not in supported:
                raise LifecycleContractError("unsupported_delivery_profile", "delivery_profile", "Review a profile actually supported by the current Guru workflow.")
            if pending is not None:
                if pending["scope_ref"] != public["scope_ref"] or pending["profile"] != public["delivery_profile"] or {k: v for k, v in pending["key"].items() if k != "delivery_id"} != task_key:
                    raise LifecycleContractError("creation_input_changed", "input", "Recover the exact pending slice before starting another creation.")
                operation = pending
            elif public["action"] == "recover_creation":
                # The public session is an explicit selection, never inventory inference.
                current = projection.current()
                if current.get("kind") != "current" or {k: v for k, v in current["key"].items() if k != "delivery_id"} != task_key:
                    raise LifecycleContractError("delivery_selection_required", "delivery_key", "Recover the exact public selection or the original Creation checkpoint.")
                delivery = projection.resolve(current["key"])
                if delivery["scope_ref"] != public["scope_ref"] or delivery["profile"] != public["delivery_profile"]:
                    raise LifecycleContractError("creation_input_changed", "scope_ref", "Select the same explicitly reviewed slice; do not infer a new identity.")
                key = current["key"]
                operation = None
            else:
                key = {**task_key, "delivery_id": str(uuid.uuid4())}
                operation = {"api_version": "1.0", "operation": "create_delivery", "key": key,
                             "owner_role": "creation", "owner_id": projection.declaration()["owners"]["creation"],
                             "scope_ref": public["scope_ref"], "profile": public["delivery_profile"]}
                # Validate first with the upstream parser. Store only recovery inputs.
                projection._call(projection.api.delivery_operations.parse_operation, operation)
            if operation is not None:
                projection.selection_preflight(operation["key"])
                if not path.is_file():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
                projection.apply(operation)
                key = operation["key"]
                delivery = projection.resolve(key)
        selected = projection.select(key)
        if selected.get("kind") != "current" or selected.get("key") != key:
            raise LifecycleContractError("delivery_selection_required", "session", "Recover the same Creation selection before Planning.")
        output = {"exit_id": expected, "delivery_key": key, "task_ref": public["task_ref"], "planning_root": delivery["planning_root"]}
        validate_json(output, package / ("schemas/public-" + expected + "-output.schema.json"), "stdout")
        if path is not None and path.is_file() and projection.has_context():
            path.unlink()
        return output
    except LifecycleContractError as exc:
        return {"exit_id": "blocked", "reason_code": exc.code}


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    args = parser.parse_args(argv)
    return invoke(package_root, Path(args.root).resolve(), read_json(args.input, "input"), read_json(args.owner_result, "owner_result"))
