from __future__ import annotations
import json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
from jsonschema import Draft202012Validator

PACKAGE=Path(__file__).resolve().parents[1]
SKILLS=PACKAGE.parents[1]
RUNTIME=SKILLS/"runtime"
if str(SKILLS) not in sys.path: sys.path.insert(0,str(SKILLS))
if str(PACKAGE/"runtime") not in sys.path: sys.path.insert(0,str(PACKAGE/"runtime"))
from runtime.command import main
from common import content_identity, dirty_paths

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

if __name__=="__main__": unittest.main()
