from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys

from adapters.eval.eval_constants import (
    MINIMAL_NATIVE_ENVIRONMENT_KEYS,
    QUALIFICATION_MODEL,
    QUALIFICATION_MODEL_REQUEST_SCHEMA,
    QUALIFICATION_PERMISSION_PROFILE,
    QUALIFICATION_PROMPT_PROTOCOL,
    QUALIFICATION_PUBLIC_AUTHORING_FACTS,
    QUALIFICATION_SKILL,
    QUALIFICATION_TRACE_HELPER_BODY,
    SECRET_ENVIRONMENT_MARKERS,
)

from adapters.eval.fixture_io import (
    run_git,
)


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
