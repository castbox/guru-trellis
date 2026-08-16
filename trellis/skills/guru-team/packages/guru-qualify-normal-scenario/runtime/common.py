from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path

from runtime.io import CommandError, read_json
from runtime.schema import validate_json


SKILL_ID = "guru-qualify-normal-scenario"
PROFILE_SCHEMAS = {
    "task_free_pre_write": "public-task-free-pre-write-input.schema.json",
    "task_free_evolution": "public-task-free-evolution-input.schema.json",
    "requirements_scope_set": "public-requirements-scope-set-input.schema.json",
    "change_request_candidate_set": "public-change-request-candidate-set-input.schema.json",
    "planning_scenario_set": "public-planning-scenario-set-input.schema.json",
    "implementation_discovery": "public-implementation-discovery-input.schema.json",
    "base_impact_candidate_set": "public-base-impact-candidate-set-input.schema.json",
    "phase2_candidate_set": "public-phase2-candidate-set-input.schema.json",
    "branch_review_candidate_set": "public-branch-review-candidate-set-input.schema.json",
    "publication_candidate_set": "public-publication-candidate-set-input.schema.json",
}
RESUME_TARGETS = {
    "task_free_pre_write": "guru-execute-task-free-change",
    "task_free_evolution": "guru-execute-task-free-change",
    "requirements_scope_set": "guru-clarify-requirements",
    "change_request_candidate_set": "guru-review-change-request",
    "planning_scenario_set": "guru-approve-task-plan",
    "implementation_discovery": "guru-resume-implementation",
    "base_impact_candidate_set": "guru-reconcile-task-base",
    "phase2_candidate_set": "guru-check-task",
    "branch_review_candidate_set": "guru-review-branch",
    "publication_candidate_set": "guru-review-task-publication",
}
CONSUMERS = {
    "classified": {"kind": "workflow", "id": "guru-normal-scenario-classified-router"},
    "scope_confirmation_required": {"kind": "skill", "id": "guru-clarify-requirements"},
    "mechanism_revision_required": {"kind": "workflow", "id": "guru-normal-scenario-mechanism-router"},
    "blocked": {"kind": "stop", "id": "normal-scenario-qualification-blocked"},
}
OUTPUT_SCHEMAS = {
    "classified": "public-classified-output.schema.json",
    "scope_confirmation_required": "public-scope-confirmation-required-output.schema.json",
    "mechanism_revision_required": "public-mechanism-revision-required-output.schema.json",
    "blocked": "public-blocked-output.schema.json",
}


def digest(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def parse(parser: argparse.ArgumentParser, argv: list[str]) -> argparse.Namespace:
    try:
        return parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the exact stdin-only command contract.") from exc


def stdin_object(value: str, field: str) -> dict:
    if value != "-":
        raise CommandError("invalid_arguments", field, "Use dash and provide the call-local JSON object on stdin.")
    return read_json("-", field)


def validate_public_input(package_root: Path, value: object) -> dict:
    if not isinstance(value, dict):
        raise CommandError("schema_mismatch", "public_input", "Provide one closed profile input object.")
    profile = value.get("profile")
    schema_name = PROFILE_SCHEMAS.get(profile)
    if schema_name is None:
        raise CommandError("schema_mismatch", "public_input.profile", "Use exactly one declared qualification profile.")
    validate_json(value, package_root / "schemas" / schema_name, "public_input")
    refs = value["candidate_refs"]
    locator_refs = [item["candidate_ref"] for item in value["candidate_locators"]]
    if len(locator_refs) != len(set(locator_refs)) or set(locator_refs) != set(refs):
        raise CommandError("schema_mismatch", "public_input.candidate_locators", "Bind exactly one locator set to every candidate ref.")
    _validate_locator(value["target_locator"], "public_input.target_locator")
    _validate_locator(value["target"]["repo_locator"], "public_input.target.repo_locator")
    for row in value["candidate_locators"]:
        for locator in row["locators"]:
            _validate_locator(locator, f"public_input.candidate_locators.{row['candidate_ref']}")
    return value


def _validate_locator(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise CommandError("unsafe_path", field, "Use a non-empty call-local locator.")
    path_value = value[5:] if value.startswith("path:") else value
    if path_value.startswith("/") or ".." in Path(path_value).parts:
        raise CommandError("unsafe_path", field, "Use a repository-relative locator without parent traversal.")


def _repo_root(public_input: dict) -> Path:
    locator = public_input["target"]["repo_locator"]
    candidate = Path(locator).resolve()
    if not candidate.is_dir() or candidate.is_symlink():
        raise CommandError("unsafe_path", "public_input.target.repo_locator", "Use the current regular repository root.")
    return candidate


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise CommandError("stale_identity", "public_input.target", "Reread the current Git identity and rerun qualification.", 3)
    return proc.stdout.strip()


def verify_current_facts(public_input: dict) -> None:
    repo = _repo_root(public_input)
    target = public_input["target"]
    current_head = _git(repo, "rev-parse", "HEAD")
    current_fields = {"checkout_head", "task_head", "review_head", "review_commit"}
    for key, value in target.items():
        if key.endswith("_head") or key == "review_commit":
            _git(repo, "cat-file", "-e", f"{value}^{{commit}}")
            if key in current_fields and value != current_head:
                raise CommandError("stale_identity", f"public_input.target.{key}", "Reread the current checkout HEAD and rerun qualification.", 3)
        if key.endswith("_path"):
            _validate_repo_path(repo, value, f"public_input.target.{key}", must_exist=True)
        elif key.endswith("_paths"):
            for index, item in enumerate(value):
                _validate_repo_path(repo, item, f"public_input.target.{key}.{index}", must_exist=False)
    for row in public_input["candidate_locators"]:
        for locator in row["locators"]:
            if locator.startswith("path:"):
                _validate_repo_path(repo, locator[5:].split(":", 1)[0], f"candidate.{row['candidate_ref']}", must_exist=True)


def _validate_repo_path(repo: Path, value: str, field: str, *, must_exist: bool) -> None:
    _validate_locator(value, field)
    candidate = repo / value
    current = repo
    for part in Path(value).parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise CommandError("unsafe_path", field, "Do not read qualification evidence through a symlink.")
    if must_exist and not candidate.is_file():
        raise CommandError("stale_identity", field, "Reread the current repository locator and rerun qualification.", 3)


def _authoring(recorded: dict) -> dict:
    return {key: copy.deepcopy(recorded[key]) for key in ("schema_version", "skill_id", "public_input", "candidate_results", "ai_review_gate", "typed_exit", "consumer")}


def record_value(package_root: Path, authored: object) -> dict:
    validate_json(authored, package_root / "schemas" / "semantic-result.schema.json", "semantic_result")
    assert isinstance(authored, dict)
    public_input = validate_public_input(package_root, authored["public_input"])
    candidate_refs = public_input["candidate_refs"]
    result_refs = [item["candidate_ref"] for item in authored["candidate_results"]]
    reviewed_refs = authored["ai_review_gate"]["reviewed_candidate_refs"]
    if len(result_refs) != len(set(result_refs)) or set(result_refs) != set(candidate_refs):
        raise CommandError("schema_mismatch", "candidate_results", "Provide exactly one decision for every input candidate and no extra decision.")
    if set(reviewed_refs) != set(candidate_refs):
        raise CommandError("schema_mismatch", "ai_review_gate.reviewed_candidate_refs", "Review the complete current candidate set.")
    exit_id = authored["typed_exit"]
    if authored["consumer"] != CONSUMERS[exit_id]:
        raise CommandError("schema_mismatch", "consumer", "Bind the AI-selected exit to its unique declared consumer.")
    recorded = copy.deepcopy(authored)
    recorded["input_sha256"] = digest(public_input)
    recorded["result_sha256"] = digest(recorded)
    return recorded


def check_value(package_root: Path, recorded: object) -> dict:
    if not isinstance(recorded, dict) or set(recorded) != {"schema_version", "skill_id", "public_input", "candidate_results", "ai_review_gate", "typed_exit", "consumer", "input_sha256", "result_sha256"}:
        raise CommandError("schema_mismatch", "recorded_result", "Use the exact stdout from the process-local recorder.")
    authored = _authoring(recorded)
    rebuilt = record_value(package_root, authored)
    if rebuilt != recorded:
        raise CommandError("stale_identity", "recorded_result", "Rerun the current semantic result through the recorder.", 3)
    verify_current_facts(recorded["public_input"])
    receipt = {
        "schema_version": "1.0",
        "skill_id": SKILL_ID,
        "input_sha256": recorded["input_sha256"],
        "result_sha256": recorded["result_sha256"],
        "typed_exit": recorded["typed_exit"],
        "consumer": copy.deepcopy(recorded["consumer"]),
    }
    receipt["receipt_sha256"] = digest(receipt)
    return receipt


def validate_receipt(recorded: dict, receipt: object) -> None:
    current = {
        "schema_version": "1.0",
        "skill_id": SKILL_ID,
        "input_sha256": recorded["input_sha256"],
        "result_sha256": recorded["result_sha256"],
        "typed_exit": recorded["typed_exit"],
        "consumer": copy.deepcopy(recorded["consumer"]),
    }
    current["receipt_sha256"] = digest(current)
    if receipt != current:
        raise CommandError("stale_identity", "validation_receipt", "Use the checker result from this exact call-local semantic result.", 3)


def typed_output(package_root: Path, recorded: dict) -> dict:
    public_input = recorded["public_input"]
    exit_id = recorded["typed_exit"]
    continuation_id = "normal-scenario:" + recorded["input_sha256"][:24]
    if exit_id == "classified":
        output = {"exit_id": exit_id, "profile": public_input["profile"], "mode": public_input["mode"], "resume_target": RESUME_TARGETS[public_input["profile"]], "continuation_id": continuation_id, "candidate_results": copy.deepcopy(recorded["candidate_results"])}
    elif exit_id == "scope_confirmation_required":
        output = {"exit_id": exit_id, "handoff_profile": "normal_scenario_scope_confirmation", "mode": public_input["mode"], "target_locator": public_input["target_locator"], "resume_target": RESUME_TARGETS[public_input["profile"]], "continuation_id": continuation_id, "candidate_refs": list(public_input["candidate_refs"])}
    elif exit_id == "mechanism_revision_required":
        output = {"exit_id": exit_id, "profile": public_input["profile"], "mode": public_input["mode"], "resume_target": RESUME_TARGETS[public_input["profile"]], "continuation_id": continuation_id, "candidate_results": copy.deepcopy(recorded["candidate_results"])}
    else:
        output = {"exit_id": "blocked"}
    validate_json(output, package_root / "schemas" / OUTPUT_SCHEMAS[exit_id], "stdout")
    return output
