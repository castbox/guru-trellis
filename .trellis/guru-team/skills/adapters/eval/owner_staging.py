from __future__ import annotations

from pathlib import Path
from typing import Any
import copy
import hashlib
import json
import os
import shutil

from adapters.eval.eval_constants import (
    OWNER_INPUT,
    OWNER_RESULT,
    PRODUCTION_SKILLS,
    QUALIFICATION_SKILL,
)

from adapters.eval.eval_support import (
    package_tree_sha256,
    qualification_runtime_environment,
    stage_qualification_public_authoring_fixture,
)

from adapters.eval.fixture_io import (
    bind_owner_result_argument,
    commit_qualification_owner_fixture,
    normalize_qualification_owner_extension,
    owner_recipe,
    run_git,
    stage_clean_installed_owner_repo,
    write_fake_gh,
)

from adapters.eval.owner_runtime import (
    load_package_owner_runtime,
    load_package_runtime_module,
)

from adapters.eval.production_fixtures import (
    stage_production_owner_execution,
)

from adapters.eval.stage0_fixtures import (
    bind_stage0_call_local_invocation,
    bind_sync_call_local_invocation,
    build_clarity_owner,
    build_context_owner,
    build_readiness_owner,
    build_task_free_change_owner,
    build_wording_owner,
    build_workflow_mode_owner,
    build_workspace_owner,
)


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
    readiness_invocation = None
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
            owner, readiness_state, change_request = build_readiness_owner(
                runtime,
                fixture,
                package,
                recipe,
                public_mode,
                str(public_payload.get("profile") or ""),
                str(public_payload["continuation_id"]),
            )
            readiness_invocation = readiness_state["invocation"]
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
            readiness_invocation,
        )
    elif skill_id != "guru-review-branch":
        bind_owner_result_argument(request, fixture, owner_path)
    return package, fixture_runtime_target, environment
