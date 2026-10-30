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
 def test_stdin_profile_read_failure_is_a_safe_input_error(self):
  from unittest.mock import patch
  invoke_spec=importlib.util.spec_from_file_location('finish_input_read_failure',PACKAGE/'runtime/invoke.py')
  invoke=importlib.util.module_from_spec(invoke_spec);invoke_spec.loader.exec_module(invoke)
  for failure in (OSError('sensitive read error'),UnicodeDecodeError('utf-8',b'\xff',0,1,'sensitive encoding error')):
   with self.subTest(failure=type(failure).__name__), patch('sys.stdin') as stream:
    stream.read.side_effect=failure
    with self.assertRaises(CommandError) as caught:
     invoke.run(PACKAGE,{},['--input','-'])
   error=caught.exception
   self.assertEqual((error.code,error.field_path,error.exit_status),('invalid_json','input',2))
   self.assertIn('Cannot read JSON from stdin',error.remediation)
   self.assertNotIn('sensitive',error.remediation)
 def test_stdin_profile_text_is_not_reinterpreted_as_a_file(self):
  import io
  from contextlib import chdir
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as directory, chdir(directory):
   Path('1').write_text(json.dumps({'profile':'legacy_history_verification'}),encoding='utf-8')
   invoke_spec=importlib.util.spec_from_file_location('finish_input_profile',PACKAGE/'runtime/invoke.py')
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
 def test_a32_hashed_finalizer_controls_without_generation(self):
  import hashlib
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);key={'task_id':'selected','lifecycle_generation':0};task_ref='.trellis/tasks/legacy-slug'
   task=root/task_ref;task.mkdir(parents=True);(task/'task.json').write_text(json.dumps({'id':'selected','status':'completed'}))
   token=hashlib.sha256(b'selected').hexdigest()[:20]
   transaction='.trellis/.runtime/guru-team/finalization-transaction/'+token+'/finalization-transaction.json'
   gate='.trellis/.runtime/guru-team/owner-checkpoints/'+token+'/task-finalization-gate.json'
   for ref,payload in [(transaction,{'schema_version':'3.0','skill_id':'guru-finalize-task','task_ref':task_ref}),(gate,{'schema_version':'5.0','identity':{'task_ref':task_ref}})]:
    path=root/ref;path.parent.mkdir(parents=True);path.write_text(json.dumps(payload))
   result=module.execute(PACKAGE,{'profile':'legacy_control_inspection','root':str(root),'key':key,'task_ref':task_ref,'control_refs':[transaction,gate]})
   self.assertEqual([r['path'] for r in result['controls']],[transaction,gate])
if __name__=='__main__':unittest.main()
