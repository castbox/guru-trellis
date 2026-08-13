from __future__ import annotations
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json
def parse(p,argv):
 p.add_argument("--json",action="store_true")
 try:return p.parse_args(argv)
 except SystemExit as exc:raise CommandError("invalid_arguments","arguments","Use exact command help.") from exc
def root(package_root,value=None):
 r=Path(value or ".").resolve()
 if not (r/".git").exists():raise CommandError("unsafe_path","root","Use a Git repository root.")
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
def git(repo,*args,check=True):
 p=subprocess.run(["git",*args],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if check and p.returncode:raise CommandError("stale_identity","repository",p.stderr.strip() or "Repair Git state.",3)
 return p.stdout.strip()
def ancestor(repo,a,b):return subprocess.run(["git","merge-base","--is-ancestor",a,b],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE).returncode==0
def dirty_paths(repo,task_ref):
 rows=[]
 for line in git(repo,"status","--porcelain=v1","-z","--untracked-files=all").split("\0"):
  if not line:continue
  path=line[3:].split(" -> ")[-1]
  if path.startswith(task_ref+"/") and Path(path).name in {"review.md","review-gate.json"}:continue
  rows.append(path)
 return rows
def content_identity(repo,base_commit,commit,task_ref):
 rows=[]
 for line in git(repo,"ls-tree","-rz",commit).split("\0"):
  if not line:continue
  meta,path=line.split("\t",1);mode,kind,oid=meta.split();
  if path.startswith(task_ref+"/") and Path(path).name in {"review.md","review-gate.json"}:continue
  rows.append({"path":path,"mode":mode,"kind":kind,"oid":oid})
 return digest({"algorithm":"guru-reviewed-content-1.0","base_commit":base_commit,"entries":sorted(rows,key=lambda x:x["path"].encode())})
def validate_gate(package_root,repo,v,expected_exit=None):
 validate_json(v,package_root/"schemas/review-gate-4.0.schema.json","gate");unsigned={k:copy.deepcopy(x) for k,x in v.items() if k not in {"generated_at","facts_sha256"}}
 if v["facts_sha256"]!=digest(unsigned):raise CommandError("stale_identity","facts_sha256","Rerecord current review facts.",3)
 if expected_exit and v["typed_exit"]!=expected_exit:raise CommandError("stale_identity","typed_exit","Use current typed exit.",3)
 current=git(repo,"rev-parse","HEAD")
 if not ancestor(repo,v["base_head"],v["review_commit"]):raise CommandError("stale_identity","base_head","Recorded base must precede reviewed task content.",3)
 pair=v.get("integration_pair")
 if pair is not None:
  if not ancestor(repo,pair["old_base_head"],pair["new_base_head"]):raise CommandError("stale_identity","integration_pair","Base continuity requires an ancestor delta.",3)
  if pair["task_head"]!=v["review_commit"]:raise CommandError("stale_identity","integration_pair.task_head","Bind continuity to reviewed task content.",3)
 if dirty_paths(repo,v["task_dir"]):raise CommandError("stale_identity","worktree","Commit or remove all non-review overlays before branch review.",3)
 if not ancestor(repo,v["review_commit"],current):raise CommandError("stale_identity","review_commit","Review commit is not current history.",3)
 if content_identity(repo,v["base_head"],current,v["task_dir"])!=v["reviewed_content_sha256"]:raise CommandError("stale_identity","reviewed_content_sha256","Run a fresh review for current task content.",3)
 for finding in v["semantic_review"]["qualified_findings"]:
  if not ancestor(repo,finding["introduced_head"],v["review_commit"]):raise CommandError("schema_mismatch","qualified_findings","Finding introduction must precede reviewed content.")
  if finding["status"]=="resolved" and (not ancestor(repo,finding["introduced_head"],finding["fix_head"]) or not ancestor(repo,finding["fix_head"],finding["closure_head"]) or not ancestor(repo,finding["closure_head"],v["review_commit"])):raise CommandError("schema_mismatch","qualified_findings","Bind introduced, fix, closure, and review ancestry.")
 return v
