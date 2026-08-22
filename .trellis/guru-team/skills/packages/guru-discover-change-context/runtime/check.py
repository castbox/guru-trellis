from __future__ import annotations
import argparse,json
from pathlib import Path
from common import active_task,check_owner_binding,check_recovery,load,parse,preview,root,validate
from runtime.io import CommandError
def run(package_root:Path,command:dict,argv:list[str])->dict:
 if command["id"]=="preview-change-context-history":
  p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--query-json");p.add_argument("--limit",type=int,default=20);a=parse(p,argv);repo=root(package_root,a.root)
  try:q=json.loads(a.query_json) if a.query_json else {}
  except Exception as exc:raise CommandError("invalid_json","query_json","Provide one query object.") from exc
  if not 1<=a.limit<=100:raise CommandError("invalid_arguments","limit","Use 1 through 100.")
  return preview(repo,q,a.limit)
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--input",required=True);p.add_argument("--public-input",required=True);p.add_argument("--transition",required=True);p.add_argument("--expected-result-sha256");p.add_argument("--active-task");p.add_argument("--recovery-continuation-id");a=parse(p,argv);repo=root(package_root,a.root);public=load(repo,package_root,a.public_input,"public_input");transition=load(repo,package_root,a.transition,"transition")
 try:v=validate(package_root,load(repo,package_root,a.input,"input"));observation=check_owner_binding(package_root,repo,public,transition,v)
 except CommandError as exc:return {"status":"passed","typed_exit":"blocked","reason":exc.code}
 if observation["classification"]!="current":return {"status":"passed","typed_exit":"refresh_base" if observation["classification"]=="refresh_base" else "blocked","reason":observation["reason"]}
 if a.recovery_continuation_id and not a.active_task:raise CommandError("invalid_arguments","recovery_continuation_id","Provide active-task identity for recovery.")
 if a.active_task:
  if v["mode"]!="workflow":raise CommandError("schema_mismatch","mode","Active-task context discovery is workflow-only.")
  td,task=active_task(repo,a.active_task)
  if a.recovery_continuation_id:check_recovery(package_root,repo,td,task,v,a.recovery_continuation_id)
 actual=v["result_identity"]["result_sha256"]
 if a.expected_result_sha256 and a.expected_result_sha256!=actual:raise CommandError("stale_identity","expected_result_sha256","Use current result digest.",3)
 return {"status":"passed","typed_exit":v["typed_exit"],"result_sha256":actual,"query_sha256":v["result_identity"]["query_sha256"],"archive_manifest_sha256":v["result_identity"]["archive_manifest_sha256"],"base_head":v["result_identity"]["base_head"]}
