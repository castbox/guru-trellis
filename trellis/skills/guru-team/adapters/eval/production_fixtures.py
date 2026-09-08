from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess

from adapters.eval.eval_constants import (
    OWNER_INPUT,
    OWNER_INVOCATION,
    OWNER_RESULT,
)

from adapters.eval.fixture_io import (
    bind_merge_gate_argument,
    bind_owner_result_argument,
    bind_review_input_argument,
    run_git,
    write_fake_gh,
    write_fake_merge_gh,
)

from adapters.eval.owner_runtime import (
    compose_production_fixture_runtime,
    compose_production_owner_command_runtime,
    load_package_owner_runtime,
)


def production_task_fixture(runtime: Any, fixture: Path) -> tuple[Path, str]:
    (fixture / ".trellis/guru-team/config.yml").write_text(
        "workspace_mode: current\n", encoding="utf-8",
    )
    task = fixture / ".trellis/tasks/current"
    task.mkdir(parents=True, exist_ok=True)
    runtime.write_json(task / "task.json", {
        "id": "current",
        "name": "current",
        "title": "Production minimal handoff eval",
        "status": "planning",
        "scope": "issue #146",
        "branch": "eval/current",
        "base_branch": "main",
    })
    for name, content in {
        "prd.md": (
            "# PRD\n\n## R1. Production eval\n\n"
            "The production eval uses the public package boundary.\n"
        ),
        "design.md": (
            "# Design\n\n## Docs SSOT Plan\n\n"
            "Strategy: ssot_first. Durable requirements own the contract.\n"
        ),
        "implement.md": (
            "# Implement\n\nExecute the recorder, checker, and public wrapper.\n"
        ),
    }.items():
        (task / name).write_text(content, encoding="utf-8")
    issue = {
        "number": 146,
        "url": "https://github.com/example/guru-extension/issues/146",
        "title": "Production minimal handoff eval",
        "reason": "The current production eval delivery scope.",
    }
    runtime.write_json(task / "issue-scope-ledger.json", {
        "schema_version": "2.0",
        "primary_issue": issue,
        "close_issues": [issue],
        "related_issues": [],
        "followup_issues": [],
    })
    durable = fixture / "docs/requirements.md"
    durable.parent.mkdir(parents=True, exist_ok=True)
    durable.write_text(
        "# Requirements\n\nThe public wrapper owns the production eval boundary.\n",
        encoding="utf-8",
    )
    source = fixture / "src/production-eval.txt"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("baseline\n", encoding="utf-8")
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-q", "-m", "stage production owner fixture")
    base_head = run_git(fixture, "rev-parse", "HEAD")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", base_head)
    run_git(fixture, "remote", "add", "origin", "https://github.com/example/guru-extension.git")
    run_git(fixture, "checkout", "-q", "-b", "eval/current")
    runtime.write_runtime_mappings(
        fixture,
        runtime.load_config(fixture),
        {
            "workspace_slug": "current",
            "task_slug": "current",
            "task_dir": ".trellis/tasks/current",
            "branch_name": "eval/current",
        },
        fixture,
    )
    return task, base_head

def production_planning_input(
    runtime: Any, fixture: Path, task: Path, exit_id: str,
) -> Path:
    statuses = {
        "approved": "passed",
        "revision_required": "revision_required",
        "clarify_scope": "clarify_scope",
        "blocked": "blocked",
    }
    consumers = {
        "approved": {"kind": "workflow", "id": "phase-1-task-activation"},
        "revision_required": {"kind": "skill", "id": "guru-approve-task-plan"},
        "clarify_scope": {
            "kind": "workflow", "id": "guru-task-plan-clarify-scope-router",
        },
        "blocked": {"kind": "stop", "id": "task-plan-approval-blocked"},
    }
    status = statuses[exit_id]
    semantic_review = {
        "status": status,
        "summary": "The exact production planning case completed semantic review.",
        "checked_dimensions": {
            "requirement_authority": True,
            "scope_boundary": True,
            "design_adequacy": True,
            "implementation_plan": True,
            "acceptance_verifiability": True,
            "docs_ssot": True,
            "provenance": True,
            "unusual_scenarios": True,
        },
        "findings": [],
        "revision_actions": (
            ["Revise the task-local planning contract."]
            if exit_id == "revision_required" else []
        ),
        "scope_proposals": (
            ["scope-proposal:R13"] if exit_id == "clarify_scope" else []
        ),
        "blocking_reasons": (
            ["The required planning authority is unavailable."]
            if exit_id == "blocked" else []
        ),
    }
    payload = {
        "mode": "workflow",
        "authority_refs": ["issue:146"],
        "docs_ssot_plan": {
            "strategy": "ssot_first",
            "durable_paths": ["docs/requirements.md"],
            "summary": "The durable requirement is the implementation source of truth.",
        },
        "semantic_review": semantic_review,
        "typed_exit": exit_id,
        "consumer": consumers[exit_id],
        "reason": f"Production planning eval selected {exit_id}.",
    }
    path = fixture / ".trellis/.runtime/guru-team/evals/planning-owner-input.json"
    runtime.write_json(path, payload)
    return path

def production_record_planning(
    runtime: Any, fixture: Path, task: Path, exit_id: str,
) -> dict[str, Any]:
    input_path = production_planning_input(runtime, fixture, task, exit_id)
    runtime.cmd_record_planning_approval(argparse.Namespace(
        root=str(fixture),
        task=task.relative_to(fixture).as_posix(),
        input=input_path.relative_to(fixture).as_posix(),
        dry_run=False,
    ))
    return runtime.cmd_check_planning_approval(argparse.Namespace(
        root=str(fixture),
        task=task.relative_to(fixture).as_posix(),
        require_exit=None,
    ))

def production_phase2_input(
    runtime: Any, fixture: Path, task: Path, package: Path, exit_id: str,
) -> Path:
    del package
    task_payload = runtime.read_json(task / "task.json")
    base_ref = runtime.diff_base_ref(
        fixture,
        str(task_payload.get("base_branch") or "main"),
    )
    implementation_paths = set(runtime.changed_files(fixture, f"{base_ref}...HEAD"))
    implementation_paths.update(
        path
        for path in runtime.git_status_paths(fixture)
        if not path.startswith(".trellis/.runtime/")
    )
    dimensions = [
        {
            "id": dimension,
            "status": "passed",
            "summary": f"The production eval reviewed {dimension}.",
        }
        for dimension in (
            "requirements", "design", "implementation", "tests", "docs_ssot",
            "cross_layer", "compatibility", "deployment_and_operations",
            "verification_completeness",
        )
    ]
    scope_decisions: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    unverified_items: list[dict[str, Any]] = []
    candidate_classifications = [{
        "candidate_ref": "candidate:phase2:no-defect",
        "decision": "rejected_not_reproduced",
        "witness": {
            "requirement_refs": ["task:prd:R1"],
            "supported_entry_refs": ["entry:guru-check-task:phase2"],
            "existing_caller_refs": ["caller:production-phase2-eval"],
            "honest_action_sequence": [
                "run the installed Phase 2 owner through its supported entry",
            ],
            "defect_observation": (
                "The supported production eval path does not reproduce a task defect."
            ),
            "excluded_assumptions": [],
        },
        "consumer_use": "task_commit_preflight",
    }]
    route = None
    consumer = {
        "passed": {"kind": "skill", "id": "guru-create-task-commit"},
        "implementation_required": {"kind": "workflow", "id": "guru-resume-implementation"},
        "planning_stale": {"kind": "workflow", "id": "guru-task-check-planning-router"},
        "blocked": {"kind": "stop", "id": "task-check-blocked"},
    }[exit_id]
    if exit_id == "implementation_required":
        candidate_classifications = [{
            "candidate_ref": "candidate:phase2:defect",
            "decision": "qualified_current",
            "witness": {
                "requirement_refs": ["task:prd:R1"],
                "supported_entry_refs": ["entry:guru-check-task:phase2"],
                "existing_caller_refs": ["caller:production-phase2-eval"],
                "honest_action_sequence": [
                    "run the supported production Phase 2 implementation check",
                ],
                "defect_observation": (
                    "The current implementation defect is reproduced on the supported eval path."
                ),
                "excluded_assumptions": [],
            },
            "consumer_use": "task_commit_preflight",
        }]
        scope_decisions = [{
            "id": "C1",
            "candidate_ref": "candidate:phase2:defect",
            "disposition": "current_scope",
            "summary": "A current-scope implementation defect remains.",
            "finding_id": "F1",
        }]
        findings = [{
            "id": "F1", "candidate_ref": "candidate:phase2:defect", "severity": "P2",
            "summary": "The current implementation requires a fix.",
            "path": "src/production-eval.txt", "status": "open",
        }]
        next(item for item in dimensions if item["id"] == "implementation")["status"] = "failed"
    elif exit_id == "planning_stale":
        route = "reapprove_plan"
        candidate_classifications = [{
            "candidate_ref": "candidate:phase2:scope",
            "decision": "qualified_approved_expansion",
            "witness": {
                "requirement_refs": ["task:scope-expansion:R13"],
                "supported_entry_refs": ["entry:guru-check-task:phase2"],
                "existing_caller_refs": ["caller:production-phase2-eval"],
                "honest_action_sequence": [
                    "review the approved expansion against the current task plan",
                ],
                "defect_observation": (
                    "The approved expansion is not represented by the current task plan."
                ),
                "excluded_assumptions": [],
            },
            "consumer_use": "task_commit_preflight",
        }]
        scope_decisions = [{
            "id": "scope-proposal:R13",
            "candidate_ref": "candidate:phase2:scope",
            "disposition": "scope_change_required",
            "summary": "The approved scope requires a current authority decision.",
            "finding_id": None,
        }]
    elif exit_id == "blocked":
        unverified_items = [{
            "id": "U1",
            "summary": "The required integration dependency is unavailable.",
            "blocking": True,
        }]
        next(
            item for item in dimensions
            if item["id"] == "verification_completeness"
        )["status"] = "blocked"
    payload = {
        "mode": "workflow",
        "reviewed_paths": sorted(implementation_paths),
        "validation": {
            "commands": [{
                "id": "production-eval",
                "outcome": "passed",
                "summary": "The production owner fixture completed its applicable checks.",
            }],
            "unverified_items": unverified_items,
            "summary": "The production eval captured the applicable validation conclusion.",
        },
        "docs_ssot": {
            "status": "passed",
            "strategy": "ssot_first",
            "durable_paths": ["docs/requirements.md"],
            "summary": "The durable requirement was the implementation input.",
        },
        "candidate_classifications": candidate_classifications,
        "semantic_review": {
            "status": exit_id,
            "summary": f"The production Phase 2 owner selected {exit_id}.",
            "adequacy_dimensions": dimensions,
            "scope_decisions": scope_decisions,
            "findings": findings,
        },
        "typed_exit": exit_id,
        "route": route,
        "reason": f"Production Phase 2 eval selected {exit_id}.",
        "consumer": consumer,
    }
    path = fixture / ".trellis/.runtime/guru-team/evals/phase2-owner-input.json"
    runtime.write_json(path, payload)
    return path

def production_record_phase2(
    runtime: Any, fixture: Path, task: Path, package: Path, exit_id: str,
) -> dict[str, Any]:
    input_path = production_phase2_input(runtime, fixture, task, package, exit_id)
    runtime.cmd_record_phase2_check(argparse.Namespace(
        root=str(fixture),
        task=task.relative_to(fixture).as_posix(),
        input=input_path.relative_to(fixture).as_posix(),
        dry_run=False,
    ))
    return runtime.cmd_check_phase2_check(argparse.Namespace(
        root=str(fixture), task=task.relative_to(fixture).as_posix(),
    ))

def production_task_commit_authoring(
    runtime: Any,
    fixture: Path,
    checked: dict[str, Any],
    review_status: str,
) -> dict[str, Any]:
    coverage_source = (
        "guru-check-task:passed DTO at "
        + str(checked["phase2_capture_commit"])
    )
    classifications = [
        {
            "path": path,
            "category": "task-reviewed",
            "reason": "The isolated production eval includes this path in the checked task scope.",
            "coverage_source": coverage_source,
        }
        for path in runtime.git_status_paths(fixture)
    ]
    return {
        "path_classifications": classifications,
        "message": {
            "type": "feat",
            "scope": "workflow",
            "summary": "增加生产闭环评测",
            "background": "需要以真实 public wrapper 验证 AI-first 任务提交合同。",
            "changes": "提交隔离 fixture 中已由 Phase 2 覆盖的精确路径。",
            "boundaries": "不执行真实发布，也不包含用户授权记录。",
            "validations": "运行共享 public Skill wrapper corpus。",
        },
        "ai_review": {
            "status": review_status,
            "summary": "The exact production eval candidate completed semantic review.",
            "evidence": [
                "Every staged path is part of the isolated fixture and the current Phase 2 result."
            ],
        },
    }

def production_commit_for_review(
    runtime: Any,
    fixture: Path,
    task: Path,
    checked: dict[str, Any],
) -> tuple[str, str]:
    if hasattr(runtime, "commit_review_fixture"):
        return runtime.commit_review_fixture(fixture, task, checked)
    public_input = {
        "profile": "initial_commit",
        "mode": "workflow",
        "task_ref": task.relative_to(fixture).as_posix(),
        "source_exit": "passed",
        "phase2_commit_anchor": checked["phase2_capture_commit"],
    }
    try:
        candidate, plan, _ = runtime.build_task_commit_candidate(
            fixture,
            task,
            public_input,
            production_task_commit_authoring(
                runtime,
                fixture,
                checked,
                "passed",
            ),
        )
        executed = runtime.execute_task_commit_candidate(fixture, candidate, task)
    except runtime.WorkflowError as exc:
        raise ValueError(
            "production Branch Review fixture task commit failed: "
            + json.dumps(exc.payload, ensure_ascii=False, sort_keys=True)
        ) from exc
    return str(executed["commit_sha"]), str(plan["git"]["base_ref"])

def production_review_candidate(
    exit_id: str,
    head: str,
    *,
    resolved: bool = False,
    introduced_head: str | None = None,
) -> list[dict[str, Any]]:
    common = {
        "candidate_ref": "candidate-001",
        "affected_behavior": "The public Branch Review route must preserve the reviewed task behavior.",
        "path": "src/production-eval.txt",
        "evidence_refs": ["git:branch_review_commit", "src/production-eval.txt"],
        "requirement_refs": ["PRD R1"],
        "scope_basis": "The approved production eval requirement owns this behavior.",
        "qualification_reason": "The candidate was classified before any severity was assigned.",
    }
    current_scope_rejections = [
        {
            "candidate_ref": f"candidate-rejected-{scenario}",
            "disposition": "rejected_candidate",
            "scenario_class": scenario,
            "affected_behavior": (
                "The reviewer candidate was evaluated against current scope "
                "and disproved by implementation evidence."
            ),
            "path": "src/production-eval.txt",
            "evidence_refs": ["src/production-eval.txt"],
            "requirement_refs": ["PRD R5"],
            "scope_basis": (
                "The production eval preserves the current approved scenario "
                "without inventing a finding."
            ),
            "qualification_reason": (
                "The current implementation satisfies the bound contract, so "
                "the candidate is rejected without severity or finding fields."
            ),
        }
        for scenario in (
            "normal_required_behavior",
            "explicit_nonstandard_requirement",
            "approved_nonstandard_expansion",
        )
    ]
    if exit_id == "implementation_required" or resolved:
        findings = [{
            **common,
            "disposition": "qualified_finding",
            "scenario_class": "normal_required_behavior",
            "finding_ref": "F-001",
            "severity": "P2",
            "introduced_head": introduced_head or head,
            "fix_head": head if resolved else None,
            "closure_head": head if resolved else None,
            "status": "resolved" if resolved else "open",
            "closure_evidence": (
                [f"commit:{head}", "test:production-eval"]
                if resolved else []
            ),
        }]
        return findings + (current_scope_rejections if resolved else [])
    if exit_id == "scope_confirmation_required":
        return [{
            **common,
            "disposition": "scope_proposal",
            "scenario_class": "unconfirmed_nonstandard_proposal",
            "proposal_ref": "scope-proposal:R2",
            "proposal": "Expand the eval beyond the approved public wrapper boundary.",
            "trigger_evidence": ["The reviewer identified an unapproved optional expansion."],
            "clarification_route": "guru-clarify-requirements",
        }]
    return current_scope_rejections

def production_review_classification(candidate: dict[str, Any]) -> dict[str, Any]:
    disposition = candidate["disposition"]
    scenario = candidate["scenario_class"]
    if disposition == "qualified_finding":
        decision = {
            "normal_required_behavior": "qualified_current",
            "explicit_nonstandard_requirement": "qualified_explicit_nonstandard",
            "approved_nonstandard_expansion": "qualified_approved_expansion",
        }[scenario]
        defect_observation = (
            "The supported Branch Review path reproduced the current required-behavior defect."
        )
    elif disposition == "scope_proposal":
        decision = "rejected_no_authority"
        defect_observation = (
            "Current authority does not authorize the optional expansion proposed by the reviewer."
        )
    else:
        decision = "rejected_not_reproduced"
        defect_observation = (
            "The complete supported Branch Review range does not reproduce the candidate defect."
        )
    return {
        "candidate_ref": candidate["candidate_ref"],
        "decision": decision,
        "witness": {
            "requirement_refs": list(candidate["requirement_refs"]),
            "supported_entry_refs": ["entry:guru-review-branch:branch-review"],
            "existing_caller_refs": ["caller:production-branch-review-eval"],
            "honest_action_sequence": [
                "review the complete current base-to-HEAD range through the supported Branch Review entry",
            ],
            "defect_observation": defect_observation,
            "excluded_assumptions": [],
        },
        "consumer_use": "branch_review_route_checker",
    }

def production_review_semantic_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    common = {
        key: candidate[key]
        for key in (
            "candidate_ref",
            "disposition",
            "affected_behavior",
            "path",
            "evidence_refs",
        )
    }
    if candidate["disposition"] == "qualified_finding":
        keys = (
            "finding_ref",
            "severity",
            "introduced_head",
            "fix_head",
            "closure_head",
            "status",
            "closure_evidence",
        )
    elif candidate["disposition"] == "scope_proposal":
        keys = (
            "proposal_ref",
            "proposal",
            "trigger_evidence",
            "clarification_route",
        )
    else:
        keys = ()
    common.update({key: candidate[key] for key in keys})
    return common

def production_record_review(
    runtime: Any,
    fixture: Path,
    task: Path,
    public_input: dict[str, Any],
    recipe: str,
) -> dict[str, Any]:
    exit_id = recipe.removeprefix("review-")
    resolved = exit_id == "finding-fix-passed"
    if resolved:
        exit_id = "passed"
    elif exit_id == "fresh-final-passed":
        exit_id = "passed"
    head = runtime.current_head(fixture)
    closure_reviewer = "finding-owner-or-replacement" if resolved else None
    reviewer = "fresh-final-reviewer" if resolved else "independent-reviewer"
    if closure_reviewer == reviewer:
        raise ValueError("finding closure and fresh final review require distinct reviewers")
    introduced_head = (
        run_git(fixture, "rev-parse", f"{head}^") if resolved else None
    )
    candidates = production_review_candidate(
        exit_id,
        head,
        resolved=resolved,
        introduced_head=introduced_head,
    )
    candidate_classifications = [
        production_review_classification(item) for item in candidates
    ]
    semantic_candidates = [
        production_review_semantic_candidate(item) for item in candidates
    ]
    semantic = {
        "qualified_findings": [
            item for item in semantic_candidates
            if item["disposition"] == "qualified_finding"
        ],
        "scope_proposals": [
            item for item in semantic_candidates
            if item["disposition"] == "scope_proposal"
        ],
        "observations": [
            item for item in semantic_candidates
            if item["disposition"] == "observation"
        ],
        "followup_candidates": [
            item for item in semantic_candidates
            if item["disposition"] == "followup_candidate"
        ],
        "rejected_candidates": [
            item for item in semantic_candidates
            if item["disposition"] == "rejected_candidate"
        ],
        "ai_review_gate": {
            "status": exit_id,
            "summary": "The production Branch Review semantic Gate selected the actual route.",
        },
    }
    semantic_path = fixture / ".trellis/.runtime/guru-team/evals/review-owner-input.json"
    semantic_path.write_text(json.dumps({
        "candidate_classifications": candidate_classifications,
        "semantic_review": semantic,
        "verification_evidence": {
            "reviewer": reviewer,
            "review_source": runtime.INDEPENDENT_REVIEW_SOURCE,
            "evidence": (
                [
                    f"{closure_reviewer} completed transient finding closure on the fix commit.",
                    "fresh-final-reviewer independently reviewed the complete current range.",
                ]
                if resolved
                else ["Reviewed the complete current range and deployment impact."]
            ),
        },
    }) + "\n", encoding="utf-8")
    public_input.update({
        "task_ref": task.relative_to(fixture).as_posix(),
        "base_ref": runtime.diff_base_ref(fixture, "main"),
        "branch_review_commit": head,
        "review_intent": (
            "fresh_final_review"
            if resolved or recipe == "review-fresh-final-passed"
            else public_input.get("review_intent", "initial_review")
        ),
    })
    runtime_input = fixture / OWNER_INPUT
    runtime_input.write_text(json.dumps(public_input) + "\n", encoding="utf-8")
    runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
    direct_recorder_inputs = {runtime_input, semantic_path}
    for runtime_artifact in runtime_dir.rglob("*"):
        if (
            runtime_artifact.is_file()
            and runtime_artifact not in direct_recorder_inputs
        ):
            runtime_artifact.unlink()
    runtime.cmd_review_branch(argparse.Namespace(
        root=str(fixture),
        json=True,
        task=task.relative_to(fixture).as_posix(),
        base_branch="main",
        evidence=(
            [
                f"{closure_reviewer} 已在 fix commit 上完成瞬态 finding closure。",
                "fresh-final-reviewer 已独立审查完整当前 range 与部署影响。",
            ]
            if resolved
            else ["已审查运行时、CI/CD、Docker、K8s、migration 与 Makefile 部署影响。"]
        ),
        reviewer=reviewer,
        review_source=runtime.INDEPENDENT_REVIEW_SOURCE,
        skill_input=runtime_input.relative_to(fixture).as_posix(),
        semantic_review_file=semantic_path.relative_to(fixture).as_posix(),
        typed_exit=exit_id,
        dry_run=False,
    ))
    return runtime.cmd_check_review_gate(argparse.Namespace(
        root=str(fixture),
        task=task.relative_to(fixture).as_posix(),
        allow_nonpass=True,
        expected_exit=exit_id,
    ))

def production_publication_authoring(
    runtime: Any,
    fixture: Path,
    task: Path,
    public_input: dict[str, Any],
    recipe: str,
) -> Path:
    route = recipe.removeprefix("publication-")
    typed_exit = (
        "return_to_task_work"
        if route in {"return", "metadata-durable-drift-return"}
        else "blocked"
        if route == "blocked"
        else "ready"
    )
    if route == "metadata-fix-ready":
        candidate_ref = "candidate:publication:metadata-revision"
        decision = "qualified_current"
        defect_observation = (
            "The owner-private PR payload required a current task-local metadata "
            "revision before publication could be ready."
        )
    elif typed_exit == "return_to_task_work":
        candidate_ref = "candidate:publication:task-work"
        decision = "qualified_current"
        defect_observation = (
            "The current publication evidence contains a task-work defect that "
            "must return to the task owner."
        )
    elif typed_exit == "blocked":
        candidate_ref = "candidate:publication:external-blocker"
        decision = "qualified_current"
        defect_observation = (
            "The supported publication entry is blocked by a current external "
            "dependency that task work cannot repair."
        )
    else:
        candidate_ref = "candidate:publication:no-defect"
        decision = "rejected_not_reproduced"
        defect_observation = (
            "The complete current publication review reproduces no required-"
            "behavior defect."
        )
    candidate_classifications = [{
        "candidate_ref": candidate_ref,
        "decision": decision,
        "witness": {
            "requirement_refs": ["issue-scope-ledger.json", "pr_payload"],
            "supported_entry_refs": [
                "guru-review-task-publication",
                "git:branch_review_commit",
            ],
            "existing_caller_refs": [
                "guru-review-task-publication",
                "guru-finalize-task",
            ],
            "honest_action_sequence": [
                "Review the current PR payload, Branch Review gate, task scope, "
                "and publication evidence through the supported publication entry."
            ],
            "defect_observation": defect_observation,
            "excluded_assumptions": [
                "No hostile input, artifact tampering, or unsupported workflow bypass."
            ],
        },
        "consumer_use": "publication_route_checker",
    }]
    dimension_status = {
        item: "passed" for item in runtime.TASK_PUBLICATION_DIMENSIONS
    }
    metadata_revision = (
        "\n\n<a id=\"metadata-fix\"></a>\n"
        "已完成 owner-private PR payload 修订并重新审查。"
        if route == "metadata-fix-ready"
        else ""
    )
    pr_payload = {
        "title": "完成：#146 验证 Publication public wrapper 闭环",
        "body": (
            "## 变更摘要\n\n"
            "- 完成真实 public wrapper、recorder 与 checker 闭环评测。\n\n"
            "## 影响范围\n\n"
            "- 影响 Publication Skill、共享 runtime 与隔离评测仓库。\n\n"
            "## 验证结果\n\n"
            "- 已执行 recorder、checker 与 public wrapper 真实命令。\n\n"
            "## Review Gate\n\n"
            "- Branch Review Gate 已通过并绑定当前 HEAD。\n\n"
            "## Issue 关闭范围\n\n"
            "- Closes #146。\n\n"
            "## 安全说明\n\n"
            "- 不写生产环境，不处理 secret，不执行真实 GitHub 发布。\n\n"
            "## Docs SSOT\n\n"
            "- strategy: ssot_first\n"
            "- durable docs: docs/requirements.md 已作为实现输入。\n"
            "- merged delta: task delta 已合并到 durable docs。\n"
            "- task history: eval staging evidence 仅保留在 task history。\n"
            "- follow-up: 当前 PR 无额外限制。"
            + metadata_revision
        ),
    }
    findings: list[dict[str, Any]] = []
    if typed_exit == "return_to_task_work":
        dimension = (
            "docs_ssot_reconciliation"
            if route == "metadata-durable-drift-return"
            else "diff_outcome_consistency"
        )
        dimension_status[dimension] = "finding"
        findings.append({
            "finding_ref": (
                "PUB-DOCS-001"
                if route == "metadata-durable-drift-return"
                else "PUB-WORK-001"
            ),
            "candidate_ref": candidate_ref,
            "dimension": dimension,
            "summary": "The current publication review requires a complete task-work rerun.",
            "scope_basis": "The approved production eval owns this current-scope behavior.",
            "evidence_refs": ["docs/requirements.md"],
            "affected_artifacts": ["docs/requirements.md"],
            "route_class": "task_work",
            "status": "open",
            "closure_evidence": [],
        })
    elif typed_exit == "blocked":
        dimension_status["artifact_binding_freshness"] = "blocked"
        findings.append({
            "finding_ref": "PUB-BLOCK-001",
            "candidate_ref": candidate_ref,
            "dimension": "artifact_binding_freshness",
            "summary": "An external publication dependency is unavailable.",
            "scope_basis": "The dependency cannot be repaired by current task work.",
            "evidence_refs": ["external:publication-dependency"],
            "affected_artifacts": ["external:publication-dependency"],
            "route_class": "external_blocker",
            "status": "open",
            "closure_evidence": [],
        })
    elif route == "metadata-fix-ready":
        findings.append({
            "finding_ref": "PUB-META-001",
            "candidate_ref": candidate_ref,
            "dimension": "pr_body_quality",
            "summary": "The owner-private PR payload was revised and rereviewed.",
            "scope_basis": "The contract permits an internal payload metadata revision.",
            "evidence_refs": ["pr_payload.body"],
            "affected_artifacts": ["pr_payload"],
            "route_class": "metadata_revision",
            "status": "closed",
            "closure_evidence": ["pr_payload.body#metadata-fix"],
        })
    dimensions = [{
        "id": dimension,
        "status": dimension_status[dimension],
        "summary": f"The semantic owner reviewed {dimension} against current evidence.",
        "evidence_refs": [
            "pr_payload",
            "issue-scope-ledger.json",
            "git:branch_review_commit",
        ],
    } for dimension in runtime.TASK_PUBLICATION_DIMENSIONS]
    authoring: dict[str, Any] = {
        "profile": public_input["profile"],
        "mode": public_input["mode"],
        "review_intent": public_input["review_intent"],
        "pr_payload": pr_payload,
        "candidate_classifications": candidate_classifications,
        "dimensions": dimensions,
        "findings": findings,
        "conclusions": {
            "issue_scope": {
                "status": (
                    "passed"
                    if typed_exit == "ready"
                    else "finding"
                    if typed_exit == "return_to_task_work"
                    else "blocked"
                ),
                "summary": "The owner reviewed current issue closure scope.",
                "evidence_refs": ["issue-scope-ledger.json"],
            },
            "docs_ssot": {
                "status": (
                    "finding"
                    if route == "metadata-durable-drift-return"
                    else "passed"
                ),
                "summary": "The owner reviewed the approved Docs SSOT outcome.",
                "evidence_refs": [
                    "git:branch_review_commit",
                    "docs/requirements.md",
                ],
            },
            "safety_deployment": {
                "status": "blocked" if typed_exit == "blocked" else "passed",
                "summary": "The owner reviewed safety and deployment impact.",
                "evidence_refs": ["pr_payload"],
            },
        },
        "route": {"typed_exit": typed_exit},
    }
    if public_input["profile"] == "publication_review_stale":
        authoring["stale_reason"] = public_input["stale_reason"]
    if typed_exit == "blocked":
        authoring["route"].update({
            "reason_code": "external_publication_dependency",
            "remediation": "Restore the external dependency and re-enter publication review.",
        })
    path = fixture / ".trellis/.runtime/guru-team/evals/publication-owner-input.json"
    runtime.write_json(path, authoring)
    return path

def extension_verification_execution(
    runtime: Any,
    fixture: Path,
    public_input: dict[str, Any],
    status: str,
    selected: list[str],
    package: Path,
    *,
    resolved_head: str,
) -> dict[str, Any]:
    commands = [{
        "id": "verify_throwaway_installation",
        "checkout_owner": "extension_source_checkout",
        "argv": ["git", "ls-remote", "origin", public_input["ref"]],
        "exit_code": 0 if status == "passed" else 2,
        "stdout_sha256": runtime.digest_text(""),
        "stderr_sha256": runtime.digest_text(
            "" if status == "passed" else "synthetic unavailable"
        ),
        "stdout_size_bytes": 0,
        "stderr_size_bytes": 0 if status == "passed" else 21,
    }]
    if status == "passed":
        example = json.loads(
            (package / "examples/execution-facts.json").read_text(encoding="utf-8")
        )
        asset_expectations = copy.deepcopy(example["asset_expectations"])
        asset_digests = copy.deepcopy(example["asset_digests"])
        asset_inventory = copy.deepcopy(example["asset_inventory"])
    else:
        asset_expectations = []
        asset_digests = []
        asset_inventory = runtime.extension_verification_asset_inventory_summary([], [])
    return {
        "schema_version": runtime.EXTENSION_VERIFICATION_SCHEMA_VERSION,
        "target_repository": {
            "repo_ref": public_input["repo_ref"],
            "remote": public_input["remote"],
            "ref": public_input["ref"],
            "branch_review_commit": None,
            "publication_head": None,
            "resolved_head": resolved_head,
            "checkout_head": resolved_head if status == "passed" else None,
            "reviewed_content_sha256": None,
            "remote_reviewed_content_sha256": None,
            "content_identity_matches": status == "passed",
        },
        "extension_source": {
            "selection": "standalone_fallback",
            "manifest_provenance": "not_available",
            "repo": public_input["repo_ref"],
            "locator": runtime.extension_verification_canonical_github_locator(
                public_input["repo_ref"]
            ),
            "requested_ref": public_input["ref"],
            "resolved_ref": public_input["ref"],
            "tree_state": "clean",
            "is_mutable_ref": False,
            "direct_oid": resolved_head,
            "commit": resolved_head,
            "checkout_head": resolved_head if status == "passed" else None,
            "ref_matches_commit": status == "passed",
            "checkout_head_matches": status == "passed",
        },
        "status": status,
        "commands": commands,
        "failure": None,
        "capabilities": runtime.extension_verification_capability_facts(
            selected,
            "passed" if status == "passed" else "blocked",
            commands,
            asset_digests,
        ),
        "asset_expectations": asset_expectations,
        "asset_digests": asset_digests,
        "asset_inventory": asset_inventory,
        "ownership": {
            "checkout_owner": "extension_source_checkout",
            "current_contract": True,
            "schema_version": "3.0",
            "inventory_id": "guru-team-upstream-ownership",
            "guru_owned_rule_count": 11,
            "managed_claim_count": 9,
        },
        "sidecars": {"checkout_owner": "extension_source_checkout", "paths": []},
    }

def extension_verification_review(
    typed_exit: str,
    selected: list[str],
) -> dict[str, Any]:
    blocked = typed_exit == "blocked"
    review: dict[str, Any] = {
        "applicability": {
            "status": "required",
            "reason": "The explicit source-repository invocation requires installation verification.",
            "evidence_paths": ["trellis/skills/guru-team/registry.json"],
        },
        "verification_profile": {
            "selected_capabilities": selected,
            "selection_reason": "The closed source profile covers every extension capability.",
            "coverage": [f"source extension -> {capability}" for capability in selected],
        },
        "semantic_review": {
            "adequacy": [{
                "id": "profile_coverage",
                "status": "blocked" if blocked else "passed",
                "evidence_refs": ["owner-staging:source-extension-verification"],
            }],
            "findings": ([{
                "finding_ref": "extension-eval-blocker-001",
                "evidence": "The synthetic source remote is unavailable.",
                "route_class": "external_blocker",
                "status": "open",
                "closure_evidence": "",
            }] if blocked else []),
            "conclusion": typed_exit,
        },
        "typed_exit": typed_exit,
        "redaction": {
            "status": "passed",
            "scanned_surfaces": ["artifact", "wrapper_stdout", "eval_trace", "retained_logs"],
        },
    }
    if blocked:
        review.update({
            "reason_code": "remote_unavailable",
            "remediation": "Restore source remote access and rerun standalone verification.",
        })
    return review

def stage_extension_verification_owner_execution(
    runtime: Any,
    fixture: Path,
    fixture_runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    typed_exit = {
        "extension-source-verified": "verified",
        "extension-source-unavailable": "blocked",
    }.get(recipe)
    if typed_exit is None:
        raise ValueError(f"unsupported source extension recipe: {recipe}")
    source_repo = request_package.parents[4]
    canonical_source = source_repo / "trellis"
    if canonical_source.is_symlink() or not canonical_source.is_dir():
        raise ValueError("canonical source tree is unavailable for extension staging")
    shutil.copytree(
        canonical_source,
        fixture / "trellis",
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    package = fixture / ".trellis/guru-team/skills/packages/guru-verify-extension-installation"
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("extension owner staging package does not match the evaluated contract")

    remotes = run_git(fixture, "remote").splitlines()
    remote_command = "set-url" if "origin" in remotes else "add"
    run_git(
        fixture,
        "remote",
        remote_command,
        "origin",
        "https://github.com/castbox/guru-trellis.git",
    )
    run_git(fixture, "add", ".")
    if subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=fixture, check=False
    ).returncode != 0:
        run_git(fixture, "commit", "-q", "-m", "stage source verification owner")
    head = run_git(fixture, "rev-parse", "HEAD")
    public_input = json.loads(public_input_path.read_text(encoding="utf-8"))
    public_input.update({
        "profile": "source_repository_verification",
        "mode": "standalone",
        "repo_ref": "castbox/guru-trellis",
        "remote": "origin",
        "ref": head,
        "caller_intent": "verify-extension-installation",
    })
    runtime_input = fixture / OWNER_INPUT
    runtime.write_json(runtime_input, public_input)
    runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
    execution_path = runtime_dir / "extension-execution-input.json"
    review_path = runtime_dir / "extension-review-input.json"
    capabilities = list(runtime.EXTENSION_VERIFICATION_CAPABILITIES)
    runtime.write_json(
        execution_path,
        extension_verification_execution(
            runtime,
            fixture,
            public_input,
            "passed" if typed_exit == "verified" else "blocked",
            capabilities,
            request_package,
            resolved_head=head,
        ),
    )
    runtime.write_json(review_path, extension_verification_review(typed_exit, capabilities))
    owner = runtime.cmd_record_extension_verification(argparse.Namespace(
        root=str(fixture),
        input=runtime_input.relative_to(fixture).as_posix(),
        execution_input=execution_path.relative_to(fixture).as_posix(),
        review_input=review_path.relative_to(fixture).as_posix(),
    ))
    runtime.write_json(fixture / OWNER_RESULT, owner)
    return package, fixture_runtime_target, {"GURU_TEAM_EVAL_STAGING": "1"}

def stage_task_pr_merge_owner_execution(
    runtime: Any,
    request: dict[str, Any],
    fixture: Path,
    fixture_runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    if not recipe.startswith("merge-"):
        raise ValueError("merge owner staging recipe is invalid")
    package = fixture / ".trellis/guru-team/skills/packages/guru-merge-task-pr"
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("merge owner staging package does not match the evaluated contract")

    public_input = json.loads(public_input_path.read_text(encoding="utf-8"))
    runtime_input = fixture / OWNER_INPUT
    runtime_input.parent.mkdir(parents=True, exist_ok=True)
    runtime.write_json(runtime_input, public_input)
    blocked_routes = {
        "merge-standalone-draft-blocked": (
            "pr_ready",
            "pull_request_draft",
            "Mark the PR Ready and rerun the live preview.",
        ),
        "merge-workflow-head-drift-blocked": (
            "repository_and_head",
            "expected_head_changed",
            "Rerun publication and merge review for the current PR head.",
        ),
        "merge-workflow-branch-drift-blocked": (
            "repository_and_head",
            "expected_branch_changed",
            "Restore the reviewed base/head branches and rerun the live preview.",
        ),
        "merge-workflow-close-scope-blocked": (
            "close_scope",
            "close_scope_mismatch",
            "Repair and rereview the PR close-keyword scope before merge.",
        ),
        "merge-workflow-added-close-scope-blocked": (
            "close_scope",
            "close_scope_mismatch",
            "Repair and rereview the PR close-keyword scope before merge.",
        ),
    }
    blocked = blocked_routes.get(recipe)
    dimensions = []
    for identifier in runtime.TASK_PR_MERGE_DIMENSIONS:
        dimensions.append({
            "id": identifier,
            "status": "blocked" if blocked and identifier == blocked[0] else "passed",
            "summary": (
                f"The controlled live facts block {identifier}."
                if blocked and identifier == blocked[0]
                else f"The controlled live facts pass {identifier}."
            ),
        })
    route = (
        {
            "typed_exit": "merge_blocked",
            "reason_code": blocked[1],
            "remediation": blocked[2],
        }
        if blocked
        else {"typed_exit": "merged", "merge_method": "merge"}
    )
    review_path = fixture / ".trellis/.runtime/guru-team/evals/merge-review.json"
    runtime.write_json(
        review_path,
        {"semantic_review": {"dimensions": dimensions}, "route": route},
    )
    fake_bin = write_fake_merge_gh(Path(request["workdir"]).resolve().parent, recipe)
    environment = {"PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}"}
    previous_path = os.environ.get("PATH")
    os.environ["PATH"] = environment["PATH"]
    owner_context: dict[str, Any] = {}
    try:
        recorded = runtime.cmd_record_task_pr_merge(argparse.Namespace(
            root=str(fixture),
            input=runtime_input.relative_to(fixture).as_posix(),
            review_input=str(review_path),
        ))
        gate_path = fixture / str(recorded["gate"])
        if not blocked:
            runtime.cmd_execute_task_pr_merge(argparse.Namespace(
                root=str(fixture),
                input=runtime_input.relative_to(fixture).as_posix(),
                gate=gate_path.relative_to(fixture).as_posix(),
            ))
        bind_merge_gate_argument(request, fixture, gate_path)
    finally:
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path
    return package, fixture_runtime_target, environment

def stage_finalization_owner_execution(
    runtime: Any,
    request: dict[str, Any],
    fixture: Path,
    fixture_runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    routes = {
        "finalization-publication-stale": (
            "publication_review_stale",
            "publication_review_stale",
        ),
        "finalization-same-plan-resume": (
            "resume_finalization",
            "draft_bound",
        ),
        "finalization-cross-month-reprepare": (
            "reprepare_required",
            "reprepare_required",
        ),
        "finalization-ready-for-merge-recovery": (
            "ready_for_merge",
            "ready",
        ),
        "finalization-publication-ready-ready-for-merge": (
            "ready_for_merge",
            "ready",
        ),
        "finalization-same-plan-ready-for-merge": (
            "ready_for_merge",
            "ready",
        ),
        "finalization-blocked": (
            "blocked",
            "prepared",
        ),
    }
    selected = routes.get(recipe)
    if selected is None:
        raise ValueError(
            f"unsupported finalization owner staging recipe: {recipe}"
        )
    exit_id, transaction_state = selected
    package = (
        fixture
        / ".trellis/guru-team/skills/packages/guru-finalize-task"
    )
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError(
            "finalization owner staging package does not match the evaluated contract"
        )

    task = fixture / ".trellis/tasks/current"
    task.mkdir(parents=True, exist_ok=True)
    runtime.write_json(task / "task.json", {
        "id": "current",
        "name": "current",
        "title": "Finalization eval",
        "status": "in_progress",
        "branch": "main",
        "base_branch": "main",
    })
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-q", "-m", "stage finalization owner")
    head = run_git(fixture, "rev-parse", "HEAD")
    public_input = json.loads(public_input_path.read_text(encoding="utf-8"))
    public_input["task_ref"] = ".trellis/tasks/current"
    plan_digest = "b" * 64
    plan_ref = f"closeout-plan:{plan_digest}"
    if "plan_ref" in public_input:
        public_input["plan_ref"] = plan_ref
    if "branch_review_commit" in public_input:
        public_input["branch_review_commit"] = head
    if "publication_head" in public_input:
        public_input["publication_head"] = head
    runtime_input = fixture / OWNER_INPUT
    runtime.write_json(runtime_input, public_input)

    runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    context_path = runtime_dir / "finalization-context.json"
    archive_locator = ".trellis/tasks/archive/2026-07/current"
    if transaction_state == "ready":
        (fixture / archive_locator).mkdir(parents=True, exist_ok=True)
    context_payload = {
        "schema_version": "2.0",
        "task_ref": public_input["task_ref"],
        "plan_ref": plan_ref,
        "plan_digest": plan_digest,
        "branch_review_commit": head,
        "publication_head": head,
        "archive_locator": archive_locator,
        "repo_ref": "example/guru-extension",
        "remote": "origin",
        "head_branch": "main",
        "pr_title": public_input.get("pr_title") or "Finalize the staged eval task",
        "pr_body": public_input.get("pr_body") or "## Eval\n\n- Finalize the staged task.\n",
        "publication_status": (
            "stale"
            if exit_id == "publication_review_stale"
            else "current"
        ),
        "publication_stale_reason": (
            "publication_review_stale"
            if exit_id == "publication_review_stale"
            else None
        ),
        "transaction_state": transaction_state,
    }
    runtime.write_json(context_path, context_payload)
    previous_eval = os.environ.get("GURU_TEAM_EVAL_STAGING")
    os.environ["GURU_TEAM_EVAL_STAGING"] = "1"
    try:
        context = runtime.finalization_eval_preview_context(
            fixture,
            public_input,
        )
        if context is None:
            raise ValueError("finalization eval context was not accepted")
        if exit_id == "reprepare_required":
            # Reprepare consumes the prior content-pushed transaction and
            # creates a replacement transaction without external mutation.
            prior = runtime.finalization_transaction_from_plan(
                context["plan"],
                next_transition="push_content",
                pre_push_remote_head=head,
            )
            runtime.finalization_write_transaction(
                fixture,
                fixture / public_input["task_ref"],
                prior,
            )
        outputs = {
            "publication_review_stale": {
                "exit_id": "publication_review_stale",
                "task_ref": public_input["task_ref"],
                "branch_review_commit": head,
                "stale_reason": "publication_review_stale",
            },
            "resume_finalization": {
                "exit_id": "resume_finalization",
                "task_ref": public_input["task_ref"],
                "plan_ref": plan_ref,
            },
            "reprepare_required": {
                "exit_id": "reprepare_required",
                "task_ref": public_input["task_ref"],
                "reason_code": "archive_month_changed",
                "branch_review_commit": head,
                "publication_head": head,
            },
            "ready_for_merge": {
                "materialization": "executor",
            },
            "blocked": {
                "exit_id": "blocked",
                "reason_code": "invalid_private_state",
                "remediation": "Repair the staged objective state and rerun finalization.",
            },
        }
        reviewed = {
            "schema_version": "3.0",
            "skill_id": "guru-finalize-task",
            "review": {
                "status": (
                    "blocked"
                    if exit_id == "blocked"
                    else "reroute"
                    if exit_id in {
                        "publication_review_stale",
                        "resume_finalization",
                        "reprepare_required",
                    }
                    else "passed"
                ),
                "summary": "The finalization eval owner reviewed the exact staged objective facts.",
            },
            "route": {
                "typed_exit": exit_id,
                "consumer": runtime.FINALIZATION_CONSUMERS[exit_id],
                "output": outputs[exit_id],
            },
        }
        review_path = runtime_dir / "semantic-review.json"
        runtime.write_json(review_path, reviewed)
        runtime.finalization_semantic_review_input(
            fixture,
            review_path.relative_to(fixture).as_posix(),
        )
        bind_review_input_argument(request, fixture, review_path)
    finally:
        if previous_eval is None:
            os.environ.pop("GURU_TEAM_EVAL_STAGING", None)
        else:
            os.environ["GURU_TEAM_EVAL_STAGING"] = previous_eval
    fake_bin = write_fake_gh(
        Path(request["workdir"]).resolve().parent,
        recipe,
    )
    return package, fixture_runtime_target, {
        "GURU_TEAM_EVAL_STAGING": "1",
        "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
    }

def stage_base_reconciliation_owner_execution(
    request: dict[str, Any],
    fixture: Path,
    fixture_runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    exits = {
        "base-reconciled": "reconciled",
        "base-review-continuity": "review_continuity_required",
        "base-implementation-required": "implementation_required",
        "base-planning-stale": "planning_stale",
        "base-scope-confirmation": "scope_confirmation_required",
        "base-blocked": "blocked",
    }
    exit_id = exits.get(recipe)
    if exit_id is None:
        raise ValueError(f"unsupported base reconciliation owner staging recipe: {recipe}")
    package = fixture / ".trellis/guru-team/skills/packages/guru-reconcile-task-base"
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("base reconciliation owner staging package does not match the evaluated contract")

    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-q", "-m", "stage base reconciliation eval")
    old_base = run_git(fixture, "rev-parse", "HEAD")
    (fixture / "base-evolution.txt").write_text("new base\n", encoding="utf-8")
    run_git(fixture, "add", "base-evolution.txt")
    run_git(fixture, "commit", "-q", "-m", "advance eval base")
    new_base = run_git(fixture, "rev-parse", "HEAD")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", new_base)
    run_git(fixture, "checkout", "-q", "-b", "eval/base-reconciliation", old_base)
    (fixture / "task-evolution.txt").write_text("task content\n", encoding="utf-8")
    run_git(fixture, "add", "task-evolution.txt")
    run_git(fixture, "commit", "-q", "-m", "stage eval task content")
    task_head = run_git(fixture, "rev-parse", "HEAD")

    public_input = json.loads(public_input_path.read_text(encoding="utf-8"))
    public_input.update({
        "task_ref": ".trellis/tasks/current",
        "task_head": task_head,
        "selected_base_ref": "origin/main",
        "old_base_head": old_base,
        "new_base_head": new_base,
    })
    if "branch_review_commit" in public_input:
        public_input["branch_review_commit"] = task_head
    task_ref = public_input["task_ref"]
    task_id = "current"
    workspace_slug = "current"
    task_dir = fixture / task_ref
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "task.json").write_text(json.dumps({
        "id": task_id,
        "name": task_id,
        "title": "Base reconciliation eval",
        "status": "planning" if public_input["profile"] == "post_plan" else "in_progress",
        "branch": "eval/base-reconciliation",
        "base_branch": "main",
    }) + "\n", encoding="utf-8")
    mappings_root = fixture / ".trellis/.runtime/guru-team"
    task_mappings = mappings_root / "tasks"
    workspace_mappings = mappings_root / "workspaces"
    task_mappings.mkdir(parents=True, exist_ok=True)
    workspace_mappings.mkdir(parents=True, exist_ok=True)
    (task_mappings / f"{task_id}.json").write_text(json.dumps({
        "schema_version": "1.0",
        "task_slug": task_id,
        "workspace_slug": workspace_slug,
        "workspace_path": str(fixture.resolve()),
        "task_artifact_dir": task_ref,
    }) + "\n", encoding="utf-8")
    (workspace_mappings / f"{workspace_slug}.json").write_text(json.dumps({
        "schema_version": "1.0",
        "workspace_slug": workspace_slug,
        "workspace_path": str(fixture.resolve()),
        "branch_name": "eval/base-reconciliation",
    }) + "\n", encoding="utf-8")
    runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    runtime_input = fixture / OWNER_INPUT
    runtime_input.write_text(json.dumps(public_input) + "\n", encoding="utf-8")

    route_payloads = {
        "reconciled": {},
        "review_continuity_required": {
            "candidate_tree_sha256": "c" * 64,
            "relevant_paths": ["base-evolution.txt"],
        },
        "implementation_required": {"finding_refs": ["base-finding-001"]},
        "planning_stale": {"reason_refs": ["authority-assumption-changed"]},
        "scope_confirmation_required": {"proposal_refs": ["scope-proposal-001"]},
        "blocked": {},
    }
    impacts = {
        "reconciled": ("unchanged", "unchanged", "compatible"),
        "review_continuity_required": ("unchanged", "unchanged", "continuity_review_required"),
        "implementation_required": ("unchanged", "implementation_required", "validation_failed"),
        "planning_stale": ("changed", "planning_stale", "insufficient_evidence"),
        "scope_confirmation_required": ("changed", "planning_stale", "insufficient_evidence"),
        "blocked": ("insufficient_evidence", "insufficient_evidence", "insufficient_evidence"),
    }
    authority, task_content, integration = impacts[exit_id]
    gate = {
        "authority_impact": authority,
        "task_content_impact": task_content,
        "integration_impact": integration,
        "reviewed_scope": ["live authority", "approved planning", "cumulative base delta", "candidate evidence"],
        "key_delta_refs": [f"{old_base}...{new_base}"],
        "validation_evidence": ["isolated candidate evidence reviewed for the exact pair"],
        "unverified_boundaries": (["applicable evidence does not support one unique route"] if exit_id == "blocked" else []),
        "summary": f"The semantic owner selected {exit_id} for the exact evolved-base pair.",
        "typed_exit": exit_id,
        "route_payload": route_payloads[exit_id],
    }
    gate_path = runtime_dir / "base-semantic-review.json"
    gate_path.write_text(json.dumps(gate) + "\n", encoding="utf-8")
    recorded = subprocess.run(
        [
            str(package / "scripts/record-base-reconciliation.sh"),
            "--root", str(fixture), "--skill-input", OWNER_INPUT,
            "--semantic-review-file", gate_path.relative_to(fixture).as_posix(),
            "--typed-exit", exit_id,
        ],
        cwd=fixture, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    if recorded.returncode != 0:
        raise ValueError(f"base reconciliation recorder staging failed: {recorded.stderr.strip()}")
    owner_result = json.loads(recorded.stdout)
    checkpoint_namespace = (
        f"{task_id}-{hashlib.sha256(task_ref.encode()).hexdigest()[:12]}"
    )
    checkpoint = (
        fixture / ".trellis/.runtime/guru-team/owner-checkpoints"
        / checkpoint_namespace / "guru-reconcile-task-base/base-reconciliation.json"
    )
    checked = subprocess.run(
        [
            str(package / "scripts/check-base-reconciliation.sh"),
            "--root", str(fixture), "--input", checkpoint.relative_to(fixture).as_posix(),
            "--expected-exit", exit_id,
        ],
        cwd=fixture, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    if checked.returncode != 0:
        raise ValueError(f"base reconciliation checker staging failed: {checked.stderr.strip()}")
    invocation_path = fixture / OWNER_INVOCATION
    invocation_path.write_text(
        json.dumps({"public_input": public_input, "owner_result": owner_result}) + "\n",
        encoding="utf-8",
    )
    return package, fixture_runtime_target, {"GURU_TEAM_EVAL_STAGING": "1"}

def stage_production_owner_execution(
    request: dict[str, Any],
    fixture: Path,
    runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    skill_id = str(request["skill_id"])
    fixture_runtime_target = fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
    if fixture_runtime_target.is_symlink() or not os.access(fixture_runtime_target, os.X_OK):
        raise ValueError("fixture public invocation runtime is unavailable")
    runtime = (
        None
        if skill_id in {"guru-maintain-architecture-baseline", "guru-restore-archived-task"}
        else load_package_owner_runtime(fixture_runtime_target, skill_id)
    )
    if runtime is not None and not hasattr(runtime, "read_json"):
        runtime.read_json = lambda path: json.loads(Path(path).read_text(encoding="utf-8"))
    if runtime is not None and not hasattr(runtime, "diff_base_ref"):
        runtime.diff_base_ref = lambda root, branch: branch
    if runtime is not None and not hasattr(runtime, "changed_files"):
        runtime.changed_files = lambda root, revision: subprocess.run(
            ["git", "diff", "--name-only", revision, "--"], cwd=root,
            text=True, stdout=subprocess.PIPE, check=False,
        ).stdout.splitlines()
    if runtime is not None and not hasattr(runtime, "git_status_paths"):
        runtime.git_status_paths = lambda root: [
            line[3:] for line in subprocess.run(
                ["git", "status", "--short"], cwd=root,
                text=True, stdout=subprocess.PIPE, check=False,
            ).stdout.splitlines() if len(line) >= 4
        ]
    if skill_id == "guru-reconcile-task-base":
        return stage_base_reconciliation_owner_execution(
            request,
            fixture,
            fixture_runtime_target,
            request_package,
            recipe,
            public_input_path,
        )
    if skill_id == "guru-finalize-task":
        return stage_finalization_owner_execution(
            runtime,
            request,
            fixture,
            fixture_runtime_target,
            request_package,
            recipe,
            public_input_path,
        )
    if skill_id == "guru-verify-extension-installation":
        return stage_extension_verification_owner_execution(
            runtime,
            fixture,
            fixture_runtime_target,
            request_package,
            recipe,
            public_input_path,
        )
    if skill_id == "guru-merge-task-pr":
        return stage_task_pr_merge_owner_execution(
            runtime,
            request,
            fixture,
            fixture_runtime_target,
            request_package,
            recipe,
            public_input_path,
        )
    if skill_id == "guru-restore-archived-task":
        return stage_restore_archived_task_owner_execution(
            request,
            fixture,
            fixture_runtime_target,
            request_package,
            recipe,
            public_input_path,
        )
    compose_production_fixture_runtime(fixture_runtime_target, runtime)
    compose_production_owner_command_runtime(fixture_runtime_target, runtime)
    task, _ = production_task_fixture(runtime, fixture)
    production_environment: dict[str, str] = {}
    package = fixture / ".trellis/guru-team/skills/packages" / skill_id
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("owner staging package does not match the evaluated package contract")
    public_input = json.loads(public_input_path.read_text(encoding="utf-8"))
    expected_prefix = {
        "guru-approve-task-plan": "planning-",
        "guru-check-task": "check-",
        "guru-create-task-commit": "commit-",
        "guru-finalize-task": "finalization-",
        "guru-review-branch": "review-",
        "guru-review-task-publication": "publication-",
        "guru-verify-extension-installation": "extension-",
    }[skill_id]
    if not recipe.startswith(expected_prefix):
        raise ValueError("production owner staging recipe does not match the evaluated package")
    if skill_id == "guru-approve-task-plan":
        planning_exit = {
            "planning-approved": "approved",
            "planning-revision-required": "revision_required",
            "planning-clarify-scope": "clarify_scope",
            "planning-blocked": "blocked",
        }.get(recipe)
        if planning_exit is None:
            raise ValueError("unsupported planning owner staging recipe")
        checked_owner = production_record_planning(
            runtime, fixture, task, planning_exit,
        )
        owner_result_path = Path(checked_owner["artifact_path"])
    else:
        production_record_planning(runtime, fixture, task, "approved")
        task_payload = json.loads((task / "task.json").read_text(encoding="utf-8"))
        task_payload["status"] = "in_progress"
        (task / "task.json").write_text(
            json.dumps(task_payload) + "\n", encoding="utf-8"
        )
        run_git(fixture, "add", task.relative_to(fixture).as_posix())
        run_git(fixture, "commit", "-q", "-m", "activate production eval task")
        (fixture / "src/production-eval.txt").write_text(
            f"{recipe}\n", encoding="utf-8",
        )
        phase2_package = fixture / ".trellis/guru-team/skills/packages/guru-check-task"
        phase2_exit = {
            "check-passed": "passed",
            "check-implementation-required": "implementation_required",
            "check-planning-stale": "planning_stale",
            "check-blocked": "blocked",
        }.get(recipe)
        checked = production_record_phase2(
            runtime,
            fixture,
            task,
            phase2_package,
            (
                "passed"
                if skill_id in {
                    "guru-create-task-commit",
                    "guru-review-branch",
                    "guru-review-task-publication",
                }
                else phase2_exit
            ),
        )
        owner_result_path = Path(checked["artifact_path"])
        if skill_id == "guru-create-task-commit":
            public_input["phase2_commit_anchor"] = checked[
                "phase2_capture_commit"
            ]
            review_status = {
                "commit-revision-required": "revision-required",
                "commit-blocked-recovery": "blocked",
            }.get(recipe, "passed")
            if recipe == "commit-revision-required":
                runtime.build_task_commit_candidate(
                    fixture,
                    task,
                    {
                        "profile": "initial_commit",
                        "mode": public_input["mode"],
                        "task_ref": task.relative_to(fixture).as_posix(),
                        "source_exit": "passed",
                        "phase2_commit_anchor": checked[
                            "phase2_capture_commit"
                        ],
                    },
                    production_task_commit_authoring(
                        runtime,
                        fixture,
                        checked,
                        "revision-required",
                    ),
                )
            owner_result_path, _, _ = runtime.build_task_commit_candidate(
                fixture,
                task,
                public_input,
                production_task_commit_authoring(
                    runtime,
                    fixture,
                    checked,
                    review_status,
                ),
            )
        elif skill_id == "guru-review-branch":
            production_commit_for_review(
                runtime, fixture, task, checked
            )
            production_record_review(
                runtime,
                fixture,
                task,
                public_input,
                recipe,
            )
            runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
            for runtime_artifact in runtime_dir.rglob("*"):
                if (
                    runtime_artifact.is_file()
                    and runtime_artifact != fixture / OWNER_INPUT
                ):
                    runtime_artifact.unlink()
        elif skill_id == "guru-review-task-publication":
            production_commit_for_review(
                runtime, fixture, task, checked
            )
            branch_input = {
                "profile": "branch_review",
                "mode": public_input["mode"],
                "task_ref": task.relative_to(fixture).as_posix(),
                "base_ref": "origin/main",
                "branch_review_commit": "0" * 40,
                "review_intent": "initial_review",
            }
            branch_check = production_record_review(
                runtime,
                fixture,
                task,
                branch_input,
                "review-passed",
            )
            branch_review_commit = branch_check["review_commit"]
            public_input["task_ref"] = task.relative_to(fixture).as_posix()
            public_input["branch_review_commit"] = branch_review_commit
            if public_input["profile"] != "publication_review":
                initial_input = {
                    "profile": "publication_review",
                    "mode": public_input["mode"],
                    "task_ref": task.relative_to(fixture).as_posix(),
                    "branch_review_commit": branch_review_commit,
                    "review_intent": "initial_review",
                }
                initial_authoring_path = production_publication_authoring(
                    runtime,
                    fixture,
                    task,
                    initial_input,
                    "publication-ready",
                )
                runtime.cmd_record_task_publication_review(argparse.Namespace(
                    root=str(fixture),
                    task=task.relative_to(fixture).as_posix(),
                    input=initial_authoring_path.relative_to(fixture).as_posix(),
                    branch_review_commit=initial_input["branch_review_commit"],
                    dry_run=False,
                ))
            if recipe == "publication-metadata-durable-drift-return":
                with (fixture / "docs/requirements.md").open(
                    "a", encoding="utf-8"
                ) as handle:
                    handle.write(
                        "\nUncommitted durable drift requires a task-work rerun.\n"
                    )
            authoring_path = production_publication_authoring(
                runtime,
                fixture,
                task,
                public_input,
                recipe,
            )
            publication_owner = runtime.cmd_record_task_publication_review(argparse.Namespace(
                root=str(fixture),
                task=task.relative_to(fixture).as_posix(),
                input=authoring_path.relative_to(fixture).as_posix(),
                branch_review_commit=branch_review_commit,
                dry_run=False,
            ))
            owner_result_path = Path(publication_owner["artifact_path"])
            runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
            for runtime_artifact in runtime_dir.rglob("*"):
                if (
                    runtime_artifact.is_file()
                    and runtime_artifact != fixture / OWNER_INPUT
                ):
                    runtime_artifact.unlink()
    runtime_input = fixture / OWNER_INPUT
    runtime.write_json(runtime_input, public_input)
    if skill_id != "guru-review-branch":
        bind_owner_result_argument(request, fixture, owner_result_path)
    return package, fixture_runtime_target, production_environment

def stage_restore_archived_task_owner_execution(
    request: dict[str, Any],
    fixture: Path,
    fixture_runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    """Build a real archive/worktree owner fixture and invoke the public restore script."""
    source_package = fixture / ".trellis/guru-team/skills/packages/guru-restore-archived-task"
    if (
        hashlib.sha256((source_package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((source_package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("restore owner staging package does not match the evaluated contract")
    if not recipe.startswith("restore-"):
        raise ValueError("restore owner staging recipe is invalid")

    case = recipe.removeprefix("restore-")
    task_id = "09-03-348-merge-blocked-phase2-reentry"
    branch = "codex/348-merge-blocked-phase2-reentry"
    repo_ref = "castbox/guru-trellis"
    pr_number = 348
    archive_locator = f".trellis/tasks/archive/2026-09/{task_id}"
    active_locator = f".trellis/tasks/{task_id}"
    worktree = fixture / "owner-worktrees" / task_id
    worktree.parent.mkdir(parents=True, exist_ok=True)
    run_git(fixture, "branch", "-M", "main")
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-q", "-m", "stage restore owner base")
    run_git(fixture, "worktree", "add", "-q", "-b", branch, str(worktree), "HEAD")
    package = worktree / ".trellis/guru-team/skills/packages/guru-restore-archived-task"

    archive = worktree / archive_locator
    active = worktree / active_locator
    archive.mkdir(parents=True, exist_ok=True)
    task_payload = {
        "id": task_id, "name": task_id, "title": "Restore eval",
        "status": "completed", "completedAt": "2026-09-03T00:00:00Z",
        "branch": branch, "base_branch": "main",
    }
    (archive / "task.json").write_text(json.dumps(task_payload) + "\n", encoding="utf-8")
    finish_summary = {
        "task": {"slug": task_id, "artifact_dir": active_locator, "archive_dir": archive_locator, "status": "completed"},
        "git": {"branch": branch, "base_branch": "main"},
        "github": {"pr_url": f"https://github.com/{repo_ref}/pull/{pr_number}", "source_issues": [pr_number], "close_issues": [], "related_issues": [], "followup_issues": []},
    }
    (archive / "finish-summary.json").write_text(json.dumps(finish_summary) + "\n", encoding="utf-8")
    run_git(worktree, "add", archive_locator)
    run_git(worktree, "commit", "-q", "-m", "stage archived task")
    expected_head = run_git(worktree, "rev-parse", "HEAD")
    archive_commit = expected_head

    workspace_slug = "348-restore"
    mapping_path = worktree / ".trellis/.runtime/guru-team/tasks" / f"{task_id}.json"
    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    mapping_path.write_text(json.dumps({
        "schema_version": "1.0", "task_slug": task_id,
        "workspace_slug": workspace_slug, "workspace_path": str(worktree),
        "task_artifact_dir": archive_locator,
    }) + "\n", encoding="utf-8")
    workspace_mapping = worktree / ".trellis/.runtime/guru-team/workspaces" / f"{workspace_slug}.json"
    workspace_mapping.parent.mkdir(parents=True, exist_ok=True)
    workspace_mapping.write_text(json.dumps({
        "schema_version": "1.0", "workspace_slug": workspace_slug,
        "workspace_path": str(worktree), "source_checkout": str(fixture),
        "branch_name": branch,
    }) + "\n", encoding="utf-8")

    public = json.loads(public_input_path.read_text(encoding="utf-8"))
    public.update({
        "exit_id": "phase2_reentry_required", "repo_ref": repo_ref,
        "pr_number": pr_number, "pr_url": f"https://github.com/{repo_ref}/pull/{pr_number}",
        "expected_head_sha": expected_head, "expected_base_branch": "main",
        "expected_head_branch": branch, "issue_number": pr_number, "task_id": task_id,
        "archive_locator": archive_locator, "active_locator": active_locator,
        "archive_commit": archive_commit, "finding_refs": ["merge-finding:348:phase2-reentry"],
        "resume_target": "phase-2",
    })
    semantic = {
        "schema_version": "1.0", "profile": "restore_archived_task", "mode": "workflow",
        "review_intent": "task_work_reentry", "classification": "task_work",
        "requires_task_content_change": True, "finding_refs": public["finding_refs"],
    }
    facts = json.loads((package / "examples/live-facts.json").read_text(encoding="utf-8"))
    facts["pr"].update({"state": "OPEN", "number": pr_number, "url": public["pr_url"], "head_sha": expected_head, "base_branch": "main", "head_branch": branch})
    facts["issue"].update({"number": pr_number, "state": "OPEN", "close_intent": "unchanged"})
    facts["remote_branch"].update({"name": branch, "head_sha": expected_head})
    facts["local_branch"].update({"name": branch, "head_sha": expected_head})
    facts["archive"].update({"locator": archive_locator, "commit": archive_commit, "task_json_sha256": hashlib.sha256((archive / "task.json").read_bytes()).hexdigest(), "finish_summary_sha256": hashlib.sha256((archive / "finish-summary.json").read_bytes()).hexdigest()})
    facts["task"].update({"id": task_id, "status": "completed", "completed_at": task_payload["completedAt"], "branch": branch, "base_branch": "main", "repo_ref": repo_ref, "issue_number": pr_number, "pr_number": pr_number, "expected_head_sha": expected_head})
    facts["runtime_mapping"].update({"state": "archived", "task_id": task_id, "archive_locator": archive_locator, "active_locator": active_locator, "repo_ref": repo_ref, "branch_name": branch, "worktree_path": str(worktree)})
    facts["worktree"].update({"path": str(worktree), "exists": True, "clean": True, "branch": branch, "occupied_by": None})
    facts["active_task"] = {"present": False, "task_id": None, "locator": None}
    if case == "idempotent":
        shutil.move(str(archive), str(active))
        task_payload["status"] = "in_progress"
        task_payload.pop("completedAt", None)
        (active / "task.json").write_text(json.dumps(task_payload) + "\n", encoding="utf-8")
        (active / "finish-summary.json").unlink()
        mapping_path.write_text(json.dumps({**json.loads(mapping_path.read_text()), "task_artifact_dir": active_locator}) + "\n", encoding="utf-8")
        current = worktree / ".trellis/.runtime/current-task"
        current.parent.mkdir(parents=True, exist_ok=True)
        current.write_text(active_locator + "\n", encoding="utf-8")
        facts["runtime_mapping"]["state"] = "active"
        facts["task"]["status"] = "in_progress"
        facts["active_task"] = {"present": True, "task_id": task_id, "locator": active_locator}
    blockers = facts["blockers"]
    if case == "external-blocker": blockers["provider"] = True
    elif case == "head-drift": facts["pr"]["head_sha"] = "2" * 40
    elif case == "scope-drift": blockers["scope_drift"] = True
    elif case == "dirty-worktree": facts["worktree"]["clean"] = False
    elif case == "active-task-conflict": facts["active_task"] = {"present": True, "task_id": "other-task", "locator": ".trellis/tasks/other-task"}
    elif case == "merged-pr": facts["pr"]["state"] = "MERGED"
    elif case not in {"success", "idempotent"}:
        raise ValueError(f"unsupported restore owner staging case: {case}")
    runtime_dir = worktree / ".trellis/.runtime/guru-team/evals"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    input_path = runtime_dir / "restore-input.json"
    semantic_path = runtime_dir / "restore-semantic.json"
    facts_path = runtime_dir / "restore-facts.json"
    input_path.write_text(json.dumps(public) + "\n", encoding="utf-8")
    semantic_path.write_text(json.dumps(semantic) + "\n", encoding="utf-8")
    facts_path.write_text(json.dumps(facts) + "\n", encoding="utf-8")
    for relative in request.get("files", []):
        path = Path(request["workdir"]) / str(relative)
        try: payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError): continue
        invocation = payload.get("public_invocation") if isinstance(payload, dict) else None
        if isinstance(invocation, dict):
            invocation["arguments"] = ["--root", str(worktree), "--input", str(input_path), "--semantic-result", str(semantic_path), "--facts", str(facts_path)]
            path.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
    return package, fixture_runtime_target, {"GURU_TEAM_EVAL_STAGING": "1"}
