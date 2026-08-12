from __future__ import annotations
import argparse, subprocess
from pathlib import Path
from common import checkpoint,content_identity,dirty_paths,git,load,parse,rel,root,task
from runtime.io import CommandError
from runtime.schema import validate_json
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--task")
 a=parse(p,argv);repo=root(package_root,a.root);td=task(repo,a.task);path=checkpoint(repo,td,"phase2-check.json");value=load(repo,package_root,str(path),"artifact");validate_json(value,package_root/"schemas/phase2-check.schema.json","artifact")
 if value["task_ref"]!=rel(repo,td) or value["reviewed_content_sha256"]!=content_identity(repo) or not set(dirty_paths(repo)).issubset(value["reviewed_paths"]):raise CommandError("stale_identity","artifact","Rerun Phase 2 against current content.",3)
 if subprocess.run(["git","merge-base","--is-ancestor",value["phase2_capture_commit"],"HEAD"],cwd=repo).returncode:raise CommandError("stale_identity","phase2_capture_commit","Rerun Phase 2 on current history.",3)
 return {"status":"ok","artifact_path":str(path),"task_dir":str(td),"head":git(repo,"rev-parse","HEAD"),"phase2_capture_commit":value["phase2_capture_commit"],"typed_exit":value["typed_exit"],"route":value["route"],"consumer":value["consumer"]}
