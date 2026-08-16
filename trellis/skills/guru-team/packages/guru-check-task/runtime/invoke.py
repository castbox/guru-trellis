from __future__ import annotations
import argparse
from pathlib import Path
from common import checkpoint,load,parse,root,task
from runtime.io import CommandError
from runtime.schema import validate_json
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--invocation");p.add_argument("--input");p.add_argument("--owner-result")
 a=parse(p,argv);repo=root(package_root,a.root)
 if a.invocation:
  envelope=load(repo,package_root,a.invocation,"invocation");public=envelope.get("public_input");owner=envelope.get("owner_result")
 else:public=load(repo,package_root,a.input,"input");owner=load(repo,package_root,a.owner_result,"owner_result")
 if not isinstance(public,dict) or not isinstance(owner,dict):raise CommandError("invalid_arguments","invocation","Provide public input and checked owner result.")
 validate_json(owner,package_root/"schemas/phase2-check.schema.json","owner_result")
 if owner["task_ref"]!=public.get("task_ref") or owner["mode"]!=public.get("mode"):raise CommandError("stale_identity","owner_result","Rerun Phase 2 for the exact public input.",3)
 exit_id=owner["typed_exit"];out={"exit_id":exit_id}
 if exit_id in {"passed","implementation_required","planning_stale"}:out["task_ref"]=owner["task_ref"]
 if exit_id=="passed":out["phase2_commit_anchor"]=owner["phase2_capture_commit"]
 elif exit_id=="implementation_required":out["finding_refs"]=[x["id"] for x in owner["semantic_review"]["findings"] if x.get("status")=="open"]
 elif exit_id=="planning_stale":out.update({"planning_route":owner["route"],"proposal_refs":[x["id"] for x in owner["semantic_review"]["scope_decisions"] if x.get("disposition")=="scope_change_required"]})
 names={"passed":"public-passed-output.schema.json","implementation_required":"public-implementation-required-output.schema.json","planning_stale":"public-planning-stale-output.schema.json","blocked":"public-blocked-output.schema.json"}
 if exit_id not in names:raise CommandError("schema_mismatch","typed_exit","Return one declared typed exit.")
 validate_json(out,package_root/"schemas"/names[exit_id],"stdout")
 if exit_id!="passed":checkpoint(repo,task(repo,owner["task_ref"]),"phase2-check.json").unlink(missing_ok=True)
 return out
