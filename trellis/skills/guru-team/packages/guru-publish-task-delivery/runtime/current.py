"""Validate the authored readiness result and project the exact pending action."""
from __future__ import annotations

import copy

import owner as o
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.delivery_projection.gates import record_gate, rework
from runtime.reviewed_content import ReviewedContentError, reviewed_content_identity
from runtime.schema import validate_json
from runtime.task_lifecycle import LifecycleContractError

PREPARE = "delivery_prepare_publication"
EXECUTE = "delivery_execute_publication"
DISCLOSURES = ("slice_summary", "remaining_work", "unverified_boundaries")
READY_POSTIMAGE_STAGES = {"converge_metadata", "mark_ready", "ready"}


def _identity(public):
    return {name: public[name] for name in ("mode", "task_ref", "delivery_key")}


def _route(public, name, **details):
    return {"exit_id": name, "task_ref": public["task_ref"], "delivery_key": public["delivery_key"], **details}


def _selection(root, public):
    projection = DeliveryProjection(root, public["task_ref"])
    selected = projection.current(public["delivery_key"])
    if (selected["kind"] not in {"current", "terminal_delivery"}
            or selected["key"] != public["delivery_key"]):
        raise o.WorkflowError("Select the exact current Delivery.", code="task_identity_stale")
    return projection, selected["delivery"], selected["gate_applicability"]


def _original_transaction(root, public, delivery):
    directory = o.transaction_path(root, "0" * 64).parent
    active = []
    ready = []
    for path in sorted(directory.glob("*.json")):
        if path.name.endswith(".gate.json"):
            continue
        value = o.read_json(path)
        identity = value.get("input", {})
        if (identity.get("task_ref"), identity.get("delivery_key")) != (public["task_ref"], public["delivery_key"]):
            continue
        stage = value.get("stage")
        if stage not in o.TERMINALS:
            o.validate_transaction(value)
            active.append(value)
        elif stage == "ready" and value.get("public_candidate") == delivery["candidate"]:
            publication = delivery["publication_result"]
            original = value.get("public_publication")
            result_id = original["result_id"] if original else "publication:" + value["transaction_ref"]
            readiness_id = (delivery["results"]["readiness"] or {}).get("result_id")
            if (publication and publication["result_id"] == result_id
                    or publication is None and identity.get("readiness_result_id") == readiness_id):
                o.validate_transaction(value)
                ready.append(value)
    matches = active or ready
    if len(matches) > 1:
        raise o.WorkflowError("Recover the unique original Publication transaction.", code="private_state_invalid")
    return matches[0] if matches else None


def merged(root, public, delivery, transaction=None, selected_pr=None):
    publication = delivery["publication_result"]
    bound = transaction and (transaction.get("bound_pr") or transaction.get("candidate_pr"))
    bound_repo = transaction and transaction["repo_ref"]
    locator = ({"repo_ref": bound_repo, "pr_number": bound["number"]} if bound else
               publication or selected_pr)
    if locator is None:
        return None
    repo = o.repository_identity(root)
    if locator["repo_ref"] != repo:
        raise o.WorkflowError("Use this repository's exact original PR.", code="pr_identity_stale")
    if publication and (publication["repo_ref"], publication["pr_number"]) != (repo, locator["pr_number"]):
        raise o.WorkflowError("The original transaction and Publication name different PRs.", code="pr_identity_stale")
    pr = o.read_pr(root, locator["pr_number"])
    if pr["state"] != "MERGED":
        return None
    return _route(public, "merged_recovery_required" if publication else "merged_adoption_required",
                  mode=public["mode"], repo_ref=repo, pr_number=pr["number"])


def _current_review(root, public, projection, selected, applicability):
    review = selected["results"]["full_review"]
    candidate = selected["candidate"]
    head = public.get("branch_review_commit", public.get("reviewed_head"))
    if (review is None or applicability["full_review"]["kind"] != "applicable"
            or (public.get("full_review_result_id") is not None and public["full_review_result_id"] != review["result_id"])
            or candidate is None or candidate["head_ref"] != head):
        return _route(public, "review_stale", stale_reason="full_review_changed")
    try:
        projection._call(projection.api.delivery_store.verify_candidate, root, candidate)
    except LifecycleContractError as exc:
        if exc.code != "candidate_mismatch":
            raise
        return _route(public, "review_stale", stale_reason="reviewed_candidate_changed")
    architecture = public["architecture_assessment"]
    try:
        content_identity = "sha256:" + reviewed_content_identity(root)["sha256"]
    except ReviewedContentError as exc:
        raise o.WorkflowError(str(exc), code="publication_stale") from exc
    if (architecture["head"], architecture["content_identity"]) != (head, content_identity):
        return _route(public, "review_stale", stale_reason="publication_architecture_changed")
    return None


def _source(public):
    return {
        "profile": "delivery_review_ready",
        **_identity(public),
        **{key: public[key] for key in ("readiness_result_id", "reviewed_head", "pr_title", "pr_body", "remaining_work_state")},
    }


def _context(root, source, transaction, publication):
    if transaction:
        ref = transaction["transaction_ref"]
    else:
        source_ref = o.transaction_ref(source)
        ref = o.digest({"source_ref": source_ref, "previous_publication": publication["result_id"]}) if publication else source_ref
    context = o.plan_from_input(root, source, prepared_transaction=(ref, transaction))
    if context["typed_exit"] != "preview":
        return context
    current = context["candidate_pr"]
    bound = transaction and (transaction.get("bound_pr") or transaction.get("candidate_pr"))
    if publication and (not current or current["number"] != publication["pr_number"]
                        or context["repo_ref"] != publication["repo_ref"]):
        raise o.WorkflowError("Retain the existing published PR identity.", code="pr_identity_stale")
    if transaction and (
        (context["repo_ref"], context["base_branch"], context["head_branch"])
        != (transaction["repo_ref"], transaction["base_branch"], transaction["head_branch"])
        or bound and (not current or current["number"] != bound["number"])
    ):
        raise o.WorkflowError("Retain the existing transaction and original PR identity.", code="pr_identity_stale")
    return context


def _target(context):
    pr = context["candidate_pr"]
    actions = [
        effect for effect, required in (
            ("push_content", context["push_required"]),
            ("create_pr", context["create_pr_required"]),
            ("converge_metadata", context["metadata_convergence_required"]),
            ("mark_ready", context["create_pr_required"] or context["ready_transition_required"]),
        ) if required
    ]
    return {"repo_ref": context["repo_ref"], "base_branch": context["base_branch"],
            "head_branch": context["head_branch"], "remote_head": context["remote_head"],
            "pr_number": pr["number"] if pr else None, "actions": actions}


def _preview_identity(output, context):
    pr = context["candidate_pr"]
    preimages = {field: pr[field] for field in ("number", "head_sha", "state", "is_draft", "title", "body")} if pr else None
    return o.digest({"preview": {key: value for key, value in output.items() if key != "preview_identity"},
                     "pr_preimage": preimages, "transaction_ref": context["transaction_ref"]})


def prepare(package, root, public, semantic):
    from readiness import project_output, validate_semantic

    validate_json(public, package / "schemas/public-delivery-prepare-publication-input-1.0.schema.json", "input")
    projection, selected, applicability = _selection(root, public)
    transaction = _original_transaction(root, public, selected)
    merged_exit = merged(root, public, selected, transaction)
    if merged_exit:
        return merged_exit
    if transaction and transaction["action"] == "return_to_draft":
        return _recover_draft(root, transaction)
    if transaction and transaction["stage"] in READY_POSTIMAGE_STAGES:
        terminal = _ready_postimage(root, transaction)
        if terminal and (terminal["exit_id"] == "ready_for_merge" or selected["publication_result"] is None):
            return terminal
        if transaction["stage"] == "ready":
            transaction = None
    stale = _current_review(root, public, projection, selected, applicability)
    if stale:
        return stale

    outcome = validate_semantic(package, root, public, semantic, projection.read_record()["source"])
    key = public["delivery_key"]
    directory = projection.planning_directory(key)
    if selected["phase"] == "publishing" and outcome != "blocked":
        reason = authority_ref(directory / "implement.md", root)
        rework(projection, key, "publication", "readiness", reason, ["readiness"])
    elif selected["phase"] != "reviewing" and outcome != "blocked":
        raise o.WorkflowError("Publication preparation requires the current reviewed Delivery.", code="publication_stale")
    if outcome != "ready":
        output = project_output(public, semantic)
        if outcome in {"planning_revision_required", "implementation_required"}:
            planning = outcome == "planning_revision_required"
            reason = authority_ref(directory / ("prd.md" if planning else "implement.md"), root)
            rework(projection, key, "readiness", "planning" if planning else "implementation", reason,
                   ["planning", "check", "full_review", "readiness"] if planning else ["readiness"])
        return output

    readiness_id = "readiness:" + o.digest({"key": key, "semantic": semantic,
                         "predecessor": public["full_review_result_id"], "architecture": public["architecture_assessment"]})
    record_gate(projection, key, "readiness", readiness_id, "ready", [authority_ref(directory / "implement.md", root)], [])
    result = {"exit_id": "publication_prepared", **_identity(public), "readiness_result_id": readiness_id,
              "reviewed_head": public["branch_review_commit"], "pr_title": semantic["pr_payload"]["title"],
              "pr_body": semantic["pr_payload"]["body"], "remaining_work_state": semantic["remaining_work_state"],
              "architecture_assessment": public["architecture_assessment"],
              **{name: semantic[name] for name in DISCLOSURES}}
    context = _context(root, _source(result), transaction, selected["publication_result"])
    if context["typed_exit"] != "preview":
        return context["output"]
    result["target"] = _target(context)
    result["preview_identity"] = _preview_identity(result, context)
    return result


def execute(package, root, public, review, observed_identity):
    validate_json(public, package / "schemas/public-delivery-execute-publication-input-1.0.schema.json", "input")
    prepared = public["prepared"]
    projection, selected, applicability = _selection(root, prepared)
    transaction = _original_transaction(root, prepared, selected)
    merged_exit = merged(root, prepared, selected, transaction)
    if merged_exit:
        return merged_exit
    if transaction and transaction["action"] == "return_to_draft":
        return _recover_draft(root, transaction)
    if transaction and transaction["stage"] in READY_POSTIMAGE_STAGES:
        terminal = _ready_postimage(root, transaction)
        if terminal and (terminal["exit_id"] == "ready_for_merge" or selected["publication_result"] is None):
            return terminal
        if transaction["stage"] == "ready":
            transaction = None
    stale = _current_review(root, prepared, projection, selected, applicability)
    if stale:
        return stale
    source = o.validate_public_input(_source(prepared))
    try:
        context = _context(root, source, transaction, selected["publication_result"])
    except o.WorkflowError as exc:
        if exc.code in {"publication_stale", "remote_identity_stale", "pr_identity_stale"}:
            return _route(prepared, "reprepare_required", reason_code=exc.code)
        raise
    if context["typed_exit"] == "blocked":
        return _route(prepared, "reprepare_required", reason_code=context["output"]["reason_code"])
    if context["typed_exit"] != "preview":
        return context["output"]
    target = _target(context)
    # The caller compares the displayed result in dialogue. The writer only
    # compares this invocation's exact objective action to the earlier preview.
    if _preview_identity({**prepared, "target": target}, context) != prepared["preview_identity"]:
        return _route(prepared, "reprepare_required", reason_code="publication_preview_changed")
    if target["actions"] and observed_identity != prepared["preview_identity"]:
        return o.blocked("confirmation_identity_mismatch", "Use the exact current publication preview.")["output"]
    o.validate_review(review)
    if transaction:
        current = context["candidate_pr"]
        refreshed = copy.deepcopy(transaction)
        refreshed.setdefault("original_action", {
            field: transaction[field]
            for field in ("input", "stage", "initial_remote_head", "candidate_pr", "bound_pr", "decisions")
        })
        refreshed.update(input=source, reviewed_head=source["reviewed_head"], initial_remote_head=context["remote_head"],
                         public_candidate=context["public_candidate"], candidate_pr=current)
        refreshed["stage"] = "push_content" if context["push_required"] else "bind_pr"
        if current:
            refreshed["existing_pr_number"] = current["number"]
        o.save_transaction(root, refreshed)
    context["prepared_execution"] = True
    try:
        return o.execute(root, context)
    except o.WorkflowError as exc:
        if exc.code == "external_command_failed" and o.load_transaction(root, context["transaction_ref"]):
            return _route(prepared, "resume_publication", transaction_ref=context["transaction_ref"])
        if exc.code in {"publication_stale", "remote_identity_stale", "pr_identity_stale"}:
            return _route(prepared, "reprepare_required", reason_code=exc.code)
        raise


def _ready_postimage(root, transaction):
    pr = o.read_pr(root, transaction["bound_pr"]["number"])
    source = transaction["input"]
    if (pr["state"] == "OPEN" and not pr["is_draft"] and pr["head_sha"] == transaction["reviewed_head"]
            and (pr["title"], pr["body"]) == (source["pr_title"], source["pr_body"])):
        if transaction["stage"] != "ready":
            if (o.find_bindable_pr(root, transaction) != pr
                    or o.remote_head(root, transaction["head_branch"]) != transaction["reviewed_head"]):
                raise o.WorkflowError("Recover the exact PR and branch from the original Ready action.",
                                      code="pr_identity_stale")
            transaction["stage"] = "ready"
            o.save_transaction(root, transaction)
        return o.ready_output(root, transaction)
    return None


def _recover_draft(root, transaction):
    from draft import output

    if transaction["stage"] == "draft_revision":
        return output(root, transaction)
    context = o.exact_context(root, transaction)
    if not context["candidate_pr"]["is_draft"]:
        return o.blocked(
            "confirmation_identity_mismatch",
            "Preview and confirm the remaining action through the original return-to-Draft profile.",
        )["output"]
    return o.execute(root, context)


def recover(root, public):
    if "transaction_ref" in public:
        transaction = o.load_transaction(root, public["transaction_ref"])
        if not transaction:
            return _route(public, "review_stale", stale_reason="private_state_missing")
        o.validate_transaction(transaction)
        if any(transaction["input"][field] != public[field] for field in ("task_ref", "delivery_key")):
            raise o.WorkflowError("Recover the same Delivery transaction.", code="private_state_invalid")
    else:
        _, selected, _ = _selection(root, public)
        transaction = _original_transaction(root, public, selected)
    if transaction and transaction["stage"] in o.TERMINALS:
        selected = DeliveryProjection(root, public["task_ref"]).resolve(public["delivery_key"])
    else:
        _, selected, _ = _selection(root, public)
    output = merged(root, public, selected, transaction)
    if output:
        return output
    if transaction and transaction["action"] == "return_to_draft":
        return _recover_draft(root, transaction)
    if transaction and transaction["stage"] in READY_POSTIMAGE_STAGES:
        output = _ready_postimage(root, transaction)
        if output:
            return output
    return _route(public, "review_stale", stale_reason="publication_preparation_required")
