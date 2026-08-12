from __future__ import annotations
import argparse,hashlib,json,os,re,stat,subprocess,sys,tempfile
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
def git(repo,*args,env=None,check=True,input=None):
 p=subprocess.run(["git",*args],cwd=repo,text=True,input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=None if env is None else {**os.environ,**env})
 if check and p.returncode:raise CommandError("stale_identity","repository",p.stderr.strip() or "Repair Git state.",3)
 return p
def sha_file(path):return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
def validate(package_root,value):validate_json(value,package_root/"schemas/task-commit-candidate.schema.json","candidate")
def repo_rel(repo,path):return path.resolve().relative_to(repo.resolve()).as_posix()
def task_dir(repo,value):
 p=(repo/str(value or "")).resolve()
 if not p.is_dir() or p.is_symlink() or not p.is_relative_to((repo/".trellis/tasks").resolve()):raise CommandError("unsafe_path","input.task_ref","Use one task below .trellis/tasks.")
 return p
def json_file(path,field):
 try:value=json.loads(path.read_text())
 except Exception as exc:raise CommandError("invalid_json",field,"Provide one valid JSON object.") from exc
 if not isinstance(value,dict):raise CommandError("invalid_json",field,"Provide one valid JSON object.")
 return value
def index_identity(repo,path):
 p=git(repo,"ls-files","--stage","--",path,check=False)
 if p.returncode or not p.stdout.strip():return None,None
 fields=p.stdout.split(None,3);return (fields[1],fields[0]) if len(fields)>=3 else (None,None)
def worktree_identity(repo,path):
 q=repo/path
 try:meta=q.lstat()
 except FileNotFoundError:return None,None
 if stat.S_ISDIR(meta.st_mode):return None,None
 if stat.S_ISLNK(meta.st_mode):content=os.readlink(q).encode();mode="120000"
 elif stat.S_ISREG(meta.st_mode):content=q.read_bytes();mode="100755" if meta.st_mode&0o111 else "100644"
 else:raise CommandError("unsafe_path",path,"Use a regular file, symlink, deletion, or initialized gitlink.")
 return hashlib.sha256(content).hexdigest(),mode
def status_records(repo):
 p=subprocess.run(["git","status","--porcelain=v1","-z","--untracked-files=all"],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise CommandError("stale_identity","repository",p.stderr.decode(errors="replace").strip() or "Repair Git state.",3)
 fields=p.stdout.split(b"\0");rows=[];i=0
 while i<len(fields):
  field=fields[i];i+=1
  if not field:continue
  if len(field)<4:raise CommandError("stale_identity","repository","Git returned an invalid status record.",3)
  status_text=field[:2].decode("ascii");path=field[3:].decode("utf-8");renamed=copied=None
  kinds={x for x in status_text if x in "RC"}
  if len(kinds)>1 or status_text in {"DD","AU","UD","UA","DU","AA","UU"}:raise CommandError("stale_identity","repository","Resolve ambiguous or unmerged Git state.",3)
  if kinds:
   if i>=len(fields) or not fields[i]:raise CommandError("stale_identity","repository","Git returned incomplete rename/copy state.",3)
   source=fields[i].decode("utf-8");i+=1
   if kinds=={"R"}:renamed=source
   else:copied=source
  rows.append((status_text,path,renamed,copied))
 return rows
def capture_snapshot(repo,excluded=()):
 entries=[]
 for status_text,path,renamed,copied in status_records(repo):
  if path in excluded or path.startswith(".trellis/.runtime/"):continue
  index_blob,index_mode=index_identity(repo,path);worktree_sha,worktree_mode=worktree_identity(repo,path);deleted="D" in status_text
  row={"path":path,"index_status":"" if status_text[0]==" " else status_text[0],"worktree_status":"" if status_text[1]==" " else status_text[1],"untracked":status_text=="??","deleted":deleted,"renamed_from":renamed,"copied_from":copied,"index_blob":index_blob,"worktree_sha256":worktree_sha,"mode":worktree_mode or index_mode}
  if row["mode"]=="160000":
   q=repo/path
   if deleted and not q.exists():row.update(gitlink_head=None,gitlink_initialized=False,gitlink_dirty=None)
   else:
    head=git(q,"rev-parse","HEAD").stdout.strip() if q.is_dir() else "";dirty=bool(git(q,"status","--porcelain",check=False).stdout) if q.is_dir() else True
    if not re.fullmatch(r"[0-9a-f]{40,64}",head) or dirty:raise CommandError("stale_identity",path,"Use an initialized clean gitlink.",3)
    row.update(gitlink_head=head,gitlink_initialized=True,gitlink_dirty=False)
  entries.append(row)
 entries.sort(key=lambda x:(x["path"],x.get("renamed_from") or "",x.get("copied_from") or ""));return {"entries":entries}
def normalize(value,field):
 if not isinstance(value,str) or not value.strip():raise CommandError("schema_mismatch",field,"Provide concrete text.")
 return "\n".join(line.rstrip() for line in value.replace("\r\n","\n").replace("\r","\n").split("\n")).strip()
def canonical_message(raw,issue):
 kind=str(raw.get("type") or "").strip().lower();scope=str(raw.get("scope") or "").strip().lower()
 if kind not in {"feat","fix","refactor","perf","test","docs","style","build","ci","chore","revert"} or not re.fullmatch(r"[a-z0-9._/-]+",scope):raise CommandError("schema_mismatch","message","Use a supported Conventional Commit type and scope.")
 values={k:normalize(raw.get(k),f"message.{k}") for k in ("summary","background","changes","boundaries","validations")}
 subject=f"{kind}({scope}): #{issue} {values['summary']}";body=f"背景：\n{values['background']}\n\n变更：\n{values['changes']}\n\n边界：\n{values['boundaries']}\n\n验证：\n{values['validations']}\n\nRefs #{issue}"
 return {"type":kind,"scope":scope,**values,"subject":subject,"body":body,"bytes":subject+"\n\n"+body+"\n"}
def candidate_path(repo,td):
 root=repo/".trellis/.runtime/guru-team/task-commit-plans"/td.name;root.mkdir(parents=True,exist_ok=True)
 existing=sorted(root.glob("[0-9][0-9][0-9].json"))
 if len(existing)>1:raise CommandError("stale_identity","candidate","Resolve ambiguous private candidates.",3)
 return (existing[0] if existing else root/"001.json"),(existing[0].stem if existing else "001")
def build_candidate(package_root,repo,public,authoring):
 profile=public.get("profile");schemas={"initial_commit":"public-initial-commit-input.schema.json","revision_reentry":"public-revision-reentry-input.schema.json","finding_fix_commit":"public-finding-fix-commit-input.schema.json","recovery_resume":"public-recovery-resume-input.schema.json"}
 if profile not in schemas:raise CommandError("schema_mismatch","input.profile","Use one declared task commit profile.")
 validate_json(public,package_root/"schemas"/schemas[profile],"input");td=task_dir(repo,public["task_ref"]);task=json_file(td/"task.json","task")
 if task.get("status")!="in_progress" or task.get("branch")!=git(repo,"rev-parse","--abbrev-ref","HEAD").stdout.strip():raise CommandError("stale_identity","task","Use the current in-progress task branch.",3)
 phase2_path=repo/".trellis/.runtime/guru-team/owner-checkpoints"/td.name/"phase2-check.json";phase2=json_file(phase2_path,"phase2")
 if phase2.get("typed_exit")!="passed" or phase2.get("task_ref")!=public["task_ref"] or phase2.get("phase2_capture_commit")!=public["phase2_commit_anchor"]:raise CommandError("stale_identity","phase2_commit_anchor","Rerun Phase 2 for the current task.",3)
 ledger=json_file(td/"issue-scope-ledger.json","issue_scope_ledger");issue=ledger.get("primary_issue",{}).get("number")
 if not isinstance(issue,int) or issue<1:raise CommandError("schema_mismatch","issue_scope_ledger","Provide one primary issue.")
 cp,sequence=candidate_path(repo,td);snapshot=capture_snapshot(repo,{repo_rel(repo,cp)});raw=authoring.get("path_classifications")
 if not isinstance(raw,list):raise CommandError("schema_mismatch","path_classifications","Classify every dirty path.")
 classifications=[]
 for item in raw:
  if not isinstance(item,dict):raise CommandError("schema_mismatch","path_classifications","Use classification objects.")
  classifications.append({"path":str(item.get("path") or "").strip(),"category":str(item.get("category") or "").strip(),"reason":normalize(item.get("reason"),"classification.reason"),"coverage_source":normalize(item.get("coverage_source"),"classification.coverage_source")})
 paths=[x["path"] for x in classifications];snapshot_by={x["path"]:x for x in snapshot["entries"]}
 if len(set(paths))!=len(paths) or set(paths)!=set(snapshot_by):raise CommandError("schema_mismatch","path_classifications","Classify every current dirty path exactly once.")
 exact={x["path"] for x in classifications if x["category"]=="task-reviewed"}
 for path in list(exact):
  source=snapshot_by[path].get("renamed_from")
  if source:exact.add(source)
 review=authoring.get("ai_review")
 if not isinstance(review,dict) or review.get("status") not in {"passed","revision-required","blocked"} or not isinstance(review.get("evidence"),list) or not review["evidence"]:raise CommandError("schema_mismatch","ai_review","Provide the completed AI review.")
 base=str(task.get("base_branch") or "main");base_ref=f"origin/{base}" if git(repo,"rev-parse","--verify",f"origin/{base}",check=False).returncode==0 else base
 candidate={"$schema":"https://github.com/castbox/guru-trellis/schemas/guru-task-commit-candidate-5.0.json","schema_version":"5.0","skill_id":"guru-create-task-commit","sequence":sequence,"task":{"id":task["id"],"path":public["task_ref"],"status":"in_progress","branch":task["branch"]},"git":{"base_branch":base,"base_ref":base_ref,"pre_commit_head":git(repo,"rev-parse","HEAD").stdout.strip(),"phase2_commit_anchor":public["phase2_commit_anchor"]},"dirty_snapshot":snapshot,"path_classifications":sorted(classifications,key=lambda x:x["path"]),"exact_stage_paths":sorted(exact),"message":canonical_message(authoring.get("message") if isinstance(authoring.get("message"),dict) else {},issue),"ai_review":{"status":review["status"],"summary":normalize(review.get("summary"),"ai_review.summary"),"evidence":[normalize(x,"ai_review.evidence") for x in review["evidence"]]}}
 validate_candidate(package_root,repo,candidate);cp.write_text(json.dumps(candidate,ensure_ascii=False,indent=2)+"\n");return cp,candidate
def validate_candidate(package_root,repo,c):
 validate(package_root,c)
 if git(repo,"rev-parse","HEAD").stdout.strip()!=c["git"]["pre_commit_head"] or git(repo,"rev-parse","--abbrev-ref","HEAD").stdout.strip()!=c["task"]["branch"]:raise CommandError("stale_identity","git.pre_commit_head","Reprepare candidate from current branch HEAD.",3)
 entries={x["path"]:x for x in c["dirty_snapshot"]["entries"]}
 by={x["path"]:x for x in c["path_classifications"]};exact=set(c["exact_stage_paths"]);reviewed={p for p,x in by.items() if x["category"]=="task-reviewed"};rename_sources={entries[p]["renamed_from"] for p in reviewed if p in entries and entries[p].get("renamed_from")}
 if not exact or not reviewed.issubset(exact) or not exact.issubset(reviewed|rename_sources) or not rename_sources.issubset(exact) or any(x["category"] in {"unreviewed-blocking","ambiguous-blocking"} for x in c["path_classifications"]):raise CommandError("schema_mismatch","exact_stage_paths","Stage reviewed paths plus their exact rename sources and resolve blocking classifications.")
 for path in exact:
  row=entries.get(path)
  if row is None:raise CommandError("stale_identity","dirty_snapshot","Reprepare current dirty paths.",3)
  q=repo/path
  if row["deleted"]:
   if q.exists():raise CommandError("stale_identity",path,"Reprepare changed path.",3)
  elif row.get("mode")=="160000":
   if not q.is_dir() or git(q,"rev-parse","HEAD").stdout.strip()!=row.get("gitlink_head") or git(q,"status","--porcelain").stdout:raise CommandError("stale_identity",path,"Reprepare the initialized clean gitlink at its exact HEAD.",3)
  elif sha_file(q)!=row["worktree_sha256"]:raise CommandError("stale_identity",path,"Reprepare changed path.",3)
 if c["ai_review"]["status"]!="passed":return "revision-required" if c["ai_review"]["status"]=="revision-required" else "blocked"
 if c["message"]["bytes"]!=c["message"]["subject"]+"\n\n"+c["message"]["body"]+"\n":raise CommandError("schema_mismatch","message.bytes","Use canonical subject/body bytes.")
 return "committed"
