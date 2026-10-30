from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
PACKAGE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE.parents[1]))
from runtime.io import CommandError
spec=importlib.util.spec_from_file_location('legacy_original_owner',PACKAGE/'runtime/legacy_maintenance.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class LegacyOwnerTests(unittest.TestCase):
 def test_stdin_profile_text_is_not_reinterpreted_as_a_file(self):
  import io
  from contextlib import chdir
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as directory, chdir(directory):
   Path('1').write_text(json.dumps({'profile':'legacy_history_verification'}),encoding='utf-8')
   with patch.dict(sys.modules), patch.object(sys,'path',[str(PACKAGE/'runtime'),*sys.path]):
    sys.modules.pop('owner',None)
    invoke_spec=importlib.util.spec_from_file_location('merge_input_profile',PACKAGE/'runtime/invoke.py')
    invoke=importlib.util.module_from_spec(invoke_spec);invoke_spec.loader.exec_module(invoke)
    with patch('sys.stdin',io.StringIO('1')), self.assertRaises(CommandError) as caught:
     invoke.run(PACKAGE,{},['--input','-'])
   self.assertEqual((caught.exception.code,caught.exception.field_path),('invalid_json','input'))
   self.assertIn('top level must be an object',caught.exception.remediation)
 def test_explicit_retirement_reads_preserved_archive_after_active_tree_removed(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);key={'task_id':'selected','lifecycle_generation':0};ref='.trellis/tasks/selected'
   active=root/ref;active.mkdir(parents=True);(active/'task.json').write_text(json.dumps({'id':'selected','lifecycle_generation':0}))
   prefix=module.CONTROL_ROOT;control=prefix+'selected.json';file=root/control;file.parent.mkdir(parents=True);file.write_text(json.dumps({'public_input':{**key,'task_ref':ref}}))
   inspection=module.execute(PACKAGE,{'profile':'legacy_control_inspection','root':str(root),'key':key,'task_ref':ref,'control_refs':[control]})
   archive='.trellis/tasks/archive/2026-10/selected';arch=root/archive;arch.mkdir(parents=True);(arch/'task.json').write_text(json.dumps({'id':'selected','completedAt':'2025-01-01'}))
   state={'public_input':{'target_checkout':str(root),'key':key,'task_ref':ref},'public_plan':{'kind':'legacy_closeout','guard':{'archive_ref':archive}},'controls':{PACKAGE.name:inspection['controls']}}
   checkpoint=Path(module.freeze_controls(root,key,ref,inspection['controls'],module.raw(arch/'task.json'),'operation'))
   public={'profile':'legacy_control_retirement','root':str(root),'key':key,'task_ref':ref,'preserved_source_ref':archive+'/task.json','control_refs':[control],'recovery_ref':str(checkpoint)}
   result=module.execute(PACKAGE,public)
   self.assertEqual(result,{'exit_id':'legacy_controls_retired','owner_id':PACKAGE.name,'key':key});self.assertFalse(file.exists());self.assertEqual(json.loads((arch/'task.json').read_text())['completedAt'],'2025-01-01')
   self.assertEqual(module.execute(PACKAGE,public),result)
 def test_other_generation_not_retired(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);active=root/'.trellis/tasks/selected';active.mkdir(parents=True);(active/'task.json').write_text(json.dumps({'id':'selected','lifecycle_generation':0}))
   prefix=module.CONTROL_ROOT;control=prefix+'later.json';file=root/control;file.parent.mkdir(parents=True);file.write_text(json.dumps({'task_id':'selected','lifecycle_generation':1}))
   with self.assertRaises(CommandError):module.execute(PACKAGE,{'profile':'legacy_control_inspection','root':str(root),'key':{'task_id':'selected','lifecycle_generation':0},'task_ref':'.trellis/tasks/selected','control_refs':[control]})
   self.assertTrue(file.exists())
 def test_tag2_original_task_ref_attribution_without_generation(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);key={'task_id':'selected','lifecycle_generation':0};task_ref='.trellis/tasks/selected';task=root/task_ref;task.mkdir(parents=True);(task/'task.json').write_text(json.dumps({'id':'selected','status':'in_progress'}))
   ref=module.CONTROL_ROOT+'original.json';path=root/ref;path.parent.mkdir(parents=True);path.write_text(json.dumps({'public_input':{'task_ref':task_ref}}))
   result=module.execute(PACKAGE,{'profile':'legacy_control_inspection','root':str(root),'key':key,'task_ref':task_ref,'control_refs':[ref]})
   self.assertEqual(result['controls'][0]['path'],ref)
 def test_public_history_profile_needs_no_current_lifecycle_and_does_not_mutate(self):
  from unittest import mock
  import subprocess
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);fact={'repo_ref':'example/repo','pr_number':1,'reviewed_head':'a'*40,'target_branch':'main','head_branch':'old-task'}
   if PACKAGE.name=='guru-merge-task-delivery':fact.update({'merge_commit':'b'*40,'target_ref':'origin/main'})
   public={'profile':'legacy_history_verification','root':str(root),'key':{'task_id':'selected','lifecycle_generation':0},'task_ref':'.trellis/tasks/old-task','fact_refs':[fact]}
   input_path=root/'input.json';input_path.write_text(json.dumps(public));before=input_path.read_bytes()
   with mock.patch.object(module.subprocess,'run',return_value=subprocess.CompletedProcess([],1,'','Unavailable')):
    result=module.maybe_run(PACKAGE,['--root',str(root),'--input',str(input_path)])
   self.assertEqual(result['exit_id'],'unverified_legacy_history');self.assertEqual(input_path.read_bytes(),before);self.assertEqual(list(root.iterdir()),[input_path])
if __name__=='__main__':unittest.main()
