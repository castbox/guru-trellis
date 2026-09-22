from __future__ import annotations

import re
from typing import Any

from .errors import LifecycleContractError


REPOSITORY_REF_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*$")
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
    if kind == "issue" and set(value) == {"kind", "repo_ref", "number"}:
        number = value.get("number")
        if type(number) is not int or number < 1:
            raise LifecycleContractError(
                "invalid_source_relation", f"{field_path}.number", "Use a positive Issue number."
            )
        return {
            "kind": "issue",
            "repo_ref": normalize_repo_ref(value.get("repo_ref"), field_path=f"{field_path}.repo_ref"),
            "number": number,
        }
    raise LifecycleContractError(
        "invalid_source_relation", field_path, "Use exactly {kind:no_issue} or {kind:issue,repo_ref,number}."
    )


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


__all__ = ["normalize_branch_ref", "normalize_delivery_target", "normalize_repo_ref", "normalize_source"]
