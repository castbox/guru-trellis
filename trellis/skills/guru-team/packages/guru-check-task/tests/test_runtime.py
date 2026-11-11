from __future__ import annotations
import copy, hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from jsonschema import Draft202012Validator

PACKAGE=Path(__file__).resolve().parents[1]
SKILLS=PACKAGE.parents[1]
KERNEL_ROOT=SKILLS if (SKILLS/"runtime/command.py").is_file() else SKILLS.parent
if str(KERNEL_ROOT) not in sys.path: sys.path.insert(0,str(KERNEL_ROOT))
if str(PACKAGE/"runtime") not in sys.path: sys.path.insert(0,str(PACKAGE/"runtime"))
from runtime.command import main
from common import PHASE2_WORKTREE_CONTENT_ALGORITHM, content_identity, dirty_paths, validate_candidate_classifications
from runtime.io import CommandError

class PackageLocalRuntimeTest(unittest.TestCase):
 def test_empty_candidates_preserve_array_uniqueness_and_reference_checks(self):
  value=json.loads((PACKAGE/"examples/phase2-check.json").read_text())
  self.assertEqual([],value["candidate_classifications"])
  validate_candidate_classifications(value)
  for rows in (None,{},"",False):
   invalid=copy.deepcopy(value);invalid["candidate_classifications"]=rows
   with self.subTest(rows=rows),self.assertRaises(CommandError):validate_candidate_classifications(invalid)
  for key in ("scope_decisions","findings"):
   invalid=copy.deepcopy(value);invalid["semantic_review"][key]=[{"candidate_ref":"candidate:phase2:boundary"}]
   with self.subTest(link=key),self.assertRaises(CommandError):validate_candidate_classifications(invalid)
  rejected={"candidate_ref":"candidate:phase2:boundary","decision":"rejected_not_reproduced"}
  value["candidate_classifications"]=[rejected]
  validate_candidate_classifications(value)
  value["candidate_classifications"].append(copy.deepcopy(rejected))
  with self.assertRaises(CommandError):validate_candidate_classifications(value)

 def git(self,repo,*args,input=None):
  return subprocess.run(["git",*args],cwd=repo,input=input,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout.strip()

 def gitlink_fixture(self,temporary):
  source=Path(temporary)/"source";repo=Path(temporary)/"repo"
  source.mkdir();self.git(source,"init","-q");self.git(source,"config","user.name","Test");self.git(source,"config","user.email","test@example.com")
  (source/"tracked.txt").write_text("one\n");self.git(source,"add","tracked.txt");self.git(source,"commit","-qm","initial")
  oid=self.git(source,"rev-parse","HEAD")
  repo.mkdir();self.git(repo,"init","-q");self.git(repo,"config","user.name","Test");self.git(repo,"config","user.email","test@example.com")
  self.git(repo,"-c","protocol.file.allow=always","submodule","add","-q",str(source),"module");self.git(repo,"commit","-qam","gitlink")
  return repo,oid

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
   entries=[{"path":"tracked.txt","kind":"file","content_sha256":hashlib.sha256(content).hexdigest(),"mode":"100644"}]
   expected=hashlib.sha256(json.dumps({"algorithm":PHASE2_WORKTREE_CONTENT_ALGORITHM,"entries":entries},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
   retired=hashlib.sha256(json.dumps({"algorithm":"guru-reviewed-content-1.0","entries":entries},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
   self.assertEqual("guru-phase2-worktree-content-3.0",PHASE2_WORKTREE_CONTENT_ALGORITHM)
   self.assertEqual(expected,content_identity(repo))
   self.assertNotEqual(retired,content_identity(repo))

 def test_content_identity_preserves_non_gitlink_payloads(self):
  with tempfile.TemporaryDirectory() as temporary:
   repo=Path(temporary);self.git(repo,"init","-q")
   content=b"tracked\n";(repo/"file.txt").write_bytes(content);os.symlink("file.txt",repo/"link")
   entries=[{"path":"file.txt","kind":"file","content_sha256":hashlib.sha256(content).hexdigest(),"mode":"100644"},{"path":"link","kind":"symlink","target":"file.txt"},{"path":"missing","kind":"missing"}]
   expected=hashlib.sha256(json.dumps({"algorithm":PHASE2_WORKTREE_CONTENT_ALGORITHM,"entries":entries},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
   self.assertEqual(expected,content_identity(repo,["file.txt","link","missing"]))

 def test_content_identity_binds_initialized_and_uninitialized_gitlink_to_index_oid(self):
  with tempfile.TemporaryDirectory() as temporary:
   repo,oid=self.gitlink_fixture(temporary)
   expected=digest=hashlib.sha256(json.dumps({"algorithm":PHASE2_WORKTREE_CONTENT_ALGORITHM,"entries":[{"path":"module","kind":"gitlink","mode":"160000","oid":oid}]},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
   self.assertEqual(expected,content_identity(repo,["module"]))
   self.git(repo,"submodule","deinit","-f","--","module")
   self.assertEqual(digest,content_identity(repo,["module"]))

 def test_content_identity_ignores_gitlink_worktree_state(self):
  cases=("dirty","head_drift","deletion","replacement","root_mismatch")
  for case in cases:
   with self.subTest(case=case),tempfile.TemporaryDirectory() as temporary:
    repo,_=self.gitlink_fixture(temporary);module=repo/"module";before=content_identity(repo,["module"])
    if case=="dirty":(module/"tracked.txt").write_text("dirty\n")
    elif case=="head_drift":
     self.git(module,"config","user.name","Test");self.git(module,"config","user.email","test@example.com")
     (module/"next.txt").write_text("next\n");self.git(module,"add","next.txt");self.git(module,"commit","-qm","next")
    else:
     shutil.rmtree(module)
     if case=="replacement":module.write_text("replacement\n")
     elif case=="root_mismatch":module.mkdir();(module/"ordinary.txt").write_text("not a submodule\n")
    self.assertEqual(before,content_identity(repo,["module"]))

 def test_content_identity_binds_parent_pointer_and_rejects_unmerged_index(self):
  for case in ("pointer_drift","index_deletion","staged_replacement","ambiguous_index"):
   with self.subTest(case=case),tempfile.TemporaryDirectory() as temporary:
    repo,oid=self.gitlink_fixture(temporary);before=content_identity(repo,["module"])
    alternate="1"*40
    if case=="pointer_drift":self.git(repo,"update-index","--cacheinfo",f"160000,{alternate},module")
    elif case=="index_deletion":self.git(repo,"update-index","--force-remove","module")
    elif case=="staged_replacement":
     shutil.rmtree(repo/"module");(repo/"module").write_text("replacement\n");self.git(repo,"add","module")
    else:
     records=f"0 {oid}\tmodule\n160000 {oid} 1\tmodule\n160000 {alternate} 2\tmodule\n"
     self.git(repo,"update-index","--index-info",input=records)
    if case=="ambiguous_index":
     with self.assertRaises(CommandError) as raised:content_identity(repo,["module"])
     self.assertEqual("stale_identity",raised.exception.code)
    else:self.assertNotEqual(before,content_identity(repo,["module"]))






if __name__=="__main__": unittest.main()
