from __future__ import annotations
import argparse
from pathlib import Path
from common import load,parse,root,validate_candidate
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--task");p.add_argument("--candidate-artifact",required=True);a=parse(p,argv);repo=root(package_root,a.root);c=load(repo,package_root,a.candidate_artifact,"candidate_artifact");exit_id=validate_candidate(package_root,repo,c);return {"status":"ok","mode":"candidate","typed_exit":exit_id,"candidate_validation":{"sequence":c["sequence"],"pre_commit_head":c["git"]["pre_commit_head"],"exact_stage_paths":c["exact_stage_paths"]},"checked_commits":[]}
