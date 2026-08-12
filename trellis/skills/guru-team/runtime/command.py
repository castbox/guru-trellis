from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

from .io import CommandError, fail, read_json_file, write_json


def _help(package_id: str, command: dict) -> str:
    usage = [command["id"]]
    lines = [f"usage: {' '.join(usage)} [arguments]", "", f"owner: {package_id}", f"stdin: {command['stdin']}", f"stdout: {command['stdout']}", f"side-effect: {command['side_effect']}", "", "arguments:", "  --help                show this help and exit", "  --json                emit one JSON object"]
    for item in command["arguments"]:
        marker = "required" if item["required"] else "optional"
        values = f" ({'|'.join(item.get('values', []))})" if item.get("values") else ""
        lines.append(f"  {item['flag']:<22} {marker}{values}: {item['description']}")
    lines.extend(["", "errors:", *[f"  {code}" for code in command["errors"]]])
    return "\n".join(lines) + "\n"


def _load_entrypoint(package_root: Path, relative: str):
    path = (package_root / relative).resolve()
    if package_root.resolve() not in path.parents or not path.is_file() or path.is_symlink():
        raise CommandError("missing_entrypoint", "commands.entrypoint", "Restore the declared package-local runtime entrypoint.")
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(f"guru_runtime_{package_root.name.replace('-', '_')}_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise CommandError("missing_entrypoint", "commands.entrypoint", "Restore the declared package-local runtime entrypoint.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _consume_global_json_flag(argv: list[str]) -> list[str]:
    if argv.count("--json") > 1:
        raise CommandError(
            "conflicting_arguments",
            "arguments.--json",
            "Provide the global JSON output flag at most once.",
        )
    return [value for value in argv if value != "--json"]


def main(package_root: Path, argv: list[str]) -> int:
    try:
        metadata = read_json_file(package_root / "commands.json", "commands.json")
        if metadata.get("package_id") != package_root.name:
            raise CommandError("owner_mismatch", "commands.package_id", "Match package_id and every command owner to the package directory.")
        if not argv:
            raise CommandError("missing_command", "command", "Select one command declared by commands.json.")
        command_id, rest = argv[0], argv[1:]
        matches = [item for item in metadata.get("commands", []) if item.get("id") == command_id]
        if len(matches) != 1:
            raise CommandError("unknown_command", "command", "Select exactly one command declared by commands.json.")
        command = matches[0]
        if command.get("owner") != package_root.name:
            raise CommandError("owner_mismatch", "commands.owner", "Restore the package-local command owner.")
        if "--help" in rest:
            if len(rest) != 1:
                raise CommandError("conflicting_arguments", "arguments", "Use --help by itself.")
            sys.stdout.write(_help(package_root.name, command))
            return 0
        module = _load_entrypoint(package_root, command["entrypoint"])
        result = module.run(package_root, command, _consume_global_json_flag(rest))
        if not isinstance(result, dict):
            raise CommandError("invalid_runtime_output", "stdout", "Return one JSON object from the package entrypoint.")
        write_json(result)
        return 0
    except CommandError as exc:
        return fail(exc)
    except Exception:
        return fail(CommandError("internal_error", "runtime", "Inspect the package runtime and retry."))


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]).resolve(), sys.argv[2:]))
