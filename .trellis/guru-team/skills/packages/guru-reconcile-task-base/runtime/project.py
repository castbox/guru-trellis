from __future__ import annotations

import argparse
import copy
from pathlib import Path

from common import parse, read_json, repo_root, resolve_commit, validate_json
from runtime.io import CommandError
from runtime.delivery_projection import DeliveryProjection
from runtime.task_lifecycle.errors import LifecycleContractError


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--authoring", required=True)
    args = parse(parser, argv)
    repo = repo_root(args.root)
    public = read_json(repo, package_root, args.input, "input")
    result = read_json(repo, package_root, args.result, "result")
    authoring = read_json(repo, package_root, args.authoring, "authoring")
    validate_json(public, package_root / "schemas/delivery-public-resolved-candidate-input-2.0.schema.json", "input")
    validate_json(result, package_root / "schemas/delivery-resolved-reconciliation-result-2.0.schema.json", "result")
    validate_json(authoring, package_root / "schemas/delivery-resolved-full-review-authoring-2.0.schema.json", "authoring")
    expected = {
        "task_ref": public["task_ref"],
        "delivery_key": public["delivery_key"],
        "branch": public["branch"],
        "committed_candidate_anchor": public["committed_candidate_anchor"],
        "old_base_head": public["old_base_head"],
        "new_base_head": public["new_base_head"],
        "merge_head": public["merge_head"],
        "stage0_tree": public["stage0_tree"],
        "index_tree_sha256": public["index_tree_sha256"],
        "parent_order": public["parent_order"],
        "commit_message": public["commit_message"],
    }
    if (
        any(result[key] != value for key, value in expected.items())
        or resolve_commit(repo, "HEAD", "HEAD") != result["reconciled_task_head"]
        or authoring["mode"] != public["mode"]
    ):
        raise CommandError("stale_identity", "result", "Use the exact current resolved reconciliation result and Branch Review authoring.", 3)
    projection = DeliveryProjection(repo, public["task_ref"])
    try:
        delivery = projection.resolve(public["delivery_key"])
        candidate = delivery["candidate"]
        base = resolve_commit(repo, authoring["base_ref"], "authoring.base_ref")
        if (delivery["phase"] != "checking" or candidate is None
                or candidate["head_ref"] != result["reconciled_task_head"]
                or candidate["base_ref"] != base
                or projection.content_base(public["delivery_key"]) != base):
            raise CommandError("stale_identity", "candidate", "Bind the reconciled HEAD with the original fixed base before committed Review.", 3)
        planning = delivery["results"]["planning"]
        if planning is None or projection.gate_applicability(public["delivery_key"])["planning"]["kind"] != "applicable":
            raise CommandError("stale_identity", "planning", "Restore applicable accepted Planning before committed Review.", 3)
        for authority in [delivery["scope_ref"]["authority"], delivery["plan_ref"], *planning["evidence"], *planning["obligations"]]:
            projection._call(projection.api.delivery_store.verify_authority, repo, authority)
        projection._call(projection.api.delivery_store.verify_candidate, repo, candidate)
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    output = {
        **copy.deepcopy(authoring),
        "task_ref": public["task_ref"],
        "delivery_key": public["delivery_key"],
        "branch_review_commit": result["reconciled_task_head"],
    }
    target = package_root.parent / "guru-review-branch/schemas/public-delivery-branch-review-input-2.0.schema.json"
    validate_json(output, target, "stdout")
    return output
