from __future__ import annotations
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json
VOCAB=("可以","允许","建议","推荐","可选","尽量","尽可能","最好","应该","应当","原则上","一般","通常","视情况","根据情况","根据需要","按需","必要时","如有需要","需要时","适当","适当时","合理","合理时","类似","相关","相应","等","等等","之类","一些","若干","部分","至少","默认")
CONTRACT_WORDING_REVIEW_DIMENSIONS=("complete_profile_scope","all_hits_classified","zero_unchecked_hits","product_semantics_preserved","retained_reasons_sufficient","zero_hits_not_requirement_review")
CONTRACT_WORDING_PLANNING_REVIEW_DIMENSIONS=("no_requirement_weakening","source_issue_semantics_preserved","conditional_paths_have_conditions","no_parallel_implementation_paths","gates_have_machine_verifiable_conditions","acceptance_criteria_are_deterministic","external_quotes_are_labeled_non_contract")
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def change_request_target_content_sha256(sc):
 items=sc.get("items") if isinstance(sc,dict) else None
 title=[x for x in items or [] if isinstance(x,dict) and x.get("field")=="title"]
 body=[x for x in items or [] if isinstance(x,dict) and x.get("field")=="body"]
 if len(title)!=1 or len(body)!=1:raise CommandError("stale_identity","owner_result.scope","Rerun wording against one current title and body.",3)
 return digest({"title_sha256":title[0]["content_sha256"],"body_sha256":body[0]["content_sha256"]})
def parse(p,argv):
 p.add_argument("--json",action="store_true")
 try:return p.parse_args(argv)
 except SystemExit as exc:raise CommandError("invalid_arguments","arguments","Use exact help.") from exc
def root(package_root,value=None):
 r=Path(value or ".").resolve()
 if not r.is_dir():raise CommandError("unsafe_path","root","Use a repository root.")
 return r
def load(repo,package_root,value,field):
 if value=="-":raw=sys.stdin.read()
 else:
  q=Path(str(value or ""));choices=[q] if q.is_absolute() else [repo/q,package_root/q];q=next((x for x in choices if x.is_file() and not x.is_symlink()),None)
  if q is None:raise CommandError("unsafe_path",field,"Use a safe JSON file.")
  raw=q.read_text()
 try:v=json.loads(raw)
 except Exception as exc:raise CommandError("invalid_json",field,"Provide one JSON object.") from exc
 if not isinstance(v,dict):raise CommandError("invalid_json",field,"Provide one JSON object.")
 return v
def file_item(repo,path):
 q=(repo/path).resolve()
 if not q.is_relative_to(repo.resolve()) or not q.is_file() or q.is_symlink() or q.suffix!=".md":raise CommandError("unsafe_path","path","Use regular Markdown paths inside the repository.")
 data=q.read_bytes();return {"kind":"markdown_file","id":"file:"+path,"path":path,"size_bytes":len(data),"content_sha256":hashlib.sha256(data).hexdigest()}
def scope(repo,profile,task=None,paths=None,change=None):
 if profile=="planning_artifacts":
  td=(repo/str(task)).resolve();items=[file_item(repo,td.relative_to(repo).as_posix()+"/"+n) for n in ("prd.md","design.md","implement.md")];identity="planning_artifacts:"+td.relative_to(repo).as_posix()
 elif profile=="explicit_paths":
  items=[file_item(repo,x) for x in paths or []];identity="explicit_paths:"+digest([x["path"] for x in items])
 elif profile=="change_request":
  if not isinstance(change,dict):raise CommandError("schema_mismatch","change_request","Provide current change request fields.")
  items=[]
  for field in ("title","body"):
   text=str(change.get(field) or "");items.append({"kind":"change_request_field","id":field+":"+str(change.get("identity") or change.get("url") or "request"),"source_kind":change.get("source_kind","draft"),"source_identity":str(change.get("identity") or change.get("url") or "request"),"field":field,"author":None,"updated_at":change.get("updated_at"),"selection_reason":None,"size_bytes":len(text.encode()),"content_sha256":hashlib.sha256(text.encode()).hexdigest()})
  identity="change_request:"+str(change.get("identity") or change.get("url") or "request")
 else:raise CommandError("invalid_arguments","profile","Use one declared profile.")
 out={"identity":identity,"items":items};out["scope_sha256"]=digest(out);return out
def scan(scope,contents):
 hits=[]
 for item in scope["items"]:
  text=contents[item["id"]]
  for line_no,line in enumerate(text.splitlines(),1):
   for term in VOCAB:
    start=0
    while (pos:=line.find(term,start))>=0:
     hit={"scope_item_id":item["id"],"locator":item.get("path") or item["id"],"line":line_no,"term":term,"text":line,"content_sha256":item["content_sha256"]};hit["hit_id"]=digest(hit);hits.append(hit);start=pos+len(term)
 out={"hits":hits};out["scan_sha256"]=digest(out);return out
def validate_result(package_root,v):validate_json(v,package_root/"schemas/contract-wording-review.schema.json","result");return v
def validation_receipt(v):
 value={"schema_version":"1.0","skill_id":"guru-review-contract-wording","operation":"check-contract-wording-review","result_sha256":v["facts_sha256"],"prerequisite_sha256":digest({"profile":v["profile"],"mode":v["mode"]}),"snapshot_sha256":digest({"scope":v["scope"],"scan":v["scan"]})};value["receipt_sha256"]=digest(value);return value
def check_receipt(v,receipt):
 if receipt!=validation_receipt(v):raise CommandError("stale_identity","validation_receipt","Run the wording checker for this exact result and snapshot.",3)
def live_issue_source(change):
 if not isinstance(change,dict) or change.get("source_kind")!="issue":return change
 locator=str(change.get("identity") or change.get("url") or "");match=re.fullmatch(r"https://github\.com/([^/]+/[^/]+)/issues/([1-9][0-9]*)",locator)
 if not match:raise CommandError("schema_mismatch","change_request.identity","Use a canonical GitHub issue URL.")
 proc=subprocess.run(["gh","issue","view",match.group(2),"--repo",match.group(1),"--json","number,url,state,title,body,updatedAt"],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if proc.returncode:raise CommandError("stale_identity","change_request",proc.stderr.strip() or "Reread the current issue.",3)
 try:live=json.loads(proc.stdout)
 except Exception as exc:raise CommandError("invalid_json","change_request","GitHub returned invalid JSON.") from exc
 if str(live.get("state") or "").lower()!="open" or live.get("url")!=locator or live.get("title")!=change.get("title") or live.get("body")!=change.get("body") or live.get("updatedAt")!=change.get("updated_at"):raise CommandError("stale_identity","change_request","Issue content changed; refresh context.",3)
 return change

# Private owner-staging API used only by the installed eval/test adapter.
def contract_wording_build_scope(repo,profile,mode,*,task_dir=None,explicit_paths=None,change_request_input=None):
 if profile=="planning_artifacts":
  if mode!="workflow" or task_dir is None or explicit_paths or change_request_input:raise CommandError("invalid_arguments","profile","Use the fixed workflow planning-artifacts scope.")
  task_path=Path(task_dir).resolve();task=task_path.relative_to(Path(repo).resolve()).as_posix();sc=scope(Path(repo),profile,task=task)
  contents={item["id"]:(Path(repo)/item["path"]).read_text() for item in sc["items"]};return sc,contents
 if profile=="explicit_paths":
  if mode!="standalone" or task_dir is not None or change_request_input:raise CommandError("invalid_arguments","profile","Use the fixed standalone explicit-paths scope.")
  sc=scope(Path(repo),profile,paths=explicit_paths);contents={item["id"]:(Path(repo)/item["path"]).read_text() for item in sc["items"]};return sc,contents
 if profile!="change_request" or task_dir is not None or explicit_paths or not change_request_input:raise CommandError("invalid_arguments","profile","Use one declared fixed wording scope.")
 change=load(Path(repo),Path(repo),change_request_input,"change_request")
 if change.get("kind")=="draft":change={"source_kind":"draft","identity":str(change.get("draft_id") or "draft"),"title":change.get("title"),"body":change.get("body"),"updated_at":None}
 elif change.get("kind")=="issue":
  proc=subprocess.run(["gh","issue","view",str(change.get("number") or ""),"--repo",str(change.get("repo") or ""),"--json","number,url,state,title,body,updatedAt"],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  if proc.returncode:raise CommandError("stale_identity","change_request",proc.stderr.strip() or "Reread the current issue.",3)
  try:live=json.loads(proc.stdout)
  except Exception as exc:raise CommandError("invalid_json","change_request","GitHub returned invalid JSON.") from exc
  change={"source_kind":"issue","identity":live.get("url"),"title":live.get("title"),"body":live.get("body"),"updated_at":live.get("updatedAt")}
 sc=scope(Path(repo),profile,change=change);contents={item["id"]:str(change[item["field"]]) for item in sc["items"]};return sc,contents

def scan_contract_wording(sc,contents):return scan(sc,contents)

def contract_wording_derive_result(profile,mode,sc,sn,authored):
 semantic=authored.get("semantic_review") if isinstance(authored,dict) else None
 if not isinstance(semantic,dict):raise CommandError("schema_mismatch","semantic_review","Provide the reviewed semantic result.")
 classes=semantic.get("classifications",[]);by={row.get("hit_id"):row for row in classes if isinstance(row,dict)}
 unchecked=sorted(hit["hit_id"] for hit in sn["hits"] if hit["hit_id"] not in by or by[hit["hit_id"]].get("classification")=="contract_violation")
 value={"schema_version":"1.0","skill_id":"guru-review-contract-wording","generated_at":authored.get("generated_at"),"profile":profile,"mode":mode,"vocabulary_version":"contract-wording-v2","classification_version":"contract-wording-classifications-v1","scope":sc,"scan":sn,"semantic_review":{"revisions":semantic.get("revisions",[]),"classifications":classes,"unchecked_normative_hits":unchecked,"ai_review_gate":semantic.get("ai_review_gate")},"typed_exit":authored.get("typed_exit")}
 value["facts_sha256"]=digest(value);return value
