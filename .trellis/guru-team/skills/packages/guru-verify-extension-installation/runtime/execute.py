from __future__ import annotations
import argparse, importlib.util
from pathlib import Path
def _o(r):
 s=importlib.util.spec_from_file_location("verify_owner",r/"runtime/owner.py");m=importlib.util.module_from_spec(s);assert s and s.loader;s.loader.exec_module(m);return m
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--input",required=True);p.add_argument("--capability",action="append",required=True);return _o(package_root).cmd_execute_extension_verification(p.parse_args(argv))
