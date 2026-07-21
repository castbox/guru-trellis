#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def option(arguments: list[str], *flags: str) -> str | None:
    for flag in flags:
        try:
            index = arguments.index(flag)
        except ValueError:
            continue
        return arguments[index + 1] if index + 1 < len(arguments) else None
    return None


def request_path(arguments: list[str]) -> Path:
    injected = os.environ.get("GURU_TEAM_NATIVE_REQUEST")
    if injected:
        return Path(injected)
    direct = option(arguments, "--request")
    if direct:
        return Path(direct)
    output = option(arguments, "--output-last-message")
    if output:
        return Path(output).parent / "adapter-request.json"
    return Path.cwd() / "adapter-request.json"


def public_invocation(
    request: dict[str, object],
    protocol: dict[str, object],
) -> subprocess.CompletedProcess[str]:
    package = Path(str(request["public_package_root"]))
    prompt = str(request["prompt"])
    helper = str(protocol["helper_path"])
    trace = str(protocol["trace_path"])
    request_sha256 = str(protocol["request_sha256"])
    skill = str(protocol["skill_path"])
    wrapper = str(protocol["wrapper_path"])
    skill_read = subprocess.run(
        [sys.executable, helper, "--trace", trace, "--request-sha256", request_sha256,
         "--projection-root", str(protocol["projection_root"]),
         "--skill-sha256", str(protocol["skill_sha256"]),
         "--wrapper-sha256", str(protocol["wrapper_sha256"]),
         "read", "--kind", "skill_contract", "--path", skill],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if skill_read.returncode != 0:
        return skill_read
    direct_read = os.environ.get("GURU_TEAM_FAKE_NATIVE_DIRECT_READ")
    if direct_read:
        targets = []
        if direct_read in {"evals", "both"}:
            targets.append(package / "evals/evals.json")
        if direct_read in {"private_runtime", "both"}:
            targets.append(package / "runtime/guru_team_trellis.py")
        denied: list[str] = []
        for target in targets:
            try:
                target.read_bytes()
            except OSError as exc:
                denied.append(str(exc))
                print(json.dumps({
                    "code": "native_projection_access_denied",
                    "path": str(target),
                    "error": type(exc).__name__,
                }, separators=(",", ":")), file=sys.stderr)
        if denied:
            return subprocess.CompletedProcess([str(package)], 9, "", "\n".join(denied))
        return subprocess.CompletedProcess([str(package)], 10, "", "execution projection unexpectedly exposed a forbidden asset")
    if str(request["skill_id"]) == "guru-example-action":
        if "Repeat" in prompt:
            forwarded = ["--input", "examples/action-reentry-input.json"]
        elif "Block" in prompt:
            generated = package / "examples/native-block-input.json"
            generated.write_text(
                json.dumps({"profile": "initial", "topic": "blocked example", "mode": "block"}),
                encoding="utf-8",
            )
            forwarded = ["--input", "examples/native-block-input.json"]
        else:
            forwarded = ["--input", "examples/action-initial-input.json"]
    elif str(request["skill_id"]) == "guru-example-sync":
        exit_id = "blocked" if "blocked" in prompt else "forwarded"
        forwarded = ["--exit-id", exit_id, "--item", "alpha"]
    else:
        raise ValueError("unknown fixture package")
    environment = dict(os.environ)
    environment["GURU_TEAM_DISPATCHER"] = os.environ.get("GURU_TEAM_DISPATCHER") or os.environ.get(
        "GURU_TEAM_FAKE_NATIVE_DISPATCHER", str(package.parents[1] / "fixture-dispatcher.py")
    )
    return subprocess.run(
        [sys.executable, helper, "--trace", trace, "--request-sha256", request_sha256,
         "--projection-root", str(protocol["projection_root"]),
         "--skill-sha256", str(protocol["skill_sha256"]),
         "--wrapper-sha256", str(protocol["wrapper_sha256"]),
         "invoke", "--wrapper", wrapper, "--", *forwarded],
        cwd=package,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def main() -> int:
    arguments = sys.argv[1:]
    request_file = request_path(arguments)
    request = json.loads(request_file.read_text(encoding="utf-8"))
    protocol_path = Path(os.environ.get("GURU_TEAM_NATIVE_PROTOCOL", str(request_file.parent / "native-protocol.json")))
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    result = public_invocation(request, protocol)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode
    command = Path(sys.argv[0]).name
    if command == "codex":
        output = option(arguments, "--output-last-message")
        if output is None:
            return 2
        Path(output).write_text(result.stdout, encoding="utf-8")
        print(json.dumps({"type": "turn.completed"}))
    elif command in {"claude", "cursor-agent"}:
        print(json.dumps({"result": result.stdout}))
    else:
        print(result.stdout, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
