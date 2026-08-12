from __future__ import annotations
import argparse,json
from pathlib import Path
from common import active_task,check_recovery,identity,load,parse,preview,root,validate
from runtime.io import CommandError
def run(package_root:Path,command:dict,argv:list[str])->dict:
 if command["id"]=="preview-change-context-history":
  p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--query-json");p.add_argument("--limit",type=int,default=20);a=parse(p,argv);repo=root(package_root,a.root)
  try:q=json.loads(a.query_json) if a.query_json else {}
  except Exception as exc:raise CommandError("invalid_json","query_json","Provide one query object.") from exc
  if not 1<=a.limit<=100:raise CommandError("invalid_arguments","limit","Use 1 through 100.")
  return preview(repo,q,a.limit)
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--input",required=True);p.add_argument("--expected-result-sha256");p.add_argument("--active-task");p.add_argument("--recovery-continuation-id");a=parse(p,argv);repo=root(package_root,a.root);v=validate(package_root,load(repo,package_root,a.input,"input"))
 rebuilt=preview(repo,v["change_input"],v["history_preview"]["limit"])
 if any(v["history_preview"].get(k)!=rebuilt.get(k) for k in ("query_sha256","archive_manifest_sha256","preview_sha256","manifest","candidates","invalid")) or v["result_identity"]!=identity(v):raise CommandError("stale_identity","owner_result","Rerun discovery from current history.",3)
 if a.recovery_continuation_id and not a.active_task:raise CommandError("invalid_arguments","recovery_continuation_id","Provide active-task identity for recovery.")
 if a.active_task:
  if v["mode"]!="workflow":raise CommandError("schema_mismatch","mode","Active-task context discovery is workflow-only.")
  td,task=active_task(repo,a.active_task)
  if a.recovery_continuation_id:check_recovery(package_root,repo,td,task,v,a.recovery_continuation_id)
 actual=v["result_identity"]["result_sha256"]
 if a.expected_result_sha256 and a.expected_result_sha256!=actual:raise CommandError("stale_identity","expected_result_sha256","Use current result digest.",3)
 return {"status":"passed","typed_exit":v["typed_exit"],"result_sha256":actual,"query_sha256":v["result_identity"]["query_sha256"],"archive_manifest_sha256":v["result_identity"]["archive_manifest_sha256"],"base_head":v["result_identity"]["base_head"],"base_sync_facts_sha256":v["result_identity"]["base_sync_facts_sha256"],"post_sync_resolution_sha256":v["result_identity"]["post_sync_resolution_sha256"]}
