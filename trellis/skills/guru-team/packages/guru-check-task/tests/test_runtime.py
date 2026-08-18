from __future__ import annotations
import copy, hashlib, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
from jsonschema import Draft202012Validator

PACKAGE=Path(__file__).resolve().parents[1]
SKILLS=PACKAGE.parents[1]
RUNTIME=SKILLS/"runtime"
if str(SKILLS) not in sys.path: sys.path.insert(0,str(SKILLS))
if str(PACKAGE/"runtime") not in sys.path: sys.path.insert(0,str(PACKAGE/"runtime"))
from runtime.command import main
from common import PHASE2_WORKTREE_CONTENT_ALGORITHM, content_identity, dirty_paths

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

 def test_dirty_paths_expands_untracked_directories(self):
  with tempfile.TemporaryDirectory() as temporary:
   repo=Path(temporary)
   subprocess.run(["git","init","-q"],cwd=repo,check=True)
   path=repo/"nested/untracked.txt"
   path.parent.mkdir()
   path.write_text("current\n")
   self.assertEqual(["nested/untracked.txt"],dirty_paths(repo))

 def test_content_identity_covers_deletions_and_untracked_bytes(self):
  with tempfile.TemporaryDirectory() as temporary:
   repo=Path(temporary)
   subprocess.run(["git","init","-q"],cwd=repo,check=True)
   tracked=repo/"tracked.txt";tracked.write_text("tracked\n")
   subprocess.run(["git","add","tracked.txt"],cwd=repo,check=True)
   initial=content_identity(repo)
   tracked.unlink()
   deleted=content_identity(repo)
   self.assertNotEqual(initial,deleted)
   untracked=repo/"untracked.txt";untracked.write_text("one\n")
   first_untracked=content_identity(repo)
   untracked.write_text("two\n")
   self.assertNotEqual(first_untracked,content_identity(repo))

 def test_content_identity_excludes_private_runtime(self):
  with tempfile.TemporaryDirectory() as temporary:
   repo=Path(temporary)
   subprocess.run(["git","init","-q"],cwd=repo,check=True)
   tracked=repo/"tracked.txt";tracked.write_text("tracked\n")
   subprocess.run(["git","add","tracked.txt"],cwd=repo,check=True)
   private=repo/".trellis/.runtime/checkpoint.json"
   private.parent.mkdir(parents=True);private.write_text("one\n")
   before=content_identity(repo)
   private.write_text("two\n")
   self.assertEqual(before,content_identity(repo))

 def test_content_identity_uses_distinct_phase2_worktree_algorithm(self):
  with tempfile.TemporaryDirectory() as temporary:
   repo=Path(temporary)
   subprocess.run(["git","init","-q"],cwd=repo,check=True)
   content=b"tracked\n"
   (repo/"tracked.txt").write_bytes(content)
   subprocess.run(["git","add","tracked.txt"],cwd=repo,check=True)
   entries=[{"path":"tracked.txt","kind":"file","content_sha256":hashlib.sha256(content).hexdigest()}]
   expected=hashlib.sha256(json.dumps({"algorithm":PHASE2_WORKTREE_CONTENT_ALGORITHM,"entries":entries},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
   retired=hashlib.sha256(json.dumps({"algorithm":"guru-reviewed-content-1.0","entries":entries},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
   self.assertEqual("guru-phase2-worktree-content-1.0",PHASE2_WORKTREE_CONTENT_ALGORITHM)
   self.assertEqual(expected,content_identity(repo))
   self.assertNotEqual(retired,content_identity(repo))

 def test_public_wrapper_retains_only_passed_checkpoint_and_projects_all_exits(self):
  example=json.loads((PACKAGE/"examples/phase2-check.json").read_text())
  with tempfile.TemporaryDirectory() as temporary:
   repo=Path(temporary)
   subprocess.run(["git","init","-q"],cwd=repo,check=True)
   task_dir=repo/".trellis/tasks/test-task";task_dir.mkdir(parents=True)
   checkpoint_path=repo/".trellis/.runtime/guru-team/owner-checkpoints/test-task/phase2-check.json"
   checkpoint_path.parent.mkdir(parents=True)
   public={"profile":"initial_check","mode":"workflow","task_ref":".trellis/tasks/test-task","source_exit":"implementation_complete"}

   def owner(exit_id):
    value=copy.deepcopy(example);value["task_ref"]=public["task_ref"]
    if exit_id=="implementation_required":
     value["typed_exit"]=exit_id;value["consumer"]={"kind":"workflow","id":"guru-resume-implementation"};value["semantic_review"]["status"]=exit_id;value["semantic_review"]["adequacy_dimensions"][2]["status"]="failed"
     value["candidate_classifications"]=[{"candidate_ref":"candidate:phase2:defect","decision":"qualified_current","witness":{"requirement_refs":["prd:R1"],"supported_entry_refs":["entry:phase2"],"existing_caller_refs":["caller:guru-check-task"],"honest_action_sequence":["run the supported Phase 2 check"],"defect_observation":"The required behavior fails.","excluded_assumptions":[]},"consumer_use":"task_commit_preflight"}]
     value["semantic_review"]["scope_decisions"]=[{"id":"C1","candidate_ref":"candidate:phase2:defect","disposition":"current_scope","summary":"A defect remains.","finding_id":"F1"}]
     value["semantic_review"]["findings"]=[{"id":"F1","candidate_ref":"candidate:phase2:defect","severity":"P2","summary":"Open defect.","path":"src/example.py","status":"open"}]
    elif exit_id=="planning_stale":
     value["typed_exit"]=exit_id;value["route"]="reapprove_plan";value["consumer"]={"kind":"workflow","id":"guru-task-check-planning-router"};value["semantic_review"]["status"]=exit_id
     value["candidate_classifications"]=[{"candidate_ref":"candidate:phase2:scope","decision":"qualified_approved_expansion","witness":{"requirement_refs":[],"supported_entry_refs":["entry:phase2"],"existing_caller_refs":["caller:guru-check-task"],"honest_action_sequence":["review the requested scope"],"defect_observation":"The request changes scope.","excluded_assumptions":[]},"consumer_use":"task_commit_preflight"}]
     value["semantic_review"]["scope_decisions"]=[{"id":"scope-proposal:R13","candidate_ref":"candidate:phase2:scope","disposition":"scope_change_required","summary":"Current scope changed.","finding_id":None}]
    elif exit_id=="blocked":
     value["typed_exit"]=exit_id;value["consumer"]={"kind":"stop","id":"task-check-blocked"};value["semantic_review"]["status"]=exit_id;value["semantic_review"]["adequacy_dimensions"][-1]["status"]="blocked";value["validation"]["unverified_items"]=[{"id":"U1","summary":"Required evidence is unavailable.","blocking":True}]
    return value

   expected={
    "passed":{"exit_id":"passed","task_ref":public["task_ref"],"phase2_commit_anchor":example["phase2_capture_commit"]},
    "implementation_required":{"exit_id":"implementation_required","task_ref":public["task_ref"],"finding_refs":["F1"]},
    "planning_stale":{"exit_id":"planning_stale","task_ref":public["task_ref"],"planning_route":"reapprove_plan","proposal_refs":["scope-proposal:R13"]},
    "blocked":{"exit_id":"blocked"},
   }
   for exit_id in expected:
    with self.subTest(exit_id=exit_id):
     checkpoint_path.write_text("checkpoint\n")
     envelope=json.dumps({"public_input":public,"owner_result":owner(exit_id)},separators=(",",":"))
     environment={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"}
     result=subprocess.run([str(PACKAGE/"scripts/invoke.sh"),"--root",str(repo),"--invocation","-"],input=envelope,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,env=environment)
     self.assertEqual(0,result.returncode,result.stderr)
     self.assertEqual(expected[exit_id],json.loads(result.stdout))
     self.assertEqual(exit_id=="passed",checkpoint_path.exists())

if __name__=="__main__": unittest.main()
