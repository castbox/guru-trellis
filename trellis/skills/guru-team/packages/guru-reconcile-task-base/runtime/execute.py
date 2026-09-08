from __future__ import annotations
import argparse, os, subprocess, sys, tempfile
from pathlib import Path
from common import checkpoint_path, index_tree_digest, is_ancestor, parse, read_json, repo_root, require_clean_worktree, resolve_commit, task_identity, validate_json, validate_public, validate_result
from runtime.io import CommandError

def _managed_validation_command(command: list[str]) -> list[str]:
    launcher = Path(command[0]).name.casefold()
    if launcher in {"python", "python3", "python.exe", "python3.exe"} or launcher.startswith("python3."):
        return [sys.executable, *command[1:]]
    return command

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
                tree=index_tree_digest(worktree)
                for command in request["validation_commands"]:
                    executed_command=_managed_validation_command(command)
                    proc=subprocess.run(executed_command,cwd=worktree,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,env={**os.environ,"GIT_TERMINAL_PROMPT":"0"}); validations.append({"argv":executed_command,"exit_code":proc.returncode})
        finally:
            if added: subprocess.run(["git","worktree","remove","--force",str(worktree)],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result={"status":"ok","task_head":task,"new_base_head":base,"merge_status":"conflicted" if merge_failed else "clean","conflict_paths":conflicts,"candidate_tree_sha256":tree,"validations":validations}; validate_json(result,package_root/"schemas/candidate-result.schema.json","result"); return result

def reconcile(package_root: Path, argv: list[str]) -> dict:
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--request",required=True)
    args=parse(parser,argv); repo=repo_root(args.root); request=read_json(repo,package_root,args.request,"request"); validate_json(request,package_root/"schemas/reconciliation-request.schema.json","request")
    identity=task_identity(repo,request["task_ref"])
    if identity["branch"] != request["branch"]:
        raise CommandError("stale_identity","branch","Use the exact current task branch.",3)
    require_clean_worktree(repo)
    prior=resolve_commit(repo,request["prior_task_head"],"prior_task_head")
    old_base=resolve_commit(repo,request["old_base_head"],"old_base_head")
    new_base=resolve_commit(repo,request["new_base_head"],"new_base_head")
    review=resolve_commit(repo,request["branch_review_commit"],"branch_review_commit")
    selected=resolve_commit(repo,request["selected_base_ref"],"selected_base_ref")
    if resolve_commit(repo,"HEAD","HEAD") != prior or selected != new_base:
        raise CommandError("stale_identity","expected_head","Rebuild and reconfirm the exact reconciliation request.",3)
    if not is_ancestor(repo,old_base,new_base):
        raise CommandError("stale_identity","base_pair","History rewrites require explicit recovery.",3)
    if not is_ancestor(repo,review,prior):
        raise CommandError("stale_identity","branch_review_commit","Use the prior full-review commit for this task history.",3)
    if is_ancestor(repo,new_base,prior):
        raise CommandError("stale_identity","new_base_head","The current task HEAD already contains this base.",3)
    merge_started=False
    try:
        merge=subprocess.run(["git","merge","--no-commit","--no-ff",new_base],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        merge_started=(repo/".git/MERGE_HEAD").is_file() or bool(subprocess.run(["git","rev-parse","-q","--verify","MERGE_HEAD"],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE).returncode==0)
        if merge.returncode:
            raise CommandError("reconciliation_failed","merge",merge.stderr.strip() or "The reviewed merge did not apply cleanly.",3)
        candidate=index_tree_digest(repo)
        if candidate != request["candidate_tree_sha256"]:
            raise CommandError("stale_identity","candidate_tree_sha256","The live merge tree differs from the reviewed candidate.",3)
        commit=subprocess.run(["git","commit","-m",request["commit_message"]],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if commit.returncode:
            raise CommandError("reconciliation_failed","commit",commit.stderr.strip() or "The local reconciliation commit failed.",3)
        reconciled=resolve_commit(repo,"HEAD","HEAD")
        if not is_ancestor(repo,prior,reconciled) or not is_ancestor(repo,new_base,reconciled):
            raise CommandError("reconciliation_failed","reconciled_task_head","The result does not contain both reviewed parents.",3)
        parents=subprocess.run(["git","show","-s","--format=%P",reconciled],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout.strip().split()
        if parents != [prior,new_base]:
            raise CommandError("reconciliation_failed","reconciled_task_head","Create exactly one merge commit with the reviewed parent order.",3)
        if index_tree_digest(repo) != request["candidate_tree_sha256"]:
            raise CommandError("reconciliation_failed","candidate_tree_sha256","The committed tree differs from the reviewed candidate.",3)
        require_clean_worktree(repo)
    except Exception:
        if resolve_commit(repo,"HEAD","HEAD") == prior and merge_started:
            subprocess.run(["git","merge","--abort"],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        raise
    result={"schema_version":"1.0","status":"committed","task_ref":request["task_ref"],"branch":request["branch"],"prior_task_head":prior,"old_base_head":old_base,"new_base_head":new_base,"branch_review_commit":review,"reconciled_task_head":reconciled,"candidate_tree_sha256":request["candidate_tree_sha256"]}
    validate_json(result,package_root/"schemas/reconciliation-result.schema.json","result"); return result

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    if command["id"]=="guard-task-base-pair": return guard(package_root,argv)
    if command["id"]=="execute-base-candidate": return candidate(package_root,argv)
    return reconcile(package_root,argv)
