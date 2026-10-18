#!/usr/bin/env python3
"""Verify the managed dependency set and required Draft 2020-12 behavior."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import sys
from pathlib import Path
from typing import Any


def load_manifest(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("dependencies"), dict):
        raise RuntimeError("invalid Python runtime manifest")
    return payload


def verify_versions(manifest: dict[str, Any]) -> dict[str, str]:
    observed: dict[str, str] = {}
    for distribution, expected in sorted(manifest["dependencies"].items()):
        actual = importlib.metadata.version(distribution)
        if actual != expected:
            raise RuntimeError(f"dependency version mismatch: {distribution}")
        observed[distribution] = actual
    return observed


def verify_draft_2020_12() -> None:
    from jsonschema import Draft202012Validator, FormatChecker

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$defs": {"label": {"type": "string", "minLength": 2}},
        "type": "object",
        "required": ["kind", "email", "labels", "value"],
        "properties": {
            "kind": {"enum": ["number", "text"]},
            "email": {"type": "string", "format": "email"},
            "labels": {"type": "array", "contains": {"$ref": "#/$defs/label"}},
            "value": {"oneOf": [{"type": "number"}, {"$ref": "#/$defs/label"}]},
        },
        "if": {"properties": {"kind": {"const": "number"}}},
        "then": {"properties": {"value": {"type": "number"}}},
        "else": {"properties": {"value": {"type": "string"}}},
    }
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    validator.validate({"kind": "number", "email": "owner@example.com", "labels": ["ok"], "value": 3})
    invalid = {"kind": "number", "email": "bad", "labels": ["x"], "value": "wrong"}
    if len(list(validator.iter_errors(invalid))) < 3:
        raise RuntimeError("Draft 2020-12 capability probe did not reject invalid data")


def probe(manifest_path: Path) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    versions = verify_versions(manifest)
    verify_draft_2020_12()
    return {"status": "ok", "dependencies": versions, "draft": "2020-12"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = probe(args.manifest)
    except Exception as exc:
        if args.json:
            print(json.dumps({"status": "failed", "error": str(exc)}, sort_keys=True))
        else:
            print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True) if args.json else "managed Python runtime: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
