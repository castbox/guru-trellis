from __future__ import annotations
import copy,json,subprocess,sys,tempfile,unittest
from pathlib import Path
PACKAGE=Path(__file__).resolve().parents[1];SKILLS=PACKAGE.parents[1];LOCAL=PACKAGE/"runtime"
for p in (SKILLS,LOCAL):
 if str(p) not in sys.path:sys.path.insert(0,str(p))
from runtime.io import CommandError
import check,invoke,record
class BranchReviewTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.parent=Path(self.tmp.name);self.repo=self.parent/"repo";self.inputs=self.parent/"inputs";self.inputs.mkdir();subprocess.run(["git","init","-q","-b","main",str(self.repo)],check=True);self.git("config","user.name","Test");self.git("config","user.email","test@example.invalid");(self.repo/"app.txt").write_text("base\n");self.git("add",".");self.git("commit","-qm","base");self.base=self.git("rev-parse","HEAD");self.git("switch","-qc","feat/test");(self.repo/"app.txt").write_text("feature\n");(self.repo/".trellis/tasks/08-12-test").mkdir(parents=True);self.git("add",".");self.git("commit","-qm","feature");self.head=self.git("rev-parse","HEAD")
 def tearDown(self):self.tmp.cleanup()
 def git(self,*a):return subprocess.run(["git",*a],cwd=self.repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip()
 def write(self,n,v):p=self.inputs/n;p.write_text(json.dumps(v));return p
 def public(self,intent="fresh_final_review"):return {"profile":"branch_review","mode":"workflow","task_ref":".trellis/tasks/08-12-test","base_ref":self.base,"branch_review_commit":self.git("rev-parse","HEAD"),"review_intent":intent}
 def auth(self,exit_id="passed"):
  return {"semantic_review":{"qualified_findings":[],"scope_proposals":[],"observations":[],"followup_candidates":[],"rejected_candidates":[],"ai_review_gate":{"status":exit_id,"summary":"Reviewed the complete current base to HEAD range."}},"verification_evidence":{"reviewer":"independent-agent-2","review_source":"independent-agent","evidence":["Reviewed complete diff and tests."]}}
 def test_pass_record_check_invoke_and_content_drift(self):
  pi=self.write("public.json",self.public());ai=self.write("auth.json",self.auth());gate=record.run(PACKAGE,{},["--root",str(self.repo),"--skill-input",str(pi),"--semantic-review-file",str(ai),"--typed-exit","passed"]);gp=self.write("gate.json",gate);self.assertEqual("passed",check.run(PACKAGE,{},["--root",str(self.repo),"--input",str(gp),"--expected-exit","passed"])["typed_exit"]);env=self.write("invoke.json",{"owner_result":gate});self.assertEqual(self.head,invoke.run(PACKAGE,{},["--root",str(self.repo),"--invocation",str(env)])["branch_review_commit"]);(self.repo/"app.txt").write_text("later\n");self.git("add","app.txt");self.git("commit","-qm","later")
  with self.assertRaises(CommandError):check.run(PACKAGE,{},["--root",str(self.repo),"--input",str(gp)])
 def test_open_finding_projects_exact_reference(self):
  auth=self.auth("implementation_required");common={"candidate_ref":"candidate-1","disposition":"qualified_finding","scenario_class":"normal_required_behavior","affected_behavior":"Required behavior is missing.","path":"app.txt","evidence_refs":["diff:app.txt"],"requirement_refs":["PRD R1"],"scope_basis":"Current task scope.","qualification_reason":"Reproduces normally.","finding_ref":"finding-1","severity":"P1","introduced_head":self.head,"fix_head":None,"closure_head":None,"status":"open","closure_evidence":[]};auth["semantic_review"]["qualified_findings"]=[common];pi=self.write("public.json",self.public("initial_review"));ai=self.write("auth.json",auth);gate=record.run(PACKAGE,{},["--root",str(self.repo),"--skill-input",str(pi),"--semantic-review-file",str(ai),"--typed-exit","implementation_required"]);env=self.write("invoke.json",{"owner_result":gate});self.assertEqual(["finding-1"],invoke.run(PACKAGE,{},["--root",str(self.repo),"--invocation",str(env)])["finding_refs"])
 def test_base_continuity_preserves_task_review_and_projects_pair(self):
  self.git("switch","main");(self.repo/"base.txt").write_text("advance\n");self.git("add","base.txt");self.git("commit","-qm","advance base");new_base=self.git("rev-parse","HEAD");self.git("switch","feat/test")
  public={"profile":"base_continuity","mode":"workflow","task_ref":".trellis/tasks/08-12-test","task_head":self.head,"branch_review_commit":self.head,"old_base_head":self.base,"new_base_head":new_base,"candidate_tree_sha256":"d"*64,"relevant_paths":["base.txt"],"resume_target":"publication_review","review_intent":"base_continuity"}
  auth=self.auth("continuity_passed");pi=self.write("continuity.json",public);ai=self.write("continuity-auth.json",auth);gate=record.run(PACKAGE,{},["--root",str(self.repo),"--skill-input",str(pi),"--semantic-review-file",str(ai),"--typed-exit","continuity_passed"]);env=self.write("continuity-invoke.json",{"owner_result":gate});out=invoke.run(PACKAGE,{},["--root",str(self.repo),"--invocation",str(env)])
  self.assertEqual("continuity_passed",out["exit_id"]);self.assertEqual(self.head,out["branch_review_commit"]);self.assertEqual(new_base,out["new_base_head"]);self.assertNotIn("relevant_paths",out)
 def test_dirty_overlay_and_non_ancestor_base_are_rejected(self):
  (self.repo/"overlay.txt").write_text("unreviewed\n");pi=self.write("public.json",self.public());ai=self.write("auth.json",self.auth())
  with self.assertRaises(CommandError):record.run(PACKAGE,{},["--root",str(self.repo),"--skill-input",str(pi),"--semantic-review-file",str(ai),"--typed-exit","passed"])
  (self.repo/"overlay.txt").unlink();public=self.public();public["base_ref"]="f"*40;pi=self.write("bad-base.json",public)
  with self.assertRaises(CommandError):record.run(PACKAGE,{},["--root",str(self.repo),"--skill-input",str(pi),"--semantic-review-file",str(ai),"--typed-exit","passed"])
 def test_runtime_has_no_example_projection_or_monolith(self):
  for p in LOCAL.glob("*.py"):
   t=p.read_text();self.assertNotIn("guru_team_trellis.py",t);self.assertNotIn("typed_output(package_root",t)
if __name__=="__main__":unittest.main()
