"""Validate immutable attribution and record an already merged Delivery."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess

from manual_recovery import blocked, immutable_candidate, merged_pr_facts, record_terminal_delivery, reviewed_pr
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.io import CommandError
from runtime.reviewed_content import reviewed_content_metadata_path
from runtime.schema import validate_json
from runtime.task_lifecycle import LifecycleContractError


def _git_bytes(root, *args):
    result = subprocess.run(["git", *args], cwd=root, capture_output=True)
    if result.returncode:
        raise CommandError("stale_identity", "repository.commit", "Read the exact Git objects for this PR and merge.", 3)
    return result.stdout


def _blob(root, commit, path):
    entry = _git_bytes(root, "--literal-pathspecs", "ls-tree", "-z", commit, "--", path)
    if not entry:
        return None
    metadata, _ = entry.split(b"\t", 1)
    mode, kind, oid = metadata.split()
    if kind != b"blob" or mode not in (b"100644", b"100755"):
        raise CommandError("stale_identity", "repository.blob", "Read the regular Task or scope artifact in Git.", 3)
    return _git_bytes(root, "cat-file", "blob", oid.decode("ascii"))


def _record(projection, commit, path):
    blob = _blob(projection.root, commit, path)
    if blob is None:
        return None
    try:
        data = json.loads(blob)
        return projection._call(projection.api.delivery_schema.parse_task_v2, data)
    except (ValueError, LifecycleContractError) as exc:
        raise CommandError("stale_identity", "repository.task_json",
                           "Read a valid public Task schema-2 record in the selected Git tree.", 3) from exc


def _delivery(record, key):
    return next(
        (row for row in record["deliveries"] if row["id"] == key["delivery_id"]
         and row["lifecycle_generation"] == key["lifecycle_generation"]),
        None,
    )


def _scope_path(authority, task_path, record):
    origin = record.get("artifact_origin")
    locator = authority["locator"]
    if origin is not None and locator.startswith(origin + "/"):
        return task_path + locator[len(origin):]
    return locator


def _scope_matches(projection, commit, task_path, current_scope, record):
    path = _scope_path(current_scope, task_path, record)
    blob = _blob(projection.root, commit, path)
    return blob is not None and "sha256:" + hashlib.sha256(blob).hexdigest() == current_scope["revision"]


def _attribution(projection, public, current, selected, facts, base, paths):
    key = public["delivery_key"]
    scope = current["accepted_scope"]
    if (scope is None or selected["scope_ref"]["authority"] != scope
            or not re.fullmatch(r"sha256:[0-9a-f]{64}", scope["revision"])
            or "://" in scope["locator"]):
        return "merged_pr_scope_mismatch", "The selected Delivery needs the current accepted scope and its committed SHA-256 artifact."
    store = projection.api.delivery_store
    context = projection._call(store.artifact_context, projection.task_dir, projection.root, current)
    try:
        projection._call(store.verify_authority, projection.root, scope, context)
    except LifecycleContractError:
        return "merged_pr_scope_mismatch", "The current accepted scope artifact is missing or differs from its recorded revision."

    task_paths = {public["task_ref"], current.get("artifact_origin", public["task_ref"])}
    head_records = {}
    for path in task_paths:
        snapshot = _record(projection, facts["head_sha"], f"{path}/task.json")
        if snapshot is not None and snapshot["id"] == key["task_id"]:
            head_records[path] = snapshot
    if not head_records:
        return "merged_pr_attribution_missing", "The PR head does not contain the original Task record."
    if len(head_records) != 1:
        return "merged_pr_attribution_ambiguous", "The PR head contains multiple records for the original Task."
    task_path, head_record = next(iter(head_records.items()))
    path = f"{task_path}/task.json"
    merge_record = _record(projection, facts["merge_sha"], path)
    if merge_record is None:
        return "merged_pr_attribution_missing", "The merge tree does not contain the original Task record."

    head_delivery = None
    for commit, label, snapshot in ((facts["head_sha"], "PR head", head_record),
                                    (facts["merge_sha"], "merge tree", merge_record)):
        if any(snapshot[field] != current[field] for field in ("id", "lifecycle_generation", "source", "base_branch")):
            return "merged_pr_attribution_mismatch", f"The {label} Task identity, generation, source or target differs."
        row = _delivery(snapshot, key)
        if row is None:
            return "merged_pr_attribution_missing", f"The {label} does not contain the selected Delivery."
        if any(row[field] != selected[field] for field in ("profile", "planning_root")):
            return "merged_pr_attribution_mismatch", f"The {label} Delivery profile or planning root differs."
        if (snapshot["accepted_scope"] != scope or row["scope_ref"] != selected["scope_ref"]
                or not _scope_matches(projection, commit, task_path, scope, snapshot)):
            return "merged_pr_scope_mismatch", f"The {label} accepted scope, Delivery scope or scope bytes differ."
        if label == "PR head":
            head_delivery = row

    previous = _record(projection, base, path)
    prior_delivery = _delivery(previous, key) if previous is not None else None
    if prior_delivery is None or any(prior_delivery[field] != head_delivery[field] for field in
                                     ("profile", "planning_root", "scope_ref", "plan_ref")):
        return None
    plan = f"{task_path}/{selected['planning_root']}"
    plan_files = {f"{plan}/{name}" for name in ("prd.md", "design.md", "implement.md", "implement.jsonl", "check.jsonl")}
    if set(paths).intersection(plan_files | {_scope_path(scope, task_path, head_record)}):
        return None
    return "merged_pr_attribution_missing", "The PR inherits the selected Delivery from its merge base and adds no matching planning evidence."


def invoke(root, package, public, review):
    validate_json(public, package / "schemas/public-delivery-adopt-merged-pr-input-1.0.schema.json", "input")
    validate_json(review, package / "schemas/adopt-merged-pr-review-1.0.schema.json", "review_input")
    try:
        key = public["delivery_key"]
        projection = DeliveryProjection(root, public["task_ref"])
        current = projection.read_record()
        selected = _delivery(current, key)
        if (current["id"] != key["task_id"] or current["lifecycle_generation"] != key["lifecycle_generation"]
                or selected is None or selected["profile"] != "pull_request"):
            return blocked(package, public, "merged_pr_attribution_mismatch",
                           "Select the existing pull-request Delivery in this Task's current generation.")
        if selected["phase"] == "stopped":
            return blocked(package, public, "merged_pr_delivery_stopped", "The selected Delivery already has a stop result.")
        if selected["publication_result"] is not None:
            return blocked(package, public, "merged_pr_publication_exists",
                           "Use delivery_merged_recovery for the selected Delivery's existing Publication.")
        if selected["delivery_result"] is None:
            if projection.task_dir.resolve().is_relative_to((root / ".trellis/tasks/archive").resolve()):
                return blocked(package, public, "merged_pr_archive_fact_missing",
                               "Resolve the missing archive fact with the original archive maintenance owner.")
            if projection.has_context():
                projection.selection_preflight(key)
            projection._require_explicit_task(key)

        for other in current["deliveries"]:
            if other["id"] == selected["id"]:
                continue
            for relation in (other["publication_result"], other["delivery_result"]):
                if (relation and relation["profile"] == "pull_request"
                        and relation["repo_ref"].casefold() == public["repo_ref"].casefold()
                        and relation["pr_number"] == public["pr_number"]):
                    return blocked(package, public, "merged_pr_attribution_ambiguous",
                                   "This Task already associates the selected PR with a different Delivery.")

        facts, reason = merged_pr_facts(root, public, current["base_branch"])
        if reason:
            return blocked(package, public, reason,
                           "Read the selected same-repository two-parent merge on the original target branch.")
        pr_head = facts["head_sha"]
        result = subprocess.run(["git", "merge-base", "--all", facts["first_parent"], pr_head],
                                cwd=root, capture_output=True, text=True)
        bases = result.stdout.splitlines()
        if result.returncode or len(bases) != 1:
            return blocked(package, public, "merged_pr_base_ambiguous",
                           "Read the unique Git merge base of the actual first parent and PR head.")
        base = bases[0]
        names = _git_bytes(root, "diff", "--name-only", "-z", "--no-renames", "--ignore-submodules=none",
                           base, pr_head, "--").decode("utf-8").split("\0")
        paths = [path for path in names if path]
        gap = _attribution(projection, public, current, selected, facts, base, paths)
        if gap:
            return blocked(package, public, *gap)
        if (review["reviewed_delivery_key"] != key or review["reviewed_scope_ref"] != selected["scope_ref"]
                or review["reviewed_pr"] != reviewed_pr(facts) or review["observed_checks"] != facts["checks"]):
            raise CommandError("stale_identity", "review_input",
                               "Reread the Delivery scope, both Git ranges and the PR head checks before review.", 3)
        gate = review["ai_review_gate"]
        if gate["status"] == "blocked":
            return blocked(package, public, "merged_pr_review_blocked", gate["summary"])
        candidate_paths = sorted(path for path in paths if not reviewed_content_metadata_path(path))
        if not candidate_paths:
            return blocked(package, public, "merged_pr_candidate_missing",
                           "The selected PR has no paths for the public Git Candidate.")
        candidate = immutable_candidate(projection, {"base_ref": base, "paths": candidate_paths}, pr_head)
        return record_terminal_delivery(package, public, projection, selected, facts, candidate)
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
