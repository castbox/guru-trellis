from __future__ import annotations
import copy, io, json, os, shutil, subprocess, sys, tempfile, unittest
from unittest.mock import patch
from pathlib import Path
from jsonschema import Draft202012Validator

PACKAGE=Path(__file__).resolve().parents[1]
SKILLS=PACKAGE.parents[1]
RUNTIME=next(path for path in (SKILLS/"runtime",SKILLS.parent/"runtime") if (path/"command.py").is_file())
LOCAL=PACKAGE/"runtime"
FINISH_SCHEMA=next(path for path in (
 SKILLS.parent/"schemas/finish-summary.schema.json",
 SKILLS.parents[1]/"workflows/guru-team/schemas/finish-summary.schema.json",
) if path.is_file())
for path in (RUNTIME.parent,LOCAL):
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

 def test_real_installed_record_check_invoke_without_input_files_or_residue(self):
  with tempfile.TemporaryDirectory() as name:
   case=Path(name);repo=case/"repo";repo.mkdir()
   guru=repo/".trellis/guru-team";installed_package=guru/"skills/packages"/PACKAGE.name
   ignore=shutil.ignore_patterns("__pycache__","*.pyc","*.pyo")
   shutil.copytree(PACKAGE,installed_package,ignore=ignore)
   shutil.copytree(SKILLS/"consumers",guru/"skills/consumers",ignore=ignore)
   shutil.copytree(SKILLS/"schemas",guru/"skills/schemas",ignore=ignore)
   shutil.copytree(SKILLS/"packages/guru-clarify-requirements/schemas",guru/"skills/packages/guru-clarify-requirements/schemas",ignore=ignore)
   shutil.copytree(RUNTIME,guru/"runtime",ignore=ignore)
   (guru/"schemas").mkdir();shutil.copy2(FINISH_SCHEMA,guru/"schemas/finish-summary.schema.json")
   public_wrapper=repo/".agents/skills"/PACKAGE.name/"scripts/invoke.sh";public_wrapper.parent.mkdir(parents=True);shutil.copy2(PACKAGE/"scripts/invoke.sh",public_wrapper);public_wrapper.chmod(0o755)
   resolver=guru/"runtime/resolve-python.sh";resolver.write_text(f'#!/usr/bin/env bash\nshift 2\nexec {json.dumps(sys.executable)} "$@"\n');resolver.chmod(0o755)
   subprocess.run(["git","init","-q","-b","main",str(repo)],check=True);subprocess.run(["git","config","user.name","Installed Wrapper Test"],cwd=repo,check=True);subprocess.run(["git","config","user.email","wrapper@example.invalid"],cwd=repo,check=True)
   subprocess.run(["git","add","."],cwd=repo,check=True);subprocess.run(["git","commit","-q","-m","installed fixture"],cwd=repo,check=True);subprocess.run(["git","remote","add","origin","https://github.com/example/guru-extension.git"],cwd=repo,check=True)
   head=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip();subprocess.run(["git","update-ref","refs/remotes/origin/main",head],cwd=repo,check=True)
   public={"profile":"pre_task","source_exit":"synced","mode":"workflow","change_input":{"issue_refs":["#300"],"pr_refs":[],"branches":[],"paths":["trellis/skills/guru-team/packages/guru-discover-change-context"],"commands":["invoke-guru-discover-change-context"],"config_keys":[],"schema_fields":["base_current"],"symbols":["check_owner_binding"],"terms":["public wrapper"],"queries":["Discovery public wrapper context ready"]},"continuation_id":"issue-300-installed-wrapper"}
   transition={"schema_version":"1.0","transition_id":"base_current:issue300","stage":"base_current","mode":"workflow","repo_locator":str(repo.resolve()),"base":{"source":"explicit","selected_base":"main","remote":"origin","ordered_candidates":["main"],"decision_head":head,"local_base_head":head,"remote_base_head":head,"post_sync_resolution_sha256":"a"*64}}
   recorder=installed_package/"scripts/record-context-discovery.sh"
   checker=installed_package/"scripts/check-context-discovery.sh"
   def snapshot():
    return {str(p.relative_to(repo)):p.read_bytes() for p in repo.rglob("*") if p.is_file() and ".git" not in p.relative_to(repo).parts}
   def call(wrapper,envelope,code=0,extra=()):
    before=snapshot()
    result=subprocess.run([str(wrapper),"--root",str(repo),"--invocation","-",*extra],cwd=repo,input=envelope if isinstance(envelope,str) else json.dumps(envelope),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={key:value for key,value in os.environ.items() if key!="PYTHONDONTWRITEBYTECODE"})
    self.assertEqual(result.returncode,code,(result.stdout,result.stderr))
    self.assertEqual(snapshot(),before)
    self.assertEqual(list(repo.rglob("__pycache__")),[])
    return json.loads(result.stdout)
   initial=snapshot()
   envelope={"schema_version":"1.0","public_input":public,"transition":transition,"owner_context":{},"owner_result":json.loads((PACKAGE/"examples/change-context-owner-result-3.0.json").read_text())}
   for mode in ("workflow","standalone"):
    envelope["public_input"]["mode"]=mode;envelope["transition"]["mode"]=mode
    envelope["owner_result"]=call(recorder,envelope)
    checked=call(checker,envelope,extra=("--expected-result-sha256",envelope["owner_result"]["result_identity"]["result_sha256"]))
    self.assertEqual(checked["typed_exit"],"context_ready")
    output=call(public_wrapper,envelope)
    self.assertEqual(output["exit_id"],"context_ready")
    interface=json.loads((PACKAGE/"interface.json").read_text())
    projection=next(p for p in interface["public_contracts"]["projections"] if p["exit_id"]=="context_ready")
    handoff={p["target"]:output[p["source"]] for p in projection["mappings"]}
    consumer_schema=json.loads((guru/"skills/packages/guru-clarify-requirements/schemas/public-initial-change-request-input-2.0.schema.json").read_text())
    self.assertEqual([],list(Draft202012Validator(consumer_schema).iter_errors(handoff)))
    transition_schema=json.loads((guru/"skills/consumers/workflow/stage0/transitions/context-current.schema.json").read_text())
    self.assertEqual([],list(Draft202012Validator(transition_schema).iter_errors(output["transition"])))
    self.assertEqual(set(output),{"exit_id","handoff_profile","handoff_mode","handoff_target_locator","handoff_continuation_id","duplicate_snapshot","transition"})
   self.assertEqual(snapshot(),initial)
   for wrapper in (recorder,checker,public_wrapper):
    with self.subTest(wrapper=wrapper.name):
     for raw in ("", "{", "{}{}", "[]"):
      self.assertEqual(call(wrapper,raw,2)["code"],"invalid_json")
     for key in envelope:
      missing=copy.deepcopy(envelope);missing.pop(key)
      self.assertEqual(call(wrapper,missing,2)["code"],"schema_mismatch")
     malformed=copy.deepcopy(envelope);malformed["owner_result"]=[]
     self.assertEqual(call(wrapper,malformed,2)["code"],"schema_mismatch")
     unknown=copy.deepcopy(envelope);unknown["unexpected"]=True
     self.assertEqual(call(wrapper,unknown,2)["code"],"schema_mismatch")
   for wrapper in (recorder,checker):
    legacy=subprocess.run([str(wrapper),"--root",str(repo),"--public-input","-","--transition","-","--input","-"],input=json.dumps(public),text=True,capture_output=True)
    self.assertEqual(legacy.returncode,2)
    self.assertEqual(json.loads(legacy.stdout)["code"],"invalid_arguments")
   invalid=json.loads(json.dumps(envelope));invalid["public_input"].pop("continuation_id")
   self.assertEqual(call(public_wrapper,invalid),{"exit_id":"blocked"})
   self.assertEqual(call(checker,invalid)["typed_exit"],"blocked")
   self.assertEqual(call(recorder,invalid,2)["code"],"schema_mismatch")
   mismatch=json.loads(json.dumps(envelope));mismatch["owner_result"]["repository"]["repo"]="other/repository"
   self.assertEqual(call(public_wrapper,mismatch),{"exit_id":"blocked"})
   self.assertEqual(call(checker,mismatch)["reason"],"repository_mismatch")
   self.assertEqual(call(recorder,mismatch,3)["code"],"stale_identity")
   dirty=repo/"ordinary-edit.txt";dirty.write_text("in-progress work\n")
   self.assertEqual(call(checker,envelope)["reason"],"dirty_authority")
   self.assertEqual(call(public_wrapper,envelope),{"exit_id":"blocked"})
   self.assertEqual(call(recorder,envelope,3)["code"],"stale_identity")
   dirty.unlink()
   subprocess.run(["git","switch","-q","-c","other"],cwd=repo,check=True)
   self.assertEqual(call(checker,envelope)["reason"],"wrong_authority_branch")
   self.assertEqual(call(public_wrapper,envelope),{"exit_id":"blocked"})
   self.assertEqual(call(recorder,envelope,3)["code"],"stale_identity")
   subprocess.run(["git","switch","-q","main"],cwd=repo,check=True)
   subprocess.run(["git","commit","--allow-empty","-q","-m","advance"],cwd=repo,check=True);advanced=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip();subprocess.run(["git","update-ref","refs/remotes/origin/main",advanced],cwd=repo,check=True)
   self.assertEqual(call(public_wrapper,envelope)["exit_id"],"refresh_base")
   self.assertEqual(call(checker,envelope)["typed_exit"],"refresh_base")
   self.assertEqual(call(recorder,envelope,3)["code"],"stale_identity")
   self.assertEqual(snapshot(),initial)
   self.assertEqual(subprocess.run(["git","status","--porcelain=v1","--ignored"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout,"")

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
   owner=json.loads((PACKAGE/"examples/change-context-owner-result-3.0.json").read_text());owner["repository"]["repo"]="other/repository"
   envelope={"schema_version":"1.0","public_input":public,"transition":transition,"owner_context":{},"owner_result":owner}
   def run_envelope(run,command):
    with patch("sys.stdin",io.StringIO(json.dumps(envelope))):return run(PACKAGE,command,["--root",str(repo),"--invocation","-"])
   self.assertEqual(run_envelope(invoke_run,{}),{"exit_id":"blocked"})
   checked=run_envelope(check_run,{"id":"check-context-discovery"});self.assertEqual(checked["typed_exit"],"blocked");self.assertEqual(checked["reason"],"repository_mismatch")
   envelope["owner_result"].pop("repository")
   self.assertEqual(run_envelope(invoke_run,{}),{"exit_id":"blocked"})
   malformed_checked=run_envelope(check_run,{"id":"check-context-discovery"});self.assertEqual(malformed_checked["typed_exit"],"blocked");self.assertEqual(malformed_checked["reason"],"schema_mismatch")
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
