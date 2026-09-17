from __future__ import annotations
import json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
from jsonschema import Draft202012Validator

PACKAGE=Path(__file__).resolve().parents[1]
SKILLS=PACKAGE.parents[1]
RUNTIME=SKILLS/"runtime"
if str(SKILLS) not in sys.path: sys.path.insert(0,str(SKILLS))
from runtime.command import main
sys.path.insert(0,str(PACKAGE/"runtime"))
import invoke, prepare, recover

class PackageLocalRuntimeTest(unittest.TestCase):
 def test_created_result_recovery_is_read_only_and_identity_bound(self):
  with tempfile.TemporaryDirectory() as tmp:
   repo=Path(tmp)/"repo";subprocess.run(["git","init","-q","-b","codex/recovery",str(repo)],check=True)
   subprocess.run(["git","config","user.name","Workspace Test"],cwd=repo,check=True);subprocess.run(["git","config","user.email","workspace@example.invalid"],cwd=repo,check=True)
   (repo/"README.md").write_text("base\n");subprocess.run(["git","add","README.md"],cwd=repo,check=True);subprocess.run(["git","commit","-q","-m","test: base"],cwd=repo,check=True)
   task_ref=".trellis/tasks/09-17-recovery";task_dir=repo/task_ref;task_dir.mkdir(parents=True)
   resolved_repo=repo.resolve();task={"id":"recovery","status":"planning","branch":"codex/recovery","base_branch":"main","worktree_path":str(resolved_repo)}
   (task_dir/"task.json").write_text(json.dumps(task))
   runtime=repo/".trellis/.runtime/guru-team";(runtime/"tasks").mkdir(parents=True);(runtime/"workspaces").mkdir(parents=True)
   (runtime/"tasks/recovery.json").write_text(json.dumps({"schema_version":"1.0","task_slug":"recovery","workspace_slug":"recovery","workspace_path":str(resolved_repo),"task_artifact_dir":task_ref,"updated_at":"2026-09-17T00:00:00Z"}))
   (runtime/"workspaces/recovery.json").write_text(json.dumps({"schema_version":"1.0","workspace_slug":"recovery","workspace_path":str(resolved_repo),"source_checkout":str(repo.parent/"source"),"branch_name":"codex/recovery","updated_at":"2026-09-17T00:00:00Z"}))
   boundary=repo/".trellis/guru-team/scripts/bash/check-workspace-boundary.sh";boundary.parent.mkdir(parents=True);boundary.write_text("#!/usr/bin/env bash\nprintf '%s\\n' '{\"status\":\"ok\"}'\n");boundary.chmod(0o755)
   task_cli=repo/".trellis/scripts/task.py";task_cli.parent.mkdir(parents=True,exist_ok=True);task_cli.write_text("import json\nprint(json.dumps({'current_task': {'dir': '.trellis/tasks/09-17-recovery'}, 'stale': False}))\n")
   invocation=Path(tmp)/"invoke.json";before=subprocess.run(["git","status","--porcelain=v1","-z","--untracked-files=all"],cwd=repo,stdout=subprocess.PIPE).stdout
   result=recover.run(PACKAGE,{},["--root",str(repo),"--task",task_ref])
   self.assertEqual(("passed","created",task_ref),(result["status"],result["typed_exit"],result["task_ref"]))
   recovered=subprocess.run(
    [str(PACKAGE/"scripts/recover-task-workspace-result.sh"),"--root",str(repo),"--task",task_ref],
    cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
    env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"},
   )
   self.assertEqual(0,recovered.returncode,recovered.stderr)
   self.assertEqual(result,json.loads(recovered.stdout))
   public={"profile":"recover_created_result","mode":"workflow","task_ref":task_ref};invocation.write_text(json.dumps({"public_input":public,"recovery_result":result}))
   self.assertEqual({"exit_id":"created"},invoke.run(PACKAGE,{},["--root",str(repo),"--invocation",str(invocation)]))
   invoked=subprocess.run(
    [str(PACKAGE/"scripts/invoke.sh"),"--root",str(repo),"--invocation",str(invocation)],
    cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
    env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"},
   )
   self.assertEqual(0,invoked.returncode,invoked.stderr)
   self.assertEqual({"exit_id":"created"},json.loads(invoked.stdout))
   after=subprocess.run(["git","status","--porcelain=v1","-z","--untracked-files=all"],cwd=repo,stdout=subprocess.PIPE).stdout
   self.assertEqual(before,after)
   task["status"]="in_progress";(task_dir/"task.json").write_text(json.dumps(task))
   with self.assertRaisesRegex(Exception,"planning task"):recover.run(PACKAGE,{},["--root",str(repo),"--task",task_ref])

 def test_prepare_base_freshness_revalidates_reviewed_provenance(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);repo=root/"repo";remote=root/"origin.git"
   subprocess.run(["git","init","-q","--bare",str(remote)],check=True)
   subprocess.run(["git","init","-q","-b","main",str(repo)],check=True)
   subprocess.run(["git","config","user.name","Workspace Test"],cwd=repo,check=True)
   subprocess.run(["git","config","user.email","workspace@example.invalid"],cwd=repo,check=True)
   (repo/"README.md").write_text("base\n");subprocess.run(["git","add","README.md"],cwd=repo,check=True);subprocess.run(["git","commit","-q","-m","test: base"],cwd=repo,check=True)
   subprocess.run(["git","remote","add","origin",str(remote)],cwd=repo,check=True);subprocess.run(["git","push","-q","-u","origin","main"],cwd=repo,check=True)
   head=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,check=True,text=True,stdout=subprocess.PIPE).stdout.strip()
   resolution={"schema_version":"1.0","skill_id":"guru-sync-base","status":"resolved","source":"explicit","selected_base":"main","remote":"origin","candidates":["main"],"decision_checkout":{"branch":"main","head":head,"clean":True}}
   provenance={"source":"explicit","selected_base":"main","remote":"origin","ordered_candidates":["main"],"decision_head":head,"local_base_head":head,"remote_base_head":head,"post_sync_resolution_sha256":prepare.digest(resolution)}
   freshness=prepare.reviewed_base_freshness(repo,{"base_branch":"conflicting-config","base_branch_candidates":["dev"]},provenance,"main")
   self.assertEqual(freshness["post_sync_resolution"],resolution);self.assertTrue(freshness["three_way_equal"]);self.assertTrue(freshness["fresh"])
   self.assertEqual(freshness["facts_sha256"],prepare.digest({k:v for k,v in freshness.items() if k!="facts_sha256"}))
   config_resolution={**resolution,"source":"config"}
   config_provenance={**provenance,"source":"config","post_sync_resolution_sha256":prepare.digest(config_resolution)}
   config_freshness=prepare.reviewed_base_freshness(repo,{"base_branch":"main","base_branch_candidates":["dev"]},config_provenance,None)
   self.assertEqual(config_freshness["post_sync_resolution"],config_resolution);self.assertTrue(config_freshness["fresh"])
   invalid=dict(provenance);invalid.pop("remote_base_head")
   with self.assertRaisesRegex(ValueError,"exactly eight fields"):prepare.reviewed_base_freshness(repo,{"base_branch":"main","base_branch_candidates":[]},invalid,"main")

 def test_prepare_base_freshness_accepts_ordered_candidate_provenance(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);repo=root/"repo";remote=root/"origin.git"
   subprocess.run(["git","init","-q","--bare",str(remote)],check=True)
   subprocess.run(["git","init","-q","-b","main",str(repo)],check=True)
   subprocess.run(["git","config","user.name","Workspace Test"],cwd=repo,check=True)
   subprocess.run(["git","config","user.email","workspace@example.invalid"],cwd=repo,check=True)
   (repo/"README.md").write_text("base\n");subprocess.run(["git","add","README.md"],cwd=repo,check=True);subprocess.run(["git","commit","-q","-m","test: base"],cwd=repo,check=True)
   subprocess.run(["git","checkout","-q","-b","dev"],cwd=repo,check=True)
   subprocess.run(["git","remote","add","origin",str(remote)],cwd=repo,check=True);subprocess.run(["git","push","-q","-u","origin","main","dev"],cwd=repo,check=True)
   head=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,check=True,text=True,stdout=subprocess.PIPE).stdout.strip()
   candidates=["dev","main"]
   resolution={"schema_version":"1.0","skill_id":"guru-sync-base","status":"resolved","source":"config-candidate","selected_base":"dev","remote":"origin","candidates":candidates,"decision_checkout":{"branch":"dev","head":head,"clean":True}}
   provenance={"source":"config-candidate","selected_base":"dev","remote":"origin","ordered_candidates":candidates,"decision_head":head,"local_base_head":head,"remote_base_head":head,"post_sync_resolution_sha256":prepare.digest(resolution)}
   freshness=prepare.reviewed_base_freshness(repo,{"base_branch":"","base_branch_candidates":candidates},provenance,None)
   self.assertEqual(freshness["post_sync_resolution"],resolution);self.assertEqual(freshness["resolution"]["candidates"],candidates)
   self.assertTrue(freshness["three_way_equal"]);self.assertTrue(freshness["fresh"])

 def test_command_and_error_contract_close(self):
  commands=json.loads((PACKAGE/"commands.json").read_text())
  catalog=json.loads((PACKAGE/"errors/catalog.json").read_text())
  command_schema=json.loads((SKILLS/"schemas/skill-commands.schema.json").read_text())
  error_schema=json.loads((SKILLS/"schemas/skill-error-catalog.schema.json").read_text())
  self.assertEqual([],list(Draft202012Validator(command_schema).iter_errors(commands)))
  self.assertEqual([],list(Draft202012Validator(error_schema).iter_errors(catalog)))
  codes={x["code"] for x in catalog["errors"]}
  for command in commands["commands"]:
   self.assertEqual(PACKAGE.name,command["owner"])
   self.assertTrue((PACKAGE/command["entrypoint"]).is_file())
   self.assertLessEqual(set(command["errors"]),codes)

 def test_recovery_profile_is_publicly_selectable(self):
  interface=json.loads((PACKAGE/"interface.json").read_text())
  self.assertEqual("1.6",interface["schema_version"])
  self.assertEqual(
   {"kind":"structured_json","profile_selector":{"source":"aggregate_public_input","field":"profile"}},
   interface["public_contracts"]["invocation"]["input_binding"],
  )
  commands={row["id"]:row for row in json.loads((PACKAGE/"commands.json").read_text())["commands"]}
  self.assertEqual("runtime/recover.py",commands["recover-task-workspace-result"]["entrypoint"])
  evals=json.loads((PACKAGE/"evals/evals.json").read_text())["evals"]
  self.assertIn("recover_created_result",{row["input_profile_id"] for row in evals})

 def test_every_command_help_is_side_effect_free(self):
  commands=json.loads((PACKAGE/"commands.json").read_text())
  for command in commands["commands"]:
   before=subprocess.run(["git","status","--porcelain=v1"],cwd=SKILLS.parents[2],text=True,stdout=subprocess.PIPE).stdout
   with self.subTest(command=command["id"]):
    self.assertEqual(0,main(PACKAGE,[command["id"],"--help"]))
   after=subprocess.run(["git","status","--porcelain=v1"],cwd=SKILLS.parents[2],text=True,stdout=subprocess.PIPE).stdout
   self.assertEqual(before,after)

 def test_runtime_and_launchers_do_not_reference_monolith(self):
  for root in (PACKAGE/"runtime",PACKAGE/"scripts"):
   for path in root.iterdir():
    if path.is_file():
     self.assertNotIn("guru_team_trellis.py",path.read_text())
     self.assertNotIn("test_guru_team_trellis.py",path.read_text())

 def test_launchers_are_executable_and_bind_interface_validators(self):
  interface=json.loads((PACKAGE/"interface.json").read_text())
  for validator in interface["validators"]:
   wrapper=PACKAGE/validator["command"]
   self.assertTrue(os.access(wrapper,os.X_OK),wrapper)
   self.assertIn("source \"$LAUNCHER\" "+validator["runtime_command"],wrapper.read_text())

if __name__=="__main__": unittest.main()
