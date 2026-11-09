from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import url2pathname

from .io import CommandError, read_json_file


def _contract_locator(schema_path: Path) -> str:
    for parent in schema_path.parents:
        if parent.name in {"packages", "contracts"}:
            return parent.name + "/" + schema_path.relative_to(parent).as_posix()
    return schema_path.name


def _constraint_diagnostic(error: Any) -> tuple[list[Any], str]:
    """Describe the failed contract without echoing submitted values."""
    path = list(error.absolute_path)
    rule, expected = error.validator, error.validator_value
    if rule == "required":
        missing = [name for name in expected if name not in error.instance]
        if missing:
            return [*path, missing[0]], "required field is missing"
    if rule == "additionalProperties":
        import re
        properties = error.schema.get("properties", {})
        patterns = error.schema.get("patternProperties", {})
        unknown = sorted(name for name in error.instance if name not in properties
                         and not any(re.search(pattern, name) for pattern in patterns))
        if unknown:
            return [*path, unknown[0]], "field is not declared by this closed object"
        return path, "object contains fields outside its declared closed properties"
    if rule in {"type", "enum", "const", "pattern", "minLength", "maxLength", "minimum", "maximum", "minItems", "maxItems"}:
        import json
        return path, f"{rule} must match {json.dumps(expected, ensure_ascii=False)}"
    return path, f"{rule} constraint is not satisfied"


def _diagnostic_error(errors: list[Any]) -> Any:
    """Prefer a declared exit or uniquely closest branch, without changing validity."""
    from jsonschema.exceptions import best_match

    selected = best_match(errors)
    if selected is None:
        return None
    root = selected
    while root.parent is not None and root not in errors:
        root = root.parent
    if root.validator in {"oneOf", "anyOf"} and root.context:
        branches: dict[int, list[Any]] = {}
        for child in root.context:
            branch = next(iter(child.schema_path), None)
            if not isinstance(branch, int):
                return selected
            branches.setdefault(branch, []).append(child)
        if isinstance(root.instance, dict) and "exit_id" in root.instance:
            # Object-level errors retain the resolved branch schema, including
            # declarations loaded through the validator's existing relative refs.
            matching = []
            declarations_known = True
            for group in branches.values():
                declarations = []
                pending = list(group)
                while pending:
                    child = pending.pop()
                    if child.absolute_path != root.absolute_path:
                        continue
                    if isinstance(child.schema, dict):
                        declaration = child.schema.get("properties", {}).get("exit_id", {})
                        if isinstance(declaration, dict) and "const" in declaration:
                            declarations.append(declaration["const"])
                    if child.validator in {"oneOf", "anyOf"}:
                        pending.extend(child.context)
                if not declarations:
                    declarations_known = False
                if root.instance["exit_id"] in declarations:
                    matching.append(group)
            if declarations_known and len(matching) == 1:
                return _diagnostic_error(matching[0])
        fewest = min(len(group) for group in branches.values())
        closest = [group for group in branches.values() if len(group) == fewest]
        if len(closest) == 1:
            return _diagnostic_error(closest[0])
    return selected


def validate_json(instance: Any, schema_path: Path, field_path: str) -> None:
    schema = read_json_file(schema_path, str(schema_path))
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ImportError as exc:
        raise CommandError("runtime_dependency_missing", field_path, "Install the Python jsonschema dependency.") from exc
    # Selected package contracts use relative refs for their versioned index.
    # Their published ids are names, so resolve those refs from the actual
    # installed file without changing the public schema on disk.
    def retrieve(uri: str) -> Resource:
        parsed = urlparse(uri)
        if parsed.scheme != "file":
            raise ValueError("Contract references must resolve to installed files.")
        path = Path(url2pathname(parsed.path))
        value = dict(read_json_file(path, str(path)))
        value["$id"] = path.resolve().as_uri()
        return Resource.from_contents(value)

    local = dict(schema)
    local["$id"] = schema_path.resolve().as_uri()
    errors = list(Draft202012Validator(local, registry=Registry(retrieve=retrieve)).iter_errors(instance))
    error = _diagnostic_error(errors)
    if error is not None:
        path, constraint = _constraint_diagnostic(error)
        suffix = ".".join(str(part) for part in path)
        raise CommandError(
            "schema_mismatch", field_path + (f".{suffix}" if suffix else ""),
            f"Contract {_contract_locator(schema_path)}: {constraint}. "
            "Read that contract and its current profile example, correct the named input and rerun this original command.",
        )
