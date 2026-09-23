from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class LifecycleContractError(ValueError):
    code: str
    field_path: str
    remediation: str

    def __str__(self) -> str:
        return f"{self.code}: {self.field_path}: {self.remediation}"

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "field_path": self.field_path,
            "remediation": self.remediation,
        }


__all__ = ["LifecycleContractError"]
