from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json


DELIVERY_SLOTS = {"planning", "delivery_review", "delivery_publication"}
REACTIVATION_SLOTS = {"reactivation", "validation"}
NON_COMPLETE = {
    "remaining_work", "evidence_pending", "additional_delivery_required",
    "requirements_revision_required", "implementation_revision_required",
}


def _load(root: Path, package: Path, name: str, field: str) -> dict:
    path = Path(name)
    candidates = [path] if path.is_absolute() else [root / path, package / path]
    source = next((item for item in candidates if item.is_file() and not item.is_symlink()), None)
    if source is None:
        raise CommandError("invalid_json", field, "Provide one existing regular JSON object.")
    try:
        value = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("invalid_json", field, "Provide one valid JSON object.") from exc
    if not isinstance(value, dict):
        raise CommandError("invalid_json", field, "Provide one JSON object.")
    return value


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the declared completion command.") from exc
    root = Path(args.root or ".").resolve()
    public = _load(root, package_root, args.input, "input")
    semantic = _load(root, package_root, args.semantic_result, "semantic_result")
    if public.get("profile", "").startswith("delivery_"):
        from delivery import invoke
        return invoke(root, package_root, public, semantic)
    raise CommandError("schema_mismatch", "profile", "Use the current TaskKey Completion profile; migrate legacy result evidence through its original owner.")


if __name__ == "__main__":
    try:
        print(json.dumps(run(Path(__file__).parents[1], {}, sys.argv[1:]), ensure_ascii=False))
    except CommandError as exc:
        print(json.dumps({"code": exc.code, "field_path": exc.field_path, "remediation": exc.remediation}), file=sys.stderr)
        raise SystemExit(exc.exit_status)
