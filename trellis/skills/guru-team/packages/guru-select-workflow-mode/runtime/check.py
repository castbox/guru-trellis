from __future__ import annotations

from pathlib import Path

from runtime.io import CommandError


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    if command["id"] != "check-workflow-environment":
        raise CommandError(
            "invalid_arguments",
            "command",
            "Invoke the declared workflow environment command.",
        )
    from environment import run as check_environment

    return check_environment(argv)
