from __future__ import annotations
import argparse
from pathlib import Path
from common import checkpoint_path, parse, read_json, repo_root, validate_json, validate_result
from runtime.io import CommandError

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--invocation",required=True)
    args=parse(parser,argv); repo=repo_root(args.root); envelope=read_json(repo,package_root,args.invocation,"invocation"); validate_json(envelope,package_root/"schemas/invocation-envelope.schema.json","invocation")
    public=envelope["public_input"]; result=envelope["owner_result"]; validate_result(package_root,repo,result,public); output=result["typed_output"]
    checkpoint=checkpoint_path(repo,public["task_ref"],allow_planning=public["profile"]=="post_plan")
    if not checkpoint.is_file():
        raise CommandError("stale_identity","checkpoint","Record one current owner result before invoking it once.",3)
    current=read_json(repo,package_root,str(checkpoint),"checkpoint"); validate_result(package_root,repo,current,public)
    if current["facts_sha256"] != result["facts_sha256"]:
        raise CommandError("stale_identity","checkpoint","Consume only the exact current owner result.",3)
    checkpoint.unlink();
    try: checkpoint.parent.rmdir()
    except OSError: pass
    return output
