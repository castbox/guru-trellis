from __future__ import annotations
import argparse
from runtime.io import CommandError
from common import branch, clean, digest, git, head, repo, resolution

def run(package_root, command, argv):
    p=argparse.ArgumentParser(add_help=False); p.add_argument("--json",action="store_true"); p.add_argument("--root"); p.add_argument("--mode",required=True,choices=("workflow","standalone")); g=p.add_mutually_exclusive_group(required=True); g.add_argument("--resolve-only",action="store_true"); g.add_argument("--execute",action="store_true"); p.add_argument("--base"); p.add_argument("--remote",default="origin"); p.add_argument("--expected-resolution-sha256")
    try: a=p.parse_args(argv)
    except SystemExit as exc: raise CommandError("invalid_arguments","arguments","Use the exact command help contract.") from exc
    root=repo(a.root); before=resolution(root,a.base,a.remote)
    if a.resolve_only:
        if a.expected_resolution_sha256: raise CommandError("invalid_arguments","expected_resolution_sha256","Do not provide an expected digest in resolve-only mode.")
        return before
    if a.expected_resolution_sha256!=before["resolution_sha256"]: raise CommandError("stale_identity","expected_resolution_sha256","Resolve again from current Git state.",3)
    base=before["selected_base"]; remote=before["remote"]; local=f"refs/heads/{base}"; tracking=f"refs/remotes/{remote}/{base}"; local_before=head(root,local)
    git(root,"fetch","--no-tags",remote,f"refs/heads/{base}:{tracking}"); remote_after=head(root,tracking)
    if branch(root)!=base: raise CommandError("git_failed","repository.branch","Run synchronization from the selected base branch.",4)
    git(root,"merge","--ff-only",tracking); after=head(root)
    if not clean(root) or after!=remote_after: raise CommandError("stale_identity","repository.head","Rerun from current clean Git state.",3)
    post={key:before[key] for key in ("schema_version","skill_id","status","source","selected_base","remote","candidates")}; post["decision_checkout"]={"branch":base,"head":after,"clean":True}
    result={"schema_version":"1.0","skill_id":"guru-sync-base","status":"synced","resolution":{key:before[key] for key in ("source","selected_base","remote","candidates","resolution_sha256")},"post_sync_resolution":post,"post_sync_resolution_sha256":digest(post),"decision_checkout":{"branch":base,"head_before":local_before,"head_after":after,"clean_before":True,"clean_after":True},"git":{"local_ref":local,"remote_ref":tracking,"local_head_before":local_before,"local_head_after":after,"remote_head_after":remote_after,"fetch_performed":True,"fast_forwarded":local_before!=after},"fresh":True}
    result["facts_sha256"]=digest(result); return result
