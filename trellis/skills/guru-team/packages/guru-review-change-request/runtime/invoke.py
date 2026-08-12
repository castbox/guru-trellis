from __future__ import annotations
import argparse
from pathlib import Path
from common import digest,load,parse,root,validate_owner
from runtime.io import CommandError
from runtime.schema import validate_json
def public_target(target):
 keys={"kind","repo","title_sha256","body_sha256","identity_sha256","content_sha256"}
 keys|={"issue_number","url","updated_at"} if target["kind"]=="existing_issue" else ({"draft_id","source_request_sha256"} if target["kind"]=="proposed_draft" else {"caller_locator","request_id","source_request_sha256"})
 return {key:target[key] for key in keys}
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--invocation",required=True);a=parse(p,argv);repo=root(package_root,a.root);e=load(repo,package_root,a.invocation,"invocation");public=e.get("public_input");owner=e.get("owner_result");up=e.get("transition")
 if not isinstance(public,dict) or not isinstance(owner,dict):raise CommandError("invalid_arguments","invocation","Provide public input and owner result.")
 validate_owner(package_root,owner,"owner_result");exit_id=owner["typed_exit"]
 if exit_id=="blocked":out={"exit_id":"blocked"};schema="public-blocked-output.schema.json"
 elif exit_id=="refresh_context":
  base=(up or {}).get("base",{});out={"exit_id":exit_id,"handoff_mode":owner["mode"],"handoff_repo_root":(up or {}).get("repo_locator","."),"handoff_route":"repo_change"};
  if base.get("selected_base"):out["handoff_base_branch"]=base["selected_base"]
  schema="public-refresh-context-output.schema.json"
 elif exit_id in {"clarify_requirements","review_wording"}:
  required_stage="context_current" if exit_id=="clarify_requirements" else "clarity_current"
  if not isinstance(up,dict) or up.get("stage")!=required_stage:raise CommandError("stale_identity","transition",f"Provide current {required_stage} transition.",3)
  out={"exit_id":exit_id,"handoff_profile":"initial_change_request" if exit_id=="clarify_requirements" else "change_request","handoff_mode":owner["mode"],"handoff_target_locator":up["target_locator"],"handoff_continuation_id":public["continuation_id"],"transition":up};schema=f"public-{exit_id.replace('_','-')}-output.schema.json"
 else:
  if not isinstance(up,dict) or up.get("stage")!="wording_current":raise CommandError("stale_identity","transition","Provide the current wording transition.",3)
  prereq=owner["prerequisites"];scope=owner["semantic_review"]["scope_conclusion"]
  readiness={"payload_sha256":digest(owner),"facts_sha256":owner["facts_sha256"],"content_sha256":owner["target"]["content_sha256"],"linkage_sha256":owner["evidence_linkage"]["linkage_sha256"]}
  current=dict(up);current.pop("context_result_sha256",None);current.update({"transition_id":"readiness_current:"+owner["facts_sha256"][:24],"stage":"readiness_current","readiness_facts_sha256":owner["facts_sha256"],"readiness_linkage_sha256":owner["evidence_linkage"]["linkage_sha256"],"target_content_sha256":owner["target"]["content_sha256"],"readiness":readiness,"target":public_target(owner["target"]),"scope":{k:scope[k] for k in ("close_issues","related_issues","followup_issues")}})
  out={"exit_id":"ready","profile":"execute_reviewed_plan","mode":owner["mode"],"transition":current};schema="public-ready-output-3.0.schema.json"
 validate_json(out,package_root/"schemas"/schema,"stdout");return out
