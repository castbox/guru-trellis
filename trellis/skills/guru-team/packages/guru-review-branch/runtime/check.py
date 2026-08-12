from __future__ import annotations
import argparse
from pathlib import Path
from common import load,parse,root,validate_gate
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--task");p.add_argument("--input",required=True);p.add_argument("--expected-exit");a=parse(p,argv);repo=root(package_root,a.root);v=validate_gate(package_root,repo,load(repo,package_root,a.input,"input"),a.expected_exit);return {"status":"ok","task_dir":v["task_dir"],"head":__import__('subprocess').run(["git","rev-parse","HEAD"],cwd=repo,text=True,stdout=__import__('subprocess').PIPE,check=True).stdout.strip(),"review_commit":v["review_commit"],"typed_exit":v["typed_exit"],"facts_sha256":v["facts_sha256"]}
