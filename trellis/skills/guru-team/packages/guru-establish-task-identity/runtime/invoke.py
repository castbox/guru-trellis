from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.identity import resolve_task_ref
from runtime.task_lifecycle.source import normalize_source, task_source


def invoke(root: Path, data: dict) -> dict:
    package = Path(__file__).resolve().parents[1]
    validate_json(data, package / "schemas/public-input.schema.json", "input")
    try:
        artifact = resolve_task_ref(root, data["task_ref"], expected_task_id=data["task_id"])
        if artifact.lifecycle_state != "active" or artifact.lifecycle_generation != data["lifecycle_generation"]:
            return {"exit_id": "invalid_task_state", "reason_code": "task_identity_stale"}
        metadata = json.loads((root / artifact.task_ref / "task.json").read_text(encoding="utf-8"))
        if "source" in metadata and "reviewed_source" in data:
            return {"exit_id": "blocked", "reason_code": "source_already_authoritative"}
        try:
            source = task_source(metadata)
        except LifecycleContractError as exc:
            if exc.code != "source_review_required":
                raise
            if "reviewed_source" not in data:
                return {"exit_id": "source_review_required", "task_id": artifact.task_id,
                        "lifecycle_generation": artifact.lifecycle_generation}
            source = normalize_source(data["reviewed_source"])
        return {"exit_id": "identity_established", **artifact.as_dto(), "source": source}
    except LifecycleContractError as exc:
        if exc.code in {"invalid_task_id", "invalid_task_ref", "invalid_task_identity", "invalid_lifecycle_generation", "task_not_found"}:
            return {"exit_id": "invalid_task_state", "reason_code": exc.code}
        return {"exit_id": "blocked", "reason_code": exc.code}
    except (OSError, ValueError) as exc:
        return {"exit_id": "blocked", "reason_code": "task_metadata_unreadable"}


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    result = invoke(Path(args.root).resolve(), read_json(args.input, "input"))
    validate_json(result, package_root / "schemas/public-output.schema.json", "stdout")
    return result
