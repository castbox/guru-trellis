from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json

EXITS = {"remaining_work","evidence_pending","additional_delivery_required","requirements_revision_required","implementation_revision_required","completed","blocked"}

def _json(root: Path, package: Path, value: str, field: str) -> dict:
    path = Path(value)
    candidates = [path] if path.is_absolute() else [root / path, package / path]
    if not candidates[0].is_file() and len(candidates) > 1 and not candidates[1].is_file():
        raise CommandError("invalid_json", field, "Provide one existing JSON object.")
    try: data = json.loads(next(p for p in candidates if p.is_file() and not p.is_symlink()).read_text())
    except (OSError, StopIteration, json.JSONDecodeError) as exc: raise CommandError("invalid_json", field, "Provide one valid JSON object.") from exc
    if not isinstance(data, dict): raise CommandError("invalid_json", field, "Provide one JSON object.")
    return data

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--input", required=True); parser.add_argument("--semantic-result", required=True)
    try: args = parser.parse_args(argv)
    except SystemExit as exc: raise CommandError("invalid_arguments", "arguments", "Use the declared completion command.") from exc
    root = Path(args.root or ".").resolve(); public = _json(root, package_root, args.input, "input"); semantic = _json(root, package_root, args.semantic_result, "semantic_result")
    validate_json(public, package_root / "schemas/public-input.schema.json", "input")
    validate_json(semantic, package_root / "schemas/semantic-result.schema.json", "semantic_result")
    if public["profile"] != semantic["profile"] or public["mode"] != semantic["mode"]: raise CommandError("stale_identity", "semantic_result", "Input and semantic result identity differ.", 3)
    exit_id = semantic["route"]["typed_exit"]
    if exit_id not in EXITS: raise CommandError("schema_mismatch", "semantic_result.route", "Unknown completion exit.")
    declared={str(item["delivery_cycle_ref"]) for item in public["delivery_facts"]}
    reviewed=set(str(item) for item in semantic["delivery_refs"])
    declared_authority=set(str(item) for item in public["authority_refs"])
    reviewed_authority=set(str(item) for item in semantic["authority_refs"])
    declared_evidence=set(str(item) for item in public["evidence_refs"])
    reviewed_evidence=set(str(item) for item in semantic["evidence_refs"])
    if exit_id == "completed":
        bindings = (
            (declared, reviewed, "delivery_refs", "Completion requires a non-empty, exact review of every current Delivery fact."),
            (declared_authority, reviewed_authority, "authority_refs", "Completion requires a non-empty, exact review of current authority."),
            (declared_evidence, reviewed_evidence, "evidence_refs", "Completion requires a non-empty, exact review of current evidence."),
        )
        for declared_refs, reviewed_refs, field, remediation in bindings:
            if not declared_refs or declared_refs != reviewed_refs:
                raise CommandError("stale_identity", field, remediation, 3)
    output = {"exit_id": exit_id}
    if exit_id == "completed":
        identity=hashlib.sha256(json.dumps({"input":public,"semantic_result":semantic},sort_keys=True,separators=(",",":")).encode()).hexdigest()[:24]
        output.update({"task_ref":public["task_ref"], "completion_ref":"completion:v1:" + identity})
    elif exit_id != "blocked":
        output.update({"task_ref":public["task_ref"], "resume_target":{"remaining_work":"active-task","evidence_pending":"evidence-refresh","additional_delivery_required":"delivery-planning","requirements_revision_required":"requirements","implementation_revision_required":"phase-2"}[exit_id]})
    validate_json(output, package_root / "schemas/public-output.schema.json", "stdout")
    return output

if __name__ == "__main__":
    try: print(json.dumps(run(Path(__file__).parents[1], {}, sys.argv[1:]), ensure_ascii=False))
    except CommandError as exc: print(json.dumps({"code":exc.code,"field_path":exc.field_path,"remediation":exc.remediation}, ensure_ascii=False), file=sys.stderr); raise SystemExit(exc.exit_status)
