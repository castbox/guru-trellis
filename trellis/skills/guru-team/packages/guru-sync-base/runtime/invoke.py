from __future__ import annotations
import argparse
import json
from runtime.io import CommandError, read_json
from execute import run as execute
from check import run as check
from common import digest, repo
from runtime.base_selection import object_source, select_base, git
from runtime.schema import validate_json


_BLOCKED_OWNER_CODES = frozenset({"git_failed", "schema_mismatch", "stale_identity"})

def run(package_root, command, argv):
    p=argparse.ArgumentParser(add_help=False); p.add_argument("--json",action="store_true"); p.add_argument("--invocation",required=True)
    try:a=p.parse_args(argv)
    except SystemExit as exc: raise CommandError("invalid_arguments","arguments","Use --invocation with one JSON object.") from exc
    data=read_json(a.invocation,"invocation"); public=data.get("public_input",data); mode=public.get("mode"); route=public.get("route","repo_change")
    validate_json(data, package_root.parents[1]/"consumers/workflow/stage0/invocations/deterministic-sync-3.0.schema.json", "invocation")
    validate_json(public, package_root/"schemas/public-input-current-3.0.schema.json", "public_input")
    if "return_identity" in public:
        if public["return_identity"].get("profile")=="existing_issue_intake":
            validate_json(public, package_root/"schemas/public-issue-review-refresh-input-1.0.schema.json", "public_input")
        else:
            validate_json(public, package_root/"schemas/public-confirmation-refresh-read-input-1.0.schema.json", "public_input")
    if mode not in ("workflow","standalone"): raise CommandError("invalid_arguments","invocation.public_input.mode","Use workflow or standalone.")
    if route not in ("repo_change","original_request"): raise CommandError("invalid_arguments","invocation.public_input.route","Use repo_change or original_request.")
    if route=="original_request":
        if mode != "workflow": raise CommandError("invalid_arguments","invocation.public_input.route","Standalone base sync cannot select the original-request route.")
        return {"exit_id":"skipped","continuation_id":f"{public.get('source_exit','start')}-original-request"}
    repo_locator=public.get("repo_root",".")
    repo(repo_locator)
    operation=public.get("operation", "sync")
    if operation not in ("sync", "read"):
        raise CommandError("invalid_arguments", "public_input.operation", "Use read for a fixed baseline or sync for actual synchronization.")
    if operation == "read":
        root=repo(repo_locator)
        selected_ref=public.get("base_ref")
        source="explicit"
        if not selected_ref:
            selected=select_base(root, public.get("base_branch"))
            local_ref="refs/heads/"+selected["selected_base"]
            selected_ref=local_ref if git(root,"rev-parse","--verify","--quiet",local_ref,check=False) else "refs/remotes/"+selected["remote"]+"/"+selected["selected_base"]
            source=selected["source"]
        if public.get("return_identity",{}).get("profile")=="existing_issue_intake":
            # Restore the already adopted object, preserving its source locator.
            # A later value of that locator is not the selected source.
            baseline=object_source(root, public["base_commit"], source=source)
            baseline["selected_ref"]=selected_ref
            baseline["identity_sha256"]=digest({key:value for key,value in baseline.items() if key!="identity_sha256"})
        else:
            baseline=object_source(root, selected_ref, public.get("base_commit"), source)
        transition={"schema_version":"2.0", "transition_id":"base_current:"+baseline["identity_sha256"][:24], "stage":"base_current", "mode":mode, "repo_locator":str(root), "base":baseline}
        output={"exit_id":"baseline_ready", "handoff_profile":"pre_task", "handoff_mode":mode, "handoff_continuation_id":"stage0-current", "transition":transition}
        if "return_identity" in public:
            output.update(handoff_profile="existing_issue_intake" if public["return_identity"]["profile"]=="existing_issue_intake" else "context_request", handoff_continuation_id=public["return_identity"]["continuation_id"], return_identity=public["return_identity"])
        validate_json(output,package_root/"schemas/public-baseline-ready-output-3.0.schema.json","stdout")
        return output
    base_args=["--mode",mode,"--root",repo_locator]+(["--base",public["base_branch"]] if public.get("base_branch") else [])
    try:
        resolved=execute(package_root,command,[*base_args,"--resolve-only"]); synced=execute(package_root,command,[*base_args,"--execute","--expected-resolution-sha256",resolved["resolution_sha256"]]); checked=check(package_root,command,["--mode",mode,"--root",repo_locator,"--result-json",json.dumps(synced),"--expected-resolution-sha256",resolved["resolution_sha256"]])
    except CommandError as exc:
        if exc.code in _BLOCKED_OWNER_CODES:
            return {"exit_id":"blocked"}
        raise
    authority_locator=checked["authority_repo_locator"]
    transition={
        "schema_version":"1.0",
        "transition_id":f"base_current:{digest({'mode':mode,'repo_locator':authority_locator,'checked':checked})[:24]}",
        "stage":"base_current",
        "mode":mode,
        "repo_locator":authority_locator,
        "base":{
            "source":resolved["source"],
            "selected_base":checked["selected_base"],
            "remote":resolved["remote"],
            "ordered_candidates":resolved["candidates"],
            "decision_head":checked["head"],
            "local_base_head":synced["git"]["local_head_after"],
            "remote_base_head":synced["git"]["remote_head_after"],
            "post_sync_resolution_sha256":checked["post_sync_resolution_sha256"],
        },
    }
    output = {
        "exit_id":"synced",
        "handoff_profile":"pre_task",
        "handoff_mode":mode,
        "handoff_repo_locator":authority_locator,
        "handoff_base_branch":checked["selected_base"],
        "handoff_continuation_id":"stage0-current",
        "transition":transition,
    }

    if "return_identity" in public:
        output.update(handoff_profile="existing_issue_intake", handoff_continuation_id=public["return_identity"]["continuation_id"], return_identity=public["return_identity"])
    validate_json(output, package_root/"schemas/public-synced-output-3.0.schema.json", "stdout")
    return output
