#!/usr/bin/env python3
"""Guru Team Trellis workflow companion scripts.

The script intentionally uses only the Python standard library plus external
`git` and `gh` commands. It is installed into target repositories under
`.trellis/guru-team/` and never modifies Trellis upstream files.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


DEFAULTS: dict[str, Any] = {
    "github_repo": "",
    "source_issue_required": False,
    "auto_create_issue": False,
    "duplicate_search_required": True,
    "duplicate_candidate_limit": 5,
    "duplicate_high_similarity_action": "confirm",
    "branch_prefix": "",
    "branch_type_default": "chore",
    "base_branch_candidates": ["dev", "develop", "main", "master"],
    "workspace_mode": "worktree",
    "worktree_root": "",
    "task_start_context_artifact": "task-start-context.json",
    "runtime_root": ".trellis/.runtime/guru-team",
    "marketplace_verification_artifact": "marketplace-verification.json",
    "artifact_language": "zh-CN",
    "review_gate": {
        "artifact_path": "review-gate.json",
        "block_priorities": ["P0", "P1", "P2", "P3"],
        "require_head_match": True,
        "require_deployment_impact_evidence": True,
    },
    "publish": {
        "draft": False,
        "close_keyword": "Closes",
        "pr_language": "zh-CN",
        "remote": "origin",
    },
    "created_issue_labels": [],
    "closeout_markers": ["最终收口口径", "Final Closeout"],
}

VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}
BLOCKING_PRIORITIES = {"P0", "P1", "P2"}
PLANNING_APPROVAL_ARTIFACT = "planning-approval.json"
PLANNING_APPROVAL_SCHEMA_VERSION = "1.2"
PLANNING_APPROVAL_CONFIRMATION_SOURCE = "explicit-post-planning-review"
PLANNING_AMBIGUITY_STATUS_PASSED = "passed"
PLANNING_AMBIGUITY_CONTROLLED_TERMS = [
    "可以",
    "允许",
    "建议",
    "推荐",
    "可选",
    "尽量",
    "尽可能",
    "最好",
    "应该",
    "应当",
    "原则上",
    "一般",
    "通常",
    "视情况",
    "根据情况",
    "根据需要",
    "按需",
    "必要时",
    "如有需要",
    "需要时",
    "适当",
    "适当时",
    "合理",
    "合理时",
    "类似",
    "相关",
    "相应",
    "等",
    "等等",
    "之类",
    "一些",
    "若干",
    "部分",
    "至少",
    "默认",
]
PLANNING_AMBIGUITY_SCAN_SCOPE = ["prd.md", "design.md", "implement.md"]
PLANNING_AMBIGUITY_CLASSIFICATIONS = [
    "contract_violation",
    "quoted_source_non_contract",
    "term_definition",
    "literal_identifier",
    "historical_record_non_contract",
    "deterministic_threshold",
    "deterministic_default",
    "deterministic_option",
    "deterministic_reference",
]
PLANNING_AMBIGUITY_BLOCKING_CLASSIFICATIONS = {"contract_violation"}
PLANNING_AMBIGUITY_REQUIRED_DIMENSIONS = [
    "no_requirement_weakening",
    "source_issue_semantics_preserved",
    "conditional_paths_have_conditions",
    "no_parallel_implementation_paths",
    "gates_have_machine_verifiable_conditions",
    "acceptance_criteria_are_deterministic",
    "external_quotes_are_labeled_non_contract",
]
PHASE2_CHECK_ARTIFACT = "phase2-check.json"
AGENT_ASSIGNMENT_ARTIFACT = "agent-assignment.json"
REVIEW_REPORT_ARTIFACT = "review.md"
MARKETPLACE_VERIFICATION_ARTIFACT = "marketplace-verification.json"
FINISH_SUMMARY_ARTIFACT = "finish-summary.json"
FINISH_SUMMARY_INDEX_ARTIFACT = "finish-summary-index.json"
FINISH_SUMMARY_SCHEMA_VERSION = 1
FINISH_SUMMARY_GENERATOR = "guru-team.finish-work"
FINISH_SUMMARY_BACKFILL_GENERATOR = "guru-team.finish-summary-backfill"
FINISH_SUMMARY_GENERATORS = {FINISH_SUMMARY_GENERATOR, FINISH_SUMMARY_BACKFILL_GENERATOR}
FINISH_SUMMARY_SURFACE_KINDS = {
    "workflow", "script", "schema", "preset", "overlay", "skill", "prompt",
    "docs", "test", "config", "task-artifact", "github", "other",
}
FINISH_SUMMARY_ARTIFACT_FILES = {
    "prd": "prd.md",
    "design": "design.md",
    "implement": "implement.md",
    "finish_summary_index": FINISH_SUMMARY_INDEX_ARTIFACT,
    "issue_scope_ledger": "issue-scope-ledger.json",
    "phase2_check": PHASE2_CHECK_ARTIFACT,
    "review": REVIEW_REPORT_ARTIFACT,
    "review_gate": "review-gate.json",
    "pr_body": "pr-body.md",
    "pr_readiness": "pr-readiness.json",
    "marketplace_verification": MARKETPLACE_VERIFICATION_ARTIFACT,
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
PR_BODY_ARTIFACT = "pr-body.md"
PR_READINESS_PUBLISH_INPUT_KEYS = {
    "repo",
    "base_branch",
    "head_branch",
    "reviewed_head_sha",
    "title",
    "body_source",
    "body_sha256",
    "draft",
    "reviewed_source",
}
REVIEW_ROUND_REPORT_DIR = "reviews"
HUMAN_MARKDOWN_ARTIFACTS = [
    {
        "label": "PRD",
        "filename": "prd.md",
        "purpose": "需求、范围、验收标准",
        "missing_status": "未生成",
    },
    {
        "label": "Design",
        "filename": "design.md",
        "purpose": "技术设计与取舍",
        "missing_status": "未生成",
    },
    {
        "label": "Implement Plan",
        "filename": "implement.md",
        "purpose": "执行计划与验证计划",
        "missing_status": "未生成",
    },
    {
        "label": "Review Report",
        "filename": REVIEW_REPORT_ARTIFACT,
        "purpose": "AI/human review 报告",
        "missing_status": "未执行",
    },
    {
        "label": "PR Body",
        "filename": "pr-body.md",
        "purpose": "给 GitHub reviewer 的 PR 说明",
        "missing_status": "未生成",
    },
]
GURU_TEAM_EXTENSION_MANIFEST = Path(".trellis/guru-team/extension.json")
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
    "pr-body.md",
    "pr-readiness.json",
]
WORKSPACE_BOUNDARY_REVIEW_METADATA = {
    PLANNING_APPROVAL_ARTIFACT,
    PHASE2_CHECK_ARTIFACT,
    AGENT_ASSIGNMENT_ARTIFACT,
    REVIEW_REPORT_ARTIFACT,
    "review-gate.json",
    "pr-body.md",
    "pr-readiness.json",
}
DEFAULT_PLANNING_ARTIFACTS = ["prd.md", "design.md", "implement.md"]
DEFAULT_PHASE2_TASK_ARTIFACTS = [
    "prd.md",
    "design.md",
    "implement.md",
    PLANNING_APPROVAL_ARTIFACT,
]
REQUIRED_PHASE2_COVERAGE = [
    "requirements",
    "design",
    "code",
    "tests",
    "spec_sync",
    "cross_layer",
    "docs_ssot",
    "deployment",
]
RESOLVED_FINDING_STATUSES = {"resolved", "fixed", "closed"}
INDEPENDENT_REVIEW_SOURCE = "independent-agent"
FORBIDDEN_REVIEW_REPORT_ENGLISH_TEMPLATE_HEADINGS = [
    "Review Rounds",
    "Findings Lifecycle",
    "Evidence Handoff",
    "Deployment / safety impact",
    "Follow-up Candidates",
    "Files Checked",
    "Issues Found and Fixed",
    "Issues Not Fixed",
    "Verification Results",
    "Summary",
]
AGENT_ASSIGNMENT_SCHEMA_VERSION = "1.1"
ALLOWED_LOGICAL_ROLES = [
    "实现代理",
    "阶段二检查代理",
    "问题发现审查代理",
    "问题闭环审查代理",
    "最终放行审查代理",
]
ALLOWED_REUSE_DECISIONS = {"reuse", "replace", "reuse-for-closure", "new-agent", "not-applicable"}
AGENT_PROGRESS_EVENTS = {
    "explicit-message-observed",
    "tool-activity-observed",
    "command-output-observed",
    "platform-progress-observed",
    "status-response-observed",
}
AGENT_TERMINAL_EVENTS = {"completed", "failed"}
AGENT_CONTROL_EVENTS = {
    "assigned",
    "status-requested",
    "status-request-failed",
    "stale-assessed",
    "resume-same-agent",
    "replacement-started",
    "terminated-unfinished",
}
AGENT_WORKSPACE_AUDIT_EVENTS = {"workspace-boundary-violation"}
ALLOWED_AGENT_STATUS_EVENTS = (
    AGENT_PROGRESS_EVENTS
    | AGENT_TERMINAL_EVENTS
    | AGENT_CONTROL_EVENTS
    | AGENT_WORKSPACE_AUDIT_EVENTS
)
AGENT_LIVENESS_DECISIONS = {
    "workspace_boundary_violation_progress",
    "progress_observed",
    "status_request_required",
    "continue_waiting_no_repeat_ping",
    "stale_allowed",
    "blocked_missing_evidence",
}
AGENT_REPLACEMENT_REASONS = {
    "max_progress_silence_exceeded",
    "terminal_failed_incomplete",
    "manual_or_platform_terminated_unfinished",
}
AGENT_TERMINATION_REASONS = {
    "stale_cutover",
    "manual_or_platform_terminated_unfinished",
}
AGENT_STATUS_EVENT_SOURCES = {"main-session", "recorder", "checker"}
AGENT_PROGRESS_SOURCE_KINDS = {
    "task_head",
    "task_status",
    "task_diff_stat",
    "task_mtime",
    "source_head",
    "source_status",
    "source_diff_stat",
    "source_mtime",
    "status_event",
}
AGENT_LIVENESS_SNAPSHOT_FIELDS = [
    "task_head",
    "task_content_status_digest",
    "task_content_diff_stat_digest",
    "task_content_max_mtime",
    "source_head",
    "source_status_digest",
    "source_diff_stat_digest",
    "source_max_mtime",
    "progress_events_count",
    "progress_events_digest",
    "progress_events_newest_event_id",
]
AGENT_LIVENESS_BLOCKED_DECISION = "blocked_missing_evidence"
AGENT_LIVENESS_DEFAULT_SCAN_INTERVAL_SECONDS = 120
AGENT_LIVENESS_DEFAULT_MAX_SILENCE_SECONDS = 180
PLACEHOLDER_EVIDENCE_VALUES = {"", "n/a", "na", "none", "unknown", "placeholder", "todo", "tbd"}
SELF_REVIEWER_PATTERNS = [
    re.compile(r"(^|[-_./\s])main[-_./\s]*session($|[-_./\s])", re.IGNORECASE),
    re.compile(r"(^|[-_./\s])self[-_./\s]*review($|[-_./\s])", re.IGNORECASE),
]
METADATA_ONLY_PREFIXES = (".trellis/tasks/", ".trellis/.runtime/")
METADATA_ONLY_FILES: set[str] = set()
PHASE2_POST_COMMIT_MUTABLE_ARTIFACTS = {
    "issue-scope-ledger.json",
    "pr-body.md",
    "pr-readiness.json",
    AGENT_ASSIGNMENT_ARTIFACT,
    REVIEW_REPORT_ARTIFACT,
    "review-gate.json",
    MARKETPLACE_VERIFICATION_ARTIFACT,
}


def is_phase2_post_commit_mutable_artifact_path(artifact_path: str) -> bool:
    normalized = artifact_path.strip().replace("\\", "/")
    if not normalized:
        return False
    if Path(normalized).name in PHASE2_POST_COMMIT_MUTABLE_ARTIFACTS:
        return True
    parts = [part for part in normalized.split("/") if part]
    return (
        len(parts) >= 4
        and parts[0] == ".trellis"
        and parts[1] == "tasks"
        and parts[-2] == REVIEW_ROUND_REPORT_DIR
        and parts[-1].endswith(".md")
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
    maximum_items: int = 100,
    minimum_length: int = 1,
    maximum_length: int = 500,
    exact_identity: bool = False,
) -> list[str]:
    if not isinstance(values, list):
        return [f"{label} must be an array."]
    errors: list[str] = []
    if not (minimum_items <= len(values) <= maximum_items):
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


def finish_summary_retrieval_text(task_title: str, index: dict[str, Any]) -> str:
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
    return "\n".join(value.strip() for value in values if value.strip())


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
            "branches": (0, 1, 1, 300), "paths": (0, 2000, 1, 500),
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


def load_finish_summary_index(task_dir: Path, value: str | None) -> tuple[Path, dict[str, Any]]:
    if not value:
        raise WorkflowError(
            "finish-work requires task-local finish-summary-index.json AI review evidence.",
            exit_code=2,
            payload={"required_flag": "--finish-summary-index-file"},
        )
    path = Path(value)
    if not path.is_absolute():
        path = (task_dir / path) if len(path.parts) == 1 else (repo_root(task_dir) / path)
    resolved = path.resolve()
    if resolved.parent != task_dir.resolve() or resolved.name != FINISH_SUMMARY_INDEX_ARTIFACT:
        raise WorkflowError("finish-summary index must be the task-local finish-summary-index.json file.", exit_code=2)
    if not resolved.is_file():
        raise WorkflowError(f"finish-summary index not found: {resolved}", exit_code=2)
    payload = read_json(resolved)
    errors: list[str] = []
    if set(payload) != {"schema_version", "index"}:
        errors.append("finish-summary index top-level keys must equal schema_version and index.")
    if payload.get("schema_version") != FINISH_SUMMARY_SCHEMA_VERSION:
        errors.append("finish-summary index schema_version must be integer 1.")
    errors.extend(finish_summary_index_errors(payload.get("index"), final=False))
    if errors:
        raise WorkflowError("finish-summary index validation failed.", exit_code=2, payload={"errors": errors})
    return resolved, payload


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
        for key, filename in FINISH_SUMMARY_ARTIFACT_FILES.items()
        if (task_dir / filename).is_file()
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


def finish_summary_git_paths(root: Path, base_ref: str, *, include_worktree: bool) -> list[str]:
    paths, _protected_paths_filtered, _snapshot_unavailable = finish_summary_git_path_snapshot(
        root, base_ref, include_worktree=include_worktree
    )
    return paths


def build_finish_summary(
    root: Path,
    task_dir: Path,
    task_context: dict[str, Any],
    ledger: dict[str, Any],
    index_payload: dict[str, Any],
    reviewed_head: str,
    *,
    pr_url: str = "",
    changed_paths: list[str] | None = None,
) -> dict[str, Any]:
    task = task_json(task_dir)
    base_branch = str(task_context.get("base_branch") or task.get("base_branch") or "").strip()
    base_ref = str(task_context.get("base_ref") or diff_base_ref(root, base_branch)).strip()
    commits_proc = run(["git", "rev-list", "--reverse", f"{base_ref}..{reviewed_head}"], cwd=root, check=False)
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
    artifacts = finish_summary_artifacts(task_dir)
    index = copy.deepcopy(index_payload["index"])
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
    index["retrieval_text"] = finish_summary_retrieval_text(str(task.get("title") or task.get("name") or task_dir.name), index)
    payload = {
        "schema_version": FINISH_SUMMARY_SCHEMA_VERSION,
        "generated_at": now_iso(),
        "generator": FINISH_SUMMARY_GENERATOR,
        "task": {
            "slug": task_dir.name,
            "title": str(task.get("title") or task.get("name") or task_dir.name),
            "status": "completed",
            "artifact_dir": str(task_context.get("task_artifact_dir") or ""),
            "archive_dir": repo_relative(root, task_dir),
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
    errors = finish_summary_errors(payload, task_dir=task_dir)
    if errors:
        raise WorkflowError("Generated finish-summary validation failed.", exit_code=2, payload={"errors": errors})
    return payload


def finish_summary_errors(payload: Any, *, task_dir: Path | None = None) -> list[str]:
    if not isinstance(payload, dict):
        return ["finish-summary must be an object."]
    generator = payload.get("generator")
    expected_keys = {"schema_version", "generated_at", "generator", "task", "git", "github", "artifacts", "index"}
    if generator == FINISH_SUMMARY_BACKFILL_GENERATOR:
        expected_keys.add("backfill")
    errors: list[str] = []
    if set(payload) != expected_keys:
        errors.append(f"finish-summary top-level keys must equal {sorted(expected_keys)}.")
    if payload.get("schema_version") != FINISH_SUMMARY_SCHEMA_VERSION:
        errors.append("schema_version must be integer 1.")
    generated_at = payload.get("generated_at")
    if not isinstance(generated_at, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", generated_at):
        errors.append("generated_at must be second-precision UTC RFC3339.")
    if generator not in FINISH_SUMMARY_GENERATORS:
        errors.append("generator is invalid.")
    task = payload.get("task")
    if not isinstance(task, dict) or set(task) != {"slug", "title", "status", "artifact_dir", "archive_dir"}:
        errors.append("task object keys are invalid.")
        task = {}
    errors.extend(finish_summary_text_errors(task.get("slug"), "task.slug", 1, 200))
    errors.extend(finish_summary_text_errors(task.get("title"), "task.title", 1, 500))
    if task.get("status") != "completed":
        errors.append("task.status must be completed.")
    errors.extend(finish_summary_path_errors(task.get("artifact_dir"), "task.artifact_dir", allow_empty=generator == FINISH_SUMMARY_BACKFILL_GENERATOR))
    errors.extend(finish_summary_path_errors(task.get("archive_dir"), "task.archive_dir"))
    if task.get("archive_dir") and not str(task.get("archive_dir")).startswith(".trellis/tasks/archive/"):
        errors.append("task.archive_dir must be under .trellis/tasks/archive/.")
    if generator == FINISH_SUMMARY_GENERATOR and task.get("artifact_dir"):
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
    minimum_git_text = 0 if generator == FINISH_SUMMARY_BACKFILL_GENERATOR else 1
    errors.extend(finish_summary_text_errors(git.get("base_branch"), "git.base_branch", minimum_git_text, 300))
    errors.extend(finish_summary_text_errors(git.get("branch"), "git.branch", minimum_git_text, 300))
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
    if not isinstance(changed_paths, list) or len(changed_paths) > 2000:
        errors.append("git.changed_paths must be an array with at most 2000 items.")
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
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, dict) or any(key not in FINISH_SUMMARY_ARTIFACT_FILES for key in artifacts):
        errors.append("artifacts keys are invalid.")
        artifacts = {}
    for key, path in artifacts.items():
        errors.extend(finish_summary_path_errors(path, f"artifacts.{key}"))
        if path != FINISH_SUMMARY_ARTIFACT_FILES[key]:
            errors.append(f"artifacts.{key} must equal {FINISH_SUMMARY_ARTIFACT_FILES[key]}.")
        if task_dir is not None and not (task_dir / str(path)).is_file():
            errors.append(f"artifacts.{key} does not exist in the archived task.")
    errors.extend(finish_summary_index_errors(payload.get("index"), artifacts=artifacts, final=True))
    index = payload.get("index") if isinstance(payload.get("index"), dict) else {}
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
    expected_retrieval = finish_summary_retrieval_text(str(task.get("title") or ""), index)
    if index.get("retrieval_text") != expected_retrieval:
        errors.append("index.retrieval_text must equal the deterministic derived text.")
    if generator == FINISH_SUMMARY_BACKFILL_GENERATOR:
        backfill = payload.get("backfill")
        expected_backfill_keys = {"generated", "generated_at", "source_artifacts", "missing_fields", "confidence"}
        if not isinstance(backfill, dict) or set(backfill) != expected_backfill_keys:
            errors.append("backfill object keys are invalid.")
        else:
            if backfill.get("generated") is not True:
                errors.append("backfill.generated must be true.")
            if not isinstance(backfill.get("generated_at"), str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", backfill["generated_at"]):
                errors.append("backfill.generated_at must be second-precision UTC RFC3339.")
            source_artifacts = backfill.get("source_artifacts")
            errors.extend(
                finish_summary_string_array_errors(
                    source_artifacts,
                    "backfill.source_artifacts",
                    maximum_items=20,
                    maximum_length=500,
                    exact_identity=True,
                )
            )
            if isinstance(source_artifacts, list):
                for path_index, path in enumerate(source_artifacts):
                    path_errors = finish_summary_path_errors(
                        path, f"backfill.source_artifacts[{path_index}]"
                    )
                    errors.extend(path_errors)
                    if (
                        not path_errors
                        and task_dir is not None
                        and isinstance(path, str)
                        and not (task_dir / path).is_file()
                    ):
                        errors.append(
                            f"backfill.source_artifacts[{path_index}] does not exist in the archived task."
                        )
            errors.extend(
                finish_summary_string_array_errors(
                    backfill.get("missing_fields"),
                    "backfill.missing_fields",
                    maximum_items=30,
                    maximum_length=200,
                )
            )
            if backfill.get("confidence") not in {"complete", "partial", "minimal"}:
                errors.append("backfill.confidence is invalid.")
            missing = backfill.get("missing_fields") if isinstance(backfill.get("missing_fields"), list) else []
            if not task.get("artifact_dir") and "task.artifact_dir" not in missing:
                errors.append("backfill.missing_fields must record empty task.artifact_dir.")
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
LOW_INFORMATION_NAMING_WORDS = {
    "bug",
    "bugs",
    "change",
    "changes",
    "cleanup",
    "fix",
    "fixes",
    "issue",
    "issues",
    "misc",
    "new",
    "task",
    "tasks",
    "todo",
    "update",
    "updates",
    "wip",
    "work",
}
VALID_BRANCH_TYPES = (
    "feat",
    "fix",
    "refactor",
    "perf",
    "test",
    "docs",
    "style",
    "build",
    "ci",
    "chore",
    "revert",
)
BRANCH_TYPE_KEYWORD_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("revert", ("revert", "rollback", "回滚")),
    ("fix", ("fix", "bug", "error", "failure", "broken", "修复", "缺陷", "错误", "失败")),
    ("docs", ("docs", "doc", "readme", "documentation", "文档", "说明")),
    ("test", ("test", "tests", "testing", "测试")),
    ("ci", ("ci", "ci/cd", "github actions", ".github/workflows", "持续集成")),
    ("build", ("build", "dependency", "dependencies", "package", "构建", "依赖")),
    ("refactor", ("refactor", "cleanup", "restructure", "重构")),
    ("perf", ("perf", "performance", "optimize", "optimization", "优化", "性能")),
    ("style", ("style", "format", "formatting", "lint", "格式")),
    ("chore", ("chore", "maintenance", "housekeeping", "维护")),
    ("feat", ("feat", "feature", "add", "support", "enable", "新增", "支持")),
)
PR_CLOSE_KEYWORDS = ["Closes", "Fixes", "Resolves", "Close", "Fix", "Resolve"]
REVIEWED_PR_BODY_SOURCE_PREFIXES = ("body-file:", "body-artifact:")
CONVENTIONAL_COMMIT_TYPES = set(VALID_BRANCH_TYPES)
CONVENTIONAL_COMMIT_SCOPE_PATTERN = r"[a-z0-9._/-]+"
CONVENTIONAL_COMMIT_SUBJECT_RE = re.compile(
    r"^(?P<type>{})\((?P<scope>{})\): #(?P<issue>\d+) (?P<description>.+)$".format(
        "|".join(sorted(CONVENTIONAL_COMMIT_TYPES)),
        CONVENTIONAL_COMMIT_SCOPE_PATTERN,
    )
)
MERGE_COMMIT_SUBJECT_RE = re.compile(
    r"^chore\(merge\): #(?P<pull_request>\d+|<pull_request>) 合并 #(?P<primary_issue>\d+) (?P<summary>.+)$"
)
CHINESE_TEXT_RE = re.compile(r"[\u4e00-\u9fff]")
WORK_COMMIT_BODY_SECTIONS = ["背景：", "变更：", "边界：", "验证："]
MERGE_COMMIT_BODY_SECTIONS = ["合并：", "范围：", "审计："]
METADATA_COMMIT_SCOPES = {"task", "trellis"}
MERGE_COMMIT_BODY_FILE_HINT = "<merge-body-file>"
DEPLOYMENT_ASSET_CATEGORIES: dict[str, list[str]] = {
    "ci_cd": [
        ".github/workflows/",
        ".github/actions/",
        ".gitlab-ci",
        "Jenkinsfile",
        "buildkite/",
        ".circleci/",
    ],
    "container": [
        "Dockerfile",
        "dockerfile",
        "docker-compose",
        "compose.",
        "container",
        "entrypoint",
        "startup",
    ],
    "kubernetes": [
        "k8s/",
        "kubernetes/",
        "deploy/",
        "deployment/",
        "kustomization.yaml",
        "kustomization.yml",
        "helm/",
        "values.yaml",
        "values.yml",
    ],
    "database": [
        "migration",
        "migrations/",
        "schema/",
        "seed",
        "seeds/",
        "backfill",
        "db/",
        "database/",
    ],
    "makefile": [
        "Makefile",
    ],
}
DEPLOYMENT_IMPACT_KEYWORDS = [
    "api",
    "service",
    "server",
    "worker",
    "background",
    "daemon",
    "cron",
    "job",
    "queue",
    "consumer",
    "cli",
    "cmd/",
    "command",
    "deploy",
    "deployment",
    "runtime",
    "entrypoint",
    "docker",
    "k8s",
    "kubernetes",
    "compose",
    "migration",
    "schema",
]


class WorkflowError(RuntimeError):
    def __init__(self, message: str, exit_code: int = 1, payload: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.exit_code = exit_code
        self.payload = payload or {}


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True, check=check)


def run_stdout(cmd: list[str], cwd: Path | None = None) -> str:
    try:
        return run(cmd, cwd=cwd).stdout.strip()
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        raise WorkflowError(f"Command failed: {shlex.join(cmd)}\n{stderr}") from exc


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise WorkflowError(f"Required tool not found on PATH: {name}")


def require_gh_auth(root: Path) -> None:
    require_tool("gh")
    proc = run(["gh", "auth", "status"], cwd=root, check=False)
    if proc.returncode != 0:
        raise WorkflowError(
            "GitHub CLI is not authenticated. Run `gh auth login` before GitHub issue intake."
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


def infer_github_repo(root: Path) -> str:
    try:
        url = run_stdout(["git", "remote", "get-url", "origin"], cwd=root)
    except WorkflowError:
        return ""
    match = re.search(r"github\.com[:/]([^/]+)/(.+?)(?:\.git)?$", url)
    if not match:
        return ""
    return f"{match.group(1)}/{match.group(2)}"


def gh_json(args: list[str], cwd: Path) -> Any:
    require_gh_auth(cwd)
    proc = run(["gh", *args], cwd=cwd, check=False)
    if proc.returncode != 0:
        raise WorkflowError(f"gh command failed: gh {shlex.join(args)}\n{proc.stderr.strip()}")
    text = proc.stdout.strip()
    return json.loads(text) if text else None


def parse_issue_ref(text: str, default_repo: str) -> tuple[str, int] | None:
    url_match = re.search(r"https://github\.com/([^/\s]+)/([^/\s]+)/issues/(\d+)", text)
    if url_match:
        return f"{url_match.group(1)}/{url_match.group(2)}", int(url_match.group(3))
    hash_match = re.search(r"(?<![\w/])#(\d+)\b", text)
    if hash_match and default_repo:
        return default_repo, int(hash_match.group(1))
    word_match = re.search(r"\bissue\s+#?(\d+)\b", text, re.IGNORECASE)
    if word_match and default_repo:
        return default_repo, int(word_match.group(1))
    return None


def clean_requirement(text: str) -> str:
    text = re.sub(r"https://github\.com/[^\s]+/issues/\d+", "", text)
    text = re.sub(r"(?<![\w/])#\d+\b", "", text)
    text = re.sub(r"\bissue\s+#?\d+\b", "", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> set[str]:
    lower = text.lower()
    tokens = set(re.findall(r"[a-z0-9][a-z0-9_-]{1,}", lower))
    cjk = "".join(re.findall(r"[\u4e00-\u9fff]", text))
    tokens.update(cjk[i : i + 2] for i in range(max(0, len(cjk) - 1)))
    return {token for token in tokens if len(token) >= 2}


def has_minimum_clarity(text: str) -> bool:
    compact = clean_requirement(text)
    if len(compact) >= 30:
        return True
    return len(tokenize(compact)) >= 4


def slugify(text: str, fallback: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    stop = {"the", "and", "for", "with", "from", "this", "that", "into", "add", "new", "issue"}
    selected = [word for word in words if word not in stop][:5]
    slug = "-".join(selected) if selected else fallback
    slug = re.sub(r"[^a-z0-9-]+", "-", slug).strip("-")
    return slug or fallback


def normalize_slug_candidate(value: str) -> str:
    raw = str(value or "").strip().lower()
    if "/" in raw:
        raw = raw.rsplit("/", 1)[1]
    normalized = re.sub(r"[^a-z0-9]+", "-", raw).strip("-")
    return re.sub(r"-+", "-", normalized)


def slug_business_tokens(value: str) -> list[str]:
    normalized = normalize_slug_candidate(value)
    tokens = re.findall(r"[a-z0-9]+", normalized)
    return [
        token
        for token in tokens
        if not token.isdigit()
        and token not in LOW_INFORMATION_NAMING_WORDS
        and len(token) >= 3
    ]


def slug_has_issue_number_prefix(slug: str, issue_number: str) -> bool:
    normalized = normalize_slug_candidate(slug)
    first = normalized.split("-", 1)[0] if normalized else ""
    if not first:
        return False
    if first == issue_number:
        return True
    if first.isdigit() and str(issue_number).isdigit():
        return int(first) == int(issue_number)
    return False


def unique_prepare_prefix(issue_number: str, issue_slug: str, short_name: str | None) -> str:
    if short_name and slug_has_issue_number_prefix(issue_slug, issue_number):
        return issue_slug
    return f"{issue_number}-{issue_slug}"


def normalized_branch_type_default(value: Any) -> str:
    branch_type = str(value or "").strip().lower()
    return branch_type if branch_type in VALID_BRANCH_TYPES else "chore"


def text_contains_branch_keyword(text: str, keyword: str) -> bool:
    if re.search(r"[\u4e00-\u9fff]", keyword):
        return keyword in text
    escaped = re.escape(keyword).replace(r"\ ", r"\s+")
    return re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", text) is not None


def generated_issue_intent_text(text: str) -> str | None:
    if "This issue body was drafted by the Guru Team Trellis intake workflow" not in text:
        return None
    prefix = text.split("## Background", 1)[0].strip()
    match = re.search(r"(?ims)^## Problem or Gap\s*(.*?)(?=^## |\Z)", text)
    problem = match.group(1).strip() if match else ""
    return "\n".join(part for part in [prefix, problem] if part)


def branch_type_catalog_line(text: str) -> bool:
    normalized = text.lower()
    catalog_markers = (
        "allowed",
        "valid",
        "supported",
        "branch type",
        "branch-type",
        "types",
        "type list",
        "合法",
        "允许",
        "支持",
        "分支类型",
        "类型",
    )
    mentioned = {
        branch_type
        for branch_type in VALID_BRANCH_TYPES
        if text_contains_branch_keyword(normalized, branch_type)
    }
    return len(mentioned) >= 4 and any(marker in normalized for marker in catalog_markers)


def sanitize_branch_type_inference_text(text: str) -> str:
    raw = str(text or "")
    generated_intent = generated_issue_intent_text(raw)
    if generated_intent is not None:
        raw = generated_intent
    raw = re.sub(r"```.*?```", "\n", raw, flags=re.DOTALL)
    raw = re.sub(r"`[^`]+`", " ", raw)
    lines = []
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped and not branch_type_catalog_line(stripped):
            lines.append(stripped)
    return "\n".join(lines)


def explicit_branch_type_marker(text: str) -> str | None:
    branch_type_alternation = "|".join(VALID_BRANCH_TYPES)
    patterns = [
        rf"(?<![a-z0-9_-])({branch_type_alternation})\s*[:：]",
        rf"\[({branch_type_alternation})\]",
        rf"\btype\s*[:=：]\s*({branch_type_alternation})\b",
        rf"\bbranch[\s_-]*type\s*[:=：]\s*({branch_type_alternation})\b",
        rf"\bbranch[\s_-]*type\s+(?:is\s+)?({branch_type_alternation})\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).lower()
    return None


def infer_branch_type(text: str, default_branch_type: Any = "chore") -> str:
    default = normalized_branch_type_default(default_branch_type)
    normalized_text = re.sub(
        r"\s+",
        " ",
        sanitize_branch_type_inference_text(str(text or "")).lower(),
    ).strip()
    if not normalized_text:
        return default
    explicit = explicit_branch_type_marker(normalized_text)
    if explicit:
        return explicit
    for branch_type, keywords in BRANCH_TYPE_KEYWORD_RULES:
        if any(text_contains_branch_keyword(normalized_text, keyword) for keyword in keywords):
            return branch_type
    return default


def assess_slug_candidate(value: str) -> dict[str, Any]:
    normalized = normalize_slug_candidate(value)
    business_tokens = slug_business_tokens(normalized)
    if not normalized:
        reason = "name is empty after ASCII slug normalization"
    elif re.fullmatch(r"\d+", normalized):
        reason = "name contains only an issue number"
    elif re.fullmatch(r"issue-\d+", normalized):
        reason = "name only repeats issue and its number"
    elif re.fullmatch(r"\d+-issue-\d+", normalized):
        reason = "name only repeats issue and its number"
    elif not business_tokens:
        reason = "name contains only generic words or numbers"
    elif len(normalized) < 8:
        reason = "name is too short"
    elif len(business_tokens) < 2:
        reason = "name needs at least two business tokens"
    else:
        reason = "ok"
    return {
        "ok": reason == "ok",
        "slug": normalized,
        "reason": reason,
        "business_tokens": business_tokens,
    }


def naming_override_flags(issue_number: str, branch_type: str) -> list[str]:
    prefix = issue_number.zfill(3) if issue_number.isdigit() else "NNN"
    suggested_slug = f"{prefix}-semantic-business-name"
    suggested_branch_type = normalized_branch_type_default(branch_type)
    return [
        f"--short-name {suggested_slug}",
        f"--workspace-slug {suggested_slug}",
        f"--branch {suggested_branch_type}/{suggested_slug}",
        f"--task-slug {suggested_slug}",
    ]


def evaluate_naming_quality(
    *,
    issue_number: str,
    source_text: str,
    slug: str,
    task_slug: str,
    workspace_slug: str,
    branch_name: str,
    branch_type: str,
    semantic_override_provided: bool,
) -> dict[str, Any]:
    checked_names = {
        "slug": assess_slug_candidate(slug),
        "task_slug": assess_slug_candidate(task_slug),
        "workspace_slug": assess_slug_candidate(workspace_slug),
        "branch_name": assess_slug_candidate(branch_name),
    }
    failures = {name: detail for name, detail in checked_names.items() if not detail["ok"]}
    source_has_non_ascii = any(ord(ch) > 127 for ch in source_text)
    if failures:
        first_name, first_failure = next(iter(failures.items()))
        detail = "; ".join(
            f"{name}={failure['slug'] or '<empty>'} ({failure['reason']})"
            for name, failure in failures.items()
        )
        reason = f"low-information prepare-task naming: {detail}"
        if source_has_non_ascii:
            reason += "; source title contains non-ASCII text, provide semantic English naming overrides instead of transliteration"
        else:
            reason += "; provide semantic English naming overrides"
        return {
            "ok": False,
            "reason": reason,
            "requires_semantic_name": True,
            "current_slug": first_failure["slug"],
            "current_surface": first_name,
            "suggested_override_flags": naming_override_flags(issue_number, branch_type),
            "checked_names": checked_names,
        }
    if source_has_non_ascii and not semantic_override_provided:
        reason = (
            "source title contains non-ASCII text; provide semantic English naming overrides "
            "instead of relying on transliteration or partial ASCII extraction"
        )
        return {
            "ok": False,
            "reason": reason,
            "requires_semantic_name": True,
            "current_slug": checked_names["workspace_slug"]["slug"],
            "current_surface": "workspace_slug",
            "suggested_override_flags": naming_override_flags(issue_number, branch_type),
            "checked_names": checked_names,
        }
    return {
        "ok": True,
        "reason": "naming includes enough business tokens",
        "requires_semantic_name": False,
        "current_slug": checked_names["workspace_slug"]["slug"],
        "current_surface": "workspace_slug",
        "suggested_override_flags": [],
        "checked_names": checked_names,
    }


def prepare_naming_payload(
    args: argparse.Namespace,
    config: dict[str, Any],
    issue_number: str,
    source_text: str,
    branch_type_source_text: str | None = None,
) -> dict[str, Any]:
    branch_type = infer_branch_type(
        branch_type_source_text if branch_type_source_text is not None else source_text,
        config.get("branch_type_default", DEFAULTS["branch_type_default"]),
    )
    if args.short_name:
        issue_slug = normalize_slug_candidate(args.short_name) or f"issue-{issue_number}"
    else:
        issue_slug = slugify(source_text, f"issue-{issue_number}")
    unique_prefix = unique_prepare_prefix(issue_number, issue_slug, args.short_name)
    task_slug = args.task_slug or unique_prefix
    workspace_slug = args.workspace_slug or unique_prefix
    branch_name = args.branch or f"{branch_type}/{unique_prefix}"
    semantic_override_provided = bool(
        args.short_name
        or (args.workspace_slug and args.task_slug and args.branch)
    )
    naming_quality = evaluate_naming_quality(
        issue_number=issue_number,
        source_text=source_text,
        slug=issue_slug,
        task_slug=task_slug,
        workspace_slug=workspace_slug,
        branch_name=branch_name,
        branch_type=branch_type,
        semantic_override_provided=semantic_override_provided,
    )
    return {
        "slug": issue_slug,
        "task_slug": task_slug,
        "workspace_slug": workspace_slug,
        "branch_name": branch_name,
        "naming_quality": naming_quality,
    }


def ensure_naming_quality_for_create(payload: dict[str, Any]) -> None:
    naming_quality = payload.get("naming_quality")
    if isinstance(naming_quality, dict) and naming_quality.get("ok") is True:
        return
    raise WorkflowError(
        "Low-information prepare-task naming blocked before create. Provide semantic English overrides with --short-name/--workspace-slug/--branch/--task-slug.",
        exit_code=2,
        payload=payload,
    )


def make_issue_title(requirement: str, short_name: str | None = None) -> str:
    text = clean_requirement(requirement)
    first = re.split(r"[。\n.!?]", text, maxsplit=1)[0].strip()
    if first:
        return first[:90]
    if short_name:
        return short_name.replace("-", " ").title()
    return "Trellis intake"


def issue_body(requirement: str, duplicates: list[dict[str, Any]]) -> str:
    duplicate_lines = "\n".join(
        f"- #{candidate['number']} {candidate['title']} ({candidate['similarity']}): {candidate['url']}"
        for candidate in duplicates
    )
    if not duplicate_lines:
        duplicate_lines = "- 创建前未发现阻塞级重复 issue。"
    return f"""## Background

This issue body was drafted by the Guru Team Trellis intake workflow because the user request did not provide an existing source issue.

## Current State

The request has not yet been converted into Trellis planning artifacts.

## Problem or Gap

{clean_requirement(requirement)}

## Requirement Change

The Trellis task `prd.md` should turn this intake into testable requirements and acceptance criteria.

## Design or Implementation Handoff

Use this issue as the discussion and intake record. Trellis task artifacts become the execution source of truth after planning.

## Out of Scope

Clarify during Trellis planning if the request is broader than the next task.

## Open Questions

Clarify during Trellis planning.

## Duplicate Issue Search

{duplicate_lines}

## Trellis Handoff

The workflow will record the Trellis task path, branch, base branch, and workspace path in the task artifacts or follow-up comments when the task is created.
"""


def confirmed_issue_prepare_command(
    args: argparse.Namespace,
    title: str,
    requirement: str,
    force_new: bool | None = None,
) -> list[str]:
    cmd = [
        "python3",
        "./.trellis/guru-team/scripts/python/guru_team_trellis.py",
        "prepare",
        "--json",
        "--create-issue-confirmed",
        "--issue-title",
        title,
        "--issue-body-file",
        "<reviewed-issue-body.md>",
    ]
    option_map = [
        ("short_name", "--short-name"),
        ("base_branch", "--base-branch"),
        ("branch", "--branch"),
        ("task_slug", "--task-slug"),
        ("workspace_slug", "--workspace-slug"),
        ("title", "--title"),
        ("assignee", "--assignee"),
        ("priority", "--priority"),
        ("description", "--description"),
    ]
    for attr, option in option_map:
        value = getattr(args, attr, None)
        if value:
            cmd.extend([option, str(value)])
    should_force_new = getattr(args, "force_new", False) if force_new is None else force_new
    if should_force_new:
        cmd.append("--force-new")
    if getattr(args, "worktree", False):
        cmd.append("--worktree")
    cmd.append(requirement)
    return cmd


def issue_view(repo: str, number: int, root: Path) -> dict[str, Any]:
    return gh_json(
        [
            "issue",
            "view",
            str(number),
            "--repo",
            repo,
            "--json",
            "number,title,url,body,comments,state",
        ],
        cwd=root,
    )


def score_duplicate(requirement: str, issue: dict[str, Any]) -> tuple[float, str]:
    req_tokens = tokenize(requirement)
    issue_text = f"{issue.get('title', '')}\n{issue.get('body', '')}"
    issue_tokens = tokenize(issue_text)
    if not req_tokens or not issue_tokens:
        return 0.0, "No comparable keywords"
    overlap = req_tokens & issue_tokens
    score = len(overlap) / max(1, len(req_tokens))
    title = issue.get("title", "").lower()
    reason = "keyword overlap: " + ", ".join(sorted(overlap)[:8]) if overlap else "weak keyword overlap"
    phrase = clean_requirement(requirement).lower()[:30]
    if phrase and phrase in title:
        score = max(score, 0.75)
        reason = "title contains the requirement phrase"
    return score, reason


def duplicate_search(repo: str, requirement: str, root: Path, limit: int) -> list[dict[str, Any]]:
    issues = gh_json(
        [
            "issue",
            "list",
            "--repo",
            repo,
            "--state",
            "open",
            "--limit",
            "50",
            "--json",
            "number,title,body,url,labels,updatedAt",
        ],
        cwd=root,
    ) or []
    candidates: list[dict[str, Any]] = []
    for issue in issues:
        score, reason = score_duplicate(requirement, issue)
        if score >= 0.18:
            similarity = "high" if score >= 0.45 else "medium" if score >= 0.25 else "low"
            candidates.append(
                {
                    "number": issue["number"],
                    "title": issue.get("title", ""),
                    "url": issue.get("url", ""),
                    "score": round(score, 3),
                    "similarity": similarity,
                    "reason": reason,
                }
            )
    candidates.sort(key=lambda item: item["score"], reverse=True)
    return candidates[:limit]


def create_issue(repo: str, title: str, body: str, root: Path, labels: list[str]) -> dict[str, Any]:
    title = title.strip()
    body = body.strip()
    if not title:
        raise WorkflowError("Confirmed issue creation requires a non-empty issue title.")
    if not body:
        raise WorkflowError("Confirmed issue creation requires a non-empty issue body.")
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        tmp.write(body + "\n")
        tmp_path = tmp.name
    try:
        cmd = ["issue", "create", "--repo", repo, "--title", title, "--body-file", tmp_path]
        for label in labels:
            if label:
                cmd.extend(["--label", str(label)])
        require_gh_auth(root)
        proc = run(["gh", *cmd], cwd=root, check=False)
        if proc.returncode != 0:
            raise WorkflowError(f"gh issue create failed:\n{proc.stderr.strip()}")
        url = proc.stdout.strip()
    finally:
        Path(tmp_path).unlink(missing_ok=True)
    match = re.search(r"/issues/(\d+)", url)
    if not match:
        raise WorkflowError(f"Could not parse created issue number from URL: {url}")
    return issue_view(repo, int(match.group(1)), root)


def read_confirmed_issue_body(path_value: str | None) -> str:
    if not path_value:
        raise WorkflowError(
            "--create-issue-confirmed requires --issue-body-file containing the AI/human reviewed issue body.",
            exit_code=2,
        )
    path = Path(path_value)
    if not path.exists():
        raise WorkflowError(f"Confirmed issue body file not found: {path}")
    body = path.read_text(encoding="utf-8").strip()
    if not body:
        raise WorkflowError(f"Confirmed issue body file is empty: {path}")
    return body


def git_branch_exists(root: Path, ref: str) -> bool:
    return run(["git", "rev-parse", "--verify", "--quiet", ref], cwd=root, check=False).returncode == 0


def local_branch_exists(root: Path, branch: str) -> bool:
    return git_branch_exists(root, f"refs/heads/{branch}")


def ref_head(root: Path, ref: str) -> str | None:
    proc = run(["git", "rev-parse", "--verify", "--quiet", ref], cwd=root, check=False)
    value = proc.stdout.strip()
    if proc.returncode == 0 and value:
        return value
    return None


def base_short_name(base_ref: str) -> str:
    normalized = normalize_ref(base_ref)
    return normalized.split("/", 1)[1] if normalized.startswith("origin/") else normalized


def inspect_base_freshness(root: Path, base_ref: str, remote: str = "origin") -> dict[str, Any]:
    base = base_short_name(base_ref)
    local_head = ref_head(root, base)
    remote_ref = f"{remote}/{base}"
    remote_head = ref_head(root, remote_ref)
    fresh = bool(remote_head and local_head == remote_head)
    if remote_head and not local_head:
        fresh = True
    status = "fresh" if fresh else "unknown"
    if remote_head and local_head and local_head != remote_head:
        status = "stale"
    if not remote_head:
        status = "remote_ref_missing"
    return {
        "remote": remote,
        "base_branch": base,
        "base_ref": base_ref,
        "remote_ref": remote_ref,
        "local_head_before": local_head,
        "local_head_after": local_head,
        "remote_head": remote_head,
        "fetch_performed": False,
        "fast_forwarded": False,
        "fresh": fresh,
        "status": status,
        "base_ref_for_worktree": remote_ref if remote_head else base_ref,
    }


def refresh_base_freshness_for_planner(root: Path, base_ref: str, remote: str = "origin") -> dict[str, Any]:
    base = base_short_name(base_ref)
    remote_ref = f"{remote}/{base}"
    local_head_before = ref_head(root, base)
    fetch_proc = run(["git", "fetch", remote, base], cwd=root, check=False)
    if fetch_proc.returncode != 0:
        local_head_after = ref_head(root, base)
        return {
            "remote": remote,
            "base_branch": base,
            "base_ref": base_ref,
            "remote_ref": remote_ref,
            "local_head_before": local_head_before,
            "local_head_after": local_head_after,
            "remote_head": None,
            "remote_head_source": "unconfirmed",
            "fetch_attempted": True,
            "fetch_performed": False,
            "fast_forwarded": False,
            "fresh": False,
            "status": "fetch_failed",
            "fetch_error": fetch_proc.stderr.strip(),
            "base_ref_for_worktree": base_ref,
        }

    remote_head = ref_head(root, remote_ref)
    local_head_after = ref_head(root, base)
    fresh = False
    status = "remote_ref_missing"
    base_ref_for_worktree = base_ref
    if remote_head:
        if not local_head_after:
            fresh = True
            status = "remote_only"
            base_ref_for_worktree = remote_ref
        elif local_head_after == remote_head:
            fresh = True
            status = "fresh"
            base_ref_for_worktree = base
        elif is_ancestor(root, local_head_after, remote_ref):
            status = "stale"
            base_ref_for_worktree = remote_ref
        else:
            status = "diverged"
            base_ref_for_worktree = remote_ref

    return {
        "remote": remote,
        "base_branch": base,
        "base_ref": base_ref,
        "remote_ref": remote_ref,
        "local_head_before": local_head_before,
        "local_head_after": local_head_after,
        "remote_head": remote_head,
        "remote_head_source": "fetched" if remote_head else "missing",
        "fetch_attempted": True,
        "fetch_performed": True,
        "fast_forwarded": False,
        "fresh": fresh,
        "status": status,
        "base_ref_for_worktree": base_ref_for_worktree,
    }


def ensure_base_freshness(root: Path, base_ref: str, remote: str = "origin") -> dict[str, Any]:
    base = base_short_name(base_ref)
    remote_ref = f"{remote}/{base}"
    local_head_before = ref_head(root, base)
    fetch_proc = run(["git", "fetch", remote, base], cwd=root, check=False)
    if fetch_proc.returncode != 0:
        raise WorkflowError(
            f"Could not refresh base branch before worktree creation: git fetch {remote} {base}\n{fetch_proc.stderr.strip()}",
            exit_code=2,
        )
    remote_head = ref_head(root, remote_ref)
    if not remote_head:
        raise WorkflowError(
            f"Remote base ref not found after fetch: {remote_ref}",
            exit_code=2,
            payload={"remote": remote, "base_branch": base, "remote_ref": remote_ref},
        )

    fast_forwarded = False
    if local_head_before:
        if local_head_before == remote_head:
            pass
        elif is_ancestor(root, local_head_before, remote_ref):
            if current_branch(root) == base:
                if git_dirty(root):
                    raise WorkflowError(
                        f"Base branch {base} is behind {remote_ref}, but the checkout is dirty and cannot be fast-forwarded safely.",
                        exit_code=2,
                    )
                run_stdout(["git", "merge", "--ff-only", remote_ref], cwd=root)
            else:
                run_stdout(["git", "branch", "-f", base, remote_ref], cwd=root)
            fast_forwarded = True
        else:
            raise WorkflowError(
                f"Local base branch {base} diverged from {remote_ref}; cannot create task worktree from stale base.",
                exit_code=2,
                payload={
                    "base_branch": base,
                    "local_head": local_head_before,
                    "remote_head": remote_head,
                    "remote_ref": remote_ref,
                },
            )

    local_head_after = ref_head(root, base)
    fresh = local_head_after == remote_head if local_head_after else True
    status = "fresh" if local_head_after and fresh else "remote_only"
    return {
        "remote": remote,
        "base_branch": base,
        "base_ref": base_ref,
        "remote_ref": remote_ref,
        "local_head_before": local_head_before,
        "local_head_after": local_head_after,
        "remote_head": remote_head,
        "fetch_performed": True,
        "fast_forwarded": fast_forwarded,
        "fresh": fresh,
        "status": status,
        "base_ref_for_worktree": base if fresh and local_head_after else remote_ref,
    }


def resolve_base_branch(root: Path, config: dict[str, Any], explicit: str | None = None) -> tuple[str, list[str]]:
    candidates = [explicit] if explicit else list(config.get("base_branch_candidates") or DEFAULTS["base_branch_candidates"])
    discovered: list[str] = []
    for candidate in candidates:
        if not candidate:
            continue
        candidate = str(candidate)
        refs = [candidate, f"origin/{candidate}"] if not candidate.startswith("origin/") else [candidate]
        for ref in refs:
            if git_branch_exists(root, ref):
                discovered.append(ref)
    if discovered:
        return discovered[0], discovered
    current = current_branch(root)
    return current, [current]


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


def git_dirty(root: Path) -> bool:
    return bool(run(["git", "status", "--porcelain"], cwd=root, check=False).stdout.strip())


def git_status_paths(root: Path) -> list[str]:
    lines = run(["git", "status", "--porcelain"], cwd=root, check=False).stdout.splitlines()
    paths: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path:
            paths.append(path)
    return paths


def has_non_metadata_dirty_paths(root: Path) -> tuple[bool, list[str]]:
    paths = git_status_paths(root)
    non_metadata = [
        path
        for path in paths
        if not path.startswith(METADATA_ONLY_PREFIXES) and path not in METADATA_ONLY_FILES
    ]
    return bool(non_metadata), non_metadata


def committed_paths_match_phase2_dirty_paths(
    root: Path,
    recorded_head: str,
    recorded_dirty_paths: list[Any],
) -> tuple[bool, list[str]]:
    proc = run(["git", "diff", "--name-only", f"{recorded_head}..HEAD"], cwd=root, check=False)
    if proc.returncode != 0:
        return False, []
    files = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    uncovered = [
        path
        for path in files
        if not path.startswith(METADATA_ONLY_PREFIXES)
        and path not in METADATA_ONLY_FILES
        and not committed_path_covered_by_phase2_dirty_path(path, recorded_dirty_paths)
    ]
    return not uncovered, uncovered


def committed_path_covered_by_phase2_dirty_path(
    committed_path: str,
    recorded_dirty_paths: list[Any],
) -> bool:
    committed = committed_path.strip().rstrip("/")
    if not committed:
        return False
    for item in recorded_dirty_paths:
        raw = str(item).strip()
        if not raw:
            continue
        dirty = raw.rstrip("/")
        if committed == dirty:
            return True
        if raw.endswith("/") and committed.startswith(f"{dirty}/"):
            return True
    return False


def stage_metadata_paths(root: Path) -> list[str]:
    metadata_paths = [
        path
        for path in git_status_paths(root)
        if path.startswith(METADATA_ONLY_PREFIXES) or path in METADATA_ONLY_FILES
    ]
    if metadata_paths:
        run_stdout(["git", "add", "--", *metadata_paths], cwd=root)
    return metadata_paths


def commit_if_metadata_dirty(root: Path, message: str) -> dict[str, Any]:
    dirty, dirty_paths = has_non_metadata_dirty_paths(root)
    if dirty:
        raise WorkflowError(
            "finish-work produced uncommitted non-metadata changes. Return to continue/review before publish.",
            exit_code=2,
            payload={"dirty_paths": dirty_paths},
        )
    metadata_paths = stage_metadata_paths(root)
    if not metadata_paths:
        return {"committed": False, "paths": []}
    if run(["git", "diff", "--cached", "--quiet"], cwd=root, check=False).returncode == 0:
        return {"committed": False, "paths": metadata_paths}
    run_stdout(["git", "commit", "-m", message], cwd=root)
    return {"committed": True, "paths": metadata_paths, "commit": current_head(root)}


def recent_work_commits(root: Path, reviewed_head: str, max_count: int = 5) -> list[str]:
    proc = run(["git", "log", "--format=%H", f"{reviewed_head}^..{reviewed_head}"], cwd=root, check=False)
    if proc.returncode == 0:
        commits = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
        if commits:
            return commits[:max_count]
    return [reviewed_head] if reviewed_head else []


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


def diff_range(root: Path, base_branch: str) -> str:
    return f"{diff_base_ref(root, base_branch)}...HEAD"


def changed_files(root: Path, diff_spec: str) -> list[str]:
    proc = run(["git", "diff", "--name-only", diff_spec], cwd=root, check=False)
    if proc.returncode != 0:
        raise WorkflowError(f"Could not compute diff for {diff_spec}:\n{proc.stderr.strip()}")
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def file_matches_marker(path: str, marker: str) -> bool:
    lowered = path.lower()
    marker_lower = marker.lower()
    name = Path(path).name
    if marker.endswith("/"):
        return lowered.startswith(marker_lower) or f"/{marker_lower}" in lowered
    if marker_lower in {"makefile", "dockerfile", "jenkinsfile"}:
        return name.lower() == marker_lower or name.lower().startswith(f"{marker_lower}.")
    return marker_lower in lowered


def classify_changed_files(files: list[str]) -> dict[str, list[str]]:
    categories: dict[str, list[str]] = {key: [] for key in DEPLOYMENT_ASSET_CATEGORIES}
    categories.update(
        {
            "docs": [],
            "tests": [],
            "trellis_artifacts": [],
            "config": [],
            "scripts": [],
            "schemas": [],
            "code": [],
            "other": [],
        }
    )
    for path in files:
        matched = False
        lowered = path.lower()
        for category, markers in DEPLOYMENT_ASSET_CATEGORIES.items():
            if any(file_matches_marker(path, marker) for marker in markers):
                categories[category].append(path)
                matched = True
        if path.startswith(".trellis/") or "/.trellis/" in path or path.startswith("trellis/"):
            categories["trellis_artifacts"].append(path)
            matched = True
        if lowered.endswith((".md", ".mdx", ".rst", ".txt")) or lowered.startswith("docs/"):
            categories["docs"].append(path)
            matched = True
        if any(part in lowered for part in ["/test", "/tests/", "_test.", ".spec.", ".test."]):
            categories["tests"].append(path)
            matched = True
        if lowered.endswith((".json", ".yaml", ".yml", ".toml", ".ini", ".conf", ".cfg", ".properties")):
            categories["config"].append(path)
            matched = True
        if lowered.endswith((".sh", ".bash", ".zsh", ".py", ".rb", ".pl")) and (
            "/script" in lowered or lowered.startswith("scripts/") or "/bin/" in lowered
        ):
            categories["scripts"].append(path)
            matched = True
        if "schema" in lowered or lowered.endswith(".schema.json"):
            categories["schemas"].append(path)
            matched = True
        if lowered.endswith(
            (
                ".go",
                ".py",
                ".ts",
                ".tsx",
                ".js",
                ".jsx",
                ".java",
                ".kt",
                ".rs",
                ".rb",
                ".php",
                ".cs",
                ".cpp",
                ".c",
                ".h",
                ".sql",
            )
        ):
            categories["code"].append(path)
            matched = True
        if not matched:
            categories["other"].append(path)
    return {key: sorted(set(value)) for key, value in categories.items() if value}


def detect_deployment_impact(files: list[str]) -> dict[str, Any]:
    changed_categories = classify_changed_files(files)
    deployment_categories = {
        key: changed_categories[key]
        for key in DEPLOYMENT_ASSET_CATEGORIES
        if key in changed_categories
    }
    changed_deployment_assets = sorted(
        {path for paths in deployment_categories.values() for path in paths}
    )
    probable_runtime_changes = sorted(
        {
            path
            for path in files
            if any(keyword in path.lower() for keyword in DEPLOYMENT_IMPACT_KEYWORDS)
            and path not in changed_deployment_assets
        }
    )
    needs_deployment_review = bool(changed_deployment_assets or probable_runtime_changes)
    return {
        "changed_file_categories": changed_categories,
        "deployment_asset_categories": deployment_categories,
        "changed_deployment_assets": changed_deployment_assets,
        "probable_runtime_changes_without_deployment_asset_change": probable_runtime_changes,
        "needs_deployment_impact_review": needs_deployment_review,
        "review_instruction": (
            "当本次 diff 改变部署资产，或业务/API/CLI/worker/runtime 形态可能变化但部署资产未改时，"
            "review evidence 必须说明 CI/CD、容器、Compose、K8s/Kustomize、migration、Makefile 是否需要同步调整；"
            "如果不需要，必须给出不需要的理由。"
        ),
    }


def evidence_mentions_category(evidence: list[str], category: str) -> bool:
    text = "\n".join(evidence).lower()
    aliases = {
        "ci_cd": ["ci", "cd", "github actions", ".github/workflows", "workflow", "发布自动化"],
        "container": ["docker", "compose", "container", "容器", "entrypoint", "startup"],
        "kubernetes": ["k8s", "kubernetes", "kustomize", "helm", "yaml", "部署"],
        "database": ["migration", "schema", "seed", "backfill", "数据库", "迁移"],
        "makefile": ["makefile", "make "],
        "runtime_impact": [
            "部署",
            "runtime",
            "运行",
            "api",
            "cli",
            "worker",
            "服务",
            "后台",
            "ci",
            "cd",
            "docker",
            "compose",
            "k8s",
            "kubernetes",
            "kustomize",
            "migration",
            "makefile",
        ],
    }
    return any(alias in text for alias in aliases.get(category, [category]))


def deployment_evidence_errors(impact: dict[str, Any], evidence: list[str], findings: list[dict[str, Any]]) -> list[str]:
    if review_gate_blocking_findings(findings):
        return []
    errors: list[str] = []
    if not evidence_mentions_category(evidence, "runtime_impact"):
        errors.append("Gate evidence 未说明本次变更的部署影响，或未说明 Docker/Compose/CI/CD/K8s/migration/Makefile 是否需要同步调整。")
    if not impact.get("needs_deployment_impact_review"):
        return errors
    deployment_categories = impact.get("deployment_asset_categories")
    if isinstance(deployment_categories, dict):
        for category, paths in deployment_categories.items():
            if paths and not evidence_mentions_category(evidence, category):
                errors.append(f"Gate evidence 未点名已变更的部署资产类别 {category}。")
    runtime_changes = impact.get("probable_runtime_changes_without_deployment_asset_change")
    if isinstance(runtime_changes, list) and runtime_changes and not evidence_mentions_category(evidence, "runtime_impact"):
        errors.append("本次 diff 可能改变 API/CLI/worker/runtime 形态，但 evidence 未说明部署资产是否需要同步调整。")
    return errors


def is_ancestor(root: Path, ancestor: str, descendant: str = "HEAD") -> bool:
    return run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=root, check=False).returncode == 0


def worktree_lines(root: Path) -> list[str]:
    proc = run(["git", "worktree", "list"], cwd=root, check=False)
    return [line for line in proc.stdout.splitlines() if line.strip()]


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


def default_worktree_root(root: Path) -> Path:
    return root.parent / f"{root.name}-worktrees"


def configured_worktree_root(root: Path, config: dict[str, Any]) -> Path:
    configured = str(config.get("worktree_root") or "").strip()
    if not configured:
        return default_worktree_root(root)
    path = Path(configured)
    return path if path.is_absolute() else (root / path).resolve()


def prepare_workspace(
    root: Path,
    config: dict[str, Any],
    branch_name: str,
    workspace_slug: str,
    base_ref: str,
    force_worktree: bool,
    create_worktree: bool,
) -> tuple[str, Path, bool]:
    require_tool("git")
    mode = str(config.get("workspace_mode") or "worktree")
    if force_worktree:
        mode = "worktree"
    if mode not in {"worktree", "current"}:
        raise WorkflowError(f"Unsupported workspace_mode: {mode}")

    if mode == "current":
        return mode, root, True

    worktree_root = configured_worktree_root(root, config)
    workspace_path = worktree_root / workspace_slug
    if workspace_path.exists():
        if not (workspace_path / ".git").exists():
            raise WorkflowError(f"Workspace path exists but is not a git worktree: {workspace_path}")
        return mode, workspace_path, True

    if not create_worktree:
        return mode, workspace_path, False

    workspace_path.parent.mkdir(parents=True, exist_ok=True)
    if local_branch_exists(root, branch_name):
        run_stdout(["git", "worktree", "add", str(workspace_path), branch_name], cwd=root)
    else:
        run_stdout(["git", "worktree", "add", "-b", branch_name, str(workspace_path), base_ref], cwd=root)
    return mode, workspace_path, True


def developer_identity_path(root: Path) -> Path:
    return root / ".trellis/.developer"


def parse_developer_identity(content: str) -> dict[str, str]:
    identity: dict[str, str] = {}
    for raw in content.splitlines():
        line = raw.strip()
        if not line:
            continue
        if "=" not in line:
            identity.setdefault("name", line)
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key:
            identity[key] = value
    return identity


def read_developer_identity(root: Path) -> dict[str, str] | None:
    path = developer_identity_path(root)
    if not path.exists():
        return None
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return None
    return parse_developer_identity(content)


def developer_name_from_identity(identity: dict[str, str] | None) -> str | None:
    if not identity:
        return None
    value = str(identity.get("name") or "").strip()
    return value or None


def write_developer_identity(path: Path, name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"name={name}\ninitialized_at={now_iso()}\n"
    path.write_text(content, encoding="utf-8")


def ensure_workspace_developer_identity(source_root: Path, workspace_path: Path, assignee: str | None = None) -> dict[str, Any]:
    source_identity_path = developer_identity_path(source_root)
    workspace_identity_path = developer_identity_path(workspace_path)
    if workspace_identity_path.exists():
        workspace_identity = read_developer_identity(workspace_path)
        return {
            "status": "exists",
            "source": "workspace",
            "path": str(workspace_identity_path),
            "developer": developer_name_from_identity(workspace_identity),
        }

    if source_identity_path.exists():
        workspace_identity_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_identity_path, workspace_identity_path)
        workspace_identity = read_developer_identity(workspace_path)
        return {
            "status": "copied",
            "source": str(source_identity_path),
            "path": str(workspace_identity_path),
            "developer": developer_name_from_identity(workspace_identity),
        }

    normalized_assignee = str(assignee or "").strip()
    if normalized_assignee:
        write_developer_identity(workspace_identity_path, normalized_assignee)
        return {
            "status": "initialized",
            "source": "--assignee",
            "path": str(workspace_identity_path),
            "developer": normalized_assignee,
        }

    recovery_command = "python3 ./.trellis/scripts/init_developer.py <name>"
    raise WorkflowError(
        "Trellis developer identity is missing. Initialize the source checkout before creating a task worktree.",
        exit_code=2,
        payload={
            "missing_identity": True,
            "source_identity_path": str(source_identity_path),
            "workspace_identity_path": str(workspace_identity_path),
            "recovery_command": recovery_command,
        },
    )


def task_start_context_path(task_dir: Path, config: dict[str, Any]) -> Path:
    return task_dir / str(config.get("task_start_context_artifact") or DEFAULTS["task_start_context_artifact"])


def runtime_root(root: Path, config: dict[str, Any]) -> Path:
    rel = Path(str(config.get("runtime_root") or DEFAULTS["runtime_root"]))
    return rel if rel.is_absolute() else root / rel


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
        and (Path(record["worktree"]) / task_dir / "task-start-context.json").is_file()
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
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        tmp_path.replace(path)
    finally:
        tmp_path.unlink(missing_ok=True)


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


def guru_team_extension_payload(root: Path) -> dict[str, Any]:
    path = root / GURU_TEAM_EXTENSION_MANIFEST
    payload, error = read_optional_json(path)
    if payload is None:
        status = "missing" if error == "missing" else "invalid"
        result: dict[str, Any] = {
            "status": status,
            "path": GURU_TEAM_EXTENSION_MANIFEST.as_posix(),
        }
        if error and error != "missing":
            result["error"] = error
        return result

    extension = payload.get("extension") if isinstance(payload.get("extension"), dict) else {}
    source = payload.get("source") if isinstance(payload.get("source"), dict) else {}
    install = payload.get("install") if isinstance(payload.get("install"), dict) else {}
    requires = extension.get("requires") if isinstance(extension.get("requires"), dict) else {}
    tested = extension.get("tested") if isinstance(extension.get("tested"), dict) else {}
    return {
        "status": "ok",
        "path": GURU_TEAM_EXTENSION_MANIFEST.as_posix(),
        "schema_version": payload.get("schema_version"),
        "extension_id": extension.get("extension_id"),
        "version": extension.get("version"),
        "workflow_template_id": extension.get("workflow_template_id"),
        "target_trellis_cli": extension.get("target_trellis_cli"),
        "trellis_cli_compatibility": requires.get("trellis_cli"),
        "tested_trellis_cli": tested.get("trellis_cli") if isinstance(tested.get("trellis_cli"), list) else [],
        "installed_at": payload.get("installed_at"),
        "source_repo": source.get("repo"),
        "source_ref": source.get("ref"),
        "source_commit": source.get("commit"),
        "source_tree_state": source.get("tree_state"),
        "source_is_mutable_ref": source.get("is_mutable_ref"),
        "selected_platforms": install.get("selected_platforms") if isinstance(install.get("selected_platforms"), list) else [],
        "all_platforms": install.get("all_platforms"),
    }


def load_task_start_context(task_dir: Path, config: dict[str, Any]) -> dict[str, Any]:
    path = task_start_context_path(task_dir, config)
    if not path.exists():
        return {}
    payload = read_json(path)
    validate_task_start_context(payload)
    payload.setdefault("_path", str(path))
    payload.setdefault("task_dir", payload.get("task_artifact_dir"))
    payload.setdefault("issue_scope_ledger", payload.get("issue_scope_ledger_seed") or {})
    return payload


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


def resolve_task_dir(root: Path, task_arg: str | None, context: dict[str, Any] | None = None) -> Path:
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


def resolve_human_markdown_artifacts(root: Path, task_dir: Path) -> dict[str, Any]:
    task_relative = repo_relative(root, task_dir)
    archived = task_relative.startswith(".trellis/tasks/archive/")
    artifacts: list[dict[str, Any]] = []
    for spec in HUMAN_MARKDOWN_ARTIFACTS:
        filename = str(spec["filename"])
        path = task_dir / filename
        exists = path.is_file()
        artifacts.append(
            {
                "label": spec["label"],
                "filename": filename,
                "purpose": spec["purpose"],
                "exists": exists,
                "status": "已生成" if exists else spec["missing_status"],
                "path": repo_relative(root, path),
                "absolute_path": str(path.resolve()),
                "link": str(path.resolve()) if exists else "",
            }
        )
    return {
        "status": "ok",
        "task_dir": str(task_dir.resolve()),
        "task_dir_relative": task_relative,
        "archived": archived,
        "markdown_artifacts": artifacts,
    }


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
        errors.append("workspace boundary 缺少 task-start-context.json，无法确认 task-local portable context。")
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


def issue_entry(number: Any, url: str = "", title: str = "", reason: str = "", evidence: list[str] | None = None) -> dict[str, Any]:
    try:
        parsed_number = int(number)
    except (TypeError, ValueError):
        parsed_number = number
    return {
        "number": parsed_number,
        "url": url,
        "title": title,
        "reason": reason,
        "acceptance_evidence": evidence or [],
    }


def default_issue_scope_ledger(task_context: dict[str, Any]) -> dict[str, Any]:
    source = task_context.get("source_issue") if isinstance(task_context.get("source_issue"), dict) else {}
    primary = issue_entry(
        source.get("number"),
        str(source.get("url") or ""),
        str(source.get("title") or ""),
        "intake 主 issue，默认进入 close 候选；publish 前必须补齐验收证据。",
    )
    return {
        "schema_version": "1.0",
        "primary_issue": primary,
        "close_issues": [primary] if primary.get("number") is not None else [],
        "related_issues": [],
        "followup_issues": [],
        "rules": [
            "close_issues 只放当前 task 明确承诺完整解决且 review gate 已验证的 issue。",
            "related_issues 只能生成 Refs/Related 语义，不能自动关闭。",
            "followup_issues 表示新范围或后续任务，不能自动关闭。",
            "新增 issue 进入 close_issues 前必须更新 prd/design/implement 并取得用户明确确认。",
        ],
    }


def issue_scope_ledger_path(task_dir: Path) -> Path:
    return task_dir / "issue-scope-ledger.json"


def ensure_issue_scope_ledger(task_dir: Path, task_context: dict[str, Any]) -> Path:
    path = issue_scope_ledger_path(task_dir)
    if not path.exists():
        ledger = task_context.get("issue_scope_ledger")
        if not isinstance(ledger, dict):
            ledger = default_issue_scope_ledger(task_context)
        write_json(path, ledger)
    return path


def load_issue_scope_ledger(task_dir: Path, task_context: dict[str, Any]) -> dict[str, Any]:
    path = issue_scope_ledger_path(task_dir)
    if path.exists():
        return read_json(path)
    ledger = task_context.get("issue_scope_ledger")
    if isinstance(ledger, dict):
        return ledger
    return default_issue_scope_ledger(task_context)


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


def issue_has_evidence(issue: dict[str, Any]) -> bool:
    for key in ("acceptance_evidence", "verification", "evidence"):
        value = issue.get(key)
        if isinstance(value, list) and any(
            (isinstance(item, str) and item.strip())
            or (isinstance(item, dict) and item.get("status") == "passed")
            for item in value
        ):
            return True
        if isinstance(value, str) and value.strip():
            return True
    return False


REMOTE_MARKETPLACE_EVIDENCE_TYPE = "remote_marketplace_verification"


def remote_marketplace_evidence(issue: dict[str, Any]) -> dict[str, Any] | None:
    evidence = issue.get("acceptance_evidence")
    if not isinstance(evidence, list):
        return None
    matches = [item for item in evidence if isinstance(item, dict) and item.get("type") == REMOTE_MARKETPLACE_EVIDENCE_TYPE]
    return matches[0] if len(matches) == 1 else None


def remote_marketplace_evidence_errors(issue: dict[str, Any], *, allow_pending: bool) -> list[str]:
    item = remote_marketplace_evidence(issue)
    if item is None:
        return ["缺少唯一 remote_marketplace_verification 结构化 evidence。"]
    status = item.get("status")
    if status == "pending" and allow_pending:
        if item != {
            "type": REMOTE_MARKETPLACE_EVIDENCE_TYPE,
            "status": "pending",
            "required": True,
            "artifact_path": "marketplace-verification.json",
            "reason": "push 后由 deterministic marketplace verifier 生成真实 evidence；pending 不满足最终 publish。",
        }:
            return ["pending remote marketplace evidence 不符合固定合同。"]
        return []
    if status != "passed":
        return ["required remote marketplace evidence 必须是 passed；pending/文字说明不能发布。"]
    required = {
        "type", "status", "required", "artifact_path", "artifact_sha256",
        "verified_content_head", "remote_head", "publish_head", "commands_passed",
    }
    if set(item) != required:
        return ["passed remote marketplace evidence 字段不符合固定合同。"]
    errors: list[str] = []
    if item.get("required") is not True:
        errors.append("remote marketplace evidence required 必须为 true。")
    if not re.fullmatch(r"[0-9a-f]{64}", str(item.get("artifact_sha256") or "")):
        errors.append("remote marketplace evidence artifact_sha256 无效。")
    for key in ["verified_content_head", "remote_head", "publish_head"]:
        if not re.fullmatch(r"[0-9a-f]{40}", str(item.get(key) or "")):
            errors.append(f"remote marketplace evidence {key} 无效。")
    if item.get("commands_passed") is not True:
        errors.append("remote marketplace evidence commands_passed 必须为 true。")
    return errors


def validate_ledger_for_publish(ledger: dict[str, Any], gate: dict[str, Any], *, allow_pending_remote_marketplace: bool = False) -> list[str]:
    errors: list[str] = []
    close_issues = ledger.get("close_issues")
    if not isinstance(close_issues, list):
        errors.append("issue-scope-ledger.json 缺少 close_issues 数组。")
        close_issues = []
    related_numbers = set(issue_numbers(ledger.get("related_issues")))
    followup_numbers = set(issue_numbers(ledger.get("followup_issues")))
    gate_reviewed = set(issue_numbers(gate.get("issue_scope", {}).get("close_issues_reviewed")))
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
        if not issue_has_evidence(issue):
            errors.append(f"close_issues 中 issue #{number} 缺少验收或验证证据。")
        if marketplace_verification_required(gate):
            errors.extend(
                f"close_issues 中 issue #{number}：{error}"
                for error in remote_marketplace_evidence_errors(issue, allow_pending=allow_pending_remote_marketplace)
            )
        if number not in gate_reviewed:
            errors.append(f"Branch Review Gate 未记录对 close issue #{number} 的覆盖结论。")
    return errors


def review_gate_config(config: dict[str, Any]) -> dict[str, Any]:
    value = config.get("review_gate")
    return value if isinstance(value, dict) else dict(DEFAULTS["review_gate"])


def publish_config(config: dict[str, Any]) -> dict[str, Any]:
    value = config.get("publish")
    return value if isinstance(value, dict) else dict(DEFAULTS["publish"])


def validate_publish_invocation(args: argparse.Namespace) -> None:
    if getattr(args, "from_finish_work", False) or getattr(args, "recovery_after_finish_work", False):
        return
    raise WorkflowError(
        "publish-pr is an internal helper. Run `.trellis/guru-team/scripts/bash/finish-work.sh --json` "
        "so archive and initial finish-summary recording complete before PR publish. If finish-work already completed and only "
        "publish recovery is needed, rerun publish-pr with --recovery-after-finish-work.",
        exit_code=2,
        payload={
            "blocked_step": "publish-pr",
            "required_entrypoint": ".trellis/guru-team/scripts/bash/finish-work.sh --json",
            "recovery_flag": "--recovery-after-finish-work",
        },
    )


def validate_finish_work_invocation(args: argparse.Namespace) -> None:
    if getattr(args, "from_trellis_finish_work", False):
        return
    raise WorkflowError(
        "finish-work is the closeout helper and must be entered through the explicit "
        "`trellis-finish-work` skill/command, not chained from `trellis-continue`. "
        "Run `.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work` "
        "only after the user/session explicitly invoked trellis-finish-work.",
        exit_code=2,
        payload={
            "blocked_step": "finish-work",
            "required_entrypoint": "trellis-finish-work",
            "intent_flag": "--from-trellis-finish-work",
        },
    )


def configured_review_gate_path(task_dir: Path, config: dict[str, Any]) -> Path:
    gate_config = review_gate_config(config)
    configured = Path(str(gate_config.get("artifact_path") or "review-gate.json"))
    return configured if configured.is_absolute() else task_dir / configured


def parse_finding_arg(value: str) -> dict[str, Any]:
    parts = [part.strip() for part in value.split("|")]
    if len(parts) < 2:
        raise WorkflowError("Invalid --finding format. Use PRIORITY|message[|path].")
    priority = parts[0].upper()
    if priority not in VALID_PRIORITIES:
        raise WorkflowError(f"Invalid finding priority: {priority}")
    return {
        "priority": priority,
        "message": parts[1],
        "path": parts[2] if len(parts) >= 3 else "",
    }


def parse_review_note_arg(value: str, kind: str) -> dict[str, Any]:
    parts = [part.strip() for part in value.split("|")]
    message = parts[0] if parts else ""
    if not message:
        raise WorkflowError(f"Invalid --{kind.replace('_', '-')} format. Use message[|path].")
    return {
        "kind": kind,
        "message": message,
        "path": parts[1] if len(parts) >= 2 else "",
    }


def load_findings(args: argparse.Namespace) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if getattr(args, "findings_file", None):
        raw = json.loads(Path(args.findings_file).read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            raw = raw.get("findings", [])
        if not isinstance(raw, list):
            raise WorkflowError("--findings-file must contain a JSON list or an object with findings[].")
        for item in raw:
            if not isinstance(item, dict):
                raise WorkflowError("Each finding must be an object.")
            priority = str(item.get("priority") or "").upper()
            if priority not in VALID_PRIORITIES:
                raise WorkflowError(f"Invalid finding priority: {priority}")
            normalized = dict(item)
            normalized["priority"] = priority
            findings.append(normalized)
    for value in getattr(args, "finding", []) or []:
        findings.append(parse_finding_arg(value))
    return findings


def load_review_notes(
    file_arg: str | None,
    inline_values: list[str] | None,
    key: str,
    kind: str,
) -> list[dict[str, Any]]:
    notes: list[dict[str, Any]] = []
    if file_arg:
        raw = json.loads(Path(file_arg).read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            raw = raw.get(key, [])
        if not isinstance(raw, list):
            raise WorkflowError(f"--{key.replace('_', '-')}-file must contain a JSON list or an object with {key}[].")
        for item in raw:
            if isinstance(item, str):
                notes.append(parse_review_note_arg(item, kind))
                continue
            if not isinstance(item, dict):
                raise WorkflowError(f"Each {kind} must be an object or string.")
            message = str(item.get("message") or "").strip()
            if not message:
                raise WorkflowError(f"Each {kind} needs a non-empty message.")
            normalized = dict(item)
            normalized["kind"] = kind
            normalized["message"] = message
            normalized["path"] = str(normalized.get("path") or "").strip()
            notes.append(normalized)
    for value in inline_values or []:
        notes.append(parse_review_note_arg(value, kind))
    return notes


def load_observations(args: argparse.Namespace) -> list[dict[str, Any]]:
    return load_review_notes(
        getattr(args, "observations_file", None),
        getattr(args, "observation", []) or [],
        "observations",
        "observation",
    )


def load_followup_candidates(args: argparse.Namespace) -> list[dict[str, Any]]:
    return load_review_notes(
        getattr(args, "followup_candidates_file", None),
        getattr(args, "followup_candidate", []) or [],
        "followup_candidates",
        "followup_candidate",
    )


def load_review_report(root: Path, task_dir: Path, report_arg: str | None) -> dict[str, Any] | None:
    if not report_arg:
        return None
    raw_path = Path(report_arg).expanduser()
    path = raw_path if raw_path.is_absolute() else root / raw_path
    if not path.exists():
        raise WorkflowError(f"--review-report not found: {path}")
    if not path.is_file():
        raise WorkflowError(f"--review-report must point to a file: {path}")
    if task_dir.resolve() not in [path.resolve(), *path.resolve().parents]:
        raise WorkflowError("--review-report must point to a task-local review.md inside the current task directory.")
    if path.name != REVIEW_REPORT_ARTIFACT:
        raise WorkflowError("--review-report must point to the task-local review.md file, not another task artifact.")
    content = path.read_bytes()
    if not content.strip():
        raise WorkflowError("--review-report must not be empty.")
    stat = path.stat()
    return {
        "path": repo_relative(root, path),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
    }


def raw_review_report_path_errors(root: Path, task_dir: Path, path: Path, label: str) -> list[str]:
    errors: list[str] = []
    resolved = path.resolve()
    reviews_dir = (task_dir / REVIEW_ROUND_REPORT_DIR).resolve()
    if reviews_dir not in [resolved, *resolved.parents] or resolved.parent != reviews_dir:
        errors.append(f"{label} must point to a task-local {REVIEW_ROUND_REPORT_DIR}/*.md file.")
    if resolved.suffix != ".md":
        errors.append(f"{label} must point to a Markdown .md file.")
    try:
        resolved.relative_to(task_dir.resolve())
    except ValueError:
        errors.append(f"{label} must stay inside the current task directory.")
    return errors


def load_review_round_report(root: Path, task_dir: Path, report_arg: str | None) -> dict[str, Any]:
    if not report_arg:
        raise WorkflowError(
            "record-agent-assignment --review-round requires --review-round-report pointing to task-local reviews/*.md.",
            exit_code=2,
        )
    path = resolve_task_local_path(root, task_dir, report_arg)
    errors = raw_review_report_path_errors(root, task_dir, path, "--review-round-report")
    if errors:
        raise WorkflowError(
            "Invalid --review-round-report.",
            exit_code=2,
            payload={"errors": errors},
        )
    return file_digest(root, path)


def review_round_report_digest_entry(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": item.get("review_report_path"),
        "sha256": item.get("review_report_sha256"),
        "size_bytes": item.get("review_report_size_bytes"),
        "modified_at": item.get("review_report_modified_at"),
    }


def add_review_round_report_digest_fields(event: dict[str, Any], digest: dict[str, Any]) -> None:
    event["review_report_path"] = digest.get("path")
    event["review_report_sha256"] = digest.get("sha256")
    event["review_report_size_bytes"] = digest.get("size_bytes")
    event["review_report_modified_at"] = digest.get("modified_at")


def resolve_task_local_path(root: Path, task_dir: Path, value: str) -> Path:
    raw_path = Path(value).expanduser()
    if raw_path.is_absolute():
        path = raw_path
    elif str(value).startswith(".trellis/") or str(value).startswith("trellis/"):
        path = root / raw_path
    else:
        path = task_dir / raw_path
    resolved = path.resolve()
    if task_dir.resolve() not in [resolved, *resolved.parents]:
        raise WorkflowError(f"Artifact path must stay inside the current task directory: {value}")
    return resolved


def resolve_repo_path(root: Path, value: str) -> Path:
    raw_path = Path(value).expanduser()
    return raw_path if raw_path.is_absolute() else root / raw_path


def resolve_checked_spec_path(root: Path, value: str) -> Path:
    path = resolve_repo_path(root, value).resolve()
    spec_root = (root / ".trellis/spec").resolve()
    if spec_root not in [path, *path.parents]:
        raise WorkflowError(f"Checked spec must stay inside .trellis/spec: {value}", exit_code=2)
    return path


def file_digest(root: Path, path: Path) -> dict[str, Any]:
    if not path.exists():
        raise WorkflowError(f"Required artifact not found: {path}")
    if not path.is_file():
        raise WorkflowError(f"Artifact must point to a file: {path}")
    content = path.read_bytes()
    if not content.strip():
        raise WorkflowError(f"Artifact must not be empty: {path}")
    stat = path.stat()
    return {
        "path": repo_relative(root, path),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
    }


def agent_assignment_path(task_dir: Path) -> Path:
    return task_dir / AGENT_ASSIGNMENT_ARTIFACT


def default_agent_assignment_payload(root: Path, task_dir: Path) -> dict[str, Any]:
    return {
        "schema_version": AGENT_ASSIGNMENT_SCHEMA_VERSION,
        "generated_at": now_iso(),
        "updated_at": now_iso(),
        "task": repo_relative(root, task_dir),
        "head": current_head(root),
        "agents": [],
        "liveness": {},
        "review_rounds": [],
        "reuse_decisions": [],
        "status_events": [],
        "notes": "agent-assignment.json 是 task-local recorder artifact：AI/human 决定 sub-agent 分配、复用、更换或状态处理；脚本只记录和校验客观字段、HEAD、digest 与枚举值。",
    }


def load_agent_assignment(root: Path, task_dir: Path) -> dict[str, Any]:
    path = agent_assignment_path(task_dir)
    if not path.exists():
        return default_agent_assignment_payload(root, task_dir)
    payload = read_json(path)
    if not isinstance(payload.get("agents"), list):
        payload["agents"] = []
    if not isinstance(payload.get("liveness"), dict):
        payload["liveness"] = {}
    if not isinstance(payload.get("review_rounds"), list):
        payload["review_rounds"] = []
    if not isinstance(payload.get("reuse_decisions"), list):
        payload["reuse_decisions"] = []
    if not isinstance(payload.get("status_events"), list):
        payload["status_events"] = []
    payload["schema_version"] = AGENT_ASSIGNMENT_SCHEMA_VERSION
    payload.setdefault("task", repo_relative(root, task_dir))
    payload.setdefault("head", current_head(root))
    return payload


def clean_optional_text(value: Any) -> str:
    return str(value or "").strip()


def validate_logical_role(value: str) -> str:
    role = value.strip()
    if role not in ALLOWED_LOGICAL_ROLES:
        raise WorkflowError(
            f"Invalid logical role: {role or '(empty)'}. Valid roles: {', '.join(ALLOWED_LOGICAL_ROLES)}",
            exit_code=2,
        )
    return role


def validate_reuse_decision_value(value: str) -> str:
    decision = value.strip()
    if decision not in ALLOWED_REUSE_DECISIONS:
        raise WorkflowError(
            f"Invalid reuse decision: {decision or '(empty)'}. Valid decisions: {', '.join(sorted(ALLOWED_REUSE_DECISIONS))}",
            exit_code=2,
        )
    return decision


def validate_agent_status_event_value(value: str) -> str:
    event = value.strip()
    if event not in ALLOWED_AGENT_STATUS_EVENTS:
        raise WorkflowError(
            f"Invalid agent status event: {event or '(empty)'}. Valid events: {', '.join(sorted(ALLOWED_AGENT_STATUS_EVENTS))}",
            exit_code=2,
        )
    return event


def parse_iso_datetime(value: Any, label: str = "timestamp") -> datetime:
    text = str(value or "").strip()
    if not text:
        raise WorkflowError(f"{label} is required.", exit_code=2)
    normalized = text.removesuffix("Z") + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise WorkflowError(f"{label} must be ISO-8601: {text}", exit_code=2) from exc
    if parsed.tzinfo is None:
        raise WorkflowError(f"{label} must include a UTC offset: {text}", exit_code=2)
    return parsed.astimezone(timezone.utc)


def parse_utc_iso_datetime(value: Any, label: str = "timestamp") -> datetime:
    text = str(value or "").strip()
    if not text:
        raise WorkflowError(f"{label} is required.", exit_code=2)
    normalized = text.removesuffix("Z") + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise WorkflowError(f"{label} must be ISO-8601 UTC: {text}", exit_code=2) from exc
    if parsed.tzinfo is None:
        raise WorkflowError(f"{label} must include a UTC offset: {text}", exit_code=2)
    if parsed.utcoffset() != timedelta(0):
        raise WorkflowError(f"{label} must be UTC, not a non-zero offset: {text}", exit_code=2)
    return parsed.astimezone(timezone.utc)


def iso_from_datetime(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_utc_iso(value: Any, label: str = "timestamp") -> str:
    return iso_from_datetime(parse_utc_iso_datetime(value, label))


def max_iso(left: str, right: str) -> str:
    if not left:
        return right
    if not right:
        return left
    return iso_from_datetime(max(parse_iso_datetime(left), parse_iso_datetime(right)))


def evidence_is_placeholder(value: str) -> bool:
    normalized = re.sub(r"\s+", " ", value.strip()).casefold()
    return normalized in PLACEHOLDER_EVIDENCE_VALUES


def validate_event_evidence(value: str) -> str:
    evidence = value.strip()
    if evidence_is_placeholder(evidence):
        raise WorkflowError("liveness event requires non-placeholder --evidence.", exit_code=2)
    return evidence


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def digest_lines(lines: list[str]) -> str:
    return digest_text("\n".join(lines))


def relative_to_repo_for_git(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.name


def filtered_git_lines(root: Path, cmd: list[str], excluded_paths: set[str]) -> list[str]:
    proc = run(cmd, cwd=root, check=False)
    text = (proc.stdout or "") if proc.returncode == 0 else (proc.stdout or "") + "\n" + (proc.stderr or "")
    excluded = {path.strip("/") for path in excluded_paths if path.strip("/")}
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line:
            continue
        if any(path and path in line for path in excluded):
            continue
        lines.append(line)
    return sorted(lines)


def max_file_mtime_iso(root: Path, excluded_paths: set[str]) -> str:
    excluded = {(root / path).resolve() for path in excluded_paths if path}
    max_mtime = 0.0
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        dirs[:] = [name for name in dirs if name != ".git"]
        for name in files:
            path = (current_path / name).resolve()
            if path in excluded:
                continue
            if any(parent.name == ".git" for parent in path.parents):
                continue
            try:
                mtime = path.stat().st_mtime
            except OSError:
                continue
            if mtime > max_mtime:
                max_mtime = mtime
    if max_mtime <= 0:
        return ""
    return datetime.fromtimestamp(max_mtime, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def progress_events_for_agent(payload: dict[str, Any], agent_id: str) -> list[dict[str, Any]]:
    events = payload.get("status_events")
    if not isinstance(events, list):
        return []
    return [
        item
        for item in events
        if isinstance(item, dict)
        and str(item.get("agent_id") or "").strip() == agent_id
        and str(item.get("event") or "").strip() in AGENT_PROGRESS_EVENTS
    ]


def progress_events_digest(payload: dict[str, Any], agent_id: str) -> dict[str, Any]:
    events = progress_events_for_agent(payload, agent_id)
    normalized = [
        {
            "event_id": str(item.get("event_id") or ""),
            "event": str(item.get("event") or ""),
            "observed_at": str(item.get("observed_at") or ""),
            "evidence": str(item.get("evidence") or ""),
        }
        for item in events
    ]
    newest = ""
    if events:
        newest_item = max(events, key=lambda item: parse_iso_datetime(item.get("observed_at"), "progress observed_at"))
        newest = str(newest_item.get("event_id") or "")
    return {
        "progress_events_count": len(events),
        "progress_events_digest": digest_text(json.dumps(normalized, ensure_ascii=False, sort_keys=True)),
        "progress_events_newest_event_id": newest,
    }


def resolve_source_repo(source_repo: str | None) -> Path:
    value = clean_optional_text(source_repo)
    if not value:
        raise WorkflowError("subagent liveness recorder/checker requires --source-repo.", exit_code=2)
    path = Path(value).expanduser()
    if not path.exists():
        raise WorkflowError(f"source repo does not exist: {path}", exit_code=2)
    return repo_root(path)


def collect_liveness_snapshot(root: Path, task_dir: Path, source_repo: Path, payload: dict[str, Any], agent_id: str, captured_at: str | None = None) -> dict[str, Any]:
    captured = captured_at or now_iso()
    artifact_relative = relative_to_repo_for_git(root, agent_assignment_path(task_dir))
    task_status_lines = filtered_git_lines(root, ["git", "status", "--porcelain"], {artifact_relative})
    task_diff_lines = filtered_git_lines(root, ["git", "diff", "--stat"], {artifact_relative})
    task_diff_lines.extend(filtered_git_lines(root, ["git", "diff", "--cached", "--stat"], {artifact_relative}))
    source_status_lines = filtered_git_lines(source_repo, ["git", "status", "--porcelain"], set())
    source_diff_lines = filtered_git_lines(source_repo, ["git", "diff", "--stat"], set())
    source_diff_lines.extend(filtered_git_lines(source_repo, ["git", "diff", "--cached", "--stat"], set()))
    return {
        "captured_at": captured,
        "task_head": current_head(root),
        "task_content_status_digest": digest_lines(task_status_lines),
        "task_content_diff_stat_digest": digest_lines(sorted(task_diff_lines)),
        "task_content_max_mtime": max_file_mtime_iso(root, {artifact_relative}),
        "source_head": current_head(source_repo),
        "source_status_digest": digest_lines(source_status_lines),
        "source_diff_stat_digest": digest_lines(sorted(source_diff_lines)),
        "source_max_mtime": max_file_mtime_iso(source_repo, set()),
        **progress_events_digest(payload, agent_id),
    }


def source_repo_from_task_context(root: Path, task_context: dict[str, Any]) -> Path:
    source = task_context.get("source_repo_path") or str(root)
    return repo_root(Path(str(source)).expanduser())


def agent_record(payload: dict[str, Any], agent_id: str) -> dict[str, Any] | None:
    agents = payload.get("agents")
    if not isinstance(agents, list):
        return None
    for item in agents:
        if isinstance(item, dict) and str(item.get("agent_id") or "").strip() == agent_id:
            return item
    return None


def next_event_id(payload: dict[str, Any], event: str, agent_id: str) -> str:
    events = payload.get("status_events")
    count = len(events) + 1 if isinstance(events, list) else 1
    seed = f"{event}|{agent_id}|{now_iso()}|{count}"
    return f"evt-{count:04d}-{hashlib.sha1(seed.encode('utf-8')).hexdigest()[:10]}"


def ensure_liveness_entry(payload: dict[str, Any], agent_id: str) -> dict[str, Any]:
    liveness = payload.setdefault("liveness", {})
    if not isinstance(liveness, dict):
        raise WorkflowError("agent-assignment.json liveness must be an object.", exit_code=2)
    entry = liveness.setdefault(agent_id, {})
    if not isinstance(entry, dict):
        raise WorkflowError(f"agent-assignment.json liveness[{agent_id}] must be an object.", exit_code=2)
    return entry


def append_agent_assignment_event(
    payload: dict[str, Any],
    root: Path,
    task_dir: Path,
    logical_role: str,
    agent_id: str,
    platform_nickname: str,
    reason: str,
    source_repo: Path | None = None,
    observed_at: str | None = None,
) -> dict[str, Any]:
    if not reason:
        raise WorkflowError("record-agent-assignment requires --reason explaining the AI/human assignment decision.", exit_code=2)
    if not agent_id:
        raise WorkflowError("assigned liveness event requires --agent-id.", exit_code=2)
    if agent_record(payload, agent_id):
        raise WorkflowError(f"agent already assigned: {agent_id}", exit_code=2)
    observed = normalize_utc_iso(observed_at or now_iso(), "assigned.observed_at")
    role = validate_logical_role(logical_role)
    event = {
        "logical_role": role,
        "agent_id": agent_id,
        "platform_nickname": platform_nickname,
        "assigned_at": observed,
        "assigned_head": current_head(root),
        "reason": reason,
    }
    payload["agents"].append(event)
    status_event = build_liveness_event(
        payload=payload,
        root=root,
        logical_role=role,
        agent_id=agent_id,
        platform_nickname=platform_nickname,
        event_name="assigned",
        observed_at=observed,
        evidence=reason,
        source="main-session",
    )
    event["event_id"] = status_event["event_id"]
    payload.setdefault("status_events", []).append(status_event)
    source = source_repo or root
    snapshot = collect_liveness_snapshot(root, task_dir, source, payload, agent_id, captured_at=observed)
    liveness = ensure_liveness_entry(payload, agent_id)
    liveness.update(
        {
            "progress_anchor_at": observed,
            "last_scan_snapshot": snapshot,
            "pending_status_request_at": None,
            "last_checked_at": "",
            "last_decision": "",
        }
    )
    return event


def append_agent_review_round(
    payload: dict[str, Any],
    root: Path,
    task_dir: Path,
    logical_role: str,
    agent_id: str,
    platform_nickname: str,
    round_value: int,
    findings_count: int,
    reuse_policy: str,
    reuse_decision: str,
    reviewed_head: str | None,
    review_round_report: str | None,
) -> dict[str, Any]:
    if round_value <= 0:
        raise WorkflowError("review round must be a positive integer.", exit_code=2)
    if findings_count < 0:
        raise WorkflowError("findings count must be a non-negative integer.", exit_code=2)
    if not reuse_policy:
        raise WorkflowError("review round requires --reuse-policy with the AI/human review reuse rule.", exit_code=2)
    event = {
        "round": round_value,
        "logical_role": validate_logical_role(logical_role),
        "agent_id": agent_id,
        "platform_nickname": platform_nickname,
        "reviewed_head": reviewed_head or current_head(root),
        "findings_count": findings_count,
        "reuse_policy": reuse_policy,
        "reuse_decision": validate_reuse_decision_value(reuse_decision),
        "recorded_at": now_iso(),
    }
    add_review_round_report_digest_fields(event, load_review_round_report(root, task_dir, review_round_report))
    payload["review_rounds"].append(event)
    return event


def append_agent_reuse_decision(
    payload: dict[str, Any],
    root: Path,
    logical_role: str,
    agent_id: str,
    decision: str,
    reason: str,
    from_round: int | None,
    to_round: int | None,
    head: str | None,
) -> dict[str, Any]:
    if not reason:
        raise WorkflowError("reuse decision requires --reuse-reason with the AI/human decision rationale.", exit_code=2)
    if from_round is not None and from_round <= 0:
        raise WorkflowError("--from-round must be a positive integer.", exit_code=2)
    if to_round is not None and to_round <= 0:
        raise WorkflowError("--to-round must be a positive integer.", exit_code=2)
    event = {
        "logical_role": validate_logical_role(logical_role),
        "agent_id": agent_id,
        "decision": validate_reuse_decision_value(decision),
        "reason": reason,
        "head": head or current_head(root),
        "recorded_at": now_iso(),
    }
    if from_round is not None:
        event["from_round"] = from_round
    if to_round is not None:
        event["to_round"] = to_round
    payload["reuse_decisions"].append(event)
    return event


def build_liveness_event(
    *,
    payload: dict[str, Any],
    root: Path,
    logical_role: str,
    agent_id: str,
    platform_nickname: str,
    event_name: str,
    observed_at: str,
    evidence: str,
    source: str,
    predecessor_agent_id: str = "",
    predecessor_event_id: str = "",
    termination_reason: str = "",
    termination_source_event_id: str = "",
    replacement_reason: str = "",
    handoff_summary: str = "",
) -> dict[str, Any]:
    event = validate_agent_status_event_value(event_name)
    if source not in AGENT_STATUS_EVENT_SOURCES:
        raise WorkflowError(f"Invalid liveness event source: {source}", exit_code=2)
    observed = normalize_utc_iso(observed_at or now_iso(), "observed_at")
    return {
        "event_id": next_event_id(payload, event, agent_id),
        "event": event,
        "agent_id": agent_id,
        "logical_role": validate_logical_role(logical_role),
        "platform_nickname": platform_nickname,
        "observed_at": observed,
        "recorded_at": now_iso(),
        "head": current_head(root),
        "source": source,
        "evidence": validate_event_evidence(evidence),
        "predecessor_agent_id": predecessor_agent_id,
        "predecessor_event_id": predecessor_event_id,
        "termination_reason": termination_reason,
        "termination_source_event_id": termination_source_event_id,
        "replacement_reason": replacement_reason,
        "handoff_summary": handoff_summary,
    }


def event_by_id(payload: dict[str, Any], event_id: str) -> dict[str, Any] | None:
    if not event_id:
        return None
    events = payload.get("status_events")
    if not isinstance(events, list):
        return None
    for item in events:
        if isinstance(item, dict) and str(item.get("event_id") or "").strip() == event_id:
            return item
    return None


def latest_progress_observed_at(payload: dict[str, Any], agent_id: str) -> str:
    events = progress_events_for_agent(payload, agent_id)
    if not events:
        return ""
    newest = max(events, key=lambda item: parse_iso_datetime(item.get("observed_at"), "progress observed_at"))
    return str(newest.get("observed_at") or "")


def validate_resume_reference(payload: dict[str, Any], agent_id: str, predecessor_event_id: str) -> None:
    predecessor = event_by_id(payload, predecessor_event_id)
    if not predecessor or str(predecessor.get("agent_id") or "") != agent_id:
        raise WorkflowError("resume-same-agent requires --predecessor-event-id referencing the same agent.", exit_code=2)
    predecessor_event = str(predecessor.get("event") or "")
    predecessor_reason = str(predecessor.get("termination_reason") or "")
    if predecessor_event == "failed":
        return
    if predecessor_event == "terminated-unfinished" and predecessor_reason == "manual_or_platform_terminated_unfinished":
        return
    raise WorkflowError("resume-same-agent may reference only failed or manual_or_platform_terminated_unfinished evidence, never stale evidence.", exit_code=2)


def validate_replacement_reference(
    payload: dict[str, Any],
    agent_id: str,
    predecessor_agent_id: str,
    predecessor_event_id: str,
    replacement_reason: str,
) -> None:
    if agent_id == predecessor_agent_id:
        raise WorkflowError("replacement-started requires a different replacement agent; use resume-same-agent for same-agent recovery.", exit_code=2)
    if not agent_record(payload, agent_id):
        raise WorkflowError("replacement-started requires the replacement agent to be assigned first.", exit_code=2)
    predecessor = event_by_id(payload, predecessor_event_id)
    if not predecessor or str(predecessor.get("agent_id") or "") != predecessor_agent_id:
        raise WorkflowError("replacement-started predecessor_event_id must reference predecessor_agent_id.", exit_code=2)
    predecessor_event = str(predecessor.get("event") or "")
    predecessor_termination_reason = str(predecessor.get("termination_reason") or "")
    expected = ""
    if predecessor_event == "stale-assessed":
        expected = "max_progress_silence_exceeded"
        has_cutover = any(
            isinstance(item, dict)
            and str(item.get("event") or "") == "terminated-unfinished"
            and str(item.get("agent_id") or "") == predecessor_agent_id
            and str(item.get("termination_reason") or "") == "stale_cutover"
            and str(item.get("termination_source_event_id") or "") == predecessor_event_id
            for item in payload.get("status_events", [])
        )
        if not has_cutover:
            raise WorkflowError("stale replacement-started requires prior terminated-unfinished termination_reason=stale_cutover.", exit_code=2)
    elif predecessor_event == "failed":
        expected = "terminal_failed_incomplete"
    elif predecessor_event == "terminated-unfinished" and predecessor_termination_reason == "manual_or_platform_terminated_unfinished":
        expected = "manual_or_platform_terminated_unfinished"
    elif predecessor_event == "terminated-unfinished" and predecessor_termination_reason == "stale_cutover":
        raise WorkflowError("stale cutover replacement-started must reference stale-assessed, not terminated-unfinished.", exit_code=2)
    else:
        raise WorkflowError("replacement-started predecessor_event_id must reference failed, stale-assessed, or terminated-unfinished evidence.", exit_code=2)
    if replacement_reason != expected:
        raise WorkflowError(
            f"replacement-started replacement_reason must be {expected} for predecessor event {predecessor_event}.",
            exit_code=2,
        )


def validate_termination_reference(payload: dict[str, Any], agent_id: str, termination_reason: str, termination_source_event_id: str) -> None:
    if termination_reason not in AGENT_TERMINATION_REASONS:
        raise WorkflowError(f"Invalid termination_reason: {termination_reason or '(empty)'}", exit_code=2)
    if termination_reason == "stale_cutover":
        source_event = event_by_id(payload, termination_source_event_id)
        if not source_event or str(source_event.get("agent_id") or "") != agent_id or str(source_event.get("event") or "") != "stale-assessed":
            raise WorkflowError("stale_cutover requires termination_source_event_id referencing same-agent stale-assessed.", exit_code=2)
    elif termination_source_event_id:
        raise WorkflowError("manual_or_platform_terminated_unfinished must not set termination_source_event_id.", exit_code=2)


def require_status_request_decision(payload: dict[str, Any], agent_id: str, event: str) -> None:
    liveness = payload.get("liveness") if isinstance(payload.get("liveness"), dict) else {}
    entry = liveness.get(agent_id) if isinstance(liveness, dict) else None
    if not isinstance(entry, dict):
        raise WorkflowError(f"{event} requires liveness entry for agent.", exit_code=2)
    if str(entry.get("last_decision") or "") != "status_request_required":
        raise WorkflowError(
            f"{event} requires last_decision == status_request_required; run check-subagent-liveness and send status request only after that decision.",
            exit_code=2,
        )


def verify_stale_assessed_freshness(root: Path, task_dir: Path, source_repo: Path, payload: dict[str, Any], agent_id: str) -> None:
    liveness = payload.get("liveness") if isinstance(payload.get("liveness"), dict) else {}
    entry = liveness.get(agent_id) if isinstance(liveness, dict) else None
    if not isinstance(entry, dict):
        raise WorkflowError("stale-assessed requires liveness entry for agent.", exit_code=2)
    if str(entry.get("last_decision") or "") != "stale_allowed":
        raise WorkflowError("stale-assessed requires last_decision == stale_allowed; rerun check-subagent-liveness first.", exit_code=2)
    previous = entry.get("last_scan_snapshot")
    if not isinstance(previous, dict):
        raise WorkflowError("stale-assessed requires last_scan_snapshot evidence.", exit_code=2)
    current = collect_liveness_snapshot(root, task_dir, source_repo, payload, agent_id, captured_at=str(previous.get("captured_at") or now_iso()))
    changed = [
        field
        for field in AGENT_LIVENESS_SNAPSHOT_FIELDS
        if str(current.get(field) or "") != str(previous.get(field) or "")
    ]
    if changed:
        raise WorkflowError(
            "stale-assessed refused because new progress or snapshot drift appeared; rerun check-subagent-liveness.",
            exit_code=2,
            payload={"changed_snapshot_fields": changed},
        )


def append_subagent_liveness_event(
    payload: dict[str, Any],
    root: Path,
    task_dir: Path,
    source_repo: Path,
    *,
    agent_id: str,
    event_name: str,
    observed_at: str,
    evidence: str,
    logical_role: str = "",
    platform_nickname: str = "",
    source: str = "main-session",
    predecessor_agent_id: str = "",
    predecessor_event_id: str = "",
    termination_reason: str = "",
    termination_source_event_id: str = "",
    replacement_reason: str = "",
    handoff_summary: str = "",
) -> dict[str, Any]:
    event = validate_agent_status_event_value(event_name)
    if event == "assigned":
        return append_agent_assignment_event(
            payload,
            root,
            task_dir,
            logical_role,
            agent_id,
            platform_nickname,
            validate_event_evidence(evidence),
            source_repo=source_repo,
            observed_at=observed_at,
        )
    assigned_agent = agent_record(payload, agent_id)
    if not assigned_agent:
        raise WorkflowError(f"liveness event requires existing assigned agent: {agent_id}", exit_code=2)
    role = str(assigned_agent.get("logical_role") or "")
    nickname = str(assigned_agent.get("platform_nickname") or "")
    if event == "resume-same-agent":
        if not predecessor_event_id or not handoff_summary:
            raise WorkflowError("resume-same-agent requires --predecessor-event-id and --handoff-summary.", exit_code=2)
        validate_resume_reference(payload, agent_id, predecessor_event_id)
    elif event == "replacement-started":
        if not predecessor_agent_id or not predecessor_event_id or not replacement_reason or not handoff_summary:
            raise WorkflowError("replacement-started requires --predecessor-agent-id, --predecessor-event-id, --replacement-reason, and --handoff-summary.", exit_code=2)
        if replacement_reason not in AGENT_REPLACEMENT_REASONS:
            raise WorkflowError(f"Invalid replacement_reason: {replacement_reason}", exit_code=2)
        validate_replacement_reference(payload, agent_id, predecessor_agent_id, predecessor_event_id, replacement_reason)
    elif event == "terminated-unfinished":
        if not termination_reason or not handoff_summary:
            raise WorkflowError("terminated-unfinished requires --termination-reason and --handoff-summary.", exit_code=2)
        validate_termination_reference(payload, agent_id, termination_reason, termination_source_event_id)
    elif event == "stale-assessed":
        verify_stale_assessed_freshness(root, task_dir, source_repo, payload, agent_id)
    elif event in {"status-requested", "status-request-failed"}:
        require_status_request_decision(payload, agent_id, event)
    else:
        forbidden_values = {
            "predecessor_agent_id": predecessor_agent_id,
            "predecessor_event_id": predecessor_event_id,
            "termination_reason": termination_reason,
            "termination_source_event_id": termination_source_event_id,
            "replacement_reason": replacement_reason,
            "handoff_summary": handoff_summary,
        }
        present = [name for name, value in forbidden_values.items() if value]
        if present:
            raise WorkflowError(f"{event} does not accept fields: {', '.join(present)}", exit_code=2)

    status_event = build_liveness_event(
        payload=payload,
        root=root,
        logical_role=role,
        agent_id=agent_id,
        platform_nickname=nickname,
        event_name=event,
        observed_at=observed_at or now_iso(),
        evidence=evidence,
        source=source,
        predecessor_agent_id=predecessor_agent_id,
        predecessor_event_id=predecessor_event_id,
        termination_reason=termination_reason,
        termination_source_event_id=termination_source_event_id,
        replacement_reason=replacement_reason,
        handoff_summary=handoff_summary,
    )
    payload.setdefault("status_events", []).append(status_event)
    liveness = ensure_liveness_entry(payload, agent_id)
    if event == "status-requested":
        if liveness.get("pending_status_request_at"):
            raise WorkflowError("status-requested already pending; run checker and do not repeat ping.", exit_code=2)
        liveness["pending_status_request_at"] = status_event["observed_at"]
    elif event in AGENT_TERMINAL_EVENTS or event == "terminated-unfinished":
        liveness["pending_status_request_at"] = None
    return status_event


def changed_snapshot_sources(previous: dict[str, Any], current: dict[str, Any], prefix: str) -> list[dict[str, Any]]:
    mapping = {
        "task": [
            ("task_head", "task_head"),
            ("task_content_status_digest", "task_status"),
            ("task_content_diff_stat_digest", "task_diff_stat"),
            ("task_content_max_mtime", "task_mtime"),
        ],
        "source": [
            ("source_head", "source_head"),
            ("source_status_digest", "source_status"),
            ("source_diff_stat_digest", "source_diff_stat"),
            ("source_max_mtime", "source_mtime"),
        ],
    }[prefix]
    sources: list[dict[str, Any]] = []
    for field, source_kind in mapping:
        if str(previous.get(field) or "") != str(current.get(field) or ""):
            sources.append(
                {
                    "source": source_kind,
                    "observed_at": current.get("captured_at"),
                    "evidence": f"{field} changed",
                }
            )
    return sources


def new_progress_event_sources(payload: dict[str, Any], agent_id: str, previous: dict[str, Any], current: dict[str, Any]) -> list[dict[str, Any]]:
    if (
        previous.get("progress_events_count") == current.get("progress_events_count")
        and previous.get("progress_events_digest") == current.get("progress_events_digest")
        and previous.get("progress_events_newest_event_id") == current.get("progress_events_newest_event_id")
    ):
        return []
    # last_scan_snapshot stores digest/count/newest rather than the full id set;
    # report the newest current progress event as the auditable trigger.
    events = progress_events_for_agent(payload, agent_id)
    if not events:
        return []
    newest = max(events, key=lambda item: parse_iso_datetime(item.get("observed_at"), "progress observed_at"))
    return [
        {
            "source": "status_event",
            "event_id": newest.get("event_id"),
            "event": newest.get("event"),
            "observed_at": newest.get("observed_at"),
            "evidence": newest.get("evidence"),
        }
    ]


def deadline_for_anchor(progress_anchor_at: str, max_progress_silence: int) -> str:
    anchor = parse_iso_datetime(progress_anchor_at, "progress_anchor_at")
    return iso_from_datetime(anchor + timedelta(seconds=max_progress_silence))


def calculate_next_wait_ms(checked_at: str, deadline_at: str, progress_scan_interval: int, immediate: bool = False) -> int:
    if immediate:
        return 0
    checked = parse_iso_datetime(checked_at, "checked_at")
    deadline = parse_iso_datetime(deadline_at, "max_progress_silence_deadline_at")
    remaining_ms = int((deadline - checked).total_seconds() * 1000)
    if remaining_ms <= 0:
        return 0
    return min(progress_scan_interval * 1000, remaining_ms)


def latest_progress_anchor(payload: dict[str, Any], agent_id: str, current_anchor: str, source_decision: str, snapshot: dict[str, Any], progress_sources: list[dict[str, Any]]) -> str:
    anchor = current_anchor
    if source_decision == "workspace_boundary_violation_progress":
        return max_iso(anchor, str(snapshot.get("captured_at") or ""))
    task_machine_sources = {"task_head", "task_status", "task_diff_stat", "task_mtime"}
    if any(source.get("source") in task_machine_sources for source in progress_sources):
        anchor = max_iso(anchor, str(snapshot.get("captured_at") or ""))
    progress_times = [
        str(source.get("observed_at") or "")
        for source in progress_sources
        if source.get("source") == "status_event" and source.get("observed_at")
    ]
    for observed_at in progress_times:
        anchor = max_iso(anchor, observed_at)
    return anchor


def evaluate_subagent_liveness(
    root: Path,
    task_dir: Path,
    source_repo: Path,
    payload: dict[str, Any],
    agent_id: str,
    progress_scan_interval: int,
    max_progress_silence: int,
    checked_at: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if progress_scan_interval <= 0 or max_progress_silence <= progress_scan_interval:
        raise WorkflowError("max-progress-silence must be greater than progress-scan-interval.", exit_code=2)
    if not agent_record(payload, agent_id):
        raise WorkflowError(f"agent is not assigned: {agent_id}", exit_code=2)
    liveness = ensure_liveness_entry(payload, agent_id)
    previous = liveness.get("last_scan_snapshot")
    if not isinstance(previous, dict):
        raise WorkflowError("liveness last_scan_snapshot is missing; record assigned baseline first.", exit_code=2)
    checked = normalize_utc_iso(checked_at or now_iso(), "checked_at")
    snapshot = collect_liveness_snapshot(root, task_dir, source_repo, payload, agent_id, captured_at=checked)
    source_progress = changed_snapshot_sources(previous, snapshot, "source")
    task_progress = changed_snapshot_sources(previous, snapshot, "task")
    event_progress = new_progress_event_sources(payload, agent_id, previous, snapshot)
    progress_sources = source_progress + task_progress + event_progress
    current_anchor = str(liveness.get("progress_anchor_at") or "")
    if not current_anchor:
        assigned = agent_record(payload, agent_id) or {}
        current_anchor = str(assigned.get("assigned_at") or checked)
    decision = ""
    reason = ""
    if source_progress:
        decision = "workspace_boundary_violation_progress"
        reason = "source checkout snapshot changed; treat as workspace boundary progress."
    elif task_progress or event_progress:
        decision = "progress_observed"
        reason = "task snapshot or recorded progress event changed."
    if decision:
        anchor = latest_progress_anchor(payload, agent_id, current_anchor, decision, snapshot, progress_sources)
        liveness["progress_anchor_at"] = anchor
        liveness["pending_status_request_at"] = None
        deadline = deadline_for_anchor(anchor, max_progress_silence)
        next_wait_ms = calculate_next_wait_ms(checked, deadline, progress_scan_interval)
    else:
        anchor = current_anchor
        deadline = deadline_for_anchor(anchor, max_progress_silence)
        pending = clean_optional_text(liveness.get("pending_status_request_at"))
        if not pending:
            decision = "status_request_required"
            reason = "no new progress and no pending status request."
            next_wait_ms = 0
        elif parse_iso_datetime(checked, "checked_at") >= parse_iso_datetime(deadline, "max_progress_silence_deadline_at"):
            decision = "stale_allowed"
            reason = "pending status request exists, no progress response appeared, and max progress silence deadline has passed."
            next_wait_ms = 0
        else:
            decision = "continue_waiting_no_repeat_ping"
            reason = "pending status request exists and deadline has not passed."
            next_wait_ms = calculate_next_wait_ms(checked, deadline, progress_scan_interval)
    liveness["last_scan_snapshot"] = snapshot
    liveness["last_checked_at"] = checked
    liveness["last_decision"] = decision
    payload["updated_at"] = now_iso()
    result = {
        "decision": decision,
        "agent_id": agent_id,
        "checked_at": checked,
        "progress_anchor_at": liveness.get("progress_anchor_at") or anchor,
        "pending_status_request_at": liveness.get("pending_status_request_at"),
        "max_progress_silence_deadline_at": deadline,
        "next_wait_ms": next_wait_ms,
        "progress_sources": progress_sources,
        "artifact": str(agent_assignment_path(task_dir)),
        "reason": reason,
    }
    return result, snapshot


def git_object_exists(root: Path, ref: str) -> bool:
    if not ref:
        return False
    return run(["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"], cwd=root, check=False).returncode == 0


def validate_head_field(root: Path, value: Any, label: str, errors: list[str], require_current: bool = False) -> None:
    head = str(value or "").strip()
    if not head:
        errors.append(f"agent-assignment.json 缺少 {label}。")
        return
    if not git_object_exists(root, head):
        errors.append(f"agent-assignment.json {label} 不是可解析的 Git commit: {head}。")
        return
    if require_current and head != current_head(root):
        errors.append(f"agent-assignment.json {label} {head} 与当前 HEAD {current_head(root)} 不一致。")


def validate_timestamp_field(value: Any, label: str, errors: list[str], required: bool = True) -> None:
    text = str(value or "").strip()
    if not text:
        if required:
            errors.append(f"agent-assignment.json 缺少 {label}。")
        return
    normalized = text.removesuffix("Z") + "+00:00" if text.endswith("Z") else text
    try:
        datetime.fromisoformat(normalized)
    except ValueError:
        errors.append(f"agent-assignment.json {label} 必须是 ISO-8601 时间: {text}。")


def validate_review_round_report_digest(root: Path, task_dir: Path, item: dict[str, Any], label: str) -> list[str]:
    entry = migrated_archive_digest_entry(root, task_dir, review_round_report_digest_entry(item)) or review_round_report_digest_entry(item)
    errors: list[str] = []
    path_value = str(entry.get("path") or "").strip()
    if path_value:
        path = resolve_repo_path(root, path_value)
        errors.extend(raw_review_report_path_errors(root, task_dir, path, f"{label}.review_report_path"))
    errors.extend(digest_errors(root, entry, f"{label} raw review report"))
    return errors


def validate_liveness_payload_errors(root: Path, payload: dict[str, Any], enforce_recovery_chains: bool = True) -> list[str]:
    errors: list[str] = []
    liveness = payload.get("liveness")
    if not isinstance(liveness, dict):
        errors.append("agent-assignment.json liveness 必须是对象。")
    agents_by_id = {
        str(item.get("agent_id") or "").strip(): item
        for item in payload.get("agents", [])
        if isinstance(item, dict) and str(item.get("agent_id") or "").strip()
    }
    status_events = payload.get("status_events")
    if not isinstance(status_events, list):
        return ["agent-assignment.json status_events 必须是数组。"]
    seen_event_ids: set[str] = set()
    for index, item in enumerate(status_events):
        if not isinstance(item, dict):
            errors.append(f"agent-assignment.json status_events[{index}] 必须是对象。")
            continue
        event_name = str(item.get("event") or "").strip()
        event_id = str(item.get("event_id") or "").strip()
        agent_id = str(item.get("agent_id") or "").strip()
        if not event_id:
            errors.append(f"agent-assignment.json status_events[{index}] 缺少 event_id。")
        elif event_id in seen_event_ids:
            errors.append(f"agent-assignment.json status_events[{index}].event_id 重复: {event_id}。")
        seen_event_ids.add(event_id)
        if event_name not in ALLOWED_AGENT_STATUS_EVENTS:
            errors.append(f"agent-assignment.json status_events[{index}].event 非法: {event_name or '(missing)'}。")
        role = str(item.get("logical_role") or "").strip()
        if role not in ALLOWED_LOGICAL_ROLES:
            errors.append(f"agent-assignment.json status_events[{index}].logical_role 非法: {role or '(missing)'}。")
        if not agent_id:
            errors.append(f"agent-assignment.json status_events[{index}] 缺少 agent_id 字段。")
        elif event_name != "assigned" and agent_id not in agents_by_id:
            errors.append(f"agent-assignment.json status_events[{index}].agent_id 未在 agents[] 中登记: {agent_id}。")
        if "platform_nickname" not in item:
            errors.append(f"agent-assignment.json status_events[{index}] 缺少 platform_nickname 字段。")
        validate_head_field(root, item.get("head"), f"status_events[{index}].head", errors)
        validate_timestamp_field(item.get("observed_at"), f"status_events[{index}].observed_at", errors)
        validate_timestamp_field(item.get("recorded_at"), f"status_events[{index}].recorded_at", errors)
        source = str(item.get("source") or "").strip()
        if source not in AGENT_STATUS_EVENT_SOURCES:
            errors.append(f"agent-assignment.json status_events[{index}].source 非法。")
        if evidence_is_placeholder(str(item.get("evidence") or "")):
            errors.append(f"agent-assignment.json status_events[{index}] 缺少非占位 evidence。")
        predecessor_agent_id = str(item.get("predecessor_agent_id") or "").strip()
        predecessor_event_id = str(item.get("predecessor_event_id") or "").strip()
        termination_reason = str(item.get("termination_reason") or "").strip()
        termination_source_event_id = str(item.get("termination_source_event_id") or "").strip()
        replacement_reason = str(item.get("replacement_reason") or "").strip()
        handoff_summary = str(item.get("handoff_summary") or "").strip()
        try:
            if event_name == "resume-same-agent":
                if not predecessor_event_id or not handoff_summary:
                    errors.append(f"agent-assignment.json status_events[{index}] resume-same-agent 缺少 predecessor_event_id 或 handoff_summary。")
                else:
                    validate_resume_reference(payload, agent_id, predecessor_event_id)
                if predecessor_agent_id or termination_reason or termination_source_event_id or replacement_reason:
                    errors.append(f"agent-assignment.json status_events[{index}] resume-same-agent 包含不应出现的结构化字段。")
            elif event_name == "replacement-started":
                if not predecessor_agent_id or not predecessor_event_id or not replacement_reason or not handoff_summary:
                    errors.append(f"agent-assignment.json status_events[{index}] replacement-started 缺少 predecessor/reason/handoff 字段。")
                else:
                    validate_replacement_reference(payload, agent_id, predecessor_agent_id, predecessor_event_id, replacement_reason)
                if termination_reason or termination_source_event_id:
                    errors.append(f"agent-assignment.json status_events[{index}] replacement-started 不得包含 termination 字段。")
            elif event_name == "terminated-unfinished":
                if not termination_reason or not handoff_summary:
                    errors.append(f"agent-assignment.json status_events[{index}] terminated-unfinished 缺少 termination_reason 或 handoff_summary。")
                else:
                    validate_termination_reference(payload, agent_id, termination_reason, termination_source_event_id)
                if predecessor_agent_id or predecessor_event_id or replacement_reason:
                    errors.append(f"agent-assignment.json status_events[{index}] terminated-unfinished 包含不应出现的 predecessor/replacement 字段。")
            elif event_name and event_name not in {"replacement-started", "resume-same-agent", "terminated-unfinished"}:
                unexpected = [
                    predecessor_agent_id,
                    predecessor_event_id,
                    termination_reason,
                    termination_source_event_id,
                    replacement_reason,
                    handoff_summary,
                ]
                if any(unexpected):
                    errors.append(f"agent-assignment.json status_events[{index}] {event_name} 包含不应出现的结构化字段。")
        except WorkflowError as exc:
            errors.append(f"agent-assignment.json status_events[{index}] {exc}")

    if enforce_recovery_chains:
        errors.extend(status_event_completion_errors(payload))
    if isinstance(liveness, dict):
        for agent_id, entry in liveness.items():
            if not isinstance(entry, dict):
                errors.append(f"agent-assignment.json liveness[{agent_id}] 必须是对象。")
                continue
            snapshot = entry.get("last_scan_snapshot")
            if snapshot is not None and not isinstance(snapshot, dict):
                errors.append(f"agent-assignment.json liveness[{agent_id}].last_scan_snapshot 必须是对象。")
                continue
            if isinstance(snapshot, dict):
                missing = [field for field in AGENT_LIVENESS_SNAPSHOT_FIELDS if field not in snapshot]
                if missing:
                    errors.append(f"agent-assignment.json liveness[{agent_id}].last_scan_snapshot 缺少字段: {', '.join(missing)}。")
            decision = str(entry.get("last_decision") or "")
            if decision and decision not in AGENT_LIVENESS_DECISIONS:
                errors.append(f"agent-assignment.json liveness[{agent_id}].last_decision 非法: {decision}。")
            if entry.get("progress_anchor_at"):
                validate_timestamp_field(entry.get("progress_anchor_at"), f"liveness[{agent_id}].progress_anchor_at", errors)
            if entry.get("last_checked_at"):
                validate_timestamp_field(entry.get("last_checked_at"), f"liveness[{agent_id}].last_checked_at", errors)
            if entry.get("pending_status_request_at"):
                validate_timestamp_field(entry.get("pending_status_request_at"), f"liveness[{agent_id}].pending_status_request_at", errors)
    return errors


def validate_agent_assignment_payload(
    root: Path,
    task_dir: Path,
    payload: dict[str, Any],
    require_current_head: bool = False,
    enforce_recovery_chains: bool = True,
) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != AGENT_ASSIGNMENT_SCHEMA_VERSION:
        errors.append(f"agent-assignment.json schema_version 必须是 {AGENT_ASSIGNMENT_SCHEMA_VERSION}。")
    if payload.get("task") != repo_relative(root, task_dir):
        errors.append(f"agent-assignment.json task 必须是 {repo_relative(root, task_dir)}。")
    validate_head_field(root, payload.get("head"), "head", errors, require_current=require_current_head)

    agents = payload.get("agents")
    if not isinstance(agents, list):
        errors.append("agent-assignment.json agents 必须是数组。")
    else:
        for index, item in enumerate(agents):
            if not isinstance(item, dict):
                errors.append(f"agent-assignment.json agents[{index}] 必须是对象。")
                continue
            role = str(item.get("logical_role") or "").strip()
            if role not in ALLOWED_LOGICAL_ROLES:
                errors.append(f"agent-assignment.json agents[{index}].logical_role 非法: {role or '(missing)'}。")
            if "agent_id" not in item:
                errors.append(f"agent-assignment.json agents[{index}] 缺少 agent_id 字段。")
            if "platform_nickname" not in item:
                errors.append(f"agent-assignment.json agents[{index}] 缺少 platform_nickname 字段。")
            if not str(item.get("reason") or "").strip():
                errors.append(f"agent-assignment.json agents[{index}] 缺少 reason。")
            validate_head_field(root, item.get("assigned_head"), f"agents[{index}].assigned_head", errors)

    rounds = payload.get("review_rounds")
    if not isinstance(rounds, list):
        errors.append("agent-assignment.json review_rounds 必须是数组。")
    else:
        seen_round_numbers: set[int] = set()
        previous_round_number = 0
        for index, item in enumerate(rounds):
            if not isinstance(item, dict):
                errors.append(f"agent-assignment.json review_rounds[{index}] 必须是对象。")
                continue
            role = str(item.get("logical_role") or "").strip()
            if role not in ALLOWED_LOGICAL_ROLES:
                errors.append(f"agent-assignment.json review_rounds[{index}].logical_role 非法: {role or '(missing)'}。")
            round_value = item.get("round")
            if not isinstance(round_value, int) or isinstance(round_value, bool) or round_value <= 0:
                errors.append(f"agent-assignment.json review_rounds[{index}].round 必须是正整数。")
            else:
                if round_value in seen_round_numbers:
                    errors.append(f"agent-assignment.json review_rounds[{index}].round {round_value} 重复；review_rounds[].round 必须唯一。")
                if round_value <= previous_round_number:
                    errors.append(
                        f"agent-assignment.json review_rounds[{index}].round {round_value} 必须按记录顺序严格递增，"
                        f"上一轮是 {previous_round_number}。"
                    )
                seen_round_numbers.add(round_value)
                previous_round_number = round_value
            findings_count = item.get("findings_count")
            if not is_strict_int(findings_count) or findings_count < 0:
                errors.append(f"agent-assignment.json review_rounds[{index}].findings_count 必须是非负整数。")
            if str(item.get("reuse_decision") or "").strip() not in ALLOWED_REUSE_DECISIONS:
                errors.append(f"agent-assignment.json review_rounds[{index}].reuse_decision 非法。")
            if not str(item.get("reuse_policy") or "").strip():
                errors.append(f"agent-assignment.json review_rounds[{index}] 缺少 reuse_policy。")
            if "agent_id" not in item:
                errors.append(f"agent-assignment.json review_rounds[{index}] 缺少 agent_id 字段。")
            if "platform_nickname" not in item:
                errors.append(f"agent-assignment.json review_rounds[{index}] 缺少 platform_nickname 字段。")
            validate_head_field(root, item.get("reviewed_head"), f"review_rounds[{index}].reviewed_head", errors)
            errors.extend(
                validate_review_round_report_digest(
                    root,
                    task_dir,
                    item,
                    f"agent-assignment.json review_rounds[{index}]",
                )
            )

    decisions = payload.get("reuse_decisions")
    if not isinstance(decisions, list):
        errors.append("agent-assignment.json reuse_decisions 必须是数组。")
    else:
        for index, item in enumerate(decisions):
            if not isinstance(item, dict):
                errors.append(f"agent-assignment.json reuse_decisions[{index}] 必须是对象。")
                continue
            role = str(item.get("logical_role") or "").strip()
            if role not in ALLOWED_LOGICAL_ROLES:
                errors.append(f"agent-assignment.json reuse_decisions[{index}].logical_role 非法: {role or '(missing)'}。")
            if str(item.get("decision") or "").strip() not in ALLOWED_REUSE_DECISIONS:
                errors.append(f"agent-assignment.json reuse_decisions[{index}].decision 非法。")
            if not str(item.get("reason") or "").strip():
                errors.append(f"agent-assignment.json reuse_decisions[{index}] 缺少 reason。")
            for round_field in ["from_round", "to_round"]:
                if round_field in item and (not is_strict_int(item.get(round_field)) or item[round_field] <= 0):
                    errors.append(
                        f"agent-assignment.json reuse_decisions[{index}].{round_field} 必须是正 strict int。"
                    )
            validate_head_field(root, item.get("head"), f"reuse_decisions[{index}].head", errors)
    errors.extend(validate_liveness_payload_errors(root, payload, enforce_recovery_chains=enforce_recovery_chains))
    return errors


def normalize_agent_assignment_for_task(root: Path, task_dir: Path, payload: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    normalized["schema_version"] = AGENT_ASSIGNMENT_SCHEMA_VERSION
    normalized["task"] = normalized_archive_task_value(root, task_dir, normalized.get("task"))
    if not isinstance(normalized.get("agents"), list):
        normalized["agents"] = []
    if not isinstance(normalized.get("liveness"), dict):
        normalized["liveness"] = {}
    if not isinstance(normalized.get("review_rounds"), list):
        normalized["review_rounds"] = []
    if not isinstance(normalized.get("reuse_decisions"), list):
        normalized["reuse_decisions"] = []
    if not isinstance(normalized.get("status_events"), list):
        normalized["status_events"] = []
    return normalized


def summarize_agent_assignment(root: Path, task_dir: Path, path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    digest = file_digest(root, path)
    roles = sorted(
        {
            str(item.get("logical_role") or "").strip()
            for item in payload.get("agents", [])
            if isinstance(item, dict) and str(item.get("logical_role") or "").strip()
        }
        | {
            str(item.get("logical_role") or "").strip()
            for item in payload.get("review_rounds", [])
            if isinstance(item, dict) and str(item.get("logical_role") or "").strip()
        }
        | {
            str(item.get("logical_role") or "").strip()
            for item in payload.get("reuse_decisions", [])
            if isinstance(item, dict) and str(item.get("logical_role") or "").strip()
        }
        | {
            str(item.get("logical_role") or "").strip()
            for item in payload.get("status_events", [])
            if isinstance(item, dict) and str(item.get("logical_role") or "").strip()
        }
    )
    return {
        **digest,
        "schema_version": payload.get("schema_version"),
        "artifact_head": payload.get("head"),
        "roles": roles,
        "agents_count": len(payload.get("agents", [])) if isinstance(payload.get("agents"), list) else 0,
        "review_rounds_count": len(payload.get("review_rounds", [])) if isinstance(payload.get("review_rounds"), list) else 0,
        "reuse_decisions_count": len(payload.get("reuse_decisions", [])) if isinstance(payload.get("reuse_decisions"), list) else 0,
        "status_events_count": len(payload.get("status_events", [])) if isinstance(payload.get("status_events"), list) else 0,
        "task": repo_relative(root, task_dir),
        "notes": "platform_nickname 仅作展示；gate 判断使用 logical_role、agent_id、HEAD、digest 与 AI/human 记录的复用决策。",
    }


def review_reports_from_assignment(root: Path, task_dir: Path, payload: dict[str, Any]) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    rounds = payload.get("review_rounds")
    if not isinstance(rounds, list):
        return reports
    for item in rounds:
        if not isinstance(item, dict):
            continue
        digest = migrated_archive_digest_entry(root, task_dir, review_round_report_digest_entry(item)) or review_round_report_digest_entry(item)
        reports.append(
            {
                "round": item.get("round"),
                "logical_role": item.get("logical_role"),
                "agent_id": item.get("agent_id"),
                "reviewed_head": item.get("reviewed_head"),
                "findings_count": item.get("findings_count"),
                "path": digest.get("path"),
                "sha256": digest.get("sha256"),
                "size_bytes": digest.get("size_bytes"),
                "modified_at": digest.get("modified_at"),
            }
        )
    return reports


def current_findings_review_round_errors(root: Path, payload: dict[str, Any], expected_findings_count: int) -> list[str]:
    rounds = payload.get("review_rounds")
    if not isinstance(rounds, list):
        return ["agent-assignment.json review_rounds 必须是数组。"]
    current = current_head(root)
    for item in rounds:
        if not isinstance(item, dict):
            continue
        if str(item.get("reviewed_head") or "").strip() == current and item.get("findings_count") == expected_findings_count:
            return []
    return [
        "Branch Review Gate findings artifact 需要 agent-assignment.json 中存在一轮 reviewed_head="
        f"{current} 且 findings_count={expected_findings_count} 的 review_rounds[] raw report evidence。"
    ]


def review_rollup_link_errors(root: Path, task_dir: Path, review_report: dict[str, Any], review_reports: list[dict[str, Any]]) -> list[str]:
    path_value = str(review_report.get("path") or "").strip()
    if not path_value:
        return ["task-local review.md 缺少 path，无法校验 raw report 链接。"]
    report_path = resolve_repo_path(root, path_value)
    try:
        content = report_path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"无法读取 task-local review.md 校验 raw report 链接: {exc}。"]
    errors: list[str] = []
    for item in review_reports:
        raw_path_value = str(item.get("path") or "").strip()
        if not raw_path_value:
            continue
        raw_path = resolve_repo_path(root, raw_path_value)
        try:
            task_relative = raw_path.resolve().relative_to(task_dir.resolve()).as_posix()
        except ValueError:
            task_relative = ""
        if raw_path_value not in content and (not task_relative or task_relative not in content):
            errors.append(f"task-local review.md 必须链接 raw review report: {task_relative or raw_path_value}。")
    return errors


def normalized_review_report_template_line(line: str) -> str:
    value = line.strip()
    value = re.sub(r"^>+\s*", "", value)
    value = re.sub(r"^#{1,6}\s*", "", value)
    value = re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+)", "", value)
    value = value.strip().strip("#").strip()
    value = value.strip("`*_ ")
    return re.sub(r"\s+", " ", value).strip()


def forbidden_review_report_heading_match(line: str) -> str | None:
    normalized = normalized_review_report_template_line(line)
    if not normalized:
        return None
    folded = normalized.casefold()
    for heading in FORBIDDEN_REVIEW_REPORT_ENGLISH_TEMPLATE_HEADINGS:
        needle = heading.casefold()
        if folded == needle:
            return heading
        if folded.startswith((f"{needle}:", f"{needle} -", f"{needle} --", f"{needle} —", f"{needle} –")):
            return heading
    return None


def review_report_template_heading_errors_for_path(root: Path, path: Path, label: str) -> list[str]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{label} 无法读取以校验中文模板标题: {exc}。"]
    errors: list[str] = []
    in_fence = False
    for line_number, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = forbidden_review_report_heading_match(line)
        if heading:
            errors.append(
                f"{label} {repo_relative(root, path)} 第 {line_number} 行包含英文模板标题 `{heading}`；"
                "`review.md` / `reviews/*.md` 的 human-readable 标题和字段名必须中文。"
            )
    return errors


def review_report_language_template_errors(
    root: Path,
    task_dir: Path,
    review_report: Any,
    review_reports: Any,
) -> list[str]:
    entries: list[tuple[str, Path]] = []
    if isinstance(review_report, dict):
        normalized_report = migrated_archive_entry(root, task_dir, review_report, REVIEW_REPORT_ARTIFACT) or review_report
        path_value = str(normalized_report.get("path") or "").strip()
        if path_value:
            entries.append(("Branch Review Gate review_report", resolve_repo_path(root, path_value)))
    if isinstance(review_reports, list):
        for index, item in enumerate(review_reports):
            if not isinstance(item, dict):
                continue
            normalized_item = migrated_archive_digest_entry(root, task_dir, item) or item
            path_value = str(normalized_item.get("path") or "").strip()
            if path_value:
                entries.append((f"Branch Review Gate review_reports[{index}]", resolve_repo_path(root, path_value)))

    errors: list[str] = []
    seen: set[Path] = set()
    for label, path in entries:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        errors.extend(review_report_template_heading_errors_for_path(root, resolved, label))
    return errors


def is_strict_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def review_round_number(item: dict[str, Any]) -> int:
    value = item.get("round")
    if is_strict_int(value):
        return value
    return 0


def finding_round_has_replacement_closure(
    payload: dict[str, Any],
    rounds: list[Any],
    finding_round: dict[str, Any],
    final_round_number: int,
) -> bool:
    finding_agent = str(finding_round.get("agent_id") or "").strip()
    finding_round_number = review_round_number(finding_round)
    if not finding_agent or finding_round_number <= 0:
        return False
    decisions = payload.get("reuse_decisions")
    status_events = payload.get("status_events")
    if not isinstance(decisions, list) or not isinstance(status_events, list):
        return False
    events_by_id = {
        str(item.get("event_id") or "").strip(): item
        for item in status_events
        if isinstance(item, dict) and str(item.get("event_id") or "").strip()
    }
    closure_candidates = [
        item
        for item in rounds
        if isinstance(item, dict)
        and review_round_number(item) > finding_round_number
        and review_round_number(item) < final_round_number
        and str(item.get("logical_role") or "").strip() == "问题闭环审查代理"
        and str(item.get("agent_id") or "").strip()
        and str(item.get("agent_id") or "").strip() != finding_agent
        and is_strict_int(item.get("findings_count"))
        and item["findings_count"] == 0
        and str(item.get("reuse_decision") or "").strip() == "replace"
    ]
    for closure in closure_candidates:
        closure_agent = str(closure.get("agent_id") or "").strip()
        closure_round_number = review_round_number(closure)
        closure_head = str(closure.get("reviewed_head") or "").strip()
        matching_decision = any(
            isinstance(item, dict)
            and str(item.get("decision") or "").strip() == "replace"
            and is_strict_int(item.get("from_round"))
            and item["from_round"] == finding_round_number
            and is_strict_int(item.get("to_round"))
            and item["to_round"] == closure_round_number
            and str(item.get("agent_id") or "").strip() == closure_agent
            and str(item.get("logical_role") or "").strip() == "问题闭环审查代理"
            and str(item.get("head") or "").strip() == closure_head
            and str(item.get("reason") or "").strip()
            for item in decisions
        )
        status_event_indexes_by_id = {
            str(item.get("event_id") or "").strip(): index
            for index, item in enumerate(status_events)
            if isinstance(item, dict) and str(item.get("event_id") or "").strip()
        }
        replacement_start_entries = [
            (index, item)
            for index, item in enumerate(status_events)
            if isinstance(item, dict)
            and str(item.get("event") or "").strip() == "replacement-started"
            and str(item.get("agent_id") or "").strip() == closure_agent
            and str(item.get("predecessor_agent_id") or "").strip() == finding_agent
            and str(item.get("predecessor_event_id") or "").strip()
            and str(item.get("logical_role") or "").strip() == "问题闭环审查代理"
            and str(item.get("head") or "").strip() == closure_head
            and str(item.get("replacement_reason") or "").strip() in AGENT_REPLACEMENT_REASONS
            and str(item.get("handoff_summary") or "").strip()
        ]
        completion_indexes = [
            index
            for index, item in enumerate(status_events)
            if isinstance(item, dict)
            and str(item.get("event") or "").strip() == "completed"
            and str(item.get("agent_id") or "").strip() == closure_agent
            and str(item.get("logical_role") or "").strip() == "问题闭环审查代理"
            and str(item.get("head") or "").strip() == closure_head
        ]
        matching_recovery_chain = False
        for replacement_index, replacement_start in replacement_start_entries:
            predecessor_event_id = str(replacement_start.get("predecessor_event_id") or "").strip()
            predecessor_index = status_event_indexes_by_id.get(predecessor_event_id)
            predecessor_event = events_by_id.get(predecessor_event_id)
            if predecessor_index is None or not isinstance(predecessor_event, dict):
                continue
            if str(predecessor_event.get("agent_id") or "").strip() != finding_agent:
                continue
            if str(predecessor_event.get("event") or "").strip() not in {"failed", "stale-assessed", "terminated-unfinished"}:
                continue
            if any(predecessor_index < replacement_index < completion_index for completion_index in completion_indexes):
                matching_recovery_chain = True
                break
        if matching_decision and matching_recovery_chain:
            return True
    return False


def finding_round_has_new_agent_closure(
    payload: dict[str, Any],
    rounds: list[Any],
    finding_round: dict[str, Any],
    final_round_number: int,
) -> bool:
    finding_agent = str(finding_round.get("agent_id") or "").strip()
    finding_round_number = review_round_number(finding_round)
    if not finding_agent or finding_round_number <= 0:
        return False
    decisions = payload.get("reuse_decisions")
    if not isinstance(decisions, list):
        return False
    closure_candidates = [
        item
        for item in rounds
        if isinstance(item, dict)
        and review_round_number(item) > finding_round_number
        and review_round_number(item) < final_round_number
        and str(item.get("logical_role") or "").strip() == "问题闭环审查代理"
        and str(item.get("agent_id") or "").strip()
        and str(item.get("agent_id") or "").strip() != finding_agent
        and is_strict_int(item.get("findings_count"))
        and item["findings_count"] >= 0
        and str(item.get("reuse_decision") or "").strip() == "new-agent"
    ]
    for closure in closure_candidates:
        closure_agent = str(closure.get("agent_id") or "").strip()
        closure_round_number = review_round_number(closure)
        closure_head = str(closure.get("reviewed_head") or "").strip()
        if any(
            isinstance(item, dict)
            and review_round_number(item) < closure_round_number
            and str(item.get("agent_id") or "").strip() == closure_agent
            for item in rounds
        ):
            continue
        if any(
            isinstance(item, dict)
            and str(item.get("decision") or "").strip() == "new-agent"
            and is_strict_int(item.get("from_round"))
            and item["from_round"] == finding_round_number
            and is_strict_int(item.get("to_round"))
            and item["to_round"] == closure_round_number
            and str(item.get("agent_id") or "").strip() == closure_agent
            and str(item.get("logical_role") or "").strip() == "问题闭环审查代理"
            and str(item.get("head") or "").strip() == closure_head
            and str(item.get("reason") or "").strip()
            for item in decisions
        ):
            return True
    return False


def final_review_round_errors(root: Path, payload: dict[str, Any], expected_head: str | None = None) -> list[str]:
    rounds = payload.get("review_rounds")
    if not isinstance(rounds, list) or not rounds:
        return ["Branch Review Gate pass 需要 agent-assignment.json 记录最终放行审查轮次。"]
    errors: list[str] = []
    seen_round_numbers: set[int] = set()
    previous_round_number = 0
    for index, item in enumerate(rounds):
        if not isinstance(item, dict):
            continue
        value = item.get("round")
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            continue
        if value in seen_round_numbers:
            errors.append(f"review_rounds[{index}].round {value} 重复；无法证明最终放行审查代理是唯一最后一轮。")
        if value <= previous_round_number:
            errors.append(
                f"review_rounds[{index}].round {value} 未按记录顺序严格递增；"
                f"无法证明最终放行审查代理是最后一轮。"
            )
        seen_round_numbers.add(value)
        previous_round_number = value
    final_rounds = [
        item
        for item in rounds
        if isinstance(item, dict) and str(item.get("logical_role") or "").strip() == "最终放行审查代理"
    ]
    if not final_rounds:
        errors.append("Branch Review Gate pass 需要 logical_role=最终放行审查代理 的 review_rounds[] 记录。")
        return errors
    final_round = max(final_rounds, key=review_round_number)
    current = expected_head or current_head(root)
    final_round_number = review_round_number(final_round)
    final_agent = str(final_round.get("agent_id") or "").strip()
    reviewed_head = str(final_round.get("reviewed_head") or "").strip()
    later_rounds = [
        str(item.get("round") or index)
        for index, item in enumerate(rounds)
        if isinstance(item, dict) and review_round_number(item) > final_round_number
    ]
    if later_rounds:
        errors.append("最终放行审查代理必须是最后一轮 review_rounds[]；后续轮次: " + ", ".join(later_rounds) + "。")
    if reviewed_head != current:
        errors.append(f"最终放行审查代理 reviewed_head {reviewed_head or '(missing)'} 与当前 HEAD {current} 不一致。")
    final_findings_count = final_round.get("findings_count")
    if not is_strict_int(final_findings_count) or final_findings_count != 0:
        errors.append("最终放行审查代理 findings_count 必须为明确整数 0。")
    if str(final_round.get("reuse_decision") or "").strip() != "new-agent":
        errors.append("最终放行审查代理 reuse_decision 必须是 new-agent，不能复用问题发现/闭环审查代理。")
    if not final_agent:
        errors.append("最终放行审查代理缺少 agent_id。")
    earlier_review_agents = {
        str(item.get("agent_id") or "").strip()
        for item in rounds
        if isinstance(item, dict)
        and review_round_number(item) < final_round_number
        and str(item.get("agent_id") or "").strip()
    }
    finding_owner_agents = {
        str(item.get("agent_id") or "").strip()
        for item in rounds
        if isinstance(item, dict)
        and item is not final_round
        and is_strict_int(item.get("findings_count"))
        and item["findings_count"] > 0
        and str(item.get("agent_id") or "").strip()
    }
    replacement_closure_agents = {
        str(item.get("agent_id") or "").strip()
        for item in rounds
        if isinstance(item, dict)
        and item is not final_round
        and str(item.get("logical_role") or "").strip() == "问题闭环审查代理"
        and str(item.get("reuse_decision") or "").strip() == "replace"
        and str(item.get("agent_id") or "").strip()
    }
    closure_agents = {
        str(item.get("agent_id") or "").strip()
        for item in rounds
        if isinstance(item, dict)
        and item is not final_round
        and str(item.get("logical_role") or "").strip() == "问题闭环审查代理"
        and str(item.get("agent_id") or "").strip()
    }
    missing_finding_owner_agent_rounds = [
        str(item.get("round") or index)
        for index, item in enumerate(rounds)
        if isinstance(item, dict)
        and item is not final_round
        and is_strict_int(item.get("findings_count"))
        and item["findings_count"] > 0
        and not str(item.get("agent_id") or "").strip()
    ]
    if missing_finding_owner_agent_rounds:
        errors.append(
            "发现过 finding 的 review_rounds[] 必须记录 agent_id，无法证明最终放行审查代理 fresh；缺失轮次: "
            + ", ".join(missing_finding_owner_agent_rounds)
            + "。"
        )
    finding_rounds = [
        item
        for item in rounds
        if isinstance(item, dict)
        and item is not final_round
        and is_strict_int(item.get("findings_count"))
        and item["findings_count"] > 0
        and str(item.get("agent_id") or "").strip()
    ]
    for finding_round in finding_rounds:
        finding_agent = str(finding_round.get("agent_id") or "").strip()
        finding_round_number = review_round_number(finding_round)
        closure_candidates = [
            item
            for item in rounds
            if isinstance(item, dict)
            and review_round_number(item) > finding_round_number
            and review_round_number(item) < final_round_number
            and str(item.get("logical_role") or "").strip() == "问题闭环审查代理"
            and str(item.get("agent_id") or "").strip() == finding_agent
            and is_strict_int(item.get("findings_count"))
            and item["findings_count"] == 0
            and str(item.get("reuse_decision") or "").strip() == "reuse-for-closure"
        ]
        has_explicit_new_agent_closure = finding_round_has_new_agent_closure(
            payload,
            rounds,
            finding_round,
            final_round_number,
        )
        if (
            not closure_candidates
            and not has_explicit_new_agent_closure
            and not finding_round_has_replacement_closure(payload, rounds, finding_round, final_round_number)
        ):
            errors.append(
                "发现过 finding 的 review agent 必须先以问题闭环审查代理复审并给出 0 findings，"
                "或由不同的新问题闭环审查代理通过 new-agent reuse_decision 的明确 from_round/to_round 关系闭环，"
                "或在原 agent 失败/中断时记录完整 replacement-started、replace reuse_decision 与 completed 替代闭环链，"
                f"然后才能启动新的最终放行审查代理；缺少闭环轮次: round {finding_round.get('round') or finding_round_number} agent {finding_agent}。"
            )
    if final_agent and final_agent in finding_owner_agents:
        errors.append("发现过 finding 的 review agent 只能做问题闭环确认，不能作为最终放行审查代理。")
    if final_agent and final_agent in replacement_closure_agents:
        errors.append("替代 finding closure 的 review agent 只能做问题闭环确认，不能作为最终放行审查代理。")
    elif final_agent and final_agent in closure_agents:
        errors.append("finding closure 的 review agent 只能做问题闭环确认，不能作为最终放行审查代理。")
    if final_agent and final_agent in earlier_review_agents:
        errors.append("最终放行审查代理必须使用未在任何更早 review_rounds[] 出现过的 fresh agent_id。")
    return errors


def status_event_completion_errors(payload: dict[str, Any]) -> list[str]:
    status_events = payload.get("status_events")
    if not isinstance(status_events, list):
        return ["agent-assignment.json status_events 必须是数组。"]
    errors: list[str] = []
    events_by_id = {
        str(item.get("event_id") or ""): item
        for item in status_events
        if isinstance(item, dict) and str(item.get("event_id") or "")
    }

    def recovery_completed_from(index: int, original_agent: str, predecessor_event_id: str, allow_resume: bool) -> bool:
        visited: set[tuple[int, str, str, bool]] = set()

        def active_agent_completes_or_recovers(start_index: int, active_agent: str) -> bool:
            for later_index, later in enumerate(status_events[start_index + 1:], start=start_index + 1):
                if not isinstance(later, dict):
                    continue
                later_event = str(later.get("event") or "").strip()
                later_agent = str(later.get("agent_id") or "").strip()
                later_event_id = str(later.get("event_id") or "").strip()
                if later_agent != active_agent:
                    continue
                if later_event == "completed":
                    return True
                if later_event == "failed":
                    return recover_from_event(later_index, active_agent, later_event_id, allow_same_agent_resume=True)
                if later_event == "terminated-unfinished":
                    reason = str(later.get("termination_reason") or "").strip()
                    if reason == "manual_or_platform_terminated_unfinished":
                        return recover_from_event(later_index, active_agent, later_event_id, allow_same_agent_resume=True)
                    # stale_cutover is recovered through its source stale-assessed event.
                    continue
                if later_event == "stale-assessed":
                    return recover_from_event(later_index, active_agent, later_event_id, allow_same_agent_resume=False)
            return False

        def recover_from_event(start_index: int, source_agent: str, source_event_id: str, allow_same_agent_resume: bool) -> bool:
            if not source_agent or not source_event_id:
                return False
            key = (start_index, source_agent, source_event_id, allow_same_agent_resume)
            if key in visited:
                return False
            visited.add(key)
            for later_index, later in enumerate(status_events[start_index + 1:], start=start_index + 1):
                if not isinstance(later, dict):
                    continue
                later_event = str(later.get("event") or "").strip()
                later_agent = str(later.get("agent_id") or "").strip()
                if (
                    allow_same_agent_resume
                    and later_event == "resume-same-agent"
                    and later_agent == source_agent
                    and str(later.get("predecessor_event_id") or "").strip() == source_event_id
                ):
                    if active_agent_completes_or_recovers(later_index, later_agent):
                        return True
                if (
                    later_event == "replacement-started"
                    and str(later.get("predecessor_agent_id") or "").strip() == source_agent
                    and str(later.get("predecessor_event_id") or "").strip() == source_event_id
                    and later_agent
                ):
                    if active_agent_completes_or_recovers(later_index, later_agent):
                        return True
            return False

        return recover_from_event(index, original_agent, predecessor_event_id, allow_resume)

    for index, item in enumerate(status_events):
        if not isinstance(item, dict):
            continue
        event_name = str(item.get("event") or "").strip()
        agent_id = str(item.get("agent_id") or "").strip()
        event_id = str(item.get("event_id") or "").strip()
        if event_name == "stale-assessed":
            stale_cutover = [
                later
                for later in status_events[index + 1:]
                if isinstance(later, dict)
                and str(later.get("event") or "") == "terminated-unfinished"
                and str(later.get("agent_id") or "") == agent_id
                and str(later.get("termination_reason") or "") == "stale_cutover"
                and str(later.get("termination_source_event_id") or "") == event_id
            ]
            if not stale_cutover:
                errors.append(f"status_events[{index}] stale-assessed 后缺少 terminated-unfinished stale_cutover。")
            stale_resume = [
                later
                for later in status_events[index + 1:]
                if isinstance(later, dict)
                and str(later.get("event") or "") == "resume-same-agent"
                and str(later.get("agent_id") or "") == agent_id
            ]
            if stale_resume:
                errors.append(f"status_events[{index}] stale-assessed 后不得 resume-same-agent。")
            if not recovery_completed_from(index, agent_id, event_id, allow_resume=False):
                errors.append(f"status_events[{index}] stale-assessed 的 replacement chain 缺少后续 replacement completed。")
        if event_name == "terminated-unfinished":
            reason = str(item.get("termination_reason") or "").strip()
            if reason == "stale_cutover":
                source_id = str(item.get("termination_source_event_id") or "").strip()
                if source_id not in events_by_id:
                    errors.append(f"status_events[{index}] stale_cutover termination_source_event_id 未引用已有 stale-assessed。")
                continue
            if not recovery_completed_from(index, agent_id, event_id, allow_resume=True):
                errors.append(
                    f"status_events[{index}] terminated-unfinished 后缺少 same-agent resume 或 replacement 且后续 completed 的完整恢复链。"
                )
        if event_name == "failed":
            if not recovery_completed_from(index, agent_id, event_id, allow_resume=True):
                errors.append(
                    f"status_events[{index}] failed 后缺少 same-agent resume 或 replacement 且后续 completed 的完整恢复链。"
                )
    return errors


def validate_agent_assignment(
    root: Path,
    task_dir: Path,
    assignment_arg: str | None = None,
    require_current_head: bool = False,
) -> tuple[Path, dict[str, Any], list[str], dict[str, Any]]:
    path = resolve_task_local_path(root, task_dir, assignment_arg) if assignment_arg else agent_assignment_path(task_dir)
    if not path.exists():
        raise WorkflowError(f"Agent assignment artifact not found: {path}", exit_code=2)
    payload = normalize_agent_assignment_for_task(root, task_dir, read_json(path))
    errors = validate_agent_assignment_payload(root, task_dir, payload, require_current_head=require_current_head)
    summary = summarize_agent_assignment(root, task_dir, path, payload) if not errors else {}
    return path, payload, errors, summary


def digest_errors(root: Path, entry: Any, label: str, require_modified_at_match: bool = False) -> list[str]:
    if not isinstance(entry, dict):
        return [f"{label} 中存在非对象 artifact entry。"]
    errors: list[str] = []
    path_value = str(entry.get("path") or "").strip()
    if not path_value:
        return [f"{label} artifact entry 缺少 path。"]
    path = resolve_repo_path(root, path_value)
    if not path.exists() or not path.is_file():
        return [f"{label} artifact 不存在或不是文件: {path_value}。"]
    current = file_digest(root, path)
    for key in ["sha256", "size_bytes", "modified_at"]:
        value = entry.get(key)
        if key not in entry or value is None or value == "":
            errors.append(f"{label} artifact 缺少 {key}: {path_value}。")
    for key in ["sha256", "size_bytes"]:
        if entry.get(key) != current.get(key):
            errors.append(f"{label} artifact 已过期: {path_value} 的 {key} 不匹配。")
    if (
        require_modified_at_match
        and entry.get("modified_at")
        and entry.get("modified_at") != current.get("modified_at")
    ):
        errors.append(f"{label} artifact 已过期: {path_value} 的 modified_at 不匹配。")
    return errors


def default_existing_task_artifacts(task_dir: Path, names: list[str]) -> list[str]:
    artifacts: list[str] = []
    for name in names:
        if (task_dir / name).is_file():
            artifacts.append(name)
    return artifacts


def dirty_paths_excluding(root: Path, excluded: set[str]) -> list[str]:
    return [
        path
        for path in git_status_paths(root)
        if path not in excluded
    ]


def task_dir_is_archived(root: Path, task_dir: Path) -> bool:
    try:
        task_dir.resolve().relative_to((tasks_root(root) / "archive").resolve())
        return True
    except ValueError:
        return False


def active_task_relative_for_archive(root: Path, task_dir: Path) -> str | None:
    if not task_dir_is_archived(root, task_dir):
        return None
    return (tasks_root(root) / task_dir.name).relative_to(root).as_posix()


def migrated_archive_entry(root: Path, task_dir: Path, entry: Any, expected_name: str) -> dict[str, Any] | None:
    if not isinstance(entry, dict):
        return None
    active_task = active_task_relative_for_archive(root, task_dir)
    if active_task is None:
        return None
    path_value = str(entry.get("path") or "").strip()
    if not path_value:
        return None
    expected_active_path = f"{active_task}/{expected_name}"
    if path_value != expected_active_path:
        return None
    archived_path = task_dir / expected_name
    if not archived_path.is_file():
        return None
    migrated = dict(entry)
    migrated.update(file_digest(root, archived_path))
    return migrated


def migrated_archive_digest_entry(root: Path, task_dir: Path, entry: Any) -> dict[str, Any] | None:
    if not isinstance(entry, dict):
        return None
    active_task = active_task_relative_for_archive(root, task_dir)
    if active_task is None:
        return None
    path_value = str(entry.get("path") or "").strip()
    if not path_value or not path_value.startswith(f"{active_task}/"):
        return None
    relative_name = path_value.removeprefix(f"{active_task}/")
    if not relative_name or relative_name.startswith("/") or ".." in relative_name.split("/"):
        return None
    if "/" in relative_name:
        parts = relative_name.split("/")
        if not (len(parts) == 2 and parts[0] == REVIEW_ROUND_REPORT_DIR and parts[1].endswith(".md") and parts[1]):
            return None
    archived_path = task_dir / relative_name
    if not archived_path.is_file():
        return None
    migrated = dict(entry)
    migrated.update(file_digest(root, archived_path))
    return migrated


def normalized_digest_entry(root: Path, task_dir: Path, entry: Any) -> Any:
    return migrated_archive_digest_entry(root, task_dir, entry) or entry


def normalized_archive_task_value(root: Path, task_dir: Path, value: Any) -> Any:
    active_task = active_task_relative_for_archive(root, task_dir)
    if active_task is None or value != active_task:
        return value
    return repo_relative(root, task_dir)


def planning_approval_path(task_dir: Path) -> Path:
    return task_dir / PLANNING_APPROVAL_ARTIFACT


def phase2_check_path(task_dir: Path) -> Path:
    return task_dir / PHASE2_CHECK_ARTIFACT


def valid_review_report_fields(root: Path, task_dir: Path, review_report: Any) -> list[str]:
    if not isinstance(review_report, dict):
        return ["Branch Review Gate 缺少 review_report；passed gate 必须引用 task-local review.md digest。"]
    review_report = migrated_archive_entry(root, task_dir, review_report, REVIEW_REPORT_ARTIFACT) or review_report
    errors: list[str] = []
    for key in ["path", "sha256", "size_bytes", "modified_at"]:
        if not review_report.get(key):
            errors.append(f"Branch Review Gate review_report 缺少 {key}。")
    path_value = str(review_report.get("path") or "").strip()
    if path_value:
        path = resolve_repo_path(root, path_value).resolve()
        if task_dir.resolve() not in [path, *path.parents]:
            errors.append("Branch Review Gate review_report 必须指向当前 task-local review.md。")
        if path.name != REVIEW_REPORT_ARTIFACT:
            errors.append("Branch Review Gate review_report 必须指向 task-local review.md。")
    if not errors:
        errors.extend(digest_errors(root, review_report, "Branch Review Gate review_report"))
    return errors


def valid_agent_assignment_summary_fields(
    root: Path,
    task_dir: Path,
    agent_assignment: Any,
    expected_head: str | None = None,
) -> list[str]:
    if not isinstance(agent_assignment, dict) or not agent_assignment:
        return ["Branch Review Gate 缺少 agent_assignment；passed gate 必须记录 fresh 最终放行审查代理的 agent-assignment.json digest。"]
    agent_assignment = migrated_archive_entry(root, task_dir, agent_assignment, AGENT_ASSIGNMENT_ARTIFACT) or agent_assignment
    errors: list[str] = []
    errors.extend(digest_errors(root, agent_assignment, "Branch Review Gate agent_assignment"))
    path_value = str(agent_assignment.get("path") or "").strip()
    if not path_value:
        errors.append("Branch Review Gate agent_assignment 缺少 path。")
        return errors
    path = resolve_repo_path(root, path_value).resolve()
    if task_dir.resolve() not in [path, *path.parents]:
        errors.append("Branch Review Gate agent_assignment 必须指向当前 task-local agent-assignment.json。")
        return errors
    if path.name != AGENT_ASSIGNMENT_ARTIFACT:
        errors.append("Branch Review Gate agent_assignment 必须指向 task-local agent-assignment.json。")
        return errors
    try:
        payload = read_json(path)
    except WorkflowError as exc:
        errors.append(str(exc))
        return errors
    payload = normalize_agent_assignment_for_task(root, task_dir, payload)
    errors.extend(validate_agent_assignment_payload(root, task_dir, payload, require_current_head=False))
    errors.extend(final_review_round_errors(root, payload, expected_head=expected_head))
    errors.extend(status_event_completion_errors(payload))
    roles = agent_assignment.get("roles")
    if not isinstance(roles, list) or not roles:
        errors.append("Branch Review Gate agent_assignment 缺少 roles 摘要。")
    else:
        invalid_roles = [str(role) for role in roles if str(role) not in ALLOWED_LOGICAL_ROLES]
        if invalid_roles:
            errors.append("Branch Review Gate agent_assignment roles 存在非法中文逻辑角色: " + ", ".join(invalid_roles) + "。")
    for key in ["agents_count", "review_rounds_count", "reuse_decisions_count", "status_events_count"]:
        if key in agent_assignment and (not isinstance(agent_assignment.get(key), int) or agent_assignment[key] < 0):
            errors.append(f"Branch Review Gate agent_assignment.{key} 必须是非负整数。")
    return errors


def valid_review_reports_summary_fields(
    root: Path,
    task_dir: Path,
    review_reports: Any,
    assignment_payload: dict[str, Any] | None = None,
) -> list[str]:
    if not isinstance(review_reports, list) or not review_reports:
        return ["Branch Review Gate 缺少 verification_evidence.review_reports[] raw report digest 摘要。"]
    errors: list[str] = []
    for index, item in enumerate(review_reports):
        if not isinstance(item, dict):
            errors.append(f"Branch Review Gate review_reports[{index}] 必须是对象。")
            continue
        for key in ["round", "logical_role", "agent_id", "reviewed_head", "findings_count", "path", "sha256", "size_bytes", "modified_at"]:
            if item.get(key) in (None, ""):
                errors.append(f"Branch Review Gate review_reports[{index}] 缺少 {key}。")
        if not is_strict_int(item.get("round")) or int(item.get("round") or 0) <= 0:
            errors.append(f"Branch Review Gate review_reports[{index}].round 必须是正整数。")
        findings_count = item.get("findings_count")
        if not is_strict_int(findings_count) or findings_count < 0:
            errors.append(f"Branch Review Gate review_reports[{index}].findings_count 必须是非负整数。")
        role = str(item.get("logical_role") or "").strip()
        if role and role not in ALLOWED_LOGICAL_ROLES:
            errors.append(f"Branch Review Gate review_reports[{index}].logical_role 非法: {role}。")
        normalized_item = migrated_archive_digest_entry(root, task_dir, item) or item
        path_value = str(normalized_item.get("path") or "").strip()
        if path_value:
            path = resolve_repo_path(root, str(normalized_item.get("path") or ""))
            errors.extend(raw_review_report_path_errors(root, task_dir, path, f"Branch Review Gate review_reports[{index}].path"))
            errors.extend(digest_errors(root, normalized_item, f"Branch Review Gate review_reports[{index}]"))
    if assignment_payload is not None and isinstance(assignment_payload.get("review_rounds"), list):
        expected = review_reports_from_assignment(root, task_dir, assignment_payload)
        actual_by_round = {
            item.get("round"): migrated_archive_digest_entry(root, task_dir, item) or item
            for item in review_reports
            if isinstance(item, dict) and is_strict_int(item.get("round"))
        }
        if len(review_reports) != len(expected):
            errors.append(
                f"Branch Review Gate review_reports[] 数量 {len(review_reports)} 与 agent-assignment.json review_rounds[] 数量 {len(expected)} 不一致。"
            )
        for expected_item in expected:
            round_value = expected_item.get("round")
            actual = actual_by_round.get(round_value)
            if actual is None:
                errors.append(f"Branch Review Gate review_reports[] 缺少 round {round_value} 的 raw report 摘要。")
                continue
            for key in ["logical_role", "agent_id", "reviewed_head", "findings_count", "path", "sha256", "size_bytes", "modified_at"]:
                if actual.get(key) != expected_item.get(key):
                    errors.append(f"Branch Review Gate review_reports[] round {round_value} 的 {key} 与 agent-assignment.json 不一致。")
    return errors


def reviewer_identity_errors(reviewer: str) -> list[str]:
    value = reviewer.strip()
    if not value:
        return ["Branch Review Gate 缺少 reviewer identity。"]
    if any(pattern.search(value) for pattern in SELF_REVIEWER_PATTERNS):
        return [
            "Branch Review Gate reviewer 不能是 main-session / self-review；通过门禁必须基于独立 Agent 审查。",
        ]
    return []


def independent_review_source_errors(review_source: str, reviewer: str) -> list[str]:
    errors: list[str] = []
    if review_source != INDEPENDENT_REVIEW_SOURCE:
        errors.append(
            f"Branch Review Gate review_source 必须是 {INDEPENDENT_REVIEW_SOURCE}；脚本 gate 只能记录独立 Agent 审查后的结果。",
        )
    errors.extend(reviewer_identity_errors(reviewer))
    return errors


def blocking_findings(findings: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
    block = {str(item).upper() for item in review_gate_config(config).get("block_priorities", ["P0", "P1", "P2", "P3"])}
    return [finding for finding in findings if str(finding.get("priority") or "").upper() in block]


def review_gate_blocking_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return list(findings)


def unresolved_blocking_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    for finding in findings:
        priority = str(finding.get("priority") or "").upper()
        status = str(finding.get("status") or "").strip().lower()
        if priority in BLOCKING_PRIORITIES and status not in RESOLVED_FINDING_STATUSES:
            blockers.append(finding)
    return blockers


def planning_ambiguity_scan_paths(task_dir: Path) -> list[Path]:
    return [task_dir / name for name in PLANNING_AMBIGUITY_SCAN_SCOPE]


def planning_normative_hit_key(hit: dict[str, Any]) -> tuple[str, int, str]:
    return (str(hit.get("path") or ""), int(hit.get("line") or 0), str(hit.get("term") or ""))


def scan_planning_normative_language(root: Path, task_dir: Path) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for path in planning_ambiguity_scan_paths(task_dir):
        if not path.exists() or not path.is_file():
            raise WorkflowError(f"Required planning artifact not found for ambiguity scan: {path}", exit_code=2)
        repo_path = repo_relative(root, path)
        for line_number, text in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for term in PLANNING_AMBIGUITY_CONTROLLED_TERMS:
                if term in text:
                    hits.append(
                        {
                            "path": repo_path,
                            "line": line_number,
                            "term": term,
                            "text": text,
                        }
                    )
    return hits


def parse_planning_normative_hit_arg(root: Path, task_dir: Path, value: str) -> dict[str, Any]:
    parts = str(value or "").split("|", 4)
    if len(parts) != 5:
        raise WorkflowError(
            'Invalid --normative-hit. Expected "path|line|term|classification|reason".',
            exit_code=2,
            payload={"normative_hit": value},
        )
    raw_path, raw_line, raw_term, raw_classification, raw_reason = [part.strip() for part in parts]
    path = resolve_task_local_path(root, task_dir, raw_path)
    scope_paths = {path.resolve(): name for name, path in zip(PLANNING_AMBIGUITY_SCAN_SCOPE, planning_ambiguity_scan_paths(task_dir))}
    if path.resolve() not in scope_paths:
        raise WorkflowError(
            "record-planning-approval --normative-hit path must be one of: "
            + ", ".join(PLANNING_AMBIGUITY_SCAN_SCOPE),
            exit_code=2,
            payload={"path": raw_path},
        )
    if not re.fullmatch(r"[1-9][0-9]*", raw_line):
        raise WorkflowError("record-planning-approval --normative-hit line must be a positive integer.", exit_code=2)
    term = raw_term
    if term not in PLANNING_AMBIGUITY_CONTROLLED_TERMS:
        raise WorkflowError(
            "record-planning-approval --normative-hit term is not in the controlled planning ambiguity vocabulary.",
            exit_code=2,
            payload={"term": term},
        )
    classification = raw_classification
    if classification and classification not in PLANNING_AMBIGUITY_CLASSIFICATIONS:
        raise WorkflowError(
            "record-planning-approval --normative-hit classification is not allowed.",
            exit_code=2,
            payload={"classification": classification},
        )
    reason = raw_reason
    if classification and not reason:
        raise WorkflowError(
            "record-planning-approval --normative-hit reason is required for classified hits.",
            exit_code=2,
            payload={"path": raw_path, "line": int(raw_line), "term": term},
        )
    return {
        "path": repo_relative(root, path),
        "line": int(raw_line),
        "term": term,
        "classification": classification,
        "reason": reason,
    }


def parse_planning_normative_hit_args(root: Path, task_dir: Path, values: list[str] | None) -> dict[tuple[str, int, str], dict[str, str]]:
    parsed: dict[tuple[str, int, str], dict[str, str]] = {}
    for value in values or []:
        item = parse_planning_normative_hit_arg(root, task_dir, value)
        key = planning_normative_hit_key(item)
        if key in parsed:
            raise WorkflowError(
                "record-planning-approval received duplicate --normative-hit classification input.",
                exit_code=2,
                payload={"path": key[0], "line": key[1], "term": key[2]},
            )
        parsed[key] = {
            "classification": str(item.get("classification") or ""),
            "reason": str(item.get("reason") or ""),
        }
    return parsed


def planning_normative_language_payload(
    root: Path,
    task_dir: Path,
    normative_hit_inputs: list[str] | None,
) -> dict[str, Any]:
    scanned_hits = scan_planning_normative_language(root, task_dir)
    scanned_keys = {planning_normative_hit_key(hit) for hit in scanned_hits}
    classifications = parse_planning_normative_hit_args(root, task_dir, normative_hit_inputs)
    unused_keys = [key for key in classifications if key not in scanned_keys]
    if unused_keys:
        first = unused_keys[0]
        raise WorkflowError(
            "record-planning-approval --normative-hit does not match a current scan hit.",
            exit_code=2,
            payload={"path": first[0], "line": first[1], "term": first[2]},
        )

    hits: list[dict[str, Any]] = []
    unchecked_hits: list[dict[str, Any]] = []
    for scanned in scanned_hits:
        key = planning_normative_hit_key(scanned)
        classification = classifications.get(key, {}).get("classification", "")
        reason = classifications.get(key, {}).get("reason", "")
        hit = {
            **scanned,
            "classification": classification,
            "reason": reason,
        }
        hits.append(hit)
        if not classification or classification in PLANNING_AMBIGUITY_BLOCKING_CLASSIFICATIONS:
            unchecked_hits.append(copy.deepcopy(hit))

    return {
        "controlled_terms": list(PLANNING_AMBIGUITY_CONTROLLED_TERMS),
        "scan_scope": list(PLANNING_AMBIGUITY_SCAN_SCOPE),
        "hits": hits,
        "unchecked_normative_hits": unchecked_hits,
    }


def planning_normative_hit_entry_errors(item: Any, label: str) -> list[str]:
    if not isinstance(item, dict):
        return [f"{label} 中存在非对象 hit。"]
    errors: list[str] = []
    for key in ["path", "term", "text", "classification", "reason"]:
        if key not in item or not isinstance(item.get(key), str):
            errors.append(f"{label} hit 缺少字符串字段 {key}。")
    if not is_strict_int(item.get("line")) or int(item.get("line") or 0) <= 0:
        errors.append(f"{label} hit.line 必须是正整数。")
    term = str(item.get("term") or "")
    if term and term not in PLANNING_AMBIGUITY_CONTROLLED_TERMS:
        errors.append(f"{label} hit.term 不在受控词表中: {term}。")
    classification = str(item.get("classification") or "")
    reason = str(item.get("reason") or "")
    if classification and classification not in PLANNING_AMBIGUITY_CLASSIFICATIONS:
        errors.append(f"{label} hit.classification 不在允许分类集合中: {classification}。")
    if classification and not reason:
        errors.append(f"{label} hit.reason 不能为空。")
    return errors


def planning_normative_language_errors(root: Path, task_dir: Path, normative: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    controlled_terms = normative.get("controlled_terms")
    if not isinstance(controlled_terms, list):
        errors.append("planning-approval.json ambiguity_review.normative_language.controlled_terms 必须是数组。")
    elif controlled_terms != PLANNING_AMBIGUITY_CONTROLLED_TERMS:
        errors.append("planning-approval.json ambiguity_review.controlled_terms 必须与当前受控弱约束词表完全一致。")

    scan_scope = normative.get("scan_scope")
    if not isinstance(scan_scope, list):
        errors.append("planning-approval.json ambiguity_review.normative_language.scan_scope 必须是数组。")
    elif scan_scope != PLANNING_AMBIGUITY_SCAN_SCOPE:
        errors.append("planning-approval.json ambiguity_review.scan_scope 必须固定为 prd.md, design.md, implement.md。")

    hits = normative.get("hits")
    if not isinstance(hits, list):
        errors.append("planning-approval.json ambiguity_review.normative_language.hits 必须是数组。")
        hits = []
    else:
        seen_keys: set[tuple[str, int, str]] = set()
        for index, item in enumerate(hits):
            errors.extend(planning_normative_hit_entry_errors(item, f"planning-approval.json hits[{index}]"))
            if isinstance(item, dict) and is_strict_int(item.get("line")):
                key = planning_normative_hit_key(item)
                if key in seen_keys:
                    errors.append(f"planning-approval.json ambiguity_review.normative_language.hits 存在重复命中: {key[0]}:{key[1]} {key[2]}。")
                seen_keys.add(key)

    unchecked_hits = normative.get("unchecked_normative_hits")
    if not isinstance(unchecked_hits, list):
        errors.append("planning-approval.json ambiguity_review.normative_language.unchecked_normative_hits 必须是数组。")
        unchecked_hits = []
    else:
        for index, item in enumerate(unchecked_hits):
            errors.extend(planning_normative_hit_entry_errors(item, f"planning-approval.json unchecked_normative_hits[{index}]"))

    try:
        current_hits = scan_planning_normative_language(root, task_dir)
    except WorkflowError as exc:
        errors.append(str(exc))
        current_hits = []

    recorded_scan_facts = [
        {
            "path": item.get("path"),
            "line": item.get("line"),
            "term": item.get("term"),
            "text": item.get("text"),
        }
        for item in hits
        if isinstance(item, dict)
    ]
    if recorded_scan_facts != current_hits:
        errors.append("planning-approval.json ambiguity_review.normative_language.hits 与当前 prd.md/design.md/implement.md 扫描结果不一致。")

    expected_unchecked = [
        copy.deepcopy(item)
        for item in hits
        if isinstance(item, dict)
        and (
            not str(item.get("classification") or "").strip()
            or str(item.get("classification") or "").strip() in PLANNING_AMBIGUITY_BLOCKING_CLASSIFICATIONS
        )
    ]
    if unchecked_hits != expected_unchecked:
        errors.append("planning-approval.json ambiguity_review.unchecked_normative_hits 与 hits[] 中未分类或 contract_violation 命中不一致。")
    if unchecked_hits:
        errors.append("planning-approval.json ambiguity_review.unchecked_normative_hits 必须为空；非空表示仍有未处理规范性弱约束命中。")
    return errors


def build_planning_ambiguity_review_payload(
    reviewer: str,
    summary: str,
    status: str,
    root: Path,
    task_dir: Path,
    normative_hit_inputs: list[str] | None,
) -> dict[str, Any]:
    normalized_status = str(status or "").strip()
    normalized_reviewer = str(reviewer or "").strip()
    normalized_summary = str(summary or "").strip()
    if normalized_status != PLANNING_AMBIGUITY_STATUS_PASSED:
        raise WorkflowError(
            f"record-planning-approval requires --ambiguity-status {PLANNING_AMBIGUITY_STATUS_PASSED}.",
            exit_code=2,
            payload={"received_status": normalized_status or "(missing)"},
        )
    if not normalized_reviewer:
        raise WorkflowError("record-planning-approval requires --ambiguity-reviewer identity metadata.", exit_code=2)
    if not normalized_summary:
        raise WorkflowError("record-planning-approval requires --ambiguity-summary with the AI ambiguity review conclusion.", exit_code=2)
    normative_language = planning_normative_language_payload(root, task_dir, normative_hit_inputs)
    if normative_language["unchecked_normative_hits"]:
        raise WorkflowError(
            "record-planning-approval blocked by unchecked normative planning artifact hits.",
            exit_code=2,
            payload={"normative_language": normative_language},
        )
    return {
        "status": PLANNING_AMBIGUITY_STATUS_PASSED,
        "reviewer": normalized_reviewer,
        "summary": normalized_summary,
        "normative_language": normative_language,
        "checked_dimensions": {
            dimension: True for dimension in PLANNING_AMBIGUITY_REQUIRED_DIMENSIONS
        },
    }


def planning_ambiguity_review_errors(root: Path, task_dir: Path, review: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(review, dict):
        return ["planning-approval.json 缺少 ambiguity_review 结构化证据。"]
    if str(review.get("status") or "").strip() != PLANNING_AMBIGUITY_STATUS_PASSED:
        errors.append(f"planning-approval.json ambiguity_review.status 必须是 {PLANNING_AMBIGUITY_STATUS_PASSED}。")
    if not str(review.get("reviewer") or "").strip():
        errors.append("planning-approval.json ambiguity_review 缺少 reviewer。")
    if not str(review.get("summary") or "").strip():
        errors.append("planning-approval.json ambiguity_review 缺少 summary。")

    normative = review.get("normative_language")
    if not isinstance(normative, dict):
        errors.append("planning-approval.json ambiguity_review 缺少 normative_language。")
        normative = {}
    errors.extend(planning_normative_language_errors(root, task_dir, normative))

    dimensions = review.get("checked_dimensions")
    if not isinstance(dimensions, dict):
        errors.append("planning-approval.json ambiguity_review 缺少 checked_dimensions。")
        dimensions = {}
    for dimension in PLANNING_AMBIGUITY_REQUIRED_DIMENSIONS:
        if dimensions.get(dimension) is not True:
            errors.append(f"planning-approval.json ambiguity_review.checked_dimensions.{dimension} 必须为 true。")
    return errors


def build_planning_approval_payload(
    root: Path,
    task_dir: Path,
    reviewer: str,
    approval_summary: str,
    user_confirmation: str,
    artifacts: list[str],
    ambiguity_reviewer: str,
    ambiguity_summary: str,
    ambiguity_status: str,
    normative_hit_inputs: list[str] | None = None,
    review_prompt_presented_at: str | None = None,
    confirmation_source: str = PLANNING_APPROVAL_CONFIRMATION_SOURCE,
) -> dict[str, Any]:
    normalized_source = str(confirmation_source or "").strip()
    if normalized_source != PLANNING_APPROVAL_CONFIRMATION_SOURCE:
        raise WorkflowError(
            "record-planning-approval requires explicit post-planning review confirmation; "
            f"--confirmation-source must be {PLANNING_APPROVAL_CONFIRMATION_SOURCE}.",
            exit_code=2,
            payload={"received_source": normalized_source or "(missing)"},
        )
    required_paths = [resolve_task_local_path(root, task_dir, name) for name in DEFAULT_PLANNING_ARTIFACTS]
    if artifacts:
        requested = [resolve_task_local_path(root, task_dir, item) for item in artifacts]
        requested_paths = {path.resolve() for path in requested}
        missing_required = [
            name
            for name, path in zip(DEFAULT_PLANNING_ARTIFACTS, required_paths)
            if path.resolve() not in requested_paths
        ]
        if missing_required:
            raise WorkflowError(
                "record-planning-approval must record all three planning documents after the explicit review prompt: "
                + ", ".join(missing_required),
                exit_code=2,
                payload={"missing_artifacts": missing_required},
            )
        artifact_paths = requested
    else:
        artifact_paths = required_paths
    ambiguity_review = build_planning_ambiguity_review_payload(
        ambiguity_reviewer,
        ambiguity_summary,
        ambiguity_status,
        root,
        task_dir,
        normative_hit_inputs,
    )
    reviewed = [file_digest(root, path) for path in artifact_paths]
    artifact_repo_paths = {str(item["path"]) for item in reviewed}
    artifact_repo_paths.add(repo_relative(root, planning_approval_path(task_dir)))
    dirty_paths = dirty_paths_excluding(root, artifact_repo_paths)
    presented_at = str(review_prompt_presented_at or "").strip() or now_iso()
    approved_at = now_iso()
    return {
        "schema_version": PLANNING_APPROVAL_SCHEMA_VERSION,
        "generated_at": approved_at,
        "review_prompt_presented_at": presented_at,
        "approved_at": approved_at,
        "task_dir": repo_relative(root, task_dir),
        "head": current_head(root),
        "dirty_paths": dirty_paths,
        "reviewer": reviewer,
        "approval_summary": approval_summary,
        "ambiguity_review": ambiguity_review,
        "user_confirmation": {
            "source": PLANNING_APPROVAL_CONFIRMATION_SOURCE,
            "message": user_confirmation,
        },
        "reviewed_artifacts": reviewed,
        "approved_artifacts": copy.deepcopy(reviewed),
        "notes": "record-planning-approval 是 recorder / validator：记录已经完成的 AI/human planning review 和用户确认；它不替代 planning 判断。",
    }


def validate_planning_approval(
    root: Path,
    task_dir: Path,
    allow_committed_head: bool = False,
) -> tuple[Path, dict[str, Any], list[str]]:
    path = planning_approval_path(task_dir)
    if not path.exists():
        raise WorkflowError(f"Planning approval artifact not found: {path}", exit_code=2)
    payload = read_json(path)
    errors: list[str] = []
    if payload.get("schema_version") != PLANNING_APPROVAL_SCHEMA_VERSION:
        errors.append(
            f"planning-approval.json schema_version 必须是 {PLANNING_APPROVAL_SCHEMA_VERSION}；旧 schema 不能作为当前 planning approval。"
        )
    if not str(payload.get("review_prompt_presented_at") or "").strip():
        errors.append("planning-approval.json 缺少 review_prompt_presented_at。")
    if not str(payload.get("approved_at") or "").strip():
        errors.append("planning-approval.json 缺少 approved_at。")
    if not str(payload.get("approval_summary") or "").strip():
        errors.append("planning-approval.json 缺少 approval_summary。")
    if not str(payload.get("reviewer") or "").strip():
        errors.append("planning-approval.json 缺少 reviewer。")
    errors.extend(planning_ambiguity_review_errors(root, task_dir, payload.get("ambiguity_review")))
    confirmation = payload.get("user_confirmation")
    if not isinstance(confirmation, dict):
        errors.append("planning-approval.json 缺少用户确认摘要。")
        confirmation = {}
    elif not str(confirmation.get("message") or "").strip():
        errors.append("planning-approval.json 缺少用户确认摘要。")
    source = str(confirmation.get("source") or "").strip() if isinstance(confirmation, dict) else ""
    if source != PLANNING_APPROVAL_CONFIRMATION_SOURCE:
        errors.append(
            "planning-approval.json user_confirmation.source 必须是 "
            f"{PLANNING_APPROVAL_CONFIRMATION_SOURCE}；Phase 0 handoff/workflow confirmation 不能替代规划审核确认。"
        )
    recorded_head = str(payload.get("head") or "")
    if not recorded_head:
        errors.append("planning-approval.json 缺少 HEAD 记录。")
    recorded_dirty = payload.get("dirty_paths")
    if not isinstance(recorded_dirty, list):
        errors.append("planning-approval.json 缺少 dirty_paths 数组。")
    reviewed = payload.get("reviewed_artifacts")
    approved_alias = payload.get("approved_artifacts")
    if not isinstance(reviewed, list) or not reviewed:
        errors.append("planning-approval.json 缺少 reviewed_artifacts。")
        reviewed = []
    if not isinstance(approved_alias, list) or not approved_alias:
        errors.append("planning-approval.json 缺少 approved_artifacts alias。")
    if reviewed:
        normalized_reviewed = [
            normalized_digest_entry(root, task_dir, item)
            for item in reviewed
        ]
        reviewed_paths = {str(item.get("path") or "") for item in normalized_reviewed if isinstance(item, dict)}
        for name in DEFAULT_PLANNING_ARTIFACTS:
            required_path = repo_relative(root, task_dir / name)
            if required_path not in reviewed_paths:
                errors.append(f"planning-approval.json 未在 reviewed_artifacts 记录 {name}。")
        for item in normalized_reviewed:
            errors.extend(digest_errors(root, item, "planning approval reviewed_artifacts"))
    if isinstance(approved_alias, list) and approved_alias:
        normalized_alias = [
            normalized_digest_entry(root, task_dir, item)
            for item in approved_alias
        ]
        alias_paths = {str(item.get("path") or "") for item in normalized_alias if isinstance(item, dict)}
        for name in DEFAULT_PLANNING_ARTIFACTS:
            required_path = repo_relative(root, task_dir / name)
            if required_path not in alias_paths:
                errors.append(f"planning-approval.json 未在 approved_artifacts alias 记录 {name}。")
        for item in normalized_alias:
            errors.extend(digest_errors(root, item, "planning approval approved_artifacts"))
    else:
        # Old artifacts with only approved_artifacts are intentionally blocked
        # by schema/source checks above; this branch keeps error output focused.
        pass
    return path, payload, errors


def normalize_coverage(items: list[str] | None) -> dict[str, bool]:
    coverage = {key: False for key in REQUIRED_PHASE2_COVERAGE}
    for item in items or []:
        key = str(item).strip()
        if not key:
            continue
        if key not in coverage:
            raise WorkflowError(
                f"Unknown phase2 coverage key: {key}. Valid keys: {', '.join(REQUIRED_PHASE2_COVERAGE)}",
                exit_code=2,
            )
        coverage[key] = True
    return coverage


def recorded_digest_paths(entries: Any) -> set[str]:
    if not isinstance(entries, list):
        return set()
    paths: set[str] = set()
    for entry in entries:
        if isinstance(entry, dict) and str(entry.get("path") or "").strip():
            paths.add(str(entry["path"]))
    return paths


def parse_validation_arg(value: str) -> dict[str, Any]:
    parts = [part.strip() for part in value.split("|", 1)]
    command = parts[0]
    result = parts[1] if len(parts) > 1 else "recorded"
    if not command:
        raise WorkflowError("Validation evidence command must not be empty.", exit_code=2)
    return {"command": command, "result": result}


def build_phase2_check_payload(
    root: Path,
    task_dir: Path,
    task_context: dict[str, Any],
    task: dict[str, Any],
    checker: str,
    check_summary: str,
    checked_artifacts: list[str],
    checked_specs: list[str],
    coverage_items: list[str],
    validation_items: list[str],
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    base_branch = base_branch_from_sources(argparse.Namespace(base_branch=None), task, task_context)
    task_artifact_names = checked_artifacts or default_existing_task_artifacts(task_dir, DEFAULT_PHASE2_TASK_ARTIFACTS)
    task_artifacts = [file_digest(root, resolve_task_local_path(root, task_dir, item)) for item in task_artifact_names]
    specs = [file_digest(root, resolve_checked_spec_path(root, item)) for item in checked_specs]
    validation_commands = [parse_validation_arg(item) for item in validation_items]
    coverage = normalize_coverage(coverage_items)
    excluded = {str(item["path"]) for item in task_artifacts}
    excluded.add(repo_relative(root, phase2_check_path(task_dir)))
    dirty_paths = dirty_paths_excluding(root, excluded)
    return {
        "schema_version": "1.0",
        "generated_at": now_iso(),
        "task_dir": repo_relative(root, task_dir),
        "base_branch": base_branch,
        "head": current_head(root),
        "diff_range": diff_range(root, base_branch),
        "dirty_paths": dirty_paths,
        "checker": checker,
        "check_summary": check_summary,
        "checked_artifacts": task_artifacts,
        "checked_specs": specs,
        "coverage": coverage,
        "validation_commands": validation_commands,
        "findings": findings,
        "notes": "record-phase2-check 是 recorder / validator：记录已经完成的完整 trellis-check 结论、证据和 stale 判定；验证命令只是 check evidence 的一部分。",
    }


def phase2_agent_assignment_errors(root: Path, task_dir: Path) -> list[str]:
    path = agent_assignment_path(task_dir)
    if not path.exists():
        return []
    try:
        raw_payload = read_json(path)
    except WorkflowError as exc:
        return [str(exc)]
    status_events = raw_payload.get("status_events")
    liveness = raw_payload.get("liveness")
    if not status_events and not liveness:
        return []
    payload = normalize_agent_assignment_for_task(root, task_dir, raw_payload)
    errors = validate_liveness_payload_errors(root, payload, enforce_recovery_chains=True)
    if errors:
        return [
            "phase2-check.json 不能在 agent-assignment.json 存在未闭环 sub-agent liveness/recovery evidence 时通过: "
            + error
            for error in errors
        ]
    return []


def validate_phase2_check(
    root: Path,
    task_dir: Path,
    allow_committed_head: bool = False,
) -> tuple[Path, dict[str, Any], list[str]]:
    path = phase2_check_path(task_dir)
    if not path.exists():
        raise WorkflowError(f"Phase 2 check artifact not found: {path}", exit_code=2)
    payload = read_json(path)
    errors: list[str] = []
    if not str(payload.get("check_summary") or "").strip():
        errors.append("phase2-check.json 缺少 check_summary。")
    if not str(payload.get("checker") or "").strip():
        errors.append("phase2-check.json 缺少 checker。")
    recorded_head = str(payload.get("head") or "")
    head = current_head(root)
    accepted_committed_state = False
    committed_head_audit_performed = False
    if recorded_head != head:
        if allow_committed_head and recorded_head and is_ancestor(root, recorded_head, "HEAD"):
            committed_head_audit_performed = True
            recorded_dirty = payload.get("dirty_paths")
            if not isinstance(recorded_dirty, list):
                errors.append("phase2-check.json 缺少 dirty_paths 数组。")
            committed_paths_covered, uncovered_paths = committed_paths_match_phase2_dirty_paths(
                root,
                recorded_head,
                recorded_dirty if isinstance(recorded_dirty, list) else [],
            )
            if not committed_paths_covered:
                errors.append(
                    "phase2-check.json 记录的 HEAD 是当前 HEAD 的祖先，但之后提交了未被 dirty_paths 覆盖的非 Trellis metadata 变更: "
                    + ", ".join(uncovered_paths[:20])
                )
            has_non_metadata, non_metadata_paths = has_non_metadata_dirty_paths(root)
            if has_non_metadata:
                errors.append(
                    "phase2-check.json 记录的 HEAD 是当前 HEAD 的祖先，但工作区存在非 Trellis metadata 变更: "
                    + ", ".join(non_metadata_paths[:20])
                )
            else:
                accepted_committed_state = committed_paths_covered
        else:
            errors.append(f"phase2-check.json 记录的 HEAD {recorded_head or '(missing)'} 与当前 HEAD {head} 不一致。")
    dirty_excluded = {repo_relative(root, phase2_check_path(task_dir))}
    dirty_excluded.update(recorded_digest_paths(payload.get("checked_artifacts")))
    dirty_now = dirty_paths_excluding(root, dirty_excluded)
    recorded_dirty = payload.get("dirty_paths")
    if not isinstance(recorded_dirty, list):
        if "phase2-check.json 缺少 dirty_paths 数组。" not in errors:
            errors.append("phase2-check.json 缺少 dirty_paths 数组。")
    elif accepted_committed_state or committed_head_audit_performed:
        pass
    elif sorted(str(item) for item in recorded_dirty) != sorted(dirty_now):
        errors.append("phase2-check.json 记录的 dirty_paths 与当前 working tree 不一致。")
    coverage = payload.get("coverage")
    if not isinstance(coverage, dict):
        errors.append("phase2-check.json 缺少 coverage。")
    else:
        for key in REQUIRED_PHASE2_COVERAGE:
            if coverage.get(key) is not True:
                errors.append(f"phase2-check.json coverage.{key} 不是 true。")
    validation_commands = payload.get("validation_commands")
    if not isinstance(validation_commands, list) or not validation_commands:
        errors.append("phase2-check.json 缺少 validation_commands。")
    checked_artifacts = payload.get("checked_artifacts")
    if not isinstance(checked_artifacts, list) or not checked_artifacts:
        errors.append("phase2-check.json 缺少 checked_artifacts。")
    else:
        for item in checked_artifacts:
            artifact_path = str(item.get("path") or "").strip() if isinstance(item, dict) else ""
            if (
                allow_committed_head
                and committed_head_audit_performed
                and is_phase2_post_commit_mutable_artifact_path(artifact_path)
            ):
                continue
            errors.extend(digest_errors(root, item, "phase2 checked_artifacts"))
    checked_specs = payload.get("checked_specs")
    if isinstance(checked_specs, list):
        for item in checked_specs:
            errors.extend(digest_errors(root, item, "phase2 checked_specs"))
    findings = payload.get("findings")
    if not isinstance(findings, list):
        errors.append("phase2-check.json 缺少 findings 数组。")
    else:
        blockers = unresolved_blocking_findings([item for item in findings if isinstance(item, dict)])
        if blockers:
            errors.append("phase2-check.json 存在未 resolved 的 P0/P1/P2 finding。")
    errors.extend(phase2_agent_assignment_errors(root, task_dir))
    return path, payload, errors


def build_review_gate_payload(
    root: Path,
    task_dir: Path,
    config: dict[str, Any],
    task_context: dict[str, Any],
    base_branch: str,
    pass_gate: bool,
    findings: list[dict[str, Any]],
    observations: list[dict[str, Any]],
    followup_candidates: list[dict[str, Any]],
    command: list[str],
    summary: str,
    evidence: list[str],
    reviewer: str,
    review_source: str,
    review_report: dict[str, Any] | None,
    agent_assignment: dict[str, Any] | None,
    review_reports: list[dict[str, Any]],
) -> dict[str, Any]:
    diff_spec = diff_range(root, base_branch)
    files = changed_files(root, diff_spec)
    deployment_impact = detect_deployment_impact(files)
    blockers = review_gate_blocking_findings(findings)
    ledger = load_issue_scope_ledger(task_dir, task_context)
    close_issues = ledger.get("close_issues") if isinstance(ledger.get("close_issues"), list) else []
    return {
        "schema_version": "1.0",
        "generated_at": now_iso(),
        "task_dir": repo_relative(root, task_dir),
        "base_branch": base_branch,
        "base_ref": diff_base_ref(root, base_branch),
        "head_branch": current_branch(root),
        "head": current_head(root),
        "diff_range": diff_spec,
        "changed_files": files,
        "review_scope": [
            "文档",
            "代码",
            "测试",
            "Trellis artifacts",
            "配置",
            "脚本",
            "schema",
            "CI/CD workflow 与发布自动化",
            "Dockerfile / Docker Compose / 容器启动脚本",
            "Kubernetes YAML / Helm values / Kustomize base 和 overlay",
            "数据库 schema / migration / seed / backfill 脚本",
            "各目录下本次变更涉及的 Makefile",
            "preset installer",
        ],
        "command": command,
        "conclusion": {
            "passed": bool(pass_gate and not blockers),
            "summary": summary or ("Branch Review Gate 通过。" if pass_gate and not blockers else "Branch Review Gate 未通过。"),
            "block_priorities": review_gate_config(config).get("block_priorities", ["P0", "P1", "P2", "P3"]),
            "blocking_findings_count": len(blockers),
            "findings_count": len(findings),
            "observations_count": len(observations),
            "followup_candidates_count": len(followup_candidates),
        },
        "findings": findings,
        "observations": observations,
        "followup_candidates": followup_candidates,
        "issue_scope": {
            "ledger_path": repo_relative(root, issue_scope_ledger_path(task_dir)),
            "close_issues_reviewed": close_issues,
            "related_issues": ledger.get("related_issues", []),
            "followup_issues": ledger.get("followup_issues", []),
        },
        "verification_evidence": {
            "base_head": f"{diff_base_ref(root, base_branch)}...{current_head(root)}",
            "changed_file_count": len(files),
            "reviewer": reviewer,
            "review_source": review_source,
            "review_report": review_report,
            "agent_assignment": agent_assignment,
            "review_reports": review_reports,
            "evidence": evidence,
            "notes": "review-branch 是 recorder / validator：记录已经完成的 AI/human review 结论、diff 范围和审查证据；它不执行 review 判断。",
        },
        "deployment_impact": deployment_impact,
    }


def repo_relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def load_review_gate(task_dir: Path, config: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    path = configured_review_gate_path(task_dir, config)
    if not path.exists():
        raise WorkflowError(f"Branch Review Gate artifact not found: {path}")
    return path, read_json(path)


def migrate_review_gate_for_archived_task(root: Path, task_dir: Path, config: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "migrated": False,
        "path": None,
        "updates": [],
    }
    if not task_dir_is_archived(root, task_dir):
        return result
    path = configured_review_gate_path(task_dir, config)
    result["path"] = str(path)
    if not path.exists():
        return result
    gate = read_json(path)
    changed = False

    archived_task = repo_relative(root, task_dir)
    if gate.get("task_dir") != archived_task:
        gate["task_dir"] = archived_task
        result["updates"].append("task_dir")
        changed = True

    issue_scope = gate.get("issue_scope")
    if isinstance(issue_scope, dict):
        expected_ledger = repo_relative(root, issue_scope_ledger_path(task_dir))
        if issue_scope.get("ledger_path") != expected_ledger:
            issue_scope["ledger_path"] = expected_ledger
            result["updates"].append("issue_scope.ledger_path")
            changed = True

    verification = gate.get("verification_evidence")
    if isinstance(verification, dict):
        review_report = verification.get("review_report")
        migrated_report = migrated_archive_entry(root, task_dir, review_report, REVIEW_REPORT_ARTIFACT)
        if migrated_report is not None and migrated_report != review_report:
            verification["review_report"] = migrated_report
            result["updates"].append("verification_evidence.review_report")
            changed = True

        agent_assignment = verification.get("agent_assignment")
        migrated_assignment = migrated_archive_entry(root, task_dir, agent_assignment, AGENT_ASSIGNMENT_ARTIFACT)
        if migrated_assignment is not None:
            migrated_assignment["task"] = normalized_archive_task_value(root, task_dir, migrated_assignment.get("task"))
            if migrated_assignment != agent_assignment:
                verification["agent_assignment"] = migrated_assignment
                result["updates"].append("verification_evidence.agent_assignment")
                changed = True

        review_reports = verification.get("review_reports")
        if isinstance(review_reports, list):
            migrated_reports: list[Any] = []
            reports_changed = False
            for item in review_reports:
                migrated_item = migrated_archive_digest_entry(root, task_dir, item) if isinstance(item, dict) else None
                if migrated_item is not None and migrated_item != item:
                    migrated_reports.append(migrated_item)
                    reports_changed = True
                else:
                    migrated_reports.append(item)
            if reports_changed:
                verification["review_reports"] = migrated_reports
                result["updates"].append("verification_evidence.review_reports")
                changed = True

    if changed:
        write_json(path, gate)
        result["migrated"] = True
    return result


def metadata_only_since(root: Path, reviewed_head: str) -> tuple[bool, list[str]]:
    proc = run(["git", "diff", "--name-only", f"{reviewed_head}...HEAD"], cwd=root, check=False)
    if proc.returncode != 0:
        return False, []
    files = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    return all(path.startswith(METADATA_ONLY_PREFIXES) or path in METADATA_ONLY_FILES for path in files), files


def validate_review_gate(
    root: Path,
    task_dir: Path,
    config: dict[str, Any],
    allow_metadata_after_gate: bool,
) -> tuple[Path, dict[str, Any], list[str]]:
    path, gate = load_review_gate(task_dir, config)
    errors: list[str] = []
    conclusion = gate.get("conclusion") if isinstance(gate.get("conclusion"), dict) else {}
    if conclusion.get("passed") is not True:
        errors.append("Branch Review Gate 结论不是 passed=true。")
    if not str(conclusion.get("summary") or "").strip():
        errors.append("Branch Review Gate 缺少中文 summary。")
    findings_raw = gate.get("findings", [])
    findings = findings_raw if isinstance(findings_raw, list) else []
    if "findings" in gate and not isinstance(findings_raw, list):
        errors.append("Branch Review Gate findings 必须是数组。")
    if findings:
        errors.append("Branch Review Gate passed=true 但 findings[] 非空；任意 finding 均阻断。")
    for key in ["findings_count", "blocking_findings_count"]:
        raw_count = conclusion.get(key)
        if raw_count is None:
            continue
        if isinstance(raw_count, bool) or not isinstance(raw_count, int):
            errors.append(f"Branch Review Gate conclusion.{key} 必须是整数。")
            continue
        if raw_count < 0:
            errors.append(f"Branch Review Gate conclusion.{key} 不能为负数。")
            continue
        if raw_count > 0:
            errors.append(f"Branch Review Gate passed=true 但 conclusion.{key}={raw_count}；任意 finding 均阻断。")
        if raw_count != len(findings):
            errors.append(
                f"Branch Review Gate conclusion.{key}={raw_count} 与 findings[] 数量 {len(findings)} 不一致。"
            )
    verification = gate.get("verification_evidence") if isinstance(gate.get("verification_evidence"), dict) else {}
    evidence = verification.get("evidence")
    if not (isinstance(evidence, list) and any(str(item).strip() for item in evidence)):
        errors.append("Branch Review Gate 缺少具体 review evidence。")
    reviewer = str(verification.get("reviewer") or "").strip()
    review_source = str(verification.get("review_source") or "").strip()
    errors.extend(independent_review_source_errors(review_source, reviewer))
    review_report = verification.get("review_report") if isinstance(verification.get("review_report"), dict) else None
    errors.extend(valid_review_report_fields(root, task_dir, review_report))
    reviewed_head = str(gate.get("head") or "")
    agent_assignment = verification.get("agent_assignment")
    errors.extend(valid_agent_assignment_summary_fields(root, task_dir, agent_assignment, expected_head=reviewed_head))
    assignment_payload_for_reports: dict[str, Any] | None = None
    if isinstance(agent_assignment, dict):
        migrated_assignment = migrated_archive_entry(root, task_dir, agent_assignment, AGENT_ASSIGNMENT_ARTIFACT) or agent_assignment
        assignment_path_value = str(migrated_assignment.get("path") or "").strip()
        if assignment_path_value:
            assignment_path = resolve_repo_path(root, assignment_path_value).resolve()
            if assignment_path.is_file() and task_dir.resolve() in [assignment_path, *assignment_path.parents]:
                try:
                    assignment_payload_for_reports = normalize_agent_assignment_for_task(root, task_dir, read_json(assignment_path))
                except WorkflowError:
                    assignment_payload_for_reports = None
    errors.extend(
        valid_review_reports_summary_fields(
            root,
            task_dir,
            verification.get("review_reports"),
            assignment_payload=assignment_payload_for_reports,
        )
    )
    errors.extend(
        review_report_language_template_errors(
            root,
            task_dir,
            review_report,
            verification.get("review_reports"),
        )
    )
    head = current_head(root)
    gate_config = review_gate_config(config)
    require_head_match = bool(gate_config.get("require_head_match", True))
    if require_head_match and reviewed_head != head:
        accepted_metadata_tail = False
        if allow_metadata_after_gate and reviewed_head and is_ancestor(root, reviewed_head, "HEAD"):
            metadata_only, tail_files = metadata_only_since(root, reviewed_head)
            accepted_metadata_tail = metadata_only
            if not metadata_only:
                errors.append(
                    "Branch Review Gate 通过后出现非 Trellis metadata 变更: "
                    + ", ".join(tail_files[:20])
                )
        if not accepted_metadata_tail:
            errors.append(f"Branch Review Gate 记录的 HEAD {reviewed_head or '(missing)'} 与当前 HEAD {head} 不一致。")
    return path, gate, errors


def base_branch_from_sources(args: argparse.Namespace, task: dict[str, Any], task_context: dict[str, Any]) -> str:
    for value in [
        getattr(args, "base_branch", None),
        task_context.get("base_branch"),
        task.get("base_branch"),
    ]:
        if value:
            return str(value)
    raise WorkflowError("Could not resolve base_branch from args, task-start-context, or task.json.")


def pr_issue_line(keyword: str, issue: dict[str, Any], mode: str) -> str:
    number = issue.get("number")
    title = str(issue.get("title") or "").strip()
    suffix = f" - {title}" if title else ""
    if mode == "close":
        return f"- {keyword} #{number}{suffix}"
    if mode == "followup":
        return f"- Follow-up #{number}{suffix}"
    return f"- Refs #{number}{suffix}"


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


def contains_chinese_text(value: str) -> bool:
    return CHINESE_TEXT_RE.search(value) is not None


def parse_commit_subject(subject: str) -> dict[str, Any] | None:
    value = subject.strip()
    merge_match = MERGE_COMMIT_SUBJECT_RE.match(value)
    if merge_match:
        return {"kind": "merge", **merge_match.groupdict()}
    match = CONVENTIONAL_COMMIT_SUBJECT_RE.match(value)
    if not match:
        return None
    parsed = {"kind": "conventional", **match.groupdict()}
    parsed["issue"] = int(parsed["issue"])
    return parsed


def validate_commit_subject(
    subject: str,
    primary_issue: int | None = None,
    pull_request: int | str | None = None,
) -> list[str]:
    errors: list[str] = []
    value = subject.strip()
    if not value:
        return ["commit subject 不能为空。"]
    if value.startswith("Merge pull request"):
        errors.append("commit subject 不得使用 GitHub 自动生成的 `Merge pull request ...`。")
    if value.startswith("完成："):
        errors.append("commit subject 不得直接使用中文 PR title / squash title。")
    if re.match(r"^#\d+\s+", value):
        errors.append("issue id 必须放在 Conventional Commits 前缀之后。")
    if re.match(rf"^[a-z]+\(#[0-9]+\):", value):
        errors.append("issue id 不得放在 scope 中。")
    if close_keyword_pattern().search(value):
        errors.append("commit subject 不得使用 Closes/Fixes/Resolves/Close/Fix/Resolve；issue 关闭语义只能放在 PR body。")

    parsed = parse_commit_subject(value)
    if parsed is None:
        errors.append("commit subject 必须匹配 `{type}({scope}): #{primary_issue} 中文描述` 或 `chore(merge): #{pull_request} 合并 #{primary_issue} 中文 PR 摘要`。")
        return errors

    if parsed["kind"] == "merge":
        if primary_issue is not None and int(parsed["primary_issue"]) != int(primary_issue):
            errors.append(f"merge commit subject primary issue 必须是 #{primary_issue}。")
        if pull_request is not None and str(parsed["pull_request"]) != str(pull_request):
            errors.append(f"merge commit subject pull request 必须是 #{pull_request}。")
        if not contains_chinese_text(str(parsed["summary"])):
            errors.append("merge commit subject 的 PR 摘要必须包含中文。")
        return errors

    if primary_issue is not None and int(parsed["issue"]) != int(primary_issue):
        errors.append(f"commit subject primary issue 必须是 #{primary_issue}。")
    description = str(parsed["description"]).strip()
    if not contains_chinese_text(description):
        errors.append("commit subject 描述必须包含中文。")
    if description.startswith("合并"):
        errors.append("工作提交不得使用 merge 语义 subject；merge commit 必须使用 `chore(merge)`。")
    return errors


def subject_kind(subject: str) -> str:
    parsed = parse_commit_subject(subject)
    if not parsed:
        return "invalid"
    if parsed["kind"] == "merge":
        return "merge"
    if parsed["type"] == "chore" and parsed["scope"] in METADATA_COMMIT_SCOPES:
        return "metadata"
    return "work"


def section_line_positions(body: str, required_sections: list[str]) -> tuple[dict[str, int], list[str]]:
    lines = body.splitlines()
    positions: dict[str, int] = {}
    errors: list[str] = []
    for section in required_sections:
        matches = [idx for idx, line in enumerate(lines) if line.strip() == section]
        if not matches:
            errors.append(f"commit body 缺少 `{section}` 小节。")
            continue
        if len(matches) > 1:
            errors.append(f"commit body `{section}` 小节重复。")
        positions[section] = matches[0]
    ordered_positions = [positions[section] for section in required_sections if section in positions]
    if ordered_positions != sorted(ordered_positions):
        errors.append("commit body 固定小节顺序不正确。")
    return positions, errors


def section_has_content(lines: list[str], start: int, end: int) -> bool:
    return any(line.strip() for line in lines[start + 1 : end])


def footer_line_index(body: str, pattern: re.Pattern[str]) -> tuple[int | None, re.Match[str] | None]:
    for idx, line in enumerate(body.splitlines()):
        match = pattern.match(line.strip())
        if match:
            return idx, match
    return None, None


def validate_work_commit_body(body: str, primary_issue: int | None = None) -> list[str]:
    value = body.strip()
    if not value:
        return ["工作提交必须包含 commit body。"]
    errors: list[str] = []
    if close_keyword_pattern().search(value):
        errors.append("commit body 不得使用 Closes/Fixes/Resolves；issue 关闭语义只能放在 PR body。")
    lines = value.splitlines()
    positions, section_errors = section_line_positions(value, WORK_COMMIT_BODY_SECTIONS)
    errors.extend(section_errors)
    footer_pattern = re.compile(r"^Refs #(?P<issue>\d+)$")
    footer_idx, footer_match = footer_line_index(value, footer_pattern)
    if footer_idx is None or footer_match is None:
        errors.append("工作提交 body footer 必须包含 `Refs #<primary_issue>`。")
    else:
        if primary_issue is not None and int(footer_match.group("issue")) != int(primary_issue):
            errors.append(f"工作提交 body footer 必须引用 `Refs #{primary_issue}`。")
        last_section_idx = positions.get(WORK_COMMIT_BODY_SECTIONS[-1])
        if last_section_idx is not None and footer_idx <= last_section_idx:
            errors.append("`Refs #<primary_issue>` footer 必须位于固定小节之后。")

    for idx, section in enumerate(WORK_COMMIT_BODY_SECTIONS):
        if section not in positions:
            continue
        next_candidates = [
            positions[next_section]
            for next_section in WORK_COMMIT_BODY_SECTIONS[idx + 1 :]
            if next_section in positions
        ]
        if footer_idx is not None:
            next_candidates.append(footer_idx)
        end = min(next_candidates) if next_candidates else len(lines)
        if not section_has_content(lines, positions[section], end):
            errors.append(f"commit body `{section}` 小节缺少实质内容。")
    return errors


def validate_metadata_commit_body(body: str) -> list[str]:
    if body.strip():
        return ["Trellis metadata 提交必须不写 body；subject 必须完整表达 metadata 动作。"]
    return []


def validate_merge_commit_body(
    body: str,
    primary_issue: int | None = None,
    pull_request: int | str | None = None,
) -> list[str]:
    value = body.strip()
    if not value:
        return ["merge commit 必须包含 body。"]
    errors: list[str] = []
    if close_keyword_pattern().search(value):
        errors.append("merge commit body 不得使用 Closes/Fixes/Resolves；issue 关闭语义只能放在 PR body。")
    lines = value.splitlines()
    positions, section_errors = section_line_positions(value, MERGE_COMMIT_BODY_SECTIONS)
    errors.extend(section_errors)
    pr_pattern = re.compile(r"^PR: #(?P<pull_request>\d+|<pull_request>)$")
    refs_pattern = re.compile(r"^Refs #(?P<primary_issue>\d+)$")
    pr_idx, pr_match = footer_line_index(value, pr_pattern)
    refs_idx, refs_match = footer_line_index(value, refs_pattern)
    if pr_idx is None or pr_match is None:
        errors.append("merge commit body 必须包含 `PR: #<pull_request>`。")
    elif pull_request is not None and str(pr_match.group("pull_request")) != str(pull_request):
        errors.append(f"merge commit body PR footer 必须引用 `PR: #{pull_request}`。")
    if refs_idx is None or refs_match is None:
        errors.append("merge commit body 必须包含 `Refs #<primary_issue>`。")
    elif primary_issue is not None and int(refs_match.group("primary_issue")) != int(primary_issue):
        errors.append(f"merge commit body Refs footer 必须引用 `Refs #{primary_issue}`。")
    footer_indexes = [idx for idx in [pr_idx, refs_idx] if idx is not None]
    first_footer_idx = min(footer_indexes) if footer_indexes else None
    last_section_idx = positions.get(MERGE_COMMIT_BODY_SECTIONS[-1])
    if first_footer_idx is not None and last_section_idx is not None and first_footer_idx <= last_section_idx:
        errors.append("merge commit body footer 必须位于固定小节之后。")

    for idx, section in enumerate(MERGE_COMMIT_BODY_SECTIONS):
        if section not in positions:
            continue
        next_candidates = [
            positions[next_section]
            for next_section in MERGE_COMMIT_BODY_SECTIONS[idx + 1 :]
            if next_section in positions
        ]
        if first_footer_idx is not None:
            next_candidates.append(first_footer_idx)
        end = min(next_candidates) if next_candidates else len(lines)
        if not section_has_content(lines, positions[section], end):
            errors.append(f"merge commit body `{section}` 小节缺少实质内容。")
    return errors


def validate_commit_message(subject: str, body: str, primary_issue: int | None = None) -> tuple[str, list[str]]:
    errors = validate_commit_subject(subject, primary_issue=primary_issue)
    kind = subject_kind(subject)
    if kind == "merge":
        parsed = parse_commit_subject(subject) or {}
        errors.extend(
            validate_merge_commit_body(
                body,
                primary_issue=primary_issue,
                pull_request=parsed.get("pull_request"),
            )
        )
    elif kind == "metadata":
        errors.extend(validate_metadata_commit_body(body))
    elif kind == "work":
        errors.extend(validate_work_commit_body(body, primary_issue=primary_issue))
    return kind, errors


def format_metadata_commit_subject(primary_issue: int, action: str = "固化任务收尾元数据") -> str:
    return f"chore(trellis): #{int(primary_issue)} {action.strip()}"


def format_merge_commit_subject(pull_request: int | str, primary_issue: int, summary: str) -> str:
    return f"chore(merge): #{pull_request} 合并 #{int(primary_issue)} {summary.strip()}"


def format_merge_commit_body(
    pull_request: int | str,
    primary_issue: int,
    summary: str,
    head_branch: str,
    base_branch: str,
) -> str:
    return (
        "合并：\n"
        f"合入 `{head_branch}` 到 `{base_branch}`，保留 PR 内部提交历史。\n\n"
        "范围：\n"
        f"本次 PR 完成 #{int(primary_issue)}：{summary.strip()}。\n\n"
        "审计：\n"
        "Trellis task archive、review gate、finish-summary 和 readiness 提交保留在 PR 分支历史中，用于审计任务过程。\n\n"
        f"PR: #{pull_request}\n"
        f"Refs #{int(primary_issue)}\n"
    )


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


def merge_summary_from_title(title: str, primary_issue: int, ledger: dict[str, Any]) -> str:
    summary = title.strip()
    if summary.startswith("完成："):
        summary = summary.removeprefix("完成：").strip()
    summary = re.sub(rf"^#{int(primary_issue)}\s*", "", summary).strip()
    if contains_chinese_text(summary):
        return summary
    close_issues = ledger.get("close_issues")
    if isinstance(close_issues, list):
        for issue in close_issues:
            if not isinstance(issue, dict):
                continue
            try:
                number = int(issue.get("number"))
            except (TypeError, ValueError):
                continue
            title_value = str(issue.get("title") or "").strip()
            if number == int(primary_issue) and contains_chinese_text(title_value):
                return title_value
    return f"完成 {summary}" if summary else f"完成 #{int(primary_issue)}"


def build_merge_commit_payload(
    *,
    primary_issue: int,
    summary: str,
    head_branch: str,
    base_branch: str,
    pull_request: int | str | None,
    body_file_hint: str = MERGE_COMMIT_BODY_FILE_HINT,
) -> dict[str, Any]:
    pull_request_value: int | str = pull_request if pull_request is not None else "<pull_request>"
    ready = pull_request is not None and str(pull_request).isdigit()
    subject = format_merge_commit_subject(pull_request_value, primary_issue, summary)
    body = format_merge_commit_body(pull_request_value, primary_issue, summary, head_branch, base_branch)
    errors = validate_commit_subject(subject, primary_issue=primary_issue, pull_request=pull_request_value)
    errors.extend(validate_merge_commit_body(body, primary_issue=primary_issue, pull_request=pull_request_value))
    command_pr = str(pull_request_value)
    return {
        "ready": ready,
        "subject": subject,
        "body": body,
        "body_file_hint": body_file_hint,
        "command": [
            "gh",
            "pr",
            "merge",
            command_pr,
            "--merge",
            "--subject",
            subject,
            "--body-file",
            body_file_hint,
        ],
        "errors": errors,
    }


def parse_pull_request_number(value: str) -> int | None:
    match = re.search(r"/pull/(\d+)(?:\b|$)", value.strip())
    if match:
        return int(match.group(1))
    match = re.search(r"#(\d+)\b", value.strip())
    if match:
        return int(match.group(1))
    return None


def git_commit_messages(root: Path, range_spec: str) -> list[dict[str, str]]:
    proc = run(["git", "log", "--reverse", "--format=%x1e%H%x1f%s%x1f%b", range_spec], cwd=root, check=False)
    if proc.returncode != 0:
        raise WorkflowError(
            "Unable to read git commit messages.",
            exit_code=2,
            payload={"range": range_spec, "stderr": proc.stderr.strip()},
        )
    commits: list[dict[str, str]] = []
    for record in proc.stdout.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        parts = record.split("\x1f", 2)
        if len(parts) != 3:
            continue
        commits.append({"hash": parts[0].strip(), "subject": parts[1].strip(), "body": parts[2].strip()})
    return commits


def is_reviewed_pr_body_source(body_source: str) -> bool:
    return body_source.startswith(REVIEWED_PR_BODY_SOURCE_PREFIXES)


def active_task_relative_path(root: Path, task_dir: Path, body_path_arg: str | None) -> str | None:
    if not body_path_arg:
        return None
    raw_path = Path(body_path_arg).expanduser()
    path = raw_path if raw_path.is_absolute() else root / raw_path
    try:
        return path.resolve().relative_to(task_dir.resolve()).as_posix()
    except ValueError:
        return None


def rewrite_active_task_artifact_path(root: Path, task_dir: Path, archived_task_dir: Path, body_path_arg: str | None) -> str | None:
    relative = active_task_relative_path(root, task_dir, body_path_arg)
    if relative is None:
        return body_path_arg
    return str(archived_task_dir / relative)


def load_pr_body_artifact(root: Path, artifact_arg: str | None) -> tuple[str | None, Path | None]:
    if not artifact_arg:
        return None, None
    raw_path = Path(artifact_arg).expanduser()
    path = raw_path if raw_path.is_absolute() else root / raw_path
    payload = read_json(path)
    ready = payload.get("ready")
    if ready is not True:
        raise WorkflowError("PR body readiness artifact is not ready=true.", exit_code=2, payload={"artifact_path": str(path)})
    body_file = str(payload.get("body_file") or "").strip()
    if body_file:
        body_path = Path(body_file).expanduser()
        resolved = body_path if body_path.is_absolute() else path.parent / body_path
        return read_pr_body_file(root, str(resolved)), resolved
    body = payload.get("body")
    if isinstance(body, str) and body.strip():
        return body.strip() + "\n", path
    raise WorkflowError(
        "PR body readiness artifact must contain a non-empty body or body_file.",
        exit_code=2,
        payload={"artifact_path": str(path)},
    )


def canonical_json_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def task_local_pr_readiness_path(root: Path, task_dir: Path, artifact_arg: str | None) -> Path:
    if not artifact_arg:
        raise WorkflowError(
            "Publish recovery requires the task-local pr-readiness.json snapshot.",
            exit_code=2,
        )
    raw = Path(artifact_arg).expanduser()
    path = raw if raw.is_absolute() else root / raw
    resolved = path.resolve()
    expected = (task_dir / PR_READINESS_ARTIFACT).resolve()
    if resolved != expected:
        raise WorkflowError(
            "Publish recovery readiness artifact must be the task-local pr-readiness.json.",
            exit_code=2,
            payload={"artifact_path": str(resolved), "expected_path": str(expected)},
        )
    return resolved


def build_pr_readiness_snapshot(
    root: Path,
    task_dir: Path,
    *,
    repo: str,
    base_branch: str,
    head_branch: str,
    reviewed_head_sha: str,
    title: str,
    draft: bool,
) -> tuple[Path, dict[str, Any]]:
    body_path = (task_dir / PR_BODY_ARTIFACT).resolve()
    if not body_path.is_file():
        raise WorkflowError(
            "PR readiness requires task-local pr-body.md.",
            exit_code=2,
            payload={"body_path": str(body_path)},
        )
    publish_inputs = {
        "repo": repo,
        "base_branch": normalize_ref(base_branch).removeprefix("origin/"),
        "head_branch": head_branch,
        "reviewed_head_sha": reviewed_head_sha,
        "title": title,
        "body_source": PR_BODY_ARTIFACT,
        "body_sha256": hashlib.sha256(body_path.read_bytes()).hexdigest(),
        "draft": draft,
        "reviewed_source": f"body-artifact:{PR_READINESS_ARTIFACT}",
    }
    artifact = {
        "ready": True,
        "body_file": PR_BODY_ARTIFACT,
        "publish_inputs": publish_inputs,
        "publish_inputs_sha256": canonical_json_sha256(publish_inputs),
    }
    return task_dir / PR_READINESS_ARTIFACT, artifact


def write_pr_readiness_snapshot(
    root: Path,
    task_dir: Path,
    **kwargs: Any,
) -> tuple[Path, dict[str, Any]]:
    path, artifact = build_pr_readiness_snapshot(root, task_dir, **kwargs)
    write_json(path, artifact)
    return path, artifact


def read_pr_readiness_publish_inputs(
    root: Path,
    task_dir: Path,
    artifact_arg: str | None,
    gate: dict[str, Any],
    *,
    require_committed: bool,
) -> tuple[Path, dict[str, Any], str]:
    path = task_local_pr_readiness_path(root, task_dir, artifact_arg)
    artifact = read_json(path)
    if set(artifact) != {"ready", "body_file", "publish_inputs", "publish_inputs_sha256"}:
        raise WorkflowError("pr-readiness.json keys are invalid.", exit_code=2)
    if artifact.get("ready") is not True or artifact.get("body_file") != PR_BODY_ARTIFACT:
        raise WorkflowError("pr-readiness.json must bind ready=true to task-local pr-body.md.", exit_code=2)
    publish_inputs = artifact.get("publish_inputs")
    if not isinstance(publish_inputs, dict) or set(publish_inputs) != PR_READINESS_PUBLISH_INPUT_KEYS:
        raise WorkflowError("pr-readiness.json publish_inputs keys are invalid.", exit_code=2)
    digest = str(artifact.get("publish_inputs_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != canonical_json_sha256(publish_inputs):
        raise WorkflowError("pr-readiness.json publish_inputs digest does not match canonical content.", exit_code=2)
    if publish_inputs.get("body_source") != PR_BODY_ARTIFACT:
        raise WorkflowError("pr-readiness.json body_source must equal pr-body.md.", exit_code=2)
    if publish_inputs.get("reviewed_source") != f"body-artifact:{PR_READINESS_ARTIFACT}":
        raise WorkflowError("pr-readiness.json reviewed_source is invalid.", exit_code=2)
    for key in ["repo", "base_branch", "head_branch", "reviewed_head_sha", "title", "body_sha256"]:
        if not isinstance(publish_inputs.get(key), str) or not str(publish_inputs[key]).strip():
            raise WorkflowError(f"pr-readiness.json publish_inputs.{key} is invalid.", exit_code=2)
    if not re.fullmatch(r"[0-9a-f]{40}", str(publish_inputs["reviewed_head_sha"])):
        raise WorkflowError("pr-readiness.json reviewed_head_sha is invalid.", exit_code=2)
    if not re.fullmatch(r"[0-9a-f]{64}", str(publish_inputs["body_sha256"])):
        raise WorkflowError("pr-readiness.json body_sha256 is invalid.", exit_code=2)
    if not isinstance(publish_inputs.get("draft"), bool):
        raise WorkflowError("pr-readiness.json draft must be boolean.", exit_code=2)

    body_path = task_dir / PR_BODY_ARTIFACT
    if not body_path.is_file():
        raise WorkflowError("pr-readiness.json bound pr-body.md is missing.", exit_code=2)
    body_bytes = body_path.read_bytes()
    if hashlib.sha256(body_bytes).hexdigest() != publish_inputs["body_sha256"]:
        raise WorkflowError("pr-readiness.json body digest does not match pr-body.md.", exit_code=2)
    body = body_bytes.decode("utf-8").strip()
    if not body:
        raise WorkflowError("pr-readiness.json bound pr-body.md is empty.", exit_code=2)

    reviewed_head = str(gate.get("head") or "")
    if reviewed_head != publish_inputs["reviewed_head_sha"]:
        raise WorkflowError("pr-readiness.json reviewed HEAD does not match Branch Review Gate.", exit_code=2)

    if require_committed:
        relative_paths = [repo_relative(root, path), repo_relative(root, body_path)]
        dirty_paths = set(git_status_paths(root))
        dirty_bound = sorted(dirty_paths.intersection(relative_paths))
        if dirty_bound:
            raise WorkflowError(
                "PR readiness artifact or body has dirty/staged changes.",
                exit_code=2,
                payload={"dirty_paths": dirty_bound},
            )
        for bound_path, relative in [(path, relative_paths[0]), (body_path, relative_paths[1])]:
            blob = subprocess.run(
                ["git", "show", f"HEAD:{relative}"],
                cwd=str(root),
                capture_output=True,
                check=False,
            )
            if blob.returncode != 0 or blob.stdout != bound_path.read_bytes():
                raise WorkflowError(
                    "PR readiness artifact or body does not match its current HEAD Git blob.",
                    exit_code=2,
                    payload={"path": relative},
                )
        history = run(
            ["git", "log", "--format=%H", "--", relative_paths[0]],
            cwd=root,
            check=False,
        )
        commits = [line for line in history.stdout.splitlines() if line.strip()]
        if history.returncode != 0 or len(commits) != 1:
            raise WorkflowError(
                "pr-readiness.json must be immutable after its initial metadata commit.",
                exit_code=2,
                payload={"artifact_commit_count": len(commits)},
            )
        ancestor = run(
            ["git", "merge-base", "--is-ancestor", str(publish_inputs["reviewed_head_sha"]), "HEAD"],
            cwd=root,
            check=False,
        )
        if ancestor.returncode != 0:
            raise WorkflowError("PR readiness reviewed HEAD is not an ancestor of current HEAD.", exit_code=2)
    return path, publish_inputs, body + "\n"


def read_pr_body_file(root: Path, body_file: str | None) -> str | None:
    if not body_file:
        return None
    raw_path = Path(body_file).expanduser()
    path = raw_path if raw_path.is_absolute() else root / raw_path
    if not path.exists():
        raise WorkflowError(f"PR body file not found: {path}", exit_code=2)
    if not path.is_file():
        raise WorkflowError(f"PR body file must point to a file: {path}", exit_code=2)
    body = path.read_text(encoding="utf-8").strip()
    if not body:
        raise WorkflowError(f"PR body file is empty: {path}", exit_code=2)
    return body + "\n"


def resolve_pr_body(
    root: Path,
    args: argparse.Namespace,
    ledger: dict[str, Any],
    gate: dict[str, Any],
    validations: list[str],
    config: dict[str, Any],
) -> tuple[str, str]:
    file_body = read_pr_body_file(root, getattr(args, "body_file", None))
    if file_body is not None:
        return file_body, f"body-file:{getattr(args, 'body_file')}"
    artifact_body, artifact_path = load_pr_body_artifact(root, getattr(args, "body_artifact", None))
    if artifact_body is not None:
        return artifact_body, f"body-artifact:{artifact_path}"
    return build_pr_body(ledger, gate, validations, config), "generated"


def validate_reviewed_body_source_for_publish(body_source: str, draft: bool) -> list[str]:
    if draft or is_reviewed_pr_body_source(body_source):
        return []
    return [
        "non-draft publish requires an AI-reviewed --body-file or --body-artifact; generated PR body is preview-only.",
    ]


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


def build_pr_body(ledger: dict[str, Any], gate: dict[str, Any], validations: list[str], config: dict[str, Any]) -> str:
    publish = publish_config(config)
    keyword = str(publish.get("close_keyword") or "Closes")
    close_issues = ledger.get("close_issues") if isinstance(ledger.get("close_issues"), list) else []
    related_issues = ledger.get("related_issues") if isinstance(ledger.get("related_issues"), list) else []
    followup_issues = ledger.get("followup_issues") if isinstance(ledger.get("followup_issues"), list) else []

    close_lines = "\n".join(pr_issue_line(keyword, issue, "close") for issue in close_issues) or "- 无"
    related_lines = "\n".join(pr_issue_line(keyword, issue, "related") for issue in related_issues) or "- 无"
    followup_lines = "\n".join(pr_issue_line(keyword, issue, "followup") for issue in followup_issues) or "- 无"
    validation_lines = "\n".join(f"- {item}" for item in validations) or "- 未提供具体 publish validation；non-draft publish 会被 PR body 质量校验阻塞。"
    gate_summary = gate.get("conclusion", {}).get("summary", "Branch Review Gate 通过。")
    gate_head = gate.get("head", "")
    gate_range = gate.get("diff_range", "")
    changed_files = gate.get("changed_files") if isinstance(gate.get("changed_files"), list) else []
    impact = gate.get("deployment_impact") if isinstance(gate.get("deployment_impact"), dict) else {}
    changed_file_lines = "\n".join(f"- `{path}`" for path in changed_files[:12]) or "- 未记录 changed_files；需要 AI 在 body file 中补充影响范围。"
    deployment_note = "未检测到部署资产变更。"
    if impact.get("needs_deployment_impact_review"):
        deployment_note = "Review Gate 已要求覆盖部署影响判断；请结合 gate evidence 确认是否需要 CI/CD、容器、K8s、migration 或 Makefile 更新。"
    summary_items: list[str] = []
    for issue in close_issues[:5]:
        number = issue.get("number")
        title = str(issue.get("title") or "").strip()
        if number and title:
            summary_items.append(f"- 完成 #{number}：{title}。")
        elif number:
            summary_items.append(f"- 完成 #{number} 对应的 PR 关闭范围。")
    if not summary_items:
        summary_items.append("- 完成 Issue Scope Ledger 中记录的 PR 关闭范围。")
    summary_items.append(f"- Review Gate 结论：{gate_summary}")
    summary_bullets = "\n".join(summary_items)

    return f"""## 变更摘要

{summary_bullets}

## 影响范围

{changed_file_lines}

## 验证结果

{validation_lines}

## Review Gate

- 结论：{gate_summary}
- Reviewed HEAD：`{gate_head}`
- Diff 范围：`{gate_range}`

## Docs SSOT

- 策略：需要 AI 在 reviewed body file 中补充 `Docs SSOT Plan` strategy。
- durable docs / 文档更新：需要说明更新清单或 no-update 理由。
- task delta merge：需要说明 task artifact delta 是否已 merge。
- task history：需要说明哪些内容仅保留为任务历史。
- follow-up / limitation：需要说明后续或当前 PR 限制。

## Issue 关闭范围

{close_lines}

### 仅引用或相关

{related_lines}

### 后续范围

{followup_lines}

## 安全说明

- 未在 PR 正文中包含 token、secret、签名 URL、`.env` 内容或数据库 URL。
- {deployment_note}
"""


def pr_title_from_task(task: dict[str, Any], args: argparse.Namespace) -> str:
    if getattr(args, "title", None):
        return str(args.title)
    title = str(task.get("title") or task.get("name") or "Trellis task").strip()
    return f"完成：{title}"


def check_env_payload(root: Path) -> dict[str, Any]:
    root = repo_root(root)
    config = load_config(root)
    repo = str(config.get("github_repo") or "").strip() or infer_github_repo(root)
    current = current_branch(root)
    base, candidates = resolve_base_branch(root, config)
    gh_installed = shutil.which("gh") is not None
    gh_authenticated = run(["gh", "auth", "status"], cwd=root, check=False).returncode == 0 if gh_installed else False
    extension = guru_team_extension_payload(root)
    warnings: list[str] = []
    next_steps: list[str] = []
    if not repo:
        warnings.append("github_repo is not configured and could not be inferred from the Git origin remote.")
        next_steps.append(
            "Set `github_repo: owner/repo` in `.trellis/guru-team/config.yml` "
            "or configure a GitHub `origin` remote before GitHub issue intake or publish."
        )
    if not gh_installed:
        warnings.append("GitHub CLI is not installed.")
        next_steps.append("Install `gh` before using Guru Team GitHub issue intake or publish.")
    elif not gh_authenticated:
        warnings.append("GitHub CLI is not authenticated.")
        next_steps.append("Run `gh auth login` before using Guru Team GitHub issue intake or publish.")
    if extension.get("status") == "missing":
        warnings.append("Guru Team extension manifest is not installed.")
        next_steps.append("Re-apply the Guru Team preset so `.trellis/guru-team/extension.json` records the installed extension version.")
    elif extension.get("status") == "invalid":
        warnings.append("Guru Team extension manifest is invalid.")
        next_steps.append("Inspect `.trellis/guru-team/extension.json` or re-apply the Guru Team preset.")
    payload = {
        "status": "ok",
        "repo_root": str(root),
        "github_repo": repo,
        "trellis_installed": (root / ".trellis").is_dir(),
        "guru_team_extension": extension,
        "gh_installed": gh_installed,
        "gh_authenticated": gh_authenticated,
        "current_branch": current,
        "base_branch": base,
        "base_branch_candidates": candidates,
        "dirty": git_dirty(root),
        "worktree_root": str(configured_worktree_root(root, config)),
        "existing_worktrees": worktree_lines(root),
    }
    if warnings:
        payload["warnings"] = warnings
    if next_steps:
        payload["next_steps"] = next_steps
    return payload


def cmd_version(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    return {
        "status": "ok",
        "repo_root": str(root),
        "guru_team_extension": guru_team_extension_payload(root),
    }


def cmd_check_workspace_boundary(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    snapshot = workspace_boundary_snapshot(
        root,
        config,
        task_context,
        task_dir,
        allow_source_clean=bool(getattr(args, "allow_source_clean", False)),
    )
    if snapshot["errors"]:
        raise WorkflowError(
            "Workspace boundary validation failed.",
            exit_code=2,
            payload=snapshot,
        )
    return snapshot


def cmd_resolve_human_artifacts(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    return resolve_human_markdown_artifacts(root, task_dir)


def infer_assignee(root: Path, explicit: str | None) -> str | None:
    if explicit:
        return explicit
    return developer_name_from_identity(read_developer_identity(root))


def create_task(root: Path, payload: dict[str, Any], args: argparse.Namespace) -> str:
    task_script = root / ".trellis/scripts/task.py"
    if not task_script.exists():
        raise WorkflowError(f"Trellis task script not found: {task_script}")
    workspace = Path(payload["workspace_path"])
    cmd = ["python3", "./.trellis/scripts/task.py", "create", payload["task_title"], "--slug", payload["task_slug"]]
    assignee = infer_assignee(root, args.assignee)
    if assignee:
        cmd.extend(["--assignee", assignee])
    if args.priority:
        cmd.extend(["--priority", args.priority])
    if args.description:
        cmd.extend(["--description", args.description])
    proc = run(cmd, cwd=workspace, check=False)
    if proc.returncode != 0:
        raise WorkflowError(f"task.py create failed:\n{proc.stderr.strip()}")
    return proc.stdout.strip()


def build_task_start_context(root: Path, payload: dict[str, Any], task_dir: Path, assignee: str | None) -> dict[str, Any]:
    freshness = payload.get("base_freshness") if isinstance(payload.get("base_freshness"), dict) else {}
    source_issue = payload.get("source_issue") if isinstance(payload.get("source_issue"), dict) else {}
    base_head_sha = str(freshness.get("local_head_after") or "")
    remote_head_sha = str(freshness.get("remote_head") or "")
    freshness_status = str(freshness.get("status") or "")
    if freshness_status == "fresh" and (not base_head_sha or not remote_head_sha or base_head_sha != remote_head_sha):
        raise WorkflowError("fresh base context requires matching local_head_after and remote_head SHA.", exit_code=2)
    if freshness_status == "remote_only" and (base_head_sha or not remote_head_sha):
        raise WorkflowError("remote_only base context requires empty local SHA and non-empty remote_head SHA.", exit_code=2)
    if freshness_status not in {"fetch_failed", "remote_ref_missing", "unknown"} and not remote_head_sha:
        raise WorkflowError(f"base context status {freshness_status or '(missing)'} requires remote_head SHA.", exit_code=2)
    context = {
        "schema_version": "1.0", "source_issue": source_issue,
        "source_repo": {"repo": payload.get("source_repo", ""), "url": source_issue.get("url", "")},
        "task_slug": payload["task_slug"], "task_title": payload["task_title"],
        "task_artifact_dir": repo_relative(Path(payload["workspace_path"]), task_dir),
        "branch_name": payload["branch_name"], "base_branch": payload["base_branch"],
        "base_ref": freshness.get("base_ref") or payload["base_branch"],
        "base_head_sha": base_head_sha,
        "remote_head_sha": remote_head_sha,
        "workspace_slug": payload["workspace_slug"], "task_workspace_id": payload["workspace_slug"],
        "assignee": assignee or "", "actor": {"login": assignee or ""},
        "issue_scope_ledger_seed": payload.get("issue_scope_ledger") or {},
        "intake_summary": {
            "duplicate_decision": {"search_performed": payload.get("duplicate_search", {}).get("performed", False), "selected_issue": source_issue.get("number")},
            "naming_quality": payload.get("naming_quality") or {},
            "confirmation": {"source_issue_confirmed": bool(source_issue), "created_by_workflow": source_issue.get("created_by_workflow", False)},
        },
    }
    validate_task_start_context(context)
    return context


TASK_START_CONTEXT_FORBIDDEN_KEYS = {
    "workspace_path", "runtime_root", "preflight", "existing_worktrees",
    "developer_identity", "current_checkout", "repo_root", "worktree_root",
    "create_task_command", "handoff_path", "handoff_written",
}


def validate_task_start_context(payload: dict[str, Any]) -> None:
    required = {
        "schema_version", "source_issue", "source_repo", "task_slug", "task_title",
        "task_artifact_dir", "branch_name", "base_branch", "base_ref", "base_head_sha",
        "remote_head_sha", "workspace_slug", "task_workspace_id", "assignee", "actor",
        "issue_scope_ledger_seed", "intake_summary",
    }
    extra = set(payload) - required
    missing = required - set(payload)
    if missing or extra:
        raise WorkflowError(f"Invalid task-start-context keys: missing={sorted(missing)}, extra={sorted(extra)}", exit_code=2)
    task_dir = str(payload.get("task_artifact_dir") or "")
    if Path(task_dir).is_absolute() or not re.fullmatch(r"\.trellis/tasks/[^/]+", task_dir):
        raise WorkflowError("task-start-context task_artifact_dir must be a repo-relative active task directory.", exit_code=2)

    def scan(value: Any, path: str = "$") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in TASK_START_CONTEXT_FORBIDDEN_KEYS:
                    raise WorkflowError(f"task-start-context forbidden key at {path}.{key}", exit_code=2)
                scan(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                scan(child, f"{path}[{index}]")
        elif isinstance(value, str):
            if value.startswith(".trellis/.runtime/") or Path(value).expanduser().is_absolute():
                raise WorkflowError(f"task-start-context contains local-only path at {path}", exit_code=2)

    scan(payload)


def cmd_prepare(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    repo = str(config.get("github_repo") or "").strip() or infer_github_repo(root)
    if not repo:
        raise WorkflowError("Could not resolve GitHub repo. Configure github_repo in .trellis/guru-team/config.yml.")
    if args.create_issue_confirmed and not str(args.issue_title or "").strip():
        raise WorkflowError(
            "--create-issue-confirmed requires --issue-title containing the AI/human reviewed issue title.",
            exit_code=2,
        )

    require_tool("git")
    require_gh_auth(root)

    requirement = " ".join(args.requirement).strip()
    if not requirement:
        raise WorkflowError("No requirement description provided.")

    provided = parse_issue_ref(requirement, repo)
    duplicates: list[dict[str, Any]] = []
    duplicate_search_performed = False
    created_by_workflow = False
    issue: dict[str, Any] | None = None
    proposed_issue: dict[str, Any] | None = None
    issue_title_for_planning = ""
    issue_body_for_branch_type = ""
    issue_number_for_slug = "new"
    source_issue: dict[str, Any] | None = None
    confirmation_required: dict[str, Any] | None = None

    if args.reuse_issue:
        issue = issue_view(repo, int(args.reuse_issue), root)
    elif provided:
        issue_repo, number = provided
        repo = issue_repo
        issue = issue_view(repo, number, root)
    else:
        if config.get("source_issue_required"):
            raise WorkflowError("No source issue provided and source_issue_required is true.")
        if not has_minimum_clarity(requirement):
            raise WorkflowError("Requirement is not clear enough for issue intake. Add target, capability, expected outcome, and boundary/open question.")
        if config.get("duplicate_search_required", True):
            duplicate_search_performed = True
            duplicates = duplicate_search(repo, requirement, root, int(config.get("duplicate_candidate_limit") or 5))
            high = [item for item in duplicates if item.get("similarity") == "high"]
            if high and not args.force_new:
                proposed_title = args.issue_title or make_issue_title(requirement, args.short_name)
                proposed_body = issue_body(requirement, duplicates)
                raise WorkflowError(
                    "Likely duplicate open issue found. Re-run with --reuse-issue <number> or --force-new after user confirmation.",
                    exit_code=2,
                    payload={
                        "duplicates": high,
                        "repo": repo,
                        "proposed_issue": {
                            "repo": repo,
                            "title": proposed_title,
                            "body": proposed_body,
                            "labels": list(config.get("created_issue_labels") or []),
                            "body_reviewed": False,
                            "create_issue_command": confirmed_issue_prepare_command(args, proposed_title, requirement, force_new=True),
                        },
                        "requires_confirmation": {
                            "reuse_issue_or_force_new": True,
                            "reason": "High-similarity duplicate candidates require AI/human review before binding an existing issue or forcing a new one.",
                        },
                    },
                )
        proposed_title = args.issue_title or make_issue_title(requirement, args.short_name)
        proposed_body = read_confirmed_issue_body(args.issue_body_file) if args.create_issue_confirmed else issue_body(requirement, duplicates)
        proposed_issue = {
            "repo": repo,
            "title": proposed_title,
            "body": proposed_body,
            "labels": list(config.get("created_issue_labels") or []),
            "body_reviewed": bool(args.create_issue_confirmed),
            "create_issue_command": confirmed_issue_prepare_command(args, proposed_title, requirement),
        }
        if config.get("auto_create_issue", False):
            proposed_issue["legacy_auto_create_issue_config_ignored"] = True
            proposed_issue["legacy_auto_create_issue_note"] = (
                "auto_create_issue is kept only for backward-compatible config parsing; "
                "prepare requires --create-issue-confirmed before GitHub issue creation."
            )
        if args.create_issue_confirmed:
            if args.create_worktree or args.create_task:
                pre_create_naming = prepare_naming_payload(
                    args,
                    config,
                    "NNN",
                    proposed_title or requirement,
                    f"{proposed_title}\n{proposed_body}",
                )
                ensure_naming_quality_for_create({**pre_create_naming, "proposed_issue": proposed_issue})
            issue = create_issue(repo, proposed_title, proposed_body, root, list(config.get("created_issue_labels") or []))
            created_by_workflow = True
        else:
            confirmation_required = {
                "create_issue": True,
                "reason": "No source issue was provided. prepare generated a proposed issue only; an AI/human must review title/body and rerun with --create-issue-confirmed before GitHub issue creation.",
                "next_commands": proposed_issue["create_issue_command"],
            }

    if issue is not None:
        issue_number = int(issue["number"])
        issue_title_for_planning = str(issue.get("title") or make_issue_title(requirement, args.short_name))
        issue_body_for_branch_type = str(issue.get("body") or "")
        issue_number_for_slug = str(issue_number)
        source_issue = {
            "number": issue_number,
            "url": issue["url"],
            "title": issue_title_for_planning,
            "created_by_workflow": created_by_workflow,
        }
    else:
        issue_title_for_planning = str(proposed_issue.get("title") if proposed_issue else make_issue_title(requirement, args.short_name))
        issue_body_for_branch_type = requirement
    if (args.create_worktree or args.create_task) and source_issue is None:
        raise WorkflowError(
            "--create-worktree and --create-task require a confirmed source issue. Review proposed_issue, create/bind the GitHub issue, then rerun prepare.",
            exit_code=2,
            payload={"proposed_issue": proposed_issue, "requires_confirmation": confirmation_required},
        )
    branch_type_source_text = "\n".join(
        part for part in [issue_title_for_planning, issue_body_for_branch_type] if part
    )
    naming_payload = prepare_naming_payload(
        args,
        config,
        issue_number_for_slug,
        issue_title_for_planning or requirement,
        branch_type_source_text or requirement,
    )
    issue_slug = str(naming_payload["slug"])
    task_slug = str(naming_payload["task_slug"])
    workspace_slug = str(naming_payload["workspace_slug"])
    branch_name = str(naming_payload["branch_name"])
    naming_quality = naming_payload["naming_quality"]
    should_create_worktree = args.create_worktree or args.create_task
    if should_create_worktree:
        ensure_naming_quality_for_create(naming_payload)
    title_prefix = f"#{issue_number_for_slug}" if issue is not None else "[proposed-issue]"
    task_title = args.title or f"{title_prefix} {issue_title_for_planning}"
    base_ref, base_candidates = resolve_base_branch(root, config, args.base_branch)
    base_freshness = (
        ensure_base_freshness(root, base_ref)
        if should_create_worktree
        else refresh_base_freshness_for_planner(root, base_ref)
    )
    workspace_base_ref = str(base_freshness.get("base_ref_for_worktree") or base_ref)
    workspace_mode, workspace_path, workspace_ready = prepare_workspace(
        root,
        config,
        branch_name,
        workspace_slug,
        workspace_base_ref,
        args.worktree,
        should_create_worktree,
    )
    current = current_branch(root)
    assignee = infer_assignee(root, args.assignee)
    developer_identity: dict[str, Any] | None = None
    if should_create_worktree and workspace_ready:
        developer_identity = ensure_workspace_developer_identity(root, workspace_path, assignee)

    create_cmd = ["python3", "./.trellis/scripts/task.py", "create", task_title, "--slug", task_slug]
    if assignee:
        create_cmd.extend(["--assignee", assignee])
    if args.priority:
        create_cmd.extend(["--priority", args.priority])
    if args.description:
        create_cmd.extend(["--description", args.description])

    payload: dict[str, Any] = {
        "schema_version": "1.2",
        "source_repo": repo,
        "source_issue": source_issue,
        "proposed_issue": proposed_issue,
        "requires_confirmation": confirmation_required,
        "slug": issue_slug,
        "naming_quality": naming_quality,
        "task_slug": task_slug,
        "task_title": task_title,
        "branch_name": branch_name,
        "workspace_slug": workspace_slug,
        "workspace_mode": workspace_mode,
        "workspace_path": str(workspace_path),
        "workspace_ready": workspace_ready,
        "base_branch": base_ref,
        "base_branch_candidates": base_candidates,
        "base_freshness": base_freshness,
        "create_task_command": create_cmd,
        "task_dir": None,
        "duplicate_search": {
            "performed": duplicate_search_performed,
            "candidates": duplicates,
        },
        "issue_scope_ledger": {},
        "preflight": {
            "repo_root": str(root),
            "current_checkout": str(root),
            "current_branch": current,
            "dirty": git_dirty(root),
            "worktree_root": str(configured_worktree_root(root, config)),
            "existing_worktrees": worktree_lines(root),
            "selected_base_branch": base_ref,
            "base_freshness": base_freshness,
            "workspace_was_created_or_reused": workspace_ready,
            "developer_identity": developer_identity,
        },
    }
    if source_issue is not None:
        payload["issue_scope_ledger"] = {
            "primary_issue": issue_entry(
                source_issue["number"],
                source_issue["url"],
                source_issue.get("title", ""),
                "intake 主 issue，默认进入 close 候选。",
            ),
            "close_issues": [
                issue_entry(
                    source_issue["number"],
                    source_issue["url"],
                    source_issue.get("title", ""),
                    "默认 close 候选；publish 前必须在 task artifact 中补齐验收证据。",
                )
            ],
            "related_issues": [],
            "followup_issues": [],
        }
    else:
        payload["issue_scope_ledger"] = {
            "primary_issue": None,
            "close_issues": [],
            "related_issues": [],
            "followup_issues": [],
            "notes": [
                "尚未创建或绑定 source issue；用户确认 proposed_issue 后重新运行 prepare。",
                "未绑定 source issue 前不得创建 Trellis task 或发布关闭语义。",
            ],
        }

    if args.create_task:
        if source_issue is None:
            raise WorkflowError(
                "--create-task requires a confirmed source issue. Review proposed_issue, create/bind the GitHub issue, then rerun prepare.",
                exit_code=2,
                payload={"proposed_issue": proposed_issue, "requires_confirmation": confirmation_required},
            )
        payload["task_dir"] = create_task(root, payload, args)
        run(["python3", "./.trellis/scripts/task.py", "set-branch", payload["task_dir"], branch_name], cwd=workspace_path, check=False)
        run(["python3", "./.trellis/scripts/task.py", "set-base-branch", payload["task_dir"], base_ref], cwd=workspace_path, check=False)
        run(["python3", "./.trellis/scripts/task.py", "set-scope", payload["task_dir"], f"GitHub issue: {source_issue['url']}"], cwd=workspace_path, check=False)
        task_dir = resolve_task_dir(workspace_path, payload["task_dir"])
        ensure_issue_scope_ledger(task_dir, payload)
        context = build_task_start_context(root, payload, task_dir, assignee)
        write_json(task_start_context_path(task_dir, config), context)
        payload["task_start_context"] = repo_relative(workspace_path, task_start_context_path(task_dir, config))

    if source_issue is not None and should_create_worktree:
        write_runtime_mappings(root, config, payload, workspace_path)
    return payload


def cmd_review_branch(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    task = task_json(task_dir)
    base_branch = base_branch_from_sources(args, task, task_context)
    ensure_issue_scope_ledger(task_dir, task_context)
    planning_path, _planning_payload, planning_errors = validate_planning_approval(
        root,
        task_dir,
        allow_committed_head=True,
    )
    if planning_errors:
        raise WorkflowError(
            "Branch Review Gate blocked because planning approval evidence is missing, stale, or incomplete.",
            exit_code=2,
            payload={"artifact_path": str(planning_path), "errors": planning_errors},
        )
    phase2_path, _phase2_payload, phase2_errors = validate_phase2_check(root, task_dir, allow_committed_head=True)
    if phase2_errors:
        raise WorkflowError(
            "Branch Review Gate blocked because Phase 2 check report is missing, stale, or incomplete.",
            exit_code=2,
            payload={"artifact_path": str(phase2_path), "errors": phase2_errors},
        )

    findings = load_findings(args)
    observations = load_observations(args)
    followup_candidates = load_followup_candidates(args)
    evidence = [str(item).strip() for item in (args.evidence or []) if str(item).strip()]
    summary = str(args.summary or "").strip()
    blockers = review_gate_blocking_findings(findings)
    if args.pass_gate and blockers:
        raise WorkflowError("--pass cannot be used when any findings are present.", exit_code=2)
    if args.pass_gate and not summary:
        raise WorkflowError(
            "Branch Review Gate pass needs --summary with a human-readable Chinese review conclusion.",
            exit_code=2,
        )
    if args.pass_gate and not evidence:
        raise WorkflowError(
            "Branch Review Gate pass needs at least one --evidence line from the actual review.",
            exit_code=2,
        )
    reviewer = str(args.reviewer or "").strip()
    review_source = str(getattr(args, "review_source", "") or "").strip()
    source_errors = independent_review_source_errors(review_source, reviewer)
    if source_errors:
        raise WorkflowError(
            "Branch Review Gate requires independent Agent review evidence before recording pass or findings.",
            exit_code=2,
            payload={"errors": source_errors},
        )
    review_report = load_review_report(root, task_dir, args.review_report)
    if not blockers and not evidence:
        raise WorkflowError(
            "Branch Review Gate passing result needs at least one --evidence line from the actual review.",
            exit_code=2,
        )
    if review_report is None:
        raise WorkflowError(
            "Branch Review Gate needs --review-report pointing to the task-local review.md from the prior AI/human review. "
            "--reviewer is identity metadata only and cannot satisfy independent review evidence.",
            exit_code=2,
        )
    if not getattr(args, "agent_assignment", None):
        raise WorkflowError(
            "Branch Review Gate pass/findings records need --agent-assignment pointing to task-local agent-assignment.json "
            "so raw review round report evidence and fresh 最终放行审查代理 metadata can be validated.",
            exit_code=2,
        )
    agent_assignment_summary: dict[str, Any] | None = None
    review_reports: list[dict[str, Any]] = []
    assignment_path, assignment_payload, assignment_errors, assignment_summary = validate_agent_assignment(
        root,
        task_dir,
        args.agent_assignment,
        require_current_head=False,
    )
    if args.pass_gate and not assignment_errors:
        assignment_errors.extend(final_review_round_errors(root, assignment_payload))
        assignment_errors.extend(status_event_completion_errors(assignment_payload))
    if not args.pass_gate and findings and not assignment_errors:
        assignment_errors.extend(current_findings_review_round_errors(root, assignment_payload, len(findings)))
    if assignment_errors:
        raise WorkflowError(
            "Branch Review Gate blocked because agent assignment evidence is invalid.",
            exit_code=2,
            payload={"artifact_path": str(assignment_path), "errors": assignment_errors},
        )
    agent_assignment_summary = assignment_summary
    review_reports = review_reports_from_assignment(root, task_dir, assignment_payload)
    template_errors = review_report_language_template_errors(root, task_dir, review_report, review_reports)
    if template_errors:
        raise WorkflowError(
            "Branch Review Gate blocked because review reports contain English template headings.",
            exit_code=2,
            payload={"errors": template_errors},
        )
    if args.pass_gate:
        link_errors = review_rollup_link_errors(root, task_dir, review_report, review_reports)
        if link_errors:
            raise WorkflowError(
                "Branch Review Gate pass blocked because review.md does not link every raw review report.",
                exit_code=2,
                payload={"errors": link_errors},
            )
    if not args.pass_gate and not findings:
        raise WorkflowError(
            "Branch Review Gate needs an explicit result. Use --pass after review found no findings, or provide --finding/--findings-file.",
            exit_code=2,
        )

    payload = build_review_gate_payload(
        root=root,
        task_dir=task_dir,
        config=config,
        task_context=task_context,
        base_branch=base_branch,
        pass_gate=bool(args.pass_gate),
        findings=findings,
        observations=observations,
        followup_candidates=followup_candidates,
        command=sys.argv[:],
        summary=summary,
        evidence=evidence,
        reviewer=reviewer,
        review_source=review_source,
        review_report=review_report,
        agent_assignment=agent_assignment_summary,
        review_reports=review_reports,
    )
    if args.pass_gate and bool(review_gate_config(config).get("require_deployment_impact_evidence", True)):
        deployment_errors = deployment_evidence_errors(payload.get("deployment_impact", {}), evidence, findings)
        if deployment_errors:
            raise WorkflowError(
                "Branch Review Gate pass needs deployment impact evidence.",
                exit_code=2,
                payload={"errors": deployment_errors, "deployment_impact": payload.get("deployment_impact", {})},
            )
    path = configured_review_gate_path(task_dir, config)
    if not args.dry_run:
        write_json(path, payload)
    payload["artifact_path"] = str(path)
    payload["dry_run"] = bool(args.dry_run)
    return payload


def cmd_record_agent_assignment(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    payload = load_agent_assignment(root, task_dir)
    payload["schema_version"] = AGENT_ASSIGNMENT_SCHEMA_VERSION
    payload["task"] = repo_relative(root, task_dir)
    payload["head"] = current_head(root)
    payload["updated_at"] = now_iso()

    logical_role = clean_optional_text(args.logical_role)
    agent_id = clean_optional_text(args.agent_id)
    platform_nickname = clean_optional_text(args.platform_nickname)
    recorded: dict[str, Any] | None = None
    status_event = clean_optional_text(getattr(args, "status_event", None))
    if status_event and args.review_round is not None:
        raise WorkflowError("--status-event cannot be combined with --review-round.", exit_code=2)
    if status_event and getattr(args, "reuse_decision", None):
        raise WorkflowError("--status-event cannot be combined with --reuse-decision.", exit_code=2)
    if status_event:
        raise WorkflowError(
            "record-agent-assignment.sh --status-event is deprecated and fails closed. "
            "Use record-subagent-liveness-event.sh for assigned/progress/status/stale/resume/replacement/terminal events.",
            exit_code=2,
        )
    elif args.review_round is not None:
        recorded = append_agent_review_round(
            payload,
            root,
            task_dir,
            logical_role,
            agent_id,
            platform_nickname,
            int(args.review_round),
            int(args.findings_count or 0),
            clean_optional_text(args.reuse_policy),
            clean_optional_text(args.reuse_decision or "not-applicable"),
            clean_optional_text(args.reviewed_head) or None,
            clean_optional_text(getattr(args, "review_round_report", None)) or None,
        )
    elif args.reuse_decision:
        recorded = append_agent_reuse_decision(
            payload,
            root,
            logical_role,
            agent_id,
            clean_optional_text(args.reuse_decision),
            clean_optional_text(args.reuse_reason),
            args.from_round,
            args.to_round,
            clean_optional_text(args.decision_head) or None,
        )
    else:
        source_repo = source_repo_from_task_context(root, task_context)
        recorded = append_agent_assignment_event(
            payload,
            root,
            task_dir,
            logical_role,
            agent_id,
            platform_nickname,
            clean_optional_text(args.reason),
            source_repo=source_repo,
        )

    errors = validate_agent_assignment_payload(root, task_dir, payload, require_current_head=True, enforce_recovery_chains=False)
    if errors:
        raise WorkflowError(
            "agent-assignment.json validation failed before write.",
            exit_code=2,
            payload={"errors": errors},
        )
    path = agent_assignment_path(task_dir)
    if not args.dry_run:
        write_json(path, payload)
    summary = summarize_agent_assignment(root, task_dir, path, payload) if path.exists() else {
        "path": repo_relative(root, path),
        "roles": sorted(
            {
                str(item.get("logical_role") or "")
                for collection in [payload.get("agents", []), payload.get("review_rounds", []), payload.get("reuse_decisions", [])]
                for item in collection
                if isinstance(item, dict) and str(item.get("logical_role") or "")
            }
            | {
                str(item.get("logical_role") or "")
                for item in payload.get("status_events", [])
                if isinstance(item, dict) and str(item.get("logical_role") or "")
            }
        ),
    }
    return {
        "status": "dry-run" if args.dry_run else "ok",
        "artifact_path": str(path),
        "recorded": recorded,
        "summary": summary,
        "notes": "record-agent-assignment 只记录 AI/human 已做出的分配、复用或状态处理判断，不决定应使用哪个 sub-agent、是否 stale 或是否应终止。",
    }


def cmd_record_subagent_liveness_event(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    source_repo = resolve_source_repo(args.source_repo)
    payload = load_agent_assignment(root, task_dir)
    payload["schema_version"] = AGENT_ASSIGNMENT_SCHEMA_VERSION
    payload["task"] = repo_relative(root, task_dir)
    payload["head"] = current_head(root)
    payload["updated_at"] = now_iso()
    if clean_optional_text(args.event) == "assigned" and getattr(args, "platform_nickname", None) is None:
        raise WorkflowError("assigned requires --platform-nickname; pass an empty string explicitly when the platform has no nickname.", exit_code=2)
    recorded = append_subagent_liveness_event(
        payload,
        root,
        task_dir,
        source_repo,
        agent_id=clean_optional_text(args.agent_id),
        event_name=clean_optional_text(args.event),
        observed_at=clean_optional_text(args.observed_at) or now_iso(),
        evidence=clean_optional_text(args.evidence),
        logical_role=clean_optional_text(getattr(args, "logical_role", "")),
        platform_nickname=clean_optional_text(getattr(args, "platform_nickname", "")),
        source=clean_optional_text(getattr(args, "source", "")) or "main-session",
        predecessor_agent_id=clean_optional_text(getattr(args, "predecessor_agent_id", "")),
        predecessor_event_id=clean_optional_text(getattr(args, "predecessor_event_id", "")),
        termination_reason=clean_optional_text(getattr(args, "termination_reason", "")),
        termination_source_event_id=clean_optional_text(getattr(args, "termination_source_event_id", "")),
        replacement_reason=clean_optional_text(getattr(args, "replacement_reason", "")),
        handoff_summary=clean_optional_text(getattr(args, "handoff_summary", "")),
    )
    errors = validate_agent_assignment_payload(root, task_dir, payload, require_current_head=True, enforce_recovery_chains=False)
    if errors:
        raise WorkflowError(
            "agent-assignment.json validation failed before write.",
            exit_code=2,
            payload={"errors": errors},
        )
    path = agent_assignment_path(task_dir)
    if not args.dry_run:
        write_json(path, payload)
    event_id = recorded.get("event_id") if isinstance(recorded, dict) else ""
    return {
        "recorded": True,
        "event_id": event_id,
        "event": clean_optional_text(args.event),
        "agent_id": clean_optional_text(args.agent_id),
        "artifact": str(path),
        "head": current_head(root),
        "updated_liveness": True,
        "dry_run": bool(args.dry_run),
    }


def cmd_check_subagent_liveness(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    path = agent_assignment_path(task_dir)
    if not path.exists():
        return {
            "decision": AGENT_LIVENESS_BLOCKED_DECISION,
            "agent_id": clean_optional_text(args.agent_id),
            "checked_at": clean_optional_text(getattr(args, "checked_at", "")) or now_iso(),
            "progress_anchor_at": "",
            "pending_status_request_at": None,
            "max_progress_silence_deadline_at": "",
            "next_wait_ms": 0,
            "progress_sources": [],
            "artifact": str(path),
            "reason": "agent-assignment.json missing",
        }
    try:
        source_repo = resolve_source_repo(args.source_repo)
        payload = load_agent_assignment(root, task_dir)
        decision, _snapshot = evaluate_subagent_liveness(
            root,
            task_dir,
            source_repo,
            payload,
            clean_optional_text(args.agent_id),
            int(args.progress_scan_interval),
            int(args.max_progress_silence),
            checked_at=clean_optional_text(getattr(args, "checked_at", "")) or None,
        )
        errors = validate_agent_assignment_payload(root, task_dir, payload, require_current_head=False, enforce_recovery_chains=False)
        if errors:
            raise WorkflowError("agent-assignment.json validation failed after liveness check.", exit_code=2, payload={"errors": errors})
        if not args.dry_run:
            write_json(path, payload)
        decision["dry_run"] = bool(args.dry_run)
        return decision
    except WorkflowError as exc:
        if exc.exit_code != 2:
            raise
        checked = clean_optional_text(getattr(args, "checked_at", "")) or now_iso()
        return {
            "decision": AGENT_LIVENESS_BLOCKED_DECISION,
            "agent_id": clean_optional_text(args.agent_id),
            "checked_at": checked,
            "progress_anchor_at": "",
            "pending_status_request_at": None,
            "max_progress_silence_deadline_at": "",
            "next_wait_ms": 0,
            "progress_sources": [],
            "artifact": str(path),
            "reason": str(exc),
            "errors": exc.payload.get("errors", []) if isinstance(exc.payload, dict) else [],
            "dry_run": bool(args.dry_run),
        }


def cmd_check_agent_assignment(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    path, payload, errors, summary = validate_agent_assignment(
        root,
        task_dir,
        args.agent_assignment,
        require_current_head=bool(args.require_current_head),
    )
    if errors:
        raise WorkflowError(
            "agent-assignment.json validation failed.",
            exit_code=2,
            payload={"artifact_path": str(path), "errors": errors},
        )
    return {
        "status": "ok",
        "artifact_path": str(path),
        "summary": summary,
        "agents_count": len(payload.get("agents", [])) if isinstance(payload.get("agents"), list) else 0,
        "review_rounds_count": len(payload.get("review_rounds", [])) if isinstance(payload.get("review_rounds"), list) else 0,
        "reuse_decisions_count": len(payload.get("reuse_decisions", [])) if isinstance(payload.get("reuse_decisions"), list) else 0,
        "status_events_count": len(payload.get("status_events", [])) if isinstance(payload.get("status_events"), list) else 0,
    }


def cmd_record_planning_approval(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    reviewer = str(args.reviewer or "").strip()
    summary = str(args.summary or "").strip()
    confirmation = str(args.user_confirmation or "").strip()
    ambiguity_reviewer = str(getattr(args, "ambiguity_reviewer", "") or "").strip()
    ambiguity_summary = str(getattr(args, "ambiguity_summary", "") or "").strip()
    ambiguity_status = str(getattr(args, "ambiguity_status", PLANNING_AMBIGUITY_STATUS_PASSED) or "").strip()
    if not reviewer:
        raise WorkflowError("record-planning-approval requires --reviewer identity metadata.", exit_code=2)
    if not summary:
        raise WorkflowError("record-planning-approval requires --summary with the planning review conclusion.", exit_code=2)
    if not confirmation:
        raise WorkflowError("record-planning-approval requires --user-confirmation evidence.", exit_code=2)
    if not ambiguity_reviewer:
        raise WorkflowError("record-planning-approval requires --ambiguity-reviewer identity metadata.", exit_code=2)
    if not ambiguity_summary:
        raise WorkflowError("record-planning-approval requires --ambiguity-summary with the AI ambiguity review conclusion.", exit_code=2)
    payload = build_planning_approval_payload(
        root=root,
        task_dir=task_dir,
        reviewer=reviewer,
        approval_summary=summary,
        user_confirmation=confirmation,
        artifacts=list(args.artifact or []),
        ambiguity_reviewer=ambiguity_reviewer,
        ambiguity_summary=ambiguity_summary,
        ambiguity_status=ambiguity_status,
        normative_hit_inputs=list(getattr(args, "normative_hit", None) or []),
        review_prompt_presented_at=getattr(args, "review_prompt_presented_at", None),
        confirmation_source=str(getattr(args, "confirmation_source", PLANNING_APPROVAL_CONFIRMATION_SOURCE) or ""),
    )
    path = planning_approval_path(task_dir)
    if not args.dry_run:
        write_json(path, payload)
    payload["artifact_path"] = str(path)
    payload["dry_run"] = bool(args.dry_run)
    return payload


def cmd_check_planning_approval(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    path, payload, errors = validate_planning_approval(
        root,
        task_dir,
        allow_committed_head=bool(getattr(args, "allow_committed_head", False)),
    )
    if errors:
        raise WorkflowError(
            "Planning approval is missing or stale.",
            exit_code=2,
            payload={"artifact_path": str(path), "errors": errors},
        )
    return {
        "status": "ok",
        "artifact_path": str(path),
        "task_dir": str(task_dir),
        "head": current_head(root),
        "approved_head": payload.get("head"),
    }


def cmd_record_phase2_check(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    task = task_json(task_dir)
    checker = str(args.checker or "").strip()
    summary = str(args.summary or "").strip()
    if not checker:
        raise WorkflowError("record-phase2-check requires --checker identity metadata.", exit_code=2)
    if not summary:
        raise WorkflowError("record-phase2-check requires --summary with the trellis-check conclusion.", exit_code=2)
    findings = load_findings(args)
    payload = build_phase2_check_payload(
        root=root,
        task_dir=task_dir,
        task_context=task_context,
        task=task,
        checker=checker,
        check_summary=summary,
        checked_artifacts=list(args.checked_artifact or []),
        checked_specs=list(args.checked_spec or []),
        coverage_items=list(args.coverage or []),
        validation_items=list(args.validation or []),
        findings=findings,
    )
    blockers = unresolved_blocking_findings(findings)
    if args.pass_check and blockers:
        raise WorkflowError("--pass cannot be used while unresolved P0/P1/P2 findings are present.", exit_code=2)
    if args.pass_check and any(value is not True for value in payload["coverage"].values()):
        missing = [key for key, value in payload["coverage"].items() if value is not True]
        raise WorkflowError(
            "record-phase2-check --pass requires every coverage key to be explicitly checked.",
            exit_code=2,
            payload={"missing_coverage": missing},
        )
    if args.pass_check and not payload["validation_commands"]:
        raise WorkflowError("record-phase2-check --pass requires at least one --validation evidence line.", exit_code=2)
    if args.pass_check:
        assignment_errors = phase2_agent_assignment_errors(root, task_dir)
        if assignment_errors:
            raise WorkflowError(
                "record-phase2-check --pass blocked because agent assignment evidence is invalid.",
                exit_code=2,
                payload={"artifact_path": str(agent_assignment_path(task_dir)), "errors": assignment_errors},
            )
    path = phase2_check_path(task_dir)
    if not args.dry_run:
        write_json(path, payload)
    payload["artifact_path"] = str(path)
    payload["dry_run"] = bool(args.dry_run)
    return payload


def cmd_check_phase2_check(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    path, payload, errors = validate_phase2_check(root, task_dir)
    if errors:
        raise WorkflowError(
            "Phase 2 check report is missing, stale, or incomplete.",
            exit_code=2,
            payload={"artifact_path": str(path), "errors": errors},
        )
    return {
        "status": "ok",
        "artifact_path": str(path),
        "task_dir": str(task_dir),
        "head": current_head(root),
        "checked_head": payload.get("head"),
    }


def cmd_check_review_gate(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    path, gate, errors = validate_review_gate(root, task_dir, config, args.allow_metadata_after_gate)
    if errors:
        raise WorkflowError(
            "Branch Review Gate has not passed for the current HEAD.",
            exit_code=2,
            payload={"artifact_path": str(path), "errors": errors},
        )
    return {
        "status": "ok",
        "artifact_path": str(path),
        "task_dir": str(task_dir),
        "head": current_head(root),
        "reviewed_head": gate.get("head"),
    }


def cmd_check_commit_messages(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config) if getattr(args, "task", None) else None
    task = task_json(task_dir) if task_dir else {}
    ledger = load_issue_scope_ledger(task_dir, task_context) if task_dir else {}
    primary_issue = int(args.primary_issue) if getattr(args, "primary_issue", None) else primary_issue_number_from_ledger(ledger)
    if getattr(args, "range", None):
        range_spec = str(args.range)
        base_ref = range_spec.split("..", 1)[0] if ".." in range_spec else ""
    else:
        base_branch = str(args.base_ref or base_branch_from_sources(args, task, task_context))
        base_ref = diff_base_ref(root, base_branch)
        range_spec = f"{base_ref}..HEAD"
    commits = git_commit_messages(root, range_spec)
    checked: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for commit in commits:
        kind, commit_errors = validate_commit_message(
            commit["subject"],
            commit.get("body", ""),
            primary_issue=primary_issue,
        )
        entry = {
            "hash": commit["hash"],
            "subject": commit["subject"],
            "kind": kind,
            "errors": commit_errors,
        }
        checked.append(entry)
        if commit_errors:
            errors.append(entry)
    payload = {
        "status": "ok" if not errors else "blocked",
        "base_ref": base_ref,
        "head": current_head(root),
        "range": range_spec,
        "primary_issue": primary_issue,
        "checked_commits": checked,
        "errors": errors,
    }
    if errors:
        raise WorkflowError("Commit message validation failed.", exit_code=2, payload=payload)
    return payload


def cmd_format_merge_commit(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config) if getattr(args, "task", None) else None
    task = task_json(task_dir) if task_dir else {}
    ledger = load_issue_scope_ledger(task_dir, task_context) if task_dir else {}
    primary_issue = int(args.primary_issue) if getattr(args, "primary_issue", None) else primary_issue_number_from_ledger(ledger)
    base_branch = str(args.base_branch or base_branch_from_sources(args, task, task_context))
    base_branch_name = normalize_ref(base_branch).removeprefix("origin/")
    head_branch = str(args.head_branch or current_branch(root))
    title = str(args.summary or pr_title_from_task(task, args)).strip()
    summary = merge_summary_from_title(title, primary_issue, ledger)
    payload = build_merge_commit_payload(
        primary_issue=primary_issue,
        summary=summary,
        head_branch=head_branch,
        base_branch=base_branch_name,
        pull_request=args.pull_request,
        body_file_hint=str(args.body_file_hint or MERGE_COMMIT_BODY_FILE_HINT),
    )
    payload.update(
        {
            "status": "ok" if not payload["errors"] else "blocked",
            "primary_issue": primary_issue,
            "pull_request": args.pull_request or "<pull_request>",
            "base_branch": base_branch_name,
            "head_branch": head_branch,
            "summary": summary,
        }
    )
    if payload["errors"]:
        raise WorkflowError("Merge commit payload validation failed.", exit_code=2, payload=payload)
    return payload


def marketplace_verification_path(task_dir: Path, config: dict[str, Any] | None = None) -> Path:
    name = str((config or {}).get("marketplace_verification_artifact") or MARKETPLACE_VERIFICATION_ARTIFACT)
    return task_dir / name


MARKETPLACE_VERIFICATION_PREFIXES = (
    "trellis/index.json",
    "trellis/guru-team-extension.json",
    "trellis/workflows/",
    "trellis/presets/",
)


def marketplace_verification_required(gate: dict[str, Any]) -> bool:
    files = gate.get("changed_files") if isinstance(gate.get("changed_files"), list) else []
    return any(str(path).startswith(MARKETPLACE_VERIFICATION_PREFIXES) for path in files)


def write_remote_marketplace_evidence(
    root: Path,
    task_dir: Path,
    ledger: dict[str, Any],
    verification_path: Path,
    verification: dict[str, Any],
) -> Path:
    contract_errors = marketplace_verification_contract_errors(verification)
    if verification.get("status") != "passed" or contract_errors:
        raise WorkflowError(
            "Cannot record remote marketplace evidence from a failed or invalid verifier payload.",
            exit_code=2,
            payload={"errors": contract_errors, "status": verification.get("status")},
        )
    artifact_relative = repo_relative(root, verification_path)
    artifact_sha = hashlib.sha256(verification_path.read_bytes()).hexdigest()
    passed = {
        "type": REMOTE_MARKETPLACE_EVIDENCE_TYPE,
        "status": "passed",
        "required": True,
        "artifact_path": artifact_relative,
        "artifact_sha256": artifact_sha,
        "verified_content_head": verification["verified_head"],
        "remote_head": verification["remote_head"],
        "publish_head": verification["verified_head"],
        "commands_passed": all(step.get("passed") is True for step in verification.get("steps", [])),
    }
    targets: list[dict[str, Any]] = []
    primary = ledger.get("primary_issue")
    if isinstance(primary, dict):
        targets.append(primary)
    close_issues = ledger.get("close_issues")
    if isinstance(close_issues, list):
        targets.extend(item for item in close_issues if isinstance(item, dict))
    for issue in targets:
        evidence = issue.setdefault("acceptance_evidence", [])
        if not isinstance(evidence, list):
            raise WorkflowError("Issue Scope Ledger acceptance_evidence must be an array.", exit_code=2)
        evidence[:] = [item for item in evidence if not (isinstance(item, dict) and item.get("type") == REMOTE_MARKETPLACE_EVIDENCE_TYPE)]
        evidence.append(dict(passed))
    path = issue_scope_ledger_path(task_dir)
    write_json(path, ledger)
    return path


def commit_marketplace_verification_metadata(
    root: Path,
    artifact_path: Path,
    ledger_path: Path,
    message: str,
) -> dict[str, Any]:
    artifact_relative = repo_relative(root, artifact_path)
    ledger_relative = repo_relative(root, ledger_path)
    allowed = {artifact_relative, ledger_relative}
    dirty_paths = git_status_paths(root)
    unexpected = [path for path in dirty_paths if path not in allowed]
    if unexpected:
        raise WorkflowError(
            "Marketplace verification metadata tail contains unexpected dirty paths.",
            exit_code=2,
            payload={"allowed_paths": sorted(allowed), "unexpected_dirty_paths": unexpected},
        )
    missing = sorted(allowed - set(dirty_paths))
    if missing:
        raise WorkflowError("Marketplace verification did not produce required artifact and ledger metadata.", exit_code=2, payload={"missing_paths": missing})
    run_stdout(["git", "add", "--", artifact_relative, ledger_relative], cwd=root)
    if run(["git", "diff", "--cached", "--quiet"], cwd=root, check=False).returncode == 0:
        raise WorkflowError("Marketplace verification artifact has no staged content to commit.", exit_code=2)
    run_stdout(["git", "commit", "-m", message], cwd=root)
    return {"committed": True, "paths": sorted(allowed), "commit": current_head(root)}


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


MARKETPLACE_VERIFICATION_KEYS = {
    "schema_version", "generated_at", "status", "repo", "remote", "branch",
    "marketplace_source", "verified_head", "remote_head", "task_dir", "steps", "assets",
}
MARKETPLACE_ASSET_KEYS = {
    "workflow_sha256", "preview_sha256", "task_start_context_schema_sha256", "finish_summary_schema_sha256",
    "runtime_gitignore_present", "workspace_gitignore_present", "session_auto_commit_false",
    "legacy_handoff_absent", "legacy_intake_schema_absent",
}


def marketplace_verification_contract_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(payload) != MARKETPLACE_VERIFICATION_KEYS:
        errors.append("marketplace verification keys do not match schema 1.0.")
    if payload.get("schema_version") != "1.0" or payload.get("status") not in {"passed", "failed"}:
        errors.append("marketplace verification schema_version/status is invalid.")
    for key in ["generated_at", "repo", "remote", "branch", "marketplace_source", "task_dir"]:
        if not isinstance(payload.get(key), str) or not payload.get(key):
            errors.append(f"marketplace verification {key} must be a non-empty string.")
    if not re.fullmatch(r"[0-9a-f]{40}", str(payload.get("verified_head") or "")):
        errors.append("marketplace verification verified_head must be a 40-character lowercase SHA.")
    remote_head = str(payload.get("remote_head") or "")
    if remote_head and not re.fullmatch(r"[0-9a-f]{40}", remote_head):
        errors.append("marketplace verification remote_head must be empty or a 40-character lowercase SHA.")
    steps = payload.get("steps")
    if not isinstance(steps, list) or not steps or any(not isinstance(step, dict) for step in steps):
        errors.append("marketplace verification steps must be a non-empty object array.")
    else:
        required_step_keys = {
            "command", "exit_code", "stdout_sha256", "stderr_sha256",
            "stdout_size_bytes", "stderr_size_bytes", "passed",
        }
        for index, step in enumerate(steps):
            if not required_step_keys.issubset(step):
                errors.append(f"marketplace verification step {index} is missing required audit fields.")
                continue
            command = step.get("command")
            if not isinstance(command, list) or not command or any(not isinstance(part, str) for part in command):
                errors.append(f"marketplace verification step {index} command is invalid.")
            if not isinstance(step.get("exit_code"), int):
                errors.append(f"marketplace verification step {index} exit_code is invalid.")
            for key in ["stdout_sha256", "stderr_sha256"]:
                if not re.fullmatch(r"[0-9a-f]{64}", str(step.get(key) or "")):
                    errors.append(f"marketplace verification step {index} {key} is invalid.")
            for key in ["stdout_size_bytes", "stderr_size_bytes"]:
                if not isinstance(step.get(key), int) or step.get(key) < 0:
                    errors.append(f"marketplace verification step {index} {key} is invalid.")
            if not isinstance(step.get("passed"), bool):
                errors.append(f"marketplace verification step {index} passed is invalid.")
    assets = payload.get("assets")
    if not isinstance(assets, dict) or set(assets) != MARKETPLACE_ASSET_KEYS:
        errors.append("marketplace verification assets keys do not match schema 1.0.")
        assets = {}
    digest_pattern = re.compile(r"^[0-9a-f]{64}$")
    for key in ["workflow_sha256", "preview_sha256", "task_start_context_schema_sha256", "finish_summary_schema_sha256"]:
        value = str(assets.get(key) or "")
        if payload.get("status") == "passed" and not digest_pattern.fullmatch(value):
            errors.append(f"passed marketplace verification requires asset digest: {key}.")
        elif payload.get("status") == "failed" and value and not digest_pattern.fullmatch(value):
            errors.append(f"failed marketplace verification asset digest must be empty or valid: {key}.")
    for key in ["runtime_gitignore_present", "workspace_gitignore_present", "session_auto_commit_false", "legacy_handoff_absent", "legacy_intake_schema_absent"]:
        if not isinstance(assets.get(key), bool):
            errors.append(f"marketplace verification asset flag must be boolean: {key}.")
        elif payload.get("status") == "passed" and assets.get(key) is not True:
            errors.append(f"passed marketplace verification requires true asset flag: {key}.")
    return errors


def execute_marketplace_verification(
    root: Path,
    task_dir: Path,
    repo: str,
    remote: str,
    branch: str,
    expected_head: str,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    remote_proc = run(["git", "ls-remote", "--heads", remote, branch], cwd=root, check=False)
    remote_lines = [line.split() for line in remote_proc.stdout.splitlines() if line.strip()]
    remote_head = remote_lines[0][0] if remote_lines and remote_lines[0] else ""
    remote_evidence = command_evidence(["git", "ls-remote", "--heads", remote, branch], remote_proc)
    remote_evidence["remote_head"] = remote_head
    remote_evidence["expected_head"] = expected_head
    remote_evidence["passed"] = remote_proc.returncode == 0 and remote_head == expected_head
    source = f"gh:{repo}/trellis#{branch}"
    steps: list[dict[str, Any]] = [remote_evidence]
    with tempfile.TemporaryDirectory(prefix="guru-marketplace-verify-") as tmp:
        temp_root = Path(tmp)
        remote_url_proc = run(["git", "remote", "get-url", remote], cwd=root, check=False)
        remote_url = remote_url_proc.stdout.strip()
        remote_url_evidence = command_evidence(["git", "remote", "get-url", remote], remote_url_proc)
        remote_url_evidence["passed"] = remote_url_proc.returncode == 0 and bool(remote_url)
        steps.append(remote_url_evidence)
        source_checkout = temp_root / "source"
        project = temp_root / "project"
        project.mkdir()
        clone_command = ["git", "clone", "--depth", "1", "--branch", branch, remote_url, str(source_checkout)]
        clone_proc = run(clone_command, cwd=temp_root, check=False)
        steps.append(command_evidence(clone_command, clone_proc, ["git", "clone", "--depth", "1", "--branch", branch, "<remote-url>", "<temp-source>"]))
        if clone_proc.returncode == 0:
            run(["git", "init", "-q"], cwd=project, check=False)
        commands = [
            (["trellis", "init", "-y", "-u", "marketplace-verifier", "--codex", "--cursor", "--workflow", "guru-team", "--workflow-source", source], None),
            (["trellis", "workflow", "--marketplace", source, "--template", "guru-team", "--create-new"], None),
            (["trellis", "workflow", "--marketplace", source, "--template", "guru-team", "--force"], None),
            ([str(source_checkout / "trellis/presets/guru-team/scripts/bash/apply.sh"), "--repo", str(project), "--all-platforms", "--json"], ["<temp-source>/trellis/presets/guru-team/scripts/bash/apply.sh", "--repo", "<temp-project>", "--all-platforms", "--json"]),
        ]
        for command, display_command in commands:
            if not all(step.get("passed") is True for step in steps):
                break
            proc = run(command, cwd=project, check=False)
            steps.append(command_evidence(command, proc, display_command))
            if proc.returncode != 0:
                break
        workflow_path = project / ".trellis/workflow.md"
        preview_path = project / ".trellis/workflow.md.new"
        installed_schema = project / ".trellis/guru-team/schemas/task-start-context.schema.json"
        installed_finish_summary_schema = project / ".trellis/guru-team/schemas/finish-summary.schema.json"
        canonical_workflow = source_checkout / "trellis/workflows/guru-team/workflow.md"
        canonical_schema = source_checkout / "trellis/workflows/guru-team/schemas/task-start-context.schema.json"
        canonical_finish_summary_schema = source_checkout / "trellis/workflows/guru-team/schemas/finish-summary.schema.json"
        project_gitignore = (project / ".gitignore").read_text(encoding="utf-8") if (project / ".gitignore").exists() else ""
        project_config = (project / ".trellis/config.yaml").read_text(encoding="utf-8") if (project / ".trellis/config.yaml").exists() else ""
        assets = {
            "workflow_sha256": digest_text(workflow_path.read_text(encoding="utf-8")) if workflow_path.exists() else "",
            "preview_sha256": digest_text(preview_path.read_text(encoding="utf-8")) if preview_path.exists() else "",
            "task_start_context_schema_sha256": hashlib.sha256(installed_schema.read_bytes()).hexdigest() if installed_schema.exists() else "",
            "finish_summary_schema_sha256": hashlib.sha256(installed_finish_summary_schema.read_bytes()).hexdigest() if installed_finish_summary_schema.exists() else "",
            "runtime_gitignore_present": ".trellis/.runtime/" in project_gitignore,
            "workspace_gitignore_present": ".trellis/workspace/" in project_gitignore,
            "session_auto_commit_false": bool(re.search(r"(?m)^session_auto_commit:\s*false\s*$", project_config)),
            "legacy_handoff_absent": not (project / ".trellis/guru-team/handoff.json").exists(),
            "legacy_intake_schema_absent": not (project / ".trellis/guru-team/schemas/intake-handoff.schema.json").exists(),
        }
        expected_workflow_sha = digest_text(canonical_workflow.read_text(encoding="utf-8")) if canonical_workflow.exists() else ""
        expected_schema_sha = hashlib.sha256(canonical_schema.read_bytes()).hexdigest() if canonical_schema.exists() else ""
        expected_finish_summary_schema_sha = hashlib.sha256(canonical_finish_summary_schema.read_bytes()).hexdigest() if canonical_finish_summary_schema.exists() else ""
    passed = all(step.get("passed") is True for step in steps) and all([
        expected_workflow_sha,
        expected_schema_sha,
        expected_finish_summary_schema_sha,
        assets["workflow_sha256"] == expected_workflow_sha,
        assets["preview_sha256"] == expected_workflow_sha,
        assets["task_start_context_schema_sha256"] == expected_schema_sha,
        assets["finish_summary_schema_sha256"] == expected_finish_summary_schema_sha,
        assets["runtime_gitignore_present"],
        assets["workspace_gitignore_present"],
        assets["session_auto_commit_false"],
        assets["legacy_handoff_absent"],
        assets["legacy_intake_schema_absent"],
    ])
    payload = {
        "schema_version": "1.0",
        "generated_at": now_iso(),
        "status": "passed" if passed else "failed",
        "repo": repo,
        "remote": remote,
        "branch": branch,
        "marketplace_source": source,
        "verified_head": expected_head,
        "remote_head": remote_head,
        "task_dir": repo_relative(root, task_dir),
        "steps": steps,
        "assets": assets,
    }
    contract_errors = marketplace_verification_contract_errors(payload)
    if contract_errors:
        payload["status"] = "failed"
        payload["assets"] = {
            "workflow_sha256": assets.get("workflow_sha256") if re.fullmatch(r"[0-9a-f]{64}", str(assets.get("workflow_sha256") or "")) else "",
            "preview_sha256": assets.get("preview_sha256") if re.fullmatch(r"[0-9a-f]{64}", str(assets.get("preview_sha256") or "")) else "",
            "task_start_context_schema_sha256": assets.get("task_start_context_schema_sha256") if re.fullmatch(r"[0-9a-f]{64}", str(assets.get("task_start_context_schema_sha256") or "")) else "",
            "finish_summary_schema_sha256": assets.get("finish_summary_schema_sha256") if re.fullmatch(r"[0-9a-f]{64}", str(assets.get("finish_summary_schema_sha256") or "")) else "",
            "runtime_gitignore_present": bool(assets.get("runtime_gitignore_present")),
            "workspace_gitignore_present": bool(assets.get("workspace_gitignore_present")),
            "session_auto_commit_false": bool(assets.get("session_auto_commit_false")),
            "legacy_handoff_absent": bool(assets.get("legacy_handoff_absent")),
            "legacy_intake_schema_absent": bool(assets.get("legacy_intake_schema_absent")),
        }
        contract_errors = marketplace_verification_contract_errors(payload)
        if contract_errors:
            raise WorkflowError("Internal marketplace verification payload contract failure.", exit_code=2, payload={"errors": contract_errors})
    write_json(marketplace_verification_path(task_dir, config), payload)
    if not passed:
        raise WorkflowError("Remote marketplace verification failed after push.", exit_code=2, payload=payload)
    return payload


def validate_marketplace_verification(
    root: Path,
    task_dir: Path,
    current_publish_head: str,
    repo: str,
    remote: str,
    branch: str,
    config: dict[str, Any] | None = None,
    ledger: dict[str, Any] | None = None,
) -> tuple[Path, dict[str, Any], list[str]]:
    path = marketplace_verification_path(task_dir, config)
    payload, read_error = read_optional_json(path)
    errors: list[str] = []
    if payload is None:
        return path, {}, [f"marketplace verification artifact {read_error or 'missing'}: {path}"]
    errors.extend(marketplace_verification_contract_errors(payload))
    expected_repo = repo.strip()
    expected_source = f"gh:{expected_repo}/trellis#{branch}" if expected_repo else ""
    if expected_repo and payload.get("repo") != expected_repo:
        errors.append("marketplace verification repo does not match the current repository.")
    if payload.get("remote") != remote or payload.get("branch") != branch:
        errors.append("marketplace verification remote/branch identity does not match publish inputs.")
    if expected_source and payload.get("marketplace_source") != expected_source:
        errors.append("marketplace verification source does not match the current repository branch.")
    if payload.get("task_dir") != repo_relative(root, task_dir):
        errors.append("marketplace verification task_dir does not match the current task.")
    sha_pattern = re.compile(r"^[0-9a-f]{40}$")
    digest_pattern = re.compile(r"^[0-9a-f]{64}$")
    if not sha_pattern.fullmatch(str(payload.get("verified_head") or "")):
        errors.append("marketplace verification verified_head must be a 40-character lowercase SHA.")
    if not sha_pattern.fullmatch(str(payload.get("remote_head") or "")):
        errors.append("marketplace verification remote_head must be a 40-character lowercase SHA.")
    if payload.get("status") != "passed":
        errors.append("marketplace verification status must be passed.")
    verified_head = str(payload.get("verified_head") or "")
    if not verified_head or payload.get("remote_head") != verified_head:
        errors.append("marketplace verification lacks a matching verified/remote content HEAD.")
    elif verified_head != current_publish_head:
        diff_proc = run(["git", "diff", "--name-only", f"{verified_head}..{current_publish_head}"], cwd=root, check=False)
        verifier_tail = {
            repo_relative(root, path),
            repo_relative(root, issue_scope_ledger_path(task_dir)),
        }
        finish_summary_tail = verifier_tail | {repo_relative(root, task_dir / FINISH_SUMMARY_ARTIFACT)}
        changed = {line.strip() for line in diff_proc.stdout.splitlines() if line.strip()}
        if diff_proc.returncode != 0 or frozenset(changed) not in {frozenset(verifier_tail), frozenset(finish_summary_tail)}:
            errors.append("marketplace verification is stale; current HEAD is not the exact verifier tail or verifier + finish-summary tail.")
        elif changed == finish_summary_tail:
            summary_path = task_dir / FINISH_SUMMARY_ARTIFACT
            summary, summary_error = read_optional_json(summary_path)
            if summary is None:
                errors.append(f"post-verifier finish-summary tail is {summary_error or 'missing'}.")
            else:
                errors.extend(finish_summary_errors(summary, task_dir=task_dir))
    remote_proc = run(["git", "ls-remote", "--heads", remote, branch], cwd=root, check=False)
    remote_lines = [line.split() for line in remote_proc.stdout.splitlines() if line.strip()]
    current_remote_head = remote_lines[0][0] if remote_lines and remote_lines[0] else ""
    if remote_proc.returncode != 0 or current_remote_head != current_publish_head:
        errors.append("remote branch does not contain the current publish HEAD including verification artifact.")
    steps = payload.get("steps")
    if not isinstance(steps, list) or len(steps) < 7 or any(not isinstance(step, dict) or step.get("passed") is not True for step in steps):
        errors.append("marketplace verification must record passed remote/ref clone/init/preview/switch/preset steps.")
    assets = payload.get("assets") if isinstance(payload.get("assets"), dict) else {}
    for key in ["workflow_sha256", "preview_sha256", "task_start_context_schema_sha256", "finish_summary_schema_sha256"]:
        if not digest_pattern.fullmatch(str(assets.get(key) or "")):
            errors.append(f"marketplace verification missing asset digest: {key}.")
    canonical_workflow = root / "trellis/workflows/guru-team/workflow.md"
    canonical_schema = root / "trellis/workflows/guru-team/schemas/task-start-context.schema.json"
    canonical_finish_summary_schema = root / "trellis/workflows/guru-team/schemas/finish-summary.schema.json"
    expected_workflow_sha = digest_text(canonical_workflow.read_text(encoding="utf-8")) if canonical_workflow.exists() else ""
    expected_schema_sha = hashlib.sha256(canonical_schema.read_bytes()).hexdigest() if canonical_schema.exists() else ""
    expected_finish_summary_schema_sha = hashlib.sha256(canonical_finish_summary_schema.read_bytes()).hexdigest() if canonical_finish_summary_schema.exists() else ""
    if assets.get("workflow_sha256") != expected_workflow_sha or assets.get("preview_sha256") != expected_workflow_sha:
        errors.append("marketplace installed/preview workflow digests do not match the current canonical workflow.")
    if assets.get("task_start_context_schema_sha256") != expected_schema_sha:
        errors.append("marketplace installed task-start-context schema digest does not match current canonical schema.")
    if assets.get("finish_summary_schema_sha256") != expected_finish_summary_schema_sha:
        errors.append("marketplace installed finish-summary schema digest does not match current canonical schema.")
    if assets.get("runtime_gitignore_present") is not True:
        errors.append("marketplace verification did not confirm runtime gitignore contract.")
    if assets.get("workspace_gitignore_present") is not True:
        errors.append("marketplace verification did not confirm workspace gitignore contract.")
    if assets.get("session_auto_commit_false") is not True:
        errors.append("marketplace verification did not confirm session_auto_commit=false.")
    if assets.get("legacy_handoff_absent") is not True or assets.get("legacy_intake_schema_absent") is not True:
        errors.append("marketplace verification did not confirm obsolete handoff artifacts are absent.")
    if ledger is not None:
        artifact_sha = hashlib.sha256(path.read_bytes()).hexdigest()
        targets: list[tuple[str, dict[str, Any]]] = []
        primary = ledger.get("primary_issue")
        if isinstance(primary, dict):
            targets.append(("primary_issue", primary))
        close_issues = ledger.get("close_issues")
        if isinstance(close_issues, list):
            targets.extend((f"close_issues issue #{issue.get('number')}", issue) for issue in close_issues if isinstance(issue, dict))
        expected_evidence = {
            "type": REMOTE_MARKETPLACE_EVIDENCE_TYPE,
            "status": "passed",
            "required": True,
            "artifact_path": repo_relative(root, path),
            "artifact_sha256": artifact_sha,
            "verified_content_head": verified_head,
            "remote_head": str(payload.get("remote_head") or ""),
            "publish_head": verified_head,
            "commands_passed": isinstance(steps, list) and bool(steps) and all(
                isinstance(step, dict) and step.get("passed") is True for step in steps
            ),
        }
        for label, issue in targets:
            evidence = remote_marketplace_evidence(issue)
            if evidence != expected_evidence:
                errors.append(f"{label} remote marketplace evidence does not match the verified artifact facts.")
    return path, payload, errors


def validate_marketplace_publish_evidence(
    root: Path,
    task_dir: Path,
    current_publish_head: str,
    repo: str,
    remote: str,
    branch: str,
    config: dict[str, Any],
    ledger: dict[str, Any],
    gate: dict[str, Any],
) -> tuple[Path, dict[str, Any]]:
    path, payload, errors = validate_marketplace_verification(
        root, task_dir, current_publish_head, repo, remote, branch, config, ledger
    )
    if errors:
        raise WorkflowError(
            "Publish blocked because remote marketplace verification artifact is missing, failed, or stale.",
            exit_code=2,
            payload={"artifact_path": str(path), "errors": errors},
        )
    ledger_errors = validate_ledger_for_publish(ledger, gate)
    if ledger_errors:
        raise WorkflowError(
            "Publish blocked because post-verifier Issue Scope Ledger evidence is incomplete or invalid.",
            exit_code=2,
            payload={"ledger_path": str(issue_scope_ledger_path(task_dir)), "errors": ledger_errors},
        )
    gate_path, _gate, gate_errors = validate_review_gate(root, task_dir, config, True)
    if gate_errors:
        raise WorkflowError(
            "Publish blocked because Branch Review Gate became invalid after marketplace metadata tail.",
            exit_code=2,
            payload={"artifact_path": str(gate_path), "errors": gate_errors},
        )
    return path, payload


def cmd_verify_marketplace(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    repo = str(args.repo or config.get("github_repo") or "").strip() or infer_github_repo(root)
    if not repo:
        raise WorkflowError("Could not resolve GitHub repo for marketplace verification.")
    branch = str(args.branch or current_branch(root))
    remote = str(args.remote or publish_config(config).get("remote") or "origin")
    return execute_marketplace_verification(root, task_dir, repo, remote, branch, current_head(root), config)


def publish_recovery_command(
    root: Path,
    task_dir: Path,
    readiness_path: Path,
    repo: str,
    remote: str,
) -> list[str]:
    command = [
        ".trellis/guru-team/scripts/bash/publish-pr.sh", "--json",
        "--recovery-after-finish-work", "--allow-metadata-after-gate",
        "--task", repo_relative(root, task_dir),
        "--repo", repo, "--remote", remote,
        "--body-artifact", str(readiness_path),
    ]
    return command


def canonical_pull_request_url(repo: str, number: int, url: Any) -> str:
    value = str(url or "")
    match = re.fullmatch(
        r"https://github\.com/([^/]+)/([^/]+)/pull/([1-9][0-9]*)",
        value,
    )
    if (
        match is None
        or f"{match.group(1)}/{match.group(2)}".casefold() != repo.casefold()
        or int(match.group(3)) != number
    ):
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        )
    return value


def resolve_open_pull_request_for_recovery(
    root: Path,
    repo: str,
    branch: str,
    base_branch: str,
) -> dict[str, Any]:
    proc = run(
        [
            "gh", "pr", "list", "--repo", repo, "--head", branch,
            "--base", base_branch, "--state", "open", "--limit", "100",
            "--json", "number,url,headRefName,baseRefName",
        ],
        cwd=root,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError("Could not query the open PR for publish recovery.", exit_code=2, payload={"stderr": proc.stderr.strip()})
    try:
        values = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise WorkflowError("Open PR recovery query returned invalid JSON.", exit_code=2) from exc
    if not isinstance(values, list):
        raise WorkflowError("Open PR recovery query must return a JSON array.", exit_code=2)
    matches: list[dict[str, Any]] = []
    for index, item in enumerate(values):
        errors: list[str] = []
        if not isinstance(item, dict):
            errors.append("entry must be an object")
        else:
            number = item.get("number")
            if isinstance(number, bool) or not isinstance(number, int) or number < 1:
                errors.append("number must be a positive integer")
            if item.get("headRefName") != branch:
                errors.append("headRefName does not match the current head branch")
            if item.get("baseRefName") != base_branch:
                errors.append("baseRefName does not match the publish base branch")
            if not errors:
                canonical_pull_request_url(repo, number, item.get("url"))
                matches.append(item)
        if errors:
            raise WorkflowError(
                "Open PR recovery query returned an invalid or mismatched entry.",
                exit_code=2,
                payload={"entry_index": index, "errors": errors},
            )
    if len(matches) > 1:
        raise WorkflowError(
            "Publish recovery found multiple open PRs for the current head/base branch.",
            exit_code=2,
            payload={
                "repo": repo,
                "head_branch": branch,
                "base_branch": base_branch,
                "open_pr_count": len(matches),
            },
        )
    return {
        "state": "one" if matches else "none",
        "open_pr_count": len(matches),
        "pull_request": matches[0] if matches else None,
    }


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
            "gh", "pr", "create", "--repo", repo, "--base", base_branch,
            "--head", branch, "--title", title, "--body-file", body_file,
        ]
        if draft:
            command.append("--draft")
        proc = run(command, cwd=root, check=False)
        if proc.returncode != 0:
            raise WorkflowError(
                f"gh pr create failed:\n{proc.stderr.strip()}",
                exit_code=2,
            )
        pr_url = proc.stdout.strip()
        pull_request = parse_pull_request_number(pr_url)
        if pull_request is None:
            raise WorkflowError("gh pr create did not return a canonical PR URL.", exit_code=2)
        return canonical_pull_request_url(repo, pull_request, pr_url)
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
        errors.append("publish repo does not match task-start-context source_repo.repo")
    expected_branch = str(task_context.get("branch_name") or "").strip()
    if expected_branch and expected_branch != branch:
        errors.append("current head branch does not match task-start-context branch_name")
    normalized_base = normalize_ref(base_branch).removeprefix("origin/")
    for label, value in [
        ("task-start-context", task_context.get("base_branch")),
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


def update_finish_summary_for_pr(
    root: Path,
    task_dir: Path,
    task_context: dict[str, Any],
    pr_url: str,
) -> tuple[Path, dict[str, Any]]:
    path = task_dir / FINISH_SUMMARY_ARTIFACT
    payload = read_json(path)
    validate_finish_summary(payload, task_dir=task_dir)
    base_branch = str(task_context.get("base_branch") or payload.get("git", {}).get("base_branch") or "")
    base_ref = str(task_context.get("base_ref") or diff_base_ref(root, base_branch))
    changed_paths, protected_paths_filtered, snapshot_unavailable = finish_summary_git_path_snapshot(
        root, base_ref, include_worktree=False
    )
    updated = copy.deepcopy(payload)
    updated["git"]["changed_paths"] = changed_paths
    updated["github"]["pr_url"] = pr_url
    updated["artifacts"] = finish_summary_artifacts(task_dir)
    pr_match = re.search(r"/pull/([1-9][0-9]*)$", pr_url)
    if pr_match is None:
        raise WorkflowError("Cannot update finish-summary from a non-canonical PR URL.", exit_code=2)
    updated["index"]["search_terms"]["pr_refs"] = [f"PR #{pr_match.group(1)}"]
    updated["index"]["search_terms"]["paths"] = changed_paths
    apply_finish_summary_path_snapshot_contract(
        updated["index"],
        protected_paths_filtered=protected_paths_filtered,
        snapshot_unavailable=snapshot_unavailable,
    )
    updated["index"]["retrieval_text"] = finish_summary_retrieval_text(
        str(updated.get("task", {}).get("title") or ""), updated["index"]
    )
    validate_finish_summary(updated, task_dir=task_dir)
    write_json(path, updated)
    validate_finish_summary(read_json(path), task_dir=task_dir)
    return path, updated


def commit_and_push_finish_summary_metadata(
    root: Path,
    summary_path: Path,
    message: str,
    remote: str,
    branch: str,
) -> dict[str, Any]:
    relative = repo_relative(root, summary_path)
    allowed = {relative}
    dirty_paths = set(git_status_paths(root))
    unexpected = sorted(dirty_paths - allowed)
    if unexpected:
        raise WorkflowError(
            "finish-summary PR metadata tail contains unexpected dirty paths.",
            exit_code=2,
            payload={"allowed_paths": sorted(allowed), "unexpected_dirty_paths": unexpected},
        )
    previous_head = current_head(root)
    committed = False
    if relative in dirty_paths:
        run_stdout(["git", "add", "--", relative], cwd=root)
        staged_proc = run(["git", "diff", "--cached", "--name-only"], cwd=root, check=False)
        staged = {line.strip() for line in staged_proc.stdout.splitlines() if line.strip()}
        if staged_proc.returncode != 0 or staged != allowed:
            raise WorkflowError(
                "finish-summary staged metadata paths do not match the exact allowlist.",
                exit_code=2,
                payload={"allowed_paths": sorted(allowed), "staged_paths": sorted(staged)},
            )
        run_stdout(["git", "commit", "-m", message], cwd=root)
        committed = True
        committed_proc = run(["git", "diff", "--name-only", f"{previous_head}..HEAD"], cwd=root, check=False)
        committed_paths = {line.strip() for line in committed_proc.stdout.splitlines() if line.strip()}
        if committed_proc.returncode != 0 or committed_paths != allowed:
            raise WorkflowError(
                "finish-summary metadata commit contains unexpected paths.",
                exit_code=2,
                payload={"allowed_paths": sorted(allowed), "committed_paths": sorted(committed_paths)},
            )
    else:
        last_commit_proc = run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"], cwd=root, check=False)
        last_commit_paths = {line.strip() for line in last_commit_proc.stdout.splitlines() if line.strip()}
        if last_commit_proc.returncode != 0 or last_commit_paths != allowed:
            raise WorkflowError(
                "finish-summary recovery found no pending change and HEAD is not the exact summary metadata tail.",
                exit_code=2,
                payload={"allowed_paths": sorted(allowed), "head_paths": sorted(last_commit_paths)},
            )
    run_stdout(["git", "push", remote, branch], cwd=root)
    metadata_head = current_head(root)
    remote_proc = run(["git", "ls-remote", "--heads", remote, branch], cwd=root, check=False)
    remote_lines = [line.split() for line in remote_proc.stdout.splitlines() if line.strip()]
    remote_head = remote_lines[0][0] if remote_lines and remote_lines[0] else ""
    if remote_proc.returncode != 0 or remote_head != metadata_head:
        raise WorkflowError(
            "Remote branch does not contain the finish-summary metadata tail.",
            exit_code=2,
            payload={"metadata_head": metadata_head, "remote_head": remote_head},
        )
    return {
        "committed": committed,
        "previous_head": previous_head,
        "commit": metadata_head,
        "paths": sorted(allowed),
        "remote_head": remote_head,
    }


def cmd_publish_pr(args: argparse.Namespace) -> dict[str, Any]:
    validate_publish_invocation(args)
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    publish = publish_config(config)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    task = task_json(task_dir)
    base_branch = base_branch_from_sources(args, task, task_context)
    repo = str(args.repo or config.get("github_repo") or "").strip() or infer_github_repo(root)
    if not repo:
        raise WorkflowError("Could not resolve GitHub repo. Configure github_repo or pass --repo owner/repo.")

    dirty, dirty_paths = has_non_metadata_dirty_paths(root)
    if dirty:
        raise WorkflowError(
            "Working tree has uncommitted non-metadata changes. Commit task work before publish.",
            exit_code=2,
            payload={"dirty_paths": dirty_paths},
        )

    gate_path, gate, gate_errors = validate_review_gate(root, task_dir, config, args.allow_metadata_after_gate)
    if gate_errors:
        raise WorkflowError(
            "Publish blocked because Branch Review Gate is not valid for the current HEAD.",
            exit_code=2,
            payload={"artifact_path": str(gate_path), "errors": gate_errors},
        )

    ledger = load_issue_scope_ledger(task_dir, task_context)
    requires_marketplace_verification = marketplace_verification_required(gate)
    ledger_errors = validate_ledger_for_publish(
        ledger,
        gate,
        allow_pending_remote_marketplace=requires_marketplace_verification,
    )
    if ledger_errors:
        raise WorkflowError(
            "Publish blocked because Issue Scope Ledger is incomplete.",
            exit_code=2,
            payload={"ledger_path": str(issue_scope_ledger_path(task_dir)), "errors": ledger_errors},
        )

    branch = current_branch(root)
    remote = str(args.remote or publish.get("remote") or "origin")
    draft = bool(args.draft) if args.draft is not None else bool(publish.get("draft", False))
    title = pr_title_from_task(task, args)
    validations = list(args.validation or [])
    body, body_source = resolve_pr_body(root, args, ledger, gate, validations, config)
    readiness_path: Path | None = None
    publish_inputs: dict[str, Any] | None = None
    if not args.dry_run:
        if args.recovery_after_finish_work and getattr(args, "body_artifact", None) and any([
            getattr(args, "title", None),
            getattr(args, "body_file", None),
            getattr(args, "draft", None) is not None,
            validations,
            getattr(args, "base_branch", None),
        ]):
            raise WorkflowError(
                "Publish recovery forbids title/body/draft/base/validation overrides; use only pr-readiness.json.",
                exit_code=2,
            )
        readiness_path, publish_inputs, body = read_pr_readiness_publish_inputs(
            root,
            task_dir,
            getattr(args, "body_artifact", None),
            gate,
            require_committed=True,
        )
        configured_repo = repo
        repo = str(publish_inputs["repo"])
        if configured_repo.casefold() != repo.casefold():
            raise WorkflowError("Publish repo does not match immutable pr-readiness.json.", exit_code=2)
        base_branch = str(publish_inputs["base_branch"])
        if branch != publish_inputs["head_branch"]:
            raise WorkflowError("Current branch does not match immutable pr-readiness.json.", exit_code=2)
        title = str(publish_inputs["title"])
        draft = bool(publish_inputs["draft"])
        body_source = str(publish_inputs["reviewed_source"])
    primary_issue = primary_issue_number_from_ledger(ledger)
    merge_summary = merge_summary_from_title(title, primary_issue, ledger)
    base_branch_name = normalize_ref(base_branch).removeprefix("origin/")
    merge_commit = build_merge_commit_payload(
        primary_issue=primary_issue,
        summary=merge_summary,
        head_branch=branch,
        base_branch=base_branch_name,
        pull_request=None,
    )
    metadata_commit_subject = format_metadata_commit_subject(primary_issue)
    body_errors = validate_pr_body_quality(body, ledger, draft)
    reviewed_source_errors = validate_reviewed_body_source_for_publish(body_source, draft)
    if body_errors:
        raise WorkflowError(
            "Publish blocked because PR body is not reviewer-readable.",
            exit_code=2,
            payload={"errors": body_errors, "body_source": body_source},
        )
    if reviewed_source_errors and not args.dry_run:
        raise WorkflowError(
            "Publish blocked because non-draft PR body lacks reviewed source evidence.",
            exit_code=2,
            payload={
                "errors": reviewed_source_errors,
                "body_source": body_source,
                "reviewed_source_required": True,
                "reviewed_source_ok": False,
            },
        )

    archive_migration = None
    metadata_commit: dict[str, Any] | None = None
    if not args.dry_run:
        archive_migration = migrate_review_gate_for_archived_task(root, task_dir, config)
        if archive_migration.get("migrated"):
            metadata_commit = commit_if_metadata_dirty(root, metadata_commit_subject)

    payload: dict[str, Any] = {
        "status": "dry-run" if args.dry_run else "ok",
        "repo": repo,
        "base_branch": base_branch_name,
        "head_branch": branch,
        "remote": remote,
        "draft": draft,
        "title": title,
        "body": body,
        "body_source": body_source,
        "reviewed_source_required": not draft,
        "reviewed_source_ok": not reviewed_source_errors,
        "reviewed_source_errors": reviewed_source_errors,
        "review_gate": str(gate_path),
        "issue_scope_ledger": str(issue_scope_ledger_path(task_dir)),
        "archive_migration": archive_migration,
        "metadata_commit": metadata_commit,
        "merge_commit": merge_commit,
    }
    if args.dry_run:
        return payload

    require_gh_auth(root)
    if readiness_path is None or publish_inputs is None:
        raise WorkflowError("Formal publish requires immutable pr-readiness.json inputs.", exit_code=2)
    recovery_command = publish_recovery_command(root, task_dir, readiness_path, repo, remote)
    payload["recovery_command"] = recovery_command
    payload["recovery_command_shell"] = shlex.join(recovery_command)
    payload["publish_inputs_sha256"] = canonical_json_sha256(publish_inputs)
    try:
        run_stdout(["git", "push", "-u", remote, branch], cwd=root)
    except WorkflowError as exc:
        if not args.recovery_after_finish_work:
            raise
        details = dict(exc.payload)
        details.update({
            "failed_stage": "recovery-content-push",
            "pr_url": "",
            "publish_inputs": publish_inputs,
            "recovery_command": recovery_command,
            "recovery_command_shell": shlex.join(recovery_command),
        })
        raise WorkflowError(
            "Publish recovery could not push the current content HEAD.",
            exit_code=2,
            payload=details,
        ) from exc
    try:
        publish_identity = validate_publish_identity_and_remote_head(
            root,
            task,
            task_context,
            repo,
            base_branch_name,
            branch,
            remote,
        )
    except WorkflowError as exc:
        if not args.recovery_after_finish_work:
            raise
        details = dict(exc.payload)
        details.update({
            "failed_stage": "recovery-publish-identity",
            "pr_url": "",
            "publish_inputs": publish_inputs,
            "recovery_command": recovery_command,
            "recovery_command_shell": shlex.join(recovery_command),
        })
        raise WorkflowError(
            "Publish recovery identity or remote HEAD validation failed.",
            exit_code=2,
            payload=details,
        ) from exc
    payload["publish_identity"] = publish_identity
    verified_content_head = publish_identity["head"]
    if requires_marketplace_verification:
        if args.recovery_after_finish_work:
            try:
                _verification_path, marketplace_verification = validate_marketplace_publish_evidence(
                    root,
                    task_dir,
                    verified_content_head,
                    repo,
                    remote,
                    branch,
                    config,
                    ledger,
                    gate,
                )
            except WorkflowError as exc:
                details = dict(exc.payload)
                details.update({
                    "failed_stage": "recovery-marketplace-evidence",
                    "pr_url": "",
                    "publish_inputs": publish_inputs,
                    "recovery_command": recovery_command,
                    "recovery_command_shell": shlex.join(recovery_command),
                })
                raise WorkflowError(
                    "Publish recovery marketplace evidence validation failed.",
                    exit_code=2,
                    payload=details,
                ) from exc
            payload["marketplace_verification_reused"] = True
            publish_head = verified_content_head
        else:
            marketplace_verification = execute_marketplace_verification(
                root, task_dir, repo, remote, branch, verified_content_head, config
            )
            verification_artifact_path = marketplace_verification_path(task_dir, config)
            updated_ledger_path = write_remote_marketplace_evidence(
                root, task_dir, ledger, verification_artifact_path, marketplace_verification
            )
            verification_commit = commit_marketplace_verification_metadata(
                root, verification_artifact_path, updated_ledger_path, metadata_commit_subject
            )
            run_stdout(["git", "push", remote, branch], cwd=root)
            publish_head = current_head(root)
            ledger = load_issue_scope_ledger(task_dir, task_context)
            _verification_path, marketplace_verification = validate_marketplace_publish_evidence(
                root,
                task_dir,
                publish_head,
                repo,
                remote,
                branch,
                config,
                ledger,
                gate,
            )
            payload["marketplace_verification_commit"] = verification_commit
        payload["marketplace_verification"] = marketplace_verification
        payload["publish_head"] = publish_head
    else:
        payload["marketplace_verification"] = {"status": "not-required", "reason": "review gate changed_files do not touch marketplace/preset public extension assets"}
    pr_url = ""
    if args.recovery_after_finish_work:
        try:
            resolution = resolve_open_pull_request_for_recovery(
                root, repo, branch, base_branch_name
            )
        except WorkflowError as exc:
            details = dict(exc.payload)
            details.update({
                "failed_stage": "open-pr-query",
                "pr_url": "",
                "publish_inputs": publish_inputs,
                "recovery_command": recovery_command,
                "recovery_command_shell": shlex.join(recovery_command),
            })
            raise WorkflowError(
                "Publish recovery could not resolve a safe open PR state.",
                exit_code=2,
                payload=details,
            ) from exc
        recovered_pr = resolution.get("pull_request")
        if resolution["state"] == "one" and isinstance(recovered_pr, dict):
            pr_url = str(recovered_pr["url"])
            payload["pr_recovery"] = {
                "state": "one",
                "open_pr_count": 1,
                "reused_existing_open_pr": True,
                "created_after_zero_open_pr": False,
                "number": recovered_pr["number"],
                "url": pr_url,
            }
        else:
            try:
                pr_url = create_pull_request(
                    root, repo, base_branch_name, branch, title, body, draft
                )
            except WorkflowError as exc:
                details = dict(exc.payload)
                details.update({
                    "failed_stage": "gh-pr-create-recovery",
                    "pr_url": "",
                    "open_pr_count": 0,
                    "publish_inputs": publish_inputs,
                    "recovery_command": recovery_command,
                    "recovery_command_shell": shlex.join(recovery_command),
                })
                raise WorkflowError(
                    "Publish recovery found no open PR and its single create retry failed.",
                    exit_code=2,
                    payload=details,
                ) from exc
            pull_request = parse_pull_request_number(pr_url)
            payload["pr_recovery"] = {
                "state": "none",
                "open_pr_count": 0,
                "reused_existing_open_pr": False,
                "created_after_zero_open_pr": True,
                "number": pull_request,
                "url": pr_url,
            }
    else:
        try:
            pr_url = create_pull_request(
                root, repo, base_branch_name, branch, title, body, draft
            )
        except WorkflowError as exc:
            details = dict(exc.payload)
            details.update({
                "failed_stage": "gh-pr-create",
                "pr_url": "",
                "publish_inputs": publish_inputs,
                "recovery_command": recovery_command,
                "recovery_command_shell": shlex.join(recovery_command),
            })
            raise WorkflowError(
                str(exc),
                exit_code=2,
                payload=details,
            ) from exc
    payload["pr_url"] = pr_url
    pull_request = parse_pull_request_number(pr_url)
    if pull_request is None:
        raise WorkflowError(
            "Could not parse pull request number from publish PR URL.",
            exit_code=2,
            payload={
                "pr_url": pr_url,
                "publish_inputs": publish_inputs,
                "recovery_command": recovery_command,
                "recovery_command_shell": shlex.join(recovery_command),
            },
        )
    payload["merge_commit"] = build_merge_commit_payload(
        primary_issue=primary_issue,
        summary=merge_summary,
        head_branch=branch,
        base_branch=base_branch_name,
        pull_request=pull_request,
    )
    failed_stage = "finish-summary-rewrite"
    try:
        summary_path, _summary = update_finish_summary_for_pr(root, task_dir, task_context, pr_url)
        failed_stage = "finish-summary-metadata-commit-push"
        payload["finish_summary_metadata"] = commit_and_push_finish_summary_metadata(
            root, summary_path, metadata_commit_subject, remote, branch
        )
    except WorkflowError as exc:
        details = dict(exc.payload)
        details.update({
            "failed_stage": failed_stage,
            "pr_url": pr_url,
            "publish_inputs": publish_inputs,
            "recovery_command": recovery_command,
            "recovery_command_shell": shlex.join(recovery_command),
        })
        raise WorkflowError(
            "PR exists but finish-summary URL metadata recovery is incomplete.",
            exit_code=2,
            payload=details,
        ) from exc
    return payload


def build_finish_work_dry_run_plan(
    root: Path,
    args: argparse.Namespace,
    config: dict[str, Any],
    task_context: dict[str, Any],
    task_dir: Path,
    task_name: str,
    gate_path: Path,
    gate: dict[str, Any],
    reviewed_head: str,
    finish_summary_index_path: Path,
    draft: bool,
    body_source: str,
    body_errors: list[str],
    reviewed_source_errors: list[str],
    ledger: dict[str, Any],
) -> dict[str, Any]:
    publish = publish_config(config)
    task = task_json(task_dir)
    base_branch = base_branch_from_sources(args, task, task_context)
    repo = str(args.repo or config.get("github_repo") or "").strip() or infer_github_repo(root)
    remote = str(args.remote or publish.get("remote") or "origin")
    head_branch = current_branch(root)
    pr_title = pr_title_from_task(task, args)
    archive_would_run = not args.skip_archive
    primary_issue = primary_issue_number_from_ledger(ledger)
    merge_summary = merge_summary_from_title(pr_title, primary_issue, ledger)
    base_branch_name = normalize_ref(base_branch).removeprefix("origin/")
    return {
        "status": "dry-run",
        "task_dir": str(task_dir),
        "task_name": task_name,
        "review_gate": str(gate_path),
        "reviewed_head": reviewed_head,
        "dry_run_side_effects": False,
        "checks": {
            "non_metadata_dirty_paths": [],
            "pr_readiness": {
                "body_source": body_source,
                "body_quality_ok": not body_errors,
                "body_quality_errors": body_errors,
                "reviewed_source_required": not draft,
                "reviewed_source_ok": not reviewed_source_errors,
                "reviewed_source_errors": reviewed_source_errors,
            },
        },
        "plan": {
            "archive": {
                "would_run": archive_would_run,
                "skip": bool(args.skip_archive),
                "task_name": task_name,
                "command": ["python3", "./.trellis/scripts/task.py", "archive", task_name],
            },
            "finish_summary": {
                "would_run": True,
                "input_validated": True,
                "index_file": repo_relative(root, finish_summary_index_path),
                "target": repo_relative(
                    root,
                    root / ".trellis/tasks/archive" / datetime.now().strftime("%Y-%m") / task_name / FINISH_SUMMARY_ARTIFACT,
                ),
                "initial_pr_url": "",
                "initial_pr_refs": [],
            },
            "metadata_commit": {
                "would_run": True,
                "message": format_metadata_commit_subject(primary_issue),
            },
            "publish": {
                "would_run": True,
                "repo": repo,
                "base_branch": base_branch_name,
                "head_branch": head_branch,
                "remote": remote,
                "draft": draft,
                "title": pr_title,
                "body_source": body_source,
                "allow_metadata_after_gate": True,
                "from_finish_work": True,
                "merge_commit": build_merge_commit_payload(
                    primary_issue=primary_issue,
                    summary=merge_summary,
                    head_branch=head_branch,
                    base_branch=base_branch_name,
                    pull_request=None,
                ),
            },
        },
    }


def cmd_finish_work(args: argparse.Namespace) -> dict[str, Any]:
    validate_finish_work_invocation(args)
    root = repo_root(Path(args.root or os.getcwd()))
    config = load_config(root)
    task_dir = resolve_task_dir(root, args.task)
    task_context = load_task_start_context(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    gate_path, gate, gate_errors = validate_review_gate(root, task_dir, config, True)
    if gate_errors:
        raise WorkflowError(
            "finish-work blocked because Branch Review Gate is not valid for the current HEAD.",
            exit_code=2,
            payload={"artifact_path": str(gate_path), "errors": gate_errors},
        )

    dirty, dirty_paths = has_non_metadata_dirty_paths(root)
    if dirty:
        raise WorkflowError(
            "Working tree has uncommitted non-metadata changes. Commit task work before finish-work.",
            exit_code=2,
            payload={"dirty_paths": dirty_paths},
        )

    reviewed_head = str(gate.get("head") or current_head(root))
    task_name = args.task_name or task_dir.name
    finish_summary_index_path, finish_summary_index = load_finish_summary_index(
        task_dir, args.finish_summary_index_file
    )
    draft = bool(args.draft) if args.draft is not None else bool(publish_config(config).get("draft", False))

    ledger = load_issue_scope_ledger(task_dir, task_context)
    validations = list(args.validation or [])
    body, body_source = resolve_pr_body(root, args, ledger, gate, validations, config)
    body_errors = validate_pr_body_quality(body, ledger, draft)
    reviewed_source_errors = validate_reviewed_body_source_for_publish(body_source, draft)
    readiness_errors = body_errors + reviewed_source_errors
    if readiness_errors:
        raise WorkflowError(
            "finish-work blocked because PR readiness evidence is incomplete.",
            exit_code=2,
            payload={
                "errors": readiness_errors,
                "body_source": body_source,
                "reviewed_source_required": not draft,
                "reviewed_source_ok": not reviewed_source_errors,
            },
        )

    task_body_path = task_dir / PR_BODY_ARTIFACT
    task_body = read_pr_body_file(root, str(task_body_path))
    if task_body != body:
        raise WorkflowError(
            "finish-work PR readiness must bind the reviewed task-local pr-body.md bytes.",
            exit_code=2,
        )
    task = task_json(task_dir)
    readiness_repo = str(args.repo or config.get("github_repo") or "").strip() or infer_github_repo(root)
    if not readiness_repo:
        raise WorkflowError("Could not resolve GitHub repo for pr-readiness.json.", exit_code=2)
    readiness_base = base_branch_from_sources(args, task, task_context)
    readiness_title = pr_title_from_task(task, args)
    readiness_path, readiness_snapshot = build_pr_readiness_snapshot(
        root,
        task_dir,
        repo=readiness_repo,
        base_branch=readiness_base,
        head_branch=current_branch(root),
        reviewed_head_sha=reviewed_head,
        title=readiness_title,
        draft=draft,
    )

    if args.dry_run:
        plan = build_finish_work_dry_run_plan(
            root,
            args,
            config,
            task_context,
            task_dir,
            task_name,
            gate_path,
            gate,
            reviewed_head,
            finish_summary_index_path,
            draft,
            body_source,
            body_errors,
            reviewed_source_errors,
            ledger,
        )
        plan["pr_readiness_snapshot"] = {
            "artifact": str(readiness_path),
            "publish_inputs_sha256": readiness_snapshot["publish_inputs_sha256"],
            "would_write": False,
        }
        return plan

    write_json(readiness_path, readiness_snapshot)

    if not args.skip_archive:
        archive_script = root / ".trellis/scripts/task.py"
        if not archive_script.exists():
            raise WorkflowError(f"Trellis task.py not found: {archive_script}")
        proc = run(["python3", "./.trellis/scripts/task.py", "archive", task_name], cwd=root, check=False)
        if proc.returncode != 0:
            raise WorkflowError(f"task.py archive failed:\n{proc.stderr.strip()}", payload={"stdout": proc.stdout.strip()})

    primary_issue = primary_issue_number_from_ledger(ledger)
    metadata_commit_subject = format_metadata_commit_subject(primary_issue)
    archived_task_dir = resolve_existing_task_dir(root, task_name)
    if archived_task_dir is None or not task_dir_is_archived(root, archived_task_dir):
        raise WorkflowError(
            "finish-work could not resolve the archived task for finish-summary recording.",
            exit_code=2,
            payload={"task_name": task_name},
        )
    finish_summary = build_finish_summary(
        root,
        archived_task_dir,
        task_context,
        ledger,
        finish_summary_index,
        reviewed_head,
    )
    finish_summary_path = archived_task_dir / FINISH_SUMMARY_ARTIFACT
    write_json(finish_summary_path, finish_summary)
    validate_finish_summary(read_json(finish_summary_path), task_dir=archived_task_dir)
    publish_task = str(archived_task_dir)
    publish_body_artifact = str(readiness_path)
    archive_migration = migrate_review_gate_for_archived_task(root, archived_task_dir, config)
    metadata_commit = commit_if_metadata_dirty(root, metadata_commit_subject)
    publish_body_artifact = rewrite_active_task_artifact_path(root, task_dir, archived_task_dir, publish_body_artifact)
    publish_args = argparse.Namespace(
        root=str(root),
        task=publish_task,
        repo=args.repo,
        base_branch=args.base_branch,
        remote=args.remote,
        title=None,
        validation=[],
        body_file=None,
        body_artifact=publish_body_artifact,
        draft=None,
        allow_metadata_after_gate=True,
        dry_run=args.dry_run,
        from_finish_work=True,
        recovery_after_finish_work=False,
    )
    publish_payload = cmd_publish_pr(publish_args)
    return {
        "status": "dry-run" if args.dry_run else "ok",
        "task_dir": str(task_dir),
        "task_name": task_name,
        "review_gate": str(gate_path),
        "reviewed_head": reviewed_head,
        "finish_summary": str(finish_summary_path),
        "metadata_commit": metadata_commit,
        "archive_migration": archive_migration,
        "publish": publish_payload,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guru Team Trellis workflow helpers")
    sub = parser.add_subparsers(dest="command", required=True)

    check_env = sub.add_parser("check-env")
    check_env.add_argument("--root")
    check_env.add_argument("--json", action="store_true")

    version = sub.add_parser("version")
    version.add_argument("--root")
    version.add_argument("--json", action="store_true")

    boundary = sub.add_parser("check-workspace-boundary")
    boundary.add_argument("--root")
    boundary.add_argument("--json", action="store_true")
    boundary.add_argument("--task")
    boundary.add_argument(
        "--allow-source-clean",
        action="store_true",
        help="Allow a clean source checkout probe to report facts without failing on expected workspace mismatch.",
    )

    human_artifacts = sub.add_parser("resolve-human-artifacts")
    human_artifacts.add_argument("--root")
    human_artifacts.add_argument("--json", action="store_true")
    human_artifacts.add_argument("--task")

    verify_marketplace = sub.add_parser("verify-marketplace")
    verify_marketplace.add_argument("--root")
    verify_marketplace.add_argument("--json", action="store_true")
    verify_marketplace.add_argument("--task")
    verify_marketplace.add_argument("--repo")
    verify_marketplace.add_argument("--remote")
    verify_marketplace.add_argument("--branch")

    prepare = sub.add_parser("prepare")
    prepare.add_argument("--root")
    prepare.add_argument("--json", action="store_true")
    prepare.add_argument("--short-name")
    prepare.add_argument("--reuse-issue", type=int)
    prepare.add_argument("--force-new", action="store_true")
    prepare.add_argument("--create-issue-confirmed", action="store_true", help="Create a GitHub issue only after AI/human review confirmed the proposed title/body.")
    prepare.add_argument("--issue-title", help="Reviewed issue title used with --create-issue-confirmed.")
    prepare.add_argument("--issue-body-file", help="Path to reviewed issue body used with --create-issue-confirmed.")
    prepare.add_argument("--base-branch")
    prepare.add_argument("--branch")
    prepare.add_argument("--task-slug")
    prepare.add_argument("--workspace-slug")
    prepare.add_argument("--title")
    prepare.add_argument("--assignee")
    prepare.add_argument("--priority")
    prepare.add_argument("--description")
    prepare.add_argument("--worktree", action="store_true")
    prepare.add_argument("--create-worktree", action="store_true")
    prepare.add_argument("--create-task", action="store_true")
    prepare.add_argument("requirement", nargs="*")

    review = sub.add_parser("review-branch")
    review.add_argument("--root")
    review.add_argument("--json", action="store_true")
    review.add_argument("--task")
    review.add_argument("--base-branch")
    review.add_argument("--pass", dest="pass_gate", action="store_true")
    review.add_argument("--summary")
    review.add_argument("--evidence", action="append", help="Chinese review evidence line. Required with --pass.")
    review.add_argument("--reviewer", help="Reviewer name or AI/human review channel.")
    review.add_argument("--review-source", help="Review source metadata. Pass and findings records require independent-agent.")
    review.add_argument("--review-report", help="Path to the prior AI/human review report recorded before gate artifact creation.")
    review.add_argument("--agent-assignment", help="Task-local agent-assignment.json. Required with --pass to validate closure-before-final and fresh final reviewer evidence.")
    review.add_argument("--finding", action="append", help="Finding as PRIORITY|message[|path].")
    review.add_argument("--findings-file", help="JSON list or object with findings[].")
    review.add_argument("--observation", action="append", help="Non-blocking observation as message[|path].")
    review.add_argument("--observations-file", help="JSON list or object with observations[].")
    review.add_argument("--followup-candidate", action="append", help="Out-of-scope follow-up candidate as message[|path].")
    review.add_argument("--followup-candidates-file", help="JSON list or object with followup_candidates[].")
    review.add_argument("--dry-run", action="store_true")

    planning = sub.add_parser("record-planning-approval")
    planning.add_argument("--root")
    planning.add_argument("--json", action="store_true")
    planning.add_argument("--task")
    planning.add_argument("--reviewer", required=True, help="Reviewer name or AI/human review channel.")
    planning.add_argument("--summary", required=True, help="Chinese planning review conclusion.")
    planning.add_argument("--ambiguity-reviewer", required=True, help="AI reviewer that completed planning artifact ambiguity review.")
    planning.add_argument("--ambiguity-summary", required=True, help="Chinese ambiguity review conclusion before planning docs are shown for confirmation.")
    planning.add_argument(
        "--ambiguity-status",
        default=PLANNING_AMBIGUITY_STATUS_PASSED,
        help=f"Must be {PLANNING_AMBIGUITY_STATUS_PASSED}; non-passed ambiguity review cannot record planning approval.",
    )
    planning.add_argument("--user-confirmation", required=True, help="Evidence summary for user approval to enter implementation.")
    planning.add_argument(
        "--review-prompt-presented-at",
        help="ISO-8601 time when the AI presented prd.md/design.md/implement.md links for explicit post-planning review. Defaults to recorder time.",
    )
    planning.add_argument(
        "--confirmation-source",
        default=PLANNING_APPROVAL_CONFIRMATION_SOURCE,
        help=f"Must be {PLANNING_APPROVAL_CONFIRMATION_SOURCE}; Phase 0 handoff/workflow confirmation is rejected.",
    )
    planning.add_argument(
        "--normative-hit",
        action="append",
        help='AI-classified scan hit as "path|line|term|classification|reason". Unclassified hits and contract_violation block approval.',
    )
    planning.add_argument("--artifact", action="append", help="Task-local artifact path to approve. Defaults to existing prd/design/implement.")
    planning.add_argument("--dry-run", action="store_true")

    check_planning = sub.add_parser("check-planning-approval")
    check_planning.add_argument("--root")
    check_planning.add_argument("--json", action="store_true")
    check_planning.add_argument("--task")
    check_planning.add_argument(
        "--allow-committed-head",
        action="store_true",
        help="Compatibility flag; planning freshness is based on reviewed planning artifact digests, not HEAD drift.",
    )

    phase2 = sub.add_parser("record-phase2-check")
    phase2.add_argument("--root")
    phase2.add_argument("--json", action="store_true")
    phase2.add_argument("--task")
    phase2.add_argument("--pass", dest="pass_check", action="store_true")
    phase2.add_argument("--checker", required=True, help="Checker name or AI/human check channel.")
    phase2.add_argument("--summary", required=True, help="Chinese trellis-check conclusion.")
    phase2.add_argument("--checked-artifact", action="append", help="Task-local artifact read by the check. Defaults to existing task planning/gate artifacts.")
    phase2.add_argument("--checked-spec", action="append", help="Repo-relative .trellis/spec file read by the check.")
    phase2.add_argument("--coverage", action="append", help="Coverage key. Required keys: requirements, design, code, tests, spec_sync, cross_layer, docs_ssot, deployment.")
    phase2.add_argument("--validation", action="append", help="Validation command evidence as COMMAND or COMMAND|RESULT.")
    phase2.add_argument("--finding", action="append", help="Finding as PRIORITY|message[|path]. Add status in findings-file for resolved blocking findings.")
    phase2.add_argument("--findings-file", help="JSON list or object with findings[].")
    phase2.add_argument("--dry-run", action="store_true")

    check_phase2 = sub.add_parser("check-phase2-check")
    check_phase2.add_argument("--root")
    check_phase2.add_argument("--json", action="store_true")
    check_phase2.add_argument("--task")

    assignment = sub.add_parser("record-agent-assignment")
    assignment.add_argument("--root")
    assignment.add_argument("--json", action="store_true")
    assignment.add_argument("--task")
    assignment.add_argument("--logical-role", required=True, choices=ALLOWED_LOGICAL_ROLES)
    assignment.add_argument("--agent-id", default="", help="Technical platform agent id. Use empty string when unavailable and explain in --reason.")
    assignment.add_argument("--platform-nickname", default="", help="Display-only platform nickname; never used for gate decisions.")
    assignment.add_argument("--reason", help="Chinese AI/human assignment rationale for agents[].")
    assignment.add_argument("--review-round", type=int, help="Record a review_rounds[] entry instead of an agents[] entry.")
    assignment.add_argument("--review-round-report", help="Task-local reviews/*.md raw report for this review round. Required with --review-round.")
    assignment.add_argument("--reviewed-head", help="Reviewed HEAD for a review round. Defaults to current HEAD.")
    assignment.add_argument("--findings-count", type=int, default=0)
    assignment.add_argument("--reuse-policy", help="Chinese review reuse policy used for this review round.")
    assignment.add_argument("--reuse-decision", choices=sorted(ALLOWED_REUSE_DECISIONS), help="Record reuse/replacement decision.")
    assignment.add_argument("--reuse-reason", help="Chinese AI/human reason for reuse_decisions[].")
    assignment.add_argument("--from-round", type=int)
    assignment.add_argument("--to-round", type=int)
    assignment.add_argument("--decision-head", help="HEAD for reuse_decisions[]. Defaults to current HEAD.")
    assignment.add_argument("--status-event", help="Deprecated. Fails closed; use record-subagent-liveness-event.sh.")
    assignment.add_argument("--decision", help="Deprecated with --status-event.")
    assignment.add_argument("--observed-at", help="Deprecated with --status-event.")
    assignment.add_argument("--last-observed-progress-at", help="Deprecated with --status-event.")
    assignment.add_argument("--workspace-evidence", help="Deprecated with --status-event.")
    assignment.add_argument("--running-command-evidence", help="Deprecated with --status-event.")
    assignment.add_argument("--supersedes-agent-id", help="Deprecated with --status-event.")
    assignment.add_argument("--handoff-summary", help="Deprecated with --status-event.")
    assignment.add_argument("--dry-run", action="store_true")

    check_assignment = sub.add_parser("check-agent-assignment")
    check_assignment.add_argument("--root")
    check_assignment.add_argument("--json", action="store_true")
    check_assignment.add_argument("--task")
    check_assignment.add_argument("--agent-assignment", help="Task-local assignment artifact path. Defaults to agent-assignment.json.")
    check_assignment.add_argument("--require-current-head", action="store_true")

    liveness_record = sub.add_parser("record-subagent-liveness-event")
    liveness_record.add_argument("--root")
    liveness_record.add_argument("--json", action="store_true")
    liveness_record.add_argument("--task")
    liveness_record.add_argument("--source-repo", required=True)
    liveness_record.add_argument("--agent-id", required=True)
    liveness_record.add_argument("--event", required=True, choices=sorted(ALLOWED_AGENT_STATUS_EVENTS))
    liveness_record.add_argument("--observed-at", help="UTC ISO-8601 observation time. Defaults to now.")
    liveness_record.add_argument("--evidence", required=True)
    liveness_record.add_argument("--logical-role", choices=ALLOWED_LOGICAL_ROLES, help="Required for assigned.")
    liveness_record.add_argument("--platform-nickname", help="Required for assigned; empty string is accepted when the platform has no nickname.")
    liveness_record.add_argument("--source", default="main-session", choices=sorted(AGENT_STATUS_EVENT_SOURCES))
    liveness_record.add_argument("--predecessor-agent-id")
    liveness_record.add_argument("--predecessor-event-id")
    liveness_record.add_argument("--termination-reason", choices=sorted(AGENT_TERMINATION_REASONS))
    liveness_record.add_argument("--termination-source-event-id")
    liveness_record.add_argument("--replacement-reason", choices=sorted(AGENT_REPLACEMENT_REASONS))
    liveness_record.add_argument("--handoff-summary")
    liveness_record.add_argument("--dry-run", action="store_true")

    liveness_check = sub.add_parser("check-subagent-liveness")
    liveness_check.add_argument("--root")
    liveness_check.add_argument("--json", action="store_true")
    liveness_check.add_argument("--task")
    liveness_check.add_argument("--source-repo", required=True)
    liveness_check.add_argument("--agent-id", required=True)
    liveness_check.add_argument("--progress-scan-interval", type=int, default=AGENT_LIVENESS_DEFAULT_SCAN_INTERVAL_SECONDS)
    liveness_check.add_argument("--max-progress-silence", type=int, default=AGENT_LIVENESS_DEFAULT_MAX_SILENCE_SECONDS)
    liveness_check.add_argument("--checked-at", help=argparse.SUPPRESS)
    liveness_check.add_argument("--dry-run", action="store_true")

    check_gate = sub.add_parser("check-review-gate")
    check_gate.add_argument("--root")
    check_gate.add_argument("--json", action="store_true")
    check_gate.add_argument("--task")
    check_gate.add_argument("--allow-metadata-after-gate", action="store_true")

    check_commits = sub.add_parser("check-commit-messages")
    check_commits.add_argument("--root")
    check_commits.add_argument("--json", action="store_true")
    check_commits.add_argument("--task")
    check_commits.add_argument("--primary-issue", type=int)
    check_commits.add_argument("--base-ref", help="Git ref used as the start of the checked range. Defaults to the task base branch.")
    check_commits.add_argument("--range", help="Explicit git log range, for example origin/main..HEAD.")

    merge_commit = sub.add_parser("format-merge-commit")
    merge_commit.add_argument("--root")
    merge_commit.add_argument("--json", action="store_true")
    merge_commit.add_argument("--task")
    merge_commit.add_argument("--primary-issue", type=int)
    merge_commit.add_argument("--pull-request", help="Pull request number. Omit to produce a dry-run placeholder payload.")
    merge_commit.add_argument("--summary", help="Chinese PR summary used in the merge commit subject/body.")
    merge_commit.add_argument("--head-branch")
    merge_commit.add_argument("--base-branch")
    merge_commit.add_argument("--title", help=argparse.SUPPRESS)
    merge_commit.add_argument("--body-file-hint", default=MERGE_COMMIT_BODY_FILE_HINT)

    publish = sub.add_parser("publish-pr")
    publish.add_argument("--root")
    publish.add_argument("--json", action="store_true")
    publish.add_argument("--task")
    publish.add_argument("--repo")
    publish.add_argument("--base-branch")
    publish.add_argument("--remote")
    publish.add_argument("--title")
    publish.add_argument("--validation", action="append", help="Chinese validation evidence line for PR body.")
    publish.add_argument("--body-file", help="AI-reviewed Markdown PR body. Preferred over generated fallback.")
    publish.add_argument("--body-artifact", help="AI-reviewed JSON readiness artifact containing body or body_file.")
    publish.add_argument("--draft", dest="draft", action="store_true", default=None)
    publish.add_argument("--no-draft", dest="draft", action="store_false")
    publish.add_argument("--allow-metadata-after-gate", action="store_true")
    publish.add_argument(
        "--recovery-after-finish-work",
        action="store_true",
        help="Explicit recovery/debug path for rerunning publish after finish-work already completed.",
    )
    publish.add_argument("--dry-run", action="store_true")

    finish = sub.add_parser("finish-work")
    finish.add_argument("--root")
    finish.add_argument("--json", action="store_true")
    finish.add_argument("--task")
    finish.add_argument("--task-name", help="Task directory/name for task.py archive. Defaults to resolved task dir name.")
    finish.add_argument("--repo")
    finish.add_argument("--base-branch")
    finish.add_argument("--remote")
    finish.add_argument("--title", help="Chinese PR title override.")
    finish.add_argument("--validation", action="append", help="Chinese validation evidence line for PR body.")
    finish.add_argument("--body-file", help="AI-reviewed Markdown PR body passed through to publish-pr.")
    finish.add_argument("--body-artifact", help="AI-reviewed JSON readiness artifact passed through to publish-pr.")
    finish.add_argument("--draft", dest="draft", action="store_true", default=None)
    finish.add_argument("--no-draft", dest="draft", action="store_false")
    finish.add_argument(
        "--finish-summary-index-file",
        help="Task-local AI-authored finish-summary-index.json. Required for dry-run and formal finish.",
    )
    finish.add_argument(
        "--from-trellis-finish-work",
        action="store_true",
        help="Required intent marker set by the explicit trellis-finish-work entrypoint.",
    )
    finish.add_argument("--skip-archive", action="store_true", help="Internal recovery switch. Do not use in normal finish-work.")
    finish.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate finish-work readiness and print planned archive/finish-summary/publish actions without writing files.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "check-env":
            payload = check_env_payload(Path(args.root or os.getcwd()))
        elif args.command == "version":
            payload = cmd_version(args)
        elif args.command == "check-workspace-boundary":
            payload = cmd_check_workspace_boundary(args)
        elif args.command == "resolve-human-artifacts":
            payload = cmd_resolve_human_artifacts(args)
        elif args.command == "verify-marketplace":
            payload = cmd_verify_marketplace(args)
        elif args.command == "prepare":
            payload = cmd_prepare(args)
        elif args.command == "review-branch":
            payload = cmd_review_branch(args)
        elif args.command == "record-planning-approval":
            payload = cmd_record_planning_approval(args)
        elif args.command == "check-planning-approval":
            payload = cmd_check_planning_approval(args)
        elif args.command == "record-phase2-check":
            payload = cmd_record_phase2_check(args)
        elif args.command == "check-phase2-check":
            payload = cmd_check_phase2_check(args)
        elif args.command == "record-agent-assignment":
            payload = cmd_record_agent_assignment(args)
        elif args.command == "check-agent-assignment":
            payload = cmd_check_agent_assignment(args)
        elif args.command == "record-subagent-liveness-event":
            payload = cmd_record_subagent_liveness_event(args)
        elif args.command == "check-subagent-liveness":
            payload = cmd_check_subagent_liveness(args)
        elif args.command == "check-review-gate":
            payload = cmd_check_review_gate(args)
        elif args.command == "check-commit-messages":
            payload = cmd_check_commit_messages(args)
        elif args.command == "format-merge-commit":
            payload = cmd_format_merge_commit(args)
        elif args.command == "publish-pr":
            payload = cmd_publish_pr(args)
        elif args.command == "finish-work":
            payload = cmd_finish_work(args)
        else:
            raise WorkflowError(f"Unsupported command: {args.command}")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    except WorkflowError as exc:
        payload = {"status": "error", "error": str(exc), **exc.payload}
        if getattr(args, "json", False):
            print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
            if exc.payload:
                print(json.dumps(exc.payload, ensure_ascii=False, indent=2), file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
