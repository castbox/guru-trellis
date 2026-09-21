from __future__ import annotations
import argparse, os, subprocess, sys, tempfile
from pathlib import Path
from common import PRE_REVIEW_PROFILES, POST_REVIEW_PROFILES, git, checkpoint_path, index_tree_digest, is_ancestor, merge_base, operation_pair, parse, read_json, repo_root, require_clean_worktree, resolve_commit, task_identity, validate_json, validate_public, validate_result
from runtime.io import CommandError

def _managed_validation_command(command: list[str]) -> list[str]:
    launcher = Path(command[0]).name.casefold()
    if launcher in {"python", "python3", "python.exe", "python3.exe"} or launcher.startswith("python3."):
        return [sys.executable, *command[1:]]
    return command

def guard(package_root: Path, argv: list[str]) -> dict:
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--input",required=True)
    args=parse(parser,argv); repo=repo_root(args.root); public=read_json(repo,package_root,args.input,"input"); validate_public(package_root,public); allow_planning=public["profile"]=="post_plan"; task_identity(repo,public["task_ref"],allow_planning=allow_planning)
    task,old,new=operation_pair(repo,public)
    status=("unchanged" if is_ancestor(repo,new,task) else "new_pair") if public["profile"] in PRE_REVIEW_PROFILES else ("unchanged" if new==old else "new_pair")
    current_head=resolve_commit(repo,"HEAD","HEAD")
    if task != public["task_head"]: status="blocked"
    cp=checkpoint_path(repo,public["task_ref"],allow_planning=allow_planning)
    typed_output=None
    if status=="new_pair" and cp.is_file():
        try:
            checkpoint=read_json(repo,package_root,str(cp),"checkpoint"); validate_result(package_root,repo,checkpoint,public)
            typed_output=checkpoint["typed_output"]; status="current_pair"; cp.unlink()
            try: cp.parent.rmdir()
            except OSError: pass
        except Exception: status="blocked"
    elif status != "blocked" and current_head != task:
        status="blocked"
    result={"status":status,"task_ref":public["task_ref"],"task_head":public["task_head"],"old_base_head":old,"new_base_head":new,"resume_target":public["resume_target"],"typed_output":typed_output}; validate_json(result,package_root/"schemas/pair-guard-result.schema.json","result"); return result

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
    identity=task_identity(repo,request["task_ref"],allow_planning=request["profile"]=="post_plan")
    if identity["branch"] != request["branch"]:
        raise CommandError("stale_identity","branch","Use the exact current task branch.",3)
    require_clean_worktree(repo)
    prior=resolve_commit(repo,request["prior_task_head"],"prior_task_head")
    old_base=resolve_commit(repo,request["old_base_head"],"old_base_head")
    new_base=resolve_commit(repo,request["new_base_head"],"new_base_head")
    selected=resolve_commit(repo,request["selected_base_ref"],"selected_base_ref")
    if resolve_commit(repo,"HEAD","HEAD") != prior or selected != new_base:
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
    result={"schema_version":"1.0","status":"committed","profile":request["profile"],"task_ref":request["task_ref"],"branch":request["branch"],"prior_task_head":prior,"old_base_head":old_base,"new_base_head":new_base,"resume_target":request["resume_target"],"reconciled_task_head":reconciled,"candidate_tree_sha256":request["candidate_tree_sha256"]}
    if review is not None: result["branch_review_commit"]=review
    validate_json(result,package_root/"schemas/reconciliation-result.schema.json","result"); return result

def _git_path(repo: Path, name: str) -> Path:
    path=Path(git(repo, "rev-parse", "--git-path", name))
    return path if path.is_absolute() else repo/path

def _other_sequencer(repo: Path) -> str | None:
    for name in ("CHERRY_PICK_HEAD", "REVERT_HEAD", "REBASE_HEAD", "BISECT_LOG", "sequencer", "rebase-merge", "rebase-apply"):
        if _git_path(repo, name).exists():
            return name
    return None

def _commit_facts(repo: Path, commit: str) -> tuple[list[str], str, str]:
    parents=git(repo,"show","-s","--format=%P",commit).split()
    tree=git(repo,"show","-s","--format=%T",commit)
    message=git(repo,"show","-s","--format=%B",commit).rstrip("\n")
    return parents,tree,message

def resolved_reconcile(package_root: Path, argv: list[str]) -> dict:
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument("--root"); parser.add_argument("--input",required=True)
    args=parse(parser,argv); repo=repo_root(args.root); request=read_json(repo,package_root,args.input,"input")
    validate_json(request,package_root/"schemas/public-resolved-candidate-input.schema.json","input")
    identity=task_identity(repo,request["task_ref"])
    if identity["branch"] != request["branch"]:
        raise CommandError("stale_identity","branch","Use the exact current task branch.",3)
    phase2=resolve_commit(repo,request["phase2_commit_anchor"],"phase2_commit_anchor")
    old=resolve_commit(repo,request["old_base_head"],"old_base_head")
    new=resolve_commit(repo,request["new_base_head"],"new_base_head")
    selected=resolve_commit(repo,request["selected_base_ref"],"selected_base_ref")
    if request["merge_head"] != new or selected != new or request["parent_order"] != [phase2,new] or not is_ancestor(repo,old,new):
        raise CommandError("stale_identity","base_pair","Use the exact reviewed parent order and selected base.",3)
    head=resolve_commit(repo,"HEAD","HEAD")
    if head != phase2:
        require_clean_worktree(repo)
        if _git_path(repo,"MERGE_HEAD").exists() or _other_sequencer(repo):
            raise CommandError("stale_identity","repository.operation","Recovery requires a terminal clean Git state.",3)
        parents,tree,message=_commit_facts(repo,head)
        if parents != request["parent_order"] or tree != request["stage0_tree"] or message != request["commit_message"]:
            raise CommandError("stale_identity","reconciled_task_head","Recover only the exact reviewed reconciliation commit.",3)
        status="recovered"
        reconciled=head
    else:
        other=_other_sequencer(repo)
        if other:
            raise CommandError("stale_identity","repository.operation",f"Finish or abort the other Git operation: {other}.",3)
        merge_path=_git_path(repo,"MERGE_HEAD")
        if not merge_path.is_file() or merge_path.is_symlink():
            raise CommandError("stale_identity","merge_head","Use the active reviewed merge operation.",3)
        merge_heads=[line.strip() for line in merge_path.read_text().splitlines() if line.strip()]
        if merge_heads != [new]:
            raise CommandError("stale_identity","merge_head","Bind exactly one reviewed MERGE_HEAD.",3)
        unresolved=git(repo,"diff","--name-only","--diff-filter=U")
        if unresolved:
            raise CommandError("stale_identity","repository.index","Resolve every conflict before reconciliation.",3)
        if subprocess.run(["git","diff","--quiet"],cwd=repo).returncode:
            raise CommandError("stale_identity","worktree","Stage every resolved change before reconciliation.",3)
        untracked=git(repo,"ls-files","--others","--exclude-standard")
        if untracked:
            raise CommandError("stale_identity","worktree","Remove untracked files before reconciliation.",3)
        tree=git(repo,"write-tree")
        if tree != request["stage0_tree"] or index_tree_digest(repo) != request["index_tree_sha256"]:
            raise CommandError("stale_identity","stage0_tree","Use the exact Phase 2 reviewed stage-0 tree and index digest.",3)
        commit=subprocess.run(["git","commit","-m",request["commit_message"]],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if commit.returncode:
            raise CommandError("reconciliation_failed","commit",commit.stderr.strip() or "The resolved reconciliation commit failed.",3)
        reconciled=resolve_commit(repo,"HEAD","HEAD")
        parents,committed_tree,message=_commit_facts(repo,reconciled)
        if parents != request["parent_order"] or committed_tree != request["stage0_tree"] or message != request["commit_message"]:
            raise CommandError("reconciliation_failed","reconciled_task_head","The created commit differs from the reviewed parents, tree, or message.",3)
        require_clean_worktree(repo)
        status="committed"
    result={"schema_version":"1.0","status":status,"task_ref":request["task_ref"],"branch":request["branch"],"phase2_commit_anchor":phase2,"old_base_head":old,"new_base_head":new,"merge_head":new,"stage0_tree":request["stage0_tree"],"index_tree_sha256":request["index_tree_sha256"],"parent_order":request["parent_order"],"commit_message":request["commit_message"],"reconciled_task_head":reconciled}
    validate_json(result,package_root/"schemas/resolved-reconciliation-result.schema.json","result"); return result

def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    if command["id"]=="guard-task-base-pair": return guard(package_root,argv)
    if command["id"]=="execute-base-candidate": return candidate(package_root,argv)
    if command["id"]=="execute-resolved-base-reconciliation": return resolved_reconcile(package_root,argv)
    return reconcile(package_root,argv)
