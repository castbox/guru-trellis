from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
from jsonschema import Draft202012Validator

PACKAGE=Path(__file__).resolve().parents[1]
SKILLS=PACKAGE.parents[1]
RUNTIME=SKILLS/"runtime"
LOCAL=PACKAGE/"runtime"
FINISH_SCHEMA=next(path for path in (
 SKILLS.parent/"schemas/finish-summary.schema.json",
 SKILLS.parents[1]/"workflows/guru-team/schemas/finish-summary.schema.json",
) if path.is_file())
for path in (SKILLS,LOCAL):
 if str(path) not in sys.path:sys.path.insert(0,str(path))
from runtime.command import main
from common import check_recovery,consume_recovery,observe_base_current,preview,record_recovery
from check import run as check_run
from invoke import run as invoke_run

class PackageLocalRuntimeTest(unittest.TestCase):
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
  self.assertIn("export PYTHONDONTWRITEBYTECODE=1",(RUNTIME/"launch.sh").read_text())

 def test_real_installed_public_wrapper_is_current_without_python_cache_residue(self):
  with tempfile.TemporaryDirectory() as name:
   case=Path(name);repo=case/"repo";inputs=case/"inputs";inputs.mkdir();repo.mkdir()
   guru=repo/".trellis/guru-team";installed_package=guru/"skills/packages"/PACKAGE.name
   ignore=shutil.ignore_patterns("__pycache__","*.pyc","*.pyo")
   shutil.copytree(PACKAGE,installed_package,ignore=ignore)
   shutil.copytree(SKILLS/"consumers",guru/"skills/consumers",ignore=ignore)
   shutil.copytree(SKILLS/"schemas",guru/"skills/schemas",ignore=ignore)
   shutil.copytree(RUNTIME,guru/"runtime",ignore=ignore)
   (guru/"schemas").mkdir();shutil.copy2(FINISH_SCHEMA,guru/"schemas/finish-summary.schema.json")
   public_wrapper=repo/".agents/skills"/PACKAGE.name/"scripts/invoke.sh";public_wrapper.parent.mkdir(parents=True);shutil.copy2(PACKAGE/"scripts/invoke.sh",public_wrapper);public_wrapper.chmod(0o755)
   resolver=guru/"runtime/resolve-python.sh";resolver.write_text(f'#!/usr/bin/env bash\nshift 2\nexec {json.dumps(sys.executable)} "$@"\n');resolver.chmod(0o755)
   subprocess.run(["git","init","-q","-b","main",str(repo)],check=True);subprocess.run(["git","config","user.name","Installed Wrapper Test"],cwd=repo,check=True);subprocess.run(["git","config","user.email","wrapper@example.invalid"],cwd=repo,check=True)
   subprocess.run(["git","add","."],cwd=repo,check=True);subprocess.run(["git","commit","-q","-m","installed fixture"],cwd=repo,check=True);subprocess.run(["git","remote","add","origin","https://github.com/example/guru-extension.git"],cwd=repo,check=True)
   head=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip();subprocess.run(["git","update-ref","refs/remotes/origin/main",head],cwd=repo,check=True)
   public={"profile":"pre_task","source_exit":"synced","mode":"workflow","change_input":{"issue_refs":["#300"],"pr_refs":[],"branches":[],"paths":["trellis/skills/guru-team/packages/guru-discover-change-context"],"commands":["invoke-guru-discover-change-context"],"config_keys":[],"schema_fields":["base_current"],"symbols":["check_owner_binding"],"terms":["public wrapper"],"queries":["Discovery public wrapper context ready"]},"continuation_id":"issue-300-installed-wrapper"}
   transition={"schema_version":"1.0","transition_id":"base_current:issue300","stage":"base_current","mode":"workflow","repo_locator":str(repo.resolve()),"base":{"source":"explicit","selected_base":"main","remote":"origin","ordered_candidates":["main"],"decision_head":head,"local_base_head":head,"remote_base_head":head,"post_sync_resolution_sha256":"a"*64}}
   public_path=inputs/"public.json";transition_path=inputs/"transition.json";public_path.write_text(json.dumps(public));transition_path.write_text(json.dumps(transition))
   recorder=installed_package/"scripts/record-context-discovery.sh";owner_path=inputs/"owner.json"
   recorded=subprocess.run([str(recorder),"--root",str(repo),"--mode","workflow","--input",str(installed_package/"examples/change-context-owner-result-3.0.json"),"--public-input",str(public_path),"--transition",str(transition_path)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True);owner=json.loads(recorded.stdout);owner_path.write_text(recorded.stdout)
   checked=subprocess.run([str(installed_package/"scripts/check-context-discovery.sh"),"--root",str(repo),"--input",str(owner_path),"--public-input",str(public_path),"--transition",str(transition_path)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
   self.assertEqual(json.loads(checked.stdout)["typed_exit"],"context_ready")
   envelope={"schema_version":"1.0","public_input":public,"transition":transition,"owner_context":{},"owner_result":owner}
   invoked=subprocess.run([str(public_wrapper),"--invocation","-"],cwd=repo,input=json.dumps(envelope),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,env={key:value for key,value in os.environ.items() if key!="PYTHONDONTWRITEBYTECODE"})
   self.assertEqual(json.loads(invoked.stdout)["exit_id"],"context_ready")
   self.assertEqual(subprocess.run(["git","status","--porcelain=v1"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout,"")
   self.assertEqual(list(repo.rglob("__pycache__")),[])
   invalid=json.loads(json.dumps(envelope));invalid["public_input"].pop("continuation_id")
   invalid_result=subprocess.run([str(public_wrapper),"--invocation","-"],cwd=repo,input=json.dumps(invalid),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
   self.assertEqual(json.loads(invalid_result.stdout),{"exit_id":"blocked"})
   mismatch=json.loads(json.dumps(envelope));mismatch["owner_result"]["repository"]["repo"]="other/repository"
   mismatch_result=subprocess.run([str(public_wrapper),"--invocation","-"],cwd=repo,input=json.dumps(mismatch),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
   self.assertEqual(json.loads(mismatch_result.stdout),{"exit_id":"blocked"})
   subprocess.run(["git","commit","--allow-empty","-q","-m","advance"],cwd=repo,check=True);advanced=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip();subprocess.run(["git","update-ref","refs/remotes/origin/main",advanced],cwd=repo,check=True)
   stale_result=subprocess.run([str(public_wrapper),"--invocation","-"],cwd=repo,input=json.dumps(envelope),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
   self.assertEqual(json.loads(stale_result.stdout)["exit_id"],"refresh_base")

 def test_recovery_checkpoint_is_package_owned_and_short_lived(self):
  with tempfile.TemporaryDirectory() as name:
   repo=Path(name);subprocess.run(["git","init","-q","-b","feat/context",str(repo)],check=True);td=repo/".trellis/tasks/08-12-context";td.mkdir(parents=True);task={"id":"08-12-context","status":"in_progress","branch":"feat/context"};(td/"task.json").write_text(json.dumps(task));payload=json.loads((PACKAGE/"examples/change-context-owner-result-3.0.json").read_text());payload["mode"]="workflow";path=record_recovery(PACKAGE,repo,td,task,payload,"resume-context");self.assertTrue(path.is_file());self.assertEqual(path,check_recovery(PACKAGE,repo,td,task,payload,"resume-context"));consume_recovery(path);self.assertFalse(path.exists());self.assertFalse(path.parent.exists())

 def test_live_base_observer_classifies_current_refresh_and_blocked_without_mutation(self):
  with tempfile.TemporaryDirectory() as name:
   repo=Path(name);subprocess.run(["git","init","-q","-b","main",str(repo)],check=True)
   subprocess.run(["git","config","user.name","Observer Test"],cwd=repo,check=True);subprocess.run(["git","config","user.email","observer@example.invalid"],cwd=repo,check=True)
   (repo/"tracked.txt").write_text("one\n");subprocess.run(["git","add","tracked.txt"],cwd=repo,check=True);subprocess.run(["git","commit","-q","-m","initial"],cwd=repo,check=True)
   subprocess.run(["git","remote","add","origin","https://github.com/example/guru-extension.git"],cwd=repo,check=True)
   head=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip();subprocess.run(["git","update-ref","refs/remotes/origin/main",head],cwd=repo,check=True)
   public={"profile":"pre_task","source_exit":"synced","mode":"workflow","change_input":{"issue_refs":["#295"],"pr_refs":[],"branches":[],"paths":[],"commands":[],"config_keys":[],"schema_fields":[],"symbols":[],"terms":[],"queries":[]},"continuation_id":"observer"}
   transition={"schema_version":"1.0","transition_id":"base_current:test","stage":"base_current","mode":"workflow","repo_locator":str(repo),"base":{"source":"explicit","selected_base":"main","remote":"origin","ordered_candidates":["main"],"decision_head":head,"local_base_head":head,"remote_base_head":head,"post_sync_resolution_sha256":"a"*64}}
   before=subprocess.run(["git","status","--porcelain=v1"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout
   current=observe_base_current(PACKAGE,public,transition);self.assertEqual(current["classification"],"current");self.assertEqual(current["observation"]["repo"],"example/guru-extension")
   self.assertEqual(before,subprocess.run(["git","status","--porcelain=v1"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout)
   with tempfile.TemporaryDirectory() as inputs_name:
    inputs=Path(inputs_name);owner=json.loads((PACKAGE/"examples/change-context-owner-result-3.0.json").read_text());owner["repository"]["repo"]="other/repository"
    public_path=inputs/"public.json";transition_path=inputs/"transition.json";owner_path=inputs/"owner.json";invocation_path=inputs/"invocation.json"
    public_path.write_text(json.dumps(public));transition_path.write_text(json.dumps(transition));owner_path.write_text(json.dumps(owner));invocation_path.write_text(json.dumps({"schema_version":"1.0","public_input":public,"transition":transition,"owner_context":{},"owner_result":owner}))
    invoked=invoke_run(PACKAGE,{},["--root",str(repo),"--invocation",str(invocation_path)]);self.assertEqual(invoked,{"exit_id":"blocked"})
    checked=check_run(PACKAGE,{"id":"check-context-discovery"},["--root",str(repo),"--input",str(owner_path),"--public-input",str(public_path),"--transition",str(transition_path)]);self.assertEqual(checked["typed_exit"],"blocked");self.assertEqual(checked["reason"],"repository_mismatch")
    malformed=dict(owner);malformed.pop("repository");owner_path.write_text(json.dumps(malformed));invocation_path.write_text(json.dumps({"schema_version":"1.0","public_input":public,"transition":transition,"owner_context":{},"owner_result":malformed}))
    self.assertEqual(invoke_run(PACKAGE,{},["--root",str(repo),"--invocation",str(invocation_path)]),{"exit_id":"blocked"})
    malformed_checked=check_run(PACKAGE,{"id":"check-context-discovery"},["--root",str(repo),"--input",str(owner_path),"--public-input",str(public_path),"--transition",str(transition_path)]);self.assertEqual(malformed_checked["typed_exit"],"blocked");self.assertEqual(malformed_checked["reason"],"schema_mismatch")
   subprocess.run(["git","commit","--allow-empty","-q","-m","advance"],cwd=repo,check=True);advanced=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip();subprocess.run(["git","update-ref","refs/remotes/origin/main",advanced],cwd=repo,check=True)
   self.assertEqual(observe_base_current(PACKAGE,public,transition)["classification"],"refresh_base")
   transition["base"].update({"decision_head":advanced,"local_base_head":advanced,"remote_base_head":advanced})
   (repo/"tracked.txt").write_text("dirty\n");self.assertEqual(observe_base_current(PACKAGE,public,transition)["reason"],"dirty_authority")
   subprocess.run(["git","restore","tracked.txt"],cwd=repo,check=True);subprocess.run(["git","switch","-q","-c","other"],cwd=repo,check=True)
   self.assertEqual(observe_base_current(PACKAGE,public,transition)["reason"],"wrong_authority_branch")

 def test_history_preview_reads_finish_summary_index_only(self):
  with tempfile.TemporaryDirectory() as name:
   repo=Path(name);(repo/".git").mkdir();(repo/".trellis/guru-team/schemas").mkdir(parents=True);shutil.copy2(FINISH_SCHEMA,repo/".trellis/guru-team/schemas/finish-summary.schema.json")
   archive=repo/".trellis/tasks/archive/2026-08/context";archive.mkdir(parents=True)
   index={"problem":"Context was missing.","outcome":"Context is available.","changed_behavior":["Added context preview."],"affected_surfaces":[{"kind":"workflow","name":"context","paths":["docs/context.md"],"change":"Added preview."}],"contract_changes":[],"search_terms":{"issue_refs":["#195"],"pr_refs":[],"branches":[],"paths":["docs/context.md"],"commands":["preview-change-context-history"],"config_keys":[],"schema_fields":[],"symbols":[],"phrases":["context preview 已完成","preview-change-context-history 命令已完成","context 检索已完成"]},"retrieval_text":"context preview and history"}
   (archive/"finish-summary.json").write_text(json.dumps({"ignored":{"private":True},"index":index}))
   (archive/"finish-summary-index.json").write_text(json.dumps(index))
   result=preview(repo,{"issue_refs":["#195"],"terms":["context"]},20)
   self.assertEqual(len(result["manifest"]),1);self.assertEqual(len(result["candidates"]),1);candidate=result["candidates"][0];self.assertEqual(candidate["finish_summary_path"],".trellis/tasks/archive/2026-08/context/finish-summary.json");self.assertGreater(candidate["score"]["total"],0);self.assertNotIn("retrieval_text",candidate["index_projection"])

 def test_history_preview_isolates_invalid_summaries_and_allows_zero_matches(self):
  with tempfile.TemporaryDirectory() as name:
   repo=Path(name);(repo/".git").mkdir();(repo/".trellis/guru-team/schemas").mkdir(parents=True);shutil.copy2(FINISH_SCHEMA,repo/".trellis/guru-team/schemas/finish-summary.schema.json");archive=repo/".trellis/tasks/archive/2026-08";archive.mkdir(parents=True)
   bad=archive/"bad";bad.mkdir();(bad/"finish-summary.json").write_text("{");missing=archive/"missing";missing.mkdir();(missing/"finish-summary.json").write_text("{}")
   result=preview(repo,{"terms":["no matching archive"]},20)
   self.assertEqual(result["candidates"],[]);self.assertEqual([row["error_code"] for row in result["invalid"]],["invalid_json","missing_index"])

if __name__=="__main__": unittest.main()
