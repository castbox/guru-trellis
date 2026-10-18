"""Package-local deterministic runtime extracted from the frozen owner implementation."""

from __future__ import annotations

import argparse

import copy

import hashlib

import importlib.util

import json

import os

import re

import shlex

import shutil

import subprocess

import sys

import tempfile

import time

import unicodedata

from pathlib import Path

from typing import Any

from urllib.parse import urlsplit

try:
    from runtime.reviewed_content import (
        PROVENANCE_TAIL_MANIFEST_PATH,
        ReviewedContentError,
        reviewed_content_identity as canonical_reviewed_content_identity,
    )
except ModuleNotFoundError:
    for runtime_parent in Path(__file__).resolve().parents:
        if (
            (runtime_parent / "runtime/reviewed_content.py").is_file()
            and (runtime_parent / "runtime/io.py").is_file()
        ):
            sys.path.insert(0, str(runtime_parent))
            break
    else:
        raise
    from runtime.reviewed_content import (
        PROVENANCE_TAIL_MANIFEST_PATH,
        ReviewedContentError,
        reviewed_content_identity as canonical_reviewed_content_identity,
    )

from runtime.temporary_lifecycle import temporary_directory

def _load_contract_validation() -> Any:
    path = Path(__file__).resolve().with_name("contract_validation.py")
    module_name = (
        "guru_verify_extension_installation_contract_validation_"
        + hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:16]
    )
    module = sys.modules.get(module_name)
    if module is not None:
        return module
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ModuleNotFoundError(f"Cannot load package-local validation runtime: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


_contract_validation = _load_contract_validation()
for _contract_name in (
    "EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER",
    "EXTENSION_VERIFICATION_TARGET_CHECKOUT_OWNER",
    "SKILL_ECMA_DOT_PATTERN",
    "SKILL_ECMA_WHITESPACE_CLASS",
    "SKILL_SCHEMA_DIALECT",
    "SKILL_UTF16_HIGH_SURROGATE",
    "SKILL_UTF16_LOW_SURROGATE",
    "SKILL_UTF16_SURROGATE_PAIR",
    "SkillPortablePattern",
    "SkillPortablePatternError",
    "context_canonical_bytes",
    "context_digest",
    "context_sort",
    "extension_verification_semantic_shape_errors",
    "extension_verification_sensitive_text",
    "skill_compile_portable_pattern",
    "skill_ecma_code_point_complement",
    "skill_format_matches",
    "skill_json_dumps",
    "skill_json_equal",
    "skill_json_loads",
    "skill_json_nonfinite_paths",
    "skill_json_schema_subset_errors",
    "skill_json_schema_validation_errors",
    "skill_lexical_relative",
    "skill_lstat_path",
    "skill_read_json",
    "skill_read_schema",
    "skill_rfc3339_date_time_matches",
    "skill_safe_relative",
    "skill_uri_matches",
    "skill_utf16_code_units",
):
    globals()[_contract_name] = getattr(_contract_validation, _contract_name)

DEFAULTS: dict[str, Any] = {
    "github_repo": "",
    "source_issue_required": False,
    "duplicate_search_required": True,
    "duplicate_candidate_limit": 5,
    "duplicate_high_similarity_action": "confirm",
    "branch_type_default": "chore",
    "base_branch": "",
    "base_branch_candidates": ["dev", "develop", "main", "master"],
    "workspace_mode": "worktree",
    "worktree_root": "",
    "runtime_root": ".trellis/.runtime/guru-team",
    "marketplace_verification_artifact": "marketplace-verification.json",
    "artifact_language": "zh-CN",
    "publish": {
        "remote": "origin",
    },
    "created_issue_labels": [],
    "closeout_markers": ["最终收口口径", "Final Closeout"],
}

GURU_TEAM_EXTENSION_MANIFEST = Path(".trellis/guru-team/extension.json")

class WorkflowError(RuntimeError):
    def __init__(self, message: str, exit_code: int = 1, payload: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.exit_code = exit_code
        self.payload = payload or {}

def run(
    cmd: list[str],
    cwd: Path | None = None,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    process_env = None if env is None else {**os.environ, **env}
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=check,
        env=process_env,
    )

def run_stdout(
    cmd: list[str], cwd: Path | None = None, env: dict[str, str] | None = None
) -> str:
    try:
        if env is None:
            return run(cmd, cwd=cwd).stdout.strip()
        return run(cmd, cwd=cwd, env=env).stdout.strip()
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        raise WorkflowError(f"Command failed: {shlex.join(cmd)}\n{stderr}") from exc

def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", '""', "''"}:
        return ""
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value

def load_config(root: Path) -> dict[str, Any]:
    config = copy.deepcopy(DEFAULTS)
    path = root / ".trellis/guru-team/config.yml"
    if not path.exists():
        return config

    current_key: str | None = None
    current_nested_key: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        text = line.strip()
        if text.startswith("- "):
            value = parse_scalar(text[2:])
            if indent >= 4 and current_key and current_nested_key and isinstance(config.get(current_key), dict):
                nested = config[current_key].setdefault(current_nested_key, [])
                if isinstance(nested, list):
                    nested.append(value)
            elif current_key:
                existing = config.setdefault(current_key, [])
                if isinstance(existing, list):
                    existing.append(value)
            continue
        if ":" not in text:
            continue
        key, value = text.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if indent == 0:
            current_key = key
            current_nested_key = None
            if value == "":
                default_value = config.get(key)
                config[key] = copy.deepcopy(default_value) if isinstance(default_value, dict) else []
            else:
                config[key] = parse_scalar(value)
        elif current_key and isinstance(config.get(current_key), dict):
            current_nested_key = key
            if value == "":
                config[current_key][key] = []
            else:
                config[current_key][key] = parse_scalar(value)
        else:
            config[key] = parse_scalar(value)
    return config

def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".trellis").is_dir():
            return candidate
    top = run_stdout(["git", "rev-parse", "--show-toplevel"], cwd=current)
    return Path(top).resolve()

def normalize_github_repository(value: Any) -> str:
    if not isinstance(value, str) or not value:
        return ""
    raw = value
    parts = raw.split("/")
    if len(parts) != 2:
        return ""
    owner, repository = parts
    component = re.compile(r"^[A-Za-z0-9_.-]+$")
    if (
        not component.fullmatch(owner)
        or not component.fullmatch(repository)
        or owner in {".", ".."}
        or repository in {".", ".."}
    ):
        return ""
    return f"{owner}/{repository}".casefold()

def git_remote_config_value_is_safe(value: Any) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and not value[0].isspace()
        and not value[-1].isspace()
        and not any(unicodedata.category(character).startswith("C") for character in value)
    )

def parse_github_remote_repository_url(value: Any) -> str:
    if not git_remote_config_value_is_safe(value):
        return ""
    raw = value
    scp = re.fullmatch(r"git@(?i:github\.com):(.+)", raw)
    if scp:
        path = scp.group(1)
    else:
        try:
            parsed = urlsplit(raw)
            port = parsed.port
        except ValueError:
            return ""
        if parsed.query or parsed.fragment or port is not None:
            return ""
        hostname = str(parsed.hostname or "").casefold()
        if parsed.scheme == "https":
            if (
                hostname != "github.com"
                or parsed.username is not None
                or parsed.password is not None
            ):
                return ""
        elif parsed.scheme == "ssh":
            if (
                hostname != "github.com"
                or parsed.username != "git"
                or parsed.password is not None
            ):
                return ""
        else:
            return ""
        if not parsed.path.startswith("/") or parsed.path.startswith("//"):
            return ""
        path = parsed.path[1:]
    if path.endswith("/"):
        return ""
    path = path.removesuffix(".git")
    return normalize_github_repository(path)

def current_branch(root: Path) -> str:
    proc = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root, check=False)
    value = proc.stdout.strip()
    if proc.returncode == 0 and value and value != "HEAD":
        return value
    proc = run(["git", "symbolic-ref", "--short", "HEAD"], cwd=root, check=False)
    value = proc.stdout.strip()
    return value or "HEAD"

def current_head(root: Path) -> str:
    return run_stdout(["git", "rev-parse", "HEAD"], cwd=root)

def reviewed_content_identity(
    root: Path,
    commit: str = "HEAD",
    include_worktree: bool = True,
) -> dict[str, str]:
    try:
        return canonical_reviewed_content_identity(root, commit, include_worktree)
    except ReviewedContentError as exc:
        raise WorkflowError(str(exc), exit_code=2, payload=exc.payload) from exc

def runtime_root(root: Path, config: dict[str, Any]) -> Path:
    rel = Path(str(config.get("runtime_root") or DEFAULTS["runtime_root"]))
    return rel if rel.is_absolute() else root / rel

def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkflowError(f"Required JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"Invalid JSON file: {path}\n{exc}") from exc
    if not isinstance(payload, dict):
        raise WorkflowError(f"Invalid JSON file: {path}\nJSON root must be an object.", exit_code=2)
    return payload

def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json_document_bytes(payload).decode("utf-8")
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        tmp_path.replace(path)
    finally:
        tmp_path.unlink(missing_ok=True)

def json_document_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def read_optional_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, "missing"
    except json.JSONDecodeError as exc:
        return None, f"invalid: {exc}"
    if not isinstance(payload, dict):
        return None, "invalid: JSON root is not an object"
    return payload, None

def publish_config(config: dict[str, Any]) -> dict[str, Any]:
    value = config.get("publish")
    return value if isinstance(value, dict) else dict(DEFAULTS["publish"])

def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def repo_relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)

def canonical_json_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def task_commit_index_identity(
    root: Path, path: str, git_env: dict[str, str] | None = None
) -> tuple[str | None, str | None]:
    proc = subprocess.run(
        ["git", "--literal-pathspecs", "ls-files", "-s", "-z", "--", path],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=None if git_env is None else {**os.environ, **git_env},
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Could not read the literal task commit index identity.",
            exit_code=2,
            payload={"stderr": proc.stderr.decode("utf-8", "replace")},
        )
    records = [record for record in proc.stdout.split(b"\0") if record]
    if not records:
        return None, None
    if len(records) != 1:
        raise WorkflowError("Task commit index identity is ambiguous for a literal path.", exit_code=2)
    metadata_raw, separator, record_path = records[0].partition(b"\t")
    if not separator or record_path.decode("utf-8", "strict") != path:
        raise WorkflowError("Task commit index identity did not return the exact literal path.", exit_code=2)
    metadata = metadata_raw.decode("ascii", "strict").split()
    if len(metadata) != 3 or metadata[2] != "0":
        raise WorkflowError("Task commit index identity has an invalid or unmerged record.", exit_code=2)
    return metadata[1], metadata[0]

def task_commit_gitlink_worktree_identity(root: Path, path: str) -> dict[str, Any]:
    target = root / path
    try:
        metadata = target.lstat()
    except FileNotFoundError as exc:
        raise WorkflowError(
            "Task commit gitlink worktree is not initialized.", exit_code=2
        ) from exc
    if not stat.S_ISDIR(metadata.st_mode):
        raise WorkflowError(
            "Task commit gitlink worktree is not an exact directory.", exit_code=2
        )

    top_proc = subprocess.run(
        ["git", "-C", str(target), "rev-parse", "--show-toplevel"],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    top_value = top_proc.stdout.decode("utf-8", "strict").rstrip("\n") if top_proc.returncode == 0 else ""
    try:
        exact_root = target.resolve(strict=True)
        reported_root = Path(top_value).resolve(strict=True) if top_value else None
    except (OSError, RuntimeError) as exc:
        raise WorkflowError(
            "Task commit gitlink worktree root is ambiguous.", exit_code=2
        ) from exc
    if top_proc.returncode != 0 or reported_root != exact_root:
        raise WorkflowError(
            "Task commit gitlink worktree is uninitialized or root-mismatched.", exit_code=2
        )

    head_proc = subprocess.run(
        ["git", "-C", str(target), "rev-parse", "--verify", "HEAD^{commit}"],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    head = head_proc.stdout.decode("ascii", "strict").strip() if head_proc.returncode == 0 else ""
    if head_proc.returncode != 0 or re.fullmatch(r"[0-9a-f]{40,64}", head) is None:
        raise WorkflowError(
            "Task commit gitlink worktree HEAD is missing or ambiguous.", exit_code=2
        )

    status_proc = subprocess.run(
        [
            "git", "-C", str(target), "status", "--porcelain=v1", "-z",
            "--untracked-files=all", "--ignore-submodules=none",
        ],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if status_proc.returncode != 0:
        raise WorkflowError(
            "Could not inspect the task commit gitlink worktree state.", exit_code=2
        )
    if status_proc.stdout:
        raise WorkflowError(
            "Task commit gitlink worktree must be clean before candidate capture.", exit_code=2
        )
    return {
        "gitlink_head": head,
        "gitlink_initialized": True,
        "gitlink_dirty": False,
    }

def task_commit_worktree_content(
    root: Path, path: str
) -> tuple[bytes | None, str | None, str | None]:
    target = root / path
    try:
        metadata = target.lstat()
    except FileNotFoundError:
        return None, None, None
    if stat.S_ISLNK(metadata.st_mode):
        content = os.fsencode(os.readlink(target))
        return content, hashlib.sha256(content).hexdigest(), "120000"
    if not stat.S_ISREG(metadata.st_mode):
        return None, None, None
    mode = "100755" if metadata.st_mode & stat.S_IXUSR else "100644"
    content = target.read_bytes()
    return content, hashlib.sha256(content).hexdigest(), mode

def task_commit_worktree_identity(root: Path, path: str) -> tuple[str | None, str | None]:
    _, content_sha256, mode = task_commit_worktree_content(root, path)
    return content_sha256, mode

def task_commit_porcelain_status_records(root: Path) -> list[dict[str, Any]]:
    proc = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Could not capture the task commit Git snapshot.",
            exit_code=2,
            payload={"stderr": proc.stderr.decode("utf-8", "replace")},
        )
    fields = proc.stdout.split(b"\0")
    records: list[dict[str, Any]] = []
    index = 0
    while index < len(fields):
        field = fields[index]
        index += 1
        if not field:
            continue
        if len(field) < 4:
            raise WorkflowError("Git returned an invalid porcelain status record.", exit_code=2)
        status_text = field[:2].decode("ascii", "strict")
        if status_text in {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}:
            raise WorkflowError(
                "Reviewed Git state contains an unresolved merge entry.",
                exit_code=2,
            )
        path = field[3:].decode("utf-8", "strict")
        renamed_from: str | None = None
        copied_from: str | None = None
        relation_kinds = {item for item in status_text if item in {"R", "C"}}
        if len(relation_kinds) > 1:
            raise WorkflowError(
                "Git returned an ambiguous rename/copy status record.", exit_code=2
            )
        if relation_kinds:
            if index >= len(fields) or not fields[index]:
                raise WorkflowError(
                    "Git returned an incomplete rename/copy status record.", exit_code=2
                )
            relation_source = fields[index].decode("utf-8", "strict")
            index += 1
            if relation_kinds == {"R"}:
                renamed_from = relation_source
            else:
                copied_from = relation_source
        records.append({
            "status_text": status_text,
            "path": path,
            "renamed_from": renamed_from,
            "copied_from": copied_from,
        })
    return records

def task_commit_snapshot_entry(
    root: Path,
    record: dict[str, Any],
) -> dict[str, Any]:
    status_text = str(record["status_text"])
    path = str(record["path"])
    index_status = "" if status_text[0] == " " else status_text[0]
    worktree_status = "" if status_text[1] == " " else status_text[1]
    untracked = status_text == "??"
    index_blob, index_mode = task_commit_index_identity(root, path)
    worktree_sha256, worktree_mode = task_commit_worktree_identity(root, path)
    deleted = "D" in status_text
    entry = {
        "path": path,
        "index_status": index_status,
        "worktree_status": worktree_status,
        "untracked": untracked,
        "deleted": deleted,
        "renamed_from": record.get("renamed_from"),
        "copied_from": record.get("copied_from"),
        "index_blob": index_blob,
        "worktree_sha256": worktree_sha256,
        "mode": worktree_mode or index_mode,
    }
    if index_mode == "160000":
        if deleted and not (root / path).exists():
            entry.update(
                {
                    "gitlink_head": None,
                    "gitlink_initialized": False,
                    "gitlink_dirty": None,
                }
            )
        else:
            entry.update(task_commit_gitlink_worktree_identity(root, path))
    return entry

EXTENSION_VERIFICATION_SKILL_ID = "guru-verify-extension-installation"

EXTENSION_VERIFICATION_SCHEMA_VERSION = "5.0"

EXTENSION_VERIFICATION_RESULT_SCHEMA_VERSION = "5.0"

EXTENSION_VERIFICATION_CAPABILITIES = (
    "marketplace_index",
    "new_repo_init",
    "existing_repo_preview_switch",
    "preset_initial_apply",
    "preset_reapply",
    "trellis_update_reapply",
    "managed_conflict_sidecars",
    "skill_contract_discovery",
    "platform_equality",
    "ownership_inventory",
    "readme_commands",
    "redaction",
)

EXTENSION_VERIFICATION_ASSET_CATEGORIES = (
    "workflow",
    "preset",
    "schema",
    "skill",
    "platform",
)

EXTENSION_VERIFICATION_FAILURE_TAIL_LIMIT = 2000

EXTENSION_VERIFICATION_FAILURE_STAGES = {
    "pre-matrix",
    "matrix-cell",
    "post-matrix",
}

EXTENSION_VERIFICATION_CAPABILITY_ASSET_CATEGORIES = {
    "marketplace_index": ("workflow",),
    "new_repo_init": ("workflow", "preset"),
    "existing_repo_preview_switch": ("workflow", "preset"),
    "preset_initial_apply": ("preset", "schema"),
    "preset_reapply": ("preset", "schema"),
    "trellis_update_reapply": ("workflow", "preset", "schema"),
    "managed_conflict_sidecars": ("preset",),
    "skill_contract_discovery": ("schema", "skill"),
    "platform_equality": ("skill", "platform"),
    "ownership_inventory": ("preset",),
    "readme_commands": ("workflow", "preset"),
    "redaction": ("schema", "skill"),
}

EXTENSION_VERIFICATION_CAPABILITY_COMMAND_REFS = {
    "marketplace_index": (
        "resolve_target_ref",
        "clone_target",
        "verify_target_checkout",
        "resolve_extension_source_ref",
        "clone_extension_source",
        "configure_extension_source_origin",
        "verify_extension_source_checkout",
        "verify_throwaway_installation",
    ),
    "new_repo_init": (
        "clone_extension_source",
        "configure_extension_source_origin",
        "verify_extension_source_checkout",
        "verify_throwaway_installation",
    ),
    "existing_repo_preview_switch": (
        "clone_extension_source",
        "configure_extension_source_origin",
        "verify_extension_source_checkout",
        "verify_throwaway_installation",
    ),
    "preset_initial_apply": (
        "configure_extension_source_origin",
        "verify_throwaway_installation",
    ),
    "preset_reapply": (
        "configure_extension_source_origin",
        "verify_throwaway_installation",
    ),
    "trellis_update_reapply": (
        "resolve_extension_source_ref",
        "configure_extension_source_origin",
        "verify_throwaway_installation",
    ),
    "managed_conflict_sidecars": (
        "configure_extension_source_origin",
        "verify_throwaway_installation",
    ),
    "skill_contract_discovery": (
        "clone_extension_source",
        "configure_extension_source_origin",
        "verify_throwaway_installation",
    ),
    "platform_equality": (
        "clone_extension_source",
        "configure_extension_source_origin",
        "verify_throwaway_installation",
    ),
    "ownership_inventory": (
        "clone_extension_source",
        "configure_extension_source_origin",
        "verify_throwaway_installation",
    ),
    "readme_commands": (
        "resolve_extension_source_ref",
        "configure_extension_source_origin",
        "verify_throwaway_installation",
    ),
    "redaction": (
        "configure_extension_source_origin",
        "verify_throwaway_installation",
    ),
}

def command_evidence(command: list[str], proc: subprocess.CompletedProcess[str], display_command: list[str] | None = None) -> dict[str, Any]:
    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()
    return {
        "command": display_command or command,
        "exit_code": proc.returncode,
        "stdout_sha256": digest_text(stdout),
        "stderr_sha256": digest_text(stderr),
        "stdout_size_bytes": len(stdout.encode("utf-8")),
        "stderr_size_bytes": len(stderr.encode("utf-8")),
        "passed": proc.returncode == 0,
    }

def extension_verification_command_evidence(
    evidence_id: str,
    checkout_owner: str,
    command: list[str],
    proc: subprocess.CompletedProcess[str],
    display_command: list[str] | None = None,
) -> dict[str, Any]:
    evidence = command_evidence(command, proc, display_command)
    return {
        "id": evidence_id,
        "checkout_owner": checkout_owner,
        "argv": evidence["command"],
        "exit_code": evidence["exit_code"],
        "stdout_sha256": evidence["stdout_sha256"],
        "stderr_sha256": evidence["stderr_sha256"],
        "stdout_size_bytes": evidence["stdout_size_bytes"],
        "stderr_size_bytes": evidence["stderr_size_bytes"],
    }

def extension_verification_sanitize_failure_tail(value: str) -> str:
    text = value.replace("\x00", "")
    text = re.sub(
        r"(?is)-----BEGIN [^-\r\n]*PRIVATE KEY-----.*?(?:-----END [^-\r\n]*PRIVATE KEY-----|$)",
        "<redacted-private-key>",
        text,
    )
    text = re.sub(r"(?i)(https?://)[^/\s@]+@", r"\1<redacted>@", text)
    text = re.sub(
        r"(?i)(github_pat_|ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9_]+",
        "<redacted-token>",
        text,
    )
    text = re.sub(
        r"(?i)(x-access-token:)[^@\s]+",
        r"\1<redacted>",
        text,
    )
    text = re.sub(
        r"(?i)(authorization:\s*(?:bearer|basic)\s+)[^\s]+",
        r"\1<redacted>",
        text,
    )
    text = re.sub(
        r"(?i)(\b[A-Z0-9_]*(?:TOKEN|PASSWORD|SECRET|API[_-]?KEY|ACCESS[_-]?KEY)[A-Z0-9_]*\b\s*[=:]\s*)[^\s&]+",
        r"\1<redacted>",
        text,
    )
    text = re.sub(
        r"(?i)([?&](?:token|access_token|api[_-]?key|awsaccesskeyid|x-amz-(?:credential|signature)|x-goog-(?:credential|signature))=)[^&\s]+",
        r"\1<redacted>",
        text,
    )
    return text[-EXTENSION_VERIFICATION_FAILURE_TAIL_LIMIT:]

def extension_verification_throwaway_failure(
    proc: subprocess.CompletedProcess[str],
) -> dict[str, Any] | None:
    if proc.returncode == 0:
        return None
    for line in reversed(proc.stdout.splitlines()):
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict) or payload.get("status") != "failed":
            continue
        failure = payload.get("failure")
        if not isinstance(failure, dict) or set(failure) != {
            "kind",
            "stage",
            "cell_id",
            "command_label",
            "exit_code",
            "error_tail",
        }:
            continue
        stage = failure.get("stage")
        cell_id = failure.get("cell_id")
        command_label = failure.get("command_label")
        exit_code = failure.get("exit_code")
        error_tail = failure.get("error_tail")
        if (
            failure.get("kind") != "matrix_failure"
            or stage not in EXTENSION_VERIFICATION_FAILURE_STAGES
            or (stage == "matrix-cell" and not isinstance(cell_id, str))
            or (stage != "matrix-cell" and cell_id is not None)
            or not isinstance(command_label, str)
            or not command_label
            or not re.fullmatch(r"[A-Za-z0-9._:-]+", command_label)
            or not isinstance(exit_code, int)
            or isinstance(exit_code, bool)
            or not isinstance(error_tail, str)
        ):
            continue
        return {
            "kind": "matrix_failure",
            "stage": stage,
            "cell_id": cell_id,
            "command_label": command_label,
            "exit_code": exit_code,
            "error_tail": extension_verification_sanitize_failure_tail(error_tail),
        }
    combined = "\n".join(part for part in (proc.stdout, proc.stderr) if part)
    return {
        "kind": "unparseable_failure_output",
        "stage": None,
        "cell_id": None,
        "command_label": "verify-throwaway-installation",
        "exit_code": proc.returncode,
        "error_tail": extension_verification_sanitize_failure_tail(combined),
    }

def extension_verification_asset_inventory_summary(
    expectations: list[dict[str, Any]],
    asset_digests: list[dict[str, Any]],
    *,
    duplicate_paths: list[str] | None = None,
    relation_errors: list[str] | None = None,
) -> dict[str, Any]:
    duplicate_paths = sorted(set(duplicate_paths or []))
    relation_errors = sorted(set(relation_errors or []))
    expected_paths = [
        str(item.get("path") or "")
        for item in expectations
        if isinstance(item, dict)
    ]
    observed_paths = [
        str(item.get("path") or "")
        for item in asset_digests
        if isinstance(item, dict)
    ]
    duplicate_paths.extend(
        path
        for path in sorted(set(expected_paths))
        if expected_paths.count(path) != 1
    )
    duplicate_paths.extend(
        path
        for path in sorted(set(observed_paths))
        if observed_paths.count(path) != 1
    )
    duplicate_paths = sorted(set(duplicate_paths))
    expected_by_path = {
        str(item["path"]): item
        for item in expectations
        if isinstance(item, dict)
        and isinstance(item.get("path"), str)
        and expected_paths.count(str(item["path"])) == 1
    }
    observed_by_path = {
        str(item["path"]): item
        for item in asset_digests
        if isinstance(item, dict)
        and isinstance(item.get("path"), str)
        and observed_paths.count(str(item["path"])) == 1
    }
    missing_paths = sorted(set(expected_by_path) - set(observed_by_path))
    unexpected_paths = sorted(set(observed_by_path) - set(expected_by_path))
    mismatched_paths = sorted(
        path
        for path in set(expected_by_path) & set(observed_by_path)
        if expected_by_path[path].get("expected_sha256") is None
        or observed_by_path[path].get("sha256")
        != expected_by_path[path].get("expected_sha256")
        or observed_by_path[path].get("category")
        != expected_by_path[path].get("category")
        or observed_by_path[path].get("platform")
        != expected_by_path[path].get("platform")
    )
    categories: list[dict[str, Any]] = []
    for category in EXTENSION_VERIFICATION_ASSET_CATEGORIES:
        category_expected = [
            item
            for item in expectations
            if isinstance(item, dict) and item.get("category") == category
        ]
        category_observed = [
            item
            for item in asset_digests
            if isinstance(item, dict) and item.get("category") == category
        ]
        category_paths = {
            str(item.get("path") or "") for item in category_expected
        }
        matched_count = sum(
            1
            for path in category_paths
            if path in expected_by_path
            and path in observed_by_path
            and path not in mismatched_paths
        )
        expected_count = len(category_expected)
        observed_count = len(category_observed)
        categories.append({
            "id": category,
            "expected_count": expected_count,
            "observed_count": observed_count,
            "matched_count": matched_count,
            "complete": (
                expected_count > 0
                and observed_count == expected_count
                and matched_count == expected_count
                and not any(path in duplicate_paths for path in category_paths)
            ),
        })
    complete = (
        bool(expectations)
        and all(item["complete"] for item in categories)
        and not duplicate_paths
        and not missing_paths
        and not unexpected_paths
        and not mismatched_paths
        and not relation_errors
    )
    return {
        "expected_set_sha256": context_digest(expectations),
        "expected_count": len(expectations),
        "observed_count": len(asset_digests),
        "matched_count": sum(item["matched_count"] for item in categories),
        "categories": categories,
        "missing_paths": missing_paths,
        "duplicate_paths": duplicate_paths,
        "unexpected_paths": unexpected_paths,
        "mismatched_paths": mismatched_paths,
        "relation_errors": relation_errors,
        "complete": complete,
    }

def extension_verification_postcheck_failure(
    commands: Sequence[Mapping[str, Any]],
    asset_inventory: Mapping[str, Any],
    ownership: Mapping[str, Any],
    sidecars: Mapping[str, Any],
    capabilities: Sequence[Mapping[str, Any]],
) -> dict[str, Any] | None:
    for command in commands:
        exit_code = command.get("exit_code")
        command_id = command.get("id")
        if (
            isinstance(exit_code, int)
            and not isinstance(exit_code, bool)
            and exit_code != 0
            and isinstance(command_id, str)
            and re.fullmatch(r"[A-Za-z0-9._:-]+", command_id)
        ):
            return {
                "kind": "postcheck_failure",
                "stage": "pre-matrix",
                "cell_id": None,
                "command_label": command_id,
                "exit_code": exit_code,
                "error_tail": extension_verification_sanitize_failure_tail(
                    f"Standalone verification command {command_id} exited {exit_code}."
                ),
            }
    checks = (
        (
            asset_inventory.get("complete") is not True,
            "asset-inventory",
            "Installed managed asset inventory is incomplete.",
        ),
        (
            ownership.get("current_contract") is not True,
            "ownership-inventory",
            "Extension source ownership inventory is not current.",
        ),
        (
            bool(sidecars.get("paths")),
            "extension-sidecar-scan",
            "Extension source contains unresolved .new or .bak sidecars.",
        ),
        (
            any(
                not item.get("command_refs") or not item.get("asset_paths")
                for item in capabilities
            ),
            "capability-evidence",
            "Selected capability lacks command or installed asset evidence.",
        ),
    )
    for failed, command_label, message in checks:
        if failed:
            return {
                "kind": "postcheck_failure",
                "stage": "post-matrix",
                "cell_id": None,
                "command_label": command_label,
                "exit_code": 1,
                "error_tail": extension_verification_sanitize_failure_tail(message),
            }
    return None

def extension_verification_installed_asset_facts(
    source_checkout: Path,
    installed_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    expectations: list[dict[str, Any]] = []
    relation_errors: list[str] = []
    duplicate_paths: list[str] = []

    def add_expectation(
        category: str,
        installed_path: str,
        source_path: str,
        relation: str,
        *,
        platform: str | None = None,
    ) -> None:
        source = source_checkout / source_path
        expected_sha256 = (
            hashlib.sha256(source.read_bytes()).hexdigest()
            if source.is_file() and not source.is_symlink()
            else None
        )
        if expected_sha256 is None:
            relation_errors.append(f"{installed_path}:missing_canonical_source")
        expectations.append({
            "checkout_owner": EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
            "category": category,
            "platform": platform,
            "path": installed_path,
            "source_path": source_path,
            "expected_sha256": expected_sha256,
            "relation": relation,
        })

    add_expectation(
        "workflow",
        ".trellis/workflow.md",
        "trellis/workflows/guru-team/workflow.md",
        "canonical_workflow",
    )
    preset_sources = (
        "trellis/workflows/guru-team/config-template.yml",
        "trellis/workflows/guru-team/scripts/bash/execute-extension-verification.sh",
        "trellis/workflows/guru-team/scripts/bash/record-extension-verification.sh",
        "trellis/workflows/guru-team/scripts/bash/check-extension-verification.sh",
        "trellis/workflows/guru-team/scripts/bash/invoke-extension-verification.sh",
    )
    for source_path in preset_sources:
        installed_path = (
            ".trellis/guru-team/"
            + source_path.removeprefix("trellis/workflows/guru-team/")
        )
        add_expectation(
            "preset",
            installed_path,
            source_path,
            "managed_manifest",
        )
    manifest_path = installed_root / ".trellis/guru-team/extension.json"
    try:
        manifest = read_json(manifest_path)
    except WorkflowError:
        manifest = {}
        relation_errors.append(
            ".trellis/guru-team/extension.json:missing_or_invalid"
        )
    install = manifest.get("install") if isinstance(manifest.get("install"), dict) else {}
    managed_assets = (
        install.get("managed_assets")
        if isinstance(install.get("managed_assets"), list)
        else []
    )
    skill_packages = (
        manifest.get("skill_packages")
        if isinstance(manifest.get("skill_packages"), dict)
        else {}
    )
    manifest_files = (
        skill_packages.get("files")
        if isinstance(skill_packages.get("files"), list)
        else []
    )
    selected_platforms = (
        install.get("selected_platforms")
        if isinstance(install.get("selected_platforms"), list)
        else []
    )
    schema_prefix = ".trellis/guru-team/schemas/"
    for installed_path in sorted(
        path for path in managed_assets
        if isinstance(path, str) and path.startswith(schema_prefix)
    ):
        relative = installed_path.removeprefix(schema_prefix)
        add_expectation(
            "schema",
            installed_path,
            f"trellis/workflows/guru-team/schemas/{relative}",
            "managed_manifest",
        )
    package_source_root = (
        source_checkout
        / "trellis/skills/guru-team/packages/"
        "guru-verify-extension-installation"
    )
    package_sources = sorted(
        path
        for path in package_source_root.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    ) if package_source_root.is_dir() and not package_source_root.is_symlink() else []
    if not package_sources:
        relation_errors.append("skill:missing_canonical_set")
    canonical_destination = (
        ".trellis/guru-team/skills/packages/"
        "guru-verify-extension-installation"
    )
    for source in package_sources:
        package_relative = source.relative_to(package_source_root).as_posix()
        source_path = source.relative_to(source_checkout).as_posix()
        add_expectation(
            "skill",
            f"{canonical_destination}/{package_relative}",
            source_path,
            "skill_manifest",
        )
    platform_roots = {
        "shared": ".agents/skills/guru-verify-extension-installation/",
        "codex": ".codex/skills/guru-verify-extension-installation/",
        "claude": ".claude/skills/guru-verify-extension-installation/",
        "cursor": ".cursor/skills/guru-verify-extension-installation/",
    }
    source_prefix = (
        "trellis/skills/guru-team/packages/"
        "guru-verify-extension-installation/"
    )
    for item in manifest_files:
        if not isinstance(item, dict):
            continue
        installed_path = item.get("path")
        source_path = item.get("source")
        if not isinstance(installed_path, str) or not isinstance(source_path, str):
            continue
        if not source_path.startswith(source_prefix):
            continue
        for platform, prefix in platform_roots.items():
            if installed_path.startswith(prefix):
                add_expectation(
                    "platform",
                    installed_path,
                    source_path,
                    "platform_manifest",
                    platform=platform,
                )
                break
    for expectation in expectations:
        installed_path = str(expectation["path"])
        relation = expectation["relation"]
        expected_sha256 = expectation["expected_sha256"]
        if relation == "managed_manifest":
            occurrences = managed_assets.count(installed_path)
            if occurrences != 1:
                relation_errors.append(
                    f"{installed_path}:managed_manifest_count={occurrences}"
                )
                if occurrences > 1:
                    duplicate_paths.append(installed_path)
        elif relation in {"skill_manifest", "platform_manifest"}:
            records = [
                item
                for item in manifest_files
                if isinstance(item, dict) and item.get("path") == installed_path
            ]
            if len(records) != 1:
                relation_errors.append(
                    f"{installed_path}:skill_manifest_count={len(records)}"
                )
                if len(records) > 1:
                    duplicate_paths.append(installed_path)
            else:
                record = records[0]
                if (
                    record.get("source") != expectation["source_path"]
                    or record.get("sha256") != expected_sha256
                ):
                    relation_errors.append(
                        f"{installed_path}:manifest_relation_mismatch"
                    )
        platform = expectation.get("platform")
        if (
            platform in {"codex", "claude", "cursor"}
            and selected_platforms.count(platform) != 1
        ):
            relation_errors.append(
                f"{installed_path}:selected_platform_mismatch"
            )

    asset_digests: list[dict[str, Any]] = []
    for expectation in expectations:
        installed_path = str(expectation["path"])
        path = installed_root / installed_path
        if path.is_file() and not path.is_symlink():
            asset_digests.append({
                "checkout_owner": EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
                "category": expectation["category"],
                "platform": expectation["platform"],
                "path": installed_path,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    summary = extension_verification_asset_inventory_summary(
        expectations,
        asset_digests,
        duplicate_paths=duplicate_paths,
        relation_errors=relation_errors,
    )
    return expectations, asset_digests, summary

def extension_verification_capability_facts(
    selected_capabilities: list[str],
    status: str,
    commands: list[dict[str, Any]],
    asset_digests: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    available_commands = {
        str(item.get("id"))
        for item in commands
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    assets_by_category: dict[str, list[str]] = {
        category: sorted(
            str(item["path"])
            for item in asset_digests
            if isinstance(item, dict)
            and item.get("category") == category
            and isinstance(item.get("path"), str)
        )
        for category in EXTENSION_VERIFICATION_ASSET_CATEGORIES
    }
    capability_status = (
        status if status in {"passed", "failed", "blocked"} else "not_run"
    )
    return [
        {
            "id": capability,
            "status": capability_status,
            "command_refs": [
                command_id
                for command_id in (
                    EXTENSION_VERIFICATION_CAPABILITY_COMMAND_REFS[capability]
                )
                if command_id in available_commands
            ],
            "asset_paths": sorted({
                path
                for category in (
                    EXTENSION_VERIFICATION_CAPABILITY_ASSET_CATEGORIES[
                        capability
                    ]
                )
                for path in assets_by_category[category]
            }),
        }
        for capability in selected_capabilities
    ]

def extension_verification_package_root(root: Path) -> Path:
    invoked = os.environ.get("GURU_TEAM_INVOKED_PACKAGE_ROOT", "")
    candidates = [
        Path(invoked) if invoked else None,
        root
        / "trellis/skills/guru-team/packages/guru-verify-extension-installation",
        root
        / ".trellis/guru-team/skills/packages/guru-verify-extension-installation",
    ]
    for candidate in candidates:
        if (
            isinstance(candidate, Path)
            and candidate.is_dir()
            and not candidate.is_symlink()
            and candidate.name == EXTENSION_VERIFICATION_SKILL_ID
        ):
            return candidate
    raise WorkflowError(
        "The active extension verification package is unavailable.",
        exit_code=2,
    )

def extension_verification_json_input(
    root: Path,
    value: str | None,
    *,
    allow_stdin: bool = False,
) -> tuple[dict[str, Any], str]:
    raw = str(value or "").strip()
    if allow_stdin and raw == "-":
        try:
            payload = json.load(sys.stdin)
        except (OSError, json.JSONDecodeError) as exc:
            raise WorkflowError("Extension verification stdin JSON is invalid.", exit_code=2) from exc
        if not isinstance(payload, dict):
            raise WorkflowError("Extension verification stdin must be an object.", exit_code=2)
        return payload, "<stdin>"
    relative = skill_safe_relative(raw)
    if relative is None:
        raise WorkflowError(
            "Extension verification input must be a safe repo- or package-relative JSON path.",
            exit_code=2,
        )
    package = extension_verification_package_root(root)
    package_candidate = package / relative
    path = package_candidate if package_candidate.is_file() else root / relative
    boundary = package if path == package_candidate else root
    errors: list[str] = []
    if skill_lstat_path(
        boundary,
        path,
        "extension verification JSON input",
        errors,
        kind="file",
    ) is None:
        raise WorkflowError(
            "Extension verification input is missing or unsafe.",
            exit_code=2,
            payload={"errors": errors},
        )
    payload = skill_read_json(path, "extension verification JSON input", errors)
    if errors or not isinstance(payload, dict):
        raise WorkflowError(
            "Extension verification input is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return payload, repo_relative(root, path) if path.is_relative_to(root) else relative.as_posix()

def extension_verification_public_input(
    root: Path,
    value: str | None,
) -> dict[str, Any]:
    payload, _ = extension_verification_json_input(root, value)
    profile = payload.get("profile")
    schema_name = (
        "public-source-repository-verification-input.schema.json"
        if profile == "source_repository_verification"
        else ""
    )
    if not schema_name:
        raise WorkflowError(
            "retired_task_bearing_extension_verification: rebuild a current source_repository_verification standalone input; business task and Finalizer verification inputs are retired.",
            exit_code=2,
        )
    package = extension_verification_package_root(root)
    errors: list[str] = []
    schema = skill_read_schema(
        package / "schemas" / schema_name,
        "extension verification public input schema",
        errors,
    )
    if isinstance(schema, dict):
        errors.extend(
            skill_json_schema_validation_errors(
                payload,
                schema,
                "extension verification public input",
            )
        )
    if errors:
        raise WorkflowError(
            "Extension verification public input failed validation.",
            exit_code=2,
            payload={"errors": errors},
        )
    return payload

def extension_verification_source_preflight(
    root: Path,
    public_input: dict[str, Any],
) -> str:
    """Reject non-source or stale calls before clone, tempdir, or artifact writes."""
    required_assets = (
        root / "trellis/guru-team-extension.json",
        root / "trellis/index.json",
        root / "trellis/workflows/guru-team/workflow.md",
        root / "trellis/presets/guru-team/scripts/bash/apply.sh",
    )
    if any(not path.is_file() or path.is_symlink() for path in required_assets):
        raise WorkflowError(
            "source_repository_required: canonical Guru Team source assets are unavailable.",
            exit_code=2,
        )
    if public_input.get("repo_ref") != "castbox/guru-trellis":
        raise WorkflowError(
            "source_repository_mismatch: verifier accepts only castbox/guru-trellis.",
            exit_code=2,
        )
    origin = run(["git", "remote", "get-url", "origin"], cwd=root, check=False)
    if (
        origin.returncode != 0
        or parse_github_remote_repository_url(origin.stdout.strip())
        != "castbox/guru-trellis"
    ):
        raise WorkflowError(
            "source_origin_mismatch: origin must identify castbox/guru-trellis.",
            exit_code=2,
        )
    requested = str(public_input.get("ref") or "")
    resolved = run(
        ["git", "rev-parse", "--verify", f"{requested}^{{commit}}"],
        cwd=root,
        check=False,
    )
    head = current_head(root)
    resolved_commit = resolved.stdout.strip()
    if (
        resolved.returncode != 0
        or re.fullmatch(r"[0-9a-f]{40}", resolved_commit) is None
        or resolved_commit != head
    ):
        raise WorkflowError(
            "source_ref_head_mismatch: requested ref must resolve to current HEAD.",
            exit_code=2,
        )
    status = run(["git", "status", "--porcelain"], cwd=root, check=False)
    if status.returncode != 0 or status.stdout.strip():
        raise WorkflowError(
            "source_checkout_not_clean: commit source changes before standalone verification.",
            exit_code=2,
        )
    return resolved_commit

def extension_verification_remote_identity(
    root: Path,
    public_input: dict[str, Any],
) -> tuple[str, str, str, str | None, str | None]:
    if public_input["mode"] == "workflow":
        remote = str(publish_config(load_config(root)).get("remote") or "origin")
        branch = current_branch(root)
        ref = f"refs/heads/{branch}"
        branch_review_commit = str(public_input["branch_review_commit"])
        publication_head = str(public_input.get("publication_head") or branch_review_commit)
    else:
        remote = str(public_input["remote"])
        ref = str(public_input["ref"])
        branch_review_commit = None
        publication_head = None
    return str(public_input["repo_ref"]), remote, ref, branch_review_commit, publication_head

def extension_verification_workflow_source(repo_ref: str, ref: str) -> str:
    for prefix in ("refs/heads/", "refs/tags/"):
        if ref.startswith(prefix):
            return f"gh:{repo_ref}/trellis#{ref}"
    if re.fullmatch(r"[0-9a-f]{40}", ref) is not None:
        return f"gh:{repo_ref}/trellis#{ref}"
    raise WorkflowError(
        "Extension verification ref cannot select a workflow marketplace source.",
        exit_code=2,
    )

def extension_verification_canonical_github_locator(repo_ref: str) -> str:
    normalized = normalize_github_repository(repo_ref)
    if not normalized:
        raise WorkflowError(
            "Extension verification repository identity is invalid.",
            exit_code=2,
        )
    return f"https://github.com/{normalized}.git"

def extension_verification_validate_remote_locator(
    candidate: str,
    repo_ref: str,
) -> str:
    """Validate a local remote without retaining it as the clone locator."""
    normalized = normalize_github_repository(repo_ref)
    if (
        not normalized
        or parse_github_remote_repository_url(candidate) != normalized
        or extension_verification_sensitive_text(candidate)
    ):
        raise WorkflowError(
            "Extension verification remote locator is invalid or unsafe.",
            exit_code=2,
        )
    return extension_verification_canonical_github_locator(normalized)

def extension_verification_manifest_source(
    target_checkout: Path,
    public_input: dict[str, Any],
    *,
    task_bearing: bool,
) -> dict[str, Any]:
    manifest_path = target_checkout / GURU_TEAM_EXTENSION_MANIFEST
    manifest, error = read_optional_json(manifest_path)
    if manifest is None:
        if error != "missing":
            raise WorkflowError(
                "Installed extension manifest is malformed.",
                exit_code=2,
            )
        if task_bearing:
            raise WorkflowError(
                "Task-bearing extension verification requires an installed manifest.",
                exit_code=2,
            )
        repo_ref = normalize_github_repository(public_input.get("repo_ref"))
        return {
            "selection": "standalone_fallback",
            "manifest_provenance": "not_available",
            "repo": repo_ref,
            "locator": extension_verification_canonical_github_locator(repo_ref),
            "requested_ref": str(public_input.get("ref") or ""),
            "manifest_commit": None,
            "tree_state": "clean",
            "is_mutable_ref": str(public_input.get("ref") or "").startswith(
                "refs/heads/"
            ),
        }

    source = manifest.get("source")
    if not isinstance(source, dict):
        raise WorkflowError(
            "Installed extension manifest source provenance is malformed.",
            exit_code=2,
        )
    source_repo = source.get("repo")
    requested_ref = source.get("ref")
    manifest_commit = source.get("commit")
    tree_state = source.get("tree_state")
    is_mutable_ref = source.get("is_mutable_ref")
    normalized_repo = parse_github_remote_repository_url(source_repo)
    canonical_locator = (
        extension_verification_canonical_github_locator(normalized_repo)
        if normalized_repo
        else ""
    )
    if (
        not isinstance(source_repo, str)
        or extension_verification_sensitive_text(source_repo)
        or source_repo != canonical_locator
        or not isinstance(requested_ref, str)
        or not requested_ref.strip()
        or re.fullmatch(r"[0-9a-f]{40}", str(manifest_commit or "")) is None
        or tree_state not in {"clean", "dirty"}
        or not isinstance(is_mutable_ref, bool)
        or (
            re.fullmatch(r"[0-9a-f]{40}", requested_ref) is not None
            and is_mutable_ref is not False
        )
    ):
        raise WorkflowError(
            "Installed extension manifest source provenance is malformed or unsafe.",
            exit_code=2,
        )
    if task_bearing and tree_state != "clean":
        raise WorkflowError(
            "Task-bearing extension verification requires clean source provenance.",
            exit_code=2,
            payload={"reason_code": "extension_source_not_clean"},
        )
    return {
        "selection": "manifest",
        "manifest_provenance": "available",
        "repo": normalized_repo,
        "locator": canonical_locator,
        "requested_ref": requested_ref,
        "manifest_commit": manifest_commit,
        "tree_state": tree_state,
        "is_mutable_ref": is_mutable_ref,
    }

def extension_verification_standalone_source(
    target_checkout: Path,
    public_input: dict[str, Any],
) -> dict[str, Any]:
    manifest_path = target_checkout / GURU_TEAM_EXTENSION_MANIFEST
    _, error = read_optional_json(manifest_path)
    if error not in {None, "missing"}:
        raise WorkflowError(
            "Installed extension manifest is malformed.",
            exit_code=2,
        )
    repo_ref = normalize_github_repository(public_input.get("repo_ref"))
    requested_ref = str(public_input.get("ref") or "")
    return {
        "selection": "standalone_fallback",
        "manifest_provenance": "not_available" if error == "missing" else "available",
        "repo": repo_ref,
        "locator": extension_verification_canonical_github_locator(repo_ref),
        "requested_ref": requested_ref,
        "manifest_commit": None,
        "tree_state": "clean",
        "is_mutable_ref": requested_ref.startswith("refs/heads/"),
    }

def extension_verification_remote_ref_command(
    remote: str,
    ref: str,
) -> list[str]:
    return ["git", "ls-remote", remote, ref, f"{ref}^{{}}"]

def extension_verification_target_ref_process(
    root: Path,
    remote: str,
    ref: str,
    locator: str,
) -> tuple[list[str], subprocess.CompletedProcess[str]]:
    if re.fullmatch(r"[0-9a-f]{40}", ref) is None:
        command = extension_verification_remote_ref_command(remote, ref)
        return command, run(command, cwd=root, check=False)
    command = ["git", "fetch", "--depth=1", "origin", ref]
    with tempfile.TemporaryDirectory(prefix="guru-target-ref-") as tmp:
        target = Path(tmp) / "repo.git"
        init_proc = run(["git", "init", "--bare", "--quiet", str(target)], check=False)
        if init_proc.returncode != 0:
            return command, subprocess.CompletedProcess(command, init_proc.returncode, "", init_proc.stderr)
        remote_proc = run(
            ["git", "remote", "add", "origin", locator],
            cwd=target,
            check=False,
        )
        if remote_proc.returncode != 0:
            return command, subprocess.CompletedProcess(command, remote_proc.returncode, "", remote_proc.stderr)
        return command, run(command, cwd=target, check=False)

def extension_verification_source_ref_command(
    locator: str,
    requested_ref: str,
) -> list[str]:
    if requested_ref.startswith(("refs/heads/", "refs/tags/")):
        candidates = [requested_ref]
    else:
        candidates = [
            f"refs/heads/{requested_ref}",
            f"refs/tags/{requested_ref}",
        ]
    return [
        "git",
        "ls-remote",
        locator,
        *candidates,
        *(f"{candidate}^{{}}" for candidate in candidates),
    ]

def extension_verification_resolved_source_ref(
    remote_proc: subprocess.CompletedProcess[str],
    requested_ref: str,
) -> tuple[str | None, str | None, str | None]:
    if remote_proc.returncode != 0:
        return None, None, None
    if requested_ref.startswith(("refs/heads/", "refs/tags/")):
        candidates = [requested_ref]
    else:
        candidates = [
            f"refs/heads/{requested_ref}",
            f"refs/tags/{requested_ref}",
        ]
    rows: dict[str, str] = {}
    allowed = set(candidates) | {f"{candidate}^{{}}" for candidate in candidates}
    for line in remote_proc.stdout.splitlines():
        fields = line.split()
        if (
            len(fields) != 2
            or fields[1] not in allowed
            or fields[1] in rows
            or re.fullmatch(r"[0-9a-f]{40}", fields[0]) is None
        ):
            return None, None, None
        rows[fields[1]] = fields[0]
    resolved = [candidate for candidate in candidates if candidate in rows]
    if len(resolved) != 1:
        return None, None, None
    resolved_ref = resolved[0]
    direct_oid = rows[resolved_ref]
    return resolved_ref, direct_oid, rows.get(f"{resolved_ref}^{{}}", direct_oid)

def extension_verification_resolve_source_reference(
    locator: str,
    requested_ref: str,
    source_checkout: Path,
) -> dict[str, Any]:
    commands: list[dict[str, Any]] = []
    if re.fullmatch(r"[0-9a-f]{40}", requested_ref) is None:
        source_command = extension_verification_source_ref_command(
            locator,
            requested_ref,
        )
        source_proc = run(source_command, cwd=source_checkout.parent, check=False)
        commands.append(
            extension_verification_command_evidence(
                "resolve_extension_source_ref",
                EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
                source_command,
                source_proc,
            )
        )
        resolved_ref, direct_oid, commit = (
            extension_verification_resolved_source_ref(
                source_proc,
                requested_ref,
            )
        )
        return {
            "status": (
                "passed"
                if resolved_ref is not None
                and direct_oid is not None
                and commit is not None
                else "failed"
            ),
            "resolved_ref": resolved_ref,
            "direct_oid": direct_oid,
            "commit": commit,
            "checkout_prepared": False,
            "commands": commands,
        }

    init_command = ["git", "init", "--quiet", str(source_checkout)]
    init_proc = run(init_command, cwd=source_checkout.parent, check=False)
    commands.append(
        extension_verification_command_evidence(
            "clone_extension_source",
            EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
            init_command,
            init_proc,
            ["git", "init", "--quiet", "<temp-extension-source-checkout>"],
        )
    )
    configure_proc = subprocess.CompletedProcess(
        [],
        1,
        "",
        "source checkout init failed",
    )
    configure_command = ["git", "remote", "add", "origin", locator]
    if init_proc.returncode == 0:
        configure_proc = run(
            configure_command,
            cwd=source_checkout,
            check=False,
        )
    commands.append(
        extension_verification_command_evidence(
            "configure_extension_source_origin",
            EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
            configure_command,
            configure_proc,
        )
    )
    fetch_proc = subprocess.CompletedProcess([], 1, "", "source checkout init failed")
    fetch_command = ["git", "fetch", "--depth=1", "origin", requested_ref]
    if configure_proc.returncode == 0:
        fetch_proc = run(fetch_command, cwd=source_checkout, check=False)
    commands.append(
        extension_verification_command_evidence(
            "fetch_extension_source_commit",
            EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
            fetch_command,
            fetch_proc,
        )
    )
    resolve_proc = subprocess.CompletedProcess([], 1, "", "source commit fetch failed")
    resolve_command = ["git", "rev-parse", "--verify", "FETCH_HEAD^{commit}"]
    if fetch_proc.returncode == 0:
        resolve_proc = run(resolve_command, cwd=source_checkout, check=False)
    commands.append(
        extension_verification_command_evidence(
            "resolve_extension_source_ref",
            EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
            resolve_command,
            resolve_proc,
        )
    )
    commit = resolve_proc.stdout.strip() or None
    passed = (
        resolve_proc.returncode == 0
        and re.fullmatch(r"[0-9a-f]{40}", commit or "") is not None
        and commit == requested_ref
    )
    return {
        "status": "passed" if passed else "failed",
        "resolved_ref": requested_ref if passed else None,
        "direct_oid": commit if passed else None,
        "commit": commit if passed else None,
        "checkout_prepared": passed,
        "commands": commands,
    }

def extension_verification_resolved_remote_head(
    remote_proc: subprocess.CompletedProcess[str],
    ref: str,
) -> str | None:
    if remote_proc.returncode != 0:
        return None
    if re.fullmatch(r"[0-9a-f]{40}", ref) is not None:
        return ref
    direct_ref = ref
    peeled_ref = f"{ref}^{{}}"
    rows: dict[str, str] = {}
    for line in remote_proc.stdout.splitlines():
        fields = line.split()
        if (
            len(fields) != 2
            or fields[1] not in {direct_ref, peeled_ref}
            or fields[1] in rows
            or re.fullmatch(r"[0-9a-f]{40}", fields[0]) is None
        ):
            return None
        rows[fields[1]] = fields[0]
    direct_head = rows.get(direct_ref)
    if direct_head is None:
        return None
    return rows.get(peeled_ref, direct_head)

def extension_verification_ownership_facts(path: Path) -> dict[str, Any]:
    facts: dict[str, Any] = {
        "checkout_owner": EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
        "current_contract": False,
        "schema_version": None,
        "inventory_id": None,
        "guru_owned_rule_count": 0,
        "managed_claim_count": 0,
    }
    if not path.is_file() or path.is_symlink():
        return facts
    payload = read_json(path)
    rules = payload.get("guru_owned_rules")
    claims = payload.get("managed_path_claims")
    overlay_root = path.parent.parent / "overlays"
    overlay_paths = (
        sorted(
            item.relative_to(overlay_root).as_posix()
            for item in overlay_root.rglob("*")
            if item.is_file() or item.is_symlink()
        )
        if overlay_root.is_dir() and not overlay_root.is_symlink()
        else []
    )
    facts.update(
        {
            "schema_version": payload.get("schema_version"),
            "inventory_id": payload.get("inventory_id"),
            "guru_owned_rule_count": len(rules) if isinstance(rules, list) else 0,
            "managed_claim_count": len(claims) if isinstance(claims, list) else 0,
        }
    )
    facts["current_contract"] = (
        set(payload)
        == {
            "schema_version",
            "inventory_id",
            "target_trellis_cli",
            "overlay_root",
            "guru_owned_rules",
            "managed_path_claims",
        }
        and payload.get("schema_version") == "3.0"
        and payload.get("inventory_id") == "guru-team-upstream-ownership"
        and payload.get("target_trellis_cli") == "0.6.17"
        and payload.get("overlay_root") == "trellis/presets/guru-team/overlays"
        and isinstance(rules, list)
        and len(rules) == 11
        and all(isinstance(item, dict) for item in rules)
        and isinstance(claims, list)
        and len(claims) == 9
        and all(isinstance(item, dict) for item in claims)
        and overlay_paths
        == [
            ".claude/commands/guru/finish-work.md",
            ".codex/prompts/guru-finish-work.md",
            ".cursor/commands/guru-finish-work.md",
        ]
    )
    return facts

def extension_verification_execute_facts(
    root: Path,
    public_input: dict[str, Any],
    selected_capabilities: list[str],
    *,
    expected_branch_review_commit: str | None = None,
) -> dict[str, Any]:
    if (
        not selected_capabilities
        or len(selected_capabilities) != len(set(selected_capabilities))
        or any(item not in EXTENSION_VERIFICATION_CAPABILITIES for item in selected_capabilities)
    ):
        raise WorkflowError(
            "Extension verification capabilities must be a non-empty unique subset of the closed catalog.",
            exit_code=2,
        )
    repo_ref, remote, ref, branch_review_commit, publication_head = extension_verification_remote_identity(
        root,
        public_input,
    )
    required_commit = publication_head or expected_branch_review_commit or branch_review_commit
    commands: list[dict[str, Any]] = []
    remote_url_proc = run(["git", "remote", "get-url", remote], cwd=root, check=False)
    commands.append(
        extension_verification_command_evidence(
            "resolve_target_locator",
            EXTENSION_VERIFICATION_TARGET_CHECKOUT_OWNER,
            ["git", "remote", "get-url", remote],
            remote_url_proc,
        )
    )
    target_locator = ""
    if remote_url_proc.returncode == 0:
        try:
            target_locator = extension_verification_validate_remote_locator(
                remote_url_proc.stdout.strip(),
                repo_ref,
            )
        except WorkflowError:
            target_locator = ""
    target_command, target_proc = extension_verification_target_ref_process(
        root,
        remote,
        ref,
        target_locator,
    ) if target_locator else (
        extension_verification_remote_ref_command(remote, ref),
        subprocess.CompletedProcess([], 1, "", "target locator unavailable"),
    )
    commands.append(
        extension_verification_command_evidence(
            "resolve_target_ref",
            EXTENSION_VERIFICATION_TARGET_CHECKOUT_OWNER,
            target_command,
            target_proc,
        )
    )
    target_head = extension_verification_resolved_remote_head(target_proc, ref)
    status = "blocked"
    reviewed_content_sha256 = None
    remote_reviewed_content_sha256: str | None = None
    target_checkout_head: str | None = None
    target_content_matches = False
    extension_source: dict[str, Any] = {
        "selection": None,
        "manifest_provenance": None,
        "repo": None,
        "locator": None,
        "requested_ref": None,
        "resolved_ref": None,
        "direct_oid": None,
        "commit": None,
        "checkout_head": None,
        "tree_state": None,
        "is_mutable_ref": None,
        "ref_matches_commit": False,
        "checkout_head_matches": False,
    }
    ownership: dict[str, Any] = {
        "checkout_owner": EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
        "current_contract": False,
        "schema_version": None,
        "inventory_id": None,
        "guru_owned_rule_count": 0,
        "managed_claim_count": 0,
    }
    sidecars: dict[str, Any] = {
        "checkout_owner": EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
        "paths": [],
    }
    failure: dict[str, Any] | None = None
    if target_head is not None and target_locator:
        with temporary_directory("extension_verification") as tmp:
            temp_root = Path(tmp)
            target_checkout = temp_root / "target-checkout"
            source_checkout = temp_root / "extension-source-checkout"
            target_clone_command = [
                "git",
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                target_locator,
                str(target_checkout),
            ]
            target_clone_proc = run(target_clone_command, cwd=temp_root, check=False)
            commands.append(
                extension_verification_command_evidence(
                    "clone_target",
                    EXTENSION_VERIFICATION_TARGET_CHECKOUT_OWNER,
                    target_clone_command,
                    target_clone_proc,
                    [
                        "git",
                        "clone",
                        "--filter=blob:none",
                        "--no-checkout",
                        "<remote-url>",
                        "<temp-target-checkout>",
                    ],
                )
            )
            target_checkout_proc = subprocess.CompletedProcess([], 1, "", "clone failed")
            target_head_proc = subprocess.CompletedProcess(
                [],
                1,
                "",
                "checkout failed",
            )
            if target_clone_proc.returncode == 0:
                target_checkout_proc = run(
                    ["git", "checkout", "--detach", target_head],
                    cwd=target_checkout,
                    check=False,
                )
                commands.append(
                    extension_verification_command_evidence(
                        "checkout_target",
                        EXTENSION_VERIFICATION_TARGET_CHECKOUT_OWNER,
                        ["git", "checkout", "--detach", target_head],
                        target_checkout_proc,
                    )
                )
            if target_checkout_proc.returncode == 0:
                target_head_command = [
                    "git",
                    "rev-parse",
                    "--verify",
                    "HEAD^{commit}",
                ]
                target_head_proc = run(
                    target_head_command,
                    cwd=target_checkout,
                    check=False,
                )
                commands.append(
                    extension_verification_command_evidence(
                        "verify_target_checkout",
                        EXTENSION_VERIFICATION_TARGET_CHECKOUT_OWNER,
                        target_head_command,
                        target_head_proc,
                    )
                )
            target_checkout_head = target_head_proc.stdout.strip() or None
            target_checkout_matches = (
                target_head_proc.returncode == 0
                and re.fullmatch(r"[0-9a-f]{40}", target_checkout_head or "")
                is not None
                and target_checkout_head == target_head
                and (required_commit is None or required_commit == target_head)
            )
            if target_checkout_matches:
                try:
                    remote_reviewed_content_sha256 = reviewed_content_identity(
                        target_checkout,
                        target_head,
                        include_worktree=False,
                    )["sha256"]
                    target_content_matches = True
                except WorkflowError:
                    remote_reviewed_content_sha256 = None
            source_checkout_proc = subprocess.CompletedProcess([], 1, "", "source failed")
            source_head_proc = subprocess.CompletedProcess([], 1, "", "source failed")
            source_resolution: dict[str, Any] = {
                "status": "failed",
                "checkout_prepared": False,
            }
            source_checkout_prepared = False
            if target_checkout_matches and target_content_matches:
                selected_source = extension_verification_standalone_source(
                    target_checkout,
                    public_input,
                )
                source_resolution = extension_verification_resolve_source_reference(
                    selected_source["locator"],
                    selected_source["requested_ref"],
                    source_checkout,
                )
                commands.extend(source_resolution["commands"])
                resolved_ref = source_resolution["resolved_ref"]
                direct_oid = source_resolution["direct_oid"]
                source_commit = source_resolution["commit"]
                manifest_commit = selected_source["manifest_commit"]
                ref_matches_commit = (
                    source_commit is not None
                    and (manifest_commit is None or source_commit == manifest_commit)
                )
                extension_source = {
                    **selected_source,
                    "resolved_ref": resolved_ref,
                    "direct_oid": direct_oid,
                    "commit": source_commit,
                    "checkout_head": None,
                    "ref_matches_commit": ref_matches_commit,
                    "checkout_head_matches": False,
                }
                extension_source.pop("manifest_commit")
                source_checkout_prepared = (
                    ref_matches_commit
                    and source_resolution["checkout_prepared"] is True
                )
                if ref_matches_commit and not source_checkout_prepared:
                    source_clone_command = [
                        "git",
                        "clone",
                        "--filter=blob:none",
                        "--no-checkout",
                        extension_source["locator"],
                        str(source_checkout),
                    ]
                    source_clone_proc = run(
                        source_clone_command,
                        cwd=temp_root,
                        check=False,
                    )
                    commands.append(
                        extension_verification_command_evidence(
                            "clone_extension_source",
                            EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
                            source_clone_command,
                            source_clone_proc,
                            [
                                "git",
                                "clone",
                                "--filter=blob:none",
                                "--no-checkout",
                                extension_source["locator"],
                                "<temp-extension-source-checkout>",
                            ],
                        )
                    )
                    source_checkout_prepared = source_clone_proc.returncode == 0
                if source_checkout_prepared:
                    source_checkout_proc = run(
                        ["git", "checkout", "--detach", extension_source["commit"]],
                        cwd=source_checkout,
                        check=False,
                    )
                    commands.append(
                        extension_verification_command_evidence(
                            "checkout_extension_source",
                            EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
                            ["git", "checkout", "--detach", extension_source["commit"]],
                            source_checkout_proc,
                        )
                    )
                if source_checkout_proc.returncode == 0:
                    source_head_command = [
                        "git",
                        "rev-parse",
                        "--verify",
                        "HEAD^{commit}",
                    ]
                    source_head_proc = run(
                        source_head_command,
                        cwd=source_checkout,
                        check=False,
                    )
                    commands.append(
                        extension_verification_command_evidence(
                            "verify_extension_source_checkout",
                            EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
                            source_head_command,
                            source_head_proc,
                        )
                    )
                source_checkout_head = source_head_proc.stdout.strip() or None
                extension_source["checkout_head"] = source_checkout_head
                extension_source["checkout_head_matches"] = (
                    source_head_proc.returncode == 0
                    and source_checkout_head == extension_source["commit"]
                )
            throwaway_proc = subprocess.CompletedProcess([], 1, "", "source failed")
            throwaway = (
                source_checkout
                / "trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh"
            )
            install_work = temp_root / "install"
            installed_root = install_work / "project"
            if extension_source["checkout_head_matches"] and throwaway.is_file():
                throwaway_proc = run(
                    [str(throwaway), str(install_work)],
                    cwd=source_checkout,
                    check=False,
                    env={
                        "TRELLIS_WORKFLOW_SOURCE": (
                            extension_verification_workflow_source(
                                extension_source["repo"],
                                extension_source["resolved_ref"],
                            )
                        )
                    },
                )
                commands.append(
                    extension_verification_command_evidence(
                        "verify_throwaway_installation",
                        EXTENSION_VERIFICATION_SOURCE_CHECKOUT_OWNER,
                        [str(throwaway), str(install_work)],
                        throwaway_proc,
                        [
                            "<temp-source>/trellis/presets/guru-team/scripts/bash/"
                            "verify-throwaway-install.sh",
                            "<temp-install-work>",
                        ],
                    )
                )
                failure = extension_verification_throwaway_failure(throwaway_proc)
            asset_expectations: list[dict[str, Any]] = []
            installed_asset_digests: list[dict[str, Any]] = []
            asset_inventory = extension_verification_asset_inventory_summary(
                [],
                [],
            )
            if installed_root.is_dir() and not installed_root.is_symlink():
                (
                    asset_expectations,
                    installed_asset_digests,
                    asset_inventory,
                ) = extension_verification_installed_asset_facts(
                    source_checkout,
                    installed_root,
                )
            ownership_path = (
                source_checkout
                / "trellis/presets/guru-team/ownership/upstream-ownership.json"
            )
            ownership = extension_verification_ownership_facts(ownership_path)
            sidecars["paths"] = sorted(
                path.relative_to(source_checkout).as_posix()
                for path in source_checkout.rglob("*")
                if path.is_file()
                and (path.name.endswith(".new") or path.name.endswith(".bak"))
                and "fixtures" not in path.parts
            )
            status = (
                "passed"
                if target_clone_proc.returncode == 0
                and target_checkout_proc.returncode == 0
                and target_checkout_matches
                and target_content_matches
                and source_resolution["status"] == "passed"
                and extension_source["ref_matches_commit"]
                and source_checkout_prepared
                and source_checkout_proc.returncode == 0
                and extension_source["checkout_head_matches"]
                and throwaway_proc.returncode == 0
                and asset_inventory["complete"]
                and ownership["current_contract"] is True
                and not sidecars["paths"]
                else "failed"
            )
    else:
        asset_expectations = []
        installed_asset_digests = []
        asset_inventory = extension_verification_asset_inventory_summary([], [])
    capabilities = extension_verification_capability_facts(
        selected_capabilities,
        status,
        commands,
        installed_asset_digests,
    )
    if status == "passed" and any(
        not item["command_refs"] or not item["asset_paths"]
        for item in capabilities
    ):
        status = "failed"
        capabilities = extension_verification_capability_facts(
            selected_capabilities,
            status,
            commands,
            installed_asset_digests,
        )
    if status == "failed" and failure is None:
        failure = extension_verification_postcheck_failure(
            commands,
            asset_inventory,
            ownership,
            sidecars,
            capabilities,
        )
    return {
        "schema_version": EXTENSION_VERIFICATION_SCHEMA_VERSION,
        "target_repository": {
            "repo_ref": repo_ref,
            "remote": remote,
            "ref": ref,
            "branch_review_commit": branch_review_commit,
            "publication_head": target_head if public_input["mode"] == "workflow" else None,
            "resolved_head": target_head,
            "checkout_head": target_checkout_head,
            "reviewed_content_sha256": reviewed_content_sha256,
            "remote_reviewed_content_sha256": remote_reviewed_content_sha256,
            "content_identity_matches": target_content_matches,
        },
        "extension_source": extension_source,
        "status": status,
        "commands": commands,
        "failure": failure,
        "capabilities": capabilities,
        "asset_expectations": asset_expectations,
        "asset_digests": installed_asset_digests,
        "asset_inventory": asset_inventory,
        "ownership": ownership,
        "sidecars": sidecars,
    }

def extension_verification_schema(root: Path) -> dict[str, Any]:
    package = extension_verification_package_root(root)
    errors: list[str] = []
    schema = skill_read_schema(
        package / "schemas/marketplace-verification.schema.json",
        "extension verification private schema",
        errors,
    )
    if errors or not isinstance(schema, dict):
        raise WorkflowError(
            "Extension verification private schema is unavailable.",
            exit_code=2,
            payload={"errors": errors},
        )
    return schema

def extension_verification_recorder_input_schema(
    root: Path,
    schema_name: str,
    label: str,
) -> dict[str, Any]:
    if schema_name not in {
        "semantic-review-input-2.0.schema.json",
        "execution-facts.schema.json",
    }:
        raise WorkflowError(
            f"{label.capitalize()} schema is unavailable.",
            exit_code=2,
        )
    package = extension_verification_package_root(root)
    schema_path = package / "schemas" / schema_name
    errors: list[str] = []
    schema = skill_read_schema(schema_path, label, errors)
    private_schema = extension_verification_schema(root)
    reference_prefix = "marketplace-verification.schema.json#"
    resolved_references = 0

    def private_pointer(fragment: str) -> dict[str, Any] | None:
        if not fragment.startswith("/"):
            errors.append(f"{label} schema has an invalid private-schema $ref")
            return None
        target: Any = private_schema
        for encoded_part in fragment[1:].split("/"):
            part = encoded_part.replace("~1", "/").replace("~0", "~")
            if not isinstance(target, dict) or part not in target:
                errors.append(f"{label} schema has an unresolved private-schema $ref")
                return None
            target = target[part]
        if not isinstance(target, dict):
            errors.append(
                f"{label} schema private-schema $ref does not resolve to an object"
            )
            return None
        return target

    def project_references(node: Any) -> Any:
        nonlocal resolved_references
        if isinstance(node, list):
            return [project_references(item) for item in node]
        if not isinstance(node, dict):
            return copy.deepcopy(node)
        reference = node.get("$ref")
        if reference is None or (
            isinstance(reference, str)
            and not reference.startswith(reference_prefix)
        ):
            return {
                key: project_references(value)
                for key, value in node.items()
            }
        if not isinstance(reference, str):
            errors.append(f"{label} schema has a non-string $ref")
            return {}
        target = private_pointer(reference[len(reference_prefix):])
        if target is None:
            return {}
        resolved_references += 1
        resolved = project_references(target)
        siblings = {
            key: value
            for key, value in node.items()
            if key != "$ref"
        }
        if siblings:
            return {
                "allOf": [
                    resolved,
                    project_references(siblings),
                ]
            }
        return resolved

    if errors or not isinstance(schema, dict):
        raise WorkflowError(
            f"{label.capitalize()} schema is unavailable.",
            exit_code=2,
            payload={"errors": context_sort(errors)},
        )
    resolved = project_references(schema)
    if resolved_references == 0:
        errors.append(f"{label} schema does not reference its private contract")
    private_definitions = private_schema.get("$defs")
    if not isinstance(private_definitions, dict):
        errors.append("extension verification private schema has invalid $defs")
    else:
        existing_definitions = resolved.get("$defs")
        if existing_definitions is not None and not isinstance(
            existing_definitions,
            dict,
        ):
            errors.append(f"{label} schema has invalid $defs")
        elif isinstance(existing_definitions, dict) and (
            set(existing_definitions) & set(private_definitions)
        ):
            errors.append(f"{label} schema collides with private contract $defs")
        else:
            resolved["$defs"] = {
                **copy.deepcopy(existing_definitions or {}),
                **copy.deepcopy(private_definitions),
            }
    errors.extend(skill_json_schema_subset_errors(resolved, label))
    if errors:
        raise WorkflowError(
            f"{label.capitalize()} schema is invalid.",
            exit_code=2,
            payload={"errors": context_sort(errors)},
        )
    return resolved

def extension_verification_source_owner_state_path(
    root: Path,
    resolved_head: str,
) -> Path:
    if re.fullmatch(r"[0-9a-f]{40}", resolved_head) is None:
        raise WorkflowError(
            "Source verification owner state requires one resolved commit.",
            exit_code=2,
        )
    return (
        runtime_root(root, load_config(root))
        / "extension-verification-result"
        / f"source-{resolved_head[:24]}"
        / "owner-state.json"
    )

def cmd_execute_extension_verification(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    public_input = extension_verification_public_input(root, args.input)
    extension_verification_source_preflight(root, public_input)
    selected = list(args.capability or [])
    return extension_verification_execute_facts(root, public_input, selected)

def extension_verification_review_input(
    root: Path,
    value: str | None,
) -> dict[str, Any]:
    reviewed, _ = extension_verification_json_input(root, value)
    schema = extension_verification_recorder_input_schema(
        root,
        "semantic-review-input-2.0.schema.json",
        "extension verification semantic review input",
    )
    errors = skill_json_schema_validation_errors(
        reviewed,
        schema,
        "extension verification semantic review input",
    )
    if errors:
        raise WorkflowError(
            "Extension verification semantic review input failed schema validation.",
            exit_code=2,
            payload={"errors": context_sort(errors)},
        )
    return reviewed

def extension_verification_execution_input(
    root: Path,
    value: str | None,
) -> dict[str, Any]:
    execution, _ = extension_verification_json_input(root, value)
    schema = extension_verification_recorder_input_schema(
        root,
        "execution-facts.schema.json",
        "extension verification execution facts",
    )
    errors = skill_json_schema_validation_errors(
        execution,
        schema,
        "extension verification execution facts",
    )
    if errors:
        raise WorkflowError(
            "Extension verification execution facts failed schema validation.",
            exit_code=2,
            payload={"errors": context_sort(errors)},
        )
    return execution

def extension_verification_minimal_result(
    public_input: dict[str, Any],
    execution: dict[str, Any],
    reviewed: dict[str, Any],
) -> dict[str, Any]:
    target = execution.get("target_repository") if isinstance(execution.get("target_repository"), dict) else {}
    source = execution.get("extension_source") if isinstance(execution.get("extension_source"), dict) else {}
    profile = reviewed.get("verification_profile") if isinstance(reviewed.get("verification_profile"), dict) else {}
    semantic = reviewed.get("semantic_review") if isinstance(reviewed.get("semantic_review"), dict) else {}
    findings = semantic.get("findings") if isinstance(semantic.get("findings"), list) else []
    typed_exit = str(reviewed.get("typed_exit") or "")
    unverified_boundaries = {
        "verified": [],
        "blocked": ["verification-blocked"],
    }.get(typed_exit, ["verification-incomplete"])
    payload: dict[str, Any] = {
        "schema_version": EXTENSION_VERIFICATION_RESULT_SCHEMA_VERSION,
        "skill_id": EXTENSION_VERIFICATION_SKILL_ID,
        "mode": public_input["mode"],
        "profile": public_input["profile"],
        "immutable_identity": {
            "repo_ref": target.get("repo_ref"),
            "remote": target.get("remote"),
            "ref": target.get("ref"),
            "branch_review_commit": target.get("branch_review_commit"),
            "publication_head": target.get("publication_head") or target.get("resolved_head"),
            "extension_source_commit": source.get("commit"),
            "capability_profile": sorted(profile.get("selected_capabilities") or []),
        },
        "semantic_result": {
            "typed_exit": typed_exit,
            "conclusion": semantic.get("conclusion"),
            "finding_refs": sorted(
                str(item.get("finding_ref"))
                for item in findings
                if isinstance(item, dict) and item.get("status") == "open" and item.get("finding_ref")
            ),
            "blocker": (
                {"reason_code": reviewed.get("reason_code"), "remediation": reviewed.get("remediation")}
                if typed_exit == "blocked"
                else None
            ),
        },
        "unverified_boundaries": unverified_boundaries,
        "identity": {"verification_ref": "<pending>"},
    }
    digest = canonical_json_sha256(payload)
    payload["identity"]["verification_ref"] = f"extension-verification:{digest[:24]}"
    return payload

def extension_verification_minimal_errors(
    root: Path,
    payload: Any,
    public_input: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    schema_errors: list[str] = []
    schema = skill_read_schema(
        extension_verification_package_root(root) / "schemas/verification-result-5.0.schema.json",
        "extension verification minimal result",
        schema_errors,
    )
    if isinstance(schema, dict):
        schema_errors.extend(skill_json_schema_validation_errors(payload, schema, "extension verification minimal result"))
    errors.extend(schema_errors)
    if not isinstance(payload, dict):
        return errors or ["minimal verification result must be an object"]
    identity = payload.get("immutable_identity") if isinstance(payload.get("immutable_identity"), dict) else {}
    if public_input is not None:
        expected = {
            "repo_ref": public_input.get("repo_ref"),
            "remote": public_input.get("remote", "origin"),
            "ref": public_input.get("ref"),
            "branch_review_commit": public_input.get("branch_review_commit"),
            "publication_head": public_input.get("publication_head"),
        }
        for key, value in expected.items():
            if value is not None and identity.get(key) != value:
                errors.append(f"minimal verification {key} does not match public input")
    unsigned = copy.deepcopy(payload)
    current_ref = (unsigned.get("identity") or {}).get("verification_ref")
    unsigned["identity"] = {"verification_ref": "<pending>"}
    expected_ref = f"extension-verification:{canonical_json_sha256(unsigned)[:24]}"
    if current_ref != expected_ref:
        errors.append("minimal verification_ref does not match result identity")
    return errors

def cmd_record_extension_verification(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    public_input = extension_verification_public_input(root, args.input)
    resolved_head = extension_verification_source_preflight(root, public_input)
    execution = extension_verification_execution_input(root, args.execution_input)
    reviewed = extension_verification_review_input(root, args.review_input)
    identity = extension_verification_remote_identity(root, public_input)
    repo_ref, remote, ref, branch_review_commit, publication_head = identity
    execution_target = (
        execution.get("target_repository")
        if isinstance(execution.get("target_repository"), dict)
        else {}
    )
    if (
        execution_target.get("repo_ref") != repo_ref
        or execution_target.get("remote") != remote
        or execution_target.get("ref") != ref
        or execution_target.get("branch_review_commit") != branch_review_commit
        or execution_target.get("publication_head") != publication_head
    ):
        raise WorkflowError(
            "Extension verification execution facts do not match the public invocation.",
            exit_code=2,
        )
    semantic_errors = extension_verification_semantic_shape_errors(
        public_input,
        execution,
        reviewed,
    )
    if semantic_errors:
        raise WorkflowError(
            "Extension verification semantic result is internally inconsistent.",
            exit_code=2,
            payload={"errors": semantic_errors},
        )
    result = extension_verification_minimal_result(public_input, execution, reviewed)
    result["immutable_identity"]["repo_ref"] = public_input["repo_ref"]
    result["immutable_identity"]["remote"] = public_input["remote"]
    result["immutable_identity"]["ref"] = public_input["ref"]
    result["immutable_identity"]["branch_review_commit"] = None
    result["immutable_identity"]["publication_head"] = resolved_head
    result["identity"]["verification_ref"] = "<pending>"
    result["identity"]["verification_ref"] = (
        f"extension-verification:{canonical_json_sha256(result)[:24]}"
    )
    result_errors = extension_verification_minimal_errors(root, result, public_input)
    if result_errors:
        raise WorkflowError(
            "Extension verification recorder produced an invalid source result.",
            exit_code=2,
            payload={"errors": result_errors},
        )
    write_json(
        extension_verification_source_owner_state_path(root, resolved_head),
        result,
    )
    return result

def extension_verification_owner_input(
    root: Path,
    value: str | None,
) -> tuple[dict[str, Any], str]:
    return extension_verification_json_input(root, value, allow_stdin=True)

def check_extension_verification_result(
    root: Path,
    payload: dict[str, Any],
    locator: str,
    public_input: dict[str, Any] | None,
) -> dict[str, Any]:
    if payload.get("schema_version") == EXTENSION_VERIFICATION_RESULT_SCHEMA_VERSION:
        if public_input is None:
            raise WorkflowError(
                "Current source verification checking requires the exact public input.",
                exit_code=2,
            )
        errors = extension_verification_minimal_errors(root, payload, public_input)
        try:
            live_source_head = extension_verification_source_preflight(
                root, public_input
            )
            expected_owner_locator = repo_relative(
                root,
                extension_verification_source_owner_state_path(
                    root, live_source_head
                ),
            )
        except WorkflowError:
            errors.append("source repository verification identity is no longer current")
            expected_owner_locator = ""
        allowed_eval = (
            os.environ.get("GURU_TEAM_EVAL_STAGING") == "1"
            and locator.startswith(".trellis/.runtime/guru-team/evals/")
        )
        if locator not in {"<stdin>", expected_owner_locator} and not allowed_eval:
            errors.append(
                "source verification result must use stdin or its ignored source-session owner state"
            )
        identity = payload.get("immutable_identity") if isinstance(payload.get("immutable_identity"), dict) else {}
        if os.environ.get("GURU_TEAM_EVAL_STAGING") != "1":
            remote_proc = run(
                extension_verification_remote_ref_command(
                    str(identity.get("remote") or ""),
                    str(identity.get("ref") or ""),
                ),
                cwd=root,
                check=False,
            )
            if extension_verification_resolved_remote_head(remote_proc, str(identity.get("ref") or "")) != identity.get("publication_head"):
                errors.append("minimal verification immutable remote ref is stale")
        if errors:
            raise WorkflowError(
                "Extension verification minimal result failed objective checks.",
                exit_code=2,
                payload={"errors": errors},
            )
        semantic = payload["semantic_result"]
        return {
            "status": "ok",
            "typed_exit": semantic["typed_exit"],
            "mode": payload["mode"],
            "verification_ref": payload["identity"]["verification_ref"],
            "artifact_sha256": context_digest(payload),
        }
    raise WorkflowError(
        "Retired extension verification evidence is not accepted by the standalone source verifier.",
        exit_code=2,
    )

def cmd_check_extension_verification(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    payload, locator = extension_verification_owner_input(root, args.input)
    public_input = (
        extension_verification_public_input(root, args.public_input)
        if args.public_input
        else None
    )
    return check_extension_verification_result(
        root,
        payload,
        locator,
        public_input,
    )

def extension_verification_output_schema(
    root: Path,
    exit_id: str,
) -> dict[str, Any]:
    package = extension_verification_package_root(root)
    names = {
        "verified": "public-verified-output-4.0.schema.json",
        "blocked": "public-blocked-output-2.0.schema.json",
    }
    errors: list[str] = []
    schema = skill_read_schema(
        package / "schemas" / names[exit_id],
        "extension verification public output schema",
        errors,
    )
    if errors or not isinstance(schema, dict):
        raise WorkflowError(
            "Extension verification public output schema is unavailable.",
            exit_code=2,
            payload={"errors": errors},
        )
    return schema

def cmd_invoke_extension_verification(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    public_input = extension_verification_public_input(root, args.input)
    owner, locator = extension_verification_owner_input(root, args.owner_result)
    checked = check_extension_verification_result(
        root,
        owner,
        locator,
        public_input,
    )
    exit_id = str(checked["typed_exit"])
    if exit_id not in {"verified", "blocked"}:
        raise WorkflowError(
            "retired_task_bearing_extension_verification: current standalone verifier supports only verified or blocked.",
            exit_code=2,
        )
    minimal = owner.get("schema_version") == EXTENSION_VERIFICATION_RESULT_SCHEMA_VERSION
    semantic_result = owner.get("semantic_result") if minimal else None
    immutable_identity = owner.get("immutable_identity") if minimal else None
    payload: dict[str, Any] = {"exit_id": exit_id}
    if exit_id == "verified":
        payload.update(
            {
                "repo_ref": public_input["repo_ref"],
                "resolved_head": immutable_identity["publication_head"],
                "session_ref": owner["identity"]["verification_ref"],
            }
        )
    else:
        blocker = semantic_result["blocker"] if minimal else owner["blocker"]
        payload.update(
            {
                "reason_code": blocker["reason_code"],
                "remediation": blocker["remediation"],
            }
        )
    schema = extension_verification_output_schema(root, exit_id)
    errors = skill_json_schema_validation_errors(
        payload,
        schema,
        f"extension verification public output {exit_id}",
    )
    if errors:
        raise WorkflowError(
            "Extension verification public output failed validation.",
            exit_code=2,
            payload={"errors": errors},
        )
    resolved_head = extension_verification_source_preflight(root, public_input)
    owner_state_path = extension_verification_source_owner_state_path(
        root,
        resolved_head,
    )
    if owner_state_path.is_symlink():
        raise WorkflowError(
            "Extension verification source owner state is unsafe.",
            exit_code=2,
        )
    owner_state_path.unlink(missing_ok=True)
    return payload
