"""Actual installed public reopen plus the retained sealed Finish transaction."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from runtime.delivery_projection.tests.test_installed_projection import DECLARATION
from runtime.delivery_projection.tests.upstream_fixture import scripts_source
from runtime.delivery_projection import DeliveryProjection, authority_ref
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore

PACKAGE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('delivery_reactivate_test_owner',PACKAGE/'runtime/invoke.py')
owner=importlib.util.module_from_spec(spec);spec.loader.exec_module(owner)

class DeliveryReactivateTests(unittest.TestCase):
    def git(self,root,*args):
        return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
    def run_transaction(self,adopt):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'repo';root.mkdir();self.git(root,'init','-q','-b','main')
            self.git(root,'config','user.name','Test');self.git(root,'config','user.email','test@example.invalid')
            shutil.copytree(scripts_source(),root/'.trellis/scripts')
            (root/'.trellis/workflow.md').write_text('[trellis-runtime-contract]\n'+json.dumps(DECLARATION)+'\n[/trellis-runtime-contract]\n')
            (root/'.trellis/.developer').write_text('fixture\n')
            (root/'.gitignore').write_text('.trellis/.runtime/\n')
            (root/'scope.md').write_text('完整保留 Task 的 scope 与下一次工作\n')
            # The official writer constructs the public aggregate; no Guru substitute.
            created=subprocess.run([sys.executable,str(root/'.trellis/scripts/task.py'),'create','重开验证','--slug','reactivate',
                            '--task-id','reactivate','--description','已正常完成后继续工作','--schema-version','2.0',
                            '--source-json','{"kind":"no_issue"}','--base-branch','main','--no-start'],cwd=root,capture_output=True,text=True)
            self.assertEqual(created.returncode,0,created.stderr+created.stdout)
            task=next(p.parent for p in (root/'.trellis/tasks').glob('*/task.json'))
            projection=DeliveryProjection(root,task.relative_to(root).as_posix());authority=authority_ref(root/'scope.md',root)
            projection.scope(authority)
            key={'task_id':'reactivate','lifecycle_generation':0}
            completion={'result_id':'completion:reactivate','owner_id':DECLARATION['owners']['completion'],'evidence':[authority],
                        'lifecycle_generation':0,'accepted_scope':authority,'delivery_result_ids':[],'outcome':'completed'}
            projection.apply({'api_version':'1.0','operation':'complete_task','key':key,'owner_role':'completion',
                              'owner_id':DECLARATION['owners']['completion'],'result':completion})
            closure={'result_id':'closure:reactivate','owner_id':DECLARATION['owners']['closure'],'evidence':[authority],
                     'lifecycle_generation':0,'completion_result_id':completion['result_id'],'disposition':'no_mutation','source_result':None}
            projection.apply({'api_version':'1.0','operation':'close_task','key':key,'owner_role':'closure',
                              'owner_id':DECLARATION['owners']['closure'],'result':closure})
            archive=root/'.trellis/tasks/archive/2026-10'/task.name;archive.parent.mkdir(parents=True);task.rename(archive)
            archive_ref=archive.relative_to(root).as_posix();active_ref='.trellis/tasks/'+task.name
            (archive/'finish-summary.json').write_text(json.dumps({'schema_version':2,'task':{'archive_dir':archive_ref,'artifact_dir':active_ref,'status':'completed'}}))
            self.git(root,'add','.');self.git(root,'commit','-qm','sealed archive');head=self.git(root,'rev-parse','HEAD')
            repository=inspect_repository(root);old_key=TaskLifecycleKey('reactivate',0)
            binding=BranchBindingStore(repository).establish(old_key,'task-old')
            ledger=ResourceLedgerStore(repository);ledger.establish_current(old_key,binding_revision=0,branch_name='task-old',branch_ownership='caller_owned',worktree_ownership='not_applicable')
            ledger.seal_for_finish(old_key,finish_result_id='finish:v1:1234567890abcdef',finish_head=head)
            finish=root/'.trellis/.runtime/guru-team/finish';finish.mkdir(parents=True)
            (finish/'1234567890abcdef.json').write_text(json.dumps({'schema_version':'2.0','stage':'success','task_ref':active_ref,
                'task_id':'reactivate','closure_result_id':'closure:reactivate','finish_ref':'finish:v1:1234567890abcdef','lifecycle_generation':0,
                'repo_ref':'castbox/guru-trellis','base_branch':'main','head_branch':'task-old','expected_base_head':head,'archive_ref':archive_ref,
                'parent_head':head,'commit':head,'pr_number':1,'pr_url':'https://github.com/castbox/guru-trellis/pull/1','target_head':head}))
            checkout=root if adopt else Path(directory)/'linked'
            if adopt:self.git(root,'switch','-qc','task-next')
            public={'profile':'delivery_reactivate_completed_task','mode':'standalone','archived_lifecycle':key}
            acquisition={'task_id':'reactivate','task_ref':active_ref,'lifecycle_generation':1,'route':'adopt_invocation_checkout' if adopt else 'provision_linked_worktree',
                'branch_ref':'refs/heads/task-next','decision_head':head,'task_artifact_expectation':'absent','transaction_id':'reactivate:1','result_id':'reactivate-result:1'}
            if adopt:acquisition['invocation_checkout']=str(checkout)
            else:acquisition.update(target_path=str(checkout),provision_disposition='new_branch')
            semantic={**public,'route':'session_binding_recovery_required','reason_refs':['新增受审查工作'],'selected_base_ref':'refs/heads/main',
                      'reviewed_base_head':head,'session_outcome':'recovery_required','acquisition':acquisition,'authority':authority}
            first=owner.execute(root,public,semantic)
            self.assertEqual(first,{'exit_id':'session_binding_recovery_required','task_id':'reactivate','lifecycle_generation':1})
            record=DeliveryProjection(checkout,active_ref).read_record();self.assertNotIn('status',record)
            self.assertEqual(record['lifecycle_generation'],1);self.assertEqual(record['completion_results'],[completion]);self.assertEqual(record['closure_results'],[closure])
            before=(checkout/active_ref/'task.json').read_bytes();bindings=BranchBindingStore(repository).read(TaskLifecycleKey('reactivate',1))
            self.assertEqual(owner.execute(root,public,semantic),first)
            semantic_path=Path(directory)/'semantic.json';semantic_path.write_text(json.dumps(semantic))
            invoked=subprocess.run(['bash',str(PACKAGE/'scripts/invoke.sh'),'--root',str(root),'--input','-',
                                    '--semantic-result',str(semantic_path)],input=json.dumps(public),text=True,capture_output=True)
            self.assertEqual(invoked.returncode,0,invoked.stderr+invoked.stdout)
            self.assertEqual(json.loads(invoked.stdout),first)
            self.assertEqual((checkout/active_ref/'task.json').read_bytes(),before)
            self.assertEqual(BranchBindingStore(repository).read(TaskLifecycleKey('reactivate',1)),bindings)
            resumed=owner.execute(root,public,{**semantic,'route':'resume_reactivation'})
            self.assertEqual(resumed['exit_id'],'resume_reactivation')
    def test_new_linked_checkout_reopens_once(self):self.run_transaction(False)
    def test_adopt_checkout_reopens_once(self):self.run_transaction(True)

if __name__=='__main__':unittest.main()
