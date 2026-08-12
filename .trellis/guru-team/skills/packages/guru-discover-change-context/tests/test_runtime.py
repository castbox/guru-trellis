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
from common import check_recovery,consume_recovery,preview,record_recovery

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

 def test_recovery_checkpoint_is_package_owned_and_short_lived(self):
  with tempfile.TemporaryDirectory() as name:
   repo=Path(name);subprocess.run(["git","init","-q","-b","feat/context",str(repo)],check=True);td=repo/".trellis/tasks/08-12-context";td.mkdir(parents=True);task={"id":"08-12-context","status":"in_progress","branch":"feat/context"};(td/"task.json").write_text(json.dumps(task));payload=json.loads((PACKAGE/"examples/change-context-owner-result.json").read_text());payload["mode"]="workflow";path=record_recovery(PACKAGE,repo,td,task,payload,"resume-context");self.assertTrue(path.is_file());self.assertEqual(path,check_recovery(PACKAGE,repo,td,task,payload,"resume-context"));consume_recovery(path);self.assertFalse(path.exists());self.assertFalse(path.parent.exists())

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
