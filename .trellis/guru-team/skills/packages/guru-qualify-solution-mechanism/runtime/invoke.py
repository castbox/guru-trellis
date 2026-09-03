from __future__ import annotations

import argparse
from pathlib import Path

from common import check_value, parse, record_value, stdin_object, typed_output, validate_receipt
from runtime.schema import validate_json


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--invocation", required=True)
    args = parse(parser, argv)
    envelope = stdin_object(args.invocation, "invocation")
    schema = package_root.parents[1] / "consumers" / "workflow" / "production" / "solution-mechanism-qualification-invocation.schema.json"
    validate_json(envelope, schema, "invocation")
    recorded = record_value(package_root, envelope["semantic_result"])
    receipt = check_value(package_root, recorded)
    supplied = envelope.get("validation_receipt")
    if supplied is not None:
        validate_receipt(recorded, supplied)
    return typed_output(package_root, recorded)
