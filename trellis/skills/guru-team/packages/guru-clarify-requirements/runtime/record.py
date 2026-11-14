from __future__ import annotations
import argparse
from runtime.io import CommandError,read_json
from common import derive_owner
def run(package_root,command,argv):
    p=argparse.ArgumentParser(add_help=False);p.add_argument("--json",action="store_true");p.add_argument("--root");p.add_argument("--mode",required=True,choices=("workflow","standalone"));p.add_argument("--input",required=True);p.add_argument("--task")
    try:a=p.parse_args(argv)
    except SystemExit as exc: raise CommandError("invalid_arguments","arguments","Use the exact command help contract.") from exc
    payload=read_json(a.input,"input")
    if payload.get("public_input",{}).get("profile")=="issue_readiness_supplement":
        from issue_review import execute
        return execute(package_root,{"public_input":payload["public_input"],"owner_result":payload},"record")
    value=derive_owner(package_root,payload,authoring=True)
    if value.get("mode")!=a.mode: raise CommandError("semantic_result_invalid","input.mode","Match the reviewed mode to the recorder mode.",3)
    return value
