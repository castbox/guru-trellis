from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle.git_facts import inspect_repository


def _load(root: Path, package: Path, name: str, field: str) -> dict:
    path = Path(name)
    candidates = [path] if path.is_absolute() else [root / path, package / path]
    source = next((item for item in candidates if item.is_file() and not item.is_symlink()), None)
    if source is None:
        raise CommandError("invalid_json", field, "Provide one regular JSON object.")
    try:
        value = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("invalid_json", field, "Provide valid JSON.") from exc
    if not isinstance(value, dict):
        raise CommandError("invalid_json", field, "Provide one JSON object.")
    return value


def _digest(value: dict) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:24]


def _transaction_ref(key: dict, transaction_id: str) -> dict:
    return {**key, "transaction_id": transaction_id, "result_id": transaction_id}


def _conflict(ref: dict, code: str, evidence: str) -> dict:
    return {"exit_id": "external_change_conflict", "transaction_ref": ref,
            "reason": {"reason_code": code, "reason_refs": [evidence]}}


def _state(root: Path, issue: dict) -> str | None:
    try:
        observed = subprocess.run(
            ["gh", "issue", "view", str(issue["issue_number"]), "--repo", issue["repo_ref"],
             "--json", "state", "--jq", ".state"],
            cwd=root, text=True, capture_output=True,
        )
    except OSError:
        return None
    if observed.returncode:
        return None
    state = observed.stdout.strip().upper()
    return state if state in {"OPEN", "CLOSED"} else None


def _store(path: Path, transaction: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(transaction, sort_keys=True), encoding="utf-8")


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    parser.add_argument("--confirmed-close", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the declared closure command.") from exc
    root = Path(args.root or ".").resolve()
    public = _load(root, package_root, args.input, "input")
    semantic = _load(root, package_root, args.semantic_result, "semantic_result")
    validate_json(public, package_root / "schemas/public-input.schema.json", "input")
    validate_json(semantic, package_root / "schemas/semantic-result.schema.json", "semantic_result")
    if (public["profile"], public["mode"]) != (semantic["profile"], semantic["mode"]):
        raise CommandError("stale_identity", "semantic_result", "Closure profile or mode changed.", 3)

    completion = public["completion_result"]
    key = {name: completion[name] for name in ("task_id", "lifecycle_generation")}
    binding = public["binding_ref"]
    if (binding["task_id"], binding["lifecycle_generation"]) != (key["task_id"], key["lifecycle_generation"]):
        raise CommandError("stale_identity", "task_lifecycle", "Completion and binding must belong to this lifecycle.", 3)
    if public["evidence_slots"].get("completion") != completion["result_id"]:
        raise CommandError("stale_identity", "evidence_slots.completion", "Use the current Completion result.", 3)
    source = public["source"]
    actions = public["action_set"]
    if source["kind"] == "no_issue" and actions:
        raise CommandError("stale_identity", "action_set", "No-Issue source has no Issue action.", 3)
    if source["kind"] == "issue" and not any(
        row["issue_ref"] == {"repo_ref": source["repo_ref"], "issue_number": source["number"]} for row in actions
    ):
        raise CommandError("stale_identity", "action_set", "Include the exact source relation in the reviewed action set.", 3)
    identities = [(row["issue_ref"]["repo_ref"], row["issue_ref"]["issue_number"]) for row in actions]
    if len(identities) != len(set(identities)):
        raise CommandError("stale_identity", "action_set", "Review each Issue once in the frozen action set.", 3)
    if semantic["route"]["typed_exit"] == "blocked":
        output = {"exit_id": "blocked", "reason": semantic["route"]["reason"]}
        validate_json(output, package_root / "schemas/public-output.schema.json", "stdout")
        return output
    if semantic["reviewed_action_set"] != actions:
        raise CommandError("stale_identity", "semantic_result.reviewed_action_set", "Review the complete current action set.", 3)

    frozen = {name: public[name] for name in (
        "completion_result", "source", "accepted_scope_identity",
        "delivery_target", "binding_ref", "content_head", "evidence_slots", "action_set",
    )}
    ref = _transaction_ref(key, "closure:" + _digest(frozen))
    path = inspect_repository(root).common_dir / "guru-team/closure" / key["task_id"] / f'{key["lifecycle_generation"]}.json'
    transaction = _load(root, package_root, str(path), "transaction") if path.is_file() else None
    supplied = public.get("transaction_ref")
    if public["source_exit"] == "external_change_conflict" and transaction is not None:
        if supplied != transaction["ref"]:
            raise CommandError("stale_identity", "transaction_ref", "Re-enter the exact conflicting Closure transaction.", 3)
        previous = transaction["ref"]
        ref = _transaction_ref(key, "closure:" + _digest({"frozen": frozen, "predecessor": previous}))
        transaction = {"frozen": frozen, "ref": ref, "verified": []}
        _store(path, transaction)
    elif public["source_exit"] == "resume_closure" and transaction is not None and supplied == transaction.get("ref"):
        ref = transaction["ref"]
    if transaction is not None and (transaction.get("frozen") != frozen or transaction.get("ref") != ref):
        output = _conflict(transaction["ref"], "frozen_closure_changed", "closure:action_set")
    elif supplied is not None and supplied != ref and public["source_exit"] != "external_change_conflict":
        raise CommandError("stale_identity", "transaction_ref", "Resume the exact Closure transaction.", 3)
    elif (any(row["disposition"] == "close" for row in actions)
          and not args.confirmed_close and not (transaction and transaction.get("terminal"))):
        output = {"exit_id": "resume_closure", "transaction_ref": ref}
    else:
        if transaction is None:
            transaction = {"frozen": frozen, "ref": ref, "verified": []}
            _store(path, transaction)
        output = None
        for row in actions:
            issue = row["issue_ref"]
            if row["disposition"] == "no_close_authority":
                continue
            issue_key = f'{issue["repo_ref"]}#{issue["issue_number"]}'
            state = _state(root, issue)
            if state is None:
                output = {"exit_id": "resume_closure", "transaction_ref": ref}
                break
            if issue_key in transaction["verified"] and state != "CLOSED":
                output = _conflict(ref, "required_closed_issue_reopened", issue_key)
                break
            if row["disposition"] == "already_closed_at_review" and state != "CLOSED":
                output = _conflict(ref, "required_closed_issue_reopened", issue_key)
                break
            if row["disposition"] == "close" and state == "OPEN":
                if transaction.get("terminal"):
                    output = _conflict(ref, "required_closed_issue_reopened", issue_key)
                    break
                try:
                    result = subprocess.run(
                        ["gh", "issue", "close", str(issue["issue_number"]), "--repo", issue["repo_ref"], "--reason", "completed"],
                        cwd=root, text=True, capture_output=True,
                    )
                    complete = result.returncode == 0 and _state(root, issue) == "CLOSED"
                except OSError:
                    complete = False
                if not complete:
                    output = {"exit_id": "resume_closure", "transaction_ref": ref}
                    break
            if issue_key not in transaction["verified"]:
                transaction["verified"].append(issue_key)
                _store(path, transaction)
        if output is None:
            terminal = "closed" if any(row["disposition"] != "no_close_authority" for row in actions) else "no_mutation"
            transaction["terminal"] = terminal
            _store(path, transaction)
            output = {"exit_id": terminal, "result_ref": {
                **key, "result_id": ref["result_id"],
            }}
    validate_json(output, package_root / "schemas/public-output.schema.json", "stdout")
    return output


if __name__ == "__main__":
    try:
        print(json.dumps(run(Path(__file__).parents[1], {}, sys.argv[1:]), ensure_ascii=False))
    except CommandError as exc:
        print(json.dumps({"code": exc.code, "field_path": exc.field_path, "remediation": exc.remediation}), file=sys.stderr)
        raise SystemExit(exc.exit_status)
