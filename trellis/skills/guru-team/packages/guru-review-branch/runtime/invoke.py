from __future__ import annotations
import argparse
from pathlib import Path
from common import load,parse,root,validate_gate
from runtime.io import CommandError
from runtime.schema import validate_json
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--invocation",required=True);a=parse(p,argv);repo=root(package_root,a.root);e=load(repo,package_root,a.invocation,"invocation");owner=e.get("owner_result")
 if not isinstance(owner,dict):raise CommandError("invalid_arguments","owner_result","Provide checked owner result.")
 validate_gate(package_root,repo,owner);x=owner["typed_exit"]
 if x=="passed":out={"exit_id":x,"task_ref":owner["task_dir"],"branch_review_commit":owner["review_commit"]};schema="public-passed-output.schema.json"
 elif x=="continuity_passed":
  pair=owner["integration_pair"];out={"exit_id":x,"task_ref":owner["task_dir"],"branch_review_commit":owner["review_commit"],**{k:pair[k] for k in ("task_head","old_base_head","new_base_head","candidate_tree_sha256","resume_target")}};schema="public-continuity-passed-output.schema.json"
 elif x=="implementation_required":out={"exit_id":x,"task_ref":owner["task_dir"],"branch_review_commit":owner["review_commit"],"finding_refs":[f["finding_ref"] for f in owner["semantic_review"]["qualified_findings"] if f["status"]=="open"]};schema="public-implementation-required-output.schema.json"
 elif x=="scope_confirmation_required":out={"exit_id":x,"task_ref":owner["task_dir"],"proposal_refs":[p["proposal_ref"] for p in owner["semantic_review"]["scope_proposals"]]};schema="public-scope-confirmation-required-output.schema.json"
 else:out={"exit_id":"blocked"};schema="public-blocked-output.schema.json"
 validate_json(out,package_root/"schemas"/schema,"stdout");return out
