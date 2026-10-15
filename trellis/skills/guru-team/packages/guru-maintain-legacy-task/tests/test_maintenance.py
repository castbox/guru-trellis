from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

PACKAGE=Path(__file__).resolve().parents[1]
SKILLS=PACKAGE.parents[1]
sys.path.insert(0,str(SKILLS))
sys.path.insert(0,str(PACKAGE/'runtime'))
import controls
spec=importlib.util.spec_from_file_location('selected_maintenance',PACKAGE/'runtime/invoke.py')
owner=importlib.util.module_from_spec(spec);spec.loader.exec_module(owner)
from runtime.io import CommandError

class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'repo';self.root.mkdir()
        self.git('init','-b','main');self.git('config','user.email','fixture@example.invalid');self.git('config','user.name','Fixture')
        self.write('.gitignore','.trellis/.runtime/\n');self.git('add','.gitignore');self.git('commit','-m','fixture')
        self.key={'task_id':'selected','lifecycle_generation':0};self.ref='.trellis/tasks/selected'
        self.write(self.ref+'/task.json',json.dumps({'id':'selected','name':'Selected','title':'Selected','status':'completed','creator':'fixture','assignee':'fixture','completedAt':'2025-01-01','pr_url':None}))
        self.write(self.ref+'/prd.md','original accepted scope\n')
    def tearDown(self):self.tmp.cleanup()
    def git(self,*args):return subprocess.check_output(['git',*args],cwd=self.root,stderr=subprocess.DEVNULL,text=True).strip()
    def write(self,ref,text):
        path=self.root/ref;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text);return path
    def test_target_native_official_dot_slash_entry(self):
        self.write('.trellis/scripts/get_context.py','print("target native")\n')
        out=owner.observe_native(self.root,[sys.executable,'./.trellis/scripts/get_context.py'])
        self.assertEqual(out['stdout'],'target native\n');self.assertEqual(out['returncode'],0)
    def test_packed_conversion_actual_native_next_owner_and_rollback(self):
        candidate_path=os.environ.get('TRELLIS_MAINTENANCE_CANDIDATE')
        if not candidate_path:self.skipTest('Set matching packed candidate.json')
        candidate=json.loads(Path(candidate_path).read_text());cli=Path(candidate_path).parent/'installed/node_modules/@mindfoldhq/trellis'
        source={'cli_package_root':str(cli),'dependency_mode':'local_candidate','expected_candidate':candidate['candidate']}
        shutil.copytree(cli/'dist/templates/trellis/scripts',self.root/'.trellis/scripts')
        shutil.copyfile(cli/'dist/templates/trellis/workflow-delivery-v1.md',self.root/'.trellis/workflow.md')
        self.write('.git/trellis/sessions/codex_fixture.json',json.dumps({'schema_version':2,**self.key}))
        old=json.loads((self.root/self.ref/'task.json').read_text())
        core_script="import {createRequire} from 'node:module';import {pathToFileURL} from 'node:url';const r=createRequire(process.argv[1]+'/package.json');const m=await import(pathToFileURL(r.resolve('@mindfoldhq/trellis-core/task/v2')));console.log(JSON.stringify(m.emptyTaskRecordV2({id:'selected',name:'Selected',title:'Selected'})));"
        projection=json.loads(subprocess.check_output(['node','--input-type=module','-e',core_script,str(cli)],text=True))
        inspected=owner.call(source,'inspectTaskTarget',{'root':str(self.root),'key':self.key,'task_ref':self.ref})
        original=(self.root/self.ref/'task.json').read_bytes()
        import hashlib
        authority={'locator':self.ref+'/prd.md','revision':'sha256:'+hashlib.sha256((self.root/self.ref/'prd.md').read_bytes()).hexdigest()}
        upstream={'root':str(self.root),'key':self.key,'task_ref':self.ref,'source_kind':'legacy','projection':projection,'artifacts':[{'path':a['path'],'action':'preserve','source':a['source']} for a in inspected['artifacts'] if a['kind']=='file' and a['path']!=self.ref+'/task.json'],'legacy_facts':[{'field':'completedAt','disposition':'source_snapshot','owner_id':'guru-maintain-legacy-task','reason':authority}],'sessions':[{'carrier':c,'action':'replace','delivery_id':None} for c in inspected['carriers']],'branch_binding':{'action':'establish','source':None,'record':{'schema_version':'1.0',**self.key,'binding_revision':1,'branch_name':'main'}}}
        public={'profile':'convert','source_ref':source,'target_checkout':str(self.root),'key':self.key,'task_ref':self.ref}
        prepared=owner.prepare(PACKAGE,public,{'upstream_input':upstream,'control_refs':{},'history_note':'Historical completedAt remains raw, current scope awaits actual planning.'});prepared['owner_recovery_refs']={}
        checkpoint=self.root/'.trellis/.runtime/guru-team/guru-maintain-legacy-task'/prepared['public_plan']['operation_id']/'checkpoint.json';owner.store(checkpoint,prepared)
        result=owner.resume(PACKAGE,checkpoint,prepared);self.assertEqual(result['exit_id'],'resume_required')
        converted=json.loads((self.root/self.ref/'task.json').read_text());self.assertEqual(converted['schema_version'],'2.0');self.assertEqual(converted['deliveries'],[]);self.assertEqual(converted['completion_results'],[])
        self.assertEqual((self.root/self.ref/'migration/source-task.json').read_bytes(),original)
        operation={'api_version':'1.0','operation':'accept_scope','key':self.key,'owner_role':'task_scope','owner_id':'trellis-start','authority':authority}
        env={**os.environ,'TRELLIS_CONTEXT_ID':'codex_fixture','PYTHONDONTWRITEBYTECODE':'1'}
        next_owner=subprocess.run([sys.executable,'.trellis/scripts/delivery.py','apply','--input',json.dumps(operation)],cwd=self.root,env=env,capture_output=True,text=True)
        self.assertEqual(next_owner.returncode,0,next_owner.stdout+next_owner.stderr)
        native=subprocess.run([sys.executable,'./.trellis/scripts/get_context.py','--mode','continuation'],cwd=self.root,env=env,capture_output=True,text=True)
        self.assertEqual(native.returncode,0,native.stdout+native.stderr)
        # Scope accepted by the actual next owner is later work: rollback preserves it.
        with self.assertRaises(CommandError):owner.call(source,'rollbackMaintenance',{'recovery_ref':prepared['upstream_recovery_ref']})
        self.assertEqual(json.loads((self.root/self.ref/'task.json').read_text())['accepted_scope'],authority)

    def test_normal_owner_edits_block_before_public_writes_on_initial_and_partial_freeze_resume(self):
        candidate_path=os.environ.get('TRELLIS_MAINTENANCE_CANDIDATE')
        if not candidate_path:self.skipTest('Set matching packed candidate.json')
        candidate=json.loads(Path(candidate_path).read_text());cli=Path(candidate_path).parent/'installed/node_modules/@mindfoldhq/trellis'
        source={'cli_package_root':str(cli),'dependency_mode':'local_candidate','expected_candidate':candidate['candidate']}
        public={'profile':'history_closeout','source_ref':source,'target_checkout':str(self.root),'key':self.key,'task_ref':self.ref}
        first='.trellis/.runtime/guru-team/guru-publish-task-delivery/state.json';second='.trellis/.runtime/guru-team/merge-task-delivery/state.json'
        payload={'public_input':{**self.key,'task_ref':self.ref}};self.write(first,json.dumps(payload));self.write(second,json.dumps(payload))
        original=(self.root/self.ref/'task.json').read_bytes()
        decision={'upstream_input':{'root':str(self.root),'key':self.key,'task_ref':self.ref,'source_kind':'legacy','archive_ref':'.trellis/tasks/archive/2026-10/selected','history_note':'External acceptance pending.','retirements':[]},'control_refs':{'guru-publish-task-delivery':[first],'guru-merge-task-delivery':[second]},'history_note':'External acceptance pending.'}
        prepared=owner.prepare(PACKAGE,public,decision);prepared['owner_recovery_refs']={}
        checkpoint=self.root/'.trellis/.runtime/guru-team/guru-maintain-legacy-task'/prepared['public_plan']['operation_id']/'checkpoint.json';owner.store(checkpoint,prepared)
        # A normal old-owner write occurs during the review pause.
        self.write(second,json.dumps(payload,indent=4))
        with self.assertRaises(CommandError) as raised:owner.resume(PACKAGE,checkpoint,prepared)
        self.assertEqual(raised.exception.code,'control_changed');self.assertEqual((self.root/self.ref/'task.json').read_bytes(),original)
        state=json.loads(checkpoint.read_text());self.assertEqual(set(state['owner_recovery_refs']),{'guru-publish-task-delivery'})
        # The second owner completes its ordinary write using its original formatting;
        # meanwhile the first owner has more normal work. Its frozen ref must recheck.
        self.write(second,json.dumps(payload));self.write(first,json.dumps(payload,indent=4))
        with self.assertRaises(CommandError) as raised:owner.resume(PACKAGE,checkpoint,state)
        self.assertEqual(raised.exception.code,'control_changed');self.assertEqual((self.root/self.ref/'task.json').read_bytes(),original)
        self.assertFalse((checkpoint.parent/'public').exists());self.assertTrue((self.root/first).exists());self.assertTrue((self.root/second).exists())
        self.assertEqual(json.loads(checkpoint.read_text())['public_plan']['operation_id'],prepared['public_plan']['operation_id'])

    def test_prepared_rollback_has_no_public_operation_and_preserves_task(self):
        candidate_path=os.environ.get('TRELLIS_MAINTENANCE_CANDIDATE')
        if not candidate_path:self.skipTest('Set matching packed candidate.json')
        candidate=json.loads(Path(candidate_path).read_text());cli=Path(candidate_path).parent/'installed/node_modules/@mindfoldhq/trellis'
        source={'cli_package_root':str(cli),'dependency_mode':'local_candidate','expected_candidate':candidate['candidate']}
        public={'profile':'history_closeout','source_ref':source,'target_checkout':str(self.root),'key':self.key,'task_ref':self.ref}
        decision={'upstream_input':{'root':str(self.root),'key':self.key,'task_ref':self.ref,'source_kind':'legacy','archive_ref':'.trellis/tasks/archive/2026-10/selected','history_note':'External acceptance pending.','retirements':[]},'control_refs':{},'history_note':'External acceptance pending.'}
        prepared=owner.prepare(PACKAGE,public,decision);prepared['owner_recovery_refs']={}
        checkpoint=self.root/'.trellis/.runtime/guru-team/guru-maintain-legacy-task'/prepared['public_plan']['operation_id']/'checkpoint.json';owner.store(checkpoint,prepared)
        original=(self.root/self.ref/'task.json').read_bytes();public_file=self.write('rollback.json',json.dumps({'profile':'rollback','recovery_ref':str(checkpoint)}))
        result=owner.run(PACKAGE,{},['--root',str(self.root),'--input',str(public_file)])
        self.assertEqual(result,{'exit_id':'rolled_back','key':self.key});self.assertEqual((self.root/self.ref/'task.json').read_bytes(),original);self.assertFalse((checkpoint.parent/'public').exists())

    def test_packed_public_closeout_fixed_recovery_and_owner_barrier(self):
        candidate_path=os.environ.get('TRELLIS_MAINTENANCE_CANDIDATE')
        if not candidate_path:self.skipTest('Set TRELLIS_MAINTENANCE_CANDIDATE to matching packed candidate.json')
        candidate=json.loads(Path(candidate_path).read_text());cli=Path(candidate_path).parent/'installed/node_modules/@mindfoldhq/trellis'
        source={'cli_package_root':str(cli),'dependency_mode':'local_candidate','expected_candidate':candidate['candidate']}
        public={'profile':'history_closeout','source_ref':source,'target_checkout':str(self.root),'key':self.key,'task_ref':self.ref}
        control='.trellis/.runtime/guru-team/guru-publish-task-delivery/state.json';self.write(control,json.dumps({'input':{**self.key,'task_ref':self.ref}}))
        decision={'upstream_input':{'root':str(self.root),'key':self.key,'task_ref':self.ref,'source_kind':'legacy','archive_ref':'.trellis/tasks/archive/2026-10/selected','history_note':'Delivered history; external acceptance remains pending.','retirements':[]},'control_refs':{'guru-publish-task-delivery':[control]},'history_note':'External acceptance remains pending.'}
        before=(self.root/self.ref/'task.json').read_bytes();prepared=owner.prepare(PACKAGE,public,decision)
        self.assertEqual((self.root/self.ref/'task.json').read_bytes(),before)
        checkpoint=self.root/'.trellis/.runtime/guru-team/guru-maintain-legacy-task'/prepared['public_plan']['operation_id']/'checkpoint.json';prepared['owner_recovery_refs']={who:owner.owner_call(PACKAGE,who,{'profile':'legacy_control_freeze','root':str(self.root),'key':self.key,'task_ref':self.ref,'controls':rows,'source':controls.raw(self.root/self.ref/'task.json'),'operation_id':prepared['public_plan']['operation_id']})['recovery_ref'] for who,rows in prepared['controls'].items()};owner.store(checkpoint,prepared)
        result=owner.resume(PACKAGE,checkpoint,prepared)
        self.assertEqual(result['exit_id'],'resume_required');self.assertFalse((self.root/self.ref).exists());self.assertFalse((self.root/control).exists())
        archive=self.root/'.trellis/tasks/archive/2026-10/selected';self.assertEqual((archive/'task.json').read_bytes(),before)
        self.assertIn('external acceptance', (archive/'maintenance-history.md').read_text())
        operation_id=prepared['public_plan']['operation_id'];again=owner.resume(PACKAGE,checkpoint,json.loads(checkpoint.read_text()))
        self.assertEqual(again['recovery_ref'],str(checkpoint));self.assertEqual(json.loads(checkpoint.read_text())['public_plan']['operation_id'],operation_id)

if __name__=='__main__':unittest.main()
