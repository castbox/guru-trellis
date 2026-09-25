from __future__ import annotations

import re
from typing import Any

from .errors import LifecycleContractError


REPOSITORY_REF_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*$")
LEGACY_ISSUE_SCOPE = re.compile(
    r"^GitHub issue: https://github\.com/([A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*)/issues/([1-9][0-9]*)$"
)
ISSUE_DISPOSITIONS = {"exact_source", "reference_only", "follow_up", "parent"}
BRANCH_REF_PATTERN = re.compile(
    r"^(?!-)(?!HEAD$)(?!/)(?!refs/remotes/)(?!(?:refs/heads/)?guru-task-lifecycle(?:/|$))"
    r"(?!.*(?:^|/)\.)(?!.*(?:^|/)[^/]*\.lock(?:/|$))"
    r"(?!.*\.\.)(?!.*@\{)"
    r"(?!.*[ ~^:?*\[\]\\])(?!.*[./]$)[^/]+(?:/[^/]+)*$"
)


def normalize_repo_ref(value: Any, *, field_path: str = "repo_ref") -> str:
    if not isinstance(value, str) or not REPOSITORY_REF_PATTERN.fullmatch(value) or value.endswith(".git"):
        raise LifecycleContractError(
            "invalid_repository_ref", field_path, "Use one portable owner/repository identity without a URL or .git suffix."
        )
    return value


def normalize_source(value: Any, *, field_path: str = "source") -> dict[str, Any]:
    if not isinstance(value, dict):
        raise LifecycleContractError("invalid_source_relation", field_path, "Use the closed issue or no_issue source object.")
    kind = value.get("kind")
    if kind == "no_issue" and set(value) == {"kind"}:
        return {"kind": "no_issue"}
    if kind == "issue" and set(value) == {"kind", "repo_ref", "number", "disposition"}:
        number = value.get("number")
        disposition = value.get("disposition")
        if type(number) is not int or number < 1 or not isinstance(disposition, str) or disposition not in ISSUE_DISPOSITIONS:
            raise LifecycleContractError(
                "invalid_source_relation", field_path, "Use a positive Issue number and a declared source disposition."
            )
        return {
            "kind": "issue",
            "repo_ref": normalize_repo_ref(value.get("repo_ref"), field_path=f"{field_path}.repo_ref"),
            "number": number,
            "disposition": value["disposition"],
        }
    raise LifecycleContractError(
        "invalid_source_relation", field_path, "Use exactly {kind:no_issue} or {kind:issue,repo_ref,number,disposition}."
    )


def task_source(metadata: Any) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise LifecycleContractError("invalid_source_relation", "task.json", "Read a task metadata object.")
    if "source" in metadata:
        return normalize_source(metadata["source"])
    scope = metadata.get("scope")
    matched = LEGACY_ISSUE_SCOPE.fullmatch(scope) if isinstance(scope, str) else None
    if matched is None:
        raise LifecycleContractError(
            "source_review_required", "task.json.source", "Review the legacy source relation before Closure."
        )
    return normalize_source({
        "kind": "issue", "repo_ref": matched[1], "number": int(matched[2]), "disposition": "exact_source",
    })


def normalize_branch_ref(value: Any, *, field_path: str = "branch_ref") -> str:
    if not isinstance(value, str) or not BRANCH_REF_PATTERN.fullmatch(value) or value.endswith((".", "/")):
        raise LifecycleContractError(
            "invalid_branch_ref",
            field_path,
            "Use one portable branch ref without a remote-tracking namespace, SHA, reflog selector or path traversal.",
        )
    return value


def normalize_delivery_target(value: Any, *, field_path: str = "delivery_target") -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != {"repo_ref", "branch_ref"}:
        raise LifecycleContractError(
            "invalid_delivery_target", field_path, "Use exactly repo_ref and branch_ref."
        )
    return {
        "repo_ref": normalize_repo_ref(value["repo_ref"], field_path=f"{field_path}.repo_ref"),
        "branch_ref": normalize_branch_ref(value["branch_ref"], field_path=f"{field_path}.branch_ref"),
    }


__all__ = ["normalize_branch_ref", "normalize_delivery_target", "normalize_repo_ref", "normalize_source", "task_source"]
