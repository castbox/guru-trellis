from __future__ import annotations
import argparse
from pathlib import Path
from common import digest,live_issue_source,load,parse,root,scan,scope,validate_result
from runtime.io import CommandError
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--input",required=True);p.add_argument("--task");p.add_argument("--path",action="append",default=[]);p.add_argument("--change-request-input");p.add_argument("--expected-facts-sha256")
 a=parse(p,argv);repo=root(package_root,a.root);v=validate_result(package_root,load(repo,package_root,a.input,"input"));change=load(repo,package_root,a.change_request_input,"change_request") if a.change_request_input else None;change=live_issue_source(change);sc=scope(repo,v["profile"],a.task,a.path,change);contents={x["id"]:((repo/x["path"]).read_text() if x["kind"]=="markdown_file" else str(change[x["field"]])) for x in sc["items"]};sn=scan(sc,contents);unsigned=dict(v);actual=unsigned.pop("facts_sha256")
 if sc!=v["scope"] or sn!=v["scan"] or digest(unsigned)!=actual:raise CommandError("stale_identity","result","Rerun wording review on current content.",3)
 if a.expected_facts_sha256 and a.expected_facts_sha256!=actual:raise CommandError("stale_identity","expected_facts_sha256","Use current facts digest.",3)
 return {"status":"passed","typed_exit":v["typed_exit"],"facts_sha256":actual}
