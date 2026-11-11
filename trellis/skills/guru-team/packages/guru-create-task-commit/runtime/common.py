from __future__ import annotations
import argparse,hashlib,json,os,re,stat,subprocess,sys,tempfile
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle import LifecycleContractError, resolve_active_task_checkout
from runtime.parent_git import ParentGitError, head_entries, index_entries as parent_index_entries, parent_status_records
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
  raw=q.read_text(encoding="utf-8")
 try:v=json.loads(raw)
 except Exception as exc:raise CommandError("invalid_json",field,"Provide one JSON object.") from exc
 if not isinstance(v,dict):raise CommandError("invalid_json",field,"Provide one JSON object.")
 return v
def git(repo,*args,env=None,check=True,input=None):
 p=subprocess.run(["git",*args],cwd=repo,text=True,encoding="utf-8",input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=None if env is None else {**os.environ,**env})
 if check and p.returncode:raise CommandError("stale_identity","repository",p.stderr.strip() or "Repair Git state.",3)
 return p
def sha_file(path):return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
def validate(package_root,value):
 if "delivery_key" in value and value.get("schema_version")!="delivery-4.0":raise CommandError("stale_identity","candidate.schema_version","Reprepare an unexecuted candidate with the current parent-index contract; recover any existing commit receipt through the original invoke first.",3)
 validate_json(value,package_root/("schemas/delivery-commit-candidate-4.0.schema.json" if "delivery_key" in value else "schemas/task-commit-candidate.schema.json"),"candidate")
def repo_rel(repo,path):return path.resolve().relative_to(repo.resolve()).as_posix()
def task_dir(repo,value):
 p=(repo/str(value or "")).resolve()
 if not p.is_dir() or p.is_symlink() or not p.is_relative_to((repo/".trellis/tasks").resolve()):raise CommandError("unsafe_path","input.task_ref","Use one task below .trellis/tasks.")
 return p
def json_file(path,field):
 try:value=json.loads(path.read_text(encoding="utf-8"))
 except Exception as exc:raise CommandError("invalid_json",field,"Provide one valid JSON object.") from exc
 if not isinstance(value,dict):raise CommandError("invalid_json",field,"Provide one valid JSON object.")
 return value
def index_identity(repo,path):
 try:entry=parent_index_entries(repo).get(path)
 except ParentGitError as exc:raise CommandError("stale_identity",path,str(exc),3) from exc
 return (entry["oid"],entry["mode"]) if entry else (None,None)
def worktree_identity(repo,path):
 q=repo/path
 try:meta=q.lstat()
 except FileNotFoundError:return None,None
 if stat.S_ISDIR(meta.st_mode):return None,None
 if stat.S_ISLNK(meta.st_mode):content=os.readlink(q).encode();mode="120000"
 elif stat.S_ISREG(meta.st_mode):content=q.read_bytes();mode="100755" if meta.st_mode&0o111 else "100644"
 else:raise CommandError("unsafe_path",path,"Use a regular file, symlink, deletion, or parent-index gitlink.")
 return hashlib.sha256(content).hexdigest(),mode
def status_records(repo):
 try:return [(row["status_text"],row["path"],row["renamed_from"],row["copied_from"]) for row in parent_status_records(repo)]
 except ParentGitError as exc:raise CommandError("stale_identity","repository",str(exc),3) from exc

def capture_snapshot(repo,excluded=()):
 try:index=parent_index_entries(repo);head=head_entries(repo)
 except ParentGitError as exc:raise CommandError("stale_identity","repository",str(exc),3) from exc
 entries=[]
 for status_text,path,renamed,copied in status_records(repo):
  if path in excluded or path.startswith(".trellis/.runtime/"):continue
  index_entry=index.get(path);head_entry=head.get(path)
  index_blob=index_entry["oid"] if index_entry else None
  index_mode=index_entry["mode"] if index_entry else None
  parent_gitlink=index_mode=="160000" or (not index_entry and head_entry and head_entry["mode"]=="160000")
  if parent_gitlink:
   worktree_sha=None;mode="160000";deleted=index_entry is None
  else:
   worktree_sha,worktree_mode=worktree_identity(repo,path)
   mode=worktree_mode or index_mode;deleted="D" in status_text
  entries.append({"path":path,"index_status":"" if status_text[0]==" " else status_text[0],"worktree_status":"" if status_text[1]==" " else status_text[1],"untracked":status_text=="??","deleted":bool(deleted),"renamed_from":renamed,"copied_from":copied,"index_blob":index_blob,"worktree_sha256":worktree_sha,"mode":mode})
 entries.sort(key=lambda x:(x["path"],x.get("renamed_from") or "",x.get("copied_from") or ""));return {"entries":entries}
def normalize(value,field):
 if not isinstance(value,str) or not value.strip():raise CommandError("schema_mismatch",field,"Provide concrete text.")
 return "\n".join(line.rstrip() for line in value.replace("\r\n","\n").replace("\r","\n").split("\n")).strip()
def canonical_message(raw,issue_reference=None):
 kind=str(raw.get("type") or "").strip().lower();scope=str(raw.get("scope") or "").strip().lower()
 if kind not in {"feat","fix","refactor","perf","test","docs","style","build","ci","chore","revert"} or not re.fullmatch(r"[a-z0-9._/-]+",scope):raise CommandError("schema_mismatch","message","Use a supported Conventional Commit type and scope.")
 values={k:normalize(raw.get(k),f"message.{k}") for k in ("summary","background","changes","boundaries","validations")}
 issue=raw.get("issue_reference",issue_reference)
 if issue is not None and (isinstance(issue,bool) or not isinstance(issue,int) or issue<1):raise CommandError("schema_mismatch","message.issue_reference","Use a positive Issue number or omit the reference.")
 prefix=f"#{issue} " if issue is not None else "";footer=f"\n\nRefs #{issue}" if issue is not None else ""
 subject=f"{kind}({scope}): {prefix}{values['summary']}";body=f"背景：\n{values['background']}\n\n变更：\n{values['changes']}\n\n边界：\n{values['boundaries']}\n\n验证：\n{values['validations']}{footer}"
 result={"type":kind,"scope":scope,**values,"subject":subject,"body":body,"bytes":subject+"\n\n"+body+"\n"}
 if issue is not None:result["issue_reference"]=issue
 return result
def candidate_path(repo,td):
 root=repo/".trellis/.runtime/guru-team/task-commit-plans"/td.name;root.mkdir(parents=True,exist_ok=True)
 existing=sorted(root.glob("[0-9][0-9][0-9].json"))
 if len(existing)>1:raise CommandError("stale_identity","candidate","Resolve ambiguous private candidates.",3)
 return (existing[0] if existing else root/"001.json"),(existing[0].stem if existing else "001")
def canonical_candidate_locator(repo,value):
 path=Path(str(value or ""));path=path if path.is_absolute() else repo/path
 try:relative=path.resolve().relative_to((repo/".trellis/.runtime/guru-team/task-commit-plans").resolve())
 except ValueError as exc:raise CommandError("unsafe_path","candidate_artifact","Use the candidate locator returned by prepare-task-commit.") from exc
 if len(relative.parts)!=2 or not re.fullmatch(r"[0-9]{3}\.json",relative.name):raise CommandError("unsafe_path","candidate_artifact","Use the candidate locator returned by prepare-task-commit.")
 return path,relative.as_posix(),relative.parent.name,relative.stem
def commit_result_path(repo,task_key,sequence):return repo/".trellis/.runtime/guru-team/task-commit-results"/task_key/f"{sequence}.json"
def build_candidate(package_root,repo,public,authoring):
 profile=public.get("profile")
 if profile=="delivery_pre_review_committed_reentry":raise CommandError("invalid_arguments","input.profile","Use invoke --input for clean committed Draft reentry; prepare accepts a dirty commit profile.")
 delivery_profile=str(profile).startswith("delivery_");schemas={"initial_commit":"public-initial-commit-input.schema.json","revision_reentry":"public-revision-reentry-input.schema.json","finding_fix_commit":"public-finding-fix-commit-input.schema.json","recovery_resume":"public-recovery-resume-input.schema.json"}
 if profile not in {"delivery_pre_review_commit", "delivery_pre_review_committed_reentry"}:raise CommandError("schema_mismatch","input.profile","Use a current Delivery commit profile; old Task planning is diagnostic-only.")
 if delivery_profile:schemas[profile]="public-"+profile.replace("_","-")+"-input-1.0.schema.json"
 if profile not in schemas:raise CommandError("schema_mismatch","input.profile","Use one declared task commit profile.")
 validate_json(public,package_root/"schemas"/schemas[profile],"input");td=task_dir(repo,public["task_ref"])
 try:checkout=resolve_active_task_checkout(repo,public["task_ref"])
 except LifecycleContractError as exc:raise CommandError("stale_identity",exc.field_path,exc.remediation,3) from exc
 task=json_file(td/"task.json","task")
 if delivery_profile:
  from delivery import current_pre_review
  from runtime.delivery_projection.adapter import DeliveryProjection
  projection=DeliveryProjection(repo,public["task_ref"])
  selected=current_pre_review(projection,public)
 cp,sequence=candidate_path(repo,td)
 receipt=commit_result_path(repo,td.name,sequence)
 if cp.is_file() and receipt.is_file():raise CommandError("stale_identity","candidate","Recover the existing candidate and commit receipt through invoke before preparing another operation.",3)
 snapshot=capture_snapshot(repo,{repo_rel(repo,cp)});raw=authoring.get("path_classifications")
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
 base=str(task.get("base_branch") or "main");base_ref=public["base_ref"]
 candidate={"$schema":"https://github.com/castbox/guru-trellis/schemas/guru-task-commit-candidate-5.0.json","schema_version":"5.0","skill_id":"guru-create-task-commit","sequence":sequence,"task":{"id":checkout.artifact.task_id,"path":public["task_ref"],"status":"in_progress","branch":checkout.branch_name},"git":{"base_branch":base,"base_ref":base_ref,"pre_commit_head":git(repo,"rev-parse","HEAD").stdout.strip()},"dirty_snapshot":snapshot,"path_classifications":sorted(classifications,key=lambda x:x["path"]),"exact_stage_paths":sorted(exact),"message":canonical_message(authoring.get("message") if isinstance(authoring.get("message"),dict) else {}),"ai_review":{"status":review["status"],"summary":normalize(review.get("summary"),"ai_review.summary"),"evidence":[normalize(x,"ai_review.evidence") for x in review["evidence"]]}}
 if delivery_profile:
  candidate.update(delivery_key=public["delivery_key"],commit_kind="pre_review",schema_version="delivery-4.0")
  candidate["$schema"]="https://github.com/castbox/guru-trellis/schemas/guru-delivery-commit-candidate-4.0.json"
  candidate["task"].pop("status")
 validate_candidate(package_root,repo,candidate);cp.write_text(json.dumps(candidate,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n");receipt=commit_result_path(repo,td.name,sequence);receipt.unlink(missing_ok=True)
 try:receipt.parent.rmdir()
 except OSError:pass
 return cp,candidate
def validate_candidate(package_root,repo,c):
 validate(package_root,c)
 if "delivery_key" in c:
  from delivery import current_pre_review
  from runtime.delivery_projection.adapter import DeliveryProjection
  projection=DeliveryProjection(repo,c["task"]["path"])
  current_pre_review(projection,{**c,"base_ref":c["git"]["base_ref"]})
 if git(repo,"rev-parse","HEAD").stdout.strip()!=c["git"]["pre_commit_head"] or git(repo,"rev-parse","--abbrev-ref","HEAD").stdout.strip()!=c["task"]["branch"]:raise CommandError("stale_identity","git.pre_commit_head","Reprepare candidate from current branch HEAD.",3)
 entries={x["path"]:x for x in c["dirty_snapshot"]["entries"]}
 by={x["path"]:x for x in c["path_classifications"]};exact=set(c["exact_stage_paths"]);reviewed={p for p,x in by.items() if x["category"]=="task-reviewed"};rename_sources={entries[p]["renamed_from"] for p in reviewed if p in entries and entries[p].get("renamed_from")}
 if not exact or not reviewed.issubset(exact) or not exact.issubset(reviewed|rename_sources) or not rename_sources.issubset(exact) or any(x["category"] in {"unreviewed-blocking","ambiguous-blocking"} for x in c["path_classifications"]):raise CommandError("schema_mismatch","exact_stage_paths","Stage reviewed paths plus their exact rename sources and resolve blocking classifications.")
 live={row["path"]:row for row in capture_snapshot(repo)["entries"]}
 for path in exact:
  row=entries.get(path)
  if row is None:
   if path in rename_sources:continue
   raise CommandError("stale_identity","dirty_snapshot","Reprepare current dirty paths.",3)
  if row.get("mode")=="160000":
   if live.get(path)!=row:raise CommandError("stale_identity",path,"Reprepare the changed parent gitlink entry.",3)
  elif row["deleted"]:
   if (repo/path).exists():raise CommandError("stale_identity",path,"Reprepare the changed deleted path.",3)
  elif worktree_identity(repo,path)!=(row["worktree_sha256"],row["mode"]):raise CommandError("stale_identity",path,"Reprepare the changed reviewed bytes or mode.",3)
 if c["ai_review"]["status"]!="passed":return "revision-required" if c["ai_review"]["status"]=="revision-required" else "blocked"
 if c["message"]["bytes"]!=c["message"]["subject"]+"\n\n"+c["message"]["body"]+"\n":raise CommandError("schema_mismatch","message.bytes","Use canonical subject/body bytes.")
 return "committed"
