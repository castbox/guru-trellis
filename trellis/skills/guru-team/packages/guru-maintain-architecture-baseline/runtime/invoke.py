from __future__ import annotations

import argparse
import copy
import hashlib
import json
import stat
import sys
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json

PROFILES = {"bootstrap_foundation", "task_impact_sync", "promotion", "repair"}
PROFILE_SCHEMAS = {
    "bootstrap_foundation": "public-input-bootstrap.schema.json",
    "task_impact_sync": "public-input-impact.schema.json",
    "promotion": "public-input-promotion.schema.json",
    "repair": "public-input-repair.schema.json",
}
EXITS = {
    "baseline_current": "public-baseline-current-output.schema.json",
    "sync_required": "public-sync-required-output.schema.json",
    "baseline_incomplete": "public-baseline-incomplete-output.schema.json",
    "architecture_conflict": "public-architecture-conflict-output.schema.json",
    "contract_incomplete": "public-contract-incomplete-output.schema.json",
    "fitness_regression": "public-fitness-regression-output.schema.json",
    "blocked": "public-blocked-output.schema.json",
}
CONSUMERS = {
    "baseline_current": {"kind": "workflow", "id": "guru-architecture-baseline-current-router"},
    "sync_required": {"kind": "skill", "id": "guru-maintain-architecture-baseline"},
    "baseline_incomplete": {"kind": "workflow", "id": "guru-architecture-baseline-bootstrap-router"},
    "architecture_conflict": {"kind": "workflow", "id": "guru-architecture-baseline-planning-router"},
    "contract_incomplete": {"kind": "workflow", "id": "guru-architecture-baseline-planning-router"},
    "fitness_regression": {"kind": "workflow", "id": "guru-architecture-baseline-check-router"},
    "blocked": {"kind": "stop", "id": "architecture-baseline-blocked"},
}
OUTPUT_FIELDS = {
    "baseline_current": ("task_locator", "stage", "baseline_identity", "constitution_identity", "impact_kind", "promotion_state", "contribution_locator", "contribution_identity", "freshness_identity"),
    "sync_required": ("task_locator", "stage", "sync_kind", "expected_current_identity", "current_identity", "sync_target", "freshness_identity"),
    "baseline_incomplete": ("authority_locator", "missing_refs", "repair_profile"),
    "architecture_conflict": ("task_locator", "stage", "conflict_refs", "return_route"),
    "contract_incomplete": ("task_locator", "stage", "missing_refs", "return_route"),
    "fitness_regression": ("task_locator", "stage", "regression_refs", "return_route"),
    "blocked": ("reason_code", "remediation"),
}


def _digest(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _json(value: str, field: str, locator: bool = False) -> dict:
    if value == "-":
        value = sys.stdin.read()
    elif locator:
        path = Path(value)
        if not path.is_absolute():
            path = Path.cwd() / path
        if not path.is_file() or path.is_symlink():
            raise CommandError("unsafe_path", field, "Use a safe regular JSON file.")
        value = path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise CommandError("invalid_json", field, "Provide one valid JSON object.") from exc
    if not isinstance(parsed, dict):
        raise CommandError("invalid_json", field, "Provide one valid JSON object.")
    return parsed


def _schema(package_root: Path, name: str) -> Path:
    path = package_root / "schemas" / name
    if not path.is_file() or path.is_symlink():
        raise CommandError("schema_mismatch", name, "Restore the declared package schema.")
    return path


def _locator(value: object, field: str) -> None:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise CommandError("unsafe_path", field, "Use a non-empty repository-relative locator.")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise CommandError("unsafe_path", field, "Use a repository-relative locator without parent traversal.")


def _require_current_constitution(constitution: dict, field: str) -> None:
    if constitution["authority_status"] != "current":
        raise CommandError(
            "semantic_result_invalid",
            f"{field}.authority_status",
            "baseline_current requires a promoted current design-constitution authority.",
            3,
        )
    locator = constitution["authority_locator"]
    _locator(locator, f"{field}.authority_locator")
    parts = Path(locator).parts
    if not parts:
        raise CommandError(
            "unsafe_path",
            f"{field}.authority_locator",
            "Current design-constitution authority must resolve to a regular repository file.",
        )
    current = Path.cwd()
    for part in parts:
        current /= part
        try:
            current_stat = current.lstat()
        except OSError as exc:
            raise CommandError(
                "unsafe_path",
                f"{field}.authority_locator",
                "Current design-constitution authority must resolve to a regular repository file.",
            ) from exc
        if stat.S_ISLNK(current_stat.st_mode):
            raise CommandError(
                "unsafe_path",
                f"{field}.authority_locator",
                "Current design-constitution authority cannot use a symlink-backed locator.",
            )
    if not stat.S_ISREG(current_stat.st_mode):
        raise CommandError(
            "unsafe_path",
            f"{field}.authority_locator",
            "Current design-constitution authority must resolve to a regular repository file.",
        )


def _bind_identity(public: dict, owner: dict, field: str) -> None:
    if owner.get(field) != public.get(field):
        raise CommandError("stale_identity", f"owner_result.{field}", "Reread current architecture authority and repeat semantic review.", 3)


def _check_project_checks(
    descriptors: object,
    checks: object,
    freshness_identity: str,
    field: str,
) -> None:
    descriptor_field = "owner_result.project_check_descriptors"
    if not isinstance(descriptors, list) or not descriptors:
        raise CommandError(
            "semantic_result_invalid",
            descriptor_field,
            "Architecture impact requires the current project Architecture check descriptors.",
            3,
        )
    if not isinstance(checks, list) or not checks:
        raise CommandError("semantic_result_invalid", field, "Architecture impact requires current project Architecture checks.", 3)
    descriptors_by_identity: dict[str, tuple[int, dict]] = {}
    for index, descriptor in enumerate(descriptors):
        descriptor_item_field = f"{descriptor_field}.{index}"
        identity = descriptor["descriptor_identity"]
        if identity in descriptors_by_identity:
            raise CommandError(
                "semantic_result_invalid",
                descriptor_item_field,
                "Declare exactly one current project Architecture check descriptor identity.",
                3,
            )
        _locator(descriptor["entrypoint"], f"{descriptor_item_field}.entrypoint")
        descriptors_by_identity[identity] = (index, descriptor)
    checks_by_identity: dict[str, int] = {}
    for index, check in enumerate(checks):
        check_field = f"{field}.{index}"
        identity = check["descriptor_identity"]
        if identity in checks_by_identity:
            raise CommandError(
                "semantic_result_invalid",
                check_field,
                "Record exactly one result for each project Architecture check descriptor identity.",
                3,
            )
        checks_by_identity[identity] = index
        descriptor_entry = descriptors_by_identity.get(identity)
        if descriptor_entry is None:
            raise CommandError(
                "semantic_result_invalid",
                check_field,
                "Bind every project Architecture check result to one current owner-reviewed descriptor identity.",
                3,
            )
        descriptor_index, descriptor = descriptor_entry
        for binding_field in (
            "check_id",
            "check_version",
            "applicable_scope",
            "rule_refs",
            "decision_refs",
            "gap_refs",
        ):
            check_value = check[binding_field]
            descriptor_value = descriptor[binding_field]
            if isinstance(check_value, list):
                matches = set(check_value) == set(descriptor_value)
            else:
                matches = check_value == descriptor_value
            if not matches:
                raise CommandError(
                    "semantic_result_invalid",
                    f"{check_field}.{binding_field}",
                    f"Bind the result {binding_field} to owner_result.project_check_descriptors.{descriptor_index}.{binding_field}.",
                    3,
                )
        if check["freshness_identity"] != freshness_identity:
            raise CommandError("stale_identity", f"{check_field}.freshness_identity", "Rerun the project Architecture check for this invocation.", 3)
        status = check["status"]
        evidence_locator = check.get("evidence_locator")
        unavailable_reason = check.get("unavailable_reason")
        if status in {"pass", "fail"}:
            if not evidence_locator or unavailable_reason is not None:
                raise CommandError("semantic_result_invalid", check_field, "A passed or failed project check requires evidence and cannot carry an unavailable reason.", 3)
            _locator(evidence_locator, f"{check_field}.evidence_locator")
        elif status == "unverified":
            if not unavailable_reason or evidence_locator is not None:
                raise CommandError("semantic_result_invalid", check_field, "An unverified project check requires an unavailable reason and cannot carry evidence.", 3)
        if check["applicability"] == "not_applicable" and (
            check["blocking"] or check["status"] != "pass"
        ):
            raise CommandError(
                "semantic_result_invalid",
                f"{check_field}.applicability",
                "A not-applicable project check requires non-blocking passed evidence that proves the current applicability decision.",
                3,
            )
        if check["blocking"] and check["status"] != "pass":
            raise CommandError("semantic_result_invalid", f"{check_field}.status", "A blocking failed or unverified project check cannot produce baseline_current.", 3)
    extra_descriptors = set(descriptors_by_identity) - set(checks_by_identity)
    if extra_descriptors:
        descriptor_index, _ = descriptors_by_identity[sorted(extra_descriptors)[0]]
        raise CommandError(
            "semantic_result_invalid",
            f"{descriptor_field}.{descriptor_index}",
            "Every current project Architecture check descriptor requires exactly one bound result.",
            3,
        )


def _check_review(review: object, expected_range: object, field: str) -> None:
    if (
        not isinstance(review, dict)
        or review.get("status") != "reviewed"
        or review.get("independent") is not True
        or review.get("committed_range") != expected_range
    ):
        raise CommandError(
            "semantic_result_invalid",
            field,
            "This stage requires an independent review of the exact caller-supplied committed range.",
            3,
        )


def _check_sync_route(value: dict, field: str) -> None:
    target = value["sync_target"]
    _locator(target["locator"], f"{field}.sync_target.locator")
    sync_kind = value["sync_kind"]
    expected_current = value["expected_current_identity"]
    current = value["current_identity"]
    target_expected = target["expected_identity"]
    target_current = target["current_identity"]
    if sync_kind == "promotion_required":
        if expected_current != current:
            raise CommandError("semantic_result_invalid", f"{field}.current_identity", "promotion_required must preserve the expected live current baseline identity.", 3)
        if target["kind"] != "contribution" or target_expected != target_current:
            raise CommandError("semantic_result_invalid", f"{field}.sync_target", "promotion_required must target one current reviewed contribution identity.", 3)
    elif sync_kind == "baseline_advanced":
        if expected_current == current:
            raise CommandError("semantic_result_invalid", f"{field}.current_identity", "baseline_advanced requires different expected and current baseline identities.", 3)
        if (
            target["kind"] != "baseline"
            or target_expected != expected_current
            or target_current != current
        ):
            raise CommandError("semantic_result_invalid", f"{field}.sync_target", "baseline_advanced must bind the same expected/current baseline pair.", 3)
    elif sync_kind == "constitution_advanced":
        if target["kind"] != "constitution" or target_expected == target_current:
            raise CommandError("semantic_result_invalid", f"{field}.sync_target", "constitution_advanced requires different constitution identities.", 3)
    elif sync_kind == "contribution_stale":
        if target["kind"] != "contribution" or target_expected == target_current:
            raise CommandError("semantic_result_invalid", f"{field}.sync_target", "contribution_stale requires different contribution identities.", 3)
    elif sync_kind == "repair":
        project_contract = value["project_contract"]
        if expected_current != current:
            raise CommandError("semantic_result_invalid", f"{field}.current_identity", "repair must preserve the current baseline identity.", 3)
        if (
            target["kind"] != "project_contract"
            or target["locator"] != project_contract["change_contract_locator"]
            or target_expected != target_current
            or target_current != project_contract["change_contract_identity"]
        ):
            raise CommandError("semantic_result_invalid", f"{field}.sync_target", "repair must bind the current project Architecture change-contract identity.", 3)


def _check_architecture_current(public: dict, recorded: dict) -> None:
    if not recorded.get("impact_reason"):
        raise CommandError("semantic_result_invalid", "owner_result.impact_reason", "Record the reviewed Architecture impact reason.", 3)
    if recorded["impact_kind"] == "architecture_impact":
        for field in (
            "change_path",
            "contribution_locator",
            "contribution_identity",
            "project_check_descriptors",
            "project_checks",
        ):
            if field not in recorded:
                raise CommandError("semantic_result_invalid", f"owner_result.{field}", "Architecture impact requires the reviewed task-local contribution and bound project checks.", 3)
        if recorded.get("promotion_state") not in {"reviewed_candidate", "reviewed_promoted"}:
            raise CommandError("semantic_result_invalid", "owner_result.promotion_state", "Architecture impact requires a reviewed candidate or reviewed promoted contribution.", 3)
        _check_project_checks(
            recorded["project_check_descriptors"],
            recorded["project_checks"],
            public["freshness_identity"],
            "owner_result.project_checks",
        )
        if public["stage"] == "branch_review":
            _check_review(
                recorded.get("review"),
                public.get("committed_range"),
                "owner_result.review",
            )
        if public["stage"] in {"publication", "acceptance_finish"} and recorded["promotion_state"] != "reviewed_promoted":
            raise CommandError("semantic_result_invalid", "owner_result.promotion_state", "Publication and Finish require reviewed promotion.", 3)
    else:
        if recorded["promotion_state"] != "no_change":
            raise CommandError("semantic_result_invalid", "owner_result.promotion_state", "No-impact work must project no_change.", 3)
        for field in (
            "change_path",
            "contribution_locator",
            "contribution_identity",
            "project_check_descriptors",
            "project_checks",
            "review",
        ):
            if field in recorded:
                raise CommandError("semantic_result_invalid", f"owner_result.{field}", "No-impact work cannot create Architecture contribution or check burden.", 3)


def _check_owner_result(package_root: Path, public: dict, owner: dict) -> dict:
    recorded = copy.deepcopy(owner)
    validate_json(recorded, _schema(package_root, "semantic-result.schema.json"), "owner_result")
    if recorded["input_sha256"] != _digest(public):
        raise CommandError("stale_identity", "owner_result.input_sha256", "Rerun semantic review against the exact current 2.0 input.", 3)
    for field in (
        "profile",
        "mode",
        "continuation_id",
        "stage",
        "task_locator",
        "baseline",
        "constitution",
        "project_contract",
        "freshness_identity",
    ):
        _bind_identity(public, recorded, field)
    if public["profile"] == "promotion":
        for field in ("expected_current_identity", "current_identity", "sync_kind", "sync_target"):
            _bind_identity(public, recorded, field)
        _check_sync_route(public, "public_input")
    exit_id = recorded["typed_exit"]
    if recorded["consumer"] != CONSUMERS[exit_id]:
        raise CommandError("semantic_result_invalid", "owner_result.consumer", "Use the unique consumer declared for this exit.", 3)
    gate_status = recorded["ai_review_gate"]["status"]
    if (exit_id == "blocked") != (gate_status == "blocked"):
        raise CommandError("semantic_result_invalid", "owner_result.ai_review_gate.status", "Blocked requires a blocked gate; every other exit requires a passed gate.", 3)
    for container, name in ((public, "public_input"), (recorded, "owner_result")):
        for field in ("task_locator", "authority_locator", "contribution_locator"):
            if field in container:
                _locator(container[field], f"{name}.{field}")
        _locator(container["baseline"]["locator"], f"{name}.baseline.locator")
        _locator(container["constitution"]["authority_locator"], f"{name}.constitution.authority_locator")
        _locator(container["project_contract"]["change_contract_locator"], f"{name}.project_contract.change_contract_locator")
        if "sync_target" in container:
            _locator(container["sync_target"]["locator"], f"{name}.sync_target.locator")
    if exit_id == "baseline_current":
        _require_current_constitution(public["constitution"], "public_input.constitution")
        expected_baseline_identity = public["baseline"]["identity"]
        if public["profile"] == "bootstrap_foundation":
            successor = public["successor_baseline"]
            if successor["locator"] != public["baseline"]["locator"]:
                raise CommandError(
                    "semantic_result_invalid",
                    "public_input.successor_baseline.locator",
                    "Bootstrap must activate the successor at the same Architecture Baseline locator.",
                    3,
                )
            if successor["identity"] == public["baseline"]["identity"]:
                raise CommandError(
                    "semantic_result_invalid",
                    "public_input.successor_baseline.identity",
                    "Bootstrap must activate a distinct successor Architecture Baseline identity.",
                    3,
                )
            expected_baseline_identity = successor["identity"]
        if recorded["baseline_identity"] != expected_baseline_identity:
            raise CommandError("stale_identity", "owner_result.baseline_identity", "Reread the live baseline identity.", 3)
        if recorded["constitution_identity"] != public["constitution"]["identity"]:
            raise CommandError("stale_identity", "owner_result.constitution_identity", "Reread the live constitution identity.", 3)
        if public["profile"] == "task_impact_sync":
            _check_architecture_current(public, recorded)
        elif public["profile"] == "promotion":
            _check_architecture_current(public, recorded)
            sync_kind = public["sync_kind"]
            target = public["sync_target"]
            if sync_kind == "promotion_required":
                if recorded.get("impact_kind") != "architecture_impact" or recorded.get("promotion_state") != "reviewed_promoted":
                    raise CommandError("semantic_result_invalid", "owner_result.promotion_state", "Successful promotion must return reviewed_promoted architecture impact.", 3)
                _check_review(
                    recorded.get("review"),
                    public["committed_range"],
                    "owner_result.review",
                )
                if (
                    recorded.get("contribution_locator") != target["locator"]
                    or recorded.get("contribution_identity") != target["current_identity"]
                ):
                    raise CommandError("stale_identity", "owner_result.contribution_identity", "Reread the current reviewed contribution before promotion.", 3)
                if public["baseline"]["identity"] == public["expected_current_identity"]:
                    raise CommandError("semantic_result_invalid", "public_input.baseline.identity", "Successful promotion must expose a successor current baseline identity.", 3)
            elif sync_kind == "baseline_advanced":
                if (
                    public["baseline"]["locator"] != target["locator"]
                    or public["baseline"]["identity"] != target["current_identity"]
                ):
                    raise CommandError("stale_identity", "public_input.baseline", "Reread the advanced current baseline before resuming the stage.", 3)
            elif sync_kind == "constitution_advanced":
                if (
                    public["constitution"]["authority_locator"] != target["locator"]
                    or public["constitution"]["identity"] != target["current_identity"]
                ):
                    raise CommandError("stale_identity", "public_input.constitution", "Reread the advanced design constitution before resuming the stage.", 3)
            elif sync_kind == "contribution_stale" and recorded["impact_kind"] == "architecture_impact":
                if (
                    recorded.get("contribution_locator") != target["locator"]
                    or recorded.get("contribution_identity") != target["current_identity"]
                ):
                    raise CommandError("stale_identity", "owner_result.contribution_identity", "Reread the current task contribution before resuming the stage.", 3)
    if exit_id == "sync_required":
        _check_sync_route(recorded, "owner_result")
    return recorded


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--invocation")
    parser.add_argument("--input")
    parser.add_argument("--owner-result")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the exact command help contract.") from exc
    if bool(args.invocation) == bool(args.input):
        raise CommandError("invalid_arguments", "arguments", "Provide exactly one invocation or public input transport.")
    if args.input and not args.owner_result:
        raise CommandError("invalid_arguments", "owner_result", "Provide a completed semantic owner result.")
    envelope = _json(args.invocation, "invocation") if args.invocation else None
    public = envelope.get("public_input") if envelope else _json(args.input, "input", True)
    owner = envelope.get("owner_result") if envelope else _json(args.owner_result, "owner_result", True)
    if not isinstance(public, dict) or not isinstance(owner, dict):
        raise CommandError("invalid_arguments", "owner_result", "Provide a completed semantic owner result.")
    if public.get("schema_version") != "2.0":
        raise CommandError("schema_mismatch", "schema_version", "Architecture Baseline accepts only the closed 2.0 contract.")
    profile = public.get("profile")
    if profile not in PROFILES:
        raise CommandError("schema_mismatch", "profile", "Use one declared Architecture Baseline profile.")
    validate_json(public, _schema(package_root, PROFILE_SCHEMAS[profile]), "input")
    owner = _check_owner_result(package_root, public, owner)
    exit_id = owner["typed_exit"]
    output = {"exit_id": exit_id}
    for key in OUTPUT_FIELDS[exit_id]:
        if key in owner:
            output[key] = owner[key]
    if exit_id == "baseline_current" and owner.get("impact_kind") == "no_architecture_impact":
        output["impact_reason"] = owner["impact_reason"]
    if exit_id == "baseline_current":
        output["source_profile"] = owner["profile"]
        output["constitution_status"] = owner["constitution"]["authority_status"]
    validate_json(output, _schema(package_root, EXITS[exit_id]), "stdout")
    return copy.deepcopy(output)
