from __future__ import annotations
import argparse,hashlib,json,os,subprocess
from pathlib import Path
from common import CONSUMERS,digest,finalize,git,load,now,parse,root,snapshot,stage,validate_plan
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
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--input");p.add_argument("--invocation");a=parse(p,argv);repo=root(package_root,a.root);e=load(repo,package_root,a.invocation,"invocation") if a.invocation else None;plan=e.get("plan") if isinstance(e,dict) else load(repo,package_root,a.input,"input");validate_plan(package_root,repo,plan);gate=plan["ai_review_gate"]["status"]
 if gate!="passed":
  before=snapshot(repo,plan);exit_id="refresh_review" if gate=="reroute" else "blocked";result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":now(),"mode":plan["mode"],"variant":"no_side_effect","plan_sha256":plan["freshness"]["plan_sha256"],"executor":stage("blocked",["The semantic gate did not authorize mutation."]),"checker":stage("not_run",[]),"created_issue":None,"created_workspace":None,"no_side_effect":{"reason_code":"target_changed" if exit_id=="refresh_review" else "execution_blocked","before":before,"after":snapshot(repo,plan),"zero_writes":True},"typed_exit":exit_id,"reason":"The reviewed plan requires refresh or is blocked.","consumer":CONSUMERS[exit_id],"facts_sha256":""};return finalize(package_root,result)
 if plan["target"]["kind"]=="reviewed_draft":
  created=create_issue(plan);result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":now(),"mode":plan["mode"],"variant":"created_issue","plan_sha256":plan["freshness"]["plan_sha256"],"executor":stage("passed",["Created and immediately reread the exact reviewed GitHub issue."]),"checker":stage("not_run",[]),"created_issue":created,"created_workspace":None,"no_side_effect":None,"typed_exit":"refresh_review","reason":"The reviewed issue was created and now requires a complete Intake refresh.","consumer":CONSUMERS["refresh_review"],"facts_sha256":""};return finalize(package_root,result)
 n=plan["naming"];workspace=repo.parent/n["workspace_slug"];branch=n["branch_name"]
 if workspace.exists():raise CommandError("stale_identity","naming.workspace_slug","Reviewed workspace path already exists.",3)
 if git(repo,"show-ref","--verify","--quiet",f"refs/heads/{branch}",check=False).returncode==0:raise CommandError("stale_identity","naming.branch_name","Reviewed branch already exists.",3)
 git(repo,"worktree","add","-b",branch,str(workspace),plan["base"]["base_ref"])
 artifact_rel=Path(plan["side_effects"]["task_artifacts"][0]);task_dir=workspace/artifact_rel.parent;task_dir.mkdir(parents=True,exist_ok=True)
 task={"id":n["task_slug"],"name":n["task_slug"],"title":n["task_title"],"status":"planning","branch":branch,"base_branch":plan["base"]["selected_base"],"creator":plan["assignee"]["login"],"assignee":plan["assignee"]["login"],"scope":f"GitHub issue: {plan['target']['url']}"};(task_dir/"task.json").write_text(json.dumps(task,ensure_ascii=False,indent=2)+"\n")
 def entry(x):return {k:x[k] for k in ("number","url","title","reason")}
 s=plan["scope"];ledger={"schema_version":"2.0","primary_issue":entry(s["primary"]),"close_issues":[entry(x) for x in s["close"]],"related_issues":[entry(x) for x in s["related"]],"followup_issues":[entry(x) for x in s["followup"]]};ledger_path=workspace/artifact_rel;ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,sort_keys=True,indent=2)+"\n");os.chmod(ledger_path,0o644)
 mappings=[]
 for rel in plan["side_effects"]["runtime_mappings"]:
  q=repo/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps({"workspace_slug":n["workspace_slug"],"branch_name":branch,"task_slug":n["task_slug"],"task_dir":artifact_rel.parent.as_posix(),"workspace_path":str(workspace.resolve())})+"\n");mappings.append({"path":rel,"ignored":True})
 data=ledger_path.read_bytes();artifact={"path":artifact_rel.as_posix(),"sha256":__import__('hashlib').sha256(data).hexdigest(),"size":len(data),"mode":"100644","tracked":True};created={"repo":plan["target"]["repo"],"issue_number":plan["target"]["issue_number"],"branch_name":branch,"base_ref":plan["base"]["base_ref"],"base_head":plan["base"]["decision_head"],"workspace_slug":n["workspace_slug"],"task_slug":n["task_slug"],"task_artifact_dir":artifact_rel.parent.as_posix(),"assignee":plan["assignee"]["login"],"task_status":"planning","artifacts":[artifact],"runtime_mappings":mappings,"workspace_boundary_match":True,"source_developer_identity_created":False,"target_developer_identity_created":False,"workspace_journal_created":False}
 result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":now(),"mode":plan["mode"],"variant":"created_workspace","plan_sha256":plan["freshness"]["plan_sha256"],"executor":stage("passed",["Created the exact reviewed branch, worktree, task, ledger, and runtime mappings."]),"checker":stage("not_run",[]),"created_issue":None,"created_workspace":created,"no_side_effect":None,"typed_exit":"created","reason":"The reviewed task workspace was created.","consumer":CONSUMERS["created"],"facts_sha256":""};return finalize(package_root,result)
