from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from common import canonical_candidate_locator,commit_result_path,git,load,parse,root
from execute import _raw_commit_message,run as execute_commit
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
def _write_receipt(package_root:Path,repo:Path,candidate_locator:str,candidate:dict,result:dict,branch_ref:str)->dict:
 commit=result["commit_sha"];receipt={"$schema":"https://github.com/castbox/guru-trellis/schemas/guru-task-commit-happy-path-result-1.0.json","schema_version":"1.0","skill_id":"guru-create-task-commit","candidate_artifact":candidate_locator,"task_ref":candidate["task"]["path"],"base_ref":candidate["git"]["base_ref"],"branch_ref":branch_ref,"pre_commit_head":candidate["git"]["pre_commit_head"],"commit_sha":commit,"commit_tree":git(repo,"show","-s","--format=%T",commit).stdout.strip(),"message_sha256":hashlib.sha256(_raw_commit_message(repo,commit).encode()).hexdigest()}
 validate_json(receipt,package_root/"schemas/happy-path-result.schema.json","happy_path_result");_path,_relative,task_key,sequence=canonical_candidate_locator(repo,candidate_locator);target=commit_result_path(repo,task_key,sequence);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n");return receipt
def _recover_receipt(package_root:Path,repo:Path,candidate_locator:str)->dict:
 _path,_relative,task_key,sequence=canonical_candidate_locator(repo,candidate_locator);target=commit_result_path(repo,task_key,sequence)
 if not target.is_file() or target.is_symlink():raise CommandError("unsafe_path","candidate_artifact","Use a current prepared candidate or its package-owned recovery receipt.")
 receipt=load(repo,package_root,target,"happy_path_result");validate_json(receipt,package_root/"schemas/happy-path-result.schema.json","happy_path_result")
 if receipt["candidate_artifact"]!=candidate_locator:raise CommandError("stale_identity","candidate_artifact","Retry the exact prepared candidate locator.",3)
 if git(repo,"symbolic-ref","HEAD").stdout.strip()!=receipt["branch_ref"] or git(repo,"rev-parse","HEAD").stdout.strip()!=receipt["commit_sha"]:raise CommandError("stale_identity","happy_path_result","The recovered branch identity changed; rerun the owning workflow from live facts.",3)
 parents=git(repo,"show","-s","--format=%P",receipt["commit_sha"]).stdout.strip().split();tree=git(repo,"show","-s","--format=%T",receipt["commit_sha"]).stdout.strip();message_sha=hashlib.sha256(_raw_commit_message(repo,receipt["commit_sha"]).encode()).hexdigest()
 if parents!=[receipt["pre_commit_head"]] or tree!=receipt["commit_tree"] or message_sha!=receipt["message_sha256"]:raise CommandError("stale_identity","happy_path_result","The recovered commit no longer matches the completed transaction.",3)
 return _project(package_root,receipt,{"exit":"committed","commit_sha":receipt["commit_sha"]})
def _run_happy_path(package_root:Path,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--candidate-artifact",required=True);a=parse(p,argv);repo=root(package_root,a.root);path,relative,_task_key,_sequence=canonical_candidate_locator(repo,a.candidate_artifact);locator=f".trellis/.runtime/guru-team/task-commit-plans/{relative}"
 if not path.is_file():return _recover_receipt(package_root,repo,locator)
 candidate=load(repo,package_root,path,"candidate_artifact");branch_ref=git(repo,"symbolic-ref","HEAD").stdout.strip();result=execute_commit(package_root,{},["--root",str(repo),"--candidate-artifact",str(path)])
 if result.get("exit")!="committed":return _project(package_root,{"task_ref":candidate["task"]["path"],"base_ref":candidate["git"]["base_ref"]},result)
 receipt=_write_receipt(package_root,repo,locator,candidate,result,branch_ref);return _project(package_root,receipt,result)
def run(package_root:Path,command:dict,argv:list[str])->dict:
 if command.get("id")=="invoke-guru-create-task-commit-happy-path-v1":return _run_happy_path(package_root,argv)
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--invocation",required=True);a=parse(p,argv);repo=root(package_root,a.root);e=load(repo,package_root,a.invocation,"invocation");result=e.get("result")
 if not isinstance(result,dict):raise CommandError("invalid_arguments","invocation.result","Provide executor result.")
 return _project(package_root,e,result)
