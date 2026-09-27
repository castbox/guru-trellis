from __future__ import annotations

import json
from typing import Any

from .branch_store import TaskLifecycleKey
from .errors import LifecycleContractError
from .git_facts import RepositoryFacts
from .resource_ledger import CleanupResource, ResourceLedgerStore
from .schema import validate_dto


def read_handoff_cleanup_inventory(repository: RepositoryFacts, inventory_ref: dict[str, Any]) -> dict[str, Any]:
    ref = validate_dto("HandoffInventoryRefDTO", inventory_ref)
    key = TaskLifecycleKey(ref["task_id"], ref["lifecycle_generation"])
    path = (repository.common_dir / "guru-team" / "handoff-cleanup" / key.task_id /
            str(key.lifecycle_generation) / f'{ref["handoff_id"]}.json')
    if not path.is_file() or path.is_symlink():
        raise LifecycleContractError(
            "handoff_inventory_missing", "handoff_inventory", "Recover the exact released source handoff inventory."
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise LifecycleContractError(
            "handoff_inventory_invalid", "handoff_inventory", "Read one valid source handoff inventory."
        ) from exc
    if (not isinstance(data, dict) or set(data) != {"schema_version", "inventory_ref", "handoff_ref", "resource_ids", "state"}
            or data["schema_version"] != "1.0" or data["state"] != "released"
            or data["inventory_ref"] != ref):
        raise LifecycleContractError(
            "handoff_inventory_stale", "handoff_inventory", "Use the exact released handoff inventory identity."
        )
    handoff = validate_dto("HandoffRefDTO", data["handoff_ref"])
    if (handoff["task_id"], handoff["lifecycle_generation"], handoff["handoff_id"]) != (
            key.task_id, key.lifecycle_generation, ref["handoff_id"]):
        raise LifecycleContractError("handoff_inventory_stale", "handoff_ref", "Keep handoff and inventory lifecycle equal.")
    identifiers = data["resource_ids"]
    if (not isinstance(identifiers, list) or not identifiers or
            any(not isinstance(item, str) or not item for item in identifiers) or
            identifiers != sorted(set(identifiers))):
        raise LifecycleContractError("handoff_inventory_invalid", "resource_ids", "Use sorted exact source resource identities.")
    ledger = ResourceLedgerStore(repository).read(key)
    if ledger is None:
        raise LifecycleContractError("resource_ownership_missing", "ledger", "Recover source resource responsibility.")
    rows = {row.resource_id: row for row in ledger.resources}
    if any(item not in rows or rows[item].ownership != "guru_owned" or
           rows[item].state != "cleanup_pending" or rows[item].responsibility_role != "retired_cleanup" or
           rows[item].kind == "remote_branch" or rows[item].expected_cleanup_head is None
           for item in identifiers):
        raise LifecycleContractError("handoff_inventory_stale", "resource_ids", "Keep source local resource responsibility pending.")
    resources = [CleanupResource(row.resource_id, row.kind, row.portable_ref, row.expected_cleanup_head).as_dict()
                 for item in identifiers for row in [rows[item]]]
    return {"handoff_ref": handoff, "resources": resources}
