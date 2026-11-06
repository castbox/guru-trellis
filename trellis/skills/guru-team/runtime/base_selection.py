"""Read-only Git base and registered-checkout facts shared by Sync and tools."""
from __future__ import annotations
import hashlib, json, re, subprocess
from pathlib import Path
from runtime.io import CommandError

DEFAULT_BASE_CANDIDATES = ("dev", "develop", "main", "master")

def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def git(root,*args,check=True):
    try:
        p=subprocess.run(["git",*args],cwd=root,text=True,encoding="utf-8",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    except OSError as exc:
        raise CommandError("git_failed","repository",f"Git inspection failed: {exc}",4) from exc
    if check and p.returncode: raise CommandError("git_failed","repository",p.stderr.strip() or "Repair Git state and retry.",4)
    return p.stdout.strip()
def _is_repository_root(root):
    value=git(root,"rev-parse","--show-toplevel",check=False)
    return bool(value) and Path(value).resolve()==root

def repo(value):
    root=Path(value or ".").resolve()
    if not _is_repository_root(root): raise CommandError("unsafe_path","root","Use the exact Git repository root.")
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
    process=subprocess.run(["git","ls-remote","--symref",remote,"HEAD"],cwd=root,text=True,encoding="utf-8",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if process.returncode: return None
    matches=[]
    for line in process.stdout.splitlines():
        match=re.fullmatch(r"ref: refs/heads/([^\t]+)\tHEAD",line)
        if match:
            value=valid_branch(root,match.group(1),"remote.default")
            if value not in matches: matches.append(value)
    return matches[0] if len(matches)==1 else None

def select_base(root,base=None,remote="origin"):
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

def authority_checkout(root,selected_base,require_clean=False):
    selected_base=valid_branch(root,selected_base,"selected_base")
    selected_ref=f"refs/heads/{selected_base}"
    matches=[item for item in _registered_worktrees(root) if item.get("branch")==selected_ref]
    if len(matches)!=1:
        reason="missing" if not matches else "ambiguous"
        raise CommandError("git_failed","repository.authority_checkout",f"The registered checkout for {selected_ref} is {reason}; repair the existing worktree registration and retry.",4)
    item=matches[0]
    path_value=item.get("worktree")
    if not isinstance(path_value,str) or not path_value:
        raise CommandError("git_failed","repository.authority_checkout","The selected-base worktree registration has no usable checkout path.",4)
    authority=Path(path_value).resolve()
    if not _is_repository_root(authority) or _common_dir(authority)!=_common_dir(root):
        raise CommandError("git_failed","repository.authority_checkout","The selected-base checkout does not match the session repository identity.",4)
    local_head=head(root,selected_ref)
    authority_head=head(authority)
    if git(authority,"symbolic-ref","HEAD",check=False)!=selected_ref or item.get("HEAD")!=authority_head or authority_head!=local_head:
        raise CommandError("git_failed","repository.authority_checkout","The selected-base checkout branch, HEAD, and local ref identity do not match.",4)
    if require_clean and not clean(authority):
        raise CommandError("git_failed","repository.authority_checkout","Clean the selected-base authority checkout before synchronization.",4)
    return authority


def object_source(root, selected_ref, expected_commit=None, source="explicit"):
    """Resolve an intentionally selected Git object without checkout or refresh."""
    selected_ref = valid_name(selected_ref, "base_ref")
    commit = git(root, "rev-parse", "--verify", f"{selected_ref}^{{commit}}", check=False)
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise CommandError("git_failed", "base_ref", "Select an available Git ref or commit through guru-sync-base operation=read; refresh an explicit remote ref separately when needed.", 4)
    if expected_commit is not None and expected_commit != commit:
        raise CommandError("stale_identity", "base_commit", "The selected ref does not resolve to the requested fixed commit. Reselect the intended ref/commit through guru-sync-base operation=read.", 3)
    value = {"kind": "git_object", "source": source, "selected_ref": selected_ref, "commit": commit}
    value["identity_sha256"] = digest(value)
    return value


def check_object_source(root, value):
    """Check the adopted immutable object; a later ref advance does not retarget it."""
    expected = {key: value[key] for key in ("kind", "source", "selected_ref", "commit")}
    if value["identity_sha256"] != digest(expected):
        raise CommandError("stale_identity", "base.identity_sha256", "Rerun guru-sync-base operation=read for the selected source.", 3)
    if git(root, "cat-file", "-t", value["commit"], check=False) != "commit":
        raise CommandError("git_failed", "base.commit", "Restore the selected commit object, then rerun guru-sync-base operation=read.", 4)
    return value["commit"]


def source_ref(value):
    return value["selected_ref"] if value.get("kind") == "git_object" else value["selected_base"]


def source_blob(root, commit, path):
    """Read one regular source blob at the selected tree, preserving its bytes."""
    relative = Path(path)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise CommandError("unsafe_path", "path", "Use a repository-relative source file path.")
    result = subprocess.run(["git", "ls-tree", "-z", commit, "--", path], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    rows = [row for row in result.stdout.split(b"\0") if row]
    if result.returncode or len(rows) != 1:
        raise CommandError("git_failed", "path", "Select a file present in the fixed baseline tree.", 4)
    metadata, _, name = rows[0].partition(b"\t")
    mode, kind, oid = metadata.split()
    if kind != b"blob" or mode not in (b"100644", b"100755") or name.decode("utf-8") != path:
        raise CommandError("git_failed", "path", "Select a regular blob in the fixed baseline tree.", 4)
    blob = subprocess.run(["git", "cat-file", "blob", oid.decode("ascii")], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if blob.returncode:
        raise CommandError("git_failed", "path", "Restore the selected baseline blob.", 4)
    return oid.decode("ascii"), blob.stdout


def check_candidate(candidate, body_sha256=None):
    if candidate is None:return
    try:actual=hashlib.sha256(Path(candidate["locator"]).read_bytes()).hexdigest()
    except OSError as exc:raise CommandError("stale_identity","transition.candidate","Restore or reselect the draft and rerun Discovery.",3) from exc
    if actual!=candidate["body_sha256"] or (body_sha256 is not None and body_sha256!=actual):
        raise CommandError("stale_identity","transition.candidate","The draft changed. Reread its content and rerun the affected Intake owners.",3)
