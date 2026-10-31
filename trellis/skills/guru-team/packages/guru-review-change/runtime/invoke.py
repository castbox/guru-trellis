from __future__ import annotations

import argparse
from pathlib import Path

from context import capture, validate_input
from runtime.io import CommandError, read_json
from runtime.schema import validate_json


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--invocation", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Provide --invocation with one call-local envelope or dash for stdin.") from exc
    envelope = read_json(args.invocation, "invocation")
    validate_json(envelope, package_root / "schemas/invocation.schema.json", "invocation")
    public_input, owner_result = envelope["public_input"], envelope["owner_result"]
    validate_input(package_root, public_input)
    exit_id = owner_result["exit_id"]
    if exit_id == "reviewed" and owner_result["snapshot"] != capture(package_root, public_input):
        raise CommandError("stale_identity", "owner_result.snapshot", "Reread changed content, recapture and complete the affected review before retrying.", 3)
    output = {"exit_id": exit_id}
    validate_json(output, package_root / f"schemas/public-{exit_id}-output.schema.json", "stdout")
    return output
