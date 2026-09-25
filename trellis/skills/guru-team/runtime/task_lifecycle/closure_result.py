from __future__ import annotations

import json
from typing import Any

from .errors import LifecycleContractError
from .git_facts import RepositoryFacts
from .schema import validate_dto


def read_terminal_closure_result(repository: RepositoryFacts, result_ref: dict[str, Any]) -> dict[str, Any]:
    """Resolve the terminal action set owned by the exact Closure transaction."""

    result = validate_dto("ResultRefDTO", result_ref)
    path = (repository.common_dir / "guru-team" / "closure" /
            result["task_id"] / f'{result["lifecycle_generation"]}.json')
    if not path.is_file() or path.is_symlink():
        raise LifecycleContractError(
            "closure_result_missing", "closure_result", "Resume the exact terminal Closure transaction."
        )
    try:
        transaction = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise LifecycleContractError(
            "closure_result_invalid", "closure_result", "Read one valid terminal Closure transaction."
        ) from exc
    reference = transaction.get("ref") if isinstance(transaction, dict) else None
    frozen = transaction.get("frozen") if isinstance(transaction, dict) else None
    terminal = transaction.get("terminal") if isinstance(transaction, dict) else None
    if (not isinstance(reference, dict) or
            {field: reference.get(field) for field in result} != result or
            not isinstance(frozen, dict) or not isinstance(frozen.get("action_set"), list) or
            terminal not in {"closed", "no_mutation"}):
        raise LifecycleContractError(
            "closure_result_stale", "closure_result", "Use the exact terminal Closure result and action set."
        )
    return {"result_ref": result, "terminal": terminal, "action_set": frozen["action_set"]}
