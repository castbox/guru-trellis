from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .installed import validate_skill_installed
from .io import CommandError, read_json_file, write_json
from .validate import _package_paths, validate, validate_interface_contract


CURRENT_INTERFACE_SCHEMA_IDS = {
    "guru-team-skill-interface-1.4",
    "guru-team-skill-interface-1.5",
    "guru-team-skill-interface-1.6",
}


def _safe_relative(value: Any, field_path: str) -> Path:
    if not isinstance(value, str):
        raise CommandError("contract_asset_invalid", field_path, "Restore the normalized package contract path.")
    path = Path(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise CommandError("contract_asset_invalid", field_path, "Restore the normalized package contract path.")
    return path


def discover(skills_root: Path, skill_id: str) -> dict[str, Any]:
    registry = read_json_file(skills_root / "registry.json", "registry")
    rows = registry.get("skills") if isinstance(registry.get("skills"), list) else []
    matches = [
        row for row in rows
        if isinstance(row, dict) and row.get("id") == skill_id and row.get("state") == "active"
    ]
    if len(matches) != 1:
        raise CommandError(
            "unknown_skill",
            "skill",
            "Choose one active stable Skill id from the validated registry.",
        )
    entry = matches[0]
    interface_schema_id = str(entry.get("interface_schema_id") or "")
    if interface_schema_id not in CURRENT_INTERFACE_SCHEMA_IDS:
        raise CommandError(
            "version_state_mismatch",
            f"skills.{skill_id}.interface_schema_id",
            "Use one of the registry-supported current Interface contracts.",
        )
    interface_path = skills_root / _safe_relative(entry.get("interface"), f"skills.{skill_id}.interface")
    interface = read_json_file(interface_path, f"skills.{skill_id}.interface")
    validate_interface_contract(skills_root, interface_path.parent, entry, interface)
    contracts = interface.get("public_contracts")
    if not isinstance(contracts, dict):
        raise CommandError(
            "public_contracts_missing",
            f"skills.{skill_id}.public_contracts",
            "Declare all six current Interface public/private contract sections.",
        )
    return {
        "status": "ok",
        "skill_id": skill_id,
        "interface_schema_id": interface_schema_id,
        "input": contracts.get("input"),
        "invocation": contracts.get("invocation"),
        "outputs": contracts.get("outputs"),
        "consumer_inputs": contracts.get("consumer_inputs"),
        "projections": contracts.get("projections"),
        "private_artifacts": contracts.get("private_artifacts"),
    }


def _validated_skills_root(root: Path, mode: str) -> Path:
    skills_root, _, _, _ = _package_paths(root, mode)
    if mode == "installed":
        result = validate_skill_installed(
            root,
            skills_root,
            root / ".trellis/workflow.md",
            root / ".trellis/guru-team/extension.json",
            require_workflow=False,
        )
        if result.get("status") != "passed":
            raise CommandError(
                "installed_drift",
                ".trellis/guru-team/skills",
                "Reapply the complete preset, resolve sidecars, and rerun installed package validation.",
            )
    else:
        validate(root, mode)
    return skills_root


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Discover one validated public Skill contract.")
    parser.add_argument("--root", required=True)
    parser.add_argument("--mode", required=True, choices=("source", "installed"))
    parser.add_argument("--skill", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = Path(args.root).resolve()
        write_json(discover(_validated_skills_root(root, args.mode), args.skill))
        return 0
    except CommandError as exc:
        sys.stderr.write(json.dumps({
            "code": exc.code,
            "field_path": exc.field_path,
            "remediation": exc.remediation,
        }, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
        return exc.exit_status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
