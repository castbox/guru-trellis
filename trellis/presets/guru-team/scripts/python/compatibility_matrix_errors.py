"""Failure projection helpers for the Trellis compatibility matrix."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Sequence


SCHEMA_VERSION = "1.0"
FAILURE_TAIL_LIMIT = 2000
FAILURE_STAGES = {"pre-matrix", "matrix-cell", "post-matrix"}
DEFAULT_COMMAND_TIMEOUT_SECONDS = 600.0


class MatrixError(RuntimeError):
    """A deterministic matrix precondition or cell check failed."""

    def __init__(
        self,
        message: str,
        *,
        stage: str = "pre-matrix",
        cell_id: str | None = None,
        command_label: str = "matrix-validation",
        exit_code: int = 2,
        error_tail: str | None = None,
    ) -> None:
        super().__init__(message)
        self.stage = stage
        self.cell_id = cell_id
        self.command_label = command_label
        self.exit_code = exit_code
        self.error_tail = error_tail if error_tail is not None else message

    def with_context(self, stage: str, cell_id: str | None) -> "MatrixError":
        return MatrixError(
            str(self),
            stage=stage,
            cell_id=cell_id,
            command_label=self.command_label,
            exit_code=self.exit_code,
            error_tail=self.error_tail,
        )


def command_timeout_seconds() -> float:
    raw = os.environ.get("GURU_MATRIX_COMMAND_TIMEOUT_SECONDS", "")
    if not raw:
        return DEFAULT_COMMAND_TIMEOUT_SECONDS
    try:
        value = float(raw)
    except ValueError:
        return DEFAULT_COMMAND_TIMEOUT_SECONDS
    return value if value > 0 else DEFAULT_COMMAND_TIMEOUT_SECONDS


def _sanitize_failure_tail(value: str) -> str:
    text = value.replace("\x00", "")
    text = re.sub(
        r"(?is)-----BEGIN [^-\r\n]*PRIVATE KEY-----.*?(?:-----END [^-\r\n]*PRIVATE KEY-----|$)",
        "<redacted-private-key>",
        text,
    )
    text = re.sub(r"(?i)(https?://)[^/\s@]+@", r"\1<redacted>@", text)
    text = re.sub(
        r"(?i)(github_pat_|ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9_]+",
        "<redacted-token>",
        text,
    )
    text = re.sub(r"(?i)(x-access-token:)[^@\s]+", r"\1<redacted>", text)
    text = re.sub(
        r"(?i)(authorization:\s*(?:bearer|basic)\s+)[^\s]+",
        r"\1<redacted>",
        text,
    )
    text = re.sub(
        r"(?i)(\b[A-Z0-9_]*(?:TOKEN|PASSWORD|SECRET|API[_-]?KEY|ACCESS[_-]?KEY)[A-Z0-9_]*\b\s*[=:]\s*)[^\s&]+",
        r"\1<redacted>",
        text,
    )
    text = re.sub(
        r"(?i)([?&](?:token|access_token|api[_-]?key|awsaccesskeyid|x-amz-(?:credential|signature)|x-goog-(?:credential|signature))=)[^&\s]+",
        r"\1<redacted>",
        text,
    )
    return text[-FAILURE_TAIL_LIMIT:]


def _stable_command_label(argv: Sequence[str]) -> str:
    executable = Path(str(argv[0])).name if argv else "unknown-command"
    if (executable.startswith("python") or executable == "resolve-python.sh") and len(argv) > 1:
        for value in argv[1:]:
            candidate = Path(str(value)).name
            if candidate.endswith((".py", ".sh")):
                return candidate
    return executable


def matrix_failure_payload(exc: MatrixError) -> dict[str, Any]:
    stage = exc.stage if exc.stage in FAILURE_STAGES else "pre-matrix"
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "failed",
        "failure": {
            "kind": "matrix_failure",
            "stage": stage,
            "cell_id": exc.cell_id if stage == "matrix-cell" else None,
            "command_label": exc.command_label,
            "exit_code": exc.exit_code,
            "error_tail": _sanitize_failure_tail(exc.error_tail),
        },
    }
