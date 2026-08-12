from __future__ import annotations
import argparse
from pathlib import Path
from common import checkpoint,content_identity,dirty_paths,git,load,parse,rel,root,store,task
from runtime.io import CommandError
from runtime.schema import validate_json
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--task");p.add_argument("--input",required=True);p.add_argument("--dry-run",action="store_true")
 a=parse(p,argv);repo=root(package_root,a.root);td=task(repo,a.task);auth=load(repo,package_root,a.input,"input")
 if auth.get("schema_version")=="4.0":value=auth
 else:
  expected={"mode","reviewed_paths","validation","docs_ssot","semantic_review","typed_exit","route","reason","consumer"}
  if set(auth)!=expected:raise CommandError("schema_mismatch","input","Provide the exact Phase 2 semantic result.")
  paths=sorted(auth["reviewed_paths"])
  dirty=dirty_paths(repo)
  if not set(dirty).issubset(paths):raise CommandError("stale_identity","reviewed_paths","Review every current dirty path.",3)
  value={"schema_version":"4.0","skill_id":"guru-check-task","task_ref":rel(repo,td),"phase2_capture_commit":git(repo,"rev-parse","HEAD"),"reviewed_content_sha256":content_identity(repo),**auth,"reviewed_paths":paths}
 validate_json(value,package_root/"schemas/phase2-check.schema.json","input");path=checkpoint(repo,td,"phase2-check.json")
 if not a.dry_run:store(path,value)
 return {**value,"artifact_path":str(path),"dry_run":a.dry_run}
