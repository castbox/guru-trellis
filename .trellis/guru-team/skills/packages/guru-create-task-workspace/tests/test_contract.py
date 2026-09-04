from __future__ import annotations
import copy,hashlib,importlib.util,json,os,shutil,subprocess,sys,tempfile,unittest
from unittest import mock
from datetime import datetime,timezone
from pathlib import Path
PACKAGE=Path(__file__).resolve().parents[1];SKILLS=next(parent for parent in PACKAGE.parents if (parent/"runtime").is_dir());LOCAL=PACKAGE/"runtime"
for p in (SKILLS,LOCAL):
 if str(p) not in sys.path:sys.path.insert(0,str(p))
from runtime.io import CommandError
import check,common,execute,invoke,record
class WorkspaceTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.parent=Path(self.tmp.name);self.repo=self.parent/"repo";self.remote=self.parent/"remote.git";subprocess.run(["git","init","-q","--bare",str(self.remote)],check=True);subprocess.run(["git","init","-q","-b","main",str(self.repo)],check=True);self.git("config","user.name","Test");self.git("config","user.email","test@example.invalid");(self.repo/"seed").write_text("seed\n");self.git("add","seed");self.git("commit","-qm","seed");self.git("remote","add","origin",str(self.remote));self.git("push","-qu","origin","main");self.head=self.git("rev-parse","HEAD");self.configure();self.plan=self.make_plan()
 def tearDown(self):self.tmp.cleanup()
 def git(self,*a):return subprocess.run(["git",*a],cwd=self.repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip()
 def write(self,n,v):p=self.repo/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v));return p
 def configure(self,mode="worktree",root=""):
  p=self.repo/".trellis/guru-team/config.yml";p.parent.mkdir(parents=True,exist_ok=True);p.write_text(f"workspace_mode: {mode}\nworktree_root: {root}\nbase_branch: main\n")
 def refresh(self,plan):
  plan["scope"]["scope_sha256"]=common.digest({k:v for k,v in plan["scope"].items() if k!="scope_sha256"});r=common.digest(common.reviewable(plan));plan["freshness"]["reviewable_plan_sha256"]=r;plan["ai_review_gate"]["reviewed_plan_sha256"]=r;plan["freshness"]["plan_sha256"]=common.plan_digest(plan);return plan
 def make_plan(self):
  task="08-12-027-workspace";plan=json.loads((PACKAGE/"examples/task-workspace-plan.json").read_text());plan["mode"]="standalone";plan["target"].update({"repo":"example/repo","issue_number":27,"url":"https://github.com/example/repo/issues/27","title_sha256":__import__('hashlib').sha256(b"Create a reviewed task workspace").hexdigest(),"body_sha256":__import__('hashlib').sha256(b"").hexdigest()});plan["base"].update({"base_ref":"HEAD","decision_head":self.head,"local_head":self.head,"remote_head":self.head});plan["naming"].update({"branch_name":"feat/027-workspace","workspace_slug":"027-workspace","task_slug":"027-workspace","task_title":"#27 Workspace"});plan["side_effects"]["task_artifacts"]=[f".trellis/tasks/{task}/issue-scope-ledger.json"];plan["side_effects"]["runtime_mappings"]=[".trellis/.runtime/guru-team/workspaces/027-workspace.json",".trellis/.runtime/guru-team/tasks/027-workspace.json"]
  plan["scope"]["primary"].update({"number":27,"url":"https://github.com/example/repo/issues/27"});plan["scope"]["close"]=[copy.deepcopy(plan["scope"]["primary"])];return self.refresh(plan)
 def draft_plan(self,title="Reviewed issue",body="Reviewed body",labels=None):
  labels=list(labels or ["runtime"]);plan=copy.deepcopy(self.plan);reviewed=common.digest({"title":title,"body":body,"labels":labels})
  plan["invocation"].update({"target_kind":"reviewed_draft","action_scope":"github_issue_mutation"});plan["target"].update({"kind":"reviewed_draft","issue_number":None,"url":None,"state":None,"updated_at":None,"title_sha256":hashlib.sha256(title.encode()).hexdigest(),"body_sha256":hashlib.sha256(body.encode()).hexdigest(),"draft":{"draft_id":"draft-112","source_request_sha256":"1"*64,"title":title,"body":body,"labels":labels,"reviewed_draft_sha256":reviewed}});plan["scope"].update({"primary":None,"close":[],"scope_sha256":common.digest({"primary":None,"close":[],"related":[],"followup":[]})});plan["side_effects"].update({"operations":["create_issue"],"task_artifacts":[],"runtime_mappings":[],"command_argv":["create-task-workspace","--input","draft.json"],"stop_after":"created_issue_refresh"});plan["freshness"]["captured_at"]="2026-01-01T00:00:00Z";return self.refresh(plan)
 def issue_row(self,number=112,title="Reviewed issue",body="Reviewed body",labels=None,state="OPEN",created_at="2026-01-01T00:00:01Z",updated_at="2026-01-01T00:00:01Z",repo="example/repo"):
  return {"number":number,"url":f"https://github.com/{repo}/issues/{number}","state":state,"title":title,"body":body,"createdAt":created_at,"updatedAt":updated_at,"labels":[{"name":label} for label in (labels or ["runtime"])]}
 def execute_and_check(self,plan=None):
  plan=plan or self.plan;pp=self.write("plan.json",plan)
  live={"number":27,"url":"https://github.com/example/repo/issues/27","state":"OPEN","title":"Create a reviewed task workspace","body":"","updatedAt":"2026-01-01T00:00:00Z"}
  with mock.patch.object(execute,"github",return_value=live):result=execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  rp=self.write("result.json",result);return result,check.run(PACKAGE,{},["--root",str(self.repo),"--plan-input",str(pp),"--input",str(rp)])
 def assert_no_workspace_writes(self,workspace):
  self.assertFalse(workspace.exists());self.assertNotEqual(0,subprocess.run(["git","show-ref","--verify","--quiet",f"refs/heads/{self.plan['naming']['branch_name']}"],cwd=self.repo).returncode);self.assertFalse((self.repo/".trellis/.runtime/guru-team/tasks/027-workspace.json").exists())
 def workspace_state(self,workspace):
  paths=[workspace/".trellis/tasks/08-12-027-workspace/task.json",self.repo/".trellis/.runtime/guru-team/workspaces/027-workspace.json",self.repo/".trellis/.runtime/guru-team/tasks/027-workspace.json",workspace/".trellis/.runtime/guru-team/workspaces/027-workspace.json",workspace/".trellis/.runtime/guru-team/tasks/027-workspace.json"]
  return {"refs":self.git("show-ref"),"worktrees":self.git("worktree","list","--porcelain"),"repo_status":common.git(self.repo,"status","--porcelain=v1","-z","--untracked-files=all").stdout,"workspace_status":common.git(workspace,"status","--porcelain=v1","-z","--untracked-files=all").stdout,"files":{str(path):path.read_bytes() for path in paths}}
 def mutation_state(self,workspace):
  paths=[workspace/".trellis/tasks/08-12-027-workspace/task.json",workspace/self.plan["side_effects"]["task_artifacts"][0],self.repo/".trellis/.runtime/guru-team/workspaces/027-workspace.json",self.repo/".trellis/.runtime/guru-team/tasks/027-workspace.json",workspace/".trellis/.runtime/guru-team/workspaces/027-workspace.json",workspace/".trellis/.runtime/guru-team/tasks/027-workspace.json"]
  target_status=common.git(workspace,"status","--porcelain=v1","-z","--untracked-files=all").stdout if (workspace/".git").exists() else None
  return {"refs":self.git("show-ref"),"worktrees":self.git("worktree","list","--porcelain"),"source_status":common.git(self.repo,"status","--porcelain=v1","-z","--untracked-files=all").stdout,"target_status":target_status,"files":{str(path):path.read_bytes() if path.is_file() else None for path in paths}}
 def test_prepare_file_entrypoint_loads_package_runtime(self):
  process=subprocess.run([sys.executable,str(LOCAL/"prepare.py"),"--help"],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  self.assertEqual(0,process.returncode,process.stderr);self.assertIn("usage: prepare-task",process.stdout)
 def test_prepare_file_entrypoint_loads_installed_runtime_layout(self):
  root=self.parent/"installed/guru-team";package=root/"skills/packages/guru-create-task-workspace";shutil.copytree(PACKAGE,package);shutil.copytree(SKILLS/"runtime",root/"runtime")
  process=subprocess.run([sys.executable,str(package/"runtime/prepare.py"),"--help"],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  self.assertEqual(0,process.returncode,process.stderr);self.assertIn("usage: prepare-task",process.stdout)
 def test_common_loads_through_shared_dynamic_command_loader_pattern(self):
  path=LOCAL/"common.py";spec=importlib.util.spec_from_file_location("guru_runtime_dynamic_common",path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  resolved=module.WorkspaceConfig("worktree",self.parent,self.repo)
  self.assertEqual(("worktree",self.parent,self.repo),tuple(resolved))
 def test_real_workspace_mutation_check_and_invoke(self):
  pp=self.write("plan.json",self.plan);self.assertEqual(self.plan,record.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)]));result,checked=self.execute_and_check();workspace=(self.parent/"repo-worktrees/027-workspace").resolve();self.assertTrue(workspace.is_dir());mapping=json.loads((self.repo/".trellis/.runtime/guru-team/tasks/027-workspace.json").read_text());self.assertEqual({"schema_version":"1.0","workspace_slug":"027-workspace","workspace_path":str(workspace),"task_artifact_dir":".trellis/tasks/08-12-027-workspace"},{key:mapping[key] for key in ("schema_version","workspace_slug","workspace_path","task_artifact_dir")});self.assertTrue((workspace/".trellis/.runtime/guru-team/tasks/027-workspace.json").is_file());boundary=PACKAGE.parents[0]/"guru-finalize-task/runtime/legacy.py";boundary_result=subprocess.run([sys.executable,str(boundary),"check-workspace-boundary","--root",str(workspace),"--task",".trellis/tasks/08-12-027-workspace","--json"],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);self.assertEqual(0,boundary_result.returncode,boundary_result.stderr);self.assertEqual("ok",json.loads(boundary_result.stdout)["status"]);self.assertNotIn(str(self.parent.resolve()),json.dumps(result));env=self.write("invoke.json",{"result":checked});self.assertEqual({"exit_id":"created"},invoke.run(PACKAGE,{},["--root",str(self.repo),"--invocation",str(env)]))
 def test_absolute_root_create_exact_reuse_and_checker(self):
  absolute=self.parent/"absolute";self.configure(root=str(absolute));result,checked=self.execute_and_check();self.assertEqual("passed",checked["checker"]["status"]);workspace=absolute/"027-workspace";self.assertTrue(workspace.is_dir());plan=copy.deepcopy(self.plan);plan["naming"].update({"branch_disposition":"reuse_exact","workspace_disposition":"reuse_exact","task_disposition":"reuse_exact"});self.refresh(plan);reused,rechecked=self.execute_and_check(plan);self.assertEqual(("created","passed"),(reused["typed_exit"],rechecked["checker"]["status"]));self.assertNotIn(str(absolute),json.dumps(reused))
 def test_relative_root_is_repository_relative(self):
  self.configure(root="../relative-root");result,checked=self.execute_and_check();workspace=(self.parent/"relative-root/027-workspace").resolve();self.assertTrue(workspace.is_dir());self.assertEqual("passed",checked["checker"]["status"]);self.assertEqual(str(workspace),json.loads((self.repo/".trellis/.runtime/guru-team/workspaces/027-workspace.json").read_text())["workspace_path"])
 def test_current_mode_uses_current_checkout_without_worktree_add(self):
  self.configure(mode="current");plan=copy.deepcopy(self.plan);plan["naming"]["workspace_disposition"]="reuse_exact";plan["side_effects"]["operations"].remove("create_worktree");self.refresh(plan);before=len(common.worktrees(self.repo));result,checked=self.execute_and_check(plan);self.assertEqual(before,len(common.worktrees(self.repo)));self.assertEqual("feat/027-workspace",self.git("branch","--show-current"));self.assertTrue((self.repo/plan["side_effects"]["task_artifacts"][0]).is_file());self.assertEqual("passed",checked["checker"]["status"]);self.assertNotIn(str(self.repo),json.dumps(result))
 def test_current_mode_reuses_and_switches_existing_branch(self):
  self.configure(mode="current");self.git("branch","feat/027-workspace");plan=copy.deepcopy(self.plan);plan["naming"].update({"branch_disposition":"reuse_exact","workspace_disposition":"reuse_exact"});plan["side_effects"]["operations"].remove("create_branch");plan["side_effects"]["operations"].remove("create_worktree");self.refresh(plan);before=len(common.worktrees(self.repo));result,checked=self.execute_and_check(plan);self.assertEqual(before,len(common.worktrees(self.repo)));self.assertEqual("feat/027-workspace",self.git("branch","--show-current"));self.assertEqual("passed",checked["checker"]["status"])
 def test_current_mode_reuse_branch_occupied_elsewhere_fails_before_writes(self):
  self.configure(mode="current");occupied=self.parent/"occupied";self.git("worktree","add","-q","-b","feat/027-workspace",str(occupied),"HEAD");plan=copy.deepcopy(self.plan);plan["naming"].update({"branch_disposition":"reuse_exact","workspace_disposition":"reuse_exact"});plan["side_effects"]["operations"].remove("create_branch");plan["side_effects"]["operations"].remove("create_worktree");self.refresh(plan);pp=self.write("occupied.json",plan)
  with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  self.assertEqual("main",self.git("branch","--show-current"));self.assertFalse((self.repo/plan["side_effects"]["task_artifacts"][0]).exists())
 def test_invalid_mode_and_conflict_fail_before_business_writes(self):
  self.configure(mode="pool");pp=self.write("invalid.json",self.plan)
  with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  self.assert_no_workspace_writes(self.parent/"repo-worktrees/027-workspace");self.configure();workspace=self.parent/"repo-worktrees/027-workspace";workspace.mkdir(parents=True)
  with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  self.assert_no_workspace_writes(workspace/"never-created")
 def test_missing_mode_and_current_root_conflict_fail_before_business_writes(self):
  config=self.repo/".trellis/guru-team/config.yml";config.write_text("worktree_root:\n")
  for text in ("worktree_root:\n", "workspace_mode: current\nworktree_root: ../other\n"):
   config.write_text(text);pp=self.write("invalid-config.json",self.plan)
   with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
   self.assert_no_workspace_writes(self.parent/"repo-worktrees/027-workspace")
 def test_duplicate_workspace_config_key_fails_closed(self):
  config=self.repo/".trellis/guru-team/config.yml";config.write_text("workspace_mode: worktree\nworkspace_mode: current\nworktree_root:\n");pp=self.write("duplicate-config.json",self.plan)
  with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  self.assert_no_workspace_writes(self.parent/"repo-worktrees/027-workspace")
 def test_nested_workspace_key_does_not_override_top_level_and_quoted_hash_is_preserved(self):
  config=self.repo/".trellis/guru-team/config.yml";config.write_text("workspace_mode: worktree\nworktree_root: '../root#named' # comment\npublish:\n  workspace_mode: current\n")
  resolved=common.resolve_workspace(self.repo,"027-workspace")
  self.assertEqual((self.parent/"root#named/027-workspace").resolve(),resolved.path)
 def test_unrelated_top_level_list_preserves_empty_workspace_scalar(self):
  config=self.repo/".trellis/guru-team/config.yml";config.write_text("base_branch: main\nbase_branch_candidates:\n  - main\nworkspace_mode: worktree\nworktree_root:\ncloseout_markers:\n  - 'Final Closeout'\n")
  values=common.config(self.repo);resolved=common.resolve_workspace(self.repo,"027-workspace")
  self.assertEqual(["Final Closeout"],values["closeout_markers"]);self.assertEqual("",values["worktree_root"]);self.assertEqual((self.parent/"repo-worktrees/027-workspace").resolve(),resolved.path)
 def test_non_scalar_worktree_root_fails_before_all_workspace_writes(self):
  config=self.repo/".trellis/guru-team/config.yml";workspace=self.parent/"repo-worktrees/027-workspace";pp=self.write("non-scalar-root.json",self.plan)
  cases={"mapping":"worktree_root:\n  path: ../other\n","list":"worktree_root:\n  - ../other\n"}
  for name,root in cases.items():
   with self.subTest(name=name):
    config.write_text(f"workspace_mode: worktree\n{root}base_branch: main\n");before=self.mutation_state(workspace)
    with self.assertRaises(CommandError) as raised:execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
    self.assertEqual(("unsafe_path","worktree_root"),(raised.exception.code,raised.exception.field_path));self.assertEqual(before,self.mutation_state(workspace))
 def test_non_directory_root_parent_fails_before_business_writes(self):
  blocked=self.parent/"blocked";blocked.write_text("not a directory\n");self.configure(root="../blocked/worktrees");pp=self.write("blocked-parent.json",self.plan)
  with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  self.assert_no_workspace_writes(self.parent/"blocked/worktrees/027-workspace")
 def test_mapping_stale_and_checker_mismatch_fail_closed(self):
  mapping=self.repo/".trellis/.runtime/guru-team/tasks/027-workspace.json";mapping.parent.mkdir(parents=True,exist_ok=True);mapping.write_text(json.dumps({"workspace_path":"/wrong"}))
  pp=self.write("mapping-conflict.json",self.plan)
  with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  self.assertFalse((self.parent/"repo-worktrees/027-workspace").exists());mapping.unlink();result,checked=self.execute_and_check();mapping.write_text(json.dumps({"workspace_path":"/stale"}));rp=self.write("checked.json",result);pp=self.write("checked-plan.json",self.plan)
  with self.assertRaises(CommandError):check.run(PACKAGE,{},["--root",str(self.repo),"--plan-input",str(pp),"--input",str(rp)])
 def test_reuse_rejects_stale_target_mapping_before_overwrite(self):
  self.execute_and_check();workspace=self.parent/"repo-worktrees/027-workspace";target_mapping=workspace/".trellis/.runtime/guru-team/tasks/027-workspace.json";target_mapping.write_text(json.dumps({"workspace_path":"/stale"}));plan=copy.deepcopy(self.plan);plan["naming"].update({"branch_disposition":"reuse_exact","workspace_disposition":"reuse_exact","task_disposition":"reuse_exact"});self.refresh(plan);pp=self.write("reuse-stale-target.json",plan)
  with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  self.assertEqual("/stale",json.loads(target_mapping.read_text())["workspace_path"])
 def test_reuse_missing_ledger_fails_before_writes_and_preserves_state(self):
  self.execute_and_check();workspace=self.parent/"repo-worktrees/027-workspace";ledger=workspace/self.plan["side_effects"]["task_artifacts"][0];ledger.unlink();plan=copy.deepcopy(self.plan);plan["naming"].update({"branch_disposition":"reuse_exact","workspace_disposition":"reuse_exact","task_disposition":"reuse_exact"});self.refresh(plan);pp=self.write("reuse-missing-ledger.json",plan);before=self.workspace_state(workspace)
  with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  self.assertFalse(ledger.exists());self.assertEqual(before,self.workspace_state(workspace))
 def test_checker_rejects_every_task_payload_field_drift(self):
  result,_=self.execute_and_check();workspace=self.parent/"repo-worktrees/027-workspace";task_path=workspace/".trellis/tasks/08-12-027-workspace/task.json";expected=json.loads(task_path.read_text());pp=self.write("checker-task-drift-plan.json",self.plan);rp=self.write("checker-task-drift-result.json",result)
  for field in ("name","title","status","creator","scope"):
   with self.subTest(field=field):
    drifted=copy.deepcopy(expected);drifted[field]=f"drifted-{field}";task_path.write_text(json.dumps(drifted))
    with self.assertRaises(CommandError):check.run(PACKAGE,{},["--root",str(self.repo),"--plan-input",str(pp),"--input",str(rp)])
  task_path.write_text(json.dumps(expected))
 def test_stale_head_rejected_before_mutation(self):
  plan=copy.deepcopy(self.plan);plan["base"]["decision_head"]="0"*40;r=common.digest(common.reviewable(plan));plan["freshness"]["reviewable_plan_sha256"]=r;plan["ai_review_gate"]["reviewed_plan_sha256"]=r;plan["freshness"]["plan_sha256"]=common.plan_digest(plan);p=self.write("stale.json",plan)
  with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(p)])
  self.assertFalse((self.parent/"repo-worktrees/027-workspace").exists())
 def test_mutation_boundary_runs_once_and_changed_authority_writes_nothing(self):
  workspace=self.parent/"repo-worktrees/027-workspace";calls=[];path=self.write("authority-changed.json",self.plan);before=self.mutation_state(workspace)
  live={"number":27,"url":"https://github.com/example/repo/issues/27","state":"OPEN","title":"Changed","body":"","updatedAt":"2026-01-01T00:00:00Z"}
  with mock.patch.object(execute,"count_operation",side_effect=calls.append),mock.patch.object(execute,"github",return_value=live):
    result=execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(path)])
  self.assertEqual(["workspace.mutation_boundary_recheck"],calls);self.assertEqual(("no_side_effect","refresh_review",True),(result["variant"],result["typed_exit"],result["no_side_effect"]["zero_writes"]));self.assertEqual(before,self.mutation_state(workspace))
 def test_final_boundary_failure_rolls_back_only_new_workspace_objects(self):
  workspace=self.parent/"repo-worktrees/027-workspace";pp=self.write("boundary-failure.json",self.plan);before=self.mutation_state(workspace)
  with mock.patch.object(execute,"verify_created_boundary",side_effect=CommandError("stale_identity","created_workspace","boundary drift",3)):
   with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  self.assertEqual(before,self.mutation_state(workspace));self.assertFalse(workspace.exists())

 def test_current_mode_final_boundary_failure_restores_original_branch_and_removes_new_objects(self):
  self.configure(mode="current");plan=copy.deepcopy(self.plan);plan["naming"]["workspace_disposition"]="reuse_exact";plan["side_effects"]["operations"].remove("create_worktree");self.refresh(plan);pp=self.write("current-boundary-failure.json",plan);before=self.mutation_state(self.repo)
  with mock.patch.object(execute,"verify_created_boundary",side_effect=CommandError("stale_identity","created_workspace","boundary drift",3)):
   with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  self.assertEqual("main",self.git("branch","--show-current"));self.assertNotEqual(0,subprocess.run(["git","show-ref","--verify","--quiet","refs/heads/feat/027-workspace"],cwd=self.repo).returncode)
  self.assertEqual(before,self.mutation_state(self.repo));self.assertFalse((self.repo/plan["side_effects"]["task_artifacts"][0]).exists());self.assertFalse((self.repo/".trellis/.runtime/guru-team/tasks/027-workspace.json").exists())

 def test_existing_objects_are_not_removed_when_later_boundary_fails(self):
  result,_=self.execute_and_check();workspace=self.parent/"repo-worktrees/027-workspace";plan=copy.deepcopy(self.plan);plan["naming"].update({"branch_disposition":"reuse_exact","workspace_disposition":"reuse_exact","task_disposition":"reuse_exact"});self.refresh(plan);pp=self.write("reuse-boundary-failure.json",plan);before=self.mutation_state(workspace)
  with mock.patch.object(execute,"verify_created_boundary",side_effect=CommandError("stale_identity","created_workspace","boundary drift",3)):
   with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  self.assertEqual(before,self.mutation_state(workspace))
 def test_github_json_and_created_issue_url_decoders_are_strict(self):
  self.assertEqual({"number":112},execute.decode_github_json('{"number":112}\n'));self.assertEqual([],execute.decode_github_json("[]\n"))
  for raw in ('"text"','112','null','not-json','{"value":NaN}','[Infinity]'):
   with self.subTest(json=raw),self.assertRaises(CommandError) as raised:execute.decode_github_json(raw)
   self.assertEqual("invalid_json",raised.exception.code)
  expected="https://github.com/example/repo/issues/112"
  for raw in (expected,expected+"\n",expected+"\r\n"):
   self.assertEqual((expected,112),execute.decode_created_issue_url("example/repo",raw))
  for raw in (""," "+expected,"\t"+expected,expected+"\nextra",expected+"\n\n","http://github.com/example/repo/issues/112","https://github.com/other/repo/issues/112",expected+"?",expected+"?x=1",expected+"#",expected+"#fragment","https://github.com/example/repo/issues/0112"):
   with self.subTest(url=raw),self.assertRaises(CommandError):execute.decode_created_issue_url("example/repo",raw)
 def test_reviewed_draft_zero_match_creates_once_preserving_exact_bytes(self):
  title=" Reviewed issue ";body="Reviewed body\nsecond line\n";plan=self.draft_plan(title,body);pp=self.write("draft.json",plan);live=self.issue_row(title=title,body=body)
  with mock.patch.object(execute,"github",side_effect=[[],live]),mock.patch.object(execute,"run_gh",return_value=live["url"]+"\n") as created,mock.patch.object(check,"github",return_value=live):
   result=execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)]);self.assertEqual(("created_issue","refresh_review"),(result["variant"],result["typed_exit"]));rp=self.write("draft-result.json",result);checked=check.run(PACKAGE,{},["--root",str(self.repo),"--plan-input",str(pp),"--input",str(rp)])
  created.assert_called_once_with("example/repo","issue","create","--title",title,"--body",body,"--label","runtime");self.assertEqual("passed",checked["checker"]["status"]);self.assertFalse((self.parent/"repo-worktrees/027-workspace").exists())
 def test_reviewed_draft_one_match_recovers_without_create(self):
  plan=self.draft_plan();pp=self.write("recover.json",plan);live=self.issue_row()
  with mock.patch.object(execute,"github",side_effect=[[live],live]),mock.patch.object(execute,"run_gh") as created:
   result=execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  created.assert_not_called();self.assertEqual((112,live["url"],"refresh_review"),(result["created_issue"]["number"],result["created_issue"]["canonical_url"],result["typed_exit"]))
 def test_reviewed_draft_label_identity_uses_canonical_case_for_live_comparison(self):
  plan=self.draft_plan(labels=["BUG"]);pp=self.write("recover-label-case.json",plan);live=self.issue_row(labels=["bug"])
  with mock.patch.object(execute,"github",side_effect=[[live],live]),mock.patch.object(execute,"run_gh") as created:
   result=execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  created.assert_not_called();self.assertEqual(112,result["created_issue"]["number"])
  rp=self.write("recover-label-case-result.json",result)
  with mock.patch.object(check,"github",return_value=live):checked=check.run(PACKAGE,{},["--root",str(self.repo),"--plan-input",str(pp),"--input",str(rp)])
  self.assertEqual("passed",checked["checker"]["status"])
 def test_reviewed_draft_multiple_matches_block_before_create(self):
  plan=self.draft_plan();pp=self.write("ambiguous.json",plan);rows=[self.issue_row(112),self.issue_row(113)]
  with mock.patch.object(execute,"github",return_value=rows),mock.patch.object(execute,"run_gh") as created,self.assertRaises(CommandError) as raised:execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  created.assert_not_called();self.assertEqual(("stale_identity","target"),(raised.exception.code,raised.exception.field_path))
 def test_reviewed_draft_lookup_allows_999_rows_but_blocks_1000(self):
  plan=self.draft_plan();pp=self.write("lookup-limit.json",plan);live=self.issue_row()
  rows=[self.issue_row(number=1000+index,title="Other issue") for index in range(999)]
  with mock.patch.object(execute,"github",side_effect=[rows,live]),mock.patch.object(execute,"run_gh",return_value=live["url"]+"\n") as created:
   result=execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  self.assertEqual(112,result["created_issue"]["number"]);created.assert_called_once()
  with mock.patch.object(execute,"github",return_value=[live]*1000),mock.patch.object(execute,"run_gh") as created,self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
  created.assert_not_called()
 def test_reviewed_draft_lookup_exact_filter_rejects_mismatches(self):
  plan=self.draft_plan();base=self.issue_row();variants=[]
  for field,value in (("title","Other"),("body","Other"),("state","CLOSED"),("createdAt","2025-12-31T23:59:59Z")):
   row=copy.deepcopy(base);row[field]=value;variants.append((field,row))
  labels=copy.deepcopy(base);labels["labels"]=[{"name":"other"}];variants.append(("labels",labels))
  for name,row in variants:
   with self.subTest(name=name),mock.patch.object(execute,"github",return_value=[row]):self.assertEqual([],execute.find_reviewed_draft_issues(plan))
  malformed=copy.deepcopy(base);malformed.pop("updatedAt")
  with mock.patch.object(execute,"github",return_value=[malformed]),self.assertRaises(CommandError):execute.find_reviewed_draft_issues(plan)
  wrong_repo=copy.deepcopy(base);wrong_repo["url"]="https://github.com/other/repo/issues/112"
  with mock.patch.object(execute,"github",return_value=[wrong_repo]),self.assertRaises(CommandError):execute.find_reviewed_draft_issues(plan)
 def test_live_binding_and_checker_reject_identity_drift(self):
  plan=self.draft_plan();live=self.issue_row()
  with mock.patch.object(execute,"github",return_value=live):binding=execute.bind_reviewed_issue(plan,112)
  for name,change in (("number",{"number":113,"url":"https://github.com/example/repo/issues/113"}),("url",{"url":"https://github.com/other/repo/issues/112"}),("state",{"state":"CLOSED"}),("title",{"title":"Other"}),("body",{"body":"Other"}),("labels",{"labels":[{"name":"other"}]}),("updated",{"updatedAt":"not-a-time"})):
   drift=copy.deepcopy(live);drift.update(change)
   with self.subTest(name=name),mock.patch.object(execute,"github",return_value=drift),self.assertRaises(CommandError):execute.bind_reviewed_issue(plan,112)
  result={"schema_version":"2.0","skill_id":"guru-create-task-workspace","generated_at":"2026-01-01T00:00:01Z","mode":plan["mode"],"variant":"created_issue","plan_sha256":plan["freshness"]["plan_sha256"],"executor":common.stage("passed",["bound"]),"checker":common.stage("not_run",[]),"created_issue":binding,"created_workspace":None,"no_side_effect":None,"typed_exit":"refresh_review","reason":"bound","consumer":common.CONSUMERS["refresh_review"],"facts_sha256":""};result=common.finalize(PACKAGE,result);pp=self.write("drift-plan.json",plan);rp=self.write("drift-result.json",result);drift=copy.deepcopy(live);drift["labels"]=[{"name":"other"}]
  with mock.patch.object(check,"github",return_value=drift),self.assertRaises(CommandError):check.run(PACKAGE,{},["--root",str(self.repo),"--plan-input",str(pp),"--input",str(rp)])
 def test_stateful_fake_gh_recovers_partial_success_without_second_create(self):
  plan=self.draft_plan(labels=["BUG"]);pp=self.write("stateful-plan.json",plan);state_path=self.write("gh-state.json",{"create_count":0,"issue":None,"fail_next_view":True});fake_bin=self.parent/"fake-bin";fake_bin.mkdir();fake_gh=fake_bin/"gh"
  fake_gh.write_text(f'''#!{sys.executable}
import json,sys
from pathlib import Path
state_path=Path({str(state_path)!r})
state=json.loads(state_path.read_text())
args=sys.argv[1:]
expected_list=['issue','list','--state','open','--search','created:>=2026-01-01','--limit','1000','--json','number,url,state,title,body,createdAt,updatedAt,labels','--repo','example/repo']
if args==expected_list:
 print(json.dumps([] if state['issue'] is None else [state['issue']]));raise SystemExit(0)
if args[:2]==['issue','create']:
 title=args[args.index('--title')+1];body=args[args.index('--body')+1]
 labels=[args[index+1] for index,value in enumerate(args[:-1]) if value=='--label']
 state['create_count']+=1
 state['issue']={{'number':112,'url':'https://github.com/example/repo/issues/112','state':'OPEN','title':title,'body':body,'createdAt':'2026-01-01T00:00:01Z','updatedAt':'2026-01-01T00:00:01Z','labels':[{{'name':label.lower()}} for label in labels]}}
 state_path.write_text(json.dumps(state));print(state['issue']['url']);raise SystemExit(0)
if args[:2]==['issue','view'] and state['issue'] is not None:
 if state['fail_next_view']:
  state['fail_next_view']=False;state_path.write_text(json.dumps(state));print('injected view failure',file=sys.stderr);raise SystemExit(1)
 print(json.dumps(state['issue']));raise SystemExit(0)
print('unsupported fake gh command: '+' '.join(args),file=sys.stderr);raise SystemExit(9)
''');fake_gh.chmod(0o755);path=f"{fake_bin}{os.pathsep}{os.environ.get('PATH','')}"
  with mock.patch.dict(os.environ,{"PATH":path}):
   with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)])
   result=execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)]);rp=self.write("stateful-result.json",result);checked=check.run(PACKAGE,{},["--root",str(self.repo),"--plan-input",str(pp),"--input",str(rp)])
  state=json.loads(state_path.read_text());self.assertEqual((1,[{"name":"bug"}]),(state["create_count"],state["issue"]["labels"]));self.assertEqual((112,state["issue"]["url"],"refresh_review","passed"),(result["created_issue"]["number"],result["created_issue"]["canonical_url"],result["typed_exit"],checked["checker"]["status"]));self.assertFalse((self.parent/"repo-worktrees/027-workspace").exists());self.assertEqual("main",self.git("branch","--show-current"))
 def test_runtime_has_no_placeholder_or_monolith(self):
  for p in LOCAL.glob("*.py"):
   t=p.read_text();self.assertNotIn("mutation is unavailable",t);self.assertNotIn("guru_team_trellis.py",t);self.assertNotIn("typed_output(package_root",t)
if __name__=="__main__":unittest.main()
