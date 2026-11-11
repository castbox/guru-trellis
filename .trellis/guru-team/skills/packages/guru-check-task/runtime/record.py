from __future__ import annotations
import argparse
from pathlib import Path
from common import checkpoint,content_identity,skill_content_identity,dirty_paths,git,load,parse,rel,root,task,validate_candidate_classifications
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.reviewed_content import reviewed_content_metadata_path
def run(package_root:Path,command:dict,argv:list[str])->dict:
 p=argparse.ArgumentParser(add_help=False);p.add_argument("--root");p.add_argument("--task");p.add_argument("--skill-input");p.add_argument("--input",required=True);p.add_argument("--dry-run",action="store_true")
 a=parse(p,argv);repo=root(package_root,a.root);td=task(repo,a.task)
 if a.input == "-" and a.skill_input == "-":raise CommandError("conflicting_arguments","skill_input","Use stdin for only one JSON locator.")
 auth=load(repo,package_root,a.input,"input")
 public=load(repo,package_root,a.skill_input,"skill_input") if a.skill_input else None
 if not public or public.get("profile") != "delivery_planning_stale_recovery" or not a.dry_run:
  raise CommandError("schema_mismatch","profile","Current development Check recording is retired; only original rollback correction with --dry-run remains. Use guru-review-branch for committed review.")
 expected={"mode","reviewed_paths","validation","docs_ssot","delivery_policy","candidate_classifications","semantic_review","typed_exit","route","reason","consumer"}
 if set(auth)!=expected:raise CommandError("schema_mismatch","input","Use the 11-field semantic input in Recorder Authoring. Full 6.0 results are output/consumer-only; see MIGRATION-710.")
 paths=sorted(auth["reviewed_paths"])
 dirty=[path for path in dirty_paths(repo) if not reviewed_content_metadata_path(path)]
 if not set(dirty).issubset(paths):raise CommandError("stale_identity","reviewed_paths","Review every current dirty path.",3)
 value={"schema_version":"6.0","skill_id":"guru-check-task","task_ref":rel(repo,td),"phase2_capture_commit":git(repo,"rev-parse","HEAD"),"reviewed_content_sha256":skill_content_identity(package_root,repo,rel(repo,td),auth["mode"],public),**auth,"reviewed_paths":paths}
 if auth["typed_exit"]!="planning_stale":raise CommandError("schema_mismatch","typed_exit","Correction can only produce this original planning_stale handoff.")
 validate_json(value,package_root/"schemas/phase2-check.schema.json","input");validate_candidate_classifications(value);path=checkpoint(repo,td,"phase2-check.json")
 return {**value,"artifact_path":str(path),"dry_run":a.dry_run}
