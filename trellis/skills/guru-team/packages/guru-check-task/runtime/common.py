from __future__ import annotations
import argparse, copy, hashlib, json, os, stat, subprocess, sys
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json
PHASE2_WORKTREE_CONTENT_ALGORITHM="guru-phase2-worktree-content-1.0"
def parse(p,argv):
 p.add_argument("--json",action="store_true")
 try:return p.parse_args(argv)
 except SystemExit as exc:raise CommandError("invalid_arguments","arguments","Use the exact command help contract.") from exc
def root(package_root,value=None):
 r=Path(value or ".").resolve()
 if not (r/".git").exists(): raise CommandError("unsafe_path","root","Use a Git repository root.")
 return r
def load(repo,package_root,value,field):
 if value=="-": raw=sys.stdin.read()
 else:
  q=Path(str(value or "")); choices=[q] if q.is_absolute() else [repo/q,package_root/q]; q=next((x for x in choices if x.is_file() and not x.is_symlink()),None)
  if q is None: raise CommandError("unsafe_path",field,"Use a safe regular JSON file.")
  raw=q.read_text()
 try:v=json.loads(raw)
 except Exception as exc:raise CommandError("invalid_json",field,"Provide one valid JSON object.") from exc
 if not isinstance(v,dict):raise CommandError("invalid_json",field,"Provide one valid JSON object.")
 return v
def task(repo,value):
 raw=str(value or "")
 if not raw:
  current=repo/".trellis/.runtime/current-task"
  if current.is_file(): raw=current.read_text().strip()
 if raw.startswith(".trellis/tasks/"): p=repo/raw
 else:
  found=list((repo/".trellis/tasks").glob(f"**/{raw}")) if raw else []
  p=found[0] if len(found)==1 else None
 if p is None or not p.is_dir() or p.is_symlink() or not p.resolve().is_relative_to((repo/".trellis/tasks").resolve()):raise CommandError("unsafe_path","task","Use one current task below .trellis/tasks.")
 return p
def rel(repo,p):return p.resolve().relative_to(repo.resolve()).as_posix()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def file_set(repo,paths):
 rows=[]
 for path in sorted(paths,key=lambda value:value.encode()):
  target=repo/path
  try:metadata=target.lstat()
  except FileNotFoundError:
   rows.append({"path":path,"kind":"missing"});continue
  if stat.S_ISREG(metadata.st_mode):rows.append({"path":path,"kind":"file","content_sha256":hashlib.sha256(target.read_bytes()).hexdigest()})
  elif stat.S_ISLNK(metadata.st_mode):rows.append({"path":path,"kind":"symlink","target":os.readlink(target)})
  else:raise CommandError("stale_identity","reviewed_paths",f"Unsupported reviewed-content path type: {path}",3)
 return digest({"algorithm":PHASE2_WORKTREE_CONTENT_ALGORITHM,"entries":rows})
def git(repo,*args):
 p=subprocess.run(["git",*args],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise CommandError("stale_identity","repository",p.stderr.strip() or "Repair Git state.",3)
 return p.stdout.strip()
def content_identity(repo,paths=None):
 if paths is None:
  tracked=git(repo,"ls-files","-z").split("\0")
  untracked=git(repo,"ls-files","--others","--exclude-standard","-z").split("\0")
  paths=sorted({x for x in [*tracked,*untracked] if x and not x.startswith(".trellis/.runtime/")})
 return file_set(repo,sorted(paths))
def dirty_paths(repo):
 raw=subprocess.run(["git","status","--porcelain=v1","-z","--untracked-files=all"],cwd=repo,stdout=subprocess.PIPE,check=True).stdout.decode("utf-8").split("\0");out=[];i=0
 while i<len(raw) and raw[i]:
  row=raw[i];status=row[:2];path=row[3:]
  if path and not path.startswith(".trellis/.runtime/"):out.append(path)
  if status[0] in "RC":i+=1
  i+=1
 return sorted(set(out))
def validate_candidate_classifications(payload):
 rows=payload.get("candidate_classifications")
 if not isinstance(rows,list) or not rows:raise CommandError("schema_mismatch","candidate_classifications","Record the complete non-empty current candidate set.")
 refs=[row.get("candidate_ref") for row in rows if isinstance(row,dict)]
 if len(refs)!=len(rows) or len(set(refs))!=len(refs):raise CommandError("schema_mismatch","candidate_classifications","Candidate refs must be unique and complete.")
 known=set(refs)
 semantic=payload.get("semantic_review") or {}
 linked=[]
 for key in ("scope_decisions","findings"):
  for row in semantic.get(key,[]):
   if isinstance(row,dict):linked.append(row.get("candidate_ref"))
 if any(not ref or ref not in known for ref in linked):raise CommandError("schema_mismatch","candidate_classifications","Every scope decision and finding must bind one current candidate ref.")
 return payload
def validate_owner(package_root,payload,name,field="input"):validate_json(payload,package_root/"schemas"/name,field);return validate_candidate_classifications(payload)
def typed_output(package_root,exit_id):
 interface=json.loads((package_root/"interface.json").read_text());rows=[x for x in interface["public_contracts"]["outputs"] if x["exit_id"]==exit_id]
 if len(rows)!=1:raise CommandError("schema_mismatch","typed_exit","Return one declared typed exit.")
 row=rows[0];value=json.loads((package_root/row["example"]["path"]).read_text());validate_json(value,package_root/row["schema"]["path"],"stdout");return value
def checkpoint(repo,t,name):return repo/".trellis/.runtime/guru-team/owner-checkpoints"/t.name/name
def store(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
