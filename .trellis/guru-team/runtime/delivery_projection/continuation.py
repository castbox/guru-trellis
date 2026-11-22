"""Read current continuation facts from the existing Task and Delivery authorities."""
from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
from typing import Any, Callable

from ..task_lifecycle.active_checkout import read_bound_checkout
from ..task_lifecycle.branch_store import TaskLifecycleKey
from ..task_lifecycle.errors import LifecycleContractError
from ..task_lifecycle.git_facts import inspect_repository
from .adapter import CurrentCheckoutPort, DeliveryProjection, _installed_modules, official_session_port

VERSION = "1.0"
_BIND = "guru-bind-task-session"
_IDENTITY = "guru-establish-task-identity"
_BRANCH = "guru-establish-task-branch-binding"
_CHECKOUT = "guru-ensure-task-checkout"
_DELIVERY = "guru-create-delivery"
_LEGACY = "guru-maintain-legacy-task"


def _result(kind: str, mode: str, **fields: Any) -> dict:
    return {"schema_version": VERSION, "kind": kind, "mode": mode, **fields}


def _diagnostic(exc: Exception, field: str, owner: str, *, fallback: str) -> dict:
    if isinstance(exc, LifecycleContractError):
        detail = exc.as_dict()
    else:
        raw = str(exc)
        code = getattr(exc, "code", None) or raw.partition(":")[0]
        if not isinstance(code, str) or not code.replace("_", "").isalnum() or not code.isascii():
            code = fallback
        detail = {"code": code, "field_path": field, "message": raw,
                  "remediation": "Reread through the original owner and resolve the reported condition."}
    text = str(exc)
    if "maintenance_required:" in text:
        detail.update(code="maintenance_required", remediation=text)
        owner = _LEGACY
    elif detail["code"] in {"unsupported_task_schema", "unsupported_legacy_task", "unsupported_binding_schema"}:
        owner = _LEGACY
    elif detail["code"] in {"binding_required", "branch_binding_conflict", "branch_binding_unavailable",
                           "binding_ownership_mismatch", "resource_ledger_conflict", "invalid_task_branch_binding"}:
        owner = _BRANCH
    elif detail["code"] in {"current_task_checkout_unresolved", "checkout_required",
                           "checkout_identity_mismatch", "ambiguous_checkout", "git_fact_unavailable"}:
        owner = _CHECKOUT
    elif detail["code"] in {"unsupported_delivery_api", "unsupported_runtime_contract",
                           "missing_runtime_contract", "invalid_runtime_contract"}:
        owner = "guru-upgrade-tools"
    return {**detail, "owner": owner}


def _error(exc: Exception, mode: str, field: str, owner: str, *, fallback: str = "stale_binding") -> dict:
    return _result("error", mode, diagnostic=_diagnostic(exc, field, owner, fallback=fallback))


def _signature(*values: Any) -> str:
    content = json.dumps(values, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + sha256(content.encode("utf-8")).hexdigest()


def _task_key(key: TaskLifecycleKey) -> dict:
    return {"task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation}


def _read_delivery(projection: DeliveryProjection, record: dict, key: dict, declaration: dict) -> dict:
    projection.api.delivery_schema.delivery_uuid(key["delivery_id"])
    for row in record["deliveries"]:
        if (row["id"], row["lifecycle_generation"]) != (key["delivery_id"], key["lifecycle_generation"]):
            continue
        if row["profile"] not in declaration["profiles"]:
            raise LifecycleContractError("unsupported_delivery_profile", "delivery.profile",
                                         "Use a profile supported by the current workflow.")
        return row
    raise LifecycleContractError("delivery_not_found", "delivery_id",
                                 "Select the exact Delivery belonging to this Task generation.")


def read_exact_delivery(root: Path, request: dict) -> dict:
    """Read one exact Delivery after the caller has verified its checkout."""
    target = request["task"]
    key = {k: target[k] for k in ("task_id", "lifecycle_generation")}
    key["delivery_id"] = request["delivery_id"]
    try:
        projection = DeliveryProjection(root, target["task_ref"])
        record = projection.read_record()
        if (record["id"], record["lifecycle_generation"]) != (target["task_id"], target["lifecycle_generation"]):
            raise LifecycleContractError("task_identity_mismatch", "task",
                                         "Reread the current Task identity through the original owner.")
        delivery = _read_delivery(projection, record, key, projection.declaration())
        applicability = projection.api.delivery_operations.get_gate_applicability(record, key)
    except (ValueError, OSError, RuntimeError) as exc:
        owner = _IDENTITY if getattr(exc, "code", None) == "task_identity_mismatch" else _DELIVERY
        return _error(exc, "explicit", "delivery", owner, fallback="delivery_projection_failed")
    return {"schema_version": VERSION, "key": key, "delivery": delivery, "gate_applicability": applicability}


def _active_binding(root: Path, official: Any, facts: Any, context: str) -> Any:
    path = official.session_path(root, context, facts)
    if official.record_exists(path):
        binding = official.read_record(path, root, facts)
        if binding.data["schema_version"] != 3:
            # The native reader knows the Task behind a predecessor binding.
            # Preserve its maintenance diagnosis before rejecting execution.
            api = _installed_modules(root, ("session_storage", "active_task"))
            active = api.active_task.resolve_active_task(root)
            if active.error:
                raise api.session_storage.SessionBindingError(active.error)
            raise LifecycleContractError("unsupported_binding_schema", "session",
                                         "Task v2 requires the original schema-3 Task/Delivery binding.")
        return binding
    # Let the installed reader diagnose a recognized predecessor carrier.
    api = _installed_modules(root, ("session_storage", "active_task"))
    if api.session_storage.unsupported_checkout_session_paths(facts, context):
        active = api.active_task.resolve_active_task(root)
        if active.error:
            raise api.session_storage.SessionBindingError(active.error)
    return None


def _source_diagnostic(root: Path, task_ref: str, original: Exception) -> Exception:
    maintenance = _installed_modules(root, ("maintenance",)).maintenance
    detail = maintenance.task_maintenance_diagnostic(root / task_ref)
    if detail:
        return LifecycleContractError("maintenance_required", "task.json", detail)
    return original


def _project_part(
    previous: dict, reuse: dict, group: str, field: str, project: Callable[[], dict],
) -> dict:
    if group in reuse and previous.get("reuse", {}).get(group) == reuse[group]:
        return previous[field]
    return project()


def read_continuation(root: Path, request: dict) -> dict:
    """Project lookup facts and their call-local reuse dependencies."""
    mode = "explicit" if request["intent"] == "inspect_task" else "session"
    target = request.get("task")
    requested_delivery = request.get("delivery_id")
    context = None
    try:
        official = official_session_port(root)
        context = official.resolve_context_key()
        facts = official.repository_facts(root)
        bound = _active_binding(root, official, facts, context) if context else None
    except (ValueError, OSError, RuntimeError) as exc:
        result = _error(exc, mode, "session", _BIND)
        if context:
            diagnostic = result["diagnostic"]
            for field in ("message", "remediation", "field_path"):
                if field in diagnostic:
                    diagnostic[field] = diagnostic[field].replace(f"{context}.json", "<current-session>.json")
        return result
    if bound is None:
        if target is None:
            return _result("no_current_task", mode)
        if context is not None and mode == "session":
            exc = LifecycleContractError("session_record_missing", "session",
                                         "Restore this Task through delivery_rebind_missing_session.")
            return _result("binding_required", mode, **target,
                           diagnostic=_diagnostic(exc, "session", _BIND, fallback="stale_binding"))
        mode = "explicit"

    if bound is not None and target is not None and (
        bound.task_id != target["task_id"] or bound.lifecycle_generation != target["lifecycle_generation"]
    ):
        return _error(LifecycleContractError("session_task_conflict", "task",
                                            "Use the current binding or enter the original Task switch owner."),
                      mode, "task", _BIND)
    identity = target if bound is None else {
        "task_id": bound.task_id, "lifecycle_generation": bound.lifecycle_generation,
    }
    key = TaskLifecycleKey(identity["task_id"], identity["lifecycle_generation"])
    try:
        repository = inspect_repository(root)
        binding, checkout = read_bound_checkout(repository, key)
    except (ValueError, OSError, RuntimeError) as exc:
        if target is not None and getattr(exc, "code", None) == "binding_required":
            exc = _source_diagnostic(root, target["task_ref"], exc)
        return _error(exc, mode, "checkout", _CHECKOUT, fallback="checkout_unavailable")

    try:
        resolved = CurrentCheckoutPort(official, checkout.path).resolve_task_identity(
            facts, key.task_id, key.lifecycle_generation)
        if resolved.workspace.resolve() != checkout.path or (
            target is not None and resolved.task_ref != target["task_ref"]
        ):
            raise LifecycleContractError("task_identity_mismatch", "task_ref",
                                         "Use the TaskRef from the current verified checkout.")
        projection = DeliveryProjection(checkout.path, resolved.task_ref)
        record = projection.read_record()
        if (record["id"], record["lifecycle_generation"]) != (key.task_id, key.lifecycle_generation):
            raise LifecycleContractError("stale_lifecycle_generation", "task",
                                         "Reread the current Task generation through the original owner.")
        declaration = projection.declaration()
    except (ValueError, OSError, RuntimeError) as exc:
        return _error(exc, mode, "task", _IDENTITY, fallback="invalid_task_record")

    selected = bound.data["delivery_id"] if bound is not None else None
    if bound is not None and requested_delivery is not None and (
        (mode == "session" and requested_delivery != selected)
        or (mode == "explicit" and selected not in (None, requested_delivery))
    ):
        return _error(LifecycleContractError("delivery_selection_conflict", "delivery_id",
                                            "Read the current selection or invoke its original selection owner."),
                      mode, "delivery_id", _DELIVERY)
    delivery_id = selected if mode == "session" else requested_delivery
    delivery = None
    if delivery_id is not None:
        try:
            delivery = _read_delivery(projection, record, {**_task_key(key), "delivery_id": delivery_id}, declaration)
        except (ValueError, OSError, RuntimeError) as exc:
            if mode == "session" and getattr(exc, "code", None) == "delivery_not_found":
                exc = LifecycleContractError("stale_binding", "session.delivery_id",
                                             "Selected Delivery does not belong to the current generation.")
            return _error(exc, mode, "delivery", _DELIVERY, fallback="delivery_projection_failed")

    reuse = {}
    previous = {}
    if mode == "session":
        origin = _signature(str(repository.common_dir), context)
        task = _signature(origin, _task_key(key), resolved.task_ref, record["source"])
        checkout_key = _signature(task, str(checkout.path), str(checkout.git_dir),
                                  binding.as_dict(), checkout.head)
        reuse = {"origin": origin, "task": task, "checkout": checkout_key}
        if delivery is not None:
            reuse["delivery"] = _signature(
                checkout_key, delivery_id, delivery["phase"], delivery["planning_root"],
                delivery["profile"], declaration)
        prior_result = request.get("previous")
        if prior_result and prior_result["reuse"]["origin"] == origin:
            previous = prior_result

    task_locator = _project_part(
        previous, reuse, "checkout", "task",
        lambda: {**_task_key(key), "task_ref": resolved.task_ref, "checkout_path": str(checkout.path)},
    )
    result = _result("no_current_delivery", mode, task=task_locator)
    if delivery is not None:
        result["kind"] = "terminal_delivery" if delivery["phase"] in {"delivered", "stopped"} else "current"
        result["delivery"] = _project_part(
            previous, reuse, "delivery", "delivery",
            lambda: {"delivery_id": delivery_id, "phase": delivery["phase"],
                     "planning_root": delivery["planning_root"]},
        )
    if reuse:
        result["reuse"] = reuse
    return result
