from __future__ import annotations
import argparse, hashlib, os, subprocess, tempfile
from pathlib import Path
from common import checkpoint_path, is_ancestor, parse, read_json, repo_root, resolve_commit, task_identity, validate_json, validate_public, validate_result

def _tree_digest(root: Path) -> str:
    rows=[]
    for path in sorted((p for p in root.rglob('*') if '.git' not in p.parts and p.is_file()),key=lambda p:p.relative_to(root).as_posix().encode()):
        rel=path.relative_to(root).as_posix(); rows.append(rel.encode()+b'\0'+hashlib.sha256(path.read_bytes()).hexdigest().encode()+b'\0')
    return hashlib.sha256(b''.join(rows)).hexdigest()

def guard(package_root: Path, argv: list[str]) -> dict:
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--input",required=True)
    args=parse(parser,argv); repo=repo_root(args.root); public=read_json(repo,package_root,args.input,"input"); validate_public(package_root,public); allow_planning=public["profile"]=="post_plan"; task_identity(repo,public["task_ref"],allow_planning=allow_planning)
    task=resolve_commit(repo,public["task_head"],"task_head"); old=resolve_commit(repo,public["old_base_head"],"old_base_head"); new=resolve_commit(repo,public["selected_base_ref"],"selected_base_ref")
    status="unchanged" if new==old else "new_pair"
    if task != public["task_head"] or new != public["new_base_head"] or resolve_commit(repo,"HEAD","HEAD") != task or not is_ancestor(repo,old,new): status="blocked"
    cp=checkpoint_path(repo,public["task_ref"],allow_planning=allow_planning)
    typed_output=None
    if status=="new_pair" and cp.is_file():
        try:
            checkpoint=read_json(repo,package_root,str(cp),"checkpoint"); validate_result(package_root,repo,checkpoint,public)
            typed_output=checkpoint["typed_output"]; status="current_pair"; cp.unlink()
            try: cp.parent.rmdir()
            except OSError: pass
        except Exception: status="blocked"
    result={"status":status,"task_ref":public["task_ref"],"task_head":public["task_head"],"old_base_head":public["old_base_head"],"new_base_head":new,"resume_target":public["resume_target"],"typed_output":typed_output}; validate_json(result,package_root/"schemas/pair-guard-result.schema.json","result"); return result

def candidate(package_root: Path, argv: list[str]) -> dict:
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--request",required=True)
    args=parse(parser,argv); repo=repo_root(args.root); request=read_json(repo,package_root,args.request,"request"); validate_json(request,package_root/"schemas/candidate-request.schema.json","request")
    task=resolve_commit(repo,request["task_head"],"task_head"); base=resolve_commit(repo,request["new_base_head"],"new_base_head"); validations=[]; conflicts=[]; tree=None
    with tempfile.TemporaryDirectory(prefix="guru-base-candidate-") as td:
        worktree=Path(td)/"worktree"; added=False
        try:
            subprocess.run(["git","worktree","add","--detach",str(worktree),base],cwd=repo,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); added=True
            merge=subprocess.run(["git","merge","--no-commit","--no-ff",task],cwd=worktree,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            merge_failed = merge.returncode != 0
            if merge_failed:
                conflicts=subprocess.run(["git","diff","--name-only","--diff-filter=U"],cwd=worktree,text=True,stdout=subprocess.PIPE,check=True).stdout.splitlines()
            else:
                tree=_tree_digest(worktree)
                for command in request["validation_commands"]:
                    proc=subprocess.run(command,cwd=worktree,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,env={**os.environ,"GIT_TERMINAL_PROMPT":"0"}); validations.append({"argv":command,"exit_code":proc.returncode})
        finally:
            if added: subprocess.run(["git","worktree","remove","--force",str(worktree)],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result={"status":"ok","task_head":task,"new_base_head":base,"merge_status":"conflicted" if merge_failed else "clean","conflict_paths":conflicts,"candidate_tree_sha256":tree,"validations":validations}; validate_json(result,package_root/"schemas/candidate-result.schema.json","result"); return result

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    return guard(package_root,argv) if command["id"]=="guard-task-base-pair" else candidate(package_root,argv)
