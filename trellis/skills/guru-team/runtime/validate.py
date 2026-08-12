from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any

from .io import CommandError, fail, read_json_file, write_json
from .installed import validate_skill_installed
from .schema import validate_json


def _active_rows(registry: dict[str, Any]) -> list[dict[str, Any]]:
    rows = registry.get("skills")
    if not isinstance(rows, list):
        raise CommandError("schema_mismatch", "registry.skills", "Restore the current Skill registry.")
    active = [row for row in rows if isinstance(row, dict) and row.get("state") == "active"]
    if len(active) != 15 or len({row.get("id") for row in active}) != 15:
        raise CommandError("owner_mismatch", "registry.skills", "Restore exactly fifteen uniquely identified active packages.")
    return active


def _package_paths(root: Path, mode: str) -> tuple[Path, Path, Path, Path]:
    if mode == "source":
        skills = root / "trellis/skills/guru-team"
        return skills, skills / "registry.json", skills / "packages", skills / "runtime"
    extension = root / ".trellis/guru-team"
    skills = extension / "skills"
    return skills, skills / "registry.json", skills / "packages", extension / "runtime"


def validate(root: Path, mode: str, platform_root: Path | None = None) -> dict[str, Any]:
    skills, registry_path, packages, kernel = _package_paths(root, mode)
    registry = read_json_file(registry_path, "registry")
    active = _active_rows(registry)
    command_schema = skills / "schemas/skill-commands.schema.json"
    error_schema = skills / "schemas/skill-error-catalog.schema.json"
    commands_seen: dict[str, str] = {}
    complete = 0
    public_only = 0
    for row in active:
        package_id = row["id"]
        package = packages / package_id
        if platform_root is not None:
            projection = platform_root / package_id
            if not (projection / "SKILL.md").is_file() or (projection / "runtime").exists() or (projection / "errors").exists() or (projection / "tests").exists():
                raise CommandError("projection_invalid", str(projection), "Install only the declared public package projection.")
            public_only += 1
        metadata_path = package / "commands.json"
        if not metadata_path.is_file():
            raise CommandError("missing_contract", str(metadata_path), "Restore commands.json for every active package.")
        complete += 1
        metadata = read_json_file(metadata_path, f"{package_id}.commands")
        catalog = read_json_file(package / "errors/catalog.json", f"{package_id}.errors")
        validate_json(metadata, command_schema, f"{package_id}.commands")
        validate_json(catalog, error_schema, f"{package_id}.errors")
        codes = {item["code"] for item in catalog["errors"]}
        interface = read_json_file(package / "interface.json", f"{package_id}.interface")
        declared = {item["id"]: item["command"] for item in interface["validators"]}
        actual = {item["validator_id"] for item in metadata["commands"]}
        if set(declared) != actual:
            raise CommandError("owner_mismatch", f"{package_id}.commands", "Cover every interface validator runtime_command exactly once.")
        flags_by_command = {
            command["id"]: {argument["flag"] for argument in command["arguments"]}
            for command in metadata["commands"]
        }
        for command in metadata["commands"]:
            command_id = command["id"]
            if command_id in commands_seen:
                raise CommandError("duplicate_command", command_id, "Assign each global command id to one package owner.")
            commands_seen[command_id] = package_id
            wrapper = package / declared[command["validator_id"]]
            entrypoint = package / command["entrypoint"]
            if command["owner"] != package_id or not wrapper.is_file() or not entrypoint.is_file() or wrapper.is_symlink() or entrypoint.is_symlink():
                raise CommandError("owner_mismatch", f"{package_id}.{command_id}", "Restore the declared owner, wrapper and entrypoint.")
            expected_role = "preview" if command_id.startswith("preview-") else "sync" if command_id == "sync-base" else Path(command["entrypoint"]).stem
            if command["runtime_role"] != expected_role:
                raise CommandError("owner_mismatch", f"{package_id}.{command_id}.runtime_role", "Match runtime role to the package-local entrypoint.")
            flags = flags_by_command[command_id]
            for argument in command["arguments"]:
                if argument["flag"] in argument["conflicts"] or not set(argument["conflicts"]).issubset(flags):
                    raise CommandError("schema_mismatch", f"{package_id}.{command_id}.arguments", "Declare conflicts only against other arguments of the same command.")
                for conflict in argument["conflicts"]:
                    peer = next(item for item in command["arguments"] if item["flag"] == conflict)
                    if argument["flag"] not in peer["conflicts"]:
                        raise CommandError("schema_mismatch", f"{package_id}.{command_id}.arguments", "Declare argument conflicts symmetrically.")
            wrapper_source = wrapper.read_text(encoding="utf-8")
            if not package_id.startswith("guru-example-") and not all(
                candidate in wrapper_source
                for candidate in (
                    "../../../runtime/launch.sh",
                    "../../../../runtime/launch.sh",
                )
            ):
                raise CommandError(
                    "runtime_dependency_missing",
                    f"{package_id}.{command_id}.wrapper",
                    "Resolve the shared launcher in both canonical and installed package layouts.",
                )
            if (
                declared[command["validator_id"]] == "scripts/invoke.sh"
                and "../../../../.trellis/guru-team/runtime/launch.sh" not in wrapper_source
            ):
                raise CommandError(
                    "runtime_dependency_missing",
                    f"{package_id}.{command_id}.wrapper",
                    "Resolve the installed shared launcher from every declared platform projection.",
                )
            if not set(command["errors"]).issubset(codes):
                raise CommandError("unknown_error", f"{package_id}.{command_id}.errors", "Declare every referenced error in the package catalog.")
            if "guru_team_trellis.py" in wrapper_source or "guru_team_trellis.py" in entrypoint.read_text(encoding="utf-8"):
                raise CommandError("legacy_dependency", f"{package_id}.{command_id}", "Remove the shared monolith dependency.")
    for path in kernel.glob("*.py"):
        if path.name == "validate.py":
            continue
        source = path.read_text(encoding="utf-8")
        ast.parse(source)
        if any(token in source for token in ("guru-" + "sync-base", "guru-" + "clarify-requirements", "typed" + "_exit", "pro" + "file")):
            raise CommandError("kernel_branching", str(path), "Keep Skill, profile and typed-exit behavior package-local.")
    return {"status": "passed", "mode": mode, "active_packages": len(active), "complete_package_commands": complete, "public_projections": public_only, "commands": len(commands_seen)}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate Guru Team package-local command ownership.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--mode", required=True, choices=("source", "installed"))
    parser.add_argument("--platform-root")
    parser.add_argument("--json", action="store_true")
    try:
        args = parser.parse_args(argv)
        root = Path(args.root).resolve()
        if args.mode == "installed":
            result = validate_skill_installed(
                root,
                root / ".trellis/guru-team/skills",
                root / ".trellis/workflow.md",
                root / ".trellis/guru-team/extension.json",
            )
        else:
            result = validate(root, args.mode, Path(args.platform_root).resolve() if args.platform_root else None)
        write_json(result)
        return 0 if result.get("status") == "passed" else 2
    except CommandError as exc:
        return fail(exc)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
