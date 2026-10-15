"""Exact historical schema-1 merge recovery by its original semantic owner."""
import argparse
import json
from pathlib import Path

from owner import (gate_path, load_json, live_facts, repo_root, validate_gate,
                   validate_public, terminal_output)
from runtime.io import CommandError
from runtime.schema import validate_json


def association_path(root, public):
    return gate_path(root, public).with_suffix(".migration.json")


def validate_source_binding(original, current):
    legacy = original["public_input"]
    task = original["pre_merge_facts"]["task"]
    key = current["delivery_key"]
    if task["stable_task_id"] != key["task_id"] or task["lifecycle_generation"] != key["lifecycle_generation"]:
        raise CommandError("stale_identity", "legacy_gate.task", "Recover the original stable Task identity and generation.", 3)
    # task_ref is a locator which can normally move into archive; ownership is
    # the original gate's immutable Task identity, not its old directory name.
    for field in ("repo_ref", "pr_number", "expected_head_sha", "publication_body_sha256"):
        if legacy[field] != current[field]:
            raise CommandError("stale_identity", "legacy_gate", "Recover exactly the original Task/PR/HEAD/body.", 3)


def recover(package, root, public):
    path = association_path(root, public)
    if not path.is_file():
        return None
    association = load_json(root, package, str(path), "migration_binding")
    validate_json(association, package / "schemas/private-delivery-migration-binding-1.0.schema.json", "migration_binding")
    if association["delivery_key"] != public["delivery_key"] or association["publication_result_id"] != public["publication_result_id"]:
        raise CommandError("stale_identity", "migration_binding", "Recover the original historical merge association.", 3)
    original = load_json(root, package, association["legacy_gate"], "legacy_gate")
    validate_gate(package, original)
    validate_source_binding(original, public)
    facts = live_facts(root, package, public, historical_only=True)
    if facts["pr"]["state"] != "MERGED":
        raise CommandError("stale_identity", "github.pr.state", "Historical recovery cannot authorize a new merge; review the current candidate.", 3)
    return terminal_output(package, root, public, facts, original["semantic_review"], historical_schema1=True)


def run(package, command, argv):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args(argv)
    root = repo_root(args.root)
    public = load_json(root, package, args.input, "input")
    review = load_json(root, package, args.owner_result, "owner_result")
    validate_json(public, package / "schemas/private-delivery-migration-input-1.0.schema.json", "input")
    validate_json(review, package / "schemas/private-delivery-migration-review-1.0.schema.json", "owner_result")
    if review["status"] != "passed":
        raise CommandError("stale_identity", "owner_result", "The original Merge owner must review actual cycle attribution and terminal facts.", 3)
    current = public["current_input"]
    validate_public(package, current)
    original = load_json(root, package, public["legacy_gate"], "legacy_gate")
    validate_gate(package, original)
    selected_path = Path(public["legacy_gate"])
    if not selected_path.is_absolute():
        selected_path = root / selected_path
    if selected_path.resolve() != gate_path(root, original["public_input"]).resolve():
        raise CommandError("stale_identity", "legacy_gate", "Use the original owner-private gate locator.", 3)
    if ("delivery_key" in original["public_input"] or original["public_input"]["delivery_cycle_ref"] != public["delivery_cycle_ref"]
            or original["semantic_review"]["route"]["typed_exit"] != "delivered"):
        raise CommandError("stale_identity", "legacy_gate", "Use the exact original schema-1 merge recovery source.", 3)
    validate_source_binding(original, current)
    association = {"schema_version": "1.0", "delivery_key": current["delivery_key"], "publication_result_id": current["publication_result_id"], "legacy_gate": public["legacy_gate"]}
    path = association_path(root, current)
    if path.is_file() and load_json(root, package, str(path), "migration_binding") != association:
        raise CommandError("stale_identity", "migration_binding", "Resume the same original historical recovery.", 3)
    # Validate actual terminal facts before persisting the minimum association.
    facts = live_facts(root, package, current, historical_only=True)
    if facts["pr"]["state"] != "MERGED":
        return {"status": "fresh_merge_review_required", "delivery_key": current["delivery_key"]}
    if args.preview:
        from owner import delivery_fact
        from runtime.delivery_projection.adapter import DeliveryProjection
        terminal_output(package, root, current, facts, original["semantic_review"], historical_schema1=True, record=False)
        projection = DeliveryProjection(root, current["task_ref"])
        writes = [path.relative_to(root).as_posix()]
        if projection.resolve(current["delivery_key"])["delivery_result"] != delivery_fact(projection, current, facts):
            writes.append(current["task_ref"] + "/task.json")
        return {"status": "preview", "write_paths": writes}
    terminal_output(package, root, current, facts, original["semantic_review"], historical_schema1=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(association, ensure_ascii=False, indent=2) + "\n")
    return {"status": "historical_delivery_recorded", "delivery_key": current["delivery_key"], "result_id": "delivery:" + facts["merge_commit"]["sha"], "source_binding": path.relative_to(root).as_posix()}
