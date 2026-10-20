from __future__ import annotations
import argparse, os, subprocess, sys, tempfile
from pathlib import Path
from common import PRE_REVIEW_PROFILES, POST_REVIEW_PROFILES, committed_tree_digest, git, checkpoint_path, index_tree_digest, is_ancestor, merge_base, operation_pair, parse, read_json, repo_root, require_clean_worktree, resolve_commit, task_identity, validate_json, validate_public, validate_result
from runtime.io import CommandError
from resolved import commit_tree, require_merge_state, tree_index, validate_integration_paths, verify_commit

def _managed_validation_command(command: list[str]) -> list[str]:
    launcher = Path(command[0]).name.casefold()
    if launcher in {"python", "python3", "python.exe", "python3.exe"} or launcher.startswith("python3."):
        return [sys.executable, *command[1:]]
    return command

def candidate(package_root: Path, argv: list[str]) -> dict:
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--request",required=True)
    args=parse(parser,argv); repo=repo_root(args.root); request=read_json(repo,package_root,args.request,"request"); validate_json(request,package_root/"schemas/delivery-candidate-request.schema.json","request")
    task=resolve_commit(repo,request["task_head"],"task_head"); base=resolve_commit(repo,request["new_base_head"],"new_base_head"); validations=[]; conflicts=[]; tree=None
    with tempfile.TemporaryDirectory(prefix="guru-base-candidate-") as td:
        worktree=Path(td)/"worktree"; added=False
        try:
            resolved=request.get("resolved_candidate")
            if resolved:
                if resolve_commit(repo,"HEAD","HEAD") != task:
                    raise CommandError("stale_identity","task_head","Use the current pre-reconciliation HEAD.",3)
                require_merge_state(repo,base)
                with tree_index(repo,resolved["stage0_tree"]) as index:
                    validate_integration_paths(repo,task,resolved["stage0_tree"],resolved["integration_paths"],index,live_index=True)
            subprocess.run(["git","worktree","add","--detach",str(worktree),base],cwd=repo,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); added=True
            if resolved:
                subprocess.run(["git","read-tree","--reset","-u",resolved["stage0_tree"]],cwd=worktree,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                merge_failed=False
            else:
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
    result={"status":"ok","task_head":task,"new_base_head":base,"merge_status":"conflicted" if merge_failed else "clean","conflict_paths":conflicts,"candidate_tree_sha256":tree,"validations":validations}; validate_json(result,package_root/"schemas/delivery-candidate-result.schema.json","result"); return result

def reconcile(package_root: Path, argv: list[str]) -> dict:
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--request",required=True)
    args=parse(parser,argv); repo=repo_root(args.root); request=read_json(repo,package_root,args.request,"request"); validate_json(request,package_root/"schemas/delivery-reconciliation-request.schema.json","request")
    identity=task_identity(repo,request["task_ref"],delivery_key=request["delivery_key"])
    if identity["branch"] != request["branch"]:
        raise CommandError("stale_identity","branch","Use the exact current task branch.",3)
    prior=resolve_commit(repo,request["prior_task_head"],"prior_task_head")
    old_base=resolve_commit(repo,request["old_base_head"],"old_base_head")
    new_base=resolve_commit(repo,request["new_base_head"],"new_base_head")
    selected=resolve_commit(repo,request["selected_base_ref"],"selected_base_ref")
    resolved=request.get("resolved_candidate")
    if request["selected_base_ref"] != new_base or selected != new_base:
        raise CommandError("stale_identity","expected_head","Rebuild and reconfirm the exact reconciliation request.",3)
    if request["profile"] in PRE_REVIEW_PROFILES:
        if old_base != merge_base(repo,prior,new_base):
            raise CommandError("stale_identity","old_base_head","Use the live operation-scoped merge base.",3)
        review=None
    else:
        if request["profile"] not in POST_REVIEW_PROFILES or not is_ancestor(repo,old_base,new_base):
            raise CommandError("stale_identity","base_pair","History rewrites require explicit recovery.",3)
        review=resolve_commit(repo,request["branch_review_commit"],"branch_review_commit")
        if not is_ancestor(repo,review,prior):
            raise CommandError("stale_identity","branch_review_commit","Use the prior full-review commit for this task history.",3)
    head=resolve_commit(repo,"HEAD","HEAD")
    if not resolved and head != prior:
        if request["profile"] in POST_REVIEW_PROFILES:
            require_clean_worktree(repo)
        tree=git(repo,"rev-parse",head+"^{tree}")
        verify_commit(repo,head,[prior,new_base],tree,request["commit_message"],request["candidate_tree_sha256"],recovery=True)
        result={"schema_version":"1.0","status":"committed","profile":request["profile"],"task_ref":request["task_ref"],"delivery_key":request["delivery_key"],"branch":request["branch"],"prior_task_head":prior,"old_base_head":old_base,"new_base_head":new_base,"resume_target":request["resume_target"],"reconciled_task_head":head,"candidate_tree_sha256":request["candidate_tree_sha256"]}
        if review is not None: result["branch_review_commit"]=review
        validate_json(result,package_root/"schemas/delivery-reconciliation-result.schema.json","result"); return result
    if is_ancestor(repo,new_base,prior):
        raise CommandError("stale_identity","new_base_head","The current task HEAD already contains this base.",3)
    if resolved:
        tree=resolved["stage0_tree"]
        head=resolve_commit(repo,"HEAD","HEAD")
        with tree_index(repo,tree) as index:
            if index_tree_digest(repo,index_file=index) != request["candidate_tree_sha256"]:
                raise CommandError("stale_identity","candidate_tree_sha256","Use the reviewed integration tree digest.",3)
            validate_integration_paths(repo,prior,tree,resolved["integration_paths"],index,live_index=False)
            if head != prior:
                verify_commit(repo,head,[prior,new_base],tree,request["commit_message"],request["candidate_tree_sha256"],recovery=True)
                reconciled=head
            else:
                require_merge_state(repo,new_base)
                validate_integration_paths(repo,prior,tree,resolved["integration_paths"],index,live_index=True)
                reconciled=commit_tree(repo,[prior,new_base],tree,request["commit_message"],request["candidate_tree_sha256"],index=index)
        result={"schema_version":"1.0","status":"committed","profile":request["profile"],"task_ref":request["task_ref"],"delivery_key":request["delivery_key"],"branch":request["branch"],"prior_task_head":prior,"old_base_head":old_base,"new_base_head":new_base,"resume_target":request["resume_target"],"reconciled_task_head":reconciled,"candidate_tree_sha256":request["candidate_tree_sha256"]}
        validate_json(result,package_root/"schemas/delivery-reconciliation-result.schema.json","result"); return result
    dirty=bool(git(repo,"status","--porcelain=v1","--untracked-files=normal"))
    if dirty and request["profile"] not in PRE_REVIEW_PROFILES:
        require_clean_worktree(repo)
    stash_oid=None
    if dirty:
        previous=git(repo,"rev-parse","--verify","-q","refs/stash",check=False)
        saved=subprocess.run(["git","stash","push","--include-untracked","-m","guru-reconcile-task-base temporary worktree"],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if saved.returncode:
            raise CommandError("reconciliation_failed","worktree",saved.stderr.strip() or "Preserve the pending task changes before reconciliation.",3)
        stash_oid=git(repo,"rev-parse","--verify","refs/stash")
        if stash_oid==previous:
            raise CommandError("reconciliation_failed","worktree","No pending changes were preserved; inspect the task worktree.",3)
    merge_started=False
    try:
        require_clean_worktree(repo)
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
        if committed_tree_digest(repo) != request["candidate_tree_sha256"]:
            raise CommandError("reconciliation_failed","candidate_tree_sha256","The committed tree differs from the reviewed candidate.",3)
        require_clean_worktree(repo)
    except Exception:
        if resolve_commit(repo,"HEAD","HEAD") == prior and merge_started:
            subprocess.run(["git","merge","--abort"],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        raise
    finally:
        if stash_oid is not None:
            restored=subprocess.run(["git","stash","apply","--index",stash_oid],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            if restored.returncode:
                raise CommandError("reconciliation_failed","worktree",f"Pending task changes remain in stash {stash_oid}; resolve the restore before continuing.",3)
            if git(repo,"stash","list","-1","--format=%H") != stash_oid:
                raise CommandError("reconciliation_failed","worktree",f"Pending task changes were restored but stash {stash_oid} requires manual disposition.",3)
            dropped=subprocess.run(["git","stash","drop","stash@{0}"],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            if dropped.returncode:
                raise CommandError("reconciliation_failed","worktree",f"Pending task changes were restored but stash {stash_oid} remains.",3)
    result={"schema_version":"1.0","status":"committed","profile":request["profile"],"task_ref":request["task_ref"],"delivery_key":request["delivery_key"],"branch":request["branch"],"prior_task_head":prior,"old_base_head":old_base,"new_base_head":new_base,"resume_target":request["resume_target"],"reconciled_task_head":reconciled,"candidate_tree_sha256":request["candidate_tree_sha256"]}
    if review is not None: result["branch_review_commit"]=review
    validate_json(result,package_root/"schemas/delivery-reconciliation-result.schema.json","result"); return result

def resolved_reconcile(package_root: Path, argv: list[str]) -> dict:
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--input",required=True)
    args=parse(parser,argv); repo=repo_root(args.root); request=read_json(repo,package_root,args.input,"input")
    validate_json(request,package_root/"schemas/delivery-public-resolved-candidate-input.schema.json","input")
    identity=task_identity(repo,request["task_ref"],delivery_key=request["delivery_key"])
    if identity["branch"] != request["branch"]:
        raise CommandError("stale_identity","branch","Use the exact current task branch.",3)
    phase2=resolve_commit(repo,request["phase2_commit_anchor"],"phase2_commit_anchor")
    old=resolve_commit(repo,request["old_base_head"],"old_base_head")
    new=resolve_commit(repo,request["new_base_head"],"new_base_head")
    selected=resolve_commit(repo,request["selected_base_ref"],"selected_base_ref")
    if request["selected_base_ref"] != new or request["merge_head"] != new or selected != new or request["parent_order"] != [phase2,new] or not is_ancestor(repo,old,new):
        raise CommandError("stale_identity","base_pair","Use the exact reviewed parent order and selected base.",3)
    head=resolve_commit(repo,"HEAD","HEAD")
    if head != phase2:
        require_clean_worktree(repo)
        verify_commit(repo,head,request["parent_order"],request["stage0_tree"],request["commit_message"],request["index_tree_sha256"],recovery=True)
        status="recovered"
        reconciled=head
    else:
        require_merge_state(repo,new)
        if subprocess.run(["git","diff","--quiet"],cwd=repo).returncode:
            raise CommandError("stale_identity","worktree","Stage every resolved change before reconciliation.",3)
        untracked=git(repo,"ls-files","--others","--exclude-standard")
        if untracked:
            raise CommandError("stale_identity","worktree","Remove untracked files before reconciliation.",3)
        tree=git(repo,"write-tree")
        if tree != request["stage0_tree"] or index_tree_digest(repo) != request["index_tree_sha256"]:
            raise CommandError("stale_identity","stage0_tree","Use the exact Phase 2 reviewed stage-0 tree and index digest.",3)
        reconciled=commit_tree(repo,request["parent_order"],request["stage0_tree"],request["commit_message"],request["index_tree_sha256"])
        require_clean_worktree(repo)
        status="committed"
    result={"schema_version":"1.0","status":status,"task_ref":request["task_ref"],"delivery_key":request["delivery_key"],"branch":request["branch"],"phase2_commit_anchor":phase2,"old_base_head":old,"new_base_head":new,"merge_head":new,"stage0_tree":request["stage0_tree"],"index_tree_sha256":request["index_tree_sha256"],"parent_order":request["parent_order"],"commit_message":request["commit_message"],"reconciled_task_head":reconciled}
    validate_json(result,package_root/"schemas/delivery-resolved-reconciliation-result.schema.json","result"); return result

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    if command["id"]=="execute-base-candidate": return candidate(package_root,argv)
    if command["id"]=="execute-resolved-base-reconciliation": return resolved_reconcile(package_root,argv)
    return reconcile(package_root,argv)
