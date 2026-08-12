from __future__ import annotations

import json
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


def read_json(value: str, field_path: str) -> dict[str, Any]:
    if value == "-":
        value = sys.stdin.read()
    elif isinstance(value, str):
        try:
            candidate = Path(value)
            if candidate.is_file():
                value = candidate.read_text(encoding="utf-8")
        except OSError:
            pass
    try:
        payload = json.loads(value)
    except (TypeError, json.JSONDecodeError) as exc:
        raise CommandError("invalid_json", field_path, "Provide one valid JSON object.") from exc
    if not isinstance(payload, dict):
        raise CommandError("invalid_json", field_path, "Provide one valid JSON object.")
    return payload


def read_json_file(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise CommandError("missing_contract", label, "Restore the declared regular JSON contract file.")
    return read_json(path.read_text(encoding="utf-8"), label)


def write_json(payload: dict[str, Any], *, stream: Any = None) -> None:
    target = sys.stdout if stream is None else stream
    target.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def fail(error: CommandError) -> int:
    payload = error.response or {
        "code": error.code,
        "field_path": error.field_path,
        "remediation": error.remediation,
    }
    stream = sys.stderr if error.response_stream == "stderr" else sys.stdout
    write_json(payload, stream=stream)
    return error.exit_status
