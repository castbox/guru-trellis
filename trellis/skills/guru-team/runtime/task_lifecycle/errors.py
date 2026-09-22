from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class LifecycleContractError(ValueError):
    code: str
    field_path: str
    remediation: str
    details: dict[str, Any] | None = None

    def __str__(self) -> str:
        return f"{self.code}: {self.field_path}: {self.remediation}"

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code,
            "field_path": self.field_path,
            "remediation": self.remediation,
        }
        if self.details:
            payload["details"] = dict(self.details)
        return payload


__all__ = ["LifecycleContractError"]
