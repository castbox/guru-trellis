from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .command import main as run_command
from .io import CommandError, fail, read_json_file


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--validator", required=True)
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    try:
        args = parser.parse_args(argv)
        package_root = Path(args.package_root).resolve()
        metadata = read_json_file(package_root / "commands.json", "commands.json")
        matches = [
            command
            for command in metadata.get("commands", [])
            if command.get("validator_id") == args.validator
        ]
        if len(matches) != 1:
            raise CommandError(
                "unknown_command",
                "validator",
                "Select exactly one validator declared by the package command index.",
            )
        command_args = args.arguments
        if command_args[:1] == ["--"]:
            command_args = command_args[1:]
        return run_command(package_root, [matches[0]["id"], *command_args])
    except CommandError as exc:
        return fail(exc)
    except SystemExit:
        return fail(CommandError(
            "invalid_arguments",
            "arguments",
            "Use --package-root, --validator and an optional -- command separator.",
        ))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
