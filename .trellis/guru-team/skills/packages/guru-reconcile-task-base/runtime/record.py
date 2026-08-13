from __future__ import annotations
import argparse, copy
from pathlib import Path
from common import checkpoint_path, digest, objective_identity, output_for, parse, read_json, repo_root, validate_json, validate_public, validate_result

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--skill-input",required=True); parser.add_argument("--semantic-review-file",required=True); parser.add_argument("--typed-exit",required=True)
    args=parse(parser,argv); repo=repo_root(args.root); public=read_json(repo,package_root,args.skill_input,"skill_input"); validate_public(package_root,public); objective_identity(repo,public)
    gate=read_json(repo,package_root,args.semantic_review_file,"semantic_review"); exit_id=args.typed_exit
    if gate.get("typed_exit") != exit_id: from runtime.io import CommandError; raise CommandError("schema_mismatch","semantic_gate.typed_exit","Match the completed AI gate.")
    output=output_for(public,gate,exit_id); validate_json(output,package_root/f"schemas/public-{exit_id.replace('_','-')}-output.schema.json","typed_output")
    result={"schema_version":"1.0","skill_id":"guru-reconcile-task-base",**{k:copy.deepcopy(v) for k,v in public.items()},"semantic_gate":gate,"typed_output":output}
    result["facts_sha256"]=digest(result); validate_result(package_root,repo,result,public)
    target=checkpoint_path(repo,public["task_ref"],allow_planning=public["profile"]=="post_plan"); target.parent.mkdir(parents=True,exist_ok=True); target.write_text(__import__('json').dumps(result,ensure_ascii=False,indent=2)+"\n")
    return result
