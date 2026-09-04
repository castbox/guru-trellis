from __future__ import annotations
import argparse,hashlib,json,os,re,subprocess
from datetime import datetime,timedelta,timezone
from pathlib import Path
from urllib.parse import urlsplit
from common import CONSUMERS,digest,finalize,git,load,now,parse,require_directory_ancestors,resolve_workspace,root,snapshot,stage,validate_plan,worktrees
from runtime.io import CommandError
def run_gh(repo,*args):
 p=subprocess.run(["gh",*args,"--repo",repo],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise CommandError("stale_identity","target",p.stderr.strip() or "Repair GitHub access and refresh the reviewed target.",3)
 return p.stdout
def decode_github_json(stdout,field="target"):
 def reject_constant(value):raise ValueError(f"non-finite JSON number: {value}")
 try:value=json.loads(stdout,parse_constant=reject_constant)
 except Exception as exc:raise CommandError("invalid_json",field,"GitHub returned invalid JSON.") from exc
 if not isinstance(value,(dict,list)):raise CommandError("invalid_json",field,"GitHub returned invalid JSON.")
 return value
def github(repo,*args):return decode_github_json(run_gh(repo,*args))
def canonical_issue_url(repo,url,number=None,field="target"):
 try:parsed=urlsplit(url) if isinstance(url,str) else None
 except ValueError as exc:raise CommandError("stale_identity",field,"GitHub did not return a canonical issue URL for the reviewed repository.",3) from exc
 parts=parsed.path.split("/") if parsed is not None else []
 if parsed is None or url!=parsed.geturl() or parsed.scheme!="https" or parsed.netloc!="github.com" or parsed.query or parsed.fragment or len(parts)!=5 or parts[0]!="" or parts[3]!="issues" or not re.fullmatch(r"[1-9][0-9]*",parts[4]) or f"{parts[1]}/{parts[2]}".casefold()!=repo.casefold():raise CommandError("stale_identity",field,"GitHub did not return a canonical issue URL for the reviewed repository.",3)
 parsed_number=int(parts[4])
 if number is not None and (isinstance(number,bool) or not isinstance(number,int) or number!=parsed_number):raise CommandError("stale_identity",field,"GitHub issue number and canonical URL do not match.",3)
 return url,parsed_number
def decode_created_issue_url(repo,stdout):
 value=stdout
 if value.endswith("\n"):
  value=value[:-1]
  if value.endswith("\r"):value=value[:-1]
 if not value or "\n" in value or "\r" in value:raise CommandError("stale_identity","target","GitHub did not return one canonical created issue URL.",3)
 return canonical_issue_url(repo,value)
def parse_utc_timestamp(value,field):
 if not isinstance(value,str):raise CommandError("stale_identity",field,"GitHub returned an invalid UTC timestamp.",3)
 normalized=value[:-1]+"+00:00" if value.endswith("Z") else value
 try:parsed=datetime.fromisoformat(normalized)
 except ValueError as exc:raise CommandError("stale_identity",field,"GitHub returned an invalid UTC timestamp.",3) from exc
 if parsed.tzinfo is None or parsed.utcoffset()!=timedelta(0):raise CommandError("stale_identity",field,"GitHub returned an invalid UTC timestamp.",3)
 return parsed.astimezone(timezone.utc)
def issue_labels(value,field):
 if not isinstance(value,list):raise CommandError("stale_identity",field,"GitHub returned invalid issue labels.",3)
 names=[]
 for row in value:
  if not isinstance(row,dict) or not isinstance(row.get("name"),str) or not row["name"]:raise CommandError("stale_identity",field,"GitHub returned invalid issue labels.",3)
  names.append(row["name"])
 return sorted(set(names))
def label_identity(names):return sorted({name.casefold() for name in names})
def issue_record(repo,value,field,include_created_at=False):
 required={"number","url","state","title","body","updatedAt","labels"}
 if include_created_at:required.add("createdAt")
 if not isinstance(value,dict) or not required.issubset(value):raise CommandError("stale_identity",field,"GitHub returned incomplete issue fields.",3)
 number=value["number"]
 if isinstance(number,bool) or not isinstance(number,int) or number<=0:raise CommandError("stale_identity",field,"GitHub returned an invalid issue number.",3)
 url,_=canonical_issue_url(repo,value["url"],number,field)
 if not isinstance(value["state"],str) or not isinstance(value["title"],str) or not isinstance(value["body"],str):raise CommandError("stale_identity",field,"GitHub returned invalid issue fields.",3)
 record={"number":number,"url":url,"state":value["state"].lower(),"title":value["title"],"body":value["body"],"updated_at":parse_utc_timestamp(value["updatedAt"],field),"labels":issue_labels(value["labels"],field)}
 if include_created_at:record["created_at"]=parse_utc_timestamp(value["createdAt"],field)
 return record
def find_reviewed_draft_issues(plan):
 t=plan["target"];d=t["draft"];captured=parse_utc_timestamp(plan["freshness"]["captured_at"],"freshness.captured_at")
 fields="number,url,state,title,body,createdAt,updatedAt,labels"
 rows=github(t["repo"],"issue","list","--state","open","--search",f"created:>={captured.date().isoformat()}","--limit","1000","--json",fields)
 if not isinstance(rows,list):raise CommandError("invalid_json","target","GitHub issue lookup did not return a JSON array.")
 if len(rows)>=1000:raise CommandError("stale_identity","target","GitHub issue lookup did not prove complete candidate exhaustion.",3)
 expected_labels=label_identity(d["labels"]);matches=[]
 for index,value in enumerate(rows):
  row=issue_record(t["repo"],value,f"target.candidates[{index}]",include_created_at=True)
  if row["state"]=="open" and row["title"]==d["title"] and row["body"]==d["body"] and label_identity(row["labels"])==expected_labels and row["created_at"]>=captured:matches.append(row)
 return sorted(matches,key=lambda row:row["number"])
def bind_reviewed_issue(plan,locator):
 t=plan["target"];d=t["draft"]
 expected_url=None
 if isinstance(locator,str):expected_url,_=canonical_issue_url(t["repo"],locator)
 elif isinstance(locator,bool) or not isinstance(locator,int) or locator<=0:raise CommandError("stale_identity","target","GitHub issue locator is invalid.",3)
 live=github(t["repo"],"issue","view",str(locator),"--json","number,url,state,title,body,updatedAt,labels")
 if not isinstance(live,dict):raise CommandError("invalid_json","target","GitHub issue view did not return a JSON object.")
 row=issue_record(t["repo"],live,"target")
 if (expected_url is not None and row["url"]!=expected_url) or (isinstance(locator,int) and row["number"]!=locator):raise CommandError("stale_identity","target","GitHub live issue does not match the reviewed locator.",3)
 title_sha256=hashlib.sha256(row["title"].encode()).hexdigest();body_sha256=hashlib.sha256(row["body"].encode()).hexdigest()
 if row["state"]!="open" or row["title"]!=d["title"] or row["body"]!=d["body"] or title_sha256!=t["title_sha256"] or body_sha256!=t["body_sha256"] or label_identity(row["labels"])!=label_identity(d["labels"]):raise CommandError("stale_identity","target","Created or recovered issue does not match the exact reviewed draft.",3)
 binding={"repo":t["repo"],"number":row["number"],"canonical_url":row["url"],"state":row["state"],"title_sha256":title_sha256,"body_sha256":body_sha256,"updated_at":live["updatedAt"],"reviewed_draft_id":d["draft_id"],"reviewed_draft_sha256":d["reviewed_draft_sha256"]}
 binding["facts_sha256"]=digest(binding);return binding
def count_operation(operation):
 path=os.environ.get("GURU_PHASE0_OPERATION_LOG")
 if path:
  with Path(path).open("a",encoding="utf-8") as stream:stream.write(json.dumps({"adapter":"workspace","operation":operation},sort_keys=True)+"\n")
def mutation_boundary_current(repo,plan):
 count_operation("workspace.mutation_boundary_recheck")
 b=plan["base"];remote=b["remote"];selected=b["selected_base"]
 fetched=git(repo,"fetch","--no-tags",remote,f"refs/heads/{selected}:refs/remotes/{remote}/{selected}",check=False)
 if fetched.returncode:return False
 if git(repo,"rev-parse","HEAD").stdout.strip()!=b["decision_head"] or git(repo,"rev-parse",f"refs/heads/{selected}").stdout.strip()!=b["local_head"] or git(repo,"rev-parse",f"refs/remotes/{remote}/{selected}").stdout.strip()!=b["remote_head"]:return False
 t=plan["target"]
 if t["kind"]=="existing_issue":
  live=github(t["repo"],"issue","view",str(t["issue_number"]),"--json","number,url,state,title,body,updatedAt")
  if not isinstance(live,dict):raise CommandError("invalid_json","target","GitHub issue view did not return a JSON object.")
  if live.get("number")!=t["issue_number"] or live.get("url")!=t["url"] or str(live.get("state") or "").lower()!=t["state"] or live.get("updatedAt")!=t["updated_at"] or hashlib.sha256(str(live.get("title") or "").encode()).hexdigest()!=t["title_sha256"] or hashlib.sha256(str(live.get("body") or "").encode()).hexdigest()!=t["body_sha256"]:return False
 return True
def create_issue(plan):
 t=plan["target"];d=t["draft"];args=["issue","create","--title",d["title"],"--body",d["body"]]
 matches=find_reviewed_draft_issues(plan)
 if len(matches)>1:raise CommandError("stale_identity","target","Multiple exact reviewed-draft issues exist; refresh Intake before mutation.",3)
 if matches:return bind_reviewed_issue(plan,matches[0]["number"])
 for label in d["labels"]:args.extend(["--label",label])
 url,_=decode_created_issue_url(t["repo"],run_gh(t["repo"],*args))
 return bind_reviewed_issue(plan,url)
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

def verify_created_boundary(repo,plan,workspace,workspace_mode,artifact_rel,task_dir):
 n=plan["naming"];branch=n["branch_name"];listed=worktrees(repo);row=listed.get(workspace)
 if not workspace.is_dir() or git(workspace,"branch","--show-current").stdout.strip()!=branch:
  raise CommandError("stale_identity","created_workspace","Created workspace branch is not current.",3)
 if workspace_mode=="worktree" and (not row or row.get("branch")!=f"refs/heads/{branch}"):
  raise CommandError("stale_identity","created_workspace","Created workspace is not registered for the reviewed branch.",3)
 task_path=task_dir/"task.json";ledger_path=workspace/artifact_rel
 if not task_path.is_file() or not ledger_path.is_file():
  raise CommandError("stale_identity","created_workspace","Created task artifacts are incomplete.",3)
 try:task=json.loads(task_path.read_text(encoding="utf-8"))
 except Exception as exc:raise CommandError("stale_identity","created_workspace.task","Created task identity is invalid.",3) from exc
 expected_task,_=workspace_payloads(plan,artifact_rel)
 if task!=expected_task:raise CommandError("stale_identity","created_workspace.task","Created task identity does not match the reviewed plan.",3)
 workspace_mapping,task_mapping=mapping_payloads(repo,plan,workspace,artifact_rel)
 for rel in plan["side_effects"]["runtime_mappings"]:
  expected=expected_mapping(rel,workspace_mapping,task_mapping)
  for mapping_root in {repo.resolve(),workspace.resolve()}:
   path=mapping_root/rel
   if not path.is_file():raise CommandError("stale_identity","created_workspace.runtime_mappings","Created runtime mapping is missing.",3)
   try:value=json.loads(path.read_text(encoding="utf-8"))
   except Exception as exc:raise CommandError("stale_identity","created_workspace.runtime_mappings","Created runtime mapping is invalid.",3) from exc
   if any(value.get(key)!=expected_value for key,expected_value in expected.items() if key!="updated_at"):
    raise CommandError("stale_identity","created_workspace.runtime_mappings","Created runtime mapping identity drifted.",3)

def rollback_created(repo,workspace,branch,original_branch,created_worktree,created_branch,created_files,created_dirs):
 errors=[]
 for path in reversed(created_files):
  try:path.unlink(missing_ok=True)
  except OSError as exc:errors.append(str(exc))
 for path in reversed(created_dirs):
  try:path.rmdir()
  except OSError:pass
 if created_worktree:
  p=git(repo,"worktree","remove","--force",str(workspace),check=False)
  if p.returncode:errors.append(p.stderr.strip() or "worktree removal failed")
 if created_branch:
  if not created_worktree and git(repo,"branch","--show-current").stdout.strip()==branch:
   p=git(repo,"switch",original_branch,check=False)
   if p.returncode:errors.append(p.stderr.strip() or "original branch restoration failed")
  p=git(repo,"branch","-D",branch,check=False)
  if p.returncode:errors.append(p.stderr.strip() or "branch removal failed")
 if errors:raise CommandError("stale_identity","rollback","Creation rollback did not complete; stop before retry.",3)
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--input");p.add_argument("--invocation");a=parse(p,argv);repo=root(package_root,a.root);e=load(repo,package_root,a.invocation,"invocation") if a.invocation else None;plan=e.get("plan") if isinstance(e,dict) else load(repo,package_root,a.input,"input");validate_plan(package_root,repo,plan);gate=plan["ai_review_gate"]["status"]
 if gate!="passed":
  before=snapshot(repo,plan);exit_id="refresh_review" if gate=="reroute" else "blocked";result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":now(),"mode":plan["mode"],"variant":"no_side_effect","plan_sha256":plan["freshness"]["plan_sha256"],"executor":stage("blocked",["The semantic gate did not authorize mutation."]),"checker":stage("not_run",[]),"created_issue":None,"created_workspace":None,"no_side_effect":{"reason_code":"target_changed" if exit_id=="refresh_review" else "execution_blocked","before":before,"after":snapshot(repo,plan),"zero_writes":True},"typed_exit":exit_id,"reason":"The reviewed plan requires refresh or is blocked.","consumer":CONSUMERS[exit_id],"facts_sha256":""};return finalize(package_root,result)
 if plan["target"]["kind"]=="reviewed_draft":
  before=snapshot(repo,plan)
  if not mutation_boundary_current(repo,plan):
   result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":now(),"mode":plan["mode"],"variant":"no_side_effect","plan_sha256":plan["freshness"]["plan_sha256"],"executor":stage("blocked",["The authoritative base or target changed at the mutation boundary."]),"checker":stage("not_run",[]),"created_issue":None,"created_workspace":None,"no_side_effect":{"reason_code":"prerequisite_refresh","before":before,"after":snapshot(repo,plan),"zero_writes":True},"typed_exit":"refresh_review","reason":"Current authority changed before the first business write.","consumer":CONSUMERS["refresh_review"],"facts_sha256":""};return finalize(package_root,result)
  created=create_issue(plan);result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":now(),"mode":plan["mode"],"variant":"created_issue","plan_sha256":plan["freshness"]["plan_sha256"],"executor":stage("passed",["Created and immediately reread the exact reviewed GitHub issue."]),"checker":stage("not_run",[]),"created_issue":created,"created_workspace":None,"no_side_effect":None,"typed_exit":"refresh_review","reason":"The reviewed issue was created and now requires a complete Intake refresh.","consumer":CONSUMERS["refresh_review"],"facts_sha256":""};return finalize(package_root,result)
 n=plan["naming"];workspace_config=resolve_workspace(repo,n["workspace_slug"]);workspace=workspace_config.path;branch=n["branch_name"];artifact_rel=Path(plan["side_effects"]["task_artifacts"][0]);task_dir=workspace/artifact_rel.parent
 before=snapshot(repo,plan)
 try:
  artifact_rel,task_dir,task,ledger_bytes=preflight(repo,plan,workspace_config)
 except CommandError as exc:
  existing_task=task_dir/"task.json"
  active_task=False
  try:
   active_task=json.loads(existing_task.read_text(encoding="utf-8")).get("status")=="in_progress"
  except (OSError, json.JSONDecodeError, AttributeError):
   pass
  if exc.code=="stale_identity" and active_task:
   result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":now(),"mode":plan["mode"],"variant":"no_side_effect","plan_sha256":plan["freshness"]["plan_sha256"],"executor":stage("blocked",["The reviewed task identity is incomplete or conflicting; no repair was attempted."]),"checker":stage("not_run",[]),"created_issue":None,"created_workspace":None,"no_side_effect":{"reason_code":"invalid_task_state","before":before,"after":snapshot(repo,plan),"zero_writes":True},"typed_exit":"invalid_task_state","reason":"The reviewed task identity cannot be consumed safely.","consumer":CONSUMERS["invalid_task_state"],"facts_sha256":""}
   return finalize(package_root,result)
  raise
 if not mutation_boundary_current(repo,plan):
  result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":now(),"mode":plan["mode"],"variant":"no_side_effect","plan_sha256":plan["freshness"]["plan_sha256"],"executor":stage("blocked",["The authoritative base or target changed at the mutation boundary."]),"checker":stage("not_run",[]),"created_issue":None,"created_workspace":None,"no_side_effect":{"reason_code":"prerequisite_refresh","before":before,"after":snapshot(repo,plan),"zero_writes":True},"typed_exit":"refresh_review","reason":"Current authority changed before the first business write.","consumer":CONSUMERS["refresh_review"],"facts_sha256":""};return finalize(package_root,result)
 created_files=[];created_dirs=[];created_worktree=False;created_branch=False;original_branch=git(repo,"branch","--show-current").stdout.strip()
 try:
  if n["branch_disposition"]=="create_new":
   if workspace_config.mode=="current":git(repo,"switch","-c",branch,plan["base"]["base_ref"])
   else:git(repo,"worktree","add","-b",branch,str(workspace),plan["base"]["base_ref"])
   created_branch=True;created_worktree=workspace_config.mode=="worktree"
  if workspace_config.mode=="current" and n["branch_disposition"]=="reuse_exact" and git(repo,"branch","--show-current").stdout.strip()!=branch:git(repo,"switch",branch)
  if n["workspace_disposition"]=="create_new" and workspace_config.mode=="worktree" and n["branch_disposition"]!="create_new":git(repo,"worktree","add",str(workspace),branch);created_worktree=True
  if not task_dir.exists():created_dirs.append(task_dir)
  task_dir.mkdir(parents=True,exist_ok=True)
  task_path=task_dir/"task.json"
  if n["task_disposition"]=="reuse_exact":
   try:existing_task=json.loads(task_path.read_text())
   except Exception as exc:raise CommandError("stale_identity","naming.task_disposition","Reusable task is invalid.",3) from exc
   if existing_task!=task:raise CommandError("stale_identity","naming.task_disposition","Reusable task does not match the reviewed task.",3)
  else:task_path.write_text(json.dumps(task,ensure_ascii=False,indent=2)+"\n");created_files.append(task_path)
  ledger_path=workspace/artifact_rel
  ledger_path.write_text(ledger_bytes);os.chmod(ledger_path,0o644);created_files.append(ledger_path)
  mappings=[];workspace_mapping,task_mapping=mapping_payloads(repo,plan,workspace,artifact_rel)
  for rel in plan["side_effects"]["runtime_mappings"]:
   payload=expected_mapping(rel,workspace_mapping,task_mapping)
   for mapping_root in {repo.resolve(),workspace.resolve()}:
    q=mapping_root/rel;q.parent.mkdir(parents=True,exist_ok=True)
    if not q.exists():created_files.append(q)
    q.write_text(json.dumps(payload)+"\n")
   mappings.append({"path":rel,"ignored":True})
  verify_created_boundary(repo,plan,workspace,workspace_config.mode,artifact_rel,task_dir)
  data=ledger_path.read_bytes();artifact={"path":artifact_rel.as_posix(),"sha256":__import__('hashlib').sha256(data).hexdigest(),"size":len(data),"mode":"100644","tracked":True};created={"repo":plan["target"]["repo"],"issue_number":plan["target"]["issue_number"],"branch_name":branch,"base_ref":plan["base"]["base_ref"],"base_head":plan["base"]["decision_head"],"workspace_slug":n["workspace_slug"],"task_slug":n["task_slug"],"task_artifact_dir":artifact_rel.parent.as_posix(),"assignee":plan["assignee"]["login"],"task_status":"planning","artifacts":[artifact],"runtime_mappings":mappings,"workspace_boundary_match":True,"source_developer_identity_created":False,"target_developer_identity_created":False,"workspace_journal_created":False}
 except Exception:
  rollback_created(repo,workspace,branch,original_branch,created_worktree,created_branch,created_files,created_dirs)
  raise
 result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":now(),"mode":plan["mode"],"variant":"created_workspace","plan_sha256":plan["freshness"]["plan_sha256"],"executor":stage("passed",["Created the exact reviewed branch, worktree, task, ledger, and runtime mappings."]),"checker":stage("not_run",[]),"created_issue":None,"created_workspace":created,"no_side_effect":None,"typed_exit":"created","reason":"The reviewed task workspace was created.","consumer":CONSUMERS["created"],"facts_sha256":""};return finalize(package_root,result)
