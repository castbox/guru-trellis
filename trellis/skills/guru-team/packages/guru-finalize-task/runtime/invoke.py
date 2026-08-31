from __future__ import annotations
import argparse, importlib.util
from pathlib import Path
from common import call_owner, parse_arguments
def _o(r):
 s=importlib.util.spec_from_file_location("finalize_owner",r/"runtime/owner.py");m=importlib.util.module_from_spec(s);assert s and s.loader;s.loader.exec_module(m);return m
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--input",required=True);p.add_argument("--owner-result",required=True)
 for x in ("repo","base_branch","remote","title","task_name"): p.add_argument("--"+x.replace("_","-"))
 p.add_argument("--validation",action="append")
 a=parse_arguments(p,argv);o=_o(package_root)
 def invoke_owner():
  root=o.repo_root(Path(a.root or "."));public,_=o.finalization_public_input(root,a.input);owner,path=o.finalization_gate_input(root,public,a.owner_result)
  checked,plan=o.check_finalization_gate_result(root,a,public,owner,path);exit_id=str((checked.get("route")or{}).get("typed_exit")or"");payload=(checked.get("route")or{}).get("output")
  if payload==o.FINALIZATION_EXECUTOR_OUTPUT_MARKER:
   closeout=plan.get("plan");pr=plan.get("published_pr")
   if not isinstance(closeout,dict) or not isinstance(pr,dict): raise o.WorkflowError("Finalization terminal output is not materializable.",exit_code=2)
   payload=o.finalization_gate_with_ready_for_merge_output(root,plan["task_dir"],checked,closeout,pr)["route"]["output"]
  schema,_=o.stage0_output_contract(o.FINALIZE_TASK_SKILL_ID,o.finalization_package_root(root),o.finalization_interface(root),exit_id)
  errors=o.skill_json_schema_validation_errors(payload,schema,f"finalization output {exit_id}")
  if errors: raise o.WorkflowError("Finalization typed output invalid.",exit_code=2,payload={"errors":errors})
  if exit_id=="ready_for_merge": o.finalization_retire_current_state(root,plan["task_dir"])
  return payload
 return call_owner(o,invoke_owner,public=True)
