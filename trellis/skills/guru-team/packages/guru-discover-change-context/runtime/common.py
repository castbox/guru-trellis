from __future__ import annotations
import argparse,copy,hashlib,json,re,subprocess,sys,unicodedata
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
  if q is None:raise CommandError("unsafe_path",field,"Use a safe regular JSON file.")
  raw=q.read_text()
 try:v=json.loads(raw)
 except Exception as exc:raise CommandError("invalid_json",field,"Provide one JSON object.") from exc
 if not isinstance(v,dict):raise CommandError("invalid_json",field,"Provide one JSON object.")
 return v
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

QUERY_KINDS=("issue_refs","pr_refs","branches","paths","commands","config_keys","schema_fields","symbols","terms","queries")
EXACT_WEIGHTS={"issue_refs":1000,"pr_refs":900,"branches":800,"paths":700,"commands":600,"config_keys":600,"schema_fields":600,"symbols":600,"terms":400,"queries":300}

def _sort(values):return sorted(set(values),key=lambda value:value.encode("utf-8"))
def _text(value,field):
 if not isinstance(value,str) or not value or any(ord(char)<32 or ord(char)==127 for char in value):raise CommandError("schema_mismatch",field,"Use one non-empty text clue without control characters.")
 value=" ".join(unicodedata.normalize("NFKC",value).casefold().strip().split())
 if not value:raise CommandError("schema_mismatch",field,"Use one non-empty normalized text clue.")
 return value
def _reference(value,pull_request):
 value=_text(value,"query.reference");marker="pull" if pull_request else "issues"
 match=re.fullmatch(rf"https://github\.com/[^/]+/[^/]+/{marker}/([1-9][0-9]*)",value) or re.fullmatch(r"(?:pr\s*)?#([1-9][0-9]*)" if pull_request else r"#?([1-9][0-9]*)",value)
 if match is None:raise CommandError("schema_mismatch","query.reference","Use a canonical issue or PR reference.")
 return f"PR #{int(match.group(1))}" if pull_request else f"#{int(match.group(1))}"
def _path(value):
 if not isinstance(value,str) or not value or "\\" in value:raise CommandError("schema_mismatch","query.paths","Use a repository-relative path clue.")
 path=Path(value)
 if path.is_absolute() or any(part in ("",".","..") for part in path.parts):raise CommandError("schema_mismatch","query.paths","Use a clean repository-relative path clue.")
 normalized=path.as_posix()
 if normalized in (".trellis/workspace",".trellis/.runtime") or normalized.startswith((".trellis/workspace/",".trellis/.runtime/")):raise CommandError("schema_mismatch","query.paths","Do not query protected workspace or runtime state.")
 return normalized
def _tokens(values):
 result=set()
 for value in values:
  split=re.sub(r"(?<=[a-z0-9])(?=[A-Z])"," ",unicodedata.normalize("NFKC",value)).casefold()
  result.update(token for token in re.findall(r"[^\W_]+",split,flags=re.UNICODE) if len(token)>=2 or token.isdigit())
 return _sort(result)
def canonical_query(raw):
 if not isinstance(raw,dict) or set(raw)-set(QUERY_KINDS):raise CommandError("schema_mismatch","query","Use only declared context query keys.")
 out={};token_inputs=[]
 for kind in QUERY_KINDS:
  values=raw.get(kind,[])
  if not isinstance(values,list):raise CommandError("schema_mismatch",f"query.{kind}","Use an array of context clues.")
  normalized=[]
  for value in values:
   if kind=="issue_refs":normalized.append(_reference(value,False))
   elif kind=="pr_refs":normalized.append(_reference(value,True))
   elif kind=="paths":normalized.append(_path(value))
   else:normalized.append(_text(value,f"query.{kind}"))
   if kind not in ("issue_refs","pr_refs"):token_inputs.append(str(value))
  out[kind]=_sort(normalized)
 if not any(out[kind] for kind in QUERY_KINDS):raise CommandError("schema_mismatch","query","Provide at least one context clue.")
 out["tokens"]=_tokens(token_inputs);out["query_sha256"]=digest(out);return out
def _valid_index(repo,index):
 schema_path=repo/".trellis/guru-team/schemas/finish-summary.schema.json"
 try:schema=json.loads(schema_path.read_text())
 except Exception:return False
 try:
  from jsonschema import Draft202012Validator
 except ImportError as exc:raise CommandError("runtime_dependency_missing","history_preview","Install the Python jsonschema dependency.") from exc
 index_schema={"$schema":schema.get("$schema"),"$defs":schema.get("$defs",{}),**schema["properties"]["index"]}
 return not any(Draft202012Validator(index_schema).iter_errors(index))
def _score(query,index):
 terms=index["search_terms"];retrieval=" ".join(unicodedata.normalize("NFKC",index["retrieval_text"]).casefold().split());retrieval_tokens=set(_tokens([index["retrieval_text"]]));normalized=set(retrieval_tokens)
 for values in terms.values():
  if isinstance(values,list):normalized.update(_text(value,"index.search_terms") for value in values if isinstance(value,str))
 matched={};exact=0;exact_count=0
 for kind in QUERY_KINDS:
  if kind=="paths":matches=[value for value in query[kind] if value in set(terms.get(kind,[]))]
  elif kind=="terms":matches=[value for value in query[kind] if value in normalized]
  elif kind=="queries":matches=[value for value in query[kind] if value in retrieval]
  else:
   candidates={value if kind in ("issue_refs","pr_refs") else _text(value,f"index.{kind}") for value in terms.get(kind,[]) if isinstance(value,str)}
   matches=[value for value in query[kind] if value in candidates]
  matches=_sort(matches)
  if matches:matched[kind]=matches;exact_count+=len(matches);exact+=EXACT_WEIGHTS[kind]*len(matches)
 token_matches=_sort(set(query["tokens"])&retrieval_tokens)
 if token_matches:matched["tokens"]=token_matches
 token=min(99,len(token_matches));return {"total":exact+token,"exact":exact,"token":token,"exact_match_count":exact_count,"token_match_count":len(token_matches)},matched
def preview(repo,raw,limit):
 if limit!=20:raise CommandError("invalid_arguments","limit","Use the fixed history preview limit 20.")
 q=canonical_query(raw);manifest=[];candidates=[];archive=repo/".trellis/tasks/archive"
 if archive.exists() and not archive.is_dir():raise CommandError("unsafe_path","archive","Archived task root must be a directory.")
 paths=sorted(archive.glob("**/finish-summary.json"),key=lambda path:path.relative_to(repo).as_posix().encode("utf-8")) if archive.exists() else []
 for path in paths:
  relative=path.relative_to(repo).as_posix();error=None;index=None
  if path.is_symlink() or not path.is_file():error="not_regular_file"
  else:
   try:payload=json.loads(path.read_text(encoding="utf-8"))
   except Exception:error="invalid_json"
   else:
    if not isinstance(payload,dict) or "index" not in payload:error="missing_index"
    else:
     index=payload["index"]
     if not _valid_index(repo,index):error="invalid_index_shape"
  if error:manifest.append({"path":relative,"status":"invalid","error_code":error});continue
  index_sha=digest(index);manifest.append({"path":relative,"status":"valid","index_sha256":index_sha});score,matched=_score(q,index)
  if score["total"]>0:
   identity={"finish_summary_path":relative,"index_sha256":index_sha}
   candidates.append({"candidate_id":digest(identity),**identity,"score":score,"matched_clues":matched,"index_projection":{key:copy.deepcopy(index[key]) for key in ("problem","outcome","changed_behavior","affected_surfaces","contract_changes","search_terms")}})
 candidates.sort(key=lambda row:(-row["score"]["total"],-row["score"]["exact_match_count"],-row["score"]["token_match_count"],row["finish_summary_path"].encode("utf-8")));candidates=candidates[:limit];invalid=[copy.deepcopy(row) for row in manifest if row["status"]=="invalid"]
 out={"algorithm_id":"guru-context-history-score-1.0","canonical_query":q,"query_sha256":q["query_sha256"],"archive_manifest_sha256":digest(manifest),"limit":limit,"manifest":manifest,"candidates":candidates,"invalid":invalid};out["preview_sha256"]=digest({key:out[key] for key in ("algorithm_id","query_sha256","archive_manifest_sha256","limit","candidates","invalid")});return out
def identity(v):
 base=v["base_evidence"];live=v["live_change"];hp=v["history_preview"];out={"query_sha256":v["canonical_query"]["query_sha256"],"archive_manifest_sha256":hp["archive_manifest_sha256"],"base_head":base["base_head"],"base_sync_facts_sha256":base["sync_result"]["facts_sha256"],"post_sync_resolution_sha256":base["post_sync_resolution_sha256"],"live_change_sha256":live["facts_sha256"]};out["payload_sha256"]=digest({k:v[k] for k in v if k!="result_identity"});out["result_sha256"]=digest(out);return out
def validate(package_root,v):validate_json(v,package_root/"schemas/change-context-owner-result.schema.json","owner_result");return v
def active_task(repo,value):
 p=(repo/str(value or "")).resolve();tasks=(repo/".trellis/tasks").resolve()
 if not p.is_dir() or p.is_symlink() or not p.is_relative_to(tasks):raise CommandError("unsafe_path","active_task","Use one active task below .trellis/tasks.")
 try:task=json.loads((p/"task.json").read_text())
 except Exception as exc:raise CommandError("invalid_json","active_task","Provide a valid active task.json.") from exc
 branch=subprocess.run(["git","rev-parse","--abbrev-ref","HEAD"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip()
 if task.get("status")!="in_progress" or task.get("branch")!=branch:raise CommandError("stale_identity","active_task","Use the current in-progress task branch.",3)
 return p,task
def recovery_path(repo,task_dir):return repo/".trellis/.runtime/guru-team/owner-checkpoints"/task_dir.name/"change-context-recovery.json"
def consume_recovery(path):
 path.unlink(missing_ok=True)
 try:path.parent.rmdir()
 except OSError:pass
def recovery_projection(repo,task_dir,task,payload,continuation):
 gate=payload.get("ai_review_gate") if isinstance(payload.get("ai_review_gate"),dict) else {}
 value={"schema_version":"1.0","skill_id":"guru-discover-change-context","task_ref":task_dir.resolve().relative_to(repo.resolve()).as_posix(),"task_id":task.get("id"),"mode":payload.get("mode"),"continuation_id":continuation,"requested_exit":payload.get("typed_exit"),"gate_status":gate.get("status"),"reviewed_scope":copy.deepcopy(gate.get("reviewed_scope")),"load_bearing_conclusions":copy.deepcopy(gate.get("load_bearing_conclusions")),"reason":gate.get("reason")}
 return value
def record_recovery(package_root,repo,task_dir,task,payload,continuation):
 value=recovery_projection(repo,task_dir,task,payload,continuation);validate_json(value,package_root/"schemas/change-context-recovery.schema.json","recovery");path=recovery_path(repo,task_dir)
 if path.is_symlink() or (path.exists() and not path.is_file()):raise CommandError("unsafe_path","recovery","Use a regular owner checkpoint path.")
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+"\n");return path
def check_recovery(package_root,repo,task_dir,task,payload,continuation):
 path=recovery_path(repo,task_dir)
 try:value=json.loads(path.read_text())
 except Exception as exc:raise CommandError("stale_identity","recovery","Rerun the interrupted context owner.",3) from exc
 try:validate_json(value,package_root/"schemas/change-context-recovery.schema.json","recovery")
 except Exception:
  consume_recovery(path);raise
 if value!=recovery_projection(repo,task_dir,task,payload,continuation):consume_recovery(path);raise CommandError("stale_identity","recovery","Rerun the interrupted context owner.",3)
 return path
