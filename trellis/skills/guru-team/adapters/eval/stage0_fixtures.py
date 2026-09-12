from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import copy
import hashlib
import io
import json
import os
import subprocess
import sys
import time

from adapters.eval.eval_constants import (
    OWNER_INVOCATION,
    WORKSPACE_CALL_LOCAL_STATE,
)

from adapters.eval.fixture_io import (
    run_git,
)

from adapters.eval.owner_runtime import (
    load_package_owner_runtime,
    load_package_runtime_module,
)


def stage0_command(
    fixture: Path, skill_id: str, command: str, payload: dict[str, Any],
    *arguments: str,
) -> dict[str, Any]:
    package = fixture / ".trellis/guru-team/skills/packages" / skill_id
    process = subprocess.run(
        ["bash", str(package / "scripts" / f"{command}.sh"), *arguments],
        cwd=fixture, input=json.dumps(payload), text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    if process.returncode:
        raise ValueError(
            f"Stage 0 producer {skill_id}/{command} failed: "
            f"{process.stdout.strip()} {process.stderr.strip()}"
        )
    result = json.loads(process.stdout)
    if not isinstance(result, dict):
        raise ValueError(f"Stage 0 producer {skill_id}/{command} returned no object")
    return result


def readiness_context(
    fixture: Path, source: dict[str, Any], mode: str, continuation: str,
) -> dict[str, Any]:
    sync = stage0_command(fixture, "guru-sync-base", "invoke", {
        "schema_version": "1.0", "public_input": {
            "source_exit": "start", "mode": mode, "repo_root": str(fixture),
            "route": "repo_change", "base_branch": "main",
        },
    }, "--invocation", "-")
    if sync.get("exit_id") != "synced":
        raise ValueError("Readiness fixture requires the production synced transition")
    skill = "guru-discover-change-context"
    package = fixture / ".trellis/guru-team/skills/packages" / skill
    runtime = load_package_runtime_module(
        fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh", skill, "common"
    )
    owner = build_context_owner(runtime, fixture, package, "context-ready")
    owner["mode"] = mode
    body_hash = hashlib.sha256(source["body"].encode()).hexdigest()
    issue = source["kind"] == "issue"
    locator = (f"https://github.com/{source['repo']}/issues/{source['number']}"
               if issue else source["draft_id"])
    live = {
        "kind": "issue" if issue else "draft", "identity": locator,
        "state": "open" if issue else "draft",
        "updated_at": source.get("updated_at") or "2026-01-01T00:00:00Z",
        "body_sha256": body_hash,
    }
    owner["live_change"] = {
        **live, "facts_sha256": runtime.digest(live), "issue_binding": None,
    }
    owner["result_identity"] = runtime.identity(owner)
    envelope = {
        "schema_version": "1.0", "transition": sync["transition"],
        "public_input": {
            "profile": "pre_task", "mode": mode,
            "change_input": owner["change_input"],
            "continuation_id": continuation, "source_exit": "synced",
        },
        "owner_result": owner, "owner_context": {},
    }
    envelope["owner_result"] = stage0_command(
        fixture, skill, "record-context-discovery", envelope, "--invocation", "-"
    )
    stage0_command(fixture, skill, "check-context-discovery", envelope, "--invocation", "-")
    result = stage0_command(fixture, skill, "invoke", envelope, "--invocation", "-")
    if result.get("exit_id") != "context_ready":
        raise ValueError("Readiness fixture requires the production context_ready transition")
    return result


def stage0_eval_hash(label: str, *values: Any) -> str:
    payload = json.dumps(
        [label, *values], sort_keys=True, separators=(",", ":"), default=str
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def stage0_contract_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def stage0_eval_base(fixture: Path) -> dict[str, Any]:
    head = run_git(fixture, "rev-parse", "HEAD")
    return {
        "source": "explicit",
        "selected_base": "main",
        "remote": "origin",
        "ordered_candidates": ["main"],
        "decision_head": head,
        "local_base_head": head,
        "remote_base_head": head,
        "post_sync_resolution_sha256": stage0_eval_hash(
            "base-current", "explicit", "main", "origin", head
        ),
    }

def stage0_eval_transition(
    skill_id: str,
    fixture: Path,
    public_input: dict[str, Any],
    owner_result: dict[str, Any],
) -> dict[str, Any] | None:
    if (
        skill_id == "guru-review-contract-wording"
        and public_input.get("profile") in {"planning_artifacts", "explicit_paths"}
    ):
        return None
    mode = str(public_input.get("mode") or owner_result.get("mode") or "workflow")
    continuation = str(public_input.get("continuation_id") or "stage0-current")
    target = str(public_input.get("target_locator") or "")
    base = stage0_eval_base(fixture)
    common = {
        "schema_version": "1.0",
        "mode": mode,
        "repo_locator": (
            str(fixture.resolve())
            if skill_id == "guru-discover-change-context"
            else "example/guru-extension"
        ),
        "base": base,
    }
    context_digest = stage0_eval_hash("context", target, continuation, base)
    clarity_digest = stage0_eval_hash("clarity", target, continuation, owner_result)
    content_digest = stage0_eval_hash("target-content", target)
    stage_by_skill = {
        "guru-discover-change-context": "base_current",
        "guru-clarify-requirements": "context_current",
        "guru-review-contract-wording": "clarity_current",
    }
    stage = stage_by_skill.get(skill_id)
    if stage is None:
        raise ValueError(f"call-local transition is not declared for {skill_id}")
    transition = {
        **common,
        "stage": stage,
    }
    if stage == "base_current":
        identity = transition["base"]["post_sync_resolution_sha256"]
        transition["transition_id"] = f"{stage}:{identity[:24]}"
        return transition
    if stage == "clarity_current":
        scope = owner_result.get("scope") if isinstance(owner_result.get("scope"), dict) else {}
        scope_identity = str(scope.get("identity") or "")
        if scope_identity:
            target = scope_identity.removeprefix("change_request:")
        content_digest = str(scope.get("scope_sha256") or content_digest)
        for item in scope.get("items", []):
            if isinstance(item, dict) and item.get("field") == "body":
                content_digest = str(item.get("content_sha256") or content_digest)
                break
    transition.update({
        "target_locator": target,
        "continuation_id": continuation,
    })
    if stage == "context_current":
        transition["context_result_sha256"] = context_digest
        target_value = owner_result.get("review_target")
        target_value = target_value if isinstance(target_value, dict) else {}
        transition["authority_content_sha256"] = str(
            target_value.get("body_sha256") or content_digest
        )
    elif stage == "clarity_current":
        transition.update({
            "context_result_sha256": context_digest,
            "clarity_result_sha256": clarity_digest,
            "target_content_sha256": content_digest,
            "clarity": {
                "facts_sha256": clarity_digest,
                "target_sha256": stage0_eval_hash("clarity-target", target),
                "disposition_sha256": stage0_eval_hash("clarity-disposition", target),
                "content_sha256": stage0_eval_hash("clarity-content", target),
                "scope_sha256": stage0_eval_hash("clarity-scope", target),
            },
            "target_disposition": {
                "disposition_sha256": stage0_eval_hash("clarity-disposition", target),
                "duplicate_facts_sha256": stage0_eval_hash("clarity-duplicates", target),
            },
        })
    identity_field = {
        "context_current": "context_result_sha256",
        "clarity_current": "clarity_result_sha256",
    }[stage]
    transition["transition_id"] = f"{stage}:{transition[identity_field][:24]}"
    return transition

def bind_stage0_call_local_invocation(
    request: dict[str, Any],
    fixture: Path,
    public_input: dict[str, Any],
    owner_result: dict[str, Any],
    owner_context: dict[str, Any],
    readiness_invocation: dict[str, Any] | None = None,
) -> None:
    skill_id = str(request["skill_id"])
    public_input = copy.deepcopy(public_input)
    if skill_id == "guru-review-contract-wording" and public_input.get("mode") == "workflow":
        scope = owner_result.get("scope") if isinstance(owner_result.get("scope"), dict) else {}
        scope_identity = str(scope.get("identity") or "")
        if scope_identity.startswith("change_request:"):
            public_input["target_locator"] = scope_identity.removeprefix(
                "change_request:"
            )
    elif skill_id == "guru-review-change-request" and public_input.get("mode") == "workflow":
        target = owner_result.get("target") if isinstance(owner_result.get("target"), dict) else {}
        if isinstance(target.get("url"), str) and target.get("url"):
            public_input["target_locator"] = target["url"]
        elif isinstance(target.get("draft_id"), str) and target.get("draft_id"):
            public_input["target_locator"] = f"draft:{target['draft_id']}"
    envelope: dict[str, Any] = {
        "schema_version": "1.0",
        "public_input": public_input,
        "owner_result": owner_result,
    }
    if skill_id == "guru-review-contract-wording":
        receipt = {
            "schema_version": "1.0",
            "skill_id": skill_id,
            "operation": "check-contract-wording-review",
            "result_sha256": owner_result["facts_sha256"],
            "prerequisite_sha256": stage0_contract_digest({"profile": owner_result["profile"], "mode": owner_result["mode"]}),
            "snapshot_sha256": stage0_contract_digest({"scope": owner_result["scope"], "scan": owner_result["scan"]}),
        }
        receipt["receipt_sha256"] = stage0_contract_digest(receipt)
        envelope["validation_receipt"] = receipt
    if skill_id == "guru-create-task-workspace":
        workspace_state = WORKSPACE_CALL_LOCAL_STATE.get(str(fixture.resolve()))
        if workspace_state is None:
            raise ValueError("workspace call-local owner state is unavailable")
        envelope["owner_plan"] = copy.deepcopy(workspace_state[0])
    else:
        envelope["owner_context"] = copy.deepcopy(owner_context)
    if skill_id == "guru-review-change-request":
        if readiness_invocation is None:
            raise ValueError("Readiness requires the checked production invocation")
        envelope = copy.deepcopy(readiness_invocation)
        transition = envelope["transition"]
    elif skill_id == "guru-create-task-workspace":
        transition = copy.deepcopy(workspace_state[1])
    else:
        transition = stage0_eval_transition(skill_id, fixture, public_input, owner_result)
    if transition is not None:
        envelope["transition"] = transition
    invocation_path = fixture / OWNER_INVOCATION
    invocation_path.write_text(json.dumps(envelope) + "\n", encoding="utf-8")

    workdir = Path(request["workdir"]).resolve()
    matched = 0
    for relative in request.get("files", []):
        path = workdir / str(relative)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        invocation = payload.get("public_invocation") if isinstance(payload, dict) else None
        if not isinstance(invocation, dict):
            continue
        if invocation.get("arguments") != ["--invocation", "-"]:
            raise ValueError("Phase 0 eval must invoke exactly --invocation -")
        matched += 1
    if matched != 1:
        raise ValueError("Phase 0 eval must declare one call-local invocation")

def bind_sync_call_local_invocation(
    request: dict[str, Any], fixture: Path
) -> None:
    route_by_case = {
        "synced-route": ("main", "repo_change"),
        "skipped-route": (None, "original_request"),
        "blocked-route": ("missing-stage0-eval-base", "repo_change"),
    }
    selected = route_by_case.get(str(request.get("case_id") or ""))
    if selected is None:
        raise ValueError("unsupported sync-base call-local eval case")
    base_branch, route = selected
    public_input: dict[str, Any] = {
        "source_exit": "start",
        "mode": "workflow",
        "repo_root": ".",
        "route": route,
    }
    if base_branch is not None:
        public_input["base_branch"] = base_branch
    invocation_path = fixture / OWNER_INVOCATION
    invocation_path.parent.mkdir(parents=True, exist_ok=True)
    invocation_path.write_text(json.dumps({
        "schema_version": "1.0",
        "public_input": public_input,
    }) + "\n", encoding="utf-8")

    workdir = Path(request["workdir"]).resolve()
    matched = 0
    for relative in request.get("files", []):
        path = workdir / str(relative)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        invocation = payload.get("public_invocation") if isinstance(payload, dict) else None
        if not isinstance(invocation, dict):
            continue
        if invocation.get("arguments") != ["--invocation", "-"]:
            raise ValueError("sync-base eval must invoke exactly --invocation -")
        matched += 1
    if matched != 1:
        raise ValueError("sync-base eval must declare one call-local invocation")

def clarity_target(
    runtime: Any,
    payload: dict[str, Any],
    *,
    state: str = "open",
    body: str = "Issue 145 owner staging body",
) -> dict[str, Any]:
    target = {
        "kind": "issue", "repo": "example/guru-extension", "issue_number": 145,
        "url": "https://github.com/example/guru-extension/issues/145", "state": state,
        "updated_at": "2026-01-01T00:00:00Z",
        "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
    }
    target["facts_sha256"] = runtime.context_digest(target)
    payload["invocation_context"] = {
        "kind": "initial_issue", "caller": "stage0 eval owner staging",
        "task_locator": None, "resume_target": "guru-review-contract-wording",
    }
    payload["review_target"] = target
    return payload

def clarity_disposition(
    runtime: Any,
    payload: dict[str, Any],
    disposition: str,
    *,
    candidates: list[dict[str, Any]] | None = None,
    selected_issue: dict[str, Any] | None = None,
    role: str = "primary",
) -> dict[str, Any]:
    payload["target_disposition"] = {
        "disposition": disposition,
        "duplicate_query": "repo:example/guru-extension is:issue is:open stage0 eval",
        "duplicate_checked_at": "2026-01-01T00:00:00Z",
        "duplicate_candidates": candidates or [], "duplicate_facts_sha256": "0" * 64,
        "selected_issue": selected_issue, "original_target_role": role,
        "decision_summary": f"The reviewed owner staging selected {disposition}.",
        "disposition_digest": "0" * 64,
    }
    return runtime.derive_requirements_clarification_result(payload)

def clarity_finalize(runtime: Any, payload: dict[str, Any]) -> dict[str, Any]:
    return runtime.derive_requirements_clarification_result(payload)

def build_clarity_owner(runtime: Any, package_root: Path, recipe: str) -> dict[str, Any]:
    payload = json.loads(
        (package_root / "examples/requirements-clarification.json").read_text(encoding="utf-8")
    )
    if recipe == "clarity-clear":
        return runtime.derive_requirements_clarification_result(payload)

    payload["mode"] = "workflow"
    if recipe == "clarity-needs-context":
        payload["typed_exit"] = "needs_context"
        payload["consumer"] = {"kind": "skill", "id": "guru-discover-change-context"}
        payload["context_evidence"] = {
            "status": "missing", "evidence_refs": ["repository.current_owner"],
            "missing_reason": "The current repository owner evidence is unavailable.",
        }
        payload["reason"] = "A named repository fact is required before clarification can continue."
        return runtime.derive_requirements_clarification_result(payload)
    if recipe == "clarity-refresh-context":
        payload["mode"] = "standalone"
        payload["typed_exit"] = "refresh_context"
        payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
        payload["context_evidence"]["status"] = "stale"
        payload["context_evidence"]["missing_reason"] = "The reviewed source binding changed."
        payload["reason"] = "The context snapshot must be refreshed from current authority."
        return runtime.derive_requirements_clarification_result(payload)
    if recipe == "clarity-blocked":
        payload = clarity_target(runtime, payload)
        payload = clarity_disposition(runtime, payload, "keep_current_open_issue")
        payload["typed_exit"] = "blocked"
        payload["consumer"] = {"kind": "stop", "id": "requirements-clarification-blocked"}
        payload["ai_review_gate"]["status"] = "blocked"
        payload["error"] = {
            "codes": ["load_bearing_decision_unresolved"],
            "summary": "A load-bearing requirement decision remains unresolved.",
        }
        payload["reason"] = "The unresolved load-bearing decision blocks the clarification loop."
        return runtime.derive_requirements_clarification_result(payload)
    if recipe == "clarity-retarget":
        payload = clarity_target(runtime, payload)
        projection = {
            "repo": "example/guru-extension", "number": 146, "identity": "#146",
            "url": "https://github.com/example/guru-extension/issues/146", "state": "open",
            "updated_at": "2026-01-01T00:00:00Z",
        }
        candidate = {
            **projection, "facts_sha256": runtime.context_digest(projection),
            "decision": "selected", "reason": "The current duplicate is the selected target.",
        }
        selected = {
            "repo": candidate["repo"], "issue_number": candidate["number"],
            "url": candidate["url"], "state": candidate["state"],
            "updated_at": candidate["updated_at"], "facts_sha256": candidate["facts_sha256"],
        }
        payload["typed_exit"] = "retarget_context"
        payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
        payload["source_actions"] = [{
            "action_id": "select_existing", "kind": "select_existing_issue",
            "target": {"repo": candidate["repo"], "issue_number": candidate["number"]},
            "payload": selected, "preimage_sha256": payload["review_target"]["facts_sha256"],
            "payload_sha256": None, "action_digest": "0" * 64, "status": "validated",
            "mutation_evidence": None,
        }]
        payload = clarity_disposition(
            runtime, payload, "retarget_existing_issue", candidates=[candidate],
            selected_issue=selected, role="related",
        )
        return clarity_finalize(runtime, payload)
    if recipe == "clarity-new-task":
        payload = clarity_target(runtime, payload, state="closed")
        payload["typed_exit"] = "new_task"
        payload["consumer"] = {"kind": "workflow", "id": "guru-full-task-intake-chain"}
        payload["source_actions"] = [{
            "action_id": "new_issue", "kind": "new_issue_draft",
            "target": {"repo": "example/guru-extension"},
            "payload": {"title": "Independent Stage 0 follow-up", "body": "Reviewed independent delivery scope."},
            "preimage_sha256": None, "payload_sha256": None, "action_digest": "0" * 64,
            "status": "draft_ready", "mutation_evidence": None,
        }]
        payload = clarity_disposition(
            runtime, payload, "create_followup_draft", role="related",
        )
        return clarity_finalize(runtime, payload)
    raise ValueError(f"unsupported clarification owner staging recipe: {recipe}")

def build_workflow_mode_owner(
    public_input: dict[str, Any], recipe: str,
) -> dict[str, Any]:
    exits = {
        "workflow-mode-explicit-task-free": "task_free",
        "workflow-mode-automatic-high-confidence": "task_free",
        "workflow-mode-insufficient-confirmed": "task_free",
        "workflow-mode-insufficient-refused": "standard_intake",
        "workflow-mode-complex-request": "standard_intake",
        "workflow-mode-simple-issue": "task_free",
        "workflow-mode-insufficient-issue-confirmed": "task_free",
        "workflow-mode-complex-issue": "standard_intake",
        "workflow-mode-same-file-count-low-risk": "task_free",
        "workflow-mode-same-file-count-high-risk": "standard_intake",
        "workflow-mode-non-default-checkout": "task_free",
        "workflow-mode-active-task-same-scope": "task_free",
        "workflow-mode-active-task-scope-expansion": "task_free",
        "workflow-mode-unrelated-worktree": "task_free",
        "workflow-mode-dirty-overlap": "task_free",
        "workflow-mode-position-evidence-insufficient": "task_free",
        "workflow-mode-unrelated-dirty": "task_free",
        "workflow-mode-repeated-turn": "task_free",
        "workflow-mode-automatic-risk-expansion": "standard_intake",
        "workflow-mode-explicit-risk-expansion": "task_free",
        "workflow-mode-blocked": "blocked",
    }
    typed_exit = exits.get(recipe)
    if typed_exit is None:
        raise ValueError(f"unsupported workflow mode owner staging recipe: {recipe}")
    owner = {
        "schema_version": "1.0",
        "typed_exit": typed_exit,
        "mode": public_input["mode"],
        "continuation_id": public_input["continuation_id"],
    }
    if typed_exit != "blocked":
        owner["selection"] = typed_exit
    return owner

def build_task_free_change_owner(
    public_input: dict[str, Any], recipe: str,
) -> dict[str, Any]:
    route = {
        "task-free-completed": ("completed", "suitable"),
        "task-free-non-default-completed": ("completed", "suitable"),
        "task-free-resume-active-task": ("resume_active_task", "resume_active_task"),
        "task-free-scope-change": ("scope_change", "scope_change"),
        "task-free-location-unrelated-worktree": ("location_required", "location_required"),
        "task-free-location-dirty-overlap": ("location_required", "location_required"),
        "task-free-location-insufficient": ("location_required", "location_required"),
        "task-free-automatic-risk-expansion": ("reselect_mode", "suitable"),
        "task-free-explicit-risk-expansion": ("explicit_choice_required", "suitable"),
        "task-free-blocked": ("blocked", "blocked"),
    }.get(recipe)
    if route is None:
        raise ValueError(f"unsupported task-free owner staging recipe: {recipe}")
    typed_exit, prewrite_status = route
    owner: dict[str, Any] = {
        "schema_version": "1.0",
        "typed_exit": typed_exit,
        "mode": public_input["mode"],
        "continuation_id": public_input["continuation_id"],
        "selection_origin": public_input["selection_origin"],
        "request_summary": public_input["request_summary"],
        "target_paths": public_input["target_paths"],
        "pre_write_review": {
            "status": prewrite_status,
            "summary": "The semantic owner reviewed current local checkout, active-task, dirty, and target-overlap facts before writing.",
        },
        "ai_review_gate": {
            "status": "blocked" if typed_exit == "blocked" else "passed",
            "summary": "The AI reviewed checkout suitability and the selected execution route from current facts.",
        },
    }
    if typed_exit == "completed":
        owner["completion_evidence"] = {
            "edited_paths": list(public_input["target_paths"]),
            "targeted_checks": [{
                "command": "git diff --check -- docs/guide.md",
                "summary": "The bounded documentation diff has no whitespace errors.",
                "status": "passed",
            }],
            "post_write_review": {
                "status": "passed",
                "summary": "The actual edit remained inside the selected paths and did not expand scope or risk.",
            },
            "unverified_boundaries": [
                "No full repository test suite was run for this documentation-only change."
            ],
        }
        owner["ai_review_gate"]["summary"] = "The AI reviewed pre-write suitability, the actual edit, targeted checks, and post-write scope/risk evolution."
    if typed_exit in {"reselect_mode", "explicit_choice_required"}:
        owner["evolution_evidence"] = {
            "write_state": "partial_edit",
            "edited_paths": [public_input["target_paths"][0]],
            "expansion": {
                "kind": "scope_and_risk",
                "summary": "The first bounded edit revealed public installation and contract impact outside task-free risk.",
            },
            "stop_after_detection": True,
            "remaining_writes_not_performed": [{
                "target_path": path,
                "summary": "The planned edit for this bounded target was not performed after expansion detection.",
            } for path in public_input["target_paths"][1:]],
            "targeted_checks": [{
                "command": "git diff --check -- docs/guide.md",
                "summary": "The partial bounded diff has no whitespace errors.",
                "status": "passed",
            }],
        }
        owner["ai_review_gate"]["summary"] = "The AI reviewed the actual partial edit, detected expanded scope and risk, and stopped all remaining writes."
    if typed_exit in {"resume_active_task", "scope_change"}:
        owner["task_ref"] = ".trellis/tasks/current"
    return owner

def build_context_owner(
    runtime: Any,
    fixture: Path,
    package_root: Path,
    recipe: str,
) -> dict[str, Any]:
    payload = json.loads(
        (package_root / "examples/change-context-owner-result-3.0.json").read_text(encoding="utf-8")
    )
    old_head = run_git(fixture, "rev-parse", "HEAD")
    payload["repository"] = {
        "repo": "example/guru-extension", "selected_base": "main", "decision_branch": "main",
    }
    payload["base_observation"] = {
        "repo": "example/guru-extension", "repo_locator": str(fixture.resolve()),
        "selected_base": "main", "remote": "origin", "authority_branch": "main",
        "decision_head": old_head, "local_head": old_head, "remote_head": old_head,
        "clean": True, "current": True,
    }
    payload["change_input"] = {
        "issue_refs": [], "pr_refs": [], "branches": [],
        "paths": ["docs/requirements.md"], "commands": [],
        "config_keys": [], "schema_fields": [], "symbols": [],
        "terms": ["change context"], "queries": [],
    }
    payload["live_change"]["issue_binding"] = None
    body_sha256 = hashlib.sha256(b"Stage 0 context owner staging draft").hexdigest()
    live_unsigned = {
        "kind": "draft", "identity": f"draft:{body_sha256}", "state": "draft",
        "updated_at": "2026-01-01T00:00:00Z", "body_sha256": body_sha256,
    }
    payload["live_change"] = {
        **live_unsigned, "facts_sha256": runtime.digest(live_unsigned), "issue_binding": None,
    }
    evidence_paths = {
        "docs": "docs/requirements.md",
        "code_contracts": "trellis/runtime.py",
        "tests": "trellis/test_runtime.py",
    }
    for group, path in evidence_paths.items():
        rows = payload["current_state"][group]
        rows[0]["path"] = path
        rows[0]["blob_or_content_sha256"] = run_git(fixture, "rev-parse", f"HEAD:{path}")
    query = runtime.canonical_query(payload["change_input"])
    payload["canonical_query"] = query
    payload["history_preview"] = runtime.preview(fixture, payload["change_input"], 20)
    payload["history_review"] = {
        "selected_candidates": [], "excluded_candidates": [], "deep_reads": [],
    }
    payload["error"] = None
    payload["typed_exit"] = "context_ready"
    payload["ai_review_gate"]["status"] = "passed"
    payload["result_identity"] = runtime.identity(payload)
    if recipe == "context-ready":
        return payload
    if recipe == "context-blocked":
        payload["typed_exit"] = "blocked"
        payload["ai_review_gate"]["status"] = "blocked"
        payload["error"] = {
            "codes": ["semantic_review_blocked"],
            "summary": "A named load-bearing repository source could not be reviewed.",
        }
        payload["result_identity"] = runtime.identity(payload)
        return payload
    if recipe == "context-refresh-base":
        run_git(fixture, "commit", "--allow-empty", "-q", "-m", "advance context fixture")
        payload["typed_exit"] = "refresh_base"
        payload["result_identity"] = runtime.identity(payload)
        return payload
    raise ValueError(f"unsupported context owner staging recipe: {recipe}")

def workspace_base_fixture(runtime: Any, head: str) -> dict[str, Any]:
    """Retain the existing #250 workspace prerequisite until that owner migrates."""
    identity = {"schema_version":"1.0","skill_id":"guru-sync-base","status":"resolved","source":"explicit","selected_base":"main","remote":"origin","candidates":["main"],"decision_checkout":{"branch":"main","head":head,"clean":True}}
    resolution_sha256=runtime.digest(identity)
    value={"schema_version":"1.0","skill_id":"guru-sync-base","status":"synced","resolution":{"source":"explicit","selected_base":"main","remote":"origin","candidates":["main"],"resolution_sha256":resolution_sha256},"post_sync_resolution":identity,"post_sync_resolution_sha256":resolution_sha256,"decision_checkout":{"branch":"main","head_before":head,"head_after":head,"clean_before":True,"clean_after":True},"git":{"local_ref":"refs/heads/main","remote_ref":"refs/remotes/origin/main","local_head_before":head,"local_head_after":head,"remote_head_after":head,"fetch_performed":True,"fast_forwarded":False},"fresh":True}
    value["facts_sha256"]=runtime.digest(value);return value

def wording_review(
    runtime: Any,
    profile: str,
    mode: str,
    scope: dict[str, Any],
    scan: dict[str, Any],
    typed_exit: str,
) -> dict[str, Any]:
    passed = typed_exit != "blocked"
    revisions: list[dict[str, Any]] = []
    if typed_exit == "content_changed":
        item = scope["items"][0]
        revisions = [{
            "revision_id": "stage0-eval-revision", "locator": item["path"],
            "before_sha256": "0" * 64, "after_sha256": item["content_sha256"],
            "reason": "The completed planning wording revision is present in the current rescan.",
            "rescan_sha256": scan["scan_sha256"],
        }]
    gate: dict[str, Any] = {
        "status": "passed" if passed else "blocked", "reviewer": "stage0-eval-reviewer",
        "summary": "The complete fixed wording scope and current rescan were semantically reviewed.",
        "reviewed_scan_sha256": scan["scan_sha256"],
        "checked_dimensions": {
            key: passed for key in runtime.CONTRACT_WORDING_REVIEW_DIMENSIONS
        },
    }
    if profile == "planning_artifacts":
        gate["planning_checked_dimensions"] = {
            key: passed for key in runtime.CONTRACT_WORDING_PLANNING_REVIEW_DIMENSIONS
        }
    authored = {
        "generated_at": "2026-01-01T00:00:00Z",
        "semantic_review": {
            "revisions": revisions,
            "classifications": [{
                "hit_id": hit["hit_id"], "classification": "term_definition",
                "reason": "The semantic review retained this explicit contract term.",
            } for hit in scan["hits"]] if passed else [],
            "ai_review_gate": gate,
        },
        "typed_exit": typed_exit,
    }
    return runtime.contract_wording_derive_result(profile, mode, scope, scan, authored)

def build_wording_owner(
    runtime: Any, fixture: Path, package_root: Path, recipe: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    change_request = {
        "kind": "draft", "draft_id": "stage0-wording-eval",
        "title": "Review Stage 0 wording",
        "body": "The current change request defines one bounded delivery unit.",
        "selected_comments": [],
    }
    change_path = fixture / ".trellis/.runtime/guru-team/evals/change-request.json"
    change_path.write_text(json.dumps(change_request) + "\n", encoding="utf-8")
    if recipe == "wording-pass":
        profile, mode = "change_request", "workflow"
        scope, contents = runtime.contract_wording_build_scope(
            fixture, profile, mode,
            change_request_input=change_path.relative_to(fixture).as_posix(),
        )
        typed_exit = "pass"
    elif recipe == "wording-content-changed":
        profile, mode = "planning_artifacts", "workflow"
        task = fixture / ".trellis/tasks/current"
        scope, contents = runtime.contract_wording_build_scope(
            fixture, profile, mode, task_dir=task,
        )
        typed_exit = "content_changed"
    elif recipe == "wording-blocked":
        profile, mode = "explicit_paths", "standalone"
        scope, contents = runtime.contract_wording_build_scope(
            fixture, profile, mode,
            explicit_paths=["docs/requirements/requirement-main.md"],
        )
        typed_exit = "blocked"
    else:
        raise ValueError(f"unsupported wording owner staging recipe: {recipe}")
    scan = runtime.scan_contract_wording(scope, contents)
    return wording_review(runtime, profile, mode, scope, scan, typed_exit), change_request

def readiness_prerequisites(
    runtime: Any,
    fixture: Path,
    source: dict[str, Any],
    source_path: Path,
    mode: str,
    continuation: str = "stage0-current",
    through: str = "wording_current",
) -> dict[str, dict[str, Any]]:
    context = readiness_context(fixture, source, mode, continuation)
    if through == "context_current":
        return {"transition": context["transition"]}
    if source.get("kind") == "issue":
        live = runtime.issue_view(
            str(source.get("repo") or ""), int(source.get("number") or 0), fixture
        )
        body_sha256 = hashlib.sha256(
            str(live.get("body") or "").encode("utf-8")
        ).hexdigest()
        invocation_kind = "initial_issue"
        authority = {
            "kind": "issue",
            "repo": source.get("repo"),
            "issue_number": source.get("number"),
            "url": live.get("url"),
            "state": str(live.get("state") or "").casefold(),
            "updated_at": live.get("updatedAt"),
            "body_sha256": body_sha256,
        }
        disposition = "keep_current_open_issue"
    else:
        body_sha256 = hashlib.sha256(source["body"].encode("utf-8")).hexdigest()
        invocation_kind = "proposed_draft"
        authority = {
            "kind": "draft", "repo": "example/guru-extension",
            "issue_number": None, "url": None, "state": "draft",
            "updated_at": None, "body_sha256": body_sha256,
        }
        disposition = "keep_current_draft"
    clarity_package = fixture / ".trellis/guru-team/skills/packages/guru-clarify-requirements"
    clarity = json.loads(
        (clarity_package / "examples/requirements-clarification.json").read_text(encoding="utf-8")
    )
    clarity["mode"] = mode
    clarity["invocation_context"] = {
        "kind": invocation_kind, "caller": "stage0 readiness eval",
        "task_locator": None, "resume_target": "guru-review-contract-wording",
    }
    clarity["review_target"] = {**authority, "facts_sha256": runtime.context_digest(authority)}
    clarity["target_disposition"] = {
        "disposition": disposition,
        "duplicate_query": "repo:example/guru-extension is:issue is:open readiness eval",
        "duplicate_checked_at": "2026-01-01T00:00:00Z", "duplicate_candidates": [],
        "duplicate_facts_sha256": "0" * 64, "selected_issue": None,
        "original_target_role": "primary",
        "decision_summary": "No current duplicate replaces the reviewed draft.",
        "disposition_digest": "0" * 64,
    }
    snapshot = context["duplicate_snapshot"]
    clarity["target_disposition"].update({
        "duplicate_query": snapshot["query"],
        "duplicate_checked_at": snapshot["checked_at"],
        "duplicate_candidates": snapshot["candidates"],
        "duplicate_facts_sha256": snapshot["facts_sha256"],
    })
    clarity["context_evidence"] = {
        "status": "current",
        "evidence_refs": ["live-authority:stage0-readiness-eval"],
        "missing_reason": None,
    }
    clarity = runtime.derive_requirements_clarification_result(clarity)
    clarity = stage0_command(
        fixture, "guru-clarify-requirements", "record-requirements-clarification",
        clarity, "--mode", mode, "--input", "-",
    )
    stage0_command(
        fixture, "guru-clarify-requirements", "check-requirements-clarification",
        clarity, "--input", "-",
    )
    clarified = stage0_command(fixture, "guru-clarify-requirements", "invoke", {
        "schema_version": "1.0", "public_input": {
            "profile": "initial_change_request", "mode": mode,
            "source_exit": "context_ready", "continuation_id": continuation,
            "target_locator": context["transition"]["target_locator"],
            "duplicate_snapshot": snapshot,
        },
        "transition": context["transition"], "owner_result": clarity, "owner_context": {},
    }, "--invocation", "-")
    if clarified.get("exit_id") != "clear":
        raise ValueError("Readiness fixture requires the production clear transition")
    if through == "clarity_current":
        return {"transition": clarified["transition"], "clarity": clarity}

    scope, contents = runtime.contract_wording_build_scope(
        fixture, "change_request", mode,
        change_request_input=source_path.relative_to(fixture).as_posix(),
    )
    scan = runtime.scan_contract_wording(scope, contents)
    wording = wording_review(runtime, "change_request", mode, scope, scan, "pass")
    wording_source = {
        "source_kind": source["kind"], "identity": clarified["transition"]["target_locator"],
        "title": source["title"], "body": source["body"],
        "updated_at": source.get("updated_at"),
    }
    wording_path = source_path.with_name("wording-source.json")
    wording_path.write_text(json.dumps(wording_source) + "\n", encoding="utf-8")
    wording = stage0_command(
        fixture, "guru-review-contract-wording", "record-contract-wording-review",
        {**wording["semantic_review"], "generated_at": wording["generated_at"], "typed_exit": "pass"},
        "--mode", mode, "--profile", "change_request", "--input", "-",
        "--change-request-input", str(wording_path),
    )
    checked = stage0_command(
        fixture, "guru-review-contract-wording", "check-contract-wording-review",
        wording, "--input", "-", "--change-request-input", str(wording_path),
    )
    worded = stage0_command(fixture, "guru-review-contract-wording", "invoke", {
        "schema_version": "1.0", "public_input": {
            "profile": "change_request", "mode": mode,
            "source_exit": "clear", "continuation_id": continuation,
            "target_locator": clarified["transition"]["target_locator"],
        },
        "transition": clarified["transition"], "owner_result": wording,
        "owner_context": {"change_request": source},
        "validation_receipt": checked["validation_receipt"],
    }, "--invocation", "-")
    if worded.get("exit_id") != "pass":
        raise ValueError("Readiness fixture requires the production pass transition")
    return {"clarity": clarity, "wording": wording, "transition": worded["transition"]}

def readiness_semantic_review(
    runtime: Any, target: dict[str, Any], linkage: dict[str, Any], typed_exit: str,
) -> dict[str, Any]:
    non_ready = typed_exit != "ready"
    finding_id = "stage0-readiness-finding"
    category = {
        "clarify_requirements": "requirement_gap",
        "review_wording": "wording_gap",
        "refresh_context": "context_stale",
        "blocked": "target_complete",
    }.get(typed_exit, "requirement_gap")
    finding = {
        "finding_id": finding_id, "category": category,
        "summary": "The reviewed evidence requires the declared prerequisite route.",
        "blocking": True, "evidence_refs": ["target"],
        "affected_hashes": [target["content_sha256"]],
        "route_basis": "The semantic review selected the owner of the identified gap.",
    }
    dimensions = [{
        "id": dimension_id, "status": "failed" if non_ready and index == 0 else "passed",
        "summary": "This readiness dimension was reviewed against current linked evidence.",
        "evidence_refs": ["target"], "affected_hashes": [target["content_sha256"]],
        "finding_ids": [finding_id] if non_ready and index == 0 else [],
    } for index, dimension_id in enumerate(runtime.CHANGE_REQUEST_REVIEW_DIMENSIONS)]
    scope_conclusion = {
        "requirement_scope_basis": "The reviewed draft and current prerequisites define the scope.",
        "delivery_unit_id": "stage0-readiness-eval", "close_issues": [],
        "related_issues": [], "followup_issues": [],
        "duplicate_reuse_decision": "No duplicate replaces this delivery unit.",
        "implementation_target": "The Stage 0 minimal handoff package graph.",
        "current_gap": "The selected route identifies the next readiness owner.",
        "archived_constraints": [], "risk_boundary": ["Normal honest workflow operation only."],
        "excluded_scope": ["Workspace mutation remains downstream."],
    }
    return {
        "dimensions": dimensions, "findings": [finding] if non_ready else [],
        "scope_conclusion": scope_conclusion,
        "ai_review_gate": {
            "status": runtime.CHANGE_REQUEST_REVIEW_GATE_BY_EXIT[typed_exit],
            "reviewer": "stage0-eval-reviewer",
            "reviewed_linkage_sha256": linkage["linkage_sha256"],
            "summary": "The complete readiness evidence was reviewed for one declared route.",
            "findings_count": 1 if non_ready else 0,
            "scope_conclusion_sha256": runtime.context_digest(scope_conclusion),
        },
    }

def build_readiness_owner(
    runtime: Any,
    fixture: Path,
    package_root: Path,
    recipe: str,
    mode: str,
    profile: str,
    continuation: str = "stage0-current",
    close_issues: list[int] | None = None,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]]:
    route_by_recipe = {
        "readiness-ready": "ready",
        "readiness-clarify": "clarify_requirements",
        "readiness-wording": "review_wording",
        "readiness-refresh": "refresh_context",
        "readiness-blocked": "blocked",
    }
    typed_exit = route_by_recipe.get(recipe)
    if typed_exit is None:
        raise ValueError(f"unsupported readiness owner staging recipe: {recipe}")
    repo = "example/guru-extension"
    request_id = "stage0-readiness-eval"
    if profile == "current_issue":
        issue = runtime.issue_view(repo, 145, fixture)
        source = {
            "kind": "issue",
            "repo": repo,
            "number": 145,
            "selected_comments": [],
            "title": issue["title"], "body": issue["body"],
            "updated_at": issue["updatedAt"],
        }
    elif profile in {"proposed_draft", "standalone_request"}:
        issue = None
        source = {
            "kind": "draft", "draft_id": f"draft:{request_id}",
            "title": "Review Stage 0 readiness",
            "body": "The current Intake workflow is one independently deliverable unit.",
            "selected_comments": [],
        }
        source["draft_id"] = "draft:" + hashlib.sha256(source["body"].encode()).hexdigest()
    else:
        raise ValueError(f"unsupported readiness input profile: {profile}")
    source_path = fixture / ".trellis/.runtime/guru-team/evals/change-request.json"
    source_path.write_text(json.dumps(source) + "\n", encoding="utf-8")
    prerequisites = readiness_prerequisites(
        runtime, fixture, source, source_path, mode, continuation,
        {"clarify_requirements": "context_current", "review_wording": "clarity_current"}.get(
            typed_exit, "wording_current"
        ),
    )
    scope, _ = runtime.contract_wording_build_scope(
        fixture, "change_request", mode,
        change_request_input=source_path.relative_to(fixture).as_posix(),
    )
    title_sha256, body_sha256, _ = runtime.change_request_review_scope_hashes(scope)
    if profile == "current_issue":
        raw_target = {
            "kind": "existing_issue",
            "repo": repo,
            "issue_number": 145,
            "url": issue.get("url") if isinstance(issue, dict) else None,
            "updated_at": issue.get("updatedAt") if isinstance(issue, dict) else None,
            "title_sha256": title_sha256,
            "body_sha256": body_sha256,
        }
    else:
        source_request_sha256 = runtime.context_digest(
            runtime.change_request_review_request_authority_projection(
                repo, source, body_sha256
            )
        )
        raw_target = {
            "kind": profile,
            "repo": repo,
            "source_request_sha256": source_request_sha256,
            "title_sha256": title_sha256,
            "body_sha256": body_sha256,
            "side_effect_free": True,
            **(
                {"draft_id": source["draft_id"]}
                if profile == "proposed_draft"
                else {
                    "caller_locator": "stage0-eval",
                    "request_id": source["draft_id"],
                }
            ),
        }
    target, scope, contents = runtime.change_request_review_normalize_target(
        fixture, raw_target, source_path.relative_to(fixture).as_posix(), mode,
    )
    transition = prerequisites["transition"]
    review = runtime.readiness_runtime
    projections = review.normalize_prerequisites(
        transition, target, source, package_root,
    )
    linkage = review.linkage(target, projections)
    semantic_review = readiness_semantic_review(runtime, target, linkage, typed_exit)
    if close_issues is not None:
        semantic_review["scope_conclusion"]["close_issues"] = close_issues
        semantic_review["ai_review_gate"]["scope_conclusion_sha256"] = runtime.context_digest(
            semantic_review["scope_conclusion"]
        )
    authored = {
        "generated_at": "2026-01-01T00:00:00Z", "mode": mode,
        "target": raw_target,
        "semantic_review": semantic_review,
        "typed_exit": typed_exit,
        "reason": "The semantic readiness review selected exactly one declared route.",
        "affected_evidence": [{
            "ref": "target", "sha256": target["content_sha256"],
            "summary": "The current reviewed change-request title and body.",
        }],
        "consumer": runtime.CHANGE_REQUEST_REVIEW_CONSUMERS[typed_exit],
    }
    envelope = {
        "schema_version": "1.0", "public_input": {
            "profile": profile, "source_exit": "start", "mode": mode,
            "continuation_id": continuation,
            "target_locator": transition["target_locator"],
        },
        "transition": transition, "owner_context": {"change_request": source},
        "owner_result": authored,
    }
    result = stage0_command(
        fixture, "guru-review-change-request", "record-change-request-review",
        envelope, "--invocation", "-",
    )
    envelope["owner_result"] = result
    checked = stage0_command(
        fixture, "guru-review-change-request", "check-change-request-review",
        envelope, "--invocation", "-",
    )
    envelope["validation_receipt"] = checked["validation_receipt"]
    return result, {"invocation": envelope, "producer_results": prerequisites}, source

def workspace_prerequisites(
    runtime: Any, fixture: Path, mode: str,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any], dict[str, Any]]:
    repo = "example/guru-extension"
    issue_number = 145
    issue_url = f"https://github.com/{repo}/issues/{issue_number}"
    updated_at = "2026-01-01T00:00:00Z"
    title = "Stage 0 workspace owner staging"
    body = "The current Intake workflow is one independently deliverable unit."
    title_sha256 = hashlib.sha256(title.encode("utf-8")).hexdigest()
    body_sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()

    head = run_git(fixture, "rev-parse", "HEAD")
    base = workspace_base_fixture(runtime, head)
    package = fixture / ".trellis/guru-team/skills/packages/guru-review-change-request"
    readiness, state, _ = build_readiness_owner(
        runtime, fixture, package, "readiness-ready", mode, "current_issue",
        close_issues=[issue_number],
    )
    public = stage0_command(
        fixture, "guru-review-change-request", "invoke", state["invocation"],
        "--invocation", "-",
    )
    if public.get("exit_id") != "ready":
        raise ValueError("Workspace fixture requires the production ready transition")
    transition = public["transition"]
    return {
        "base": base,
        "discovery": {
            "context_result_sha256": transition["context_result_sha256"],
        },
        "clarity": state["producer_results"]["clarity"],
        "wording": state["producer_results"]["wording"],
        "readiness": readiness,
    }, {
        "repo": repo, "issue_number": issue_number, "url": issue_url,
        "updated_at": updated_at, "title": title, "body": body,
        "title_sha256": title_sha256, "body_sha256": body_sha256,
    }, transition

def workspace_plan(
    runtime: Any,
    fixture: Path,
    recipe: str,
    mode: str,
    prerequisites: dict[str, dict[str, Any]],
    issue: dict[str, Any],
) -> dict[str, Any]:
    projections: dict[str, dict[str, Any]] = {}
    for key, payload in prerequisites.items():
        projections[key] = runtime.task_workspace_prerequisite_projection(
            key, f"call-local:{key}", payload, runtime.context_digest(payload)
        )

    gate_status = {
        "workspace-created": "passed",
        "workspace-refresh-review": "reroute",
        "workspace-blocked": "blocked",
        "workspace-invalid-task-state": "passed",
    }.get(recipe)
    if gate_status is None:
        raise ValueError(f"unsupported task workspace owner staging recipe: {recipe}")
    task_slug = "145-stage0-owner-eval"
    task_dir = f".trellis/tasks/{time.strftime('%m-%d')}-{task_slug}"
    scope_item = {
        "number": issue["issue_number"], "url": issue["url"],
        "title": issue["title"],
        "reason": "The reviewed Stage 0 delivery unit closes this exact issue.",
    }
    base_result = prerequisites["base"]
    naming_disposition = "conflict_blocked" if gate_status == "blocked" else "create_new"
    plan: dict[str, Any] = {
        "schema_version": "2.0", "skill_id": "guru-create-task-workspace",
        "generated_at": "2026-01-01T00:00:00Z", "mode": mode,
        "invocation": {
            "caller": "guru-review-change-request:ready", "target_kind": "existing_issue",
            "action_scope": "workspace_and_task_mutation",
            "resume_identity": "stage0-workspace-eval",
        },
        "prerequisites": projections,
        "target": {
            "kind": "existing_issue", "repo": issue["repo"],
            "issue_number": issue["issue_number"], "url": issue["url"],
            "state": "open", "updated_at": issue["updated_at"],
            "title_sha256": issue["title_sha256"], "body_sha256": issue["body_sha256"],
            "draft": None,
            "disposition_sha256": prerequisites["clarity"]["target_disposition"]["disposition_digest"],
            "duplicate_decision_sha256": prerequisites["clarity"]["target_disposition"]["duplicate_facts_sha256"],
            "created_issue_binding_sha256": None, "created_issue_result": None,
        },
        "scope": {
            "primary": scope_item, "close": [scope_item], "related": [], "followup": [],
            "scope_sha256": "0" * 64,
        },
        "base": {
            "selected_base": base_result["resolution"]["selected_base"],
            "remote": base_result["resolution"]["remote"],
            "base_ref": base_result["git"]["remote_ref"],
            "decision_head": base_result["decision_checkout"]["head_after"],
            "local_head": base_result["git"]["local_head_after"],
            "remote_head": base_result["git"]["remote_head_after"],
            "post_sync_resolution_sha256": base_result["post_sync_resolution_sha256"],
            "sync_facts_sha256": base_result["facts_sha256"],
        },
        "naming": {
            "branch_name": f"feat/{task_slug}", "workspace_slug": task_slug,
            "task_slug": task_slug, "task_title": "#145 Stage 0 owner eval",
            "reason": "Names bind the reviewed issue and isolated eval workspace.",
            "branch_disposition": naming_disposition,
            "workspace_disposition": naming_disposition,
            "task_disposition": naming_disposition,
        },
        "assignee": {
            "login": "stage0-eval", "source": "single_issue_assignee",
            "candidates": ["stage0-eval"],
            "resolution_evidence": "The live source issue has one exact assignee.",
        },
        "side_effects": {
            "operations": [
                "create_branch", "create_worktree", "create_task",
                "write_task_artifacts", "write_runtime_mappings",
            ],
            "task_artifacts": [
                f"{task_dir}/{name}" for name in runtime.TASK_WORKSPACE_ARTIFACT_NAMES
            ],
            "runtime_mappings": [
                f".trellis/.runtime/guru-team/workspaces/{task_slug}.json",
                f".trellis/.runtime/guru-team/tasks/{task_slug}.json",
            ],
            "command_argv": ["create-task-workspace", "--invocation", "-"],
            "stop_after": "created_workspace",
        },
        "ai_review_gate": {
            "status": gate_status, "reviewer": "stage0-eval-reviewer",
            "reviewed_plan_sha256": "0" * 64,
            "summary": "The exact target, names, assignee, scope and mutation boundary were reviewed.",
            "evidence": [
                "The invocation owns one isolated workspace and task.",
                "All durable artifacts are task-local and all runtime mappings are ignored.",
            ],
        },
        "freshness": {
            "captured_at": "2026-01-01T00:00:00Z",
            "reviewable_plan_sha256": "0" * 64, "plan_sha256": "0" * 64,
        },
    }
    plan["scope"]["scope_sha256"] = runtime.task_workspace_scope_digest(plan["scope"])
    reviewable = runtime.context_digest(runtime.task_workspace_reviewable_projection(plan))
    plan["ai_review_gate"]["reviewed_plan_sha256"] = reviewable
    plan["freshness"]["reviewable_plan_sha256"] = reviewable
    plan["freshness"]["plan_sha256"] = runtime.task_workspace_plan_digest(plan)
    return plan

def call_runtime_with_json(
    function: Any,
    args: argparse.Namespace,
    payload: dict[str, Any],
) -> dict[str, Any]:
    previous_stdin = sys.stdin
    sys.stdin = io.StringIO(json.dumps(payload))
    try:
        return function(args)
    finally:
        sys.stdin = previous_stdin

def build_workspace_owner(
    runtime: Any, fixture: Path, recipe: str, mode: str,
) -> dict[str, Any]:
    prerequisites, issue, transition = workspace_prerequisites(runtime, fixture, mode)
    plan = workspace_plan(
        runtime, fixture, recipe, mode, prerequisites, issue
    )
    if recipe == "workspace-invalid-task-state":
        workspace_path = fixture.parent / "owner-worktrees" / plan["naming"]["workspace_slug"]
        task_dir = workspace_path / Path(plan["side_effects"]["task_artifacts"][0]).parent
        task_dir.mkdir(parents=True, exist_ok=True)
        (task_dir / "task.json").write_text(
            json.dumps({
                "id": plan["naming"]["task_slug"],
                "name": plan["naming"]["task_slug"],
                "status": "in_progress",
                "branch": plan["naming"]["branch_name"],
            }) + "\n",
            encoding="utf-8",
        )
    if not isinstance(transition, dict):
        raise ValueError("workspace readiness transition is unavailable")
    if transition.get("stage") != "readiness_current":
        raise ValueError("workspace readiness transition stage is invalid")
    transition_payloads = prerequisites
    plan["prerequisites"] = {
        key: runtime.task_workspace_prerequisite_projection(
            key,
            f"call-local:{key}",
            payload,
            runtime.context_digest(payload),
        )
        for key, payload in transition_payloads.items()
    }
    reviewable = runtime.context_digest(
        runtime.task_workspace_reviewable_projection(plan)
    )
    plan["ai_review_gate"]["reviewed_plan_sha256"] = reviewable
    plan["freshness"]["reviewable_plan_sha256"] = reviewable
    plan["freshness"]["plan_sha256"] = runtime.task_workspace_plan_digest(plan)
    WORKSPACE_CALL_LOCAL_STATE[str(fixture.resolve())] = (
        copy.deepcopy(plan),
        copy.deepcopy(transition),
    )
    common = {
        "schema_version": "1.0",
        "plan": plan,
        "transition": transition,
    }
    call_runtime_with_json(
        runtime.cmd_record_task_workspace_plan,
        argparse.Namespace(root=str(fixture), input=None, invocation="-", plan_input=None),
        common,
    )
    result = call_runtime_with_json(
        runtime.cmd_create_task_workspace,
        argparse.Namespace(
            root=str(fixture), input=None, invocation="-", plan_input=None,
            refresh_review=recipe == "workspace-refresh-review",
            reason=None,
            reason_code=(
                "disposition_changed" if recipe == "workspace-refresh-review"
                else "object_conflict" if recipe == "workspace-blocked" else None
            ),
        ),
        common,
    )
    return call_runtime_with_json(
        runtime.cmd_check_task_workspace_result,
        argparse.Namespace(root=str(fixture), input=None, invocation="-", plan_input=None),
        {**common, "result": result},
    )
