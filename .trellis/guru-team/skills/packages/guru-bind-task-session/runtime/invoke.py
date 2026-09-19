from __future__ import annotations
import argparse, importlib.util, json, os, re, sys, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from datetime import datetime, timezone
from runtime.schema import validate_json
from runtime.io import CommandError

EXITS={"resume":"session_resumed","rebind":"session_rebound","switch":"task_switched","reactivate":"reactivate_rebound","manual_recovery":"session_manually_recovered"}

def load_json(value, field):
    if value == "-": value=sys.stdin.read()
    elif isinstance(value,str) and Path(value).is_file(): value=Path(value).read_text()
    try: data=json.loads(value)
    except Exception as exc: raise CommandError("invalid_json",field,"Provide one JSON object.") from exc
    if not isinstance(data,dict): raise CommandError("invalid_json",field,"Provide one JSON object.")
    return data

def active_module(root: Path):
    init=root/".trellis/scripts/common/__init__.py"
    if not init.is_file(): raise CommandError("stale_identity","session_identity","Official Trellis session resolver is unavailable.",3)
    package_root=init.parent
    name="guru_bind_target_common"
    spec=importlib.util.spec_from_file_location(name,init,submodule_search_locations=[str(package_root)])
    if spec is None or spec.loader is None: raise CommandError("stale_identity","session_identity","Session resolver cannot be loaded.",3)
    mod=importlib.util.module_from_spec(spec); sys.modules[name]=mod
    spec.loader.exec_module(mod); return mod

def session_id(mod):
    key=mod.resolve_context_key()
    if not key: raise CommandError("stale_identity","session_identity","Current session identity is unavailable.",3)
    return key

def _git(root: Path, *args: str) -> str:
    p=subprocess.run(["git",*args],cwd=root,text=True,capture_output=True)
    if p.returncode: raise CommandError("stale_identity","git","Live Git identity could not be read.",3)
    return p.stdout.strip()

def _safe_path(path: Path, root: Path, field: str) -> Path:
    path=path.resolve()
    try: path.relative_to(root.resolve())
    except ValueError: raise CommandError("stale_identity",field,"Path escapes the reviewed workspace.",3)
    current=root.resolve()
    for part in path.relative_to(current).parts:
        current=current/part
        if current.is_symlink(): raise CommandError("stale_identity",field,"Binding path contains a symlink.",3)
    return path

def task_facts(root: Path, task_ref: str, allow_missing_mappings: bool = False):
    source_root=root.resolve()
    task_path=(source_root/task_ref).resolve()
    if not task_path.is_dir():
        mapping=source_root/".trellis/.runtime/guru-team/tasks"/(Path(task_ref).name+".json")
        if mapping.is_file():
            data=json.loads(mapping.read_text()); task_path=Path(data.get("workspace_path","")).resolve()/task_ref
    if not task_path.is_dir(): raise CommandError("stale_identity","task_ref","Task directory is unavailable.",3)
    meta=task_path/"task.json"
    if not meta.is_file(): raise CommandError("stale_identity","task.json","Official task identity is unavailable.",3)
    task=json.loads(meta.read_text())
    if not task.get("id") or not task_path.name.endswith(task.get("id")) or task.get("status") not in {"planning","in_progress"}: raise CommandError("stale_identity","task.json","Task identity or lifecycle status is invalid.",3)
    workspace=Path(task.get("worktree_path") or "").resolve()
    if not workspace.is_dir() or (workspace/task_ref).resolve()!=task_path: raise CommandError("stale_identity","workspace","Task workspace does not match task identity.",3)
    branch=_git(workspace,"branch","--show-current")
    if branch != task.get("branch"): raise CommandError("stale_identity","branch","Task branch does not match current checkout.",3)
    head=_git(workspace,"rev-parse","HEAD")
    mapping_roots={source_root,workspace}
    tm=None; wm=None
    for base in mapping_roots:
        tmap=base/".trellis/.runtime/guru-team/tasks"/f"{task.get('id')}.json"
        wmap=base/".trellis/.runtime/guru-team/workspaces"/f"{task.get('id')}.json"
        if tmap.is_file(): tm=json.loads(tmap.read_text())
        if wmap.is_file(): wm=json.loads(wmap.read_text())
    if (not tm or not wm) and not allow_missing_mappings: raise CommandError("stale_identity","runtime_mapping","Task/workspace mapping identity drifted.",3)
    if tm and wm and (tm.get("task_artifact_dir")!=task_ref or tm.get("workspace_path")!=str(workspace) or wm.get("workspace_path")!=str(workspace) or wm.get("branch_name")!=branch): raise CommandError("stale_identity","runtime_mapping","Task/workspace mapping identity drifted.",3)
    generation=int(task.get("lifecycle_generation") or 1)
    for obj in (tm,wm):
        if obj is not None and obj.get("lifecycle_generation",generation)!=generation: raise CommandError("stale_identity","lifecycle_generation","Task and workspace lifecycle generations differ.",3)
    return task, head, branch, workspace, generation

def write_recovery_mappings(root: Path, workspace: Path, task: dict, task_ref: str, branch: str):
    slug=str(task["id"]); workspace_slug=slug; now=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    payloads={".trellis/.runtime/guru-team/tasks/%s.json"%slug:{"schema_version":"1.0","task_slug":slug,"workspace_slug":workspace_slug,"workspace_path":str(workspace),"task_artifact_dir":task_ref,"updated_at":now},".trellis/.runtime/guru-team/workspaces/%s.json"%slug:{"schema_version":"1.0","workspace_slug":workspace_slug,"workspace_path":str(workspace),"source_checkout":str(root),"branch_name":branch,"updated_at":now}}
    for base in {root.resolve(),workspace.resolve()}:
        for rel,payload in payloads.items():
            path=base/rel; path.parent.mkdir(parents=True,exist_ok=True)
            if path.exists():
                current=json.loads(path.read_text())
                if any(current.get(k)!=v for k,v in payload.items() if k!="updated_at"): raise CommandError("stale_identity","runtime_mapping","Existing mapping conflicts with recovery identity.",3)
            else: path.write_text(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n")

def execute(root: Path, input_value: str, owner_value: str):
    public=load_json(input_value,"input"); owner=load_json(owner_value,"owner_result")
    validate_json(public,Path(__file__).parents[1]/"schemas/public-input.schema.json","input")
    validate_json(owner,Path(__file__).parents[1]/"schemas/semantic-result.schema.json","owner_result")
    for k in ("profile","mode","task_ref","continuation_id"):
        if owner.get(k)!=public.get(k): raise CommandError("stale_identity",f"owner_result.{k}","Rerun semantic review for the current binding request.",3)
    if public.get("profile")=="switch_task" and owner.get("target_task_ref")!=public.get("target_task_ref"): raise CommandError("stale_identity","target_task_ref","Switch target changed.",3)
    mod=active_module(root); sid=session_id(mod); manual=public.get("profile")=="manual_recovery" or owner.get("route")=="manual_recovery"; task,head,branch,workspace,generation=task_facts(root,owner["task_ref"],allow_missing_mappings=manual)
    if public.get("profile")=="switch_task" and public.get("target_task_ref"):
        previous=mod.resolve_active_task()
        if previous.error or previous.task_path == owner["task_ref"]: raise CommandError("stale_identity","target_task_ref","Switch requires a distinct validated source task.",3)
        task_facts(root,public["target_task_ref"])
    if generation != int(owner["lifecycle_generation"]): raise CommandError("stale_identity","lifecycle_generation","Requested lifecycle generation is stale.",3)
    if manual: write_recovery_mappings(root,workspace,task,owner["task_ref"],branch)
    try: mod.set_active_task(owner["task_ref"],workspace)
    except Exception as exc: raise CommandError("stale_identity","session_identity",f"Official session binding could not be established: {exc}",3)
    bindings=root/".trellis/.runtime/guru-team/session-bindings"; bindings.mkdir(parents=True,exist_ok=True)
    bid=f"{sid}--{task['id']}"; path=bindings/f"{bid}.json"
    payload={"schema_version":"1.0","binding_id":bid,"session_id":sid,"task_ref":owner["task_ref"],"task_id":task["id"],"workspace_path":str(workspace),"branch":branch,"base_branch":task.get("base_branch"),"task_head":head,"lifecycle_generation":generation,"current_route":owner["resume_target"],"updated_at":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
    if path.exists():
        current=json.loads(path.read_text())
        for key in ("session_id","task_ref","task_id","workspace_path","branch","base_branch","task_head","lifecycle_generation","current_route"):
            if current.get(key)!=payload.get(key): raise CommandError("stale_identity","binding","Existing binding conflicts with current identity.",3)
    else: path.write_text(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n")
    out={"exit_id":EXITS[owner["route"]],"task_ref":owner["task_ref"],"session_id":sid,"binding_id":bid,"lifecycle_generation":generation,"resume_target":owner["resume_target"]}
    validate_json(out,Path(__file__).parents[1]/"schemas/public-output.schema.json","stdout"); return out

def run(package_root: Path, command: dict, argv: list[str]):
    ap=argparse.ArgumentParser(add_help=False); ap.add_argument("--root",default="."); ap.add_argument("--input",required=True); ap.add_argument("--owner-result",required=True); a=ap.parse_args(argv)
    return execute(Path(a.root).resolve(),a.input,a.owner_result)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default="."); ap.add_argument("--input",required=True); ap.add_argument("--owner-result",required=True); a=ap.parse_args()
    print(json.dumps(execute(Path(a.root).resolve(),a.input,a.owner_result),ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    try: main()
    except CommandError as exc: print(json.dumps({"code":exc.code,"field_path":exc.field_path,"remediation":exc.remediation},ensure_ascii=False)); raise SystemExit(exc.exit_status)
