from __future__ import annotations
import argparse
from pathlib import Path
from common import active_task,identity,load,parse,preview,record_recovery,root,validate
from runtime.io import CommandError
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--mode",required=True,choices=("workflow","standalone"));p.add_argument("--input",required=True);p.add_argument("--expected-result-sha256");p.add_argument("--active-task");p.add_argument("--recovery-continuation-id");a=parse(p,argv);repo=root(package_root,a.root);v=load(repo,package_root,a.input,"input")
 if v.get("mode")!=a.mode:raise CommandError("schema_mismatch","mode","Match owner result mode.")
 v["canonical_query"]=__import__("common").canonical_query(v["change_input"]);v["history_preview"]=preview(repo,v["change_input"],v.get("history_preview",{}).get("limit",20));v["result_identity"]=identity(v);validate(package_root,v)
 if a.recovery_continuation_id and not a.active_task:raise CommandError("invalid_arguments","recovery_continuation_id","Provide active-task identity for recovery.")
 if a.active_task:
  if a.mode!="workflow":raise CommandError("schema_mismatch","mode","Active-task context discovery is workflow-only.")
  td,task=active_task(repo,a.active_task)
  if a.recovery_continuation_id:record_recovery(package_root,repo,td,task,v,a.recovery_continuation_id)
 if a.expected_result_sha256 and a.expected_result_sha256!=v["result_identity"]["result_sha256"]:raise CommandError("stale_identity","expected_result_sha256","Use current result digest.",3)
 return v
