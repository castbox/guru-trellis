"""Bind an explicit shared PR to the existing Publication transaction writer."""
from __future__ import annotations

import hashlib
import json

from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.task_lifecycle import LifecycleContractError


def _snapshot(root, projection, commit, source):
    import owner as o
    try:
        value = json.loads(o.git_text(root, "show", f"{commit}:{source['task_ref']}/task.json"))
        record = projection._call(projection.api.delivery_schema.parse_task_v2, value)
        projection._call(projection.api.delivery_operations.get_gate_applicability, record, source["delivery_key"])
        selected = next(row for row in record["deliveries"] if row["id"] == source["delivery_key"]["delivery_id"]
                        and row["lifecycle_generation"] == source["delivery_key"]["lifecycle_generation"])
    except (ValueError, StopIteration, LifecycleContractError) as exc:
        raise o.WorkflowError("The selected commit does not carry this public Task/Delivery.", code="publication_stale") from exc
    return record, selected


def _shared_source(root, source, projection, selected, head, pr_head):
    import owner as o
    commit = source["source_commit"]
    for oid in {commit, head, pr_head}:
        if projection.commit(oid) != oid:
            raise o.WorkflowError("Make the exact source and PR commits available through the original Git fact owner.", code="publication_stale")
    if not (o.is_ancestor(root, commit, head) or o.is_ancestor(root, head, commit)):
        raise o.WorkflowError("Source and candidate commits have no supported ancestor relationship.", code="publication_stale")
    if not o.is_ancestor(root, pr_head, head):
        raise o.WorkflowError("The original PR head is not the candidate's fast-forward lineage.", code="pr_identity_stale")
    current = projection.read_record()
    for oid in {commit, head, pr_head}:
        record, delivery = _snapshot(root, projection, oid, source)
        if (any(record[field] != current[field] for field in ("id", "lifecycle_generation", "source", "base_branch"))
                or delivery["planning_root"] != selected["planning_root"] or delivery["profile"] != selected["profile"]
                or oid == commit and (record["accepted_scope"] != current["accepted_scope"]
                    or any(delivery[field] != selected[field] for field in ("scope_ref", "plan_ref"))
                    or delivery["results"]["planning"] != selected["results"]["planning"])):
            raise o.WorkflowError("Shared source, PR and current Planning belong to different Task/Delivery authority.", code="publication_stale")
        for name in ("prd.md", "design.md", "implement.md", "implement.jsonl", "check.jsonl"):
            o.git_text(root, "show", f"{oid}:{source['task_ref']}/{delivery['planning_root']}/{name}")
    return o.git_text(root, "diff", "--name-only", head, commit).splitlines()


def plan(root, source, existing, ref):
    import owner as o
    _task_dir, task = o.task_context(root, source["task_ref"])
    projection = DeliveryProjection(root, source["task_ref"])
    projection.selection_preflight(source["delivery_key"])
    selected = projection.resolve(source["delivery_key"])
    repo = o.repository_identity(root)
    if repo != source["pr_ref"]["repo_ref"]:
        return o.blocked("repository_identity_mismatch", "Use the exact PR in this Task's repository.")
    pr = o.read_pr(root, source["pr_ref"]["pr_number"])
    branch = pr["head_branch"]
    raw = {"state": pr["state"], "headRefName": branch, "baseRefName": pr["base_branch"],
           "url": pr["url"], "headRepositoryOwner": pr["head_owner"]}
    if not o.same_repo_pr(raw, repo, branch, task["base_branch"]):
        return o.blocked("pr_identity_mismatch", "Recover only the specified same-repository Open PR and original target.")
    remote = o.remote_head(root, branch)
    if remote != pr["head_sha"]:
        return o.blocked("remote_pr_head_mismatch", "Read matching remote ref and PR head before resuming Publication.")
    ready = source["profile"] == "delivery_remote_ready_recovery"
    head = source["reviewed_head"] if ready else source["candidate_head"]
    delta = _shared_source(root, source, projection, selected, head, pr["head_sha"])
    applicability = projection.gate_applicability(source["delivery_key"])
    planning = selected["results"]["planning"]
    if (planning is None or planning["outcome"] != "accepted" or applicability["planning"]["kind"] != "applicable"):
        raise o.WorkflowError("Restore current accepted Planning through its original owner.", code="publication_stale")
    publication = selected["publication_result"]
    if ready:
        readiness = selected["results"]["readiness"]
        candidate = selected["candidate"]
        if (readiness is None or readiness["result_id"] != source["readiness_result_id"]
                or applicability["readiness"]["kind"] != "applicable"
                or candidate is None or candidate["kind"] != "git" or candidate["head_ref"] != head):
            return {"typed_exit": "review_stale", "output": {"exit_id": "review_stale", "task_ref": source["task_ref"],
                    "delivery_key": source["delivery_key"], "stale_reason": "readiness_changed"}}
        base = candidate["base_ref"]
        if publication is not None and (publication["repo_ref"] != repo or publication["pr_number"] != pr["number"]
                or publication["candidate"] != candidate or publication["reviewed_head"] != head
                or publication["target_ref"] != task["base_branch"]
                or publication["publication_ref"]["revision"] != "sha256:" + hashlib.sha256(source["pr_body"].encode()).hexdigest()):
            raise o.WorkflowError("Recover the exact original public Publication and payload.", code="publication_stale")
    else:
        if selected["phase"] != "implementing":
            raise o.WorkflowError("Return publishing revisions through the original return-to-Draft owner first.", code="publication_stale")
        base = source["base_ref"]
    if (projection.commit(base) != base or projection.content_base(source["delivery_key"], development_base=base) != base
            or not o.is_ancestor(root, base, head) or not o.git_text(root, "diff", "--name-only", base, head)):
        raise o.WorkflowError("Retain this Delivery's fixed nonempty B..H range.", code="publication_stale")
    for authority in [selected["scope_ref"]["authority"], selected["plan_ref"], *planning["evidence"], *planning["obligations"]]:
        projection._call(projection.api.delivery_store.verify_authority, root, authority)
    if existing and existing.get("candidate_pr", {}).get("number") != pr["number"]:
        raise o.WorkflowError("Resume the same explicitly selected PR.", code="pr_identity_stale")
    effects = []
    if not ready and not pr["is_draft"]:
        effects.append("ensure_draft")
    if remote != head:
        effects.append("push_content")
    if pr["title"] != source["pr_title"] or pr["body"] != source["pr_body"]:
        effects.append("converge_metadata")
    if ready and pr["is_draft"]:
        effects.append("mark_ready")
    identity = {"task_ref": source["task_ref"], "delivery_key": source["delivery_key"], "repo_ref": repo,
                "pr_number": pr["number"], "base_branch": task["base_branch"], "head_branch": branch,
                "remote_ref": "refs/heads/" + branch,
                "source_commit": source["source_commit"], "base_ref": base, "reviewed_head": head,
                "expected_remote_head": remote, "pr_title": source["pr_title"],
                "pr_body_sha256": hashlib.sha256(source["pr_body"].encode()).hexdigest(), "maximum_side_effects": effects}
    return {"typed_exit": "preview", "transaction_ref": ref, "transaction_stage": existing["stage"] if existing else ("push_content" if ready else "ensure_draft"),
            "confirmation_identity": o.digest(identity), "plan_identity": identity, "input": source,
            "public_candidate": selected["candidate"] if ready else None, "public_publication": publication if ready else None,
            "repo_ref": repo, "base_branch": task["base_branch"], "head_branch": branch, "remote_head": remote,
            "candidate_pr": pr, "reviewed_head": head, "base_ref": base, "source_delta_paths": delta,
            "local_delta_paths": o.git_text(root, "diff", "--name-only", head).splitlines(),
            "working_tree_status": o.git_text(root, "status", "--porcelain").splitlines(),
            "candidate_paths": o.git_text(root, "diff", "--name-only", base, head).splitlines(),
            "push_required": remote != head, "create_pr_required": False,
            "metadata_convergence_required": "converge_metadata" in effects,
            "ready_transition_required": "mark_ready" in effects, "terminal_recovery": not effects}


def initial(context):
    import owner as o
    ready = context["input"]["profile"] == "delivery_remote_ready_recovery"
    if ready:
        tx = o.initial_transaction(context)
        tx["public_publication"] = context["public_publication"]
    else:
        from draft import initial as draft_initial
        tx = draft_initial(context)
    tx["existing_pr_number"] = context["candidate_pr"]["number"]
    return tx
