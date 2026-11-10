from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .installed import parse_workflow_markers, validate_skill_installed
from .io import CommandError, read_json_file, write_json
from .validate import _package_paths, validate, validate_interface_contract


CURRENT_INTERFACE_SCHEMA_IDS = {
    "guru-team-skill-interface-1.4",
    "guru-team-skill-interface-1.5",
    "guru-team-skill-interface-1.6",
    "guru-team-skill-interface-1.7",
    "guru-team-skill-interface-1.8",
    "guru-team-skill-interface-1.9",
}


def _safe_relative(value: Any, field_path: str) -> Path:
    if not isinstance(value, str):
        raise CommandError("contract_asset_invalid", field_path, "Restore the normalized package contract path.")
    path = Path(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise CommandError("contract_asset_invalid", field_path, "Restore the normalized package contract path.")
    return path


def _interface(skills_root: Path, skill_id: str) -> tuple[dict, Path, dict]:
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
            "Declare the public contract sections required by the selected Interface.",
        )
    return entry, interface_path, interface


def _unique(items: list[dict], field_path: str) -> dict:
    if not items:
        raise CommandError("unmapped_exit", field_path, "Restore the declared exit's unique workflow and Interface mapping.")
    if len(items) != 1:
        raise CommandError("multiple_exit", field_path, "Keep exactly one mapping for the selected exit or consumer.")
    return items[0]


def _consumer_entry(skills_root: Path, consumer: dict, consumer_input: dict) -> dict:
    entry, interface_path, interface = _interface(skills_root, consumer["id"])
    contract = consumer_input.get("contract", {})
    if contract.get("interface_path") != entry["interface"]:
        raise CommandError("consumer_mismatch", "consumer_input.contract.interface_path", "Reference the consumer's current registered Interface.")
    inputs = interface["public_contracts"]["input"]
    input_locator = {"interface_path": entry["interface"], "section": "public_contracts.input", "kind": inputs["kind"]}
    if "profile_selector" in contract:
        input_locator["profile_selector"] = contract["profile_selector"]
    elif "profile_id" in contract:
        profiles = [item for item in inputs.get("profiles", []) if item["id"] == contract["profile_id"]]
        profile = _unique(profiles, "consumer_input.contract.profile_id")
        input_locator.update(profile_id=profile["id"], schema=profile["schema"], example=profile["example"])
    return {
        "interface_path": entry["interface"],
        "skill_path": (interface_path.parent / "SKILL.md").relative_to(skills_root).as_posix(),
        "invocation": interface["public_contracts"]["invocation"],
        "input": input_locator,
    }


def _discover_exit(skills_root: Path, entry: dict, interface: dict, exit_id: str, workflow: Path | None) -> dict:
    declared = [item for item in interface["external_exits"] if item["id"] == exit_id]
    if not declared:
        raise CommandError("unknown_exit", "exit", "Choose an external exit declared by the selected current Interface.")
    selected = _unique(declared, "interface.external_exits")
    if workflow is None or not workflow.is_file() or workflow.is_symlink():
        raise CommandError("unmapped_exit", "workflow", "Restore the selected source or installed workflow before querying its exits.")
    errors: list[str] = []
    try:
        markers = parse_workflow_markers(workflow, errors)
    except (OSError, UnicodeError) as exc:
        raise CommandError("invalid_workflow", "workflow", "Provide the readable UTF-8 workflow for the selected mode.") from exc
    if errors:
        raise CommandError("invalid_workflow", "workflow", "Repair invalid workflow marker JSON before querying exits.")
    matching_markers = [
        item for item in markers["exit"]
        if item["payload"].get("skill") == entry["id"] and item["payload"].get("exit") == exit_id
    ]
    marker = _unique(matching_markers, "workflow.exit")
    consumer = selected["consumer"]
    if marker["payload"].get("consumer") != consumer:
        raise CommandError("consumer_mismatch", "workflow.exit.consumer", "Keep the workflow exit consumer identical to the selected Interface declaration.")
    contracts = interface["public_contracts"]
    output = _unique([item for item in contracts["outputs"] if item["exit_id"] == exit_id], "public_contracts.outputs")
    result = {
        "status": "ok", "skill_id": entry["id"], "exit_id": exit_id,
        "interface_schema_id": entry["interface_schema_id"], "interface_path": entry["interface"],
        "consumer": consumer, "output": output,
        "workflow_exit": {"path": str(workflow), "line": marker["line"]},
        "producer_entry": {
            "skill_path": str(Path(entry["interface"]).parent / "SKILL.md"),
            "invocation": contracts["invocation"],
        },
    }
    if interface.get("execution_kind") != "instruction_only":
        projections = [item for item in contracts["projections"] if item["exit_id"] == exit_id]
        projection = _unique(projections, "public_contracts.projections")
        consumer_inputs = [item for item in contracts["consumer_inputs"] if item["id"] == projection["consumer_input_id"]]
        consumer_input = _unique(consumer_inputs, "public_contracts.consumer_inputs")
        if output["consumer_use_ids"] != [projection["id"]] or consumer_input["consumer"] != consumer:
            raise CommandError("consumer_mismatch", "public_contracts.projections", "Bind the exit output and projection to its declared consumer input.")
        result.update(projection=projection, consumer_input=consumer_input)
    else:
        consumer_input = {}
    if consumer["kind"] == "skill":
        result["consumer_entry"] = _consumer_entry(skills_root, consumer, consumer_input)
    else:
        targets = [item for item in markers["target"] if item["payload"].get("id") == consumer["id"]]
        target = _unique(targets, "workflow.target")
        if target["kind"] != consumer["kind"]:
            raise CommandError("consumer_mismatch", "workflow.target", "Match the declared workflow or stop target kind.")
        result["consumer_entry"] = {"path": str(workflow), "line": target["line"]}
    return result


def discover(skills_root: Path, skill_id: str, exit_id: str | None = None, *, workflow: Path | None = None) -> dict[str, Any]:
    entry, _, interface = _interface(skills_root, skill_id)
    if exit_id is not None:
        return _discover_exit(skills_root, entry, interface, exit_id, workflow)
    interface_schema_id = entry["interface_schema_id"]
    contracts = interface["public_contracts"]
    if interface.get("execution_kind") == "instruction_only":
        return {
            "status": "ok",
            "skill_id": skill_id,
            "interface_schema_id": interface_schema_id,
            "execution_kind": "instruction_only",
            "input": contracts["input"],
            "invocation": contracts["invocation"],
            "outputs": contracts["outputs"],
            "external_exits": interface["external_exits"],
        }
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
    parser.add_argument("--exit", dest="exit_id", help="Locate the declared consumer of an actual typed exit without executing it.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = Path(args.root).resolve()
        workflow = root / "trellis/workflows/guru-team/workflow.md" if args.mode == "source" else root / ".trellis/workflow.md"
        write_json(discover(_validated_skills_root(root, args.mode), args.skill, args.exit_id, workflow=workflow))
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
