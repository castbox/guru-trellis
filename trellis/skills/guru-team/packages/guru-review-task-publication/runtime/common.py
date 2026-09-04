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
    "runtime",
}

_OWNER_NAMESPACE_PROJECTIONS = {
    "issue_scope_ledger": ("task_content", "publication.issue_scope_ledger"),
    "publication_content": ("publication_content", "publication.pr_payload.body"),
    "branch_review_handoff": ("stale_identity", "input.branch_review_commit"),
    "runtime_dependency": ("runtime_dependency", "runtime"),
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
    namespace = _owner_namespace(payload)
    if _has_namespaced_owner_errors(payload) and namespace is None:
        return None
    value = payload.get("error_code")
    if isinstance(value, str) and _SAFE_CODE.fullmatch(value.strip()):
        return value.strip()
    values = payload.get("error_codes")
    if isinstance(values, list):
        raw_candidates = [item.strip() for item in values if isinstance(item, str) and item.strip()]
        if namespace:
            for item in raw_candidates:
                item_namespace, detail = item.split(":", 1)
                if item_namespace.strip() != namespace:
                    continue
                detail = detail.strip()
                return detail if _SAFE_CODE.fullmatch(detail) else f"{namespace}_contract_failed"
        candidates = [item for item in raw_candidates if _SAFE_CODE.fullmatch(item)]
        joined = " ".join(candidates).casefold()
        if any(token in joined for token in ("continuity", "reviewed_content", "reviewed-content")):
            return "reviewed_content_continuity_failed"
        if any(token in joined for token in ("input", "authoring", "schema", "contract")):
            return "publication_input_invalid"
        if len(candidates) == 1:
            return candidates[0]
    values = payload.get("errors")
    if isinstance(values, list):
        if namespace:
            for item in values:
                if isinstance(item, str) and ":" in item:
                    item_namespace, detail = item.split(":", 1)
                    if item_namespace.strip() != namespace:
                        continue
                    detail = detail.strip()
                    return detail if _SAFE_CODE.fullmatch(detail) else f"{namespace.strip()}_contract_failed"
        joined = " ".join(item for item in values if isinstance(item, str)).casefold()
        if any(token in joined for token in ("continuity", "reviewed content", "reviewed-content")):
            return "reviewed_content_continuity_failed"
        if any(token in joined for token in ("input", "authoring", "schema", "contract")):
            return "publication_input_invalid"
    return None


def _owner_error_values(payload: dict[str, Any]) -> list[str]:
    values = payload.get("error_codes")
    if not isinstance(values, list):
        values = payload.get("errors")
    if not isinstance(values, list):
        return []
    return [item.strip() for item in values if isinstance(item, str) and item.strip()]


def _has_namespaced_owner_errors(payload: dict[str, Any]) -> bool:
    return any(":" in item for item in _owner_error_values(payload))


def _owner_namespace(payload: dict[str, Any]) -> str | None:
    values = _owner_error_values(payload)
    if not values or any(":" not in item for item in values):
        return None
    namespaces = {
        item.split(":", 1)[0].strip()
        for item in values
    }
    if len(namespaces) != 1:
        return None
    namespace = next(iter(namespaces))
    return namespace if namespace in _OWNER_NAMESPACE_PROJECTIONS else None


def _owner_locator(payload: dict[str, Any], namespace: str, code: str) -> str:
    values = _owner_error_values(payload)
    details = [item.split(":", 1)[1].strip() for item in values if ":" in item]
    if namespace == "issue_scope_ledger" and code == "issue_scope_ledger_primary_disposition_invalid":
        return "publication.issue_scope_ledger.primary_issue"
    if namespace == "publication_content":
        title_error = any(detail == "PR title is empty" for detail in details)
        body_error = any(
            detail == "PR body is empty" or detail.startswith("PR body ")
            for detail in details
        )
        if title_error and not body_error:
            return "publication.pr_payload.title"
        if title_error and body_error:
            return "publication.pr_payload"
    return _OWNER_NAMESPACE_PROJECTIONS[namespace][1]


def _diagnostic_from_owner_error(exc: BaseException) -> CommandError:
    payload = getattr(exc, "payload", None)
    payload = payload if isinstance(payload, dict) else {}
    code = _stable_code(payload)
    namespace = _owner_namespace(payload)
    if code in _FRESHNESS_CODES or payload.get("freshness") is True:
        code = "publication_stale"
    elif code is None:
        code = "internal_error"

    locator = payload.get("field_path", payload.get("locator"))
    if namespace and (not isinstance(locator, str) or locator.strip() in {"", "owner", "publication"}):
        locator = _owner_locator(payload, namespace, code)
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
    recovery_scope = _OWNER_NAMESPACE_PROJECTIONS[namespace][0] if namespace else None
    if recovery_scope is None and code in {
        "publication_stale",
        "reviewed_content_continuity_failed",
    }:
        recovery_scope = "stale_identity"
    response = {
        "code": code,
        "field_path": locator,
        "remediation": remediation,
    }
    if recovery_scope:
        response["recovery_scope"] = recovery_scope
    return CommandError(code, locator, remediation, response=response)


def call_owner(owner: Any, command: Callable[..., dict[str, Any]], *args: Any) -> dict[str, Any]:
    try:
        return command(*args)
    except owner.WorkflowError as exc:
        raise _diagnostic_from_owner_error(exc) from exc
