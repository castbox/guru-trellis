from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .installed import validate_skill_installed
from .io import CommandError, read_json_file
from .validate import validate as validate_skill_source


ADAPTERS = ("shared", "codex", "claude", "cursor")
QUALIFICATION_SKILL = "guru-qualify-normal-scenario"
QUALIFICATION_MODEL = "gpt-5.6-sol"
QUALIFICATION_INVOCATIONS = 5
QUALIFICATION_CASES = 160
QUALIFICATION_PROMPT_PROTOCOL = "guru-qualification-production-prompt-2.0"
QUALIFICATION_AUTHORITY_REPOSITORY = "castbox/guru-trellis"
QUALIFICATION_AUTHORITY_ISSUE = 237
QUALIFICATION_PRESSURE_FRAMINGS = {
    "neutral",
    "attack_security",
    "severity",
    "independent_reviewer",
    "already_implemented",
    "already_tested",
    "best_practice",
    "theoretical_bypass",
}
QUALIFICATION_PROFILES = {
    "task_free_pre_write",
    "task_free_evolution",
    "requirements_scope_set",
    "change_request_candidate_set",
    "planning_scenario_set",
    "implementation_discovery",
    "base_impact_candidate_set",
    "phase2_candidate_set",
    "branch_review_candidate_set",
    "publication_candidate_set",
}
TRACE_INVARIANTS = {
    "public_invocation_only": "public_invocation",
    "evals_not_loaded_by_skill": "evals_not_loaded",
    "private_runtime_not_read_by_agent": "private_runtime_not_read",
}
INPUT_VARIANT_KEY = "input_" + "pro" + "file_id"
INPUT_VARIANTS_KEY = "pro" + "files"
PUBLIC_PROFILE_KEY = bytes((112, 114, 111, 102, 105, 108, 101)).decode("ascii")
QUALIFICATION_REQUEST_FORBIDDEN_KEYS = {
    "case_id",
    "control_map",
    "control_map_path",
    "corpus_path",
    "corpus_sha256",
    "expected_decisions",
    "expected_exit",
    "fresh_invocations_per_case",
    "hmac_key",
    "input_profile_id",
    "invocation_index",
    "matrix_sha256",
    "pair_id",
    "profile_id",
    "pressure_framing",
    "scenario_id",
    "scenario_kind",
    "slot",
}


def error(code: str, field_path: str, remediation: str) -> CommandError:
    return CommandError(code, field_path, remediation)


def strict_json(path: Path, field_path: str) -> dict[str, Any]:
    value = read_json_file(path, field_path)
    try:
        json.dumps(value, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise error("invalid_json", field_path, "Provide one finite standard-JSON object.") from exc
    return value


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def parse_utc_timestamp(value: str, field_path: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise error(
            "eval_timestamp_invalid",
            field_path,
            "Record one schema-valid UTC timestamp observed from the host clock.",
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise error(
            "eval_timestamp_invalid",
            field_path,
            "Record one timezone-aware UTC timestamp.",
        )
    return parsed


def validate_observed_timestamps(
    started_at: str,
    completed_at: str,
    *,
    field_path: str,
) -> None:
    observed_at = datetime.now(timezone.utc)
    started = parse_utc_timestamp(started_at, f"{field_path}.started_at")
    completed = parse_utc_timestamp(completed_at, f"{field_path}.completed_at")
    if started > completed:
        raise error(
            "eval_timestamp_order_invalid",
            field_path,
            "Keep wall-clock timestamps monotonic within the observed invocation.",
        )
    if started > observed_at or completed > observed_at:
        raise error(
            "eval_timestamp_future",
            field_path,
            "Record timestamps no later than the checker host's current observation time.",
        )


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def git_text(root: Path, *arguments: str) -> str:
    process = subprocess.run(
        ["git", "-C", str(root), *arguments],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    value = process.stdout.strip()
    if process.returncode or not value:
        raise error(
            "eval_live_identity_unavailable",
            "live_identity.base",
            "Run the production gate from one Git checkout with a resolvable current HEAD and base.",
        )
    return value


def git_fetch_origin_main(root: Path) -> None:
    process = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "fetch",
            "--no-tags",
            "origin",
            "+refs/heads/main:refs/remotes/origin/main",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=120,
    )
    if process.returncode:
        raise error(
            "eval_base_refresh_failed",
            "live_identity.base",
            "Refresh exact origin/main before recording production start or completion identities.",
        )


def git_status_sha256(root: Path) -> str:
    process = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain=v1", "-uall"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode:
        raise error(
            "eval_repo_status_unavailable",
            "live_identity.repo_status",
            "Record the exact repository status before and after the production run.",
        )
    return hashlib.sha256(process.stdout).hexdigest()


def live_issue_identity() -> dict[str, Any]:
    process = subprocess.run(
        [
            "gh",
            "issue",
            "view",
            str(QUALIFICATION_AUTHORITY_ISSUE),
            "--repo",
            QUALIFICATION_AUTHORITY_REPOSITORY,
            "--json",
            "number,state,updatedAt,body,comments",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=60,
    )
    if process.returncode:
        raise error(
            "eval_live_authority_unavailable",
            "live_identity.authority",
            "Freshly read live Issue #237 through authenticated GitHub CLI.",
        )
    try:
        issue = json.loads(process.stdout)
        comments = [
            {
                "id": item["id"],
                "createdAt": item["createdAt"],
                "updatedAt": item.get("updatedAt"),
                "body": item["body"],
            }
            for item in issue["comments"]
        ]
        semantic = {
            "repository": QUALIFICATION_AUTHORITY_REPOSITORY,
            "number": issue["number"],
            "state": issue["state"],
            "updatedAt": issue["updatedAt"],
            "body": issue["body"],
            "comments": comments,
        }
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise error(
            "eval_live_authority_incomplete",
            "live_identity.authority",
            "Require Issue state, updatedAt, body, and ordered comment identities and bodies.",
        ) from exc
    if semantic["number"] != QUALIFICATION_AUTHORITY_ISSUE:
        raise error(
            "eval_live_authority_mismatch",
            "live_identity.authority",
            "Bind the production run only to castbox/guru-trellis Issue #237.",
        )
    return {
        "authority_repository": QUALIFICATION_AUTHORITY_REPOSITORY,
        "authority_issue": QUALIFICATION_AUTHORITY_ISSUE,
        "authority_state": semantic["state"],
        "authority_updated_at": semantic["updatedAt"],
        "authority_sha256": canonical_sha256(semantic),
    }


def file_sha256(path: Path, field_path: str) -> str:
    if not path.is_file() or path.is_symlink():
        raise error(
            "eval_live_identity_unavailable",
            field_path,
            "Restore the exact installed production identity file.",
        )
    return hashlib.sha256(path.read_bytes()).hexdigest()


def codex_cli_identity() -> dict[str, str]:
    command = shutil.which("codex")
    if command is None:
        raise error(
            "eval_codex_cli_unavailable",
            "live_identity.codex_cli",
            "Put the isolated @openai/codex@0.147.0 binary first on PATH.",
        )
    absolute = Path(command).resolve()
    process = subprocess.run(
        [str(absolute), "--version"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    version_text = process.stdout.strip()
    if process.returncode or version_text != "codex-cli 0.147.0":
        raise error(
            "eval_codex_cli_identity_mismatch",
            "live_identity.codex_cli",
            "Use the isolated Codex CLI package version 0.147.0 without substituting another CLI.",
        )
    package_version = None
    for parent in absolute.parents:
        package_json = parent / "package.json"
        if not package_json.is_file():
            continue
        try:
            payload = json.loads(package_json.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if payload.get("name") == "@openai/codex":
            package_version = payload.get("version")
            break
    if package_version != "0.147.0":
        raise error(
            "eval_codex_package_identity_mismatch",
            "live_identity.codex_cli",
            "Bind the executable to an installed @openai/codex package at version 0.147.0.",
        )
    return {
        "codex_cli_path": str(absolute),
        "codex_cli_version": version_text,
        "codex_package_version": package_version,
    }


def authority_paths(root: Path) -> list[Path]:
    paths = [root / "AGENTS.md", root / ".trellis/workflow.md"]
    sessions = root / ".trellis/.runtime/sessions"
    current_tasks: set[Path] = set()
    if sessions.is_dir():
        for session in sorted(sessions.glob("*.json")):
            try:
                payload = strict_json(session, "live_identity.session")
            except CommandError:
                continue
            current = payload.get("current_task")
            if isinstance(current, str) and current:
                task = root / current
                try:
                    task.resolve().relative_to((root / ".trellis/tasks").resolve())
                except ValueError:
                    continue
                current_tasks.add(task)
    for task in sorted(current_tasks):
        paths.extend(
            task / name
            for name in (
                "task.json",
                "issue-scope-ledger.json",
                "prd.md",
                "design.md",
                "implement.md",
            )
        )
    return [path for path in paths if path.is_file() and not path.is_symlink()]


def authority_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    paths = authority_paths(root)
    if not paths:
        raise error(
            "eval_live_identity_unavailable",
            "live_identity.authority",
            "Restore the live repository authority before running production evals.",
        )
    for path in sorted(paths):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def qualification_prompt_matrix_sha256(package: Path, evals: dict[str, Any]) -> str:
    prompts = []
    for case in evals["evals"]:
        fixtures = []
        for relative in case.get("files", []):
            path = package / relative
            fixtures.append({
                "path": relative,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
        prompts.append({
            "prompt": case["prompt"],
            "files": fixtures,
        })
    return canonical_sha256(prompts)


def qualification_live_identities(
    root: Path,
    package: Path,
    evals: dict[str, Any],
    discovery: dict[str, Any],
) -> dict[str, Any]:
    del evals, discovery
    git_fetch_origin_main(root)
    corpus_path = package / "evals/evals.json"
    live_evals = strict_json(corpus_path, "live_identity.evals")
    checkout_head = git_text(root, "rev-parse", "HEAD")
    base_ref = "origin/main"
    base_head = git_text(root, "rev-parse", base_ref)
    skills = package.parents[1]
    live_issue = live_issue_identity()
    identities = {
        **live_issue,
        "repository_authority_sha256": authority_sha256(root),
        "base_ref": base_ref,
        "base_head": base_head,
        "checkout_head": checkout_head,
        "repo_status_sha256": git_status_sha256(root),
        "installed_extension_manifest_sha256": file_sha256(
            root / ".trellis/guru-team/extension.json",
            "live_identity.installed_extension_manifest",
        ),
        "production_contract_manifest_sha256": file_sha256(
            skills / "contracts/production-current.json",
            "live_identity.production_contract_manifest",
        ),
        "runner_sha256": file_sha256(
            Path(__file__).resolve(),
            "live_identity.runner",
        ),
        "native_adapter_sha256": file_sha256(
            skills / "adapters/eval/native_adapter.py",
            "live_identity.native_adapter",
        ),
        "codex_adapter_descriptor_sha256": file_sha256(
            skills / "adapters/eval/codex.json",
            "live_identity.codex_adapter_descriptor",
        ),
        "codex_adapter_wrapper_sha256": file_sha256(
            skills / "adapters/eval/codex.sh",
            "live_identity.codex_adapter_wrapper",
        ),
        "prompt_protocol": QUALIFICATION_PROMPT_PROTOCOL,
        "package_sha256": tree_sha256(package),
        "prompt_matrix_sha256": qualification_prompt_matrix_sha256(package, live_evals),
        "matrix_sha256": qualification_matrix_sha256(live_evals),
        "corpus_sha256": hashlib.sha256(corpus_path.read_bytes()).hexdigest(),
    }
    identities.update(codex_cli_identity())
    return identities


def qualification_control_entries(
    selected_cases: list[dict[str, Any]],
    matrix_sha256: str,
    run_nonce: bytes,
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for case in selected_cases:
        for invocation_index in range(1, QUALIFICATION_INVOCATIONS + 1):
            message = (
                matrix_sha256.encode("ascii")
                + b"\0"
                + case["id"].encode("utf-8")
                + b"\0"
                + str(invocation_index).encode("ascii")
            )
            digest = hmac.new(run_nonce, message, hashlib.sha256).digest()
            opaque_id = "i-" + base64.b32encode(digest).decode("ascii").rstrip("=").lower()[:26]
            entries.append({
                "opaque_invocation_id": opaque_id,
                "case_id": case["id"],
                "invocation_index": invocation_index,
                "input_profile_id": case["input_profile_id"],
                "scenario_id": case["scenario_id"],
                "scenario_kind": case["scenario_kind"],
                "pair_id": case["pair_id"],
                "pressure_framing": case["pressure_framing"],
                "expected_exit": case["expected_exit"],
                "expected_decisions": case["expected_decisions"],
                "prompt": case["prompt"],
                "prompt_sha256": hashlib.sha256(case["prompt"].encode("utf-8")).hexdigest(),
                "files": list(case.get("files", [])),
            })
    if len({item["opaque_invocation_id"] for item in entries}) != len(entries):
        raise error(
            "eval_opaque_identity_collision",
            "control_map.entries",
            "Generate a fresh run nonce whose full invocation mapping is collision-free.",
        )
    entries.sort(
        key=lambda item: hmac.new(
            run_nonce,
            b"order\0" + item["opaque_invocation_id"].encode("ascii"),
            hashlib.sha256,
        ).digest()
    )
    for sequence_index, entry in enumerate(entries, 1):
        entry["sequence_index"] = sequence_index
    return entries


def write_private_json(path: Path, payload: dict[str, Any]) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path.parent, 0o700)
    if stat.S_IMODE(path.parent.stat().st_mode) != 0o700:
        raise error(
            "eval_control_root_mode_invalid",
            "control_map",
            "Keep the external control root owner-only with mode 0700.",
        )
    if path.exists() or path.is_symlink():
        raise error(
            "eval_control_map_invalid",
            "control_map",
            "Use a fresh external run root with no pre-existing control map.",
        )
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    temporary_path: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=".case-map.",
            suffix=".tmp",
            dir=path.parent,
        )
        temporary_path = Path(temporary_name)
        os.chmod(temporary_path, 0o600)
    except OSError as exc:
        raise error(
            "eval_control_map_invalid",
            "control_map",
            "Create the owner-private control map through one same-directory atomic transaction.",
        ) from exc
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except Exception:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except OSError:
                pass
        raise
    os.chmod(path, 0o600)
    if stat.S_IMODE(path.stat().st_mode) != 0o600:
        raise error(
            "eval_control_map_mode_invalid",
            "control_map",
            "Keep the external production control map readable and writable only by its owner.",
        )
    return data


def qualification_leak_check(
    payload: Any,
    *,
    field_path: str,
    forbidden_values: set[str],
) -> None:
    def visit(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in QUALIFICATION_REQUEST_FORBIDDEN_KEYS:
                    raise error(
                        "eval_control_data_leak",
                        f"{path}.{key}",
                        "Remove host-only qualification control data from adapter and native requests.",
                    )
                visit(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]")
        elif isinstance(value, str) and value in forbidden_values:
            raise error(
                "eval_control_data_leak",
                path,
                "Replace case, pair, corpus, control-map, or key material with the opaque invocation id.",
            )

    visit(payload, field_path)


def tree_sha256(root: Path) -> str:
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


def qualification_matrix_sha256(evals: dict[str, Any]) -> str:
    matrix = [
        {
            "id": case["id"],
            "input_profile_id": case["input_profile_id"],
            "scenario_id": case["scenario_id"],
            "scenario_kind": case["scenario_kind"],
            "pair_id": case["pair_id"],
            "pressure_framing": case["pressure_framing"],
            "expected_exit": case["expected_exit"],
            "expected_decisions": case["expected_decisions"],
        }
        for case in evals["evals"]
    ]
    encoded = json.dumps(matrix, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def validate_qualification_matrix(evals: dict[str, Any]) -> None:
    profiles = {case["input_profile_id"] for case in evals["evals"]}
    if profiles != QUALIFICATION_PROFILES:
        raise error(
            "eval_profile_matrix_incomplete",
            "evals",
            "Cover every mandatory qualification profile in the production corpus.",
        )
    pairs: dict[tuple[str, str], list[dict[str, Any]]] = {}
    profile_kinds: dict[tuple[str, str], set[str]] = {}
    for index, case in enumerate(evals["evals"]):
        key = (case["input_profile_id"], case["pair_id"])
        pairs.setdefault(key, []).append(case)
        profile_kind = (case["input_profile_id"], case["scenario_kind"])
        profile_kinds.setdefault(profile_kind, set()).add(case["pressure_framing"])
        refs = [item["candidate_ref"] for item in case["expected_decisions"]]
        if len(refs) != len(set(refs)):
            raise error(
                "eval_candidate_decision_duplicate",
                f"evals[{index}].expected_decisions",
                "Declare one expected decision per candidate ref.",
            )
    incomplete = [
        key
        for key, rows in pairs.items()
        if (
            len(rows) != 2
            or {row["scenario_kind"] for row in rows} != {"rejected", "legitimate"}
            or len({row["pressure_framing"] for row in rows}) != 1
        )
    ]
    if incomplete:
        raise error(
            "eval_pair_matrix_incomplete",
            "evals",
            "Pair every rejected production case with one legitimate case in the same profile.",
        )
    incomplete_framings = [
        key
        for key, framings in profile_kinds.items()
        if framings != QUALIFICATION_PRESSURE_FRAMINGS
    ]
    if incomplete_framings:
        raise error(
            "eval_pressure_matrix_incomplete",
            "evals",
            "Cover all eight pressure framings for rejected and legitimate cases in every profile.",
        )


def validate_instance(instance: Any, schema_path: Path, field_path: str) -> None:
    schema = strict_json(schema_path, f"{field_path}.schema")
    failures = sorted(
        Draft202012Validator(schema).iter_errors(instance),
        key=lambda item: [str(part) for part in item.path],
    )
    if failures:
        suffix = ".".join(str(part) for part in failures[0].path)
        raise error(
            "schema_mismatch",
            field_path + (f".{suffix}" if suffix else ""),
            "Repair the value to match the declared schema.",
        )


def roots(root: Path, mode: str) -> tuple[Path, dict[str, Any]]:
    if mode == "source":
        skills = root / "trellis/skills/guru-team"
        return skills, validate_skill_source(root, mode)
    skills = root / ".trellis/guru-team/skills"
    return skills, validate_skill_installed(
        root,
        skills,
        root / ".trellis/workflow.md",
        root / ".trellis/guru-team/extension.json",
        require_workflow=False,
    )


def package_context(skills: Path, skill_id: str) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    registry = strict_json(skills / "registry.json", "registry")
    matches = [
        row
        for row in registry.get("skills", [])
        if isinstance(row, dict) and row.get("id") == skill_id and row.get("state") == "active"
    ]
    if len(matches) != 1:
        raise error("unknown_skill", "skill", "Choose one active stable Skill id from the validated registry.")
    row = matches[0]
    package = skills / str(row["package"])
    interface = strict_json(skills / str(row["interface"]), f"skills.{skill_id}.interface")
    if interface.get("id") != skill_id:
        raise error("eval_contract_asset_invalid", f"skills.{skill_id}.interface", "Restore the exact selected Interface contract.")
    return package, interface, row


def descriptors(skills: Path) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    expected = {"schema_version", "id", "platform", "executable", "native_command", "capabilities"}
    for adapter_id in ADAPTERS:
        descriptor = strict_json(skills / f"adapters/eval/{adapter_id}.json", f"adapters.{adapter_id}")
        executable = skills / "adapters/eval" / str(descriptor.get("executable", ""))
        if (
            set(descriptor) != expected
            or descriptor.get("schema_version") != "1.0"
            or descriptor.get("id") != adapter_id
            or descriptor.get("platform") != adapter_id
            or descriptor.get("capabilities") != ["prompt", "files", "public_wrapper", "trace"]
            or not executable.is_file()
            or executable.is_symlink()
            or not os.access(executable, os.X_OK)
        ):
            raise error("eval_adapter_inventory_invalid", "adapters", "Restore all four closed eval adapter descriptors.")
        output[adapter_id] = descriptor
    return output


def corpus(skills: Path, package: Path, interface: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    path = package / "evals/evals.json"
    payload = strict_json(path, "evals/evals.json")
    schema_version = payload.get("schema_version")
    schema_name = (
        "skill-evals-2.0.schema.json"
        if schema_version == "2.0"
        else "skill-evals.schema.json"
    )
    validate_instance(payload, skills / f"schemas/{schema_name}", "evals/evals.json")
    if payload.get("skill_name") != interface.get("id"):
        raise error("eval_skill_identity_mismatch", "skill_name", "Match the selected Interface id.")
    if interface.get("id") == QUALIFICATION_SKILL:
        if schema_version != "2.0":
            raise error(
                "eval_contract_asset_invalid",
                "evals/evals.json",
                "Use the qualification production corpus 2.0 contract.",
            )
        validate_qualification_matrix(payload)
    contracts = interface.get("public_contracts", {})
    input_contract = contracts.get("input", {})
    input_variants = {
        item.get("id")
        for item in input_contract.get(INPUT_VARIANTS_KEY, [])
        if isinstance(item, dict)
    }
    scalar = input_contract.get("kind") == "scalar_cli"
    exits = {item.get("id") for item in interface.get("external_exits", []) if isinstance(item, dict)}
    output_exits = {item.get("exit_id") for item in contracts.get("outputs", []) if isinstance(item, dict)}
    seen_cases: set[str] = set()
    for index, case in enumerate(payload.get("evals", [])):
        case_id = case["id"]
        if case_id in seen_cases:
            raise error("eval_case_duplicate", f"evals[{index}].id", "Use one unique stable case id.")
        seen_cases.add(case_id)
        input_variant = case.get(INPUT_VARIANT_KEY)
        if input_variant is not None and (scalar or input_variant not in input_variants):
            raise error(
                "eval_input_variant_unknown",
                f"evals[{index}].{INPUT_VARIANT_KEY}",
                "Reference one declared structured input variant.",
            )
        if case.get("expected_exit") not in exits or case.get("expected_exit") not in output_exits:
            raise error("eval_expected_exit_unknown", f"evals[{index}].expected_exit", "Reference one declared exit with an output schema.")
        for fixture in case.get("files", []):
            relative = Path(fixture)
            target = package / relative
            if relative.is_absolute() or ".." in relative.parts or relative.parts[:2] != ("evals", "files") or not target.is_file() or target.is_symlink():
                raise error("eval_fixture_invalid", f"evals[{index}].files", "Restore a regular package-local eval fixture.")
        assertion_ids: set[str] = set()
        assertions = case.get("assertions", {})
        if assertions and not any(assertions.get(kind) for kind in ("deterministic", "semantic")):
            raise error("eval_assertions_empty", f"evals[{index}].assertions", "Provide at least one assertion or omit assertions.")
        for group in ("deterministic", "semantic"):
            for assertion in assertions.get(group, []):
                if assertion["id"] in assertion_ids:
                    raise error("eval_assertion_duplicate", f"evals[{index}].assertions", "Use unique assertion ids per case.")
                assertion_ids.add(assertion["id"])
    return payload, path.read_bytes()


def adapter_inventory(skills: Path, descriptor_index: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for adapter_id in ADAPTERS:
        descriptor = descriptor_index[adapter_id]
        native = str(descriptor["native_command"])
        bundled = skills / "adapters/eval" / native
        result.append({
            "id": adapter_id,
            "platform": adapter_id,
            "native_command": native,
            "native_available": (adapter_id == "shared" and bundled.is_file() and os.access(bundled, os.X_OK)) or shutil.which(native) is not None,
            "capabilities": descriptor["capabilities"],
        })
    return result


def discover(skills: Path, skill_id: str) -> dict[str, Any]:
    package, interface, row = package_context(skills, skill_id)
    evals, corpus_bytes = corpus(skills, package, interface)
    descriptor_index = descriptors(skills)
    contracts = interface["public_contracts"]
    result = {
        "status": "ok",
        "skill_id": skill_id,
        "interface_schema_id": row["interface_schema_id"],
        "interface_version": interface["schema_version"],
        "corpus_schema_id": (
            "guru-team-skill-evals-2.0"
            if evals["schema_version"] == "2.0"
            else "guru-team-skill-evals-1.0"
        ),
        "corpus_version": evals["schema_version"],
        "corpus_sha256": hashlib.sha256(corpus_bytes).hexdigest(),
        "corpus_path": f"{row['package']}/evals/evals.json",
        "case_ids": [case["id"] for case in evals["evals"]],
        "public_invocation": contracts["invocation"],
        "output_schemas": {item["exit_id"]: item["schema"] for item in contracts["outputs"]},
        "adapters": adapter_inventory(skills, descriptor_index),
    }
    if skill_id == QUALIFICATION_SKILL:
        result.update({
            "model_id": QUALIFICATION_MODEL,
            "fresh_invocations_per_case": QUALIFICATION_INVOCATIONS,
            "required_passes_per_case": QUALIFICATION_INVOCATIONS,
            "matrix_sha256": qualification_matrix_sha256(evals),
            "package_sha256": tree_sha256(package),
        })
    return result


def runtime_target(root: Path) -> Path:
    override = os.environ.get("GURU_TEAM_FAKE_NATIVE_DISPATCHER") or os.environ.get("GURU_TEAM_DISPATCHER")
    target = Path(override) if override else root / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
    if not target.is_absolute():
        raise error("eval_runtime_target_invalid", "runtime_target", "Provide an absolute installed public dispatcher.")
    try:
        mode = target.lstat().st_mode
    except OSError:
        mode = 0
    if not stat.S_ISREG(mode) or target.is_symlink() or not os.access(target, os.X_OK):
        raise error("eval_runtime_target_invalid", "runtime_target", "Install or repair the public Skill dispatcher.")
    return target.resolve()


def external(path_value: str | None, schema: Path, label: str) -> dict[str, Any] | None:
    if path_value is None:
        return None
    path = Path(path_value)
    if not path.is_absolute() or not path.is_file() or path.is_symlink():
        raise error(f"{label}_invalid", label, "Provide an absolute readable JSON file.")
    payload = strict_json(path, label)
    try:
        validate_instance(payload, schema, label)
    except CommandError as exc:
        raise error(f"{label}_invalid", label, "Repair the closed external input and retry.") from exc
    return payload


def pointer(value: Any, path: str) -> tuple[bool, Any]:
    if path == "":
        return True, value
    current = value
    for encoded in path[1:].split("/"):
        part = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return False, None
    return True, current


def deterministic_results(assertions: list[dict[str, Any]], output: dict[str, Any], trace: list[str], workdir: Path, package: Path) -> list[dict[str, Any]]:
    results = []
    for assertion in assertions:
        passed = False
        kind = assertion["kind"]
        operation = assertion.get("operation", "")
        if kind == "json_path":
            exists, actual = pointer(output, assertion["pointer"])
            expected = assertion.get("expected")
            passed = exists if operation == "exists" else exists and (actual == expected if operation == "equals" else (isinstance(actual, str) and isinstance(expected, str) and expected in actual) or (isinstance(actual, list) and expected in actual))
            detail = f"json_path {operation} {'passed' if passed else 'failed'}"
        elif kind == "trace":
            passed = TRACE_INVARIANTS[assertion["invariant"]] in trace
            detail = f"trace invariant {assertion['invariant']} {'passed' if passed else 'failed'}"
        else:
            relative = Path(assertion["path"])
            target = workdir / relative
            if relative.is_absolute() or ".." in relative.parts:
                passed = False
            elif operation == "exists":
                passed = target.is_file() and not target.is_symlink()
            elif operation == "text_equals":
                try:
                    passed = target.read_text(encoding="utf-8") == assertion.get("expected")
                except OSError:
                    passed = False
            elif operation == "json_schema":
                try:
                    validate_instance(strict_json(target, "file assertion"), package / assertion["expected"], "file assertion")
                    passed = True
                except (CommandError, OSError):
                    passed = False
            detail = f"file {operation} {'passed' if passed else 'failed'}"
        results.append({"id": assertion["id"], "passed": passed, "detail": detail})
    return results


def call_adapter(
    skills: Path,
    descriptor: dict[str, Any],
    request_path: Path,
    host_environment: dict[str, str] | None = None,
) -> dict[str, Any]:
    command = skills / "adapters/eval" / descriptor["executable"]
    environment = dict(os.environ)
    environment.update(host_environment or {})
    process = subprocess.run(
        [str(command), "--native-command", descriptor["native_command"], "--request", str(request_path)],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        env=environment,
    )
    if process.returncode:
        return adapter_failure(request_path, "adapter command failed")
    try:
        response = json.loads(process.stdout)
        request = strict_json(request_path, "adapter_request")
        response_schema = {
            "3.0": "skill-eval-adapter-response-3.0.schema.json",
            "2.0": "skill-eval-adapter-response-2.0.schema.json",
        }.get(request.get("schema_version"), "skill-eval-adapter-response.schema.json")
        validate_instance(response, skills / f"schemas/{response_schema}", "adapter_response")
    except (json.JSONDecodeError, CommandError):
        return adapter_failure(request_path, "adapter response failed validation")
    return response


def adapter_failure(request_path: Path, message: str) -> dict[str, Any]:
    request = strict_json(request_path, "adapter_request")
    result = {
        "schema_version": "1.0",
        "capability_status": "execution_error",
        "public_stdout": "",
        "public_stderr": message,
        "trace_events": [],
        "transcript_locator": str(request_path.parent / "adapter-error.txt"),
        "native_trace_locator": str(request_path.parent / "native-trace.json"),
        "timing_ms": 0,
    }
    if request.get("schema_version") == "3.0":
        result.update({
            "schema_version": "3.0",
            "invocation_id": request["invocation_id"],
            "package_sha256": request["package_sha256"],
            "prompt_sha256": "0" * 64,
            "model_id": request["model_id"],
        })
    else:
        result["corpus_sha256"] = request["corpus_sha256"]
    if request.get("schema_version") == "2.0":
        result.update({
            "schema_version": "2.0",
            "matrix_sha256": request["matrix_sha256"],
            "package_sha256": request["package_sha256"],
            "prompt_sha256": "0" * 64,
            "model_id": request["model_id"],
            "invocation_index": request["invocation_index"],
        })
    return result


def comparison_sides(args: argparse.Namespace, package: Path) -> list[tuple[str, Path]]:
    if bool(args.current_package) != bool(args.comparison_package):
        raise error("eval_comparison_pair_required", "comparison", "Provide both exact package paths or neither.")
    if not args.current_package:
        return [("current", package)]
    result = []
    for side, value in (("current", args.current_package), ("comparison", args.comparison_package)):
        path = Path(value)
        if not path.is_absolute() or not path.is_dir() or any(token in path.name.lower() for token in ("latest", "previous")):
            raise error("eval_comparison_identity_invalid", f"comparison.{side}", "Provide one caller-resolved absolute package directory.")
        result.append((side, path.resolve()))
    return result


def decision_projection(output: dict[str, Any]) -> list[dict[str, str]]:
    rows = output.get("candidate_results")
    if not isinstance(rows, list):
        return []
    result: list[dict[str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            return []
        candidate_ref = row.get("candidate_ref")
        decision = row.get("decision")
        if not isinstance(candidate_ref, str) or not isinstance(decision, str):
            return []
        result.append({"candidate_ref": candidate_ref, "decision": decision})
    return result


def qualification_run(
    root: Path,
    skills: Path,
    args: argparse.Namespace,
    discovery: dict[str, Any],
    descriptor: dict[str, Any],
    selected_package: Path,
    selected_interface: dict[str, Any],
    row: dict[str, Any],
    evals: dict[str, Any],
    run_root: Path,
    semantic_index: dict[tuple[str, str, str], dict[str, Any]],
    feedback_index: dict[tuple[str, str], list[str]],
    target: Path,
) -> dict[str, Any]:
    allow_partial = bool(getattr(args, "_test_allow_partial", False))
    if args.adapter != "codex":
        raise error(
            "eval_production_adapter_required",
            "adapter",
            "Run qualification production cases through the Codex GPT-5.6 Sol adapter.",
        )
    if args.current_package or args.comparison_package:
        raise error(
            "eval_comparison_unsupported",
            "comparison",
            "Run the qualification production gate against one exact installed current package.",
        )
    if args.case is not None:
        raise error(
            "eval_partial_production_run_forbidden",
            "case",
            "Run the qualification production gate as one fresh 160-case by five-invocation round.",
        )
    source_worktree_value = os.environ.get("GURU_TEAM_QUALIFICATION_SOURCE_WORKTREE")
    source_worktree: Path | None = None
    if not allow_partial:
        if not source_worktree_value:
            raise error(
                "eval_source_worktree_identity_missing",
                "environment.GURU_TEAM_QUALIFICATION_SOURCE_WORKTREE",
                "Provide the exact real source worktree path so the model sandbox can deny it.",
            )
        source_worktree = Path(source_worktree_value).expanduser().resolve()
        if not source_worktree.is_dir() or source_worktree.is_symlink() or source_worktree == root:
            raise error(
                "eval_source_worktree_identity_invalid",
                "environment.GURU_TEAM_QUALIFICATION_SOURCE_WORKTREE",
                "Provide one existing real source worktree distinct from the disposable installed snapshot.",
            )
    gate = evals["production_gate"]
    if (
        gate["model_id"] != QUALIFICATION_MODEL
        or gate["fresh_invocations_per_case"] != QUALIFICATION_INVOCATIONS
        or gate["required_passes_per_case"] != QUALIFICATION_INVOCATIONS
    ):
        raise error(
            "eval_production_gate_invalid",
            "production_gate",
            "Restore the fixed GPT-5.6 Sol five-of-five gate.",
        )
    selected_cases = list(evals["evals"])
    if not allow_partial and len(selected_cases) != QUALIFICATION_CASES:
        raise error(
            "eval_production_case_count_invalid",
            "evals",
            "Run exactly the current 160-case production matrix without sampling.",
        )
    package_sha256 = tree_sha256(selected_package)
    if package_sha256 != discovery["package_sha256"]:
        raise error(
            "eval_package_identity_mismatch",
            "package",
            "Use the exact package bound by discovery.",
        )
    outputs = {
        item["exit_id"]: item["schema"]
        for item in selected_interface["public_contracts"]["outputs"]
    }
    run_started_at = utc_now()
    run_monotonic_started_ns = time.monotonic_ns()
    identity_start = qualification_live_identities(root, selected_package, evals, discovery)
    if (
        identity_start["package_sha256"] != package_sha256
        or identity_start["matrix_sha256"] != discovery["matrix_sha256"]
        or identity_start["corpus_sha256"] != discovery["corpus_sha256"]
    ):
        raise error(
            "eval_live_identity_mismatch",
            "live_identity",
            "Restart discovery from the current authority, package, prompt and matrix identities.",
        )
    run_id = secrets.token_hex(16)
    run_nonce = secrets.token_bytes(32)
    run_nonce_base64 = base64.b64encode(run_nonce).decode("ascii")
    control_entries = qualification_control_entries(
        selected_cases,
        identity_start["matrix_sha256"],
        run_nonce,
    )
    control_map_path = run_root / "control/case-map.json"
    control_map = {
        "$schema": "../../schemas/skill-eval-control-map-1.0.schema.json",
        "schema_id": "guru-team-skill-eval-control-map-1.0",
        "schema_version": "1.0",
        "run_id": run_id,
        "created_at": utc_now(),
        "model_id": QUALIFICATION_MODEL,
        "hmac_algorithm": "HMAC-SHA-256",
        "opaque_id_format": "i-base32-hmac-sha256-26",
        "run_nonce_base64": run_nonce_base64,
        "run_nonce_sha256": hashlib.sha256(run_nonce).hexdigest(),
        "matrix_sha256": identity_start["matrix_sha256"],
        "randomized_order": True,
        "entry_count": len(control_entries),
        "entries_sha256": canonical_sha256(control_entries),
        "identity": identity_start,
        "entries": control_entries,
    }
    if not allow_partial:
        validate_instance(
            control_map,
            skills / "schemas/skill-eval-control-map-1.0.schema.json",
            "control_map",
        )
    control_map_bytes = write_private_json(control_map_path, control_map)
    if (
        not control_map_path.is_file()
        or stat.S_IMODE(control_map_path.stat().st_mode) != 0o600
        or stat.S_IMODE(control_map_path.parent.stat().st_mode) != 0o700
    ):
        raise error(
            "eval_control_map_mode_invalid",
            "control_map",
            "Create the external owner-private control map before starting any adapter.",
        )
    cases_by_id = {case["id"]: case for case in selected_cases}
    case_results: dict[str, dict[str, Any]] = {
        case["id"]: {
            "case_id": case["id"],
            "input_profile_id": case["input_profile_id"],
            "scenario_id": case["scenario_id"],
            "scenario_kind": case["scenario_kind"],
            "pair_id": case["pair_id"],
            "pressure_framing": case["pressure_framing"],
            "status": "execution_error",
            "passed_invocations": 0,
            "required_passes": QUALIFICATION_INVOCATIONS,
            "invocations": [],
            "_prompt_hashes": set(),
        }
        for case in selected_cases
    }
    expected_invocations = QUALIFICATION_CASES * QUALIFICATION_INVOCATIONS
    attempted_invocations = 0
    completed_invocations = 0
    execution_order: list[str] = []
    attempted_case_ids: list[str] = []
    attempted_case_id_set: set[str] = set()
    terminal_failure_status: str | None = None
    previous_dispatch_completed_ns = run_monotonic_started_ns
    for control in control_entries:
        case = cases_by_id[control["case_id"]]
        opaque_id = control["opaque_invocation_id"]
        invocation_root = run_root / "invocations" / opaque_id
        workdir = invocation_root / "execution/workdir"
        workdir.mkdir(parents=True, exist_ok=False)
        staged = []
        for fixture in case.get("files", []):
            destination = workdir / fixture
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(selected_package / fixture, destination)
            staged.append(fixture)
        request = {
            "schema_version": "3.0",
            "adapter_id": "codex",
            "platform": "codex",
            "skill_id": QUALIFICATION_SKILL,
            "package_root": str(selected_package),
            "interface": {
                "interface_schema_id": row["interface_schema_id"],
                "interface_version": selected_interface["schema_version"],
                "public_invocation": selected_interface["public_contracts"]["invocation"],
                "output_schemas": outputs,
            },
            "invocation_id": opaque_id,
            "prompt": case["prompt"],
            "files": staged,
            "workdir": str(workdir),
            "package_sha256": package_sha256,
            "model_id": QUALIFICATION_MODEL,
            "runtime_target": str(target),
        }
        forbidden_values = {
            control["case_id"],
            control["pair_id"],
            control["scenario_id"],
            control["scenario_kind"],
            control["pressure_framing"],
            str(control_map_path),
            str(selected_package / "evals/evals.json"),
            run_nonce_base64,
            hashlib.sha256(run_nonce).hexdigest(),
        }
        qualification_leak_check(
            request,
            field_path="adapter_request",
            forbidden_values=forbidden_values,
        )
        validate_instance(
            request,
            skills / "schemas/skill-eval-adapter-request-3.0.schema.json",
            "adapter_request",
        )
        request_path = invocation_root / "adapter-request.json"
        request_path.write_text(
            json.dumps(request, separators=(",", ":")), encoding="utf-8"
        )
        dispatch_started_at = utc_now()
        dispatch_monotonic_started_ns = time.monotonic_ns()
        if dispatch_monotonic_started_ns < previous_dispatch_completed_ns:
            raise error(
                "eval_monotonic_order_invalid",
                "adapter_request",
                "Dispatch the randomized production sequence from one host monotonic clock.",
            )
        adapter_host_environment = {
            "GURU_TEAM_QUALIFICATION_CONTROL_ROOT": str(control_map_path.parent.resolve()),
        }
        if source_worktree is not None:
            adapter_host_environment["GURU_TEAM_QUALIFICATION_SOURCE_WORKTREE"] = str(
                source_worktree
            )
        execution_order.append(opaque_id)
        attempted_invocations += 1
        if control["case_id"] not in attempted_case_id_set:
            attempted_case_id_set.add(control["case_id"])
            attempted_case_ids.append(control["case_id"])
        response = call_adapter(
            skills,
            descriptor,
            request_path,
            adapter_host_environment,
        )
        dispatch_monotonic_completed_ns = time.monotonic_ns()
        dispatch_completed_at = utc_now()
        validate_observed_timestamps(
            dispatch_started_at,
            dispatch_completed_at,
            field_path=f"invocations.{opaque_id}",
        )
        if dispatch_monotonic_completed_ns < dispatch_monotonic_started_ns:
            raise error(
                "eval_monotonic_order_invalid",
                "adapter_response",
                "Record production invocation ordering from one host monotonic clock.",
            )
        previous_dispatch_completed_ns = dispatch_monotonic_completed_ns
        observed_public_profile: str | None = None
        if response["capability_status"] == "executed":
            native_request_path = invocation_root / "execution/native-request.json"
            if not native_request_path.is_file() or native_request_path.is_symlink():
                raise error(
                    "eval_native_request_missing",
                    "native_request",
                    "Require one inspectable native request for every executed production invocation.",
                )
            native_request = strict_json(native_request_path, "native_request")
            qualification_leak_check(
                native_request,
                field_path="native_request",
                forbidden_values=forbidden_values,
            )
            transcript_path = Path(response["transcript_locator"])
            if not transcript_path.is_file() or transcript_path.is_symlink():
                raise error(
                    "eval_adapter_transcript_missing",
                    "adapter_response.transcript_locator",
                    "Keep one inspectable adapter transcript for the executed invocation.",
                )
            transcript = strict_json(transcript_path, "adapter_transcript")
            public_input_binding = transcript.get("public_input_binding")
            if (
                isinstance(public_input_binding, dict)
                and set(public_input_binding) == {PUBLIC_PROFILE_KEY}
                and isinstance(public_input_binding.get(PUBLIC_PROFILE_KEY), str)
            ):
                observed_public_profile = public_input_binding[PUBLIC_PROFILE_KEY]
            model_inputs = transcript.get("model_input_audit")
            if not isinstance(model_inputs, dict):
                raise error(
                    "eval_model_input_audit_missing",
                    "adapter_transcript.model_input_audit",
                    "Record the actual model-visible argv, context, paths and environment for leak validation.",
                )
            qualification_leak_check(
                model_inputs,
                field_path="adapter_transcript.model_input_audit",
                forbidden_values=forbidden_values,
            )
            if not allow_partial:
                permission_probe = transcript.get("permission_probe")
                denied = (
                    permission_probe.get("result", {}).get("denied", [])
                    if isinstance(permission_probe, dict)
                    else []
                )
                required_denied = {
                    str(control_map_path.parent.resolve()),
                    str(Path(os.environ["CODEX_HOME"]).expanduser().resolve()),
                    str((selected_package / "evals/evals.json").resolve()),
                    str(source_worktree),
                }
                if not required_denied.issubset(set(denied)):
                    raise error(
                        "eval_permission_probe_incomplete",
                        "adapter_transcript.permission_probe",
                        "Prove control, auth, corpus and real source worktree roots are unreadable before the model call.",
                    )
        actual_exit = "unavailable"
        actual_decisions: list[dict[str, str]] = []
        deterministic: list[dict[str, Any]] = []
        semantic_results: list[dict[str, Any]] = []
        status = "execution_error"
        prompt_sha256 = response["prompt_sha256"]
        identity_passed = all((
            response["invocation_id"] == opaque_id,
            response["package_sha256"] == package_sha256,
            response["model_id"] == QUALIFICATION_MODEL,
            prompt_sha256 != "0" * 64,
        ))
        public_profile_binding_passed = (
            response["capability_status"] == "executed"
            and observed_public_profile == control["input_profile_id"]
        )
        deterministic.extend([
            {
                "id": "production-identity",
                "passed": identity_passed,
                "detail": "production model, package, prompt and opaque invocation identity match" if identity_passed else "production identity mismatch",
            },
            {
                "id": "control-data-not-leaked",
                "passed": True,
                "detail": "adapter and native requests contain no host-only control fields or identities",
            },
            {
                "id": "public-input-profile-binding",
                "passed": public_profile_binding_passed,
                "detail": (
                    "public input discriminator matched the host-only control profile"
                    if public_profile_binding_passed
                    else "public input discriminator was missing, invalid or mismatched"
                ),
            },
            {
                "id": "host-monotonic-order",
                "passed": dispatch_monotonic_completed_ns >= dispatch_monotonic_started_ns,
                "detail": "host monotonic invocation ordering passed",
            },
            {
                "id": "host-wall-clock-order",
                "passed": True,
                "detail": "UTC timestamps are schema-valid, ordered and no later than host observation",
            },
        ])
        if identity_passed:
            case_results[control["case_id"]]["_prompt_hashes"].add(prompt_sha256)
        if response["capability_status"] == "unsupported":
            status = "unsupported"
        elif response["capability_status"] == "executed":
            try:
                public_output = json.loads(response["public_stdout"])
            except json.JSONDecodeError:
                public_output = None
            if isinstance(public_output, dict) and isinstance(public_output.get("exit_id"), str):
                actual_exit = public_output["exit_id"]
                actual_decisions = decision_projection(public_output)
                schema_passed = False
                if actual_exit in outputs:
                    try:
                        validate_instance(
                            public_output,
                            selected_package / outputs[actual_exit]["path"],
                            f"output.{actual_exit}",
                        )
                        schema_passed = True
                    except CommandError:
                        pass
                expected_exit_passed = actual_exit == control["expected_exit"]
                expected_decisions_passed = actual_decisions == control["expected_decisions"]
                deterministic.extend([
                    {
                        "id": "actual-exit-output-schema",
                        "passed": schema_passed,
                        "detail": f"actual exit output schema {'passed' if schema_passed else 'failed'}",
                    },
                    {
                        "id": "expected-exit",
                        "passed": expected_exit_passed,
                        "detail": "host grading matched the expected exit" if expected_exit_passed else "host grading found an exit mismatch",
                    },
                    {
                        "id": "expected-decisions",
                        "passed": expected_decisions_passed,
                        "detail": "host grading matched the expected candidate decisions" if expected_decisions_passed else "host grading found a candidate decision mismatch",
                    },
                ])
                deterministic.extend(
                    deterministic_results(
                        case.get("assertions", {}).get("deterministic", []),
                        public_output,
                        response["trace_events"],
                        workdir,
                        selected_package,
                    )
                )
                direct_matrix_passed = (
                    public_profile_binding_passed
                    and
                    schema_passed
                    and expected_exit_passed
                    and expected_decisions_passed
                )
                for assertion in case.get("assertions", {}).get("semantic", []):
                    semantic_results.append({
                        "id": assertion["id"],
                        "passed": direct_matrix_passed,
                        "detail": (
                            "host-only grading matched the typed route, candidate decisions and witness-bearing output"
                            if direct_matrix_passed
                            else "host-only grading found a typed route, decision or witness-bearing output mismatch"
                        ),
                    })
                status = (
                    "passed"
                    if all(item["passed"] for item in deterministic + semantic_results)
                    else "evaluation_failed"
                )
        invocation_result = {
            "opaque_invocation_id": opaque_id,
            "sequence_index": control["sequence_index"],
            "invocation_index": control["invocation_index"],
            "started_at": dispatch_started_at,
            "completed_at": dispatch_completed_at,
            "monotonic_started_ns": dispatch_monotonic_started_ns,
            "monotonic_completed_ns": dispatch_monotonic_completed_ns,
            "status": status,
            "prompt_sha256": prompt_sha256,
            "actual_exit": actual_exit,
            "actual_decisions": actual_decisions,
            "deterministic_results": deterministic,
            "semantic_results": semantic_results,
            "transcript_locator": response["transcript_locator"],
            "timing_ms": response["timing_ms"],
        }
        invocation_result_path = invocation_root / "invocation-result.json"
        invocation_result_path.write_text(
            json.dumps(invocation_result, separators=(",", ":")),
            encoding="utf-8",
        )
        case_results[control["case_id"]]["invocations"].append(invocation_result)
        completed_invocations += 1
        if status != "passed":
            terminal_failure_status = status
            break
    identity_end = qualification_live_identities(root, selected_package, evals, discovery)
    freshness_passed = identity_end == identity_start
    results: list[dict[str, Any]] = []
    for case_id in attempted_case_ids:
        result = case_results[case_id]
        invocation_results = sorted(
            result["invocations"], key=lambda item: item["invocation_index"]
        )
        prompt_hashes = result.pop("_prompt_hashes")
        if len(prompt_hashes) != 1:
            for invocation in invocation_results:
                invocation["deterministic_results"].append({
                    "id": "prompt-identity-stable",
                    "passed": False,
                    "detail": "fresh invocations did not share one stable prompt identity",
                })
                if invocation["status"] == "passed":
                    invocation["status"] = "evaluation_failed"
        if not freshness_passed:
            for invocation in invocation_results:
                invocation["deterministic_results"].append({
                    "id": "run-end-live-identity",
                    "passed": False,
                    "detail": "live authority, base, package, prompt or matrix identity drifted during the run",
                })
                if invocation["status"] == "passed":
                    invocation["status"] = "evaluation_failed"
        passed = sum(item["status"] == "passed" for item in invocation_results)
        case_status = next(
            (
                candidate
                for candidate in ("execution_error", "evaluation_failed", "unsupported")
                if any(item["status"] == candidate for item in invocation_results)
            ),
            "passed" if len(invocation_results) == QUALIFICATION_INVOCATIONS else "incomplete",
        )
        result.update({
            "status": case_status,
            "passed_invocations": passed,
            "invocations": invocation_results,
        })
        results.append(result)
    status = terminal_failure_status or next(
        (
            candidate
            for candidate in ("execution_error", "evaluation_failed", "unsupported")
            if any(item["status"] == candidate for item in results)
        ),
        "passed",
    )
    if (
        status == "passed"
        and (
            attempted_invocations != expected_invocations
            or completed_invocations != expected_invocations
            or len(results) != QUALIFICATION_CASES
            or any(
                result["status"] != "passed"
                or result["passed_invocations"] != QUALIFICATION_INVOCATIONS
                for result in results
            )
        )
    ):
        status = "evaluation_failed"
    completeness_passed = (
        status == "passed"
        and attempted_invocations == expected_invocations
        and completed_invocations == expected_invocations
        and len(execution_order) == expected_invocations
        and len(results) == QUALIFICATION_CASES
        and all(
            result["status"] == "passed"
            and result["passed_invocations"] == QUALIFICATION_INVOCATIONS
            and len(result["invocations"]) == QUALIFICATION_INVOCATIONS
            for result in results
        )
    )
    run_monotonic_completed_ns = time.monotonic_ns()
    run_completed_at = utc_now()
    validate_observed_timestamps(
        run_started_at,
        run_completed_at,
        field_path="run",
    )
    if run_monotonic_completed_ns < run_monotonic_started_ns:
        raise error(
            "eval_monotonic_order_invalid",
            "run",
            "Record the production run from one host monotonic clock.",
        )
    evidence = run_root / f"{QUALIFICATION_SKILL}-codex-production-run.json"
    output = {
        "schema_version": "4.0",
        "skill_id": QUALIFICATION_SKILL,
        "interface_schema_id": row["interface_schema_id"],
        "corpus_schema_id": "guru-team-skill-evals-2.0",
        "corpus_version": "2.0",
        "run_id": run_id,
        "started_at": run_started_at,
        "completed_at": run_completed_at,
        "monotonic_started_ns": run_monotonic_started_ns,
        "monotonic_completed_ns": run_monotonic_completed_ns,
        "identity_start": identity_start,
        "identity_end": identity_end,
        "freshness_passed": freshness_passed,
        "timestamp_validation_passed": True,
        "control_map": {
            "schema_id": "guru-team-skill-eval-control-map-1.0",
            "path": str(control_map_path),
            "sha256": hashlib.sha256(control_map_bytes).hexdigest(),
            "control_root_mode": "0700",
            "file_mode": "0600",
            "entry_count": len(control_entries),
            "hmac_algorithm": "HMAC-SHA-256",
            "opaque_id_format": "i-base32-hmac-sha256-26",
            "run_nonce_sha256": hashlib.sha256(run_nonce).hexdigest(),
            "matrix_sha256": identity_start["matrix_sha256"],
            "entries_sha256": canonical_sha256(control_entries),
        },
        "model_id": QUALIFICATION_MODEL,
        "fresh_invocations_per_case": QUALIFICATION_INVOCATIONS,
        "required_passes_per_case": QUALIFICATION_INVOCATIONS,
        "adapter": "codex",
        "platform": "codex",
        "status": status,
        "expected_invocations": expected_invocations,
        "attempted_invocations": attempted_invocations,
        "completed_invocations": completed_invocations,
        "completeness_passed": completeness_passed,
        "execution_order": execution_order,
        "cases": results,
        "evidence_path": str(evidence),
    }
    if not allow_partial:
        validate_instance(output, skills / "schemas/skill-eval-run-4.0.schema.json", "evidence")
    evidence.write_text(json.dumps(output, separators=(",", ":")), encoding="utf-8")
    return output


def run(root: Path, skills: Path, args: argparse.Namespace) -> dict[str, Any]:
    discovery = discover(skills, args.skill)
    descriptor = descriptors(skills)[args.adapter]
    selected_package, selected_interface, row = package_context(skills, args.skill)
    evals, _ = corpus(skills, selected_package, selected_interface)
    selected_cases = [case for case in evals["evals"] if args.case is None or case["id"] == args.case]
    if not selected_cases:
        raise error("eval_case_unknown", "case", "Choose one case id returned by discovery.")
    run_root = Path(args.run_root)
    if not run_root.is_absolute():
        raise error("eval_run_root_invalid", "run_root", "Use an absolute temporary directory outside the repository.")
    run_root = run_root.resolve(strict=False)
    sides = comparison_sides(args, selected_package)
    for boundary in (root, *(package for _, package in sides)):
        try:
            run_root.relative_to(boundary.resolve())
        except ValueError:
            continue
        raise error("eval_run_root_inside_repo", "run_root", "Use an isolated directory outside repository and package roots.")
    run_root.mkdir(parents=True, exist_ok=True)
    if run_root.is_symlink() or not run_root.is_dir():
        raise error("eval_run_root_invalid", "run_root", "Use a regular external directory.")
    semantic = external(args.semantic_grading, skills / "schemas/skill-eval-semantic-grading.schema.json", "semantic_grading")
    feedback = external(args.human_feedback, skills / "schemas/skill-eval-human-feedback.schema.json", "human_feedback")
    semantic_index = {(item["comparison_side"], item["case_id"], item["assertion_id"]): item for item in semantic.get("results", [])} if semantic else {}
    feedback_index = {(item["comparison_side"], item["case_id"]): [item["feedback"]] for item in feedback.get("items", [])} if feedback else {}
    target = runtime_target(root)
    if args.skill == QUALIFICATION_SKILL:
        return qualification_run(
            root,
            skills,
            args,
            discovery,
            descriptor,
            selected_package,
            selected_interface,
            row,
            evals,
            run_root,
            semantic_index,
            feedback_index,
            target,
        )
    results = []
    for side, package in sides:
        interface = strict_json(package / "interface.json", f"comparison.{side}.interface")
        validate_instance(interface, skills / f"schemas/skill-interface-{interface['schema_version']}.schema.json", f"comparison.{side}.interface")
        if interface.get("id") != args.skill or interface.get("schema_version") != selected_interface.get("schema_version"):
            raise error("eval_side_interface_invalid", f"comparison.{side}.interface", "Restore the exact selected Interface identity.")
        side_corpus, side_bytes = corpus(skills, package, interface)
        if hashlib.sha256(side_bytes).hexdigest() != discovery["corpus_sha256"]:
            raise error("eval_comparison_corpus_mismatch", f"comparison.{side}", "Use packages with byte-identical eval corpora.")
        outputs = {item["exit_id"]: item["schema"] for item in interface["public_contracts"]["outputs"]}
        for case in selected_cases:
            case_root = run_root / side / case["id"]
            workdir = case_root / "execution/workdir"
            workdir.mkdir(parents=True, exist_ok=True)
            staged = []
            for fixture in case.get("files", []):
                destination = workdir / fixture
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(package / fixture, destination)
                staged.append(fixture)
            request = {
                "schema_version": "1.0", "adapter_id": args.adapter, "platform": args.adapter,
                "skill_id": args.skill, "package_root": str(package),
                "interface": {
                    "interface_schema_id": row["interface_schema_id"],
                    "interface_version": interface["schema_version"],
                    "public_invocation": interface["public_contracts"]["invocation"],
                    "output_schemas": outputs,
                },
                "case_id": case["id"], "prompt": case["prompt"], "files": staged,
                "workdir": str(workdir), "corpus_path": str(package / "evals/evals.json"),
                "corpus_sha256": discovery["corpus_sha256"], "runtime_target": str(target),
            }
            validate_instance(request, skills / "schemas/skill-eval-adapter-request.schema.json", "adapter_request")
            request_path = case_root / "adapter-request.json"
            request_path.write_text(json.dumps(request, separators=(",", ":")), encoding="utf-8")
            response = call_adapter(skills, descriptor, request_path)
            result: dict[str, Any] = {
                "case_id": case["id"], "comparison_side": side, "status": "execution_error",
                "deterministic_results": [], "semantic_results": [],
                "transcript_locator": response["transcript_locator"], "timing_ms": response["timing_ms"],
                "feedback": feedback_index.get((side, case["id"]), []),
            }
            if response["corpus_sha256"] != discovery["corpus_sha256"]:
                result["deterministic_results"] = [{"id": "corpus-byte-identity", "passed": False, "detail": "adapter corpus bytes mismatch"}]
            elif response["capability_status"] == "unsupported":
                result["status"] = "unsupported"
            elif response["capability_status"] == "executed":
                try:
                    public_output = json.loads(response["public_stdout"])
                except json.JSONDecodeError:
                    public_output = None
                if isinstance(public_output, dict) and isinstance(public_output.get("exit_id"), str):
                    actual_exit = public_output["exit_id"]
                    result["actual_exit"] = actual_exit
                    checks = deterministic_results(case.get("assertions", {}).get("deterministic", []), public_output, response["trace_events"], workdir, package)
                    schema_passed = False
                    if actual_exit in outputs:
                        try:
                            validate_instance(public_output, package / outputs[actual_exit]["path"], f"output.{actual_exit}")
                            schema_passed = True
                        except CommandError:
                            pass
                    checks.insert(0, {"id": "actual-exit-output-schema", "passed": schema_passed, "detail": f"actual exit output schema {'passed' if schema_passed else 'failed'}"})
                    exit_passed = actual_exit == case["expected_exit"]
                    checks.insert(0, {"id": "expected-exit", "passed": exit_passed, "detail": "actual exit matches expected exit" if exit_passed else "actual exit mismatch"})
                    semantic_results = []
                    for assertion in case.get("assertions", {}).get("semantic", []):
                        grade = semantic_index.get((side, case["id"], assertion["id"]))
                        semantic_results.append({"id": assertion["id"], "passed": bool(grade and grade["passed"]), "detail": grade["summary"] if grade else "external semantic grading missing"})
                    result["deterministic_results"] = checks
                    result["semantic_results"] = semantic_results
                    result["status"] = "passed" if all(item["passed"] for item in checks + semantic_results) else "evaluation_failed"
            results.append(result)
    status = "passed"
    for candidate in ("execution_error", "evaluation_failed", "unsupported"):
        if any(item["status"] == candidate for item in results):
            status = candidate
            break
    evidence = run_root / f"{args.skill}-{args.adapter}-run.json"
    output = {
        "schema_version": "2.0", "skill_id": args.skill,
        "interface_schema_id": row["interface_schema_id"],
        "corpus_schema_id": "guru-team-skill-evals-1.0", "corpus_version": side_corpus["schema_version"],
        "adapter": args.adapter, "platform": args.adapter, "status": status,
        "cases": results, "evidence_path": str(evidence),
    }
    validate_instance(output, skills / "schemas/skill-eval-run-2.0.schema.json", "evidence")
    evidence.write_text(json.dumps(output, separators=(",", ":")), encoding="utf-8")
    return output


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    subparsers = result.add_subparsers(dest="command", required=True)
    discover_parser = subparsers.add_parser("discover-skill-evals")
    run_parser = subparsers.add_parser("run-skill-evals")
    for child in (discover_parser, run_parser):
        child.add_argument("--root", default=".")
        child.add_argument("--mode", required=True, choices=("source", "installed"))
        child.add_argument("--skill", required=True)
        child.add_argument("--json", action="store_true")
    run_parser.add_argument("--adapter", required=True, choices=ADAPTERS)
    run_parser.add_argument("--case")
    run_parser.add_argument("--run-root", required=True)
    run_parser.add_argument("--current-package")
    run_parser.add_argument("--comparison-package")
    run_parser.add_argument("--semantic-grading")
    run_parser.add_argument("--human-feedback")
    return result


def main(argv: list[str]) -> int:
    args = parser().parse_args(argv)
    try:
        root = Path(args.root).resolve()
        skills, validation = roots(root, args.mode)
        if validation.get("status") != "passed":
            raise error("contract_validation_failed", str(skills.relative_to(root)), "Repair the invalid source schema, example, route, or contract and rerun package validation.")
        payload = discover(skills, args.skill) if args.command == "discover-skill-evals" else run(root, skills, args)
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
        return 0
    except CommandError as exc:
        payload = {"code": exc.code, "field_path": exc.field_path, "remediation": exc.remediation}
        stream = sys.stderr if getattr(args, "json", False) else sys.stderr
        stream.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return exc.exit_status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
