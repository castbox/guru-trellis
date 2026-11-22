"""Public CLI for read-only continuation and exact Delivery facts."""
from __future__ import annotations

import argparse
from pathlib import Path
from uuid import UUID

from ..io import CommandError, fail, read_json, write_json
from ..task_lifecycle.errors import LifecycleContractError
from ..task_lifecycle.identity import normalize_generation, normalize_task_id, normalize_task_ref
from .continuation import VERSION, read_continuation, read_exact_delivery

_DEFAULT = {"schema_version": VERSION, "intent": "continue_session"}
_TASK_FIELDS = {"task_id", "lifecycle_generation", "task_ref"}
_DELIVERY_FIELDS = {"delivery_id", "phase", "planning_root"}


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CommandError("invalid_arguments", "arguments", message)


def _invalid(field: str, message: str) -> None:
    raise CommandError("invalid_arguments", field, message)


def _task(value: object) -> None:
    if not isinstance(value, dict) or set(value) != _TASK_FIELDS:
        _invalid("task", "Provide task_id, lifecycle_generation and the exact active task_ref.")
    assert isinstance(value, dict)
    if (normalize_task_id(value["task_id"]) != value["task_id"]
            or normalize_generation(value["lifecycle_generation"]) != value["lifecycle_generation"]
            or normalize_task_ref(value["task_ref"]) != value["task_ref"]
            or value["task_ref"].startswith(".trellis/tasks/archive/")):
        _invalid("task", "Use the normalized current Task identity and locator.")


def _delivery(value: object) -> None:
    try:
        valid = isinstance(value, str) and str(UUID(value)) == value
    except ValueError:
        valid = False
    if not valid:
        _invalid("delivery_id", "Use the exact canonical Delivery UUID.")


def _previous(value: object) -> None:
    if (not isinstance(value, dict)
            or value.get("schema_version") != VERSION or value.get("mode") != "session"
            or value.get("kind") not in ("current", "terminal_delivery", "no_current_delivery")):
        _invalid("previous", "Pass the complete previous successful session query result.")
    assert isinstance(value, dict)
    has_delivery = value["kind"] != "no_current_delivery"
    fields = {"schema_version", "kind", "mode", "task", "reuse"}
    if has_delivery:
        fields.add("delivery")
    if set(value) != fields:
        _invalid("previous", "Pass the complete previous successful session query result.")
    task = value["task"]
    if not isinstance(task, dict) or set(task) != _TASK_FIELDS | {"checkout_path"}:
        _invalid("previous.task", "Use the unchanged Task object from the previous successful query.")
    _task({field: task[field] for field in _TASK_FIELDS})
    if not isinstance(task["checkout_path"], str) or not Path(task["checkout_path"]).is_absolute():
        _invalid("previous.task.checkout_path", "Use the verified absolute checkout locator.")
    marks = {"origin", "task", "checkout"}
    if has_delivery:
        marks.add("delivery")
        delivery = value["delivery"]
        if not isinstance(delivery, dict) or set(delivery) != _DELIVERY_FIELDS:
            _invalid("previous.delivery", "Use the exact prior Delivery locator.")
        _delivery(delivery["delivery_id"])
        if not all(isinstance(delivery[f], str) and delivery[f] for f in ("phase", "planning_root")):
            _invalid("previous.delivery", "Use the unchanged Delivery values.")
    reuse = value["reuse"]
    if not isinstance(reuse, dict) or set(reuse) != marks or not all(
        isinstance(mark, str) and mark for mark in reuse.values()
    ):
        _invalid("previous.reuse", "Pass the reuse object from the prior successful query.")


def _validate(request: dict, *, exact: bool) -> None:
    fields = {"schema_version", "task", "delivery_id"}
    if not exact:
        fields.update(("intent", "previous"))
    if set(request) - fields or request.get("schema_version") != VERSION:
        _invalid("input", "Use the closed continuation input with schema_version 1.0.")
    intent = request.get("intent")
    if not exact and intent not in ("continue_session", "inspect_task"):
        _invalid("intent", "Choose continue_session or inspect_task.")
    if "task" in request:
        _task(request["task"])
    elif exact or intent == "inspect_task" or "delivery_id" in request:
        _invalid("task", "Provide the explicit Task identity for this query.")
    if "delivery_id" in request:
        _delivery(request["delivery_id"])
    elif exact:
        _invalid("delivery_id", "Provide the exact Delivery UUID for the record read.")
    if "previous" in request:
        if intent != "continue_session":
            _invalid("previous", "Only continue_session accepts the previous session result.")
        _previous(request["previous"])


def main(argv: list[str] | None = None) -> int:
    parser = Parser(prog="read-continuation-context",
                    description="Read current Task, checkout and Delivery location without writing resources.")
    parser.add_argument("--root", default=".", help="Repository checkout.")
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument("--input", choices=("-",), help="Read continuation input on stdin.")
    choice.add_argument("--delivery-record", choices=("-",),
                        help="Read an exact Delivery record for an already verified checkout.")
    try:
        args = parser.parse_args(argv)
        exact = args.delivery_record is not None
        request = read_json("-", "input") if args.input or exact else _DEFAULT
        _validate(request, exact=exact)
        root = Path(args.root).resolve()
        result = read_exact_delivery(root, request) if exact else read_continuation(root, request)
        write_json(result)
        return int(result.get("kind") == "error")
    except CommandError as exc:
        return fail(exc)
    except LifecycleContractError as exc:
        return fail(CommandError(exc.code, exc.field_path, exc.remediation))


if __name__ == "__main__":
    raise SystemExit(main())
