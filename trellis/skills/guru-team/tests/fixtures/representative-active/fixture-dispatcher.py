#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def fail(code: str, field_path: str, remediation: str) -> int:
    print(json.dumps({
        "code": code,
        "field_path": field_path,
        "remediation": remediation,
    }, separators=(",", ":")), file=sys.stderr)
    return 2


def option(arguments: list[str], flag: str) -> str | None:
    try:
        index = arguments.index(flag)
    except ValueError:
        return None
    return arguments[index + 1] if index + 1 < len(arguments) else None


def main() -> int:
    arguments = sys.argv[1:]
    package_value = option(arguments, "--package-root")
    if package_value is None:
        return fail("missing_package_root", "invocation.package_root", "Use the package wrapper instead of calling the fixture dispatcher directly.")
    package = Path(package_value)
    try:
        forwarded = arguments[arguments.index("--") + 1:]
    except ValueError:
        forwarded = []

    if package.name == "guru-example-action":
        input_value = option(forwarded, "--input")
        if input_value is None:
            return fail("missing_argument", "arguments.input", "Provide --input with a package-relative JSON example path.")
        input_path = Path(input_value)
        if input_path.is_absolute() or ".." in input_path.parts:
            return fail("invalid_path", "arguments.input", "Use a safe package-relative input path.")
        try:
            payload = json.loads((package / input_path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return fail("invalid_input", "arguments.input", "Provide a readable JSON object from the package.")
        if not isinstance(payload, dict):
            return fail("invalid_input", "input", "Provide a JSON object matching a declared profile.")
        profile = payload.get("profile")
        topic = payload.get("topic")
        if profile not in {"initial", "reentry"}:
            return fail("unknown_profile", "input.profile", "Use the initial or reentry profile.")
        if not isinstance(topic, str) or not topic:
            return fail("invalid_input", "input.topic", "Provide a non-empty topic.")
        if profile == "reentry":
            result = {"exit_id": "repeat", "profile": "reentry", "next_topic": topic}
        elif payload.get("mode") == "forward":
            result = {"exit_id": "forwarded", "forwarded_item": topic}
        elif payload.get("mode") == "block":
            result = {"exit_id": "blocked"}
        elif payload.get("mode") == "complete":
            result = {"exit_id": "completed", "result": f"{topic} complete"}
        else:
            return fail("invalid_input", "input.mode", "Use complete, forward, or block for the initial profile.")
    elif package.name == "guru-example-sync":
        exit_id = option(forwarded, "--exit-id")
        item = option(forwarded, "--item")
        if exit_id != "forwarded":
            return fail("invalid_argument", "arguments.exit_id", "Use --exit-id forwarded for the representative sync invocation.")
        if not item:
            return fail("missing_argument", "arguments.item", "Provide --item with a non-empty value.")
        result = {"exit_id": "synced", "item": item}
    else:
        return fail("unknown_skill", "invocation.package_root", "Invoke a declared representative fixture package.")
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
