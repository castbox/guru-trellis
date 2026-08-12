from __future__ import annotations
import argparse, importlib.util
from pathlib import Path
from common import call_owner, parse_arguments
def _owner(root):
    spec=importlib.util.spec_from_file_location("publication_owner",root/"runtime/owner.py"); module=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(module); return module
def run(package_root: Path, command: dict, argv: list[str])->dict:
    p=argparse.ArgumentParser(add_help=False); p.add_argument("--root"); p.add_argument("--input",required=True); p.add_argument("--owner-result",required=True)
    a=parse_arguments(p, argv); o=_owner(package_root)

    def invoke_owner() -> dict:
        root=o.repo_root(Path(a.root or ".")); public=o.read_json(Path(a.input)) if a.input!="-" else o.skill_json_loads(__import__("sys").stdin.read(),"public input")
        owner=o.read_json(Path(a.owner_result)); task=o.resolve_task_dir(root,public.get("task_ref")); errors=o.task_publication_check_errors(root,task,owner)
        if errors: raise o.WorkflowError("Publication owner result failed objective checking.",exit_code=2,payload={"errors":errors})
        exit_id=str((owner.get("route") or {}).get("typed_exit") or ""); payload={"exit_id":exit_id}
        if exit_id=="ready": payload.update({"task_ref":owner["task_ref"],"branch_review_commit":owner["branch_review_commit"],"pr_payload":owner["pr_payload"]})
        elif exit_id=="revise_metadata": payload["task_ref"]=owner["task_ref"]
        elif exit_id=="return_to_task_work": payload["task_ref"]=owner["task_ref"]
        else: raise o.WorkflowError("Publication typed exit is unknown.",exit_code=2)
        return payload

    return call_owner(o, invoke_owner)
