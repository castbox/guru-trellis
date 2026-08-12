from __future__ import annotations
import argparse,copy
from runtime.io import CommandError,read_json
from runtime.schema import validate_json
from common import digest,validate_owner
def run(package_root,command,argv):
    p=argparse.ArgumentParser(add_help=False);p.add_argument("--json",action="store_true");p.add_argument("--invocation",required=True)
    try:a=p.parse_args(argv)
    except SystemExit as exc: raise CommandError("invalid_arguments","arguments","Use --invocation with one JSON object.") from exc
    envelope=read_json(a.invocation,"invocation"); public=envelope.get("public_input",{}); owner=validate_owner(package_root,envelope.get("owner_result",{})); exit_id=owner["typed_exit"]
    if public.get("profile")=="initial_change_request" and public.get("source_exit")=="context_ready":
        snapshot=public.get("duplicate_snapshot"); disposition=owner.get("target_disposition")
        if not isinstance(snapshot,dict) or not isinstance(disposition,dict): raise CommandError("stale_identity","public_input.duplicate_snapshot","Refresh context and reuse its checked duplicate snapshot.",3)
        unsigned={key:copy.deepcopy(snapshot[key]) for key in ("query","checked_at","target_locator","authority_content_sha256","candidates")}
        expected=[{**item,"identity":f"#{item['number']}","state":"open","decision":next((row.get("decision") for row in disposition.get("duplicate_candidates",[]) if row.get("repo")==item["repo"] and row.get("number")==item["number"]),None),"reason":next((row.get("reason") for row in disposition.get("duplicate_candidates",[]) if row.get("repo")==item["repo"] and row.get("number")==item["number"]),None)} for item in snapshot["candidates"]]
        if snapshot.get("facts_sha256")!=digest(unsigned) or snapshot.get("target_locator")!=public.get("target_locator") or snapshot.get("authority_content_sha256")!=envelope.get("transition",{}).get("authority_content_sha256") or disposition.get("duplicate_query")!=snapshot.get("query") or disposition.get("duplicate_checked_at")!=snapshot.get("checked_at") or disposition.get("duplicate_candidates")!=expected or disposition.get("duplicate_facts_sha256")!=snapshot.get("facts_sha256"):
            raise CommandError("stale_identity","public_input.duplicate_snapshot","Refresh context before deciding duplicate disposition.",3)
    output=copy.deepcopy(envelope.get("typed_output"))
    if not isinstance(output,dict) or output.get("exit_id")!=exit_id: raise CommandError("semantic_result_invalid","invocation.typed_output","Provide the AI-reviewed typed output for the checked owner result.",3)
    validate_json(output,next(package_root.glob(f"schemas/public-{exit_id.replace('_','-')}-output*.schema.json")),"typed_output")
    return output
