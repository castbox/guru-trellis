from __future__ import annotations

from collections.abc import Callable
import re
from typing import Any

from runtime.io import CommandError


def parse_arguments(parser: Any, argv: list[str]) -> Any:
    try:
        return parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError(
            "invalid_arguments",
            "arguments",
            "Use the exact command help contract.",
        ) from exc


_SAFE_CODE = re.compile(r"^[a-z][a-z0-9_]{1,63}$")
_SAFE_LOCATOR = re.compile(r"^[a-z][a-z0-9_.\[\]-]{0,127}$")
_FRESHNESS_CODES = {
    "publication_stale",
    "publication_freshness_failed",
    "owner_result_stale",
    "checkpoint_stale",
    "stale_publication",
}
_KNOWN_LOCATORS = {
    "arguments",
    "input",
    "input.profile",
    "input.task_ref",
    "input.branch_review_commit",
    "publication",
    "publication.freshness",
    "publication.owner_result",
    "reviewed_content",
    "reviewed_content.continuity",
    "git",
    "github",
    "owner",
}


def _stable_text(value: Any, fallback: str) -> str:
    if not isinstance(value, str):
        return fallback
    value = value.strip()
    lowered = value.casefold()
    if (
        not value
        or len(value) > 240
        or "\n" in value
        or "\r" in value
        or "://" in value
        or "ghp_" in lowered
        or "token" in lowered
        or "credential" in lowered
        or "/users/" in lowered
        or value.startswith(("/", "~"))
    ):
        return fallback
    return value


def _stable_code(payload: dict[str, Any]) -> str | None:
    value = payload.get("error_code")
    if isinstance(value, str) and _SAFE_CODE.fullmatch(value.strip()):
        return value.strip()
    values = payload.get("error_codes")
    if isinstance(values, list):
        candidates = [item.strip() for item in values if isinstance(item, str) and _SAFE_CODE.fullmatch(item.strip())]
        joined = " ".join(candidates).casefold()
        if any(token in joined for token in ("continuity", "reviewed_content", "reviewed-content")):
            return "reviewed_content_continuity_failed"
        if any(token in joined for token in ("input", "authoring", "schema", "contract")):
            return "publication_input_invalid"
        if len(candidates) == 1:
            return candidates[0]
    values = payload.get("errors")
    if isinstance(values, list):
        joined = " ".join(item for item in values if isinstance(item, str)).casefold()
        if any(token in joined for token in ("continuity", "reviewed content", "reviewed-content")):
            return "reviewed_content_continuity_failed"
        if any(token in joined for token in ("input", "authoring", "schema", "contract")):
            return "publication_input_invalid"
    return None


def _diagnostic_from_owner_error(exc: BaseException) -> CommandError:
    payload = getattr(exc, "payload", None)
    payload = payload if isinstance(payload, dict) else {}
    code = _stable_code(payload)
    if code in _FRESHNESS_CODES or payload.get("freshness") is True:
        code = "publication_stale"
    elif code is None:
        code = "internal_error"

    locator = payload.get("field_path", payload.get("locator"))
    if not isinstance(locator, str) or not _SAFE_LOCATOR.fullmatch(locator.strip()):
        locator = "publication" if code != "internal_error" else "owner"
    else:
        locator = locator.strip()
        if locator not in _KNOWN_LOCATORS and not locator.startswith(("input.", "publication.", "reviewed_content.", "github.")):
            locator = "publication"

    remediation = payload.get("remediation", payload.get("recovery"))
    remediation = _stable_text(remediation, "Inspect the Publication owner contract and retry.")
    if code == "publication_stale":
        remediation = _stable_text(remediation, "Repeat the ten-dimension review against current evidence.")
    elif code == "internal_error":
        remediation = "Inspect the Publication package runtime and retry."
    return CommandError(code, locator, remediation)


def call_owner(owner: Any, command: Callable[..., dict[str, Any]], *args: Any) -> dict[str, Any]:
    try:
        return command(*args)
    except owner.WorkflowError as exc:
        raise _diagnostic_from_owner_error(exc) from exc
