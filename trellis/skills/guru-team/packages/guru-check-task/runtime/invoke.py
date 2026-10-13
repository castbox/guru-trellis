from __future__ import annotations
import argparse, importlib.util
from pathlib import Path
from check import run as check_phase2
from common import checkpoint,load,parse,root,task
from runtime.io import CommandError
from runtime.schema import validate_json

def run(package_root:Path,command:dict,argv:list[str])->dict:
 if command.get("id")=="project-resolved-reconciliation":
  from project import run as project_resolved_reconciliation
  return project_resolved_reconciliation(package_root,command,argv)
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--invocation");p.add_argument("--input");p.add_argument("--owner-result")
 a=parse(p,argv);repo=root(package_root,a.root)
 if a.invocation:
  envelope=load(repo,package_root,a.invocation,"invocation");public=envelope.get("public_input");owner=envelope.get("owner_result")
 else:public=load(repo,package_root,a.input,"input");owner=load(repo,package_root,a.owner_result,"owner_result")
 if not isinstance(public,dict) or not isinstance(owner,dict):raise CommandError("invalid_arguments","invocation","Provide public input and checked owner result.")
 if public.get("profile") == "delivery_scope_revision":
     from runtime.delivery_projection.scope_revision import revise
     return revise(repo, package_root, public, owner, owner_role="check", expected_phase="checking")
 if public.get("profile") == "delivery_scope_withdrawal":
  from runtime.delivery_projection.withdrawal import stop
  return stop(repo,package_root,public,owner,owner_role="check",expected_phase="checking")
 if str(public.get("profile", "")).startswith("delivery_"):
  from delivery import invoke as invoke_delivery
  from runtime.task_lifecycle.errors import LifecycleContractError
  try:return invoke_delivery(package_root,repo,public,owner)
  except LifecycleContractError as exc:raise CommandError("stale_identity",exc.field_path,exc.remediation,3) from exc
 raise CommandError("schema_mismatch","profile","Migrate through the public Delivery contract; legacy Task development profiles are not active.")
