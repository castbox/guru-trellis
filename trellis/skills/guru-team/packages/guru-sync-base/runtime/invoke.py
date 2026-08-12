from __future__ import annotations
import argparse
import json
from runtime.io import CommandError, read_json
from execute import run as execute
from check import run as check
from common import digest, repo


_BLOCKED_OWNER_CODES = frozenset({"git_failed", "schema_mismatch", "stale_identity"})

def run(package_root, command, argv):
    p=argparse.ArgumentParser(add_help=False); p.add_argument("--json",action="store_true"); p.add_argument("--invocation",required=True)
    try:a=p.parse_args(argv)
    except SystemExit as exc: raise CommandError("invalid_arguments","arguments","Use --invocation with one JSON object.") from exc
    data=read_json(a.invocation,"invocation"); public=data.get("public_input",data); mode=public.get("mode"); route=public.get("route","repo_change")
    if mode not in ("workflow","standalone"): raise CommandError("invalid_arguments","invocation.public_input.mode","Use workflow or standalone.")
    if route not in ("repo_change","original_request"): raise CommandError("invalid_arguments","invocation.public_input.route","Use repo_change or original_request.")
    if route=="original_request":
        if mode != "workflow": raise CommandError("invalid_arguments","invocation.public_input.route","Standalone base sync cannot select the original-request route.")
        return {"exit_id":"skipped","continuation_id":f"{public.get('source_exit','start')}-original-request"}
    repo_locator=public.get("repo_root",".")
    repo(repo_locator)
    base_args=["--mode",mode,"--root",repo_locator]+(["--base",public["base_branch"]] if public.get("base_branch") else [])
    try:
        resolved=execute(package_root,command,[*base_args,"--resolve-only"]); synced=execute(package_root,command,[*base_args,"--execute","--expected-resolution-sha256",resolved["resolution_sha256"]]); checked=check(package_root,command,["--mode",mode,"--root",repo_locator,"--result-json",json.dumps(synced),"--expected-resolution-sha256",resolved["resolution_sha256"]])
    except CommandError as exc:
        if exc.code in _BLOCKED_OWNER_CODES:
            return {"exit_id":"blocked"}
        raise
    transition={
        "schema_version":"1.0",
        "transition_id":f"base_current:{digest({'mode':mode,'repo_locator':repo_locator,'checked':checked})[:24]}",
        "stage":"base_current",
        "mode":mode,
        "repo_locator":repo_locator,
        "base":{
            "source":resolved["source"],
            "selected_base":checked["selected_base"],
            "remote":resolved["remote"],
            "ordered_candidates":resolved["candidates"],
            "decision_head":resolved["decision_checkout"]["head"],
            "local_base_head":synced["git"]["local_head_after"],
            "remote_base_head":synced["git"]["remote_head_after"],
            "post_sync_resolution_sha256":checked["post_sync_resolution_sha256"],
        },
    }
    return {
        "exit_id":"synced",
        "handoff_profile":"pre_task",
        "handoff_mode":mode,
        "handoff_repo_locator":repo_locator,
        "handoff_base_branch":checked["selected_base"],
        "handoff_continuation_id":"stage0-current",
        "transition":transition,
    }
