from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import owner


AGENT_RECOVERY_RUNTIME_DIR = ".trellis/.runtime/guru-team/agent-recovery"


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--task")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guru Team Finalizer compatibility helpers")
    commands = parser.add_subparsers(dest="command", required=True)

    boundary = commands.add_parser("check-workspace-boundary")
    _add_common(boundary)
    boundary.add_argument("--allow-source-clean", action="store_true")

    recovery_record = commands.add_parser("record-agent-recovery")
    _add_common(recovery_record)
    recovery_record.add_argument("--event", required=True, choices=["unfinished", "replacement"])
    recovery_record.add_argument("--logical-role", required=True)
    recovery_record.add_argument("--agent-id", required=True)
    recovery_record.add_argument("--reason", required=True)
    recovery_record.add_argument("--handoff-summary", required=True)
    recovery_record.add_argument("--predecessor-event-id")
    recovery_record.add_argument("--dry-run", action="store_true")

    recovery_check = commands.add_parser("check-agent-recovery")
    _add_common(recovery_check)

    finish = commands.add_parser("finish-work")
    _add_common(finish)
    finish.add_argument("--task-name")
    finish.add_argument("--repo")
    finish.add_argument("--base-branch")
    finish.add_argument("--remote")
    finish.add_argument("--title")
    finish.add_argument("--validation", action="append")
    finish.add_argument("--expected-plan-digest")
    finish.add_argument("--dry-run", action="store_true")
    return parser


def _workspace_boundary(args: argparse.Namespace) -> dict[str, Any]:
    root = owner.repo_root(Path(args.root or Path.cwd()))
    config = owner.load_config(root)
    task_dir = owner.resolve_task_dir(root, args.task)
    try:
        task_context = owner.load_task_runtime_identity(task_dir, config)
    except owner.WorkflowError as exc:
        raise owner.WorkflowError(
            "Workspace boundary validation failed.",
            exit_code=2,
            payload={"status": "blocked", "task_dir": str(task_dir.resolve()), "errors": [str(exc)]},
        ) from exc
    return owner.assert_workspace_boundary(
        root,
        config,
        task_context,
        task_dir,
        allow_source_clean=bool(args.allow_source_clean),
    )


def _digest(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _recovery_path(root: Path, task_dir: Path) -> Path:
    task_ref = owner.repo_relative(root, task_dir)
    task_key = hashlib.sha256(task_ref.encode()).hexdigest()[:16]
    return root / AGENT_RECOVERY_RUNTIME_DIR / f"{task_key}.json"


def _recovery_facts(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(value) for key, value in payload.items() if key not in {"updated_at", "facts_sha256"}}


def _valid_timestamp(value: Any) -> bool:
    try:
        datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return False
    return True


def _recovery_errors(root: Path, task_dir: Path, payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return ["agent recovery checkpoint must be an object"]
    expected_keys = {"schema_version", "task_ref", "events", "updated_at", "facts_sha256"}
    errors: list[str] = []
    if set(payload) != expected_keys:
        errors.append("agent recovery checkpoint keys are invalid")
    if payload.get("schema_version") != "1.0":
        errors.append("agent recovery checkpoint schema_version must be 1.0")
    if payload.get("task_ref") != owner.repo_relative(root, task_dir):
        errors.append("agent recovery checkpoint task identity mismatch")
    if not _valid_timestamp(payload.get("updated_at")):
        errors.append("agent recovery checkpoint updated_at must be ISO-8601")
    events = payload.get("events")
    if not isinstance(events, list) or not events:
        errors.append("agent recovery checkpoint requires at least one recovery event")
        events = []
    event_by_id: dict[str, dict[str, Any]] = {}
    open_unfinished_by_role: dict[str, str] = {}
    required = {"event_id", "event", "logical_role", "agent_id", "reason", "handoff_summary", "observed_head", "recorded_at", "predecessor_event_id"}
    for index, event in enumerate(events, start=1):
        label = f"agent recovery event {index}"
        if not isinstance(event, dict) or set(event) != required:
            errors.append(f"{label} keys are invalid")
            continue
        event_id = str(event.get("event_id") or "")
        event_name = str(event.get("event") or "")
        role = str(event.get("logical_role") or "").strip()
        predecessor = event.get("predecessor_event_id")
        if event_id != f"recovery-{index:03d}" or event_id in event_by_id:
            errors.append(f"{label} event_id is not the next stable sequence")
        if event_name not in {"unfinished", "replacement"}:
            errors.append(f"{label} event must be unfinished or replacement")
        if not all(str(event.get(key) or "").strip() for key in ("logical_role", "agent_id", "reason", "handoff_summary")):
            errors.append(f"{label} requires role, agent, reason and handoff summary")
        observed_head = str(event.get("observed_head") or "")
        if not re.fullmatch(r"[0-9a-f]{40}", observed_head) or not owner.is_ancestor(root, observed_head, "HEAD"):
            errors.append(f"{label} observed_head is not current branch history")
        if not _valid_timestamp(event.get("recorded_at")):
            errors.append(f"{label} recorded_at must be ISO-8601")
        if event_name == "unfinished":
            if predecessor is not None:
                errors.append(f"{label} unfinished must not name a predecessor")
            if role in open_unfinished_by_role:
                errors.append(f"{label} duplicates an open unfinished role")
            open_unfinished_by_role[role] = event_id
        elif event_name == "replacement":
            predecessor_id = str(predecessor or "")
            prior = event_by_id.get(predecessor_id)
            if prior is None or prior.get("event") != "unfinished" or prior.get("logical_role") != role or open_unfinished_by_role.get(role) != predecessor_id:
                errors.append(f"{label} replacement must close the open unfinished role")
            else:
                open_unfinished_by_role.pop(role, None)
        event_by_id[event_id] = event
    if payload.get("facts_sha256") != _digest(_recovery_facts(payload)):
        errors.append("agent recovery checkpoint facts_sha256 mismatch")
    return sorted(set(errors))


def _record_recovery(args: argparse.Namespace) -> dict[str, Any]:
    root = owner.repo_root(Path(args.root or Path.cwd()))
    config = owner.load_config(root)
    task_dir = owner.resolve_task_dir(root, args.task)
    owner.assert_workspace_boundary(root, config, owner.load_task_runtime_identity(task_dir, config), task_dir)
    path = _recovery_path(root, task_dir)
    payload = owner.read_json(path) if path.is_file() and not path.is_symlink() else {"schema_version": "1.0", "task_ref": owner.repo_relative(root, task_dir), "events": [], "updated_at": owner.now_iso(), "facts_sha256": ""}
    existing_errors = _recovery_errors(root, task_dir, payload) if payload["events"] else []
    if existing_errors:
        raise owner.WorkflowError("Existing agent recovery checkpoint is invalid.", exit_code=2, payload={"errors": existing_errors})
    predecessor = str(args.predecessor_event_id or "").strip()
    if args.event == "unfinished" and predecessor:
        raise owner.WorkflowError("unfinished recovery event must not name a predecessor", exit_code=2)
    if args.event == "replacement" and not predecessor:
        raise owner.WorkflowError("replacement recovery event requires --predecessor-event-id", exit_code=2)
    recorded_at = owner.now_iso()
    event = {"event_id": f"recovery-{len(payload['events']) + 1:03d}", "event": args.event, "logical_role": args.logical_role.strip(), "agent_id": args.agent_id.strip(), "reason": args.reason.strip(), "handoff_summary": args.handoff_summary.strip(), "observed_head": owner.current_head(root), "recorded_at": recorded_at, "predecessor_event_id": predecessor or None}
    payload["events"].append(event)
    payload["updated_at"] = recorded_at
    payload["facts_sha256"] = _digest(_recovery_facts(payload))
    errors = _recovery_errors(root, task_dir, payload)
    if errors:
        raise owner.WorkflowError("Agent recovery event is invalid.", exit_code=2, payload={"errors": errors})
    if not args.dry_run:
        owner.write_json(path, payload)
    return {"status": "recorded", "task_ref": payload["task_ref"], "event": event, "checkpoint": owner.repo_relative(root, path), "dry_run": bool(args.dry_run)}


def _check_recovery(args: argparse.Namespace) -> dict[str, Any]:
    root = owner.repo_root(Path(args.root or Path.cwd()))
    config = owner.load_config(root)
    task_dir = owner.resolve_task_dir(root, args.task)
    owner.assert_workspace_boundary(root, config, owner.load_task_runtime_identity(task_dir, config), task_dir)
    path = _recovery_path(root, task_dir)
    if not path.is_file() or path.is_symlink():
        raise owner.WorkflowError("Agent recovery checkpoint is missing or unsafe.", exit_code=2)
    payload = owner.read_json(path)
    errors = _recovery_errors(root, task_dir, payload)
    if errors:
        raise owner.WorkflowError("Agent recovery checkpoint is invalid.", exit_code=2, payload={"errors": errors})
    open_unfinished: dict[str, str] = {}
    replacements = 0
    for event in payload["events"]:
        if event["event"] == "unfinished":
            open_unfinished[event["logical_role"]] = event["event_id"]
        else:
            open_unfinished.pop(event["logical_role"], None)
            replacements += 1
    return {"status": "ok", "task_ref": payload["task_ref"], "checkpoint": owner.repo_relative(root, path), "events_count": len(payload["events"]), "replacement_count": replacements, "open_unfinished": open_unfinished}


def _handler(command: str) -> Callable[[argparse.Namespace], dict[str, Any]]:
    handlers = {
        "check-workspace-boundary": _workspace_boundary,
        "record-agent-recovery": _record_recovery,
        "check-agent-recovery": _check_recovery,
        "finish-work": owner.cmd_finish_work,
    }
    return handlers[command]


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    try:
        payload = _handler(args.command)(args)
    except owner.WorkflowError as exc:
        payload = {"status": "error", "error": str(exc), **exc.payload}
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        return exc.exit_code
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
