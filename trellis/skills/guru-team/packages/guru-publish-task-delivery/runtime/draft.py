"""Draft actions inside the existing Publication transaction and recovery owner."""
from __future__ import annotations

import hashlib
from pathlib import Path

from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.delivery_projection.gates import rework
from runtime.task_lifecycle import LifecycleContractError
from runtime.schema import validate_json


def plan(root, source, existing, ref):
    import owner as o
    if existing is not None and existing["stage"] in o.TERMINALS:
        return {"typed_exit": "historical_terminal", "output": output(root, existing)}
    _task_dir, task = o.task_context(root, source["task_ref"])
    projection = DeliveryProjection(root, source["task_ref"])
    projection.selection_preflight(source["delivery_key"])
    selected = projection.resolve(source["delivery_key"])
    returning = source["profile"] == "delivery_return_to_draft"
    if returning:
        # A recorded action may already have performed its public rework before
        # losing command output. It still owns the same PR mutation.
        allowed = {"publishing", "implementing"} if existing else {"publishing"}
        if selected["phase"] not in allowed:
            raise o.WorkflowError("Return the current publishing Delivery through its Publication owner.", code="publication_stale")
        head = existing["reviewed_head"] if existing else o.git_text(root, "rev-parse", "HEAD")
        base = (selected.get("candidate") or {}).get("base_ref")
    else:
        # Planning applicability is public; no Check checkpoint or gate is read.
        planning = selected["results"]["planning"]
        if (selected["phase"] != "implementing" or planning is None or planning["outcome"] != "accepted"
                or projection.gate_applicability(source["delivery_key"])["planning"]["kind"] != "applicable"):
            raise o.WorkflowError("Draft publication requires current activated Planning in implementation.", code="publication_stale")
        for reference in [selected["scope_ref"]["authority"], selected["plan_ref"], *planning["evidence"], *planning["obligations"]]:
            projection._call(projection.api.delivery_store.verify_authority, root, reference)
        base, head = source["base_ref"], source["candidate_head"]
        if (projection.commit(base) != base or projection.content_base(source["delivery_key"], development_base=base) != base
                or projection.commit(head) != head or not o.git_text(root, "diff", "--name-only", base, head)):
            raise o.WorkflowError("Use the fixed nonempty complete content range.", code="publication_stale")
    if o.git_text(root, "rev-parse", "HEAD") != head:
        raise o.WorkflowError("The selected Draft candidate HEAD changed; recover the old action first.", code="publication_stale")
    repo = o.repository_identity(root)
    candidates = o.list_open_prs(root, task["branch"])
    if len(candidates) > 1 or any(not o.same_repo_pr(row, repo, task["branch"], task["base_branch"]) for row in candidates):
        raise o.WorkflowError("Use the unique same-repository Open PR and exact target.", code="pr_identity_stale")
    pr = o.normalize_pr(candidates[0]) if candidates else None
    remote = o.remote_head(root, task["branch"])
    if returning and (pr is None or pr["head_sha"] != head):
        raise o.WorkflowError("Return the original current PR at its actual published HEAD.", code="pr_identity_stale")
    if pr and remote != pr["head_sha"]:
        raise o.WorkflowError("The remote branch and PR HEAD differ.", code="pr_identity_stale")
    if remote and remote != head and not o.is_ancestor(root, remote, head):
        raise o.WorkflowError("Draft update requires the original fast-forward lineage.", code="publication_stale")
    if existing:
        original = existing.get("candidate_pr")
        if original and (pr is None or pr["number"] != original["number"]):
            raise o.WorkflowError("The original PR identity changed.", code="pr_identity_stale")
    effects = ["ensure_draft"] if returning else ["ensure_draft", "push_content", "bind_pr", "converge_metadata"]
    identity = {"task_ref": source["task_ref"], "delivery_key": source["delivery_key"], "repo_ref": repo,
                "base_branch": task["base_branch"], "head_branch": task["branch"], "reviewed_head": head,
                "action": "return_to_draft" if returning else "draft_publish", "maximum_side_effects": effects}
    if not returning:
        identity.update(pr_title=source["pr_title"], pr_body_sha256=hashlib.sha256(source["pr_body"].encode()).hexdigest())
    else:
        identity.update(pr_number=pr["number"], revision_reason=source["revision_reason"])
    return {"typed_exit": "preview", "transaction_ref": ref, "transaction_stage": existing["stage"] if existing else "ensure_draft",
            "confirmation_identity": o.digest(identity), "plan_identity": identity, "input": source,
            "public_candidate": None, "repo_ref": repo, "base_branch": task["base_branch"], "head_branch": task["branch"],
            "remote_head": remote, "candidate_pr": pr, "reviewed_head": head, "base_ref": base,
            "push_required": not returning and remote != head, "create_pr_required": not returning and pr is None,
            "metadata_convergence_required": bool(not returning and pr and (pr["title"] != source["pr_title"] or pr["body"] != source["pr_body"])),
            "ready_transition_required": False, "terminal_recovery": False}


def initial(context):
    import owner as o
    returning = context["input"]["profile"] == "delivery_return_to_draft"
    source = context["input"]
    # Use the same push/bind/metadata writer as final Publication.
    tx = o.initial_transaction({**context, "input": {**source, "reviewed_head": context["reviewed_head"]}})
    tx["input"] = source
    tx.update(action="return_to_draft" if returning else "draft_publish", terminal="draft_revision" if returning else "draft",
              stage="ensure_draft", base_ref=context["base_ref"])
    pr = context["candidate_pr"]
    tx["decisions"]["draft"] = {"pr_number": pr["number"] if pr else None,
        "head_sha": pr["head_sha"] if pr else None, "original_is_draft": pr["is_draft"] if pr else None,
        "mutation_required": bool(pr and not pr["is_draft"])}
    return tx


def ensure_draft(root, tx):
    import owner as o
    decision = tx["decisions"]["draft"]
    pr = o.find_bindable_pr(root, tx)
    if decision["pr_number"] is None:
        if pr is not None:
            raise o.WorkflowError("An unexpected PR appeared before the recorded Draft action.", code="pr_identity_stale")
    else:
        if pr is None or pr["number"] != decision["pr_number"] or pr["head_sha"] != decision["head_sha"]:
            raise o.WorkflowError("Draft preimage no longer names the original PR/HEAD.", code="pr_identity_stale")
        if not pr["is_draft"]:
            if not decision["mutation_required"] or decision["original_is_draft"] is not False:
                raise o.WorkflowError("Draft state differs from this action's recorded preimage/postimage.", code="pr_identity_stale")
            o._run(root, ["gh", "pr", "ready", str(pr["number"]), "--repo", tx["repo_ref"], "--undo"], allow_failure=True)
            pr = o.read_pr(root, pr["number"])
            if not pr["is_draft"] or pr["head_sha"] != decision["head_sha"]:
                raise o.WorkflowError("Return-to-Draft mutation did not converge.", code="external_command_failed")
    if tx["action"] == "return_to_draft":
        projection = DeliveryProjection(root, tx["input"]["task_ref"])
        key = tx["input"]["delivery_key"]
        selected = projection.resolve(key)
        if selected["phase"] == "publishing":
            reason = authority_ref(projection.planning_directory(key) / "implement.md", root)
            rework(projection, key, "publication", "implementation", reason, ["check", "full_review", "readiness"])
        elif selected["phase"] != "implementing" or any(selected["results"][name] is not None for name in ("check", "full_review", "readiness")):
            raise o.WorkflowError("Recover the original public revision transition.", code="publication_stale")
        tx["bound_pr"] = {"number": pr["number"], "url": pr["url"], "head_sha": pr["head_sha"]}
        tx["stage"] = "draft_revision"
    else:
        tx["stage"] = "push_content"
    o.save_transaction(root, tx)


def output(root, tx):
    import owner as o
    bound = tx.get("bound_pr")
    if not isinstance(bound, dict):
        raise o.WorkflowError("Draft result lacks the original PR binding.", code="private_state_invalid")
    pr = o.read_pr(root, bound["number"])
    source = tx["input"]
    if pr["state"] != "OPEN" or not pr["is_draft"] or pr["head_sha"] != tx["reviewed_head"]:
        raise o.WorkflowError("Draft terminal PR/HEAD facts changed.", code="publication_stale")
    result = {"task_ref": source["task_ref"], "delivery_key": source["delivery_key"], "repo_ref": tx["repo_ref"], "pr_number": pr["number"]}
    if tx["terminal"] == "draft":
        if pr["title"] != source["pr_title"] or pr["body"] != source["pr_body"]:
            raise o.WorkflowError("Draft terminal payload changed.", code="publication_stale")
        result.update(exit_id="draft_published", base_ref=source["base_ref"], candidate_head=source["candidate_head"])
    else:
        result["exit_id"] = "draft_revision_ready"
    package = Path(__file__).resolve().parents[1]
    validate_json(result, package / ("schemas/public-output-delivery-" + result["exit_id"].replace("_", "-") + "-1.0.schema.json"), "stdout")
    return result
