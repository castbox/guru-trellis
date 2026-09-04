from __future__ import annotations
import argparse
from pathlib import Path
from common import load,parse,root,validate
from runtime.io import CommandError
from runtime.schema import validate_json
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--invocation",required=True);a=parse(p,argv);repo=root(package_root,a.root);e=load(repo,package_root,a.invocation,"invocation");result=e.get("result") or e.get("owner_result")
 if not isinstance(result,dict):raise CommandError("invalid_arguments","invocation.result","Provide the checked executor result.")
 validate(package_root,result,"task-workspace-result.schema.json","result")
 if result.get("checker",{}).get("status")!="passed":raise CommandError("stale_identity","result.checker","Check the executor result before projection.",3)
 exit_id=result["typed_exit"];out={"exit_id":exit_id}
 if exit_id=="refresh_review":out.update({"mode":result["mode"],"base_branch":e.get("base_branch") or "main"})
 if exit_id=="invalid_task_state":out.update({"reason_code":"invalid_task_state"})
 schema={"created":"public-created-output.schema.json","refresh_review":"public-refresh-review-output.schema.json","blocked":"public-blocked-output.schema.json","invalid_task_state":"public-invalid-task-state-output.schema.json"}[exit_id];validate_json(out,package_root/"schemas"/schema,"stdout");return out
