from __future__ import annotations
import argparse
from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from common import clean, digest, head, repo

def run(package_root, command, argv):
    p=argparse.ArgumentParser(add_help=False); p.add_argument("--json",action="store_true"); p.add_argument("--root"); p.add_argument("--mode",required=True,choices=("workflow","standalone")); p.add_argument("--result-json"); p.add_argument("--expected-resolution-sha256"); p.add_argument("--record-skipped")
    try:a=p.parse_args(argv)
    except SystemExit as exc: raise CommandError("invalid_arguments","arguments","Use the exact command help contract.") from exc
    if a.record_skipped:
        if a.mode!="workflow" or a.record_skipped!="original-request-route" or a.result_json or a.expected_resolution_sha256: raise CommandError("invalid_arguments","record_skipped","Use only the declared workflow skipped route.")
        value={"schema_version":"1.0","skill_id":"guru-sync-base","status":"skipped","mode":"workflow","route_id":a.record_skipped}; value["facts_sha256"]=digest(value); return value
    if not a.result_json or not a.expected_resolution_sha256: raise CommandError("invalid_arguments","result_json","Provide result JSON and its expected resolution digest.")
    value=read_json(a.result_json,"result_json"); validate_json(value,package_root/"schemas/base-sync-result.schema.json","result_json")
    if value["resolution"]["resolution_sha256"]!=a.expected_resolution_sha256: raise CommandError("stale_identity","expected_resolution_sha256","Resolve again from current Git state.",3)
    unsigned=dict(value); actual=unsigned.pop("facts_sha256")
    root=repo(a.root); expected=value["git"]["remote_head_after"]
    if digest(unsigned)!=actual or not clean(root) or head(root)!=expected or head(root,value["git"]["local_ref"])!=expected or head(root,value["git"]["remote_ref"])!=expected: raise CommandError("stale_identity","result_json","Rerun synchronization and validation from current Git state.",3)
    return {"schema_version":"1.0","skill_id":"guru-sync-base","status":"validated","mode":a.mode,"post_sync_resolution_sha256":value["post_sync_resolution_sha256"],"facts_sha256":actual,"selected_base":value["resolution"]["selected_base"],"head":expected}
