from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from .installed import MARKER_PATTERNS, read_workflow_routing, validate_skill_installed, workflow_facts
from .io import CommandError, read_json_file, write_json
from .validate import _package_paths, validate, validate_interface_contract


CURRENT_INTERFACE_SCHEMA_IDS = {
    "guru-team-skill-interface-1.4",
    "guru-team-skill-interface-1.5",
    "guru-team-skill-interface-1.6",
    "guru-team-skill-interface-1.7",
    "guru-team-skill-interface-1.8",
    "guru-team-skill-interface-1.9",
    "guru-team-skill-interface-1.10",
}


def _safe_relative(value: Any, field_path: str) -> Path:
    if not isinstance(value, str):
        raise CommandError("contract_asset_invalid", field_path, "Restore the normalized package contract path.")
    path = Path(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise CommandError("contract_asset_invalid", field_path, "Restore the normalized package contract path.")
    return path


def call_local_public_input(package: Path, interface: dict[str, Any]) -> dict[str, Any]:
    """Read the target Interface's own fixed call-local input declaration."""
    declaration = interface.get("public_contracts", {}).get("invocation", {}).get("call_local", {}).get("public_input")
    if not isinstance(declaration, dict):
        raise CommandError("missing_contract", "invocation.call_local.public_input", "Declare the target-owned structured call-local input.")
    resolved = {}
    for key, directory in (("schema", "schemas"), ("example", "examples")):
        relative = _safe_relative(declaration[key]["path"], "call_local.public_input." + key)
        if relative.parts[0] != directory:
            raise CommandError("contract_asset_invalid", "call_local.public_input." + key, "Use the target package's public schema and example directories.")
        path = package / relative
        if not path.is_file() or path.is_symlink():
            raise CommandError("missing_contract", "call_local.public_input." + key, "Restore the target-owned public input asset.")
        resolved[key] = path
    from .schema import validate_json
    example = read_json_file(resolved["example"], "call_local.public_input.example")
    schema = read_json_file(resolved["schema"], "call_local.public_input.schema")
    if schema.get("$id") != declaration["schema"]["schema_id"]:
        raise CommandError("version_state_mismatch", "call_local.public_input.schema", "Use the declared target-owned input schema identity.")
    validate_json(example, resolved["schema"], "call_local.public_input.example")
    return resolved


def select_authoring_profile(contract: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    """Select only the producer's declared handoff discriminator."""
    if "authoring_profiles" not in contract:
        return contract
    selected = output.get(contract["profile_selector"]["field"])
    matches = [row for row in contract["authoring_profiles"] if row["profile_id"] == selected]
    if len(matches) != 1:
        raise CommandError("profile_binding_mismatch", "consumer.authoring_profiles", "Preserve one declared authoring profile for the actual producer handoff.")
    return matches[0]


def _skill_interface(skills_root: Path, skill_id: str) -> tuple[dict[str, Any], dict[str, Any], Path]:
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
    return entry, interface, interface_path.parent


def discover(skills_root: Path, skill_id: str) -> dict[str, Any]:
    entry, interface, _ = _skill_interface(skills_root, skill_id)
    interface_schema_id = entry["interface_schema_id"]
    contracts = interface.get("public_contracts")
    if not isinstance(contracts, dict):
        raise CommandError(
            "public_contracts_missing",
            f"skills.{skill_id}.public_contracts",
            "Declare the public contract sections required by the selected Interface.",
        )
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


def _one(values: list[dict[str, Any]], field: str) -> dict[str, Any]:
    if len(values) != 1:
        raise CommandError(
            "unmapped_exit" if not values else "multiple_exit_contracts", field,
            "Restore one current output, projection and unique consumer contract for this exit.",
        )
    return values[0]


def _target_entry(root: Path, routing: Path, text: str, consumer: dict[str, Any]) -> dict[str, Any]:
    lines = text.splitlines()
    starts = [index for index, line in enumerate(lines) if line.strip() == "### " + consumer["id"]]
    if len(starts) != 1:
        raise CommandError("unmapped_exit", "consumer.entry", "Restore one target section in the managed routing reference.")
    start = starts[0]
    end = next((index for index in range(start + 1, len(lines)) if re.match(r"^#{1,3}\s", lines[index])), len(lines))
    section = lines[start:end]
    markers = [
        (match.group(1), json.loads(match.group(2)))
        for line in section if (match := MARKER_PATTERNS["target"].fullmatch(line))
    ]
    if markers != [(consumer["kind"], {"id": consumer["id"]})]:
        raise CommandError("unmapped_exit", "consumer.entry", "Keep the target's unique marker inside its matching Markdown section.")
    body = "\n".join(line for line in section[1:] if not MARKER_PATTERNS["target"].fullmatch(line)).strip()
    if not body:
        raise CommandError("unmapped_exit", "consumer.entry", "Restore the original target's behavior and necessary contract references.")
    return {"locator": routing.relative_to(root).as_posix() + "#" + consumer["id"], "body": body}


def discover_exit(root: Path, mode: str, skills_root: Path, skill_id: str, exit_id: str) -> dict[str, Any]:
    entry, interface, package = _skill_interface(skills_root, skill_id)
    exits = [row for row in interface["external_exits"] if row.get("id") == exit_id]
    if not exits:
        raise CommandError("unknown_exit", "exit", "Choose one exit declared by the selected active Skill.")
    selected = _one(exits, "exit")
    contracts = interface["public_contracts"]
    output = _one([row for row in contracts["outputs"] if row.get("exit_id") == exit_id], "output_contract")
    workflow = root / ("trellis/workflows/guru-team/workflow.md" if mode == "source" else ".trellis/workflow.md")
    extension_root = root / ("trellis/workflows/guru-team" if mode == "source" else ".trellis/guru-team")
    registry = read_json_file(skills_root / "registry.json", "registry")
    active = {
        row["id"]: {**row, "interface_data": read_json_file(skills_root / row["interface"], "interface")}
        for row in registry["skills"] if row.get("state") == "active"
    }
    errors: list[str] = []
    workflow_facts(root, workflow, active, True, errors, extension_root=extension_root)
    if errors:
        raise CommandError("workflow_graph_invalid", "workflow", "Restore the matching workflow reference and Interface graph: " + "; ".join(errors))
    consumer = selected["consumer"]
    result = {
        "status": "ok", "skill_id": skill_id, "exit_id": exit_id,
        "consumer": consumer, "contract_root": package.relative_to(root).as_posix(),
        "output_contract": output,
    }
    if interface.get("execution_kind") == "instruction_only":
        result["entry"] = {"locator": (package / "SKILL.md").relative_to(root).as_posix(), "body": output["contract"]}
        return result
    projection = _one([row for row in contracts["projections"] if row.get("exit_id") == exit_id], "projection")
    if output.get("consumer_use_ids") != [projection["id"]]:
        raise CommandError("unmapped_exit", "output_contract.consumer_use_ids", "Bind the selected output to its one declared consumer projection.")
    consumer_input = _one([
        row for row in contracts["consumer_inputs"]
        if row.get("id") == projection["consumer_input_id"] and row.get("consumer") == consumer
    ], "consumer_input")
    result.update(consumer_input=consumer_input, projection=projection)
    contract = consumer_input.get("contract", {})
    if contract.get("kind") == "json_schema":
        relative = _safe_relative(contract.get("path"), "consumer_input.contract.path")
        # The querying AI reads this schema through the existing package/shared roots.
        schema_path = next((
            path for path in (package / relative, skills_root / relative)
            if path.is_file() and not path.is_symlink()
        ), None)
        if schema_path is None:
            raise CommandError("missing_contract", "consumer_input.contract.path", "Restore the selected consumer schema under its package or shared consumers root.")
        result["consumer_schema_locator"] = schema_path.relative_to(root).as_posix()
    if consumer["kind"] == "skill":
        _, target_interface, target_package = _skill_interface(skills_root, consumer["id"])
        if contract.get("kind") == "skill_call_local_input":
            assets = call_local_public_input(target_package, target_interface)
            result["consumer_schema_locator"] = assets["schema"].relative_to(root).as_posix()
            result["consumer_example_locator"] = assets["example"].relative_to(root).as_posix()
        result["entry"] = {
            "locator": (target_package / "SKILL.md").relative_to(root).as_posix(),
            "contract_root": target_package.relative_to(root).as_posix(),
            "entry_preconditions": target_interface["entry_preconditions"],
            "input": target_interface["public_contracts"]["input"],
            "invocation": target_interface["public_contracts"]["invocation"],
        }
    elif entry.get("workflow_integration_state", "integrated") == "integrated":
        routing, routing_text = read_workflow_routing(workflow, extension_root)
        result["entry"] = _target_entry(root, routing, routing_text, consumer)
    else:
        result["entry"] = {"locator": (package / "SKILL.md").relative_to(root).as_posix()}
    return result


def _validated_skills_root(root: Path, mode: str, *, require_workflow: bool = False) -> Path:
    skills_root, _, _, _ = _package_paths(root, mode)
    if mode == "installed":
        result = validate_skill_installed(
            root,
            skills_root,
            root / ".trellis/workflow.md",
            root / ".trellis/guru-team/extension.json",
            require_workflow=require_workflow,
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
    parser.add_argument("--exit", action="append", dest="exits")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = Path(args.root).resolve()
        if args.exits is not None and len(args.exits) != 1:
            raise CommandError("multiple_exits", "exit", "Query exactly one original Skill exit at a time.")
        skills_root = _validated_skills_root(root, args.mode, require_workflow=bool(args.exits))
        write_json(
            discover_exit(root, args.mode, skills_root, args.skill, args.exits[0])
            if args.exits else discover(skills_root, args.skill)
        )
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
