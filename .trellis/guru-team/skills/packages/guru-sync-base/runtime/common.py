from runtime.base_selection import (digest, git, repo, clean, head, branch, valid_name, valid_branch, valid_remote, load_base_config, configured_candidates, remote_default, select_base, DEFAULT_BASE_CANDIDATES, _registered_worktrees, _common_dir)
from runtime.base_selection import authority_checkout as _authority_checkout

def authority_checkout(root, selected_base):
    return _authority_checkout(root, selected_base, require_clean=True)

def resolution(root,base,remote):
    selected=select_base(root,base,remote)
    authority=authority_checkout(root,selected["selected_base"])
    value={"schema_version":"1.0","skill_id":"guru-sync-base","status":"resolved",**selected,"decision_checkout":{"branch":selected["selected_base"],"head":head(authority),"clean":True}}
    value["resolution_sha256"]=digest(value); return value
