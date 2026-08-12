from __future__ import annotations
import argparse
from pathlib import Path
from common import checkpoint,file_set,load,parse,rel,root,task
from runtime.io import CommandError
from runtime.schema import validate_json
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--task");p.add_argument("--require-exit",choices=("approved","revision_required","clarify_scope","blocked"))
 a=parse(p,argv);repo=root(package_root,a.root);td=task(repo,a.task);path=checkpoint(repo,td,"planning-approval.json");value=load(repo,package_root,str(path),"artifact")
 validate_json(value,package_root/"schemas/planning-approval.schema.json","artifact");paths=[rel(repo,td/name) for name in ("prd.md","design.md","implement.md")]
 if value["task_ref"]!=rel(repo,td) or value["planning_paths"]!=paths or value["reviewed_content_sha256"]!=file_set(repo,paths):raise CommandError("stale_identity","artifact","Rerun planning review from current files.",3)
 if a.require_exit and value["typed_exit"]!=a.require_exit:raise CommandError("stale_identity","typed_exit","Rerun planning for the required exit.",3)
 return {"status":"ok","artifact_path":str(path),"task_dir":str(td),"typed_exit":value["typed_exit"],"consumer":value["consumer"]}
