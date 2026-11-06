"""Public and installed Skill file projections owned by the preset installer."""

from __future__ import annotations

import json
from pathlib import Path

from skill_runtime_inventory import (
    PLATFORM_PACKAGE_REQUIRED_SCHEMA_PATHS,
    PLATFORM_PACKAGE_REQUIRED_PUBLIC_PATHS,
    PLATFORM_PACKAGE_PUBLIC_TEACHING_PATHS,
)

def skill_package_source_files(package_root: Path) -> list[Path]:
    return sorted(
        path
        for path in package_root.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and not {"__pycache__", ".pytest_cache"}.intersection(path.relative_to(package_root).parts)
        and path.suffix not in {".pyc", ".pyo"}
    )


def skill_package_installed_files(package_root: Path) -> list[Path]:
    """Return package files that belong in the installed runtime projection."""
    return [
        path
        for path in skill_package_source_files(package_root)
        if "tests" not in path.relative_to(package_root).parts
    ]


def skill_platform_public_files(package_root: Path) -> list[Path]:
    """Return the Agent-readable projection without package-private runtime assets."""
    interface = json.loads((package_root / "interface.json").read_text(encoding="utf-8"))
    required_schema_paths = PLATFORM_PACKAGE_REQUIRED_SCHEMA_PATHS.get(
        str(interface.get("id")), frozenset()
    )
    required_public_paths = PLATFORM_PACKAGE_REQUIRED_PUBLIC_PATHS.get(
        str(interface.get("id")), frozenset()
    )
    teaching_paths = PLATFORM_PACKAGE_PUBLIC_TEACHING_PATHS.get(str(interface.get("id")), frozenset())
    declared_artifacts = {
        Path(item["path"]) for item in interface.get("artifacts", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    if not teaching_paths.issubset(declared_artifacts) or any(
        not (package_root / path).is_file() or (package_root / path).is_symlink()
        for path in teaching_paths
    ):
        raise SystemExit(f"Missing declared public teaching example for {package_root.name}.")
    declared_schema_paths = {
        Path(str(item["path"]))
        for item in interface.get("schemas", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    if not required_schema_paths.issubset(declared_schema_paths):
        raise SystemExit(
            f"Platform-required schemas are not declared by {package_root.name}."
        )
    declared_public_examples = {
        Path(str(item["example"]["path"]))
        for item in interface.get("public_contracts", {}).get("input", {}).get("profiles", [])
        if isinstance(item, dict)
        and isinstance(item.get("example"), dict)
        and isinstance(item["example"].get("path"), str)
    }
    if not required_public_paths.issubset(declared_public_examples):
        raise SystemExit(
            f"Platform-required public examples are not declared by {package_root.name}."
        )
    private_paths = {
        str(item["schema"]["path"])
        for item in interface.get("public_contracts", {}).get("private_artifacts", [])
        if isinstance(item, dict)
        and isinstance(item.get("schema"), dict)
        and isinstance(item["schema"].get("path"), str)
    }
    for inventory_name in ("schemas", "artifacts"):
        private_paths.update(
            str(item["path"])
            for item in interface.get(inventory_name, [])
            if isinstance(item, dict)
            and isinstance(item.get("id"), str)
            and item["id"].startswith("legacy_private_gate_")
            and isinstance(item.get("path"), str)
        )
    private_artifact_paths = {
        str(item["path"])
        for item in interface.get("artifacts", [])
        if isinstance(item, dict)
        and isinstance(item.get("path"), str)
        and str(item["path"]) not in {
            str(ref.get("example", {}).get("path"))
            for ref in interface.get("public_contracts", {}).get("outputs", [])
            if isinstance(ref, dict) and isinstance(ref.get("example"), dict)
        }
    }
    invocation_examples = set(interface.get("public_contracts", {}).get("invocation", {}).get("example_argv", []))
    error_example = interface.get("public_contracts", {}).get("invocation", {}).get("error_example", {}).get("path")
    if isinstance(error_example, str):
        invocation_examples.add(error_example)
    public_example_paths = {path.as_posix() for path in declared_public_examples}
    public_example_paths.update(
        item["path"] for item in interface.get("artifacts", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
        and item["path"] in invocation_examples
    )
    private_artifact_paths.difference_update(public_example_paths)
    public_authoring_paths: set[Path] = set()
    for item in interface.get("public_contracts", {}).get("consumer_inputs", []):
        if not isinstance(item, dict) or not isinstance(item.get("contract"), dict):
            continue
        contract = item["contract"]
        for index, variant in enumerate((contract, *contract.get("alternate_authoring", []))):
            example = variant.get("authoring_example")
            if not isinstance(example, dict) or not isinstance(example.get("path"), str):
                continue
            relative = Path(example["path"])
            source = package_root / relative
            if index and (not source.is_file() or source.is_symlink()):
                raise SystemExit(f"Missing canonical Skill authoring example: {source}")
            public_authoring_paths.add(relative)
    public_wrapper = str(
        interface.get("public_contracts", {})
        .get("invocation", {})
        .get("wrapper", "")
    )
    excluded_roots = {"runtime", "tests", "errors"}
    result = []
    for path in skill_package_source_files(package_root):
        relative = path.relative_to(package_root)
        relative_text = relative.as_posix()
        if relative.parts[0] in excluded_roots:
            continue
        if relative.parts[0] == "scripts" and relative_text != public_wrapper:
            continue
        if relative in required_schema_paths or relative in required_public_paths or relative in teaching_paths:
            result.append(path)
            continue
        if relative in public_authoring_paths:
            result.append(path)
            continue
        if relative_text in private_paths or relative_text in private_artifact_paths:
            continue
        result.append(path)
    return result
