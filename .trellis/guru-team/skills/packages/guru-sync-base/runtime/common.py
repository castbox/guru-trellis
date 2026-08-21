from __future__ import annotations
import hashlib, json, re, subprocess
from pathlib import Path
from runtime.io import CommandError

DEFAULT_BASE_CANDIDATES = ("dev", "develop", "main", "master")

def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def git(root,*args,check=True):
    try:
        p=subprocess.run(["git",*args],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    except OSError as exc:
        raise CommandError("git_failed","repository",f"Git inspection failed: {exc}",4) from exc
    if check and p.returncode: raise CommandError("git_failed","repository",p.stderr.strip() or "Repair Git state and retry.",4)
    return p.stdout.strip()
def repo(value):
    root=Path(value or ".").resolve()
    if git(root,"rev-parse","--show-toplevel",check=False)!=str(root): raise CommandError("unsafe_path","root","Use the exact Git repository root.")
    return root
def clean(root): return git(root,"status","--porcelain=v1","-z")==""
def head(root,ref="HEAD"): return git(root,"rev-parse","--verify",ref)
def branch(root): return git(root,"symbolic-ref","--short","HEAD")
def valid_name(value,label):
    if not isinstance(value,str) or not value or value.strip()!=value or value.startswith("-") or re.search(r"[\x00-\x1f\x7f]",value): raise CommandError("unsafe_path",label,"Use a safe Git name.")
    return value

def valid_branch(root,value,label):
    value=valid_name(value,label)
    if subprocess.run(["git","check-ref-format","--branch",value],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE).returncode:
        raise CommandError("unsafe_path",label,"Use a valid Git branch name.")
    return value

def valid_remote(root,value):
    value=valid_name(value or "origin","remote")
    if subprocess.run(["git","check-ref-format",f"refs/remotes/{value}/probe"],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE).returncode:
        raise CommandError("unsafe_path","remote","Use a remote name that forms a valid remote-tracking ref.")
    return value

def _scalar(value):
    value=value.strip()
    if not value: return ""
    if len(value)>=2 and value[0]==value[-1] and value[0] in "'\"": return value[1:-1]
    lowered=value.casefold()
    if lowered in ("true","false"): return lowered=="true"
    if lowered in ("null","~"): return None
    if re.fullmatch(r"[-+]?\d+",value): return int(value)
    if value.startswith("[") or value.startswith("{"): return {"unsupported_inline_value":value}
    return value

def load_base_config(root):
    path=root/".trellis/guru-team/config.yml"
    if not path.is_file(): return {"base_branch":"","base_branch_candidates":list(DEFAULT_BASE_CANDIDATES)}
    values={"base_branch":"","base_branch_candidates":list(DEFAULT_BASE_CANDIDATES)}
    active=None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line=raw.split("#",1)[0].rstrip()
        if not line.strip(): continue
        text=line.strip()
        if len(line)!=len(line.lstrip()):
            if active=="base_branch_candidates" and text.startswith("- "):
                if not isinstance(values[active],list): values[active]={"invalid_list":text}
                else: values[active].append(_scalar(text[2:]))
            elif active=="base_branch_candidates": values[active]={"invalid_list":text}
            continue
        active=None
        if ":" not in text: continue
        key,value=(part.strip() for part in text.split(":",1))
        if key=="base_branch": values[key]=_scalar(value)
        elif key=="base_branch_candidates":
            if value: values[key]=_scalar(value)
            else: values[key]=[]; active=key
    return values

def configured_candidates(root,config):
    raw=config.get("base_branch_candidates",list(DEFAULT_BASE_CANDIDATES))
    if not isinstance(raw,list) or any(not isinstance(item,str) for item in raw):
        raise CommandError("invalid_arguments","config.base_branch_candidates","Use a YAML list of branch names.")
    values=[]
    for item in raw:
        if not item: continue
        item=valid_branch(root,item,"config.base_branch_candidates")
        if item not in values: values.append(item)
    return values

def remote_default(root,remote):
    process=subprocess.run(["git","ls-remote","--symref",remote,"HEAD"],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if process.returncode: return None
    matches=[]
    for line in process.stdout.splitlines():
        match=re.fullmatch(r"ref: refs/heads/([^\t]+)\tHEAD",line)
        if match:
            value=valid_branch(root,match.group(1),"remote.default")
            if value not in matches: matches.append(value)
    return matches[0] if len(matches)==1 else None

def select_base(root,base,remote):
    remote=valid_remote(root,remote)
    if base:
        source="explicit"; base=valid_branch(root,base,"base"); candidates=[base]
    else:
        config=load_base_config(root)
        scalar=config.get("base_branch","")
        if scalar is None: scalar=""
        if not isinstance(scalar,str): raise CommandError("invalid_arguments","config.base_branch","Use a scalar branch name or an empty value.")
        if scalar:
            source="config"; base=valid_branch(root,scalar,"config.base_branch"); candidates=[base]
        else:
            candidates=configured_candidates(root,config)
            for candidate in candidates:
                if git(root,"rev-parse","--verify","--quiet",f"refs/heads/{candidate}",check=False) or git(root,"rev-parse","--verify","--quiet",f"refs/remotes/{remote}/{candidate}",check=False):
                    source="config-candidate"; base=candidate; break
            else:
                base=remote_default(root,remote)
                if not base: raise CommandError("git_failed","repository","Configure a valid base or repair the remote default branch.",4)
                source="remote-default"
                if base not in candidates: candidates.append(base)
    return {"source":source,"selected_base":base,"remote":remote,"candidates":candidates}

def _common_dir(root):
    value=Path(git(root,"rev-parse","--git-common-dir"))
    return (value if value.is_absolute() else root/value).resolve()

def _registered_worktrees(root):
    raw=git(root,"worktree","list","--porcelain","-z")
    records=[]
    record={}
    for field in raw.split("\0"):
        if not field:
            if record: records.append(record); record={}
            continue
        key,separator,value=field.partition(" ")
        record[key]=value if separator else True
    if record: records.append(record)
    return records

def authority_checkout(root,selected_base):
    selected_base=valid_branch(root,selected_base,"selected_base")
    selected_ref=f"refs/heads/{selected_base}"
    matches=[item for item in _registered_worktrees(root) if item.get("branch")==selected_ref]
    if len(matches)!=1:
        reason="missing" if not matches else "ambiguous"
        raise CommandError("git_failed","repository.authority_checkout",f"The registered clean checkout for {selected_ref} is {reason}; repair the existing worktree registration and retry.",4)
    item=matches[0]
    path_value=item.get("worktree")
    if not isinstance(path_value,str) or not path_value:
        raise CommandError("git_failed","repository.authority_checkout","The selected-base worktree registration has no usable checkout path.",4)
    authority=Path(path_value).resolve()
    if git(authority,"rev-parse","--show-toplevel",check=False)!=str(authority) or _common_dir(authority)!=_common_dir(root):
        raise CommandError("git_failed","repository.authority_checkout","The selected-base checkout does not match the session repository identity.",4)
    local_head=head(root,selected_ref)
    authority_head=head(authority)
    if git(authority,"symbolic-ref","HEAD",check=False)!=selected_ref or item.get("HEAD")!=authority_head or authority_head!=local_head:
        raise CommandError("git_failed","repository.authority_checkout","The selected-base checkout branch, HEAD, and local ref identity do not match.",4)
    if not clean(authority):
        raise CommandError("git_failed","repository.authority_checkout","Clean the selected-base authority checkout before synchronization.",4)
    return authority

def resolution(root,base,remote):
    selected=select_base(root,base,remote)
    authority=authority_checkout(root,selected["selected_base"])
    value={"schema_version":"1.0","skill_id":"guru-sync-base","status":"resolved",**selected,"decision_checkout":{"branch":selected["selected_base"],"head":head(authority),"clean":True}}
    value["resolution_sha256"]=digest(value); return value
