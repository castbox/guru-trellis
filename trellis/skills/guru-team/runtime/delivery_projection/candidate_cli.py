"""Read-only CLI for the original implementation owner's Git Candidate facts."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from ..io import CommandError, fail, read_json, write_json
from ..task_lifecycle.errors import LifecycleContractError
from .adapter import DeliveryProjection


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CommandError("invalid_arguments", "arguments", message + ". Read --help for this command's public contract.")


def construct(
    root: Path, task_ref: str, key: dict, paths: list[str], *, head: str,
    development_base: str | None = None, observed_target: str | None = None,
) -> dict:
    """Project existing facts without selecting scope, writing a gate or reworking."""
    projection = DeliveryProjection(root, task_ref)
    projection.resolve(key)
    projection._require_explicit_task(key)
    current = projection.current(key)
    kind = current.get("kind")
    if kind == "error":
        raise LifecycleContractError(current["code"], "current.error", current["message"])
    if kind == "no_current_task":
        raise LifecycleContractError("no_current_task", "session.task", "Invoke original Identity/Ensure/Bind for this explicit Task, then reread current.")
    if kind == "no_current_delivery":
        raise LifecycleContractError("no_current_delivery", "session.delivery", "Invoke guru-create-delivery:delivery_selection for this explicit key, then reread current.")
    if kind == "terminal_delivery":
        raise LifecycleContractError("terminal_delivery", "delivery.phase", "Return to the original terminal/release owner; do not construct an execution candidate for a terminal Delivery.")
    if kind != "current" or current.get("key") != key:
        raise LifecycleContractError("delivery_selection_conflict", "current.key", "Use this receiving session's exact current Delivery; resolve a different selection through its original owner.")
    delivery = current["delivery"]
    if delivery["profile"] != "pull_request" or delivery["profile"] not in projection.declaration()["profiles"]:
        raise LifecycleContractError("unsupported_delivery_profile", "delivery.profile", "This construct entry serves the current Git pull_request Delivery. Existing upstream git_free candidate consumers retain their own entry.")
    actual_head = projection.commit("HEAD")
    if projection.commit(head) != actual_head:
        raise LifecycleContractError("candidate_head_mismatch", "head", "Reread this checkout's actual HEAD and review the changed content before constructing its candidate.")
    base = projection.content_base(key, development_base=development_base, observed_target=observed_target)
    return projection.candidate(paths, head_ref=actual_head, base_ref=base)


def main(argv: list[str] | None = None) -> int:
    parser = Parser(
        prog="construct-delivery-candidate",
        description="Construct the current Git pull_request Delivery's complete Candidate; stdout is the existing Candidate JSON object and no state is written.",
        epilog="The original owner selects B and paths. An existing same-Delivery B wins, then actual prior delivered heads, then --development-base or the unique merge base of --observed-target. No fetch or integration occurs. Consume this output through the original delivery.py begin-check/rework contracts; this command supplies no semantic pass.",
    )
    parser.add_argument("--root", default=".", help="Registered Task checkout (default: current directory).")
    parser.add_argument("--task", required=True, help="Exact repository-relative active TaskRef from Identity/Ensure.")
    parser.add_argument("--delivery-key", required=True, help="Actual DeliveryKey: inline JSON, a regular UTF-8 JSON file, or - for stdin.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--development-base", help="Owner-selected development baseline, used only when no same-Delivery/prior-delivery base exists.")
    source.add_argument("--observed-target", help="One locally available observed target commit, used only when no retained or explicit development base exists.")
    parser.add_argument("--head", required=True, help="Actual current HEAD; resolved to its complete commit OID.")
    parser.add_argument("--paths", required=True, nargs="+", help="Owner-selected repository-relative file paths, including the actual dirty increment and deleted files; directories are not expanded recursively. The original algorithm adds complete B..HEAD committed paths.")
    try:
        args = parser.parse_args(argv)
        key = read_json(args.delivery_key, "delivery_key")
        result = construct(Path(args.root).resolve(), args.task, key, args.paths,
                           head=args.head, development_base=args.development_base,
                           observed_target=args.observed_target)
        write_json(result)
        return 0
    except CommandError as exc:
        return fail(exc)
    except LifecycleContractError as exc:
        return fail(CommandError(exc.code, exc.field_path, exc.remediation, 3))
    except (OSError, subprocess.CalledProcessError):
        return fail(CommandError("internal_error", "candidate", "Candidate fact construction failed. Preserve the original exit/stdout/stderr and report the failure to the original executor maintainer; do not repair runtime or reconstruct a partial Candidate in the business call."))


if __name__ == "__main__":
    raise SystemExit(main())
