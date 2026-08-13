from __future__ import annotations
import argparse
from pathlib import Path
from common import parse, read_json, repo_root, validate_result

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--input",required=True); parser.add_argument("--expected-exit")
    args=parse(parser,argv); repo=repo_root(args.root); result=read_json(repo,package_root,args.input,"input"); validate_result(package_root,repo,result)
    if args.expected_exit and result["typed_output"]["exit_id"] != args.expected_exit:
        from runtime.io import CommandError
        raise CommandError("stale_identity","typed_exit","Use the current selected exit.",3)
    return {"status":"ok","task_ref":result["task_ref"],"task_head":result["task_head"],"new_base_head":result["new_base_head"],"typed_exit":result["typed_output"]["exit_id"],"facts_sha256":result["facts_sha256"]}
