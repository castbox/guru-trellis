from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

from .io import CommandError, fail, read_json_file, write_json
from .installed import validate_skill_installed
from .schema import validate_json


APPROVED_KERNEL_FILES = {
    "__init__.py",
    "command.py",
    "bootstrap.py",
    "compat.py",
    "discovery.py",
    "eval_runner.py",
    "installed.py",
    "io.py",
    "launch.sh",
    "probe.py",
    "python-runtime.json",
    "reviewed_content.py",
    "requirements.lock",
    "resolve-python.sh",
    "schema.py",
    "temporary-inventory.json",
    "temporary_lifecycle.py",
    "validate.py",
}


def _fold_string(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _fold_string(node.left)
        right = _fold_string(node.right)
        if left is not None and right is not None:
            return left + right
    return None


def _active_rows(registry: dict[str, Any]) -> list[dict[str, Any]]:
    rows = registry.get("skills")
    if not isinstance(rows, list):
        raise CommandError("schema_mismatch", "registry.skills", "Restore the current Skill registry.")
    active = [row for row in rows if isinstance(row, dict) and row.get("state") == "active"]
    if len(active) != len({row.get("id") for row in active}):
        raise CommandError("owner_mismatch", "registry.skills", "Restore uniquely identified active packages.")
    return active


def _package_paths(root: Path, mode: str) -> tuple[Path, Path, Path, Path]:
    if mode == "source":
        skills = root / "trellis/skills/guru-team"
        return skills, skills / "registry.json", skills / "packages", skills / "runtime"
    extension = root / ".trellis/guru-team"
    skills = extension / "skills"
    return skills, skills / "registry.json", skills / "packages", extension / "runtime"


def validate_interface_contract(
    skills: Path,
    package: Path,
    row: dict[str, Any],
    interface: dict[str, Any],
) -> None:
    interface_schema_id = row.get("interface_schema_id")
    prefix = "guru-team-skill-interface-"
    if not isinstance(interface_schema_id, str) or not interface_schema_id.startswith(prefix):
        raise CommandError(
            "version_state_mismatch",
            f"{row.get('id', 'unknown')}.interface_schema_id",
            "Bind every active package to one published Interface schema id.",
        )
    version = interface_schema_id.removeprefix(prefix)
    expected_ref = f"../../schemas/skill-interface-{version}.schema.json"
    if (
        interface.get("$schema") != expected_ref
        or interface.get("schema_version") != version
        or interface.get("id") != row.get("id")
    ):
        raise CommandError(
            "version_state_mismatch",
            f"{row.get('id', 'unknown')}.interface",
            "Keep registry schema id, Interface schema reference, version and package id identical.",
        )
    schema_path = skills / f"schemas/skill-interface-{version}.schema.json"
    validate_json(interface, schema_path, f"{row['id']}.interface")

    public_contracts = interface.get("public_contracts")
    invocation = public_contracts.get("invocation") if isinstance(public_contracts, dict) else None
    input_contract = public_contracts.get("input") if isinstance(public_contracts, dict) else None
    binding = invocation.get("input_binding") if isinstance(invocation, dict) else None
    selector = binding.get("profile_selector") if isinstance(binding, dict) else None
    if not isinstance(selector, dict):
        return
    if not isinstance(input_contract, dict) or input_contract.get("kind") != "structured_json":
        raise CommandError(
            "profile_binding_mismatch",
            f"{row['id']}.public_contracts.input",
            "Use aggregate public-input profile selection only with a structured input contract.",
        )
    selector_field = selector.get("field")
    profiles = input_contract.get("profiles")
    if not isinstance(selector_field, str) or not isinstance(profiles, list) or not profiles:
        raise CommandError(
            "profile_binding_mismatch",
            f"{row['id']}.public_contracts.invocation.input_binding.profile_selector",
            "Declare one selector field and at least one closed structured input profile.",
        )
    profile_ids = [profile.get("id") for profile in profiles if isinstance(profile, dict)]
    discriminators = [profile.get("discriminator") for profile in profiles if isinstance(profile, dict)]
    discriminator_fields = [item.get("field") for item in discriminators if isinstance(item, dict)]
    discriminator_values = [item.get("value") for item in discriminators if isinstance(item, dict)]
    if (
        len(profile_ids) != len(profiles)
        or len(discriminator_fields) != len(profiles)
        or len(discriminator_values) != len(profiles)
        or len(set(profile_ids)) != len(profiles)
        or len(set(discriminator_values)) != len(profiles)
        or set(discriminator_fields) != {selector_field}
        or profile_ids != discriminator_values
    ):
        raise CommandError(
            "profile_binding_mismatch",
            f"{row['id']}.public_contracts.input.profiles",
            "Keep profile ids and unique discriminator values identical under the declared selector field.",
        )
    aggregate_ref = input_contract.get("aggregate_schema")
    if not isinstance(aggregate_ref, dict) or not isinstance(aggregate_ref.get("path"), str):
        raise CommandError(
            "profile_binding_mismatch",
            f"{row['id']}.public_contracts.input.aggregate_schema",
            "Declare the aggregate public-input schema used by selector binding.",
        )
    aggregate_schema = read_json_file(
        package / aggregate_ref["path"], f"{row['id']}.aggregate_schema"
    )
    profile_schemas: list[dict[str, Any]] = []
    profile_examples: list[dict[str, Any]] = []
    expected_refs: list[dict[str, str]] = []
    for profile in profiles:
        profile_schema_ref = profile.get("schema")
        example_ref = profile.get("example")
        if (
            not isinstance(profile_schema_ref, dict)
            or not isinstance(profile_schema_ref.get("path"), str)
            or not isinstance(example_ref, dict)
            or not isinstance(example_ref.get("path"), str)
        ):
            raise CommandError(
                "profile_binding_mismatch",
                f"{row['id']}.public_contracts.input.profiles",
                "Bind every selected profile to one closed schema and one public example.",
            )
        profile_schema_path = package / profile_schema_ref["path"]
        profile_schema = read_json_file(profile_schema_path, f"{row['id']}.{profile['id']}.schema")
        field_contract = profile_schema.get("properties", {}).get(selector_field)
        if not isinstance(field_contract, dict) or field_contract.get("const") != profile["id"]:
            raise CommandError(
                "profile_binding_mismatch",
                f"{row['id']}.public_contracts.input.profiles.{profile['id']}.discriminator",
                "Keep the closed profile schema const identical to its public discriminator.",
            )
        example = read_json_file(package / example_ref["path"], f"{row['id']}.{profile['id']}.example")
        validate_json(example, profile_schema_path, f"{row['id']}.{profile['id']}.example")
        profile_schemas.append(profile_schema)
        profile_examples.append(example)
        expected_refs.append({"$ref": Path(profile_schema_ref["path"]).name})
    if aggregate_schema.get("oneOf") != expected_refs:
        raise CommandError(
            "profile_binding_mismatch",
            f"{row['id']}.public_contracts.input.aggregate_schema",
            "Keep the aggregate oneOf in the exact declared profile order with package-local schema refs.",
        )
    resolved_aggregate = dict(aggregate_schema)
    resolved_aggregate["oneOf"] = profile_schemas
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise CommandError(
            "runtime_dependency_missing",
            f"{row['id']}.public_contracts.input.aggregate_schema",
            "Install the Python jsonschema dependency.",
        ) from exc
    for profile, example in zip(profiles, profile_examples, strict=True):
        errors = list(Draft202012Validator(resolved_aggregate).iter_errors(example))
        if errors:
            raise CommandError(
                "schema_mismatch",
                f"{row['id']}.{profile['id']}.aggregate_example",
                "Repair the public example to match exactly one aggregate profile schema.",
            )


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
        validate_interface_contract(skills, package, row, interface)
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
    actual_kernel_files = {
        path.name for path in kernel.iterdir()
        if path.is_file() and not path.is_symlink()
    }
    if actual_kernel_files != APPROVED_KERNEL_FILES:
        unexpected = sorted(actual_kernel_files - APPROVED_KERNEL_FILES)
        missing = sorted(APPROVED_KERNEL_FILES - actual_kernel_files)
        raise CommandError(
            "kernel_branching",
            str(kernel),
            f"Restore the closed neutral kernel inventory; unexpected={unexpected}, missing={missing}.",
        )
    forbidden_kernel_values = {
        "guru-sync-base", "guru-clarify-requirements", "typed_exit", "profile"
    }
    forbidden_kernel_functions = {"prepare", "reviewed_base_freshness", "_reviewed_base_freshness"}
    for path in kernel.glob("*.py"):
        if path.name == "validate.py":
            continue
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        folded_values = set()
        for node in ast.walk(tree):
            folded = _fold_string(node)
            if folded is not None:
                folded_values.add(folded)
        function_names = {
            node.name for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        if forbidden_kernel_values & folded_values or forbidden_kernel_functions & function_names:
            raise CommandError("kernel_branching", str(path), "Keep Skill, profile and typed-exit behavior package-local.")

    if mode == "source":
        compatibility_root = root / "trellis/workflows/guru-team/scripts/bash"
        declared_wrappers = {
            (package_id, Path(item["command"]).name)
            for package_id, interface in (
                (row["id"], read_json_file(packages / row["id"] / "interface.json", f"{row['id']}.interface"))
                for row in active
            )
            for item in interface["validators"]
        }
        for wrapper in compatibility_root.glob("*.sh"):
            source = wrapper.read_text(encoding="utf-8")
            matches = set(
                re.findall(
                    r"(?:skills/guru-team|skills)/packages/(guru-[a-z0-9-]+)/scripts/([a-z0-9-]+\.sh)",
                    source,
                )
            )
            if matches and not matches.issubset(declared_wrappers):
                raise CommandError(
                    "owner_mismatch",
                    str(wrapper),
                    "Route every package compatibility wrapper to a declared active validator wrapper.",
                )
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
