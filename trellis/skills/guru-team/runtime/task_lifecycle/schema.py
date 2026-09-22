from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterator

from .errors import LifecycleContractError


CONTRACT_ROOT = Path(__file__).resolve().parents[2] / "contracts" / "task-lifecycle"
CATALOG_NAME = "task-lifecycle-dtos.schema.json"
_SCHEMA_NAME = re.compile(r"^[a-z0-9][a-z0-9.-]*\.schema\.json$")


def _nodes(value: Any) -> Iterator[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from _nodes(child)


def _validate_local_schema(schema: dict[str, Any], *, label: str) -> None:
    for node in _nodes(schema):
        if not isinstance(node, dict):
            continue
        ref = node.get("$ref")
        if ref is not None and (not isinstance(ref, str) or not ref.startswith("#/") or ".." in ref):
            raise LifecycleContractError(
                "unsafe_schema_reference",
                f"{label}.$ref",
                "Use a fragment reference within the selected task lifecycle schema.",
            )
        nested_id = node.get("$id")
        if node is not schema and nested_id is not None:
            raise LifecycleContractError(
                "nested_schema_identity",
                f"{label}.$id",
                "Keep the schema catalog as one local resource boundary.",
            )


def load_contract(name: str = CATALOG_NAME, *, contract_root: Path | None = None) -> dict[str, Any]:
    if not isinstance(name, str) or not _SCHEMA_NAME.fullmatch(name):
        raise LifecycleContractError(
            "invalid_contract_name", "contract", "Use one declared schema filename."
        )
    root = (contract_root or CONTRACT_ROOT).resolve()
    path = root / name
    try:
        if path.is_symlink() or not path.is_file() or path.resolve().parent != root:
            raise LifecycleContractError(
                "missing_contract", name, "Restore the regular schema below the task lifecycle contract root."
            )
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise LifecycleContractError(
            "invalid_contract_json", name, "Repair the schema JSON."
        ) from exc
    if not isinstance(payload, dict):
        raise LifecycleContractError(
            "invalid_contract_json", name, "Use one JSON object as the schema root."
        )
    _validate_local_schema(payload, label=name)
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise LifecycleContractError(
            "runtime_dependency_missing", "jsonschema", "Install the locked runtime dependencies."
        ) from exc
    try:
        Draft202012Validator.check_schema(payload)
    except Exception as exc:
        raise LifecycleContractError(
            "invalid_contract_schema", name, "Repair the Draft 2020-12 schema."
        ) from exc
    return payload


def dto_names(*, contract_root: Path | None = None) -> tuple[str, ...]:
    schema = load_contract(contract_root=contract_root)
    return tuple(sorted(name for name in schema["$defs"] if name.endswith("DTO")))


def validate_dto(name: str, payload: Any, *, contract_root: Path | None = None) -> dict[str, Any]:
    schema = load_contract(contract_root=contract_root)
    if name not in schema.get("$defs", {}) or not name.endswith("DTO"):
        raise LifecycleContractError(
            "unknown_dto", "dto_name", "Use one named DTO from the task lifecycle catalog."
        )
    selected = {
        "$schema": schema["$schema"],
        "$ref": f"#/$defs/{name}",
        "$defs": schema["$defs"],
    }
    from jsonschema import Draft202012Validator

    errors = sorted(Draft202012Validator(selected).iter_errors(payload), key=lambda item: list(item.path))
    if errors:
        suffix = ".".join(str(part) for part in errors[0].path)
        field = name + (f".{suffix}" if suffix else "")
        raise LifecycleContractError(
            "dto_schema_mismatch", field, "Provide the exact closed DTO fields and value domains."
        )
    if name == "HandoffRefDTO":
        expected_ref = f"refs/heads/guru-task-lifecycle/{payload['task_id']}"
        if payload["receipt_ref"] != expected_ref:
            raise LifecycleContractError(
                "dto_identity_mismatch",
                "HandoffRefDTO.receipt_ref",
                "Bind the handoff receipt control ref to the same TaskId as the DTO.",
            )
    return deepcopy(payload)


__all__ = ["CATALOG_NAME", "CONTRACT_ROOT", "dto_names", "load_contract", "validate_dto"]
