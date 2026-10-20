from __future__ import annotations

import base64
import json
import re
import subprocess
from typing import Any

from ..io import CommandError
from ..schema import validate_json
from .errors import LifecycleContractError
from .git_facts import RepositoryFacts
from .identity import resolve_task_id
from .schema import CONTRACT_ROOT, validate_dto


def closure_carrier_path(result_ref: dict[str, Any]) -> str:
    encoded = base64.urlsafe_b64encode(result_ref["result_id"].encode("utf-8")).decode("ascii").rstrip("=")
    return f"closeout/closure/{encoded}.json"


def read_shared_closure_result(projection: Any, result_ref: dict[str, Any], authority: dict) -> dict:
    """Read the exact minimal carrier through the installed authority resolver."""
    result = validate_dto("ResultRefDTO", result_ref)
    record = projection.read_record()
    store = projection.api.delivery_store
    context = projection._call(store.artifact_context, projection.task_dir, projection.root, record)
    suffix = "/" + closure_carrier_path(result)
    expected = {projection.task_ref + suffix, (record.get("artifact_origin") or projection.task_ref) + suffix}
    if authority["locator"] not in expected:
        raise LifecycleContractError("closure_result_stale", "shared_result", "Select the exact Task-owned Closure carrier.")
    try:
        projection._call(store.verify_authority, projection.root, authority, context)
        locator = projection._call(store.authority_locator, authority, context)
        if re.fullmatch(r"[a-f0-9]{40}(?:[a-f0-9]{24})?", authority["revision"]):
            raw = subprocess.run(["git", "show", f"{authority['revision']}:{locator}"], cwd=projection.root,
                                 text=True, capture_output=True, check=True).stdout
        else:
            raw = (projection.root / locator).read_text(encoding="utf-8")
        payload = json.loads(raw)
        schema = CONTRACT_ROOT.parents[1] / "packages/guru-complete-task-closure/schemas/shared-result.schema.json"
        validate_json(payload, schema, "shared_result")
    except (CommandError, OSError, ValueError, subprocess.SubprocessError) as exc:
        raise LifecycleContractError("closure_result_invalid", "shared_result", "Read the original Closure carrier at its exact authority revision.") from exc
    if (payload["result_ref"] != result or record["id"] != result["task_id"]
            or record["lifecycle_generation"] != result["lifecycle_generation"]):
        raise LifecycleContractError("closure_result_stale", "result_ref", "Use the exact current Closure result and Task generation.")
    completion = next((row for row in record["completion_results"]
                       if row["result_id"] == payload["completion_result_id"]), None)
    if (completion is None or completion["lifecycle_generation"] != result["lifecycle_generation"]
            or completion["accepted_scope"] != record["accepted_scope"]):
        raise LifecycleContractError("closure_result_stale", "completion_result", "Review the current public Completion and accepted scope.")
    actions, source = payload["action_set"], payload["source"]
    identities = [(row["issue_ref"]["repo_ref"], row["issue_ref"]["issue_number"]) for row in actions]
    if len(identities) != len(set(identities)) or (source["kind"] == "no_issue" and actions):
        raise LifecycleContractError("closure_result_stale", "action_set", "Read one consistent Closure action set.")
    if source["kind"] == "issue":
        exact = next((row for row in actions if row["issue_ref"] == {
            "repo_ref": source["repo_ref"], "issue_number": source["number"]}), None)
        if (exact is None or source["disposition"] == "exact_source" and exact["disposition"] == "no_close_authority"
                or source["disposition"] != "exact_source" and any(row["disposition"] != "no_close_authority" for row in actions)):
            raise LifecycleContractError("closure_result_stale", "source", "Read the reviewed source relation and its precise action.")
    return payload


def read_terminal_closure_result(repository: RepositoryFacts, result_ref: dict[str, Any]) -> dict[str, Any]:
    """Project the public Closure and its shared carrier to Finish snapshot 2.0."""
    from ..delivery_projection.adapter import DeliveryProjection

    result = validate_dto("ResultRefDTO", result_ref)
    root = repository.context_path
    artifact = resolve_task_id(root, result["task_id"])
    projection = DeliveryProjection(root, artifact.task_ref)
    record = projection.read_record()
    closure = next((row for row in record["closure_results"] if row["result_id"] == result["result_id"]
                    and row["lifecycle_generation"] == result["lifecycle_generation"]), None)
    if closure is None:
        raise LifecycleContractError("closure_result_stale", "closure_result", "Recover the exact public Closure result through its original owner.")
    suffix = "/" + closure_carrier_path(result)
    wanted = {artifact.task_ref + suffix, (record.get("artifact_origin") or artifact.task_ref) + suffix}
    carriers = [ref for ref in closure["evidence"] if ref["locator"] in wanted]
    if len(carriers) != 1:
        raise LifecycleContractError("closure_result_missing", "closure_result", "The original Closure owner must provide its exact shared action-set input.")
    payload = read_shared_closure_result(projection, result, carriers[0])
    source, actions = payload["source"], payload["action_set"]
    source_closed = source["kind"] == "issue" and any(
        row["issue_ref"] == {"repo_ref": source["repo_ref"], "issue_number": source["number"]}
        and row["disposition"] in {"close", "already_closed_at_review"} for row in actions)
    source_fact = ({"locator": f"https://github.com/{source['repo_ref']}/issues/{source['number']}", "revision": "CLOSED"}
                   if source_closed else None)
    if (closure["completion_result_id"] != payload["completion_result_id"]
            or closure["disposition"] != ("source_closed" if source_closed else "no_mutation")
            or closure["source_result"] != source_fact):
        raise LifecycleContractError("closure_result_stale", "closure_result", "Read matching public Closure, Completion, source and actions.")
    return {"result_ref": result,
            "terminal": "closed" if any(row["disposition"] in {"close", "already_closed_at_review"} for row in actions) else "no_mutation",
            "action_set": actions, "source": source}
