from __future__ import annotations
import argparse, copy, hashlib, json, subprocess, sys
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json
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
def file_set(repo,paths):return digest([{"path":x,"content_sha256":hashlib.sha256((repo/x).read_bytes()).hexdigest()} for x in paths])
def git(repo,*args):
 p=subprocess.run(["git",*args],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise CommandError("stale_identity","repository",p.stderr.strip() or "Repair Git state.",3)
 return p.stdout.strip()
def content_identity(repo,paths=None):
 paths=paths or [x for x in git(repo,"ls-files").splitlines() if not x.startswith(".trellis/.runtime/")]
 return file_set(repo,sorted(paths))
def validate_owner(package_root,payload,name,field="input"):validate_json(payload,package_root/"schemas"/name,field);return payload
def typed_output(package_root,exit_id):
 interface=json.loads((package_root/"interface.json").read_text());rows=[x for x in interface["public_contracts"]["outputs"] if x["exit_id"]==exit_id]
 if len(rows)!=1:raise CommandError("schema_mismatch","typed_exit","Return one declared typed exit.")
 row=rows[0];value=json.loads((package_root/row["example"]["path"]).read_text());validate_json(value,package_root/row["schema"]["path"],"stdout");return value
def checkpoint(repo,t,name):return repo/".trellis/.runtime/guru-team/owner-checkpoints"/t.name/name
def store(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
def consume_checkpoint(repo,t,value):
 q=Path(str(value or ""));q=q if q.is_absolute() else repo/q
 expected=checkpoint(repo,t,"planning-approval.json")
 if q.is_symlink() or q.resolve()!=expected.resolve() or not q.is_file():raise CommandError("unsafe_path","owner_result","Use the exact current planning checkpoint.")
 q.unlink()
 for parent in (q.parent,q.parent.parent):
  try:parent.rmdir()
  except OSError:break
