from __future__ import annotations
import argparse,hashlib,json,os,subprocess
from pathlib import Path
from common import CONSUMERS,digest,finalize,git,load,now,parse,require_directory_ancestors,resolve_workspace,root,snapshot,stage,validate_plan,worktrees
from runtime.io import CommandError
def github(repo,*args):
 p=subprocess.run(["gh",*args,"--repo",repo],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise CommandError("stale_identity","target",p.stderr.strip() or "Repair GitHub access and refresh the reviewed target.",3)
 try:return json.loads(p.stdout)
 except Exception as exc:raise CommandError("invalid_json","target","GitHub returned invalid JSON.") from exc
def create_issue(plan):
 t=plan["target"];d=t["draft"];args=["issue","create","--title",d["title"],"--body",d["body"]]
 for label in d["labels"]:args.extend(["--label",label])
 created=github(t["repo"],*args);url=created.get("url") if isinstance(created,dict) else None
 if not url:raise CommandError("stale_identity","target","GitHub did not return the created issue URL.",3)
 live=github(t["repo"],"issue","view",str(url),"--json","number,url,state,title,body,updatedAt,labels")
 labels=sorted(x.get("name") for x in live.get("labels",[]) if isinstance(x,dict) and x.get("name"))
 binding={"repo":t["repo"],"number":live.get("number"),"canonical_url":live.get("url"),"state":str(live.get("state") or "").lower(),"title_sha256":hashlib.sha256(str(live.get("title") or "").encode()).hexdigest(),"body_sha256":hashlib.sha256(str(live.get("body") or "").encode()).hexdigest(),"updated_at":live.get("updatedAt"),"reviewed_draft_id":d["draft_id"],"reviewed_draft_sha256":d["reviewed_draft_sha256"]}
 if binding["state"]!="open" or binding["title_sha256"]!=t["title_sha256"] or binding["body_sha256"]!=t["body_sha256"] or labels!=sorted(d["labels"]) or not isinstance(binding["number"],int):raise CommandError("stale_identity","target","Created issue does not match the exact reviewed draft.",3)
 binding["facts_sha256"]=digest(binding);return binding
def workspace_payloads(plan,artifact_rel):
 n=plan["naming"]
 task={"id":n["task_slug"],"name":n["task_slug"],"title":n["task_title"],"status":"planning","branch":n["branch_name"],"base_branch":plan["base"]["selected_base"],"creator":plan["assignee"]["login"],"assignee":plan["assignee"]["login"],"scope":f"GitHub issue: {plan['target']['url']}"}
 def entry(x):return {k:x[k] for k in ("number","url","title","reason")}
 s=plan["scope"];ledger={"schema_version":"2.0","primary_issue":entry(s["primary"]),"close_issues":[entry(x) for x in s["close"]],"related_issues":[entry(x) for x in s["related"]],"followup_issues":[entry(x) for x in s["followup"]]}
 return task,json.dumps(ledger,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
def mapping_payloads(repo,plan,workspace,artifact_rel):
 n=plan["naming"]
 workspace_mapping={"schema_version":"1.0","workspace_slug":n["workspace_slug"],"workspace_path":str(workspace),"source_checkout":str(repo),"branch_name":n["branch_name"],"updated_at":now()}
 task_mapping={"schema_version":"1.0","task_slug":n["task_slug"],"workspace_slug":n["workspace_slug"],"workspace_path":str(workspace),"task_artifact_dir":artifact_rel.parent.as_posix(),"updated_at":now()}
 return workspace_mapping,task_mapping
def expected_mapping(rel,workspace_mapping,task_mapping):
 return workspace_mapping if "/workspaces/" in rel else task_mapping
def preflight(repo,plan,workspace):
 n=plan["naming"];branch=n["branch_name"];artifact_rel=Path(plan["side_effects"]["task_artifacts"][0]);task_dir=workspace.path/artifact_rel.parent
 require_directory_ancestors(workspace.path,"worktree_root");require_directory_ancestors(task_dir,"task_artifacts")
 branch_exists=git(repo,"show-ref","--verify","--quiet",f"refs/heads/{branch}",check=False).returncode==0
 branch_exact=branch_exists and git(repo,"rev-parse",f"refs/heads/{branch}").stdout.strip()==plan["base"]["decision_head"]
 listed=worktrees(repo);row=listed.get(workspace.path);workspace_exists=workspace.path.exists()
 if workspace.mode=="current":
  current=git(repo,"branch","--show-current").stdout.strip()
  if current not in {plan["base"]["selected_base"],branch}:raise CommandError("stale_identity","workspace_mode","Current checkout is not the reviewed base or target branch.",3)
  occupied=next((path for path,value in listed.items() if path!=repo.resolve() and value.get("branch")==f"refs/heads/{branch}"),None)
  if occupied:raise CommandError("stale_identity","workspace_mode","Reviewed branch is checked out in another workspace.",3)
  exact_workspace=True
 else:
  exact_workspace=bool(row and row.get("branch")==f"refs/heads/{branch}" and workspace.path.is_dir() and branch_exact)
 task_path=task_dir/"task.json";ledger_path=workspace.path/artifact_rel;expected_task,expected_ledger=workspace_payloads(plan,artifact_rel)
 try:exact_task=task_path.is_file() and json.loads(task_path.read_text())==expected_task
 except Exception:exact_task=False
 facts={"branch":branch_exists,"workspace":workspace_exists,"exact_branch":branch_exact,"exact_workspace":exact_workspace,"task":task_path.exists(),"exact_task":exact_task}
 expected={"branch":"branch_disposition","workspace":"workspace_disposition","task":"task_disposition"}
 for key,field in expected.items():
  disposition=n[field];exists=facts[key];exact=facts[f"exact_{key}"]
  if disposition=="create_new" and exists:raise CommandError("stale_identity",f"naming.{field}",f"Reviewed {key} already exists.",3)
  if disposition=="reuse_exact" and not exact:raise CommandError("stale_identity",f"naming.{field}",f"Reviewed {key} is not an exact reusable object.",3)
  if disposition=="conflict_blocked":raise CommandError("stale_identity",f"naming.{field}",f"Reviewed {key} disposition blocks mutation.",3)
 ledger_exists=ledger_path.exists()
 ledger_exact=ledger_exists and ledger_path.is_file() and ledger_path.read_bytes()==expected_ledger.encode()
 if n["task_disposition"]=="reuse_exact" and not ledger_exact:raise CommandError("stale_identity","created_workspace.artifacts","Reusable task ledger is missing or does not match the reviewed scope.",3)
 if ledger_exists and not ledger_exact:raise CommandError("stale_identity","created_workspace.artifacts","Existing ledger conflicts with the reviewed scope.",3)
 for rel in plan["side_effects"]["runtime_mappings"]:
  workspace_mapping,task_mapping=mapping_payloads(repo,plan,workspace.path,artifact_rel);expected_mapping_value=expected_mapping(rel,workspace_mapping,task_mapping)
  for mapping_root in {repo.resolve(),workspace.path.resolve()}:
   q=mapping_root/rel
   require_directory_ancestors(q.parent,"runtime_mapping")
   if q.exists():
    try:m=json.loads(q.read_text())
    except Exception as exc:raise CommandError("stale_identity","runtime_mapping","Existing runtime mapping is invalid.",3) from exc
    if any(m.get(key)!=value for key,value in expected_mapping_value.items() if key!="updated_at"):raise CommandError("stale_identity","runtime_mapping","Existing runtime mapping conflicts with the reviewed workspace.",3)
 return artifact_rel,task_dir,expected_task,expected_ledger
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--input");p.add_argument("--invocation");a=parse(p,argv);repo=root(package_root,a.root);e=load(repo,package_root,a.invocation,"invocation") if a.invocation else None;plan=e.get("plan") if isinstance(e,dict) else load(repo,package_root,a.input,"input");validate_plan(package_root,repo,plan);gate=plan["ai_review_gate"]["status"]
 if gate!="passed":
  before=snapshot(repo,plan);exit_id="refresh_review" if gate=="reroute" else "blocked";result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":now(),"mode":plan["mode"],"variant":"no_side_effect","plan_sha256":plan["freshness"]["plan_sha256"],"executor":stage("blocked",["The semantic gate did not authorize mutation."]),"checker":stage("not_run",[]),"created_issue":None,"created_workspace":None,"no_side_effect":{"reason_code":"target_changed" if exit_id=="refresh_review" else "execution_blocked","before":before,"after":snapshot(repo,plan),"zero_writes":True},"typed_exit":exit_id,"reason":"The reviewed plan requires refresh or is blocked.","consumer":CONSUMERS[exit_id],"facts_sha256":""};return finalize(package_root,result)
 if plan["target"]["kind"]=="reviewed_draft":
  created=create_issue(plan);result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":now(),"mode":plan["mode"],"variant":"created_issue","plan_sha256":plan["freshness"]["plan_sha256"],"executor":stage("passed",["Created and immediately reread the exact reviewed GitHub issue."]),"checker":stage("not_run",[]),"created_issue":created,"created_workspace":None,"no_side_effect":None,"typed_exit":"refresh_review","reason":"The reviewed issue was created and now requires a complete Intake refresh.","consumer":CONSUMERS["refresh_review"],"facts_sha256":""};return finalize(package_root,result)
 n=plan["naming"];workspace_config=resolve_workspace(repo,n["workspace_slug"]);workspace=workspace_config.path;branch=n["branch_name"];artifact_rel,task_dir,task,ledger_bytes=preflight(repo,plan,workspace_config)
 if n["branch_disposition"]=="create_new":
  if workspace_config.mode=="current":git(repo,"switch","-c",branch,plan["base"]["base_ref"])
  else:git(repo,"worktree","add","-b",branch,str(workspace),plan["base"]["base_ref"])
 if workspace_config.mode=="current" and n["branch_disposition"]=="reuse_exact" and git(repo,"branch","--show-current").stdout.strip()!=branch:git(repo,"switch",branch)
 if n["workspace_disposition"]=="create_new" and workspace_config.mode=="worktree" and n["branch_disposition"]!="create_new":git(repo,"worktree","add",str(workspace),branch)
 task_dir.mkdir(parents=True,exist_ok=True)
 task_path=task_dir/"task.json"
 if n["task_disposition"]=="reuse_exact":
  try:existing_task=json.loads(task_path.read_text())
  except Exception as exc:raise CommandError("stale_identity","naming.task_disposition","Reusable task is invalid.",3) from exc
  if existing_task!=task:raise CommandError("stale_identity","naming.task_disposition","Reusable task does not match the reviewed task.",3)
 else:task_path.write_text(json.dumps(task,ensure_ascii=False,indent=2)+"\n")
 ledger_path=workspace/artifact_rel
 ledger_path.write_text(ledger_bytes);os.chmod(ledger_path,0o644)
 mappings=[];workspace_mapping,task_mapping=mapping_payloads(repo,plan,workspace,artifact_rel)
 for rel in plan["side_effects"]["runtime_mappings"]:
  payload=expected_mapping(rel,workspace_mapping,task_mapping)
  for mapping_root in {repo.resolve(),workspace.resolve()}:
   q=mapping_root/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(payload)+"\n")
  mappings.append({"path":rel,"ignored":True})
 data=ledger_path.read_bytes();artifact={"path":artifact_rel.as_posix(),"sha256":__import__('hashlib').sha256(data).hexdigest(),"size":len(data),"mode":"100644","tracked":True};created={"repo":plan["target"]["repo"],"issue_number":plan["target"]["issue_number"],"branch_name":branch,"base_ref":plan["base"]["base_ref"],"base_head":plan["base"]["decision_head"],"workspace_slug":n["workspace_slug"],"task_slug":n["task_slug"],"task_artifact_dir":artifact_rel.parent.as_posix(),"assignee":plan["assignee"]["login"],"task_status":"planning","artifacts":[artifact],"runtime_mappings":mappings,"workspace_boundary_match":True,"source_developer_identity_created":False,"target_developer_identity_created":False,"workspace_journal_created":False}
 result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":now(),"mode":plan["mode"],"variant":"created_workspace","plan_sha256":plan["freshness"]["plan_sha256"],"executor":stage("passed",["Created the exact reviewed branch, worktree, task, ledger, and runtime mappings."]),"checker":stage("not_run",[]),"created_issue":None,"created_workspace":created,"no_side_effect":None,"typed_exit":"created","reason":"The reviewed task workspace was created.","consumer":CONSUMERS["created"],"facts_sha256":""};return finalize(package_root,result)
