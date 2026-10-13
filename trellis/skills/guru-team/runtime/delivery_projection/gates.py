"""Thin projections of completed Guru judgments into the public owner API.

Callers own semantic outcomes. This module keeps no state, selects no route,
and delegates identity, applicability and transitions to the installed API.
"""
from __future__ import annotations


def record_gate(projection, key: dict, role: str, result_id: str,
                outcome: str, evidence: list[dict], obligations: list[dict]) -> dict:
    delivery = projection.resolve(key)
    predecessor = {"check": "planning", "full_review": "check", "readiness": "full_review"}[role]
    owner_id = projection.declaration()["owners"][role]
    result = {"result_id": result_id, "owner_role": role, "owner_id": owner_id,
              "outcome": outcome, "scope_ref": delivery["scope_ref"],
              "plan_ref": delivery["plan_ref"], "candidate": delivery["candidate"],
              "predecessor_result_id": delivery["results"][predecessor]["result_id"],
              "obligations": obligations, "evidence": evidence}
    return projection.apply({"api_version": "1.0", "operation": "record_gate",
                             "key": key, "owner_role": role, "owner_id": owner_id,
                             "expected_phase": delivery["phase"], "result": result})


def rework(projection, key: dict, owner_role: str, target_role: str,
           reason: dict, affected_results: list[str], *, scope_ref: dict | None = None) -> dict:
    delivery = projection.resolve(key)
    operation = {"api_version": "1.0", "operation": "rework", "key": key,
                             "owner_role": owner_role,
                             "owner_id": projection.declaration()["owners"][owner_role],
                             "expected_phase": delivery["phase"], "target_role": target_role,
                             "reason": reason, "affected_results": affected_results}
    if scope_ref is not None:
        operation["scope_ref"] = scope_ref
    return projection.apply(operation)
