"""Package-local deterministic runtime extracted from the frozen owner implementation."""

from __future__ import annotations

import argparse

import copy

import hashlib

import ipaddress

import json

import math

import os

import re

import shlex

import shutil

import stat

import subprocess

import sys

import tempfile

import unicodedata

from datetime import datetime, timezone

from pathlib import Path

from typing import Any

from urllib.parse import urlsplit

try:
    from runtime.reviewed_content import (
        PROVENANCE_TAIL_MANIFEST_PATH,
        ReviewedContentError,
        os_noise_path as ai_first_os_noise_path,
        reviewed_content_identity as canonical_reviewed_content_identity,
        reviewed_content_metadata_path,
    )
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from runtime.reviewed_content import (
        PROVENANCE_TAIL_MANIFEST_PATH,
        ReviewedContentError,
        os_noise_path as ai_first_os_noise_path,
        reviewed_content_identity as canonical_reviewed_content_identity,
        reviewed_content_metadata_path,
    )

DEFAULTS: dict[str, Any] = {
    "github_repo": "",
    "duplicate_search_required": True,
    "duplicate_candidate_limit": 5,
    "duplicate_high_similarity_action": "confirm",
    "branch_type_default": "chore",
    "base_branch": "",
    "base_branch_candidates": ["dev", "develop", "main", "master"],
    "workspace_mode": "worktree",
    "worktree_root": "",
    "runtime_root": ".trellis/.runtime/guru-team",
    "artifact_language": "zh-CN",
    "publish": {
        "remote": "origin",
    },
    "created_issue_labels": [],
    "closeout_markers": ["最终收口口径", "Final Closeout"],
}

PLANNING_APPROVAL_ARTIFACT = "planning-approval.json"

PHASE2_CHECK_ARTIFACT = "phase2-check.json"

CONTEXT_DISCOVERY_RECOVERY_ARTIFACT = "change-context-recovery.json"

AI_FIRST_OWNER_CHECKPOINT_DIR = "owner-checkpoints"

AI_FIRST_OWNER_ARTIFACTS = frozenset({
    CONTEXT_DISCOVERY_RECOVERY_ARTIFACT,
    PLANNING_APPROVAL_ARTIFACT,
    PHASE2_CHECK_ARTIFACT,
    "review-gate.json",
    "pr-readiness.json",
    "task-finalization-gate.json",
    "task-finalization-transition-gate.json",
    "finalization-transaction.json",
})

PROVENANCE_TAIL_ALLOWED_FIELDS = frozenset({
    "installed_at",
    "install.managed_asset_hashes",
    "install.managed_asset_hashes..trellis/spec/workflow/semantic-retrieval.md",
    "source.ref",
    "source.commit",
    "source.tree_state",
    "source.is_mutable_ref",
})

PROVENANCE_TAIL_FILE_ACTION_CONTAINERS = (
    "skill_packages.files",
    "overlays.files",
)

PROVENANCE_TAIL_OBJECT_PRESENCE = object()

AGENT_ASSIGNMENT_ARTIFACT = "agent-assignment.json"

REVIEW_REPORT_ARTIFACT = "review.md"

FINISH_SUMMARY_ARTIFACT = "finish-summary.json"

TASK_FINALIZATION_GATE_ARTIFACT = "task-finalization-gate.json"

TASK_FINALIZATION_TRANSITION_GATE_ARTIFACT = "task-finalization-transition-gate.json"

FINALIZATION_PLAN_SCHEMA_VERSION = "4.0"

CLOSEOUT_ARCHIVE_DURABLE_ARTIFACTS = {
    "task.json",
    "prd.md",
    "design.md",
    "implement.md",
    FINISH_SUMMARY_ARTIFACT,
}

CLOSEOUT_ARCHIVE_CORE_ARTIFACTS = {
    *CLOSEOUT_ARCHIVE_DURABLE_ARTIFACTS,
}

CLOSEOUT_ARCHIVE_MAX_ARTIFACTS = 5

CLOSEOUT_PR_PLACEHOLDER_NUMBER = 9223372036854775807

CLOSEOUT_SUMMARY_RUNTIME_FACT_FIELDS = [
    "github.pr_url",
    "index.search_terms.pr_refs",
]

CLOSEOUT_TRANSITIONS = [
    "prepared",
    "content_pushed",
    "draft_bound",
    "projection_validated",
    "archive_moved",
    "archive_pushed",
    "ready",
]

FINISH_SUMMARY_SCHEMA_VERSION = 2

FINISH_SUMMARY_GENERATOR = "guru-team.finalize-task"

HISTORICAL_FINISH_SUMMARY_SCHEMA_VERSION = 1

HISTORICAL_FINISH_SUMMARY_GENERATOR = "guru-team.finish-work"

FINISH_SUMMARY_SURFACE_KINDS = {
    "workflow", "script", "schema", "preset", "overlay", "skill", "prompt",
    "docs", "test", "config", "task-artifact", "github", "other",
}

CURRENT_FINISH_SUMMARY_ARTIFACT_FILES = {
    "prd": "prd.md",
    "design": "design.md",
    "implement": "implement.md",
}

HISTORICAL_FINISH_SUMMARY_ARTIFACT_FILES = {
    **CURRENT_FINISH_SUMMARY_ARTIFACT_FILES,
    "finish_summary_index": "finish-summary-" "index.json",
    "phase2_check": PHASE2_CHECK_ARTIFACT,
    "review": REVIEW_REPORT_ARTIFACT,
    "review_gate": "review-gate.json",
    "pr_body": "pr-" "body.md",
    "pr_readiness": "pr-readiness.json",
    "task_finalization_gate": TASK_FINALIZATION_GATE_ARTIFACT,
}

FINISH_SUMMARY_INDEX_KEYS = {
    "problem", "outcome", "changed_behavior", "affected_surfaces",
    "contract_changes", "search_terms",
}

FINISH_SUMMARY_AI_SEARCH_TERM_KEYS = {
    "commands", "config_keys", "schema_fields", "symbols", "phrases",
}

FINISH_SUMMARY_SEARCH_TERM_KEYS = {
    "issue_refs", "pr_refs", "branches", "paths",
    *FINISH_SUMMARY_AI_SEARCH_TERM_KEYS,
}

FINISH_SUMMARY_COMPLETION_MARKERS = (
    "完成", "改为", "不再", "新增", "移除", "修复", "支持", "写入", "更新", "归档", "回写", "保留",
)

FINISH_SUMMARY_FORBIDDEN_TEXT = (
    ".trellis/workspace/", ".trellis/.runtime/", "/Users/", "/tmp/",
)

FINISH_SUMMARY_PROTECTED_PATH_PREFIXES = (
    ".trellis/workspace/", ".trellis/.runtime/",
)

FINISH_SUMMARY_PROTECTED_PATH_FILTER_CONTRACT = {
    "contract": "finish-summary protected path filtering",
    "before": "原始 Git 变更集合包含受保护运行态路径。",
    "after": "完成摘要已过滤受保护运行态路径，过滤项未写入 path 字段。",
    "source_artifact": "",
}

FINISH_SUMMARY_PATH_SNAPSHOT_UNAVAILABLE_CONTRACT = {
    "contract": "finish-summary git path snapshot unavailable",
    "before": "Git 变更路径快照未成功完成。",
    "after": "完成摘要已使用空路径集合，未写入未验证路径。",
    "source_artifact": "",
}

PR_READINESS_ARTIFACT = "pr-readiness.json"

REVIEW_ROUND_REPORT_DIR = "reviews"

WORKSPACE_BOUNDARY_SUSPICIOUS_TASK_ARTIFACTS = [
    "task.json",
    "prd.md",
    "design.md",
    "implement.md",
    "implement.jsonl",
    "check.jsonl",
    PLANNING_APPROVAL_ARTIFACT,
    PHASE2_CHECK_ARTIFACT,
    AGENT_ASSIGNMENT_ARTIFACT,
    REVIEW_REPORT_ARTIFACT,
    "review-gate.json",
    "pr-readiness.json",
]

WORKSPACE_BOUNDARY_REVIEW_METADATA = {
    PLANNING_APPROVAL_ARTIFACT,
    PHASE2_CHECK_ARTIFACT,
    AGENT_ASSIGNMENT_ARTIFACT,
    REVIEW_REPORT_ARTIFACT,
    "review-gate.json",
    "pr-readiness.json",
}

BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX = (
    "Branch Review content changed after branch_review_commit: "
)

def finish_summary_normalized_text(value: str) -> str:
    folded = value.strip().casefold()
    folded = re.sub(r"\s+", "", folded)
    return "".join(char for char in folded if char.isalnum())

def finish_summary_duplicate_errors(values: Any, label: str) -> list[str]:
    if not isinstance(values, list):
        return [f"{label} must be an array."]
    errors: list[str] = []
    seen: dict[str, int] = {}
    for index, value in enumerate(values):
        if not isinstance(value, str):
            continue
        normalized = finish_summary_normalized_text(value)
        if normalized in seen:
            errors.append(f"{label}[{index}] duplicates {label}[{seen[normalized]}] after normalization.")
        else:
            seen[normalized] = index
    return errors

def finish_summary_exact_duplicate_errors(values: Any, label: str) -> list[str]:
    if not isinstance(values, list):
        return [f"{label} must be an array."]
    errors: list[str] = []
    seen: dict[str, int] = {}
    for index, value in enumerate(values):
        if not isinstance(value, str):
            continue
        if value in seen:
            errors.append(f"{label}[{index}] duplicates {label}[{seen[value]}].")
        else:
            seen[value] = index
    return errors

def finish_summary_object_fingerprint(value: dict[str, Any], *, exact_fields: set[str]) -> str:
    normalized = {
        key: item
        if key in exact_fields or not isinstance(item, str)
        else finish_summary_normalized_text(item)
        for key, item in value.items()
    }
    return json.dumps(normalized, ensure_ascii=False, sort_keys=True)

def finish_summary_text_errors(value: Any, label: str, minimum: int, maximum: int) -> list[str]:
    if not isinstance(value, str):
        return [f"{label} must be a string."]
    errors: list[str] = []
    if value != value.strip():
        errors.append(f"{label} must not contain leading or trailing whitespace.")
    if not (minimum <= len(value) <= maximum):
        errors.append(f"{label} length must be between {minimum} and {maximum} characters.")
    if any(marker in value for marker in FINISH_SUMMARY_FORBIDDEN_TEXT):
        errors.append(f"{label} contains a forbidden workspace/runtime/absolute path marker.")
    clauses = [part for part in re.split(r"[。！？!?；;，,\n]+", value) if part.strip()]
    for previous, current in zip(clauses, clauses[1:]):
        if finish_summary_normalized_text(previous) == finish_summary_normalized_text(current):
            errors.append(f"{label} contains adjacent duplicate clauses.")
            break
    return errors

def finish_summary_path_errors(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, str):
        return [f"{label} must be a string path."]
    if not value:
        return [] if allow_empty else [f"{label} must not be empty."]
    parts = value.split("/")
    errors: list[str] = []
    if "\\" in value:
        errors.append(f"{label} must not contain backslashes.")
    if "\r" in value or "\n" in value:
        errors.append(f"{label} must not contain carriage returns or line feeds.")
    if value != value.strip() or value.startswith("/") or re.match(r"^[A-Za-z]:/", value):
        errors.append(f"{label} must be a clean relative path.")
    if any(part in {"", ".", ".."} for part in parts):
        errors.append(f"{label} must not contain empty, dot, or parent segments.")
    if finish_summary_path_is_protected(value):
        errors.append(f"{label} must not point to workspace or runtime state.")
    if len(value) > 500:
        errors.append(f"{label} exceeds 500 characters.")
    return errors

def finish_summary_path_is_protected(value: str) -> bool:
    return any(
        value == prefix.removesuffix("/") or value.startswith(prefix)
        for prefix in FINISH_SUMMARY_PROTECTED_PATH_PREFIXES
    )

def sanitize_finish_summary_git_paths(paths: Any) -> tuple[list[str], bool]:
    if not isinstance(paths, (list, tuple, set)) or any(
        not isinstance(path, str) or not path.strip()
        for path in paths
    ):
        raise WorkflowError("finish-summary changed paths must be non-empty strings.", exit_code=2)
    raw_paths = sorted(set(paths))
    protected_paths_filtered = any(finish_summary_path_is_protected(path) for path in raw_paths)
    safe_paths = [path for path in raw_paths if not finish_summary_path_is_protected(path)]
    path_errors = [
        error
        for path in safe_paths
        for error in finish_summary_path_errors(path, "git.changed_paths[]")
    ]
    if path_errors:
        raise WorkflowError(
            "finish-summary changed paths are invalid.",
            exit_code=2,
            payload={"errors": path_errors},
        )
    return safe_paths, protected_paths_filtered

def apply_finish_summary_path_filter_contract(index: dict[str, Any], protected_paths_filtered: bool) -> None:
    contracts = index.get("contract_changes")
    existing = contracts if isinstance(contracts, list) else []
    filtered_contracts = [
        item
        for item in existing
        if not (
            isinstance(item, dict)
            and item.get("contract") == FINISH_SUMMARY_PROTECTED_PATH_FILTER_CONTRACT["contract"]
        )
    ]
    if protected_paths_filtered:
        filtered_contracts.append(copy.deepcopy(FINISH_SUMMARY_PROTECTED_PATH_FILTER_CONTRACT))
    index["contract_changes"] = filtered_contracts

def apply_finish_summary_path_snapshot_contract(
    index: dict[str, Any],
    *,
    protected_paths_filtered: bool,
    snapshot_unavailable: bool,
) -> None:
    contracts = index.get("contract_changes")
    existing = contracts if isinstance(contracts, list) else []
    index["contract_changes"] = [
        item
        for item in existing
        if not (
            isinstance(item, dict)
            and item.get("contract")
            in {
                FINISH_SUMMARY_PROTECTED_PATH_FILTER_CONTRACT["contract"],
                FINISH_SUMMARY_PATH_SNAPSHOT_UNAVAILABLE_CONTRACT["contract"],
            }
        )
    ]
    if snapshot_unavailable:
        index["contract_changes"].append(
            copy.deepcopy(FINISH_SUMMARY_PATH_SNAPSHOT_UNAVAILABLE_CONTRACT)
        )
    else:
        apply_finish_summary_path_filter_contract(index, protected_paths_filtered)

def finish_summary_string_array_errors(
    values: Any,
    label: str,
    *,
    minimum_items: int = 0,
    maximum_items: int | None = 100,
    minimum_length: int = 1,
    maximum_length: int = 500,
    exact_identity: bool = False,
) -> list[str]:
    if not isinstance(values, list):
        return [f"{label} must be an array."]
    errors: list[str] = []
    if len(values) < minimum_items or (
        maximum_items is not None and len(values) > maximum_items
    ):
        errors.append(f"{label} item count must be between {minimum_items} and {maximum_items}.")
    for index, value in enumerate(values):
        errors.extend(finish_summary_text_errors(value, f"{label}[{index}]", minimum_length, maximum_length))
    duplicate_errors = (
        finish_summary_exact_duplicate_errors(values, label)
        if exact_identity
        else finish_summary_duplicate_errors(values, label)
    )
    errors.extend(duplicate_errors)
    return errors

def finish_summary_retrieval_values(task_title: str, index: dict[str, Any]) -> list[str]:
    values: list[str] = [task_title, str(index.get("problem") or ""), str(index.get("outcome") or "")]
    values.extend(str(item) for item in index.get("changed_behavior", []) if isinstance(item, str))
    for item in index.get("affected_surfaces", []):
        if isinstance(item, dict) and isinstance(item.get("change"), str):
            values.append(item["change"])
    for item in index.get("contract_changes", []):
        if isinstance(item, dict):
            for key in ["before", "after"]:
                if isinstance(item.get(key), str):
                    values.append(item[key])
    search_terms = index.get("search_terms") if isinstance(index.get("search_terms"), dict) else {}
    values.extend(str(item) for item in search_terms.get("phrases", []) if isinstance(item, str))
    return [value.strip() for value in values if value.strip()]

def finish_summary_retrieval_text(task_title: str, index: dict[str, Any]) -> str:
    return "\n".join(finish_summary_retrieval_values(task_title, index))

def current_finish_summary_retrieval_text(task_title: str, index: dict[str, Any]) -> str:
    values: list[str] = []
    normalized: set[str] = set()
    for value in finish_summary_retrieval_values(task_title, index):
        key = finish_summary_normalized_text(value)
        if key and key not in normalized:
            values.append(value)
            normalized.add(key)
    return "\n".join(values)

def finish_summary_index_errors(index: Any, *, artifacts: dict[str, Any] | None = None, final: bool) -> list[str]:
    if not isinstance(index, dict):
        return ["index must be an object."]
    expected_keys = FINISH_SUMMARY_INDEX_KEYS | ({"retrieval_text"} if final else set())
    errors: list[str] = []
    if set(index) != expected_keys:
        errors.append(f"index keys must equal {sorted(expected_keys)}.")
    errors.extend(finish_summary_text_errors(index.get("problem"), "index.problem", 1, 400))
    errors.extend(finish_summary_text_errors(index.get("outcome"), "index.outcome", 1, 500))
    changed = index.get("changed_behavior")
    errors.extend(
        finish_summary_string_array_errors(
            changed, "index.changed_behavior", minimum_items=1, maximum_items=12, maximum_length=180
        )
    )
    surfaces = index.get("affected_surfaces")
    if not isinstance(surfaces, list):
        errors.append("index.affected_surfaces must be an array.")
    else:
        if not (1 <= len(surfaces) <= 20):
            errors.append("index.affected_surfaces item count must be between 1 and 20.")
        seen_surfaces: set[str] = set()
        for index_number, surface in enumerate(surfaces):
            label = f"index.affected_surfaces[{index_number}]"
            if not isinstance(surface, dict):
                errors.append(f"{label} must be an object.")
                continue
            if set(surface) != {"kind", "name", "paths", "change"}:
                errors.append(f"{label} keys are invalid.")
            if surface.get("kind") not in FINISH_SUMMARY_SURFACE_KINDS:
                errors.append(f"{label}.kind is invalid.")
            errors.extend(finish_summary_text_errors(surface.get("name"), f"{label}.name", 1, 200))
            paths = surface.get("paths")
            if not isinstance(paths, list):
                errors.append(f"{label}.paths must be an array.")
            else:
                if len(paths) > 100:
                    errors.append(f"{label}.paths exceeds 100 items.")
                for path_index, path in enumerate(paths):
                    errors.extend(finish_summary_path_errors(path, f"{label}.paths[{path_index}]"))
                errors.extend(finish_summary_exact_duplicate_errors(paths, f"{label}.paths"))
            errors.extend(finish_summary_text_errors(surface.get("change"), f"{label}.change", 1, 240))
            fingerprint = finish_summary_object_fingerprint(surface, exact_fields={"paths"})
            if fingerprint in seen_surfaces:
                errors.append(f"{label} duplicates an earlier affected surface.")
            seen_surfaces.add(fingerprint)
    contracts = index.get("contract_changes")
    if not isinstance(contracts, list):
        errors.append("index.contract_changes must be an array.")
    else:
        contract_limit = 20 if final else 19
        if len(contracts) > contract_limit:
            errors.append(f"index.contract_changes exceeds {contract_limit} items.")
        seen_contracts: set[str] = set()
        artifact_values = set(artifacts.values()) if isinstance(artifacts, dict) else set()
        for index_number, contract in enumerate(contracts):
            label = f"index.contract_changes[{index_number}]"
            if not isinstance(contract, dict):
                errors.append(f"{label} must be an object.")
                continue
            if set(contract) != {"contract", "before", "after", "source_artifact"}:
                errors.append(f"{label} keys are invalid.")
            errors.extend(finish_summary_text_errors(contract.get("contract"), f"{label}.contract", 1, 200))
            errors.extend(finish_summary_text_errors(contract.get("before"), f"{label}.before", 1, 400))
            errors.extend(finish_summary_text_errors(contract.get("after"), f"{label}.after", 1, 400))
            source_artifact = contract.get("source_artifact")
            if source_artifact != "":
                errors.extend(finish_summary_path_errors(source_artifact, f"{label}.source_artifact"))
                if final and source_artifact not in artifact_values:
                    errors.append(f"{label}.source_artifact must reference an artifacts value.")
            fingerprint = finish_summary_object_fingerprint(contract, exact_fields={"source_artifact"})
            if fingerprint in seen_contracts:
                errors.append(f"{label} duplicates an earlier contract change.")
            seen_contracts.add(fingerprint)
    search_terms = index.get("search_terms")
    expected_search_keys = FINISH_SUMMARY_SEARCH_TERM_KEYS if final else FINISH_SUMMARY_AI_SEARCH_TERM_KEYS
    if not isinstance(search_terms, dict):
        errors.append("index.search_terms must be an object.")
    else:
        if set(search_terms) != expected_search_keys:
            errors.append(f"index.search_terms keys must equal {sorted(expected_search_keys)}.")
        limits = {
            "issue_refs": (0, 100, 1, 30), "pr_refs": (0, 1, 1, 30),
            "branches": (0, 1, 1, 300), "paths": (0, None, 1, 500),
            "commands": (0, 100, 1, 200), "config_keys": (0, 100, 1, 200),
            "schema_fields": (0, 100, 1, 300), "symbols": (0, 100, 1, 300),
            "phrases": (3, 40, 2, 60),
        }
        for key in expected_search_keys:
            minimum_items, maximum_items, minimum_length, maximum_length = limits[key]
            values = search_terms.get(key)
            errors.extend(
                finish_summary_string_array_errors(
                    values, f"index.search_terms.{key}",
                    minimum_items=minimum_items, maximum_items=maximum_items,
                    minimum_length=minimum_length, maximum_length=maximum_length,
                    exact_identity=key == "paths",
                )
            )
            if final and key == "paths" and isinstance(values, list):
                for path_index, path in enumerate(values):
                    errors.extend(
                        finish_summary_path_errors(path, f"index.search_terms.paths[{path_index}]")
                    )
        phrases = search_terms.get("phrases") if isinstance(search_terms.get("phrases"), list) else []
        if phrases and not any(re.search(r"[\u3400-\u9fff]", phrase) for phrase in phrases if isinstance(phrase, str)):
            errors.append("index.search_terms.phrases must include a Chinese problem phrase.")
        searchable_tokens: list[str] = []
        for key in ["commands", "config_keys", "schema_fields", "symbols"]:
            values = search_terms.get(key)
            if isinstance(values, list):
                searchable_tokens.extend(str(value) for value in values)
        if final and isinstance(artifacts, dict):
            searchable_tokens.extend(Path(str(value)).name for value in artifacts.values())
        if final:
            paths = search_terms.get("paths")
            if isinstance(paths, list):
                searchable_tokens.extend(Path(str(value)).name for value in paths)
        if searchable_tokens and not any(
            token.casefold() in phrase.casefold()
            for token in searchable_tokens
            for phrase in phrases
            if token and isinstance(phrase, str)
        ):
            errors.append("index.search_terms.phrases must include an artifact/path/command/config/schema/symbol token.")
        if phrases and not any(
            marker in phrase for marker in FINISH_SUMMARY_COMPLETION_MARKERS
            for phrase in phrases if isinstance(phrase, str)
        ):
            errors.append("index.search_terms.phrases must include a completed-behavior phrase.")
    if final:
        errors.extend(finish_summary_text_errors(index.get("retrieval_text"), "index.retrieval_text", 1, 3000))
    return errors

def finish_summary_artifacts(task_dir: Path) -> dict[str, str]:
    return {
        key: filename
        for key, filename in CURRENT_FINISH_SUMMARY_ARTIFACT_FILES.items()
        if (task_dir / filename).is_file()
    }

def finish_summary_section_bullets(body: str, section_name: str) -> list[str]:
    section = find_pr_body_sections(body).get(section_name, "")
    bullets = [
        normalized_body_line(line)
        for line in section.splitlines()
        if line.strip().startswith(("-", "*", "•"))
        and normalized_body_line(line)
    ]
    return list(dict.fromkeys(bullets))

def finish_summary_surface_kind(path: str) -> str:
    if path.startswith(("trellis/workflows/", ".trellis/workflow")):
        return "workflow"
    if "/scripts/" in path or path.endswith((".py", ".sh")):
        return "script"
    if "/schemas/" in path or path.endswith(".schema.json"):
        return "schema"
    if "/overlays/" in path:
        return "overlay"
    if path.startswith("trellis/presets/"):
        return "preset"
    if "/skills/" in path:
        return "skill"
    if "/tests/" in path or Path(path).name.startswith("test_"):
        return "test"
    if path.endswith(("README.md", ".md")):
        return "docs"
    if path.endswith((".yml", ".yaml", ".toml")):
        return "config"
    if path.startswith((".codex/", ".claude/", ".cursor/", ".agents/")):
        return "prompt"
    if path.startswith(".trellis/tasks/"):
        return "task-artifact"
    return "other"

def build_finish_summary_index(
    task_title: str,
    pr_body: str,
    changed_paths: list[str],
) -> dict[str, Any]:
    changed_behavior = finish_summary_section_bullets(pr_body, "变更摘要")
    if not changed_behavior:
        raise WorkflowError(
            "Reviewed PR body must contain at least one concrete 变更摘要 bullet.",
            exit_code=2,
        )
    changed_behavior = changed_behavior[:12]
    grouped: dict[str, list[str]] = {}
    for path in changed_paths:
        grouped.setdefault(finish_summary_surface_kind(path), []).append(path)
    affected_surfaces = [
        {
            "kind": kind,
            "name": kind,
            "paths": paths[:100],
            "change": changed_behavior[0][:240],
        }
        for kind, paths in sorted(grouped.items())[:20]
    ]
    if not affected_surfaces:
        affected_surfaces = [{
            "kind": "other",
            "name": "task",
            "paths": [],
            "change": changed_behavior[0][:240],
        }]
    first_path_name = Path(changed_paths[0]).name if changed_paths else "task"
    phrase_candidates = [
        task_title[:60],
        changed_behavior[0][:60],
        f"完成 {first_path_name} 相关变更"[:60],
        "完成任务范围内合同同步",
    ]
    phrases: list[str] = []
    normalized: set[str] = set()
    for phrase in phrase_candidates:
        phrase = phrase.strip()
        key = finish_summary_normalized_text(phrase)
        if len(phrase) >= 2 and key and key not in normalized:
            phrases.append(phrase)
            normalized.add(key)
        if len(phrases) == 3:
            break
    if len(phrases) < 3:
        phrases.extend(["完成发布合同更新", "更新归档检索信息"][: 3 - len(phrases)])
    return {
        "problem": task_title[:400],
        "outcome": changed_behavior[0][:500],
        "changed_behavior": changed_behavior,
        "affected_surfaces": affected_surfaces,
        "contract_changes": [],
        "search_terms": {
            "commands": [],
            "config_keys": [],
            "schema_fields": [],
            "symbols": [first_path_name] if not changed_paths else [],
            "phrases": phrases,
        },
    }

def finish_summary_git_output_paths(output: str) -> set[str]:
    values = output.split("\0") if "\0" in output else output.splitlines()
    return {value for value in values if value}

def finish_summary_git_path_snapshot(
    root: Path,
    base_ref: str,
    *,
    include_worktree: bool,
) -> tuple[list[str], bool, bool]:
    range_spec = base_ref if include_worktree else f"{base_ref}...HEAD"
    proc = run(["git", "diff", "--name-only", "-z", range_spec], cwd=root, check=False)
    if proc.returncode != 0:
        return [], False, True
    paths = finish_summary_git_output_paths(proc.stdout)
    if include_worktree:
        untracked_proc = run(
            ["git", "ls-files", "--others", "--exclude-standard", "-z"],
            cwd=root,
            check=False,
        )
        if untracked_proc.returncode != 0:
            return [], False, True
        paths.update(finish_summary_git_output_paths(untracked_proc.stdout))
    safe_paths, protected_paths_filtered = sanitize_finish_summary_git_paths(paths)
    return safe_paths, protected_paths_filtered, False

def build_finish_summary(
    root: Path,
    task_dir: Path,
    task_context: dict[str, Any],
    pr_body: str,
    review_commit: str,
    *,
    pr_url: str = "",
    changed_paths: list[str] | None = None,
    archive_dir_override: str | None = None,
    generated_at_override: str | None = None,
    artifacts_override: dict[str, str] | None = None,
) -> dict[str, Any]:
    task = task_json(task_dir)
    base_branch = str(task_context.get("base_branch") or task.get("base_branch") or "").strip()
    base_ref = str(task_context.get("base_ref") or diff_base_ref(root, base_branch)).strip()
    commits_proc = run(["git", "rev-list", "--reverse", f"{base_ref}..{review_commit}"], cwd=root, check=False)
    if commits_proc.returncode != 0:
        raise WorkflowError("Could not calculate finish-summary task commits.", exit_code=2)
    commits = [line.strip() for line in commits_proc.stdout.splitlines() if line.strip()]
    if changed_paths is None:
        changed_paths, protected_paths_filtered, snapshot_unavailable = finish_summary_git_path_snapshot(
            root, base_ref, include_worktree=True
        )
    else:
        changed_paths, protected_paths_filtered = sanitize_finish_summary_git_paths(changed_paths)
        snapshot_unavailable = False
    github = {"pr_url": pr_url}
    artifacts = copy.deepcopy(artifacts_override) if artifacts_override is not None else finish_summary_artifacts(task_dir)
    task_title = str(task.get("title") or task.get("name") or task_dir.name)
    index = build_finish_summary_index(task_title, pr_body, changed_paths)
    apply_finish_summary_path_snapshot_contract(
        index,
        protected_paths_filtered=protected_paths_filtered,
        snapshot_unavailable=snapshot_unavailable,
    )
    pr_match = re.search(r"/pull/([1-9][0-9]*)$", pr_url)
    index["search_terms"] = {
        "issue_refs": [],
        "pr_refs": [f"PR #{pr_match.group(1)}"] if pr_match else [],
        "branches": [str(task_context.get("branch_name") or current_branch(root))],
        "paths": sorted(set(changed_paths)),
        **copy.deepcopy(index["search_terms"]),
    }
    index["retrieval_text"] = current_finish_summary_retrieval_text(task_title, index)
    payload = {
        "schema_version": FINISH_SUMMARY_SCHEMA_VERSION,
        "generated_at": generated_at_override or now_iso(),
        "generator": FINISH_SUMMARY_GENERATOR,
        "task": {
            "slug": task_dir.name,
            "title": task_title,
            "status": "completed",
            "artifact_dir": str(task_context.get("task_artifact_dir") or ""),
            "archive_dir": archive_dir_override or repo_relative(root, task_dir),
        },
        "git": {
            "base_branch": base_branch,
            "branch": str(task_context.get("branch_name") or current_branch(root)),
            "commits": commits,
            "changed_paths": sorted(set(changed_paths)),
        },
        "github": github,
        "artifacts": artifacts,
        "index": index,
    }
    errors = finish_summary_errors(payload, task_dir=None if archive_dir_override else task_dir)
    if errors:
        raise WorkflowError("Generated finish-summary validation failed.", exit_code=2, payload={"errors": errors})
    return payload

def finish_summary_errors(payload: Any, *, task_dir: Path | None = None) -> list[str]:
    if not isinstance(payload, dict):
        return ["finish-summary must be an object."]
    schema_version = payload.get("schema_version")
    historical = schema_version == HISTORICAL_FINISH_SUMMARY_SCHEMA_VERSION
    generator = payload.get("generator")
    expected_keys = {"schema_version", "generated_at", "generator", "task", "git", "github", "artifacts", "index"}
    errors: list[str] = []
    if set(payload) != expected_keys:
        errors.append(f"finish-summary top-level keys must equal {sorted(expected_keys)}.")
    if schema_version not in {
        FINISH_SUMMARY_SCHEMA_VERSION,
        HISTORICAL_FINISH_SUMMARY_SCHEMA_VERSION,
    }:
        errors.append("schema_version must be current integer 2 or historical integer 1.")
    generated_at = payload.get("generated_at")
    if not isinstance(generated_at, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", generated_at):
        errors.append("generated_at must be second-precision UTC RFC3339.")
    expected_generator = (
        HISTORICAL_FINISH_SUMMARY_GENERATOR if historical else FINISH_SUMMARY_GENERATOR
    )
    if generator != expected_generator:
        errors.append(f"generator must equal {expected_generator}.")
    task = payload.get("task")
    if not isinstance(task, dict) or set(task) != {"slug", "title", "status", "artifact_dir", "archive_dir"}:
        errors.append("task object keys are invalid.")
        task = {}
    errors.extend(finish_summary_text_errors(task.get("slug"), "task.slug", 1, 200))
    errors.extend(finish_summary_text_errors(task.get("title"), "task.title", 1, 500))
    if task.get("status") != "completed":
        errors.append("task.status must be completed.")
    errors.extend(finish_summary_path_errors(task.get("artifact_dir"), "task.artifact_dir"))
    errors.extend(finish_summary_path_errors(task.get("archive_dir"), "task.archive_dir"))
    if task.get("archive_dir") and not str(task.get("archive_dir")).startswith(".trellis/tasks/archive/"):
        errors.append("task.archive_dir must be under .trellis/tasks/archive/.")
    if task.get("artifact_dir"):
        artifact_dir_value = str(task.get("artifact_dir"))
        if not artifact_dir_value.startswith(".trellis/tasks/") or artifact_dir_value.startswith(".trellis/tasks/archive/"):
            errors.append("normal task.artifact_dir must be the original active task path.")
    if task_dir is not None:
        root_for_task = repo_root(task_dir)
        if not task_dir_is_archived(root_for_task, task_dir):
            errors.append("finish-summary must live in an archived task directory.")
        if task.get("slug") != task_dir.name:
            errors.append("task.slug must equal the archive task directory basename.")
        if task.get("archive_dir") != repo_relative(root_for_task, task_dir):
            errors.append("task.archive_dir must match the current archived task directory.")
    git = payload.get("git")
    if not isinstance(git, dict) or set(git) != {"base_branch", "branch", "commits", "changed_paths"}:
        errors.append("git object keys are invalid.")
        git = {}
    errors.extend(finish_summary_text_errors(git.get("base_branch"), "git.base_branch", 1, 300))
    errors.extend(finish_summary_text_errors(git.get("branch"), "git.branch", 1, 300))
    commits = git.get("commits")
    if not isinstance(commits, list) or len(commits) > 500:
        errors.append("git.commits must be an array with at most 500 items.")
    else:
        if len(set(commits)) != len(commits):
            errors.append("git.commits must be unique.")
        for commit in commits:
            if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
                errors.append("git.commits entries must be lowercase 40-character SHAs.")
    changed_paths = git.get("changed_paths")
    if not isinstance(changed_paths, list):
        errors.append("git.changed_paths must be an array.")
        changed_paths = []
    else:
        for path in changed_paths:
            errors.extend(finish_summary_path_errors(path, "git.changed_paths[]"))
        if changed_paths != sorted(set(changed_paths)):
            errors.append("git.changed_paths must be sorted and unique.")
    github = payload.get("github")
    github_keys = {"pr_url"}
    if not isinstance(github, dict) or set(github) != github_keys:
        errors.append("github object keys are invalid.")
        github = {}
    pr_url = github.get("pr_url")
    if (
        not isinstance(pr_url, str)
        or len(pr_url) > 1000
        or (pr_url and not re.fullmatch(r"https://github\.com/[^/]+/[^/]+/pull/[1-9][0-9]*", pr_url))
    ):
        errors.append("github.pr_url must be empty or a canonical GitHub pull URL.")
    artifact_contract = (
        HISTORICAL_FINISH_SUMMARY_ARTIFACT_FILES
        if historical
        else CURRENT_FINISH_SUMMARY_ARTIFACT_FILES
    )
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, dict) or any(key not in artifact_contract for key in artifacts):
        errors.append("artifacts keys are invalid.")
        artifacts = {}
    for key, path in artifacts.items():
        errors.extend(finish_summary_path_errors(path, f"artifacts.{key}"))
        if path != artifact_contract[key]:
            errors.append(f"artifacts.{key} must equal {artifact_contract[key]}.")
        if task_dir is not None and not (task_dir / str(path)).is_file():
            errors.append(f"artifacts.{key} does not exist in the archived task.")
    index = payload.get("index") if isinstance(payload.get("index"), dict) else {}
    errors.extend(finish_summary_index_errors(index, artifacts=artifacts, final=True))
    search_terms = index.get("search_terms") if isinstance(index.get("search_terms"), dict) else {}
    if search_terms.get("issue_refs") != []:
        errors.append("index.search_terms.issue_refs must be empty in the current contract.")
    pr_match = re.search(r"/pull/([1-9][0-9]*)$", pr_url or "")
    expected_pr_refs = [f"PR #{pr_match.group(1)}"] if pr_match else []
    if search_terms.get("pr_refs") != expected_pr_refs:
        errors.append("index.search_terms.pr_refs must be derived from github.pr_url.")
    expected_branches = [git.get("branch")] if git.get("branch") else []
    if search_terms.get("branches") != expected_branches:
        errors.append("index.search_terms.branches must be derived from git.branch.")
    if search_terms.get("paths") != changed_paths:
        errors.append("index.search_terms.paths must equal sorted git.changed_paths.")
    retrieval_builder = (
        finish_summary_retrieval_text
        if historical
        else current_finish_summary_retrieval_text
    )
    expected_retrieval = retrieval_builder(str(task.get("title") or ""), index)
    if index.get("retrieval_text") != expected_retrieval:
        errors.append("index.retrieval_text must equal the deterministic derived text.")
    return errors

PR_BODY_REQUIRED_SECTIONS = [
    "变更摘要",
    "影响范围",
    "验证结果",
    "Review Gate",
    "Issue 关闭范围",
    "安全说明",
    "Docs SSOT",
]

PR_BODY_SECTION_ALIASES = {
    "变更摘要": ["变更摘要", "更新摘要"],
    "影响范围": ["影响范围"],
    "验证结果": ["验证结果", "验证"],
    "Review Gate": ["Review Gate", "ReviewGate"],
    "Issue 关闭范围": ["Issue 关闭范围", "议题关闭范围", "关联议题"],
    "安全说明": ["安全说明", "安全与部署影响", "安全/部署影响", "安全和部署影响"],
    "Docs SSOT": ["Docs SSOT", "文档同步", "文档同步结果"],
}

PR_BODY_DOCS_SSOT_KEY_ALIASES = {
    "strategy": ["strategy", "策略", "ssot_first", "delta_first", "bootstrap_or_repair_docs", "no_docs_update_needed"],
    "durable_docs": ["durable docs", "长期文档", "durable 文档", "文档更新", "no-update", "无需更新"],
    "merged_delta": ["merged delta", "task delta", "task artifact delta", "任务文档差异", "任务差异", "任务增量", "同步", "回写", "写回", "合并", "merge"],
    "task_history": ["task history", "task-history-only", "任务历史", "仅保留"],
    "followup_or_limitation": ["follow-up", "followup", "后续", "限制", "limitation"],
}

PR_BODY_LOW_INFORMATION_PHRASES = [
    "当前 Trellis task",
    "已提交实现与文档更新",
    "详见 artifact",
    "详见 Trellis task artifact",
    "详见 Trellis task artifact 与 Review Gate 记录",
    "未提供具体 publish validation",
    "需要 AI 在 body file 中补充",
    "未记录 changed_files",
]

PR_BODY_PLACEHOLDER_VALUES = {
    "",
    "无",
    "n/a",
    "na",
    "none",
    "tbd",
    "todo",
    "待补充",
    "待定",
}

PR_CLOSE_KEYWORDS = ["Closes", "Fixes", "Resolves", "Close", "Fix", "Resolve"]

class WorkflowError(RuntimeError):
    def __init__(self, message: str, exit_code: int = 1, payload: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.exit_code = exit_code
        self.payload = payload or {}

GITHUB_ERROR_CODES = {
    "cli_missing": "github_cli_missing",
    "auth_failed": "github_auth_failed",
    "repo_access_denied": "github_repo_access_denied",
    "permission_denied": "github_permission_denied",
    "api_unavailable": "github_api_unavailable",
    "response_incomplete": "github_response_incomplete",
}

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

def require_gh_auth(root: Path) -> None:
    if shutil.which("gh") is None:
        raise WorkflowError(
            "GitHub CLI is not installed or is unavailable on PATH.",
            exit_code=2,
            payload={
                "error_code": GITHUB_ERROR_CODES["cli_missing"],
                "recovery": "Install GitHub CLI, then retry the same repo-bound operation.",
            },
        )
    proc = run(["gh", "auth", "status"], cwd=root, check=False)
    if proc.returncode != 0:
        raise WorkflowError(
            "GitHub CLI authentication is unavailable or invalid.",
            exit_code=2,
            payload={
                "error_code": GITHUB_ERROR_CODES["auth_failed"],
                "recovery": "Repair authentication with `gh auth login`, verify `gh auth status`, and retry.",
            },
        )

def github_error_from_process(
    proc: subprocess.CompletedProcess[str],
    *,
    operation: str,
    repo: str,
) -> WorkflowError:
    stderr = proc.stderr.strip()
    lowered = stderr.casefold()
    if (
        "could not resolve to a repository" in lowered
        or operation == "repo_access"
        and any(token in lowered for token in ("http 404", "not found"))
    ):
        category = "repo_access_denied"
        recovery = "Verify the owner/repository identity and grant the authenticated actor repository access."
    elif any(
        token in lowered
        for token in ("http 401", "authentication", "not logged", "bad credentials", "requires authentication")
    ):
        category = "auth_failed"
        recovery = "Repair authentication with `gh auth login`, verify `gh auth status`, and retry."
    elif any(
        token in lowered
        for token in ("http 403", "forbidden", "resource not accessible", "permission", "insufficient scope")
    ):
        category = "permission_denied"
        recovery = "Grant the authenticated actor the required repository permission or scope, then retry."
    elif any(
        token in lowered
        for token in (
            "http 500", "http 502", "http 503", "http 504", "timeout", "timed out",
            "connection refused", "could not resolve host", "network is unreachable", "tls handshake",
        )
    ):
        category = "api_unavailable"
        recovery = "Retry the same repo-bound GitHub CLI operation after API or network recovery."
    elif operation == "repo_access":
        category = "repo_access_denied"
        recovery = "Verify the owner/repository identity and the authenticated actor's repository access."
    else:
        category = "api_unavailable"
        recovery = "Inspect the GitHub CLI/API failure and retry the same repo-bound operation."
    return WorkflowError(
        f"GitHub CLI operation failed for {repo}: {operation}.",
        exit_code=2,
        payload={
            "error_code": GITHUB_ERROR_CODES[category],
            "operation": operation,
            "repo": repo,
            "exit_code": proc.returncode,
            "stderr_classification": category,
            "recovery": recovery,
        },
    )

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

def parse_nul_terminated_git_config_values(output: Any) -> list[str] | None:
    if not isinstance(output, str) or not output or not output.endswith("\0"):
        return None
    values = output.split("\0")
    if values[-1] != "" or any(value == "" for value in values[:-1]):
        return None
    return values[:-1]

def git_config_origin_is_nul_safe(root: Path, origin: str) -> bool:
    if not isinstance(origin, str) or not origin or any(
        unicodedata.category(character).startswith("C") for character in origin
    ):
        return False
    if origin == "command line:":
        return True
    if not origin.startswith("file:"):
        return False
    path = Path(origin[len("file:") :])
    if not path.is_absolute():
        path = root / path
    try:
        return b"\0" not in path.read_bytes()
    except OSError:
        return False

def parse_git_config_origin_value_pairs(
    root: Path, output: Any
) -> list[tuple[str, str]] | None:
    fields = parse_nul_terminated_git_config_values(output)
    if fields is None or len(fields) % 2 != 0:
        return None
    pairs = list(zip(fields[::2], fields[1::2]))
    if any(not git_config_origin_is_nul_safe(root, origin) for origin, _value in pairs):
        return None
    return pairs

def read_raw_git_config_values(
    root: Path, key: str, *, missing_allowed: bool
) -> list[str] | None:
    try:
        result = run(
            ["git", "config", "--null", "--show-origin", "--get-all", key],
            cwd=root,
            check=False,
        )
    except UnicodeError:
        return None
    if result.returncode == 1 and missing_allowed:
        return []
    if result.returncode != 0:
        return None
    pairs = parse_git_config_origin_value_pairs(root, result.stdout)
    return [value for _origin, value in pairs] if pairs is not None else None

def git_url_rewrite_config_is_safe(root: Path) -> bool:
    try:
        result = run(
            [
                "git",
                "config",
                "--null",
                "--show-origin",
                "--get-regexp",
                r"^url\..*\.(insteadof|pushinsteadof)$",
            ],
            cwd=root,
            check=False,
        )
    except UnicodeError:
        return False
    if result.returncode == 1:
        return True
    if result.returncode != 0:
        return False
    pairs = parse_git_config_origin_value_pairs(root, result.stdout)
    if pairs is None:
        return False
    for _origin, record in pairs:
        if record.count("\n") != 1:
            return False
        key, pattern = record.split("\n", 1)
        lowered = key.casefold()
        suffix = next(
            (
                candidate
                for candidate in [".insteadof", ".pushinsteadof"]
                if lowered.endswith(candidate)
            ),
            "",
        )
        base = key[len("url.") : -len(suffix)] if key.startswith("url.") and suffix else ""
        if not git_remote_config_value_is_safe(base) or not git_remote_config_value_is_safe(pattern):
            return False
    return True

def parse_effective_git_remote_urls(output: Any, expected_count: int) -> list[str] | None:
    if not isinstance(output, str) or not output.endswith("\n"):
        return None
    values = output[:-1].split("\n")
    if len(values) != expected_count or any(
        not git_remote_config_value_is_safe(value) for value in values
    ):
        return None
    return values

def validate_github_remote_repository(root: Path, remote: str, expected_repo: str) -> str:
    expected = normalize_github_repository(expected_repo)
    if not expected:
        raise WorkflowError("Closeout immutable GitHub repository identity is invalid.", exit_code=2)
    if not isinstance(remote, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", remote):
        raise WorkflowError("Closeout Git remote name is invalid.", exit_code=2)
    if not git_url_rewrite_config_is_safe(root):
        raise WorkflowError(
            "Closeout Git URL rewrite configuration is invalid.",
            exit_code=2,
            payload={"source": "url-rewrite-config"},
        )
    raw_fetch = read_raw_git_config_values(root, f"remote.{remote}.url", missing_allowed=False)
    raw_push = read_raw_git_config_values(root, f"remote.{remote}.pushurl", missing_allowed=True)
    if raw_fetch is None or raw_push is None or not raw_fetch:
        raise WorkflowError(
            "Closeout could not read the raw Git remote repository identity.",
            exit_code=2,
            payload={"remote": remote, "source": "raw-config"},
        )
    raw_urls = {"fetch": raw_fetch, "push": raw_push or raw_fetch}
    for direction, values in raw_urls.items():
        if any(not git_remote_config_value_is_safe(value) for value in values):
            raise WorkflowError(
                "Closeout raw Git remote repository identity is invalid.",
                exit_code=2,
                payload={"remote": remote, "direction": direction, "source": "raw-config"},
            )
    commands = {
        "fetch": ["git", "remote", "get-url", "--all", remote],
        "push": ["git", "remote", "get-url", "--push", "--all", remote],
    }
    for direction, command in commands.items():
        result = run(command, cwd=root, check=False)
        if result.returncode != 0:
            raise WorkflowError(
                "Closeout could not read the effective Git remote repository identity.",
                exit_code=2,
                payload={"remote": remote, "direction": direction},
            )
        urls = parse_effective_git_remote_urls(result.stdout, len(raw_urls[direction]))
        if not urls:
            raise WorkflowError(
                "Closeout effective Git remote repository output is invalid.",
                exit_code=2,
                payload={"remote": remote, "direction": direction},
            )
        for value in urls:
            actual = parse_github_remote_repository_url(value)
            if actual != expected:
                raise WorkflowError(
                    "Closeout Git remote repository differs from the immutable GitHub repository.",
                    exit_code=2,
                    payload={"remote": remote, "direction": direction, "expected_repo": expected},
                )
    return expected

def infer_github_repo(root: Path) -> str:
    try:
        result = run(["git", "remote", "get-url", "origin"], cwd=root, check=False)
    except UnicodeError:
        return ""
    if result.returncode != 0:
        return ""
    urls = parse_effective_git_remote_urls(result.stdout, 1)
    return parse_github_remote_repository_url(urls[0]) if urls else ""

def github_repo_binding(args: list[str], explicit_repo: str | None = None) -> str:
    repo = normalize_github_repository(explicit_repo)
    if not args:
        return ""
    if args[0] in {"issue", "pr", "run"}:
        if "--repo" not in args:
            return ""
        index = args.index("--repo")
        bound = normalize_github_repository(args[index + 1] if index + 1 < len(args) else "")
        if not bound or (repo and bound != repo):
            return ""
        return bound
    if args[0] == "api" and len(args) > 1:
        match = re.match(r"^repos/([^/]+/[^/]+)(?:/|$)", args[1])
        if not match:
            return ""
        bound = normalize_github_repository(match.group(1))
        if not bound or (repo and bound != repo):
            return ""
        return bound
    return ""

def github_response_incomplete(
    *, operation: str, repo: str, detail: str
) -> WorkflowError:
    return WorkflowError(
        f"GitHub CLI response is incomplete for {repo}: {operation}.",
        exit_code=2,
        payload={
            "error_code": GITHUB_ERROR_CODES["response_incomplete"],
            "operation": operation,
            "repo": repo,
            "detail": detail,
            "recovery": "Fail closed and repair the adapter/query contract before retrying.",
        },
    )

def gh_json(
    args: list[str],
    cwd: Path,
    *,
    repo: str | None = None,
    required_fields: tuple[str, ...] = (),
    operation: str = "read",
) -> Any:
    bound_repo = github_repo_binding(args, repo)
    if not bound_repo:
        raise github_response_incomplete(
            operation=operation,
            repo=normalize_github_repository(repo) or "<unbound>",
            detail="GitHub CLI command lacks an explicit or matching repository binding.",
        )
    require_gh_auth(cwd)
    proc = run(["gh", *args], cwd=cwd, check=False)
    if proc.returncode != 0:
        raise github_error_from_process(proc, operation=operation, repo=bound_repo)
    text = proc.stdout.strip()
    if not text:
        raise github_response_incomplete(
            operation=operation, repo=bound_repo, detail="Response body is empty."
        )
    try:
        payload = json.loads(text)
    except (json.JSONDecodeError, TypeError) as exc:
        raise github_response_incomplete(
            operation=operation, repo=bound_repo, detail="Response body is not valid JSON."
        ) from exc
    if required_fields:
        rows = payload if isinstance(payload, list) else [payload]
        if any(
            not isinstance(row, dict) or any(field not in row or row[field] is None for field in required_fields)
            for row in rows
        ):
            raise github_response_incomplete(
                operation=operation,
                repo=bound_repo,
                detail="Required fields are missing: " + ", ".join(required_fields),
            )
    return payload

def git_branch_exists(root: Path, ref: str) -> bool:
    return run(["git", "rev-parse", "--verify", "--quiet", ref], cwd=root, check=False).returncode == 0

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

def ai_first_git_blob_contents(
    root: Path,
    object_specs: dict[str, str],
) -> dict[str, bytes]:
    ordered = [
        (relative, object_specs[relative])
        for relative in sorted(object_specs, key=lambda item: item.encode("utf-8"))
        if "\n" not in object_specs[relative] and "\r" not in object_specs[relative]
    ]
    if not ordered:
        return {}
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=str(root),
        input=("\n".join(spec for _relative, spec in ordered) + "\n").encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        return {}
    contents: dict[str, bytes] = {}
    offset = 0
    for relative, _spec in ordered:
        header_end = proc.stdout.find(b"\n", offset)
        if header_end < 0:
            return {}
        header = proc.stdout[offset:header_end]
        offset = header_end + 1
        if header.endswith(b" missing"):
            continue
        fields = header.split(b" ")
        if len(fields) != 3:
            return {}
        try:
            size = int(fields[2])
        except ValueError:
            return {}
        content_end = offset + size
        if content_end >= len(proc.stdout) or proc.stdout[content_end:content_end + 1] != b"\n":
            return {}
        content = proc.stdout[offset:content_end]
        offset = content_end + 1
        if fields[1] == b"blob":
            contents[relative] = content
    if offset != len(proc.stdout):
        return {}
    return contents

def git_status_paths(root: Path, *, fail_closed: bool = False) -> list[str]:
    proc = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all", "--no-renames"],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        if fail_closed:
            raise WorkflowError("Could not inspect Git status paths.", exit_code=2)
        return []
    paths: list[str] = []
    for record in proc.stdout.split(b"\0"):
        if not record:
            continue
        if len(record) < 4:
            if fail_closed:
                raise WorkflowError("Git status returned an invalid path record.", exit_code=2)
            continue
        try:
            path = record[3:].decode("utf-8", "strict")
            if not ai_first_os_noise_path(path):
                paths.append(path)
        except UnicodeError as exc:
            if fail_closed:
                raise WorkflowError("Git status returned an invalid path record.", exit_code=2) from exc
            raise
    return paths

def normalize_ref(ref: str) -> str:
    return ref.removeprefix("refs/heads/")

def diff_base_ref(root: Path, base_branch: str) -> str:
    candidates: list[str] = []
    base = normalize_ref(base_branch)
    if base.startswith("origin/"):
        candidates.append(base)
        candidates.append(base.split("/", 1)[1])
    else:
        candidates.append(f"origin/{base}")
        candidates.append(base)
    for candidate in candidates:
        if git_branch_exists(root, candidate):
            return candidate
    return candidates[0]

def is_ancestor(root: Path, ancestor: str, descendant: str = "HEAD") -> bool:
    return run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=root, check=False).returncode == 0

def worktree_records(root: Path) -> list[dict[str, str]]:
    proc = run(["git", "worktree", "list", "--porcelain"], cwd=root, check=False)
    records: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in [*proc.stdout.splitlines(), ""]:
        if not line.strip():
            if current.get("worktree"):
                records.append(current)
            current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    return records

def runtime_root(root: Path, config: dict[str, Any]) -> Path:
    rel = Path(str(config.get("runtime_root") or DEFAULTS["runtime_root"]))
    return rel if rel.is_absolute() else root / rel

def ai_first_task_checkpoint_key(task_dir: Path) -> str:
    identity = task_dir.name
    task_path = task_dir / "task.json"
    if task_path.is_file() and not task_path.is_symlink():
        try:
            payload = read_json(task_path)
        except (OSError, ValueError, WorkflowError):
            payload = {}
        candidate = str(payload.get("id") or "").strip()
        if candidate:
            identity = candidate
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()[:20]

def ai_first_owner_checkpoint_path(
    root: Path,
    task_dir: Path,
    artifact_name: str,
) -> Path:
    if artifact_name not in AI_FIRST_OWNER_ARTIFACTS:
        raise WorkflowError(
            f"Unsupported AI-first owner artifact: {artifact_name}",
            exit_code=2,
        )
    return (
        runtime_root(root, load_config(root))
        / AI_FIRST_OWNER_CHECKPOINT_DIR
        / ai_first_task_checkpoint_key(task_dir)
        / artifact_name
    )

def runtime_workspace_path(root: Path, config: dict[str, Any], workspace_slug: str) -> Path:
    return runtime_root(root, config) / "workspaces" / f"{workspace_slug}.json"

def runtime_task_path(root: Path, config: dict[str, Any], task_slug: str) -> Path:
    return runtime_root(root, config) / "tasks" / f"{task_slug}.json"

def write_runtime_mappings(root: Path, config: dict[str, Any], payload: dict[str, Any], workspace_path: Path) -> None:
    workspace_slug = str(payload["workspace_slug"])
    roots = {root.resolve(), workspace_path.resolve()}
    workspace_payload = {
        "schema_version": "1.0", "workspace_slug": workspace_slug,
        "workspace_path": str(workspace_path.resolve()), "source_checkout": str(root.resolve()),
        "branch_name": payload["branch_name"], "updated_at": now_iso(),
    }
    for runtime_repo in roots:
        write_json(runtime_workspace_path(runtime_repo, config, workspace_slug), workspace_payload)
    task_slug = str(payload.get("task_slug") or "")
    task_dir = str(payload.get("task_dir") or "")
    if task_slug and task_dir:
        task_payload = {
            "schema_version": "1.0", "task_slug": task_slug, "workspace_slug": workspace_slug,
            "workspace_path": str(workspace_path.resolve()), "task_artifact_dir": task_dir,
            "updated_at": now_iso(),
        }
        for runtime_repo in roots:
            write_json(runtime_task_path(runtime_repo, config, task_slug), task_payload)

def rebuild_runtime_mappings(root: Path, config: dict[str, Any], context: dict[str, Any]) -> dict[str, Any] | None:
    workspace_slug = str(context.get("workspace_slug") or "").strip()
    task_slug = str(context.get("task_slug") or "").strip()
    task_dir = str(context.get("task_artifact_dir") or "").strip()
    branch_name = str(context.get("branch_name") or "").strip()
    if not all([workspace_slug, task_slug, task_dir, branch_name]):
        return None

    records = worktree_records(root)
    expected_branch = f"refs/heads/{branch_name}"
    matches = [
        Path(record["worktree"]).resolve()
        for record in records
        if record.get("branch") == expected_branch
        and (Path(record["worktree"]) / task_dir / "task.json").is_file()
    ]
    if len(matches) != 1:
        return None

    workspace_path = matches[0]
    base_branch = str(context.get("base_branch") or "").strip()
    base_ref = f"refs/heads/{base_branch}" if base_branch else ""
    source_candidates = [
        Path(record["worktree"]).resolve()
        for record in records
        if Path(record["worktree"]).resolve() != workspace_path
        and (not base_ref or record.get("branch") == base_ref)
    ]
    source_checkout = source_candidates[0] if source_candidates else root.resolve()
    payload = {
        "workspace_slug": workspace_slug,
        "task_slug": task_slug,
        "task_dir": task_dir,
        "branch_name": branch_name,
    }
    write_runtime_mappings(source_checkout, config, payload, workspace_path)
    cache, _ = read_optional_json(runtime_workspace_path(workspace_path, config, workspace_slug))
    return cache

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

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

def load_task_runtime_identity(task_dir: Path, config: dict[str, Any]) -> dict[str, Any]:
    task_path = task_dir / "task.json"
    if not task_path.is_file() or task_path.is_symlink():
        return {}
    root = repo_root(task_dir)
    task = read_json(task_path)
    task_slug = str(task.get("id") or task.get("name") or "").strip()
    task_relative = repo_relative(root, task_dir)
    branch_name = str(task.get("branch") or "").strip()
    base_branch = str(task.get("base_branch") or "").strip()
    if not all((task_slug, task_relative, branch_name, base_branch)):
        raise WorkflowError(
            "Task runtime identity requires task.json id, branch and base_branch.",
            exit_code=2,
        )

    task_mapping_path = runtime_task_path(root, config, task_slug)
    task_mapping, task_mapping_error = read_optional_json(task_mapping_path)
    if task_mapping is None and task_mapping_error == "missing":
        rebuild_runtime_mappings(
            root,
            config,
            {
                "workspace_slug": root.name,
                "task_slug": task_slug,
                "task_artifact_dir": task_relative,
                "branch_name": branch_name,
                "base_branch": base_branch,
            },
        )
        task_mapping, task_mapping_error = read_optional_json(task_mapping_path)
    if task_mapping is None:
        raise WorkflowError(
            "Task runtime identity could not derive or rebuild the ignored task mapping.",
            exit_code=2,
            payload={"path": str(task_mapping_path), "error": task_mapping_error},
        )
    workspace_slug = str(task_mapping.get("workspace_slug") or "").strip()
    expected_task_mapping = {
        "schema_version": "1.0",
        "task_slug": task_slug,
        "workspace_slug": workspace_slug,
        "workspace_path": str(root.resolve()),
        "task_artifact_dir": task_relative,
    }
    if not workspace_slug or any(
        task_mapping.get(key) != value for key, value in expected_task_mapping.items()
    ):
        raise WorkflowError(
            "Ignored task runtime mapping does not match task.json and the current checkout.",
            exit_code=2,
            payload={"path": str(task_mapping_path)},
        )

    workspace_mapping_path = runtime_workspace_path(root, config, workspace_slug)
    workspace_mapping, workspace_mapping_error = read_optional_json(workspace_mapping_path)
    if workspace_mapping is None:
        raise WorkflowError(
            "Task runtime identity requires the ignored workspace mapping.",
            exit_code=2,
            payload={"path": str(workspace_mapping_path), "error": workspace_mapping_error},
        )
    expected_workspace_mapping = {
        "schema_version": "1.0",
        "workspace_slug": workspace_slug,
        "workspace_path": str(root.resolve()),
        "branch_name": branch_name,
    }
    if any(
        workspace_mapping.get(key) != value
        for key, value in expected_workspace_mapping.items()
    ):
        raise WorkflowError(
            "Ignored workspace runtime mapping does not match task.json and the current checkout.",
            exit_code=2,
            payload={"path": str(workspace_mapping_path)},
        )

    current_records = [
        record
        for record in worktree_records(root)
        if Path(record.get("worktree") or "").resolve() == root.resolve()
    ]
    if (
        len(current_records) != 1
        or current_records[0].get("branch") != f"refs/heads/{branch_name}"
    ):
        raise WorkflowError(
            "Current Git worktree identity does not match task.json branch.",
            exit_code=2,
        )

    base_ref = diff_base_ref(root, base_branch)
    merge_base = run(
        ["git", "merge-base", base_ref, "HEAD"], cwd=root, check=False
    )
    base_head_sha = merge_base.stdout.strip() if merge_base.returncode == 0 else ""
    if not re.fullmatch(r"[0-9a-f]{40}", base_head_sha):
        raise WorkflowError(
            "Could not derive the current task base from live Git facts.",
            exit_code=2,
        )

    source_repo = str(config.get("github_repo") or "").strip() or infer_github_repo(root)
    return {
        "_path": str(task_mapping_path),
        "_identity_source": "task_json_runtime_mapping",
        "schema_version": "runtime-1.0",
        "source_repo": {"repo": source_repo},
        "task_slug": task_slug,
        "task_title": str(task.get("title") or task.get("name") or task_slug),
        "task_artifact_dir": task_relative,
        "task_dir": task_relative,
        "branch_name": branch_name,
        "base_branch": base_branch,
        "base_ref": base_ref,
        "base_head_sha": base_head_sha,
        "remote_head_sha": "",
        "workspace_slug": workspace_slug,
        "task_workspace_id": workspace_slug,
        "assignee": str(task.get("assignee") or ""),
        "actor": {"login": str(task.get("creator") or task.get("assignee") or "")},
        "intake_summary": {},
    }

def tasks_root(root: Path) -> Path:
    return root / ".trellis/tasks"

def resolve_existing_task_dir(root: Path, value: str) -> Path | None:
    raw = Path(value)
    candidates: list[Path] = []
    if raw.is_absolute():
        candidates.append(raw)
    else:
        candidates.extend([root / raw, tasks_root(root) / value])
    for candidate in candidates:
        if candidate.is_dir() and (candidate / "task.json").is_file():
            return candidate.resolve()

    base_name = raw.name.rstrip("/")
    task_root = tasks_root(root)
    active = task_root / base_name
    if active.is_dir() and (active / "task.json").is_file():
        return active.resolve()
    archive_root = task_root / "archive"
    if archive_root.is_dir():
        for month in sorted(archive_root.iterdir(), reverse=True):
            archived = month / base_name
            if archived.is_dir() and (archived / "task.json").is_file():
                return archived.resolve()
    return None

def current_task_dir(root: Path) -> Path | None:
    task_script = root / ".trellis/scripts/task.py"
    if not task_script.exists():
        return None
    proc = run([sys.executable, "./.trellis/scripts/task.py", "current"], cwd=root, check=False)
    value = proc.stdout.strip()
    if proc.returncode == 0 and value:
        return resolve_existing_task_dir(root, value)
    return None

def resolve_task_dir(
    root: Path,
    task_arg: str | None,
    context: dict[str, Any] | None = None,
) -> Path:
    if task_arg:
        resolved = resolve_existing_task_dir(root, task_arg)
        if resolved:
            return resolved
        raise WorkflowError(f"Could not resolve task directory: {task_arg}")

    if context:
        context_task = str(context.get("task_artifact_dir") or "").strip()
        if context_task:
            resolved = resolve_existing_task_dir(root, context_task)
            if resolved:
                return resolved

    current = current_task_dir(root)
    if current:
        return current
    raise WorkflowError("Could not resolve current Trellis task. Pass --task <task-dir>.")

def path_within(parent: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False

def optional_resolved_path(value: Any) -> Path | None:
    text = str(value or "").strip()
    if not text:
        return None
    return Path(text).expanduser().resolve()

def safe_git_status_paths(root: Path | None) -> list[str]:
    if root is None or not root.exists():
        return []
    try:
        return git_status_paths(root)
    except (OSError, subprocess.SubprocessError):
        return []

def source_path_is_tracked_clean(root: Path, relative_path: str) -> bool:
    """Return whether one source path is tracked by Git and clean at every layer."""
    try:
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", relative_path],
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if tracked.returncode != 0 or not tracked.stdout.strip():
            return False
        for diff_args in (
            ["git", "diff", "--quiet", "--cached", "--", relative_path],
            ["git", "diff", "--quiet", "--", relative_path],
        ):
            if subprocess.run(
                diff_args,
                cwd=str(root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            ).returncode != 0:
                return False
        return True
    except OSError:
        return False

def workspace_boundary_context(
    root: Path,
    config: dict[str, Any],
    context: dict[str, Any],
    task_dir: Path,
) -> dict[str, Any]:
    workspace_mode = str(config.get("workspace_mode") or "").strip()
    task_relative = str(context.get("task_artifact_dir") or repo_relative(root, task_dir)).strip("/")
    expected_workspace = root.resolve()
    source_checkout = None
    workspace_slug = str(context.get("workspace_slug") or "").strip()
    if workspace_slug:
        cache, _ = read_optional_json(runtime_workspace_path(root, config, workspace_slug))
        if not cache:
            cache = rebuild_runtime_mappings(root, config, context)
        cached_path = optional_resolved_path((cache or {}).get("workspace_path"))
        if cached_path and cached_path.exists():
            expected_workspace = cached_path
            source_checkout = optional_resolved_path((cache or {}).get("source_checkout"))
    return {
        "workspace_mode": workspace_mode,
        "expected_workspace": expected_workspace,
        "actual_repo_root": root.resolve(),
        "source_checkout": source_checkout,
        "task_dir": task_dir.resolve(),
        "task_dir_relative": task_relative,
        "task_context_present": bool(context),
    }

def collect_workspace_boundary_snapshot(
    context: dict[str, Any],
    config: dict[str, Any],
    task_context: dict[str, Any],
) -> dict[str, Any]:
    actual_root = context["actual_repo_root"]
    expected_workspace = context.get("expected_workspace")
    source_checkout = context.get("source_checkout")
    task_dir = context["task_dir"]
    task_relative = str(context.get("task_dir_relative") or "").strip("/")
    task_status_root = expected_workspace if isinstance(expected_workspace, Path) else actual_root
    source_status = safe_git_status_paths(source_checkout if isinstance(source_checkout, Path) else None)
    task_status = safe_git_status_paths(task_status_root if isinstance(task_status_root, Path) else None)
    suspicious: list[dict[str, Any]] = []

    if (
        isinstance(source_checkout, Path)
        and task_relative
        and (
            not isinstance(expected_workspace, Path)
            or source_checkout.resolve() != expected_workspace.resolve()
        )
    ):
        source_task_dir = (source_checkout / task_relative).resolve()
        for name in WORKSPACE_BOUNDARY_SUSPICIOUS_TASK_ARTIFACTS:
            artifact = source_task_dir / name
            relative_path = f"{task_relative}/{name}"
            if artifact.exists() and (
                name in WORKSPACE_BOUNDARY_REVIEW_METADATA
                or not source_path_is_tracked_clean(source_checkout, relative_path)
            ):
                suspicious.append(
                    {
                        "kind": "same_task_review_metadata" if name in WORKSPACE_BOUNDARY_REVIEW_METADATA else "same_task_artifact",
                        "path": repo_relative(source_checkout, artifact),
                        "absolute_path": str(artifact.resolve()),
                    }
                )
        reviews_dir = source_task_dir / REVIEW_ROUND_REPORT_DIR
        if reviews_dir.exists():
            suspicious.append(
                {
                    "kind": "same_task_reviews_dir",
                    "path": repo_relative(source_checkout, reviews_dir),
                    "absolute_path": str(reviews_dir.resolve()),
                }
            )
        for dirty_path in source_status:
            normalized = dirty_path.strip().replace("\\", "/")
            if normalized.startswith(f"{task_relative}/"):
                suspicious.append(
                    {
                        "kind": "same_task_dirty_path",
                        "path": normalized,
                        "absolute_path": str((source_checkout / normalized).resolve()),
                    }
                )

    return {
        "workspace_mode": context.get("workspace_mode"),
        "expected_workspace": str(expected_workspace) if expected_workspace else None,
        "actual_repo_root": str(actual_root),
        "source_checkout": str(source_checkout) if source_checkout else None,
        "task_dir": str(task_dir),
        "task_dir_relative": task_relative,
        "source_checkout_status": source_status,
        "task_worktree_status": task_status,
        "suspicious_source_artifacts": suspicious,
    }

def blocking_suspicious_source_artifacts(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in snapshot.get("suspicious_source_artifacts", []) if isinstance(item, dict)]

def workspace_boundary_errors(
    context: dict[str, Any],
    snapshot: dict[str, Any],
    *,
    allow_source_clean: bool = False,
) -> list[str]:
    errors: list[str] = []
    task_context_present = bool(context.get("task_context_present"))
    workspace_mode = str(context.get("workspace_mode") or "")
    expected_workspace = context.get("expected_workspace")
    actual_root = context["actual_repo_root"]
    source_checkout = context.get("source_checkout")
    task_dir = context["task_dir"]
    blockers = blocking_suspicious_source_artifacts(snapshot)

    if workspace_mode == "worktree" and not task_context_present:
        errors.append("workspace boundary 缺少可验证的 task/runtime/worktree identity。")
    elif workspace_mode == "worktree" and isinstance(expected_workspace, Path) and actual_root.resolve() != expected_workspace.resolve():
            allow_source = (
                allow_source_clean
                and isinstance(source_checkout, Path)
                and actual_root.resolve() == source_checkout.resolve()
                and not snapshot.get("source_checkout_status")
                and not blockers
            )
            if not allow_source:
                errors.append(
                    "workspace boundary mismatch: expected runtime workspace="
                    f"{expected_workspace}, actual_repo_root={actual_root}, source_checkout={source_checkout or '(unknown)'}, task_dir={task_dir}."
                )

    if not path_within(tasks_root(actual_root), task_dir):
        errors.append(
            "workspace boundary mismatch: task_dir must be under the actual repo root .trellis/tasks; "
            f"actual_repo_root={actual_root}, task_dir={task_dir}."
        )

    if blockers:
        blocked_paths = [str(item.get("absolute_path") or item.get("path")) for item in blockers]
        errors.append(
            "workspace boundary blocked: source checkout contains current-task artifacts or review metadata: "
            + ", ".join(blocked_paths[:20])
        )
    return errors

def workspace_boundary_snapshot(
    root: Path,
    config: dict[str, Any],
    task_context: dict[str, Any],
    task_dir: Path,
    *,
    allow_source_clean: bool = False,
) -> dict[str, Any]:
    context = workspace_boundary_context(root, config, task_context, task_dir)
    snapshot = collect_workspace_boundary_snapshot(context, config, task_context)
    errors = workspace_boundary_errors(context, snapshot, allow_source_clean=allow_source_clean)
    snapshot["status"] = "blocked" if errors else "ok"
    snapshot["errors"] = errors
    return snapshot

def assert_workspace_boundary(
    root: Path,
    config: dict[str, Any],
    task_context: dict[str, Any],
    task_dir: Path,
    *,
    allow_source_clean: bool = False,
) -> dict[str, Any]:
    snapshot = workspace_boundary_snapshot(
        root,
        config,
        task_context,
        task_dir,
        allow_source_clean=allow_source_clean,
    )
    if snapshot["errors"]:
        raise WorkflowError(
            "Workspace boundary validation failed.",
            exit_code=2,
            payload=snapshot,
        )
    return snapshot

def task_json(task_dir: Path) -> dict[str, Any]:
    return read_json(task_dir / "task.json")
