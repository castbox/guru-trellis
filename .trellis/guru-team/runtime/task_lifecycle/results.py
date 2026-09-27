from __future__ import annotations

from typing import Any

from .schema import validate_dto


def task_identity(task_id: str, task_ref: str) -> dict[str, Any]:
    return validate_dto("TaskIdentityDTO", {"task_id": task_id, "task_ref": task_ref})


def task_lifecycle(task_id: str, lifecycle_generation: int) -> dict[str, Any]:
    return validate_dto(
        "TaskLifecycleDTO",
        {"task_id": task_id, "lifecycle_generation": lifecycle_generation},
    )


def task_artifact(task_id: str, task_ref: str, lifecycle_generation: int) -> dict[str, Any]:
    return validate_dto(
        "TaskArtifactDTO",
        {"task_id": task_id, "task_ref": task_ref, "lifecycle_generation": lifecycle_generation},
    )


def result_ref(task_id: str, lifecycle_generation: int, result_id: str) -> dict[str, Any]:
    return validate_dto(
        "ResultRefDTO",
        {"task_id": task_id, "lifecycle_generation": lifecycle_generation, "result_id": result_id},
    )


def transaction_ref(task_id: str, lifecycle_generation: int, transaction_id: str, result_id: str) -> dict[str, Any]:
    return validate_dto(
        "TransactionRefDTO",
        {
            "task_id": task_id,
            "lifecycle_generation": lifecycle_generation,
            "transaction_id": transaction_id,
            "result_id": result_id,
        },
    )


def reason(reason_code: str, reason_refs: list[str]) -> dict[str, Any]:
    return validate_dto("ReasonDTO", {"reason_code": reason_code, "reason_refs": reason_refs})


__all__ = ["reason", "result_ref", "task_artifact", "task_identity", "task_lifecycle", "transaction_ref", "validate_dto"]
