from __future__ import annotations
import argparse
from pathlib import Path
from common import checkpoint,file_set,load,parse,rel,root,store,task
from runtime.schema import validate_json
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--task");p.add_argument("--input",required=True);p.add_argument("--dry-run",action="store_true")
 a=parse(p,argv);repo=root(package_root,a.root);td=task(repo,a.task);auth=load(repo,package_root,a.input,"input")
 if auth.get("schema_version")=="3.0":value=auth
 else:
  expected={"mode","authority_refs","docs_ssot_plan","semantic_review","typed_exit","consumer","reason"}
  if set(auth)!=expected:raise __import__("runtime.io",fromlist=["CommandError"]).CommandError("schema_mismatch","input","Provide the exact planning semantic result.")
  paths=[rel(repo,td/name) for name in ("prd.md","design.md","implement.md")]
  if any(not (repo/x).is_file() or (repo/x).is_symlink() or not (repo/x).read_text().strip() for x in paths):raise __import__("runtime.io",fromlist=["CommandError"]).CommandError("stale_identity","planning_paths","Restore all nonempty planning files.",3)
  value={"schema_version":"3.0","skill_id":"guru-approve-task-plan","task_ref":rel(repo,td),"planning_paths":paths,"reviewed_content_sha256":file_set(repo,paths),**auth}
 validate_json(value,package_root/"schemas/planning-approval.schema.json","input")
 path=checkpoint(repo,td,"planning-approval.json")
 if not a.dry_run:store(path,value)
 return {**value,"artifact_path":str(path),"dry_run":a.dry_run}
