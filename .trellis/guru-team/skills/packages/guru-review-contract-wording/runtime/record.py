from __future__ import annotations
import argparse,hashlib
from pathlib import Path
from common import digest,live_issue_source,load,parse,root,scan,scope,validate_result
from runtime.io import CommandError
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--mode",required=True,choices=("workflow","standalone"));p.add_argument("--profile",required=True,choices=("change_request","planning_artifacts","explicit_paths"));p.add_argument("--input");p.add_argument("--task");p.add_argument("--path",action="append",default=[]);p.add_argument("--change-request-input");p.add_argument("--scan-only",action="store_true")
 a=parse(p,argv);repo=root(package_root,a.root);change=load(repo,package_root,a.change_request_input,"change_request") if a.change_request_input else None;change=live_issue_source(change);sc=scope(repo,a.profile,a.task,a.path,change);contents={}
 for item in sc["items"]:
  contents[item["id"]]=(repo/item["path"]).read_text() if item["kind"]=="markdown_file" else str(change[item["field"]])
 sn=scan(sc,contents)
 if a.scan_only:return {"status":"scanned","skill_id":"guru-review-contract-wording","profile":a.profile,"mode":a.mode,"vocabulary_version":"contract-wording-v2","scope":sc,"scan":sn}
 auth=load(repo,package_root,a.input,"input");classes=auth.get("classifications",[]);by={x.get("hit_id"):x for x in classes if isinstance(x,dict)};ids={x["hit_id"] for x in sn["hits"]};unchecked=sorted(x for x in ids if x not in by or by[x].get("classification")=="contract_violation")
 if set(by)!=ids or len(by)!=len(classes):raise CommandError("schema_mismatch","classifications","Classify every current hit exactly once.")
 auth["unchecked_normative_hits"]=unchecked;gate=auth.get("ai_review_gate",{});gate["reviewed_scan_sha256"]=sn["scan_sha256"];exit_id=auth.pop("typed_exit",None) or ("blocked" if unchecked else ("content_changed" if auth.get("revisions") else "pass"))
 if exit_id=="pass" and (unchecked or auth.get("revisions")):raise CommandError("schema_mismatch","typed_exit","Pass requires no revisions or unchecked hits.")
 v={"schema_version":"1.0","skill_id":"guru-review-contract-wording","generated_at":auth.pop("generated_at","1970-01-01T00:00:00Z"),"profile":a.profile,"mode":a.mode,"vocabulary_version":"contract-wording-v2","classification_version":"contract-wording-classifications-v1","scope":sc,"scan":sn,"semantic_review":auth,"typed_exit":exit_id};v["facts_sha256"]=digest(v);return validate_result(package_root,v)
