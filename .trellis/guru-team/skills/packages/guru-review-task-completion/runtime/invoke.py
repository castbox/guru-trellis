from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json


DELIVERY_SLOTS = {"planning", "delivery_review", "delivery_publication"}
REACTIVATION_SLOTS = {"reactivation", "validation"}
NON_COMPLETE = {
    "remaining_work", "evidence_pending", "additional_delivery_required",
    "requirements_revision_required", "implementation_revision_required",
}


def _load(root: Path, package: Path, name: str, field: str) -> dict:
    path = Path(name)
    candidates = [path] if path.is_absolute() else [root / path, package / path]
    source = next((item for item in candidates if item.is_file() and not item.is_symlink()), None)
    if source is None:
        raise CommandError("invalid_json", field, "Provide one existing regular JSON object.")
    try:
        value = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("invalid_json", field, "Provide one valid JSON object.") from exc
    if not isinstance(value, dict):
        raise CommandError("invalid_json", field, "Provide one JSON object.")
    return value


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the declared completion command.") from exc
    root = Path(args.root or ".").resolve()
    public = _load(root, package_root, args.input, "input")
    semantic = _load(root, package_root, args.semantic_result, "semantic_result")
    validate_json(public, package_root / "schemas/public-input.schema.json", "input")
    validate_json(semantic, package_root / "schemas/semantic-result.schema.json", "semantic_result")
    if (public["profile"], public["mode"]) != (semantic["profile"], semantic["mode"]):
        raise CommandError("stale_identity", "semantic_result", "Completion profile or mode changed.", 3)

    artifact = public["task_artifact"]
    slots = public["evidence_slots"]
    if "merge_result" in public:
        merge = public["merge_result"]
        if (artifact["task_id"], artifact["lifecycle_generation"]) != (merge["task_id"], merge["lifecycle_generation"]):
            raise CommandError("stale_identity", "merge_result", "Merge result belongs to another lifecycle.", 3)
        if merge["task_ref"] != artifact["task_ref"]:
            raise CommandError("stale_identity", "merge_result.task_ref", "Merge task locator differs.", 3)
        if set(slots) != DELIVERY_SLOTS:
            raise CommandError("stale_identity", "evidence_slots", "Use exactly the current Delivery evidence slots.", 3)
        reviewed_basis = (semantic.get("reviewed_merge_result_id") == merge["result_id"]
                          and "reviewed_reactivation_anchor" not in semantic)
    else:
        anchor = public["reactivation_anchor"]
        if (artifact["task_id"] != anchor["task_id"]
                or artifact["lifecycle_generation"] != anchor["archived_generation"] + 1
                or artifact["task_ref"].startswith(".trellis/tasks/archive/")):
            raise CommandError("stale_identity", "reactivation_anchor", "Review the preceding archived generation and current active task.", 3)
        if set(slots) != REACTIVATION_SLOTS:
            raise CommandError("stale_identity", "evidence_slots", "Use current reactivation and validation evidence.", 3)
        reviewed_basis = (semantic.get("reviewed_reactivation_anchor") == anchor
                          and "reviewed_merge_result_id" not in semantic)
    if (semantic["reviewed_scope_identity"] != public["accepted_scope_identity"]
            or not reviewed_basis
            or semantic["reviewed_evidence_slots"] != slots):
        raise CommandError("stale_identity", "semantic_result", "Review the exact scope, completion basis and selected evidence slots.", 3)

    exit_id = semantic["route"]["typed_exit"]
    if exit_id == "completed":
        if semantic["remaining_work_refs"]:
            raise CommandError("stale_identity", "remaining_work_refs", "Accepted work remains.", 3)
        digest = hashlib.sha256(json.dumps({"input": public, "semantic": semantic}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:24]
        output = {"exit_id": exit_id, "result_ref": {
            "task_id": artifact["task_id"], "lifecycle_generation": artifact["lifecycle_generation"],
            "result_id": "completion:" + digest,
        }}
    elif exit_id == "blocked":
        output = {"exit_id": exit_id, "reason": semantic["route"]["reason"]}
    elif exit_id in NON_COMPLETE:
        output = {"exit_id": exit_id, "task_artifact": artifact,
                  "reason": semantic["route"]["reason"]}
    else:
        raise CommandError("schema_mismatch", "semantic_result.route", "Unknown completion route.")
    validate_json(output, package_root / "schemas/public-output.schema.json", "stdout")
    return output


if __name__ == "__main__":
    try:
        print(json.dumps(run(Path(__file__).parents[1], {}, sys.argv[1:]), ensure_ascii=False))
    except CommandError as exc:
        print(json.dumps({"code": exc.code, "field_path": exc.field_path, "remediation": exc.remediation}), file=sys.stderr)
        raise SystemExit(exc.exit_status)
