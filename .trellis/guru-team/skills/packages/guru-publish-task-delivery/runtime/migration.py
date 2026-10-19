"""Original publication owner's one-window private transaction conversion."""
import argparse
import copy
from pathlib import Path

from owner import (WorkflowError, load_transaction, read_json, repo_root,
                   save_transaction, validate_transaction, ready_output,
                   validate_public_input, transaction_path, digest, read_pr, find_bindable_pr)
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.schema import validate_json
from runtime.io import CommandError
from runtime.task_lifecycle import LifecycleContractError


def _run(package, command, argv):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args(argv)
    root = repo_root(Path(args.root or "."))
    public, review = read_json(args.input), read_json(args.owner_result)
    if public.get("profile") == "publication_transaction_636":
        validate_json(public, package / "schemas/private-publication-transaction-636-input.schema.json", "input")
    else:
        validate_json(public, package / "schemas/private-delivery-migration-input-1.0.schema.json", "input")
    validate_json(review, package / "schemas/private-delivery-migration-review-1.0.schema.json", "owner_result")
    if review["status"] != "passed":
        raise WorkflowError("Original Publish owner must review actual same-cycle attribution and recovery obligations.", code="private_state_invalid")
    transaction = load_transaction(root, public["transaction_ref"])
    if transaction is None:
        raise WorkflowError("Recover the exact original publication transaction.", code="private_state_missing")
    if transaction.get("schema_version") == "1.0":
        validate_json(transaction, package / "schemas/publication-transaction.schema.json", "transaction")
        if transaction.get("transaction_sha256") != digest({k:v for k,v in transaction.items() if k != "transaction_sha256"}):
            raise WorkflowError("The original transaction digest is stale.", code="private_state_invalid")
    else:
        validate_transaction(transaction)
    if public.get("profile") == "publication_transaction_636":
        return migrate_636(root, transaction, public, args.preview)
    source = transaction["input"]
    projection = DeliveryProjection(root, source["task_ref"])
    projection.resolve(public["delivery_key"])
    if "delivery_key" in source:
        if source["delivery_key"] != public["delivery_key"]:
            raise WorkflowError("The transaction was bound to another Delivery.", code="private_state_invalid")
        return ({"status": "preview", "write_paths": []} if args.preview
                else {"status": "already_bound", "transaction_ref": transaction["transaction_ref"]})
    if source["delivery_cycle_ref"] != public["delivery_cycle_ref"]:
        raise WorkflowError("Use the actual original cycle selected by the history owner.", code="private_state_invalid")
    migrated = copy.deepcopy(transaction)
    if public["profile"] == "historical_publication_migration":
        if transaction["stage"] != "ready":
            raise WorkflowError("Only actual terminal Ready transactions use historical conversion.", code="private_state_invalid")
        # Original producer rereads exact PR bytes/HEAD/Draft state first.
        # No current readiness is inferred from those historical facts.
        ready_output(root, transaction)
        candidate = public["candidate"]
        projection._call(projection.api.delivery_schema.candidate, candidate)
        if candidate["head_ref"] != transaction["reviewed_head"]:
            raise WorkflowError("Bind the actual original published candidate.", code="private_state_invalid")
        new_source = {**source, "profile": "delivery_review_ready", "delivery_key": public["delivery_key"], "readiness_result_id": None}
        new_source.pop("delivery_cycle_ref")
    else:
        new_source = validate_public_input(public["current_input"])
        if new_source["delivery_key"] != public["delivery_key"] or any(new_source[field] != source[field] for field in ("task_ref", "mode", "reviewed_head", "pr_title", "pr_body", "remaining_work_state")):
            raise WorkflowError("Fresh readiness must cover the unchanged original publication action.", code="private_state_invalid")
        delivery = projection.resolve(public["delivery_key"])
        readiness = delivery["results"]["readiness"]
        if (readiness is None or readiness["result_id"] != new_source["readiness_result_id"]
                or projection.gate_applicability(public["delivery_key"])["readiness"]["kind"] != "applicable"):
            raise WorkflowError("Fresh current Readiness is required before continuing an incomplete transaction.", code="publication_stale")
        candidate = delivery["candidate"]
    migrated.update(schema_version="2.0", action="ready", terminal="ready")
    migrated["input"] = new_source
    migrated["public_candidate"] = candidate
    if args.preview:
        return {"status": "preview", "write_paths": [transaction_path(root, transaction["transaction_ref"]).relative_to(root).as_posix()]}
    save_transaction(root, migrated)
    # Keep the old transaction ref/retry stage and all actual decisions. No
    # push/PR/Ready mutation or public gate occurs in this private command.
    return {"status": "transaction_bound", "transaction_ref": transaction["transaction_ref"]}


def migrate_636(root, transaction, public, preview):
    """One-time current 1.0 -> 2.0 conversion; no remote mutation or gate."""
    source = transaction["input"]
    if source.get("task_ref") != public["task_ref"] or source.get("delivery_key") != public["delivery_key"]:
        raise WorkflowError("Select the exact original current Delivery transaction.", code="private_state_invalid")
    if transaction["schema_version"] == "2.0":
        return {"status":"already_bound", "transaction_ref":transaction["transaction_ref"]}
    projection = DeliveryProjection(root, source["task_ref"])
    selected = projection.resolve(source["delivery_key"])
    pr = (read_pr(root, transaction["bound_pr"]["number"]) if transaction.get("bound_pr")
          else find_bindable_pr(root, transaction))
    if pr is not None:
        heads = {transaction["reviewed_head"], transaction.get("initial_remote_head")}
        original = transaction.get("candidate_pr")
        if original:heads.add(original["head_sha"])
        if pr["head_sha"] not in heads:
            raise WorkflowError("The actual PR HEAD is outside this operation's preimage/postimage.", code="publication_stale")
    if transaction["stage"] == "ready":
        if (pr is None or pr["state"] not in {"OPEN", "MERGED"} or pr["is_draft"]
                or pr["head_sha"] != transaction["reviewed_head"]
                or pr["title"] != source["pr_title"] or pr["body"] != source["pr_body"]):
            raise WorkflowError("Recover the actual original Ready result before conversion.", code="publication_stale")
    else:
        readiness = selected["results"]["readiness"]
        if (selected["phase"] != "publishing" or readiness is None
                or readiness["result_id"] != source["readiness_result_id"]
                or projection.gate_applicability(source["delivery_key"])["readiness"]["kind"] != "applicable"
                or selected["candidate"]["head_ref"] != transaction["reviewed_head"]):
            raise WorkflowError("Recover applicable original readiness before converting a pending Ready action.", code="publication_stale")
    migrated = copy.deepcopy(transaction)
    migrated.update(schema_version="2.0", action="ready", terminal="ready")
    path = transaction_path(root, transaction["transaction_ref"]).relative_to(root).as_posix()
    if preview:return {"status":"preview", "write_paths":[path]}
    save_transaction(root, migrated)
    return {"status":"transaction_bound", "transaction_ref":migrated["transaction_ref"]}


def run(package, command, argv):
    try:
        return _run(package, command, argv)
    except WorkflowError as exc:
        code = exc.code if exc.code in {"invalid_json", "schema_mismatch", "external_command_failed"} else "publication_stale"
        raise CommandError(code, "migration", str(exc), 3) from exc
    except LifecycleContractError as exc:
        raise CommandError("publication_stale", exc.field_path, exc.remediation, 3) from exc
