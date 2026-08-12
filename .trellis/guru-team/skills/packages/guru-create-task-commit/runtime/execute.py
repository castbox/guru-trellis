from __future__ import annotations
import argparse,os,subprocess,tempfile
from pathlib import Path
from common import git,load,parse,root,validate_candidate
from runtime.io import CommandError
def index_entries(repo,excluded):
 p=subprocess.run(["git","ls-files","--stage","-z"],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise CommandError("stale_identity","index",p.stderr.decode(errors="replace").strip() or "Read the live index.",3)
 result={}
 for record in p.stdout.split(b"\0"):
  if not record:continue
  metadata,separator,path=record.partition(b"\t")
  if not separator:raise CommandError("stale_identity","index","Git returned an invalid index entry.",3)
  name=path.decode("utf-8")
  if name not in excluded:result[name]=metadata.decode("ascii")
 return result
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--task");p.add_argument("--candidate-artifact",required=True);a=parse(p,argv);repo=root(package_root,a.root);c=load(repo,package_root,a.candidate_artifact,"candidate_artifact");exit_id=validate_candidate(package_root,repo,c)
 if exit_id!="committed":return {"status":"not_committed","typed_exit":exit_id,"task_ref":c["task"]["path"]}
 pre=c["git"]["pre_commit_head"];branch=git(repo,"symbolic-ref","HEAD").stdout.strip();exact=set(c["exact_stage_paths"]);index_before=index_entries(repo,exact)
 fd,index=tempfile.mkstemp(prefix="guru-task-commit-");os.close(fd);os.unlink(index);env={"GIT_INDEX_FILE":index}
 try:
  git(repo,"read-tree",pre,env=env);git(repo,"add","-A","--",*c["exact_stage_paths"],env=env);tree=git(repo,"write-tree",env=env).stdout.strip();commit=git(repo,"commit-tree",tree,"-p",pre,env=env,input=c["message"]["bytes"]).stdout.strip();git(repo,"update-ref",branch,commit,pre);git(repo,"reset","-q",commit,"--",*c["exact_stage_paths"])
 finally:
  Path(index).unlink(missing_ok=True)
 if index_entries(repo,exact)!=index_before:raise CommandError("stale_identity","index","Unrelated live index entries changed during isolated commit.",3)
 if git(repo,"diff","--cached","--quiet",commit,"--",*c["exact_stage_paths"],check=False).returncode:raise CommandError("stale_identity","index","Committed paths remain staged after isolated commit.",3)
 if git(repo,"rev-parse","HEAD").stdout.strip()!=commit:raise CommandError("stale_identity","commit","Commit publication postcondition failed.",3)
 candidate=Path(a.candidate_artifact);candidate=candidate if candidate.is_absolute() else repo/candidate;candidate.unlink(missing_ok=True)
 phase2=repo/".trellis/.runtime/guru-team/owner-checkpoints"/Path(c["task"]["path"]).name/"phase2-check.json";phase2.unlink(missing_ok=True)
 return {"status":"committed","exit":"committed","pre_commit_head":pre,"commit_sha":commit}
