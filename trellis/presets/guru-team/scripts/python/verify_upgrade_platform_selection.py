#!/usr/bin/env python3
"""Resolve and validate exact platform selections for throwaway upgrades."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_PLATFORMS = ("claude", "codex", "cursor")


class SelectionError(RuntimeError):
    pass


def _load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SelectionError(f"cannot read {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SelectionError(f"{label} must be a JSON object")
    return value


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SelectionError(f"{label} must be an object")
    return value


def _require_selection(value: Any, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item for item in value
    ):
        raise SelectionError(f"{label} must be a non-empty string array")
    selection = tuple(value)
    if len(selection) != len(set(selection)) or selection != tuple(sorted(selection)):
        raise SelectionError(f"{label} must be sorted and unique")
    return selection


def platform_inventory(source_manifest: Mapping[str, Any]) -> tuple[str, ...]:
    extension = source_manifest.get("extension", source_manifest)
    public_api = _require_object(
        _require_object(extension, "extension").get("public_api"),
        "extension.public_api",
    )
    capabilities = _require_object(
        public_api.get("platform_capabilities"),
        "extension.public_api.platform_capabilities",
    )
    rows = capabilities.get("upstream_platforms")
    if not isinstance(rows, list) or not rows:
        raise SelectionError("upstream_platforms must be a non-empty array")
    flags: list[str] = []
    for index, raw in enumerate(rows):
        row = _require_object(raw, f"upstream_platforms[{index}]")
        cli_flag = row.get("cli_flag")
        if not isinstance(cli_flag, str) or not cli_flag:
            raise SelectionError(f"upstream_platforms[{index}].cli_flag is invalid")
        flags.append(cli_flag)
    if len(flags) != len(set(flags)):
        raise SelectionError("upstream platform cli_flag values must be unique")
    if not set(DEFAULT_PLATFORMS).issubset(flags):
        raise SelectionError("upstream inventory does not contain the default platforms")
    return tuple(flags)


def installed_selection(
    installed_manifest: Mapping[str, Any], supported: Sequence[str]
) -> tuple[str, ...]:
    selections = {
        section: _require_selection(
            _require_object(installed_manifest.get(section), section).get(
                "selected_platforms"
            ),
            f"{section}.selected_platforms",
        )
        for section in ("install", "skill_packages", "overlays")
    }
    distinct = set(selections.values())
    if len(distinct) != 1:
        raise SelectionError(
            "installed manifest platform selections disagree: "
            + json.dumps(selections, sort_keys=True)
        )
    selection = next(iter(distinct))
    unknown = sorted(set(selection) - set(supported))
    if unknown:
        raise SelectionError(f"installed manifest selects unknown platforms: {unknown}")
    return selection


def validate_requested_selection(
    requested: Sequence[str], installed: Sequence[str], supported: Sequence[str]
) -> tuple[str, ...]:
    if not requested:
        raise SelectionError("upgrade verification requires repeated --platform flags")
    requested_selection = tuple(requested)
    if len(requested_selection) != len(set(requested_selection)):
        raise SelectionError("repeated --platform values must be unique")
    unknown = sorted(set(requested_selection) - set(supported))
    if unknown:
        raise SelectionError(f"requested unknown platforms: {unknown}")
    if tuple(sorted(requested_selection)) != tuple(installed):
        raise SelectionError(
            "requested --platform values do not match installed manifest selection"
        )
    return tuple(installed)


def platform_args(selection: Sequence[str]) -> list[str]:
    return [part for platform in selection for part in ("--platform", platform)]


def aggregate_results(
    mode: str, selection: Sequence[str], result_paths: Sequence[Path]
) -> dict[str, Any]:
    if len(selection) != len(result_paths):
        raise SelectionError("result count does not match selected platform count")
    results = []
    for platform, path in zip(selection, result_paths):
        payload = _load_object(path, f"{platform} verifier result")
        if payload.get("status") != "passed" or payload.get("mode") != mode:
            raise SelectionError(f"{platform} verifier result did not pass in {mode} mode")
        if payload.get("platform") != platform:
            raise SelectionError(f"{platform} verifier result identity mismatch")
        results.append(payload)
    return {
        "schema_version": "1.0",
        "status": "passed",
        "mode": mode,
        "selected_platforms": list(selection),
        "platform_args": platform_args(selection),
        "results": results,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    inventory = sub.add_parser("inventory-lines")
    inventory.add_argument("--source-manifest", type=Path, required=True)
    validate = sub.add_parser("validate-upgrade")
    validate.add_argument("--source-manifest", type=Path, required=True)
    validate.add_argument("--installed-manifest", type=Path, required=True)
    validate.add_argument("--platform", action="append", default=[])
    aggregate = sub.add_parser("aggregate")
    aggregate.add_argument("--mode", choices=("focused", "existing"), required=True)
    aggregate.add_argument("--platform", action="append", default=[])
    aggregate.add_argument("--result", type=Path, action="append", default=[])
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "inventory-lines":
            source = _load_object(args.source_manifest, "source manifest")
            print("\n".join(platform_inventory(source)))
            return 0
        if args.command == "validate-upgrade":
            source = _load_object(args.source_manifest, "source manifest")
            supported = platform_inventory(source)
            installed = installed_selection(
                _load_object(args.installed_manifest, "installed manifest"), supported
            )
            selection = validate_requested_selection(args.platform, installed, supported)
            result = {
                "schema_version": "1.0",
                "status": "passed",
                "selected_platforms": list(selection),
                "platform_args": platform_args(selection),
            }
        else:
            result = aggregate_results(args.mode, args.platform, args.result)
    except SelectionError as exc:
        print(
            json.dumps(
                {"schema_version": "1.0", "status": "failed", "error": str(exc)},
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
