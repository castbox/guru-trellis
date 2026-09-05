from __future__ import annotations
import argparse,hashlib
from pathlib import Path
from common import canonical_candidate_locator,commit_result_path,git,load,parse,root
from execute import _raw_commit_message,recover_published_happy_path_commit,run as execute_commit
from runtime.io import CommandError
from runtime.schema import validate_json
def _project(package_root:Path,e:dict,result:dict)->dict:
 exit_id=result.get("typed_exit") or result.get("exit")
 if exit_id=="committed":
  task_ref=result.get("task_ref") or e.get("task_ref");base_ref=result.get("base_ref") or e.get("base_ref");commit=result.get("branch_review_commit") or result.get("commit_sha")
  if not all(isinstance(x,str) and x for x in (task_ref,base_ref,commit)):raise CommandError("invalid_arguments","invocation.result","Provide committed task, base, and commit identity.")
  out={"exit_id":"committed","task_ref":task_ref,"base_ref":base_ref,"branch_review_commit":commit};schema="public-committed-output.schema.json"
 elif exit_id=="revision-required":out={"exit_id":exit_id,"task_ref":result["task_ref"]};schema="public-revision-required-output.schema.json"
 else:out={"exit_id":"blocked"};schema="public-blocked-output.schema.json"
 validate_json(out,package_root/"schemas"/schema,"stdout");return out
def _recover_receipt(package_root:Path,repo:Path,candidate_locator:str)->dict:
 candidate_path,_relative,task_key,sequence=canonical_candidate_locator(repo,candidate_locator);target=commit_result_path(repo,task_key,sequence)
 if not target.is_file() or target.is_symlink():raise CommandError("unsafe_path","candidate_artifact","Use a current prepared candidate or its package-owned recovery receipt.")
 receipt=load(repo,package_root,target,"happy_path_result");validate_json(receipt,package_root/"schemas/happy-path-result.schema.json","happy_path_result")
 if receipt["candidate_artifact"]!=candidate_locator:raise CommandError("stale_identity","candidate_artifact","Retry the exact prepared candidate locator.",3)
 if git(repo,"symbolic-ref","HEAD").stdout.strip()!=receipt["branch_ref"] or git(repo,"rev-parse","HEAD").stdout.strip()!=receipt["commit_sha"]:raise CommandError("stale_identity","happy_path_result","The recovered branch identity changed; rerun the owning workflow from live facts.",3)
 parents=git(repo,"show","-s","--format=%P",receipt["commit_sha"]).stdout.strip().split();tree=git(repo,"show","-s","--format=%T",receipt["commit_sha"]).stdout.strip();message_sha=hashlib.sha256(_raw_commit_message(repo,receipt["commit_sha"]).encode()).hexdigest()
 if parents!=[receipt["pre_commit_head"]] or tree!=receipt["commit_tree"] or message_sha!=receipt["message_sha256"]:raise CommandError("stale_identity","happy_path_result","The recovered commit no longer matches the completed transaction.",3)
 if candidate_path.is_file():
  candidate=load(repo,package_root,candidate_path,"candidate_artifact");recover_published_happy_path_commit(package_root,repo,candidate_locator,candidate,receipt)
 return _project(package_root,receipt,{"exit":"committed","commit_sha":receipt["commit_sha"]})
def _run_happy_path(package_root:Path,root_value:str|None,candidate_artifact:str)->dict:
 repo=root(package_root,root_value);path,relative,_task_key,_sequence=canonical_candidate_locator(repo,candidate_artifact);locator=f".trellis/.runtime/guru-team/task-commit-plans/{relative}"
 if not path.is_file():return _recover_receipt(package_root,repo,locator)
 candidate=load(repo,package_root,path,"candidate_artifact");_unused,_relative,task_key,sequence=canonical_candidate_locator(repo,locator);receipt_path=commit_result_path(repo,task_key,sequence)
 if receipt_path.is_file() and not receipt_path.is_symlink():
  try:
   receipt=load(repo,package_root,receipt_path,"happy_path_result");validate_json(receipt,package_root/"schemas/happy-path-result.schema.json","happy_path_result")
  except CommandError:
   if git(repo,"rev-parse","HEAD").stdout.strip()!=candidate["git"]["pre_commit_head"]:raise
  else:
   if git(repo,"symbolic-ref","HEAD").stdout.strip()==receipt["branch_ref"] and git(repo,"rev-parse","HEAD").stdout.strip()==receipt["commit_sha"]:return _recover_receipt(package_root,repo,locator)
 result=execute_commit(package_root,{"_happy_path_candidate_locator":locator},["--root",str(repo),"--candidate-artifact",str(path)])
 if result.get("exit")!="committed":return _project(package_root,{"task_ref":candidate["task"]["path"],"base_ref":candidate["git"]["base_ref"]},result)
 return _recover_receipt(package_root,repo,locator)
def _run_compatibility_projection(package_root:Path,root_value:str|None,invocation:str)->dict:
 repo=root(package_root,root_value);e=load(repo,package_root,invocation,"invocation");result=e.get("result")
 if not isinstance(result,dict):raise CommandError("invalid_arguments","invocation.result","Provide executor result.")
 return _project(package_root,e,result)
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--candidate-artifact");p.add_argument("--invocation");a=parse(p,argv)
 if a.candidate_artifact and a.invocation:raise CommandError("conflicting_arguments","arguments","Use --candidate-artifact for the Happy Path or --invocation for compatibility, not both.")
 if a.candidate_artifact:return _run_happy_path(package_root,a.root,a.candidate_artifact)
 if a.invocation:return _run_compatibility_projection(package_root,a.root,a.invocation)
 raise CommandError("invalid_arguments","arguments","Provide --candidate-artifact for the Happy Path or --invocation for compatibility.")
