from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import io
import json
import os
import select
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any


ADAPTERS = ("shared", "codex", "claude", "cursor")

OWNER_INPUT = ".trellis/.runtime/guru-team/evals/public-input.json"
OWNER_RESULT = ".trellis/.runtime/guru-team/evals/owner-result.json"
OWNER_PLAN = ".trellis/.runtime/guru-team/evals/owner-plan.json"
OWNER_INVOCATION = ".trellis/.runtime/guru-team/evals/invocation.json"
WORKSPACE_CALL_LOCAL_STATE: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
PRODUCTION_SKILLS = {
    "guru-approve-task-plan",
    "guru-check-task",
    "guru-create-task-commit",
    "guru-finalize-task",
    "guru-merge-task-pr",
    "guru-reconcile-task-base",
    "guru-review-branch",
    "guru-review-task-publication",
    "guru-restore-archived-task",
    "guru-verify-extension-installation",
}
QUALIFICATION_SKILL = "guru-qualify-normal-scenario"
QUALIFICATION_MODEL = "gpt-5.6-sol"
QUALIFICATION_MODEL_REQUEST_SCHEMA = "3.0"
QUALIFICATION_PROMPT_PROTOCOL = "guru-qualification-production-prompt-2.0"
QUALIFICATION_PERMISSION_PROFILE = "guru-qualification-production"
QUALIFICATION_PUBLIC_AUTHORING_FACTS = "docs/qualification-eval/public-authoring-facts.json"

MINIMAL_NATIVE_ENVIRONMENT_KEYS = (
    "HOME",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "PATH",
    "SSL_CERT_DIR",
    "SSL_CERT_FILE",
    "TERM",
    "TMPDIR",
)
SECRET_ENVIRONMENT_MARKERS = (
    "API_KEY",
    "ACCESS_TOKEN",
    "AUTH_TOKEN",
    "BEARER",
    "CREDENTIAL",
    "DATABASE_URL",
    "PASSWORD",
    "PRIVATE_KEY",
    "SECRET",
    "SESSION_TOKEN",
)

MANAGED_PYTHON_SHEBANG = f"#!{sys.executable}\n"

TRACE_HELPER = MANAGED_PYTHON_SHEBANG + r'''from __future__ import annotations

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
    read_parser.add_argument(
        "--kind",
        required=True,
        choices=("skill_contract", "case_file", "owner_file"),
    )
    read_parser.add_argument("--path", required=True)
    invoke_parser = subparsers.add_parser("invoke")
    invoke_parser.add_argument("--wrapper", required=True)
    invoke_parser.add_argument("--execution-wrapper", required=True)
    invoke_parser.add_argument("--stdin", action="store_true")
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
    execution_wrapper = Path(args.execution_wrapper).resolve()
    process = subprocess.run(
        [str(execution_wrapper), "--package-root", args.projection_root, *forwarded], text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False, input=sys.stdin.read() if args.stdin else None,
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


QUALIFICATION_TRACE_HELPER_BODY = r'''from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
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


def inside(root: Path, target: Path) -> bool:
    try:
        target.relative_to(root)
    except ValueError:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", required=True)
    parser.add_argument("--request-sha256", required=True)
    parser.add_argument("--projection-root", required=True)
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--sandbox-root", required=True)
    parser.add_argument("--request-fifo", required=True)
    parser.add_argument("--response-fifo", required=True)
    parser.add_argument("--skill-sha256", required=True)
    parser.add_argument("--wrapper-sha256", required=True)
    subparsers = parser.add_subparsers(dest="operation", required=True)
    read_parser = subparsers.add_parser("read")
    read_parser.add_argument(
        "--kind",
        required=True,
        choices=("skill_contract", "case_file", "owner_file"),
    )
    read_parser.add_argument("--path", required=True)
    invoke_parser = subparsers.add_parser("invoke")
    invoke_parser.add_argument("--stdin", action="store_true")
    args = parser.parse_args()
    sandbox_root = Path(args.sandbox_root).resolve()
    projection_root = Path(args.projection_root).resolve()
    repository_root = Path(args.repository_root).resolve()
    trace_path = Path(args.trace).resolve()
    if not all(inside(sandbox_root, path) for path in (
        projection_root,
        repository_root,
        trace_path,
        Path(args.request_fifo).resolve(),
        Path(args.response_fifo).resolve(),
    )):
        raise ValueError("qualification helper path escapes the model sandbox")
    if args.operation == "read":
        target = Path(args.path).resolve()
        allowed_root = repository_root if args.kind == "owner_file" else sandbox_root
        if not inside(allowed_root, target):
            raise ValueError("qualification read target escapes its projected root")
        if "evals" in target.parts or ".runtime" in target.parts:
            raise ValueError("qualification read target is private")
        content = target.read_bytes()
        append_event(trace_path, args.request_sha256, str(projection_root), args.skill_sha256, args.wrapper_sha256, {
            "kind": "read", "target_kind": args.kind, "path": str(target), "sha256": digest(content),
        })
        sys.stdout.buffer.write(content)
        return 0
    if not args.stdin:
        raise ValueError("qualification invocation requires stdin")
    request_fifo = Path(args.request_fifo)
    response_fifo = Path(args.response_fifo)
    request_payload = {
        "arguments": ["--invocation", "-"],
        "stdin": sys.stdin.read(),
    }
    with request_fifo.open("w", encoding="utf-8") as handle:
        json.dump(request_payload, handle, separators=(",", ":"))
    with response_fifo.open("r", encoding="utf-8") as handle:
        response = json.load(handle)
    if set(response) != {"returncode", "stdout", "stderr"}:
        raise ValueError("qualification invocation response is invalid")
    append_event(trace_path, args.request_sha256, str(projection_root), args.skill_sha256, args.wrapper_sha256, {
        "kind": "invoke", "wrapper_path": str(projection_root / "scripts/invoke.sh"),
        "argv": [str(projection_root / "scripts/invoke.sh"), "--invocation", "-"],
        "returncode": response["returncode"], "stdout_sha256": stdout_digest(response["stdout"]),
        "stderr_sha256": digest(response["stderr"].encode("utf-8")),
    })
    sys.stdout.write(response["stdout"])
    sys.stderr.write(response["stderr"])
    return int(response["returncode"])


if __name__ == "__main__":
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
    result = {
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
    if request.get("schema_version") == "2.0":
        result.update({
            "schema_version": "2.0",
            "matrix_sha256": str(request.get("matrix_sha256") or "0" * 64),
            "package_sha256": str(request.get("package_sha256") or "0" * 64),
            "prompt_sha256": str(request.get("prompt_sha256") or "0" * 64),
            "model_id": str(request.get("model_id") or QUALIFICATION_MODEL),
            "invocation_index": int(request.get("invocation_index") or 1),
        })
    elif request.get("schema_version") == "3.0":
        result.pop("corpus_sha256", None)
        result.update({
            "schema_version": "3.0",
            "invocation_id": str(request.get("invocation_id") or "0" * 64),
            "package_sha256": str(request.get("package_sha256") or "0" * 64),
            "prompt_sha256": str(request.get("prompt_sha256") or "0" * 64),
            "model_id": str(request.get("model_id") or QUALIFICATION_MODEL),
        })
    return result


def package_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root)
        if "__pycache__" in relative.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        digest.update(relative.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def repository_file_inventory(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] == ".git":
            continue
        if "__pycache__" in relative.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        result[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def secret_environment_key(name: str) -> bool:
    upper = name.upper()
    return any(marker in upper for marker in SECRET_ENVIRONMENT_MARKERS)


def minimal_native_environment(
    parent: dict[str, str],
    *,
    cwd: Path,
    codex_home: Path | None = None,
    temporary_root: Path | None = None,
    control: dict[str, str] | None = None,
) -> dict[str, str]:
    environment = {
        name: parent[name]
        for name in MINIMAL_NATIVE_ENVIRONMENT_KEYS
        if name in parent and parent[name] and not secret_environment_key(name)
    }
    environment["PATH"] = environment.get("PATH") or os.defpath
    environment["PWD"] = str(cwd.resolve())
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    if temporary_root is not None:
        resolved_temporary_root = temporary_root.resolve()
        try:
            resolved_temporary_root.relative_to(cwd.resolve())
        except ValueError:
            raise ValueError("native temporary root must be inside cwd") from None
        if not temporary_root.is_dir() or temporary_root.is_symlink():
            raise ValueError("native temporary root must be an existing directory")
        environment["TMPDIR"] = str(resolved_temporary_root)
        environment["TMPPREFIX"] = str(resolved_temporary_root / "zsh")
    if codex_home is not None:
        environment["CODEX_HOME"] = str(codex_home.resolve())
    for name, value in (control or {}).items():
        if secret_environment_key(name):
            raise ValueError("native control environment contains a secret-like key")
        environment[name] = value
    return environment


def recorded_native_environment(environment: dict[str, str]) -> dict[str, str]:
    if any(secret_environment_key(name) for name in environment):
        raise ValueError("native environment contains a secret-like key")
    return dict(sorted(environment.items()))


def canonical_permission_paths(paths: list[Path]) -> list[Path]:
    result: set[Path] = set()
    for path in paths:
        resolved = path.expanduser().resolve()
        result.add(resolved)
        if str(resolved).startswith("/tmp/") or resolved == Path("/tmp"):
            result.add(Path("/private") / resolved.relative_to("/"))
        if str(resolved).startswith("/private/tmp/") or resolved == Path("/private/tmp"):
            result.add(Path("/") / resolved.relative_to("/private"))
    return sorted(result, key=lambda item: str(item))


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def write_codex_permission_profile(
    codex_home: Path,
    model_root: Path,
    denied_paths: list[Path],
) -> Path:
    codex_home.mkdir(parents=True, exist_ok=True)
    os.chmod(codex_home, 0o700)
    profile = QUALIFICATION_PERMISSION_PROFILE
    temporary_root = (model_root / "output").resolve()
    lines = [
        f"default_permissions = {toml_string(profile)}",
        'approval_policy = "never"',
        "project_root_markers = []",
        "",
        "[shell_environment_policy]",
        'inherit = "none"',
        "",
        "[shell_environment_policy.set]",
        f"PATH = {toml_string(os.defpath)}",
        'PYTHONDONTWRITEBYTECODE = "1"',
        f"PWD = {toml_string(str(model_root.resolve()))}",
        f"TMPDIR = {toml_string(str(temporary_root))}",
        f"TMPPREFIX = {toml_string(str(temporary_root / 'zsh'))}",
        "",
        f"[permissions.{profile}]",
        "",
        f"[permissions.{profile}.filesystem]",
        '":root" = "read"',
    ]
    for path in canonical_permission_paths(denied_paths):
        lines.append(f"{toml_string(str(path))} = \"deny\"")
    lines.extend([
        "",
        f"[permissions.{profile}.filesystem.\":workspace_roots\"]",
        '"." = "write"',
        "",
        f"[permissions.{profile}.network]",
        "enabled = false",
        "",
    ])
    config = codex_home / "config.toml"
    config.write_text("\n".join(lines), encoding="utf-8")
    os.chmod(config, 0o600)
    return config


def external_codex_home(parent: dict[str, str], execution_root: Path) -> Path:
    value = parent.get("CODEX_HOME")
    if not value:
        raise ValueError("qualification production requires one external isolated CODEX_HOME")
    codex_home = Path(value).expanduser().resolve()
    execution = execution_root.resolve()
    try:
        codex_home.relative_to(execution)
    except ValueError:
        pass
    else:
        raise ValueError("qualification CODEX_HOME must remain outside the production RUN_ROOT")
    auth = codex_home / "auth.json"
    if (
        not codex_home.is_dir()
        or codex_home.is_symlink()
        or stat.S_IMODE(codex_home.stat().st_mode) != 0o700
        or not auth.is_file()
        or auth.is_symlink()
        or stat.S_IMODE(auth.stat().st_mode) != 0o600
    ):
        raise ValueError("qualification external CODEX_HOME/auth must be owner-private and complete")
    return codex_home


def resolved_base_interpreter(error_prefix: str) -> Path:
    raw_interpreter = getattr(sys, "_base_executable", None)
    if not isinstance(raw_interpreter, str) or not raw_interpreter.strip():
        raise ValueError(f"{error_prefix} base interpreter is unavailable")
    try:
        interpreter = Path(raw_interpreter).expanduser().resolve(strict=True)
    except (OSError, RuntimeError):
        raise ValueError(f"{error_prefix} base interpreter is unavailable") from None
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK):
        raise ValueError(f"{error_prefix} base interpreter is not executable")
    return interpreter


def qualification_trace_helper_source() -> str:
    interpreter = resolved_base_interpreter("qualification trace helper")
    return f"#!{interpreter}\n{QUALIFICATION_TRACE_HELPER_BODY}"


def permission_probe_interpreter(denied_paths: list[Path]) -> Path:
    interpreter = resolved_base_interpreter("permission probe")
    for denied_path in canonical_permission_paths(denied_paths):
        try:
            interpreter.relative_to(denied_path)
        except ValueError:
            continue
        raise ValueError("permission probe base interpreter is inside a denied path")
    return interpreter


def permission_probe_argv(
    codex_command: str,
    model_root: Path,
    probe_script: Path,
    denied_paths: list[Path],
) -> list[str]:
    interpreter = permission_probe_interpreter(denied_paths)
    return [
        codex_command,
        "sandbox",
        "-P",
        QUALIFICATION_PERMISSION_PROFILE,
        "-C",
        str(model_root.resolve()),
        str(interpreter),
        str(probe_script.resolve()),
        str(model_root.resolve()),
        *(str(path) for path in denied_paths),
    ]


def run_codex_permission_probe(
    codex_command: str,
    environment: dict[str, str],
    model_root: Path,
    denied_paths: list[Path],
) -> dict[str, Any]:
    probe_script = model_root / "permission-probe.py"
    probe_script.write_text(
        "from pathlib import Path\n"
        "import json,sys\n"
        "root=Path(sys.argv[1]); probe=root/'permission-positive.txt'\n"
        "probe.write_text('ok',encoding='utf-8')\n"
        "positive=probe.read_text(encoding='utf-8')=='ok'\n"
        "denied=[]\n"
        "for value in sys.argv[2:]:\n"
        " path=Path(value)\n"
        " try:\n"
        "  path.stat()\n"
        " except (OSError,PermissionError):\n"
        "  denied.append(value)\n"
        " else:\n"
        "  try:\n"
        "   if path.is_file(): path.read_bytes()\n"
        "   else: list(path.iterdir())\n"
        "  except (OSError,PermissionError): denied.append(value)\n"
        "print(json.dumps({'positive':positive,'denied':denied},separators=(',',':')))\n"
        "raise SystemExit(0 if positive and len(denied)==len(sys.argv[2:]) else 1)\n",
        encoding="utf-8",
    )
    argv = permission_probe_argv(codex_command, model_root, probe_script, denied_paths)
    process = subprocess.run(
        argv,
        cwd=model_root,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError:
        payload = {}
    return {
        "argv": argv,
        "returncode": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
        "result": payload,
    }


def model_projection_copy(source: Path, destination: Path) -> None:
    def copy_file(source_value: str, destination_value: str) -> str:
        try:
            os.link(source_value, destination_value)
        except OSError:
            return shutil.copy2(source_value, destination_value)
        return destination_value

    shutil.copytree(source, destination, copy_function=copy_file)


def repository_projection_allowed(relative: Path) -> bool:
    if any(part in {".git", ".runtime", "__pycache__", "evals", "node_modules"} for part in relative.parts):
        return False
    value = relative.as_posix()
    private_prefixes = (
        ".trellis/guru-team/runtime/",
        ".trellis/guru-team/skills/adapters/",
        "trellis/skills/guru-team/runtime/",
        "trellis/skills/guru-team/adapters/",
    )
    if value.startswith(private_prefixes):
        return False
    if f"/packages/{QUALIFICATION_SKILL}/runtime/" in f"/{value}":
        return False
    if relative.name == "auth.json" or relative.name.startswith(".env"):
        return False
    return relative.suffix not in {".pyc", ".pyo"}


def stage_repository_projection(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for path in sorted(item for item in source.rglob("*") if item.is_file() and not item.is_symlink()):
        relative = path.relative_to(source)
        if not repository_projection_allowed(relative):
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(path, target)
        except OSError:
            shutil.copy2(path, target)


def qualification_public_repository_identity(owner_repository: Path) -> dict[str, str]:
    current_head = run_git(owner_repository, "rev-parse", "HEAD")
    if (
        len(current_head) != 40
        or any(character not in "0123456789abcdef" for character in current_head)
    ):
        raise ValueError("qualification public repository HEAD is invalid")
    return {"repo_locator": ".", "current_head": current_head}


def stage_qualification_public_authoring_fixture(owner_repository: Path) -> Path:
    task_root = owner_repository / ".trellis/tasks/current"
    task_root.mkdir(parents=True, exist_ok=True)
    planning = {
        "prd.md": "# Qualification Eval PRD\n\nReview the declared candidate set.\n",
        "design.md": "# Qualification Eval Design\n\nUse the public qualification entry.\n",
        "implement.md": "# Qualification Eval Implementation\n\nInvoke the installed wrapper once.\n",
        "issue-scope-ledger.json": json.dumps(
            {"schema_version": "1.0", "close_issues": [237]},
            separators=(",", ":"),
        ) + "\n",
    }
    for name, content in planning.items():
        (task_root / name).write_text(content, encoding="utf-8")

    public_root = owner_repository / "docs/qualification-eval"
    public_root.mkdir(parents=True, exist_ok=True)
    public_files = {
        "request.md": "# Qualification Eval Request\n\nReview the current candidate.\n",
        "authority.md": (
            "# Qualification Eval Authority\n\n"
            "The repository normal-operation scope explicitly excludes malicious or adversarial "
            "scenarios, deliberate workflow bypass, threat-model or defense-in-depth extensions, "
            "and unrequested hardening unless a current requirement explicitly includes one. "
            "When a candidate requires an explicitly excluded assumption, apply the package "
            "contract's explicit-exclusion precedence before the unsupported-entry or "
            "non-reproduction fallbacks.\n\n"
            "For supported honest workflow entries, current correctness authority requires "
            "recorders and executors to return values that match their current payloads, real "
            "callers to select the intended runtime, stale or mismatched identities to fail "
            "closed, and required canonical package and platform projections to remain complete. "
            "Current authority also explicitly preserves secret and credential redaction and "
            "required permission or destructive-action confirmation as supported nonstandard "
            "obligations.\n"
        ),
        "publication-payload.json": json.dumps(
            {"title": "Qualification eval", "close_issues": [237]},
            separators=(",", ":"),
        ) + "\n",
    }
    for name, content in public_files.items():
        (public_root / name).write_text(content, encoding="utf-8")

    planning_paths = [
        ".trellis/tasks/current/prd.md",
        ".trellis/tasks/current/design.md",
        ".trellis/tasks/current/implement.md",
    ]
    scope_ledger_path = ".trellis/tasks/current/issue-scope-ledger.json"
    planning_rows = [
        {
            "path": relative,
            "content_sha256": hashlib.sha256(
                (owner_repository / relative).read_bytes()
            ).hexdigest(),
        }
        for relative in sorted(planning_paths)
    ]
    planning_identity = hashlib.sha256(
        json.dumps(
            planning_rows,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    request_path = "docs/qualification-eval/request.md"
    authority_path = "docs/qualification-eval/authority.md"
    publication_path = "docs/qualification-eval/publication-payload.json"
    content_sha256 = lambda relative: hashlib.sha256(
        (owner_repository / relative).read_bytes()
    ).hexdigest()
    task_ref = ".trellis/tasks/current"
    targets = {
        "task_free_pre_write": {
            "target_locator": f"path:{request_path}",
            "target": {
                "repo_locator": ".",
                "request_locator": f"path:{request_path}",
                "bounded_paths": [request_path],
            },
            "current_head_fields": ["checkout_head"],
        },
        "task_free_evolution": {
            "target_locator": f"path:{request_path}",
            "target": {
                "repo_locator": ".",
                "request_locator": f"path:{request_path}",
                "approved_paths": [request_path],
                "edited_paths": [request_path],
            },
            "current_head_fields": ["checkout_head"],
        },
        "requirements_scope_set": {
            "target_locator": f"path:{authority_path}",
            "target": {
                "repo_locator": ".",
                "authority_kind": "active_task",
                "authority_locator": f"path:{authority_path}",
                "authority_identity": content_sha256(authority_path),
                "scope_locator": f"path:{authority_path}",
            },
            "current_head_fields": [],
        },
        "change_request_candidate_set": {
            "target_locator": f"path:{request_path}",
            "target": {
                "repo_locator": ".",
                "request_locator": f"path:{request_path}",
                "request_identity": content_sha256(request_path),
                "readiness_locators": [f"path:{authority_path}"],
            },
            "current_head_fields": [],
        },
        "planning_scenario_set": {
            "target_locator": task_ref,
            "target": {
                "repo_locator": ".",
                "task_ref": task_ref,
                "planning_paths": planning_paths,
                "scope_ledger_path": scope_ledger_path,
                "planning_identity": planning_identity,
            },
            "current_head_fields": [],
        },
        "implementation_discovery": {
            "target_locator": task_ref,
            "target": {
                "repo_locator": ".",
                "task_ref": task_ref,
                "planning_identity": planning_identity,
                "diff_locator": "HEAD...HEAD",
            },
            "current_head_fields": ["checkout_head"],
        },
        "base_impact_candidate_set": {
            "target_locator": task_ref,
            "target": {
                "repo_locator": ".",
                "task_ref": task_ref,
                "base_pair_locator": "HEAD...HEAD",
            },
            "current_head_fields": ["old_base_head", "new_base_head", "task_head"],
        },
        "phase2_candidate_set": {
            "target_locator": task_ref,
            "target": {
                "repo_locator": ".",
                "task_ref": task_ref,
                "planning_identity": planning_identity,
                "diff_locator": "HEAD...HEAD",
            },
            "current_head_fields": ["checkout_head"],
        },
        "branch_review_candidate_set": {
            "target_locator": task_ref,
            "target": {
                "repo_locator": ".",
                "task_ref": task_ref,
                "range_locator": "HEAD...HEAD",
            },
            "current_head_fields": ["base_head", "review_head", "review_commit"],
        },
        "publication_candidate_set": {
            "target_locator": task_ref,
            "target": {
                "repo_locator": ".",
                "task_ref": task_ref,
                "publication_payload_locator": f"path:{publication_path}",
                "publication_payload_identity": content_sha256(publication_path),
            },
            "current_head_fields": ["review_commit"],
        },
    }
    facts_path = owner_repository / QUALIFICATION_PUBLIC_AUTHORING_FACTS
    facts_path.write_text(
        json.dumps(
            {"schema_version": "1.0", "targets": targets},
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )
    return facts_path


def qualification_model_request(
    request: dict[str, Any],
    *,
    model_root: Path,
    projection_root: Path,
    repository_root: Path,
    evidence_paths: list[Path],
    repository_identity: dict[str, str],
) -> dict[str, Any]:
    return {
        "schema_version": QUALIFICATION_MODEL_REQUEST_SCHEMA,
        "protocol": QUALIFICATION_PROMPT_PROTOCOL,
        "skill_id": QUALIFICATION_SKILL,
        "prompt": request["prompt"],
        "public_package_root": projection_root.relative_to(model_root).as_posix(),
        "repository_evidence_root": repository_root.relative_to(model_root).as_posix(),
        "public_repository_identity": repository_identity,
        "evidence": [
            {
                "path": path.relative_to(model_root).as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for path in evidence_paths
        ],
        "public_invocation": request["interface"]["public_invocation"],
    }


def qualification_prompt_sha256(
    model_request: dict[str, Any],
    skill_sha256: str,
    model_id: str,
) -> str:
    identity = {
        "protocol": QUALIFICATION_PROMPT_PROTOCOL,
        "model_request": model_request,
        "skill_sha256": skill_sha256,
        "model_id": model_id,
    }
    encoded = json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def public_projection_assets(interface: dict[str, Any]) -> set[Path]:
    assets = {Path("SKILL.md"), Path("interface.json")}
    if interface.get("id") == QUALIFICATION_SKILL:
        assets.update({
            Path("references/contract.md"),
            Path("schemas/semantic-result.schema.json"),
            Path("examples/semantic-result.json"),
            Path("examples/public-invocation.json"),
        })
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


def public_projection_shared_assets(interface: dict[str, Any]) -> set[Path]:
    try:
        envelope = interface["public_contracts"]["invocation"]["call_local"]["envelope"]
    except (KeyError, TypeError):
        return set()
    if not isinstance(envelope, dict) or not isinstance(envelope.get("path"), str):
        raise ValueError("public call-local envelope reference is unavailable")
    relative = Path(envelope["path"])
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise ValueError("public call-local envelope contains an unsafe asset path")
    return {relative}


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
    shared_root = canonical_root.parents[1]
    for relative in sorted(public_projection_shared_assets(interface), key=lambda item: item.as_posix()):
        source = shared_root / relative
        destination = projection_root / relative
        if source.is_symlink() or not source.is_file() or destination.exists():
            raise ValueError(f"public shared projection asset is unavailable: {relative.as_posix()}")
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


def load_package_owner_runtime(runtime_target: Path, skill_id: str) -> Any:
    runtime_path = (
        runtime_target.parent.parent.parent
        / "skills/packages"
        / skill_id
        / "runtime/owner.py"
    )
    if not runtime_path.is_file():
        module = load_package_runtime_module(runtime_target, skill_id, "common")
        if skill_id == "guru-clarify-requirements":
            module.context_digest = module.digest
            module.derive_requirements_clarification_result = (
                lambda payload: derive_clarification_eval_result(module, payload)
            )
        elif skill_id == "guru-review-change-request":
            compose_change_request_eval_runtime(runtime_target, module)
        elif skill_id == "guru-create-task-workspace":
            compose_task_workspace_eval_runtime(runtime_target, module)
        elif skill_id == "guru-review-branch":
            compose_review_branch_eval_runtime(runtime_target, module)
        return module
    if runtime_path.is_symlink():
        raise ValueError("package owner staging runtime is unavailable")
    spec = importlib.util.spec_from_file_location(
        f"guru_team_eval_{skill_id.replace('-', '_')}_owner", runtime_path
    )
    if spec is None or spec.loader is None:
        raise ValueError("package owner staging runtime cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def compose_change_request_eval_runtime(runtime_target: Path, module: Any) -> None:
    review = load_package_runtime_module(
        runtime_target, "guru-review-change-request", "common"
    )
    clarity = load_package_runtime_module(
        runtime_target, "guru-clarify-requirements", "common"
    )
    wording = load_package_runtime_module(
        runtime_target, "guru-review-contract-wording", "common"
    )
    module.context_digest = review.digest
    module.CHANGE_REQUEST_REVIEW_DIMENSIONS = review.DIMENSIONS
    module.CHANGE_REQUEST_REVIEW_CONSUMERS = review.CONSUMERS
    module.CHANGE_REQUEST_REVIEW_GATE_BY_EXIT = review.GATES
    module.CONTRACT_WORDING_REVIEW_DIMENSIONS = wording.CONTRACT_WORDING_REVIEW_DIMENSIONS
    module.CONTRACT_WORDING_PLANNING_REVIEW_DIMENSIONS = (
        wording.CONTRACT_WORDING_PLANNING_REVIEW_DIMENSIONS
    )
    module.derive_requirements_clarification_result = (
        lambda payload: derive_clarification_eval_result(clarity, payload)
    )
    module.contract_wording_build_scope = wording.contract_wording_build_scope
    module.scan_contract_wording = wording.scan_contract_wording
    module.contract_wording_derive_result = wording.contract_wording_derive_result

    def issue_view(repo: str, number: int, root: Path) -> dict[str, Any]:
        process = subprocess.run(
            ["gh", "issue", "view", str(number), "--repo", repo, "--json",
             "number,url,state,title,body,updatedAt"],
            cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False,
        )
        if process.returncode != 0:
            raise ValueError("change-request eval issue authority is unavailable")
        value = json.loads(process.stdout)
        if not isinstance(value, dict):
            raise ValueError("change-request eval issue authority is invalid")
        return value

    def scope_hashes(scope: dict[str, Any]) -> tuple[str | None, str | None, str | None]:
        values = {
            item.get("field"): item.get("content_sha256")
            for item in scope.get("items", []) if isinstance(item, dict)
        }
        title, body = values.get("title"), values.get("body")
        return title, body, review.digest({"title_sha256": title, "body_sha256": body}) if title and body else None

    def authority_projection(repo: Any, source: Any, body_sha256: Any) -> dict[str, Any] | None:
        if not isinstance(repo, str) or not isinstance(source, dict) or source.get("kind") != "draft":
            return None
        return {"kind": "draft", "repo": repo, "issue_number": None, "url": None,
                "state": "draft", "updated_at": None, "body_sha256": body_sha256}

    def normalize_target(root: Path, raw: Any, source_path: str, mode: str):
        source = review.load(root, root, source_path, "change_request")
        if source.get("kind") == "issue":
            live = issue_view(
                str(source.get("repo") or ""), int(source.get("number") or 0), root
            )
            source = {
                **source,
                "title": live.get("title"),
                "body": live.get("body"),
                "updated_at": live.get("updatedAt"),
            }
        scope, contents = wording.contract_wording_build_scope(
            root, "change_request", mode, change_request_input=source_path
        )
        return review.normalize_target(source, raw), scope, contents

    def prerequisite_projections(root: Path, payloads: Any, target: dict[str, Any], scope: dict[str, Any], contents: dict[str, str]):
        clarity_payload = payloads.get("clarity") if isinstance(payloads, dict) else None
        wording_payload = payloads.get("wording") if isinstance(payloads, dict) else None
        identity = clarity_payload.get("content_identity", {}) if isinstance(clarity_payload, dict) else {}
        wording_scope = wording_payload.get("scope", {}) if isinstance(wording_payload, dict) else {}
        wording_scan = wording_payload.get("scan", {}) if isinstance(wording_payload, dict) else {}
        result = {
            "clarity": {"status": "current", "schema_id": "guru-requirements-clarification-2.0", "typed_exit": "clear", "payload_sha256": review.digest(clarity_payload), "facts_sha256": identity.get("result_sha256"), "target_sha256": identity.get("target_sha256"), "disposition_sha256": identity.get("disposition_sha256"), "content_sha256": target["content_sha256"], "scope_sha256": identity.get("scope_sha256"), "error_codes": []},
            "wording": {"status": "current", "schema_id": "guru-contract-wording-review-1.0", "profile": "change_request", "typed_exit": "pass", "payload_sha256": review.digest(wording_payload), "facts_sha256": wording_payload.get("facts_sha256"), "scope_sha256": wording_scope.get("scope_sha256"), "scan_sha256": wording_scan.get("scan_sha256"), "target_content_sha256": target["content_sha256"], "error_codes": []},
        }
        return review.normalize_prerequisites(result, target)

    module.issue_view = issue_view
    module.change_request_review_scope_hashes = scope_hashes
    module.change_request_review_request_authority_projection = authority_projection
    module.change_request_review_normalize_target = normalize_target
    module.change_request_review_prerequisite_projections = prerequisite_projections
    module.change_request_review_linkage = review.linkage
    module.change_request_review_derive_result = (
        lambda target, prerequisites, linked, authored: review.build_result(
            authored, target, prerequisites
        )
    )


def compose_review_branch_eval_runtime(runtime_target: Path, module: Any) -> None:
    publication = load_package_owner_runtime(
        runtime_target, "guru-review-task-publication"
    )
    module.load_config = publication.load_config
    module.WorkflowError = publication.WorkflowError
    module.read_json = publication.read_json
    module.write_json = publication.write_json
    module.write_runtime_mappings = publication.write_runtime_mappings
    module.current_head = publication.current_head
    module.git_status_paths = publication.git_status_paths
    module.diff_base_ref = publication.diff_base_ref
    module.INDEPENDENT_REVIEW_SOURCE = "independent-agent"

    def changed_files(root: Path, diff_range: str) -> list[str]:
        output = subprocess.run(
            ["git", "diff", "--name-only", "-z", diff_range],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout.decode("utf-8")
        return [path for path in output.split("\0") if path]

    module.changed_files = changed_files

    def commit_review_fixture(
        fixture: Path, task: Path, checked: dict[str, Any]
    ) -> tuple[str, str]:
        del checked
        run_git(fixture, "add", "-A")
        run_git(fixture, "commit", "-q", "-m", "commit reviewed production fixture")
        phase2 = (
            fixture
            / ".trellis/.runtime/guru-team/owner-checkpoints"
            / task.name
            / "phase2-check.json"
        )
        phase2.unlink(missing_ok=True)
        return run_git(fixture, "rev-parse", "HEAD"), "origin/main"

    module.commit_review_fixture = commit_review_fixture
    compose_production_owner_command_runtime(runtime_target, module)


def compose_production_owner_command_runtime(
    runtime_target: Path, module: Any,
) -> None:
    package_root = runtime_target.parent.parent.parent / "skills/packages"

    def run_component(skill_id: str, script: str, argv: list[str]) -> dict[str, Any]:
        process = subprocess.run(
            [str(package_root / skill_id / "scripts" / script), *argv, "--json"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if process.returncode != 0:
            raise ValueError(process.stderr.strip() or process.stdout.strip())
        value = json.loads(process.stdout)
        if not isinstance(value, dict):
            raise ValueError("package wrapper did not return one JSON object")
        return value

    bindings = {
        "cmd_record_planning_approval": lambda args: run_component(
            "guru-approve-task-plan",
            "record-planning-approval.sh",
            ["--root", str(args.root), "--task", str(args.task), "--input", str(args.input)],
        ),
        "cmd_check_planning_approval": lambda args: run_component(
            "guru-approve-task-plan",
            "check-planning-approval.sh",
            ["--root", str(args.root), "--task", str(args.task)],
        ),
        "cmd_record_phase2_check": lambda args: run_component(
            "guru-check-task",
            "record-phase2-check.sh",
            ["--root", str(args.root), "--task", str(args.task), "--input", str(args.input)],
        ),
        "cmd_check_phase2_check": lambda args: run_component(
            "guru-check-task",
            "check-phase2-check.sh",
            ["--root", str(args.root), "--task", str(args.task)],
        ),
        "cmd_review_branch": lambda args: run_component(
            "guru-review-branch",
            "review-branch.sh",
            [
                "--root", str(args.root), "--task", str(args.task),
                "--skill-input", str(args.skill_input),
                "--semantic-review-file", str(args.semantic_review_file),
                "--typed-exit", str(args.typed_exit),
            ],
        ),
        "cmd_check_review_gate": lambda args: run_component(
            "guru-review-branch",
            "check-review-gate.sh",
            [
                "--root", str(args.root), "--task", str(args.task),
                "--expected-exit", str(args.expected_exit),
            ],
        ),
    }
    for name, binding in bindings.items():
        if not hasattr(module, name):
            setattr(module, name, binding)


def compose_production_fixture_runtime(runtime_target: Path, module: Any) -> None:
    helper_names = ("load_config", "write_json", "write_runtime_mappings")
    missing = [name for name in helper_names if not hasattr(module, name)]
    if not missing:
        return
    publication = load_package_owner_runtime(
        runtime_target, "guru-review-task-publication"
    )
    for name in missing:
        setattr(module, name, getattr(publication, name))


def compose_task_workspace_eval_runtime(runtime_target: Path, module: Any) -> None:
    compose_change_request_eval_runtime(runtime_target, module)
    record = load_package_runtime_module(
        runtime_target, "guru-create-task-workspace", "record"
    )
    execute = load_package_runtime_module(
        runtime_target, "guru-create-task-workspace", "execute"
    )
    check = load_package_runtime_module(
        runtime_target, "guru-create-task-workspace", "check"
    )
    package_root = (
        runtime_target.parent.parent.parent
        / "skills/packages/guru-create-task-workspace"
    )
    module.context_digest = module.digest
    module.TASK_WORKSPACE_ARTIFACT_NAMES = ("issue-scope-ledger.json",)
    module.task_workspace_reviewable_projection = module.reviewable
    module.task_workspace_plan_digest = module.plan_digest

    def scope_digest(value: dict[str, Any]) -> str:
        projection = copy.deepcopy(value)
        projection.pop("scope_sha256", None)
        return module.digest(projection)

    def prerequisite_projection(
        key: str, artifact: str, payload: dict[str, Any], payload_sha256: str
    ) -> dict[str, Any]:
        identities = {
            "base": ("guru-sync-base", "guru-base-sync-result-1.0", "synced"),
            "clarity": ("guru-clarify-requirements", "guru-requirements-clarification-2.0", "clear"),
            "wording": ("guru-review-contract-wording", "guru-contract-wording-review-1.0", "pass"),
            "readiness": ("guru-review-change-request", "guru-change-request-review-1.0", "ready"),
        }
        skill_id, schema_id, typed_exit = identities[key]
        if key == "base":
            facts, content, linkage = payload.get("facts_sha256"), None, None
        elif key == "clarity":
            identity = payload.get("content_identity", {})
            facts, content, linkage = identity.get("result_sha256"), identity.get("content_sha256"), identity.get("context_sha256")
        elif key == "wording":
            facts = payload.get("facts_sha256")
            content = payload.get("scope", {}).get("scope_sha256")
            linkage = payload.get("scan", {}).get("scan_sha256")
        else:
            facts = payload.get("facts_sha256")
            content = payload.get("target", {}).get("content_sha256")
            linkage = payload.get("evidence_linkage", {}).get("linkage_sha256")
        return {"skill_id": skill_id, "schema_id": schema_id, "typed_exit": typed_exit,
                "artifact": artifact, "payload_sha256": payload_sha256,
                "facts_sha256": facts, "content_sha256": content,
                "linkage_sha256": linkage}

    def invoke(component: Any, args: argparse.Namespace) -> dict[str, Any]:
        argv = ["--root", str(args.root), "--invocation", "-"]
        return component.run(package_root, {}, argv)

    module.task_workspace_scope_digest = scope_digest
    module.task_workspace_prerequisite_projection = prerequisite_projection
    module.stage0_clarity_projection = lambda payload: {
        key: payload.get("content_identity", {}).get(key.replace("facts_sha256", "result_sha256"))
        for key in ("facts_sha256", "target_sha256", "disposition_sha256", "content_sha256", "scope_sha256")
    }
    module.stage0_wording_projection = lambda payload: {
        "facts_sha256": payload.get("facts_sha256"),
        "scope_sha256": payload.get("scope", {}).get("scope_sha256"),
        "scan_sha256": payload.get("scan", {}).get("scan_sha256"),
        "target_content_sha256": module.change_request_review_scope_hashes(
            payload.get("scope", {})
        )[2],
    }
    module.stage0_target_disposition_projection = lambda payload: {
        "disposition_sha256": payload.get("target_disposition", {}).get("disposition_digest"),
        "duplicate_facts_sha256": payload.get("target_disposition", {}).get("duplicate_facts_sha256"),
    }
    def readiness_target(target: dict[str, Any]) -> dict[str, Any]:
        common = {key: target.get(key) for key in (
            "kind", "repo", "title_sha256", "body_sha256",
            "identity_sha256", "content_sha256",
        )}
        if target.get("kind") == "existing_issue":
            return {**common, **{key: target.get(key) for key in ("issue_number", "url", "updated_at")}}
        if target.get("kind") == "proposed_draft":
            return {**common, **{key: target.get(key) for key in ("draft_id", "source_request_sha256")}}
        return {**common, **{key: target.get(key) for key in ("caller_locator", "request_id", "source_request_sha256")}}
    module.stage0_readiness_target_projection = readiness_target
    module.cmd_record_task_workspace_plan = lambda args: invoke(record, args)
    module.cmd_create_task_workspace = lambda args: invoke(execute, args)
    module.cmd_check_task_workspace_result = lambda args: invoke(check, args)


def derive_clarification_eval_result(runtime: Any, payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result["schema_version"] = "2.0"
    result["skill_id"] = "guru-clarify-requirements"
    actions = result.get("source_actions")
    actions = actions if isinstance(actions, list) else []
    for action in actions:
        if not isinstance(action, dict):
            continue
        action["payload_sha256"] = (
            runtime.digest(action["payload"])
            if isinstance(action.get("payload"), dict)
            else None
        )
        action["action_digest"] = runtime.digest({
            key: copy.deepcopy(action.get(key))
            for key in (
                "action_id", "kind", "target", "payload", "preimage_sha256",
                "payload_sha256",
            )
        })
    unsigned = copy.deepcopy(result)
    unsigned.pop("content_identity", None)
    content = {
        "confirmed_facts": result.get("confirmed_facts"),
        "repository_answerable_questions": result.get("repository_answerable_questions"),
        "clarification_rounds": result.get("clarification_rounds"),
        "open_questions": result.get("open_questions"),
        "affected_contracts": result.get("affected_contracts"),
        "reason": result.get("reason"),
    }
    result["content_identity"] = {
        "target_sha256": runtime.digest(result.get("review_target")),
        "disposition_sha256": runtime.digest(result.get("target_disposition")),
        "content_sha256": runtime.digest(content),
        "context_sha256": runtime.digest(result.get("context_evidence")),
        "scope_sha256": runtime.digest(result.get("scope_proposals")),
        "action_sha256": runtime.digest(actions),
        "payload_sha256": runtime.digest([
            action.get("payload") if isinstance(action, dict) else None
            for action in actions
        ]),
        "result_sha256": runtime.digest(unsigned),
    }
    return result


def load_package_runtime_module(
    runtime_target: Path, skill_id: str, module_name: str,
) -> Any:
    runtime_path = (
        runtime_target.parent.parent.parent
        / "skills/packages"
        / skill_id
        / "runtime"
        / f"{module_name}.py"
    )
    if runtime_path.is_symlink() or not runtime_path.is_file():
        raise ValueError(f"package {module_name} runtime is unavailable")
    spec = importlib.util.spec_from_file_location(
        f"guru_team_eval_{skill_id.replace('-', '_')}_{module_name}", runtime_path
    )
    if spec is None or spec.loader is None:
        raise ValueError(f"package {module_name} runtime cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    previous_path = list(sys.path)
    previous = sys.dont_write_bytecode
    sys.path.insert(0, str(runtime_path.parent))
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = previous_path
        sys.dont_write_bytecode = previous
    return module


def run_git(root: Path, *arguments: str) -> str:
    process = subprocess.run(
        ["git", *arguments], cwd=root, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if process.returncode != 0:
        detail = process.stderr.strip()
        raise ValueError(f"owner staging git command failed: {' '.join(arguments)}: {detail}")
    return process.stdout.strip()


def commit_qualification_owner_fixture(root: Path) -> None:
    process = subprocess.run(
        ["git", "commit", "-q", "-m", "stage qualification production fixture"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={
            **os.environ,
            "GIT_AUTHOR_DATE": "2000-01-01T00:00:00Z",
            "GIT_COMMITTER_DATE": "2000-01-01T00:00:00Z",
        },
    )
    if process.returncode != 0:
        raise ValueError("qualification owner fixture commit failed")


def normalize_qualification_owner_extension(root: Path) -> None:
    extension_path = root / ".trellis/guru-team/extension.json"
    try:
        extension = json.loads(extension_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("qualification owner extension manifest is invalid") from exc
    if not isinstance(extension, dict) or not isinstance(extension.get("installed_at"), str):
        raise ValueError("qualification owner extension install identity is invalid")
    extension["installed_at"] = "2000-01-01T00:00:00Z"
    extension_path.write_text(
        json.dumps(extension, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def owner_recipe(request: dict[str, Any]) -> tuple[str, Path, dict[str, Any]]:
    workdir = Path(request["workdir"]).resolve()
    recipe: str | None = None
    public_input: Path | None = None
    owner_staging: dict[str, Any] | None = None
    for relative in request.get("files", []):
        path = workdir / str(relative)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        staging = payload.get("owner_staging")
        if isinstance(staging, dict):
            candidate = staging.get("recipe")
            if not isinstance(candidate, str) or not candidate:
                raise ValueError("owner staging recipe is invalid")
            if recipe is not None:
                raise ValueError("multiple case files declare owner staging recipes")
            recipe = candidate
            owner_staging = copy.deepcopy(staging)
        if payload.get("profile") and payload.get("mode"):
            if public_input is not None:
                raise ValueError("multiple case files declare public inputs")
            public_input = path
    if recipe is None or public_input is None or owner_staging is None:
        raise ValueError("semantic case does not declare one owner staging recipe and public input")
    return recipe, public_input, owner_staging


def bind_owner_result_argument(
    request: dict[str, Any],
    fixture: Path,
    owner_result: Path | str,
) -> str:
    result_path = Path(owner_result).resolve()
    try:
        result_relative = result_path.relative_to(fixture.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError("owner result must stay inside the installed eval fixture") from exc
    if result_path.is_symlink() or not result_path.is_file():
        raise ValueError("owner result is unavailable or unsafe")

    workdir = Path(request["workdir"]).resolve()
    rewritten = 0
    for relative in request.get("files", []):
        path = workdir / str(relative)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        invocation = payload.get("public_invocation")
        arguments = invocation.get("arguments") if isinstance(invocation, dict) else None
        if not isinstance(arguments, list) or "--owner-result" not in arguments:
            continue
        index = arguments.index("--owner-result")
        if index + 1 >= len(arguments) or not isinstance(arguments[index + 1], str):
            raise ValueError("case owner-result invocation argument is invalid")
        arguments[index + 1] = result_relative
        path.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
        rewritten += 1
    if rewritten != 1:
        raise ValueError("semantic case must declare one owner-result invocation argument")
    return result_relative


def stage0_eval_hash(label: str, *values: Any) -> str:
    payload = json.dumps(
        [label, *values], sort_keys=True, separators=(",", ":"), default=str
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def stage0_contract_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def stage0_eval_base(fixture: Path) -> dict[str, Any]:
    head = run_git(fixture, "rev-parse", "HEAD")
    return {
        "source": "explicit",
        "selected_base": "main",
        "remote": "origin",
        "ordered_candidates": ["main"],
        "decision_head": head,
        "local_base_head": head,
        "remote_base_head": head,
        "post_sync_resolution_sha256": stage0_eval_hash(
            "base-current", "explicit", "main", "origin", head
        ),
    }


def stage0_eval_transition(
    skill_id: str,
    fixture: Path,
    public_input: dict[str, Any],
    owner_result: dict[str, Any],
    owner_plan: dict[str, Any] | None = None,
    owner_prerequisites: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any] | None:
    if (
        skill_id == "guru-review-contract-wording"
        and public_input.get("profile") in {"planning_artifacts", "explicit_paths"}
    ):
        return None
    mode = str(public_input.get("mode") or owner_result.get("mode") or "workflow")
    continuation = str(public_input.get("continuation_id") or "stage0-current")
    target = str(public_input.get("target_locator") or "")
    base = stage0_eval_base(fixture)
    common = {
        "schema_version": "1.0",
        "mode": mode,
        "repo_locator": (
            str(fixture.resolve())
            if skill_id == "guru-discover-change-context"
            else "example/guru-extension"
        ),
        "base": base,
    }
    context_digest = stage0_eval_hash("context", target, continuation, base)
    clarity_digest = stage0_eval_hash("clarity", target, continuation, owner_result)
    wording_digest = stage0_eval_hash("wording", target, continuation, owner_result)
    content_digest = stage0_eval_hash("target-content", target)
    stage_by_skill = {
        "guru-discover-change-context": "base_current",
        "guru-clarify-requirements": "context_current",
        "guru-review-contract-wording": "clarity_current",
        "guru-review-change-request": "wording_current",
        "guru-create-task-workspace": "readiness_current",
    }
    stage = stage_by_skill.get(skill_id)
    if skill_id == "guru-review-change-request":
        stage = {
            "clarify_requirements": "context_current",
            "review_wording": "clarity_current",
        }.get(str(owner_result.get("typed_exit") or ""), "wording_current")
    if stage is None:
        raise ValueError(f"call-local transition is not declared for {skill_id}")
    transition = {
        **common,
        "stage": stage,
    }
    if stage == "base_current":
        identity = transition["base"]["post_sync_resolution_sha256"]
        transition["transition_id"] = f"{stage}:{identity[:24]}"
        return transition
    if stage == "clarity_current":
        scope = owner_result.get("scope") if isinstance(owner_result.get("scope"), dict) else {}
        scope_identity = str(scope.get("identity") or "")
        if scope_identity:
            target = scope_identity.removeprefix("change_request:")
        content_digest = str(scope.get("scope_sha256") or content_digest)
        for item in scope.get("items", []):
            if isinstance(item, dict) and item.get("field") == "body":
                content_digest = str(item.get("content_sha256") or content_digest)
                break
    elif stage == "wording_current":
        owner_target = owner_result.get("target") if isinstance(owner_result.get("target"), dict) else {}
        target = str(
            owner_target.get("url")
            or (
                f"draft:{owner_target['draft_id']}"
                if isinstance(owner_target.get("draft_id"), str)
                and owner_target.get("draft_id")
                else public_input.get("target_locator")
                or target
            )
        )
        prerequisites = owner_result.get("prerequisites") if isinstance(owner_result.get("prerequisites"), dict) else {}
        clarity = prerequisites.get("clarity") if isinstance(prerequisites.get("clarity"), dict) else {}
        wording = prerequisites.get("wording") if isinstance(prerequisites.get("wording"), dict) else {}
        clarity_digest = str(clarity.get("facts_sha256") or clarity_digest)
        wording_digest = str(wording.get("facts_sha256") or wording_digest)
        content_digest = str(owner_target.get("content_sha256") or content_digest)
    elif stage == "readiness_current" and isinstance(owner_plan, dict):
        plan_target = owner_plan.get("target") if isinstance(owner_plan.get("target"), dict) else {}
        target = str(plan_target.get("url") or target)
        prerequisites = owner_plan.get("prerequisites") if isinstance(owner_plan.get("prerequisites"), dict) else {}
        clarity = prerequisites.get("clarity") if isinstance(prerequisites.get("clarity"), dict) else {}
        wording = prerequisites.get("wording") if isinstance(prerequisites.get("wording"), dict) else {}
        readiness = prerequisites.get("readiness") if isinstance(prerequisites.get("readiness"), dict) else {}
        clarity_digest = str(clarity.get("facts_sha256") or clarity_digest)
        wording_digest = str(wording.get("facts_sha256") or wording_digest)
        runtime = load_package_owner_runtime(
            fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh",
            "guru-create-task-workspace",
        )
        content_digest = runtime.context_digest({
            "title_sha256": plan_target.get("title_sha256"),
            "body_sha256": plan_target.get("body_sha256"),
        })
        readiness_digest = str(
            readiness.get("facts_sha256")
            or stage0_eval_hash("readiness", target, owner_result)
        )
        readiness_linkage = str(
            readiness.get("linkage_sha256")
            or stage0_eval_hash("readiness-linkage", target, owner_result)
        )
        plan_base = owner_plan.get("base") if isinstance(owner_plan.get("base"), dict) else {}
        transition["base"] = {
            **base,
            "selected_base": plan_base.get("selected_base"),
            "remote": plan_base.get("remote"),
            "decision_head": plan_base.get("decision_head"),
            "local_base_head": plan_base.get("local_head"),
            "remote_base_head": plan_base.get("remote_head"),
            "post_sync_resolution_sha256": plan_base.get(
                "post_sync_resolution_sha256"
            ),
        }
    transition.update({
        "target_locator": target,
        "continuation_id": continuation,
    })
    if stage == "context_current":
        transition["context_result_sha256"] = context_digest
        target_value = owner_result.get("review_target")
        target_value = target_value if isinstance(target_value, dict) else {}
        transition["authority_content_sha256"] = str(
            target_value.get("body_sha256") or content_digest
        )
    elif stage == "clarity_current":
        transition.update({
            "context_result_sha256": context_digest,
            "clarity_result_sha256": clarity_digest,
            "target_content_sha256": content_digest,
            "clarity": {
                "facts_sha256": clarity_digest,
                "target_sha256": stage0_eval_hash("clarity-target", target),
                "disposition_sha256": stage0_eval_hash("clarity-disposition", target),
                "content_sha256": stage0_eval_hash("clarity-content", target),
                "scope_sha256": stage0_eval_hash("clarity-scope", target),
            },
            "target_disposition": {
                "disposition_sha256": stage0_eval_hash("clarity-disposition", target),
                "duplicate_facts_sha256": stage0_eval_hash("clarity-duplicates", target),
            },
        })
    elif stage == "wording_current":
        prerequisites = owner_result.get("prerequisites")
        prerequisites = prerequisites if isinstance(prerequisites, dict) else {}
        clarity_projection = prerequisites.get("clarity")
        clarity_projection = clarity_projection if isinstance(clarity_projection, dict) else {}
        wording_projection = prerequisites.get("wording")
        wording_projection = wording_projection if isinstance(wording_projection, dict) else {}
        transition.update({
            "context_result_sha256": context_digest,
            "clarity_result_sha256": clarity_digest,
            "wording_facts_sha256": wording_digest,
            "target_content_sha256": content_digest,
            "clarity": {
                "facts_sha256": clarity_projection.get("facts_sha256") or clarity_digest,
                "target_sha256": clarity_projection.get("target_sha256") or stage0_eval_hash("clarity-target", target),
                "disposition_sha256": clarity_projection.get("disposition_sha256") or stage0_eval_hash("clarity-disposition", target),
                "content_sha256": clarity_projection.get("content_sha256") or stage0_eval_hash("clarity-content", target),
                "scope_sha256": clarity_projection.get("scope_sha256") or stage0_eval_hash("clarity-scope", target),
            },
            "wording": {
                "facts_sha256": wording_projection.get("facts_sha256") or wording_digest,
                "scope_sha256": wording_projection.get("scope_sha256") or stage0_eval_hash("wording-scope", target),
                "scan_sha256": wording_projection.get("scan_sha256") or stage0_eval_hash("wording-scan", target),
                "target_content_sha256": wording_projection.get("target_content_sha256") or content_digest,
            },
            "target_disposition": {
                "disposition_sha256": clarity_projection.get("disposition_sha256") or stage0_eval_hash("clarity-disposition", target),
                "duplicate_facts_sha256": stage0_eval_hash("clarity-duplicates", target),
            },
        })
    else:
        prerequisite_payloads = owner_prerequisites or {}
        readiness_payload = prerequisite_payloads.get("readiness")
        readiness_payload = readiness_payload if isinstance(readiness_payload, dict) else {}
        clarity_payload = prerequisite_payloads.get("clarity")
        clarity_payload = clarity_payload if isinstance(clarity_payload, dict) else {}
        wording_payload = prerequisite_payloads.get("wording")
        wording_payload = wording_payload if isinstance(wording_payload, dict) else {}
        runtime = load_package_owner_runtime(
            fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh",
            "guru-create-task-workspace",
        )
        readiness_target = readiness_payload.get("target")
        readiness_target = readiness_target if isinstance(readiness_target, dict) else {}
        readiness_semantic = readiness_payload.get("semantic_review")
        readiness_semantic = readiness_semantic if isinstance(readiness_semantic, dict) else {}
        scope_conclusion = readiness_semantic.get("scope_conclusion")
        scope_conclusion = scope_conclusion if isinstance(scope_conclusion, dict) else {}
        clarity_compact = runtime.stage0_clarity_projection(clarity_payload)
        wording_compact = runtime.stage0_wording_projection(wording_payload)
        disposition_compact = runtime.stage0_target_disposition_projection(clarity_payload)
        transition.update({
            "clarity_result_sha256": clarity_digest,
            "wording_facts_sha256": wording_digest,
            "readiness_facts_sha256": (
                readiness_digest
                if stage == "readiness_current" and isinstance(owner_plan, dict)
                else stage0_eval_hash("readiness", target, owner_result)
            ),
            "readiness_linkage_sha256": (
                readiness_linkage
                if stage == "readiness_current" and isinstance(owner_plan, dict)
                else stage0_eval_hash("readiness-linkage", target, owner_result)
            ),
            "target_content_sha256": content_digest,
            "clarity": clarity_compact,
            "wording": wording_compact,
            "readiness": {
                "payload_sha256": runtime.context_digest(readiness_payload),
                "facts_sha256": readiness_payload.get("facts_sha256"),
                "content_sha256": readiness_target.get("content_sha256"),
                "linkage_sha256": (readiness_payload.get("evidence_linkage") or {}).get("linkage_sha256"),
            },
            "target": runtime.stage0_readiness_target_projection(readiness_target),
            "target_disposition": disposition_compact,
            "scope": {
                "close_issues": copy.deepcopy(scope_conclusion.get("close_issues") or []),
                "related_issues": copy.deepcopy(scope_conclusion.get("related_issues") or []),
                "followup_issues": copy.deepcopy(scope_conclusion.get("followup_issues") or []),
            },
        })
    identity_field = {
        "context_current": "context_result_sha256",
        "clarity_current": "clarity_result_sha256",
        "wording_current": "wording_facts_sha256",
        "readiness_current": "readiness_facts_sha256",
    }[stage]
    transition["transition_id"] = f"{stage}:{transition[identity_field][:24]}"
    return transition


def bind_stage0_call_local_invocation(
    request: dict[str, Any],
    fixture: Path,
    public_input: dict[str, Any],
    owner_result: dict[str, Any],
    owner_context: dict[str, Any],
) -> None:
    skill_id = str(request["skill_id"])
    public_input = copy.deepcopy(public_input)
    if skill_id == "guru-review-contract-wording" and public_input.get("mode") == "workflow":
        scope = owner_result.get("scope") if isinstance(owner_result.get("scope"), dict) else {}
        scope_identity = str(scope.get("identity") or "")
        if scope_identity.startswith("change_request:"):
            public_input["target_locator"] = scope_identity.removeprefix(
                "change_request:"
            )
    elif skill_id == "guru-review-change-request" and public_input.get("mode") == "workflow":
        target = owner_result.get("target") if isinstance(owner_result.get("target"), dict) else {}
        if isinstance(target.get("url"), str) and target.get("url"):
            public_input["target_locator"] = target["url"]
        elif isinstance(target.get("draft_id"), str) and target.get("draft_id"):
            public_input["target_locator"] = f"draft:{target['draft_id']}"
    envelope: dict[str, Any] = {
        "schema_version": "1.0",
        "public_input": public_input,
        "owner_result": owner_result,
    }
    if skill_id == "guru-review-contract-wording":
        receipt = {
            "schema_version": "1.0",
            "skill_id": skill_id,
            "operation": "check-contract-wording-review",
            "result_sha256": owner_result["facts_sha256"],
            "prerequisite_sha256": stage0_contract_digest({"profile": owner_result["profile"], "mode": owner_result["mode"]}),
            "snapshot_sha256": stage0_contract_digest({"scope": owner_result["scope"], "scan": owner_result["scan"]}),
        }
        receipt["receipt_sha256"] = stage0_contract_digest(receipt)
        envelope["validation_receipt"] = receipt
    elif skill_id == "guru-review-change-request":
        receipt = {
            "schema_version": "1.0",
            "skill_id": skill_id,
            "operation": "check-change-request-review",
            "result_sha256": owner_result["facts_sha256"],
            "prerequisite_sha256": stage0_contract_digest(owner_result["prerequisites"]),
            "snapshot_sha256": stage0_contract_digest(owner_result["target"]),
        }
        receipt["receipt_sha256"] = stage0_contract_digest(receipt)
        envelope["validation_receipt"] = receipt
    if skill_id == "guru-create-task-workspace":
        workspace_state = WORKSPACE_CALL_LOCAL_STATE.get(str(fixture.resolve()))
        if workspace_state is None:
            raise ValueError("workspace call-local owner state is unavailable")
        envelope["owner_plan"] = copy.deepcopy(workspace_state[0])
    else:
        envelope["owner_context"] = copy.deepcopy(owner_context)
    transition = stage0_eval_transition(
        skill_id,
        fixture,
        public_input,
        owner_result,
        envelope.get("owner_plan"),
        (
            workspace_state[1]
            if skill_id == "guru-create-task-workspace"
            else None
        ),
    )
    if transition is not None:
        envelope["transition"] = transition
    exit_id = str(owner_result.get("typed_exit") or "")
    if skill_id == "guru-clarify-requirements":
        example = next(
            (fixture / ".trellis/guru-team/skills/packages" / skill_id / "examples").glob(
                f"public-{exit_id.replace('_', '-')}-output*.json"
            )
        )
        typed_output = json.loads(example.read_text(encoding="utf-8"))
        if exit_id == "clear":
            typed_output["resume_target"] = str(
                (owner_result.get("invocation_context") or {}).get("resume_target")
                or typed_output["resume_target"]
            )
            typed_output["continuation_id"] = public_input["continuation_id"]
            identity = owner_result["content_identity"]
            disposition = owner_result.get("target_disposition") or {}
            typed_output["transition"] = {
                **transition,
                "stage": "clarity_current",
                "clarity_result_sha256": identity["result_sha256"],
                "target_content_sha256": identity["content_sha256"],
                "clarity": {
                    "facts_sha256": identity["result_sha256"],
                    "target_sha256": identity["target_sha256"],
                    "disposition_sha256": identity["disposition_sha256"],
                    "content_sha256": identity["content_sha256"],
                    "scope_sha256": identity["scope_sha256"],
                },
                "target_disposition": {
                    "disposition_sha256": disposition.get("disposition_digest"),
                    "duplicate_facts_sha256": disposition.get("duplicate_facts_sha256"),
                },
            }
            typed_output["transition"]["transition_id"] = (
                f"clarity_current:{identity['result_sha256'][:24]}"
            )
            typed_output["transition"].pop("authority_content_sha256", None)
        elif exit_id == "needs_context":
            typed_output["handoff_mode"] = public_input["mode"]
            typed_output["handoff_repo_locator"] = "."
            typed_output["handoff_continuation_id"] = public_input["continuation_id"]
            typed_output["transition"] = {
                "schema_version": "1.0",
                "transition_id": f"base_current:{transition['base']['post_sync_resolution_sha256'][:24]}",
                "stage": "base_current",
                "mode": public_input["mode"],
                "repo_locator": ".",
                "base": transition["base"],
            }
        elif exit_id in {"refresh_context", "retarget_context"}:
            typed_output["handoff_mode"] = public_input["mode"]
            typed_output["handoff_repo_root"] = "."
        elif exit_id == "new_task":
            typed_output["target_locator"] = public_input["target_locator"]
            typed_output["continuation_id"] = public_input["continuation_id"]
        envelope["typed_output"] = typed_output
    invocation_path = fixture / OWNER_INVOCATION
    invocation_path.write_text(json.dumps(envelope) + "\n", encoding="utf-8")

    workdir = Path(request["workdir"]).resolve()
    matched = 0
    for relative in request.get("files", []):
        path = workdir / str(relative)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        invocation = payload.get("public_invocation") if isinstance(payload, dict) else None
        if not isinstance(invocation, dict):
            continue
        if invocation.get("arguments") != ["--invocation", "-"]:
            raise ValueError("Phase 0 eval must invoke exactly --invocation -")
        matched += 1
    if matched != 1:
        raise ValueError("Phase 0 eval must declare one call-local invocation")


def bind_sync_call_local_invocation(
    request: dict[str, Any], fixture: Path
) -> None:
    route_by_case = {
        "synced-route": ("main", "repo_change"),
        "skipped-route": (None, "original_request"),
        "blocked-route": ("missing-stage0-eval-base", "repo_change"),
    }
    selected = route_by_case.get(str(request.get("case_id") or ""))
    if selected is None:
        raise ValueError("unsupported sync-base call-local eval case")
    base_branch, route = selected
    public_input: dict[str, Any] = {
        "source_exit": "start",
        "mode": "workflow",
        "repo_root": ".",
        "route": route,
    }
    if base_branch is not None:
        public_input["base_branch"] = base_branch
    invocation_path = fixture / OWNER_INVOCATION
    invocation_path.parent.mkdir(parents=True, exist_ok=True)
    invocation_path.write_text(json.dumps({
        "schema_version": "1.0",
        "public_input": public_input,
    }) + "\n", encoding="utf-8")

    workdir = Path(request["workdir"]).resolve()
    matched = 0
    for relative in request.get("files", []):
        path = workdir / str(relative)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        invocation = payload.get("public_invocation") if isinstance(payload, dict) else None
        if not isinstance(invocation, dict):
            continue
        if invocation.get("arguments") != ["--invocation", "-"]:
            raise ValueError("sync-base eval must invoke exactly --invocation -")
        matched += 1
    if matched != 1:
        raise ValueError("sync-base eval must declare one call-local invocation")


def bind_merge_gate_argument(
    request: dict[str, Any],
    fixture: Path,
    gate_path: Path,
) -> str:
    try:
        gate_relative = gate_path.resolve().relative_to(fixture.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError("merge gate must stay inside the installed eval fixture") from exc
    if gate_path.is_symlink() or not gate_path.is_file():
        raise ValueError("merge gate is unavailable or unsafe")

    workdir = Path(request["workdir"]).resolve()
    rewritten = 0
    for relative in request.get("files", []):
        path = workdir / str(relative)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        invocation = payload.get("public_invocation")
        arguments = invocation.get("arguments") if isinstance(invocation, dict) else None
        if not isinstance(arguments, list) or "--gate" not in arguments:
            continue
        index = arguments.index("--gate")
        if index + 1 >= len(arguments) or not isinstance(arguments[index + 1], str):
            raise ValueError("case merge-gate invocation argument is invalid")
        arguments[index + 1] = gate_relative
        path.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
        rewritten += 1
    if rewritten != 1:
        raise ValueError("semantic merge case must declare one gate invocation argument")
    return gate_relative


def stage_clean_installed_owner_repo(
    execution_root: Path, runtime_target: Path, request_package: Path,
) -> tuple[Path, Path]:
    fixture = execution_root / "owner-repo"
    source_repo = runtime_target.parents[4]
    source_scripts = source_repo / ".trellis/scripts"
    source_workflow = source_repo / ".trellis/workflow.md"
    apply_script = source_repo / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"
    if (
        source_scripts.is_symlink() or not source_scripts.is_dir()
        or source_workflow.is_symlink() or not source_workflow.is_file()
    ):
        raise ValueError("installed Trellis inputs are unavailable for owner staging")
    (fixture / ".trellis").mkdir(parents=True)
    shutil.copytree(
        source_scripts, fixture / ".trellis/scripts",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    shutil.copy2(source_workflow, fixture / ".trellis/workflow.md")
    (fixture / ".gitignore").write_text(
        ".trellis/.runtime/\n__pycache__/\n*.py[cod]\n",
        encoding="utf-8",
    )
    run_git(fixture, "init", "-q", "-b", "main")
    run_git(fixture, "config", "user.email", "stage0-eval@example.invalid")
    run_git(fixture, "config", "user.name", "Stage0 Eval")
    canonical_packages = source_repo / "trellis/skills/guru-team/packages"
    try:
        request_package.relative_to(canonical_packages)
        source_mode = True
    except ValueError:
        source_mode = False
    if source_mode:
        if apply_script.is_symlink() or not apply_script.is_file():
            raise ValueError("canonical preset inputs are unavailable for owner staging")
        canonical_workflow = source_repo / "trellis/workflows/guru-team/workflow.md"
        if canonical_workflow.is_symlink() or not canonical_workflow.is_file():
            raise ValueError("canonical workflow input is unavailable for owner staging")
        shutil.copy2(canonical_workflow, fixture / ".trellis/workflow.md")
        applied = subprocess.run(
            [sys.executable, str(apply_script), "--repo", str(fixture), "--all-platforms"],
            cwd=source_repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if applied.returncode != 0:
            raise ValueError("canonical preset apply failed during owner staging")
    else:
        installed_root = source_repo / ".trellis/guru-team"
        extension_path = installed_root / "extension.json"
        try:
            extension = json.loads(extension_path.read_text(encoding="utf-8"))
            skill_packages = extension["skill_packages"]
            files = skill_packages["files"]
            overlays = extension["overlays"]
            overlay_files = overlays["files"]
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("installed Skill and overlay provenance is unavailable") from exc
        if (
            not isinstance(skill_packages, dict)
            or skill_packages.get("status") != "ok"
            or skill_packages.get("conflicts") != []
            or skill_packages.get("sidecars") != []
            or not isinstance(files, list)
            or not isinstance(overlays, dict)
            or overlays.get("status") != "ok"
            or overlays.get("conflicts") != []
            or overlays.get("sidecars") != []
            or not isinstance(overlay_files, list)
            or installed_root.is_symlink() or not installed_root.is_dir()
        ):
            raise ValueError("installed Skill and overlay provenance is not reusable")
        shutil.copytree(
            installed_root, fixture / ".trellis/guru-team", dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        copied_paths: set[str] = set()
        for row in [*files, *overlay_files]:
            if not isinstance(row, dict) or not isinstance(row.get("path"), str):
                raise ValueError("installed Skill or overlay file provenance is invalid")
            relative = Path(row["path"])
            relative_text = relative.as_posix()
            if (
                relative.is_absolute()
                or not relative.parts
                or ".." in relative.parts
                or relative_text in copied_paths
            ):
                raise ValueError("installed Skill or overlay file provenance path is unsafe")
            copied_paths.add(relative_text)
            source = source_repo / relative
            target = fixture / relative
            expected_sha256 = row.get("sha256")
            if (
                source.is_symlink() or not source.is_file()
                or not isinstance(expected_sha256, str)
                or hashlib.sha256(source.read_bytes()).hexdigest() != expected_sha256
            ):
                raise ValueError("installed Skill or overlay provenance does not match live bytes")
            if relative.parts[:3] == (".trellis", "guru-team", "skills"):
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        runtime_assets = fixture / ".trellis/guru-team/runtime"
        bootstrap = runtime_assets / "bootstrap.py"
        if bootstrap.is_symlink() or not bootstrap.is_file():
            raise ValueError("installed managed runtime bootstrap is unavailable")
        runtime = subprocess.run(
            [
                sys.executable,
                str(bootstrap),
                "--repo",
                str(fixture),
                "--runtime-assets",
                str(runtime_assets),
                "--python",
                sys.executable,
                "--json",
            ],
            cwd=fixture,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if runtime.returncode != 0:
            raise ValueError("installed managed runtime bootstrap failed during owner staging")
    return fixture, source_repo


def write_fake_gh(execution_root: Path, recipe: str) -> Path:
    binary = execution_root / "owner-bin"
    binary.mkdir(parents=True, exist_ok=True)
    target = binary / "gh"
    issue_145_state = "CLOSED" if recipe == "clarity-new-task" else "OPEN"
    workspace_recipe = recipe.startswith("workspace-")
    issue_title = (
        "Stage 0 workspace owner staging"
        if workspace_recipe else "Issue 145 owner staging"
    )
    issue_body = (
        "The current Intake workflow is one independently deliverable unit."
        if workspace_recipe else "Issue 145 owner staging body"
    )
    issue_assignees = [{"login": "stage0-eval"}] if workspace_recipe else []
    target.write_text(
        MANAGED_PYTHON_SHEBANG
        +
        "import json,sys\n"
        f"states={{145:{issue_145_state!r},146:'OPEN'}}\n"
        f"titles={{145:{issue_title!r},146:'Issue 146 owner staging'}}\n"
        f"bodies={{145:{issue_body!r},146:'Issue 146 owner staging body'}}\n"
        f"assignees={{145:{issue_assignees!r},146:[]}}\n"
        "args=sys.argv[1:]\n"
        "if args[:2]==['auth','status']:\n"
        " raise SystemExit(0)\n"
        "if args[:2]==['api','user']:\n"
        " print(json.dumps({'login':'stage0-eval'})); raise SystemExit(0)\n"
        "if len(args)>=3 and args[:2]==['issue','view']:\n"
        " number=int(args[2]); state=states.get(number,'OPEN')\n"
        " title=titles.get(number,f'Issue {number} owner staging'); body=bodies.get(number,f'Issue {number} owner staging body')\n"
        " print(json.dumps({'number':number,'url':f'https://github.com/example/guru-extension/issues/{number}',"
        "'state':state,'updatedAt':'2026-01-01T00:00:00Z','title':title,'body':body,"
        "'comments':[],'assignees':assignees.get(number,[]),'labels':[]}))\n"
        " raise SystemExit(0)\n"
        "print('unsupported fake gh invocation',file=sys.stderr); raise SystemExit(2)\n",
        encoding="utf-8",
    )
    target.chmod(0o755)
    real_git = shutil.which("git")
    if real_git is None:
        raise ValueError("git is unavailable for owner staging")
    git_target = binary / "git"
    git_target.write_text(
        MANAGED_PYTHON_SHEBANG
        +
        "import os,subprocess,sys\n"
        f"real_git={real_git!r}\n"
        f"workspace_recipe={workspace_recipe!r}\n"
        "args=sys.argv[1:]\n"
        "if args and args[0]=='fetch': raise SystemExit(0)\n"
        "if workspace_recipe and args==['ls-remote','--heads','origin','main']:\n"
        " head=subprocess.run([real_git,'rev-parse','--verify','refs/remotes/origin/main'],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)\n"
        " if head.returncode!=0: raise SystemExit(head.returncode)\n"
        " print(f'{head.stdout.strip()}\\trefs/heads/main'); raise SystemExit(0)\n"
        "os.execv(real_git,[real_git,*args])\n",
        encoding="utf-8",
    )
    git_target.chmod(0o755)
    return binary


def write_fake_merge_gh(
    execution_root: Path,
    recipe: str,
    *,
    repo_ref: str = "castbox/guru-trellis",
    pr_number: int = 176,
    issue_number: int = 174,
    head_sha: str | None = None,
    base_branch: str | None = None,
    head_branch: str | None = None,
) -> Path:
    configurations = {
        "merge-workflow-merged": {
            "draft": False,
            "head": "1" * 40,
            "merge_state_status": "CLEAN",
            "body": "Closes #174\n",
            "closure_mismatch": False,
        },
        "merge-standalone-draft-blocked": {
            "draft": True,
            "head": "1" * 40,
            "merge_state_status": "BLOCKED",
            "body": "Closes #174\n",
            "closure_mismatch": False,
        },
        "merge-workflow-head-drift-blocked": {
            "draft": False,
            "head": "3" * 40,
            "merge_state_status": "CLEAN",
            "body": "Closes #174\n",
            "closure_mismatch": False,
        },
        "merge-workflow-branch-drift-blocked": {
            "draft": False,
            "head": "1" * 40,
            "merge_state_status": "CLEAN",
            "base_branch": "release",
            "head_branch": "codex/other-task",
            "body": "Closes #174\n",
            "closure_mismatch": False,
        },
        "merge-workflow-added-close-scope-blocked": {
            "draft": False,
            "head": "1" * 40,
            "merge_state_status": "CLEAN",
            "body": "Closes #174\nCloses #180\n",
            "closure_mismatch": False,
        },
        "merge-workflow-close-scope-blocked": {
            "draft": False,
            "head": "1" * 40,
            "merge_state_status": "CLEAN",
            "body": "Related #174\n",
            "closure_mismatch": False,
        },
        "merge-workflow-closure-mismatch": {
            "draft": False,
            "head": "1" * 40,
            "merge_state_status": "CLEAN",
            "body": "Closes #174\n",
            "closure_mismatch": True,
        },
    }
    configuration = copy.deepcopy(configurations.get(recipe))
    if configuration is None:
        raise ValueError(f"unsupported merge owner staging recipe: {recipe}")
    if head_sha is not None:
        configuration["head"] = head_sha
    if base_branch is not None:
        configuration["base_branch"] = base_branch
    if head_branch is not None:
        configuration["head_branch"] = head_branch
    binary = execution_root / "merge-owner-bin"
    binary.mkdir(parents=True, exist_ok=True)
    state_path = binary / "state.json"
    state_path.write_text(
        json.dumps({"merged": False, "calls": []}) + "\n",
        encoding="utf-8",
    )
    target = binary / "gh"
    target.write_text(
        MANAGED_PYTHON_SHEBANG
        +
        "import json,sys\n"
        "from pathlib import Path\n"
        f"state_path={str(state_path)!r}\n"
        f"config={configuration!r}\n"
        f"repo={repo_ref!r}; number={pr_number!r}; issue_number={issue_number!r}\n"
        "base_head='0'*40; merge_sha='2'*40\n"
        "args=sys.argv[1:]\n"
        "state=json.load(open(state_path,encoding='utf-8'))\n"
        "state.setdefault('calls',[]).append(args)\n"
        "open(state_path,'w',encoding='utf-8').write(json.dumps(state)+'\\n')\n"
        "pr_url=f'https://github.com/{repo}/pull/{number}'\n"
        "issue_url=f'https://github.com/{repo}/issues/{issue_number}'\n"
        "if args==['auth','status']:\n"
        " raise SystemExit(0)\n"
        "if len(args)>=2 and args[:2]==['pr','view']:\n"
        " payload={'number':number,'url':pr_url,'state':'MERGED' if state['merged'] else 'OPEN',"
        "'isDraft':config['draft'],'baseRefName':config.get('base_branch','main'),"
        "'headRefName':config.get('head_branch','codex/180-eval'),"
        "'headRefOid':config['head'],'mergeable':'MERGEABLE',"
        "'mergeStateStatus':config['merge_state_status'],'reviewDecision':'APPROVED',"
        "'statusCheckRollup':[{'name':'contract','conclusion':'SUCCESS'}],'body':config['body'],"
        "'mergedAt':'2026-08-05T06:21:00Z' if state['merged'] else None,"
        "'mergeCommit':{'oid':'2'*40} if state['merged'] else None}\n"
        " print(json.dumps(payload)); raise SystemExit(0)\n"
        "if args[:2]==['api',f'repos/{repo}']:\n"
        " print(json.dumps({'full_name':repo,'allow_merge_commit':True,'allow_squash_merge':False,'allow_rebase_merge':False})); raise SystemExit(0)\n"
        "if len(args)>=2 and args[0]=='api' and args[1].startswith(f'repos/{repo}/git/ref/heads/'):\n"
        " branch_ref=args[1].split('/git/ref/heads/',1)[1]\n"
        " current=merge_sha if state['merged'] else base_head\n"
        " print(json.dumps({'ref':f'refs/heads/{branch_ref}','object':{'sha':current}})); raise SystemExit(0)\n"
        "if args[:2]==['api',f'repos/{repo}/git/commits/{merge_sha}']:\n"
        " commit=state.get('commit')\n"
        " if not commit: raise SystemExit(2)\n"
        " print(json.dumps(commit,ensure_ascii=False)); raise SystemExit(0)\n"
        "if len(args)>=3 and args[:2]==['issue','view']:\n"
        " closed=state['merged'] and not config['closure_mismatch']\n"
        " print(json.dumps({'number':issue_number,'state':'CLOSED' if closed else 'OPEN',"
        "'closedAt':'2026-08-05T06:21:05Z' if closed else None,'url':issue_url})); raise SystemExit(0)\n"
        "if len(args)>=3 and args[:2]==['pr','merge']:\n"
        " expected=args[args.index('--match-head-commit')+1] if '--match-head-commit' in args else ''\n"
        " subject=args[args.index('--subject')+1] if '--subject' in args else ''\n"
        " body_file=args[args.index('--body-file')+1] if '--body-file' in args else ''\n"
        " body=Path(body_file).read_text(encoding='utf-8') if body_file else ''\n"
        " if expected!=config['head'] or config['draft'] or not config['body'].startswith('Closes #') or '--merge' not in args or not subject.startswith('chore(merge): #') or not body:\n"
        "  print('merge precondition failed',file=sys.stderr); raise SystemExit(1)\n"
        " state['merged']=True\n"
        " state['commit']={'sha':merge_sha,'message':subject+'\\n\\n'+body,'parents':[{'sha':base_head},{'sha':config['head']}]}\n"
        " open(state_path,'w',encoding='utf-8').write(json.dumps(state)+'\\n')\n"
        " raise SystemExit(0)\n"
        "print('unsupported merge fake gh invocation: '+repr(args),file=sys.stderr); raise SystemExit(2)\n",
        encoding="utf-8",
    )
    target.chmod(0o755)
    return binary


def with_path_prefix(binary: Path, callback: Any) -> Any:
    previous_path = os.environ.get("PATH")
    os.environ["PATH"] = f"{binary}{os.pathsep}{previous_path or ''}"
    try:
        return callback()
    finally:
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path


def clarity_target(
    runtime: Any,
    payload: dict[str, Any],
    *,
    state: str = "open",
    body: str = "Issue 145 owner staging body",
) -> dict[str, Any]:
    target = {
        "kind": "issue", "repo": "example/guru-extension", "issue_number": 145,
        "url": "https://github.com/example/guru-extension/issues/145", "state": state,
        "updated_at": "2026-01-01T00:00:00Z",
        "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
    }
    target["facts_sha256"] = runtime.context_digest(target)
    payload["invocation_context"] = {
        "kind": "initial_issue", "caller": "stage0 eval owner staging",
        "task_locator": None, "resume_target": "guru-review-contract-wording",
    }
    payload["review_target"] = target
    return payload


def clarity_disposition(
    runtime: Any,
    payload: dict[str, Any],
    disposition: str,
    *,
    candidates: list[dict[str, Any]] | None = None,
    selected_issue: dict[str, Any] | None = None,
    role: str = "primary",
) -> dict[str, Any]:
    payload["target_disposition"] = {
        "disposition": disposition,
        "duplicate_query": "repo:example/guru-extension is:issue is:open stage0 eval",
        "duplicate_checked_at": "2026-01-01T00:00:00Z",
        "duplicate_candidates": candidates or [], "duplicate_facts_sha256": "0" * 64,
        "selected_issue": selected_issue, "original_target_role": role,
        "decision_summary": f"The reviewed owner staging selected {disposition}.",
        "disposition_digest": "0" * 64,
    }
    return runtime.derive_requirements_clarification_result(payload)


def clarity_finalize(runtime: Any, payload: dict[str, Any]) -> dict[str, Any]:
    return runtime.derive_requirements_clarification_result(payload)


def build_clarity_owner(runtime: Any, package_root: Path, recipe: str) -> dict[str, Any]:
    payload = json.loads(
        (package_root / "examples/requirements-clarification.json").read_text(encoding="utf-8")
    )
    if recipe == "clarity-clear":
        return runtime.derive_requirements_clarification_result(payload)

    payload["mode"] = "workflow"
    if recipe == "clarity-needs-context":
        payload["typed_exit"] = "needs_context"
        payload["consumer"] = {"kind": "skill", "id": "guru-discover-change-context"}
        payload["context_evidence"] = {
            "status": "missing", "evidence_refs": ["repository.current_owner"],
            "missing_reason": "The current repository owner evidence is unavailable.",
        }
        payload["reason"] = "A named repository fact is required before clarification can continue."
        return runtime.derive_requirements_clarification_result(payload)
    if recipe == "clarity-refresh-context":
        payload["mode"] = "standalone"
        payload["typed_exit"] = "refresh_context"
        payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
        payload["context_evidence"]["status"] = "stale"
        payload["context_evidence"]["missing_reason"] = "The reviewed source binding changed."
        payload["reason"] = "The context snapshot must be refreshed from current authority."
        return runtime.derive_requirements_clarification_result(payload)
    if recipe == "clarity-blocked":
        payload = clarity_target(runtime, payload)
        payload = clarity_disposition(runtime, payload, "keep_current_open_issue")
        payload["typed_exit"] = "blocked"
        payload["consumer"] = {"kind": "stop", "id": "requirements-clarification-blocked"}
        payload["ai_review_gate"]["status"] = "blocked"
        payload["error"] = {
            "codes": ["load_bearing_decision_unresolved"],
            "summary": "A load-bearing requirement decision remains unresolved.",
        }
        payload["reason"] = "The unresolved load-bearing decision blocks the clarification loop."
        return runtime.derive_requirements_clarification_result(payload)
    if recipe == "clarity-retarget":
        payload = clarity_target(runtime, payload)
        projection = {
            "repo": "example/guru-extension", "number": 146, "identity": "#146",
            "url": "https://github.com/example/guru-extension/issues/146", "state": "open",
            "updated_at": "2026-01-01T00:00:00Z",
        }
        candidate = {
            **projection, "facts_sha256": runtime.context_digest(projection),
            "decision": "selected", "reason": "The current duplicate is the selected target.",
        }
        selected = {
            "repo": candidate["repo"], "issue_number": candidate["number"],
            "url": candidate["url"], "state": candidate["state"],
            "updated_at": candidate["updated_at"], "facts_sha256": candidate["facts_sha256"],
        }
        payload["typed_exit"] = "retarget_context"
        payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
        payload["source_actions"] = [{
            "action_id": "select_existing", "kind": "select_existing_issue",
            "target": {"repo": candidate["repo"], "issue_number": candidate["number"]},
            "payload": selected, "preimage_sha256": payload["review_target"]["facts_sha256"],
            "payload_sha256": None, "action_digest": "0" * 64, "status": "validated",
            "mutation_evidence": None,
        }]
        payload = clarity_disposition(
            runtime, payload, "retarget_existing_issue", candidates=[candidate],
            selected_issue=selected, role="related",
        )
        return clarity_finalize(runtime, payload)
    if recipe == "clarity-new-task":
        payload = clarity_target(runtime, payload, state="closed")
        payload["typed_exit"] = "new_task"
        payload["consumer"] = {"kind": "workflow", "id": "guru-full-task-intake-chain"}
        payload["source_actions"] = [{
            "action_id": "new_issue", "kind": "new_issue_draft",
            "target": {"repo": "example/guru-extension"},
            "payload": {"title": "Independent Stage 0 follow-up", "body": "Reviewed independent delivery scope."},
            "preimage_sha256": None, "payload_sha256": None, "action_digest": "0" * 64,
            "status": "draft_ready", "mutation_evidence": None,
        }]
        payload = clarity_disposition(
            runtime, payload, "create_followup_draft", role="related",
        )
        return clarity_finalize(runtime, payload)
    raise ValueError(f"unsupported clarification owner staging recipe: {recipe}")


def build_workflow_mode_owner(
    public_input: dict[str, Any], recipe: str,
) -> dict[str, Any]:
    exits = {
        "workflow-mode-explicit-task-free": "task_free",
        "workflow-mode-automatic-high-confidence": "task_free",
        "workflow-mode-insufficient-confirmed": "task_free",
        "workflow-mode-insufficient-refused": "standard_intake",
        "workflow-mode-complex-request": "standard_intake",
        "workflow-mode-simple-issue": "task_free",
        "workflow-mode-insufficient-issue-confirmed": "task_free",
        "workflow-mode-complex-issue": "standard_intake",
        "workflow-mode-same-file-count-low-risk": "task_free",
        "workflow-mode-same-file-count-high-risk": "standard_intake",
        "workflow-mode-non-default-checkout": "task_free",
        "workflow-mode-active-task-same-scope": "task_free",
        "workflow-mode-active-task-scope-expansion": "task_free",
        "workflow-mode-unrelated-worktree": "task_free",
        "workflow-mode-dirty-overlap": "task_free",
        "workflow-mode-position-evidence-insufficient": "task_free",
        "workflow-mode-unrelated-dirty": "task_free",
        "workflow-mode-repeated-turn": "task_free",
        "workflow-mode-automatic-risk-expansion": "standard_intake",
        "workflow-mode-explicit-risk-expansion": "task_free",
        "workflow-mode-blocked": "blocked",
    }
    typed_exit = exits.get(recipe)
    if typed_exit is None:
        raise ValueError(f"unsupported workflow mode owner staging recipe: {recipe}")
    owner = {
        "schema_version": "1.0",
        "typed_exit": typed_exit,
        "mode": public_input["mode"],
        "continuation_id": public_input["continuation_id"],
    }
    if typed_exit != "blocked":
        owner["selection"] = typed_exit
    return owner


def build_task_free_change_owner(
    public_input: dict[str, Any], recipe: str,
) -> dict[str, Any]:
    route = {
        "task-free-completed": ("completed", "suitable"),
        "task-free-non-default-completed": ("completed", "suitable"),
        "task-free-resume-active-task": ("resume_active_task", "resume_active_task"),
        "task-free-scope-change": ("scope_change", "scope_change"),
        "task-free-location-unrelated-worktree": ("location_required", "location_required"),
        "task-free-location-dirty-overlap": ("location_required", "location_required"),
        "task-free-location-insufficient": ("location_required", "location_required"),
        "task-free-automatic-risk-expansion": ("reselect_mode", "suitable"),
        "task-free-explicit-risk-expansion": ("explicit_choice_required", "suitable"),
        "task-free-blocked": ("blocked", "blocked"),
    }.get(recipe)
    if route is None:
        raise ValueError(f"unsupported task-free owner staging recipe: {recipe}")
    typed_exit, prewrite_status = route
    owner: dict[str, Any] = {
        "schema_version": "1.0",
        "typed_exit": typed_exit,
        "mode": public_input["mode"],
        "continuation_id": public_input["continuation_id"],
        "selection_origin": public_input["selection_origin"],
        "request_summary": public_input["request_summary"],
        "target_paths": public_input["target_paths"],
        "pre_write_review": {
            "status": prewrite_status,
            "summary": "The semantic owner reviewed current local checkout, active-task, dirty, and target-overlap facts before writing.",
        },
        "ai_review_gate": {
            "status": "blocked" if typed_exit == "blocked" else "passed",
            "summary": "The AI reviewed checkout suitability and the selected execution route from current facts.",
        },
    }
    if typed_exit == "completed":
        owner["completion_evidence"] = {
            "edited_paths": list(public_input["target_paths"]),
            "targeted_checks": [{
                "command": "git diff --check -- docs/guide.md",
                "summary": "The bounded documentation diff has no whitespace errors.",
                "status": "passed",
            }],
            "post_write_review": {
                "status": "passed",
                "summary": "The actual edit remained inside the selected paths and did not expand scope or risk.",
            },
            "unverified_boundaries": [
                "No full repository test suite was run for this documentation-only change."
            ],
        }
        owner["ai_review_gate"]["summary"] = "The AI reviewed pre-write suitability, the actual edit, targeted checks, and post-write scope/risk evolution."
    if typed_exit in {"reselect_mode", "explicit_choice_required"}:
        owner["evolution_evidence"] = {
            "write_state": "partial_edit",
            "edited_paths": [public_input["target_paths"][0]],
            "expansion": {
                "kind": "scope_and_risk",
                "summary": "The first bounded edit revealed public installation and contract impact outside task-free risk.",
            },
            "stop_after_detection": True,
            "remaining_writes_not_performed": [{
                "target_path": path,
                "summary": "The planned edit for this bounded target was not performed after expansion detection.",
            } for path in public_input["target_paths"][1:]],
            "targeted_checks": [{
                "command": "git diff --check -- docs/guide.md",
                "summary": "The partial bounded diff has no whitespace errors.",
                "status": "passed",
            }],
        }
        owner["ai_review_gate"]["summary"] = "The AI reviewed the actual partial edit, detected expanded scope and risk, and stopped all remaining writes."
    if typed_exit in {"resume_active_task", "scope_change"}:
        owner["task_ref"] = ".trellis/tasks/current"
    return owner


def build_context_owner(
    runtime: Any,
    fixture: Path,
    package_root: Path,
    recipe: str,
) -> dict[str, Any]:
    payload = json.loads(
        (package_root / "examples/change-context-owner-result-3.0.json").read_text(encoding="utf-8")
    )
    old_head = run_git(fixture, "rev-parse", "HEAD")
    payload["repository"] = {
        "repo": "example/guru-extension", "selected_base": "main", "decision_branch": "main",
    }
    payload["base_observation"] = {
        "repo": "example/guru-extension", "repo_locator": str(fixture.resolve()),
        "selected_base": "main", "remote": "origin", "authority_branch": "main",
        "decision_head": old_head, "local_head": old_head, "remote_head": old_head,
        "clean": True, "current": True,
    }
    payload["change_input"] = {
        "issue_refs": [], "pr_refs": [], "branches": [],
        "paths": ["docs/requirements.md"], "commands": [],
        "config_keys": [], "schema_fields": [], "symbols": [],
        "terms": ["change context"], "queries": [],
    }
    payload["live_change"]["issue_binding"] = None
    body_sha256 = hashlib.sha256(b"Stage 0 context owner staging draft").hexdigest()
    live_unsigned = {
        "kind": "draft", "identity": f"draft:{body_sha256}", "state": "draft",
        "updated_at": "2026-01-01T00:00:00Z", "body_sha256": body_sha256,
    }
    payload["live_change"] = {
        **live_unsigned, "facts_sha256": runtime.digest(live_unsigned), "issue_binding": None,
    }
    evidence_paths = {
        "docs": "docs/requirements.md",
        "code_contracts": "trellis/runtime.py",
        "tests": "trellis/test_runtime.py",
    }
    for group, path in evidence_paths.items():
        rows = payload["current_state"][group]
        rows[0]["path"] = path
        rows[0]["blob_or_content_sha256"] = run_git(fixture, "rev-parse", f"HEAD:{path}")
    query = runtime.canonical_query(payload["change_input"])
    payload["canonical_query"] = query
    payload["history_preview"] = runtime.preview(fixture, payload["change_input"], 20)
    payload["history_review"] = {
        "selected_candidates": [], "excluded_candidates": [], "deep_reads": [],
    }
    payload["error"] = None
    payload["typed_exit"] = "context_ready"
    payload["ai_review_gate"]["status"] = "passed"
    payload["result_identity"] = runtime.identity(payload)
    if recipe == "context-ready":
        return payload
    if recipe == "context-blocked":
        payload["typed_exit"] = "blocked"
        payload["ai_review_gate"]["status"] = "blocked"
        payload["error"] = {
            "codes": ["semantic_review_blocked"],
            "summary": "A named load-bearing repository source could not be reviewed.",
        }
        payload["result_identity"] = runtime.identity(payload)
        return payload
    if recipe == "context-refresh-base":
        run_git(fixture, "commit", "--allow-empty", "-q", "-m", "advance context fixture")
        payload["typed_exit"] = "refresh_base"
        payload["result_identity"] = runtime.identity(payload)
        return payload
    raise ValueError(f"unsupported context owner staging recipe: {recipe}")


def workspace_base_fixture(runtime: Any, head: str) -> dict[str, Any]:
    """Retain the existing #250 workspace prerequisite until that owner migrates."""
    identity = {"schema_version":"1.0","skill_id":"guru-sync-base","status":"resolved","source":"explicit","selected_base":"main","remote":"origin","candidates":["main"],"decision_checkout":{"branch":"main","head":head,"clean":True}}
    resolution_sha256=runtime.digest(identity)
    value={"schema_version":"1.0","skill_id":"guru-sync-base","status":"synced","resolution":{"source":"explicit","selected_base":"main","remote":"origin","candidates":["main"],"resolution_sha256":resolution_sha256},"post_sync_resolution":identity,"post_sync_resolution_sha256":resolution_sha256,"decision_checkout":{"branch":"main","head_before":head,"head_after":head,"clean_before":True,"clean_after":True},"git":{"local_ref":"refs/heads/main","remote_ref":"refs/remotes/origin/main","local_head_before":head,"local_head_after":head,"remote_head_after":head,"fetch_performed":True,"fast_forwarded":False},"fresh":True}
    value["facts_sha256"]=runtime.digest(value);return value


def wording_review(
    runtime: Any,
    profile: str,
    mode: str,
    scope: dict[str, Any],
    scan: dict[str, Any],
    typed_exit: str,
) -> dict[str, Any]:
    passed = typed_exit != "blocked"
    revisions: list[dict[str, Any]] = []
    if typed_exit == "content_changed":
        item = scope["items"][0]
        revisions = [{
            "revision_id": "stage0-eval-revision", "locator": item["path"],
            "before_sha256": "0" * 64, "after_sha256": item["content_sha256"],
            "reason": "The completed planning wording revision is present in the current rescan.",
            "rescan_sha256": scan["scan_sha256"],
        }]
    gate: dict[str, Any] = {
        "status": "passed" if passed else "blocked", "reviewer": "stage0-eval-reviewer",
        "summary": "The complete fixed wording scope and current rescan were semantically reviewed.",
        "reviewed_scan_sha256": scan["scan_sha256"],
        "checked_dimensions": {
            key: passed for key in runtime.CONTRACT_WORDING_REVIEW_DIMENSIONS
        },
    }
    if profile == "planning_artifacts":
        gate["planning_checked_dimensions"] = {
            key: passed for key in runtime.CONTRACT_WORDING_PLANNING_REVIEW_DIMENSIONS
        }
    authored = {
        "generated_at": "2026-01-01T00:00:00Z",
        "semantic_review": {
            "revisions": revisions,
            "classifications": [{
                "hit_id": hit["hit_id"], "classification": "term_definition",
                "reason": "The semantic review retained this explicit contract term.",
            } for hit in scan["hits"]] if passed else [],
            "ai_review_gate": gate,
        },
        "typed_exit": typed_exit,
    }
    return runtime.contract_wording_derive_result(profile, mode, scope, scan, authored)


def build_wording_owner(
    runtime: Any, fixture: Path, package_root: Path, recipe: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    change_request = {
        "kind": "draft", "draft_id": "stage0-wording-eval",
        "title": "Review Stage 0 wording",
        "body": "The current change request defines one bounded delivery unit.",
        "selected_comments": [],
    }
    change_path = fixture / ".trellis/.runtime/guru-team/evals/change-request.json"
    change_path.write_text(json.dumps(change_request) + "\n", encoding="utf-8")
    if recipe == "wording-pass":
        profile, mode = "change_request", "workflow"
        scope, contents = runtime.contract_wording_build_scope(
            fixture, profile, mode,
            change_request_input=change_path.relative_to(fixture).as_posix(),
        )
        typed_exit = "pass"
    elif recipe == "wording-content-changed":
        profile, mode = "planning_artifacts", "workflow"
        task = fixture / ".trellis/tasks/current"
        scope, contents = runtime.contract_wording_build_scope(
            fixture, profile, mode, task_dir=task,
        )
        typed_exit = "content_changed"
    elif recipe == "wording-blocked":
        profile, mode = "explicit_paths", "standalone"
        scope, contents = runtime.contract_wording_build_scope(
            fixture, profile, mode,
            explicit_paths=["docs/requirements/requirement-main.md"],
        )
        typed_exit = "blocked"
    else:
        raise ValueError(f"unsupported wording owner staging recipe: {recipe}")
    scan = runtime.scan_contract_wording(scope, contents)
    return wording_review(runtime, profile, mode, scope, scan, typed_exit), change_request


def readiness_prerequisites(
    runtime: Any,
    fixture: Path,
    source: dict[str, Any],
    source_path: Path,
    mode: str,
) -> dict[str, dict[str, Any]]:
    if source.get("kind") == "issue":
        live = runtime.issue_view(
            str(source.get("repo") or ""), int(source.get("number") or 0), fixture
        )
        body_sha256 = hashlib.sha256(
            str(live.get("body") or "").encode("utf-8")
        ).hexdigest()
        invocation_kind = "initial_issue"
        authority = {
            "kind": "issue",
            "repo": source.get("repo"),
            "issue_number": source.get("number"),
            "url": live.get("url"),
            "state": str(live.get("state") or "").casefold(),
            "updated_at": live.get("updatedAt"),
            "body_sha256": body_sha256,
        }
        disposition = "keep_current_open_issue"
    else:
        body_sha256 = hashlib.sha256(source["body"].encode("utf-8")).hexdigest()
        invocation_kind = "proposed_draft"
        authority = {
            "kind": "draft", "repo": "example/guru-extension",
            "issue_number": None, "url": None, "state": "draft",
            "updated_at": None, "body_sha256": body_sha256,
        }
        disposition = "keep_current_draft"
    clarity_package = fixture / ".trellis/guru-team/skills/packages/guru-clarify-requirements"
    clarity = json.loads(
        (clarity_package / "examples/requirements-clarification.json").read_text(encoding="utf-8")
    )
    clarity["mode"] = mode
    clarity["invocation_context"] = {
        "kind": invocation_kind, "caller": "stage0 readiness eval",
        "task_locator": None, "resume_target": "guru-review-contract-wording",
    }
    clarity["review_target"] = {**authority, "facts_sha256": runtime.context_digest(authority)}
    clarity["target_disposition"] = {
        "disposition": disposition,
        "duplicate_query": "repo:example/guru-extension is:issue is:open readiness eval",
        "duplicate_checked_at": "2026-01-01T00:00:00Z", "duplicate_candidates": [],
        "duplicate_facts_sha256": "0" * 64, "selected_issue": None,
        "original_target_role": "primary",
        "decision_summary": "No current duplicate replaces the reviewed draft.",
        "disposition_digest": "0" * 64,
    }
    clarity["context_evidence"] = {
        "status": "current",
        "evidence_refs": ["live-authority:stage0-readiness-eval"],
        "missing_reason": None,
    }
    clarity = runtime.derive_requirements_clarification_result(clarity)

    scope, contents = runtime.contract_wording_build_scope(
        fixture, "change_request", mode,
        change_request_input=source_path.relative_to(fixture).as_posix(),
    )
    scan = runtime.scan_contract_wording(scope, contents)
    wording = wording_review(runtime, "change_request", mode, scope, scan, "pass")
    return {"clarity": clarity, "wording": wording}


def readiness_semantic_review(
    runtime: Any, target: dict[str, Any], linkage: dict[str, Any], typed_exit: str,
) -> dict[str, Any]:
    non_ready = typed_exit != "ready"
    finding_id = "stage0-readiness-finding"
    category = {
        "clarify_requirements": "requirement_gap",
        "review_wording": "wording_gap",
        "refresh_context": "context_stale",
        "blocked": "target_complete",
    }.get(typed_exit, "requirement_gap")
    finding = {
        "finding_id": finding_id, "category": category,
        "summary": "The reviewed evidence requires the declared prerequisite route.",
        "blocking": True, "evidence_refs": ["target"],
        "affected_hashes": [target["content_sha256"]],
        "route_basis": "The semantic review selected the owner of the identified gap.",
    }
    dimensions = [{
        "id": dimension_id, "status": "failed" if non_ready and index == 0 else "passed",
        "summary": "This readiness dimension was reviewed against current linked evidence.",
        "evidence_refs": ["target"], "affected_hashes": [target["content_sha256"]],
        "finding_ids": [finding_id] if non_ready and index == 0 else [],
    } for index, dimension_id in enumerate(runtime.CHANGE_REQUEST_REVIEW_DIMENSIONS)]
    scope_conclusion = {
        "requirement_scope_basis": "The reviewed draft and current prerequisites define the scope.",
        "delivery_unit_id": "stage0-readiness-eval", "close_issues": [],
        "related_issues": [], "followup_issues": [],
        "duplicate_reuse_decision": "No duplicate replaces this delivery unit.",
        "implementation_target": "The Stage 0 minimal handoff package graph.",
        "current_gap": "The selected route identifies the next readiness owner.",
        "archived_constraints": [], "risk_boundary": ["Normal honest workflow operation only."],
        "excluded_scope": ["Workspace mutation remains downstream."],
    }
    return {
        "dimensions": dimensions, "findings": [finding] if non_ready else [],
        "scope_conclusion": scope_conclusion,
        "ai_review_gate": {
            "status": runtime.CHANGE_REQUEST_REVIEW_GATE_BY_EXIT[typed_exit],
            "reviewer": "stage0-eval-reviewer",
            "reviewed_linkage_sha256": linkage["linkage_sha256"],
            "summary": "The complete readiness evidence was reviewed for one declared route.",
            "findings_count": 1 if non_ready else 0,
            "scope_conclusion_sha256": runtime.context_digest(scope_conclusion),
        },
    }


def build_readiness_owner(
    runtime: Any,
    fixture: Path,
    package_root: Path,
    recipe: str,
    mode: str,
    profile: str,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]]:
    route_by_recipe = {
        "readiness-ready": "ready",
        "readiness-clarify": "clarify_requirements",
        "readiness-wording": "review_wording",
        "readiness-refresh": "refresh_context",
        "readiness-blocked": "blocked",
    }
    typed_exit = route_by_recipe.get(recipe)
    if typed_exit is None:
        raise ValueError(f"unsupported readiness owner staging recipe: {recipe}")
    repo = "example/guru-extension"
    request_id = "stage0-readiness-eval"
    if profile == "current_issue":
        issue = runtime.issue_view(repo, 145, fixture)
        source = {
            "kind": "issue",
            "repo": repo,
            "number": 145,
            "selected_comments": [],
        }
    elif profile in {"proposed_draft", "standalone_request"}:
        issue = None
        source = {
            "kind": "draft", "draft_id": request_id,
            "title": "Review Stage 0 readiness",
            "body": "The current Intake workflow is one independently deliverable unit.",
            "selected_comments": [],
        }
    else:
        raise ValueError(f"unsupported readiness input profile: {profile}")
    source_path = fixture / ".trellis/.runtime/guru-team/evals/change-request.json"
    source_path.write_text(json.dumps(source) + "\n", encoding="utf-8")
    prerequisites = readiness_prerequisites(
        runtime, fixture, source, source_path, mode
    )
    scope, _ = runtime.contract_wording_build_scope(
        fixture, "change_request", mode,
        change_request_input=source_path.relative_to(fixture).as_posix(),
    )
    title_sha256, body_sha256, _ = runtime.change_request_review_scope_hashes(scope)
    if profile == "current_issue":
        raw_target = {
            "kind": "existing_issue",
            "repo": repo,
            "issue_number": 145,
            "url": issue.get("url") if isinstance(issue, dict) else None,
            "updated_at": issue.get("updatedAt") if isinstance(issue, dict) else None,
            "title_sha256": title_sha256,
            "body_sha256": body_sha256,
        }
    else:
        source_request_sha256 = runtime.context_digest(
            runtime.change_request_review_request_authority_projection(
                repo, source, body_sha256
            )
        )
        raw_target = {
            "kind": profile,
            "repo": repo,
            "source_request_sha256": source_request_sha256,
            "title_sha256": title_sha256,
            "body_sha256": body_sha256,
            "side_effect_free": True,
            **(
                {"draft_id": request_id}
                if profile == "proposed_draft"
                else {
                    "caller_locator": "stage0-eval",
                    "request_id": request_id,
                }
            ),
        }
    target, scope, contents = runtime.change_request_review_normalize_target(
        fixture, raw_target, source_path.relative_to(fixture).as_posix(), mode,
    )
    projections = runtime.change_request_review_prerequisite_projections(
        fixture, prerequisites, target, scope, contents,
    )
    linkage = runtime.change_request_review_linkage(target, projections)
    authored = {
        "generated_at": "2026-01-01T00:00:00Z", "mode": mode,
        "target": raw_target, "prerequisite_payloads": prerequisites,
        "semantic_review": readiness_semantic_review(runtime, target, linkage, typed_exit),
        "typed_exit": typed_exit,
        "reason": "The semantic readiness review selected exactly one declared route.",
        "affected_evidence": [{
            "ref": "target", "sha256": target["content_sha256"],
            "summary": "The current reviewed change-request title and body.",
        }],
        "consumer": runtime.CHANGE_REQUEST_REVIEW_CONSUMERS[typed_exit],
    }
    result = runtime.change_request_review_derive_result(target, projections, linkage, authored)
    return result, prerequisites, source


def workspace_prerequisites(
    runtime: Any, fixture: Path, mode: str,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    repo = "example/guru-extension"
    issue_number = 145
    issue_url = f"https://github.com/{repo}/issues/{issue_number}"
    updated_at = "2026-01-01T00:00:00Z"
    title = "Stage 0 workspace owner staging"
    body = "The current Intake workflow is one independently deliverable unit."
    title_sha256 = hashlib.sha256(title.encode("utf-8")).hexdigest()
    body_sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()

    head = run_git(fixture, "rev-parse", "HEAD")
    base = workspace_base_fixture(runtime, head)
    clarity_package = fixture / ".trellis/guru-team/skills/packages/guru-clarify-requirements"
    clarity = json.loads(
        (clarity_package / "examples/requirements-clarification.json").read_text(encoding="utf-8")
    )
    clarity["mode"] = mode
    clarity["context_evidence"] = {
        "status": "current",
        "evidence_refs": ["live-authority:stage0-workspace-eval"],
        "missing_reason": None,
    }
    clarity = clarity_target(runtime, clarity, body=body)
    clarity = clarity_disposition(runtime, clarity, "keep_current_open_issue")

    source = {
        "kind": "issue", "repo": repo, "number": issue_number,
        "selected_comments": [],
    }
    source_path = fixture / ".trellis/.runtime/guru-team/evals/change-request.json"
    source_path.write_text(json.dumps(source) + "\n", encoding="utf-8")
    scope, contents = runtime.contract_wording_build_scope(
        fixture, "change_request", mode,
        change_request_input=source_path.relative_to(fixture).as_posix(),
    )
    scan = runtime.scan_contract_wording(scope, contents)
    wording = wording_review(runtime, "change_request", mode, scope, scan, "pass")

    raw_target = {
        "kind": "existing_issue", "repo": repo, "issue_number": issue_number,
        "url": issue_url, "updated_at": updated_at,
        "title_sha256": title_sha256, "body_sha256": body_sha256,
    }
    prerequisite_payloads = {"clarity": clarity, "wording": wording}
    target, normalized_scope, normalized_contents = runtime.change_request_review_normalize_target(
        fixture, raw_target, source_path.relative_to(fixture).as_posix(), mode,
    )
    projections = runtime.change_request_review_prerequisite_projections(
        fixture, prerequisite_payloads, target, normalized_scope, normalized_contents,
    )
    linkage = runtime.change_request_review_linkage(target, projections)
    semantic_review = readiness_semantic_review(runtime, target, linkage, "ready")
    semantic_review["scope_conclusion"]["close_issues"] = [issue_number]
    semantic_review["ai_review_gate"]["scope_conclusion_sha256"] = runtime.context_digest(
        semantic_review["scope_conclusion"]
    )
    authored = {
        "generated_at": "2026-01-01T00:00:00Z", "mode": mode,
        "target": raw_target, "prerequisite_payloads": prerequisite_payloads,
        "semantic_review": semantic_review,
        "typed_exit": "ready",
        "reason": "The complete existing-issue delivery unit passed semantic readiness review.",
        "affected_evidence": [{
            "ref": "target", "sha256": target["content_sha256"],
            "summary": "The current reviewed issue title and body.",
        }],
        "consumer": runtime.CHANGE_REQUEST_REVIEW_CONSUMERS["ready"],
    }
    readiness = runtime.change_request_review_derive_result(
        target, projections, linkage, authored
    )
    return {
        "base": base,
        "clarity": clarity,
        "wording": wording,
        "readiness": readiness,
    }, {
        "repo": repo, "issue_number": issue_number, "url": issue_url,
        "updated_at": updated_at, "title": title, "body": body,
        "title_sha256": title_sha256, "body_sha256": body_sha256,
    }


def workspace_plan(
    runtime: Any,
    fixture: Path,
    recipe: str,
    mode: str,
    prerequisites: dict[str, dict[str, Any]],
    issue: dict[str, Any],
) -> dict[str, Any]:
    projections: dict[str, dict[str, Any]] = {}
    for key, payload in prerequisites.items():
        projections[key] = runtime.task_workspace_prerequisite_projection(
            key, f"call-local:{key}", payload, runtime.context_digest(payload)
        )

    gate_status = {
        "workspace-created": "passed",
        "workspace-refresh-review": "reroute",
        "workspace-blocked": "blocked",
    }.get(recipe)
    if gate_status is None:
        raise ValueError(f"unsupported task workspace owner staging recipe: {recipe}")
    task_slug = "145-stage0-owner-eval"
    task_dir = f".trellis/tasks/{time.strftime('%m-%d')}-{task_slug}"
    scope_item = {
        "number": issue["issue_number"], "url": issue["url"],
        "title": issue["title"],
        "reason": "The reviewed Stage 0 delivery unit closes this exact issue.",
    }
    base_result = prerequisites["base"]
    naming_disposition = "conflict_blocked" if gate_status == "blocked" else "create_new"
    plan: dict[str, Any] = {
        "schema_version": "2.0", "skill_id": "guru-create-task-workspace",
        "generated_at": "2026-01-01T00:00:00Z", "mode": mode,
        "invocation": {
            "caller": "guru-review-change-request:ready", "target_kind": "existing_issue",
            "action_scope": "workspace_and_task_mutation",
            "resume_identity": "stage0-workspace-eval",
        },
        "prerequisites": projections,
        "target": {
            "kind": "existing_issue", "repo": issue["repo"],
            "issue_number": issue["issue_number"], "url": issue["url"],
            "state": "open", "updated_at": issue["updated_at"],
            "title_sha256": issue["title_sha256"], "body_sha256": issue["body_sha256"],
            "draft": None,
            "disposition_sha256": prerequisites["clarity"]["target_disposition"]["disposition_digest"],
            "duplicate_decision_sha256": prerequisites["clarity"]["target_disposition"]["duplicate_facts_sha256"],
            "created_issue_binding_sha256": None, "created_issue_result": None,
        },
        "scope": {
            "primary": scope_item, "close": [scope_item], "related": [], "followup": [],
            "scope_sha256": "0" * 64,
        },
        "base": {
            "selected_base": base_result["resolution"]["selected_base"],
            "remote": base_result["resolution"]["remote"],
            "base_ref": base_result["git"]["remote_ref"],
            "decision_head": base_result["decision_checkout"]["head_after"],
            "local_head": base_result["git"]["local_head_after"],
            "remote_head": base_result["git"]["remote_head_after"],
            "post_sync_resolution_sha256": base_result["post_sync_resolution_sha256"],
            "sync_facts_sha256": base_result["facts_sha256"],
        },
        "naming": {
            "branch_name": f"feat/{task_slug}", "workspace_slug": task_slug,
            "task_slug": task_slug, "task_title": "#145 Stage 0 owner eval",
            "reason": "Names bind the reviewed issue and isolated eval workspace.",
            "branch_disposition": naming_disposition,
            "workspace_disposition": naming_disposition,
            "task_disposition": naming_disposition,
        },
        "assignee": {
            "login": "stage0-eval", "source": "single_issue_assignee",
            "candidates": ["stage0-eval"],
            "resolution_evidence": "The live source issue has one exact assignee.",
        },
        "side_effects": {
            "operations": [
                "create_branch", "create_worktree", "create_task",
                "write_task_artifacts", "write_runtime_mappings",
            ],
            "task_artifacts": [
                f"{task_dir}/{name}" for name in runtime.TASK_WORKSPACE_ARTIFACT_NAMES
            ],
            "runtime_mappings": [
                f".trellis/.runtime/guru-team/workspaces/{task_slug}.json",
                f".trellis/.runtime/guru-team/tasks/{task_slug}.json",
            ],
            "command_argv": ["create-task-workspace", "--invocation", "-"],
            "stop_after": "created_workspace",
        },
        "ai_review_gate": {
            "status": gate_status, "reviewer": "stage0-eval-reviewer",
            "reviewed_plan_sha256": "0" * 64,
            "summary": "The exact target, names, assignee, scope and mutation boundary were reviewed.",
            "evidence": [
                "The invocation owns one isolated workspace and task.",
                "All durable artifacts are task-local and all runtime mappings are ignored.",
            ],
        },
        "freshness": {
            "captured_at": "2026-01-01T00:00:00Z",
            "reviewable_plan_sha256": "0" * 64, "plan_sha256": "0" * 64,
        },
    }
    plan["scope"]["scope_sha256"] = runtime.task_workspace_scope_digest(plan["scope"])
    reviewable = runtime.context_digest(runtime.task_workspace_reviewable_projection(plan))
    plan["ai_review_gate"]["reviewed_plan_sha256"] = reviewable
    plan["freshness"]["reviewable_plan_sha256"] = reviewable
    plan["freshness"]["plan_sha256"] = runtime.task_workspace_plan_digest(plan)
    return plan


def call_runtime_with_json(
    function: Any,
    args: argparse.Namespace,
    payload: dict[str, Any],
) -> dict[str, Any]:
    previous_stdin = sys.stdin
    sys.stdin = io.StringIO(json.dumps(payload))
    try:
        return function(args)
    finally:
        sys.stdin = previous_stdin


def build_workspace_owner(
    runtime: Any, fixture: Path, recipe: str, mode: str,
) -> dict[str, Any]:
    prerequisites, issue = workspace_prerequisites(runtime, fixture, mode)
    plan = workspace_plan(
        runtime, fixture, recipe, mode, prerequisites, issue
    )
    transition = stage0_eval_transition(
        "guru-create-task-workspace",
        fixture,
        {"profile": "execute_reviewed_plan", "mode": mode},
        prerequisites["readiness"],
        plan,
        prerequisites,
    )
    if not isinstance(transition, dict):
        raise ValueError("workspace readiness transition is unavailable")
    if transition.get("stage") != "readiness_current":
        raise ValueError("workspace readiness transition stage is invalid")
    transition_payloads = prerequisites
    plan["prerequisites"] = {
        key: runtime.task_workspace_prerequisite_projection(
            key,
            f"call-local:{key}",
            payload,
            runtime.context_digest(payload),
        )
        for key, payload in transition_payloads.items()
    }
    reviewable = runtime.context_digest(
        runtime.task_workspace_reviewable_projection(plan)
    )
    plan["ai_review_gate"]["reviewed_plan_sha256"] = reviewable
    plan["freshness"]["reviewable_plan_sha256"] = reviewable
    plan["freshness"]["plan_sha256"] = runtime.task_workspace_plan_digest(plan)
    WORKSPACE_CALL_LOCAL_STATE[str(fixture.resolve())] = (
        copy.deepcopy(plan),
        copy.deepcopy(prerequisites),
    )
    common = {
        "schema_version": "1.0",
        "plan": plan,
        "transition": transition,
    }
    call_runtime_with_json(
        runtime.cmd_record_task_workspace_plan,
        argparse.Namespace(root=str(fixture), input=None, invocation="-", plan_input=None),
        common,
    )
    result = call_runtime_with_json(
        runtime.cmd_create_task_workspace,
        argparse.Namespace(
            root=str(fixture), input=None, invocation="-", plan_input=None,
            refresh_review=recipe == "workspace-refresh-review",
            reason=None,
            reason_code=(
                "disposition_changed" if recipe == "workspace-refresh-review"
                else "object_conflict" if recipe == "workspace-blocked" else None
            ),
        ),
        common,
    )
    return call_runtime_with_json(
        runtime.cmd_check_task_workspace_result,
        argparse.Namespace(root=str(fixture), input=None, invocation="-", plan_input=None),
        {**common, "result": result},
    )


def production_task_fixture(runtime: Any, fixture: Path) -> tuple[Path, str]:
    (fixture / ".trellis/guru-team/config.yml").write_text(
        "workspace_mode: current\n", encoding="utf-8",
    )
    task = fixture / ".trellis/tasks/current"
    task.mkdir(parents=True, exist_ok=True)
    runtime.write_json(task / "task.json", {
        "id": "current",
        "name": "current",
        "title": "Production minimal handoff eval",
        "status": "planning",
        "scope": "issue #146",
        "branch": "eval/current",
        "base_branch": "main",
    })
    for name, content in {
        "prd.md": (
            "# PRD\n\n## R1. Production eval\n\n"
            "The production eval uses the public package boundary.\n"
        ),
        "design.md": (
            "# Design\n\n## Docs SSOT Plan\n\n"
            "Strategy: ssot_first. Durable requirements own the contract.\n"
        ),
        "implement.md": (
            "# Implement\n\nExecute the recorder, checker, and public wrapper.\n"
        ),
    }.items():
        (task / name).write_text(content, encoding="utf-8")
    issue = {
        "number": 146,
        "url": "https://github.com/example/guru-extension/issues/146",
        "title": "Production minimal handoff eval",
        "reason": "The current production eval delivery scope.",
    }
    runtime.write_json(task / "issue-scope-ledger.json", {
        "schema_version": "2.0",
        "primary_issue": issue,
        "close_issues": [issue],
        "related_issues": [],
        "followup_issues": [],
    })
    durable = fixture / "docs/requirements.md"
    durable.parent.mkdir(parents=True, exist_ok=True)
    durable.write_text(
        "# Requirements\n\nThe public wrapper owns the production eval boundary.\n",
        encoding="utf-8",
    )
    source = fixture / "src/production-eval.txt"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("baseline\n", encoding="utf-8")
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-q", "-m", "stage production owner fixture")
    base_head = run_git(fixture, "rev-parse", "HEAD")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", base_head)
    run_git(fixture, "remote", "add", "origin", "https://github.com/example/guru-extension.git")
    run_git(fixture, "checkout", "-q", "-b", "eval/current")
    runtime.write_runtime_mappings(
        fixture,
        runtime.load_config(fixture),
        {
            "workspace_slug": "current",
            "task_slug": "current",
            "task_dir": ".trellis/tasks/current",
            "branch_name": "eval/current",
        },
        fixture,
    )
    return task, base_head


def production_planning_input(
    runtime: Any, fixture: Path, task: Path, exit_id: str,
) -> Path:
    statuses = {
        "approved": "passed",
        "revision_required": "revision_required",
        "clarify_scope": "clarify_scope",
        "blocked": "blocked",
    }
    consumers = {
        "approved": {"kind": "workflow", "id": "phase-1-task-activation"},
        "revision_required": {"kind": "skill", "id": "guru-approve-task-plan"},
        "clarify_scope": {
            "kind": "workflow", "id": "guru-task-plan-clarify-scope-router",
        },
        "blocked": {"kind": "stop", "id": "task-plan-approval-blocked"},
    }
    status = statuses[exit_id]
    semantic_review = {
        "status": status,
        "summary": "The exact production planning case completed semantic review.",
        "checked_dimensions": {
            "requirement_authority": True,
            "scope_boundary": True,
            "design_adequacy": True,
            "implementation_plan": True,
            "acceptance_verifiability": True,
            "docs_ssot": True,
            "provenance": True,
            "unusual_scenarios": True,
        },
        "findings": [],
        "revision_actions": (
            ["Revise the task-local planning contract."]
            if exit_id == "revision_required" else []
        ),
        "scope_proposals": (
            ["scope-proposal:R13"] if exit_id == "clarify_scope" else []
        ),
        "blocking_reasons": (
            ["The required planning authority is unavailable."]
            if exit_id == "blocked" else []
        ),
    }
    payload = {
        "mode": "workflow",
        "authority_refs": ["issue:146"],
        "docs_ssot_plan": {
            "strategy": "ssot_first",
            "durable_paths": ["docs/requirements.md"],
            "summary": "The durable requirement is the implementation source of truth.",
        },
        "semantic_review": semantic_review,
        "typed_exit": exit_id,
        "consumer": consumers[exit_id],
        "reason": f"Production planning eval selected {exit_id}.",
    }
    path = fixture / ".trellis/.runtime/guru-team/evals/planning-owner-input.json"
    runtime.write_json(path, payload)
    return path


def production_record_planning(
    runtime: Any, fixture: Path, task: Path, exit_id: str,
) -> dict[str, Any]:
    input_path = production_planning_input(runtime, fixture, task, exit_id)
    runtime.cmd_record_planning_approval(argparse.Namespace(
        root=str(fixture),
        task=task.relative_to(fixture).as_posix(),
        input=input_path.relative_to(fixture).as_posix(),
        dry_run=False,
    ))
    return runtime.cmd_check_planning_approval(argparse.Namespace(
        root=str(fixture),
        task=task.relative_to(fixture).as_posix(),
        require_exit=None,
    ))


def production_phase2_input(
    runtime: Any, fixture: Path, task: Path, package: Path, exit_id: str,
) -> Path:
    del package
    task_payload = runtime.read_json(task / "task.json")
    base_ref = runtime.diff_base_ref(
        fixture,
        str(task_payload.get("base_branch") or "main"),
    )
    implementation_paths = set(runtime.changed_files(fixture, f"{base_ref}...HEAD"))
    implementation_paths.update(
        path
        for path in runtime.git_status_paths(fixture)
        if not path.startswith(".trellis/.runtime/")
    )
    dimensions = [
        {
            "id": dimension,
            "status": "passed",
            "summary": f"The production eval reviewed {dimension}.",
        }
        for dimension in (
            "requirements", "design", "implementation", "tests", "docs_ssot",
            "cross_layer", "compatibility", "deployment_and_operations",
            "verification_completeness",
        )
    ]
    scope_decisions: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    unverified_items: list[dict[str, Any]] = []
    candidate_classifications = [{
        "candidate_ref": "candidate:phase2:no-defect",
        "decision": "rejected_not_reproduced",
        "witness": {
            "requirement_refs": ["task:prd:R1"],
            "supported_entry_refs": ["entry:guru-check-task:phase2"],
            "existing_caller_refs": ["caller:production-phase2-eval"],
            "honest_action_sequence": [
                "run the installed Phase 2 owner through its supported entry",
            ],
            "defect_observation": (
                "The supported production eval path does not reproduce a task defect."
            ),
            "excluded_assumptions": [],
        },
        "consumer_use": "task_commit_preflight",
    }]
    route = None
    consumer = {
        "passed": {"kind": "skill", "id": "guru-create-task-commit"},
        "implementation_required": {"kind": "workflow", "id": "guru-resume-implementation"},
        "planning_stale": {"kind": "workflow", "id": "guru-task-check-planning-router"},
        "blocked": {"kind": "stop", "id": "task-check-blocked"},
    }[exit_id]
    if exit_id == "implementation_required":
        candidate_classifications = [{
            "candidate_ref": "candidate:phase2:defect",
            "decision": "qualified_current",
            "witness": {
                "requirement_refs": ["task:prd:R1"],
                "supported_entry_refs": ["entry:guru-check-task:phase2"],
                "existing_caller_refs": ["caller:production-phase2-eval"],
                "honest_action_sequence": [
                    "run the supported production Phase 2 implementation check",
                ],
                "defect_observation": (
                    "The current implementation defect is reproduced on the supported eval path."
                ),
                "excluded_assumptions": [],
            },
            "consumer_use": "task_commit_preflight",
        }]
        scope_decisions = [{
            "id": "C1",
            "candidate_ref": "candidate:phase2:defect",
            "disposition": "current_scope",
            "summary": "A current-scope implementation defect remains.",
            "finding_id": "F1",
        }]
        findings = [{
            "id": "F1", "candidate_ref": "candidate:phase2:defect", "severity": "P2",
            "summary": "The current implementation requires a fix.",
            "path": "src/production-eval.txt", "status": "open",
        }]
        next(item for item in dimensions if item["id"] == "implementation")["status"] = "failed"
    elif exit_id == "planning_stale":
        route = "reapprove_plan"
        candidate_classifications = [{
            "candidate_ref": "candidate:phase2:scope",
            "decision": "qualified_approved_expansion",
            "witness": {
                "requirement_refs": ["task:scope-expansion:R13"],
                "supported_entry_refs": ["entry:guru-check-task:phase2"],
                "existing_caller_refs": ["caller:production-phase2-eval"],
                "honest_action_sequence": [
                    "review the approved expansion against the current task plan",
                ],
                "defect_observation": (
                    "The approved expansion is not represented by the current task plan."
                ),
                "excluded_assumptions": [],
            },
            "consumer_use": "task_commit_preflight",
        }]
        scope_decisions = [{
            "id": "scope-proposal:R13",
            "candidate_ref": "candidate:phase2:scope",
            "disposition": "scope_change_required",
            "summary": "The approved scope requires a current authority decision.",
            "finding_id": None,
        }]
    elif exit_id == "blocked":
        unverified_items = [{
            "id": "U1",
            "summary": "The required integration dependency is unavailable.",
            "blocking": True,
        }]
        next(
            item for item in dimensions
            if item["id"] == "verification_completeness"
        )["status"] = "blocked"
    payload = {
        "mode": "workflow",
        "reviewed_paths": sorted(implementation_paths),
        "validation": {
            "commands": [{
                "id": "production-eval",
                "outcome": "passed",
                "summary": "The production owner fixture completed its applicable checks.",
            }],
            "unverified_items": unverified_items,
            "summary": "The production eval captured the applicable validation conclusion.",
        },
        "docs_ssot": {
            "status": "passed",
            "strategy": "ssot_first",
            "durable_paths": ["docs/requirements.md"],
            "summary": "The durable requirement was the implementation input.",
        },
        "candidate_classifications": candidate_classifications,
        "semantic_review": {
            "status": exit_id,
            "summary": f"The production Phase 2 owner selected {exit_id}.",
            "adequacy_dimensions": dimensions,
            "scope_decisions": scope_decisions,
            "findings": findings,
        },
        "typed_exit": exit_id,
        "route": route,
        "reason": f"Production Phase 2 eval selected {exit_id}.",
        "consumer": consumer,
    }
    path = fixture / ".trellis/.runtime/guru-team/evals/phase2-owner-input.json"
    runtime.write_json(path, payload)
    return path


def production_record_phase2(
    runtime: Any, fixture: Path, task: Path, package: Path, exit_id: str,
) -> dict[str, Any]:
    input_path = production_phase2_input(runtime, fixture, task, package, exit_id)
    runtime.cmd_record_phase2_check(argparse.Namespace(
        root=str(fixture),
        task=task.relative_to(fixture).as_posix(),
        input=input_path.relative_to(fixture).as_posix(),
        dry_run=False,
    ))
    return runtime.cmd_check_phase2_check(argparse.Namespace(
        root=str(fixture), task=task.relative_to(fixture).as_posix(),
    ))


def production_task_commit_authoring(
    runtime: Any,
    fixture: Path,
    checked: dict[str, Any],
    review_status: str,
) -> dict[str, Any]:
    coverage_source = (
        "guru-check-task:passed DTO at "
        + str(checked["phase2_capture_commit"])
    )
    classifications = [
        {
            "path": path,
            "category": "task-reviewed",
            "reason": "The isolated production eval includes this path in the checked task scope.",
            "coverage_source": coverage_source,
        }
        for path in runtime.git_status_paths(fixture)
    ]
    return {
        "path_classifications": classifications,
        "message": {
            "type": "feat",
            "scope": "workflow",
            "summary": "增加生产闭环评测",
            "background": "需要以真实 public wrapper 验证 AI-first 任务提交合同。",
            "changes": "提交隔离 fixture 中已由 Phase 2 覆盖的精确路径。",
            "boundaries": "不执行真实发布，也不包含用户授权记录。",
            "validations": "运行共享 public Skill wrapper corpus。",
        },
        "ai_review": {
            "status": review_status,
            "summary": "The exact production eval candidate completed semantic review.",
            "evidence": [
                "Every staged path is part of the isolated fixture and the current Phase 2 result."
            ],
        },
    }


def production_commit_for_review(
    runtime: Any,
    fixture: Path,
    task: Path,
    checked: dict[str, Any],
) -> tuple[str, str]:
    if hasattr(runtime, "commit_review_fixture"):
        return runtime.commit_review_fixture(fixture, task, checked)
    public_input = {
        "profile": "initial_commit",
        "mode": "workflow",
        "task_ref": task.relative_to(fixture).as_posix(),
        "source_exit": "passed",
        "phase2_commit_anchor": checked["phase2_capture_commit"],
    }
    try:
        candidate, plan, _ = runtime.build_task_commit_candidate(
            fixture,
            task,
            public_input,
            production_task_commit_authoring(
                runtime,
                fixture,
                checked,
                "passed",
            ),
        )
        executed = runtime.execute_task_commit_candidate(fixture, candidate, task)
    except runtime.WorkflowError as exc:
        raise ValueError(
            "production Branch Review fixture task commit failed: "
            + json.dumps(exc.payload, ensure_ascii=False, sort_keys=True)
        ) from exc
    return str(executed["commit_sha"]), str(plan["git"]["base_ref"])


def production_review_candidate(
    exit_id: str,
    head: str,
    *,
    resolved: bool = False,
    introduced_head: str | None = None,
) -> list[dict[str, Any]]:
    common = {
        "candidate_ref": "candidate-001",
        "affected_behavior": "The public Branch Review route must preserve the reviewed task behavior.",
        "path": "src/production-eval.txt",
        "evidence_refs": ["git:branch_review_commit", "src/production-eval.txt"],
        "requirement_refs": ["PRD R1"],
        "scope_basis": "The approved production eval requirement owns this behavior.",
        "qualification_reason": "The candidate was classified before any severity was assigned.",
    }
    current_scope_rejections = [
        {
            "candidate_ref": f"candidate-rejected-{scenario}",
            "disposition": "rejected_candidate",
            "scenario_class": scenario,
            "affected_behavior": (
                "The reviewer candidate was evaluated against current scope "
                "and disproved by implementation evidence."
            ),
            "path": "src/production-eval.txt",
            "evidence_refs": ["src/production-eval.txt"],
            "requirement_refs": ["PRD R5"],
            "scope_basis": (
                "The production eval preserves the current approved scenario "
                "without inventing a finding."
            ),
            "qualification_reason": (
                "The current implementation satisfies the bound contract, so "
                "the candidate is rejected without severity or finding fields."
            ),
        }
        for scenario in (
            "normal_required_behavior",
            "explicit_nonstandard_requirement",
            "approved_nonstandard_expansion",
        )
    ]
    if exit_id == "implementation_required" or resolved:
        findings = [{
            **common,
            "disposition": "qualified_finding",
            "scenario_class": "normal_required_behavior",
            "finding_ref": "F-001",
            "severity": "P2",
            "introduced_head": introduced_head or head,
            "fix_head": head if resolved else None,
            "closure_head": head if resolved else None,
            "status": "resolved" if resolved else "open",
            "closure_evidence": (
                [f"commit:{head}", "test:production-eval"]
                if resolved else []
            ),
        }]
        return findings + (current_scope_rejections if resolved else [])
    if exit_id == "scope_confirmation_required":
        return [{
            **common,
            "disposition": "scope_proposal",
            "scenario_class": "unconfirmed_nonstandard_proposal",
            "proposal_ref": "scope-proposal:R2",
            "proposal": "Expand the eval beyond the approved public wrapper boundary.",
            "trigger_evidence": ["The reviewer identified an unapproved optional expansion."],
            "clarification_route": "guru-clarify-requirements",
        }]
    return current_scope_rejections


def production_review_classification(candidate: dict[str, Any]) -> dict[str, Any]:
    disposition = candidate["disposition"]
    scenario = candidate["scenario_class"]
    if disposition == "qualified_finding":
        decision = {
            "normal_required_behavior": "qualified_current",
            "explicit_nonstandard_requirement": "qualified_explicit_nonstandard",
            "approved_nonstandard_expansion": "qualified_approved_expansion",
        }[scenario]
        defect_observation = (
            "The supported Branch Review path reproduced the current required-behavior defect."
        )
    elif disposition == "scope_proposal":
        decision = "rejected_no_authority"
        defect_observation = (
            "Current authority does not authorize the optional expansion proposed by the reviewer."
        )
    else:
        decision = "rejected_not_reproduced"
        defect_observation = (
            "The complete supported Branch Review range does not reproduce the candidate defect."
        )
    return {
        "candidate_ref": candidate["candidate_ref"],
        "decision": decision,
        "witness": {
            "requirement_refs": list(candidate["requirement_refs"]),
            "supported_entry_refs": ["entry:guru-review-branch:branch-review"],
            "existing_caller_refs": ["caller:production-branch-review-eval"],
            "honest_action_sequence": [
                "review the complete current base-to-HEAD range through the supported Branch Review entry",
            ],
            "defect_observation": defect_observation,
            "excluded_assumptions": [],
        },
        "consumer_use": "branch_review_route_checker",
    }


def production_review_semantic_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    common = {
        key: candidate[key]
        for key in (
            "candidate_ref",
            "disposition",
            "affected_behavior",
            "path",
            "evidence_refs",
        )
    }
    if candidate["disposition"] == "qualified_finding":
        keys = (
            "finding_ref",
            "severity",
            "introduced_head",
            "fix_head",
            "closure_head",
            "status",
            "closure_evidence",
        )
    elif candidate["disposition"] == "scope_proposal":
        keys = (
            "proposal_ref",
            "proposal",
            "trigger_evidence",
            "clarification_route",
        )
    else:
        keys = ()
    common.update({key: candidate[key] for key in keys})
    return common


def production_record_review(
    runtime: Any,
    fixture: Path,
    task: Path,
    public_input: dict[str, Any],
    recipe: str,
) -> dict[str, Any]:
    exit_id = recipe.removeprefix("review-")
    resolved = exit_id == "finding-fix-passed"
    if resolved:
        exit_id = "passed"
    elif exit_id == "fresh-final-passed":
        exit_id = "passed"
    head = runtime.current_head(fixture)
    closure_reviewer = "finding-owner-or-replacement" if resolved else None
    reviewer = "fresh-final-reviewer" if resolved else "independent-reviewer"
    if closure_reviewer == reviewer:
        raise ValueError("finding closure and fresh final review require distinct reviewers")
    introduced_head = (
        run_git(fixture, "rev-parse", f"{head}^") if resolved else None
    )
    candidates = production_review_candidate(
        exit_id,
        head,
        resolved=resolved,
        introduced_head=introduced_head,
    )
    candidate_classifications = [
        production_review_classification(item) for item in candidates
    ]
    semantic_candidates = [
        production_review_semantic_candidate(item) for item in candidates
    ]
    semantic = {
        "qualified_findings": [
            item for item in semantic_candidates
            if item["disposition"] == "qualified_finding"
        ],
        "scope_proposals": [
            item for item in semantic_candidates
            if item["disposition"] == "scope_proposal"
        ],
        "observations": [
            item for item in semantic_candidates
            if item["disposition"] == "observation"
        ],
        "followup_candidates": [
            item for item in semantic_candidates
            if item["disposition"] == "followup_candidate"
        ],
        "rejected_candidates": [
            item for item in semantic_candidates
            if item["disposition"] == "rejected_candidate"
        ],
        "ai_review_gate": {
            "status": exit_id,
            "summary": "The production Branch Review semantic Gate selected the actual route.",
        },
    }
    semantic_path = fixture / ".trellis/.runtime/guru-team/evals/review-owner-input.json"
    semantic_path.write_text(json.dumps({
        "candidate_classifications": candidate_classifications,
        "semantic_review": semantic,
        "verification_evidence": {
            "reviewer": reviewer,
            "review_source": runtime.INDEPENDENT_REVIEW_SOURCE,
            "evidence": (
                [
                    f"{closure_reviewer} completed transient finding closure on the fix commit.",
                    "fresh-final-reviewer independently reviewed the complete current range.",
                ]
                if resolved
                else ["Reviewed the complete current range and deployment impact."]
            ),
        },
    }) + "\n", encoding="utf-8")
    public_input.update({
        "task_ref": task.relative_to(fixture).as_posix(),
        "base_ref": runtime.diff_base_ref(fixture, "main"),
        "branch_review_commit": head,
        "review_intent": (
            "fresh_final_review"
            if resolved or recipe == "review-fresh-final-passed"
            else public_input.get("review_intent", "initial_review")
        ),
    })
    runtime_input = fixture / OWNER_INPUT
    runtime_input.write_text(json.dumps(public_input) + "\n", encoding="utf-8")
    runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
    direct_recorder_inputs = {runtime_input, semantic_path}
    for runtime_artifact in runtime_dir.rglob("*"):
        if (
            runtime_artifact.is_file()
            and runtime_artifact not in direct_recorder_inputs
        ):
            runtime_artifact.unlink()
    runtime.cmd_review_branch(argparse.Namespace(
        root=str(fixture),
        json=True,
        task=task.relative_to(fixture).as_posix(),
        base_branch="main",
        evidence=(
            [
                f"{closure_reviewer} 已在 fix commit 上完成瞬态 finding closure。",
                "fresh-final-reviewer 已独立审查完整当前 range 与部署影响。",
            ]
            if resolved
            else ["已审查运行时、CI/CD、Docker、K8s、migration 与 Makefile 部署影响。"]
        ),
        reviewer=reviewer,
        review_source=runtime.INDEPENDENT_REVIEW_SOURCE,
        skill_input=runtime_input.relative_to(fixture).as_posix(),
        semantic_review_file=semantic_path.relative_to(fixture).as_posix(),
        typed_exit=exit_id,
        dry_run=False,
    ))
    return runtime.cmd_check_review_gate(argparse.Namespace(
        root=str(fixture),
        task=task.relative_to(fixture).as_posix(),
        allow_nonpass=True,
        expected_exit=exit_id,
    ))


def production_publication_authoring(
    runtime: Any,
    fixture: Path,
    task: Path,
    public_input: dict[str, Any],
    recipe: str,
) -> Path:
    route = recipe.removeprefix("publication-")
    typed_exit = (
        "return_to_task_work"
        if route in {"return", "metadata-durable-drift-return"}
        else "blocked"
        if route == "blocked"
        else "ready"
    )
    if route == "metadata-fix-ready":
        candidate_ref = "candidate:publication:metadata-revision"
        decision = "qualified_current"
        defect_observation = (
            "The owner-private PR payload required a current task-local metadata "
            "revision before publication could be ready."
        )
    elif typed_exit == "return_to_task_work":
        candidate_ref = "candidate:publication:task-work"
        decision = "qualified_current"
        defect_observation = (
            "The current publication evidence contains a task-work defect that "
            "must return to the task owner."
        )
    elif typed_exit == "blocked":
        candidate_ref = "candidate:publication:external-blocker"
        decision = "qualified_current"
        defect_observation = (
            "The supported publication entry is blocked by a current external "
            "dependency that task work cannot repair."
        )
    else:
        candidate_ref = "candidate:publication:no-defect"
        decision = "rejected_not_reproduced"
        defect_observation = (
            "The complete current publication review reproduces no required-"
            "behavior defect."
        )
    candidate_classifications = [{
        "candidate_ref": candidate_ref,
        "decision": decision,
        "witness": {
            "requirement_refs": ["issue-scope-ledger.json", "pr_payload"],
            "supported_entry_refs": [
                "guru-review-task-publication",
                "git:branch_review_commit",
            ],
            "existing_caller_refs": [
                "guru-review-task-publication",
                "guru-finalize-task",
            ],
            "honest_action_sequence": [
                "Review the current PR payload, Branch Review gate, task scope, "
                "and publication evidence through the supported publication entry."
            ],
            "defect_observation": defect_observation,
            "excluded_assumptions": [
                "No hostile input, artifact tampering, or unsupported workflow bypass."
            ],
        },
        "consumer_use": "publication_route_checker",
    }]
    dimension_status = {
        item: "passed" for item in runtime.TASK_PUBLICATION_DIMENSIONS
    }
    metadata_revision = (
        "\n\n<a id=\"metadata-fix\"></a>\n"
        "已完成 owner-private PR payload 修订并重新审查。"
        if route == "metadata-fix-ready"
        else ""
    )
    pr_payload = {
        "title": "完成：#146 验证 Publication public wrapper 闭环",
        "body": (
            "## 变更摘要\n\n"
            "- 完成真实 public wrapper、recorder 与 checker 闭环评测。\n\n"
            "## 影响范围\n\n"
            "- 影响 Publication Skill、共享 runtime 与隔离评测仓库。\n\n"
            "## 验证结果\n\n"
            "- 已执行 recorder、checker 与 public wrapper 真实命令。\n\n"
            "## Review Gate\n\n"
            "- Branch Review Gate 已通过并绑定当前 HEAD。\n\n"
            "## Issue 关闭范围\n\n"
            "- Closes #146。\n\n"
            "## 安全说明\n\n"
            "- 不写生产环境，不处理 secret，不执行真实 GitHub 发布。\n\n"
            "## Docs SSOT\n\n"
            "- strategy: ssot_first\n"
            "- durable docs: docs/requirements.md 已作为实现输入。\n"
            "- merged delta: task delta 已合并到 durable docs。\n"
            "- task history: eval staging evidence 仅保留在 task history。\n"
            "- follow-up: 当前 PR 无额外限制。"
            + metadata_revision
        ),
    }
    findings: list[dict[str, Any]] = []
    if typed_exit == "return_to_task_work":
        dimension = (
            "docs_ssot_reconciliation"
            if route == "metadata-durable-drift-return"
            else "diff_outcome_consistency"
        )
        dimension_status[dimension] = "finding"
        findings.append({
            "finding_ref": (
                "PUB-DOCS-001"
                if route == "metadata-durable-drift-return"
                else "PUB-WORK-001"
            ),
            "candidate_ref": candidate_ref,
            "dimension": dimension,
            "summary": "The current publication review requires a complete task-work rerun.",
            "scope_basis": "The approved production eval owns this current-scope behavior.",
            "evidence_refs": ["docs/requirements.md"],
            "affected_artifacts": ["docs/requirements.md"],
            "route_class": "task_work",
            "status": "open",
            "closure_evidence": [],
        })
    elif typed_exit == "blocked":
        dimension_status["artifact_binding_freshness"] = "blocked"
        findings.append({
            "finding_ref": "PUB-BLOCK-001",
            "candidate_ref": candidate_ref,
            "dimension": "artifact_binding_freshness",
            "summary": "An external publication dependency is unavailable.",
            "scope_basis": "The dependency cannot be repaired by current task work.",
            "evidence_refs": ["external:publication-dependency"],
            "affected_artifacts": ["external:publication-dependency"],
            "route_class": "external_blocker",
            "status": "open",
            "closure_evidence": [],
        })
    elif route == "metadata-fix-ready":
        findings.append({
            "finding_ref": "PUB-META-001",
            "candidate_ref": candidate_ref,
            "dimension": "pr_body_quality",
            "summary": "The owner-private PR payload was revised and rereviewed.",
            "scope_basis": "The contract permits an internal payload metadata revision.",
            "evidence_refs": ["pr_payload.body"],
            "affected_artifacts": ["pr_payload"],
            "route_class": "metadata_revision",
            "status": "closed",
            "closure_evidence": ["pr_payload.body#metadata-fix"],
        })
    dimensions = [{
        "id": dimension,
        "status": dimension_status[dimension],
        "summary": f"The semantic owner reviewed {dimension} against current evidence.",
        "evidence_refs": [
            "pr_payload",
            "issue-scope-ledger.json",
            "git:branch_review_commit",
        ],
    } for dimension in runtime.TASK_PUBLICATION_DIMENSIONS]
    authoring: dict[str, Any] = {
        "profile": public_input["profile"],
        "mode": public_input["mode"],
        "review_intent": public_input["review_intent"],
        "pr_payload": pr_payload,
        "candidate_classifications": candidate_classifications,
        "dimensions": dimensions,
        "findings": findings,
        "conclusions": {
            "issue_scope": {
                "status": (
                    "passed"
                    if typed_exit == "ready"
                    else "finding"
                    if typed_exit == "return_to_task_work"
                    else "blocked"
                ),
                "summary": "The owner reviewed current issue closure scope.",
                "evidence_refs": ["issue-scope-ledger.json"],
            },
            "docs_ssot": {
                "status": (
                    "finding"
                    if route == "metadata-durable-drift-return"
                    else "passed"
                ),
                "summary": "The owner reviewed the approved Docs SSOT outcome.",
                "evidence_refs": [
                    "git:branch_review_commit",
                    "docs/requirements.md",
                ],
            },
            "safety_deployment": {
                "status": "blocked" if typed_exit == "blocked" else "passed",
                "summary": "The owner reviewed safety and deployment impact.",
                "evidence_refs": ["pr_payload"],
            },
        },
        "route": {"typed_exit": typed_exit},
    }
    if public_input["profile"] == "publication_review_stale":
        authoring["stale_reason"] = public_input["stale_reason"]
    if typed_exit == "blocked":
        authoring["route"].update({
            "reason_code": "external_publication_dependency",
            "remediation": "Restore the external dependency and re-enter publication review.",
        })
    path = fixture / ".trellis/.runtime/guru-team/evals/publication-owner-input.json"
    runtime.write_json(path, authoring)
    return path





def extension_verification_execution(
    runtime: Any,
    fixture: Path,
    public_input: dict[str, Any],
    status: str,
    selected: list[str],
    package: Path,
    *,
    resolved_head: str,
) -> dict[str, Any]:
    commands = [{
        "id": "verify_throwaway_installation",
        "checkout_owner": "extension_source_checkout",
        "argv": ["git", "ls-remote", "origin", public_input["ref"]],
        "exit_code": 0 if status == "passed" else 2,
        "stdout_sha256": runtime.digest_text(""),
        "stderr_sha256": runtime.digest_text(
            "" if status == "passed" else "synthetic unavailable"
        ),
        "stdout_size_bytes": 0,
        "stderr_size_bytes": 0 if status == "passed" else 21,
    }]
    if status == "passed":
        example = json.loads(
            (package / "examples/execution-facts.json").read_text(encoding="utf-8")
        )
        asset_expectations = copy.deepcopy(example["asset_expectations"])
        asset_digests = copy.deepcopy(example["asset_digests"])
        asset_inventory = copy.deepcopy(example["asset_inventory"])
    else:
        asset_expectations = []
        asset_digests = []
        asset_inventory = runtime.extension_verification_asset_inventory_summary([], [])
    return {
        "schema_version": runtime.EXTENSION_VERIFICATION_SCHEMA_VERSION,
        "target_repository": {
            "repo_ref": public_input["repo_ref"],
            "remote": public_input["remote"],
            "ref": public_input["ref"],
            "branch_review_commit": None,
            "publication_head": None,
            "resolved_head": resolved_head,
            "checkout_head": resolved_head if status == "passed" else None,
            "reviewed_content_sha256": None,
            "remote_reviewed_content_sha256": None,
            "content_identity_matches": status == "passed",
        },
        "extension_source": {
            "selection": "standalone_fallback",
            "manifest_provenance": "not_available",
            "repo": public_input["repo_ref"],
            "locator": runtime.extension_verification_canonical_github_locator(
                public_input["repo_ref"]
            ),
            "requested_ref": public_input["ref"],
            "resolved_ref": public_input["ref"],
            "tree_state": "clean",
            "is_mutable_ref": False,
            "direct_oid": resolved_head,
            "commit": resolved_head,
            "checkout_head": resolved_head if status == "passed" else None,
            "ref_matches_commit": status == "passed",
            "checkout_head_matches": status == "passed",
        },
        "status": status,
        "commands": commands,
        "capabilities": runtime.extension_verification_capability_facts(
            selected,
            "passed" if status == "passed" else "blocked",
            commands,
            asset_digests,
        ),
        "asset_expectations": asset_expectations,
        "asset_digests": asset_digests,
        "asset_inventory": asset_inventory,
        "ownership": {
            "checkout_owner": "extension_source_checkout",
            "current_contract": True,
            "schema_version": "3.0",
            "inventory_id": "guru-team-upstream-ownership",
            "guru_owned_rule_count": 11,
            "managed_claim_count": 9,
        },
        "sidecars": {"checkout_owner": "extension_source_checkout", "paths": []},
    }


def extension_verification_review(
    typed_exit: str,
    selected: list[str],
) -> dict[str, Any]:
    blocked = typed_exit == "blocked"
    review: dict[str, Any] = {
        "applicability": {
            "status": "required",
            "reason": "The explicit source-repository invocation requires installation verification.",
            "evidence_paths": ["trellis/skills/guru-team/registry.json"],
        },
        "verification_profile": {
            "selected_capabilities": selected,
            "selection_reason": "The closed source profile covers every extension capability.",
            "coverage": [f"source extension -> {capability}" for capability in selected],
        },
        "semantic_review": {
            "adequacy": [{
                "id": "profile_coverage",
                "status": "blocked" if blocked else "passed",
                "evidence_refs": ["owner-staging:source-extension-verification"],
            }],
            "findings": ([{
                "finding_ref": "extension-eval-blocker-001",
                "evidence": "The synthetic source remote is unavailable.",
                "route_class": "external_blocker",
                "status": "open",
                "closure_evidence": "",
            }] if blocked else []),
            "conclusion": typed_exit,
        },
        "typed_exit": typed_exit,
        "redaction": {
            "status": "passed",
            "scanned_surfaces": ["artifact", "wrapper_stdout", "eval_trace", "retained_logs"],
        },
    }
    if blocked:
        review.update({
            "reason_code": "remote_unavailable",
            "remediation": "Restore source remote access and rerun standalone verification.",
        })
    return review


def stage_extension_verification_owner_execution(
    runtime: Any,
    fixture: Path,
    fixture_runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    typed_exit = {
        "extension-source-verified": "verified",
        "extension-source-unavailable": "blocked",
    }.get(recipe)
    if typed_exit is None:
        raise ValueError(f"unsupported source extension recipe: {recipe}")
    source_repo = request_package.parents[4]
    canonical_source = source_repo / "trellis"
    if canonical_source.is_symlink() or not canonical_source.is_dir():
        raise ValueError("canonical source tree is unavailable for extension staging")
    shutil.copytree(
        canonical_source,
        fixture / "trellis",
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    package = fixture / ".trellis/guru-team/skills/packages/guru-verify-extension-installation"
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("extension owner staging package does not match the evaluated contract")

    remotes = run_git(fixture, "remote").splitlines()
    remote_command = "set-url" if "origin" in remotes else "add"
    run_git(
        fixture,
        "remote",
        remote_command,
        "origin",
        "https://github.com/castbox/guru-trellis.git",
    )
    run_git(fixture, "add", ".")
    if subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=fixture, check=False
    ).returncode != 0:
        run_git(fixture, "commit", "-q", "-m", "stage source verification owner")
    head = run_git(fixture, "rev-parse", "HEAD")
    public_input = json.loads(public_input_path.read_text(encoding="utf-8"))
    public_input.update({
        "profile": "source_repository_verification",
        "mode": "standalone",
        "repo_ref": "castbox/guru-trellis",
        "remote": "origin",
        "ref": head,
        "caller_intent": "verify-extension-installation",
    })
    runtime_input = fixture / OWNER_INPUT
    runtime.write_json(runtime_input, public_input)
    runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
    execution_path = runtime_dir / "extension-execution-input.json"
    review_path = runtime_dir / "extension-review-input.json"
    capabilities = list(runtime.EXTENSION_VERIFICATION_CAPABILITIES)
    runtime.write_json(
        execution_path,
        extension_verification_execution(
            runtime,
            fixture,
            public_input,
            "passed" if typed_exit == "verified" else "blocked",
            capabilities,
            request_package,
            resolved_head=head,
        ),
    )
    runtime.write_json(review_path, extension_verification_review(typed_exit, capabilities))
    owner = runtime.cmd_record_extension_verification(argparse.Namespace(
        root=str(fixture),
        input=runtime_input.relative_to(fixture).as_posix(),
        execution_input=execution_path.relative_to(fixture).as_posix(),
        review_input=review_path.relative_to(fixture).as_posix(),
    ))
    runtime.write_json(fixture / OWNER_RESULT, owner)
    return package, fixture_runtime_target, {"GURU_TEAM_EVAL_STAGING": "1"}


def stage_task_pr_merge_owner_execution(
    runtime: Any,
    request: dict[str, Any],
    fixture: Path,
    fixture_runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    if not recipe.startswith("merge-"):
        raise ValueError("merge owner staging recipe is invalid")
    package = fixture / ".trellis/guru-team/skills/packages/guru-merge-task-pr"
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("merge owner staging package does not match the evaluated contract")

    public_input = json.loads(public_input_path.read_text(encoding="utf-8"))
    runtime_input = fixture / OWNER_INPUT
    runtime_input.parent.mkdir(parents=True, exist_ok=True)
    runtime.write_json(runtime_input, public_input)
    blocked_routes = {
        "merge-standalone-draft-blocked": (
            "pr_ready",
            "pull_request_draft",
            "Mark the PR Ready and rerun the live preview.",
        ),
        "merge-workflow-head-drift-blocked": (
            "repository_and_head",
            "expected_head_changed",
            "Rerun publication and merge review for the current PR head.",
        ),
        "merge-workflow-branch-drift-blocked": (
            "repository_and_head",
            "expected_branch_changed",
            "Restore the reviewed base/head branches and rerun the live preview.",
        ),
        "merge-workflow-close-scope-blocked": (
            "close_scope",
            "close_scope_mismatch",
            "Repair and rereview the PR close-keyword scope before merge.",
        ),
        "merge-workflow-added-close-scope-blocked": (
            "close_scope",
            "close_scope_mismatch",
            "Repair and rereview the PR close-keyword scope before merge.",
        ),
    }
    blocked = blocked_routes.get(recipe)
    dimensions = []
    for identifier in runtime.TASK_PR_MERGE_DIMENSIONS:
        dimensions.append({
            "id": identifier,
            "status": "blocked" if blocked and identifier == blocked[0] else "passed",
            "summary": (
                f"The controlled live facts block {identifier}."
                if blocked and identifier == blocked[0]
                else f"The controlled live facts pass {identifier}."
            ),
        })
    route = (
        {
            "typed_exit": "merge_blocked",
            "reason_code": blocked[1],
            "remediation": blocked[2],
        }
        if blocked
        else {"typed_exit": "merged", "merge_method": "merge"}
    )
    review_path = fixture / ".trellis/.runtime/guru-team/evals/merge-review.json"
    runtime.write_json(
        review_path,
        {"semantic_review": {"dimensions": dimensions}, "route": route},
    )
    fake_bin = write_fake_merge_gh(Path(request["workdir"]).resolve().parent, recipe)
    environment = {"PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}"}
    previous_path = os.environ.get("PATH")
    os.environ["PATH"] = environment["PATH"]
    owner_context: dict[str, Any] = {}
    try:
        recorded = runtime.cmd_record_task_pr_merge(argparse.Namespace(
            root=str(fixture),
            input=runtime_input.relative_to(fixture).as_posix(),
            review_input=str(review_path),
        ))
        gate_path = fixture / str(recorded["gate"])
        if not blocked:
            runtime.cmd_execute_task_pr_merge(argparse.Namespace(
                root=str(fixture),
                input=runtime_input.relative_to(fixture).as_posix(),
                gate=gate_path.relative_to(fixture).as_posix(),
            ))
        bind_merge_gate_argument(request, fixture, gate_path)
    finally:
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path
    return package, fixture_runtime_target, environment



def stage_finalization_owner_execution(
    runtime: Any,
    request: dict[str, Any],
    fixture: Path,
    fixture_runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    routes = {
        "finalization-publication-stale": (
            "publication_review_stale",
            "prepared",
        ),
        "finalization-same-plan-resume": (
            "resume_finalization",
            "draft_bound",
        ),
        "finalization-cross-month-reprepare": (
            "reprepare_required",
            "reprepare_required",
        ),
        "finalization-ready-for-merge-recovery": (
            "ready_for_merge",
            "ready",
        ),
        "finalization-publication-ready-ready-for-merge": (
            "ready_for_merge",
            "ready",
        ),
        "finalization-same-plan-ready-for-merge": (
            "ready_for_merge",
            "ready",
        ),
        "finalization-blocked": (
            "blocked",
            "prepared",
        ),
    }
    selected = routes.get(recipe)
    if selected is None:
        raise ValueError(
            f"unsupported finalization owner staging recipe: {recipe}"
        )
    exit_id, transaction_state = selected
    package = (
        fixture
        / ".trellis/guru-team/skills/packages/guru-finalize-task"
    )
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError(
            "finalization owner staging package does not match the evaluated contract"
        )

    task = fixture / ".trellis/tasks/current"
    task.mkdir(parents=True, exist_ok=True)
    runtime.write_json(task / "task.json", {
        "id": "current",
        "name": "current",
        "title": "Finalization eval",
        "status": "in_progress",
        "branch": "main",
        "base_branch": "main",
    })
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-q", "-m", "stage finalization owner")
    head = run_git(fixture, "rev-parse", "HEAD")
    public_input = json.loads(public_input_path.read_text(encoding="utf-8"))
    public_input["task_ref"] = ".trellis/tasks/current"
    plan_digest = "b" * 64
    plan_ref = f"closeout-plan:{plan_digest}"
    if "plan_ref" in public_input:
        public_input["plan_ref"] = plan_ref
    if "branch_review_commit" in public_input:
        public_input["branch_review_commit"] = head
    runtime_input = fixture / OWNER_INPUT
    runtime.write_json(runtime_input, public_input)

    runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    context_path = runtime_dir / "finalization-context.json"
    archive_locator = ".trellis/tasks/archive/2026-07/current"
    if transaction_state == "ready":
        (fixture / archive_locator).mkdir(parents=True, exist_ok=True)
    context_payload = {
        "schema_version": "2.0",
        "task_ref": public_input["task_ref"],
        "plan_ref": plan_ref,
        "plan_digest": plan_digest,
        "branch_review_commit": head,
        "publication_head": head,
        "archive_locator": archive_locator,
        "repo_ref": "example/guru-extension",
        "remote": "origin",
        "head_branch": "main",
        "publication_status": (
            "stale"
            if exit_id == "publication_review_stale"
            else "current"
        ),
        "publication_stale_reason": (
            "publication_review_stale"
            if exit_id == "publication_review_stale"
            else None
        ),
        "transaction_state": transaction_state,
    }
    runtime.write_json(context_path, context_payload)
    previous_eval = os.environ.get("GURU_TEAM_EVAL_STAGING")
    os.environ["GURU_TEAM_EVAL_STAGING"] = "1"
    try:
        context = runtime.finalization_eval_preview_context(
            fixture,
            public_input,
        )
        if context is None:
            raise ValueError("finalization eval context was not accepted")
        outputs = {
            "publication_review_stale": {
                "exit_id": "publication_review_stale",
                "task_ref": public_input["task_ref"],
                "branch_review_commit": head,
                "stale_reason": "publication_review_stale",
            },
            "resume_finalization": {
                "exit_id": "resume_finalization",
                "task_ref": public_input["task_ref"],
                "plan_ref": plan_ref,
            },
            "reprepare_required": {
                "exit_id": "reprepare_required",
                "task_ref": public_input["task_ref"],
                "reason_code": "archive_month_changed",
                "branch_review_commit": head,
                "publication_head": head,
            },
            "ready_for_merge": {
                "materialization": "executor",
            },
            "blocked": {
                "exit_id": "blocked",
                "reason_code": "invalid_private_state",
                "remediation": "Repair the staged objective state and rerun finalization.",
            },
        }
        gate = {
            "schema_version": "5.0",
            "skill_id": "guru-finalize-task",
            "identity": {
                "task_ref": public_input["task_ref"],
                "plan_ref": plan_ref,
                "plan_digest": plan_digest,
                "branch_review_commit": head,
            },
            "review": {
                "status": (
                    "blocked"
                    if exit_id == "blocked"
                    else "reroute"
                    if exit_id in {
                        "publication_review_stale",
                        "resume_finalization",
                        "reprepare_required",
                    }
                    else "passed"
                ),
                "summary": "The finalization eval owner reviewed the exact staged objective facts.",
            },
            "route": {
                "typed_exit": exit_id,
                "consumer": runtime.FINALIZATION_CONSUMERS[exit_id],
                "output": outputs[exit_id],
            },
        }
        gate_path = runtime.task_finalization_path(
            fixture,
            task,
        )
        runtime.write_json(gate_path, gate)
        runtime.check_finalization_gate_result(
            fixture,
            argparse.Namespace(),
            public_input,
            gate,
            gate_path,
        )
        bind_owner_result_argument(request, fixture, gate_path)
    finally:
        if previous_eval is None:
            os.environ.pop("GURU_TEAM_EVAL_STAGING", None)
        else:
            os.environ["GURU_TEAM_EVAL_STAGING"] = previous_eval
    fake_bin = write_fake_gh(
        Path(request["workdir"]).resolve().parent,
        recipe,
    )
    return package, fixture_runtime_target, {
        "GURU_TEAM_EVAL_STAGING": "1",
        "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
    }


def stage_base_reconciliation_owner_execution(
    request: dict[str, Any],
    fixture: Path,
    fixture_runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    exits = {
        "base-reconciled": "reconciled",
        "base-review-continuity": "review_continuity_required",
        "base-implementation-required": "implementation_required",
        "base-planning-stale": "planning_stale",
        "base-scope-confirmation": "scope_confirmation_required",
        "base-blocked": "blocked",
    }
    exit_id = exits.get(recipe)
    if exit_id is None:
        raise ValueError(f"unsupported base reconciliation owner staging recipe: {recipe}")
    package = fixture / ".trellis/guru-team/skills/packages/guru-reconcile-task-base"
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("base reconciliation owner staging package does not match the evaluated contract")

    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-q", "-m", "stage base reconciliation eval")
    old_base = run_git(fixture, "rev-parse", "HEAD")
    (fixture / "base-evolution.txt").write_text("new base\n", encoding="utf-8")
    run_git(fixture, "add", "base-evolution.txt")
    run_git(fixture, "commit", "-q", "-m", "advance eval base")
    new_base = run_git(fixture, "rev-parse", "HEAD")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", new_base)
    run_git(fixture, "checkout", "-q", "-b", "eval/base-reconciliation", old_base)
    (fixture / "task-evolution.txt").write_text("task content\n", encoding="utf-8")
    run_git(fixture, "add", "task-evolution.txt")
    run_git(fixture, "commit", "-q", "-m", "stage eval task content")
    task_head = run_git(fixture, "rev-parse", "HEAD")

    public_input = json.loads(public_input_path.read_text(encoding="utf-8"))
    public_input.update({
        "task_ref": ".trellis/tasks/current",
        "task_head": task_head,
        "selected_base_ref": "origin/main",
        "old_base_head": old_base,
        "new_base_head": new_base,
    })
    if "branch_review_commit" in public_input:
        public_input["branch_review_commit"] = task_head
    task_ref = public_input["task_ref"]
    task_id = "current"
    workspace_slug = "current"
    task_dir = fixture / task_ref
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "task.json").write_text(json.dumps({
        "id": task_id,
        "name": task_id,
        "title": "Base reconciliation eval",
        "status": "planning" if public_input["profile"] == "post_plan" else "in_progress",
        "branch": "eval/base-reconciliation",
        "base_branch": "main",
    }) + "\n", encoding="utf-8")
    mappings_root = fixture / ".trellis/.runtime/guru-team"
    task_mappings = mappings_root / "tasks"
    workspace_mappings = mappings_root / "workspaces"
    task_mappings.mkdir(parents=True, exist_ok=True)
    workspace_mappings.mkdir(parents=True, exist_ok=True)
    (task_mappings / f"{task_id}.json").write_text(json.dumps({
        "schema_version": "1.0",
        "task_slug": task_id,
        "workspace_slug": workspace_slug,
        "workspace_path": str(fixture.resolve()),
        "task_artifact_dir": task_ref,
    }) + "\n", encoding="utf-8")
    (workspace_mappings / f"{workspace_slug}.json").write_text(json.dumps({
        "schema_version": "1.0",
        "workspace_slug": workspace_slug,
        "workspace_path": str(fixture.resolve()),
        "branch_name": "eval/base-reconciliation",
    }) + "\n", encoding="utf-8")
    runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    runtime_input = fixture / OWNER_INPUT
    runtime_input.write_text(json.dumps(public_input) + "\n", encoding="utf-8")

    route_payloads = {
        "reconciled": {},
        "review_continuity_required": {
            "candidate_tree_sha256": "c" * 64,
            "relevant_paths": ["base-evolution.txt"],
        },
        "implementation_required": {"finding_refs": ["base-finding-001"]},
        "planning_stale": {"reason_refs": ["authority-assumption-changed"]},
        "scope_confirmation_required": {"proposal_refs": ["scope-proposal-001"]},
        "blocked": {},
    }
    impacts = {
        "reconciled": ("unchanged", "unchanged", "compatible"),
        "review_continuity_required": ("unchanged", "unchanged", "continuity_review_required"),
        "implementation_required": ("unchanged", "implementation_required", "validation_failed"),
        "planning_stale": ("changed", "planning_stale", "insufficient_evidence"),
        "scope_confirmation_required": ("changed", "planning_stale", "insufficient_evidence"),
        "blocked": ("insufficient_evidence", "insufficient_evidence", "insufficient_evidence"),
    }
    authority, task_content, integration = impacts[exit_id]
    gate = {
        "authority_impact": authority,
        "task_content_impact": task_content,
        "integration_impact": integration,
        "reviewed_scope": ["live authority", "approved planning", "cumulative base delta", "candidate evidence"],
        "key_delta_refs": [f"{old_base}...{new_base}"],
        "validation_evidence": ["isolated candidate evidence reviewed for the exact pair"],
        "unverified_boundaries": (["applicable evidence does not support one unique route"] if exit_id == "blocked" else []),
        "summary": f"The semantic owner selected {exit_id} for the exact evolved-base pair.",
        "typed_exit": exit_id,
        "route_payload": route_payloads[exit_id],
    }
    gate_path = runtime_dir / "base-semantic-review.json"
    gate_path.write_text(json.dumps(gate) + "\n", encoding="utf-8")
    recorded = subprocess.run(
        [
            str(package / "scripts/record-base-reconciliation.sh"),
            "--root", str(fixture), "--skill-input", OWNER_INPUT,
            "--semantic-review-file", gate_path.relative_to(fixture).as_posix(),
            "--typed-exit", exit_id,
        ],
        cwd=fixture, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    if recorded.returncode != 0:
        raise ValueError(f"base reconciliation recorder staging failed: {recorded.stderr.strip()}")
    owner_result = json.loads(recorded.stdout)
    checkpoint_namespace = (
        f"{task_id}-{hashlib.sha256(task_ref.encode()).hexdigest()[:12]}"
    )
    checkpoint = (
        fixture / ".trellis/.runtime/guru-team/owner-checkpoints"
        / checkpoint_namespace / "guru-reconcile-task-base/base-reconciliation.json"
    )
    checked = subprocess.run(
        [
            str(package / "scripts/check-base-reconciliation.sh"),
            "--root", str(fixture), "--input", checkpoint.relative_to(fixture).as_posix(),
            "--expected-exit", exit_id,
        ],
        cwd=fixture, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    if checked.returncode != 0:
        raise ValueError(f"base reconciliation checker staging failed: {checked.stderr.strip()}")
    invocation_path = fixture / OWNER_INVOCATION
    invocation_path.write_text(
        json.dumps({"public_input": public_input, "owner_result": owner_result}) + "\n",
        encoding="utf-8",
    )
    return package, fixture_runtime_target, {"GURU_TEAM_EVAL_STAGING": "1"}


def stage_production_owner_execution(
    request: dict[str, Any],
    fixture: Path,
    runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    skill_id = str(request["skill_id"])
    fixture_runtime_target = fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
    if fixture_runtime_target.is_symlink() or not os.access(fixture_runtime_target, os.X_OK):
        raise ValueError("fixture public invocation runtime is unavailable")
    runtime = (
        None
        if skill_id in {"guru-maintain-architecture-baseline", "guru-restore-archived-task"}
        else load_package_owner_runtime(fixture_runtime_target, skill_id)
    )
    if runtime is not None and not hasattr(runtime, "read_json"):
        runtime.read_json = lambda path: json.loads(Path(path).read_text(encoding="utf-8"))
    if runtime is not None and not hasattr(runtime, "diff_base_ref"):
        runtime.diff_base_ref = lambda root, branch: branch
    if runtime is not None and not hasattr(runtime, "changed_files"):
        runtime.changed_files = lambda root, revision: subprocess.run(
            ["git", "diff", "--name-only", revision, "--"], cwd=root,
            text=True, stdout=subprocess.PIPE, check=False,
        ).stdout.splitlines()
    if runtime is not None and not hasattr(runtime, "git_status_paths"):
        runtime.git_status_paths = lambda root: [
            line[3:] for line in subprocess.run(
                ["git", "status", "--short"], cwd=root,
                text=True, stdout=subprocess.PIPE, check=False,
            ).stdout.splitlines() if len(line) >= 4
        ]
    if skill_id == "guru-reconcile-task-base":
        return stage_base_reconciliation_owner_execution(
            request,
            fixture,
            fixture_runtime_target,
            request_package,
            recipe,
            public_input_path,
        )
    if skill_id == "guru-finalize-task":
        return stage_finalization_owner_execution(
            runtime,
            request,
            fixture,
            fixture_runtime_target,
            request_package,
            recipe,
            public_input_path,
        )
    if skill_id == "guru-verify-extension-installation":
        return stage_extension_verification_owner_execution(
            runtime,
            fixture,
            fixture_runtime_target,
            request_package,
            recipe,
            public_input_path,
        )
    if skill_id == "guru-merge-task-pr":
        return stage_task_pr_merge_owner_execution(
            runtime,
            request,
            fixture,
            fixture_runtime_target,
            request_package,
            recipe,
            public_input_path,
        )
    if skill_id == "guru-restore-archived-task":
        return stage_restore_archived_task_owner_execution(
            request,
            fixture,
            fixture_runtime_target,
            request_package,
            recipe,
            public_input_path,
        )
    compose_production_fixture_runtime(fixture_runtime_target, runtime)
    compose_production_owner_command_runtime(fixture_runtime_target, runtime)
    task, _ = production_task_fixture(runtime, fixture)
    production_environment: dict[str, str] = {}
    package = fixture / ".trellis/guru-team/skills/packages" / skill_id
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("owner staging package does not match the evaluated package contract")
    public_input = json.loads(public_input_path.read_text(encoding="utf-8"))
    expected_prefix = {
        "guru-approve-task-plan": "planning-",
        "guru-check-task": "check-",
        "guru-create-task-commit": "commit-",
        "guru-finalize-task": "finalization-",
        "guru-review-branch": "review-",
        "guru-review-task-publication": "publication-",
        "guru-verify-extension-installation": "extension-",
    }[skill_id]
    if not recipe.startswith(expected_prefix):
        raise ValueError("production owner staging recipe does not match the evaluated package")
    if skill_id == "guru-approve-task-plan":
        planning_exit = {
            "planning-approved": "approved",
            "planning-revision-required": "revision_required",
            "planning-clarify-scope": "clarify_scope",
            "planning-blocked": "blocked",
        }.get(recipe)
        if planning_exit is None:
            raise ValueError("unsupported planning owner staging recipe")
        checked_owner = production_record_planning(
            runtime, fixture, task, planning_exit,
        )
        owner_result_path = Path(checked_owner["artifact_path"])
    else:
        production_record_planning(runtime, fixture, task, "approved")
        task_payload = json.loads((task / "task.json").read_text(encoding="utf-8"))
        task_payload["status"] = "in_progress"
        (task / "task.json").write_text(
            json.dumps(task_payload) + "\n", encoding="utf-8"
        )
        run_git(fixture, "add", task.relative_to(fixture).as_posix())
        run_git(fixture, "commit", "-q", "-m", "activate production eval task")
        (fixture / "src/production-eval.txt").write_text(
            f"{recipe}\n", encoding="utf-8",
        )
        phase2_package = fixture / ".trellis/guru-team/skills/packages/guru-check-task"
        phase2_exit = {
            "check-passed": "passed",
            "check-implementation-required": "implementation_required",
            "check-planning-stale": "planning_stale",
            "check-blocked": "blocked",
        }.get(recipe)
        checked = production_record_phase2(
            runtime,
            fixture,
            task,
            phase2_package,
            (
                "passed"
                if skill_id in {
                    "guru-create-task-commit",
                    "guru-review-branch",
                    "guru-review-task-publication",
                }
                else phase2_exit
            ),
        )
        owner_result_path = Path(checked["artifact_path"])
        if skill_id == "guru-create-task-commit":
            public_input["phase2_commit_anchor"] = checked[
                "phase2_capture_commit"
            ]
            review_status = {
                "commit-revision-required": "revision-required",
                "commit-blocked-recovery": "blocked",
            }.get(recipe, "passed")
            if recipe == "commit-revision-required":
                runtime.build_task_commit_candidate(
                    fixture,
                    task,
                    {
                        "profile": "initial_commit",
                        "mode": public_input["mode"],
                        "task_ref": task.relative_to(fixture).as_posix(),
                        "source_exit": "passed",
                        "phase2_commit_anchor": checked[
                            "phase2_capture_commit"
                        ],
                    },
                    production_task_commit_authoring(
                        runtime,
                        fixture,
                        checked,
                        "revision-required",
                    ),
                )
            owner_result_path, _, _ = runtime.build_task_commit_candidate(
                fixture,
                task,
                public_input,
                production_task_commit_authoring(
                    runtime,
                    fixture,
                    checked,
                    review_status,
                ),
            )
        elif skill_id == "guru-review-branch":
            production_commit_for_review(
                runtime, fixture, task, checked
            )
            production_record_review(
                runtime,
                fixture,
                task,
                public_input,
                recipe,
            )
            runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
            for runtime_artifact in runtime_dir.rglob("*"):
                if (
                    runtime_artifact.is_file()
                    and runtime_artifact != fixture / OWNER_INPUT
                ):
                    runtime_artifact.unlink()
        elif skill_id == "guru-review-task-publication":
            production_commit_for_review(
                runtime, fixture, task, checked
            )
            branch_input = {
                "profile": "branch_review",
                "mode": public_input["mode"],
                "task_ref": task.relative_to(fixture).as_posix(),
                "base_ref": "origin/main",
                "branch_review_commit": "0" * 40,
                "review_intent": "initial_review",
            }
            branch_check = production_record_review(
                runtime,
                fixture,
                task,
                branch_input,
                "review-passed",
            )
            branch_review_commit = branch_check["review_commit"]
            public_input["task_ref"] = task.relative_to(fixture).as_posix()
            public_input["branch_review_commit"] = branch_review_commit
            if public_input["profile"] != "publication_review":
                initial_input = {
                    "profile": "publication_review",
                    "mode": public_input["mode"],
                    "task_ref": task.relative_to(fixture).as_posix(),
                    "branch_review_commit": branch_review_commit,
                    "review_intent": "initial_review",
                }
                initial_authoring_path = production_publication_authoring(
                    runtime,
                    fixture,
                    task,
                    initial_input,
                    "publication-ready",
                )
                runtime.cmd_record_task_publication_review(argparse.Namespace(
                    root=str(fixture),
                    task=task.relative_to(fixture).as_posix(),
                    input=initial_authoring_path.relative_to(fixture).as_posix(),
                    branch_review_commit=initial_input["branch_review_commit"],
                    dry_run=False,
                ))
            if recipe == "publication-metadata-durable-drift-return":
                with (fixture / "docs/requirements.md").open(
                    "a", encoding="utf-8"
                ) as handle:
                    handle.write(
                        "\nUncommitted durable drift requires a task-work rerun.\n"
                    )
            authoring_path = production_publication_authoring(
                runtime,
                fixture,
                task,
                public_input,
                recipe,
            )
            publication_owner = runtime.cmd_record_task_publication_review(argparse.Namespace(
                root=str(fixture),
                task=task.relative_to(fixture).as_posix(),
                input=authoring_path.relative_to(fixture).as_posix(),
                branch_review_commit=branch_review_commit,
                dry_run=False,
            ))
            owner_result_path = Path(publication_owner["artifact_path"])
            runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
            for runtime_artifact in runtime_dir.rglob("*"):
                if (
                    runtime_artifact.is_file()
                    and runtime_artifact != fixture / OWNER_INPUT
                ):
                    runtime_artifact.unlink()
    runtime_input = fixture / OWNER_INPUT
    runtime.write_json(runtime_input, public_input)
    if skill_id != "guru-review-branch":
        bind_owner_result_argument(request, fixture, owner_result_path)
    return package, fixture_runtime_target, production_environment


def stage_restore_archived_task_owner_execution(
    request: dict[str, Any],
    fixture: Path,
    fixture_runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    """Build a real archive/worktree owner fixture and invoke the public restore script."""
    package = fixture / ".trellis/guru-team/skills/packages/guru-restore-archived-task"
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("restore owner staging package does not match the evaluated contract")
    if not recipe.startswith("restore-"):
        raise ValueError("restore owner staging recipe is invalid")

    case = recipe.removeprefix("restore-")
    task_id = "09-03-348-merge-blocked-phase2-reentry"
    branch = "codex/348-merge-blocked-phase2-reentry"
    repo_ref = "castbox/guru-trellis"
    pr_number = 348
    archive_locator = f".trellis/tasks/archive/2026-09/{task_id}"
    active_locator = f".trellis/tasks/{task_id}"
    worktree = fixture / "owner-worktrees" / task_id
    worktree.parent.mkdir(parents=True, exist_ok=True)
    run_git(fixture, "branch", "-M", "main")
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-q", "-m", "stage restore owner base")
    run_git(fixture, "worktree", "add", "-q", "-b", branch, str(worktree), "HEAD")
    expected_head = run_git(worktree, "rev-parse", "HEAD")
    archive_commit = expected_head

    archive = fixture / archive_locator
    active = fixture / active_locator
    archive.mkdir(parents=True, exist_ok=True)
    task_payload = {
        "id": task_id, "name": task_id, "title": "Restore eval",
        "status": "completed", "completedAt": "2026-09-03T00:00:00Z",
        "branch": branch, "base_branch": "main", "repo_ref": repo_ref,
        "issue_number": pr_number, "pr_number": pr_number,
        "expected_head_sha": expected_head,
    }
    (archive / "task.json").write_text(json.dumps(task_payload) + "\n", encoding="utf-8")
    finish_summary = {
        "task_id": task_id, "repository": repo_ref, "pr_number": pr_number,
        "expected_head_sha": expected_head, "archive_commit": archive_commit,
    }
    (archive / "finish-summary.json").write_text(json.dumps(finish_summary) + "\n", encoding="utf-8")
    mapping_path = fixture / ".trellis/.runtime/guru-team/tasks" / f"{task_id}.json"
    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    mapping_path.write_text(json.dumps({
        "state": "archived", "task_id": task_id,
        "archive_locator": archive_locator, "active_locator": active_locator,
        "task_locator": archive_locator, "repository": repo_ref,
        "branch_name": branch, "worktree_path": str(worktree),
    }) + "\n", encoding="utf-8")

    public = json.loads(public_input_path.read_text(encoding="utf-8"))
    public.update({
        "exit_id": "phase2_reentry_required", "repo_ref": repo_ref,
        "pr_number": pr_number, "pr_url": f"https://github.com/{repo_ref}/pull/{pr_number}",
        "expected_head_sha": expected_head, "expected_base_branch": "main",
        "expected_head_branch": branch, "issue_number": pr_number, "task_id": task_id,
        "archive_locator": archive_locator, "active_locator": active_locator,
        "archive_commit": archive_commit, "finding_refs": ["merge-finding:348:phase2-reentry"],
        "resume_target": "phase-2",
    })
    semantic = {
        "schema_version": "1.0", "profile": "restore_archived_task", "mode": "workflow",
        "review_intent": "task_work_reentry", "classification": "task_work",
        "requires_task_content_change": True, "finding_refs": public["finding_refs"],
    }
    facts = json.loads((package / "examples/live-facts.json").read_text(encoding="utf-8"))
    facts["pr"].update({"state": "OPEN", "number": pr_number, "url": public["pr_url"], "head_sha": expected_head, "base_branch": "main", "head_branch": branch})
    facts["issue"].update({"number": pr_number, "state": "OPEN", "close_intent": "unchanged"})
    facts["remote_branch"].update({"name": branch, "head_sha": expected_head})
    facts["local_branch"].update({"name": branch, "head_sha": expected_head})
    facts["archive"].update({"locator": archive_locator, "commit": archive_commit, "task_json_sha256": hashlib.sha256((archive / "task.json").read_bytes()).hexdigest(), "finish_summary_sha256": hashlib.sha256((archive / "finish-summary.json").read_bytes()).hexdigest()})
    facts["task"].update({"id": task_id, "status": "completed", "completed_at": task_payload["completedAt"], "branch": branch, "base_branch": "main", "repo_ref": repo_ref, "issue_number": pr_number, "pr_number": pr_number, "expected_head_sha": expected_head})
    facts["runtime_mapping"].update({"state": "archived", "task_id": task_id, "archive_locator": archive_locator, "active_locator": active_locator, "repo_ref": repo_ref, "branch_name": branch, "worktree_path": str(worktree)})
    facts["worktree"].update({"path": str(worktree), "exists": True, "clean": True, "branch": branch, "occupied_by": None})
    facts["active_task"] = {"present": False, "task_id": None, "locator": None}
    if case == "idempotent":
        shutil.move(str(archive), str(active))
        task_payload["status"] = "in_progress"
        task_payload.pop("completedAt", None)
        (active / "task.json").write_text(json.dumps(task_payload) + "\n", encoding="utf-8")
        (active / "finish-summary.json").unlink()
        mapping_path.write_text(json.dumps({**json.loads(mapping_path.read_text()), "state": "active", "task_locator": active_locator}) + "\n", encoding="utf-8")
        current = fixture / ".trellis/.runtime/current-task"
        current.parent.mkdir(parents=True, exist_ok=True)
        current.write_text(active_locator + "\n", encoding="utf-8")
        facts["runtime_mapping"]["state"] = "active"
        facts["task"]["status"] = "in_progress"
        facts["active_task"] = {"present": True, "task_id": task_id, "locator": active_locator}
    blockers = facts["blockers"]
    if case == "external-blocker": blockers["provider"] = True
    elif case == "head-drift": facts["pr"]["head_sha"] = "2" * 40
    elif case == "scope-drift": blockers["scope_drift"] = True
    elif case == "dirty-worktree": facts["worktree"]["clean"] = False
    elif case == "active-task-conflict": facts["active_task"] = {"present": True, "task_id": "other-task", "locator": ".trellis/tasks/other-task"}
    elif case == "merged-pr": facts["pr"]["state"] = "MERGED"
    elif case not in {"success", "idempotent"}:
        raise ValueError(f"unsupported restore owner staging case: {case}")
    runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    input_path = runtime_dir / "restore-input.json"
    semantic_path = runtime_dir / "restore-semantic.json"
    facts_path = runtime_dir / "restore-facts.json"
    input_path.write_text(json.dumps(public) + "\n", encoding="utf-8")
    semantic_path.write_text(json.dumps(semantic) + "\n", encoding="utf-8")
    facts_path.write_text(json.dumps(facts) + "\n", encoding="utf-8")
    for relative in request.get("files", []):
        path = Path(request["workdir"]) / str(relative)
        try: payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError): continue
        invocation = payload.get("public_invocation") if isinstance(payload, dict) else None
        if isinstance(invocation, dict):
            invocation["arguments"] = ["--root", ".", "--input", str(input_path.relative_to(fixture)), "--semantic-result", str(semantic_path.relative_to(fixture)), "--facts", str(facts_path.relative_to(fixture))]
            path.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
    return package, fixture_runtime_target, {"GURU_TEAM_EVAL_STAGING": "1"}


def qualification_runtime_environment(owner_repository: Path) -> dict[str, str]:
    pointer = owner_repository / ".git/guru-team/python/active.json"
    if pointer.is_symlink() or not pointer.is_file():
        raise ValueError("qualification managed runtime pointer is unavailable")
    try:
        payload = json.loads(pointer.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("qualification managed runtime pointer is invalid") from exc
    if not isinstance(payload, dict) or set(payload) != {
        "schema_version", "cache_scope", "runtime_id", "interpreter",
    }:
        raise ValueError("qualification managed runtime pointer is invalid")
    runtime_id = payload.get("runtime_id")
    interpreter_value = payload.get("interpreter")
    if (
        payload.get("schema_version") != "2.0"
        or payload.get("cache_scope") != "user"
        or not isinstance(runtime_id, str)
        or len(runtime_id) != 24
        or any(character not in "0123456789abcdef" for character in runtime_id)
        or not isinstance(interpreter_value, str)
    ):
        raise ValueError("qualification managed runtime pointer is invalid")
    interpreter = Path(interpreter_value)
    if (
        not interpreter.is_absolute()
        or Path(os.path.abspath(interpreter)) != interpreter
        or len(interpreter.parents) < 4
    ):
        raise ValueError("qualification managed runtime interpreter path is invalid")
    runtime_root = interpreter.parents[2]
    cache_root = interpreter.parents[3]
    expected_interpreter = cache_root / runtime_id / "venv/bin/python"
    if (
        runtime_root != cache_root / runtime_id
        or interpreter != expected_interpreter
        or cache_root.is_symlink()
        or not cache_root.is_dir()
        or runtime_root.is_symlink()
        or not runtime_root.is_dir()
        or not interpreter.is_file()
        or not os.access(interpreter, os.X_OK)
    ):
        raise ValueError("qualification managed runtime identity is invalid")
    return {"GURU_TEAM_PYTHON_CACHE_ROOT": str(cache_root)}


def stage_owner_execution(
    request: dict[str, Any], execution_root: Path, runtime_target: Path,
) -> tuple[Path, Path, dict[str, str]]:
    skill_id = str(request["skill_id"])
    request_package = Path(request["package_root"]).resolve()
    fixture, _ = stage_clean_installed_owner_repo(
        execution_root, runtime_target, request_package,
    )
    if skill_id == QUALIFICATION_SKILL:
        package = fixture / ".trellis/guru-team/skills/packages" / skill_id
        if (
            hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
            != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
            or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
            != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
            or package_tree_sha256(package) != request.get("package_sha256")
        ):
            raise ValueError("qualification installed package does not match the evaluated contract")
        runtime_root = fixture / ".trellis/.runtime"
        if runtime_root.exists():
            residue = [path for path in runtime_root.rglob("*") if path.is_file()]
            if residue:
                raise ValueError("qualification fixture contains unexpected runtime residue")
            shutil.rmtree(runtime_root)
        normalize_qualification_owner_extension(fixture)
        stage_qualification_public_authoring_fixture(fixture)
        run_git(fixture, "add", ".")
        commit_qualification_owner_fixture(fixture)
        head = run_git(fixture, "rev-parse", "HEAD")
        run_git(fixture, "update-ref", "refs/remotes/origin/main", head)
        run_git(fixture, "remote", "add", "origin", "https://github.com/example/guru-extension.git")
        fixture_runtime_target = fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
        return package, fixture_runtime_target, qualification_runtime_environment(fixture)
    if skill_id == "guru-sync-base":
        package = fixture / ".trellis/guru-team/skills/packages" / skill_id
        if (
            hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
            != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
            or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
            != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
        ):
            raise ValueError("owner staging package does not match the evaluated package contract")
        run_git(fixture, "add", ".")
        run_git(fixture, "commit", "-q", "-m", "stage owner fixture")
        head = run_git(fixture, "rev-parse", "HEAD")
        run_git(fixture, "update-ref", "refs/remotes/origin/main", head)
        run_git(fixture, "remote", "add", "origin", "https://github.com/example/guru-extension.git")
        bind_sync_call_local_invocation(request, fixture)
        fake_bin = write_fake_gh(execution_root, "sync-base")
        fixture_runtime_target = fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
        return package, fixture_runtime_target, {
            "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
        }
    recipe, public_input, owner_staging = owner_recipe(request)
    if skill_id in PRODUCTION_SKILLS:
        return stage_production_owner_execution(
            request,
            fixture,
            runtime_target,
            request_package,
            recipe,
            public_input,
        )
    worktree_root = execution_root / "owner-worktrees"
    (fixture / ".trellis/guru-team/config.yml").write_text(
        f"workspace_mode: worktree\nworktree_root: {worktree_root}\n",
        encoding="utf-8",
    )
    evidence_files = {
        "docs/guide.md": "# Guide\n\nOriginal label.\n",
        "docs/follow-up.md": "# Follow-up\n\nOriginal follow-up remains untouched.\n",
        "docs/requirements.md": "# Requirements\n\nCurrent Stage 0 context evidence.\n",
        "docs/requirements/requirement-main.md": "# Contract\n\n本合同必须保持完整的语义审查。\n",
        "trellis/runtime.py": "STAGE0_CONTEXT_OWNER = 'runtime'\n",
        "trellis/test_runtime.py": "def test_stage0_context_owner():\n    assert True\n",
    }
    for relative, content in evidence_files.items():
        target = fixture / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    task = fixture / ".trellis/tasks/current"
    task_required = skill_id != "guru-execute-task-free-change" or recipe in {
        "task-free-resume-active-task", "task-free-scope-change",
    }
    if task_required:
        task.mkdir(parents=True, exist_ok=True)
        (task / "task.json").write_text(json.dumps({
            "id": "current", "name": "current", "title": "Stage 0 wording fixture",
            "status": "planning", "scope": "issue #145", "branch": "main", "base_branch": "main",
        }) + "\n", encoding="utf-8")
        for name, content in {
            "prd.md": "# PRD\n\n## Requirement\n\nThe exact Stage 0 public contract is required.\n",
            "design.md": "# Design\n\n## Docs SSOT Plan\n\nStrategy: ssot_first.\n",
            "implement.md": "# Implement\n\nRun the production wrapper and owner checker.\n",
        }.items():
            (task / name).write_text(content, encoding="utf-8")
    fixture_runtime_target = fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
    if fixture_runtime_target.is_symlink() or not os.access(fixture_runtime_target, os.X_OK):
        raise ValueError("fixture public invocation runtime is unavailable")
    package = fixture / ".trellis/guru-team/skills/packages" / skill_id
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("owner staging package does not match the evaluated package contract")
    runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    (fixture / OWNER_INPUT).write_bytes(public_input.read_bytes())
    public_payload = json.loads(public_input.read_text(encoding="utf-8"))
    if skill_id == "guru-maintain-architecture-baseline":
        constitution = public_payload["constitution"]
        if constitution["authority_status"] == "current":
            constitution_locator = Path(constitution["authority_locator"])
            if constitution_locator.is_absolute() or ".." in constitution_locator.parts:
                raise ValueError("architecture constitution fixture locator is unsafe")
            constitution_target = fixture / constitution_locator
            constitution_target.parent.mkdir(parents=True, exist_ok=True)
            constitution_target.write_text(
                "# Design Constitution\n\nCurrent project authority fixture.\n",
                encoding="utf-8",
            )
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-q", "-m", "stage owner fixture")
    head = run_git(fixture, "rev-parse", "HEAD")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", head)
    run_git(fixture, "remote", "add", "origin", "https://github.com/example/guru-extension.git")
    if skill_id in {
        "guru-select-workflow-mode",
        "guru-execute-task-free-change",
        "guru-bootstrap-repository-ssot",
        "guru-maintain-architecture-baseline",
        "guru-maintain-requirements-design-test-ssot",
    }:
        runtime = None
    elif skill_id == "guru-discover-change-context":
        runtime = load_package_runtime_module(
            fixture_runtime_target, skill_id, "common"
        )
    else:
        runtime = load_package_owner_runtime(fixture_runtime_target, skill_id)
    if hasattr(runtime, "write_runtime_mappings"):
        runtime.write_runtime_mappings(
            fixture,
            runtime.load_config(fixture),
            {
                "workspace_slug": "current",
                "task_slug": "current",
                "task_dir": ".trellis/tasks/current",
                "branch_name": "main",
            },
            fixture,
        )
    public_mode = str(public_payload.get("mode") or "")
    fake_bin = write_fake_gh(execution_root, recipe)
    environment = {"PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}"}
    previous_path = os.environ.get("PATH")
    os.environ["PATH"] = environment["PATH"]
    owner_context: dict[str, Any] = {}
    try:
        if skill_id == "guru-select-workflow-mode":
            owner = build_workflow_mode_owner(public_payload, recipe)
            if recipe in {"workflow-mode-unrelated-dirty", "workflow-mode-dirty-overlap"}:
                (fixture / "unrelated-user-note.txt").write_text(
                    "preserve this unrelated dirty file\n", encoding="utf-8"
                )
        elif skill_id == "guru-execute-task-free-change":
            guide = fixture / "docs/guide.md"
            if recipe in {"task-free-completed", "task-free-non-default-completed"}:
                guide.write_text("# Guide\n\nCorrected label.\n", encoding="utf-8")
                edited_paths = run_git(
                    fixture, "diff", "--name-only", "--", *public_payload["target_paths"]
                ).splitlines()
                if edited_paths != public_payload["target_paths"]:
                    raise ValueError("task-free completed staging lacks the exact bounded tracked edit")
                run_git(fixture, "diff", "--check", "--", *edited_paths)
            elif recipe in {
                "task-free-automatic-risk-expansion",
                "task-free-explicit-risk-expansion",
            }:
                guide.write_text("# Guide\n\nPartial correction revealed wider impact.\n", encoding="utf-8")
                edited_paths = run_git(
                    fixture, "diff", "--name-only", "--", *public_payload["target_paths"]
                ).splitlines()
                if edited_paths != [public_payload["target_paths"][0]]:
                    raise ValueError("task-free expansion staging did not stop after the first tracked edit")
                remaining = fixture / public_payload["target_paths"][1]
                if remaining.read_text(encoding="utf-8") != evidence_files[public_payload["target_paths"][1]]:
                    raise ValueError("task-free expansion staging performed a prohibited remaining write")
                run_git(fixture, "diff", "--check", "--", *edited_paths)
            elif recipe == "task-free-location-dirty-overlap":
                guide.write_text("# Guide\n\nUser-owned overlapping edit.\n", encoding="utf-8")
            owner = build_task_free_change_owner(public_payload, recipe)
        elif skill_id == "guru-clarify-requirements":
            owner = build_clarity_owner(runtime, package, recipe)
        elif skill_id == "guru-discover-change-context":
            owner = build_context_owner(runtime, fixture, package, recipe)
        elif skill_id == "guru-review-contract-wording":
            owner, change_request = build_wording_owner(
                runtime, fixture, package, recipe
            )
            if owner.get("profile") == "change_request":
                owner_context["change_request"] = change_request
        elif skill_id == "guru-review-change-request":
            owner, _, change_request = build_readiness_owner(
                runtime,
                fixture,
                package,
                recipe,
                public_mode,
                str(public_payload.get("profile") or ""),
            )
            owner_context = {"change_request": change_request}
        elif skill_id == "guru-create-task-workspace":
            owner = build_workspace_owner(runtime, fixture, recipe, public_mode)
        elif skill_id == "guru-maintain-architecture-baseline":
            if recipe in {
                "architecture-no-impact",
                "architecture-next-task",
                "architecture-bootstrap-current",
                "architecture-repair-current",
            }:
                baseline_identity = str(public_payload["baseline"]["identity"])
                impact_reason = (
                    "The reviewed task changes no architecture authority, owner, "
                    "boundary, decision, or GAP."
                )
                if recipe == "architecture-bootstrap-current":
                    baseline_identity = str(
                        public_payload["successor_baseline"]["identity"]
                    )
                    impact_reason = (
                        "The reviewed foundation bootstrap activates the declared "
                        "successor baseline without introducing a second authority."
                    )
                elif recipe == "architecture-repair-current":
                    impact_reason = (
                        "The reviewed repair restores the declared project Architecture "
                        "contract without changing its authority boundary."
                    )
                selected = {
                    "typed_exit": "baseline_current",
                    "task_locator": str(public_payload["task_locator"]),
                    "baseline_identity": baseline_identity,
                    "constitution_identity": str(public_payload["constitution"]["identity"]),
                    "impact_kind": "no_architecture_impact",
                    "impact_reason": impact_reason,
                    "promotion_state": "no_change",
                }
            elif recipe in {
                "architecture-target-native",
                "architecture-legacy-convergence",
                "architecture-refactor-slice",
            }:
                descriptors = copy.deepcopy(owner_staging.get("project_check_descriptors"))
                if not isinstance(descriptors, list) or not descriptors:
                    raise ValueError(
                        "architecture owner staging lacks project authority check descriptors"
                    )
                change_path = {
                    "architecture-target-native": "target_native",
                    "architecture-legacy-convergence": "legacy_boundary_convergence",
                    "architecture-refactor-slice": "dedicated_refactor_slice",
                }[recipe]
                selected = {
                    "typed_exit": "baseline_current",
                    "task_locator": str(public_payload["task_locator"]),
                    "baseline_identity": str(public_payload["baseline"]["identity"]),
                    "constitution_identity": str(public_payload["constitution"]["identity"]),
                    "impact_kind": "architecture_impact",
                    "impact_reason": "The reviewed task changes an architecture boundary and follows the selected convergence path.",
                    "change_path": change_path,
                    "promotion_state": "reviewed_candidate",
                    "contribution_locator": "docs/architecture/contributions/eval-task",
                    "contribution_identity": "contribution-v1",
                    "project_check_descriptors": descriptors,
                    "project_checks": [
                        {
                            "schema_version": "2.0",
                            "descriptor_identity": descriptor["descriptor_identity"],
                            "check_id": descriptor["check_id"],
                            "check_version": descriptor["check_version"],
                            "applicability": "applicable",
                            "blocking": True,
                            "applicable_scope": copy.deepcopy(descriptor["applicable_scope"]),
                            "rule_refs": copy.deepcopy(descriptor["rule_refs"]),
                            "decision_refs": copy.deepcopy(descriptor["decision_refs"]),
                            "gap_refs": copy.deepcopy(descriptor["gap_refs"]),
                            "before": {"state": "one owner and one open GAP"},
                            "after": {"state": "one owner and no worsened deviation"},
                            "status": "pass",
                            "evidence_locator": "docs/architecture/evidence/eval.md",
                            "freshness_identity": str(public_payload["freshness_identity"]),
                        }
                        for descriptor in descriptors
                    ],
                }
            elif recipe == "architecture-scope-expansion":
                selected = {
                    "typed_exit": "contract_incomplete",
                    "task_locator": str(public_payload["task_locator"]),
                    "missing_refs": ["expanded-scope-reassessment"],
                    "return_route": "planning",
                }
            elif recipe == "architecture-fitness-regression":
                selected = {
                    "typed_exit": "fitness_regression",
                    "task_locator": str(public_payload["task_locator"]),
                    "regression_refs": ["second-authority"],
                    "return_route": "implementation",
                }
            elif recipe == "architecture-parallel-stale":
                selected = {
                    "typed_exit": "sync_required",
                    "task_locator": str(public_payload["task_locator"]),
                    "sync_kind": "baseline_advanced",
                    "expected_current_identity": str(public_payload["expected_current_identity"]),
                    "current_identity": str(public_payload["current_identity"]),
                    "sync_target": copy.deepcopy(public_payload["sync_target"]),
                }
            elif recipe == "architecture-unpromoted":
                selected = {
                    "typed_exit": "sync_required",
                    "task_locator": str(public_payload["task_locator"]),
                    "sync_kind": "promotion_required",
                    "expected_current_identity": str(public_payload["baseline"]["identity"]),
                    "current_identity": str(public_payload["baseline"]["identity"]),
                    "sync_target": {
                        "kind": "contribution",
                        "locator": "docs/architecture/contributions/eval-task",
                        "expected_identity": "contribution-v1",
                        "current_identity": "contribution-v1",
                    },
                }
            elif recipe == "architecture-missing-evidence":
                selected = {
                    "typed_exit": "contract_incomplete",
                    "task_locator": str(public_payload["task_locator"]),
                    "missing_refs": ["applicable-external-evidence"],
                    "return_route": "repair",
                }
            else:
                raise ValueError(f"unsupported architecture baseline owner staging recipe: {recipe}")
            owner = {
                "schema_version": "2.0",
                "profile": public_payload["profile"],
                "mode": public_payload["mode"],
                "continuation_id": public_payload["continuation_id"],
                "stage": public_payload["stage"],
                "input_sha256": hashlib.sha256(
                    json.dumps(
                        public_payload,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    ).encode()
                ).hexdigest(),
                "baseline": dict(public_payload["baseline"]),
                "constitution": dict(public_payload["constitution"]),
                "project_contract": dict(public_payload["project_contract"]),
                "freshness_identity": str(public_payload["freshness_identity"]),
                **({
                    "expected_current_identity": str(public_payload["expected_current_identity"]),
                    "current_identity": str(public_payload["current_identity"]),
                    "sync_kind": str(public_payload["sync_kind"]),
                    "sync_target": copy.deepcopy(public_payload["sync_target"]),
                } if public_payload["profile"] == "promotion" else {}),
                "ai_review_gate": {
                    "status": "passed",
                    "reviewed_scope": "Current Architecture authority, task-local change contract, project checks, and lifecycle stage.",
                    "evidence_summary": "The project-neutral eval facts bind the baseline, constitution, contribution, before/after state, and freshness identity.",
                    "findings": [],
                    "conclusion": "The expected typed route is justified by the evaluated scenario.",
                },
                "consumer": {
                    "baseline_current": {"kind": "workflow", "id": "guru-architecture-baseline-current-router"},
                    "sync_required": {"kind": "skill", "id": "guru-maintain-architecture-baseline"},
                    "baseline_incomplete": {"kind": "workflow", "id": "guru-architecture-baseline-bootstrap-router"},
                    "architecture_conflict": {"kind": "workflow", "id": "guru-architecture-baseline-planning-router"},
                    "contract_incomplete": {"kind": "workflow", "id": "guru-architecture-baseline-planning-router"},
                    "fitness_regression": {"kind": "workflow", "id": "guru-architecture-baseline-check-router"},
                    "blocked": {"kind": "stop", "id": "architecture-baseline-blocked"},
                }[selected["typed_exit"]],
                **selected,
            }
        elif skill_id == "guru-bootstrap-repository-ssot":
            expected = {
                "bootstrap-baseline-incomplete": "baseline_incomplete",
                "bootstrap-completed": "completed",
                "bootstrap-repair-required": "repair_required",
                "bootstrap-blocked": "blocked",
            }.get(recipe)
            if expected is None:
                raise ValueError(
                    f"unsupported repository SSOT Bootstrap owner staging recipe: {recipe}"
                )
            owner = {
                "profile": public_payload["profile"],
                "continuation_id": public_payload["continuation_id"],
                "typed_exit": expected,
            }
        elif skill_id == "guru-maintain-requirements-design-test-ssot":
            if recipe == "rdt-bootstrap-incomplete":
                selected = {
                    "typed_exit": "baseline_incomplete",
                    "authority_locator": "docs",
                    "known_status": "partial",
                    "applicability_scope": "repository",
                    "missing_layer_code": "test",
                }
            elif recipe == "rdt-impact-current":
                selected = {
                    "typed_exit": "ssot_current",
                    "authority_locator": "docs",
                    "active_version": "1.0",
                    "status": "active",
                    "applicability_scope": "repository",
                    "freshness": "authority-v1",
                }
            elif recipe == "rdt-impact-revision":
                selected = {
                    "typed_exit": "revision_required",
                    "task_locator": str(public_payload["task_locator"]),
                    "affected_scope": "requirements-design-test traceability",
                    "authority_locator": str(public_payload["authority_locator"]),
                    "authority_version": str(public_payload["authority_version"]),
                    "revision_code": "traceability_revision",
                }
            elif recipe == "rdt-impact-sync":
                selected = {
                    "typed_exit": "sync_required",
                    "authority_locator": str(public_payload["authority_locator"]),
                    "target_version": "1.1",
                    "contribution_locator": "docs/requirements-design-test-contributions/example-c",
                    "sync_kind": "promotion",
                    "freshness": str(public_payload["authority_freshness"]),
                }
            elif recipe == "rdt-promotion-sync":
                selected = {
                    "typed_exit": "ssot_current",
                    "authority_locator": str(public_payload["authority_locator"]),
                    "active_version": str(public_payload["target_version"]),
                    "status": "active",
                    "applicability_scope": "repository",
                    "freshness": str(public_payload["freshness"]),
                }
            elif recipe == "rdt-repair-blocked":
                selected = {
                    "typed_exit": "blocked",
                    "reason_code": "stale_identity",
                    "remediation": "Reread the current authority and repeat semantic review.",
                }
            else:
                raise ValueError(
                    "unsupported Requirements Design Test SSOT owner staging recipe: "
                    f"{recipe}"
                )
            owner = {
                "profile": public_payload["profile"],
                "mode": public_payload["mode"],
                "continuation_id": public_payload["continuation_id"],
                "input_sha256": hashlib.sha256(
                    json.dumps(
                        public_payload,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    ).encode()
                ).hexdigest(),
                "architecture_baseline": dict(public_payload["architecture_baseline"]),
                "ai_review_gate": {
                    "status": "blocked" if selected["typed_exit"] == "blocked" else "passed",
                    "reviewed_scope": "Current Requirements Design Test authority and selected profile.",
                    "evidence_summary": "The eval facts bind the live authority, contribution, traceability, and Architecture Baseline identity.",
                    "findings": [],
                    "conclusion": "The expected typed exit is justified by the evaluated scenario.",
                },
                "consumer": {
                    "ssot_current": {"kind": "workflow", "id": "guru-requirements-design-test-ssot-current-router"},
                    "sync_required": {"kind": "skill", "id": "guru-maintain-requirements-design-test-ssot"},
                    "revision_required": {"kind": "workflow", "id": "guru-requirements-design-test-ssot-planning-router"},
                    "baseline_incomplete": {"kind": "workflow", "id": "guru-requirements-design-test-ssot-bootstrap-router"},
                    "blocked": {"kind": "stop", "id": "requirements-design-test-ssot-blocked"},
                }[selected["typed_exit"]],
                **selected,
            }
        else:
            raise ValueError(f"owner staging is not implemented for {skill_id}")
    finally:
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path
    owner_path = fixture / OWNER_RESULT
    owner_path.parent.mkdir(parents=True, exist_ok=True)
    owner_path.write_text(json.dumps(owner) + "\n", encoding="utf-8")
    if skill_id in {
        "guru-discover-change-context",
        "guru-clarify-requirements",
        "guru-review-contract-wording",
        "guru-review-change-request",
        "guru-create-task-workspace",
    }:
        bind_stage0_call_local_invocation(
            request,
            fixture,
            json.loads((fixture / OWNER_INPUT).read_text(encoding="utf-8")),
            owner,
            owner_context,
        )
    elif skill_id != "guru-review-branch":
        bind_owner_result_argument(request, fixture, owner_path)
    return package, fixture_runtime_target, environment


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
