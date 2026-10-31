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
from runtime.io import CommandError, project_intermediate_receipt
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
from runtime.delivery_projection.tests.upstream_fixture import install_common, public_task
from common import active_task,check_recovery,consume_recovery,observe_base_current,preview,record_recovery
from check import run as check_run
from invoke import run as invoke_run

class PackageLocalRuntimeTest(unittest.TestCase):
 def test_command_and_error_contract_close(self):
  commands=json.loads((PACKAGE/"commands.json").read_text())
  catalog=json.loads((PACKAGE/"errors/catalog.json").read_text())
  command_schema=json.loads((SKILLS/"schemas/skill-commands-1.1.schema.json").read_text())
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
   ignore=shutil.ignore_patterns("__pycache__",".pytest_cache","*.pyc","*.pyo")
   shutil.copytree(PACKAGE,installed_package,ignore=ignore)
   shutil.copytree(SKILLS/"consumers",guru/"skills/consumers",ignore=ignore)
   shutil.copytree(SKILLS/"schemas",guru/"skills/schemas",ignore=ignore)
   shutil.copytree(SKILLS/"packages/guru-clarify-requirements/schemas",guru/"skills/packages/guru-clarify-requirements/schemas",ignore=ignore)
   shutil.copytree(RUNTIME,guru/"runtime",ignore=ignore)
   (guru/"schemas").mkdir();shutil.copy2(FINISH_SCHEMA,guru/"schemas/finish-summary.schema.json")
   public_wrapper=repo/".agents/skills"/PACKAGE.name/"scripts/invoke.sh";public_wrapper.parent.mkdir(parents=True);shutil.copy2(PACKAGE/"scripts/invoke.sh",public_wrapper);public_wrapper.chmod(0o755)
   resolver=guru/"runtime/resolve-python.sh";resolver.write_text(f'#!/usr/bin/env bash\nshift 2\nexec {json.dumps(sys.executable)} "$@"\n');resolver.chmod(0o755)
   subprocess.run(["git","init","-q","-b","main",str(repo)],check=True);subprocess.run(["git","config","user.name","Installed Wrapper Test"],cwd=repo,check=True);subprocess.run(["git","config","user.email","wrapper@example.invalid"],cwd=repo,check=True)
   (repo/".gitignore").write_text(".trellis/tasks/archive/\n")
   subprocess.run(["git","add","."],cwd=repo,check=True);subprocess.run(["git","commit","-q","-m","installed fixture"],cwd=repo,check=True);subprocess.run(["git","remote","add","origin","https://github.com/example/guru-extension.git"],cwd=repo,check=True)
   head=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip();subprocess.run(["git","update-ref","refs/remotes/origin/main",head],cwd=repo,check=True)
   public={"clarify_profile": "standard_intake", "profile":"pre_task","source_exit":"synced","mode":"workflow","change_input":{"issue_refs":["#300"],"pr_refs":[],"branches":[],"paths":["trellis/skills/guru-team/packages/guru-discover-change-context"],"commands":["invoke-guru-discover-change-context"],"config_keys":[],"schema_fields":["base_current"],"symbols":["check_owner_binding"],"terms":["public wrapper"],"queries":["Discovery public wrapper context ready"]},"continuation_id":"issue-300-installed-wrapper"}
   transition={"schema_version":"1.0","transition_id":"base_current:issue300","stage":"base_current","mode":"workflow","repo_locator":str(repo.resolve()),"base":{"source":"explicit","selected_base":"main","remote":"origin","ordered_candidates":["main"],"decision_head":head,"local_base_head":head,"remote_base_head":head,"post_sync_resolution_sha256":"a"*64}}
   recorder=installed_package/"scripts/record-context-discovery.sh"
   checker=installed_package/"scripts/check-context-discovery.sh"
   def snapshot():
    return {str(p.relative_to(repo)):p.read_bytes() for p in repo.rglob("*") if p.is_file() and ".git" not in p.relative_to(repo).parts}
   def call(wrapper,envelope,code=0,extra=(),with_stderr=False):
    before=snapshot()
    result=subprocess.run([str(wrapper),"--root",str(repo),"--invocation","-",*extra],cwd=repo,input=envelope if isinstance(envelope,str) else json.dumps(envelope),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={key:value for key,value in os.environ.items() if key!="PYTHONDONTWRITEBYTECODE"})
    self.assertEqual(result.returncode,code,(result.stdout,result.stderr))
    self.assertEqual(snapshot(),before)
    self.assertEqual(list(repo.rglob("__pycache__")),[])
    output=json.loads(result.stdout)
    output=project_intermediate_receipt(output,SKILLS/"schemas") if code==0 and wrapper!=public_wrapper else output
    return (output,result.stderr) if with_stderr else output
   def blocked_diagnostic(envelope,field):
    checked=call(checker,envelope)
    self.assertEqual((checked["status"],checked["typed_exit"],checked["reason"]),("passed","blocked","stale_identity"))
    self.assertEqual(set(checked["diagnostic"]),{"code","field_path","remediation"})
    self.assertEqual(checked["diagnostic"]["field_path"],field)
    output,stderr=call(public_wrapper,envelope,with_stderr=True)
    self.assertEqual(output,{"exit_id":"blocked"})
    self.assertEqual(json.loads(stderr),checked["diagnostic"])
    self.assertNotIn("中文证据",stderr)
    self.assertNotIn("draft:",stderr)
    return checked["diagnostic"]
   initial=snapshot()
   envelope={"schema_version":"1.0","public_input":public,"transition":transition,"owner_context":{},"owner_result":json.loads((PACKAGE/"examples/change-context-owner-result-3.0.json").read_text())}
   for mode in ("workflow","standalone"):
    envelope["public_input"]["mode"]=mode;envelope["transition"]["mode"]=mode
    envelope["owner_result"]["ai_review_gate"]["reason"]="中文证据：当前调查与范围一致。"
    envelope["owner_result"]=call(recorder,envelope)
    checked=call(checker,envelope,extra=("--expected-result-sha256",envelope["owner_result"]["result_identity"]["result_sha256"]))
    self.assertEqual(checked["typed_exit"],"context_ready")
    output=call(public_wrapper,envelope)
    self.assertEqual(output["exit_id"],"context_ready")
    interface=json.loads((PACKAGE/"interface.json").read_text())
    projection=next(p for p in interface["public_contracts"]["projections"] if p["exit_id"]=="context_ready")
    handoff={p["target"]:output[p["source"]] for p in projection["mappings"] if p["source"] in output}
    consumer_schema=json.loads((guru/"skills/packages/guru-clarify-requirements/schemas/public-standard-intake-input.schema.json").read_text())
    self.assertEqual([],list(Draft202012Validator(consumer_schema).iter_errors(handoff)))
    transition_schema=json.loads((guru/"skills/consumers/workflow/stage0/transitions/context-current.schema.json").read_text())
    self.assertEqual([],list(Draft202012Validator(transition_schema).iter_errors(output["transition"])))
    self.assertEqual(set(output),{"exit_id","handoff_profile","handoff_mode","handoff_target_locator","handoff_continuation_id","duplicate_snapshot","transition"})
    # A current input and an earlier genuine recorded result can be paired by mistake.
    changed=copy.deepcopy(envelope)
    changed["public_input"]["change_input"]["terms"]=["current local fix"]
    current_result=call(recorder,changed)
    blocked_diagnostic(changed,"owner_result.change_input.terms[0]")
    changed["owner_result"]=current_result
    self.assertEqual(call(public_wrapper,changed)["exit_id"],"context_ready")
    if mode=="workflow":workflow_result=copy.deepcopy(envelope["owner_result"])
    else:
     mispaired=copy.deepcopy(envelope);mispaired["owner_result"]=workflow_result
     blocked_diagnostic(mispaired,"owner_result.mode")
    # Simulate an ordinary caller decoding each stdout chunk independently.
    complete=json.dumps(envelope,ensure_ascii=False).encode("utf-8")
    boundary=complete.index("中文证据".encode("utf-8"))+1
    split_read=complete[:boundary].decode("utf-8",errors="replace")+complete[boundary:].decode("utf-8",errors="replace")
    info=blocked_diagnostic(split_read,"owner_result.result_identity.payload_sha256")
    self.assertIn("does not establish",info["remediation"])
    self.assertEqual(call(checker,complete.decode("utf-8"))["typed_exit"],"context_ready")
    self.assertEqual(call(public_wrapper,complete.decode("utf-8"))["exit_id"],"context_ready")
   # A context return for another real target keeps the original direct error contract.
   returning=copy.deepcopy(envelope)
   returning["public_input"]={key:value for key,value in returning["public_input"].items() if key!="clarify_profile"}
   returning["public_input"].update({"profile":"context_request","source_exit":"needs_context","return_identity":{"profile":"standard_intake","target_locator":"https://github.com/example/guru-extension/issues/301","continuation_id":public["continuation_id"]}})
   returning["owner_result"]=call(recorder,returning)
   target_error=call(public_wrapper,returning,3)
   self.assertEqual((target_error["code"],target_error["field_path"]),("stale_identity","return_identity.target_locator"))
   self.assertIn("needs_context",target_error["remediation"])
   # A newly visible legacy archive row changes history without changing base refs.
   archive=repo/".trellis/tasks/archive/legacy-context";archive.mkdir(parents=True)
   summary=archive/"finish-summary.json";summary.write_text("{}\n")
   current_history=call(recorder,envelope)
   blocked_diagnostic(envelope,"owner_result.history_preview.archive_manifest_sha256")
   history_envelope=copy.deepcopy(envelope);history_envelope["owner_result"]=current_history
   self.assertEqual(call(public_wrapper,history_envelope)["exit_id"],"context_ready")
   summary.unlink();archive.rmdir();archive.parent.rmdir();archive.parent.parent.rmdir()
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
   wrong_authoring=copy.deepcopy(envelope);wrong_authoring["owner_result"]["repository"]["selected_base"]="another-base"
   authoring_error=call(recorder,wrong_authoring,2)
   self.assertEqual((authoring_error["code"],authoring_error["field_path"]),("schema_mismatch","repository.selected_base"))
   dirty=repo/"ordinary-edit.txt";dirty.write_text("in-progress work\n")
   dirty_check=call(checker,envelope)
   self.assertEqual(dirty_check["reason"],"dirty_authority")
   self.assertEqual(dirty_check["diagnostic"]["field_path"],"base_current.clean")
   self.assertEqual(call(public_wrapper,envelope),{"exit_id":"blocked"})
   self.assertEqual(call(recorder,envelope,3)["code"],"stale_identity")
   dirty.unlink()
   subprocess.run(["git","switch","-q","-c","other"],cwd=repo,check=True)
   branch_check=call(checker,envelope)
   self.assertEqual(branch_check["reason"],"wrong_authority_branch")
   self.assertEqual(branch_check["diagnostic"]["field_path"],"base_current.authority_branch")
   self.assertEqual(call(public_wrapper,envelope),{"exit_id":"blocked"})
   self.assertEqual(call(recorder,envelope,3)["code"],"stale_identity")
   subprocess.run(["git","switch","-q","main"],cwd=repo,check=True)
   subprocess.run(["git","commit","--allow-empty","-q","-m","advance"],cwd=repo,check=True);advanced=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip();subprocess.run(["git","update-ref","refs/remotes/origin/main",advanced],cwd=repo,check=True)
   self.assertEqual(call(public_wrapper,envelope)["exit_id"],"refresh_base")
   refresh_check=call(checker,envelope)
   self.assertEqual(refresh_check["typed_exit"],"refresh_base")
   self.assertEqual(refresh_check["reason"],"base_head_advanced")
   self.assertEqual(refresh_check["diagnostic"]["field_path"],"base_current.decision_head")
   self.assertIn("guru-sync-base",refresh_check["diagnostic"]["remediation"])
   self.assertEqual(call(recorder,envelope,3)["code"],"stale_identity")
   refreshed=copy.deepcopy(envelope)
   refreshed["transition"]["base"].update({"decision_head":advanced,"local_base_head":advanced,"remote_base_head":advanced})
   fresh_result=call(recorder,refreshed)
   blocked_diagnostic(refreshed,"owner_result.base_observation.decision_head")
   refreshed["owner_result"]=fresh_result
   self.assertEqual(call(public_wrapper,refreshed)["exit_id"],"context_ready")
   self.assertEqual(snapshot(),initial)
   self.assertEqual(subprocess.run(["git","status","--porcelain=v1","--ignored"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout,"")

 def test_recovery_checkpoint_is_package_owned_and_short_lived(self):
  with tempfile.TemporaryDirectory() as name:
   repo=Path(name);subprocess.run(["git","init","-q","-b","feat/context",str(repo)],check=True);td=repo/".trellis/tasks/08-12-context";td.mkdir(parents=True);task={"id":"08-12-context","status":"in_progress","branch":"feat/context"};(td/"task.json").write_text(json.dumps(task));payload=json.loads((PACKAGE/"examples/change-context-owner-result-3.0.json").read_text());payload["mode"]="workflow";path=record_recovery(PACKAGE,repo,td,task,payload,"resume-context");self.assertTrue(path.is_file());self.assertEqual(path,check_recovery(PACKAGE,repo,td,task,payload,"resume-context"));consume_recovery(path);self.assertFalse(path.exists());self.assertFalse(path.parent.exists())

 def test_active_task_uses_current_checkout_binding_without_legacy_branch(self):
  with tempfile.TemporaryDirectory() as name:
   repo=Path(name);subprocess.run(["git","init","-q","-b","feat/context",str(repo)],check=True)
   subprocess.run(["git","-C",str(repo),"-c","user.name=Test","-c","user.email=test@example.invalid","commit","--allow-empty","-q","-m","seed"],check=True)
   td=repo/".trellis/tasks/08-12-context";td.mkdir(parents=True)
   task={"id":"08-12-context","name":"context","title":"Context","description":"Context fixture","status":"in_progress","priority":"P2","createdAt":"2026-01-01","notes":"","lifecycle_generation":0,"source":{"kind":"no_issue"},"children":[],"relatedFiles":[],"meta":{},**{k:None for k in ("dev_type","scope","package","completedAt","base_branch","worktree_path","commit","pr_url","parent")}};(td/"task.json").write_text(json.dumps(task))
   install_common(repo);task=public_task(task);(td/"task.json").write_text(json.dumps(task))
   store=BranchBindingStore(inspect_repository(repo));key=TaskLifecycleKey(task["id"],0)
   ref=".trellis/tasks/08-12-context"
   with self.assertRaises(CommandError) as missing:active_task(repo,ref)
   self.assertEqual(("stale_identity","branch_binding",3),(missing.exception.code,missing.exception.field_path,missing.exception.exit_status))
   binding=store.establish(key,"feat/other")
   with self.assertRaises(CommandError) as wrong:active_task(repo,ref)
   self.assertEqual(("stale_identity","worktree",3),(wrong.exception.code,wrong.exception.field_path,wrong.exception.exit_status))
   payload=binding.as_dict();payload["branch_name"]="feat/context";store.path_for(key).write_text(json.dumps(payload))
   self.assertEqual((td.resolve(),task),active_task(repo,ref))
   # Legacy status cannot become a current execution authority.
   task["status"]="completed";(td/"task.json").write_text(json.dumps(task))
   with self.assertRaises(CommandError) as stale:active_task(repo,ref)
   self.assertEqual("stale_identity",stale.exception.code)

 def test_live_base_observer_classifies_current_refresh_and_blocked_without_mutation(self):
  with tempfile.TemporaryDirectory() as name:
   repo=Path(name);subprocess.run(["git","init","-q","-b","main",str(repo)],check=True)
   subprocess.run(["git","config","user.name","Observer Test"],cwd=repo,check=True);subprocess.run(["git","config","user.email","observer@example.invalid"],cwd=repo,check=True)
   (repo/"tracked.txt").write_text("one\n");subprocess.run(["git","add","tracked.txt"],cwd=repo,check=True);subprocess.run(["git","commit","-q","-m","initial"],cwd=repo,check=True)
   subprocess.run(["git","remote","add","origin","https://github.com/example/guru-extension.git"],cwd=repo,check=True)
   head=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip();subprocess.run(["git","update-ref","refs/remotes/origin/main",head],cwd=repo,check=True)
   public={"clarify_profile": "standard_intake", "profile":"pre_task","source_exit":"synced","mode":"workflow","change_input":{"issue_refs":["#295"],"pr_refs":[],"branches":[],"paths":[],"commands":[],"config_keys":[],"schema_fields":[],"symbols":[],"terms":[],"queries":[]},"continuation_id":"observer"}
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
