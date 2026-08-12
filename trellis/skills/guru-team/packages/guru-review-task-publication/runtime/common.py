from __future__ import annotations

from collections.abc import Callable
from typing import Any

from runtime.io import CommandError


def parse_arguments(parser: Any, argv: list[str]) -> Any:
    try:
        return parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError(
            "invalid_arguments",
            "arguments",
            "Use the exact command help contract.",
        ) from exc


def call_owner(owner: Any, command: Callable[..., dict[str, Any]], *args: Any) -> dict[str, Any]:
    try:
        return command(*args)
    except owner.WorkflowError as exc:
        raise CommandError(
            "publication_stale",
            "publication",
            "Repeat the ten-dimension review against current evidence.",
        ) from exc
