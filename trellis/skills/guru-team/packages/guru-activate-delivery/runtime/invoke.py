"""Only Activation writes the public Planning gate after the semantic boundary."""
from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from pathlib import Path

from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from runtime.task_lifecycle.errors import LifecycleContractError


def planning_identity(root: Path, directory: Path) -> str:
    root, directory = root.resolve(), directory.resolve()
    entries = []
    for filename in ("prd.md", "design.md", "implement.md"):
        path = directory / filename
        if not path.is_file() or not path.read_text().strip():
            raise LifecycleContractError("missing_planning_artifact", filename, "Restore the current complete Delivery plan.")
        entries.append({"path": path.relative_to(root).as_posix(), "content_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    entries.sort(key=lambda entry: entry["path"])
    return "planning:" + hashlib.sha256(json.dumps(entries, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def invoke(package: Path, root: Path, public: dict, owner: dict) -> dict:
    root = root.resolve()
    if public.get("profile") == "delivery_scope_revision":
        from runtime.delivery_projection.scope_revision import revise
        return revise(root, package, public, owner, owner_role="planning", expected_phase="planning")
    if public.get("profile") == "delivery_scope_withdrawal":
        from runtime.delivery_projection.withdrawal import stop
        return stop(root, package, public, owner, owner_role="planning", expected_phase="planning")
    validate_json(public, package / "schemas/public-delivery-activation-input.schema.json", "input")
    validate_json(owner, package / "schemas/semantic-result.schema.json", "owner_result")
    if owner["typed_exit"] == "blocked":
        return {"exit_id": "blocked", "reason_code": "semantic_blocked"}
    if owner["typed_exit"] == "invalid_delivery_state":
        return {"exit_id": "invalid_delivery_state", "reason_code": "semantic_invalid_delivery_state"}
    if owner["typed_exit"] == "planning_refresh_required":
        return {"exit_id": "planning_refresh_required", "delivery_key": public["delivery_key"], "task_ref": public["task_ref"]}
    if owner["typed_exit"] != "delivery_started":
        raise CommandError("schema_mismatch", "owner_result.typed_exit", "Use the declared Activation outcome.")
    try:
        projection = DeliveryProjection(root, public["task_ref"])
        key = public["delivery_key"]
        delivery = projection.resolve(key)
        current = projection.current(key)
        if current.get("kind") != "current" or current.get("key") != key:
            raise LifecycleContractError("delivery_selection_required", "delivery_key", "Bind the exact public current Delivery before Activation.")
        directory = projection.planning_directory(key)
        if public["planning_result_id"] != planning_identity(root, directory):
            return {"exit_id": "planning_refresh_required", "delivery_key": key, "task_ref": public["task_ref"]}
        plan = authority_ref(directory / "design.md", root)
        path = root / ".trellis/.runtime/guru-team/delivery-activation" / (key["delivery_id"] + ".json")
        if public["action"] == "recover_activation":
            result = delivery["results"]["planning"]
            if result is None or result["plan_ref"] != plan or result["scope_ref"] != delivery["scope_ref"]:
                raise LifecycleContractError("planning_result_unavailable", "planning_result", "Return to the original plan presentation and acceptance boundary; phase alone is insufficient.")
        else:
            # A normal retry uses the exact pending operation, not another result id.
            if path.is_file():
                operation = json.loads(path.read_text())
                result = operation["result"]
                if operation["key"] != key or result["plan_ref"] != plan or result["scope_ref"] != delivery["scope_ref"]:
                    # The old operation cannot accept this changed plan. Its
                    # same-owner consumer ends here before fresh Planning.
                    path.unlink()
                    return {"exit_id": "planning_refresh_required", "delivery_key": key, "task_ref": public["task_ref"]}
            else:
                result = {"result_id": "planning-accepted:" + str(uuid.uuid4()), "owner_role": "planning",
                          "owner_id": projection.declaration()["owners"]["planning"], "outcome": "accepted",
                          "scope_ref": delivery["scope_ref"], "plan_ref": plan, "candidate": None,
                          "predecessor_result_id": None, "obligations": [],
                          "evidence": [authority_ref(directory / filename, root) for filename in ("prd.md", "design.md", "implement.md")]}
                operation = {"api_version": "1.0", "operation": "record_gate", "key": key,
                             "owner_role": "planning", "owner_id": result["owner_id"],
                             "expected_phase": "planning", "result": result}
                projection._call(projection.api.delivery_operations.parse_operation, operation)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + "\n")
            projection.apply(operation)
        output = {"exit_id": "delivery_started", "delivery_key": key, "task_ref": public["task_ref"], "planning_accepted_result_id": result["result_id"]}
        validate_json(output, package / "schemas/public-delivery-started-output.schema.json", "stdout")
        if path.is_file():
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
