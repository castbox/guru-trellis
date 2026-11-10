from __future__ import annotations
import argparse, copy, hashlib, json, os, re, stat, subprocess, sys
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.reviewed_content import reviewed_content_metadata_path
from runtime.parent_git import ParentGitError, index_entries, head_entries, parent_status_records
PHASE2_WORKTREE_CONTENT_ALGORITHM="guru-phase2-worktree-content-3.0"
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
def gitlink_entries(repo,paths,*,resolved=False):
 try:index=index_entries(repo);tree=head_entries(repo)
 except ParentGitError as exc:raise CommandError("stale_identity","reviewed_paths",str(exc),3) from exc
 entries={}
 for path in paths:
  entry=index.get(path)
  if entry is not None and entry["mode"]=="160000":entries[path]={**entry,"kind":"gitlink"}
  elif entry is None and tree.get(path,{}).get("mode")=="160000":entries[path]={"path":path,"kind":"missing"}
 return entries
def file_set(repo,paths,*,resolved=False):
 rows=[];gitlinks=gitlink_entries(repo,paths,resolved=resolved)
 for path in sorted(paths,key=lambda value:value.encode()):
  entry=gitlinks.get(path)
  if entry is not None:
   rows.append(entry);continue
  target=repo/path
  try:metadata=target.lstat()
  except FileNotFoundError:
   rows.append({"path":path,"kind":"missing"});continue
  if stat.S_ISREG(metadata.st_mode):rows.append({"path":path,"kind":"file","content_sha256":hashlib.sha256(target.read_bytes()).hexdigest(),"mode":"100755" if metadata.st_mode & stat.S_IXUSR else "100644"})
  elif stat.S_ISLNK(metadata.st_mode):rows.append({"path":path,"kind":"symlink","target":os.readlink(target)})
  else:raise CommandError("stale_identity","reviewed_paths",f"Unsupported reviewed-content path type: {path}",3)
 return digest({"algorithm":PHASE2_WORKTREE_CONTENT_ALGORITHM,"entries":rows})
def git(repo,*args):
 p=subprocess.run(["git",*args],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise CommandError("stale_identity","repository",p.stderr.strip() or "Repair Git state.",3)
 return p.stdout.strip()
def content_identity(repo,paths=None,*,resolved=False):
 if paths is None:
  try:
   paths=set(index_entries(repo))
   for row in parent_status_records(repo):
    paths.add(row["path"])
    if row.get("renamed_from"):paths.add(row["renamed_from"])
  except ParentGitError as exc:raise CommandError("stale_identity","reviewed_paths",str(exc),3) from exc
  paths={path for path in paths if not reviewed_content_metadata_path(path)}
 return file_set(repo,sorted(paths),resolved=resolved)
def dirty_paths(repo):
 try:records=parent_status_records(repo)
 except ParentGitError as exc:raise CommandError("stale_identity","repository",str(exc),3) from exc
 return sorted({row["path"] for row in records if not row["path"].startswith(".trellis/.runtime/")})
def validate_candidate_classifications(payload):
 rows=payload.get("candidate_classifications")
 if not isinstance(rows,list):raise CommandError("schema_mismatch","candidate_classifications","Record the complete current candidate set as an array, including an empty array when no candidates were observed.")
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


def skill_content_identity(package, repo, task_ref, mode, public=None):
    """Select resolved capture only from a validated public Delivery input."""
    if public is None:
        return content_identity(repo)
    if public.get("profile") == "delivery_planning_stale_recovery":
        validate_json(public, package / "schemas/public-delivery-planning-stale-recovery-input-1.0.schema.json", "skill_input")
        if public["task_ref"] != task_ref or public["mode"] != mode:
            raise CommandError("stale_identity", "skill_input", "Use the same Task and mode for rollback correction.", 3)
        if public["original_check_input"]["profile"] == "delivery_resolved_reconciliation":
            from delivery import _current_delivery
            from runtime.delivery_projection.adapter import DeliveryProjection
            delivery = _current_delivery(DeliveryProjection(repo, task_ref), public)
            return resolved_content_identity(repo, public["original_check_input"], delivery)
        return content_identity(repo)
    from delivery import _binding
    from runtime.delivery_projection.adapter import DeliveryProjection
    profile = public.get("profile", "")
    profiles = {"delivery_candidate_check", "delivery_initial_check", "delivery_finding_fix_rerun",
                "delivery_planning_reentry", "delivery_resolved_reconciliation"}
    if profile not in profiles:
        raise CommandError("schema_mismatch", "skill_input.profile", "Use one current Check Delivery profile.")
    validate_json(public, package / "schemas" / ("public-" + profile.replace("_", "-") + "-input-1.0.schema.json"), "skill_input")
    if public["task_ref"] != task_ref or public["mode"] != mode:
        raise CommandError("stale_identity", "skill_input", "Use the same Task and mode as the semantic result.", 3)
    delivery = _binding(DeliveryProjection(repo, task_ref), public)
    if profile != "delivery_resolved_reconciliation":
        return content_identity(repo)
    return resolved_content_identity(repo, public, delivery)


def resolved_content_identity(repo, public, delivery):
    """Bind semantic stage-0 entries, independent of Git index cache bytes."""
    from runtime.git_merge import git_path, require_merge_state
    merge_path = git_path(repo, "MERGE_HEAD")
    merge_heads = merge_path.read_text().split() if merge_path.is_file() else []
    if len(merge_heads) != 1:
        raise CommandError("stale_identity", "merge_head", "Use exactly one active resolved merge.", 3)
    merge_head = git(repo, "rev-parse", "--verify", merge_heads[0] + "^{commit}")
    require_merge_state(repo, merge_head)
    try:
        records = parent_status_records(repo)
    except ParentGitError as exc:
        raise CommandError("stale_identity", "repository.index", str(exc), 3) from exc
    current_metadata = public["task_ref"] + "/task.json"
    if any(row["path"] != current_metadata and
           (row["status_text"] == "??" or row["status_text"][1] != " ")
           for row in records):
        raise CommandError("stale_identity", "worktree", "Stage every reviewed business change before resolved Check.", 3)
    raw = git(repo, "ls-files", "--stage", "-z")
    entries = []
    for row in filter(None, raw.split("\0")):
        metadata, path = row.split("\t", 1)
        mode, oid, stage = metadata.split()
        if stage != "0":
            raise CommandError("stale_identity", "repository.index", "Resolve every index entry before Check.", 3)
        entries.append({"path": path, "mode": mode, "oid": oid})
    return digest({"algorithm": "guru-phase2-resolved-content-2.0",
                   "head": git(repo, "rev-parse", "HEAD"), "merge_head": merge_head,
                   "stage0_tree": git(repo, "write-tree"), "stage0_entries": entries,
                   "content": content_identity(repo, resolved=True),
                   "task_ref": public["task_ref"], "delivery_key": public["delivery_key"],
                   "planning_result": public["planning_accepted_result_id"],
                   "candidate": delivery["candidate"]})
