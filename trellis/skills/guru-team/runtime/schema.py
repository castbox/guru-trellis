from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import CommandError, read_json_file


def validate_json(instance: Any, schema_path: Path, field_path: str) -> None:
    schema = read_json_file(schema_path, str(schema_path))
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise CommandError("runtime_dependency_missing", field_path, "Install the Python jsonschema dependency.") from exc
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda item: list(item.path))
    if errors:
        suffix = ".".join(str(part) for part in errors[0].path)
        raise CommandError("schema_mismatch", field_path + (f".{suffix}" if suffix else ""), "Repair the JSON value to match the declared schema.")
