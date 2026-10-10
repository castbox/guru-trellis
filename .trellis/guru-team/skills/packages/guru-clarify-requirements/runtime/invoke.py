from __future__ import annotations
import argparse,re
from pathlib import Path
from runtime.task_lifecycle import LifecycleContractError, resolve_active_task_checkout
from runtime.io import CommandError,read_json
from runtime.schema import validate_json
from common import validate_owner

OUTPUT_SCHEMAS = {
    "clear": "public-clear-output-3.0.schema.json",
    "needs_context": "public-needs-context-output.schema.json",
    "refresh_context": "public-refresh-context-output.schema.json",
    "retarget_context": "public-retarget-context-output.schema.json",
    "new_task": "public-new-task-output.schema.json",
    "blocked": "public-blocked-output.schema.json",
}


def typed_output(package_root, public, transition, owner):
    exit_id = owner["typed_exit"]
    if exit_id == "blocked":
        output = {"exit_id": "blocked"}
    elif exit_id == "clear":
        identity = owner["content_identity"]
        disposition = owner["target_disposition"]
        active_task_clear = (
            public.get("profile") == "active_task_scope_change"
            and owner.get("invocation_context", {}).get("kind") == "active_task_scope_change"
        )
        disposition_names = {
            "keep_current_open_issue": "retained",
            "keep_current_draft": "retained",
            "retarget_existing_issue": "selected",
            "reopen_closed_issue": "reopened",
            "create_followup_draft": "retained",
            "block_target_complete": "complete",
        }
        if not isinstance(transition, dict) or transition.get("stage") != "context_current":
            raise CommandError("stale_identity", "transition", "Provide the current context transition.", 3)
        if disposition is None and active_task_clear:
            public_disposition = "retained"
            transition_disposition = {
                "disposition_sha256": identity["disposition_sha256"],
                "duplicate_facts_sha256": identity["disposition_sha256"],
            }
        elif isinstance(disposition, dict) and disposition.get("disposition") in disposition_names:
            public_disposition = disposition_names[disposition["disposition"]]
            transition_disposition = {
                "disposition_sha256": disposition.get("disposition_digest"),
                "duplicate_facts_sha256": disposition.get("duplicate_facts_sha256"),
            }
        else:
            raise CommandError("semantic_result_invalid", "owner_result.target_disposition", "Use the checked target disposition.", 3)
        current = dict(transition)
        current.pop("authority_content_sha256", None)
        current.update({
            "clarify_profile": public["profile"],
            "source_selection": owner["source_selection"],
            "stage": "clarity_current",
            "transition_id": f"clarity_current:{identity['result_sha256'][:24]}",
            "clarity_result_sha256": identity["result_sha256"],
            "target_content_sha256": identity["content_sha256"],
            "clarity": {
                "facts_sha256": identity["result_sha256"],
                "target_sha256": identity["target_sha256"],
                "disposition_sha256": identity["disposition_sha256"],
                "content_sha256": identity["content_sha256"],
                "scope_sha256": identity["scope_sha256"],
            },
            "target_disposition": transition_disposition,
        })
        output = {
            "exit_id": "clear",
            "profile": public["profile"],
            "source_selection": owner["source_selection"],
            "resume_target": owner["invocation_context"]["resume_target"],
            "target_disposition": public_disposition,
            "continuation_id": public["continuation_id"],
            "transition": current,
        }
    elif exit_id == "needs_context":
        if not isinstance(transition, dict) or transition.get("stage") != "context_current":
            raise CommandError("stale_identity", "transition", "Provide the current context transition.", 3)
        base = transition.get("base")
        if not isinstance(base, dict):
            raise CommandError("stale_identity", "transition.base", "Provide the current base transition.", 3)
        required_base_fields = (
            "source", "selected_base", "remote", "ordered_candidates",
            "decision_head", "local_base_head", "remote_base_head",
            "post_sync_resolution_sha256",
        )
        if any(field not in base for field in required_base_fields):
            raise CommandError("stale_identity", "transition.base", "Provide the current base transition.", 3)
        if (
            not isinstance(base["source"], str)
            or base["source"] not in {"explicit", "config", "config-candidate", "remote-default"}
            or not isinstance(base["selected_base"], str) or not base["selected_base"]
            or not isinstance(base["remote"], str) or not base["remote"]
            or not isinstance(base["ordered_candidates"], list)
            or not base["ordered_candidates"]
            or any(not isinstance(candidate, str) or not candidate for candidate in base["ordered_candidates"])
            or len(set(base["ordered_candidates"])) != len(base["ordered_candidates"])
            or any(
                not isinstance(base[field], str)
                or not re.fullmatch(r"[0-9a-f]{40}", base[field])
                for field in ("decision_head", "local_base_head", "remote_base_head")
            )
            or not isinstance(base["post_sync_resolution_sha256"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", base["post_sync_resolution_sha256"])
        ):
            raise CommandError("stale_identity", "transition.base", "Provide the current base transition.", 3)
        if not isinstance(transition.get("repo_locator"), str) or not transition["repo_locator"]:
            raise CommandError("stale_identity", "transition.repo_locator", "Provide the current repository transition.", 3)
        base_transition = {
            "schema_version": "1.0",
            "transition_id": f"base_current:{base['post_sync_resolution_sha256'][:24]}",
            "stage": "base_current",
            "mode": transition["mode"],
            "repo_locator": transition["repo_locator"],
            "base": base,
        }
        output = {
            "exit_id": "needs_context",
            "handoff_profile": "context_request",
            "handoff_mode": public["mode"],
            "handoff_repo_locator": transition.get("repo_locator") or ".",
            "handoff_base_branch": base["selected_base"],
            "handoff_continuation_id": public["continuation_id"],
            "transition": base_transition,
            "return_identity": {
                key: public[key] for key in (
                    "profile", "target_locator", "continuation_id",
                    "source_locators", "task_locator", "task_id",
                    "lifecycle_generation", "resume_target",
                ) if key in public
            },
        }
    elif exit_id in {"refresh_context", "retarget_context"}:
        output = {
            "exit_id": exit_id,
            "handoff_mode": public["mode"],
            "handoff_repo_root": (transition or {}).get("repo_locator") or ".",
            "handoff_route": "repo_change",
        }
        base = (transition or {}).get("base")
        if (
            isinstance(base, dict)
            and base.get("selected_base")
            and base.get("source") == "explicit"
        ):
            output["handoff_base_branch"] = base["selected_base"]
    elif exit_id == "new_task":
        output = {
            "exit_id": "new_task",
            "target_locator": public["target_locator"],
            "continuation_id": public["continuation_id"],
        }
    else:
        raise CommandError("schema_mismatch", "typed_exit", "Return one declared typed exit.", 3)
    validate_json(output, package_root / "schemas" / OUTPUT_SCHEMAS[exit_id], "stdout")
    return output


def run(package_root,command,argv):
    p=argparse.ArgumentParser(add_help=False);p.add_argument("--json",action="store_true");p.add_argument("--invocation",required=True)
    try:a=p.parse_args(argv)
    except SystemExit as exc: raise CommandError("invalid_arguments","arguments","Use --invocation with one JSON object.") from exc
    envelope=read_json(a.invocation,"invocation")
    validate_json(envelope, package_root.parents[1] / "consumers/workflow/stage0/invocations/semantic-owner.schema.json", "invocation")
    public=envelope["public_input"]
    profiles = {
        "standard_intake": "public-standard-intake-input.schema.json",
        "reviewed_plan_intake": "public-reviewed-plan-intake-input.schema.json",
        "active_task_scope_change": "public-active-task-scope-change-input.schema.json",
        "standalone_review": "public-standalone-review-input.schema.json",
        "normal_scenario_scope_confirmation": "public-normal-scenario-scope-confirmation-input.schema.json",
        "solution_mechanism_scope_confirmation": "public-solution-mechanism-scope-confirmation-input.schema.json",
    }
    profile = public.get("profile")
    if profile not in profiles:
        raise CommandError("schema_mismatch", "public_input.profile", "Use a current Clarify profile; migrate initial_change_request through fresh Intake.", 3)
    validate_json(public, package_root / "schemas" / profiles[profile], "public_input")
    owner=validate_owner(package_root,envelope["owner_result"])
    transition=envelope.get("transition")
    exit_id=owner["typed_exit"]
    if public.get("mode") != owner.get("mode"):
        raise CommandError("stale_identity", "mode", "Match the public input to the checked owner result.", 3)
    context = owner["invocation_context"]
    if profile in {"normal_scenario_scope_confirmation", "solution_mechanism_scope_confirmation"}:
        if context["kind"] != profile or context["resume_target"] != public["resume_target"]:
            raise CommandError("stale_identity", "resume_target", "Return to the original qualification owner.", 3)
        if exit_id == "needs_context":
            raise CommandError("schema_mismatch", "typed_exit", "Repair authority through the original qualification owner.", 3)
    elif profile == "active_task_scope_change":
        try:
            task = resolve_active_task_checkout(Path.cwd(), public["task_locator"]).artifact
        except LifecycleContractError as exc:
            raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
        if (task.task_id, task.lifecycle_generation) != (public["task_id"], public["lifecycle_generation"]):
            raise CommandError("stale_identity", "task_id", "Rebuild the current active-task input from live task identity.", 3)
        if context["kind"] != profile or context["task_locator"] != public["task_locator"] or context["resume_target"] != public["resume_target"]:
            raise CommandError("stale_identity", "task_locator", "Preserve the interrupted task and original caller.", 3)
    elif profile == "standalone_review" and (context["kind"] != profile or context["resume_target"] != public["resume_target"]):
        raise CommandError("stale_identity", "resume_target", "Preserve the declared standalone consumer.", 3)
    if profile == "reviewed_plan_intake" and (not isinstance(transition, dict) or transition.get("source_locators") != public["source_locators"]):
        raise CommandError("stale_identity", "source_locators", "Refresh the selected source projection before clarification.", 3)
    if isinstance(transition, dict):
        if transition.get("mode") != public.get("mode"):
            raise CommandError("stale_identity", "transition.mode", "Match the transition to the public input.", 3)
        if transition.get("continuation_id") and transition.get("continuation_id") != public.get("continuation_id"):
            raise CommandError("stale_identity", "continuation_id", "Refresh the current transition before invoking the Skill.", 3)
        if transition.get("target_locator") and public.get("target_locator") and transition["target_locator"] != public["target_locator"]:
            raise CommandError("stale_identity", "target_locator", "Refresh the current target transition before invoking the Skill.", 3)
    if public.get("profile") in {"standard_intake", "reviewed_plan_intake"} and public.get("source_exit")=="context_ready":
        snapshot=public.get("duplicate_snapshot"); disposition=owner.get("target_disposition")
        if not isinstance(snapshot,dict) or not isinstance(disposition,dict): raise CommandError("stale_identity","public_input.duplicate_snapshot","Refresh context and reuse its checked duplicate snapshot.",3)
        expected=[{**item,"identity":f"#{item['number']}","state":"open","decision":next((row.get("decision") for row in disposition.get("duplicate_candidates",[]) if row.get("repo")==item["repo"] and row.get("number")==item["number"]),None),"reason":next((row.get("reason") for row in disposition.get("duplicate_candidates",[]) if row.get("repo")==item["repo"] and row.get("number")==item["number"]),None)} for item in snapshot["candidates"]]
        if snapshot.get("target_locator")!=public.get("target_locator") or snapshot.get("authority_content_sha256")!=envelope.get("transition",{}).get("authority_content_sha256") or disposition.get("duplicate_query")!=snapshot.get("query") or disposition.get("duplicate_checked_at")!=snapshot.get("checked_at") or disposition.get("duplicate_candidates")!=expected or disposition.get("duplicate_facts_sha256")!=snapshot.get("facts_sha256"):
            raise CommandError("stale_identity","public_input.duplicate_snapshot","Refresh context before deciding duplicate disposition.",3)
    return typed_output(package_root, public, transition, owner)
