from __future__ import annotations
import argparse, importlib.util
from pathlib import Path
from common import call_owner, parse_arguments
def _o(r):
 s=importlib.util.spec_from_file_location("finalize_owner",r/"runtime/owner.py");m=importlib.util.module_from_spec(s);assert s and s.loader;s.loader.exec_module(m);return m
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False)
 for x in ("root","input","repo","base_branch","remote","title","task_name"): p.add_argument("--"+x.replace("_","-"),required=x=="input")
 p.add_argument("--validation",action="append");p.add_argument("--gate")
 o=_o(package_root);return call_owner(o,o.cmd_execute_finalization_transition,parse_arguments(p,argv))
