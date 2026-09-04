from __future__ import annotations
import argparse,copy,hashlib,json,os,subprocess
from pathlib import Path
from common import digest,finalize,git,load,parse,resolve_workspace,root,stage,validate,validate_plan,worktrees
from execute import expected_mapping,issue_record,label_identity,mapping_payloads,parse_utc_timestamp,workspace_payloads
from runtime.io import CommandError
def github(repo,number):
 p=subprocess.run(["gh","issue","view",str(number),"--repo",repo,"--json","number,url,state,title,body,updatedAt,labels"],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise CommandError("stale_identity","created_issue",p.stderr.strip() or "Reread the created issue.",3)
 try:value=json.loads(p.stdout)
 except Exception as exc:raise CommandError("invalid_json","created_issue","GitHub returned invalid JSON.") from exc
 if not isinstance(value,dict):raise CommandError("invalid_json","created_issue","GitHub issue view did not return a JSON object.")
 return value
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--input");p.add_argument("--plan-input");p.add_argument("--invocation");a=parse(p,argv);repo=root(package_root,a.root)
 if a.invocation:e=load(repo,package_root,a.invocation,"invocation");plan=e.get("plan");result=e.get("result")
 else:plan=load(repo,package_root,a.plan_input,"plan_input");result=load(repo,package_root,a.input,"input")
 validate_plan(package_root,repo,plan);validate(package_root,result,"task-workspace-result.schema.json","result")
 unsigned=copy.deepcopy(result);actual=unsigned.pop("facts_sha256");
 if digest(unsigned)!=actual or result["plan_sha256"]!=plan["freshness"]["plan_sha256"]:raise CommandError("stale_identity","result","Rerun the exact workspace executor.",3)
 if result["variant"]=="created_workspace":
  c=result["created_workspace"];resolved=resolve_workspace(repo,c["workspace_slug"]);workspace=resolved.path
  listed=worktrees(repo);row=listed.get(workspace)
  if not workspace.is_dir() or git(workspace,"rev-parse","--abbrev-ref","HEAD").stdout.strip()!=c["branch_name"] or (resolved.mode=="worktree" and (not row or row.get("branch")!=f"refs/heads/{c['branch_name']}")):raise CommandError("stale_identity","created_workspace","Workspace identity drifted.",3)
  task=workspace/c["task_artifact_dir"]/"task.json";ledger=workspace/c["artifacts"][0]["path"]
  if not task.is_file() or not ledger.is_file():raise CommandError("stale_identity","created_workspace.artifacts","Task artifacts are missing.",3)
  try:task_value=json.loads(task.read_text())
  except Exception as exc:raise CommandError("stale_identity","created_workspace.artifacts","Task identity is invalid.",3) from exc
  expected_task,_=workspace_payloads(plan,Path(c["artifacts"][0]["path"]))
  if task_value!=expected_task:raise CommandError("stale_identity","created_workspace.artifacts","Task identity drifted.",3)
  data=ledger.read_bytes();row=c["artifacts"][0]
  if hashlib.sha256(data).hexdigest()!=row["sha256"] or len(data)!=row["size"] or oct(os.stat(ledger).st_mode&0o777)!="0o644":raise CommandError("stale_identity","created_workspace.artifacts","Ledger bytes or mode drifted.",3)
  workspace_mapping,task_mapping=mapping_payloads(repo,plan,workspace,Path(c["artifacts"][0]["path"]))
  for row in c["runtime_mappings"]:
   expected=expected_mapping(row["path"],workspace_mapping,task_mapping)
   for mapping_root in {repo.resolve(),workspace.resolve()}:
    mapping_path=mapping_root/row["path"]
    if not mapping_path.is_file():raise CommandError("stale_identity","created_workspace.runtime_mappings","Runtime mapping is missing.",3)
    try:mapping=json.loads(mapping_path.read_text())
    except Exception as exc:raise CommandError("stale_identity","created_workspace.runtime_mappings","Runtime mapping is invalid.",3) from exc
    if any(mapping.get(key)!=value for key,value in expected.items() if key!="updated_at"):raise CommandError("stale_identity","created_workspace.runtime_mappings","Runtime mapping identity drifted.",3)
 if result["variant"]=="created_issue":
  c=result["created_issue"];t=plan["target"];d=t.get("draft")
  if t.get("kind")!="reviewed_draft" or not isinstance(d,dict) or c["repo"]!=t["repo"] or c["reviewed_draft_id"]!=d["draft_id"] or c["reviewed_draft_sha256"]!=d["reviewed_draft_sha256"]:raise CommandError("stale_identity","created_issue","Created issue reviewed-draft identity drifted; refresh Intake.",3)
  live=github(c["repo"],c["number"]);row=issue_record(c["repo"],live,"created_issue")
  title_sha256=hashlib.sha256(row["title"].encode()).hexdigest();body_sha256=hashlib.sha256(row["body"].encode()).hexdigest()
  if row["number"]!=c["number"] or row["url"]!=c["canonical_url"] or row["state"]!="open" or row["title"]!=d["title"] or row["body"]!=d["body"] or label_identity(row["labels"])!=label_identity(d["labels"]) or row["updated_at"]!=parse_utc_timestamp(c["updated_at"],"created_issue.updated_at") or title_sha256!=c["title_sha256"] or body_sha256!=c["body_sha256"] or title_sha256!=t["title_sha256"] or body_sha256!=t["body_sha256"]:raise CommandError("stale_identity","created_issue","Created issue identity drifted; refresh Intake.",3)
 checked=copy.deepcopy(result);checked["checker"]=stage("passed",["Validated plan identity, typed consumer, live workspace, task artifacts, and runtime mappings."]);return finalize(package_root,checked)
