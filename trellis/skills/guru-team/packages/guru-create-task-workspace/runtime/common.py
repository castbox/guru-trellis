from __future__ import annotations
import argparse,copy,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
from typing import NamedTuple
SHARED_ROOT=next((p for p in Path(__file__).resolve().parents if (p/"runtime/io.py").is_file() and (p/"runtime/schema.py").is_file()),None)
if SHARED_ROOT is not None and str(SHARED_ROOT) not in sys.path:sys.path.insert(0,str(SHARED_ROOT))
from runtime.io import CommandError
from runtime.schema import validate_json
CONSUMERS={"created":{"kind":"workflow","id":"guru-task-workspace-created"},"refresh_review":{"kind":"skill","id":"guru-sync-base"},"blocked":{"kind":"stop","id":"task-workspace-blocked"}}
class WorkspaceConfig(NamedTuple):
 mode:str
 root:Path
 path:Path

def _strip_yaml_comment(raw):
 quote=None;escaped=False
 for index,char in enumerate(raw):
  if escaped:escaped=False;continue
  if char=="\\" and quote=='"':escaped=True;continue
  if char in {"'",'"'}:
   if quote==char:quote=None
   elif quote is None:quote=char
  elif char=="#" and quote is None:return raw[:index]
 return raw

def config(repo):
 path=repo/".trellis/guru-team/config.yml"
 if not path.is_file() or path.is_symlink():raise CommandError("unsafe_path","workspace_config","Install a regular .trellis/guru-team/config.yml file.")
 values={"github_repo":"","base_branch":"","base_branch_candidates":["dev","develop","main","master"]};active_list=None;seen=set()
 for raw in path.read_text(encoding="utf-8").splitlines():
  line=_strip_yaml_comment(raw).rstrip()
  if not line.strip():continue
  text=line.strip()
  if text.startswith("- ") and active_list:
   current=values.setdefault(active_list,[])
   if current=="":current=[];values[active_list]=current
   if not isinstance(current,list):raise CommandError("unsafe_path","workspace_config",f"Configuration key is not a list: {active_list}.")
   current.append(text[2:].strip().strip("'\""));continue
  if len(line)!=len(line.lstrip()):
   if active_list:values[active_list]={"invalid_structure":text};active_list=None
   continue
  active_list=None
  if ":" not in text:continue
  key,value=(part.strip() for part in text.split(":",1));active_list=key if not value else None
  if key in seen:raise CommandError("unsafe_path","workspace_config",f"Duplicate configuration key: {key}.")
  seen.add(key)
  if not value:
   if key in values and isinstance(values[key],list):values[key]=[]
   else:values[key]=""
  elif value.casefold() in {"true","false"}:values[key]=value.casefold()=="true"
  elif value.isdigit():values[key]=int(value)
  else:values[key]=value.strip("'\"")
 return values

def resolve_workspace(repo,workspace_slug):
 values=config(repo);mode=values.get("workspace_mode");configured=values.get("worktree_root","")
 if mode not in {"worktree","current"}:raise CommandError("unsafe_path","workspace_mode","Set workspace_mode to worktree or current before mutation.")
 if not isinstance(configured,str) or "\x00" in configured or "\n" in configured or "\r" in configured or configured.strip().startswith(("[","{")):raise CommandError("unsafe_path","worktree_root","Use an empty, absolute, or repository-relative path scalar.")
 if mode=="current":
  if configured.strip():raise CommandError("unsafe_path","worktree_root","Leave worktree_root empty when workspace_mode is current.")
  return WorkspaceConfig(mode,repo,repo)
 value=configured.strip();candidate=Path(value) if value else repo.parent/f"{repo.name}-worktrees"
 workspace_root=(candidate if candidate.is_absolute() else repo/candidate).resolve()
 workspace=(workspace_root/workspace_slug).resolve()
 if workspace_root==repo or workspace==repo or repo in workspace.parents:raise CommandError("unsafe_path","worktree_root","Use a workspace root outside the repository checkout.")
 return WorkspaceConfig(mode,workspace_root,workspace)

def require_directory_ancestors(path,field):
 candidate=path
 while not candidate.exists() and candidate!=candidate.parent:candidate=candidate.parent
 if candidate.exists() and not candidate.is_dir():raise CommandError("unsafe_path",field,"Resolve the non-directory parent path before mutation.")

def worktrees(repo):
 rows={};current={}
 for line in git(repo,"worktree","list","--porcelain").stdout.splitlines()+[""]:
  if not line:
   if "worktree" in current:rows[Path(current["worktree"]).resolve()]=current
   current={};continue
  key,_,value=line.partition(" ");current[key]=value
 return rows
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
