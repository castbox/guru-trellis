from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import url2pathname

from .io import CommandError, read_json_file


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
    errors = sorted(
        Draft202012Validator(local, registry=Registry(retrieve=retrieve)).iter_errors(instance),
        key=lambda item: list(item.path),
    )
    if errors:
        suffix = ".".join(str(part) for part in errors[0].path)
        raise CommandError("schema_mismatch", field_path + (f".{suffix}" if suffix else ""), "Repair the JSON value to match the declared schema.")
