from __future__ import annotations
import argparse,copy,hashlib,json,os,subprocess
from pathlib import Path
from common import digest,finalize,git,load,parse,root,stage,validate,validate_plan
from runtime.io import CommandError
def github(repo,number):
 p=subprocess.run(["gh","issue","view",str(number),"--repo",repo,"--json","number,url,state,title,body,updatedAt,labels"],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise CommandError("stale_identity","created_issue",p.stderr.strip() or "Reread the created issue.",3)
 try:return json.loads(p.stdout)
 except Exception as exc:raise CommandError("invalid_json","created_issue","GitHub returned invalid JSON.") from exc
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--input");p.add_argument("--plan-input");p.add_argument("--invocation");a=parse(p,argv);repo=root(package_root,a.root)
 if a.invocation:e=load(repo,package_root,a.invocation,"invocation");plan=e.get("plan");result=e.get("result")
 else:plan=load(repo,package_root,a.plan_input,"plan_input");result=load(repo,package_root,a.input,"input")
 validate_plan(package_root,repo,plan);validate(package_root,result,"task-workspace-result.schema.json","result")
 unsigned=copy.deepcopy(result);actual=unsigned.pop("facts_sha256");
 if digest(unsigned)!=actual or result["plan_sha256"]!=plan["freshness"]["plan_sha256"]:raise CommandError("stale_identity","result","Rerun the exact workspace executor.",3)
 if result["variant"]=="created_workspace":
  c=result["created_workspace"];workspace=repo.parent/c["workspace_slug"]
  if not workspace.is_dir() or git(workspace,"rev-parse","--abbrev-ref","HEAD").stdout.strip()!=c["branch_name"]:raise CommandError("stale_identity","created_workspace","Workspace identity drifted.",3)
  task=workspace/c["task_artifact_dir"]/"task.json";ledger=workspace/c["artifacts"][0]["path"]
  if not task.is_file() or not ledger.is_file():raise CommandError("stale_identity","created_workspace.artifacts","Task artifacts are missing.",3)
  data=ledger.read_bytes();row=c["artifacts"][0]
  if hashlib.sha256(data).hexdigest()!=row["sha256"] or len(data)!=row["size"] or oct(os.stat(ledger).st_mode&0o777)!="0o644":raise CommandError("stale_identity","created_workspace.artifacts","Ledger bytes or mode drifted.",3)
  for row in c["runtime_mappings"]:
   if not (repo/row["path"]).is_file():raise CommandError("stale_identity","created_workspace.runtime_mappings","Runtime mapping is missing.",3)
 if result["variant"]=="created_issue":
  c=result["created_issue"];live=github(c["repo"],c["number"])
  if live.get("url")!=c["canonical_url"] or str(live.get("state") or "").lower()!="open" or hashlib.sha256(str(live.get("title") or "").encode()).hexdigest()!=c["title_sha256"] or hashlib.sha256(str(live.get("body") or "").encode()).hexdigest()!=c["body_sha256"]:raise CommandError("stale_identity","created_issue","Created issue identity drifted; refresh Intake.",3)
 checked=copy.deepcopy(result);checked["checker"]=stage("passed",["Validated plan identity, typed consumer, live workspace, task artifacts, and runtime mappings."]);return finalize(package_root,checked)
