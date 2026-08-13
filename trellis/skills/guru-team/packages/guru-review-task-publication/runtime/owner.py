#!/usr/bin/env python3
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

AI_FIRST_OS_NOISE_NAMES = frozenset({".DS_Store"})

REVIEWED_CONTENT_ALGORITHM = "guru-reviewed-content-1.0"

REVIEWED_CONTENT_METADATA_PREFIXES = (
    ".trellis/tasks",
    ".trellis/workspace",
    ".trellis/.runtime",
)

PROVENANCE_TAIL_MANIFEST_PATH = ".trellis/guru-team/extension.json"

PROVENANCE_TAIL_ALLOWED_FIELDS = frozenset({
    "installed_at",
    "install.managed_asset_hashes",
    "install.managed_asset_hashes..trellis/spec/workflow/semantic-retrieval.md",
    "source.ref",
    "source.commit",
    "source.tree_state",
    "source.is_mutable_ref",
})

PROVENANCE_TAIL_OBJECT_PRESENCE = object()

AGENT_ASSIGNMENT_ARTIFACT = "agent-assignment.json"

REVIEW_REPORT_ARTIFACT = "review.md"

FINISH_SUMMARY_ARTIFACT = "finish-summary.json"

CLOSEOUT_PLAN_ARTIFACT = "closeout-plan.json"

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

def ai_first_os_noise_path(path: str) -> bool:
    return Path(path).name in AI_FIRST_OS_NOISE_NAMES

def reviewed_content_metadata_path(path: str) -> bool:
    return path == PROVENANCE_TAIL_MANIFEST_PATH or ai_first_os_noise_path(path) or any(
        path == prefix or path.startswith(prefix + "/")
        for prefix in REVIEWED_CONTENT_METADATA_PREFIXES
    )

def reviewed_content_tree_entries(
    root: Path,
    commit: str,
) -> dict[str, dict[str, str]]:
    if not isinstance(commit, str) or not commit.strip():
        raise WorkflowError(
            "Reviewed-content commit must be a non-empty Git revision.",
            exit_code=2,
        )
    proc = subprocess.run(
        ["git", "ls-tree", "-r", "-z", "--full-tree", commit.strip()],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Could not read the reviewed-content commit tree.",
            exit_code=2,
            payload={"stderr": proc.stderr.decode("utf-8", "replace")},
        )
    entries: dict[str, dict[str, str]] = {}
    for raw_record in proc.stdout.split(b"\0"):
        if not raw_record:
            continue
        metadata_raw, separator, path_raw = raw_record.partition(b"\t")
        if not separator:
            raise WorkflowError(
                "Git returned an invalid reviewed-content tree record.",
                exit_code=2,
            )
        try:
            path = path_raw.decode("utf-8", "strict")
            metadata = metadata_raw.decode("ascii", "strict").split()
        except UnicodeDecodeError as exc:
            raise WorkflowError(
                "Reviewed-content tree paths must be valid UTF-8.",
                exit_code=2,
            ) from exc
        if len(metadata) != 3:
            raise WorkflowError(
                "Git returned incomplete reviewed-content tree metadata.",
                exit_code=2,
            )
        mode, object_type, oid = metadata
        path_parts = path.split("/")
        valid_type = (
            (mode == "160000" and object_type == "commit")
            or (mode in {"100644", "100755", "120000"} and object_type == "blob")
        )
        if (
            not valid_type
            or re.fullmatch(r"[0-9a-f]{40,64}", oid) is None
            or not path
            or path.startswith("/")
            or any(part in {"", ".", ".."} for part in path_parts)
            or path in entries
        ):
            raise WorkflowError(
                "Reviewed-content tree contains an unsupported or ambiguous entry.",
                exit_code=2,
                payload={"path": path},
            )
        if reviewed_content_metadata_path(path):
            continue
        entries[path] = {"path": path, "mode": mode, "oid": oid}
    return entries

def reviewed_content_blob_oid(root: Path, content: bytes) -> str:
    proc = subprocess.run(
        ["git", "hash-object", "--stdin"],
        cwd=str(root),
        input=content,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    oid = proc.stdout.decode("ascii", "strict").strip() if proc.returncode == 0 else ""
    if proc.returncode != 0 or re.fullmatch(r"[0-9a-f]{40,64}", oid) is None:
        raise WorkflowError(
            "Could not calculate a reviewed-content blob identity.",
            exit_code=2,
            payload={"stderr": proc.stderr.decode("utf-8", "replace")},
        )
    return oid

def reviewed_content_worktree_overlays(root: Path) -> list[dict[str, Any]]:
    overlays: list[dict[str, Any]] = []
    for record in task_commit_porcelain_status_records(root):
        path = str(record.get("path") or "")
        renamed_from = record.get("renamed_from")
        if isinstance(renamed_from, str) and not reviewed_content_metadata_path(
            renamed_from
        ):
            overlays.append({"path": renamed_from, "deleted": True})
        if reviewed_content_metadata_path(path):
            continue
        entry = task_commit_snapshot_entry(root, record)
        if entry.get("deleted") is True:
            overlays.append({"path": path, "deleted": True})
            continue
        mode = str(entry.get("mode") or "")
        if mode == "160000":
            oid = str(entry.get("gitlink_head") or "")
            index_oid = str(entry.get("index_blob") or "")
            if (
                entry.get("gitlink_initialized") is not True
                or entry.get("gitlink_dirty") is not False
                or re.fullmatch(r"[0-9a-f]{40,64}", oid) is None
                or re.fullmatch(r"[0-9a-f]{40,64}", index_oid) is None
            ):
                raise WorkflowError(
                    "Reviewed-content gitlink identity is unavailable or dirty.",
                    exit_code=2,
                    payload={"path": path},
                )
            if entry.get("index_status") and index_oid != oid:
                raise WorkflowError(
                    "Reviewed-content gitlink index pointer does not match its worktree binding.",
                    exit_code=2,
                    payload={"path": path},
                )
        else:
            content, _sha256, worktree_mode = task_commit_worktree_content(root, path)
            if content is None or worktree_mode not in {"100644", "100755", "120000"}:
                raise WorkflowError(
                    "Reviewed-content worktree entry is unavailable or unsupported.",
                    exit_code=2,
                    payload={"path": path},
                )
            mode = worktree_mode
            oid = reviewed_content_blob_oid(root, content)
        overlay = {
            "path": path,
            "deleted": False,
            "mode": mode,
            "oid": oid,
        }
        if mode == "160000":
            overlay["index_oid"] = index_oid
        overlays.append(overlay)
    return sorted(
        overlays,
        key=lambda item: (
            str(item["path"]).encode("utf-8"),
            0 if item.get("deleted") is True else 1,
        ),
    )

def reviewed_content_gitlink_identity(
    root: Path,
    path: str,
    recorded_oid: str | None,
    overlay: dict[str, Any] | None,
) -> str:
    expected_oid = (
        str(overlay.get("oid") or "") if overlay else str(recorded_oid or "")
    )
    expected_index_oid = (
        str(overlay.get("index_oid") or "") if overlay else str(recorded_oid or "")
    )
    if (
        re.fullmatch(r"[0-9a-f]{40,64}", expected_oid) is None
        or re.fullmatch(r"[0-9a-f]{40,64}", expected_index_oid) is None
    ):
        raise WorkflowError(
            "Reviewed-content gitlink binding is unavailable or ambiguous.",
            exit_code=2,
            payload={"path": path},
        )

    target = root / path
    try:
        metadata = target.lstat()
    except FileNotFoundError:
        metadata = None
    deinitialized = metadata is None
    if metadata is not None and stat.S_ISDIR(metadata.st_mode):
        try:
            with os.scandir(target) as children:
                deinitialized = next(children, None) is None
        except OSError as exc:
            raise WorkflowError(
                "Reviewed-content gitlink worktree root is ambiguous.",
                exit_code=2,
                payload={"path": path},
            ) from exc

    current_index_oid, current_index_mode = task_commit_index_identity(root, path)
    if current_index_oid != expected_index_oid or current_index_mode != "160000":
        raise WorkflowError(
            "Reviewed-content gitlink index binding drifted after capture.",
            exit_code=2,
            payload={"path": path},
        )
    if deinitialized:
        if overlay is not None:
            raise WorkflowError(
                "Reviewed-content gitlink overlay requires an initialized worktree.",
                exit_code=2,
                payload={"path": path},
            )
        return expected_oid

    identity = task_commit_gitlink_worktree_identity(root, path)
    if identity.get("gitlink_head") != expected_oid:
        raise WorkflowError(
            "Reviewed-content gitlink worktree HEAD drifted after capture.",
            exit_code=2,
            payload={"path": path},
        )
    return expected_oid

def reviewed_content_identity(
    root: Path,
    commit: str = "HEAD",
    include_worktree: bool = True,
) -> dict[str, str]:
    if include_worktree:
        resolved_commit = run_stdout(["git", "rev-parse", commit], cwd=root)
        if resolved_commit != current_head(root):
            raise WorkflowError(
                "Reviewed-content worktree overlays require the current HEAD commit.",
                exit_code=2,
            )
    entries = reviewed_content_tree_entries(root, commit)
    recorded_gitlink_oids = {
        path: entry["oid"]
        for path, entry in entries.items()
        if entry["mode"] == "160000"
    }
    if include_worktree:
        gitlink_overlays: dict[str, dict[str, Any]] = {}
        for overlay in reviewed_content_worktree_overlays(root):
            path = str(overlay["path"])
            existing = entries.get(path)
            if overlay.get("deleted") is True:
                if existing is not None and existing["mode"] == "160000":
                    raise WorkflowError(
                        "Reviewed-content gitlink deletion or replacement is unsupported.",
                        exit_code=2,
                        payload={"path": path},
                    )
                entries.pop(path, None)
            else:
                if (
                    existing is not None
                    and existing["mode"] == "160000"
                    and str(overlay["mode"]) != "160000"
                ):
                    raise WorkflowError(
                        "Reviewed-content gitlink deletion or replacement is unsupported.",
                        exit_code=2,
                        payload={"path": path},
                    )
                entries[path] = {
                    "path": path,
                    "mode": str(overlay["mode"]),
                    "oid": str(overlay["oid"]),
                }
                if overlay["mode"] == "160000":
                    gitlink_overlays[path] = overlay
        for path, entry in entries.items():
            if entry["mode"] != "160000":
                continue
            entry["oid"] = reviewed_content_gitlink_identity(
                root,
                path,
                recorded_gitlink_oids.get(path),
                gitlink_overlays.get(path),
            )
    canonical_entries = sorted(
        entries.values(),
        key=lambda item: item["path"].encode("utf-8"),
    )
    sha256 = canonical_json_sha256(
        {
            "algorithm": REVIEWED_CONTENT_ALGORITHM,
            "entries": canonical_entries,
        }
    )
    return {"algorithm": REVIEWED_CONTENT_ALGORITHM, "sha256": sha256}

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

def current_task_dir(root: Path) -> Path | None:
    task_script = root / ".trellis/scripts/task.py"
    if not task_script.exists():
        return None
    proc = run(["python3", "./.trellis/scripts/task.py", "current"], cwd=root, check=False)
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
            if artifact.exists():
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

def is_strict_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)

def task_dir_is_archived(root: Path, task_dir: Path) -> bool:
    try:
        task_dir.resolve().relative_to((tasks_root(root) / "archive").resolve())
        return True
    except ValueError:
        return False

def contract_wording_read_input(root: Path, value: str | None, label: str) -> dict[str, Any]:
    if isinstance(value, dict):
        return copy.deepcopy(value)
    if not value:
        raise WorkflowError(f"{label} requires an input JSON file.", exit_code=2)
    if value == "-":
        raw = sys.stdin.read()
    else:
        path = Path(value)
        if not path.is_absolute():
            path = root / path
        try:
            raw = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise WorkflowError(f"{label} input is unreadable.", exit_code=2) from exc
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"{label} input is invalid JSON.", exit_code=2) from exc
    if not isinstance(payload, dict):
        raise WorkflowError(f"{label} input root must be an object.", exit_code=2)
    return payload

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

def canonical_json_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

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

TASK_PUBLICATION_DIMENSIONS = (
    "diff_outcome_consistency",
    "issue_scope_closure",
    "pr_body_quality",
    "validation_claims",
    "branch_review_summary",
    "docs_ssot_reconciliation",
    "safety_deployment_impact",
    "finish_summary_semantics",
    "metadata_tail_integrity",
    "artifact_binding_freshness",
)

TASK_PUBLICATION_CONSUMERS = {
    "ready": {"kind": "skill", "id": "guru-finalize-task"},
    "return_to_task_work": {
        "kind": "workflow",
        "id": "guru-task-publication-work-router",
    },
    "blocked": {"kind": "stop", "id": "task-publication-review-blocked"},
}

def task_publication_schema(root: Path) -> dict[str, Any]:
    candidates = (
        root
        / "trellis/skills/guru-team/packages/guru-review-task-publication/schemas/pr-readiness.schema.json",
        root
        / ".trellis/guru-team/skills/packages/guru-review-task-publication/schemas/pr-readiness.schema.json",
    )
    for path in candidates:
        if path.is_file() and not path.is_symlink():
            errors: list[str] = []
            schema = skill_read_schema(path, "task publication readiness schema", errors)
            if isinstance(schema, dict) and not errors:
                return schema
    raise WorkflowError(
        "guru-review-task-publication readiness schema is unavailable.",
        exit_code=2,
    )

def task_publication_path(
    root: Path,
    task_dir: Path,
) -> Path:
    return ai_first_owner_checkpoint_path(root, task_dir, PR_READINESS_ARTIFACT)

def task_publication_issue_scope_ledger_binding(
    ledger: dict[str, Any],
    content: bytes,
) -> dict[str, str]:
    return task_publication_binding({
        "artifact_sha256": hashlib.sha256(content).hexdigest(),
        "primary_issue": ledger.get("primary_issue"),
        "close_issues": ledger.get("close_issues"),
        "related_issues": ledger.get("related_issues"),
        "followup_issues": ledger.get("followup_issues"),
    })

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

def task_publication_binding(
    value: Any,
    *,
    status: str = "passed",
) -> dict[str, str]:
    return {
        "status": status,
        "facts_sha256": context_digest(value),
    }

def task_publication_entry_precondition_bindings(
    root: Path,
    task_dir: Path,
    config: dict[str, Any],
    invocation: dict[str, Any],
) -> tuple[dict[str, dict[str, str]], list[str], dict[str, Any], dict[str, Any]]:
    """Rebuild the objective publication-entry preconditions.

    The function records only deterministic facts after the semantic owner has
    authored its review. It never selects a finding route, dimension status, or
    typed exit.
    """
    bindings: dict[str, dict[str, str]] = {}
    errors: list[str] = []

    step_errors: list[str] = []
    try:
        readiness_schema = task_publication_schema(root)
        package_candidates = (
            root / "trellis/skills/guru-team/packages/guru-review-task-publication",
            root / ".trellis/guru-team/skills/packages/guru-review-task-publication",
        )
        package = next(
            (
                candidate
                for candidate in package_candidates
                if (candidate / "interface.json").is_file()
                and (candidate / "schemas/public-input.schema.json").is_file()
            ),
            None,
        )
        if package is None:
            raise WorkflowError(
                "guru-review-task-publication package is unavailable.",
                exit_code=2,
            )
        runtime_facts = {
            "schema": readiness_schema,
            "interface_sha256": hashlib.sha256(
                (package / "interface.json").read_bytes()
            ).hexdigest(),
            "public_input_schema_sha256": hashlib.sha256(
                (package / "schemas/public-input.schema.json").read_bytes()
            ).hexdigest(),
        }
    except (OSError, WorkflowError) as exc:
        step_errors.append(f"runtime_dependency:{exc}")
    if step_errors:
        errors.extend(step_errors)
    else:
        bindings["runtime_dependency"] = task_publication_binding(runtime_facts)

    task_context: dict[str, Any] = {}
    task: dict[str, Any] = {}
    step_errors = []
    try:
        task_context = load_task_runtime_identity(task_dir, config)
        assert_workspace_boundary(root, config, task_context, task_dir)
        task = task_json(task_dir)
    except WorkflowError as exc:
        step_errors.append(f"task_workspace:{exc}")
    if step_errors:
        errors.extend(step_errors)
    else:
        bindings["task_workspace"] = task_publication_binding({
            "task_artifact_dir": task_context.get("task_artifact_dir"),
            "task_workspace_id": task_context.get("task_workspace_id"),
            "workspace_mode": config.get("workspace_mode"),
            "repo_root": str(root.resolve()),
        })

    step_errors = []
    expected_task = repo_relative(root, task_dir)
    expected_branch = str(
        task_context.get("branch_name") or task.get("branch") or ""
    )
    expected_base = str(
        task_context.get("base_branch") or task.get("base_branch") or ""
    )
    if (
        not task
        or task.get("status") != "in_progress"
        or not expected_branch
        or current_branch(root) != expected_branch
        or not expected_base
        or invocation.get("task_ref", expected_task) != expected_task
    ):
        step_errors.append("task_identity:current task, branch, base, or status mismatch")
    if step_errors:
        errors.extend(step_errors)
    else:
        bindings["task_identity"] = task_publication_binding({
            "task_ref": expected_task,
            "task_id": task.get("id"),
            "status": task.get("status"),
            "branch": expected_branch,
            "base_branch": expected_base,
        })

    branch_review_commit = str(invocation.get("branch_review_commit") or "")
    review_handoff: dict[str, Any] = {
        "typed_exit": "passed",
        "branch_review_commit": branch_review_commit,
    }
    review_errors: list[str] = []
    if not re.fullmatch(r"[0-9a-f]{40}", branch_review_commit):
        review_errors.append("Branch Review DTO branch_review_commit is invalid.")
    else:
        try:
            reviewed_content_sha256 = reviewed_content_identity(
                root,
                branch_review_commit,
                include_worktree=False,
            )["sha256"]
            review_errors.extend(
                review_branch_content_continuity_errors(
                    root,
                    task_dir,
                    branch_review_commit,
                    reviewed_content_sha256,
                    current_head(root),
                )
            )
        except WorkflowError as exc:
            review_errors.append(
                f"Branch Review DTO content continuity is unavailable: {exc}"
            )
    if review_errors:
        errors.extend(
            f"branch_review_handoff:{item}" for item in sorted(set(review_errors))
        )
    else:
        bindings["branch_review_handoff"] = task_publication_binding(
            review_handoff
        )

    try:
        repository = task_publication_repository_binding(root, task_dir)
    except WorkflowError as exc:
        repository = {}
        errors.append(f"review_range_and_working_tree:{exc}")

    ledger: dict[str, Any] = {}
    ledger_errors: list[str] = []
    ledger_path = issue_scope_ledger_path(task_dir)
    try:
        ledger = load_issue_scope_ledger(task_dir, task_context)
    except WorkflowError as exc:
        ledger_errors.append(str(exc))
    if (
        not isinstance(ledger.get("primary_issue"), dict)
        or not isinstance(ledger.get("close_issues"), list)
        or not isinstance(ledger.get("related_issues"), list)
        or not isinstance(ledger.get("followup_issues"), list)
    ):
        ledger_errors.append("issue scope ledger identity is incomplete")
    if not ledger_errors:
        ledger_errors.extend(
            validate_ledger_for_publish(
                ledger,
            )
        )
    if ledger_errors:
        errors.extend(
            f"issue_scope_ledger:{item}" for item in sorted(set(ledger_errors))
        )
    else:
        bindings["issue_scope_ledger"] = (
            task_publication_issue_scope_ledger_binding(
                ledger,
                ledger_path.read_bytes(),
            )
        )

    publication_content_errors: list[str] = []
    pr_payload = invocation.get("pr_payload")
    if not isinstance(pr_payload, dict) or set(pr_payload) != {"title", "body"}:
        publication_content_errors.append("PR payload must contain exactly title and body")
        pr_payload = {}
    title = pr_payload.get("title")
    body = pr_payload.get("body")
    if not isinstance(title, str) or not title.strip():
        publication_content_errors.append("PR title is empty")
    if not isinstance(body, str) or not body.strip():
        publication_content_errors.append("PR body is empty")
    elif ledger:
        publication_content_errors.extend(validate_pr_body_quality(body, ledger, False))
    if publication_content_errors:
        errors.extend(
            f"publication_content:{item}"
            for item in sorted(set(publication_content_errors))
        )
    else:
        bindings["publication_content"] = task_publication_binding({
            "pr_title": title,
            "pr_body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        })

    if repository:
        unexpected_status_paths = task_publication_unexpected_status_paths(
            repository["status_paths"],
        )
        if unexpected_status_paths:
            errors.append(
                "review_range_and_working_tree:working tree has paths outside "
                "the reviewed-content boundary: "
                + ", ".join(unexpected_status_paths[:20])
                + "."
            )
        else:
            bindings["review_range_and_working_tree"] = task_publication_binding(
                repository
            )

    bindings["invocation_freshness"] = task_publication_binding({
        "task_ref": expected_task,
        "branch_review_commit": branch_review_commit,
    })

    expected_ids = {
        "runtime_dependency",
        "task_workspace",
        "task_identity",
        "branch_review_handoff",
        "issue_scope_ledger",
        "publication_content",
        "review_range_and_working_tree",
        "invocation_freshness",
    }
    for entry_id in sorted(expected_ids - set(bindings)):
        entry_errors = [
            item
            for item in errors
            if item.startswith(entry_id + ":")
        ]
        bindings[entry_id] = task_publication_binding(
            {
                "entry_precondition_id": entry_id,
                "errors": entry_errors or ["objective evidence unavailable"],
            },
            status="failed",
        )
    return bindings, sorted(set(errors)), review_handoff, repository

def task_publication_semantic_errors(
    authored: dict[str, Any],
    *,
    branch_review_commit: str,
) -> list[str]:
    errors: list[str] = []
    pr_payload = authored.get("pr_payload")
    if not isinstance(pr_payload, dict) or set(pr_payload) != {"title", "body"}:
        errors.append("publication pr_payload must contain exactly title and body")
    elif (
        not isinstance(pr_payload.get("title"), str)
        or not pr_payload["title"].strip()
        or not isinstance(pr_payload.get("body"), str)
        or not pr_payload["body"].strip()
    ):
        errors.append("publication pr_payload title and body must be non-empty")
    candidate_commit = str(
        authored.get("branch_review_commit") or branch_review_commit
    )
    if candidate_commit != branch_review_commit:
        errors.append(
            "publication branch_review_commit does not match current Branch Review"
        )
    dimensions = authored.get("dimensions")
    if not isinstance(dimensions, list):
        errors.append("publication dimensions must be a list")
        dimensions = []
    ids = [item.get("id") for item in dimensions if isinstance(item, dict)]
    if ids != list(TASK_PUBLICATION_DIMENSIONS):
        errors.append("publication dimensions must contain the exact ordered ten ids")
    for item in dimensions:
        if (
            not isinstance(item, dict)
            or set(item) != {"id", "status", "summary", "evidence_refs"}
            or item.get("status") not in {"passed", "finding", "blocked"}
            or not isinstance(item.get("summary"), str)
            or not str(item.get("summary") or "").strip()
            or not isinstance(item.get("evidence_refs"), list)
            or not item.get("evidence_refs")
            or any(
                not isinstance(value, str) or not value.strip()
                for value in item.get("evidence_refs", [])
            )
        ):
            errors.append("publication dimension evidence is incomplete")
            break

    findings = authored.get("findings")
    if not isinstance(findings, list):
        errors.append("publication findings must be a list")
        findings = []
    refs: list[str] = []
    for finding in findings:
        if not isinstance(finding, dict):
            errors.append("publication finding must be an object")
            continue
        required = {
            "finding_ref",
            "dimension",
            "summary",
            "scope_basis",
            "evidence_refs",
            "affected_artifacts",
            "route_class",
            "status",
            "closure_evidence",
        }
        if set(finding) != required:
            errors.append("publication finding fields are incomplete or unknown")
            continue
        refs.append(str(finding.get("finding_ref") or ""))
        if (
            finding.get("dimension") not in TASK_PUBLICATION_DIMENSIONS
            or finding.get("route_class")
            not in {"metadata_revision", "task_work", "external_blocker"}
            or finding.get("status") not in {"open", "closed"}
        ):
            errors.append("publication finding enum is invalid")
        textual_fields = ("summary", "scope_basis")
        list_fields = ("evidence_refs", "affected_artifacts")
        if any(
            not isinstance(finding.get(field), str)
            or not str(finding.get(field) or "").strip()
            for field in textual_fields
        ) or any(
            not isinstance(finding.get(field), list)
            or not finding.get(field)
            or any(
                not isinstance(value, str) or not value.strip()
                for value in finding.get(field, [])
            )
            for field in list_fields
        ):
            errors.append("publication finding evidence must be non-empty")
        closure = finding.get("closure_evidence")
        if (
            not isinstance(closure, list)
            or any(not isinstance(value, str) or not value.strip() for value in closure)
            or (finding.get("status") == "closed" and not closure)
            or (finding.get("status") == "open" and bool(closure))
        ):
            errors.append("publication finding closure evidence does not match status")
    if len(refs) != len(set(refs)) or any(not value for value in refs):
        errors.append("publication finding refs must be unique and non-empty")

    conclusions = authored.get("conclusions")
    if not isinstance(conclusions, dict) or set(conclusions) != {
        "issue_scope",
        "docs_ssot",
        "safety_deployment",
    }:
        errors.append("publication conclusions are incomplete")
        conclusions = {}
    for conclusion in conclusions.values():
        if (
            not isinstance(conclusion, dict)
            or set(conclusion) != {"status", "summary", "evidence_refs"}
            or conclusion.get("status") not in {"passed", "finding", "blocked"}
            or not isinstance(conclusion.get("summary"), str)
            or not str(conclusion.get("summary") or "").strip()
            or not isinstance(conclusion.get("evidence_refs"), list)
            or not conclusion.get("evidence_refs")
        ):
            errors.append("publication conclusion evidence is incomplete")
            break

    route = authored.get("route")
    typed_exit = route.get("typed_exit") if isinstance(route, dict) else None
    if typed_exit not in TASK_PUBLICATION_CONSUMERS:
        errors.append("publication route is invalid")
        return sorted(set(errors))
    expected_route_fields = (
        {"typed_exit", "reason_code", "remediation"}
        if typed_exit == "blocked"
        else {"typed_exit"}
    )
    if set(route) != expected_route_fields:
        errors.append("publication route fields are incomplete or unknown")

    dimension_statuses = {
        str(item.get("id")): str(item.get("status"))
        for item in dimensions
        if isinstance(item, dict)
    }
    open_findings = [
        item
        for item in findings
        if isinstance(item, dict) and item.get("status") == "open"
    ]
    for finding in open_findings:
        if dimension_statuses.get(str(finding.get("dimension") or "")) == "passed":
            errors.append(
                "open publication finding must reference a non-passed dimension"
            )
    open_finding_dimensions = {
        str(item.get("dimension") or "") for item in open_findings
    }
    if any(
        status != "passed" and dimension not in open_finding_dimensions
        for dimension, status in dimension_statuses.items()
    ):
        errors.append(
            "every non-passed publication dimension requires open finding evidence"
        )

    if typed_exit == "ready":
        if any(status != "passed" for status in dimension_statuses.values()):
            errors.append("ready requires every publication dimension to pass")
        if any(item.get("status") != "closed" for item in findings):
            errors.append("ready requires every publication finding to close")
        if any(item.get("status") != "passed" for item in conclusions.values()):
            errors.append("ready requires every publication conclusion to pass")
    elif typed_exit == "return_to_task_work":
        if not any(status == "finding" for status in dimension_statuses.values()):
            errors.append("return_to_task_work requires a finding publication dimension")
        if any(status == "blocked" for status in dimension_statuses.values()):
            errors.append("return_to_task_work cannot carry a blocked publication dimension")
        if not any(item.get("route_class") == "task_work" for item in open_findings):
            errors.append("return_to_task_work requires an open task_work finding")
        if any(
            item.get("route_class") != "task_work"
            or dimension_statuses.get(str(item.get("dimension") or "")) != "finding"
            for item in open_findings
        ):
            errors.append(
                "return_to_task_work open findings must reference finding dimensions"
            )
        if any(item.get("status") == "blocked" for item in conclusions.values()):
            errors.append(
                "return_to_task_work cannot carry a blocked publication conclusion"
            )
    else:
        if (
            not isinstance(route.get("reason_code"), str)
            or not str(route.get("reason_code") or "").strip()
            or not isinstance(route.get("remediation"), str)
            or not str(route.get("remediation") or "").strip()
        ):
            errors.append("blocked requires non-empty reason_code and remediation")
        if not any(status == "blocked" for status in dimension_statuses.values()):
            errors.append("blocked requires a blocked publication dimension")
        if not any(
            item.get("route_class") == "external_blocker"
            for item in open_findings
        ):
            errors.append("blocked requires an open external_blocker finding")
        if any(
            item.get("route_class") != "external_blocker"
            or dimension_statuses.get(str(item.get("dimension") or "")) != "blocked"
            for item in open_findings
        ):
            errors.append("blocked open findings must reference blocked dimensions")
        if not any(item.get("status") == "blocked" for item in conclusions.values()):
            errors.append("blocked requires a blocked publication conclusion")
    return sorted(set(errors))

def task_publication_closeout_preflight(
    root: Path,
    task_dir: Path,
    branch_review_commit: str,
    pr_payload: dict[str, Any],
) -> dict[str, Any]:
    """Run the exact side-effect-free Finalizer producer preflight."""
    config = load_config(root)
    task_context = load_task_runtime_identity(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    args = argparse.Namespace(
        repo=None,
        remote=None,
        base_branch=None,
        title=None,
        include_finalization_gate=True,
    )
    return prepare_closeout(
        root,
        args,
        config,
        task_dir,
        task_context,
        publication_ready={
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": repo_relative(root, task_dir),
            "branch_review_commit": branch_review_commit,
            "pr_title": pr_payload["title"],
            "pr_body": pr_payload["body"],
        },
    )

def task_publication_check_errors(
    root: Path,
    task_dir: Path,
    payload: dict[str, Any],
) -> list[str]:
    errors = skill_json_schema_validation_errors(
        payload,
        task_publication_schema(root),
        "task publication readiness",
    )
    if payload.get("task_ref") != repo_relative(root, task_dir):
        errors.append("task publication task identity mismatch")
    route = payload.get("route") if isinstance(payload.get("route"), dict) else {}
    typed_exit = route.get("typed_exit")
    branch_review_commit = str(payload.get("branch_review_commit") or "")
    reviewed_content_sha256 = str(payload.get("reviewed_content_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", branch_review_commit):
        errors.append("task publication branch_review_commit is invalid")
    else:
        continuity_errors = review_branch_content_continuity_errors(
            root,
            task_dir,
            branch_review_commit,
            reviewed_content_sha256,
            current_head(root),
        )
        errors.extend(
            "task publication reviewed content is stale: " + item
            for item in continuity_errors
            if not (
                typed_exit == "return_to_task_work"
                and item.startswith(BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX)
                and len(item) > len(BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX)
            )
        )
    if (
        typed_exit != "return_to_task_work"
        and payload.get("reviewed_content_sha256")
        != reviewed_content_identity(root)["sha256"]
    ):
        errors.append("task publication reviewed content identity is stale")
    invocation = {
        "task_ref": payload.get("task_ref"),
        "branch_review_commit": branch_review_commit,
        "pr_payload": copy.deepcopy(payload.get("pr_payload")),
    }
    _, entry_errors, _, _ = task_publication_entry_precondition_bindings(
        root,
        task_dir,
        load_config(root),
        invocation,
    )
    if typed_exit == "ready":
        errors.extend(entry_errors)
        try:
            task_publication_closeout_preflight(
                root,
                task_dir,
                branch_review_commit,
                payload.get("pr_payload") or {},
            )
        except WorkflowError as exc:
            errors.append(f"finalizer_preflight:{exc}")
            errors.extend(
                f"finalizer_preflight:{item}"
                for item in exc.payload.get("errors", [])
                if isinstance(item, str)
            )
    errors.extend(
        task_publication_semantic_errors(
            payload,
            branch_review_commit=str(payload.get("branch_review_commit") or ""),
        )
    )
    return sorted(set(errors))

def cmd_record_task_publication_review(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_runtime_identity(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    authored = contract_wording_read_input(
        root,
        args.input,
        "guru-review-task-publication recorder",
    )
    path = task_publication_path(root, task_dir)
    profile = authored.get("profile")
    mode = authored.get("mode")
    review_intent = authored.get("review_intent")
    authoring_fields = {
        "profile",
        "mode",
        "review_intent",
        "pr_payload",
        "dimensions",
        "findings",
        "conclusions",
        "route",
    }
    if profile == "publication_review_stale":
        authoring_fields.add("stale_reason")
    authoring_errors: list[str] = []
    if set(authored) != authoring_fields:
        authoring_errors.append(
            "publication authoring fields are incomplete or unknown"
        )
    if profile not in {"publication_review", "publication_review_stale"}:
        authoring_errors.append("publication profile is invalid")
    if mode not in {"workflow", "standalone"}:
        authoring_errors.append("publication mode is invalid")
    if review_intent not in {
        "initial_review",
        "metadata_revision_review",
        "stale_reentry_review",
    }:
        authoring_errors.append("publication review_intent is invalid")
    if profile == "publication_review_stale":
        if review_intent != "stale_reentry_review":
            authoring_errors.append(
                "stale publication requires stale_reentry_review intent"
            )
        if not isinstance(authored.get("stale_reason"), str) or not str(
            authored.get("stale_reason") or ""
        ).strip():
            authoring_errors.append(
                "stale publication requires non-empty stale_reason"
            )
    if authoring_errors:
        raise WorkflowError(
            "AI-authored task publication review is structurally invalid.",
            exit_code=2,
            payload={"error_codes": sorted(set(authoring_errors))},
        )
    invocation = {
        "profile": profile,
        "mode": mode,
        "review_intent": review_intent,
        "stale_reason": authored.get("stale_reason"),
        "task_ref": repo_relative(root, task_dir),
        "branch_review_commit": str(
            getattr(args, "branch_review_commit", "") or ""
        ),
        "pr_payload": copy.deepcopy(authored.get("pr_payload")),
    }
    entry_bindings, entry_errors, review_gate, repository = (
        task_publication_entry_precondition_bindings(
            root,
            task_dir,
            config,
            invocation,
        )
    )
    route = authored.get("route") if isinstance(authored.get("route"), dict) else {}
    typed_exit = route.get("typed_exit")
    if entry_errors and typed_exit == "ready":
        raise WorkflowError(
            "Ready task publication entry preconditions are missing, stale, or incomplete.",
            exit_code=2,
            payload={
                "task_ref": repo_relative(root, task_dir),
                "error_codes": entry_errors,
            },
        )
    branch_review_commit = str(invocation["branch_review_commit"])
    payload: dict[str, Any] = {
        "schema_version": "4.0",
        "skill_id": TASK_PUBLICATION_SKILL_ID,
        "task_ref": repo_relative(root, task_dir),
        "branch_review_commit": branch_review_commit,
        "reviewed_content_sha256": reviewed_content_identity(root)["sha256"],
        "pr_payload": copy.deepcopy(authored.get("pr_payload")),
        "dimensions": copy.deepcopy(authored.get("dimensions")),
        "findings": copy.deepcopy(authored.get("findings")),
        "conclusions": copy.deepcopy(authored.get("conclusions")),
        "route": copy.deepcopy(route),
    }
    errors = task_publication_check_errors(
        root,
        task_dir,
        payload,
    )
    if errors:
        raise WorkflowError(
            "Task publication readiness materialization failed validation.",
            exit_code=2,
            payload={"error_codes": errors},
        )
    if not args.dry_run:
        write_json(path, payload)
    return {
        **payload,
        "artifact_path": str(path),
        "dry_run": bool(args.dry_run),
    }

def cmd_check_task_publication_review(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_runtime_identity(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    path = task_publication_path(root, task_dir)
    if not path.is_file() or path.is_symlink():
        raise WorkflowError(
            "Task publication readiness artifact is missing or unsafe.",
            exit_code=2,
        )
    payload = read_json(path)
    errors = task_publication_check_errors(
        root,
        task_dir,
        payload,
    )
    expected_exit = str(getattr(args, "expected_exit", "") or "")
    typed_exit = (payload.get("route") or {}).get("typed_exit")
    if expected_exit and typed_exit != expected_exit:
        errors.append("task publication expected exit mismatch")
    if errors:
        raise WorkflowError(
            "Task publication readiness is missing, stale, or incomplete.",
            exit_code=2,
            payload={"artifact_path": str(path), "errors": sorted(set(errors))},
        )
    return {
        "status": "ok",
        "artifact_path": str(path),
        "task_dir": str(task_dir),
        "task_ref": payload["task_ref"],
        "branch_review_commit": payload["branch_review_commit"],
        "typed_exit": typed_exit,
        "owner_result": payload,
    }

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

def provenance_tail_manifest_errors(
    before: Any,
    after: Any,
    reviewed_content_head: str,
) -> list[str]:
    """Validate the only manifest mutation allowed after reviewed content."""
    errors: list[str] = []
    if not isinstance(before, dict) or not isinstance(after, dict):
        return ["provenance_tail_manifest_invalid"]
    if re.fullmatch(r"[0-9a-f]{40}", str(reviewed_content_head or "")) is None:
        errors.append("provenance_tail_reviewed_head_invalid")
    changed = provenance_tail_manifest_field_diff(before, after)
    unexpected = sorted(
        set(changed) - PROVENANCE_TAIL_ALLOWED_FIELDS,
        key=lambda item: item.encode("utf-8"),
    )
    if unexpected:
        errors.append("provenance_tail_manifest_fields_outside_allowlist")
    source = after.get("source")
    if not isinstance(source, dict):
        errors.append("provenance_tail_source_missing")
    else:
        if source.get("ref") != reviewed_content_head:
            errors.append("provenance_tail_source_ref_mismatch")
        if source.get("commit") != reviewed_content_head:
            errors.append("provenance_tail_source_commit_mismatch")
        if source.get("tree_state") != "clean":
            errors.append("provenance_tail_source_not_clean")
        if source.get("is_mutable_ref") is not False:
            errors.append("provenance_tail_source_ref_mutable")
    if "installed_at" in after and not isinstance(after["installed_at"], str):
        errors.append("provenance_tail_installed_at_invalid")
    return sorted(set(errors))

def provenance_tail_commit_errors(
    root: Path,
    reviewed_content_head: str,
    publication_head: str,
    *,
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
                provenance_tail_manifest_errors(before, after, reviewed_content_head)
            )
    return sorted(set(errors))

def finalizer_publication_identity(
    root: Path,
    reviewed_content_head: str,
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
    errors = provenance_tail_commit_errors(root, reviewed_content_head, publication_head)
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

SKILL_SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"

TASK_PUBLICATION_SKILL_ID = "guru-review-task-publication"

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
        ["python3", "-c", parser, str(config_path)],
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

def closeout_json_artifact_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

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
        if set(value) != keys:
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
    if (
        existing_plan is not None
        and publication_ready is not None
        and publication_commit
        != str(existing_plan.get("git", {}).get("branch_review_commit") or "")
    ):
        prospective_git = {
            "repo": normalize_github_repository(
                str(args.repo or config.get("github_repo") or "").strip()
                or infer_github_repo(root)
            ),
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
            raise WorkflowError(
                "Publication preflight cannot reuse a retired pre-#205 closeout plan.",
                exit_code=2,
                payload={"reason_code": "publication_reprepare_required"},
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

def context_canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

def context_digest(value: Any) -> str:
    return hashlib.sha256(context_canonical_bytes(value)).hexdigest()

def context_sort(values: set[str] | list[str]) -> list[str]:
    return sorted(set(values), key=lambda item: item.encode("utf-8"))
