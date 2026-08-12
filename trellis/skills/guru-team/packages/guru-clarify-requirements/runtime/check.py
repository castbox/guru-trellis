from __future__ import annotations
import argparse
from runtime.io import CommandError,read_json
from common import validate_owner
def run(package_root,command,argv):
    p=argparse.ArgumentParser(add_help=False);p.add_argument("--json",action="store_true");p.add_argument("--root");p.add_argument("--input",required=True);p.add_argument("--task");p.add_argument("--expected-result-sha256")
    try:a=p.parse_args(argv)
    except SystemExit as exc: raise CommandError("invalid_arguments","arguments","Use the exact command help contract.") from exc
    value=validate_owner(package_root,read_json(a.input,"input")); identity=value["content_identity"]
    if a.expected_result_sha256 and a.expected_result_sha256!=identity["result_sha256"]: raise CommandError("stale_identity","expected_result_sha256","Reread current authority and repeat the semantic round.",3)
    return {"status":"passed","typed_exit":value["typed_exit"],"target_sha256":identity["target_sha256"],"disposition_sha256":identity["disposition_sha256"],"context_sha256":identity["context_sha256"],"scope_sha256":identity["scope_sha256"],"action_sha256":identity["action_sha256"],"result_sha256":identity["result_sha256"]}
