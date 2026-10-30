from __future__ import annotations

import json
import os
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class CommandError(Exception):
    code: str
    field_path: str
    remediation: str
    exit_status: int = 2
    response: dict[str, Any] | None = None
    response_stream: str = "stdout"


def decode_json(
    value: str, field_path: str, *,
    syntax_remediation: str = "The JSON text has invalid syntax. Provide valid JSON with an object at the top level.",
) -> dict[str, Any]:
    """Decode already-read text without interpreting it as a carrier."""
    if isinstance(value, str) and not value.strip():
        raise CommandError("invalid_json", field_path, "The JSON input is empty. Provide one JSON object.")
    try:
        payload = json.loads(value)
    except (TypeError, json.JSONDecodeError) as exc:
        raise CommandError("invalid_json", field_path, syntax_remediation) from exc
    if not isinstance(payload, dict):
        raise CommandError("invalid_json", field_path, "The JSON top level must be an object. Provide a JSON object.")
    return payload


def read_stdin(field_path: str) -> str:
    try:
        return sys.stdin.read()
    except (OSError, UnicodeError) as exc:
        raise CommandError("invalid_json", field_path, "Cannot read JSON from stdin. Provide readable UTF-8 JSON input.") from exc


def read_json(value: str, field_path: str) -> dict[str, Any]:
    if value == "-":
        return decode_json(read_stdin(field_path), field_path)
    if not isinstance(value, str):
        return decode_json(value, field_path)

    candidate = Path(value)
    remediation = (
        "The input is neither an existing regular JSON file nor valid inline JSON. "
        "Use an explicit ./, ../ or absolute file path, or valid inline JSON or stdin if supported by this command."
    )
    try:
        mode = candidate.stat().st_mode
    except FileNotFoundError:
        relative_prefixes = tuple(
            parent + separator
            for separator in (os.sep, os.altsep) if separator is not None
            for parent in (".", "..")
        )
        if candidate.is_absolute() or value.startswith(relative_prefixes):
            remediation = "The JSON file does not exist. Provide an existing regular UTF-8 JSON file or another input form supported by this command."
    except OSError:
        remediation = "Cannot inspect the JSON input file. Provide a readable regular UTF-8 JSON file or another input form supported by this command."
    else:
        if stat.S_ISREG(mode):
            try:
                content = candidate.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                raise CommandError("invalid_json", field_path, "Cannot read the JSON file as UTF-8. Provide a readable regular UTF-8 JSON file.") from exc
            return decode_json(content, field_path)
        remediation = (
            "This JSON input carrier is not a regular file and is unsupported. "
            "Use a regular UTF-8 JSON file, or inline JSON or stdin if supported by this command."
        )
    return decode_json(value, field_path, syntax_remediation=remediation)


def read_json_file(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise CommandError("missing_contract", label, "Restore the declared regular JSON contract file.")
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise CommandError("invalid_json", label, "Cannot read the JSON file as UTF-8. Provide a readable regular UTF-8 JSON file.") from exc
    return decode_json(content, label)


def write_json(payload: dict[str, Any], *, stream: Any = None) -> None:
    target = sys.stdout if stream is None else stream
    target.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def project_intermediate_receipt(payload: Any, schemas: Path) -> dict[str, Any]:
    """Project current CLI transport for the same owner's record/check consumer."""
    from .schema import validate_json

    validate_json(payload, schemas / "intermediate-command-receipt-1.0.schema.json", "stdout")
    return payload["result"]


def fail(error: CommandError) -> int:
    payload = error.response or {
        "code": error.code,
        "field_path": error.field_path,
        "remediation": error.remediation,
    }
    stream = sys.stderr if error.response_stream == "stderr" else sys.stdout
    write_json(payload, stream=stream)
    return error.exit_status
