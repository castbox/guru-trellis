"""Bind one completed independent judgment to the two required public results."""
from __future__ import annotations

import hashlib
import json

from common import dirty_paths, git
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.delivery_projection.gates import record_gate, rework
from runtime.io import CommandError


def candidate(projection, public, *, recovery=False, implementation_reentry=False):
    key = public["delivery_key"]
    current = projection.current(key)
    if current.get("kind") != "current" or current.get("key") != key:
        raise CommandError("stale_identity", "delivery_key", "Use the exact selected active Delivery.", 3)
    delivery = projection.resolve(key)
    allowed = {"planning"} if recovery else {"implementing"} if implementation_reentry else {"checking", "reviewing"}
    if delivery["phase"] not in allowed:
        raise CommandError("stale_identity", "delivery.phase", "Bind the committed candidate through implementation/begin_check, or recover the original rollback.", 3)
    value = delivery["candidate"]
    head = public.get("task_head", public.get("branch_review_commit"))
    base = value["base_ref"] if value and public["profile"] == "delivery_base_continuity" else public.get("base_ref")
    if (value is None or value["kind"] != "git" or value["head_ref"] != head
            or value["base_ref"] != base or head != git(projection.root, "rev-parse", "HEAD")
            or dirty_paths(projection.root, public["task_ref"])):
        raise CommandError("stale_identity", "candidate", "Review the complete clean committed candidate with its fixed content base.", 3)
    projection._call(projection.api.delivery_store.verify_candidate, projection.root, value)
    if not recovery and not implementation_reentry:
        if projection.gate_applicability(key)["planning"]["kind"] != "applicable":
            raise CommandError("stale_identity", "planning", "Return changed Planning to its original owner.", 3)
        for ref in [delivery["scope_ref"]["authority"], delivery["plan_ref"], *delivery["results"]["planning"]["evidence"]]:
            projection._call(projection.api.delivery_store.verify_authority, projection.root, ref)
    declaration = projection.declaration()["owners"]
    if declaration["check"] != "guru-review-branch" or declaration["full_review"] != "guru-review-branch":
        raise CommandError("stale_identity", "owners", "Install the matching post-commit Review workflow and package together.", 3)
    return delivery


def review_binding(projection, key):
    delivery = projection.resolve(key)
    planning = delivery["results"]["planning"]
    return {"candidate": delivery["candidate"], "scope_ref": delivery["scope_ref"],
            "plan_ref": delivery["plan_ref"],
            "planning_result_id": planning["result_id"] if planning else None}


def validate_review_binding(projection, owner):
    actual = review_binding(projection, owner["delivery_key"])
    expected = owner["review_binding"]
    if (any(actual[name] != expected[name] for name in ("candidate", "scope_ref", "plan_ref"))
            or (actual["planning_result_id"] != expected["planning_result_id"]
                and not (owner["typed_exit"] == "planning_stale" and actual["planning_result_id"] is None))):
        raise CommandError("stale_identity", "review_binding", "Review the current scope, plan, Planning result and complete committed candidate.", 3)


def result_id(owner, role):
    # Timestamp is not a semantic result identity. Both roles name the same
    # actual result without deriving either outcome from the other role.
    value = {name: item for name, item in owner.items() if name not in {"generated_at", "facts_sha256"}}
    return role.replace("_", "-") + ":" + hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def passed(projection, public, owner):
    key = public["delivery_key"]
    candidate(projection, public)
    evidence = [authority_ref(projection.planning_directory(key) / "implement.md", projection.root)]
    for role in ("check", "full_review"):
        judgment = owner["gate_judgments"][role]
        if judgment["outcome"] != "passed":
            raise CommandError("schema_mismatch", "gate_judgments." + role, "Record each actual passing responsibility before its public result.")
        identity = result_id(owner, role)
        delivery = projection.resolve(key)
        prior = delivery["results"][role]
        if prior is not None and prior["result_id"] == identity:
            if projection.gate_applicability(key)[role]["kind"] != "applicable":
                raise CommandError("stale_identity", role, "Recover only the exact applicable result.", 3)
            continue
        if role == "check" and delivery["phase"] != "checking":
            raise CommandError("stale_identity", "check", "A different historical Check is not this review; use original rework/migration.", 3)
        record_gate(projection, key, role, identity, judgment["outcome"], evidence, [])
    return result_id(owner, "full_review")


def recover_pass(projection, public):
    delivery = candidate(projection, public)
    checks = projection.gate_applicability(public["delivery_key"])
    check, full = (delivery["results"][name] for name in ("check", "full_review"))
    if (check is None or full is None or checks["check"]["kind"] != "applicable"
            or checks["full_review"]["kind"] != "applicable"
            or check["owner_id"] != "guru-review-branch" or full["owner_id"] != "guru-review-branch"
            or full["predecessor_result_id"] != check["result_id"]
            or any(row["outcome"] != "passed" or row["candidate"] != delivery["candidate"] for row in (check, full))):
        raise CommandError("stale_identity", "review_result", "Recover the original semantic result for a missing step, or perform the actual independent review.", 3)
    return full["result_id"]


def rollback_binding(projection, public):
    delivery = projection.resolve(public["delivery_key"])
    return {"delivery_key": public["delivery_key"], "candidate": delivery["candidate"],
            "scope_ref": delivery["scope_ref"], "plan_ref": delivery["plan_ref"],
            "planning": delivery["results"]["planning"]}


def planning_stale(projection, public, owner):
    revision = owner["planning_revision"]
    binding = owner["rollback_binding"]
    if not revision or not binding:
        raise CommandError("schema_mismatch", "planning_revision", "Retain the actual planning repair and original rollback binding.")
    route = revision["planning_route"]
    if (route == "reapprove_plan" and (revision["proposal_refs"] or not revision["revision_actions"])) or (route == "clarify_requirements" and not revision["proposal_refs"]):
        raise CommandError("schema_mismatch", "planning_revision", "Current-scope repairs need concrete revision_actions; real scope changes need proposal_refs.")
    for ref in [binding["scope_ref"]["authority"], binding["plan_ref"], *binding["planning"]["evidence"]]:
        projection._call(projection.api.delivery_store.verify_authority, projection.root, ref)
    key = public["delivery_key"]
    delivery = projection.resolve(key)
    if delivery["phase"] == "planning":
        if (any(delivery["results"][name] is not None for name in ("planning", "check", "full_review", "readiness"))
                or any(binding[name] != delivery[name] for name in ("candidate", "scope_ref", "plan_ref"))):
            raise CommandError("stale_identity", "rollback_binding", "Recover only this already completed planning rollback.", 3)
        candidate(projection, public, recovery=True)
    else:
        candidate(projection, public)
        if binding != rollback_binding(projection, public):
            raise CommandError("stale_identity", "rollback_binding", "Use the original current planning/candidate binding.", 3)
        role = "check" if delivery["phase"] == "checking" else "full_review"
        rework(projection, key, role, "planning", authority_ref(projection.planning_directory(key) / "prd.md", projection.root), ["planning", "check", "full_review", "readiness"])
    output = {"exit_id": "planning_stale", "task_ref": public["task_ref"], "delivery_key": key,
              "planning_route": route, "proposal_refs": revision["proposal_refs"]}
    if route == "reapprove_plan":
        output["revision_actions"] = revision["revision_actions"]
    return output
