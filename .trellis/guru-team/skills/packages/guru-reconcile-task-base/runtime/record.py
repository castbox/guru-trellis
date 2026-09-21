from __future__ import annotations
import argparse, copy
from pathlib import Path
from common import PRE_REVIEW_PROFILES, POST_REVIEW_PROFILES, checkpoint_path, digest, objective_identity, operation_pair, output_for, parse, read_json, repo_root, validate_json, validate_public, validate_result
from runtime.io import CommandError

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--skill-input",required=True); parser.add_argument("--semantic-review-file",required=True); parser.add_argument("--typed-exit",required=True); parser.add_argument("--reconciliation-result")
    args=parse(parser,argv); repo=repo_root(args.root); public=read_json(repo,package_root,args.skill_input,"skill_input"); validate_public(package_root,public)
    gate=read_json(repo,package_root,args.semantic_review_file,"semantic_review"); exit_id=args.typed_exit
    if gate.get("typed_exit") != exit_id: raise CommandError("schema_mismatch","semantic_gate.typed_exit","Match the completed AI gate.")
    _,old_base,new_base=operation_pair(repo,public)
    operation={**public,"old_base_head":old_base,"new_base_head":new_base}
    receipt=None
    if args.reconciliation_result:
        receipt=read_json(repo,package_root,args.reconciliation_result,"reconciliation_result"); validate_json(receipt,package_root/"schemas/reconciliation-result.schema.json","reconciliation_result")
    committed_reconciliation=(exit_id=="review_continuity_required" or (exit_id=="reconciled" and public["profile"] in PRE_REVIEW_PROFILES))
    if committed_reconciliation:
        if receipt is None:
            raise CommandError("schema_mismatch","reconciliation_result","This route requires the checked local reconciliation result.")
        if any(receipt[key] != value for key,value in {
            "profile":public["profile"],"task_ref":public["task_ref"],"prior_task_head":public["task_head"],"old_base_head":old_base,"new_base_head":new_base,"resume_target":public["resume_target"],"candidate_tree_sha256":gate.get("route_payload",{}).get("candidate_tree_sha256")}.items()):
            raise CommandError("stale_identity","reconciliation_result","Use the result for this exact reviewed pair.",3)
        if public["profile"] in POST_REVIEW_PROFILES and receipt.get("branch_review_commit") != public["branch_review_commit"]:
            raise CommandError("stale_identity","reconciliation_result","Use the result for the exact prior full-review identity.",3)
        current_head=receipt["reconciled_task_head"]
    else:
        if receipt is not None:
            raise CommandError("schema_mismatch","reconciliation_result","Only committed reconciliation routes consume a reconciliation result.")
        current_head=public["task_head"]
    objective_identity(repo,public,expected_head=current_head)
    output=output_for(operation,gate,exit_id,task_head=current_head); validate_json(output,package_root/f"schemas/public-{exit_id.replace('_','-')}-output.schema.json","typed_output")
    result={"schema_version":"2.0","skill_id":"guru-reconcile-task-base",**{k:copy.deepcopy(v) for k,v in public.items() if k not in {"task_head","old_base_head","new_base_head"}},"prior_task_head":public["task_head"],"task_head":current_head,"old_base_head":old_base,"new_base_head":new_base,"semantic_gate":gate,"reconciliation_result":receipt,"typed_output":output}
    result["facts_sha256"]=digest(result); validate_result(package_root,repo,result,public)
    target=checkpoint_path(repo,public["task_ref"],allow_planning=public["profile"]=="post_plan"); target.parent.mkdir(parents=True,exist_ok=True); target.write_text(__import__('json').dumps(result,ensure_ascii=False,indent=2)+"\n")
    return result
