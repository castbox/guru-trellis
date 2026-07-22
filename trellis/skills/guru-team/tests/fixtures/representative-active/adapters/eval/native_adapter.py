#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any


ADAPTERS = ("shared", "codex", "claude", "cursor")

TRACE_HELPER = r'''#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def stdout_digest(value: str) -> str:
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        normalized = value.strip()
    else:
        normalized = json.dumps(payload, separators=(",", ":"))
    return digest(normalized.encode("utf-8"))


def append_event(
    trace_path: Path,
    request_sha256: str,
    projection_root: str,
    skill_sha256: str,
    wrapper_sha256: str,
    event: dict[str, object],
) -> None:
    if trace_path.exists():
        payload = json.loads(trace_path.read_text(encoding="utf-8"))
    else:
        payload = {
            "schema_version": "1.0",
            "request_sha256": request_sha256,
            "projection_root": projection_root,
            "skill_sha256": skill_sha256,
            "wrapper_sha256": wrapper_sha256,
            "events": [],
        }
    if (
        payload.get("request_sha256") != request_sha256
        or payload.get("projection_root") != projection_root
        or payload.get("skill_sha256") != skill_sha256
        or payload.get("wrapper_sha256") != wrapper_sha256
        or not isinstance(payload.get("events"), list)
    ):
        raise ValueError("native trace request binding mismatch")
    event["request_sha256"] = request_sha256
    payload["events"].append(event)
    trace_path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", required=True)
    parser.add_argument("--request-sha256", required=True)
    parser.add_argument("--projection-root", required=True)
    parser.add_argument("--skill-sha256", required=True)
    parser.add_argument("--wrapper-sha256", required=True)
    subparsers = parser.add_subparsers(dest="operation", required=True)
    read_parser = subparsers.add_parser("read")
    read_parser.add_argument("--kind", required=True, choices=("skill_contract", "case_file"))
    read_parser.add_argument("--path", required=True)
    invoke_parser = subparsers.add_parser("invoke")
    invoke_parser.add_argument("--wrapper", required=True)
    invoke_parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    trace_path = Path(args.trace).resolve()
    if args.operation == "read":
        target = Path(args.path).resolve()
        content = target.read_bytes()
        append_event(trace_path, args.request_sha256, args.projection_root, args.skill_sha256, args.wrapper_sha256, {
            "kind": "read", "target_kind": args.kind, "path": str(target), "sha256": digest(content),
        })
        sys.stdout.buffer.write(content)
        return 0
    wrapper = Path(args.wrapper).resolve()
    forwarded = list(args.arguments)
    if forwarded and forwarded[0] == "--":
        forwarded = forwarded[1:]
    process = subprocess.run(
        [str(wrapper), *forwarded], text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    append_event(trace_path, args.request_sha256, args.projection_root, args.skill_sha256, args.wrapper_sha256, {
        "kind": "invoke", "wrapper_path": str(wrapper), "argv": [str(wrapper), *forwarded],
        "returncode": process.returncode, "stdout_sha256": stdout_digest(process.stdout),
        "stderr_sha256": digest(process.stderr.encode("utf-8")),
    })
    sys.stdout.write(process.stdout)
    sys.stderr.write(process.stderr)
    return process.returncode


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
'''


def emit(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, separators=(",", ":")))
    return 0


def response(
    request: dict[str, Any],
    status: str,
    transcript: Path,
    *,
    stdout: str = "",
    stderr: str = "",
    trace_events: list[str] | None = None,
    timing_ms: int = 0,
    native_trace: Path | None = None,
) -> dict[str, Any]:
    try:
        corpus_sha256 = hashlib.sha256(Path(request["corpus_path"]).read_bytes()).hexdigest()
    except (KeyError, OSError, TypeError):
        corpus_sha256 = str(request.get("corpus_sha256") or "0" * 64)
    return {
        "schema_version": "1.0",
        "capability_status": status,
        "corpus_sha256": corpus_sha256,
        "public_stdout": stdout,
        "public_stderr": stderr,
        "trace_events": trace_events or [],
        "transcript_locator": str(transcript),
        "native_trace_locator": str(native_trace or transcript.with_name("native-trace.json")),
        "timing_ms": timing_ms,
    }


def public_projection_assets(interface: dict[str, Any]) -> set[Path]:
    assets = {Path("SKILL.md"), Path("interface.json")}
    contracts = interface.get("public_contracts")
    if not isinstance(contracts, dict):
        raise ValueError("public Interface contracts are unavailable")

    def add_reference(reference: Any) -> None:
        if not isinstance(reference, dict):
            return
        value = reference.get("path")
        if not isinstance(value, str):
            return
        relative = Path(value)
        if relative.is_absolute() or not relative.parts or ".." in relative.parts:
            raise ValueError("public Interface contains an unsafe asset path")
        assets.add(relative)

    public_input = contracts.get("input")
    if isinstance(public_input, dict):
        add_reference(public_input.get("aggregate_schema"))
        for profile in public_input.get("profiles", []):
            if isinstance(profile, dict):
                add_reference(profile.get("schema"))
                add_reference(profile.get("example"))
    invocation = contracts.get("invocation")
    if not isinstance(invocation, dict):
        raise ValueError("public invocation contract is unavailable")
    wrapper = invocation.get("wrapper")
    if not isinstance(wrapper, str):
        raise ValueError("public wrapper locator is unavailable")
    wrapper_path = Path(wrapper)
    if wrapper_path.is_absolute() or not wrapper_path.parts or ".." in wrapper_path.parts:
        raise ValueError("public wrapper locator is unsafe")
    assets.add(wrapper_path)
    add_reference(invocation.get("error_schema"))
    add_reference(invocation.get("error_example"))
    for output in contracts.get("outputs", []):
        if isinstance(output, dict):
            add_reference(output.get("schema"))
            add_reference(output.get("example"))
    return assets


def stage_public_projection(request: dict[str, Any], execution_root: Path) -> tuple[Path, Path, Path, str, str]:
    canonical_root = Path(request["package_root"]).resolve()
    interface = json.loads((canonical_root / "interface.json").read_text(encoding="utf-8"))
    if not isinstance(interface, dict) or interface.get("id") != request.get("skill_id"):
        raise ValueError("exact public Interface identity is unavailable")
    projection_root = execution_root / "public-packages" / str(request["skill_id"])
    projection_root.mkdir(parents=True, exist_ok=False)
    for relative in sorted(public_projection_assets(interface), key=lambda item: item.as_posix()):
        source = canonical_root / relative
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"public projection asset is unavailable: {relative.as_posix()}")
        destination = projection_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    if (projection_root / "evals").exists() or any(path.name == "guru_team_trellis.py" for path in projection_root.rglob("*")):
        raise ValueError("public projection contains eval or private runtime assets")
    local_invocation = interface.get("public_contracts", {}).get("invocation")
    request_interface = request.get("interface")
    request_invocation = request_interface.get("public_invocation") if isinstance(request_interface, dict) else None
    if not isinstance(local_invocation, dict) or request_invocation != local_invocation:
        raise ValueError("side-local public invocation contract does not match exact package Interface")
    wrapper_relative = local_invocation["wrapper"]
    wrapper_path = projection_root / wrapper_relative
    skill_path = projection_root / "SKILL.md"
    skill_sha256 = hashlib.sha256(skill_path.read_bytes()).hexdigest()
    wrapper_sha256 = hashlib.sha256(wrapper_path.read_bytes()).hexdigest()
    if skill_sha256 != hashlib.sha256((canonical_root / "SKILL.md").read_bytes()).hexdigest():
        raise ValueError("public projection Skill bytes differ from canonical bytes")
    if wrapper_sha256 != hashlib.sha256((canonical_root / wrapper_relative).read_bytes()).hexdigest():
        raise ValueError("public projection wrapper bytes differ from canonical bytes")
    return projection_root, skill_path, wrapper_path, skill_sha256, wrapper_sha256


def public_runtime_target(request: dict[str, Any]) -> Path:
    target = request.get("runtime_target")
    if not isinstance(target, str) or not target:
        raise ValueError("public invocation runtime boundary is unavailable")
    candidate = Path(target)
    if not candidate.is_absolute() or candidate.is_symlink():
        raise ValueError("public invocation runtime boundary target is unsafe")
    resolved = Path(os.path.abspath(candidate))
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise ValueError("public invocation runtime boundary target is unavailable")
    return resolved


def start_public_runtime_boundary(
    execution_root: Path,
    target: Path,
    package_root: Path,
    projection_root: Path,
) -> tuple[Path, threading.Thread, threading.Event]:
    request_path = execution_root / "public-invocation-request.json"
    response_path = execution_root / "public-invocation-response.json"
    request_path.unlink(missing_ok=True)
    response_path.unlink(missing_ok=True)
    stop = threading.Event()

    def serve() -> None:
        try:
            while not request_path.is_file():
                if stop.wait(0.01):
                    return
            try:
                request = json.loads(request_path.read_text(encoding="utf-8"))
                arguments = request["arguments"]
                if not isinstance(arguments, list) or any(not isinstance(item, str) for item in arguments):
                    raise ValueError("invalid public invocation arguments")
                if arguments[:2] != ["--package-root", str(projection_root)]:
                    raise ValueError("public invocation package projection binding is invalid")
                arguments = ["--package-root", str(package_root), *arguments[2:]]
                process = subprocess.run(
                    [str(target), *arguments],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                response_payload = {
                    "returncode": process.returncode,
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                }
            except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
                response_payload = {"returncode": 2, "stdout": "", "stderr": str(exc)}
            response_path.write_text(
                json.dumps(response_payload, separators=(",", ":")), encoding="utf-8",
            )
            while request_path.exists() or response_path.exists():
                if stop.wait(0.01):
                    return
        finally:
            if stop.is_set():
                try:
                    request_path.unlink(missing_ok=True)
                    response_path.unlink(missing_ok=True)
                except OSError:
                    pass

    thread = threading.Thread(target=serve, name="guru-eval-public-invocation", daemon=True)
    thread.start()
    boundary = execution_root / "public-invocation-boundary.sh"
    boundary.write_text(
        "#!/usr/bin/env python3\n"
        "import json,sys,time\n"
        "from pathlib import Path\n"
        f"request_path=Path({str(request_path)!r}); response_path=Path({str(response_path)!r})\n"
        "request_path.write_text(json.dumps({'arguments':sys.argv[1:]},separators=(',',':')),encoding='utf-8')\n"
        "for _ in range(3000):\n"
        " if response_path.is_file(): break\n"
        " time.sleep(0.01)\n"
        "else: raise SystemExit('public invocation response timed out')\n"
        "result=json.loads(response_path.read_text(encoding='utf-8')); request_path.unlink(missing_ok=True); response_path.unlink(missing_ok=True)\n"
        "sys.stdout.write(result['stdout']); sys.stderr.write(result['stderr'])\n"
        "raise SystemExit(result['returncode'])\n",
        encoding="utf-8",
    )
    boundary.chmod(0o755)
    return boundary, thread, stop


def build_context(
    request: dict[str, Any],
) -> tuple[str, Path, Path, Path, Path, Path, str, Path, threading.Thread, threading.Event]:
    workdir = Path(request["workdir"]).resolve()
    execution_root = workdir.parent
    projection_root, skill_path, wrapper_path, skill_sha256, wrapper_sha256 = stage_public_projection(request, execution_root)
    runtime_target = public_runtime_target(request)
    trace_path = execution_root / "native-trace.json"
    helper_path = execution_root / "native-trace-helper.py"
    helper_path.write_text(TRACE_HELPER, encoding="utf-8")
    helper_path.chmod(0o755)
    file_sections: list[str] = []
    for relative in request["files"]:
        staged = workdir / relative
        if not staged.is_file():
            raise ValueError("staged case file is unavailable")
        try:
            content = staged.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = f"<binary sha256={hashlib.sha256(staged.read_bytes()).hexdigest()}>"
        file_sections.append(f"### {relative}\n{content}")
    context = "\n".join([
        "Execute exactly one Guru Team Skill behavior eval.",
        f"Skill id: {request['skill_id']}",
        f"Exact public Skill projection: {projection_root}",
        f"Public wrapper: {wrapper_path}",
        f"Isolated workdir: {workdir}",
        f"Native trace helper: {helper_path}",
        f"Native trace receipt: {trace_path}",
        "The projection is the complete execution-visible package. Paths absent from it are outside the native execution contract.",
        "All Skill/runtime file reads and the public invocation must use the trace helper. Direct reads or direct wrapper execution are unsupported.",
        "First read the exact Skill contract with the helper's read operation, then invoke the exact public wrapper with its invoke operation.",
        "Return only the wrapper's single typed-exit JSON object, with no Markdown fence or explanation.",
        f"Case prompt:\n{request['prompt']}",
        f"Public invocation contract:\n{json.dumps(request['interface']['public_invocation'], separators=(',', ':'))}",
        "Staged case files:\n" + ("\n".join(file_sections) if file_sections else "<none>"),
        "The adapter has already completed any declared owner staging and checker validation in the installed fixture.",
        "Use the exact public_invocation.arguments from the staged case facts; do not recreate or rewrite public input, owner result, or owner plan files.",
        "For this post-owner invocation boundary, run only the exact Skill read command above and then the exact wrapper invocation command above. Do not read linked references, Interface assets, examples, wrapper source, or any other file.",
    ])
    native_request = {
        "schema_version": "1.0",
        "skill_id": request["skill_id"],
        "case_id": request["case_id"],
        "prompt": request["prompt"],
        "files": request["files"],
        "workdir": str(workdir),
        "public_package_root": str(projection_root),
        "public_invocation": request["interface"]["public_invocation"],
    }
    native_request_path = execution_root / "native-request.json"
    native_request_path.write_text(json.dumps(native_request, separators=(",", ":")), encoding="utf-8")
    request_sha256 = hashlib.sha256(native_request_path.read_bytes()).hexdigest()
    helper_arguments = (
        f"--trace {trace_path} --request-sha256 {request_sha256} --projection-root {projection_root} "
        f"--skill-sha256 {skill_sha256} --wrapper-sha256 {wrapper_sha256}"
    )
    context = context.replace(
        "First read the exact Skill contract with the helper's read operation, then invoke the exact public wrapper with its invoke operation.",
        f"First read the exact Skill contract with: {helper_path} {helper_arguments} read --kind skill_contract --path {skill_path}\n"
        f"Then invoke the exact public wrapper with: {helper_path} {helper_arguments} invoke --wrapper {wrapper_path} -- <declared wrapper arguments>",
    )
    context_path = execution_root / "native-context.txt"
    context_path.write_text(context, encoding="utf-8")
    protocol_path = execution_root / "native-protocol.json"
    protocol_path.write_text(json.dumps({
        "schema_version": "1.0", "native_request_path": str(native_request_path),
        "request_sha256": request_sha256, "helper_path": str(helper_path),
        "trace_path": str(trace_path), "skill_path": str(skill_path),
        "wrapper_path": str(wrapper_path), "projection_root": str(projection_root),
        "skill_sha256": skill_sha256, "wrapper_sha256": wrapper_sha256,
    }, separators=(",", ":")), encoding="utf-8")
    runtime_repo_root = runtime_target.parents[4]
    installed_package_root = (
        runtime_repo_root / ".trellis/guru-team/skills/packages" / str(request["skill_id"])
    )
    runtime_package_root = (
        installed_package_root
        if installed_package_root.is_dir() and not installed_package_root.is_symlink()
        else projection_root
    )
    boundary_path, boundary_thread, boundary_stop = start_public_runtime_boundary(
        execution_root, runtime_target, runtime_package_root, projection_root
    )
    return (
        context, context_path, wrapper_path, trace_path, protocol_path,
        native_request_path, request_sha256, boundary_path, boundary_thread,
        boundary_stop,
    )


def validate_native_trace(
    trace_path: Path,
    request_sha256: str,
    request: dict[str, Any],
    wrapper_path: Path,
    public_stdout: str,
    protocol_path: Path,
) -> list[str]:
    try:
        payload = json.loads(trace_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise ValueError("native trace receipt is missing or malformed")
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    expected_top = {"schema_version", "request_sha256", "projection_root", "skill_sha256", "wrapper_sha256", "events"}
    if set(payload) != expected_top or payload.get("schema_version") != "1.0" or payload.get("request_sha256") != request_sha256:
        raise ValueError("native trace receipt request binding is invalid")
    events = payload.get("events")
    if not isinstance(events, list) or len(events) < 2:
        raise ValueError("native trace receipt is incomplete")
    projection_root = Path(protocol["projection_root"]).resolve()
    skill_path = Path(protocol["skill_path"]).resolve()
    if (
        payload.get("projection_root") != str(projection_root)
        or payload.get("skill_sha256") != protocol.get("skill_sha256")
        or payload.get("wrapper_sha256") != protocol.get("wrapper_sha256")
        or (projection_root / "evals").exists()
        or any(path.name == "guru_team_trellis.py" for path in projection_root.rglob("*"))
    ):
        raise ValueError("native trace public projection binding is invalid")
    workdir = Path(request["workdir"]).resolve()
    allowed_reads = {skill_path, *(workdir / relative for relative in request["files"])}
    skill_reads = []
    invocations = []
    for event in events:
        if not isinstance(event, dict) or event.get("request_sha256") != request_sha256:
            raise ValueError("native trace event binding is invalid")
        if event.get("kind") == "read":
            if set(event) != {"kind", "target_kind", "path", "sha256", "request_sha256"}:
                raise ValueError("native read trace shape is invalid")
            target = Path(str(event.get("path"))).resolve()
            if target not in allowed_reads:
                raise ValueError("native trace contains an undeclared file read")
            try:
                expected_sha256 = hashlib.sha256(target.read_bytes()).hexdigest()
            except OSError:
                raise ValueError("native trace read target is unavailable")
            if event.get("sha256") != expected_sha256:
                raise ValueError("native trace read digest mismatch")
            if target == skill_path and event.get("target_kind") == "skill_contract":
                skill_reads.append(event)
        elif event.get("kind") == "invoke":
            if set(event) != {"kind", "wrapper_path", "argv", "returncode", "stdout_sha256", "stderr_sha256", "request_sha256"}:
                raise ValueError("native invocation trace shape is invalid")
            invocations.append(event)
        else:
            raise ValueError("native trace event kind is invalid")
    if len(skill_reads) != 1 or events.index(skill_reads[0]) != 0:
        raise ValueError("native trace must begin with one exact Skill read")
    if len(invocations) != 1 or events.index(invocations[0]) != len(events) - 1:
        raise ValueError("native trace must end with one public wrapper invocation")
    invocation = invocations[0]
    argv = invocation.get("argv")
    if (
        Path(str(invocation.get("wrapper_path"))).resolve() != wrapper_path.resolve()
        or not isinstance(argv, list) or not argv
        or Path(str(argv[0])).resolve() != wrapper_path.resolve()
        or any(not isinstance(item, str) for item in argv)
        or invocation.get("returncode") != 0
        or invocation.get("stdout_sha256") != hashlib.sha256(public_stdout.encode("utf-8")).hexdigest()
        or not isinstance(invocation.get("stderr_sha256"), str)
        or len(invocation["stderr_sha256"]) != 64
    ):
        raise ValueError("native public wrapper invocation receipt is invalid")
    return ["public_invocation", "evals_not_loaded", "private_runtime_not_read"]


def native_argv(
    adapter: str,
    command: str,
    request: dict[str, Any],
    context: str,
    context_path: Path,
    native_request_path: Path,
    projection_root: Path,
) -> tuple[list[str], Path | None]:
    workdir = str(Path(request["workdir"]).resolve())
    if adapter == "shared":
        return [command, "--request", str(native_request_path), "--context", str(context_path), "--workdir", workdir], None
    if adapter == "codex":
        output_path = native_request_path.with_name("native-last-message.txt")
        trusted_root = str(Path(request["runtime_target"]).resolve().parents[4])
        return [
            command, "exec", "--ephemeral", "--ignore-user-config", "--sandbox", "workspace-write",
            "--cd", trusted_root, "--add-dir", workdir, "--add-dir", str(projection_root),
            "--output-last-message", str(output_path), context,
        ], output_path
    if adapter == "claude":
        return [
            command, "--print", "--safe-mode", "--output-format", "json", "--no-session-persistence",
            "--permission-mode", "dontAsk", "--add-dir", str(projection_root),
        ], None
    return [command, "--print", "--output-format", "json", context], None


def unwrap_native_output(adapter: str, stdout: str, output_path: Path | None) -> str:
    value = output_path.read_text(encoding="utf-8") if output_path and output_path.is_file() else stdout
    if adapter in {"claude", "cursor"}:
        try:
            payload = json.loads(value)
        except json.JSONDecodeError:
            payload = None
        if isinstance(payload, dict) and isinstance(payload.get("result"), str):
            value = payload["result"]
    value = value.strip()
    if value.startswith("```") and value.endswith("```"):
        lines = value.splitlines()
        value = "\n".join(lines[1:-1]).strip()
    payload = json.loads(value)
    if not isinstance(payload, dict):
        raise ValueError("native output is not one typed JSON object")
    return json.dumps(payload, separators=(",", ":"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", required=True, choices=ADAPTERS)
    parser.add_argument("--native-command", required=True)
    parser.add_argument("--request", required=True)
    args = parser.parse_args()
    request_path = Path(args.request).resolve()
    transcript = request_path.parent / "adapter-transcript.json"
    try:
        request = json.loads(request_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        fallback = {"corpus_sha256": "0" * 64}
        transcript.write_text(json.dumps({"adapter": args.adapter, "error": str(exc)}), encoding="utf-8")
        return emit(response(fallback, "execution_error", transcript, stderr="adapter request/context invalid"))
    packaged_native = Path(__file__).resolve().parent / args.native_command
    native = (
        str(packaged_native)
        if args.adapter == "shared" and packaged_native.is_file() and os.access(packaged_native, os.X_OK)
        else shutil.which(args.native_command)
    )
    if native is None:
        transcript.write_text(json.dumps({"adapter": args.adapter, "native_command": args.native_command, "status": "unsupported"}), encoding="utf-8")
        return emit(response(request, "unsupported", transcript, native_trace=Path(request["workdir"]).resolve().parent / "native-trace.json"))
    if args.adapter == "cursor":
        status = subprocess.run(
            [native, "status"], text=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False,
        )
        status_text = f"{status.stdout}\n{status.stderr}".lower()
        if status.returncode != 0 or any(
            marker in status_text
            for marker in ("not logged in", "not authenticated", "unauthenticated", "login required")
        ):
            transcript.write_text(json.dumps({
                "adapter": args.adapter, "native_command": args.native_command,
                "status": "unsupported", "reason": "authentication unavailable",
            }), encoding="utf-8")
            return emit(response(
                request, "unsupported", transcript,
                native_trace=Path(request["workdir"]).resolve().parent / "native-trace.json",
            ))
    try:
        (
            context, context_path, wrapper_path, trace_path, protocol_path,
            native_request_path, request_sha256, boundary_path,
            boundary_thread, boundary_stop,
        ) = build_context(request)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        transcript.write_text(json.dumps({"adapter": args.adapter, "error": str(exc)}), encoding="utf-8")
        return emit(response(request, "execution_error", transcript, stderr="adapter request/context invalid"))
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    projection_root = Path(protocol["projection_root"])
    argv, output_path = native_argv(args.adapter, native, request, context, context_path, native_request_path, projection_root)
    native_environment = dict(os.environ)
    native_environment.pop("GURU_TEAM_FAKE_NATIVE_DISPATCHER", None)
    native_environment.pop("OLDPWD", None)
    native_environment["PWD"] = str(Path(request["workdir"]).resolve().parent)
    native_environment["GURU_TEAM_DISPATCHER"] = str(boundary_path)
    native_environment["GURU_TEAM_NATIVE_REQUEST"] = str(native_request_path)
    native_environment["GURU_TEAM_NATIVE_PROTOCOL"] = str(protocol_path)
    started = time.monotonic_ns()
    process = subprocess.run(
        argv,
        cwd=Path(request["workdir"]).resolve().parent,
        input=context if args.adapter == "claude" else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=native_environment,
    )
    boundary_stop.set()
    boundary_thread.join(timeout=1)
    timing_ms = max(0, (time.monotonic_ns() - started) // 1_000_000)
    transcript.write_text(json.dumps({
        "adapter": args.adapter,
        "native_command": args.native_command,
        "argv": argv,
        "context_path": str(context_path),
        "protocol_path": str(protocol_path),
        "native_trace_path": str(trace_path),
        "native_request_path": str(native_request_path),
        "projection_root": str(projection_root),
        "wrapper_path": str(wrapper_path),
        "returncode": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
    }, indent=2), encoding="utf-8")
    if process.returncode != 0:
        return emit(response(request, "execution_error", transcript, stderr=process.stderr, timing_ms=timing_ms, native_trace=trace_path))
    try:
        public_stdout = unwrap_native_output(args.adapter, process.stdout, output_path)
        trace_events = validate_native_trace(trace_path, request_sha256, request, wrapper_path, public_stdout, protocol_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return emit(response(request, "execution_error", transcript, stderr=str(exc), timing_ms=timing_ms, native_trace=trace_path))
    return emit(response(
        request,
        "executed",
        transcript,
        stdout=public_stdout,
        stderr=process.stderr,
        trace_events=trace_events,
        timing_ms=timing_ms,
        native_trace=trace_path,
    ))


if __name__ == "__main__":
    raise SystemExit(main())
