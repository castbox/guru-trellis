"""Creation-owned pending input lifetime and its matching Author consumer port."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.task_lifecycle.errors import LifecycleContractError


def pending_directory(root: Path, task_ref: str) -> Path:
    return root / ".trellis/.runtime/guru-team/delivery-creation" / Path(task_ref).name


def checkpoint(root: Path, task_ref: str, continuation_id: str) -> Path:
    return pending_directory(root, task_ref) / (hashlib.sha256(continuation_id.encode()).hexdigest() + ".json")


def retire_creation_result(root: Path, *, task_ref: str, delivery_key: dict) -> bool:
    """Author calls after validating its successful initial handoff.

    The consumer supplies only its public identity. Creation validates and
    removes its own matching operation; absent or stale pending inputs remain
    ordinary owner state and do not overturn an otherwise current Author.
    """
    root = root.resolve()
    directory = pending_directory(root, task_ref)
    try:
        projection = DeliveryProjection(root, task_ref)
        current = projection.current(delivery_key)
        if current.get("kind") != "current" or current.get("key") != delivery_key:
            return False
        delivery = projection.resolve(delivery_key)
        if (delivery["phase"] != "planning"
                or delivery["scope_ref"]["authority"] != projection.read_record()["accepted_scope"]):
            return False
        owner = projection.declaration()["owners"]["creation"]
        consumed = False
        for path in directory.glob("*.json"):
            operation = json.loads(path.read_text())
            projection._call(projection.api.delivery_operations.parse_operation, operation)
            if (operation["operation"] == "create_delivery" and operation["key"] == delivery_key
                    and operation["owner_role"] == "creation" and operation["owner_id"] == owner
                    and operation["scope_ref"] == delivery["scope_ref"] and operation["profile"] == delivery["profile"]):
                path.unlink()
                consumed = True
        if consumed and not any(directory.iterdir()):
            directory.rmdir()
        return consumed
    except (LifecycleContractError, OSError, ValueError):
        return False
