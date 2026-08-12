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


def call_owner(
    owner: Any,
    command: Callable[..., dict[str, Any]],
    *args: Any,
    public: bool = False,
) -> dict[str, Any]:
    try:
        return command(*args)
    except owner.WorkflowError as exc:
        response = None
        stream = "stdout"
        if not public:
            response = {"status": "error", "error": str(exc), **exc.payload}
            stream = "stderr"
        raise CommandError(
            "finalization_stale",
            "finalization",
            "Reprepare from current publication authority.",
            exc.exit_code,
            response=response,
            response_stream=stream,
        ) from exc
