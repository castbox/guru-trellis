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

import time

import unicodedata

from collections.abc import Iterable

from datetime import datetime, timezone

from pathlib import Path

from typing import Any

from urllib.parse import quote, urlsplit

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

PROVENANCE_TAIL_INAPPLICABLE_ERRORS = frozenset({
    "provenance_tail_changed_paths_invalid",
    "provenance_tail_parent_mismatch",
})

PROVENANCE_TAIL_OBJECT_PRESENCE = object()

PROVENANCE_APPLY_PLATFORMS = ("claude", "codex", "cursor")

AGENT_ASSIGNMENT_ARTIFACT = "agent-assignment.json"

REVIEW_REPORT_ARTIFACT = "review.md"

FINISH_SUMMARY_ARTIFACT = "finish-summary.json"

CLOSEOUT_PLAN_ARTIFACT = "closeout-plan.json"

FINALIZATION_TRANSACTION_ARTIFACT = "finalization-transaction.json"

TASK_FINALIZATION_GATE_ARTIFACT = "task-finalization-gate.json"

TASK_FINALIZATION_TRANSITION_GATE_ARTIFACT = "task-finalization-transition-gate.json"

CLOSEOUT_PLAN_SCHEMA_VERSION = "4.0"

LEGACY_CLOSEOUT_PLAN_SCHEMA_VERSION = "2.0"

LEGACY_CLOSEOUT_RETIRED_ARTIFACTS = {
    "pr-" "body.md",
    "finish-summary-" "index.json",
}

CLOSEOUT_ARCHIVE_DURABLE_ARTIFACTS = {
    "task.json",
    "prd.md",
    "design.md",
    "implement.md",
    "issue-scope-ledger.json",
    FINISH_SUMMARY_ARTIFACT,
}

CLOSEOUT_ARCHIVE_CORE_ARTIFACTS = {
    *CLOSEOUT_ARCHIVE_DURABLE_ARTIFACTS,
}

CLOSEOUT_ARCHIVE_MAX_ARTIFACTS = 6

CLOSEOUT_ARCHIVE_LEGACY_MAX_ARTIFACTS = 8

CLOSEOUT_PR_PLACEHOLDER_NUMBER = 9223372036854775807

CLOSEOUT_PR_HEAD_READ_ATTEMPTS = 6

CLOSEOUT_PR_HEAD_READ_DELAY_SECONDS = 1

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
    "issue_scope_ledger": "issue-scope-ledger.json",
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
    "issue-scope-ledger.json",
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

def finish_summary_issue_numbers(ledger: dict[str, Any], key: str) -> list[int]:
    if key == "source_issues":
        primary = ledger.get("primary_issue")
        values = [primary] if isinstance(primary, dict) else []
    else:
        ledger_key = {"close_issues": "close_issues", "related_issues": "related_issues", "followup_issues": "followup_issues"}[key]
        raw = ledger.get(ledger_key)
        values = raw if isinstance(raw, list) else []
    numbers = {
        int(item["number"])
        for item in values
        if isinstance(item, dict) and isinstance(item.get("number"), int) and not isinstance(item.get("number"), bool) and item["number"] > 0
    }
    return sorted(numbers)

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
    ledger: dict[str, Any],
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
    github = {
        key: finish_summary_issue_numbers(ledger, key)
        for key in ["source_issues", "close_issues", "related_issues", "followup_issues"]
    }
    github["pr_url"] = pr_url
    artifacts = copy.deepcopy(artifacts_override) if artifacts_override is not None else finish_summary_artifacts(task_dir)
    task_title = str(task.get("title") or task.get("name") or task_dir.name)
    index = build_finish_summary_index(task_title, pr_body, changed_paths)
    apply_finish_summary_path_snapshot_contract(
        index,
        protected_paths_filtered=protected_paths_filtered,
        snapshot_unavailable=snapshot_unavailable,
    )
    issue_numbers = sorted({number for key in ["source_issues", "close_issues", "related_issues", "followup_issues"] for number in github[key]})
    pr_match = re.search(r"/pull/([1-9][0-9]*)$", pr_url)
    index["search_terms"] = {
        "issue_refs": [f"#{number}" for number in issue_numbers],
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
    github_keys = {"source_issues", "close_issues", "related_issues", "followup_issues", "pr_url"}
    if not isinstance(github, dict) or set(github) != github_keys:
        errors.append("github object keys are invalid.")
        github = {}
    for key in ["source_issues", "close_issues", "related_issues", "followup_issues"]:
        values = github.get(key)
        if not isinstance(values, list) or len(values) > 100 or any(isinstance(value, bool) or not isinstance(value, int) or value < 1 for value in values):
            errors.append(f"github.{key} must contain positive issue integers.")
        elif values != sorted(set(values)):
            errors.append(f"github.{key} must be sorted and unique.")
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
    issue_values = sorted({number for key in ["source_issues", "close_issues", "related_issues", "followup_issues"] for number in github.get(key, []) if isinstance(number, int) and not isinstance(number, bool)})
    if search_terms.get("issue_refs") != [f"#{number}" for number in issue_values]:
        errors.append("index.search_terms.issue_refs must be derived from all GitHub issue arrays.")
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

def validate_finish_summary(payload: Any, *, task_dir: Path | None = None) -> None:
    errors = finish_summary_errors(payload, task_dir=task_dir)
    if errors:
        raise WorkflowError("finish-summary validation failed.", exit_code=2, payload={"errors": errors})

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

def run_gh_command(
    args: list[str],
    cwd: Path,
    *,
    repo: str | None = None,
    operation: str,
) -> subprocess.CompletedProcess[str]:
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
    return proc

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

def ai_first_retire_owner_checkpoints(
    root: Path,
    task_dir: Path,
    artifact_names: Iterable[str],
) -> list[str]:
    retired: list[str] = []
    checkpoint_dir: Path | None = None
    for artifact_name in artifact_names:
        path = ai_first_owner_checkpoint_path(root, task_dir, artifact_name)
        checkpoint_dir = path.parent
        if path.is_symlink():
            raise WorkflowError(
                f"AI-first owner checkpoint is unsafe: {artifact_name}",
                exit_code=2,
            )
        if path.is_file():
            path.unlink()
            retired.append(artifact_name)
        elif path.exists():
            raise WorkflowError(
                f"AI-first owner checkpoint is not a regular file: {artifact_name}",
                exit_code=2,
            )
    if checkpoint_dir is not None:
        try:
            checkpoint_dir.rmdir()
        except OSError:
            pass
        try:
            checkpoint_dir.parent.rmdir()
        except OSError:
            pass
    return retired

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

def load_task_runtime_identity(
    task_dir: Path,
    config: dict[str, Any],
    *,
    allow_rebuild: bool = True,
) -> dict[str, Any]:
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
    if allow_rebuild and task_mapping is None and task_mapping_error == "missing":
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

    ledger_path = issue_scope_ledger_path(task_dir)
    ledger = read_json(ledger_path) if ledger_path.is_file() else {}
    primary = ledger.get("primary_issue") if isinstance(ledger.get("primary_issue"), dict) else {}
    source_repo = str(config.get("github_repo") or "").strip() or infer_github_repo(root)
    return {
        "_path": str(task_mapping_path),
        "_identity_source": "task_json_runtime_mapping",
        "schema_version": "runtime-1.0",
        "source_issue": copy.deepcopy(primary),
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
        "issue_scope_ledger_seed": {},
        "issue_scope_ledger": ledger,
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

def plan_only_archived_task_candidate(root: Path, candidate: Path) -> Path | None:
    root_lexical = closeout_lexical_path(root)
    target = reject_closeout_symlink_components(
        root_lexical,
        candidate,
        "archived plan-only task locator",
    )
    archive_root = root_lexical / ".trellis/tasks/archive"
    try:
        relative = target.relative_to(archive_root)
    except ValueError as exc:
        raise WorkflowError(
            "finish-work archived plan-only task locator must stay under the current repository archive root.",
            exit_code=2,
            payload={"path": str(candidate), "archive_root": str(archive_root)},
        ) from exc
    if len(relative.parts) != 2 or not re.fullmatch(r"\d{4}-\d{2}", relative.parts[0]):
        raise WorkflowError(
            "finish-work archived plan-only task locator must be an exact archive month/task path.",
            exit_code=2,
            payload={"path": str(candidate)},
        )
    try:
        task_mode = os.lstat(target).st_mode
        plan_mode = os.lstat(target / CLOSEOUT_PLAN_ARTIFACT).st_mode
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise WorkflowError(
            "finish-work could not inspect the archived plan-only task locator.",
            exit_code=2,
            payload={"path": str(candidate)},
        ) from exc
    if not stat.S_ISDIR(task_mode) or not stat.S_ISREG(plan_mode):
        raise WorkflowError(
            "finish-work archived plan-only locator must be a real directory with a regular closeout plan file.",
            exit_code=2,
            payload={"path": str(candidate)},
        )
    return target

def ordinary_task_dir_candidate_matches(candidate: Path) -> bool:
    return candidate.is_dir() and (candidate / "task.json").is_file()

def preflight_finish_work_ordinary_candidate(
    root: Path,
    candidate: Path,
    label: str,
) -> bool:
    symlink_error: WorkflowError | None = None
    # Capture raw alias evidence before using the ordinary resolver's
    # follow-symlink predicates to decide whether this candidate matches.
    try:
        reject_closeout_symlink_components(root, candidate, label)
    except WorkflowError as exc:
        if not exc.payload.get("symlink_component"):
            raise
        symlink_error = exc
    if not ordinary_task_dir_candidate_matches(candidate):
        return False
    if symlink_error is not None:
        raise symlink_error
    return True

def preflight_finish_work_basename_candidates(root: Path, basename: str) -> None:
    label = "task basename candidate"
    direct_candidates = [root / basename, tasks_root(root) / basename]
    for candidate in direct_candidates:
        if preflight_finish_work_ordinary_candidate(root, candidate, label):
            return

    archive_root = tasks_root(root) / "archive"
    reject_closeout_symlink_components(root, archive_root, label)
    if not archive_root.is_dir():
        return
    for month in sorted(archive_root.iterdir(), reverse=True):
        candidate = month / basename
        if preflight_finish_work_ordinary_candidate(root, candidate, label):
            return

def resolve_finish_work_task_dir(root: Path, task_arg: str | None) -> Path:
    if not task_arg:
        return resolve_task_dir(root, task_arg)

    root_lexical = closeout_lexical_path(root)
    raw = Path(task_arg).expanduser()
    basename = raw.name.rstrip("/")
    exact_plan_only_candidate: Path | None = None
    if len(raw.parts) == 1 and basename not in {"", ".", ".."}:
        preflight_finish_work_basename_candidates(root_lexical, basename)
        lookup_by_basename = True
    else:
        if raw.is_absolute():
            candidate = raw
        elif raw.parts and raw.parts[0] == "archive":
            candidate = tasks_root(root_lexical) / raw
        else:
            candidate = root_lexical / raw
        target = reject_closeout_symlink_components(
            root_lexical,
            candidate,
            "archived plan-only task locator",
        )
        try:
            relative = target.relative_to(root_lexical)
        except ValueError as exc:
            raise WorkflowError(
                "finish-work archived plan-only task locator must stay inside the current repository.",
                exit_code=2,
                payload={"path": str(task_arg)},
            ) from exc
        if (
            len(relative.parts) == 3
            and relative.parts[:2] == (".trellis", "tasks")
        ):
            lookup_by_basename = True
        elif relative.parts[:3] == (".trellis", "tasks", "archive"):
            archive_relative = relative.parts[3:]
            if (
                len(archive_relative) != 2
                or not re.fullmatch(r"\d{4}-\d{2}", archive_relative[0])
            ):
                raise WorkflowError(
                    "finish-work archived plan-only task locator must be an exact archive month/task path.",
                    exit_code=2,
                    payload={"path": str(task_arg)},
                )
            exact_plan_only_candidate = target
            lookup_by_basename = False
        else:
            raise WorkflowError(
                "finish-work plan-only task locator must be a task basename, exact active locator, or exact archive locator.",
                exit_code=2,
                payload={"path": str(task_arg)},
            )

    normal = resolve_existing_task_dir(root, task_arg)
    if normal is not None:
        return normal

    transaction_task_ref = f".trellis/tasks/{basename}"
    transaction_match = finalization_find_transaction_by_task_ref(
        root_lexical,
        transaction_task_ref,
    )
    if transaction_match is not None:
        archive_root = tasks_root(root_lexical) / "archive"
        archived_matches = [
            month / basename
            for month in sorted(archive_root.iterdir(), reverse=True)
            if archive_root.is_dir()
            and re.fullmatch(r"\d{4}-\d{2}", month.name)
            and (month / basename).is_dir()
            and not (month / basename).is_symlink()
        ] if archive_root.is_dir() else []
        if len(archived_matches) != 1:
            raise WorkflowError(
                "finish-work transaction recovery requires one exact archived task.",
                exit_code=2,
                payload={
                    "task_ref": transaction_task_ref,
                    "candidates": [
                        repo_relative(root_lexical, candidate)
                        for candidate in archived_matches
                    ],
                },
            )
        return archived_matches[0]

    if exact_plan_only_candidate is not None:
        archived = plan_only_archived_task_candidate(
            root_lexical,
            exact_plan_only_candidate,
        )
        if archived is not None:
            return archived

    if lookup_by_basename:
        archive_root = tasks_root(root_lexical) / "archive"
        plan_only_matches: list[Path] = []
        if archive_root.is_dir():
            for month in sorted(archive_root.iterdir(), reverse=True):
                if not re.fullmatch(r"\d{4}-\d{2}", month.name):
                    continue
                archived = plan_only_archived_task_candidate(
                    root_lexical,
                    month / basename,
                )
                if archived is not None:
                    plan_only_matches.append(archived)
        if len(plan_only_matches) > 1:
            raise WorkflowError(
                "finish-work found multiple archived plan-only tasks with the same basename; pass an exact archive locator.",
                exit_code=2,
                payload={
                    "task": basename,
                    "candidates": [
                        repo_relative(root_lexical, candidate)
                        for candidate in plan_only_matches
                    ],
                },
            )
        if plan_only_matches:
            return plan_only_matches[0]
    raise WorkflowError(f"Could not resolve task directory: {task_arg}")

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

def issue_scope_ledger_path(task_dir: Path) -> Path:
    return task_dir / "issue-scope-ledger.json"

def issue_scope_ledger_errors(ledger: Any) -> list[str]:
    if not isinstance(ledger, dict):
        return ["issue_scope_ledger_root_invalid"]
    expected_keys = {
        "schema_version",
        "primary_issue",
        "close_issues",
        "related_issues",
        "followup_issues",
    }
    errors: list[str] = []
    if set(ledger) != expected_keys:
        errors.append("issue_scope_ledger_fields_invalid")
    if ledger.get("schema_version") != "2.0":
        errors.append("issue_scope_ledger_schema_version_invalid")

    entry_keys = {"number", "url", "title", "reason"}
    entries_by_bucket: dict[str, list[dict[str, Any]]] = {}
    for key in ("close_issues", "related_issues", "followup_issues"):
        values = ledger.get(key)
        if not isinstance(values, list):
            errors.append(f"issue_scope_ledger_{key}_invalid")
            entries_by_bucket[key] = []
            continue
        entries_by_bucket[key] = [item for item in values if isinstance(item, dict)]
        if len(entries_by_bucket[key]) != len(values):
            errors.append(f"issue_scope_ledger_{key}_entry_invalid")

    primary = ledger.get("primary_issue")
    candidates: list[tuple[str, Any]] = [("primary_issue", primary)]
    candidates.extend(
        (key, item)
        for key, values in entries_by_bucket.items()
        for item in values
    )
    for bucket, item in candidates:
        if not isinstance(item, dict) or set(item) != entry_keys:
            errors.append(f"issue_scope_ledger_{bucket}_entry_fields_invalid")
            continue
        number = item.get("number")
        if not is_strict_int(number) or number <= 0:
            errors.append(f"issue_scope_ledger_{bucket}_number_invalid")
        if not all(
            isinstance(item.get(key), str) and str(item.get(key)).strip()
            for key in ("url", "title", "reason")
        ):
            errors.append(f"issue_scope_ledger_{bucket}_entry_text_invalid")

    seen: dict[int, str] = {}
    for bucket, values in entries_by_bucket.items():
        local: set[int] = set()
        for item in values:
            number = item.get("number")
            if not is_strict_int(number):
                continue
            if number in local or number in seen:
                errors.append("issue_scope_ledger_issue_disposition_not_unique")
            local.add(number)
            seen[number] = bucket
    if isinstance(primary, dict) and is_strict_int(primary.get("number")):
        number = int(primary["number"])
        matches = [
            item
            for values in entries_by_bucket.values()
            for item in values
            if item.get("number") == number
        ]
        if len(matches) != 1 or matches[0] != primary:
            errors.append("issue_scope_ledger_primary_disposition_invalid")
    return context_sort(errors)

def load_issue_scope_ledger(task_dir: Path, task_context: dict[str, Any]) -> dict[str, Any]:
    del task_context
    path = issue_scope_ledger_path(task_dir)
    if path.is_symlink() or not path.is_file():
        raise WorkflowError(
            "Current Issue Scope Ledger 2.0 is missing.",
            exit_code=2,
        )
    ledger = read_json(path)
    errors = issue_scope_ledger_errors(ledger)
    if errors:
        raise WorkflowError(
            "Issue Scope Ledger is invalid.",
            exit_code=2,
            payload={"error_codes": errors},
        )
    return ledger

def issue_numbers(items: Any) -> list[int]:
    numbers: list[int] = []
    if not isinstance(items, list):
        return numbers
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            numbers.append(int(item.get("number")))
        except (TypeError, ValueError):
            continue
    return numbers

def validate_ledger_for_publish(
    ledger: dict[str, Any],
) -> list[str]:
    errors: list[str] = issue_scope_ledger_errors(ledger)
    close_issues = ledger.get("close_issues")
    if not isinstance(close_issues, list):
        errors.append("issue-scope-ledger.json 缺少 close_issues 数组。")
        close_issues = []
    related_numbers = set(issue_numbers(ledger.get("related_issues")))
    followup_numbers = set(issue_numbers(ledger.get("followup_issues")))
    for issue in close_issues:
        if not isinstance(issue, dict):
            errors.append("close_issues 中存在非对象条目。")
            continue
        try:
            number = int(issue.get("number"))
        except (TypeError, ValueError):
            errors.append("close_issues 中存在缺少 number 的条目。")
            continue
        if number in related_numbers or number in followup_numbers:
            errors.append(f"issue #{number} 同时出现在 close_issues 与 related/followup 中。")
    return context_sort(errors)

def publish_config(config: dict[str, Any]) -> dict[str, Any]:
    value = config.get("publish")
    return value if isinstance(value, dict) else dict(DEFAULTS["publish"])

def validate_finish_work_invocation(args: argparse.Namespace) -> None:
    if getattr(args, "from_guru_finalizer", False):
        return
    raise WorkflowError(
        "finish-work is an internal closeout helper. Re-enter the explicit "
        "`guru-finish-work` entry so it can route current publication readiness "
        "to `guru-finalize-task`; do not invoke this helper directly.",
        exit_code=2,
        payload={
            "blocked_step": "finish-work",
            "required_entrypoint": "guru-finish-work",
        },
    )

def is_strict_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)

def task_dir_is_archived(root: Path, task_dir: Path) -> bool:
    try:
        task_dir.resolve().relative_to((tasks_root(root) / "archive").resolve())
        return True
    except ValueError:
        return False

def repo_relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)

def finalizer_unreviewed_dirty_paths(
    root: Path,
    task_dir: Path,
    *,
    allow_publication_issue_scope_ledger: bool = False,
) -> list[str]:
    del task_dir, allow_publication_issue_scope_ledger
    return [
        path
        for path in git_status_paths(root, fail_closed=True)
        if not reviewed_content_metadata_path(path)
    ]

def review_branch_content_continuity_errors(
    root: Path,
    task_dir: Path,
    review_commit: str,
    reviewed_content_sha256: str,
    current: str | None = None,
) -> list[str]:
    del task_dir
    current_head_value = current or current_head(root)
    if not re.fullmatch(r"[0-9a-f]{40}", review_commit):
        return ["Branch Review review_commit is invalid."]
    if not re.fullmatch(r"[0-9a-f]{64}", reviewed_content_sha256):
        return ["Branch Review reviewed_content_sha256 is invalid."]
    if not is_ancestor(root, review_commit, current_head_value):
        return [
            "Branch Review review_commit is not an ancestor of the current HEAD."
        ]
    try:
        anchor_identity = reviewed_content_identity(
            root,
            review_commit,
            include_worktree=False,
        )["sha256"]
        current_identity = reviewed_content_identity(
            root,
            current_head_value,
            include_worktree=True,
        )["sha256"]
    except WorkflowError:
        return ["Branch Review could not calculate reviewed-content continuity."]
    if anchor_identity != reviewed_content_sha256:
        return ["Branch Review gate identity does not match review_commit."]
    if current_identity != reviewed_content_sha256:
        return [BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX + "identity mismatch"]
    return []

def base_branch_from_sources(args: argparse.Namespace, task: dict[str, Any], task_context: dict[str, Any]) -> str:
    for value in [
        getattr(args, "base_branch", None),
        task_context.get("base_branch"),
        task.get("base_branch"),
    ]:
        if value:
            return str(value)
    raise WorkflowError("Could not resolve base_branch from args, task runtime identity, or task.json.")

def markdown_section_ranges(body: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^(#{2,6})\s+(.+?)\s*$", body))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[title] = body[start:end].strip()
    return sections

def find_pr_body_sections(body: str) -> dict[str, str]:
    raw_sections = markdown_section_ranges(body)
    found: dict[str, str] = {}
    for required, aliases in PR_BODY_SECTION_ALIASES.items():
        for title, content in raw_sections.items():
            normalized_title = re.sub(r"\s+", " ", title).strip()
            if any(alias.lower() in normalized_title.lower() for alias in aliases):
                found[required] = content
                break
    return found

def normalized_body_line(line: str) -> str:
    return line.strip().lstrip("-*•").strip()

def section_has_specific_bullet(section: str) -> bool:
    for line in section.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("-") or stripped.startswith("*") or stripped.startswith("•")):
            continue
        normalized = normalized_body_line(stripped).lower()
        if normalized in PR_BODY_PLACEHOLDER_VALUES:
            continue
        if "详见" in normalized:
            continue
        if len(normalized) < 8:
            continue
        return True
    return False

def section_has_substantive_text(section: str) -> bool:
    lines = [normalized_body_line(line) for line in section.splitlines()]
    meaningful = [line for line in lines if line and line.lower() not in PR_BODY_PLACEHOLDER_VALUES]
    if not meaningful:
        return False
    return any("详见" not in line for line in meaningful)

def missing_docs_ssot_keys(section: str) -> list[str]:
    lowered = section.lower()
    missing: list[str] = []
    for key, aliases in PR_BODY_DOCS_SSOT_KEY_ALIASES.items():
        if not any(alias.lower() in lowered for alias in aliases):
            missing.append(key)
    return missing

def issue_number_set(items: Any) -> set[int]:
    return set(issue_numbers(items))

def close_keyword_pattern() -> re.Pattern[str]:
    return re.compile(r"(?i)\b(" + "|".join(re.escape(keyword) for keyword in PR_CLOSE_KEYWORDS) + r")\s+#(\d+)\b")

def format_metadata_commit_subject(primary_issue: int, action: str = "固化任务收尾元数据") -> str:
    return f"chore(trellis): #{int(primary_issue)} {action.strip()}"

def primary_issue_number_from_ledger(ledger: dict[str, Any]) -> int:
    primary = ledger.get("primary_issue")
    if isinstance(primary, dict):
        try:
            return int(primary.get("number"))
        except (TypeError, ValueError):
            pass
    close_issues = ledger.get("close_issues")
    if isinstance(close_issues, list):
        for issue in close_issues:
            if not isinstance(issue, dict):
                continue
            try:
                return int(issue.get("number"))
            except (TypeError, ValueError):
                continue
    raise WorkflowError("Could not resolve primary issue from issue-scope-ledger.json.", exit_code=2)

def parse_pull_request_number(value: str) -> int | None:
    match = re.search(r"/pull/(\d+)(?:\b|$)", value.strip())
    if match:
        return int(match.group(1))
    match = re.search(r"#(\d+)\b", value.strip())
    if match:
        return int(match.group(1))
    return None

def canonical_json_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def closeout_lexical_path(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))

def reanchor_darwin_system_repo_alias(boundary: Path, target: Path) -> Path | None:
    if sys.platform != "darwin":
        return None
    alias_prefix = Path("/var")
    canonical_prefix = Path("/private/var")
    try:
        alias_mode = os.lstat(alias_prefix).st_mode
        alias_target = Path(os.readlink(alias_prefix))
    except OSError:
        return None
    if not stat.S_ISLNK(alias_mode):
        return None
    if not alias_target.is_absolute():
        alias_target = alias_prefix.parent / alias_target
    if closeout_lexical_path(alias_target) != canonical_prefix:
        return None

    prefix_pairs = [
        (canonical_prefix, alias_prefix),
        (alias_prefix, canonical_prefix),
    ]
    for boundary_prefix, target_prefix in prefix_pairs:
        try:
            repo_suffix = boundary.relative_to(boundary_prefix)
            alias_repo_root = target_prefix / repo_suffix
            path_suffix = target.relative_to(alias_repo_root)
        except ValueError:
            continue
        return boundary / path_suffix
    return None

def reject_closeout_symlink_components(root: Path, path: Path, label: str) -> Path:
    boundary = closeout_lexical_path(root)
    target = closeout_lexical_path(path)
    try:
        relative = target.relative_to(boundary)
    except ValueError:
        mapped = reanchor_darwin_system_repo_alias(boundary, target)
        if mapped is None:
            raise WorkflowError(
                f"finish-work {label} must stay inside the repository root.",
                exit_code=2,
                payload={"path": str(path)},
            )
        target = mapped
        relative = target.relative_to(boundary)

    components = [boundary]
    current = boundary
    for part in relative.parts:
        current = current / part
        components.append(current)
    for component in components:
        try:
            mode = os.lstat(component).st_mode
        except FileNotFoundError:
            break
        except OSError as exc:
            raise WorkflowError(
                f"finish-work could not inspect {label} path components.",
                exit_code=2,
                payload={"path": str(path), "component": str(component)},
            ) from exc
        if stat.S_ISLNK(mode):
            component_label = "." if component == boundary else component.relative_to(boundary).as_posix()
            raise WorkflowError(
                f"finish-work {label} path must not contain symbolic-link components.",
                exit_code=2,
                payload={"path": str(path), "symlink_component": component_label},
            )
    return target

def validate_pr_body_quality(body: str, ledger: dict[str, Any], draft: bool) -> list[str]:
    errors: list[str] = []
    sections = find_pr_body_sections(body)
    for section in PR_BODY_REQUIRED_SECTIONS:
        if section not in sections:
            errors.append(f"PR body 缺少 `{section}` section。")

    if not draft:
        for phrase in PR_BODY_LOW_INFORMATION_PHRASES:
            if phrase in body:
                errors.append(f"PR body 包含低信息量摘要或占位短语：{phrase}")

    summary = sections.get("变更摘要", "")
    if summary and not section_has_specific_bullet(summary):
        errors.append("PR body `变更摘要` 缺少具体 bullet。")
    for section in ["影响范围", "验证结果", "安全说明"]:
        value = sections.get(section, "")
        if value and not section_has_substantive_text(value):
            errors.append(f"PR body `{section}` 缺少具体内容。")
    docs_ssot = sections.get("Docs SSOT", "")
    if docs_ssot:
        missing = missing_docs_ssot_keys(docs_ssot)
        if missing:
            errors.append("PR body `Docs SSOT` section 缺少客观键：{}。".format(", ".join(missing)))

    close_allowed = issue_number_set(ledger.get("close_issues"))
    related_numbers = issue_number_set(ledger.get("related_issues"))
    followup_numbers = issue_number_set(ledger.get("followup_issues"))
    for match in close_keyword_pattern().finditer(body):
        number = int(match.group(2))
        if number not in close_allowed:
            errors.append(f"PR body 对非 close_issues issue #{number} 使用了 close keyword。")
        if number in related_numbers or number in followup_numbers:
            errors.append(f"PR body 对 related/followup issue #{number} 使用了 close keyword。")
    return errors

def task_publication_repository_binding(
    root: Path,
    task_dir: Path,
) -> dict[str, Any]:
    task = task_json(task_dir)
    base_branch = str(task.get("base_branch") or "")
    base_ref = diff_base_ref(root, base_branch) if base_branch else ""
    diff_process = run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        cwd=root,
        check=False,
    )
    if diff_process.returncode != 0:
        raise WorkflowError(
            "Task publication review could not rebuild the current diff.",
            exit_code=2,
        )
    readiness_relative = repo_relative(root, task_dir / PR_READINESS_ARTIFACT)
    return {
        "head": current_head(root),
        "branch": current_branch(root),
        "base_ref": base_ref,
        "diff_paths": sorted(
            line.strip()
            for line in diff_process.stdout.splitlines()
            if line.strip()
        ),
        "status_paths": sorted(
            path
            for path in git_status_paths(root, fail_closed=True)
            if path != readiness_relative
        ),
    }

def task_publication_unexpected_status_paths(
    status_paths: list[str],
) -> list[str]:
    return sorted(
        path for path in status_paths if not reviewed_content_metadata_path(path)
    )

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

def closeout_reviewed_change_facts(
    root: Path,
    task_context: dict[str, Any],
    branch_review_commit: str,
) -> dict[str, Any]:
    """Rebuild one reviewed-path fact set for closeout and its projections."""
    base_head = str(task_context.get("base_head_sha") or "").strip()
    if re.fullmatch(r"[0-9a-f]{40}", base_head) is None:
        raise WorkflowError(
            "Closeout reviewed paths require the pinned task base commit.",
            exit_code=2,
        )
    proc = run(
        ["git", "diff", "--name-only", f"{base_head}...{branch_review_commit}"],
        cwd=root,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Could not rebuild closeout reviewed paths from the pinned task base.",
            exit_code=2,
            payload={
                "base_head": base_head,
                "branch_review_commit": branch_review_commit,
                "stderr": proc.stderr.strip(),
            },
        )
    changed_paths = sorted(
        {
            path.strip()
            for path in proc.stdout.splitlines()
            if path.strip()
        }
    )
    return {"changed_paths": changed_paths}

def provenance_tail_flatten_manifest(value: Any, prefix: str = "") -> dict[str, Any]:
    """Return deterministic dotted paths for the manifest field-diff contract."""
    if isinstance(value, dict):
        flattened: dict[str, Any] = (
            {prefix: PROVENANCE_TAIL_OBJECT_PRESENCE}
            if prefix
            else {}
        )
        for key in sorted(value):
            child = f"{prefix}.{key}" if prefix else str(key)
            flattened.update(provenance_tail_flatten_manifest(value[key], child))
        return flattened
    return {prefix: value}

def provenance_tail_manifest_field_diff(
    before: Any,
    after: Any,
) -> list[str]:
    before_flat = provenance_tail_flatten_manifest(before)
    after_flat = provenance_tail_flatten_manifest(after)
    return sorted(
        [
            path
            for path in set(before_flat) | set(after_flat)
            if (
                path not in before_flat
                or path not in after_flat
                or before_flat[path] != after_flat[path]
            )
        ],
        key=lambda item: item.encode("utf-8"),
    )

def provenance_tail_safe_file_action_transition(
    before: Any,
    after: Any,
    container: str,
) -> bool:
    """Accept only an ordered installed-to-unchanged files transition."""
    if container not in PROVENANCE_TAIL_FILE_ACTION_CONTAINERS:
        return False
    if not isinstance(before, dict) or not isinstance(after, dict):
        return False
    section_name, field_name = container.split(".", 1)
    before_section = before.get(section_name)
    after_section = after.get(section_name)
    if not isinstance(before_section, dict) or not isinstance(after_section, dict):
        return False
    before_files = before_section.get(field_name)
    after_files = after_section.get(field_name)
    if not isinstance(before_files, list) or not isinstance(after_files, list):
        return False
    if len(before_files) != len(after_files):
        return False
    for before_item, after_item in zip(before_files, after_files):
        if not isinstance(before_item, dict) or not isinstance(after_item, dict):
            return False
        if before_item.get("action") != "installed":
            return False
        if after_item.get("action") != "unchanged":
            return False
        before_identity = dict(before_item)
        after_identity = dict(after_item)
        before_identity.pop("action", None)
        after_identity.pop("action", None)
        try:
            before_bytes = json.dumps(
                before_identity,
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            after_bytes = json.dumps(
                after_identity,
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        except (TypeError, ValueError):
            return False
        if before_bytes != after_bytes:
            return False
    return True

def provenance_canonical_github_locator(repo_ref: str) -> str:
    """Return the one credential-free GitHub locator accepted for source fetch."""
    normalized = normalize_github_repository(repo_ref)
    if not normalized:
        return ""
    return f"https://github.com/{normalized}.git"

def provenance_source_binding_errors(
    manifest: Any,
    target_repo: Any,
    reviewed_content_head: str,
) -> tuple[dict[str, str] | None, list[str]]:
    """Resolve the closed self-hosted/installed extension source identity."""
    errors: list[str] = []
    target_repo_ref = normalize_github_repository(target_repo)
    if not target_repo_ref:
        errors.append("provenance_tail_target_repo_invalid")
    if re.fullmatch(r"[0-9a-f]{40}", str(reviewed_content_head or "")) is None:
        errors.append("provenance_tail_reviewed_head_invalid")
    if not isinstance(manifest, dict):
        errors.append("provenance_tail_manifest_invalid")
        return None, sorted(set(errors))
    if manifest.get("schema_version") != "2.0":
        errors.append("provenance_tail_manifest_schema_mismatch")
    extension = manifest.get("extension")
    if not isinstance(extension, dict) or extension.get("extension_id") != "guru-team":
        errors.append("provenance_tail_extension_identity_mismatch")
    source = manifest.get("source")
    if not isinstance(source, dict):
        errors.append("provenance_tail_source_missing")
        return None, sorted(set(errors))

    source_locator = source.get("repo")
    source_repo_ref = parse_github_remote_repository_url(source_locator)
    canonical_locator = provenance_canonical_github_locator(source_repo_ref)
    if (
        not isinstance(source_locator, str)
        or not source_repo_ref
        or source_locator != canonical_locator
    ):
        errors.append("provenance_tail_source_repo_invalid")
    source_ref = source.get("ref")
    source_commit = source.get("commit")
    if re.fullmatch(r"[0-9a-f]{40}", str(source_ref or "")) is None:
        errors.append("provenance_tail_source_ref_invalid")
    if re.fullmatch(r"[0-9a-f]{40}", str(source_commit or "")) is None:
        errors.append("provenance_tail_source_commit_invalid")
    if source_ref != source_commit:
        errors.append("provenance_tail_source_ref_commit_mismatch")
    tree_state = source.get("tree_state")
    mutable_ref = source.get("is_mutable_ref")
    if tree_state not in {"clean", "dirty"}:
        errors.append("provenance_tail_source_tree_state_invalid")
    if not isinstance(mutable_ref, bool):
        errors.append("provenance_tail_source_ref_mutability_invalid")
    if errors:
        return None, sorted(set(errors))

    mode = "self_hosted" if source_repo_ref == target_repo_ref else "installed"
    if mode == "installed" and tree_state != "clean":
        errors.append("provenance_tail_source_not_clean")
    if mode == "installed" and mutable_ref is not False:
        errors.append("provenance_tail_source_ref_mutable")
    if errors:
        return None, sorted(set(errors))
    bound_commit = (
        reviewed_content_head if mode == "self_hosted" else str(source_commit)
    )
    return {
        "mode": mode,
        "target_repo": target_repo_ref,
        "target_reviewed_head": reviewed_content_head,
        "source_repo": source_repo_ref,
        "source_locator": canonical_locator,
        "source_ref": bound_commit,
        "source_commit": bound_commit,
    }, []

def provenance_source_binding(
    manifest: Any,
    target_repo: Any,
    reviewed_content_head: str,
) -> dict[str, str]:
    binding, errors = provenance_source_binding_errors(
        manifest,
        target_repo,
        reviewed_content_head,
    )
    if binding is None or errors:
        raise WorkflowError(
            "Installed extension source provenance is invalid for Finalizer preparation.",
            exit_code=2,
            payload={
                "reason_code": "provenance_source_binding_invalid",
                "errors": errors,
            },
        )
    return binding

def provenance_apply_platform_args(manifest: Any) -> list[str]:
    """Project one reviewed installed platform identity into preset apply argv."""
    errors: list[str] = []
    selected_by_locator: dict[str, list[str]] = {}
    for object_name in ("install", "skill_packages", "overlays"):
        container = manifest.get(object_name) if isinstance(manifest, dict) else None
        if not isinstance(container, dict):
            errors.append(f"provenance_platform_selection_{object_name}_missing")
            continue
        selected = container.get("selected_platforms")
        if not isinstance(selected, list):
            errors.append(
                f"provenance_platform_selection_{object_name}_type_invalid"
            )
            continue
        if not selected:
            errors.append(f"provenance_platform_selection_{object_name}_empty")
            continue
        if any(not isinstance(platform, str) for platform in selected):
            errors.append(
                f"provenance_platform_selection_{object_name}_member_invalid"
            )
            continue
        if len(selected) != len(set(selected)):
            errors.append(
                f"provenance_platform_selection_{object_name}_duplicate"
            )
        if selected != sorted(selected):
            errors.append(
                f"provenance_platform_selection_{object_name}_not_sorted"
            )
        if any(platform not in PROVENANCE_APPLY_PLATFORMS for platform in selected):
            errors.append(
                f"provenance_platform_selection_{object_name}_unknown"
            )
        selected_by_locator[object_name] = selected

    if len(selected_by_locator) == 3:
        selections = list(selected_by_locator.values())
        if selections[1:] != selections[:-1]:
            errors.append("provenance_platform_selection_mismatch")

    install = manifest.get("install") if isinstance(manifest, dict) else None
    all_platforms = install.get("all_platforms") if isinstance(install, dict) else None
    if not isinstance(all_platforms, bool):
        errors.append("provenance_platform_selection_all_platforms_invalid")
    elif "install" in selected_by_locator:
        full_selection = selected_by_locator["install"] == list(
            PROVENANCE_APPLY_PLATFORMS
        )
        if all_platforms and not full_selection:
            errors.append("provenance_platform_selection_all_platforms_mismatch")

    if errors:
        raise WorkflowError(
            "Installed platform selection is invalid for Finalizer preparation.",
            exit_code=2,
            payload={
                "reason_code": "provenance_platform_selection_invalid",
                "errors": sorted(set(errors)),
            },
        )

    selected = selected_by_locator["install"]
    if all_platforms:
        return ["--all-platforms"]
    return [item for platform in selected for item in ("--platform", platform)]

def provenance_tail_manifest_errors(
    before: Any,
    after: Any,
    reviewed_content_head: str,
    target_repo: Any,
) -> list[str]:
    """Validate the only manifest mutation allowed after reviewed content."""
    errors: list[str] = []
    if not isinstance(before, dict) or not isinstance(after, dict):
        return ["provenance_tail_manifest_invalid"]
    binding, binding_errors = provenance_source_binding_errors(
        before,
        target_repo,
        reviewed_content_head,
    )
    errors.extend(binding_errors)
    changed = provenance_tail_manifest_field_diff(before, after)
    unexpected = set(changed) - PROVENANCE_TAIL_ALLOWED_FIELDS
    for container in PROVENANCE_TAIL_FILE_ACTION_CONTAINERS:
        if (
            container in unexpected
            and provenance_tail_safe_file_action_transition(
                before,
                after,
                container,
            )
        ):
            unexpected.remove(container)
    unexpected = sorted(unexpected, key=lambda item: item.encode("utf-8"))
    if unexpected:
        errors.append("provenance_tail_manifest_fields_outside_allowlist")
    source = after.get("source")
    if not isinstance(source, dict):
        errors.append("provenance_tail_source_missing")
    elif binding is not None:
        if source.get("repo") != binding["source_locator"]:
            errors.append("provenance_tail_source_repo_mismatch")
        if source.get("ref") != binding["source_ref"]:
            errors.append("provenance_tail_source_ref_mismatch")
        if source.get("commit") != binding["source_commit"]:
            errors.append("provenance_tail_source_commit_mismatch")
        if source.get("tree_state") != "clean":
            errors.append("provenance_tail_source_not_clean")
        if source.get("is_mutable_ref") is not False:
            errors.append("provenance_tail_source_ref_mutable")
    if "installed_at" in after and not isinstance(after["installed_at"], str):
        errors.append("provenance_tail_installed_at_invalid")
    return sorted(set(errors))

def provenance_tail_git_status_paths(root: Path) -> list[str]:
    proc = run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=root,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Could not inspect provenance metadata-tail checkout status.",
            exit_code=2,
        )
    paths: list[str] = []
    for record in proc.stdout.split("\0"):
        if not record:
            continue
        path = record[3:] if len(record) >= 3 else ""
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[-1]
        if path:
            paths.append(path)
    return sorted(set(paths), key=lambda item: item.encode("utf-8"))

def read_json_from_git(root: Path, revision_path: str) -> Any:
    proc = run(["git", "show", revision_path], cwd=root, check=False)
    if proc.returncode != 0:
        raise WorkflowError(
            "Could not read the provenance manifest from the reviewed Git commit.",
            exit_code=2,
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise WorkflowError(
            "The provenance manifest in the reviewed Git commit is invalid JSON.",
            exit_code=2,
        ) from exc

def provenance_tail_checkout_errors(
    root: Path,
    reviewed_content_head: str,
) -> list[str]:
    """Check one detached clean target checkout before apply or commit."""
    errors: list[str] = []
    try:
        head = current_head(root)
    except WorkflowError:
        head = ""
    if head != reviewed_content_head:
        errors.append("provenance_tail_checkout_head_mismatch")
    branch = current_branch(root)
    if branch != "HEAD":
        errors.append("provenance_tail_checkout_not_detached")
    if provenance_tail_git_status_paths(root):
        errors.append("provenance_tail_checkout_not_clean")
    return sorted(set(errors))

def provenance_extension_source_checkout_errors(
    root: Path,
    binding: dict[str, str],
) -> list[str]:
    """Validate extension source identity independently from the target checkout."""
    errors: list[str] = []
    try:
        head = current_head(root)
    except WorkflowError:
        head = ""
    if head != binding["source_commit"]:
        errors.append("provenance_tail_extension_source_head_mismatch")
    if current_branch(root) != "HEAD":
        errors.append("provenance_tail_extension_source_not_detached")
    if provenance_tail_git_status_paths(root):
        errors.append("provenance_tail_extension_source_not_clean")
    origin = run(
        ["git", "remote", "get-url", "--all", "origin"],
        cwd=root,
        check=False,
    )
    urls = origin.stdout.splitlines() if origin.returncode == 0 else []
    if (
        not urls
        or any(
            parse_github_remote_repository_url(value) != binding["source_repo"]
            for value in urls
        )
    ):
        errors.append("provenance_tail_extension_source_repo_mismatch")
    if binding["mode"] == "installed" and urls != [binding["source_locator"]]:
        errors.append("provenance_tail_extension_source_origin_not_canonical")
    return sorted(set(errors))

def provenance_tail_manifest_postimage(
    parent: dict[str, Any],
    binding: dict[str, str],
) -> dict[str, Any]:
    """Build the Finalizer-only provenance tail without reinstalling the preset."""
    postimage = copy.deepcopy(parent)
    source = postimage.get("source")
    if not isinstance(source, dict):
        raise WorkflowError(
            "Provenance tail manifest source is missing.",
            exit_code=2,
            payload={"reason_code": "provenance_tail_source_missing"},
        )
    source.update(
        {
            "repo": binding["source_locator"],
            "ref": binding["source_ref"],
            "commit": binding["source_commit"],
            "tree_state": "clean",
            "is_mutable_ref": False,
        }
    )
    postimage["source"] = source
    return postimage

def prepare_provenance_extension_source_checkout(
    target_root: Path,
    source_root: Path,
    binding: dict[str, str],
) -> None:
    """Create the package-local detached source checkout for one binding mode."""
    if binding["mode"] == "self_hosted":
        proc = run(
            [
                "git",
                "worktree",
                "add",
                "--detach",
                str(source_root),
                binding["source_commit"],
            ],
            cwd=target_root,
            check=False,
        )
        if proc.returncode != 0:
            raise WorkflowError(
                "Could not create the self-hosted extension source checkout.",
                exit_code=2,
                payload={"reason_code": "provenance_source_checkout_create_failed"},
            )
    else:
        init = run(
            ["git", "init", "--quiet", str(source_root)],
            check=False,
        )
        if init.returncode != 0:
            raise WorkflowError(
                "Could not initialize the installed extension source checkout.",
                exit_code=2,
                payload={"reason_code": "provenance_source_checkout_init_failed"},
            )
        origin = run(
            ["git", "remote", "add", "origin", binding["source_locator"]],
            cwd=source_root,
            check=False,
        )
        if origin.returncode != 0:
            raise WorkflowError(
                "Could not configure the canonical extension source origin.",
                exit_code=2,
                payload={"reason_code": "provenance_source_origin_failed"},
            )
        fetch = run(
            [
                "git",
                "fetch",
                "--depth=1",
                "origin",
                binding["source_commit"],
            ],
            cwd=source_root,
            check=False,
        )
        if fetch.returncode != 0 and "not our ref" in fetch.stderr.lower():
            fetch = run(
                ["git", "fetch", "--depth=1", "origin", "HEAD"],
                cwd=source_root,
                check=False,
            )
        if fetch.returncode != 0:
            raise WorkflowError(
                "Could not fetch the immutable extension source commit.",
                exit_code=2,
                payload={"reason_code": "provenance_source_fetch_failed"},
            )
        resolved = run(
            ["git", "rev-parse", "--verify", "FETCH_HEAD^{commit}"],
            cwd=source_root,
            check=False,
        )
        if (
            resolved.returncode != 0
            or resolved.stdout.strip() != binding["source_commit"]
        ):
            raise WorkflowError(
                "Fetched extension source does not match the immutable manifest commit.",
                exit_code=2,
                payload={"reason_code": "provenance_source_fetch_mismatch"},
            )
        checkout = run(
            ["git", "checkout", "--detach", binding["source_commit"]],
            cwd=source_root,
            check=False,
        )
        if checkout.returncode != 0:
            raise WorkflowError(
                "Could not detach the immutable extension source checkout.",
                exit_code=2,
                payload={"reason_code": "provenance_source_checkout_failed"},
            )
    errors = provenance_extension_source_checkout_errors(source_root, binding)
    if errors:
        raise WorkflowError(
            "Extension source checkout failed its immutable clean-source contract.",
            exit_code=2,
            payload={"reason_code": "provenance_source_checkout_invalid", "errors": errors},
        )

def provenance_tail_commit_errors(
    root: Path,
    reviewed_content_head: str,
    publication_head: str,
    *,
    target_repo: Any,
    require_current: bool = True,
) -> list[str]:
    """Validate one committed provenance tail and its reviewed/publication identities."""
    errors: list[str] = []
    if re.fullmatch(r"[0-9a-f]{40}", str(publication_head or "")) is None:
        errors.append("provenance_tail_publication_head_invalid")
        return sorted(set(errors))
    if require_current and publication_head != current_head(root):
        errors.append("provenance_tail_publication_head_not_current")
    parent_proc = run(
        ["git", "show", "-s", "--format=%P", publication_head],
        cwd=root,
        check=False,
    )
    parents = parent_proc.stdout.split() if parent_proc.returncode == 0 else []
    if parents != [reviewed_content_head]:
        errors.append("provenance_tail_parent_mismatch")
    changed_proc = run(
        [
            "git",
            "diff-tree",
            "--root",
            "--no-commit-id",
            "--name-only",
            "--no-renames",
            "-r",
            "-z",
            publication_head,
        ],
        cwd=root,
        check=False,
    )
    changed = {
        item for item in changed_proc.stdout.split("\0") if item
    } if changed_proc.returncode == 0 else set()
    if changed != {PROVENANCE_TAIL_MANIFEST_PATH}:
        errors.append("provenance_tail_changed_paths_invalid")
    if not errors:
        before_proc = run(
            ["git", "show", f"{publication_head}^:{PROVENANCE_TAIL_MANIFEST_PATH}"],
            cwd=root,
            check=False,
        )
        after_proc = run(
            ["git", "show", f"{publication_head}:{PROVENANCE_TAIL_MANIFEST_PATH}"],
            cwd=root,
            check=False,
        )
        try:
            before = json.loads(before_proc.stdout)
            after = json.loads(after_proc.stdout)
        except (json.JSONDecodeError, TypeError):
            errors.append("provenance_tail_manifest_unreadable")
        else:
            errors.extend(
                provenance_tail_manifest_errors(
                    before,
                    after,
                    reviewed_content_head,
                    target_repo,
                )
            )
    return sorted(set(errors))

def validate_provenance_metadata_tail(
    root: Path,
    reviewed_content_head: str,
    publication_head: str,
    *,
    target_repo: Any,
) -> dict[str, Any]:
    errors = provenance_tail_commit_errors(
        root,
        reviewed_content_head,
        publication_head,
        target_repo=target_repo,
    )
    if errors:
        raise WorkflowError(
            "Provenance metadata-tail failed its clean-source contract.",
            exit_code=2,
            payload={"errors": errors},
        )
    return {
        "status": "passed",
        "reviewed_content_head": reviewed_content_head,
        "publication_head": publication_head,
        "changed_paths": [PROVENANCE_TAIL_MANIFEST_PATH],
        "changed_fields": sorted(PROVENANCE_TAIL_ALLOWED_FIELDS),
    }

def commit_provenance_metadata_tail(
    root: Path,
    reviewed_content_head: str,
    *,
    target_repo: Any,
    message: str = "chore(trellis): 更新 Guru Team provenance 元数据",
) -> dict[str, Any]:
    """Commit an already-applied manifest tail; no preset/apply is performed here."""
    if current_head(root) != reviewed_content_head:
        raise WorkflowError("Provenance tail commit requires reviewed HEAD as parent.", exit_code=2)
    dirty = provenance_tail_git_status_paths(root)
    if dirty != [PROVENANCE_TAIL_MANIFEST_PATH]:
        raise WorkflowError(
            "Provenance tail commit requires exactly one manifest-only dirty path.",
            exit_code=2,
            payload={"dirty_paths": dirty},
        )
    parent = read_json_from_git(root, f"{reviewed_content_head}:{PROVENANCE_TAIL_MANIFEST_PATH}")
    manifest = read_json(root / PROVENANCE_TAIL_MANIFEST_PATH)
    errors = provenance_tail_manifest_errors(
        parent,
        manifest,
        reviewed_content_head,
        target_repo,
    )
    if errors:
        raise WorkflowError("Provenance tail manifest is outside the allowlist.", exit_code=2, payload={"errors": errors})
    run_stdout(["git", "add", "--", PROVENANCE_TAIL_MANIFEST_PATH], cwd=root)
    run_stdout(["git", "commit", "--no-verify", "-m", message], cwd=root)
    publication_head = current_head(root)
    return validate_provenance_metadata_tail(
        root,
        reviewed_content_head,
        publication_head,
        target_repo=target_repo,
    )

def finalizer_publication_identity(
    root: Path,
    reviewed_content_head: str,
    target_repo: Any,
) -> dict[str, Any]:
    """Project the reviewed head and the optional single provenance tail."""
    if re.fullmatch(r"[0-9a-f]{40}", str(reviewed_content_head or "")) is None:
        raise WorkflowError("Finalizer reviewed_content_head is invalid.", exit_code=2)
    publication_head = current_head(root)
    if publication_head == reviewed_content_head:
        return {
            "reviewed_content_head": reviewed_content_head,
            "publication_head": publication_head,
            "metadata_tail": None,
        }
    if not is_ancestor(root, reviewed_content_head, publication_head):
        raise WorkflowError(
            "Finalizer publication head is not a descendant of reviewed content.",
            exit_code=2,
        )
    errors = provenance_tail_commit_errors(
        root,
        reviewed_content_head,
        publication_head,
        target_repo=target_repo,
    )
    if errors == ["provenance_tail_changed_paths_invalid"]:
        # Existing task/archive metadata commits are excluded from reviewed
        # content and are not provenance tails; keep their historical behavior.
        paths_proc = run(
            [
                "git", "diff-tree", "--no-commit-id", "--name-only", "--no-renames",
                "-r", "-z", publication_head,
            ],
            cwd=root,
            check=False,
        )
        paths = {item for item in paths_proc.stdout.split("\0") if item}
        if (
            paths
            and PROVENANCE_TAIL_MANIFEST_PATH not in paths
            and all(reviewed_content_metadata_path(path) for path in paths)
        ):
            return {
                "reviewed_content_head": reviewed_content_head,
                "publication_head": publication_head,
                "metadata_tail": None,
            }
    if errors:
        raise WorkflowError(
            "Finalizer publication head contains an invalid provenance tail.",
            exit_code=2,
            payload={"errors": errors},
        )
    return {
        "reviewed_content_head": reviewed_content_head,
        "publication_head": publication_head,
        "metadata_tail": {
            "commit": publication_head,
            "parent": reviewed_content_head,
            "path": PROVENANCE_TAIL_MANIFEST_PATH,
        },
    }

def finalizer_pre_pr_provenance_tail_required(
    root: Path,
    plan: dict[str, Any],
) -> bool:
    """Return whether the current pre-PR plan still carries stale provenance."""
    git = plan.get("git") if isinstance(plan.get("git"), dict) else {}
    reviewed = str(git.get("branch_review_commit") or "")
    target_repo = git.get("repo")
    if re.fullmatch(r"[0-9a-f]{40}", reviewed) is None:
        raise WorkflowError("Finalizer reviewed content identity is invalid.", exit_code=2)
    payload = read_json_from_git(
        root,
        f"{reviewed}:{PROVENANCE_TAIL_MANIFEST_PATH}",
    )
    binding = provenance_source_binding(payload, target_repo, reviewed)
    publication = finalizer_publication_identity(root, reviewed, target_repo)
    if publication["metadata_tail"] is not None:
        return False
    source = payload["source"]
    return not (
        source.get("repo") == binding["source_locator"]
        and source.get("ref") == binding["source_ref"]
        and source.get("commit") == binding["source_commit"]
        and source.get("tree_state") == "clean"
        and source.get("is_mutable_ref") is False
    )

def prepare_provenance_metadata_tail(
    root: Path,
    reviewed_content_head: str,
    target_repo: Any,
) -> dict[str, Any]:
    """Apply source-owned preset bytes to one isolated target reviewed checkout."""
    if current_head(root) != reviewed_content_head:
        raise WorkflowError(
            "Provenance tail preparation requires the reviewed content HEAD.",
            exit_code=2,
        )
    with tempfile.TemporaryDirectory(prefix="guru-provenance-source-") as tmp:
        target_reviewed_checkout = Path(tmp) / "target-reviewed"
        extension_source_checkout = Path(tmp) / "extension-source"
        run_stdout(
            [
                "git",
                "worktree",
                "add",
                "--detach",
                str(target_reviewed_checkout),
                reviewed_content_head,
            ],
            cwd=root,
        )
        binding: dict[str, str] | None = None
        try:
            pre_errors = provenance_tail_checkout_errors(
                target_reviewed_checkout,
                reviewed_content_head,
            )
            if pre_errors:
                raise WorkflowError(
                    "Provenance target checkout is not a clean reviewed checkout.",
                    exit_code=2,
                    payload={"errors": pre_errors},
                )
            parent = read_json_from_git(
                target_reviewed_checkout,
                f"{reviewed_content_head}:{PROVENANCE_TAIL_MANIFEST_PATH}",
            )
            binding = provenance_source_binding(
                parent,
                target_repo,
                reviewed_content_head,
            )
            # Keep the installed platform matrix fail-closed without invoking
            # the full preset installer or changing managed files.
            provenance_apply_platform_args(parent)
            prepare_provenance_extension_source_checkout(
                root,
                extension_source_checkout,
                binding,
            )
            source_errors = provenance_extension_source_checkout_errors(
                extension_source_checkout,
                binding,
            )
            if source_errors:
                raise WorkflowError(
                    "Provenance source checkout is not clean or canonical.",
                    exit_code=2,
                    payload={"errors": source_errors},
                )
            postimage = provenance_tail_manifest_postimage(parent, binding)
            write_json(
                target_reviewed_checkout / PROVENANCE_TAIL_MANIFEST_PATH,
                postimage,
            )
            dirty = provenance_tail_git_status_paths(target_reviewed_checkout)
            if dirty != [PROVENANCE_TAIL_MANIFEST_PATH]:
                raise WorkflowError(
                    "Provenance tail producer produced changes outside the provenance manifest.",
                    exit_code=2,
                    payload={"dirty_paths": dirty},
                )
            manifest = read_json(
                target_reviewed_checkout / PROVENANCE_TAIL_MANIFEST_PATH
            )
            errors = provenance_tail_manifest_errors(
                parent,
                manifest,
                reviewed_content_head,
                target_repo,
            )
            if errors:
                raise WorkflowError(
                    "Provenance tail producer produced invalid metadata.",
                    exit_code=2,
                    payload={"errors": errors},
                )
            result = commit_provenance_metadata_tail(
                target_reviewed_checkout,
                reviewed_content_head,
                target_repo=target_repo,
            )
            publication_head = str(result["publication_head"])
        finally:
            if binding is not None and binding["mode"] == "self_hosted":
                run(
                    [
                        "git",
                        "worktree",
                        "remove",
                        "--force",
                        str(extension_source_checkout),
                    ],
                    cwd=root,
                    check=False,
                )
            run(
                [
                    "git",
                    "worktree",
                    "remove",
                    "--force",
                    str(target_reviewed_checkout),
                ],
                cwd=root,
                check=False,
            )
    run_stdout(["git", "merge", "--ff-only", publication_head], cwd=root)
    return {
        "reviewed_content_head": reviewed_content_head,
        "publication_head": publication_head,
        "metadata_tail": {
            "commit": publication_head,
            "parent": reviewed_content_head,
            "path": PROVENANCE_TAIL_MANIFEST_PATH,
        },
    }

def finalizer_tracked_pre_pr_artifacts(root: Path, task_dir: Path) -> list[str]:
    """Return tracked plan/verification artifacts that reprepare may not retire."""
    plan = closeout_plan_path(task_dir)
    tracked_owner_state: list[str] = []
    for path in (plan,):
        relative = repo_relative(root, path)
        if run(
            ["git", "ls-files", "--error-unmatch", "--", relative],
            cwd=root,
            check=False,
        ).returncode == 0:
            tracked_owner_state.append(relative)
    return sorted(tracked_owner_state, key=lambda item: item.encode("utf-8"))

def finalizer_base_evolution_shared_preflight(
    root: Path,
    task_dir: Path,
    previous_plan: dict[str, Any],
    current_plan: dict[str, Any],
) -> dict[str, Any]:
    """Prove shared normal-path facts for one pre-PR plan supersession."""
    previous_git = previous_plan.get("git") if isinstance(previous_plan.get("git"), dict) else {}
    current_git = current_plan.get("git") if isinstance(current_plan.get("git"), dict) else {}
    task_ref = repo_relative(root, task_dir)
    previous_reviewed = str(previous_git.get("branch_review_commit") or "")
    current_reviewed = str(current_git.get("reviewed_content_head") or current_git.get("branch_review_commit") or "")
    if (
        previous_plan.get("schema_version") != CLOSEOUT_PLAN_SCHEMA_VERSION
        or previous_plan.get("task", {}).get("active_locator") != task_ref
        or current_plan.get("task", {}).get("active_locator") != task_ref
        or any(previous_git.get(key) != current_git.get(key) for key in ("repo", "remote", "base_branch", "head_branch"))
        or previous_reviewed == current_reviewed
        or not is_ancestor(root, previous_reviewed, current_reviewed)
    ):
        raise WorkflowError(
            "Persisted closeout plan is not an eligible base-evolution predecessor.",
            exit_code=2,
            payload={"reason_code": "provenance_reprepare_base_evolution_mismatch"},
        )
    if task_json(task_dir).get("status") != "in_progress":
        raise WorkflowError("Base-evolution recovery requires task status=in_progress.", exit_code=2)
    if finalizer_tracked_pre_pr_artifacts(root, task_dir):
        raise WorkflowError(
            "Finalizer will not delete tracked task artifacts during reprepare.",
            exit_code=2,
            payload={"tracked_paths": finalizer_tracked_pre_pr_artifacts(root, task_dir)},
        )
    archive_locator = str(previous_plan.get("task", {}).get("archive_locator") or "")
    if not archive_locator or (root / archive_locator).exists() or (task_dir / FINISH_SUMMARY_ARTIFACT).exists():
        raise WorkflowError(
            "Base-evolution recovery is unavailable after archive publication starts.",
            exit_code=2,
            payload={"reason_code": "provenance_reprepare_archive_started"},
        )
    branch_ref = f"refs/heads/{current_git.get('head_branch')}"
    branch_worktrees = [record for record in worktree_records(root) if record.get("branch") == branch_ref]
    current_worktrees = [record for record in branch_worktrees if Path(record.get("worktree") or "").resolve() == root.resolve()]
    parallel = sorted(str(record.get("worktree") or "") for record in branch_worktrees if record not in current_worktrees)
    if len(current_worktrees) != 1 or parallel:
        raise WorkflowError(
            "Base-evolution recovery requires one exclusive publication worktree.",
            exit_code=2,
            payload={"reason_code": "provenance_reprepare_parallel_publication_consumer", "worktrees": parallel},
        )
    existing_pr = resolve_closeout_pull_request(
        root,
        str(current_git.get("repo") or ""),
        str(current_git.get("head_branch") or ""),
        str(current_git.get("base_branch") or ""),
        str(current_git.get("remote") or "origin"),
    )
    if existing_pr is not None:
        raise WorkflowError(
            "Base-evolution recovery is unavailable after pull request creation.",
            exit_code=2,
            payload={"reason_code": "provenance_reprepare_pull_request_exists", "pull_request": existing_pr.get("number")},
        )
    remote_head = closeout_remote_branch_head(root, current_plan)
    if not remote_head or not is_ancestor(root, remote_head, current_reviewed):
        raise WorkflowError(
            "Base-evolution recovery requires a fast-forwardable remote ancestor.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_remote_not_reviewed_head",
                "reviewed_content_head": current_reviewed,
                "remote_head": remote_head,
                "fast_forwardable": False,
            },
        )
    return {
        "previous_reviewed_content_head": previous_reviewed,
        "reviewed_content_head": current_reviewed,
        "remote_head": remote_head,
    }

def finalizer_pre_pr_base_evolution_supersession_preflight(
    root: Path,
    task_dir: Path,
    previous_plan: dict[str, Any],
    current_plan: dict[str, Any],
) -> dict[str, Any]:
    """Prove that one pre-#191 owner-private plan may be superseded."""
    task_ref = repo_relative(root, task_dir)
    previous_git = previous_plan.get("git") if isinstance(previous_plan.get("git"), dict) else {}
    if set(previous_git) != {
        "repo",
        "remote",
        "base_branch",
        "head_branch",
        "branch_review_commit",
    }:
        raise WorkflowError(
            "Persisted closeout plan is not an eligible pre-#191 base-evolution predecessor.",
            exit_code=2,
            payload={"reason_code": "provenance_reprepare_base_evolution_mismatch"},
        )
    facts = finalizer_base_evolution_shared_preflight(
        root,
        task_dir,
        previous_plan,
        current_plan,
    )
    return {
        **facts,
        "supersession_kind": "legacy_pre_191",
    }

def finalizer_current_plan_base_evolution_supersession_preflight(
    root: Path,
    task_dir: Path,
    previous_plan: dict[str, Any],
    current_plan: dict[str, Any],
    *,
    allowed_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Prove that an unused current schema-3 plan may follow reviewed content."""
    previous_git = previous_plan.get("git") if isinstance(previous_plan.get("git"), dict) else {}
    current_git = current_plan.get("git") if isinstance(current_plan.get("git"), dict) else {}
    previous_reviewed = str(previous_git.get("branch_review_commit") or "")
    previous_publication = str(previous_git.get("publication_head") or "")
    current_reviewed = str(
        current_git.get("reviewed_content_head")
        or current_git.get("branch_review_commit")
        or ""
    )
    if (
        set(previous_git)
        != {
            "repo",
            "remote",
            "base_branch",
            "head_branch",
            "branch_review_commit",
            "reviewed_content_head",
            "publication_head",
        }
        or previous_git.get("reviewed_content_head") != previous_reviewed
        or re.fullmatch(r"[0-9a-f]{40}", previous_publication) is None
        or provenance_tail_commit_errors(
            root,
            previous_reviewed,
            previous_publication,
            target_repo=previous_git.get("repo"),
            require_current=False,
        )
        or not is_ancestor(root, previous_publication, current_reviewed)
    ):
        raise WorkflowError(
            "Persisted current closeout plan is not an eligible base-evolution predecessor.",
            exit_code=2,
            payload={"reason_code": "provenance_reprepare_base_evolution_mismatch"},
        )
    facts = finalizer_base_evolution_shared_preflight(
        root,
        task_dir,
        previous_plan,
        current_plan,
    )
    if facts["remote_head"] == current_reviewed:
        raise WorkflowError(
            "Current-plan base evolution is unavailable after the reviewed descendant is pushed.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_remote_not_reviewed_head",
                "reviewed_content_head": current_reviewed,
                "remote_head": facts["remote_head"],
                "fast_forwardable": True,
            },
        )
    if not is_ancestor(root, facts["remote_head"], previous_reviewed):
        raise WorkflowError(
            "Current-plan base evolution is unavailable after predecessor publication is pushed.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_remote_not_reviewed_head",
                "reviewed_content_head": current_reviewed,
                "predecessor_reviewed_content_head": previous_reviewed,
                "predecessor_publication_head": previous_publication,
                "remote_head": facts["remote_head"],
                "fast_forwardable": True,
                "predecessor_has_outbound_publication_side_effect": True,
            },
        )
    standard_gate = task_finalization_path(root, task_dir)
    transition_gate = task_finalization_transition_path(root, task_dir)
    existing_gates = [
        path
        for path in (standard_gate, transition_gate)
        if path.exists() or path.is_symlink()
    ]
    allowed_gate_matches = (
        allowed_gate is not None
        and existing_gates == [standard_gate]
        and standard_gate.is_file()
        and not standard_gate.is_symlink()
        and read_json(standard_gate) == allowed_gate
    )
    if existing_gates and not allowed_gate_matches:
        raise WorkflowError(
            "Current-plan base evolution is unavailable after a finalization gate starts.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_gate_started",
                "gates": [repo_relative(root, path) for path in existing_gates],
            },
        )
    return {
        **facts,
        "supersession_kind": "current_plan",
        "previous_publication_head": previous_publication,
    }

def finalizer_current_transaction_base_evolution_supersession_preflight(
    root: Path,
    task_dir: Path,
    transaction: dict[str, Any],
    current_plan: dict[str, Any],
    *,
    allowed_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Prove that one pushed pre-PR transaction may follow reviewed content."""
    current_git = (
        current_plan.get("git")
        if isinstance(current_plan.get("git"), dict)
        else {}
    )
    current_task = (
        current_plan.get("task")
        if isinstance(current_plan.get("task"), dict)
        else {}
    )
    previous_reviewed = str(transaction.get("branch_review_commit") or "")
    previous_publication = str(transaction.get("publication_head") or "")
    current_reviewed = str(
        current_git.get("reviewed_content_head")
        or current_git.get("branch_review_commit")
        or ""
    )
    task_ref = repo_relative(root, task_dir)
    identity_matches = (
        transaction.get("task_ref") == task_ref
        and current_task.get("active_locator") == task_ref
        and transaction.get("repo_ref") == current_git.get("repo")
        and transaction.get("base_branch") == current_git.get("base_branch")
        and transaction.get("branch") == current_git.get("head_branch")
    )
    previous_publication_errors = (
        []
        if previous_publication == previous_reviewed
        else provenance_tail_commit_errors(
            root,
            previous_reviewed,
            previous_publication,
            target_repo=transaction.get("repo_ref"),
            require_current=False,
        )
    )
    if (
        transaction.get("next_transition") != "verify"
        or "pr" in transaction
        or "verification_ref" in transaction
        or current_plan.get("marketplace", {}).get("required") is not True
        or not identity_matches
        or previous_reviewed == current_reviewed
        or re.fullmatch(r"[0-9a-f]{40}", previous_reviewed) is None
        or re.fullmatch(r"[0-9a-f]{40}", previous_publication) is None
        or previous_publication_errors
        or not is_ancestor(root, previous_publication, current_reviewed)
        or not finalizer_pre_pr_provenance_tail_required(root, current_plan)
    ):
        raise WorkflowError(
            "Current Finalizer transaction is not an eligible base-evolution predecessor.",
            exit_code=2,
            payload={"reason_code": "provenance_reprepare_base_evolution_mismatch"},
        )
    archive_locator = str(current_task.get("archive_locator") or "")
    previous_plan = {
        "schema_version": CLOSEOUT_PLAN_SCHEMA_VERSION,
        "task": {
            "active_locator": task_ref,
            "archive_locator": archive_locator,
        },
        "git": {
            "repo": current_git.get("repo"),
            "remote": current_git.get("remote"),
            "base_branch": current_git.get("base_branch"),
            "head_branch": current_git.get("head_branch"),
            "branch_review_commit": previous_reviewed,
        },
    }
    facts = finalizer_base_evolution_shared_preflight(
        root,
        task_dir,
        previous_plan,
        current_plan,
    )
    remote_head = str(facts["remote_head"])
    if remote_head != previous_publication:
        raise WorkflowError(
            "Transaction base-evolution recovery requires the remote at the predecessor publication HEAD.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_remote_not_reviewed_head",
                "reviewed_content_head": current_reviewed,
                "previous_publication_head": previous_publication,
                "remote_head": remote_head,
                "fast_forwardable": bool(
                    remote_head and is_ancestor(root, remote_head, current_reviewed)
                ),
            },
        )
    standard_gate = task_finalization_path(root, task_dir)
    transition_gate = task_finalization_transition_path(root, task_dir)
    existing_gates = [
        path for path in (standard_gate, transition_gate)
        if path.exists() or path.is_symlink()
    ]
    allowed_gate_matches = (
        allowed_gate is not None
        and existing_gates == [standard_gate]
        and standard_gate.is_file()
        and not standard_gate.is_symlink()
        and read_json(standard_gate) == allowed_gate
    )
    if existing_gates and not allowed_gate_matches:
        raise WorkflowError(
            "Transaction base-evolution recovery found another Finalizer gate.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_gate_started",
                "gates": [repo_relative(root, path) for path in existing_gates],
            },
        )
    return {
        **facts,
        "previous_publication_head": previous_publication,
        "supersession_kind": "current_transaction",
    }

def finalizer_pre_pr_provenance_reprepare_preflight(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    *,
    previous_plan: dict[str, Any] | None = None,
    previous_transaction: dict[str, Any] | None = None,
    allowed_current_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Prove the pre-PR recovery window before any producer or cleanup mutation."""
    git = plan.get("git") if isinstance(plan.get("git"), dict) else {}
    task = plan.get("task") if isinstance(plan.get("task"), dict) else {}
    reviewed_content_head = str(
        git.get("reviewed_content_head") or git.get("branch_review_commit") or ""
    )
    if re.fullmatch(r"[0-9a-f]{40}", reviewed_content_head) is None:
        raise WorkflowError(
            "Provenance reprepare reviewed content identity is invalid.",
            exit_code=2,
            payload={"reason_code": "provenance_reprepare_reviewed_head_invalid"},
        )
    local_head = current_head(root)
    existing_tail_errors = (
        []
        if local_head == reviewed_content_head
        else provenance_tail_commit_errors(
            root,
            reviewed_content_head,
            local_head,
            target_repo=git.get("repo"),
        )
    )
    if existing_tail_errors:
        raise WorkflowError(
            "Provenance reprepare requires reviewed content HEAD or its valid existing tail.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_local_head_changed",
                "errors": existing_tail_errors,
            },
        )

    tracked_owner_state = finalizer_tracked_pre_pr_artifacts(root, task_dir)
    if tracked_owner_state:
        raise WorkflowError(
            "Finalizer will not delete tracked task artifacts during reprepare.",
            exit_code=2,
            payload={"tracked_paths": tracked_owner_state},
        )

    active_locator = str(task.get("active_locator") or "")
    archive_locator = str(task.get("archive_locator") or "")
    if (
        not active_locator
        or repo_relative(root, task_dir) != active_locator
        or (archive_locator and (root / archive_locator).exists())
    ):
        raise WorkflowError(
            "Provenance reprepare is unavailable after archive publication starts.",
            exit_code=2,
            payload={"reason_code": "provenance_reprepare_archive_started"},
        )

    head_branch = str(git.get("head_branch") or "")
    branch_ref = f"refs/heads/{head_branch}"
    branch_worktrees = [
        record
        for record in worktree_records(root)
        if record.get("branch") == branch_ref
    ]
    current_branch_worktrees = [
        record
        for record in branch_worktrees
        if Path(record.get("worktree") or "").resolve() == root.resolve()
    ]
    parallel_consumers = sorted(
        str(record.get("worktree") or "")
        for record in branch_worktrees
        if Path(record.get("worktree") or "").resolve() != root.resolve()
    )
    if not head_branch or len(current_branch_worktrees) != 1 or parallel_consumers:
        raise WorkflowError(
            "Provenance reprepare requires one exclusive publication worktree.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_parallel_publication_consumer",
                "worktrees": parallel_consumers,
            },
        )

    existing_pr = resolve_closeout_pull_request(
        root,
        str(git.get("repo") or ""),
        head_branch,
        str(git.get("base_branch") or ""),
        str(git.get("remote") or "origin"),
    )
    if existing_pr is not None:
        raise WorkflowError(
            "Provenance reprepare is unavailable after pull request creation.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_pull_request_exists",
                "pull_request": existing_pr.get("number"),
            },
        )

    remote_head = closeout_remote_branch_head(root, plan)
    if previous_plan is not None and previous_transaction is not None:
        raise WorkflowError(
            "Provenance reprepare has multiple predecessor authorities.",
            exit_code=2,
        )
    if previous_plan is not None:
        previous_git = (
            previous_plan.get("git")
            if isinstance(previous_plan.get("git"), dict)
            else {}
        )
        if "publication_head" in previous_git:
            base_evolution = (
                finalizer_current_plan_base_evolution_supersession_preflight(
                    root,
                    task_dir,
                    previous_plan,
                    plan,
                    allowed_gate=allowed_current_gate,
                )
            )
        else:
            base_evolution = finalizer_pre_pr_base_evolution_supersession_preflight(
                root,
                task_dir,
                previous_plan,
                plan,
            )
    elif previous_transaction is not None:
        base_evolution = (
            finalizer_current_transaction_base_evolution_supersession_preflight(
                root,
                task_dir,
                previous_transaction,
                plan,
                allowed_gate=allowed_current_gate,
            )
        )
    else:
        base_evolution = None
    if (
        previous_plan is None
        and previous_transaction is None
        and remote_head
        and remote_head != reviewed_content_head
    ):
        raise WorkflowError(
            "Provenance reprepare requires no remote branch or the remote branch at reviewed content HEAD.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_remote_not_reviewed_head",
                "reviewed_content_head": reviewed_content_head,
                "remote_head": remote_head,
                "fast_forwardable": bool(
                    remote_head
                    and is_ancestor(root, remote_head, reviewed_content_head)
                ),
            },
        )
    return {
        "reviewed_content_head": reviewed_content_head,
        "local_head": local_head,
        "remote_head": remote_head,
        "head_branch": head_branch,
        "pull_request": None,
        "parallel_publication_consumers": [],
        "tracked_task_artifacts": [],
        "base_evolution": base_evolution,
    }

def finalizer_supersede_pre_pr_state(root: Path, task_dir: Path) -> list[str]:
    """Retire only owner-private Finalizer state before a fresh plan is reviewed."""
    retired: list[str] = []
    plan = closeout_plan_path(task_dir)
    transaction = finalization_transaction_path(root, task_dir)
    tracked_owner_state = finalizer_tracked_pre_pr_artifacts(root, task_dir)
    if tracked_owner_state:
        raise WorkflowError(
            "Finalizer will not delete tracked task artifacts during reprepare.",
            exit_code=2,
            payload={"tracked_paths": tracked_owner_state},
        )
    if plan.is_file() and not plan.is_symlink():
        persisted_plan = read_json(plan)
        try:
            validate_closeout_plan_for_migration(persisted_plan)
        except WorkflowError:
            persisted_plan = None
        plan.unlink()
        retired.append(repo_relative(root, plan))
    for gate in (
        task_finalization_path(root, task_dir),
        task_finalization_transition_path(root, task_dir),
    ):
        if gate.is_file() and not gate.is_symlink():
            gate.unlink()
            retired.append(repo_relative(root, gate))
    if transaction.is_file() and not transaction.is_symlink():
        transaction.unlink()
        retired.append(repo_relative(root, transaction))
    retired.extend(
        ai_first_retire_owner_checkpoints(
            root,
            task_dir,
            (
                TASK_FINALIZATION_GATE_ARTIFACT,
                TASK_FINALIZATION_TRANSITION_GATE_ARTIFACT,
            ),
        )
    )
    return retired

SKILL_SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"

TASK_PUBLICATION_SKILL_ID = "guru-review-task-publication"

FINALIZE_TASK_SKILL_ID = "guru-finalize-task"

def skill_safe_relative(value: Any) -> Path | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    path = Path(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return None
    return path

def skill_lexical_relative(boundary: Path, path: Path) -> Path | None:
    boundary_abs = Path(os.path.abspath(boundary))
    path_abs = Path(os.path.abspath(path))
    try:
        relative = path_abs.relative_to(boundary_abs)
    except ValueError:
        return None
    if not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        return None
    return relative

def skill_lstat_path(
    boundary: Path,
    path: Path,
    label: str,
    errors: list[str],
    *,
    kind: str,
    required: bool = True,
) -> os.stat_result | None:
    boundary_abs = Path(os.path.abspath(boundary))
    path_abs = Path(os.path.abspath(path))
    if path_abs == boundary_abs:
        try:
            current_stat = boundary_abs.lstat()
        except FileNotFoundError:
            if required:
                errors.append(f"missing {label}")
            return None
        except OSError:
            errors.append(f"{label} cannot be inspected")
            return None
        if stat.S_ISLNK(current_stat.st_mode):
            errors.append(f"{label} contains a symlink component")
            return None
        if kind == "file" and not stat.S_ISREG(current_stat.st_mode):
            errors.append(f"{label} is not a regular file")
            return None
        if kind == "directory" and not stat.S_ISDIR(current_stat.st_mode):
            errors.append(f"{label} is not a directory")
            return None
        return current_stat
    relative = skill_lexical_relative(boundary, path)
    if relative is None:
        errors.append(f"{label} is outside its lexical boundary")
        return None
    current = Path(os.path.abspath(boundary))
    for index, part in enumerate(relative.parts):
        current /= part
        try:
            current_stat = current.lstat()
        except FileNotFoundError:
            if required:
                errors.append(f"missing {label}")
            return None
        except OSError:
            errors.append(f"{label} cannot be inspected")
            return None
        if stat.S_ISLNK(current_stat.st_mode):
            errors.append(f"{label} contains a symlink component")
            return None
        if index < len(relative.parts) - 1 and not stat.S_ISDIR(current_stat.st_mode):
            errors.append(f"{label} has a non-directory ancestor")
            return None
    if kind == "file" and not stat.S_ISREG(current_stat.st_mode):
        errors.append(f"{label} is not a regular file")
        return None
    if kind == "directory" and not stat.S_ISDIR(current_stat.st_mode):
        errors.append(f"{label} is not a directory")
        return None
    return current_stat

def skill_read_schema(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    payload = skill_read_json(path, label, errors)
    if payload is None:
        return None
    if not isinstance(payload.get("type"), str) and not any(
        key in payload for key in ("$ref", "oneOf", "anyOf", "allOf")
    ):
        errors.append(f"{label} is not a recognizable JSON schema")
    schema_uri = payload.get("$schema")
    if schema_uri is not None and schema_uri not in {
        "https://json-schema.org/draft/2020-12/schema",
        "http://json-schema.org/draft-07/schema#",
    }:
        errors.append(f"{label} declares an unsupported JSON schema dialect")
    return payload

def skill_json_loads(value: str) -> Any:
    def reject_constant(constant: str) -> Any:
        raise ValueError(f"non-standard JSON constant: {constant}")

    def parse_finite_float(number: str) -> float:
        parsed = float(number)
        if not math.isfinite(parsed):
            raise ValueError("JSON number is outside the finite runtime range")
        return parsed

    return json.loads(
        value,
        parse_constant=reject_constant,
        parse_float=parse_finite_float,
    )

def skill_json_nonfinite_paths(value: Any, path: str = "$") -> list[str]:
    if isinstance(value, float) and not math.isfinite(value):
        return [path]
    if isinstance(value, list):
        return [
            child_path
            for index, item in enumerate(value)
            for child_path in skill_json_nonfinite_paths(item, f"{path}[{index}]")
        ]
    if isinstance(value, dict):
        return [
            child_path
            for key, item in value.items()
            for child_path in skill_json_nonfinite_paths(item, f"{path}.{key}")
        ]
    return []

def skill_rfc3339_date_time_matches(value: str) -> bool:
    matched = re.fullmatch(
        r"(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})"
        r"[Tt](?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2})"
        r"(?:\.[0-9]+)?(?P<zone>[Zz]|[+-][0-9]{2}:[0-9]{2})",
        value,
    )
    if matched is None:
        return False
    values = {key: int(matched.group(key)) for key in (
        "year", "month", "day", "hour", "minute", "second",
    )}
    zone = matched.group("zone")
    if (
        values["hour"] > 23
        or values["minute"] > 59
        or values["second"] > 60
    ):
        return False

    def leap_year(year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    month_lengths = [
        31,
        29 if leap_year(values["year"]) else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]
    if (
        values["month"] < 1
        or values["month"] > 12
        or values["day"] < 1
        or values["day"] > month_lengths[values["month"] - 1]
    ):
        return False

    if zone.lower() == "z":
        offset_minutes = 0
    else:
        offset_hour = int(zone[1:3])
        offset_minute = int(zone[4:6])
        if offset_hour > 23 or offset_minute > 59:
            return False
        sign = 1 if zone[0] == "+" else -1
        offset_minutes = sign * (offset_hour * 60 + offset_minute)
    if values["second"] != 60:
        return True

    def days_before_year(year: int) -> int:
        # RFC 3339 includes year 0000; count proleptic Gregorian years [0, year).
        return (
            365 * year
            + (year + 3) // 4
            - (year + 99) // 100
            + (year + 399) // 400
        )

    def day_ordinal(year: int, month: int, day: int) -> int:
        lengths = [
            31,
            29 if leap_year(year) else 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ]
        return days_before_year(year) + sum(lengths[:month - 1]) + day - 1

    local_day = day_ordinal(values["year"], values["month"], values["day"])
    utc_minutes = (
        local_day * 24 * 60
        + values["hour"] * 60
        + values["minute"]
        - offset_minutes
    )
    utc_day, utc_minute = divmod(utc_minutes, 24 * 60)
    if utc_minute != 23 * 60 + 59:
        return False
    return any(
        utc_day == day_ordinal(year, month, day)
        for year in range(max(0, values["year"] - 1), min(9999, values["year"] + 1) + 1)
        for month, day in ((6, 30), (12, 31))
    )

def skill_uri_matches(value: str) -> bool:
    if not value or any(ord(character) < 0x21 or ord(character) > 0x7E for character in value):
        return False
    matched = re.match(r"(?P<scheme>[A-Za-z][A-Za-z0-9+.-]*):", value)
    if matched is None:
        return False
    remainder = value[matched.end():]

    unreserved = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")
    sub_delimiters = set("!$&'()*+,;=")

    def component_matches(component: str, extra: str = "") -> bool:
        allowed = unreserved | sub_delimiters | set(extra)
        index = 0
        while index < len(component):
            character = component[index]
            if character == "%":
                if (
                    index + 2 >= len(component)
                    or re.fullmatch(r"[0-9A-Fa-f]{2}", component[index + 1:index + 3]) is None
                ):
                    return False
                index += 3
                continue
            if character not in allowed:
                return False
            index += 1
        return True

    if remainder.count("#") > 1:
        return False
    hierarchy_and_query, separator, fragment = remainder.partition("#")
    if separator and not component_matches(fragment, ":@/?"):
        return False
    hierarchy, query_separator, query = hierarchy_and_query.partition("?")
    if query_separator and not component_matches(query, ":@/?"):
        return False

    authority: str | None = None
    path = hierarchy
    if hierarchy.startswith("//"):
        authority_and_path = hierarchy[2:]
        authority, path_separator, path_tail = authority_and_path.partition("/")
        path = f"/{path_tail}" if path_separator else ""
    if not component_matches(path, ":@/"):
        return False
    if authority is None:
        return True

    if authority.count("@") > 1:
        return False
    userinfo, at, host_and_port = authority.rpartition("@")
    if not at:
        host_and_port = authority
    elif not component_matches(userinfo, ":"):
        return False

    if host_and_port.startswith("["):
        closing = host_and_port.find("]")
        if closing < 0:
            return False
        literal = host_and_port[1:closing]
        suffix = host_and_port[closing + 1:]
        if suffix and (
            not suffix.startswith(":")
            or suffix[1:] and not suffix[1:].isdigit()
        ):
            return False
        if re.fullmatch(r"[Vv][0-9A-Fa-f]+\.[A-Za-z0-9._~!$&'()*+,;=:-]+", literal) is None:
            if "%" in literal:
                return False
            try:
                ipaddress.IPv6Address(literal)
            except ValueError:
                return False
        return True

    if host_and_port.count(":") > 1:
        return False
    host, colon, port = host_and_port.rpartition(":")
    if not colon:
        host = host_and_port
    elif port and not port.isdigit():
        return False
    return component_matches(host)

def skill_format_matches(value: str, expected: str) -> bool:
    if expected == "date-time":
        return skill_rfc3339_date_time_matches(value)
    if expected == "uri":
        return skill_uri_matches(value)
    return False

def skill_read_json(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        payload = skill_json_loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing {label}")
        return None
    except OSError:
        errors.append(f"unreadable {label}")
        return None
    except (UnicodeDecodeError, ValueError):
        errors.append(f"invalid JSON in {label}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{label} root must be an object")
        return None
    return payload

def skill_json_equal(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return left == right
    if type(left) is not type(right):
        return False
    if isinstance(left, list):
        return len(left) == len(right) and all(
            skill_json_equal(left_item, right_item)
            for left_item, right_item in zip(left, right)
        )
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            skill_json_equal(left[key], right[key]) for key in left
        )
    return left == right

SKILL_ECMA_WHITESPACE_CLASS = (
    r"\u0009-\u000d\u0020\u00a0\u1680\u2000-\u200a"
    r"\u2028\u2029\u202f\u205f\u3000\ufeff"
)

SKILL_UTF16_HIGH_SURROGATE = r"[\ud800-\udbff]"

SKILL_UTF16_LOW_SURROGATE = r"[\udc00-\udfff]"

SKILL_UTF16_SURROGATE_PAIR = r"[\ud800-\udbff][\udc00-\udfff]"

def skill_ecma_code_point_complement(excluded_class: str) -> str:
    """Match one ECMA Unicode code point outside a BMP-only character class."""

    return (
        rf"(?:{SKILL_UTF16_SURROGATE_PAIR}|"
        rf"(?!{SKILL_UTF16_SURROGATE_PAIR})"
        rf"(?:(?<!{SKILL_UTF16_HIGH_SURROGATE})(?={SKILL_UTF16_LOW_SURROGATE})|"
        rf"(?!{SKILL_UTF16_LOW_SURROGATE}))[^{excluded_class}])"
    )

SKILL_ECMA_DOT_PATTERN = skill_ecma_code_point_complement(r"\n\r\u2028\u2029")

class SkillPortablePatternError(ValueError):
    pass

def skill_utf16_code_units(value: str) -> str:
    """Project a Python Unicode string onto JavaScript UTF-16 code units."""

    encoded = value.encode("utf-16-le", errors="surrogatepass")
    return "".join(
        chr(encoded[position] | encoded[position + 1] << 8)
        for position in range(0, len(encoded), 2)
    )

class SkillPortablePattern:
    def __init__(self, compiled: re.Pattern[str]):
        self._compiled = compiled

    @property
    def pattern(self) -> str:
        return self._compiled.pattern

    def search(self, value: str) -> re.Match[str] | None:
        return self._compiled.search(skill_utf16_code_units(value))

def skill_compile_portable_pattern(pattern: str) -> SkillPortablePattern:
    """Compile the closed ASCII-source pattern subset with ECMA-262 semantics."""

    def fail(reason: str, position: int) -> None:
        raise SkillPortablePatternError(f"{reason} at offset {position}")

    for position, character in enumerate(pattern):
        if ord(character) > 0x7F:
            fail("uses a non-ASCII pattern character", position)
        if ord(character) < 0x20 or ord(character) == 0x7F:
            fail("uses a raw control character", position)

    control_escapes = {
        "t": (r"\t", 0x09),
        "n": (r"\n", 0x0A),
        "v": (r"\v", 0x0B),
        "f": (r"\f", 0x0C),
        "r": (r"\r", 0x0D),
    }
    syntax_escapes = set(r"^$\.*+?()[]{}|/")

    def parse_escape(
        position: int,
        *,
        in_class: bool,
    ) -> tuple[str, int | None, int]:
        if position + 1 >= len(pattern):
            fail("ends with an incomplete escape", position)
        marker = pattern[position + 1]
        if marker in control_escapes:
            rendered, codepoint = control_escapes[marker]
            return rendered, codepoint, position + 2
        if marker == "u":
            digits = pattern[position + 2:position + 6]
            if len(digits) != 4 or re.fullmatch(r"[0-9A-Fa-f]{4}", digits) is None:
                fail("has an invalid Unicode escape", position)
            codepoint = int(digits, 16)
            if codepoint > 0x7F:
                fail("uses a non-ASCII Unicode escape", position)
            return f"\\u{digits}", codepoint, position + 6
        if marker == "s":
            if in_class:
                return SKILL_ECMA_WHITESPACE_CLASS, None, position + 2
            return f"[{SKILL_ECMA_WHITESPACE_CLASS}]", None, position + 2
        if marker == "S":
            if in_class:
                fail("uses \\S inside a character class", position)
            return (
                skill_ecma_code_point_complement(SKILL_ECMA_WHITESPACE_CLASS),
                None,
                position + 2,
            )
        allowed_syntax = syntax_escapes | ({"-"} if in_class else set())
        if marker in allowed_syntax:
            return re.escape(marker), ord(marker), position + 2
        fail(f"uses unsupported escape \\{marker}", position)

    def parse_class(position: int) -> tuple[str, int]:
        cursor = position + 1
        negated = cursor < len(pattern) and pattern[cursor] == "^"
        if negated:
            cursor += 1
        parts: list[str] = []
        saw_item = False

        def parse_atom(atom_position: int) -> tuple[str, int | None, int]:
            character = pattern[atom_position]
            if character == "\\":
                return parse_escape(atom_position, in_class=True)
            if character == "[":
                fail("uses a nested character class", atom_position)
            if character == "-":
                return r"\-", ord("-"), atom_position + 1
            if character == "^":
                return r"\^", ord("^"), atom_position + 1
            return re.escape(character), ord(character), atom_position + 1

        while cursor < len(pattern):
            if pattern[cursor] == "]":
                if not saw_item:
                    fail("uses an empty character class", position)
                class_body = "".join(parts)
                if negated:
                    return skill_ecma_code_point_complement(class_body), cursor + 1
                return f"[{class_body}]", cursor + 1
            if pattern[cursor] == "-":
                parts.append(r"\-")
                saw_item = True
                cursor += 1
                continue

            rendered, codepoint, next_cursor = parse_atom(cursor)
            if (
                next_cursor < len(pattern)
                and pattern[next_cursor] == "-"
                and next_cursor + 1 < len(pattern)
                and pattern[next_cursor + 1] != "]"
            ):
                if codepoint is None:
                    fail("uses a character-set escape as a range endpoint", cursor)
                endpoint_rendered, endpoint_codepoint, endpoint_cursor = parse_atom(next_cursor + 1)
                if endpoint_codepoint is None:
                    fail("uses a character-set escape as a range endpoint", next_cursor + 1)
                if codepoint > endpoint_codepoint:
                    fail("uses a descending character range", cursor)
                parts.append(f"{rendered}-{endpoint_rendered}")
                cursor = endpoint_cursor
            else:
                parts.append(rendered)
                cursor = next_cursor
            saw_item = True

        fail("has an unterminated character class", position)

    translated: list[str] = []
    group_kinds: list[str] = []
    cursor = 0
    can_quantify = False
    while cursor < len(pattern):
        character = pattern[cursor]
        if character == "\\":
            rendered, _, cursor = parse_escape(cursor, in_class=False)
            translated.append(rendered)
            can_quantify = True
            continue
        if character == "[":
            rendered, cursor = parse_class(cursor)
            translated.append(rendered)
            can_quantify = True
            continue
        if character == "(":
            if pattern.startswith("(?:", cursor):
                translated.append("(?:")
                group_kinds.append("group")
                cursor += 3
            elif pattern.startswith("(?!", cursor):
                translated.append("(?!")
                group_kinds.append("negative_lookahead")
                cursor += 3
            elif pattern.startswith("(?", cursor):
                fail("uses an unsupported group or assertion", cursor)
            else:
                # Captures are deliberately erased because backreferences are outside the subset.
                translated.append("(?:")
                group_kinds.append("group")
                cursor += 1
            can_quantify = False
            continue
        if character == ")":
            if not group_kinds:
                fail("has an unmatched closing parenthesis", cursor)
            group_kind = group_kinds.pop()
            translated.append(")")
            cursor += 1
            can_quantify = group_kind == "group"
            continue
        if character == "|":
            translated.append("|")
            cursor += 1
            can_quantify = False
            continue
        if character == "^":
            translated.append("^")
            cursor += 1
            can_quantify = False
            continue
        if character == "$":
            translated.append(r"\Z")
            cursor += 1
            can_quantify = False
            continue
        if character == ".":
            translated.append(SKILL_ECMA_DOT_PATTERN)
            cursor += 1
            can_quantify = True
            continue
        if character in "*+?":
            if not can_quantify:
                fail("uses a misplaced or repeated quantifier", cursor)
            translated.append(character)
            cursor += 1
            can_quantify = False
            continue
        if character == "{":
            if not can_quantify:
                fail("uses a misplaced or repeated quantifier", cursor)
            closing = pattern.find("}", cursor + 1)
            if closing < 0:
                fail("has an unterminated bounded quantifier", cursor)
            body = pattern[cursor + 1:closing]
            match = re.fullmatch(r"([0-9]+)(?:,([0-9]*))?", body)
            if match is None:
                fail("has an invalid bounded quantifier", cursor)
            lower_text = match.group(1)
            upper_text = match.group(2)
            if len(lower_text) > 6 or upper_text is not None and len(upper_text) > 6:
                fail("uses a bounded quantifier outside the portable range", cursor)
            lower = int(lower_text)
            if upper_text not in (None, "") and lower > int(upper_text):
                fail("has a descending bounded quantifier", cursor)
            translated.append(pattern[cursor:closing + 1])
            cursor = closing + 1
            can_quantify = False
            continue
        if character in "}]":
            fail(f"has an unmatched {character}", cursor)

        translated.append(re.escape(character))
        cursor += 1
        can_quantify = True

    if group_kinds:
        fail("has an unterminated group", len(pattern))
    try:
        return SkillPortablePattern(re.compile("".join(translated)))
    except re.error as error:
        raise SkillPortablePatternError("cannot be represented by the portable pattern subset") from error

def skill_json_schema_subset_errors(
    schema: Any,
    label: str,
    *,
    relative_root: Path | None = None,
    boundary: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    local_ref_targets: dict[int, dict[str, Any]] = {}
    allowed_keywords = {
        "$schema", "$id", "$defs", "$ref", "title", "description",
        "type", "const", "enum", "allOf", "anyOf", "oneOf", "not",
        "if", "then", "else", "minLength", "maxLength", "pattern", "format",
        "minimum", "maximum", "minItems", "maxItems", "uniqueItems", "items",
        "contains", "properties", "required", "minProperties", "additionalProperties",
    }
    json_types = {"object", "array", "string", "boolean", "null", "integer", "number"}
    supported_formats = {"date-time", "uri"}

    def add(path: str, reason: str) -> None:
        errors.append(f"[schema_subset] {label} schema {reason} at {path}")

    for nonfinite_path in skill_json_nonfinite_paths(schema):
        add(nonfinite_path, "contains a non-finite number")

    def resolve_ref(reference: Any, path: str, node: dict[str, Any]) -> None:
        if not isinstance(reference, str):
            add(path, "has a non-string $ref")
            return
        if reference.startswith("#/"):
            target: Any = schema
            for encoded_part in reference[2:].split("/"):
                part = encoded_part.replace("~1", "/").replace("~0", "~")
                if not isinstance(target, dict) or part not in target:
                    add(path, "has an unresolved $ref")
                    return
                target = target[part]
            if not isinstance(target, dict):
                add(path, "has a $ref that does not resolve to an object schema")
            else:
                local_ref_targets[id(node)] = target
            return
        relative = skill_safe_relative(reference)
        if relative is None or relative_root is None or boundary is None:
            add(path, "has a non-local or invalid $ref")
            return
        target_path = relative_root / relative
        reference_errors: list[str] = []
        if skill_lstat_path(
            boundary,
            target_path,
            f"schema reference {reference}",
            reference_errors,
            kind="file",
        ) is None:
            add(path, "has an unsafe or unresolved package-local $ref")
            return
        try:
            target = skill_json_loads(target_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError):
            add(path, "has an unreadable package-local $ref")
            return
        if not isinstance(target, dict):
            add(path, "has a package-local $ref that does not resolve to an object schema")

    def validate_nonnegative_integer(value: Any, path: str, keyword: str) -> None:
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            add(path, f"has an invalid {keyword}")

    def validate_node(node: Any, path: str) -> None:
        if not isinstance(node, dict):
            add(path, "uses a boolean or non-object schema node")
            return

        for keyword in sorted(set(node) - allowed_keywords):
            add(path, f"uses unsupported keyword {keyword}")

        if "$schema" in node and node.get("$schema") != SKILL_SCHEMA_DIALECT:
            add(path, "declares an unsupported $schema dialect")
        for keyword in ("$id", "title", "description"):
            if keyword in node and not isinstance(node.get(keyword), str):
                add(path, f"has a non-string {keyword}")
        if "$id" in node and path != "$":
            add(path, "uses a non-root $id resource boundary")
        if "$ref" in node:
            resolve_ref(node.get("$ref"), path, node)

        definitions = node.get("$defs")
        if definitions is not None:
            if not isinstance(definitions, dict):
                add(path, "has a non-object $defs")
            else:
                for name, child in definitions.items():
                    validate_node(child, f"{path}.$defs.{name}")

        expected_type = node.get("type")
        if expected_type is not None:
            if isinstance(expected_type, str):
                expected_types = [expected_type]
            elif isinstance(expected_type, list):
                expected_types = expected_type
            else:
                expected_types = []
            if (
                not expected_types
                or any(not isinstance(item, str) or item not in json_types for item in expected_types)
                or len(expected_types) != len(set(expected_types))
            ):
                add(path, "has an invalid type")

        enum = node.get("enum")
        if enum is not None:
            if not isinstance(enum, list) or not enum:
                add(path, "has an invalid enum")
            elif any(
                skill_json_equal(item, previous)
                for index, item in enumerate(enum)
                for previous in enum[:index]
            ):
                add(path, "has duplicate enum values")

        for keyword in ("allOf", "anyOf", "oneOf"):
            branches = node.get(keyword)
            if branches is not None:
                if not isinstance(branches, list) or not branches:
                    add(path, f"has an invalid {keyword}")
                else:
                    for index, branch in enumerate(branches):
                        validate_node(branch, f"{path}.{keyword}[{index}]")
        for keyword in ("not", "if", "then", "else", "items", "contains"):
            if keyword in node:
                validate_node(node.get(keyword), f"{path}.{keyword}")

        for keyword in ("minLength", "maxLength", "minItems", "maxItems", "minProperties"):
            if keyword in node:
                validate_nonnegative_integer(node.get(keyword), path, keyword)
        if (
            isinstance(node.get("minLength"), int)
            and not isinstance(node.get("minLength"), bool)
            and isinstance(node.get("maxLength"), int)
            and not isinstance(node.get("maxLength"), bool)
            and node["minLength"] > node["maxLength"]
        ):
            add(path, "has minLength greater than maxLength")
        if (
            isinstance(node.get("minItems"), int)
            and not isinstance(node.get("minItems"), bool)
            and isinstance(node.get("maxItems"), int)
            and not isinstance(node.get("maxItems"), bool)
            and node["minItems"] > node["maxItems"]
        ):
            add(path, "has minItems greater than maxItems")

        pattern = node.get("pattern")
        if pattern is not None:
            if not isinstance(pattern, str):
                add(path, "has a non-string pattern")
            else:
                try:
                    skill_compile_portable_pattern(pattern)
                except SkillPortablePatternError as error:
                    add(path, f"has an invalid portable pattern ({error})")
        expected_format = node.get("format")
        if expected_format is not None:
            if not isinstance(expected_format, str):
                add(path, "has a non-string format")
            elif expected_format not in supported_formats:
                add(path, "has an unsupported format")

        for keyword in ("minimum", "maximum"):
            value = node.get(keyword)
            if keyword in node and (
                not isinstance(value, (int, float)) or isinstance(value, bool)
                or isinstance(value, float) and not math.isfinite(value)
            ):
                add(path, f"has an invalid {keyword}")
        if (
            isinstance(node.get("minimum"), (int, float))
            and not isinstance(node.get("minimum"), bool)
            and isinstance(node.get("maximum"), (int, float))
            and not isinstance(node.get("maximum"), bool)
            and node["minimum"] > node["maximum"]
        ):
            add(path, "has minimum greater than maximum")

        if "uniqueItems" in node and not isinstance(node.get("uniqueItems"), bool):
            add(path, "has a non-boolean uniqueItems")
        properties = node.get("properties")
        if properties is not None:
            if not isinstance(properties, dict):
                add(path, "has non-object properties")
            else:
                for name, child in properties.items():
                    validate_node(child, f"{path}.properties.{name}")
        required = node.get("required")
        if required is not None and (
            not isinstance(required, list)
            or any(not isinstance(item, str) for item in required)
            or len(required) != len(set(required))
        ):
            add(path, "has an invalid required")
        if "additionalProperties" in node:
            additional = node.get("additionalProperties")
            if isinstance(additional, dict):
                validate_node(additional, f"{path}.additionalProperties")
            elif not isinstance(additional, bool):
                add(path, "has an invalid additionalProperties")

    def schema_children(node: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
        children: list[tuple[str, dict[str, Any]]] = []
        for keyword in ("$defs", "properties"):
            values = node.get(keyword)
            if isinstance(values, dict):
                children.extend(
                    (f"{keyword}.{name}", child)
                    for name, child in values.items()
                    if isinstance(child, dict)
                )
        for keyword in ("allOf", "anyOf", "oneOf"):
            values = node.get(keyword)
            if isinstance(values, list):
                children.extend(
                    (f"{keyword}[{index}]", child)
                    for index, child in enumerate(values)
                    if isinstance(child, dict)
                )
        for keyword in ("not", "if", "then", "else", "items", "contains"):
            child = node.get(keyword)
            if isinstance(child, dict):
                children.append((keyword, child))
        additional = node.get("additionalProperties")
        if isinstance(additional, dict):
            children.append(("additionalProperties", additional))
        return children

    def detect_recursive_refs(
        node: dict[str, Any],
        path: str,
        active: set[int],
        complete: set[int],
    ) -> None:
        node_id = id(node)
        if node_id in active:
            add(path, "has a recursive $ref")
            return
        if node_id in complete:
            return
        active.add(node_id)
        for child_label, child in schema_children(node):
            detect_recursive_refs(child, f"{path}.{child_label}", active, complete)
        target = local_ref_targets.get(node_id)
        if target is not None:
            detect_recursive_refs(target, f"{path}.$ref", active, complete)
        active.remove(node_id)
        complete.add(node_id)

    validate_node(schema, "$")
    if isinstance(schema, dict):
        detect_recursive_refs(schema, "$", set(), set())
    return errors

def skill_json_schema_validation_errors(
    instance: Any,
    schema: dict[str, Any],
    label: str,
) -> list[str]:
    errors = skill_json_schema_subset_errors(schema, label)
    if errors:
        return errors
    nonfinite_paths = skill_json_nonfinite_paths(instance)
    if nonfinite_paths:
        return [
            f"{label} contains a non-finite number at {path}"
            for path in nonfinite_paths
        ]
    active_references: set[str] = set()

    def resolve_ref(reference: Any, output: list[str], path: str) -> dict[str, Any] | None:
        if not isinstance(reference, str) or not reference.startswith("#/"):
            output.append(f"{label} schema has an unsupported reference at {path}")
            return None
        target: Any = schema
        for encoded_part in reference[2:].split("/"):
            part = encoded_part.replace("~1", "/").replace("~0", "~")
            if not isinstance(target, dict) or part not in target:
                output.append(f"{label} schema has an unresolved reference at {path}")
                return None
            target = target[part]
        if not isinstance(target, dict):
            output.append(f"{label} schema reference does not resolve to an object at {path}")
            return None
        return target

    def type_matches(value: Any, expected: str) -> bool:
        if expected == "object":
            return isinstance(value, dict)
        if expected == "array":
            return isinstance(value, list)
        if expected == "string":
            return isinstance(value, str)
        if expected == "boolean":
            return isinstance(value, bool)
        if expected == "null":
            return value is None
        if expected == "integer":
            return (
                isinstance(value, int) and not isinstance(value, bool)
            ) or (
                isinstance(value, float) and math.isfinite(value) and value.is_integer()
            )
        if expected == "number":
            return (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and (not isinstance(value, float) or math.isfinite(value))
            )
        return False

    def validate(value: Any, node: Any, path: str, output: list[str]) -> None:
        if not isinstance(node, dict):
            output.append(f"{label} schema node is not an object at {path}")
            return
        if "$ref" in node:
            reference = node.get("$ref")
            target = resolve_ref(reference, output, path)
            if target is not None and isinstance(reference, str):
                if reference in active_references:
                    output.append(f"{label} schema has a recursive reference at {path}")
                else:
                    active_references.add(reference)
                    try:
                        validate(value, target, path, output)
                    finally:
                        active_references.remove(reference)
        all_options = node.get("allOf")
        if all_options is not None:
            if not isinstance(all_options, list) or not all_options:
                output.append(f"{label} schema has an invalid allOf at {path}")
            else:
                for option in all_options:
                    validate(value, option, path, output)
        any_options = node.get("anyOf")
        if any_options is not None:
            if not isinstance(any_options, list) or not any_options:
                output.append(f"{label} schema has an invalid anyOf at {path}")
            else:
                branch_results: list[list[str]] = []
                for option in any_options:
                    branch_errors: list[str] = []
                    validate(value, option, path, branch_errors)
                    branch_results.append(branch_errors)
                if not any(not branch_errors for branch_errors in branch_results):
                    output.append(f"{label} violates anyOf at {path}")
        options = node.get("oneOf")
        if options is not None:
            if not isinstance(options, list) or not options:
                output.append(f"{label} schema has an invalid oneOf at {path}")
                return
            matches = 0
            for option in options:
                branch_errors: list[str] = []
                validate(value, option, path, branch_errors)
                if not branch_errors:
                    matches += 1
            if matches != 1:
                output.append(f"{label} violates oneOf at {path}")

        negated = node.get("not")
        if negated is not None:
            negated_errors: list[str] = []
            validate(value, negated, path, negated_errors)
            if not negated_errors:
                output.append(f"{label} violates not at {path}")

        condition = node.get("if")
        if condition is not None:
            condition_errors: list[str] = []
            validate(value, condition, path, condition_errors)
            branch = node.get("then") if not condition_errors else node.get("else")
            if branch is not None:
                validate(value, branch, path, output)

        expected_type = node.get("type")
        if expected_type is not None:
            expected_types = (
                [expected_type]
                if isinstance(expected_type, str)
                else expected_type
                if isinstance(expected_type, list)
                else []
            )
            if (
                not expected_types
                or any(not isinstance(item, str) for item in expected_types)
                or not any(type_matches(value, item) for item in expected_types)
            ):
                output.append(f"{label} has wrong type at {path}")
                return
        if "const" in node and not skill_json_equal(value, node.get("const")):
            output.append(f"{label} violates const at {path}")
        enum = node.get("enum")
        if enum is not None:
            if not isinstance(enum, list) or not any(skill_json_equal(value, item) for item in enum):
                output.append(f"{label} violates enum at {path}")

        if isinstance(value, str):
            minimum = node.get("minLength")
            if isinstance(minimum, int) and len(value) < minimum:
                output.append(f"{label} is shorter than minLength at {path}")
            maximum = node.get("maxLength")
            if isinstance(maximum, int) and len(value) > maximum:
                output.append(f"{label} is longer than maxLength at {path}")
            pattern = node.get("pattern")
            if isinstance(pattern, str):
                try:
                    pattern_matches = skill_compile_portable_pattern(pattern).search(value) is not None
                except SkillPortablePatternError:
                    pattern_matches = False
                if not pattern_matches:
                    output.append(f"{label} violates pattern at {path}")
            expected_format = node.get("format")
            if isinstance(expected_format, str) and not skill_format_matches(value, expected_format):
                output.append(f"{label} violates format at {path}")

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            minimum = node.get("minimum")
            maximum = node.get("maximum")
            if isinstance(minimum, (int, float)) and value < minimum:
                output.append(f"{label} is less than minimum at {path}")
            if isinstance(maximum, (int, float)) and value > maximum:
                output.append(f"{label} is greater than maximum at {path}")

        if isinstance(value, list):
            minimum = node.get("minItems")
            if isinstance(minimum, int) and len(value) < minimum:
                output.append(f"{label} has fewer than minItems at {path}")
            maximum = node.get("maxItems")
            if isinstance(maximum, int) and len(value) > maximum:
                output.append(f"{label} has more than maxItems at {path}")
            if node.get("uniqueItems") is True:
                for index, item in enumerate(value):
                    if any(skill_json_equal(item, previous) for previous in value[:index]):
                        output.append(f"{label} violates uniqueItems at {path}")
                        break
            item_schema = node.get("items")
            if item_schema is not None:
                for index, item in enumerate(value):
                    validate(item, item_schema, f"{path}[{index}]", output)
            contains_schema = node.get("contains")
            if contains_schema is not None:
                contains_match = False
                for index, item in enumerate(value):
                    branch_errors: list[str] = []
                    validate(item, contains_schema, f"{path}[{index}]", branch_errors)
                    if not branch_errors:
                        contains_match = True
                        break
                if not contains_match:
                    output.append(f"{label} violates contains at {path}")

        if isinstance(value, dict):
            minimum = node.get("minProperties")
            if isinstance(minimum, int) and len(value) < minimum:
                output.append(f"{label} has fewer than minProperties at {path}")
            required = node.get("required")
            if isinstance(required, list):
                for key in required:
                    if isinstance(key, str) and key not in value:
                        output.append(f"{label} is missing required property at {path}.{key}")
            properties = node.get("properties")
            declared_properties = properties if isinstance(properties, dict) else {}
            additional = node.get("additionalProperties")
            for key in value:
                if key not in declared_properties:
                    if additional is False:
                        output.append(f"{label} has an additional property at {path}.{key}")
                    elif isinstance(additional, dict):
                        validate(value[key], additional, f"{path}.{key}", output)
            if isinstance(properties, dict):
                for key, child_schema in properties.items():
                    if key in value:
                        validate(value[key], child_schema, f"{path}.{key}", output)

    try:
        validate(instance, schema, "$", errors)
    except Exception:
        errors.append(f"{label} schema validation failed safely on malformed input")
    return errors

def stage0_invocation_error(code: str, field_path: str, remediation: str, message: str) -> WorkflowError:
    return WorkflowError(
        message,
        exit_code=2,
        payload={"code": code, "field_path": field_path, "remediation": remediation},
    )

def stage0_output_contract(
    skill_id: str,
    package: Path,
    interface: dict[str, Any],
    exit_id: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    declared_exits = {
        str(item.get("id") or "")
        for item in interface.get("external_exits", []) if isinstance(item, dict)
    }
    if exit_id not in declared_exits:
        raise stage0_invocation_error(
            "unknown_typed_exit",
            "owner_result.typed_exit",
            f"Rerun the owner step so it returns one declared typed exit for {skill_id}: {', '.join(sorted(declared_exits))}.",
            "Stage 0 owner result selected an unknown typed exit.",
        )
    contracts = interface["public_contracts"]
    outputs = [
        item for item in contracts.get("outputs", [])
        if isinstance(item, dict) and item.get("exit_id") == exit_id
    ]
    projections = [
        item for item in contracts.get("projections", [])
        if isinstance(item, dict) and item.get("exit_id") == exit_id
    ]
    if len(outputs) != 1 or len(projections) != 1:
        raise stage0_invocation_error(
            "invalid_public_contract",
            f"public_contracts.outputs.{exit_id}",
            "Restore one output and one projection for every declared typed exit.",
            "Stage 0 typed output contract is missing or ambiguous.",
        )
    output = outputs[0]
    projection = projections[0]
    schema_ref = output.get("schema")
    errors: list[str] = []
    schema = skill_read_schema(
        package / str(schema_ref.get("path") if isinstance(schema_ref, dict) else ""),
        "Stage 0 typed output schema",
        errors,
    )
    if errors or not isinstance(schema, dict):
        raise stage0_invocation_error(
            "invalid_public_contract",
            f"public_contracts.outputs.{exit_id}",
            "Restore the declared output schema and rerun package validation.",
            "Stage 0 typed output contract is invalid.",
        )
    return schema, projection

def stage0_owner_path(root: Path, value: str | None, field: str) -> Path:
    raw = str(value or "").strip()
    relative = skill_safe_relative(raw)
    if relative is None:
        raise stage0_invocation_error(
            "invalid_owner_result",
            field,
            "Provide the repo-relative locator emitted by the completed owner step.",
            "Stage 0 owner result locator is invalid.",
        )
    path = root / relative
    errors: list[str] = []
    if skill_lstat_path(root, path, "Stage 0 owner result", errors, kind="file") is None:
        raise stage0_invocation_error(
            "invalid_owner_result",
            field,
            "Restore the regular repo-local owner result and rerun its checker.",
            "Stage 0 owner result is missing or unsafe.",
        )
    return path

def parse_canonical_pull_request_url(repo: str, url: Any) -> tuple[str, int]:
    expected_repo = normalize_github_repository(repo)
    if not expected_repo or not isinstance(url, str) or not git_remote_config_value_is_safe(url):
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        )
    try:
        parsed = urlsplit(url)
    except ValueError as exc:
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        ) from exc
    parts = parsed.path.split("/")
    if (
        parsed.scheme != "https"
        or parsed.netloc != "github.com"
        or parsed.query
        or parsed.fragment
        or len(parts) != 5
        or parts[0] != ""
        or parts[3] != "pull"
        or not re.fullmatch(r"[1-9][0-9]*", parts[4])
        or normalize_github_repository(f"{parts[1]}/{parts[2]}") != expected_repo
    ):
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        )
    try:
        number = int(parts[4])
    except ValueError as exc:
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        ) from exc
    return url, number

def canonical_pull_request_url(repo: str, number: int, url: Any) -> str:
    value, parsed_number = parse_canonical_pull_request_url(repo, url)
    if isinstance(number, bool) or not isinstance(number, int) or parsed_number != number:
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        )
    return value

def create_pull_request(
    root: Path,
    repo: str,
    base_branch: str,
    branch: str,
    title: str,
    body: str,
    draft: bool,
) -> str:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        tmp.write(body)
        body_file = tmp.name
    try:
        command = [
            "pr", "create", "--repo", repo, "--base", base_branch,
            "--head", branch, "--title", title, "--body-file", body_file,
        ]
        if draft:
            command.append("--draft")
        proc = run_gh_command(command, root, repo=repo, operation="pull_request_create")
        pr_url = proc.stdout.strip()
        try:
            canonical_url, _ = parse_canonical_pull_request_url(repo, pr_url)
        except WorkflowError as exc:
            raise github_response_incomplete(
                operation="pull_request_create",
                repo=repo,
                detail="gh pr create did not return a canonical PR URL for the current repository.",
            ) from exc
        return canonical_url
    finally:
        Path(body_file).unlink(missing_ok=True)

def update_pull_request_metadata(
    root: Path,
    repo: str,
    number: int,
    title: str,
    body: str,
) -> None:
    if normalize_github_repository(repo) != repo.casefold():
        raise WorkflowError("Closeout pull request repository is invalid.", exit_code=2)
    if isinstance(number, bool) or not isinstance(number, int) or number <= 0:
        raise WorkflowError("Closeout pull request number is invalid.", exit_code=2)
    try:
        body_bytes = body.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise WorkflowError("Closeout pull request body is not valid UTF-8.", exit_code=2) from exc
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
        tmp.write(body_bytes)
        body_file = tmp.name
    try:
        run_gh_command(
            [
                "pr",
                "edit",
                str(number),
                "--repo",
                repo,
                "--title",
                title,
                "--body-file",
                body_file,
            ],
            root,
            repo=repo,
            operation="pull_request_edit",
        )
    finally:
        Path(body_file).unlink(missing_ok=True)

def validate_publish_identity_and_remote_head(
    root: Path,
    task: dict[str, Any],
    task_context: dict[str, Any],
    repo: str,
    base_branch: str,
    branch: str,
    remote: str,
) -> dict[str, str]:
    errors: list[str] = []
    expected_repo = str(
        task_context.get("source_repo", {}).get("repo")
        if isinstance(task_context.get("source_repo"), dict)
        else ""
    ).strip()
    if expected_repo and expected_repo.casefold() != repo.casefold():
        errors.append("publish repo does not match current task runtime repository identity")
    expected_branch = str(task_context.get("branch_name") or "").strip()
    if expected_branch and expected_branch != branch:
        errors.append("current head branch does not match current task runtime branch")
    normalized_base = normalize_ref(base_branch).removeprefix("origin/")
    for label, value in [
        ("task runtime identity", task_context.get("base_branch")),
        ("task.json", task.get("base_branch")),
    ]:
        if value and normalize_ref(str(value)).removeprefix("origin/") != normalized_base:
            errors.append(f"publish base branch does not match {label} base_branch")
    if errors:
        raise WorkflowError(
            "Publish branch/base/repository identity validation failed.",
            exit_code=2,
            payload={"errors": errors},
        )
    head = current_head(root)
    remote_proc = run(["git", "ls-remote", "--heads", remote, branch], cwd=root, check=False)
    remote_lines = [line.split() for line in remote_proc.stdout.splitlines() if line.strip()]
    remote_head = remote_lines[0][0] if len(remote_lines) == 1 and remote_lines[0] else ""
    if remote_proc.returncode != 0 or remote_head != head:
        raise WorkflowError(
            "Publish remote branch HEAD does not match the current local HEAD.",
            exit_code=2,
            payload={"head": head, "remote_head": remote_head},
        )
    return {
        "repo": repo,
        "base_branch": normalized_base,
        "head_branch": branch,
        "head": head,
        "remote_head": remote_head,
    }

def closeout_plan_path(task_dir: Path) -> Path:
    return task_dir / CLOSEOUT_PLAN_ARTIFACT

def task_finalization_path(
    root: Path,
    task_dir: Path,
) -> Path:
    return ai_first_owner_checkpoint_path(
        root,
        task_dir,
        TASK_FINALIZATION_GATE_ARTIFACT,
    )

def task_finalization_transition_path(
    root: Path,
    task_dir: Path,
) -> Path:
    return ai_first_owner_checkpoint_path(
        root,
        task_dir,
        TASK_FINALIZATION_TRANSITION_GATE_ARTIFACT,
    )

def closeout_ledger_matches_plan_bytes(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    ledger: dict[str, Any],
) -> bool:
    inputs = plan.get("inputs")
    bound = (
        inputs.get("issue_scope_ledger")
        if isinstance(inputs, dict)
        else None
    )
    path = issue_scope_ledger_path(task_dir)
    return issue_scope_ledger_errors(ledger) == [] and bound == closeout_input_record(
        root,
        path,
    )

def closeout_input_record(root: Path, path: Path, *, payload: dict[str, Any] | None = None) -> dict[str, str]:
    if not path.is_file() and payload is None:
        raise WorkflowError("Closeout protected input is missing.", exit_code=2, payload={"path": str(path)})
    digest = canonical_json_sha256(payload) if payload is not None else hashlib.sha256(path.read_bytes()).hexdigest()
    return {"path": repo_relative(root, path), "sha256": digest}

def current_archive_month() -> str:
    """Return the month used by the unmodified official task archive command."""
    return datetime.now().strftime("%Y-%m")

def closeout_archive_month(plan: dict[str, Any]) -> str:
    parts = Path(str(plan.get("task", {}).get("archive_locator") or "")).parts
    if len(parts) != 5 or parts[:3] != (".trellis", "tasks", "archive"):
        raise WorkflowError("Closeout archive locator does not contain one canonical month.", exit_code=2)
    month = parts[3]
    if not re.fullmatch(r"\d{4}-\d{2}", month):
        raise WorkflowError("Closeout archive locator month is invalid.", exit_code=2)
    return month

def assert_closeout_archive_month_current(plan: dict[str, Any]) -> None:
    planned = closeout_archive_month(plan)
    actual = current_archive_month()
    if planned != actual:
        raise WorkflowError(
            "Closeout archive month no longer matches the official task.py archive month; the task remains active.",
            exit_code=2,
            payload={
                "stage": "archive-month-preflight",
                "planned_month": planned,
                "official_month": actual,
                "next_action": "rerun trellis-finish-work dry-run and review a new digest before formal closeout",
            },
        )

def assert_closeout_archive_path_preflight(root: Path, archive_locator: str) -> None:
    """Inspect archive ancestors lexically without following symlink components."""
    parts = Path(archive_locator).parts
    if (
        len(parts) != 5
        or parts[:3] != (".trellis", "tasks", "archive")
        or not re.fullmatch(r"\d{4}-\d{2}", parts[3])
        or not parts[4]
    ):
        raise WorkflowError("Closeout archive locator is not canonical.", exit_code=2)
    components = (
        ("archive-root", root.joinpath(*parts[:3])),
        ("archive-month", root.joinpath(*parts[:4])),
        ("archive-destination", root.joinpath(*parts)),
    )
    for component, path in components:
        try:
            mode = os.lstat(path).st_mode
        except FileNotFoundError:
            break
        except OSError as exc:
            raise WorkflowError(
                "Closeout archive path component could not be inspected lexically.",
                exit_code=2,
                payload={
                    "stage": "archive-path-preflight",
                    "component": component,
                    "path": path.relative_to(root).as_posix(),
                },
            ) from exc
        if stat.S_ISLNK(mode):
            raise WorkflowError(
                "Closeout archive path contains a symlink component; the task remains active.",
                exit_code=2,
                payload={
                    "stage": "archive-path-preflight",
                    "component": component,
                    "path": path.relative_to(root).as_posix(),
                },
            )
        if component != "archive-destination" and not stat.S_ISDIR(mode):
            raise WorkflowError(
                "Closeout archive path ancestor is not a directory; the task remains active.",
                exit_code=2,
                payload={
                    "stage": "archive-path-preflight",
                    "component": component,
                    "path": path.relative_to(root).as_posix(),
                },
            )
        if component == "archive-destination":
            raise WorkflowError(
                "Closeout planned archive locator already exists; the task remains active.",
                exit_code=2,
                payload={
                    "stage": "archive-locator-preflight",
                    "archive_locator": archive_locator,
                },
            )

def official_active_task_match(tasks_dir: Path, task_name: str) -> Path | None:
    """Mirror official task_utils.find_task_by_name active-directory lookup."""
    if not task_name or not tasks_dir.is_dir():
        return None
    exact_match = tasks_dir / task_name
    if exact_match.is_dir():
        return exact_match
    for candidate in tasks_dir.iterdir():
        if candidate.is_dir() and candidate.name.endswith(f"-{task_name}"):
            return candidate
    return None

def official_archive_would_handle_child_metadata(child_json: Path) -> bool:
    """Match official read_json plus the truthy child_data mutation guard."""
    try:
        payload = json.loads(child_json.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return False
    return bool(payload)

def validate_closeout_task_children(task_dir: Path, task: dict[str, Any]) -> None:
    children = task.get("children", [])
    if not isinstance(children, list) or any(not isinstance(child, str) for child in children):
        raise WorkflowError(
            "Closeout task children must be a list of strings.",
            exit_code=2,
            payload={"stage": "task-children-preflight"},
        )
    tasks_dir = task_dir.parent
    active_children: list[str] = []
    for child_name in children:
        child_dir = official_active_task_match(tasks_dir, child_name)
        if child_dir is not None and official_archive_would_handle_child_metadata(
            child_dir / "task.json"
        ):
            active_children.append(child_dir.name)
    if active_children:
        raise WorkflowError(
            "Closeout archive transaction would modify active child task metadata.",
            exit_code=2,
            payload={
                "stage": "task-children-preflight",
                "active_children": active_children,
            },
        )

def closeout_transaction_parent_head(plan: dict[str, Any]) -> str:
    git = plan.get("git", {}) if isinstance(plan.get("git"), dict) else {}
    return str(git.get("publication_head") or git.get("branch_review_commit") or "")

def validate_closeout_reviewed_content(
    root: Path,
    plan: dict[str, Any],
    commit: str,
    *,
    include_worktree: bool,
) -> str:
    branch_review_commit = closeout_transaction_parent_head(plan)
    if (
        re.fullmatch(r"[0-9a-f]{40}", branch_review_commit) is None
        or re.fullmatch(r"[0-9a-f]{40}", commit) is None
        or not is_ancestor(root, branch_review_commit, commit)
    ):
        raise WorkflowError(
            "Closeout commit is not a descendant of branch_review_commit.",
            exit_code=2,
        )
    anchor_identity = reviewed_content_identity(
        root,
        branch_review_commit,
        include_worktree=False,
    )["sha256"]
    current_identity = reviewed_content_identity(
        root,
        commit,
        include_worktree=include_worktree,
    )["sha256"]
    if current_identity != anchor_identity:
        raise WorkflowError(
            "Closeout reviewed content changed after Branch Review.",
            exit_code=2,
        )
    return anchor_identity

def normalize_closeout_archive_identity(value: Any, archive_locator: str) -> Any:
    if isinstance(value, dict):
        return {
            key: normalize_closeout_archive_identity(item, archive_locator)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [normalize_closeout_archive_identity(item, archive_locator) for item in value]
    if isinstance(value, str):
        if value == archive_locator:
            return "<archive-locator>"
        prefix = f"{archive_locator}/"
        if value.startswith(prefix):
            return f"<archive-locator>/{value.removeprefix(prefix)}"
    return value

def closeout_month_supersession_errors(
    previous: dict[str, Any],
    current: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    try:
        previous_month = closeout_archive_month(previous)
        current_month = closeout_archive_month(current)
    except WorkflowError as exc:
        return [str(exc)]
    if previous_month == current_month:
        errors.append("closeout archive month supersession requires a changed month.")
    if current.get("projection", {}).get("migration_predecessor_plan_digest") is not None:
        errors.append(
            "closeout archive month supersession must retire migration predecessor compatibility."
        )

    normalized: list[dict[str, Any]] = []
    for plan, locator in (
        (previous, previous["task"]["archive_locator"]),
        (current, current["task"]["archive_locator"]),
    ):
        candidate = copy.deepcopy(plan)
        candidate.pop("plan_digest", None)
        candidate["projection"]["migration_predecessor_plan_digest"] = None
        candidate["projection"]["summary_template_sha256"] = "<archive-template-digest>"
        normalized.append(normalize_closeout_archive_identity(candidate, locator))
    if normalized[0] != normalized[1]:
        errors.append("archive month supersession changed facts beyond archive identity.")
    return errors

def official_after_archive_hook_state(root: Path) -> dict[str, Any]:
    """Reject official after_archive hooks before the archive command can run them."""
    config_path = root / ".trellis/config.yaml"
    try:
        mode = os.lstat(config_path).st_mode
    except FileNotFoundError:
        return {"commands": []}
    except OSError as exc:
        raise WorkflowError("Could not inspect official Trellis config for after_archive hooks.", exit_code=2) from exc
    if not stat.S_ISREG(mode):
        raise WorkflowError(
            "Official Trellis config must be a regular file before finish-work archive.",
            exit_code=2,
            payload={"path": ".trellis/config.yaml", "stage": "after-archive-hook-preflight"},
        )
    try:
        raw = config_path.read_bytes()
        content = raw.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise WorkflowError(
            "Official Trellis config is unreadable for after_archive hook preflight.",
            exit_code=2,
            payload={"path": ".trellis/config.yaml", "stage": "after-archive-hook-preflight"},
        ) from exc
    if b"\x00" in raw:
        raise WorkflowError(
            "Official Trellis config contains an invalid NUL byte.",
            exit_code=2,
            payload={"path": ".trellis/config.yaml", "stage": "after-archive-hook-preflight"},
        )

    parser_path = root / ".trellis/scripts/common/config.py"
    if not parser_path.is_file() or parser_path.is_symlink():
        raise WorkflowError(
            "Official Trellis config parser is unavailable for after_archive hook preflight.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight"},
        )
    parser = (
        "import json,sys; "
        "from common.config import parse_simple_yaml; "
        "print(json.dumps(parse_simple_yaml(open(sys.argv[1], encoding='utf-8').read())))"
    )
    proc = run(
        [sys.executable, "-c", parser, str(config_path)],
        cwd=root / ".trellis/scripts",
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Official Trellis config could not be parsed for after_archive hook preflight.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight"},
        )
    try:
        parsed = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise WorkflowError(
            "Official Trellis config parser returned invalid hook state.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight"},
        ) from exc
    if not isinstance(parsed, dict):
        raise WorkflowError("Official Trellis config root must be a mapping.", exit_code=2)
    hooks = parsed.get("hooks")
    declarations = len(re.findall(r"(?m)^[ \t]*after_archive[ \t]*:", content))
    if hooks is None:
        if declarations:
            raise WorkflowError(
                "Official after_archive hook declaration is outside a parseable hooks mapping.",
                exit_code=2,
                payload={"stage": "after-archive-hook-preflight"},
            )
        return {"commands": []}
    if not isinstance(hooks, dict) or declarations > 1:
        raise WorkflowError(
            "Official after_archive hook configuration is ambiguous or unparsable.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight"},
        )
    configured_present = "after_archive" in hooks
    if declarations != (1 if configured_present else 0):
        raise WorkflowError(
            "Official after_archive hook declaration is outside the parsed hooks mapping.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight"},
        )
    configured = hooks.get("after_archive", [])
    if configured in ({}, None):
        configured = []
    if not isinstance(configured, list) or any(not isinstance(item, str) for item in configured):
        raise WorkflowError(
            "Official after_archive hook configuration must be an empty command list for finish-work.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight"},
        )
    if configured:
        raise WorkflowError(
            "Guru Team finish-work does not support non-empty official after_archive hooks because they run after the task move.",
            exit_code=2,
            payload={
                "stage": "after-archive-hook-preflight",
                "configured_command_count": len(configured),
                "hook_executed": False,
            },
        )
    return {"commands": []}

def closeout_pr_placeholder(repo: str) -> dict[str, Any]:
    number = CLOSEOUT_PR_PLACEHOLDER_NUMBER
    return {
        "number": number,
        "url": f"https://github.com/{repo}/pull/{number}",
        "ref": f"PR #{number}",
    }

def render_closeout_summary_for_pr(plan: dict[str, Any], pr: dict[str, Any]) -> dict[str, Any]:
    number = pr.get("number")
    if (
        not isinstance(number, int)
        or isinstance(number, bool)
        or number < 1
        or number > CLOSEOUT_PR_PLACEHOLDER_NUMBER
    ):
        raise WorkflowError("Final projection PR number is invalid.", exit_code=2)
    expected_url = canonical_pull_request_url(plan["git"]["repo"], number, pr.get("url"))
    summary = copy.deepcopy(plan["projection"]["summary_template"])
    summary["github"]["pr_url"] = expected_url
    summary["index"]["search_terms"]["pr_refs"] = [f"PR #{number}"]
    summary["index"]["retrieval_text"] = current_finish_summary_retrieval_text(
        str(summary["task"]["title"]), summary["index"]
    )
    return summary

def closeout_summary_for_pr(plan: dict[str, Any], pr: dict[str, Any]) -> dict[str, Any]:
    summary = render_closeout_summary_for_pr(plan, pr)
    validate_finish_summary(summary)
    return summary

def closeout_json_artifact_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def closeout_summary_runtime_pr_facts_from_bytes(
    plan: dict[str, Any], content: bytes, *, expected_pr: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Bind runtime PR facts without invoking the general local summary validator."""
    try:
        summary = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError("Committed final summary is not deterministic UTF-8 JSON.", exit_code=2) from exc
    if not isinstance(summary, dict):
        raise WorkflowError("Committed final summary JSON root must be an object.", exit_code=2)
    github = summary.get("github")
    index = summary.get("index")
    search_terms = index.get("search_terms") if isinstance(index, dict) else None
    pr_url = github.get("pr_url") if isinstance(github, dict) else None
    try:
        pr_url, number = parse_canonical_pull_request_url(plan["git"]["repo"], pr_url)
    except WorkflowError as exc:
        raise WorkflowError(
            "Committed final summary PR URL is not canonical for the immutable repo.", exit_code=2
        ) from exc
    if not isinstance(search_terms, dict) or search_terms.get("pr_refs") != [f"PR #{number}"]:
        raise WorkflowError("Committed final summary PR ref does not match its canonical URL.", exit_code=2)
    runtime_pr = {"number": number, "url": pr_url}
    if expected_pr is not None:
        expected_number = expected_pr.get("number")
        if not isinstance(expected_number, int) or isinstance(expected_number, bool):
            raise WorkflowError("Expected final summary PR number is invalid.", exit_code=2)
        expected_url = canonical_pull_request_url(
            plan["git"]["repo"], expected_number, expected_pr.get("url")
        )
        if number != expected_number or pr_url != expected_url:
            raise WorkflowError(
                "Final summary runtime PR facts differ from the bound pull request.",
                exit_code=2,
            )
        runtime_pr = {"number": expected_number, "url": expected_url}
    expected_summary = render_closeout_summary_for_pr(plan, runtime_pr)
    expected_bytes = closeout_json_artifact_bytes(expected_summary)
    actual_digest = hashlib.sha256(content).hexdigest()
    expected_digest = hashlib.sha256(expected_bytes).hexdigest()
    if content != expected_bytes:
        raise WorkflowError(
            "Final summary bytes do not match the deterministic runtime PR projection.",
            exit_code=2,
            payload={
                "expected_summary_sha256": expected_digest,
                "actual_summary_sha256": actual_digest,
            },
        )
    return {
        "number": number,
        "url": str(pr_url),
        "summary_sha256": actual_digest,
    }

def closeout_summary_template_digest(plan: dict[str, Any], summary: dict[str, Any]) -> str:
    normalized = copy.deepcopy(summary)
    placeholder = plan["projection"]["summary_placeholder"]
    normalized["github"]["pr_url"] = placeholder["url"]
    normalized["index"]["search_terms"]["pr_refs"] = [placeholder["ref"]]
    normalized["index"]["retrieval_text"] = current_finish_summary_retrieval_text(
        str(normalized["task"]["title"]), normalized["index"]
    )
    return closeout_json_artifact_sha256(normalized)

def validate_closeout_final_summary(plan: dict[str, Any], summary: dict[str, Any]) -> None:
    validate_finish_summary(summary)
    pr_url = summary.get("github", {}).get("pr_url")
    try:
        _canonical_url, number = parse_canonical_pull_request_url(plan["git"]["repo"], pr_url)
    except WorkflowError as exc:
        raise WorkflowError(
            "Final summary PR URL does not match closeout repo identity.", exit_code=2
        ) from exc
    expected_ref = [f"PR #{number}"]
    if summary.get("index", {}).get("search_terms", {}).get("pr_refs") != expected_ref:
        raise WorkflowError("Final summary PR ref does not match canonical PR identity.", exit_code=2)
    actual = closeout_summary_template_digest(plan, summary)
    expected = plan["projection"]["summary_template_sha256"]
    if actual != expected:
        raise WorkflowError(
            "Final summary differs from the prevalidated closeout template.",
            exit_code=2,
            payload={"expected_template_sha256": expected, "actual_template_sha256": actual},
        )

def read_and_validate_closeout_final_summary(path: Path, plan: dict[str, Any]) -> dict[str, Any]:
    summary = read_json(path)
    expected_file_sha = closeout_json_artifact_sha256(summary)
    actual_file_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual_file_sha != expected_file_sha:
        raise WorkflowError(
            "Final summary bytes are not the exact deterministic JSON artifact encoding.",
            exit_code=2,
            payload={"expected_file_sha256": expected_file_sha, "actual_file_sha256": actual_file_sha},
        )
    validate_closeout_final_summary(plan, summary)
    return summary

def closeout_plan_digest(plan: dict[str, Any]) -> str:
    payload = copy.deepcopy(plan)
    payload.pop("plan_digest", None)
    return canonical_json_sha256(payload)

def closeout_archive_retained_paths(plan: dict[str, Any]) -> list[str]:
    move_paths = plan.get("projection", {}).get("move_paths", [])
    if not isinstance(move_paths, list):
        return []
    if plan.get("schema_version") != CLOSEOUT_PLAN_SCHEMA_VERSION:
        return []
    allowed = set(CLOSEOUT_ARCHIVE_CORE_ARTIFACTS)
    if CLOSEOUT_PLAN_ARTIFACT in move_paths:
        allowed.add(CLOSEOUT_PLAN_ARTIFACT)
    retained = sorted(
        set(move_paths) & allowed
    )
    return retained

def closeout_archive_pruned_paths(plan: dict[str, Any]) -> list[str]:
    move_paths = plan.get("projection", {}).get("move_paths", [])
    if not isinstance(move_paths, list):
        return []
    return sorted(set(move_paths) - set(closeout_archive_retained_paths(plan)))

def closeout_json_artifact_sha256(payload: dict[str, Any]) -> str:
    return hashlib.sha256(closeout_json_artifact_bytes(payload)).hexdigest()

def closeout_plan_errors(
    plan: Any,
    *,
    allow_legacy_migration: bool = False,
) -> list[str]:
    if not isinstance(plan, dict):
        return ["closeout plan must be an object."]
    expected = {
        "schema_version", "task", "git", "inputs", "review", "publish",
        "projection", "transitions", "plan_digest",
    }
    errors: list[str] = []
    if set(plan) != expected:
        errors.append("closeout plan top-level keys do not match a supported schema.")
    legacy_schema2 = (
        allow_legacy_migration
        and plan.get("schema_version") == LEGACY_CLOSEOUT_PLAN_SCHEMA_VERSION
    )
    if plan.get("schema_version") != CLOSEOUT_PLAN_SCHEMA_VERSION and not legacy_schema2:
        errors.append("closeout plan schema_version must match the current contract.")
    digest = str(plan.get("plan_digest") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != closeout_plan_digest(plan):
        errors.append("closeout plan digest does not match canonical content.")
    if plan.get("transitions") != CLOSEOUT_TRANSITIONS:
        errors.append("closeout plan transitions are invalid.")
    task = plan.get("task") if isinstance(plan.get("task"), dict) else {}
    git = plan.get("git") if isinstance(plan.get("git"), dict) else {}
    review = plan.get("review") if isinstance(plan.get("review"), dict) else {}
    publish = plan.get("publish") if isinstance(plan.get("publish"), dict) else {}
    projection = plan.get("projection") if isinstance(plan.get("projection"), dict) else {}
    projection_keys = {
        "active_locator", "archive_locator", "finish_summary_locator",
        "move_paths", "tracked_move_paths", "untracked_archive_outputs",
        "reviewed_tracked_bindings", "migration_predecessor_plan_digest",
        "summary_placeholder",
        "summary_template_sha256", "summary_template", "runtime_fact_fields",
        "retired_tracked_paths",
    }
    nested_keys = {
        "task": (task, {"id", "title", "source_issue", "active_locator", "archive_locator"}),
        "review": (review, {"branch_review_commit", "changed_paths", "close_issues_reviewed"}),
        "publish": (
            publish,
            {
                "title",
                "body_sha256" if legacy_schema2 else "body",
                "draft",
                "draft_to_ready",
                "match",
            },
        ),
        "projection": (
            projection,
            projection_keys,
        ),
    }
    for label, (value, keys) in nested_keys.items():
        legacy_projection_keys = (
            label == "projection"
            and allow_legacy_migration
            and set(value) == keys - {"retired_tracked_paths"}
        )
        if set(value) != keys and not legacy_projection_keys:
            errors.append(f"closeout plan {label} keys are invalid.")
    git_keys = {
        "repo", "remote", "base_branch", "head_branch", "branch_review_commit",
        "reviewed_content_head", "publication_head",
    }
    legacy_git = allow_legacy_migration and set(git) == {
        "repo", "remote", "base_branch", "head_branch", "branch_review_commit",
    }
    if set(git) != git_keys and not legacy_git:
        errors.append("closeout plan git keys are invalid.")
    for label, value in [
        ("task.active_locator", task.get("active_locator")),
        ("task.archive_locator", task.get("archive_locator")),
        ("projection.finish_summary_locator", projection.get("finish_summary_locator")),
    ]:
        errors.extend(finish_summary_path_errors(value, label))
    if not str(task.get("active_locator") or "").startswith(".trellis/tasks/"):
        errors.append("closeout task active locator is invalid.")
    if not str(task.get("archive_locator") or "").startswith(".trellis/tasks/archive/"):
        errors.append("closeout task archive locator is invalid.")
    if not isinstance(task.get("source_issue"), int) or isinstance(task.get("source_issue"), bool) or int(task.get("source_issue") or 0) < 1:
        errors.append("closeout task source_issue is invalid.")
    for key in ["repo", "remote", "base_branch", "head_branch"]:
        if not isinstance(git.get(key), str) or not str(git[key]).strip():
            errors.append(f"closeout git.{key} is invalid.")
    if normalize_github_repository(git.get("repo")) != git.get("repo"):
        errors.append("closeout git.repo must be a normalized GitHub owner/repository identity.")
    if not re.fullmatch(r"[0-9a-f]{40}", str(git.get("branch_review_commit") or "")):
        errors.append("closeout branch_review_commit is invalid.")
    reviewed_head = str(git.get("reviewed_content_head") or git.get("branch_review_commit") or "")
    publication_head = str(git.get("publication_head") or git.get("branch_review_commit") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", reviewed_head):
        errors.append("closeout reviewed_content_head is invalid.")
    if not re.fullmatch(r"[0-9a-f]{40}", publication_head):
        errors.append("closeout publication_head is invalid.")
    if reviewed_head != str(git.get("branch_review_commit") or ""):
        errors.append("closeout reviewed_content_head does not match branch_review_commit.")
    if review.get("branch_review_commit") != git.get("branch_review_commit"):
        errors.append("closeout review commit does not match git identity.")
    changed = review.get("changed_paths")
    if not isinstance(changed, list) or any(not isinstance(path, str) for path in changed) or changed != sorted(set(changed)):
        errors.append("closeout review changed paths must be sorted and unique.")
    reviewed_issues = review.get("close_issues_reviewed")
    if not isinstance(reviewed_issues, list) or any(not isinstance(number, int) or isinstance(number, bool) for number in reviewed_issues) or reviewed_issues != sorted(set(reviewed_issues)):
        errors.append("closeout reviewed close issues must be sorted and unique.")
    if publish.get("draft") is not True or publish.get("draft_to_ready") is not True:
        errors.append("closeout publish must use draft then ready.")
    if not isinstance(publish.get("title"), str) or not publish["title"].strip():
        errors.append("closeout publish title is invalid.")
    if legacy_schema2:
        if not re.fullmatch(r"[0-9a-f]{64}", str(publish.get("body_sha256") or "")):
            errors.append("legacy closeout publish body digest is invalid.")
    elif not isinstance(publish.get("body"), str) or not publish["body"].strip():
        errors.append("closeout publish body is invalid.")
    expected_match = {"repo": git.get("repo"), "head": git.get("head_branch"), "base": git.get("base_branch")}
    if publish.get("match") != expected_match:
        errors.append("closeout publish match identity does not match git identity.")
    if projection.get("active_locator") != task.get("active_locator") or projection.get("archive_locator") != task.get("archive_locator"):
        errors.append("closeout projection task locators do not match task identity.")
    if projection.get("finish_summary_locator") != f"{task.get('archive_locator')}/{FINISH_SUMMARY_ARTIFACT}":
        errors.append("closeout projection finish-summary locator is invalid.")
    move_paths = projection.get("move_paths")
    if (
        not isinstance(move_paths, list)
        or not move_paths
        or any(
            not isinstance(path, str)
            or bool(finish_summary_path_errors(path, "projection.move_paths[]"))
            for path in move_paths
        )
        or move_paths != sorted(set(move_paths))
    ):
        errors.append("closeout move paths must be a sorted unique task-relative file set.")
        move_paths = []
    tracked_move_paths = projection.get("tracked_move_paths")
    if (
        not isinstance(tracked_move_paths, list)
        or tracked_move_paths != sorted(set(tracked_move_paths))
        or any(path not in move_paths for path in tracked_move_paths)
    ):
        errors.append("closeout tracked move paths must be a sorted subset of move paths.")
        tracked_move_paths = []
    retired_tracked_paths = projection.get("retired_tracked_paths", [])
    if (
        not isinstance(retired_tracked_paths, list)
        or retired_tracked_paths != sorted(set(retired_tracked_paths))
        or any(
            not isinstance(path, str)
            or bool(finish_summary_path_errors(path, "projection.retired_tracked_paths[]"))
            for path in retired_tracked_paths
        )
        or set(retired_tracked_paths) - {CLOSEOUT_PLAN_ARTIFACT}
        or set(retired_tracked_paths) & set(move_paths)
    ):
        errors.append(
            "closeout retired tracked paths must be the disjoint historical closeout plan deletion set."
        )
        retired_tracked_paths = []
    untracked_archive_outputs = projection.get("untracked_archive_outputs")
    if (
        not isinstance(untracked_archive_outputs, list)
        or not untracked_archive_outputs
        or untracked_archive_outputs != sorted(set(untracked_archive_outputs))
        or any(path not in move_paths for path in untracked_archive_outputs)
    ):
        errors.append("closeout untracked archive outputs must be a sorted non-empty subset of move paths.")
        untracked_archive_outputs = []
    if (
        set(tracked_move_paths) & set(untracked_archive_outputs)
        or sorted(set(tracked_move_paths) | set(untracked_archive_outputs)) != move_paths
    ):
        errors.append("closeout tracked/untracked move classes must be disjoint and cover every move path.")
    if FINISH_SUMMARY_ARTIFACT not in untracked_archive_outputs:
        errors.append("closeout final summary must be classified as an untracked archive output.")
    reviewed_bindings = projection.get("reviewed_tracked_bindings")
    if not isinstance(reviewed_bindings, list):
        errors.append("closeout reviewed tracked bindings must be an array.")
        reviewed_bindings = []
    else:
        binding_paths: list[str] = []
        for index, binding in enumerate(reviewed_bindings):
            if not isinstance(binding, dict) or set(binding) != {"path", "mode", "sha256"}:
                errors.append(f"closeout reviewed tracked binding {index} is invalid.")
                continue
            path = binding.get("path")
            mode = binding.get("mode")
            digest_value = binding.get("sha256")
            if (
                not isinstance(path, str)
                or path not in tracked_move_paths
                or path == CLOSEOUT_PLAN_ARTIFACT
                or finish_summary_path_errors(path, f"projection.reviewed_tracked_bindings[{index}].path")
            ):
                errors.append(f"closeout reviewed tracked binding {index} path is invalid.")
            else:
                binding_paths.append(path)
            if mode not in {"100644", "100755"}:
                errors.append(f"closeout reviewed tracked binding {index} mode is invalid.")
            if re.fullmatch(r"[0-9a-f]{64}", str(digest_value or "")) is None:
                errors.append(f"closeout reviewed tracked binding {index} digest is invalid.")
        if binding_paths != sorted(set(binding_paths)):
            errors.append("closeout reviewed tracked binding paths must be sorted and unique.")
    migration_predecessor = projection.get("migration_predecessor_plan_digest")
    if (
        migration_predecessor is not None
        and re.fullmatch(r"[0-9a-f]{64}", str(migration_predecessor)) is None
    ):
        errors.append("closeout migration predecessor plan digest is invalid.")
    if migration_predecessor == digest:
        errors.append("closeout migration predecessor must differ from the current plan digest.")
    forbidden_finalizer_artifacts = {
        PR_READINESS_ARTIFACT,
        TASK_FINALIZATION_GATE_ARTIFACT,
    }
    if forbidden_finalizer_artifacts & set(move_paths):
        errors.append(
            "closeout plan must not move owner-private publication or finalization gates."
        )
    if legacy_schema2:
        legacy_retained = {
            *CLOSEOUT_ARCHIVE_CORE_ARTIFACTS,
            CLOSEOUT_PLAN_ARTIFACT,
        }
        retained_paths = sorted(set(move_paths) & legacy_retained)
    else:
        retained_paths = closeout_archive_retained_paths(plan)
    required_retained = {FINISH_SUMMARY_ARTIFACT}
    if CLOSEOUT_PLAN_ARTIFACT in move_paths:
        required_retained.add(CLOSEOUT_PLAN_ARTIFACT)
    if not required_retained.issubset(retained_paths):
        errors.append("closeout archive is missing required recovery artifacts.")
    archive_limit = (
        CLOSEOUT_ARCHIVE_LEGACY_MAX_ARTIFACTS
        if CLOSEOUT_PLAN_ARTIFACT in move_paths
        else CLOSEOUT_ARCHIVE_MAX_ARTIFACTS
    )
    if len(retained_paths) > archive_limit:
        errors.append("closeout archive exceeds the long-term artifact budget.")
    placeholder = projection.get("summary_placeholder")
    expected_placeholder = closeout_pr_placeholder(str(git.get("repo") or "invalid/invalid"))
    if placeholder != expected_placeholder:
        errors.append("closeout summary PR placeholder is invalid.")
    if projection.get("runtime_fact_fields") != CLOSEOUT_SUMMARY_RUNTIME_FACT_FIELDS:
        errors.append("closeout summary runtime fact fields are invalid.")
    template = projection.get("summary_template")
    template_digest = str(projection.get("summary_template_sha256") or "")
    if not isinstance(template, dict):
        errors.append("closeout summary template must be an object.")
    else:
        template_errors = finish_summary_errors(template)
        if template_errors:
            errors.extend(f"closeout summary template: {error}" for error in template_errors)
        if template.get("github", {}).get("pr_url") != expected_placeholder["url"]:
            errors.append("closeout summary template PR URL must equal the deterministic placeholder.")
        if template.get("index", {}).get("search_terms", {}).get("pr_refs") != [expected_placeholder["ref"]]:
            errors.append("closeout summary template PR ref must equal the deterministic placeholder.")
        if template.get("task", {}).get("archive_dir") != task.get("archive_locator"):
            errors.append("closeout summary template archive locator is invalid.")
        template_artifacts = set(template.get("artifacts", {}).values()) if isinstance(template.get("artifacts"), dict) else set()
        if not template_artifacts.issubset(set(retained_paths)):
            errors.append("closeout summary template artifacts are outside the retained archive set.")
        if not re.fullmatch(r"[0-9a-f]{64}", template_digest) or template_digest != closeout_json_artifact_sha256(template):
            errors.append("closeout summary template digest does not match canonical content.")
    inputs = plan.get("inputs")
    if not isinstance(inputs, dict) or not inputs:
        errors.append("closeout inputs must be a non-empty object.")
    else:
        required_inputs = {
            "task",
            "issue_scope_ledger",
            "official_after_archive_hooks",
        }
        if legacy_schema2:
            required_inputs.update({"pr_body", "finish_summary_index"})
        if not required_inputs.issubset(inputs):
            errors.append("closeout inputs are missing required direct-consumer facts.")
        if "task_context" in inputs or "review_gate" in inputs:
            errors.append("closeout plan must not persist producer-private runtime identity.")
        for key, item in inputs.items():
            if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
                errors.append(f"closeout input {key} is invalid.")
            elif not re.fullmatch(r"[0-9a-f]{64}", str(item.get("sha256") or "")):
                errors.append(f"closeout input {key} digest is invalid.")
            else:
                errors.extend(finish_summary_path_errors(item.get("path"), f"inputs.{key}.path"))
    return errors

def validate_closeout_plan(plan: Any) -> dict[str, Any]:
    errors = closeout_plan_errors(plan)
    if errors:
        raise WorkflowError("closeout-plan validation failed.", exit_code=2, payload={"errors": errors})
    return plan

def validate_closeout_plan_for_migration(plan: Any) -> dict[str, Any]:
    errors = closeout_plan_errors(plan, allow_legacy_migration=True)
    if errors:
        raise WorkflowError(
            "closeout-plan migration input validation failed.",
            exit_code=2,
            payload={"errors": errors},
        )
    return plan

def closeout_live_move_classes(
    root: Path,
    active_locator: str,
    move_paths: list[str],
) -> tuple[list[str], list[str]]:
    tracked: list[str] = []
    for relative in move_paths:
        repo_path = f"{active_locator}/{relative}"
        _blob, mode = task_commit_index_identity(root, repo_path)
        if mode is None:
            continue
        if mode not in {"100644", "100755"}:
            raise WorkflowError(
                "Closeout tracked move paths must be regular Git index entries.",
                exit_code=2,
                payload={"path": relative, "mode": mode},
            )
        tracked.append(relative)
    tracked_move_paths = sorted(tracked)
    untracked_archive_outputs = sorted(set(move_paths) - set(tracked_move_paths))
    return tracked_move_paths, untracked_archive_outputs

def closeout_reviewed_tracked_binding_map(
    plan: dict[str, Any],
) -> dict[str, dict[str, str]]:
    bindings = plan.get("projection", {}).get("reviewed_tracked_bindings", [])
    if not isinstance(bindings, list):
        return {}
    return {
        str(binding["path"]): binding
        for binding in bindings
        if isinstance(binding, dict)
        and set(binding) == {"path", "mode", "sha256"}
        and isinstance(binding.get("path"), str)
    }

def build_closeout_reviewed_tracked_bindings(
    root: Path,
    active_locator: str,
    tracked_move_paths: list[str],
    transaction_parent: str,
) -> list[dict[str, str]]:
    bindings: list[dict[str, str]] = []
    for relative in tracked_move_paths:
        # The immutable plan binds its own canonical bytes through plan_digest.
        if relative == CLOSEOUT_PLAN_ARTIFACT:
            continue
        repo_path = f"{active_locator}/{relative}"
        parent_mode, object_type, _object_id = closeout_commit_tree_entry(
            root,
            transaction_parent,
            repo_path,
        )
        if object_type != "blob" or parent_mode not in {"100644", "100755"}:
            raise WorkflowError(
                "Closeout tracked move paths must resolve to regular transaction-parent blobs.",
                exit_code=2,
                payload={"path": relative, "mode": parent_mode, "type": object_type},
            )
        content, content_sha256, working_mode = task_commit_worktree_content(
            root,
            repo_path,
        )
        if (
            content is None
            or content_sha256 is None
            or working_mode not in {"100644", "100755"}
        ):
            raise WorkflowError(
                "Closeout tracked move path is not a readable regular working-tree file.",
                exit_code=2,
                payload={"path": relative},
            )
        parent_content = closeout_commit_blob_bytes(
            root,
            transaction_parent,
            repo_path,
        )
        if working_mode != parent_mode or content != parent_content:
            bindings.append(
                {
                    "path": relative,
                    "mode": working_mode,
                    "sha256": content_sha256,
                }
            )
    return bindings

def build_closeout_plan(
    root: Path,
    task_dir: Path,
    task_context: dict[str, Any],
    task: dict[str, Any],
    ledger: dict[str, Any],
    *,
    repo: str,
    remote: str,
    base_branch: str,
    head_branch: str,
    branch_review_commit: str,
    title: str,
    body: str,
    review_facts: dict[str, Any] | None = None,
    include_closeout_plan: bool = True,
    allow_existing_summary: bool = False,
    existing_plan_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(review_facts, dict):
        raise WorkflowError(
            "Current closeout requires reviewed Publication facts.",
            exit_code=2,
        )
    reviewed_paths = list(review_facts["changed_paths"])
    active_locator = repo_relative(root, task_dir)
    existing_plan_path = closeout_plan_path(task_dir)
    existing_plan = copy.deepcopy(existing_plan_override) if existing_plan_override else (
        read_json(existing_plan_path)
        if include_closeout_plan and existing_plan_path.is_file()
        else {}
    )
    if existing_plan:
        validate_closeout_plan_for_migration(existing_plan)
    legacy_plan = (
        existing_plan.get("schema_version") == LEGACY_CLOSEOUT_PLAN_SCHEMA_VERSION
    )
    plan_schema_version = CLOSEOUT_PLAN_SCHEMA_VERSION
    existing_task = existing_plan.get("task") if isinstance(existing_plan.get("task"), dict) else {}
    existing_projection = (
        existing_plan.get("projection")
        if isinstance(existing_plan.get("projection"), dict)
        else {}
    )
    archive_month_now = current_archive_month()
    existing_archive_month = (
        closeout_archive_month(existing_plan) if existing_plan else None
    )
    same_archive_month = existing_archive_month == archive_month_now
    archive_locator = str(existing_task.get("archive_locator") or "")
    if archive_locator and not same_archive_month:
        archive_locator = f".trellis/tasks/archive/{archive_month_now}/{task_dir.name}"
    if not archive_locator:
        archive_locator = f".trellis/tasks/archive/{archive_month_now}/{task_dir.name}"
    assert_closeout_archive_path_preflight(root, archive_locator)
    observed_task_files = {
        path.relative_to(task_dir).as_posix()
        for path in task_dir.rglob("*")
        if path.is_file()
    }
    active_prefix = f"{active_locator}/"
    observed_task_files.update(
        path.removeprefix(active_prefix)
        for path in git_status_paths(root)
        if path.startswith(active_prefix)
    )
    retired_tracked_paths: list[str] = []
    historical_plan_relative = f"{active_locator}/{CLOSEOUT_PLAN_ARTIFACT}"
    if (
        not include_closeout_plan
        and CLOSEOUT_PLAN_ARTIFACT in observed_task_files
    ):
        if os.path.lexists(existing_plan_path):
            raise WorkflowError(
                "Current Finalizer requires the retired closeout plan to remain absent.",
                exit_code=2,
                payload={"path": historical_plan_relative},
            )
        if run(
            ["git", "ls-files", "--error-unmatch", "--", historical_plan_relative],
            cwd=root,
            check=False,
        ).returncode != 0:
            raise WorkflowError(
                "Current Finalizer found an unowned closeout plan status path.",
                exit_code=2,
                payload={"path": historical_plan_relative},
            )
        retired_tracked_paths = [CLOSEOUT_PLAN_ARTIFACT]
        observed_task_files.remove(CLOSEOUT_PLAN_ARTIFACT)
    if existing_projection:
        task_files = set(existing_projection.get("move_paths", []))
        unexpected_task_files = sorted(observed_task_files - task_files)
        if unexpected_task_files:
            raise WorkflowError(
                "Persisted closeout plan does not own newly added task artifacts.",
                exit_code=2,
                payload={"unexpected_task_files": unexpected_task_files},
            )
    else:
        if (
            (task_dir / FINISH_SUMMARY_ARTIFACT).exists()
            and not allow_existing_summary
        ):
            raise WorkflowError(
                "Initial closeout prepare found a stale final summary before the immutable plan existed.",
                exit_code=2,
            )
        task_files = set(observed_task_files)
        task_files.add(FINISH_SUMMARY_ARTIFACT)
        if include_closeout_plan:
            task_files.add(CLOSEOUT_PLAN_ARTIFACT)
    move_paths = sorted(task_files)
    tracked_move_paths, untracked_archive_outputs = closeout_live_move_classes(
        root,
        active_locator,
        move_paths,
    )
    binding_paths = [
        path
        for path in tracked_move_paths
        if not (legacy_plan and path in LEGACY_CLOSEOUT_RETIRED_ARTIFACTS)
    ]
    reviewed_tracked_bindings = build_closeout_reviewed_tracked_bindings(
        root,
        active_locator,
        binding_paths,
        branch_review_commit,
    )
    migration_predecessor_plan_digest: str | None = None
    if same_archive_month and existing_plan:
        if existing_plan.get("schema_version") == LEGACY_CLOSEOUT_PLAN_SCHEMA_VERSION:
            migration_predecessor_plan_digest = str(existing_plan["plan_digest"])
        elif "migration_predecessor_plan_digest" in existing_projection:
            migration_predecessor_plan_digest = existing_projection.get(
                "migration_predecessor_plan_digest"
            )
    retained_names = set(CLOSEOUT_ARCHIVE_CORE_ARTIFACTS)
    retained_archive_paths = sorted(set(move_paths) & retained_names)
    transaction_paths = sorted(
        {f"{active_locator}/{name}" for name in tracked_move_paths}
        | {f"{active_locator}/{name}" for name in retired_tracked_paths}
        | {f"{archive_locator}/{name}" for name in retained_archive_paths}
    )
    ledger_path = issue_scope_ledger_path(task_dir)
    inputs = {
        "task": closeout_input_record(root, task_dir / "task.json"),
        "issue_scope_ledger": closeout_input_record(root, ledger_path),
        "official_after_archive_hooks": closeout_input_record(
            root,
            root / ".trellis/config.yaml",
            payload=official_after_archive_hook_state(root),
        ),
    }
    config_path = root / ".trellis/guru-team/config.yml"
    if config_path.is_file():
        inputs["guru_team_config"] = closeout_input_record(root, config_path)
    source_issue = primary_issue_number_from_ledger(ledger)
    placeholder = closeout_pr_placeholder(repo)
    existing_summary_template = (
        existing_projection.get("summary_template")
        if isinstance(existing_projection.get("summary_template"), dict)
        else {}
    )
    generated_at = str(
        existing_summary_template.get("generated_at")
        or ""
    )
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", generated_at):
        commit_time = run_stdout(
            ["git", "show", "-s", "--format=%cI", branch_review_commit],
            cwd=root,
        )
        try:
            generated_at = (
                datetime.fromisoformat(commit_time)
                .astimezone(timezone.utc)
                .strftime("%Y-%m-%dT%H:%M:%SZ")
            )
        except ValueError as exc:
            raise WorkflowError(
                "Reviewed content commit time is invalid for the deterministic final-summary projection.",
                exit_code=2,
            ) from exc
    projected_artifacts = {
        key: filename
        for key, filename in CURRENT_FINISH_SUMMARY_ARTIFACT_FILES.items()
        if filename in retained_archive_paths
    }
    summary_template = build_finish_summary(
        root,
        task_dir,
        task_context,
        ledger,
        body,
        branch_review_commit,
        pr_url=placeholder["url"],
        changed_paths=sorted(set(reviewed_paths) | set(transaction_paths)),
        archive_dir_override=archive_locator,
        generated_at_override=generated_at,
        artifacts_override=projected_artifacts,
    )
    try:
        publication_head = current_head(root)
    except WorkflowError:
        publication_head = branch_review_commit
    if re.fullmatch(r"[0-9a-f]{40}", publication_head) is None:
        publication_head = branch_review_commit
    plan: dict[str, Any] = {
        "schema_version": plan_schema_version,
        "task": {
            "id": str(task.get("id") or task.get("name") or task_dir.name),
            "title": str(task.get("title") or task.get("name") or task_dir.name),
            "source_issue": source_issue,
            "active_locator": active_locator,
            "archive_locator": archive_locator,
        },
        "git": {
            "repo": repo,
            "remote": remote,
            "base_branch": normalize_ref(base_branch).removeprefix("origin/"),
            "head_branch": head_branch,
            "branch_review_commit": branch_review_commit,
            "reviewed_content_head": branch_review_commit,
            "publication_head": publication_head,
        },
        "inputs": inputs,
        "review": {
            "branch_review_commit": branch_review_commit,
            "changed_paths": reviewed_paths,
            "close_issues_reviewed": sorted(
                set(issue_numbers(ledger.get("close_issues")))
            ),
        },
        "publish": {
            "title": title,
            "body": body,
            "draft": True,
            "draft_to_ready": True,
            "match": {"repo": repo, "head": head_branch, "base": normalize_ref(base_branch).removeprefix("origin/")},
        },
        "projection": {
            "active_locator": active_locator,
            "archive_locator": archive_locator,
            "finish_summary_locator": f"{archive_locator}/{FINISH_SUMMARY_ARTIFACT}",
            "move_paths": move_paths,
            "tracked_move_paths": tracked_move_paths,
            "retired_tracked_paths": retired_tracked_paths,
            "untracked_archive_outputs": untracked_archive_outputs,
            "reviewed_tracked_bindings": reviewed_tracked_bindings,
            "migration_predecessor_plan_digest": migration_predecessor_plan_digest,
            "summary_placeholder": placeholder,
            "summary_template_sha256": closeout_json_artifact_sha256(summary_template),
            "summary_template": summary_template,
            "runtime_fact_fields": list(CLOSEOUT_SUMMARY_RUNTIME_FACT_FIELDS),
        },
        "transitions": list(CLOSEOUT_TRANSITIONS),
        "plan_digest": "",
    }
    plan["plan_digest"] = closeout_plan_digest(plan)
    return validate_closeout_plan(plan)

def closeout_schema2_migration_errors(
    previous: dict[str, Any],
    current: dict[str, Any],
) -> list[str]:
    try:
        validate_closeout_plan_for_migration(previous)
        validate_closeout_plan(current)
    except WorkflowError as exc:
        return [str(exc)]
    errors: list[str] = []
    if previous.get("schema_version") != LEGACY_CLOSEOUT_PLAN_SCHEMA_VERSION:
        return ["schema 2.0 migration requires one legacy plan"]
    for key in ("task", "review", "transitions"):
        if previous.get(key) != current.get(key):
            errors.append(f"schema 2.0 migration changed protected {key} facts")

    previous_git = copy.deepcopy(previous.get("git", {}))
    current_git = copy.deepcopy(current.get("git", {}))
    if set(previous_git) == {
        "repo", "remote", "base_branch", "head_branch", "branch_review_commit",
    }:
        previous_git["reviewed_content_head"] = previous_git["branch_review_commit"]
        previous_git["publication_head"] = previous_git["branch_review_commit"]
    if previous_git.get("publication_head") != current_git.get("publication_head"):
        previous_git.pop("publication_head", None)
        current_git.pop("publication_head", None)
    if previous_git != current_git:
        errors.append("schema 2.0 migration changed protected git identity facts")

    previous_publish = previous.get("publish", {})
    current_publish = current.get("publish", {})
    if (
        previous_publish.get("title") != current_publish.get("title")
        or previous_publish.get("draft") != current_publish.get("draft")
        or previous_publish.get("draft_to_ready")
        != current_publish.get("draft_to_ready")
        or previous_publish.get("match") != current_publish.get("match")
        or hashlib.sha256(
            str(current_publish.get("body") or "").encode("utf-8")
        ).hexdigest()
        != previous_publish.get("body_sha256")
    ):
        errors.append("schema 2.0 migration PR payload does not match Publication 4.0")

    expected_inputs = {
        key: value
        for key, value in previous.get("inputs", {}).items()
        if key not in {"pr_body", "finish_summary_index"}
    }
    if current.get("inputs") != expected_inputs:
        errors.append("schema 2.0 migration changed protected live input facts")

    previous_projection = previous["projection"]
    current_projection = current["projection"]
    if current_projection.get("migration_predecessor_plan_digest") != previous.get("plan_digest"):
        errors.append(
            "schema 2.0 migration predecessor digest does not bind the legacy plan"
        )
    for key in (
        "active_locator",
        "archive_locator",
        "finish_summary_locator",
        "move_paths",
        "summary_placeholder",
        "runtime_fact_fields",
    ):
        if previous_projection.get(key) != current_projection.get(key):
            errors.append(f"schema 2.0 migration changed protected projection.{key}")

    return errors

def finalizer_tracked_legacy_closeout_plan(
    root: Path,
    task_dir: Path,
) -> dict[str, Any] | None:
    """Load only an exact committed schema-2 plan eligible for Finalizer recovery."""
    path = closeout_plan_path(task_dir)
    if not path.is_file() or path.is_symlink():
        return None
    relative = repo_relative(root, path)
    if run(
        ["git", "ls-files", "--error-unmatch", "--", relative],
        cwd=root,
        check=False,
    ).returncode != 0:
        return None
    working = validate_closeout_plan_for_migration(read_json(path))
    if working.get("schema_version") != LEGACY_CLOSEOUT_PLAN_SCHEMA_VERSION:
        return None
    committed_bytes = ai_first_git_blob_contents(
        root,
        {relative: f"HEAD:{relative}"},
    ).get(relative)
    if committed_bytes is None:
        raise WorkflowError(
            "Tracked legacy closeout plan is missing from committed HEAD.",
            exit_code=2,
            payload={"reason_code": "legacy_closeout_plan_head_missing"},
        )
    if path.read_bytes() != committed_bytes:
        raise WorkflowError(
            "Tracked legacy closeout plan differs from its committed HEAD bytes.",
            exit_code=2,
            payload={"reason_code": "legacy_closeout_plan_worktree_drift"},
        )
    return working

def resolve_closeout_branch_review_commit(
    task_ref: str,
    *,
    publication_ready: dict[str, Any] | None,
    existing_plan: dict[str, Any] | None,
    allow_base_evolution_supersession: bool = False,
) -> str:
    if existing_plan is not None and not allow_base_evolution_supersession:
        plan_task_ref = str(existing_plan.get("task", {}).get("active_locator") or "")
        branch_review_commit = str(
            existing_plan.get("git", {}).get("branch_review_commit") or ""
        )
        if plan_task_ref != task_ref:
            raise WorkflowError(
                "Persisted closeout plan does not match the current task.",
                exit_code=2,
            )
    else:
        if publication_ready is None:
            raise WorkflowError(
                "Initial closeout requires a Publication ready DTO or immutable plan.",
                exit_code=2,
            )
        branch_review_commit = str(
            publication_ready.get("branch_review_commit") or ""
        )

    publication_mismatch = publication_ready is not None and (
        publication_ready.get("profile") != "publication_ready"
        or publication_ready.get("task_ref") != task_ref
        or publication_ready.get("branch_review_commit") != branch_review_commit
    )
    if (
        publication_ready is not None
        and existing_plan is not None
        and not allow_base_evolution_supersession
    ):
        publish = existing_plan.get("publish", {})
        payload_title = publication_ready.get("pr_title")
        payload_body = publication_ready.get("pr_body")
        if (
            existing_plan.get("schema_version")
            == LEGACY_CLOSEOUT_PLAN_SCHEMA_VERSION
        ):
            publication_mismatch = publication_mismatch or (
                payload_title != publish.get("title")
                or not isinstance(payload_body, str)
                or hashlib.sha256(payload_body.encode("utf-8")).hexdigest()
                != publish.get("body_sha256")
            )
        else:
            publication_mismatch = publication_mismatch or (
                payload_title != publish.get("title")
                or payload_body != publish.get("body")
            )
    if publication_mismatch:
        raise WorkflowError(
            "Finalizer Publication ready DTO does not match the current task or immutable plan.",
            exit_code=2,
        )
    if re.fullmatch(r"[0-9a-f]{40}", branch_review_commit) is None:
        raise WorkflowError(
            "Finalizer branch_review_commit is invalid.",
            exit_code=2,
        )
    return branch_review_commit

def prepare_closeout(
    root: Path,
    args: argparse.Namespace,
    config: dict[str, Any],
    task_dir: Path,
    task_context: dict[str, Any],
    *,
    publication_ready: dict[str, Any] | None = None,
    allowed_current_gate: dict[str, Any] | None = None,
    current_finalizer: bool = False,
) -> dict[str, Any]:
    official_after_archive_hook_state(root)
    existing_plan_path = closeout_plan_path(task_dir)
    legacy_finalizer_plan = (
        finalizer_tracked_legacy_closeout_plan(root, task_dir)
        if current_finalizer
        else None
    )
    existing_plan = (
        legacy_finalizer_plan
        if current_finalizer
        else (
            validate_closeout_plan_for_migration(read_json(existing_plan_path))
            if existing_plan_path.is_file()
            and not existing_plan_path.is_symlink()
            else None
        )
    )
    expected_task_ref = repo_relative(root, task_dir)
    base_evolution_supersession: dict[str, Any] | None = None
    publication_commit = str(
        publication_ready.get("branch_review_commit") or ""
    ) if publication_ready is not None else ""
    target_repo = normalize_github_repository(
        str(args.repo or config.get("github_repo") or "").strip()
        or infer_github_repo(root)
    )
    if (
        existing_plan is not None
        and publication_ready is not None
        and publication_commit
        != str(existing_plan.get("git", {}).get("branch_review_commit") or "")
    ):
        prospective_git = {
            "repo": target_repo,
            "remote": str(args.remote or publish_config(config).get("remote") or "origin"),
            "base_branch": base_branch_from_sources(args, task_json(task_dir), task_context),
            "head_branch": current_branch(root),
            "branch_review_commit": publication_commit,
            "reviewed_content_head": publication_commit,
            "publication_head": current_head(root),
        }
        prospective_plan = {
            "schema_version": CLOSEOUT_PLAN_SCHEMA_VERSION,
            "task": {
                "active_locator": expected_task_ref,
                "archive_locator": str(existing_plan.get("task", {}).get("archive_locator") or ""),
            },
            "git": prospective_git,
        }
        existing_git = (
            existing_plan.get("git")
            if isinstance(existing_plan.get("git"), dict)
            else {}
        )
        if "publication_head" in existing_git:
            base_evolution_supersession = (
                finalizer_current_plan_base_evolution_supersession_preflight(
                    root,
                    task_dir,
                    existing_plan,
                    prospective_plan,
                    allowed_gate=allowed_current_gate,
                )
            )
        else:
            base_evolution_supersession = (
                finalizer_pre_pr_base_evolution_supersession_preflight(
                    root,
                    task_dir,
                    existing_plan,
                    prospective_plan,
                )
            )
    branch_review_commit = resolve_closeout_branch_review_commit(
        expected_task_ref,
        publication_ready=publication_ready,
        existing_plan=existing_plan,
        allow_base_evolution_supersession=base_evolution_supersession is not None,
    )
    validate_closeout_reviewed_content(
        root,
        {"git": {"branch_review_commit": branch_review_commit}},
        current_head(root),
        include_worktree=True,
    )
    publication_identity = finalizer_publication_identity(
        root,
        branch_review_commit,
        target_repo,
    )
    review_facts = closeout_reviewed_change_facts(
        root,
        task_context,
        branch_review_commit,
    )
    ledger = load_issue_scope_ledger(task_dir, task_context)
    dirty_paths = finalizer_unreviewed_dirty_paths(
        root,
        task_dir,
    )
    if dirty_paths:
        raise WorkflowError(
            "Working tree has uncommitted reviewed content. Commit reviewed task work before finish-work.",
            exit_code=2,
            payload={"dirty_paths": dirty_paths},
        )
    ledger_errors = validate_ledger_for_publish(ledger)
    if ledger_errors:
        raise WorkflowError("Issue Scope Ledger is incomplete for closeout.", exit_code=2, payload={"errors": ledger_errors})
    if (
        existing_plan is not None
        and existing_plan.get("schema_version") == "3.0"
        and base_evolution_supersession is None
    ):
        title = str(existing_plan["publish"]["title"])
        body = str(existing_plan["publish"]["body"])
    elif publication_ready is not None:
        title = str(publication_ready.get("pr_title") or "")
        body = str(publication_ready.get("pr_body") or "")
    else:
        raise WorkflowError(
            "Initial closeout requires the Publication 4.0 exact PR payload.",
            exit_code=2,
        )
    body_errors = validate_pr_body_quality(body, ledger, False)
    if not title.strip():
        body_errors.append("PR title is empty.")
    if body_errors:
        raise WorkflowError(
            "finish-work blocked because PR readiness evidence is incomplete.",
            exit_code=2,
            payload={"errors": body_errors},
        )
    task = task_json(task_dir)
    if task.get("status") != "in_progress":
        raise WorkflowError(
            "Initial or resumed closeout preparation requires task status=in_progress.",
            exit_code=2,
        )
    validate_closeout_task_children(task_dir, task)
    repo = normalize_github_repository(
        str(args.repo or config.get("github_repo") or "").strip() or infer_github_repo(root)
    )
    if not repo:
        raise WorkflowError("Could not resolve GitHub repo for closeout plan.", exit_code=2)
    base = base_branch_from_sources(args, task, task_context)
    branch = current_branch(root)
    remote = str(args.remote or publish_config(config).get("remote") or "origin")
    validate_github_remote_repository(root, remote, repo)
    plan = build_closeout_plan(
        root, task_dir, task_context, task, ledger,
        repo=repo, remote=remote, base_branch=base, head_branch=branch,
        branch_review_commit=branch_review_commit, title=title, body=body,
        review_facts=review_facts,
        include_closeout_plan=not current_finalizer,
        allow_existing_summary=current_finalizer,
        existing_plan_override=legacy_finalizer_plan,
    )
    month_supersession: dict[str, Any] | None = None
    pre_pr_reprepare: dict[str, Any] | None = None
    migration_normalization: dict[str, Any] | None = None
    existing = closeout_plan_path(task_dir)
    if current_finalizer and legacy_finalizer_plan is not None:
        migration_errors = closeout_schema2_migration_errors(
            legacy_finalizer_plan,
            plan,
        )
        if migration_errors:
            raise WorkflowError(
                "Tracked legacy closeout plan is not an exact current-plan migration predecessor.",
                exit_code=2,
                payload={"migration_errors": migration_errors},
            )
        migration_normalization = {"previous_plan": legacy_finalizer_plan}
    elif not current_finalizer and existing.is_file():
        persisted = validate_closeout_plan_for_migration(read_json(existing))
        if persisted != plan:
            migration_errors = closeout_schema2_migration_errors(persisted, plan)
            if base_evolution_supersession is not None:
                pre_pr_reprepare = {
                    "previous_plan": persisted,
                    "prior_state": "content_pushed",
                    "base_evolution": base_evolution_supersession,
                }
            elif not migration_errors:
                migration_normalization = {"previous_plan": persisted}
            else:
                persisted_git = persisted.get("git", {})
                plan_git = plan.get("git", {})
                provenance_only = (
                    persisted_git.get("repo") == plan_git.get("repo")
                    and persisted_git.get("remote") == plan_git.get("remote")
                    and persisted_git.get("base_branch") == plan_git.get("base_branch")
                    and persisted_git.get("head_branch") == plan_git.get("head_branch")
                    and persisted_git.get("branch_review_commit")
                    == plan_git.get("branch_review_commit")
                    and persisted_git.get("publication_head")
                    != plan_git.get("publication_head")
                    and plan_git.get("publication_head") == current_head(root)
                    and publication_identity.get("metadata_tail") is not None
                    and not (task_dir / FINISH_SUMMARY_ARTIFACT).exists()
                )
                if provenance_only:
                    pre_pr_reprepare = {
                        "previous_plan": persisted,
                        "prior_state": "content_pushed",
                    }
                if pre_pr_reprepare is None:
                    previous_month = closeout_archive_month(persisted)
                    next_month = closeout_archive_month(plan)
                    supersession_errors = closeout_month_supersession_errors(persisted, plan)
                    if (
                        previous_month == next_month
                        or task.get("status") != "in_progress"
                        or (root / persisted["task"]["archive_locator"]).exists()
                        or supersession_errors
                    ):
                        raise WorkflowError(
                            "Persisted closeout plan no longer matches protected inputs.",
                            exit_code=2,
                            payload={
                                "persisted_digest": persisted.get("plan_digest"),
                                "rebuilt_digest": plan.get("plan_digest"),
                                "migration_errors": migration_errors,
                                "month_supersession_errors": supersession_errors,
                            },
                        )
                    prior_state = resolve_closeout_pre_draft_state(
                        root,
                        task_dir,
                        persisted,
                        ledger,
                    )
                    if prior_state != "content_pushed":
                        raise WorkflowError(
                            "Stale-month plan has no unique current-contract reprepare state.",
                            exit_code=2,
                            payload={"state": prior_state},
                        )
                    month_supersession = {
                        "previous_plan": persisted,
                        "previous_month": previous_month,
                        "current_month": next_month,
                        "prior_state": prior_state,
                    }
        else:
            plan = persisted
    return {
        "plan": plan,
        "plan_digest": plan["plan_digest"],
        "task": task,
        "task_context": task_context,
        "ledger": ledger,
        "body": body,
        "month_supersession": month_supersession,
        "pre_pr_reprepare": pre_pr_reprepare,
        "migration_normalization": migration_normalization,
        "reviewed_content_head": publication_identity["reviewed_content_head"],
        "publication_head": publication_identity["publication_head"],
        "metadata_tail": publication_identity["metadata_tail"],
    }

def resolve_closeout_pre_draft_state(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    ledger: dict[str, Any],
    *,
    require_plan_artifact: bool = True,
) -> str:
    plan_path = closeout_plan_path(task_dir)
    if require_plan_artifact and not plan_path.exists():
        return "prepared"
    if require_plan_artifact and (not plan_path.is_file() or plan_path.is_symlink()):
        raise WorkflowError("Interrupted closeout plan is unavailable or unsafe.", exit_code=2)
    if require_plan_artifact and validate_closeout_plan_for_migration(read_json(plan_path)) != plan:
        raise WorkflowError(
            "Interrupted closeout plan differs from the rebuilt immutable plan.",
            exit_code=2,
        )
    if not closeout_ledger_matches_plan_bytes(root, task_dir, plan, ledger):
        raise WorkflowError(
            "Issue Scope Ledger bytes differ from the immutable closeout plan.",
            exit_code=2,
        )
    branch_review_commit = str(plan["git"]["branch_review_commit"])
    anchor_identity = reviewed_content_identity(
        root,
        branch_review_commit,
        include_worktree=False,
    )["sha256"]
    continuity_errors = review_branch_content_continuity_errors(
        root,
        task_dir,
        branch_review_commit,
        anchor_identity,
        current_head(root),
    )
    if continuity_errors:
        raise WorkflowError(
            "Closeout reviewed content is stale.",
            exit_code=2,
            payload={"errors": continuity_errors},
        )
    if not require_plan_artifact:
        publication_head = str(
            plan["git"].get("publication_head")
            or plan["git"]["branch_review_commit"]
        )
        remote_head = closeout_remote_branch_head(root, plan)
        if remote_head != publication_head:
            return "prepared"
    return "content_pushed"

def closeout_remote_branch_head(root: Path, plan: dict[str, Any]) -> str:
    proc = run(
        ["git", "ls-remote", "--heads", plan["git"]["remote"], plan["git"]["head_branch"]],
        cwd=root,
        check=False,
    )
    rows = [line.split() for line in proc.stdout.splitlines() if line.strip()]
    if proc.returncode != 0 or len(rows) > 1:
        raise WorkflowError("Could not resolve the unique closeout remote branch HEAD.", exit_code=2)
    return rows[0][0] if rows else ""

def push_closeout_branch_if_needed(root: Path, plan: dict[str, Any]) -> bool:
    local_head = current_head(root)
    if closeout_remote_branch_head(root, plan) == local_head:
        return False
    command = ["git", "push", plan["git"]["remote"], plan["git"]["head_branch"]]
    run_stdout(command, cwd=root)
    return True

def closeout_pull_request_head_repository(
    item: dict[str, Any], expected_repo: str
) -> tuple[str, bool]:
    expected = normalize_github_repository(expected_repo)
    repository = item.get("headRepository")
    owner = item.get("headRepositoryOwner")
    cross_repository = item.get("isCrossRepository")
    if (
        not expected
        or not isinstance(repository, dict)
        or not isinstance(owner, dict)
        or not isinstance(cross_repository, bool)
    ):
        raise WorkflowError("Closeout pull request head repository identity is missing or invalid.", exit_code=2)
    actual = normalize_github_repository(repository.get("nameWithOwner"))
    owner_login = str(owner.get("login") or "").strip().casefold()
    if not actual or owner_login != actual.split("/", 1)[0]:
        raise WorkflowError("Closeout pull request head repository fields are inconsistent.", exit_code=2)
    is_target = actual == expected
    if cross_repository != (not is_target):
        raise WorkflowError("Closeout pull request cross-repository identity is inconsistent.", exit_code=2)
    return actual, is_target

def resolve_closeout_pull_request(
    root: Path, repo: str, branch: str, base_branch: str, remote: str = "origin"
) -> dict[str, Any] | None:
    expected_repo = validate_github_remote_repository(root, remote, repo)
    values = gh_json(
        [
            "pr", "list", "--repo", repo, "--head", branch,
            "--base", base_branch, "--state", "open", "--limit", "100",
            "--json", (
                "number,url,title,body,headRefName,baseRefName,headRefOid,isDraft,"
                "headRepository,headRepositoryOwner,isCrossRepository"
            ),
        ],
        cwd=root,
        required_fields=(
            "number", "url", "title", "body", "headRefName", "baseRefName",
            "headRefOid", "isDraft", "headRepository", "headRepositoryOwner",
            "isCrossRepository",
        ),
        operation="pull_request_read",
    )
    if not isinstance(values, list):
        raise github_response_incomplete(
            operation="pull_request_read", repo=repo, detail="Pull request list is not an array."
        )
    exact: list[dict[str, Any]] = []
    cross_repository: list[dict[str, Any]] = []
    for item in values:
        if not isinstance(item, dict):
            raise WorkflowError("Closeout pull request identity is invalid.", exit_code=2)
        number = item.get("number")
        if (
            not isinstance(number, int)
            or item.get("headRefName") != branch
            or item.get("baseRefName") != base_branch
        ):
            raise WorkflowError("Closeout pull request repo/head/base identity is invalid.", exit_code=2)
        actual_repo, is_target = closeout_pull_request_head_repository(item, expected_repo)
        if not is_target:
            cross_repository.append({"number": number, "head_repository": actual_repo})
            continue
        item["url"] = canonical_pull_request_url(expected_repo, number, item.get("url"))
        if not re.fullmatch(r"[0-9a-f]{40}", str(item.get("headRefOid") or "")):
            raise WorkflowError("Closeout pull request headRefOid is invalid.", exit_code=2)
        if not isinstance(item.get("isDraft"), bool):
            raise WorkflowError("Closeout pull request draft state is invalid.", exit_code=2)
        if not isinstance(item.get("title"), str) or not isinstance(item.get("body"), str):
            raise WorkflowError("Closeout pull request title/body identity is invalid.", exit_code=2)
        exact.append(item)
    if cross_repository:
        raise WorkflowError(
            "Closeout found cross-repository pull request candidates for the immutable head branch.",
            exit_code=2,
            payload={"candidates": cross_repository},
        )
    if len(exact) > 1:
        raise WorkflowError(
            "Closeout requires zero or one exact open pull request.",
            exit_code=2,
            payload={"open_pr_count": len(exact)},
        )
    return exact[0] if exact else None


def resolve_closeout_terminal_pull_requests(
    root: Path, repo: str, branch: str, base_branch: str, remote: str = "origin"
) -> list[dict[str, Any]]:
    """Return exact same-repository Closed or Merged PRs for the target branch."""
    expected_repo = validate_github_remote_repository(root, remote, repo)
    values = gh_json(
        [
            "pr", "list", "--repo", repo, "--head", branch,
            "--base", base_branch, "--state", "closed", "--limit", "100",
            "--json", (
                "number,url,state,headRefName,baseRefName,headRepository,"
                "headRepositoryOwner,isCrossRepository"
            ),
        ],
        cwd=root,
        required_fields=(
            "number", "url", "state", "headRefName", "baseRefName",
            "headRepository", "headRepositoryOwner", "isCrossRepository",
        ),
        operation="pull_request_read",
    )
    if not isinstance(values, list):
        raise github_response_incomplete(
            operation="pull_request_read",
            repo=repo,
            detail="Terminal pull request list is not an array.",
        )
    exact: list[dict[str, Any]] = []
    for item in values:
        if not isinstance(item, dict):
            raise WorkflowError("Terminal closeout pull request identity is invalid.", exit_code=2)
        number = item.get("number")
        state = item.get("state")
        if (
            not isinstance(number, int)
            or state not in {"CLOSED", "MERGED"}
            or item.get("headRefName") != branch
            or item.get("baseRefName") != base_branch
        ):
            raise WorkflowError(
                "Terminal closeout pull request repo/head/base/state identity is invalid.",
                exit_code=2,
            )
        _actual_repo, is_target = closeout_pull_request_head_repository(item, expected_repo)
        if not is_target:
            continue
        exact.append(
            {
                "number": number,
                "url": canonical_pull_request_url(expected_repo, number, item.get("url")),
                "state": state,
            }
        )
    return exact

def closeout_pull_request_close_issues(body: str) -> list[int]:
    if not isinstance(body, str):
        raise WorkflowError("Closeout pull request body identity is invalid.", exit_code=2)
    return sorted({int(match.group(2)) for match in close_keyword_pattern().finditer(body)})

def classify_existing_pr_recovery(
    root: Path,
    plan: dict[str, Any],
    existing_pr: dict[str, Any] | None = None,
    remote_head: str | None = None,
    *,
    allow_equal: bool = False,
) -> dict[str, Any] | None:
    """Build the exact side-effect-free adoption facts for one current PR."""
    git = plan["git"]
    pr = existing_pr if existing_pr is not None else resolve_closeout_pull_request(
        root,
        git["repo"],
        git["head_branch"],
        git["base_branch"],
        git["remote"],
    )
    if pr is None:
        return None
    remote = remote_head if remote_head is not None else closeout_remote_branch_head(root, plan)
    pr_head = str(pr.get("headRefOid") or "")
    publication_head = str(git.get("publication_head") or git.get("branch_review_commit") or "")
    if remote != pr_head:
        raise WorkflowError(
            "Existing PR recovery requires identical remote branch and PR HEADs.",
            exit_code=2,
            payload={
                "reason_code": "existing_pr_remote_head_mismatch",
                "remote_head": remote,
                "pr_head": pr_head,
            },
        )
    if remote == publication_head:
        if not allow_equal:
            raise WorkflowError(
                "Fresh existing PR recovery cannot adopt an already-pushed publication HEAD without an owner transaction.",
                exit_code=2,
                payload={
                    "reason_code": "existing_pr_unbound_equal_head",
                    "remote_head": remote,
                    "publication_head": publication_head,
                },
            )
        ancestry = "equal"
    elif remote and is_ancestor(root, remote, publication_head):
        ancestry = "strict_ancestor"
    else:
        raise WorkflowError(
            "Fresh existing PR recovery requires a strict publication HEAD ancestor; equality is valid only for a transaction-bound resume.",
            exit_code=2,
            payload={
                "reason_code": "existing_pr_head_not_ancestor",
                "remote_head": remote,
                "publication_head": publication_head,
            },
        )
    reviewed_scope = sorted(set(plan["review"]["close_issues_reviewed"]))
    live_scope = closeout_pull_request_close_issues(str(pr.get("body") or ""))
    if live_scope != reviewed_scope:
        raise WorkflowError(
            "Existing PR recovery close scope differs from the current reviewed Issue Scope Ledger.",
            exit_code=2,
            payload={
                "reason_code": "existing_pr_scope_drift",
                "live_close_issues": live_scope,
                "reviewed_close_issues": reviewed_scope,
            },
        )
    metadata_comparison = {
        "live_title": pr.get("title"),
        "live_body": pr.get("body"),
        "title_matches": pr.get("title") == plan["publish"]["title"],
        "body_matches": pr.get("body") == plan["publish"]["body"],
    }
    return {
        "mode": "existing_pr_recovery",
        "pr": {"number": pr["number"], "url": pr["url"]},
        "initial_state": "draft" if pr["isDraft"] else "ready",
        "initial_is_draft": bool(pr["isDraft"]),
        "pre_push_remote_head": remote,
        "publication_head": publication_head,
        "ancestry": ancestry,
        "push_required": ancestry == "strict_ancestor",
        "metadata_update_required": not (
            metadata_comparison["title_matches"]
            and metadata_comparison["body_matches"]
        ),
        "metadata_comparison": metadata_comparison,
        "ready_action": "mark_ready" if pr["isDraft"] else "preserve_ready",
    }

def provenance_tail_transaction_rebind_errors(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
) -> list[str]:
    """Validate the one supported predecessor-to-current provenance identity step."""
    git = plan["git"]
    active_task_dir = root / str(plan["task"]["active_locator"])
    current_publication_head = str(
        git.get("publication_head") or git.get("branch_review_commit") or ""
    )
    errors = [
        field
        for field, matches in (
            ("task_ref", transaction.get("task_ref") == plan["task"]["active_locator"]),
            ("repo_ref", transaction.get("repo_ref") == git.get("repo")),
            ("base_branch", transaction.get("base_branch") == git.get("base_branch")),
            ("branch", transaction.get("branch") == git.get("head_branch")),
            (
                "publication",
                transaction.get("publication")
                == {
                    "title": plan["publish"]["title"],
                    "body": plan["publish"]["body"],
                },
            ),
            (
                "close_issues",
                transaction.get("close_issues")
                == plan["review"]["close_issues_reviewed"],
            ),
            (
                "current_reviewed_publication_head",
                git.get("branch_review_commit") == current_publication_head,
            ),
            (
                "archive_state",
                not (active_task_dir / FINISH_SUMMARY_ARTIFACT).exists(),
            ),
        )
        if not matches
    ]
    predecessor_reviewed_head = str(transaction.get("branch_review_commit") or "")
    predecessor_publication_head = str(transaction.get("publication_head") or "")
    if predecessor_reviewed_head != predecessor_publication_head:
        errors.extend(
            provenance_tail_commit_errors(
                root,
                predecessor_reviewed_head,
                predecessor_publication_head,
                target_repo=git.get("repo"),
                require_current=False,
            )
        )
    errors.extend(
        provenance_tail_commit_errors(
            root,
            predecessor_publication_head,
            current_publication_head,
            target_repo=git.get("repo"),
        )
    )
    return sorted(set(errors))

def provenance_tail_transaction_rebind_is_base_evolution(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
) -> bool:
    """Identify a current base descendant without treating business drift as a tail."""
    git = plan.get("git") if isinstance(plan.get("git"), dict) else {}
    base_branch = str(git.get("base_branch") or "")
    current_publication_head = str(
        git.get("publication_head") or git.get("branch_review_commit") or ""
    )
    predecessor_publication_head = str(transaction.get("publication_head") or "")
    if not base_branch or not re.fullmatch(
        r"[0-9a-f]{40}", current_publication_head
    ) or not re.fullmatch(r"[0-9a-f]{40}", predecessor_publication_head):
        return False
    base_ref = diff_base_ref(root, base_branch)
    base_proc = run(
        ["git", "rev-parse", "--verify", base_ref],
        cwd=root,
        check=False,
    )
    base_head = base_proc.stdout.strip() if base_proc.returncode == 0 else ""
    if not (
        re.fullmatch(r"[0-9a-f]{40}", base_head) is not None
        and base_head != predecessor_publication_head
        and is_ancestor(root, base_head, current_publication_head)
        and not is_ancestor(root, base_head, predecessor_publication_head)
    ):
        return False
    merge_base_proc = run(
        ["git", "merge-base", predecessor_publication_head, base_head],
        cwd=root,
        check=False,
    )
    if merge_base_proc.returncode != 0:
        return False
    merge_base = merge_base_proc.stdout.strip()
    current_delta = run(
        [
            "git", "diff", "--no-ext-diff", "--binary",
            f"{predecessor_publication_head}..{current_publication_head}",
        ],
        cwd=root,
        check=False,
    )
    base_delta = run(
        [
            "git", "diff", "--no-ext-diff", "--binary",
            f"{merge_base}..{base_head}",
        ],
        cwd=root,
        check=False,
    )
    return (
        current_delta.returncode == 0
        and base_delta.returncode == 0
        and current_delta.stdout == base_delta.stdout
    )

def classify_provenance_tail_transaction_rebind(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
) -> dict[str, Any] | None:
    """Classify one old unbound publication transaction against a legal new tail."""
    if (
        transaction.get("mode") != "ordinary_publication"
        or transaction.get("next_transition") != "push_content"
        or transaction.get("pr") is not None
        or transaction.get("adopted_pr") is not None
    ):
        return None
    errors = provenance_tail_transaction_rebind_errors(root, plan, transaction)
    if errors and not (
        set(errors) <= PROVENANCE_TAIL_INAPPLICABLE_ERRORS
        and provenance_tail_transaction_rebind_is_base_evolution(
            root, plan, transaction
        )
    ):
        raise WorkflowError(
            "Task finalization transaction cannot rebind across the current provenance tail.",
            exit_code=2,
            payload={
                "reason_code": "provenance_tail_transaction_rebind_invalid",
                "errors": errors,
            },
        )
    git = plan["git"]
    candidate = resolve_closeout_pull_request(
        root,
        git["repo"],
        git["head_branch"],
        git["base_branch"],
        git["remote"],
    )
    if candidate is None:
        terminal_prs = resolve_closeout_terminal_pull_requests(
            root,
            git["repo"],
            git["head_branch"],
            git["base_branch"],
            git["remote"],
        )
        if terminal_prs:
            raise WorkflowError(
                "Provenance-tail transaction rebind found a Closed or Merged pull request for the immutable head/base.",
                exit_code=2,
                payload={
                    "reason_code": "pre_finalizer_terminal_pr_exists",
                    "pull_requests": terminal_prs,
                },
            )
        return None
    remote_head = closeout_remote_branch_head(root, plan)
    predecessor_publication_head = str(transaction["publication_head"])
    if remote_head != predecessor_publication_head:
        raise WorkflowError(
            "Provenance-tail transaction rebind requires the remote and PR at the predecessor Publication HEAD.",
            exit_code=2,
            payload={
                "reason_code": "provenance_tail_transaction_rebind_remote_head_mismatch",
                "remote_head": remote_head,
                "predecessor_publication_head": predecessor_publication_head,
            },
        )
    recovery = classify_existing_pr_recovery(
        root,
        plan,
        candidate,
        remote_head,
    )
    if (
        recovery.get("ancestry") != "strict_ancestor"
        or recovery.get("push_required") is not True
        or recovery.get("pre_push_remote_head") != predecessor_publication_head
    ):
        raise WorkflowError(
            "Provenance-tail transaction rebind no longer matches strict-ancestor recovery.",
            exit_code=2,
            payload={"reason_code": "existing_pr_recovery_drift"},
        )
    return recovery

def classify_unbound_equal_head_recovery(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
) -> dict[str, Any] | None:
    """Adopt only one exact ordinary transaction whose publication is already pushed."""
    if (
        transaction.get("mode") != "ordinary_publication"
        or transaction.get("next_transition") != "push_content"
        or transaction.get("pr") is not None
        or transaction.get("adopted_pr") is not None
    ):
        return None
    finalization_validate_transaction_plan(transaction, plan)
    git = plan["git"]
    candidate = resolve_closeout_pull_request(
        root,
        git["repo"],
        git["head_branch"],
        git["base_branch"],
        git["remote"],
    )
    if candidate is None:
        terminal_prs = resolve_closeout_terminal_pull_requests(
            root,
            git["repo"],
            git["head_branch"],
            git["base_branch"],
            git["remote"],
        )
        if terminal_prs:
            raise WorkflowError(
                "Unbound equal-HEAD recovery found a Closed or Merged pull request for the immutable head/base.",
                exit_code=2,
                payload={
                    "reason_code": "pre_finalizer_terminal_pr_exists",
                    "pull_requests": terminal_prs,
                },
            )
        return None
    remote_head = closeout_remote_branch_head(root, plan)
    publication_head = str(
        git.get("publication_head") or git.get("branch_review_commit") or ""
    )
    if remote_head != str(candidate.get("headRefOid") or ""):
        return classify_existing_pr_recovery(
            root,
            plan,
            candidate,
            remote_head,
            allow_equal=True,
        )
    if remote_head != publication_head:
        raise WorkflowError(
            "Unbound ordinary recovery requires identical remote, PR, and Publication HEADs.",
            exit_code=2,
            payload={
                "reason_code": "existing_pr_unbound_equal_head_required",
                "remote_head": remote_head,
                "pr_head": candidate.get("headRefOid"),
                "publication_head": publication_head,
            },
        )
    return classify_existing_pr_recovery(
        root,
        plan,
        candidate,
        remote_head,
        allow_equal=True,
    )

def finalization_validate_recovery_metadata_decision(
    publication: dict[str, Any],
    metadata_comparison: Any,
    metadata_update_required: Any,
) -> dict[str, Any]:
    """Validate the persisted original metadata snapshot and convergence decision."""
    if (
        not isinstance(metadata_comparison, dict)
        or set(metadata_comparison)
        != {"live_title", "live_body", "title_matches", "body_matches"}
        or not isinstance(metadata_comparison.get("live_title"), str)
        or not isinstance(metadata_comparison.get("live_body"), str)
        or not isinstance(metadata_comparison.get("title_matches"), bool)
        or not isinstance(metadata_comparison.get("body_matches"), bool)
        or not isinstance(metadata_update_required, bool)
    ):
        raise WorkflowError(
            "Existing PR recovery transaction metadata decision is incomplete.",
            exit_code=2,
            payload={"reason_code": "existing_pr_transaction_drift"},
        )
    expected_comparison = {
        "live_title": metadata_comparison["live_title"],
        "live_body": metadata_comparison["live_body"],
        "title_matches": (
            metadata_comparison["live_title"] == publication.get("title")
        ),
        "body_matches": (
            metadata_comparison["live_body"] == publication.get("body")
        ),
    }
    expected_update_required = not (
        expected_comparison["title_matches"]
        and expected_comparison["body_matches"]
    )
    if (
        metadata_comparison != expected_comparison
        or metadata_update_required is not expected_update_required
    ):
        raise WorkflowError(
            "Existing PR recovery transaction metadata decision is inconsistent.",
            exit_code=2,
            payload={"reason_code": "existing_pr_transaction_drift"},
        )
    return copy.deepcopy(metadata_comparison)

def finalization_convert_unbound_equal_head_transaction(
    plan: dict[str, Any],
    transaction: dict[str, Any],
    pr: dict[str, Any],
    recovery: dict[str, Any],
) -> dict[str, Any]:
    """Convert one exact ordinary owner transaction into its bound recovery shape."""
    finalization_validate_transaction_plan(transaction, plan)
    publication_head = str(
        plan["git"].get("publication_head")
        or plan["git"].get("branch_review_commit")
        or ""
    )
    if (
        transaction.get("mode") != "ordinary_publication"
        or transaction.get("next_transition") != "push_content"
        or transaction.get("pr") is not None
        or transaction.get("adopted_pr") is not None
        or recovery.get("mode") != "existing_pr_recovery"
        or recovery.get("ancestry") != "equal"
        or recovery.get("push_required") is not False
        or recovery.get("publication_head") != publication_head
        or recovery.get("pre_push_remote_head") != publication_head
        or recovery.get("pr")
        != {"number": pr.get("number"), "url": pr.get("url")}
        or not isinstance(recovery.get("initial_is_draft"), bool)
    ):
        raise WorkflowError(
            "Unbound equal-HEAD recovery no longer matches its exact ordinary transaction.",
            exit_code=2,
            payload={"reason_code": "existing_pr_recovery_drift"},
        )
    metadata_comparison = finalization_validate_recovery_metadata_decision(
        transaction["publication"],
        recovery.get("metadata_comparison"),
        recovery.get("metadata_update_required"),
    )
    adopted_pr = {
        "number": pr["number"],
        "url": pr["url"],
        "initial_is_draft": bool(recovery["initial_is_draft"]),
        "pre_push_remote_head": publication_head,
        "metadata_update_required": bool(
            recovery["metadata_update_required"]
        ),
        "metadata_comparison": metadata_comparison,
    }
    return finalization_transaction_from_plan(
        plan,
        next_transition="bind_pr",
        pr=pr,
        mode="existing_pr_recovery",
        adopted_pr=adopted_pr,
    )

def finalization_adopt_unbound_equal_head_transaction(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
    recovery_preview: dict[str, Any],
) -> dict[str, Any]:
    """Reread exact live facts, convert once, and persist before external mutation."""
    current_recovery = classify_unbound_equal_head_recovery(
        root,
        plan,
        transaction,
    )
    if current_recovery is None or current_recovery != recovery_preview:
        raise WorkflowError(
            "Unbound equal-HEAD recovery facts changed after semantic preview.",
            exit_code=2,
            payload={"reason_code": "existing_pr_recovery_drift"},
        )
    converted = finalization_convert_unbound_equal_head_transaction(
        plan,
        transaction,
        current_recovery["pr"],
        current_recovery,
    )
    finalization_write_transaction(root, task_dir, converted)
    return converted

def finalization_convert_provenance_tail_transaction(
    plan: dict[str, Any],
    transaction: dict[str, Any],
    pr: dict[str, Any],
    recovery: dict[str, Any],
) -> dict[str, Any]:
    """Project one legal predecessor transaction into current strict recovery."""
    publication_head = str(
        plan["git"].get("publication_head")
        or plan["git"].get("branch_review_commit")
        or ""
    )
    predecessor_publication_head = str(transaction.get("publication_head") or "")
    if (
        transaction.get("mode") != "ordinary_publication"
        or transaction.get("next_transition") != "push_content"
        or transaction.get("pr") is not None
        or transaction.get("adopted_pr") is not None
        or recovery.get("mode") != "existing_pr_recovery"
        or recovery.get("ancestry") != "strict_ancestor"
        or recovery.get("push_required") is not True
        or recovery.get("publication_head") != publication_head
        or recovery.get("pre_push_remote_head") != predecessor_publication_head
        or recovery.get("pr")
        != {"number": pr.get("number"), "url": pr.get("url")}
        or not isinstance(recovery.get("initial_is_draft"), bool)
    ):
        raise WorkflowError(
            "Provenance-tail recovery no longer matches its predecessor transaction.",
            exit_code=2,
            payload={"reason_code": "existing_pr_recovery_drift"},
        )
    metadata_comparison = finalization_validate_recovery_metadata_decision(
        {
            "title": plan["publish"]["title"],
            "body": plan["publish"]["body"],
        },
        recovery.get("metadata_comparison"),
        recovery.get("metadata_update_required"),
    )
    adopted_pr = {
        "number": pr["number"],
        "url": pr["url"],
        "initial_is_draft": bool(recovery["initial_is_draft"]),
        "pre_push_remote_head": predecessor_publication_head,
        "metadata_update_required": bool(recovery["metadata_update_required"]),
        "metadata_comparison": metadata_comparison,
    }
    return finalization_transaction_from_plan(
        plan,
        next_transition="push_content",
        pr=pr,
        pre_push_remote_head=predecessor_publication_head,
        mode="existing_pr_recovery",
        adopted_pr=adopted_pr,
    )

def finalization_adopt_provenance_tail_transaction(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
    recovery_preview: dict[str, Any],
) -> dict[str, Any]:
    """Reread, bind, and persist strict recovery before its publication push."""
    current_recovery = classify_provenance_tail_transaction_rebind(
        root,
        plan,
        transaction,
    )
    if current_recovery is None or current_recovery != recovery_preview:
        raise WorkflowError(
            "Provenance-tail recovery facts changed after semantic preview.",
            exit_code=2,
            payload={"reason_code": "existing_pr_recovery_drift"},
        )
    converted = finalization_convert_provenance_tail_transaction(
        plan,
        transaction,
        current_recovery["pr"],
        current_recovery,
    )
    finalization_write_transaction(root, task_dir, converted)
    return converted

def finalization_existing_pr_recovery_context(
    root: Path,
    plan: dict[str, Any],
    current_transaction: dict[str, Any] | None,
    state: str,
) -> tuple[str, dict[str, Any] | None]:
    """Classify recovery without overriding an owning reprepare decision."""
    if state == "reprepare_required":
        return state, None
    if current_transaction is None:
        candidate = resolve_closeout_pull_request(
            root,
            plan["git"]["repo"],
            plan["git"]["head_branch"],
            plan["git"]["base_branch"],
            plan["git"]["remote"],
        )
        if candidate is None:
            return state, None
        return "existing_pr_recovery", classify_existing_pr_recovery(
            root, plan, candidate
        )
    if current_transaction.get("mode") == "ordinary_publication":
        recovery = classify_unbound_equal_head_recovery(
            root,
            plan,
            current_transaction,
        )
        if recovery is None:
            return state, None
        return "existing_pr_recovery", recovery
    if current_transaction.get("mode") != "existing_pr_recovery":
        return state, None
    candidate, remote_head = finalization_pre_mutation_remote_preflight(
        root, plan, current_transaction
    )
    if candidate is None:
        raise WorkflowError(
            "Existing PR recovery transaction lost its bound PR.", exit_code=2
        )
    recovery = current_transaction["adopted_pr"]
    publication_head = str(current_transaction["publication_head"])
    metadata_comparison = {
        "live_title": candidate.get("title"),
        "live_body": candidate.get("body"),
        "title_matches": candidate.get("title") == plan["publish"]["title"],
        "body_matches": candidate.get("body") == plan["publish"]["body"],
    }
    return state, {
        "mode": "existing_pr_recovery",
        "pr": {"number": candidate["number"], "url": candidate["url"]},
        "initial_state": "draft" if recovery["initial_is_draft"] else "ready",
        "initial_is_draft": bool(recovery["initial_is_draft"]),
        "pre_push_remote_head": recovery["pre_push_remote_head"],
        "publication_head": publication_head,
        "ancestry": (
            "equal"
            if recovery["pre_push_remote_head"] == publication_head
            else "strict_ancestor"
        ),
        "push_required": remote_head != publication_head,
        "metadata_update_required": not (
            metadata_comparison["title_matches"]
            and metadata_comparison["body_matches"]
        ),
        "metadata_comparison": metadata_comparison,
        "ready_action": (
            "mark_ready" if recovery["initial_is_draft"] else "preserve_ready"
        ),
    }

def finalization_post_bind_existing_pr_recovery(
    transaction: dict[str, Any] | None,
    plan: dict[str, Any],
) -> bool:
    """Return whether one exact transaction owns the post-bind recovery stage."""
    if (
        not isinstance(transaction, dict)
        or transaction.get("mode") != "existing_pr_recovery"
        or transaction.get("next_transition")
        not in {"archive", "push_archive", "mark_ready"}
    ):
        return False
    finalization_validate_transaction_plan(transaction, plan)
    if not isinstance(transaction.get("pr"), dict) or not isinstance(
        transaction.get("adopted_pr"), dict
    ):
        raise WorkflowError(
            "Post-bind existing PR recovery transaction is incomplete.",
            exit_code=2,
        )
    return True

def finalization_retired_projection_predecessor_digest(
    plan: dict[str, Any],
) -> str:
    """Rebuild the unique pre-retirement plan digest for one current projection."""
    if plan.get("projection", {}).get("retired_tracked_paths") != [
        CLOSEOUT_PLAN_ARTIFACT
    ]:
        raise WorkflowError(
            "Current plan does not match the controlled retired-plan projection.",
            exit_code=2,
        )
    predecessor_plan = copy.deepcopy(plan)
    predecessor_projection = predecessor_plan["projection"]
    predecessor_projection.pop("retired_tracked_paths", None)
    predecessor_projection["move_paths"] = sorted(
        set(predecessor_projection["move_paths"]) | {CLOSEOUT_PLAN_ARTIFACT}
    )
    predecessor_projection["tracked_move_paths"] = sorted(
        set(predecessor_projection["tracked_move_paths"]) | {CLOSEOUT_PLAN_ARTIFACT}
    )
    predecessor_plan["plan_digest"] = ""
    return closeout_plan_digest(predecessor_plan)

def finalization_rebind_retired_projection_transaction(
    transaction: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    """Project one post-bind legacy-plan deletion onto the current plan digest."""
    if (
        transaction.get("mode") != "existing_pr_recovery"
        or transaction.get("next_transition")
        not in {"archive", "push_archive", "mark_ready"}
    ):
        raise WorkflowError(
            "Post-bind transaction does not match the controlled retired-plan projection.",
            exit_code=2,
        )
    if transaction.get("plan_digest") != (
        finalization_retired_projection_predecessor_digest(plan)
    ):
        raise WorkflowError(
            "Post-bind transaction does not bind the exact retired-plan predecessor digest.",
            exit_code=2,
        )
    replacement = finalization_transaction_from_plan(
        plan,
        next_transition=str(transaction["next_transition"]),
        pr=(transaction.get("pr") if isinstance(transaction.get("pr"), dict) else None),
        mode="existing_pr_recovery",
        adopted_pr=(
            transaction.get("adopted_pr")
            if isinstance(transaction.get("adopted_pr"), dict)
            else None
        ),
    )
    prior_identity = {
        key: value for key, value in transaction.items() if key != "plan_digest"
    }
    replacement_identity = {
        key: value for key, value in replacement.items() if key != "plan_digest"
    }
    if prior_identity != replacement_identity:
        raise WorkflowError(
            "Post-bind transaction cannot bind a changed retired-plan identity.",
            exit_code=2,
        )
    return replacement

def finalizer_pre_pr_provenance_tail_applies(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any] | None,
) -> bool:
    """Keep pre-PR provenance inference behind an exact post-bind transaction."""
    if finalization_post_bind_existing_pr_recovery(transaction, plan):
        return False
    return finalizer_pre_pr_provenance_tail_required(root, plan)

def finalization_pre_mutation_remote_preflight(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any] | None,
    *,
    allow_legacy_plan_recovery: bool = False,
    existing_pr_recovery: dict[str, Any] | None = None,
) -> tuple[dict[str, Any] | None, str]:
    """Require an unowned remote or the exact Finalizer-owned recovery state."""
    git = plan["git"]
    existing_pr = resolve_closeout_pull_request(
        root,
        git["repo"],
        git["head_branch"],
        git["base_branch"],
        git["remote"],
    )
    remote_head = closeout_remote_branch_head(root, plan)
    if transaction is None:
        if existing_pr_recovery is not None:
            current_recovery = classify_existing_pr_recovery(
                root, plan, existing_pr, remote_head
            )
            if current_recovery is None or current_recovery != existing_pr_recovery:
                raise WorkflowError(
                    "Existing PR recovery facts changed after semantic preview.",
                    exit_code=2,
                    payload={"reason_code": "existing_pr_recovery_drift"},
                )
            return existing_pr, remote_head
        if allow_legacy_plan_recovery and existing_pr is not None:
            local_head = current_head(root)
            if remote_head != local_head:
                raise WorkflowError(
                    "Legacy Finalizer recovery requires the existing remote at current HEAD.",
                    exit_code=2,
                    payload={"reason_code": "legacy_finalizer_remote_head_drift"},
                )
            validate_closeout_remote_pull_request_identity(
                plan,
                existing_pr,
                expected_draft=True,
                expected_head=remote_head,
            )
            return existing_pr, remote_head
        reviewed_head = str(git["branch_review_commit"])
        remote_is_historical_baseline = bool(
            remote_head
            and remote_head != reviewed_head
            and is_ancestor(root, remote_head, reviewed_head)
        )
        if (
            existing_pr is not None
            or (remote_head and not remote_is_historical_baseline)
        ):
            raise WorkflowError(
                "Task finalization requires an unpublished branch and no Open PR before its first remote mutation.",
                exit_code=2,
                payload={
                    "reason_code": "pre_finalizer_remote_state_exists",
                    "remote_head": remote_head,
                    "pull_request": (
                        existing_pr.get("number") if existing_pr is not None else None
                    ),
                },
            )
        terminal_prs = resolve_closeout_terminal_pull_requests(
            root,
            git["repo"],
            git["head_branch"],
            git["base_branch"],
            git["remote"],
        )
        if terminal_prs:
            raise WorkflowError(
                "Task finalization found a Closed or Merged pull request for the immutable head/base before its first remote mutation.",
                exit_code=2,
                payload={
                    "reason_code": "pre_finalizer_terminal_pr_exists",
                    "pull_requests": terminal_prs,
                },
            )
        return None, remote_head

    identity_mismatches = [
        field
        for field, matches in (
            ("repo_ref", transaction.get("repo_ref") == git.get("repo")),
            ("base_branch", transaction.get("base_branch") == git.get("base_branch")),
            ("branch", transaction.get("branch") == git.get("head_branch")),
            (
                "branch_review_commit",
                transaction.get("branch_review_commit")
                == git.get("branch_review_commit"),
            ),
            (
                "publication_head",
                transaction.get("publication_head")
                == (git.get("publication_head") or git.get("branch_review_commit")),
            ),
        )
        if not matches
    ]
    if identity_mismatches:
        raise WorkflowError(
            "Task finalization owner transaction identity differs from the current plan: "
            + ", ".join(identity_mismatches),
            exit_code=2,
            payload={
                "reason_code": "finalizer_transaction_identity_drift",
                "mismatch_fields": identity_mismatches,
            },
        )
    allowed_heads = {
        str(transaction["branch_review_commit"]),
        str(transaction["publication_head"]),
    }
    if transaction.get("next_transition") == "push_content":
        allowed_heads.add(str(transaction.get("pre_push_remote_head") or ""))
    if remote_head not in allowed_heads:
        raise WorkflowError(
            "Task finalization remote branch drifted outside its owner transaction.",
            exit_code=2,
            payload={
                "reason_code": "finalizer_remote_head_drift",
                "remote_head": remote_head,
                "allowed_heads": sorted(allowed_heads),
            },
        )
    bound_pr = transaction.get("pr")
    recovery = transaction.get("adopted_pr")
    if existing_pr is None:
        if bound_pr is not None:
            raise WorkflowError(
                "Task finalization transaction-bound PR is no longer Open.",
                exit_code=2,
                payload={"reason_code": "finalizer_bound_pr_missing"},
            )
        return None, remote_head
    if not isinstance(bound_pr, dict):
        raise WorkflowError(
            "Task finalization found an Open PR before Finalizer bound it.",
            exit_code=2,
            payload={
                "reason_code": "pre_finalizer_pull_request_exists",
                "pull_request": existing_pr.get("number"),
            },
        )
    if transaction.get("mode") == "existing_pr_recovery":
        if not isinstance(recovery, dict) or (
            recovery.get("number") != bound_pr.get("number")
            or recovery.get("url") != bound_pr.get("url")
        ):
            raise WorkflowError(
                "Existing PR recovery transaction identity is incomplete.",
                exit_code=2,
                payload={"reason_code": "existing_pr_transaction_drift"},
            )
        if remote_head != existing_pr.get("headRefOid"):
            raise WorkflowError(
                "Existing PR recovery remote and PR HEADs diverged.",
                exit_code=2,
                payload={"reason_code": "existing_pr_remote_head_mismatch"},
            )
        validate_closeout_remote_pull_request_binding(
            plan,
            existing_pr,
            expected_draft=bool(recovery["initial_is_draft"]),
            expected_head=remote_head,
            bound_pr=bound_pr,
        )
        if closeout_pull_request_close_issues(str(existing_pr.get("body") or "")) != sorted(
            set(transaction["close_issues"])
        ):
            raise WorkflowError(
                "Existing PR recovery close scope drifted after transaction binding.",
                exit_code=2,
                payload={"reason_code": "existing_pr_scope_drift"},
            )
        if (
            transaction.get("next_transition") == "bind_pr"
            and recovery.get("pre_push_remote_head")
            == transaction.get("publication_head")
        ):
            metadata_comparison = finalization_validate_recovery_metadata_decision(
                transaction["publication"],
                recovery.get("metadata_comparison"),
                recovery.get("metadata_update_required"),
            )
            live_metadata = {
                "title": existing_pr.get("title"),
                "body": existing_pr.get("body"),
            }
            original_metadata = {
                "title": metadata_comparison["live_title"],
                "body": metadata_comparison["live_body"],
            }
            converged_metadata = {
                "title": transaction["publication"]["title"],
                "body": transaction["publication"]["body"],
            }
            if live_metadata != original_metadata and not (
                recovery["metadata_update_required"]
                and live_metadata == converged_metadata
            ):
                raise WorkflowError(
                    "Equal-HEAD recovery PR metadata differs from both its original binding and exact Publication convergence.",
                    exit_code=2,
                    payload={"reason_code": "existing_pr_recovery_drift"},
                )
        if transaction.get("next_transition") not in {"push_content", "bind_pr"}:
            validate_closeout_remote_pull_request_identity(
                plan,
                existing_pr,
                expected_draft=bool(recovery["initial_is_draft"]),
                expected_head=remote_head,
                bound_pr=bound_pr,
            )
    else:
        validate_closeout_remote_pull_request_identity(
            plan,
            existing_pr,
            expected_draft=True,
            expected_head=remote_head,
            bound_pr=bound_pr,
        )
    return existing_pr, remote_head

def closeout_task_dir_from_plan(root: Path, plan: dict[str, Any]) -> Path:
    active = root / plan["task"]["active_locator"]
    archived = root / plan["task"]["archive_locator"]
    if active.is_dir() and not archived.exists():
        return active
    if archived.is_dir() and not active.exists():
        return archived
    raise WorkflowError(
        "Closeout PR identity requires exactly one active or archived task locator.",
        exit_code=2,
    )

def validate_closeout_remote_pull_request_binding(
    plan: dict[str, Any],
    pr: dict[str, Any],
    *,
    expected_draft: bool,
    expected_head: str | None = None,
    bound_pr: dict[str, Any] | None = None,
) -> None:
    expected_repo = normalize_github_repository(plan["git"]["repo"])
    actual_repo, is_target = closeout_pull_request_head_repository(pr, expected_repo)
    if not is_target or actual_repo != expected_repo:
        raise WorkflowError("Closeout pull request head repository differs from immutable readiness.", exit_code=2)
    number = pr.get("number")
    if not isinstance(number, int):
        raise WorkflowError("Closeout pull request number is invalid.", exit_code=2)
    canonical_url = canonical_pull_request_url(plan["git"]["repo"], number, pr.get("url"))
    if pr.get("url") != canonical_url:
        raise WorkflowError("Closeout pull request URL is not canonical.", exit_code=2)
    if (
        pr.get("headRefName") != plan["git"]["head_branch"]
        or pr.get("baseRefName") != plan["git"]["base_branch"]
    ):
        raise WorkflowError("Closeout pull request head/base differs from the immutable plan.", exit_code=2)
    if pr.get("isDraft") is not expected_draft:
        state = "draft" if expected_draft else "ready"
        raise WorkflowError(f"Closeout pull request is not in expected {state} state.", exit_code=2)
    if expected_head is not None and pr.get("headRefOid") != expected_head:
        raise WorkflowError("Closeout pull request HEAD differs from the expected immutable stage HEAD.", exit_code=2)
    if bound_pr is not None:
        bound_number = bound_pr.get("number")
        if not isinstance(bound_number, int):
            raise WorkflowError("Bound closeout pull request number is invalid.", exit_code=2)
        bound_url = canonical_pull_request_url(plan["git"]["repo"], bound_number, bound_pr.get("url"))
        if number != bound_number or canonical_url != bound_url:
            raise WorkflowError("Closeout pull request number/URL differs from the bound remote identity.", exit_code=2)

def validate_closeout_remote_pull_request_identity(
    plan: dict[str, Any],
    pr: dict[str, Any],
    *,
    expected_draft: bool,
    expected_head: str | None = None,
    bound_pr: dict[str, Any] | None = None,
) -> None:
    validate_closeout_remote_pull_request_binding(
        plan,
        pr,
        expected_draft=expected_draft,
        expected_head=expected_head,
        bound_pr=bound_pr,
    )
    if pr.get("title") != plan["publish"]["title"]:
        raise WorkflowError("Closeout pull request title differs from immutable readiness.", exit_code=2)
    body = pr.get("body")
    if not isinstance(body, str):
        raise WorkflowError("Closeout pull request body identity is invalid.", exit_code=2)
    if body != plan["publish"]["body"]:
        raise WorkflowError("Closeout pull request body differs from immutable readiness.", exit_code=2)

def closeout_immutable_pr_body(plan: dict[str, Any]) -> str:
    body = plan.get("publish", {}).get("body")
    if not isinstance(body, str) or not body:
        raise WorkflowError("Closeout immutable plan PR body is missing.", exit_code=2)
    return body

def validate_closeout_pull_request_identity(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    pr: dict[str, Any],
    *,
    expected_draft: bool,
    require_summary: bool,
    expected_head: str | None = None,
    bound_pr: dict[str, Any] | None = None,
) -> None:
    validate_closeout_remote_pull_request_identity(
        plan,
        pr,
        expected_draft=expected_draft,
        expected_head=expected_head,
        bound_pr=bound_pr,
    )
    number = pr["number"]
    canonical_url = canonical_pull_request_url(plan["git"]["repo"], number, pr.get("url"))

    expected_body = closeout_immutable_pr_body(plan)
    if pr.get("body") != expected_body:
        raise WorkflowError("Closeout pull request body differs from immutable readiness.", exit_code=2)

    summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    if require_summary and not summary_path.is_file():
        raise WorkflowError("Closeout final summary is missing for PR identity validation.", exit_code=2)
    if summary_path.is_file():
        summary = read_and_validate_closeout_final_summary(summary_path, plan)
        expected_ref = f"PR #{number}"
        if (
            summary.get("github", {}).get("pr_url") != canonical_url
            or summary.get("index", {}).get("search_terms", {}).get("pr_refs") != [expected_ref]
        ):
            raise WorkflowError(
                "Closeout final summary does not reference the same immutable pull request.",
                exit_code=2,
            )

def ensure_closeout_draft_pr(root: Path, plan: dict[str, Any], body: str) -> dict[str, Any]:
    git = plan["git"]
    task_dir = closeout_task_dir_from_plan(root, plan)
    expected_body = closeout_immutable_pr_body(plan)
    if body != expected_body:
        raise WorkflowError("Closeout requested PR body differs from the immutable plan.", exit_code=2)
    existing = resolve_closeout_pull_request(
        root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
    )
    if existing is not None:
        expected_head = current_head(root)
        validate_closeout_remote_pull_request_binding(
            plan,
            existing,
            expected_draft=True,
            expected_head=expected_head,
        )
        if (
            existing.get("title") != plan["publish"]["title"]
            or existing.get("body") != expected_body
        ):
            update_pull_request_metadata(
                root,
                git["repo"],
                existing["number"],
                plan["publish"]["title"],
                expected_body,
            )
            rebound = resolve_closeout_pull_request(
                root,
                git["repo"],
                git["head_branch"],
                git["base_branch"],
                git["remote"],
            )
            if rebound is None:
                raise WorkflowError(
                    "Updated draft PR could not be rebound to one immutable identity.",
                    exit_code=2,
                )
            validate_closeout_pull_request_identity(
                root,
                task_dir,
                plan,
                rebound,
                expected_draft=True,
                require_summary=False,
                expected_head=expected_head,
                bound_pr=existing,
            )
            return rebound
        validate_closeout_pull_request_identity(
            root,
            task_dir,
            plan,
            existing,
            expected_draft=True,
            require_summary=False,
            expected_head=expected_head,
        )
        return existing
    pr_url = create_pull_request(
        root, git["repo"], git["base_branch"], git["head_branch"],
        plan["publish"]["title"], body, True,
    )
    number = parse_pull_request_number(pr_url)
    if number is None:
        raise WorkflowError("Could not parse draft PR identity.", exit_code=2)
    created = resolve_closeout_pull_request(
        root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
    )
    if created is None or created.get("number") != number:
        raise WorkflowError("Created draft PR could not be rebound to one immutable identity.", exit_code=2)
    validate_closeout_pull_request_identity(
        root,
        task_dir,
        plan,
        created,
        expected_draft=True,
        require_summary=False,
        expected_head=current_head(root),
    )
    return created

def ensure_closeout_bound_pr(
    root: Path,
    plan: dict[str, Any],
    body: str,
    transaction: dict[str, Any] | None,
) -> dict[str, Any]:
    if not isinstance(transaction, dict) or transaction.get("mode") != "existing_pr_recovery":
        return ensure_closeout_draft_pr(root, plan, body)
    recovery = transaction.get("adopted_pr")
    bound_pr = transaction.get("pr")
    if not isinstance(recovery, dict) or not isinstance(bound_pr, dict):
        raise WorkflowError("Existing PR recovery transaction is incomplete.", exit_code=2)
    git = plan["git"]
    existing = resolve_closeout_pull_request(
        root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
    )
    if existing is None:
        raise WorkflowError(
            "Existing PR recovery candidate is no longer Open.",
            exit_code=2,
            payload={"reason_code": "finalizer_bound_pr_missing"},
        )
    expected_head = current_head(root)
    validate_closeout_remote_pull_request_binding(
        plan,
        existing,
        expected_draft=bool(recovery["initial_is_draft"]),
        expected_head=expected_head,
        bound_pr=bound_pr,
    )
    if (
        existing.get("title") != plan["publish"]["title"]
        or existing.get("body") != body
    ):
        update_pull_request_metadata(
            root,
            git["repo"],
            existing["number"],
            plan["publish"]["title"],
            body,
        )
        rebound = resolve_closeout_pull_request(
            root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
        )
        if rebound is None:
            raise WorkflowError("Updated recovery PR could not be rebound.", exit_code=2)
        existing = rebound
    validate_closeout_pull_request_identity(
        root,
        closeout_task_dir_from_plan(root, plan),
        plan,
        existing,
        expected_draft=bool(recovery["initial_is_draft"]),
        require_summary=False,
        expected_head=expected_head,
        bound_pr=bound_pr,
    )
    return existing


def finalization_expected_pr_draft_state(
    transaction: dict[str, Any] | None,
    *,
    current_finalizer: bool,
) -> bool:
    if (
        current_finalizer
        and isinstance(transaction, dict)
        and transaction.get("mode") == "existing_pr_recovery"
    ):
        recovery = transaction.get("adopted_pr")
        if not isinstance(recovery, dict) or not isinstance(
            recovery.get("initial_is_draft"), bool
        ):
            raise WorkflowError(
                "Existing PR recovery transaction is missing its initial Draft/Ready state.",
                exit_code=2,
            )
        return bool(recovery["initial_is_draft"])
    return True


def build_final_archive_projection(
    root: Path,
    task_dir: Path,
    prepared: dict[str, Any],
    pr: dict[str, Any],
    *,
    expected_draft: bool = True,
) -> tuple[Path, dict[str, Any]]:
    plan = prepared["plan"]
    ledger = load_issue_scope_ledger(task_dir, prepared["task_context"])
    ledger_errors = validate_ledger_for_publish(ledger)
    if ledger_errors:
        raise WorkflowError("Final projection ledger validation failed.", exit_code=2, payload={"errors": ledger_errors})
    branch_review_commit = str(plan["git"]["branch_review_commit"])
    anchor_identity = reviewed_content_identity(
        root,
        branch_review_commit,
        include_worktree=False,
    )["sha256"]
    continuity_errors = review_branch_content_continuity_errors(
        root,
        task_dir,
        branch_review_commit,
        anchor_identity,
        current_head(root),
    )
    if continuity_errors:
        raise WorkflowError(
            "Final projection content changed after Publication review.",
            exit_code=2,
            payload={"errors": continuity_errors},
        )
    validate_closeout_pull_request_identity(
        root,
        task_dir,
        plan,
        pr,
        expected_draft=expected_draft,
        require_summary=False,
        expected_head=current_head(root),
    )
    summary = closeout_summary_for_pr(plan, pr)
    if summary["index"]["search_terms"]["pr_refs"] != [f"PR #{pr['number']}"]:
        raise WorkflowError("Final projection must contain one canonical PR ref.", exit_code=2)
    required_artifacts = set(summary["artifacts"].values()) | {
        "issue-scope-ledger.json",
    }
    if CLOSEOUT_PLAN_ARTIFACT in plan["projection"]["move_paths"]:
        required_artifacts.add(CLOSEOUT_PLAN_ARTIFACT)
    missing = sorted(name for name in required_artifacts if not (task_dir / name).is_file())
    if missing:
        raise WorkflowError("Final archive projection is missing task artifacts.", exit_code=2, payload={"missing": missing})
    validate_closeout_final_summary(plan, summary)
    path = task_dir / FINISH_SUMMARY_ARTIFACT
    write_json(path, summary)
    read_and_validate_closeout_final_summary(path, plan)
    return path, summary

def closeout_commit_paths(root: Path, commit: str) -> set[str]:
    return set(
        run_stdout(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "--no-renames", "-r", commit],
            cwd=root,
        ).splitlines()
    )

def closeout_archive_transaction_paths(plan: dict[str, Any]) -> set[str]:
    projection = plan["projection"]
    active = plan["task"]["active_locator"]
    archived = plan["task"]["archive_locator"]
    return {
        *(f"{active}/{path}" for path in projection["tracked_move_paths"]),
        *(f"{active}/{path}" for path in projection.get("retired_tracked_paths", [])),
        *(f"{archived}/{path}" for path in closeout_archive_retained_paths(plan)),
    }

def validate_closeout_archive_git_paths(
    paths: set[str], plan: dict[str, Any], *, stage: str
) -> None:
    expected = closeout_archive_transaction_paths(plan)
    if paths != expected:
        raise WorkflowError(
            f"Closeout {stage} paths do not equal the immutable tracked/untracked archive transaction.",
            exit_code=2,
            payload={
                "stage": stage,
                "expected_paths": sorted(expected),
                "actual_paths": sorted(paths),
                "missing_paths": sorted(expected - paths),
                "extra_paths": sorted(paths - expected),
            },
        )

def closeout_commit_parent(root: Path, commit: str) -> str:
    return run_stdout(["git", "rev-parse", f"{commit}^"], cwd=root)

def closeout_commit_tracked_task_paths(
    root: Path, commit: str, active_locator: str
) -> set[str]:
    return set(
        run_stdout(
            ["git", "ls-tree", "-r", "--name-only", commit, "--", active_locator],
            cwd=root,
        ).splitlines()
    )

def validate_closeout_active_projection(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
) -> None:
    if repo_relative(root, task_dir) != plan["task"]["active_locator"] or not task_dir.is_dir():
        raise WorkflowError("Closeout active projection locator is invalid.", exit_code=2)
    actual_files = sorted(path.relative_to(task_dir).as_posix() for path in task_dir.rglob("*") if path.is_file())
    expected_files = plan["projection"]["move_paths"]
    if actual_files != expected_files:
        raise WorkflowError(
            "Closeout active projection does not match the complete planned move set.",
            exit_code=2,
            payload={"expected_files": expected_files, "actual_files": actual_files},
        )
    read_and_validate_closeout_final_summary(task_dir / FINISH_SUMMARY_ARTIFACT, plan)

def closeout_commit_tree_entry(root: Path, commit: str, path: str) -> tuple[str, str, str]:
    proc = run(["git", "ls-tree", commit, "--", path], cwd=root, check=False)
    rows = [line for line in proc.stdout.splitlines() if line]
    if proc.returncode != 0 or len(rows) != 1:
        raise WorkflowError(
            "Closeout transaction parent is missing one exact tracked move path.",
            exit_code=2,
            payload={"commit": commit, "path": path, "stage": "pre-archive-continuity"},
        )
    metadata, separator, actual_path = rows[0].partition("\t")
    fields = metadata.split()
    if separator != "\t" or actual_path != path or len(fields) != 3:
        raise WorkflowError(
            "Closeout evidence tree entry is ambiguous.",
            exit_code=2,
            payload={"commit": commit, "path": path, "stage": "pre-archive-continuity"},
        )
    return fields[0], fields[1], fields[2]

def closeout_untracked_paths(root: Path) -> set[str]:
    proc = run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError("Could not enumerate pre-archive untracked paths.", exit_code=2)
    return {path for path in proc.stdout.split("\0") if path}

def closeout_projection_content_is_current(
    plan: dict[str, Any],
    relative: str,
    content: bytes,
    mode: str | None = None,
) -> bool:
    if relative == CLOSEOUT_PLAN_ARTIFACT:
        return content == closeout_json_artifact_bytes(plan)
    projection = plan.get("projection", {})
    if "reviewed_tracked_bindings" in projection:
        binding = closeout_reviewed_tracked_binding_map(plan).get(relative)
        return bool(
            binding is not None
            and mode == binding.get("mode")
            and hashlib.sha256(content).hexdigest() == binding.get("sha256")
        )
    input_key = {
        "task.json": "task",
        "issue-scope-ledger.json": "issue_scope_ledger",
    }.get(relative)
    if input_key is None:
        return False
    record = plan.get("inputs", {}).get(input_key)
    if not isinstance(record, dict):
        return False
    actual = hashlib.sha256(content).hexdigest()
    return actual == record.get("sha256")

def validate_closeout_pre_move_continuity(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    transaction_parent: str,
    *,
    expected_summary_pr: dict[str, Any] | None = None,
) -> None:
    """Validate every local archive input before official task.py can mutate it."""
    assert_closeout_archive_month_current(plan)
    hook_state = official_after_archive_hook_state(root)
    hook_input = plan.get("inputs", {}).get("official_after_archive_hooks")
    if (
        not isinstance(hook_input, dict)
        or hook_input.get("path") != ".trellis/config.yaml"
        or hook_input.get("sha256") != canonical_json_sha256(hook_state)
    ):
        raise WorkflowError(
            "Official after_archive hook state drifted from the immutable closeout plan.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight", "hook_executed": False},
        )

    active_locator = plan["task"]["active_locator"]
    for relative in plan["projection"]["move_paths"]:
        target = task_dir / relative
        try:
            working_mode = os.lstat(target).st_mode
        except OSError as exc:
            raise WorkflowError(
                "Closeout pre-archive move path is missing or unreadable.",
                exit_code=2,
                payload={"path": relative, "stage": "pre-archive-continuity"},
            ) from exc
        if not stat.S_ISREG(working_mode):
            raise WorkflowError(
                "Closeout pre-archive move paths must be regular files; symlinks and special modes are rejected.",
                exit_code=2,
                payload={"path": relative, "stage": "pre-archive-continuity"},
            )

    for relative in plan["projection"].get("retired_tracked_paths", []):
        target = task_dir / relative
        if os.path.lexists(target):
            raise WorkflowError(
                "Retired closeout artifact was re-materialized before archive.",
                exit_code=2,
                payload={"path": relative, "stage": "pre-archive-continuity"},
            )
        git_mode, object_type, _object_id = closeout_commit_tree_entry(
            root,
            transaction_parent,
            f"{active_locator}/{relative}",
        )
        if object_type != "blob" or git_mode not in {"100644", "100755"}:
            raise WorkflowError(
                "Retired closeout artifact parent must be one exact regular Git blob.",
                exit_code=2,
                payload={"path": relative, "stage": "pre-archive-continuity"},
            )

    closeout_summary_runtime_pr_facts_from_bytes(
        plan,
        (task_dir / FINISH_SUMMARY_ARTIFACT).read_bytes(),
        expected_pr=expected_summary_pr,
    )

    binding_map = closeout_reviewed_tracked_binding_map(plan)
    observed_binding_paths: set[str] = set()
    for relative in plan["projection"]["tracked_move_paths"]:
        repo_path = f"{active_locator}/{relative}"
        git_mode, object_type, _object_id = closeout_commit_tree_entry(
            root, transaction_parent, repo_path
        )
        if object_type != "blob" or git_mode not in {"100644", "100755"}:
            raise WorkflowError(
                "Closeout tracked move paths must be regular Git blobs, not symlinks, submodules, or special modes.",
                exit_code=2,
                payload={
                    "path": relative,
                    "git_mode": git_mode,
                    "object_type": object_type,
                    "stage": "pre-archive-continuity",
                },
            )
        target = task_dir / relative
        working_mode = os.lstat(target).st_mode
        expected_working_mode = "100755" if working_mode & 0o111 else "100644"
        if (
            plan["projection"].get("migration_predecessor_plan_digest") is not None
            and relative in LEGACY_CLOSEOUT_RETIRED_ARTIFACTS
        ):
            continue
        before = closeout_commit_blob_bytes(root, transaction_parent, repo_path)
        current_bytes = target.read_bytes()
        differs_from_parent = (
            current_bytes != before or expected_working_mode != git_mode
        )
        binding = binding_map.get(relative)
        if binding is not None:
            observed_binding_paths.add(relative)
        if (
            (binding is not None or differs_from_parent)
            and not closeout_projection_content_is_current(
                plan,
                relative,
                current_bytes,
                expected_working_mode,
            )
        ):
            raise WorkflowError(
                "Closeout tracked output differs from its transaction-parent blob and reviewed binding before archive.",
                exit_code=2,
                payload={
                    "path": relative,
                    "expected_mode": git_mode,
                    "actual_mode": expected_working_mode,
                    "stage": "pre-archive-continuity",
                },
            )
    expected_binding_paths = set(binding_map)
    if observed_binding_paths != expected_binding_paths:
        raise WorkflowError(
            "Closeout reviewed tracked bindings do not exactly cover the metadata tail.",
            exit_code=2,
            payload={
                "expected_paths": sorted(expected_binding_paths),
                "actual_paths": sorted(observed_binding_paths),
                "stage": "pre-archive-continuity",
            },
        )

    expected_outputs = {
        f"{active_locator}/{relative}"
        for relative in plan["projection"]["untracked_archive_outputs"]
    }
    dirty = set(git_status_paths(root))
    staged = set(
        run_stdout(
            ["git", "diff", "--cached", "--name-only", "--no-renames"], cwd=root
        ).splitlines()
    )
    untracked = closeout_untracked_paths(root)
    allowed_dirty = {
        f"{active_locator}/{relative}"
        for relative in (
            plan["projection"]["move_paths"]
            + plan["projection"].get("retired_tracked_paths", [])
        )
    }
    dirty_is_valid = dirty.issubset(allowed_dirty)
    if not dirty_is_valid or staged or untracked != expected_outputs:
        raise WorkflowError(
            "Closeout pre-archive dirty/staged/untracked paths do not match the immutable final outputs.",
            exit_code=2,
            payload={
                "stage": "pre-archive-continuity",
                "next_transition": "archive-move",
                "expected_paths": sorted(expected_outputs),
                "dirty_paths": sorted(dirty),
                "staged_paths": sorted(staged),
                "untracked_paths": sorted(untracked),
            },
        )

def compact_closeout_archive(archived: Path, plan: dict[str, Any]) -> None:
    """Remove task-local intermediates that have no long-term archive consumer."""
    parents: set[Path] = set()
    for relative in closeout_archive_pruned_paths(plan):
        target = archived / relative
        try:
            mode = os.lstat(target).st_mode
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise WorkflowError(
                "Compact archive artifact could not be inspected.",
                exit_code=2,
                payload={"path": relative, "stage": "archive-compaction"},
            ) from exc
        if not stat.S_ISREG(mode):
            raise WorkflowError(
                "Compact archive may remove only regular task-local files.",
                exit_code=2,
                payload={"path": relative, "stage": "archive-compaction"},
            )
        target.unlink()
        parents.update(target.parents)
    for parent in sorted(
        (path for path in parents if path != archived and archived in path.parents),
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        try:
            parent.rmdir()
        except OSError:
            pass

def validate_closeout_archive_move_layout(root: Path, archived: Path, plan: dict[str, Any]) -> None:
    active = root / plan["task"]["active_locator"]
    expected_archived = root / plan["task"]["archive_locator"]
    if (
        active.exists()
        or closeout_lexical_path(archived) != closeout_lexical_path(expected_archived)
        or archived.is_symlink()
        or not archived.is_dir()
    ):
        raise WorkflowError(
            "Archived closeout must have no active locator and one complete planned archive locator.",
            exit_code=2,
        )
    actual_files = sorted(path.relative_to(archived).as_posix() for path in archived.rglob("*") if path.is_file())
    expected_files = closeout_archive_retained_paths(plan)
    if actual_files != expected_files:
        raise WorkflowError(
            "Archived closeout files do not match the complete prevalidated move set.",
            exit_code=2,
            payload={"expected_files": expected_files, "actual_files": actual_files},
        )

def closeout_commit_blob_bytes(root: Path, commit: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Closeout could not read an immutable Git blob.",
            exit_code=2,
            payload={"commit": commit, "path": path},
        )
    return proc.stdout

def closeout_optional_commit_blob_bytes(root: Path, commit: str, path: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.stdout if proc.returncode == 0 else None

def validate_closeout_task_json_archive_change(before: bytes, after: bytes) -> None:
    try:
        before_payload = json.loads(before.decode("utf-8"))
        after_payload = json.loads(after.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError("Closeout task.json archive blobs are invalid JSON.", exit_code=2) from exc
    if not isinstance(before_payload, dict) or not isinstance(after_payload, dict):
        raise WorkflowError("Closeout task.json archive blobs must be objects.", exit_code=2)
    expected = copy.deepcopy(before_payload)
    expected["status"] = "completed"
    completed_at = after_payload.get("completedAt")
    if not isinstance(completed_at, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", completed_at):
        raise WorkflowError("Archived task.json completedAt is not an official date value.", exit_code=2)
    expected["completedAt"] = completed_at
    if after_payload != expected:
        raise WorkflowError(
            "Archived task.json contains changes beyond the official status/completedAt transition.",
            exit_code=2,
        )

def closeout_task_json_reviewed_pre_move_bytes(
    transaction_parent: bytes,
    archived: bytes,
) -> bytes:
    """Reverse only the two fields that official task archive overwrites."""
    try:
        parent_payload = json.loads(transaction_parent.decode("utf-8"))
        archived_payload = json.loads(archived.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError("Closeout task.json archive blobs are invalid JSON.", exit_code=2) from exc
    if not isinstance(parent_payload, dict) or not isinstance(archived_payload, dict):
        raise WorkflowError("Closeout task.json archive blobs must be objects.", exit_code=2)

    reviewed_payload = copy.deepcopy(archived_payload)
    for field in ("status", "completedAt"):
        if field in parent_payload:
            reviewed_payload[field] = parent_payload[field]
        else:
            reviewed_payload.pop(field, None)
    # Official task_store.write_json uses this exact encoding without a trailing newline.
    return json.dumps(reviewed_payload, indent=2, ensure_ascii=False).encode("utf-8")

def validate_closeout_archive_blob_continuity(
    root: Path,
    archived: Path,
    plan: dict[str, Any],
    transaction_parent: str,
    *,
    archive_commit: str | None = None,
    expected_summary_pr: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active_locator = plan["task"]["active_locator"]
    archive_locator = plan["task"]["archive_locator"]
    retained_paths = set(closeout_archive_retained_paths(plan))
    for relative in plan["projection"].get("retired_tracked_paths", []):
        active_path = f"{active_locator}/{relative}"
        parent_mode, parent_type, _parent_oid = closeout_commit_tree_entry(
            root,
            transaction_parent,
            active_path,
        )
        if parent_type != "blob" or parent_mode not in {"100644", "100755"}:
            raise WorkflowError(
                "Retired closeout artifact parent is not a regular Git blob.",
                exit_code=2,
                payload={"path": relative},
            )
        if os.path.lexists(archived / relative):
            raise WorkflowError(
                "Retired closeout artifact remains in the compact archive.",
                exit_code=2,
                payload={"path": relative},
            )
        if archive_commit is not None and (
            closeout_optional_commit_blob_bytes(
                root,
                archive_commit,
                f"{archive_locator}/{relative}",
            )
            is not None
            or closeout_optional_commit_blob_bytes(root, archive_commit, active_path)
            is not None
        ):
            raise WorkflowError(
                "Retired closeout artifact was not deleted by the archive commit.",
                exit_code=2,
                payload={"path": relative},
            )
    for relative in plan["projection"]["tracked_move_paths"]:
        if relative not in retained_paths:
            if archive_commit is None:
                if (archived / relative).exists():
                    raise WorkflowError(
                        "Pruned closeout artifact remains in the compact archive.",
                        exit_code=2,
                        payload={"path": relative},
                    )
            elif closeout_optional_commit_blob_bytes(
                root, archive_commit, f"{archive_locator}/{relative}"
            ) is not None:
                raise WorkflowError(
                    "Pruned closeout artifact remains in the committed compact archive.",
                    exit_code=2,
                    payload={"path": relative},
                )
            continue
        before = closeout_commit_blob_bytes(
            root,
            transaction_parent,
            f"{active_locator}/{relative}",
        )
        parent_mode, parent_type, _parent_oid = closeout_commit_tree_entry(
            root,
            transaction_parent,
            f"{active_locator}/{relative}",
        )
        if parent_type != "blob" or parent_mode not in {"100644", "100755"}:
            raise WorkflowError(
                "Archived tracked output parent is not a regular Git blob.",
                exit_code=2,
                payload={"path": relative},
            )
        if archive_commit is None:
            target = archived / relative
            if not target.is_file():
                raise WorkflowError(
                    "Archived tracked output is missing during content validation.",
                    exit_code=2,
                    payload={"path": relative},
                )
            after = target.read_bytes()
            working_mode = os.lstat(target).st_mode
            after_mode = "100755" if working_mode & 0o111 else "100644"
        else:
            archive_path = f"{archive_locator}/{relative}"
            after = closeout_commit_blob_bytes(root, archive_commit, archive_path)
            after_mode, after_type, _after_oid = closeout_commit_tree_entry(
                root,
                archive_commit,
                archive_path,
            )
            if after_type != "blob" or after_mode not in {"100644", "100755"}:
                raise WorkflowError(
                    "Archived tracked output is not a regular Git blob.",
                    exit_code=2,
                    payload={"path": relative},
                )
        if relative == "task.json":
            binding = closeout_reviewed_tracked_binding_map(plan).get(relative)
            reviewed_before = before
            if binding is not None:
                reviewed_before = closeout_task_json_reviewed_pre_move_bytes(before, after)
                if hashlib.sha256(reviewed_before).hexdigest() != binding.get("sha256"):
                    raise WorkflowError(
                        "Archived task.json does not derive from its reviewed pre-move binding.",
                        exit_code=2,
                        payload={"path": relative},
                    )
            validate_closeout_task_json_archive_change(reviewed_before, after)
            expected_mode = binding.get("mode") if binding is not None else parent_mode
            if after_mode != expected_mode:
                raise WorkflowError(
                    "Archived task.json mode differs from its reviewed pre-move mode.",
                    exit_code=2,
                    payload={"path": relative},
                )
        elif (
            (before != after or parent_mode != after_mode)
            and not closeout_projection_content_is_current(
                plan,
                relative,
                after,
                after_mode,
            )
        ):
            raise WorkflowError(
                "Archived tracked output differs from its transaction-parent blob and reviewed binding.",
                exit_code=2,
                payload={"path": relative},
            )
    if archive_commit is None:
        summary_path = archived / FINISH_SUMMARY_ARTIFACT
        try:
            summary_bytes = summary_path.read_bytes()
        except OSError as exc:
            raise WorkflowError("Archived final summary is missing during continuity validation.", exit_code=2) from exc
    else:
        summary_bytes = closeout_commit_blob_bytes(
            root,
            archive_commit,
            f"{archive_locator}/{FINISH_SUMMARY_ARTIFACT}",
        )
    return closeout_summary_runtime_pr_facts_from_bytes(
        plan,
        summary_bytes,
        expected_pr=expected_summary_pr,
    )

def validate_closeout_archive_commit_tree(
    root: Path, plan: dict[str, Any], archive_commit: str
) -> None:
    active_locator = plan["task"]["active_locator"]
    archive_locator = plan["task"]["archive_locator"]
    active_paths = closeout_commit_tracked_task_paths(root, archive_commit, active_locator)
    archived_paths = closeout_commit_tracked_task_paths(root, archive_commit, archive_locator)
    expected_archived_paths = {
        f"{archive_locator}/{relative}"
        for relative in closeout_archive_retained_paths(plan)
    }
    if active_paths or archived_paths != expected_archived_paths:
        raise WorkflowError(
            "Closeout archive commit tree does not contain the exact completed task move.",
            exit_code=2,
            payload={
                "commit": archive_commit,
                "unexpected_active_paths": sorted(active_paths),
                "expected_archive_paths": sorted(expected_archived_paths),
                "actual_archive_paths": sorted(archived_paths),
            },
        )

def resolve_committed_closeout_archive_transaction(
    root: Path, plan: dict[str, Any]
) -> dict[str, Any] | None:
    archive_commit = current_head(root)
    committed_paths = closeout_commit_paths(root, archive_commit)
    if committed_paths != closeout_archive_transaction_paths(plan):
        return None
    validate_closeout_archive_git_paths(committed_paths, plan, stage="archive-committed-head")
    transaction_parent = closeout_commit_parent(root, archive_commit)
    try:
        validate_closeout_reviewed_content(
            root,
            plan,
            transaction_parent,
            include_worktree=False,
        )
        validate_closeout_reviewed_content(
            root,
            plan,
            archive_commit,
            include_worktree=False,
        )
    except WorkflowError:
        return None
    validate_closeout_archive_commit_tree(root, plan, archive_commit)
    summary_pr = validate_closeout_archive_blob_continuity(
        root,
        root / plan["task"]["archive_locator"],
        plan,
        transaction_parent,
        archive_commit=archive_commit,
    )
    return {
        "commit": archive_commit,
        "parent": transaction_parent,
        "paths": sorted(committed_paths),
        "summary_pr": summary_pr,
    }

def assert_archived_committed_workspace_boundary(
    root: Path,
    config: dict[str, Any],
    task_dir: Path,
    expected_plan_digest: str,
) -> dict[str, Any]:
    root = closeout_lexical_path(root)
    task_dir = closeout_lexical_path(task_dir)
    try:
        task_locator = task_dir.relative_to(root).as_posix()
    except ValueError as exc:
        raise WorkflowError(
            "Archived closeout workspace boundary task locator is outside the repository.",
            exit_code=2,
            payload={"repo_root": str(root), "task_dir": str(task_dir)},
        ) from exc

    git_root = Path(run_stdout(["git", "rev-parse", "--show-toplevel"], cwd=root)).resolve()
    if git_root != root:
        raise WorkflowError(
            "Archived closeout workspace boundary repository root mismatch.",
            exit_code=2,
            payload={"expected_root": str(root), "actual_git_root": str(git_root)},
        )
    if (
        not task_dir_is_archived(root, task_dir)
        or not path_within(tasks_root(root) / "archive", task_dir)
    ):
        raise WorkflowError(
            "Archived closeout workspace boundary task locator is invalid.",
            exit_code=2,
            payload={"repo_root": str(root), "task_dir": str(task_dir)},
        )

    archive_commit = current_head(root)
    archive_plan_path = f"{task_locator}/{CLOSEOUT_PLAN_ARTIFACT}"
    plan_blob = closeout_optional_commit_blob_bytes(root, archive_commit, archive_plan_path)
    plan_source = "archive"
    working_plan_path = task_dir / CLOSEOUT_PLAN_ARTIFACT
    if plan_blob is None and working_plan_path.exists():
        if not working_plan_path.is_file() or working_plan_path.is_symlink():
            raise WorkflowError(
                "Archived closeout working-tree plan is unavailable or unsafe.",
                exit_code=2,
            )
        plan_blob = working_plan_path.read_bytes()
        plan_source = "archive_worktree"
    if plan_blob is None:
        raise WorkflowError(
            "Archived closeout has neither the exact committed archive plan nor the current archived working-tree plan.",
            exit_code=2,
            payload={"head": archive_commit, "task_dir": task_locator},
        )
    try:
        raw_plan = json.loads(plan_blob.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(
            "Archived closeout committed plan is invalid JSON.",
            exit_code=2,
        ) from exc
    plan = validate_closeout_plan_for_migration(raw_plan)
    if expected_plan_digest != plan["plan_digest"]:
        raise WorkflowError(
            "Archived closeout workspace boundary expected digest mismatch.",
            exit_code=2,
            payload={
                "expected": expected_plan_digest,
                "actual": plan["plan_digest"],
            },
        )

    task = plan["task"]
    git = plan["git"]
    projection = plan["projection"]
    summary = projection["summary_template"]
    summary_task = summary.get("task") if isinstance(summary.get("task"), dict) else {}
    summary_git = summary.get("git") if isinstance(summary.get("git"), dict) else {}
    summary_github = summary.get("github") if isinstance(summary.get("github"), dict) else {}
    active_locator = str(task["active_locator"])
    archive_locator = str(task["archive_locator"])
    expected_task_dir = closeout_lexical_path(root / archive_locator)
    try:
        resolved_task_dir = task_dir.resolve(strict=True)
        resolved_expected_task_dir = expected_task_dir.resolve(strict=True)
    except (FileNotFoundError, OSError) as exc:
        raise WorkflowError(
            "Archived closeout workspace boundary could not resolve the validated task locator.",
            exit_code=2,
            payload={"task_dir": str(task_dir), "archive_locator": archive_locator},
        ) from exc
    active_parts = Path(active_locator).parts
    archive_parts = Path(archive_locator).parts
    source_issues = summary_github.get("source_issues")
    plan_projection_valid = (
        CLOSEOUT_PLAN_ARTIFACT in projection["move_paths"]
        and sum(
            CLOSEOUT_PLAN_ARTIFACT in projection[classification]
            for classification in (
                "tracked_move_paths",
                "untracked_archive_outputs",
            )
        )
        == 1
    )
    locator_identity_valid = (
        task_locator == archive_locator
        and resolved_task_dir == resolved_expected_task_dir
        and active_parts[:2] == (".trellis", "tasks")
        and len(active_parts) == 3
        and archive_parts[:3] == (".trellis", "tasks", "archive")
        and len(archive_parts) == 5
        and active_parts[-1] == archive_parts[-1] == task_dir.name
        and not (root / active_locator).exists()
        and plan_projection_valid
        and summary_task.get("slug") == task_dir.name
        and summary_task.get("title") == task["title"]
        and summary_task.get("artifact_dir") == active_locator
        and summary_task.get("archive_dir") == archive_locator
        and summary_git.get("branch") == git["head_branch"]
        and summary_git.get("base_branch") == git["base_branch"]
        and isinstance(source_issues, list)
        and task["source_issue"] in source_issues
    )
    if not locator_identity_valid:
        raise WorkflowError(
            "Archived closeout workspace boundary task identity or locator mismatch.",
            exit_code=2,
            payload={
                "task_dir": task_locator,
                "active_locator": active_locator,
                "archive_locator": archive_locator,
            },
        )

    configured_repo_value = str(config.get("github_repo") or "").strip()
    configured_repo = normalize_github_repository(configured_repo_value)
    if configured_repo_value and configured_repo != git["repo"]:
        raise WorkflowError(
            "Archived closeout workspace boundary configured repository mismatch.",
            exit_code=2,
            payload={"expected_repo": git["repo"], "configured_repo": configured_repo},
        )
    validate_github_remote_repository(root, git["remote"], git["repo"])
    actual_branch = current_branch(root)
    if actual_branch != git["head_branch"]:
        raise WorkflowError(
            "Archived closeout workspace boundary branch mismatch.",
            exit_code=2,
            payload={"expected_branch": git["head_branch"], "actual_branch": actual_branch},
        )
    base_refs = [git["base_branch"], f"{git['remote']}/{git['base_branch']}"]
    if not any(git_branch_exists(root, ref) for ref in base_refs):
        raise WorkflowError(
            "Archived closeout workspace boundary base branch is unavailable.",
            exit_code=2,
            payload={"base_branch": git["base_branch"], "checked_refs": base_refs},
        )

    transaction = resolve_committed_closeout_archive_transaction(root, plan)
    if plan_source == "archive" and transaction is None:
        raise WorkflowError(
            "Archived closeout workspace boundary requires the exact committed archive transaction.",
            exit_code=2,
            payload={"head": archive_commit, "task_dir": task_locator},
        )
    if plan_source == "archive_worktree":
        if transaction is not None:
            raise WorkflowError(
                "Archived closeout working plan cannot replace an exact archive plan.",
                exit_code=2,
            )
        validate_closeout_reviewed_content(
            root,
            plan,
            archive_commit,
            include_worktree=True,
        )
    return {
        "status": "ok",
        "mode": (
            "archived-committed-exact"
            if transaction is not None
            else "archived-incomplete-move"
        ),
        "repo_root": str(root),
        "task_dir": str(task_dir),
        "task_dir_relative": task_locator,
        "plan": plan,
        "archive_commit": transaction,
    }

def assert_archived_current_transaction_boundary(
    root: Path,
    config: dict[str, Any],
    task_dir: Path,
    transaction: dict[str, Any],
    expected_plan_digest: str,
) -> dict[str, Any]:
    archive_locator = repo_relative(root, task_dir)
    active_locator = str(transaction["task_ref"])
    if (
        transaction.get("plan_digest") != expected_plan_digest
        or Path(active_locator).name != task_dir.name
        or not task_dir_is_archived(root, task_dir)
        or (root / active_locator).exists()
    ):
        raise WorkflowError(
            "Archived finalization transaction identity is stale.",
            exit_code=2,
        )
    archive_head = current_head(root)
    if closeout_commit_parent(root, archive_head) != transaction["publication_head"]:
        raise WorkflowError(
            "Archived finalization transaction is not the exact publication child.",
            exit_code=2,
        )
    try:
        task = json.loads(
            closeout_commit_blob_bytes(
                root,
                archive_head,
                f"{archive_locator}/task.json",
            ).decode("utf-8")
        )
        summary = json.loads(
            closeout_commit_blob_bytes(
                root,
                archive_head,
                f"{archive_locator}/{FINISH_SUMMARY_ARTIFACT}",
            ).decode("utf-8")
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(
            "Archived finalization committed evidence is invalid.",
            exit_code=2,
        ) from exc
    if not isinstance(task, dict) or task.get("status") != "completed" or not isinstance(summary, dict):
        raise WorkflowError(
            "Archived finalization transaction is missing durable task evidence.",
            exit_code=2,
        )
    summary_task = summary.get("task") if isinstance(summary.get("task"), dict) else {}
    summary_git = summary.get("git") if isinstance(summary.get("git"), dict) else {}
    summary_github = summary.get("github") if isinstance(summary.get("github"), dict) else {}
    if (
        summary_task.get("artifact_dir") != active_locator
        or summary_task.get("archive_dir") != archive_locator
        or summary_git.get("branch") != transaction.get("branch")
        or summary_git.get("base_branch") != transaction.get("base_branch")
        or current_branch(root) != transaction.get("branch")
    ):
        raise WorkflowError(
            "Archived finalization summary does not match the transaction.",
            exit_code=2,
        )
    configured_repo = normalize_github_repository(config.get("github_repo"))
    if configured_repo and configured_repo != transaction.get("repo_ref"):
        raise WorkflowError(
            "Archived finalization repository does not match configuration.",
            exit_code=2,
        )
    remote = str(publish_config(config).get("remote") or "origin")
    validate_github_remote_repository(root, remote, str(transaction["repo_ref"]))
    pr_url = summary_github.get("pr_url")
    canonical_url, pr_number = parse_canonical_pull_request_url(
        str(transaction["repo_ref"]),
        pr_url,
    )
    plan = {
        "plan_digest": transaction["plan_digest"],
        "task": {
            "active_locator": active_locator,
            "archive_locator": archive_locator,
        },
        "git": {
            "repo": transaction["repo_ref"],
            "remote": remote,
            "base_branch": transaction["base_branch"],
            "head_branch": transaction["branch"],
            "branch_review_commit": transaction["branch_review_commit"],
            "reviewed_content_head": transaction["branch_review_commit"],
            "publication_head": transaction["publication_head"],
        },
        "review": {
            "close_issues_reviewed": transaction["close_issues"],
        },
        "publish": {
            "title": transaction["publication"]["title"],
            "body": transaction["publication"]["body"],
            "draft": True,
            "draft_to_ready": True,
            "match": {
                "repo": transaction["repo_ref"],
                "head": transaction["branch"],
                "base": transaction["base_branch"],
            },
        },
        "marketplace": {"required": "verification_ref" in transaction},
    }
    archive_commit = {
        "commit": archive_head,
        "parent": transaction["publication_head"],
        "paths": sorted(closeout_commit_paths(root, archive_head)),
        "summary_pr": {"number": pr_number, "url": canonical_url},
    }
    return {"plan": plan, "archive_commit": archive_commit}

def restore_current_archive_move_for_reentry(
    root: Path,
    archived: Path,
    transaction: dict[str, Any],
) -> Path:
    active = root / str(transaction["task_ref"])
    if (
        current_head(root) != transaction["publication_head"]
        or active.exists()
        or not archived.is_dir()
        or archived.is_symlink()
    ):
        raise WorkflowError(
            "Current archive-move recovery identity is invalid.",
            exit_code=2,
        )
    run_stdout(["git", "reset", "--mixed", "--quiet", "HEAD"], cwd=root)
    active.parent.mkdir(parents=True, exist_ok=True)
    archived.rename(active)
    run_stdout(
        [
            "git",
            "restore",
            f"--source={transaction['publication_head']}",
            "--worktree",
            "--",
            str(transaction["task_ref"]),
        ],
        cwd=root,
    )
    task_path = active / "task.json"
    if not task_path.is_file() or task_path.is_symlink():
        raise WorkflowError(
            "Current archive-move recovery is missing task identity.",
            exit_code=2,
        )
    task = read_json(task_path)
    if task.get("status") not in {"in_progress", "completed"}:
        raise WorkflowError(
            "Current archive-move recovery requires completed move metadata.",
            exit_code=2,
        )
    if task.get("status") == "completed":
        task["status"] = "in_progress"
        task.pop("completedAt", None)
        write_json(task_path, task)
    return active

def execute_archive_metadata_transaction(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    *,
    bound_pr: dict[str, Any] | None = None,
) -> tuple[Path, dict[str, Any]]:
    archive_script = root / ".trellis/scripts/task.py"
    if not archive_script.is_file():
        raise WorkflowError(f"Trellis task.py not found: {archive_script}")
    transaction_parent = current_head(root)
    validate_closeout_reviewed_content(
        root,
        plan,
        transaction_parent,
        include_worktree=True,
    )
    validate_closeout_active_projection(
        root,
        task_dir,
        plan,
    )
    assert_closeout_archive_path_preflight(root, plan["task"]["archive_locator"])
    validate_closeout_pre_move_continuity(
        root,
        task_dir,
        plan,
        transaction_parent,
        expected_summary_pr=bound_pr,
    )
    proc = run(
        [sys.executable, "./.trellis/scripts/task.py", "archive", task_dir.name, "--no-commit"],
        cwd=root,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError("task.py archive move failed.", exit_code=2, payload={"stderr": proc.stderr.strip(), "stdout": proc.stdout.strip()})
    archived = root / plan["task"]["archive_locator"]
    compact_closeout_archive(archived, plan)
    validate_closeout_archive_move_layout(root, archived, plan)
    validate_closeout_archive_blob_continuity(
        root,
        archived,
        plan,
        transaction_parent,
        expected_summary_pr=bound_pr,
    )
    active_locator = plan["task"]["active_locator"]
    archive_locator = plan["task"]["archive_locator"]
    dirty = set(git_status_paths(root))
    validate_closeout_archive_git_paths(dirty, plan, stage="archive-move-dirty")
    run_stdout(["git", "add", "-A", "--", active_locator, archive_locator], cwd=root)
    staged = set(run_stdout(["git", "diff", "--cached", "--name-only", "--no-renames"], cwd=root).splitlines())
    validate_closeout_archive_git_paths(staged, plan, stage="archive-staged")
    run_stdout(["git", "commit", "-m", format_metadata_commit_subject(int(plan["task"]["source_issue"]))], cwd=root)
    archive_commit = current_head(root)
    committed = closeout_commit_paths(root, archive_commit)
    validate_closeout_archive_git_paths(committed, plan, stage="archive-commit")
    if committed != staged:
        raise WorkflowError("Archive metadata commit differs from its staged transaction.", exit_code=2, payload={"staged": sorted(staged), "committed": sorted(committed)})
    if closeout_commit_parent(root, archive_commit) != transaction_parent:
        raise WorkflowError("Archive metadata commit parent is not the validated transaction parent.", exit_code=2)
    validate_closeout_archive_blob_continuity(
        root,
        archived,
        plan,
        transaction_parent,
        archive_commit=archive_commit,
        expected_summary_pr=bound_pr,
    )
    if git_status_paths(root):
        raise WorkflowError("Archive metadata commit left repository paths dirty.", exit_code=2)
    run_stdout(["git", "push", plan["git"]["remote"], plan["git"]["head_branch"]], cwd=root)
    return archived, {"commit": archive_commit, "parent": transaction_parent, "paths": sorted(committed)}

def ensure_closeout_pr_ready(
    root: Path, plan: dict[str, Any], *, bound_pr: dict[str, Any] | None = None
) -> dict[str, Any]:
    git = plan["git"]
    pr = resolve_closeout_pull_request(
        root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
    )
    if pr is None:
        raise WorkflowError("Closeout draft PR is missing.", exit_code=2)
    local_head = current_head(root)
    validate_closeout_remote_pull_request_identity(
        plan,
        pr,
        expected_draft=bool(pr["isDraft"]),
        bound_pr=bound_pr,
    )
    remote_head = closeout_remote_branch_head(root, plan)
    if local_head != remote_head:
        raise WorkflowError(
            "Closeout local/remote/PR HEAD identity mismatch.",
            exit_code=2,
            payload={"local_head": local_head, "remote_head": remote_head, "pr_head": pr["headRefOid"]},
        )
    initial_pr = pr
    for attempt in range(CLOSEOUT_PR_HEAD_READ_ATTEMPTS):
        if pr["headRefOid"] == local_head:
            break
        if attempt + 1 == CLOSEOUT_PR_HEAD_READ_ATTEMPTS:
            raise WorkflowError(
                "Closeout local/remote/PR HEAD identity mismatch.",
                exit_code=2,
                payload={
                    "local_head": local_head,
                    "remote_head": remote_head,
                    "pr_head": pr["headRefOid"],
                },
            )
        time.sleep(CLOSEOUT_PR_HEAD_READ_DELAY_SECONDS)
        reread = resolve_closeout_pull_request(
            root,
            git["repo"],
            git["head_branch"],
            git["base_branch"],
            git["remote"],
        )
        if reread is None:
            raise WorkflowError(
                "Closeout pull request disappeared while waiting for HEAD convergence.",
                exit_code=2,
            )
        validate_closeout_remote_pull_request_identity(
            plan,
            reread,
            expected_draft=bool(initial_pr["isDraft"]),
            bound_pr=bound_pr or initial_pr,
        )
        remote_head = closeout_remote_branch_head(root, plan)
        if remote_head != local_head:
            raise WorkflowError(
                "Closeout local/remote/PR HEAD identity mismatch.",
                exit_code=2,
                payload={
                    "local_head": local_head,
                    "remote_head": remote_head,
                    "pr_head": reread["headRefOid"],
                },
            )
        pr = reread
    validate_closeout_remote_pull_request_identity(
        plan,
        pr,
        expected_draft=bool(initial_pr["isDraft"]),
        expected_head=local_head,
        bound_pr=bound_pr or initial_pr,
    )
    if pr["isDraft"]:
        try:
            run_gh_command(
                ["pr", "ready", "--repo", git["repo"], str(pr["number"])],
                root,
                repo=git["repo"],
                operation="pull_request_ready",
            )
        except WorkflowError as exc:
            raise WorkflowError(
                "Draft-to-ready transition failed.",
                exit_code=2,
                payload={**exc.payload, "stage": "draft-to-ready"},
            ) from exc
        confirmed = resolve_closeout_pull_request(
            root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
        )
        if confirmed is None or confirmed.get("isDraft") is not False or confirmed.get("headRefOid") != local_head:
            raise WorkflowError("Draft-to-ready transition could not be confirmed.", exit_code=2, payload={"stage": "draft-to-ready-confirmation"})
        validate_closeout_remote_pull_request_identity(
            plan,
            confirmed,
            expected_draft=False,
            expected_head=local_head,
            bound_pr=bound_pr or pr,
        )
        pr = confirmed
    return {"pr": pr, "local_head": local_head, "remote_head": remote_head, "status": "ready"}

def resume_archive_metadata_transaction(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    *,
    bound_pr: dict[str, Any] | None = None,
) -> dict[str, Any]:
    compact_closeout_archive(task_dir, plan)
    validate_closeout_archive_move_layout(root, task_dir, plan)
    dirty = set(git_status_paths(root))
    if dirty:
        validate_closeout_archive_git_paths(dirty, plan, stage="archive-recovery-dirty")
        transaction_parent = current_head(root)
        validate_closeout_reviewed_content(
            root,
            plan,
            transaction_parent,
            include_worktree=True,
        )
        validate_closeout_archive_blob_continuity(
            root,
            task_dir,
            plan,
            transaction_parent,
            expected_summary_pr=bound_pr,
        )
        active = plan["task"]["active_locator"]
        archived = plan["task"]["archive_locator"]
        staged = set(run_stdout(["git", "diff", "--cached", "--name-only", "--no-renames"], cwd=root).splitlines())
        if not staged:
            pathspecs = (
                [f"{active}/{relative}" for relative in plan["projection"]["tracked_move_paths"]]
                + [
                    f"{active}/{relative}"
                    for relative in plan["projection"].get("retired_tracked_paths", [])
                ]
                + [
                    f"{archived}/{relative}"
                    for relative in closeout_archive_retained_paths(plan)
                ]
            )
            run_stdout(["git", "add", "-A", "--", *pathspecs], cwd=root)
            staged = set(run_stdout(["git", "diff", "--cached", "--name-only", "--no-renames"], cwd=root).splitlines())
        validate_closeout_archive_git_paths(staged, plan, stage="archive-recovery-staged")
        run_stdout(["git", "commit", "-m", format_metadata_commit_subject(int(plan["task"]["source_issue"]))], cwd=root)
        archive_commit = current_head(root)
        archive_paths = closeout_commit_paths(root, archive_commit)
        validate_closeout_archive_git_paths(archive_paths, plan, stage="archive-recovery-commit")
        if closeout_commit_parent(root, archive_commit) != transaction_parent:
            raise WorkflowError("Recovered archive commit does not match the exact parent/path transaction.", exit_code=2)
        validate_closeout_archive_blob_continuity(
            root,
            task_dir,
            plan,
            transaction_parent,
            archive_commit=archive_commit,
            expected_summary_pr=bound_pr,
        )
    else:
        archive_commit = current_head(root)
        last_paths = closeout_commit_paths(root, archive_commit)
        transaction_parent = closeout_commit_parent(root, archive_commit)
        validate_closeout_archive_git_paths(last_paths, plan, stage="archive-recovery-head")
        validate_closeout_reviewed_content(
            root,
            plan,
            transaction_parent,
            include_worktree=False,
        )
        validate_closeout_archive_blob_continuity(
            root,
            task_dir,
            plan,
            transaction_parent,
            archive_commit=archive_commit,
            expected_summary_pr=bound_pr,
        )
    local_head = current_head(root)
    remote_proc = run(
        ["git", "ls-remote", "--heads", plan["git"]["remote"], plan["git"]["head_branch"]],
        cwd=root,
        check=False,
    )
    rows = [line.split() for line in remote_proc.stdout.splitlines() if line.strip()]
    remote_head = rows[0][0] if len(rows) == 1 else ""
    if remote_proc.returncode != 0 or remote_head != local_head:
        run_stdout(["git", "push", plan["git"]["remote"], plan["git"]["head_branch"]], cwd=root)
    return {
        "commit": archive_commit,
        "parent": transaction_parent,
        "paths": sorted(closeout_commit_paths(root, archive_commit)),
    }

def resume_archived_closeout(
    root: Path,
    args: argparse.Namespace,
    task_dir: Path,
    *,
    committed_plan: dict[str, Any] | None = None,
    committed_archive: dict[str, Any] | None = None,
    finalization_transaction: dict[str, Any] | None = None,
) -> dict[str, Any]:
    plan = committed_plan or validate_closeout_plan_for_migration(
        read_json(closeout_plan_path(task_dir))
    )
    expected = str(getattr(args, "expected_plan_digest", "") or "")
    if expected != plan["plan_digest"]:
        raise WorkflowError("Formal closeout expected digest does not match the archived plan.", exit_code=2, payload={"expected": expected, "actual": plan["plan_digest"]})
    git = plan["git"]
    require_gh_auth(root)
    archive_commit = committed_archive or resolve_committed_closeout_archive_transaction(root, plan)
    finalizer_recovery = (
        archive_commit is not None
        and isinstance(getattr(args, "finalization_gate", None), dict)
    )
    if finalizer_recovery:
        local_head = current_head(root)
        remote_head = closeout_remote_branch_head(root, plan)
        if remote_head != local_head:
            raise WorkflowError(
                "Archived finalization recovery requires the pushed archive HEAD before Ready.",
                exit_code=2,
                payload={"local_head": local_head, "remote_head": remote_head},
            )
    bound_pr: dict[str, Any] | None = None
    if archive_commit is not None:
        summary_pr = archive_commit.get("summary_pr")
        if not isinstance(summary_pr, dict):
            commit = str(archive_commit.get("commit") or "")
            summary_bytes = closeout_commit_blob_bytes(
                root,
                commit,
                f"{plan['task']['archive_locator']}/{FINISH_SUMMARY_ARTIFACT}",
            )
            summary_pr = closeout_summary_runtime_pr_facts_from_bytes(plan, summary_bytes)
        bound_pr = summary_pr
    pr = resolve_closeout_pull_request(
        root, git["repo"], git["head_branch"], git["base_branch"], git["remote"]
    )
    if pr is None:
        raise WorkflowError("Archived closeout recovery requires the bound pull request.", exit_code=2)
    expected_draft = True if finalizer_recovery else bool(pr["isDraft"])
    if (
        finalizer_recovery
        and isinstance(finalization_transaction, dict)
        and finalization_transaction.get("mode") == "existing_pr_recovery"
    ):
        adopted_pr = finalization_transaction.get("adopted_pr")
        if not isinstance(adopted_pr, dict) or not isinstance(
            adopted_pr.get("initial_is_draft"), bool
        ):
            raise WorkflowError(
                "Archived existing PR recovery transaction is incomplete.",
                exit_code=2,
                payload={"reason_code": "existing_pr_transaction_drift"},
            )
        expected_draft = bool(adopted_pr["initial_is_draft"])
    validate_closeout_remote_pull_request_identity(
        plan,
        pr,
        expected_draft=expected_draft,
        bound_pr=bound_pr,
    )
    if archive_commit is None:
        archive_commit = resume_archive_metadata_transaction(
            root,
            task_dir,
            plan,
            bound_pr=pr,
        )
    else:
        if not finalizer_recovery:
            push_closeout_branch_if_needed(root, plan)
    result = ensure_closeout_pr_ready(root, plan, bound_pr=bound_pr or pr)
    return {
        "status": "ok",
        "stage": "ready",
        "task_dir": str(task_dir),
        "archived_task_dir": str(task_dir),
        "plan_digest": plan["plan_digest"],
        "archive_commit": archive_commit,
        "publish": result,
    }

def apply_active_closeout_month_supersession(
    root: Path,
    task_dir: Path,
    prepared: dict[str, Any],
) -> str:
    supersession = prepared.get("month_supersession")
    if not isinstance(supersession, dict):
        raise WorkflowError("Closeout month supersession state is missing.", exit_code=2)
    previous = supersession["previous_plan"]
    plan = prepared["plan"]
    errors = closeout_month_supersession_errors(previous, plan)
    if errors:
        raise WorkflowError(
            "Closeout archive month supersession is no longer valid.",
            exit_code=2,
            payload={"errors": errors, "stage": "archive-month-reprepare"},
        )
    assert_closeout_archive_month_current(plan)
    if (root / previous["task"]["archive_locator"]).exists():
        raise WorkflowError(
            "Closeout archive month supersession refuses an already moved task.",
            exit_code=2,
            payload={"stage": "archive-month-reprepare"},
        )
    summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    if summary_path.exists():
        read_and_validate_closeout_final_summary(summary_path, previous)
        summary_path.unlink()
    write_json(closeout_plan_path(task_dir), plan)
    return str(supersession["prior_state"])

def resume_active_archive_move(
    root: Path,
    args: argparse.Namespace,
    config: dict[str, Any],
    task_dir: Path,
    task_context: dict[str, Any],
) -> dict[str, Any]:
    plan = validate_closeout_plan_for_migration(
        read_json(closeout_plan_path(task_dir))
    )
    expected = str(getattr(args, "expected_plan_digest", "") or "")
    if expected != plan["plan_digest"]:
        raise WorkflowError("Archive-move recovery digest does not match committed plan.", exit_code=2)
    task = task_json(task_dir)
    if task.get("status") != "completed":
        raise WorkflowError("Archive-move recovery requires active task status=completed.", exit_code=2)
    del config
    validate_closeout_reviewed_content(
        root,
        plan,
        current_head(root),
        include_worktree=True,
    )
    summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    if not summary_path.is_file():
        raise WorkflowError("Archive-move recovery requires the validated final summary.", exit_code=2)
    validate_closeout_active_projection(
        root,
        task_dir,
        plan,
    )
    assert_closeout_archive_month_current(plan)
    official_after_archive_hook_state(root)
    require_gh_auth(root)
    pr = resolve_closeout_pull_request(
        root,
        plan["git"]["repo"],
        plan["git"]["head_branch"],
        plan["git"]["base_branch"],
        plan["git"]["remote"],
    )
    if pr is None or pr.get("isDraft") is not True:
        raise WorkflowError("Archive-move recovery requires the bound draft PR.", exit_code=2)
    validate_closeout_pull_request_identity(
        root,
        task_dir,
        plan,
        pr,
        expected_draft=True,
        require_summary=True,
        expected_head=current_head(root),
    )
    archived_task_dir, archive_commit = execute_archive_metadata_transaction(
        root,
        task_dir,
        plan,
        bound_pr=pr,
    )
    publish_payload = ensure_closeout_pr_ready(root, plan, bound_pr=pr)
    return {
        "status": "ok",
        "stage": "ready",
        "entry_state": "archive_moved",
        "task_dir": str(task_dir),
        "archived_task_dir": str(archived_task_dir),
        "closeout_plan_digest": plan["plan_digest"],
        "finish_summary": str(archived_task_dir / FINISH_SUMMARY_ARTIFACT),
        "archive_commit": archive_commit,
        "publish": publish_payload,
    }

def execute_closeout_content_push(
    root: Path,
    task_dir: Path,
    task_context: dict[str, Any],
    prepared: dict[str, Any],
    *,
    persist_closeout_plan: bool = True,
) -> dict[str, Any]:
    """Push reviewed content before continuing directly to Draft PR binding."""
    plan = prepared["plan"]
    validate_closeout_reviewed_content(
        root,
        plan,
        current_head(root),
        include_worktree=True,
    )
    publication_head = str(
        plan["git"].get("publication_head") or plan["git"]["branch_review_commit"]
    )
    if current_head(root) != publication_head:
        raise WorkflowError(
            "Closeout exact publication push requires local HEAD at publication_head.",
            exit_code=2,
        )
    run_stdout(
        [
            "git",
            "push",
            "-u",
            plan["git"]["remote"],
            f"{publication_head}:refs/heads/{plan['git']['head_branch']}",
        ],
        cwd=root,
    )
    validate_publish_identity_and_remote_head(
        root,
        prepared["task"],
        task_context,
        plan["git"]["repo"],
        plan["git"]["base_branch"],
        plan["git"]["head_branch"],
        plan["git"]["remote"],
    )
    if persist_closeout_plan:
        write_json(closeout_plan_path(task_dir), plan)
    return {
        "status": "ok",
        "stage": "content_pushed",
        "entry_state": "prepared",
        "task_dir": str(task_dir),
        "closeout_plan_digest": plan["plan_digest"],
        "plan_ref": (
            f"closeout-plan:{plan['plan_digest']}"
            if persist_closeout_plan
            else f"finalization:{plan['plan_digest']}"
        ),
        "branch_review_commit": plan["git"]["branch_review_commit"],
    }

def _cmd_finish_work_impl(args: argparse.Namespace) -> dict[str, Any]:
    validate_finish_work_invocation(args)
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_finish_work_task_dir(root, args.task)
    if task_dir_is_archived(root, task_dir):
        if args.dry_run:
            raise WorkflowError("Archived closeout recovery does not have a new dry-run phase.", exit_code=2)
        current_match = finalization_find_transaction_by_task_ref(
            root,
            f".trellis/tasks/{task_dir.name}",
        )
        if current_match is not None:
            transaction, _transaction_path = current_match
            if current_head(root) == transaction["publication_head"]:
                active_task_dir = restore_current_archive_move_for_reentry(
                    root,
                    task_dir,
                    transaction,
                )
                resumed_args = copy.copy(args)
                resumed_args.task = str(active_task_dir)
                return cmd_finish_work(resumed_args)
            boundary = assert_archived_current_transaction_boundary(
                root,
                config,
                task_dir,
                transaction,
                str(getattr(args, "expected_plan_digest", "") or ""),
            )
            result = resume_archived_closeout(
                root,
                args,
                task_dir,
                committed_plan=boundary["plan"],
                committed_archive=boundary["archive_commit"],
                finalization_transaction=transaction,
            )
            result["retired_owner_state"] = finalization_retire_current_state(
                root,
                root / str(transaction["task_ref"]),
            )
            return result
        committed_boundary = assert_archived_committed_workspace_boundary(
            root,
            config,
            task_dir,
            str(getattr(args, "expected_plan_digest", "") or ""),
        )
        return resume_archived_closeout(
            root,
            args,
            task_dir,
            committed_plan=committed_boundary["plan"],
            committed_archive=committed_boundary.get("archive_commit"),
        )
    task_context = load_task_runtime_identity(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    current_finalizer = bool(getattr(args, "from_guru_finalizer", False))
    if closeout_plan_path(task_dir).is_file() and task_json(task_dir).get("status") == "completed":
        if args.dry_run:
            raise WorkflowError("Interrupted archive move must resume through formal finish-work.", exit_code=2)
        return resume_active_archive_move(root, args, config, task_dir, task_context)

    prepared = prepare_closeout(
        root,
        args,
        config,
        task_dir,
        task_context,
        publication_ready=getattr(args, "publication_ready", None),
        current_finalizer=current_finalizer,
    )
    plan = prepared["plan"]
    if args.dry_run:
        return {
            "status": "dry-run",
            "dry_run_side_effects": False,
            "task_dir": str(task_dir),
            "closeout_plan": plan,
            "closeout_plan_digest": plan["plan_digest"],
            "expected_actions": list(CLOSEOUT_TRANSITIONS[1:]),
        }

    expected_digest = str(getattr(args, "expected_plan_digest", "") or "")
    if expected_digest != plan["plan_digest"]:
        raise WorkflowError(
            "Formal closeout expected digest does not match the rebuilt plan.",
            exit_code=2,
            payload={"expected": expected_digest, "actual": plan["plan_digest"], "failed_stage": "plan-digest-handshake"},
        )
    assert_closeout_archive_month_current(plan)
    require_gh_auth(root)
    if current_finalizer:
        transaction = finalization_read_transaction(root, task_dir)
        prior_transaction = transaction
        retired_projection_rebound = False
        if (
            isinstance(transaction, dict)
            and transaction.get("plan_digest") != plan["plan_digest"]
            and transaction.get("mode") == "existing_pr_recovery"
            and transaction.get("next_transition")
            in {"archive", "push_archive", "mark_ready"}
        ):
            transaction = finalization_rebind_retired_projection_transaction(
                transaction,
                plan,
            )
            prior_transaction = transaction
            retired_projection_rebound = True
        migration = prepared.get("migration_normalization")
        legacy_plan = (
            migration.get("previous_plan")
            if isinstance(migration, dict)
            and isinstance(migration.get("previous_plan"), dict)
            else None
        )
        legacy_plan_recovery = (
            transaction is None
            and isinstance(legacy_plan, dict)
            and legacy_plan.get("schema_version")
            == LEGACY_CLOSEOUT_PLAN_SCHEMA_VERSION
            and plan.get("projection", {}).get(
                "migration_predecessor_plan_digest"
            )
            == legacy_plan.get("plan_digest")
        )
        recovery_preview = getattr(args, "existing_pr_recovery", None)
        if (
            isinstance(transaction, dict)
            and transaction.get("mode") == "ordinary_publication"
            and isinstance(recovery_preview, dict)
        ):
            if recovery_preview.get("ancestry") == "strict_ancestor":
                transaction = finalization_adopt_provenance_tail_transaction(
                    root,
                    task_dir,
                    plan,
                    transaction,
                    recovery_preview,
                )
            else:
                transaction = finalization_adopt_unbound_equal_head_transaction(
                    root,
                    task_dir,
                    plan,
                    transaction,
                    recovery_preview,
                )
            prior_transaction = transaction
        recovered_legacy_pr, pre_push_remote_head = finalization_pre_mutation_remote_preflight(
            root,
            plan,
            prior_transaction,
            allow_legacy_plan_recovery=legacy_plan_recovery,
            existing_pr_recovery=(
                recovery_preview
                if transaction is None and isinstance(recovery_preview, dict)
                else None
            ),
        )
        if retired_projection_rebound:
            finalization_write_transaction(root, task_dir, transaction)
        if transaction is None:
            if isinstance(recovery_preview, dict):
                if recovered_legacy_pr is None:
                    raise WorkflowError(
                        "Existing PR recovery preview lost its bound PR.", exit_code=2
                    )
                adopted_pr = {
                    "number": recovered_legacy_pr["number"],
                    "url": recovered_legacy_pr["url"],
                    "initial_is_draft": bool(recovery_preview["initial_is_draft"]),
                    "pre_push_remote_head": pre_push_remote_head,
                }
                needs_push = pre_push_remote_head != str(
                    plan["git"].get("publication_head")
                    or plan["git"]["branch_review_commit"]
                )
                transaction = finalization_transaction_from_plan(
                    plan,
                    next_transition="push_content" if needs_push else "bind_pr",
                    pr=recovered_legacy_pr,
                    pre_push_remote_head=pre_push_remote_head if needs_push else None,
                    mode="existing_pr_recovery",
                    adopted_pr=adopted_pr,
                )
            else:
                transaction = finalization_transaction_from_plan(
                    plan,
                    next_transition=("bind_pr" if recovered_legacy_pr else "push_content"),
                    pr=recovered_legacy_pr,
                    pre_push_remote_head=(
                        None if recovered_legacy_pr is not None else pre_push_remote_head
                    ),
                )
            finalization_write_transaction(root, task_dir, transaction)
        else:
            if transaction.get("plan_digest") != plan["plan_digest"]:
                replacement = finalization_transaction_from_plan(
                    plan,
                    next_transition=str(transaction["next_transition"]),
                    pr=(
                        transaction["pr"]
                        if isinstance(transaction.get("pr"), dict)
                        else None
                    ),
                    pre_push_remote_head=(
                        str(transaction["pre_push_remote_head"])
                        if transaction.get("next_transition") == "push_content"
                        and isinstance(transaction.get("pre_push_remote_head"), str)
                        else None
                    ),
                    mode=str(transaction.get("mode") or "ordinary_publication"),
                    adopted_pr=(
                        transaction.get("adopted_pr")
                        if isinstance(transaction.get("adopted_pr"), dict)
                        else None
                    ),
                )
                prior_identity = {
                    key: value
                    for key, value in transaction.items()
                    if key != "plan_digest"
                }
                replacement_identity = {
                    key: value
                    for key, value in replacement.items()
                    if key != "plan_digest"
                }
                if prior_identity != replacement_identity:
                    raise WorkflowError(
                        "Task finalization transaction cannot bind a changed plan identity.",
                        exit_code=2,
                    )
                transaction = replacement
                finalization_write_transaction(root, task_dir, transaction)
            else:
                finalization_validate_transaction_plan(transaction, plan)
        summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
        if summary_path.exists():
            if not summary_path.is_file() or summary_path.is_symlink():
                raise WorkflowError(
                    "Task finalization summary recovery path is unsafe.",
                    exit_code=2,
                )
            try:
                read_and_validate_closeout_final_summary(summary_path, plan)
            except WorkflowError:
                summary_path.unlink()
    ledger = load_issue_scope_ledger(task_dir, task_context)
    if prepared.get("month_supersession") is not None:
        supersession = prepared["month_supersession"]
        if supersession.get("committed") is True:
            push_closeout_branch_if_needed(root, supersession["previous_plan"])
        validate_publish_identity_and_remote_head(
            root, prepared["task"], task_context, plan["git"]["repo"],
            plan["git"]["base_branch"], plan["git"]["head_branch"], plan["git"]["remote"],
        )
        entry_state = apply_active_closeout_month_supersession(root, task_dir, prepared)
    else:
        migration = prepared.get("migration_normalization")
        state_plan = (
            migration["previous_plan"]
            if isinstance(migration, dict)
            and isinstance(migration.get("previous_plan"), dict)
            else plan
        )
        entry_state = resolve_closeout_pre_draft_state(
            root,
            task_dir,
            state_plan,
            ledger,
            require_plan_artifact=not current_finalizer,
        )
        if legacy_plan_recovery and recovered_legacy_pr is not None and entry_state == "prepared":
            entry_state = "content_pushed"
        if not current_finalizer and state_plan is not plan:
            write_json(closeout_plan_path(task_dir), plan)
            if validate_closeout_plan(read_json(closeout_plan_path(task_dir))) != plan:
                raise WorkflowError(
                    "Schema 2.0 closeout migration did not persist the reviewed normalized plan.",
                    exit_code=2,
                )
    if entry_state == "prepared":
        if current_finalizer:
            finalization_pre_mutation_remote_preflight(
                root,
                plan,
                transaction,
            )
        execute_closeout_content_push(
            root,
            task_dir,
            task_context,
            prepared,
            persist_closeout_plan=not current_finalizer,
        )
        entry_state = "content_pushed"
        if current_finalizer:
            transaction = finalization_advance_transaction(
                plan,
                transaction,
                next_transition="bind_pr",
            )
            finalization_write_transaction(root, task_dir, transaction)

    if entry_state == "content_pushed":
        validate_publish_identity_and_remote_head(
            root, prepared["task"], task_context, plan["git"]["repo"],
            plan["git"]["base_branch"], plan["git"]["head_branch"], plan["git"]["remote"],
        )

    validate_closeout_reviewed_content(
        root,
        plan,
        current_head(root),
        include_worktree=True,
    )

    if current_finalizer:
        finalization_pre_mutation_remote_preflight(
            root,
            plan,
            transaction,
        )
    pr = ensure_closeout_bound_pr(root, plan, prepared["body"], transaction if current_finalizer else None)
    if current_finalizer:
        transaction = finalization_advance_transaction(
            plan,
            transaction,
            next_transition="archive",
            pr=pr,
        )
        finalization_write_transaction(root, task_dir, transaction)
    finish_summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    expected_draft = finalization_expected_pr_draft_state(
        transaction,
        current_finalizer=current_finalizer,
    )
    if finish_summary_path.is_file():
        validate_closeout_active_projection(
            root,
            task_dir,
            plan,
        )
        validate_closeout_pull_request_identity(
            root,
            task_dir,
            plan,
            pr,
            expected_draft=expected_draft,
            require_summary=True,
            expected_head=current_head(root),
        )
    else:
        finish_summary_path, _summary = build_final_archive_projection(
            root,
            task_dir,
            prepared,
            pr,
            expected_draft=expected_draft,
        )
    finalization_gate = getattr(args, "finalization_gate", None)
    if isinstance(finalization_gate, dict):
        if (
            finalization_gate.get("route", {}).get("typed_exit") != "ready_for_merge"
            or finalization_gate.get("route", {}).get("output")
            != FINALIZATION_EXECUTOR_OUTPUT_MARKER
        ):
            raise WorkflowError(
                "Task finalization requires the exact private published marker before archive.",
                exit_code=2,
            )
    archived_task_dir, archive_commit = execute_archive_metadata_transaction(
        root,
        task_dir,
        plan,
        bound_pr=pr,
    )
    publish_payload = ensure_closeout_pr_ready(root, plan, bound_pr=pr)
    retired_owner_state: list[str] = []
    if current_finalizer:
        finalization_write_transaction(
            root,
            archived_task_dir,
            finalization_advance_transaction(
                plan,
                transaction,
                next_transition="mark_ready",
                pr=publish_payload["pr"],
            ),
        )
    return {
        "status": "ok",
        "stage": "ready",
        "task_dir": str(task_dir),
        "archived_task_dir": str(archived_task_dir),
        "closeout_plan_digest": plan["plan_digest"],
        "entry_state": entry_state,
        "finish_summary": str(archived_task_dir / finish_summary_path.name),
        "archive_commit": archive_commit,
        "publish": publish_payload,
        "retired_owner_state": retired_owner_state,
    }

def cmd_finish_work(args: argparse.Namespace) -> dict[str, Any]:
    return _cmd_finish_work_impl(args)

FINALIZATION_CONSUMERS = {
    "base_reconciliation_required": {
        "kind": "skill",
        "id": "guru-reconcile-task-base",
    },
    "publication_review_stale": {
        "kind": "skill",
        "id": TASK_PUBLICATION_SKILL_ID,
    },
    "resume_finalization": {
        "kind": "skill",
        "id": FINALIZE_TASK_SKILL_ID,
    },
    "reprepare_required": {
        "kind": "skill",
        "id": FINALIZE_TASK_SKILL_ID,
    },
    "ready_for_merge": {
        "kind": "skill",
        "id": "guru-merge-task-pr",
    },
    "blocked": {
        "kind": "stop",
        "id": "task-finalization-blocked",
    },
}

FINALIZATION_EXECUTOR_OUTPUT_MARKER = {"materialization": "executor"}

FINALIZATION_GATE_SCHEMA_VERSION = "5.0"

FINALIZATION_REPREPARE_ARCHIVE_MONTH = "archive_month_changed"

FINALIZATION_REPREPARE_PROVENANCE_TAIL = "provenance_tail_required"

FINALIZATION_COMMITTED_RECOVERY_STATES = {"archived", "ready"}

FINALIZATION_RESUME_RECOVERY_STATES = {
    "content_pushed",
    "draft_bound",
    "projection_validated",
    "archive_moved",
    "archive_pushed",
    "archived",
}

def finalization_package_root(root: Path) -> Path:
    invoked = os.environ.get("GURU_TEAM_INVOKED_PACKAGE_ROOT", "")
    candidates = [
        Path(invoked) if invoked else None,
        root / "trellis/skills/guru-team/packages/guru-finalize-task",
        root / ".trellis/guru-team/skills/packages/guru-finalize-task",
    ]
    for candidate in candidates:
        if (
            isinstance(candidate, Path)
            and candidate.is_dir()
            and not candidate.is_symlink()
            and candidate.name == FINALIZE_TASK_SKILL_ID
        ):
            return candidate
    raise WorkflowError("The active task finalization package is unavailable.", exit_code=2)

def finalization_json_input(
    root: Path,
    value: str | None,
    label: str,
    *,
    allow_stdin: bool = False,
) -> tuple[dict[str, Any], str]:
    raw = str(value or "").strip()
    if allow_stdin and raw == "-":
        try:
            payload = json.load(sys.stdin)
        except (OSError, json.JSONDecodeError) as exc:
            raise WorkflowError(f"{label} stdin JSON is invalid.", exit_code=2) from exc
        if not isinstance(payload, dict):
            raise WorkflowError(f"{label} stdin must be an object.", exit_code=2)
        return payload, "<stdin>"
    relative = skill_safe_relative(raw)
    if relative is None:
        raise WorkflowError(
            f"{label} must be a safe repo- or package-relative JSON path.",
            exit_code=2,
        )
    package = finalization_package_root(root)
    package_candidate = package / relative
    path = package_candidate if package_candidate.is_file() else root / relative
    boundary = package if path == package_candidate else root
    errors: list[str] = []
    if skill_lstat_path(
        boundary,
        path,
        label,
        errors,
        kind="file",
    ) is None:
        raise WorkflowError(f"{label} is missing or unsafe.", exit_code=2)
    payload = skill_read_json(path, label, errors)
    if errors or not isinstance(payload, dict):
        raise WorkflowError(
            f"{label} is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    locator = repo_relative(root, path) if path.is_relative_to(root) else relative.as_posix()
    return payload, locator

def finalization_interface(root: Path) -> dict[str, Any]:
    package = finalization_package_root(root)
    errors: list[str] = []
    interface = skill_read_json(package / "interface.json", "task finalization interface", errors)
    if errors or not isinstance(interface, dict) or interface.get("id") != FINALIZE_TASK_SKILL_ID:
        raise WorkflowError("Task finalization interface is unavailable.", exit_code=2)
    return interface

def finalization_public_input(
    root: Path,
    value: str | None,
) -> tuple[dict[str, Any], str]:
    payload, locator = finalization_json_input(root, value, "task finalization public input")
    package = finalization_package_root(root)
    interface = finalization_interface(root)
    profiles = interface["public_contracts"]["input"]["profiles"]
    profile = next(
        (
            item
            for item in profiles
            if isinstance(item, dict) and item.get("id") == payload.get("profile")
        ),
        None,
    )
    errors: list[str] = []
    schema = skill_read_schema(
        package / str((profile.get("schema") or {}).get("path") if isinstance(profile, dict) else ""),
        "task finalization public input schema",
        errors,
    )
    if isinstance(schema, dict):
        errors.extend(
            skill_json_schema_validation_errors(
                payload,
                schema,
                "task finalization public input",
            )
        )
    if errors or not isinstance(profile, dict) or not isinstance(schema, dict):
        raise WorkflowError(
            "Task finalization public input failed its declared profile.",
            exit_code=2,
            payload={"errors": errors},
        )
    return payload, locator

def finalization_semantic_review_input(
    root: Path,
    value: str | None,
) -> dict[str, Any]:
    payload, _ = finalization_json_input(
        root,
        value,
        "task finalization semantic review input",
        allow_stdin=True,
    )
    package = finalization_package_root(root)
    errors: list[str] = []
    schema = skill_read_schema(
        package / "schemas/semantic-review-input-3.0.schema.json",
        "task finalization semantic review input schema",
        errors,
    )
    if isinstance(schema, dict):
        errors.extend(
            skill_json_schema_validation_errors(
                payload,
                schema,
                "task finalization semantic review input",
            )
        )
    if errors or not isinstance(schema, dict):
        raise WorkflowError(
            "Task finalization semantic review input is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return payload

def finalization_task_dir(root: Path, public_input: dict[str, Any]) -> Path:
    task_ref = str(public_input.get("task_ref") or "")
    task_dir = resolve_finish_work_task_dir(root, task_ref)
    resolved_ref = repo_relative(root, task_dir)
    if resolved_ref == task_ref:
        return task_dir
    if task_dir_is_archived(root, task_dir):
        transaction_match = finalization_find_transaction_by_task_ref(
            root,
            task_ref,
        )
        if transaction_match is not None:
            transaction, _transaction_path = transaction_match
            if transaction.get("task_ref") == task_ref:
                return task_dir
        if finalization_current_terminal_gate(root, task_dir, task_ref) is not None:
            return task_dir
        if finalization_terminal_projection_gate(root, task_dir, public_input) is not None:
            return task_dir
        plan = finalization_closeout_plan(root, task_dir)
        if (
            plan is not None
            and task_ref == plan["task"]["active_locator"]
            and resolved_ref == plan["task"]["archive_locator"]
        ):
            return task_dir
    if resolved_ref != task_ref:
        raise WorkflowError(
            "Task finalization task_ref does not resolve to the exact task locator.",
            exit_code=2,
        )
    return task_dir

def finalization_transaction_path(root: Path, task_dir: Path) -> Path:
    return (
        runtime_root(root, load_config(root))
        / "finalization-transaction"
        / ai_first_task_checkpoint_key(task_dir)
        / FINALIZATION_TRANSACTION_ARTIFACT
    )

def finalization_transaction_schema(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    schema = skill_read_schema(
        finalization_package_root(root)
        / "schemas/finalization-transaction.schema.json",
        "task finalization transaction",
        errors,
    )
    if errors or not isinstance(schema, dict):
        raise WorkflowError(
            "Task finalization transaction schema is unavailable.",
            exit_code=2,
            payload={"errors": errors},
        )
    return schema

def finalization_transaction_from_plan(
    plan: dict[str, Any],
    *,
    next_transition: str,
    pr: dict[str, Any] | None = None,
    pre_push_remote_head: str | None = None,
    mode: str = "ordinary_publication",
    adopted_pr: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": "3.0",
        "skill_id": FINALIZE_TASK_SKILL_ID,
        "mode": mode,
        "task_ref": plan["task"]["active_locator"],
        "repo_ref": plan["git"]["repo"],
        "base_branch": plan["git"]["base_branch"],
        "branch": plan["git"]["head_branch"],
        "branch_review_commit": plan["git"]["branch_review_commit"],
        "publication_head": (
            plan["git"].get("publication_head")
            or plan["git"]["branch_review_commit"]
        ),
        "plan_digest": plan["plan_digest"],
        "publication": {
            "title": plan["publish"]["title"],
            "body": plan["publish"]["body"],
        },
        "close_issues": plan["review"]["close_issues_reviewed"],
        "next_transition": next_transition,
    }
    if pr is not None:
        payload["pr"] = {
            "number": pr["number"],
            "url": pr["url"],
        }
    if pre_push_remote_head is not None:
        payload["pre_push_remote_head"] = pre_push_remote_head
    if adopted_pr is not None:
        payload["adopted_pr"] = copy.deepcopy(adopted_pr)
    return payload

def finalization_advance_transaction(
    plan: dict[str, Any],
    transaction: dict[str, Any],
    *,
    next_transition: str,
    pr: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return finalization_transaction_from_plan(
        plan,
        next_transition=next_transition,
        pr=pr if pr is not None else (
            transaction.get("pr") if isinstance(transaction.get("pr"), dict) else None
        ),
        mode=str(transaction.get("mode") or "ordinary_publication"),
        adopted_pr=(
            transaction.get("adopted_pr")
            if isinstance(transaction.get("adopted_pr"), dict)
            else None
        ),
    )


def finalization_reprepared_transaction(
    plan: dict[str, Any],
    previous_transaction: dict[str, Any] | None,
    *,
    pre_push_remote_head: str,
) -> dict[str, Any]:
    if (
        isinstance(previous_transaction, dict)
        and previous_transaction.get("mode") == "existing_pr_recovery"
    ):
        adopted_pr = previous_transaction.get("adopted_pr")
        pr = previous_transaction.get("pr")
        if not isinstance(adopted_pr, dict) or not isinstance(pr, dict):
            raise WorkflowError(
                "Existing PR recovery transaction is incomplete during reprepare.",
                exit_code=2,
            )
        return finalization_transaction_from_plan(
            plan,
            next_transition="push_content",
            pr=pr,
            pre_push_remote_head=pre_push_remote_head,
            mode="existing_pr_recovery",
            adopted_pr=adopted_pr,
        )
    return finalization_transaction_from_plan(
        plan,
        next_transition="push_content",
        pre_push_remote_head=pre_push_remote_head,
    )

def finalization_validate_transaction_plan(
    transaction: dict[str, Any],
    plan: dict[str, Any],
) -> None:
    expected = finalization_transaction_from_plan(
        plan,
        next_transition=str(transaction.get("next_transition") or "push_content"),
        pr=(transaction.get("pr") if isinstance(transaction.get("pr"), dict) else None),
        pre_push_remote_head=(
            str(transaction["pre_push_remote_head"])
            if transaction.get("next_transition") == "push_content"
            and isinstance(transaction.get("pre_push_remote_head"), str)
            else None
        ),
        mode=str(transaction.get("mode") or "ordinary_publication"),
        adopted_pr=(
            transaction.get("adopted_pr")
            if isinstance(transaction.get("adopted_pr"), dict)
            else None
        ),
    )
    if transaction != expected:
        raise WorkflowError(
            "Task finalization transaction no longer matches the rebuilt plan.",
            exit_code=2,
        )

def finalization_write_transaction(
    root: Path,
    task_dir: Path,
    payload: dict[str, Any],
) -> Path:
    errors = skill_json_schema_validation_errors(
        payload,
        finalization_transaction_schema(root),
        "task finalization transaction",
    )
    if errors:
        raise WorkflowError(
            "Task finalization transaction is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    path = finalization_transaction_path(root, task_dir)
    write_json(path, payload)
    return path

def finalization_read_transaction(
    root: Path,
    task_dir: Path,
) -> dict[str, Any] | None:
    path = finalization_transaction_path(root, task_dir)
    if not path.exists():
        return None
    if not path.is_file() or path.is_symlink():
        raise WorkflowError(
            "Task finalization transaction is unsafe.", exit_code=2
        )
    payload = read_json(path)
    errors = skill_json_schema_validation_errors(
        payload,
        finalization_transaction_schema(root),
        "task finalization transaction",
    )
    if errors:
        raise WorkflowError(
            "Task finalization transaction is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return payload

def finalization_current_terminal_gate(
    root: Path,
    task_dir: Path,
    task_ref: str,
) -> dict[str, Any] | None:
    """Resolve the adjacent terminal gate without reviving transaction state."""
    if not task_dir_is_archived(root, task_dir) or closeout_plan_path(task_dir).exists():
        return None
    path = task_finalization_path(root, task_dir)
    if not path.exists():
        return None
    if not path.is_file() or path.is_symlink():
        raise WorkflowError(
            "Archived current Finalizer gate is missing or unsafe.", exit_code=2
        )
    gate = finalization_normalize_gate(root, read_json(path))
    identity = gate.get("identity") if isinstance(gate.get("identity"), dict) else {}
    plan_digest = str(identity.get("plan_digest") or "")
    plan_ref = str(identity.get("plan_ref") or "")
    if not plan_ref.startswith("finalization:"):
        return None
    errors = skill_json_schema_validation_errors(
        gate,
        finalization_gate_schema(root),
        "task finalization gate",
    )
    if (
        errors
        or identity.get("task_ref") != task_ref
        or re.fullmatch(r"[0-9a-f]{64}", plan_digest) is None
        or plan_ref != f"finalization:{plan_digest}"
        or re.fullmatch(
            r"[0-9a-f]{40}", str(identity.get("branch_review_commit") or "")
        )
        is None
        or gate.get("route")
        != {
            "typed_exit": "ready_for_merge",
            "consumer": FINALIZATION_CONSUMERS["ready_for_merge"],
            "output": FINALIZATION_EXECUTOR_OUTPUT_MARKER,
        }
    ):
        raise WorkflowError(
            "Archived current Finalizer gate does not bind the terminal transaction.",
            exit_code=2,
            payload={"errors": errors},
        )
    return gate


def finalization_terminal_projection_gate(
    root: Path,
    task_dir: Path,
    public_input: dict[str, Any],
) -> dict[str, Any] | None:
    """Project a retired gate from the committed terminal archive authority."""
    task_ref = str(public_input.get("task_ref") or "")
    archive_locator = repo_relative(root, task_dir)
    if (
        not task_dir_is_archived(root, task_dir)
        or closeout_plan_path(task_dir).exists()
        or task_finalization_path(root, task_dir).exists()
        or finalization_find_transaction_by_task_ref(root, task_ref) is not None
    ):
        return None
    task = task_json(task_dir)
    summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    if task.get("status") != "completed":
        return None
    if not summary_path.is_file() or summary_path.is_symlink():
        return None
    summary = read_json(summary_path)
    validate_finish_summary(summary)
    summary_task = summary.get("task") if isinstance(summary.get("task"), dict) else {}
    summary_git = summary.get("git") if isinstance(summary.get("git"), dict) else {}
    branch_review_commit = str(public_input.get("branch_review_commit") or "")
    commits = summary_git.get("commits") if isinstance(summary_git.get("commits"), list) else []
    if (
        summary_task.get("artifact_dir") != task_ref
        or summary_task.get("archive_dir") != archive_locator
        or re.fullmatch(r"[0-9a-f]{40}", branch_review_commit) is None
        or branch_review_commit not in commits
    ):
        return None
    archive_commit = finalization_terminal_archive_commit(
        root,
        task_ref,
        archive_locator,
        branch_review_commit,
    )
    terminal_digest = canonical_json_sha256(
        {
            "schema_version": "1.0",
            "task_ref": task_ref,
            "archive_locator": archive_locator,
            "branch_review_commit": branch_review_commit,
            "archive_commit": archive_commit,
            "finish_summary_sha256": canonical_json_sha256(summary),
        }
    )
    return {
        "schema_version": FINALIZATION_GATE_SCHEMA_VERSION,
        "skill_id": FINALIZE_TASK_SKILL_ID,
        "identity": {
            "task_ref": task_ref,
            "plan_ref": f"finalization:{terminal_digest}",
            "plan_digest": terminal_digest,
            "branch_review_commit": branch_review_commit,
        },
        "review": {
            "status": "passed",
            "summary": "The committed terminal archive remains the reviewed Ready authority.",
        },
        "route": {
            "typed_exit": "ready_for_merge",
            "consumer": copy.deepcopy(FINALIZATION_CONSUMERS["ready_for_merge"]),
            "output": copy.deepcopy(FINALIZATION_EXECUTOR_OUTPUT_MARKER),
        },
    }


def finalization_terminal_archive_commit(
    root: Path,
    task_ref: str,
    archive_locator: str,
    branch_review_commit: str,
) -> str:
    """Require current HEAD to be the exact reviewed archive metadata commit."""
    archive_commit = current_head(root)
    transaction_parent = closeout_commit_parent(root, archive_commit)
    parent_active_paths = closeout_commit_tracked_task_paths(
        root,
        transaction_parent,
        task_ref,
    )
    expected_archive_paths = {
        f"{archive_locator}/{relative}"
        for relative in CLOSEOUT_ARCHIVE_DURABLE_ARTIFACTS
    }
    archived_paths = closeout_commit_tracked_task_paths(
        root,
        archive_commit,
        archive_locator,
    )
    remaining_active_paths = closeout_commit_tracked_task_paths(
        root,
        archive_commit,
        task_ref,
    )
    committed_paths = closeout_commit_paths(root, archive_commit)
    expected_paths = parent_active_paths | expected_archive_paths
    reviewed_identity = reviewed_content_identity(
        root,
        branch_review_commit,
        include_worktree=False,
    )["sha256"]
    archive_identity = reviewed_content_identity(
        root,
        archive_commit,
        include_worktree=False,
    )["sha256"]
    if (
        not parent_active_paths
        or not is_ancestor(root, branch_review_commit, transaction_parent)
        or archived_paths != expected_archive_paths
        or remaining_active_paths
        or committed_paths != expected_paths
        or archive_identity != reviewed_identity
    ):
        raise WorkflowError(
            "Archived current Finalizer HEAD is not the exact reviewed archive metadata commit.",
            exit_code=2,
            payload={
                "archive_commit": archive_commit,
                "transaction_parent": transaction_parent,
                "expected_paths": sorted(expected_paths),
                "actual_paths": sorted(committed_paths),
            },
        )
    return archive_commit

def finalization_find_transaction_by_task_ref(
    root: Path,
    task_ref: str,
) -> tuple[dict[str, Any], Path] | None:
    owner_root = runtime_root(root, load_config(root)) / "finalization-transaction"
    if not owner_root.exists():
        return None
    if not owner_root.is_dir() or owner_root.is_symlink():
        raise WorkflowError("Task finalization transaction owner root is unsafe.", exit_code=2)
    matches: list[tuple[dict[str, Any], Path]] = []
    for owner_dir in sorted(owner_root.iterdir()):
        if not owner_dir.is_dir() or owner_dir.is_symlink():
            raise WorkflowError("Task finalization transaction owner entry is unsafe.", exit_code=2)
        path = owner_dir / FINALIZATION_TRANSACTION_ARTIFACT
        if not path.exists():
            continue
        if not path.is_file() or path.is_symlink():
            raise WorkflowError("Task finalization transaction is unsafe.", exit_code=2)
        payload = read_json(path)
        errors = skill_json_schema_validation_errors(
            payload,
            finalization_transaction_schema(root),
            "task finalization transaction",
        )
        if errors:
            raise WorkflowError(
                "Task finalization transaction is invalid.",
                exit_code=2,
                payload={"errors": errors},
            )
        if payload.get("task_ref") == task_ref:
            matches.append((payload, path))
    if len(matches) > 1:
        raise WorkflowError(
            "Task finalization found multiple transactions for one task.",
            exit_code=2,
        )
    return matches[0] if matches else None

def finalization_retire_current_state(root: Path, task_dir: Path) -> list[str]:
    retired: list[str] = []
    task_ref = repo_relative(root, task_dir)
    transaction_match = finalization_find_transaction_by_task_ref(root, task_ref)
    candidates = [
        (
            transaction_match[1]
            if transaction_match is not None
            else finalization_transaction_path(root, task_dir)
        ),
        task_finalization_path(root, task_dir),
        task_finalization_transition_path(root, task_dir),
    ]
    for path in candidates:
        if path.is_symlink():
            raise WorkflowError(
                "Task finalization terminal cleanup found unsafe owner state.",
                exit_code=2,
            )
        if path.is_dir():
            shutil.rmtree(path)
            retired.append(repo_relative(root, path))
        elif path.is_file():
            path.unlink()
            retired.append(repo_relative(root, path))
    return retired

def finalization_publication_owner_result(
    root: Path,
    task_dir: Path,
    public_input: dict[str, Any],
    verification: tuple[dict[str, Any], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    del verification
    task_ref = repo_relative(root, task_dir)
    if public_input.get("task_ref") != task_ref:
        raise WorkflowError(
            "Task finalization publication handoff does not match the resolved task.",
            exit_code=2,
        )

    profile = str(public_input.get("profile") or "")
    branch_review_commit = str(public_input.get("branch_review_commit") or "")
    if profile == "publication_ready":
        task = task_json(task_dir)
        if task.get("status") != "in_progress":
            return {
                "owner_status": "stale",
                "branch_review_commit": branch_review_commit,
                "stale_reason": "publication_review_stale",
            }
        repository = task_publication_repository_binding(root, task_dir)
        unexpected = task_publication_unexpected_status_paths(
            repository["status_paths"],
        )
        if unexpected:
            raise WorkflowError(
                "Task finalization found dirty paths outside the reviewed-content boundary.",
                exit_code=2,
                payload={"unexpected_dirty_paths": unexpected},
            )
        task_context = load_task_runtime_identity(task_dir, load_config(root))
        old_base_head = str(task_context.get("base_head_sha") or "")
        base_branch = str(task_context.get("base_branch") or task.get("base_branch") or "")
        selected_base_ref = diff_base_ref(root, base_branch)
        new_base_head = run(["git", "rev-parse", selected_base_ref], cwd=root).stdout.strip()
        if old_base_head != new_base_head:
            task_head = current_head(root)
            if not is_ancestor(root, old_base_head, new_base_head):
                raise WorkflowError("Finalizer base evolution is not an ancestor delta.", exit_code=2)
            return {
                "owner_status": "base_reconciliation_required",
                "task_ref": task_ref,
                "task_head": task_head,
                "publication_head": task_head,
                "selected_base_ref": selected_base_ref,
                "old_base_head": old_base_head,
                "new_base_head": new_base_head,
                "branch_review_commit": branch_review_commit,
                "resume_target": "finalization_resume",
            }
    elif profile == "reprepare_preview":
        publication_head = str(public_input.get("publication_head") or "")
        reason_code = str(public_input.get("reason_code") or "")
        plan = finalization_closeout_plan(root, task_dir)
        if plan is not None:
            plan_reviewed = str(plan["git"]["branch_review_commit"])
            plan_publication = str(
                plan["git"].get("publication_head") or plan_reviewed
            )
            if (
                plan_reviewed != branch_review_commit
                or plan_publication != publication_head
            ):
                return {
                    "owner_status": "stale",
                    "branch_review_commit": branch_review_commit,
                    "stale_reason": "publication_review_stale",
                }
        try:
            target_repo = (
                plan.get("git", {}).get("repo")
                if isinstance(plan, dict)
                and isinstance(plan.get("git"), dict)
                else infer_github_repo(root)
            )
            publication_identity = finalizer_publication_identity(
                root,
                branch_review_commit,
                target_repo,
            )
        except WorkflowError as exc:
            return {
                "owner_status": "stale",
                "branch_review_commit": branch_review_commit,
                "stale_reason": "publication_review_stale",
                "errors": [str(exc)],
            }
        if (
            publication_head != current_head(root)
            or publication_identity["publication_head"] != publication_head
            or (
                reason_code == FINALIZATION_REPREPARE_PROVENANCE_TAIL
                and publication_identity["metadata_tail"] is None
            )
        ):
            return {
                "owner_status": "stale",
                "branch_review_commit": branch_review_commit,
                "stale_reason": "publication_review_stale",
            }
    else:
        transaction = finalization_read_transaction(root, task_dir)
        if transaction is None:
            return {
                "owner_status": "stale",
                "branch_review_commit": branch_review_commit,
                "stale_reason": "publication_review_missing",
            }
        branch_review_commit = str(transaction["branch_review_commit"])
        supplied_commit = public_input.get("branch_review_commit")
        if (
            isinstance(supplied_commit, str)
            and supplied_commit != branch_review_commit
        ):
            return {
                "owner_status": "stale",
                "branch_review_commit": branch_review_commit,
                "stale_reason": "publication_review_stale",
            }
    try:
        reviewed_content_sha256 = reviewed_content_identity(
            root,
            branch_review_commit,
            include_worktree=False,
        )["sha256"]
        continuity_errors = review_branch_content_continuity_errors(
            root,
            task_dir,
            branch_review_commit,
            reviewed_content_sha256,
            current_head(root),
        )
    except WorkflowError as exc:
        continuity_errors = [str(exc)]
    if continuity_errors:
        return {
            "owner_status": "stale",
            "branch_review_commit": branch_review_commit,
            "stale_reason": "publication_review_stale",
            "errors": continuity_errors,
        }
    return {
        "status": "ok",
        "owner_status": "current",
        "typed_exit": "ready",
        "task_ref": task_ref,
        "branch_review_commit": branch_review_commit,
    }

def finalization_prepare_publication_ready(
    public_input: dict[str, Any],
    *,
    existing_plan: dict[str, Any] | None = None,
    transaction: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Select exact Publication authority without inflating reprepare identity."""
    if public_input.get("profile") == "publication_ready":
        return public_input
    if transaction is not None:
        profile = public_input.get("profile")
        if (
            public_input.get("task_ref") != transaction.get("task_ref")
            or (
                profile == "reprepare_preview"
                and (
                    public_input.get("branch_review_commit")
                    != transaction.get("branch_review_commit")
                    or public_input.get("publication_head")
                    != transaction.get("publication_head")
                )
            )
        ):
            raise WorkflowError(
                "Task finalization reprepare input differs from its owner publication authority.",
                exit_code=2,
            )
        publication = transaction["publication"]
        return {
            "profile": "publication_ready",
            "mode": public_input["mode"],
            "task_ref": transaction["task_ref"],
            "branch_review_commit": transaction["branch_review_commit"],
            "pr_title": publication["title"],
            "pr_body": publication["body"],
        }
    if public_input.get("profile") != "reprepare_preview":
        return None
    del existing_plan
    raise WorkflowError(
        "Task finalization reprepare is missing its owner publication authority.",
        exit_code=2,
    )

def finalization_closeout_plan(
    root: Path,
    task_dir: Path,
) -> dict[str, Any] | None:
    plan_path = closeout_plan_path(task_dir)
    if not task_dir_is_archived(root, task_dir):
        if not plan_path.is_file() or plan_path.is_symlink():
            return None
        return validate_closeout_plan_for_migration(read_json(plan_path))
    locator = repo_relative(root, task_dir)
    working_plan: dict[str, Any] | None = None
    if plan_path.exists():
        if not plan_path.is_file() or plan_path.is_symlink():
            raise WorkflowError(
                "Archived finalization verification recovery has an unsafe working-tree plan.",
                exit_code=2,
            )
        working_plan = validate_closeout_plan_for_migration(read_json(plan_path))
    content = closeout_optional_commit_blob_bytes(
        root,
        current_head(root),
        f"{locator}/{CLOSEOUT_PLAN_ARTIFACT}",
    )
    if working_plan is not None:
        if content is not None:
            try:
                committed_plan = validate_closeout_plan_for_migration(
                    json.loads(content.decode("utf-8"))
                )
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise WorkflowError(
                    "Archived finalization verification recovery has an invalid committed plan.",
                    exit_code=2,
                ) from exc
            if committed_plan != working_plan:
                raise WorkflowError(
                    "Archived finalization working-tree plan differs from its committed plan.",
                    exit_code=2,
                )
        return working_plan
    if content is None:
        raise WorkflowError(
            "Archived finalization verification recovery is missing its committed plan.",
            exit_code=2,
        )
    try:
        return validate_closeout_plan_for_migration(
            json.loads(content.decode("utf-8"))
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(
            "Archived finalization verification recovery has an invalid committed plan.",
            exit_code=2,
        ) from exc

def finalization_eval_preview_context(
    root: Path,
    public_input: dict[str, Any],
) -> dict[str, Any] | None:
    if os.environ.get("GURU_TEAM_EVAL_STAGING") != "1":
        return None
    path = root / ".trellis/.runtime/guru-team/evals/finalization-context.json"
    if not path.is_file() or path.is_symlink():
        return None
    payload = read_json(path)
    expected_keys = {
        "schema_version",
        "task_ref",
        "plan_ref",
        "plan_digest",
        "branch_review_commit",
        "publication_head",
        "archive_locator",
        "repo_ref",
        "remote",
        "head_branch",
        "publication_status",
        "publication_stale_reason",
        "transaction_state",
    }
    states = {
        "prepared",
        "content_pushed",
        "draft_bound",
        "projection_validated",
        "archive_moved",
        "archive_pushed",
        "archived",
        "ready",
        "reprepare_required",
    }
    if (
        set(payload) != expected_keys
        or payload.get("schema_version") != "2.0"
        or payload.get("task_ref") != public_input.get("task_ref")
        or not re.fullmatch(r"closeout-plan:[0-9a-f]{64}", str(payload.get("plan_ref") or ""))
        or payload.get("plan_ref") != f"closeout-plan:{payload.get('plan_digest')}"
        or not re.fullmatch(r"[0-9a-f]{64}", str(payload.get("plan_digest") or ""))
        or not re.fullmatch(
            r"[0-9a-f]{40}", str(payload.get("branch_review_commit") or "")
        )
        or not re.fullmatch(
            r"[0-9a-f]{40}", str(payload.get("publication_head") or "")
        )
        or normalize_github_repository(payload.get("repo_ref")) != payload.get("repo_ref")
        or payload.get("publication_status") not in {"current", "stale"}
        or (
            payload.get("publication_status") == "current"
            and payload.get("publication_stale_reason") is not None
        )
        or (
            payload.get("publication_status") == "stale"
            and payload.get("publication_stale_reason")
            not in {
                "publication_review_missing",
                "publication_review_stale",
            }
        )
        or payload.get("transaction_state") not in states
        or (
            payload.get("transaction_state") == "reprepare_required"
            and (
                public_input.get("profile") != "reprepare_preview"
                or public_input.get("reason_code") not in {
                    FINALIZATION_REPREPARE_ARCHIVE_MONTH,
                    FINALIZATION_REPREPARE_PROVENANCE_TAIL,
                }
            )
        )
    ):
        raise WorkflowError(
            "Task finalization eval objective facts are invalid.",
            exit_code=2,
        )
    task_dir = finalization_task_dir(root, public_input)
    if payload["transaction_state"] == "ready":
        archive_relative = skill_safe_relative(str(payload["archive_locator"]))
        archive_dir = root / archive_relative if archive_relative is not None else None
        if (
            archive_relative is None
            or archive_relative.as_posix() != payload["archive_locator"]
            or archive_dir is None
            or not archive_dir.is_dir()
            or archive_dir.is_symlink()
        ):
            raise WorkflowError(
                "Task finalization eval terminal archive locator is unavailable.",
                exit_code=2,
            )
        task_dir = archive_dir
    plan = {
        "plan_digest": payload["plan_digest"],
        "git": {
            "repo": payload["repo_ref"],
            "remote": payload["remote"],
            "base_branch": "main",
            "head_branch": payload["head_branch"],
            "branch_review_commit": payload["branch_review_commit"],
            "reviewed_content_head": payload["branch_review_commit"],
            "publication_head": payload["publication_head"],
        },
        "review": {"close_issues_reviewed": [174]},
        "task": {
            "active_locator": payload["task_ref"],
            "archive_locator": payload["archive_locator"],
        },
    }
    return {
        "task_dir": task_dir,
        "task_context": None,
        "prepared": None,
        "plan": plan,
        "plan_ref": payload["plan_ref"],
        "transaction_state": payload["transaction_state"],
        "published_transition_complete": payload["transaction_state"] == "ready",
        "published_pr": (
            {
                "number": 118,
                "url": f"https://github.com/{payload['repo_ref']}/pull/118",
                "headRefOid": payload["publication_head"],
            }
            if payload["transaction_state"] == "ready"
            else None
        ),
        "publication": {"owner_status": "current"},
        "publication_status": payload["publication_status"],
        "publication_stale_reason": payload["publication_stale_reason"],
        "publication_branch_review_commit": payload["branch_review_commit"],
        "reprepare_reason_code": (
            public_input.get("reason_code")
            if payload["transaction_state"] == "reprepare_required"
            else None
        ),
        "verification": None,
    }

def finalization_archived_published_facts(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any] | None = None,
) -> tuple[bool, dict[str, Any] | None]:
    transaction = transaction or resolve_committed_closeout_archive_transaction(
        root,
        plan,
    )
    if transaction is None:
        raise WorkflowError(
            "Archived task finalization is not the exact plan transaction.",
            exit_code=2,
        )
    summary_pr = transaction.get("summary_pr")
    if not isinstance(summary_pr, dict):
        raise WorkflowError(
            "Archived task finalization is missing its committed PR identity.",
            exit_code=2,
        )
    git = plan["git"]
    pr = resolve_closeout_pull_request(
        root,
        git["repo"],
        git["head_branch"],
        git["base_branch"],
        git["remote"],
    )
    if pr is None:
        raise WorkflowError(
            "Archived task finalization requires the bound pull request.",
            exit_code=2,
        )
    local_head = current_head(root)
    validate_closeout_remote_pull_request_identity(
        plan,
        pr,
        expected_draft=bool(pr["isDraft"]),
        bound_pr=summary_pr,
    )
    complete = (
        pr.get("isDraft") is False
        and closeout_remote_branch_head(root, plan) == local_head
        and pr.get("headRefOid") == local_head
    )
    return complete, pr if complete else None

def finalization_archived_owner_results(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
    public_input: dict[str, Any],
) -> tuple[dict[str, Any], tuple[dict[str, Any], dict[str, Any]] | None]:
    del root, plan, transaction, public_input
    return {"owner_status": "current"}, None

def finalization_current_archived_context(
    root: Path,
    task_dir: Path,
    public_input: dict[str, Any],
    transaction: dict[str, Any],
) -> dict[str, Any]:
    task_ref = str(public_input.get("task_ref") or "")
    archive_locator = repo_relative(root, task_dir)
    next_transition = transaction.get("next_transition")
    if (
        transaction.get("task_ref") != task_ref
        or next_transition not in {"archive", "push_archive", "mark_ready"}
        or not isinstance(transaction.get("pr"), dict)
        or closeout_plan_path(task_dir).exists()
    ):
        raise WorkflowError(
            "Archived current Finalizer transaction is incomplete or legacy-bound.",
            exit_code=2,
        )
    task = task_json(task_dir)
    if task.get("status") != "completed":
        raise WorkflowError(
            "Archived current Finalizer task is not completed.",
            exit_code=2,
        )
    remote = str(publish_config(load_config(root)).get("remote") or "origin")
    repo = validate_github_remote_repository(
        root,
        remote,
        str(transaction["repo_ref"]),
    )
    pr = resolve_closeout_pull_request(
        root,
        repo,
        str(transaction["branch"]),
        str(transaction["base_branch"]),
        remote,
    )
    bound_pr = transaction["pr"]
    adopted_pr = transaction.get("adopted_pr")
    expected_draft = (
        bool(adopted_pr.get("initial_is_draft"))
        if next_transition != "mark_ready" and isinstance(adopted_pr, dict)
        else False
    )
    if (
        pr is None
        or pr.get("number") != bound_pr.get("number")
        or pr.get("url")
        != canonical_pull_request_url(repo, int(bound_pr["number"]), bound_pr.get("url"))
        or pr.get("isDraft") is not expected_draft
    ):
        raise WorkflowError(
            "Archived current Finalizer pull request is not the exact Ready transaction.",
            exit_code=2,
        )
    ready_head = str(pr.get("headRefOid") or "")
    local_head = current_head(root)
    remote_head = closeout_remote_branch_head(
        root,
        {"git": {"remote": remote, "head_branch": transaction["branch"]}},
    )
    if (
        re.fullmatch(r"[0-9a-f]{40}", ready_head) is None
        or local_head != remote_head
        or local_head != ready_head
    ):
        raise WorkflowError(
            "Archived current Finalizer local, remote and Ready PR heads differ.",
            exit_code=2,
        )
    summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    if not summary_path.is_file() or summary_path.is_symlink():
        raise WorkflowError(
            "Archived current Finalizer summary is missing or unsafe.",
            exit_code=2,
        )
    summary = read_json(summary_path)
    validate_finish_summary(summary)
    if (
        summary.get("task", {}).get("artifact_dir") != task_ref
        or summary.get("task", {}).get("archive_dir") != archive_locator
        or summary.get("github", {}).get("pr_url") != pr.get("url")
        or summary.get("index", {}).get("search_terms", {}).get("pr_refs")
        != [f"PR #{pr['number']}"]
    ):
        raise WorkflowError(
            "Archived current Finalizer summary does not bind the Ready PR transaction.",
            exit_code=2,
        )
    plan = {
        "plan_digest": transaction["plan_digest"],
        "git": {
            "repo": repo,
            "remote": remote,
            "base_branch": transaction["base_branch"],
            "head_branch": transaction["branch"],
            "branch_review_commit": transaction["branch_review_commit"],
            "reviewed_content_head": transaction["branch_review_commit"],
        "publication_head": local_head,
        },
        "marketplace": {"required": "verification_ref" in transaction},
        "publish": copy.deepcopy(transaction["publication"]),
        "review": {
            "close_issues_reviewed": transaction["close_issues"],
        },
        "task": {
            "active_locator": task_ref,
            "archive_locator": archive_locator,
        },
    }
    return {
        "task_dir": task_dir,
        "task_context": None,
        "prepared": None,
        "plan": plan,
        "plan_ref": f"finalization:{transaction['plan_digest']}",
        "transaction_state": "ready" if next_transition == "mark_ready" else "archived",
        "published_transition_complete": next_transition == "mark_ready",
        "published_pr": pr if next_transition == "mark_ready" else None,
        "publication": {"owner_status": "current"},
        "publication_status": "current",
        "publication_stale_reason": None,
        "publication_branch_review_commit": transaction["branch_review_commit"],
        "reprepare_reason_code": None,
        "verification": None,
        "publication_mode": str(transaction.get("mode") or "ordinary_publication"),
        "existing_pr_recovery": copy.deepcopy(transaction.get("adopted_pr")),
    }

def finalization_current_terminal_context(
    root: Path,
    task_dir: Path,
    public_input: dict[str, Any],
    gate: dict[str, Any],
) -> dict[str, Any]:
    """Rebuild the checked Ready context after a no-reentry Finalizer run."""
    identity = gate["identity"]
    task_ref = str(public_input.get("task_ref") or "")
    archive_locator = repo_relative(root, task_dir)
    task = task_json(task_dir)
    summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
    if task.get("status") != "completed":
        raise WorkflowError(
            "Archived current Finalizer task is not completed.", exit_code=2
        )
    if not summary_path.is_file() or summary_path.is_symlink():
        raise WorkflowError(
            "Archived current Finalizer summary is missing or unsafe.", exit_code=2
        )
    summary = read_json(summary_path)
    validate_finish_summary(summary)
    ledger = load_issue_scope_ledger(task_dir, {})
    close_issues_reviewed = sorted(set(issue_numbers(ledger["close_issues"])))
    summary_task = summary.get("task") if isinstance(summary.get("task"), dict) else {}
    summary_git = summary.get("git") if isinstance(summary.get("git"), dict) else {}
    summary_github = (
        summary.get("github") if isinstance(summary.get("github"), dict) else {}
    )
    summary_commits = (
        summary_git.get("commits") if isinstance(summary_git.get("commits"), list) else []
    )
    search_terms = (
        summary.get("index", {}).get("search_terms", {})
        if isinstance(summary.get("index"), dict)
        and isinstance(summary.get("index", {}).get("search_terms"), dict)
        else {}
    )
    branch = str(task.get("branch") or "")
    base_branch = str(task.get("base_branch") or "")
    if (
        identity.get("task_ref") != task_ref
        or public_input.get("branch_review_commit")
        != identity.get("branch_review_commit")
        or summary_task.get("artifact_dir") != task_ref
        or summary_task.get("archive_dir") != archive_locator
        or summary_git.get("branch") != branch
        or summary_git.get("base_branch") != base_branch
        or identity.get("branch_review_commit") not in summary_commits
    ):
        raise WorkflowError(
            "Archived current Finalizer summary does not bind the terminal gate.",
            exit_code=2,
        )
    archive_commit = finalization_terminal_archive_commit(
        root,
        task_ref,
        archive_locator,
        str(identity.get("branch_review_commit") or ""),
    )
    remote = str(publish_config(load_config(root)).get("remote") or "origin")
    repo = normalize_github_repository(infer_github_repo(root))
    repo = validate_github_remote_repository(root, remote, repo)
    pr = resolve_closeout_pull_request(
        root,
        repo,
        branch,
        base_branch,
        remote,
    )
    if pr is None:
        raise WorkflowError(
            "Archived current Finalizer requires the bound Ready pull request.",
            exit_code=2,
        )
    pr_url, pr_number = parse_canonical_pull_request_url(
        repo, summary_github.get("pr_url")
    )
    ready_head = str(pr.get("headRefOid") or "")
    local_head = current_head(root)
    archive_status = run_stdout(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", archive_locator],
        cwd=root,
    )
    reviewed_is_ancestor = run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            str(identity.get("branch_review_commit") or ""),
            local_head,
        ],
        cwd=root,
        check=False,
    ).returncode == 0
    remote_head = closeout_remote_branch_head(
        root,
        {"git": {"remote": remote, "head_branch": branch}},
    )
    if (
        pr.get("number") != pr_number
        or pr.get("url") != pr_url
        or pr.get("isDraft") is not False
        or pr.get("title") != public_input.get("pr_title")
        or pr.get("body") != public_input.get("pr_body")
        or re.fullmatch(r"[0-9a-f]{40}", ready_head) is None
        or local_head != remote_head
        or local_head != ready_head
        or local_head != archive_commit
        or archive_status
        or not reviewed_is_ancestor
        or search_terms.get("pr_refs") != [f"PR #{pr_number}"]
    ):
        raise WorkflowError(
            "Archived current Finalizer live Ready facts do not match its terminal gate.",
            exit_code=2,
        )
    plan = {
        "plan_digest": identity["plan_digest"],
        "git": {
            "repo": repo,
            "remote": remote,
            "base_branch": base_branch,
            "head_branch": branch,
            "branch_review_commit": identity["branch_review_commit"],
            "reviewed_content_head": identity["branch_review_commit"],
            "publication_head": ready_head,
        },
        "marketplace": {"required": False},
        "publish": {
            "title": public_input["pr_title"],
            "body": public_input["pr_body"],
        },
        "review": {"close_issues_reviewed": close_issues_reviewed},
        "task": {
            "active_locator": task_ref,
            "archive_locator": archive_locator,
        },
    }
    return {
        "task_dir": task_dir,
        "task_context": None,
        "prepared": None,
        "plan": plan,
        "plan_ref": identity["plan_ref"],
        "transaction_state": "ready",
        "published_transition_complete": True,
        "published_pr": pr,
        "publication": {"owner_status": "current"},
        "publication_status": "current",
        "publication_stale_reason": None,
        "publication_branch_review_commit": identity["branch_review_commit"],
        "reprepare_reason_code": None,
        "verification": None,
        "publication_mode": "ordinary_publication",
        "existing_pr_recovery": None,
    }

def finalization_preview_context(
    root: Path,
    args: argparse.Namespace,
    public_input: dict[str, Any],
) -> dict[str, Any]:
    official_after_archive_hook_state(root)
    eval_context = finalization_eval_preview_context(root, public_input)
    if eval_context is not None:
        return eval_context
    task_dir = finalization_task_dir(root, public_input)
    archived = task_dir_is_archived(root, task_dir)
    config = load_config(root)
    reprepare_reason_code: str | None = None
    transaction_rebind_recovery: dict[str, Any] | None = None
    if archived:
        transaction_match = finalization_find_transaction_by_task_ref(
            root,
            str(public_input.get("task_ref") or ""),
        )
        if transaction_match is not None:
            return finalization_current_archived_context(
                root,
                task_dir,
                public_input,
                transaction_match[0],
            )
        terminal_gate = finalization_current_terminal_gate(
            root,
            task_dir,
            str(public_input.get("task_ref") or ""),
        )
        if terminal_gate is not None:
            return finalization_current_terminal_context(
                root,
                task_dir,
                public_input,
                terminal_gate,
            )
        terminal_projection_gate = finalization_terminal_projection_gate(
            root,
            task_dir,
            public_input,
        )
        if terminal_projection_gate is not None:
            return finalization_current_terminal_context(
                root,
                task_dir,
                public_input,
                terminal_projection_gate,
            )
        plan = finalization_closeout_plan(root, task_dir)
        if plan is None:
            raise WorkflowError(
                "Archived task finalization is missing its immutable plan.",
                exit_code=2,
            )
        transaction = resolve_committed_closeout_archive_transaction(root, plan)
        if transaction is None:
            raise WorkflowError(
                "Archived task finalization is not the exact plan transaction.",
                exit_code=2,
            )
        publication, verification = finalization_archived_owner_results(
            root,
            plan,
            transaction,
            public_input,
        )
        published_transition_complete, published_pr = (
            finalization_archived_published_facts(root, plan, transaction)
        )
        state = "ready" if published_transition_complete else "archived"
        prepared = None
        task_context = None
    else:
        current_transaction = finalization_read_transaction(root, task_dir)
        verification = None
        publication = finalization_publication_owner_result(
            root,
            task_dir,
            public_input,
            verification,
        )
        if publication.get("owner_status") == "base_reconciliation_required":
            return {
                "task_dir": task_dir,
                "task_context": None,
                "prepared": None,
                "plan": None,
                "plan_ref": None,
                "transaction_state": "base_reconciliation_required",
                "publication": publication,
                "publication_status": "current",
                "publication_stale_reason": None,
                "publication_branch_review_commit": publication["branch_review_commit"],
                "base_reconciliation": publication,
                "verification": None,
            }
        if publication.get("owner_status") == "stale":
            return {
                "task_dir": task_dir,
                "task_context": None,
                "prepared": None,
                "plan": None,
                "plan_ref": None,
                "transaction_state": "publication_review_stale",
                "publication": publication,
                "publication_status": "stale",
                "publication_stale_reason": publication["stale_reason"],
                "publication_branch_review_commit": publication.get(
                    "branch_review_commit"
                ),
                "verification": None,
            }
        published_transition_complete = False
        published_pr = None
        task_context = load_task_runtime_identity(task_dir, config)
        assert_workspace_boundary(root, config, task_context, task_dir)
        task = task_json(task_dir)
        if task.get("status") == "completed" and closeout_plan_path(task_dir).is_file():
            plan = validate_closeout_plan_for_migration(
                read_json(closeout_plan_path(task_dir))
            )
            state = "archive_moved"
            prepared = None
        else:
            existing_plan_for_payload = None
            prepared = prepare_closeout(
                root,
                args,
                config,
                task_dir,
                task_context,
                publication_ready=finalization_prepare_publication_ready(
                    public_input,
                    existing_plan=existing_plan_for_payload,
                    transaction=current_transaction,
                ),
                allowed_current_gate=getattr(
                    args,
                    "_finalization_checked_gate",
                    None,
                ),
                current_finalizer=True,
            )
            plan = prepared["plan"]
            if current_transaction is not None:
                try:
                    finalization_validate_transaction_plan(
                        current_transaction,
                        plan,
                    )
                except WorkflowError:
                    if (
                        current_transaction.get("mode") == "existing_pr_recovery"
                        and current_transaction.get("next_transition")
                        in {"archive", "push_archive", "mark_ready"}
                    ):
                        current_transaction = (
                            finalization_rebind_retired_projection_transaction(
                                current_transaction,
                                plan,
                            )
                        )
                    elif (
                        current_transaction.get("mode") == "ordinary_publication"
                        and current_transaction.get("next_transition") == "push_content"
                        and current_transaction.get("pr") is None
                        and current_transaction.get("adopted_pr") is None
                    ):
                        transaction_rebind_recovery = (
                            classify_provenance_tail_transaction_rebind(
                                root,
                                plan,
                                current_transaction,
                            )
                        )
                        if transaction_rebind_recovery is None:
                            base_evolution = (
                                finalizer_current_transaction_base_evolution_supersession_preflight(
                                    root,
                                    task_dir,
                                    current_transaction,
                                    plan,
                                    allowed_gate=getattr(
                                        args,
                                        "_finalization_checked_gate",
                                        None,
                                    ),
                                )
                            )
                            prepared["pre_pr_reprepare"] = {
                                "previous_transaction": copy.deepcopy(current_transaction),
                                "prior_state": "content_pushed",
                                "base_evolution": base_evolution,
                            }
                    else:
                        base_evolution = (
                            finalizer_current_transaction_base_evolution_supersession_preflight(
                                root,
                                task_dir,
                                current_transaction,
                                plan,
                                allowed_gate=getattr(
                                    args,
                                    "_finalization_checked_gate",
                                    None,
                                ),
                            )
                        )
                        prepared["pre_pr_reprepare"] = {
                            "previous_transaction": copy.deepcopy(current_transaction),
                            "prior_state": "content_pushed",
                            "base_evolution": base_evolution,
                        }
            if prepared.get("month_supersession") is not None:
                state = "reprepare_required"
                reprepare_reason_code = FINALIZATION_REPREPARE_ARCHIVE_MONTH
            elif prepared.get("pre_pr_reprepare") is not None:
                state = "reprepare_required"
                reprepare_reason_code = FINALIZATION_REPREPARE_PROVENANCE_TAIL
            else:
                migration = prepared.get("migration_normalization")
                state_plan = (
                    migration["previous_plan"]
                    if isinstance(migration, dict)
                    and isinstance(migration.get("previous_plan"), dict)
                    else plan
                )
                state = resolve_closeout_pre_draft_state(
                    root,
                    task_dir,
                    state_plan,
                    prepared["ledger"],
                    require_plan_artifact=False,
                )
                if (
                    public_input.get("profile") == "reprepare_preview"
                    and public_input.get("reason_code")
                    == FINALIZATION_REPREPARE_PROVENANCE_TAIL
                    and state == "content_pushed"
                ):
                    remote_head = closeout_remote_branch_head(root, plan)
                    publication_head = str(
                        plan["git"].get("publication_head")
                        or plan["git"]["branch_review_commit"]
                    )
                    if remote_head != publication_head:
                        if remote_head and is_ancestor(root, remote_head, publication_head):
                            state = "prepared"
                        else:
                            raise WorkflowError(
                                "Reprepared closeout remote HEAD is not the immutable publication ancestor.",
                                exit_code=2,
                                payload={
                                    "remote_head": remote_head,
                                    "publication_head": publication_head,
                                },
                            )
    existing_pr_recovery: dict[str, Any] | None = None
    if not archived and isinstance(plan, dict):
        if transaction_rebind_recovery is not None:
            state = "existing_pr_recovery"
            existing_pr_recovery = transaction_rebind_recovery
        else:
            state, existing_pr_recovery = finalization_existing_pr_recovery_context(
                root, plan, current_transaction, state
            )
    if (
        not archived
        and isinstance(prepared, dict)
        and state in {"prepared", "content_pushed"}
        and prepared.get("metadata_tail") is None
        and finalizer_pre_pr_provenance_tail_applies(
            root,
            plan,
            current_transaction,
        )
    ):
        state = "reprepare_required"
        reprepare_reason_code = FINALIZATION_REPREPARE_PROVENANCE_TAIL
    plan_ref = (
        f"closeout-plan:{plan['plan_digest']}"
        if archived
        else f"finalization:{plan['plan_digest']}"
    )
    input_plan_ref = public_input.get("plan_ref")
    migration = (
        prepared.get("migration_normalization")
        if isinstance(prepared, dict)
        else None
    )
    migration_plan_ref = (
        f"closeout-plan:{migration['previous_plan']['plan_digest']}"
        if isinstance(migration, dict)
        and isinstance(migration.get("previous_plan"), dict)
        else None
    )
    if (
        isinstance(input_plan_ref, str)
        and input_plan_ref not in {plan_ref, migration_plan_ref}
    ):
        raise WorkflowError(
            "Task finalization plan_ref does not match the current immutable plan.",
            exit_code=2,
        )
    return {
        "task_dir": task_dir,
        "task_context": task_context,
        "prepared": prepared,
        "plan": plan,
        "plan_ref": plan_ref,
        "transaction_state": state,
        "published_transition_complete": published_transition_complete,
        "published_pr": published_pr,
        "publication": publication,
        "publication_status": "current",
        "publication_stale_reason": None,
        "publication_branch_review_commit": plan["git"]["branch_review_commit"],
        "reprepare_reason_code": reprepare_reason_code,
        "verification": verification,
        "publication_mode": (
            "existing_pr_recovery"
            if existing_pr_recovery is not None
            else "ordinary_publication"
        ),
        "existing_pr_recovery": existing_pr_recovery,
    }

def cmd_preview_finalization(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    public_input, input_locator = finalization_public_input(root, args.input)
    context = finalization_preview_context(root, args, public_input)
    return finalization_preview_receipt(root, public_input, input_locator, context)


def finalization_confirmation_projection(
    public_input: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any] | None:
    plan = context.get("plan")
    if not isinstance(plan, dict):
        return None
    publication_mode = str(
        context.get("publication_mode")
        or (
            "existing_pr_recovery"
            if isinstance(context.get("existing_pr_recovery"), dict)
            else "ordinary_publication"
        )
    )
    side_effects = (
        [
            "bind_existing_pr_transaction",
            "push_or_preserve_exact_publication_head",
            "converge_or_preserve_pr_metadata",
            "archive",
            "push_archive",
            "mark_or_preserve_ready",
            "verify_three_way_head",
        ]
        if publication_mode == "existing_pr_recovery"
        else [
            "push_exact_publication_head",
            "create_draft_pr",
            "archive",
            "push_archive",
            "mark_ready",
            "verify_three_way_head",
        ]
    )
    return {
        "schema_version": "1.0",
        "task_ref": str(public_input.get("task_ref") or plan["task"]["active_locator"]),
        "repo_ref": plan["git"]["repo"],
        "base_branch": plan["git"]["base_branch"],
        "head_branch": plan["git"]["head_branch"],
        "branch_review_commit": plan["git"]["branch_review_commit"],
        "pr_title": plan["publish"]["title"],
        "pr_body": plan["publish"]["body"],
        "close_issues": list(plan["review"]["close_issues_reviewed"]),
        "publication_mode": publication_mode,
        "side_effects": side_effects,
    }


def finalization_confirmation_identity(
    public_input: dict[str, Any],
    context: dict[str, Any],
) -> str | None:
    projection = finalization_confirmation_projection(public_input, context)
    return canonical_json_sha256(projection) if projection is not None else None


def finalization_preview_receipt(
    root: Path,
    public_input: dict[str, Any],
    input_locator: str,
    context: dict[str, Any],
) -> dict[str, Any]:
    plan = context["plan"]
    if plan is None:
        receipt = {
            "schema_version": "1.0",
            "status": "ok",
            "side_effects": False,
            "input_locator": input_locator,
            "profile": public_input["profile"],
            "mode": public_input["mode"],
            "task_ref": public_input["task_ref"],
            "plan_ref": None,
            "closeout_plan": None,
            "closeout_plan_bytes_sha256": None,
            "closeout_plan_digest": None,
            "branch_review_commit": context.get(
                "publication_branch_review_commit"
            ),
            "transaction_state": context["transaction_state"],
            "publication_status": context["publication_status"],
            "publication_stale_reason": context["publication_stale_reason"],
            "expected_actions": [],
            "publication_mode": "ordinary_publication",
            "existing_pr_recovery": None,
            "confirmation_identity": None,
        }
    else:
        receipt = {
            "schema_version": "1.0",
            "status": "ok",
            "side_effects": False,
            "input_locator": input_locator,
            "profile": public_input["profile"],
            "mode": public_input["mode"],
            "task_ref": public_input["task_ref"],
            "plan_ref": context["plan_ref"],
            "closeout_plan": plan,
            "closeout_plan_bytes_sha256": hashlib.sha256(
                closeout_json_artifact_bytes(plan)
            ).hexdigest(),
            "closeout_plan_digest": plan["plan_digest"],
            "branch_review_commit": plan["git"]["branch_review_commit"],
            "transaction_state": context["transaction_state"],
            "publication_status": context["publication_status"],
            "publication_stale_reason": context["publication_stale_reason"],
            "publication_mode": context.get("publication_mode", "ordinary_publication"),
            "existing_pr_recovery": copy.deepcopy(context.get("existing_pr_recovery")),
            "expected_actions": (
                [
                    "bind_existing_pr_transaction",
                    "push_exact_publication_head"
                    if context.get("existing_pr_recovery", {}).get("push_required")
                    else "preserve_existing_remote_head",
                    "converge_pr_metadata"
                    if context.get("existing_pr_recovery", {}).get("metadata_update_required")
                    else "preserve_current_pr_metadata",
                    "archive",
                    "push_archive",
                    context.get("existing_pr_recovery", {}).get("ready_action"),
                    "verify_three_way_head",
                ]
                if context.get("existing_pr_recovery") is not None
                else list(CLOSEOUT_TRANSITIONS[1:])
            ),
            "confirmation_identity": finalization_confirmation_identity(
                public_input,
                context,
            ),
        }
    errors: list[str] = []
    schema = skill_read_schema(
        finalization_package_root(root) / "schemas/finalization-preview-1.0.schema.json",
        "task finalization preview receipt",
        errors,
    )
    if isinstance(schema, dict):
        errors.extend(
            skill_json_schema_validation_errors(
                receipt,
                schema,
                "task finalization preview receipt",
            )
        )
    if errors or not isinstance(schema, dict):
        raise WorkflowError(
            "Task finalization preview receipt is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return receipt

def finalization_output_contract(
    root: Path,
    exit_id: str,
) -> dict[str, Any]:
    package = finalization_package_root(root)
    interface = finalization_interface(root)
    schema, _ = stage0_output_contract(
        FINALIZE_TASK_SKILL_ID,
        package,
        interface,
        exit_id,
    )
    return schema

def finalization_reprepare_public_output(
    root: Path,
    *,
    task_ref: str,
    reason_code: str,
    branch_review_commit: str,
    publication_head: str,
) -> dict[str, Any]:
    payload = {
        "exit_id": "reprepare_required",
        "task_ref": task_ref,
        "reason_code": reason_code,
        "branch_review_commit": branch_review_commit,
        "publication_head": publication_head,
    }
    errors = skill_json_schema_validation_errors(
        payload,
        finalization_output_contract(root, "reprepare_required"),
        "task finalization reprepare_required output",
    )
    if errors:
        raise WorkflowError(
            "Task finalization reprepare output is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return payload

def finalization_route_branch_review_commit(
    context: dict[str, Any],
    exit_id: str,
) -> str | None:
    if exit_id == "publication_review_stale":
        value = context.get("publication_branch_review_commit")
        return str(value) if isinstance(value, str) else None
    plan = context.get("plan")
    if isinstance(plan, dict):
        return str(plan["git"]["branch_review_commit"])
    return None

def finalization_validate_route(
    root: Path,
    public_input: dict[str, Any],
    context: dict[str, Any],
    route: dict[str, Any],
    *,
    allow_pending_transition: bool = False,
) -> None:
    exit_id = str(route.get("typed_exit") or "")
    if route.get("consumer") != FINALIZATION_CONSUMERS.get(exit_id):
        raise WorkflowError(
            "Task finalization selected consumer does not match the typed exit.",
            exit_code=2,
        )
    output = route.get("output")
    if not isinstance(output, dict):
        raise WorkflowError("Task finalization route output must be an object.", exit_code=2)
    plan = context["plan"]
    state = context["transaction_state"]
    executor_materialized = output == FINALIZATION_EXECUTOR_OUTPUT_MARKER
    if executor_materialized and exit_id not in {"ready_for_merge", "reprepare_required"}:
        raise WorkflowError(
            "Only ready_for_merge or reprepare_required may defer public output to the deterministic executor.",
            exit_code=2,
        )
    if exit_id == "ready_for_merge" and not executor_materialized:
        raise WorkflowError(
            "The persisted ready_for_merge route must retain the exact private executor marker.",
            exit_code=2,
        )
    if (
        exit_id == "reprepare_required"
        and context.get("reprepare_reason_code") == FINALIZATION_REPREPARE_PROVENANCE_TAIL
        and not executor_materialized
    ):
        raise WorkflowError(
            "Provenance reprepare must retain the executor marker until publication_head exists.",
            exit_code=2,
        )
    if (
        exit_id == "reprepare_required"
        and context.get("reprepare_reason_code") == FINALIZATION_REPREPARE_ARCHIVE_MONTH
        and executor_materialized
    ):
        raise WorkflowError(
            "Archive-month reprepare must retain its complete current public output.",
            exit_code=2,
        )
    if executor_materialized and not (
        allow_pending_transition
        or (
            state in FINALIZATION_COMMITTED_RECOVERY_STATES
            and context.get("published_transition_complete") is True
        )
    ):
        raise WorkflowError(
            "The executor marker is not valid before its checked transition.",
            exit_code=2,
        )
    if not executor_materialized:
        schema = finalization_output_contract(root, exit_id)
        errors = skill_json_schema_validation_errors(
            output,
            schema,
            f"task finalization route output {exit_id}",
        )
        if errors:
            raise WorkflowError(
                "Task finalization route output is invalid.",
                exit_code=2,
                payload={"errors": errors},
            )
        if exit_id == "base_reconciliation_required":
            facts = context.get("base_reconciliation")
            if not isinstance(facts, dict) or output != {
                "exit_id": exit_id,
                **{
                    key: facts[key]
                    for key in (
                        "task_ref",
                        "task_head",
                        "publication_head",
                        "selected_base_ref",
                        "old_base_head",
                        "new_base_head",
                        "branch_review_commit",
                        "resume_target",
                    )
                },
            }:
                raise WorkflowError(
                    "base_reconciliation_required does not match the current base pair.",
                    exit_code=2,
                )
            return
        expected_task_ref = (
            plan["task"]["archive_locator"]
            if exit_id == "ready_for_merge"
            and plan is not None
            and state in FINALIZATION_COMMITTED_RECOVERY_STATES
            else public_input.get("task_ref")
        )
        for field, expected in (
            ("task_ref", expected_task_ref),
            ("plan_ref", context.get("plan_ref")),
            (
                "branch_review_commit",
                finalization_route_branch_review_commit(context, exit_id),
            ),
            (
                "publication_head",
                (
                    plan["git"].get("publication_head")
                    or plan["git"].get("branch_review_commit")
                )
                if plan is not None
                else None,
            ),
        ):
            if field in output and output.get(field) != expected:
                raise WorkflowError(
                    f"Task finalization route output {field} does not match current facts.",
                    exit_code=2,
                )
    publication_status = context.get("publication_status", "current")
    if context.get("transaction_state") == "base_reconciliation_required" and exit_id != "blocked":
        raise WorkflowError("Current base evolution requires reconciliation or a blocked route.", exit_code=2)
    if exit_id == "publication_review_stale":
        if (
            publication_status != "stale"
            or state != "publication_review_stale"
            or output.get("task_ref") != public_input.get("task_ref")
            or output.get("branch_review_commit")
            != context.get("publication_branch_review_commit")
            or output.get("stale_reason")
            != context.get("publication_stale_reason")
        ):
            raise WorkflowError(
                "publication_review_stale is not compatible with current owner facts.",
                exit_code=2,
            )
        return
    if publication_status == "stale" and exit_id != "blocked":
        raise WorkflowError(
            "Current stale publication facts require an AI-authored stale or blocked route.",
            exit_code=2,
        )
    if plan is None:
        return
    if exit_id == "resume_finalization":
        if state not in FINALIZATION_RESUME_RECOVERY_STATES:
            raise WorkflowError(
                "resume_finalization is not compatible with a legal same-plan recovery state.",
                exit_code=2,
            )
    if exit_id == "reprepare_required" and state != "reprepare_required":
        raise WorkflowError(
            "reprepare_required is not compatible with the current transaction state.",
            exit_code=2,
        )
    if exit_id == "reprepare_required" and context.get("reprepare_reason_code") not in {
        FINALIZATION_REPREPARE_ARCHIVE_MONTH,
        FINALIZATION_REPREPARE_PROVENANCE_TAIL,
    }:
        raise WorkflowError(
            "reprepare_required reason does not match the current recovery state.",
            exit_code=2,
        )
    if (
        exit_id == "reprepare_required"
        and not executor_materialized
        and output.get("reason_code") != context.get("reprepare_reason_code")
    ):
        raise WorkflowError(
            "reprepare_required reason does not match the current recovery state.",
            exit_code=2,
        )
    if exit_id == "ready_for_merge" and state not in FINALIZATION_COMMITTED_RECOVERY_STATES:
        if not allow_pending_transition or not executor_materialized:
            raise WorkflowError(
                "ready_for_merge requires the exact private marker before its executor transition.",
                exit_code=2,
            )
    if (
        exit_id == "ready_for_merge"
        and state in FINALIZATION_COMMITTED_RECOVERY_STATES
        and context.get("published_transition_complete") is not True
        and not allow_pending_transition
    ):
        raise WorkflowError(
            "ready_for_merge requires the exact archive transaction and ready pull request.",
            exit_code=2,
        )

def finalization_gate_schema(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    schema = skill_read_schema(
        finalization_package_root(root) / "schemas/task-finalization-gate-5.0.schema.json",
        "task finalization gate schema",
        errors,
    )
    if errors or not isinstance(schema, dict):
        raise WorkflowError("Task finalization gate schema is unavailable.", exit_code=2)
    return schema

def finalization_normalize_gate(root: Path, payload: Any) -> dict[str, Any]:
    del root
    if not isinstance(payload, dict):
        raise WorkflowError("Task finalization gate must be an object.", exit_code=2)
    return payload

def finalization_base_evolution_supersession_pending(
    context: dict[str, Any],
) -> bool:
    prepared = context.get("prepared")
    reprepare = (
        prepared.get("pre_pr_reprepare")
        if isinstance(prepared, dict)
        else None
    )
    return (
        context.get("transaction_state") == "reprepare_required"
        and context.get("reprepare_reason_code")
        == FINALIZATION_REPREPARE_PROVENANCE_TAIL
        and isinstance(reprepare, dict)
        and isinstance(reprepare.get("base_evolution"), dict)
        and reprepare["base_evolution"].get("supersession_kind")
        == "legacy_pre_191"
        and isinstance(reprepare.get("previous_plan"), dict)
    )

def cmd_record_finalization_gate(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    public_input, _ = finalization_public_input(root, args.input)
    reviewed = finalization_semantic_review_input(root, args.review_input)
    context = finalization_preview_context(root, args, public_input)
    return finalization_record_gate_result(
        root,
        public_input,
        reviewed,
        context,
        dry_run=bool(getattr(args, "dry_run", False)),
        include_private=False,
    )


def finalization_record_gate_result(
    root: Path,
    public_input: dict[str, Any],
    reviewed: dict[str, Any],
    context: dict[str, Any],
    *,
    dry_run: bool,
    include_private: bool,
) -> dict[str, Any]:
    finalization_validate_route(
        root,
        public_input,
        context,
        reviewed["route"],
        allow_pending_transition=True,
    )
    plan = context["plan"]
    gate = {
        "schema_version": FINALIZATION_GATE_SCHEMA_VERSION,
        "skill_id": FINALIZE_TASK_SKILL_ID,
        "identity": {
            "task_ref": public_input["task_ref"],
            "plan_ref": context["plan_ref"] if plan is not None else None,
            "plan_digest": plan["plan_digest"] if plan is not None else None,
            "branch_review_commit": finalization_route_branch_review_commit(
                context,
                str(reviewed["route"]["typed_exit"]),
            ),
        },
        "review": copy.deepcopy(reviewed["review"]),
        "route": copy.deepcopy(reviewed["route"]),
    }
    errors = skill_json_schema_validation_errors(
        gate,
        finalization_gate_schema(root),
        "task finalization gate",
    )
    if errors:
        raise WorkflowError(
            "Task finalization recorder produced an invalid gate.",
            exit_code=2,
            payload={"errors": errors},
        )
    task_dir = context["task_dir"]
    artifact_path = (
        task_finalization_transition_path(root, task_dir)
        if finalization_base_evolution_supersession_pending(context)
        else task_finalization_path(root, task_dir)
    )
    committed_recovery = (
        context["transaction_state"] in FINALIZATION_COMMITTED_RECOVERY_STATES
    )
    if not dry_run and not committed_recovery:
        write_json(artifact_path, gate)
    result = {
        "status": "ok",
        "artifact_path": str(artifact_path),
        "typed_exit": gate["route"]["typed_exit"],
        "plan_ref": context["plan_ref"],
        "plan_digest": plan["plan_digest"] if plan is not None else None,
        "dry_run": dry_run,
    }
    if include_private:
        result["gate"] = gate
        result["gate_path"] = artifact_path
    return result

def finalization_gate_input(
    root: Path,
    public_input: dict[str, Any],
    value: str | None,
) -> tuple[dict[str, Any], Path]:
    task_dir = finalization_task_dir(root, public_input)
    expected = task_finalization_path(root, task_dir)
    if task_dir_is_archived(root, task_dir):
        transaction_match = finalization_find_transaction_by_task_ref(
            root,
            str(public_input.get("task_ref") or ""),
        )
        # A completed terminal recovery retires the owner gate and transaction.
        # Keep the caller's exact locator binding, but allow the archived
        # committed-terminal projection to rebuild the checked marker when the
        # normal owner artifact was intentionally retired.
        owner_result_missing_after_terminal_cleanup = False
        if value:
            relative = skill_safe_relative(str(value).strip())
            supplied = root / relative if relative is not None else None
            if supplied is None or supplied.resolve() != expected.resolve():
                raise WorkflowError(
                    "Task finalization gate must use the exact owner-private artifact.",
                    exit_code=2,
                )
            if expected.exists() or expected.is_symlink():
                supplied = stage0_owner_path(root, value, "arguments.owner_result")
            else:
                owner_result_missing_after_terminal_cleanup = True
        if transaction_match is not None:
            if not expected.is_file() or expected.is_symlink():
                raise WorkflowError(
                    "Archived current Finalizer is missing its owner-private gate.",
                    exit_code=2,
                )
            return finalization_normalize_gate(root, read_json(expected)), expected
        terminal_gate = finalization_current_terminal_gate(
            root,
            task_dir,
            str(public_input.get("task_ref") or ""),
        )
        if terminal_gate is not None:
            if value and not owner_result_missing_after_terminal_cleanup:
                supplied = stage0_owner_path(root, value, "arguments.owner_result")
                if supplied.resolve() != expected.resolve():
                    raise WorkflowError(
                        "Task finalization gate must use the exact owner-private artifact.",
                        exit_code=2,
                    )
            return terminal_gate, expected
        terminal_projection_gate = finalization_terminal_projection_gate(
            root,
            task_dir,
            public_input,
        )
        if terminal_projection_gate is not None:
            if not value or not owner_result_missing_after_terminal_cleanup:
                raise WorkflowError(
                    "Retired terminal projection requires its exact owner-private locator.",
                    exit_code=2,
                )
            return terminal_projection_gate, expected
        plan = finalization_closeout_plan(root, task_dir)
        if plan is None:
            raise WorkflowError(
                "Archived task finalization is missing its immutable plan.",
                exit_code=2,
            )
        transaction = resolve_committed_closeout_archive_transaction(root, plan)
        if transaction is None:
            raise WorkflowError(
                "Archived task finalization is not the exact plan transaction.",
                exit_code=2,
            )
        if expected.is_file() and not expected.is_symlink():
            return finalization_normalize_gate(root, read_json(expected)), expected
        return {
            "schema_version": FINALIZATION_GATE_SCHEMA_VERSION,
            "skill_id": FINALIZE_TASK_SKILL_ID,
            "identity": {
                "task_ref": plan["task"]["active_locator"],
                "plan_ref": f"closeout-plan:{plan['plan_digest']}",
                "plan_digest": plan["plan_digest"],
                "branch_review_commit": plan["git"]["branch_review_commit"],
            },
            "review": {
                "status": "passed",
                "summary": "The committed archive transaction is the unchanged reviewed closeout plan.",
            },
            "route": {
                "typed_exit": "ready_for_merge",
                "consumer": copy.deepcopy(FINALIZATION_CONSUMERS["ready_for_merge"]),
                "output": copy.deepcopy(FINALIZATION_EXECUTOR_OUTPUT_MARKER),
            },
        }, expected
    transition = task_finalization_transition_path(root, task_dir)
    path = (
        stage0_owner_path(root, value, "arguments.owner_result")
        if value
        else (
            transition
            if transition.is_file() and not transition.is_symlink()
            else expected
        )
    )
    if path.resolve() not in {expected.resolve(), transition.resolve()}:
        raise WorkflowError(
            "Task finalization gate must use the exact owner-private artifact.",
            exit_code=2,
        )
    if path.resolve() == transition.resolve() and (
        not expected.is_file() or expected.is_symlink()
    ):
        raise WorkflowError(
            "Task finalization transition gate requires its legacy predecessor checkpoint.",
            exit_code=2,
        )
    return finalization_normalize_gate(root, read_json(path)), path

def check_finalization_gate_result(
    root: Path,
    args: argparse.Namespace,
    public_input: dict[str, Any],
    gate: dict[str, Any],
    gate_path: Path,
    *,
    allow_pending_transition: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    preview_args = copy.copy(args)
    preview_args._finalization_checked_gate = gate
    context = finalization_preview_context(root, preview_args, public_input)
    return check_finalization_gate_context(
        root,
        public_input,
        gate,
        gate_path,
        context,
        allow_pending_transition=allow_pending_transition,
    )


def check_finalization_gate_context(
    root: Path,
    public_input: dict[str, Any],
    gate: dict[str, Any],
    gate_path: Path,
    context: dict[str, Any],
    *,
    allow_pending_transition: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    errors = skill_json_schema_validation_errors(
        gate,
        finalization_gate_schema(root),
        "task finalization gate",
    )
    transition_gate = task_finalization_transition_path(root, context["task_dir"])
    if (
        gate_path.resolve() == transition_gate.resolve()
        and not finalization_base_evolution_supersession_pending(context)
    ):
        errors.append(
            "task finalization transition gate is outside base-evolution supersession"
        )
    committed_recovery = (
        context["transaction_state"] in FINALIZATION_COMMITTED_RECOVERY_STATES
    )
    plan = context["plan"]
    expected_identity = {
        "task_ref": (
            plan["task"]["active_locator"]
            if committed_recovery and plan is not None
            else public_input["task_ref"]
        ),
        "plan_ref": context["plan_ref"] if plan is not None else None,
        "plan_digest": plan["plan_digest"] if plan is not None else None,
        "branch_review_commit": finalization_route_branch_review_commit(
            context,
            str((gate.get("route") or {}).get("typed_exit") or ""),
        ),
    }
    if gate.get("identity") != expected_identity:
        errors.append("task finalization gate objective identity mismatch")
    try:
        finalization_validate_route(
            root,
            public_input,
            context,
            gate.get("route") or {},
            allow_pending_transition=allow_pending_transition,
        )
    except WorkflowError as exc:
        errors.append(str(exc))
    if errors:
        raise WorkflowError(
            "Task finalization gate failed objective checks.",
            exit_code=2,
            payload={"artifact_path": str(gate_path), "errors": errors},
        )
    return gate, context

def cmd_check_finalization_gate(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    public_input, _ = finalization_public_input(root, args.input)
    gate, gate_path = finalization_gate_input(root, public_input, args.gate)
    checked, context = check_finalization_gate_result(
        root,
        args,
        public_input,
        gate,
        gate_path,
        allow_pending_transition=True,
    )
    return {
        "status": "ok",
        "artifact_path": str(gate_path),
        "typed_exit": checked["route"]["typed_exit"],
        "task_ref": public_input["task_ref"],
        "plan_ref": context["plan_ref"],
        "plan_digest": (
            context["plan"]["plan_digest"]
            if context["plan"] is not None
            else None
        ),
        "transaction_state": context["transaction_state"],
    }

def finalization_live_open_close_issues(
    root: Path,
    repo: str,
    issue_numbers: list[int],
) -> list[dict[str, Any]]:
    normalized_repo = normalize_github_repository(repo)
    if normalized_repo != repo:
        raise WorkflowError(
            "Task finalization requires a canonical repository identity.",
            exit_code=2,
        )
    issues: list[dict[str, Any]] = []
    for issue_number in issue_numbers:
        issue = gh_json(
            [
                "issue",
                "view",
                str(issue_number),
                "--repo",
                repo,
                "--json",
                "number,state,url",
            ],
            cwd=root,
            repo=repo,
            required_fields=("number", "state", "url"),
            operation="finalization_issue_preflight",
        )
        expected_url = f"https://github.com/{repo}/issues/{issue_number}"
        if (
            not isinstance(issue, dict)
            or issue.get("number") != issue_number
            or issue.get("url") != expected_url
        ):
            raise github_response_incomplete(
                operation="finalization_issue_preflight",
                repo=repo,
                detail=f"Issue #{issue_number} identity does not match.",
            )
        state = str(issue.get("state") or "").upper()
        if state != "OPEN":
            raise WorkflowError(
                f"Task finalization close issue #{issue_number} is not Open before merge.",
                exit_code=2,
            )
        issues.append(
            {
                "number": issue_number,
                "state": state,
                "url": expected_url,
            }
        )
    return issues

def finalization_gate_with_ready_for_merge_output(
    root: Path,
    task_dir: Path,
    gate: dict[str, Any],
    plan: dict[str, Any],
    pr: dict[str, Any],
) -> dict[str, Any]:
    if (
        gate.get("route", {}).get("typed_exit") != "ready_for_merge"
        or gate.get("route", {}).get("output")
        != FINALIZATION_EXECUTOR_OUTPUT_MARKER
    ):
        raise WorkflowError(
            "Task finalization gate did not retain the exact private ready_for_merge marker.",
            exit_code=2,
        )
    if repo_relative(root, task_dir) != plan["task"]["archive_locator"]:
        raise WorkflowError(
            "Task finalization ready_for_merge output requires the exact archived task locator.",
            exit_code=2,
        )
    finalization_live_open_close_issues(
        root,
        plan["git"]["repo"],
        plan["review"]["close_issues_reviewed"],
    )
    updated = copy.deepcopy(gate)
    updated["route"]["output"] = {
        "exit_id": "ready_for_merge",
        "repo_ref": plan["git"]["repo"],
        "pr_number": pr["number"],
        "pr_url": canonical_pull_request_url(
            plan["git"]["repo"],
            pr["number"],
            pr["url"],
        ),
        "expected_head_sha": pr["headRefOid"],
        "expected_base_branch": plan["git"]["base_branch"],
        "expected_head_branch": plan["git"]["head_branch"],
        "expected_close_issues": plan["review"]["close_issues_reviewed"],
    }
    errors = skill_json_schema_validation_errors(
        updated["route"]["output"],
        finalization_output_contract(root, "ready_for_merge"),
        "task finalization ready_for_merge output",
    )
    if errors:
        raise WorkflowError(
            "Task finalization ready_for_merge output is invalid.",
            exit_code=2,
            payload={"errors": errors},
        )
    return updated

def execute_finalization_transition_result(
    root: Path,
    args: argparse.Namespace,
    public_input: dict[str, Any],
    gate: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    exit_id = gate["route"]["typed_exit"]
    task_dir = context["task_dir"]
    if exit_id == "reprepare_required":
        reason_code = context["reprepare_reason_code"]
        reviewed_content_head = context["plan"]["git"]["reviewed_content_head"]
        reprepare: dict[str, Any] | None = None
        reprepare_facts: dict[str, Any] | None = None
        if reason_code == FINALIZATION_REPREPARE_PROVENANCE_TAIL:
            reprepare = (
                context.get("prepared", {}).get("pre_pr_reprepare")
                if isinstance(context.get("prepared"), dict)
                else None
            )
            previous_plan = (
                reprepare.get("previous_plan")
                if isinstance(reprepare, dict)
                and isinstance(reprepare.get("previous_plan"), dict)
                else None
            )
            previous_transaction = (
                reprepare.get("previous_transaction")
                if isinstance(reprepare, dict)
                and isinstance(reprepare.get("previous_transaction"), dict)
                else None
            )
            reprepare_facts = finalizer_pre_pr_provenance_reprepare_preflight(
                root,
                task_dir,
                context["plan"],
                previous_plan=previous_plan,
                previous_transaction=previous_transaction,
                allowed_current_gate=gate,
            )
            target_repo = context["plan"]["git"]["repo"]
            publication = finalizer_publication_identity(
                root,
                reviewed_content_head,
                target_repo,
            )
            provenance = (
                publication
                if publication["metadata_tail"] is not None
                else prepare_provenance_metadata_tail(
                    root,
                    reviewed_content_head,
                    target_repo,
                )
            )
        elif reason_code == FINALIZATION_REPREPARE_ARCHIVE_MONTH:
            publication = finalizer_publication_identity(
                root,
                reviewed_content_head,
                context["plan"]["git"]["repo"],
            )
            provenance = publication
        else:
            raise WorkflowError(
                "Finalizer reprepare reason is unsupported.",
                exit_code=2,
            )
        previous_owner_transaction = finalization_read_transaction(root, task_dir)
        retired = finalizer_supersede_pre_pr_state(root, task_dir)
        replacement_transaction: dict[str, Any] | None = None
        base_evolution = (
            reprepare.get("base_evolution")
            if isinstance(reprepare, dict)
            else None
        )
        if reason_code in {
            FINALIZATION_REPREPARE_PROVENANCE_TAIL,
            FINALIZATION_REPREPARE_ARCHIVE_MONTH,
        }:
            task_context = context.get("task_context")
            if not isinstance(task_context, dict):
                raise WorkflowError(
                    "Provenance reprepare is missing current task runtime identity.",
                    exit_code=2,
                )
            replacement_args = copy.copy(args)
            replacement_args.repo = context["plan"]["git"]["repo"]
            replacement_args.remote = context["plan"]["git"]["remote"]
            replacement_args.base_branch = context["plan"]["git"]["base_branch"]
            replacement_args.title = context["plan"]["publish"]["title"]
            replacement_args.include_finalization_gate = True
            replacement = prepare_closeout(
                root,
                replacement_args,
                load_config(root),
                task_dir,
                task_context,
                publication_ready={
                    "profile": "publication_ready",
                    "mode": public_input.get("mode", "workflow"),
                    "task_ref": public_input["task_ref"],
                    "branch_review_commit": provenance["reviewed_content_head"],
                    "pr_title": context["plan"]["publish"]["title"],
                    "pr_body": context["plan"]["publish"]["body"],
                },
                current_finalizer=True,
            )
            if reprepare_facts is None:
                previous_recovery = (
                    previous_owner_transaction.get("adopted_pr")
                    if isinstance(previous_owner_transaction, dict)
                    and previous_owner_transaction.get("mode")
                    == "existing_pr_recovery"
                    else None
                )
                if isinstance(previous_recovery, dict):
                    pre_push_remote_head = str(
                        previous_recovery.get("pre_push_remote_head") or ""
                    )
                else:
                    _existing_pr, pre_push_remote_head = (
                        finalization_pre_mutation_remote_preflight(
                            root,
                            replacement["plan"],
                            None,
                        )
                    )
                replacement_transaction = finalization_reprepared_transaction(
                    replacement["plan"],
                    previous_owner_transaction,
                    pre_push_remote_head=pre_push_remote_head,
                )
            else:
                replacement_transaction = finalization_reprepared_transaction(
                    replacement["plan"],
                    previous_owner_transaction,
                    pre_push_remote_head=str(reprepare_facts["remote_head"]),
                )
            finalization_pre_mutation_remote_preflight(
                root,
                replacement["plan"],
                replacement_transaction,
            )
            finalization_write_transaction(
                root,
                task_dir,
                replacement_transaction,
            )
        output = finalization_reprepare_public_output(
            root,
            task_ref=public_input["task_ref"],
            reason_code=reason_code,
            branch_review_commit=provenance["reviewed_content_head"],
            publication_head=provenance["publication_head"],
        )
        return {
            "status": "ok",
            "stage": "reprepare_required",
            "typed_exit": exit_id,
            "retired_owner_state": retired,
            "reviewed_content_head": provenance["reviewed_content_head"],
            "publication_head": provenance["publication_head"],
            "replacement_transaction_created": replacement_transaction is not None,
            "output": output,
        }
    if exit_id == "ready_for_merge":
        if context["transaction_state"] == "ready":
            pr = context.get("published_pr")
            if not isinstance(pr, dict):
                raise WorkflowError(
                    "Task finalization Ready recovery is missing the bound pull request.",
                    exit_code=2,
                )
            materialized_gate = finalization_gate_with_ready_for_merge_output(
                root,
                task_dir,
                gate,
                context["plan"],
                pr,
            )
            retired_owner_state = finalization_retire_current_state(root, task_dir)
            return {
                "status": "ok",
                "stage": "ready_recovered",
                "typed_exit": exit_id,
                "output": materialized_gate["route"]["output"],
                "retired_owner_state": retired_owner_state,
            }
        if (
            context["transaction_state"] == "archived"
            and context.get("published_transition_complete") is not True
        ):
            transaction = finalization_read_transaction(root, task_dir)
            if not isinstance(transaction, dict):
                raise WorkflowError(
                    "Task finalization archived recovery is missing its transaction.",
                    exit_code=2,
                )
            bound_pr = transaction.get("pr")
            if not isinstance(bound_pr, dict):
                raise WorkflowError(
                    "Task finalization archived recovery is missing its bound pull request.",
                    exit_code=2,
                )
            publish_payload = ensure_closeout_pr_ready(
                root,
                context["plan"],
                bound_pr=bound_pr,
            )
            finalization_write_transaction(
                root,
                task_dir,
                finalization_advance_transaction(
                    context["plan"],
                    transaction,
                    next_transition="mark_ready",
                    pr=publish_payload["pr"],
                ),
            )
            materialized_gate = finalization_gate_with_ready_for_merge_output(
                root,
                task_dir,
                gate,
                context["plan"],
                publish_payload["pr"],
            )
            retired_owner_state = finalization_retire_current_state(root, task_dir)
            return {
                "status": "ok",
                "stage": "ready_recovered",
                "typed_exit": exit_id,
                "output": materialized_gate["route"]["output"],
                "retired_owner_state": retired_owner_state,
            }
        finish_args = copy.copy(args)
        finish_args.task = public_input["task_ref"]
        finish_args.from_guru_finalizer = True
        finish_args.expected_plan_digest = context["plan"]["plan_digest"]
        finish_args.dry_run = False
        finish_args.finalization_gate = gate
        finish_args.existing_pr_recovery = copy.deepcopy(
            context.get("existing_pr_recovery")
        )
        finish_args.publication_ready = finalization_prepare_publication_ready(
            public_input,
            transaction=finalization_read_transaction(root, task_dir),
        )
        result = cmd_finish_work(finish_args)
        materialized_gate = finalization_gate_with_ready_for_merge_output(
            root,
            Path(result["archived_task_dir"]),
            gate,
            context["plan"],
            result["publish"]["pr"],
        )
        return {
            **result,
            "typed_exit": exit_id,
            "output": materialized_gate["route"]["output"],
        }
    return {
        "status": "ok",
        "stage": "no_side_effect",
        "typed_exit": exit_id,
        "output": copy.deepcopy(gate["route"]["output"]),
    }


def cmd_execute_finalization_transition(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    public_input, _ = finalization_public_input(root, args.input)
    gate, gate_path = finalization_gate_input(root, public_input, args.gate)
    gate, context = check_finalization_gate_result(
        root,
        args,
        public_input,
        gate,
        gate_path,
        allow_pending_transition=True,
    )
    return execute_finalization_transition_result(
        root,
        args,
        public_input,
        gate,
        context,
    )

def context_sort(values: set[str] | list[str]) -> list[str]:
    return sorted(set(values), key=lambda item: item.encode("utf-8"))
