from __future__ import annotations
import argparse,json,sys,shutil,subprocess
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json
def load(root,pkg,value,field):
 p=Path(value); src=next((x for x in ([p] if p.is_absolute() else [root/p,pkg/p]) if x.is_file() and not x.is_symlink()),None)
 if src is None: raise CommandError("invalid_json",field,"Provide one regular JSON file.")
 try:v=json.loads(src.read_text())
 except json.JSONDecodeError as exc: raise CommandError("invalid_json",field,"Provide valid JSON.") from exc
 if not isinstance(v,dict): raise CommandError("invalid_json",field,"Provide one object.")
 return v

def git(root,*args,check=True):
 proc=subprocess.run(["git",*args],cwd=root,text=True,capture_output=True)
 if check and proc.returncode: raise CommandError("stale_identity","owned_resources",proc.stderr.strip() or "Refresh the reviewed task resources.",3)
 return proc

def registered_worktrees(root):
 rows={}; current={}
 for line in git(root,"worktree","list","--porcelain").stdout.splitlines()+[""]:
  if not line:
   if "worktree" in current: rows[str(Path(current["worktree"]).resolve())]=current
   current={}; continue
  key,_,value=line.partition(" "); current[key]=value
 return rows

def validate_runtime_resource(root,path,public,receipt_path):
 runtime_root=(root/".trellis/.runtime/guru-team").resolve()
 if not str(path).startswith(str(runtime_root)+"/"): raise CommandError("stale_identity","owned_resources","Runtime cleanup is outside the task runtime root.",3)
 if path==receipt_path.resolve(): return
 if not path.is_file() or path.is_symlink(): raise CommandError("stale_identity","owned_resources","Cleanup accepts only current task-bound runtime files.",3)
 try:value=json.loads(path.read_text())
 except (OSError,json.JSONDecodeError) as exc: raise CommandError("stale_identity","owned_resources","Runtime resource is not current task-bound JSON.",3) from exc
 if not isinstance(value,dict) or public["task_ref"] not in {value.get("task_ref"),value.get("task_artifact_dir")}:
  raise CommandError("stale_identity","owned_resources","Runtime resource does not belong to the current task.",3)

def validate_resources(root,public,resources,receipt,receipt_path):
 worktree_rows=registered_worktrees(root); head_ref="refs/heads/"+receipt["head_branch"]
 seen=set()
 for item in resources:
  identity=(item["kind"],item["locator"])
  if identity in seen: raise CommandError("stale_identity","owned_resources","Cleanup resources must be unique.",3)
  seen.add(identity); kind,locator=identity
  if kind=="branch":
   if locator!=receipt["head_branch"] or locator in {receipt["base_branch"],"main","master"} or locator.startswith("refs/"):
    raise CommandError("stale_identity","owned_resources","Branch cleanup must target the exact Finish head branch.",3)
   branch=git(root,"show-ref","--verify","--quiet",head_ref,check=False)
   if branch.returncode==0 and git(root,"merge-base","--is-ancestor",head_ref,f"refs/remotes/origin/{receipt['base_branch']}",check=False).returncode:
    raise CommandError("stale_identity","owned_resources","Finish head branch is not contained in the verified target baseline.",3)
  elif kind=="worktree":
   path=Path(locator)
   if not path.is_absolute(): raise CommandError("stale_identity","owned_resources","Worktree cleanup requires one exact absolute path.",3)
   resolved=path.resolve()
   if resolved==root: raise CommandError("stale_identity","owned_resources","Cleanup cannot remove the checkout executing the command.",3)
   row=worktree_rows.get(str(resolved))
   if row is None or row.get("branch")!=head_ref: raise CommandError("stale_identity","owned_resources","Worktree is not registered to the exact Finish head branch.",3)
   if git(resolved,"status","--porcelain=v1","--untracked-files=all").stdout:
    raise CommandError("stale_identity","owned_resources","Finish worktree is not clean and cannot be removed.",3)
  else:
   validate_runtime_resource(root,(root/locator).resolve(),public,receipt_path)
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False); p.add_argument("--root"); p.add_argument("--input",required=True); p.add_argument("--semantic-result",required=True); p.add_argument("--confirmed-cleanup",action="store_true")
 try:a=p.parse_args(argv)
 except SystemExit as exc: raise CommandError("invalid_arguments","arguments","Use the cleanup command contract.") from exc
 root=Path(a.root or ".").resolve(); public=load(root,package_root,a.input,"input"); semantic=load(root,package_root,a.semantic_result,"semantic_result")
 validate_json(public,package_root/"schemas/public-input.schema.json","input"); validate_json(semantic,package_root/"schemas/semantic-result.schema.json","semantic_result")
 if public["profile"]!=semantic["profile"] or public["mode"]!=semantic["mode"]: raise CommandError("stale_identity","semantic_result","Cleanup identity differs from Finish.",3)
 route=semantic["route"]
 receipt_suffix=public["finish_ref"].rsplit(":",1)[-1]
 receipt=root/".trellis/.runtime/guru-team/finish"/(receipt_suffix+".json")
 if route["typed_exit"]=="cleaned":
  if not receipt.is_file() or receipt.is_symlink(): raise CommandError("stale_identity","finish_ref","Current Finish success receipt is missing or stale.",3)
 receipt_value=json.loads(receipt.read_text())
 validate_json(receipt_value,package_root.parent/"guru-finish-task/schemas/finish-transaction.schema.json","finish_receipt")
 if receipt_value.get("stage")!="success" or receipt_value.get("task_ref")!=public["task_ref"] or receipt_value.get("finish_ref")!=public["finish_ref"]: raise CommandError("stale_identity","finish_ref","Finish receipt is not the current terminal transaction for this cleanup call.",3)
 resources=semantic["owned_resources"]
 if public.get("resources") is not None and public["resources"]!=resources: raise CommandError("stale_identity","owned_resources","Cleanup resource discovery changed after review.",3)
 if route["typed_exit"]=="cleaned": validate_resources(root,public,resources,receipt_value,receipt)
 if route["typed_exit"]=="cleaned" and not a.confirmed_cleanup: return {"exit_id":"remaining_resources","task_ref":public["task_ref"],"finish_ref":public["finish_ref"],"remaining":[x["locator"] for x in resources]}
 if route["typed_exit"]=="cleaned":
  remaining=[]
  for item in sorted(resources,key=lambda value:{"worktree":0,"branch":1,"runtime":2}[value["kind"]]):
   kind,locator=item["kind"],item["locator"]
   if kind=="runtime":
    path=(root/locator).resolve()
    if path.exists() and path!=receipt.resolve(): path.unlink()
   elif kind=="worktree":
    path=Path(locator).resolve()
    if path.exists():
     proc=subprocess.run(["git","worktree","remove",str(path)],cwd=root,text=True,capture_output=True)
     if proc.returncode!=0: remaining.append(locator)
   elif kind=="branch":
    proc=subprocess.run(["git","branch","-d",locator],cwd=root,text=True,capture_output=True)
    if proc.returncode!=0 and "not found" not in proc.stderr.lower(): remaining.append(locator)
  if remaining: return {"exit_id":"remaining_resources","task_ref":public["task_ref"],"finish_ref":public["finish_ref"],"remaining":remaining}
  receipt.unlink(missing_ok=True)
 out={"exit_id":route["typed_exit"],"task_ref":public["task_ref"],"finish_ref":public["finish_ref"]}
 if route["typed_exit"]!="cleaned": out.update({"reason_code":route["reason_code"],"remediation":route["remediation"]})
 validate_json(out,package_root/"schemas/public-output.schema.json","stdout"); return out
if __name__=="__main__":
 try:print(json.dumps(run(Path(__file__).parents[1],{},sys.argv[1:]),ensure_ascii=False))
 except CommandError as exc: print(json.dumps({"code":exc.code,"field_path":exc.field_path,"remediation":exc.remediation},ensure_ascii=False),file=sys.stderr); raise SystemExit(exc.exit_status)
