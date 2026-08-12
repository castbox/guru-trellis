from __future__ import annotations
import copy,json,subprocess,sys,tempfile,unittest
from unittest import mock
from datetime import datetime,timezone
from pathlib import Path
PACKAGE=Path(__file__).resolve().parents[1];SKILLS=PACKAGE.parents[1];LOCAL=PACKAGE/"runtime"
for p in (SKILLS,LOCAL):
 if str(p) not in sys.path:sys.path.insert(0,str(p))
from runtime.io import CommandError
import check,common,execute,invoke,record
class WorkspaceTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.parent=Path(self.tmp.name);self.repo=self.parent/"repo";subprocess.run(["git","init","-q","-b","main",str(self.repo)],check=True);self.git("config","user.name","Test");self.git("config","user.email","test@example.invalid");(self.repo/"seed").write_text("seed\n");self.git("add","seed");self.git("commit","-qm","seed");self.head=self.git("rev-parse","HEAD");self.plan=self.make_plan()
 def tearDown(self):self.tmp.cleanup()
 def git(self,*a):return subprocess.run(["git",*a],cwd=self.repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip()
 def write(self,n,v):p=self.repo/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v));return p
 def make_plan(self):
  task="08-12-027-workspace";plan=json.loads((PACKAGE/"examples/task-workspace-plan.json").read_text());plan["mode"]="standalone";plan["target"].update({"repo":"example/repo","issue_number":27,"url":"https://github.com/example/repo/issues/27"});plan["base"].update({"base_ref":"HEAD","decision_head":self.head,"local_head":self.head,"remote_head":self.head});plan["naming"].update({"branch_name":"feat/027-workspace","workspace_slug":"027-workspace","task_slug":"027-workspace","task_title":"#27 Workspace"});plan["side_effects"]["task_artifacts"]=[f".trellis/tasks/{task}/issue-scope-ledger.json"];plan["side_effects"]["runtime_mappings"]=[".trellis/.runtime/guru-team/workspaces/027-workspace.json",".trellis/.runtime/guru-team/tasks/027-workspace.json"]
  plan["scope"]["primary"].update({"number":27,"url":"https://github.com/example/repo/issues/27"});plan["scope"]["close"]=[copy.deepcopy(plan["scope"]["primary"])];plan["scope"]["scope_sha256"]=common.digest({k:v for k,v in plan["scope"].items() if k!="scope_sha256"});r=common.digest(common.reviewable(plan));plan["freshness"]["reviewable_plan_sha256"]=r;plan["ai_review_gate"]["reviewed_plan_sha256"]=r;plan["freshness"]["plan_sha256"]=common.plan_digest(plan);return plan
 def test_real_workspace_mutation_check_and_invoke(self):
  pp=self.write("plan.json",self.plan);self.assertEqual(self.plan,record.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)]));result=execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)]);self.assertEqual("created",result["typed_exit"]);rp=self.write("result.json",result);checked=check.run(PACKAGE,{},["--root",str(self.repo),"--plan-input",str(pp),"--input",str(rp)]);env=self.write("invoke.json",{"result":checked});self.assertEqual({"exit_id":"created"},invoke.run(PACKAGE,{},["--root",str(self.repo),"--invocation",str(env)]))
 def test_stale_head_rejected_before_mutation(self):
  plan=copy.deepcopy(self.plan);plan["base"]["decision_head"]="0"*40;r=common.digest(common.reviewable(plan));plan["freshness"]["reviewable_plan_sha256"]=r;plan["ai_review_gate"]["reviewed_plan_sha256"]=r;plan["freshness"]["plan_sha256"]=common.plan_digest(plan);p=self.write("stale.json",plan)
  with self.assertRaises(CommandError):execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(p)])
  self.assertFalse((self.parent/"027-workspace").exists())
 def test_reviewed_draft_creates_and_rereads_issue_before_refresh(self):
  plan=copy.deepcopy(self.plan);title="Reviewed issue";body="Reviewed body";reviewed=common.digest({"title":title,"body":body,"labels":["runtime"]})
  plan["invocation"].update({"target_kind":"reviewed_draft","action_scope":"github_issue_mutation"});plan["target"].update({"kind":"reviewed_draft","issue_number":None,"url":None,"state":None,"updated_at":None,"title_sha256":__import__('hashlib').sha256(title.encode()).hexdigest(),"body_sha256":__import__('hashlib').sha256(body.encode()).hexdigest(),"draft":{"draft_id":"draft-112","source_request_sha256":"1"*64,"title":title,"body":body,"labels":["runtime"],"reviewed_draft_sha256":reviewed}});plan["scope"].update({"primary":None,"close":[],"scope_sha256":common.digest({"primary":None,"close":[],"related":[],"followup":[]})});plan["side_effects"].update({"operations":["create_issue"],"task_artifacts":[],"runtime_mappings":[],"command_argv":["create-task-workspace","--input","draft.json"],"stop_after":"created_issue_refresh"});r=common.digest(common.reviewable(plan));plan["freshness"]["reviewable_plan_sha256"]=r;plan["ai_review_gate"]["reviewed_plan_sha256"]=r;plan["freshness"]["plan_sha256"]=common.plan_digest(plan);pp=self.write("draft.json",plan)
  live={"number":112,"url":"https://github.com/example/repo/issues/112","state":"OPEN","title":title,"body":body,"updatedAt":"2026-08-12T00:00:00Z","labels":[{"name":"runtime"}]}
  with mock.patch.object(execute,"github",side_effect=[{"url":live["url"]},live]),mock.patch.object(check,"github",return_value=live):
   result=execute.run(PACKAGE,{},["--root",str(self.repo),"--input",str(pp)]);self.assertEqual(("created_issue","refresh_review"),(result["variant"],result["typed_exit"]));rp=self.write("draft-result.json",result);checked=check.run(PACKAGE,{},["--root",str(self.repo),"--plan-input",str(pp),"--input",str(rp)])
  self.assertEqual("passed",checked["checker"]["status"]);self.assertFalse((self.parent/"027-workspace").exists())
 def test_runtime_has_no_placeholder_or_monolith(self):
  for p in LOCAL.glob("*.py"):
   t=p.read_text();self.assertNotIn("mutation is unavailable",t);self.assertNotIn("guru_team_trellis.py",t);self.assertNotIn("typed_output(package_root",t)
if __name__=="__main__":unittest.main()
