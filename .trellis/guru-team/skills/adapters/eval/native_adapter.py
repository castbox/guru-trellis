from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import hashlib
import json
import os
import select
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time

# The CLI is also executed directly by the platform shell adapters.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from adapters.eval.eval_constants import (
    ADAPTERS,
    MANAGED_PYTHON_SHEBANG,
    OWNER_INVOCATION,
    OWNER_RESULT,
    QUALIFICATION_MODEL,
    QUALIFICATION_PUBLIC_AUTHORING_FACTS,
    QUALIFICATION_SKILL,
    TRACE_HELPER,
)

from adapters.eval.eval_support import (
    canonical_permission_paths,
    emit,
    external_codex_home,
    minimal_native_environment,
    model_projection_copy,
    public_runtime_target,
    qualification_model_request,
    qualification_prompt_sha256,
    qualification_public_repository_identity,
    qualification_trace_helper_source,
    recorded_native_environment,
    repository_file_inventory,
    response,
    run_codex_permission_probe,
    stage_public_projection,
    stage_repository_projection,
    write_codex_permission_profile,
)

from adapters.eval.owner_staging import (
    stage_owner_execution,
)


def start_public_runtime_boundary(
    execution_root: Path,
    target: Path,
    package_root: Path,
    projection_root: Path,
    wrapper_path: Path,
    runtime_environment: dict[str, str],
) -> tuple[Path, threading.Thread, threading.Event]:
    request_path = execution_root / "public-invocation-request.json"
    response_path = execution_root / "public-invocation-response.json"
    response_draft_path = execution_root / "public-invocation-response.pending.json"
    request_path.unlink(missing_ok=True)
    response_path.unlink(missing_ok=True)
    response_draft_path.unlink(missing_ok=True)
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
                projection_wrapper = Path(str(request.get("wrapper_path") or ""))
                try:
                    wrapper_relative = projection_wrapper.relative_to(projection_root)
                except ValueError as exc:
                    raise ValueError("public invocation wrapper binding is invalid") from exc
                installed_wrapper = package_root / wrapper_relative
                if installed_wrapper.is_symlink() or not os.access(installed_wrapper, os.X_OK):
                    raise ValueError("installed public invocation wrapper is unavailable")
                arguments = arguments[2:]
                stdin_text = None
                if "--invocation" in arguments:
                    invocation_index = arguments.index("--invocation")
                    if (
                        invocation_index + 1 < len(arguments)
                        and arguments[invocation_index + 1] == "-"
                    ):
                        invocation_path = target.parents[4] / OWNER_INVOCATION
                        if invocation_path.is_symlink() or not invocation_path.is_file():
                            raise ValueError("stdin invocation envelope is unavailable or unsafe")
                        stdin_text = invocation_path.read_text(encoding="utf-8")
                elif "--owner-result" in arguments:
                    owner_index = arguments.index("--owner-result")
                    if (
                        owner_index + 1 < len(arguments)
                        and arguments[owner_index + 1] == "-"
                    ):
                        owner_path = target.parents[4] / OWNER_RESULT
                        if owner_path.is_symlink() or not owner_path.is_file():
                            raise ValueError("stdin owner result is unavailable or unsafe")
                        stdin_text = owner_path.read_text(encoding="utf-8")
                process = subprocess.run(
                    [str(installed_wrapper), *arguments],
                    cwd=target.parents[4],
                    text=True,
                    input=stdin_text,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                    env={**os.environ, **runtime_environment},
                )
                response_payload = {
                    "returncode": process.returncode,
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                }
            except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
                response_payload = {"returncode": 2, "stdout": "", "stderr": str(exc)}
            response_draft_path.write_text(
                json.dumps(response_payload, separators=(",", ":")), encoding="utf-8",
            )
            response_draft_path.replace(response_path)
            while request_path.exists() or response_path.exists():
                if stop.wait(0.01):
                    return
        finally:
            if stop.is_set():
                try:
                    request_path.unlink(missing_ok=True)
                    response_path.unlink(missing_ok=True)
                    response_draft_path.unlink(missing_ok=True)
                except OSError:
                    pass

    thread = threading.Thread(target=serve, name="guru-eval-public-invocation", daemon=True)
    thread.start()
    boundary = execution_root / "public-invocation-boundary.sh"
    boundary.write_text(
        MANAGED_PYTHON_SHEBANG
        +
        "import json,sys,time\n"
        "from pathlib import Path\n"
        f"request_path=Path({str(request_path)!r}); response_path=Path({str(response_path)!r})\n"
        f"request_path.write_text(json.dumps({{'arguments':sys.argv[1:],'wrapper_path':{str(wrapper_path)!r}}},separators=(',',':')),encoding='utf-8')\n"
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

def start_qualification_runtime_boundary(
    request_fifo: Path,
    response_fifo: Path,
    stop: threading.Event,
    owner_repository: Path,
    package_root: Path,
    runtime_environment: dict[str, str],
    public_input_binding: dict[str, str],
) -> threading.Thread:
    installed_wrapper = package_root / "scripts/invoke.sh"
    if installed_wrapper.is_symlink() or not os.access(installed_wrapper, os.X_OK):
        raise ValueError("installed qualification public invocation wrapper is unavailable")
    for fifo in (request_fifo, response_fifo):
        if fifo.exists():
            fifo.unlink()
        os.mkfifo(fifo, mode=0o600)

    def serve() -> None:
        descriptor = os.open(request_fifo, os.O_RDONLY | os.O_NONBLOCK)
        try:
            chunks: list[bytes] = []
            while not stop.is_set():
                readable, _, _ = select.select([descriptor], [], [], 0.1)
                if not readable:
                    continue
                chunk = os.read(descriptor, 65536)
                if chunk:
                    chunks.append(chunk)
                    continue
                if not chunks:
                    continue
                try:
                    payload = json.loads(b"".join(chunks))
                    if (
                        not isinstance(payload, dict)
                        or payload.get("arguments") != ["--invocation", "-"]
                        or not isinstance(payload.get("stdin"), str)
                    ):
                        raise ValueError("qualification invocation request is invalid")
                    try:
                        envelope = json.loads(payload["stdin"])
                    except json.JSONDecodeError:
                        envelope = None
                    semantic_result = envelope.get("semantic_result") if isinstance(envelope, dict) else None
                    public_input = semantic_result.get("public_input") if isinstance(semantic_result, dict) else None
                    observed_profile = public_input.get("profile") if isinstance(public_input, dict) else None
                    if isinstance(observed_profile, str):
                        public_input_binding["profile"] = observed_profile
                    environment = minimal_native_environment(
                        dict(os.environ),
                        cwd=owner_repository,
                        control=runtime_environment,
                    )
                    process = subprocess.run(
                        [str(installed_wrapper), "--invocation", "-"],
                        cwd=owner_repository,
                        input=payload["stdin"],
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False,
                        env=environment,
                    )
                    response = {
                        "returncode": process.returncode,
                        "stdout": process.stdout,
                        "stderr": process.stderr,
                    }
                except Exception as exc:
                    response = {
                        "returncode": 2,
                        "stdout": "",
                        "stderr": f"qualification invocation boundary failed: {exc}",
                    }
                with response_fifo.open("w", encoding="utf-8") as handle:
                    json.dump(response, handle, separators=(",", ":"))
                return
        finally:
            os.close(descriptor)

    thread = threading.Thread(
        target=serve,
        name="guru-qualification-public-invocation",
        daemon=True,
    )
    thread.start()
    return thread

def build_context(
    request: dict[str, Any],
    adapter: str = "shared",
) -> tuple[
    str,
    Path,
    Path,
    Path,
    Path,
    Path,
    str,
    Path,
    threading.Thread | None,
    threading.Event | None,
    dict[str, str] | None,
]:
    workdir = Path(request["workdir"]).resolve()
    execution_root = workdir.parent
    projection_root, skill_path, wrapper_path, skill_sha256, wrapper_sha256 = stage_public_projection(request, execution_root)
    runtime_target = public_runtime_target(request)
    runtime_package_root, execution_runtime_target, runtime_environment = stage_owner_execution(
        request, execution_root, runtime_target
    )
    owner_repository = execution_runtime_target.parents[4]
    qualification_codex = request["skill_id"] == QUALIFICATION_SKILL and adapter == "codex"
    public_repository_identity = (
        qualification_public_repository_identity(owner_repository)
        if qualification_codex
        else None
    )
    public_input_binding: dict[str, str] | None = None
    if not qualification_codex:
        boundary_path, boundary_thread, boundary_stop = start_public_runtime_boundary(
            execution_root,
            execution_runtime_target,
            runtime_package_root,
            projection_root,
            wrapper_path,
            runtime_environment,
        )
    if qualification_codex:
        if request.get("schema_version") == "3.0":
            model_root = (execution_root / "model-sandbox").resolve()
            if model_root.exists():
                raise ValueError("qualification model sandbox already exists")
            model_root.mkdir(parents=True)
        else:
            model_root = Path(
                tempfile.mkdtemp(prefix="guru-qualification-model-")
            ).resolve()
        model_projection_root = model_root / "public-package"
        model_repository_root = model_root / "evidence/repository"
        model_evidence_root = model_root / "evidence/case"
        model_output_root = model_root / "output"
        model_bin_root = model_root / "bin"
        model_evidence_root.mkdir(parents=True)
        model_output_root.mkdir()
        model_bin_root.mkdir()
        model_projection_copy(projection_root, model_projection_root)
        stage_repository_projection(owner_repository, model_repository_root)
        evidence_paths: list[Path] = []
        for index, relative in enumerate(request["files"], 1):
            staged = workdir / relative
            if not staged.is_file():
                raise ValueError("staged case file is unavailable")
            suffix = staged.suffix if staged.suffix else ".data"
            target = model_evidence_root / f"evidence-{index:02d}{suffix}"
            shutil.copy2(staged, target)
            evidence_paths.append(target)
        trace_path = model_root / "native-trace.json"
        helper_path = model_bin_root / "native-trace-helper.py"
        request_fifo = model_root / ".invoke-request"
        response_fifo = model_root / ".invoke-response"
        boundary_stop = threading.Event()
        public_input_binding = {}
        boundary_thread = start_qualification_runtime_boundary(
            request_fifo,
            response_fifo,
            boundary_stop,
            owner_repository,
            runtime_package_root,
            runtime_environment,
            public_input_binding,
        )
        boundary_path = request_fifo
        projection_root = model_projection_root
        skill_path = projection_root / "SKILL.md"
        wrapper_path = projection_root / "scripts/invoke.sh"
        workdir = model_evidence_root
        helper_source = qualification_trace_helper_source()
    else:
        model_root = execution_root
        model_repository_root = owner_repository
        evidence_paths = [workdir / relative for relative in request["files"]]
        trace_path = execution_root / "native-trace.json"
        helper_path = execution_root / "native-trace-helper.py"
        request_fifo = execution_root / ".unused-request"
        response_fifo = execution_root / ".unused-response"
        helper_source = TRACE_HELPER
    helper_path.write_text(helper_source, encoding="utf-8")
    helper_path.chmod(0o755)
    file_sections: list[str] = []
    for index, relative in enumerate(request["files"]):
        staged = evidence_paths[index] if qualification_codex else workdir / relative
        if not staged.is_file():
            raise ValueError("staged case file is unavailable")
        if qualification_codex:
            file_sections.append(f"### {relative}\n{staged}")
        else:
            try:
                content = staged.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                content = f"<binary sha256={hashlib.sha256(staged.read_bytes()).hexdigest()}>"
            file_sections.append(f"### {relative}\n{content}")
    context_lines = [
        "Execute exactly one Guru Team Skill behavior eval.",
        f"Skill id: {request['skill_id']}",
        f"Exact public Skill projection: {projection_root}",
        f"Public wrapper: {wrapper_path}",
        f"Isolated workdir: {workdir}",
        f"Repository evidence projection: {model_repository_root}",
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
    ]
    if qualification_codex:
        assert public_repository_identity is not None
        context_lines.insert(
            6,
            "Public repository identity:\n"
            + json.dumps(public_repository_identity, separators=(",", ":")),
        )
        context_lines[-2:] = [
            "This Skill has no staged owner result. Directly review the case evidence and repository evidence projection under the Skill contract.",
            "Author the complete invocation-local semantic_result yourself. Do not infer or search for an expected decision or expected exit.",
            f"Before authoring public input, read {model_repository_root / QUALIFICATION_PUBLIC_AUTHORING_FACTS} with the trace helper owner_file operation. Copy the target_locator and non-Git target fields from the targets entry matching the public profile discriminator, then add exactly the listed current_head_fields using public_repository_identity.current_head. Do not include current_head_fields itself in public input, and never substitute the 40-character Git HEAD for a 64-character content identity.",
            "Use public_repository_identity.current_head for every current checkout_head, task_head, review_head, or review_commit field required by the selected public input schema; historical example identities are not current fixture evidence.",
            "Pass exactly one JSON envelope to the public wrapper through stdin. Do not write the envelope, decisions, typed result, or any qualification state to a file.",
            "Re-read every staged case file through the trace helper before deciding. Use the helper's owner_file read operation for any necessary read-only inspection of the repository evidence projection; never read eval corpus files or .trellis/.runtime.",
            "For this semantic invocation boundary, run only those traced reads and then the exact stdin public wrapper invocation command below.",
        ]
    context = "\n".join(context_lines)
    if qualification_codex:
        assert public_repository_identity is not None
        native_request = qualification_model_request(
            request,
            model_root=model_root,
            projection_root=projection_root,
            repository_root=model_repository_root,
            evidence_paths=evidence_paths,
            repository_identity=public_repository_identity,
        )
    else:
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
    if request.get("schema_version") == "2.0" and not qualification_codex:
        native_request.update({
            "model_id": request["model_id"],
            "invocation_index": request["invocation_index"],
        })
    native_request_path = (
        execution_root / "native-request.json"
        if qualification_codex
        else model_root / "native-request.json"
    )
    native_request_path.write_text(json.dumps(native_request, separators=(",", ":")), encoding="utf-8")
    request_sha256 = hashlib.sha256(native_request_path.read_bytes()).hexdigest()
    helper_arguments = (
        f"--trace {trace_path} --request-sha256 {request_sha256} --projection-root {projection_root} "
        f"--skill-sha256 {skill_sha256} --wrapper-sha256 {wrapper_sha256}"
    )
    context = context.replace(
        "First read the exact Skill contract with the helper's read operation, then invoke the exact public wrapper with its invoke operation.",
        f"First read the exact Skill contract with: {helper_path} {helper_arguments} read --kind skill_contract --path {skill_path}\n"
        f"Then invoke the exact public wrapper with: {helper_path} {helper_arguments} invoke --wrapper {wrapper_path} --execution-wrapper {boundary_path} -- <declared wrapper arguments>",
    )
    if qualification_codex:
        case_read_commands = "\n".join(
            f"{helper_path} {helper_arguments} --repository-root {model_repository_root} "
            f"--sandbox-root {model_root} --request-fifo {request_fifo} --response-fifo {response_fifo} "
            f"read --kind case_file --path {path}"
            for path in evidence_paths
        )
        qualification_helper_arguments = (
            f"{helper_arguments} --repository-root {model_repository_root} "
            f"--sandbox-root {model_root} --request-fifo {request_fifo} --response-fifo {response_fifo}"
        )
        public_interface_path = projection_root / "interface.json"
        public_interface = json.loads(public_interface_path.read_text(encoding="utf-8"))
        profile_schema_paths = [
            projection_root / item["schema"]["path"]
            for item in public_interface["public_contracts"]["input"]["profiles"]
        ]
        profile_schema_read_commands = "\n".join(
            f"{helper_path} {qualification_helper_arguments} read --kind skill_contract --path {path}"
            for path in profile_schema_paths
        )
        context = context.replace(
            f"First read the exact Skill contract with: {helper_path} {helper_arguments} read --kind skill_contract --path {skill_path}",
            f"First read the exact Skill contract with: {helper_path} {qualification_helper_arguments} read --kind skill_contract --path {skill_path}",
        )
        context = context.replace(
            f"Then invoke the exact public wrapper with: {helper_path} {helper_arguments} invoke --wrapper {wrapper_path} --execution-wrapper {boundary_path} -- <declared wrapper arguments>",
            (
                "Before authoring the invocation envelope, read the exact public Interface and shared "
                "authoring schemas with these commands:\n"
                f"{helper_path} {qualification_helper_arguments} read --kind skill_contract --path {public_interface_path}\n"
                f"{helper_path} {qualification_helper_arguments} read --kind skill_contract --path {projection_root / 'schemas/semantic-result.schema.json'}\n"
                f"{helper_path} {qualification_helper_arguments} read --kind skill_contract --path {projection_root / 'schemas/public-input.schema.json'}\n"
                "Then execute exactly one of the following profile-schema reads: choose the schema whose "
                "declared discriminator equals the public_input.profile you author. Do not infer the profile "
                "shape from an example, a prior invocation, or the case framing:\n"
                f"{profile_schema_read_commands}\n"
                "Then re-read every staged case file with these exact commands:\n"
                f"{case_read_commands or '<no staged case files>'}\n"
                "For additional installed-repository evidence, use the same helper read command with "
                f"--kind owner_file --path <absolute-path-below-{model_repository_root}>.\n"
                "Finally pass exactly one JSON invocation envelope to the exact public wrapper through "
                "this quoted heredoc. Do not use printf and do not interpolate the JSON into a shell-quoted "
                "argument:\n"
                f"{helper_path} {qualification_helper_arguments} invoke --stdin <<'GURU_INVOCATION_JSON'\n"
                "<invocation-envelope-json>\n"
                "GURU_INVOCATION_JSON"
            ),
        )
        request["prompt_sha256"] = qualification_prompt_sha256(
            native_request,
            skill_sha256,
            request["model_id"],
        )
    context_path = model_root / "native-context.txt"
    context_path.write_text(context, encoding="utf-8")
    private_root = execution_root / "private-control"
    private_root.mkdir(exist_ok=True)
    protocol_path = private_root / "native-protocol.json"
    protocol_path.write_text(json.dumps({
        "schema_version": "1.0", "native_request_path": str(native_request_path),
        "request_sha256": request_sha256, "helper_path": str(helper_path),
        "trace_path": str(trace_path), "skill_path": str(skill_path),
        "wrapper_path": str(wrapper_path), "execution_wrapper_path": str(boundary_path),
        "owner_repository": str(owner_repository),
        "repository_projection_root": str(model_repository_root),
        "model_root": str(model_root),
        "request_fifo": str(request_fifo),
        "response_fifo": str(response_fifo),
        "private_root": str(private_root),
        "projection_root": str(projection_root),
        "skill_sha256": skill_sha256, "wrapper_sha256": wrapper_sha256,
    }, separators=(",", ":")), encoding="utf-8")
    return (
        context, context_path, wrapper_path, trace_path, protocol_path,
        native_request_path, request_sha256, boundary_path, boundary_thread,
        boundary_stop, public_input_binding,
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
    qualification_codex = (
        request.get("skill_id") == QUALIFICATION_SKILL
        and protocol.get("model_root") != str(Path(request["workdir"]).resolve().parent)
    )
    if qualification_codex:
        model_root = Path(protocol["model_root"]).resolve()
        declared_case_reads = {
            path.resolve()
            for path in (model_root / "evidence/case").iterdir()
            if path.is_file()
        }
    else:
        workdir = Path(request["workdir"]).resolve()
        declared_case_reads = {(workdir / relative).resolve() for relative in request["files"]}
    allowed_reads = {skill_path, *declared_case_reads}
    owner_repository = Path(
        protocol.get("repository_projection_root") or protocol["owner_repository"]
    ).resolve()
    skill_reads = []
    case_reads: set[Path] = set()
    invocations = []
    for event in events:
        if not isinstance(event, dict) or event.get("request_sha256") != request_sha256:
            raise ValueError("native trace event binding is invalid")
        if event.get("kind") == "read":
            if set(event) != {"kind", "target_kind", "path", "sha256", "request_sha256"}:
                raise ValueError("native read trace shape is invalid")
            target = Path(str(event.get("path"))).resolve()
            owner_read = False
            public_projection_read = False
            if (
                qualification_codex
                and event.get("target_kind") == "skill_contract"
            ):
                try:
                    public_relative = target.relative_to(projection_root)
                except ValueError:
                    pass
                else:
                    public_projection_read = (
                        ".runtime" not in public_relative.parts
                        and "evals" not in public_relative.parts
                    )
            if qualification_codex and event.get("target_kind") == "owner_file":
                try:
                    owner_relative = target.relative_to(owner_repository)
                except ValueError:
                    pass
                else:
                    owner_read = (
                        ".git" not in owner_relative.parts
                        and ".runtime" not in owner_relative.parts
                        and "evals" not in owner_relative.parts
                    )
            if (
                target not in allowed_reads
                and not public_projection_read
                and not owner_read
            ):
                raise ValueError("native trace contains an undeclared file read")
            try:
                expected_sha256 = hashlib.sha256(target.read_bytes()).hexdigest()
            except OSError:
                raise ValueError("native trace read target is unavailable")
            if event.get("sha256") != expected_sha256:
                raise ValueError("native trace read digest mismatch")
            if target == skill_path and event.get("target_kind") == "skill_contract":
                skill_reads.append(event)
            if target in declared_case_reads and event.get("target_kind") == "case_file":
                case_reads.add(target)
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
    if qualification_codex and case_reads != declared_case_reads:
        raise ValueError("qualification native trace must re-read every staged case file")
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
    if qualification_codex and argv != [
        str(wrapper_path.resolve()), "--invocation", "-",
    ]:
        raise ValueError("qualification public invocation arguments are invalid")
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
        return [sys.executable, command, "--request", str(native_request_path), "--context", str(context_path), "--workdir", workdir], None
    if adapter == "codex":
        qualification_request = (
            request.get("skill_id") == QUALIFICATION_SKILL
            or request.get("schema_version") in {"2.0", "3.0"}
        )
        model_root = Path(
            request.get("_model_root") or native_request_path.resolve().parent
        ).resolve()
        output_path = model_root / "output/native-last-message.txt"
        if qualification_request:
            if request.get("model_id") != QUALIFICATION_MODEL:
                raise ValueError("qualification production model identity is invalid")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            argv = [
                command,
                "exec",
                "--ephemeral",
                "--strict-config",
                "--skip-git-repo-check",
                "--cd",
                str(model_root),
                "--model",
                QUALIFICATION_MODEL,
                "--output-last-message",
                str(output_path),
                context,
            ]
            return argv, output_path
        trusted_root = str(Path(request["runtime_target"]).resolve().parents[4])
        execution_root = str(native_request_path.resolve().parent)
        argv = [
            command, "exec", "--ephemeral", "--ignore-user-config", "--sandbox", "workspace-write",
            "--cd", trusted_root, "--add-dir", execution_root,
            "--add-dir", workdir, "--add-dir", str(projection_root),
        ]
        argv.extend(["--output-last-message", str(output_path), context])
        return argv, output_path
    if adapter == "claude":
        trace_helper = native_request_path.with_name("native-trace-helper.py")
        return [
            command, "--print", "--safe-mode", "--output-format", "json", "--no-session-persistence",
            "--permission-mode", "dontAsk",
            f"--allowedTools=Bash({trace_helper} *)",
            "--add-dir", str(projection_root),
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
            boundary_thread, boundary_stop, public_input_binding,
        ) = build_context(request, args.adapter)
    except Exception as exc:
        transcript.write_text(json.dumps({"adapter": args.adapter, "error": str(exc)}), encoding="utf-8")
        return emit(response(request, "execution_error", transcript, stderr="adapter request/context invalid"))
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    projection_root = Path(protocol["projection_root"])
    owner_repository = Path(protocol["owner_repository"])
    model_root = Path(protocol["model_root"])
    qualification_codex = request.get("skill_id") == QUALIFICATION_SKILL and args.adapter == "codex"
    repository_before = (
        repository_file_inventory(owner_repository)
        if request.get("skill_id") == QUALIFICATION_SKILL
        else None
    )
    codex_home = None
    permission_probe: dict[str, Any] | None = None
    denied_paths: list[Path] = []
    if qualification_codex:
        private_root = Path(protocol["private_root"])
        codex_home = external_codex_home(dict(os.environ), request_path.parents[2])
        control_root_value = os.environ.get("GURU_TEAM_QUALIFICATION_CONTROL_ROOT")
        source_worktree_value = os.environ.get("GURU_TEAM_QUALIFICATION_SOURCE_WORKTREE")
        if not control_root_value or not source_worktree_value:
            raise ValueError("qualification host-only deny roots are incomplete")
        control_root = Path(control_root_value).expanduser().resolve()
        source_worktree = Path(source_worktree_value).expanduser().resolve()
        control_map = control_root / "case-map.json"
        if (
            not control_root.is_dir()
            or control_root.is_symlink()
            or stat.S_IMODE(control_root.stat().st_mode) != 0o700
            or not control_map.is_file()
            or control_map.is_symlink()
            or stat.S_IMODE(control_map.stat().st_mode) != 0o600
            or not source_worktree.is_dir()
            or source_worktree.is_symlink()
        ):
            raise ValueError("qualification host-only deny roots are invalid")
        denied_paths = [
            codex_home,
            control_root,
            source_worktree,
            private_root,
            owner_repository,
            Path(request["workdir"]),
            Path(request["package_root"]),
            Path("/tmp"),
            Path("/private/tmp"),
        ]
        canonical_corpus = Path(request["package_root"]) / "evals/evals.json"
        if canonical_corpus.exists():
            denied_paths.append(canonical_corpus)
        write_codex_permission_profile(codex_home, model_root, denied_paths)
        request["_model_root"] = str(model_root)
    argv, output_path = native_argv(
        args.adapter,
        native,
        request,
        context,
        context_path,
        native_request_path,
        projection_root,
    )
    native_environment = minimal_native_environment(
        dict(os.environ),
        cwd=model_root,
        codex_home=codex_home,
        temporary_root=model_root / "output" if qualification_codex else None,
        control={
            "GURU_TEAM_DISPATCHER": str(boundary_path),
            "GURU_TEAM_NATIVE_REQUEST": str(native_request_path),
            "GURU_TEAM_NATIVE_PROTOCOL": str(protocol_path),
        },
    )
    if qualification_codex:
        permission_probe = run_codex_permission_probe(
            native,
            native_environment,
            model_root,
            canonical_permission_paths(denied_paths),
        )
        if permission_probe["returncode"] != 0:
            if boundary_stop is not None:
                boundary_stop.set()
            transcript.write_text(json.dumps({
                "adapter": args.adapter,
                "native_command": args.native_command,
                "environment": recorded_native_environment(native_environment),
                "permission_probe": permission_probe,
                "status": "execution_error",
            }, indent=2), encoding="utf-8")
            return emit(response(
                request,
                "execution_error",
                transcript,
                stderr="qualification Codex permission probe failed",
                native_trace=trace_path,
            ))
    model_input_audit = {
        "argv": argv,
        "cwd": str(model_root.resolve()),
        "context": context,
        "context_path": str(context_path.resolve()),
        "native_request": json.loads(native_request_path.read_text(encoding="utf-8")),
        "native_request_path": str(native_request_path.resolve()),
        "projection_root": str(projection_root.resolve()),
        "repository_projection_root": str(Path(protocol["repository_projection_root"]).resolve()),
        "wrapper_path": str(wrapper_path.resolve()),
        "environment": recorded_native_environment(native_environment),
    }
    started = time.monotonic_ns()
    process = subprocess.run(
        argv,
        cwd=model_root,
        input=context if args.adapter == "claude" else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=native_environment,
    )
    if boundary_stop is not None:
        boundary_stop.set()
    if boundary_thread is not None:
        boundary_thread.join(timeout=1)
    timing_ms = max(0, (time.monotonic_ns() - started) // 1_000_000)
    residue_error = None
    if repository_before is not None:
        repository_after = repository_file_inventory(owner_repository)
        if repository_after != repository_before:
            residue_error = "qualification invocation changed repository file inventory"
        runtime_root = owner_repository / ".trellis/.runtime"
        if runtime_root.exists():
            residue_error = "qualification invocation created ignored runtime residue"
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
        "environment": recorded_native_environment(native_environment),
        "model_input_audit": model_input_audit,
        "public_input_binding": public_input_binding,
        "permission_probe": permission_probe,
        "returncode": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
    }, indent=2), encoding="utf-8")
    if process.returncode != 0:
        return emit(response(request, "execution_error", transcript, stderr=process.stderr, timing_ms=timing_ms, native_trace=trace_path))
    if residue_error is not None:
        return emit(response(request, "execution_error", transcript, stderr=residue_error, timing_ms=timing_ms, native_trace=trace_path))
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
