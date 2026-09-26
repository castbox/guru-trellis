"""Shared deterministic task-worktree and agent-recovery helpers."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository, resolve_task_ref
from task_lifecycle.git_facts import find_registration, is_ancestor


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def _task(root: Path, value: str | None) -> tuple[str, object]:
    if not value:
        value = subprocess.run(
            [sys.executable, str(root / ".trellis/scripts/task.py"), "current"],
            cwd=root, capture_output=True, text=True, check=True,
        ).stdout.strip()
    path = Path(value)
    if path.is_absolute():
        path = path.resolve().relative_to(root)
    if len(path.parts) == 1:
        path = Path(".trellis/tasks") / path
    identity = resolve_task_ref(root, path.as_posix())
    if identity.lifecycle_state != "active":
        raise ValueError("workspace boundary requires an active task")
    return identity.task_ref, identity


def _boundary(root: Path, task_ref: str, identity: object) -> dict:
    repository = inspect_repository(root)
    registration = find_registration(repository, root)
    branch = _git(root, "symbolic-ref", "-q", "HEAD")
    binding = BranchBindingStore(repository).read(
        TaskLifecycleKey(identity.task_id, identity.lifecycle_generation)
    )
    if binding is None:
        raise ValueError("task branch binding required before checkout boundary validation")
    expected = binding.branch_ref
    if registration is None or branch != expected or registration.registered_branch_ref != expected:
        raise ValueError("workspace boundary does not match task branch and worktree registration")
    return {
        "status": "ok", "task_dir_relative": task_ref, "actual_repo_root": str(root),
        "expected_workspace": str(root), "task_worktree_status": _git(root, "status", "--porcelain").splitlines(),
        "source_checkout_status": [], "suspicious_source_artifacts": [], "errors": [],
    }


def _checkpoint(root: Path, task_ref: str) -> Path:
    key = hashlib.sha256(task_ref.encode()).hexdigest()[:16]
    return root / ".trellis/.runtime/guru-team/agent-recovery" / f"{key}.json"


def _digest(payload: dict) -> str:
    facts = {key: value for key, value in payload.items() if key not in {"updated_at", "facts_sha256"}}
    encoded = json.dumps(facts, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _check(root: Path, task_ref: str, payload: dict) -> dict:
    if set(payload) != {"schema_version", "task_ref", "events", "updated_at", "facts_sha256"}:
        raise ValueError("agent recovery checkpoint fields mismatch")
    if payload["schema_version"] != "1.0" or payload["task_ref"] != task_ref or payload["facts_sha256"] != _digest(payload):
        raise ValueError("agent recovery checkpoint identity or facts mismatch")
    datetime.fromisoformat(payload["updated_at"].replace("Z", "+00:00"))
    open_roles: dict[str, str] = {}
    replacements = 0
    for index, event in enumerate(payload["events"], start=1):
        if set(event) != {"event_id", "event", "logical_role", "agent_id", "reason", "handoff_summary", "observed_head", "recorded_at", "predecessor_event_id"}:
            raise ValueError("agent recovery event fields mismatch")
        role = event["logical_role"]
        if event["event_id"] != f"recovery-{index:03d}" or not all(event[key] for key in ("agent_id", "logical_role", "reason", "handoff_summary")):
            raise ValueError("agent recovery event identity mismatch")
        datetime.fromisoformat(event["recorded_at"].replace("Z", "+00:00"))
        if not is_ancestor(inspect_repository(root), event["observed_head"], _git(root, "rev-parse", "HEAD")):
            raise ValueError("agent recovery observed HEAD is not current history")
        if event["event"] == "unfinished" and event["predecessor_event_id"] is None and role not in open_roles:
            open_roles[role] = event["event_id"]
        elif event["event"] == "replacement" and open_roles.get(role) == event["predecessor_event_id"]:
            del open_roles[role]
            replacements += 1
        else:
            raise ValueError("agent recovery event does not follow its predecessor")
    if not payload["events"]:
        raise ValueError("agent recovery checkpoint has no events")
    return {"status": "ok", "task_ref": task_ref, "events_count": len(payload["events"]),
            "replacement_count": replacements, "open_unfinished": open_roles}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Guru Team task lifecycle helpers")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("check-task-checkout-boundary", "record-agent-recovery", "check-agent-recovery"):
        command = commands.add_parser(name)
        command.add_argument("--root")
        command.add_argument("--task")
        command.add_argument("--json", action="store_true")
        if name == "check-task-checkout-boundary":
            command.add_argument("--allow-source-clean", action="store_true")
        if name == "record-agent-recovery":
            command.add_argument("--event", required=True, choices=("unfinished", "replacement"))
            for field in ("logical-role", "agent-id", "reason", "handoff-summary"):
                command.add_argument(f"--{field}", required=True)
            command.add_argument("--predecessor-event-id")
            command.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = inspect_repository(Path(args.root or Path.cwd())).context_path
        task_ref, identity = _task(root, args.task)
        boundary = _boundary(root, task_ref, identity)
        if args.command == "check-task-checkout-boundary":
            result = boundary
        else:
            path = _checkpoint(root, task_ref)
            if args.command == "record-agent-recovery":
                payload = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {
                    "schema_version": "1.0", "task_ref": task_ref, "events": []}
                if payload["events"]:
                    _check(root, task_ref, payload)
                if args.event == "replacement" and not args.predecessor_event_id:
                    raise ValueError("replacement requires a predecessor event")
                if args.event == "unfinished" and args.predecessor_event_id:
                    raise ValueError("unfinished must not name a predecessor")
                now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                event = {"event_id": f"recovery-{len(payload['events']) + 1:03d}", "event": args.event,
                         "logical_role": args.logical_role, "agent_id": args.agent_id, "reason": args.reason,
                         "handoff_summary": args.handoff_summary, "observed_head": _git(root, "rev-parse", "HEAD"),
                         "recorded_at": now, "predecessor_event_id": args.predecessor_event_id}
                payload["events"].append(event)
                payload["updated_at"] = now
                payload["facts_sha256"] = _digest(payload)
                _check(root, task_ref, payload)
                if not args.dry_run:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                result = {"status": "recorded", "task_ref": task_ref, "event": event,
                          "checkpoint": path.relative_to(root).as_posix(), "dry_run": args.dry_run}
            else:
                result = _check(root, task_ref, json.loads(path.read_text(encoding="utf-8")))
                result["checkpoint"] = path.relative_to(root).as_posix()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "blocked", "errors": [str(exc)]}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
