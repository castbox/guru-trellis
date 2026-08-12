from __future__ import annotations
import argparse,copy
from runtime.io import CommandError,read_json
from runtime.schema import validate_json
from common import validate_owner
def run(package_root,command,argv):
    p=argparse.ArgumentParser(add_help=False);p.add_argument("--json",action="store_true");p.add_argument("--invocation",required=True)
    try:a=p.parse_args(argv)
    except SystemExit as exc: raise CommandError("invalid_arguments","arguments","Use --invocation with one JSON object.") from exc
    envelope=read_json(a.invocation,"invocation"); owner=validate_owner(package_root,envelope.get("owner_result",{})); exit_id=owner["typed_exit"]
    output=copy.deepcopy(envelope.get("typed_output"))
    if not isinstance(output,dict) or output.get("exit_id")!=exit_id: raise CommandError("semantic_result_invalid","invocation.typed_output","Provide the AI-reviewed typed output for the checked owner result.",3)
    validate_json(output,next(package_root.glob(f"schemas/public-{exit_id.replace('_','-')}-output*.schema.json")),"typed_output")
    return output
