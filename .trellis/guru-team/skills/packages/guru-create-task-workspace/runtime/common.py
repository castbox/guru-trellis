from __future__ import annotations
import argparse,copy,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json
CONSUMERS={"created":{"kind":"workflow","id":"guru-task-workspace-created"},"refresh_review":{"kind":"skill","id":"guru-sync-base"},"blocked":{"kind":"stop","id":"task-workspace-blocked"}}
def parse(p,argv):
 p.add_argument("--json",action="store_true")
 try:return p.parse_args(argv)
 except SystemExit as exc:raise CommandError("invalid_arguments","arguments","Use exact command help.") from exc
def root(package_root,value=None):
 r=Path(value or ".").resolve()
 if not r.is_dir():raise CommandError("unsafe_path","root","Use a repository root.")
 return r
def load(repo,package_root,value,field):
 if value=="-":raw=sys.stdin.read()
 else:
  q=Path(str(value or ""));choices=[q] if q.is_absolute() else [repo/q,package_root/q];q=next((x for x in choices if x.is_file() and not x.is_symlink()),None)
  if q is None:raise CommandError("unsafe_path",field,"Use a regular JSON file.")
  raw=q.read_text()
 try:v=json.loads(raw)
 except Exception as exc:raise CommandError("invalid_json",field,"Provide one JSON object.") from exc
 if not isinstance(v,dict):raise CommandError("invalid_json",field,"Provide one JSON object.")
 return v
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def git(repo,*args,check=True):
 p=subprocess.run(["git",*args],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if check and p.returncode:raise CommandError("stale_identity","repository",p.stderr.strip() or "Repair Git state.",3)
 return p
def validate(package_root,v,name,field="input"):validate_json(v,package_root/"schemas"/name,field);return v
def reviewable(plan):return {k:copy.deepcopy(plan[k]) for k in ("schema_version","skill_id","mode","invocation","prerequisites","target","scope","base","naming","assignee","side_effects")}
def plan_digest(plan):
 v=copy.deepcopy(plan);v["freshness"].pop("plan_sha256",None);return digest(v)
def validate_plan(package_root,repo,plan):
 validate(package_root,plan,"task-workspace-plan.schema.json")
 r=digest(reviewable(plan));f=plan["freshness"]
 if f["reviewable_plan_sha256"]!=r or f["plan_sha256"]!=plan_digest(plan) or plan["ai_review_gate"]["reviewed_plan_sha256"]!=r:raise CommandError("stale_identity","freshness","Rerecord the exact current plan.",3)
 if git(repo,"rev-parse","HEAD").stdout.strip()!=plan["base"]["decision_head"]:raise CommandError("stale_identity","base.decision_head","Refresh base and plan.",3)
 return plan
def finalize(package_root,result):
 result["facts_sha256"]=digest({k:v for k,v in result.items() if k!="facts_sha256"});return validate(package_root,result,"task-workspace-result.schema.json","result")
def snapshot(repo,plan):
 return {"head":git(repo,"rev-parse","HEAD").stdout.strip(),"status_sha256":hashlib.sha256(git(repo,"status","--porcelain=v1","-z","--untracked-files=all").stdout.encode()).hexdigest(),"worktrees_sha256":hashlib.sha256(git(repo,"worktree","list","--porcelain").stdout.encode()).hexdigest(),"issues_sha256":digest(plan["target"])}
def stage(status,evidence):return {"status":status,"checked_at":now(),"evidence":evidence}
