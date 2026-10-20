"""Task Commit candidate facts for one public Delivery, including clean reentry."""
from __future__ import annotations

import json
from pathlib import Path

from common import git, status_records
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.io import CommandError
from runtime.reviewed_content import reviewed_content_metadata_path
from runtime.schema import validate_json
from runtime.task_lifecycle import resolve_active_task_checkout
from runtime.task_lifecycle import LifecycleContractError
from migration import matches_committed, read_source


def _current_check(projection, public):
    delivery = projection.resolve(public["delivery_key"])
    check = delivery["results"]["check"]
    if (check is None or check["result_id"] != public["check_result_id"]
            or projection.gate_applicability(public["delivery_key"])["check"]["kind"] != "applicable"):
        raise CommandError("stale_identity", "check_result_id", "Run the current Delivery Check owner.", 3)
    try:
        projection._call(projection.api.delivery_store.verify_candidate, projection.root, delivery["candidate"])
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    if delivery["candidate"]["head_ref"] != git(projection.root, "rev-parse", "HEAD").stdout.strip():
        raise CommandError("stale_identity", "candidate.head_ref", "Run fresh Check at the actual committed HEAD.", 3)
    return delivery


def current_check(projection, public):
    try:
        return _current_check(projection, public)
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc


def current_draft(projection, public):
    """Validate accepted Planning and the fixed range without creating Check."""
    try:
        projection.selection_preflight(public["delivery_key"])
        delivery = projection.resolve(public["delivery_key"])
        planning = delivery["results"]["planning"]
        if (delivery["phase"] != "implementing" or planning is None
                or planning["outcome"] != "accepted"
                or projection.gate_applicability(public["delivery_key"])["planning"]["kind"] != "applicable"):
            raise CommandError("stale_identity", "planning", "Use the activated implementing Delivery with current accepted Planning.", 3)
        base = public["base_ref"]
        if projection.commit(base) != base or projection.content_base(public["delivery_key"], development_base=base) != base:
            raise CommandError("stale_identity", "base_ref", "Retain this Delivery's fixed complete base OID.", 3)
        for reference in [delivery["scope_ref"]["authority"], delivery["plan_ref"], *planning["evidence"], *planning["obligations"]]:
            projection._call(projection.api.delivery_store.verify_authority, projection.root, reference)
        return delivery
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc


def clean_candidate(projection, public):
    repo = projection.root
    early = public.get("profile") == "delivery_draft_committed_reentry"
    delivery = current_draft(projection, public) if early else current_check(projection, public)
    try:
        checkout = resolve_active_task_checkout(repo, public["task_ref"])
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    for marker in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply", "sequencer"):
        if Path(git(repo, "rev-parse", "--path-format=absolute", "--git-path", marker).stdout.strip()).exists():
            raise CommandError("stale_identity", "git_operation_state", "Finish the current Git operation with its owner.", 3)
    if any(not reviewed_content_metadata_path(row[1]) or (row[2] and not reviewed_content_metadata_path(row[2]))
           for row in status_records(repo)):
        raise CommandError("stale_identity", "worktree", "Use exact dirty candidate commit before committed reentry.", 3)
    record = projection.read_record()
    base = record["base_branch"]
    if not isinstance(base, str) or not base:
        raise CommandError("stale_identity", "base_branch", "Resolve the task selected base before Task Commit.", 3)
    base_ref = public["base_ref"] if early else delivery["candidate"]["base_ref"]
    if (base_ref is None or projection.commit(base_ref) != base_ref
            or not git(repo, "diff", "--name-only", base_ref, head).stdout.strip()):
        raise CommandError("stale_identity", "base_ref", "Use the current Check's fixed, nonempty complete content range.", 3)
    committed = git(repo, "show", f"HEAD:{public['task_ref']}/task.json", check=False)
    try:
        metadata = json.loads(committed.stdout)
    except ValueError as exc:
        raise CommandError("stale_identity", "task_metadata", "Commit the stable Task identity before reentry.", 3) from exc
    if committed.returncode or any(metadata.get(field) != record[field] for field in ("id", "lifecycle_generation", "source")):
        raise CommandError("stale_identity", "task_metadata", "Committed Task identity/source differs from current scope.", 3)
    # Gates and public migration update task.json after commit. A real Plan2
    # relocation may leave new planning paths absent from HEAD; only this
    # owner's reviewed original committed source bridge can cover that case.
    source = None
    for name in ("prd.md", "design.md", "implement.md", "implement.jsonl", "check.jsonl"):
        path = projection.planning_directory(public["delivery_key"]) / name
        if not path.is_file():
            raise CommandError("stale_identity", "planning", "Restore the complete Delivery planning context.", 3)
        relative = path.relative_to(repo).as_posix()
        direct = git(repo, "cat-file", "-e", "HEAD:" + relative, check=False).returncode == 0
        if direct:
            matches = matches_committed(repo, head, relative, path)
        else:
            source = source or read_source(projection_package(), repo, public["delivery_key"])
            matches = source is not None and matches_committed(repo, source["source_commit"], source["planning_sources"][name], path, source.get("planning_projection"))
        if not matches:
            raise CommandError("stale_identity", "planning", "Restore the original equivalent Plan2 source or commit genuine planning changes through the dirty path.", 3)
    if checkout.artifact.task_id != public["delivery_key"]["task_id"]:
        raise CommandError("stale_identity", "checkout", "Resolve the exact registered Task checkout.", 3)
    return delivery, head, base_ref


def projection_package():
    return Path(__file__).resolve().parents[1]


def invoke(package, repo, public, owner):
    validate_json(public, package / "schemas" / ("public-" + public["profile"].replace("_", "-") + "-input-1.0.schema.json"), "input")
    projection = DeliveryProjection(repo, public["task_ref"])
    if public["profile"] not in {"delivery_committed_reentry", "delivery_draft_committed_reentry"}:
        raise CommandError("invalid_arguments", "profile", "Use the reviewed exact-commit candidate entry for dirty work.")
    validate_json(owner, package / "schemas/delivery-commit-review-1.0.schema.json", "owner_result")
    _delivery, head, base_ref = clean_candidate(projection, public)
    if owner["status"] == "passed":
        if public["profile"] == "delivery_draft_committed_reentry":
            output = {"exit_id": "draft_committed", "task_ref": public["task_ref"], "delivery_key": public["delivery_key"], "base_ref": base_ref, "commit_sha": head}
        else:
            output = {"exit_id": "committed", "task_ref": public["task_ref"], "delivery_key": public["delivery_key"],
                      "base_ref": base_ref, "branch_review_commit": head, "check_result_id": public["check_result_id"]}
    elif owner["status"] == "revision-required":
        output = {"exit_id": "revision-required", "task_ref": public["task_ref"], "delivery_key": public["delivery_key"]}
    else:
        output = {"exit_id": "blocked"}
    validate_json(output, package / "schemas" / ("public-output-delivery-" + output["exit_id"].replace("_", "-") + "-1.0.schema.json"), "stdout")
    return output
